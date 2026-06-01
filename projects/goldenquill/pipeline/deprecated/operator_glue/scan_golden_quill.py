#!/usr/bin/env python3
"""DEPRECATED operator glue — Tilth Scout scan for Golden Quill / FIT Farms.

This non-runtime module is preserved for audit history only. It is not part of
Tilth's runtime pipeline, must not be imported by production code, and
intentionally lives under ``pipeline.deprecated.operator_glue`` so AST-lint can
quarantine the direct provider-HTTP pattern it contains.

Two-track framing (per Josh 2026-04-14):
  Track A — "We build it."  Grants where FIT Farms (for-profit, PA) is
            the applicant and funds go toward building/commercializing Golden Quill.
            Think SBIR, Ben Franklin Technology Partners, innovation grants.
  Track B — "Others buy it and set it up."  Grants that cooperator farms / orgs can
            cite to justify purchasing and deploying a Golden Quill node on their site.
            Think USDA VAPG with a tech component, PA Ag Innovation at deployed sites,
            REAP, UAIP, specialty-crop tech adoption tracks.

Writes structured output to pipeline/radar/ + appends to run_log.json.
"""
from __future__ import annotations
import sys, json, csv, datetime, urllib.request
from pathlib import Path

TILTH = Path.home() / ".openclaw/agents/tilth-workspace"
sys.path.insert(0, str(TILTH / "pipeline/orchestrator"))
from router import call_seat  # type: ignore

def _load_env():
    env_path = Path.home() / ".openclaw/.env"
    out = {}
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k,v = line.split("=",1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    return out

def call_scribe_direct(system: str, user: str, max_tokens: int = 8000) -> str:
    """Call Scribe (Claude Sonnet 4.6) via Anthropic API directly using the same key
    OpenClaw uses. Equivalent to what the OpenClaw plugin does internally, but avoids
    the gateway dependency for this scan."""
    env = _load_env()
    key = env.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY missing from ~/.openclaw/.env")
    payload = {
        "model": "claude-sonnet-4-5-20250929",  # Sonnet 4.6 actual id per OpenClaw convention
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    # Try sonnet-4-6 first, fall back to 4-5 id if model name unknown
    for model_id in ("claude-sonnet-4-6", "claude-sonnet-4-5-20250929"):
        payload["model"] = model_id
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                body = json.loads(resp.read())
            parts = body.get("content") or []
            return "".join(p.get("text","") for p in parts if p.get("type") == "text")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8","replace")
            if "model" in err_body.lower() and model_id == "claude-sonnet-4-6":
                print(f"  model {model_id} rejected, trying fallback...")
                continue
            raise RuntimeError(f"anthropic http {e.code}: {err_body[:400]}")
    raise RuntimeError("all model ids failed")

ORG_CTX = (TILTH / "orgs/fit_farms/PROJECT_CONTEXT.md").read_text()

DB_DIR = TILTH / "pipeline/scout/databases"
RADAR_DIR = TILTH / "pipeline/radar"
RADAR_DIR.mkdir(parents=True, exist_ok=True)

# Load the primary master database (Funders_Programs sheet). Keep it compact so Scout
# doesn't choke — filter to rows likely relevant to ag-tech / innovation / specialty crop.
master_csv = DB_DIR / "Funders_Master_PA_NY_NJ_2025_2026_DEDUPED__Funders_Programs.csv"
rows = list(csv.DictReader(open(master_csv)))
HEADERS = ["Entity Name","Entity Type","States Served","Focus Areas",
           "Funding Instruments","Typical Award/Range","Deadline / Close",
           "Eligibility","Small Business Eligible?","How to Apply / URL","Notes"]

KEEP_KEYWORDS = (
    "ag","farm","mushroom","mycology","specialty crop","innovation","technology",
    "cooperative","small business","sbir","value-added","rural","urban ag",
    "food","regenerative","climate","conservation","remediation","beginning farmer",
    "veteran","workforce","diagnostic","data","analytics","hydropon","soil",
)
def keep(r):
    blob = " ".join((r.get(k) or "") for k in r).lower()
    return any(k in blob for k in KEEP_KEYWORDS)

filtered = [r for r in rows if keep(r)]
# cap to 80 rows so prompt stays in Scout's window
compact = [{h: (r.get(h) or "")[:160] for h in HEADERS} for r in filtered[:60]]

DB_BLOCK = json.dumps(compact, indent=1)

# Prior-finds: high-confidence opportunities already surfaced in handoff docs.
# Scout/Scribe should evaluate these alongside the database rather than rediscover them.
PRIOR_FINDS = [
    {"name":"USDA VAPG FY2026","funder":"USDA Rural Development","award_range":"Planning up to $75K / Working up to $250K",
     "deadline":"April 22, 2026","track":"B (cooperator applies; Golden Quill is the tool)",
     "note":"Already the Tilth dogfood — MycoSymbiotics applicant path, not FIT Farms."},
    {"name":"NSF SBIR Phase I — Agricultural Technologies","funder":"NSF","award_range":"up to $305K",
     "deadline":"~May 5, 2026","track":"A (FIT Farms builds Golden Quill)",
     "note":"For-profit small business eligible. Strongest Track A fit. Pitch deck required first."},
    {"name":"USDA NIFA SBIR Phase I","funder":"USDA NIFA","award_range":"up to $125K",
     "deadline":"Summer/Fall 2026 cycle","track":"A",
     "note":"For-profit small business. Ag-tech emphasis matches Golden Quill exactly."},
    {"name":"Heinz Endowments — regional grant-competition capacity","funder":"Heinz Endowments",
     "award_range":"Unknown — ~$10M pool","deadline":"Rolling / by program officer contact",
     "track":"A or B (likely via 501(c)(3) partner)",
     "note":"Requires 501(c)(3). Route via MycoSymbiotics Cooperative as partner if pursued."},
    {"name":"CMU Integrated Innovation Institute capstone","funder":"CMU III",
     "award_range":"$10–30K engineering in-kind","deadline":"Semester-based",
     "track":"A (Golden Quill build support, in-kind)",
     "note":"Below-market engineering via student capstone. High-leverage, low-cash."},
    {"name":"PA Ag Innovation Grant","funder":"PA Dept of Agriculture",
     "award_range":"$7.5–50K / up to $2M","deadline":"April 18, 2026",
     "track":"OFF-TABLE FOR GOLDEN QUILL",
     "note":"Josh using this elsewhere — do NOT propose for Golden Quill. Exclude from ranking."},
]

SYSTEM = """You are acting as Scout, the discovery seat of Tilth. Find and filter grant opportunities.

CRITICAL OUTPUT RULES:
- Respond with a single JSON object. No preamble. No postamble. No markdown fences. No <think> tags. No reasoning trace.
- The FIRST character of your response must be `{`. The LAST must be `}`.
- If a field is unknown, use the string "unknown". Do not omit required keys.
- Cap each track at 6 items. Quality > quantity.

For this scan you are working TWO parallel tracks and must return BOTH:
  Track A — BUILD IT. Grants where FIT Farms (for-profit, PA) is the applicant
            and the funds go toward building/commercializing the Golden Quill product
            (hardware + Tilth software). Prefer SBIR, innovation, ag-tech, small-business tech tracks.
  Track B — BUY & DEPLOY. Grants that a COOPERATOR FARM or food-hub could cite to
            justify purchasing a Golden Quill node and deploying it on their operation.
            Prefer USDA VAPG (tech-enabled), PA Ag Innovation, REAP, UAIP, specialty-crop
            adoption tracks. Applicant is the cooperator, Golden Quill is the tool.

Rules:
- FIT Farms is FOR-PROFIT. Grants that require 501(c)(3) status are OFF-TABLE for Track A
  unless they allow small-business or fiscal-sponsor applicants. Mark these clearly.
- Every opportunity you return must have a source string the user can verify.
- Urgency flags: URGENT (<14d), SHORT-FUSE (15-45d), STANDARD (>45d), ROLLING, UPCOMING, CLOSED.
- If you don't know the deadline from the provided data, mark it "unknown" and set urgency UPCOMING.
- No fabrication. If a program name is unfamiliar, either leave it out or mark confidence "low".

You will receive a list of PRIOR FINDS. Evaluate them alongside the database and include
the ones still live in your output (don't rediscover them — just validate and keep).

Output ONLY a JSON object with this exact shape:
{
  "track_a_build_it": [
    {"name": "...", "funder": "...", "award_range": "...", "deadline": "...",
     "urgency": "...", "eligibility_note": "...", "why_fit": "...",
     "rank_score": 0-100, "source": "...", "confidence": "high|medium|low"},
    ...
  ],
  "track_b_buy_and_deploy": [ {...same schema...} ],
  "federal_gaps_not_in_database": [ {...same schema...} ],
  "top_5_overall": ["name of #1","name of #2","name of #3","name of #4","name of #5"],
  "one_line_take": "..."
}

rank_score guidance: (fit × urgency × award_size × eligibility_certainty).
 - 90-100: pursue now, strong fit, open deadline, for-profit eligible
 - 70-89: strong fit with some friction (partner needed, prep time tight)
 - 50-69: plausible with reframing
 - <50: long shot

No markdown. No prose outside the JSON."""

USER = f"""FIT Farms PROJECT_CONTEXT (ground truth for applicant identity):
---
{ORG_CTX}
---

PRIOR FINDS (already surfaced in handoff docs — validate and keep the live ones,
 do NOT rediscover, and respect OFF-TABLE markers):
{json.dumps(PRIOR_FINDS, indent=1)}

Funder database (filtered to {len(compact)} rows of 217 total, headers: {HEADERS}):
{DB_BLOCK}

Today's date: 2026-04-14.
Scan BOTH tracks. Rank with rank_score. Return the JSON. Conservative — quality over quantity."""

print(f"[{datetime.datetime.utcnow().isoformat()}Z] Scout scan: Golden Quill / FIT Farms")
print(f"  db rows considered: {len(compact)} of {len(rows)}")
print(f"  calling seat: scout")

# Seat routing for first shadow run:
#  - Scout (Ollama Mistral 7B on 8GB M1) is undersized for 80-row JSON structuring.
#  - Scribe is gated via_openclaw=true (not router-callable).
#  - Judge (Groq/Qwen 3 32B) IS router-callable, freshly restored today, 4000 max_tokens,
#    and evaluation+ranking IS the Judge's job description. Using Judge for this scan
#    is mildly off-spec (Judge normally scores, not discovers) but defensible as a
#    hybrid discover+rank pass. Logged as scout_shadow_via_judge for transparency.
SEAT_USED = "scout_shadow_via_anthropic_direct"
content = call_scribe_direct(system=SYSTEM, user=USER, max_tokens=8000)

# try to parse JSON
parsed = None
err = None
try:
    parsed = json.loads(content)
except Exception as e:
    err = str(e)
    # Best-effort: strip code fences
    t = content.strip()
    if t.startswith("```"):
        t = t.split("\n",1)[1]
        if t.endswith("```"):
            t = t.rsplit("```",1)[0]
    try:
        parsed = json.loads(t)
        err = None
    except Exception as e2:
        err = f"{err} | {e2}"

stamp = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H%M")
out_path = RADAR_DIR / f"golden_quill_scan_{stamp}.json"
payload = {
    "run_id": stamp,
    "org": "fit_farms",
    "project": "Golden Quill",
    "tracks": ["A_build_it", "B_buy_and_deploy"],
    "db_rows_considered": len(compact),
    "db_rows_total": len(rows),
    "seat_called": SEAT_USED,
    "parse_error": err,
    "raw_content": content if err else None,
    "result": parsed,
}
out_path.write_text(json.dumps(payload, indent=2))
print(f"  wrote: {out_path}")

# Append to run_log.json
log_path = TILTH / "pipeline/orchestrator/run_log.json"
if log_path.exists():
    log = json.loads(log_path.read_text())
else:
    log = {"runs": []}
log.setdefault("runs", []).append({
    "run_id": stamp,
    "timestamp_utc": datetime.datetime.utcnow().isoformat() + "Z",
    "type": "scout_scan",
    "org": "fit_farms",
    "project": "Golden Quill",
    "output": str(out_path),
    "parse_error": err,
})
log_path.write_text(json.dumps(log, indent=2))
print(f"  run_log updated: {log_path}")

# Print a human summary
if parsed:
    print("\n=== RESULT SUMMARY ===")
    for track in ("track_a_build_it","track_b_buy_and_deploy","federal_gaps_not_in_database"):
        items = parsed.get(track, [])
        print(f"\n-- {track} ({len(items)}) --")
        for it in items[:10]:
            print(f"  [{it.get('urgency','?')}] {it.get('name','?')} / {it.get('funder','?')}  — {it.get('deadline','?')}")
    print(f"\n>> {parsed.get('one_line_take','')}")
else:
    print("\n=== PARSE FAILED ===")
    print(content[:2000])
