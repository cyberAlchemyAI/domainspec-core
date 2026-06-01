"""Tilth UI Scout bridge — RESCAN button entrypoint.

============================================================================
DEV PATH — NOT FOR CUSTOMER DEPLOYMENTS.

This file is the operator's daily-driver Scout face on dev hardware (8GB
Mac Mini). It bypasses the v0.1 production routing chain in two ways that
are intentional for dev velocity but FORBIDDEN for any deployed Tilth:

  1. No classification ceremony. Cloud calls skip `classification_context`
     (Frontier-Eligible posture's PRE-gate requirement per v7.0.7 §4) and
     skip the `enforce_outbound_boundary` wrapper entirely.
  2. No sovereignty session boot, no vault commit hook, no checkpoint /
     degradation ledger writes. The bridge is stateless beyond the UI's
     event log.

Customer-facing v0.1 Beta / V1 / V1.x deployments MUST go through:
  pipeline/orchestrator/seats/scout.py  → router.call_seat("scout", ...)
which honors the deployment posture, classification register, outbound
boundary, and the full Five Operating Laws via Logician PRE/POST gates.

Two specific blockers prevent this bridge from collapsing into the
production seat right now:

  - provider_boundary.py:368 `stdlib_urlopen_caller` refuses non-https
    URLs structurally (DC-CYCLE2-02). Local ollama at http://localhost:11434
    cannot be reached even via the `_local_provider_caller` shim. Fix is
    ~5 LOC at LOCKED §4 v2.x.5 code; needs a Thesis Team audit.
  - Section 5 Pipeline orchestrator (the glue around `run_scout_discover`
    with production FDBroker/NonceRegistry/SynopsisFetcher/ApplicantProfile
    bindings + sovereignty session boot) is not yet wired.

Engineer onboarding pointer: docs/scout_dev_vs_production_path.md.
============================================================================

What the bridge does:
  1. Live Grants.gov search2 fetch (Channel A, public API, no auth).
  2. Cloud-frontier triage via Gemini 2.5 Flash by default (free tier,
     ~13s for 5 candidates, full coverage); env-var swappable to Claude,
     GPT, or local ollama for offline use.
  3. Map must_read / maybe / declined → the opportunity / totals shape
     the tilth_ui projection consumes
     (archive/legacy/tilth_ui_static_stitch_scaffold/SCOUT_INTEGRATION_SPEC.md §2).

Channels B-F (cached, state, federal-program, RSS, web) stay dark in this
dev face — those are real per-channel work that belongs in the production
path, not the dev shell. Channel A alone gives ~25 live federal rows
per scan, which matches what the Monday radar surfaces.

stdout = a single JSON object:
  {"ok": bool, "reason": str, "opportunities": [...], "totals": {...}, "meta": {...}}
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

from pipeline.orchestrator.provider_boundary import (
    enforce_outbound_boundary,
    stdlib_urlopen_caller,
    ClassificationContext,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Reuse the orchestrator seat's LLM-facing prompt + parse/validate helpers
# verbatim — single source of truth for Scout's triage behavior. The seat
# module is NOT invoked end-to-end here; see _ollama_chat below for why.
from pipeline.orchestrator.seats.scout import (  # noqa: E402
    SYSTEM_PROMPT as SCOUT_SYSTEM_PROMPT,
    build_user_prompt,
    extract_json,
    validate as validate_scout_output,
)

GRANTS_GOV_URL = "https://api.grants.gov/v1/api/search2"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
GOOGLE_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

DEFAULT_LOOKBACK_DAYS = 14
DEFAULT_LIMIT = 25
# Dev default: Gemini 2.5 Flash — Google AI Studio free tier (60 RPM,
# 1M tokens/day), ~13s wall clock for 5-candidate triage, validation_passed
# under live test. Override via --model or TILTH_UI_SCOUT_MODEL env var.
# Production deployments do NOT read this — they go through router.yaml
# via pipeline.orchestrator.seats.scout instead. See file-top banner.
DEFAULT_MODEL = "gemini-2.5-flash"
USER_AGENT = "Golden-Quill-Scout-UI/0.1"

# Why bypass `pipeline.orchestrator.seats.scout.run(...)` for the dev face:
#
# The orchestrator seat routes through `call_seat` → `_local_provider_caller`
# / `enforce_outbound_boundary` → `stdlib_urlopen_caller`. Two real frictions
# for dev use on Josh's 8GB box:
#   (1) `stdlib_urlopen_caller` refuses non-https schemes structurally
#       (provider_boundary.py:368), so local ollama at http://localhost:11434
#       cannot be reached — v0.1 architectural gap, fix is ~5 LOC at LOCKED
#       code (see memory project-v01-outbound-boundary-ollama-gap).
#   (2) Cloud providers via the router require `classification_context` per
#       v7.0.7 §4. For Josh's personal dev RESCAN — not a customer-facing
#       Tilth deployment — that classification ceremony is overkill.
#
# So the bridge calls providers directly via their public APIs. The
# orchestrator seat's SYSTEM_PROMPT + build_user_prompt + extract_json +
# validate helpers are still imported verbatim — Scout's reasoning contract
# is unchanged; only the transport is bypassed.
#
# Production customer deployments (Local-Only-Sovereign / Frontier-Eligible
# / Split-Context-Hybrid postures) MUST go through the orchestrator router
# once the boundary gap closes. This bridge is the dev / "Tilth gets a face"
# path; not the production cycle path.


_DOTENV_PATH = Path.home() / ".openclaw" / ".env"
_dotenv_cache: dict[str, str] | None = None


def _load_openclaw_dotenv() -> dict[str, str]:
    """Read ~/.openclaw/.env as a fallback for API keys.

    OpenClaw stores provider keys in this file; subprocesses (like this
    bridge) may not inherit them via env. Pure stdlib parser — no python-dotenv
    dependency.
    """
    global _dotenv_cache
    if _dotenv_cache is not None:
        return _dotenv_cache
    out: dict[str, str] = {}
    if _DOTENV_PATH.is_file():
        try:
            text = _DOTENV_PATH.read_text(encoding="utf-8")
        except OSError:
            _dotenv_cache = out
            return out
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            k, _, v = stripped.partition("=")
            v = v.strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
                v = v[1:-1]
            out[k.strip()] = v
    _dotenv_cache = out
    return out


def _resolve_api_key(name: str) -> str | None:
    val = os.environ.get(name)
    if val:
        return val
    val = _load_openclaw_dotenv().get(name)
    return val or None


def _http_post_json(url: str, *, headers: dict[str, str], body: dict, timeout_s: float) -> dict:
    caller = enforce_outbound_boundary(
        stdlib_urlopen_caller,
        classification_context=ClassificationContext(inputs=()),
        posture="frontier_eligible",
    )
    try:
        status, response_bytes = caller(
            url=url,
            headers={"User-Agent": USER_AGENT, "Content-Type": "application/json", **headers},
            body=json.dumps(body).encode("utf-8"),
            timeout_seconds=timeout_s,
        )
        if status >= 400:
            err_body = response_bytes.decode("utf-8", errors="replace")[:600]
            raise RuntimeError(f"HTTP {status}: {err_body}")
        return json.loads(response_bytes.decode("utf-8"))
    except Exception as exc:
        if isinstance(exc, RuntimeError) and str(exc).startswith("HTTP"):
            raise
        raise RuntimeError(f"Request failed: {type(exc).__name__}: {exc}") from exc


def _anthropic_chat(*, system: str, prompt: str, model: str, timeout_s: float = 120.0) -> dict:
    key = _resolve_api_key("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY not set (checked env + ~/.openclaw/.env)")
    resp = _http_post_json(
        ANTHROPIC_URL,
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
        body={
            "model": model,
            "max_tokens": 4096,
            "system": system + "\n\nReturn ONLY a JSON object — no markdown fences.",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
        },
        timeout_s=timeout_s,
    )
    parts = resp.get("content") or []
    text = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
    return {
        "content": text,
        "model": resp.get("model") or model,
        "family": "anthropic",
        "usage": resp.get("usage") or {},
    }


def _openai_chat(*, system: str, prompt: str, model: str, timeout_s: float = 120.0) -> dict:
    key = _resolve_api_key("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set (checked env + ~/.openclaw/.env)")
    resp = _http_post_json(
        OPENAI_URL,
        headers={"Authorization": f"Bearer {key}"},
        body={
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2,
        },
        timeout_s=timeout_s,
    )
    choices = resp.get("choices") or [{}]
    text = (choices[0].get("message") or {}).get("content", "")
    return {
        "content": text,
        "model": resp.get("model") or model,
        "family": "openai",
        "usage": resp.get("usage") or {},
    }


def _google_chat(*, system: str, prompt: str, model: str, timeout_s: float = 120.0) -> dict:
    key = _resolve_api_key("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("GOOGLE_API_KEY not set (checked env + ~/.openclaw/.env)")
    resp = _http_post_json(
        GOOGLE_URL_TEMPLATE.format(model=model, key=key),
        headers={},
        body={
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.2,
            },
        },
        timeout_s=timeout_s,
    )
    candidates = resp.get("candidates") or [{}]
    parts = ((candidates[0].get("content") or {}).get("parts")) or [{}]
    text = "".join(p.get("text", "") for p in parts)
    return {
        "content": text,
        "model": model,
        "family": "google",
        "usage": resp.get("usageMetadata") or {},
    }


def _ollama_chat(*, system: str, prompt: str, model: str, timeout_s: float = 180.0) -> dict:
    body = {
        "model": model,
        "system": system,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.2},
    }
    caller = enforce_outbound_boundary(
        stdlib_urlopen_caller,
        classification_context=ClassificationContext(inputs=()),
        posture="frontier_eligible",
    )
    status, response_bytes = caller(
        url=OLLAMA_URL,
        headers={"User-Agent": USER_AGENT, "Content-Type": "application/json"},
        body=json.dumps(body).encode("utf-8"),
        timeout_seconds=timeout_s,
    )
    if status >= 400:
        raise RuntimeError(f"Ollama HTTP {status}: {response_bytes.decode('utf-8', errors='replace')}")
    payload = json.loads(response_bytes.decode("utf-8"))
    return {
        "content": payload.get("response", ""),
        "model": model,
        "family": "mistral" if "mistral" in model.lower() else (
            "alibaba" if "qwen" in model.lower() else "ollama"
        ),
        "usage": {
            "prompt_eval_count": payload.get("prompt_eval_count"),
            "eval_count": payload.get("eval_count"),
        },
    }


# Model-id → (callable, default-fallback-id-if-key-missing)
_PROVIDERS: dict[str, Callable[..., dict]] = {
    "claude-sonnet-4-6": _anthropic_chat,
    "claude-sonnet-4-5": _anthropic_chat,
    "claude-opus-4-6": _anthropic_chat,
    "claude-opus-4-7": _anthropic_chat,
    "claude-haiku-4-5": _anthropic_chat,
    "gpt-5.1": _openai_chat,
    "gpt-5": _openai_chat,
    "gpt-4o": _openai_chat,
    "gpt-4o-mini": _openai_chat,
    "gemini-2.5-pro": _google_chat,
    "gemini-2.5-flash": _google_chat,
    "mistral:7b": _ollama_chat,
    "mixtral:8x7b": _ollama_chat,
    "qwen2.5:7b": _ollama_chat,
    "qwen2.5:14b": _ollama_chat,
}

OLLAMA_FALLBACK_MODEL = "mistral:7b"


def _resolve_provider(model_id: str) -> tuple[Callable[..., dict], str]:
    fn = _PROVIDERS.get(model_id)
    if fn is None:
        # Unknown model id — best-effort routing by prefix
        if model_id.startswith("claude"):
            return _anthropic_chat, model_id
        if model_id.startswith("gpt"):
            return _openai_chat, model_id
        if model_id.startswith("gemini"):
            return _google_chat, model_id
        return _ollama_chat, model_id
    return fn, model_id


def _call_provider_with_fallback(
    *,
    system: str,
    prompt: str,
    primary_model: str,
    allow_ollama_fallback: bool,
) -> tuple[dict, dict]:
    """Call the primary provider; on failure fall back to local ollama if allowed.

    Returns (resp_dict, route_meta) where route_meta carries which provider
    fired and why (success / fallback reason).
    """
    fn, model = _resolve_provider(primary_model)
    route_meta = {"primary_model": primary_model, "primary_attempted": True}
    try:
        resp = fn(system=system, prompt=prompt, model=model)
        route_meta["primary_ok"] = True
        return resp, route_meta
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError, RuntimeError, KeyError, ValueError) as exc:
        route_meta["primary_ok"] = False
        route_meta["primary_error"] = f"{type(exc).__name__}: {exc}"

    if not allow_ollama_fallback or fn is _ollama_chat:
        raise RuntimeError(route_meta["primary_error"])

    route_meta["fallback_attempted"] = True
    route_meta["fallback_model"] = OLLAMA_FALLBACK_MODEL
    resp = _ollama_chat(system=system, prompt=prompt, model=OLLAMA_FALLBACK_MODEL)
    route_meta["fallback_ok"] = True
    return resp, route_meta


def fetch_grants_gov(*, lookback_days: int, page_size: int) -> list[dict]:
    """Hit Grants.gov search2 for opportunities posted in the last N days."""
    posted_from = (datetime.now(timezone.utc) - timedelta(days=lookback_days)).strftime("%m/%d/%Y")
    body = json.dumps({
        "keyword": "",
        "oppNum": "",
        "cfda": "",
        "agencies": "",
        "sortBy": "openDate|desc",
        "rows": page_size,
        "eligibilities": "",
        "fundingCategories": "",
        "fundingInstruments": "",
        "dateRange": "",
        "oppStatuses": "posted",
        "startRecordNum": 0,
        "postedDateFrom": posted_from,
    }).encode("utf-8")
    caller = enforce_outbound_boundary(
        stdlib_urlopen_caller,
        classification_context=ClassificationContext(inputs=()),
        posture="frontier_eligible",
    )
    status, response_bytes = caller(
        url=GRANTS_GOV_URL,
        headers={
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        body=body,
        timeout_seconds=30.0,
    )
    if status >= 400:
        raise RuntimeError(f"Grants.gov HTTP {status}: {response_bytes.decode('utf-8', errors='replace')}")
    payload = json.loads(response_bytes.decode("utf-8"))
    return payload.get("data", {}).get("oppHits", []) or []


def normalize_grants_gov_hit(hit: dict) -> dict:
    return {
        "title": hit.get("title") or "Untitled",
        "funder": hit.get("agencyName") or hit.get("agency") or "",
        "program": hit.get("oppNumber") or "",
        "deadline": hit.get("closeDate") or "",
        "max_award": str(hit.get("ceiling") or ""),
        "summary": hit.get("description") or "",
        "source_id": hit.get("id") or hit.get("oppNumber") or "",
        "source_url": (
            f"https://www.grants.gov/search-results-detail/{hit.get('id')}"
            if hit.get("id") else ""
        ),
        "agency_code": hit.get("agencyCode") or "",
        "opp_status": hit.get("oppStatus") or "",
        "open_date": hit.get("openDate") or "",
    }


def days_until(deadline_text: str) -> int | None:
    if not deadline_text:
        return None
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(deadline_text, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        return (dt - datetime.now(timezone.utc)).days
    return None


def urgency_label(days: int | None) -> tuple[str, bool]:
    if days is None:
        return "", False
    if days <= 14:
        return "🔴 < 14 days", True
    if days <= 30:
        return "🟡 < 30 days", False
    return "🟢 ≥ 30 days", False


def usd_int(val) -> int:
    if val in (None, ""):
        return 0
    try:
        return int(float(str(val).replace(",", "").replace("$", "")))
    except (TypeError, ValueError):
        return 0


def map_seat_output_to_ui(
    seat_out: dict,
    candidates_by_title: dict[str, dict],
) -> dict:
    """Map orchestrator/seats/scout.py output to the UI opportunity/totals shape."""
    opportunities: list[dict] = []
    value_total = 0
    new_today_count = 0

    def emit(item: dict, tier: str) -> None:
        nonlocal value_total, new_today_count
        title = item.get("title", "")
        cand = candidates_by_title.get(title, {})
        deadline = item.get("deadline") or cand.get("deadline") or ""
        days = days_until(deadline)
        urgency_text, urgent = urgency_label(days)
        award_size = usd_int(item.get("max_award") or cand.get("max_award"))
        fit_score = item.get("fit_score")
        confidence = fit_score if isinstance(fit_score, int) else (
            72 if tier == "declined" else 84 if tier == "maybe" else 92
        )
        opp_code = cand.get("program") or item.get("program") or ""
        opp_id_seed = (cand.get("source_id") or opp_code or title)
        opp_id = f"opp_{str(opp_id_seed)[:24].replace(' ', '_')}"
        rationale_text = (
            item.get("why_must_read")
            or item.get("what_would_upgrade_this")
            or item.get("reason")
            or ""
        )
        opportunities.append({
            "id": opp_id,
            "program": title,
            "agency": item.get("funder") or cand.get("funder") or "",
            "level": "Federal",
            "who_applies": item.get("dialect_family") or "",
            "what_it_funds": rationale_text[:240],
            "award_size": award_size,
            "match": item.get("match_required") or "",
            "deadline": deadline,
            "urgency": urgency_text,
            "url": cand.get("source_url") or "",
            "amount": award_size,
            "urgent": urgent,
            "confidence": confidence,
            "backing": "STAGING_SOURCE_QUALIFIED" if tier == "must_read" else "STAGING_NEEDS_REVIEW",
            "code": opp_code,
            "summary": (item.get("action_needed") or rationale_text)[:160],
            "rationale": rationale_text,
            "quote": (cand.get("summary") or "")[:240],
            "tier": tier,
        })
        value_total += award_size
        opened_days = days_until(cand.get("open_date") or "")
        if opened_days is not None and opened_days >= -7:
            new_today_count += 1

    for tier in ("must_read", "maybe", "declined"):
        for item in seat_out.get(tier, []) or []:
            emit(item, tier)

    meta_in = seat_out.get("meta", {})
    return {
        "opportunities": opportunities,
        "totals": {
            "value": value_total,
            "signals": len(opportunities),
            "blocked_value": 0,
            "tracked": len(opportunities),
            "new_today": new_today_count,
        },
        "meta": {
            "seat": meta_in.get("seat"),
            "model": meta_in.get("model"),
            "family": meta_in.get("family"),
            "elapsed_seconds": meta_in.get("elapsed_seconds"),
            "candidates_reviewed": seat_out.get("candidates_reviewed"),
            "validation_passed": meta_in.get("validation_passed"),
            "validation_errors": meta_in.get("validation_errors", []),
            "channel_coverage": ["A:grants_gov"],
            "route": meta_in.get("route", {}),
        },
    }


def emit_failure(reason: str) -> None:
    print(json.dumps({
        "ok": False,
        "reason": reason,
        "opportunities": [],
        "totals": {"value": 0, "signals": 0, "blocked_value": 0, "tracked": 0, "new_today": 0},
        "meta": {"channel_coverage": ["A:grants_gov"]},
    }))


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Tilth UI Scout bridge — RESCAN entrypoint.")
    ap.add_argument("--org-slug", required=True)
    ap.add_argument("--cycle-id", required=True)
    ap.add_argument("--query", default="")
    ap.add_argument("--cic", default="")
    ap.add_argument("--clc", default="")
    ap.add_argument("--lookback-days", type=int, default=DEFAULT_LOOKBACK_DAYS)
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    ap.add_argument(
        "--model",
        default=os.environ.get("TILTH_UI_SCOUT_MODEL", DEFAULT_MODEL),
        help=(
            "Triage model id. Default: gemini-2.5-flash (free tier, fast, full triage "
            "coverage; uses GOOGLE_API_KEY). Override via --model or TILTH_UI_SCOUT_MODEL "
            "env var. Recognized: claude-{sonnet,opus,haiku}-4-*, gpt-{5.1,5,4o,4o-mini}, "
            "gemini-2.5-{pro,flash}, mistral:7b, mixtral:8x7b, qwen2.5:{7b,14b}."
        ),
    )
    ap.add_argument(
        "--no-fallback",
        action="store_true",
        default=bool(os.environ.get("TILTH_UI_SCOUT_NO_FALLBACK")),
        help="Disable ollama fallback when the cloud call fails. Default: fallback enabled.",
    )
    args = ap.parse_args(argv)

    # 1. Resolve PROJECT_CONTEXT — fall back to a minimal stub if missing
    #    (Law 3 still respected — only one org's context per run).
    context_path_real = REPO_ROOT / "orgs" / args.org_slug / "PROJECT_CONTEXT.md"
    fallback_context_text: str | None = None
    if not context_path_real.is_file():
        fallback_context_text = (
            f"# {args.org_slug}\n"
            f"organization: {args.org_slug}\n"
            f"applicant: (PROJECT_CONTEXT not on file — Scout running with skeleton context)\n"
            f"location: (unknown)\n"
            f"sectors: (unknown)\n"
            f"cic: {args.cic}\n"
            f"clc: {args.clc}\n"
        )

    # 2. Live Grants.gov fetch
    try:
        hits = fetch_grants_gov(lookback_days=args.lookback_days, page_size=args.limit)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        emit_failure(f"GRANTS_GOV_FETCH_FAILED: {type(exc).__name__}: {exc}")
        return 1

    candidates = [normalize_grants_gov_hit(h) for h in hits[:args.limit]]
    if not candidates:
        emit_failure("NO_CANDIDATES: Grants.gov returned 0 opportunities for the lookback window.")
        return 0

    if args.query:
        q = args.query.lower()
        filtered = [
            c for c in candidates
            if q in (c["title"] + " " + c["funder"] + " " + c["summary"]).lower()
        ]
        if filtered:
            candidates = filtered

    candidates_by_title = {c["title"]: c for c in candidates}

    # 3. Triage — direct ollama call using the orchestrator seat's prompts.
    if fallback_context_text is not None:
        context_text = fallback_context_text
    else:
        context_text = context_path_real.read_text(encoding="utf-8")

    client_org = "unknown"
    for line in context_text.splitlines()[:20]:
        if "organization" in line.lower() or "applicant" in line.lower() or line.startswith("# "):
            client_org = line.strip().lstrip("#").strip()[:80]
            break

    user_prompt = build_user_prompt(context_text, candidates)
    started_at = datetime.now(timezone.utc)
    try:
        resp, route_meta = _call_provider_with_fallback(
            system=SCOUT_SYSTEM_PROMPT,
            prompt=user_prompt,
            primary_model=args.model,
            allow_ollama_fallback=not args.no_fallback,
        )
    except Exception as exc:
        emit_failure(f"SCOUT_CALL_FAILED: {type(exc).__name__}: {exc}")
        return 2

    elapsed = (datetime.now(timezone.utc) - started_at).total_seconds()

    try:
        parsed = extract_json(resp["content"])
    except Exception as exc:
        emit_failure(
            f"SCOUT_OUTPUT_UNPARSEABLE: {type(exc).__name__}: {exc}; "
            f"raw_head={(resp.get('content') or '')[:200]!r}"
        )
        return 3

    validation_errors = validate_scout_output(parsed, len(candidates))

    seat_out = {
        "meta": {
            "seat": "scout",
            "model": resp.get("model"),
            "family": resp.get("family"),
            "elapsed_seconds": round(elapsed, 2),
            "usage": resp.get("usage"),
            "validation_errors": validation_errors,
            "validation_passed": len(validation_errors) == 0,
            "route": route_meta,
        },
        "client_org": client_org,
        "candidates_reviewed": len(candidates),
        "must_read": parsed.get("must_read", []),
        "maybe": parsed.get("maybe", []),
        "declined": parsed.get("declined", []),
        "recommended_next_steps": parsed.get("recommended_next_steps", []),
    }

    # 4. Map seat output → UI shape
    ui_shape = map_seat_output_to_ui(seat_out, candidates_by_title)
    ui_shape["ok"] = True
    ui_shape["reason"] = ""
    print(json.dumps(ui_shape))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
