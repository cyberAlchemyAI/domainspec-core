---
title: WPFA white-glove pubkey-pin runbook
filed: 2026-05-18
operator: Josh Inklovich (or designated operator at deployment)
status: AUTHORED 2026-05-18 — operator-runbook; not a code or spec change
parent_locks:
  - pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md                                 # §17 v1 LOCKED 2026-05-11
  - pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md                     # §2 v7.4 LOCKED 2026-05-11
  - pipeline/blueprint/v0.1/section_04_v2_x_z_wpfa_amendment.md                                   # §4 v2.x.z LOCKED 2026-05-11
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                                   # v7.0.7 LOCKED 2026-05-10 — §6.1 SN-LLC router-template Ed25519 signing precedent (same trust mechanism, byte-for-byte)
authority: code phase landed 2026-05-11; scope brief PR #36 surfaced this runbook as Track A doc tidy-up; this file is the operator-facing companion to `tilth wpfa registry pin-pubkey`
applies_to: every white-glove Beta deployment of Golden Quill before the first cycle-close emission
cross_links:
  - docs/wpfa_status.md
  - docs/white_glove_v0_1_beta.md
  - pipeline/cli/tilth_wpfa.py
  - pipeline/orchestrator/seats/wpfa/cycle_accountant.py
---

# 1. What this runbook covers

The one ceremony every Golden Quill deployment must complete before its first WPFA cycle-close emission: pinning the Sovereign Node LLC (SN-LLC) Ed25519 public key into the operator-attested file at `vault_shared/wpfa/sn_llc_pubkey.signed.yaml`.

Until pinning lands, the WPFA Cycle Accountant fails closed at `load_active()` via `F-WPFA-COEFFICIENT-SIGNATURE-INVALID.pubkey_mismatch`. After pinning, the Coefficient Registry's `sn_llc_signature_ed25519` is verified against the pinned key on every receipt emission. The trust mechanism mirrors v7.0.7 §6.1 router-template signing byte-for-byte (canonical-JSON encode of all fields except the signature, sorted keys, no insignificant whitespace, UTF-8). Once pinned, rotation requires a co-signature from the prior pinned key (Trust-On-First-Use rotation).

# 2. Preconditions

Before pinning, all of the following must be true:

1. Golden Quill appliance is booted and the operator holds shell access.
2. The repository working tree is on the `main` branch (or a release tag) and clean.
3. The operator has obtained the SN-LLC inaugural Q3-2026 public key bundle out-of-band — a YAML file containing exactly the field `pubkey_hex: <64 lowercase hex characters>`. The 64-hex string is the Ed25519 raw public key (32 bytes). The bundle is published by SN-LLC at its official channel; the operator verifies the source through SN-LLC's standard out-of-band channel (in-person, signed-email, or other operator-trusted channel) before importing.
4. The operator holds the `operator_key_id` short identifier they will use to attest the pinning event (e.g., `josh-2026-q3`). This string is recorded verbatim in the pinned file.
5. The operator has decided whether this is a *first pin* (no prior pinned key exists) or a *rotation* (prior pinned key exists and is being replaced).
   - **First pin:** `vault_shared/wpfa/sn_llc_pubkey.signed.yaml` is currently the placeholder scaffold (`pubkey_hex: ""`); proceed via §3.
   - **Rotation:** the file already carries a populated `pubkey_hex`; proceed via §4 (the co-signature path).
6. The terminal session is a real TTY. The pin verb refuses to run non-interactively; tests use the `--no-confirm-prompt` flag but production pinning **must not**.

# 3. First-pin procedure (no prior pinned key)

## 3.1 Stage the incoming SN-LLC pubkey bundle

Save the bundle to a local path you can reference. Convention:

```
~/sn_llc_pubkey_q3_2026.yaml
```

with file contents exactly:

```yaml
pubkey_hex: "<64-lowercase-hex>"
```

Verify by inspection that the file is well-formed YAML and that `pubkey_hex` is 64 lowercase hex characters.

## 3.2 Determine the pin attestation timestamp

Choose a UTC ISO-8601 'Z' timestamp the moment before you run the verb. Convention is to use `date -u +%Y-%m-%dT%H:%M:%SZ`. This value will be recorded as `pinned_at_utc` in the pinned file.

## 3.3 Run the pin verb

From the repository root:

```bash
.venv/bin/python3 -m pipeline.cli.tilth_wpfa registry pin-pubkey \
  --path ~/sn_llc_pubkey_q3_2026.yaml \
  --operator-key-id josh-2026-q3 \
  --pinned-at-utc 2026-MM-DDTHH:MM:SSZ
```

(Replace `josh-2026-q3` and the timestamp with the values from §2 step 4 and §3.2.)

## 3.4 Confirm at the TTY prompt

The verb prints:

```
Pin SN-LLC pubkey=<first-16-hex-chars>…? [yes/no]:
```

Type `yes` and press Enter to confirm. Any other input (including empty, `y`, `Y`) is rejected. The verb fails closed if the input is not exactly `yes`.

## 3.5 Verify the pinned file

After the verb prints `SN-LLC pubkey pinned: <path>`, inspect the resulting file:

```bash
cat vault_shared/wpfa/sn_llc_pubkey.signed.yaml
```

Expected fields:

```yaml
operator_key_id: josh-2026-q3
pinned_at_utc: '2026-MM-DDTHH:MM:SSZ'
pubkey_hex: '<the 64-hex pubkey you pinned>'
```

If any field is missing or the `pubkey_hex` does not match the bundle, the pin did not complete; restore the placeholder scaffold and retry from §3.1.

## 3.6 Add a ledger entry (operator audit trail)

Append one line to the operator audit ledger at `pipeline/institutional_memory/operator_attestation_ledger.jsonl` (create the file if it does not exist) capturing the pinning event:

```json
{"event": "wpfa_pubkey_pin_first", "operator_key_id": "josh-2026-q3", "pubkey_hex_prefix": "<first-16-hex>", "pinned_at_utc": "2026-MM-DDTHH:MM:SSZ", "source_bundle_path": "~/sn_llc_pubkey_q3_2026.yaml", "ledger_appended_at_utc": "<now>"}
```

This entry is the operator's own audit record. It is informational; it is not a runtime gate.

## 3.7 Smoke-test the pinned key against the active registry

If SN-LLC's inaugural Q3-2026 signed Coefficient Registry has already been imported (i.e., `vault_shared/wpfa/coefficient_registry/active.yaml` carries a populated `sn_llc_signature_ed25519`), verify the signature roundtrip:

```bash
.venv/bin/python3 -m pipeline.cli.tilth_wpfa registry update \
  --path vault_shared/wpfa/coefficient_registry/active.yaml
```

A clean exit code (0) plus the message `registry update staged` confirms the pinned pubkey verifies the active registry. Any of the F-WPFA-COEFFICIENT-* failure codes printed means either the registry or the pinned key is wrong — stop and triage before any cycle-close emission.

If the inaugural registry has not yet been imported, this smoke step is deferred to the registry-import procedure (separate runbook — see §6).

# 4. Rotation procedure (prior pinned key exists)

Rotation requires a **prior-key co-signature** over the new pubkey bytes. The trust assumption is that SN-LLC publishes the new pubkey **plus** a signature of the new pubkey bytes by the *prior* pinned pubkey. This forecloses the "attacker replaces pinned pubkey" attack at the on-disk file boundary.

## 4.1 Obtain the rotation bundle from SN-LLC

The bundle MUST carry both:

- the new `pubkey_hex` (64 lowercase hex)
- a `co_signed_by_prior_signature_hex` string — 128 lowercase hex characters — the Ed25519 signature of the raw new-pubkey bytes by the prior pinned pubkey

Stage these to two local files (or read them off the bundle into your shell):

```
~/sn_llc_pubkey_q4_2026.yaml         # carries: pubkey_hex
~/sn_llc_pubkey_q4_2026_cosig.hex    # carries: 128-hex on a single line
```

Verify both are well-formed before continuing.

## 4.2 Run the pin-pubkey verb with the co-signature flag

```bash
.venv/bin/python3 -m pipeline.cli.tilth_wpfa registry pin-pubkey \
  --path ~/sn_llc_pubkey_q4_2026.yaml \
  --operator-key-id josh-2026-q4 \
  --pinned-at-utc 2026-MM-DDTHH:MM:SSZ \
  --co-signed-by-prior-signature-hex "$(cat ~/sn_llc_pubkey_q4_2026_cosig.hex)"
```

The verb verifies the co-signature before prompting for confirmation. Verification failure prints `F-WPFA-COEFFICIENT-SIGNATURE-INVALID: prior-pubkey co-signature does not verify new pubkey` and exits non-zero — the prior pinned key is untouched. Re-stage and retry only after re-obtaining a valid co-signature from SN-LLC.

## 4.3 Confirm + verify + ledger

The TTY prompt, file inspection, and ledger entry steps mirror §3.4–§3.6. The ledger event field changes from `wpfa_pubkey_pin_first` to `wpfa_pubkey_pin_rotation`, and the entry adds:

```json
"prior_operator_key_id": "<the operator_key_id from the old pinned file>",
"prior_pubkey_hex_prefix": "<first-16-hex of old pubkey>",
"co_signed_by_prior_signature_hex_prefix": "<first-16-hex of the co-signature>"
```

## 4.4 v1.x rotation hardening (forward-binding marker; not active at v0.1)

Per §17.15.1 forward-binding (RT-03 / RT-C2-01 disposition), v1.x will introduce:

- atomic `registry_rotation.lock` file held during rotation, plus a 48h pubkey-rotation lock-out after rotation that defeats the "rotate-twice-during-cycle-close-race" attack
- a registry-rollback mutex held during any active cycle-close emission

These are not active at v0.1 single-client (A1+A4 threat model). At v0.1 the operator runs exactly one workflow at a time; serialization is by hand. Document the rotation event timing in the ledger entry to support future audits.

# 5. Failure modes and recovery

| Symptom | Probable cause | Recovery |
|---|---|---|
| `F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED` at receipt emission | `active.yaml` is still the scaffold placeholder | Import SN-LLC's inaugural signed registry (see §6). Pubkey pinning alone does not unblock emission. |
| `F-WPFA-COEFFICIENT-SIGNATURE-INVALID.pubkey_mismatch` at receipt emission | Pinned pubkey does not match the registry's signing key | Re-verify the source of the bundle. If a rotation event occurred at SN-LLC between when you obtained the registry and when you obtained the pubkey, use the rotation procedure (§4). |
| `F-WPFA-COEFFICIENT-SIGNATURE-INVALID: prior-pubkey co-signature does not verify new pubkey` during rotation | Co-signature is wrong, malformed, or signed with the wrong key | Re-obtain the rotation bundle from SN-LLC; verify the co-signature is fresh and against the exact new-pubkey bytes. Do not edit the prior pinned file by hand. |
| Verb refuses to start: `error: --yes / -y / --force / --auto-confirm rejected` | Operator passed a banned autoconfirm flag | Remove the banned flag. Production pinning must be interactive. Test fixtures use `--no-confirm-prompt`, NOT `--yes`. |
| Verb refuses to start: `error: requires TTY` | Command was piped or run from a non-TTY context (e.g., from inside an automated dispatcher) | Run from a real terminal session. White-glove pinning is operator-attested ceremony, not automation. |
| Pinned file appears empty / malformed after the verb prints success | File system race or write interrupted mid-flight | Restore the placeholder scaffold from version control (`git checkout -- vault_shared/wpfa/sn_llc_pubkey.signed.yaml`) and retry from §3.1. |

# 6. Companion procedure: importing SN-LLC's signed Coefficient Registry

Once the pubkey is pinned, the operator imports SN-LLC's inaugural Q3-2026 signed Coefficient Registry via `tilth wpfa registry update --path <path-to-signed-registry.yaml>`. That procedure has its own runbook (deferred; not in scope for this Track A tidy-up). The shape of the registry SN-LLC will publish is described in `pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md` and in the placeholder scaffold's leading comment at `vault_shared/wpfa/coefficient_registry/active.yaml`.

Until that import is complete, every WPFA cycle-close emission fails closed at `load_active()`. This is intentional: WPFA refuses to emit claims it cannot anchor to a signed, methodology-pinned baseline.

# 7. What this runbook does **not** cover

- Authoring or signing the Coefficient Registry itself (SN-LLC governance task, external to Golden Quill operator scope)
- Defining the methodology document published at `methodology_url` (SN-LLC governance task)
- Importing the signed Coefficient Registry into `active.yaml` (deferred companion runbook per §6)
- Operator-key generation or storage best practices (handled at white-glove appliance setup, not at WPFA pinning time)
- Buyer-facing PDF emission (`tilth wpfa pdf emit`) — covered by §17.7 of the blueprint and the white-glove playbook

# 8. Audit trail

After completing §3 or §4, the deployment carries:

- One populated file at `vault_shared/wpfa/sn_llc_pubkey.signed.yaml`.
- One ledger row at `pipeline/institutional_memory/operator_attestation_ledger.jsonl`.
- One historical pubkey copy at `vault_shared/wpfa/sn_llc_pubkey_history/<pinned_at_utc>.yaml` if the platform's history-mirroring extension is active (v1.x; not at v0.1 — the `_history/` directory is empty at v0.1).

These three artifacts together let any subsequent audit reconstruct who pinned what when, with what operator key, and (for rotations) under what co-signature.
