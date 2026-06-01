"""Validate that every gate's (gate_type, severity, fail_action) tuple matches
one of the rows in FID Refinement Methodology Discipline 3a.4.

Allowed tuples:
  hard_eligibility_gate     | P0                       | REJECT_NO_DRAFT | HOLD_DRAFT
  verify_required_gate      | VERIFY_REQUIRED | HIGH    | HOLD_FOR_OPERATOR_REVIEW
  competitive_scoring_signal| LOW | MED | HIGH          | WARN_OPERATOR | SCORE_DOWN
  drafting_warning          | LOW | MED                 | WARN_SCRIBE
  relationship_signal       | LOW | MED                 | WARN_OPERATOR

Returns exit 0 on clean run, exit 1 on any inconsistency.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml  # PyYAML
except ImportError:  # pragma: no cover
    print(
        "gate_taxonomy_consistency.py requires PyYAML "
        "(`pip install pyyaml --break-system-packages`).",
        file=sys.stderr,
    )
    raise SystemExit(2)

ALLOWED: dict[str, tuple[set[str], set[str]]] = {
    "hard_eligibility_gate": (
        {"P0"},
        {"REJECT_NO_DRAFT", "HOLD_DRAFT"},
    ),
    "verify_required_gate": (
        {"VERIFY_REQUIRED", "HIGH"},
        {"HOLD_FOR_OPERATOR_REVIEW"},
    ),
    "competitive_scoring_signal": (
        {"LOW", "MED", "HIGH"},
        {"WARN_OPERATOR", "SCORE_DOWN"},
    ),
    "drafting_warning": (
        {"LOW", "MED"},
        {"WARN_SCRIBE"},
    ),
    "relationship_signal": (
        {"LOW", "MED"},
        {"WARN_OPERATOR"},
    ),
}

GATE_LIST_KEYS = ("eligibility_gates", "logician_gates", "logician_gate_candidates")
YAML_BLOCK_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)


def extract_yaml_blocks(text: str) -> list[tuple[int, str]]:
    blocks: list[tuple[int, str]] = []
    cursor = 0
    line = 1
    for match in YAML_BLOCK_RE.finditer(text):
        body_start = match.start(1)
        line += text.count("\n", cursor, body_start)
        blocks.append((line, match.group(1)))
        cursor = match.end(1)
        line += match.group(1).count("\n")
    return blocks


def check_gate(gate: dict) -> str | None:
    gate_type = gate.get("gate_type")
    severity = gate.get("severity")
    fail_action = gate.get("fail_action") or gate.get("on_fail")
    if gate_type is None or severity is None or fail_action is None:
        # Schema check is separate; here we only check consistency for gates
        # that carry the three relevant fields.
        return None
    if gate_type not in ALLOWED:
        return f"unknown gate_type: {gate_type}"
    allowed_severities, allowed_fail_actions = ALLOWED[gate_type]
    if severity not in allowed_severities:
        return (
            f"severity '{severity}' not in {sorted(allowed_severities)} "
            f"for gate_type '{gate_type}'"
        )
    if fail_action not in allowed_fail_actions:
        return (
            f"fail_action '{fail_action}' not in {sorted(allowed_fail_actions)} "
            f"for gate_type '{gate_type}'"
        )
    return None


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
                findings.append((path, block_line, f"yaml parse error: {exc}"))
                continue
            if not isinstance(doc, dict):
                continue
            for key in GATE_LIST_KEYS:
                gates = doc.get(key)
                if not isinstance(gates, list):
                    continue
                for idx, gate in enumerate(gates):
                    if not isinstance(gate, dict):
                        continue
                    issue = check_gate(gate)
                    if issue:
                        gate_label = (
                            gate.get("gate_id")
                            or gate.get("gate")
                            or f"#{idx}"
                        )
                        findings.append(
                            (path, block_line,
                             f"{key} gate {gate_label}: {issue}")
                        )
    return findings


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv[1:]]
    if not paths:
        print(
            "usage: python -m pipeline.funder_intelligence._validators."
            "gate_taxonomy_consistency <files...>",
            file=sys.stderr,
        )
        return 2
    findings = check(paths)
    for path, lineno, message in findings:
        print(f"{path}:{lineno}: {message}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
