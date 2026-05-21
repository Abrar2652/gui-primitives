"""Intervention 1 — primitive-aware chain-of-thought prompting.

This is the cheapest baseline and serves a specific scientific purpose: it
isolates the *language* component of the failure. If a model can recover once
it is told, in words, to decompose the spatial relation, the bottleneck is
reasoning/instruction-following. If CoT does NOT help but a visual intervention
(Set-of-Mark, steering) does, the bottleneck is perception. The paper needs
both arms to make that argument cleanly.
"""
from __future__ import annotations

from ..benchmark.primitives import PrimitiveType

# A short, primitive-specific decomposition appended before the click request.
_SCAFFOLD: dict[str, str] = {
    PrimitiveType.REL_POS_H.value:
        "First find the anchor element. Then decide which side — left or right — "
        "the instruction names. Then pick the element on that side.",
    PrimitiveType.REL_POS_V.value:
        "First find the anchor element. Then decide whether the instruction says "
        "above or below. Then pick the element on that side.",
    PrimitiveType.CONTAINMENT.value:
        "First locate the named panel boundary. Then decide if the target is "
        "inside or outside that boundary. Then pick the matching element.",
    PrimitiveType.LIST_ORDINAL.value:
        "First find the list. Then count items from the top. Then pick the item "
        "at the named ordinal position.",
    PrimitiveType.ALIGNMENT.value:
        "First find the anchor. Then decide whether the instruction says same row "
        "or same column. Then pick the aligned element.",
    PrimitiveType.PROXIMITY.value:
        "First find the anchor. Then compare distances of the candidate elements. "
        "Then pick the nearest or farthest as instructed.",
    PrimitiveType.OCCLUSION.value:
        "First find any overlay or dialog. Then decide whether the target should "
        "be fully visible or partly hidden. Then pick the matching element.",
}

_TEMPLATE = (
    "{instruction}\n\n"
    "Think step by step about the spatial relation: {scaffold}\n"
    "After reasoning, output ONLY the final answer on the last line as click(x, y).")


def cot_instruction(item: dict) -> str:
    """Rewrite an item's instruction with a primitive-aware CoT scaffold."""
    scaffold = _SCAFFOLD.get(item.get("primitive", ""),
                             "Identify the anchor, then the relation, then the target.")
    return _TEMPLATE.format(instruction=item["instruction"], scaffold=scaffold)
