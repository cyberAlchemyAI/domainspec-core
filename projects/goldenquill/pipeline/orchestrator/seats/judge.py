#!/usr/bin/env python3
"""
Judge seat — scores a draft against a funder rubric.

Input:
    --draft  <path>    Markdown or plain-text draft
    --rubric <path>    Rubric JSON (extracted from RFA)
    --rfa    <path>    (optional) RFA text for context
    --out    <path>    Where to write judge.json

Output JSON schema:
{
  "meta": {
    "seat": "judge",
    "model": "...",
    "family": "...",
    "timestamp": "...",
    "rubric": "vapg_fy26",
    "draft_path": "..."
  },
  "total_score": 78,
  "max_score": 100,
  "recommendation": "competitive" | "marginal" | "not_ready",
  "criteria": [
    {
      "id": "a.i",
      "name": "Technological feasibility",
      "max_points": 10,
      "score": 7,
      "tier_matched": "5-7",
      "evidence": "Draft para 3 cites ...",
      "missing": ["Marketing experience not addressed"],
      "notes": "..."
    },
    ...
  ],
  "overall_notes": "..."
}

Law 5 & Rule 2: Judge validates its own output before writing — all criteria
must be scored, total must be <= max, evidence strings must be non-empty.
"""

from __future__ import annotations
import argparse
import json
import sys
import time
from pathlib import Path

# Allow import of router from parent dir
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from router import call_seat  # noqa: E402


SYSTEM_PROMPT = """You are Judge — one seat in a multi-family AI council that evaluates grant applications.

Your job: score a draft against the funder's own rubric, strictly.

Rules:
1. Score ONLY against the rubric provided. Do not import criteria from other programs.
2. For each criterion, state (a) the score, (b) which tier band matched, (c) specific evidence from the draft (quoted or paraphrased with location), and (d) what is missing.
3. If the draft does not address a must_address item, flag it in "missing".
4. Be parsimonious with points. Reviewers reading actual applications rarely give max scores.
5. Return ONLY a JSON object matching the schema. No preamble, no markdown fences, no commentary.
6. Never invent facts about the applicant. If evidence is missing, the score reflects missing evidence.

Output JSON schema:
{
  "total_score": int,
  "recommendation": "competitive" | "marginal" | "not_ready",
  "criteria": [
    {"id": str, "name": str, "max_points": int, "score": int,
     "tier_matched": str, "evidence": str, "missing": [str], "notes": str}
  ],
  "overall_notes": str
}
"""


def build_user_prompt(draft: str, rubric: dict, rfa: str | None) -> str:
    parts = []
    parts.append("FUNDER RUBRIC (authoritative — the only thing you score against):")
    parts.append(json.dumps(rubric, indent=2))
    parts.append("")
    if rfa:
        parts.append("RFA EXCERPT (context only — do not score against this):")
        parts.append(rfa[:6000])
        parts.append("")
    parts.append("APPLICANT DRAFT (score this):")
    parts.append(draft)
    parts.append("")
    parts.append("Return the JSON object and nothing else.")
    return "\n".join(parts)


def strip_fences(s: str) -> str:
    s = s.strip()
    if s.startswith("```"):
        # Remove opening fence
        first_nl = s.find("\n")
        s = s[first_nl + 1 :] if first_nl > 0 else s[3:]
        if s.endswith("```"):
            s = s[:-3]
    return s.strip()


def extract_json(text: str) -> dict:
    """Locate first top-level JSON object and parse it."""
    t = strip_fences(text)
    # Find first { and try to parse from there progressively
    start = t.find("{")
    if start < 0:
        raise ValueError("no JSON object found in model output")
    # Use JSON decoder raw_decode to find the full object
    decoder = json.JSONDecoder()
    obj, _ = decoder.raw_decode(t[start:])
    return obj


def validate(out: dict, rubric: dict) -> list[str]:
    """Return list of validation errors. Empty = passed."""
    errs: list[str] = []
    if "total_score" not in out or not isinstance(out["total_score"], int):
        errs.append("total_score missing or not int")
    if "criteria" not in out or not isinstance(out["criteria"], list):
        errs.append("criteria missing or not list")
        return errs

    # Collect expected criterion ids from rubric (flat list of leaf criteria)
    expected_ids = set()
    max_total = 0
    for crit in rubric.get("scoring_criteria", []):
        if "subcriteria" in crit:
            for sub in crit["subcriteria"]:
                expected_ids.add(sub["id"])
                if isinstance(sub.get("max_points"), int):
                    max_total += sub["max_points"]
        else:
            expected_ids.add(crit["id"])
            if isinstance(crit.get("max_points"), int):
                max_total += crit["max_points"]

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

    # No total_score drift check here — we auto-correct in run() using per-criterion sum
    # (per-criterion scores are authoritative; LLMs are unreliable at addition).

    if out.get("recommendation") not in ("competitive", "marginal", "not_ready"):
        errs.append(f"recommendation invalid: {out.get('recommendation')}")
    return errs


def run(draft_path: Path, rubric_path: Path, rfa_path: Path | None, out_path: Path) -> dict:
    draft = draft_path.read_text(encoding="utf-8")
    rubric = json.loads(rubric_path.read_text(encoding="utf-8"))
    rfa = rfa_path.read_text(encoding="utf-8") if rfa_path and rfa_path.exists() else None

    user_prompt = build_user_prompt(draft, rubric, rfa)
    t0 = time.time()
    resp = call_seat("judge", [{"role": "user", "content": user_prompt}], system=SYSTEM_PROMPT)
    elapsed = time.time() - t0

    try:
        scored = extract_json(resp["content"])
    except Exception as e:
        raise RuntimeError(f"Judge output not parseable as JSON: {e}\n---\n{resp['content'][:500]}")

    errs = validate(scored, rubric)

    # Authoritative total = sum of per-criterion scores. Log correction if model drifted.
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

    meta = {
        "seat": "judge",
        "model": resp["model"],
        "family": resp["family"],
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "rubric_file": str(rubric_path),
        "draft_path": str(draft_path),
        "elapsed_seconds": round(elapsed, 2),
        "usage": resp.get("usage"),
        "validation_errors": errs,
        "validation_passed": len(errs) == 0,
        "total_score_correction": total_correction,
    }
    # Compute rubric's max possible total correctly:
    # - If a criterion has subcriteria, sum the subcriteria max_points
    # - Otherwise use the criterion's own max_points
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

    out = {
        "meta": meta,
        "total_score": authoritative_total,
        "max_score": max_total,
        "recommendation": scored.get("recommendation"),
        "criteria": scored.get("criteria", []),
        "overall_notes": scored.get("overall_notes", ""),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Judge seat — rubric scoring.")
    ap.add_argument("--draft", required=True, type=Path)
    ap.add_argument("--rubric", required=True, type=Path)
    ap.add_argument("--rfa", type=Path, default=None)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args(argv)

    out = run(args.draft, args.rubric, args.rfa, args.out)
    print(f"[judge/{out['meta']['family']}/{out['meta']['model']}] {out['total_score']}/{out['max_score']} — {out['recommendation']}")
    if not out["meta"]["validation_passed"]:
        print("VALIDATION ERRORS:", file=sys.stderr)
        for e in out["meta"]["validation_errors"]:
            print(f"  - {e}", file=sys.stderr)
        return 2
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
