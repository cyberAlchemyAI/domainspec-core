"""Round-3 tests for ``pipeline.seats.scribe.logician_wiring``.

Exercises the PRE-gate assembler (8 checks) and POST-gate assembler
(11 checks + global admin-risk) with E-017-injected stub seams.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Mapping

import pytest

from pipeline.seats.scribe.admin_risk_adapter import (
    AdminRiskEntry,
    AdminRiskRegister,
)
from pipeline.seats.scribe.logician_wiring import (
    PostGateAssembly,
    PreGateAssembly,
    assemble_scribe_post_gate,
    assemble_scribe_pre_gate,
)
from pipeline.seats.scribe.section_draft import (
    AdminRiskFlag,
    ClaimEvidence,
    ConversationAnchor,
    EligibleActivityMatch,
    SectionDraft,
    SectionLimit,
)
from pipeline.seats.scribe.seat import (
    F_SCRIBE_CONVERSATION_ANCHOR_INVALID,
    F_SCRIBE_DIALECT_DRIFT,
    F_SCRIBE_DIALECT_INDUCED_IDENTITY,
    F_SCRIBE_DIALECT_UNCLASSIFIED,
    F_SCRIBE_INELIGIBLE_ACTIVITY,
    F_SCRIBE_ORG_CROSS_REF,
    F_SCRIBE_OVERLOOKED_EXPENSE_UNRESOLVED,
    F_SCRIBE_PARAPHRASED_NUMERIC,
    F_SCRIBE_SCOPE_MISSING,
    F_SCRIBE_SECTION_OVER_LIMIT_UNFLAGGED,
    F_SCRIBE_TEMPLATE_DRIFT,
    F_SCRIBE_TEMPLATE_UNKNOWN,
    F_SCRIBE_UNSOURCED_CLAIM,
    ScribeEnvelope,
    ScribeGateFailed,
    decode_envelope,
)


_SHELL_HASH_128 = "a" * 128
_FIXED_NOW = datetime(2026, 4, 22, 12, 0, tzinfo=timezone.utc)


def _make_envelope(**overrides: Any) -> ScribeEnvelope:
    base = {
        "envelope_version": "scribe-envelope.v1",
        "run_id": "run-1",
        "org_slug": "fit_farms_llc",
        "iteration_number": 0,
        "section_name": "Project Narrative",
        "section_order": 1,
        "funder_dialect": "conservative",
        "operator_override_dialect": None,
        "program_code": "VAPG",
        "admin_risk_register_snapshot_path": "/v/admin_risk.yaml",
        "admin_risk_snapshot_age_hours": 0.5,
        "conversation_log_anchor": None,
        "compiled_prompt_shell_sha3_512": _SHELL_HASH_128,
        "compiled_prompt": "Draft.",
        "project_context": {"applicant_name": "FIT Farms"},
        "envelope_emitted_at_utc": "2026-04-22T12:00:00+00:00",
    }
    base.update(overrides)
    return decode_envelope(raw_bytes=json.dumps(base).encode("utf-8"))


def _make_register(*, age: float = 0.5) -> AdminRiskRegister:
    return AdminRiskRegister(
        version="2.2",
        entries=(
            AdminRiskEntry(
                term="diversity",
                severity="medium",
                progressive_register="OK",
                suggested_substitutions=("inclusion",),
                context="",
                variants=(),
            ),
        ),
        snapshot_sha3_512="b" * 128,
        snapshot_age_hours=age,
    )


# ---------------------------------------------------------------------------
# Stub seams
# ---------------------------------------------------------------------------


def _no_foreign_orgs(**kwargs):
    return ()


def _kgie_pass(*, envelope):
    return "pass"


def _no_rfa_drift(*, envelope):
    return False


def _no_template_drift(*, envelope):
    return False


def _no_unsourced(**kwargs):
    return ()


def _no_anchor_mismatch(*, anchor, run_id):
    return False


def _empty_evidence_text(*, envelope):
    return ""


def _no_identity_claims(*, envelope):
    return ()


# ---------------------------------------------------------------------------
# PRE-gate
# ---------------------------------------------------------------------------


class TestPreGate:

    def _run(self, envelope=None, **overrides) -> PreGateAssembly:
        if envelope is None:
            envelope = _make_envelope()
        kwargs = dict(
            envelope=envelope,
            admin_risk_register=_make_register(),
            cedar_cross_org_check=_no_foreign_orgs,
            kgie_status_getter=_kgie_pass,
            rfa_drift_check=_no_rfa_drift,
            template_drift_check=_no_template_drift,
        )
        kwargs.update(overrides)
        return assemble_scribe_pre_gate(**kwargs)

    def test_happy_path_returns_assembly(self):
        out = self._run()
        assert isinstance(out, PreGateAssembly)
        assert F_SCRIBE_ORG_CROSS_REF in out.codes_checked
        assert "F-SCRIBE-KGIE-FAIL" in out.codes_checked

    def test_org_cross_ref_trips(self):
        def _foreign(**kwargs):
            return ("competitor_org",)

        with pytest.raises(ScribeGateFailed) as exc:
            self._run(cedar_cross_org_check=_foreign)
        assert exc.value.failure_code == F_SCRIBE_ORG_CROSS_REF
        assert "competitor_org" in str(exc.value.evidence)

    def test_kgie_fail_trips(self):
        def _kgie_fail(*, envelope):
            return "fail"

        with pytest.raises(ScribeGateFailed) as exc:
            self._run(kgie_status_getter=_kgie_fail)
        assert exc.value.failure_code == "F-SCRIBE-KGIE-FAIL"

    def test_kgie_needs_operator_input_no_override_trips(self):
        def _needs(*, envelope):
            return "needs_operator_input"

        with pytest.raises(ScribeGateFailed) as exc:
            self._run(kgie_status_getter=_needs)
        assert exc.value.failure_code == F_SCRIBE_SCOPE_MISSING

    def test_kgie_needs_operator_input_with_override_passes(self):
        def _needs(*, envelope):
            return "needs_operator_input"

        env = _make_envelope(operator_override_dialect="conservative")
        out = self._run(envelope=env, kgie_status_getter=_needs)
        assert isinstance(out, PreGateAssembly)

    def test_rfa_drift_trips(self):
        def _drift(*, envelope):
            return True

        with pytest.raises(ScribeGateFailed) as exc:
            self._run(rfa_drift_check=_drift)
        assert exc.value.failure_code == "F-SCRIBE-RFA-DRIFT"

    def test_template_unknown_trips(self):
        env = _make_envelope(program_code="UNREGISTERED-PROGRAM")
        with pytest.raises(ScribeGateFailed) as exc:
            self._run(envelope=env)
        assert exc.value.failure_code == F_SCRIBE_TEMPLATE_UNKNOWN

    def test_template_drift_trips(self):
        def _drift(*, envelope):
            return True

        with pytest.raises(ScribeGateFailed) as exc:
            self._run(template_drift_check=_drift)
        assert exc.value.failure_code == F_SCRIBE_TEMPLATE_DRIFT

    def test_admin_risk_envelope_age_over_24_trips(self):
        env = _make_envelope(admin_risk_snapshot_age_hours=24.5)
        with pytest.raises(ScribeGateFailed) as exc:
            self._run(envelope=env)
        assert exc.value.failure_code == "F-SCRIBE-ADMIN-RISK-REGISTER-STALE"

    def test_admin_risk_register_age_mismatch_trips(self):
        with pytest.raises(ScribeGateFailed) as exc:
            self._run(admin_risk_register=_make_register(age=99.0))
        assert exc.value.failure_code == "F-SCRIBE-ADMIN-RISK-REGISTER-STALE"


# ---------------------------------------------------------------------------
# POST-gate fixtures
# ---------------------------------------------------------------------------


def _section_draft(
    *,
    body_text: str = "FIT Farms operates a regenerative cooperative.",
    section_name: str = "Project Narrative",
    draft_dialect: str = "conservative",
    over_limit_flag: bool = False,
    rfa_section_limit: SectionLimit | None = None,
    word_count: int | None = None,
    character_count: int | None = None,
    eligible_activity_map: tuple[EligibleActivityMatch, ...] = (),
    claim_evidence_map: tuple[ClaimEvidence, ...] = (),
) -> SectionDraft:
    if word_count is None:
        word_count = len(body_text.split())
    if character_count is None:
        character_count = len(body_text)
    return SectionDraft(
        section_name=section_name,
        section_order=1,
        body_text=body_text,
        word_count=word_count,
        character_count=character_count,
        over_limit_flag=over_limit_flag,
        rfa_section_limit=rfa_section_limit,
        draft_dialect=draft_dialect,
        drafted_at_utc=_FIXED_NOW,
        claim_evidence_map=claim_evidence_map,
        eligible_activity_map=eligible_activity_map,
        admin_risk_flags=(),
        scope_check_comments=(),
    )


class TestPostGate:

    def _run(self, *, drafts=None, **overrides) -> PostGateAssembly:
        if drafts is None:
            drafts = (_section_draft(),)
        envelope = overrides.pop("envelope", _make_envelope())
        kwargs = dict(
            envelope=envelope,
            section_drafts=drafts,
            admin_risk_flags=(),
            admin_risk_register=_make_register(),
            source_tag_verify=_no_unsourced,
            conversation_anchor_verify=_no_anchor_mismatch,
            evidence_text_provider=_empty_evidence_text,
            identity_claim_provider=_no_identity_claims,
        )
        kwargs.update(overrides)
        return assemble_scribe_post_gate(**kwargs)

    def test_happy_path_returns_assembly(self):
        out = self._run()
        assert isinstance(out, PostGateAssembly)
        assert F_SCRIBE_UNSOURCED_CLAIM in out.codes_checked
        assert F_SCRIBE_INELIGIBLE_ACTIVITY in out.codes_checked

    def test_unsourced_claim_trips(self):
        def _missing(**kwargs):
            return ("Unsourced claim text",)

        with pytest.raises(ScribeGateFailed) as exc:
            self._run(source_tag_verify=_missing)
        assert exc.value.failure_code == F_SCRIBE_UNSOURCED_CLAIM

    def test_paraphrased_numeric_trips(self):
        # body has a number not in evidence
        sd = _section_draft(body_text="we will hire 7 workers.")

        def _evidence_text(*, envelope):
            return "we will hire 5 workers"

        with pytest.raises(ScribeGateFailed) as exc:
            self._run(drafts=(sd,), evidence_text_provider=_evidence_text)
        assert exc.value.failure_code == F_SCRIBE_PARAPHRASED_NUMERIC
        assert "7" in str(exc.value.evidence["missing_tokens"])

    def test_dialect_drift_trips(self):
        # body uses progressive vocabulary in a conservative-declared draft
        sd = _section_draft(
            body_text="this proposal advances equity for our community.",
            draft_dialect="conservative",
        )
        with pytest.raises(ScribeGateFailed) as exc:
            self._run(drafts=(sd,))
        assert exc.value.failure_code == F_SCRIBE_DIALECT_DRIFT

    def test_dialect_induced_identity_trips(self):
        # soul_fire body uses ancestral knowledge proxy without claim
        sd = _section_draft(
            body_text="we draw on ancestral knowledge to grow.",
            draft_dialect="soul_fire",
        )
        with pytest.raises(ScribeGateFailed) as exc:
            self._run(drafts=(sd,))
        assert exc.value.failure_code == F_SCRIBE_DIALECT_INDUCED_IDENTITY

    def test_section_over_limit_unflagged_trips(self):
        # SectionDraft.__post_init__ refuses to construct an inconsistent
        # over_limit_flag, so we build a CONSISTENT draft (over_limit=True)
        # then mutate the flag to False via object.__setattr__ — exercising
        # the post-gate defense-in-depth walker that catches slip-past.
        limit = SectionLimit(limit_kind="words", limit_value=5)
        body = "we are growing food for our cooperative in rural pennsylvania."
        sd = _section_draft(
            body_text=body,
            over_limit_flag=True,
            rfa_section_limit=limit,
        )
        object.__setattr__(sd, "over_limit_flag", False)
        with pytest.raises(ScribeGateFailed) as exc:
            self._run(drafts=(sd,))
        assert exc.value.failure_code == F_SCRIBE_SECTION_OVER_LIMIT_UNFLAGGED

    def test_budget_section_missing_marker_trips(self):
        sd = _section_draft(
            section_name="Budget Narrative",
            body_text="our budget covers labor and materials.",
        )
        with pytest.raises(ScribeGateFailed) as exc:
            self._run(drafts=(sd,))
        assert exc.value.failure_code == F_SCRIBE_OVERLOOKED_EXPENSE_UNRESOLVED

    def test_budget_section_with_marker_passes(self):
        sd = _section_draft(
            section_name="Budget Narrative",
            body_text=(
                "our budget covers labor and materials. "
                "[OVERLOOKED-EXPENSES-RESOLVED]"
            ),
        )
        out = self._run(drafts=(sd,))
        assert isinstance(out, PostGateAssembly)

    def test_ineligible_activity_trips(self):
        # An EligibleActivityMatch with matched_rfa_activity=None must carry
        # scope_check_flag=True. We bypass the constructor invariant via
        # object.__setattr__ to exercise the walker (it exists as a defense
        # in depth check).
        bad_match = EligibleActivityMatch(
            activity_phrase="mining bitcoin",
            matched_rfa_activity=None,
            scope_check_flag=True,
        )
        # mutate frozen field to simulate slip-past
        object.__setattr__(bad_match, "scope_check_flag", False)
        sd = _section_draft(eligible_activity_map=(bad_match,))
        with pytest.raises(ScribeGateFailed) as exc:
            self._run(drafts=(sd,))
        assert exc.value.failure_code == F_SCRIBE_INELIGIBLE_ACTIVITY

    def test_admin_risk_unflagged_term_trips(self):
        sd = _section_draft(
            body_text="our diversity initiative drives growth.",
            section_name="Project Narrative",
        )
        with pytest.raises(ScribeGateFailed) as exc:
            self._run(drafts=(sd,))
        assert exc.value.failure_code == "F-SCRIBE-ADMIN-RISK-UNFLAGGED"

    def test_admin_risk_unflagged_silenced_when_flag_declared(self):
        sd = _section_draft(
            body_text="our diversity initiative drives growth.",
            section_name="Project Narrative",
        )
        flag = AdminRiskFlag(
            term="diversity",
            severity="medium",
            proposed_substitution="inclusion",
            applicant_approved=False,
        )
        out = self._run(drafts=(sd,), admin_risk_flags=(flag,))
        assert isinstance(out, PostGateAssembly)

    def test_admin_risk_high_unapproved_trips(self):
        register = AdminRiskRegister(
            version="2.2",
            entries=(
                AdminRiskEntry(
                    term="environmental justice",
                    severity="high",
                    progressive_register="OK",
                    suggested_substitutions=("ecological stewardship",),
                    context="",
                    variants=(),
                ),
            ),
            snapshot_sha3_512="b" * 128,
            snapshot_age_hours=0.5,
        )
        sd = _section_draft(
            body_text="environmental justice frames our work.",
            section_name="Project Narrative",
            draft_dialect="progressive",  # term lives in progressive vocab
        )
        flag = AdminRiskFlag(
            term="environmental justice",
            severity="high",
            proposed_substitution="ecological stewardship",
            applicant_approved=False,
        )
        env = _make_envelope(funder_dialect="progressive")
        with pytest.raises(ScribeGateFailed) as exc:
            self._run(
                envelope=env,
                drafts=(sd,),
                admin_risk_flags=(flag,),
                admin_risk_register=register,
            )
        assert exc.value.failure_code == "F-SCRIBE-ADMIN-RISK-HIGH-UNAPPROVED"


# ---------------------------------------------------------------------------
# Conversation anchor parsing
# ---------------------------------------------------------------------------


class TestConversationAnchor:

    def _run(self, env, **overrides):
        kwargs = dict(
            envelope=env,
            section_drafts=(_section_draft(),),
            admin_risk_flags=(),
            admin_risk_register=_make_register(),
            source_tag_verify=_no_unsourced,
            conversation_anchor_verify=_no_anchor_mismatch,
            evidence_text_provider=_empty_evidence_text,
            identity_claim_provider=_no_identity_claims,
        )
        kwargs.update(overrides)
        return assemble_scribe_post_gate(**kwargs)

    def test_no_anchor_passes(self):
        out = self._run(_make_envelope(conversation_log_anchor=None))
        assert isinstance(out, PostGateAssembly)

    def test_malformed_anchor_shape_trips(self):
        env = _make_envelope(conversation_log_anchor="bogus-string")
        with pytest.raises(ScribeGateFailed) as exc:
            self._run(env)
        assert exc.value.failure_code == F_SCRIBE_CONVERSATION_ANCHOR_INVALID

    def test_anchor_run_id_mismatch_trips(self):
        env = _make_envelope(
            run_id="run-A",
            conversation_log_anchor="USER_DATA:run-B:1:" + "a" * 32,
        )
        with pytest.raises(ScribeGateFailed) as exc:
            self._run(env)
        assert exc.value.failure_code == F_SCRIBE_CONVERSATION_ANCHOR_INVALID
        assert exc.value.trigger == "envelope_anchor_run_id_mismatch"

    def test_anchor_turn_ordinal_not_int_trips(self):
        env = _make_envelope(
            run_id="run-A",
            conversation_log_anchor="USER_DATA:run-A:notint:" + "a" * 32,
        )
        with pytest.raises(ScribeGateFailed) as exc:
            self._run(env)
        assert exc.value.failure_code == F_SCRIBE_CONVERSATION_ANCHOR_INVALID

    def test_anchor_hash_verification_callback_trips(self):
        env = _make_envelope(
            run_id="run-A",
            conversation_log_anchor="USER_DATA:run-A:1:" + "a" * 32,
        )

        def _mismatch(*, anchor, run_id):
            return True

        with pytest.raises(ScribeGateFailed) as exc:
            self._run(env, conversation_anchor_verify=_mismatch)
        assert exc.value.failure_code == F_SCRIBE_CONVERSATION_ANCHOR_INVALID
        assert exc.value.trigger == "conversation_anchor_hash_mismatch"
