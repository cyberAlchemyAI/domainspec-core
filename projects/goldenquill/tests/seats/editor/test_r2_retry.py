"""tests/seats/editor/test_r2_retry.py — R2 §3.1 retry-with-clarification.

Spec card §3.1:
- On parse / shape failure: retry once with clarification suffix.
- Bounded N=2 (one retry).
- On second failure: original F-code propagates.
- Hard launcher failures (timeout / subprocess crash) are NOT retried.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

from pipeline.seats.editor import (
    EditorInput,
    EditorOutputShapeError,
    EditorSingleReplacementError,
    EditorSkillOutputMalformedJson,
    EditorSkillSubprocessFail,
    EditorSkillTimeout,
    F_EDITOR_OUTPUT_SHAPE,
    F_EDITOR_SINGLE_REPLACEMENT,
    F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON,
    F_EDITOR_SKILL_SUBPROCESS_FAIL,
    F_EDITOR_SKILL_TIMEOUT,
    SkillSubprocessResult,
    invoke_editor_adapter,
)
from pipeline.seats.editor.adapter import (
    _RETRY_WITH_CLARIFICATION_MAX_ATTEMPTS,
    _RETRYABLE_FAILURE_CODES,
    _build_clarification_suffix,
)


UTC = timezone.utc


def _clock():
    return datetime(2026, 4, 29, 12, 0, tzinfo=UTC)


VALID_JSON_TEMPLATE = json.dumps(
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


class _CountingLauncher:
    def __init__(self, stdouts: list[str]):
        self._stdouts = list(stdouts)
        self.calls: list[bytes] = []

    def __call__(
        self,
        *,
        skill_slug,
        stdin_payload,
        timeout_ms,
    ) -> SkillSubprocessResult:
        self.calls.append(stdin_payload)
        idx = min(len(self.calls) - 1, len(self._stdouts) - 1)
        return SkillSubprocessResult(stdout=self._stdouts[idx], exit_code=0)


class _RaisingLauncher:
    def __init__(self, exc: BaseException):
        self.exc = exc
        self.calls = 0

    def __call__(self, **_kwargs) -> SkillSubprocessResult:
        self.calls += 1
        raise self.exc


def _make_input(
    *,
    body_text: str = (
        "We grow specialty mushrooms across many beds inside the cooperative "
        "facility, processing them into dried products and value-added "
        "preparations for regional wholesale customers and direct retail "
        "buyers throughout the Mid-Atlantic."
    ),
) -> EditorInput:
    return EditorInput(
        section_drafts=(
            {"section_name": "1.a", "section_order": 1, "body_text": body_text},
        ),
        rfa_excerpt="rfa",
        dialect="centrist",
        session_id="s",
        org_slug="o",
    )


# ---------------------------------------------------------------------------
# Module-level constants pinned (V1 rebind-resistance)
# ---------------------------------------------------------------------------


class TestRetryConstants:
    def test_max_attempts_is_two(self):
        assert _RETRY_WITH_CLARIFICATION_MAX_ATTEMPTS == 2

    def test_retryable_codes_are_three(self):
        assert _RETRYABLE_FAILURE_CODES == frozenset(
            {
                F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON,
                F_EDITOR_OUTPUT_SHAPE,
                F_EDITOR_SINGLE_REPLACEMENT,
            }
        )

    def test_clarification_suffix_includes_failure_code(self):
        s = _build_clarification_suffix(
            first_failure_code=F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON,
            first_failure_message="JSON decode failed",
        )
        assert F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON in s
        assert "re-emit a single JSON object" in s

    def test_clarification_suffix_truncates_long_message(self):
        long_msg = "A" * 1000
        s = _build_clarification_suffix(
            first_failure_code="X", first_failure_message=long_msg
        )
        # message portion limited to 256 chars + "..."
        assert "AAA..." in s
        # never larger than reasonable bound
        assert len(s) < 800

    def test_clarification_suffix_handles_multiline_message(self):
        s = _build_clarification_suffix(
            first_failure_code="X",
            first_failure_message="line 1\nline 2 with secret stack info",
        )
        assert "line 2" not in s  # only first line used


# ---------------------------------------------------------------------------
# Retry path — first attempt fails, second succeeds
# ---------------------------------------------------------------------------


class TestRetryRecovery:
    def test_malformed_then_valid(self):
        launcher = _CountingLauncher(["not json", VALID_JSON_TEMPLATE])
        out = invoke_editor_adapter(
            _make_input(), skill_launcher=launcher, clock=_clock
        )
        assert len(out.flagged_terms) == 1
        assert len(launcher.calls) == 2
        # First call has no clarification.
        first = json.loads(launcher.calls[0].decode("utf-8"))
        assert "clarification" not in first
        # Second call carries clarification + retry_attempt=2.
        second = json.loads(launcher.calls[1].decode("utf-8"))
        assert "clarification" in second
        assert second["retry_attempt"] == 2
        assert F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON in second["clarification"]

    def test_shape_violation_then_valid(self):
        bad = json.dumps(
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
                        "original": "x",
                        "issue": "y",
                        "issue_type": "climate_nostalgia",
                        "severity": "low",
                        "options": [
                            {"label": "A", "text": "a", "note": ""},
                            {"label": "B", "text": "b", "note": ""},
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
        launcher = _CountingLauncher([bad, VALID_JSON_TEMPLATE])
        out = invoke_editor_adapter(
            _make_input(), skill_launcher=launcher, clock=_clock
        )
        assert len(launcher.calls) == 2
        assert len(out.flagged_terms) == 1
        second = json.loads(launcher.calls[1].decode("utf-8"))
        assert F_EDITOR_OUTPUT_SHAPE in second["clarification"]

    def test_single_replacement_then_valid(self):
        # First call returns a suggestion with 1 option (validator trips)
        bad = json.dumps(
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
                        "original": "x",
                        "issue": "y",
                        "issue_type": "jargon",
                        "severity": "low",
                        "options": [{"label": "A", "text": "a", "note": ""}],
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
        launcher = _CountingLauncher([bad, VALID_JSON_TEMPLATE])
        out = invoke_editor_adapter(
            _make_input(), skill_launcher=launcher, clock=_clock
        )
        assert len(launcher.calls) == 2
        second = json.loads(launcher.calls[1].decode("utf-8"))
        assert F_EDITOR_SINGLE_REPLACEMENT in second["clarification"]
        assert len(out.flagged_terms) == 1

    def test_disable_retry_raises_immediately(self):
        launcher = _CountingLauncher(["not json", VALID_JSON_TEMPLATE])
        with pytest.raises(EditorSkillOutputMalformedJson):
            invoke_editor_adapter(
                _make_input(),
                skill_launcher=launcher,
                clock=_clock,
                enable_retry_with_clarification=False,
            )
        assert len(launcher.calls) == 1


# ---------------------------------------------------------------------------
# Retry exhausted — second attempt also fails
# ---------------------------------------------------------------------------


class TestRetryExhausted:
    def test_two_malformed_attempts_propagate(self):
        launcher = _CountingLauncher(["not json", "still not json"])
        with pytest.raises(EditorSkillOutputMalformedJson):
            invoke_editor_adapter(
                _make_input(), skill_launcher=launcher, clock=_clock
            )
        assert len(launcher.calls) == 2

    def test_two_shape_attempts_propagate(self):
        bad = json.dumps(
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
                        "original": "x",
                        "issue": "y",
                        "issue_type": "unknown",
                        "severity": "low",
                        "options": [
                            {"label": "A", "text": "a", "note": ""},
                            {"label": "B", "text": "b", "note": ""},
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
        launcher = _CountingLauncher([bad, bad])
        with pytest.raises(EditorOutputShapeError):
            invoke_editor_adapter(
                _make_input(), skill_launcher=launcher, clock=_clock
            )
        assert len(launcher.calls) == 2


# ---------------------------------------------------------------------------
# Hard launcher failures — NOT retried
# ---------------------------------------------------------------------------


class TestHardLauncherFailuresNotRetried:
    def test_timeout_not_retried(self):
        launcher = _RaisingLauncher(TimeoutError("timed out"))
        with pytest.raises(EditorSkillTimeout) as exc_info:
            invoke_editor_adapter(
                _make_input(), skill_launcher=launcher, clock=_clock
            )
        assert exc_info.value.failure_code == F_EDITOR_SKILL_TIMEOUT
        assert launcher.calls == 1

    def test_subprocess_fail_not_retried(self):
        launcher = _RaisingLauncher(RuntimeError("boom"))
        with pytest.raises(EditorSkillSubprocessFail) as exc_info:
            invoke_editor_adapter(
                _make_input(), skill_launcher=launcher, clock=_clock
            )
        assert exc_info.value.failure_code == F_EDITOR_SKILL_SUBPROCESS_FAIL
        assert launcher.calls == 1

    def test_timeout_on_retry_propagates(self):
        # First call fails parse → triggers retry; retry raises Timeout.
        class _MixedLauncher:
            def __init__(self):
                self.calls = 0

            def __call__(self, **_kwargs):
                self.calls += 1
                if self.calls == 1:
                    return SkillSubprocessResult(stdout="not json", exit_code=0)
                raise TimeoutError("retry timed out")

        launcher = _MixedLauncher()
        with pytest.raises(EditorSkillTimeout):
            invoke_editor_adapter(
                _make_input(), skill_launcher=launcher, clock=_clock
            )
        assert launcher.calls == 2


# ---------------------------------------------------------------------------
# Clarification-payload integrity
# ---------------------------------------------------------------------------


class TestClarificationPayload:
    def test_original_envelope_preserved(self):
        launcher = _CountingLauncher(["not json", VALID_JSON_TEMPLATE])
        invoke_editor_adapter(
            _make_input(), skill_launcher=launcher, clock=_clock
        )
        first = json.loads(launcher.calls[0].decode("utf-8"))
        second = json.loads(launcher.calls[1].decode("utf-8"))
        for key in (
            "draft_markdown",
            "rfa_excerpt",
            "dialect",
            "session_id",
            "org_slug",
            "invocation_at_utc",
        ):
            assert second[key] == first[key], f"{key} changed across retry"

    def test_clarification_payload_canonical_json(self):
        launcher = _CountingLauncher(["not json", VALID_JSON_TEMPLATE])
        invoke_editor_adapter(
            _make_input(), skill_launcher=launcher, clock=_clock
        )
        # Re-encoding the parsed object reproduces the bytes exactly.
        second_bytes = launcher.calls[1]
        second = json.loads(second_bytes.decode("utf-8"))
        re_encoded = json.dumps(
            second, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        assert re_encoded == second_bytes
