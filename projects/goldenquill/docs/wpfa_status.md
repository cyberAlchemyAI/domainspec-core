---
title: WPFA — section §17 status surface
filed: 2026-05-18
operator: Josh Inklovich
status: AUTHORED 2026-05-18 — discoverable status page; reflects state as of this filing date
parent_locks:
  - pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md                                 # §17 v1 LOCKED 2026-05-11 (row 205)
  - pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md                     # §2 v7.4 LOCKED 2026-05-11 (row 206)
  - pipeline/blueprint/v0.1/section_04_v2_x_z_wpfa_amendment.md                                   # §4 v2.x.z LOCKED 2026-05-11 (row 207)
  - pipeline/blueprint/v0.1/section_00_5_section_17_wpfa_amendment.md                             # §0.5 v19 LOCKED 2026-05-11 (row 208)
audience: anyone (operator, agent, auditor) wanting a one-page "what is WPFA, where is it, what state is it in" without reading the LOCK memory file or the full blueprint
update_discipline: refresh when the SN-LLC inaugural registry lands, when v1.x rotation hardening activates, or whenever a state row below changes
---

# What is WPFA?

**Watts Per Funding Action.** §17 of Tilth's blueprint. At every grant-cycle close, the always-local Cycle Accountant emits a `CycleReceipt` Pydantic artifact that proves what Tilth's inference path actually consumed (dollars + watt-hours) versus what 100%-routing to a quarterly cloud baseline would have consumed. Every claim links to a Sovereign-Node-LLC-signed Coefficient Registry version, a `cycle_id`, and at least one Logfire trace_id. The receipt is the sales lever that turns "we have a 128 GB box on your desk" into "and here's the receipt that proves the dividend." Methodology is open; calculation code is proprietary.

Sibling-not-nested with §16 Reflection Packet — both read the cycle-close Logfire span tree, neither reads the other's output.

# Current state (as of 2026-05-18)

| Layer | State | Authority |
|---|---|---|
| §17 v1 blueprint | LOCKED 2026-05-11 (row 205) | `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md` |
| §2 v7.4 Coefficient Registry signed-asset class | LOCKED 2026-05-11 (row 206) | `pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md` |
| §4 v2.x.z F-WPFA-* failure-code family (12 codes / 10 modules) | LOCKED 2026-05-11 (row 207); predicate bodies LIVE | `pipeline/blueprint/v0.1/section_04_v2_x_z_wpfa_amendment.md` |
| §0.5 v19 Interface Index registration (32 rows; new `ast-lint` vocabulary kind) | LOCKED 2026-05-11 (row 208) | `pipeline/blueprint/v0.1/section_00_5_section_17_wpfa_amendment.md` |
| Code phase (6 scope items: weasyprint, CLI verbs, dashboard, Cedar engine, indirect-template scan, Logfire canonicalization) | LANDED 2026-05-11 | session_id `2026-05-11T20:30:00` in `pipeline/metrics/session_log.jsonl` |
| WPFA-specific test coverage | 88 tests landed + integration smoke; AST-lint exit 0 | `tests/seats/wpfa/`, `tests/integration/test_wpfa_end_to_end.py`, `tests/cli/test_tilth_wpfa.py`, `tests/logician/gates/test_f_wpfa_all_gates.py` |
| Coefficient Registry signed asset | **SCAFFOLD** — fail-closed until SN-LLC publishes inaugural Q3-2026 release | `vault_shared/wpfa/coefficient_registry/active.yaml` |
| SN-LLC pinned pubkey | **SCAFFOLD** — fail-closed until white-glove pubkey-pin ceremony | `vault_shared/wpfa/sn_llc_pubkey.signed.yaml` (runbook: `docs/wpfa_white_glove_pubkey_pin_runbook_2026-05-18.md`) |

The two scaffolds are intentional and load-bearing: they are the fail-closed boundary protecting v0.1 from emitting un-anchored receipts before SN-LLC publishes its inaugural cooperative-signed methodology.

# Where the code lives

Production modules (all live; no NotImplementedError / TODO / FIXME):

```
pipeline/orchestrator/seats/wpfa/
├── __init__.py
├── _cedar_bootstrap.py            # Cedar engine bootstrap; three cycle_receipt_* rules
├── cycle_accountant.py            # compose_receipt + run_cycle_accountant_pipeline (620 LOC)
├── pdf_emitter.py                 # weasyprint substrate + RT-C2-02 indirect-template scan (491 LOC)
├── dashboard.py                   # Cowork HTML dashboard; per-org + per-quarter rollups (354 LOC)
└── templates/buyer_facing_pdf.html

pipeline/cli/tilth_wpfa.py         # four TTY-gated verbs (pdf emit / registry update / rollback / pin-pubkey)

pipeline/vault/sub_kinds/
├── cycle_receipts.py              # CycleReceipt schema + 17 invariants (588 LOC)
└── coefficient_registry.py        # load_active + verify_signature (458 LOC)

pipeline/logician/gates/f_wpfa_*.py        # 10 modules realizing 12 F-WPFA-* failure codes
pipeline/linting/r_wpfa_*.py               # 2 AST-lint rules (NO-AUTOSIGN + DECIMAL-MANDATE-ENERGY)
```

Scaffold + per-org artifacts:

```
vault_shared/wpfa/
├── coefficient_registry/
│   ├── active.yaml                # SCAFFOLD until SN-LLC publishes
│   └── history/.gitkeep
├── sn_llc_pubkey.signed.yaml      # SCAFFOLD until white-glove pin
└── sn_llc_pubkey_history/.gitkeep

orgs/_TEMPLATE/
├── wpfa_artifacts/.gitkeep         # per-client buyer-facing PDF output dir
└── vault/operational/cycle_receipts/.gitkeep
```

# CLI surface

Four operator verbs at `tilth wpfa <verb>`, all TTY-gated, all pre-argparse-reject `--yes` / `-y` / `--force` / `--auto-confirm`:

| Verb | Purpose |
|---|---|
| `tilth wpfa pdf emit` | Emit a buyer-facing PDF for one operator-attested CycleReceipt |
| `tilth wpfa registry update` | Stage a new SN-LLC-signed Coefficient Registry version (signature verify + history copy + active.yaml repoint) |
| `tilth wpfa registry rollback` | Re-pin active.yaml to a prior signed registry by SHA3-512 hex |
| `tilth wpfa registry pin-pubkey` | Set / co-signed-rotates the white-glove-pinned SN-LLC public key |

See `docs/wpfa_white_glove_pubkey_pin_runbook_2026-05-18.md` for the white-glove pin ceremony.

# Failure-code family (F-WPFA-*)

Twelve codes / ten modules. All predicate bodies LIVE at LOCK (first §4 amendment family with LIVE bodies, per §17 v1 LOCK row 205 distinction). EXCLUDED from `F-CLASS-COVERAGE-INCOMPLETE` META gate per OQ-6 default — F-WPFA-* is its own family.

| Code | Tier | Severity |
|---|---|---|
| `F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED` | PRE-load | P0 |
| `F-WPFA-COEFFICIENT-SIGNATURE-INVALID` | PRE-load | P0 |
| `F-WPFA-COEFFICIENT-ROLLBACK-INVALID` | PRE-load | HIGH |
| `F-WPFA-MODEL-COEFFICIENT-MISSING` | PRE-emission | HIGH |
| `F-WPFA-BASELINE-MISSING` | PRE-emission | HIGH |
| `F-WPFA-SPAN-PROVENANCE-MISSING` | PRE-emission | HIGH |
| `F-WPFA-COUNTERFACTUAL-INFLATION` | PRE-emission | P0 |
| `F-WPFA-OPERATOR-SIGNATURE-MISSING` | PRE-PDF-emit | HIGH |
| `F-WPFA-DIMENSION-UNSUPPORTED` | PRE-emission | HIGH |
| `F-WPFA-REGISTRY-DRIFT` | POST-load (advisory) | MEDIUM |
| `F-WPFA-SCHEMA-INVALID` | PRE-write + POST-read | HIGH |
| `F-WPFA-CROSS-ORG-LEAK` | PRE-write | P0 |
| `F-WPFA-PDF-CONFIDENTIAL-LEAK` | PRE-PDF-emit | P0 |

(The table lists 13 lines because the coefficient-registry-validation triplet ships as 3 codes in 1 module per OQ-4 default — total module count = 10; total code count = 12. The PDF-auditability concern is a sub-tag `.pdf_claim_unlinked` under `F-WPFA-SPAN-PROVENANCE-MISSING` per OQ-7 default.)

# Open blockers (operator-territory; not code work)

1. **SN-LLC inaugural Q3-2026 Coefficient Registry publication.** Sovereign Node LLC defines per-model dollar + watt-hour coefficients, signs the registry under SN-LLC's Ed25519 key, and publishes the signed YAML. Until this lands, every cycle-close emission fail-closes at `load_active()`. Governance + measurement deliverable, not software.
2. **White-glove operator pubkey-pin ceremony.** Operator runs `tilth wpfa registry pin-pubkey` once at onboarding. CLI verb is implemented and TTY-gated. Procedure: `docs/wpfa_white_glove_pubkey_pin_runbook_2026-05-18.md`.

Both blockers are documented in the next-dispatch scoping brief: `docs/wpfa_section_17_next_dispatch_brief_2026-05-18.md` (filed 2026-05-18; PR #36 against `main`).

# v0.1 vs v0.2 vs v1.x vs Stage-2+ scope boundary

Active at v0.1 Beta: `CycleReceipt` schema, sub-kind registry row, Coefficient Registry signed-asset class, Cycle Accountant module, F-WPFA-* family, operator-facing dashboard, buyer-facing PDF artifact, operator Ed25519 attestation flow.

v0.2 first wave: `water` + `co2` dimensions, dashboard scheduled-refresh (per `schedule` skill), multi-currency / FX, peer-review-of-methodology candidate.

v1.x: atomic `registry_rotation.lock` + 48h pubkey-rotation lock-out (RT-03, RT-C2-01), registry-rollback mutex during cycle-close (RT-14), Tilth-side coefficient measurement (operator on-hardware energy measurement), Archivist v1.x quarterly digest composition with WPFA rollup section.

Stage-2+ (12-Tilth fleet milestone and beyond): per-fleet rollup (currently renders as data-free `[Stage-2+]` placeholder card per RT-11), uint128 promotion for energy overflow (RT-08), aggregate-dashboard privacy mask (RT-10), deployment-side baseline-whitelist (RT-04 / v2 multi-tenant), principal-attribute cryptographic binding (RT-09 / v2 multi-tenant), Stage-5 commons consent-tier WPFA aggregation.

All v1.x / Stage-2+ / v2 items are **HARD-LOCKED-as-deferred** per §17.14 and require an architecture-axiom relaxation to activate.

# Related files

| Purpose | Path |
|---|---|
| Full §17 v1 blueprint | `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md` |
| Memory anchor | `spaces/653ca68f-939c-4abd-91c8-44e896d0ce7b/memory/project_blueprint_section_17_wpfa_v1_locked.md` |
| Code-phase dispatch packet (LANDED 2026-05-11) | `pipeline/handoffs/ws_wpfa_code_phase_handoff_2026-05-11.md` |
| Pre-LOCK Thesis handoff (rows 205-208 LOCK precedent) | `pipeline/handoffs/ws_wpfa_handoff_2026-05-10.md` |
| Audit trail (Thesis cycle 1 + 2) | `pipeline/validation/wpfa_thesis_2026-05-10/` |
| §16 / §17 sibling reconciliation memo | `pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md` |
| Next-dispatch scoping brief (PR #36) | `docs/wpfa_section_17_next_dispatch_brief_2026-05-18.md` |
| White-glove pubkey-pin runbook | `docs/wpfa_white_glove_pubkey_pin_runbook_2026-05-18.md` |
| White-glove playbook (umbrella) | `docs/white_glove_v0_1_beta.md` |
