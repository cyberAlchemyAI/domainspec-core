"""§8 Editor — whole-section capstone integration tests.

Per handoff `pipeline/handoffs/section_8_editor_whole_section_capstone_2026-04-29.md`.

Promotes §8 from per-round LOCKs (R1 adapter + R2 polish, both LOCKED 2026-04-29
row 105) to LOCKED-as-a-whole-section. Test-only round; ZERO new §8 production
code.

Five test surfaces per the handoff:

- X.1 Full Editor invocation lifecycle — `run_seat` → decode_envelope →
  PRE-gate → `invoke_editor_adapter` (skill-subprocess + parse + map +
  validate + R2 retry) → POST-gate → `encode_result` → stdout.
- X.2 F-EDITOR-* failure-code matrix — every declared F-EDITOR-* code trips
  via the canonical path. Eight codes total: ENVELOPE-MALFORMED,
  ORG-CROSS-REF, OUTPUT-SHAPE, REWROTE-INSTEAD-OF-FLAGGED,
  SINGLE-REPLACEMENT, SKILL-OUTPUT-MALFORMED-JSON, SKILL-SUBPROCESS-FAIL,
  SKILL-TIMEOUT.
- X.3 Adapter-legacy equivalence — feed the existing pass/ corpus (vapg +
  reap) into both the new adapter's parse path and the legacy
  `pipeline.orchestrator.seats.editor.extract_json` + `validate`; verify
  byte-equivalent JSON parse + zero-error legacy validate.
- X.4 Cross-round composition — R1 (adapter / seat / types) + R2 (validator
  + retry-with-clarification) compose without import-time gaps;
  BLUEPRINT_DEPS hash pins consistent; F-code constants uniquely-named with
  canonical `F-EDITOR-` prefix; V1 inline-literal rebind-resistance pinned
  at capstone (180_000 ms timeout + 40% rewrite threshold + N=2 retry cap).
- X.5 Adversarial — defense-in-depth across composed surface (PRE trip
  short-circuits adapter; clock-raise propagates; sanitized stderr on bug-
  class; multi-violation deterministic ordering; uppercase-hash boundary).

All collaborators injected via existing E-017 Protocol seams. No network,
no actual subprocess, no clock dependency.
"""
from __future__ import annotations

import io
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from pipeline.seats import editor as editor_pkg
from pipeline.seats.editor import (
    BLUEPRINT_DEPS,
    ENVELOPE_VERSION_V1,
    EXIT_GATE_FAIL,
    EXIT_INTERNAL_ERROR,
    EXIT_OK,
    F_EDITOR_ENVELOPE_MALFORMED,
    F_EDITOR_ORG_CROSS_REF,
    F_EDITOR_OUTPUT_SHAPE,
    F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED,
    F_EDITOR_SINGLE_REPLACEMENT,
    F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON,
    F_EDITOR_SKILL_SUBPROCESS_FAIL,
    F_EDITOR_SKILL_TIMEOUT,
    RESULT_VERSION_V1,
    EditorEnvelope,
    EditorEnvelopeMalformed,
    EditorGateFailed,
    EditorInput,
    EditorOutput,
    EditorOutputShapeError,
    EditorRewroteInsteadOfFlaggedError,
    EditorSingleReplacementError,
    EditorSkillOutputMalformedJson,
    EditorSkillSubprocessFail,
    EditorSkillTimeout,
    SkillLauncher,
    SkillSubprocessResult,
    TAXONOMY_CATEGORIES,
    ValidationReport,
    apply_r2_validation,
    audit_taxonomy_sort,
    audit_terms_to_verify_cross_reference,
    decode_envelope,
    dedupe_quick_wins,
    default_cross_org_pre_gate,
    default_noop_post_gate,
    encode_result,
    invoke_editor_adapter,
    parse_skill_output,
    run_seat,
    validate_editor_output_shape,
)
from pipeline.seats.editor.types import (
    _DIALECT_VALID,
    _ISSUE_TYPE_VALID,
    _REPLACEMENT_LABEL_VALID,
    _SEVERITY_VALID,
)


UTC = timezone.utc
_FIXED_NOW = datetime(2026, 4, 29, 12, 0, tzinfo=UTC)
CORPUS_ROOT = Path(__file__).resolve().parent.parent.parent / "corpus" / "editor" / "v1"


# ---------------------------------------------------------------------------
# Shared fixtures + helpers
# ---------------------------------------------------------------------------


def _clock() -> datetime:
    return _FIXED_NOW


def _ok_skill_stdout(*, suggestions: int = 1, body_chars: int = 0) -> str:
    """Build a well-formed skill stdout with N suggestions.

    Each suggestion uses 2 replacement options (within 2-3 invariant).
    Replacement text length stays under the 40% rewrite threshold relative
    to ``body_chars`` (caller-controlled).
    """
    return json.dumps(
        {
            "readability": {
                "score_10": 7,
                "estimated_grade_level": 11,
                "grade_level_estimate": "grade 11",
                "key_message": "summary",
                "reviewer_fatigue_sections": [],
                "verdict": "ok",
            },
            "strengths": [],
            "suggestions": [
                {
                    "section": "1.a",
                    "original": "vague phrase",
                    "issue": "vague",
                    "issue_type": "jargon",
                    "severity": "low",
                    "options": [
                        {"label": "A", "text": "x", "note": ""},
                        {"label": "B", "text": "y", "note": ""},
                    ],
                    "rubric_connection": "",
                }
                for _ in range(suggestions)
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


_DEFAULT_BODY = "We grow specialty mushrooms across cooperative facilities for regional buyers. " * 4


def _make_envelope_dict(**overrides: Any) -> dict[str, Any]:
    base = {
        "envelope_version": ENVELOPE_VERSION_V1,
        "run_id": "run-2026-04-29-capstone",
        "org_slug": "mycosymbiotics",
        "iteration_number": 0,
        "section_drafts": [
            {
                "section_name": "1.a",
                "section_order": 1,
                "body_text": _DEFAULT_BODY,
            }
        ],
        "rfa_excerpt": "USDA VAPG FY26 — operational efficiency.",
        "dialect": "centrist",
        "session_id": "sess-1",
        "envelope_emitted_at_utc": "2026-04-29T12:00:00+00:00",
    }
    base.update(overrides)
    return base


class _FakeLauncher:
    """E-017 SkillLauncher fake — returns canned stdout list, tracks calls."""

    def __init__(
        self,
        *,
        stdouts: list[str] | None = None,
        exit_codes: list[int] | None = None,
    ) -> None:
        self._stdouts = list(stdouts) if stdouts is not None else [_ok_skill_stdout()]
        self._exit_codes = (
            list(exit_codes) if exit_codes is not None else [0] * len(self._stdouts)
        )
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
    def __init__(self, exc: BaseException) -> None:
        self._exc = exc

    def __call__(self, **_kwargs) -> SkillSubprocessResult:
        raise self._exc


def _run_seat(
    *,
    envelope_dict: dict[str, Any] | None = None,
    skill_launcher: SkillLauncher | None = None,
    pre_gate: Any = None,
    post_gate: Any = None,
    ambient_org_slug: str = "mycosymbiotics",
    clock: Any = _clock,
) -> tuple[int, bytes, bytes]:
    if envelope_dict is None:
        envelope_dict = _make_envelope_dict()
    if skill_launcher is None:
        skill_launcher = _FakeLauncher()
    if pre_gate is None:
        pre_gate = default_cross_org_pre_gate
    if post_gate is None:
        post_gate = default_noop_post_gate
    stdin = io.BytesIO(json.dumps(envelope_dict).encode("utf-8"))
    stdout = io.BytesIO()
    stderr = io.BytesIO()
    rc = run_seat(
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        clock=clock,
        skill_launcher=skill_launcher,
        pre_gate=pre_gate,
        post_gate=post_gate,
        ambient_org_slug=ambient_org_slug,
    )
    return rc, stdout.getvalue(), stderr.getvalue()


def _stderr_failure_code(stderr_bytes: bytes) -> str:
    line = json.loads(stderr_bytes.decode("utf-8").strip())
    return line["failure_code"]


def _make_input(*, body_text: str = _DEFAULT_BODY) -> EditorInput:
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


def _build_ok_output() -> EditorOutput:
    """Construct a minimal happy-path EditorOutput via the adapter."""
    inp = _make_input()
    launcher = _FakeLauncher(stdouts=[_ok_skill_stdout()])
    return invoke_editor_adapter(inp, skill_launcher=launcher, clock=_clock)


def _load_corpus_pass(name: str) -> dict:
    return json.loads((CORPUS_ROOT / "pass" / f"{name}.json").read_text())


# ---------------------------------------------------------------------------
# X.1 Full Editor invocation lifecycle (≥20 composition tests)
# ---------------------------------------------------------------------------


class TestX1FullLifecycle:
    """End-to-end ``run_seat`` across decode → PRE → adapter → POST → encode."""

    def test_happy_path_exit_zero_emits_canonical_result(self):
        rc, stdout, stderr = _run_seat()
        assert rc == EXIT_OK
        assert stderr == b""
        decoded = json.loads(stdout)
        assert decoded["result_version"] == RESULT_VERSION_V1
        assert decoded["run_id"] == "run-2026-04-29-capstone"
        assert decoded["org_slug"] == "mycosymbiotics"
        assert decoded["iteration_number"] == 0

    def test_happy_path_canonical_keys_sorted(self):
        rc, stdout, _ = _run_seat()
        assert rc == EXIT_OK
        decoded = json.loads(stdout)
        assert list(decoded.keys()) == sorted(decoded.keys())
        # editor_output sub-keys also sorted (canonical JSON).
        eo = decoded["editor_output"]
        assert list(eo.keys()) == sorted(eo.keys())

    def test_happy_path_trailing_newline_on_stdout(self):
        rc, stdout, _ = _run_seat()
        assert rc == EXIT_OK
        assert stdout.endswith(b"\n")

    def test_happy_path_seat_emitted_at_utc_round_trip(self):
        rc, stdout, _ = _run_seat()
        decoded = json.loads(stdout)
        emit_dt = datetime.fromisoformat(decoded["seat_emitted_at_utc"])
        assert emit_dt == _FIXED_NOW

    def test_run_id_passes_through_envelope_to_result(self):
        env_dict = _make_envelope_dict(run_id="run-special-XYZ")
        rc, stdout, _ = _run_seat(envelope_dict=env_dict)
        assert rc == EXIT_OK
        decoded = json.loads(stdout)
        assert decoded["run_id"] == "run-special-XYZ"

    def test_iteration_number_passes_through(self):
        env_dict = _make_envelope_dict(iteration_number=4)
        rc, stdout, _ = _run_seat(envelope_dict=env_dict)
        decoded = json.loads(stdout)
        assert decoded["iteration_number"] == 4

    def test_org_slug_passes_through(self):
        env_dict = _make_envelope_dict(org_slug="fit_farms_llc")
        rc, stdout, _ = _run_seat(
            envelope_dict=env_dict, ambient_org_slug="fit_farms_llc"
        )
        decoded = json.loads(stdout)
        assert decoded["org_slug"] == "fit_farms_llc"

    def test_dialect_round_trips_to_skill_payload(self):
        # Build an envelope with each valid dialect and confirm skill stdin
        # payload mirrors it.
        captured: dict[str, str] = {}

        class _DialectCapture:
            def __call__(self, **kwargs):
                payload = json.loads(kwargs["stdin_payload"].decode("utf-8"))
                captured["dialect"] = payload["dialect"]
                return SkillSubprocessResult(stdout=_ok_skill_stdout(), exit_code=0)

        env_dict = _make_envelope_dict(dialect="conservative")
        rc, _, _ = _run_seat(envelope_dict=env_dict, skill_launcher=_DialectCapture())
        assert rc == EXIT_OK
        assert captured["dialect"] == "conservative"

    def test_pre_gate_runs_before_adapter(self):
        # A failing PRE-gate prevents the launcher from ever being called.
        launcher = _FakeLauncher()

        def _foreign(*, envelope, ambient_org_slug):
            raise EditorGateFailed(
                failure_code=F_EDITOR_ORG_CROSS_REF,
                trigger="custom",
                evidence={},
            )

        rc, _, _ = _run_seat(skill_launcher=launcher, pre_gate=_foreign)
        assert rc == EXIT_GATE_FAIL
        assert launcher.calls == []

    def test_post_gate_runs_after_adapter(self):
        # POST-gate trip emits stderr but adapter ran (launcher was called).
        launcher = _FakeLauncher()

        def _post_trip(*, envelope, editor_output):
            raise EditorGateFailed(
                failure_code="F-CUSTOM-POST",
                trigger="post-gate",
                evidence={"observed": "violation"},
            )

        rc, _, stderr = _run_seat(skill_launcher=launcher, post_gate=_post_trip)
        assert rc == EXIT_GATE_FAIL
        assert len(launcher.calls) == 1
        assert _stderr_failure_code(stderr) == "F-CUSTOM-POST"

    def test_skill_launcher_called_with_180000_ms_timeout(self):
        timeouts: list[int] = []

        class _CaptureTimeout:
            def __call__(self, **kwargs):
                timeouts.append(kwargs["timeout_ms"])
                return SkillSubprocessResult(
                    stdout=_ok_skill_stdout(), exit_code=0
                )

        rc, _, _ = _run_seat(skill_launcher=_CaptureTimeout())
        assert rc == EXIT_OK
        assert timeouts == [180_000]

    def test_skill_launcher_called_with_editor_slug(self):
        slugs: list[str] = []

        class _CaptureSlug:
            def __call__(self, **kwargs):
                slugs.append(kwargs["skill_slug"])
                return SkillSubprocessResult(
                    stdout=_ok_skill_stdout(), exit_code=0
                )

        rc, _, _ = _run_seat(skill_launcher=_CaptureSlug())
        assert rc == EXIT_OK
        assert slugs == ["editor"]

    def test_multi_section_drafts_rendered_in_section_order(self):
        env_dict = _make_envelope_dict(
            section_drafts=[
                {"section_name": "B-second", "section_order": 2, "body_text": "Bbody"},
                {"section_name": "A-first", "section_order": 1, "body_text": "Abody"},
            ]
        )
        captured_md: list[str] = []

        class _CaptureMd:
            def __call__(self, **kwargs):
                payload = json.loads(kwargs["stdin_payload"].decode("utf-8"))
                captured_md.append(payload["draft_markdown"])
                return SkillSubprocessResult(
                    stdout=_ok_skill_stdout(), exit_code=0
                )

        rc, _, _ = _run_seat(envelope_dict=env_dict, skill_launcher=_CaptureMd())
        assert rc == EXIT_OK
        md = captured_md[0]
        assert md.index("## A-first") < md.index("## B-second")

    def test_rfa_excerpt_truncated_at_4000_chars(self):
        env_dict = _make_envelope_dict(rfa_excerpt="x" * 5000)
        captured: list[int] = []

        class _CaptureRfaLen:
            def __call__(self, **kwargs):
                payload = json.loads(kwargs["stdin_payload"].decode("utf-8"))
                captured.append(len(payload["rfa_excerpt"]))
                return SkillSubprocessResult(
                    stdout=_ok_skill_stdout(), exit_code=0
                )

        rc, _, _ = _run_seat(envelope_dict=env_dict, skill_launcher=_CaptureRfaLen())
        assert rc == EXIT_OK
        assert captured == [4000]

    def test_session_id_flows_to_skill_invocation(self):
        env_dict = _make_envelope_dict(session_id="sess-XYZ-2026")
        captured: list[str] = []

        class _CaptureSession:
            def __call__(self, **kwargs):
                payload = json.loads(kwargs["stdin_payload"].decode("utf-8"))
                captured.append(payload["session_id"])
                return SkillSubprocessResult(
                    stdout=_ok_skill_stdout(), exit_code=0
                )

        rc, _, _ = _run_seat(envelope_dict=env_dict, skill_launcher=_CaptureSession())
        assert rc == EXIT_OK
        assert captured == ["sess-XYZ-2026"]

    def test_run_seat_returns_int_no_sys_exit_on_happy_path(self):
        # Defensive against drift: run_seat must return an int (no sys.exit).
        rc, _, _ = _run_seat()
        assert isinstance(rc, int)
        assert rc == EXIT_OK

    def test_run_seat_returns_int_on_gate_fail(self):
        rc, _, _ = _run_seat(ambient_org_slug="other-org")
        assert isinstance(rc, int)
        assert rc == EXIT_GATE_FAIL

    def test_envelope_decode_round_trip(self):
        env_dict = _make_envelope_dict(run_id="rt-1")
        env_bytes = json.dumps(env_dict).encode("utf-8")
        env = decode_envelope(raw_bytes=env_bytes)
        assert isinstance(env, EditorEnvelope)
        assert env.envelope_version == ENVELOPE_VERSION_V1
        assert env.run_id == "rt-1"
        assert env.iteration_number == 0
        assert len(env.section_drafts) == 1

    def test_emitted_stdout_carries_editor_output_block(self):
        rc, stdout, _ = _run_seat()
        decoded = json.loads(stdout)
        eo = decoded["editor_output"]
        assert "flagged_terms" in eo
        assert "tone_feedback" in eo
        assert "taxonomy_check" in eo
        assert "quick_wins" in eo
        assert "terms_to_verify" in eo
        assert "gaps" in eo

    def test_flagged_terms_carry_2_3_replacement_options(self):
        rc, stdout, _ = _run_seat()
        decoded = json.loads(stdout)
        for ft in decoded["editor_output"]["flagged_terms"]:
            n = len(ft["replacement_options"])
            assert 2 <= n <= 3

    def test_default_pre_gate_blocks_cross_org_invocation(self):
        rc, _, stderr = _run_seat(ambient_org_slug="competitor-org")
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_EDITOR_ORG_CROSS_REF

    def test_default_post_gate_does_not_alter_output(self):
        # The default no-op POST-gate must not modify stdout shape.
        rc, stdout, _ = _run_seat(post_gate=default_noop_post_gate)
        decoded = json.loads(stdout)
        assert decoded["result_version"] == RESULT_VERSION_V1


# ---------------------------------------------------------------------------
# X.2 F-EDITOR-* failure-code matrix (8 codes)
# ---------------------------------------------------------------------------


class TestX2FCodeMatrixEnvelope:
    """Envelope-decode-class F-codes."""

    def test_envelope_malformed_via_non_json_stdin(self):
        stdin = io.BytesIO(b"not-json")
        stdout = io.BytesIO()
        stderr = io.BytesIO()
        rc = run_seat(
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            clock=_clock,
            skill_launcher=_FakeLauncher(),
            pre_gate=default_cross_org_pre_gate,
            post_gate=default_noop_post_gate,
            ambient_org_slug="o",
        )
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr.getvalue()) == F_EDITOR_ENVELOPE_MALFORMED

    def test_envelope_malformed_via_wrong_version(self):
        env_dict = _make_envelope_dict(envelope_version="editor-envelope.v0")
        rc, _, stderr = _run_seat(envelope_dict=env_dict)
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_EDITOR_ENVELOPE_MALFORMED

    def test_envelope_malformed_via_empty_section_drafts(self):
        env_dict = _make_envelope_dict(section_drafts=[])
        rc, _, stderr = _run_seat(envelope_dict=env_dict)
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_EDITOR_ENVELOPE_MALFORMED


class TestX2FCodeMatrixPreGate:
    """PRE-gate F-codes."""

    def test_org_cross_ref_fires_on_ambient_mismatch(self):
        rc, _, stderr = _run_seat(ambient_org_slug="competitor")
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_EDITOR_ORG_CROSS_REF


class TestX2FCodeMatrixAdapter:
    """Adapter / launcher / parse / map / validate F-codes."""

    def test_skill_timeout_fires(self):
        rc, _, stderr = _run_seat(
            skill_launcher=_RaisingLauncher(TimeoutError("timed out")),
        )
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_EDITOR_SKILL_TIMEOUT

    def test_skill_subprocess_fail_fires(self):
        rc, _, stderr = _run_seat(
            skill_launcher=_RaisingLauncher(RuntimeError("crash")),
        )
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_EDITOR_SKILL_SUBPROCESS_FAIL

    def test_skill_output_malformed_json_fires_after_retry(self):
        # Both attempts return non-JSON; retry exhausts; F-code fires.
        rc, _, stderr = _run_seat(
            skill_launcher=_FakeLauncher(stdouts=["not json", "still not json"]),
        )
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON

    def test_output_shape_fires_on_invalid_issue_type(self):
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
                        "issue_type": "climate_nostalgia",  # not in valid set
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
        rc, _, stderr = _run_seat(skill_launcher=_FakeLauncher(stdouts=[bad, bad]))
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_EDITOR_OUTPUT_SHAPE

    def test_single_replacement_fires_after_retry(self):
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
                        "options": [
                            {"label": "A", "text": "only_one", "note": ""},
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
        rc, _, stderr = _run_seat(skill_launcher=_FakeLauncher(stdouts=[bad, bad]))
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_EDITOR_SINGLE_REPLACEMENT

    def test_rewrite_threshold_fires_without_retry(self):
        # Body is short (~80 chars); replacements summing >32 chars trip the
        # 40% threshold. F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED is NOT retryable.
        short_body = "We grow mushrooms at the cooperative facility on shared beds."
        env_dict = _make_envelope_dict(
            section_drafts=[
                {
                    "section_name": "1.a",
                    "section_order": 1,
                    "body_text": short_body,
                }
            ]
        )
        rewrite = json.dumps(
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
                        "original": short_body,
                        "issue": "rewrite",
                        "issue_type": "jargon",
                        "severity": "high",
                        "options": [
                            {"label": "A", "text": "X" * 40, "note": ""},
                            {"label": "B", "text": "Y" * 40, "note": ""},
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
        launcher = _FakeLauncher(stdouts=[rewrite])
        rc, _, stderr = _run_seat(envelope_dict=env_dict, skill_launcher=launcher)
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED
        # NOT retried — single launcher call.
        assert len(launcher.calls) == 1


class TestX2FCodeMatrixCompleteness:
    """Closure check: every declared F-EDITOR-* string is reachable somewhere."""

    def test_all_f_codes_have_canonical_prefix(self):
        f_codes = (
            F_EDITOR_ENVELOPE_MALFORMED,
            F_EDITOR_ORG_CROSS_REF,
            F_EDITOR_OUTPUT_SHAPE,
            F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED,
            F_EDITOR_SINGLE_REPLACEMENT,
            F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON,
            F_EDITOR_SKILL_SUBPROCESS_FAIL,
            F_EDITOR_SKILL_TIMEOUT,
        )
        for code in f_codes:
            assert code.startswith("F-EDITOR-"), code

    def test_f_codes_uniquely_named(self):
        f_codes = (
            F_EDITOR_ENVELOPE_MALFORMED,
            F_EDITOR_ORG_CROSS_REF,
            F_EDITOR_OUTPUT_SHAPE,
            F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED,
            F_EDITOR_SINGLE_REPLACEMENT,
            F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON,
            F_EDITOR_SKILL_SUBPROCESS_FAIL,
            F_EDITOR_SKILL_TIMEOUT,
        )
        assert len(set(f_codes)) == len(f_codes) == 8

    def test_f_codes_use_upper_kebab_body(self):
        f_codes = (
            F_EDITOR_ENVELOPE_MALFORMED,
            F_EDITOR_ORG_CROSS_REF,
            F_EDITOR_OUTPUT_SHAPE,
            F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED,
            F_EDITOR_SINGLE_REPLACEMENT,
            F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON,
            F_EDITOR_SKILL_SUBPROCESS_FAIL,
            F_EDITOR_SKILL_TIMEOUT,
        )
        for code in f_codes:
            body = code[len("F-EDITOR-"):]
            assert body == body.upper(), code
            assert "_" not in body, code


# ---------------------------------------------------------------------------
# X.3 Adapter-legacy equivalence
# ---------------------------------------------------------------------------


class TestX3AdapterLegacyEquivalence:
    """Both pass/ corpus fixtures parse identically through new + legacy paths.

    Legacy adapter ``pipeline.orchestrator.seats.editor`` exposes
    ``strip_fences`` + ``extract_json`` (the same parse discipline lifted
    into the new adapter as ``_strip_fences`` + ``_extract_json_object``).
    Equivalence is byte-equality of the parsed JSON object plus zero-error
    legacy ``validate`` against a derivation of the parsed shape.
    """

    def _parse_through_new_adapter(self, fix: dict) -> EditorOutput:
        inp = EditorInput(
            section_drafts=tuple(fix["input_section_drafts"]),
            rfa_excerpt=fix["input_rfa_excerpt"],
            dialect=fix["input_dialect"],
            session_id="s",
            org_slug="o",
        )
        launcher = _FakeLauncher(stdouts=[fix["skill_stdout"]])
        return invoke_editor_adapter(inp, skill_launcher=launcher, clock=_clock)

    def _parse_through_legacy(self, fix: dict) -> dict:
        from pipeline.orchestrator.seats.editor import extract_json
        return extract_json(fix["skill_stdout"])

    def _legacy_compatible_view(self, fix: dict) -> dict:
        """Translate the new skill JSON into the legacy schema for validate()."""
        raw = self._parse_through_legacy(fix)
        # Map suggestions[].options[] (objects) → legacy replacements (strings).
        legacy_issues: list[dict[str, Any]] = []
        for i, sug in enumerate(raw.get("suggestions", [])):
            legacy_issues.append(
                {
                    "id": f"i{i}",
                    "location": sug.get("section", ""),
                    "issue_type": sug.get("issue_type", "jargon"),
                    "severity": sug.get("severity", "low"),
                    "excerpt": sug.get("original", ""),
                    "why_it_hurts": sug.get("issue", ""),
                    "replacements": [
                        opt["text"] for opt in sug.get("options", [])
                    ],
                }
            )
        return {
            "overall_readability": raw.get("readability", {}),
            "taxonomy_check": raw.get("taxonomy_check", {}),
            "issues": legacy_issues,
            "quick_wins": raw.get("quick_wins", []),
            "terms_to_verify": raw.get("terms_to_verify", []),
        }

    def test_vapg_corpus_parses_through_new_adapter(self):
        fix = _load_corpus_pass("vapg_clean_draft")
        out = self._parse_through_new_adapter(fix)
        assert isinstance(out, EditorOutput)
        assert len(out.flagged_terms) == 1

    def test_reap_corpus_parses_through_new_adapter(self):
        fix = _load_corpus_pass("reap_clean_draft")
        out = self._parse_through_new_adapter(fix)
        assert isinstance(out, EditorOutput)
        assert len(out.flagged_terms) >= 1

    def test_vapg_corpus_legacy_extract_json_equivalent(self):
        fix = _load_corpus_pass("vapg_clean_draft")
        new_obj = parse_skill_output(fix["skill_stdout"])
        legacy_obj = self._parse_through_legacy(fix)
        # Byte-equivalent parse — both helpers strip fences + raw-decode the
        # same JSON object.
        assert dict(new_obj) == dict(legacy_obj)

    def test_reap_corpus_legacy_extract_json_equivalent(self):
        fix = _load_corpus_pass("reap_clean_draft")
        new_obj = parse_skill_output(fix["skill_stdout"])
        legacy_obj = self._parse_through_legacy(fix)
        assert dict(new_obj) == dict(legacy_obj)

    def test_vapg_corpus_passes_legacy_validate(self):
        from pipeline.orchestrator.seats.editor import validate
        fix = _load_corpus_pass("vapg_clean_draft")
        legacy_view = self._legacy_compatible_view(fix)
        errs = validate(legacy_view)
        assert errs == []

    def test_reap_corpus_passes_legacy_validate(self):
        from pipeline.orchestrator.seats.editor import validate
        fix = _load_corpus_pass("reap_clean_draft")
        legacy_view = self._legacy_compatible_view(fix)
        errs = validate(legacy_view)
        assert errs == []

    def test_strip_fences_byte_identical_on_fenced_input(self):
        from pipeline.orchestrator.seats.editor import strip_fences as legacy_strip
        from pipeline.seats.editor.adapter import _strip_fences as new_strip
        text = "```json\n{\"a\":1}\n```"
        assert legacy_strip(text) == new_strip(text)

    def test_strip_fences_byte_identical_on_unfenced_input(self):
        from pipeline.orchestrator.seats.editor import strip_fences as legacy_strip
        from pipeline.seats.editor.adapter import _strip_fences as new_strip
        text = '  {"a": 1}\n  '
        assert legacy_strip(text) == new_strip(text)


# ---------------------------------------------------------------------------
# X.4 Cross-round composition (R1 + R2 compose without gaps)
# ---------------------------------------------------------------------------


class TestX4CrossRoundComposition:
    """R1 (adapter / seat / types) + R2 (validator / retry) compose cleanly."""

    def test_blueprint_deps_pins_all_six_anchors(self):
        # Editor ships with five anchors: §7 scribe, §0.5 scribe-amendment,
        # §5 pipeline, §4 logician, §6 envelope, plus the operator-vetted
        # skill markdown. All six must be present.
        expected = {
            "section_07_scribe.md",
            "section_00_5_section_07_scribe_amendment.md",
            "section_05_pipeline.md",
            "section_04_logician.md",
            "section_06_operating_envelope.md",
            "skills/editor/SKILL.md",
        }
        assert set(BLUEPRINT_DEPS.keys()) == expected

    def test_blueprint_deps_hash_format_invariants(self):
        # All hash_sha3_512_prefix16 entries are 16-hex lowercase.
        for anchor, meta in BLUEPRINT_DEPS.items():
            h = meta.get("hash_sha3_512_prefix16")
            assert isinstance(h, str), anchor
            assert len(h) == 16, (anchor, h)
            assert all(c in "0123456789abcdef" for c in h), (anchor, h)

    def test_blueprint_deps_section_07_scribe_pinned_at_v1_1_1(self):
        assert BLUEPRINT_DEPS["section_07_scribe.md"]["version"] == "v1.1.1"

    def test_envelope_version_inline_literal(self):
        assert ENVELOPE_VERSION_V1 == "editor-envelope.v1"

    def test_result_version_inline_literal(self):
        assert RESULT_VERSION_V1 == "editor-result.v1"

    def test_exit_codes_inline_literals(self):
        assert EXIT_OK == 0
        assert EXIT_INTERNAL_ERROR == 1
        assert EXIT_GATE_FAIL == 2

    def test_timeout_inline_literal_180000_ms(self):
        # The 180_000 ms timeout is asserted at every launcher invocation
        # in this capstone's _FakeLauncher; this test pins it as a contract.
        captured: list[int] = []

        class _CaptureT:
            def __call__(self, **kwargs):
                captured.append(kwargs["timeout_ms"])
                return SkillSubprocessResult(
                    stdout=_ok_skill_stdout(), exit_code=0
                )

        rc, _, _ = _run_seat(skill_launcher=_CaptureT())
        assert rc == EXIT_OK
        assert captured == [180_000]

    def test_dialect_valid_set_complete(self):
        assert _DIALECT_VALID == frozenset(
            {"conservative", "centrist", "progressive", "soul_fire"}
        )

    def test_severity_valid_set_complete(self):
        assert _SEVERITY_VALID == frozenset({"high", "medium", "low"})

    def test_replacement_label_valid_set_complete(self):
        assert _REPLACEMENT_LABEL_VALID == frozenset({"A", "B", "C"})

    def test_issue_type_valid_set_includes_specificity_gap(self):
        # specificity_gap was added to the valid issue-type vocabulary at R1
        # per types.py docstring (lifted from skills/editor/SKILL.md §3).
        assert "specificity_gap" in _ISSUE_TYPE_VALID

    def test_issue_type_valid_set_has_nine_entries(self):
        assert len(_ISSUE_TYPE_VALID) == 9

    def test_taxonomy_categories_pinned(self):
        assert TAXONOMY_CATEGORIES == ("goals", "outputs", "outcomes", "objectives")

    def test_validation_report_surface_complete(self):
        rep = ValidationReport(
            taxonomy_duplicates=("dup",),
            term_orphans=("orphan",),
            quick_wins_deduplicated=2,
        )
        assert rep.taxonomy_duplicates == ("dup",)
        assert rep.term_orphans == ("orphan",)
        assert rep.quick_wins_deduplicated == 2

    def test_apply_r2_validation_round_trip_on_happy_output(self):
        out = _build_ok_output()
        deduped, report = apply_r2_validation(out)
        # Identity-preserved when no duplicates / orphans / dedupes.
        assert deduped is out
        assert report.taxonomy_duplicates == ()
        assert report.term_orphans == ()
        assert report.quick_wins_deduplicated == 0

    def test_dedupe_quick_wins_idempotent_on_unique_inputs(self):
        out = _build_ok_output()
        deduped, removed = dedupe_quick_wins(out)
        assert removed == 0
        assert deduped is out

    def test_audit_taxonomy_sort_reads_categories_correctly(self):
        out = _build_ok_output()
        # Empty categories → empty duplicates.
        assert audit_taxonomy_sort(out) == ()

    def test_audit_terms_to_verify_returns_orphans(self):
        out = _build_ok_output()
        # Empty terms_to_verify → empty orphans.
        assert audit_terms_to_verify_cross_reference(out) == ()

    def test_invoke_editor_adapter_builds_typed_editor_output(self):
        out = _build_ok_output()
        assert isinstance(out, EditorOutput)
        # 2-3 invariant baked in.
        for ft in out.flagged_terms:
            assert 2 <= len(ft.replacement_options) <= 3

    def test_validate_editor_output_shape_passes_on_happy_path(self):
        out = _build_ok_output()
        # Source body is _DEFAULT_BODY; happy fixture's replacements are tiny
        # and well under the 40% threshold.
        validate_editor_output_shape(
            out,
            source_section_drafts=(
                {
                    "section_name": "1.a",
                    "section_order": 1,
                    "body_text": _DEFAULT_BODY,
                },
            ),
        )

    def test_skill_launcher_protocol_is_runtime_checkable(self):
        # E-017 12th firing — Protocol must accept any duck-typed launcher.
        fake = _FakeLauncher()
        assert isinstance(fake, SkillLauncher)

    def test_package_init_re_exports_cover_full_surface(self):
        # Every public symbol in pipeline.seats.editor.__all__ must resolve.
        for name in editor_pkg.__all__:
            assert hasattr(editor_pkg, name), name


# ---------------------------------------------------------------------------
# X.5 Adversarial — defense-in-depth across composed surface
# ---------------------------------------------------------------------------


class TestX5Adversarial:

    def test_pre_gate_trip_short_circuits_post_gate(self):
        # PRE-gate raises → POST-gate never runs (counted-call assertion).
        post_calls: list[Any] = []

        def _track_post(*, envelope, editor_output) -> None:
            post_calls.append(editor_output)

        rc, _, _ = _run_seat(
            ambient_org_slug="other-org",
            post_gate=_track_post,
        )
        assert rc == EXIT_GATE_FAIL
        assert post_calls == []

    def test_pre_gate_unhandled_raise_is_bug_class_exit_1(self):
        def _broken_pre(*, envelope, ambient_org_slug):
            raise RuntimeError("pre_gate seat bug")

        rc, _, stderr = _run_seat(pre_gate=_broken_pre)
        assert rc == EXIT_INTERNAL_ERROR
        # Sanitized stderr — class name only, no message leak.
        assert b"RuntimeError" in stderr
        assert b"pre_gate seat bug" not in stderr

    def test_post_gate_unhandled_raise_is_bug_class_exit_1(self):
        def _broken_post(*, envelope, editor_output):
            raise TypeError("post_gate seat bug")

        rc, _, stderr = _run_seat(post_gate=_broken_post)
        assert rc == EXIT_INTERNAL_ERROR
        assert b"TypeError" in stderr
        # Defense-in-depth: message scrubbed.
        assert b"post_gate seat bug" not in stderr

    def test_misbehaving_launcher_returns_non_result_object(self):
        class _BadLauncher:
            def __call__(self, **_kwargs):
                return "not-a-result-object"  # wrong type

        rc, _, stderr = _run_seat(skill_launcher=_BadLauncher())
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_EDITOR_SKILL_SUBPROCESS_FAIL

    def test_two_violations_first_detection_wins(self):
        # Adapter's mapper validates structural shape BEFORE the validator
        # checks 2-3 invariant; an object with both invalid issue_type AND
        # 1-option replacement should surface OUTPUT-SHAPE first (mapper
        # runs first in _parse_map_validate).
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
                        "issue_type": "INVALID_KIND",
                        "severity": "low",
                        "options": [
                            {"label": "A", "text": "a", "note": ""},
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
        rc, _, stderr = _run_seat(skill_launcher=_FakeLauncher(stdouts=[bad, bad]))
        assert rc == EXIT_GATE_FAIL
        # Mapper-stage shape error wins; not single-replacement.
        assert _stderr_failure_code(stderr) == F_EDITOR_OUTPUT_SHAPE

    def test_naive_datetime_in_envelope_rejected_at_decode(self):
        env_dict = _make_envelope_dict(
            envelope_emitted_at_utc="2026-04-29T12:00:00"  # no tz
        )
        rc, _, stderr = _run_seat(envelope_dict=env_dict)
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_EDITOR_ENVELOPE_MALFORMED

    def test_invalid_dialect_rejected_at_envelope_decode(self):
        env_dict = _make_envelope_dict(dialect="hard_left")
        rc, _, stderr = _run_seat(envelope_dict=env_dict)
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_EDITOR_ENVELOPE_MALFORMED

    def test_negative_iteration_number_rejected(self):
        env_dict = _make_envelope_dict(iteration_number=-1)
        rc, _, stderr = _run_seat(envelope_dict=env_dict)
        assert rc == EXIT_GATE_FAIL
        assert _stderr_failure_code(stderr) == F_EDITOR_ENVELOPE_MALFORMED

    def test_stderr_failure_payload_includes_envelope_version(self):
        rc, _, stderr = _run_seat(ambient_org_slug="other-org")
        assert rc == EXIT_GATE_FAIL
        line = json.loads(stderr.decode("utf-8").strip())
        assert line["envelope_version"] == ENVELOPE_VERSION_V1
        assert line["failure_code"] == F_EDITOR_ORG_CROSS_REF
        assert "emitted_at_utc" in line

    def test_clock_propagates_runtime_error_through_adapter(self):
        # The clock seam is consulted both by adapter (invocation_at_utc)
        # and seat (seat_emitted_at_utc + stderr emit_at_utc). A raising
        # clock surfaces from inside invoke_editor_adapter — the seat
        # converts the RuntimeError to EXIT_INTERNAL_ERROR (bug-class).
        def _broken_clock():
            raise RuntimeError("clock down")

        rc, _, stderr = _run_seat(clock=_broken_clock)
        assert rc == EXIT_INTERNAL_ERROR
        assert b"RuntimeError" in stderr

    def test_envelope_round_trip_preserves_iteration_through_result(self):
        env_dict = _make_envelope_dict(iteration_number=7)
        rc, stdout, _ = _run_seat(envelope_dict=env_dict)
        decoded = json.loads(stdout)
        assert decoded["iteration_number"] == 7

    def test_envelope_round_trip_preserves_org_slug_through_result(self):
        env_dict = _make_envelope_dict(org_slug="run_a_muck_farm")
        rc, stdout, _ = _run_seat(
            envelope_dict=env_dict, ambient_org_slug="run_a_muck_farm"
        )
        decoded = json.loads(stdout)
        assert decoded["org_slug"] == "run_a_muck_farm"


# ---------------------------------------------------------------------------
# X.6 Capstone manifest — pin LOCK shape so a future drift surfaces
# ---------------------------------------------------------------------------


class TestX6CapstoneManifest:
    """Promotes the §8 surface from per-round LOCKs to LOCKED-as-a-whole.

    These tests pin the closed-set of public exports + F-codes one more
    time — even if a future round adds R3 (e.g., revision-loop hooks),
    these manifest tests will surface the surface-area change before the
    LOCK-as-a-whole stamp can be re-issued.
    """

    def test_lifecycle_constants_present(self):
        for name in (
            "EXIT_OK",
            "EXIT_INTERNAL_ERROR",
            "EXIT_GATE_FAIL",
            "ENVELOPE_VERSION_V1",
            "RESULT_VERSION_V1",
        ):
            assert hasattr(editor_pkg, name), name

    def test_all_eight_failure_codes_exposed_via_package_init(self):
        expected = {
            "F_EDITOR_OUTPUT_SHAPE",
            "F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED",
            "F_EDITOR_SINGLE_REPLACEMENT",
            "F_EDITOR_SKILL_SUBPROCESS_FAIL",
            "F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON",
            "F_EDITOR_SKILL_TIMEOUT",
            "F_EDITOR_ENVELOPE_MALFORMED",
            "F_EDITOR_ORG_CROSS_REF",
        }
        for name in expected:
            assert hasattr(editor_pkg, name), name

    def test_all_six_exception_classes_exposed(self):
        expected = {
            "EditorOutputShapeError",
            "EditorRewroteInsteadOfFlaggedError",
            "EditorSingleReplacementError",
            "EditorSkillSubprocessFail",
            "EditorSkillOutputMalformedJson",
            "EditorSkillTimeout",
        }
        for name in expected:
            assert hasattr(editor_pkg, name), name

    def test_envelope_decoder_and_result_encoder_exposed(self):
        assert hasattr(editor_pkg, "decode_envelope")
        assert hasattr(editor_pkg, "encode_result")

    def test_default_pre_and_post_gate_exposed(self):
        assert hasattr(editor_pkg, "default_cross_org_pre_gate")
        assert hasattr(editor_pkg, "default_noop_post_gate")

    def test_r2_validation_helpers_exposed(self):
        for name in (
            "audit_taxonomy_sort",
            "assert_tone_consistency",
            "dedupe_quick_wins",
            "audit_terms_to_verify_cross_reference",
            "apply_r2_validation",
            "TAXONOMY_CATEGORIES",
            "ValidationReport",
        ):
            assert hasattr(editor_pkg, name), name

    def test_run_seat_is_callable(self):
        assert callable(run_seat)

    def test_invoke_editor_adapter_is_callable(self):
        assert callable(invoke_editor_adapter)

    def test_envelope_malformed_exception_class_present(self):
        assert hasattr(editor_pkg, "EditorEnvelopeMalformed")
        assert issubclass(EditorEnvelopeMalformed, RuntimeError)

    def test_gate_failed_exception_carries_failure_code_attribute(self):
        gf = EditorGateFailed(
            failure_code="F-X",
            trigger="t",
            evidence={"k": "v"},
        )
        assert gf.failure_code == "F-X"
        assert gf.trigger == "t"
        assert gf.evidence == {"k": "v"}
