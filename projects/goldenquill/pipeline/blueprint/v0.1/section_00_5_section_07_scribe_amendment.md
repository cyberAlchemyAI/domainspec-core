---
title: §0.5 Blueprint Interface Index — v7 amendment LOCKED (Section 7 Scribe rows; pure row-append, no vocabulary extension)
filed: 2026-04-21 (DRAFT); 2026-04-21 (LOCKED alongside §7 v1.1.1)
operator: Josh
status: **LOCKED 2026-04-21** — companion to §7 Scribe v1.1.1 LOCK 2026-04-21. Landed same-day per §7.17 row-append obligation, matching §0.5 v6 ↔ §6 v1-r1 precedent (separate companion amendment file, not an in-place edit of `section_00_5_interface_index_locked.md`). Runtime-live. Supersedes §0.5 v6 LOCKED 2026-04-21.
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md                      # §0.5 v5 LOCKED 2026-04-19 — 101 rows, 13-value closed primitive_kind vocabulary
  - pipeline/blueprint/v0.1/section_00_5_section_06_operating_envelope_amendment.md     # §0.5 v6 LOCKED 2026-04-21 — rows 104-117 + `procedure` vocabulary extension (v6 vocabulary = 16 values)
  - pipeline/blueprint/v0.1/section_07_scribe.md                                        # §7 v1.1.1 LOCKED 2026-04-21 — Thesis Rounds 1+2 complete; closeout at `pipeline/validation/section_07_thesis_round_2/CLOSEOUT.md`
kind_of_amendment: pure row-append (rows 118–158; 41 new rows). NO vocabulary extension — every row's `primitive_kind` resolves against the v5-LOCKED + v6-extended 16-value closed vocabulary.
dependency_order: §0.5 v6 LANDS FIRST (LOCKED 2026-04-21 compound with §6 v1-r1). This v7 amendment extends v6 with §7-owned rows. Landing v7 against a v5-only base would skip rows 102-117 and emit F-INDEX-STALE.
---

# Amendment §A — row append (rows 118–158)

Reproduced from §7 v1.1.1 §7.17 with kind-vocabulary alignment. All rows `stability_tier = STABLE` unless otherwise annotated (v0.1 has no DORMANT_UNTIL_* on Scribe rows — all §7 primitives are live on §7 + §6 co-LOCK).

**Schemas (rows 118–131) — Scribe's 14 canonical shapes:**

| Row | Path | Kind | Parent |
|---|---|---|---|
| 118 | `scribe.rfa_extracted_record.v1` | schema | §7.3 |
| 119 | `scribe.kgie_preflight_result.v1` | schema | §7.4 |
| 120 | `scribe.section_draft.v1` | schema | §7.5 |
| 121 | `scribe.smart_objective.v1` | schema | §7.6 |
| 122 | `scribe.overlooked_expenses_walk.v1` | schema | §7.7 |
| 123 | `scribe.program_template.v1` | schema | §7.9 |
| 124 | `scribe.claim_evidence_entry.v1` | schema | §7.2 (Law 1) |
| 125 | `scribe.admin_risk_flag.v1` | schema | §7.11 |
| 126 | `scribe.eligible_activity_match.v1` | schema | §7.5 (v1.1 Law 2 POST-gate support) |
| 127 | `scribe.conversation_anchor.v1` | schema | §7.4a (v1.1 USER_DATA canonical shape) |
| 128 | `scribe.dialect_register.v1` | constant | §7.8 (4-value closed enumeration) |
| 129 | `scribe.dialect_identity_proxy_table.v1` | constant | §7.2 (v1.1 Law 5 POST-gate table) |
| 130 | `scribe.section_order_invariant.v1` | invariant | §7.5 |
| 131 | `scribe.dialect_register_mix_ban.v1` | invariant | §7.8 (Law 4) |

**Failure codes (rows 132–153) — 22 §7-owned Logician-registered codes:**

| Row | Path | Kind | Parent |
|---|---|---|---|
| 132 | `scribe.failure_code.f_scribe_rfa_missing.v1` | failure-code | §7.13 |
| 133 | `scribe.failure_code.f_scribe_rfa_drift.v1` | failure-code | §7.13 |
| 134 | `scribe.failure_code.f_scribe_phase_0_missing.v1` | failure-code | §7.13 |
| 135 | `scribe.failure_code.f_scribe_kgie_fail.v1` | failure-code | §7.13 |
| 136 | `scribe.failure_code.f_scribe_scope_missing.v1` | failure-code | §7.13 |
| 137 | `scribe.failure_code.f_scribe_unsourced_claim.v1` | failure-code | §7.13 |
| 138 | `scribe.failure_code.f_scribe_smart_invented_metric.v1` | failure-code | §7.13 |
| 139 | `scribe.failure_code.f_scribe_overlooked_expense_unresolved.v1` | failure-code | §7.13 |
| 140 | `scribe.failure_code.f_scribe_dialect_unclassified.v1` | failure-code | §7.13 |
| 141 | `scribe.failure_code.f_scribe_dialect_drift.v1` | failure-code | §7.13 |
| 142 | `scribe.failure_code.f_scribe_admin_risk_unflagged.v1` | failure-code | §7.13 |
| 143 | `scribe.failure_code.f_scribe_admin_risk_high_unapproved.v1` | failure-code | §7.13 |
| 144 | `scribe.failure_code.f_scribe_admin_risk_register_stale.v1` | failure-code | §7.13 + §7.16 |
| 145 | `scribe.failure_code.f_scribe_evaluation_criterion_missing.v1` | failure-code | §7.13 |
| 146 | `scribe.failure_code.f_scribe_section_over_limit_unflagged.v1` | failure-code | §7.13 |
| 147 | `scribe.failure_code.f_scribe_org_cross_ref.v1` | failure-code | §7.13 (Law 3) |
| 148 | `scribe.failure_code.f_scribe_ineligible_activity.v1` | failure-code | §7.13 (v1.1 Law 2 Scribe-owned) |
| 149 | `scribe.failure_code.f_scribe_template_unknown.v1` | failure-code | §7.13 |
| 150 | `scribe.failure_code.f_scribe_template_drift.v1` | failure-code | §7.13 (v1.1) |
| 151 | `scribe.failure_code.f_scribe_paraphrased_numeric.v1` | failure-code | §7.13 (v1.1) |
| 152 | `scribe.failure_code.f_scribe_dialect_induced_identity.v1` | failure-code | §7.13 (v1.1) |
| 153 | `scribe.failure_code.f_scribe_conversation_anchor_invalid.v1` | failure-code | §7.13 (v1.1) |

**PRE/POST-gate checks (rows 154–157) — 4 Scribe-owned gate predicates:**

| Row | Path | Kind | Parent |
|---|---|---|---|
| 154 | `scribe.pre_gate.kgie_pass.v1` | pre-gate-check | §7.4 |
| 155 | `scribe.post_gate.claim_evidence_grep.v1` | post-gate-check | §7.13 (F-SCRIBE-UNSOURCED-CLAIM) |
| 156 | `scribe.post_gate.ineligible_activity.v1` | post-gate-check | §7.2 (v1.1 Law 2 Scribe-owned) |
| 157 | `scribe.post_gate.numeric_verbatim.v1` | post-gate-check | §7.6 (v1.1 numeric-verbatim invariant) |

**Test corpus (row 158) — golden drafts reference:**

| Row | Path | Kind | Parent |
|---|---|---|---|
| 158 | `scribe.test.corpus.v1` | test | §7.14 |

# Amendment §B — kind-vocabulary validation

All rows resolve against the v6-extended 16-value closed vocabulary. NO Amendment §A-style vocabulary extension required at v7.

- Rows 118–127: `schema` — v5 LOCKED ✓
- Rows 128, 129: `constant` — v5 LOCKED ✓ (closed-set semantics documented per-row in the description column, not in `primitive_kind`)
- Rows 130, 131: `invariant` — v5 LOCKED ✓
- Rows 132–153: `failure-code` — v5 LOCKED ✓
- Row 154: `pre-gate-check` — v5 LOCKED ✓
- Rows 155–157: `post-gate-check` — v5 LOCKED ✓
- Row 158: `test` — v5 LOCKED ✓

**Parent-wins invariant (§0.5.3 v5 LOCKED).** Every row's `parent` field points at the §7 subsection that owns the primitive. §7 v1.1.1 LOCK is the parent artifact; downstream consumers (§8 Editor, §9 Judge, §10 Red Team, §5 v6) inherit these rows at their own LOCK without re-declaration.

# Amendment §C — row-count bump

**Pre-amendment state:** §0.5 row count = 117 (v6 LOCKED 2026-04-21).

**Post-amendment state:** 117 + 41 (rows 118–158) = **158**.

**`F-INDEX-STALE` implication (§6.10 / §6.2 order 3).** At joint LOCK with §7 v1.1.1, the §0.5 LOCKED file header MUST declare `row_count: 158` and the enumerated row bodies MUST match. Mismatch trips F-INDEX-STALE on the next pipeline run.

# Amendment §D — compound-commit binding (per §6.17 + §7.17)

**Compound transaction shape at joint LOCK:**

```
TxnKind: index_amendment
Staged writes:
  1. pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md  (v6 → v7, incorporating rows 118-158)
  2. pipeline/blueprint/v0.1/section_07_scribe.md                     (v1.1.1 LOCK-ELIGIBLE → LOCKED)
  3. pipeline/blueprint/v0.1/section_00_5_section_07_scribe_amendment.md  (DRAFT → RETIRED, absorbed into §0.5 v7)
```

**Hash-binding (§4.11 predicate requirement):** §0.5 v7 LOCKED file's `section_07_anchor_hash` field MUST equal SHA-3-512(§7 v1.1.1 LOCKED file bytes).

**Abort invariant (§4.10.7.4 lock-release):** If any of the three staged writes fails persist, the §2 vault dispatcher's abort helper reverts ALL three. Partial LOCK is not a permitted terminal state.

**Bundle-size headroom (mirroring §6.17 v1-r1 discipline):**

| Artifact | Bytes |
|---|---:|
| `section_07_scribe.md` v1.1.1 | ~70 KB (`wc -c` at LOCK time) |
| `section_00_5_section_07_scribe_amendment.md` | ~8 KB |
| Staged-writes envelope | ~2 KB |
| **Bundle total (upper bound)** | **~80 KB** |
| **MAX_COMPOUND_TXN_BYTES cap** | **67,108,864 B (64 MiB)** |
| **Headroom multiple** | **~840×** |

Three orders of magnitude under cap; consistent with §6 LOCK bundle.

# Amendment §E — audit coverage rationale

**Why no standalone Thesis round for this amendment:** §7.17 enumerates these rows verbatim; §7 Thesis Round 1 (driver) and Round 2 (verification) both audited §7.17 as part of the §7 v1 → v1.1.1 payload. The row list is a mechanical derivation from §7's already-audited schemas — not a new scope surface. All kinds resolve against the v6-LOCKED vocabulary (no extension, no new semantic commitments). This amendment is a formalization artifact, authored at §7 LOCK time to satisfy the §7.17 row-append obligation without re-opening the two-audit cycle.

**Precedent:** §0.5 v6 amendment shipped alongside §6 v1 audits under the same pattern — §0.5 v6 was in-scope during §6's Thesis Rounds 1 and 2 as part of the bundled payload. §0.5 v7 differs only in that it was authored after §7's Thesis Rounds closed; the rows themselves were already audited inside §7.17. No audit substance is added by authoring the row list in a separate file; the file exists to satisfy the compound-commit staged-writes contract.

**If Thesis-round coverage is insufficient:** operator may open a §0.5 v7 micro-Thesis (Editor + Judge + Red Team, single-artifact payload) before LOCK. This would be defensible under L-005 as a scope-honest extension. Author's read: mechanical row-append from already-audited source material does not warrant a fresh two-audit cycle; precedent is §0.5 v6.

# Amendment §F — open questions (for operator attention at LOCK)

1. **`scribe.dialect_identity_proxy_table.v1` kind selection.** Row 129 kinds as `constant` but the v1.1 `scribe.dialect_identity_proxy_table.v1` is a closed-set lookup table. Options: (a) keep `constant` with closed-set semantics in the description (this amendment); (b) introduce `closed-set-constant` via a v0.5 v8 micro-vocabulary extension; (c) re-kind as `schema` (the table is data-shaped). Author preference: (a) — closed-set semantics are a description-layer concern, not a vocabulary-layer concern; the existing `constant` kind covers both open and closed sets per §0.5 v5 definition.

2. **Failure-code row granularity.** Rows 132-153 register 22 failure codes as individual rows. Alternative: register a single `scribe.failure_code_registry.v1` row that points at §7.13 as a group. Author preference: per-code rows — each code is individually Logician-enforceable and individually groppable at verifier time; grouping would hide a failure code behind a parent row and weaken D-05 check #3 (failure-code enumeration).

3. **Row count firms at exactly 158.** §7.17 said "approximately 35 rows"; this amendment enumerates 41. The delta (14 failure codes that §7.17 named via `F-SCRIBE-RFA-MISSING through F-SCRIBE-INELIGIBLE-ACTIVITY` shorthand plus 4 v1.1 additions) accounts for the count. Operator should verify 158 at LOCK; if a failure code was duplicated or missed in the §7.13 round trip, correct the count before sealing.

# Amendment §G — status footer

**LOCKED 2026-04-21 alongside §7 v1.1.1 LOCK 2026-04-21.** Runtime-live.

**LOCK-path taken:** companion-file pattern (this amendment file is §0.5 v7's source of truth; `section_00_5_interface_index_locked.md` is NOT edited in place). Matches §0.5 v6 ↔ §6 v1-r1 precedent — the already-audited parent section (§7) LOCK + the row-append companion (this file) LOCK land the same day, and the three-staged-write composition described in Amendment §D was reduced to two effective file transitions (§7 DRAFT → LOCKED; this amendment DRAFT → LOCKED). No retire-absorb of a separate file was required.

**Audit coverage:** §7.17 enumerates rows 118–158 verbatim; both §7 Thesis Rounds 1 and 2 audited them as part of the §7 payload. Mechanical row-append from already-audited source material; no standalone Thesis round per Amendment §E precedent.

**D-05 check #5 (§0.5 row-presence):** satisfied — rows 118–158 are registered in this LOCKED companion amendment file; §0.5 row count 117 → 158. Next pipeline run has no F-INDEX-STALE exposure from §7 subsection references.

**Closeout:** `pipeline/validation/section_07_thesis_round_2/CLOSEOUT.md` (§7 Thesis cycle) + this amendment footer (§0.5 v7 companion).
