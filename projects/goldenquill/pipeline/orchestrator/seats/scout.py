#!/usr/bin/env python3
"""
Scout seat — opportunity discovery and filtering.

Unlike the scoring seats, Scout is the front of the pipeline: it finds and
ranks grant opportunities against a client's PROJECT_CONTEXT. It does NOT
write. It does NOT score drafts. It produces a ranked shortlist.

v0.1 scope:
  - Read candidate RFAs from a directory (each file = one opportunity summary)
  - Read client PROJECT_CONTEXT.md
  - Filter: hard constraints (eligibility, deadline, amount, geography)
  - Rank: soft fit (sector, project type, funder dialect match)
  - Output a ranked shortlist with must_read / maybe / declined tiers

Future:
  - Fetchers for Grants.gov API, SAM.gov API, Candid API (separate modules)
  - RSS/email parsing for Sentinel integration
  - Multi-client cross-reference (Law 3 — org isolation enforced by caller,
    never by Scout reading multiple contexts in one run)

Input:
    --context     <path>   PROJECT_CONTEXT.md for the client
    --candidates  <path>   Directory of RFA candidate files (.md, .json, .txt)
                           OR single JSON list of opportunities
    --out         <path>   Where to write radar.json

Output JSON:
{
  "meta": {...},
  "client_org": str,
  "candidates_reviewed": int,
  "must_read": [{"title": str, "fit_score": int, "why": str, "deadline": str, ...}],
  "maybe": [...],
  "declined": [{"title": str, "reason": str}],
  "recommended_next_steps": [str]
}
"""

from __future__ import annotations
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from router import call_seat  # noqa: E402


SYSTEM_PROMPT = """You are Scout — the opportunity discovery seat in a multi-family AI grant-writing council.

Your job: given a client's PROJECT_CONTEXT and a set of candidate grant opportunities, decide which are worth the applicant's time and which are not. You are NOT a matchmaker that says "yes" to everything. A ruthless no is as valuable as a hot yes.

You work in three tiers:

1. MUST_READ — opportunities where the fit is strong AND the timing works AND the applicant is clearly eligible. These deserve an immediate deep read and likely a draft kickoff.

2. MAYBE — partial fit, or fit is strong but timing/eligibility/match requirements create friction. Flag what would have to be true to upgrade this to must_read.

3. DECLINED — hard mismatch on eligibility, scope, deadline already passed, geography, applicant type, grant amount too small to justify the writing cost. State the reason briefly.

For each opportunity, assess:
- Eligibility (hard gate — does the applicant type match?)
- Scope alignment (soft — does the project fit what this program funds?)
- Timing (when's the deadline? Is there enough runway to write?)
- Match requirement (does the applicant have the required cash/in-kind match?)
- Funder dialect (conservative / centrist / progressive / soul-fire — does the applicant's framing fit this funder?)
- Admin-risk terms (language in the RFA that could backfire if mirrored uncritically)

Rules:
- Never invent data about the applicant. Use ONLY what's in the PROJECT_CONTEXT.
- If the PROJECT_CONTEXT has [NEEDED] fields, flag them in "recommended_next_steps" — do not decline based on missing data alone.
- Be specific about WHY. "Low fit" is useless. "Funder prioritizes urban agriculture; applicant is rural PA; only competitive under regional set-asides" is useful.
- Deadlines within 14 days get an auto "high urgency" note regardless of tier.
- Return ONLY a JSON object matching the schema. No preamble, no markdown fences.

Output JSON schema:
{
  "must_read": [
    {"title": str, "funder": str, "program": str, "deadline": str,
     "max_award": str, "match_required": str, "fit_score": int,
     "why_must_read": str, "dialect_family": str, "action_needed": str}
  ],
  "maybe": [
    {"title": str, "funder": str, "deadline": str, "fit_score": int,
     "what_would_upgrade_this": str, "why_not_must_read": str}
  ],
  "declined": [
    {"title": str, "funder": str, "reason": str, "decline_category": str}
  ],
  "recommended_next_steps": [str]
}
"""


def load_candidates(candidates_path: Path) -> list[dict]:
    """Load candidate RFAs from a directory of files or a single JSON list."""
    items: list[dict] = []
    if candidates_path.is_file():
        text = candidates_path.read_text(encoding="utf-8")
        try:
            data = json.loads(text)
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and "opportunities" in data:
                return data["opportunities"]
        except json.JSONDecodeError:
            # Single markdown/text file treated as one candidate
            return [{"title": candidates_path.stem, "body": text}]
    if candidates_path.is_dir():
        for f in sorted(candidates_path.iterdir()):
            if f.is_file() and f.suffix in (".md", ".txt", ".json"):
                if f.suffix == ".json":
                    try:
                        data = json.loads(f.read_text(encoding="utf-8"))
                        if isinstance(data, list):
                            items.extend(data)
                        else:
                            items.append(data)
                        continue
                    except json.JSONDecodeError:
                        pass
                items.append({
                    "title": f.stem,
                    "source_file": str(f),
                    "body": f.read_text(encoding="utf-8"),
                })
    return items


def build_user_prompt(context: str, candidates: list[dict]) -> str:
    parts = []
    parts.append("CLIENT PROJECT_CONTEXT (authoritative — do not invent beyond this):")
    parts.append(context[:6000])
    parts.append("")
    parts.append(f"CANDIDATE OPPORTUNITIES ({len(candidates)} to review):")
    # Trim each candidate body so the prompt fits
    for i, c in enumerate(candidates, start=1):
        body = c.get("body") or c.get("description") or ""
        slim = {
            "n": i,
            "title": c.get("title", f"candidate_{i}"),
            "funder": c.get("funder"),
            "program": c.get("program"),
            "deadline": c.get("deadline"),
            "max_award": c.get("max_award"),
            "summary": (body[:800] if body else c.get("summary", "")),
        }
        parts.append(json.dumps(slim, indent=2))
        parts.append("")
    parts.append("Return the JSON object and nothing else.")
    parts.append("BE TERSE. Each string field: one sentence, maximum 25 words. Prioritize ruthlessly — not every candidate belongs in must_read.")
    return "\n".join(parts)


def strip_fences(s: str) -> str:
    s = s.strip()
    if s.startswith("```"):
        first_nl = s.find("\n")
        s = s[first_nl + 1 :] if first_nl > 0 else s[3:]
        if s.endswith("```"):
            s = s[:-3]
    return s.strip()


def extract_json(text: str) -> dict:
    t = strip_fences(text)
    start = t.find("{")
    if start < 0:
        raise ValueError("no JSON object found in model output")
    decoder = json.JSONDecoder()
    obj, _ = decoder.raw_decode(t[start:])
    return obj


def validate(out: dict, n_candidates: int) -> list[str]:
    errs: list[str] = []
    for key in ("must_read", "maybe", "declined", "recommended_next_steps"):
        if key not in out or not isinstance(out[key], list):
            errs.append(f"{key} missing or not list")

    if all(isinstance(out.get(k), list) for k in ("must_read", "maybe", "declined")):
        total = len(out["must_read"]) + len(out["maybe"]) + len(out["declined"])
        if total != n_candidates:
            errs.append(
                f"candidate accounting: got {total} triaged vs {n_candidates} input"
            )

    for i, item in enumerate(out.get("must_read", [])):
        if not item.get("title"):
            errs.append(f"must_read[{i}]: title empty")
        if not item.get("why_must_read"):
            errs.append(f"must_read[{i}]: why_must_read empty")
        fs = item.get("fit_score")
        if not isinstance(fs, int) or not (0 <= fs <= 100):
            errs.append(f"must_read[{i}]: fit_score invalid: {fs}")

    for i, item in enumerate(out.get("declined", [])):
        if not item.get("title"):
            errs.append(f"declined[{i}]: title empty")
        if not item.get("reason"):
            errs.append(f"declined[{i}]: reason empty")

    return errs


def run(context_path: Path, candidates_path: Path, out_path: Path) -> dict:
    context = context_path.read_text(encoding="utf-8")
    candidates = load_candidates(candidates_path)
    if not candidates:
        raise RuntimeError(f"no candidates found at {candidates_path}")

    # Try to extract client org name from context
    client_org = "unknown"
    for line in context.splitlines()[:20]:
        if "organization" in line.lower() or "applicant" in line.lower() or line.startswith("# "):
            client_org = line.strip().lstrip("#").strip()[:80]
            break

    user_prompt = build_user_prompt(context, candidates)
    t0 = time.time()
    resp = call_seat("scout", [{"role": "user", "content": user_prompt}], system=SYSTEM_PROMPT)
    elapsed = time.time() - t0

    try:
        parsed = extract_json(resp["content"])
    except Exception as e:
        raise RuntimeError(f"Scout output not parseable: {e}\n---\n{resp['content'][:500]}")

    errs = validate(parsed, len(candidates))

    meta = {
        "seat": "scout",
        "model": resp["model"],
        "family": resp["family"],
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "context_path": str(context_path),
        "candidates_path": str(candidates_path),
        "elapsed_seconds": round(elapsed, 2),
        "usage": resp.get("usage"),
        "validation_errors": errs,
        "validation_passed": len(errs) == 0,
    }

    out = {
        "meta": meta,
        "client_org": client_org,
        "candidates_reviewed": len(candidates),
        "must_read": parsed.get("must_read", []),
        "maybe": parsed.get("maybe", []),
        "declined": parsed.get("declined", []),
        "recommended_next_steps": parsed.get("recommended_next_steps", []),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Scout seat — opportunity discovery.")
    ap.add_argument("--context", required=True, type=Path,
                    help="PROJECT_CONTEXT.md for the client (one org per run — Law 3)")
    ap.add_argument("--candidates", required=True, type=Path,
                    help="Directory of RFA candidates OR single JSON list")
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args(argv)

    out = run(args.context, args.candidates, args.out)
    print(f"[scout/{out['meta']['family']}/{out['meta']['model']}] "
          f"{out['candidates_reviewed']} candidates → "
          f"{len(out['must_read'])} must_read, "
          f"{len(out['maybe'])} maybe, "
          f"{len(out['declined'])} declined")
    if not out["meta"]["validation_passed"]:
        print("VALIDATION ERRORS:", file=sys.stderr)
        for e in out["meta"]["validation_errors"]:
            print(f"  - {e}", file=sys.stderr)
        return 2
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
