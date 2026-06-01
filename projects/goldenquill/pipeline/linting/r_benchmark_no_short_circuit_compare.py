"""R-BENCHMARK-NO-SHORT-CIRCUIT-COMPARE — AST-lint rule (M1 §5.2.1).

Forbids short-circuit ``==`` / ``!=`` comparisons on ``benchmark_hash``
or ``kfr_hash`` named values inside
``pipeline/logician/benchmarks/**``.  All hash equality MUST go
through :func:`hmac.compare_digest` per the constant-time discipline.

Heuristic — flags any ``ast.Compare`` whose left or right operand is
an ``ast.Name`` with id matching ``benchmark_hash`` / ``kfr_hash`` /
``content_hash``, where the operator is :class:`ast.Eq` or
:class:`ast.NotEq`.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation


_BENCHMARK_TARGET_GLOB = "pipeline/logician/benchmarks/**/*.py"

_HASH_NAMES = frozenset({
    "benchmark_hash",
    "kfr_hash",
    "content_hash",
    "fact_hash",
})


def _is_hash_name(node: ast.AST) -> bool:
    return isinstance(node, ast.Name) and node.id in _HASH_NAMES


def _check_benchmark_no_short_circuit_compare(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        operators = node.ops
        if not any(isinstance(op, (ast.Eq, ast.NotEq)) for op in operators):
            continue
        operands = [node.left] + list(node.comparators)
        if any(_is_hash_name(op) for op in operands):
            yield Violation(
                rule_name="R-BENCHMARK-NO-SHORT-CIRCUIT-COMPARE",
                reason_tag="hash_compared_with_short_circuit_eq",
                file=path,
                line=node.lineno,
                col=node.col_offset,
                message=(
                    "hash-named operand compared with == / != — use "
                    "hmac.compare_digest(...) per M1 §5.2.1 (constant-"
                    "time discipline)"
                ),
            )


BENCHMARK_NO_SHORT_CIRCUIT_COMPARE: Rule = Rule(
    name="R-BENCHMARK-NO-SHORT-CIRCUIT-COMPARE",
    reason_tag="benchmark_no_short_circuit_compare",
    target_glob=_BENCHMARK_TARGET_GLOB,
    check=_check_benchmark_no_short_circuit_compare,
    description=(
        "Forbid == / != on hash-named operands in benchmark "
        "modules; require hmac.compare_digest."
    ),
)


__all__ = ["BENCHMARK_NO_SHORT_CIRCUIT_COMPARE"]
