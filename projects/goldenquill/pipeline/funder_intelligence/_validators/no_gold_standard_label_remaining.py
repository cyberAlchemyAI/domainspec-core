"""Catch any surviving `gold[- ]standard(s?)` / `gold_standard` rhetoric in
charter prose and YAML.

Pass-0 pattern G3. Promoted to CI check at Pass 1 LOCK 2026-05-18.

Excluded paths: MANIFEST.md (Pass 1 normalizes its rows; the validator runs
*after* the normalization lands), README.md, audit-trail comments inside
charters that retain the historical label for traceability.

Returns exit 0 on clean run, exit 1 on any finding.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Matches any of: gold-standard, gold standard, GOLD-STANDARD, gold-standards,
# gold_standard, GOLD_STANDARD, GOLD-STANDARDS.
PATTERN = re.compile(
    r"""gold[-_ ]standards?""",
    re.IGNORECASE,
)

# Skip lines that are obviously audit-trail comments preserving historical
# labels (Pass 0 retained these for traceability) OR lines that explicitly
# document the *retirement* of the gold-standard label as part of the
# Discipline-8 lifecycle narrative.
AUDIT_TRAIL_MARKERS = (
    "[FIDELITY-FIX-",
    "[FID-RE-AUTHOR]",
    "historical_tracks",
    "retired_commodity_track_model",
    # Retirement-narrative markers — a line that uses any of these alongside
    # `gold-standard` is documenting the retirement, not committing the
    # offense.
    "depth_charter_v0",
    "pre_corpus_hypothesis",
    "honest-lifecycle-labels",
    "honest lifecycle labels",
    "rhetoric demotion",
    "rhetoric was retired",
    "lifecycle flips to",
    "gold_standard_candidate",  # canonical post-source label (Discipline 8)
)


def is_audit_trail(line: str) -> bool:
    return any(marker in line for marker in AUDIT_TRAIL_MARKERS)


def check(paths: list[Path]) -> list[tuple[Path, int, str]]:
    findings: list[tuple[Path, int, str]] = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            findings.append((path, 0, f"read error: {exc}"))
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            if PATTERN.search(line) and not is_audit_trail(line):
                findings.append(
                    (path, lineno, f"gold-standard token: {line.strip()}")
                )
    return findings


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv[1:]]
    if not paths:
        print(
            "usage: python -m pipeline.funder_intelligence._validators."
            "no_gold_standard_label_remaining <files...>",
            file=sys.stderr,
        )
        return 2
    findings = check(paths)
    for path, lineno, message in findings:
        print(f"{path}:{lineno}: {message}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
