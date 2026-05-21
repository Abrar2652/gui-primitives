"""The headline scientific result: does per-primitive competence *predict*
GUI-grounding success on a held-out, external benchmark (ScreenSpot-Pro)?

Design
------
Unit of analysis: one (model, ScreenSpot-Pro item) pair.
  outcome    : the model clicked inside the GT box on that item (0/1).
  predictors : for each primitive p, a feature  requires_p * competence_{model,p}
               where requires_p   = 1 if the item's instruction is auto-tagged
                                     with primitive p (benchmark.primitives.tag_instruction)
               and   competence   = that model's accuracy on primitive p in the
                                     GUI-Primitives diagnostic.
  controls   : model fixed effects (so the effect is within-model), and log
               target-area (so we are not just re-discovering the known
               small-target effect from the ScreenSpot-Pro paper).

A positive, significant coefficient on a primitive feature means: holding the
model and the target size fixed, items that need primitive p are grounded more
accurately by models that are better at p. That is the link the paper claims.

Standard errors are clustered by ScreenSpot-Pro item (the same item appears once
per model), which is the correct, conservative choice and pre-empts a reviewer
objection about non-independence.
"""
from __future__ import annotations
import math
from typing import Any

from ..benchmark.primitives import PRIMITIVES, tag_instruction


def _load_llm_tags(tags_path: str | None) -> dict[str, list[str]] | None:
    """Load LLM-judge primitive tags keyed by item_id.

    Format (one JSON object per line):
      {"item_id": "...", "majority_primitives": [list_of_primitive_names], ...}
    Returns None if the file is missing (caller falls back to keyword tagger).
    """
    if not tags_path:
        return None
    from pathlib import Path
    import json as _json
    p = Path(tags_path)
    if not p.exists():
        return None
    out: dict[str, list[str]] = {}
    for line in p.read_text().splitlines():
        if not line.strip():
            continue
        d = _json.loads(line)
        out[d["item_id"]] = list(d.get("majority_primitives", []))
    return out


def build_regression_frame(
    screenspot_records: dict[str, list[dict[str, Any]]],
    primitive_competence: dict[str, dict[str, float]],
    llm_tags_path: str | None = "data/screenspot_pro/ssp_primitive_tags.jsonl",
):
    """Assemble the modeling table.

    screenspot_records   : {model_key: [scored ScreenSpot-Pro records]}
                           each record needs instruction, correct, target_bbox.
    primitive_competence : {model_key: {primitive: accuracy}}
    llm_tags_path        : optional path to LLM-as-judge per-item primitive tags
                           (one JSON line per item, key `majority_primitives`).
                           If present, overrides the keyword tagger which only
                           matches ~38 of 1,581 SS-Pro instructions.
    Returns a pandas DataFrame.
    """
    import pandas as pd
    prim_names = [p.value for p in PRIMITIVES]
    llm_tags = _load_llm_tags(llm_tags_path)
    rows = []
    for model_key, recs in screenspot_records.items():
        comp = primitive_competence.get(model_key, {})
        for r in recs:
            iid = r.get("item_id", r.get("instruction"))
            if llm_tags is not None and iid in llm_tags:
                req = set(llm_tags[iid])
            else:
                req = set(tag_instruction(r.get("instruction", "")))
            bbox = r.get("target_bbox") or [0, 0, 1, 1]
            row = {
                "model": model_key,
                "item": iid,
                "success": int(bool(r.get("correct"))),
                "log_area": math.log(max(1.0, (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]))),
            }
            for p in prim_names:
                row[f"feat_{p}"] = (1.0 if p in req else 0.0) * comp.get(p, 0.0)
                row[f"req_{p}"] = 1.0 if p in req else 0.0
            rows.append(row)
    return pd.DataFrame(rows)


def fit_competence_regression(df) -> dict[str, Any]:
    """Logistic regression with model fixed effects and item-clustered SEs.

    Returns a serializable summary: per-primitive coefficient, clustered p-value,
    odds ratio, plus model pseudo R-squared.
    """
    import numpy as np
    import pandas as pd
    import statsmodels.formula.api as smf

    prim_names = [p.value for p in PRIMITIVES]
    # Drop primitive features tagged on fewer than `min_active` unique SS-Pro
    # items (those columns are all-zero or near-zero-variance after the model
    # fixed effects absorb everything, which makes the design matrix singular).
    min_active = 5
    n_unique_active_items: dict[str, int] = {}
    for p in prim_names:
        col = df[f"req_{p}"]
        n_unique_active_items[p] = int((col > 0).any() and
                                       df.loc[col > 0, "item"].nunique())
    active = [p for p in prim_names if n_unique_active_items[p] >= min_active]
    dropped = [p for p in prim_names if p not in active]
    # Standardize each active feature to zero-mean / unit-variance so the
    # regression coefficients are comparable across primitives and so that
    # very-low-variance features (some primitives have nearly identical
    # competence across all models) don't blow up to extreme magnitudes.
    df = df.copy()
    for p in active:
        col = f"feat_{p}"
        mu, sd = df[col].mean(), df[col].std()
        if sd > 0:
            df[col] = (df[col] - mu) / sd
        else:
            # zero-variance feature — drop entirely
            active = [a for a in active if a != p]
            dropped = dropped + [p]
    # Also standardize log_area for the same reason.
    mu, sd = df["log_area"].mean(), df["log_area"].std()
    if sd > 0:
        df["log_area"] = (df["log_area"] - mu) / sd

    feat_terms = " + ".join(f"feat_{p}" for p in active) or "1"
    formula = f"success ~ {feat_terms} + log_area + C(model)"
    # statsmodels 0.14: cluster-robust covariance is passed to fit() directly.
    item_codes = df["item"].astype("category").cat.codes
    fitted = smf.logit(formula, data=df).fit(
        disp=False, cov_type="cluster", cov_kwds={"groups": item_codes})
    summary = {"pseudo_r2": float(fitted.prsquared), "n_obs": int(df.shape[0]),
               "active_primitives": active, "dropped_primitives": dropped,
               "primitives": {},
               # Per-feature design matrix correlation diagnostics — extreme
               # values flag inter-primitive collinearity that makes individual
               # coefficient interpretations unsafe.
               "coefficient_stability_warning": None}
    params, pvals, bse = fitted.params, fitted.pvalues, fitted.bse
    # Detect coefficient instability: extreme magnitudes signal that the
    # regression is identifying perfect / near-perfect linear combinations
    # of competence features. With n_models <= 5 this is expected when LLM
    # tagging covers many primitives.
    extreme_coefs = []
    for p in active:
        term = f"feat_{p}"
        if term in params.index:
            coef = float(params[term])
            if abs(coef) > 3.0:  # standardized coefs > 3sd are suspect
                extreme_coefs.append(p)
            se = float(bse[term]) if term in bse.index else 0.0
            summary["primitives"][p] = {
                "coef": coef,
                "odds_ratio": float(np.exp(coef)) if abs(coef) < 50 else float("inf"),
                "std_error": se,
                "p_value": float(pvals[term]),
                "unstable": abs(coef) > 3.0,
            }
    if extreme_coefs:
        summary["coefficient_stability_warning"] = (
            f"Coefficient magnitudes for {extreme_coefs} exceed 3 SD, "
            "indicating near-collinearity between competence features "
            "(expected with few unique models). Use overall pseudo-R^2 "
            "and the model-level Spearman correlation, not individual "
            "feature coefficients, as the headline statistic.")
    return summary
