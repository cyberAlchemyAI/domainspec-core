"""O1 dry-run: exercise the listener-study pipeline on SYNTHETIC ratings only.

No felt-match claim. Proves the harness builds a blinded battery and scores a
correlation. The LIVE run (human listeners) is handed off to research-evidence-harness
under the pre-registered criterion.md. Post-O8 caveat: the strangeness proxy rests on
the perceptual floor, whose stability on stochastic timbres is currently UNRESOLVED (O8).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from studio_core.l3_evidence.listener_harness import (build_battery,
                                                      score_correlation)

THETAS = np.array([[8, 10, 0.05], [12, 18, 0.08], [18, 28, 0.12],
                   [26, 40, 0.18], [34, 55, 0.26]], dtype=float)


def main():
    battery = build_battery(THETAS, seed=11, dur_s=0.35)
    vals = [s.objective_value for s in battery]
    rng = np.random.default_rng(99)
    # synthetic listener = proxy + noise (pipeline check, NOT evidence)
    ratings_tracking = list(np.array(vals) + rng.normal(0, 0.02, len(vals)))
    ratings_random = list(rng.uniform(min(vals), max(vals), len(vals)))
    out = {
        "n_stimuli": len(battery),
        "objective_values": [round(v, 4) for v in vals],
        "synthetic_tracking_corr": score_correlation(vals, ratings_tracking),
        "synthetic_random_corr": score_correlation(vals, ratings_random),
        "status": "DRY-RUN ONLY — synthetic ratings, no felt-match claim.",
        "handoff": "live run -> research-evidence-harness under criterion.md",
        "o8_caveat": "proxy rests on a floor whose stochastic-timbre stability is UNRESOLVED (O8 FAIL).",
    }
    p = Path(__file__).parent / "dryrun_report.json"
    p.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main()
