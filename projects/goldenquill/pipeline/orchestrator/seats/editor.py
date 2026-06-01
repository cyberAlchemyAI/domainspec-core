#!/usr/bin/env python3
"""
Editor seat — clarity pass over Scribe's draft.

Per the Tilth spec: reads the draft through different eyes than the scorer.
Flags jargon, hedge language, buried claims, and misplaced goal/output/outcome/
objective distinctions. For every issue, offers 2-3 concrete replacement
options the applicant can pick from. Does NOT rewrite the draft silently —
that's Law 4 (Apolitical Sector Language): the applicant approves each change.

Editor's job is "make this accessible to people who know their work but don't
write grants for a living." It is not adversarial (that's Red Team's job).

Input:
    --draft  <path>    Markdown draft from Scribe
    --rfa    <path>    (optional) RFA for dialect / scope reference
    --out    <path>    Where to write editor.json

Output JSON schema:
{
  "meta": {...},
  "overall_readability": {
    "score_10": int,
    "grade_level_estimate": str,
    "verdict": str
  },
  "taxonomy_check": {
    "goals_identified": [str],
    "outputs_identified": [str],
    "outcomes_identified": [str],
    "objectives_identified": [str],
    "miscategorizations": [{"excerpt": str, "stated_as": str, "should_be": str, "why": str}]
  },
  "issues": [
    {
      "id": str,
      "location": str,                    # section or paragraph reference
      "issue_type": str,                  # "jargon" | "hedge_language" | "buried_claim" |
                                          # "goal_output_confusion" | "passive_voice" |
                                          # "dialect_mismatch" | "redundancy" | "ambiguity"
      "severity": "high" | "medium" | "low",
      "excerpt": str,                     # the phrase or sentence at issue
      "why_it_hurts": str,                # why this makes the draft less accessible
      "replacements": [str, str, str]     # 2-3 concrete alternatives — NEVER one option
    }
  ],
  "quick_wins": [str],                    # top 3-5 highest-leverage edits
  "terms_to_verify": [str]                # admin-risk register candidates (flagged terms)
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


SYSTEM_PROMPT = """You are Editor — the clarity seat in a multi-family AI grant-writing council.

Your job is to make the draft accessible. You read with fresh eyes, as if you've never seen this project before. You are NOT scoring the rubric (Judge does that). You are NOT attacking the argument (Red Team does that). You are making sure someone skimming this at hour four of a twelve-hour review day can follow it.

Your four tasks:

1. TAXONOMY CHECK. Grant reviewers expect crisp distinctions:
   - Goals: the "north star" / mission-level aims
   - Objectives: concrete, time-bound targets that get you toward goals
   - Outputs: tangible deliverables produced during the project (reports, events, products, trainings delivered)
   - Outcomes: changes in the world that result from the outputs (knowledge gained, practices adopted, revenue generated)
   Drafts routinely mix these up. Identify what's in the draft, and flag any miscategorizations with a short "why" explanation.

2. ISSUE FLAGGING. For each clarity problem, produce:
   - location (section or paragraph reference — cite the heading if any)
   - issue_type (one of the enumerated types below)
   - severity (high / medium / low)
   - excerpt (the exact phrase)
   - why_it_hurts (one sentence — what a reviewer would think)
   - replacements: **always 2 or 3 options**, never just one. The applicant picks. This is a non-negotiable rule — it preserves the applicant's voice.

   Issue types:
   - jargon (unexplained sector-specific term)
   - hedge_language (weaselly modifiers: "may", "could", "hopefully", "try to")
   - buried_claim (the strongest point is in the third sentence of the paragraph)
   - goal_output_confusion (see taxonomy above)
   - passive_voice (where active voice would be clearer and stronger)
   - dialect_mismatch (tone/vocabulary wrong for this funder type)
   - redundancy (same idea repeated without adding anything)
   - ambiguity (a pronoun or reference that's unclear)

3. QUICK WINS. Identify the top 3-5 highest-leverage edits across the whole draft. These are the things that, fixed, would noticeably raise the draft's clarity score.

4. TERMS TO VERIFY. Flag any terms that could be admin-risk (e.g., "equity", "DEI", "climate justice", "Indigenous", "underserved", "environmental justice") — not to censor, but because the Logician's admin-risk register requires applicant approval before these are used. List them so Josh can decide.

Rules:
- Never propose a rewrite of the whole draft. Point-fix only.
- Always offer 2-3 replacements per issue. Never 1, never more than 3.
- Stay specific. "Tighten the intro" is useless. "Paragraph 2 opens with 'It is important to note that' — cut those six words; sentence works without them" is useful.
- Do not invent facts. If a section lacks substance, flag "ambiguity" with severity high; do not suggest replacement text that adds claims not in the original.
- Return ONLY a JSON object matching the schema. No preamble, no markdown fences.

Output JSON schema:
{
  "overall_readability": {"score_10": int, "grade_level_estimate": str, "verdict": str},
  "taxonomy_check": {
    "goals_identified": [str],
    "outputs_identified": [str],
    "outcomes_identified": [str],
    "objectives_identified": [str],
    "miscategorizations": [{"excerpt": str, "stated_as": str, "should_be": str, "why": str}]
  },
  "issues": [
    {"id": str, "location": str, "issue_type": str, "severity": str,
     "excerpt": str, "why_it_hurts": str, "replacements": [str]}
  ],
  "quick_wins": [str],
  "terms_to_verify": [str]
}
"""


def build_user_prompt(draft: str, rfa: str | None) -> str:
    parts = []
    if rfa:
        parts.append("FUNDER RFA EXCERPT (for dialect and scope reference only):")
        parts.append(rfa[:4000])
        parts.append("")
    parts.append("APPLICANT DRAFT (pass through clarity edit):")
    parts.append(draft)
    parts.append("")
    parts.append("Return the JSON object and nothing else. Remember: 2-3 replacement options per issue — never 1, never more than 3.")
    parts.append("BE TERSE. Each string: one sentence, maximum 30 words. Keep issues list focused (top 12-15 issues max).")
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


VALID_ISSUE_TYPES = {
    "jargon", "hedge_language", "buried_claim", "goal_output_confusion",
    "passive_voice", "dialect_mismatch", "redundancy", "ambiguity",
}
VALID_SEVERITIES = {"high", "medium", "low"}


def validate(out: dict) -> list[str]:
    errs: list[str] = []

    readability = out.get("overall_readability")
    if not isinstance(readability, dict):
        errs.append("overall_readability missing or not dict")
    else:
        s = readability.get("score_10")
        if not isinstance(s, int) or not (0 <= s <= 10):
            errs.append(f"overall_readability.score_10 invalid: {s}")

    tax = out.get("taxonomy_check")
    if not isinstance(tax, dict):
        errs.append("taxonomy_check missing or not dict")
    else:
        for key in ("goals_identified", "outputs_identified",
                    "outcomes_identified", "objectives_identified",
                    "miscategorizations"):
            if key not in tax:
                errs.append(f"taxonomy_check.{key} missing")

    issues = out.get("issues")
    if not isinstance(issues, list):
        errs.append("issues missing or not list")
        return errs
    if not issues:
        errs.append("issues list is empty — Editor must flag at least one issue or state none found explicitly")

    for i, iss in enumerate(issues):
        prefix = f"issues[{i}]"
        if iss.get("issue_type") not in VALID_ISSUE_TYPES:
            errs.append(f"{prefix}: issue_type invalid: {iss.get('issue_type')}")
        if iss.get("severity") not in VALID_SEVERITIES:
            errs.append(f"{prefix}: severity invalid: {iss.get('severity')}")
        if not iss.get("excerpt"):
            errs.append(f"{prefix}: excerpt empty")
        if not iss.get("why_it_hurts"):
            errs.append(f"{prefix}: why_it_hurts empty")
        reps = iss.get("replacements")
        if not isinstance(reps, list):
            errs.append(f"{prefix}: replacements missing or not list")
        elif not (2 <= len(reps) <= 3):
            errs.append(f"{prefix}: replacements must be 2 or 3 options (got {len(reps)})")
        elif any(not r or not isinstance(r, str) for r in reps):
            errs.append(f"{prefix}: replacements contain empty/non-string entries")

    if not isinstance(out.get("quick_wins"), list):
        errs.append("quick_wins missing or not list")
    if not isinstance(out.get("terms_to_verify"), list):
        errs.append("terms_to_verify missing or not list")

    return errs


def run(draft_path: Path, rfa_path: Path | None, out_path: Path) -> dict:
    draft = draft_path.read_text(encoding="utf-8")
    rfa = rfa_path.read_text(encoding="utf-8") if rfa_path and rfa_path.exists() else None

    user_prompt = build_user_prompt(draft, rfa)
    t0 = time.time()
    resp = call_seat("editor", [{"role": "user", "content": user_prompt}], system=SYSTEM_PROMPT)
    elapsed = time.time() - t0

    try:
        parsed = extract_json(resp["content"])
    except Exception as e:
        raise RuntimeError(f"Editor output not parseable: {e}\n---\n{resp['content'][:500]}")

    errs = validate(parsed)

    # Assign stable IDs to issues if missing
    for i, iss in enumerate(parsed.get("issues", []), start=1):
        if not iss.get("id"):
            iss["id"] = f"E{i:03d}"

    meta = {
        "seat": "editor",
        "model": resp["model"],
        "family": resp["family"],
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "draft_path": str(draft_path),
        "rfa_file": str(rfa_path) if rfa_path else None,
        "elapsed_seconds": round(elapsed, 2),
        "usage": resp.get("usage"),
        "validation_errors": errs,
        "validation_passed": len(errs) == 0,
    }

    out = {
        "meta": meta,
        "overall_readability": parsed.get("overall_readability", {}),
        "taxonomy_check": parsed.get("taxonomy_check", {}),
        "issues": parsed.get("issues", []),
        "quick_wins": parsed.get("quick_wins", []),
        "terms_to_verify": parsed.get("terms_to_verify", []),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Editor seat — clarity pass.")
    ap.add_argument("--draft", required=True, type=Path)
    ap.add_argument("--rfa", type=Path, default=None)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args(argv)

    out = run(args.draft, args.rfa, args.out)
    n_issues = len(out["issues"])
    n_high = sum(1 for i in out["issues"] if i.get("severity") == "high")
    n_terms = len(out["terms_to_verify"])
    readability = out["overall_readability"].get("score_10", "?")
    print(f"[editor/{out['meta']['family']}/{out['meta']['model']}] "
          f"readability {readability}/10 — {n_issues} issues ({n_high} high) "
          f"— {n_terms} terms flagged for admin-risk review")
    if not out["meta"]["validation_passed"]:
        print("VALIDATION ERRORS:", file=sys.stderr)
        for e in out["meta"]["validation_errors"]:
            print(f"  - {e}", file=sys.stderr)
        return 2
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
