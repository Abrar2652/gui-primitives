"""The seven GUI spatial primitives that define the GUI-Primitives benchmark.

Design rationale (for the paper's Methods section):
  * Each primitive is *elementary*: it isolates one spatial relation a click
    instruction can hinge on. Compositionality is explicitly out of scope here
    and is left to a controlled secondary analysis.
  * Each primitive ships a set of `contrastive_pairs`: relation words that, when
    swapped in an otherwise identical instruction over an identical screenshot,
    flip the correct target. This is what makes the items *minimal pairs* in the
    sense of What's-Up (Kamath et al., EMNLP 2023): accuracy above chance cannot
    come from a language prior or an object prior, only from grounding.
  * `keywords` are used to auto-tag external instructions (ScreenSpot-Pro) with
    the primitives they require, which feeds the primitive -> grounding
    regression in eval/regression.py.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class PrimitiveType(str, Enum):
    REL_POS_H = "rel_pos_horizontal"
    REL_POS_V = "rel_pos_vertical"
    CONTAINMENT = "containment"
    LIST_ORDINAL = "list_ordinal"
    ALIGNMENT = "alignment"
    PROXIMITY = "proximity"
    OCCLUSION = "occlusion"


@dataclass(frozen=True)
class Primitive:
    ptype: PrimitiveType
    description: str
    relations: Tuple[str, ...]                  # surface relation words
    contrastive_pairs: Tuple[Tuple[str, str], ...]  # (relation, its minimal-pair flip)
    templates: Tuple[str, ...]                  # {rel}/{anchor}/{ord} are filled in
    keywords: Tuple[str, ...]                   # for auto-tagging external instructions


PRIMITIVES: dict[PrimitiveType, Primitive] = {
    PrimitiveType.REL_POS_H: Primitive(
        ptype=PrimitiveType.REL_POS_H,
        description="Horizontal relative position of one element to an anchor.",
        relations=("to the left of", "to the right of"),
        contrastive_pairs=(("to the left of", "to the right of"),),
        templates=("Click the element {rel} the {anchor}.",
                   "Select the control {rel} '{anchor}'."),
        keywords=("left of", "right of", "leftmost", "rightmost", "left side", "right side"),
    ),
    PrimitiveType.REL_POS_V: Primitive(
        ptype=PrimitiveType.REL_POS_V,
        description="Vertical relative position of one element to an anchor.",
        relations=("above", "below"),
        contrastive_pairs=(("above", "below"),),
        templates=("Click the element {rel} the {anchor}.",
                   "Select the item directly {rel} '{anchor}'."),
        keywords=("above", "below", "under", "on top of", "beneath", "topmost", "bottom"),
    ),
    PrimitiveType.CONTAINMENT: Primitive(
        ptype=PrimitiveType.CONTAINMENT,
        description="Whether the target lies inside vs. outside a named panel/region.",
        relations=("inside", "outside"),
        contrastive_pairs=(("inside", "outside"),),
        templates=("Click the {anchor} button that is {rel} the panel.",
                   "Select the '{anchor}' control located {rel} the dialog."),
        keywords=("inside", "outside", "within", "in the panel", "in the dialog",
                  "in the toolbar", "in the sidebar"),
    ),
    PrimitiveType.LIST_ORDINAL: Primitive(
        ptype=PrimitiveType.LIST_ORDINAL,
        description="Ordinal position of an item in a list or menu.",
        relations=("first", "second", "third", "fourth", "fifth", "last"),
        contrastive_pairs=(("first", "second"), ("second", "third"),
                           ("third", "last"), ("first", "last")),
        templates=("Click the {ord} item in the list.",
                   "Select the {ord} entry of the menu."),
        keywords=("first", "second", "third", "fourth", "fifth", "last", "next item",
                  "top item", "ordinal"),
    ),
    PrimitiveType.ALIGNMENT: Primitive(
        ptype=PrimitiveType.ALIGNMENT,
        description="Whether two elements share a row vs. a column.",
        relations=("in the same row as", "in the same column as"),
        contrastive_pairs=(("in the same row as", "in the same column as"),),
        templates=("Click the element {rel} the {anchor}.",
                   "Select the control aligned {rel} '{anchor}'."),
        keywords=("same row", "same column", "aligned", "same line", "next to in the row"),
    ),
    PrimitiveType.PROXIMITY: Primitive(
        ptype=PrimitiveType.PROXIMITY,
        description="Which element of a group is nearest vs. farthest from an anchor.",
        relations=("nearest to", "farthest from"),
        contrastive_pairs=(("nearest to", "farthest from"),),
        templates=("Click the icon {rel} the {anchor}.",
                   "Select the button {rel} '{anchor}'."),
        keywords=("nearest", "closest", "farthest", "furthest", "next to", "adjacent"),
    ),
    PrimitiveType.OCCLUSION: Primitive(
        ptype=PrimitiveType.OCCLUSION,
        description="Whether the target is fully visible vs. partly occluded by an overlay.",
        relations=("fully visible", "partly hidden"),
        contrastive_pairs=(("fully visible", "partly hidden"),),
        templates=("Click the {anchor} control that is {rel}.",
                   "Select the '{anchor}' element that is currently {rel}."),
        keywords=("visible", "hidden", "occluded", "covered", "behind the", "obscured"),
    ),
}

# Per-primitive chance level: P(correct under random pick among the candidates the
# minimal-pair construction guarantees). Two-candidate primitives -> 0.5.
CHANCE: dict[PrimitiveType, float] = {
    PrimitiveType.REL_POS_H: 0.5,
    PrimitiveType.REL_POS_V: 0.5,
    PrimitiveType.CONTAINMENT: 0.5,
    PrimitiveType.LIST_ORDINAL: 0.2,   # five-way ordinal slot among list items
    PrimitiveType.ALIGNMENT: 0.5,
    PrimitiveType.PROXIMITY: 0.5,
    PrimitiveType.OCCLUSION: 0.5,
}


def tag_instruction(text: str) -> list[str]:
    """Return the list of primitive names whose keywords appear in an instruction.

    Used to featurize external benchmarks (ScreenSpot-Pro) for the
    primitive-competence -> grounding-success regression. Deliberately
    high-precision: an item with no keyword hit contributes only the intercept.
    """
    low = text.lower()
    hits: list[str] = []
    for ptype, prim in PRIMITIVES.items():
        if any(kw in low for kw in prim.keywords):
            hits.append(ptype.value)
    return hits
