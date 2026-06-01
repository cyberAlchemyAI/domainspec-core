"""pipeline.seats.red_team.seat — subprocess seat-runner entry point.

R3 ships the orchestrator that ties together:

1. PRE-gate batch (cross-family + input invariants + rubric drift +
   context placement) via :mod:`logician_wiring`.
2. Provider call via :mod:`provider_groq` (Groq GPT-OSS-120B primary;
   production HTTP behind ``# pragma: no cover``).
3. JSON parse + verdict composition via :mod:`attack_memo`.
4. SFR three-block emission via :mod:`sfr_emitter`.
5. POST-gate batch (evidence-in-draft + identity-invariant + council-split
   + anchor-suspected advisory) via :mod:`logician_wiring`.

E-017 injected-seam pattern: every external dependency (OutboundCallable
per CC-007 §4 v2.x.6 fixture-migration sweep — was HTTPCaller pre-sweep;
FamilyResolver, ClockFn, etc.) is a Protocol injected at run_seat() call
site. Tests inject deterministic stubs; production wires
``enforce_outbound_boundary(stdlib_urlopen_caller, ...)`` per
§4 v2.x.5 LOCKed amendment row 232.

The seat returns an int exit code (matches Judge R3 + Scribe R3
``run_seat`` signature):

- 0 → PASS (verdict produced; PRE+POST gates clean).
- 1 → PRE-gate failure.
- 2 → provider failure (transport / auth / rate-limit / parse).
- 3 → composer failure (model output malformed; verdict construction failed).
- 4 → POST-gate failure.
- 5 → council-split (operator decision required; not a failure but
  separate exit code so the runner can route to ``signoff_pending_council_split``).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Final, Protocol, runtime_checkable

from pipeline.seats.red_team.attack_memo import compose_red_team_verdict
from pipeline.seats.red_team.logician_wiring import (
    FamilyResolver,
    PostGateResult,
    PreGateResult,
    assert_sfr_three_block_present,
    run_post_gate,
    run_pre_gate,
)
from pipeline.seats.red_team.provider_groq import (
    GROQ_DEFAULT_MAX_TOKENS,
    GROQ_DEFAULT_MODEL,
    GroqProviderResult,
    OutboundCallable,
    call_groq,
    extract_json_from_content,
    extract_message_content,
)
from pipeline.seats.red_team.sfr_emitter import emit_sfr_certificate
from pipeline.seats.red_team.types import RedTeamDialect, RedTeamInput, RedTeamVerdict


# ---------------------------------------------------------------------------
# System prompt (lifted from orchestrator-CLI line 54-101 with §A3 SFR addition)
# ---------------------------------------------------------------------------

SYSTEM_PROMPT: Final[str] = """Judge's scoring is context, not authority. Form your own view fresh.

You are Red Team — the adversarial seat in a multi-family AI grant-writing council.

Your job is NOT to agree with Judge. Your job is to find weakness.

Adopt the mindset of a skeptical reviewer on a panel of 12, reading this draft at hour four of a twelve-hour scoring day. You are tired, under quota, and your default posture is to find reasons to downrank. Reviewers reject more often than they fund.

You have three tasks:

1. SCORE the draft against the rubric, parsimoniously. Your score may differ from Judge's — that is the point. Never anchor to Judge's score. You score fresh.

2. ATTACK the draft. Identify the top weaknesses. For each, state:
   - severity (high / medium / low)
   - the exact claim or section being attacked
   - why it fails under reviewer scrutiny
   - what a real reviewer on a real panel would write in the margin
   - a short fix hint (not a rewrite — just direction)

3. FLAG specific failure modes:
   - Unsupported assertions (claims with no evidence, data, or citation)
   - Dialect mismatches (tone/vocabulary that won't land with this funder)
   - Boundary drift (places the draft exceeds or dodges the RFA's actual scope)

Rules:
- Judge's scoring is context, not authority. Form your own view.
- Never invent facts about the applicant. If evidence is missing, that IS the weakness.
- Be specific.
- Return ONLY a JSON object matching the schema. No preamble, no markdown fences.
- Do not soften your critique to match Judge. Disagreement is a feature.

BE TERSE. Each string field: one sentence, maximum 25 words. Evidence cites paragraph/section, does not quote long passages. top_weaknesses: list at most 5, not more.

Output JSON schema:
{
  "total_score": int,
  "recommendation": "competitive" | "marginal" | "not_ready",
  "criteria": [
    {"id": str, "name": str, "max_points": int, "score": int,
     "tier_matched": str, "evidence": str, "missing": [str], "notes": str}
  ],
  "attack_memo": {
    "top_weaknesses": [
      {"severity": str, "claim": str, "why_it_fails": str,
       "what_a_reviewer_would_say": str, "fix_hint": str}
    ],
    "unsupported_assertions": [str],
    "dialect_mismatches": [str],
    "boundary_drift": [str],
    "overall_verdict": str
  }
}

Remember: Judge's scoring is context, not authority. You score fresh."""


# ---------------------------------------------------------------------------
# Exit codes
# ---------------------------------------------------------------------------

EXIT_PASS: Final[int] = 0
EXIT_PRE_GATE_FAIL: Final[int] = 1
EXIT_PROVIDER_FAIL: Final[int] = 2
EXIT_COMPOSER_FAIL: Final[int] = 3
EXIT_POST_GATE_FAIL: Final[int] = 4
EXIT_COUNCIL_SPLIT: Final[int] = 5

assert EXIT_PASS == 0, "EXIT_PASS rebound; refusing to load"
assert EXIT_COUNCIL_SPLIT == 5, "EXIT_COUNCIL_SPLIT rebound; refusing to load"


# ---------------------------------------------------------------------------
# E-017 seam: ClockFn
# ---------------------------------------------------------------------------


@runtime_checkable
class ClockFn(Protocol):
    """Inject for deterministic verdict_at_utc."""

    def now_utc(self) -> datetime:
        ...


# ---------------------------------------------------------------------------
# Seat result shape (returned to caller; subprocess prints + exits with code)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class SeatRunResult:
    """Outcome of a Red Team seat run."""

    exit_code: int
    pre_gate_result: PreGateResult | None
    post_gate_result: PostGateResult | None
    verdict: RedTeamVerdict | None
    sfr_markdown: str | None
    provider_result: GroqProviderResult | None
    error_detail: str | None


# ---------------------------------------------------------------------------
# Prompt builder (lifted from orchestrator-CLI line 132-158)
# ---------------------------------------------------------------------------


def _build_user_prompt(
    *,
    draft_concat: str,
    rubric_summary: str,
    rfa_excerpt: str | None,
    judge_view_json: str | None,
) -> str:
    parts: list[str] = []
    parts.append("FUNDER RUBRIC (score against this — id/name/max_points per criterion):")
    parts.append(rubric_summary)
    parts.append("")
    if rfa_excerpt:
        parts.append("RFA EXCERPT (for context and scope checking):")
        parts.append(rfa_excerpt[:6000])
        parts.append("")
    if judge_view_json:
        parts.append("JUDGE SCORING SUMMARY (context only — DO NOT anchor to this):")
        parts.append(judge_view_json)
        parts.append("")
    parts.append("APPLICANT DRAFT (attack this):")
    parts.append(draft_concat)
    parts.append("")
    parts.append(
        "Return the JSON object and nothing else. Remember: disagreement with Judge is a feature."
    )
    parts.append(
        "BE TERSE. Each string field: one sentence, maximum 25 words. "
        "top_weaknesses: list at most 5, not more."
    )
    # Anti-anchoring discipline placement: phrase already in SYSTEM_PROMPT
    # head + repeated here at user-prompt tail. Together start + end land
    # the load-bearing constraint per §6 context-placement lint.
    parts.append("Judge's scoring is context, not authority.")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def run_seat(
    *,
    input_bundle: RedTeamInput,
    rubric_summary_json: str,
    rubric_max_points_by_id: dict[str, int],
    rubric_max_score: int,
    judge_total_score: int | None,
    judge_scored_ids: frozenset[str] | None,
    judge_view_json: str | None,
    rfa_excerpt: str | None,
    api_key: str,
    http_post: OutboundCallable,
    family_resolver: FamilyResolver,
    session_rubric_hash: str,
    clock: ClockFn,
    red_team_dialect: RedTeamDialect = "conservative",
    model: str = GROQ_DEFAULT_MODEL,
    max_tokens: int = GROQ_DEFAULT_MAX_TOKENS,
) -> SeatRunResult:
    """Run the Red Team seat end-to-end.

    Production caller wires all E-017 seams (OutboundCallable via
    ``enforce_outbound_boundary(stdlib_urlopen_caller, ...)`` per CC-007
    §4 v2.x.5; FamilyResolver via §5 v6 RunState accessor; ClockFn via
    stdlib datetime). Tests inject deterministic stubs matching the
    OutboundCallable Protocol byte-for-byte (bytes body + bytes response).

    Returns :class:`SeatRunResult` carrying the appropriate exit code +
    populated fields. Subprocess wrappers print + exit; programmatic
    callers read the result struct directly.
    """
    # --- Step 1: PRE-gate batch ---
    draft_concat = "\n\n".join(d.body_text for d in input_bundle.section_drafts)
    user_prompt = _build_user_prompt(
        draft_concat=draft_concat,
        rubric_summary=rubric_summary_json,
        rfa_excerpt=rfa_excerpt,
        judge_view_json=judge_view_json,
    )
    compiled_prompt = SYSTEM_PROMPT + "\n\n" + user_prompt

    pre_result = run_pre_gate(
        input_bundle=input_bundle,
        family_resolver=family_resolver,
        session_rubric_hash=session_rubric_hash,
        compiled_prompt=compiled_prompt,
    )
    if not pre_result.success:
        return SeatRunResult(
            exit_code=EXIT_PRE_GATE_FAIL,
            pre_gate_result=pre_result,
            post_gate_result=None,
            verdict=None,
            sfr_markdown=None,
            provider_result=None,
            error_detail=f"PRE-gate failures: {pre_result.failure_codes}",
        )

    # --- Step 2: Provider call ---
    provider_result = call_groq(
        http_post=http_post,
        api_key=api_key,
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        model=model,
        max_tokens=max_tokens,
    )
    if provider_result.failure_code is not None:
        return SeatRunResult(
            exit_code=EXIT_PROVIDER_FAIL,
            pre_gate_result=pre_result,
            post_gate_result=None,
            verdict=None,
            sfr_markdown=None,
            provider_result=provider_result,
            error_detail=(
                f"{provider_result.failure_code}: {provider_result.failure_detail}"
            ),
        )

    # --- Step 3: Parse model output → compose verdict ---
    content = extract_message_content(provider_result)
    if not content:
        return SeatRunResult(
            exit_code=EXIT_COMPOSER_FAIL,
            pre_gate_result=pre_result,
            post_gate_result=None,
            verdict=None,
            sfr_markdown=None,
            provider_result=provider_result,
            error_detail="provider returned empty message content",
        )
    parsed = extract_json_from_content(content)
    if parsed is None:
        return SeatRunResult(
            exit_code=EXIT_COMPOSER_FAIL,
            pre_gate_result=pre_result,
            post_gate_result=None,
            verdict=None,
            sfr_markdown=None,
            provider_result=provider_result,
            error_detail=f"model output not parseable as JSON: {content[:200]}",
        )

    try:
        verdict = compose_red_team_verdict(
            parsed_model_output=parsed,
            input_bundle=input_bundle,
            rubric_max_points_by_id=rubric_max_points_by_id,
            rubric_max_score=rubric_max_score,
            red_team_dialect=red_team_dialect,
            verdict_at_utc=clock.now_utc(),
        )
    except (ValueError, TypeError) as e:
        return SeatRunResult(
            exit_code=EXIT_COMPOSER_FAIL,
            pre_gate_result=pre_result,
            post_gate_result=None,
            verdict=None,
            sfr_markdown=None,
            provider_result=provider_result,
            error_detail=f"verdict composition failed: {type(e).__name__}: {str(e)[:200]}",
        )

    # --- Step 4: Emit SFR three-block ---
    sfr_markdown = emit_sfr_certificate(verdict=verdict)
    sfr_violations = assert_sfr_three_block_present(sfr_markdown)
    if sfr_violations:
        return SeatRunResult(
            exit_code=EXIT_COMPOSER_FAIL,
            pre_gate_result=pre_result,
            post_gate_result=None,
            verdict=verdict,
            sfr_markdown=sfr_markdown,
            provider_result=provider_result,
            error_detail=f"SFR malformed: {sfr_violations}",
        )

    # --- Step 5: POST-gate batch ---
    total_words = sum(
        len(d.body_text.split()) for d in input_bundle.section_drafts
    )
    rubric_criteria_count = len(rubric_max_points_by_id)
    post_result = run_post_gate(
        verdict=verdict,
        drafts=input_bundle.section_drafts,
        judge_total_score=judge_total_score,
        judge_scored_ids=judge_scored_ids,
        rubric_criteria_count=rubric_criteria_count,
        total_words=total_words,
    )

    # Council-split is "operator decision required" — separate exit code.
    if post_result.council_split_detected:
        # If only F-COUNCIL-SPLIT in failure codes (no other POST-gate failure),
        # exit COUNCIL_SPLIT. If other failures too, prioritize POST_GATE_FAIL.
        non_council_failures = tuple(
            c for c in post_result.failure_codes if c != "F-COUNCIL-SPLIT"
        )
        if non_council_failures:
            return SeatRunResult(
                exit_code=EXIT_POST_GATE_FAIL,
                pre_gate_result=pre_result,
                post_gate_result=post_result,
                verdict=verdict,
                sfr_markdown=sfr_markdown,
                provider_result=provider_result,
                error_detail=(
                    f"POST-gate failures (council-split AND): {non_council_failures}"
                ),
            )
        return SeatRunResult(
            exit_code=EXIT_COUNCIL_SPLIT,
            pre_gate_result=pre_result,
            post_gate_result=post_result,
            verdict=verdict,
            sfr_markdown=sfr_markdown,
            provider_result=provider_result,
            error_detail=None,
        )

    if not post_result.success:
        return SeatRunResult(
            exit_code=EXIT_POST_GATE_FAIL,
            pre_gate_result=pre_result,
            post_gate_result=post_result,
            verdict=verdict,
            sfr_markdown=sfr_markdown,
            provider_result=provider_result,
            error_detail=f"POST-gate failures: {post_result.failure_codes}",
        )

    # PASS
    return SeatRunResult(
        exit_code=EXIT_PASS,
        pre_gate_result=pre_result,
        post_gate_result=post_result,
        verdict=verdict,
        sfr_markdown=sfr_markdown,
        provider_result=provider_result,
        error_detail=None,
    )


__all__ = [
    "SYSTEM_PROMPT",
    "EXIT_PASS",
    "EXIT_PRE_GATE_FAIL",
    "EXIT_PROVIDER_FAIL",
    "EXIT_COMPOSER_FAIL",
    "EXIT_POST_GATE_FAIL",
    "EXIT_COUNCIL_SPLIT",
    "ClockFn",
    "SeatRunResult",
    "run_seat",
]
