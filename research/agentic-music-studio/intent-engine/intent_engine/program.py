"""Core typed artifacts (see ../MODEL.md). Single-voice v1."""
from __future__ import annotations

from dataclasses import dataclass, field

from studio_core.l0_signal.gendyn import GendynWalk


@dataclass(frozen=True)
class RenderCtx:
    """Frozen render context (F4) — shared by tune and render, or the meter lies."""
    dur_s: float = 0.4
    sr: int = 22050


@dataclass
class FeatureTarget:
    feature: str  # 'spectral_centroid' | 'harmonicity_match' | 'dissonance_minor2'  (live keys, F3)
    op: str       # 'low' (seek target) | 'high' (maximize)
    value: float
    status: str = "grounded"  # 'grounded' | 'proxy'
    weight: float = 1.0       # steering weight — critique shifts this to slide the trade-off (Option 1)


@dataclass
class Program:
    """The human-readable code form. v1: voice + effects + seed. No pattern/scale (G1)."""
    engine: str               # 'gendyn'
    effects: list[str]        # e.g. ['dark', 'violin', 'strange']
    seed: int
    ctx: RenderCtx = field(default_factory=RenderCtx)


@dataclass
class IntentSpec:
    engine: str
    effects: list[str]
    targets: list[FeatureTarget]
    seed: int
    ctx: RenderCtx = field(default_factory=RenderCtx)


@dataclass
class RealizedSpec:
    walk: GendynWalk
    ctx: RenderCtx
    feats: dict
    targets: list[FeatureTarget]
