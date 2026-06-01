import argparse
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

from pipeline.nervous_system.scout_adapters.grants_gov_download import parse_grants_gov_file
from pipeline.nervous_system.scout_enrichment.aln_enrichment import join_opportunities_to_assistance_listings
from pipeline.nervous_system.scout_read_models.enriched_opportunity_export import export_enriched_opportunities_read_model

def utc_now_seconds_z() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def main():
    parser = argparse.ArgumentParser(description="Scout Intake CLI")
    parser.add_argument("--source", required=True, choices=["grants_gov"], help="Source system identifier")
    parser.add_argument("--identity-scope", required=True, choices=["public_corpus", "applied_as_entity"], help="Identity scope for parsing")
    parser.add_argument("--input", required=True, help="Path to input source file")
    parser.add_argument("--output-root", required=True, help="Directory to write output artifacts")
    parser.add_argument("--run-id", help="Deterministic run ID (optional)")
    parser.add_argument("--generated-at-utc", help="Timestamp in exact YYYY-MM-DDTHH:MM:SSZ format (optional)")
    parser.add_argument("--applied-as-entity-id", help="Required when identity_scope=applied_as_entity")
    parser.add_argument("--source-hash", help="Verbatim caller-provided hash of source file bytes")

    args = parser.parse_args()

    if args.identity_scope == "applied_as_entity" and not args.applied_as_entity_id:
        print("Error: --applied-as-entity-id is required when identity_scope=applied_as_entity", file=sys.stderr)
        sys.exit(1)

    if args.identity_scope == "public_corpus" and args.applied_as_entity_id:
        print("Error: --applied-as-entity-id is forbidden when identity_scope=public_corpus", file=sys.stderr)
        sys.exit(1)

    generated_at_utc = args.generated_at_utc or utc_now_seconds_z()
    if "." in generated_at_utc or not generated_at_utc.endswith("Z"):
        print("Error: Invalid generated_at_utc format", file=sys.stderr)
        sys.exit(1)

    run_id = args.run_id
    if not run_id:
        run_timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        run_id = f"scout-intake-{args.source}-{run_timestamp}"

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    file_bytes = input_path.read_bytes()
    derived_hash = hashlib.sha256(file_bytes).hexdigest()
    source_hash = args.source_hash if args.source_hash else derived_hash

    try:
        if args.source == "grants_gov":
            parse_result = parse_grants_gov_file(
                file_path=str(input_path),
                applied_as_entity_id=args.applied_as_entity_id,
                identity_scope=args.identity_scope,
                imported_at_utc=generated_at_utc,
            )
            opportunities = parse_result.opportunities
        else:
            print(f"Error: Unsupported source: {args.source}", file=sys.stderr)
            sys.exit(1)

        enriched_records_raw = join_opportunities_to_assistance_listings(
            opportunities=opportunities,
            assistance_listings=[],
            joined_at_utc=generated_at_utc
        )

        from pipeline.nervous_system.scout_enrichment.capital_efficiency_discovery import discover_capital_efficiency_signals
        from dataclasses import replace

        enriched_records = []
        for r in enriched_records_raw:
            signals = discover_capital_efficiency_signals(r.opportunity)
            enriched_records.append(replace(r, capital_efficiency_signals=signals))

        export_enriched_opportunities_read_model(
            enriched_records=enriched_records,
            output_root=args.output_root,
            run_id=run_id,
            generated_at_utc=generated_at_utc,
            source_grants_gov_file=input_path.name,
            source_sam_gov_file="None",
            source_grants_gov_hash=source_hash,
            source_sam_gov_hash="None"
        )
        print("Intake complete.", file=sys.stdout)
    except Exception as e:
        print(f"Error during intake: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
