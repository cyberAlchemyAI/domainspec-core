import argparse
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pipeline.nervous_system.scout_adapters.grants_gov_download import GrantsGovOpportunityRecord
from pipeline.nervous_system.scout_adapters.sam_gov_assistance_listings import SamGovAssistanceListingRecord
from pipeline.nervous_system.scout_enrichment.aln_enrichment import join_opportunities_to_assistance_listings
from pipeline.nervous_system.scout_read_models.enriched_opportunity_export import export_enriched_opportunities_read_model

def create_synthetic_opportunity(opp_id: str, title: str, aln: Optional[str]) -> GrantsGovOpportunityRecord:
    opp = GrantsGovOpportunityRecord(
        opportunity_id=f"OPP-{opp_id}",
        applied_as_entity_id="test_entity",
        raw_import_id=f"IMP-{opp_id}",
        title=title,
        funder="Synthetic Agency",
        close_date_utc=None,
        posted_date_utc=None,
        opportunity_number=f"NO-{opp_id}",
        description="Synthetic description",
        eligibility_text=None,
        award_ceiling=None,
        award_floor=None,
        url=None,
    )
    if aln is not None:
        object.__setattr__(opp, "cfda_number", aln)
    return opp

def create_synthetic_listing(listing_id: str, title: str, aln: str) -> SamGovAssistanceListingRecord:
    return SamGovAssistanceListingRecord(
        listing_id=f"ALN-{listing_id}",
        raw_import_id=f"IMP-{listing_id}",
        assistance_listing_number=aln,
        program_title=title,
        agency="Synthetic Agency",
        agency_code="001",
        subagency=None,
        assistance_type=None,
        objectives=None,
        eligible_applicants=None,
        beneficiaries=None,
        use_restrictions=None,
        application_procedures=None,
        award_floor=None,
        award_ceiling=None,
        last_updated_date=None,
        url=None,
    )

def main():
    parser = argparse.ArgumentParser(description="Smoke test for Scout Read-Model Export CLI")
    parser.add_argument("--output-root", required=True, help="Directory to write output artifacts")
    parser.add_argument("--run-id", required=True, help="Run ID for the snapshot")
    parser.add_argument("--generated-at-utc", help="Timestamp of generation")
    parser.add_argument("--source-grants-gov-file", default="synthetic_grants_gov_demo.csv")
    parser.add_argument("--source-sam-gov-file", default="synthetic_sam_gov_demo.csv")
    parser.add_argument("--source-grants-gov-hash", default=hashlib.sha256(b"synthetic_grants_gov_demo").hexdigest())
    parser.add_argument("--source-sam-gov-hash", default=hashlib.sha256(b"synthetic_sam_gov_demo").hexdigest())
    parser.add_argument("--overwrite-snapshot", action="store_true")

    args = parser.parse_args()

    generated_at_utc = args.generated_at_utc or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Create Synthetic Opportunities
    opp_matched = create_synthetic_opportunity("1", "Matched Opp", "10.001")
    opp_missing = create_synthetic_opportunity("2", "Missing ALN Opp", None)
    opp_unmatched = create_synthetic_opportunity("3", "Unmatched Opp", "99.999")
    opp_malformed = create_synthetic_opportunity("4", "Malformed ALN Opp", "abc")
    opp_ambiguous = create_synthetic_opportunity("5", "Ambiguous Opp", "10.002")

    opportunities = [opp_matched, opp_missing, opp_unmatched, opp_malformed, opp_ambiguous]

    # Create Synthetic SAM.gov Listings
    list_matched = create_synthetic_listing("1", "Matched Listing", "10.001")
    list_ambiguous_1 = create_synthetic_listing("2", "Ambiguous Listing 1", "10.002")
    list_ambiguous_2 = create_synthetic_listing("3", "Ambiguous Listing 2", "10.002")

    listings = [list_matched, list_ambiguous_1, list_ambiguous_2]

    # Run ALN Enrichment
    enriched_raw = join_opportunities_to_assistance_listings(
        opportunities=opportunities,
        assistance_listings=listings,
        joined_at_utc=generated_at_utc
    )

    from pipeline.nervous_system.scout_enrichment.capital_efficiency_discovery import discover_capital_efficiency_signals
    from dataclasses import replace

    enriched = []
    for r in enriched_raw:
        signals = discover_capital_efficiency_signals(r.opportunity)
        enriched.append(replace(r, capital_efficiency_signals=signals))

    # Run Read Model Export
    try:
        result = export_enriched_opportunities_read_model(
            enriched_records=enriched,
            output_root=args.output_root,
            run_id=args.run_id,
            generated_at_utc=generated_at_utc,
            source_grants_gov_file=args.source_grants_gov_file,
            source_sam_gov_file=args.source_sam_gov_file,
            source_grants_gov_hash=args.source_grants_gov_hash,
            source_sam_gov_hash=args.source_sam_gov_hash,
            overwrite_snapshot=args.overwrite_snapshot
        )
    except Exception as e:
        print(f"Error during export: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"run_id: {args.run_id}")
    print(f"snapshot_dir: {result.snapshot_dir}")
    print(f"latest_dir: {result.latest_dir}")
    print(f"full_record_count: {result.full_record_count}")
    print(f"index_record_count: {result.index_record_count}")
    print(f"matched_count: {result.matched_count}")
    print(f"missing_aln_count: {result.missing_aln_count}")
    print(f"malformed_aln_count: {result.malformed_aln_count}")
    print(f"unmatched_count: {result.unmatched_count}")
    print(f"ambiguous_count: {result.ambiguous_count}")
    print(f"manifest_path: {result.manifest_path}")

if __name__ == "__main__":
    main()
