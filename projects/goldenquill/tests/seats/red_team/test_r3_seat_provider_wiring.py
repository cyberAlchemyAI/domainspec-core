"""§10 Red Team R3 — provider_groq + seat.run_seat + logician_wiring tests.

Round 3 covers:
- :mod:`provider_groq` — call_groq with deterministic OutboundCallable stub;
  HTTP error mapping (auth/rate-limit/transport/parse failure codes).
- :mod:`logician_wiring` — run_pre_gate + run_post_gate orchestration;
  3-way cross-family distinct check; council-split + anchor-suspected
  detection routing.
- :mod:`seat` — run_seat end-to-end with deterministic stubs (no real LLM
  call). Exit-code routing (PASS / PRE / PROVIDER / COMPOSER / POST /
  COUNCIL_SPLIT).

Production HTTP is `# pragma: no cover` (real network not exercised at
LOCK time per Judge R3 self-LOCK basis).

Stub-shape note (CC-007 §4 v2.x.6 fixture-migration sweep, 2026-05-16): the
prior `_StubHTTPCaller` / `_RaisingHTTPCaller` Protocol shape (dict body +
str response) was retired in favor of unified ``OutboundCallable`` shape
(bytes body + bytes response) — the same shape ``call_groq`` consumes in
production via ``enforce_outbound_boundary``. Test stubs now match the
production wire-up Protocol byte-for-byte; dual-path support in
``call_groq`` is collapsed.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest


# ---------------------------------------------------------------------------
# Stubs
# ---------------------------------------------------------------------------


class _StubOutboundCallable:
    """Deterministic OutboundCallable stub. Returns canned (status, body_bytes).

    Matches the production ``OutboundCallable`` Protocol from
    ``pipeline.orchestrator.provider_boundary``: keyword-only
    ``(url, headers, body: bytes, timeout_seconds: float)`` →
    ``(status_code: int, response_bytes: bytes)``.
    """

    def __init__(self, status: int, body: bytes | str) -> None:
        self._status = status
        # Accept str for ergonomic test-fixture construction; encode once.
        self._body = body.encode("utf-8") if isinstance(body, str) else body
        self.calls: list = []

    def __call__(self, *, url, headers, body, timeout_seconds):
        self.calls.append((url, headers, body, timeout_seconds))
        return (self._status, self._body)


class _RaisingOutboundCallable:
    """OutboundCallable that always raises — simulates transport failure."""

    def __init__(self, exc_type=ConnectionError, msg="connection refused") -> None:
        self._exc_type = exc_type
        self._msg = msg

    def __call__(self, *, url, headers, body, timeout_seconds):
        raise self._exc_type(self._msg)


class _StubFamilyResolver:
    """FamilyResolver stub backed by a dict."""

    def __init__(self, mapping: dict) -> None:
        self._mapping = mapping

    def resolve(self, *, seat: str) -> str:
        if seat not in self._mapping:
            raise KeyError(seat)
        return self._mapping[seat]


class _StubClock:
    def __init__(self, dt: datetime) -> None:
        self._dt = dt

    def now_utc(self) -> datetime:
        return self._dt


def _ok_groq_response_body() -> str:
    """Return a Groq-shaped success response body."""
    return json.dumps(
        {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "total_score": 12,
                                "recommendation": "marginal",
                                "criteria": [
                                    {
                                        "id": "need",
                                        "name": "Need",
                                        "max_points": 15,
                                        "score": 12,
                                        "tier_matched": "strong evidence",
                                        "evidence": "organic mango buyers exceed supply",
                                        "missing": ["LOIs"],
                                        "notes": "solid",
                                    }
                                ],
                                "attack_memo": {
                                    "top_weaknesses": [
                                        {
                                            "severity": "medium",
                                            "claim": "Paragraph 3 asserts demand without LOIs",
                                            "why_it_fails": "no buyer evidence",
                                            "what_a_reviewer_would_say": "Where are the LOIs?",
                                            "fix_hint": "Add 3 LOIs",
                                        }
                                    ],
                                    "unsupported_assertions": [],
                                    "dialect_mismatches": [],
                                    "boundary_drift": [],
                                    "overall_verdict": "Marginal feasibility.",
                                },
                            }
                        )
                    }
                }
            ]
        }
    )


# ---------------------------------------------------------------------------
# provider_groq
# ---------------------------------------------------------------------------


class TestCallGroq:
    def test_success_path(self) -> None:
        from pipeline.seats.red_team.provider_groq import (
            call_groq,
            extract_message_content,
            extract_json_from_content,
        )

        stub = _StubOutboundCallable(200, _ok_groq_response_body())
        result = call_groq(
            http_post=stub,
            api_key="test-key",
            system_prompt="sys",
            user_prompt="user",
        )
        assert result.failure_code is None
        content = extract_message_content(result)
        assert content is not None
        parsed = extract_json_from_content(content)
        assert parsed["total_score"] == 12

    def test_empty_api_key_returns_auth_fail(self) -> None:
        from pipeline.seats.red_team.provider_groq import (
            F_RT_PROVIDER_AUTH_FAIL,
            call_groq,
        )

        stub = _StubOutboundCallable(200, "{}")
        result = call_groq(
            http_post=stub, api_key="", system_prompt="s", user_prompt="u"
        )
        assert result.failure_code == F_RT_PROVIDER_AUTH_FAIL

    def test_401_returns_auth_fail(self) -> None:
        from pipeline.seats.red_team.provider_groq import (
            F_RT_PROVIDER_AUTH_FAIL,
            call_groq,
        )

        stub = _StubOutboundCallable(401, '{"error":"unauthorized"}')
        result = call_groq(
            http_post=stub, api_key="bad", system_prompt="s", user_prompt="u"
        )
        assert result.failure_code == F_RT_PROVIDER_AUTH_FAIL

    def test_429_returns_rate_limited(self) -> None:
        from pipeline.seats.red_team.provider_groq import (
            F_RT_PROVIDER_RATE_LIMITED,
            call_groq,
        )

        stub = _StubOutboundCallable(429, '{"error":"rate limit"}')
        result = call_groq(
            http_post=stub, api_key="ok", system_prompt="s", user_prompt="u"
        )
        assert result.failure_code == F_RT_PROVIDER_RATE_LIMITED

    def test_500_returns_transport_fail(self) -> None:
        from pipeline.seats.red_team.provider_groq import (
            F_RT_PROVIDER_TRANSPORT_FAIL,
            call_groq,
        )

        stub = _StubOutboundCallable(500, "internal server error")
        result = call_groq(
            http_post=stub, api_key="ok", system_prompt="s", user_prompt="u"
        )
        assert result.failure_code == F_RT_PROVIDER_TRANSPORT_FAIL

    def test_unexpected_status_returns_transport_fail(self) -> None:
        from pipeline.seats.red_team.provider_groq import (
            F_RT_PROVIDER_TRANSPORT_FAIL,
            call_groq,
        )

        stub = _StubOutboundCallable(418, "I'm a teapot")
        result = call_groq(
            http_post=stub, api_key="ok", system_prompt="s", user_prompt="u"
        )
        assert result.failure_code == F_RT_PROVIDER_TRANSPORT_FAIL

    def test_caller_exception_returns_transport_fail(self) -> None:
        from pipeline.seats.red_team.provider_groq import (
            F_RT_PROVIDER_TRANSPORT_FAIL,
            call_groq,
        )

        result = call_groq(
            http_post=_RaisingOutboundCallable(),
            api_key="ok",
            system_prompt="s",
            user_prompt="u",
        )
        assert result.failure_code == F_RT_PROVIDER_TRANSPORT_FAIL

    def test_malformed_json_returns_parse_fail(self) -> None:
        from pipeline.seats.red_team.provider_groq import (
            F_RT_PROVIDER_PARSE_FAIL,
            call_groq,
        )

        stub = _StubOutboundCallable(200, "not valid json {{{")
        result = call_groq(
            http_post=stub, api_key="ok", system_prompt="s", user_prompt="u"
        )
        assert result.failure_code == F_RT_PROVIDER_PARSE_FAIL


class TestExtractHelpers:
    def test_extract_message_content_ok(self) -> None:
        from pipeline.seats.red_team.provider_groq import (
            GroqProviderResult,
            extract_message_content,
        )

        r = GroqProviderResult(
            status_code=200,
            raw_text="x",
            parsed={"choices": [{"message": {"content": "hi"}}]},
            failure_code=None,
            failure_detail=None,
        )
        assert extract_message_content(r) == "hi"

    def test_extract_message_content_none_on_failure(self) -> None:
        from pipeline.seats.red_team.provider_groq import (
            F_RT_PROVIDER_AUTH_FAIL,
            GroqProviderResult,
            extract_message_content,
        )

        r = GroqProviderResult(
            status_code=401,
            raw_text="x",
            parsed={},
            failure_code=F_RT_PROVIDER_AUTH_FAIL,
            failure_detail="bad key",
        )
        assert extract_message_content(r) is None

    def test_extract_json_strips_fences(self) -> None:
        from pipeline.seats.red_team.provider_groq import extract_json_from_content

        wrapped = '```json\n{"a": 1}\n```'
        assert extract_json_from_content(wrapped) == {"a": 1}

    def test_extract_json_with_trailing_prose(self) -> None:
        from pipeline.seats.red_team.provider_groq import extract_json_from_content

        s = '{"a": 1, "b": 2}\n\nThis is some commentary.'
        assert extract_json_from_content(s) == {"a": 1, "b": 2}

    def test_extract_json_returns_none_on_no_brace(self) -> None:
        from pipeline.seats.red_team.provider_groq import extract_json_from_content

        assert extract_json_from_content("just text no brace") is None

    def test_extract_json_returns_none_on_empty(self) -> None:
        from pipeline.seats.red_team.provider_groq import extract_json_from_content

        assert extract_json_from_content("") is None


# ---------------------------------------------------------------------------
# logician_wiring — run_pre_gate
# ---------------------------------------------------------------------------


def _make_input_bundle(
    *,
    run_id: str = "run-1",
    rubric_hash: str = "h" * 64,
    judge_run_id: str | None = "run-1",
    judge_rubric_hash: str | None = None,
    funder_dialect: str = "conservative",
):
    from pipeline.seats.red_team.types import RedTeamInput

    if judge_rubric_hash is None:
        judge_rubric_hash = rubric_hash

    class FakeSD:
        def __init__(self, body: str = "the draft body for the proposal") -> None:
            self.section_name = "p"
            self.section_order = 1
            self.body_text = body
            self.claim_evidence_map: tuple = ()

    class FakeJV:
        def __init__(self):
            self.run_id = judge_run_id
            self.rubric_hash = judge_rubric_hash
            self.total_score = 85
            self.max_score = 100
            self.recommendation = "competitive"
            self.overall_notes = "n"

    class FakeRubric:
        rubric_id = "vapg"
        content_hash = rubric_hash
        max_score = 100
        criteria = ()

    return RedTeamInput(
        run_id=run_id,
        section_drafts=(
            FakeSD(
                body="organic mango buyers exceed supply in the region. "
                "Paragraph 3 asserts demand without LOIs as central risk."
            ),
        ),
        claim_evidence_map=(),
        rubric=FakeRubric(),
        judge_verdict=FakeJV() if judge_run_id is not None else None,
        funder_dialect=funder_dialect,  # type: ignore[arg-type]
        admin_risk_register_snapshot=object(),
        prepared_at_utc=datetime.now(tz=timezone.utc),
    )


class TestRunPreGate:
    def test_clean_pass_3way_distinct(self) -> None:
        from pipeline.seats.red_team.logician_wiring import run_pre_gate

        ib = _make_input_bundle(rubric_hash="a" * 64)
        fr = _StubFamilyResolver(
            {"scribe": "Anthropic", "judge": "Google", "red_team": "OpenAI-OSS"}
        )
        compiled = (
            "Judge's scoring is context, not authority. "
            + "FILLER " * 200
            + "Judge's scoring is context, not authority."
        )
        result = run_pre_gate(
            input_bundle=ib,
            family_resolver=fr,
            session_rubric_hash="a" * 64,
            compiled_prompt=compiled,
        )
        assert result.success is True
        assert result.failure_codes == ()

    def test_red_team_collides_with_scribe(self) -> None:
        from pipeline.seats.red_team.logician_wiring import run_pre_gate
        from pipeline.seats.red_team.types import F_RT_FAMILY_OVERLAP

        ib = _make_input_bundle(rubric_hash="a" * 64)
        fr = _StubFamilyResolver(
            {"scribe": "Anthropic", "judge": "Google", "red_team": "Anthropic"}
        )
        compiled = (
            "Judge's scoring is context, not authority. "
            + "FILLER " * 200
            + "Judge's scoring is context, not authority."
        )
        result = run_pre_gate(
            input_bundle=ib,
            family_resolver=fr,
            session_rubric_hash="a" * 64,
            compiled_prompt=compiled,
        )
        assert result.success is False
        assert F_RT_FAMILY_OVERLAP in result.failure_codes
        assert any("Scribe" in d for d in result.failure_details)

    def test_red_team_collides_with_judge(self) -> None:
        from pipeline.seats.red_team.logician_wiring import run_pre_gate
        from pipeline.seats.red_team.types import F_RT_FAMILY_OVERLAP

        ib = _make_input_bundle(rubric_hash="a" * 64)
        fr = _StubFamilyResolver(
            {"scribe": "Anthropic", "judge": "Google", "red_team": "Google"}
        )
        compiled = (
            "Judge's scoring is context, not authority. "
            + "FILLER " * 200
            + "Judge's scoring is context, not authority."
        )
        result = run_pre_gate(
            input_bundle=ib,
            family_resolver=fr,
            session_rubric_hash="a" * 64,
            compiled_prompt=compiled,
        )
        assert F_RT_FAMILY_OVERLAP in result.failure_codes
        assert any("Judge" in d for d in result.failure_details)

    def test_rubric_drift(self) -> None:
        from pipeline.seats.red_team.logician_wiring import run_pre_gate
        from pipeline.seats.red_team.types import F_RT_RUBRIC_DRIFT

        ib = _make_input_bundle(rubric_hash="a" * 64)
        fr = _StubFamilyResolver(
            {"scribe": "Anthropic", "judge": "Google", "red_team": "OpenAI-OSS"}
        )
        compiled = (
            "Judge's scoring is context, not authority. "
            + "FILLER " * 200
            + "Judge's scoring is context, not authority."
        )
        result = run_pre_gate(
            input_bundle=ib,
            family_resolver=fr,
            session_rubric_hash="DIFFERENT" + "0" * 55,
            compiled_prompt=compiled,
        )
        assert F_RT_RUBRIC_DRIFT in result.failure_codes

    def test_anti_anchoring_phrase_missing(self) -> None:
        from pipeline.seats.red_team.logician_wiring import run_pre_gate
        from pipeline.seats.red_team.types import F_RT_CONTEXT_PLACEMENT

        ib = _make_input_bundle(rubric_hash="a" * 64)
        fr = _StubFamilyResolver(
            {"scribe": "Anthropic", "judge": "Google", "red_team": "OpenAI-OSS"}
        )
        result = run_pre_gate(
            input_bundle=ib,
            family_resolver=fr,
            session_rubric_hash="a" * 64,
            compiled_prompt="just some text without the phrase",
        )
        assert F_RT_CONTEXT_PLACEMENT in result.failure_codes

    def test_anti_anchoring_phrase_only_at_start(self) -> None:
        from pipeline.seats.red_team.logician_wiring import run_pre_gate
        from pipeline.seats.red_team.types import F_RT_CONTEXT_PLACEMENT

        ib = _make_input_bundle(rubric_hash="a" * 64)
        fr = _StubFamilyResolver(
            {"scribe": "Anthropic", "judge": "Google", "red_team": "OpenAI-OSS"}
        )
        compiled = (
            "Judge's scoring is context, not authority. " + "FILLER " * 500
        )
        result = run_pre_gate(
            input_bundle=ib,
            family_resolver=fr,
            session_rubric_hash="a" * 64,
            compiled_prompt=compiled,
        )
        assert F_RT_CONTEXT_PLACEMENT in result.failure_codes


# ---------------------------------------------------------------------------
# logician_wiring — run_post_gate
# ---------------------------------------------------------------------------


def _make_verdict(*, score: int = 12, evidence_in_draft: bool = True):
    """Build a small RedTeamVerdict for POST-gate testing."""
    from pipeline.seats.red_team.types import (
        AttackMemo,
        RedTeamCriterionScore,
        RedTeamVerdict,
        Weakness,
    )

    crit_evidence = "organic mango buyers exceed supply" if evidence_in_draft else "NOT IN DRAFT"
    weakness_claim = "Paragraph 3 asserts demand" if evidence_in_draft else "NOT IN DRAFT"
    # Cap criterion score at max_points (15); total_score = sum of criteria scores.
    crit_score = min(score, 15)
    return RedTeamVerdict(
        run_id="run-1",
        rubric_id="vapg",
        rubric_hash="h" * 64,
        total_score=crit_score,
        max_score=100,
        recommendation="marginal",
        criteria=(
            RedTeamCriterionScore(
                criterion_id="need",
                criterion_name="Need",
                max_points=15,
                score=crit_score,
                tier_matched="strong",
                evidence=crit_evidence,
                missing=("LOIs",),
                notes="solid",
            ),
        ),
        attack_memo=AttackMemo(
            top_weaknesses=(
                Weakness(
                    severity="medium",
                    claim=weakness_claim,
                    why_it_fails="no LOIs",
                    what_a_reviewer_would_say="where are LOIs?",
                    fix_hint="add LOIs",
                ),
            ),
            unsupported_assertions=(),
            dialect_mismatches=(),
            boundary_drift=(),
            overall_verdict="marginal feasibility",
        ),
        total_score_correction=None,
        verdict_at_utc=datetime.now(tz=timezone.utc),
        red_team_dialect="conservative",
    )


def _make_drafts(body: str):
    class FakeSD:
        section_name = "p"
        section_order = 1
        body_text = body
        claim_evidence_map: tuple = ()

    return (FakeSD(),)


class TestRunPostGate:
    def test_clean_pass(self) -> None:
        from pipeline.seats.red_team.logician_wiring import run_post_gate

        verdict = _make_verdict(score=12)
        # Body must contain Red Team's quoted evidence + weakness claim.
        body = (
            "organic mango buyers exceed supply in the region. "
            "Paragraph 3 asserts demand which the reviewer questions."
        )
        result = run_post_gate(
            verdict=verdict,
            drafts=_make_drafts(body),
            judge_total_score=15,  # Δ = 3; below threshold of 10
            judge_scored_ids=frozenset({"need"}),
            rubric_criteria_count=2,
            total_words=20,
        )
        assert result.success is True
        assert result.council_split_detected is False
        assert result.judge_anchor_suspected is False

    def test_evidence_paraphrased(self) -> None:
        from pipeline.seats.red_team.logician_wiring import run_post_gate
        from pipeline.seats.red_team.types import F_RT_EVIDENCE_NOT_IN_DRAFT

        verdict = _make_verdict(score=10, evidence_in_draft=False)
        result = run_post_gate(
            verdict=verdict,
            drafts=_make_drafts("totally different body"),
            judge_total_score=10,
            judge_scored_ids=frozenset({"need"}),
            rubric_criteria_count=2,
            total_words=10,
        )
        assert result.success is False
        assert F_RT_EVIDENCE_NOT_IN_DRAFT in result.failure_codes

    def test_council_split_detected(self) -> None:
        from pipeline.seats.red_team.logician_wiring import run_post_gate
        from pipeline.seats.red_team.types import F_COUNCIL_SPLIT

        verdict = _make_verdict(score=2)  # red_team=2; Judge=15 → Δ=13 ≥ 10
        body = (
            "organic mango buyers exceed supply in the region. "
            "Paragraph 3 asserts demand which the reviewer questions."
        )
        result = run_post_gate(
            verdict=verdict,
            drafts=_make_drafts(body),
            judge_total_score=15,
            judge_scored_ids=frozenset({"need"}),
            rubric_criteria_count=2,
            total_words=20,
        )
        assert result.council_split_detected is True
        assert F_COUNCIL_SPLIT in result.failure_codes

    def test_anchor_suspected_advisory_only(self) -> None:
        from pipeline.seats.red_team.logician_wiring import run_post_gate

        verdict = _make_verdict(score=15)  # red_team=15; Judge=15 → Δ=0 < 2
        body = (
            "organic mango buyers exceed supply in the region. "
            "Paragraph 3 asserts demand which the reviewer questions. "
            + "more body content here " * 100
        )
        result = run_post_gate(
            verdict=verdict,
            drafts=_make_drafts(body),
            judge_total_score=15,
            judge_scored_ids=frozenset({"need"}),
            rubric_criteria_count=7,  # ≥ 5 required for advisory
            total_words=1500,  # ≥ 1000 required
        )
        # Advisory fired — but doesn't add to failure_codes
        assert result.judge_anchor_suspected is True
        assert "F-RT-JUDGE-ANCHOR-SUSPECTED" not in result.failure_codes


# ---------------------------------------------------------------------------
# logician_wiring — assert_sfr_three_block_present
# ---------------------------------------------------------------------------


class TestAssertSfrThreeBlockPresent:
    def test_clean_three_block(self) -> None:
        from pipeline.seats.red_team.logician_wiring import (
            assert_sfr_three_block_present,
        )

        sfr = "## Premises\n\n## Execution trace\n\n## Conclusion\n\nrec"
        assert assert_sfr_three_block_present(sfr) == ()

    def test_missing_premises_block(self) -> None:
        from pipeline.seats.red_team.logician_wiring import (
            assert_sfr_three_block_present,
        )

        sfr = "## Execution trace\n\n## Conclusion"
        v = assert_sfr_three_block_present(sfr)
        assert any("Premises" in vv for vv in v)

    def test_missing_trace_block(self) -> None:
        from pipeline.seats.red_team.logician_wiring import (
            assert_sfr_three_block_present,
        )

        sfr = "## Premises\n\n## Conclusion"
        v = assert_sfr_three_block_present(sfr)
        assert any("Execution trace" in vv for vv in v)

    def test_wrong_block_order(self) -> None:
        from pipeline.seats.red_team.logician_wiring import (
            assert_sfr_three_block_present,
        )

        sfr = "## Conclusion\n\n## Premises\n\n## Execution trace"
        v = assert_sfr_three_block_present(sfr)
        assert any("block_order_wrong" in vv for vv in v)


# ---------------------------------------------------------------------------
# seat — run_seat end-to-end
# ---------------------------------------------------------------------------


class TestRunSeatHappyPath:
    def _build_args(self):
        from pipeline.seats.red_team.seat import run_seat

        ib = _make_input_bundle(rubric_hash="h" * 64)
        return run_seat, ib

    def test_pass_path(self) -> None:
        run_seat, ib = self._build_args()
        from pipeline.seats.red_team.seat import EXIT_PASS

        stub = _StubOutboundCallable(200, _ok_groq_response_body())
        fr = _StubFamilyResolver(
            {"scribe": "Anthropic", "judge": "Google", "red_team": "OpenAI-OSS"}
        )
        clock = _StubClock(datetime(2026, 5, 1, 23, 0, tzinfo=timezone.utc))
        result = run_seat(
            input_bundle=ib,
            rubric_summary_json='{"max_score":100,"criteria":[{"id":"need","max_points":15}]}',
            rubric_max_points_by_id={"need": 15},
            rubric_max_score=100,
            judge_total_score=10,  # Δ=2 with red team 12; below threshold
            judge_scored_ids=frozenset({"need"}),
            judge_view_json='{"total_score":10,"max_score":100,"recommendation":"marginal"}',
            rfa_excerpt="rfa text excerpt",
            api_key="test-key",
            http_post=stub,
            family_resolver=fr,
            session_rubric_hash="h" * 64,
            clock=clock,
        )
        assert result.exit_code == EXIT_PASS
        assert result.verdict is not None
        assert result.sfr_markdown is not None
        assert result.post_gate_result.success is True

    def test_pre_gate_fail_path(self) -> None:
        run_seat, ib = self._build_args()
        from pipeline.seats.red_team.seat import EXIT_PRE_GATE_FAIL

        stub = _StubOutboundCallable(200, _ok_groq_response_body())
        # Family collision: red_team == scribe family
        fr = _StubFamilyResolver(
            {"scribe": "Anthropic", "judge": "Google", "red_team": "Anthropic"}
        )
        clock = _StubClock(datetime(2026, 5, 1, 23, 0, tzinfo=timezone.utc))
        result = run_seat(
            input_bundle=ib,
            rubric_summary_json='{}',
            rubric_max_points_by_id={"need": 15},
            rubric_max_score=100,
            judge_total_score=85,
            judge_scored_ids=frozenset({"need"}),
            judge_view_json=None,
            rfa_excerpt=None,
            api_key="test-key",
            http_post=stub,
            family_resolver=fr,
            session_rubric_hash="h" * 64,
            clock=clock,
        )
        assert result.exit_code == EXIT_PRE_GATE_FAIL
        assert result.verdict is None

    def test_provider_fail_path(self) -> None:
        run_seat, ib = self._build_args()
        from pipeline.seats.red_team.seat import EXIT_PROVIDER_FAIL

        stub = _StubOutboundCallable(401, '{"error":"unauthorized"}')
        fr = _StubFamilyResolver(
            {"scribe": "Anthropic", "judge": "Google", "red_team": "OpenAI-OSS"}
        )
        clock = _StubClock(datetime(2026, 5, 1, 23, 0, tzinfo=timezone.utc))
        result = run_seat(
            input_bundle=ib,
            rubric_summary_json='{}',
            rubric_max_points_by_id={"need": 15},
            rubric_max_score=100,
            judge_total_score=85,
            judge_scored_ids=frozenset({"need"}),
            judge_view_json=None,
            rfa_excerpt=None,
            api_key="bad",
            http_post=stub,
            family_resolver=fr,
            session_rubric_hash="h" * 64,
            clock=clock,
        )
        assert result.exit_code == EXIT_PROVIDER_FAIL
        assert result.provider_result.failure_code == "F-RT-PROVIDER-AUTH-FAIL"

    def test_composer_fail_on_malformed_model_output(self) -> None:
        run_seat, ib = self._build_args()
        from pipeline.seats.red_team.seat import EXIT_COMPOSER_FAIL

        # Model returns gibberish, not valid JSON-shaped Red Team output
        bad_body = json.dumps(
            {"choices": [{"message": {"content": "not a json object at all"}}]}
        )
        stub = _StubOutboundCallable(200, bad_body)
        fr = _StubFamilyResolver(
            {"scribe": "Anthropic", "judge": "Google", "red_team": "OpenAI-OSS"}
        )
        clock = _StubClock(datetime(2026, 5, 1, 23, 0, tzinfo=timezone.utc))
        result = run_seat(
            input_bundle=ib,
            rubric_summary_json='{}',
            rubric_max_points_by_id={"need": 15},
            rubric_max_score=100,
            judge_total_score=85,
            judge_scored_ids=frozenset({"need"}),
            judge_view_json=None,
            rfa_excerpt=None,
            api_key="test-key",
            http_post=stub,
            family_resolver=fr,
            session_rubric_hash="h" * 64,
            clock=clock,
        )
        assert result.exit_code == EXIT_COMPOSER_FAIL

    def test_council_split_path(self) -> None:
        run_seat, ib = self._build_args()
        from pipeline.seats.red_team.seat import EXIT_COUNCIL_SPLIT

        stub = _StubOutboundCallable(200, _ok_groq_response_body())
        fr = _StubFamilyResolver(
            {"scribe": "Anthropic", "judge": "Google", "red_team": "OpenAI-OSS"}
        )
        clock = _StubClock(datetime(2026, 5, 1, 23, 0, tzinfo=timezone.utc))
        # Red Team scores 12 (from canned response); Judge=85 → delta=73 → council split.
        result = run_seat(
            input_bundle=ib,
            rubric_summary_json='{}',
            rubric_max_points_by_id={"need": 15},
            rubric_max_score=100,
            judge_total_score=85,
            judge_scored_ids=frozenset({"need"}),
            judge_view_json=None,
            rfa_excerpt=None,
            api_key="test-key",
            http_post=stub,
            family_resolver=fr,
            session_rubric_hash="h" * 64,
            clock=clock,
        )
        assert result.exit_code == EXIT_COUNCIL_SPLIT
        assert result.verdict is not None
        assert result.post_gate_result.council_split_detected is True
