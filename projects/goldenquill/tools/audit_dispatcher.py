#!/usr/bin/env python3
"""Audit dispatcher — fan out a prompt to N seats, write outputs, emit board-health.

Usage:
    python3 tools/audit_dispatcher.py \\
        --prompt pipeline/validation/FOUR_PILLAR_AUDIT_META_REVIEW.md \\
        --audit meta_review_2026-04-15 \\
        --seats scout editor judge red_team code_review reasoner_review \\
        --bundle pipeline/validation/FOUR_PILLAR_AUDIT_PROMPT.md \\
                 pipeline/validation/FOUR_PILLAR_AUDIT_PIPELINE.md \\
                 pipeline/validation/TOKEN_BUDGET.md

Writes:
    pipeline/validation/<audit>/<seat>.md   — each seat's findings
    pipeline/validation/<audit>/_board_health.json — per-seat status, timing, usage
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / "pipeline/orchestrator"))
sys.path.insert(0, str(_REPO))

from router import call_seat  # noqa: E402
from pipeline.logician.gates.client_term_leak_gate import scan_text, DEFAULT_REGISTER  # noqa: E402


COT_RE = re.compile(r"<think>.*?</think>", re.DOTALL)


def strip_cot(text: str) -> str:
    """Drop reasoning-model chain-of-thought wrappers if they leak into content."""
    return COT_RE.sub("", text).strip()


def bundle_files(paths: list[Path]) -> str:
    parts = ["\n\n## FILES UNDER REVIEW\n"]
    for p in paths:
        parts.append(f"\n===== FILE: {p.name} =====\n")
        parts.append(p.read_text(encoding="utf-8"))
        parts.append(f"\n===== END: {p.name} =====\n")
    return "".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True, help="Path to the audit prompt file")
    ap.add_argument("--audit", required=True, help="Audit run name (output subdir)")
    ap.add_argument("--seats", nargs="+", required=True, help="Seats to dispatch to")
    ap.add_argument("--bundle", nargs="*", default=[],
                    help="Files to append to the prompt as 'FILES UNDER REVIEW'")
    args = ap.parse_args()

    prompt_path = (_REPO / args.prompt).resolve()
    if not prompt_path.exists():
        print(f"[dispatcher] FATAL: prompt not found: {prompt_path}", file=sys.stderr)
        return 2

    prompt = prompt_path.read_text(encoding="utf-8")
    if args.bundle:
        bundle_paths = [(_REPO / b).resolve() for b in args.bundle]
        missing = [p for p in bundle_paths if not p.exists()]
        if missing:
            print(f"[dispatcher] FATAL: bundle files missing: {missing}", file=sys.stderr)
            return 2
        prompt = prompt + bundle_files(bundle_paths)

    # --- PRE-DISPATCH: client-term leak gate (fail-closed) ---------------
    leaks = scan_text(prompt, register_path=DEFAULT_REGISTER)
    if leaks:
        print(f"[dispatcher] BLOCKED: client-term leak gate failed "
              f"({len(leaks)} matches). Dispatch aborted.", file=sys.stderr)
        for f in leaks[:20]:
            print(f"  line {f.line}:{f.column}  term={f.term!r}  …{f.context}…",
                  file=sys.stderr)
        out_dir = _REPO / "pipeline/validation" / args.audit
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "_leak_gate_BLOCKED.json").write_text(
            json.dumps({
                "status": "BLOCKED",
                "count": len(leaks),
                "findings": [f.to_dict() for f in leaks],
            }, indent=2), encoding="utf-8",
        )
        return 2
    print(f"[dispatcher] leak-gate CLEAN on inbound payload "
          f"({len(prompt)} chars, 0 matches)")

    out_dir = _REPO / "pipeline/validation" / args.audit
    out_dir.mkdir(parents=True, exist_ok=True)

    health: dict = {
        "audit": args.audit,
        "prompt": str(prompt_path.relative_to(_REPO)),
        "bundle": args.bundle,
        "started": time.time(),
        "prompt_chars": len(prompt),
        "seats": {},
    }

    overall_t0 = time.time()
    for seat in args.seats:
        print(f"[dispatcher] → {seat} ...", flush=True)
        t0 = time.time()
        try:
            r = call_seat(seat, [{"role": "user", "content": prompt}])
            raw = r["content"] or ""
            content = strip_cot(raw)
            # POST-receive leak-gate on the seat's output.
            seat_leaks = scan_text(content, register_path=DEFAULT_REGISTER)
            if seat_leaks:
                out_name = f"{seat}.QUARANTINE.md"
                banner = (
                    "<!-- QUARANTINED — client-term leak gate matched "
                    f"{len(seat_leaks)} term(s). Operator must review before "
                    "this output is admitted into synthesis. -->\n\n"
                )
                (out_dir / out_name).write_text(banner + content,
                                                encoding="utf-8")
                status = "QUARANTINED"
            else:
                (out_dir / f"{seat}.md").write_text(content, encoding="utf-8")
                status = "OK"
            health["seats"][seat] = {
                "status": status,
                "model": r.get("model"),
                "family": r.get("family"),
                "elapsed_s": round(time.time() - t0, 2),
                "raw_chars": len(raw),
                "content_chars": len(content),
                "cot_stripped_chars": len(raw) - len(content),
                "leak_matches": len(seat_leaks),
                "leak_terms": sorted({f.term for f in seat_leaks}) or None,
                "usage": r.get("usage"),
            }
            tag = status if status == "OK" else f"{status}({len(seat_leaks)})"
            print(f"[dispatcher]   {seat} {tag} {round(time.time()-t0,1)}s "
                  f"{len(content)} chars", flush=True)
        except Exception as e:
            health["seats"][seat] = {
                "status": "FAIL",
                "error": str(e)[:400],
                "elapsed_s": round(time.time() - t0, 2),
            }
            print(f"[dispatcher]   {seat} FAIL: {e}", flush=True)

    health["finished"] = time.time()
    health["elapsed_total_s"] = round(time.time() - overall_t0, 2)
    ok = sum(1 for s in health["seats"].values() if s["status"] == "OK")
    quarantined = sum(1 for s in health["seats"].values() if s["status"] == "QUARANTINED")
    failed = sum(1 for s in health["seats"].values() if s["status"] == "FAIL")
    total = len(health["seats"])
    if ok == total:
        health["board_status"] = "HEALTHY"
    elif failed == 0 and (ok + quarantined) == total:
        health["board_status"] = "QUARANTINED"
    else:
        health["board_status"] = "DEGRADED"
    health["seats_healthy"] = f"{ok}/{total}"
    health["seats_quarantined"] = quarantined
    health["seats_failed"] = failed

    (out_dir / "_board_health.json").write_text(
        json.dumps(health, indent=2), encoding="utf-8"
    )
    print(f"[dispatcher] done → {out_dir} "
          f"[{health['board_status']}, {health['seats_healthy']}, "
          f"{health['elapsed_total_s']}s]")
    return 0 if health["board_status"] == "HEALTHY" else 1


if __name__ == "__main__":
    sys.exit(main())
