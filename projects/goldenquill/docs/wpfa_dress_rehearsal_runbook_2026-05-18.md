---
title: WPFA dress-rehearsal runbook — operator-only synthetic-registry end-to-end emission
filed: 2026-05-18
status: AUTHORED 2026-05-18 — operator runbook for dress-rehearsing the end-to-end WPFA emission flow against an operator-only synthetic Coefficient Registry before SN-LLC's inaugural Q3-2026 publication lands
applies_to: any v0.1 Beta deployment that wants confidence beyond the code-phase smoke + 88 WPFA tests before paid Beta launch
parent_locks:
  - pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md                                 # §17 v1 LOCKED 2026-05-11
  - pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md                     # §2 v7.4 LOCKED 2026-05-11
authority: PR #36 Track C scoping; operator greenlit 2026-05-18
cross_links:
  - docs/wpfa_status.md
  - docs/wpfa_white_glove_pubkey_pin_runbook_2026-05-18.md
  - docs/wpfa_sn_llc_signing_ceremony_runbook_2026-05-18.md
  - docs/wpfa_methodology_v1_draft_2026-05-18.md
risk: HIGH — this runbook involves pinning a NOT-FOR-BUYER operator-rehearsal pubkey AT THE SAME PATH the real SN-LLC pubkey will eventually pin to (`vault_shared/wpfa/sn_llc_pubkey.signed.yaml`). The operator MUST follow §7 cleanup before any subsequent attempt to load the real SN-LLC registry, or signature verification will fail-closed.
---

# 0. Purpose and risk acknowledgment

This runbook describes how to **dress-rehearse** the full WPFA end-to-end emission path against an operator-only synthetic Coefficient Registry, *before* SN-LLC has published its inaugural Q3-2026 signed registry. The goal is to surface any integration gap the code-phase smoke + 88 WPFA tests did not catch — including:

- weasyprint substrate behaviour against a real (not synthetic) Logfire span tree
- operator-attestation TTY ceremony in a live shell
- buyer-facing PDF rendering at real-data scale
- per-org isolation in the dashboard (Law 3) at real-data scale
- Cedar policy evaluation for `cycle_receipt_*` rules in production posture

**RISK.** This rehearsal pins a clearly-labeled operator-rehearsal pubkey at `vault_shared/wpfa/sn_llc_pubkey.signed.yaml` for the duration of the rehearsal. Unless §7 cleanup runs, the operator-rehearsal pubkey would remain pinned and any subsequent attempt to load the real SN-LLC registry would fail-closed via `F-WPFA-COEFFICIENT-SIGNATURE-INVALID.pubkey_mismatch`. Treat the cleanup step as mandatory, not optional.

**The artifacts emitted during the rehearsal are NOT for buyer use.** The synthetic registry uses an operator-held keypair labeled `operator_dress_rehearsal_only`. Any CycleReceipt or PDF emitted under this pubkey is for internal verification, not for board reports, grant reports, or sales conversations.

# 1. Preconditions

Before rehearsing:

1. **WPFA §17 v1 LOCKED + Code phase LANDED.** Both true as of 2026-05-11; verifiable via `docs/wpfa_status.md`.
2. **Repository on `main`** or a release tag, working tree clean.
3. **No production rehearsal target.** Ideally, choose an org that has no prior CycleReceipts. If using an org with prior receipts, those receipts emitted under (correctly) the scaffold-blocked Cycle Accountant — i.e., there are no prior receipts because Cycle Accountant was fail-closed.
4. **Real Logfire export available.** A captured Logfire span tree from a recent grant cycle on this deployment. This is the only mechanism by which the rehearsal exercises "real-data scale" — using a synthetic span tree only re-exercises the existing integration smoke.
5. **Operator-rehearsal keypair generated.** See §2.
6. **Cleanup scheduled.** Operator commits in writing (own audit ledger) when §7 cleanup will run. Convention: cleanup runs immediately after rehearsal capture, same session, before sign-off.
7. **TTY available.** Real terminal session; no automated dispatch.

# 2. Generate the operator-rehearsal keypair

Use `cryptography.hazmat` to generate a one-time Ed25519 keypair labeled for rehearsal-only:

```bash
python3 <<'PY'
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
priv = Ed25519PrivateKey.generate()
pub = priv.public_key()
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption, PublicFormat
priv_bytes = priv.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
pub_bytes = pub.public_bytes(Encoding.Raw, PublicFormat.Raw)
print("priv_hex (KEEP SECRET):", priv_bytes.hex())
print("pub_hex (will be pinned, NOT FOR BUYER):", pub_bytes.hex())
PY
```

Stash the private key in a local-only path (e.g., `~/.tilth_rehearsal/priv.hex` chmod 600). Do NOT commit it. Do NOT use a key you'd ever use for real signing.

# 3. Stage a synthetic Coefficient Registry signed with the rehearsal key

Author a registry file (e.g., `~/sn_llc_synthetic_rehearsal.unsigned.yaml`) using the draft template at `vault_shared/wpfa/coefficient_registry/draft_Q3_2026_unsigned.yaml`. Fill in the `<TBD>` placeholders with plausible-but-explicit-rehearsal values:

- `schema_version: "1.0.0"`
- `sn_llc_signing_key_id: "operator_dress_rehearsal_only"` (this string is the load-bearing label — it MUST contain `dress_rehearsal` somewhere so audit logs can filter it)
- Numeric coefficients: order-of-magnitude plausible. SN-LLC's eventual published values may differ ±50%; that's fine, the rehearsal is about flow not numbers.

Sign per `docs/wpfa_sn_llc_signing_ceremony_runbook_2026-05-18.md` §4, but using the rehearsal private key from §2 instead of SN-LLC's:

```bash
python3 <<'PY'
import json, yaml, sys
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

REG_PATH = "~/sn_llc_synthetic_rehearsal.unsigned.yaml"
PRIV_HEX = "<your-rehearsal-priv-hex-from-§2>"

import os
reg = yaml.safe_load(open(os.path.expanduser(REG_PATH)).read())
payload = {k: v for k, v in reg.items() if k != "sn_llc_signature_ed25519"}
canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

priv = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(PRIV_HEX))
sig = priv.sign(canonical).hex()
reg["sn_llc_signature_ed25519"] = sig
print(yaml.safe_dump(reg, sort_keys=True))
PY
```

Save the output as `~/sn_llc_synthetic_rehearsal.signed.yaml`.

# 4. Pin the rehearsal pubkey

Stage the pubkey bundle:

```bash
cat > ~/operator_rehearsal_pubkey.yaml <<EOF
pubkey_hex: "<rehearsal-pub-hex-from-§2>"
EOF
```

Pin it via `tilth wpfa registry pin-pubkey`:

```bash
.venv/bin/python3 -m pipeline.cli.tilth_wpfa registry pin-pubkey \
  --path ~/operator_rehearsal_pubkey.yaml \
  --operator-key-id rehearsal-only-2026-05-18 \
  --pinned-at-utc 2026-MM-DDTHH:MM:SSZ
```

Confirm `yes` at the TTY prompt. Verify the resulting file at `vault_shared/wpfa/sn_llc_pubkey.signed.yaml` carries the rehearsal pubkey + the `rehearsal-only-2026-05-18` operator key id.

**Audit-ledger entry (mandatory).** Append:

```json
{"event": "wpfa_pubkey_pin_rehearsal", "operator_key_id": "rehearsal-only-2026-05-18", "pubkey_hex_prefix": "<first-16-hex>", "pinned_at_utc": "...", "cleanup_required_by_utc": "<within-session-close>"}
```

to `pipeline/institutional_memory/operator_attestation_ledger.jsonl`. The `cleanup_required_by_utc` field is a discipline gate — if you find this ledger entry later without a paired `wpfa_pubkey_pin_rehearsal_cleanup` event before its deadline, that's an audit failure.

# 5. Import the synthetic registry

```bash
.venv/bin/python3 -m pipeline.cli.tilth_wpfa registry update \
  --path ~/sn_llc_synthetic_rehearsal.signed.yaml
```

The CLI:
- canonicalizes the file (per §3 of the signing-ceremony runbook)
- verifies the signature against the rehearsal pubkey just pinned
- copies the prior `active.yaml` to `vault_shared/wpfa/coefficient_registry/history/<sha3>.yaml`
- writes the new file to `vault_shared/wpfa/coefficient_registry/active.yaml`

Clean exit code = registry staged. Cycle Accountant load_active() will now succeed.

# 6. Run the end-to-end emission

## 6.1 Identify the Logfire export

Capture the Logfire span tree from the chosen real grant cycle. Convention:

```
~/.tilth_rehearsal/logfire_export_<cycle_id>.json
```

(Ensure this is a clean export — no embedded buyer-PII the operator wouldn't want in a CycleReceipt's audit trail.)

## 6.2 Invoke Cycle Accountant

Through the orchestrator's §5 v8 dispatcher cycle-close hook, OR directly via the `compose_receipt` DI seam for a controlled rehearsal:

```python
from pipeline.orchestrator.seats.wpfa.cycle_accountant import compose_receipt, CycleAccountantInput
# (Operator constructs input + spans + registry; refer to pipeline/orchestrator/seats/wpfa/cycle_accountant.py docstring)
```

A controlled `compose_receipt` invocation is easier for rehearsal because it surfaces gate failures explicitly without the orchestrator's surface wrapping.

The result, on success, is a populated CycleReceipt object. Without operator attestation it writes to `orgs/<slug>/vault/operational/cycle_receipts/<cycle_id>.json` as an internal-only receipt.

## 6.3 Operator-attest the receipt (optional rehearsal)

If the rehearsal scope includes the buyer-facing PDF path, the operator signs the receipt over its canonical-JSON bytes (excluding the signature field) using an operator Ed25519 keypair. The mechanism mirrors §4 of `docs/wpfa_white_glove_pubkey_pin_runbook_2026-05-18.md` but for receipt attestation — see §17.7.6 and the `cycle_receipt_operator_attestation` Cedar policy.

**Even during rehearsal, the operator MUST manually mark the resulting PDF as `[REHEARSAL — NOT FOR BUYER]`** — either by post-emission watermarking (a separate operator tool) or by adding a `[REHEARSAL]` prefix to the `--client-name` argument passed to `tilth wpfa pdf emit`. The emitter itself does not auto-watermark rehearsal artifacts; this is operator discipline.

## 6.4 Emit the PDF (if §6.3 attestation done)

```bash
.venv/bin/python3 -m pipeline.cli.tilth_wpfa pdf emit \
  --receipt-path orgs/<slug>/vault/operational/cycle_receipts/<cycle_id>.json \
  --client-name "[REHEARSAL] <client-display-name>" \
  --operator-display-name "<operator-name>" \
  --signing-key-id-display "operator_dress_rehearsal_only" \
  --methodology-url "https://sovereignnode.example/methodology/wpfa-v1"
```

The PDF lands at `orgs/<slug>/wpfa_artifacts/<cycle_id>.pdf`. **Mark it manually for non-buyer use** if your post-emission process does not auto-watermark.

# 7. Cleanup (MANDATORY — runs in the same session)

This is non-negotiable. Skipping cleanup leaves the operator-rehearsal pubkey pinned, which will fail-close any subsequent SN-LLC registry import.

## 7.1 Delete the rehearsal CycleReceipt and PDF

```bash
rm -f orgs/<slug>/vault/operational/cycle_receipts/<cycle_id>.json
rm -f orgs/<slug>/wpfa_artifacts/<cycle_id>.pdf
```

(Or move them to an explicit `_rehearsal_artifacts/` archive sub-directory clearly labeled NOT FOR BUYER.)

## 7.2 Restore the scaffold placeholder for the registry

```bash
git checkout -- vault_shared/wpfa/coefficient_registry/active.yaml
```

Verify the file now carries `schema_version: "0.0.0-scaffold"` and the empty signature placeholder.

## 7.3 Restore the scaffold placeholder for the pinned pubkey

```bash
git checkout -- vault_shared/wpfa/sn_llc_pubkey.signed.yaml
```

Verify the file now carries empty `pubkey_hex`.

## 7.4 Clean up rehearsal keypair material

```bash
rm -f ~/.tilth_rehearsal/priv.hex
rm -f ~/sn_llc_synthetic_rehearsal.{unsigned,signed}.yaml
rm -f ~/operator_rehearsal_pubkey.yaml
rm -f ~/.tilth_rehearsal/logfire_export_<cycle_id>.json
```

(Or move to a clearly-labeled offline archive if the operator wants to retain rehearsal materials for audit purposes — but not in any path that Tilth runtime reads.)

## 7.5 Cleanup audit-ledger entry

Append:

```json
{"event": "wpfa_pubkey_pin_rehearsal_cleanup", "operator_key_id": "rehearsal-only-2026-05-18", "cleanup_at_utc": "<now>", "artifacts_removed": ["<receipt>", "<pdf>", "<priv>", "<registry-files>"]}
```

to `pipeline/institutional_memory/operator_attestation_ledger.jsonl`. This is the paired event that closes the discipline gate from §4's ledger entry.

## 7.6 Verify scaffold state

Sanity-check that the workspace is back to scaffold:

```bash
.venv/bin/python3 -c '
from pathlib import Path
import yaml
reg = yaml.safe_load(Path("vault_shared/wpfa/coefficient_registry/active.yaml").read_text())
pub = yaml.safe_load(Path("vault_shared/wpfa/sn_llc_pubkey.signed.yaml").read_text())
assert reg["sn_llc_signature_ed25519"] == "", "registry signature not cleared"
assert reg["sn_llc_signing_key_id"] == "scaffold", "registry signing key id not scaffold"
assert pub["pubkey_hex"] == "", "pinned pubkey not cleared"
print("scaffold state restored")
'
```

# 8. What this rehearsal does NOT validate

- Real SN-LLC registry signature interop (the rehearsal uses an operator-held key, not SN-LLC's key)
- Real buyer's response to the PDF artifact (the rehearsal artifact is labeled NOT FOR BUYER and is not for distribution)
- Real coefficient correctness (the rehearsal uses plausible-but-not-measured values)
- Multi-operator rotation race conditions (forward-bound to v1.x per §17.15.1)
- Production methodology URL (the rehearsal uses the placeholder URL)

What it DOES validate (the rehearsal's actual value):
- The end-to-end emission flow against a REAL Logfire span tree (not the synthetic one used in the integration smoke)
- The buyer-facing PDF rendering at real-data scale
- The TTY ceremony for both pubkey pinning and registry update
- Operator-attestation flow against a real receipt
- The cleanup discipline itself — practicing the cleanup ahead of any production rehearsal that might inadvertently leave state behind

# 9. When to dress-rehearse

Operator discretion. Recommended once before the first paid Beta deployment cuts. NOT recommended for every release — the rehearsal is meaningful primarily as a one-time integration shake-out before SN-LLC's inaugural registry lands.

If the operator's confidence is already high (e.g., after PR #36's recon confirmed 88 WPFA tests + integration smoke + 0/0 lint failures), the rehearsal can be skipped in favor of running the first paid Beta deployment directly against the SN-LLC-published registry. The choice is an operator decision per PR #36 Q2.

# 10. Failure modes specific to rehearsal

| Symptom | Cause | Recovery |
|---|---|---|
| pin-pubkey verb rejects because prior pin exists | An earlier rehearsal didn't clean up | Run §7 first, then retry §4 |
| registry update verb prints `F-WPFA-COEFFICIENT-SIGNATURE-INVALID` | Rehearsal pubkey pinned in §4 doesn't match the keypair used to sign in §3 | Regenerate keypair (§2) ensuring you use the matching pub for §4 and priv for §3 |
| Cycle Accountant prints `F-WPFA-MODEL-COEFFICIENT-MISSING` | The Logfire export refers to a model_id not in the synthetic registry's `entries` | Add the missing model to the synthetic registry, re-sign (§3), re-import (§5) |
| Cycle Accountant prints `F-WPFA-COUNTERFACTUAL-INFLATION` | The synthetic registry's `baseline_model_id` is not in `entries` | Schema invariant — add the baseline entry to `entries` |
| PDF emitter prints `F-WPFA-OPERATOR-SIGNATURE-MISSING` | Receipt was emitted without operator attestation; PDF requires it | Re-emit receipt with operator attestation per §6.3 |
| PDF emitter prints `F-WPFA-PDF-CONFIDENTIAL-LEAK` | A field marked `confidential` in the classification register is reaching the rendered PDF | Either re-classify the field as `shareable`/`public` (deliberate operator decision via Classification Review), OR exclude it from the buyer-facing template |

# 11. Cross-references

- `docs/wpfa_status.md` — §17 status surface
- `docs/wpfa_white_glove_pubkey_pin_runbook_2026-05-18.md` — operator pubkey-pin ceremony (the real one)
- `docs/wpfa_sn_llc_signing_ceremony_runbook_2026-05-18.md` — SN-LLC's side of the inaugural publish
- `docs/wpfa_methodology_v1_draft_2026-05-18.md` — methodology skeleton
- `vault_shared/wpfa/coefficient_registry/draft_Q3_2026_unsigned.yaml` — shape template
- `pipeline/orchestrator/seats/wpfa/cycle_accountant.py` — Cycle Accountant module
- `pipeline/cli/tilth_wpfa.py` — CLI verbs
- `tests/integration/test_wpfa_end_to_end.py` — what the existing integration smoke validates (the floor of confidence)
