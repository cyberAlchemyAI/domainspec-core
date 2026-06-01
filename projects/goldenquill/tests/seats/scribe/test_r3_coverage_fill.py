"""R3 targeted coverage-fill tests for the defensive paths in seat.py,
logician_wiring.py, and admin_risk_adapter.py.

These exercise raise-paths that the happy-path tests do not hit — primarily
constructor-bypass routes (object.__setattr__), clock-failure fallbacks,
and result-emission error paths.
"""
from __future__ import annotations

import io
import json
from datetime import datetime, timezone
from typing import Any, Mapping

import pytest

from pipeline.seats.scribe.admin_risk_adapter import (
    AdminRiskEntry,
    AdminRiskRegister,
    AdminRiskRegisterMalformed,
    parse_admin_risk_register,
    load_admin_risk_register,
    scan_draft_for_admin_risk,
)
from pipeline.seats.scribe.logician_wiring import (
    PostGateAssembly,
    PreGateAssembly,
    assemble_scribe_post_gate,
    assemble_scribe_pre_gate,
)
from pipeline.seats.scribe.provider_anthropic import AnthropicResponse
from pipeline.seats.scribe.seat import (
    EXIT_INTERNAL_ERROR,
    F_SCRIBE_CONVERSATION_ANCHOR_INVALID,
    F_SCRIBE_DIALECT_UNCLASSIFIED,
    ScribeEnvelope,
    ScribeEnvelopeMalformed,
    ScribeGateFailed,
    ScribeResult,
    decode_envelope,
    run_seat,
)
from pipeline.seats.scribe.section_draft import (
    AdminRiskFlag,
    ClaimEvidence,
    ConversationAnchor,
    EligibleActivityMatch,
    SectionDraft,
    SectionLimit,
)


_HASH128 = "a" * 128
_NOW = datetime(2026, 4, 22, 12, 0, tzinfo=timezone.utc)


def _envelope_dict(**overrides: Any) -> dict[str, Any]:
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
        "compiled_prompt_shell_sha3_512": _HASH128,
        "compiled_prompt": "Draft.",
        "project_context": {"applicant_name": "FIT Farms"},
        "envelope_emitted_at_utc": "2026-04-22T12:00:00+00:00",
    }
    base.update(overrides)
    return base


def _make_envelope(**overrides: Any) -> ScribeEnvelope:
    return decode_envelope(raw_bytes=json.dumps(_envelope_dict(**overrides)).encode("utf-8"))


def _make_register() -> AdminRiskRegister:
    return AdminRiskRegister(
        version="2.2",
        entries=(
            AdminRiskEntry(
                term="x",
                severity="low",
                progressive_register="OK",
                suggested_substitutions=(),
                context="",
                variants=(),
            ),
        ),
        snapshot_sha3_512="b" * 128,
        snapshot_age_hours=0.0,
    )


def _section_draft(**overrides: Any) -> SectionDraft:
    body = overrides.pop("body_text", "regenerative cooperative")
    base = dict(
        section_name="Project Narrative",
        section_order=1,
        body_text=body,
        word_count=len(body.split()),
        character_count=len(body),
        over_limit_flag=False,
        rfa_section_limit=None,
        draft_dialect="conservative",
        drafted_at_utc=_NOW,
        claim_evidence_map=(),
        eligible_activity_map=(),
        admin_risk_flags=(),
        scope_check_comments=(),
    )
    base.update(overrides)
    return SectionDraft(**base)


# ---------------------------------------------------------------------------
# Decoder edge paths
# ---------------------------------------------------------------------------


def test_envelope_emitted_at_utc_must_be_string():
    d = _envelope_dict(envelope_emitted_at_utc=12345)
    with pytest.raises(ScribeEnvelopeMalformed) as exc:
        decode_envelope(raw_bytes=json.dumps(d).encode("utf-8"))
    assert "ISO-8601 string" in str(exc.value)


def test_envelope_emitted_at_utc_must_be_iso8601():
    d = _envelope_dict(envelope_emitted_at_utc="not-an-iso-string")
    with pytest.raises(ScribeEnvelopeMalformed) as exc:
        decode_envelope(raw_bytes=json.dumps(d).encode("utf-8"))
    assert "not ISO-8601" in str(exc.value)


def test_project_context_must_be_mapping():
    d = _envelope_dict(project_context=["array-not-mapping"])
    with pytest.raises(ScribeEnvelopeMalformed) as exc:
        decode_envelope(raw_bytes=json.dumps(d).encode("utf-8"))
    assert "project_context must be mapping" in str(exc.value)


# ---------------------------------------------------------------------------
# ScribeEnvelope.__post_init__ defensive path (constructor-bypass)
# ---------------------------------------------------------------------------


def test_envelope_post_init_rejects_blank_run_id_via_direct_construction():
    with pytest.raises(ScribeEnvelopeMalformed):
        ScribeEnvelope(
            envelope_version="scribe-envelope.v1",
            run_id="   ",  # blank-after-strip
            org_slug="o",
            iteration_number=0,
            section_name="s",
            section_order=1,
            funder_dialect="conservative",
            operator_override_dialect=None,
            program_code="VAPG",
            admin_risk_register_snapshot_path="/p",
            admin_risk_snapshot_age_hours=0.0,
            conversation_log_anchor=None,
            compiled_prompt_shell_sha3_512=_HASH128,
            compiled_prompt="x",
            project_context={},
            envelope_emitted_at_utc=_NOW,
        )


def test_envelope_post_init_rejects_blank_org_slug():
    with pytest.raises(ScribeEnvelopeMalformed):
        ScribeEnvelope(
            envelope_version="scribe-envelope.v1",
            run_id="r",
            org_slug="   ",
            iteration_number=0,
            section_name="s",
            section_order=1,
            funder_dialect="conservative",
            operator_override_dialect=None,
            program_code="VAPG",
            admin_risk_register_snapshot_path="/p",
            admin_risk_snapshot_age_hours=0.0,
            conversation_log_anchor=None,
            compiled_prompt_shell_sha3_512=_HASH128,
            compiled_prompt="x",
            project_context={},
            envelope_emitted_at_utc=_NOW,
        )


def test_envelope_post_init_rejects_blank_section_name():
    with pytest.raises(ScribeEnvelopeMalformed):
        ScribeEnvelope(
            envelope_version="scribe-envelope.v1",
            run_id="r",
            org_slug="o",
            iteration_number=0,
            section_name="   ",
            section_order=1,
            funder_dialect="conservative",
            operator_override_dialect=None,
            program_code="VAPG",
            admin_risk_register_snapshot_path="/p",
            admin_risk_snapshot_age_hours=0.0,
            conversation_log_anchor=None,
            compiled_prompt_shell_sha3_512=_HASH128,
            compiled_prompt="x",
            project_context={},
            envelope_emitted_at_utc=_NOW,
        )


# ---------------------------------------------------------------------------
# ScribeResult.__post_init__ defensive paths
# ---------------------------------------------------------------------------


def test_scribe_result_rejects_negative_iteration():
    with pytest.raises(ValueError):
        ScribeResult(
            result_version="scribe-result.v1",
            run_id="r",
            org_slug="o",
            iteration_number=-1,
            section_drafts=(_section_draft(),),
            compiled_prompt_shell_sha3_512=_HASH128,
            provider_landed_family="anthropic",
            provider_landed_model_id="claude",
            admin_risk_flags=(),
            seat_emitted_at_utc=_NOW,
        )


def test_scribe_result_rejects_empty_family():
    with pytest.raises(ValueError):
        ScribeResult(
            result_version="scribe-result.v1",
            run_id="r",
            org_slug="o",
            iteration_number=0,
            section_drafts=(_section_draft(),),
            compiled_prompt_shell_sha3_512=_HASH128,
            provider_landed_family="",
            provider_landed_model_id="claude",
            admin_risk_flags=(),
            seat_emitted_at_utc=_NOW,
        )


def test_scribe_result_rejects_empty_model_id():
    with pytest.raises(ValueError):
        ScribeResult(
            result_version="scribe-result.v1",
            run_id="r",
            org_slug="o",
            iteration_number=0,
            section_drafts=(_section_draft(),),
            compiled_prompt_shell_sha3_512=_HASH128,
            provider_landed_family="anthropic",
            provider_landed_model_id="",
            admin_risk_flags=(),
            seat_emitted_at_utc=_NOW,
        )


def test_scribe_result_rejects_naive_seat_emitted():
    with pytest.raises(ValueError):
        ScribeResult(
            result_version="scribe-result.v1",
            run_id="r",
            org_slug="o",
            iteration_number=0,
            section_drafts=(_section_draft(),),
            compiled_prompt_shell_sha3_512=_HASH128,
            provider_landed_family="anthropic",
            provider_landed_model_id="claude",
            admin_risk_flags=(),
            seat_emitted_at_utc=datetime(2026, 1, 1),
        )


def test_scribe_result_rejects_short_shell_hash():
    with pytest.raises(ValueError):
        ScribeResult(
            result_version="scribe-result.v1",
            run_id="r",
            org_slug="o",
            iteration_number=0,
            section_drafts=(_section_draft(),),
            compiled_prompt_shell_sha3_512="short",
            provider_landed_family="anthropic",
            provider_landed_model_id="claude",
            admin_risk_flags=(),
            seat_emitted_at_utc=_NOW,
        )


# ---------------------------------------------------------------------------
# run_seat — clock-failure fallback in stderr emitter (line 499-500)
# ---------------------------------------------------------------------------


def test_run_seat_recovers_when_clock_raises_during_stderr_emit():
    stdin = io.BytesIO(b"")  # → envelope_malformed → emits stderr
    stdout = io.BytesIO()
    stderr = io.BytesIO()

    def _broken_clock():
        raise RuntimeError("clock unavailable")

    rc = run_seat(
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        clock=_broken_clock,
        anthropic_call=lambda **_: None,
        response_parse=lambda **_: ((), ()),
        pre_gate=lambda **_: None,
        post_gate=lambda **_: None,
        admin_risk_fetch=lambda **_: _make_register(),
        anthropic_binding=object(),
    )
    assert rc == 2  # EXIT_GATE_FAIL
    line = json.loads(stderr.getvalue().decode("utf-8"))
    # The fallback ISO is real wall-clock — so it's a non-empty string ending
    # with a UTC offset.
    assert "T" in line["emitted_at_utc"]
    assert line["emitted_at_utc"].endswith("+00:00")


# ---------------------------------------------------------------------------
# run_seat — result-emission failure path (lines 690-693)
# ---------------------------------------------------------------------------


def test_run_seat_returns_exit_1_when_stdout_write_raises():
    class _RaisingStdout:
        def write(self, data):
            raise OSError("disk full")

    stdin = io.BytesIO(json.dumps(_envelope_dict()).encode("utf-8"))
    stdout = _RaisingStdout()
    stderr = io.BytesIO()

    def _clock():
        return _NOW

    rc = run_seat(
        stdin=stdin,
        stdout=stdout,  # type: ignore[arg-type]
        stderr=stderr,
        clock=_clock,
        anthropic_call=lambda **_: AnthropicResponse(
            text_body="x",
            landed_model_id="claude",
            response_sha3_512="c" * 128,
            prompt_token_estimate=64,
            raw_response_canonical_json_bytes=b"{}",
        ),
        response_parse=lambda **_: ((_section_draft(),), ()),
        pre_gate=lambda **_: None,
        post_gate=lambda **_: None,
        admin_risk_fetch=lambda **_: _make_register(),
        anthropic_binding=object(),
    )
    assert rc == EXIT_INTERNAL_ERROR
    assert b"result emission failed" in stderr.getvalue()


# ---------------------------------------------------------------------------
# logician_wiring — defensive funder_dialect-not-in-set path (line 327)
# ---------------------------------------------------------------------------


def test_pre_gate_dialect_unclassified_via_setattr_bypass():
    # Construct a valid envelope, then mutate funder_dialect via
    # object.__setattr__ to slip a value past construction.
    env = _make_envelope()
    object.__setattr__(env, "funder_dialect", "anarchist")
    with pytest.raises(ScribeGateFailed) as exc:
        assemble_scribe_pre_gate(
            envelope=env,
            admin_risk_register=_make_register(),
            cedar_cross_org_check=lambda **_: (),
            kgie_status_getter=lambda **_: "pass",
            rfa_drift_check=lambda **_: False,
            template_drift_check=lambda **_: False,
        )
    assert exc.value.failure_code == F_SCRIBE_DIALECT_UNCLASSIFIED


# ---------------------------------------------------------------------------
# logician_wiring — limit_kind == "characters" branch (412-413)
# ---------------------------------------------------------------------------


def test_post_gate_over_limit_for_characters_kind():
    limit = SectionLimit(limit_kind="characters", limit_value=10)
    body = "this body has more than ten characters."
    sd = _section_draft(
        body_text=body,
        over_limit_flag=True,  # consistent with body > limit
        rfa_section_limit=limit,
    )
    object.__setattr__(sd, "over_limit_flag", False)  # bypass to fire walker

    out_or_exc = pytest.raises(ScribeGateFailed)
    with out_or_exc as exc:
        assemble_scribe_post_gate(
            envelope=_make_envelope(),
            section_drafts=(sd,),
            admin_risk_flags=(),
            admin_risk_register=_make_register(),
            source_tag_verify=lambda **_: (),
            conversation_anchor_verify=lambda **_: False,
            evidence_text_provider=lambda **_: "",
            identity_claim_provider=lambda **_: (),
        )
    assert exc.value.failure_code == "F-SCRIBE-SECTION-OVER-LIMIT-UNFLAGGED"


def test_post_gate_pages_limit_treated_as_authoritative():
    # pages limit_kind: walker falls through ("True" passthrough); over_limit
    # flag is taken as authoritative — no trip even if counts don't match.
    limit = SectionLimit(limit_kind="pages", limit_value=2)
    body = "two pages of content."
    sd = _section_draft(
        body_text=body,
        over_limit_flag=False,
        rfa_section_limit=limit,
    )
    out = assemble_scribe_post_gate(
        envelope=_make_envelope(),
        section_drafts=(sd,),
        admin_risk_flags=(),
        admin_risk_register=_make_register(),
        source_tag_verify=lambda **_: (),
        conversation_anchor_verify=lambda **_: False,
        evidence_text_provider=lambda **_: "",
        identity_claim_provider=lambda **_: (),
    )
    assert isinstance(out, PostGateAssembly)


# ---------------------------------------------------------------------------
# logician_wiring — _check_anchor_pointers (USER_DATA evidence variants)
# ---------------------------------------------------------------------------


def test_post_gate_user_data_evidence_no_anchor_trips():
    ev = ClaimEvidence(
        claim_text="something",
        evidence_kind="USER_DATA",
        source_pointer="USER_DATA:run-A:1:" + "a" * 32,
    )
    sd = _section_draft(claim_evidence_map=(ev,))
    env = _make_envelope(conversation_log_anchor=None)
    with pytest.raises(ScribeGateFailed) as exc:
        assemble_scribe_post_gate(
            envelope=env,
            section_drafts=(sd,),
            admin_risk_flags=(),
            admin_risk_register=_make_register(),
            source_tag_verify=lambda **_: (),
            conversation_anchor_verify=lambda **_: False,
            evidence_text_provider=lambda **_: "",
            identity_claim_provider=lambda **_: (),
        )
    assert exc.value.failure_code == F_SCRIBE_CONVERSATION_ANCHOR_INVALID


def test_post_gate_user_data_evidence_pointer_mismatch_trips():
    ev = ClaimEvidence(
        claim_text="something",
        evidence_kind="USER_DATA",
        source_pointer="USER_DATA:run-A:99:" + "z" * 32,  # wrong turn + prefix
    )
    sd = _section_draft(claim_evidence_map=(ev,))
    env = _make_envelope(
        run_id="run-A",
        conversation_log_anchor="USER_DATA:run-A:1:" + "a" * 32,
    )
    with pytest.raises(ScribeGateFailed) as exc:
        assemble_scribe_post_gate(
            envelope=env,
            section_drafts=(sd,),
            admin_risk_flags=(),
            admin_risk_register=_make_register(),
            source_tag_verify=lambda **_: (),
            conversation_anchor_verify=lambda **_: False,
            evidence_text_provider=lambda **_: "",
            identity_claim_provider=lambda **_: (),
        )
    assert exc.value.failure_code == F_SCRIBE_CONVERSATION_ANCHOR_INVALID


def test_post_gate_non_user_data_evidence_kind_skipped():
    # RFA / PROJECT_CONTEXT pointers don't go through the anchor walker.
    ev = ClaimEvidence(
        claim_text="cited fact",
        evidence_kind="RFA",
        source_pointer="rfa.md#L42",
    )
    sd = _section_draft(claim_evidence_map=(ev,))
    env = _make_envelope()
    out = assemble_scribe_post_gate(
        envelope=env,
        section_drafts=(sd,),
        admin_risk_flags=(),
        admin_risk_register=_make_register(),
        source_tag_verify=lambda **_: (),
        conversation_anchor_verify=lambda **_: False,
        evidence_text_provider=lambda **_: "",
        identity_claim_provider=lambda **_: (),
    )
    assert isinstance(out, PostGateAssembly)


# ---------------------------------------------------------------------------
# logician_wiring — admin-risk RuntimeError without F-code passthrough (671)
# ---------------------------------------------------------------------------


def test_post_gate_admin_risk_unrelated_runtime_error_re_raises():
    """An unrelated RuntimeError from verify_draft_flags_or_raise must
    re-raise rather than being routed to F-SCRIBE-ADMIN-RISK-UNFLAGGED."""

    class _BadRegister:
        # Subclass that raises RuntimeError on .entries access.
        @property
        def entries(self):
            raise RuntimeError("disk failure unrelated to flagging")

        @property
        def version(self):
            return "2.2"

        @property
        def snapshot_sha3_512(self):
            return "b" * 128

        @property
        def snapshot_age_hours(self):
            return 0.0

    sd = _section_draft()
    env = _make_envelope()
    with pytest.raises(RuntimeError, match="disk failure"):
        assemble_scribe_post_gate(
            envelope=env,
            section_drafts=(sd,),
            admin_risk_flags=(),
            admin_risk_register=_BadRegister(),  # type: ignore[arg-type]
            source_tag_verify=lambda **_: (),
            conversation_anchor_verify=lambda **_: False,
            evidence_text_provider=lambda **_: "",
            identity_claim_provider=lambda **_: (),
        )


# ---------------------------------------------------------------------------
# logician_wiring — anchor-prefix-malformed (lines 742-749)
# ---------------------------------------------------------------------------


def test_post_gate_anchor_prefix_wrong_length_trips():
    # ConversationAnchor requires a 32-hex prefix; a too-short string
    # raises ValueError inside the parser, which we route to F-SCRIBE-
    # CONVERSATION-ANCHOR-INVALID.
    env = _make_envelope(
        run_id="run-A",
        conversation_log_anchor="USER_DATA:run-A:1:tooshort",
    )
    with pytest.raises(ScribeGateFailed) as exc:
        assemble_scribe_post_gate(
            envelope=env,
            section_drafts=(_section_draft(),),
            admin_risk_flags=(),
            admin_risk_register=_make_register(),
            source_tag_verify=lambda **_: (),
            conversation_anchor_verify=lambda **_: False,
            evidence_text_provider=lambda **_: "",
            identity_claim_provider=lambda **_: (),
        )
    assert exc.value.failure_code == F_SCRIBE_CONVERSATION_ANCHOR_INVALID
    assert exc.value.trigger == "envelope_anchor_prefix_malformed"


# ---------------------------------------------------------------------------
# admin_risk_adapter — load malformed (240-241), variants list (190),
# scan dedup-on-non-flag (369), AdminRiskRegister __post_init__ (127-131)
# ---------------------------------------------------------------------------


def test_admin_risk_register_rejects_blank_version():
    with pytest.raises(ValueError):
        AdminRiskRegister(
            version="",
            entries=(
                AdminRiskEntry(
                    term="x",
                    severity="low",
                    progressive_register="OK",
                    suggested_substitutions=(),
                    context="",
                    variants=(),
                ),
            ),
            snapshot_sha3_512="a" * 128,
            snapshot_age_hours=0.0,
        )


def test_admin_risk_register_rejects_negative_age():
    with pytest.raises(ValueError):
        AdminRiskRegister(
            version="2.2",
            entries=(
                AdminRiskEntry(
                    term="x",
                    severity="low",
                    progressive_register="OK",
                    suggested_substitutions=(),
                    context="",
                    variants=(),
                ),
            ),
            snapshot_sha3_512="a" * 128,
            snapshot_age_hours=-0.1,
        )


def test_parse_register_rejects_variants_not_list():
    with pytest.raises(AdminRiskRegisterMalformed) as exc:
        parse_admin_risk_register(
            raw_mapping={
                "version": "2.2",
                "entries": [
                    {
                        "term": "x",
                        "severity": "RED",
                        "variants": "not-a-list",
                    }
                ],
            },
            snapshot_sha3_512="a" * 128,
            snapshot_age_hours=0.0,
        )
    assert "'variants' must be list" in str(exc.value)


def test_load_admin_risk_register_rejects_unserializable_payload():
    # `bytes` are not JSON-serializable; the canonicalizer trips.
    def _loader(*, register_path):
        return {"version": "2.2", "entries": [], "extra": object()}

    with pytest.raises(AdminRiskRegisterMalformed) as exc:
        load_admin_risk_register(
            register_loader=_loader,
            register_path="/v/r.yaml",
            snapshot_age_hours=0.0,
        )
    # Either canonicalization-failure OR empty-entries — both are valid
    # mid-load failures wrapped in AdminRiskRegisterMalformed.
    assert "ADMIN-RISK-REGISTER-MALFORMED" in str(exc.value)


def test_scan_dedup_skips_already_seen_term_when_match_returns_none():
    # With auto_substitute_low_enabled, a LOW-severity match produces no
    # flag — but the entry's term is then NOT added to seen_terms; this
    # means a later same-term entry could re-attempt to flag. Verify the
    # scanner is well-behaved with multiple LOW matches.
    register = AdminRiskRegister(
        version="2.2",
        entries=(
            AdminRiskEntry(
                term="rural",
                severity="low",
                progressive_register="OK",
                suggested_substitutions=("country",),
                context="",
                variants=(),
            ),
        ),
        snapshot_sha3_512="a" * 128,
        snapshot_age_hours=0.0,
    )
    # auto_substitute drops flag → seen_terms remains empty; no error
    flags = scan_draft_for_admin_risk(
        draft_body="rural development is rural rural rural.",
        register=register,
        funder_dialect="conservative",
        auto_substitute_low_enabled=True,
    )
    assert flags == ()
