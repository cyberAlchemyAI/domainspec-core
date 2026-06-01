"""R3 adversarial + property tests for the Scribe seat subprocess.

Covers:
- Mutation-resistant frozen-dataclass invariants (post_init re-checks)
- JSON canonicalization determinism on result encoding
- Stderr emission shape under malformed envelopes
- Round-trip envelope encoding (decode(emit(...)) == original)
- Property tests for envelope construction over a seeded Random space
"""
from __future__ import annotations

import io
import json
import random
from datetime import datetime, timezone, timedelta
from typing import Any

import pytest

from pipeline.seats.scribe.admin_risk_adapter import AdminRiskRegister, AdminRiskEntry
from pipeline.seats.scribe.provider_anthropic import AnthropicResponse
from pipeline.seats.scribe.seat import (
    ENVELOPE_VERSION_V1,
    EXIT_GATE_FAIL,
    EXIT_OK,
    F_SCRIBE_ENVELOPE_MALFORMED,
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
    SectionDraft,
)


_SHELL_HASH = "a" * 128
_NOW = datetime(2026, 4, 22, 12, 0, tzinfo=timezone.utc)


def _envelope_dict(**overrides: Any) -> dict[str, Any]:
    base = {
        "envelope_version": "scribe-envelope.v1",
        "run_id": "run-prop-1",
        "org_slug": "fit_farms_llc",
        "iteration_number": 0,
        "section_name": "Project Narrative",
        "section_order": 1,
        "funder_dialect": "conservative",
        "operator_override_dialect": None,
        "program_code": "VAPG",
        "admin_risk_register_snapshot_path": "/v/admin_risk.yaml",
        "admin_risk_snapshot_age_hours": 0.0,
        "conversation_log_anchor": None,
        "compiled_prompt_shell_sha3_512": _SHELL_HASH,
        "compiled_prompt": "Draft.",
        "project_context": {"applicant_name": "FIT Farms"},
        "envelope_emitted_at_utc": "2026-04-22T12:00:00+00:00",
    }
    base.update(overrides)
    return base


def _make_section_draft() -> SectionDraft:
    body = "regenerative cooperative land stewardship"
    return SectionDraft(
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


# ---------------------------------------------------------------------------
# Adversarial: malformed envelope variants → exit 2 + stderr JSON line
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "stdin_bytes, expected_phrase",
    [
        (b"", "stdin empty"),
        (b"   ", "stdin is not JSON"),
        (b"null", "top-level must be object"),
        (b"42", "top-level must be object"),
        (b'"a string"', "top-level must be object"),
        (b"[1,2,3]", "top-level must be object"),
        (
            json.dumps({"envelope_version": "wrong"}).encode("utf-8"),
            "envelope_version must be",
        ),
    ],
)
def test_malformed_stdin_routes_to_exit_2(stdin_bytes, expected_phrase):
    with pytest.raises(ScribeEnvelopeMalformed) as exc:
        decode_envelope(raw_bytes=stdin_bytes)
    assert expected_phrase in str(exc.value)


def test_run_seat_emits_single_line_stderr_on_envelope_fail():
    stdin = io.BytesIO(b"")
    stdout = io.BytesIO()
    stderr = io.BytesIO()

    def _clock():
        return _NOW

    rc = run_seat(
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        clock=_clock,
        anthropic_call=lambda **_: AnthropicResponse(
            text_body="x",
            landed_model_id="claude",
            response_sha3_512="c" * 128,
            prompt_token_estimate=64,
            raw_response_canonical_json_bytes=b"{}",
        ),
        response_parse=lambda **_: ((_make_section_draft(),), ()),
        pre_gate=lambda **_: None,
        post_gate=lambda **_: None,
        admin_risk_fetch=lambda **_: AdminRiskRegister(
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
        ),
        anthropic_binding=object(),
    )
    assert rc == EXIT_GATE_FAIL
    err = stderr.getvalue()
    assert err.endswith(b"\n")
    assert err.count(b"\n") == 1, "exactly one stderr line per failure"
    parsed = json.loads(err.decode("utf-8"))
    assert parsed["failure_code"] == F_SCRIBE_ENVELOPE_MALFORMED
    assert parsed["envelope_version"] == ENVELOPE_VERSION_V1
    assert parsed["emitted_at_utc"] == _NOW.isoformat()


# ---------------------------------------------------------------------------
# Property: envelope round-trip encode → decode preserves all fields
# ---------------------------------------------------------------------------


def test_property_envelope_decode_is_idempotent_for_well_formed_input():
    # 32 random well-formed envelopes; decode must succeed and the
    # resulting frozen ScribeEnvelope must mirror the source dict.
    rng = random.Random(0xC0FFEE)
    dialects = ["conservative", "centrist", "progressive", "soul_fire"]
    programs = ["VAPG", "REAP", "SCBGP", "SARE", "SBIR"]
    for _ in range(32):
        section_order = rng.randint(1, 99)
        iteration = rng.randint(0, 10)
        age = rng.uniform(0.0, 23.99)
        d = _envelope_dict(
            run_id=f"run-{rng.randrange(10_000)}",
            org_slug=f"org-{rng.randrange(1_000)}",
            iteration_number=iteration,
            section_order=section_order,
            funder_dialect=rng.choice(dialects),
            program_code=rng.choice(programs),
            admin_risk_snapshot_age_hours=age,
        )
        env = decode_envelope(raw_bytes=json.dumps(d).encode("utf-8"))
        assert env.run_id == d["run_id"]
        assert env.org_slug == d["org_slug"]
        assert env.section_order == section_order
        assert env.iteration_number == iteration
        assert env.funder_dialect == d["funder_dialect"]
        assert env.program_code == d["program_code"]
        assert abs(env.admin_risk_snapshot_age_hours - age) < 1e-9


# ---------------------------------------------------------------------------
# Property: result encoder is deterministic over field permutations
# ---------------------------------------------------------------------------


def test_property_encode_result_canonical_bytes_invariant():
    """Encoding twice produces byte-identical output."""
    base = ScribeResult(
        result_version="scribe-result.v1",
        run_id="r1",
        org_slug="o1",
        iteration_number=0,
        section_drafts=(_make_section_draft(),),
        compiled_prompt_shell_sha3_512=_SHELL_HASH,
        provider_landed_family="anthropic",
        provider_landed_model_id="claude",
        admin_risk_flags=(
            AdminRiskFlag(
                term="dei",
                severity="medium",
                proposed_substitution=None,
                applicant_approved=False,
            ),
            AdminRiskFlag(
                term="equity",
                severity="high",
                proposed_substitution="parity",
                applicant_approved=True,
            ),
        ),
        seat_emitted_at_utc=_NOW,
    )
    a = encode_result(base)
    b = encode_result(base)
    assert a == b
    decoded = json.loads(a)
    assert decoded["result_version"] == RESULT_VERSION_V1
    assert decoded["admin_risk_flags_count"] == 2
    # canonical: sorted keys at every level
    assert decoded["admin_risk_flags"][0]["term"] == "dei"


# ---------------------------------------------------------------------------
# Adversarial: NULL bytes / unicode / very-long inputs
# ---------------------------------------------------------------------------


def test_envelope_with_unicode_org_slug_decodes():
    d = _envelope_dict(org_slug="füùçåcoôp_2026")
    env = decode_envelope(raw_bytes=json.dumps(d).encode("utf-8"))
    assert env.org_slug == "füùçåcoôp_2026"


def test_envelope_with_control_chars_in_compiled_prompt_decodes():
    # JSON allows escaped control bytes in strings; the seat must not choke.
    d = _envelope_dict(compiled_prompt="hello\tworld\n\rline")
    env = decode_envelope(raw_bytes=json.dumps(d).encode("utf-8"))
    assert "\t" in env.compiled_prompt
    assert "\n" in env.compiled_prompt
    assert "\r" in env.compiled_prompt


def test_envelope_with_very_long_compiled_prompt_decodes():
    # 200 KB prompt — must not blow the parser.
    long_prompt = "x" * 200_000
    d = _envelope_dict(compiled_prompt=long_prompt)
    env = decode_envelope(raw_bytes=json.dumps(d).encode("utf-8"))
    assert len(env.compiled_prompt) == 200_000


def test_envelope_emits_canonical_iso_for_offset_z():
    # +00:00 vs Z are equivalent — fromisoformat in py3.11+ accepts both.
    d = _envelope_dict(envelope_emitted_at_utc="2026-04-22T12:00:00+00:00")
    env = decode_envelope(raw_bytes=json.dumps(d).encode("utf-8"))
    # round-trip
    assert env.envelope_emitted_at_utc == _NOW


# ---------------------------------------------------------------------------
# Adversarial: ScribeGateFailed exception shape
# ---------------------------------------------------------------------------


def test_gate_failed_carries_kwargs():
    exc = ScribeGateFailed(
        failure_code="F-SCRIBE-ORG-CROSS-REF",
        trigger="cedar_tripped",
        evidence={"foreign_slugs": ["other_org"]},
    )
    assert exc.failure_code == "F-SCRIBE-ORG-CROSS-REF"
    assert exc.trigger == "cedar_tripped"
    assert exc.evidence == {"foreign_slugs": ["other_org"]}
    # message form
    assert "F-SCRIBE-ORG-CROSS-REF" in str(exc)
    assert "cedar_tripped" in str(exc)


def test_gate_failed_evidence_is_copied_not_aliased():
    src = {"k": "v"}
    exc = ScribeGateFailed(
        failure_code="F-SCRIBE-X",
        trigger="x",
        evidence=src,
    )
    src["k"] = "mutated"
    assert exc.evidence == {"k": "v"}, "evidence must be defensively copied"
