"""Program -> IntentSpec (resolve effects to targets); + an untuned pre-L1 render (m1)."""
from __future__ import annotations

import numpy as np

from studio_core.l0_signal.gendyn import GendynWalk, RandomWalkBound, render

from ..intent.vocabulary import VOCAB
from ..program import IntentSpec, Program


def compile_program(prog: Program) -> IntentSpec:
    engine = prog.engine
    targets = []
    for e in prog.effects:
        if e not in VOCAB:
            raise ValueError(f"unknown effect '{e}' (not in governed vocabulary)")
        kind, val = VOCAB[e]
        if kind == "engine":
            engine = val
        else:
            targets.append(val)
    return IntentSpec(engine=engine, effects=prog.effects, targets=targets,
                      seed=prog.seed, ctx=prog.ctx)


def _default_walk(seed: int) -> GendynWalk:
    return GendynWalk(12, RandomWalkBound(-1.0, 1.0, "gauss", 0.08, True),
                      RandomWalkBound(8.0, 40.0, "gauss", 1.5, True), seed)


def render_untuned(prog: Program) -> np.ndarray:
    """Pre-L1: a DEFAULT (untuned) GENDYN voice — makes *a* sound, not the tuned target (m1)."""
    return render(_default_walk(prog.seed), prog.ctx.dur_s, prog.ctx.sr)
