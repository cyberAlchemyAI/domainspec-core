"""§7 Scribe — whole-section capstone integration tests.

Per handoff `pipeline/handoffs/section_7_scribe_whole_section_capstone_2026-04-29.md`.

Promotes §7 from per-round LOCKs (R1 + R2 + R2.5 + R3) to LOCKED-as-a-whole-section.
Test-only round; ZERO new §7 production code.

Three test surfaces from the handoff:

- W.1 Full Scribe invocation lifecycle — seat.py subprocess entry calling
  PRE-gate → KGIE preflight → compose → Anthropic → POST-gate → output via
  the real ``assemble_scribe_pre_gate`` / ``assemble_scribe_post_gate``
  assemblers (only collaborators outside the assemblers — Anthropic +
  vault-fetch — are stubbed via the existing R3 E-017 seams).
- W.2 F-SCRIBE-* failure-code matrix — every declared F-SCRIBE-* failure code
  triggers via the canonical path and propagates through ``run_seat`` exit-code
  routing. Codes that are R3-out-of-scope by design (declared as constants for
  §5 R5+ revision-loop binding) get a presence test instead of a trip test.
- W.3 Cross-round composition gaps — R1 types feed R2 shapers feed R3 seat
  surface without import-time failures; BLUEPRINT_DEPS hash pins consistent
  across rounds; R2.5 SectionDraft consumed by R3 result emission.

All collaborators are injected via the existing E-017 Protocol seams. No
network, no subprocess, no clock dependency.
"""
from __future__ import annotations

import io
import json
from datetime import datetime, timezone
from typing import Any, Mapping

import pytest

from pipeline.seats import scribe as scribe_pkg
from pipeline.seats.scribe import (
    BLUEPRINT_DEPS,
    DIALECT_VOCABULARY,
    KNOWN_PROGRAMS,
    SNAPSHOT_AGE_HOURS_CEILING,
)
from pipeline.seats.scribe.admin_risk_adapter import (
    AdminRiskEntry,
    AdminRiskRegister,
    AdminRiskRegisterMalformed,
    F_SCRIBE_ADMIN_RISK_HIGH_UNAPPROVED,
    F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED,
    F_SCRIBE_ADMIN_RISK_REGISTER_STALE,
    F_SCRIBE_ADMIN_RISK_UNFLAGGED,
    parse_admin_risk_register,
    scan_draft_for_admin_risk,
)
from pipeline.seats.scribe.logician_wiring import (
    PostGateAssembly,
    PreGateAssembly,
    assemble_scribe_post_gate,
    assemble_scribe_pre_gate,
)
from pipeline.seats.scribe.provider_anthropic import (
    AnthropicBYOKMissing,
    AnthropicPayloadCeiling,
    AnthropicProviderMalformed,
    AnthropicResponse,
    AnthropicSemanticFailure,
    AnthropicTransportFailure,
    F_SCRIBE_BYOK_MISSING,
    F_SCRIBE_PAYLOAD_CEILING,
    F_SCRIBE_PROVIDER_MALFORMED,
    F_SCRIBE_SEMANTIC_FAILURE,
    F_SCRIBE_TRANSPORT_FAILURE,
)
from pipeline.seats.scribe.seat import (
    ENVELOPE_VERSION_V1,
    EXIT_GATE_FAIL,
    EXIT_INTERNAL_ERROR,
    EXIT_OK,
    F_SCRIBE_CONVERSATION_ANCHOR_INVALID,
    F_SCRIBE_DIALECT_DRIFT,
    F_SCRIBE_DIALECT_INDUCED_IDENTITY,
    F_SCRIBE_DIALECT_UNCLASSIFIED,
    F_SCRIBE_ENVELOPE_MALFORMED,
    F_SCRIBE_EVALUATION_CRITERION_MISSING,
    F_SCRIBE_INELIGIBLE_ACTIVITY,
    F_SCRIBE_ORG_CROSS_REF,
    F_SCRIBE_OVERLOOKED_EXPENSE_UNRESOLVED,
    F_SCRIBE_PARAPHRASED_NUMERIC,
    F_SCRIBE_SCOPE_MISSING,
    F_SCRIBE_SECTION_OVER_LIMIT_UNFLAGGED,
    F_SCRIBE_SMART_INVENTED_METRIC,
    F_SCRIBE_TEMPLATE_DRIFT,
    F_SCRIBE_TEMPLATE_UNKNOWN,
    F_SCRIBE_UNSOURCED_CLAIM,
    RESULT_VERSION_V1,
    ScribeEnvelope,
    ScribeGateFailed,
    decode_envelope,
    run_seat,
)
from pipeline.seats.scribe.section_draft import (
    AdminRiskFlag,
    ClaimEvidence,
    EligibleActivityMatch,
    SectionDraft,
    SectionLimit,
)
from pipeline.seats.scribe.types import (
    F_SCRIBE_KGIE_FAIL,
    F_SCRIBE_PHASE_0_MISSING,
    F_SCRIBE_RFA_DRIFT,
    F_SCRIBE_RFA_MISSING,
    IdentityClaim,
)


# ---------------------------------------------------------------------------
# Shared fixtures — full lifecycle through real PRE/POST-gate assemblers.
# ---------------------------------------------------------------------------

_SHELL_HASH_128 = "f" * 128
_RESPONSE_HASH_128 = "c" * 128
_FIXED_NOW = datetime(2026, 4, 29, 12, 0, tzinfo=timezone.utc)
_DEFAULT_BODY = "FIT Farms operates a regenerative cooperative."


def _make_envelope_dict(**overrides: Any) -> dict[str, Any]:
    base = {
        "envelope_version": "scribe-envelope.v1",
        "run_id": "run-2026-04-29-capstone",
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
        "compiled_prompt": "Draft the Project Narrative.",
        "project_context": {"applicant_name": "FIT Farms"},
        "envelope_emitted_at_utc": "2026-04-29T12:00:00+00:00",
    }
    base.update(overrides)
    return base


def _make_envelope(**overrides: Any) -> ScribeEnvelope:
    raw = json.dumps(_make_envelope_dict(**overrides)).encode("utf-8")
    return decode_envelope(raw_bytes=raw)


def _make_section_draft(
    *,
    body_text: str = _DEFAULT_BODY,
    section_name: str = "Project Narrative",
    draft_dialect: str = "conservative",
    over_limit_flag: bool = False,
    rfa_section_limit: SectionLimit | None = None,
    eligible_activity_map: tuple[EligibleActivityMatch, ...] = (),
    claim_evidence_map: tuple[ClaimEvidence, ...] = (),
    admin_risk_flags: tuple[AdminRiskFlag, ...] = (),
    word_count: int | None = None,
    character_count: int | None = None,
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
        admin_risk_flags=admin_risk_flags,
        scope_check_comments=(),
    )


def _make_register(*, age: float = 0.5, severity: str = "medium") -> AdminRiskRegister:
    return AdminRiskRegister(
        version="2.2",
        entries=(
            AdminRiskEntry(
                term="diversity",
                severity=severity,  # type: ignore[arg-type]
                progressive_register="OK",
                suggested_substitutions=("inclusion",),
                context="federal admin-risk",
                variants=(),
            ),
        ),
        snapshot_sha3_512="b" * 128,
        snapshot_age_hours=age,
    )


def _ok_response() -> AnthropicResponse:
    return AnthropicResponse(
        text_body="parsed-body",
        landed_model_id="claude-sonnet-4-5-20250929",
        response_sha3_512=_RESPONSE_HASH_128,
        prompt_token_estimate=128,
        raw_response_canonical_json_bytes=b'{"k":"v"}',
    )


def _clock() -> datetime:
    return _FIXED_NOW


# ---------------------------------------------------------------------------
# Wired collaborators that route every PRE/POST check through the REAL
# assemblers. Stubs are limited to vault-fetch + Anthropic + the eight
# Logician seams that span outside §7 (Cedar / KGIE / RFA-drift / template-
# drift / source-tag-verify / conversation-anchor-verify / evidence-text /
# identity-claim).
# ---------------------------------------------------------------------------


def _no_foreign_orgs(**_: Any) -> tuple[str, ...]:
    return ()


def _kgie_pass(*, envelope: ScribeEnvelope) -> str:  # noqa: ARG001
    return "pass"


def _no_rfa_drift(*, envelope: ScribeEnvelope) -> bool:  # noqa: ARG001
    return False


def _no_template_drift(*, envelope: ScribeEnvelope) -> bool:  # noqa: ARG001
    return False


def _no_unsourced(**_: Any) -> tuple[str, ...]:
    return ()


def _anchor_match(*, anchor: Any, run_id: str) -> bool:  # noqa: ARG001
    return False


def _empty_evidence(*, envelope: ScribeEnvelope) -> str:  # noqa: ARG001
    return ""


def _no_identity(*, envelope: ScribeEnvelope) -> tuple[Any, ...]:  # noqa: ARG001
    return ()


def _make_pre_gate(
    *,
    cedar: Any = _no_foreign_orgs,
    kgie: Any = _kgie_pass,
    rfa_drift: Any = _no_rfa_drift,
    template_drift: Any = _no_template_drift,
):
    def _pre(*, envelope, admin_risk_register):
        return assemble_scribe_pre_gate(
            envelope=envelope,
            admin_risk_register=admin_risk_register,
            cedar_cross_org_check=cedar,
            kgie_status_getter=kgie,
            rfa_drift_check=rfa_drift,
            template_drift_check=template_drift,
        )

    return _pre


def _make_post_gate(
    *,
    source_tag: Any = _no_unsourced,
    anchor_verify: Any = _anchor_match,
    evidence_text: Any = _empty_evidence,
    identity: Any = _no_identity,
):
    def _post(*, envelope, section_drafts, admin_risk_flags, admin_risk_register):
        return assemble_scribe_post_gate(
            envelope=envelope,
            section_drafts=section_drafts,
            admin_risk_flags=admin_risk_flags,
            admin_risk_register=admin_risk_register,
            source_tag_verify=source_tag,
            conversation_anchor_verify=anchor_verify,
            evidence_text_provider=evidence_text,
            identity_claim_provider=identity,
        )

    return _post


def _ok_anthropic(**_: Any) -> AnthropicResponse:
    return _ok_response()


def _make_admin_risk_fetch(register: AdminRiskRegister | None = None):
    register_obj = register if register is not None else _make_register()

    def _fetch(*, envelope: ScribeEnvelope) -> AdminRiskRegister:  # noqa: ARG001
        return register_obj

    return _fetch


def _make_response_parse(
    drafts: tuple[SectionDraft, ...] | None = None,
    flags: tuple[AdminRiskFlag, ...] = (),
):
    if drafts is None:
        drafts = (_make_section_draft(),)

    def _parse(
        *, response: AnthropicResponse, envelope: ScribeEnvelope
    ) -> tuple[tuple[SectionDraft, ...], tuple[AdminRiskFlag, ...]]:
        del response, envelope
        return drafts, flags

    return _parse


def _run_seat(
    *,
    envelope_dict: dict[str, Any] | None = None,
    pre_gate: Any = None,
    post_gate: Any = None,
    response_parse: Any = None,
    anthropic_call: Any = _ok_anthropic,
    admin_risk_fetch: Any = None,
    register: AdminRiskRegister | None = None,
) -> tuple[int, bytes, bytes]:
    if envelope_dict is None:
        envelope_dict = _make_envelope_dict()
    if pre_gate is None:
        pre_gate = _make_pre_gate()
    if post_gate is None:
        post_gate = _make_post_gate()
    if response_parse is None:
        response_parse = _make_response_parse()
    if admin_risk_fetch is None:
        admin_risk_fetch = _make_admin_risk_fetch(register)
    stdin = io.BytesIO(json.dumps(envelope_dict).encode("utf-8"))
    stdout = io.BytesIO()
    stderr = io.BytesIO()
    rc = run_seat(
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        clock=_clock,
        anthropic_call=anthropic_call,
        response_parse=response_parse,
        pre_gate=pre_gate,
        post_gate=post_gate,
        admin_risk_fetch=admin_risk_fetch,
        anthropic_binding=object(),
    )
    return rc, stdout.getvalue(), stderr.getvalue()


def _stderr_failure_code(stderr_bytes: bytes) -> str:
    line = json.loads(stderr_bytes.decode("utf-8").strip())
    return line["failure_code"]


# ---------------------------------------------------------------------------
# W.1 Full Scribe invocation lifecycle
# ---------------------------------------------------------------------------


class TestW1FullLifecycle:
    """Real PRE-gate + Anthropic + POST-gate composition, end-to-end."""

    def test_happy_path_exit_zero_emits_canonical_result(self):
        rc, stdout, stderr = _run_seat()
        assert rc == EXIT_OK
        assert stderr == b""
        decoded = json.loads(stdout)
        assert decoded["result_version"] == RESULT_VERSION_V1
        assert decoded["provider_landed_family"] == "anthropic"
        assert decoded["section_drafts_count"] == 1
        assert decoded["admin_risk_flags_count"] == 0
        # Envelope shell hash echoes through to result (§6.11 passthrough).
        assert decoded["compiled_prompt_shell_sha3_512"] == _SHELL_HASH_128

    def test_happy_path_canonical_json_keys_sorted(self):
        rc, stdout, _ = _run_seat()
        assert rc == EXIT_OK
        decoded = json.loads(stdout)
        assert list(decoded.keys()) == sorted(decoded.keys())

    def test_happy_path_result_includes_section_metadata(self):
        rc, stdout, _ = _run_seat()
        assert rc == EXIT_OK
        decoded = json.loads(stdout)
        section = decoded["section_drafts"][0]
        assert section["section_name"] == "Project Narrative"
        assert section["section_order"] == 1
        assert section["draft_dialect"] == "conservative"
        # word_count + character_count round-trip from SectionDraft.
        assert section["word_count"] == len(_DEFAULT_BODY.split())
        assert section["character_count"] == len(_DEFAULT_BODY)

    def test_kgie_needs_operator_input_with_override_passes(self):
        envelope_dict = _make_envelope_dict(operator_override_dialect="conservative")

        def _needs(*, envelope):  # noqa: ARG001
            return "needs_operator_input"

        rc, stdout, stderr = _run_seat(
            envelope_dict=envelope_dict,
            pre_gate=_make_pre_gate(kgie=_needs),
        )
        assert rc == EXIT_OK
        assert stderr == b""
        assert b'"result_version":"scribe-result.v1"' in stdout

    def test_admin_risk_flagged_term_with_declared_flag_passes(self):
        # Body contains "diversity" (medium severity in fixture register);
        # POST-gate requires a declared AdminRiskFlag; once present, PASS.
        sd = _make_section_draft(
            body_text="our diversity initiative drives growth.",
        )
        flag = AdminRiskFlag(
            term="diversity",
            severity="medium",
            proposed_substitution="inclusion",
            applicant_approved=False,
        )
        rc, stdout, stderr = _run_seat(
            response_parse=_make_response_parse(drafts=(sd,), flags=(flag,)),
        )
        assert rc == EXIT_OK
        assert stderr == b""
        decoded = json.loads(stdout)
        assert decoded["admin_risk_flags_count"] == 1
        assert decoded["admin_risk_flags"][0]["term"] == "diversity"
        assert decoded["admin_risk_flags"][0]["severity"] == "medium"

    def test_admin_risk_low_severity_silent_substitution_no_flag(self):
        # LOW severity term + auto_substitute_low_enabled=False (POST-gate
        # default) should still PASS without declared flag because LOW
        # entries are skipped in `verify_draft_flags_or_raise` —
        # `if expected_flag.severity == "low": continue`.
        register = _make_register(severity="low")
        sd = _make_section_draft(
            body_text="our diversity initiative drives growth.",
        )
        rc, stdout, stderr = _run_seat(
            response_parse=_make_response_parse(drafts=(sd,)),
            register=register,
        )
        assert rc == EXIT_OK
        assert stderr == b""
        decoded = json.loads(stdout)
        assert decoded["admin_risk_flags_count"] == 0

    def test_pre_gate_runs_before_anthropic(self):
        # PRE-gate trip → Anthropic must NOT be called.
        anthropic_calls: list[Any] = []

        def _track_anthropic(**kwargs: Any) -> AnthropicResponse:
            anthropic_calls.append(kwargs)
            return _ok_response()

        def _foreign_org(**_: Any) -> tuple[str, ...]:
            return ("competitor_org",)

        rc, stdout, stderr = _run_seat(
            pre_gate=_make_pre_gate(cedar=_foreign_org),
            anthropic_call=_track_anthropic,
        )
        assert rc == EXIT_GATE_FAIL
        assert stdout == b""
        assert anthropic_calls == []
        assert _stderr_failure_code(stderr) == F_SCRIBE_ORG_CROSS_REF

    def test_post_gate_runs_after_anthropic(self):
        # Anthropic returns OK, response_parse returns a draft, POST-gate
        # trips on dialect drift — exit 2 with POST F-code.
        sd = _make_section_draft(
            body_text="this proposal advances equity for our community.",
            draft_dialect="conservative",
        )
        rc, _, stderr = _run_seat(
            response_parse=_make_response_parse(drafts=(sd,)),
        )
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_DIALECT_DRIFT

    def test_admin_risk_fetch_invoked_with_envelope(self):
        captured: list[ScribeEnvelope] = []

        def _capture_fetch(*, envelope: ScribeEnvelope) -> AdminRiskRegister:
            captured.append(envelope)
            return _make_register()

        rc, _, _ = _run_seat(admin_risk_fetch=_capture_fetch)
        assert rc == EXIT_OK
        assert len(captured) == 1
        assert captured[0].org_slug == "fit_farms_llc"
        assert captured[0].run_id == "run-2026-04-29-capstone"

    def test_response_parse_invoked_with_anthropic_response_and_envelope(self):
        captured: dict[str, Any] = {}

        def _capture_parse(
            *, response: AnthropicResponse, envelope: ScribeEnvelope
        ) -> tuple[tuple[SectionDraft, ...], tuple[AdminRiskFlag, ...]]:
            captured["response"] = response
            captured["envelope"] = envelope
            return (_make_section_draft(),), ()

        rc, _, _ = _run_seat(response_parse=_capture_parse)
        assert rc == EXIT_OK
        assert isinstance(captured["response"], AnthropicResponse)
        assert isinstance(captured["envelope"], ScribeEnvelope)
        assert captured["response"].landed_model_id == "claude-sonnet-4-5-20250929"

    def test_progressive_dialect_with_matching_identity_claim_passes(self):
        # progressive funder + soul_fire-tagged body would normally trip
        # F-SCRIBE-DIALECT-INDUCED-IDENTITY when "ancestral knowledge" is
        # present without a claim. Provide the IdentityClaim → POST-gate PASS.
        envelope_dict = _make_envelope_dict(funder_dialect="progressive")
        sd = _make_section_draft(
            body_text="we draw on ancestral knowledge to grow.",
            draft_dialect="soul_fire",
        )

        def _identity(*, envelope):  # noqa: ARG001
            return (
                IdentityClaim(
                    claim="ancestral-knowledge keepers",
                    source_field_in_project_context="applicant.identity_statement",
                    rfa_priority_points=5,
                ),
            )

        rc, stdout, stderr = _run_seat(
            envelope_dict=envelope_dict,
            response_parse=_make_response_parse(drafts=(sd,)),
            post_gate=_make_post_gate(identity=_identity),
        )
        assert rc == EXIT_OK
        assert stderr == b""
        assert b'"section_drafts_count":1' in stdout

    def test_env_envelope_decode_round_trips_project_context(self):
        # Round-trip — the project_context Mapping carried at envelope decode
        # time is read back by the POST-gate path through the
        # source_tag_verify hook.
        captured_context: list[Mapping[str, Any]] = []

        def _capture_unsourced(
            *,
            claim_evidence_map: tuple[ClaimEvidence, ...],
            project_context: Mapping[str, Any],
            rfa_body_text: str,
            conversation_log: Mapping[str, str],
        ) -> tuple[str, ...]:
            del claim_evidence_map, rfa_body_text, conversation_log
            captured_context.append(project_context)
            return ()

        rc, _, _ = _run_seat(
            post_gate=_make_post_gate(source_tag=_capture_unsourced),
        )
        assert rc == EXIT_OK
        assert captured_context[0]["applicant_name"] == "FIT Farms"


# ---------------------------------------------------------------------------
# W.2 F-SCRIBE-* failure-code matrix
# ---------------------------------------------------------------------------


class TestW2FCodeMatrixEnvelopeDecode:
    """F-codes that fire at envelope-decode boundary."""

    def test_envelope_malformed_empty_stdin(self):
        stdin = io.BytesIO(b"")
        stdout = io.BytesIO()
        stderr = io.BytesIO()
        rc = run_seat(
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            clock=_clock,
            anthropic_call=_ok_anthropic,
            response_parse=_make_response_parse(),
            pre_gate=_make_pre_gate(),
            post_gate=_make_post_gate(),
            admin_risk_fetch=_make_admin_risk_fetch(),
            anthropic_binding=object(),
        )
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr.getvalue()) == F_SCRIBE_ENVELOPE_MALFORMED


class TestW2FCodeMatrixPreGate:
    """F-codes raised by ``assemble_scribe_pre_gate``."""

    def test_org_cross_ref(self):
        def _foreign(**_: Any) -> tuple[str, ...]:
            return ("competitor_org",)

        rc, _, stderr = _run_seat(pre_gate=_make_pre_gate(cedar=_foreign))
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_ORG_CROSS_REF

    def test_kgie_fail(self):
        def _kgie_fail(*, envelope):  # noqa: ARG001
            return "fail"

        rc, _, stderr = _run_seat(pre_gate=_make_pre_gate(kgie=_kgie_fail))
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_KGIE_FAIL

    def test_rfa_drift(self):
        def _drift(*, envelope):  # noqa: ARG001
            return True

        rc, _, stderr = _run_seat(pre_gate=_make_pre_gate(rfa_drift=_drift))
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_RFA_DRIFT

    def test_scope_missing(self):
        def _needs(*, envelope):  # noqa: ARG001
            return "needs_operator_input"

        rc, _, stderr = _run_seat(pre_gate=_make_pre_gate(kgie=_needs))
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_SCOPE_MISSING

    def test_dialect_unclassified_defensive(self):
        # Envelope construction enforces the closed set, but assemble_pre_gate
        # carries a defensive recheck for callers who slip an invalid value
        # past via ``object.__setattr__``. Exercise directly through the
        # assembler (the seat-level path is unreachable since decode pins the
        # closed set first).
        env = _make_envelope()
        object.__setattr__(env, "funder_dialect", "anarchist")
        with pytest.raises(ScribeGateFailed) as exc:
            assemble_scribe_pre_gate(
                envelope=env,
                admin_risk_register=_make_register(),
                cedar_cross_org_check=_no_foreign_orgs,
                kgie_status_getter=_kgie_pass,
                rfa_drift_check=_no_rfa_drift,
                template_drift_check=_no_template_drift,
            )
        assert exc.value.failure_code == F_SCRIBE_DIALECT_UNCLASSIFIED

    def test_template_unknown(self):
        env_dict = _make_envelope_dict(program_code="UNREGISTERED-PROGRAM")
        rc, _, stderr = _run_seat(envelope_dict=env_dict)
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_TEMPLATE_UNKNOWN

    def test_template_drift(self):
        def _drift(*, envelope):  # noqa: ARG001
            return True

        rc, _, stderr = _run_seat(pre_gate=_make_pre_gate(template_drift=_drift))
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_TEMPLATE_DRIFT

    def test_admin_risk_register_stale_envelope_age(self):
        env_dict = _make_envelope_dict(admin_risk_snapshot_age_hours=24.5)
        rc, _, stderr = _run_seat(envelope_dict=env_dict)
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_ADMIN_RISK_REGISTER_STALE

    def test_admin_risk_register_stale_register_age(self):
        # Belt-and-suspenders branch — register-side age over ceiling.
        rc, _, stderr = _run_seat(register=_make_register(age=99.0))
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_ADMIN_RISK_REGISTER_STALE


class TestW2FCodeMatrixAnthropic:
    """F-codes raised by Anthropic provider exceptions in run_seat."""

    def test_byok_missing(self):
        def _raise(**_: Any) -> AnthropicResponse:
            raise AnthropicBYOKMissing("F-SCRIBE-BYOK-MISSING: empty key")

        rc, _, stderr = _run_seat(anthropic_call=_raise)
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_BYOK_MISSING

    def test_payload_ceiling(self):
        def _raise(**_: Any) -> AnthropicResponse:
            raise AnthropicPayloadCeiling("over ceiling")

        rc, _, stderr = _run_seat(anthropic_call=_raise)
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_PAYLOAD_CEILING

    def test_transport_failure(self):
        def _raise(**_: Any) -> AnthropicResponse:
            raise AnthropicTransportFailure("retry exhausted")

        rc, _, stderr = _run_seat(anthropic_call=_raise)
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_TRANSPORT_FAILURE

    def test_semantic_failure(self):
        def _raise(**_: Any) -> AnthropicResponse:
            raise AnthropicSemanticFailure("400 bad request")

        rc, _, stderr = _run_seat(anthropic_call=_raise)
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_SEMANTIC_FAILURE

    def test_provider_malformed(self):
        def _raise(**_: Any) -> AnthropicResponse:
            raise AnthropicProviderMalformed("non-json body")

        rc, _, stderr = _run_seat(anthropic_call=_raise)
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_PROVIDER_MALFORMED


class TestW2FCodeMatrixPostGate:
    """F-codes raised by ``assemble_scribe_post_gate``."""

    def test_unsourced_claim(self):
        def _unsourced(**_: Any) -> tuple[str, ...]:
            return ("unverifiable claim",)

        rc, _, stderr = _run_seat(
            post_gate=_make_post_gate(source_tag=_unsourced),
        )
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_UNSOURCED_CLAIM

    def test_paraphrased_numeric(self):
        sd = _make_section_draft(body_text="we will hire 7 workers.")

        def _evidence(*, envelope):  # noqa: ARG001
            return "we will hire 5 workers"

        rc, _, stderr = _run_seat(
            response_parse=_make_response_parse(drafts=(sd,)),
            post_gate=_make_post_gate(evidence_text=_evidence),
        )
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_PARAPHRASED_NUMERIC

    def test_dialect_drift(self):
        sd = _make_section_draft(
            body_text="this proposal advances equity for our community.",
            draft_dialect="conservative",
        )
        rc, _, stderr = _run_seat(
            response_parse=_make_response_parse(drafts=(sd,)),
        )
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_DIALECT_DRIFT

    def test_dialect_induced_identity(self):
        sd = _make_section_draft(
            body_text="we draw on ancestral knowledge to grow.",
            draft_dialect="soul_fire",
        )
        rc, _, stderr = _run_seat(
            response_parse=_make_response_parse(drafts=(sd,)),
        )
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_DIALECT_INDUCED_IDENTITY

    def test_section_over_limit_unflagged(self):
        # Construct a CONSISTENT draft (over_limit=True), then mutate the
        # frozen flag to False to test the POST-gate defense-in-depth walker.
        limit = SectionLimit(limit_kind="words", limit_value=3)
        sd = _make_section_draft(
            body_text="we are growing food for our cooperative.",
            over_limit_flag=True,
            rfa_section_limit=limit,
        )
        object.__setattr__(sd, "over_limit_flag", False)
        rc, _, stderr = _run_seat(
            response_parse=_make_response_parse(drafts=(sd,)),
        )
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_SECTION_OVER_LIMIT_UNFLAGGED

    def test_overlooked_expense_unresolved(self):
        sd = _make_section_draft(
            section_name="Budget Narrative",
            body_text="our budget covers labor and materials.",
        )
        rc, _, stderr = _run_seat(
            response_parse=_make_response_parse(drafts=(sd,)),
        )
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_OVERLOOKED_EXPENSE_UNRESOLVED

    def test_ineligible_activity(self):
        bad_match = EligibleActivityMatch(
            activity_phrase="mining bitcoin",
            matched_rfa_activity=None,
            scope_check_flag=True,
        )
        object.__setattr__(bad_match, "scope_check_flag", False)
        sd = _make_section_draft(eligible_activity_map=(bad_match,))
        rc, _, stderr = _run_seat(
            response_parse=_make_response_parse(drafts=(sd,)),
        )
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_INELIGIBLE_ACTIVITY

    def test_conversation_anchor_invalid_shape(self):
        env_dict = _make_envelope_dict(conversation_log_anchor="bogus")
        rc, _, stderr = _run_seat(envelope_dict=env_dict)
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_CONVERSATION_ANCHOR_INVALID

    def test_admin_risk_unflagged(self):
        sd = _make_section_draft(
            body_text="our diversity initiative drives growth.",
        )
        rc, _, stderr = _run_seat(
            response_parse=_make_response_parse(drafts=(sd,)),
        )
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_ADMIN_RISK_UNFLAGGED

    def test_admin_risk_high_unapproved(self):
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
        sd = _make_section_draft(
            body_text="environmental justice frames our work.",
            draft_dialect="progressive",
        )
        flag = AdminRiskFlag(
            term="environmental justice",
            severity="high",
            proposed_substitution="ecological stewardship",
            applicant_approved=False,
        )
        env_dict = _make_envelope_dict(funder_dialect="progressive")
        rc, _, stderr = _run_seat(
            envelope_dict=env_dict,
            response_parse=_make_response_parse(drafts=(sd,), flags=(flag,)),
            register=register,
        )
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_ADMIN_RISK_HIGH_UNAPPROVED


class TestW2FCodeMatrixAdapter:
    """F-codes raised by the admin-risk adapter parser (not via run_seat)."""

    def test_admin_risk_register_malformed_missing_version(self):
        with pytest.raises(AdminRiskRegisterMalformed) as exc:
            parse_admin_risk_register(
                raw_mapping={"entries": [{"term": "x", "severity": "RED"}]},
                snapshot_sha3_512="d" * 128,
                snapshot_age_hours=0.5,
            )
        assert F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED in str(exc.value)

    def test_admin_risk_register_malformed_bad_severity(self):
        with pytest.raises(AdminRiskRegisterMalformed) as exc:
            parse_admin_risk_register(
                raw_mapping={
                    "version": "2.2",
                    "entries": [{"term": "x", "severity": "MAGENTA"}],
                },
                snapshot_sha3_512="d" * 128,
                snapshot_age_hours=0.5,
            )
        assert "MAGENTA" in str(exc.value)
        assert F_SCRIBE_ADMIN_RISK_REGISTER_MALFORMED in str(exc.value)


class TestW2FCodeMatrixDeclaredButOutOfR3Scope:
    """F-codes declared by R1/R2 for §5 R5+ revision-loop wiring.

    Per logician_wiring.assemble_scribe_post_gate docstring (lines 489-496):
    F-SCRIBE-SMART-INVENTED-METRIC and F-SCRIBE-EVALUATION-CRITERION-MISSING
    are declared as constants but NOT advertised in ``codes_checked`` at R3.
    F-SCRIBE-RFA-MISSING and F-SCRIBE-PHASE-0-MISSING ship at R1 for the
    Logician PRE-gate slot table; R3 binds them at the §5 R5+ revision-loop
    layer when the multi-section draft accumulator + Phase-0 prerequisite
    resolver land. These are included in the matrix as presence tests so the
    capstone covers the full §7.13 declared-code surface.
    """

    def test_rfa_missing_constant_present(self):
        assert F_SCRIBE_RFA_MISSING == "F-SCRIBE-RFA-MISSING"
        # Exported from the package.
        assert hasattr(scribe_pkg, "F_SCRIBE_RFA_MISSING")

    def test_phase_0_missing_constant_present(self):
        assert F_SCRIBE_PHASE_0_MISSING == "F-SCRIBE-PHASE-0-MISSING"
        assert hasattr(scribe_pkg, "F_SCRIBE_PHASE_0_MISSING")

    def test_smart_invented_metric_constant_present(self):
        assert F_SCRIBE_SMART_INVENTED_METRIC == "F-SCRIBE-SMART-INVENTED-METRIC"
        assert hasattr(scribe_pkg, "F_SCRIBE_SMART_INVENTED_METRIC")

    def test_evaluation_criterion_missing_constant_present(self):
        assert F_SCRIBE_EVALUATION_CRITERION_MISSING == "F-SCRIBE-EVALUATION-CRITERION-MISSING"
        assert hasattr(scribe_pkg, "F_SCRIBE_EVALUATION_CRITERION_MISSING")


# ---------------------------------------------------------------------------
# W.3 Cross-round composition gaps
# ---------------------------------------------------------------------------


class TestW3CrossRoundComposition:
    """R1 types feed R2 shapers feed R3 seat surface without import-time gaps."""

    def test_r1_types_importable(self):
        from pipeline.seats.scribe import types as r1_types

        # Phase 0 + KGIE shapes
        assert hasattr(r1_types, "RfaExtractedRecord")
        assert hasattr(r1_types, "KgiePreflightResult")
        assert hasattr(r1_types, "IdentityClaim")
        assert hasattr(r1_types, "KeywordCheck")
        assert hasattr(r1_types, "GeographyRecord")
        assert hasattr(r1_types, "ExperienceSummary")
        # R1 F-code constants
        assert hasattr(r1_types, "F_SCRIBE_RFA_MISSING")
        assert hasattr(r1_types, "F_SCRIBE_RFA_DRIFT")
        assert hasattr(r1_types, "F_SCRIBE_PHASE_0_MISSING")
        assert hasattr(r1_types, "F_SCRIBE_KGIE_FAIL")

    def test_r1_kgie_importable(self):
        from pipeline.seats.scribe import kgie as r1_kgie

        assert callable(r1_kgie.kgie_preflight)

    def test_r2_shapers_importable(self):
        from pipeline.seats.scribe import (
            dialect,
            overlooked_expenses,
            program_templates,
            smart,
        )

        assert callable(smart.validate_smart_objective)
        assert callable(overlooked_expenses.is_finalizable)
        assert callable(dialect.detect_dialect_drift)
        assert callable(program_templates.compute_template_sha3_512)

    def test_r2_5_section_draft_importable(self):
        from pipeline.seats.scribe import compress, section_draft

        assert callable(compress.count_words)
        assert hasattr(section_draft, "SectionDraft")
        assert hasattr(section_draft, "ClaimEvidence")
        assert hasattr(section_draft, "ConversationAnchor")
        assert hasattr(section_draft, "EligibleActivityMatch")
        assert hasattr(section_draft, "AdminRiskFlag")
        assert hasattr(section_draft, "CompressedSectionDraft")

    def test_r3_seat_importable(self):
        from pipeline.seats.scribe import (
            admin_risk_adapter,
            logician_wiring,
            provider_anthropic,
            seat,
        )

        assert callable(seat.run_seat)
        assert callable(seat.decode_envelope)
        assert callable(seat.encode_result)
        assert callable(provider_anthropic.call_anthropic_scribe)
        assert callable(admin_risk_adapter.parse_admin_risk_register)
        assert callable(logician_wiring.assemble_scribe_pre_gate)
        assert callable(logician_wiring.assemble_scribe_post_gate)

    def test_r2_5_section_draft_consumed_by_r3_seat(self):
        # SectionDraft constructed via R2.5 shape feeds the run_seat result
        # encoder (R3 surface) byte-identically through an end-to-end run.
        sd = _make_section_draft()
        rc, stdout, _ = _run_seat(response_parse=_make_response_parse(drafts=(sd,)))
        assert rc == EXIT_OK
        decoded = json.loads(stdout)
        assert decoded["section_drafts"][0]["body_text"] == sd.body_text
        assert decoded["section_drafts"][0]["word_count"] == sd.word_count
        assert decoded["section_drafts"][0]["character_count"] == sd.character_count

    def test_blueprint_deps_pin_all_anchors_present(self):
        # R3 BLUEPRINT_DEPS must pin all six §-anchors per the §7 v1.1.1
        # composition surface.
        assert "section_07_scribe.md" in BLUEPRINT_DEPS
        assert "section_00_5_section_07_scribe_amendment.md" in BLUEPRINT_DEPS
        assert "section_04_logician.md" in BLUEPRINT_DEPS
        assert "section_06_operating_envelope.md" in BLUEPRINT_DEPS
        assert "section_05_pipeline.md" in BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in BLUEPRINT_DEPS

    def test_blueprint_deps_pin_hash_format(self):
        # All hashes must be 16 lowercase-hex chars (sha3_512 prefix16).
        for anchor, payload in BLUEPRINT_DEPS.items():
            del anchor
            h = payload["hash_sha3_512_prefix16"]
            assert isinstance(h, str)
            assert len(h) == 16
            assert all(c in "0123456789abcdef" for c in h)

    def test_blueprint_deps_pin_section_07_v1_1_1(self):
        # §7 anchor pins v1.1.1 — promoted under the same blueprint version
        # by R1/R2/R2.5/R3 and reaffirmed by the whole-section capstone.
        section_07 = BLUEPRINT_DEPS["section_07_scribe.md"]
        assert section_07["version"] == "v1.1.1"

    def test_all_f_scribe_codes_uniquely_named(self):
        # Each F-SCRIBE-* string constant maps to a distinct value — no two
        # constants share a value (catch copy-paste regression in §7.13).
        f_codes = {
            name: getattr(scribe_pkg, name)
            for name in scribe_pkg.__all__
            if name.startswith("F_SCRIBE_")
        }
        # 29 declared F-codes per §7.13 R3 surface.
        assert len(f_codes) == 29
        assert len(set(f_codes.values())) == 29

    def test_all_f_scribe_codes_have_canonical_prefix(self):
        for name in scribe_pkg.__all__:
            if not name.startswith("F_SCRIBE_"):
                continue
            value = getattr(scribe_pkg, name)
            assert isinstance(value, str)
            assert value.startswith("F-SCRIBE-")

    def test_all_f_scribe_codes_use_dash_separator(self):
        # F-codes are dash-separated UPPER-KEBAB; never carry underscores or
        # lowercase letters in the body.
        for name in scribe_pkg.__all__:
            if not name.startswith("F_SCRIBE_"):
                continue
            value = getattr(scribe_pkg, name)
            body = value[len("F-SCRIBE-") :]
            assert "_" not in body
            assert body == body.upper()

    def test_envelope_decode_to_pre_gate_round_trip(self):
        # Envelope decoded from canonical JSON feeds the assembler
        # constructor without re-encoding.
        env = _make_envelope()
        out = assemble_scribe_pre_gate(
            envelope=env,
            admin_risk_register=_make_register(),
            cedar_cross_org_check=_no_foreign_orgs,
            kgie_status_getter=_kgie_pass,
            rfa_drift_check=_no_rfa_drift,
            template_drift_check=_no_template_drift,
        )
        assert isinstance(out, PreGateAssembly)
        assert out.run_id == env.run_id
        assert out.org_slug == env.org_slug

    def test_envelope_decode_to_post_gate_round_trip(self):
        env = _make_envelope()
        out = assemble_scribe_post_gate(
            envelope=env,
            section_drafts=(_make_section_draft(),),
            admin_risk_flags=(),
            admin_risk_register=_make_register(),
            source_tag_verify=_no_unsourced,
            conversation_anchor_verify=_anchor_match,
            evidence_text_provider=_empty_evidence,
            identity_claim_provider=_no_identity,
        )
        assert isinstance(out, PostGateAssembly)
        assert out.run_id == env.run_id
        assert out.org_slug == env.org_slug

    def test_pre_gate_codes_checked_subset(self):
        env = _make_envelope()
        out = assemble_scribe_pre_gate(
            envelope=env,
            admin_risk_register=_make_register(),
            cedar_cross_org_check=_no_foreign_orgs,
            kgie_status_getter=_kgie_pass,
            rfa_drift_check=_no_rfa_drift,
            template_drift_check=_no_template_drift,
        )
        # Must advertise the 8 R3 PRE-gate codes.
        assert F_SCRIBE_ORG_CROSS_REF in out.codes_checked
        assert F_SCRIBE_KGIE_FAIL in out.codes_checked
        assert F_SCRIBE_RFA_DRIFT in out.codes_checked
        assert F_SCRIBE_SCOPE_MISSING in out.codes_checked
        assert F_SCRIBE_DIALECT_UNCLASSIFIED in out.codes_checked
        assert F_SCRIBE_TEMPLATE_UNKNOWN in out.codes_checked
        assert F_SCRIBE_TEMPLATE_DRIFT in out.codes_checked
        assert F_SCRIBE_ADMIN_RISK_REGISTER_STALE in out.codes_checked

    def test_post_gate_codes_checked_subset(self):
        env = _make_envelope()
        out = assemble_scribe_post_gate(
            envelope=env,
            section_drafts=(_make_section_draft(),),
            admin_risk_flags=(),
            admin_risk_register=_make_register(),
            source_tag_verify=_no_unsourced,
            conversation_anchor_verify=_anchor_match,
            evidence_text_provider=_empty_evidence,
            identity_claim_provider=_no_identity,
        )
        # Must advertise the 10 R3 POST-gate codes.
        assert F_SCRIBE_UNSOURCED_CLAIM in out.codes_checked
        assert F_SCRIBE_PARAPHRASED_NUMERIC in out.codes_checked
        assert F_SCRIBE_DIALECT_INDUCED_IDENTITY in out.codes_checked
        assert F_SCRIBE_DIALECT_DRIFT in out.codes_checked
        assert F_SCRIBE_SECTION_OVER_LIMIT_UNFLAGGED in out.codes_checked
        assert F_SCRIBE_OVERLOOKED_EXPENSE_UNRESOLVED in out.codes_checked
        assert F_SCRIBE_INELIGIBLE_ACTIVITY in out.codes_checked
        assert F_SCRIBE_CONVERSATION_ANCHOR_INVALID in out.codes_checked
        assert F_SCRIBE_ADMIN_RISK_UNFLAGGED in out.codes_checked
        assert F_SCRIBE_ADMIN_RISK_HIGH_UNAPPROVED in out.codes_checked

    def test_post_gate_does_not_advertise_r5_deferred_codes(self):
        # Per assembler docstring: F-SCRIBE-SMART-INVENTED-METRIC and
        # F-SCRIBE-EVALUATION-CRITERION-MISSING are R3 out-of-scope.
        env = _make_envelope()
        out = assemble_scribe_post_gate(
            envelope=env,
            section_drafts=(_make_section_draft(),),
            admin_risk_flags=(),
            admin_risk_register=_make_register(),
            source_tag_verify=_no_unsourced,
            conversation_anchor_verify=_anchor_match,
            evidence_text_provider=_empty_evidence,
            identity_claim_provider=_no_identity,
        )
        assert F_SCRIBE_SMART_INVENTED_METRIC not in out.codes_checked
        assert F_SCRIBE_EVALUATION_CRITERION_MISSING not in out.codes_checked

    def test_dialect_vocabulary_immutable_at_module_load(self):
        # Captured frozen — trying to mutate the proxy raises.
        with pytest.raises(TypeError):
            DIALECT_VOCABULARY["conservative"] = frozenset()  # type: ignore[index]

    def test_known_programs_are_complete(self):
        # §7.9 ships eight programs (VAPG / REAP / SCBGP / SARE / SBIR /
        # AFRI / 2501 / UAIP). Whole-section capstone re-pins this so a
        # row-append must retest the catalog.
        expected = {"VAPG", "REAP", "SCBGP", "SARE", "SBIR", "AFRI", "2501", "UAIP"}
        assert set(KNOWN_PROGRAMS.keys()) == expected

    def test_snapshot_age_ceiling_is_24_hours(self):
        # §6.13 v1-r1 LOCKED 24h ceiling; constant is human-reading only,
        # but this test pins the value so a future operator-side rebind
        # can't silently widen the freshness window.
        assert SNAPSHOT_AGE_HOURS_CEILING == 24.0


# ---------------------------------------------------------------------------
# W.4 Adversarial — defense-in-depth across composed surface
# ---------------------------------------------------------------------------


class TestW4Adversarial:

    def test_pre_gate_trip_short_circuits_post_gate(self):
        # PRE-gate raises → POST-gate never runs (verify by counting calls).
        post_calls: list[Any] = []

        def _track_post(**kwargs: Any) -> None:
            post_calls.append(kwargs)

        def _foreign(**_: Any) -> tuple[str, ...]:
            return ("competitor_org",)

        rc, _, _ = _run_seat(
            pre_gate=_make_pre_gate(cedar=_foreign),
            post_gate=_track_post,
        )
        assert rc == EXIT_GATE_FAIL
        assert post_calls == []

    def test_anthropic_unhandled_exception_is_bug_class_exit_1(self):
        class _NewException(RuntimeError):
            pass

        def _raise(**_: Any) -> AnthropicResponse:
            raise _NewException("synthetic")

        rc, _, stderr = _run_seat(anthropic_call=_raise)
        # Defense-in-depth: not every Anthropic-class exception maps to a
        # known F-code; bug-class is exit 1, distinguishable from gate-class.
        assert rc == EXIT_INTERNAL_ERROR
        assert b"anthropic_call raised unhandled exception" in stderr
        assert b"class=_NewException" in stderr

    def test_response_parse_seat_bug_is_exit_1(self):
        def _parse_bug(*, response, envelope):  # noqa: ARG001
            raise KeyError("unexpected schema")

        rc, _, stderr = _run_seat(response_parse=_parse_bug)
        assert rc == EXIT_INTERNAL_ERROR
        assert b"response_parse raised" in stderr

    def test_post_gate_seat_bug_is_exit_1(self):
        def _post_bug(**_: Any) -> None:
            raise TypeError("seat bug")

        rc, _, stderr = _run_seat(post_gate=_post_bug)
        assert rc == EXIT_INTERNAL_ERROR
        assert b"post_gate raised unhandled exception" in stderr
        assert b"class=TypeError" in stderr

    def test_pre_gate_seat_bug_is_exit_1(self):
        def _pre_bug(**_: Any) -> None:
            raise RuntimeError("pre_gate seat bug")

        rc, _, stderr = _run_seat(pre_gate=_pre_bug)
        assert rc == EXIT_INTERNAL_ERROR
        assert b"pre_gate raised unhandled exception" in stderr
        assert b"class=RuntimeError" in stderr

    def test_admin_risk_fetch_unhandled_is_exit_1(self):
        def _fetch_bug(*, envelope):  # noqa: ARG001
            raise OSError("vault disk read failed")

        rc, _, stderr = _run_seat(admin_risk_fetch=_fetch_bug)
        assert rc == EXIT_INTERNAL_ERROR
        assert b"admin_risk_fetch raised unhandled exception" in stderr
        assert b"class=OSError" in stderr

    def test_two_post_gate_violations_first_detection_wins(self):
        # Body simultaneously trips dialect-drift AND admin-risk-unflagged.
        # POST-gate ordering: source-tag → numeric → induced-identity →
        # dialect-drift → ... → admin-risk. Dialect drift fires first.
        sd = _make_section_draft(
            body_text="our diversity initiative advances equity for community.",
            draft_dialect="conservative",
        )
        rc, _, stderr = _run_seat(
            response_parse=_make_response_parse(drafts=(sd,)),
        )
        assert rc == EXIT_GATE_FAIL
        # Either drift or unflagged is acceptable (both are real violations);
        # the deterministic order pins drift first per assembler design.
        assert _stderr_failure_code(stderr) == F_SCRIBE_DIALECT_DRIFT

    def test_envelope_with_uppercase_shell_hash_rejected(self):
        # Defense against accidentally-uppercased shell hash (canonical-form
        # invariant from §6.11).
        env_dict = _make_envelope_dict(compiled_prompt_shell_sha3_512="A" * 128)
        rc, _, stderr = _run_seat(envelope_dict=env_dict)
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_SCRIBE_ENVELOPE_MALFORMED

    def test_stderr_failure_payload_includes_envelope_version(self):
        # Every gate-class stderr line MUST carry the canonical envelope
        # version so downstream log readers can route by version.
        rc, _, stderr = _run_seat(
            pre_gate=lambda **_: (_ for _ in ()).throw(
                ScribeGateFailed(
                    failure_code=F_SCRIBE_ORG_CROSS_REF,
                    trigger="synthetic",
                    evidence={},
                )
            ),
        )
        assert rc == EXIT_GATE_FAIL
        line = json.loads(stderr.decode("utf-8").strip())
        assert line["envelope_version"] == ENVELOPE_VERSION_V1
        assert line["failure_code"] == F_SCRIBE_ORG_CROSS_REF
        assert "emitted_at_utc" in line

    def test_admin_risk_scan_skips_low_severity_in_post_gate_default(self):
        # `verify_draft_flags_or_raise` skips LOW even when the term matches.
        # POST-gate composition path passes when no MEDIUM/HIGH match.
        register = _make_register(severity="low")
        sd = _make_section_draft(
            body_text="our diversity initiative drives growth.",
        )
        flags = scan_draft_for_admin_risk(
            draft_body=sd.body_text,
            register=register,
            funder_dialect="conservative",
        )
        assert len(flags) == 1
        assert flags[0].term == "diversity"
        assert flags[0].severity == "low"
        # Through the seat, even without declared flag → PASS (LOW skipped).
        rc, _, stderr = _run_seat(
            response_parse=_make_response_parse(drafts=(sd,)),
            register=register,
        )
        assert rc == EXIT_OK
        assert stderr == b""

    def test_envelope_round_trip_preserves_run_id_through_result(self):
        # Run-id flows envelope → result without mutation (audit-trail
        # invariant for §5 R3+ vault-record pairing).
        env_dict = _make_envelope_dict(run_id="run-special-2026-04-29-XYZ")
        rc, stdout, _ = _run_seat(envelope_dict=env_dict)
        assert rc == EXIT_OK
        decoded = json.loads(stdout)
        assert decoded["run_id"] == "run-special-2026-04-29-XYZ"
