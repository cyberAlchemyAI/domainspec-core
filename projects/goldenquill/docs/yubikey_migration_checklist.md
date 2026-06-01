# YubiKey migration checklist — operator-attestation key (role 6)

**Purpose.** Migrate the operator-attestation Ed25519 keypair from Apple Notes locked-note custody (current posture per admin-risk-002) to YubiKey hardware-token custody. This is the "hardware-token upgrade" path called out in admin-risk-002 verdict and `vault_shared/key_rotation_policy.md` §6.5 "upgrade paths."

**Status.** Optional polish, not required for v0.1 Beta. Apple Notes posture is acceptable; YubiKey is the next-tier closure. Decide based on (a) whether buyer-facing WPFA PDFs start shipping in volume and (b) operator preference on key-custody class.

**Time budget.** 90-120 minutes wall-clock for full ceremony including device PIN setup. Hardware procurement is separate (1-7 days shipping).

**Critical constraint.** YubiKey 5 series supports Ed25519 via the OpenPGP applet (firmware 5.2.3+) and via PIV with workarounds. Native Ed25519 in the OpenPGP slot is the recommended path. The FIDO2 slot does NOT export key material for arbitrary signing — that's WebAuthn-only and won't work for `pipeline/scripts/verify_signed_assets.py`-style signature verification.

---

## §1 — Procurement

### Recommended models

| Model | Why | Cost (USD, list) |
|---|---|---|
| YubiKey 5C NFC | USB-C (matches modern Mac), NFC for phone backup, OpenPGP Ed25519 in firmware 5.2.3+, FIDO2/PIV/OTP all on board | ~$55 |
| YubiKey 5 NFC | USB-A version of the above for older machines or backup workflows | ~$50 |
| YubiKey 5C | USB-C without NFC if NFC isn't needed | ~$50 |

**Recommendation.** Buy **two units of YubiKey 5C NFC** — one primary, one offline backup. Identical seed across both at generation time. Two-unit posture is standard for any production signing role; loss-of-device probability is roughly cube-root of loss-of-two-devices probability.

### Where to buy

- **yubico.com** (manufacturer direct) — most current firmware, no supply-chain hop. Recommended. Look for "YubiKey 5C NFC" in the FIPS or non-FIPS line; non-FIPS is fine for v0.1.
- **Amazon Yubico storefront** — same units, faster shipping, slight supply-chain risk (counterfeit possible from third-party sellers). Only buy from "Sold by: Yubico" listings.
- **Avoid:** eBay, Newegg marketplace, AliExpress — counterfeit YubiKeys exist.

### Decision points before purchase

1. **FIPS or non-FIPS?** Non-FIPS for v0.1. FIPS 140-2 Level 3 adds ~$25/unit and FIPS-mode firmware is restrictive on Ed25519 support (some FIPS-mode keys disable Ed25519 entirely). Go non-FIPS unless a funder explicitly requires FIPS attestation later.
2. **One unit or two?** Two. Single-unit YubiKey custody is worse than Apple Notes + sealed envelope because losing one device with no backup is unrecoverable; Apple Notes is at least passphrase-recoverable from operator memory.
3. **Same seed on both, or different seeds with shared role pubkey?** Same seed on both. Different seeds means the pubkey YAML pins one of them; if that one is lost, the backup unit can't sign as the pinned identity. Same-seed-cloning is YubiKey's documented dual-device posture (Yubico calls it "redundant key" pattern).
4. **Touch-required for signing?** YES. Configure the OpenPGP signature slot to require physical touch per signature. This prevents malware on the connected host from signing WPFA CycleReceipts silently. Touch latency adds ~1 second per sign, acceptable for the WPFA cycle-close cadence.

### Estimated total

| Item | Qty | Cost |
|---|---|---|
| YubiKey 5C NFC | 2 | $110 |
| Tax (PA ~6%) | — | $7 |
| Shipping (yubico.com standard) | 1 | $0 (free over $40) |
| **Total** | — | **~$117** |

Plus 1-7 days shipping if buying yubico.com direct. Amazon Prime can next-day if speed matters.

---

## §2 — Pre-arrival setup (do this while waiting for hardware)

1. **Install `gpg` + `ykman` on the Mac.**
   ```
   brew install gnupg ykman
   ```
2. **Decide PIN policy.** YubiKey OpenPGP has two PINs:
   - **User PIN** — for routine signing (6+ digits, blocks after 3 wrong attempts, unblockable via Admin PIN).
   - **Admin PIN** — for management operations (8+ digits, blocks after 3 wrong attempts, unblockable via factory reset which wipes the slot).
   
   **Recommendation.** Generate both PINs in Apple Notes locked-note (or a dedicated passphrase manager). User PIN gets used several times per cycle; Admin PIN gets used at setup + key generation + every few months for rotation. **Do NOT use birthday, address numbers, last-4-of-SSN, or other guessable patterns.** Recommend `openssl rand -base64 12 | tr -d '/=+' | head -c 8` for the Admin PIN (8 chars of strong entropy).

3. **Decide touch policy.** Recommended: **touch required for sign** (default) on the OpenPGP signature slot.

4. **Read `vault_shared/key_rotation_policy.md` §4 rotation runbook + §6.5 upgrade paths.** The migration is a rotation event, not a new-install ceremony — the existing pubkey `094a4dc41fa778397f581a8f5977dfc99a2cd9cdee8890bdabd296a78bbbd8cf` will be retired and a NEW pubkey will be pinned.

5. **Notify any downstream consumers.** Currently zero — no signatures in flight per `docs/operator_attestation_state_audit_2026-05-18.md`. So this leg is a no-op today. If migration happens after WPFA buyer-PDFs start shipping, this leg requires customer notification per `vault_shared/key_rotation_policy.md` §4.

---

## §3 — Ceremony (do this with both YubiKeys present)

### Step 3.1 — Initialize both YubiKeys

For each YubiKey:

```
ykman openpgp reset
# enter "y" to confirm — wipes any prior state
ykman openpgp access change-pin
# set User PIN (default factory User PIN is 123456)
ykman openpgp access change-admin-pin
# set Admin PIN (default factory Admin PIN is 12345678)
ykman openpgp keys set-touch sig on
# require touch on signature slot
```

### Step 3.2 — Generate the Ed25519 keypair on Primary YubiKey

```
gpg --card-edit
# at the gpg/card> prompt:
admin
# enable admin commands
key-attr
# select 2 (ECC) and ed25519 for signature key
generate
# follow prompts; do NOT save a backup seed via GPG (the seed will be exported manually next step)
```

### Step 3.3 — Export the Ed25519 seed for cloning to Secondary YubiKey

**This is the sensitive step.** YubiKey's OpenPGP applet does not natively export Ed25519 private keys after generation. The recommended pattern is:

- Generate the Ed25519 keypair OFF-DEVICE using `openssl genpkey -algorithm Ed25519 -out /tmp/ed25519.pem` (or equivalent)
- Import the same key to BOTH YubiKeys via `gpg --import` + `keytocard` 
- Securely wipe `/tmp/ed25519.pem` (use `rm -P` on macOS for secure overwrite)

This puts the operator briefly in possession of the raw seed during transit. Mitigations:
- Generate on an air-gapped Mac or in a VM with no network access
- Wipe immediately after both YubiKeys hold the seed
- Apple Notes stash of the seed (matches admin-risk-002 posture) IS acceptable since the YubiKey copies are the production hardware-token custody and the Apple Notes copy becomes the offline backup

### Step 3.4 — Verify both YubiKeys sign identically

```
echo "test" | gpg --sign --output /tmp/sig1.bin
# swap YubiKey
echo "test" | gpg --sign --output /tmp/sig2.bin
# both signatures should verify against the same pubkey
gpg --verify /tmp/sig1.bin
gpg --verify /tmp/sig2.bin
# clean up
rm /tmp/sig1.bin /tmp/sig2.bin
```

### Step 3.5 — Update `vault_shared/operator_attestation/publisher_pubkey.signed.yaml`

This is a **rotation event**, not a new install. The new pubkey YAML carries `prior_pubkey_chain` containing the OLD pubkey + a signature by the OLD pubkey over the NEW pubkey (co-sign attestation per §4 of the policy).

Steps:
1. With the OLD Apple-Notes-custody key, sign the NEW YubiKey pubkey (the co-sign attestation).
2. Generate the new `publisher_pubkey.signed.yaml`:
   - `publisher_pubkey_ed25519_hex` = NEW YubiKey pubkey hex
   - `prior_pubkey_chain` = `[{"prior_pubkey_ed25519_hex": "094a4dc4...", "cosign_signature_ed25519_hex": "<OLD-key signature over NEW canonical bytes>"}]`
   - `published_at_utc` = ceremony moment
   - Self-sign with the NEW YubiKey key (this is the TOFU self-sign for the new identity)
3. Verify the new asset round-trips via `pipeline/scripts/verify_signed_assets.py --verbose`.

### Step 3.6 — Author admin-risk ledger row

Use the template at `pipeline/engineering/_templates/yubikey_migration_template.jsonl`. The row's `event_kind` is `pubkey_rotation`, `event_kind_subtype` is `hardware_token_upgrade`. Severity: **MED** (rotation event, not compromise). The row chains via `references_row_id` back to the most recent operator-attestation ledger row (likely the latest `key_backup_verified` row).

### Step 3.7 — Retire the old key

After the new pubkey is pinned and verified:
1. Open the Apple Notes locked-note "Tilth key custody — operator.attestation_publisher"
2. Update the note title to "RETIRED 2026-XX-XX — Tilth key custody — operator.attestation_publisher (pre-YubiKey-migration)"
3. Optionally: scrub the key bytes from the note body (preserve title + retirement date). This is a **judgment call** — retaining the retired seed lets you re-verify historical signatures emitted under the old key; scrubbing it closes the SPOF on the old key entirely. **Recommendation: retain for 1 year, then scrub.**
4. Update the offline sealed-envelope address card to reflect the retirement. Either fold a new "RETIRED 2026-XX-XX" card behind the active one, or write a fresh envelope for the new YubiKey custody and seal both into the offline storage with a date-ordered cover sheet.

### Step 3.8 — Physically store the Secondary YubiKey offline

The Primary YubiKey stays at Josh's workstation. The Secondary YubiKey goes into the same physical-storage location as the sealed envelope from admin-risk-003 (or a separate offline location if Josh prefers geographic redundancy). Document the Secondary location on the offline address card.

---

## §4 — Post-migration verification

1. Run `pipeline/scripts/verify_signed_assets.py --verbose` — should return FAIL: 0 with the new pubkey now in VERIFIED bucket (and prior_pubkey_chain co-sign verifying against the retired pubkey).
2. Run the next WPFA CycleReceipt buyer-PDF emission (if any are in the queue) — should sign cleanly with the YubiKey + touch.
3. Schedule the next quarterly verification per the runbook at `docs/operator_attestation_quarterly_verification_runbook.md` — but with a SUBSTANTIVE variation: the verification now checks BOTH the YubiKey custody (insert primary, prompt for User PIN, sign a test message — should succeed; do NOT consume the touch on the cycle slot) AND the secondary-YubiKey offline storage (physically inspect, do NOT insert routinely).

---

## §5 — Open decision points (operator confirms before ceremony)

These must be settled before §3 fires:

1. **PIN policy specifics.** What User PIN length? What Admin PIN length? Where stashed?
2. **Touch policy.** Touch required for sign? (Recommended: YES.)
3. **Same-seed or different-seed for the two units?** (Recommended: same-seed.)
4. **Apple Notes retention.** Retain the old seed in Apple Notes for 1 year, or scrub immediately on migration? (Recommended: retain 1 year for historical signature verifiability.)
5. **Geographic redundancy for the Secondary YubiKey.** Same offline location as the sealed envelope, or separate location? (Recommended: same location is fine for v0.1; geographic separation matters more once buyer-facing PDFs are in production volume.)
6. **Cadence change post-migration.** Does quarterly verification become semi-annual once hardware-token custody is in place? (Recommended: keep quarterly for the first year, then re-evaluate.)
7. **Migration timing.** Now (before any buyer-facing PDFs ship) is the cleanest moment — no in-flight signatures to worry about. Migrating mid-deployment-cycle requires customer notification per §4 policy.

---

## §6 — Ledger row template

Pre-staged at `pipeline/engineering/_templates/yubikey_migration_template.jsonl`. Fill the `<FILL>` fields at ceremony fire-time.

## §7 — What this checklist does not do

- Does not generate any keys.
- Does not modify any signed asset.
- Does not purchase any hardware.
- Does not commit Josh to migration — this is an opt-in upgrade.

This is procurement + procedure documentation. Execution is operator-driven at a time of operator's choosing.

## §8 — Authorities

- `vault_shared/key_rotation_policy.md` §3 (rotation cadence), §4 (rotation runbook), §6.5 (upgrade paths)
- `pipeline/engineering/admin_risk_ledger.v1.jsonl` rows 001, 002, 003
- `docs/operator_attestation_state_audit_2026-05-18.md`
- Yubico OpenPGP docs: https://developers.yubico.com/PGP/ (operator can web-search for current versions before purchase)
