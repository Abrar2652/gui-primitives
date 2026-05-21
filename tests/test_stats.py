"""Statistical tests: bootstrap CI, McNemar, Holm correction, effect size."""
from guiprim.eval.stats import bootstrap_ci, mcnemar, holm_bonferroni, cohens_h


def test_bootstrap_ci_brackets_mean():
    vals = [1] * 70 + [0] * 30
    mean, lo, hi = bootstrap_ci(vals, n_resamples=500)
    assert abs(mean - 0.7) < 1e-9
    assert lo <= mean <= hi
    assert 0.0 <= lo and hi <= 1.0


def test_bootstrap_ci_empty():
    mean, lo, hi = bootstrap_ci([], n_resamples=100)
    assert mean != mean  # nan


def test_mcnemar_no_difference():
    a = [True, True, False, False]
    res = mcnemar(a, a)
    assert res["n_discordant"] == 0
    assert res["p_value"] == 1.0
    assert res["acc_delta"] == 0.0


def test_mcnemar_detects_improvement():
    # b fixes 20 items a got wrong, breaks none -> strongly significant.
    a = [False] * 20 + [True] * 20
    b = [True] * 20 + [True] * 20
    res = mcnemar(a, b)
    assert res["b10"] == 20 and res["b01"] == 0
    assert res["p_value"] < 0.01
    assert abs(res["acc_delta"] - 0.5) < 1e-9


def test_holm_bonferroni_monotone_and_flags():
    pvals = {"p1": 0.001, "p2": 0.04, "p3": 0.5}
    out = holm_bonferroni(pvals, alpha=0.05)
    assert out["p1"]["reject"]
    assert not out["p3"]["reject"]
    # adjusted p-values are non-decreasing in raw rank order
    assert out["p1"]["p_adj"] <= out["p2"]["p_adj"] <= out["p3"]["p_adj"]


def test_cohens_h_sign():
    assert cohens_h(0.8, 0.5) > 0
    assert cohens_h(0.3, 0.5) < 0
    assert abs(cohens_h(0.5, 0.5)) < 1e-12
