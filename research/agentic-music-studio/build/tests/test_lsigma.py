import numpy as np

from studio_core.l0_signal.engine import AdditiveVoice
from studio_core.lsigma.spectralize import SpectralizeParams, spectralize


def test_spectralize_pure():
    sig = AdditiveVoice(((220.0, 1.0), (440.0, 0.5), (660.0, 0.25))).render(0.5, 22050)
    p = SpectralizeParams()
    a = spectralize(sig, 22050, p)
    b = spectralize(sig, 22050, p)
    assert np.array_equal(a.partials, b.partials)


def test_spectralize_recovers_additive_partials():
    # the analyzable control: P should recover the known partials within ~1 bin.
    sig = AdditiveVoice(((300.0, 1.0), (600.0, 0.6), (900.0, 0.3))).render(0.5, 22050)
    P = spectralize(sig, 22050, SpectralizeParams())
    freqs = sorted(P.freqs())
    assert len(freqs) >= 3
    res = 22050 / 1024  # ~21.5 Hz/bin
    for target in (300.0, 600.0, 900.0):
        assert min(abs(f - target) for f in freqs) <= 2 * res


def test_silent_signal_empty():
    P = spectralize(np.zeros(8192, dtype=np.float32), 22050, SpectralizeParams())
    assert P.partials.shape[0] == 0
