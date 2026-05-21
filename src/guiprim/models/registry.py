"""Model factory. Dispatches a model config to the right wrapper, including a
deterministic Dummy model used by `make smoke` and CI (no GPU, no network)."""
from __future__ import annotations
import hashlib
from typing import Any

from .base import GroundingResult, VLMWrapper


class DummyModel(VLMWrapper):
    """Deterministic stub: returns a coordinate hashed from the instruction so
    that the full pipeline (inference -> eval -> stats -> figures) can be wired
    and tested without any model weights."""

    def ground(self, image_path: str, instruction: str,
               system: str | None = None) -> GroundingResult:
        from PIL import Image
        W, H = Image.open(image_path).size
        h = int(hashlib.md5(instruction.encode()).hexdigest(), 16)
        x, y = (h % W), ((h // W) % H)
        return GroundingResult(raw_text=f"click({x}, {y})", pred_xy=(x, y),
                               meta={"image_wh": (W, H), "dummy": True})


def build_model(model_cfg: dict[str, Any]) -> VLMWrapper:
    fam = model_cfg["family"]
    if fam == "dummy":
        return DummyModel(model_cfg)
    if fam in ("openai_api", "closed_api"):
        from .closed_api import ClosedAPIWrapper
        return ClosedAPIWrapper(model_cfg)
    if fam in ("qwen2_5_vl", "qwen2_vl", "mllama",
               "idefics3", "pixtral", "gemma3", "paligemma2"):
        from .hf_vlm import HFVLMWrapper
        return HFVLMWrapper(model_cfg)
    if fam in ("internvl", "internvl3"):
        from .chat_vlm import InternVL3Wrapper
        return InternVL3Wrapper(model_cfg)
    if fam == "deepseek_vl2":
        from .chat_vlm import DeepSeekVL2Wrapper
        return DeepSeekVL2Wrapper(model_cfg)
    if fam == "ollama":
        from .ollama_vlm import OllamaWrapper
        return OllamaWrapper(model_cfg)
    raise ValueError(f"unknown model family: {fam}")
