"""Lsigma — Spectralize: Signal -> PartialSet (the Popper-forced bridge, DD3).

Every L1 feature consumes a partial set P. GENDYN produces none (emergent
spectrum). This module extracts a representative P from realized signal via a
frozen STFT + per-frame peak-pick + cross-frame stability filter.

Determinism: spectralize() is a pure function of (signal, sr, params). Composed
with L0 determinism, P becomes a function of (Spec, seed) alone — closing the
L0->L1 gap. Whether P is *stable* (robust to small param perturbations) is the
open question O8, measured by experiments/o8_spectralize_stability.py.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.signal import find_peaks, stft


@dataclass(frozen=True)
class SpectralizeParams:
    """FROZEN + version-pinned. Changing it is an L1-migration event."""

    n_fft: int = 1024
    hop: int = 256
    window: str = "hann"
    peak_threshold_db: float = -40.0  # relative to per-frame max
    max_partials: int = 24
    min_frame_frac: float = 0.5  # a bin must appear in >= this fraction of frames


@dataclass
class PartialSet:
    partials: np.ndarray  # shape (K, 2): columns = [freq_hz, amp]
    f0: float | None = None

    def freqs(self) -> np.ndarray:
        return self.partials[:, 0] if self.partials.size else np.array([])

    def amps(self) -> np.ndarray:
        return self.partials[:, 1] if self.partials.size else np.array([])


def spectralize(signal: np.ndarray, sr: int, p: SpectralizeParams) -> PartialSet:
    if signal.size == 0 or float(np.max(np.abs(signal))) == 0.0:
        return PartialSet(partials=np.empty((0, 2)), f0=None)

    f, _t, Z = stft(
        signal,
        fs=sr,
        window=p.window,
        nperseg=p.n_fft,
        noverlap=p.n_fft - p.hop,
        boundary=None,
        padded=False,
    )
    mag = np.abs(Z)  # (n_freq, n_frames)
    n_freq, n_frames = mag.shape
    if n_frames == 0:
        return PartialSet(partials=np.empty((0, 2)), f0=None)

    thresh_lin = 10.0 ** (p.peak_threshold_db / 20.0)
    present = np.zeros(n_freq, dtype=int)  # frames each bin is a peak in
    amp_sum = np.zeros(n_freq, dtype=float)

    for j in range(n_frames):
        col = mag[:, j]
        cmax = float(col.max())
        if cmax <= 0:
            continue
        peaks, _props = find_peaks(col, height=cmax * thresh_lin)
        present[peaks] += 1
        amp_sum[peaks] += col[peaks]

    keep = present >= max(1, int(round(p.min_frame_frac * n_frames)))
    idx = np.flatnonzero(keep)
    if idx.size == 0:
        # fall back to the single strongest stable-ish bin so downstream never NaNs blindly
        idx = np.array([int(np.argmax(present))])

    amps = amp_sum[idx] / np.maximum(1, present[idx])
    freqs = f[idx]
    order = np.argsort(amps)[::-1][: p.max_partials]
    freqs, amps = freqs[order], amps[order]
    fre_order = np.argsort(freqs)
    partials = np.column_stack([freqs[fre_order], amps[fre_order]])
    f0 = float(partials[0, 0]) if partials.size else None
    return PartialSet(partials=partials, f0=f0)
