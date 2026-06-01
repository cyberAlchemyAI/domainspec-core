"""CLI for building the Pennsylvania foundation candidate corpus."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline.funder_corpus.pa_foundations import build_pa_foundation_candidates


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tilth-pa-foundations",
        description="Build a PA philanthropic foundation candidate dataset from IRS CSV inputs.",
    )
    parser.add_argument("--bmf-csv", required=True, type=Path)
    parser.add_argument("--teos-index-csv", required=True, action="append", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--json-output", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    result = build_pa_foundation_candidates(
        bmf_csv=args.bmf_csv,
        teos_index_csvs=args.teos_index_csv,
        output_dir=args.output_dir,
    )

    payload = {
        "source_bmf_rows": result.source_bmf_rows,
        "source_index_rows": result.source_index_rows,
        "pa_501c3_rows": result.pa_501c3_rows,
        "candidate_rows": result.candidate_rows,
        "linked_filing_rows": result.linked_filing_rows,
        "output_ndjson": str(result.output_ndjson),
        "output_csv": str(result.output_csv),
        "output_summary": str(result.output_summary),
    }
    if args.json_output:
        print(json.dumps(payload, sort_keys=True))
    else:
        print(f"PA 501(c)(3) rows: {result.pa_501c3_rows}")
        print(f"Foundation candidates: {result.candidate_rows}")
        print(f"Linked latest filings: {result.linked_filing_rows}")
        print(f"NDJSON: {result.output_ndjson}")
        print(f"CSV: {result.output_csv}")
        print(f"Summary: {result.output_summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
