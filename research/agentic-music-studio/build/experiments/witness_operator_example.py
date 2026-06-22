"""Operator-example witness: "dark violin stochastic synth -> dissonance scale -> strangeness".

Demonstrates the pipeline end-to-end. NOTE (post-O8): under FROZEN Spectralize
params the realization replays bit-identically (Reading A holds); but O8 showed
the feature VALUES are analyzer-dependent on this stochastic timbre (Reading B
fails). So this witness proves mechanical reproducibility, NOT that the perceptual
targets are timbre-faithful properties. Reported honestly.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from studio_core.l1_features import features as F
from studio_core.l2_effects.objective import features_of, low, make_walk, search
from studio_core.l3_evidence.meter import report_features
from studio_core.lsigma.spectralize import SpectralizeParams, spectralize
from studio_core.spec import FROZEN_SPECTRALIZE, Spec, analyze, realize

SR, DUR = 22050, 0.4


def main():
    rep = {}
    # "dark + violin-ish stochastic": minimize centroid + harmonicity match-distance
    obj = lambda f: 1.0 * f["spectral_centroid"] / 1000.0 + 2.0 * f["harmonicity_match"]
    res = search(obj, seed=7, dur_s=DUR, maxiter=10, popsize=8)
    walk = make_walk(res.theta, 7)
    spec = Spec(l0=walk, dur_s=DUR, sr=SR)

    # Reading A: bit-identical replay under frozen params
    s1, s2 = realize(spec), realize(spec)
    replay_identical = bool(np.array_equal(s1, s2))
    P = analyze(spec)

    # "dissonance scale": choose intervals against THIS timbre's P (timbre-relative, D5)
    ratios = np.linspace(1.0, 2.0, 200)
    curve = F.dissonance_curve(P, ratios)
    # a "strange" scale = pick local-dissonance-maximizing steps (most rough intervals)
    strange_idx = np.argsort(curve)[::-1][:5]
    strange_scale = sorted(float(ratios[i]) for i in strange_idx)

    rep["theta"] = [round(float(x), 3) for x in res.theta]
    rep["replay_bit_identical"] = replay_identical
    rep["features"] = report_features(P)
    rep["dissonance_scale_strange_ratios"] = [round(r, 4) for r in strange_scale]
    rep["strangeness_proxy"] = round(float(F.dissonance(P, strange_scale[0]) + F.harmonicity_match(P)), 4)
    rep["honesty"] = (
        "Replay is bit-identical (Reading A). Per O8, feature VALUES drift 6-9% median "
        "under analyzer-param perturbation on this stochastic timbre (Reading B fails), so "
        "the perceptual targets are NOT analyzer-independent properties. 'strangeness' is a "
        "proxy, never asserted as the felt effect (O1)."
    )

    out = Path(__file__).parent / "witness_report.json"
    out.write_text(json.dumps(rep, indent=2))
    print(json.dumps(rep, indent=2))
    return rep


if __name__ == "__main__":
    main()
