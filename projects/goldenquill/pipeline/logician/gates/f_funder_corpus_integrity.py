"""F-FUNDER-CORPUS-INTEGRITY — PRE-load + POST-load gate (Law 5 fabrication, P0).

Per architecture v7.0.5 §5.7 + companion `section_04_v7_0_5_companion.md`.

The Funder Intel read pipeline wrapper recomputes SHA3-512 of on-disk
bytes and compares against the recorded `content_hash` in the register
BEFORE the bytes reach Scout / Scribe / Editor / Judge / Red Team. Any
mismatch fail-closes — the doc is excluded from the seat working set
and quarantined to ``vault_shared/funder_intelligence/_quarantine/``.

Cycle 2 Probe C closure: process-scope BYTE caching is FORBIDDEN. The
wrapper MAY cache parsed content (post-verification) within a single
agent invocation but MUST recompute SHA3-512 of the on-disk bytes on
every `load()` call regardless of prior verification state in the same
process. This gate enforces only the per-call comparison; the caller's
loop discipline enforces the no-byte-caching rule.

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional

from pipeline.logician.gates._protocols import HashBytesCallable


F_FUNDER_CORPUS_INTEGRITY: Final[str] = "F-FUNDER-CORPUS-INTEGRITY"


@dataclass(frozen=True, kw_only=True)
class FunderCorpusIntegrityResult:
    """Result of F-FUNDER-CORPUS-INTEGRITY check."""

    success: bool
    failure_code: Optional[str]
    detail: str
    computed_hash_prefix16: Optional[str] = None
    recorded_hash_prefix16: Optional[str] = None


def _hashlib_sha3_512(b: bytes) -> str:
    """Default HashBytesCallable — pure-Python SHA3-512 hex digest.

    Imported lazily inside this helper to keep the module-load surface
    free of `import hashlib` per the §4 v2.2 _protocols.py discipline
    (gates declare crypto callables as Protocol; module load runs no
    crypto). Production wiring binds this default at first use.
    """
    import hashlib  # noqa: WPS433 — lazy by design (see docstring)
    return hashlib.sha3_512(b).hexdigest()


def check_funder_corpus_integrity(
    *,
    doc_bytes: bytes,
    recorded_hash: str,
    hash_bytes: Optional[HashBytesCallable] = None,
) -> FunderCorpusIntegrityResult:
    """PRE/POST-load gate: SHA3-512 of doc_bytes must match recorded hash.

    Parameters
    ----------
    doc_bytes
        On-disk bytes of the Funder Intel doc the wrapper just read.
    recorded_hash
        SHA3-512 hex digest as recorded in
        ``vault_shared/funder_intelligence/register.yaml`` `content_hash`.
        Compared as a normalized lowercase hex string.
    hash_bytes
        Injected HashBytesCallable for SHA3-512 hex digest computation.
        None → uses pure-Python `hashlib.sha3_512` (lazy import).

    Returns
    -------
    FunderCorpusIntegrityResult. Passes when computed hash == recorded
    hash (case-insensitive); fails (P0) otherwise.
    """
    if not recorded_hash:
        return FunderCorpusIntegrityResult(
            success=False,
            failure_code=F_FUNDER_CORPUS_INTEGRITY,
            detail="recorded_hash empty — register row malformed",
        )

    hasher = hash_bytes if hash_bytes is not None else _hashlib_sha3_512
    computed = hasher(doc_bytes)
    computed_norm = computed.strip().lower()
    recorded_norm = recorded_hash.strip().lower()

    if computed_norm == recorded_norm:
        return FunderCorpusIntegrityResult(
            success=True,
            failure_code=None,
            detail="SHA3-512 of doc_bytes matches recorded content_hash",
            computed_hash_prefix16=computed_norm[:16],
            recorded_hash_prefix16=recorded_norm[:16],
        )
    return FunderCorpusIntegrityResult(
        success=False,
        failure_code=F_FUNDER_CORPUS_INTEGRITY,
        detail=(
            "SHA3-512 of doc_bytes does not match recorded content_hash — "
            "tamper or corruption; doc excluded from seat working set, "
            "quarantine to vault_shared/funder_intelligence/_quarantine/"
        ),
        computed_hash_prefix16=computed_norm[:16],
        recorded_hash_prefix16=recorded_norm[:16],
    )
