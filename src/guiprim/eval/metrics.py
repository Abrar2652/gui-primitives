"""Grounding metrics.

Primary metric (matches ScreenSpot-Pro): point-in-box accuracy — the predicted
click is correct iff it lands inside the ground-truth element box.

Secondary, reviewer-facing metrics:
  * pair_consistency: fraction of minimal pairs where BOTH members are correct.
    A model that always clicks the same element scores ~0.5 on raw accuracy but
    ~0.0 here — this is the metric that proves the benchmark resists shortcuts.
  * normalized center distance: continuous error signal for regression / plots.
"""
from __future__ import annotations
import math
from collections import defaultdict
from typing import Any


def point_in_box(xy, bbox) -> bool:
    """True iff point xy=(x,y) lies inside bbox=[x1,y1,x2,y2]."""
    if xy is None or bbox is None:
        return False
    x, y = xy
    return bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3]


def center_distance(xy, bbox, image_wh=None) -> float | None:
    """Euclidean distance from prediction to box center; normalized if image_wh given."""
    if xy is None or bbox is None:
        return None
    cx, cy = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2
    d = math.hypot(xy[0] - cx, xy[1] - cy)
    if image_wh:
        d /= math.hypot(*image_wh)
    return d


def score_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Annotate each prediction record with `correct`, `near` (loose hit
    within 2x target-diagonal of the box center), and `dist`.

    The `near` flag complements the strict point-in-box accuracy: tiny-icon
    targets (median 31x26 px in our real-screenshot subset) penalize all
    models harshly under strict scoring; reporting `near` alongside `correct`
    distinguishes target-size confounds from grounding-direction failures.
    """
    import math
    out = []
    for r in records:
        xy = tuple(r["pred_xy"]) if r.get("pred_xy") else None
        bb = r.get("target_bbox")
        rr = dict(r)
        rr["correct"] = point_in_box(xy, bb)
        rr["chose_distractor"] = point_in_box(xy, r.get("distractor_bbox"))
        rr["dist"] = center_distance(xy, bb)
        # Near-hit: prediction within 2x the target bbox diagonal from center.
        rr["near"] = False
        if xy and bb and rr["dist"] is not None:
            diag = math.hypot(bb[2] - bb[0], bb[3] - bb[1])
            rr["near"] = rr["dist"] <= 2.0 * diag
        out.append(rr)
    return out


def per_primitive_table(scored: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    """Aggregate accuracy, distractor-rate, and continuous error metrics per primitive.

    Continuous metrics complement the strict point-in-box accuracy: a model that
    consistently lands NEAR the target (but not inside the tight bbox) looks bad
    on accuracy but good on mean_dist. The gap between the two diagnoses *target
    size* vs *grounding direction* failure — useful for the paper's discussion.
    """
    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in scored:
        buckets[r.get("primitive", "unknown")].append(r)
    table = {}
    for prim, rs in buckets.items():
        n = len(rs)
        dists = [r["dist"] for r in rs if r.get("dist") is not None]
        table[prim] = {
            "n": n,
            "accuracy": sum(r["correct"] for r in rs) / n if n else 0.0,
            "loose_accuracy": sum(r.get("near", False) for r in rs) / n if n else 0.0,
            "distractor_rate": sum(r["chose_distractor"] for r in rs) / n if n else 0.0,
            "parse_fail_rate": sum(r.get("pred_xy") is None for r in rs) / n if n else 0.0,
            "mean_dist_px": (sum(dists) / len(dists)) if dists else None,
            "median_dist_px": (sorted(dists)[len(dists) // 2]) if dists else None,
        }
    return table


def pair_consistency(scored: list[dict[str, Any]]) -> dict[str, float]:
    """Per-primitive fraction of minimal pairs with BOTH members correct.

    Only counts pairs where BOTH members were actually evaluated (pair_id has
    exactly two records). Splits that subset the benchmark (e.g. the 196-item
    closed-model core split) will have many incomplete pairs, which inflate
    or deflate the metric if not filtered out. See pair_consistency_with_n.
    """
    return {p: v["pair_consistency"] for p, v in pair_consistency_with_n(scored).items()}


def pair_consistency_with_n(scored: list[dict[str, Any]]
                            ) -> dict[str, dict[str, float]]:
    """Per-primitive pair-consistency plus the count of *complete* pairs the
    metric was computed over. Use this in tables so readers can spot small-n
    primitives where pair_consistency is unreliable."""
    pairs: dict[Any, list[dict]] = defaultdict(list)
    for r in scored:
        pairs[r.get("pair_id")].append(r)
    by_prim: dict[str, list[bool]] = defaultdict(list)
    for members in pairs.values():
        if len(members) != 2:
            continue
        prim = members[0].get("primitive", "unknown")
        by_prim[prim].append(all(m["correct"] for m in members))
    return {p: {"pair_consistency": sum(v) / len(v) if v else 0.0,
                "n_complete_pairs": len(v)}
            for p, v in by_prim.items()}
