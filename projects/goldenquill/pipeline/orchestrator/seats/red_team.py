#!/usr/bin/env python3
"""
Red Team seat — adversarial review of a grant draft.

Fires on every draft (per routing.yaml debate_policy.trigger=every_draft).
Produces BOTH a score (commensurable with Judge) AND a prosecutorial memo
(richer than a number). This is the second voice in the council.

Law 4 / Rule 3: If |judge_score - red_team_score| >= disagreement_threshold,
the Logician flags "council split" and the human breaks the tie. Red Team
does NOT try to agree with Judge. Its job is to find the weakest parts.

Input:
    --draft  <path>    Markdown or plain-text draft
    --rubric <path>    Rubric JSON (same one Judge used)
    --rfa    <path>    (optional) RFA text
    --judge  <path>    (optional) judge.json — shown for context, NOT as authority
    --out    <path>    Where to write red_team.json

Output JSON schema:
{
  "meta": {...},
  "total_score": int,
  "max_score": int,
  "recommendation": "competitive" | "marginal" | "not_ready",
  "criteria": [
    {"id": str, "name": str, "max_points": int, "score": int,
     "tier_matched": str, "evidence": str, "missing": [str], "notes": str}
  ],
  "attack_memo": {
    "top_weaknesses": [
      {"severity": "high"|"medium"|"low", "claim": str, "why_it_fails": str,
       "what_a_reviewer_would_say": str, "fix_hint": str}
    ],
    "unsupported_assertions": [str],
    "dialect_mismatches": [str],   # places draft speaks wrong dialect for funder
    "boundary_drift": [str],       # places draft exceeds RFA scope
    "overall_verdict": str
  }
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


SYSTEM_PROMPT = """You are Red Team — the adversarial seat in a multi-family AI grant-writing council.

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
- Be specific. "Weak case for feasibility" is useless. "Paragraph 3 asserts market demand but cites no buyer interviews, distributor commitments, or comparable products" is useful.
- Return ONLY a JSON object matching the schema. No preamble, no markdown fences.
- Do not soften your critique to match Judge. Disagreement is a feature.

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
"""


def slim_rubric(rubric: dict) -> dict:
    """Compact rubric view — id/name/max_points only, drops tier descriptions and must_address.
    Reduces token count so Red Team's response has room within free-tier TPM."""
    slim_criteria = []
    for crit in rubric.get("scoring_criteria", []):
        subs = crit.get("subcriteria")
        if subs:
            for s in subs:
                slim_criteria.append({
                    "id": s.get("id"),
                    "name": s.get("name"),
                    "max_points": s.get("max_points"),
                    "parent": crit.get("name"),
                })
        else:
            slim_criteria.append({
                "id": crit.get("id"),
                "name": crit.get("name"),
                "max_points": crit.get("max_points"),
            })
    return {
        "program": rubric.get("meta", {}).get("program"),
        "max_score": rubric.get("meta", {}).get("max_score"),
        "criteria": slim_criteria,
    }


def build_user_prompt(draft: str, rubric: dict, rfa: str | None, judge: dict | None) -> str:
    parts = []
    parts.append("FUNDER RUBRIC (score against this — id/name/max_points per criterion):")
    parts.append(json.dumps(slim_rubric(rubric), indent=2))
    parts.append("")
    if rfa:
        parts.append("RFA EXCERPT (for context and scope checking):")
        parts.append(rfa[:6000])
        parts.append("")
    if judge:
        # Trimmed view: headline numbers only, no per-criterion detail.
        # Red Team should form its own criterion-level view, not anchor to Judge's.
        judge_view = {
            "total_score": judge.get("total_score"),
            "max_score": judge.get("max_score"),
            "recommendation": judge.get("recommendation"),
            "overall_notes": (judge.get("overall_notes") or "")[:400],
        }
        parts.append("JUDGE SCORING SUMMARY (context only — DO NOT anchor to this):")
        parts.append(json.dumps(judge_view, indent=2))
        parts.append("")
    parts.append("APPLICANT DRAFT (attack this):")
    parts.append(draft)
    parts.append("")
    parts.append("Return the JSON object and nothing else. Remember: disagreement with Judge is a feature, not a bug.")
    parts.append("BE TERSE. Each string field: one sentence, maximum 25 words. Evidence cites paragraph/section, does not quote long passages. top_weaknesses: list at most 5, not more.")
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


def validate(out: dict, rubric: dict) -> list[str]:
    errs: list[str] = []
    if "total_score" not in out or not isinstance(out["total_score"], int):
        errs.append("total_score missing or not int")
    if "criteria" not in out or not isinstance(out["criteria"], list):
        errs.append("criteria missing or not list")
        return errs

    expected_ids = set()
    for crit in rubric.get("scoring_criteria", []):
        if "subcriteria" in crit:
            for sub in crit["subcriteria"]:
                expected_ids.add(sub["id"])
        else:
            expected_ids.add(crit["id"])

    seen_ids = set()
    for c in out["criteria"]:
        if "id" not in c:
            errs.append("criterion missing id")
            continue
        seen_ids.add(c["id"])
        if "score" not in c or not isinstance(c["score"], int):
            errs.append(f"criterion {c['id']}: score missing or not int")
        if "max_points" in c and isinstance(c["max_points"], int):
            if isinstance(c.get("score"), int) and c["score"] > c["max_points"]:
                errs.append(f"criterion {c['id']}: score {c['score']} > max {c['max_points']}")
        if not c.get("evidence"):
            errs.append(f"criterion {c['id']}: evidence empty")

    missing_ids = expected_ids - seen_ids
    if missing_ids:
        errs.append(f"unscored criteria: {sorted(missing_ids)}")

    memo = out.get("attack_memo")
    if not isinstance(memo, dict):
        errs.append("attack_memo missing or not dict")
    else:
        if not isinstance(memo.get("top_weaknesses"), list) or not memo["top_weaknesses"]:
            errs.append("attack_memo.top_weaknesses missing or empty — Red Team must produce at least one weakness")
        else:
            for i, w in enumerate(memo["top_weaknesses"]):
                for key in ("severity", "claim", "why_it_fails", "what_a_reviewer_would_say"):
                    if not w.get(key):
                        errs.append(f"attack_memo.top_weaknesses[{i}]: missing '{key}'")
        if not memo.get("overall_verdict"):
            errs.append("attack_memo.overall_verdict empty")

    # No total_score drift check — we auto-correct using per-criterion sum in run().

    if out.get("recommendation") not in ("competitive", "marginal", "not_ready"):
        errs.append(f"recommendation invalid: {out.get('recommendation')}")
    return errs


def run(draft_path: Path, rubric_path: Path, rfa_path: Path | None,
        judge_path: Path | None, out_path: Path) -> dict:
    draft = draft_path.read_text(encoding="utf-8")
    rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
    rfa = rfa_path.read_text(encoding="utf-8") if rfa_path and rfa_path.exists() else None
    judge = None
    if judge_path and judge_path.exists():
        judge = json.loads(judge_path.read_text(encoding="utf-8"))

    user_prompt = build_user_prompt(draft, rubric, rfa, judge)
    t0 = time.time()
    resp = call_seat("red_team", [{"role": "user", "content": user_prompt}], system=SYSTEM_PROMPT)
    elapsed = time.time() - t0

    try:
        scored = extract_json(resp["content"])
    except Exception as e:
        raise RuntimeError(f"Red Team output not parseable: {e}\n---\n{resp['content'][:500]}")

    errs = validate(scored, rubric)

    # Authoritative total = sum of per-criterion scores
    reported_total = scored.get("total_score")
    computed_total = sum(
        c.get("score", 0) for c in scored.get("criteria", [])
        if isinstance(c.get("score"), int)
    )
    total_correction = None
    if isinstance(reported_total, int) and reported_total != computed_total:
        total_correction = {
            "model_reported": reported_total,
            "computed_from_criteria": computed_total,
            "delta": computed_total - reported_total,
        }
    authoritative_total = computed_total

    max_total = 0
    for crit in rubric.get("scoring_criteria", []):
        subs = crit.get("subcriteria")
        if subs:
            for sub in subs:
                if isinstance(sub.get("max_points"), int):
                    max_total += sub["max_points"]
        elif isinstance(crit.get("max_points"), int):
            max_total += crit["max_points"]
    if not max_total:
        max_total = rubric.get("meta", {}).get("max_score", 100)

    meta = {
        "seat": "red_team",
        "model": resp["model"],
        "family": resp["family"],
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "rubric_file": str(rubric_path),
        "draft_path": str(draft_path),
        "judge_file": str(judge_path) if judge_path else None,
        "elapsed_seconds": round(elapsed, 2),
        "usage": resp.get("usage"),
        "validation_errors": errs,
        "validation_passed": len(errs) == 0,
        "total_score_correction": total_correction,
    }

    out = {
        "meta": meta,
        "total_score": authoritative_total,
        "max_score": max_total,
        "recommendation": scored.get("recommendation"),
        "criteria": scored.get("criteria", []),
        "attack_memo": scored.get("attack_memo", {}),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Red Team seat — adversarial review.")
    ap.add_argument("--draft", required=True, type=Path)
    ap.add_argument("--rubric", required=True, type=Path)
    ap.add_argument("--rfa", type=Path, default=None)
    ap.add_argument("--judge", type=Path, default=None,
                    help="Path to judge.json (context only, not authority)")
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args(argv)

    out = run(args.draft, args.rubric, args.rfa, args.judge, args.out)
    n_weak = len(out["attack_memo"].get("top_weaknesses", []))
    print(f"[red_team/{out['meta']['family']}/{out['meta']['model']}] "
          f"{out['total_score']}/{out['max_score']} — {out['recommendation']} "
          f"({n_weak} weaknesses flagged)")
    if not out["meta"]["validation_passed"]:
        print("VALIDATION ERRORS:", file=sys.stderr)
        for e in out["meta"]["validation_errors"]:
            print(f"  - {e}", file=sys.stderr)
        return 2
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
