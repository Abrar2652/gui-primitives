"""Render the human-verified core items with bbox overlays.

For each item produces one PNG in human_eval/renders_for_annotation/:
  - full screenshot at <=1024px wide
  - green rectangle = target_bbox (the constructor's claimed correct answer)
  - red rectangle   = distractor_bbox (the minimal-pair foil)
  - a thin yellow border crop in the bottom-right showing both boxes
    zoomed in, so small UI elements are legible.

Used by the LLM-as-annotator dry run; real human annotators use the same
images so judgements are directly comparable.
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "data" / "benchmark"
OUT = ROOT / "human_eval" / "renders_for_annotation"
OUT.mkdir(parents=True, exist_ok=True)

MAX_FULL_W = 1024
ZOOM_MAX = 480


def _scale(im: Image.Image, max_w: int) -> tuple[Image.Image, float]:
    if im.width <= max_w:
        return im, 1.0
    s = max_w / im.width
    return im.resize((max_w, int(im.height * s))), s


def _draw_box(d: ImageDraw.ImageDraw, box, color: str, label: str, scale: float) -> None:
    x1, y1, x2, y2 = [c * scale for c in box]
    d.rectangle([x1, y1, x2, y2], outline=color, width=3)
    d.text((x1 + 2, max(0, y1 - 12)), label, fill=color)


def _zoom_crop(im: Image.Image, t_box, d_box, scale: float) -> Image.Image:
    pad = 60
    xs = [t_box[0] * scale, t_box[2] * scale, d_box[0] * scale, d_box[2] * scale]
    ys = [t_box[1] * scale, t_box[3] * scale, d_box[1] * scale, d_box[3] * scale]
    x1 = max(0, int(min(xs) - pad))
    y1 = max(0, int(min(ys) - pad))
    x2 = min(im.width, int(max(xs) + pad))
    y2 = min(im.height, int(max(ys) + pad))
    crop = im.crop((x1, y1, x2, y2))
    if crop.width > ZOOM_MAX:
        z = ZOOM_MAX / crop.width
        crop = crop.resize((ZOOM_MAX, int(crop.height * z)))
    return crop


def render_item(item: dict) -> Path:
    img_path = Path(item["image_path"])
    im = Image.open(img_path).convert("RGB")
    full, s = _scale(im, MAX_FULL_W)
    draw = ImageDraw.Draw(full)
    _draw_box(draw, item["target_bbox"], "lime", "T (target)", s)
    _draw_box(draw, item["distractor_bbox"], "red", "D (distractor)", s)

    zoom = _zoom_crop(im, item["target_bbox"], item["distractor_bbox"], 1.0)
    zdraw = ImageDraw.Draw(zoom)
    # Recompute boxes in zoom space.
    pad = 60
    xs = [item["target_bbox"][0], item["target_bbox"][2],
          item["distractor_bbox"][0], item["distractor_bbox"][2]]
    ys = [item["target_bbox"][1], item["target_bbox"][3],
          item["distractor_bbox"][1], item["distractor_bbox"][3]]
    ox = max(0, int(min(xs) - pad))
    oy = max(0, int(min(ys) - pad))
    raw_zoom_w = min(im.width, int(max(xs) + pad)) - ox
    z = zoom.width / raw_zoom_w if raw_zoom_w > 0 else 1.0
    for box, color, lab in [
        (item["target_bbox"], "lime", "T"),
        (item["distractor_bbox"], "red", "D"),
    ]:
        x1 = (box[0] - ox) * z
        y1 = (box[1] - oy) * z
        x2 = (box[2] - ox) * z
        y2 = (box[3] - oy) * z
        zdraw.rectangle([x1, y1, x2, y2], outline=color, width=2)
        zdraw.text((x1 + 2, max(0, y1 - 11)), lab, fill=color)

    # Compose: full on top, zoom below.
    out_w = max(full.width, zoom.width)
    out_h = full.height + zoom.height + 10
    canvas = Image.new("RGB", (out_w, out_h), "white")
    canvas.paste(full, (0, 0))
    canvas.paste(zoom, (0, full.height + 10))
    out_path = OUT / f"{item['item_id']}.png"
    canvas.save(out_path, optimize=True)
    return out_path


def main() -> None:
    items = [json.loads(l) for l in (BENCH / "items.jsonl").read_text().splitlines() if l.strip()]
    splits = json.loads((BENCH / "splits.json").read_text())
    keep = set(splits["human_verified"])
    core = [it for it in items if it["item_id"] in keep]
    print(f"rendering {len(core)} items -> {OUT}")
    for i, it in enumerate(core, 1):
        try:
            render_item(it)
        except Exception as e:
            print(f"  [{i}/{len(core)}] FAILED {it['item_id']}: {e}")
            continue
        if i % 25 == 0 or i == len(core):
            print(f"  [{i}/{len(core)}] {it['item_id']}")


if __name__ == "__main__":
    main()
