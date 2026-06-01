---
title: §0.5 Blueprint Interface Index — v6 amendment LOCKED (Section 6 Operating Envelope rows + `procedure` vocabulary extension)
filed: 2026-04-20 (DRAFT); 2026-04-21 (LOCKED as compound transaction with §6 v1-r1)
operator: Josh
status: **LOCKED 2026-04-21** — landed atomically with §6 v1-r1 LOCK per §6.17 compound-commit obligation (L-005 two-audit cycle complete; closeout at `pipeline/validation/section_06_thesis_round_2/closeout_summary.md`). Supplements §0.5 v5 LOCKED 2026-04-19 + §0.5 cedar-policy-kinds amendment. Runtime-live.
parent_locks:
  - pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md                      # §0.5 v5 LOCKED 2026-04-19 — 101 rows, 13-value closed primitive_kind vocabulary
  - pipeline/blueprint/v0.1/section_00_5_cedar_policy_kinds_amendment.md                # DRAFT — adds rows 102-103 (cedar-policy-seed, cedar-policy-code kinds); PENDING_PARENT_BACKFILL
  - pipeline/blueprint/v0.1/section_06_operating_envelope.md                            # DRAFT v1-r1 SCOPING (v1 filed 2026-04-20; v1-r1 post-Audit-1 revision 2026-04-21) — §6.14 declares rows 104-117; §6.17 binds compound-commit; Thesis Round 1 verdicts + author response at §6.19
dependency_order: cedar-policy-kinds amendment LANDS FIRST (or concurrently as a three-way compound), THEN this v6 amendment. Rationale: cedar-policy-kinds extends the closed vocabulary 13→15; this amendment extends 15→16 (adds `procedure`) and registers 14 new rows. Landing this amendment against a v5-only base would skip rows 102-103 and emit a D-05 check-4 failure when §6 references cedar-policy seeds.
kind_of_amendment: composite — (a) closed-vocabulary extension (§0.5.3.1 closed set 15 → 16 values: add `procedure`) + (b) row append (rows 104-117; 14 new rows) + (c) row-count bump (101 → 117 — accounting for rows 102-103 from cedar-policy-kinds amendment + rows 104-117 from this amendment)
---

# Amendment §A — closed-vocabulary extension (§0.5.3.1)

**Current state (v5 + cedar-policy-kinds amendment):** `primitive_kind` closed vocabulary = 15 values:

1. `architecture-mechanism`
2. `allowlist-row`
3. `mechanism`
4. `interface-contract`
5. `post-gate-check`
6. `pre-gate-check`
7. `failure-code`
8. `constant`
9. `invariant`
10. `marker`
11. `schema`
12. (+ two more v5 values — full enumeration per §0.5 v5 LOCKED file)
13. (…)
14. `cedar-policy-seed` (PENDING_PARENT_BACKFILL per cedar-policy-kinds amendment)
15. `cedar-policy-code` (PENDING_PARENT_BACKFILL per cedar-policy-kinds amendment)

**This amendment adds:** 16. `procedure`

**Definition (§0.5.3.1 new row):**

> **`procedure`** — an audit-time or LOCK-time checklist that runs against a blueprint section or architecture artifact. Distinct from `mechanism` (which is a runtime behavior) and `schema` (which is a data shape). A `procedure` is a sequence of named checks that a human or automated auditor runs; it does not execute inside the Tilth runtime. Canonical example: §6.9 D-05 Downstream drift audit checklist.

**Why `procedure` is load-bearing.** §6 v1 §6.9 declares D-05 as a blueprint-wide audit procedure. The existing vocabulary has no good fit: `mechanism` implies runtime execution (D-05 runs at audit + LOCK, not at pipeline start); `schema` implies a data shape (D-05 is a sequence of checks, not a payload shape); `invariant` implies a condition that must always hold (D-05 is an audit procedure that CHECKS invariants, distinct from the invariants themselves). Without `procedure`, §6.9 D-05 has no valid `primitive_kind` and §6 LOCK fails D-05 check #4 on its own §0.5 registration.

**Ripple check.** Adding `procedure` does not invalidate any v5 LOCKED rows (no v5 row uses it today). It does not conflict with the cedar-policy-kinds amendment. Forward-compat for future amendments that wish to register audit-time checklists (e.g., future Section 13 delegation audits, future Thesis-round procedures) is improved — without this extension, future authors would face the same vocabulary gap §6 faces today.

**Alternative considered.** §6.15 OQ1 listed three options. Option A (this amendment) is author's preference and is adopted here pending Thesis-round confirmation. Options B (recast as `mechanism`) and C (recast as `schema` for audit payload) are explicitly rejected:
- Option B: `mechanism` semantic match is wrong — D-05 is not runtime-executable; it has no seat-invocation signature; it has no pipeline-start ordering slot. Forcing it into `mechanism` dilutes the kind's meaning for downstream consumers.
- Option C: the "checklist items" are not a runtime-consumable schema; they are prose bullets for an auditor. A `schema` kind with six markdown bullet rows is a stretch.

# Amendment §B — row append (rows 104–117)

Reproduced from §6 v1 §6.14 with kind-vocabulary alignment. Stability tier annotations per §6.14.

| Row | Path | Kind | Parent | Stability tier |
|---|---|---|---|---|
| 104 | `operating_envelope.router.schema.block_1_opus_47` | schema | §6.3 | STABLE |
| 105 | `operating_envelope.router.schema.block_2_code_committee` | schema | §6.4 | STABLE |
| 106 | `operating_envelope.sfr.certificate_format` | schema | §6.5 | STABLE |
| 107 | `operating_envelope.sfr.post_gate_parser` | post-gate-check | §6.5 | STABLE |
| 108 | `operating_envelope.context_placement.pre_gate` | pre-gate-check | §6.6 | STABLE |
| 109 | `operating_envelope.context_placement.middle_contradiction_lint` | pre-gate-check | §6.6 | STABLE |
| 110 | `operating_envelope.prompt_template.compilation_pipeline` | mechanism | §6.11 | STABLE |
| 111 | `operating_envelope.track_registry.schema` | schema | §6.7 | STABLE |
| 112 | `operating_envelope.track_registry.frozen_pre_gate` | pre-gate-check | §6.7 | DORMANT_UNTIL_SECTION_5_V6 |
| 113 | `operating_envelope.hardware_tier.metadata` | schema | §6.8 | STABLE |
| 114 | `operating_envelope.pre_gate_precedence_table` | schema | §6.2 | STABLE |
| 115 | `operating_envelope.d05_downstream_drift.checklist` | procedure | §6.9 | STABLE (depends on Amendment §A) |
| 116 | `operating_envelope.failure_code.f_context_middle_contradiction` | failure-code | §6.6 + §6.12 | STABLE |
| 117 | `operating_envelope.failure_code.f_hardware_tier_below_floor` | failure-code | §6.8 + §6.12 | STABLE |

**Kind vocabulary validation (Amendment §A + cedar-policy-kinds dependency):**

- Rows 104, 105, 106, 111, 113, 114: `schema` — v5 LOCKED ✓
- Row 107: `post-gate-check` — v5 LOCKED ✓
- Rows 108, 109, 112: `pre-gate-check` — v5 LOCKED ✓
- Row 110: `mechanism` — v5 LOCKED ✓
- Row 115: `procedure` — requires Amendment §A above ✓
- Rows 116, 117: `failure-code` — v5 LOCKED ✓

All kinds now resolve against the amended vocabulary.

**Parent-wins invariant (§0.5.3 v5 LOCKED).** Each row's `parent` field points at the §6 subsection that owns the primitive. §6 v1 LOCK is the parent artifact; any downstream consumer (§7, §8, §9, §10, §5 v6) is a child that inherits these rows' contracts at its own LOCK without re-declaration.

# Amendment §C — row-count bump

**Pre-amendment state:** §0.5 row count = 101 (v5 LOCKED) + 2 (cedar-policy-kinds amendment PENDING) = **103 at combined-amendment landing**.

**Post-amendment state:** 103 + 14 (this amendment) = **117**.

**Implication for `F-N1-COUNT-STALE` (§6.10).** `F-N1-COUNT-STALE` guards the Section N.1 blueprint-section row count (architecture-level), NOT the §0.5 row count. The §0.5-side drift gate is `F-INDEX-STALE` at PRE-gate order 3 (§6.2 table). `F-INDEX-STALE` fires if the §0.5 Interface Index LOCKED file's declared row count does not match its enumerated rows.

**Operator action at joint LOCK.** At the three-way compound commit (cedar-policy-kinds amendment + this amendment + §6 v1 blueprint), the §0.5 v6 LOCKED file header MUST declare `row_count: 117` and the enumerated row bodies MUST match. Mismatch trips `F-INDEX-STALE` on the next pipeline run.

# Amendment §D — compound-commit binding (per §6.17)

**Compound transaction shape at joint LOCK:**

```
TxnKind: index_amendment
Staged writes:
  1. pipeline/blueprint/v0.1/section_00_5_interface_index_locked.md  (v5 → v6, incorporating cedar-policy-kinds rows 102-103 + this amendment rows 104-117 + `procedure` vocabulary extension)
  2. pipeline/blueprint/v0.1/section_06_operating_envelope.md         (DRAFT v1 → LOCKED v1)
  3. pipeline/blueprint/v0.1/section_00_5_cedar_policy_kinds_amendment.md  (DRAFT → RETIRED, superseded by §0.5 v6)
  4. pipeline/blueprint/v0.1/section_00_5_section_06_operating_envelope_amendment.md  (DRAFT → RETIRED, superseded by §0.5 v6)
```

**Hash-binding (§4.11 predicate requirement):** §0.5 v6 LOCKED file's `section_06_anchor_hash` field MUST equal SHA-3-512(§6 v1 LOCKED file bytes). §0.5 v6's `cedar_policy_kinds_anchor_hash` field MAY be null (the cedar-policy-kinds amendment retires at joint LOCK; its claims are absorbed into v6).

**Abort invariant (§4.10.7.4 lock-release):** If any of the four staged writes fails persist, the §2 vault dispatcher's abort helper reverts ALL four. Partial LOCK is not a permitted terminal state. Either all four land or none do.

**Cedar policy consulted:** `pipeline/logician/cedar_policies/compound_commit.cedar` at module boot (§4.11 spec card). `CompoundTxnKind.index_amendment` MUST be registered in `V0_1_COMPOUND_TXN_REGISTRY` with a predicate that accepts this four-write bundle as a well-formed `index_amendment` transaction.

# Amendment §E — open questions carried to Thesis-round

1. **Three-way compound vs. two-way decomposition.** Amendment §D above proposes a four-staged-write compound. An alternative: land cedar-policy-kinds amendment FIRST as a two-write compound (§0.5 v5.1 + cedar_policy kinds amendment retire), THEN land this §6 amendment as a separate three-write compound (§0.5 v5.1 → v6 + §6 v1 LOCK + this amendment retire). Tradeoff: four-write is atomic-but-larger; two-step is simpler-but-has-an-intermediate-state. Author's preference: four-write, because the intermediate state of "cedar-policy-kinds amendment landed but §6 still DRAFT" leaves rows 102-103 orphaned (no §6 consumer) until §6 LOCKs.

2. **`procedure` vocabulary definition breadth.** §0.5.3.1 Amendment §A above defines `procedure` as "an audit-time or LOCK-time checklist". Question: does this definition accept future examples like a Thesis-round procedure template (e.g., "steps the Judge takes when scoring a blueprint section")? Or is `procedure` narrowly scoped to drift-audit checklists? Author's preliminary read: broad — any audit-time or LOCK-time named sequence of checks qualifies. Thesis confirmation requested.

3. **`DORMANT_UNTIL_<X>` stability tier pattern.** Row 112 uses a stability tier `DORMANT_UNTIL_SECTION_5_V6`. This is a new tier formulation (v5 LOCKED tiers are STABLE / EXPERIMENTAL / DEPRECATED / REMOVED). Question: is `DORMANT_UNTIL_<X>` a valid composite tier, or does §0.5 need a separate `dormant` tier in a §0.5 v6.x amendment? Author's preliminary read: composite is fine as a tier string, because consumers grep the prefix `DORMANT` rather than parsing the suffix. Thesis confirmation requested.

4. **Retirement of superseded amendment files.** Amendment §D proposes that the cedar-policy-kinds amendment and this amendment both retire at joint LOCK (absorbed into §0.5 v6 LOCKED body). Question: should the retired amendment files be deleted, moved to a `pipeline/blueprint/v0.1/archive/` subdirectory, or marked `retired: true` in their frontmatter and kept in place for audit? Author's preliminary read: move to archive subdirectory with dated subfolders (`archive/2026-04-20_section_00_5_v6/`), preserving the audit trail without polluting the live blueprint directory. Thesis confirmation requested.

# Amendment §F — status footer

**DRAFT filed 2026-04-20 alongside §6 v1 SCOPING DRAFT.** Awaits:
1. Thesis-round audit paired with §6 Thesis-round (same Editor + Judge + Red Team team; Judge + Red Team verdicts in SFR format per A3).
2. Joint author response.
3. Verification-round audit per L-005 two-audit cycle.
4. Joint LOCK commit as a four-staged-write compound transaction per Amendment §D.

**Not runtime-live until joint LOCK with §6 v1.** Standalone LOCK of this amendment without §6 v1 is INCOMPLETE (rows reference §6 subsections that would not exist at LOCKED status); §6 v1 LOCK without this amendment is INCOMPLETE (§6 LOCK fails D-05 check #5 on the §0.5 Index row presence for rows 104-117).
