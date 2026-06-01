# Operator-attestation keypair — state audit, 2026-05-18

**Scope.** Read-only audit of the operator-attestation Ed25519 keypair state,
prompted by an earlier project-audit reading that flagged the private key as
"potentially lost." This document is recon + risk assessment + recommended
action. **No keys were generated, no assets were signed, no private-key
contents were read or exposed in writing this audit.**

**Bottom line.** Pubkey present and self-verifying; private key intentionally
redacted from `_private/` with the operator's keystash already confirmed in
Apple Notes (online) and a sealed-envelope address card (offline); zero
signatures in flight under this key. **All green — no action needed.**

---

## 1. Pubkey state

`vault_shared/operator_attestation/publisher_pubkey.signed.yaml`

| Field | Value |
|---|---|
| Pubkey hex | `094a4dc41fa778397f581a8f5977dfc99a2cd9cdee8890bdabd296a78bbbd8cf` |
| Published at (UTC) | `2026-05-17T21:56:20Z` |
| Publisher role id | `operator.attestation_publisher` |
| Prior pubkey chain | `[]` (TOFU first install — no rotation history) |
| Canonical-bytes SHA3-512 recorded | `09bd191bcfb37f70183710a67ff1d240…` |
| Canonical-bytes SHA3-512 computed | `09bd191bcfb37f70183710a67ff1d240…` |
| Canonical-bytes SHA3-512 match | ✓ |
| Self-signature verifies | ✓ |
| Signature method | Ed25519 over canonical JSON (sort_keys, separators=(',', ':')) with `publisher_signature_ed25519_hex` + `canonical_bytes_sha3_512_hex` excluded prior to canonicalization |

**How the signing happened.** The file's own comment block (lines preceding
the data) describes the canonicalization recipe and identifies the signing
event as Trust-On-First-Use self-signing at "ceremony first-install" on
2026-05-17. The signature verifies against the same pubkey it pins —
self-verifying TOFU asset, byte-for-byte mirror of the FID-publisher
introduction precedent (2026-05-16 19:30Z).

**CI verifier confirmation.** `pipeline/scripts/verify_signed_assets.py
--verbose` (the script that gates the `Signature round-trip` GitHub Actions
job) runs clean against the current repo: `Total: 78  |  VERIFIED: 48
DEFERRED_V0_2: 27  PLACEHOLDER: 3  FAIL: 0`. The operator-attestation
pubkey YAML is in the VERIFIED bucket, not PLACEHOLDER and not FAIL.

---

## 2. Private key reachability

`_private/operator_attestation_privkey_2026-05-17.txt`

| Property | Value |
|---|---|
| Present on disk | YES |
| Size on disk | 855 bytes |
| Total lines | 18 |
| Comment lines | 18 |
| Data lines | 0 |
| Contains key material | **NO — this is a redacted stub** |

**Status.** Every line in the file is a comment. There are zero data lines.
The file's own header reads "OPERATOR-ATTESTATION ED25519 PRIVATE KEY —
REDACTED 2026-05-17" and explains that the private-key bytes were scrubbed
from this file on 2026-05-17 at operator confirmation, with the key stashed
in Apple Notes locked-note per `vault_shared/key_rotation_policy.md` §6.5
step 1.

**Why this looks alarming but isn't.** The file is 855 bytes (≈ the size of
an annotated PEM-style private-key file would be), so a size-based scan
without reading the file body could mistake it for a live key. It is not.
The body is documentation. The actual private key lives in two places per
the admin-risk ledger — neither of which is this repository.

**Repo containment.** `.gitignore` excludes `_private/` wholesale at the
`# === 2026-05-11 sweep additions ===` block (`_private/` directory rule).
The stub file is not committed and cannot leak via the repo.

**Off-repo key custody.** Per `pipeline/engineering/admin_risk_ledger.v1.jsonl`:

- **admin-risk-002** (2026-05-17T22:19:57Z) — operator confirmed the private
  key is stashed in Apple Notes locked-note titled per the convention
  "Tilth key custody — operator.attestation_publisher". Posture: AES-128-GCM
  at rest, PBKDF2 key derivation from operator note password, not
  Secure-Enclave-backed, iCloud-syncable if iCloud Notes is enabled.
- **admin-risk-003** (2026-05-18T01:39:52Z) — operator wrote and stored the
  offline sealed-envelope address card per policy §6.5 step 2 (vault name +
  note title prefix + rotation date; pointer-only, no key material).
  §6.4 single-point-of-failure flag closed at this row.

Both ledger rows carry verbatim operator confirmation text and timestamped
authorship. They are the ground truth for "where is the key" and they
agree: online primary in Apple Notes, offline secondary in a sealed
envelope.

---

## 3. Signatures in flight

Search across `pipeline/engineering/lock_history.v1.jsonl`, all card YAMLs,
all signed assets, and the full repo tree (excluding `.venv/`, `.git/`,
`.claude/`, `__pycache__/`):

| Surface | Count | Notes |
|---|---|---|
| `lock_history.v1.jsonl` rows containing pubkey hex `094a4dc4…` | **0** | No lock_history row is signed by this key. The 4 hits for the string `operator_attestation` are all design references in spec text — CycleReceipt Cedar rule, `F-PACKET-OPERATOR-SIGNATURE-INVALID` predicate-input row, blueprint amendment narrative — not signature bytes produced by the key. |
| Card YAMLs (`vault_shared/cards/`, `pipeline/cards/`) signed by this key | **0** | Cards are signed by the cards-publisher pubkey (`c93f1881…` post-rotation; rotated from compromised `0b1a0bbf…` at row 280, 2026-05-18T00:00:00Z), not by the operator-attestation pubkey. |
| Buyer-facing WPFA CycleReceipt PDFs | **0** | The §17 WPFA buyer-facing PDF emitter is gated by `F-WPFA-OPERATOR-SIGNATURE-MISSING` against this pubkey. No CycleReceipts have been emitted yet — the role is provisioned but not used. |
| Reflection Packet operator-attestation signatures | **0** | The §4 v2.x.y.1 `F-PACKET-OPERATOR-SIGNATURE-INVALID` predicate binds to this pubkey at v0.2 first wave. The v0.1 hook is DORMANT (the predicate raises `NotImplementedError`), so no real packets have been signed. |
| Any other artifact carrying an Ed25519 signature produced by this seed | **0** | Repo-wide grep for the pubkey hex finds only the policy doc, the admin-risk ledger, a handoff document discussing the keypair, the self-signed pubkey YAML, and the redacted privkey stub — all references *to* the key, not signatures *by* the key. |

**The pubkey is provisioned but not yet load-bearing.** It exists on the
shelf, signed-into-existence by itself, waiting for its first WPFA cycle
close. There is nothing downstream of this key that would lose
verifiability if the key disappeared today, because nothing has been signed
by it yet.

---

## 4. Risk assessment

Applying the decision tree from the audit prompt:

- Private key present (in operator custody — Apple Notes online + sealed
  envelope offline) ✓
- Pubkey verified (TOFU self-signature round-trips under the documented
  canonicalization recipe; CI verifier confirms it) ✓
- Signatures round-trip — N/A, no signatures in flight ✓ (vacuously true)

This is the **"all green, no action needed"** branch of the prompt's
decision tree.

**Blast radius if the key were lost right now.** Zero — there are no signed
artifacts to lose verifiability of. The cost of regeneration would be one
TOFU ceremony, one admin-risk ledger row, and one self-signed pubkey YAML
update. The cost of doing nothing is also zero — the existing key is
healthy, backed up online and offline, and operator-confirmed in custody.

**Where the earlier audit reading went sideways.** `docs/project_audit_2026-05-18.md`
lines 18, 466, and 484-486 originally read the 855-byte stub as live key
material and the role as "MISSING placeholder." The audit author has
already published a correction at lines 202 and 470 (folded in at PR #19's
signature-round-trip verifier run, 2026-05-18) acknowledging that
`094a4dc4…` is a real TOFU-self-signed asset and Role 6 is PINNED. The
correction is correct. This audit confirms that correction stands and
extends it: not only is the pubkey real, the private key is recoverable
(online + offline backup), and nothing has been signed yet so there is no
risk surface at all.

The remaining residual that the project-audit document flags — "off-machine
backup" — was the open item *at the time of that audit's writing*. Admin-risk
ledger rows 002 (Apple Notes stash) and 003 (sealed-envelope address card)
have since closed both legs of the §6.5 backup posture. The off-machine
backup is no longer open.

---

## 5. Recommended next action

**None required.** The operator-attestation keypair is in the cleanest state
possible for a not-yet-load-bearing signing role: pubkey published and
verified, private key in dual-redundant operator custody, zero signatures
in flight, gitignore correctly tight, CI verifier passing.

The next event that touches this key will be the first WPFA CycleReceipt
buyer-facing PDF emission. At that point, the operator will retrieve the
key from Apple Notes, run the signing ceremony per
`vault_shared/key_rotation_policy.md`, and an admin-risk-ledger row
referencing `references_row_id: admin-risk-003` will record the first
production use. Nothing about the current state blocks that event.

**Optional polish items (operator-confirmed disposition, 2026-05-18):**

1. **First quarterly verification (ETA 2026-08-17) — SCHEDULED.** Reminder
   scheduled at `mcp__scheduled-tasks` with fireAt `2026-08-17T09:00:00-04:00`
   (taskId `operator-attestation-quarterly-verification-2026-08-17`). Runbook
   landed at `docs/operator_attestation_quarterly_verification_runbook.md`.
   Pre-staged ledger row template at
   `pipeline/engineering/_templates/key_backup_verified_template.jsonl` —
   day-of fill-in is ~30 seconds. The verification itself is a physical
   envelope check + Apple Notes passphrase liveness check; no key material
   is read or copied.

2. **Hardware-token upgrade (YubiKey 5C NFC, 2 units) — CHECKLIST LANDED.**
   Procurement + setup + migration ceremony documented at
   `docs/yubikey_migration_checklist.md`. Pre-staged ledger row template
   at `pipeline/engineering/_templates/yubikey_migration_template.jsonl`.
   Migration is voluntary upgrade per `vault_shared/key_rotation_policy.md`
   §6.5 upgrade-paths; not required for v0.1 Beta. Open operator decision
   points (PIN policy, touch policy, same-seed-vs-different, Apple-Notes-
   retention, geographic redundancy, cadence change, timing) listed at
   checklist §5. Execution is operator-driven at operator's chosen moment.

3. **Reflection Packet producer pubkey (v0.2 event) — LOCKED AT NO-ACTION
   per operator decision 2026-05-18.** Option (a) selected: wait for v0.2
   first-wave LOCK. The placeholder posture at
   `vault_shared/reflection_packet/producer_pubkey.signed.yaml` is the
   correct posture for v0.1; the asset's own comment block specifies the
   ceremony fires at white-glove onboarding via `tilth reflection-packet
   pubkey init`, and the publisher signature requires SN-LLC's pubkey
   (also currently PLACEHOLDER) to land first. Cross-role bridging via
   operator-attestation as interim publisher was considered (option b)
   and rejected because it adds key-reuse risk to a key that is currently
   not load-bearing. Tracked at `vault_shared/key_rotation_policy.md` §8.5
   item 2; will close at v0.2 first wave LOCK.

**Operator decision point on this audit.** None remaining. The three
optional items are now: scheduled (#1), documented + queued (#2), and
explicitly deferred to v0.2 (#3). No keypair action recommended today.

---

## 6. What this audit did not do

- Did not read the private-key contents (confirmed file is a 18-line
  comment-only stub before opening the body; counted lines and inspected
  comment headers only).
- Did not generate a new keypair.
- Did not sign any asset.
- Did not modify any signed asset.
- Did not modify `.gitignore`, the admin-risk ledger, the key-rotation
  policy doc, or any TOFU YAML.
- Did not exfiltrate the pubkey hex to any non-repo location (the hex is
  public-by-design and already lives in 5 repo files).

Read-only. Report-only.

---

## Sources

- `vault_shared/operator_attestation/publisher_pubkey.signed.yaml`
- `vault_shared/key_rotation_policy.md` §§ 3, 4, 6.4, 6.5, 8.1, 8.5
- `pipeline/engineering/admin_risk_ledger.v1.jsonl` rows 001, 002, 003
- `pipeline/engineering/lock_history.v1.jsonl` (grep: 0 rows signed by `094a4dc4…`)
- `pipeline/scripts/verify_signed_assets.py` (CI verifier, FAIL: 0)
- `.github/workflows/signature_roundtrip.yml`
- `.gitignore` `_private/` rule
- `docs/project_audit_2026-05-18.md` §13 row 2 + lines 18, 202, 466, 470, 484-490
- `pipeline/handoffs/od_e_fix_forward_paired_commit_2026-05-17.md` lines 209-215
  (explanation of why `094a4dc4…` is a pubkey, not a seed)
