#!/usr/bin/env python3
"""Regenerate the ``ALLOWED_HTTP_LIBS`` constant in
``pipeline/linting/r_no_direct_provider_http.py``.

Companion script for §4 v2.x.5 amendment (LOCKED 2026-05-16) — Cycle 2
§12.8 RT-C2-06 fold-in.

Reads ``sys.stdlib_module_names`` filtered for HTTP-class library names
(regex: ``^(urllib|http|httpx|requests|aiohttp|urllib3|httpcore)``) and
prints what the regenerated frozenset would contain. If the regenerated set
diverges from the hard-coded constant in
``pipeline/linting/r_no_direct_provider_http.py``, the script emits a
build-time warning to stderr and exits with status 1.

The hard-coded constant remains the canonical source; this script is a
drift-detector, NOT a runtime patch. Operator runs it as part of major-
version stdlib upgrades (Python 3.x → 3.y) and manually updates the
constant accordingly.

Usage::

    python3 scripts/regenerate_allowed_http_libs.py
    python3 scripts/regenerate_allowed_http_libs.py --check  # exit 1 on drift
    python3 scripts/regenerate_allowed_http_libs.py --emit   # print frozenset
"""

from __future__ import annotations

import argparse
import re
import sys

# Pattern from §4 v2.x.5 §12.8 RT-C2-06 fold-in.
_HTTP_CLASS_PATTERN = re.compile(
    r"^(urllib|http|httpx|requests|aiohttp|urllib3|httpcore)"
)


def discover_http_class_stdlib_modules() -> frozenset[str]:
    """Return the subset of ``sys.stdlib_module_names`` matching the pattern."""
    return frozenset(
        name
        for name in sys.stdlib_module_names
        if _HTTP_CLASS_PATTERN.match(name)
    )


def hard_coded_allowed_libs() -> frozenset[str]:
    """Read the hard-coded ALLOWED_HTTP_LIBS constant from the rule module."""
    try:
        from pipeline.linting.r_no_direct_provider_http import ALLOWED_HTTP_LIBS
    except ImportError as exc:
        print(
            f"ERROR: failed to import ALLOWED_HTTP_LIBS: {exc}", file=sys.stderr,
        )
        sys.exit(2)
    return ALLOWED_HTTP_LIBS


def format_frozenset(items: frozenset[str]) -> str:
    """Pretty-print a frozenset for the constant declaration."""
    lines = ["frozenset({"]
    for name in sorted(items):
        lines.append(f'    "{name}",')
    lines.append("})")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if regenerated set diverges from hard-coded constant.",
    )
    parser.add_argument(
        "--emit",
        action="store_true",
        help="Print the regenerated frozenset declaration.",
    )
    args = parser.parse_args()

    regenerated = discover_http_class_stdlib_modules()
    # Filter to stdlib-only — third-party libs (httpx, requests, aiohttp,
    # urllib3, httpcore) are matched by the pattern but NOT in
    # sys.stdlib_module_names; they're discovered via the regex pattern but
    # then dropped here.
    stdlib_only = frozenset(
        name for name in regenerated if name in sys.stdlib_module_names
    )

    if args.emit:
        print("ALLOWED_HTTP_LIBS: Final[frozenset[str]] = ", end="")
        print(format_frozenset(stdlib_only))
        return 0

    hard_coded = hard_coded_allowed_libs()

    extra_in_stdlib = stdlib_only - hard_coded
    missing_from_stdlib = hard_coded - stdlib_only

    print(
        f"Python {sys.version_info.major}.{sys.version_info.minor}: "
        f"{len(stdlib_only)} HTTP-class stdlib modules discovered"
    )
    print(f"Hard-coded ALLOWED_HTTP_LIBS: {sorted(hard_coded)}")
    print(f"Stdlib-discovered:            {sorted(stdlib_only)}")

    drift = bool(extra_in_stdlib or missing_from_stdlib)
    if drift:
        if extra_in_stdlib:
            print(
                "WARNING: stdlib has new HTTP-class modules not in "
                f"ALLOWED_HTTP_LIBS: {sorted(extra_in_stdlib)}",
                file=sys.stderr,
            )
        if missing_from_stdlib:
            print(
                "WARNING: ALLOWED_HTTP_LIBS references modules not in stdlib "
                f"(may be third-party): {sorted(missing_from_stdlib)}",
                file=sys.stderr,
            )
        print(
            "Operator action: review divergence, decide whether to extend "
            "ALLOWED_HTTP_LIBS, and re-LOCK §4 v2.x.5+ amendment.",
            file=sys.stderr,
        )
        if args.check:
            return 1
    else:
        print("No drift detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
