"""Closed-vocabulary intent resolver (G8): intent text -> IntentSpec + unknown words.

NOT an open-vocabulary parser — unknown adjectives are flagged, never guessed. Open intent
is the deferred LLM front-end's job (DD2).
"""
from __future__ import annotations

import re

from ..program import IntentSpec, RenderCtx
from .vocabulary import FILLER, VOCAB

DEFAULT_SEED = 0x5EED


def parse_intent(text: str) -> tuple[IntentSpec, list[str]]:
    words = re.findall(r"[a-z]+", text.lower())
    engine = "gendyn"
    effects: list[str] = []
    targets = []
    unknown: list[str] = []
    seen = set()
    for w in words:
        if w in VOCAB:
            kind, val = VOCAB[w]
            if kind == "engine":
                engine = val
            elif w not in seen:
                effects.append(w)
                targets.append(val)
                seen.add(w)
        elif w in FILLER:
            continue
        else:
            unknown.append(w)
    spec = IntentSpec(engine=engine, effects=effects, targets=targets,
                      seed=DEFAULT_SEED, ctx=RenderCtx())
    return spec, unknown
