"""Catch YAML placeholders like `key: <NEEDED — Pillar 2: ...>` whose embedded
`: ` breaks `yaml.safe_load`.

Pass-0 pattern G1. Promoted to permanent CI check at Pass 1 LOCK 2026-05-18.

Returns exit 0 on clean run, exit 1 on any finding. Prints `path:line: <finding>`.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Match: optional indent + key + colon + space + angle-bracket placeholder
# whose interior contains another `:` (after a space, mimicking YAML's
# mapping-value parse rule) and which is NOT already quoted.
PATTERN = re.compile(
    r"""^\s*[a-z_][a-z0-9_]*:\s+<[^>"]*:[^>"]*>\s*$""",
    re.MULTILINE,
)


def check(paths: list[Path]) -> list[tuple[Path, int, str]]:
    findings: list[tuple[Path, int, str]] = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            findings.append((path, 0, f"read error: {exc}"))
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            if PATTERN.match(line):
                findings.append(
                    (path, lineno, f"unquoted-colon placeholder: {line.strip()}")
                )
    return findings


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv[1:]]
    if not paths:
        print(
            "usage: python -m pipeline.funder_intelligence._validators."
            "no_unquoted_colon_placeholders <files...>",
            file=sys.stderr,
        )
        return 2
    findings = check(paths)
    for path, lineno, message in findings:
        print(f"{path}:{lineno}: {message}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
