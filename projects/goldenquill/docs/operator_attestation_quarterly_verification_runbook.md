# Operator-attestation key backup — quarterly verification runbook

**Authority.** `vault_shared/key_rotation_policy.md` §6.5 step 3 + `admin-risk-003.verification_cadence_next`.

**Cadence.** Quarterly. First scheduled fire: **2026-08-17 09:00 EDT**. Each verification reschedules the next one 90 days out.

**Purpose.** Liveness check on the dual-redundant key backup posture (Apple Notes online + sealed envelope offline). Confirms both backup legs are still intact, the address card still points where it should, and the operator can still unlock the Apple Notes locked-note. Does NOT involve reading or copying any private-key bytes.

**Time budget.** 30 seconds + the ledger row append.

---

## Procedure (Josh does this on the day)

### Step 1 — Locate the sealed envelope (offline secondary)

Retrieve the sealed envelope from its physically separate storage location (per admin-risk-003 the envelope contains a pointer-only address card, no key material).

**Expected.** Envelope is sealed, tamper-evident closure intact, location matches what was recorded at sealing 2026-05-18T01:39:52Z.

**If tampered:** STOP. Do not open. Escalate to `vault_shared/key_rotation_policy.md` §4 compromise-response runbook. The compromise window is the period from previous verification to now.

### Step 2 — Open, visually inspect, re-seal

Open the envelope. Confirm the address card reads:

```
Vault name:           Apple Notes
Note title prefix:    Tilth key custody — operator.attestation_publisher
Rotation date:        2026-05-17
```

**Expected.** All three fields match the canonical values above. No private-key material anywhere on the card.

**If mismatched:** STOP. Note the actual values, escalate to §4 compromise-response runbook — the address card has been substituted.

Re-seal the envelope (fresh tamper-evident closure) and return it to its storage location.

### Step 3 — Apple Notes passphrase liveness check

Open Apple Notes. Locate the locked note titled "Tilth key custody — operator.attestation_publisher" (or matching the prefix on the card).

Tap the note. Apple Notes should prompt for the note passphrase. Enter it.

**Expected.** Note unlocks. (You're confirming the passphrase still works — you are NOT reading the key material. Once unlocked, re-lock immediately without scrolling, copying, or screenshotting.)

**If passphrase no longer works:** STOP. This is a partial backup failure (online leg lost; offline leg still intact via the address card). Escalate to §4 — but note that the offline pointer + the operator's memory of the key may still recover the seed if the operator can reconstruct it.

Re-lock the note.

### Step 4 — Append ledger row

Append a `key_backup_verified` row to `pipeline/engineering/admin_risk_ledger.v1.jsonl` using the template at `pipeline/engineering/_templates/key_backup_verified_template.jsonl`. Fill the four `<FILL>` fields:

- `row_id` — next available `admin-risk-XXX` integer
- `event_timestamp_utc` — moment of physical verification (steps 1-3 completion)
- `ledger_row_authored_at_utc` — moment the ledger row is written
- `verified_at_utc` — same as `event_timestamp_utc`

The row's `references_row_id` chains back to `admin-risk-003` (or to the most recent `key_backup_verified` row if subsequent quarters have already happened).

Commit the ledger row with a one-line commit message: `admin-risk: Q<N> 2026-XX-XX key_backup_verified`.

### Step 5 — Schedule next quarter

Open Claude (Cowork mode) and ask it to re-fire this runbook for 2026-11-17 09:00 EST (i.e., +90 days from this verification, adjusted for any DST shift). Or run `mcp__scheduled-tasks__create_scheduled_task` directly with `fireAt: "2026-11-17T09:00:00-05:00"` and the same prompt text (the scheduled task created at 2026-05-18 has its prompt at `/Users/goldenquill/Documents/Claude/Scheduled/operator-attestation-quarterly-verification-2026-08-17/SKILL.md` — copy it forward).

---

## What this runbook does not do

- Does not read or copy private-key bytes.
- Does not generate new keys.
- Does not sign or modify any signed asset.
- Does not modify the `vault_shared/operator_attestation/publisher_pubkey.signed.yaml` pinning.
- Does not modify `vault_shared/key_rotation_policy.md`.

This is a backup-liveness check, not a rotation.

---

## Cadence drift

If a quarter slips past 2 weeks (verification not done by Q+14 days), the next ledger row should be authored with `severity: MED` instead of `LOW` and a `cadence_drift: true` field. Two consecutive slips (180 days without verification) escalates to HIGH and triggers a §4 review — not a compromise event, but a posture audit on whether the backup is still operationally trusted.

If the quarter slips past 90 days unverified, the key is treated as **backup-unverified** and any new buyer-facing WPFA CycleReceipt emission is gated (`F-WPFA-OPERATOR-SIGNATURE-MISSING` stays open as a soft warning until verification re-lands).

## Authorities

- `vault_shared/key_rotation_policy.md` §3 (operator-attestation: annual review + on-compromise), §4 (compromise-response runbook), §6.4 (SPOF), §6.5 (backup posture)
- `pipeline/engineering/admin_risk_ledger.v1.jsonl` rows 001, 002, 003
- `vault_shared/operator_attestation/publisher_pubkey.signed.yaml` (the pinning being protected)
- `docs/operator_attestation_state_audit_2026-05-18.md` (most recent state audit)
