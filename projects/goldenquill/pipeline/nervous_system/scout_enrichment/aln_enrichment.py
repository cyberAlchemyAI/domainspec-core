import re
from dataclasses import dataclass
from typing import Optional, Sequence

from pipeline.nervous_system.scout_models.capital_efficiency_signals import CapitalEfficiencySignal

@dataclass(frozen=True, kw_only=True)
class EnrichedOpportunityRecord:
    opportunity: object
    assistance_listing: Optional[object]
    assistance_listing_number_normalized: Optional[str]
    enrichment_status: str
    enrichment_reason: str
    enrichment_version: str
    joined_at_utc: Optional[str] = None
    capital_efficiency_signals: tuple[CapitalEfficiencySignal, ...] = ()


def normalize_aln(raw: object) -> Optional[str]:
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None

    # Strip all whitespace
    s = re.sub(r"\s+", "", s)

    # Reject if it contains non-numeric characters other than a single dot
    if not re.match(r"^[0-9\.]+$", s):
        return None

    # Count dots
    dots = s.count(".")
    if dots > 1:
        return None
    elif dots == 1:
        parts = s.split(".")
        if len(parts[0]) != 2:
            return None

        # Determine behavior for suffix: pad with 0s up to 3 digits if short?
        # Specification says: "10.1" -> "10.001" if this is the chosen rule, or whatever is deterministic.
        # "10001" -> "10.001".
        # Let's standardize: right-pad the fractional part to 3 digits? Wait, "10.1" -> "10.100" or "10.001"?
        # Usually Assistance Listings are 2 digits dot 3 digits. e.g. 10.001.
        # If someone writes "10.1", do they mean 10.100 or 10.001?
        # Let's reject short/ambiguous unless it's strictly deterministic.
        # Actually, "10.1" is often 10.100, but some might think 10.001.
        # But user said: "- Accept short suffixes only if deterministic: "10.1" -> "10.001" if this is the chosen rule."
        # Let's right-pad with zeros for the suffix? No, usually ALNs are like 10.001, so if they give 10.1, maybe they mean 10.100? No, usually 10.001.
        # Let's just strictly require the right side to be up to 3 digits, and if it's less than 3, we zero-pad on the LEFT of the fractional part? Wait, "10.1" -> "10.001" is zero-padding on the left of the fraction.
        # Let's use: zero-pad fractional part to 3 digits on the LEFT: `parts[1].zfill(3)`
        left = parts[0]
        right = parts[1].zfill(3)
        if len(right) > 3:
            return None
        return f"{left}.{right}"
    else:
        # No dots
        if len(s) == 5:
            # "10001" -> "10.001"
            return f"{s[:2]}.{s[2:]}"
        elif len(s) == 6:
            # "010001" -> "01.001" if we decide that. Wait, ALN is 2 digits dot 3 digits.
            return f"{s[:2]}.{s[2:5]}" if len(s) == 5 else None  # Reject 6 digits to avoid ambiguity
        else:
            return None


def extract_opportunity_aln(opportunity: object) -> Optional[str]:
    # Try direct attributes
    for attr in [
        "assistance_listing_number",
        "assistance_listing",
        "cfda_number",
        "cfda",
        "funding_activity_category_aln",
    ]:
        val = getattr(opportunity, attr, None)
        if val is not None:
            return str(val)

    # Try raw_data if it exists (e.g. dict)
    raw_data = getattr(opportunity, "raw_data", None)
    if isinstance(raw_data, dict):
        aliases = {"cfda", "cfda_number", "assistance_listing", "assistance_listing_number", "cfda number"}
        for k, v in raw_data.items():
            if str(k).strip().lower() in aliases:
                if v is not None:
                    return str(v)

    # Try raw_import.raw_data or similar? The prompt mentions:
    # "opportunity.raw_import/raw row if present by convention"
    # D3 opportunity doesn't have raw_data, but it has raw_import_id. We can't access the row from just the ID without the parser result.
    # So we just return None if not found.
    return None


def build_assistance_listing_index(listings: Sequence[object]) -> dict[str, list[object]]:
    index = {}
    for listing in listings:
        # Get ALN
        raw_aln = getattr(listing, "assistance_listing_number", None)
        if not raw_aln:
            raw_aln = getattr(listing, "source_record_id", None)

        norm = normalize_aln(raw_aln)
        if norm:
            if norm not in index:
                index[norm] = []
            index[norm].append(listing)
    return index


def join_opportunities_to_assistance_listings(
    opportunities: Sequence[object],
    assistance_listings: Sequence[object],
    *,
    joined_at_utc: Optional[str] = None,
    enrichment_version: str = "aln_enrichment_v1"
) -> tuple[EnrichedOpportunityRecord, ...]:

    index = build_assistance_listing_index(assistance_listings)
    enriched = []

    for opp in opportunities:
        raw_aln = extract_opportunity_aln(opp)

        if not raw_aln or not raw_aln.strip():
            enriched.append(
                EnrichedOpportunityRecord(
                    opportunity=opp,
                    assistance_listing=None,
                    assistance_listing_number_normalized=None,
                    enrichment_status="missing_aln",
                    enrichment_reason="No ALN found on opportunity",
                    enrichment_version=enrichment_version,
                    joined_at_utc=joined_at_utc
                )
            )
            continue

        norm_aln = normalize_aln(raw_aln)
        if not norm_aln:
            enriched.append(
                EnrichedOpportunityRecord(
                    opportunity=opp,
                    assistance_listing=None,
                    assistance_listing_number_normalized=None,
                    enrichment_status="malformed_aln",
                    enrichment_reason=f"ALN '{raw_aln}' could not be normalized",
                    enrichment_version=enrichment_version,
                    joined_at_utc=joined_at_utc
                )
            )
            continue

        matches = index.get(norm_aln, [])
        if not matches:
            enriched.append(
                EnrichedOpportunityRecord(
                    opportunity=opp,
                    assistance_listing=None,
                    assistance_listing_number_normalized=norm_aln,
                    enrichment_status="unmatched",
                    enrichment_reason=f"Normalized ALN '{norm_aln}' not found in reference index",
                    enrichment_version=enrichment_version,
                    joined_at_utc=joined_at_utc
                )
            )
        elif len(matches) == 1:
            enriched.append(
                EnrichedOpportunityRecord(
                    opportunity=opp,
                    assistance_listing=matches[0],
                    assistance_listing_number_normalized=norm_aln,
                    enrichment_status="matched",
                    enrichment_reason="Successfully matched to single reference record",
                    enrichment_version=enrichment_version,
                    joined_at_utc=joined_at_utc
                )
            )
        else:
            enriched.append(
                EnrichedOpportunityRecord(
                    opportunity=opp,
                    assistance_listing=None,
                    assistance_listing_number_normalized=norm_aln,
                    enrichment_status="ambiguous",
                    enrichment_reason=f"Normalized ALN '{norm_aln}' matches {len(matches)} reference records",
                    enrichment_version=enrichment_version,
                    joined_at_utc=joined_at_utc
                )
            )

    return tuple(enriched)
