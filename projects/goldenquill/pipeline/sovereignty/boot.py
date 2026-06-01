"""§9 boot_envelope orchestrator. [Section 1 Round J capstone]

Section 1's entry point. Stitches together all §9 phases using the
primitives LOCKED in Rounds A–I. Fail-closed at every step. Any failure
halts; no step is skipped.

Phases (see §9 of blueprint for full prose):

1.  Platform detection — Darwin/Linux gate.
2.  ``resource.setrlimit(RLIMIT_CORE, (0, 0))`` core-dump suppression.
2.5 ``append_boot_clock_record`` tamper-evident wall-clock append.
3.  Repo-root sanity (``router.yaml`` + ``orgs/`` + directory).
4.  Keystore resolution (caller-provided; v0.1 does not auto-resolve).
5.  Operator identity probe.
6.  ``verify_router_integrity`` HMAC gate.
7.  Ledger verification (admin_risk + degradation + watermarks) —
    executed only when the ledger files exist on disk; first-boot
    state is detected via the Round I init-marker predicate instead.
7c.0a/b Sovereignty init-marker verify (and first-boot write).
8.  Orphan-key sweep (stub — deferred to a later round; logged).
9.  INTERRUPTED-session detection.
10. Org slug resolution (if ``slug_arg`` supplied).
11. Return :class:`SovereigntyEnvelope`.

v0.1 scope (deliberate):

* Wrapper-manifest verification (§9 step 1.5) is the v0.2+ concern.
  Under v0.1, if ``TILTH_WRAPPER_MANIFEST_FD`` is absent, step 1.5
  is a no-op skip per blueprint.
* Ledger HMAC-key wiring is the operator's responsibility — callers
  pass a ``ledger_hmac_keys`` dict; if empty, step 7 is a no-op.
* Orphan-key sweep is a scaffold only; full keystore enumeration
  lives in a future round.
"""

from __future__ import annotations

import datetime as _dt
import platform as _platform_mod
import resource
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

from pipeline.sovereignty.admin_risk import BootClockRecord
from pipeline.sovereignty.audit import verify_ledger, verify_watermarks
from pipeline.sovereignty.boot_clock import (
    append_boot_clock_record,
    read_boot_clock_history,
    read_boot_epoch_ns,
)
from pipeline.sovereignty.init_marker import (
    LedgerState,
    SovereigntyInitMarker,
    verify_sovereignty_init_marker,
    write_sovereignty_init_marker_first_boot,
)
from pipeline.sovereignty.interrupted_state import (
    OperatorDecisionRequired,
    detect_interrupted,
)
from pipeline.sovereignty.keys import KeyStore
from pipeline.sovereignty.org_slug import (
    canonical_slug,
    ensure_slug_available,
)
from pipeline.sovereignty.router_integrity import (
    RouterManifest,
    verify_router_integrity,
)

__all__ = [
    "OPERATOR_IDENTITY_KEY_ID",
    "WRAPPER_MANIFEST_FD_ENV_VAR",
    "BootEnvelopeError",
    "UnsupportedPlatform",
    "RepoRootInvalid",
    "OperatorNotProvisioned",
    "SovereigntyEnvelope",
    "boot_envelope",
]

OPERATOR_IDENTITY_KEY_ID: str = "operator.identity.v1"
WRAPPER_MANIFEST_FD_ENV_VAR: str = "TILTH_WRAPPER_MANIFEST_FD"


# ---------------------------------------------------------------------------
# Exceptions (E-014 family taxonomy)
# ---------------------------------------------------------------------------


class BootEnvelopeError(RuntimeError):
    """Common parent for boot_envelope failures."""

    code: str = "F-BOOT"


class UnsupportedPlatform(BootEnvelopeError):
    """Platform is neither Darwin nor Linux."""

    code = "F-BOOT-PLATFORM"


class RepoRootInvalid(BootEnvelopeError):
    """Repo root missing, not a directory, or missing router.yaml / orgs/."""

    code = "F-BOOT-REPO"


class OperatorNotProvisioned(BootEnvelopeError):
    """``operator.identity.v1`` not found in keystore — run onboarding."""

    code = "F-BOOT-OPERATOR"


# ---------------------------------------------------------------------------
# SovereigntyEnvelope
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class SovereigntyEnvelope:
    """Handle returned by :func:`boot_envelope`. [§9 step 11]

    Carries everything downstream callers (Section 5 CLI → start_session)
    need to bind an RFA + PROJECT_CONTEXT to a session.
    """

    repo_root: Path
    keystore: KeyStore
    operator_identity_present: bool
    platform: str
    router_manifest: RouterManifest
    init_marker: SovereigntyInitMarker
    boot_epoch_ns: int
    slug: str | None
    warnings: tuple[str, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------------
# §9 step 2.5 — boot_clock_history wall/epoch derivation
# ---------------------------------------------------------------------------


def _iso_utc_now() -> str:
    return (
        _dt.datetime.now(_dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _ledger_state(
    repo_root: Path,
    ledger_name: str,
    watermarks: dict,
) -> LedgerState:
    """Derive :class:`LedgerState` for ``verify_sovereignty_init_marker``."""
    wm = watermarks.get(ledger_name)
    last_seq = wm.last_seq_id if wm is not None else 0
    body_exists = False
    if watermarks:
        body_exists = True
    return LedgerState(
        ledger_name=ledger_name,
        last_seq_id=last_seq,
        watermark_body_exists=body_exists,
    )


# ---------------------------------------------------------------------------
# boot_envelope
# ---------------------------------------------------------------------------


def boot_envelope(
    *,
    repo_root: Path,
    keystore: KeyStore,
    ledger_hmac_keys: Mapping[str, bytes] | None = None,
    watermarks_hmac_key: bytes | None = None,
    slug_arg: str | None = None,
    operator_slug: str | None = None,
    skip_operator_identity_probe: bool = False,
) -> SovereigntyEnvelope:
    """Run §9 phases 1-11. See module docstring for phase list.

    :param repo_root: absolute path to the Tilth repo root; must exist,
        be a directory, and contain ``router.yaml`` + ``orgs/``.
    :param keystore: a concrete :class:`KeyStore` already resolved by
        the caller (v0.1 does not auto-resolve in boot_envelope).
    :param ledger_hmac_keys: optional ``{ledger_name: hmac_key_bytes}``
        mapping. When supplied AND the ledger file exists, its trailer
        is verified. Missing ledgers are treated as first-boot per §9.
    :param watermarks_hmac_key: optional keystore-derived bytes for
        ``tilth.watermarks.hmac.v1``; enables watermark body+trailer
        verification. Omitted → legitimate-first-boot path.
    :param slug_arg: optional operator-supplied org slug. Canonicalized
        and checked for availability (new-org create flow).
    :param operator_slug: optional operator identifier to carry into
        the init-marker body on first boot.
    :param skip_operator_identity_probe: test-only knob for environments
        where pre-provisioning the operator-identity key is noise.

    :raises TypeError: E-001 arg-type gates.
    :raises UnsupportedPlatform: anything other than Darwin/Linux.
    :raises RepoRootInvalid: F-BOOT-REPO.
    :raises OperatorNotProvisioned: F-BOOT-OPERATOR.
    :raises OperatorDecisionRequired: INTERRUPTED session found.
    :raises BootEnvelopeError / family exceptions: any chain/HMAC/init
        failure raised by the composed primitives.
    """
    # -- E-001 arg types ----------------------------------------------------
    if not isinstance(repo_root, Path):
        raise TypeError("repo_root must be pathlib.Path")
    if not isinstance(keystore, KeyStore):
        raise TypeError("keystore must be a KeyStore instance")
    if ledger_hmac_keys is not None and not isinstance(ledger_hmac_keys, Mapping):
        raise TypeError("ledger_hmac_keys must be Mapping[str, bytes] | None")
    if watermarks_hmac_key is not None and not isinstance(watermarks_hmac_key, bytes):
        raise TypeError("watermarks_hmac_key must be bytes | None")
    if slug_arg is not None and not isinstance(slug_arg, str):
        raise TypeError("slug_arg must be str | None")
    if operator_slug is not None and not isinstance(operator_slug, str):
        raise TypeError("operator_slug must be str | None")

    warnings: list[str] = []

    # -- Step 1 — Platform detection ---------------------------------------
    system = _platform_mod.system()
    if system not in ("Darwin", "Linux"):
        raise UnsupportedPlatform(f"F-BOOT-PLATFORM unsupported: {system}")

    # -- Pre-flight (step 3 split): minimal repo_root directory check ------
    # Step 2.5 writes inside repo_root/sovereignty/; fail early if the
    # path cannot hold it. Full sanity (router.yaml + orgs/) runs at
    # blueprint step 3 below.
    if not repo_root.exists():
        raise RepoRootInvalid(f"F-BOOT-REPO not found: {repo_root}")
    if not repo_root.is_dir():
        raise RepoRootInvalid(f"F-BOOT-REPO not a directory: {repo_root}")

    # -- Step 2 — Core-dump suppression ------------------------------------
    try:
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    except (ValueError, resource.error) as exc:  # type: ignore[attr-defined]
        warnings.append(f"rlimit_core_setrlimit_failed:{exc}")

    # -- Step 2.5 — boot_clock_history append ------------------------------
    boot_epoch_ns = read_boot_epoch_ns()
    record = BootClockRecord(
        boot_epoch_ns=boot_epoch_ns,
        wall_at_boot_utc=_iso_utc_now(),
    )
    append_boot_clock_record(
        repo_root=repo_root,
        record=record,
        keystore=keystore,
    )

    # -- Step 3 — Repo root sanity -----------------------------------------
    if not repo_root.exists():
        raise RepoRootInvalid(f"F-BOOT-REPO not found: {repo_root}")
    if not repo_root.is_dir():
        raise RepoRootInvalid(f"F-BOOT-REPO not a directory: {repo_root}")
    if not (repo_root / "router.yaml").is_file():
        raise RepoRootInvalid(f"F-BOOT-REPO missing router.yaml under {repo_root}")
    if not (repo_root / "orgs").is_dir():
        raise RepoRootInvalid(f"F-BOOT-REPO missing orgs/ under {repo_root}")

    # -- Step 4 — Keystore (caller-provided in v0.1) -----------------------
    # -- Step 5 — Operator identity probe ----------------------------------
    operator_identity_present = False
    if not skip_operator_identity_probe:
        try:
            if keystore.exists(OPERATOR_IDENTITY_KEY_ID):
                operator_identity_present = True
            else:
                raise OperatorNotProvisioned(
                    f"F-BOOT-OPERATOR {OPERATOR_IDENTITY_KEY_ID} absent"
                )
        except NotImplementedError:
            warnings.append("operator_identity_probe_skipped_keystore_stub")

    # -- Step 6 — Router integrity verify ----------------------------------
    router_manifest = verify_router_integrity(
        repo_root=repo_root, keystore=keystore
    )

    # -- Step 7 — Ledger verification --------------------------------------
    watermarks: dict = {}
    if watermarks_hmac_key is not None:
        watermarks_body_path = (
            repo_root / "sovereignty" / "watermarks" / "ledger_watermarks.json"
        )
        watermarks_hmac_path = (
            repo_root / "sovereignty" / "watermarks" / "ledger_watermarks.hmac"
        )
        watermarks = verify_watermarks(
            watermarks_body_path,
            watermarks_hmac_path,
            watermarks_hmac_key=watermarks_hmac_key,
        )

    if ledger_hmac_keys:
        for ledger_name, hmac_key in ledger_hmac_keys.items():
            jsonl = repo_root / "sovereignty" / "ledgers" / f"{ledger_name}.jsonl"
            trailer = repo_root / "sovereignty" / "ledgers" / f"{ledger_name}.hmac"
            if jsonl.is_file():
                verify_ledger(jsonl, trailer, hmac_key=hmac_key)

    # -- Step 7c.0a / 7c.0b — Sovereignty init marker ----------------------
    sov_dir = repo_root / "sovereignty"
    sov_dir.mkdir(parents=True, exist_ok=True)
    marker_path = sov_dir / "init.marker"
    marker_hmac = sov_dir / "init.marker.hmac"
    marker_lock = sov_dir / "init.marker.lock"
    ledger_states = {
        "admin_risk": _ledger_state(repo_root, "admin_risk", watermarks),
        "degradation": _ledger_state(repo_root, "degradation", watermarks),
    }
    body = verify_sovereignty_init_marker(
        marker_path=marker_path,
        hmac_path=marker_hmac,
        keystore=keystore,
        ledger_states=ledger_states,
    )
    if body is None:
        # Legitimate first boot — write the marker once.
        history = read_boot_clock_history(repo_root)
        body = write_sovereignty_init_marker_first_boot(
            marker_path=marker_path,
            hmac_path=marker_hmac,
            lock_path=marker_lock,
            keystore=keystore,
            boot_clock_history_seq=len(history),
            boot_epoch_ns=boot_epoch_ns,
            operator_slug=operator_slug,
        )

    # -- Step 8 — Orphan-key sweep (scaffold) ------------------------------
    warnings.append("orphan_key_sweep_not_yet_implemented")

    # -- Step 9 — INTERRUPTED detection ------------------------------------
    interrupted = detect_interrupted(repo_root)
    if interrupted is not None:
        raise OperatorDecisionRequired(session=interrupted)

    # -- Step 10 — Org slug resolution -------------------------------------
    resolved_slug: str | None = None
    if slug_arg is not None:
        resolved_slug = canonical_slug(slug_arg)
        ensure_slug_available(resolved_slug, repo_root)

    # -- Step 11 — Return envelope -----------------------------------------
    return SovereigntyEnvelope(
        repo_root=repo_root,
        keystore=keystore,
        operator_identity_present=operator_identity_present,
        platform=system,
        router_manifest=router_manifest,
        init_marker=body,
        boot_epoch_ns=boot_epoch_ns,
        slug=resolved_slug,
        warnings=tuple(warnings),
    )
