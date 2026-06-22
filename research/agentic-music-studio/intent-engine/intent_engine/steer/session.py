"""L3.1 — render + meter (#10) + show the code. The reverse channel.

Reports the analyzer-independent darkness reading AND the proxy strangeness, each honestly
labelled (F2) — never asserts a felt result.
"""
from __future__ import annotations

import numpy as np

from studio_core.l0_signal.gendyn import render
from studio_core.l1_features import features as F
from studio_core.lsigma.spectralize import SpectralizeParams, spectralize

from ..codegen.dsl import unparse
from ..program import Program, RealizedSpec

FROZEN = SpectralizeParams()


def readout(rs: RealizedSpec) -> dict:
    sig = render(rs.walk, rs.ctx.dur_s, rs.ctx.sr)
    P = spectralize(sig, rs.ctx.sr, FROZEN)
    centroid = F.moment_centroid(sig, rs.ctx.sr)
    diss = F.dissonance(P, 16 / 15)
    return {
        "spectral_centroid_hz": _r(centroid),
        "spectral_centroid_note": "analyzer-independent (Reading-B); felt-match = O1, open (F2)",
        "dissonance_minor2": _r(diss),
        "dissonance_note": "proxy — judge it; Reading-B unresolved on GENDYN until Spectralize-v2",
        "harmonicity_match": _r(F.harmonicity_match(P)),
    }


def show(rs: RealizedSpec, prog: Program) -> str:
    rep = readout(rs)
    lines = ["--- meter (objective readout; you supply the felt verdict) ---"]
    for k, v in rep.items():
        lines.append(f"  {k}: {v}")
    lines.append("--- code (read it; you can hand-edit it) ---")
    lines.append(unparse(prog))
    return "\n".join(lines)


def _r(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)
