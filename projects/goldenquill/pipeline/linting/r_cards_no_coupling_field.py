"""R-CARDS-NO-COUPLING-FIELD — AST-lint rule for card files.

Per blueprint §4 v2.x card-hardening §4.X.3. Scans every YAML file under
pipeline/cards/CIC/**.yaml and pipeline/cards/CLC/**.yaml for forbidden
top-level field names matching the canonical FORBIDDEN_FIELD_REGISTRY
imported from pipeline.logician.gates.f_cards_coupling_violation_extension.

LIVE at v7.0.11 LOCK — independent of the runtime gate body's
NotImplementedError state. AST-lint runs at build time; the runtime gate
runs at loader time. Belt + suspenders against re-introduction of the
killed common_clc_patterns_observed field (architecture v7.0.11 §6.1
resolved Option A) and equivalents.

Mirrors §4 v2.x.1 row-198 R-ARCHIVIST-NO-CANONICAL-MUTATE pattern
byte-for-byte for the MappingProxyType-wrapped FORBIDDEN constant import
+ glob-based file scan + per-violation finding emission.
"""

from __future__ import annotations

import glob
import os
from dataclasses import dataclass
from typing import Final, Literal, Sequence

import yaml

from pipeline.logician.gates.f_cards_coupling_violation_extension import (
    FORBIDDEN_FIELD_REGISTRY,
)


RULE_ID: Final[str] = "R-CARDS-NO-COUPLING-FIELD"


CARD_SCAN_ROOTS: Final[tuple[tuple[str, str], ...]] = (
    ("pipeline/cards/CIC/**/*.yaml", "CIC"),
    ("pipeline/cards/CLC/**/*.yaml", "CLC"),
    ("pipeline/cards/matrix/**/*.yaml", "MATRIX"),
)


@dataclass(frozen=True, kw_only=True)
class LintFinding:
    rule_id: str
    file_path: str
    card_axis: Literal["CIC", "CLC", "MATRIX"]
    forbidden_field: str
    severity: Literal["FAIL"]
    message: str


def scan_card_file(
    *,
    file_path: str,
    card_axis: Literal["CIC", "CLC", "MATRIX"],
) -> Sequence[LintFinding]:
    """Scan a single card YAML file for forbidden top-level fields.
    Returns a sequence of LintFinding (empty if clean).
    """

    findings: list[LintFinding] = []
    with open(file_path) as f:
        body = yaml.safe_load(f)

    if not isinstance(body, dict):
        return ()

    forbidden_fields = FORBIDDEN_FIELD_REGISTRY.get(card_axis, frozenset())
    for forbidden in forbidden_fields:
        if forbidden in body:
            findings.append(LintFinding(
                rule_id=RULE_ID,
                file_path=file_path,
                card_axis=card_axis,
                forbidden_field=forbidden,
                severity="FAIL",
                message=(
                    f"R-CARDS-NO-COUPLING-FIELD: {file_path} contains forbidden "
                    f"top-level field {forbidden!r} for axis {card_axis}. "
                    f"Per architecture v7.0.11 §6.1 + F-CARDS-COUPLING-VIOLATION-"
                    f"EXTENSION discipline, this field is structurally forbidden "
                    f"in card bodies."
                ),
            ))

    return tuple(findings)


def scan_all_cards(
    *,
    workspace_root: str = ".",
) -> Sequence[LintFinding]:
    """Run R-CARDS-NO-COUPLING-FIELD across every card YAML in
    pipeline/cards/. Returns all findings.

    Exit-code-1 behavior: caller should check `len(findings) > 0` and exit
    non-zero per AST-lint runner convention.
    """

    all_findings: list[LintFinding] = []
    for glob_pattern, axis in CARD_SCAN_ROOTS:
        full_pattern = os.path.join(workspace_root, glob_pattern)
        for file_path in glob.glob(full_pattern, recursive=True):
            all_findings.extend(scan_card_file(
                file_path=file_path, card_axis=axis,
            ))

    return tuple(all_findings)


def main() -> int:
    """CLI entry. Returns exit code (0 if clean, 1 if any findings)."""
    findings = scan_all_cards()
    if not findings:
        print(f"{RULE_ID}: clean — no forbidden coupling fields found.")
        return 0

    for f in findings:
        print(f.message)
    print(f"{RULE_ID}: {len(findings)} violation(s).")
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
