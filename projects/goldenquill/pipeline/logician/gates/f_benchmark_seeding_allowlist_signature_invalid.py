"""F-BENCHMARK-SEEDING-ALLOWLIST-SIGNATURE-INVALID — PRE-load gate (M1 §5.2.3).

RT-09 closure.  The SN-LLC seeding allowlist file is signed; the
loader refuses any unsigned/tampered allowlist fail-closed.

Wraps :func:`pipeline.logician.benchmarks.seeding_allowlist_loader.load_seeding_allowlist`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional

from pipeline.logician.benchmarks.seeding_allowlist_loader import (
    AllowlistError,
    SeedingAllowlist,
    load_seeding_allowlist,
)
from pipeline.logician.gates._protocols import SignatureVerifyCallable


F_BENCHMARK_SEEDING_ALLOWLIST_SIGNATURE_INVALID: Final[str] = (
    "F-BENCHMARK-SEEDING-ALLOWLIST-SIGNATURE-INVALID"
)


@dataclass(frozen=True, kw_only=True)
class AllowlistSignatureResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    allowlist: Optional[SeedingAllowlist] = None


def check_benchmark_seeding_allowlist_signature_invalid(
    *,
    raw_bytes: bytes,
    operator_public_key: bytes,
    expected_key_id: str,
    signature_verify: SignatureVerifyCallable,
) -> AllowlistSignatureResult:
    """PRE-load gate: verify SN-LLC seeding allowlist signature."""
    try:
        allowlist = load_seeding_allowlist(
            raw_bytes=raw_bytes,
            operator_public_key=operator_public_key,
            expected_key_id=expected_key_id,
            signature_verify=signature_verify,
        )
    except AllowlistError as exc:
        return AllowlistSignatureResult(
            success=False,
            failure_code=F_BENCHMARK_SEEDING_ALLOWLIST_SIGNATURE_INVALID,
            detail=str(exc),
        )
    return AllowlistSignatureResult(
        success=True,
        failure_code=None,
        detail=(
            f"SN-LLC seeding allowlist signature verified under key "
            f"{expected_key_id!r}; {len(allowlist.allowed_source_domains)} "
            f"domain(s), {len(allowlist.allowed_source_path_prefixes)} "
            "path-prefix(es)"
        ),
        allowlist=allowlist,
    )


__all__ = [
    "F_BENCHMARK_SEEDING_ALLOWLIST_SIGNATURE_INVALID",
    "AllowlistSignatureResult",
    "check_benchmark_seeding_allowlist_signature_invalid",
]
