"""Round-3 tests for ``pipeline.seats.judge.seat``.

Covers the subprocess entry contract: envelope decoding, exit-code
routing, gate-trip stderr emission, Google exception → exit-code
mapping, and the result encoder. Uses fully-injected E-017 seams so
tests are deterministic — no network, no subprocess, no real clock.
"""
from __future__ import annotations

import io
import json
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any, Mapping

import pytest

from pipeline.seats.judge.provider_google import (
    GoogleBYOKMissing,
    GoogleCallCallable,
    GooglePayloadCeiling,
    GoogleProviderMalformed,
    GoogleSemanticFailure,
    GoogleTransportFailure,
)
from pipeline.seats.judge.seat import (
    ENVELOPE_VERSION_V1,
    EXIT_GATE_FAIL,
    EXIT_INTERNAL_ERROR,
    EXIT_OK,
    F_JUDGE_CROSS_FAMILY_COLLISION,
    F_JUDGE_ENVELOPE_MALFORMED,
    F_JUDGE_ORG_CROSS_REF,
    F_JUDGE_RUBRIC_LOAD_FAIL,
    F_JUDGE_SCORE_ORCHESTRATION_FAIL,
    RESULT_VERSION_V1,
    JudgeEnvelope,
    JudgeEnvelopeMalformed,
    JudgeGateFailed,
    JudgeResult,
    decode_envelope,
    encode_result,
    run_seat,
)
from pipeline.seats.judge.sfr_emitter import SfrLineItem, SfrReport
from pipeline.seats.judge.types import (
    CriterionScore,
    F_JUDGE_EVIDENCE_NOT_IN_DRAFT,
    JudgeOutput,
    JudgeVerdict,
    ResponsivenessMap,
    Rubric,
    RubricCriterion,
)


# ---------------------------------------------------------------------------
# Constants + fixtures
# ---------------------------------------------------------------------------


_SHELL_HASH_128 = "a" * 128
_RFA_HASH_128 = "b" * 128
_RUBRIC_HASH_64 = "c" * 64
_FIXED_NOW = datetime(2026, 4, 30, 12, 0, tzinfo=timezone.utc)


def _make_envelope_dict(**overrides: Any) -> dict[str, Any]:
    base = {
        "envelope_version": "judge-envelope.v1",
        "run_id": "run-2026-04-30-001",
        "org_slug": "fit_farms_llc",
        "iteration_number": 0,
        "program_code": "VAPG",
        "rubric_path": "/rubrics/vapg_fy26.json",
        "rfa_content_sha3_512": _RFA_HASH_128,
        "rfa_scope_summary": "Value-Added Producer Grant FY26 — planning + working capital.",
        "scribe_provider_family": "anthropic",
        "section_drafts_blob": [
            {
                "section_name": "Project Narrative",
                "section_order": 1,
                "body_text": "FIT Farms grows gourmet mushrooms in a 50-acre cooperative.",
                "claim_evidence_map": [],
            }
        ],
        "compiled_prompt_shell_sha3_512": _SHELL_HASH_128,
        "project_context": {"applicant_name": "FIT Farms"},
        "envelope_emitted_at_utc": "2026-04-30T12:00:00+00:00",
    }
    base.update(overrides)
    return base


def _make_envelope_bytes(**overrides: Any) -> bytes:
    return json.dumps(_make_envelope_dict(**overrides)).encode("utf-8")


def _make_envelope(**overrides: Any) -> JudgeEnvelope:
    return decode_envelope(raw_bytes=_make_envelope_bytes(**overrides))


def _fixed_clock() -> datetime:
    return _FIXED_NOW


class _FakeSectionDraft:
    def __init__(
        self,
        section_name: str = "Project Narrative",
        section_order: int = 1,
        body_text: str = "FIT Farms grows gourmet mushrooms.",
    ) -> None:
        self.section_name = section_name
        self.section_order = section_order
        self.body_text = body_text
        self.claim_evidence_map: tuple = ()


def _build_rubric(
    *,
    program_code: str = "VAPG",
    funder: str = "USDA Rural Development",
    nofo_number: str = "USDA-RBCS-VAPG-2026",
    rubric_sha256: str = _RUBRIC_HASH_64,
) -> Rubric:
    crit = RubricCriterion(
        id="b",
        name="Personnel",
        max_points=20,
        scorer="review_panel",
        subcriteria=(),
        must_address=("qualifications",),
        tiers=(
            MappingProxyType({"points": 20, "description": "Strong qualifications"}),
        ),
    )
    return Rubric(
        program_code=program_code,
        funder=funder,
        nofo_number=nofo_number,
        max_score=100,
        min_score=50,
        criteria=(crit,),
        rubric_sha256=rubric_sha256,
        loaded_at_utc=_FIXED_NOW,
    )


def _build_criterion_score() -> CriterionScore:
    return CriterionScore(
        criterion_id="b",
        score=18,
        evidence_quote="FIT Farms grows gourmet mushrooms.",
        confidence=0.95,
        rationale="Strong applicant operations.",
    )


def _build_judge_verdict(rubric: Rubric) -> JudgeVerdict:
    cs = _build_criterion_score()
    jo = JudgeOutput(
        criterion_scores=(cs,),
        total_score=18,
        max_total=20,
        rubric_sha256=rubric.rubric_sha256,
        rfa_content_sha3_512=_RFA_HASH_128,
        scored_at_utc=_FIXED_NOW,
    )
    return JudgeVerdict(
        judge_output=jo,
        rubric_program_code=rubric.program_code,
        responsiveness_map=ResponsivenessMap(entries=()),
        assembled_at_utc=_FIXED_NOW,
    )


def _build_sfr_report(rubric: Rubric, verdict: JudgeVerdict) -> SfrReport:
    line = SfrLineItem(
        criterion_id="b",
        score=18,
        max_points=20,
        confidence=0.95,
        evidence_quote="FIT Farms grows gourmet mushrooms.",
        rationale="Strong applicant operations.",
    )
    return SfrReport(
        program_code=rubric.program_code,
        funder=rubric.funder,
        nofo_number=rubric.nofo_number,
        rubric_sha256=rubric.rubric_sha256,
        rfa_scope_summary="Value-Added Producer Grant FY26 — planning + working capital.",
        line_items=(line,),
        total_score=18,
        max_total=20,
        percent_score=18 / 20,
        pass_threshold=50,
        passed=False,
        mean_confidence=0.95,
    )


def _make_seat_kwargs(*, stdin_bytes: bytes | None = None) -> dict[str, Any]:
    """Build a fully-stubbed run_seat kwargs bundle. Tests override pieces."""
    rubric = _build_rubric()
    verdict = _build_judge_verdict(rubric)

    def _google_call(*, binding, compiled_prompt, org_slug):  # pragma: no cover
        raise AssertionError("default google_call should not run")

    def _rubric_loader(*, rubric_path: str) -> Rubric:
        return rubric

    def _section_draft_decoder(*, blob):
        return (_FakeSectionDraft(),)

    def _score_orchestrator(*, envelope, rubric, section_drafts, google_call):
        return verdict, "google", "gemini-2.5-pro-002"

    def _sfr_emitter(*, envelope, judge_verdict, rubric, section_drafts):
        return _build_sfr_report(rubric, judge_verdict)

    def _pre_gate(*, envelope) -> None:
        return None

    def _post_gate(*, envelope, judge_verdict, rubric, section_drafts) -> None:
        return None

    return {
        "stdin": io.BytesIO(stdin_bytes if stdin_bytes is not None else _make_envelope_bytes()),
        "stdout": io.BytesIO(),
        "stderr": io.BytesIO(),
        "clock": _fixed_clock,
        "google_call": _google_call,
        "rubric_loader": _rubric_loader,
        "section_draft_decoder": _section_draft_decoder,
        "score_orchestrator": _score_orchestrator,
        "sfr_emitter": _sfr_emitter,
        "pre_gate": _pre_gate,
        "post_gate": _post_gate,
    }


def _decode_stderr_jsonl(buf: io.BytesIO) -> list[dict[str, Any]]:
    raw = buf.getvalue().decode("utf-8")
    return [json.loads(line) for line in raw.splitlines() if line.strip()]


def _decode_stdout_json(buf: io.BytesIO) -> dict[str, Any]:
    raw = buf.getvalue().decode("utf-8")
    return json.loads(raw)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


class TestConstants:
    def test_envelope_version_v1(self):
        assert ENVELOPE_VERSION_V1 == "judge-envelope.v1"

    def test_result_version_v1(self):
        assert RESULT_VERSION_V1 == "judge-result.v1"

    def test_exit_codes(self):
        assert EXIT_OK == 0
        assert EXIT_INTERNAL_ERROR == 1
        assert EXIT_GATE_FAIL == 2

    def test_envelope_malformed_code(self):
        assert F_JUDGE_ENVELOPE_MALFORMED == "F-JUDGE-ENVELOPE-MALFORMED"

    def test_cross_family_code(self):
        assert F_JUDGE_CROSS_FAMILY_COLLISION == "F-JUDGE-CROSS-FAMILY-COLLISION"

    def test_org_cross_ref_code(self):
        assert F_JUDGE_ORG_CROSS_REF == "F-JUDGE-ORG-CROSS-REF"

    def test_rubric_load_fail_code(self):
        assert F_JUDGE_RUBRIC_LOAD_FAIL == "F-JUDGE-RUBRIC-LOAD-FAIL"

    def test_score_orchestration_fail_code(self):
        assert F_JUDGE_SCORE_ORCHESTRATION_FAIL == "F-JUDGE-SCORE-ORCHESTRATION-FAIL"


# ---------------------------------------------------------------------------
# JudgeEnvelope __post_init__ invariants
# ---------------------------------------------------------------------------


class TestJudgeEnvelopeInvariants:
    def _kw(self, **overrides: Any) -> dict[str, Any]:
        base = {
            "envelope_version": "judge-envelope.v1",
            "run_id": "r1",
            "org_slug": "fit",
            "iteration_number": 0,
            "program_code": "VAPG",
            "rubric_path": "/r.json",
            "rfa_content_sha3_512": _RFA_HASH_128,
            "rfa_scope_summary": "scope",
            "scribe_provider_family": "anthropic",
            "section_drafts_blob": ({"x": 1},),
            "compiled_prompt_shell_sha3_512": _SHELL_HASH_128,
            "project_context": {"a": 1},
            "envelope_emitted_at_utc": _FIXED_NOW,
        }
        base.update(overrides)
        return base

    def test_happy_path_constructs(self):
        env = JudgeEnvelope(**self._kw())
        assert env.envelope_version == "judge-envelope.v1"
        assert isinstance(env.project_context, MappingProxyType)

    def test_wrong_version_rejected(self):
        with pytest.raises(JudgeEnvelopeMalformed):
            JudgeEnvelope(**self._kw(envelope_version="judge-envelope.v0"))

    def test_empty_run_id_rejected(self):
        with pytest.raises(JudgeEnvelopeMalformed):
            JudgeEnvelope(**self._kw(run_id="   "))

    def test_empty_org_slug_rejected(self):
        with pytest.raises(JudgeEnvelopeMalformed):
            JudgeEnvelope(**self._kw(org_slug=""))

    def test_negative_iteration_rejected(self):
        with pytest.raises(JudgeEnvelopeMalformed):
            JudgeEnvelope(**self._kw(iteration_number=-1))

    def test_blank_program_code_rejected(self):
        with pytest.raises(JudgeEnvelopeMalformed):
            JudgeEnvelope(**self._kw(program_code=" "))

    def test_blank_rubric_path_rejected(self):
        with pytest.raises(JudgeEnvelopeMalformed):
            JudgeEnvelope(**self._kw(rubric_path=""))

    def test_short_rfa_hash_rejected(self):
        with pytest.raises(JudgeEnvelopeMalformed):
            JudgeEnvelope(**self._kw(rfa_content_sha3_512="abc"))

    def test_uppercase_rfa_hash_rejected(self):
        with pytest.raises(JudgeEnvelopeMalformed):
            JudgeEnvelope(**self._kw(rfa_content_sha3_512="A" * 128))

    def test_blank_rfa_scope_rejected(self):
        with pytest.raises(JudgeEnvelopeMalformed):
            JudgeEnvelope(**self._kw(rfa_scope_summary="   "))

    def test_blank_scribe_family_rejected(self):
        with pytest.raises(JudgeEnvelopeMalformed):
            JudgeEnvelope(**self._kw(scribe_provider_family="  "))

    def test_empty_drafts_blob_rejected(self):
        with pytest.raises(JudgeEnvelopeMalformed):
            JudgeEnvelope(**self._kw(section_drafts_blob=()))

    def test_short_compiled_shell_hash_rejected(self):
        with pytest.raises(JudgeEnvelopeMalformed):
            JudgeEnvelope(**self._kw(compiled_prompt_shell_sha3_512="aaa"))

    def test_uppercase_compiled_shell_hash_rejected(self):
        with pytest.raises(JudgeEnvelopeMalformed):
            JudgeEnvelope(**self._kw(compiled_prompt_shell_sha3_512="A" * 128))

    def test_naive_datetime_rejected(self):
        with pytest.raises(JudgeEnvelopeMalformed):
            JudgeEnvelope(
                **self._kw(envelope_emitted_at_utc=datetime(2026, 4, 30, 12, 0))
            )


# ---------------------------------------------------------------------------
# decode_envelope
# ---------------------------------------------------------------------------


class TestDecodeEnvelope:
    def test_happy_path(self):
        env = decode_envelope(raw_bytes=_make_envelope_bytes())
        assert env.envelope_version == "judge-envelope.v1"
        assert env.run_id == "run-2026-04-30-001"
        assert env.org_slug == "fit_farms_llc"

    def test_empty_stdin(self):
        with pytest.raises(JudgeEnvelopeMalformed, match="stdin empty"):
            decode_envelope(raw_bytes=b"")

    def test_invalid_utf8(self):
        with pytest.raises(JudgeEnvelopeMalformed, match="not UTF-8"):
            decode_envelope(raw_bytes=b"\xff\xfe\xfd")

    def test_invalid_json(self):
        with pytest.raises(JudgeEnvelopeMalformed, match="not JSON"):
            decode_envelope(raw_bytes=b"{not json")

    def test_top_level_array(self):
        with pytest.raises(JudgeEnvelopeMalformed, match="must be object"):
            decode_envelope(raw_bytes=b"[]")

    def test_wrong_envelope_version(self):
        bad = _make_envelope_dict(envelope_version="other")
        with pytest.raises(JudgeEnvelopeMalformed, match="envelope_version"):
            decode_envelope(raw_bytes=json.dumps(bad).encode("utf-8"))

    def test_missing_keys(self):
        bad = _make_envelope_dict()
        del bad["program_code"]
        with pytest.raises(JudgeEnvelopeMalformed, match="missing keys"):
            decode_envelope(raw_bytes=json.dumps(bad).encode("utf-8"))

    def test_emitted_at_not_string(self):
        bad = _make_envelope_dict(envelope_emitted_at_utc=12345)
        with pytest.raises(JudgeEnvelopeMalformed, match="ISO-8601 string"):
            decode_envelope(raw_bytes=json.dumps(bad).encode("utf-8"))

    def test_emitted_at_not_iso(self):
        bad = _make_envelope_dict(envelope_emitted_at_utc="not-a-date")
        with pytest.raises(JudgeEnvelopeMalformed, match="ISO-8601"):
            decode_envelope(raw_bytes=json.dumps(bad).encode("utf-8"))

    def test_project_context_not_mapping(self):
        bad = _make_envelope_dict(project_context=[1, 2, 3])
        with pytest.raises(JudgeEnvelopeMalformed, match="project_context"):
            decode_envelope(raw_bytes=json.dumps(bad).encode("utf-8"))

    def test_drafts_blob_not_array(self):
        bad = _make_envelope_dict(section_drafts_blob={"x": 1})
        with pytest.raises(JudgeEnvelopeMalformed, match="must be array"):
            decode_envelope(raw_bytes=json.dumps(bad).encode("utf-8"))

    def test_drafts_blob_with_non_object_entry(self):
        bad = _make_envelope_dict(section_drafts_blob=[{"a": 1}, 7])
        with pytest.raises(JudgeEnvelopeMalformed, match="must.*be objects"):
            decode_envelope(raw_bytes=json.dumps(bad).encode("utf-8"))


# ---------------------------------------------------------------------------
# encode_result
# ---------------------------------------------------------------------------


class TestEncodeResult:
    def _build_result(self) -> JudgeResult:
        rubric = _build_rubric()
        verdict = _build_judge_verdict(rubric)
        sfr = _build_sfr_report(rubric, verdict)
        return JudgeResult(
            result_version="judge-result.v1",
            run_id="r1",
            org_slug="fit",
            iteration_number=0,
            judge_verdict=verdict,
            sfr_report=sfr,
            sfr_text="SFR rendered",
            compiled_prompt_shell_sha3_512=_SHELL_HASH_128,
            provider_landed_family="google",
            provider_landed_model_id="gemini-2.5-pro-002",
            seat_emitted_at_utc=_FIXED_NOW,
        )

    def test_round_trip_keys(self):
        r = self._build_result()
        out = encode_result(r)
        assert out.endswith(b"\n")
        parsed = json.loads(out.decode("utf-8"))
        assert parsed["result_version"] == "judge-result.v1"
        assert parsed["run_id"] == "r1"
        assert parsed["judge_verdict"]["judge_output"]["total_score"] == 18
        assert parsed["sfr_report"]["pass_threshold"] == 50

    def test_canonical_form_sorted_keys(self):
        r = self._build_result()
        out = encode_result(r).decode("utf-8")
        assert "judge_verdict" in out
        # sort_keys=True ⇒ alphabetical at top level
        first_keys = list(json.loads(out).keys())
        assert first_keys == sorted(first_keys)

    def test_wrong_version_rejected(self):
        rubric = _build_rubric()
        verdict = _build_judge_verdict(rubric)
        sfr = _build_sfr_report(rubric, verdict)
        with pytest.raises(ValueError, match="judge-result.v1"):
            JudgeResult(
                result_version="other",
                run_id="r1",
                org_slug="fit",
                iteration_number=0,
                judge_verdict=verdict,
                sfr_report=sfr,
                sfr_text="SFR rendered",
                compiled_prompt_shell_sha3_512=_SHELL_HASH_128,
                provider_landed_family="google",
                provider_landed_model_id="gemini-2.5-pro-002",
                seat_emitted_at_utc=_FIXED_NOW,
            )

    def test_blank_provider_family_rejected(self):
        rubric = _build_rubric()
        verdict = _build_judge_verdict(rubric)
        sfr = _build_sfr_report(rubric, verdict)
        with pytest.raises(ValueError, match="provider_landed_family"):
            JudgeResult(
                result_version="judge-result.v1",
                run_id="r1",
                org_slug="fit",
                iteration_number=0,
                judge_verdict=verdict,
                sfr_report=sfr,
                sfr_text="SFR rendered",
                compiled_prompt_shell_sha3_512=_SHELL_HASH_128,
                provider_landed_family="",
                provider_landed_model_id="gemini-2.5-pro-002",
                seat_emitted_at_utc=_FIXED_NOW,
            )

    def test_blank_provider_model_id_rejected(self):
        rubric = _build_rubric()
        verdict = _build_judge_verdict(rubric)
        sfr = _build_sfr_report(rubric, verdict)
        with pytest.raises(ValueError, match="provider_landed_model_id"):
            JudgeResult(
                result_version="judge-result.v1",
                run_id="r1",
                org_slug="fit",
                iteration_number=0,
                judge_verdict=verdict,
                sfr_report=sfr,
                sfr_text="SFR rendered",
                compiled_prompt_shell_sha3_512=_SHELL_HASH_128,
                provider_landed_family="google",
                provider_landed_model_id="",
                seat_emitted_at_utc=_FIXED_NOW,
            )

    def test_naive_emitted_at_rejected(self):
        rubric = _build_rubric()
        verdict = _build_judge_verdict(rubric)
        sfr = _build_sfr_report(rubric, verdict)
        with pytest.raises(ValueError, match="seat_emitted_at_utc"):
            JudgeResult(
                result_version="judge-result.v1",
                run_id="r1",
                org_slug="fit",
                iteration_number=0,
                judge_verdict=verdict,
                sfr_report=sfr,
                sfr_text="SFR rendered",
                compiled_prompt_shell_sha3_512=_SHELL_HASH_128,
                provider_landed_family="google",
                provider_landed_model_id="gemini-2.5-pro-002",
                seat_emitted_at_utc=datetime(2026, 4, 30, 12, 0),
            )

    def test_short_shell_hash_rejected(self):
        rubric = _build_rubric()
        verdict = _build_judge_verdict(rubric)
        sfr = _build_sfr_report(rubric, verdict)
        with pytest.raises(ValueError, match="compiled_prompt_shell_sha3_512"):
            JudgeResult(
                result_version="judge-result.v1",
                run_id="r1",
                org_slug="fit",
                iteration_number=0,
                judge_verdict=verdict,
                sfr_report=sfr,
                sfr_text="SFR rendered",
                compiled_prompt_shell_sha3_512="abc",
                provider_landed_family="google",
                provider_landed_model_id="gemini-2.5-pro-002",
                seat_emitted_at_utc=_FIXED_NOW,
            )

    def test_blank_sfr_text_rejected(self):
        rubric = _build_rubric()
        verdict = _build_judge_verdict(rubric)
        sfr = _build_sfr_report(rubric, verdict)
        with pytest.raises(ValueError, match="sfr_text"):
            JudgeResult(
                result_version="judge-result.v1",
                run_id="r1",
                org_slug="fit",
                iteration_number=0,
                judge_verdict=verdict,
                sfr_report=sfr,
                sfr_text="   ",
                compiled_prompt_shell_sha3_512=_SHELL_HASH_128,
                provider_landed_family="google",
                provider_landed_model_id="gemini-2.5-pro-002",
                seat_emitted_at_utc=_FIXED_NOW,
            )

    def test_negative_iteration_rejected(self):
        rubric = _build_rubric()
        verdict = _build_judge_verdict(rubric)
        sfr = _build_sfr_report(rubric, verdict)
        with pytest.raises(ValueError, match="iteration_number"):
            JudgeResult(
                result_version="judge-result.v1",
                run_id="r1",
                org_slug="fit",
                iteration_number=-1,
                judge_verdict=verdict,
                sfr_report=sfr,
                sfr_text="SFR rendered",
                compiled_prompt_shell_sha3_512=_SHELL_HASH_128,
                provider_landed_family="google",
                provider_landed_model_id="gemini-2.5-pro-002",
                seat_emitted_at_utc=_FIXED_NOW,
            )


# ---------------------------------------------------------------------------
# run_seat happy path + envelope-level failures
# ---------------------------------------------------------------------------


class TestRunSeatHappyPath:
    def test_returns_zero(self):
        kw = _make_seat_kwargs()
        rc = run_seat(**kw)
        assert rc == EXIT_OK

    def test_stdout_carries_judge_result(self):
        kw = _make_seat_kwargs()
        run_seat(**kw)
        out = _decode_stdout_json(kw["stdout"])
        assert out["result_version"] == "judge-result.v1"
        assert out["run_id"] == "run-2026-04-30-001"
        assert out["provider_landed_family"] == "google"
        assert out["provider_landed_model_id"] == "gemini-2.5-pro-002"
        assert "judge_verdict" in out
        assert "sfr_report" in out
        assert out["sfr_text"]  # non-empty SFR text

    def test_stderr_empty_on_happy_path(self):
        kw = _make_seat_kwargs()
        run_seat(**kw)
        assert kw["stderr"].getvalue() == b""


class TestRunSeatEnvelopeFailures:
    def test_empty_stdin_exit_2(self):
        kw = _make_seat_kwargs(stdin_bytes=b"")
        rc = run_seat(**kw)
        assert rc == EXIT_GATE_FAIL
        rows = _decode_stderr_jsonl(kw["stderr"])
        assert len(rows) == 1
        assert rows[0]["failure_code"] == F_JUDGE_ENVELOPE_MALFORMED

    def test_invalid_json_exit_2(self):
        kw = _make_seat_kwargs(stdin_bytes=b"{not json")
        rc = run_seat(**kw)
        assert rc == EXIT_GATE_FAIL
        rows = _decode_stderr_jsonl(kw["stderr"])
        assert rows[0]["failure_code"] == F_JUDGE_ENVELOPE_MALFORMED

    def test_missing_required_key_exit_2(self):
        bad = _make_envelope_dict()
        del bad["scribe_provider_family"]
        kw = _make_seat_kwargs(stdin_bytes=json.dumps(bad).encode("utf-8"))
        rc = run_seat(**kw)
        assert rc == EXIT_GATE_FAIL


# ---------------------------------------------------------------------------
# run_seat — pre-gate failures
# ---------------------------------------------------------------------------


class TestRunSeatPreGate:
    def test_pre_gate_judge_gate_failed_exit_2(self):
        kw = _make_seat_kwargs()

        def _bad_pre(*, envelope):
            raise JudgeGateFailed(
                failure_code=F_JUDGE_CROSS_FAMILY_COLLISION,
                trigger="cross_family",
                evidence={"scribe_provider_family": "google"},
            )

        kw["pre_gate"] = _bad_pre
        rc = run_seat(**kw)
        assert rc == EXIT_GATE_FAIL
        rows = _decode_stderr_jsonl(kw["stderr"])
        assert rows[0]["failure_code"] == F_JUDGE_CROSS_FAMILY_COLLISION
        assert rows[0]["trigger"] == "cross_family"

    def test_pre_gate_unhandled_exception_exit_1(self):
        kw = _make_seat_kwargs()

        def _bad_pre(*, envelope):
            raise RuntimeError("unexpected")

        kw["pre_gate"] = _bad_pre
        rc = run_seat(**kw)
        assert rc == EXIT_INTERNAL_ERROR
        msg = kw["stderr"].getvalue().decode("utf-8")
        assert "pre_gate raised" in msg
        assert "RuntimeError" in msg


# ---------------------------------------------------------------------------
# run_seat — rubric loader failures
# ---------------------------------------------------------------------------


class TestRunSeatRubricLoader:
    def test_rubric_loader_judge_gate_failed_exit_2(self):
        kw = _make_seat_kwargs()

        def _bad_loader(*, rubric_path):
            raise JudgeGateFailed(
                failure_code="F-JUDGE-RUBRIC-MALFORMED",
                trigger="bad_rubric",
                evidence={"path": rubric_path},
            )

        kw["rubric_loader"] = _bad_loader
        rc = run_seat(**kw)
        assert rc == EXIT_GATE_FAIL
        rows = _decode_stderr_jsonl(kw["stderr"])
        assert rows[0]["failure_code"] == "F-JUDGE-RUBRIC-MALFORMED"

    def test_rubric_loader_unhandled_exception_exit_2(self):
        kw = _make_seat_kwargs()

        def _bad_loader(*, rubric_path):
            raise FileNotFoundError("rubric missing")

        kw["rubric_loader"] = _bad_loader
        rc = run_seat(**kw)
        assert rc == EXIT_GATE_FAIL
        rows = _decode_stderr_jsonl(kw["stderr"])
        assert rows[0]["failure_code"] == F_JUDGE_RUBRIC_LOAD_FAIL
        assert rows[0]["evidence"]["exception_class"] == "FileNotFoundError"


# ---------------------------------------------------------------------------
# run_seat — section_draft_decoder failures
# ---------------------------------------------------------------------------


class TestRunSeatSectionDraftDecoder:
    def test_decoder_judge_gate_failed_exit_2(self):
        kw = _make_seat_kwargs()

        def _bad_decoder(*, blob):
            raise JudgeGateFailed(
                failure_code="F-JUDGE-DRAFT-DECODE-FAIL",
                trigger="bad_blob",
                evidence={},
            )

        kw["section_draft_decoder"] = _bad_decoder
        rc = run_seat(**kw)
        assert rc == EXIT_GATE_FAIL
        rows = _decode_stderr_jsonl(kw["stderr"])
        assert rows[0]["failure_code"] == "F-JUDGE-DRAFT-DECODE-FAIL"

    def test_decoder_unhandled_exception_exit_1(self):
        kw = _make_seat_kwargs()

        def _bad_decoder(*, blob):
            raise RuntimeError("decoder bug")

        kw["section_draft_decoder"] = _bad_decoder
        rc = run_seat(**kw)
        assert rc == EXIT_INTERNAL_ERROR
        msg = kw["stderr"].getvalue().decode("utf-8")
        assert "section_draft_decoder" in msg
        assert "RuntimeError" in msg


# ---------------------------------------------------------------------------
# run_seat — score_orchestrator failures (Google exception mapping)
# ---------------------------------------------------------------------------


class TestRunSeatScoreOrchestrator:
    @pytest.mark.parametrize(
        "exc_class,code",
        [
            (GoogleBYOKMissing, "F-JUDGE-BYOK-MISSING"),
            (GooglePayloadCeiling, "F-JUDGE-PAYLOAD-CEILING"),
            (GoogleTransportFailure, "F-JUDGE-TRANSPORT-FAILURE"),
            (GoogleSemanticFailure, "F-JUDGE-SEMANTIC-FAILURE"),
            (GoogleProviderMalformed, "F-JUDGE-PROVIDER-MALFORMED"),
        ],
    )
    def test_google_exception_maps_to_failure_code(self, exc_class, code):
        kw = _make_seat_kwargs()

        def _bad_orch(*, envelope, rubric, section_drafts, google_call):
            raise exc_class("simulated failure")

        kw["score_orchestrator"] = _bad_orch
        rc = run_seat(**kw)
        assert rc == EXIT_GATE_FAIL
        rows = _decode_stderr_jsonl(kw["stderr"])
        assert rows[0]["failure_code"] == code
        assert rows[0]["evidence"]["exception_class"] == exc_class.__name__

    def test_orchestrator_judge_gate_failed_exit_2(self):
        kw = _make_seat_kwargs()

        def _bad_orch(*, envelope, rubric, section_drafts, google_call):
            raise JudgeGateFailed(
                failure_code=F_JUDGE_EVIDENCE_NOT_IN_DRAFT,
                trigger="evidence_not_substring",
                evidence={"unsourced": ["b"]},
            )

        kw["score_orchestrator"] = _bad_orch
        rc = run_seat(**kw)
        assert rc == EXIT_GATE_FAIL
        rows = _decode_stderr_jsonl(kw["stderr"])
        assert rows[0]["failure_code"] == F_JUDGE_EVIDENCE_NOT_IN_DRAFT

    def test_orchestrator_unhandled_exception_exit_2(self):
        kw = _make_seat_kwargs()

        def _bad_orch(*, envelope, rubric, section_drafts, google_call):
            raise ValueError("bug class")

        kw["score_orchestrator"] = _bad_orch
        rc = run_seat(**kw)
        assert rc == EXIT_GATE_FAIL
        rows = _decode_stderr_jsonl(kw["stderr"])
        assert rows[0]["failure_code"] == F_JUDGE_SCORE_ORCHESTRATION_FAIL
        assert rows[0]["evidence"]["exception_class"] == "ValueError"

    def test_byok_evidence_includes_org_slug(self):
        kw = _make_seat_kwargs()

        def _bad_orch(*, envelope, rubric, section_drafts, google_call):
            raise GoogleBYOKMissing("byok absent")

        kw["score_orchestrator"] = _bad_orch
        rc = run_seat(**kw)
        assert rc == EXIT_GATE_FAIL
        rows = _decode_stderr_jsonl(kw["stderr"])
        assert rows[0]["evidence"]["org_slug"] == "fit_farms_llc"


# ---------------------------------------------------------------------------
# run_seat — sfr_emitter failures
# ---------------------------------------------------------------------------


class TestRunSeatSfrEmitter:
    def test_sfr_emitter_judge_gate_failed_exit_2(self):
        kw = _make_seat_kwargs()

        def _bad_sfr(*, envelope, judge_verdict, rubric, section_drafts):
            raise JudgeGateFailed(
                failure_code="F-JUDGE-SFR-EMIT-FAIL",
                trigger="sfr_validation",
                evidence={},
            )

        kw["sfr_emitter"] = _bad_sfr
        rc = run_seat(**kw)
        assert rc == EXIT_GATE_FAIL
        rows = _decode_stderr_jsonl(kw["stderr"])
        assert rows[0]["failure_code"] == "F-JUDGE-SFR-EMIT-FAIL"

    def test_sfr_emitter_unhandled_exception_exit_1(self):
        kw = _make_seat_kwargs()

        def _bad_sfr(*, envelope, judge_verdict, rubric, section_drafts):
            raise RuntimeError("sfr exploded")

        kw["sfr_emitter"] = _bad_sfr
        rc = run_seat(**kw)
        assert rc == EXIT_INTERNAL_ERROR
        msg = kw["stderr"].getvalue().decode("utf-8")
        assert "sfr_emitter" in msg
        assert "RuntimeError" in msg


# ---------------------------------------------------------------------------
# run_seat — post_gate failures
# ---------------------------------------------------------------------------


class TestRunSeatPostGate:
    def test_post_gate_judge_gate_failed_exit_2(self):
        kw = _make_seat_kwargs()

        def _bad_post(*, envelope, judge_verdict, rubric, section_drafts):
            raise JudgeGateFailed(
                failure_code=F_JUDGE_EVIDENCE_NOT_IN_DRAFT,
                trigger="post_gate_law5",
                evidence={"unsourced": ["b"]},
            )

        kw["post_gate"] = _bad_post
        rc = run_seat(**kw)
        assert rc == EXIT_GATE_FAIL
        rows = _decode_stderr_jsonl(kw["stderr"])
        assert rows[0]["failure_code"] == F_JUDGE_EVIDENCE_NOT_IN_DRAFT

    def test_post_gate_unhandled_exception_exit_1(self):
        kw = _make_seat_kwargs()

        def _bad_post(*, envelope, judge_verdict, rubric, section_drafts):
            raise RuntimeError("post bug")

        kw["post_gate"] = _bad_post
        rc = run_seat(**kw)
        assert rc == EXIT_INTERNAL_ERROR
        msg = kw["stderr"].getvalue().decode("utf-8")
        assert "post_gate raised" in msg


# ---------------------------------------------------------------------------
# JudgeGateFailed exception shape
# ---------------------------------------------------------------------------


class TestJudgeGateFailed:
    def test_carries_failure_code_trigger_evidence(self):
        exc = JudgeGateFailed(
            failure_code="F-X", trigger="t", evidence={"a": 1}
        )
        assert exc.failure_code == "F-X"
        assert exc.trigger == "t"
        assert exc.evidence == {"a": 1}
        assert "F-X: t" in str(exc)

    def test_evidence_is_copied_dict(self):
        original = {"a": 1}
        exc = JudgeGateFailed(
            failure_code="F-X", trigger="t", evidence=original
        )
        original["a"] = 2
        # Implementation copies; mutating the source must not bleed in.
        assert exc.evidence == {"a": 1}
