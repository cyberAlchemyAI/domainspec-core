"""Legacy beneficiary_records ``consent_tier_history`` back-fill migration.

Per WS-J Slice 2 (2026-05-11) handoff + §13 v1 RT-C2-06 closure.

Operator-invoked, never auto-run. Walks
``orgs/<slug>/vault/operational/grants/<grant_id>/*/beneficiary_records/``
+ for each on-disk record that lacks a ``consent_tier_history`` field,
back-fills an empty signed history initialized with the record's
``created_at_utc`` (or ``captured_at``) as the floor consent_tier-set
event. The operator Ed25519-signs each migration via injected signer.

Fail-closed posture:

* If ``consent_tier_history`` already exists for any record AND
  ``force=False`` → :class:`MigrationAlreadyApplied` aborts the run.
* With ``force=True`` → existing histories are PRESERVED (NOT
  overwritten); the migration becomes a no-op for already-migrated
  records but the audit log entry records the no-op with
  ``status="already_applied"`` so the audit trail captures the
  operator-confirmed re-run.

Audit trail: every migrated record produces one JSONL row appended to
``orgs/<slug>/vault/operational/grants/<grant_id>/migrations/lock_history.v1.jsonl``
— mirrors the engineering ledger row shape but scoped to the per-org
vault namespace per Law 3.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final, Mapping, Optional, Protocol, Sequence, runtime_checkable

import yaml

from pipeline.orchestrator.seats.report_generator._canonical import (
    canonical_json_bytes,
    compute_sha3_512_hex,
)


# ---------------------------------------------------------------------------
# Failure code + status constants
# ---------------------------------------------------------------------------


F_MIGRATION_BENEFICIARY_HISTORY_BACKFILL: Final[str] = (
    "F-MIGRATION-BENEFICIARY-HISTORY-BACKFILL"
)

STATUS_BACKFILLED: Final[str] = "backfilled"
STATUS_ALREADY_APPLIED: Final[str] = "already_applied"
STATUS_SKIPPED_FORCE_FALSE: Final[str] = "skipped_force_false"
STATUS_ERROR: Final[str] = "error"

HISTORY_KIND_INITIAL: Final[str] = "initial"


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class MigrationError(Exception):
    """Base migration error."""


class MigrationAlreadyApplied(MigrationError):
    """Raised when a record already has consent_tier_history and force=False."""


class MigrationScanError(MigrationError):
    """Raised when scanning the operational subtree fails."""


# ---------------------------------------------------------------------------
# Injected signer Protocol
# ---------------------------------------------------------------------------


@runtime_checkable
class Ed25519SignerProtocol(Protocol):
    """Injected operator Ed25519 signer.

    ``__call__(message_bytes) -> signature_bytes`` returns the Ed25519
    signature over the canonical-JSON bytes of the migration payload
    under the operator's private key.
    """

    def __call__(self, message_bytes: bytes) -> bytes: ...


# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class MigrationRecordResult:
    """Outcome for a single beneficiary_records file."""

    record_path: str
    record_id: str
    status: str
    pre_migration_content_sha3_512: str
    post_migration_content_sha3_512: Optional[str] = None
    migration_signature: Optional[str] = None  # hex
    detail: str = ""


@dataclass(frozen=True, kw_only=True)
class MigrationRunResult:
    """Outcome of a full beneficiary_records migration run."""

    org_slug: str
    grant_id: str
    records_scanned: int
    records_backfilled: int
    records_already_applied: int
    records_skipped_force_false: int
    records_errored: int
    record_results: tuple[MigrationRecordResult, ...]
    audit_log_path: str
    invoked_at_utc: str


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def _operational_grant_root(
    *, repo_root: Path, org_slug: str, grant_id: str
) -> Path:
    return (
        repo_root / "orgs" / org_slug / "vault" / "operational" / "grants" / grant_id
    )


def _audit_log_path(
    *, repo_root: Path, org_slug: str, grant_id: str
) -> Path:
    return (
        _operational_grant_root(
            repo_root=repo_root, org_slug=org_slug, grant_id=grant_id
        )
        / "migrations"
        / "lock_history.v1.jsonl"
    )


def _find_beneficiary_records_files(
    *, repo_root: Path, org_slug: str, grant_id: str
) -> list[Path]:
    """Walk every period_<n>/beneficiary_records/ subtree + return *.yaml files."""
    grant_root = _operational_grant_root(
        repo_root=repo_root, org_slug=org_slug, grant_id=grant_id
    )
    if not grant_root.is_dir():
        raise MigrationScanError(
            f"operational grant root not found: {grant_root!r}"
        )
    files: list[Path] = []
    for period_dir in sorted(grant_root.iterdir()):
        if not period_dir.is_dir():
            continue
        beneficiary_dir = period_dir / "beneficiary_records"
        if not beneficiary_dir.is_dir():
            continue
        for f in sorted(beneficiary_dir.iterdir()):
            if f.suffix.lower() not in (".yaml", ".yml"):
                continue
            if not f.is_file():
                continue
            files.append(f)
    return files


# ---------------------------------------------------------------------------
# Per-record migration
# ---------------------------------------------------------------------------


def _load_record(path: Path) -> Mapping[str, object]:
    """``yaml.safe_load`` a beneficiary_records file; raises on parse error."""
    try:
        with open(path, "rb") as fh:
            content = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        raise MigrationError(
            f"YAML parse failure at {path!r}: {exc}"
        ) from exc
    if not isinstance(content, Mapping):
        raise MigrationError(
            f"beneficiary record at {path!r} not a Mapping (got "
            f"{type(content).__name__})"
        )
    return content


def _content_hash(content: Mapping[str, object]) -> str:
    return compute_sha3_512_hex(canonical_json_bytes(dict(content)))


def _initial_history_event(
    *,
    consent_tier: str,
    set_at_utc: str,
) -> Mapping[str, object]:
    """Build the floor consent_tier-set event for the initial history."""
    return {
        "kind": HISTORY_KIND_INITIAL,
        "tier": consent_tier,
        "set_at_utc": set_at_utc,
    }


def _signed_migration_payload(
    *,
    record_id: str,
    pre_content_sha3_512: str,
    history_event: Mapping[str, object],
    invoked_at_utc: str,
) -> dict[str, object]:
    """Canonical signing payload for the migration event."""
    return {
        "kind": "beneficiary_consent_tier_history_backfill",
        "record_id": record_id,
        "pre_migration_content_sha3_512": pre_content_sha3_512,
        "history_event": dict(history_event),
        "invoked_at_utc": invoked_at_utc,
    }


def _migrate_record(
    *,
    record_path: Path,
    record_content: Mapping[str, object],
    operator_signer: Ed25519SignerProtocol,
    invoked_at_utc: str,
    force: bool,
) -> MigrationRecordResult:
    """Migrate one beneficiary_records file.

    Returns a :class:`MigrationRecordResult` describing the outcome.
    Never partially-mutates: write happens after signature is computed.
    """
    record_id = str(record_content.get("record_id", record_path.stem))
    pre_hash = _content_hash(record_content)

    existing_history = record_content.get("consent_tier_history")
    if existing_history not in (None, ()):
        # An existing list (even empty) → already-migrated.
        if not force:
            raise MigrationAlreadyApplied(
                f"record {record_path.name!r} already has consent_tier_history "
                f"(use --force to acknowledge re-run no-op)"
            )
        return MigrationRecordResult(
            record_path=str(record_path),
            record_id=record_id,
            status=STATUS_ALREADY_APPLIED,
            pre_migration_content_sha3_512=pre_hash,
            detail=(
                "consent_tier_history already present; --force acknowledged; "
                "preserving existing history (no overwrite)"
            ),
        )

    # Determine the floor event's set_at_utc.
    set_at_utc = (
        str(record_content.get("created_at_utc"))
        if record_content.get("created_at_utc")
        else str(record_content.get("captured_at", invoked_at_utc))
    )
    consent_tier = str(record_content.get("consent_tier", "anonymized"))

    history_event = _initial_history_event(
        consent_tier=consent_tier, set_at_utc=set_at_utc
    )
    signing_payload = _signed_migration_payload(
        record_id=record_id,
        pre_content_sha3_512=pre_hash,
        history_event=history_event,
        invoked_at_utc=invoked_at_utc,
    )
    payload_bytes = canonical_json_bytes(signing_payload)
    try:
        signature_bytes = operator_signer(payload_bytes)
    except Exception as exc:
        return MigrationRecordResult(
            record_path=str(record_path),
            record_id=record_id,
            status=STATUS_ERROR,
            pre_migration_content_sha3_512=pre_hash,
            detail=f"signer raised {type(exc).__name__}: {exc!s}",
        )
    if not isinstance(signature_bytes, bytes):
        return MigrationRecordResult(
            record_path=str(record_path),
            record_id=record_id,
            status=STATUS_ERROR,
            pre_migration_content_sha3_512=pre_hash,
            detail=(
                f"signer returned {type(signature_bytes).__name__}; expected bytes"
            ),
        )
    signature_hex = signature_bytes.hex()

    # Build the migrated content.
    history_event_with_sig = dict(history_event)
    history_event_with_sig["set_by_operator_signature"] = signature_hex
    history_event_with_sig["set_by_operator_at_utc"] = invoked_at_utc

    migrated = dict(record_content)
    migrated["consent_tier_history"] = [history_event_with_sig]
    post_hash = _content_hash(migrated)

    # Atomic write — temp file + rename.
    tmp_path = record_path.with_suffix(record_path.suffix + ".tmp")
    try:
        with open(tmp_path, "w", encoding="utf-8") as fh:
            yaml.safe_dump(migrated, fh, default_flow_style=False, sort_keys=True)
        tmp_path.replace(record_path)
    except OSError as exc:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass
        return MigrationRecordResult(
            record_path=str(record_path),
            record_id=record_id,
            status=STATUS_ERROR,
            pre_migration_content_sha3_512=pre_hash,
            detail=f"write failure: {type(exc).__name__}: {exc!s}",
        )

    return MigrationRecordResult(
        record_path=str(record_path),
        record_id=record_id,
        status=STATUS_BACKFILLED,
        pre_migration_content_sha3_512=pre_hash,
        post_migration_content_sha3_512=post_hash,
        migration_signature=signature_hex,
        detail=(
            f"back-filled consent_tier_history with floor event tier="
            f"{consent_tier!r} set_at_utc={set_at_utc!r}"
        ),
    )


def _append_audit_log(
    *,
    audit_log_path: Path,
    result: MigrationRecordResult,
    invoked_at_utc: str,
    operator_key_id: str,
    org_slug: str,
    grant_id: str,
) -> None:
    """Append one JSONL row per migrated record."""
    audit_log_path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "module": "pipeline.orchestrator.migrations.beneficiary_records_history",
        "blueprint_section": (
            "section_13_data_collector.md / section_14_report_generator.md"
        ),
        "migration_kind": "beneficiary_consent_tier_history_backfill",
        "org_slug": org_slug,
        "grant_id": grant_id,
        "record_path": result.record_path,
        "record_id": result.record_id,
        "status": result.status,
        "pre_migration_content_sha3_512": result.pre_migration_content_sha3_512,
        "post_migration_content_sha3_512": result.post_migration_content_sha3_512,
        "migration_signature": result.migration_signature,
        "operator_key_id": operator_key_id,
        "invoked_at_utc": invoked_at_utc,
        "detail": result.detail,
        "lock_class": "data_migration",
    }
    with open(audit_log_path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")


# ---------------------------------------------------------------------------
# Top-level migration entry point
# ---------------------------------------------------------------------------


def run_beneficiary_records_history_migration(
    *,
    repo_root: Path,
    org_slug: str,
    grant_id: str,
    operator_signer: Ed25519SignerProtocol,
    operator_key_id: str,
    invoked_at_utc: str,
    backfill_empty_history: bool = True,
    force: bool = False,
) -> MigrationRunResult:
    """Run the beneficiary_records consent_tier_history back-fill migration.

    :param repo_root: workspace root containing ``orgs/``.
    :param org_slug: org slug under ``orgs/`` — Law 3 Org Isolation.
    :param grant_id: grant subtree under ``orgs/<slug>/vault/operational/grants/``.
    :param operator_signer: injected Ed25519 signer Protocol — produces the
        per-record migration signature over canonical-JSON of the signing
        payload.
    :param operator_key_id: operator key fingerprint string for audit log.
    :param invoked_at_utc: ISO-8601 UTC timestamp of the migration run.
    :param backfill_empty_history: when True (default) actually performs the
        back-fill; when False, scan-only mode (no writes).
    :param force: when True, allow re-run on already-migrated records (no-op
        with audit log entry); when False, fail-closed on first already-
        migrated record.

    :raises MigrationAlreadyApplied: if any record already has
        ``consent_tier_history`` and ``force=False``.
    :raises MigrationScanError: if the operational subtree is malformed.

    :returns: :class:`MigrationRunResult` summarizing the run.
    """
    if not org_slug:
        raise MigrationError("org_slug is required")
    if not grant_id:
        raise MigrationError("grant_id is required")
    if not isinstance(operator_signer, Ed25519SignerProtocol):
        # runtime_checkable Protocol — accept any object with __call__.
        if not callable(operator_signer):
            raise TypeError(
                f"operator_signer must be callable Ed25519SignerProtocol; got "
                f"{type(operator_signer).__name__}"
            )
    if not isinstance(repo_root, Path):
        raise TypeError(f"repo_root must be Path; got {type(repo_root).__name__}")

    files = _find_beneficiary_records_files(
        repo_root=repo_root, org_slug=org_slug, grant_id=grant_id
    )

    audit_log = _audit_log_path(
        repo_root=repo_root, org_slug=org_slug, grant_id=grant_id
    )

    record_results: list[MigrationRecordResult] = []
    backfilled = 0
    already_applied = 0
    skipped_force_false = 0
    errored = 0

    for record_path in files:
        try:
            content = _load_record(record_path)
        except MigrationError as exc:
            errored += 1
            record_results.append(
                MigrationRecordResult(
                    record_path=str(record_path),
                    record_id=record_path.stem,
                    status=STATUS_ERROR,
                    pre_migration_content_sha3_512="",
                    detail=str(exc),
                )
            )
            continue

        if not backfill_empty_history:
            # Scan-only mode — surface what WOULD be migrated.
            existing = content.get("consent_tier_history")
            if existing in (None, ()):
                skipped_force_false += 1
                record_results.append(
                    MigrationRecordResult(
                        record_path=str(record_path),
                        record_id=str(
                            content.get("record_id", record_path.stem)
                        ),
                        status=STATUS_SKIPPED_FORCE_FALSE,
                        pre_migration_content_sha3_512=_content_hash(content),
                        detail="scan-only: missing consent_tier_history",
                    )
                )
            else:
                already_applied += 1
                record_results.append(
                    MigrationRecordResult(
                        record_path=str(record_path),
                        record_id=str(
                            content.get("record_id", record_path.stem)
                        ),
                        status=STATUS_ALREADY_APPLIED,
                        pre_migration_content_sha3_512=_content_hash(content),
                        detail="scan-only: consent_tier_history already present",
                    )
                )
            continue

        try:
            result = _migrate_record(
                record_path=record_path,
                record_content=content,
                operator_signer=operator_signer,
                invoked_at_utc=invoked_at_utc,
                force=force,
            )
        except MigrationAlreadyApplied:
            # Fail-closed propagation (no audit log; whole run aborts).
            raise

        record_results.append(result)
        if result.status == STATUS_BACKFILLED:
            backfilled += 1
        elif result.status == STATUS_ALREADY_APPLIED:
            already_applied += 1
        elif result.status == STATUS_ERROR:
            errored += 1

        _append_audit_log(
            audit_log_path=audit_log,
            result=result,
            invoked_at_utc=invoked_at_utc,
            operator_key_id=operator_key_id,
            org_slug=org_slug,
            grant_id=grant_id,
        )

    return MigrationRunResult(
        org_slug=org_slug,
        grant_id=grant_id,
        records_scanned=len(files),
        records_backfilled=backfilled,
        records_already_applied=already_applied,
        records_skipped_force_false=skipped_force_false,
        records_errored=errored,
        record_results=tuple(record_results),
        audit_log_path=str(audit_log),
        invoked_at_utc=invoked_at_utc,
    )


__all__ = [
    "Ed25519SignerProtocol",
    "F_MIGRATION_BENEFICIARY_HISTORY_BACKFILL",
    "HISTORY_KIND_INITIAL",
    "MigrationAlreadyApplied",
    "MigrationError",
    "MigrationRecordResult",
    "MigrationRunResult",
    "MigrationScanError",
    "STATUS_ALREADY_APPLIED",
    "STATUS_BACKFILLED",
    "STATUS_ERROR",
    "STATUS_SKIPPED_FORCE_FALSE",
    "run_beneficiary_records_history_migration",
]
