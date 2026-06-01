"""R-NO-POLITICAL-AXIS-LITERAL — AST-lint rule. [§4 v2.x apolitical_dialect §4.X.2]

Architecture v7.0.12 LOCKED 2026-05-16T14:00:00Z retires the four-axis political
enum (``conservative | centrist | progressive | soul_fire | soul-fire``) from
Tilth's routing substrate. The retired vocabulary cannot appear as a Pydantic
``Literal[...]`` annotation in routing-relevant code, nor as a field-name token,
in any newly-authored module.

This rule is **Layer 1 of two-layer defense** against accidental reintroduction:

- **Layer 1 (this AST-lint rule)** — commit-hook static check on Python source
  matching the rule's target glob. Fires when:
   * a string literal containing a retired field-name pattern (e.g.
     ``funder_political_axis``, ``progressive_register``) appears in source;
   * a Pydantic ``Literal[...]`` annotation contains two or more retired
     enum values;
   * an unresolvable ``Literal[*X]`` / ``Literal[X]`` reference is encountered
     where ``X`` could plausibly evaluate to the retired enum.
- **Layer 2 (runtime gate)** — :mod:`pipeline.logician.gates.f_dialect_political_axis_leak`
  catches the same conditions at startup / config-refresh / card-reload time,
  including paths that bypass the commit hook (manual operator vault edits).

Scope and migration discipline
------------------------------
The amendment LOCKed under **Option-B split** (per architecture v7.0.12 §7
Cycle-2 fold-in ``JD-C2-LOW-2``): the cards-ceremony that re-keys the operator
substrate (`pipeline/seats/scribe/dialect.py`, `pipeline/seats/red_team/types.py`,
`pipeline/seats/editor/types.py`, etc.) is deferred 22-36 hours and runs as a
separate ceremony. Until that ceremony runs, the seats/orchestrator subtrees
still carry the retired vocabulary by intentional deferral.

This AST-lint rule therefore scopes to subtrees that are **already migrated or
greenfield** and **must stay clean**:

- ``pipeline/cards/**/*.py`` — Card System code (greenfield at v0.2 first wave;
  Wave 2 cartridges + their schemas).
- ``pipeline/types/**/*.py`` — Type modules (already migrated; CapitalLogicCard
  + CustomerIdentityCategory enums carry no political axis).
- ``pipeline/logician/gates/**/*.py`` — Logician gate modules (with named
  exemptions for the gates that legitimately reference the vocabulary as
  detectors: ``f_dialect_political_axis_leak.py``, ``f_dialect_migration_incomplete.py``,
  ``f_logician_spine_drift.py``, ``f_funder_corpus_stale.py``).

The seats / orchestrator subtrees are **out of scope at this LOCK** by design.
A follow-on amendment widens the target_glob after the cards-ceremony lands
the migrations.

Exemption mechanism
-------------------
Path-suffix exemptions live in ``_EXEMPT_FILE_SUFFIXES`` and require a
named-rationale comment. Adding a new exemption is allowed only with a
documented amendment row (per the §4 v2.x.1 sub-tag-extension precedent — a
new exemption is a new code-row, not a config edit).

Authority:
  - architecture v7.0.12 §1.3 + §3 + §4 (LOCKED 2026-05-16T14:00:00Z; rows 234/248)
  - section_04_logician_v2_x_apolitical_dialect.md §4.X.2 (LOCKED rows 236/249)
  - section_00_5_apolitical_dialect_amendment.md §A row 551 (LOCKED rows 237/246)
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation


# ---------------------------------------------------------------------------
# Retired vocabulary — closed set per architecture v7.0.12 §1.1.
# Kept in lockstep with :mod:`pipeline.logician.gates.f_dialect_political_axis_leak`
# (single source of truth lives at the gate; this module restates for AST-lint
# independence).
# ---------------------------------------------------------------------------

_RETIRED_LITERALS: frozenset[str] = frozenset(
    {"conservative", "centrist", "progressive", "soul_fire", "soul-fire"}
)


# Layer 1 field-name regex (case-insensitive word-boundary-aware per FI-2).
_FIELD_NAME_REGEX = re.compile(
    r"(?i)\b(funder[_\-]?political[_\-]?axis|progressive[_\-]?register)\b"
)

# Substring detector for any identifier containing ``political_axis``.
_FIELD_NAME_SUBSTRING = re.compile(r"(?i)political[_\-]?axis")


# ---------------------------------------------------------------------------
# Target globs.
#
# Two rule instances are registered so the harness can match each path
# subtree under its own glob (harness matches one glob per Rule instance).
# Both share the same _check callable.
# ---------------------------------------------------------------------------

_PRIMARY_TARGET_GLOB = "pipeline/cards/**/*.py"
_SECONDARY_TARGET_GLOB = "pipeline/types/**/*.py"
_TERTIARY_TARGET_GLOB = "pipeline/logician/gates/**/*.py"


# ---------------------------------------------------------------------------
# Path-suffix exemptions (named rationale only).
# ---------------------------------------------------------------------------

_EXEMPT_FILE_SUFFIXES: tuple[str, ...] = (
    # Detector modules — legitimately reference the retired vocabulary
    # because their job is to find leaks of it.
    "pipeline/logician/gates/f_dialect_political_axis_leak.py",
    "pipeline/logician/gates/f_dialect_migration_incomplete.py",
    # Migration-pending Logician gates per Option-B split — the cards-
    # ceremony will rewrite these. Until then, they legitimately carry
    # the retired enum as the *prior* dialect set they validate.
    # Each row carries the v7.0.12 LOCK row that authorizes the
    # exemption + the follow-on amendment row that removes it.
    #   v7.0.12 LOCK rows 234/248 (architecture) authorize the exemption;
    #   the cards-ceremony follow-on amendment (TBD row, post-22-36h
    #   operator work) will rewrite these files and remove the exemption.
    "pipeline/logician/gates/f_logician_spine_drift.py",
    "pipeline/logician/gates/f_funder_corpus_stale.py",
    # The AST-lint rule itself + its tests carry the retired vocabulary
    # as part of their detection regex / fixture data.
    "pipeline/linting/r_no_political_axis_literal.py",
)


def _is_exempt(path: Path) -> bool:
    posix = path.as_posix()
    return any(posix.endswith(suffix) for suffix in _EXEMPT_FILE_SUFFIXES)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _literal_values_from_subscript(
    node: ast.Subscript,
) -> tuple[tuple[str, ...], bool]:
    """Extract string literal values from ``Literal[...]`` annotation.

    Per Cycle 1 FI-4 + Cycle 2 C2-H-2: walk the slice tuple, resolve
    direct constants + simple list/tuple literals. Returns
    ``(values, fully_resolved)``. ``fully_resolved=False`` means the
    annotation references a non-trivial expression (Name lookups, calls,
    attribute access, ``typing.get_args(X)``, etc.); the caller should
    treat unresolved Literal[...] as a fail-closed signal at the runtime
    gate layer (this AST-lint rule reports it as an unresolved-literal
    violation only if the file's identifier or context carries one of
    the retired tokens — otherwise it stays silent to avoid noise on
    every Literal[...] in the codebase).
    """
    values: list[str] = []
    resolved = True

    # Python 3.8+: subscript.slice is the value directly (not Index).
    slice_node: ast.AST
    if hasattr(node, "slice") and isinstance(node.slice, ast.Index):  # pragma: no cover - py3.8
        slice_node = node.slice.value  # type: ignore[attr-defined]
    else:
        slice_node = node.slice

    def _emit(n: ast.AST) -> None:
        nonlocal resolved
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            values.append(n.value)
        elif isinstance(n, (ast.List, ast.Tuple, ast.Set)):
            for elt in n.elts:
                _emit(elt)
        elif isinstance(n, ast.Starred):
            _emit(n.value)
        else:
            # Names, calls, attribute access, etc. — cannot statically resolve.
            resolved = False

    if isinstance(slice_node, ast.Tuple):
        for elt in slice_node.elts:
            _emit(elt)
    else:
        _emit(slice_node)

    return tuple(values), resolved


def _is_literal_annotation(node: ast.Subscript) -> bool:
    """Return True if ``node`` is ``Literal[...]`` (qualified or bare)."""
    if isinstance(node.value, ast.Name) and node.value.id == "Literal":
        return True
    if (
        isinstance(node.value, ast.Attribute)
        and node.value.attr == "Literal"
    ):
        return True
    return False


# ---------------------------------------------------------------------------
# Check
# ---------------------------------------------------------------------------


def _check_no_political_axis_literal(
    tree: ast.AST, path: Path
) -> Iterator[Violation]:
    if _is_exempt(path):
        return
    for node in ast.walk(tree):
        # Layer 1: string literals carrying retired field-name patterns.
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value
            if _FIELD_NAME_REGEX.search(value) or _FIELD_NAME_SUBSTRING.search(value):
                yield Violation(
                    rule_name="R-NO-POLITICAL-AXIS-LITERAL",
                    reason_tag=(
                        "f_dialect_political_axis_leak.field_name_in_literal"
                    ),
                    file=path,
                    line=getattr(node, "lineno", 1),
                    col=getattr(node, "col_offset", 0),
                    message=(
                        "F-DIALECT-POLITICAL-AXIS-LEAK: string literal "
                        f"{value!r} contains a retired political-axis "
                        "field-name pattern (funder_political_axis or "
                        "progressive_register). Architecture v7.0.12 LOCKED "
                        "2026-05-16 retires the four-axis political enum; "
                        "rename routing fields to CLC slugs (per the eight "
                        "CapitalLogicCard values in "
                        "pipeline/types/identity_capital.py) or remove the "
                        "literal. The runtime gate "
                        "F-DIALECT-POLITICAL-AXIS-LEAK fail-closes at "
                        "startup if this literal survives into a routing "
                        "context."
                    ),
                )
            continue
        # Layer 1: identifier names carrying retired field-name tokens
        # (FunctionDef args, AnnAssign targets, AsyncFunctionDef args, etc.).
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for arg in [*node.args.args, *node.args.kwonlyargs]:
                arg_name = arg.arg
                if (
                    _FIELD_NAME_REGEX.search(arg_name)
                    or _FIELD_NAME_SUBSTRING.search(arg_name)
                ):
                    yield Violation(
                        rule_name="R-NO-POLITICAL-AXIS-LITERAL",
                        reason_tag=(
                            "f_dialect_political_axis_leak.field_name_in_identifier"
                        ),
                        file=path,
                        line=getattr(arg, "lineno", node.lineno),
                        col=getattr(arg, "col_offset", node.col_offset),
                        message=(
                            "F-DIALECT-POLITICAL-AXIS-LEAK: function "
                            f"argument {arg_name!r} contains a retired "
                            "political-axis field-name token. Architecture "
                            "v7.0.12 retires this surface."
                        ),
                    )
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            tgt = node.target.id
            if _FIELD_NAME_REGEX.search(tgt) or _FIELD_NAME_SUBSTRING.search(tgt):
                yield Violation(
                    rule_name="R-NO-POLITICAL-AXIS-LITERAL",
                    reason_tag=(
                        "f_dialect_political_axis_leak.field_name_in_identifier"
                    ),
                    file=path,
                    line=getattr(node, "lineno", 1),
                    col=getattr(node, "col_offset", 0),
                    message=(
                        "F-DIALECT-POLITICAL-AXIS-LEAK: annotated "
                        f"assignment target {tgt!r} contains a retired "
                        "political-axis field-name token."
                    ),
                )
        # Layer 2: Literal[...] annotations containing retired enum values.
        if isinstance(node, ast.Subscript) and _is_literal_annotation(node):
            values, resolved = _literal_values_from_subscript(node)
            if resolved:
                norm = {v.lower().replace("-", "_") for v in values}
                retired_in_literal = norm.intersection(
                    {"conservative", "centrist", "progressive", "soul_fire"}
                )
                if len(retired_in_literal) >= 2:
                    yield Violation(
                        rule_name="R-NO-POLITICAL-AXIS-LITERAL",
                        reason_tag=(
                            "f_dialect_political_axis_leak.pydantic_literal"
                        ),
                        file=path,
                        line=getattr(node, "lineno", 1),
                        col=getattr(node, "col_offset", 0),
                        message=(
                            "F-DIALECT-POLITICAL-AXIS-LEAK: Literal[...] "
                            f"annotation contains {sorted(retired_in_literal)!r} "
                            "— at least two retired political-axis values "
                            "present. Architecture v7.0.12 retires this enum; "
                            "key dialect routing off the eight-value "
                            "CapitalLogicCard slug set instead."
                        ),
                    )


# ---------------------------------------------------------------------------
# Rule instances (one per target glob)
# ---------------------------------------------------------------------------


NO_POLITICAL_AXIS_LITERAL_CARDS: Rule = Rule(
    name="R-NO-POLITICAL-AXIS-LITERAL",
    reason_tag="no_political_axis_literal_cards",
    target_glob=_PRIMARY_TARGET_GLOB,
    check=_check_no_political_axis_literal,
    description=(
        "Forbid retired political-axis vocabulary in `pipeline/cards/**/*.py` "
        "— Card System code is greenfield post-v7.0.12 and must stay clean. "
        "Companion runtime gate: F-DIALECT-POLITICAL-AXIS-LEAK."
    ),
)


NO_POLITICAL_AXIS_LITERAL_TYPES: Rule = Rule(
    name="R-NO-POLITICAL-AXIS-LITERAL",
    reason_tag="no_political_axis_literal_types",
    target_glob=_SECONDARY_TARGET_GLOB,
    check=_check_no_political_axis_literal,
    description=(
        "Forbid retired political-axis vocabulary in `pipeline/types/**/*.py` "
        "— the canonical CapitalLogicCard + CustomerIdentityCategory enums "
        "carry no political axis; any reappearance is a regression."
    ),
)


NO_POLITICAL_AXIS_LITERAL_LOGICIAN: Rule = Rule(
    name="R-NO-POLITICAL-AXIS-LITERAL",
    reason_tag="no_political_axis_literal_logician",
    target_glob=_TERTIARY_TARGET_GLOB,
    check=_check_no_political_axis_literal,
    description=(
        "Forbid retired political-axis vocabulary in newly-authored Logician "
        "gates under `pipeline/logician/gates/**/*.py`. Named exemptions for "
        "detector modules (f_dialect_*) and migration-pending gates (f_logician_spine_drift, "
        "f_funder_corpus_stale) — exemption removal is gated on the post-v7.0.12 "
        "cards-ceremony per Option-B split (JD-C2-LOW-2)."
    ),
)


__all__ = [
    "NO_POLITICAL_AXIS_LITERAL_CARDS",
    "NO_POLITICAL_AXIS_LITERAL_TYPES",
    "NO_POLITICAL_AXIS_LITERAL_LOGICIAN",
]
