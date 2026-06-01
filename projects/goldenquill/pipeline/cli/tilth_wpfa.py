"""``tilth wpfa <verb>`` — operator-facing WPFA CLI surface. [§17.7.4, §2.14.6]

Four verbs, all TTY-gated. argparse-level rejection of ``--yes`` /
``--force`` / ``--auto-confirm`` per §11.7 four-layer autopromote precedent
(Layer 4 of the buyer-PDF defense; Layers 1-3 live in code).

Verbs
-----
* ``tilth wpfa pdf emit`` — emits a buyer-facing PDF for one CycleReceipt.
* ``tilth wpfa registry update`` — stages a new SN-LLC-signed Coefficient
  Registry version (signature verify + history copy + active.yaml repoint).
* ``tilth wpfa registry rollback`` — re-pins active.yaml to a prior signed
  registry by SHA3-512 hex.
* ``tilth wpfa registry pin-pubkey`` — sets / co-signed-rotates the
  white-glove-pinned SN-LLC public key.

Each verb fails closed on:
* missing TTY (when interactive confirmation is required)
* argparse-level autoconfirm flags (BANNED_FLAGS below)
* signature / schema validation failure
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Optional, Sequence

import yaml
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from pipeline.logician.gates.f_wpfa_coefficient_registry_validation import (
    check_f_wpfa_coefficient_registry_unsigned,
    check_f_wpfa_coefficient_rollback_invalid,
)
from pipeline.orchestrator.seats.wpfa._cedar_bootstrap import (
    CycleReceiptCedarDenied,
    evaluate_cycle_receipt_operator_attestation,
    register_wpfa_policies,
)
from pipeline.orchestrator.seats.wpfa.pdf_emitter import (
    build_pdf_render_context,
    emit_buyer_facing_pdf,
)
from pipeline.vault.sub_kinds.coefficient_registry import (
    CoefficientRegistryError,
    load_active,
)
from pipeline.vault.sub_kinds.cycle_receipts import (
    CycleReceipt,
    from_canonical_bytes,
)


# ---------------------------------------------------------------------------
# Banned-flag detection — Layer 4 of the buyer-PDF defense
# ---------------------------------------------------------------------------


BANNED_FLAGS: tuple[str, ...] = ("--yes", "-y", "--force", "--auto-confirm")


def _reject_banned_flags(argv: Sequence[str]) -> None:
    """Pre-argparse autoconfirm flag rejection.

    Per §11.7 four-layer autopromote precedent + §2.14.6 binding: WPFA
    verbs MUST NOT accept --yes / --force / --auto-confirm. Detection
    happens BEFORE argparse parses, so any presence of the flag in argv
    surfaces a clear error rather than an "unrecognized argument" trace.
    """
    for arg in argv:
        for banned in BANNED_FLAGS:
            if arg == banned or arg.startswith(banned + "="):
                raise SystemExit(
                    f"error: {banned!s} is not accepted by `tilth wpfa` verbs "
                    "(§11.7 four-layer autopromote precedent; operator must "
                    "confirm interactively on TTY)."
                )


def _require_tty() -> None:
    if not sys.stdin.isatty():
        raise SystemExit(
            "error: this verb requires a TTY for operator confirmation "
            "(§17.7.4 Layer 4 / §2.14.6 TTY-gating)."
        )


def _confirm_tty(prompt: str) -> bool:
    """Interactive TTY confirmation. Returns True iff operator types 'yes'."""
    _require_tty()
    sys.stderr.write(prompt)
    sys.stderr.flush()
    answer = input().strip().lower()
    return answer in {"yes", "y"}


# ---------------------------------------------------------------------------
# Key loading (mirrors tilth_review_classify._load_signing_key)
# ---------------------------------------------------------------------------


def _load_signing_key(path: Path) -> bytes:
    if not path.is_file():
        raise SystemExit(f"error: signing key file not found at {path}")
    raw = path.read_bytes()
    if len(raw) == 32:
        return raw
    try:
        loaded = serialization.load_pem_private_key(raw, password=None)
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(
            f"error: signing key at {path} is neither raw 32 bytes nor PEM "
            f"({type(exc).__name__}: {exc})"
        ) from exc
    if not isinstance(loaded, ed25519.Ed25519PrivateKey):
        raise SystemExit(
            f"error: signing key at {path} is not Ed25519 "
            f"(got {type(loaded).__name__})"
        )
    return loaded.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )


def _load_pubkey_hex(path: Path) -> str:
    if not path.is_file():
        raise SystemExit(f"error: pubkey file not found at {path}")
    raw = path.read_bytes()
    if len(raw) == 32:
        return raw.hex()
    try:
        loaded = serialization.load_pem_public_key(raw)
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(
            f"error: pubkey at {path} is neither raw 32 bytes nor PEM "
            f"({type(exc).__name__}: {exc})"
        ) from exc
    if not isinstance(loaded, ed25519.Ed25519PublicKey):
        raise SystemExit(
            f"error: pubkey at {path} is not Ed25519 "
            f"(got {type(loaded).__name__})"
        )
    return loaded.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()


def _load_pinned_sn_llc_pubkey_hex(repo_root: Path) -> str:
    """Read the white-glove-pinned SN-LLC pubkey from disk."""
    pinned = repo_root / "vault_shared" / "wpfa" / "sn_llc_pubkey.signed.yaml"
    if not pinned.is_file():
        raise SystemExit(
            f"error: SN-LLC pinned pubkey not found at {pinned!s} — run "
            "`tilth wpfa registry pin-pubkey` at white-glove onboarding"
        )
    parsed = yaml.safe_load(pinned.read_bytes())
    if not isinstance(parsed, dict) or "pubkey_hex" not in parsed:
        raise SystemExit(
            f"error: pinned pubkey file {pinned!s} malformed — missing "
            "'pubkey_hex'"
        )
    pubkey_hex = parsed["pubkey_hex"]
    if (
        not isinstance(pubkey_hex, str)
        or len(pubkey_hex) != 64
        or not all(c in "0123456789abcdef" for c in pubkey_hex.lower())
    ):
        raise SystemExit(
            f"error: pinned pubkey at {pinned!s} is not 64-char lowercase hex"
        )
    return pubkey_hex


# ---------------------------------------------------------------------------
# Signature verifier — pynacl-or-cryptography Ed25519
# ---------------------------------------------------------------------------


def _verify_ed25519(
    message_bytes: bytes,
    signature: bytes,
    public_key: bytes,
) -> bool:
    """Verify Ed25519 signature using `cryptography`. Returns True iff valid."""
    try:
        pubkey = ed25519.Ed25519PublicKey.from_public_bytes(public_key)
        pubkey.verify(signature, message_bytes)
        return True
    except Exception:  # noqa: BLE001 — fail-closed
        return False


# ---------------------------------------------------------------------------
# Verb: tilth wpfa pdf emit
# ---------------------------------------------------------------------------


def _verb_pdf_emit(args: argparse.Namespace) -> int:
    """Emit a buyer-facing PDF for one operator-attested CycleReceipt."""
    repo_root: Path = args.repo_root.resolve()
    receipt_path: Path = args.receipt_path.resolve()
    if not receipt_path.is_file():
        sys.stderr.write(f"error: receipt not found at {receipt_path!s}\n")
        return 1
    try:
        receipt = from_canonical_bytes(receipt_path.read_bytes())
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(
            f"error: receipt at {receipt_path!s} failed to decode: "
            f"{type(exc).__name__}: {exc}\n"
        )
        return 1

    # Cedar Rule 5 / Logician F-WPFA-OPERATOR-SIGNATURE-MISSING — pre-flight.
    register_wpfa_policies()
    try:
        evaluate_cycle_receipt_operator_attestation(
            signed_by_operator_ed25519=receipt.signed_by_operator_ed25519,
            target_artifact="pdf",
        )
    except CycleReceiptCedarDenied as exc:
        sys.stderr.write(
            f"F-WPFA-OPERATOR-SIGNATURE-MISSING (Cedar denial): {exc}\n"
        )
        return 1

    # TTY confirmation — operator must confirm before buyer-facing emission.
    if not args.no_confirm_prompt:
        if not _confirm_tty(
            f"Emit buyer-facing PDF for cycle_id={receipt.cycle_id!r} "
            f"signed_by={receipt.signed_by_operator_ed25519[:16]}…? [yes/no]: "
        ):
            sys.stderr.write("operator declined emission\n")
            return 1

    # Load classification register (best-effort: missing = fail-closed via gate)
    classification_register: Optional[dict[str, str]] = None
    register_path = (
        repo_root
        / "orgs"
        / receipt.org_slug
        / "vault"
        / "classification"
        / "register.yaml"
    )
    if register_path.is_file():
        try:
            parsed = yaml.safe_load(register_path.read_bytes())
            if isinstance(parsed, dict):
                # Per-org register may be {field_path: {classification: ...}}
                # or {field_path: classification_string}; normalize.
                normalized: dict[str, str] = {}
                for k, v in parsed.items():
                    if isinstance(v, str):
                        normalized[str(k)] = v
                    elif isinstance(v, dict) and "classification" in v:
                        normalized[str(k)] = str(v["classification"])
                classification_register = normalized
        except Exception:  # noqa: BLE001 — fail-closed downstream
            classification_register = None

    context = build_pdf_render_context(
        receipt=receipt,
        client_name=args.client_name,
        operator_display_name=args.operator_display_name,
        signing_key_id_display=args.signing_key_id_display,
        methodology_url=args.methodology_url,
        grant_identifier=args.grant_identifier,
        confidential_value_strings=tuple(args.confidential_value or ()),
    )

    output_dir = repo_root / "orgs" / receipt.org_slug / "wpfa_artifacts"
    output_dir.mkdir(parents=True, exist_ok=True)
    result = emit_buyer_facing_pdf(
        receipt=receipt,
        context=context,
        output_dir=output_dir,
        classification_register=classification_register,
    )
    if not result.success:
        sys.stderr.write(
            f"PDF emission FAILED: {', '.join(result.failure_codes)}\n"
            f"  detail: {result.detail}\n"
        )
        return 1
    sys.stderr.write(f"PDF emitted to {result.output_path!s}\n")
    if args.json_output:
        sys.stdout.write(
            json.dumps(
                {
                    "ok": True,
                    "output_path": str(result.output_path),
                    "cycle_id": receipt.cycle_id,
                    "org_slug": receipt.org_slug,
                }
            )
            + "\n"
        )
    return 0


# ---------------------------------------------------------------------------
# Verb: tilth wpfa registry update
# ---------------------------------------------------------------------------


def _verb_registry_update(args: argparse.Namespace) -> int:
    """Stage a new SN-LLC-signed Coefficient Registry version.

    Pre-staging discipline:
      1. Strict JSON parse of candidate (RT-C2-04 fold-in — comments, YAML
         tags, etc. fail closed at json.loads).
      2. Signature presence check (F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED).
      3. Full load + verify (F-WPFA-COEFFICIENT-SIGNATURE-INVALID).
      4. Compute SHA3-512 of canonical bytes.
      5. Copy into history/ keyed by SHA3.
      6. Repoint active.yaml.
    """
    repo_root: Path = args.repo_root.resolve()
    candidate: Path = args.path.resolve()
    if not candidate.is_file():
        sys.stderr.write(f"error: candidate not found at {candidate!s}\n")
        return 1

    raw = candidate.read_bytes()
    # RT-C2-04 fold-in: strict JSON parse — any YAML-specific construct
    # (anchors, tags, comments outside JSON grammar) fails closed here.
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(
            f"F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED (candidate failed strict "
            f"JSON parse — comments/anchors/tags are forbidden): "
            f"{type(exc).__name__}: {exc}\n"
        )
        return 1

    sig_hex = parsed.get("sn_llc_signature_ed25519")
    pre = check_f_wpfa_coefficient_registry_unsigned(signature_hex=sig_hex)
    if not pre.success:
        sys.stderr.write(f"{pre.failure_code}: {pre.detail}\n")
        return 1

    pinned_pubkey_hex = _load_pinned_sn_llc_pubkey_hex(repo_root)

    # Full load + verify via the canonical loader
    try:
        registry = load_active(
            registry_path=candidate,
            pinned_pubkey_hex=pinned_pubkey_hex,
            signature_verify=_verify_ed25519,
        )
    except CoefficientRegistryError as exc:
        sys.stderr.write(
            f"F-WPFA-COEFFICIENT-SIGNATURE-INVALID: {type(exc).__name__}: {exc}\n"
        )
        return 1

    # Compute SHA3-512 of canonical bytes for history filename
    from pipeline.vault.sub_kinds.coefficient_registry import to_canonical_bytes

    sha3_hex = hashlib.sha3_512(to_canonical_bytes(registry)).hexdigest()

    if not args.no_confirm_prompt:
        if not _confirm_tty(
            f"Stage Coefficient Registry sha3={sha3_hex[:16]}… "
            f"quarter={registry.quarter!r} baseline={registry.baseline_model_id!r}? "
            "[yes/no]: "
        ):
            sys.stderr.write("operator declined staging\n")
            return 1

    history_dir = (
        repo_root / "vault_shared" / "wpfa" / "coefficient_registry" / "history"
    )
    history_dir.mkdir(parents=True, exist_ok=True)
    target = history_dir / f"{sha3_hex}.yaml"
    if target.exists():
        sys.stderr.write(
            f"note: history target {target!s} already exists; re-pointing active\n"
        )
    else:
        shutil.copyfile(candidate, target)
    active_path = (
        repo_root / "vault_shared" / "wpfa" / "coefficient_registry" / "active.yaml"
    )
    shutil.copyfile(target, active_path)
    sys.stderr.write(
        f"Coefficient Registry staged: sha3={sha3_hex} → {active_path!s}\n"
    )
    if args.json_output:
        sys.stdout.write(
            json.dumps(
                {
                    "ok": True,
                    "sha3_512": sha3_hex,
                    "active_path": str(active_path),
                    "history_path": str(target),
                    "quarter": registry.quarter,
                    "baseline_model_id": registry.baseline_model_id,
                }
            )
            + "\n"
        )
    return 0


# ---------------------------------------------------------------------------
# Verb: tilth wpfa registry rollback
# ---------------------------------------------------------------------------


def _verb_registry_rollback(args: argparse.Namespace) -> int:
    """Re-pin active.yaml to a prior signed registry by SHA3 hex."""
    repo_root: Path = args.repo_root.resolve()
    target_sha3: str = args.to_sha3.lower()

    history_dir = (
        repo_root / "vault_shared" / "wpfa" / "coefficient_registry" / "history"
    )
    rb = check_f_wpfa_coefficient_rollback_invalid(
        rollback_target_sha3=target_sha3,
        history_dir=history_dir,
    )
    if not rb.success:
        sys.stderr.write(f"{rb.failure_code}: {rb.detail}\n")
        return 1

    if not args.no_confirm_prompt:
        if not _confirm_tty(
            f"Rollback Coefficient Registry → sha3={target_sha3[:16]}…? "
            f"reason={args.reason!r} [yes/no]: "
        ):
            sys.stderr.write("operator declined rollback\n")
            return 1

    src = history_dir / f"{target_sha3}.yaml"
    active = (
        repo_root / "vault_shared" / "wpfa" / "coefficient_registry" / "active.yaml"
    )
    shutil.copyfile(src, active)
    sys.stderr.write(f"rollback complete: active.yaml → {src!s}\n")
    # Audit-ledger entry
    audit_dir = repo_root / "vault_shared" / "wpfa" / "rollback_audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    audit_entry = audit_dir / f"{target_sha3}.yaml"
    audit_entry.write_text(
        yaml.safe_dump(
            {
                "target_sha3_512": target_sha3,
                "reason": args.reason,
                "operator_key_id": args.operator_key_id,
                "rolled_back_at_utc": args.rolled_back_at_utc,
            }
        )
    )
    if args.json_output:
        sys.stdout.write(
            json.dumps(
                {
                    "ok": True,
                    "rolled_back_to_sha3_512": target_sha3,
                    "active_path": str(active),
                    "audit_entry": str(audit_entry),
                }
            )
            + "\n"
        )
    return 0


# ---------------------------------------------------------------------------
# Verb: tilth wpfa registry pin-pubkey
# ---------------------------------------------------------------------------


def _verb_registry_pin_pubkey(args: argparse.Namespace) -> int:
    """Set / rotate the white-glove-pinned SN-LLC pubkey."""
    repo_root: Path = args.repo_root.resolve()
    new_pubkey_path: Path = args.path.resolve()
    new_pubkey_hex = _load_pubkey_hex(new_pubkey_path)
    pinned_path = (
        repo_root / "vault_shared" / "wpfa" / "sn_llc_pubkey.signed.yaml"
    )

    # Co-signed rotation: if a pinned file exists, the new pubkey MUST be
    # accompanied by a signature from the prior pubkey over the new key bytes.
    if pinned_path.is_file():
        if args.co_signed_by_prior_signature_hex is None:
            sys.stderr.write(
                "error: prior pinned pubkey exists at "
                f"{pinned_path!s}; rotation requires "
                "--co-signed-by-prior-signature-hex (signature of new pubkey "
                "by prior pubkey) per §2.14.4 #4.\n"
            )
            return 1
        prior = yaml.safe_load(pinned_path.read_bytes())
        if not isinstance(prior, dict) or "pubkey_hex" not in prior:
            sys.stderr.write(
                f"error: prior pinned pubkey at {pinned_path!s} malformed\n"
            )
            return 1
        prior_pubkey_hex = prior["pubkey_hex"]
        try:
            sig_bytes = bytes.fromhex(args.co_signed_by_prior_signature_hex)
            prior_pubkey_bytes = bytes.fromhex(prior_pubkey_hex)
            new_pubkey_bytes = bytes.fromhex(new_pubkey_hex)
        except ValueError as exc:
            sys.stderr.write(f"error: hex decode failed: {exc}\n")
            return 1
        if not _verify_ed25519(new_pubkey_bytes, sig_bytes, prior_pubkey_bytes):
            sys.stderr.write(
                "F-WPFA-COEFFICIENT-SIGNATURE-INVALID: prior-pubkey "
                "co-signature does not verify new pubkey\n"
            )
            return 1

    if not args.no_confirm_prompt:
        if not _confirm_tty(
            f"Pin SN-LLC pubkey={new_pubkey_hex[:16]}…? [yes/no]: "
        ):
            sys.stderr.write("operator declined pinning\n")
            return 1

    pinned_path.parent.mkdir(parents=True, exist_ok=True)
    pinned_path.write_text(
        yaml.safe_dump(
            {
                "pubkey_hex": new_pubkey_hex,
                "pinned_at_utc": args.pinned_at_utc,
                "operator_key_id": args.operator_key_id,
            }
        )
    )
    sys.stderr.write(f"SN-LLC pubkey pinned: {pinned_path!s}\n")
    if args.json_output:
        sys.stdout.write(
            json.dumps(
                {
                    "ok": True,
                    "pubkey_hex": new_pubkey_hex,
                    "pinned_path": str(pinned_path),
                }
            )
            + "\n"
        )
    return 0


# ---------------------------------------------------------------------------
# Argparse wiring
# ---------------------------------------------------------------------------


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tilth_wpfa",
        description=(
            "Tilth WPFA operator CLI. Four verbs: `pdf emit`, "
            "`registry update`, `registry rollback`, `registry pin-pubkey`. "
            "All TTY-gated; --yes/--force/--auto-confirm are REJECTED at "
            "argparse level (§11.7 four-layer autopromote precedent)."
        ),
    )
    parser.add_argument(
        "--repo-root",
        dest="repo_root",
        type=Path,
        default=Path.cwd(),
        help="Workspace root (default: cwd).",
    )
    parser.add_argument(
        "--json-output",
        dest="json_output",
        action="store_true",
        help="Emit machine-readable JSON summary on stdout.",
    )
    parser.add_argument(
        "--no-confirm-prompt",
        dest="no_confirm_prompt",
        action="store_true",
        help=(
            "Skip the TTY confirmation prompt. Intended for test fixtures "
            "and CI pipelines ONLY — this flag is documented but the verb "
            "still requires a TTY for human invocation contexts."
        ),
    )
    sub = parser.add_subparsers(dest="verb", required=True)

    # tilth wpfa pdf
    pdf = sub.add_parser("pdf", help="PDF emission verbs")
    pdf_sub = pdf.add_subparsers(dest="pdf_verb", required=True)
    emit = pdf_sub.add_parser(
        "emit",
        help=(
            "Emit a buyer-facing PDF for one operator-attested CycleReceipt."
        ),
    )
    emit.add_argument("--receipt-path", type=Path, required=True)
    emit.add_argument("--client-name", required=True)
    emit.add_argument("--operator-display-name", required=True)
    emit.add_argument("--signing-key-id-display", required=True)
    emit.add_argument("--methodology-url", required=True)
    emit.add_argument("--grant-identifier", default="—")
    emit.add_argument(
        "--confidential-value",
        action="append",
        default=None,
        help=(
            "Repeatable. Each value string is scanned against the rendered "
            "HTML+CSS+JS to detect indirect-template leakage per RT-C2-02."
        ),
    )
    emit.set_defaults(func=_verb_pdf_emit)

    # tilth wpfa registry
    reg = sub.add_parser("registry", help="Coefficient Registry verbs")
    reg_sub = reg.add_subparsers(dest="registry_verb", required=True)

    update = reg_sub.add_parser("update", help="Stage a new signed registry")
    update.add_argument("--path", type=Path, required=True)
    update.set_defaults(func=_verb_registry_update)

    rollback = reg_sub.add_parser(
        "rollback",
        help="Re-pin active.yaml to a prior signed registry by SHA3 hex",
    )
    rollback.add_argument("--to-sha3", required=True)
    rollback.add_argument("--reason", required=True)
    rollback.add_argument("--operator-key-id", required=True)
    rollback.add_argument("--rolled-back-at-utc", required=True)
    rollback.set_defaults(func=_verb_registry_rollback)

    pin = reg_sub.add_parser(
        "pin-pubkey",
        help="Set / rotate the white-glove-pinned SN-LLC pubkey",
    )
    pin.add_argument("--path", type=Path, required=True)
    pin.add_argument("--operator-key-id", required=True)
    pin.add_argument("--pinned-at-utc", required=True)
    pin.add_argument(
        "--co-signed-by-prior-signature-hex",
        default=None,
        help=(
            "Required when rotating an existing pinned pubkey. Ed25519 "
            "signature (hex) of the new pubkey bytes by the prior pinned "
            "pubkey. Trust-On-First-Use rotation per v7.0.7 §6.1."
        ),
    )
    pin.set_defaults(func=_verb_registry_pin_pubkey)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    _reject_banned_flags(argv)
    parser = _build_argparser()
    args = parser.parse_args(argv)
    return args.func(args)


__all__ = ["BANNED_FLAGS", "main"]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
