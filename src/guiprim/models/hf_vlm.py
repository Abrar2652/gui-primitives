"""Hugging Face VLM wrappers for the open models in the diagnostic.

Supported families: qwen2_5_vl, internvl, mllama (Llama-3.2-Vision).
Heavy imports (torch, transformers) are deferred to construction time so the
pure-python parts of the repo import cleanly without a GPU stack.

ATTENTION CAPTURE — read before relying on it
----------------------------------------------
`capture_attention` returns attention from image tokens. The *index range* of
image tokens in the sequence, and the spatial (rows, cols) layout of the patch
grid, are MODEL-SPECIFIC. The Qwen2.5-VL path below is implemented and tested
against the processor's grid metadata. For InternVL / mllama the hooks are in
place but the image-token localization MUST be verified against the processor
output before the steering experiments are trusted (see CLAUDE.md, "Gotchas").
"""
from __future__ import annotations
from typing import Any

from .base import GroundingResult, VLMWrapper
from ..inference.parsing import parse_coordinate

_GROUNDING_SYS = (
    "You are a GUI grounding assistant. Given a screenshot and an instruction, "
    "respond with ONLY the pixel coordinate to click, formatted exactly as "
    "click(x, y). Do not explain.")


class HFVLMWrapper(VLMWrapper):
    def __init__(self, cfg: dict[str, Any]):
        super().__init__(cfg)
        import torch
        from transformers import AutoProcessor
        self._torch = torch
        dtype = {"bfloat16": torch.bfloat16, "float16": torch.float16,
                 "float32": torch.float32}[cfg.get("dtype", "bfloat16")]
        self.processor = AutoProcessor.from_pretrained(cfg["hf_id"], trust_remote_code=True)
        self.model = self._load_model(cfg, dtype)
        self.model.eval()

    def _load_model(self, cfg, dtype):
        from transformers import AutoModelForCausalLM, AutoModelForImageTextToText
        kw = dict(torch_dtype=dtype, device_map=cfg.get("device_map", "auto"),
                  trust_remote_code=True)
        try:
            return AutoModelForImageTextToText.from_pretrained(cfg["hf_id"], **kw)
        except Exception:
            return AutoModelForCausalLM.from_pretrained(cfg["hf_id"], **kw)

    # ------------------------------ inference ------------------------------
    def _build_inputs(self, image_path: str, instruction: str, system: str):
        from PIL import Image
        image = Image.open(image_path).convert("RGB")
        # PaliGemma 2: use `<image>detect TARGET` which returns
        # `<loc####><loc####><loc####><loc####>` tokens encoding
        # y_min, x_min, y_max, x_max in 1024-normalized space, followed
        # by the detected class label.  Our parser handles the <loc> form.
        if self.family == "paligemma2":
            text = f"<image>detect {instruction}"
            inputs = self.processor(text=[text], images=[image],
                                     return_tensors="pt")
            return ({k: v.to(self.model.device) for k, v in inputs.items()},
                    image.size)
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": instruction}]},
        ]
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True)
        inputs = self.processor(text=[text], images=[image], return_tensors="pt")
        return {k: v.to(self.model.device) for k, v in inputs.items()}, image.size

    def ground(self, image_path: str, instruction: str,
               system: str | None = None) -> GroundingResult:
        sys = system or _GROUNDING_SYS
        inputs, (W, H) = self._build_inputs(image_path, instruction, sys)
        with self._torch.no_grad():
            out = self.model.generate(**inputs, max_new_tokens=128, do_sample=False)
        gen = out[0][inputs["input_ids"].shape[1]:]
        # PaliGemma encodes coordinates as <loc####> SPECIAL tokens; keep them.
        skip_special = (self.family != "paligemma2")
        text = self.processor.decode(gen, skip_special_tokens=skip_special)
        xy = parse_coordinate(text, image_wh=(W, H), coord_space=self.coord_space)
        return GroundingResult(raw_text=text, pred_xy=xy,
                               meta={"image_wh": (W, H)})

    # -------------------------- attention capture --------------------------
    def capture_attention(self, image_path: str, instruction: str) -> dict[str, Any]:
        if not self.supports_attention_capture:
            raise NotImplementedError(self.key)
        inputs, _ = self._build_inputs(image_path, instruction, _GROUNDING_SYS)
        with self._torch.no_grad():
            out = self.model(**inputs, output_attentions=True, use_cache=False)
        # attentions: tuple[L] of tensor[B, H, T, T]; take the last query position.
        attn = self._torch.stack([a[0, :, -1, :] for a in out.attentions])  # [L,H,T]
        start, end, grid = self._image_token_span(inputs)
        img_attn = attn[:, :, start:end]                                    # [L,H,Timg]
        return {"attn": img_attn.float().cpu(), "image_token_index": (start, end),
                "grid": grid}

    def _image_token_span(self, inputs) -> tuple[int, int, tuple[int, int]]:
        """Locate image tokens and the patch grid. Qwen2.5-VL path implemented."""
        if self.family == "qwen2_5_vl":
            ids = inputs["input_ids"][0]
            img_tok = self.model.config.image_token_id
            mask = (ids == img_tok).nonzero(as_tuple=True)[0]
            if len(mask) == 0:
                raise RuntimeError("no image tokens found; check processor version")
            start, end = int(mask[0]), int(mask[-1]) + 1
            # grid_thw -> (t, h, w) patch counts; merged by spatial_merge_size.
            thw = inputs["image_grid_thw"][0].tolist()
            m = getattr(self.model.config.vision_config, "spatial_merge_size", 2)
            return start, end, (thw[1] // m, thw[2] // m)
        raise NotImplementedError(
            f"verify image-token span for family '{self.family}' before use "
            "(see hf_vlm.py docstring)")

    def cleanup(self) -> None:
        import gc
        del self.model
        gc.collect()
        if self._torch.cuda.is_available():
            self._torch.cuda.empty_cache()
