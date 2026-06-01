"""``tilth migrate beneficiary_records`` — legacy consent_tier_history back-fill CLI.

Authority
---------
§13 v1 LOCKED 2026-05-10 (RT-C2-06 closure). WS-J Slice 2 handoff
(2026-05-11).

Usage
-----
::

    # Live back-fill with operator signing key (raw 32-byte file or PEM/PKCS8)
    python -m pipeline.cli.tilth_migrate_beneficiary_records \\
        --org-slug mycosymbiotics_cooperative \\
        --grant-id VAPG-FY26-PLANNING \\
        --signed-by ~/.tilth/op_ed25519.key \\
        --operator-key-id op-001 \\
        --backfill-empty-history

    # Scan-only — show what WOULD migrate without writing
    python -m pipeline.cli.tilth_migrate_beneficiary_records \\
        --org-slug mycosymbiotics_cooperative \\
        --grant-id VAPG-FY26-PLANNING \\
        --signed-by ~/.tilth/op_ed25519.key \\
        --operator-key-id op-001 \\
        --no-backfill-empty-history

    # --force allows no-op re-run on already-migrated records (default
    # fail-closes on the first one).

Exit codes
----------
* 0 — migration completed; audit log written.
* 1 — fail-closed (already-applied records without ``--force``, scan errors,
  signer failures, write IO errors).
* 2 — CLI argument error (handled by argparse).

What this CLI is NOT
--------------------
* Not Intake — Intake produces the initial beneficiary_records; this CLI
  retro-fits the §13 v1 RT-C2-06 ``consent_tier_history`` schema field.
* Not the Logician — gate predicates that consume ``consent_tier_history``
  fire at report finalize time, not by this migration CLI.
* Not idempotent without ``--force`` — by design. Fail-closed on second run
  acknowledges that operator must explicitly confirm a re-run.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Sequence

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from pipeline.orchestrator.migrations.beneficiary_records_history import (
    MigrationAlreadyApplied,
    MigrationError,
    MigrationRunResult,
    MigrationScanError,
    run_beneficiary_records_history_migration,
)


# ---------------------------------------------------------------------------
# argparse
# ---------------------------------------------------------------------------


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tilth_migrate_beneficiary_records",
        description=(
            "Back-fill consent_tier_history on legacy beneficiary_records "
            "operational-data rows per §13 v1 RT-C2-06 closure. Operator-"
            "invoked; signs each migration via injected Ed25519 key. "
            "Fail-closed on already-migrated records unless --force."
        ),
    )
    parser.add_argument(
        "--org-slug",
        dest="org_slug",
        required=True,
        help="Org slug under orgs/<slug>/ — Law 3 Org Isolation enforced.",
    )
    parser.add_argument(
        "--grant-id",
        dest="grant_id",
        required=True,
        help=(
            "Grant id under orgs/<slug>/vault/operational/grants/<grant_id>/."
        ),
    )
    parser.add_argument(
        "--repo-root",
        dest="repo_root",
        type=Path,
        default=Path.cwd(),
        help="Workspace root (default: current working directory).",
    )
    parser.add_argument(
        "--signed-by",
        dest="signing_key_file",
        type=Path,
        required=True,
        help=(
            "Path to the operator's Ed25519 private key (raw 32-byte file "
            "OR PKCS8/PEM)."
        ),
    )
    parser.add_argument(
        "--operator-key-id",
        dest="operator_key_id",
        required=True,
        help="Operator key fingerprint string used in audit trail.",
    )
    parser.add_argument(
        "--backfill-empty-history",
        dest="backfill_empty_history",
        action="store_true",
        default=True,
        help=(
            "Perform the back-fill (default). Use --no-backfill-empty-history "
            "for scan-only mode."
        ),
    )
    parser.add_argument(
        "--no-backfill-empty-history",
        dest="backfill_empty_history",
        action="store_false",
        help="Scan-only mode — no writes; surface what WOULD migrate.",
    )
    parser.add_argument(
        "--force",
        dest="force",
        action="store_true",
        help=(
            "Allow re-run on already-migrated records (no-op; audit entry "
            "still recorded). Default: fail-closed on first already-"
            "migrated record."
        ),
    )
    parser.add_argument(
        "--json-output",
        dest="json_output",
        action="store_true",
        help="Emit machine-readable JSON summary on stdout.",
    )
    parser.add_argument(
        "--quiet",
        dest="quiet",
        action="store_true",
        help="Suppress per-record human-readable rendering.",
    )
    return parser


# ---------------------------------------------------------------------------
# Key loading (mirrors tilth_review_classify.py pattern)
# ---------------------------------------------------------------------------


def _load_signing_key(path: Path) -> bytes:
    if not path.is_file():
        raise SystemExit(f"error: signing key file not found at {path}")
    raw = path.read_bytes()
    if len(raw) == 32:
        return raw
    try:
        loaded = serialization.load_pem_private_key(raw, password=None)
    except Exception as exc:  # noqa: BLE001 — surface to operator
        raise SystemExit(
            f"error: signing key at {path} is neither raw 32 bytes nor PEM "
            f"({type(exc).__name__}: {exc})"
        ) from exc
    if not isinstance(loaded, ed25519.Ed25519PrivateKey):
        raise SystemExit(
            f"error: signing key at {path} is not Ed25519 (got "
            f"{type(loaded).__name__})"
        )
    return loaded.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )


def _build_signer(signing_key_bytes: bytes):
    """Construct a closed-over Ed25519 signer callable."""
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(signing_key_bytes)

    def _sign(message_bytes: bytes) -> bytes:
        return private_key.sign(message_bytes)

    return _sign


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _summarize_result(result: MigrationRunResult) -> dict:
    return {
        "ok": True,
        "org_slug": result.org_slug,
        "grant_id": result.grant_id,
        "records_scanned": result.records_scanned,
        "records_backfilled": result.records_backfilled,
        "records_already_applied": result.records_already_applied,
        "records_skipped_force_false": result.records_skipped_force_false,
        "records_errored": result.records_errored,
        "audit_log_path": result.audit_log_path,
        "invoked_at_utc": result.invoked_at_utc,
        "record_results": [
            {
                "record_path": r.record_path,
                "record_id": r.record_id,
                "status": r.status,
                "pre_migration_content_sha3_512": r.pre_migration_content_sha3_512,
                "post_migration_content_sha3_512": r.post_migration_content_sha3_512,
                "migration_signature_short": (
                    (r.migration_signature or "")[:16] if r.migration_signature else ""
                ),
                "detail": r.detail,
            }
            for r in result.record_results
        ],
    }


def _render_human(result: MigrationRunResult) -> str:
    lines: list[str] = []
    lines.append("")
    lines.append("=== beneficiary_records consent_tier_history migration ===")
    lines.append(f"  org_slug:                 {result.org_slug}")
    lines.append(f"  grant_id:                 {result.grant_id}")
    lines.append(f"  records_scanned:          {result.records_scanned}")
    lines.append(f"  records_backfilled:       {result.records_backfilled}")
    lines.append(f"  records_already_applied:  {result.records_already_applied}")
    lines.append(f"  records_skipped (scan):   {result.records_skipped_force_false}")
    lines.append(f"  records_errored:          {result.records_errored}")
    lines.append(f"  audit_log_path:           {result.audit_log_path}")
    lines.append(f"  invoked_at_utc:           {result.invoked_at_utc}")
    lines.append("")
    for r in result.record_results:
        lines.append(f"  - {r.record_id} :: {r.status}")
        lines.append(f"      path:   {r.record_path}")
        lines.append(f"      detail: {r.detail}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_argparser()
    args = parser.parse_args(argv)

    repo_root: Path = args.repo_root.resolve()
    signing_key_bytes = _load_signing_key(args.signing_key_file)
    signer = _build_signer(signing_key_bytes)
    invoked_at_utc = (
        datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z")
    )

    try:
        result = run_beneficiary_records_history_migration(
            repo_root=repo_root,
            org_slug=args.org_slug,
            grant_id=args.grant_id,
            operator_signer=signer,
            operator_key_id=args.operator_key_id,
            invoked_at_utc=invoked_at_utc,
            backfill_empty_history=args.backfill_empty_history,
            force=args.force,
        )
    except MigrationAlreadyApplied as exc:
        if args.json_output:
            sys.stdout.write(
                json.dumps(
                    {
                        "ok": False,
                        "stage": "migrate_record",
                        "code": "MIGRATION_ALREADY_APPLIED",
                        "detail": str(exc),
                    }
                )
                + "\n"
            )
        else:
            print(f"fail-closed: {exc}", file=sys.stderr)
            print(
                "  → use --force to acknowledge re-run no-op",
                file=sys.stderr,
            )
        return 1
    except MigrationScanError as exc:
        if args.json_output:
            sys.stdout.write(
                json.dumps(
                    {
                        "ok": False,
                        "stage": "scan_subtree",
                        "code": "MIGRATION_SCAN_ERROR",
                        "detail": str(exc),
                    }
                )
                + "\n"
            )
        else:
            print(f"scan error: {exc}", file=sys.stderr)
        return 1
    except MigrationError as exc:
        if args.json_output:
            sys.stdout.write(
                json.dumps(
                    {
                        "ok": False,
                        "stage": "migrate_record",
                        "code": "MIGRATION_ERROR",
                        "detail": str(exc),
                    }
                )
                + "\n"
            )
        else:
            print(f"migration error: {exc}", file=sys.stderr)
        return 1

    # Surface — JSON to stdout (machine), human to stderr.
    if args.json_output:
        sys.stdout.write(json.dumps(_summarize_result(result)) + "\n")
    elif not args.quiet:
        print(_render_human(result), file=sys.stderr)

    # Non-zero exit if any records errored — operator should investigate.
    if result.records_errored > 0:
        return 1
    return 0


__all__ = ["main"]


if __name__ == "__main__":  # pragma: no cover — thin entry point
    raise SystemExit(main(sys.argv[1:]))
