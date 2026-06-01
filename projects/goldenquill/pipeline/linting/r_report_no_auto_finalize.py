"""R-REPORT-NO-AUTO-FINALIZE — AST-lint rule (§14 v1 LOCK §14.16 Layer 1).

Per §14 v1 LOCKED 2026-05-10 §14.16.4 + WS-J Slice 3 handoff (2026-05-11).

Layer 1 of the three-layer R-REPORT-NO-AUTO-FINALIZE defense (AST-lint +
Logician F-REPORT-COMMITMENT-UNTRACED PRE-pre-finalize + Cedar
``report_finalize.cedar`` PERMIT/DENY at write path).

Targets ``pipeline/orchestrator/tracks/report_mode.py`` and
``pipeline/orchestrator/seats/report_generator/**/*.py``. Forbids:

1. Any ``GrantReportBundle(...)`` constructor call with
   ``bundle_state="FINALIZED"`` (literal-string kwarg). The ONLY admissible
   construction-site for a FINALIZED bundle is inside the function named
   ``finalize_operator_signed_report`` (whitelisted function name).
2. Any ``ClaimEvidenceMap(...)`` constructor call with
   ``operator_signature_status="SIGNED"`` (literal-string kwarg) outside
   the whitelisted signer module ``claim_evidence_map`` (where
   :func:`sign_claim_evidence_map` is the sanctioned producer).

The whitelist principle: a contributor extending the substrate with a new
finalization path MUST either (a) route through
``finalize_operator_signed_report``, or (b) explicitly add the new
function name to the whitelist in code review.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation


# Files in scope for this rule (multi-glob — we apply via a wrapper).
_REPORT_MODE_GLOB = "pipeline/orchestrator/tracks/report_mode.py"
_REPORT_GENERATOR_GLOB = "pipeline/orchestrator/seats/report_generator/**/*.py"
_REPORT_GENERATOR_COMPOSERS_GLOB = (
    "pipeline/orchestrator/seats/report_generator/composers/*.py"
)

# Function names that are allowed to construct a FINALIZED bundle / SIGNED map.
_FINALIZE_WHITELIST: frozenset[str] = frozenset(
    {
        "finalize_operator_signed_report",
        # The signer module's own sign_claim_evidence_map is the
        # sanctioned producer of SIGNED maps.
        "sign_claim_evidence_map",
    }
)


def _walk_with_enclosing_function(
    tree: ast.AST,
) -> Iterator[tuple[ast.AST, ast.FunctionDef | ast.AsyncFunctionDef | None]]:
    """Yield (node, enclosing_function_or_None) for every node in tree.

    Enclosing-function is the nearest FunctionDef / AsyncFunctionDef
    ancestor in lexical scope.
    """

    def _recurse(
        node: ast.AST,
        enclosing: ast.FunctionDef | ast.AsyncFunctionDef | None,
    ) -> Iterator[
        tuple[ast.AST, ast.FunctionDef | ast.AsyncFunctionDef | None]
    ]:
        yield (node, enclosing)
        new_enclosing = enclosing
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            new_enclosing = node
        for child in ast.iter_child_nodes(node):
            yield from _recurse(child, new_enclosing)

    yield from _recurse(tree, None)


def _is_call_to_named_constructor(
    node: ast.AST, target_names: frozenset[str]
) -> bool:
    """Return True iff ``node`` is an ``ast.Call`` whose func resolves to one
    of ``target_names`` (bare Name OR Attribute whose ``.attr`` matches).
    """
    if not isinstance(node, ast.Call):
        return False
    func = node.func
    if isinstance(func, ast.Name):
        return func.id in target_names
    if isinstance(func, ast.Attribute):
        return func.attr in target_names
    return False


def _kwarg_string_value(node: ast.Call, key: str) -> str | None:
    """Extract the literal-string value of ``key=`` kwarg, or None."""
    for kw in node.keywords:
        if kw.arg == key and isinstance(kw.value, ast.Constant) and isinstance(
            kw.value.value, str
        ):
            return kw.value.value
    return None


def _check_report_no_auto_finalize(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    for node, enclosing in _walk_with_enclosing_function(tree):
        # Rule (1) — FINALIZED bundle construction outside whitelist.
        if _is_call_to_named_constructor(node, frozenset({"GrantReportBundle"})):
            assert isinstance(node, ast.Call)
            value = _kwarg_string_value(node, "bundle_state")
            if value == "FINALIZED":
                if enclosing is None or enclosing.name not in _FINALIZE_WHITELIST:
                    yield Violation(
                        rule_name="R-REPORT-NO-AUTO-FINALIZE",
                        reason_tag="grant_report_bundle_finalized_outside_whitelist",
                        file=path,
                        line=node.lineno,
                        col=node.col_offset,
                        message=(
                            "GrantReportBundle(..., bundle_state=\"FINALIZED\") "
                            "constructed outside `finalize_operator_signed_report`; "
                            "auto-finalize forbidden per §14.16 (Layer 1)"
                        ),
                    )
        # Rule (2) — SIGNED claim_evidence_map construction outside whitelist.
        if _is_call_to_named_constructor(node, frozenset({"ClaimEvidenceMap"})):
            assert isinstance(node, ast.Call)
            value = _kwarg_string_value(node, "operator_signature_status")
            if value == "SIGNED":
                if enclosing is None or enclosing.name not in _FINALIZE_WHITELIST:
                    yield Violation(
                        rule_name="R-REPORT-NO-AUTO-FINALIZE",
                        reason_tag="claim_evidence_map_signed_outside_whitelist",
                        file=path,
                        line=node.lineno,
                        col=node.col_offset,
                        message=(
                            "ClaimEvidenceMap(..., operator_signature_status="
                            "\"SIGNED\") constructed outside the sanctioned "
                            "signer surface; must route through "
                            "sign_claim_evidence_map / finalize_operator_signed_report"
                        ),
                    )


def _check_multi_glob(tree: ast.AST, path: Path) -> Iterator[Violation]:
    """Multi-glob wrapper — apply the rule under either glob."""
    from pipeline.linting.ast_lint import _glob_matches_path  # local to avoid cycle

    if not any(
        _glob_matches_path(g, path)
        for g in (
            _REPORT_MODE_GLOB,
            _REPORT_GENERATOR_GLOB,
            _REPORT_GENERATOR_COMPOSERS_GLOB,
        )
    ):
        return
    yield from _check_report_no_auto_finalize(tree, path)


REPORT_NO_AUTO_FINALIZE: Rule = Rule(
    name="R-REPORT-NO-AUTO-FINALIZE",
    reason_tag="report_no_auto_finalize",
    # Permissive glob — wrapper filters via the multi-glob set.
    target_glob="pipeline/orchestrator/**/*.py",
    check=_check_multi_glob,
    description=(
        "Forbid GrantReportBundle(bundle_state=\"FINALIZED\") and "
        "ClaimEvidenceMap(operator_signature_status=\"SIGNED\") construction "
        "outside the whitelisted finalize_operator_signed_report / "
        "sign_claim_evidence_map functions (§14.16 Layer 1)."
    ),
)


__all__ = ["REPORT_NO_AUTO_FINALIZE"]
