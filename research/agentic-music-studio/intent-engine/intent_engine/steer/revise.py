"""L3.2 — closed critique lexicon -> typed Edit on a FeatureTarget (G-critique, Option 1).

Each entry: (feature, field, delta) where field is 'weight' (slide the trade-off — the steering
knob) or 'value' (move a setpoint). Unknown critique -> ask (never guess). Every edit is a diff
on the IntentSpec, then re-tuned via L1.
"""
from __future__ import annotations

from dataclasses import replace

from ..program import FeatureTarget, IntentSpec

# critique -> (feature, field, delta)
CRITIQUE_LEXICON = {
    "more bite": ("dissonance_minor2", "weight", +1.5),   # raise strangeness weight -> trade darkness for bite
    "less bite": ("dissonance_minor2", "weight", -1.0),
    "darker": ("spectral_centroid", "value", -120.0),     # move the dark setpoint down
    "brighter": ("spectral_centroid", "value", +120.0),
    "too muddy": ("spectral_centroid", "value", +150.0),
}


class UnknownCritique(Exception):
    pass


def revise(ispec: IntentSpec, critique: str) -> IntentSpec:
    key = critique.strip().lower()
    if key not in CRITIQUE_LEXICON:
        raise UnknownCritique(
            f"'{critique}' not in the v1 critique lexicon {sorted(CRITIQUE_LEXICON)}; "
            f"which target did you mean (spectral_centroid / dissonance_minor2)?"
        )
    feature, field, delta = CRITIQUE_LEXICON[key]
    new_targets, hit = [], False
    for t in ispec.targets:
        if t.feature == feature:
            cur = getattr(t, field)
            new_targets.append(replace(t, **{field: max(0.0, cur + delta) if field == "weight" else cur + delta}))
            hit = True
        else:
            new_targets.append(t)
    if not hit:
        status = "proxy" if feature == "dissonance_minor2" else "grounded"
        op = "high" if feature == "dissonance_minor2" else "low"
        base = FeatureTarget(feature, op, 0.0, status)
        new_targets.append(replace(base, **{field: max(0.0, delta) if field == "weight" else delta}))
    return replace(ispec, targets=new_targets)
