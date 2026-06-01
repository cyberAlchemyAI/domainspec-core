"""audit_term_signer.py — operator utility for admin_risk_register migration.

Per Cycle 2 fold-in C2-H-4 of §4 v2.x apolitical_dialect (LOCKED
2026-05-16T14:00:00Z): the migration of admin_risk_register from the
retired ``progressive_register`` field to v7.0.12's ``per_clc_register``
requires a per-term Ed25519 signature pair. This script provides the
operator-facing tool for filling in those signatures.

Workflow
--------
1. Operator generates the empty audit-decisions Markdown table via
   :func:`render_empty_template_to_disk` (or the ``--scaffold`` mode here).
2. Operator opens the file, fills in the ``audit_status`` column for each
   row with one of:
     - ``confirmed_avoid_all`` — AVOID is the right default across all 8 CLCs
       (empty ``per_clc_register`` on the register entry stays empty)
     - ``confirmed_per_clc`` — operator populated the register entry's
       ``per_clc_register`` map with explicit per-CLC values
3. Operator runs this script with their Ed25519 private key path.
4. Script reads each row whose ``audit_status`` is non-PENDING and whose
   signature is still ``<PENDING>``, signs the canonical-bytes shape from
   :func:`canonical_decision_bytes`, writes back the signature_hex +
   pubkey_hex columns. Already-signed rows are left untouched.
5. The F-DIALECT-MIGRATION-INCOMPLETE gate verifies every signature against
   the canonical bytes at LOCK ceremony pre-flight.

Usage::

    python -m pipeline.scripts.audit_term_signer --scaffold
    # ... operator fills audit_status column manually in the file ...
    python -m pipeline.scripts.audit_term_signer \\
        --key path/to/ed25519_operator.key \\
        --decisions pipeline/institutional_memory/admin_risk_register_audit_decisions.md
    # ... LOCK ceremony pre-flight passes ...

Private key file format
-----------------------
The script accepts the raw 32-byte Ed25519 private seed encoded as 64 hex
characters in a single-line file (operator-managed; the script never
prints the seed). A future hardening can swap this for HSM / OS keychain;
the dispatch boundary is the ``--key`` argument shape.

Authority
---------
- §4 v2.x apolitical_dialect §4.X.6 (LOCKED 2026-05-16T14:00:00Z; lock_history rows 236/249)
- Cycle 2 fold-in C2-H-4 (per-term Ed25519 — single-file-signature shortcut closed)
- Cycle 2 fold-in C2-NEW-MED-2 (audit_status closed set)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable, Optional

from pipeline.institutional_memory._audit_decisions import (
    DEFAULT_ADMIN_RISK_REGISTER_PATH,
    DEFAULT_AUDIT_DECISIONS_PATH,
    canonical_decision_bytes,
    compute_term_hash,
    read_admin_risk_register,
    read_audit_decisions,
    render_empty_decisions_template,
)
from pipeline.logician.gates.f_dialect_migration_incomplete import (
    AUDIT_STATUS_CONFIRMED_AVOID_ALL,
    AUDIT_STATUS_CONFIRMED_PER_CLC,
)


PENDING_SENTINELS: frozenset[str] = frozenset(
    {"<PENDING>", "<pending>", "", "null", "None", "-"}
)


def _load_ed25519_signer(key_path: Path):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import (
        Ed25519PrivateKey,
    )

    raw = key_path.read_text(encoding="utf-8").strip()
    try:
        seed = bytes.fromhex(raw)
    except ValueError as exc:
        raise SystemExit(
            f"error: {key_path} is not a hex-encoded Ed25519 seed"
        ) from exc
    if len(seed) != 32:
        raise SystemExit(
            f"error: {key_path} must contain a 32-byte (64-hex-char) "
            f"Ed25519 seed; got {len(seed)} bytes"
        )
    return Ed25519PrivateKey.from_private_bytes(seed)


def _public_key_hex(signer) -> str:
    from cryptography.hazmat.primitives import serialization

    pub_bytes = signer.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return pub_bytes.hex()


def _is_pending(cell: str) -> bool:
    return cell.strip() in PENDING_SENTINELS


def _row_signature_complete(row_cells: list[str]) -> bool:
    """A row is considered already-signed if both signature_hex AND
    pubkey_hex are populated with non-sentinel values."""
    if len(row_cells) < 5:
        return False
    return not _is_pending(row_cells[3]) and not _is_pending(row_cells[4])


def cmd_scaffold(args: argparse.Namespace) -> int:
    """Render an empty audit-decisions template seeded from the current
    admin_risk_register.yaml; write to disk."""
    register_path = Path(args.register or DEFAULT_ADMIN_RISK_REGISTER_PATH)
    decisions_path = Path(args.decisions or DEFAULT_AUDIT_DECISIONS_PATH)
    if decisions_path.exists() and not args.force:
        print(
            f"error: {decisions_path} already exists; pass --force to overwrite",
            file=sys.stderr,
        )
        return 2
    entries = list(read_admin_risk_register(register_path))
    if not entries:
        print(
            f"error: no entries parsed from {register_path}",
            file=sys.stderr,
        )
        return 2
    text = render_empty_decisions_template(entries=entries)
    decisions_path.write_text(text, encoding="utf-8")
    print(
        f"wrote empty audit-decisions template for {len(entries)} terms "
        f"to {decisions_path}",
        file=sys.stderr,
    )
    return 0


def cmd_sign(args: argparse.Namespace) -> int:
    """Sign every non-PENDING, unsigned row in the audit-decisions file."""
    decisions_path = Path(args.decisions or DEFAULT_AUDIT_DECISIONS_PATH)
    register_path = Path(args.register or DEFAULT_ADMIN_RISK_REGISTER_PATH)
    key_path = Path(args.key)
    if not key_path.exists():
        print(f"error: key file {key_path} not found", file=sys.stderr)
        return 2
    if not decisions_path.exists():
        print(
            f"error: decisions file {decisions_path} not found — run with "
            "--scaffold first",
            file=sys.stderr,
        )
        return 2
    signer = _load_ed25519_signer(key_path)
    pubkey_hex = _public_key_hex(signer)

    # Build term → severity index from the register so we can recompute
    # term_hash from authoritative bytes (defends against typos in the
    # decisions file's term_hash column).
    register_entries = list(read_admin_risk_register(register_path))
    severity_by_term: dict[str, str] = {
        e.term: e.severity for e in register_entries
    }

    lines = decisions_path.read_text(encoding="utf-8").splitlines()
    rewritten: list[str] = []
    signed_count = 0
    already_signed_count = 0
    skipped_pending_count = 0
    skipped_unknown_term_count = 0
    for raw_line in lines:
        # Only attempt to parse table rows; pass everything else through.
        if not raw_line.strip().startswith("|"):
            rewritten.append(raw_line)
            continue
        cells = [c.strip() for c in raw_line.strip().strip("|").split("|")]
        if len(cells) < 5:
            rewritten.append(raw_line)
            continue
        term = cells[0]
        if not term or term.lower() == "term" or "---" in cells[0]:
            rewritten.append(raw_line)
            continue
        audit_status = cells[2]
        if audit_status not in {
            AUDIT_STATUS_CONFIRMED_AVOID_ALL,
            AUDIT_STATUS_CONFIRMED_PER_CLC,
        }:
            skipped_pending_count += 1
            rewritten.append(raw_line)
            continue
        if _row_signature_complete(cells):
            already_signed_count += 1
            rewritten.append(raw_line)
            continue
        severity = severity_by_term.get(term)
        if severity is None:
            skipped_unknown_term_count += 1
            rewritten.append(raw_line)
            continue
        # Recompute term_hash + sign.
        term_hash = compute_term_hash(term, severity)
        cb = canonical_decision_bytes(
            term=term, term_hash=term_hash, audit_status=audit_status
        )
        sig_hex = signer.sign(cb).hex()
        rewritten_cells = [
            term,
            term_hash,
            audit_status,
            sig_hex,
            pubkey_hex,
        ]
        rewritten.append("| " + " | ".join(rewritten_cells) + " |")
        signed_count += 1

    if signed_count > 0:
        decisions_path.write_text(
            "\n".join(rewritten) + "\n", encoding="utf-8"
        )
    print(
        f"signed={signed_count} already_signed={already_signed_count} "
        f"pending_audit_status={skipped_pending_count} "
        f"unknown_term={skipped_unknown_term_count}",
        file=sys.stderr,
    )
    if skipped_unknown_term_count > 0:
        print(
            "warning: rows skipped because the term was not found in "
            "admin_risk_register.yaml — check for typos",
            file=sys.stderr,
        )
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    """Verify every signed row against canonical bytes.

    Doesn't talk to the gate — straight verification of the file's own
    signatures, as a self-check before LOCK ceremony.
    """
    from pipeline.institutional_memory._audit_decisions import (
        make_signature_verifier,
    )

    decisions_path = Path(args.decisions or DEFAULT_AUDIT_DECISIONS_PATH)
    if not decisions_path.exists():
        print(f"error: {decisions_path} not found", file=sys.stderr)
        return 2
    verify = make_signature_verifier()
    ok = 0
    bad = 0
    skipped = 0
    for row in read_audit_decisions(decisions_path):
        if (
            row.operator_ed25519_signature_hex is None
            or row.operator_pubkey_ed25519_hex is None
        ):
            skipped += 1
            continue
        passed = verify(
            term=row.term,
            term_hash=row.term_hash,
            audit_status=row.audit_status,
            signature_hex=row.operator_ed25519_signature_hex,
            pubkey_hex=row.operator_pubkey_ed25519_hex,
        )
        if passed:
            ok += 1
        else:
            bad += 1
            print(
                f"INVALID SIGNATURE for term={row.term!r} "
                f"audit_status={row.audit_status!r}",
                file=sys.stderr,
            )
    print(
        f"signatures_ok={ok} signatures_bad={bad} skipped_unsigned={skipped}",
        file=sys.stderr,
    )
    return 0 if bad == 0 else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="audit_term_signer",
        description=(
            "Per-term Ed25519 signer for admin_risk_register migration "
            "audit decisions. Per §4 v2.x apolitical_dialect §4.X.6 + "
            "Cycle 2 fold-in C2-H-4."
        ),
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    scaffold = sub.add_parser(
        "scaffold",
        help="Render an empty audit-decisions Markdown table from admin_risk_register.yaml",
    )
    scaffold.add_argument("--register", help="Path to admin_risk_register.yaml")
    scaffold.add_argument(
        "--decisions",
        help="Output path (default: admin_risk_register_audit_decisions.md)",
    )
    scaffold.add_argument(
        "--force", action="store_true", help="Overwrite existing file"
    )
    scaffold.set_defaults(func=cmd_scaffold)

    sign = sub.add_parser(
        "sign",
        help="Sign every non-PENDING, unsigned row in the audit-decisions file",
    )
    sign.add_argument(
        "--key", required=True, help="Path to Ed25519 private seed (hex)"
    )
    sign.add_argument("--register", help="Path to admin_risk_register.yaml")
    sign.add_argument("--decisions", help="Path to audit-decisions Markdown")
    sign.set_defaults(func=cmd_sign)

    verify = sub.add_parser(
        "verify",
        help="Verify every signed row against canonical bytes (self-check)",
    )
    verify.add_argument("--decisions", help="Path to audit-decisions Markdown")
    verify.set_defaults(func=cmd_verify)

    return p


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover - thin wrapper
    raise SystemExit(main())
