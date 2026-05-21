"""Benchmark synthesis end-to-end on the synthetic UI corpus, plus validation."""
import json

from guiprim.benchmark.synthetic_ui import build_synthetic_corpus
from guiprim.benchmark.synthesize import synthesize
from guiprim.benchmark.validate import validate_items, ValidationError
from guiprim.benchmark.primitives import PRIMITIVES, tag_instruction

ALL_PRIMS = [p.value for p in PRIMITIVES]


def test_synthetic_corpus_renders(tmp_path):
    corpus = build_synthetic_corpus(tmp_path / "ui", n_images=12, seed=1)
    recs = [json.loads(l) for l in corpus.read_text().splitlines() if l.strip()]
    assert len(recs) == 12
    for r in recs:
        assert r["elements"] and "image_size" in r
        assert (tmp_path / "ui").exists()


def test_synthesize_produces_minimal_pairs(tmp_path):
    corpus = build_synthetic_corpus(tmp_path / "ui", n_images=40, seed=2)
    items = synthesize(corpus, ALL_PRIMS, n_items=120, seed=2)
    assert items, "synthesis produced no items"
    # Every pair_id must have exactly two members with different targets.
    pairs: dict[int, list] = {}
    for it in items:
        pairs.setdefault(it["pair_id"], []).append(it)
    for members in pairs.values():
        assert len(members) == 2
        assert members[0]["target_bbox"] != members[1]["target_bbox"]
        assert members[0]["image_path"] == members[1]["image_path"]


def test_synthesized_items_pass_validation(tmp_path):
    corpus = build_synthetic_corpus(tmp_path / "ui", n_images=40, seed=3)
    items = synthesize(corpus, ALL_PRIMS, n_items=120, seed=3)
    report = validate_items(items)
    assert report["n_items"] == len(items)
    assert report["per_primitive"]


def test_validation_rejects_broken_pairs():
    bad = [{"item_id": "x", "pair_id": 0, "primitive": "alignment",
            "image_path": "a.png", "target_bbox": [0, 0, 1, 1],
            "distractor_bbox": [2, 2, 3, 3]}]  # only one member of the pair
    try:
        validate_items(bad)
        assert False, "should have raised"
    except ValidationError:
        pass


def test_tag_instruction_detects_primitives():
    assert "rel_pos_horizontal" in tag_instruction("click the icon to the left of Save")
    assert "list_ordinal" in tag_instruction("select the third item in the menu")
    assert tag_instruction("click the button") == []
