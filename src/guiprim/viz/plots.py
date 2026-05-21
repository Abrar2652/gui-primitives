"""EMNLP camera-ready paper figures.

All figures render headless (Agg). Each plot saves *both* a vector PDF
(with TrueType-embedded fonts) and a 300-dpi PNG at exact ACL column widths
(3.3in single / 7.0in double). Each function carries a one-line docstring
naming the paper claim it supports.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Optional

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

log = logging.getLogger("guiprim.viz")

# ---------------------------------------------------------------------------
# Style: Okabe-Ito (colorblind-safe) + project indigo/terra accents
# ---------------------------------------------------------------------------
OKABE_ITO = [
    "#0072B2",  # blue
    "#D55E00",  # vermilion
    "#009E73",  # bluish green
    "#CC79A7",  # reddish purple
    "#E69F00",  # orange
    "#56B4E9",  # sky blue
    "#F0E442",  # yellow
    "#000000",  # black (use sparingly)
]
INDIGO = "#3949AB"  # project primary accent
TERRA = "#BF5B30"   # project secondary accent
GREY_FILL = "#BDBDBD"
GREY_GRID = "#E5E5E5"
GREY_SPINE = "#555555"

# ACL column widths in inches
W_SINGLE = 3.3
W_DOUBLE = 7.0

# Pretty primitive names for axis labels
PRIM_LABELS = {
    "rel_pos_horizontal": "rel-pos\nhorizontal",
    "rel_pos_vertical": "rel-pos\nvertical",
    "containment": "containment",
    "list_ordinal": "list-ordinal",
    "alignment": "alignment",
    "occlusion": "occlusion",
    "proximity": "proximity",
}

PRIM_ORDER = [
    "rel_pos_horizontal",
    "rel_pos_vertical",
    "containment",
    "list_ordinal",
    "alignment",
    "proximity",
    "occlusion",
]


def _apply_global_style() -> None:
    """Configure matplotlib for EMNLP camera-ready output once per process."""
    plt.rcParams.update({
        # Embed TrueType (Type 42) fonts so ACL print-shop accepts the PDF
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        # Sans default; falls back gracefully if Helvetica missing
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 8.0,
        "axes.labelsize": 8.5,
        "axes.titlesize": 9.0,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "legend.fontsize": 7.0,
        "axes.linewidth": 0.6,
        "axes.edgecolor": GREY_SPINE,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": GREY_GRID,
        "grid.linestyle": "-",
        "grid.linewidth": 0.4,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "xtick.major.width": 0.5,
        "ytick.major.width": 0.5,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
    })


def _save(fig, out_dir: str | Path, name: str) -> Path:
    """Save the figure as PDF (vector) and PNG (300 dpi); return PDF path."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = out_dir / f"{name}.pdf"
    png = out_dir / f"{name}.png"
    fig.savefig(pdf)
    fig.savefig(png, dpi=300)
    plt.close(fig)
    return pdf


def _x_only_grid(ax) -> None:
    """Show only horizontal y-grid; suppress x grid."""
    ax.grid(True, axis="y", linewidth=0.4, color=GREY_GRID)
    ax.grid(False, axis="x")


def _short_model(mk: str) -> str:
    """Compact display name for a model registry key."""
    table = {
        "closed_claude_haiku": "Haiku 4.5",
        "closed_claude_opus": "Opus 4.7",
        "closed_claude_sonnet": "Sonnet 4.6",
        "closed_gpt5": "GPT-5",
        "closed_gpt4_1": "GPT-4.1",
        "closed_gpt4o_mini": "GPT-4o-mini",
        "closed_gemini_flash": "Gemini-Flash",
        "qwen2_5_vl_7b": "Qwen2.5-VL",
        "qwen2_vl_7b": "Qwen2-VL",
        "os_atlas_base_7b": "OS-Atlas",
        "internvl3_8b": "InternVL3",
        "llama32_11b_vision": "Llama-3.2",
        "minicpm_v_ollama": "MiniCPM-V",
        "gemma3_4b": "Gemma3-4B",
        "gemma3_12b": "Gemma3-12B",
        "gemma3_27b": "Gemma3-27B",
        "gemma3_27b_ollama": "Gemma3-27B-q4",
        "paligemma2_3b": "PaliGemma2-3B",
        "paligemma2_10b": "PaliGemma2-10B",
    }
    return table.get(mk, mk)


def _sig_marker(p: float) -> str:
    """ACL-style significance marker from a Holm-adjusted p-value."""
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return "n.s."


# ---------------------------------------------------------------------------
# Figure 1 — minimal-pair conceptual teaser
# ---------------------------------------------------------------------------

def fig_teaser_minimal_pair(items_path: Path, out_dir: str | Path) -> Optional[Path]:
    """Fig 1: minimal-pair teaser — illustrates the diagnostic design (Claim 1)."""
    _apply_global_style()
    try:
        from PIL import Image
    except ImportError:
        log.warning("teaser: PIL unavailable -> skip")
        return None

    items = [json.loads(l) for l in Path(items_path).open()]
    # Choose a clean rel_pos_horizontal minimal pair from ui_vision
    from collections import defaultdict
    pairs: dict = defaultdict(list)
    for it in items:
        if it.get("source") == "ui_vision" and it.get("primitive") == "rel_pos_horizontal":
            pairs[it["pair_id"]].append(it)
    cand = [(pid, ps) for pid, ps in pairs.items() if len(ps) == 2]
    if not cand:
        log.warning("teaser: no ui_vision horizontal pair -> skip")
        return None

    # Prefer one whose two bboxes are within a comfortable crop window
    def _score(ps):
        b0, b1 = ps[0]["target_bbox"], ps[1]["target_bbox"]
        dx = abs(b0[0] - b1[0])
        return -dx if dx > 60 else -1e9
    pid, ps = max(cand, key=lambda c: _score(c[1]))
    img_path = ps[0]["image_path"]
    if not Path(img_path).exists():
        log.warning("teaser: image %s missing -> skip", img_path)
        return None

    img = Image.open(img_path).convert("RGB")
    W, H = img.size

    # Crop window: tight box around both targets with padding
    boxes = [p["target_bbox"] for p in ps]
    xs = [b[0] for b in boxes] + [b[2] for b in boxes]
    ys = [b[1] for b in boxes] + [b[3] for b in boxes]
    cx0, cy0, cx1, cy1 = min(xs), min(ys), max(xs), max(ys)
    pad_x = max(140, 0.5 * (cx1 - cx0))
    pad_y = max(40, 0.8 * (cy1 - cy0))
    cx0 = max(0, int(cx0 - pad_x))
    cy0 = max(0, int(cy0 - pad_y))
    cx1 = min(W, int(cx1 + pad_x))
    cy1 = min(H, int(cy1 + pad_y))
    crop = img.crop((cx0, cy0, cx1, cy1))
    cw, ch = crop.size
    img_aspect = ch / cw

    # Two stacked panels: image (top) + caption block (bottom)
    fig = plt.figure(figsize=(W_SINGLE, W_SINGLE * img_aspect + 0.95))
    gs = fig.add_gridspec(2, 1,
                          height_ratios=[img_aspect, 0.95 / W_SINGLE],
                          hspace=0.05)
    ax = fig.add_subplot(gs[0, 0])
    ax.imshow(crop)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.grid(False)
    ax.set_title("Minimal pair: same image, swapped relational word",
                 fontsize=8.5, pad=3)

    # Overlay target boxes
    colors = [INDIGO, TERRA]
    for (b, c) in zip(boxes, colors):
        x0, y0, x1, y1 = [b[0] - cx0, b[1] - cy0, b[2] - cx0, b[3] - cy0]
        ax.add_patch(mpatches.Rectangle(
            (x0, y0), x1 - x0, y1 - y0,
            fill=False, edgecolor=c, linewidth=1.6,
        ))

    # Caption panel: colored bullets + instructions
    cap_ax = fig.add_subplot(gs[1, 0])
    cap_ax.set_xticks([]); cap_ax.set_yticks([])
    for s in ("top", "right", "left", "bottom"):
        cap_ax.spines[s].set_visible(False)
    cap_ax.grid(False)
    cap_ax.set_xlim(0, 1); cap_ax.set_ylim(0, 1)

    inst_a = ps[0]["instruction"].rstrip(".")
    inst_b = ps[1]["instruction"].rstrip(".")
    cap_ax.add_patch(mpatches.Rectangle((0.02, 0.62), 0.05, 0.20,
                                        fill=False, edgecolor=INDIGO, linewidth=1.6,
                                        transform=cap_ax.transAxes))
    cap_ax.text(0.10, 0.72, f'A:  "{inst_a}"', fontsize=7.5,
                va="center", color="black", transform=cap_ax.transAxes)
    cap_ax.add_patch(mpatches.Rectangle((0.02, 0.22), 0.05, 0.20,
                                        fill=False, edgecolor=TERRA, linewidth=1.6,
                                        transform=cap_ax.transAxes))
    cap_ax.text(0.10, 0.32, f'B:  "{inst_b}"', fontsize=7.5,
                va="center", color="black", transform=cap_ax.transAxes)

    return _save(fig, out_dir, "fig1_minimal_pair_teaser")


# ---------------------------------------------------------------------------
# Figure 2 — per-primitive accuracy across VLMs (bootstrap CI + chance lines)
# ---------------------------------------------------------------------------

def fig_per_primitive(
    table: dict[str, dict[str, dict]],
    chance: dict[str, float],
    out_dir: str | Path,
    top_n: int = 8,
) -> Path:
    """Fig 2: per-primitive accuracy with bootstrap-CI bars (Claim 2)."""
    _apply_global_style()

    prims = [p for p in PRIM_ORDER if p in {q for m in table.values() for q in m}]
    if not prims:
        prims = sorted({p for m in table.values() for p in m})

    # Rank models by mean accuracy across primitives and keep top-N
    def _mean_acc(mk):
        accs = [table[mk][p]["accuracy"] for p in prims if p in table[mk]]
        return float(np.mean(accs)) if accs else 0.0
    models = sorted(table, key=_mean_acc, reverse=True)[:top_n]

    fig, ax = plt.subplots(figsize=(W_DOUBLE, 2.6))
    group_width = 0.84
    bar_w = group_width / max(1, len(models))
    x_centers = np.arange(len(prims))

    for i, mk in enumerate(models):
        ys = [table[mk].get(p, {}).get("accuracy", np.nan) for p in prims]
        lo = [table[mk].get(p, {}).get("ci_lo", y) for p, y in zip(prims, ys)]
        hi = [table[mk].get(p, {}).get("ci_hi", y) for p, y in zip(prims, ys)]
        err_low = [max(0.0, y - l) for y, l in zip(ys, lo)]
        err_high = [max(0.0, h - y) for y, h in zip(ys, hi)]
        xs = x_centers - group_width / 2 + i * bar_w + bar_w / 2
        ax.bar(xs, ys, width=bar_w * 0.92,
               color=OKABE_ITO[i % len(OKABE_ITO)],
               edgecolor="black", linewidth=0.6,
               label=_short_model(mk))
        ax.errorbar(xs, ys, yerr=[err_low, err_high], fmt="none",
                    ecolor=GREY_SPINE, elinewidth=0.5, capsize=1.2)

    # Chance lines per primitive (dashed segments above their group)
    for j, p in enumerate(prims):
        c = chance.get(p, 0.5)
        ax.hlines(c, j - group_width / 2 - 0.04, j + group_width / 2 + 0.04,
                  colors=GREY_SPINE, linestyles=(0, (3, 2)), linewidth=0.6)

    ax.set_xticks(x_centers)
    ax.set_xticklabels([PRIM_LABELS.get(p, p) for p in prims])
    ax.set_ylabel("point-in-box accuracy")
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    _x_only_grid(ax)

    # Legend above the plot, single row if it fits
    ncol = min(len(models), 8)
    leg = ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.20),
                    ncol=ncol, frameon=False, handlelength=1.2,
                    columnspacing=0.9, handletextpad=0.4)

    # Chance-line key in lower right
    ax.plot([], [], linestyle=(0, (3, 2)), color=GREY_SPINE,
            linewidth=0.8, label="chance")
    return _save(fig, out_dir, "fig2_per_primitive")


# ---------------------------------------------------------------------------
# Figure 3 — intervention deltas (paired-bar with Holm-adjusted markers)
# ---------------------------------------------------------------------------

def fig_intervention_deltas(
    deltas_with_ci: dict[str, dict[str, dict]],
    comparisons_holm: dict[str, dict[str, dict]],
    out_dir: str | Path,
) -> Path:
    """Fig 3: training-free intervention deltas with Holm-corrected sig (Claim 3)."""
    _apply_global_style()

    iv_order = ["som", "cot", "steering"]
    iv_label = {"som": "Set-of-Mark", "cot": "CoT", "steering": "Steering"}
    models = [m for m in deltas_with_ci if any(iv in deltas_with_ci[m] for iv in iv_order)]
    if not models:
        log.warning("intervention deltas: no data -> skip")
        return Path()
    # Show open replication pair first (full intervention triple), then
    # closed APIs (SoM-only). Within each tier, by descending baseline.
    def _is_closed(m): return m.startswith("closed_")
    def _max_base(m):
        return max((deltas_with_ci[m][iv]["baseline_acc"]
                    for iv in iv_order if iv in deltas_with_ci[m]), default=0.0)
    open_models = sorted([m for m in models if not _is_closed(m)], key=_max_base, reverse=True)
    closed_models = sorted([m for m in models if _is_closed(m)], key=_max_base, reverse=True)
    models = open_models + closed_models

    fig, ax = plt.subplots(figsize=(W_DOUBLE, 2.6))
    iv_present = [iv for iv in iv_order if any(iv in deltas_with_ci[m] for m in models)]
    iv_x = np.arange(len(iv_present))
    bar_w = 0.82 / max(1, len(models))

    for i, mk in enumerate(models):
        ys, lo, hi, stars = [], [], [], []
        for iv in iv_present:
            d = deltas_with_ci[mk].get(iv)
            if d is None:
                ys.append(0.0); lo.append(0.0); hi.append(0.0); stars.append("")
                continue
            ys.append(d["delta"])
            lo.append(d.get("delta_ci_lo", d["delta"]))
            hi.append(d.get("delta_ci_hi", d["delta"]))
            p_adj = comparisons_holm.get(mk, {}).get(iv, {}).get("p_adj", 1.0)
            stars.append(_sig_marker(p_adj))
        xs = iv_x - bar_w / 2 + i * bar_w
        ax.bar(xs, ys, width=bar_w * 0.92,
               color=OKABE_ITO[i], edgecolor="black", linewidth=0.7,
               label=_short_model(mk))
        ax.errorbar(xs, ys, yerr=[[max(0.0, y - l) for y, l in zip(ys, lo)],
                                  [max(0.0, h - y) for y, h in zip(ys, hi)]],
                    fmt="none", ecolor=GREY_SPINE, elinewidth=0.5, capsize=1.2)
        # Significance stars above bars
        for x, y, s in zip(xs, ys, stars):
            if s:
                ax.text(x, y + 0.012, s, ha="center", va="bottom", fontsize=6.5)

    ax.axhline(0, color=GREY_SPINE, linewidth=0.6)
    ax.set_xticks(iv_x)
    ax.set_xticklabels([iv_label.get(iv, iv) for iv in iv_present], rotation=0)
    ax.set_ylabel(r"$\Delta$ accuracy vs baseline")
    _x_only_grid(ax)

    # Compute headroom so the in-plot key never overlaps the bars
    max_top = 0.0
    for mk in models:
        for iv in iv_present:
            d = deltas_with_ci[mk].get(iv)
            if d is None:
                continue
            max_top = max(max_top, d.get("delta_ci_hi", d["delta"]))
    ax.set_ylim(top=max(0.5, max_top * 1.40))

    # Model legend (top-right)
    ax.legend(loc="upper right", frameon=False, handlelength=1.2,
              bbox_to_anchor=(1.0, 1.0))

    # Significance key — narrow vertical stack at mid-right,
    # in the empty band between the SoM bars and the CoT/Steering bars.
    sig_txt = (
        r"$^{***}\,p_\mathrm{adj}{<}0.001$" "\n"
        r"$^{**}\,p_\mathrm{adj}{<}0.01$"   "\n"
        r"$^{*}\,p_\mathrm{adj}{<}0.05$"    "\n"
        "n.s. = not significant"            "\n"
        "(paired McNemar, Holm)"
    )
    ax.text(0.98, 0.50, sig_txt, transform=ax.transAxes,
            ha="right", va="center", fontsize=6.2, color=GREY_SPINE,
            linespacing=1.5,
            bbox=dict(facecolor="white", edgecolor=GREY_GRID,
                      linewidth=0.4, boxstyle="round,pad=0.35"))
    return _save(fig, out_dir, "fig3_intervention_deltas")


# ---------------------------------------------------------------------------
# Figure 4 — shortcut-control collapse
# ---------------------------------------------------------------------------

def fig_controls(controls_block: dict[str, dict], out_dir: str | Path) -> Path:
    """Fig 4: shortcut controls — main vs text-only/shuffled/blur (Claim 2 robustness)."""
    _apply_global_style()
    if not controls_block:
        log.warning("controls: no data -> skip")
        return Path()

    cond_order = ["main", "text_only", "shuffled", "blur"]
    cond_label = {"main": "main", "text_only": "text\nonly", "shuffled": "shuffled", "blur": "blur"}
    models = list(controls_block)

    fig, ax = plt.subplots(figsize=(W_SINGLE, 2.4))
    bar_w = 0.7 / max(1, len(models))
    x = np.arange(len(cond_order))

    for i, mk in enumerate(models):
        ck = controls_block[mk]
        acc = ck.get("accuracy", ck) if isinstance(ck, dict) else ck
        ys = [acc.get(c, 0.0) for c in cond_order]
        xs = x - 0.35 + i * bar_w + bar_w / 2
        # Color: main = indigo; controls = terra; failing check = grey hatch
        colors, hatches = [], []
        for c in cond_order:
            if c == "main":
                colors.append(INDIGO); hatches.append(None)
            else:
                check = (ck.get("checks") or {}).get(c, {})
                if check and not check.get("passed", True):
                    colors.append(GREY_FILL); hatches.append("//")
                else:
                    colors.append(TERRA); hatches.append(None)
        bars = ax.bar(xs, ys, width=bar_w * 0.92,
                      color=colors, edgecolor="black", linewidth=0.7)
        for b, h in zip(bars, hatches):
            if h:
                b.set_hatch(h)

    # Annotate the "expected drop" with arrow from main -> text_only of the first model
    if models:
        mk = models[0]
        acc = controls_block[mk].get("accuracy", controls_block[mk])
        if "main" in acc and "text_only" in acc:
            ax.annotate(
                f"−{(acc['main']-acc['text_only'])*100:.0f}pt",
                xy=(1.0, acc["text_only"]), xytext=(0.5, acc["main"] + 0.05),
                ha="center", fontsize=7,
                arrowprops=dict(arrowstyle="->", color=GREY_SPINE, lw=0.6),
            )

    ax.set_xticks(x)
    ax.set_xticklabels([cond_label[c] for c in cond_order])
    ax.set_ylabel("accuracy")
    ax.set_ylim(0, max(0.3, max((controls_block[m].get("accuracy", controls_block[m])).get("main", 0.0)
                                for m in models) * 1.25))
    _x_only_grid(ax)

    # Legend keys
    legend_items = [
        mpatches.Patch(color=INDIGO, label="main"),
        mpatches.Patch(color=TERRA, label="control (passes test)"),
        mpatches.Patch(facecolor=GREY_FILL, hatch="//", edgecolor="white",
                       label="control (failed test)"),
    ]
    ax.legend(handles=legend_items, loc="upper right", frameon=False,
              handlelength=1.4, fontsize=6.5)
    return _save(fig, out_dir, "fig4_controls")


# ---------------------------------------------------------------------------
# Figure 5 — primitive → ScreenSpot-Pro regression forest plot
# ---------------------------------------------------------------------------

def fig_regression_forest(reg: dict[str, Any], out_dir: str | Path) -> Path:
    """Fig 5: primitive→ScreenSpot-Pro odds-ratio forest plot (Claim 2 headline)."""
    _apply_global_style()
    prims_d = reg.get("primitives", {})
    if not prims_d:
        log.warning("regression: no primitives in summary -> skip")
        return Path()

    # Sort by primitive order; recover SE from p when not stored
    from scipy.stats import norm as _norm
    rows = []
    for p in PRIM_ORDER:
        if p not in prims_d:
            continue
        v = prims_d[p]
        coef = v["coef"]
        pval = v.get("p_value", 1.0)
        se = v.get("std_error", 0.0) or 0.0
        if se <= 0 and abs(coef) > 1e-9 and 0 < pval < 1:
            # |z| = inverse-normal(1 - p/2); se = |coef|/|z|
            z_abs = float(abs(_norm.ppf(1.0 - pval / 2.0)))
            if z_abs > 1e-9:
                se = abs(coef) / z_abs
        z = 1.96
        odds = float(np.exp(coef))
        lo = float(np.exp(coef - z * se)) if se > 0 else odds
        hi = float(np.exp(coef + z * se)) if se > 0 else odds
        rows.append((p, coef, odds, lo, hi, pval))

    fig, ax = plt.subplots(figsize=(W_SINGLE, 2.4))
    y_pos = np.arange(len(rows))[::-1]  # top primitive at top
    for (p, coef, odds, lo, hi, pval), y in zip(rows, y_pos):
        color = INDIGO if pval < 0.05 else GREY_FILL
        ax.plot([lo, hi], [y, y], color=color, linewidth=1.2)
        ax.plot(odds, y, "o", color=color, markersize=4.5, markeredgewidth=0)
        # p-value annotation on the right
        sig = _sig_marker(pval)
        if sig != "n.s.":
            ax.text(max(hi, odds) * 1.05, y, sig, va="center", fontsize=6.5, color=color)

    ax.axvline(1.0, color=GREY_SPINE, linestyle=(0, (3, 2)), linewidth=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([PRIM_LABELS.get(p, p).replace("\n", " ") for p, *_ in rows])
    ax.set_xlabel("odds ratio (95% CI, item-clustered)")
    ax.set_xscale("log")
    # Sane tick range
    all_lo = [r[3] for r in rows] + [1.0]
    all_hi = [r[4] for r in rows] + [1.0]
    ax.set_xlim(min(all_lo) * 0.85, max(all_hi) * 1.15)
    _x_only_grid(ax)
    ax.grid(True, axis="x", linewidth=0.4, color=GREY_GRID)

    r2 = reg.get("pseudo_r2", float("nan"))
    n = reg.get("n_obs", 0)
    ax.set_title(rf"primitive $\rightarrow$ ScreenSpot-Pro    "
                 rf"pseudo-$R^2$={r2:.3f}  $n$={n:,}", fontsize=8.5, pad=4)
    return _save(fig, out_dir, "fig5_regression_forest")


# ---------------------------------------------------------------------------
# Supplementary S1 — model × primitive accuracy heatmap
# ---------------------------------------------------------------------------

def fig_supp_heatmap(
    table: dict[str, dict[str, dict]],
    out_dir: str | Path,
) -> Path:
    """Supp. S1: model×primitive accuracy heatmap (overview, greyscale-safe)."""
    _apply_global_style()
    prims = [p for p in PRIM_ORDER if p in {q for m in table.values() for q in m}]
    if not prims:
        prims = sorted({p for m in table.values() for p in m})

    # Sort models by mean across primitives, descending
    def _mean_acc(mk):
        return float(np.mean([table[mk][p]["accuracy"] for p in prims if p in table[mk]] or [0]))
    models = sorted(table, key=_mean_acc, reverse=True)
    M = np.array([[table[mk].get(p, {}).get("accuracy", np.nan) for p in prims]
                  for mk in models])

    h = 0.18 * len(models) + 0.8
    fig, ax = plt.subplots(figsize=(W_DOUBLE, h))
    im = ax.imshow(M, aspect="auto", cmap="viridis", vmin=0, vmax=1)
    ax.set_xticks(np.arange(len(prims)))
    ax.set_xticklabels([PRIM_LABELS.get(p, p).replace("\n", " ") for p in prims],
                       rotation=30, ha="right")
    ax.set_yticks(np.arange(len(models)))
    ax.set_yticklabels([_short_model(mk) for mk in models])
    ax.set_xlabel("primitive")
    ax.grid(False)
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)

    # Cell text annotation (skipped if too dense)
    if len(models) * len(prims) <= 140:
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                v = M[i, j]
                if np.isnan(v):
                    continue
                color = "white" if v < 0.5 else "black"
                ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                        fontsize=6.0, color=color)

    cbar = fig.colorbar(im, ax=ax, fraction=0.018, pad=0.01)
    cbar.set_label("accuracy", fontsize=7.5)
    cbar.ax.tick_params(labelsize=6.5)
    return _save(fig, out_dir, "fig_supp_heatmap")


# ---------------------------------------------------------------------------
# Supplementary S2 — attention map from the top localization head
# ---------------------------------------------------------------------------

def fig_supp_attention(
    heads_json: Path,
    items_path: Path,
    out_dir: str | Path,
) -> Optional[Path]:
    """Supp. S2: overlay top localization-head attention on one item (Claim 3 mechanism)."""
    _apply_global_style()
    heads_json = Path(heads_json)
    if not heads_json.exists():
        log.warning("supp attention: %s missing -> skip", heads_json)
        return None
    try:
        meta = json.loads(heads_json.read_text())
    except Exception as e:
        log.warning("supp attention: failed to load heads json (%s) -> skip", e)
        return None

    # Expected schema: {"item_id":..., "image_path":..., "attention_grid":[[...]], "target_bbox":[...]}
    item_id = meta.get("item_id")
    img_path = meta.get("image_path")
    grid = meta.get("attention_grid")
    bbox = meta.get("target_bbox")
    if not (img_path and grid):
        log.warning("supp attention: heads json lacks attention_grid/image_path -> skip")
        return None

    try:
        from PIL import Image
    except ImportError:
        log.warning("supp attention: PIL unavailable -> skip")
        return None
    if not Path(img_path).exists():
        log.warning("supp attention: image %s missing -> skip", img_path)
        return None

    img = np.array(Image.open(img_path).convert("RGB"))
    H, W = img.shape[:2]
    A = np.array(grid, dtype=float)
    A = (A - A.min()) / (A.max() - A.min() + 1e-9)

    fig, ax = plt.subplots(figsize=(W_SINGLE, W_SINGLE * H / max(W, 1)))
    ax.imshow(img)
    ax.imshow(A, extent=[0, W, H, 0], cmap="magma", alpha=0.45, interpolation="bilinear")
    if bbox:
        ax.add_patch(mpatches.Rectangle(
            (bbox[0], bbox[1]), bbox[2] - bbox[0], bbox[3] - bbox[1],
            fill=False, edgecolor="white", linewidth=1.2,
        ))
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.set_title(f"top localization head, item {item_id}", fontsize=8.5, pad=3)
    ax.grid(False)
    return _save(fig, out_dir, "fig_supp_attention")


# ---------------------------------------------------------------------------
# Figure 6 — Headline scatter: GUI-Primitives vs ScreenSpot-Pro (per model)
# ---------------------------------------------------------------------------

def fig_headline_scatter(
    stratified_corr: dict[str, Any],
    out_dir: str | Path,
) -> Optional[Path]:
    """Fig 6: per-model GUI-Primitives competence vs SS-Pro success (headline scatter)."""
    _apply_global_style()
    per = stratified_corr.get("per_model", {})
    corrs = stratified_corr.get("correlations", {}).get("all", {})
    if not per:
        log.warning("headline scatter: no per_model data -> skip")
        return None

    xs, ys, names = [], [], []
    for mk, v in per.items():
        if v.get("ssp") is None:
            continue
        xs.append(v["all"]); ys.append(v["ssp"]); names.append(mk)
    if len(xs) < 3:
        log.warning("headline scatter: %d models with both axes -> skip", len(xs))
        return None
    xs = np.array(xs); ys = np.array(ys)

    fig, ax = plt.subplots(figsize=(W_SINGLE, W_SINGLE * 0.92))

    # Least-squares line + a bootstrap 95% CI band on the regression line
    rng = np.random.default_rng(0)
    n = len(xs)
    x_grid = np.linspace(xs.min() * 0.95, xs.max() * 1.05, 80)
    boots = []
    for _ in range(1000):
        idx = rng.integers(0, n, n)
        if len(np.unique(xs[idx])) < 2:
            continue
        m_, b_ = np.polyfit(xs[idx], ys[idx], 1)
        boots.append(m_ * x_grid + b_)
    boots = np.array(boots)
    band_lo = np.percentile(boots, 2.5, axis=0)
    band_hi = np.percentile(boots, 97.5, axis=0)
    m, b = np.polyfit(xs, ys, 1)
    ax.fill_between(x_grid, band_lo, band_hi, color=INDIGO, alpha=0.12,
                    linewidth=0)
    ax.plot(x_grid, m * x_grid + b, color=INDIGO, linewidth=1.0)

    # Single marker style (color-coded closed vs open), with manually-tuned
    # label offsets for the 10 model points to avoid overlaps.
    closed_keys = {k for k in names if k.startswith("closed_")}
    for x, y, nm in zip(xs, ys, names):
        col = TERRA if nm in closed_keys else INDIGO
        ax.scatter(x, y, s=30, facecolor=col, edgecolor="black",
                   linewidth=0.5, zorder=3)

    # Horizontal labels with hand-tuned offsets per model. The bottom-
    # cluster uses a staircase of y-offsets so each label sits at its own
    # vertical band. Opus and OS-Atlas labels point LEFT to clear the
    # right-side stat box and the bottom-cluster staircase respectively.
    # ("ha=right" means the label's right edge sits at the offset point.)
    # Convention: every label sits at upper-right (dx=+6 pt) of its
    # dot, only the dy varies. Bottom-cluster dots are too close in x
    # for all labels to share one row, so dy climbs as a "staircase" so
    # each label gets its own y band. A thin vertical leader line
    # connects each raised label to its dot so the dot directly below
    # the label is the one being named.
    label_spec = {
        # name                        : (dx, dy)
        "closed_claude_opus":           ( -5,  6),
        "qwen2_5_vl_7b":                ( -5,  6),
        "closed_claude_sonnet":         ( -5,  6),
        "os_atlas_base_7b":             ( -10,  8),
        "closed_gpt5":                  ( -5,  6),
        # bottom cluster (all at y≈0.003) sorted by x — staircase y-offset
        "llama32_11b_vision":           ( -5,  6),    # x=0.012
        "qwen2_vl_7b":                  ( -10, 15),    # x=0.038
        "internvl3_8b":                 ( -5, 25),    # x=0.095
        "gemma3_27b_ollama":            ( 7, 35),    # x=0.103
        "gemma3_27b":                   ( 6, 6),    # x=0.134 (far enough right that low dy is safe)
    }
    arrow_props = dict(arrowstyle="-", color=GREY_SPINE, lw=0.4,
                       shrinkA=0, shrinkB=2)
    for x, y, nm in zip(xs, ys, names):
        dx, dy = label_spec.get(nm, (6, 6))
        ax.annotate(_short_model(nm), xy=(x, y), xytext=(dx, dy),
                    textcoords="offset points",
                    fontsize=6.2, color="black",
                    ha="left", va="bottom",
                    arrowprops=arrow_props)

    ax.set_xlabel("per-model GUI-Primitives accuracy")
    ax.set_ylabel("per-model ScreenSpot-Pro accuracy")
    ax.set_xlim(0, max(xs) * 1.12)
    ax.set_ylim(0, max(ys) * 1.18)
    _x_only_grid(ax)
    ax.grid(True, axis="x", linewidth=0.4, color=GREY_GRID)

    # Correlation panel + marker legend (upper-left inside the plot)
    rho = corrs.get("spearman_rho", float("nan"))
    rho_p = corrs.get("spearman_p", float("nan"))
    r = corrs.get("pearson_r", float("nan"))
    r_p = corrs.get("pearson_p", float("nan"))
    n_models = corrs.get("n_models", len(xs))
    txt = (
        rf"Spearman $\rho$={rho:+.3f}  ($p$={rho_p:.3f})" + "\n"
        rf"Pearson $r$={r:+.3f}  ($p$={r_p:.3f})" + "\n"
        rf"$n$={n_models} models"
    )
    ax.text(0.03, 0.97, txt, transform=ax.transAxes, ha="left", va="top",
            fontsize=6.5, color="black", linespacing=1.5,
            bbox=dict(facecolor="white", edgecolor="black",
                      linewidth=0.6, boxstyle="round,pad=0.35"))
    # No in-plot marker legend (orange = closed API, indigo = open weights;
    # explained in the figure caption to keep the plot uncluttered).
    return _save(fig, out_dir, "fig6_headline_scatter")


# ---------------------------------------------------------------------------
# Figure 7 — Human-vs-model ceiling gap (clean 185-item split)
# ---------------------------------------------------------------------------

def fig_human_gap(
    clean_block: dict[str, dict],
    human_acc: float,
    out_dir: str | Path,
    top_n: int = 12,
) -> Optional[Path]:
    """Fig 7: human-vs-model accuracy gap on the n=185 verified-clean core."""
    _apply_global_style()
    if not clean_block:
        log.warning("human gap: no clean comparison -> skip")
        return None

    pairs = [(mk, v["overall_accuracy"]) for mk, v in clean_block.items()
             if v.get("overall_accuracy") is not None]
    pairs.sort(key=lambda kv: -kv[1])
    pairs = pairs[:top_n]
    if not pairs:
        log.warning("human gap: no non-null accuracies -> skip")
        return None

    fig, ax = plt.subplots(figsize=(W_SINGLE, max(1.8, 0.18 * len(pairs) + 0.6)))
    y_pos = np.arange(len(pairs))
    closed_keys = {mk for mk, _ in pairs if mk.startswith("closed_")}
    colors = [TERRA if mk in closed_keys else INDIGO for mk, _ in pairs]
    ax.barh(y_pos, [a for _, a in pairs], color=colors,
            edgecolor="black", linewidth=0.5, height=0.72)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([_short_model(mk) for mk, _ in pairs])
    ax.invert_yaxis()
    ax.set_xlabel("accuracy on $n{=}185$ human-clean core")
    ax.set_xlim(0, 1.0)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.grid(True, axis="x", linewidth=0.4, color=GREY_GRID)
    ax.grid(False, axis="y")

    # Human ceiling line
    ax.axvline(human_acc, color="black", linestyle=(0, (3, 2)), linewidth=0.8)

    # Best-model gap arrow at the top, with the gap label above and the
    # "human ceiling" tag offset BELOW the arrow so they don't overlap.
    best_mk, best_acc = pairs[0]
    ax.annotate("",
                xy=(best_acc, -0.6), xytext=(human_acc, -0.6),
                arrowprops=dict(arrowstyle="<->", color=GREY_SPINE,
                                lw=0.6, shrinkA=2, shrinkB=2))
    gap = human_acc - best_acc
    ax.text((human_acc + best_acc) / 2, -0.95,
            f"{gap*100:.0f}-pt human-model gap",
            ha="center", va="bottom", fontsize=6.5, color="black",
            style="italic")
    ax.text(human_acc, -0.10, f"human  {human_acc:.2f}",
            ha="right", va="top", fontsize=6.5, color="black",
            style="italic", rotation=90)

    # Legend (top-right, away from the data-poor bottom)
    handles = [
        mpatches.Patch(facecolor=TERRA, edgecolor="black", linewidth=0.5,
                       label="closed API"),
        mpatches.Patch(facecolor=INDIGO, edgecolor="black", linewidth=0.5,
                       label="open weights"),
    ]
    ax.legend(handles=handles, loc="lower right", frameon=False,
              fontsize=6.5, handlelength=1.0,
              bbox_to_anchor=(1.0, 0.02))
    return _save(fig, out_dir, "fig7_human_gap")


# ---------------------------------------------------------------------------
# Figure 8 — Pair-consistency (What's-Up signature)
# ---------------------------------------------------------------------------

def fig_pair_consistency(
    table: dict[str, dict[str, dict]],
    out_dir: str | Path,
    top_n: int = 8,
    min_pairs: int = 20,
) -> Path:
    """Fig 8: pair-consistency vs accuracy — the relational-failure signature."""
    _apply_global_style()
    prims = [p for p in PRIM_ORDER if p in {q for m in table.values() for q in m}]

    def _mean_acc(mk):
        return float(np.mean([table[mk][p]["accuracy"] for p in prims
                              if p in table[mk]] or [0.0]))
    models = sorted(table, key=_mean_acc, reverse=True)[:top_n]

    fig, ax = plt.subplots(figsize=(W_SINGLE, W_SINGLE * 0.92))
    # Color = model index; marker shape = primitive class
    prim_marker = {
        "rel_pos_horizontal": "o", "rel_pos_vertical": "s",
        "containment": "^", "list_ordinal": "D",
        "alignment": "P", "proximity": "X", "occlusion": "*",
    }
    for i, mk in enumerate(models):
        color = OKABE_ITO[i % len(OKABE_ITO)]
        for p in prims:
            cell = table[mk].get(p, {})
            acc = cell.get("accuracy")
            pc = cell.get("pair_consistency")
            n_pairs = cell.get("n_complete_pairs", 0)
            if acc is None or pc is None or n_pairs < min_pairs:
                continue
            ax.scatter(acc, pc, marker=prim_marker.get(p, "o"),
                       facecolor=color, edgecolor="black", linewidth=0.4,
                       s=24, alpha=0.85, zorder=3)

    # Diagonal y=x (upper bound: pair_consistency <= min(acc_pair_a, acc_pair_b) <= acc)
    lim = 1.0
    ax.plot([0, lim], [0, lim], color=GREY_SPINE,
            linestyle=(0, (3, 2)), linewidth=0.6, zorder=1, label="$y=x$")

    ax.set_xlabel("per-primitive accuracy")
    ax.set_ylabel("pair-consistency (both pair-items correct)")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_aspect("equal", adjustable="box")
    _x_only_grid(ax)
    ax.grid(True, axis="x", linewidth=0.4, color=GREY_GRID)

    # Primitive marker legend (compact)
    prim_handles = []
    for p in prims:
        prim_handles.append(plt.Line2D([0], [0], marker=prim_marker.get(p, "o"),
                                       linestyle="", markersize=4.5,
                                       markerfacecolor=GREY_FILL,
                                       markeredgecolor="black",
                                       markeredgewidth=0.4,
                                       label=PRIM_LABELS.get(p, p).replace("\n", " ")))
    ax.legend(handles=prim_handles, loc="lower right", frameon=False,
              fontsize=5.8, handlelength=0.8, ncol=1,
              labelspacing=0.25)
    ax.text(0.02, 0.97,
            "below $y{=}x$ = ‘guessed individual items\nbut failed the relational pair’",
            transform=ax.transAxes, ha="left", va="top",
            fontsize=6.0, color=GREY_SPINE, style="italic",
            linespacing=1.4)
    return _save(fig, out_dir, "fig8_pair_consistency")


# ---------------------------------------------------------------------------
# Figure 9 — Per-primitive SoM lift (where the intervention works)
# ---------------------------------------------------------------------------

def fig_som_per_primitive(
    per_prim_block: dict[str, dict[str, dict[str, dict]]],
    out_dir: str | Path,
) -> Optional[Path]:
    """Fig 9: per-primitive Set-of-Mark accuracy delta with CIs (which primitives benefit)."""
    _apply_global_style()
    models = [m for m in per_prim_block if "som" in per_prim_block.get(m, {})]
    if not models:
        log.warning("som per-primitive: no SoM data -> skip")
        return None

    prims = [p for p in PRIM_ORDER
             if any(p in per_prim_block[m]["som"] for m in models)]
    if not prims:
        log.warning("som per-primitive: no primitives -> skip")
        return None

    fig, ax = plt.subplots(figsize=(W_SINGLE, 0.32 * len(prims) + 0.9))
    bar_h = 0.36
    y_pos = np.arange(len(prims))[::-1]

    for i, mk in enumerate(models[:2]):
        deltas, lo, hi, sigs = [], [], [], []
        for p in prims:
            d = per_prim_block[mk]["som"].get(p, {})
            deltas.append(d.get("delta", 0.0))
            lo.append(d.get("delta_ci_lo", deltas[-1]))
            hi.append(d.get("delta_ci_hi", deltas[-1]))
            sigs.append(bool(d.get("sig", False)))
        ys = y_pos + (i - 0.5) * bar_h
        ax.barh(ys, deltas, height=bar_h * 0.92,
                color=OKABE_ITO[i], edgecolor="black", linewidth=0.5,
                label=_short_model(mk))
        ax.errorbar(deltas, ys,
                    xerr=[[max(0.0, d - l) for d, l in zip(deltas, lo)],
                          [max(0.0, h - d) for d, h in zip(deltas, hi)]],
                    fmt="none", ecolor=GREY_SPINE,
                    elinewidth=0.5, capsize=1.2)
        for d, y, s in zip(deltas, ys, sigs):
            if s:
                ax.text(d + 0.012, y, "*", ha="left", va="center", fontsize=7)

    ax.axvline(0, color=GREY_SPINE, linewidth=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([PRIM_LABELS.get(p, p).replace("\n", " ") for p in prims])
    ax.set_xlabel(r"Set-of-Mark $\Delta$ accuracy vs baseline")
    _x_only_grid(ax)
    ax.grid(True, axis="x", linewidth=0.4, color=GREY_GRID)
    ax.grid(False, axis="y")

    # Extend x to the left so the legend sits in the (mostly empty) negative
    # half rather than colliding with the SoM bars
    xmin, xmax = ax.get_xlim()
    ax.set_xlim(min(xmin, -0.5), xmax)
    # Legend in the upper-left negative-x clear zone (no footnote — the
    # caption will explain that * = bootstrap CI excludes zero).
    ax.legend(loc="upper left", frameon=False, fontsize=6.5,
              handlelength=1.0, bbox_to_anchor=(0.02, 0.98),
              title="* CI excludes 0", title_fontsize=5.8)
    return _save(fig, out_dir, "fig9_som_per_primitive")
