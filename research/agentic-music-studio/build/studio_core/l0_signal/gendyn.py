"""L0 — GENDYN dynamic stochastic synthesis (Xenakis, C2/D4).

The waveform is a polygon of N breakpoints; each breakpoint's amplitude and
time-interval is driven by a bounded, reflected random walk. Spectrum is
*emergent* from the walk dynamics — never designed in the frequency domain.

Determinism contract: render() is a pure function of (walk, dur_s, sr). Two
calls return bit-identical arrays. The only randomness source is a seeded
numpy Generator keyed by walk.seed.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class RandomWalkBound:
    """The *bound* of a random walk, not the noise. Seedable + reproducible."""

    lo: float
    hi: float
    step_dist: str = "gauss"  # 'gauss' | 'uniform' | 'cauchy'
    step_scale: float = 0.05
    mirror: bool = True  # reflect at bounds (vs clip)


@dataclass(frozen=True)
class GendynWalk:
    breakpoints: int
    amp_walk: RandomWalkBound
    time_walk: RandomWalkBound  # interpreted as segment lengths in samples
    seed: int


def _reflect(y: np.ndarray, lo: float, hi: float) -> np.ndarray:
    """Fold values into [lo, hi] by triangle reflection (deterministic)."""
    span = hi - lo
    if span <= 0:
        return np.full_like(y, lo)
    z = np.mod(y - lo, 2 * span)
    z = np.where(z > span, 2 * span - z, z)
    return lo + z


def _step(x: np.ndarray, b: RandomWalkBound, rng: np.random.Generator) -> np.ndarray:
    if b.step_dist == "gauss":
        delta = rng.normal(0.0, b.step_scale, x.shape)
    elif b.step_dist == "uniform":
        delta = rng.uniform(-b.step_scale, b.step_scale, x.shape)
    elif b.step_dist == "cauchy":
        # clip heavy tails so a single step cannot blow past the bounds / NaN
        delta = np.clip(rng.standard_cauchy(x.shape) * b.step_scale, -2 * b.step_scale, 2 * b.step_scale)
    else:
        raise ValueError(f"unknown step_dist: {b.step_dist}")
    y = x + delta
    return _reflect(y, b.lo, b.hi) if b.mirror else np.clip(y, b.lo, b.hi)


def _interp_polygon(amps: np.ndarray, seg_samples: np.ndarray) -> np.ndarray:
    """Linear-interpolate one closed cycle: amp[i] -> amp[(i+1)%N] over seg_samples[i]."""
    n = len(amps)
    pieces = []
    for i in range(n):
        a0 = float(amps[i])
        a1 = float(amps[(i + 1) % n])
        m = int(seg_samples[i])
        pieces.append(np.linspace(a0, a1, m, endpoint=False))
    return np.concatenate(pieces)


def render(walk: GendynWalk, dur_s: float, sr: int) -> np.ndarray:
    """Render a GENDYN voice. Pure function of (walk, dur_s, sr)."""
    if walk.breakpoints < 2:
        raise ValueError("GENDYN needs >= 2 breakpoints")
    rng = np.random.default_rng(walk.seed)
    n = walk.breakpoints
    amps = rng.uniform(walk.amp_walk.lo, walk.amp_walk.hi, n)
    times = rng.uniform(walk.time_walk.lo, walk.time_walk.hi, n)

    total = int(round(dur_s * sr))
    out: list[np.ndarray] = []
    written = 0
    while written < total:
        amps = _step(amps, walk.amp_walk, rng)
        times = _step(times, walk.time_walk, rng)
        seg = np.maximum(1, np.round(times)).astype(int)  # >=1 sample per segment
        cycle = _interp_polygon(amps, seg)
        out.append(cycle)
        written += len(cycle)

    sig = np.concatenate(out)[:total]
    peak = float(np.max(np.abs(sig))) if sig.size else 0.0
    if peak > 0:
        sig = sig / peak * 0.99
    return sig.astype(np.float32)
