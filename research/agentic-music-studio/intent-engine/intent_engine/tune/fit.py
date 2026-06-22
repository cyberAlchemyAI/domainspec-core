"""L1 — the engineering (MODEL I2): deterministic objective search over the GENDYN voice.

Thin adapter over studio-core `search` machinery (G3/G6). Uses moment_centroid for 'darkness'
(F1, not the peak-pick), the FROZEN render ctx (F4), and the live `dissonance_minor2` key (F3).
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import differential_evolution

from studio_core.l0_signal.gendyn import render
from studio_core.l1_features import features as F
from studio_core.l2_effects.objective import THETA_BOUNDS, make_walk
from studio_core.lsigma.spectralize import SpectralizeParams, spectralize

from ..program import IntentSpec, RealizedSpec

FROZEN_SPECTRALIZE = SpectralizeParams()


def feats_of(theta, seed: int, ctx) -> dict:
    """The three live readout keys. Centroid via moment_centroid (full-spectrum, F1)."""
    walk = make_walk(theta, seed)
    sig = render(walk, ctx.dur_s, ctx.sr)
    P = spectralize(sig, ctx.sr, FROZEN_SPECTRALIZE)
    return {
        "spectral_centroid": F.moment_centroid(sig, ctx.sr),       # F1
        "harmonicity_match": F.harmonicity_match(P),
        "dissonance_minor2": F.dissonance(P, 16 / 15),             # F3 live key
    }


# per-feature normalizers so weighted terms are comparable (Option 1 weighted steering)
_NORM = {"spectral_centroid": 1000.0, "harmonicity_match": 1.0, "dissonance_minor2": 10.0}


def _objective(targets):
    """Weighted multi-objective. 'low' SEEKS its target (two-sided), so it genuinely competes
    with 'high' (maximize); shifting a target's weight slides the trade-off (the steering knob)."""
    def cost(feats: dict) -> float:
        c = 0.0
        for t in targets:
            v = feats[t.feature]
            n = _NORM.get(t.feature, 1.0)
            if np.isnan(v):
                c += 1e9
                continue
            if t.op == "low":
                term = abs(v - t.value) / n          # seek the target (creates tension)
            else:  # 'high' -> reward larger value
                term = -v / n
            c += t.weight * term
        return c
    return cost


def fit(ispec: IntentSpec) -> RealizedSpec:
    obj = _objective(ispec.targets)
    ctx = ispec.ctx  # FROZEN render ctx shared with render (F4)

    def f(theta):
        return obj(feats_of(theta, ispec.seed, ctx))

    res = differential_evolution(
        f, THETA_BOUNDS, seed=ispec.seed, maxiter=12, popsize=6,
        tol=0.01, polish=False, init="sobol",
    )
    walk = make_walk(res.x, ispec.seed)            # search -> SearchResult -> make_walk (F6)
    feats = feats_of(res.x, ispec.seed, ctx)
    return RealizedSpec(walk=walk, ctx=ctx, feats=feats, targets=ispec.targets)
