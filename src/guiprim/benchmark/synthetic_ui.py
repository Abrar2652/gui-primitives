"""Synthetic GUI renderer.

This produces screenshot images with *exactly known* element bounding boxes,
in the same schema as a real UI corpus (data/schema/ui_corpus.schema.json).
Its purpose is twofold:
  1. CI / smoke testing: the whole pipeline runs end-to-end with no downloads.
  2. A controlled-stimulus arm of the paper. Because the layout is generated, we
     can hold every nuisance variable constant and vary only the spatial
     relation — the strongest possible defense against a "shortcut learning"
     reviewer objection.

It is NOT a replacement for real screenshots; the headline numbers come from a
real UI corpus + ScreenSpot-Pro. The synthetic arm is reported as a clean-room
confirmation.
"""
from __future__ import annotations
import random
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

_PALETTE = [(52, 73, 94), (41, 128, 185), (39, 174, 96),
            (192, 57, 43), (142, 68, 173), (211, 84, 0)]
_LABELS = ["Save", "Open", "Close", "Edit", "Delete", "Copy", "Paste", "Run",
           "Stop", "Export", "Import", "Filter", "Sort", "Zoom", "Reset"]


def render_synthetic_ui(out_path: str | Path, rng: random.Random,
                         canvas: tuple[int, int] = (1280, 800)) -> dict[str, Any]:
    """Render one synthetic screenshot and return its element annotation record."""
    out_path = Path(out_path)
    W, H = canvas
    img = Image.new("RGB", canvas, (236, 240, 241))
    draw = ImageDraw.Draw(img)
    elements: list[dict[str, Any]] = []
    eid = 0

    def add(bbox, etype, text, parent=None):
        nonlocal eid
        col = rng.choice(_PALETTE)
        draw.rectangle(bbox, fill=col, outline=(255, 255, 255), width=2)
        draw.text((bbox[0] + 6, bbox[1] + 6), text, fill=(255, 255, 255))
        elements.append({"id": f"e{eid}", "bbox": list(map(int, bbox)),
                         "type": etype, "text": text, "parent_id": parent})
        eid += 1
        return f"e{eid - 1}"

    # Top toolbar: a horizontal strip of buttons (feeds rel_pos_h, proximity).
    n_tools = rng.randint(4, 7)
    tw, gap = 110, 14
    x0 = 24
    for i in range(n_tools):
        x = x0 + i * (tw + gap)
        add((x, 18, x + tw, 58), "button", rng.choice(_LABELS))

    # Left sidebar panel with an item list (feeds containment, list_ordinal).
    panel = (24, 90, 320, H - 30)
    draw.rectangle(panel, outline=(127, 140, 141), width=3)
    panel_id = len(elements)
    elements.append({"id": f"e{eid}", "bbox": list(panel), "type": "panel",
                     "text": "Sidebar", "parent_id": None})
    panel_eid = f"e{eid}"; eid += 1
    n_list = rng.randint(4, 6)
    ih = 52
    for i in range(n_list):
        y = panel[1] + 20 + i * (ih + 10)
        add((panel[0] + 16, y, panel[2] - 16, y + ih), "list_item",
            f"Item {i + 1}", parent=panel_eid)

    # Right working area with a small grid (feeds rel_pos_v, alignment).
    gx0, gy0, cell = 380, 120, 150
    for r in range(3):
        for c in range(4):
            x, y = gx0 + c * (cell + 16), gy0 + r * (cell + 16)
            add((x, y, x + cell, y + cell), "tile", rng.choice(_LABELS))

    # Optional modal overlay (feeds occlusion): drawn last so it covers tiles.
    if rng.random() < 0.5:
        mx, my = rng.randint(500, 760), rng.randint(220, 420)
        draw.rectangle((mx, my, mx + 260, my + 150), fill=(44, 62, 80),
                       outline=(241, 196, 15), width=3)
        draw.text((mx + 12, my + 12), "Dialog", fill=(255, 255, 255))
        elements.append({"id": f"e{eid}", "bbox": [mx, my, mx + 260, my + 150],
                         "type": "overlay", "text": "Dialog", "parent_id": None})
        eid += 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
    return {"image_path": str(out_path), "image_size": [W, H], "elements": elements,
            "source": "synthetic"}


def build_synthetic_corpus(out_dir: str | Path, n_images: int, seed: int) -> Path:
    """Render `n_images` synthetic screenshots; write a JSONL UI corpus. Returns it."""
    import json
    out_dir = Path(out_dir)
    (out_dir / "images").mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    corpus = out_dir / "corpus.jsonl"
    with open(corpus, "w") as f:
        for i in range(n_images):
            rec = render_synthetic_ui(out_dir / "images" / f"ui_{i:04d}.png", rng)
            f.write(json.dumps(rec) + "\n")
    return corpus
