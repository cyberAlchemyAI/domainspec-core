"""Tiny intermediate module for ``Rule`` / ``Violation``.

Hosting the dataclasses here breaks the import cycle between
:mod:`pipeline.linting.ast_lint` (which builds DEFAULT_RULES at module
load) and the WS-L Slice 4 rule modules (each of which references
``Rule`` to construct its rule-instance constant).  The cycle was
visible only when running ``python -m pipeline.linting.ast_lint`` —
the ``__main__`` double-load surfaces partial-init errors that tests
do not reach because pytest does not exec a ``-m`` reimport.

This module has no third-party imports beyond stdlib, no project
imports, and no module-level side effects beyond declaring the
dataclasses.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable


@dataclass(frozen=True, kw_only=True)
class Violation:
    rule_name: str
    reason_tag: str
    file: Path
    line: int
    col: int
    message: str


@dataclass(frozen=True, kw_only=True)
class Rule:
    name: str
    reason_tag: str
    target_glob: str
    check: Callable[[ast.AST, Path], Iterable[Violation]]
    description: str = ""


__all__ = ["Rule", "Violation"]
