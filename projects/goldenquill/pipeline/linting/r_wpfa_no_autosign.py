"""R-WPFA-NO-AUTOSIGN — AST-lint rule. [§5.1.WPFA.DEFENSE Layer 1]

Forbids any callsite outside the operator-attestation flow that would
populate ``CycleReceipt.signed_by_operator_ed25519`` automatically.
Specifically: a CycleReceipt constructor call with a non-None
``signed_by_operator_ed25519`` keyword whose value is a string literal,
function call, or attribute access that isn't ``operator_signer(...)``.

This is Layer 1 of the three-layer defense around buyer-facing PDF
emission. Defense layers 2 + 3 are at Cedar policy + Logician gate
(F-WPFA-OPERATOR-SIGNATURE-MISSING). Layer 4 is TTY-gating at the CLI
verb.

Module: targets ``pipeline/orchestrator/seats/wpfa/**/*.py``
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation


_TARGET_GLOB = "pipeline/orchestrator/seats/wpfa/**/*.py"

# Allowed ways to source the signature value at the CycleReceipt
# constructor call site. Any other shape is a Layer-1 violation.
_ALLOWED_SOURCE_NAMES = frozenset(
    {"operator_signer", "sig_hex", "signed_by_operator_ed25519"}
)


def _is_allowed_source(node: ast.AST) -> bool:
    if isinstance(node, ast.Constant) and node.value is None:
        return True  # explicit None — internal-only receipt
    if isinstance(node, ast.Name) and node.id in _ALLOWED_SOURCE_NAMES:
        return True
    if isinstance(node, ast.Attribute):
        # e.g., `unsigned.signed_by_operator_ed25519`
        return node.attr in _ALLOWED_SOURCE_NAMES
    if isinstance(node, ast.Call):
        # `operator_signer(...)` — only callable form permitted
        func = node.func
        if isinstance(func, ast.Name) and func.id == "operator_signer":
            return True
    return False


def _check_wpfa_no_autosign(tree: ast.AST, path: Path) -> Iterator[Violation]:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        # Look for CycleReceipt(...) constructor calls
        func = node.func
        target_name = None
        if isinstance(func, ast.Name):
            target_name = func.id
        elif isinstance(func, ast.Attribute):
            target_name = func.attr
        if target_name != "CycleReceipt":
            continue
        for kw in node.keywords:
            if kw.arg != "signed_by_operator_ed25519":
                continue
            if not _is_allowed_source(kw.value):
                yield Violation(
                    rule_name="R-WPFA-NO-AUTOSIGN",
                    reason_tag="wpfa_signature_from_non_operator_signer",
                    file=path,
                    line=kw.value.lineno,
                    col=kw.value.col_offset,
                    message=(
                        "CycleReceipt(signed_by_operator_ed25519=...) may only "
                        "be populated by `operator_signer(...)` return value, "
                        "a `sig_hex`-named local, an attribute matching the "
                        "allowed sources, or `None` (internal-only). Three-"
                        "layer defense Layer 1 fires: R-WPFA-NO-AUTOSIGN."
                    ),
                )


WPFA_NO_AUTOSIGN: Rule = Rule(
    name="R-WPFA-NO-AUTOSIGN",
    reason_tag="wpfa_no_autosign",
    target_glob=_TARGET_GLOB,
    check=_check_wpfa_no_autosign,
    description=(
        "Forbid CycleReceipt construction with signed_by_operator_ed25519 "
        "set to anything other than operator_signer(...) return value, "
        "allowlisted local names, an allowed attribute, or None."
    ),
)


__all__ = ["WPFA_NO_AUTOSIGN"]
