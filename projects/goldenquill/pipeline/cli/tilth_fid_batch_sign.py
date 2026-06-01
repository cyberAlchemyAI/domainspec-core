"""``tilth fid batch-sign`` — Pillar-1 charter batch sign-ceremony tool.

Authority
---------
Sign-ceremony spec: ``pipeline/funder_intelligence/pillar_1_charters/MANIFEST.md``
§"Sign-off path".
Underlying single-charter signing helper: ``pipeline/funder_intelligence
/_methodology/sign_charter.py``.
This tool wraps it for batch operation.

Scope
-----
Reduces the 14-charter sign-ceremony from 14 manual sign_charter invocations
to a two-step paced ceremony optimized for a hardware-key offline-signing
flow (YubiKey, Nitrokey, air-gapped openssl, etc.):

  Step 1 — ``stage``: write canonical bytes for each charter to disk PLUS
  a signatures.yaml template with placeholder hex per charter. Operator
  carries the bytes (or just the per-charter SHA3-512 hash) to their
  offline signer, batch-signs all 14 in one session, writes hex back into
  signatures.yaml.

  Step 2 — ``apply``: read the populated signatures.yaml, verify each
  signature against canonical bytes + the pinned FID publisher pubkey,
  apply via sign_charter for each charter, rename files to
  ``_charter_v1_SIGNED.md``, update the Pillar-1 MANIFEST table.

CC-007 / Law-5 boundary
------------------------
This tool performs zero outbound HTTP. It only reads/writes on-disk files
and invokes ``sign_charter.main()`` in-process for the apply step. Private
key material never enters this process — operator signs offline against
canonical bytes Tilth never touches.

Subcommands
-----------
* ``stage`` — write canonical bytes + signatures.yaml template for all 14
  Phase-1 roster charters (or a subset via ``--artifact-id``).
* ``apply`` — read populated signatures.yaml, apply each via sign_charter.
* ``status`` — print per-charter lifecycle (DRAFT v0 / SIGNED v1 / MISSING)
  and signatures.yaml population state.
* ``verify-only`` — verify each populated signature without applying
  (dry-run audit).

Exit codes
----------
* 0 — subcommand succeeded.
* 1 — bad CLI args / file not found / partial failure (some charters
  signed, some not — see report).
* 2 — verification failed (signatures.yaml hex does not verify against
  canonical bytes + pinned pubkey).
* 3 — apply step failed for all signatures (no charter successfully
  signed; ceremony aborted).
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import pathlib
import sys
from typing import Optional, Sequence

try:
    import yaml
except ImportError as e:  # pragma: no cover - imported by tests under venv
    print(f"ERROR: missing dep ({e}); install via `pip install pyyaml`.", file=sys.stderr)
    sys.exit(1)


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
FID_ROOT = REPO_ROOT / "pipeline" / "funder_intelligence"
CHARTERS_DIR = FID_ROOT / "pillar_1_charters"
MANIFEST = CHARTERS_DIR / "MANIFEST.md"

# Phase-1 roster + dispatch order (per Pillar-1 MANIFEST D2).
# Funders ordered first (Batch A — any order); programs in dispatch sequence.
PHASE_1_ROSTER: tuple[str, ...] = (
    # Batch A — funders
    "USDA-RD",
    "USDA-NIFA",
    "USDA-AMS",
    "PA-DEPT-AG",
    "PA-DCED",
    "HEINZ-FOUNDATION",
    "NCBA-CLUSA",
    "RICHARD-KING-MELLON-FOUNDATION",
    # Batch B — programs, in dispatch sequence
    "USDA-RD-RBDG-FY26",         # anchor
    "USDA-NIFA-SARE-NE-FY26",
    "USDA-RD-CFP-FY26",
    "USDA-RD-RCDG-FY26",
    "USDA-AMS-VAPG-FY26",        # deferred — cycle closed, but charter preserved
    "PA-DEPT-AG-AGINNOV-FY26",
)


# ─────────────────────────────────────────────────────────────────────
# Path helpers
# ─────────────────────────────────────────────────────────────────────

def draft_charter_path(artifact_id: str) -> pathlib.Path:
    return CHARTERS_DIR / f"{artifact_id}_charter_v0_DRAFT.md"


def signed_charter_path(artifact_id: str) -> pathlib.Path:
    return CHARTERS_DIR / f"{artifact_id}_charter_v1_SIGNED.md"


def canonical_bytes_path(stage_dir: pathlib.Path, artifact_id: str) -> pathlib.Path:
    return stage_dir / f"{artifact_id}.canonical_bytes"


def signatures_yaml_path(stage_dir: pathlib.Path) -> pathlib.Path:
    return stage_dir / "signatures.yaml"


# ─────────────────────────────────────────────────────────────────────
# Data types
# ─────────────────────────────────────────────────────────────────────

@dataclasses.dataclass
class CharterStageResult:
    artifact_id: str
    draft_path: pathlib.Path
    canonical_bytes_path: pathlib.Path
    content_hash_sha3_512: str
    canonical_bytes_size: int


@dataclasses.dataclass
class CharterApplyResult:
    artifact_id: str
    rc: int                       # 0 = signed, !=0 = failed
    message: str
    new_path: Optional[pathlib.Path] = None


# ─────────────────────────────────────────────────────────────────────
# stage
# ─────────────────────────────────────────────────────────────────────

def _resolve_artifact_set(args_ids: list[str] | None) -> list[str]:
    if not args_ids:
        return list(PHASE_1_ROSTER)
    bad = [a for a in args_ids if a not in PHASE_1_ROSTER]
    if bad:
        raise ValueError(
            f"artifact_id(s) not in Phase-1 roster: {bad}. "
            f"Roster: {', '.join(PHASE_1_ROSTER)}"
        )
    return args_ids


def _import_sign_charter():
    """Lazy-import sign_charter so tests can monkeypatch FID_ROOT paths first."""
    # Real-path import — fails fast if PR #33 hasn't merged.
    from pipeline.funder_intelligence._methodology import sign_charter  # noqa: WPS433
    return sign_charter


def cmd_stage(args: argparse.Namespace) -> int:
    """Write canonical bytes + signatures.yaml template for the specified set."""
    try:
        artifact_ids = _resolve_artifact_set(args.artifact_id)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    stage_dir: pathlib.Path = args.stage_dir.resolve()
    stage_dir.mkdir(parents=True, exist_ok=True)

    try:
        sign_charter = _import_sign_charter()
    except ImportError as e:
        print(
            f"ERROR: sign_charter helper not importable ({e}). "
            f"PR #33 must merge before batch sign can run.",
            file=sys.stderr,
        )
        return 1

    results: list[CharterStageResult] = []
    missing: list[str] = []
    already_signed: list[str] = []

    for aid in artifact_ids:
        draft = draft_charter_path(aid)
        if signed_charter_path(aid).exists():
            already_signed.append(aid)
            continue
        if not draft.exists():
            missing.append(aid)
            continue

        raw = draft.read_bytes()
        try:
            canonical = sign_charter.canonicalize_charter(raw)
        except ValueError as e:
            print(f"ERROR canonicalizing {aid}: {e}", file=sys.stderr)
            return 1

        hash_hex = sign_charter.content_hash(canonical)
        out = canonical_bytes_path(stage_dir, aid)
        out.write_bytes(canonical)
        results.append(CharterStageResult(
            artifact_id=aid,
            draft_path=draft,
            canonical_bytes_path=out,
            content_hash_sha3_512=hash_hex,
            canonical_bytes_size=len(canonical),
        ))

    # Write signatures.yaml template — sorted by roster order for stability.
    sigs_doc = {
        "fid_batch_sign_ceremony": {
            "staged_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "stage_dir": str(stage_dir),
            "signer_pubkey_fingerprint": "<fill_with_FID_publisher_pubkey_hex>",
            "charters": [
                {
                    "artifact_id": r.artifact_id,
                    "draft_path": str(r.draft_path.relative_to(REPO_ROOT)),
                    "canonical_bytes_path": str(r.canonical_bytes_path),
                    "content_hash_sha3_512": r.content_hash_sha3_512,
                    "canonical_bytes_size": r.canonical_bytes_size,
                    "signature_hex": "<fill_with_operator_Ed25519_signature_hex_or_omit_to_skip>",
                    "signed_at": "<fill_with_UTC_ISO_8601_timestamp_or_omit_to_default_to_now>",
                }
                for r in results
            ],
        }
    }
    sigs_path = signatures_yaml_path(stage_dir)
    sigs_path.write_text(
        yaml.safe_dump(sigs_doc, sort_keys=False, allow_unicode=True, default_flow_style=False)
    )

    print("=== FID Batch Sign — Stage ===")
    print(f"stage_dir: {stage_dir}")
    print(f"signatures.yaml: {sigs_path}")
    print(f"charters staged: {len(results)}")
    if already_signed:
        print(f"already signed (skipped): {already_signed}")
    if missing:
        print(f"missing draft (skipped): {missing}")
    print()
    print("Next steps:")
    print(f"  1. Operator signs each canonical_bytes_path offline with FID publisher Ed25519 key.")
    print(f"  2. Operator fills signature_hex (and optionally signed_at) into {sigs_path}.")
    print(f"  3. Run: python -m pipeline.cli.tilth_fid_batch_sign apply --stage-dir {stage_dir}")
    return 0


# ─────────────────────────────────────────────────────────────────────
# apply
# ─────────────────────────────────────────────────────────────────────

PLACEHOLDER_HEX_PREFIX = "<fill"
PLACEHOLDER_TIME_PREFIX = "<fill"


def _load_signatures_yaml(stage_dir: pathlib.Path) -> dict:
    p = signatures_yaml_path(stage_dir)
    if not p.exists():
        raise FileNotFoundError(f"signatures.yaml not at {p}. Run `stage` first.")
    data = yaml.safe_load(p.read_text()) or {}
    root = data.get("fid_batch_sign_ceremony")
    if not isinstance(root, dict):
        raise ValueError(f"{p}: top-level `fid_batch_sign_ceremony` mapping not found.")
    if not isinstance(root.get("charters"), list):
        raise ValueError(f"{p}: `charters` list not found.")
    return root


def cmd_apply(args: argparse.Namespace) -> int:
    """Read signatures.yaml, apply each via sign_charter, report results."""
    stage_dir: pathlib.Path = args.stage_dir.resolve()
    try:
        ceremony = _load_signatures_yaml(stage_dir)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    signer_fp = ceremony.get("signer_pubkey_fingerprint")
    if not signer_fp or signer_fp.startswith(PLACEHOLDER_HEX_PREFIX):
        print(
            f"ERROR: signer_pubkey_fingerprint not set in signatures.yaml. "
            f"Fill with FID publisher pubkey hex.",
            file=sys.stderr,
        )
        return 1

    try:
        sign_charter = _import_sign_charter()
    except ImportError as e:
        print(
            f"ERROR: sign_charter helper not importable ({e}). "
            f"PR #33 must merge before batch sign can run.",
            file=sys.stderr,
        )
        return 1

    results: list[CharterApplyResult] = []
    n_signed = 0
    n_skipped = 0
    n_failed = 0

    for entry in ceremony["charters"]:
        aid = entry.get("artifact_id")
        sig_hex = entry.get("signature_hex", "")
        signed_at = entry.get("signed_at", "")
        if not aid:
            results.append(CharterApplyResult(
                artifact_id="<unknown>",
                rc=1,
                message="entry missing artifact_id",
            ))
            n_failed += 1
            continue

        if not sig_hex or sig_hex.startswith(PLACEHOLDER_HEX_PREFIX):
            results.append(CharterApplyResult(
                artifact_id=aid,
                rc=0,
                message="signature_hex not filled — skipped",
            ))
            n_skipped += 1
            continue

        if signed_at.startswith(PLACEHOLDER_TIME_PREFIX) or not signed_at:
            signed_at = ""  # let sign_charter default to now()

        draft_path = pathlib.Path(entry.get("draft_path", ""))
        if not draft_path.is_absolute():
            draft_path = REPO_ROOT / draft_path
        if not draft_path.exists():
            results.append(CharterApplyResult(
                artifact_id=aid,
                rc=1,
                message=f"draft_path missing: {draft_path}",
            ))
            n_failed += 1
            continue

        # Build argv for sign_charter.main; --signer-pubkey-fingerprint is the
        # batch-level publisher key, --signature-hex is per-charter.
        sub_argv = [
            str(draft_path),
            "--signer-pubkey-fingerprint", signer_fp,
            "--signature-hex", sig_hex,
        ]
        if signed_at:
            sub_argv += ["--signed-at", signed_at]
        if args.allow_missing_pubkey_yaml:
            sub_argv.append("--allow-missing-pubkey-yaml")

        rc = sign_charter.main(sub_argv)
        if rc == 0:
            new_path = signed_charter_path(aid)
            results.append(CharterApplyResult(
                artifact_id=aid,
                rc=0,
                message="signed",
                new_path=new_path,
            ))
            n_signed += 1
        else:
            results.append(CharterApplyResult(
                artifact_id=aid,
                rc=rc,
                message=f"sign_charter exit {rc}",
            ))
            n_failed += 1

    # Report
    print("=== FID Batch Sign — Apply ===")
    for r in results:
        marker = "OK" if r.rc == 0 and r.new_path else ("SKIP" if "skipped" in r.message else "FAIL")
        print(f"  [{marker}] {r.artifact_id}: {r.message}")
    print()
    print(f"signed:  {n_signed}")
    print(f"skipped: {n_skipped}")
    print(f"failed:  {n_failed}")

    if n_signed == 0 and n_failed > 0:
        return 3
    if n_failed > 0:
        return 1
    return 0


# ─────────────────────────────────────────────────────────────────────
# status
# ─────────────────────────────────────────────────────────────────────

def cmd_status(args: argparse.Namespace) -> int:
    """Print per-charter lifecycle + optional signatures.yaml population state."""
    print("=== FID Batch Sign — Status ===")
    n_signed = 0
    n_draft = 0
    n_missing = 0
    for aid in PHASE_1_ROSTER:
        if signed_charter_path(aid).exists():
            state = "SIGNED v1"
            n_signed += 1
        elif draft_charter_path(aid).exists():
            state = "DRAFT v0"
            n_draft += 1
        else:
            state = "MISSING"
            n_missing += 1
        print(f"  {aid:36s}  {state}")
    print()
    print(f"signed: {n_signed} / 14   draft: {n_draft} / 14   missing: {n_missing} / 14")

    if args.stage_dir:
        stage_dir: pathlib.Path = args.stage_dir.resolve()
        sigs_path = signatures_yaml_path(stage_dir)
        if sigs_path.exists():
            try:
                root = _load_signatures_yaml(stage_dir)
            except ValueError as e:
                print(f"\nsignatures.yaml at {sigs_path} is malformed: {e}")
                return 1
            filled = sum(
                1 for e in root["charters"]
                if e.get("signature_hex", "").strip()
                and not e.get("signature_hex", "").startswith(PLACEHOLDER_HEX_PREFIX)
            )
            total = len(root["charters"])
            print(f"\nsignatures.yaml: {sigs_path}")
            print(f"  signatures filled: {filled} / {total}")
        else:
            print(f"\nsignatures.yaml not found at {sigs_path}")
    return 0


# ─────────────────────────────────────────────────────────────────────
# verify-only
# ─────────────────────────────────────────────────────────────────────

def cmd_verify_only(args: argparse.Namespace) -> int:
    """Verify every filled signature in signatures.yaml without applying."""
    stage_dir: pathlib.Path = args.stage_dir.resolve()
    try:
        ceremony = _load_signatures_yaml(stage_dir)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    signer_fp = ceremony.get("signer_pubkey_fingerprint", "")
    if not signer_fp or signer_fp.startswith(PLACEHOLDER_HEX_PREFIX):
        print("ERROR: signer_pubkey_fingerprint placeholder; fill before verify.", file=sys.stderr)
        return 1

    try:
        sign_charter = _import_sign_charter()
    except ImportError as e:
        print(f"ERROR: sign_charter helper not importable ({e}).", file=sys.stderr)
        return 1

    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

    pubkey = Ed25519PublicKey.from_public_bytes(bytes.fromhex(signer_fp))

    n_ok = 0
    n_bad = 0
    n_skipped = 0
    print("=== FID Batch Sign — Verify-Only ===")
    for entry in ceremony["charters"]:
        aid = entry.get("artifact_id", "<unknown>")
        sig_hex = entry.get("signature_hex", "")
        if not sig_hex or sig_hex.startswith(PLACEHOLDER_HEX_PREFIX):
            print(f"  [SKIP] {aid}: signature_hex not filled")
            n_skipped += 1
            continue

        bytes_path = pathlib.Path(entry.get("canonical_bytes_path", ""))
        if not bytes_path.exists():
            print(f"  [FAIL] {aid}: canonical_bytes_path missing: {bytes_path}")
            n_bad += 1
            continue

        canonical = bytes_path.read_bytes()
        # Recompute expected hash + compare
        expected_hash = entry.get("content_hash_sha3_512", "")
        actual_hash = sign_charter.content_hash(canonical)
        if expected_hash and expected_hash != actual_hash:
            print(
                f"  [FAIL] {aid}: content_hash_sha3_512 mismatch "
                f"(entry={expected_hash[:16]}..., disk={actual_hash[:16]}...)"
            )
            n_bad += 1
            continue

        if sign_charter.verify_signature(canonical, sig_hex, pubkey):
            print(f"  [OK]   {aid}: signature verifies")
            n_ok += 1
        else:
            print(f"  [FAIL] {aid}: Ed25519 verify failed")
            n_bad += 1

    print()
    print(f"verified ok: {n_ok}    failed: {n_bad}    skipped: {n_skipped}")
    if n_bad > 0:
        return 2
    return 0


# ─────────────────────────────────────────────────────────────────────
# Argparse wiring
# ─────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tilth fid batch-sign",
        description=(
            "FID Pillar-1 batch sign-ceremony tool. Wraps "
            "pipeline/funder_intelligence/_methodology/sign_charter.py for "
            "the 14-charter Phase-1 roster."
        ),
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    p_stage = sub.add_parser("stage", help="Write canonical bytes + signatures.yaml template.")
    p_stage.add_argument(
        "--stage-dir", type=pathlib.Path, required=True,
        help="Directory to write canonical_bytes files + signatures.yaml into.",
    )
    p_stage.add_argument(
        "--artifact-id", action="append", default=None,
        help="Optional artifact_id subset (repeat for multiple). Defaults to all 14.",
    )
    p_stage.set_defaults(func=cmd_stage)

    p_apply = sub.add_parser("apply", help="Apply each populated signature via sign_charter.")
    p_apply.add_argument("--stage-dir", type=pathlib.Path, required=True)
    p_apply.add_argument(
        "--allow-missing-pubkey-yaml", action="store_true",
        help="(Testing.) Pass-through to sign_charter; skip pinned-pubkey verification.",
    )
    p_apply.set_defaults(func=cmd_apply)

    p_status = sub.add_parser("status", help="Print per-charter lifecycle (+ optional sigs.yaml state).")
    p_status.add_argument(
        "--stage-dir", type=pathlib.Path, default=None,
        help="Optional. If set, also report signatures.yaml population state.",
    )
    p_status.set_defaults(func=cmd_status)

    p_v = sub.add_parser("verify-only", help="Verify each filled signature without applying.")
    p_v.add_argument("--stage-dir", type=pathlib.Path, required=True)
    p_v.set_defaults(func=cmd_verify_only)

    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
