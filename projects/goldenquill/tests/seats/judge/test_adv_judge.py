"""Adversarial tests for pipeline.seats.judge — R1 attack-surface enumeration.

Per spec card §10 + §15: many evidence-fabrication attack vectors are
documented at R1 but enforced at R3 by the Logician POST-gate
``F-JUDGE-EVIDENCE-NOT-IN-DRAFT``. R1 ships the failure-code constant +
this adversarial-surface enumeration so the R3 gate has a clear target.

Each test below either:
- documents an R3-deferred attack (LLM fabricates evidence that R1
  CANNOT detect; R3 gate scope), or
- enforces an R1-scope hardening (frozen mutability, BOM rejection,
  uppercase-hash rejection, score injection from extra LLM fields).

The R3-deferred tests assert the R1 behavior (passes through silently)
and document the R3 gate that would catch the attack.
"""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path

import pytest

from pipeline.seats.judge.dimension_scorer import score_dimension
from pipeline.seats.judge.rubric_loader import load_rubric
from pipeline.seats.judge.types import (
    CriterionScore,
    F_JUDGE_EVIDENCE_NOT_IN_DRAFT,
    F_JUDGE_SCORE_OUT_OF_BOUND,
    F_JUDGE_SCORE_UNPARSEABLE,
    Rubric,
    RubricCriterion,
)


UTC_NOW = datetime(2026, 4, 29, 12, 0, 0, tzinfo=timezone.utc)
SHA256_VALID = "0" * 64
REPO_ROOT = Path(__file__).resolve().parents[3]
LIVE_VAPG = REPO_ROOT / "pipeline" / "rubrics" / "vapg_fy26.json"


class _FakeDraft:
    def __init__(self, name: str, body: str):
        self.section_name = name
        self.section_order = 1
        self.body_text = body
        self.claim_evidence_map: tuple = ()


def _crit() -> RubricCriterion:
    return RubricCriterion(
        id="b",
        name="Q",
        max_points=20,
        scorer="review_panel",
        subcriteria=(),
        must_address=("foo",),
        tiers=({"points": 5, "description": "ok"},),
    )


def _make_llm(payload):
    body = json.dumps(payload) if not isinstance(payload, str) else payload

    def _call(*, prompt: str, max_tokens: int) -> str:
        return body

    return _call


# ---------------------------------------------------------------------------
# R3-deferred attack vectors — documents what R1 does NOT catch.
# ---------------------------------------------------------------------------


class TestR3DeferredEvidenceFabrication:
    """Each test below documents an evidence-fabrication attack that R1
    does NOT enforce. The Logician POST-gate
    ``F-JUDGE-EVIDENCE-NOT-IN-DRAFT`` (wired at R3) catches them.
    """

    def test_invented_quote_not_in_any_draft_passes_at_r1(self):
        # R3 gate: F-JUDGE-EVIDENCE-NOT-IN-DRAFT (POST-gate).
        # R1 emits the candidate score+quote without verifying.
        draft = _FakeDraft("Real section", "We grow gourmet mushrooms.")
        llm = _make_llm(
            {
                "score": 18,
                # Quote NOT a substring of body_text.
                "evidence_quote": "We pioneered solid-state fermentation.",
                "confidence": 0.95,
                "rationale": "Convincing claim",
            }
        )
        cs = score_dimension((draft,), _crit(), llm_call=llm, clock=lambda: UTC_NOW)
        # R1 accepts. R3 gate would reject this CriterionScore.
        assert cs.evidence_quote == "We pioneered solid-state fermentation."
        assert F_JUDGE_EVIDENCE_NOT_IN_DRAFT == "F-JUDGE-EVIDENCE-NOT-IN-DRAFT"

    def test_paraphrased_evidence_passes_at_r1(self):
        # R3 gate: F-JUDGE-EVIDENCE-NOT-IN-DRAFT — substring check rejects
        # paraphrased text.
        draft = _FakeDraft("S", "We grow gourmet mushrooms.")
        llm = _make_llm(
            {
                "score": 10,
                "evidence_quote": "The applicant cultivates premium fungi.",
                "confidence": 0.7,
                "rationale": "Paraphrase of body text",
            }
        )
        cs = score_dimension((draft,), _crit(), llm_call=llm, clock=lambda: UTC_NOW)
        assert "premium fungi" in cs.evidence_quote
        # R3 substring-in-body check fails. R1 silent pass-through.

    def test_cross_org_evidence_passes_at_r1(self):
        # R3 gate combined with Law 3 cross-org isolation: an evidence
        # quote from a different org's draft would be caught by Logician
        # PRE-gate F-SCRIBE-ORG-CROSS-REF + Judge POST-gate
        # F-JUDGE-EVIDENCE-NOT-IN-DRAFT. R1 has no org context and cannot
        # detect.
        my_draft = _FakeDraft("Mine", "My org grows shiitake.")
        llm = _make_llm(
            {
                "score": 12,
                # Quote belongs to a different org's draft (not in tuple).
                "evidence_quote": "Other org grows lion's mane.",
                "confidence": 0.6,
                "rationale": "From wrong org",
            }
        )
        cs = score_dimension((my_draft,), _crit(), llm_call=llm, clock=lambda: UTC_NOW)
        assert "Other org" in cs.evidence_quote

    def test_quote_from_rfa_not_draft_passes_at_r1(self):
        # R3 gate substring-checks against SectionDraft.body_text only;
        # quote-from-RFA is rejected.
        draft = _FakeDraft("S", "We grow gourmet mushrooms.")
        llm = _make_llm(
            {
                "score": 8,
                # This is RFA-text, not draft-text.
                "evidence_quote": "must be ready for implementation",
                "confidence": 0.55,
                "rationale": "Quoted from RFA",
            }
        )
        cs = score_dimension((draft,), _crit(), llm_call=llm, clock=lambda: UTC_NOW)
        assert "ready for implementation" in cs.evidence_quote


class TestR3DeferredHashDrift:
    def test_rubric_hash_drift_mid_flight_documented_for_r3(self, tmp_path):
        # R3 PRE-gate F-JUDGE-RUBRIC-HASH-DRIFT re-hashes on every
        # invocation. R1 only records the load-time hash. If the on-disk
        # rubric changes between load and audit, R1 cannot detect drift
        # at that point — that detection is the R3 gate.
        original = json.loads(LIVE_VAPG.read_text())
        p = tmp_path / "v1.json"
        p.write_text(json.dumps(original), encoding="utf-8")
        v1 = load_rubric(p, clock=lambda: UTC_NOW)
        # Mutate the on-disk file post-load.
        modified = dict(original)
        modified["meta"] = dict(original["meta"])
        modified["meta"]["nofo_number"] = "DRIFTED-001"
        p.write_text(json.dumps(modified), encoding="utf-8")
        v2 = load_rubric(p, clock=lambda: UTC_NOW)
        # Hashes differ, but v1's pinned hash is unchanged in-memory.
        assert v1.rubric_sha256 != v2.rubric_sha256
        # R1 ships the constant; R3 wires the gate.
        from pipeline.seats.judge.types import F_JUDGE_RUBRIC_HASH_DRIFT
        assert F_JUDGE_RUBRIC_HASH_DRIFT == "F-JUDGE-RUBRIC-HASH-DRIFT"


# ---------------------------------------------------------------------------
# R1-scope hardenings
# ---------------------------------------------------------------------------


class TestR1Hardenings:
    def test_score_injection_extra_field_silently_ignored(self):
        # LLM injects extra fields trying to override behavior. R1 parser
        # ignores them — no field-leakage to CriterionScore.
        draft = _FakeDraft("S", "body")
        llm = _make_llm(
            {
                "score": 5,
                "evidence_quote": "body",
                "confidence": 0.5,
                "rationale": "ok",
                "override_max_points": 999,
                "max_points": 50,  # tries to override criterion max
                "criterion_id": "WRONG",  # tries to override id
            }
        )
        cs = score_dimension((draft,), _crit(), llm_call=llm, clock=lambda: UTC_NOW)
        assert cs.criterion_id == "b"  # source of truth: criterion arg
        assert cs.score == 5

    def test_object_setattr_on_frozen_rubric_raises(self):
        r = Rubric(
            program_code="P",
            funder="F",
            nofo_number="N",
            max_score=30,
            min_score=0,
            criteria=(_crit(),),
            rubric_sha256=SHA256_VALID,
            loaded_at_utc=UTC_NOW,
        )
        # __setattr__ on slots-equipped frozen dataclass raises.
        with pytest.raises(FrozenInstanceError):
            r.max_score = 999  # type: ignore[misc]

    def test_setattr_unknown_field_rejected_by_slots(self):
        # slots=True prevents adding undeclared attributes — defense
        # against a downstream consumer trying to bolt-on side data.
        r = Rubric(
            program_code="P",
            funder="F",
            nofo_number="N",
            max_score=30,
            min_score=0,
            criteria=(_crit(),),
            rubric_sha256=SHA256_VALID,
            loaded_at_utc=UTC_NOW,
        )
        with pytest.raises((AttributeError, FrozenInstanceError, TypeError)):
            r.unknown_extra_field = "leak"  # type: ignore[attr-defined]

    def test_uppercase_hex_in_rubric_sha256_rejected(self):
        with pytest.raises(ValueError, match="must be lowercase hex"):
            Rubric(
                program_code="P",
                funder="F",
                nofo_number="N",
                max_score=30,
                min_score=0,
                criteria=(_crit(),),
                rubric_sha256="A" * 64,
                loaded_at_utc=UTC_NOW,
            )

    def test_bom_in_rubric_file_rejected(self, tmp_path):
        # Canonical-bytes discipline: a BOM produces different bytes than
        # the BOM-stripped version, so silently stripping would let a
        # BOM/no-BOM pair drift past hash comparison.
        p = tmp_path / "bom.json"
        p.write_bytes(b"\xef\xbb\xbf{}")
        with pytest.raises(ValueError, match="UTF-8 BOM"):
            load_rubric(p, clock=lambda: UTC_NOW)

    def test_negative_score_rejected_at_dataclass(self):
        # Even if the scorer somehow constructs a negative-score
        # CriterionScore, the dataclass __post_init__ refuses.
        with pytest.raises(ValueError, match="score must be >= 0"):
            CriterionScore(
                criterion_id="b",
                score=-1,
                evidence_quote="body",
                confidence=0.5,
                rationale="ok",
            )

    def test_llm_returns_fenced_json_with_language_tag(self):
        # Defends against ```json fences from confabulating LLMs.
        draft = _FakeDraft("S", "body")
        body = (
            "```json\n"
            + json.dumps(
                {
                    "score": 7,
                    "evidence_quote": "body",
                    "confidence": 0.5,
                    "rationale": "ok",
                }
            )
            + "\n```"
        )
        llm = _make_llm(body)
        cs = score_dimension((draft,), _crit(), llm_call=llm, clock=lambda: UTC_NOW)
        assert cs.score == 7

    def test_llm_returns_fenced_json_inline_form(self):
        draft = _FakeDraft("S", "body")
        # Single-line ```json{...}``` form (no newline after fence).
        body = (
            "```json"
            + json.dumps(
                {
                    "score": 5,
                    "evidence_quote": "body",
                    "confidence": 0.5,
                    "rationale": "ok",
                }
            )
            + "```"
        )
        llm = _make_llm(body)
        cs = score_dimension((draft,), _crit(), llm_call=llm, clock=lambda: UTC_NOW)
        assert cs.score == 5

    def test_rubric_with_both_subcriteria_and_tiers_empty_rejected(self):
        with pytest.raises(ValueError, match="incoherent"):
            RubricCriterion(
                id="x",
                name="X",
                max_points=10,
                scorer="review_panel",
                subcriteria=(),
                must_address=(),
                tiers=(),
            )

    def test_score_out_of_bound_carries_f_code(self):
        draft = _FakeDraft("S", "body")
        llm = _make_llm(
            {
                "score": 99,
                "evidence_quote": "body",
                "confidence": 0.5,
                "rationale": "ok",
            }
        )
        with pytest.raises(ValueError) as exc:
            score_dimension(
                (draft,), _crit(), llm_call=llm, clock=lambda: UTC_NOW
            )
        assert F_JUDGE_SCORE_OUT_OF_BOUND in str(exc.value)

    def test_unparseable_carries_f_code(self):
        draft = _FakeDraft("S", "body")
        llm = _make_llm("garbage non-json")
        with pytest.raises(ValueError) as exc:
            score_dimension(
                (draft,), _crit(), llm_call=llm, clock=lambda: UTC_NOW
            )
        assert F_JUDGE_SCORE_UNPARSEABLE in str(exc.value)
