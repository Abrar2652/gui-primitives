"""Statistical tests. Every headline comparison in the paper goes through here.

  * bootstrap_ci      — CIs on accuracy (no normality assumption).
  * mcnemar           — paired test for "model/intervention A vs B on the same
                        items"; exact binomial when the discordant count is small.
  * holm_bonferroni   — family-wise error control across the 7 primitives, so a
                        reviewer cannot dismiss a per-primitive finding as
                        multiple-comparisons noise.
  * cohens_h          — effect size for two proportions (report alongside p).
"""
from __future__ import annotations
import math
import random
from typing import Sequence


def bootstrap_ci(values: Sequence[float], n_resamples: int = 2000,
                 ci: float = 0.95, seed: int = 13) -> tuple[float, float, float]:
    """Percentile bootstrap CI for the mean of `values` (e.g. a 0/1 correctness
    array). Returns (point_estimate, lo, hi)."""
    vals = list(values)
    n = len(vals)
    if n == 0:
        return (float("nan"),) * 3
    rng = random.Random(seed)
    means = []
    for _ in range(n_resamples):
        s = sum(vals[rng.randrange(n)] for _ in range(n)) / n
        means.append(s)
    means.sort()
    lo = means[int((1 - ci) / 2 * n_resamples)]
    hi = means[int((1 + ci) / 2 * n_resamples) - 1]
    return (sum(vals) / n, lo, hi)


def mcnemar(a_correct: Sequence[bool], b_correct: Sequence[bool]) -> dict[str, float]:
    """Paired McNemar test. `a` and `b` are aligned per-item correctness arrays.

    Returns discordant counts, a two-sided p-value (exact binomial when the
    discordant total is small, chi-square with continuity correction otherwise),
    and the accuracy delta b - a.
    """
    if len(a_correct) != len(b_correct):
        raise ValueError("McNemar requires aligned arrays")
    b01 = sum(1 for x, y in zip(a_correct, b_correct) if x and not y)  # a right, b wrong
    b10 = sum(1 for x, y in zip(a_correct, b_correct) if not x and y)  # a wrong, b right
    n_disc = b01 + b10
    if n_disc == 0:
        p = 1.0
    elif n_disc < 25:
        # exact two-sided binomial test, p = 0.5
        k = min(b01, b10)
        tail = sum(_binom(n_disc, i) for i in range(0, k + 1)) * (0.5 ** n_disc)
        p = min(1.0, 2 * tail)
    else:
        chi2 = (abs(b01 - b10) - 1) ** 2 / n_disc
        p = _chi2_sf_1df(chi2)
    n = len(a_correct)
    delta = (sum(b_correct) - sum(a_correct)) / n if n else 0.0
    return {"b01": b01, "b10": b10, "n_discordant": n_disc, "p_value": p,
            "acc_delta": delta}


def holm_bonferroni(pvalues: dict[str, float], alpha: float = 0.05) -> dict[str, dict]:
    """Holm step-down correction. Returns per-key adjusted p and reject flag."""
    items = sorted(pvalues.items(), key=lambda kv: kv[1])
    m = len(items)
    out, running = {}, 0.0
    for rank, (key, p) in enumerate(items):
        adj = min(1.0, max(running, (m - rank) * p))
        running = adj
        out[key] = {"p_raw": p, "p_adj": adj, "reject": adj < alpha}
    return out


def cohens_h(p1: float, p2: float) -> float:
    """Effect size for the difference between two proportions."""
    phi = lambda p: 2 * math.asin(math.sqrt(min(max(p, 0.0), 1.0)))
    return phi(p1) - phi(p2)


# --------------------------- small math helpers ----------------------------
def _binom(n: int, k: int) -> float:
    return math.comb(n, k)


def _chi2_sf_1df(x: float) -> float:
    """Survival function of chi-square with 1 dof = erfc(sqrt(x/2))."""
    return math.erfc(math.sqrt(x / 2.0))
