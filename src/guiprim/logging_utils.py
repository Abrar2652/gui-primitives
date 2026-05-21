"""Run logging. Each run gets a directory, a JSON manifest (config snapshot +
git commit + environment) and a rotating log file, so any result can be traced
back to the exact code and configuration that produced it."""
from __future__ import annotations
import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def _git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "unknown"


def get_logger(name: str = "guiprim") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(h)
        logger.setLevel(logging.INFO)
    return logger


def init_run(run_dir: str | Path, config: dict[str, Any]) -> Path:
    """Create a run directory and write a provenance manifest. Returns the path."""
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "created": datetime.utcnow().isoformat() + "Z",
        "git_commit": _git_commit(),
        "python": sys.version,
        "config": config,
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    fh = logging.FileHandler(run_dir / "run.log")
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    get_logger().addHandler(fh)
    return run_dir
