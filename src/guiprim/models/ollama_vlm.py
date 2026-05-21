"""Wrapper for VLMs served by a local Ollama daemon (default
http://localhost:11434). Ollama hosts open-weight VLMs such as
llava, llama3.2-vision (incl. 90B), qwen2.5-vl (incl. 72B), minicpm-v,
moondream, bakllava, gemma3 (vision-capable variants), etc.

Config schema:
  family: ollama
  hf_id:  ollama-tag, e.g. 'llama3.2-vision:90b' or 'qwen2.5vl:7b'
  api:
    base_url: http://localhost:11434     (override if needed)
    timeout:  120                         (seconds per request)

The wrapper sends a base64-encoded image to ollama's /api/chat endpoint
and parses the reply with the standard `parse_coordinate` helper.
"""
from __future__ import annotations
import base64
import json
import os
from typing import Any

import urllib.request
import urllib.error

from .base import GroundingResult, VLMWrapper
from ..inference.parsing import parse_coordinate


_GROUNDING_SYS = (
    "You are a GUI grounding assistant. Given a screenshot and an "
    "instruction, respond with ONLY the pixel coordinate to click, "
    "formatted exactly as click(x, y). Do not explain.")


class OllamaWrapper(VLMWrapper):
    def __init__(self, cfg: dict[str, Any]):
        super().__init__(cfg)
        api = cfg.get("api", {})
        self.base_url = api.get("base_url", os.environ.get(
            "OLLAMA_BASE_URL", "http://localhost:11434"))
        self.timeout = float(api.get("timeout", 240))
        self.model_id = cfg["hf_id"]
        self._used = 0

    def _post(self, body: dict) -> dict:
        data = json.dumps(body).encode()
        req = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read())

    def ground(self, image_path: str, instruction: str,
               system: str | None = None) -> GroundingResult:
        from PIL import Image
        W, H = Image.open(image_path).size
        sys_msg = system or _GROUNDING_SYS
        # Read + base64 the image
        b64 = base64.b64encode(open(image_path, "rb").read()).decode()
        # Some ollama VLMs (notably moondream) silently drop their answer if
        # the request uses a separate `system` role; collapse system+user into
        # a single user message which all of the VLMs we care about accept.
        body = {
            "model": self.model_id,
            "stream": False,
            "messages": [
                {"role": "user",
                 "content": f"{sys_msg}\n\n{instruction}",
                 "images": [b64]},
            ],
            "options": {"temperature": 0.0, "num_predict": 128},
        }
        try:
            resp = self._post(body)
            text = resp.get("message", {}).get("content", "")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            return GroundingResult(raw_text="", pred_xy=None,
                                   meta={"image_wh": (W, H),
                                         "error": str(e)[:200]})
        self._used += 1
        xy = parse_coordinate(text, image_wh=(W, H),
                              coord_space=self.coord_space)
        return GroundingResult(raw_text=text, pred_xy=xy,
                               meta={"image_wh": (W, H),
                                     "api_calls_used": self._used,
                                     "provider": "ollama"})

    def cleanup(self) -> None:
        pass
