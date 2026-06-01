"""R-REPORT-VAULT-INTENT-REQUIRED — AST-lint rule (§14 v1 LOCK §14.0 + §14.16).

Per §14 v1 LOCKED 2026-05-10 §14.0 per-substrate contract reference + WS-J
Slice 3 handoff (2026-05-11).

Layer 1 of R-REPORT-VAULT-INTENT-REQUIRED. Targets the §14 Report Generator
seat modules (composers + track-mode entry point). Forbids:

* Any ``open(...)`` call against a path that references a §14 read
  substrate. Heuristic: if the file under audit imports the Vault read
  intent Protocol from ``_base`` or the composer dispatcher, then ANY
  bare ``open(...)`` call in the module is a violation — the composer
  layer never opens files; the injected read-intent callable is the
  sanctioned route.
* Any ``pathlib.Path(...).read_text(...) / .read_bytes(...)`` call —
  same prohibition: only the injected callable touches disk.
* Any direct import of ``yaml`` / ``json`` / ``builtins.open`` whose
  use is not bracketed by a comment indicating sanctioned use (the
  rule doesn't enforce comments; it just rejects the call sites).

Scope: ``pipeline/orchestrator/seats/report_generator/**/*.py`` AND
``pipeline/orchestrator/tracks/report_mode.py``. The signer module
``claim_evidence_map.py`` is exempt — it does no I/O and only handles
in-memory canonical bytes.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation


_REPORT_GENERATOR_GLOB = "pipeline/orchestrator/seats/report_generator/**/*.py"
_REPORT_MODE_GLOB = "pipeline/orchestrator/tracks/report_mode.py"

# Files inside the report_generator tree that are EXEMPT from this rule
# (they are pure-Python helpers with no substrate I/O semantics).
_EXEMPT_BASENAMES: frozenset[str] = frozenset(
    {
        # canonical-JSON encoder + hash helpers — no disk I/O
        "_canonical.py",
        # frozen schema dataclasses — no I/O
        "_schemas.py",
        # commitment_id regex + sanitize — no I/O
        "_commitment_id.py",
        # entailment helpers — pure
        "_entailment.py",
        # Cedar policy bootstrap — reads policy files (workspace-shared,
        # not operational substrate); sanctioned by the engine architecture.
        # The Cedar load path is its own audit surface (CriticalPolicyError).
        "_cedar_bootstrap.py",
        # signer envelope — no I/O, only canonical-bytes + Ed25519 protocol
        "claim_evidence_map.py",
    }
)

# Forbidden bare-name function calls.
_FORBIDDEN_BARE_NAMES: frozenset[str] = frozenset({"open"})

# Forbidden Attribute call surfaces.
_FORBIDDEN_ATTRS: frozenset[tuple[str, str]] = frozenset(
    {
        # path object I/O accessors
        ("Path", "read_text"),
        ("Path", "read_bytes"),
        ("Path", "open"),
        # io builtins
        ("io", "open"),
        ("builtins", "open"),
        ("os", "open"),
        # yaml / json shorthand (these usually wrap open() but we add
        # belt-and-braces — composers must never read YAML directly)
        ("yaml", "safe_load"),
        ("yaml", "load"),
        ("json", "load"),
    }
)


def _is_exempt(path: Path) -> bool:
    return path.name in _EXEMPT_BASENAMES


def _check_report_vault_intent_required(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    if _is_exempt(path):
        return
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        # bare-name forbidden calls (open(...))
        if isinstance(func, ast.Name) and func.id in _FORBIDDEN_BARE_NAMES:
            yield Violation(
                rule_name="R-REPORT-VAULT-INTENT-REQUIRED",
                reason_tag="raw_open_in_report_generator",
                file=path,
                line=node.lineno,
                col=node.col_offset,
                message=(
                    f"raw `{func.id}(...)` call inside §14 Report Generator "
                    "substrate; substrate reads must wrap the injected "
                    "VaultReadIntentCallable (R-REPORT-VAULT-INTENT-REQUIRED)"
                ),
            )
            continue
        # Attribute calls — Path(x).read_text() / yaml.safe_load(...) etc
        if isinstance(func, ast.Attribute):
            value = func.value
            attr = func.attr
            # Pattern A: Name.attr  (e.g. yaml.safe_load, os.open)
            if isinstance(value, ast.Name) and (value.id, attr) in _FORBIDDEN_ATTRS:
                yield Violation(
                    rule_name="R-REPORT-VAULT-INTENT-REQUIRED",
                    reason_tag=f"forbidden_attr_call:{value.id}.{attr}",
                    file=path,
                    line=node.lineno,
                    col=node.col_offset,
                    message=(
                        f"forbidden `{value.id}.{attr}(...)` call inside §14 "
                        "Report Generator substrate; reads must wrap the "
                        "injected VaultReadIntentCallable"
                    ),
                )
                continue
            # Pattern B: Call.attr  (e.g. Path(x).read_text())
            if isinstance(value, ast.Call):
                inner = value.func
                if isinstance(inner, ast.Name) and (inner.id, attr) in _FORBIDDEN_ATTRS:
                    yield Violation(
                        rule_name="R-REPORT-VAULT-INTENT-REQUIRED",
                        reason_tag=f"forbidden_call_chain:{inner.id}().{attr}",
                        file=path,
                        line=node.lineno,
                        col=node.col_offset,
                        message=(
                            f"forbidden `{inner.id}(...).{attr}(...)` chain "
                            "inside §14 Report Generator substrate; reads "
                            "must wrap the injected VaultReadIntentCallable"
                        ),
                    )


def _check_multi_glob(tree: ast.AST, path: Path) -> Iterator[Violation]:
    """Multi-glob wrapper."""
    from pipeline.linting.ast_lint import _glob_matches_path

    if not any(
        _glob_matches_path(g, path)
        for g in (_REPORT_GENERATOR_GLOB, _REPORT_MODE_GLOB)
    ):
        return
    yield from _check_report_vault_intent_required(tree, path)


REPORT_VAULT_INTENT_REQUIRED: Rule = Rule(
    name="R-REPORT-VAULT-INTENT-REQUIRED",
    reason_tag="report_vault_intent_required",
    target_glob="pipeline/orchestrator/**/*.py",
    check=_check_multi_glob,
    description=(
        "Forbid raw open() / Path.read_text() / yaml.safe_load(...) calls "
        "inside the §14 Report Generator substrate; substrate reads must "
        "wrap the injected VaultReadIntentCallable per §14.0 + §14.16."
    ),
)


__all__ = ["REPORT_VAULT_INTENT_REQUIRED"]
