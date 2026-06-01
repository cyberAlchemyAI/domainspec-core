"""Validate that every charter's `runtime_consumers.scribe` block is a
structured mapping with the 7 fields required at Pass-3 LOCK 2026-05-19.

Required fields per scribe block:
  - voice_change         (string, non-empty)
  - section_ordering     (list of strings)
  - must_do              (list of strings)
  - must_not_do          (list of strings)
  - cross_funder_signal  (string, non-empty)
  - source_authority     (string, non-empty)
  - prose_summary        (string, non-empty — pre-Pass-3 prose preserved verbatim)

Pre-Pass-3 charters carried `scribe: |` as a multi-line prose string. Pass 3
reshapes to the 7-field mapping while preserving the original prose under
`prose_summary:`. This validator enforces the new shape.

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
        "scribe_block_shape_check.py requires PyYAML "
        "(`pip install pyyaml --break-system-packages`).",
        file=sys.stderr,
    )
    raise SystemExit(2)


REQUIRED_FIELDS = (
    "voice_change",
    "section_ordering",
    "must_do",
    "must_not_do",
    "cross_funder_signal",
    "source_authority",
    "prose_summary",
)

# Fields expected to be non-empty strings.
STRING_FIELDS = (
    "voice_change",
    "cross_funder_signal",
    "source_authority",
    "prose_summary",
)

# Fields expected to be lists of strings.
LIST_FIELDS = (
    "section_ordering",
    "must_do",
    "must_not_do",
)

YAML_BLOCK_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)


def extract_yaml_blocks(text: str) -> list[tuple[int, str]]:
    """Return (1-based_start_line, body) tuples for every fenced yaml block."""
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


def check_scribe_block(scribe: object) -> list[str]:
    findings: list[str] = []
    if not isinstance(scribe, dict):
        findings.append(
            f"runtime_consumers.scribe is not a mapping "
            f"(got {type(scribe).__name__}); expected 7-field structured shape "
            f"per Pass-3 LOCK 2026-05-19"
        )
        return findings
    for field in REQUIRED_FIELDS:
        if field not in scribe:
            findings.append(f"runtime_consumers.scribe missing field: {field}")
    for field in STRING_FIELDS:
        value = scribe.get(field)
        if value is None:
            continue  # already reported as missing above
        if not isinstance(value, str):
            findings.append(
                f"runtime_consumers.scribe.{field} is not a string "
                f"(got {type(value).__name__})"
            )
        elif not value.strip():
            findings.append(
                f"runtime_consumers.scribe.{field} is empty string"
            )
    for field in LIST_FIELDS:
        value = scribe.get(field)
        if value is None:
            continue
        if not isinstance(value, list):
            findings.append(
                f"runtime_consumers.scribe.{field} is not a list "
                f"(got {type(value).__name__})"
            )
            continue
        if not value:
            findings.append(
                f"runtime_consumers.scribe.{field} is empty list"
            )
            continue
        for idx, item in enumerate(value):
            if not isinstance(item, str):
                findings.append(
                    f"runtime_consumers.scribe.{field}[{idx}] is not a string "
                    f"(got {type(item).__name__})"
                )
    return findings


CHARTER_FILE_SUFFIX = "_charter_v0_DRAFT.md"


def is_charter_file(path: Path) -> bool:
    """Skip MANIFEST.md / README.md and any non-charter index files.

    Charters in pillar_1_charters/ follow the `*_charter_v0_DRAFT.md`
    naming convention; index / manifest files do not and should not be
    expected to carry runtime_consumers.scribe blocks.
    """
    return path.name.endswith(CHARTER_FILE_SUFFIX)


def check(paths: list[Path]) -> list[tuple[Path, int, str]]:
    findings: list[tuple[Path, int, str]] = []
    for path in paths:
        if not is_charter_file(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            findings.append((path, 0, f"read error: {exc}"))
            continue

        found_scribe_block = False
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
            consumers = doc.get("runtime_consumers")
            if not isinstance(consumers, dict):
                continue
            scribe = consumers.get("scribe")
            if scribe is None:
                continue
            found_scribe_block = True
            for issue in check_scribe_block(scribe):
                findings.append((path, block_line, issue))

        if not found_scribe_block:
            findings.append(
                (path, 0,
                 "no runtime_consumers.scribe block found in any yaml fence")
            )
    return findings


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv[1:]]
    if not paths:
        print(
            "usage: python -m pipeline.funder_intelligence._validators."
            "scribe_block_shape_check <files...>",
            file=sys.stderr,
        )
        return 2
    findings = check(paths)
    for path, lineno, message in findings:
        print(f"{path}:{lineno}: {message}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
