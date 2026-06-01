"""M7 health-tuple assembly + signing call-site (§4.10).

Composes per-channel DISCOVER health states into a :class:`HealthTuple`,
delegates HMAC signing to Section 1's ``sign_health_tuple`` primitive, and
writes the signed artefact to the org run log via the §2 vault write path.

Scout never opens the keystore and never crafts the HMAC buffer itself —
the ``SessionSigner`` Protocol binds the Section 1 primitive at the seam.
``VaultWriter`` does the same for the §2 write dispatcher so tests can
substitute an in-memory recorder.

Blueprint anchors:
- §2.3 HealthTuple + SignedHealthTuple schemas (Round 1 ``_types.py``)
- §4.10 assemble_and_sign_health_tuple (this module)
- §6.10 F-SCOUT-H-0{1..4} + §6.7 F-SCOUT-V-06 failure taxonomy
- §8 SESSION_HMAC_KEY_LEN_BYTES + RUN_ID_HEX_LEN pins
- §9 INTENT_SCOUT_RUN_LOG_WRITE
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import time
from typing import Callable, Optional, Protocol

from pipeline.scout._constants import (
    HEALTH_DEGRADED,
    HEALTH_FAILED,
    HEALTH_OK,
    INTENT_SCOUT_RUN_LOG_WRITE,
    RUN_ID_HEX_LEN,
)
from pipeline.scout._types import (
    HealthTuple,
    SignedHealthTuple,
    health_tuple_canonical_bytes,
)

__all__ = [
    "HealthTupleSchemaError",
    "SessionSigner",
    "VaultWriter",
    "assemble_and_sign_health_tuple",
]


# ---------------------------------------------------------------------------
# Error taxonomy — §6.10 + §6.7 F-SCOUT-V-06
# ---------------------------------------------------------------------------


class HealthTupleSchemaError(RuntimeError):
    """Raised for any Round-2 schema or entropy event.

    ``code`` is the primary failure code (one of the F-SCOUT-H-* / -V-06
    families). ``sub_tag`` carries §6.10 sub-codes such as
    ``urandom_short_read``.
    """

    def __init__(self, message: str, *, code: str, sub_tag: Optional[str] = None):
        super().__init__(message)
        self.code = code
        self.sub_tag = sub_tag


# ---------------------------------------------------------------------------
# Injection Protocols (E-017 pattern)
# ---------------------------------------------------------------------------


class SessionSigner(Protocol):
    """Minimal session-shape Scout needs for M7 signing.

    Production binding: a :class:`pipeline.sovereignty.session.Session`
    plus a ``sign_health_tuple`` closure over
    :func:`pipeline.sovereignty.session.sign_health_tuple`. Tests inject
    a dataclass-style fake whose ``sign_health_tuple`` returns a fixed
    64-byte digest.
    """

    session_id: str
    slug: str
    hmac_key_id: str

    def sign_health_tuple(self, tuple_bytes: bytes) -> bytes: ...


class VaultWriter(Protocol):
    """§2 vault-write seam.

    Production binding adapts
    :func:`pipeline.vault.vault_write.vault_write`. Tests inject a memory
    writer that records the ``(path, bytes_, intent, session_id, slug)``
    tuple for assertion.
    """

    def write(
        self,
        *,
        path: str,
        bytes_: bytes,
        intent: str,
        session_id: str,
        slug: str,
    ) -> None: ...


ClockFn = Callable[[], str]
UrandomFn = Callable[[int], bytes]
MonotonicFn = Callable[[], int]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


_CHANNEL_KEYS: tuple[str, ...] = ("A", "B", "C", "D", "E", "F")
_CHANNEL_A_ENDPOINTS: tuple[str, ...] = ("grants.gov", "sam.gov", "usaspending.gov")
_VALID_STATES: frozenset[str] = frozenset({HEALTH_OK, HEALTH_DEGRADED, HEALTH_FAILED})
_RUN_TIEBREAK_SEED_LEN: int = 16
_RUN_URANDOM_LEN: int = 8


def _default_clock() -> str:
    """UTC ISO-8601 second-resolution timestamp with ``Z`` suffix."""
    now = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")
    return now.replace("+00:00", "Z")


def _fresh_urandom(n: int, urandom: UrandomFn) -> bytes:
    """§4.10 A-v3-10 / RT-v2-LOW-03 short-read hardening.

    One retry on short read; second short read raises
    ``F-SCOUT-H-03.urandom_short_read``.
    """
    buf = urandom(n)
    if len(buf) != n:
        buf = urandom(n)
        if len(buf) != n:
            raise HealthTupleSchemaError(
                f"F-SCOUT-H-03.urandom_short_read: os.urandom({n}) returned "
                f"{len(buf)} bytes twice",
                code="F-SCOUT-H-03",
                sub_tag="urandom_short_read",
            )
    return buf


def _run_log_health_path(slug: str, run_id: str) -> str:
    """Composed path for the signed run-log artefact.

    String composition rather than ``Path`` concatenation — the
    :class:`VaultWriter` binding is responsible for resolving this against
    the org vault root with :func:`pipeline.sovereignty.isolation.within_org_root`.
    """
    return f"orgs/{slug}/scout/run_log/{run_id}-health.json"


def _signed_health_tuple_bytes(signed: SignedHealthTuple) -> bytes:
    """Canonical-JSON encoding of a SignedHealthTuple for vault storage."""
    payload = {
        "tuple_canonical": signed.tuple_canonical.hex(),
        "hmac_sha3_512": signed.hmac_sha3_512.hex(),
        "signed_at_utc": signed.signed_at_utc,
        "hmac_key_id": signed.hmac_key_id,
    }
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


# ---------------------------------------------------------------------------
# Public entry — assemble_and_sign_health_tuple
# ---------------------------------------------------------------------------


def assemble_and_sign_health_tuple(
    *,
    session: SessionSigner,
    per_channel: dict[str, str],
    per_channel_a_endpoints: dict[str, str],
    run_wall_ns: int,
    run_tiebreak_seed: bytes,
    vault_writer: VaultWriter,
    clock: ClockFn = _default_clock,
    urandom: UrandomFn = os.urandom,
    monotonic_ns: MonotonicFn = time.monotonic_ns,
) -> SignedHealthTuple:
    """Assemble, sign, and persist a :class:`SignedHealthTuple`. [§4.10]

    Raises :class:`HealthTupleSchemaError` with one of the §6.10 / §6.7
    failure codes on any validation or entropy event. Propagates
    underlying Section 1 / §2 errors wrapped as F-SCOUT-H-04 with
    ``__cause__`` preserved.
    """

    for ch in _CHANNEL_KEYS:
        state = per_channel.get(ch)
        if state not in _VALID_STATES:
            raise HealthTupleSchemaError(
                f"F-SCOUT-H-01: channel {ch} missing or invalid (got {state!r})",
                code="F-SCOUT-H-01",
            )
    for ep in _CHANNEL_A_ENDPOINTS:
        state = per_channel_a_endpoints.get(ep)
        if state not in _VALID_STATES:
            raise HealthTupleSchemaError(
                f"F-SCOUT-H-02: endpoint {ep} missing or invalid (got {state!r})",
                code="F-SCOUT-H-02",
            )

    if len(run_tiebreak_seed) != _RUN_TIEBREAK_SEED_LEN:
        raise HealthTupleSchemaError(
            f"F-SCOUT-V-06: run_tiebreak_seed length={len(run_tiebreak_seed)} "
            f"(expected {_RUN_TIEBREAK_SEED_LEN})",
            code="F-SCOUT-V-06",
        )

    backbone_failed = all(
        per_channel_a_endpoints[ep] == HEALTH_FAILED for ep in _CHANNEL_A_ENDPOINTS
    )

    run_monotonic_ns = monotonic_ns()
    run_urandom = _fresh_urandom(_RUN_URANDOM_LEN, urandom)
    digest_material = (
        f"{session.session_id}|{run_wall_ns}|{run_monotonic_ns}|".encode("utf-8")
        + run_urandom
    )
    run_id = hashlib.sha3_512(digest_material).hexdigest()[:RUN_ID_HEX_LEN]

    tuple_obj = HealthTuple(
        session_id=session.session_id,
        slug=session.slug,
        run_id=run_id,
        run_wall_ns=run_wall_ns,
        channel_a=per_channel["A"],
        channel_b=per_channel["B"],
        channel_c=per_channel["C"],
        channel_d=per_channel["D"],
        channel_e=per_channel["E"],
        channel_f=per_channel["F"],
        channel_a_endpoints=dict(per_channel_a_endpoints),
        backbone_failed=backbone_failed,
        run_entropy={
            "run_urandom_hex": run_urandom.hex(),
            "run_monotonic_ns": run_monotonic_ns,
            "run_tiebreak_seed_hex": run_tiebreak_seed.hex(),
        },
    )

    canonical = health_tuple_canonical_bytes(tuple_obj)

    try:
        signature = session.sign_health_tuple(canonical)
    except Exception as exc:  # F-SCOUT-H-04: Section 1 propagation.
        raise HealthTupleSchemaError(
            f"F-SCOUT-H-04: sign_health_tuple raised: {exc}",
            code="F-SCOUT-H-04",
        ) from exc

    signed = SignedHealthTuple(
        tuple_canonical=canonical,
        hmac_sha3_512=signature,
        signed_at_utc=clock(),
        hmac_key_id=session.hmac_key_id,
    )

    vault_writer.write(
        path=_run_log_health_path(session.slug, run_id),
        bytes_=_signed_health_tuple_bytes(signed),
        intent=INTENT_SCOUT_RUN_LOG_WRITE,
        session_id=session.session_id,
        slug=session.slug,
    )

    return signed
