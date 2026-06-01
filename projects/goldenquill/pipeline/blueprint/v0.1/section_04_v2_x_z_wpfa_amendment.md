---
title: §4 v2.x.z — Logician F-WPFA-* failure-code family amendment
filed: 2026-05-11
operator: Josh Inklovich
status: LOCKED 2026-05-11 — compound paired-commit (sibling 3/4) with §17 v1 + §2 v7.4 Coefficient Registry + §0.5 v19 paired-commit at the same `lock_timestamp_utc` per §6.17 Option-B. L-005 strict two-cycle CLOSED with FULL LIVE CROSS-FAMILY rigor (audit trail at `pipeline/validation/wpfa_thesis_2026-05-10/`). Tenth substantive v0.1+v0.2 round to LOCK at FULL live cross-family rigor.
parent_locks:
  - pipeline/blueprint/v0.1/section_04_v2_x_amendment.md                                            # §4 v2.x LOCKED 2026-05-10 rows 193/194 — F-CLASS-* dormant primitives + v7.0.4-M1 corrective predicates; format pattern this amendment mirrors
  - pipeline/blueprint/v0.1/section_04_v2_x_1_amendment.md                                          # §4 v2.x.1 LOCKED 2026-05-10 row 199 — narrow-corrective amendment precedent for new code family
  - pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md                                   # v7.0.4-M1 row 190 — Decimal mandate (extended to energy per §17.3.5)
  - pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md                                  # §17 v1 LOCKED 2026-05-11 (paired sibling 1/4)
  - pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md                       # §2 v7.4 LOCKED 2026-05-11 (paired sibling 2/4)
companion_amendments: [section_17_watts_per_funding_action.md, section_02_v7_4_coefficient_registry_amendment.md, section_00_5_section_17_wpfa_amendment.md]
compound_lock_with: section_17_watts_per_funding_action.md v1 + section_02_v7_4_coefficient_registry_amendment.md v7.4 + section_00_5_section_17_wpfa_amendment.md v19
---

# Amendment intent

Register the F-WPFA-* failure-code family in §4 Logician. Twelve failure codes; ten realization modules (the three coefficient-registry-validation codes consolidate into a single module per §6 OQ-4 default). Predicate bodies are **LIVE at LOCK** per operator directive (NOT NotImplementedError stubs — distinct from prior dormant-binding amendments like §4 v2.x F-CLASS-* + §4 v2.x.2 F-REFLECTION-* HORIZON rows).

This is the **first §4 amendment with LIVE predicate bodies at LOCK time.** Prior amendments declared signatures with stubs; the Code phase realized bodies. WPFA's v0.1 Beta scope LOCK includes Cycle Accountant module + LIVE predicates because the buyer-facing PDF artifact is a sales-lever for first paid Beta deployment.

# §5.1.WPFA — F-WPFA-* family — ACTIVE BINDING

All twelve codes are ACTIVE at this LOCK. Module bodies live at `pipeline/logician/gates/f_wpfa_*.py`. Tests at `tests/logician/gates/test_f_wpfa_*.py`. Cedar policy extensions at `pipeline/vault/policies/operational_subkinds.cedar`.

## §5.1.WPFA.1 — `F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED` (PRE-load, P0)

**Trigger.** Coefficient Registry loaded without a `sn_llc_signature_ed25519` field, or field is empty / not hex / wrong length for Ed25519 raw signature (128 hex chars).

**Predicate signature.**
```python
def f_wpfa_coefficient_registry_unsigned(
    registry_yaml_path: str,
) -> GateOutcome: ...
```

**Realization module.** `pipeline/logician/gates/f_wpfa_coefficient_registry_validation.py` (consolidated per OQ-4 default with F-WPFA-COEFFICIENT-SIGNATURE-INVALID + F-WPFA-COEFFICIENT-ROLLBACK-INVALID).

**M13.** Audited bypass permitted with HIGH-severity admin-risk ledger entry.

**Mirrors.** `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` (v7.0.7) at the registry layer.

## §5.1.WPFA.2 — `F-WPFA-COEFFICIENT-SIGNATURE-INVALID` (PRE-load, P0)

**Trigger.** Registry signature does not verify against white-glove-pinned SN-LLC pubkey. Deployment stays on prior pinned version.

**Sub-tags.** `.pubkey_mismatch`, `.signature_bytes_invalid`, `.canonical_json_mismatch`.

**Realization module.** Consolidated in `f_wpfa_coefficient_registry_validation.py`.

**M13.** Audited bypass permitted with HIGH-severity admin-risk ledger entry.

## §5.1.WPFA.3 — `F-WPFA-COEFFICIENT-ROLLBACK-INVALID` (PRE-load, HIGH)

**Trigger.** Rollback target SHA3 does not resolve to a registry on disk under `history/`.

**Realization module.** Consolidated in `f_wpfa_coefficient_registry_validation.py`.

**M13.** Audited bypass permitted with HIGH-severity admin-risk ledger entry.

## §5.1.WPFA.4 — `F-WPFA-MODEL-COEFFICIENT-MISSING` (PRE-emission, HIGH)

**Trigger.** Span tree references a `model_id` that has no entry in the loaded Coefficient Registry.

**Sub-tags.** `.unknown_model_id`, `.deprecated_model_referenced`.

**Predicate signature.**
```python
def f_wpfa_model_coefficient_missing(
    span_model_ids: Iterable[str],
    registry: CoefficientRegistry,
) -> GateOutcome: ...
```

**Realization module.** `pipeline/logician/gates/f_wpfa_model_coefficient_missing.py`.

**M13.** Audited bypass permitted; common cause is operator added a new local model SKU without updating the registry.

## §5.1.WPFA.5 — `F-WPFA-BASELINE-MISSING` (PRE-emission, HIGH)

**Trigger.** Counterfactual baseline not set for the cycle's quarter (registry's `baseline_model_id` is unset or does not resolve to an entry in the registry's `entries` tuple).

**Realization module.** `pipeline/logician/gates/f_wpfa_baseline_missing.py`.

**M13.** Audited.

## §5.1.WPFA.6 — `F-WPFA-SPAN-PROVENANCE-MISSING` (PRE-emission, HIGH)

**Trigger.** Any quantitative claim in the receipt (`actual.dollars_total`, per-model row, `counterfactual.*`, `delta.*`, PDF rendered claim) does not carry an originating `trace_id`/`span_id` in `span_provenance.per_claim_span_ids`.

**Sub-tags.** `.no_trace_id`, `.trace_id_unresolvable_in_logfire`, `.claim_key_unmapped`, `.pdf_claim_unlinked` (per OQ-7 default — F-WPFA-PDF-AUDITABILITY-BROKEN folded in as sub-tag).

**Cross-reference (per Path B naming reconciliation, `pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md`):** sibling pattern to a forthcoming `F-PACKET-SPAN-PROVENANCE-MISSING` (Reflection Packet artifact, scope deferred per Q2). The §15 Archivist Reflection sub-mode's F-REFLECTION-* family does NOT contain this code; the Reflection Packet's family is `F-PACKET-*`.

**Realization module.** `pipeline/logician/gates/f_wpfa_span_provenance_missing.py`.

**M13.** Audited.

## §5.1.WPFA.7 — `F-WPFA-COUNTERFACTUAL-INFLATION` (PRE-emission, P0)

**Trigger.** Counterfactual computed using a baseline model NOT actually in the SN-LLC-signed registry. PRE-gate verifies `baseline_model_id` matches `coefficient_registry.baseline_model_id` exactly.

**Realization module.** `pipeline/logician/gates/f_wpfa_counterfactual_inflation.py`.

**M13.** **NOT bypassable for buyer-attested receipts.** Internal-only receipts permit M13 with HIGH-severity admin-risk entry. This is the structural audit-integrity gate.

**Cycle 1 RT-04 disposition (BOUNDED-BY-A4).** The proposed "per-quarter baseline-whitelist" mitigation would require an additional signed asset published by SN-LLC — recursive trust chain that does not improve the v0.1 trust floor. The fundamental v0.1 trust model is: operator pins SN-LLC pubkey at white-glove (A4); SN-LLC publishes registries with their `baseline_model_id` selection; the operator audits SN-LLC's publication choices via the methodology document at the published URL. Compromise of SN-LLC's signing key breaks the entire trust chain regardless of additional whitelist layers. **Forward-design marker (v2 multi-tenant):** deployment-side baseline-whitelist as an operator-overridable filter on registry contents — operator declares "I will only accept baseline ∈ {claude-sonnet-4-6, gemini-2.5-pro}" at white-glove + per-grant SP0 override. Lands in Section O.5 v2 multi-tenant mitigation track.

## §5.1.WPFA.8 — `F-WPFA-OPERATOR-SIGNATURE-MISSING` (PRE-PDF-emit, HIGH)

**Trigger.** Buyer-facing PDF emission attempted without `signed_by_operator_ed25519` set on the source receipt.

**Sub-tag.** `.pdf_emission_without_attestation`.

**Realization module.** `pipeline/logician/gates/f_wpfa_operator_signature_missing.py`.

**M13.** **NOT permitted** (per OQ-E default — this is the structural attestation boundary; M13 would defeat the purpose).

## §5.1.WPFA.9 — `F-WPFA-DIMENSION-UNSUPPORTED` (PRE-emission, HIGH)

**Trigger.** Receipt asserts a dimension (water/CO2) not in `dimensions_active` for this schema version, OR `dimensions_active` at v0.1 contains anything other than `("dollars", "energy")`.

**Sub-tags.** `.water_at_v0_1`, `.co2_at_v0_1`, `.unknown_dimension`.

**Realization module.** `pipeline/logician/gates/f_wpfa_dimension_unsupported.py`.

**M13.** Audited.

## §5.1.WPFA.10 — `F-WPFA-REGISTRY-DRIFT` (POST-load advisory, MEDIUM)

**Trigger.** Local hardware measurement deviates >X% from SN-LLC registry coefficient for the same SKU (advisory threshold operator-tunable; default X=20%).

**Sub-tags.** `.idle_watts_drift`, `.peak_watts_drift`, `.watt_hours_per_million_drift`, `.registry_version_mismatch_no_ledger_entry` (per §17.16 receipt-vs-registry-version interplay).

**Realization module.** `pipeline/logician/gates/f_wpfa_registry_drift.py`.

**M13.** Not needed (advisory).

## §5.1.WPFA.11 — `F-WPFA-SCHEMA-INVALID` (PRE-write + POST-read, HIGH)

**Trigger.** Schema validation failure (any of the 17 CycleReceipt invariants in §17.3.4) at write OR at decode round-trip.

**Sub-tags.** `.numeric_field_float`, `.classification_register_version_invalid`, `.dimensions_active_invalid`, `.per_model_aggregate_mismatch`, `.delta_arithmetic_mismatch`, `.semver_version_invalid`, `.schema_drift_advisory` (forward-compat tolerant-reader path).

**Realization module.** `pipeline/logician/gates/f_wpfa_schema_invalid.py`. Mirrors `F-OPERATIONAL-SCHEMA-INVALID` (§2 v7.2 §7).

**M13.** Audited.

## §5.1.WPFA.12 — `F-WPFA-CROSS-ORG-LEAK` (PRE-write, P0)

**Trigger.** Any CycleReceipt write whose path resolves to `orgs/<other_slug>/vault/operational/cycle_receipts/...` where `<other_slug>` differs from the receipt's `org_slug` field.

**Realization module.** `pipeline/logician/gates/f_wpfa_cross_org_leak.py`. Defense-in-depth on top of `operational_org_isolation.cedar` Rule 1.

**M13.** **NOT bypassable** (Law 3 structural gate).

## §5.1.WPFA.13 — `F-WPFA-PDF-CONFIDENTIAL-LEAK` (PRE-PDF-emit, P0)

**Trigger.** Buyer-facing PDF emission attempts to render any field value whose classification register entry is `confidential`.

**Sub-tags.** `.confidential_field_in_pdf`, `.classification_register_unread_at_emit`.

**Realization module.** `pipeline/logician/gates/f_wpfa_pdf_confidential_leak.py`.

**M13.** **NOT bypassable for buyer-attested artifacts** (Law 3 + v7.0.7 structural gate).

# §5.1.WPFA.META — F-CLASS-COVERAGE-INCOMPLETE META gate exclusion

Per §6 OQ-6 default, F-WPFA-* is **EXCLUDED** from the F-CLASS-COVERAGE-INCOMPLETE META gate's `REQUIRED_F_CLASS_CODES` registry. Rationale: F-WPFA-* is its own family with its own gate ownership; the META gate is scoped to F-CLASS-* (classification-routing). Including F-WPFA-* would conflate two orthogonal families.

Documentary note for future amendments: if a `F-WPFA-COVERAGE-INCOMPLETE` META gate is later required (own-family L-006 dormant-binding pattern), it goes in §5.1.WPFA.META as a new code, not as an extension of F-CLASS-COVERAGE-INCOMPLETE.

# §5.1.WPFA.A1A4 — A1+A4 boundary conditions (Cycle 1 RT-09 + RT-14 disposition)

Three Cycle-1 Red Team findings (RT-09 Cedar principal-attribute spoofing, RT-14 rollback race during cycle-close, RT-03 pubkey rotation race) are **bounded by v0.1 architecture A1 (single-client threat model) + A4 (operator-trusted preflight)**:

- **RT-09 (Cedar principal-attribute spoofing).** At v0.1 single-client, the operator IS the principal. There are no untrusted principals to spoof. `wpfa_dashboard_workspace_aggregate` is operator-bound by definition (only the operator can launch the dashboard CLI). Cryptographic binding of `org_slug` attribute to principal identity is a **v2 multi-tenant track** mitigation that activates when Stage-2+ adds untrusted-principal scenarios. Lands in Section O.5 v2 multi-tenant mitigation track.
- **RT-14 (rollback race during cycle-close).** At v0.1 single-client, the operator runs exactly one workflow at a time; rollback cannot interleave with active emission. Forward-bound to **v1.x WPFA amendment** as a registry-version mutex lock during cycle-close.
- **RT-03 (pubkey rotation race).** §2 v7.4 §2.14.4 #4 already mandates dual-signature. Forward-bound to **v1.x WPFA amendment** as a 48h minimum lock-out period for multi-tenant scenarios.

These dispositions follow the row-179 + row-180 + row-190 + row-196/197 precedent: bounded-by-arch-axiom findings are NOT structural blockers at LOCK; they ARE forward-design markers that activate at the architecture-axiom-relaxation transition (Stage 1 → Stage 2).

**Cycle 2 RT-C2-01 fold-in (parallel rotation race).** An operator may accidentally launch two `tilth wpfa registry pin-pubkey` (or `tilth wpfa registry rotate-signing-key`) CLI invocations concurrently in separate terminals. At v0.1 single-client A1, this is operator-self-defeating (the operator is the only race participant; the dual-signature requirement plus TTY-gating already serialize most paths). Forward-binding marker for **v1.x WPFA amendment**: atomic `registry_rotation.lock` filesystem lock acquired before any rotation step, released after dual-signature + 48h lock-out period record completes. v0.1 ships without the explicit lock; the threat model bounds the residual race window.

**Cycle 2 NEW probes disposition (row-170 transparent pattern):**

| Probe | Severity | Disposition | Action |
|---|---|---|---|
| RT-C2-01 | HIGH P0 | FOLDED via documentary edit + v1.x marker | §5.1.WPFA.A1A4 above |
| RT-C2-02 | MED | FOLDED via documentary edit | §17.7.6 sub-tag extension |
| RT-C2-03 | MED | FOLDED via documentary edit | §17.5.3 logfire export canonicalization |
| RT-C2-04 | LOW | FOLDED via documentary edit | §2.14.4 #1 reinforced |
| RT-C2-05 | HIGH P0 | **FIX-IN-PLACE LANDED at LOCK** | §17.3.4 invariant 1 + `pipeline/vault/sub_kinds/cycle_receipts.py` `_CYCLE_ID_RE` enforced; regression test at `tests/vault/sub_kinds/test_cycle_receipts.py::TestSchemaInvariants::test_cycle_id_rejects_path_separators` extended + new test for strict regex |

# §5.1.WPFA.DEFENSE — Three-layer defense pattern for buyer-PDF emission

Buyer-facing PDF emission carries three structural defense layers (per §11.7 four-layer autopromote precedent, narrowed to three for v0.1 — TTY-gating is the fourth layer at the CLI verb invocation):

1. **AST-lint** — `R-WPFA-NO-AUTOSIGN`: ban any callsite that calls `pdf_emitter.emit()` without first reading the operator-signed receipt's `signed_by_operator_ed25519`. Module: `pipeline/linting/r_wpfa_no_autosign.py`.
2. **Cedar policy** — `cycle_receipt_operator_attestation` requires non-None operator signature; deny default.
3. **Runtime gate** — `F-WPFA-OPERATOR-SIGNATURE-MISSING` PRE-emission predicate.

(Fourth layer at the CLI: `tilth wpfa pdf emit` is TTY-gated; argparse-level rejection of `--yes`/`--force`/`--auto-confirm`.)

# §5.1.WPFA.AST_LINT — AST-lint rule extensions

Two new AST-lint rules ship with this amendment:

1. **`R-WPFA-NO-AUTOSIGN`** — defined above. Prevents bypassing operator attestation.
2. **`R-WPFA-DECIMAL-MANDATE-ENERGY`** — extends A12 Decimal-mandate AST-lint rule to ban `float` annotations on field names matching the regex `(_minor_units|_micro|_saved)$`. Mirrors existing R3-equivalent currency rule per v7.0.4-M1 §6. Module: `pipeline/linting/r_wpfa_decimal_mandate_energy.py`.

# §5.1.WPFA.AUDIT — Audit trail

See `pipeline/validation/wpfa_thesis_2026-05-10/`.

# §5.1.WPFA.NOTES — Notes for downstream consumers

- The F-WPFA-* family is registered in §0.5 v19 paired-commit (one row per code = 13 rows; plus 2 AST-lint rule rows = 15 failure-code-class rows).
- The F-CIC-CLC-COUPLING-VIOLATION-class regression test (per `pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md` §5) MUST verify: F-WPFA-* codes belong only to §17 WPFA; no F-* code crosses seat ownership.
- Sibling-family naming reconciliation: F-REFLECTION-* belongs to §15 Archivist Reflection sub-mode; F-PACKET-* (when authored) belongs to forthcoming §16 Reflection Packet; F-WPFA-* belongs to §17.

# Changelog

- **2026-05-11 §4 v2.x.z LOCKED** — F-WPFA-* family (12 codes; 13 with F-WPFA-COEFFICIENT-ROLLBACK-INVALID expansion; consolidated into 10 modules per OQ-4 default). Predicate bodies LIVE at LOCK (first §4 amendment with LIVE bodies). Compound paired-commit with §17 v1 + §2 v7.4 + §0.5 v19. Path B documentary edit applied to §5.1.WPFA.6 cross-reference (F-PACKET-SPAN-PROVENANCE-MISSING sibling pattern).
