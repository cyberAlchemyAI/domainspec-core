"""Round-3 tests for ``pipeline.seats.scribe.seat``.

Covers the subprocess entry contract: envelope decoding, exit-code routing,
gate-trip stderr emission, Anthropic exception → exit-code mapping, and
the result encoder. Uses fully-injected E-017 seams so tests are
deterministic and run with no network / subprocess / clock.
"""
from __future__ import annotations

import io
import json
from datetime import datetime, timezone
from typing import Any, Mapping

import pytest

from pipeline.seats.scribe.admin_risk_adapter import AdminRiskRegister, AdminRiskEntry
from pipeline.seats.scribe.provider_anthropic import (
    AnthropicBYOKMissing,
    AnthropicPayloadCeiling,
    AnthropicProviderMalformed,
    AnthropicResponse,
    AnthropicSemanticFailure,
    AnthropicTransportFailure,
)
from pipeline.seats.scribe.seat import (
    ENVELOPE_VERSION_V1,
    EXIT_GATE_FAIL,
    EXIT_INTERNAL_ERROR,
    EXIT_OK,
    F_SCRIBE_CONVERSATION_ANCHOR_INVALID,
    F_SCRIBE_ENVELOPE_MALFORMED,
    F_SCRIBE_INELIGIBLE_ACTIVITY,
    RESULT_VERSION_V1,
    ScribeEnvelope,
    ScribeEnvelopeMalformed,
    ScribeGateFailed,
    ScribeResult,
    decode_envelope,
    encode_result,
    run_seat,
)
from pipeline.seats.scribe.section_draft import (
    AdminRiskFlag,
    EligibleActivityMatch,
    SectionDraft,
)


# ---------------------------------------------------------------------------
# Fixtures + helpers
# ---------------------------------------------------------------------------


_SHELL_HASH_128 = "a" * 128
_FIXED_NOW = datetime(2026, 4, 22, 12, 0, tzinfo=timezone.utc)


def _make_envelope_dict(**overrides: Any) -> dict[str, Any]:
    base = {
        "envelope_version": "scribe-envelope.v1",
        "run_id": "run-2026-04-22-001",
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
        "envelope_emitted_at_utc": "2026-04-22T12:00:00+00:00",
    }
    base.update(overrides)
    return base


def _make_envelope(**overrides: Any) -> ScribeEnvelope:
    raw = json.dumps(_make_envelope_dict(**overrides)).encode("utf-8")
    return decode_envelope(raw_bytes=raw)


def _make_section_draft() -> SectionDraft:
    body = "FIT Farms operates a 50-acre cooperative."
    return SectionDraft(
        section_name="Project Narrative",
        section_order=1,
        body_text=body,
        word_count=6,
        character_count=len(body),
        over_limit_flag=False,
        rfa_section_limit=None,
        draft_dialect="conservative",
        drafted_at_utc=_FIXED_NOW,
        claim_evidence_map=(),
        eligible_activity_map=(),
        admin_risk_flags=(),
        scope_check_comments=(),
    )


def _make_register() -> AdminRiskRegister:
    return AdminRiskRegister(
        version="2.2",
        entries=(
            AdminRiskEntry(
                term="dei",
                severity="medium",
                progressive_register="OK",
                suggested_substitutions=("inclusion",),
                context="federal admin-risk",
                variants=(),
            ),
        ),
        snapshot_sha3_512="b" * 128,
        snapshot_age_hours=0.5,
    )


def _clock() -> datetime:
    return _FIXED_NOW


def _admin_risk_fetch(*, envelope: ScribeEnvelope) -> AdminRiskRegister:
    return _make_register()


def _anthropic_call_ok(**kwargs: Any) -> AnthropicResponse:
    return AnthropicResponse(
        text_body="parsed-body",
        landed_model_id="claude-sonnet-4-5-20250929",
        response_sha3_512="c" * 128,
        prompt_token_estimate=128,
        raw_response_canonical_json_bytes=b'{"k":"v"}',
    )


def _response_parse_ok(
    *, response: AnthropicResponse, envelope: ScribeEnvelope
) -> tuple[tuple[SectionDraft, ...], tuple[AdminRiskFlag, ...]]:
    return (_make_section_draft(),), ()


def _pre_gate_pass(*, envelope: ScribeEnvelope, admin_risk_register: AdminRiskRegister) -> None:
    return None


def _post_gate_pass(
    *,
    envelope: ScribeEnvelope,
    section_drafts: tuple[SectionDraft, ...],
    admin_risk_flags: tuple[AdminRiskFlag, ...],
    admin_risk_register: AdminRiskRegister,
) -> None:
    return None


def _run(
    *,
    stdin_bytes: bytes,
    anthropic_call: Any = _anthropic_call_ok,
    response_parse: Any = _response_parse_ok,
    pre_gate: Any = _pre_gate_pass,
    post_gate: Any = _post_gate_pass,
    admin_risk_fetch: Any = _admin_risk_fetch,
) -> tuple[int, bytes, bytes]:
    stdin = io.BytesIO(stdin_bytes)
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


# ---------------------------------------------------------------------------
# Envelope decode tests
# ---------------------------------------------------------------------------


class TestEnvelopeDecode:

    def test_happy_path_decodes(self):
        env = _make_envelope()
        assert env.envelope_version == ENVELOPE_VERSION_V1
        assert env.run_id == "run-2026-04-22-001"
        assert env.org_slug == "fit_farms_llc"
        assert env.section_order == 1
        assert env.envelope_emitted_at_utc.tzinfo is not None

    def test_empty_stdin_raises(self):
        with pytest.raises(ScribeEnvelopeMalformed) as exc:
            decode_envelope(raw_bytes=b"")
        assert F_SCRIBE_ENVELOPE_MALFORMED in str(exc.value)

    def test_invalid_utf8_raises(self):
        with pytest.raises(ScribeEnvelopeMalformed) as exc:
            decode_envelope(raw_bytes=b"\xff\xfe\xfa not utf8")
        assert "stdin not UTF-8" in str(exc.value)

    def test_non_object_top_level_raises(self):
        with pytest.raises(ScribeEnvelopeMalformed) as exc:
            decode_envelope(raw_bytes=b'["arrays-not-allowed"]')
        assert "top-level must be object" in str(exc.value)

    def test_wrong_envelope_version_raises(self):
        raw = json.dumps(_make_envelope_dict(envelope_version="scribe-envelope.v2")).encode("utf-8")
        with pytest.raises(ScribeEnvelopeMalformed) as exc:
            decode_envelope(raw_bytes=raw)
        assert "envelope_version must be" in str(exc.value)

    def test_missing_required_keys_raises(self):
        d = _make_envelope_dict()
        del d["compiled_prompt"]
        raw = json.dumps(d).encode("utf-8")
        with pytest.raises(ScribeEnvelopeMalformed) as exc:
            decode_envelope(raw_bytes=raw)
        assert "missing keys" in str(exc.value)

    def test_naive_datetime_rejected(self):
        # ISO-8601 string with no offset → naive datetime → __post_init__ trips
        with pytest.raises(ScribeEnvelopeMalformed) as exc:
            _make_envelope(envelope_emitted_at_utc="2026-04-22T12:00:00")
        assert "timezone-aware" in str(exc.value)

    def test_bad_dialect_rejected(self):
        with pytest.raises(ScribeEnvelopeMalformed) as exc:
            _make_envelope(funder_dialect="anarchist")
        assert "funder_dialect must be one of" in str(exc.value)

    def test_short_shell_hash_rejected(self):
        with pytest.raises(ScribeEnvelopeMalformed) as exc:
            _make_envelope(compiled_prompt_shell_sha3_512="a" * 64)
        assert "128 hex chars" in str(exc.value)

    def test_uppercase_shell_hash_rejected(self):
        with pytest.raises(ScribeEnvelopeMalformed) as exc:
            _make_envelope(compiled_prompt_shell_sha3_512="A" * 128)
        assert "lowercase hex" in str(exc.value)

    def test_negative_iteration_rejected(self):
        with pytest.raises(ScribeEnvelopeMalformed):
            _make_envelope(iteration_number=-1)

    def test_section_order_below_1_rejected(self):
        with pytest.raises(ScribeEnvelopeMalformed):
            _make_envelope(section_order=0)

    def test_negative_snapshot_age_rejected(self):
        with pytest.raises(ScribeEnvelopeMalformed):
            _make_envelope(admin_risk_snapshot_age_hours=-0.1)


# ---------------------------------------------------------------------------
# Result encoder tests
# ---------------------------------------------------------------------------


class TestResultEncoder:

    def _make_result(self, **overrides: Any) -> ScribeResult:
        base = dict(
            result_version="scribe-result.v1",
            run_id="run-1",
            org_slug="fit_farms_llc",
            iteration_number=0,
            section_drafts=(_make_section_draft(),),
            compiled_prompt_shell_sha3_512=_SHELL_HASH_128,
            provider_landed_family="anthropic",
            provider_landed_model_id="claude-sonnet-4-5-20250929",
            admin_risk_flags=(),
            seat_emitted_at_utc=_FIXED_NOW,
        )
        base.update(overrides)
        return ScribeResult(**base)

    def test_encode_emits_canonical_json_with_trailing_newline(self):
        result = self._make_result()
        out = encode_result(result)
        assert out.endswith(b"\n")
        decoded = json.loads(out)
        assert decoded["result_version"] == RESULT_VERSION_V1
        assert decoded["section_drafts_count"] == 1
        # canonical: keys sorted
        keys = list(decoded.keys())
        assert keys == sorted(keys)

    def test_encode_is_deterministic(self):
        a = encode_result(self._make_result())
        b = encode_result(self._make_result())
        assert a == b

    def test_encode_strips_no_separators(self):
        # canonical separators `(",", ":")` — no spaces in the JSON
        out = encode_result(self._make_result())
        assert b", " not in out
        assert b": " not in out

    def test_result_rejects_wrong_version(self):
        with pytest.raises(ValueError):
            self._make_result(result_version="scribe-result.v2")

    def test_result_rejects_empty_section_drafts(self):
        with pytest.raises(ValueError):
            self._make_result(section_drafts=())


# ---------------------------------------------------------------------------
# run_seat exit-code routing tests
# ---------------------------------------------------------------------------


class TestRunSeatExitCodes:

    def test_happy_path_returns_0(self):
        rc, stdout, stderr = _run(
            stdin_bytes=json.dumps(_make_envelope_dict()).encode("utf-8")
        )
        assert rc == EXIT_OK
        assert stderr == b""
        decoded = json.loads(stdout)
        assert decoded["result_version"] == RESULT_VERSION_V1
        assert decoded["provider_landed_family"] == "anthropic"
        assert decoded["section_drafts_count"] == 1

    def test_empty_stdin_routes_to_exit_2_envelope_malformed(self):
        rc, stdout, stderr = _run(stdin_bytes=b"")
        assert rc == EXIT_GATE_FAIL
        assert stdout == b""
        line = json.loads(stderr.decode("utf-8").strip())
        assert line["failure_code"] == F_SCRIBE_ENVELOPE_MALFORMED
        assert line["envelope_version"] == ENVELOPE_VERSION_V1

    def test_pre_gate_trip_routes_to_exit_2(self):
        def _bad_pre(*, envelope, admin_risk_register):
            raise ScribeGateFailed(
                failure_code="F-SCRIBE-ORG-CROSS-REF",
                trigger="cedar_tripped",
                evidence={"foreign_slugs": ["other_org"]},
            )

        rc, stdout, stderr = _run(
            stdin_bytes=json.dumps(_make_envelope_dict()).encode("utf-8"),
            pre_gate=_bad_pre,
        )
        assert rc == EXIT_GATE_FAIL
        line = json.loads(stderr.decode("utf-8").strip())
        assert line["failure_code"] == "F-SCRIBE-ORG-CROSS-REF"
        assert line["trigger"] == "cedar_tripped"

    def test_post_gate_trip_routes_to_exit_2(self):
        def _bad_post(*, envelope, section_drafts, admin_risk_flags, admin_risk_register):
            raise ScribeGateFailed(
                failure_code=F_SCRIBE_INELIGIBLE_ACTIVITY,
                trigger="unmatched_activity_without_scope_check_flag",
                evidence={"activities": ["mining bitcoin"]},
            )

        rc, stdout, stderr = _run(
            stdin_bytes=json.dumps(_make_envelope_dict()).encode("utf-8"),
            post_gate=_bad_post,
        )
        assert rc == EXIT_GATE_FAIL
        line = json.loads(stderr.decode("utf-8").strip())
        assert line["failure_code"] == F_SCRIBE_INELIGIBLE_ACTIVITY

    def test_byok_missing_routes_to_exit_2(self):
        def _byok_raise(**kwargs):
            raise AnthropicBYOKMissing("ANTHROPIC_API_KEY empty")

        rc, _, stderr = _run(
            stdin_bytes=json.dumps(_make_envelope_dict()).encode("utf-8"),
            anthropic_call=_byok_raise,
        )
        assert rc == EXIT_GATE_FAIL
        line = json.loads(stderr.decode("utf-8").strip())
        assert line["failure_code"] == "F-SCRIBE-BYOK-MISSING"

    def test_payload_ceiling_routes_to_exit_2(self):
        def _ceiling_raise(**kwargs):
            raise AnthropicPayloadCeiling("over 200k chars")

        rc, _, stderr = _run(
            stdin_bytes=json.dumps(_make_envelope_dict()).encode("utf-8"),
            anthropic_call=_ceiling_raise,
        )
        assert rc == EXIT_GATE_FAIL
        line = json.loads(stderr.decode("utf-8").strip())
        assert line["failure_code"] == "F-SCRIBE-PAYLOAD-CEILING"

    def test_transport_failure_routes_to_exit_2(self):
        def _transport_raise(**kwargs):
            raise AnthropicTransportFailure("retry exhausted")

        rc, _, stderr = _run(
            stdin_bytes=json.dumps(_make_envelope_dict()).encode("utf-8"),
            anthropic_call=_transport_raise,
        )
        assert rc == EXIT_GATE_FAIL
        line = json.loads(stderr.decode("utf-8").strip())
        assert line["failure_code"] == "F-SCRIBE-TRANSPORT-FAILURE"

    def test_semantic_failure_routes_to_exit_2(self):
        def _sem_raise(**kwargs):
            raise AnthropicSemanticFailure("400 bad request")

        rc, _, stderr = _run(
            stdin_bytes=json.dumps(_make_envelope_dict()).encode("utf-8"),
            anthropic_call=_sem_raise,
        )
        assert rc == EXIT_GATE_FAIL
        line = json.loads(stderr.decode("utf-8").strip())
        assert line["failure_code"] == "F-SCRIBE-SEMANTIC-FAILURE"

    def test_provider_malformed_routes_to_exit_2(self):
        def _malformed_raise(**kwargs):
            raise AnthropicProviderMalformed("non-json body")

        rc, _, stderr = _run(
            stdin_bytes=json.dumps(_make_envelope_dict()).encode("utf-8"),
            anthropic_call=_malformed_raise,
        )
        assert rc == EXIT_GATE_FAIL
        line = json.loads(stderr.decode("utf-8").strip())
        assert line["failure_code"] == "F-SCRIBE-PROVIDER-MALFORMED"

    def test_response_parse_bug_routes_to_exit_1(self):
        def _bad_parse(*, response, envelope):
            raise KeyError("unexpected schema")  # NOT a ScribeGateFailed

        rc, stdout, stderr = _run(
            stdin_bytes=json.dumps(_make_envelope_dict()).encode("utf-8"),
            response_parse=_bad_parse,
        )
        assert rc == EXIT_INTERNAL_ERROR
        assert b"response_parse raised" in stderr

    def test_response_parse_gate_failed_routes_to_exit_2(self):
        def _gate_parse(*, response, envelope):
            raise ScribeGateFailed(
                failure_code=F_SCRIBE_CONVERSATION_ANCHOR_INVALID,
                trigger="parse_anchor_bad",
                evidence={},
            )

        rc, _, stderr = _run(
            stdin_bytes=json.dumps(_make_envelope_dict()).encode("utf-8"),
            response_parse=_gate_parse,
        )
        assert rc == EXIT_GATE_FAIL
        line = json.loads(stderr.decode("utf-8").strip())
        assert line["failure_code"] == F_SCRIBE_CONVERSATION_ANCHOR_INVALID

    def test_admin_risk_fetch_gate_failed_routes_to_exit_2(self):
        def _fetch_fail(*, envelope):
            raise ScribeGateFailed(
                failure_code="F-SCRIBE-ADMIN-RISK-REGISTER-MALFORMED",
                trigger="bad_yaml",
                evidence={},
            )

        rc, _, stderr = _run(
            stdin_bytes=json.dumps(_make_envelope_dict()).encode("utf-8"),
            admin_risk_fetch=_fetch_fail,
        )
        assert rc == EXIT_GATE_FAIL
        line = json.loads(stderr.decode("utf-8").strip())
        assert line["failure_code"] == "F-SCRIBE-ADMIN-RISK-REGISTER-MALFORMED"

    def test_stderr_payload_includes_emitted_at_utc(self):
        rc, _, stderr = _run(stdin_bytes=b"")
        line = json.loads(stderr.decode("utf-8").strip())
        # ISO format with offset
        assert "T" in line["emitted_at_utc"]
        assert line["emitted_at_utc"].endswith("+00:00")

    def test_anthropic_call_unhandled_exception_routes_to_exit_1(self):
        """gpt_oss adversarial finding F-1: defense-in-depth catch for any
        Anthropic-class exception not enumerated. Treated as bug-class
        (exit 1) — distinguishable from gate-class (exit 2). Sanitized
        stderr format: class name only, no traceback / repr (gpt_oss
        cycle-2 fingerprint-leak finding)."""

        class _FutureAnthropicException(RuntimeError):
            pass

        def _future_raise(**kwargs):
            raise _FutureAnthropicException(
                "secret message with /users/op/path data"
            )

        rc, _, stderr = _run(
            stdin_bytes=json.dumps(_make_envelope_dict()).encode("utf-8"),
            anthropic_call=_future_raise,
        )
        assert rc == EXIT_INTERNAL_ERROR
        assert b"anthropic_call raised unhandled exception" in stderr
        assert b"class=_FutureAnthropicException" in stderr
        # Defense-in-depth: NO leaking of exception .args content
        assert b"/users/op/path" not in stderr

    def test_admin_risk_fetch_non_gate_exception_routes_to_exit_1(self):
        """gpt_oss cycle-3 finding F-1: defense-in-depth catch for any
        non-ScribeGateFailed exception from the vault-primitive seam."""

        def _fetch_bug(*, envelope):
            raise OSError("vault disk read failed at /v/admin_risk.yaml")

        rc, _, stderr = _run(
            stdin_bytes=json.dumps(_make_envelope_dict()).encode("utf-8"),
            admin_risk_fetch=_fetch_bug,
        )
        assert rc == EXIT_INTERNAL_ERROR
        assert b"admin_risk_fetch raised unhandled exception" in stderr
        assert b"class=OSError" in stderr
        # Defense-in-depth: filesystem path must NOT leak.
        assert b"/v/admin_risk.yaml" not in stderr

    def test_pre_gate_non_gate_exception_routes_to_exit_1(self):
        """gpt_oss cycle-3 finding F-2: defense-in-depth catch for any
        non-ScribeGateFailed exception from pre_gate."""

        def _pre_bug(*, envelope, admin_risk_register):
            raise RuntimeError("pre_gate has a bug at line /op/path:42")

        rc, _, stderr = _run(
            stdin_bytes=json.dumps(_make_envelope_dict()).encode("utf-8"),
            pre_gate=_pre_bug,
        )
        assert rc == EXIT_INTERNAL_ERROR
        assert b"pre_gate raised unhandled exception" in stderr
        assert b"class=RuntimeError" in stderr
        assert b"/op/path" not in stderr

    def test_anthropic_evidence_field_does_not_leak_str_exc(self):
        """gpt_oss cycle-3 finding F-3: structured-stderr `evidence` field
        must carry only `exception_class`, never `str(exc)`. Defense-in-
        depth against provider-level error messages echoing prompt content
        or operator filesystem paths."""

        def _byok_raise(**kwargs):
            raise AnthropicBYOKMissing(
                "F-SCRIBE-BYOK-MISSING: keystore retrieve failed for "
                "org=fit_farms_llc with /private/keychain leak data"
            )

        rc, _, stderr = _run(
            stdin_bytes=json.dumps(_make_envelope_dict()).encode("utf-8"),
            anthropic_call=_byok_raise,
        )
        assert rc == EXIT_GATE_FAIL
        line = json.loads(stderr.decode("utf-8").strip())
        assert line["evidence"]["exception_class"] == "AnthropicBYOKMissing"
        # Defense-in-depth: full exception .args content must not leak.
        assert "/private/keychain" not in stderr.decode("utf-8")
        # The org_slug is intentionally surfaced in BYOK failures (operator
        # diagnostic — which org's keystore failed) — but the rest is class only.
        assert line["evidence"]["org_slug"] == "fit_farms_llc"

    def test_post_gate_non_gate_exception_routes_to_exit_1(self):
        """gpt_oss adversarial finding F-2: post_gate raising a
        non-ScribeGateFailed exception is bug-class (exit 1). Same
        sanitized stderr format."""

        def _post_bug(**kwargs):
            raise TypeError("post_gate has a bug with /private/path")

        rc, _, stderr = _run(
            stdin_bytes=json.dumps(_make_envelope_dict()).encode("utf-8"),
            post_gate=_post_bug,
        )
        assert rc == EXIT_INTERNAL_ERROR
        assert b"post_gate raised unhandled exception" in stderr
        assert b"class=TypeError" in stderr
        assert b"/private/path" not in stderr
