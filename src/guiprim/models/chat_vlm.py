"""Wrapper for VLMs whose inference API is `model.chat()` rather than the
generic HF `AutoProcessor(images=..., text=...)` path.

Two families share this style:
  * InternVL3 / InternVL3_5 (OpenGVLab) — `model.chat(tokenizer, pixel_values,
    question, generation_config)`; image preprocessed via a custom
    tile-builder.
  * DeepSeek-VL2 — packaged as a separate Python module
    (`deepseek_vl2.models`) with its own processor returning ready-to-feed
    inputs; not present in transformers proper.

This wrapper dispatches on `family` and adapts each to our `VLMWrapper`
interface so downstream code (inference runner, eval, regression) does not
care which backend produced the prediction.
"""
from __future__ import annotations
from typing import Any

from .base import GroundingResult, VLMWrapper
from ..inference.parsing import parse_coordinate


_GROUNDING_SYS = (
    "You are a GUI grounding assistant. Given a screenshot and an "
    "instruction, respond with ONLY the pixel coordinate to click, "
    "formatted exactly as click(x, y). Do not explain.")


# --------------------------- InternVL3 ----------------------------------
def _internvl_load_image(image_path: str, input_size: int = 448,
                        max_num: int = 12):
    """Replicate the official InternVL3 tile-based image preprocessing
    (dynamic high-resolution input). Returns a torch.Tensor [N_tiles, 3, H, W]."""
    import torch
    import torchvision.transforms as T
    from torchvision.transforms.functional import InterpolationMode
    from PIL import Image
    IMAGENET_MEAN = (0.485, 0.456, 0.406)
    IMAGENET_STD = (0.229, 0.224, 0.225)

    transform = T.Compose([
        T.Lambda(lambda img: img.convert("RGB") if img.mode != "RGB" else img),
        T.Resize((input_size, input_size),
                 interpolation=InterpolationMode.BICUBIC),
        T.ToTensor(),
        T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])

    def find_closest_aspect_ratio(ar, target_ratios, w, h, size):
        best = float("inf"); best_ratio = (1, 1); area = w * h
        for ratio in target_ratios:
            target_ar = ratio[0] / ratio[1]
            ratio_diff = abs(ar - target_ar)
            if ratio_diff < best:
                best = ratio_diff; best_ratio = ratio
            elif ratio_diff == best and area > 0.5 * size * size * ratio[0] * ratio[1]:
                best_ratio = ratio
        return best_ratio

    def dynamic_preprocess(image, min_num=1, max_num=12, image_size=448):
        ow, oh = image.size
        ar = ow / oh
        target_ratios = set((i, j) for n in range(min_num, max_num + 1)
                            for i in range(1, n + 1) for j in range(1, n + 1)
                            if min_num <= i * j <= max_num)
        target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])
        tr = find_closest_aspect_ratio(ar, target_ratios, ow, oh, image_size)
        tw = image_size * tr[0]; th = image_size * tr[1]
        blocks = tr[0] * tr[1]
        resized = image.resize((tw, th))
        processed = []
        for i in range(blocks):
            box = ((i % (tw // image_size)) * image_size,
                   (i // (tw // image_size)) * image_size,
                   ((i % (tw // image_size)) + 1) * image_size,
                   ((i // (tw // image_size)) + 1) * image_size)
            processed.append(resized.crop(box))
        # Thumbnail (full image at base resolution) as last tile
        if len(processed) != 1:
            processed.append(image.resize((image_size, image_size)))
        return processed

    image = Image.open(image_path).convert("RGB")
    images = dynamic_preprocess(image, image_size=input_size, max_num=max_num)
    pixel_values = torch.stack([transform(i) for i in images])
    return pixel_values


class InternVL3Wrapper(VLMWrapper):
    """Generic InternVL3 / InternVL3.5 wrapper using model.chat()."""

    def __init__(self, cfg: dict[str, Any]):
        super().__init__(cfg)
        import torch
        from transformers import AutoTokenizer, AutoModel
        self._torch = torch
        dtype = {"bfloat16": torch.bfloat16, "float16": torch.float16,
                 "float32": torch.float32}[cfg.get("dtype", "bfloat16")]
        self.tokenizer = AutoTokenizer.from_pretrained(
            cfg["hf_id"], trust_remote_code=True, use_fast=False)
        self.model = AutoModel.from_pretrained(
            cfg["hf_id"], torch_dtype=dtype,
            device_map=cfg.get("device_map", "auto"),
            trust_remote_code=True).eval()

    def ground(self, image_path: str, instruction: str,
               system: str | None = None) -> GroundingResult:
        from PIL import Image
        W, H = Image.open(image_path).size
        sys_msg = system or _GROUNDING_SYS
        question = (f"<image>\n{sys_msg}\n\n{instruction}")
        pixel_values = _internvl_load_image(
            image_path, max_num=12).to(self.model.dtype).to(self.model.device)
        generation_config = dict(max_new_tokens=128, do_sample=False)
        try:
            response = self.model.chat(
                self.tokenizer, pixel_values, question, generation_config)
        except Exception as e:
            return GroundingResult(raw_text=f"[ERR:{str(e)[:80]}]",
                                   pred_xy=None,
                                   meta={"image_wh": (W, H)})
        xy = parse_coordinate(response, image_wh=(W, H),
                              coord_space=self.coord_space)
        return GroundingResult(raw_text=response, pred_xy=xy,
                               meta={"image_wh": (W, H)})

    def cleanup(self) -> None:
        import gc
        del self.model
        gc.collect()
        if self._torch.cuda.is_available():
            self._torch.cuda.empty_cache()


# --------------------------- DeepSeek-VL2 -------------------------------
class DeepSeekVL2Wrapper(VLMWrapper):
    """DeepSeek-VL2 wrapper using its bespoke `deepseek_vl2` Python package."""

    def __init__(self, cfg: dict[str, Any]):
        super().__init__(cfg)
        import torch
        from deepseek_vl2.models import (DeepseekVLV2ForCausalLM,
                                          DeepseekVLV2Processor)
        self._torch = torch
        dtype = {"bfloat16": torch.bfloat16, "float16": torch.float16,
                 "float32": torch.float32}[cfg.get("dtype", "bfloat16")]
        self.processor = DeepseekVLV2Processor.from_pretrained(cfg["hf_id"])
        self.tokenizer = self.processor.tokenizer
        self.model = DeepseekVLV2ForCausalLM.from_pretrained(
            cfg["hf_id"], torch_dtype=dtype,
            device_map=cfg.get("device_map", "auto"),
            trust_remote_code=True).eval()

    def ground(self, image_path: str, instruction: str,
               system: str | None = None) -> GroundingResult:
        from PIL import Image
        W, H = Image.open(image_path).size
        sys_msg = system or _GROUNDING_SYS
        conversation = [{
            "role": "<|User|>",
            "content": f"<image>\n{sys_msg}\n\n{instruction}",
            "images": [image_path],
        }, {"role": "<|Assistant|>", "content": ""}]
        try:
            pil_images = [Image.open(image_path).convert("RGB")]
            prepare = self.processor(
                conversations=conversation, images=pil_images,
                force_batchify=True, system_prompt=""
            ).to(self.model.device)
            with self._torch.no_grad():
                outputs = self.model.language_model.generate(
                    inputs_embeds=self.model.prepare_inputs_embeds(**prepare),
                    attention_mask=prepare.attention_mask,
                    pad_token_id=self.tokenizer.eos_token_id,
                    bos_token_id=self.tokenizer.bos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    max_new_tokens=128, do_sample=False, use_cache=True)
            text = self.tokenizer.decode(outputs[0].cpu().tolist(),
                                         skip_special_tokens=True)
        except Exception as e:
            return GroundingResult(raw_text=f"[ERR:{str(e)[:80]}]",
                                   pred_xy=None,
                                   meta={"image_wh": (W, H)})
        xy = parse_coordinate(text, image_wh=(W, H),
                              coord_space=self.coord_space)
        return GroundingResult(raw_text=text, pred_xy=xy,
                               meta={"image_wh": (W, H)})

    def cleanup(self) -> None:
        import gc
        del self.model
        gc.collect()
        if self._torch.cuda.is_available():
            self._torch.cuda.empty_cache()
