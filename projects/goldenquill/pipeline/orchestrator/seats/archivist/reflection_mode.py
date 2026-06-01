"""Reflection sub-mode SCAFFOLD — Archivist's third cadence (v0.1 Beta hook).

Internal name: `reflection_agent` / Reflection sub-mode / `--cadence reflection`.
External name (architecture v7.0.9 §8): "Lessons Memory" / "Outcome Learning" /
"Funding Lessons Digest". Operator-facing CLI surface: `tilth archivist lessons
--org <slug>` / `tilth archivist lessons --workspace`.

At v0.1 Beta hook this module is SCAFFOLD ONLY. The Pydantic AI agent is NOT
constructed. The three tools (`read_priors`, `record_reflection`,
`score_against_priors`) are NOT defined as callable Pydantic AI tools. The
seat-mode-dispatcher inside Archivist is NOT invoked. This module exists so
that:

1. Architecture v7.0.9 §1 seat-home binding has an on-disk evidence anchor.
2. The 17 F-REFLECTION-* predicate signatures at `logician/gates/reflection_gates.py`
   have a wiring target visible to test introspection.
3. The 5 F-ARCHIVIST-* sub-tag extensions per architecture v7.0.9 §3 are
   declared at the seat-module layer (additive entries to the parent gate's
   sub-tag registry — predicate body inherits from parent §4 v2.x rows 193/194).
4. v0.2 SPEC §15 v2.x Reflection amendment authors have a stable signature
   surface to lift to SPEC.

This is NOT a runtime module. Do NOT import this from any non-test code path
without first reading architecture v7.0.9 §9 ship plan.

Bound to the BINDING-vs-HORIZON-vs-PROBE-DEPENDENT split per operator refinement
2026-05-10 — see `logician/gates/reflection_gates.py` GATE_TIERS for the
authoritative tier label per gate.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


# ============================================================================
# Internal-vs-external naming (architecture v7.0.9 §8)
# ============================================================================

INTERNAL_CADENCE_NAME: str = "reflection"
"""Internal cadence flag value: `--cadence reflection`. Used at the dispatcher
+ blueprint + architecture text + audit trails + memory files. Grep-anchor for
internal-context surfaces."""

EXTERNAL_CADENCE_DISPLAY_NAME: str = "Lessons Memory"
"""External display name for operator-facing CLI + customer-facing materials.
Operator selected `tilth archivist lessons` as the v0.1 customer-facing CLI
surface per architecture v7.0.9 §8.2."""

EXTERNAL_ALTERNATIVES: tuple[str, ...] = (
    "Lessons Memory",
    "Outcome Learning",
    "Funding Lessons Digest",
)
"""Per architecture v7.0.9 §8.2 — three external surfaces; CLI uses 'Lessons
Memory' (mapped to `tilth archivist lessons`); business-plan + investor +
forward-binding GUI use any of the three per context."""


# ============================================================================
# Forward-binding dataclass schemas (v0.2 SPEC promotes to frozen kw_only)
# ============================================================================

@dataclass
class ReflectionInput:
    """v0.1 Beta hook SCAFFOLD shape. v0.2 SPEC §15 v2.x promotes this to a
    frozen kw_only Pydantic dataclass with full field validation.

    Architecturally-binding fields per architecture v7.0.9 §4 (grounding-signal-
    class registry) + §2 (predicate dependencies):
      - grounding_signal_classes : set[str] — REQUIRED. F-REFLECTION-NO-
        EXTERNAL-SIGNAL fail-closes when empty.
      - source_substrate_paths : list[str] — pointer-only schema per §15.5.0.A;
        no upstream content re-encoded.
      - rationale : str — pattern-level only per F-ARCHIVIST-LESSON-INSTANCE-
        LEAK + Reflection sub-tag extension.
    """
    run_id: str = ""
    org_slug: str = ""
    grounding_signal_classes: set[str] = field(default_factory=set)
    source_substrate_paths: list[str] = field(default_factory=list)
    rationale: str = ""
    cadence: str = INTERNAL_CADENCE_NAME


@dataclass
class ArchivistReflectionDigest:
    """Output contract SCAFFOLD. v0.2 SPEC §15 v2.x promotes to
    `archivist_reflection_digest.v1` schema with frozen kw_only + Ed25519
    signature on (input_hash, output_hash, run_id, operator_attach_decision,
    timestamp_utc) per architecture v7.0.9 §6 (Anthropic Dreams gap — signed
    audit trail)."""
    digest_id: str = ""
    archivist_run_id: str = ""
    cadence: str = INTERNAL_CADENCE_NAME
    proposed_at_utc: str = ""
    proposed_action: str = ""  # e.g., "surface_pattern" / "mark_for_review"
    source_substrate_path: str = ""
    pattern_summary: str = ""  # pattern-level only — never instance-level
    rationale: str = ""
    grounding_signal_classes: set[str] = field(default_factory=set)


# ============================================================================
# Sub-tag extension declaration (architecture v7.0.9 §3)
# ============================================================================

# The 5 F-ARCHIVIST-* sub-tag extensions per architecture v7.0.9 §3. These are
# declarative entries at the seat-module layer; the parent gate's predicate body
# at §4 v2.x rows 193/194 already enforces the parent's failure mode. Sub-tag
# attribution surfaces when the reflection_agent (v1.x scope) invokes a path
# that the parent gate fires on.
REFLECTION_SUB_TAGS_UNDER_F_ARCHIVIST: dict[str, str] = {
    "F-ARCHIVIST-CROSS-ORG-LEAK": "reflection_cross_org_read",
    "F-ARCHIVIST-AUTO-APPLY-ATTEMPTED": "reflection_attach_unsigned",
    "F-ARCHIVIST-LESSON-INSTANCE-LEAK": "reflection_instance_in_pattern_field",
    "F-ARCHIVIST-CADENCE-DRIFT": "reflection_interval_drift",
    "F-ARCHIVIST-READ-WITHOUT-VAULT-INTENT": "reflection_evidence_out_of_run",
}


# ============================================================================
# reflection_agent SCAFFOLD (NOT constructed at v0.1 Beta hook)
# ============================================================================

class ReflectionAgentNotConstructedError(RuntimeError):
    """Raised if any caller tries to instantiate the reflection_agent at v0.1
    Beta hook. Per architecture v7.0.9 §9.1, the v0.1 hook is dormant Cedar/
    Python primitives only — no agent construction, no runtime invocation.
    The agent ships at v1.x runtime amendment.
    """


def construct_reflection_agent(*args: Any, **kwargs: Any) -> Any:
    """Stub for v1.x runtime amendment. Architecturally bound to:
      - Always-local classification posture (synthesis §5.2 — reflection
        derives from post-fill drafts which contain Confidential KFR-resolved
        slot values; v7.0.7 §1 routes any Confidential input to local-only).
      - Three tools per Lane 4 + synthesis §5.2: `read_priors` /
        `record_reflection` / `score_against_priors`.
      - Own `Deps` per Pydantic AI multi-agent hand-off idiom.
      - Constructed by Archivist's seat-mode-dispatcher on `--cadence reflection`;
        torn down at end-of-cadence.

    At v0.1 Beta hook this raises. v1.x runtime amendment realizes.
    """
    raise ReflectionAgentNotConstructedError(
        "reflection_agent is not constructed at v0.1 Beta hook. "
        "Per architecture v7.0.9 §9.1, the v0.1 hook is dormant Cedar/Python "
        "primitives only. v1.x runtime amendment lands the agent + tools."
    )


# ============================================================================
# Public API
# ============================================================================

__all__ = [
    "INTERNAL_CADENCE_NAME",
    "EXTERNAL_CADENCE_DISPLAY_NAME",
    "EXTERNAL_ALTERNATIVES",
    "ReflectionInput",
    "ArchivistReflectionDigest",
    "REFLECTION_SUB_TAGS_UNDER_F_ARCHIVIST",
    "ReflectionAgentNotConstructedError",
    "construct_reflection_agent",
]
