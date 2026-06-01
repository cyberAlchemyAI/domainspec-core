---
title: §2 v7.4 — Coefficient Registry signed-asset class amendment
filed: 2026-05-11
operator: Josh Inklovich
status: LOCKED 2026-05-11 — compound paired-commit (sibling 2/4) with §17 v1 + §4 v2.x.z F-WPFA-* amendment + §0.5 v19 paired-commit at the same `lock_timestamp_utc` per §6.17 Option-B. L-005 strict two-cycle CLOSED with FULL LIVE CROSS-FAMILY rigor (audit trail at `pipeline/validation/wpfa_thesis_2026-05-10/`). Tenth substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor.
parent_locks:
  - pipeline/blueprint/v0.1/section_02_v7_2_amendment.md                                            # §2 v7.2 LOCKED 2026-05-10 row 186 — SUB_KIND_REGISTRY + operational-data sub-kinds; precedent for signed-asset-class shape
  - pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md                                   # v7.0.4-M1 row 190 — canonical-JSON signing discipline
  - pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md                                     # v7.0.5 row 179 — Funder Intel DB curation slot (precedent for signed-asset publication mechanism)
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                                     # v7.0.7 row 180 — §6.1 SN-LLC router-template Ed25519 signing + white-glove-pinned pubkey + Trust-On-First-Use rotation; load-bearing precedent mirrored byte-for-byte
companion_amendments: [section_17_watts_per_funding_action.md, section_04_v2_x_z_wpfa_amendment.md, section_00_5_section_17_wpfa_amendment.md]
compound_lock_with: section_17_watts_per_funding_action.md v1 + section_04_v2_x_z_wpfa_amendment.md v2.x.z + section_00_5_section_17_wpfa_amendment.md v19
---

# §2.14 — Coefficient Registry signed-asset class

This amendment registers the **Coefficient Registry** as a new signed-asset class under v7.0.7 §6.1 trust discipline, parallel to the router-template publication mechanism. The Coefficient Registry carries per-model coefficients (dollars + watt-hours per million tokens) for every model Tilth can route to, plus per-hardware-SKU baseline metrics for local nodes.

**This is NOT a §2 sub-kind extension.** Sub-kinds live under `orgs/<slug>/vault/operational/<sub_kind>/` (per-client). The Coefficient Registry is **workspace-shared** — one registry per Tilth deployment, published by SN-LLC, read by the WPFA Cycle Accountant during cycle close. It is a new class of asset, distinct from operational records and from per-org configuration.

## §2.14.1 — Asset class definition

Signed-asset classes are workspace-shared, externally-published, cryptographically-verified data files. The router-template (per v7.0.7 §6.1) is the first member of this class; the Coefficient Registry is the second.

**Properties (binding for every signed-asset-class member):**
1. **Externally published.** SN-LLC (or a designated publisher) authors and publishes; the Tilth deployment consumes.
2. **Ed25519 signed.** Every release carries `<asset>_signature_ed25519` over canonical-JSON-encoded content (excluding the signature field itself).
3. **White-glove-pinned publisher pubkey.** Operator pins the publisher's Ed25519 public key at white-glove onboarding; future-rotation requires the new key co-signed by the previous (Trust-On-First-Use rotation, audited).
4. **PRE-load signature verify, fail-closed.** Before any asset content is used in pipeline logic, the Logician verifies the signature against the pinned pubkey. Failure → deployment stays on prior pinned version; no auto-update.
5. **Per-deployment opt-in.** Deployments don't auto-update — operator opts in per release via a TTY-gated CLI verb (per Intake §11.7 precedent; no `--yes`/`--auto-confirm`/`--force` flags; argparse-level rejection).
6. **Quarterly cadence (soft) + 7-day emergency.** Publisher commits to quarterly review at minimum; emergency updates (model deprecation, coefficient correction, security) follow a 7-day discipline.
7. **Rollback protocol.** Every published asset carries `rollback_pointer` to the prior version's SHA3-512. Operator-initiated rollback re-pins the prior version. PRE-gate: rollback target SHA3 MUST resolve to an asset on disk under `history/` (else fail-closed via the asset class's specific `*_ROLLBACK_INVALID` code).
8. **Canonical-JSON signing scope.** The signature covers a canonical-JSON serialization of the asset, excluding the signature field itself. Canonical-JSON discipline per v7.0.4-M1 §2.4 (sorted keys, no insignificant whitespace, UTF-8, no Unicode normalization side-effects).

The Coefficient Registry inherits all eight properties from the signed-asset class and adds three Registry-specific PRE-gate predicates (§2.14.4 below).

## §2.14.2 — CoefficientRegistry + CoefficientEntry Pydantic shapes

Module: `pipeline/vault/sub_kinds/coefficient_registry.py` (NEW). Tests: `tests/vault/sub_kinds/test_coefficient_registry.py`.

```python
@dataclass(frozen=True, kw_only=True)
class CoefficientRegistry:
    schema_version: str                                 # semver
    quarter: str                                        # e.g., "Q3-2026"
    published_at: str                                   # UTC ISO-8601 'Z'
    sn_llc_signature_ed25519: str                       # hex Ed25519 signature over canonical-JSON of all other fields
    sn_llc_signing_key_id: str                          # opaque key identifier; rotates per A12 crypto-agility envelope
    baseline_model_id: str                              # the quarter's flagship counterfactual reference (e.g., "claude-sonnet-4-6")
    entries: tuple[CoefficientEntry, ...]               # one per model
    methodology_url: str                                # stable URL where coefficients + citations + methodology document live
    rollback_pointer: str | None                        # optional SHA3-512 hex of the prior registry version


@dataclass(frozen=True, kw_only=True)
class CoefficientEntry:
    model_id: str                                       # canonical model identifier — MUST match Logfire span model_id
    is_local: bool
    hardware_sku: str | None                            # "apple_m3_ultra" | "amd_gx_10" | "nvidia_spark" | None for cloud
    dollars_per_million_input_tokens_minor_units: int   # A12 — int minor units per million
    dollars_per_million_output_tokens_minor_units: int
    watt_hours_per_million_input_tokens_micro: int      # A12 — int micro-Wh per million
    watt_hours_per_million_output_tokens_micro: int
    idle_watts_baseline_micro: int | None               # local only — baseline draw at idle
    peak_watts_under_load_micro: int | None             # local only — peak draw during inference
    citation_url: str                                   # publisher's source for this coefficient
    measurement_date: str                               # UTC 'YYYY-MM-DD' (LOCKED per OQ-G default — date-only)
    measurement_methodology_url: str                    # detailed methodology document
```

## §2.14.3 — Invariants (`__post_init__`)

**CoefficientRegistry:**
1. `schema_version` matches `^\d+\.\d+\.\d+$` (semver).
2. `quarter` matches `^Q[1-4]-\d{4}$`.
3. `published_at` matches `^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$`.
4. `sn_llc_signature_ed25519` is non-empty hex; length matches Ed25519 raw signature (128 hex chars = 64 bytes).
5. `sn_llc_signing_key_id` is non-empty.
6. `baseline_model_id` is non-empty AND resolves to a `CoefficientEntry` in `entries` (any entry where `entry.model_id == baseline_model_id`).
7. `entries` is non-empty; each `model_id` is unique across the tuple.
8. `methodology_url` is non-empty AND matches a URL regex (`^https?://`).
9. `rollback_pointer`, if non-None, is 128-hex-char SHA3-512.

**CoefficientEntry:**
1. `model_id` non-empty.
2. All `dollars_per_million_*` and `watt_hours_per_million_*` fields are non-negative integers.
3. If `is_local == True`, `hardware_sku` is non-None AND `idle_watts_baseline_micro` + `peak_watts_under_load_micro` are non-None and non-negative integers.
4. If `is_local == False`, `hardware_sku` is None AND `idle_watts_baseline_micro` is None AND `peak_watts_under_load_micro` is None.
5. `citation_url` matches `^https?://`.
6. `measurement_date` matches `^\d{4}-\d{2}-\d{2}$` (date-only per OQ-G default).
7. `measurement_methodology_url` matches `^https?://`.

## §2.14.4 — Trust mechanism (mirrors v7.0.7 §6.1 router-template byte-for-byte)

The following discipline is binding and Thesis-overrideable only by escalation. Deviation from v7.0.7 §6.1 is a defect:

1. **Signing scope.** SN-LLC signs the canonical-JSON-encoded registry over **all fields except `sn_llc_signature_ed25519`**. Canonical-JSON per v7.0.4-M1 §2.4 (sorted keys; no insignificant whitespace; UTF-8; no Unicode normalization side-effects). The signing payload uses a fixed serialization order matching the Pydantic `@dataclass` field order — implementation MUST stably sort keys lexicographically. **Loader-side discipline (Cycle 1 RT-01/RT-02 closure):** the `load_active` loader reads via `json.loads` only; YAML anchor expansion, duplicate keys, and YAML-specific tags are forbidden at the loader. The `.yaml` file extension is a naming convention; on-disk contents MUST be canonical-JSON-parsable. Any YAML-anchor abuse attack surface is closed at the loader boundary by the JSON parser's strict mode (no anchors, no merge keys, no implicit type coercion). The signature is verified over the EXACT bytes the loader will use to instantiate the dataclass — there is no re-serialization gap between verification and use. **Cycle 2 RT-C2-04 fold-in:** files containing characters outside the JSON lexical grammar — including comment prefixes (`#`, `//`), YAML tags (`!!`), or any non-JSON tokens — fail closed at `json.loads(...)` with `F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED` (the signature cannot have been computed over invalid JSON). Operator-side hygiene: the `tilth wpfa registry update` CLI rejects any candidate file that fails JSON strict parse before staging it.
2. **Verification.** Golden Quill verifies the signature against the white-glove-pinned SN-LLC public key BEFORE loading any registry update. Verification uses `pynacl` Ed25519 primitives (added to Golden Image build per ADR-001 substrate-frozen discipline).
3. **Pinned pubkey location.** `vault_shared/wpfa/sn_llc_pubkey.signed.yaml` — set at white-glove onboarding. Format: `pubkey_hex: <hex>`, `pinned_at_utc: <iso>`, `pinned_by_operator_ed25519: <hex>` (operator self-attests the pinning event with their own Ed25519 over the pubkey bytes).
4. **Pubkey rotation.** New SN-LLC pubkey MUST be co-signed by the prior SN-LLC pubkey (audit trail in `vault_shared/wpfa/sn_llc_pubkey_history/<rotation_index>.yaml`). Trust-On-First-Use rotation per v7.0.7 §6.1. **Cycle 1 RT-03 partial fold (v1.x amendment-realization marker):** at v0.1 single-client (A1+A4), the rotation race window is bounded by the operator's mediation of the rotation event (the operator authorizes the new pubkey through the TTY-gated `tilth wpfa registry pin-pubkey` CLI verb). A 48-hour minimum lock-out period between dual-signed publication and active-use is **forward-bound to v1.x WPFA amendment** for multi-tenant scenarios where multiple operators may race the rotation. The v0.1 floor remains the dual-signature requirement.
5. **Failure mode.** Any verification failure fails-closed via `F-WPFA-COEFFICIENT-SIGNATURE-INVALID` (see §4 v2.x.z). Deployment stays on previous pinned version. No auto-fallback to an unsigned variant. Sub-tags `.pubkey_mismatch`, `.signature_bytes_invalid`, `.canonical_json_mismatch`.

## §2.14.5 — On-disk layout

```
vault_shared/wpfa/
├── coefficient_registry/
│   ├── active.yaml                    # current pinned version; symlink-or-content-copy of one history file
│   └── history/
│       └── <sha3_512_hex>.yaml        # full history; receipts may reference historical versions for re-emission audits
├── sn_llc_pubkey.signed.yaml          # pinned SN-LLC pubkey (white-glove sets at onboarding)
└── sn_llc_pubkey_history/             # rotation audit trail
    └── <rotation_index>.yaml          # prior-key-co-signs-new-key entries
```

## §2.14.6 — Update CLI surface (Code-phase realization)

Operator-facing CLI verbs (always-local; TTY-gated per Intake §11.7 four-layer defense):

- `tilth wpfa registry update --path <path-to-new-registry.yaml>` — validates the proposed registry's signature against the pinned pubkey, computes SHA3-512, copies into `history/`, updates `active.yaml`, writes audit-ledger entry. Fails closed on signature-invalid or schema-invalid.
- `tilth wpfa registry rollback --to <sha3_512_hex>` — validates target SHA3 resolves under `history/`, re-pins `active.yaml` to the target, writes audit-ledger entry recording the rollback reason. Fails closed if target SHA3 absent.
- `tilth wpfa registry pin-pubkey --path <path-to-pubkey.yaml>` — only callable at white-glove onboarding OR via co-signed rotation flow; refuses if `sn_llc_pubkey.signed.yaml` already exists AND new pubkey is NOT co-signed by the prior key. TTY-gated.

All three are non-bypassable (no `--yes`/`--force`/`--auto-confirm` flags). argparse-level rejection enforces.

## §2.14.7 — Update cadence

- **Quarterly cadence** (soft commitment) — SN-LLC reviews and republishes at minimum once per quarter.
- **7-day emergency** — for model deprecations, coefficient corrections, security responses. Mirrors v7.0.7 §6.1 router-template emergency cadence.
- **Per-deployment opt-in** — deployments don't auto-update; operator pulls each release.

## §2.14.8 — Rollback protocol (binding)

- Every published registry carries `rollback_pointer` to the prior version's SHA3-512 (computed from canonical-JSON of the prior registry).
- Inaugural registry (Q3-2026 seed) has `rollback_pointer == None` — no prior version exists.
- Operator-initiated rollback (`tilth wpfa registry rollback --to <sha3>`) re-pins the prior registry as `active.yaml`.
- PRE-gate: rollback target SHA3 MUST resolve to a registry on disk under `history/`. Absent → fail-closed via `F-WPFA-COEFFICIENT-ROLLBACK-INVALID`.
- **Rollback authority (LOCKED per OQ-3 default):** operator-direct with audit-ledger entry. SN-LLC co-signed acknowledgment is NOT required (operator owns the deployment).

## §2.14.9 — Receipt-vs-registry version interplay

- Receipts pin the `coefficients_registry_version` at emission time.
- A re-emission against the same `cycle_id` MAY pin a different registry version IF the operator provides an admin-risk-ledger reference justifying the recomputation.
- PRE-gate: receipts with different `coefficients_registry_version` than the currently-active registry MUST carry an admin-risk-ledger reference (else `F-WPFA-REGISTRY-DRIFT.registry_version_mismatch_no_ledger_entry` — sub-tag advisory).

## §2.14.10 — Inaugural registry seed (Q3-2026)

SN-LLC publishes the inaugural Q3-2026 Coefficient Registry on or before the first Beta deployment. Seed at `vault_shared/wpfa/coefficient_registry/active.yaml` with rollback_pointer=null and methodology_url pointing to the canonical SN-LLC-maintained methodology document.

Expected entries (at minimum) for the inaugural registry:
- `claude-sonnet-4-6` (baseline_model_id; cloud; Anthropic-published coefficients).
- `claude-opus-4-6` (cloud; Anthropic).
- `gemini-2.5-pro` (cloud; Google).
- `llama-3.3-70b-versatile` via Groq (cloud).
- `openai/gpt-oss-120b` via Groq (cloud).
- `local/m3-ultra-llama-70b` (local; hardware_sku="apple_m3_ultra").
- `local/gx-10-llama-70b` (local; hardware_sku="amd_gx_10").
- `local/spark-llama-70b` (local; hardware_sku="nvidia_spark").

(The inaugural seed file at `vault_shared/wpfa/coefficient_registry/active.yaml` is a scaffold at compound-LOCK time; SN-LLC's first published values land at first Beta deployment cut.)

## §2.14.11 — Loader interface

```python
def load_active(
    *,
    registry_path: str,
    pinned_pubkey_path: str,
) -> CoefficientRegistry:
    """Load and verify the active Coefficient Registry.

    Fails closed on:
      - Missing or unreadable file (raises CoefficientRegistryUnreadableError).
      - Signature absent (raises CoefficientRegistryUnsignedError → F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED).
      - Signature invalid (raises CoefficientSignatureInvalidError → F-WPFA-COEFFICIENT-SIGNATURE-INVALID).
      - Schema invariants violated (raises CoefficientSchemaInvalidError).

    Returns a frozen CoefficientRegistry on success.
    """
```

Loader is always-local. No network access. Tests inject deterministic registry content for unit + integration tests.

## §2.14.12 — Audit trail

See §17.18.

---

# Changelog

- **2026-05-11 §2 v7.4 LOCKED** — Coefficient Registry signed-asset class introduced. Compound paired-commit with §17 v1 + §4 v2.x.z + §0.5 v19. Trust mechanism mirrors v7.0.7 §6.1 router-template byte-for-byte (Thesis Cycle 1 + Cycle 2 verified). Inaugural Q3-2026 seed scaffolded at `vault_shared/wpfa/coefficient_registry/active.yaml`.
