#!/usr/bin/env python3
"""
Golden Quill / Tilth — Audit Assembler (deterministic)
------------------------------------------------------
Reads per-seat audit output files + `_board_health.json` from an audit run
directory, clusters findings by (section, anchor), ranks by seat count,
and writes `_SYNTHESIS.md`.

No LLM. Pure parse + group + rank. Same input produces the same output.

This module is the "spine" of every audit run. Until it existed, every
synthesis was an LLM-or-human claim; now every run produces a
reproducible artifact. (Finding SYN-1 in the 2026-04-15 meta-review.)

Usage:
    python3 audit_assembler.py <run_dir>
    python3 audit_assembler.py <run_dir> -o /tmp/synth.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

# --------------------------------------------------------------------- config

PILLAR_SECTIONS = ("SEEK", "STABILIZE", "SECURE", "ADVISE")
META_PRODUCT = "PRODUCT-VS-OPERATOR"
META_DESCIMPL = "DESCRIPTION-VS-IMPLEMENTATION"
SECTION_ORDER = (
    META_DESCIMPL,
    META_PRODUCT,
    "SEEK",
    "STABILIZE",
    "SECURE",
    "ADVISE",
)

FIELD_NAMES = [
    # Longer labels first so regex prefers them over shorter prefixes.
    "Where impl would need to live",
    "Where claim lives",
    "Why it matters for the OS",
    "Correct parameterization",
    "Tacit assumption",
    "Where it lives",
    "Why it matters",
    "Operator question",
    "Severity",
    "Claim",
    "Where",
    "What",
    "Why",
    "Fix",
    "Tag",
]
FIELD_RE = re.compile(
    r"^\s*(?:\*\*)?(" + "|".join(re.escape(n) for n in FIELD_NAMES) + r")(?:\*\*)?\s*:\s*(.*)$"
)

SECTION_RE = re.compile(r"^##\s+(.+?)\s*$")
NUMBERED_ITEM_RE = re.compile(r"^\s*\d+\.\s+(.*)$")
BOLD_WRAP_RE = re.compile(r"^\*+\s*(.*?)\s*\*+$")


def _clean_value(v: str) -> str:
    """Strip enclosing **bold**, backticks, smart quotes, trailing colon."""
    v = v.strip()
    # Repeatedly strip matched *bold* wrappers and trailing bold artifacts.
    for _ in range(3):
        m = BOLD_WRAP_RE.match(v)
        if m:
            v = m.group(1).strip()
            continue
        break
    # Strip trailing orphan ** (from patterns like "**Tag:** **GAP**")
    while v.endswith("*"):
        v = v.rstrip("*").rstrip()
    while v.startswith("*"):
        v = v.lstrip("*").lstrip()
    return v.strip()

PATH_RE = re.compile(
    r"[`']?("
    r"[A-Za-z0-9_][A-Za-z0-9_./-]*\.[A-Za-z]{1,6}"  # file.ext
    r"|[A-Za-z0-9_]+/[A-Za-z0-9_./-]+/?"             # dir/sub or path
    r")[`']?"
)

STOPWORDS = frozenset(
    """
the a an and or of to in on at for with by from this that these those is
are was were be been being has have had do does did no not as it its but
if then than so such which who whom what when where why how seat seats
pipeline implementation implemented code file files path paths
""".split()
)

# Fields that are keyed to clusters.
ANCHOR_FIELDS = ("Where", "Where claim lives", "Where it lives")
CLAIM_FIELDS = ("Claim", "Tacit assumption", "What", "_opening")


# --------------------------------------------------------------------- parse

def _normalize_section(header: str) -> str | None:
    h = header.strip().upper().rstrip(":")
    if h.startswith("PRODUCT-VS-OPERATOR"):
        return META_PRODUCT
    if h.startswith("DESCRIPTION-VS-IMPLEMENTATION"):
        return META_DESCIMPL
    if h in PILLAR_SECTIONS:
        return h
    return None


def parse_seat_file(path: Path) -> list[dict]:
    """Parse one seat's markdown output into a list of finding dicts.

    Each finding carries:
        _section : str (DESCRIPTION-VS-IMPLEMENTATION|PRODUCT-VS-OPERATOR|SEEK|...)
        _opening : str (optional — prose between numbered-item start and first field)
        <FieldName> : str (for each recognized field)
    """
    findings: list[dict] = []
    text = path.read_text(encoding="utf-8", errors="replace")

    current_section: str | None = None
    current_finding: dict | None = None
    current_field: str | None = None

    def flush() -> None:
        nonlocal current_finding, current_field
        if current_finding and current_finding.get("_has_content"):
            current_finding.pop("_has_content", None)
            findings.append(current_finding)
        current_finding = None
        current_field = None

    for raw in text.splitlines():
        line = raw.rstrip()

        sec_m = SECTION_RE.match(line)
        if sec_m:
            flush()
            current_section = _normalize_section(sec_m.group(1))
            continue

        if current_section is None:
            continue

        item_m = NUMBERED_ITEM_RE.match(line)
        if item_m:
            flush()
            current_finding = {"_section": current_section, "_has_content": False}
            rest = item_m.group(1).strip()
            fm = FIELD_RE.match(rest)
            if fm:
                current_field = fm.group(1)
                current_finding[current_field] = _clean_value(fm.group(2))
            else:
                current_finding["_opening"] = _clean_value(rest)
                current_field = None
            current_finding["_has_content"] = True
            continue

        if current_finding is None:
            continue

        fm = FIELD_RE.match(line)
        if fm:
            current_field = fm.group(1)
            value = _clean_value(fm.group(2))
            existing = current_finding.get(current_field)
            current_finding[current_field] = (existing + "\n" + value).strip() if existing else value
            current_finding["_has_content"] = True
            continue

        if current_field and line.strip():
            existing = current_finding.get(current_field, "")
            current_finding[current_field] = (existing + " " + line.strip()).strip()

    flush()
    return findings


# --------------------------------------------------------------------- cluster

def normalize_anchor(value: str | None) -> str | None:
    if not value:
        return None
    m = PATH_RE.search(value)
    if not m:
        return None
    anchor = m.group(1)
    anchor = re.sub(r":\d+(?:-\d+)?$", "", anchor)  # strip trailing line refs
    return anchor.lower().rstrip("/")


def _keywords(text: str, n: int = 3) -> tuple[str, ...]:
    if not text:
        return ()
    words = re.findall(r"[A-Za-z]{4,}", text.lower())
    kept = tuple(w for w in words if w not in STOPWORDS)
    return kept[:n]


def cluster_key(finding: dict) -> tuple:
    section = finding.get("_section", "")
    anchor = None
    for f in ANCHOR_FIELDS:
        anchor = normalize_anchor(finding.get(f))
        if anchor:
            break
    if anchor:
        return (section, "anchor", anchor)
    tag = (finding.get("Tag") or "").strip().upper()
    claim_text = next(
        (finding[f] for f in CLAIM_FIELDS if f in finding and finding[f].strip()),
        "",
    )
    return (section, "kw", tag, _keywords(claim_text))


def _severity_rank(members: list[tuple[str, dict]]) -> int:
    order = {"CRITICAL": 0, "HIGH": 1, "MED": 2, "MEDIUM": 2, "LOW": 3}
    best = 4
    for _seat, fin in members:
        s = (fin.get("Severity") or "").strip().upper()
        best = min(best, order.get(s, 4))
    return best


def _section_rank(section: str) -> int:
    try:
        return SECTION_ORDER.index(section)
    except ValueError:
        return 99


# --------------------------------------------------------------------- render

def format_finding(finding: dict, seat: str) -> str:
    lines = [f"- **seat:** `{seat}`"]
    order = (
        "Tag", "Severity",
        "Claim", "Tacit assumption", "Correct parameterization",
        "Where", "Where claim lives", "Where impl would need to live", "Where it lives",
        "What", "Why it matters for the OS", "Why it matters", "Why",
        "Fix", "Operator question",
    )
    emitted = False
    for key in order:
        val = finding.get(key, "")
        if val and val.strip():
            lines.append(f"  - **{key}:** {val.strip()}")
            emitted = True
    if not emitted and finding.get("_opening"):
        lines.append(f"  - {finding['_opening'].strip()}")
    return "\n".join(lines)


def find_seat_files(run_dir: Path) -> dict[str, Path]:
    out: dict[str, Path] = {}
    for p in sorted(run_dir.iterdir()):
        if not p.is_file() or p.suffix != ".md":
            continue
        if p.name.startswith("_"):
            continue
        if p.name.endswith(".QUARANTINE.md"):
            continue
        out[p.stem] = p
    return out


def assemble(run_dir: Path) -> str:
    bh_path = run_dir / "_board_health.json"
    if not bh_path.exists():
        raise FileNotFoundError(f"missing board-health file: {bh_path}")
    bh = json.loads(bh_path.read_text(encoding="utf-8"))

    seat_files = find_seat_files(run_dir)
    if not seat_files:
        raise FileNotFoundError(f"no seat .md files in {run_dir}")

    per_seat = {seat: parse_seat_file(path) for seat, path in seat_files.items()}

    clusters: dict[tuple, list[tuple[str, dict]]] = defaultdict(list)
    for seat, findings in per_seat.items():
        for fin in findings:
            clusters[cluster_key(fin)].append((seat, fin))

    convergence: list[tuple[tuple, list[tuple[str, dict]]]] = []
    singletons: list[tuple[tuple, list[tuple[str, dict]]]] = []
    for key, members in clusters.items():
        unique_seats = {s for s, _ in members}
        (convergence if len(unique_seats) >= 2 else singletons).append((key, members))

    convergence.sort(
        key=lambda kv: (
            -len({s for s, _ in kv[1]}),
            _severity_rank(kv[1]),
            _section_rank(kv[0][0]),
        )
    )
    singletons.sort(key=lambda kv: (_section_rank(kv[0][0]), _severity_rank(kv[1])))

    op_questions: list[tuple[str, str, str]] = []
    sovereignty: list[tuple[str, dict]] = []
    for seat, findings in per_seat.items():
        for fin in findings:
            q = (fin.get("Operator question") or "").strip()
            if q:
                op_questions.append((seat, fin.get("_section", ""), q))
            if (fin.get("Tag") or "").strip().upper() == "SOVEREIGNTY":
                sovereignty.append((seat, fin))

    # ----- build markdown -----
    out: list[str] = []
    out.append("---")
    out.append("title: Project Audit — Synthesis (deterministic assembler)")
    out.append(f"run: {bh.get('audit', run_dir.name)}")
    out.append(
        f"board_status: {bh.get('board_status', 'unknown')} "
        f"({bh.get('seats_healthy', '?/?')}, {bh.get('elapsed_total_s', 0):.0f}s)"
    )
    out.append(f"seats: {', '.join(sorted(per_seat.keys()))}")
    out.append("assembler: pipeline/orchestrator/audit_assembler.py (pure Python, no LLM)")
    out.append("---")
    out.append("")
    out.append("# Project Audit — Synthesis")
    out.append("")

    out.append("## Board health snapshot")
    out.append("")
    for seat in sorted(bh.get("seats", {})):
        s = bh["seats"][seat]
        out.append(
            f"- **{seat}** ({s.get('family')}/{s.get('model')}, "
            f"{s.get('elapsed_s', 0):.1f}s) — status {s.get('status')}, "
            f"{s.get('content_chars', 0)} chars, leaks {s.get('leak_matches', 0)}"
        )
    out.append("")

    out.append(f"## Convergence findings (≥2 seats on same anchor) — {len(convergence)} clusters")
    out.append("")
    if not convergence:
        out.append("_No convergence clusters this run._")
        out.append("")
    for idx, (key, members) in enumerate(convergence, 1):
        seats_in = sorted({s for s, _ in members})
        section = key[0]
        anchor_or_kw = key[2] if key[1] == "anchor" else "shared-keywords"
        out.append(
            f"### C-{idx} — `{section}`  anchor: `{anchor_or_kw}`  "
            f"raised_by: {', '.join(seats_in)} ({len(seats_in)} seats)"
        )
        out.append("")
        for seat, fin in members:
            out.append(format_finding(fin, seat))
            out.append("")

    out.append(f"## Singleton findings (single-seat, verbatim) — {len(singletons)} items")
    out.append("")
    by_section: dict[str, list[tuple[str, dict]]] = defaultdict(list)
    for key, members in singletons:
        by_section[key[0]].append(members[0])
    for sec in SECTION_ORDER:
        if sec not in by_section:
            continue
        out.append(f"### {sec}")
        out.append("")
        for seat, fin in by_section[sec]:
            out.append(format_finding(fin, seat))
            out.append("")

    out.append(f"## Sovereignty findings (each must carry a local alternative) — {len(sovereignty)} items")
    out.append("")
    if not sovereignty:
        out.append("_None flagged this run._")
        out.append("")
    for seat, fin in sovereignty:
        out.append(format_finding(fin, seat))
        out.append("")

    out.append(f"## Operator questions ({len(op_questions)} surfaced)")
    out.append("")
    for seat, sec, q in op_questions:
        out.append(f"- [{sec}] ({seat}) {q}")
    out.append("")

    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Deterministic audit-output assembler")
    ap.add_argument("run_dir", type=Path, help="Audit run directory (has seat .md + _board_health.json)")
    ap.add_argument("-o", "--output", type=Path, default=None, help="Output file (default: <run_dir>/_SYNTHESIS.md)")
    ap.add_argument("--stdout", action="store_true", help="Print synthesis to stdout instead of writing")
    args = ap.parse_args(argv)

    run_dir = args.run_dir.resolve()
    if not run_dir.is_dir():
        print(f"error: {run_dir} is not a directory", file=sys.stderr)
        return 2

    md = assemble(run_dir)
    if args.stdout:
        print(md)
        return 0
    out_path = args.output or (run_dir / "_SYNTHESIS.md")
    out_path.write_text(md, encoding="utf-8")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
