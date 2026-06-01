"""R-V0-10-NO-SLOT-TOKEN-EMISSION — AST-lint rule. [v7.0.10 §2.2 Layer 1]

Architecture v7.0.10 LOCKED 2026-05-11 (row 215) deprecates the v7.0.7-era
"Sanitized" / opaque-slot-token customer-facing posture entirely. No legitimate
code path under any v7.0.10 posture (Frontier-Eligible / Split-Context Hybrid /
Local-Only-Sovereign) emits `[SLOT_*]` tokens into cloud-routed prompts. The
two F-CLASS-* gates that policed the discipline at v7.0.7
(`F-CLASS-SLOT-ID-NON-OPAQUE` + `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED`)
remain live as defense-in-depth — they fail-closed on any `\\[SLOT_[^\\]]*\\]`
pattern in a cloud-routed prompt, but any firing is a bug-or-attack signal.

This AST-lint rule is **Layer 1 of three-layer defense** against accidental
slot-token emission, paired with the runtime POST-call boundary gates above.
The rule scans every Python module under the orchestrator + seats trees (the
code paths that can construct cloud-routable prompts) for string literals
containing the substring `[SLOT_` — any match is a violation.

Scope:
  - ``pipeline/orchestrator/**/*.py``
  - ``pipeline/seats/**/*.py``

Out of scope (allow-listed):
  - ``pipeline/linting/**/*.py``      — lint rules themselves reference the pattern in docstrings + regex constants
  - ``pipeline/logician/gates/**/*.py`` — the defense-in-depth gate modules reference the pattern in their predicates
  - Tests under ``tests/**`` — out of scope (rule target_glob excludes tests by default)

If a legitimate use of the literal token surfaces (e.g., a migration helper
that reads legacy v7.0.7-era artifacts), the path can be added to the inline
allow-list. The default disposition is fail-closed.

Authority:
  - architecture v7.0.10 §2.2 (deprecation rationale + repurpose disposition)
  - architecture v7.0.10 §5.2 (defense-in-depth gate roster)
  - section_04_v2_x_amendment.md §4.3.6 (predicate-level discipline)
  - section_00_5_v7_0_10_amendment.md §C (disposition_at_v7_0_10 sub-tag)
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Iterator

from pipeline.linting._rule_types import Rule, Violation


_TARGET_GLOB = "pipeline/orchestrator/**/*.py"
_SECONDARY_TARGET_GLOB = "pipeline/seats/**/*.py"

# Broadened pattern per v7.0.10 §2.2 — matches any slot-shaped token (numeric,
# alphabetic, mixed, empty suffix). Matches the runtime gate regex byte-for-byte.
_SLOT_TOKEN_RE = re.compile(r"\[SLOT_[^\]]*\]")

# Paths exempted from the rule because they reference the literal token as
# part of documenting / scanning for the defense-in-depth surface (NOT as a
# cloud-routed emission path). Each exemption is named with rationale.
_EXEMPT_FILE_SUFFIXES: tuple[str, ...] = (
    # `pipeline/orchestrator/seats/data_collector/field_validator.py` —
    # contains an outbound-boundary regex that scans Data Collector message
    # bodies for `[SLOT_*]` patterns (defense-in-depth, mirrors
    # F-CLASS-SLOT-ID-NON-OPAQUE per the gate's docstring). Detection-side
    # use, not emission-side use; firing here would be a false positive.
    "pipeline/orchestrator/seats/data_collector/field_validator.py",
)


def _is_exempt(path: Path) -> bool:
    posix = path.as_posix()
    return any(posix.endswith(suffix) for suffix in _EXEMPT_FILE_SUFFIXES)


def _check_no_slot_token_emission(tree: ast.AST, path: Path) -> Iterator[Violation]:
    if _is_exempt(path):
        return
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant):
            continue
        value = node.value
        if not isinstance(value, str):
            continue
        if _SLOT_TOKEN_RE.search(value) is None:
            continue
        yield Violation(
            rule_name="R-V0-10-NO-SLOT-TOKEN-EMISSION",
            reason_tag="v0_10_slot_token_literal_in_orchestrator_or_seat",
            file=path,
            line=getattr(node, "lineno", 1),
            col=getattr(node, "col_offset", 0),
            message=(
                "String literal containing a `[SLOT_*]` token detected in an "
                "orchestrator or seat module. Architecture v7.0.10 LOCKED "
                "2026-05-11 (row 215) deprecates the opaque-slot-token mechanism "
                "entirely. No legitimate code path under any v7.0.10 posture "
                "emits slot tokens into cloud-routed prompts. The defense-in-"
                "depth runtime gates (F-CLASS-SLOT-ID-NON-OPAQUE PRE + "
                "F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED POST) will fail-"
                "closed if a slot token reaches the outbound boundary; this "
                "AST-lint rule is Layer 1 — catching the emission at module "
                "load time. If you believe this literal is legitimate, add the "
                "path suffix to `_EXEMPT_FILE_SUFFIXES` with a comment naming "
                "the rationale + amendment row."
            ),
        )


V0_10_NO_SLOT_TOKEN_EMISSION: Rule = Rule(
    name="R-V0-10-NO-SLOT-TOKEN-EMISSION",
    reason_tag="v0_10_no_slot_token_emission",
    target_glob=_TARGET_GLOB,
    check=_check_no_slot_token_emission,
    description=(
        "Forbid `[SLOT_*]` token literals in orchestrator modules. v7.0.10 "
        "deprecated the opaque-slot-token mechanism; defense-in-depth Layer 1."
    ),
)


V0_10_NO_SLOT_TOKEN_EMISSION_SEATS: Rule = Rule(
    name="R-V0-10-NO-SLOT-TOKEN-EMISSION",
    reason_tag="v0_10_no_slot_token_emission",
    target_glob=_SECONDARY_TARGET_GLOB,
    check=_check_no_slot_token_emission,
    description=(
        "Forbid `[SLOT_*]` token literals in seat modules. v7.0.10 "
        "deprecated the opaque-slot-token mechanism; defense-in-depth Layer 1."
    ),
)


__all__ = [
    "V0_10_NO_SLOT_TOKEN_EMISSION",
    "V0_10_NO_SLOT_TOKEN_EMISSION_SEATS",
]
