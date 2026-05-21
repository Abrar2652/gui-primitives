"""Config loading with single-level `inherit:` support and dotted-key access.

Configs are plain YAML. An experiment config may set `inherit: <relative path>`;
the parent is loaded first and the child is deep-merged on top. This keeps every
experiment's full effective configuration explicit and snapshot-able into the run
manifest (see logging_utils.init_run)."""
from __future__ import annotations
import copy
from pathlib import Path
from typing import Any

import yaml


def _deep_merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in override.items():
        if k == "inherit":
            continue
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML config, resolving a single `inherit:` parent if present."""
    path = Path(path)
    with open(path) as f:
        cfg = yaml.safe_load(f) or {}
    parent_rel = cfg.get("inherit")
    if parent_rel:
        parent = load_config((path.parent / parent_rel).resolve())
        cfg = _deep_merge(parent, cfg)
    return cfg


def get(cfg: dict, dotted_key: str, default: Any = None) -> Any:
    """Read a nested value with a dotted key, e.g. get(cfg, 'eval.bootstrap_ci')."""
    node: Any = cfg
    for part in dotted_key.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node
