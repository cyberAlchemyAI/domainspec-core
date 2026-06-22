"""L0 — EngineSpec protocol + an additive control voice.

The engine is swappable behind this protocol (DD1/DD2): a hand-written GENDYN
today, a SuperCollider OSC bridge later. The additive voice is the control case
where a PartialSet is authored directly (no Spectralize needed) — used to sanity
-check L1 features before trusting them on GENDYN output.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np


class EngineSpec(Protocol):
    def render(self, dur_s: float, sr: int) -> np.ndarray: ...


@dataclass(frozen=True)
class AdditiveVoice:
    """Sum of sinusoids with known (freq, amp) partials — the analyzable control."""

    partials: tuple[tuple[float, float], ...]  # (freq_hz, amp)
    seed: int = 0

    def render(self, dur_s: float, sr: int) -> np.ndarray:
        n = int(round(dur_s * sr))
        t = np.arange(n) / sr
        sig = np.zeros(n, dtype=np.float64)
        for f, a in self.partials:
            sig += a * np.sin(2 * np.pi * f * t)
        peak = float(np.max(np.abs(sig))) if sig.size else 0.0
        if peak > 0:
            sig = sig / peak * 0.99
        return sig.astype(np.float32)
