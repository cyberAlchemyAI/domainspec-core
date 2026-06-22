"""The one shared Spec (D1) — every interface edits this; realize() is deterministic."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .l0_signal.gendyn import GendynWalk, render
from .lsigma.spectralize import PartialSet, SpectralizeParams, spectralize

FROZEN_SPECTRALIZE = SpectralizeParams()  # the version-pinned analyzer


@dataclass
class FeatureTarget:
    feature: str  # 'spectral_centroid' | 'dissonance' | 'harmonicity_match'
    op: str       # 'low' | 'high' | 'band'
    value: float


@dataclass
class Spec:
    l0: GendynWalk
    dur_s: float = 0.5
    sr: int = 22050
    l1_targets: list[FeatureTarget] = field(default_factory=list)
    l2_effects: list = field(default_factory=list)
    labels: list = field(default_factory=list)

    @property
    def seed(self) -> int:
        return self.l0.seed


def realize(spec: Spec) -> np.ndarray:
    """Deterministic: same Spec -> bit-identical signal."""
    return render(spec.l0, spec.dur_s, spec.sr)


def analyze(spec: Spec, params: SpectralizeParams = FROZEN_SPECTRALIZE) -> PartialSet:
    return spectralize(realize(spec), spec.sr, params)
