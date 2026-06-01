"""CLI for ranking PA funders by regenerative project fit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline.funder_corpus.pa_foundations import build_regenerative_shortlist


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tilth-pa-regenerative-shortlist",
        description="Rank funder-priority rows for regenerative PA project relevance.",
    )
    parser.add_argument("--priorities-csv", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--max-rows", type=int, default=3000)
    parser.add_argument("--json-output", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = build_regenerative_shortlist(
        priorities_csv=args.priorities_csv,
        output_dir=args.output_dir,
        max_rows=args.max_rows,
    )
    payload = {
        "funder_rows_read": result.funder_rows_read,
        "shortlist_rows": result.shortlist_rows,
        "output_ndjson": str(result.output_ndjson),
        "output_csv": str(result.output_csv),
        "output_summary": str(result.output_summary),
    }
    if args.json_output:
        print(json.dumps(payload, sort_keys=True))
    else:
        print(f"Funder rows read: {result.funder_rows_read}")
        print(f"Shortlist rows: {result.shortlist_rows}")
        print(f"NDJSON: {result.output_ndjson}")
        print(f"CSV: {result.output_csv}")
        print(f"Summary: {result.output_summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
