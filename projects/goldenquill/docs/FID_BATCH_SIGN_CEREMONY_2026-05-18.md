# FID Pillar-1 Batch Sign-Ceremony — Operator Workflow

**Status:** Canonical operator-facing workflow for the 14-charter Phase-1 batch sign ceremony.
**Tool:** `pipeline/cli/tilth_fid_batch_sign.py`
**Underlying signer:** `pipeline/funder_intelligence/_methodology/sign_charter.py` (PR #33 lands this).
**Pillar-1 roster authority:** `pipeline/funder_intelligence/pillar_1_charters/MANIFEST.md`.
**Pillar-2 unblock spec:** `docs/FID_PILLAR_2_OPERATOR_WORKFLOW_2026-05-18.md`.

---

## §0 — Why a batch ceremony

Signing 14 charters one at a time via `sign_charter.py` means 14 round-trips between Tilth (canonical bytes + hash) and your offline signer (Ed25519 signature). This tool collapses that into two clean phases:

1. **Stage** — Tilth emits the canonical bytes + SHA3-512 hash for all 14 charters into one directory, plus a `signatures.yaml` template.
2. **Apply** — once you've filled signatures into the YAML (from your one offline batch-sign session), Tilth verifies + applies all 14 in one invocation.

Optimized for hardware-key flows (YubiKey, Nitrokey, air-gapped openssl). One PIN unlock, 14 signatures, one apply step.

---

## §1 — Prerequisite

`sign_charter.py` must exist on disk (lands when PR #33 merges). The tool's `stage` and `apply` subcommands will exit 1 with a clear error if the helper is unimportable.

---

## §2 — Step 1: stage

```bash
.venv/bin/python -m pipeline.cli.tilth_fid_batch_sign stage \
    --stage-dir /tmp/fid-batch-sign-$(date -u +%Y-%m-%d)
```

What this does:

- Iterates the 14-artifact Phase-1 roster (USDA-RD, USDA-NIFA, USDA-AMS, PA-DEPT-AG, PA-DCED, HEINZ-FOUNDATION, NCBA-CLUSA, RICHARD-KING-MELLON-FOUNDATION, plus the 6 programs in dispatch order).
- For each charter at `_charter_v0_DRAFT.md`: computes canonical bytes (via `sign_charter.canonicalize_charter()`), SHA3-512 hashes them, writes `<artifact_id>.canonical_bytes` into the stage dir.
- Writes `signatures.yaml` with one entry per charter — `signer_pubkey_fingerprint` and `signature_hex` fields are placeholdered for you to fill.
- Skips any charter already at `_charter_v1_SIGNED.md` (idempotent).

Optional: stage a subset.

```bash
.venv/bin/python -m pipeline.cli.tilth_fid_batch_sign stage \
    --stage-dir /tmp/fid-batch-sign-funders \
    --artifact-id USDA-RD \
    --artifact-id HEINZ-FOUNDATION
```

---

## §3 — Step 2: operator offline batch-sign

This step is **fully operator-side** — Tilth is not involved.

Your job:

1. Open `signatures.yaml`. Fill `signer_pubkey_fingerprint:` with your FID publisher Ed25519 pubkey hex (must match the pinned pubkey at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`).
2. For each charter entry: sign the bytes at `canonical_bytes_path` offline with your FID publisher Ed25519 private key. Paste the hex signature into `signature_hex:`.
3. Optionally set `signed_at:` to a UTC ISO-8601 timestamp (defaults to now() if omitted).
4. Save.

The canonical bytes are content-stable (SHA3-512 hash recorded at stage time matches what the verifier recomputes at apply time; mismatch fails closed in `verify-only`).

To skip a charter (e.g., not ready to sign yet), leave its `signature_hex:` placeholder unchanged. It will be reported as `SKIP` at apply time, not failed.

---

## §4 — Step 2.5 (optional): verify-only

Audit your signatures before applying — verify each filled signature against canonical bytes without modifying any charter file.

```bash
.venv/bin/python -m pipeline.cli.tilth_fid_batch_sign verify-only \
    --stage-dir /tmp/fid-batch-sign-2026-05-18
```

- `OK` per charter: signature verifies.
- `SKIP` per charter: `signature_hex` still placeholdered.
- `FAIL` per charter: signature does not verify (wrong bytes signed, wrong key, hex typo).

Exit code 0 if no failures; 2 if any verify failed. Run this before `apply` to catch issues without producing partial-state.

---

## §5 — Step 3: apply

```bash
.venv/bin/python -m pipeline.cli.tilth_fid_batch_sign apply \
    --stage-dir /tmp/fid-batch-sign-2026-05-18
```

For each charter entry with a filled `signature_hex:`:

- Re-verify signature against canonical bytes (defense in depth — `verify-only` is optional, this isn't).
- Call `sign_charter.main()` with the per-charter draft path, the batch-level `signer_pubkey_fingerprint`, and the per-charter `signature_hex`.
- `sign_charter` rewrites the charter §7 signature block with the signature data, renames the file from `_charter_v0_DRAFT.md` to `_charter_v1_SIGNED.md`, and updates the Pillar-1 MANIFEST row.

Report at end:

```
signed:  N
skipped: M  (signature_hex placeholdered)
failed:  K  (sig_verify failed / draft missing / other)
```

Exit codes:

- 0 — all targeted charters signed successfully.
- 1 — partial failure (some signed, some failed).
- 3 — total failure (no charter signed; ceremony aborted).

---

## §6 — Step 4: status (any time)

```bash
.venv/bin/python -m pipeline.cli.tilth_fid_batch_sign status
```

Prints per-charter lifecycle (`SIGNED v1` / `DRAFT v0` / `MISSING`) and roll-up counts.

With `--stage-dir`, also reports `signatures.yaml` fill progress (`signatures filled: N / 14`).

---

## §7 — Idempotency + recovery

- `stage` is idempotent — re-running with the same `--stage-dir` overwrites `signatures.yaml` (so re-run carefully; back up any in-progress signatures first).
- Skipped charters can be re-staged later with a fresh `--stage-dir` and signed in a follow-up ceremony.
- A charter that fails to apply (bad signature, etc.) stays at `_charter_v0_DRAFT.md`. Diagnose, re-stage that one charter into a fresh stage dir, fix the signature, re-apply.
- Once a charter is at `_charter_v1_SIGNED.md`, the batch tool refuses to re-stage it (the underlying `sign_charter.py` has the same idempotent guard).

---

## §8 — CC-007 / Law-5 boundary

This tool performs zero outbound HTTP. It only reads/writes on-disk files and invokes `sign_charter.main()` in-process for the apply step. Your Ed25519 private key never enters the tool — you sign offline against canonical bytes Tilth never touches, then paste hex back in.

The pinned FID publisher pubkey verification (built into `sign_charter`) is the trust root. The batch tool inherits it.

---

## §9 — What unblocks on completion

| State                                                       | Unblocks                                                          |
|-------------------------------------------------------------|-------------------------------------------------------------------|
| 1+ Batch A charter at `_v1_SIGNED.md`                       | Pillar-2 `init` for that funder (status flips `FETCHING`)          |
| 1+ Batch B charter at `_v1_SIGNED.md`                       | Pillar-2 `init` for that program (status flips `FETCHING`)         |
| All 14 charters at `_v1_SIGNED.md`                          | Full parallel Pillar-2 dispatch fires (Weeks 2-3 corpus assembly) |
| All 14 Pillar-2 `_signed.yaml` on disk                       | Pillar-3 extraction dispatch fires (Weeks 4-5)                    |

---

## §10 — Failure modes

| Symptom                                              | Cause                                                                | Fix                                                                                                       |
|------------------------------------------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| `stage` exit 1 "sign_charter helper not importable" | PR #33 not yet merged.                                               | Wait for PR #33 to merge, or check out a branch where sign_charter.py exists.                            |
| `verify-only` reports FAIL on one charter           | Wrong bytes signed (drift between stage and sign).                  | Re-stage that charter into a fresh stage dir; re-sign canonical bytes; retry.                            |
| `verify-only` reports FAIL on all charters          | Wrong `signer_pubkey_fingerprint`.                                   | Confirm against `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`. Update + re-run.        |
| `apply` exit 3 "no charter signed; aborted"         | All signatures failed verification.                                  | Same as above. Run `verify-only` first to surface which.                                                  |
| `apply` exit 1 "partial failure"                    | Some charters signed; others failed.                                 | Read the per-charter report. Re-stage the failures into a fresh stage dir for a follow-up ceremony.       |
| Charter file missing at apply                        | `_charter_v0_DRAFT.md` deleted between stage and apply.              | Restore from git; re-stage; re-apply.                                                                     |
| MANIFEST row not updated after apply                 | `sign_charter` MANIFEST regen failed (exit 3).                       | The charter file IS signed on disk. Manually update the MANIFEST row, or re-run with the MANIFEST present.|
