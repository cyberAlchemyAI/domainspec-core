"""L3 — the reverse channel (process #10, C12).

Reports what the agent perceives (the L1 numbers), never the adjective. The
human supplies the felt verdict; the meter only says "this is what you hit; judge it."
"""
from __future__ import annotations

import numpy as np

from ..l1_features import features as F
from ..lsigma.spectralize import PartialSet


def report_features(P: PartialSet) -> dict:
    return {
        "n_partials": int(P.partials.shape[0]),
        "f0_hz": None if P.f0 is None else round(P.f0, 2),
        "spectral_centroid_hz": _r(F.spectral_centroid(P)),
        "harmonicity_match": _r(F.harmonicity_match(P)),
        "dissonance_minor2": _r(F.dissonance(P, 16 / 15)),
        "note": "objective readout only — felt effect is the human's verdict (O1).",
    }


def _r(x: float) -> float | None:
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)
