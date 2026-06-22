"""O8 — is Spectralize reproducible AND stable on stochastic GENDYN timbres?

This is the L0 STOP-GATE. Three tests:
  1. re-render identity      : same (walk,seed) -> identical signal -> identical features (MUST pass).
  2. seed sweep              : characterize the (expected) spread across seeds.
  3. param-perturbation      : hold (walk,seed) fixed, vary SpectralizeParams over a grid;
                               measure |Δfeature|/feature. THIS IS O8.

Pass criterion: test 1 exact; test 3 median relative drift < EPS for centroid AND dissonance.
Fail => floor degrades to signal-only on stochastic timbres (model's own collapse-test).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from studio_core.l0_signal.gendyn import GendynWalk, RandomWalkBound, render
from studio_core.l1_features import features as F
from studio_core.lsigma.spectralize import SpectralizeParams, spectralize

EPS = 0.05  # relative-drift pass threshold (recorded decision)
SR = 22050
DUR = 0.4


def walk(seed):
    return GendynWalk(12,
                      RandomWalkBound(-1.0, 1.0, "gauss", 0.08, True),
                      RandomWalkBound(8.0, 40.0, "gauss", 1.5, True),
                      seed)


def feats(sig, p):
    P = spectralize(sig, SR, p)
    return {
        "centroid": F.spectral_centroid(P),
        "dissonance": F.dissonance(P, 16 / 15),
        "n_partials": P.partials.shape[0],
    }


def rel(a, b):
    if a is None or b is None or np.isnan(a) or np.isnan(b) or a == 0:
        return float("nan")
    return abs(b - a) / abs(a)


def main():
    base_p = SpectralizeParams()
    report = {"eps": EPS}

    # --- Test 1: re-render identity ---
    s1 = render(walk(7), DUR, SR)
    s2 = render(walk(7), DUR, SR)
    identical = bool(np.array_equal(s1, s2))
    f1, f2 = feats(s1, base_p), feats(s2, base_p)
    report["test1_rerender_identity"] = {
        "signal_identical": identical,
        "features_identical": f1 == f2,
    }

    # --- Test 2: seed sweep (descriptive) ---
    seeds = range(20)
    cents = [feats(render(walk(s), DUR, SR), base_p)["centroid"] for s in seeds]
    diss = [feats(render(walk(s), DUR, SR), base_p)["dissonance"] for s in seeds]
    report["test2_seed_sweep"] = {
        "centroid_mean": float(np.nanmean(cents)),
        "centroid_cv": float(np.nanstd(cents) / np.nanmean(cents)),
        "dissonance_mean": float(np.nanmean(diss)),
        "dissonance_cv": float(np.nanstd(diss) / (np.nanmean(diss) or 1)),
    }

    # --- Test 3: param-perturbation sensitivity (THE O8 TEST) ---
    fixed = render(walk(7), DUR, SR)
    ref = feats(fixed, base_p)
    grid = []
    for n_fft in (512, 1024, 2048):
        for hop in (128, 256, 512):
            for thr in (-50.0, -40.0, -30.0):
                if (n_fft, hop, thr) == (base_p.n_fft, base_p.hop, base_p.peak_threshold_db):
                    continue
                p = SpectralizeParams(n_fft=n_fft, hop=min(hop, n_fft // 2),
                                      peak_threshold_db=thr)
                fp = feats(fixed, p)
                grid.append({
                    "n_fft": n_fft, "hop": hop, "thr_db": thr,
                    "centroid_drift": rel(ref["centroid"], fp["centroid"]),
                    "dissonance_drift": rel(ref["dissonance"], fp["dissonance"]),
                })
    c_drift = np.array([g["centroid_drift"] for g in grid], dtype=float)
    d_drift = np.array([g["dissonance_drift"] for g in grid], dtype=float)
    report["test3_param_perturbation"] = {
        "ref_centroid": ref["centroid"], "ref_dissonance": ref["dissonance"],
        "ref_n_partials": ref["n_partials"],
        "centroid_drift_median": float(np.nanmedian(c_drift)),
        "centroid_drift_max": float(np.nanmax(c_drift)),
        "dissonance_drift_median": float(np.nanmedian(d_drift)),
        "dissonance_drift_max": float(np.nanmax(d_drift)),
        "grid_size": len(grid),
    }

    # --- Control: same perturbation on an ADDITIVE voice (should be far more stable) ---
    from studio_core.l0_signal.engine import AdditiveVoice
    add = AdditiveVoice(((300.0, 1.0), (600.0, 0.6), (900.0, 0.3))).render(DUR, SR)
    add_ref = feats(add, base_p)
    add_c, add_d = [], []
    for n_fft in (512, 1024, 2048):
        for thr in (-50.0, -40.0, -30.0):
            p = SpectralizeParams(n_fft=n_fft, hop=n_fft // 4, peak_threshold_db=thr)
            fp = feats(add, p)
            add_c.append(rel(add_ref["centroid"], fp["centroid"]))
            add_d.append(rel(add_ref["dissonance"], fp["dissonance"]))
    report["control_additive_voice"] = {
        "centroid_drift_median": float(np.nanmedian(add_c)),
        "dissonance_drift_median": float(np.nanmedian(add_d)),
    }

    # --- Verdict ---
    t1 = report["test1_rerender_identity"]["signal_identical"] and \
        report["test1_rerender_identity"]["features_identical"]
    c_med = report["test3_param_perturbation"]["centroid_drift_median"]
    d_med = report["test3_param_perturbation"]["dissonance_drift_median"]
    t3 = (c_med < EPS) and (d_med < EPS)
    report["verdict"] = {
        "test1_pass": bool(t1),
        "test3_pass": bool(t3),
        "O8": "PASS" if (t1 and t3) else "FAIL",
        "interpretation": (
            "Spectralize reproducible AND stable on GENDYN -> L1 floor holds."
            if (t1 and t3) else
            "Param drift exceeds EPS on GENDYN -> P is analyzer-dependent; closed floor "
            "degrades to signal-only for stochastic timbres (model collapse-test fires). "
            "L0 STOP-GATE: bank this finding; do not promote L1 on stochastic voices as-is."
        ),
    }

    out = Path(__file__).parent / "o8_report.json"
    out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report["verdict"], indent=2))
    print("centroid drift  median/max:",
          report["test3_param_perturbation"]["centroid_drift_median"],
          report["test3_param_perturbation"]["centroid_drift_max"])
    print("dissonance drift median/max:",
          report["test3_param_perturbation"]["dissonance_drift_median"],
          report["test3_param_perturbation"]["dissonance_drift_max"])
    print("control additive centroid drift median:",
          report["control_additive_voice"]["centroid_drift_median"])
    print("wrote", out)
    return report


if __name__ == "__main__":
    main()
