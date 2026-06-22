"""L3.3 (NEW, G7) — the human hand-edits the shown DSL text → re-parse → re-render.

The write-side of "the human directs": the code is a first-class editable input, not just a
menu to nudge. A hand-edit round-trips parse → compile → render.
"""
from __future__ import annotations

import numpy as np

from ..codegen.compile import compile_program, render_untuned
from ..codegen.dsl import parse
from ..program import IntentSpec, Program


def apply_edit(edited_text: str) -> tuple[Program, IntentSpec, np.ndarray]:
    prog = parse(edited_text)                 # human's edited code
    ispec = compile_program(prog)             # resolve effects
    sig = render_untuned(prog)                # untuned render (tune via fit if targets present)
    return prog, ispec, sig
