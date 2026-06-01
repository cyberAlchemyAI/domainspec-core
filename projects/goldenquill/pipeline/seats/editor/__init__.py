"""pipeline.seats.editor — §8 Editor seat (clarity pass).

Blueprint anchor: ``skills/editor/SKILL.md`` + ``pipeline/blueprint/v0.1/section_07_scribe.md``
v1.1.1 LOCKED 2026-04-21 (consumed `SectionDraft` shape) +
``pipeline/blueprint/v0.1/section_05_pipeline.md`` v6 (§4.4 invoke contract) +
``pipeline/blueprint/v0.1/section_04_logician.md`` v2.1 (PRE/POST gate-runner
contracts).

Spec-card governance:

- Parent card: ``pipeline/engineering/spec_cards/section_7_council_seats_pipeline_modules.md``
- R1 (this tranche): ``section_08_editor_round_1_adapter.md`` —
  adapter pattern entry per OQ-1 resolution. Wraps :file:`skills/editor/SKILL.md`
  rather than reimplementing its prompt logic in Python; full port deferred
  to v0.1.1 if drift surfaces.

Adapter rationale (parent spec §4 Option A; OQ-1 resolution 2026-04-21):

- Editor's load-bearing logic lives in the SKILL.md system prompt + the
  2-3-replacement invariant — both operator-vetted (3 grants won in 2026).
- Editor is SFR-exempt per architecture §F.1; no three-block verdict
  format to enforce at output boundary.
- Adapter scope = 1-2 sessions vs 3-4 for full port. R1 = adapter +
  shape validation + Logician gate wiring; R2 = polish + retry edges.

Import discipline (AST-lint R2 guard at parent ``pipeline.seats``):

- Seats may import from ``pipeline.logician`` (gate-code constants and
  exception classes) and ``pipeline.vault`` (draft + conversation-log
  persistence via the write dispatcher).
- Seats may NOT import from ``pipeline.loop`` — orchestration calls into
  seats via ``seat_runner.invoke_seat``, never the other way around.
- R1 uses skill subprocess via injected ``SkillLauncher`` Protocol;
  production wires clawdis.

Five Operating Laws enforcement (R1 layer):

- Law 4 (apolitical sector language) — :func:`adapter.validate_editor_output_shape`
  fires :data:`adapter.F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED` on whole-draft
  rewrite (40% body-coverage threshold inline-literal); 2-3 invariant
  enforcement via :data:`adapter.F_EDITOR_SINGLE_REPLACEMENT`. Admin-risk
  flagged terms surface on ``EditorOutput.terms_to_verify`` for Logician
  cross-check (out of R1 scope to consume).
- Law 3 (org isolation) — :func:`seat.default_cross_org_pre_gate` asserts
  envelope.org_slug matches ambient ``TILTH_ORG_SLUG``; raises
  :data:`seat.F_EDITOR_ORG_CROSS_REF` on mismatch.

Cross-family rigor: Editor production binding = Meta
(``groq/llama-3.3-70b-versatile`` primary + ``openai/gpt-4o-mini`` fallback)
per ``router.yaml``. R1 adapter is pure Python with no LLM call — the
LLM call lives inside the skill subprocess (separate trust boundary).
Cross-family enforcement happens upstream at
:func:`pipeline.loop.seat_runner.invoke_editor`.
"""

from __future__ import annotations

from typing import Final

from pipeline.seats.editor.adapter import (
    EditorOutputShapeError,
    EditorRewroteInsteadOfFlaggedError,
    EditorSingleReplacementError,
    EditorSkillOutputMalformedJson,
    EditorSkillSubprocessFail,
    EditorSkillTimeout,
    F_EDITOR_OUTPUT_SHAPE,
    F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED,
    F_EDITOR_SINGLE_REPLACEMENT,
    F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON,
    F_EDITOR_SKILL_SUBPROCESS_FAIL,
    F_EDITOR_SKILL_TIMEOUT,
    SkillLauncher,
    SkillSubprocessResult,
    invoke_editor_adapter,
    parse_skill_output,
    validate_editor_output_shape,
)
from pipeline.seats.editor.seat import (
    ENVELOPE_VERSION_V1,
    EXIT_GATE_FAIL,
    EXIT_INTERNAL_ERROR,
    EXIT_OK,
    F_EDITOR_ENVELOPE_MALFORMED,
    F_EDITOR_ORG_CROSS_REF,
    RESULT_VERSION_V1,
    ClockFn,
    EditorEnvelope,
    EditorEnvelopeMalformed,
    EditorGateFailed,
    EditorSeatResult,
    PostGateCallable,
    PreGateCallable,
    decode_envelope,
    default_cross_org_pre_gate,
    default_noop_post_gate,
    encode_result,
    run_seat,
)
from pipeline.seats.editor.types import (
    Dialect,
    EditorGap,
    EditorInput,
    EditorOutput,
    EditorSkillInvocation,
    FlaggedTerm,
    IssueType,
    Miscategorization,
    ReadabilityFeedback,
    ReplacementLabel,
    ReplacementOption,
    Severity,
    TaxonomyCheck,
    ToneFeedback,
)
from pipeline.seats.editor.validator import (
    TAXONOMY_CATEGORIES,
    ValidationReport,
    apply_r2_validation,
    assert_tone_consistency,
    audit_taxonomy_sort,
    audit_terms_to_verify_cross_reference,
    dedupe_quick_wins,
)


# BLUEPRINT_DEPS — engineering-process §4.6 hash-pinned citation block.
# Hashes computed 2026-04-29 at R1 landing. L-015 sweep currently scoped
# to ``pipeline.vault``; citation block is rendered in the canonical shape
# so a future scope-expansion picks up Editor cleanly.
BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_07_scribe.md": {
        "version": "v1.1.1",
        "hash_sha3_512_prefix16": "e793055d257ae56b",
        "sections_implemented": [
            "§7.5 SectionDraft schema (consumed via EditorInput.section_drafts dict shape)",
        ],
    },
    "section_00_5_section_07_scribe_amendment.md": {
        "version": "§0.5 v7",
        "hash_sha3_512_prefix16": "b99312d9a3ba3527",
        "sections_implemented": [
            "§A row 120 SectionDraft schema (input-side dict shape pin)",
        ],
    },
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§4.4 Editor invoke_seat contract (180_000 ms inline-literal timeout)",
            "§5.7 structured stderr single-line JSON on gate-trip",
        ],
    },
    "section_04_logician.md": {
        "version": "v2.1",
        "hash_sha3_512_prefix16": "b7e5439cac97b2fe",
        "sections_implemented": [
            "§4.2.1 PRE-gate slot table (F_EDITOR_ORG_CROSS_REF caller-supplied check)",
            "§4.2.1 POST-gate slot table (F-EDITOR-OUTPUT-SHAPE + F-EDITOR-REWROTE-INSTEAD-OF-FLAGGED + F-EDITOR-SINGLE-REPLACEMENT)",
        ],
    },
    "section_06_operating_envelope.md": {
        "version": "v1-r1",
        "hash_sha3_512_prefix16": "f4a55d9650489531",
        "sections_implemented": [
            "§6.13 V1 inline-literal rebind-resistance (180_000 ms timeout, 40% rewrite threshold)",
        ],
    },
    "skills/editor/SKILL.md": {
        "version": "v1",
        "hash_sha3_512_prefix16": "7d41fd4d809b3531",
        "contract": "JSON output schema lines 194-241 (readability/strengths/suggestions/gaps); 2-3 replacement invariant",
    },
}


__all__ = [
    # Input/output shapes
    "EditorInput",
    "EditorOutput",
    "EditorSkillInvocation",
    "FlaggedTerm",
    "ReplacementOption",
    "Miscategorization",
    "TaxonomyCheck",
    "ReadabilityFeedback",
    "ToneFeedback",
    "EditorGap",
    # Closed-set Literals
    "Dialect",
    "IssueType",
    "Severity",
    "ReplacementLabel",
    # Adapter surface
    "SkillLauncher",
    "SkillSubprocessResult",
    "invoke_editor_adapter",
    "parse_skill_output",
    "validate_editor_output_shape",
    # Adapter exceptions
    "EditorOutputShapeError",
    "EditorRewroteInsteadOfFlaggedError",
    "EditorSingleReplacementError",
    "EditorSkillSubprocessFail",
    "EditorSkillOutputMalformedJson",
    "EditorSkillTimeout",
    # Seat-layer surface
    "EditorEnvelope",
    "EditorSeatResult",
    "EditorEnvelopeMalformed",
    "EditorGateFailed",
    "ClockFn",
    "PreGateCallable",
    "PostGateCallable",
    "decode_envelope",
    "encode_result",
    "run_seat",
    "default_cross_org_pre_gate",
    "default_noop_post_gate",
    # Constants
    "ENVELOPE_VERSION_V1",
    "RESULT_VERSION_V1",
    "EXIT_OK",
    "EXIT_INTERNAL_ERROR",
    "EXIT_GATE_FAIL",
    # Failure-code constants
    "F_EDITOR_OUTPUT_SHAPE",
    "F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED",
    "F_EDITOR_SINGLE_REPLACEMENT",
    "F_EDITOR_SKILL_SUBPROCESS_FAIL",
    "F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON",
    "F_EDITOR_SKILL_TIMEOUT",
    "F_EDITOR_ENVELOPE_MALFORMED",
    "F_EDITOR_ORG_CROSS_REF",
    # R2 enhanced-validation surface
    "TAXONOMY_CATEGORIES",
    "ValidationReport",
    "apply_r2_validation",
    "assert_tone_consistency",
    "audit_taxonomy_sort",
    "audit_terms_to_verify_cross_reference",
    "dedupe_quick_wins",
    # Blueprint pin
    "BLUEPRINT_DEPS",
]
