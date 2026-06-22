"""IntentSpec -> Program (DSL text). DETERMINISTIC TRANSLITERATION — zero generative
intelligence (the engineering is the L1 search, MODEL I2). Every Program field is sourced
from the IntentSpec; nothing is invented (I3/G5)."""
from __future__ import annotations

from ..program import IntentSpec, Program
from .dsl import unparse


def author(ispec: IntentSpec) -> tuple[str, Program]:
    prog = Program(engine=ispec.engine, effects=list(ispec.effects),
                   seed=ispec.seed, ctx=ispec.ctx)  # every field from ispec — none invented
    return unparse(prog), prog
