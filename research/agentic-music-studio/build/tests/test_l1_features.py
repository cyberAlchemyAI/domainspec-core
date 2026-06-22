import numpy as np

from studio_core.l1_features import features as F
from studio_core.lsigma.spectralize import PartialSet


def _P(partials, f0=None):
    arr = np.array(partials, dtype=float)
    return PartialSet(partials=arr, f0=f0 if f0 is not None else (float(arr[0, 0]) if len(arr) else None))


def test_centroid_known():
    # two equal-amp partials at 100 and 300 -> centroid 200
    P = _P([[100.0, 1.0], [300.0, 1.0]])
    assert abs(F.spectral_centroid(P) - 200.0) < 1e-6


def test_centroid_reproducible():
    P = _P([[100.0, 1.0], [305.0, 0.4]])
    assert F.spectral_centroid(P) == F.spectral_centroid(P)


def test_dissonance_unison_low_vs_minor_second_high():
    # harmonic-ish template: unison (ratio 1) should be < a dissonant small interval
    P = _P([[200.0, 1.0], [400.0, 0.5], [600.0, 0.33]])
    d_unison = F.dissonance(P, 1.0)
    d_min2 = F.dissonance(P, 16 / 15)  # ~semitone, classically rough
    assert d_min2 > d_unison


def test_dissonance_curve_shape():
    P = _P([[200.0, 1.0], [400.0, 0.5], [600.0, 0.33], [800.0, 0.25]])
    ratios = np.linspace(1.0, 2.0, 25)
    curve = F.dissonance_curve(P, ratios)
    assert curve.shape == (25,)
    # octave (2:1) should be markedly more consonant than the rough quartertone-ish region
    assert curve[-1] < curve[3]


def test_harmonicity_match_perfect_vs_inharmonic():
    f0 = 200.0
    tmpl = F.violin_template()
    harmonic = _P([[f0 * n, tmpl[n - 1]] for n in range(1, 9)], f0=f0)
    inharmonic = _P([[f0 * (n ** 1.4), tmpl[n - 1]] for n in range(1, 9)], f0=f0)
    assert F.harmonicity_match(harmonic, tmpl) < F.harmonicity_match(inharmonic, tmpl)
