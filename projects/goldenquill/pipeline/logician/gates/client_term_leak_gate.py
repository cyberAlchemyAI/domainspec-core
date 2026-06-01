#!/usr/bin/env python3
"""Client-term leak gate — deterministic, fail-closed.

Scans a text payload for any term in the client-term register. If any match
is found and the scope is declared as "product", the gate fails closed: the
dispatcher must not fan out.

This gate exists because Law 3 (Org Isolation) is meaningless if the author
of a product-level prompt can embed client-specific terms by hand and no
check runs before dispatch. The register is the source of truth for the
product-vs-operator boundary.

Usage (CLI):
    python3 -m pipeline.logician.gates.client_term_leak_gate <file> [--register PATH]

Exit codes:
    0 — clean, no leak
    1 — leak detected (findings printed to stdout as JSON)
    2 — configuration error (register missing, file unreadable)

Usage (Python):
    from pipeline.logician.gates.client_term_leak_gate import scan_text, LeakFinding
    findings = scan_text(text, register_path=...)
    if findings: ...  # fail closed
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path


# Config ships with this module — co-located at pipeline/logician/config/.
# __file__ = pipeline/logician/gates/client_term_leak_gate.py
# .parent.parent = pipeline/logician/
DEFAULT_REGISTER = Path(__file__).resolve().parent.parent / "config" / "client_term_register.txt"


@dataclass
class LeakFinding:
    term: str
    line: int
    column: int
    context: str  # 60 chars around the match

    def to_dict(self) -> dict:
        return asdict(self)


def load_register(path: Path = DEFAULT_REGISTER) -> list[str]:
    """Return the list of banned terms (comments/blanks stripped)."""
    if not path.exists():
        raise FileNotFoundError(f"client-term register not found: {path}")
    terms: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        terms.append(s)
    # Sort longest-first so multi-word phrases match before their substrings
    terms.sort(key=len, reverse=True)
    return terms


def _compile_patterns(terms: list[str]) -> list[tuple[str, re.Pattern]]:
    """Whole-word, case-insensitive patterns. Preserves the original term
    for reporting."""
    compiled = []
    for t in terms:
        # Escape regex specials, then bracket with word boundaries. For
        # multi-word terms the boundary still works because \b matches at
        # the outer edge of each word.
        pat = re.compile(rf"\b{re.escape(t)}\b", re.IGNORECASE)
        compiled.append((t, pat))
    return compiled


def scan_text(text: str, register_path: Path = DEFAULT_REGISTER) -> list[LeakFinding]:
    terms = load_register(register_path)
    patterns = _compile_patterns(terms)
    findings: list[LeakFinding] = []

    # Walk by line so we can report line/col without reconstructing offsets.
    for line_idx, line in enumerate(text.splitlines(), start=1):
        for term, pat in patterns:
            for m in pat.finditer(line):
                start = m.start()
                ctx_lo = max(0, start - 30)
                ctx_hi = min(len(line), start + len(m.group(0)) + 30)
                ctx = line[ctx_lo:ctx_hi].strip()
                findings.append(LeakFinding(
                    term=term,
                    line=line_idx,
                    column=start + 1,
                    context=ctx,
                ))
    return findings


def scan_file(path: Path, register_path: Path = DEFAULT_REGISTER) -> list[LeakFinding]:
    text = path.read_text(encoding="utf-8")
    return scan_text(text, register_path=register_path)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="File to scan")
    ap.add_argument("--register", default=str(DEFAULT_REGISTER),
                    help="Path to the client-term register")
    ap.add_argument("--json", action="store_true",
                    help="Emit findings as JSON (default: human lines)")
    args = ap.parse_args()

    path = Path(args.file)
    reg = Path(args.register)
    if not path.exists():
        print(f"[leak-gate] FATAL: file not found: {path}", file=sys.stderr)
        return 2
    if not reg.exists():
        print(f"[leak-gate] FATAL: register not found: {reg}", file=sys.stderr)
        return 2

    findings = scan_file(path, register_path=reg)
    if not findings:
        print(f"[leak-gate] CLEAN: {path} — no client-term leaks (register: "
              f"{len(load_register(reg))} terms)")
        return 0

    if args.json:
        print(json.dumps({
            "status": "LEAK_DETECTED",
            "file": str(path),
            "register": str(reg),
            "count": len(findings),
            "findings": [f.to_dict() for f in findings],
        }, indent=2))
    else:
        print(f"[leak-gate] LEAK_DETECTED: {path}")
        print(f"[leak-gate] {len(findings)} matches against register "
              f"({len(load_register(reg))} terms):")
        for f in findings:
            print(f"  line {f.line}:{f.column}  term={f.term!r}")
            print(f"    …{f.context}…")
    return 1


if __name__ == "__main__":
    sys.exit(main())
