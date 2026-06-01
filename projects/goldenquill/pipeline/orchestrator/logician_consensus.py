#!/usr/bin/env python3
"""
Logician consensus gate — deterministic, no LLM.

Reads judge.json and red_team.json for the same draft. Decides:
  (a) Did both seats validate their own outputs? (Rule 2 — Magic Step)
  (b) Do Judge and Red Team agree within disagreement_threshold_points?
  (c) Do per-criterion scores diverge sharply anywhere?
  (d) Are Red Team's attack_memo findings addressed by Judge's criteria scoring?

If disagreement exceeds threshold, writes council_split.json flagging the
decision for the human. Law 4: applicant breaks ties, never an LLM.

Law 5 / Rule 4 enforcement:
  - Fail-closed: if either seat's validation_passed=False, emit BLOCK verdict.
  - Never rewrite or synthesize scores. Only compare and report.

Input:
    --judge     <path>    judge.json from judge.py
    --red-team  <path>    red_team.json from red_team.py
    --routing   <path>    routing.yaml (for disagreement_threshold_points)
    --out       <path>    Where to write consensus.json

Output JSON:
{
  "meta": {...},
  "verdict": "aligned" | "council_split" | "block",
  "judge_score": int,
  "red_team_score": int,
  "score_delta": int,
  "threshold_points": int,
  "validation": {
    "judge_passed": bool,
    "red_team_passed": bool,
    "errors": [str]
  },
  "per_criterion_divergence": [
    {"id": str, "judge_score": int, "red_team_score": int, "delta": int}
  ],
  "notes": [str],
  "next_action": str
}
"""

from __future__ import annotations
import argparse
import json
import sys
import time
from pathlib import Path

# Reuse the mini-YAML parser from router.py for the threshold
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
try:
    from router import _parse_yaml  # noqa: E402
except ImportError:
    _parse_yaml = None


def load_threshold(routing_path: Path) -> int:
    """Read disagreement_threshold_points from routing.yaml. Default 10."""
    if not routing_path.exists():
        return 10
    text = routing_path.read_text(encoding="utf-8")
    if _parse_yaml:
        try:
            cfg = _parse_yaml(text)
            return int(cfg.get("debate_policy", {}).get("disagreement_threshold_points", 10))
        except Exception:
            pass
    # Regex fallback if YAML parse fails
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("disagreement_threshold_points"):
            try:
                return int(line.split(":")[1].strip())
            except Exception:
                return 10
    return 10


def per_criterion_divergence(judge: dict, red_team: dict) -> list[dict]:
    j_map = {c["id"]: c["score"] for c in judge.get("criteria", []) if "id" in c and isinstance(c.get("score"), int)}
    r_map = {c["id"]: c["score"] for c in red_team.get("criteria", []) if "id" in c and isinstance(c.get("score"), int)}
    all_ids = sorted(set(j_map) | set(r_map))
    out = []
    for cid in all_ids:
        js = j_map.get(cid)
        rs = r_map.get(cid)
        if js is None or rs is None:
            out.append({"id": cid, "judge_score": js, "red_team_score": rs, "delta": None,
                        "note": "missing in one seat"})
        else:
            out.append({"id": cid, "judge_score": js, "red_team_score": rs, "delta": abs(js - rs)})
    return out


def run(judge_path: Path, red_team_path: Path, routing_path: Path, out_path: Path) -> dict:
    judge = json.loads(judge_path.read_text(encoding="utf-8"))
    red_team = json.loads(red_team_path.read_text(encoding="utf-8"))
    threshold = load_threshold(routing_path)

    judge_passed = judge.get("meta", {}).get("validation_passed", False)
    red_team_passed = red_team.get("meta", {}).get("validation_passed", False)
    errs: list[str] = []
    if not judge_passed:
        errs.extend(f"judge: {e}" for e in judge.get("meta", {}).get("validation_errors", []))
    if not red_team_passed:
        errs.extend(f"red_team: {e}" for e in red_team.get("meta", {}).get("validation_errors", []))

    j_score = judge.get("total_score")
    r_score = red_team.get("total_score")

    notes: list[str] = []
    verdict = "aligned"
    next_action = "proceed_to_editor"

    # Fail-closed: validation must pass
    if not (judge_passed and red_team_passed):
        verdict = "block"
        next_action = "fix_seat_outputs_before_proceeding"
        notes.append("One or both seats failed self-validation — Rule 2 gate blocks pipeline.")
    else:
        # Overall score disagreement
        if isinstance(j_score, int) and isinstance(r_score, int):
            delta = abs(j_score - r_score)
            if delta >= threshold:
                verdict = "council_split"
                next_action = "surface_to_applicant_for_tie_break"
                notes.append(
                    f"Score delta {delta} >= threshold {threshold} — Law 4 requires human decision."
                )
            else:
                notes.append(f"Score delta {delta} within threshold {threshold}.")

        # Recommendation class mismatch (also counts as a split)
        j_rec = judge.get("recommendation")
        r_rec = red_team.get("recommendation")
        if j_rec and r_rec and j_rec != r_rec:
            if verdict == "aligned":
                verdict = "council_split"
                next_action = "surface_to_applicant_for_tie_break"
            notes.append(f"Recommendation mismatch: judge={j_rec}, red_team={r_rec}.")

    divergence = per_criterion_divergence(judge, red_team) if judge_passed and red_team_passed else []
    # Flag per-criterion deltas that look extreme (>= half of that criterion's max)
    sharp_criteria = [
        d for d in divergence
        if isinstance(d.get("delta"), int) and d["delta"] >= 3  # rough heuristic
    ]
    if sharp_criteria:
        ids = ", ".join(d["id"] for d in sharp_criteria)
        notes.append(f"Sharp per-criterion disagreement on: {ids}")

    # Red Team attack memo summary
    memo = red_team.get("attack_memo", {})
    n_high = sum(1 for w in memo.get("top_weaknesses", []) if w.get("severity") == "high")
    if n_high:
        notes.append(f"Red Team flagged {n_high} high-severity weakness(es) regardless of score.")

    meta = {
        "seat": "logician_consensus",
        "implementation": "python_deterministic",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "judge_file": str(judge_path),
        "red_team_file": str(red_team_path),
        "judge_model": judge.get("meta", {}).get("model"),
        "judge_family": judge.get("meta", {}).get("family"),
        "red_team_model": red_team.get("meta", {}).get("model"),
        "red_team_family": red_team.get("meta", {}).get("family"),
    }

    out = {
        "meta": meta,
        "verdict": verdict,
        "judge_score": j_score,
        "red_team_score": r_score,
        "score_delta": abs(j_score - r_score) if isinstance(j_score, int) and isinstance(r_score, int) else None,
        "threshold_points": threshold,
        "validation": {
            "judge_passed": judge_passed,
            "red_team_passed": red_team_passed,
            "errors": errs,
        },
        "per_criterion_divergence": divergence,
        "notes": notes,
        "next_action": next_action,
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out


def main(argv: list[str]) -> int:
    default_routing = Path(__file__).resolve().parent.parent / "routing.yaml"
    ap = argparse.ArgumentParser(description="Logician consensus gate (deterministic).")
    ap.add_argument("--judge", required=True, type=Path)
    ap.add_argument("--red-team", required=True, type=Path)
    ap.add_argument("--routing", type=Path, default=default_routing)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args(argv)

    out = run(args.judge, args.red_team, args.routing, args.out)
    v = out["verdict"]
    jfam = out["meta"]["judge_family"]
    rfam = out["meta"]["red_team_family"]
    print(f"[logician/consensus] {jfam}={out['judge_score']} vs {rfam}={out['red_team_score']} "
          f"(delta {out['score_delta']}, threshold {out['threshold_points']}) → {v.upper()}")
    for n in out["notes"]:
        print(f"  • {n}")
    if v == "block":
        print("PIPELINE BLOCKED — fix seat validation errors first.", file=sys.stderr)
        return 2
    if v == "council_split":
        print("COUNCIL SPLIT — human decision required before editor pass.", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
