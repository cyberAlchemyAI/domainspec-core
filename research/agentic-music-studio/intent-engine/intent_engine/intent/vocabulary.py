"""The governed effect vocabulary (a resolver, not an open parser — G8).

Each effect resolves either to the engine choice or to a FeatureTarget with a CONCRETE value
(G9). Live keys only (F3): spectral_centroid / harmonicity_match / dissonance_minor2.
Extensible via the contrastive gate (governance, not a primitive layer — O6).
"""
from __future__ import annotations

from ..program import FeatureTarget

# effect_word -> ('engine', name) | ('target', FeatureTarget)
VOCAB: dict[str, tuple] = {
    "stochastic": ("engine", "gendyn"),
    # darkness: low centroid (moment_centroid baseline ~790 Hz on GENDYN; push below 500). grounded.
    "dark": ("target", FeatureTarget("spectral_centroid", "low", 500.0, "grounded")),
    "darkness": ("target", FeatureTarget("spectral_centroid", "low", 500.0, "grounded")),
    # violin-ness: low harmonicity match-distance (0 = perfect). grounded.
    "violin": ("target", FeatureTarget("harmonicity_match", "low", 0.15, "grounded")),
    # strangeness: maximize dissonance — PROXY (felt-match = O1, unverified). Reading-B also open on GENDYN.
    "strange": ("target", FeatureTarget("dissonance_minor2", "high", 0.0, "proxy")),
    "strangeness": ("target", FeatureTarget("dissonance_minor2", "high", 0.0, "proxy")),
}

# words the resolver knows to ignore (closed-vocabulary v1)
FILLER = {"synth", "bring", "a", "some", "the", "to", "listener", "then", "use", "and", "of"}
