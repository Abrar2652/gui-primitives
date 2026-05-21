"""Grounding metrics: point-in-box, scoring, per-primitive, pair consistency."""
from guiprim.eval.metrics import (point_in_box, score_records,
                                  per_primitive_table, pair_consistency)


def test_point_in_box():
    assert point_in_box((5, 5), [0, 0, 10, 10])
    assert not point_in_box((15, 5), [0, 0, 10, 10])
    assert not point_in_box(None, [0, 0, 10, 10])
    assert not point_in_box((5, 5), None)


def _rec(item_id, pair_id, prim, pred, target, distractor):
    return {"item_id": item_id, "pair_id": pair_id, "primitive": prim,
            "pred_xy": pred, "target_bbox": target, "distractor_bbox": distractor}


def test_score_records_flags_correct_and_distractor():
    recs = [
        _rec("a", 0, "rel_pos_horizontal", [5, 5], [0, 0, 10, 10], [20, 0, 30, 10]),
        _rec("b", 0, "rel_pos_horizontal", [25, 5], [20, 0, 30, 10], [0, 0, 10, 10]),
    ]
    scored = score_records(recs)
    assert scored[0]["correct"] and not scored[0]["chose_distractor"]
    assert scored[1]["correct"]


def test_per_primitive_table_accuracy():
    recs = [
        _rec("a", 0, "containment", [5, 5], [0, 0, 10, 10], [50, 50, 60, 60]),
        _rec("b", 1, "containment", [99, 99], [0, 0, 10, 10], [50, 50, 60, 60]),
    ]
    table = per_primitive_table(score_records(recs))
    assert table["containment"]["n"] == 2
    assert table["containment"]["accuracy"] == 0.5


def test_pair_consistency_requires_both_members_correct():
    # pair 0: both correct -> consistent. pair 1: one wrong -> inconsistent.
    recs = [
        _rec("a0", 0, "alignment", [5, 5], [0, 0, 10, 10], [50, 50, 60, 60]),
        _rec("a1", 0, "alignment", [55, 55], [50, 50, 60, 60], [0, 0, 10, 10]),
        _rec("b0", 1, "alignment", [5, 5], [0, 0, 10, 10], [50, 50, 60, 60]),
        _rec("b1", 1, "alignment", [999, 999], [50, 50, 60, 60], [0, 0, 10, 10]),
    ]
    cons = pair_consistency(score_records(recs))
    assert cons["alignment"] == 0.5
