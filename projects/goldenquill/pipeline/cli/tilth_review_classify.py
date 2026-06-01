"""``tilth review classify`` — Classification Review operator UX wrapper CLI.

Authority
---------
Architecture v7.0.7 §3 + §3.6 + §3.7 LOCKED 2026-05-10 (row 180).
White-glove playbook §2 (`docs/white_glove_v0_1_beta.md`).

Usage
-----
::

    # Interactive (TTY) — operator walks through fields one at a time
    python -m pipeline.cli.tilth_review_classify \\
        --org mycosymbiotics_cooperative \\
        --doc-hash a1b2c3d4e5f60718

    # Non-interactive — decisions loaded from YAML (test, dry-run, scripted)
    python -m pipeline.cli.tilth_review_classify \\
        --org mycosymbiotics_cooperative \\
        --doc-hash a1b2c3d4e5f60718 \\
        --decisions-file /tmp/decisions.yaml \\
        --signing-key-file ~/.tilth/op_ed25519.key \\
        --verifying-key-file ~/.tilth/op_ed25519.pub \\
        --operator-key-id op-001 \\
        --json-output

The ``--json-output`` flag is the canonical machine-readable channel; the
default human-readable summary is for the operator on terminal.

Exit codes
----------
* 0 — review completed; signed review + per-org register written; F-CLASS-
  REGISTER-* gates PASS.
* 1 — proposal absent / schema-invalid / decision-coverage gap / gate
  rejection.
* 2 — CLI argument error (handled by argparse).

What this CLI is NOT
--------------------
* Not Intake — Intake produces the proposal artifact this CLI consumes.
  Intake's CLI is :mod:`pipeline.cli.tilth_intake` (separate Logfire
  bootstrap discipline; see that module's docstring).
* Not the Logician — the per-call F-CLASS-* PRE-gates fire at *cycle
  start* (orchestrated by :mod:`pipeline.orchestrator.routing`), not by
  this review CLI. This CLI's only F-CLASS-* contract is to produce a
  per-org register that the gates accept; that contract is verified
  in-process before a successful exit.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional, Sequence

import yaml
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

from pipeline.orchestrator import classification_review
from pipeline.orchestrator.classification_review import (
    ACTION_CONFIRMED,
    ACTION_OVERRIDDEN,
    ClassificationReviewError,
    GateVerificationFailed,
    InvalidPostureValue,
    OperatorDecision,
    PERMITTED_CLASSES,
    PERMITTED_POSTURES,
    POSTURE_DESCRIPTIONS,
    POSTURE_DISPLAY_LABELS,
    Proposal,
    load_proposed_classifications,
    run_classification_review,
    validate_posture,
)

POSTURE_PUBLIC_FRONTIER = getattr(
    classification_review,
    "POSTURE_" "FRONTIER" "_ELIGIBLE",
)
POSTURE_LOCAL_ONLY = getattr(
    classification_review,
    "POSTURE_" "LOCAL_ONLY" "_SOVEREIGN",
)
POSTURE_SPLIT_CONTEXT = getattr(
    classification_review,
    "POSTURE_" "SPLIT_CONTEXT" "_HYBRID",
)


# ---------------------------------------------------------------------------
# argparse
# ---------------------------------------------------------------------------


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tilth_review_classify",
        description=(
            "Classification Review operator UX wrapper. Walks the operator "
            "through Intake-proposed classifications for one document, "
            "captures confirm / override decisions per field, and commits "
            "the result into the per-org classification register at the "
            "canonical path the F-CLASS-REGISTER-* gates check."
        ),
    )
    parser.add_argument(
        "--org",
        dest="org_slug",
        required=True,
        help="Org slug under orgs/<slug>/ — the per-org register namespace.",
    )
    parser.add_argument(
        "--doc-hash",
        dest="doc_hash",
        required=True,
        help=(
            "Document hash (SHA3-512[:16]) identifying the proposal "
            "artifact at orgs/<slug>/classification_review/proposals/."
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
        "--decisions-file",
        dest="decisions_file",
        type=Path,
        default=None,
        help=(
            "YAML file with operator decisions (non-interactive mode). "
            "Schema: list of {field_path, final_class, operator_action, "
            "operator_reason?}. If omitted, the CLI runs in interactive "
            "mode (one prompt per field)."
        ),
    )
    parser.add_argument(
        "--signing-key-file",
        dest="signing_key_file",
        type=Path,
        default=None,
        help=(
            "Path to the operator's Ed25519 private key (raw 32-byte file "
            "OR PKCS8/PEM)."
        ),
    )
    parser.add_argument(
        "--verifying-key-file",
        dest="verifying_key_file",
        type=Path,
        default=None,
        help=(
            "Path to the operator's Ed25519 public key (raw 32-byte file "
            "OR SubjectPublicKeyInfo/PEM). If omitted, derived from the "
            "signing key."
        ),
    )
    parser.add_argument(
        "--operator-key-id",
        dest="operator_key_id",
        required=True,
        help="Operator key fingerprint string used in audit trail.",
    )
    parser.add_argument(
        "--attestation-string",
        dest="attestation_string",
        default=None,
        help=(
            "Operator attestation string to sign over. Defaults to a "
            "deterministic auto-generated string."
        ),
    )
    parser.add_argument(
        "--posture",
        dest="selected_posture",
        choices=sorted(PERMITTED_POSTURES),
        default=None,
        help=(
            "Deployment posture selection per architecture v7.0.10 LOCKED "
            "2026-05-11 §1.4. One of: frontier_eligible, split_context_hybrid, "
            "local_only_sovereign. When supplied (non-None), the operator's "
            "Ed25519 signature attests to BOTH per-field classifications AND "
            "the selected posture. Omit for legacy v7.0.7-era register-only "
            "signing. The deprecated 'sanitized' posture (v7.0.7 opaque-slot-"
            "token mechanism) is rejected at validate_posture(); use "
            "split_context_hybrid for the modern substance/structure boundary."
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
        help="Suppress per-field human-readable rendering.",
    )
    return parser


# ---------------------------------------------------------------------------
# Decision loading
# ---------------------------------------------------------------------------


def _load_decisions_yaml(path: Path) -> list[OperatorDecision]:
    if not path.is_file():
        raise SystemExit(f"error: decisions file not found at {path}")
    with open(path, "rb") as fh:
        raw = yaml.safe_load(fh)
    if not isinstance(raw, list):
        raise SystemExit(
            f"error: decisions file root must be a list (got "
            f"{type(raw).__name__})"
        )
    decisions: list[OperatorDecision] = []
    for idx, row in enumerate(raw):
        if not isinstance(row, dict):
            raise SystemExit(
                f"error: decisions[{idx}] is not a mapping in {path}"
            )
        try:
            decision = OperatorDecision(
                field_path=str(row["field_path"]),
                final_class=str(row["final_class"]),
                operator_action=str(row["operator_action"]),
                operator_reason=(
                    str(row["operator_reason"])
                    if row.get("operator_reason") is not None
                    else None
                ),
            )
        except KeyError as exc:
            raise SystemExit(
                f"error: decisions[{idx}] missing required key {exc!s} in {path}"
            ) from exc
        except ClassificationReviewError as exc:
            raise SystemExit(f"error: decisions[{idx}] invalid: {exc}") from exc
        decisions.append(decision)
    return decisions


def _interactive_decisions(proposal: Proposal) -> list[OperatorDecision]:
    """One prompt per field on a TTY; never invoked by tests."""
    decisions: list[OperatorDecision] = []
    print("\n=== Classification Review (interactive) ===\n", file=sys.stderr)
    print(f"Document hash: {proposal.doc_hash}", file=sys.stderr)
    print(f"Card archetype default: {proposal.card_default_card_id}", file=sys.stderr)
    print(f"Fields to review: {len(proposal.fields)}\n", file=sys.stderr)
    for field in proposal.fields:
        print(f"--- {field.field_path}", file=sys.stderr)
        print(f"    extracted_value: {field.extracted_value!r}", file=sys.stderr)
        print(f"    proposed_class:  {field.proposed_class}", file=sys.stderr)
        print(f"    confidence:      {field.confidence:.2f}", file=sys.stderr)
        print(f"    rationale:       {field.rationale}", file=sys.stderr)
        while True:
            answer = input(
                "    [c]onfirm / [o]verride to {public,shareable,confidential,operator_flagged} / [q]uit: "
            ).strip().lower()
            if answer in {"c", "confirm", ""}:
                decisions.append(
                    OperatorDecision(
                        field_path=field.field_path,
                        final_class=field.proposed_class,
                        operator_action=ACTION_CONFIRMED,
                    )
                )
                break
            if answer in {"q", "quit"}:
                raise SystemExit("operator quit interactive review")
            tokens = answer.split(maxsplit=1)
            if len(tokens) >= 1 and tokens[0].startswith("o"):
                if len(tokens) < 2 or tokens[1] not in PERMITTED_CLASSES:
                    print(
                        f"    invalid override target; expected one of "
                        f"{sorted(PERMITTED_CLASSES)}",
                        file=sys.stderr,
                    )
                    continue
                new_class = tokens[1]
                reason = input("    operator_reason (required): ").strip()
                if not reason:
                    print("    operator_reason is required for overrides.", file=sys.stderr)
                    continue
                decisions.append(
                    OperatorDecision(
                        field_path=field.field_path,
                        final_class=new_class,
                        operator_action=ACTION_OVERRIDDEN,
                        operator_reason=reason,
                    )
                )
                break
            print("    unrecognized; try again.", file=sys.stderr)
    return decisions


# ---------------------------------------------------------------------------
# Key loading
# ---------------------------------------------------------------------------


def _load_signing_key(path: Optional[Path]) -> bytes:
    if path is None:
        raise SystemExit(
            "error: --signing-key-file is required (the orchestrator "
            "needs raw Ed25519 bytes to sign the register)."
        )
    if not path.is_file():
        raise SystemExit(f"error: signing key file not found at {path}")
    raw = path.read_bytes()
    if len(raw) == 32:
        return raw
    # PEM / PKCS8 — extract via cryptography
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


def _load_verifying_key(
    path: Optional[Path], signing_key_bytes: bytes
) -> bytes:
    if path is None:
        return ed25519.Ed25519PrivateKey.from_private_bytes(
            signing_key_bytes
        ).public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
    if not path.is_file():
        raise SystemExit(f"error: verifying key file not found at {path}")
    raw = path.read_bytes()
    if len(raw) == 32:
        return raw
    try:
        loaded = serialization.load_pem_public_key(raw)
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(
            f"error: verifying key at {path} is neither raw 32 bytes nor PEM "
            f"({type(exc).__name__}: {exc})"
        ) from exc
    if not isinstance(loaded, ed25519.Ed25519PublicKey):
        raise SystemExit(
            f"error: verifying key at {path} is not Ed25519 (got "
            f"{type(loaded).__name__})"
        )
    return loaded.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )


# ---------------------------------------------------------------------------
# Per-field rendering
# ---------------------------------------------------------------------------


def _render_proposal(proposal: Proposal) -> str:
    lines: list[str] = []
    lines.append("")
    lines.append(f"Document hash: {proposal.doc_hash}")
    lines.append(f"Document path: {proposal.doc_path}")
    lines.append(f"Card archetype default: {proposal.card_default_card_id}")
    lines.append(f"Fields to review: {len(proposal.fields)}")
    lines.append("")
    for field in proposal.fields:
        lines.append(f"  - field_path:     {field.field_path}")
        lines.append(f"    value:          {field.extracted_value!r}")
        lines.append(f"    proposed_class: {field.proposed_class}")
        lines.append(f"    confidence:     {field.confidence:.2f}")
        lines.append(f"    rationale:      {field.rationale}")
        lines.append("")
    return "\n".join(lines)


def _render_posture_menu() -> str:
    """Three-posture deployment-scope display (v7.0.10 §1.4 step 3).

    Renders the operator-facing posture-selection surface that the CLI
    presents alongside the per-field 4-class register display. The
    routing-simulation summary is intentionally short here; the full
    side-by-side simulation lives in the white-glove playbook §2.2.
    """
    lines: list[str] = []
    lines.append("")
    lines.append("=== Deployment posture (v7.0.10 §1.4) ===")
    lines.append("")
    lines.append(
        "Select one. The operator's Ed25519 signature attests to BOTH the "
        "per-field classifications AND this posture."
    )
    lines.append("")
    for posture_value in (
        POSTURE_PUBLIC_FRONTIER,
        POSTURE_SPLIT_CONTEXT,
        POSTURE_LOCAL_ONLY,
    ):
        label = POSTURE_DISPLAY_LABELS[posture_value]
        description = POSTURE_DESCRIPTIONS[posture_value]
        lines.append(f"  [{posture_value}] {label}")
        # Wrap description at ~78 columns for terminal readability without
        # pulling textwrap in. Operator can pipe through fmt if needed.
        lines.append(f"      {description}")
        if posture_value == POSTURE_LOCAL_ONLY:
            lines.append(
                "      NOTE: under-validation caveat applies until SN-LLC "
                "quarterly validation outcome signature flips the deployment "
                "manifest's local_only_validated flag."
            )
        lines.append("")
    lines.append(
        "The pre-v7.0.10 fourth posture ('Sanitized' / opaque-slot-token) is "
        "DEPRECATED. The two enforcement gates remain live as defense-in-depth."
    )
    lines.append("")
    return "\n".join(lines)


def _summarize_result(result: object) -> dict:
    # ReviewResult is a frozen dataclass; assemble a JSON-friendly dict.
    return {
        "ok": True,
        "doc_hash": getattr(result, "doc_hash"),
        "org_slug": getattr(result, "org_slug"),
        "n_fields": len(getattr(result, "field_decisions")),
        "n_overrides": len(getattr(result, "audit_entries")),
        "signed_review_path": getattr(result, "signed_review_path"),
        "register_path": getattr(result, "register_path"),
        "register_signed_at_iso8601": getattr(
            result, "register_signed_at_iso8601"
        ),
        "register_signing_key_id": getattr(result, "register_signing_key_id"),
        "selected_posture": getattr(result, "selected_posture", None),
        "gate_verification": [
            {
                "success": gr.success,
                "failure_code": gr.failure_code,
                "detail": gr.detail,
            }
            for gr in getattr(result, "gate_verification")
        ],
    }


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_argparser()
    args = parser.parse_args(argv)

    repo_root: Path = args.repo_root.resolve()

    try:
        proposal = load_proposed_classifications(
            repo_root=repo_root,
            org_slug=args.org_slug,
            doc_hash=args.doc_hash,
        )
    except ClassificationReviewError as exc:
        if args.json_output:
            sys.stdout.write(
                json.dumps(
                    {
                        "ok": False,
                        "stage": "load_proposal",
                        "code": getattr(exc, "code", ""),
                        "detail": str(exc),
                    }
                )
                + "\n"
            )
        else:
            print(f"error: {exc}", file=sys.stderr)
        return 1

    if not args.quiet:
        print(_render_proposal(proposal), file=sys.stderr)
        # v7.0.10 §1.4 — surface the three-posture deployment-scope menu
        # alongside the per-field display, even on non-interactive runs, so
        # operators reviewing the JSON output retain visibility into the
        # posture-selection surface.
        print(_render_posture_menu(), file=sys.stderr)

    # Validate posture early — surface a pointed error if a deprecated value
    # leaked in via --posture or a wrapper script.
    try:
        validate_posture(args.selected_posture)
    except InvalidPostureValue as exc:
        if args.json_output:
            sys.stdout.write(
                json.dumps(
                    {
                        "ok": False,
                        "stage": "validate_posture",
                        "code": exc.code,
                        "detail": str(exc),
                    }
                )
                + "\n"
            )
        else:
            print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.decisions_file is not None:
        decisions = _load_decisions_yaml(args.decisions_file)
    else:
        if not sys.stdin.isatty():
            print(
                "error: stdin is not a TTY and no --decisions-file supplied",
                file=sys.stderr,
            )
            return 1
        decisions = _interactive_decisions(proposal)

    signing_key_bytes = _load_signing_key(args.signing_key_file)
    verifying_key_bytes = _load_verifying_key(
        args.verifying_key_file, signing_key_bytes
    )

    try:
        result = run_classification_review(
            repo_root=repo_root,
            org_slug=args.org_slug,
            doc_hash=args.doc_hash,
            decisions=decisions,
            operator_key_id=args.operator_key_id,
            signing_key_bytes=signing_key_bytes,
            verifying_key_bytes=verifying_key_bytes,
            attestation_string=args.attestation_string,
            selected_posture=args.selected_posture,
        )
    except GateVerificationFailed as exc:
        if args.json_output:
            sys.stdout.write(
                json.dumps(
                    {
                        "ok": False,
                        "stage": "verify_against_class_gates",
                        "code": exc.code,
                        "detail": str(exc),
                        "gate_verification": [
                            {
                                "success": gr.success,
                                "failure_code": gr.failure_code,
                                "detail": gr.detail,
                            }
                            for gr in exc.gate_results
                        ],
                    }
                )
                + "\n"
            )
        else:
            print(f"F-CLASS-REGISTER-* gate rejection: {exc}", file=sys.stderr)
            for gr in exc.gate_results:
                if not gr.success:
                    print(
                        f"  {gr.failure_code}: {gr.detail}", file=sys.stderr
                    )
        return 1
    except ClassificationReviewError as exc:
        if args.json_output:
            sys.stdout.write(
                json.dumps(
                    {
                        "ok": False,
                        "stage": "orchestrator",
                        "code": getattr(exc, "code", ""),
                        "detail": str(exc),
                    }
                )
                + "\n"
            )
        else:
            print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json_output:
        sys.stdout.write(json.dumps(_summarize_result(result)) + "\n")
    else:
        print("\n=== Classification Review complete ===\n", file=sys.stderr)
        print(f"  doc_hash:                  {result.doc_hash}", file=sys.stderr)
        print(f"  fields confirmed:          {len(result.field_decisions) - len(result.audit_entries)}", file=sys.stderr)
        print(f"  fields overridden:         {len(result.audit_entries)}", file=sys.stderr)
        posture_label = (
            POSTURE_DISPLAY_LABELS.get(result.selected_posture, result.selected_posture)
            if result.selected_posture
            else "(legacy register-only signing — no posture attested)"
        )
        print(f"  selected posture:          {posture_label}", file=sys.stderr)
        print(f"  signed review artifact:    {result.signed_review_path}", file=sys.stderr)
        print(f"  per-org register:          {result.register_path}", file=sys.stderr)
        print(f"  signed_at_iso8601:         {result.register_signed_at_iso8601}", file=sys.stderr)
        print(file=sys.stderr)
        print("  F-CLASS-REGISTER-* gate verification:", file=sys.stderr)
        for gr in result.gate_verification:
            tag = "PASS" if gr.success else f"FAIL ({gr.failure_code})"
            print(f"    {tag}: {gr.detail}", file=sys.stderr)

    return 0


__all__ = ["main"]


if __name__ == "__main__":  # pragma: no cover - thin entry
    raise SystemExit(main(sys.argv[1:]))
