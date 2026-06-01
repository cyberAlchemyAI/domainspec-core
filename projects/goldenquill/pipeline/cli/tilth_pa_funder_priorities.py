"""CLI for deriving funder priorities and annual giving from grant rows."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline.funder_corpus.pa_foundations import aggregate_funder_priorities


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tilth-pa-funder-priorities",
        description="Aggregate annual giving and top priorities from extracted grant rows.",
    )
    parser.add_argument("--grants-csv", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--top-n", type=int, default=8)
    parser.add_argument("--json-output", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    result = aggregate_funder_priorities(
        grants_csv=args.grants_csv,
        output_dir=args.output_dir,
        top_n=args.top_n,
    )
    payload = {
        "grant_rows_read": result.grant_rows_read,
        "funder_year_rows": result.funder_year_rows,
        "output_ndjson": str(result.output_ndjson),
        "output_csv": str(result.output_csv),
        "output_summary": str(result.output_summary),
    }
    if args.json_output:
        print(json.dumps(payload, sort_keys=True))
    else:
        print(f"Grant rows read: {result.grant_rows_read}")
        print(f"Funder-year rows: {result.funder_year_rows}")
        print(f"NDJSON: {result.output_ndjson}")
        print(f"CSV: {result.output_csv}")
        print(f"Summary: {result.output_summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
