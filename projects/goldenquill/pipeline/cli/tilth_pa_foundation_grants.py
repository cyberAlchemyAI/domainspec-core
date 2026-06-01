"""CLI for extracting 990-PF grant rows from an IRS TEOS XML zip."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline.funder_corpus.pa_foundations import extract_pf_grants_from_zip


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tilth-pa-foundation-grants",
        description="Extract 990-PF grants from one IRS TEOS XML archive using the PA candidate CSV.",
    )
    parser.add_argument("--candidates-csv", required=True, type=Path)
    parser.add_argument("--teos-zip", required=True, type=Path)
    parser.add_argument("--xml-batch-id", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--limit-filings", type=int)
    parser.add_argument("--json-output", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    result = extract_pf_grants_from_zip(
        candidates_csv=args.candidates_csv,
        teos_zip=args.teos_zip,
        xml_batch_id=args.xml_batch_id,
        output_dir=args.output_dir,
        limit_filings=args.limit_filings,
    )
    payload = {
        "candidate_rows_read": result.candidate_rows_read,
        "candidate_filings_selected": result.candidate_filings_selected,
        "xml_files_found": result.xml_files_found,
        "grant_rows": result.grant_rows,
        "output_ndjson": str(result.output_ndjson),
        "output_csv": str(result.output_csv),
        "output_summary": str(result.output_summary),
    }
    if args.json_output:
        print(json.dumps(payload, sort_keys=True))
    else:
        print(f"Candidate filings selected: {result.candidate_filings_selected}")
        print(f"XML files found: {result.xml_files_found}")
        print(f"Grant rows: {result.grant_rows}")
        print(f"NDJSON: {result.output_ndjson}")
        print(f"CSV: {result.output_csv}")
        print(f"Summary: {result.output_summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
