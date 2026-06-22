"""L3 — listener-study harness for O1 (scaffold; live run handed off).

Builds a blinded battery of stimuli at varying strangeness-objective targets and
scores the correlation between the objective value and listener "strangeness"
ratings. The ACTUAL run needs human participants and a pre-registered criterion
(experiments/o1_strangeness_study/criterion.md) — handed off to
research-evidence-harness. score_correlation is validated here on synthetic
ratings only (no felt-match claim).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.stats import spearmanr

from ..l2_effects.objective import features_of
from ..lsigma.spectralize import SpectralizeParams


@dataclass
class Stimulus:
    stimulus_id: int
    theta: np.ndarray
    objective_value: float  # the strangeness proxy (higher = more dissonant/inharmonic)


def strangeness_value(feats: dict) -> float:
    """proxy = w1*dissonance + w2*inharmonicity-ish(1-match). NOT the felt effect (O1)."""
    diss = feats["dissonance_minor2"]
    inharm = feats["harmonicity_match"]  # higher match-distance ~ less harmonic ~ stranger (proxy)
    return float(1.0 * diss + 0.5 * inharm)


def build_battery(thetas: np.ndarray, *, seed: int = 11, sr: int = 22050,
                  dur_s: float = 0.4, params: SpectralizeParams | None = None) -> list[Stimulus]:
    if params is None:
        params = SpectralizeParams()
    out = []
    for i, theta in enumerate(thetas):
        _P, feats = features_of(np.asarray(theta), seed, sr, dur_s, params)
        out.append(Stimulus(stimulus_id=i, theta=np.asarray(theta),
                            objective_value=strangeness_value(feats)))
    # blinded presentation order (deterministic shuffle)
    rng = np.random.default_rng(seed)
    rng.shuffle(out)
    return out


def score_correlation(objective_values, ratings) -> dict:
    rho, p = spearmanr(objective_values, ratings)
    return {"spearman_rho": float(rho), "p_value": float(p), "n": len(ratings)}
