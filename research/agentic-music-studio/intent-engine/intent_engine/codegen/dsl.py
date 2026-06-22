"""The v1 DSL: `voice gendyn <effect>*` + `seed <int>`. No pattern/scale (G1)."""
from __future__ import annotations

from ..program import Program, RenderCtx

DEFAULT_SEED = 0x5EED


def parse(text: str) -> Program:
    engine = None
    effects: list[str] = []
    seed = None
    for raw in text.strip().splitlines():
        toks = raw.split()
        if not toks:
            continue
        head = toks[0]
        if head in ("pattern", "scale"):
            raise ValueError(f"'{head}' is not in v1 (single-voice timbre; rhythm/pitch deferred — G1)")
        if head == "voice":
            if len(toks) < 2:
                raise ValueError("voice needs an engine")
            engine, effects = toks[1], toks[2:]
            if engine != "gendyn":
                raise ValueError(f"v1 engine must be 'gendyn', got '{engine}'")
        elif head == "seed":
            seed = int(toks[1], 0)
        else:
            raise ValueError(f"unknown DSL line: '{head}'")
    if engine is None:
        raise ValueError("no `voice` line")
    if seed is None:
        seed = DEFAULT_SEED  # default + (caller may warn)
    return Program(engine=engine, effects=effects, seed=seed, ctx=RenderCtx())


def unparse(p: Program) -> str:
    line = f"voice {p.engine}" + ("" if not p.effects else " " + " ".join(p.effects))
    return f"{line}\nseed {hex(p.seed)}"
