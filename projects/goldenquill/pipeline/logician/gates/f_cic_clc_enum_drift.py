"""F-CIC-CLC-ENUM-DRIFT — canonical enum integrity check.

PRE-gate at order 6.45. Fires earliest of the four CIC × CLC gates because
every other identity/capital invariant assumes the canonical enum is intact.
Fail-closed at startup AND on every reload of
``pipeline/types/identity_capital.py``.

Authority: ``pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md``
§4.0 (LOCKED 2026-05-08, Cycle-1 RT-01 fix).

Two checks
----------
1. **Hash check.** SHA3-512 of the canonical-enum module file matches an
   operator-signed reference hash held in
   ``vault_shared/canonical_enum_hashes.yaml``. Reference hash is signed
   Ed25519 + ML-DSA-65 hybrid per A12 crypto-agility envelope.
2. **Count check.** ``len(CustomerIdentityCategory.__args__)`` == 6 AND
   ``len(CapitalLogicCard.__args__)`` == 8. Counts are also cross-validated
   against the canonical-count constants declared in the v7.0.8 amendment
   text (parser pulls them from ``architecture_v7_0_8_amendment.md`` §1).

Subcodes
--------
- ``F-CIC-CLC-ENUM-DRIFT.hash_mismatch``  — file hash differs from signed reference
- ``F-CIC-CLC-ENUM-DRIFT.signature_invalid`` — reference hash signature failed verification
- ``F-CIC-CLC-ENUM-DRIFT.count_cic`` — CIC arg count != 6
- ``F-CIC-CLC-ENUM-DRIFT.count_clc`` — CLC arg count != 8
- ``F-CIC-CLC-ENUM-DRIFT.amendment_count_drift`` — amendment text declares a
  count that does not match the in-code constant (defends against in-code
  edits that update both the enum AND the count constant in lock-step
  without amendment authorization)

Recovery: a legitimate enum modification (e.g., adding a 7th CIC after the
"additional pathways" research lands) requires (a) a new architecture
amendment that resolves the §1 closed-set discipline, (b) operator re-signing
of ``vault_shared/canonical_enum_hashes.yaml`` against the new module, (c)
Cycle-2 verification of the new amendment. Until all three complete, enum
drift is fail-closed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from pipeline.types import (
    CAPITAL_LOGIC_CARD_VALUES,
    CUSTOMER_IDENTITY_CATEGORY_VALUES,
    canonical_cic_count,
    canonical_clc_count,
)


GATE_ID = "F-CIC-CLC-ENUM-DRIFT"
PRE_GATE_ORDER = 6.45


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EnumDriftResult:
    """Result of running F-CIC-CLC-ENUM-DRIFT at startup.

    ``passed=True`` means hash + signature + count + amendment-count all check
    out. ``passed=False`` means at least one subcode fired; Tilth refuses to
    start.
    """

    passed: bool
    subcodes: tuple[str, ...]
    detail: str


# ---------------------------------------------------------------------------
# Injected dependencies
# ---------------------------------------------------------------------------


@runtime_checkable
class EnumModuleBytesReaderCallable(Protocol):
    """Returns raw bytes of ``pipeline/types/identity_capital.py``.

    Gate computes SHA3-512 via the injected hash callable. Raising is the
    fail-closed signal.
    """

    def __call__(self) -> bytes: ...


@runtime_checkable
class CanonicalHashReaderCallable(Protocol):
    """Returns the operator-signed reference-hash record.

    Returned dict must carry:

    - ``identity_capital_module_sha3_512: str`` — hex
    - ``signature_ed25519: bytes``
    - ``signature_ml_dsa_65: bytes``
    - ``signed_payload_bytes: bytes`` — exact bytes both signatures cover
    - ``operator_public_key_ed25519: bytes``
    - ``operator_public_key_ml_dsa_65: bytes``

    Raising is the fail-closed signal.
    """

    def __call__(self) -> dict: ...


@runtime_checkable
class HashBytesCallable(Protocol):
    """Injected SHA3-512 digest function. Returns lowercase hex string."""

    def __call__(self, data: bytes) -> str: ...


@runtime_checkable
class HybridSignatureVerifyCallable(Protocol):
    """Injected hybrid Ed25519 + ML-DSA-65 verifier per A12 crypto-agility.

    Returns ``True`` ONLY when BOTH legs verify. Returns ``False`` if either
    leg fails. Raising is the fail-closed signal.
    """

    def __call__(
        self,
        message_bytes: bytes,
        ed25519_signature: bytes,
        ed25519_public_key: bytes,
        ml_dsa_65_signature: bytes,
        ml_dsa_65_public_key: bytes,
    ) -> bool: ...


@runtime_checkable
class AmendmentCountReaderCallable(Protocol):
    """Returns the canonical (CIC, CLC) counts as declared in the v7.0.8
    amendment text.

    Reader parses ``pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md``
    §1 and extracts the canonical counts. Returns a ``(cic_count, clc_count)``
    tuple. Raising is the fail-closed signal.
    """

    def __call__(self) -> tuple[int, int]: ...


# ---------------------------------------------------------------------------
# Gate implementation
# ---------------------------------------------------------------------------


def run(
    *,
    enum_module_reader: EnumModuleBytesReaderCallable,
    canonical_hash_reader: CanonicalHashReaderCallable,
    hash_bytes: HashBytesCallable,
    verify_hybrid_signature: HybridSignatureVerifyCallable,
    amendment_count_reader: AmendmentCountReaderCallable,
) -> EnumDriftResult:
    """Run F-CIC-CLC-ENUM-DRIFT at startup.

    All file/crypto I/O is via injected callables — gate code never imports
    ``hashlib``, ``cryptography``, or any I/O library directly.
    """
    subcodes: list[str] = []
    detail_parts: list[str] = []

    # ---- 1. Count check (in-code, cheapest first) ----
    actual_cic_count = len(CUSTOMER_IDENTITY_CATEGORY_VALUES)
    actual_clc_count = len(CAPITAL_LOGIC_CARD_VALUES)

    if actual_cic_count != canonical_cic_count():
        subcodes.append(f"{GATE_ID}.count_cic")
        detail_parts.append(
            f"CustomerIdentityCategory has {actual_cic_count} entries; "
            f"canonical is {canonical_cic_count()}"
        )

    if actual_clc_count != canonical_clc_count():
        subcodes.append(f"{GATE_ID}.count_clc")
        detail_parts.append(
            f"CapitalLogicCard has {actual_clc_count} entries; "
            f"canonical is {canonical_clc_count()}"
        )

    # ---- 2. Amendment-text count cross-check ----
    amendment_cic_count, amendment_clc_count = amendment_count_reader()
    if (
        amendment_cic_count != canonical_cic_count()
        or amendment_clc_count != canonical_clc_count()
    ):
        subcodes.append(f"{GATE_ID}.amendment_count_drift")
        detail_parts.append(
            f"v7.0.8 amendment §1 declares ({amendment_cic_count}, "
            f"{amendment_clc_count}); in-code constants are "
            f"({canonical_cic_count()}, {canonical_clc_count()})"
        )

    # ---- 3. Hash check ----
    module_bytes = enum_module_reader()
    actual_hash = hash_bytes(module_bytes)

    canonical_record = canonical_hash_reader()
    expected_hash = canonical_record["identity_capital_module_sha3_512"]

    if actual_hash != expected_hash:
        subcodes.append(f"{GATE_ID}.hash_mismatch")
        detail_parts.append(
            f"identity_capital.py SHA3-512 mismatch: "
            f"actual={actual_hash[:16]}..., expected={expected_hash[:16]}..."
        )

    # ---- 4. Signature verification on the reference record ----
    signature_valid = verify_hybrid_signature(
        canonical_record["signed_payload_bytes"],
        canonical_record["signature_ed25519"],
        canonical_record["operator_public_key_ed25519"],
        canonical_record["signature_ml_dsa_65"],
        canonical_record["operator_public_key_ml_dsa_65"],
    )
    if signature_valid is not True:
        subcodes.append(f"{GATE_ID}.signature_invalid")
        detail_parts.append(
            "operator signature on canonical_enum_hashes.yaml failed hybrid "
            "Ed25519+ML-DSA-65 verification"
        )

    if subcodes:
        return EnumDriftResult(
            passed=False,
            subcodes=tuple(subcodes),
            detail="; ".join(detail_parts),
        )

    return EnumDriftResult(
        passed=True,
        subcodes=(),
        detail="hash + signature + counts all match canonical",
    )
