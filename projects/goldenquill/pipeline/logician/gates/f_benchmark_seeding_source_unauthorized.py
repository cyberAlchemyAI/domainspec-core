"""F-BENCHMARK-SEEDING-SOURCE-UNAUTHORIZED — benchmark PRE-write gate (M1 §5.4).

DC-CF-04 leg 3 — refuses any benchmark seed whose ``source_doc`` is
not on the SN-LLC-curated allowlist.  Wraps
:func:`pipeline.logician.benchmarks.seeding_allowlist_loader.source_doc_authorized`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional

from pipeline.logician.benchmarks.seeding_allowlist_loader import (
    SeedingAllowlist,
    source_doc_authorized,
)


F_BENCHMARK_SEEDING_SOURCE_UNAUTHORIZED: Final[str] = (
    "F-BENCHMARK-SEEDING-SOURCE-UNAUTHORIZED"
)


@dataclass(frozen=True, kw_only=True)
class SeedingSourceUnauthorizedResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    benchmark_id: Optional[str] = None
    source_doc: Optional[str] = None


def check_benchmark_seeding_source_unauthorized(
    *,
    benchmark_id: str,
    source_doc: str,
    allowlist: SeedingAllowlist,
) -> SeedingSourceUnauthorizedResult:
    """PRE-write gate: source_doc must match the SN-LLC seeding allowlist."""
    authorized, reason = source_doc_authorized(
        source_doc=source_doc, allowlist=allowlist
    )
    if authorized:
        return SeedingSourceUnauthorizedResult(
            success=True,
            failure_code=None,
            detail=f"benchmark_id={benchmark_id!r}: {reason}",
            benchmark_id=benchmark_id,
            source_doc=source_doc,
        )
    return SeedingSourceUnauthorizedResult(
        success=False,
        failure_code=F_BENCHMARK_SEEDING_SOURCE_UNAUTHORIZED,
        detail=(
            f"benchmark_id={benchmark_id!r} source_doc rejected: {reason}"
        ),
        benchmark_id=benchmark_id,
        source_doc=source_doc,
    )


__all__ = [
    "F_BENCHMARK_SEEDING_SOURCE_UNAUTHORIZED",
    "SeedingSourceUnauthorizedResult",
    "check_benchmark_seeding_source_unauthorized",
]
