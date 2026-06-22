"""SWU-A honesty gate (F1): does the multitaper moment_centroid actually clear EPS on GENDYN?

The Round-2 refresh refused to ASSUME "<0.05 drift on GENDYN" — this measures it.
- moment_centroid's analyzer params are (nw, k). Perturb them on a fixed GENDYN signal,
  measure relative centroid drift (Reading-B = analyzer-independence).
- Compare against the OLD peak-pick centroid under the SpectralizeParams grid (the 6.1% path).
- Additive control for reference.
PASS iff moment_centroid drift median < EPS (0.05). FAIL is a banked finding, not a silent pass.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from studio_core.l0_signal.engine import AdditiveVoice
from studio_core.l0_signal.gendyn import GendynWalk, RandomWalkBound, render
from studio_core.l1_features import features as F
from studio_core.lsigma.spectralize import SpectralizeParams, spectralize

EPS = 0.05
SR, DUR = 22050, 0.4


def gwalk(seed):
    return GendynWalk(12, RandomWalkBound(-1.0, 1.0, "gauss", 0.08, True),
                      RandomWalkBound(8.0, 40.0, "gauss", 1.5, True), seed)


def rel(a, b):
    if a is None or b is None or np.isnan(a) or np.isnan(b) or a == 0:
        return float("nan")
    return abs(b - a) / abs(a)


def moment_drift(sig):
    ref = F.moment_centroid(sig, SR, nw=4.0, k=7)
    drifts = []
    for nw in (3.0, 4.0, 5.0):
        for k in (5, 7, 9):
            if (nw, k) == (4.0, 7):
                continue
            drifts.append(rel(ref, F.moment_centroid(sig, SR, nw=nw, k=k)))
    return ref, np.array(drifts, dtype=float)


def peakpick_drift(sig):
    """The OLD path: peak-pick centroid under the SpectralizeParams grid (reproduces O8)."""
    base = SpectralizeParams()
    ref = F.spectral_centroid(spectralize(sig, SR, base))
    drifts = []
    for n_fft in (512, 1024, 2048):
        for hop in (128, 256, 512):
            for thr in (-50.0, -40.0, -30.0):
                if (n_fft, hop, thr) == (base.n_fft, base.hop, base.peak_threshold_db):
                    continue
                p = SpectralizeParams(n_fft=n_fft, hop=min(hop, n_fft // 2), peak_threshold_db=thr)
                drifts.append(rel(ref, F.spectral_centroid(spectralize(sig, SR, p))))
    return ref, np.array(drifts, dtype=float)


def main():
    gen = render(gwalk(7), DUR, SR)
    add = AdditiveVoice(((300.0, 1.0), (600.0, 0.6), (900.0, 0.3))).render(DUR, SR)

    g_ref, g_moment = moment_drift(gen)
    g_pref, g_peak = peakpick_drift(gen)
    a_ref, a_moment = moment_drift(add)

    # determinism: same signal -> identical moment centroid
    determ = F.moment_centroid(gen, SR) == F.moment_centroid(gen, SR)

    moment_med = float(np.nanmedian(g_moment))
    moment_max = float(np.nanmax(g_moment))
    peak_med = float(np.nanmedian(g_peak))
    passed = (moment_med < EPS) and determ

    report = {
        "eps": EPS,
        "determinism_identical": bool(determ),
        "gendyn_moment_centroid_hz": round(g_ref, 2),
        "gendyn_moment_drift_median": round(moment_med, 4),
        "gendyn_moment_drift_max": round(moment_max, 4),
        "gendyn_OLD_peakpick_drift_median": round(peak_med, 4),
        "additive_moment_drift_median": round(float(np.nanmedian(a_moment)), 4),
        "verdict": "PASS" if passed else "FAIL",
        "reading": "B (analyzer-independence). Felt-match = O1, NOT established here.",
        "interpretation": (
            f"moment_centroid drift {moment_med:.3f} < EPS {EPS} on GENDYN -> the darkness reading is "
            f"analyzer-independent (vs the old peak-pick {peak_med:.3f}). L-pre honesty gate PASSES."
            if passed else
            f"moment_centroid drift {moment_med:.3f} >= EPS {EPS} -> escalate (reassignment / longer "
            f"averaging). BANKED finding; L-pre does NOT pass as-is."
        ),
    }
    out = Path(__file__).parent / "o8_v2_centroid.json"
    out.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    main()
