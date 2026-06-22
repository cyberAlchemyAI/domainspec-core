"""Render listenable WAV files from the intent-engine, so the operator can actually HEAR it.

Renders the tuned voices at a longer duration than the search used (the walk is seeded, so a
longer render is just more cycles of the same process). Writes 16-bit WAVs to ./audio/.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from scipy.io import wavfile

from intent_engine.intent.parse import parse_intent
from intent_engine.steer.revise import revise
from intent_engine.tune.fit import fit
from studio_core.l0_signal.gendyn import GendynWalk, RandomWalkBound, render

SR = 22050
LISTEN_S = 3.0
PEAK = 0.5  # keep it gentle on the ears; GENDYN is harsh

OUT = Path(__file__).parent.parent / "audio"
OUT.mkdir(exist_ok=True)


def write(name: str, walk: GendynWalk, dur=LISTEN_S):
    sig = render(walk, dur, SR).astype(np.float32)
    p = float(np.max(np.abs(sig))) or 1.0
    sig = (sig / p) * PEAK
    pcm = (sig * 32767).astype(np.int16)
    path = OUT / name
    wavfile.write(str(path), SR, pcm)
    return path


def main():
    made = []

    # 0) a plain untuned GENDYN voice (the raw engine)
    plain = GendynWalk(12, RandomWalkBound(-1.0, 1.0, "gauss", 0.08, True),
                       RandomWalkBound(8.0, 40.0, "gauss", 1.5, True), 0x5EED)
    made.append(write("00_plain_gendyn.wav", plain))

    # 1) the operator example: "dark violin stochastic synth, bring strangeness"
    spec, _ = parse_intent("dark violin stochastic synth, bring strangeness")
    rs = fit(spec)
    made.append(write("01_dark_violin_strange.wav", rs.walk))

    # 2) same, then "more bite" (steered)
    rs_bite = fit(revise(spec, "more bite"))
    made.append(write("02_more_bite.wav", rs_bite.walk))

    # 3) "darker" instead
    rs_dark = fit(revise(spec, "darker"))
    made.append(write("03_darker.wav", rs_dark.walk))

    print("wrote:")
    for m in made:
        print("  ", m)
    print(f"\nfeatures (operator example): centroid={rs.feats['spectral_centroid']:.0f}Hz "
          f"dissonance={rs.feats['dissonance_minor2']:.2f}")
    print(f"features (more bite):        centroid={rs_bite.feats['spectral_centroid']:.0f}Hz "
          f"dissonance={rs_bite.feats['dissonance_minor2']:.2f}")
    return made


if __name__ == "__main__":
    main()
