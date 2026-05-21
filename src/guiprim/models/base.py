"""Model abstraction.

Every model — open or closed — is a `VLMWrapper` exposing a single grounding
call. Interventions never touch model-specific code: they wrap a VLMWrapper.
Attention capture is optional and advertised via `supports_attention_capture`.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class GroundingResult:
    """One model response on one item."""
    raw_text: str
    pred_xy: tuple[float, float] | None      # parsed pixel coordinate, if any
    meta: dict[str, Any] = field(default_factory=dict)


class VLMWrapper(ABC):
    """Common interface. `cfg` is the loaded model YAML."""

    def __init__(self, cfg: dict[str, Any]):
        self.cfg = cfg
        self.key: str = cfg["key"]
        self.family: str = cfg["family"]
        self.coord_space: str = cfg.get("coord_space", "pixel")
        self.supports_attention_capture: bool = bool(
            cfg.get("supports_attention_capture", False))

    @abstractmethod
    def ground(self, image_path: str, instruction: str,
               system: str | None = None) -> GroundingResult:
        """Return the model's grounding response for one (image, instruction)."""

    # --- optional internals hooks (only for open models, used by interventions) ---
    def capture_attention(self, image_path: str, instruction: str) -> dict[str, Any]:
        """Return per-(layer,head) attention over image tokens for one input.

        Implemented only by open HF models with `supports_attention_capture`.
        Returns {'attn': tensor[L,H,Timg], 'image_token_index': (start,end),
                 'grid': (rows,cols)} or raises NotImplementedError.
        """
        raise NotImplementedError(f"{self.key} does not support attention capture")

    def cleanup(self) -> None:
        """Free GPU memory. Override in GPU-backed wrappers."""
