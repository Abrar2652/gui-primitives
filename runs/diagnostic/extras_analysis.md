# Extras analysis — runs/diagnostic

## (D) Intervention deltas with paired bootstrap 95% CI

Per-model, per-intervention accuracy improvement over baseline,
with item-paired bootstrap CI on the delta (2000 resamples).

| model | intervention | n | baseline | with intervention | Δ (95% CI) | CI excludes 0 |
|---|---|---:|---:|---:|---:|:---:|
| closed_claude_opus | som | 196 | 0.311 | 0.403 | +0.092  [-0.005, +0.189] | — |
| closed_gpt5 | som | 196 | 0.296 | 0.867 | +0.571  [+0.500, +0.643] | ✓ |
| os_atlas_base_7b | som | 994 | 0.101 | 0.521 | +0.421  [+0.382, +0.458] | ✓ |
| qwen2_5_vl_7b | cot | 994 | 0.220 | 0.225 | +0.005  [-0.007, +0.017] | — |
| qwen2_5_vl_7b | som | 994 | 0.220 | 0.571 | +0.351  [+0.313, +0.390] | ✓ |
| qwen2_5_vl_7b | steering | 994 | 0.220 | 0.235 | +0.015  [+0.002, +0.028] | ✓ |

## (B) Per-primitive intervention deltas

Where each intervention helps and where it hurts, per primitive.

### closed_claude_opus — som

| primitive | n | baseline | with intervention | Δ (95% CI) |
|---|---:|---:|---:|---:|
| alignment | 28 | 0.071 | 0.321 | +0.250  [+0.071, +0.429] ✓ |
| containment | 28 | 0.071 | 0.464 | +0.393  [+0.143, +0.607] ✓ |
| list_ordinal | 28 | 0.821 | 0.321 | -0.500  [-0.679, -0.321] ✓ |
| occlusion | 28 | 0.321 | 0.500 | +0.179  [-0.036, +0.393] |
| proximity | 28 | 0.321 | 0.393 | +0.071  [-0.179, +0.321] |
| rel_pos_horizontal | 28 | 0.357 | 0.429 | +0.071  [-0.214, +0.357] |
| rel_pos_vertical | 28 | 0.214 | 0.393 | +0.179  [-0.071, +0.393] |

### closed_gpt5 — som

| primitive | n | baseline | with intervention | Δ (95% CI) |
|---|---:|---:|---:|---:|
| alignment | 28 | 0.036 | 0.821 | +0.786  [+0.643, +0.929] ✓ |
| containment | 28 | 0.071 | 0.821 | +0.750  [+0.536, +0.929] ✓ |
| list_ordinal | 28 | 0.821 | 0.929 | +0.107  [-0.036, +0.286] |
| occlusion | 28 | 0.286 | 0.964 | +0.679  [+0.500, +0.857] ✓ |
| proximity | 28 | 0.214 | 0.857 | +0.643  [+0.464, +0.821] ✓ |
| rel_pos_horizontal | 28 | 0.321 | 0.857 | +0.536  [+0.357, +0.714] ✓ |
| rel_pos_vertical | 28 | 0.321 | 0.821 | +0.500  [+0.321, +0.679] ✓ |

### os_atlas_base_7b — som

| primitive | n | baseline | with intervention | Δ (95% CI) |
|---|---:|---:|---:|---:|
| alignment | 142 | 0.021 | 0.542 | +0.521  [+0.444, +0.606] ✓ |
| containment | 142 | 0.035 | 0.444 | +0.408  [+0.331, +0.507] ✓ |
| list_ordinal | 142 | 0.239 | 0.472 | +0.232  [+0.127, +0.331] ✓ |
| occlusion | 142 | 0.077 | 0.472 | +0.394  [+0.317, +0.479] ✓ |
| proximity | 142 | 0.007 | 0.563 | +0.556  [+0.465, +0.641] ✓ |
| rel_pos_horizontal | 142 | 0.155 | 0.634 | +0.479  [+0.366, +0.577] ✓ |
| rel_pos_vertical | 142 | 0.169 | 0.521 | +0.352  [+0.239, +0.458] ✓ |

### qwen2_5_vl_7b — cot

| primitive | n | baseline | with intervention | Δ (95% CI) |
|---|---:|---:|---:|---:|
| alignment | 142 | 0.042 | 0.035 | -0.007  [-0.042, +0.021] |
| containment | 142 | 0.049 | 0.035 | -0.014  [-0.042, +0.014] |
| list_ordinal | 142 | 0.810 | 0.831 | +0.021  [+0.000, +0.049] |
| occlusion | 142 | 0.077 | 0.106 | +0.028  [+0.007, +0.056] ✓ |
| proximity | 142 | 0.042 | 0.028 | -0.014  [-0.035, +0.000] |
| rel_pos_horizontal | 142 | 0.211 | 0.232 | +0.021  [-0.007, +0.056] |
| rel_pos_vertical | 142 | 0.310 | 0.310 | +0.000  [-0.049, +0.049] |

### qwen2_5_vl_7b — som

| primitive | n | baseline | with intervention | Δ (95% CI) |
|---|---:|---:|---:|---:|
| alignment | 142 | 0.042 | 0.465 | +0.423  [+0.331, +0.500] ✓ |
| containment | 142 | 0.049 | 0.556 | +0.507  [+0.423, +0.585] ✓ |
| list_ordinal | 142 | 0.810 | 0.486 | -0.324  [-0.437, -0.204] ✓ |
| occlusion | 142 | 0.077 | 0.521 | +0.444  [+0.359, +0.521] ✓ |
| proximity | 142 | 0.042 | 0.620 | +0.577  [+0.500, +0.655] ✓ |
| rel_pos_horizontal | 142 | 0.211 | 0.641 | +0.430  [+0.338, +0.528] ✓ |
| rel_pos_vertical | 142 | 0.310 | 0.711 | +0.401  [+0.303, +0.500] ✓ |

### qwen2_5_vl_7b — steering

| primitive | n | baseline | with intervention | Δ (95% CI) |
|---|---:|---:|---:|---:|
| alignment | 142 | 0.042 | 0.021 | -0.021  [-0.042, +0.000] |
| containment | 142 | 0.049 | 0.127 | +0.077  [+0.028, +0.127] ✓ |
| list_ordinal | 142 | 0.810 | 0.831 | +0.021  [+0.000, +0.049] |
| occlusion | 142 | 0.077 | 0.085 | +0.007  [-0.021, +0.042] |
| proximity | 142 | 0.042 | 0.035 | -0.007  [-0.035, +0.014] |
| rel_pos_horizontal | 142 | 0.211 | 0.232 | +0.021  [-0.014, +0.063] |
| rel_pos_vertical | 142 | 0.310 | 0.317 | +0.007  [-0.021, +0.042] |

## (C) Source-stratified model-level competence correlation

Per-model GUI-Primitives accuracy (overall, real-only, synthetic-only)
vs ScreenSpot-Pro accuracy, then Spearman ρ across models for each slice.
This tests whether the headline rho=1.0 is driven by one source.

| model | GUI-Prim (all) | GUI-Prim (real) | GUI-Prim (synth) | SS-Pro |
|---|---:|---:|---:|---:|
| closed_claude_opus | 0.313 | 0.190 | 0.364 | 0.507 |
| closed_claude_sonnet | 0.222 | 0.059 | 0.290 | 0.071 |
| closed_gpt5 | 0.265 | 0.031 | 0.361 | 0.028 |
| gemma3_27b | 0.134 | 0.000 | 0.189 | 0.003 |
| gemma3_27b_ollama | 0.103 | 0.003 | 0.143 | 0.006 |
| internvl3_8b | 0.095 | 0.003 | 0.132 | 0.006 |
| llama32_11b_vision | 0.012 | 0.000 | 0.017 | 0.002 |
| os_atlas_base_7b | 0.101 | 0.000 | 0.142 | 0.154 |
| qwen2_5_vl_7b | 0.220 | 0.028 | 0.300 | 0.261 |
| qwen2_vl_7b | 0.038 | 0.000 | 0.054 | 0.003 |

Spearman ρ between each slice's accuracy and SS-Pro accuracy:

| slice | n models | Spearman ρ (p) | Pearson r (p) |
|---|---:|---:|---:|
| all | 10 | +0.736 (0.0153) | +0.675 (0.0321) |
| ui_vision | 10 | +0.705 (0.0229) | +0.863 (0.00129) |
| synthetic | 10 | +0.760 (0.0108) | +0.601 (0.0662) |

## (S1) Loose-accuracy sensitivity to the tolerance multiplier

Reviewer-asked: justify the 2× target-diagonal tolerance. We sweep the
multiplier k ∈ {0, 1, 2, 3, 5} and report accuracy at each. A natural
choice will produce a smooth, monotone curve; an arbitrary choice
would not.

| model | k=0.0 | k=1.0 | k=2.0 | k=3.0 | k=5.0 |
|---|---:|---:|---:|---:|---:|
| closed_claude_haiku | 0.239 | 0.397 | 0.572 | 0.656 | 0.748 |
| closed_claude_opus | 0.313 | 0.550 | 0.694 | 0.798 | 0.881 |
| closed_claude_sonnet | 0.222 | 0.459 | 0.631 | 0.742 | 0.854 |
| closed_gemini_flash | 0.073 | 0.339 | 0.523 | 0.625 | 0.753 |
| closed_gpt4_1 | 0.096 | 0.405 | 0.546 | 0.650 | 0.767 |
| closed_gpt4o_mini | 0.068 | 0.386 | 0.516 | 0.597 | 0.734 |
| closed_gpt5 | 0.265 | 0.407 | 0.573 | 0.659 | 0.783 |
| gemma3_12b | 0.074 | 0.373 | 0.529 | 0.637 | 0.757 |
| gemma3_27b | 0.134 | 0.333 | 0.508 | 0.593 | 0.729 |
| gemma3_27b_ollama | 0.103 | 0.390 | 0.513 | 0.598 | 0.744 |
| gemma3_4b | 0.022 | 0.273 | 0.493 | 0.613 | 0.733 |
| internvl3_8b | 0.095 | 0.372 | 0.547 | 0.636 | 0.759 |
| llama32_11b_vision | 0.012 | 0.297 | 0.455 | 0.528 | 0.728 |
| minicpm_v_ollama | 0.081 | 0.303 | 0.455 | 0.552 | 0.681 |
| os_atlas_base_7b | 0.101 | 0.324 | 0.560 | 0.665 | 0.797 |
| paligemma2_10b | 0.029 | 0.210 | 0.376 | 0.482 | 0.631 |
| paligemma2_3b | 0.041 | 0.214 | 0.421 | 0.512 | 0.710 |
| qwen2_5_vl_7b | 0.220 | 0.401 | 0.574 | 0.681 | 0.804 |
| qwen2_vl_7b | 0.038 | 0.307 | 0.510 | 0.574 | 0.735 |

(k=0 is strict point-in-box; k=2 is the paper's loose metric.
 k=5 effectively converges to in-the-screenshot.)

## (S2) Per-application × per-primitive predictive analysis

Reviewer-asked: do specific primitives predict failure in specific
apps? For each application, we report SS-Pro accuracy delta =
(items needing primitive p) − (items NOT needing p), averaged
across models. A large negative delta says items in that app needing
primitive p are systematically harder.

| app | rp_horiz | rp_verti | containm | list_ord | alignmen | proximit | occlusio |
|---|---:|---:|---:|---:|---:|---:|---:|
| android | -0.07 | +0.20 | +0.01 | +0.03 | — | — | — |
| autocad | — | — | — | — | — | — | — |
| blender | -0.06 | -0.01 | -0.01 | — | — | — | -0.01 |
| davinci | — | — | — | — | — | — | — |
| eviews | — | — | — | — | — | — | — |
| excel | -0.08 | +0.02 | -0.05 | +0.02 | -0.04 | — | -0.08 |
| fruitloops | — | — | -0.06 | -0.05 | — | — | — |
| illustrator | -0.06 | -0.06 | -0.06 | -0.06 | -0.06 | — | — |
| inventor | -0.05 | — | — | +0.05 | — | — | — |
| linux | — | — | -0.00 | +0.05 | — | — | — |
| macos | — | — | +0.02 | -0.08 | -0.08 | -0.08 | +0.02 |
| matlab | — | -0.05 | -0.05 | +0.05 | — | — | — |
| origin | — | — | +0.05 | +0.15 | — | — | -0.06 |
| photoshop | -0.16 | — | — | -0.16 | — | — | — |
| powerpoint | — | — | -0.05 | — | -0.05 | — | — |
| premiere | -0.01 | -0.08 | +0.06 | -0.12 | — | — | — |
| pycharm | -0.03 | -0.04 | -0.06 | +0.01 | — | — | — |
| quartus | — | — | -0.07 | — | — | — | — |
| solidworks | — | — | -0.04 | -0.04 | — | -0.04 | — |
| stata | — | — | — | -0.04 | — | — | -0.09 |
| unreal | — | — | -0.07 | — | — | — | — |
| vivado | -0.04 | — | +0.01 | -0.14 | — | — | -0.14 |
| vmware | — | — | -0.03 | — | — | — | — |
| vscode | — | — | -0.02 | +0.08 | — | — | — |
| windows | +0.11 | +0.16 | -0.05 | +0.04 | -0.10 | — | +0.11 |
| word | — | — | +0.01 | -0.03 | +0.04 | — | +0.14 |

(blank cells = too few items in that app needed/didn't-need the
 primitive to compute a stable delta; minimum 3 items per side.)
