"""Robust coordinate parsing.

Different VLMs report click targets in different formats and coordinate spaces.
A brittle parser would silently turn correct model outputs into wrong ones and
poison the headline numbers, so this module is deliberately defensive and is
covered by tests/test_parsing.py.

coord_space:
  pixel      -> values are already in image pixels
  norm_1     -> values in [0,1]; multiplied by (W,H)
  norm_1000  -> values in [0,1000] (Qwen-style); scaled by (W/1000, H/1000)
"""
from __future__ import annotations
import re

# Ordered: most explicit / least ambiguous formats first.
_PATTERNS = [
    r"click\s*\(\s*([0-9]*\.?[0-9]+)\s*,\s*([0-9]*\.?[0-9]+)\s*\)",
    r"x\s*[=:]\s*([0-9]*\.?[0-9]+)\s*,?\s*y\s*[=:]\s*([0-9]*\.?[0-9]+)",
    r'"x"\s*:\s*([0-9]*\.?[0-9]+)\s*,\s*"y"\s*:\s*([0-9]*\.?[0-9]+)',
    r"<click>\s*([0-9]*\.?[0-9]+)\s*,\s*([0-9]*\.?[0-9]+)\s*</click>",
    r"point[^0-9]*([0-9]*\.?[0-9]+)\s*,\s*([0-9]*\.?[0-9]+)",
    r"[\(\[]\s*([0-9]*\.?[0-9]+)\s*,\s*([0-9]*\.?[0-9]+)\s*[\)\]]",
]

# OS-Atlas / Qwen2-VL grounding bbox output:
#   <|box_start|>(x1,y1),(x2,y2)<|box_end|>
# When the model returns a bbox for the referred element, we score against its
# center (a natural click target). Handled separately so we don't accidentally
# pick the top-left corner via the generic (x,y) regex above.
_BBOX_PATTERN = re.compile(
    r"<\|box_start\|>\s*\(\s*([0-9]*\.?[0-9]+)\s*,\s*([0-9]*\.?[0-9]+)\s*\)\s*,"
    r"\s*\(\s*([0-9]*\.?[0-9]+)\s*,\s*([0-9]*\.?[0-9]+)\s*\)\s*<\|box_end\|>",
    re.IGNORECASE,
)

# Qwen2-VL sometimes emits click(x1,y1,x2,y2) — a four-arg click that's really a
# bbox. Map to center to keep the prediction usable.
_CLICK4_PATTERN = re.compile(
    r"click\s*\(\s*([0-9]*\.?[0-9]+)\s*,\s*([0-9]*\.?[0-9]+)\s*,"
    r"\s*([0-9]*\.?[0-9]+)\s*,\s*([0-9]*\.?[0-9]+)\s*\)",
    re.IGNORECASE,
)

# MiniCPM-V and some other VLMs emit "<box>x1 y1 x2 y2</box>" (space- or
# comma-separated 4 numbers in angle-bracket tags). Same convention: take
# the center.
_BOX_TAG_PATTERN = re.compile(
    r"<box>\s*([0-9]*\.?[0-9]+)\s*[\s,]\s*([0-9]*\.?[0-9]+)\s*[\s,]\s*"
    r"([0-9]*\.?[0-9]+)\s*[\s,]\s*([0-9]*\.?[0-9]+)\s*</box>",
    re.IGNORECASE,
)

# PaliGemma's <loc####> grounding format: 4 consecutive special tokens
#   <loc_YMIN><loc_XMIN><loc_YMAX><loc_XMAX>
# encoding coordinates as integers in 1024-normalized space (NOT pixel).
_PALIGEMMA_LOC_PATTERN = re.compile(
    r"<loc(\d{4})>\s*<loc(\d{4})>\s*<loc(\d{4})>\s*<loc(\d{4})>",
    re.IGNORECASE,
)


def parse_coordinate(text: str, image_wh: tuple[int, int],
                     coord_space: str = "pixel") -> tuple[float, float] | None:
    """Extract a single (x, y) click coordinate in PIXEL space, or None."""
    if not text:
        return None
    W, H = image_wh
    # PaliGemma <loc####> tokens encode (y_min, x_min, y_max, x_max) in
    # 1024-normalized space; convert to image pixels via direct W*v/1024.
    m = _PALIGEMMA_LOC_PATTERN.search(text)
    if m:
        y1n, x1n, y2n, x2n = (int(m.group(i)) for i in (1, 2, 3, 4))
        cx = (x1n + x2n) / 2.0 * W / 1024.0
        cy = (y1n + y2n) / 2.0 * H / 1024.0
        # Clamp to canvas
        cx = min(max(cx, 0.0), W); cy = min(max(cy, 0.0), H)
        return (cx, cy)
    # Then try the explicit bbox formats and use the center: OS-Atlas
    # <|box_start|>(x1,y1),(x2,y2)<|box_end|>, Qwen2-VL click(x1,y1,x2,y2),
    # MiniCPM-V <box>x1 y1 x2 y2</box>.
    for bp in (_BBOX_PATTERN, _CLICK4_PATTERN, _BOX_TAG_PATTERN):
        m = bp.search(text)
        if m:
            x1, y1, x2, y2 = (float(m.group(i)) for i in (1, 2, 3, 4))
            cx, cy = (x1 + x2) / 2.0, (y1 + y2) / 2.0
            return _to_pixels(cx, cy, W, H, coord_space)
    for pat in _PATTERNS:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if not m:
            continue
        x, y = float(m.group(1)), float(m.group(2))
        return _to_pixels(x, y, W, H, coord_space)
    return None


def _to_pixels(x: float, y: float, W: int, H: int, space: str) -> tuple[float, float]:
    if space == "norm_1":
        x, y = x * W, y * H
    elif space == "norm_1000":
        x, y = x * W / 1000.0, y * H / 1000.0
    elif space == "pixel":
        # Heuristic guard: a model told to use pixels but emitting [0,1] values.
        if 0.0 <= x <= 1.0 and 0.0 <= y <= 1.0:
            x, y = x * W, y * H
    else:
        raise ValueError(f"unknown coord_space: {space}")
    # Clamp into the canvas; out-of-bounds predictions are still scored as misses
    # but clamping keeps downstream geometry well-defined.
    return (min(max(x, 0.0), W), min(max(y, 0.0), H))
