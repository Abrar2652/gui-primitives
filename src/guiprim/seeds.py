"""Centralised seeding. Every script calls set_global_seed() exactly once so that
a run is bit-reproducible given the same config — a hard requirement for the
reproducibility claims in the paper."""
from __future__ import annotations
import os
import random


def set_global_seed(seed: int) -> None:
    """Seed Python, NumPy and (if present) PyTorch, and force deterministic kernels."""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        # Determinism: greedy decoding + these flags make generation reproducible.
        torch.use_deterministic_algorithms(True, warn_only=True)
        torch.backends.cudnn.benchmark = False
    except ImportError:
        pass
