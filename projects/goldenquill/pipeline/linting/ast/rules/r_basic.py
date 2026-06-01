from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation

# ---------------------------------------------------------------------------
# R1 — LOGICIAN_IMPORT_BAN
# ---------------------------------------------------------------------------

_LLM_PROVIDER_ROOTS: tuple[str, ...] = (
    "anthropic",
    "openai",
    "groq",
    "google.generativeai",
    "ollama",
)

def _is_banned_provider(module: str) -> bool:
    for root in _LLM_PROVIDER_ROOTS:
        if module == root or module.startswith(root + "."):
            return True
    return False

def _check_logician_import_ban(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _is_banned_provider(alias.name):
                    yield Violation(
                        rule_name="LOGICIAN_IMPORT_BAN",
                        reason_tag="logician_imports_llm_client",
                        file=path,
                        line=node.lineno,
                        col=node.col_offset,
                        message=(
                            f"Logician module must not import LLM client "
                            f"{alias.name!r}"
                        ),
                    )
        elif isinstance(node, ast.ImportFrom):
            if node.module and _is_banned_provider(node.module):
                yield Violation(
                    rule_name="LOGICIAN_IMPORT_BAN",
                    reason_tag="logician_imports_llm_client",
                    file=path,
                    line=node.lineno,
                    col=node.col_offset,
                    message=(
                        f"Logician module must not import LLM client "
                        f"{node.module!r}"
                    ),
                )

LOGICIAN_IMPORT_BAN = Rule(
    name="LOGICIAN_IMPORT_BAN",
    reason_tag="logician_imports_llm_client",
    target_glob="pipeline/logician/**/*.py",
    check=_check_logician_import_ban,
    description=(
        "No module under pipeline/logician/ may import an LLM client SDK "
        "(anthropic, openai, groq, google.generativeai, ollama). "
        "Blueprint: section_04_logician.md §3.1, §7.4."
    ),
)


# ---------------------------------------------------------------------------
# R2 — LOOP_LOGICIAN_BAN
# ---------------------------------------------------------------------------

def _check_loop_logician_ban(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    """Only the public surface `from pipeline.logician import X` is allowed."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("pipeline.logician."):
                    yield Violation(
                        rule_name="LOOP_LOGICIAN_BAN",
                        reason_tag="loop_imports_logician_internal",
                        file=path,
                        line=node.lineno,
                        col=node.col_offset,
                        message=(
                            f"Loop must import only the public logician "
                            f"API; got {alias.name!r}"
                        ),
                    )
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if mod.startswith("pipeline.logician."):
                yield Violation(
                    rule_name="LOOP_LOGICIAN_BAN",
                    reason_tag="loop_imports_logician_internal",
                    file=path,
                    line=node.lineno,
                    col=node.col_offset,
                    message=(
                        f"Loop must import only the public logician API; "
                        f"got {mod!r}"
                    ),
                )

LOOP_LOGICIAN_BAN = Rule(
    name="LOOP_LOGICIAN_BAN",
    reason_tag="loop_imports_logician_internal",
    target_glob="pipeline/loop/**/*.py",
    check=_check_loop_logician_ban,
    description=(
        "Modules under pipeline/loop/ may only import from the public "
        "pipeline.logician surface — never reach into internal submodules."
    ),
)


# ---------------------------------------------------------------------------
# R3 — LOGICIAN_OPEN_BAN
# ---------------------------------------------------------------------------

_VAULT_PATH_PREFIXES: tuple[str, ...] = ("orgs/", "vault_shared/")

def _check_logician_open_ban(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Name) and func.id == "open"):
            continue
        if not node.args:
            continue
        first = node.args[0]
        if not (isinstance(first, ast.Constant) and isinstance(first.value, str)):
            continue
        literal = first.value
        if any(literal.startswith(p) for p in _VAULT_PATH_PREFIXES):
            yield Violation(
                rule_name="LOGICIAN_OPEN_BAN",
                reason_tag="logician_opens_vault_path",
                file=path,
                line=node.lineno,
                col=node.col_offset,
                message=(
                    f"Logician module must not open vault path {literal!r} "
                    f"directly — route via vault broker"
                ),
            )

LOGICIAN_OPEN_BAN = Rule(
    name="LOGICIAN_OPEN_BAN",
    reason_tag="logician_opens_vault_path",
    target_glob="pipeline/logician/**/*.py",
    check=_check_logician_open_ban,
    description=(
        "No module under pipeline/logician/ may call open() on a literal "
        "'orgs/...' or 'vault_shared/...' path. Blueprint: "
        "section_04_logician.md §7.6."
    ),
)


# ---------------------------------------------------------------------------
# R4 — SCOUT_NO_SETATTR_OPERATOR_DECISION
# ---------------------------------------------------------------------------

_OP_DECISION_ATTR = "operator_decision"

def _check_scout_no_setattr_operator_decision(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    if path.name == "review_stage.py":
        return

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            is_setattr_builtin = (
                isinstance(node.func, ast.Name) and node.func.id == "setattr"
            )
            is_setattr_dunder = (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "__setattr__"
            )
            if is_setattr_builtin or is_setattr_dunder:
                if len(node.args) >= 2:
                    name_arg = node.args[1]
                    if (
                        isinstance(name_arg, ast.Constant)
                        and isinstance(name_arg.value, str)
                        and name_arg.value == _OP_DECISION_ATTR
                    ):
                        yield Violation(
                            rule_name="SCOUT_NO_SETATTR_OPERATOR_DECISION",
                            reason_tag="scout_setattr_operator_decision_outside_review_stage",
                            file=path,
                            line=node.lineno,
                            col=node.col_offset,
                            message=(
                                "operator_decision may only be written by "
                                "pipeline/scout/review_stage.py"
                            ),
                        )
        elif isinstance(node, ast.Assign):
            for tgt in node.targets:
                if (
                    isinstance(tgt, ast.Attribute)
                    and tgt.attr == _OP_DECISION_ATTR
                    and isinstance(tgt.ctx, ast.Store)
                ):
                    yield Violation(
                        rule_name="SCOUT_NO_SETATTR_OPERATOR_DECISION",
                        reason_tag="scout_setattr_operator_decision_outside_review_stage",
                        file=path,
                        line=node.lineno,
                        col=node.col_offset,
                        message="operator_decision may only be written by pipeline/scout/review_stage.py",
                    )
        elif isinstance(node, ast.AugAssign):
            tgt = node.target
            if (
                isinstance(tgt, ast.Attribute)
                and tgt.attr == _OP_DECISION_ATTR
                and isinstance(tgt.ctx, ast.Store)
            ):
                yield Violation(
                    rule_name="SCOUT_NO_SETATTR_OPERATOR_DECISION",
                    reason_tag="scout_setattr_operator_decision_outside_review_stage",
                    file=path,
                    line=node.lineno,
                    col=node.col_offset,
                    message="operator_decision may only be written by pipeline/scout/review_stage.py",
                )

SCOUT_NO_SETATTR_OPERATOR_DECISION = Rule(
    name="SCOUT_NO_SETATTR_OPERATOR_DECISION",
    reason_tag="scout_setattr_operator_decision_outside_review_stage",
    target_glob="pipeline/scout/**/*.py",
    check=_check_scout_no_setattr_operator_decision,
    description=(
        "`operator_decision` may only be written inside "
        "pipeline/scout/review_stage.py. Blueprint: section_03_scout.md §7.16."
    ),
)


# ---------------------------------------------------------------------------
# R5 — SCOUT_NO_EVAL
# ---------------------------------------------------------------------------

_DYNAMIC_EXEC_BUILTINS: frozenset[str] = frozenset({"eval", "exec", "compile"})

def _check_scout_no_eval(tree: ast.AST, path: Path) -> Iterator[Violation]:
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in _DYNAMIC_EXEC_BUILTINS
        ):
            yield Violation(
                rule_name="SCOUT_NO_EVAL",
                reason_tag="scout_dynamic_code_execution",
                file=path,
                line=node.lineno,
                col=node.col_offset,
                message=(
                    f"Scout must not call {node.func.id}() — dynamic code "
                    f"execution is forbidden under §7.16"
                ),
            )

SCOUT_NO_EVAL = Rule(
    name="SCOUT_NO_EVAL",
    reason_tag="scout_dynamic_code_execution",
    target_glob="pipeline/scout/**/*.py",
    check=_check_scout_no_eval,
    description=(
        "No module under pipeline/scout/ may call eval(), exec(), or "
        "compile(). Blueprint: section_03_scout.md §7.16."
    ),
)
