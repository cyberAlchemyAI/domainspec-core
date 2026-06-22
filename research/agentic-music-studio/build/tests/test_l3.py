import numpy as np

from studio_core.l0_signal.engine import AdditiveVoice
from studio_core.l3_evidence.listener_harness import (build_battery,
                                                      score_correlation)
from studio_core.l3_evidence.meter import report_features
from studio_core.lsigma.spectralize import SpectralizeParams, spectralize


def test_meter_reports_numbers_not_adjectives():
    sig = AdditiveVoice(((220.0, 1.0), (440.0, 0.5))).render(0.4, 22050)
    P = spectralize(sig, 22050, SpectralizeParams())
    rep = report_features(P)
    assert "spectral_centroid_hz" in rep and "note" in rep
    assert "strange" not in str(rep).lower().replace("o1", "")  # no felt-adjective asserted


def test_correlation_pipeline_on_synthetic_ratings():
    thetas = [[8, 10, 0.05], [15, 25, 0.1], [25, 40, 0.2], [35, 55, 0.28]]
    battery = build_battery(np.array(thetas, dtype=float), seed=3, dur_s=0.3)
    vals = [s.objective_value for s in battery]
    # synthetic "listener" perfectly tracks the proxy -> rho ~ 1 (pipeline sanity only)
    ratings = list(vals)
    out = score_correlation(vals, ratings)
    assert out["n"] == 4 and out["spearman_rho"] > 0.99
