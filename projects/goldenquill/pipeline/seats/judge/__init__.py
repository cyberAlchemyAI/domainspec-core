"""pipeline.seats.judge — §9 Judge scoring seat.

R1 spec card: ``pipeline/engineering/spec_cards/section_09_judge_round_1_types_and_rubric_primitives.md``
(PRE-STAGED 2026-04-21; LOCKED 2026-04-29 self-LOCK cycle-1 per Round 1
single-cycle precedent — Scribe R1 LOCK + §5 R1-foundations precedent).

R2 spec card: ``pipeline/engineering/spec_cards/section_09_judge_round_2_cross_rubric_and_verdict.md``
(PRE-STAGED 2026-04-29; LOCKED 2026-04-29 self-LOCK cycle-1 — same single-cycle
precedent; pure-deterministic stdlib + intra-package composition over R1).

Round 1: types + rubric loader + dimension-scorer primitive.
Pure-deterministic; zero LLM, zero network, zero subprocess.

Round 2 (this tranche): cross-rubric dispatcher + responsiveness mapper +
:class:`JudgeVerdict` assembler. Pure composition over R1 — still zero LLM,
zero network, zero subprocess. Adds the verbatim evidence-in-draft pre-check
(Law 5 enforcement at assembly time; R3 wires the Logician POST-gate).

Future rounds:

- **Round 3** — ``seat.py`` subprocess entry, Google Gemini 2.5 Pro
  provider binding, Logician PRE/POST gate wiring (notably
  ``F-JUDGE-EVIDENCE-NOT-IN-DRAFT`` enforcing Law 5 evidence-in-draft
  discipline), SFR format emission, cross-family collision PRE-gate.

Cross-family rigor: Judge production binding = ``google/gemini-2.5-pro``
per ``router.yaml``. Any committee dispatch reviewing Judge code MUST
substitute any Google-family reviewer to a non-Google family
(``codex`` / ``qwen3-32b`` / ``llama-3.3-70b`` / ``gpt-oss-120b`` /
``kimi-k2``).

Five Operating Laws — Judge enforcement:

- Law 5 (Applicant brings the substance) — ``CriterionScore.evidence_quote``
  must be a verbatim substring of at least one
  ``SectionDraftLike.body_text`` in ``JudgeInput.section_drafts``. R1
  ships the ``F_JUDGE_EVIDENCE_NOT_IN_DRAFT`` failure-code constant +
  the attack-surface adversarial documentation; R3 wires the enforcing
  Logician POST-gate.

Import discipline (R1):

- ``pipeline.seats.judge.*`` imports stdlib + intra-package only.
- No ``pipeline.logician`` / ``pipeline.vault`` / ``pipeline.providers``
  imports until R3 wiring.
- Forward-Protocols (``SectionDraftLike``, ``ClaimEvidenceLike``,
  ``LLMCallFn``) replace concrete imports of Scribe R3's
  ``SectionDraft`` and provider modules at R1.
"""

from __future__ import annotations

from typing import Final

from pipeline.seats.judge.cross_rubric_dispatch import (
    dispatch_criteria_to_scorers,
    dispatch_score_units,
    parent_criterion_for_unit,
)
from pipeline.seats.judge.dimension_scorer import (
    ClockFn,
    score_dimension,
)
from pipeline.seats.judge.logician_wiring import (
    CedarCrossOrgCheck,
    JudgePostGateAssembly,
    JudgePreGateAssembly,
    RubricHashRecompute,
    assemble_judge_post_gate,
    assemble_judge_pre_gate,
)
from pipeline.seats.judge.provider_google import (
    F_JUDGE_BYOK_MISSING,
    F_JUDGE_PAYLOAD_CEILING,
    F_JUDGE_PROVIDER_MALFORMED,
    F_JUDGE_SEMANTIC_FAILURE,
    F_JUDGE_TRANSPORT_FAILURE,
    GoogleBYOKMissing,
    GoogleBinding,
    GoogleCallCallable,
    GooglePayloadCeiling,
    GoogleProviderMalformed,
    GoogleResponse,
    GoogleSemanticFailure,
    GoogleTransportFailure,
    call_google_judge,
    load_judge_binding_from_router_mapping,
)
from pipeline.seats.judge.responsiveness_mapper import (
    KNOWN_RESPONSIVENESS_FACTOR_KEYS,
    build_responsiveness_map,
    extract_responsiveness_factors_from_rubric_json,
)
from pipeline.seats.judge.rubric_loader import (
    compute_rubric_sha256,
    load_rubric,
)
from pipeline.seats.judge.seat import (
    ENVELOPE_VERSION_V1,
    EXIT_GATE_FAIL,
    EXIT_INTERNAL_ERROR,
    EXIT_OK,
    F_JUDGE_CROSS_FAMILY_COLLISION,
    F_JUDGE_ENVELOPE_MALFORMED,
    F_JUDGE_ORG_CROSS_REF,
    F_JUDGE_RUBRIC_LOAD_FAIL,
    F_JUDGE_SCORE_ORCHESTRATION_FAIL,
    RESULT_VERSION_V1,
    JudgeEnvelope,
    JudgeEnvelopeMalformed,
    JudgeGateFailed,
    JudgeResult,
    decode_envelope,
    encode_result,
    run_seat,
)
from pipeline.seats.judge.sfr_emitter import (
    SFR_BLOCK_NAMES,
    SfrLineItem,
    SfrReport,
    emit_sfr,
    render_sfr_text,
)
from pipeline.seats.judge.types import (
    F_JUDGE_CRITERION_MISSING,
    F_JUDGE_EVIDENCE_NOT_IN_DRAFT,
    F_JUDGE_RUBRIC_HASH_DRIFT,
    F_JUDGE_RUBRIC_MALFORMED,
    F_JUDGE_SCORE_OUT_OF_BOUND,
    F_JUDGE_SCORE_UNPARSEABLE,
    ClaimEvidenceLike,
    CriterionScore,
    JudgeInput,
    JudgeOutput,
    JudgeVerdict,
    LLMCallFn,
    ResponsivenessEntry,
    ResponsivenessMap,
    Rubric,
    RubricCriterion,
    RubricScorerRole,
    RubricSubCriterion,
    SectionDraftLike,
)
from pipeline.seats.judge.verdict_assembler import (
    assemble_verdict,
)


# ---------------------------------------------------------------------------
# BLUEPRINT_DEPS — engineering-process §4.6 hash-pinned citation block.
# Hashes computed 2026-04-29 at R1 landing (sha3_512 prefix16 over the
# canonical file bytes).
# ---------------------------------------------------------------------------

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "vapg_fy26.json": {
        "version": "extracted-2026-04-12 (LOCKed de-facto by operator)",
        "hash_sha3_512_prefix16": "0993e19979ea07d9",
        "sections_implemented": [
            "VAPG FY26 rubric JSON shape — happy-path fixture for "
            "rubric_loader (100 pts; 7 criteria a/b/c/d/e/f/g; "
            "criteria a + f have subcriteria)",
        ],
    },
    "section_07_scribe.md": {
        # Substantive body: v1.1.1 LOCKED 2026-04-21 (unchanged).
        # Hash refreshed 2026-05-15 after non-substantive parent_locks
        # header additions for v7.0.7 (2026-05-10) and v7.0.10
        # (2026-05-11) — footer-addendum discipline per architecture
        # v7.0.7 §8.3. Substantive Scribe body is unchanged; the pin
        # tracks current bytes so future drift detection stays meaningful.
        "version": "v1.1.1 (header parent_locks refreshed)",
        "hash_sha3_512_prefix16": "b33146a4c13a3013",
        "sections_implemented": [
            "§7.5 SectionDraft surface — forward-Protocol "
            "SectionDraftLike anticipates the four fields Judge reads "
            "(section_name / section_order / body_text / "
            "claim_evidence_map); Judge R2 binds the Protocol to the "
            "concrete pipeline.seats.scribe.section_draft.SectionDraft "
            "via the E-026 __module__ lineage assertion test",
            "§7.2 Law 5 evidence-sourcing posture — Judge mirrors on "
            "the scoring side via F-JUDGE-EVIDENCE-NOT-IN-DRAFT (R2 "
            "verbatim-substring pre-check at verdict_assembler; R3 "
            "wires the enforcing Logician POST-gate)",
        ],
    },
    "pipeline/seats/scribe/section_draft.py": {
        "version": "Scribe R2.5 LOCKED 2026-04-22",
        "hash_sha3_512_prefix16": "c4a8dd0e9a4c4ef6",
        "sections_implemented": [
            "Concrete SectionDraft import target for the E-026 "
            "__module__ lineage bind exercised at "
            "tests/seats/judge/test_e026_section_draft_bind.py",
        ],
    },
    "section_00_5_interface_index.md": {
        "version": "current",
        "hash_sha3_512_prefix16": "e2eb52c57b2d54da",
        "sections_implemented": [
            "pipeline.contract.judge row — STUB pending §9 blueprint; "
            "R2 lands JudgeVerdict + JudgeInput + dispatch contract in "
            "code, §0.5 row population deferred to §9 blueprint LOCK",
        ],
    },
    "tilth_architecture_locked.md": {
        "version": "v7 LOCKED 2026-04-19",
        "hash_sha3_512_prefix16": "2ff40734a399eb9f",
        "sections_implemented": [
            "§D.4 Judge role — cross-family rigor against Scribe's "
            "production binding (Anthropic) and against Judge's own "
            "production binding (Google)",
            "§E cross-family guard — Judge committee carve-out: "
            "reviewer family ≠ Google",
            "§F.1 SFR format — Judge is NOT SFR-exempt; R3 emission "
            "land",
        ],
    },
    "skills/judge-rubric/SKILL.md": {
        "version": "port-source attestation",
        "hash_sha3_512_prefix16": "cdcb840cab093f82",
        "sections_implemented": [
            "12-dimension 90+ rubric semantics — port source per "
            "parent OQ-1 resolution (Judge = FULL PORT)",
        ],
    },
    "pipeline/engineering/agents/judge_scoring_agent_v1.md": {
        "version": "v2 (port-source attestation)",
        "hash_sha3_512_prefix16": "a64fc93e7c7451a6",
        "sections_implemented": [
            "G-Eval scoring protocol + calibration anchors — port "
            "source per parent OQ-1 resolution",
        ],
    },
}


__all__ = [
    # Rubric shapes
    "Rubric",
    "RubricCriterion",
    "RubricSubCriterion",
    "RubricScorerRole",
    # Scoring shapes
    "CriterionScore",
    "JudgeInput",
    "JudgeOutput",
    # R2 verdict + responsiveness shapes
    "JudgeVerdict",
    "ResponsivenessEntry",
    "ResponsivenessMap",
    # Forward-Protocols
    "SectionDraftLike",
    "ClaimEvidenceLike",
    "LLMCallFn",
    # Rubric primitives
    "load_rubric",
    "compute_rubric_sha256",
    # Dimension primitive
    "score_dimension",
    "ClockFn",
    # R2 dispatch primitives
    "dispatch_criteria_to_scorers",
    "dispatch_score_units",
    "parent_criterion_for_unit",
    # R2 responsiveness primitives
    "KNOWN_RESPONSIVENESS_FACTOR_KEYS",
    "build_responsiveness_map",
    "extract_responsiveness_factors_from_rubric_json",
    # R2 verdict assembler
    "assemble_verdict",
    # R3 provider_google
    "GoogleBinding",
    "GoogleResponse",
    "GoogleCallCallable",
    "call_google_judge",
    "load_judge_binding_from_router_mapping",
    "GoogleBYOKMissing",
    "GoogleTransportFailure",
    "GoogleSemanticFailure",
    "GooglePayloadCeiling",
    "GoogleProviderMalformed",
    # R3 SFR emitter
    "SFR_BLOCK_NAMES",
    "SfrLineItem",
    "SfrReport",
    "emit_sfr",
    "render_sfr_text",
    # R3 seat subprocess entry
    "JudgeEnvelope",
    "JudgeResult",
    "JudgeGateFailed",
    "JudgeEnvelopeMalformed",
    "decode_envelope",
    "encode_result",
    "run_seat",
    "ENVELOPE_VERSION_V1",
    "RESULT_VERSION_V1",
    "EXIT_OK",
    "EXIT_INTERNAL_ERROR",
    "EXIT_GATE_FAIL",
    # R3 logician_wiring
    "CedarCrossOrgCheck",
    "RubricHashRecompute",
    "JudgePreGateAssembly",
    "JudgePostGateAssembly",
    "assemble_judge_pre_gate",
    "assemble_judge_post_gate",
    # F-code constants (§9 R1)
    "F_JUDGE_RUBRIC_MALFORMED",
    "F_JUDGE_CRITERION_MISSING",
    "F_JUDGE_SCORE_UNPARSEABLE",
    "F_JUDGE_EVIDENCE_NOT_IN_DRAFT",
    "F_JUDGE_SCORE_OUT_OF_BOUND",
    "F_JUDGE_RUBRIC_HASH_DRIFT",
    # F-code constants (§9 R3)
    "F_JUDGE_BYOK_MISSING",
    "F_JUDGE_TRANSPORT_FAILURE",
    "F_JUDGE_SEMANTIC_FAILURE",
    "F_JUDGE_PAYLOAD_CEILING",
    "F_JUDGE_PROVIDER_MALFORMED",
    "F_JUDGE_ENVELOPE_MALFORMED",
    "F_JUDGE_CROSS_FAMILY_COLLISION",
    "F_JUDGE_ORG_CROSS_REF",
    "F_JUDGE_RUBRIC_LOAD_FAIL",
    "F_JUDGE_SCORE_ORCHESTRATION_FAIL",
    # Blueprint pin
    "BLUEPRINT_DEPS",
]
