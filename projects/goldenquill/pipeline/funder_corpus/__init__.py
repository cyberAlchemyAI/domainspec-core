"""Funder corpus builders for public grantmaker intelligence datasets."""

from pipeline.funder_corpus.pa_foundations import (
    CandidateBuildResult,
    FunderPriorityResult,
    GrantExtractionResult,
    aggregate_funder_priorities,
    build_pa_foundation_candidates,
    extract_pf_grants_from_zip,
)

__all__ = [
    "CandidateBuildResult",
    "FunderPriorityResult",
    "GrantExtractionResult",
    "aggregate_funder_priorities",
    "build_pa_foundation_candidates",
    "extract_pf_grants_from_zip",
]
