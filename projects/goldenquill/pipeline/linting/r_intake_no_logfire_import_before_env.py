"""R-INTAKE-NO-LOGFIRE-IMPORT-BEFORE-ENV — AST-lint rule (M1 §8.4 / §8.4.1).

Validates that no Intake module reaches a Logfire import (direct or
``from logfire import ...``) before the env-var setup has run.  The
heuristic — any module whose first non-trivial import statement at
top-level is ``logfire`` or imports from ``logfire`` is flagged.

Because the Logfire stub is installed at module import time of
:mod:`pipeline.cli.tilth_intake`, the rule additionally flags any
Intake module that imports Logfire BEFORE the bootstrap.  Concrete
heuristic for v0.1: any ``import logfire`` / ``from logfire import``
statement in an Intake module at the top level.

Targets ``pipeline/cli/**/*.py`` and ``pipeline/orchestrator/seats/intake*.py``.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation


_INTAKE_CLI_GLOB = "pipeline/cli/**/*.py"
_INTAKE_SEAT_GLOB = "pipeline/orchestrator/seats/intake*.py"


def _check_intake_no_logfire_import_before_env(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    if not isinstance(tree, ast.Module):
        return

    # Walk top-level statements in declared order; the env-var setup
    # MUST appear before any logfire import.
    saw_env_setup = False
    for stmt in tree.body:
        if isinstance(stmt, ast.Assign):
            # Look for ``os.environ["LOGFIRE_ENABLED"] = "0"`` or
            # ``install_logfire_disabled_stub()``.
            for target in stmt.targets:
                if (
                    isinstance(target, ast.Subscript)
                    and isinstance(target.value, ast.Attribute)
                    and isinstance(target.value.value, ast.Name)
                    and target.value.value.id == "os"
                    and target.value.attr == "environ"
                ):
                    saw_env_setup = True
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            func = stmt.value.func
            if (
                isinstance(func, ast.Name)
                and func.id == "install_logfire_disabled_stub"
            ):
                saw_env_setup = True
            if (
                isinstance(func, ast.Attribute)
                and func.attr == "install_logfire_disabled_stub"
            ):
                saw_env_setup = True
        if isinstance(stmt, ast.Import):
            for alias in stmt.names:
                if alias.name == "logfire" or alias.name.startswith("logfire."):
                    if not saw_env_setup:
                        yield Violation(
                            rule_name="R-INTAKE-NO-LOGFIRE-IMPORT-BEFORE-ENV",
                            reason_tag="logfire_imported_before_env_setup",
                            file=path,
                            line=stmt.lineno,
                            col=stmt.col_offset,
                            message=(
                                f"`import {alias.name}` precedes Logfire "
                                "env-var bootstrap; M1 §8.4 requires "
                                "LOGFIRE_ENABLED=0 set before any "
                                "logfire import"
                            ),
                        )
        if isinstance(stmt, ast.ImportFrom):
            mod = stmt.module or ""
            if mod == "logfire" or mod.startswith("logfire."):
                if not saw_env_setup:
                    yield Violation(
                        rule_name="R-INTAKE-NO-LOGFIRE-IMPORT-BEFORE-ENV",
                        reason_tag="logfire_imported_before_env_setup",
                        file=path,
                        line=stmt.lineno,
                        col=stmt.col_offset,
                        message=(
                            f"`from {mod} import ...` precedes Logfire "
                            "env-var bootstrap; M1 §8.4 requires "
                            "LOGFIRE_ENABLED=0 set before any logfire "
                            "import"
                        ),
                    )


INTAKE_NO_LOGFIRE_IMPORT_BEFORE_ENV: Rule = Rule(
    name="R-INTAKE-NO-LOGFIRE-IMPORT-BEFORE-ENV",
    reason_tag="intake_no_logfire_import_before_env",
    target_glob=_INTAKE_CLI_GLOB,
    check=_check_intake_no_logfire_import_before_env,
    description=(
        "Refuse Intake modules that import logfire before the env-var "
        "bootstrap (M1 §8.4)."
    ),
)

INTAKE_SEAT_NO_LOGFIRE_IMPORT_BEFORE_ENV: Rule = Rule(
    name="R-INTAKE-NO-LOGFIRE-IMPORT-BEFORE-ENV",
    reason_tag="intake_seat_no_logfire_import_before_env",
    target_glob=_INTAKE_SEAT_GLOB,
    check=_check_intake_no_logfire_import_before_env,
    description=(
        "Refuse Intake-seat modules that import logfire before the "
        "env-var bootstrap (M1 §8.4)."
    ),
)


__all__ = [
    "INTAKE_NO_LOGFIRE_IMPORT_BEFORE_ENV",
    "INTAKE_SEAT_NO_LOGFIRE_IMPORT_BEFORE_ENV",
]
