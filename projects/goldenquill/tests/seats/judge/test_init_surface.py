"""Tests for pipeline.seats.judge.__init__ — public surface + BLUEPRINT_DEPS.

Covers:
- __all__ exports exactly the names listed in the R1 + R2 spec cards §4.
- Each exported symbol resolves to a truthy / non-None object.
- BLUEPRINT_DEPS pins the spec-card anchors with sha3_512 prefix16
  (R1 anchors + R2 additions: section_draft.py + interface_index.md).
- BLUEPRINT_DEPS hashes match the on-disk file bytes (L-015 lineage).
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pipeline.seats.judge as judge


REPO_ROOT = Path(__file__).resolve().parents[3]


EXPECTED_PUBLIC = {
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
}


class TestPublicSurface:
    def test_all_matches_expected_set(self):
        assert set(judge.__all__) == EXPECTED_PUBLIC

    def test_all_is_list_or_tuple(self):
        # Tuple/list both acceptable; precedent in seat __init__ is list.
        assert isinstance(judge.__all__, (list, tuple))

    def test_all_no_duplicates(self):
        assert len(set(judge.__all__)) == len(judge.__all__)

    def test_each_symbol_resolves(self):
        for name in EXPECTED_PUBLIC:
            obj = getattr(judge, name, None)
            assert obj is not None, f"Public symbol {name!r} is None on import."


class TestBlueprintDepsPin:
    def test_blueprint_deps_is_dict(self):
        assert isinstance(judge.BLUEPRINT_DEPS, dict)

    def test_five_anchor_keys_present(self):
        keys = set(judge.BLUEPRINT_DEPS.keys())
        # R1 anchors (still required at R2).
        assert "vapg_fy26.json" in keys
        assert "section_07_scribe.md" in keys
        assert "tilth_architecture_locked.md" in keys
        assert "skills/judge-rubric/SKILL.md" in keys
        assert "pipeline/engineering/agents/judge_scoring_agent_v1.md" in keys

    def test_r2_anchor_keys_present(self):
        keys = set(judge.BLUEPRINT_DEPS.keys())
        # R2 additions per the R2 spec card §1 BLUEPRINT_DEPS pin.
        assert "pipeline/seats/scribe/section_draft.py" in keys
        assert "section_00_5_interface_index.md" in keys

    def test_each_entry_has_required_subkeys(self):
        for key, entry in judge.BLUEPRINT_DEPS.items():
            assert "version" in entry
            assert "hash_sha3_512_prefix16" in entry
            assert "sections_implemented" in entry
            prefix = entry["hash_sha3_512_prefix16"]
            assert isinstance(prefix, str)
            assert len(prefix) == 16
            assert all(ch in "0123456789abcdef" for ch in prefix)

    def test_vapg_rubric_hash_matches_disk(self):
        path = REPO_ROOT / "pipeline" / "rubrics" / "vapg_fy26.json"
        actual = hashlib.sha3_512(path.read_bytes()).hexdigest()[:16]
        assert (
            judge.BLUEPRINT_DEPS["vapg_fy26.json"]["hash_sha3_512_prefix16"]
            == actual
        )

    def test_scribe_blueprint_hash_matches_disk(self):
        path = (
            REPO_ROOT / "pipeline" / "blueprint" / "v0.1" / "section_07_scribe.md"
        )
        actual = hashlib.sha3_512(path.read_bytes()).hexdigest()[:16]
        assert (
            judge.BLUEPRINT_DEPS["section_07_scribe.md"]["hash_sha3_512_prefix16"]
            == actual
        )

    def test_architecture_hash_matches_disk(self):
        path = (
            REPO_ROOT
            / "pipeline"
            / "architecture"
            / "v0.1"
            / "tilth_architecture_locked.md"
        )
        actual = hashlib.sha3_512(path.read_bytes()).hexdigest()[:16]
        assert (
            judge.BLUEPRINT_DEPS["tilth_architecture_locked.md"][
                "hash_sha3_512_prefix16"
            ]
            == actual
        )

    def test_skill_hash_matches_disk(self):
        path = REPO_ROOT / "skills" / "judge-rubric" / "SKILL.md"
        actual = hashlib.sha3_512(path.read_bytes()).hexdigest()[:16]
        assert (
            judge.BLUEPRINT_DEPS["skills/judge-rubric/SKILL.md"][
                "hash_sha3_512_prefix16"
            ]
            == actual
        )

    def test_agent_hash_matches_disk(self):
        path = (
            REPO_ROOT
            / "pipeline"
            / "engineering"
            / "agents"
            / "judge_scoring_agent_v1.md"
        )
        actual = hashlib.sha3_512(path.read_bytes()).hexdigest()[:16]
        assert (
            judge.BLUEPRINT_DEPS[
                "pipeline/engineering/agents/judge_scoring_agent_v1.md"
            ]["hash_sha3_512_prefix16"]
            == actual
        )

    def test_section_draft_hash_matches_disk(self):
        path = (
            REPO_ROOT / "pipeline" / "seats" / "scribe" / "section_draft.py"
        )
        actual = hashlib.sha3_512(path.read_bytes()).hexdigest()[:16]
        assert (
            judge.BLUEPRINT_DEPS["pipeline/seats/scribe/section_draft.py"][
                "hash_sha3_512_prefix16"
            ]
            == actual
        )

    def test_interface_index_hash_matches_disk(self):
        path = (
            REPO_ROOT
            / "pipeline"
            / "blueprint"
            / "v0.1"
            / "section_00_5_interface_index.md"
        )
        actual = hashlib.sha3_512(path.read_bytes()).hexdigest()[:16]
        assert (
            judge.BLUEPRINT_DEPS["section_00_5_interface_index.md"][
                "hash_sha3_512_prefix16"
            ]
            == actual
        )


class TestRoundTripUsage:
    def test_load_score_compose_judge_output(self, tmp_path):
        """End-to-end round trip: load rubric → score one dimension via
        fake LLM → manually construct JudgeOutput. Hash propagates."""
        import json
        from datetime import datetime, timezone

        rubric_path = REPO_ROOT / "pipeline" / "rubrics" / "vapg_fy26.json"
        clock = lambda: datetime(2026, 4, 29, tzinfo=timezone.utc)
        rubric = judge.load_rubric(rubric_path, clock=clock)

        crit_b = next(c for c in rubric.criteria if c.id == "b")

        class _Draft:
            section_name = "Personnel"
            section_order = 1
            body_text = "Lead has 15 years experience."
            claim_evidence_map: tuple = ()

        def _llm(*, prompt: str, max_tokens: int) -> str:
            return json.dumps(
                {
                    "score": 18,
                    "evidence_quote": "Lead has 15 years experience.",
                    "confidence": 0.92,
                    "rationale": "Strong qualifications",
                }
            )

        cs = judge.score_dimension(
            (_Draft(),), crit_b, llm_call=_llm, clock=clock
        )

        jo = judge.JudgeOutput(
            criterion_scores=(cs,),
            total_score=cs.score,
            max_total=crit_b.max_points,
            rubric_sha256=rubric.rubric_sha256,
            rfa_content_sha3_512="0" * 128,
            scored_at_utc=clock(),
        )
        # The rubric_sha256 propagated through the round trip — this is
        # the audit-traceability property the spec card pins.
        assert jo.rubric_sha256 == rubric.rubric_sha256
