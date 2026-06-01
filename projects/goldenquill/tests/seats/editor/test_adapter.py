"""tests/seats/editor/test_adapter.py — R1 adapter happy/fail paths.

Spec card §7 coverage:
- adapter happy path on canned corpus fixtures
- parse_skill_output on fenced / prose-wrapped JSON
- validator F-EDITOR-* code matrix (single-replacement, rewrite-threshold,
  output-shape)
- launcher exception mapping (timeout / generic subprocess fail)
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pytest

from pipeline.seats.editor import (
    EditorInput,
    EditorOutput,
    EditorOutputShapeError,
    EditorRewroteInsteadOfFlaggedError,
    EditorSingleReplacementError,
    EditorSkillOutputMalformedJson,
    EditorSkillSubprocessFail,
    EditorSkillTimeout,
    F_EDITOR_OUTPUT_SHAPE,
    F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED,
    F_EDITOR_SINGLE_REPLACEMENT,
    F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON,
    F_EDITOR_SKILL_SUBPROCESS_FAIL,
    F_EDITOR_SKILL_TIMEOUT,
    SkillLauncher,
    SkillSubprocessResult,
    invoke_editor_adapter,
    parse_skill_output,
    validate_editor_output_shape,
)


UTC = timezone.utc
CORPUS_ROOT = Path(__file__).resolve().parent.parent.parent / "corpus" / "editor" / "v1"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _fixed_clock(value: datetime = datetime(2026, 4, 29, 12, 0, tzinfo=UTC)):
    def _clock() -> datetime:
        return value
    return _clock


class _FakeLauncher:
    """E-017 injected SkillLauncher fake — returns canned stdout."""

    def __init__(self, *, stdouts: list[str], exit_codes: list[int] | None = None):
        self._stdouts = list(stdouts)
        self._exit_codes = list(exit_codes) if exit_codes else [0] * len(stdouts)
        self.calls: list[bytes] = []

    def __call__(
        self,
        *,
        skill_slug,
        stdin_payload,
        timeout_ms,
    ) -> SkillSubprocessResult:
        assert skill_slug == "editor"
        assert timeout_ms == 180_000
        self.calls.append(stdin_payload)
        idx = min(len(self.calls) - 1, len(self._stdouts) - 1)
        return SkillSubprocessResult(
            stdout=self._stdouts[idx], exit_code=self._exit_codes[idx]
        )


class _RaisingLauncher:
    def __init__(self, exc: BaseException):
        self._exc = exc

    def __call__(self, **_kwargs) -> SkillSubprocessResult:
        raise self._exc


class _MisbehavingLauncher:
    def __call__(self, **_kwargs):
        return "not-a-result-object"  # wrong type


def _make_input(*, body_text: str = "We grow mushrooms across the cooperative.") -> EditorInput:
    return EditorInput(
        section_drafts=(
            {
                "section_name": "1.a",
                "section_order": 1,
                "body_text": body_text,
            },
        ),
        rfa_excerpt="rfa",
        dialect="centrist",
        session_id="sess-1",
        org_slug="mycosymbiotics",
    )


def _load_fixture(rel_path: str) -> dict:
    return json.loads((CORPUS_ROOT / rel_path).read_text())


# ---------------------------------------------------------------------------
# parse_skill_output (strip fences / extract JSON)
# ---------------------------------------------------------------------------


class TestParseSkillOutput:
    def test_plain_json(self):
        obj = parse_skill_output('{"a": 1}')
        assert obj == {"a": 1}

    def test_fenced_json(self):
        text = "```json\n{\"a\":1}\n```"
        obj = parse_skill_output(text)
        assert obj == {"a": 1}

    def test_prose_wrapped_json(self):
        text = 'Here is the result:\n{"a": 2}\nThanks.'
        obj = parse_skill_output(text)
        assert obj == {"a": 2}

    def test_empty_raises(self):
        with pytest.raises(EditorSkillOutputMalformedJson, match="empty"):
            parse_skill_output("")

    def test_no_object_raises(self):
        with pytest.raises(EditorSkillOutputMalformedJson, match="no JSON object"):
            parse_skill_output("This is not JSON.")

    def test_array_without_brace_raises_no_object(self):
        # `[1,2,3]` contains no `{` → "no JSON object found" branch.
        with pytest.raises(EditorSkillOutputMalformedJson, match="no JSON object"):
            parse_skill_output("[1, 2, 3]")

    def test_decode_error_raises(self):
        with pytest.raises(EditorSkillOutputMalformedJson, match="JSON decode"):
            parse_skill_output("{ this is broken")

    def test_fence_with_no_newline_after_open(self):
        text = "```{\"a\":1}```"
        obj = parse_skill_output(text)
        assert obj == {"a": 1}


# ---------------------------------------------------------------------------
# Validator — F-EDITOR-* code matrix
# ---------------------------------------------------------------------------


def _build_passable_output_from_fixture(fixture_name: str) -> tuple[EditorOutput, tuple]:
    fix = _load_fixture(f"pass/{fixture_name}.json")
    inp = EditorInput(
        section_drafts=tuple(
            tuple({k: v for k, v in sd.items()} for sd in (sd_dict,))[0]
            for sd_dict in fix["input_section_drafts"]
        ),
        rfa_excerpt=fix["input_rfa_excerpt"],
        dialect=fix["input_dialect"],
        session_id="sess",
        org_slug="org",
    )
    launcher = _FakeLauncher(stdouts=[fix["skill_stdout"]])
    out = invoke_editor_adapter(
        inp, skill_launcher=launcher, clock=_fixed_clock()
    )
    return out, inp.section_drafts


class TestValidator:
    def test_passes_on_vapg_corpus(self):
        out, src = _build_passable_output_from_fixture("vapg_clean_draft")
        validate_editor_output_shape(out, source_section_drafts=src)

    def test_passes_on_reap_corpus(self):
        out, src = _build_passable_output_from_fixture("reap_clean_draft")
        validate_editor_output_shape(out, source_section_drafts=src)

    def test_rejects_non_editor_output_input(self):
        with pytest.raises(EditorOutputShapeError, match="output must be"):
            validate_editor_output_shape(
                "not-an-output",  # type: ignore[arg-type]
                source_section_drafts=(),
            )


# ---------------------------------------------------------------------------
# invoke_editor_adapter — happy paths
# ---------------------------------------------------------------------------


class TestAdapterHappyPath:
    def test_vapg_corpus_round_trip(self):
        fix = _load_fixture("pass/vapg_clean_draft.json")
        inp = EditorInput(
            section_drafts=tuple(fix["input_section_drafts"]),
            rfa_excerpt=fix["input_rfa_excerpt"],
            dialect=fix["input_dialect"],
            session_id="s",
            org_slug="o",
        )
        launcher = _FakeLauncher(stdouts=[fix["skill_stdout"]])
        out = invoke_editor_adapter(
            inp, skill_launcher=launcher, clock=_fixed_clock()
        )
        assert isinstance(out, EditorOutput)
        assert len(out.flagged_terms) == 1
        assert 0 <= out.tone_feedback.overall_readability.score_10 <= 10

    def test_reap_corpus_round_trip(self):
        fix = _load_fixture("pass/reap_clean_draft.json")
        inp = EditorInput(
            section_drafts=tuple(fix["input_section_drafts"]),
            rfa_excerpt=fix["input_rfa_excerpt"],
            dialect=fix["input_dialect"],
            session_id="s",
            org_slug="o",
        )
        launcher = _FakeLauncher(stdouts=[fix["skill_stdout"]])
        out = invoke_editor_adapter(
            inp, skill_launcher=launcher, clock=_fixed_clock()
        )
        assert len(out.flagged_terms) == 2
        assert any(
            ft.issue_type == "goal_output_confusion" for ft in out.flagged_terms
        )

    def test_idempotent_under_fixed_clock(self):
        fix = _load_fixture("pass/vapg_clean_draft.json")
        inp = EditorInput(
            section_drafts=tuple(fix["input_section_drafts"]),
            rfa_excerpt=fix["input_rfa_excerpt"],
            dialect=fix["input_dialect"],
            session_id="s",
            org_slug="o",
        )
        launcher_a = _FakeLauncher(stdouts=[fix["skill_stdout"]])
        out_a = invoke_editor_adapter(
            inp, skill_launcher=launcher_a, clock=_fixed_clock()
        )
        launcher_b = _FakeLauncher(stdouts=[fix["skill_stdout"]])
        out_b = invoke_editor_adapter(
            inp, skill_launcher=launcher_b, clock=_fixed_clock()
        )
        assert out_a == out_b
        # Stdin payload bytes are also identical under fixed clock.
        assert launcher_a.calls == launcher_b.calls

    def test_stdin_payload_is_canonical_json(self):
        fix = _load_fixture("pass/vapg_clean_draft.json")
        inp = EditorInput(
            section_drafts=tuple(fix["input_section_drafts"]),
            rfa_excerpt=fix["input_rfa_excerpt"],
            dialect=fix["input_dialect"],
            session_id="s",
            org_slug="o",
        )
        launcher = _FakeLauncher(stdouts=[fix["skill_stdout"]])
        invoke_editor_adapter(inp, skill_launcher=launcher, clock=_fixed_clock())
        payload = json.loads(launcher.calls[0].decode("utf-8"))
        assert set(payload.keys()) >= {
            "draft_markdown",
            "rfa_excerpt",
            "dialect",
            "session_id",
            "org_slug",
            "invocation_at_utc",
        }
        # Sort-key invariant: re-encoding the parsed dict matches.
        canonical = json.dumps(
            payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        assert canonical.encode("utf-8") == launcher.calls[0]

    def test_rfa_excerpt_truncated_at_4000_chars(self):
        long_rfa = "x" * 5000
        inp = EditorInput(
            section_drafts=(
                {
                    "section_name": "s",
                    "section_order": 1,
                    "body_text": "body",
                },
            ),
            rfa_excerpt=long_rfa,
            dialect="centrist",
            session_id="s",
            org_slug="o",
        )
        captured_rfa: list[str] = []

        def _capture_launcher(**kwargs):
            payload = json.loads(kwargs["stdin_payload"].decode("utf-8"))
            captured_rfa.append(payload["rfa_excerpt"])
            return SkillSubprocessResult(
                stdout='{"readability":{"score_10":7,"grade_level_estimate":"g","verdict":"ok","key_message":"ok","reviewer_fatigue_sections":[]},"strengths":[],"suggestions":[],"gaps":[],"quick_wins":[],"terms_to_verify":[],"taxonomy_check":{"goals_identified":[],"outputs_identified":[],"outcomes_identified":[],"objectives_identified":[],"miscategorizations":[]}}',
                exit_code=0,
            )

        invoke_editor_adapter(inp, skill_launcher=_capture_launcher, clock=_fixed_clock())
        assert len(captured_rfa[0]) == 4000

    def test_section_drafts_rendered_in_order(self):
        inp = EditorInput(
            section_drafts=(
                {"section_name": "B", "section_order": 2, "body_text": "Bbody"},
                {"section_name": "A", "section_order": 1, "body_text": "Abody"},
            ),
            rfa_excerpt="",
            dialect="centrist",
            session_id="s",
            org_slug="o",
        )

        seen_md: list[str] = []

        def _capture(**kwargs):
            payload = json.loads(kwargs["stdin_payload"].decode("utf-8"))
            seen_md.append(payload["draft_markdown"])
            return SkillSubprocessResult(
                stdout='{"readability":{"score_10":7,"grade_level_estimate":"g","verdict":"ok","key_message":"k","reviewer_fatigue_sections":[]},"strengths":[],"suggestions":[],"gaps":[],"quick_wins":[],"terms_to_verify":[],"taxonomy_check":{"goals_identified":[],"outputs_identified":[],"outcomes_identified":[],"objectives_identified":[],"miscategorizations":[]}}',
                exit_code=0,
            )

        invoke_editor_adapter(inp, skill_launcher=_capture, clock=_fixed_clock())
        assert "## A" in seen_md[0]
        assert seen_md[0].index("## A") < seen_md[0].index("## B")


# ---------------------------------------------------------------------------
# F-EDITOR-* code matrix — fail paths
# ---------------------------------------------------------------------------


class TestFailureCodes:
    def test_single_replacement_corpus(self):
        fix = _load_fixture("fail/skill_output_missing_options.json")
        inp = EditorInput(
            section_drafts=tuple(fix["input_section_drafts"]),
            rfa_excerpt=fix["input_rfa_excerpt"],
            dialect=fix["input_dialect"],
            session_id="s",
            org_slug="o",
        )
        # Skill returns same malformed output twice → R2 retry exhausts → raise
        launcher = _FakeLauncher(stdouts=[fix["skill_stdout"], fix["skill_stdout"]])
        with pytest.raises(EditorSingleReplacementError) as exc_info:
            invoke_editor_adapter(
                inp, skill_launcher=launcher, clock=_fixed_clock()
            )
        assert exc_info.value.failure_code == F_EDITOR_SINGLE_REPLACEMENT

    def test_rewrite_threshold_corpus(self):
        fix = _load_fixture("fail/skill_output_rewritten_body.json")
        inp = EditorInput(
            section_drafts=tuple(fix["input_section_drafts"]),
            rfa_excerpt=fix["input_rfa_excerpt"],
            dialect=fix["input_dialect"],
            session_id="s",
            org_slug="o",
        )
        # F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED is NOT in the retryable set
        # (it's a Law-4 enforcement, not a parse / shape recovery target).
        launcher = _FakeLauncher(stdouts=[fix["skill_stdout"]])
        with pytest.raises(EditorRewroteInsteadOfFlaggedError) as exc_info:
            invoke_editor_adapter(
                inp, skill_launcher=launcher, clock=_fixed_clock()
            )
        assert exc_info.value.failure_code == F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED

    def test_malformed_json_raises(self):
        inp = _make_input()
        # Both attempts return non-JSON → raise after retry.
        launcher = _FakeLauncher(stdouts=["not json", "still not json"])
        with pytest.raises(EditorSkillOutputMalformedJson) as exc_info:
            invoke_editor_adapter(
                inp, skill_launcher=launcher, clock=_fixed_clock()
            )
        assert exc_info.value.failure_code == F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON

    def test_top_level_array_raises(self):
        inp = _make_input()
        launcher = _FakeLauncher(stdouts=["[1,2,3]", "[4,5]"])
        with pytest.raises(EditorSkillOutputMalformedJson):
            invoke_editor_adapter(
                inp, skill_launcher=launcher, clock=_fixed_clock()
            )

    def test_empty_stdout_raises(self):
        inp = _make_input()
        launcher = _FakeLauncher(stdouts=["", ""])
        with pytest.raises(EditorSkillOutputMalformedJson, match="empty"):
            invoke_editor_adapter(
                inp, skill_launcher=launcher, clock=_fixed_clock()
            )

    def test_unknown_issue_type_wrapped_as_output_shape(self):
        # The mapper raises EditorOutputShapeError for invalid issue_type;
        # retry path runs once then re-raises.
        bad_json = json.dumps(
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
        launcher = _FakeLauncher(stdouts=[bad_json, bad_json])
        with pytest.raises(EditorOutputShapeError, match="issue_type"):
            invoke_editor_adapter(
                _make_input(), skill_launcher=launcher, clock=_fixed_clock()
            )

    def test_rewrite_not_retried(self):
        # F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED is NOT retryable → only 1 call.
        fix = _load_fixture("fail/skill_output_rewritten_body.json")
        inp = EditorInput(
            section_drafts=tuple(fix["input_section_drafts"]),
            rfa_excerpt=fix["input_rfa_excerpt"],
            dialect=fix["input_dialect"],
            session_id="s",
            org_slug="o",
        )
        launcher = _FakeLauncher(stdouts=[fix["skill_stdout"], fix["skill_stdout"]])
        with pytest.raises(EditorRewroteInsteadOfFlaggedError):
            invoke_editor_adapter(
                inp, skill_launcher=launcher, clock=_fixed_clock()
            )
        assert len(launcher.calls) == 1


# ---------------------------------------------------------------------------
# Launcher exception mapping
# ---------------------------------------------------------------------------


class TestLauncherExceptions:
    def test_timeout_mapped(self):
        launcher = _RaisingLauncher(TimeoutError("timed out"))
        with pytest.raises(EditorSkillTimeout) as exc_info:
            invoke_editor_adapter(
                _make_input(), skill_launcher=launcher, clock=_fixed_clock()
            )
        assert exc_info.value.failure_code == F_EDITOR_SKILL_TIMEOUT

    def test_subprocess_called_process_error_mapped(self):
        exc = subprocess.CalledProcessError(returncode=1, cmd=["x"])
        launcher = _RaisingLauncher(exc)
        with pytest.raises(EditorSkillSubprocessFail) as exc_info:
            invoke_editor_adapter(
                _make_input(), skill_launcher=launcher, clock=_fixed_clock()
            )
        assert exc_info.value.failure_code == F_EDITOR_SKILL_SUBPROCESS_FAIL

    def test_runtime_error_mapped(self):
        launcher = _RaisingLauncher(RuntimeError("boom"))
        with pytest.raises(EditorSkillSubprocessFail):
            invoke_editor_adapter(
                _make_input(), skill_launcher=launcher, clock=_fixed_clock()
            )

    def test_misbehaving_launcher_returns_non_result(self):
        with pytest.raises(EditorSkillSubprocessFail, match="expected SkillSubprocessResult"):
            invoke_editor_adapter(
                _make_input(),
                skill_launcher=_MisbehavingLauncher(),
                clock=_fixed_clock(),
            )

    def test_input_type_check(self):
        with pytest.raises(TypeError, match="EditorInput"):
            invoke_editor_adapter(
                "not-input",  # type: ignore[arg-type]
                skill_launcher=_FakeLauncher(stdouts=[""]),
                clock=_fixed_clock(),
            )

    def test_clock_propagates_runtime_error(self):
        def _broken_clock():
            raise RuntimeError("clock broken")

        with pytest.raises(RuntimeError, match="clock broken"):
            invoke_editor_adapter(
                _make_input(),
                skill_launcher=_FakeLauncher(stdouts=["{}"]),
                clock=_broken_clock,
            )


# ---------------------------------------------------------------------------
# Protocol surface
# ---------------------------------------------------------------------------


class TestSkillLauncherProtocol:
    def test_launcher_protocol_runtime_checkable(self):
        fake = _FakeLauncher(stdouts=["{}"])
        assert isinstance(fake, SkillLauncher)

    def test_skill_subprocess_result_validates_types(self):
        with pytest.raises(TypeError):
            SkillSubprocessResult(stdout=123, exit_code=0)  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            SkillSubprocessResult(stdout="ok", exit_code="not-int")  # type: ignore[arg-type]
        # bool is rejected (isinstance(True, int) is True in Python; explicit guard)
        with pytest.raises(TypeError):
            SkillSubprocessResult(stdout="ok", exit_code=True)  # type: ignore[arg-type]
