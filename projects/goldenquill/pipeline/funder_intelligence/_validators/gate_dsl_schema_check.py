"""Validate that every gate in `pillar_1_charters/*.md` carries the typed-DSL
fields required by FID Refinement Methodology Discipline 3a.

Required fields per gate:
  - gate_id (or `gate:` legacy synonym in funder-level charters)
  - gate_type   (added at Pass 1 LOCK 2026-05-18)
  - severity
  - fail_action (or `on_fail:` legacy synonym in eligibility_gates blocks)
  - source_required
  - corpus_ref  (or top-level `source_backing.corpus_refs:` reference)
  - confidence  (added at Pass 1 LOCK 2026-05-18)

Pass 1 introduces `gate_type` + `confidence` on every gate without changing
existing severity / fail_action / predicate semantics.

Pass 1 does NOT enforce field-/operator-/value-presence (those require
predicate decomposition; deferred).

Returns exit 0 on clean run, exit 1 on any finding.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml  # PyYAML
except ImportError:  # pragma: no cover
    print(
        "gate_dsl_schema_check.py requires PyYAML "
        "(`pip install pyyaml --break-system-packages`).",
        file=sys.stderr,
    )
    raise SystemExit(2)


REQUIRED_FIELDS = (
    ("gate_id", "gate"),          # accept either spelling
    ("gate_type",),
    ("severity",),
    ("fail_action", "on_fail"),
    ("source_required",),
    ("confidence",),
)

# Top-level YAML keys that hold lists of gates inside a charter.
GATE_LIST_KEYS = ("eligibility_gates", "logician_gates", "logician_gate_candidates")

YAML_BLOCK_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)


def extract_yaml_blocks(text: str) -> list[tuple[int, str]]:
    """Return (1-based_start_line, body) tuples for every fenced yaml block."""
    blocks: list[tuple[int, str]] = []
    cursor = 0
    line = 1
    for match in YAML_BLOCK_RE.finditer(text):
        # Count newlines from cursor up to the body start.
        body_start = match.start(1)
        line += text.count("\n", cursor, body_start)
        blocks.append((line, match.group(1)))
        cursor = match.end(1)
        # Account for the line offset of the body itself.
        line += match.group(1).count("\n")
    return blocks


def gate_has(field_aliases: tuple[str, ...], gate: dict) -> bool:
    return any(alias in gate for alias in field_aliases)


def check_gate(gate: dict) -> list[str]:
    missing: list[str] = []
    for aliases in REQUIRED_FIELDS:
        if not gate_has(aliases, gate):
            missing.append("/".join(aliases))
    return missing


def check(paths: list[Path]) -> list[tuple[Path, int, str]]:
    findings: list[tuple[Path, int, str]] = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            findings.append((path, 0, f"read error: {exc}"))
            continue

        for block_line, body in extract_yaml_blocks(text):
            try:
                doc = yaml.safe_load(body)
            except yaml.YAMLError as exc:
                findings.append(
                    (path, block_line, f"yaml parse error: {exc}")
                )
                continue
            if not isinstance(doc, dict):
                continue
            for key in GATE_LIST_KEYS:
                gates = doc.get(key)
                if not isinstance(gates, list):
                    continue
                for idx, gate in enumerate(gates):
                    if not isinstance(gate, dict):
                        findings.append(
                            (path, block_line,
                             f"{key}[{idx}] is not a mapping")
                        )
                        continue
                    missing = check_gate(gate)
                    if missing:
                        gate_label = gate.get("gate_id") or gate.get("gate") or f"#{idx}"
                        findings.append(
                            (path, block_line,
                             f"{key} gate {gate_label}: missing fields "
                             f"{', '.join(missing)}")
                        )
    return findings


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv[1:]]
    if not paths:
        print(
            "usage: python -m pipeline.funder_intelligence._validators."
            "gate_dsl_schema_check <files...>",
            file=sys.stderr,
        )
        return 2
    findings = check(paths)
    for path, lineno, message in findings:
        print(f"{path}:{lineno}: {message}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
