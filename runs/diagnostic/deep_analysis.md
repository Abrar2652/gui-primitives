# Deep analysis — runs/diagnostic

## 1. Per-application ScreenSpot-Pro accuracy

| application | closed_claude_opus | closed_claude_sonnet | closed_gpt5 | gemma3_27b | gemma3_27b_ollama | internvl3_8b | llama32_11b_vision | os_atlas_base_7b | qwen2_5_vl_7b | qwen2_vl_7b |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| android | 0.31 (n=80) | 0.03 (n=80) | 0.03 (n=80) | 0.00 (n=80) | 0.00 (n=80) | 0.00 (n=80) | 0.00 (n=80) | 0.11 (n=80) | 0.26 (n=80) | 0.00 (n=80) |
| autocad | 0.12 (n=34) | 0.03 (n=34) | 0.00 (n=34) | 0.00 (n=34) | 0.00 (n=34) | 0.06 (n=34) | 0.00 (n=34) | 0.00 (n=34) | 0.03 (n=34) | 0.03 (n=34) |
| blender | 0.68 (n=71) | 0.06 (n=71) | 0.00 (n=71) | 0.00 (n=71) | 0.00 (n=71) | 0.00 (n=71) | 0.00 (n=71) | 0.15 (n=71) | 0.17 (n=71) | 0.00 (n=71) |
| davinci | 0.57 (n=44) | 0.00 (n=44) | 0.00 (n=44) | 0.00 (n=44) | 0.00 (n=44) | 0.00 (n=44) | 0.00 (n=44) | 0.14 (n=44) | 0.18 (n=44) | 0.00 (n=44) |
| eviews | 1.00 (n=50) | 0.06 (n=50) | 0.00 (n=50) | 0.00 (n=50) | 0.00 (n=50) | 0.00 (n=50) | 0.00 (n=50) | 0.50 (n=50) | 0.68 (n=50) | 0.00 (n=50) |
| excel | 0.45 (n=64) | 0.02 (n=64) | 0.02 (n=64) | 0.00 (n=64) | 0.00 (n=64) | 0.00 (n=64) | 0.00 (n=64) | 0.11 (n=64) | 0.19 (n=64) | 0.00 (n=64) |
| fruitloops | 0.39 (n=57) | 0.04 (n=57) | 0.02 (n=57) | 0.00 (n=57) | 0.00 (n=57) | 0.00 (n=57) | 0.00 (n=57) | 0.12 (n=57) | 0.05 (n=57) | 0.00 (n=57) |
| illustrator | 0.29 (n=31) | 0.23 (n=31) | 0.00 (n=31) | 0.00 (n=31) | 0.00 (n=31) | 0.00 (n=31) | 0.00 (n=31) | 0.06 (n=31) | 0.00 (n=31) | 0.00 (n=31) |
| inventor | 0.09 (n=70) | 0.11 (n=70) | 0.09 (n=70) | 0.00 (n=70) | 0.00 (n=70) | 0.04 (n=70) | 0.03 (n=70) | 0.01 (n=70) | 0.07 (n=70) | 0.03 (n=70) |
| linux | 0.60 (n=50) | 0.00 (n=50) | 0.02 (n=50) | 0.00 (n=50) | 0.00 (n=50) | 0.00 (n=50) | 0.00 (n=50) | 0.12 (n=50) | 0.28 (n=50) | 0.00 (n=50) |
| macos | 0.28 (n=65) | 0.00 (n=65) | 0.02 (n=65) | 0.00 (n=65) | 0.00 (n=65) | 0.00 (n=65) | 0.00 (n=65) | 0.12 (n=65) | 0.35 (n=65) | 0.00 (n=65) |
| matlab | 0.82 (n=93) | 0.05 (n=93) | 0.04 (n=93) | 0.03 (n=93) | 0.03 (n=93) | 0.00 (n=93) | 0.01 (n=93) | 0.20 (n=93) | 0.34 (n=93) | 0.00 (n=93) |
| origin | 0.37 (n=62) | 0.02 (n=62) | 0.00 (n=62) | 0.02 (n=62) | 0.02 (n=62) | 0.00 (n=62) | 0.00 (n=62) | 0.10 (n=62) | 0.03 (n=62) | 0.02 (n=62) |
| photoshop | 0.76 (n=51) | 0.24 (n=51) | 0.04 (n=51) | 0.00 (n=51) | 0.02 (n=51) | 0.00 (n=51) | 0.00 (n=51) | 0.22 (n=51) | 0.29 (n=51) | 0.02 (n=51) |
| powerpoint | 0.71 (n=82) | 0.07 (n=82) | 0.01 (n=82) | 0.00 (n=82) | 0.00 (n=82) | 0.01 (n=82) | 0.00 (n=82) | 0.23 (n=82) | 0.41 (n=82) | 0.00 (n=82) |
| premiere | 0.67 (n=52) | 0.04 (n=52) | 0.02 (n=52) | 0.00 (n=52) | 0.00 (n=52) | 0.00 (n=52) | 0.00 (n=52) | 0.17 (n=52) | 0.21 (n=52) | 0.00 (n=52) |
| pycharm | 0.53 (n=78) | 0.19 (n=78) | 0.04 (n=78) | 0.00 (n=78) | 0.00 (n=78) | 0.00 (n=78) | 0.00 (n=78) | 0.10 (n=78) | 0.08 (n=78) | 0.00 (n=78) |
| quartus | 0.49 (n=45) | 0.09 (n=45) | 0.02 (n=45) | 0.02 (n=45) | 0.02 (n=45) | 0.00 (n=45) | 0.00 (n=45) | 0.13 (n=45) | 0.20 (n=45) | 0.00 (n=45) |
| solidworks | 0.10 (n=77) | 0.13 (n=77) | 0.03 (n=77) | 0.00 (n=77) | 0.00 (n=77) | 0.00 (n=77) | 0.00 (n=77) | 0.01 (n=77) | 0.08 (n=77) | 0.00 (n=77) |
| stata | 0.59 (n=49) | 0.02 (n=49) | 0.00 (n=49) | 0.00 (n=49) | 0.00 (n=49) | 0.00 (n=49) | 0.00 (n=49) | 0.04 (n=49) | 0.18 (n=49) | 0.00 (n=49) |
| unreal | 0.80 (n=35) | 0.17 (n=35) | 0.06 (n=35) | 0.00 (n=35) | 0.09 (n=35) | 0.06 (n=35) | 0.00 (n=35) | 0.06 (n=35) | 0.43 (n=35) | 0.00 (n=35) |
| vivado | 0.69 (n=80) | 0.03 (n=80) | 0.04 (n=80) | 0.00 (n=80) | 0.00 (n=80) | 0.00 (n=80) | 0.00 (n=80) | 0.29 (n=80) | 0.33 (n=80) | 0.00 (n=80) |
| vmware | 0.46 (n=41) | 0.00 (n=41) | 0.00 (n=41) | 0.00 (n=41) | 0.00 (n=41) | 0.00 (n=41) | 0.00 (n=41) | 0.22 (n=41) | 0.56 (n=41) | 0.00 (n=41) |
| vscode | 0.65 (n=55) | 0.00 (n=55) | 0.02 (n=55) | 0.00 (n=55) | 0.02 (n=55) | 0.02 (n=55) | 0.00 (n=55) | 0.13 (n=55) | 0.35 (n=55) | 0.00 (n=55) |
| windows | 0.40 (n=81) | 0.20 (n=81) | 0.06 (n=81) | 0.00 (n=81) | 0.00 (n=81) | 0.00 (n=81) | 0.00 (n=81) | 0.09 (n=81) | 0.20 (n=81) | 0.00 (n=81) |
| word | 0.42 (n=84) | 0.06 (n=84) | 0.08 (n=84) | 0.00 (n=84) | 0.00 (n=84) | 0.00 (n=84) | 0.00 (n=84) | 0.38 (n=84) | 0.67 (n=84) | 0.00 (n=84) |

## 2. Cohen's h vs chance level

### closed_claude_haiku

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| alignment | 0.042 | 0.50 | -1.157 | large | below |
| rel_pos_vertical | 0.268 | 0.50 | -0.483 | small | below |
| list_ordinal | 0.824 | 0.20 | +1.348 | large | above |
| rel_pos_horizontal | 0.232 | 0.50 | -0.565 | medium | below |
| occlusion | 0.099 | 0.50 | -0.932 | large | below |
| containment | 0.021 | 0.50 | -1.279 | large | below |
| proximity | 0.190 | 0.50 | -0.668 | medium | below |

### closed_claude_opus

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| alignment | 0.127 | 0.50 | -0.843 | large | below |
| rel_pos_vertical | 0.261 | 0.50 | -0.499 | small | below |
| list_ordinal | 0.831 | 0.20 | +1.367 | large | above |
| rel_pos_horizontal | 0.507 | 0.50 | +0.014 | trivial | above |
| occlusion | 0.127 | 0.50 | -0.843 | large | below |
| containment | 0.077 | 0.50 | -1.007 | large | below |
| proximity | 0.261 | 0.50 | -0.499 | small | below |

### closed_claude_sonnet

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| rel_pos_vertical | 0.169 | 0.50 | -0.723 | medium | below |
| proximity | 0.120 | 0.50 | -0.864 | large | below |
| alignment | 0.063 | 0.50 | -1.062 | large | below |
| occlusion | 0.092 | 0.50 | -0.956 | large | below |
| containment | 0.014 | 0.50 | -1.333 | large | below |
| rel_pos_horizontal | 0.268 | 0.50 | -0.483 | small | below |
| list_ordinal | 0.831 | 0.20 | +1.367 | large | above |

### closed_gemini_flash

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| alignment | 0.042 | 0.50 | -1.157 | large | below |
| rel_pos_vertical | 0.155 | 0.50 | -0.762 | medium | below |
| list_ordinal | 0.000 | 0.20 | -0.927 | large | below |
| rel_pos_horizontal | 0.183 | 0.50 | -0.686 | medium | below |
| occlusion | 0.049 | 0.50 | -1.123 | large | below |
| containment | 0.021 | 0.50 | -1.279 | large | below |
| proximity | 0.063 | 0.50 | -1.062 | large | below |

### closed_gpt4_1

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| alignment | 0.035 | 0.50 | -1.193 | large | below |
| rel_pos_vertical | 0.106 | 0.50 | -0.909 | large | below |
| list_ordinal | 0.063 | 0.20 | -0.418 | small | below |
| rel_pos_horizontal | 0.261 | 0.50 | -0.499 | small | below |
| occlusion | 0.077 | 0.50 | -1.007 | large | below |
| containment | 0.028 | 0.50 | -1.234 | large | below |
| proximity | 0.099 | 0.50 | -0.932 | large | below |

### closed_gpt4o_mini

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| alignment | 0.106 | 0.50 | -0.909 | large | below |
| rel_pos_vertical | 0.113 | 0.50 | -0.886 | large | below |
| list_ordinal | 0.007 | 0.20 | -0.759 | medium | below |
| rel_pos_horizontal | 0.085 | 0.50 | -0.981 | large | below |
| occlusion | 0.077 | 0.50 | -1.007 | large | below |
| containment | 0.042 | 0.50 | -1.157 | large | below |
| proximity | 0.049 | 0.50 | -1.123 | large | below |

### closed_gpt5

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| list_ordinal | 0.817 | 0.20 | +1.330 | large | above |
| rel_pos_vertical | 0.324 | 0.50 | -0.360 | small | below |
| rel_pos_horizontal | 0.282 | 0.50 | -0.452 | small | below |
| occlusion | 0.106 | 0.50 | -0.909 | large | below |
| containment | 0.042 | 0.50 | -1.157 | large | below |
| proximity | 0.197 | 0.50 | -0.651 | medium | below |
| alignment | 0.085 | 0.50 | -0.981 | large | below |

### gemma3_12b

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| alignment | 0.042 | 0.50 | -1.157 | large | below |
| rel_pos_vertical | 0.120 | 0.50 | -0.864 | large | below |
| list_ordinal | 0.303 | 0.20 | +0.238 | small | above |
| rel_pos_horizontal | 0.000 | 0.50 | -1.571 | large | below |
| occlusion | 0.049 | 0.50 | -1.123 | large | below |
| containment | 0.007 | 0.50 | -1.403 | large | below |
| proximity | 0.000 | 0.50 | -1.571 | large | below |

### gemma3_27b

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| alignment | 0.049 | 0.50 | -1.123 | large | below |
| rel_pos_vertical | 0.232 | 0.50 | -0.565 | medium | below |
| list_ordinal | 0.507 | 0.20 | +0.658 | medium | above |
| rel_pos_horizontal | 0.127 | 0.50 | -0.843 | large | below |
| occlusion | 0.007 | 0.50 | -1.403 | large | below |
| containment | 0.014 | 0.50 | -1.333 | large | below |
| proximity | 0.000 | 0.50 | -1.571 | large | below |

### gemma3_27b_ollama

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| rel_pos_vertical | 0.239 | 0.50 | -0.548 | medium | below |
| proximity | 0.007 | 0.50 | -1.403 | large | below |
| alignment | 0.070 | 0.50 | -1.034 | large | below |
| occlusion | 0.049 | 0.50 | -1.123 | large | below |
| containment | 0.049 | 0.50 | -1.123 | large | below |
| rel_pos_horizontal | 0.085 | 0.50 | -0.981 | large | below |
| list_ordinal | 0.218 | 0.20 | +0.045 | trivial | above |

### gemma3_4b

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| rel_pos_vertical | 0.056 | 0.50 | -1.092 | large | below |
| proximity | 0.000 | 0.50 | -1.571 | large | below |
| alignment | 0.007 | 0.50 | -1.403 | large | below |
| occlusion | 0.028 | 0.50 | -1.234 | large | below |
| containment | 0.035 | 0.50 | -1.193 | large | below |
| rel_pos_horizontal | 0.000 | 0.50 | -1.571 | large | below |
| list_ordinal | 0.028 | 0.20 | -0.590 | medium | below |

### internvl3_8b

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| rel_pos_vertical | 0.127 | 0.50 | -0.843 | large | below |
| proximity | 0.042 | 0.50 | -1.157 | large | below |
| alignment | 0.028 | 0.50 | -1.234 | large | below |
| occlusion | 0.021 | 0.50 | -1.279 | large | below |
| containment | 0.070 | 0.50 | -1.034 | large | below |
| rel_pos_horizontal | 0.183 | 0.50 | -0.686 | medium | below |
| list_ordinal | 0.190 | 0.20 | -0.025 | trivial | below |

### llama32_11b_vision

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| rel_pos_vertical | 0.007 | 0.50 | -1.403 | large | below |
| proximity | 0.000 | 0.50 | -1.571 | large | below |
| alignment | 0.042 | 0.50 | -1.157 | large | below |
| occlusion | 0.014 | 0.50 | -1.333 | large | below |
| containment | 0.000 | 0.50 | -1.571 | large | below |
| rel_pos_horizontal | 0.021 | 0.50 | -1.279 | large | below |
| list_ordinal | 0.000 | 0.20 | -0.927 | large | below |

### minicpm_v_ollama

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| rel_pos_vertical | 0.155 | 0.50 | -0.762 | medium | below |
| proximity | 0.014 | 0.50 | -1.333 | large | below |
| alignment | 0.028 | 0.50 | -1.234 | large | below |
| occlusion | 0.070 | 0.50 | -1.034 | large | below |
| containment | 0.049 | 0.50 | -1.123 | large | below |
| rel_pos_horizontal | 0.056 | 0.50 | -1.092 | large | below |
| list_ordinal | 0.197 | 0.20 | -0.007 | trivial | below |

### os_atlas_base_7b

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| alignment | 0.021 | 0.50 | -1.279 | large | below |
| rel_pos_vertical | 0.169 | 0.50 | -0.723 | medium | below |
| list_ordinal | 0.239 | 0.20 | +0.095 | trivial | above |
| rel_pos_horizontal | 0.155 | 0.50 | -0.762 | medium | below |
| occlusion | 0.077 | 0.50 | -1.007 | large | below |
| containment | 0.035 | 0.50 | -1.193 | large | below |
| proximity | 0.007 | 0.50 | -1.403 | large | below |

### paligemma2_10b

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| rel_pos_vertical | 0.042 | 0.50 | -1.157 | large | below |
| proximity | 0.007 | 0.50 | -1.403 | large | below |
| alignment | 0.021 | 0.50 | -1.279 | large | below |
| occlusion | 0.063 | 0.50 | -1.062 | large | below |
| containment | 0.021 | 0.50 | -1.279 | large | below |
| rel_pos_horizontal | 0.049 | 0.50 | -1.123 | large | below |
| list_ordinal | 0.000 | 0.20 | -0.927 | large | below |

### paligemma2_3b

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| rel_pos_vertical | 0.099 | 0.50 | -0.932 | large | below |
| proximity | 0.042 | 0.50 | -1.157 | large | below |
| alignment | 0.021 | 0.50 | -1.279 | large | below |
| occlusion | 0.056 | 0.50 | -1.092 | large | below |
| containment | 0.028 | 0.50 | -1.234 | large | below |
| rel_pos_horizontal | 0.007 | 0.50 | -1.403 | large | below |
| list_ordinal | 0.035 | 0.20 | -0.550 | medium | below |

### qwen2_5_vl_7b

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| alignment | 0.042 | 0.50 | -1.157 | large | below |
| rel_pos_vertical | 0.310 | 0.50 | -0.390 | small | below |
| list_ordinal | 0.810 | 0.20 | +1.312 | large | above |
| rel_pos_horizontal | 0.211 | 0.50 | -0.616 | medium | below |
| occlusion | 0.077 | 0.50 | -1.007 | large | below |
| containment | 0.049 | 0.50 | -1.123 | large | below |
| proximity | 0.042 | 0.50 | -1.157 | large | below |

### qwen2_vl_7b

| primitive | acc | chance | h | interp | direction |
|---|---:|---:|---:|---|---|
| rel_pos_vertical | 0.113 | 0.50 | -0.886 | large | below |
| proximity | 0.014 | 0.50 | -1.333 | large | below |
| alignment | 0.014 | 0.50 | -1.333 | large | below |
| occlusion | 0.021 | 0.50 | -1.279 | large | below |
| containment | 0.000 | 0.50 | -1.571 | large | below |
| rel_pos_horizontal | 0.106 | 0.50 | -0.909 | large | below |
| list_ordinal | 0.000 | 0.20 | -0.927 | large | below |

## 3. Real vs synthetic accuracy stratification

### closed_claude_haiku

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| alignment | 66 | 0.03 | 76 | 0.05 |
| rel_pos_vertical | 48 | 0.02 | 94 | 0.39 |
| list_ordinal | 24 | 0.00 | 118 | 0.99 |
| rel_pos_horizontal | 68 | 0.03 | 74 | 0.42 |
| occlusion |  |  | 142 | 0.10 |
| containment |  |  | 142 | 0.02 |
| proximity | 84 | 0.08 | 58 | 0.34 |

### closed_claude_opus

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| alignment | 66 | 0.15 | 76 | 0.11 |
| rel_pos_vertical | 48 | 0.19 | 94 | 0.30 |
| list_ordinal | 24 | 0.00 | 118 | 1.00 |
| rel_pos_horizontal | 68 | 0.44 | 74 | 0.57 |
| occlusion |  |  | 142 | 0.13 |
| containment |  |  | 142 | 0.08 |
| proximity | 84 | 0.07 | 58 | 0.53 |

### closed_claude_sonnet

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| rel_pos_vertical | 48 | 0.06 | 94 | 0.22 |
| proximity | 84 | 0.06 | 58 | 0.21 |
| alignment | 66 | 0.02 | 76 | 0.11 |
| occlusion |  |  | 142 | 0.09 |
| containment |  |  | 142 | 0.01 |
| rel_pos_horizontal | 68 | 0.12 | 74 | 0.41 |
| list_ordinal | 24 | 0.00 | 118 | 1.00 |

### closed_gemini_flash

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| alignment | 66 | 0.00 | 76 | 0.08 |
| rel_pos_vertical | 48 | 0.00 | 94 | 0.23 |
| list_ordinal | 24 | 0.00 | 118 | 0.00 |
| rel_pos_horizontal | 68 | 0.04 | 74 | 0.31 |
| occlusion |  |  | 142 | 0.05 |
| containment |  |  | 142 | 0.02 |
| proximity | 84 | 0.00 | 58 | 0.16 |

### closed_gpt4_1

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| alignment | 66 | 0.00 | 76 | 0.07 |
| rel_pos_vertical | 48 | 0.00 | 94 | 0.16 |
| list_ordinal | 24 | 0.00 | 118 | 0.08 |
| rel_pos_horizontal | 68 | 0.00 | 74 | 0.50 |
| occlusion |  |  | 142 | 0.08 |
| containment |  |  | 142 | 0.03 |
| proximity | 84 | 0.00 | 58 | 0.24 |

### closed_gpt4o_mini

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| alignment | 66 | 0.00 | 76 | 0.20 |
| rel_pos_vertical | 48 | 0.00 | 94 | 0.17 |
| list_ordinal | 24 | 0.00 | 118 | 0.01 |
| rel_pos_horizontal | 68 | 0.00 | 74 | 0.16 |
| occlusion |  |  | 142 | 0.08 |
| containment |  |  | 142 | 0.04 |
| proximity | 84 | 0.00 | 58 | 0.12 |

### closed_gpt5

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| list_ordinal | 24 | 0.00 | 118 | 0.98 |
| rel_pos_vertical | 48 | 0.08 | 94 | 0.45 |
| rel_pos_horizontal | 68 | 0.04 | 74 | 0.50 |
| occlusion |  |  | 142 | 0.11 |
| containment |  |  | 142 | 0.04 |
| proximity | 84 | 0.02 | 58 | 0.45 |
| alignment | 66 | 0.00 | 76 | 0.16 |

### gemma3_12b

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| alignment | 66 | 0.00 | 76 | 0.08 |
| rel_pos_vertical | 48 | 0.02 | 94 | 0.17 |
| list_ordinal | 24 | 0.00 | 118 | 0.36 |
| rel_pos_horizontal | 68 | 0.00 | 74 | 0.00 |
| occlusion |  |  | 142 | 0.05 |
| containment |  |  | 142 | 0.01 |
| proximity | 84 | 0.00 | 58 | 0.00 |

### gemma3_27b

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| alignment | 66 | 0.00 | 76 | 0.09 |
| rel_pos_vertical | 48 | 0.00 | 94 | 0.35 |
| list_ordinal | 24 | 0.00 | 118 | 0.61 |
| rel_pos_horizontal | 68 | 0.00 | 74 | 0.24 |
| occlusion |  |  | 142 | 0.01 |
| containment |  |  | 142 | 0.01 |
| proximity | 84 | 0.00 | 58 | 0.00 |

### gemma3_27b_ollama

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| rel_pos_vertical | 48 | 0.00 | 94 | 0.36 |
| proximity | 84 | 0.00 | 58 | 0.02 |
| alignment | 66 | 0.00 | 76 | 0.13 |
| occlusion |  |  | 142 | 0.05 |
| containment |  |  | 142 | 0.05 |
| rel_pos_horizontal | 68 | 0.01 | 74 | 0.15 |
| list_ordinal | 24 | 0.00 | 118 | 0.26 |

### gemma3_4b

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| rel_pos_vertical | 48 | 0.02 | 94 | 0.07 |
| proximity | 84 | 0.00 | 58 | 0.00 |
| alignment | 66 | 0.00 | 76 | 0.01 |
| occlusion |  |  | 142 | 0.03 |
| containment |  |  | 142 | 0.04 |
| rel_pos_horizontal | 68 | 0.00 | 74 | 0.00 |
| list_ordinal | 24 | 0.00 | 118 | 0.03 |

### internvl3_8b

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| rel_pos_vertical | 48 | 0.02 | 94 | 0.18 |
| proximity | 84 | 0.00 | 58 | 0.10 |
| alignment | 66 | 0.00 | 76 | 0.05 |
| occlusion |  |  | 142 | 0.02 |
| containment |  |  | 142 | 0.07 |
| rel_pos_horizontal | 68 | 0.00 | 74 | 0.35 |
| list_ordinal | 24 | 0.00 | 118 | 0.23 |

### llama32_11b_vision

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| rel_pos_vertical | 48 | 0.00 | 94 | 0.01 |
| proximity | 84 | 0.00 | 58 | 0.00 |
| alignment | 66 | 0.00 | 76 | 0.08 |
| occlusion |  |  | 142 | 0.01 |
| containment |  |  | 142 | 0.00 |
| rel_pos_horizontal | 68 | 0.00 | 74 | 0.04 |
| list_ordinal | 24 | 0.00 | 118 | 0.00 |

### minicpm_v_ollama

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| rel_pos_vertical | 48 | 0.00 | 94 | 0.23 |
| proximity | 84 | 0.00 | 58 | 0.03 |
| alignment | 66 | 0.00 | 76 | 0.05 |
| occlusion |  |  | 142 | 0.07 |
| containment |  |  | 142 | 0.05 |
| rel_pos_horizontal | 68 | 0.00 | 74 | 0.11 |
| list_ordinal | 24 | 0.04 | 118 | 0.23 |

### os_atlas_base_7b

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| alignment | 66 | 0.00 | 76 | 0.04 |
| rel_pos_vertical | 48 | 0.00 | 94 | 0.26 |
| list_ordinal | 24 | 0.00 | 118 | 0.29 |
| rel_pos_horizontal | 68 | 0.00 | 74 | 0.30 |
| occlusion |  |  | 142 | 0.08 |
| containment |  |  | 142 | 0.04 |
| proximity | 84 | 0.00 | 58 | 0.02 |

### paligemma2_10b

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| rel_pos_vertical | 48 | 0.00 | 94 | 0.06 |
| proximity | 84 | 0.00 | 58 | 0.02 |
| alignment | 66 | 0.02 | 76 | 0.03 |
| occlusion |  |  | 142 | 0.06 |
| containment |  |  | 142 | 0.02 |
| rel_pos_horizontal | 68 | 0.00 | 74 | 0.09 |
| list_ordinal | 24 | 0.00 | 118 | 0.00 |

### paligemma2_3b

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| rel_pos_vertical | 48 | 0.00 | 94 | 0.15 |
| proximity | 84 | 0.01 | 58 | 0.09 |
| alignment | 66 | 0.00 | 76 | 0.04 |
| occlusion |  |  | 142 | 0.06 |
| containment |  |  | 142 | 0.03 |
| rel_pos_horizontal | 68 | 0.01 | 74 | 0.00 |
| list_ordinal | 24 | 0.00 | 118 | 0.04 |

### qwen2_5_vl_7b

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| alignment | 66 | 0.03 | 76 | 0.05 |
| rel_pos_vertical | 48 | 0.04 | 94 | 0.45 |
| list_ordinal | 24 | 0.00 | 118 | 0.97 |
| rel_pos_horizontal | 68 | 0.03 | 74 | 0.38 |
| occlusion |  |  | 142 | 0.08 |
| containment |  |  | 142 | 0.05 |
| proximity | 84 | 0.02 | 58 | 0.07 |

### qwen2_vl_7b

| primitive | ui_vision n | ui_vision acc | synthetic n | synthetic acc |
|---|---:|---:|---:|---:|
| rel_pos_vertical | 48 | 0.00 | 94 | 0.17 |
| proximity | 84 | 0.00 | 58 | 0.03 |
| alignment | 66 | 0.00 | 76 | 0.03 |
| occlusion |  |  | 142 | 0.02 |
| containment |  |  | 142 | 0.00 |
| rel_pos_horizontal | 68 | 0.00 | 74 | 0.20 |
| list_ordinal | 24 | 0.00 | 118 | 0.00 |

## 4. Pair-consistency vs acc² (What's-Up signature)

A `relational_failure_flag` (🚩) fires when pair_consistency < acc²/2 —
meaning failures on minimal pairs *correlate* with the relation word.
Rows marked `(n<5)` had too few complete pairs in this split for the
signature to be meaningful (e.g. closed models on the 196-item core).

### closed_claude_haiku

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| alignment | 71 | 0.042 | 0.000 | 0.002 | -0.002 | 🚩 |
| rel_pos_vertical | 71 | 0.268 | 0.070 | 0.072 | -0.001 |  |
| list_ordinal | 71 | 0.824 | 0.817 | 0.679 | +0.138 |  |
| rel_pos_horizontal | 71 | 0.232 | 0.085 | 0.054 | +0.030 |  |
| occlusion | 71 | 0.099 | 0.014 | 0.010 | +0.004 |  |
| containment | 71 | 0.021 | 0.000 | 0.000 | -0.000 | 🚩 |
| proximity | 71 | 0.190 | 0.042 | 0.036 | +0.006 |  |

### closed_claude_opus

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| alignment | 71 | 0.127 | 0.028 | 0.016 | +0.012 |  |
| rel_pos_vertical | 71 | 0.261 | 0.099 | 0.068 | +0.031 |  |
| list_ordinal | 71 | 0.831 | 0.831 | 0.691 | +0.140 |  |
| rel_pos_horizontal | 71 | 0.507 | 0.239 | 0.257 | -0.018 |  |
| occlusion | 71 | 0.127 | 0.028 | 0.016 | +0.012 |  |
| containment | 71 | 0.077 | 0.014 | 0.006 | +0.008 |  |
| proximity | 71 | 0.261 | 0.099 | 0.068 | +0.031 |  |

### closed_claude_sonnet

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| rel_pos_vertical | 71 | 0.169 | 0.014 | 0.029 | -0.014 | 🚩 |
| proximity | 71 | 0.120 | 0.014 | 0.014 | -0.000 |  |
| alignment | 71 | 0.063 | 0.000 | 0.004 | -0.004 | 🚩 |
| occlusion | 71 | 0.092 | 0.000 | 0.008 | -0.008 | 🚩 |
| containment | 71 | 0.014 | 0.000 | 0.000 | -0.000 | 🚩 |
| rel_pos_horizontal | 71 | 0.268 | 0.085 | 0.072 | +0.013 |  |
| list_ordinal | 71 | 0.831 | 0.831 | 0.691 | +0.140 |  |

### closed_gemini_flash

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| alignment | 71 | 0.042 | 0.000 | 0.002 | -0.002 | 🚩 |
| rel_pos_vertical | 71 | 0.155 | 0.042 | 0.024 | +0.018 |  |
| list_ordinal | 71 | 0.000 | 0.000 | 0.000 | +0.000 |  |
| rel_pos_horizontal | 71 | 0.183 | 0.000 | 0.034 | -0.034 | 🚩 |
| occlusion | 71 | 0.049 | 0.000 | 0.002 | -0.002 | 🚩 |
| containment | 71 | 0.021 | 0.000 | 0.000 | -0.000 | 🚩 |
| proximity | 71 | 0.063 | 0.000 | 0.004 | -0.004 | 🚩 |

### closed_gpt4_1

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| alignment | 71 | 0.035 | 0.000 | 0.001 | -0.001 | 🚩 |
| rel_pos_vertical | 71 | 0.106 | 0.000 | 0.011 | -0.011 | 🚩 |
| list_ordinal | 71 | 0.063 | 0.000 | 0.004 | -0.004 | 🚩 |
| rel_pos_horizontal | 71 | 0.261 | 0.099 | 0.068 | +0.031 |  |
| occlusion | 71 | 0.077 | 0.000 | 0.006 | -0.006 | 🚩 |
| containment | 71 | 0.028 | 0.000 | 0.001 | -0.001 | 🚩 |
| proximity | 71 | 0.099 | 0.000 | 0.010 | -0.010 | 🚩 |

### closed_gpt4o_mini

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| alignment | 71 | 0.106 | 0.028 | 0.011 | +0.017 |  |
| rel_pos_vertical | 71 | 0.113 | 0.000 | 0.013 | -0.013 | 🚩 |
| list_ordinal | 71 | 0.007 | 0.000 | 0.000 | -0.000 | 🚩 |
| rel_pos_horizontal | 71 | 0.085 | 0.028 | 0.007 | +0.021 |  |
| occlusion | 71 | 0.077 | 0.000 | 0.006 | -0.006 | 🚩 |
| containment | 71 | 0.042 | 0.000 | 0.002 | -0.002 | 🚩 |
| proximity | 71 | 0.049 | 0.000 | 0.002 | -0.002 | 🚩 |

### closed_gpt5

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| list_ordinal | 71 | 0.817 | 0.803 | 0.667 | +0.135 |  |
| rel_pos_vertical | 71 | 0.324 | 0.127 | 0.105 | +0.022 |  |
| rel_pos_horizontal | 71 | 0.282 | 0.127 | 0.079 | +0.047 |  |
| occlusion | 71 | 0.106 | 0.000 | 0.011 | -0.011 | 🚩 |
| containment | 71 | 0.042 | 0.014 | 0.002 | +0.012 |  |
| proximity | 71 | 0.197 | 0.000 | 0.039 | -0.039 | 🚩 |
| alignment | 71 | 0.085 | 0.014 | 0.007 | +0.007 |  |

### gemma3_12b

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| alignment | 71 | 0.042 | 0.000 | 0.002 | -0.002 | 🚩 |
| rel_pos_vertical | 71 | 0.120 | 0.028 | 0.014 | +0.014 |  |
| list_ordinal | 71 | 0.303 | 0.028 | 0.092 | -0.064 | 🚩 |
| rel_pos_horizontal | 71 | 0.000 | 0.000 | 0.000 | +0.000 |  |
| occlusion | 71 | 0.049 | 0.000 | 0.002 | -0.002 | 🚩 |
| containment | 71 | 0.007 | 0.000 | 0.000 | -0.000 | 🚩 |
| proximity | 71 | 0.000 | 0.000 | 0.000 | +0.000 |  |

### gemma3_27b

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| alignment | 71 | 0.049 | 0.000 | 0.002 | -0.002 | 🚩 |
| rel_pos_vertical | 71 | 0.232 | 0.056 | 0.054 | +0.002 |  |
| list_ordinal | 71 | 0.507 | 0.268 | 0.257 | +0.011 |  |
| rel_pos_horizontal | 71 | 0.127 | 0.000 | 0.016 | -0.016 | 🚩 |
| occlusion | 71 | 0.007 | 0.000 | 0.000 | -0.000 | 🚩 |
| containment | 71 | 0.014 | 0.000 | 0.000 | -0.000 | 🚩 |
| proximity | 71 | 0.000 | 0.000 | 0.000 | +0.000 |  |

### gemma3_27b_ollama

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| rel_pos_vertical | 71 | 0.239 | 0.099 | 0.057 | +0.041 |  |
| proximity | 71 | 0.007 | 0.000 | 0.000 | -0.000 | 🚩 |
| alignment | 71 | 0.070 | 0.000 | 0.005 | -0.005 | 🚩 |
| occlusion | 71 | 0.049 | 0.000 | 0.002 | -0.002 | 🚩 |
| containment | 71 | 0.049 | 0.000 | 0.002 | -0.002 | 🚩 |
| rel_pos_horizontal | 71 | 0.085 | 0.000 | 0.007 | -0.007 | 🚩 |
| list_ordinal | 71 | 0.218 | 0.070 | 0.048 | +0.023 |  |

### gemma3_4b

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| rel_pos_vertical | 71 | 0.056 | 0.000 | 0.003 | -0.003 | 🚩 |
| proximity | 71 | 0.000 | 0.000 | 0.000 | +0.000 |  |
| alignment | 71 | 0.007 | 0.000 | 0.000 | -0.000 | 🚩 |
| occlusion | 71 | 0.028 | 0.000 | 0.001 | -0.001 | 🚩 |
| containment | 71 | 0.035 | 0.000 | 0.001 | -0.001 | 🚩 |
| rel_pos_horizontal | 71 | 0.000 | 0.000 | 0.000 | +0.000 |  |
| list_ordinal | 71 | 0.028 | 0.000 | 0.001 | -0.001 | 🚩 |

### internvl3_8b

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| rel_pos_vertical | 71 | 0.127 | 0.000 | 0.016 | -0.016 | 🚩 |
| proximity | 71 | 0.042 | 0.000 | 0.002 | -0.002 | 🚩 |
| alignment | 71 | 0.028 | 0.000 | 0.001 | -0.001 | 🚩 |
| occlusion | 71 | 0.021 | 0.000 | 0.000 | -0.000 | 🚩 |
| containment | 71 | 0.070 | 0.014 | 0.005 | +0.009 |  |
| rel_pos_horizontal | 71 | 0.183 | 0.000 | 0.034 | -0.034 | 🚩 |
| list_ordinal | 71 | 0.190 | 0.000 | 0.036 | -0.036 | 🚩 |

### llama32_11b_vision

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| rel_pos_vertical | 71 | 0.007 | 0.000 | 0.000 | -0.000 | 🚩 |
| proximity | 71 | 0.000 | 0.000 | 0.000 | +0.000 |  |
| alignment | 71 | 0.042 | 0.000 | 0.002 | -0.002 | 🚩 |
| occlusion | 71 | 0.014 | 0.000 | 0.000 | -0.000 | 🚩 |
| containment | 71 | 0.000 | 0.000 | 0.000 | +0.000 |  |
| rel_pos_horizontal | 71 | 0.021 | 0.000 | 0.000 | -0.000 | 🚩 |
| list_ordinal | 71 | 0.000 | 0.000 | 0.000 | +0.000 |  |

### minicpm_v_ollama

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| rel_pos_vertical | 71 | 0.155 | 0.042 | 0.024 | +0.018 |  |
| proximity | 71 | 0.014 | 0.000 | 0.000 | -0.000 | 🚩 |
| alignment | 71 | 0.028 | 0.000 | 0.001 | -0.001 | 🚩 |
| occlusion | 71 | 0.070 | 0.000 | 0.005 | -0.005 | 🚩 |
| containment | 71 | 0.049 | 0.000 | 0.002 | -0.002 | 🚩 |
| rel_pos_horizontal | 71 | 0.056 | 0.000 | 0.003 | -0.003 | 🚩 |
| list_ordinal | 71 | 0.197 | 0.042 | 0.039 | +0.003 |  |

### os_atlas_base_7b

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| alignment | 71 | 0.021 | 0.000 | 0.000 | -0.000 | 🚩 |
| rel_pos_vertical | 71 | 0.169 | 0.000 | 0.029 | -0.029 | 🚩 |
| list_ordinal | 71 | 0.239 | 0.056 | 0.057 | -0.001 |  |
| rel_pos_horizontal | 71 | 0.155 | 0.014 | 0.024 | -0.010 |  |
| occlusion | 71 | 0.077 | 0.000 | 0.006 | -0.006 | 🚩 |
| containment | 71 | 0.035 | 0.000 | 0.001 | -0.001 | 🚩 |
| proximity | 71 | 0.007 | 0.000 | 0.000 | -0.000 | 🚩 |

### paligemma2_10b

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| rel_pos_vertical | 71 | 0.042 | 0.000 | 0.002 | -0.002 | 🚩 |
| proximity | 71 | 0.007 | 0.000 | 0.000 | -0.000 | 🚩 |
| alignment | 71 | 0.021 | 0.000 | 0.000 | -0.000 | 🚩 |
| occlusion | 71 | 0.063 | 0.000 | 0.004 | -0.004 | 🚩 |
| containment | 71 | 0.021 | 0.000 | 0.000 | -0.000 | 🚩 |
| rel_pos_horizontal | 71 | 0.049 | 0.000 | 0.002 | -0.002 | 🚩 |
| list_ordinal | 71 | 0.000 | 0.000 | 0.000 | +0.000 |  |

### paligemma2_3b

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| rel_pos_vertical | 71 | 0.099 | 0.000 | 0.010 | -0.010 | 🚩 |
| proximity | 71 | 0.042 | 0.000 | 0.002 | -0.002 | 🚩 |
| alignment | 71 | 0.021 | 0.000 | 0.000 | -0.000 | 🚩 |
| occlusion | 71 | 0.056 | 0.000 | 0.003 | -0.003 | 🚩 |
| containment | 71 | 0.028 | 0.000 | 0.001 | -0.001 | 🚩 |
| rel_pos_horizontal | 71 | 0.007 | 0.000 | 0.000 | -0.000 | 🚩 |
| list_ordinal | 71 | 0.035 | 0.000 | 0.001 | -0.001 | 🚩 |

### qwen2_5_vl_7b

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| alignment | 71 | 0.042 | 0.000 | 0.002 | -0.002 | 🚩 |
| rel_pos_vertical | 71 | 0.310 | 0.141 | 0.096 | +0.045 |  |
| list_ordinal | 71 | 0.810 | 0.789 | 0.656 | +0.133 |  |
| rel_pos_horizontal | 71 | 0.211 | 0.085 | 0.045 | +0.040 |  |
| occlusion | 71 | 0.077 | 0.000 | 0.006 | -0.006 | 🚩 |
| containment | 71 | 0.049 | 0.014 | 0.002 | +0.012 |  |
| proximity | 71 | 0.042 | 0.000 | 0.002 | -0.002 | 🚩 |

### qwen2_vl_7b

| primitive | n_pairs | acc | pair_cons | acc² | delta | flag |
|---|---:|---:|---:|---:|---:|---|
| rel_pos_vertical | 71 | 0.113 | 0.014 | 0.013 | +0.001 |  |
| proximity | 71 | 0.014 | 0.000 | 0.000 | -0.000 | 🚩 |
| alignment | 71 | 0.014 | 0.000 | 0.000 | -0.000 | 🚩 |
| occlusion | 71 | 0.021 | 0.000 | 0.000 | -0.000 | 🚩 |
| containment | 71 | 0.000 | 0.000 | 0.000 | +0.000 |  |
| rel_pos_horizontal | 71 | 0.106 | 0.000 | 0.011 | -0.011 | 🚩 |
| list_ordinal | 71 | 0.000 | 0.000 | 0.000 | +0.000 |  |

## 5. Cost report

| model | total GPU-hours | $ |
|---|---:|---:|
| _dropped_models | 0.00 | 0.00 |
| closed_claude_haiku | 0.48 | 1.32 |
| closed_claude_opus | 3.22 | 0.00 |
| closed_claude_sonnet | 1.45 | 0.00 |
| closed_gemini_flash | 0.32 | 0.16 |
| closed_gpt4_1 | 0.43 | 0.00 |
| closed_gpt4o_mini | 1.20 | 0.24 |
| closed_gpt5 | 28.86 | 0.00 |
| figs | 0.00 | 0.00 |
| gemma3_12b | 0.35 | 0.00 |
| gemma3_27b | 12.15 | 0.00 |
| gemma3_27b_ollama | 1.44 | 0.00 |
| gemma3_4b | 0.25 | 0.00 |
| internvl3_8b | 1.29 | 0.00 |
| llama32_11b_vision | 3.20 | 0.00 |
| minicpm_v_ollama | 1.13 | 0.00 |
| os_atlas_base_7b | 3.51 | 0.00 |
| paligemma2_10b | 0.60 | 0.00 |
| paligemma2_3b | 0.25 | 0.00 |
| qwen2_5_vl_7b | 5.39 | 0.00 |
| qwen2_vl_7b | 3.65 | 0.00 |

## 5b. Model-level competence correlation

Per-model: mean GUI-Primitives accuracy vs ScreenSpot-Pro accuracy. Robust complement to the item-level regression.

| model | GUI-Primitives acc | ScreenSpot-Pro acc |
|---|---:|---:|
| closed_claude_haiku | 0.239 | — |
| closed_claude_opus | 0.313 | 0.507 |
| closed_claude_sonnet | 0.222 | 0.071 |
| closed_gemini_flash | 0.073 | — |
| closed_gpt4_1 | 0.096 | — |
| closed_gpt4o_mini | 0.068 | — |
| closed_gpt5 | 0.265 | 0.028 |
| gemma3_12b | 0.074 | — |
| gemma3_27b | 0.134 | 0.003 |
| gemma3_27b_ollama | 0.103 | 0.006 |
| gemma3_4b | 0.022 | — |
| internvl3_8b | 0.095 | 0.006 |
| llama32_11b_vision | 0.012 | 0.002 |
| minicpm_v_ollama | 0.081 | — |
| os_atlas_base_7b | 0.101 | 0.154 |
| paligemma2_10b | 0.029 | — |
| paligemma2_3b | 0.041 | — |
| qwen2_5_vl_7b | 0.220 | 0.261 |
| qwen2_vl_7b | 0.038 | 0.003 |

**Spearman rho=+0.736 (p=0.0153), Pearson r=+0.675 (p=0.0321), n=10**

## 6. Qualitative failure examples (3 per primitive per model)

### closed_claude_haiku

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [231.0, 57.0]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [145.0, 115.0]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [222.85714285714286, 88.16326530612245]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [222.85714285714286, 57.55102040816327]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=378  src=ui_vision  image=193bf4a40a8cc7c2fb66fd0d571412fe.png
  - inst 0: `Select the item directly above 'plastic tool'.`
  - inst 1: `Click the element below the plastic tool.`
  - pred 0: [16.64, 559.36]  target 0: [3.4, 766.5, 32.2, 791.2]
  - pred 1: [15.918367346938776, 562.0408163265306]  target 1: [3.4, 823.1, 34.6, 846.3]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [1835.52, 85.76]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [1780.48, 85.76]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [660.7413333333334, 301.6693333333333]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [660.7413333333334, 421.36]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=259  src=ui_vision  image=9ddc289297f51dfb16c5a0abbd19c9aa.png
  - inst 0: `Select the button nearest to 'edit contents of frame'.`
  - inst 1: `Click the icon farthest from the edit contents of frame.`
  - pred 0: [726.8799999999999, 526.4]  target 0: [861.6, 52.2, 884.7, 76.1]
  - pred 1: [870.2399999999999, 418.87999999999994]  target 1: [55.2, 85.0, 1655.4, 111.9]

**alignment** (3 examples):

- pair_id=217  src=synthetic  image=ui_0152.png
  - inst 0: `Select the control aligned in the same column as 'Paste'.`
  - inst 1: `Select the control aligned in the same row as 'Paste'.`
  - pred 0: [79.0, 38.0]  target 0: [40, 110, 304, 162]
  - pred 1: [203.0, 37.0]  target 1: [396, 18, 506, 58]
- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [168.9795918367347, 12.244897959183675]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [170.24, 23.04]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [1355.52, 328.96]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [1395.2, 328.96]  target 1: [1340.9, 316.7, 1376.9, 342.9]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [615.0, 463.0]  target 0: [712, 452, 862, 602]
  - pred 1: [615.0, 528.0]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [451.0, 37.0]  target 0: [878, 286, 1028, 436]
  - pred 1: [451.0, 37.0]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [825.0, 362.0]  target 0: [712, 120, 862, 270]
  - pred 1: [729.0, 298.0]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [172.0, 430.0]  target 0: [712, 120, 862, 270]
  - pred 1: [172.0, 430.0]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: None  target 0: [396, 18, 506, 58]
  - pred 1: None  target 1: [40, 296, 304, 348]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: None  target 0: [40, 234, 304, 286]
  - pred 1: None  target 1: [749, 394, 1009, 544]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: [1232.64, 756.48]  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [1314.56, 756.48]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [452.0, 599.0]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [929.0, 599.0]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=35  src=ui_vision  image=720435a916fe1ddc2ee7fb3cfc00cd47.png
  - inst 0: `Select the control to the right of 'Left arrow'.`
  - inst 1: `Click the element to the left of the Left arrow.`
  - pred 0: [261.12, 93.44]  target 0: [511.2, 177.4, 544.8, 208.3]
  - pred 1: [476.16, 188.16]  target 1: [446.4, 179.0, 472.8, 209.8]

**list_ordinal** (3 examples):

- pair_id=389  src=ui_vision  image=c0ec43d8febbbcc338adc784beb85cc8.png
  - inst 0: `Select the second entry of the menu.`
  - inst 1: `Click the first item in the list.`
  - pred 0: [1264.64, 142.08]  target 0: [1886.4, 175.9, 1920.0, 200.6]
  - pred 1: [302.08, 609.28]  target 1: [1845.6, 174.4, 1881.6, 199.1]
- pair_id=409  src=ui_vision  image=f6a16dc903a62ce7ea4446f2e8fbc095.png
  - inst 0: `Click the first item in the list.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [90.0, 41.0]  target 0: [191.2, 92.8, 232.2, 113.5]
  - pred 1: [71.0, 41.0]  target 1: [225.4, 120.7, 256.1, 142.3]
- pair_id=384  src=ui_vision  image=96364f0a524df3d5d92ed492a8f1521b.png
  - inst 0: `Select the second entry of the menu.`
  - inst 1: `Select the first entry of the menu.`
  - pred 0: [374.0, 200.0]  target 0: [476.4, 114.9, 500.3, 134.4]
  - pred 1: [328.0, 123.0]  target 1: [432.0, 115.9, 471.3, 133.3]

### closed_claude_opus

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [25.6, 89.60000000000001]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [1839.3600000000001, 89.60000000000001]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [671.7333333333333, 273.57866666666666]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [1094.3146666666667, 310.2186666666667]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=259  src=ui_vision  image=9ddc289297f51dfb16c5a0abbd19c9aa.png
  - inst 0: `Select the button nearest to 'edit contents of frame'.`
  - inst 1: `Click the icon farthest from the edit contents of frame.`
  - pred 0: [841.1199999999999, 62.71999999999999]  target 0: [861.6, 52.2, 884.7, 76.1]
  - pred 1: [1016.9599999999999, 62.71999999999999]  target 1: [55.2, 85.0, 1655.4, 111.9]

**alignment** (3 examples):

- pair_id=217  src=synthetic  image=ui_0152.png
  - inst 0: `Select the control aligned in the same column as 'Paste'.`
  - inst 1: `Select the control aligned in the same row as 'Paste'.`
  - pred 0: [79.0, 39.0]  target 0: [40, 110, 304, 162]
  - pred 1: [204.0, 39.0]  target 1: [396, 18, 506, 58]
- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [182.44897959183675, 23.26530612244898]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [168.96, 17.92]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [1314.56, 330.24]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [1317.1200000000001, 330.24]  target 1: [1340.9, 316.7, 1376.9, 342.9]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [622.0, 528.0]  target 0: [712, 452, 862, 602]
  - pred 1: [621.0, 528.0]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [451.0, 39.0]  target 0: [878, 286, 1028, 436]
  - pred 1: [451.0, 39.0]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [787.0, 361.0]  target 0: [712, 120, 862, 270]
  - pred 1: [787.0, 360.0]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [172.0, 425.0]  target 0: [712, 120, 862, 270]
  - pred 1: [172.0, 432.0]  target 1: [40, 234, 304, 286]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [172.0, 322.0]  target 0: [40, 234, 304, 286]
  - pred 1: [327.0, 39.0]  target 1: [749, 394, 1009, 544]
- pair_id=457  src=synthetic  image=ui_0185.png
  - inst 0: `Select the 'Sidebar' control located inside the dialog.`
  - inst 1: `Select the 'Sidebar' control located outside the dialog.`
  - pred 0: [173.0, 437.0]  target 0: [40, 296, 304, 348]
  - pred 1: [172.0, 437.0]  target 1: [712, 452, 862, 602]

**rel_pos_vertical** (3 examples):

- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [154.28571428571428, 112.6530612244898]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [153.06122448979593, 75.91836734693878]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=185  src=synthetic  image=ui_0151.png
  - inst 0: `Select the item directly above 'Item 1'.`
  - inst 1: `Click the element below the Item 1.`
  - pred 0: [172.0, 98.0]  target 0: [24, 18, 134, 58]
  - pred 1: [172.0, 198.0]  target 1: [40, 234, 304, 286]
- pair_id=378  src=ui_vision  image=193bf4a40a8cc7c2fb66fd0d571412fe.png
  - inst 0: `Select the item directly above 'plastic tool'.`
  - inst 1: `Click the element below the plastic tool.`
  - pred 0: [17.92, 751.36]  target 0: [3.4, 766.5, 32.2, 791.2]
  - pred 1: [22.040816326530614, 891.4285714285714]  target 1: [3.4, 823.1, 34.6, 846.3]

**list_ordinal** (3 examples):

- pair_id=389  src=ui_vision  image=c0ec43d8febbbcc338adc784beb85cc8.png
  - inst 0: `Select the second entry of the menu.`
  - inst 1: `Click the first item in the list.`
  - pred 0: [1427.2, 189.44]  target 0: [1886.4, 175.9, 1920.0, 200.6]
  - pred 1: [312.32, 624.64]  target 1: [1845.6, 174.4, 1881.6, 199.1]
- pair_id=409  src=ui_vision  image=f6a16dc903a62ce7ea4446f2e8fbc095.png
  - inst 0: `Click the first item in the list.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [577.0, 117.0]  target 0: [191.2, 92.8, 232.2, 113.5]
  - pred 1: [1217.0, 365.0]  target 1: [225.4, 120.7, 256.1, 142.3]
- pair_id=384  src=ui_vision  image=96364f0a524df3d5d92ed492a8f1521b.png
  - inst 0: `Select the second entry of the menu.`
  - inst 1: `Select the first entry of the menu.`
  - pred 0: [531.0, 224.0]  target 0: [476.4, 114.9, 500.3, 134.4]
  - pred 1: [529.0, 203.0]  target 1: [432.0, 115.9, 471.3, 133.3]

**rel_pos_horizontal** (3 examples):

- pair_id=2  src=synthetic  image=ui_0139.png
  - inst 0: `Click the element to the left of the Close.`
  - inst 1: `Click the element to the right of the Close.`
  - pred 0: [575.0, 38.0]  target 0: [24, 18, 134, 58]
  - pred 1: [327.0, 39.0]  target 1: [644, 18, 754, 58]
- pair_id=227  src=ui_vision  image=0c69dea5692893df064678029f62c9ff.png
  - inst 0: `Select the control to the right of 'centre justify'.`
  - inst 1: `Select the control to the left of 'centre justify'.`
  - pred 0: [400.40816326530614, 151.83673469387756]  target 0: [313.8, 112.6, 335.4, 132.8]
  - pred 1: [296.96, 121.60000000000001]  target 1: [262.3, 112.6, 284.9, 133.4]
- pair_id=339  src=ui_vision  image=d0a7bcf3558ed4fe15f27b18e18e465d.png
  - inst 0: `Select the control to the left of 'selected vector features'.`
  - inst 1: `Click the element to the right of the selected vector features.`
  - pred 0: [43.52, 559.36]  target 0: [368.6, 197.0, 416.6, 229.4]
  - pred 1: [227.84, 344.32]  target 1: [461.5, 197.0, 514.3, 224.8]

### closed_claude_sonnet

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [1150.0, 117.0]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [1176.0, 117.0]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [225.3061224489796, 58.775510204081634]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [193.46938775510205, 58.775510204081634]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=185  src=synthetic  image=ui_0151.png
  - inst 0: `Select the item directly above 'Item 1'.`
  - inst 1: `Click the element below the Item 1.`
  - pred 0: None  target 0: [24, 18, 134, 58]
  - pred 1: [171.0, 197.0]  target 1: [40, 234, 304, 286]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [1760.8163265306123, 82.04081632653062]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [1709.387755102041, 82.04081632653062]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [632.0867346938775, 358.68877551020404]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [1060.8775510204082, 287.41836734693874]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=31  src=synthetic  image=ui_0207.png
  - inst 0: `Click the icon nearest to the Zoom.`
  - inst 1: `Click the icon farthest from the Zoom.`
  - pred 0: [79.0, 38.0]  target 0: [148, 18, 258, 58]
  - pred 1: [952.0, 525.0]  target 1: [644, 18, 754, 58]

**alignment** (3 examples):

- pair_id=217  src=synthetic  image=ui_0152.png
  - inst 0: `Select the control aligned in the same column as 'Paste'.`
  - inst 1: `Select the control aligned in the same row as 'Paste'.`
  - pred 0: [456.0, 360.0]  target 0: [40, 110, 304, 162]
  - pred 1: [575.0, 38.0]  target 1: [396, 18, 506, 58]
- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [168.9795918367347, 17.142857142857142]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [145.71428571428572, 17.142857142857142]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [1231.8367346938776, 319.59183673469386]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [1323.6734693877552, 281.6326530612245]  target 1: [1340.9, 316.7, 1376.9, 342.9]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [622.0, 525.0]  target 0: [712, 452, 862, 602]
  - pred 1: [622.0, 525.0]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [452.0, 38.0]  target 0: [878, 286, 1028, 436]
  - pred 1: [452.0, 38.0]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [787.0, 359.0]  target 0: [712, 120, 862, 270]
  - pred 1: [787.0, 358.0]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [172.0, 428.0]  target 0: [712, 120, 862, 270]
  - pred 1: [172.0, 430.0]  target 1: [40, 234, 304, 286]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [172.0, 383.0]  target 0: [40, 234, 304, 286]
  - pred 1: [172.0, 383.0]  target 1: [749, 394, 1009, 544]
- pair_id=457  src=synthetic  image=ui_0185.png
  - inst 0: `Select the 'Sidebar' control located inside the dialog.`
  - inst 1: `Select the 'Sidebar' control located outside the dialog.`
  - pred 0: [172.0, 430.0]  target 0: [40, 296, 304, 348]
  - pred 1: [172.0, 430.0]  target 1: [712, 452, 862, 602]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: [588.9795918367347, 724.8979591836735]  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [641.6326530612245, 731.0204081632653]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=291  src=ui_vision  image=7a2089c29b5a44fd0f64566b4da8748f.png
  - inst 0: `Click the element to the left of the calligraphic line.`
  - inst 1: `Select the control to the right of 'calligraphic line'.`
  - pred 0: [639.6428571428571, 60.0]  target 0: [703.7, 59.7, 728.9, 76.1]
  - pred 1: [691.0714285714286, 60.0]  target 1: [762.5, 58.2, 785.6, 77.6]
- pair_id=213  src=synthetic  image=ui_0152.png
  - inst 0: `Click the element to the left of the Copy.`
  - inst 1: `Click the element to the right of the Copy.`
  - pred 0: [456.0, 193.0]  target 0: [24, 18, 134, 58]
  - pred 1: [327.0, 38.0]  target 1: [520, 18, 630, 58]

**list_ordinal** (3 examples):

- pair_id=389  src=ui_vision  image=c0ec43d8febbbcc338adc784beb85cc8.png
  - inst 0: `Select the second entry of the menu.`
  - inst 1: `Click the first item in the list.`
  - pred 0: [1327.3469387755101, 175.10204081632654]  target 0: [1886.4, 175.9, 1920.0, 200.6]
  - pred 1: [1121.6326530612246, 857.1428571428571]  target 1: [1845.6, 174.4, 1881.6, 199.1]
- pair_id=409  src=ui_vision  image=f6a16dc903a62ce7ea4446f2e8fbc095.png
  - inst 0: `Click the first item in the list.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [574.0, 122.0]  target 0: [191.2, 92.8, 232.2, 113.5]
  - pred 1: [675.0, 122.0]  target 1: [225.4, 120.7, 256.1, 142.3]
- pair_id=384  src=ui_vision  image=96364f0a524df3d5d92ed492a8f1521b.png
  - inst 0: `Select the second entry of the menu.`
  - inst 1: `Select the first entry of the menu.`
  - pred 0: [51.0, 34.0]  target 0: [476.4, 114.9, 500.3, 134.4]
  - pred 1: [19.0, 34.0]  target 1: [432.0, 115.9, 471.3, 133.3]

### closed_gemini_flash

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [455.0, 157.0]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [916.0, 196.0]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [65.0, 58.0]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [65.0, 58.0]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=378  src=ui_vision  image=193bf4a40a8cc7c2fb66fd0d571412fe.png
  - inst 0: `Select the item directly above 'plastic tool'.`
  - inst 1: `Click the element below the plastic tool.`
  - pred 0: [9.0, 335.0]  target 0: [3.4, 766.5, 32.2, 791.2]
  - pred 1: [10.0, 695.0]  target 1: [3.4, 823.1, 34.6, 846.3]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [14.0, 42.0]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [956.0, 82.0]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [14.0, 60.0]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [368.0, 375.0]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=259  src=ui_vision  image=9ddc289297f51dfb16c5a0abbd19c9aa.png
  - inst 0: `Select the button nearest to 'edit contents of frame'.`
  - inst 1: `Click the icon farthest from the edit contents of frame.`
  - pred 0: [212.0, 63.0]  target 0: [861.6, 52.2, 884.7, 76.1]
  - pred 1: [10.0, 25.0]  target 1: [55.2, 85.0, 1655.4, 111.9]

**alignment** (3 examples):

- pair_id=217  src=synthetic  image=ui_0152.png
  - inst 0: `Select the control aligned in the same column as 'Paste'.`
  - inst 1: `Select the control aligned in the same row as 'Paste'.`
  - pred 0: [355.0, 244.0]  target 0: [40, 110, 304, 162]
  - pred 1: [159.0, 49.0]  target 1: [396, 18, 506, 58]
- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [675.0, 737.0]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [676.0, 737.0]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [663.0, 323.0]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [663.0, 277.0]  target 1: [1340.9, 316.7, 1376.9, 342.9]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [485.0, 659.0]  target 0: [712, 452, 862, 602]
  - pred 1: [485.0, 658.0]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [352.0, 48.0]  target 0: [878, 286, 1028, 436]
  - pred 1: [352.0, 48.0]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [615.0, 451.0]  target 0: [712, 120, 862, 270]
  - pred 1: [616.0, 451.0]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [134.0, 538.0]  target 0: [712, 120, 862, 270]
  - pred 1: [134.0, 538.0]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: [61.0, 48.0]  target 0: [396, 18, 506, 58]
  - pred 1: [134.0, 170.0]  target 1: [40, 296, 304, 348]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [134.0, 538.0]  target 0: [40, 234, 304, 286]
  - pred 1: [449.0, 48.0]  target 1: [749, 394, 1009, 544]

**list_ordinal** (3 examples):

- pair_id=392  src=synthetic  image=ui_0085.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Select the second entry of the menu.`
  - pred 0: [134.0, 170.0]  target 0: [40, 110, 304, 162]
  - pred 1: [134.0, 248.0]  target 1: [40, 172, 304, 224]
- pair_id=11  src=synthetic  image=ui_0070.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [134.0, 170.0]  target 0: [40, 110, 304, 162]
  - pred 1: [134.0, 248.0]  target 1: [40, 172, 304, 224]
- pair_id=428  src=synthetic  image=ui_0044.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [134.0, 170.0]  target 0: [40, 110, 304, 162]
  - pred 1: [134.0, 247.0]  target 1: [40, 172, 304, 224]

**rel_pos_horizontal** (3 examples):

- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [128.0, 168.0]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [131.0, 168.0]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=35  src=ui_vision  image=720435a916fe1ddc2ee7fb3cfc00cd47.png
  - inst 0: `Select the control to the right of 'Left arrow'.`
  - inst 1: `Click the element to the left of the Left arrow.`
  - pred 0: [242.0, 180.0]  target 0: [511.2, 177.4, 544.8, 208.3]
  - pred 1: [207.0, 180.0]  target 1: [446.4, 179.0, 472.8, 209.8]
- pair_id=321  src=ui_vision  image=8c29c18fa5c6871b1bb29f52bf41dc20.png
  - inst 0: `Click the element to the left of the Open Project.`
  - inst 1: `Select the control to the right of 'Open Project'.`
  - pred 0: [18.0, 63.0]  target 0: [57.3, 45.2, 98.1, 83.1]
  - pred 1: [64.0, 60.0]  target 1: [141.3, 45.2, 194.1, 84.5]

### closed_gpt4_1

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [1012.0, 120.0]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [1012.0, 120.0]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [62.0, 52.0]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [613.0, 527.0]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=185  src=synthetic  image=ui_0151.png
  - inst 0: `Select the item directly above 'Item 1'.`
  - inst 1: `Click the element below the Item 1.`
  - pred 0: [164.0, 98.0]  target 0: [24, 18, 134, 58]
  - pred 1: [164.0, 148.0]  target 1: [40, 234, 304, 286]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [1302.0, 61.0]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [1292.0, 61.0]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [900.0, 82.0]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [116.0, 62.0]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=31  src=synthetic  image=ui_0207.png
  - inst 0: `Click the icon nearest to the Zoom.`
  - inst 1: `Click the icon farthest from the Zoom.`
  - pred 0: [128.0, 38.0]  target 0: [148, 18, 258, 58]
  - pred 1: [1052.0, 540.0]  target 1: [644, 18, 754, 58]

**alignment** (3 examples):

- pair_id=217  src=synthetic  image=ui_0152.png
  - inst 0: `Select the control aligned in the same column as 'Paste'.`
  - inst 1: `Select the control aligned in the same row as 'Paste'.`
  - pred 0: [86.0, 40.0]  target 0: [40, 110, 304, 162]
  - pred 1: [156.0, 38.0]  target 1: [396, 18, 506, 58]
- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [1012.0, 573.0]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [1092.0, 613.0]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [1022.0, 210.0]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [1092.0, 246.0]  target 1: [1340.9, 316.7, 1376.9, 342.9]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [522.0, 538.0]  target 0: [712, 452, 862, 602]
  - pred 1: [507.0, 561.0]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [782.0, 357.0]  target 0: [712, 120, 862, 270]
  - pred 1: [782.0, 370.0]  target 1: [546, 452, 696, 602]
- pair_id=180  src=synthetic  image=ui_0123.png
  - inst 0: `Click the Close control that is partly hidden.`
  - inst 1: `Click the Close control that is fully visible.`
  - pred 0: [950.0, 441.0]  target 0: [712, 452, 862, 602]
  - pred 1: [304.0, 29.0]  target 1: [380, 120, 530, 270]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [164.0, 547.0]  target 0: [712, 120, 862, 270]
  - pred 1: [164.0, 553.0]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: [48.0, 38.0]  target 0: [396, 18, 506, 58]
  - pred 1: [166.0, 104.0]  target 1: [40, 296, 304, 348]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [140.0, 146.0]  target 0: [40, 234, 304, 286]
  - pred 1: [61.0, 38.0]  target 1: [749, 394, 1009, 544]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: [1042.0, 117.0]  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [613.0, 227.0]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [1012.0, 133.0]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [624.0, 153.0]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=35  src=ui_vision  image=720435a916fe1ddc2ee7fb3cfc00cd47.png
  - inst 0: `Select the control to the right of 'Left arrow'.`
  - inst 1: `Click the element to the left of the Left arrow.`
  - pred 0: [355.0, 128.0]  target 0: [511.2, 177.4, 544.8, 208.3]
  - pred 1: [222.0, 120.0]  target 1: [446.4, 179.0, 472.8, 209.8]

**list_ordinal** (3 examples):

- pair_id=392  src=synthetic  image=ui_0085.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Select the second entry of the menu.`
  - pred 0: [164.0, 102.0]  target 0: [40, 110, 304, 162]
  - pred 1: [164.0, 153.0]  target 1: [40, 172, 304, 224]
- pair_id=11  src=synthetic  image=ui_0070.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [164.0, 101.0]  target 0: [40, 110, 304, 162]
  - pred 1: [167.0, 153.0]  target 1: [40, 172, 304, 224]
- pair_id=428  src=synthetic  image=ui_0044.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [162.0, 101.0]  target 0: [40, 110, 304, 162]
  - pred 1: [164.0, 146.0]  target 1: [40, 172, 304, 224]

### closed_gpt4o_mini

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [600.0, 300.0]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [600.0, 400.0]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [100.0, 300.0]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [150.0, 290.0]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=185  src=synthetic  image=ui_0151.png
  - inst 0: `Select the item directly above 'Item 1'.`
  - inst 1: `Click the element below the Item 1.`
  - pred 0: [40.0, 150.0]  target 0: [24, 18, 134, 58]
  - pred 1: [50.0, 150.0]  target 1: [40, 234, 304, 286]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [1260.0, 30.0]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [1200.0, 30.0]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [1000.0, 200.0]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [92.0, 200.0]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=259  src=ui_vision  image=9ddc289297f51dfb16c5a0abbd19c9aa.png
  - inst 0: `Select the button nearest to 'edit contents of frame'.`
  - inst 1: `Click the icon farthest from the edit contents of frame.`
  - pred 0: [470.0, 370.0]  target 0: [861.6, 52.2, 884.7, 76.1]
  - pred 1: [1000.0, 50.0]  target 1: [55.2, 85.0, 1655.4, 111.9]

**alignment** (3 examples):

- pair_id=217  src=synthetic  image=ui_0152.png
  - inst 0: `Select the control aligned in the same column as 'Paste'.`
  - inst 1: `Select the control aligned in the same row as 'Paste'.`
  - pred 0: [100.0, 50.0]  target 0: [40, 110, 304, 162]
  - pred 1: [200.0, 50.0]  target 1: [396, 18, 506, 58]
- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [1000.0, 600.0]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [1000.0, 600.0]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [1000.0, 400.0]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [400.0, 300.0]  target 1: [1340.9, 316.7, 1376.9, 342.9]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [370.0, 470.0]  target 0: [712, 452, 862, 602]
  - pred 1: [600.0, 400.0]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [200.0, 100.0]  target 0: [878, 286, 1028, 436]
  - pred 1: [200.0, 50.0]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [600.0, 400.0]  target 0: [712, 120, 862, 270]
  - pred 1: [800.0, 400.0]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [100.0, 300.0]  target 0: [712, 120, 862, 270]
  - pred 1: [80.0, 200.0]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: [50.0, 300.0]  target 0: [396, 18, 506, 58]
  - pred 1: [40.0, 150.0]  target 1: [40, 296, 304, 348]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [40.0, 150.0]  target 0: [40, 234, 304, 286]
  - pred 1: [50.0, 300.0]  target 1: [749, 394, 1009, 544]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: [1000.0, 400.0]  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [1200.0, 400.0]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [370.0, 150.0]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [800.0, 300.0]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=347  src=synthetic  image=ui_0075.png
  - inst 0: `Select the control to the left of 'Import'.`
  - inst 1: `Click the element to the right of the Import.`
  - pred 0: [150.0, 50.0]  target 0: [24, 18, 134, 58]
  - pred 1: [200.0, 50.0]  target 1: [520, 18, 630, 58]

**list_ordinal** (3 examples):

- pair_id=392  src=synthetic  image=ui_0085.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Select the second entry of the menu.`
  - pred 0: [30.0, 100.0]  target 0: [40, 110, 304, 162]
  - pred 1: [20.0, 60.0]  target 1: [40, 172, 304, 224]
- pair_id=11  src=synthetic  image=ui_0070.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [20.0, 50.0]  target 0: [40, 110, 304, 162]
  - pred 1: [50.0, 150.0]  target 1: [40, 172, 304, 224]
- pair_id=428  src=synthetic  image=ui_0044.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [50.0, 100.0]  target 0: [40, 110, 304, 162]
  - pred 1: [50.0, 130.0]  target 1: [40, 172, 304, 224]

### closed_gpt5

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [1346.0, 63.0]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [1292.0, 64.0]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [46.0, 50.0]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [885.0, 382.0]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=259  src=ui_vision  image=9ddc289297f51dfb16c5a0abbd19c9aa.png
  - inst 0: `Select the button nearest to 'edit contents of frame'.`
  - inst 1: `Click the icon farthest from the edit contents of frame.`
  - pred 0: [566.0, 51.0]  target 0: [861.6, 52.2, 884.7, 76.1]
  - pred 1: [1085.0, 50.0]  target 1: [55.2, 85.0, 1655.4, 111.9]

**alignment** (3 examples):

- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [1048.0, 572.0]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [998.0, 349.0]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [1107.0, 219.0]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [1118.0, 191.0]  target 1: [1340.9, 316.7, 1376.9, 342.9]
- pair_id=322  src=ui_vision  image=8c29c18fa5c6871b1bb29f52bf41dc20.png
  - inst 0: `Select the control aligned in the same row as 'Open Project'.`
  - inst 1: `Select the control aligned in the same column as 'Open Project'.`
  - pred 0: [846.0, 355.0]  target 0: [57.3, 45.2, 98.1, 83.1]
  - pred 1: [769.0, 419.0]  target 1: [88.5, 7.3, 124.5, 33.5]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [586.0, 542.0]  target 0: [712, 452, 862, 602]
  - pred 1: [620.0, 551.0]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [744.0, 407.0]  target 0: [878, 286, 1028, 436]
  - pred 1: [424.0, 44.0]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [777.0, 346.0]  target 0: [712, 120, 862, 270]
  - pred 1: [795.0, 304.0]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [165.0, 650.0]  target 0: [712, 120, 862, 270]
  - pred 1: [160.0, 104.0]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: [75.0, 35.0]  target 0: [396, 18, 506, 58]
  - pred 1: [150.0, 126.0]  target 1: [40, 296, 304, 348]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [167.0, 372.0]  target 0: [40, 234, 304, 286]
  - pred 1: [1035.0, 534.0]  target 1: [749, 394, 1009, 544]

**rel_pos_vertical** (3 examples):

- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [205.0, 95.0]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [116.0, 66.0]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=378  src=ui_vision  image=193bf4a40a8cc7c2fb66fd0d571412fe.png
  - inst 0: `Select the item directly above 'plastic tool'.`
  - inst 1: `Click the element below the plastic tool.`
  - pred 0: [28.0, 446.0]  target 0: [3.4, 766.5, 32.2, 791.2]
  - pred 1: [28.0, 513.0]  target 1: [3.4, 823.1, 34.6, 846.3]
- pair_id=208  src=ui_vision  image=70e1a72a7e02a905df56bc4b6a66f216.png
  - inst 0: `Select the item directly above 'chat'.`
  - inst 1: `Select the item directly below 'chat'.`
  - pred 0: [1341.0, 407.0]  target 0: [9.8, 335.1, 42.1, 362.3]
  - pred 1: [1339.0, 340.0]  target 1: [6.7, 426.7, 38.1, 454.6]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: [952.0, 86.0]  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [959.0, 86.0]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [887.0, 97.0]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [970.0, 97.0]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=35  src=ui_vision  image=720435a916fe1ddc2ee7fb3cfc00cd47.png
  - inst 0: `Select the control to the right of 'Left arrow'.`
  - inst 1: `Click the element to the left of the Left arrow.`
  - pred 0: [113.0, 70.0]  target 0: [511.2, 177.4, 544.8, 208.3]
  - pred 1: [92.0, 83.0]  target 1: [446.4, 179.0, 472.8, 209.8]

**list_ordinal** (3 examples):

- pair_id=389  src=ui_vision  image=c0ec43d8febbbcc338adc784beb85cc8.png
  - inst 0: `Select the second entry of the menu.`
  - inst 1: `Click the first item in the list.`
  - pred 0: [962.0, 134.0]  target 0: [1886.4, 175.9, 1920.0, 200.6]
  - pred 1: [206.0, 466.0]  target 1: [1845.6, 174.4, 1881.6, 199.1]
- pair_id=409  src=ui_vision  image=f6a16dc903a62ce7ea4446f2e8fbc095.png
  - inst 0: `Click the first item in the list.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [49.0, 70.0]  target 0: [191.2, 92.8, 232.2, 113.5]
  - pred 1: [703.0, 378.0]  target 1: [225.4, 120.7, 256.1, 142.3]
- pair_id=384  src=ui_vision  image=96364f0a524df3d5d92ed492a8f1521b.png
  - inst 0: `Select the second entry of the menu.`
  - inst 1: `Select the first entry of the menu.`
  - pred 0: [371.0, 122.0]  target 0: [476.4, 114.9, 500.3, 134.4]
  - pred 1: [39.0, 36.0]  target 1: [432.0, 115.9, 471.3, 133.3]

### gemma3_12b

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [877.0, 2.0]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [877.0, 2.0]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [488.0, 431.0]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [588.0, 111.0]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=185  src=synthetic  image=ui_0151.png
  - inst 0: `Select the item directly above 'Item 1'.`
  - inst 1: `Click the element below the Item 1.`
  - pred 0: [131.0, 101.0]  target 0: [24, 18, 134, 58]
  - pred 1: [150.0, 150.0]  target 1: [40, 234, 304, 286]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [1738.0, 10.0]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [1781.0, 10.0]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [117.0, 678.0]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [511.0, 338.0]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=31  src=synthetic  image=ui_0207.png
  - inst 0: `Click the icon nearest to the Zoom.`
  - inst 1: `Click the icon farthest from the Zoom.`
  - pred 0: [133.0, 27.0]  target 0: [148, 18, 258, 58]
  - pred 1: [681.0, 531.0]  target 1: [644, 18, 754, 58]

**alignment** (3 examples):

- pair_id=217  src=synthetic  image=ui_0152.png
  - inst 0: `Select the control aligned in the same column as 'Paste'.`
  - inst 1: `Select the control aligned in the same row as 'Paste'.`
  - pred 0: [133.0, 166.0]  target 0: [40, 110, 304, 162]
  - pred 1: [161.0, 10.0]  target 1: [396, 18, 506, 58]
- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [1681.0, 611.0]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [1581.0, 638.0]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [681.0, 638.0]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [681.0, 617.0]  target 1: [1340.9, 316.7, 1376.9, 342.9]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [588.0, 571.0]  target 0: [712, 452, 862, 602]
  - pred 1: [588.0, 578.0]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [151.0, 101.0]  target 0: [878, 286, 1028, 436]
  - pred 1: [163.0, 100.0]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [481.0, 331.0]  target 0: [712, 120, 862, 270]
  - pred 1: [481.0, 331.0]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [100.0, 100.0]  target 0: [712, 120, 862, 270]
  - pred 1: [100.0, 100.0]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: [118.0, 118.0]  target 0: [396, 18, 506, 58]
  - pred 1: [118.0, 118.0]  target 1: [40, 296, 304, 348]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [118.0, 566.0]  target 0: [40, 234, 304, 286]
  - pred 1: [117.0, 566.0]  target 1: [749, 394, 1009, 544]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: [131.0, 1007.0]  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [133.0, 638.0]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [131.0, 10.0]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [168.0, 110.0]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=347  src=synthetic  image=ui_0075.png
  - inst 0: `Select the control to the left of 'Import'.`
  - inst 1: `Click the element to the right of the Import.`
  - pred 0: [131.0, 116.0]  target 0: [24, 18, 134, 58]
  - pred 1: [181.0, 10.0]  target 1: [520, 18, 630, 58]

**list_ordinal** (3 examples):

- pair_id=392  src=synthetic  image=ui_0085.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Select the second entry of the menu.`
  - pred 0: [133.0, 100.0]  target 0: [40, 110, 304, 162]
  - pred 1: [171.0, 66.0]  target 1: [40, 172, 304, 224]
- pair_id=389  src=ui_vision  image=c0ec43d8febbbcc338adc784beb85cc8.png
  - inst 0: `Select the second entry of the menu.`
  - inst 1: `Click the first item in the list.`
  - pred 0: [231.0, 171.0]  target 0: [1886.4, 175.9, 1920.0, 200.6]
  - pred 1: [161.0, 231.0]  target 1: [1845.6, 174.4, 1881.6, 199.1]
- pair_id=409  src=ui_vision  image=f6a16dc903a62ce7ea4446f2e8fbc095.png
  - inst 0: `Click the first item in the list.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [178.0, 156.0]  target 0: [191.2, 92.8, 232.2, 113.5]
  - pred 1: [188.0, 238.0]  target 1: [225.4, 120.7, 256.1, 142.3]

### gemma3_27b

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [119.0, 86.0]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [872.0, 648.0]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [141.0, 111.0]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [731.0, 611.0]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=378  src=ui_vision  image=193bf4a40a8cc7c2fb66fd0d571412fe.png
  - inst 0: `Select the item directly above 'plastic tool'.`
  - inst 1: `Click the element below the plastic tool.`
  - pred 0: [27.0, 83.0]  target 0: [3.4, 766.5, 32.2, 791.2]
  - pred 1: [65.0, 638.0]  target 1: [3.4, 823.1, 34.6, 846.3]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [149.0, 18.0]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [748.0, 14.0]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [1798.0, 731.0]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [238.0, 618.0]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=31  src=synthetic  image=ui_0207.png
  - inst 0: `Click the icon nearest to the Zoom.`
  - inst 1: `Click the icon farthest from the Zoom.`
  - pred 0: [131.0, 64.0]  target 0: [148, 18, 258, 58]
  - pred 1: [859.0, 641.0]  target 1: [644, 18, 754, 58]

**alignment** (3 examples):

- pair_id=217  src=synthetic  image=ui_0152.png
  - inst 0: `Select the control aligned in the same column as 'Paste'.`
  - inst 1: `Select the control aligned in the same row as 'Paste'.`
  - pred 0: [114.0, 331.0]  target 0: [40, 110, 304, 162]
  - pred 1: [112.0, 28.0]  target 1: [396, 18, 506, 58]
- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [1193.0, 641.0]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [1198.0, 658.0]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [684.0, 441.0]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [731.0, 641.0]  target 1: [1340.9, 316.7, 1376.9, 342.9]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [651.0, 678.0]  target 0: [712, 452, 862, 602]
  - pred 1: [651.0, 681.0]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [266.0, 141.0]  target 0: [878, 286, 1028, 436]
  - pred 1: [266.0, 114.0]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [661.0, 608.0]  target 0: [712, 120, 862, 270]
  - pred 1: [614.0, 691.0]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [22.0, 18.0]  target 0: [712, 120, 862, 270]
  - pred 1: [25.0, 25.0]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: [21.0, 118.0]  target 0: [396, 18, 506, 58]
  - pred 1: [214.0, 144.0]  target 1: [40, 296, 304, 348]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [216.0, 179.0]  target 0: [40, 234, 304, 286]
  - pred 1: [21.0, 119.0]  target 1: [749, 394, 1009, 544]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: [37.0, 34.0]  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [448.0, 616.0]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [134.0, 24.0]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [158.0, 164.0]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=35  src=ui_vision  image=720435a916fe1ddc2ee7fb3cfc00cd47.png
  - inst 0: `Select the control to the right of 'Left arrow'.`
  - inst 1: `Click the element to the left of the Left arrow.`
  - pred 0: [119.0, 83.0]  target 0: [511.2, 177.4, 544.8, 208.3]
  - pred 1: [66.0, 83.0]  target 1: [446.4, 179.0, 472.8, 209.8]

**list_ordinal** (3 examples):

- pair_id=392  src=synthetic  image=ui_0085.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Select the second entry of the menu.`
  - pred 0: [65.0, 25.0]  target 0: [40, 110, 304, 162]
  - pred 1: [131.0, 33.0]  target 1: [40, 172, 304, 224]
- pair_id=389  src=ui_vision  image=c0ec43d8febbbcc338adc784beb85cc8.png
  - inst 0: `Select the second entry of the menu.`
  - inst 1: `Click the first item in the list.`
  - pred 0: [131.0, 114.0]  target 0: [1886.4, 175.9, 1920.0, 200.6]
  - pred 1: [148.0, 184.0]  target 1: [1845.6, 174.4, 1881.6, 199.1]
- pair_id=409  src=ui_vision  image=f6a16dc903a62ce7ea4446f2e8fbc095.png
  - inst 0: `Click the first item in the list.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [159.0, 251.0]  target 0: [191.2, 92.8, 232.2, 113.5]
  - pred 1: [179.0, 241.0]  target 1: [225.4, 120.7, 256.1, 142.3]

### gemma3_27b_ollama

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [139.0, 11.0]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [788.0, 688.0]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [189.0, 61.0]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [189.0, 61.0]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=378  src=ui_vision  image=193bf4a40a8cc7c2fb66fd0d571412fe.png
  - inst 0: `Select the item directly above 'plastic tool'.`
  - inst 1: `Click the element below the plastic tool.`
  - pred 0: [29.0, 81.0]  target 0: [3.4, 766.5, 32.2, 791.2]
  - pred 1: [29.0, 74.0]  target 1: [3.4, 823.1, 34.6, 846.3]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [1366.0, 28.0]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [678.0, 14.0]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [179.0, 74.0]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [260.0, 260.0]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=31  src=synthetic  image=ui_0207.png
  - inst 0: `Click the icon nearest to the Zoom.`
  - inst 1: `Click the icon farthest from the Zoom.`
  - pred 0: [156.0, 16.0]  target 0: [148, 18, 258, 58]
  - pred 1: [839.0, 684.0]  target 1: [644, 18, 754, 58]

**alignment** (3 examples):

- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [111.0, 559.0]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [111.0, 561.0]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [561.0, 371.0]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [561.0, 671.0]  target 1: [1340.9, 316.7, 1376.9, 342.9]
- pair_id=322  src=ui_vision  image=8c29c18fa5c6871b1bb29f52bf41dc20.png
  - inst 0: `Select the control aligned in the same row as 'Open Project'.`
  - inst 1: `Select the control aligned in the same column as 'Open Project'.`
  - pred 0: [226.0, 266.0]  target 0: [57.3, 45.2, 98.1, 83.1]
  - pred 1: [266.0, 266.0]  target 1: [88.5, 7.3, 124.5, 33.5]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [395.0, 495.0]  target 0: [712, 452, 862, 602]
  - pred 1: [396.0, 628.0]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [149.0, 16.0]  target 0: [878, 286, 1028, 436]
  - pred 1: [156.0, 18.0]  target 1: [40, 172, 304, 224]
- pair_id=180  src=synthetic  image=ui_0123.png
  - inst 0: `Click the Close control that is partly hidden.`
  - inst 1: `Click the Close control that is fully visible.`
  - pred 0: [166.0, 28.0]  target 0: [712, 452, 862, 602]
  - pred 1: [136.0, 28.0]  target 1: [380, 120, 530, 270]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [16.0, 16.0]  target 0: [712, 120, 862, 270]
  - pred 1: [26.0, 146.0]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: [16.0, 16.0]  target 0: [396, 18, 506, 58]
  - pred 1: [26.0, 146.0]  target 1: [40, 296, 304, 348]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [224.0, 224.0]  target 0: [40, 234, 304, 286]
  - pred 1: [176.0, 176.0]  target 1: [749, 394, 1009, 544]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: [199.0, 768.0]  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [789.0, 746.0]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [18.0, 18.0]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [189.0, 69.0]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=35  src=ui_vision  image=720435a916fe1ddc2ee7fb3cfc00cd47.png
  - inst 0: `Select the control to the right of 'Left arrow'.`
  - inst 1: `Click the element to the left of the Left arrow.`
  - pred 0: [778.0, 32.0]  target 0: [511.2, 177.4, 544.8, 208.3]
  - pred 1: [70.0, 30.0]  target 1: [446.4, 179.0, 472.8, 209.8]

**list_ordinal** (3 examples):

- pair_id=392  src=synthetic  image=ui_0085.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Select the second entry of the menu.`
  - pred 0: [176.0, 28.0]  target 0: [40, 110, 304, 162]
  - pred 1: [156.0, 164.0]  target 1: [40, 172, 304, 224]
- pair_id=428  src=synthetic  image=ui_0044.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [177.0, 31.0]  target 0: [40, 110, 304, 162]
  - pred 1: [182.0, 164.0]  target 1: [40, 172, 304, 224]
- pair_id=165  src=synthetic  image=ui_0019.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [177.0, 31.0]  target 0: [40, 110, 304, 162]
  - pred 1: [47.0, 132.0]  target 1: [40, 172, 304, 224]

### gemma3_4b

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [1016.0, 89.0]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [1031.0, 720]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [581.0, 434.0]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [577.0, 363.0]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=185  src=synthetic  image=ui_0151.png
  - inst 0: `Select the item directly above 'Item 1'.`
  - inst 1: `Click the element below the Item 1.`
  - pred 0: [100.0, 200.0]  target 0: [24, 18, 134, 58]
  - pred 1: [144.0, 336.0]  target 1: [40, 234, 304, 286]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [1311.0, 166.0]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [1311.0, 166.0]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [1033.0, 633.0]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [535.0, 256.0]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=31  src=synthetic  image=ui_0207.png
  - inst 0: `Click the icon nearest to the Zoom.`
  - inst 1: `Click the icon farthest from the Zoom.`
  - pred 0: [141.0, 234.0]  target 0: [148, 18, 258, 58]
  - pred 1: [948.0, 634.0]  target 1: [644, 18, 754, 58]

**alignment** (3 examples):

- pair_id=217  src=synthetic  image=ui_0152.png
  - inst 0: `Select the control aligned in the same column as 'Paste'.`
  - inst 1: `Select the control aligned in the same row as 'Paste'.`
  - pred 0: [351.0, 83.0]  target 0: [40, 110, 304, 162]
  - pred 1: [361.0, 214.0]  target 1: [396, 18, 506, 58]
- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [1348.0, 734.0]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [1331.0, 734.0]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [841.0, 633.0]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [841.0, 333.0]  target 1: [1340.9, 316.7, 1376.9, 342.9]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [546.0, 346.0]  target 0: [712, 452, 862, 602]
  - pred 1: [546.0, 346.0]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [414.0, 234.0]  target 0: [878, 286, 1028, 436]
  - pred 1: [414.0, 234.0]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [486.0, 234.0]  target 0: [712, 120, 862, 270]
  - pred 1: [648.0, 336.0]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [1280, 73.0]  target 0: [712, 120, 862, 270]
  - pred 1: [416.0, 264.0]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: [16.0, 216.0]  target 0: [396, 18, 506, 58]
  - pred 1: [141.0, 236.0]  target 1: [40, 296, 304, 348]
- pair_id=457  src=synthetic  image=ui_0185.png
  - inst 0: `Select the 'Sidebar' control located inside the dialog.`
  - inst 1: `Select the 'Sidebar' control located outside the dialog.`
  - pred 0: [416.0, 236.0]  target 0: [40, 296, 304, 348]
  - pred 1: [141.0, 236.0]  target 1: [712, 452, 862, 602]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: [42.0, 23.0]  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [41.0, 13.0]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [10.0, 16.0]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [10.0, 13.0]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=347  src=synthetic  image=ui_0075.png
  - inst 0: `Select the control to the left of 'Import'.`
  - inst 1: `Click the element to the right of the Import.`
  - pred 0: [141.0, 234.0]  target 0: [24, 18, 134, 58]
  - pred 1: [351.0, 224.0]  target 1: [520, 18, 630, 58]

**list_ordinal** (3 examples):

- pair_id=392  src=synthetic  image=ui_0085.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Select the second entry of the menu.`
  - pred 0: [147.0, 234.0]  target 0: [40, 110, 304, 162]
  - pred 1: [361.0, 234.0]  target 1: [40, 172, 304, 224]
- pair_id=11  src=synthetic  image=ui_0070.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [141.0, 213.0]  target 0: [40, 110, 304, 162]
  - pred 1: [466.0, 83.0]  target 1: [40, 172, 304, 224]
- pair_id=428  src=synthetic  image=ui_0044.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [141.0, 234.0]  target 0: [40, 110, 304, 162]
  - pred 1: [350.0, 230.0]  target 1: [40, 172, 304, 224]

### internvl3_8b

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [450.0, 171.0]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [191.0, 194.0]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [440.0, 175.0]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [468.0, 121.0]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=378  src=ui_vision  image=193bf4a40a8cc7c2fb66fd0d571412fe.png
  - inst 0: `Select the item directly above 'plastic tool'.`
  - inst 1: `Click the element below the plastic tool.`
  - pred 0: [23.0, 470.0]  target 0: [3.4, 766.5, 32.2, 791.2]
  - pred 1: [16.0, 7.0]  target 1: [3.4, 823.1, 34.6, 846.3]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [97.0, 7.0]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [963.0, 7.0]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [562.0, 335.0]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [408.0, 350.0]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=31  src=synthetic  image=ui_0207.png
  - inst 0: `Click the icon nearest to the Zoom.`
  - inst 1: `Click the icon farthest from the Zoom.`
  - pred 0: [100.0, 34.0]  target 0: [148, 18, 258, 58]
  - pred 1: [7.0, 164.0]  target 1: [644, 18, 754, 58]

**alignment** (3 examples):

- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [521.0, 255.0]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [594.0, 257.0]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [802.0, 281.0]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [816.0, 280.0]  target 1: [1340.9, 316.7, 1376.9, 342.9]
- pair_id=322  src=ui_vision  image=8c29c18fa5c6871b1bb29f52bf41dc20.png
  - inst 0: `Select the control aligned in the same row as 'Open Project'.`
  - inst 1: `Select the control aligned in the same column as 'Open Project'.`
  - pred 0: [526.0, 465.0]  target 0: [57.3, 45.2, 98.1, 83.1]
  - pred 1: [512.0, 500.0]  target 1: [88.5, 7.3, 124.5, 33.5]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [462.0, 600.0]  target 0: [712, 452, 862, 602]
  - pred 1: [450.0, 600.0]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [331.0, 3.0]  target 0: [878, 286, 1028, 436]
  - pred 1: [334.0, 3.0]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [562.0, 3.0]  target 0: [712, 120, 862, 270]
  - pred 1: [562.0, 343.0]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [102.0, 3.0]  target 0: [712, 120, 862, 270]
  - pred 1: [107.0, 231.0]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: [100.0, 30.0]  target 0: [396, 18, 506, 58]
  - pred 1: [102.0, 29.0]  target 1: [40, 296, 304, 348]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [102.0, 29.0]  target 0: [40, 234, 304, 286]
  - pred 1: [100.0, 30.0]  target 1: [749, 394, 1009, 544]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: None  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [938.0, 7.0]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [116.0, 171.0]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [200.0, 150.0]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=35  src=ui_vision  image=720435a916fe1ddc2ee7fb3cfc00cd47.png
  - inst 0: `Select the control to the right of 'Left arrow'.`
  - inst 1: `Click the element to the left of the Left arrow.`
  - pred 0: [100.0, 47.0]  target 0: [511.2, 177.4, 544.8, 208.3]
  - pred 1: [100.0, 47.0]  target 1: [446.4, 179.0, 472.8, 209.8]

**list_ordinal** (3 examples):

- pair_id=392  src=synthetic  image=ui_0085.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Select the second entry of the menu.`
  - pred 0: [50.0, 3.0]  target 0: [40, 110, 304, 162]
  - pred 1: [100.0, 36.0]  target 1: [40, 172, 304, 224]
- pair_id=11  src=synthetic  image=ui_0070.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [50.0, 33.0]  target 0: [40, 110, 304, 162]
  - pred 1: [100.0, 239.0]  target 1: [40, 172, 304, 224]
- pair_id=428  src=synthetic  image=ui_0044.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [100.0, 31.0]  target 0: [40, 110, 304, 162]
  - pred 1: [100.0, 239.0]  target 1: [40, 172, 304, 224]

### llama32_11b_vision

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [7.0, 7.0]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [102.0, 78.0]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [0.0, 0.0]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [0.0, 0.0]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=185  src=synthetic  image=ui_0151.png
  - inst 0: `Select the item directly above 'Item 1'.`
  - inst 1: `Click the element below the Item 1.`
  - pred 0: [0.0, 63.0]  target 0: [24, 18, 134, 58]
  - pred 1: [123.0, 123.0]  target 1: [40, 234, 304, 286]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [0.0, 0.0]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [0.0, 0.0]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [0.0, 0.0]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [342.0, 343.0]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=31  src=synthetic  image=ui_0207.png
  - inst 0: `Click the icon nearest to the Zoom.`
  - inst 1: `Click the icon farthest from the Zoom.`
  - pred 0: [102.0, 102.0]  target 0: [148, 18, 258, 58]
  - pred 1: [0.0, 0.0]  target 1: [644, 18, 754, 58]

**alignment** (3 examples):

- pair_id=217  src=synthetic  image=ui_0152.png
  - inst 0: `Select the control aligned in the same column as 'Paste'.`
  - inst 1: `Select the control aligned in the same row as 'Paste'.`
  - pred 0: [74.0, 21.0]  target 0: [40, 110, 304, 162]
  - pred 1: [74.0, 24.0]  target 1: [396, 18, 506, 58]
- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [114.0, 0.0]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [114.0, 0.0]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [102.0, 0.0]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [0.0, 0.0]  target 1: [1340.9, 316.7, 1376.9, 342.9]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [102.0, 555.0]  target 0: [712, 452, 862, 602]
  - pred 1: [102.0, 644.0]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [102.0, 343.0]  target 0: [878, 286, 1028, 436]
  - pred 1: [102.0, 64.0]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [102.0, 444.0]  target 0: [712, 120, 862, 270]
  - pred 1: [109.0, 444.0]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [0.0, 0.0]  target 0: [712, 120, 862, 270]
  - pred 1: [0.0, 0.0]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: [0.0, 0.0]  target 0: [396, 18, 506, 58]
  - pred 1: [0.0, 0.0]  target 1: [40, 296, 304, 348]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [0.0, 0.0]  target 0: [40, 234, 304, 286]
  - pred 1: [0.0, 0.0]  target 1: [749, 394, 1009, 544]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: [0.0, 0.0]  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [0.0, 0.0]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [6.0, 6.0]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [102.0, 24.0]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=347  src=synthetic  image=ui_0075.png
  - inst 0: `Select the control to the left of 'Import'.`
  - inst 1: `Click the element to the right of the Import.`
  - pred 0: [100.0, 123.0]  target 0: [24, 18, 134, 58]
  - pred 1: [234.0, 144.0]  target 1: [520, 18, 630, 58]

**list_ordinal** (3 examples):

- pair_id=392  src=synthetic  image=ui_0085.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Select the second entry of the menu.`
  - pred 0: [0.0, 0.0]  target 0: [40, 110, 304, 162]
  - pred 1: [0.0, 0.0]  target 1: [40, 172, 304, 224]
- pair_id=11  src=synthetic  image=ui_0070.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [0.0, 0.0]  target 0: [40, 110, 304, 162]
  - pred 1: [0.0, 0.0]  target 1: [40, 172, 304, 224]
- pair_id=428  src=synthetic  image=ui_0044.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [0.0, 0.0]  target 0: [40, 110, 304, 162]
  - pred 1: [0.0, 0.0]  target 1: [40, 172, 304, 224]

### minicpm_v_ollama

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [427.52, 304.2]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [258.56, 348.84]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [1368.0, 884.594]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [1175.04, 30.84]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=378  src=ui_vision  image=193bf4a40a8cc7c2fb66fd0d571412fe.png
  - inst 0: `Select the item directly above 'plastic tool'.`
  - inst 1: `Click the element below the plastic tool.`
  - pred 0: [680.64, 578.34]  target 0: [3.4, 766.5, 32.2, 791.2]
  - pred 1: [772.8, 575.1]  target 1: [3.4, 823.1, 34.6, 846.3]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [576.0, 36.18]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: None  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [1637.808, 191.008]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [998.44, 256.54]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=259  src=ui_vision  image=9ddc289297f51dfb16c5a0abbd19c9aa.png
  - inst 0: `Select the button nearest to 'edit contents of frame'.`
  - inst 1: `Click the icon farthest from the edit contents of frame.`
  - pred 0: [835.8, 53.766]  target 0: [861.6, 52.2, 884.7, 76.1]
  - pred 1: [1006.32, 374.796]  target 1: [55.2, 85.0, 1655.4, 111.9]

**alignment** (3 examples):

- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [1501.44, 256.373]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [1591.68, 335.738]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [1106.88, 221.85]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [1161.6, 220.32]  target 1: [1340.9, 316.7, 1376.9, 342.9]
- pair_id=322  src=ui_vision  image=8c29c18fa5c6871b1bb29f52bf41dc20.png
  - inst 0: `Select the control aligned in the same row as 'Open Project'.`
  - inst 1: `Select the control aligned in the same column as 'Open Project'.`
  - pred 0: [1417.92, 457.47]  target 0: [57.3, 45.2, 98.1, 83.1]
  - pred 1: [1416.96, 461.55]  target 1: [88.5, 7.3, 124.5, 33.5]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [583.04, 482.0]  target 0: [712, 452, 862, 602]
  - pred 1: [583.04, 482.0]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [426.24, 26.8]  target 0: [878, 286, 1028, 436]
  - pred 1: [542.08, 16.8]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [917.12, 292.8]  target 0: [712, 120, 862, 270]
  - pred 1: [884.48, 199.2]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [128.0, 312.8]  target 0: [712, 120, 862, 270]
  - pred 1: [138.88, 313.2]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: [626.56, 356.4]  target 0: [396, 18, 506, 58]
  - pred 1: [116.48, 188.4]  target 1: [40, 296, 304, 348]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [124.8, 232.0]  target 0: [40, 234, 304, 286]
  - pred 1: [119.68, 397.2]  target 1: [749, 394, 1009, 544]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: [784.32, 636.12]  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [1507.2, 360.18]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [683.0, 118.408]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [464.44, 301.074]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=347  src=synthetic  image=ui_0075.png
  - inst 0: `Select the control to the left of 'Import'.`
  - inst 1: `Click the element to the right of the Import.`
  - pred 0: [182.4, 33.6]  target 0: [24, 18, 134, 58]
  - pred 1: [182.4, 36.4]  target 1: [520, 18, 630, 58]

**list_ordinal** (3 examples):

- pair_id=392  src=synthetic  image=ui_0085.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Select the second entry of the menu.`
  - pred 0: [115.84, 235.2]  target 0: [40, 110, 304, 162]
  - pred 1: [157.44, 55.2]  target 1: [40, 172, 304, 224]
- pair_id=11  src=synthetic  image=ui_0070.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [115.84, 235.2]  target 0: [40, 110, 304, 162]
  - pred 1: [264.96, 107.2]  target 1: [40, 172, 304, 224]
- pair_id=428  src=synthetic  image=ui_0044.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [653.44, 338.4]  target 0: [40, 110, 304, 162]
  - pred 1: [124.8, 247.2]  target 1: [40, 172, 304, 224]

### os_atlas_base_7b

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [128.0, 72.0]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [192.0, 648.0]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [729.6, 993.048]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [19.2, 102.8]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=378  src=ui_vision  image=193bf4a40a8cc7c2fb66fd0d571412fe.png
  - inst 0: `Select the item directly above 'plastic tool'.`
  - inst 1: `Click the element below the plastic tool.`
  - pred 0: [1345.92, 109.08]  target 0: [3.4, 766.5, 32.2, 791.2]
  - pred 1: [349.44, 776.52]  target 1: [3.4, 823.1, 34.6, 846.3]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [226.56, 79.92]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [1824.0, 79.92]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [734.632, 233.68]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [912.336, 242.824]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=31  src=synthetic  image=ui_0207.png
  - inst 0: `Click the icon nearest to the Zoom.`
  - inst 1: `Click the icon farthest from the Zoom.`
  - pred 0: [26.88, 23.2]  target 0: [148, 18, 258, 58]
  - pred 1: [385.28, 124.8]  target 1: [644, 18, 754, 58]

**alignment** (3 examples):

- pair_id=217  src=synthetic  image=ui_0152.png
  - inst 0: `Select the control aligned in the same column as 'Paste'.`
  - inst 1: `Select the control aligned in the same row as 'Paste'.`
  - pred 0: [153.6, 24.0]  target 0: [40, 110, 304, 162]
  - pred 1: [153.6, 24.0]  target 1: [396, 18, 506, 58]
- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [165.12, 9.62]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [165.12, 9.62]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [1501.44, 241.74]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [1499.52, 238.68]  target 1: [1340.9, 316.7, 1376.9, 342.9]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [547.84, 454.4]  target 0: [712, 452, 862, 602]
  - pred 1: [547.84, 455.2]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [398.08, 21.6]  target 0: [878, 286, 1028, 436]
  - pred 1: [398.08, 21.6]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [716.8, 292.0]  target 0: [712, 120, 862, 270]
  - pred 1: [716.8, 291.2]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [39.68, 24.0]  target 0: [712, 120, 862, 270]
  - pred 1: [44.8, 104.0]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: [30.72, 24.8]  target 0: [396, 18, 506, 58]
  - pred 1: [32.0, 23.2]  target 1: [40, 296, 304, 348]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [38.4, 359.2]  target 0: [40, 234, 304, 286]
  - pred 1: [28.16, 21.6]  target 1: [749, 394, 1009, 544]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: [347.52, 776.52]  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [391.68, 776.52]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [178.946, 124.906]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [178.946, 124.906]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=35  src=ui_vision  image=720435a916fe1ddc2ee7fb3cfc00cd47.png
  - inst 0: `Select the control to the right of 'Left arrow'.`
  - inst 1: `Click the element to the left of the Left arrow.`
  - pred 0: [232.32, 78.84]  target 0: [511.2, 177.4, 544.8, 208.3]
  - pred 1: [192.0, 108.0]  target 1: [446.4, 179.0, 472.8, 209.8]

**list_ordinal** (3 examples):

- pair_id=392  src=synthetic  image=ui_0085.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Select the second entry of the menu.`
  - pred 0: [38.4, 115.2]  target 0: [40, 110, 304, 162]
  - pred 1: [275.2, 24.8]  target 1: [40, 172, 304, 224]
- pair_id=11  src=synthetic  image=ui_0070.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [37.12, 24.0]  target 0: [40, 110, 304, 162]
  - pred 1: [48.64, 115.2]  target 1: [40, 172, 304, 224]
- pair_id=165  src=synthetic  image=ui_0019.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [33.28, 23.2]  target 0: [40, 110, 304, 162]
  - pred 1: [48.64, 115.2]  target 1: [40, 172, 304, 224]

### paligemma2_10b

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [648.75, 342.0703125]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [646.875, 341.015625]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [1010.625, 698.216796875]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [957.1875, 512.494140625]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=185  src=synthetic  image=ui_0151.png
  - inst 0: `Select the item directly above 'Item 1'.`
  - inst 1: `Click the element below the Item 1.`
  - pred 0: None  target 0: [24, 18, 134, 58]
  - pred 1: [638.125, 398.828125]  target 1: [40, 234, 304, 286]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [45.9375, 89.6484375]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [22.5, 92.28515625]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [491.09765625, 120.55078125]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [491.09765625, 122.0390625]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=31  src=synthetic  image=ui_0207.png
  - inst 0: `Click the icon nearest to the Zoom.`
  - inst 1: `Click the icon farthest from the Zoom.`
  - pred 0: [43.75, 34.765625]  target 0: [148, 18, 258, 58]
  - pred 1: [385.0, 33.984375]  target 1: [644, 18, 754, 58]

**alignment** (3 examples):

- pair_id=217  src=synthetic  image=ui_0152.png
  - inst 0: `Select the control aligned in the same column as 'Paste'.`
  - inst 1: `Select the control aligned in the same row as 'Paste'.`
  - pred 0: [36.875, 35.546875]  target 0: [40, 110, 304, 162]
  - pred 1: [36.875, 35.546875]  target 1: [396, 18, 506, 58]
- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [966.5625, 475.36328125]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [1293.75, 712.10546875]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [959.0625, 546.85546875]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [957.1875, 508.505859375]  target 1: [1340.9, 316.7, 1376.9, 342.9]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [564.375, 458.59375]  target 0: [712, 452, 862, 602]
  - pred 1: [558.75, 458.59375]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [445.0, 39.453125]  target 0: [878, 286, 1028, 436]
  - pred 1: [769.375, 310.546875]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [665.0, 390.234375]  target 0: [712, 120, 862, 270]
  - pred 1: [639.375, 399.609375]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [384.375, 38.671875]  target 0: [712, 120, 862, 270]
  - pred 1: [170.625, 433.59375]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: [38.75, 35.9375]  target 0: [396, 18, 506, 58]
  - pred 1: [172.5, 430.46875]  target 1: [40, 296, 304, 348]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [170.0, 429.296875]  target 0: [40, 234, 304, 286]
  - pred 1: [29.375, 35.15625]  target 1: [749, 394, 1009, 544]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: [1568.4375, 264.7265625]  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [1002.1875, 820.01953125]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [126.0615234375, 431.8603515625]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [677.6640625, 431.8603515625]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=347  src=synthetic  image=ui_0075.png
  - inst 0: `Select the control to the left of 'Import'.`
  - inst 1: `Click the element to the right of the Import.`
  - pred 0: [426.25, 37.890625]  target 0: [24, 18, 134, 58]
  - pred 1: [421.25, 34.765625]  target 1: [520, 18, 630, 58]

**list_ordinal** (3 examples):

- pair_id=392  src=synthetic  image=ui_0085.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Select the second entry of the menu.`
  - pred 0: [453.75, 35.546875]  target 0: [40, 110, 304, 162]
  - pred 1: [451.25, 35.15625]  target 1: [40, 172, 304, 224]
- pair_id=11  src=synthetic  image=ui_0070.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [255.0, 38.671875]  target 0: [40, 110, 304, 162]
  - pred 1: [31.25, 32.03125]  target 1: [40, 172, 304, 224]
- pair_id=428  src=synthetic  image=ui_0044.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [639.375, 399.609375]  target 0: [40, 110, 304, 162]
  - pred 1: [35.625, 33.984375]  target 1: [40, 172, 304, 224]

### paligemma2_3b

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [650.0, 342.0703125]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [650.0, 342.0703125]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [1003.125, 696.7109375]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [1003.125, 693.197265625]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=185  src=synthetic  image=ui_0151.png
  - inst 0: `Select the item directly above 'Item 1'.`
  - inst 1: `Click the element below the Item 1.`
  - pred 0: [170.0, 429.6875]  target 0: [24, 18, 134, 58]
  - pred 1: [170.0, 429.6875]  target 1: [40, 234, 304, 286]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [11.25, 90.17578125]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [1865.625, 87.5390625]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [672.6875, 224.73046875]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [910.6328125, 507.50390625]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=31  src=synthetic  image=ui_0207.png
  - inst 0: `Click the icon nearest to the Zoom.`
  - inst 1: `Click the icon farthest from the Zoom.`
  - pred 0: [702.5, 419.53125]  target 0: [148, 18, 258, 58]
  - pred 1: [633.125, 399.609375]  target 1: [644, 18, 754, 58]

**alignment** (3 examples):

- pair_id=217  src=synthetic  image=ui_0152.png
  - inst 0: `Select the control aligned in the same column as 'Paste'.`
  - inst 1: `Select the control aligned in the same row as 'Paste'.`
  - pred 0: [881.875, 466.015625]  target 0: [40, 110, 304, 162]
  - pred 1: [881.875, 466.015625]  target 1: [396, 18, 506, 58]
- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [959.0625, 480.5302734375]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [959.0625, 480.5302734375]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [329.0625, 585.703125]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [324.375, 585.703125]  target 1: [1340.9, 316.7, 1376.9, 342.9]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [811.875, 447.265625]  target 0: [712, 452, 862, 602]
  - pred 1: [811.875, 447.265625]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [773.75, 310.9375]  target 0: [878, 286, 1028, 436]
  - pred 1: [774.375, 310.9375]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [661.875, 392.96875]  target 0: [712, 120, 862, 270]
  - pred 1: [661.875, 392.96875]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [170.0, 432.421875]  target 0: [712, 120, 862, 270]
  - pred 1: [170.0, 432.421875]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: [65.625, 37.5]  target 0: [396, 18, 506, 58]
  - pred 1: [61.875, 37.5]  target 1: [40, 296, 304, 348]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [880.0, 466.015625]  target 0: [40, 234, 304, 286]
  - pred 1: [65.625, 37.109375]  target 1: [749, 394, 1009, 544]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: [952.5, 607.5]  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [1599.375, 445.078125]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [133.3984375, 430.802734375]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [682.3330078125, 430.802734375]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=347  src=synthetic  image=ui_0075.png
  - inst 0: `Select the control to the left of 'Import'.`
  - inst 1: `Click the element to the right of the Import.`
  - pred 0: [170.0, 430.859375]  target 0: [24, 18, 134, 58]
  - pred 1: [632.5, 399.609375]  target 1: [520, 18, 630, 58]

**list_ordinal** (3 examples):

- pair_id=392  src=synthetic  image=ui_0085.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Select the second entry of the menu.`
  - pred 0: [170.0, 429.296875]  target 0: [40, 110, 304, 162]
  - pred 1: [58.75, 138.671875]  target 1: [40, 172, 304, 224]
- pair_id=11  src=synthetic  image=ui_0070.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [170.0, 429.6875]  target 0: [40, 110, 304, 162]
  - pred 1: [621.875, 192.1875]  target 1: [40, 172, 304, 224]
- pair_id=428  src=synthetic  image=ui_0044.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [170.0, 433.59375]  target 0: [40, 110, 304, 162]
  - pred 1: [786.875, 193.359375]  target 1: [40, 172, 304, 224]

### qwen2_5_vl_7b

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [230.0, 56.0]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [1203.0, 84.0]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [147.0, 62.0]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [120.0, 63.0]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=378  src=ui_vision  image=193bf4a40a8cc7c2fb66fd0d571412fe.png
  - inst 0: `Select the item directly above 'plastic tool'.`
  - inst 1: `Click the element below the plastic tool.`
  - pred 0: [12.0, 378.0]  target 0: [3.4, 766.5, 32.2, 791.2]
  - pred 1: [10.0, 259.0]  target 1: [3.4, 823.1, 34.6, 846.3]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [1876.0, 90.0]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [1520.0, 89.0]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [1024.0, 305.0]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [1078.0, 302.0]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=259  src=ui_vision  image=9ddc289297f51dfb16c5a0abbd19c9aa.png
  - inst 0: `Select the button nearest to 'edit contents of frame'.`
  - inst 1: `Click the icon farthest from the edit contents of frame.`
  - pred 0: [103.0, 62.0]  target 0: [861.6, 52.2, 884.7, 76.1]
  - pred 1: [1062.0, 563.0]  target 1: [55.2, 85.0, 1655.4, 111.9]

**alignment** (3 examples):

- pair_id=217  src=synthetic  image=ui_0152.png
  - inst 0: `Select the control aligned in the same column as 'Paste'.`
  - inst 1: `Select the control aligned in the same row as 'Paste'.`
  - pred 0: [102.0, 34.0]  target 0: [40, 110, 304, 162]
  - pred 1: [102.0, 34.0]  target 1: [396, 18, 506, 58]
- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [142.0, 15.0]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [142.0, 15.0]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [1364.0, 250.0]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [1364.0, 250.0]  target 1: [1340.9, 316.7, 1376.9, 342.9]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [612.0, 534.0]  target 0: [712, 452, 862, 602]
  - pred 1: [612.0, 530.0]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [450.0, 32.0]  target 0: [878, 286, 1028, 436]
  - pred 1: [450.0, 36.0]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [750.0, 361.0]  target 0: [712, 120, 862, 270]
  - pred 1: [748.0, 360.0]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [180.0, 452.0]  target 0: [712, 120, 862, 270]
  - pred 1: [187.0, 430.0]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: [180.0, 425.0]  target 0: [396, 18, 506, 58]
  - pred 1: [169.0, 420.0]  target 1: [40, 296, 304, 348]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [186.0, 420.0]  target 0: [40, 234, 304, 286]
  - pred 1: [160.0, 425.0]  target 1: [749, 394, 1009, 544]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: [1024.0, 790.0]  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [1024.0, 790.0]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [1025.0, 96.0]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [1025.0, 96.0]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=35  src=ui_vision  image=720435a916fe1ddc2ee7fb3cfc00cd47.png
  - inst 0: `Select the control to the right of 'Left arrow'.`
  - inst 1: `Click the element to the left of the Left arrow.`
  - pred 0: [270.0, 135.0]  target 0: [511.2, 177.4, 544.8, 208.3]
  - pred 1: [204.0, 96.0]  target 1: [446.4, 179.0, 472.8, 209.8]

**list_ordinal** (3 examples):

- pair_id=389  src=ui_vision  image=c0ec43d8febbbcc338adc784beb85cc8.png
  - inst 0: `Select the second entry of the menu.`
  - inst 1: `Click the first item in the list.`
  - pred 0: [1842.0, 95.0]  target 0: [1886.4, 175.9, 1920.0, 200.6]
  - pred 1: [1203.0, 436.0]  target 1: [1845.6, 174.4, 1881.6, 199.1]
- pair_id=409  src=ui_vision  image=f6a16dc903a62ce7ea4446f2e8fbc095.png
  - inst 0: `Click the first item in the list.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [210.0, 346.0]  target 0: [191.2, 92.8, 232.2, 113.5]
  - pred 1: [201.0, 346.0]  target 1: [225.4, 120.7, 256.1, 142.3]
- pair_id=384  src=ui_vision  image=96364f0a524df3d5d92ed492a8f1521b.png
  - inst 0: `Select the second entry of the menu.`
  - inst 1: `Select the first entry of the menu.`
  - pred 0: [50.0, 32.0]  target 0: [476.4, 114.9, 500.3, 134.4]
  - pred 1: [12.0, 34.0]  target 1: [432.0, 115.9, 471.3, 133.3]

### qwen2_vl_7b

**rel_pos_vertical** (3 examples):

- pair_id=199  src=ui_vision  image=4907f58b1addf95747d6af7aafb76e04.png
  - inst 0: `Click the element above the replace.`
  - inst 1: `Click the element below the replace.`
  - pred 0: [100.0, 100.0]  target 0: [1165.2, 74.1, 1195.6, 96.7]
  - pred 1: [13.0, 100.0]  target 1: [1158.5, 130.1, 1185.7, 152.7]
- pair_id=365  src=ui_vision  image=0c9820a4005d278ca747aea15560ec9b.png
  - inst 0: `Select the item directly below 'print preview'.`
  - inst 1: `Select the item directly above 'print preview'.`
  - pred 0: [10.0, 10.0]  target 0: [147.5, 81.6, 167.9, 104.4]
  - pred 1: [10.0, 10.0]  target 1: [143.9, 27.7, 190.3, 41.0]
- pair_id=378  src=ui_vision  image=193bf4a40a8cc7c2fb66fd0d571412fe.png
  - inst 0: `Select the item directly above 'plastic tool'.`
  - inst 1: `Click the element below the plastic tool.`
  - pred 0: [10.0, 100.0]  target 0: [3.4, 766.5, 32.2, 791.2]
  - pred 1: [10.0, 100.0]  target 1: [3.4, 823.1, 34.6, 846.3]

**proximity** (3 examples):

- pair_id=112  src=ui_vision  image=ad46317d3b830f8185cb91bfa7af616e.png
  - inst 0: `Click the icon farthest from the current file directory.`
  - inst 1: `Select the button nearest to 'current file directory'.`
  - pred 0: [118.0, 70.0]  target 0: [76.4, 569.8, 201.2, 603.7]
  - pred 1: [678.0, 70.0]  target 1: [58.6, 161.1, 127.7, 181.5]
- pair_id=195  src=ui_vision  image=1859bb48a5efea49991919744c1ccd5b.png
  - inst 0: `Select the button farthest from 'Selected glyph box highlighted'.`
  - inst 1: `Click the icon nearest to the Selected glyph box highlighted.`
  - pred 0: [96.0, 25.0]  target 0: [661.5, 394.7, 689.9, 419.7]
  - pred 1: [291.0, 230.0]  target 1: [688.3, 421.2, 715.4, 446.9]
- pair_id=31  src=synthetic  image=ui_0207.png
  - inst 0: `Click the icon nearest to the Zoom.`
  - inst 1: `Click the icon farthest from the Zoom.`
  - pred 0: [20.0, 27.0]  target 0: [148, 18, 258, 58]
  - pred 1: [428.0, 357.0]  target 1: [644, 18, 754, 58]

**alignment** (3 examples):

- pair_id=217  src=synthetic  image=ui_0152.png
  - inst 0: `Select the control aligned in the same column as 'Paste'.`
  - inst 1: `Select the control aligned in the same row as 'Paste'.`
  - pred 0: [20.0, 27.0]  target 0: [40, 110, 304, 162]
  - pred 1: [20.0, 27.0]  target 1: [396, 18, 506, 58]
- pair_id=81  src=ui_vision  image=f51c978400b8a800b79a27424b5d73c4.png
  - inst 0: `Select the control aligned in the same column as 'Navigate Backwards'.`
  - inst 1: `Select the control aligned in the same row as 'Navigate Backwards'.`
  - pred 0: [10.0, 10.0]  target 0: [0.0, 39.3, 235.2, 61.3]
  - pred 1: [10.0, 10.0]  target 1: [104.0, 6.7, 135.2, 28.6]
- pair_id=311  src=ui_vision  image=2c0461b176fb61dfc5eaefcde66bace2.png
  - inst 0: `Click the element in the same column as the Align to Left.`
  - inst 1: `Click the element in the same row as the Align to Left.`
  - pred 0: [784.0, 280.0]  target 0: [1256.9, 278.8, 1292.9, 306.5]
  - pred 1: [784.0, 283.0]  target 1: [1340.9, 316.7, 1376.9, 342.9]

**occlusion** (3 examples):

- pair_id=462  src=synthetic  image=ui_0194.png
  - inst 0: `Select the 'Reset' element that is currently partly hidden.`
  - inst 1: `Select the 'Reset' element that is currently fully visible.`
  - pred 0: [428.0, 562.0]  target 0: [712, 452, 862, 602]
  - pred 1: [428.0, 562.0]  target 1: [40, 172, 304, 224]
- pair_id=453  src=synthetic  image=ui_0142.png
  - inst 0: `Select the 'Paste' element that is currently partly hidden.`
  - inst 1: `Select the 'Paste' element that is currently fully visible.`
  - pred 0: [308.0, 20.0]  target 0: [878, 286, 1028, 436]
  - pred 1: [309.0, 20.0]  target 1: [40, 172, 304, 224]
- pair_id=429  src=synthetic  image=ui_0044.png
  - inst 0: `Select the 'Paste' element that is currently fully visible.`
  - inst 1: `Click the Paste control that is partly hidden.`
  - pred 0: [558.0, 357.0]  target 0: [712, 120, 862, 270]
  - pred 1: [558.0, 357.0]  target 1: [546, 452, 696, 602]

**containment** (3 examples):

- pair_id=438  src=synthetic  image=ui_0028.png
  - inst 0: `Select the 'Sidebar' control located outside the dialog.`
  - inst 1: `Select the 'Sidebar' control located inside the dialog.`
  - pred 0: [20.0, 27.0]  target 0: [712, 120, 862, 270]
  - pred 1: [29.0, 125.0]  target 1: [40, 234, 304, 286]
- pair_id=399  src=synthetic  image=ui_0213.png
  - inst 0: `Click the Sidebar button that is outside the panel.`
  - inst 1: `Click the Sidebar button that is inside the panel.`
  - pred 0: [22.0, 30.0]  target 0: [396, 18, 506, 58]
  - pred 1: [21.0, 27.0]  target 1: [40, 296, 304, 348]
- pair_id=215  src=synthetic  image=ui_0152.png
  - inst 0: `Click the Sidebar button that is inside the panel.`
  - inst 1: `Click the Sidebar button that is outside the panel.`
  - pred 0: [21.0, 27.0]  target 0: [40, 234, 304, 286]
  - pred 1: [20.0, 27.0]  target 1: [749, 394, 1009, 544]

**rel_pos_horizontal** (3 examples):

- pair_id=196  src=ui_vision  image=e4200754f6e1837e624fa6125b03c2e0.png
  - inst 0: `Click the element to the left of the flip vertical.`
  - inst 1: `Select the control to the right of 'flip vertical'.`
  - pred 0: [13.0, 105.0]  target 0: [261.0, 768.4, 285.0, 797.7]
  - pred 1: [15.0, 705.0]  target 1: [810.4, 766.1, 834.4, 795.4]
- pair_id=239  src=ui_vision  image=8d9266554713a61f9ba2787d068c6920.png
  - inst 0: `Click the element to the left of the sort to descending order.`
  - inst 1: `Click the element to the right of the sort to descending order.`
  - pred 0: [131.0, 150.0]  target 0: [470.0, 51.6, 493.9, 76.3]
  - pred 1: [131.0, 150.0]  target 1: [536.6, 52.6, 562.2, 74.3]
- pair_id=35  src=ui_vision  image=720435a916fe1ddc2ee7fb3cfc00cd47.png
  - inst 0: `Select the control to the right of 'Left arrow'.`
  - inst 1: `Click the element to the left of the Left arrow.`
  - pred 0: [13.0, 100.0]  target 0: [511.2, 177.4, 544.8, 208.3]
  - pred 1: [10.0, 100.0]  target 1: [446.4, 179.0, 472.8, 209.8]

**list_ordinal** (3 examples):

- pair_id=392  src=synthetic  image=ui_0085.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Select the second entry of the menu.`
  - pred 0: [30.0, 140.0]  target 0: [40, 110, 304, 162]
  - pred 1: [214.0, 21.0]  target 1: [40, 172, 304, 224]
- pair_id=11  src=synthetic  image=ui_0070.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [30.0, 29.0]  target 0: [40, 110, 304, 162]
  - pred 1: [30.0, 139.0]  target 1: [40, 172, 304, 224]
- pair_id=428  src=synthetic  image=ui_0044.png
  - inst 0: `Select the first entry of the menu.`
  - inst 1: `Click the second item in the list.`
  - pred 0: [66.5, 50.5]  target 0: [40, 110, 304, 162]
  - pred 1: [30.0, 217.0]  target 1: [40, 172, 304, 224]
