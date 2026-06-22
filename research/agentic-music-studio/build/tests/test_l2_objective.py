import numpy as np

from studio_core.l2_effects.objective import (THETA_BOUNDS, features_of, low,
                                              random_search, search)
from studio_core.lsigma.spectralize import SpectralizeParams


def test_features_of_reproducible():
    theta = np.array([12.0, 20.0, 0.1])
    a = features_of(theta, 5, 22050, 0.3, SpectralizeParams())[1]
    b = features_of(theta, 5, 22050, 0.3, SpectralizeParams())[1]
    assert a == b


def test_search_lowers_centroid_vs_baseline():
    # "dark" = minimize centroid. Search should beat the mean random-init centroid.
    rng = np.random.default_rng(0)
    inits = [np.array([rng.uniform(lo, hi) for lo, hi in THETA_BOUNDS]) for _ in range(12)]
    base = np.nanmean([features_of(t, 5, 22050, 0.3, SpectralizeParams())[1]["spectral_centroid"] for t in inits])
    # pure-minimize objective (an Objective is just feats -> cost)
    res = search(lambda feats: feats["spectral_centroid"], seed=5, dur_s=0.3, maxiter=8, popsize=6)
    assert res.feats["spectral_centroid"] <= base
