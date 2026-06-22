"""L1 — the perceptual-feature floor (build-from-owned, Lakatos).

Each feature is a pure function over a PartialSet. Owners:
- spectral_centroid: MPEG-7 AudioSpectrumCentroid variant / Beauchamp lineage.
- dissonance: Plomp & Levelt 1965 + Sethares 1998 (C3/D5).
- harmonicity_match: AudioCommons-style timbre-template distance (violin template
  is SYNTHETIC here — recorded assumption, see violin_template()).
"""
from __future__ import annotations

import numpy as np
from scipy.signal.windows import dpss

from ..lsigma.spectralize import PartialSet


def spectral_centroid(P: PartialSet) -> float:
    """Amplitude-weighted mean partial frequency (Hz). Range [0, sr/2]."""
    a = P.amps()
    if a.size == 0 or a.sum() == 0:
        return float("nan")
    return float(np.sum(P.freqs() * a) / np.sum(a))


def _pair_dissonance(f1: float, f2: float, a1: float, a2: float) -> float:
    """Sethares (1998) parametric sensory-dissonance of one partial pair."""
    if f1 == f2:
        return 0.0
    fmin = min(f1, f2)
    s = 0.24 / (0.0207 * fmin + 18.96)
    b1, b2 = 3.5, 5.75
    x = abs(f2 - f1)
    loudness = min(a1, a2)  # Sethares uses the quieter partial
    return loudness * (np.exp(-b1 * s * x) - np.exp(-b2 * s * x))


def dissonance(P: PartialSet, interval_ratio: float) -> float:
    """Sensory dissonance of P sounded against a copy transposed by interval_ratio.

    Combined spectrum = P ∪ (interval_ratio * P); sum pairwise dissonance.
    """
    f = P.freqs()
    a = P.amps()
    if f.size == 0:
        return 0.0
    freqs = np.concatenate([f, f * interval_ratio])
    amps = np.concatenate([a, a])
    total = 0.0
    k = len(freqs)
    for i in range(k):
        for j in range(i + 1, k):
            total += _pair_dissonance(freqs[i], freqs[j], amps[i], amps[j])
    norm = float(np.sum(a) ** 2) or 1.0
    return float(total / norm)


def dissonance_curve(P: PartialSet, ratios: np.ndarray) -> np.ndarray:
    return np.array([dissonance(P, float(r)) for r in ratios])


def violin_template(n_harmonics: int = 16) -> np.ndarray:
    """SYNTHETIC violin-ish amplitude profile over harmonics 1..n.

    ASSUMPTION (recorded): 1/n rolloff with a mild formant bump near harmonics
    2-4. A measured violin spectrum should replace this before any O1 claim.
    """
    n = np.arange(1, n_harmonics + 1)
    amp = 1.0 / n
    amp *= 1.0 + 0.6 * np.exp(-((n - 3.0) ** 2) / 4.0)  # formant bump
    return amp / amp.max()


def harmonicity_match(P: PartialSet, template: np.ndarray | None = None) -> float:
    """Distance in [0, 1] of P's harmonic amplitude profile to a template.

    0 = perfect match. Resamples P onto a harmonic grid built on its own f0 and
    compares (cosine distance). Deterministic.
    """
    if template is None:
        template = violin_template()
    f = P.freqs()
    a = P.amps()
    if f.size == 0 or P.f0 in (None, 0):
        return 1.0
    f0 = P.f0
    k = len(template)
    grid = np.zeros(k)
    for fi, ai in zip(f, a):
        h = int(round(fi / f0))
        if 1 <= h <= k:
            grid[h - 1] += ai
    if grid.sum() == 0:
        return 1.0
    grid = grid / np.linalg.norm(grid)
    tmpl = template / np.linalg.norm(template)
    cos = float(np.dot(grid, tmpl))
    return float(1.0 - max(0.0, min(1.0, cos)))


# --- L-pre (F1/F3 from the Spectralize refine): full-spectrum, multitaper centroid ---
# This BYPASSES the peak-picked PartialSet. The O8 wobble was in the peak-pick; computing
# the centroid as a moment over a low-variance (multitaper) magnitude spectrum is the F3 fix.
# Owner-note: upstream studio-core addition (intent-engine SWU-A).

def multitaper_magnitude(signal: np.ndarray, sr: int, nw: float = 4.0, k: int = 7):
    """Thomson multitaper magnitude spectrum: average |FFT| over K DPSS tapers.

    Returns (freqs, mag). Averaging K near-independent tapered estimates is the
    variance fix (Welch/Thomson) that makes a stochastic-signal spectrum stop jittering.
    """
    n = len(signal)
    if n == 0:
        return np.array([]), np.array([])
    k = min(k, max(1, int(2 * nw) - 1))
    tapers = dpss(n, nw, k)  # (k, n)
    freqs = np.fft.rfftfreq(n, 1.0 / sr)
    power = np.zeros(freqs.shape[0])
    for taper in tapers:
        spec = np.fft.rfft(signal * taper)
        power += np.abs(spec) ** 2
    power /= k
    return freqs, np.sqrt(power)


def moment_centroid(signal: np.ndarray, sr: int, nw: float = 4.0, k: int = 7) -> float:
    """Spectral centroid (Hz) as the energy-weighted mean over the FULL multitaper
    magnitude spectrum — no peak-pick. The L-pre 'darkness' estimator."""
    freqs, mag = multitaper_magnitude(signal, sr, nw, k)
    s = float(mag.sum())
    if s == 0.0 or freqs.size == 0:
        return float("nan")
    return float(np.sum(freqs * mag) / s)
