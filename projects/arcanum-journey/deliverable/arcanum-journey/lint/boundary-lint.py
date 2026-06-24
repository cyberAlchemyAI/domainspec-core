#!/usr/bin/env python3
"""Public-boundary lint for the Arcanum Journey deliverable (S-006 / SWU-AJ-BOUNDARY-1).

Enforces DEC-AJ-HOME-001: the deliverable ships into the PUBLIC arcanum submodule,
so it must contain NO private operator data. This lint fails (exit 1) if the package
references private paths or anything that looks like a real person name in a persona.

Run: python3 boundary-lint.py [package_dir]   (default: parent of this script's dir)
"""
import os
import re
import sys

# Paths that are private in this repo and must never be referenced by the package.
PRIVATE_PATH_MARKERS = [
    "cyberAlchemy-v2",
    "implementation/domainspec",
    "validation/poker-team",
    "projects/arcanum-journey/.craft",   # planning ledger stays private
    "/development/invoke-runs/",
]

# A persona ref must be the anonymized handle, never a "Last, First" name pattern.
PERSON_NAME_RE = re.compile(r"\b[A-Z][a-z]+,\s+[A-Z][a-z]+\b")

# Files we scan (text only).
TEXT_EXT = {".md", ".json", ".yaml", ".yml", ".html", ".py", ".txt"}


def scan(package_dir):
    findings = []
    for root, _dirs, files in os.walk(package_dir):
        for fn in files:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in TEXT_EXT:
                continue
            path = os.path.join(root, fn)
            if os.path.abspath(path) == os.path.abspath(__file__):
                continue  # don't flag this lint's own marker list
            try:
                with open(path, encoding="utf-8") as fh:
                    text = fh.read()
            except (UnicodeDecodeError, OSError):
                continue
            for marker in PRIVATE_PATH_MARKERS:
                if marker in text:
                    findings.append((path, f"private path marker: {marker}"))
            for m in PERSON_NAME_RE.finditer(text):
                findings.append((path, f"possible real person name: '{m.group(0)}'"))
    return findings


def main():
    pkg = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    findings = scan(pkg)
    if findings:
        print(f"BOUNDARY LINT: FAIL ({len(findings)} issue(s)) in {pkg}")
        for path, why in findings:
            print(f"  - {path}: {why}")
        return 1
    print(f"BOUNDARY LINT: PASS — no private data found in {pkg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
