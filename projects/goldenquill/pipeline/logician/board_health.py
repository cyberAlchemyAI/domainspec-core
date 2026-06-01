"""Board Health — detect, classify, and remedy seat failures in any
multi-seat pipeline (probe harness, council draft/score, thesis defense).

Why this exists
---------------
On 2026-04-14 a 3-seat code review ran and two of the three seats returned
empty/thin output. The Judge (qwen3-32b) exhausted max_tokens inside its
<think> stream; the Editor (deepseek-r1-distill-llama-70b) was decommissioned
mid-run and we fell back to a non-reasoning Llama that returned 276 chars.
Nothing in the pipeline SAW that the board hadn't actually reviewed —
we only noticed when the operator read the report.

On a live grant, a silently-unreviewed draft is worse than no review at
all: it produces a false signal of rigor. This module is the check-and-
balance layer. Every seat call routes through classify_response() before
its output counts. If the seat is broken, remedy_plan() decides whether
to retry with adjusted params, switch model, or escalate to the operator
with a specific diagnosis (not "board failed" — "Judge truncated in think;
retry with max_tokens=24576 or swap to moonshotai/kimi-k2-instruct").

Failure modes classified
------------------------
    HEALTHY                — content, passes validator
    TRUNCATED_IN_THINK     — reasoning stream present, final content empty
    EMPTY_CONTENT          — no content, no reasoning (model or API glitch)
    THIN_CONTENT           — content present but below length threshold
    MISSING_STRUCTURE      — content present, lacks required section/tag schema
    DECOMMISSIONED         — HTTP 400 "model has been decommissioned"
    RATE_LIMITED           — HTTP 429
    AUTH_FAILED            — HTTP 401 / 403
    SERVER_ERROR           — HTTP 5xx
    TIMEOUT                — curl / subprocess timeout
    TRANSPORT              — network transport, malformed JSON, etc.

Remedy ladder per class
-----------------------
    TRUNCATED_IN_THINK  → retry_same_model, max_tokens += 8192 (cap 32768)
                          if still truncated → switch to reasoning fallback
    THIN_CONTENT        → retry_same_model with stronger schema nudge
                          if still thin → switch to more capable fallback
    MISSING_STRUCTURE   → retry_same_model with output-contract reminder
    DECOMMISSIONED      → switch_model (next in seat's candidate list)
    RATE_LIMITED        → wait + retry_same_model (up to 2 retries)
    AUTH_FAILED         → ESCALATE (bad key; operator must intervene)
    SERVER_ERROR        → wait + retry_same_model (up to 2 retries)
    TIMEOUT             → retry_same_model once with longer timeout
                          if still timeout → switch_model
    TRANSPORT           → retry_same_model once; if persists → ESCALATE
    EMPTY_CONTENT       → retry_same_model once; if persists → switch_model

Escalation
----------
When the ladder runs out, `RemedyResult.action == "ESCALATE"` and the
caller MUST NOT proceed as if the seat ran. For the probe this means the
validator_status is FAIL. For the council this means the draft is
QUARANTINED — no publish, operator reads the diagnostic.
"""
from __future__ import annotations

import dataclasses
import re
from typing import Optional


# --- Status constants ------------------------------------------------------

HEALTHY = "HEALTHY"
TRUNCATED_IN_THINK = "TRUNCATED_IN_THINK"
EMPTY_CONTENT = "EMPTY_CONTENT"
THIN_CONTENT = "THIN_CONTENT"
MISSING_STRUCTURE = "MISSING_STRUCTURE"
DECOMMISSIONED = "DECOMMISSIONED"
BAD_REQUEST = "BAD_REQUEST"       # HTTP 400, not decommissioned — this model
                                  # rejected the request shape (unsupported
                                  # param, context too long, etc.). Retry on
                                  # same model will fail the same way; must
                                  # switch model.
RATE_LIMITED = "RATE_LIMITED"
AUTH_FAILED = "AUTH_FAILED"
SERVER_ERROR = "SERVER_ERROR"
TIMEOUT = "TIMEOUT"
TRANSPORT = "TRANSPORT"

FAILURE_STATUSES = {
    TRUNCATED_IN_THINK, EMPTY_CONTENT, THIN_CONTENT, MISSING_STRUCTURE,
    DECOMMISSIONED, BAD_REQUEST, RATE_LIMITED, AUTH_FAILED, SERVER_ERROR,
    TIMEOUT, TRANSPORT,
}


# --- Types -----------------------------------------------------------------

@dataclasses.dataclass
class ResponseInfo:
    """Everything the classifier needs about a single seat call."""
    http_code: int              # -1 if no HTTP response (transport/timeout)
    content: str                # final assistant content (may be "")
    reasoning: str = ""         # reasoning/think stream if parsed separately
    body_snippet: str = ""      # first ~400 chars of raw body for diag
    exception_type: str = ""    # e.g. "TimeoutExpired"
    exception_msg: str = ""     # short msg


@dataclasses.dataclass
class Validator:
    """What does 'structurally complete' mean for this seat?"""
    min_content_chars: int = 800
    required_tags: Optional[list[str]] = None       # e.g. ["BRITTLE","BUG"]
    min_distinct_tags: int = 0
    required_sections: Optional[list[str]] = None   # e.g. ["## File: topology"]
    min_required_sections: int = 0


@dataclasses.dataclass
class RemedyResult:
    """Classifier verdict + next action for the caller."""
    status: str                         # one of the status constants
    action: str                         # RETRY_SAME | SWITCH_MODEL | ESCALATE | PROCEED
    reason: str                         # human-readable diagnosis
    adjust_max_tokens: Optional[int] = None
    wait_seconds: float = 0.0
    attempts_left: int = 0              # caller decrements

    @property
    def ok(self) -> bool:
        return self.status == HEALTHY


# --- Classification --------------------------------------------------------

_TRUNCATION_HINTS = ("max_tokens", "finish_reason=length")


def classify_response(
    resp: ResponseInfo,
    finish_reason: str = "",
    validator: Optional[Validator] = None,
) -> str:
    """Classify a single response into one of the status constants."""
    # Transport/timeout/auth/rate-limit first — HTTP layer beats content.
    if resp.exception_type == "TimeoutExpired":
        return TIMEOUT
    if resp.http_code == -1:
        return TRANSPORT
    if resp.http_code == 429:
        return RATE_LIMITED
    if resp.http_code in (401, 403):
        return AUTH_FAILED
    if 500 <= resp.http_code < 600:
        return SERVER_ERROR
    if resp.http_code == 400:
        if "decommission" in resp.body_snippet.lower():
            return DECOMMISSIONED
        # Any other 400 = this model rejects this request shape (unsupported
        # param, ctx overflow, etc.). Retrying on the same model won't change
        # that; fall through to SWITCH_MODEL via BAD_REQUEST.
        return BAD_REQUEST
    if resp.http_code != 200:
        return TRANSPORT  # other non-200s not specifically handled

    # HTTP 200 — now content-layer classification.
    content = resp.content or ""
    reasoning = resp.reasoning or ""

    if not content and not reasoning:
        return EMPTY_CONTENT
    if not content and reasoning:
        # Model spent its entire budget inside <think> without emitting
        # a final answer — classic qwen3-think pathology.
        return TRUNCATED_IN_THINK
    # finish_reason == "length" with short content = also truncation
    if finish_reason == "length" and len(content) < 1500:
        return TRUNCATED_IN_THINK

    v = validator or Validator()
    if len(content) < v.min_content_chars:
        return THIN_CONTENT

    if v.required_sections and v.min_required_sections > 0:
        hits = sum(1 for s in v.required_sections if s in content)
        if hits < v.min_required_sections:
            return MISSING_STRUCTURE

    if v.required_tags and v.min_distinct_tags > 0:
        tag_set = set()
        for t in v.required_tags:
            if re.search(rf"\b{re.escape(t)}\b", content):
                tag_set.add(t)
        if len(tag_set) < v.min_distinct_tags:
            return MISSING_STRUCTURE

    return HEALTHY


# --- Remedy ladder ---------------------------------------------------------

def remedy_plan(
    status: str,
    *,
    current_max_tokens: int,
    attempts_made: int,
    has_fallback_model: bool,
) -> RemedyResult:
    """Given the classifier verdict + current state, return the next action.

    Parameters
    ----------
    current_max_tokens
        What the just-completed call used. Ladder may raise it.
    attempts_made
        How many attempts on the current model have happened.
    has_fallback_model
        True if the seat has another candidate model after the current one.
    """
    if status == HEALTHY:
        return RemedyResult(HEALTHY, "PROCEED", "seat passed validator")

    # TRUNCATED_IN_THINK — raise budget, retry once; if repeats, swap model.
    if status == TRUNCATED_IN_THINK:
        if attempts_made < 2 and current_max_tokens < 32768:
            new_max = min(current_max_tokens + 8192, 32768)
            return RemedyResult(
                status, "RETRY_SAME",
                f"model exhausted tokens inside reasoning; raising max_tokens "
                f"{current_max_tokens}→{new_max}",
                adjust_max_tokens=new_max,
                attempts_left=1,
            )
        if has_fallback_model:
            return RemedyResult(
                status, "SWITCH_MODEL",
                "reasoning truncation persists at 32k; switching to fallback model",
            )
        return RemedyResult(
            status, "ESCALATE",
            "reasoning truncation persists and no fallback model available",
        )

    # THIN_CONTENT — retry once; if still thin, swap.
    if status == THIN_CONTENT:
        if attempts_made < 2:
            return RemedyResult(
                status, "RETRY_SAME",
                "output below length threshold; retrying with same model "
                "(adds schema pressure on retry framing)",
                attempts_left=1,
            )
        if has_fallback_model:
            return RemedyResult(
                status, "SWITCH_MODEL",
                "thin output persists; switching to more capable fallback",
            )
        return RemedyResult(
            status, "ESCALATE",
            "thin output persists and no fallback model available",
        )

    # MISSING_STRUCTURE — retry with reminder; if still wrong, swap.
    if status == MISSING_STRUCTURE:
        if attempts_made < 2:
            return RemedyResult(
                status, "RETRY_SAME",
                "output missing required sections/tags; retrying with "
                "output-contract reminder",
                attempts_left=1,
            )
        if has_fallback_model:
            return RemedyResult(
                status, "SWITCH_MODEL",
                "structure violation persists; switching to fallback",
            )
        return RemedyResult(
            status, "ESCALATE",
            "structure violation persists and no fallback model available",
        )

    if status == DECOMMISSIONED:
        if has_fallback_model:
            return RemedyResult(
                status, "SWITCH_MODEL",
                "model decommissioned by provider; switching to fallback",
            )
        return RemedyResult(
            status, "ESCALATE",
            "model decommissioned and no fallback model available",
        )

    if status == BAD_REQUEST:
        # 400 that isn't decommissioned = model rejects request shape.
        # Retry on same model will fail identically; must switch.
        if has_fallback_model:
            return RemedyResult(
                status, "SWITCH_MODEL",
                "model rejected request shape (HTTP 400); switching to "
                "fallback (likely unsupported param or context overflow)",
            )
        return RemedyResult(
            status, "ESCALATE",
            "model rejected request shape (HTTP 400) and no fallback available",
        )

    if status == RATE_LIMITED:
        if attempts_made < 3:
            return RemedyResult(
                status, "RETRY_SAME",
                "provider rate-limit; backing off and retrying",
                wait_seconds=5.0 * (attempts_made + 1),
                attempts_left=1,
            )
        return RemedyResult(
            status, "ESCALATE",
            "rate-limit persists across retries",
        )

    if status == SERVER_ERROR:
        if attempts_made < 3:
            return RemedyResult(
                status, "RETRY_SAME",
                "provider 5xx; retrying with backoff",
                wait_seconds=3.0 * (attempts_made + 1),
                attempts_left=1,
            )
        if has_fallback_model:
            return RemedyResult(
                status, "SWITCH_MODEL",
                "5xx persists; switching to fallback provider model",
            )
        return RemedyResult(status, "ESCALATE", "5xx persists and no fallback")

    if status == TIMEOUT:
        if attempts_made < 2:
            return RemedyResult(
                status, "RETRY_SAME",
                "timeout; retrying once",
                attempts_left=1,
            )
        if has_fallback_model:
            return RemedyResult(
                status, "SWITCH_MODEL",
                "timeout persists; switching to fallback",
            )
        return RemedyResult(status, "ESCALATE", "timeout persists and no fallback")

    if status == EMPTY_CONTENT:
        if attempts_made < 2:
            return RemedyResult(
                status, "RETRY_SAME",
                "empty response; retrying once",
                attempts_left=1,
            )
        if has_fallback_model:
            return RemedyResult(
                status, "SWITCH_MODEL",
                "empty response persists; switching to fallback",
            )
        return RemedyResult(status, "ESCALATE",
                            "empty response persists and no fallback")

    if status == TRANSPORT:
        if attempts_made < 2:
            return RemedyResult(
                status, "RETRY_SAME",
                "transport error; retrying once",
                attempts_left=1,
            )
        return RemedyResult(
            status, "ESCALATE",
            "transport errors persist (check network / API endpoint)",
        )

    if status == AUTH_FAILED:
        return RemedyResult(
            status, "ESCALATE",
            "API auth failed — key invalid or revoked; operator must intervene",
        )

    # Unknown status — fail safe, escalate.
    return RemedyResult(status, "ESCALATE", f"unhandled status {status!r}")


# --- Orchestrator ----------------------------------------------------------

@dataclasses.dataclass
class SeatCallLog:
    """Per-attempt audit trail for one seat."""
    attempt: int
    model: str
    status: str
    action: str
    reason: str
    http_code: int
    content_chars: int
    reasoning_chars: int
    elapsed: float


@dataclasses.dataclass
class SeatResult:
    seat_name: str
    final_model: str
    content: str
    healthy: bool
    terminal_status: str        # HEALTHY or the final failure status
    escalation_reason: str      # "" when healthy
    attempts: list[SeatCallLog]


def run_seat_with_remedy(
    seat_name: str,
    candidate_models: list[str],
    call_fn,
    *,
    validator: Optional[Validator] = None,
    initial_max_tokens: int = 16384,
    max_attempts_per_model: int = 2,
) -> SeatResult:
    """Drive one seat through the full remedy ladder.

    `call_fn(model, max_tokens) -> (ResponseInfo, finish_reason, elapsed)`.
    Caller implements the HTTP call; this orchestrator decides what to do
    with its result.

    Returns SeatResult. If terminal_status != HEALTHY, the caller MUST NOT
    count this seat as having reviewed — escalate to operator.
    """
    attempts: list[SeatCallLog] = []
    for model_idx, model in enumerate(candidate_models):
        has_fallback = model_idx < len(candidate_models) - 1
        current_max = initial_max_tokens
        for attempt_idx in range(max_attempts_per_model):
            resp, finish, elapsed = call_fn(model, current_max)
            status = classify_response(resp, finish, validator)
            plan = remedy_plan(
                status,
                current_max_tokens=current_max,
                attempts_made=attempt_idx + 1,
                has_fallback_model=has_fallback,
            )
            attempts.append(SeatCallLog(
                attempt=len(attempts) + 1,
                model=model,
                status=status,
                action=plan.action,
                reason=plan.reason,
                http_code=resp.http_code,
                content_chars=len(resp.content or ""),
                reasoning_chars=len(resp.reasoning or ""),
                elapsed=round(elapsed, 2),
            ))
            if plan.action == "PROCEED":
                return SeatResult(
                    seat_name=seat_name,
                    final_model=model,
                    content=resp.content,
                    healthy=True,
                    terminal_status=HEALTHY,
                    escalation_reason="",
                    attempts=attempts,
                )
            if plan.action == "RETRY_SAME":
                if plan.adjust_max_tokens:
                    current_max = plan.adjust_max_tokens
                if plan.wait_seconds:
                    import time as _time
                    _time.sleep(plan.wait_seconds)
                continue
            if plan.action == "SWITCH_MODEL":
                break  # out of inner loop, try next candidate
            if plan.action == "ESCALATE":
                return SeatResult(
                    seat_name=seat_name,
                    final_model=model,
                    content=resp.content,
                    healthy=False,
                    terminal_status=status,
                    escalation_reason=plan.reason,
                    attempts=attempts,
                )
    # Ran out of models.
    last = attempts[-1] if attempts else None
    return SeatResult(
        seat_name=seat_name,
        final_model=last.model if last else "",
        content="",
        healthy=False,
        terminal_status=last.status if last else EMPTY_CONTENT,
        escalation_reason="all candidate models exhausted",
        attempts=attempts,
    )


def summarize_board_health(seat_results: list[SeatResult]) -> dict:
    """Roll-up for reports."""
    healthy = [r for r in seat_results if r.healthy]
    unhealthy = [r for r in seat_results if not r.healthy]
    return {
        "board_status": "HEALTHY" if not unhealthy else "DEGRADED",
        "seats_total": len(seat_results),
        "seats_healthy": len(healthy),
        "seats_unhealthy": len(unhealthy),
        "unhealthy_seats": [
            {
                "seat": r.seat_name,
                "final_model": r.final_model,
                "terminal_status": r.terminal_status,
                "escalation_reason": r.escalation_reason,
                "attempts": len(r.attempts),
            }
            for r in unhealthy
        ],
    }
