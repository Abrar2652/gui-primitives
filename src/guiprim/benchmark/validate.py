"""Benchmark quality gates.

Every check here maps to a question a reviewer will ask. The build script runs
all of them and refuses to proceed if a hard gate fails, so a malformed
benchmark can never silently reach the experiments.
"""
from __future__ import annotations
from collections import Counter
from typing import Any

from .primitives import CHANCE, PrimitiveType
from .synthesize import area, intersects


class ValidationError(Exception):
    pass


def validate_items(items: list[dict[str, Any]]) -> dict[str, Any]:
    """Run all checks. Returns a report dict; raises ValidationError on a hard fail."""
    report: dict[str, Any] = {"n_items": len(items), "issues": [], "per_primitive": {}}
    if not items:
        raise ValidationError("empty benchmark")

    by_prim = Counter(it["primitive"] for it in items)
    report["per_primitive"] = dict(by_prim)

    # Gate 1: minimal pairs are complete (both members present, distinct targets).
    pairs: dict[int, list[dict]] = {}
    for it in items:
        pairs.setdefault(it["pair_id"], []).append(it)
    broken = [pid for pid, mem in pairs.items() if len(mem) != 2]
    if broken:
        raise ValidationError(f"{len(broken)} minimal pairs are not exactly size 2")
    for pid, mem in pairs.items():
        if mem[0]["target_bbox"] == mem[1]["target_bbox"]:
            raise ValidationError(f"pair {pid}: target does not move when relation flips")
        if mem[0]["image_path"] != mem[1]["image_path"]:
            raise ValidationError(f"pair {pid}: members use different screenshots")

    # Gate 2: target and distractor are disjoint enough to be unambiguous.
    overlap = 0
    for it in items:
        t, d = it["target_bbox"], it["distractor_bbox"]
        if intersects(t, d) and _iou(t, d) > 0.5:
            overlap += 1
    if overlap:
        report["issues"].append(f"{overlap} items: target/distractor IoU > 0.5")

    # Gate 3: degenerate (zero-area) boxes.
    degen = sum(1 for it in items if area(it["target_bbox"]) <= 0)
    if degen:
        raise ValidationError(f"{degen} items have zero-area target boxes")

    # Soft check: per-primitive coverage balance (warn, do not fail).
    if by_prim:
        lo, hi = min(by_prim.values()), max(by_prim.values())
        if hi > 3 * max(lo, 1):
            report["issues"].append(
                f"primitive coverage imbalanced (min={lo}, max={hi})")

    report["chance_levels"] = {p.value: CHANCE[p] for p in PrimitiveType}
    return report


def _iou(a, b) -> float:
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    union = area(a) + area(b) - inter
    return inter / union if union else 0.0
