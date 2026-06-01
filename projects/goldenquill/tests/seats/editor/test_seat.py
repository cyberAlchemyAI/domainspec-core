"""tests/seats/editor/test_seat.py — R1 subprocess entry coverage.

Spec card §7 — seat.py exercise:
- decode_envelope (happy + malformed)
- encode_result canonical bytes
- run_seat full lifecycle (PRE/adapter/POST → exit 0)
- run_seat fail-closed routes (envelope malformed, PRE/POST gates, adapter)
- default PRE-gate cross-org check
"""

from __future__ import annotations

import io
import json
from datetime import datetime, timezone

import pytest

from pipeline.seats.editor import (
    EXIT_GATE_FAIL,
    EXIT_INTERNAL_ERROR,
    EXIT_OK,
    EditorEnvelope,
    EditorEnvelopeMalformed,
    EditorGateFailed,
    EditorOutput,
    EditorSeatResult,
    F_EDITOR_ENVELOPE_MALFORMED,
    F_EDITOR_ORG_CROSS_REF,
    SkillSubprocessResult,
    decode_envelope,
    default_cross_org_pre_gate,
    default_noop_post_gate,
    encode_result,
    run_seat,
)


UTC = timezone.utc


def _clock():
    return datetime(2026, 4, 29, 12, 0, tzinfo=UTC)


def _make_envelope_dict() -> dict:
    return {
        "envelope_version": "editor-envelope.v1",
        "run_id": "run-1",
        "org_slug": "mycosymbiotics",
        "iteration_number": 0,
        "section_drafts": [
            {
                "section_name": "1.a",
                "section_order": 1,
                "body_text": "We grow mushrooms across many beds at the cooperative facility.",
            },
        ],
        "rfa_excerpt": "rfa",
        "dialect": "centrist",
        "session_id": "sess-1",
        "envelope_emitted_at_utc": "2026-04-29T12:00:00+00:00",
    }


_VALID_SKILL_STDOUT = json.dumps(
    {
        "readability": {
            "score_10": 7,
            "grade_level_estimate": "g",
            "verdict": "ok",
            "key_message": "k",
            "reviewer_fatigue_sections": [],
        },
        "strengths": [],
        "suggestions": [
            {
                "section": "1.a",
                "original": "vague",
                "issue": "vague",
                "issue_type": "jargon",
                "severity": "low",
                "options": [
                    {"label": "A", "text": "specific1", "note": ""},
                    {"label": "B", "text": "specific2", "note": ""},
                ],
                "rubric_connection": "",
            }
        ],
        "gaps": [],
        "quick_wins": [],
        "terms_to_verify": [],
        "taxonomy_check": {
            "goals_identified": [],
            "outputs_identified": [],
            "outcomes_identified": [],
            "objectives_identified": [],
            "miscategorizations": [],
        },
    }
)


class _Launcher:
    def __init__(self, stdout: str = _VALID_SKILL_STDOUT):
        self.stdout = stdout
        self.calls = 0

    def __call__(self, **_kwargs) -> SkillSubprocessResult:
        self.calls += 1
        return SkillSubprocessResult(stdout=self.stdout, exit_code=0)


# ---------------------------------------------------------------------------
# decode_envelope
# ---------------------------------------------------------------------------


class TestDecodeEnvelope:
    def test_happy_path(self):
        env_bytes = json.dumps(_make_envelope_dict()).encode("utf-8")
        env = decode_envelope(raw_bytes=env_bytes)
        assert isinstance(env, EditorEnvelope)
        assert env.envelope_version == "editor-envelope.v1"
        assert env.run_id == "run-1"

    def test_empty_stdin(self):
        with pytest.raises(EditorEnvelopeMalformed, match="empty"):
            decode_envelope(raw_bytes=b"")

    def test_non_utf8(self):
        with pytest.raises(EditorEnvelopeMalformed, match="UTF-8"):
            decode_envelope(raw_bytes=b"\xff\xfe\x00\x00")

    def test_not_json(self):
        with pytest.raises(EditorEnvelopeMalformed, match="not JSON"):
            decode_envelope(raw_bytes=b"not json")

    def test_top_level_array(self):
        with pytest.raises(EditorEnvelopeMalformed, match="must be"):
            decode_envelope(raw_bytes=b"[1,2,3]")

    def test_wrong_version(self):
        d = _make_envelope_dict()
        d["envelope_version"] = "editor-envelope.v0"
        with pytest.raises(EditorEnvelopeMalformed, match="envelope_version"):
            decode_envelope(raw_bytes=json.dumps(d).encode("utf-8"))

    def test_missing_keys(self):
        d = _make_envelope_dict()
        d.pop("run_id")
        with pytest.raises(EditorEnvelopeMalformed, match="missing keys"):
            decode_envelope(raw_bytes=json.dumps(d).encode("utf-8"))

    def test_non_string_emit_at(self):
        d = _make_envelope_dict()
        d["envelope_emitted_at_utc"] = 12345
        with pytest.raises(EditorEnvelopeMalformed, match="ISO-8601"):
            decode_envelope(raw_bytes=json.dumps(d).encode("utf-8"))

    def test_bad_iso8601(self):
        d = _make_envelope_dict()
        d["envelope_emitted_at_utc"] = "not a date"
        with pytest.raises(EditorEnvelopeMalformed, match="ISO-8601"):
            decode_envelope(raw_bytes=json.dumps(d).encode("utf-8"))

    def test_section_drafts_not_list(self):
        d = _make_envelope_dict()
        d["section_drafts"] = "not a list"
        with pytest.raises(EditorEnvelopeMalformed, match="section_drafts"):
            decode_envelope(raw_bytes=json.dumps(d).encode("utf-8"))

    def test_section_drafts_entry_not_dict(self):
        d = _make_envelope_dict()
        d["section_drafts"] = ["not-a-dict"]
        with pytest.raises(EditorEnvelopeMalformed, match="section_drafts"):
            decode_envelope(raw_bytes=json.dumps(d).encode("utf-8"))


# ---------------------------------------------------------------------------
# EditorEnvelope.__post_init__
# ---------------------------------------------------------------------------


class TestEditorEnvelope:
    def _envelope_kwargs(self) -> dict:
        return dict(
            envelope_version="editor-envelope.v1",
            run_id="run-1",
            org_slug="o",
            iteration_number=0,
            section_drafts=(
                {"section_name": "1.a", "section_order": 1, "body_text": "x"},
            ),
            rfa_excerpt="",
            dialect="centrist",
            session_id="s",
            envelope_emitted_at_utc=datetime(2026, 4, 29, tzinfo=UTC),
        )

    def test_rejects_negative_iteration(self):
        kw = self._envelope_kwargs()
        kw["iteration_number"] = -1
        with pytest.raises(EditorEnvelopeMalformed, match="iteration_number"):
            EditorEnvelope(**kw)

    def test_rejects_naive_datetime(self):
        kw = self._envelope_kwargs()
        kw["envelope_emitted_at_utc"] = datetime(2026, 4, 29)
        with pytest.raises(EditorEnvelopeMalformed, match="timezone"):
            EditorEnvelope(**kw)

    def test_rejects_invalid_dialect(self):
        kw = self._envelope_kwargs()
        kw["dialect"] = "hard_left"
        with pytest.raises(EditorEnvelopeMalformed, match="dialect"):
            EditorEnvelope(**kw)

    def test_rejects_empty_section_drafts(self):
        kw = self._envelope_kwargs()
        kw["section_drafts"] = ()
        with pytest.raises(EditorEnvelopeMalformed, match="section_drafts"):
            EditorEnvelope(**kw)

    def test_rejects_empty_session_id(self):
        kw = self._envelope_kwargs()
        kw["session_id"] = ""
        with pytest.raises(EditorEnvelopeMalformed, match="session_id"):
            EditorEnvelope(**kw)


# ---------------------------------------------------------------------------
# EditorSeatResult.__post_init__
# ---------------------------------------------------------------------------


class TestEditorSeatResult:
    def _ok_kwargs(self, output: EditorOutput) -> dict:
        return dict(
            result_version="editor-result.v1",
            run_id="r",
            org_slug="o",
            iteration_number=0,
            editor_output=output,
            seat_emitted_at_utc=datetime(2026, 4, 29, tzinfo=UTC),
        )

    def test_rejects_wrong_version(self, ok_output: EditorOutput):
        kw = self._ok_kwargs(ok_output)
        kw["result_version"] = "editor-result.v0"
        with pytest.raises(ValueError, match="result_version"):
            EditorSeatResult(**kw)

    def test_rejects_negative_iteration(self, ok_output: EditorOutput):
        kw = self._ok_kwargs(ok_output)
        kw["iteration_number"] = -1
        with pytest.raises(ValueError, match="iteration_number"):
            EditorSeatResult(**kw)

    def test_rejects_naive_datetime(self, ok_output: EditorOutput):
        kw = self._ok_kwargs(ok_output)
        kw["seat_emitted_at_utc"] = datetime(2026, 4, 29)
        with pytest.raises(ValueError, match="timezone"):
            EditorSeatResult(**kw)


@pytest.fixture
def ok_output() -> EditorOutput:
    """Build a minimal happy-path EditorOutput for codec tests."""
    from pipeline.seats.editor import (
        FlaggedTerm,
        ReadabilityFeedback,
        ReplacementOption,
        TaxonomyCheck,
        ToneFeedback,
    )
    return EditorOutput(
        flagged_terms=(
            FlaggedTerm(
                section_ref="1.a",
                issue_type="jargon",
                severity="low",
                excerpt="x",
                why_it_hurts="y",
                replacement_options=(
                    ReplacementOption(label="A", text="a", note=""),
                    ReplacementOption(label="B", text="b", note=""),
                ),
                rubric_connection="",
            ),
        ),
        taxonomy_check=TaxonomyCheck(
            goals_identified=(),
            outputs_identified=(),
            outcomes_identified=(),
            objectives_identified=(),
            miscategorizations=(),
        ),
        tone_feedback=ToneFeedback(
            overall_readability=ReadabilityFeedback(
                score_10=7, grade_level_estimate="g", verdict="ok"
            ),
            key_message="k",
            reviewer_fatigue_sections=(),
        ),
        quick_wins=(),
        terms_to_verify=(),
        gaps=(),
    )


# ---------------------------------------------------------------------------
# encode_result
# ---------------------------------------------------------------------------


class TestEncodeResult:
    def test_canonical_bytes(self, ok_output: EditorOutput):
        result = EditorSeatResult(
            result_version="editor-result.v1",
            run_id="r",
            org_slug="o",
            iteration_number=0,
            editor_output=ok_output,
            seat_emitted_at_utc=datetime(2026, 4, 29, tzinfo=UTC),
        )
        encoded = encode_result(result)
        assert encoded.endswith(b"\n")
        decoded = json.loads(encoded.decode("utf-8"))
        assert decoded["result_version"] == "editor-result.v1"
        assert "editor_output" in decoded


# ---------------------------------------------------------------------------
# run_seat lifecycle
# ---------------------------------------------------------------------------


class TestRunSeat:
    def test_happy_path_exit_zero(self):
        env_bytes = json.dumps(_make_envelope_dict()).encode("utf-8")
        stdin = io.BytesIO(env_bytes)
        stdout = io.BytesIO()
        stderr = io.BytesIO()
        rc = run_seat(
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            clock=_clock,
            skill_launcher=_Launcher(),
            pre_gate=default_cross_org_pre_gate,
            post_gate=default_noop_post_gate,
            ambient_org_slug="mycosymbiotics",
        )
        assert rc == EXIT_OK
        out = json.loads(stdout.getvalue().decode("utf-8"))
        assert out["result_version"] == "editor-result.v1"
        assert out["run_id"] == "run-1"

    def test_envelope_malformed_exit_two(self):
        stdin = io.BytesIO(b"not-json")
        stdout = io.BytesIO()
        stderr = io.BytesIO()
        rc = run_seat(
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            clock=_clock,
            skill_launcher=_Launcher(),
            pre_gate=default_cross_org_pre_gate,
            post_gate=default_noop_post_gate,
            ambient_org_slug="o",
        )
        assert rc == EXIT_GATE_FAIL
        err = json.loads(stderr.getvalue().decode("utf-8"))
        assert err["failure_code"] == F_EDITOR_ENVELOPE_MALFORMED

    def test_pre_gate_cross_org_mismatch_exit_two(self):
        env_bytes = json.dumps(_make_envelope_dict()).encode("utf-8")
        stdin = io.BytesIO(env_bytes)
        stdout = io.BytesIO()
        stderr = io.BytesIO()
        rc = run_seat(
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            clock=_clock,
            skill_launcher=_Launcher(),
            pre_gate=default_cross_org_pre_gate,
            post_gate=default_noop_post_gate,
            ambient_org_slug="other-org",
        )
        assert rc == EXIT_GATE_FAIL
        err = json.loads(stderr.getvalue().decode("utf-8"))
        assert err["failure_code"] == F_EDITOR_ORG_CROSS_REF

    def test_pre_gate_unhandled_raise_exit_one(self):
        env_bytes = json.dumps(_make_envelope_dict()).encode("utf-8")

        def _broken_pre_gate(*, envelope, ambient_org_slug):
            raise RuntimeError("bug")

        stdin = io.BytesIO(env_bytes)
        stdout = io.BytesIO()
        stderr = io.BytesIO()
        rc = run_seat(
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            clock=_clock,
            skill_launcher=_Launcher(),
            pre_gate=_broken_pre_gate,
            post_gate=default_noop_post_gate,
            ambient_org_slug="mycosymbiotics",
        )
        assert rc == EXIT_INTERNAL_ERROR
        # Sanitized stderr — class name only.
        assert b"RuntimeError" in stderr.getvalue()
        assert b"bug" not in stderr.getvalue()  # message scrubbed

    def test_skill_timeout_exit_two(self):
        class _TO:
            def __call__(self, **_kwargs):
                raise TimeoutError("timed out")

        env_bytes = json.dumps(_make_envelope_dict()).encode("utf-8")
        stdin = io.BytesIO(env_bytes)
        stdout = io.BytesIO()
        stderr = io.BytesIO()
        rc = run_seat(
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            clock=_clock,
            skill_launcher=_TO(),
            pre_gate=default_cross_org_pre_gate,
            post_gate=default_noop_post_gate,
            ambient_org_slug="mycosymbiotics",
        )
        assert rc == EXIT_GATE_FAIL
        err = json.loads(stderr.getvalue().decode("utf-8"))
        assert err["failure_code"] == "F-EDITOR-SKILL-TIMEOUT"

    def test_skill_subprocess_fail_exit_two(self):
        class _SF:
            def __call__(self, **_kwargs):
                raise RuntimeError("crash")

        env_bytes = json.dumps(_make_envelope_dict()).encode("utf-8")
        stdin = io.BytesIO(env_bytes)
        stdout = io.BytesIO()
        stderr = io.BytesIO()
        rc = run_seat(
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            clock=_clock,
            skill_launcher=_SF(),
            pre_gate=default_cross_org_pre_gate,
            post_gate=default_noop_post_gate,
            ambient_org_slug="mycosymbiotics",
        )
        assert rc == EXIT_GATE_FAIL
        err = json.loads(stderr.getvalue().decode("utf-8"))
        assert err["failure_code"] == "F-EDITOR-SKILL-SUBPROCESS-FAIL"

    def test_skill_malformed_json_exit_two(self):
        # First call returns non-JSON; retry also returns non-JSON.
        class _BadJson:
            def __init__(self):
                self.calls = 0

            def __call__(self, **_kwargs):
                self.calls += 1
                return SkillSubprocessResult(stdout="not json", exit_code=0)

        env_bytes = json.dumps(_make_envelope_dict()).encode("utf-8")
        stdin = io.BytesIO(env_bytes)
        stdout = io.BytesIO()
        stderr = io.BytesIO()
        rc = run_seat(
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            clock=_clock,
            skill_launcher=_BadJson(),
            pre_gate=default_cross_org_pre_gate,
            post_gate=default_noop_post_gate,
            ambient_org_slug="mycosymbiotics",
        )
        assert rc == EXIT_GATE_FAIL
        err = json.loads(stderr.getvalue().decode("utf-8"))
        assert err["failure_code"] == "F-EDITOR-SKILL-OUTPUT-MALFORMED-JSON"

    def test_post_gate_failed_exit_two(self):
        def _failing_post_gate(*, envelope, editor_output):
            raise EditorGateFailed(
                failure_code="F-CUSTOM",
                trigger="custom",
                evidence={"info": "x"},
            )

        env_bytes = json.dumps(_make_envelope_dict()).encode("utf-8")
        stdin = io.BytesIO(env_bytes)
        stdout = io.BytesIO()
        stderr = io.BytesIO()
        rc = run_seat(
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            clock=_clock,
            skill_launcher=_Launcher(),
            pre_gate=default_cross_org_pre_gate,
            post_gate=_failing_post_gate,
            ambient_org_slug="mycosymbiotics",
        )
        assert rc == EXIT_GATE_FAIL
        err = json.loads(stderr.getvalue().decode("utf-8"))
        assert err["failure_code"] == "F-CUSTOM"

    def test_post_gate_unhandled_raise_exit_one(self):
        def _broken_post_gate(*, envelope, editor_output):
            raise RuntimeError("bug")

        env_bytes = json.dumps(_make_envelope_dict()).encode("utf-8")
        stdin = io.BytesIO(env_bytes)
        stdout = io.BytesIO()
        stderr = io.BytesIO()
        rc = run_seat(
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            clock=_clock,
            skill_launcher=_Launcher(),
            pre_gate=default_cross_org_pre_gate,
            post_gate=_broken_post_gate,
            ambient_org_slug="mycosymbiotics",
        )
        assert rc == EXIT_INTERNAL_ERROR

    def test_envelope_input_construction_failure_exit_two(self):
        # Send an envelope with empty section_drafts via decode_envelope's
        # gap (decode admits if list is non-empty; we route through normal
        # path then EditorInput would normally accept anything decoded;
        # rare path. Use empty rfa_excerpt that's tolerated, and nudge by
        # patching after decode.) — covered indirectly elsewhere.
        # Instead: trigger via env with empty section_drafts (caught by
        # EditorEnvelope.__post_init__ → envelope_decode_failed).
        d = _make_envelope_dict()
        d["section_drafts"] = []
        env_bytes = json.dumps(d).encode("utf-8")
        stdin = io.BytesIO(env_bytes)
        stdout = io.BytesIO()
        stderr = io.BytesIO()
        rc = run_seat(
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            clock=_clock,
            skill_launcher=_Launcher(),
            pre_gate=default_cross_org_pre_gate,
            post_gate=default_noop_post_gate,
            ambient_org_slug="mycosymbiotics",
        )
        assert rc == EXIT_GATE_FAIL


# ---------------------------------------------------------------------------
# default_cross_org_pre_gate
# ---------------------------------------------------------------------------


class TestDefaultPreGate:
    def test_match_passes(self):
        env = decode_envelope(
            raw_bytes=json.dumps(_make_envelope_dict()).encode("utf-8")
        )
        # No raise.
        default_cross_org_pre_gate(envelope=env, ambient_org_slug="mycosymbiotics")

    def test_mismatch_raises(self):
        env = decode_envelope(
            raw_bytes=json.dumps(_make_envelope_dict()).encode("utf-8")
        )
        with pytest.raises(EditorGateFailed) as exc_info:
            default_cross_org_pre_gate(envelope=env, ambient_org_slug="other")
        assert exc_info.value.failure_code == F_EDITOR_ORG_CROSS_REF

    def test_default_post_gate_returns_none(self, ok_output: EditorOutput):
        env = decode_envelope(
            raw_bytes=json.dumps(_make_envelope_dict()).encode("utf-8")
        )
        assert default_noop_post_gate(envelope=env, editor_output=ok_output) is None
