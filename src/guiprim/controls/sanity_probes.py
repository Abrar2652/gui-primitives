"""Sanity / shortcut probes.

These are the controls that make the diagnostic reviewer-proof. Each one breaks
a specific shortcut a skeptic would worry about; a benchmark that is genuinely
testing grounding must collapse toward chance on all of them.

  make_text_only       blank canvas, real instruction  -> kills any language /
                        object-frequency prior. Expect ~chance.
  make_shuffled        real image, instruction from a DIFFERENT item -> kills
                        any image-only prior. Expect ~chance.
  make_blurred         heavily blurred image -> kills reliance on text the model
                        could OCR instead of localize. Expect a large drop.
  make_position_shift  same target re-rendered at canonical canvas positions
                        (synthetic only) -> tests position invariance; reported
                        as a consistency rate, not accuracy.

`expected_control_behavior` documents the pass criteria the analysis enforces.
"""
from __future__ import annotations
import random
from pathlib import Path
from typing import Any


def make_text_only(items: list[dict[str, Any]], out_dir: str | Path) -> list[dict]:
    """Replace each screenshot with a blank canvas of the same size."""
    from PIL import Image
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    blanks: dict[tuple, str] = {}
    out = []
    for it in items:
        wh = tuple(it["image_size"])
        if wh not in blanks:
            p = out_dir / f"blank_{wh[0]}x{wh[1]}.png"
            Image.new("RGB", wh, (240, 240, 240)).save(p)
            blanks[wh] = str(p)
        nit = dict(it)
        nit["_render_path"] = blanks[wh]
        nit["item_id"] = it["item_id"] + "::textonly"
        nit["_control"] = "text_only"
        out.append(nit)
    return out


def make_shuffled(items: list[dict[str, Any]], seed: int = 13) -> list[dict]:
    """Pair each instruction with another item's screenshot (same primitive)."""
    rng = random.Random(seed)
    by_prim: dict[str, list[dict]] = {}
    for it in items:
        by_prim.setdefault(it["primitive"], []).append(it)
    out = []
    for it in items:
        pool = [o for o in by_prim[it["primitive"]]
                if o["image_path"] != it["image_path"]]
        if not pool:
            continue
        donor = rng.choice(pool)
        nit = dict(it)
        nit["_render_path"] = donor["image_path"]
        nit["item_id"] = it["item_id"] + "::shuffled"
        nit["_control"] = "shuffled"
        out.append(nit)
    return out


def make_blurred(items: list[dict[str, Any]], out_dir: str | Path,
                 radius: int = 12) -> list[dict]:
    """Heavily Gaussian-blur each screenshot."""
    from PIL import Image, ImageFilter
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    cache: dict[str, str] = {}
    out = []
    for it in items:
        src = it["image_path"]
        if src not in cache:
            p = out_dir / f"blur_{Path(src).stem}.png"
            Image.open(src).convert("RGB").filter(
                ImageFilter.GaussianBlur(radius)).save(p)
            cache[src] = str(p)
        nit = dict(it)
        nit["_render_path"] = cache[src]
        nit["item_id"] = it["item_id"] + "::blur"
        nit["_control"] = "blur"
        out.append(nit)
    return out


def make_position_shift(items: list[dict[str, Any]], out_dir: str | Path,
                        positions: int = 4) -> list[dict]:
    """Synthetic-only: re-render the target element at canonical canvas positions.

    Returns variants tagged with `_shift_group` (the original item_id) so the
    analysis can compute a per-item position-invariance rate. Requires items to
    carry `image_size`; the actual re-rendering hook is left to the synthetic
    corpus builder, so here we emit the variant records and the translation each
    expects. Non-synthetic items are skipped.
    """
    out = []
    for it in items:
        if it.get("source") != "synthetic":
            continue
        W, H = it["image_size"]
        anchors = [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)][:positions]
        for k, (fx, fy) in enumerate(anchors):
            nit = dict(it)
            nit["item_id"] = f"{it['item_id']}::pos{k}"
            nit["_control"] = "position_shift"
            nit["_shift_group"] = it["item_id"]
            nit["_shift_target_center"] = [fx * W, fy * H]
            out.append(nit)
    return out


def expected_control_behavior() -> dict[str, str]:
    """Pass criteria enforced by scripts/06_analyze.py."""
    return {
        "text_only": "accuracy within +/- 1.5 * chance; significantly below the "
                     "main condition (McNemar p < 0.05).",
        "shuffled": "accuracy near chance; significantly below the main condition.",
        "blur": "large, significant accuracy drop vs the main condition.",
        "position_shift": "report invariance rate; flag if < 0.7 (position bias).",
    }


def evaluate_control(name: str, main_acc: float, ctrl_acc: float,
                     mcnemar_p: float | None, chance: float = 0.5
                     ) -> dict[str, object]:
    """Return {passed, reason} for one control. Implements the criteria in
    expected_control_behavior() so 06_analyze.py can flag violations.

    A passing control means the shortcut it kills cannot explain main accuracy:
    that is, removing the shortcut drives accuracy *significantly* below the
    main condition. Ceiling effects (control acc >= main acc) are failures.
    """
    sig_below = (mcnemar_p is not None and mcnemar_p < 0.05
                 and ctrl_acc < main_acc)
    if name == "text_only":
        # Killing the image should drop accuracy significantly. Bonus check:
        # control acc shouldn't sit above the per-pair chance for the benchmark.
        ceiling_ok = ctrl_acc <= chance + 0.10
        passed = sig_below and ceiling_ok
        return {"passed": passed,
                "reason": (f"acc={ctrl_acc:.3f} significantly below main "
                           f"({main_acc:.3f}); McNemar p={mcnemar_p:.2g}"
                           if passed
                           else (f"acc={ctrl_acc:.3f} not significantly below "
                                 f"main={main_acc:.3f} (p={mcnemar_p})"
                                 if not sig_below
                                 else f"acc={ctrl_acc:.3f} above pair-chance "
                                      f"ceiling {chance + 0.10:.2f}"))}
    if name == "shuffled":
        passed = sig_below
        return {"passed": passed,
                "reason": (f"acc={ctrl_acc:.3f} significantly below main "
                           f"({main_acc:.3f}); McNemar p={mcnemar_p:.2g}"
                           if passed else
                           f"acc={ctrl_acc:.3f} not significantly below "
                           f"main={main_acc:.3f} (p={mcnemar_p})")}
    if name == "blur":
        # Require >= 10 absolute-point drop and McNemar significance.
        large_drop = (main_acc - ctrl_acc) >= 0.10
        passed = large_drop and sig_below
        return {"passed": passed,
                "reason": (f"drop={main_acc - ctrl_acc:.3f}; "
                           f"McNemar p={mcnemar_p:.2g}" if passed
                           else (f"drop={main_acc - ctrl_acc:.3f} too small"
                                 if not large_drop
                                 else f"drop not significant (p={mcnemar_p})"))}
    if name == "position_shift":
        passed = ctrl_acc >= 0.70   # invariance rate, not accuracy
        return {"passed": passed,
                "reason": f"position-invariance rate={ctrl_acc:.3f} "
                          f"({'>=' if passed else '<'} 0.70)"}
    return {"passed": False, "reason": f"unknown control '{name}'"}
