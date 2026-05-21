"""Closed-model wrapper. Used as a non-Qwen-lineage reference on the
human-verified core split. A hard item cap (api.max_items) protects the budget.

Supports three providers:
  openai     OpenAI Chat Completions (GPT-4o-mini, GPT-4o, GPT-4.1, ...)
  anthropic  Anthropic Messages (Claude Haiku, Sonnet, Opus, ...)
  google     Google Generative AI (Gemini 1.5 / 2.0 Flash, Pro, ...)
"""
from __future__ import annotations
import base64
import os
import re
import time
from typing import Any

from .base import GroundingResult, VLMWrapper
from ..inference.parsing import parse_coordinate


def _with_retry(call, max_attempts: int = 10):
    """Retry an API call on 429 / 5xx with exponential backoff. The OpenAI
    TPM limit on gpt-4o-mini is ~200k tokens/min, and each high-res
    screenshot eats ~37k input tokens, so a serial loop quickly hits the
    cap; the backoff makes the wrapper safe without changing the runner.
    Honors the API's `Please try again in Xms.` hint when present.
    """
    delay = 2.0
    for attempt in range(max_attempts):
        try:
            return call()
        except Exception as e:
            msg = str(e)
            transient = ("429" in msg or "rate" in msg.lower()
                         or "5" in msg[:5] and " 5" in msg
                         or "overloaded" in msg.lower())
            if not transient or attempt == max_attempts - 1:
                raise
            # Parse explicit "try again in Xms" hints (OpenAI), else exponential.
            wait_s = delay
            m = re.search(r"try again in ([\d.]+)([ms]+)", msg)
            if m:
                v, unit = float(m.group(1)), m.group(2)
                wait_s = v / 1000.0 if "ms" in unit else v
            wait_s = max(wait_s, delay)
            time.sleep(wait_s)
            delay = min(delay * 2, 120.0)
    raise RuntimeError("unreachable")

_SYS = ("You are a GUI grounding assistant. Given a screenshot and an "
        "instruction, reply with ONLY the click coordinate as click(x, y) "
        "in pixels of the provided image. No explanation.")


class ClosedAPIWrapper(VLMWrapper):
    def __init__(self, cfg: dict[str, Any]):
        super().__init__(cfg)
        api = cfg.get("api", {})
        self.provider = api.get("provider", "openai")
        env_default = {"openai": "OPENAI_API_KEY",
                       "anthropic": "ANTHROPIC_API_KEY",
                       "google": "GOOGLE_API_KEY"}[self.provider]
        env_key = api.get("env_key", env_default)
        key = os.environ.get(env_key)
        if not key:
            raise RuntimeError(f"set {env_key} for the closed model")
        self.model_id = cfg["hf_id"]
        self.max_items = int(api.get("max_items", 250))
        self._used = 0
        self._init_client(key)

    def _init_client(self, key: str) -> None:
        if self.provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=key)
        elif self.provider == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic(api_key=key)
        elif self.provider == "google":
            import google.generativeai as genai
            genai.configure(api_key=key)
            self.client = genai.GenerativeModel(self.model_id)
        else:
            raise ValueError(f"unknown provider {self.provider!r}")

    def ground(self, image_path: str, instruction: str,
               system: str | None = None) -> GroundingResult:
        if self._used >= self.max_items:
            return GroundingResult(raw_text="", pred_xy=None,
                                   meta={"skipped": "budget_cap"})
        from PIL import Image
        import io
        W, H = Image.open(image_path).size
        sys_msg = system or _SYS
        prompt = sys_msg + "\n\n" + instruction

        # All three closed providers (OpenAI, Anthropic, Google) internally
        # downsample large images, and the model returns coordinates in that
        # downsampled frame. To keep predictions interpretable in original
        # pixel coordinates we pre-resize to MAX_DIM=1500 ourselves and
        # scale pred_xy back at the end.
        MAX_DIM = 1500
        scale_back = 1.0
        if max(W, H) > MAX_DIM:
            scale = MAX_DIM / max(W, H)
            scale_back = 1.0 / scale
        else:
            scale = 1.0

        if self.provider == "openai":
            if scale < 1.0:
                img = Image.open(image_path).convert("RGB")
                new_w = int(W * scale); new_h = int(H * scale)
                img = img.resize((new_w, new_h), Image.LANCZOS)
                buf = io.BytesIO(); img.save(buf, format="PNG", optimize=True)
                b64 = base64.b64encode(buf.getvalue()).decode()
            else:
                b64 = base64.b64encode(open(image_path, "rb").read()).decode()
            kw = dict(model=self.model_id,
                      messages=[
                          {"role": "system", "content": sys_msg},
                          {"role": "user", "content": [
                              {"type": "text", "text": instruction},
                              {"type": "image_url",
                               "image_url": {"url": f"data:image/png;base64,{b64}"}}]}])
            # GPT-5 family is a reasoning model: uses `max_completion_tokens`
            # and forbids `temperature` (always greedy). Older 4.x/4o families
            # take `max_tokens` + optional `temperature`.
            if self.model_id.startswith(("gpt-5", "o1", "o3", "o4")):
                # Reasoning models burn budget on internal `reasoning_tokens`
                # before emitting visible text. 1024 was too small, 4096 left
                # ~3% of items still hitting the cap. 8192 mops up the
                # remaining stragglers.
                kw["max_completion_tokens"] = 8192
            else:
                kw["max_tokens"] = 256
                kw["temperature"] = 0.0
            resp = _with_retry(lambda: self.client.chat.completions.create(**kw))
            text = resp.choices[0].message.content or ""

        elif self.provider == "anthropic":
            # Anthropic's vision API enforces:
            #   * <= 5 MB base64 payload per image
            #   * effective max-side ~1568 px (server downsamples larger images)
            # We pre-resize so we (a) stay under 5 MB and (b) know the exact
            # coord-frame the model is reasoning in, so we can scale pred_xy
            # back to original pixel space ourselves.
            from PIL import Image
            import io
            img = Image.open(image_path).convert("RGB")
            orig_w, orig_h = img.size
            MAX_DIM = 1500   # slight buffer below Anthropic's 1568 limit
            scale_back = 1.0
            if max(orig_w, orig_h) > MAX_DIM:
                scale = MAX_DIM / max(orig_w, orig_h)
                new_w = int(orig_w * scale)
                new_h = int(orig_h * scale)
                img = img.resize((new_w, new_h), Image.LANCZOS)
                scale_back = 1.0 / scale
            buf = io.BytesIO()
            img.save(buf, format="PNG", optimize=True)
            png_bytes = buf.getvalue()
            # If still > 4.5 MB (rare for typical screenshots), further shrink.
            while len(png_bytes) > 4_500_000 and max(img.size) > 400:
                new_w = int(img.size[0] * 0.85)
                new_h = int(img.size[1] * 0.85)
                img = img.resize((new_w, new_h), Image.LANCZOS)
                scale_back *= 1 / 0.85
                buf = io.BytesIO()
                img.save(buf, format="PNG", optimize=True)
                png_bytes = buf.getvalue()
            b64 = base64.b64encode(png_bytes).decode()
            kw = dict(model=self.model_id, max_tokens=256,
                      system=sys_msg,
                      messages=[{"role": "user", "content": [
                          {"type": "image", "source": {
                              "type": "base64", "media_type": "image/png", "data": b64}},
                          {"type": "text", "text": instruction}]}])
            # Claude Opus 4.7 and later reasoning-capable models deprecate the
            # `temperature` parameter (the API rejects requests that set it).
            # Sniff the model id and only include temperature for the older
            # families that still accept it.
            if not self.model_id.startswith(("claude-opus-4-7",
                                              "claude-opus-4-8")):
                kw["temperature"] = 0.0
            resp = _with_retry(lambda: self.client.messages.create(**kw))
            # resp.content is a list of TextBlock/ImageBlock/etc.
            text = "".join(b.text for b in resp.content if hasattr(b, "text"))

        elif self.provider == "google":
            img = Image.open(image_path).convert("RGB")
            if scale < 1.0:
                new_w = int(W * scale); new_h = int(H * scale)
                img = img.resize((new_w, new_h), Image.LANCZOS)
            try:
                resp = _with_retry(lambda: self.client.generate_content(
                    [prompt, img],
                    generation_config={"temperature": 0.0, "max_output_tokens": 256}))
                text = (resp.text if hasattr(resp, "text") and resp.text else "")
            except Exception as e:
                # Safety filters or quota errors after retries; treat as a non-fatal miss.
                text = ""

        else:
            raise ValueError(f"unknown provider {self.provider!r}")

        self._used += 1
        # The model saw a resized image; its predictions are in that frame.
        # Parse with the resized dims so out-of-bounds filters use the right
        # space, then scale back to original pixel coords.
        eff_scale = 1.0 / scale_back if scale_back != 0 else 1.0
        scaled_W = int(W * eff_scale) if eff_scale < 1.0 else W
        scaled_H = int(H * eff_scale) if eff_scale < 1.0 else H
        xy = parse_coordinate(text, image_wh=(scaled_W, scaled_H),
                              coord_space=self.coord_space)
        if xy is not None and scale_back != 1.0:
            xy = (xy[0] * scale_back, xy[1] * scale_back)
        return GroundingResult(raw_text=text, pred_xy=xy,
                               meta={"image_wh": (W, H), "api_calls_used": self._used,
                                     "provider": self.provider,
                                     "scale_back": scale_back})
