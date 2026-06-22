"""L2 — effects = objectives over L1 (Wittgenstein: an effect IS a D3 Objective).

A param vector theta maps to a GendynWalk; the voice is rendered, spectralized,
and scored by an objective built from L1 features. search() runs gradient-free
global optimization (differential_evolution, DD4) with a seeded random-search
baseline for comparison.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy.optimize import differential_evolution

from ..l0_signal.gendyn import GendynWalk, RandomWalkBound
from ..l1_features import features as F
from ..lsigma.spectralize import PartialSet, SpectralizeParams, spectralize

# theta = [time_lo, time_span, amp_step]  (a small, interpretable param space)
THETA_BOUNDS = [(4.0, 40.0), (4.0, 60.0), (0.01, 0.30)]


def make_walk(theta: np.ndarray, seed: int, breakpoints: int = 12) -> GendynWalk:
    time_lo, time_span, amp_step = theta
    return GendynWalk(
        breakpoints=breakpoints,
        amp_walk=RandomWalkBound(-1.0, 1.0, "gauss", float(amp_step), True),
        time_walk=RandomWalkBound(float(time_lo), float(time_lo + time_span), "gauss", 1.5, True),
        seed=seed,
    )


def features_of(theta: np.ndarray, seed: int, sr: int, dur_s: float,
                params: SpectralizeParams) -> tuple[PartialSet, dict]:
    from ..l0_signal.gendyn import render
    walk = make_walk(theta, seed)
    sig = render(walk, dur_s, sr)
    P = spectralize(sig, sr, params)
    feats = {
        "spectral_centroid": F.spectral_centroid(P),
        "harmonicity_match": F.harmonicity_match(P),
        "dissonance_minor2": F.dissonance(P, 16 / 15),
    }
    return P, feats


# --- objective combinators (each returns a cost; lower is better) ---

def low(feature: str, target: float):
    def cost(feats: dict) -> float:
        v = feats[feature]
        return max(0.0, v - target) if not np.isnan(v) else 1e9
    return cost


def high(feature: str):
    def cost(feats: dict) -> float:
        v = feats[feature]
        return -v if not np.isnan(v) else 1e9
    return cost


def weighted(terms: list[tuple[float, Callable]]):
    def cost(feats: dict) -> float:
        return float(sum(w * c(feats) for w, c in terms))
    return cost


@dataclass
class SearchResult:
    theta: np.ndarray
    cost: float
    feats: dict
    n_eval: int


def search(objective, *, seed: int = 7, sr: int = 22050, dur_s: float = 0.4,
           params: SpectralizeParams | None = None, maxiter: int = 15,
           popsize: int = 8) -> SearchResult:
    if params is None:
        params = SpectralizeParams()
    n_eval = {"n": 0}

    def f(theta):
        n_eval["n"] += 1
        _P, feats = features_of(theta, seed, sr, dur_s, params)
        return objective(feats)

    res = differential_evolution(
        f, THETA_BOUNDS, seed=seed, maxiter=maxiter, popsize=popsize,
        tol=0.01, polish=False, init="sobol",
    )
    _P, feats = features_of(res.x, seed, sr, dur_s, params)
    return SearchResult(theta=res.x, cost=float(res.fun), feats=feats, n_eval=n_eval["n"])


def random_search(objective, *, seed: int = 7, sr: int = 22050, dur_s: float = 0.4,
                  params: SpectralizeParams | None = None, n: int = 120) -> SearchResult:
    if params is None:
        params = SpectralizeParams()
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(n):
        theta = np.array([rng.uniform(lo, hi) for lo, hi in THETA_BOUNDS])
        _P, feats = features_of(theta, seed, sr, dur_s, params)
        c = objective(feats)
        if best is None or c < best.cost:
            best = SearchResult(theta=theta, cost=float(c), feats=feats, n_eval=n)
    return best
