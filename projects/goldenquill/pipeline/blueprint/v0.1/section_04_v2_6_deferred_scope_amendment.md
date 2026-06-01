---
title: Blueprint §4 Logician — Amendment v2.6 (deferred-scope honesty)
section: §4 Logician
parent_blueprint: section_04_logician.md
parent_version: v2.1
parent_hash_at_amendment_prefix16: e0507e6daaa18676
amendment_version: v2.6
amendment_date: 2026-04-29
amendment_status: DRAFT — awaiting LOCK ceremony alongside §4 Group 7 Batch A pre_gate / gate_runner / cedar_eval cycle-2 promotions
scope: Three deferred-scope items surfaced by the §4 Group 7 Batch A committee dispatch (2026-04-29). Each item is a public-API or blueprint-semantic delta that exceeds L-005 narrow-fix scope; this amendment formally records the deferral with cross-references to the implementation rounds that will close them.
slot_rationale: v2.1.1 is taken by the in-flight GPP-DET amendment (DRAFT awaiting Tier 2 / Tier 3 GPP-COUNCIL signed manifest); v2.2/v2.3/v2.4/v2.5 are taken. v2.6 is the next available slot in the v2.x amendment chain.
---

# §4 Logician — Amendment v2.6 (deferred-scope honesty)

## 0. Amendment intent

The §4 Group 7 Batch A committee dispatch (`pipeline/validation/code_reviews/logician_group_7_batch_a_2026-04-22/synthesis.md`, dispatched 2026-04-29) surfaced six findings across three modules. Three of those findings (a, c, e) closed via L-005 narrow-fix in the same session (≤~5 LOC each, zero public-API delta, zero blueprint-semantic delta). The remaining three findings (b, d, f) are public-API deltas or blueprint-semantic shifts that exceed L-005 scope.

Per CLAUDE.md ("Do not silently rewrite … applicant must approve") and L-005 audit-cycle discipline ("no silent third round"), this amendment formally records the deferred-scope items rather than papering over them. Each deferral cross-references a blueprint anchor, the round that surfaced it, and the implementation round target that will close the deferral.

## 1. Deferred-scope items

### Item B — PRE-gate rows 19 (`F-PRE-INDEX-STALE`) + 20 (`F-PRE-CROSS-ORG-READ`) deferred

**Surfaced at:** Round §4 Group 7 Batch A, R4 Gemini-Flash sub finding `F-R4-PRE-01 HIGH` on `pipeline/logician/pre_gate.py` (2026-04-29).

**Blueprint anchor:** §4 v2.1 §4.2.1 PRE-gate row table — explicitly enumerates 20 rows; the v2.1 expansion added rows 19 + 20 over the v2.0 18-row floor.

**Current implementation:** [`pipeline/logician/pre_gate.py:102`](../../logician/pre_gate.py#L102) defines `PRE_GATE_CHECK_ORDER: tuple[int, ...] = tuple(range(1, 19))` (18 entries; rows 19 + 20 absent). Module docstring + `system_llama.txt` reviewer prompt acknowledge the gap as known-deferred. The Batch A pre-dispatch disclosure (D-01..D-09) did not name the gap explicitly, which surfaced as a disclosure-honesty mismatch when the cross-family R4 seat flagged it as a substrate gap.

**Reason for deferral:** `F-PRE-INDEX-STALE` (row 19) requires a hash-integrity check against the §0.5 Interface Index — a runtime-live consumer that depends on §0.5 v6/v7 amendment-pin tracking which is in flight; `F-PRE-CROSS-ORG-READ` (row 20) requires a session-scoped predicate against the §1 BT3 admin-risk register surface which itself only stabilised post-§1 Round J (2026-04-21) + §1 BT3 Section 1 admin-risk public-API publication. Implementing rows 19 + 20 against an in-flight §0.5 pin set or a freshly-LOCKed §1 BT3 surface risks a re-amendment cycle when those upstream pins shift; deferral is the honest scope call.

**Implementation round target:** **Round M** (post-§4 Round L capstone). Round M scope: implement rows 19 + 20 against the post-Round-L stable §0.5 / §1 BT3 surfaces, with full failure-code coverage (`F-PRE-INDEX-STALE.*` + `F-PRE-CROSS-ORG-READ.*` sub-codes per §6.1) and committee dispatch under §4 v2.6 → §4 v2.7 promotion semantics. Pre-staged spec card name: `pipeline/engineering/spec_cards/section_4_round_m_pre_gate_rows_19_20.md` (TBD).

**Honesty note:** the `## 0. Amendment intent` clause of this amendment + the `system_llama.txt` line "v2.1 row 19 ... and row 20 ... are NOT yet in the module — verify the disclosure flags this as known v2.1 deferred scope" together constitute the explicit deferred-scope record. Future Batch A-style committee dispatches MUST cite this amendment in their pre_dispatch_disclosure D-section to avoid the disclosure-mismatch the cross-family seat flagged.

### Item D — `gate_runner.operator_signoff(...)` public method deferred

**Surfaced at:** Round §4 Group 7 Batch A, R4 Gemini-Flash sub finding `R4-GATE-RUNNER-1 MEDIUM` on `pipeline/logician/gate_runner.py` (2026-04-29).

**Blueprint anchor:** §4 v2.1 references `gate_runner.operator_signoff(rfa_hash, draft_version, operator_keyring) -> SignedClaimEvidenceMap` as a published §5 wiring entry-point invoked by Section 5 CLI at `tilth review --sign`. (See blueprint §5.4 "What Section 4 publishes".)

**Current implementation:** `LogicianGateRunner` does not expose `operator_signoff`. The §4.5 BT7 atomic sign-overwrite flow is implemented in `pipeline/logician/claim_evidence.py` (BT7 owner module) but the `gate_runner` published wrapper is absent.

**Reason for deferral:** `operator_signoff` is the §4 ↔ §5 binding entry-point. Its signature consumes `operator_keyring` (Section 1 published surface) and produces `SignedClaimEvidenceMap` (BT7-canonical via `claim_evidence.py`). The wrapper is straightforward (~30-50 LOC) but binding it requires both §5 R13 capstone LOCK (already done 2026-04-21, stabilised the §5 CLI surface) AND the §4 Round L capstone (test-only, currently pending Batches A/B/C close). Implementing pre-Round-L would force re-dispatch of `gate_runner` after Round L per the test-suite re-validation discipline; better to land in the §4 ↔ §5 cross-section round post-Round-L.

**Implementation round target:** **§4 ↔ §5 cross-section round** (post-§4 Round L). Adds `operator_signoff` to `LogicianGateRunner` + co-test under `tests/logician/test_gate_runner_operator_signoff.py`. Unblocks `tilth review --sign` CLI integration end-to-end. Pre-staged spec card name: `pipeline/engineering/spec_cards/section_4_section_5_cross_round.md` (TBD).

**Honesty note:** the §4 v2.1 blueprint statement "What Section 4 publishes — `gate_runner.operator_signoff(...)`" stands as written; the v2.6 amendment formally tracks the gap until the §4 ↔ §5 round closes. Cross-family seats reviewing `gate_runner` future-promotions MUST cite this amendment in their pre_dispatch_disclosure D-section.

### Item F — Cedar policy-load failure code rename `F-PRE-04.* / F-PRE-17.*` → `F-CEDAR-*` deferred

**Surfaced at:** Round §4 Group 7 Batch A, R3 gpt-oss-120b finding `F-2 MEDIUM` on `pipeline/logician/cedar_eval.py` (2026-04-29).

**Blueprint anchor:** §4 v2.1 §6.10 specifies dedicated `F-CEDAR-01` / `F-CEDAR-02` / `F-CEDAR-03` / `F-CEDAR-04` codes for Cedar policy-load + evaluation failures, distinct from the §6.1 `F-PRE-*` PRE-gate code namespace.

**Current implementation:** `pipeline/logician/cedar_eval.py` uses `F_PRE_04_CEDAR_UNSIGNED` / `F_PRE_04_LEDGER_MISMATCH` / `F_PRE_17_CEDAR_COMPILE_ERROR` — codes inherited from the PRE-gate row hosting the call site (rows 4 + 17), not the §6.10 Cedar-namespace codes the blueprint specifies.

**Reason for deferral:** the rename is mechanically simple (~6-10 LOC + matching test pin updates) BUT touches the public failure-code surface. Existing tests assert the `F-PRE-04.*` codes; downstream consumers (committee summary scripts, daily-log F-AMDT-12 readers, audit-trail validators) may pattern-match the existing strings. A blanket rename without coordinating with downstream consumers risks breaking test fixtures, committee-summary regex assertions, or future audit-trail replays. L-005 narrow-fix discipline excludes public-API delta rounds; this is one.

**Implementation round target:** **§4 v2.7 coordinated rename round** (post-§4 Round L). Coordinated with: (a) update of `cedar_eval.py` failure-code constants, (b) update of `pre_gate.py` failure-code re-exports (`evaluate_check_04_cedar_policy_signed` returns the new codes), (c) update of `pipeline/logician/gates/` reader assertions if any, (d) update of all `tests/logician/test_*` assertions, (e) update of any `pipeline/validation/code_reviews/*` synthesis pattern-matches that name the old codes, (f) update of §6.1 + §6.10 blueprint cross-references. Pre-staged spec card name: `pipeline/engineering/spec_cards/section_4_v2_7_failure_code_rename.md` (TBD).

**Honesty note:** future committee dispatches that flag the F-PRE-04 / F-PRE-17 namespace as a §6.10 violation should reference this amendment + classify the finding as INFO (deferred per amendment) or escalate via L-005 if the deferral is no longer load-bearing. The amendment does NOT excuse the substrate from eventually using the §6.10 codes — it formalises the timing.

## 2. Out-of-scope for v2.6

This amendment does NOT modify:

- §4 v2.1 base-layer semantics (parent-LOCK stable at hash `e0507e6daaa18676`).
- §4 v2.2 12-gate F-AMDT-* enforcement (LOCKED 2026-04-21 across Waves 1-4).
- §4 v2.3 / v2.4 / v2.5 cross-cutting amendments (LOCKED-internal 2026-04-19).
- §4 v2.1.1 GPP-DET amendment (DRAFT, awaiting Tier 2 / Tier 3 GPP-COUNCIL signed manifest — independent timeline).

This amendment does NOT add any new failure codes, public-API surfaces, or blueprint sections. It records the deferred-scope items only.

## 3. Coupling

- **Round §4 Group 7 Batch A** (this round, 2026-04-29) — `post_gate` LOCKED (cycle-1, 5/5 PASS); `pre_gate` / `gate_runner` / `cedar_eval` cycle-2 promotions pending the L-005 narrow-fixes (a, c, e) plus committee Audit #2. This amendment ships alongside the cycle-2 promotion ceremonies as the formal deferred-scope record.
- **Round §4 Round L capstone** (test-only, self-LOCK eligible per §1 J / §2 K / §5 R13 precedent) — exercises the substrate AS-IS (rows 19 + 20 deferred per Item B; `operator_signoff` deferred per Item D; F-PRE-04/F-PRE-17 codes deferred per Item F). Test-author session honors the deferrals; integration tests do not exercise the deferred surfaces.
- **Round M** (Item B closer) — implements PRE-gate rows 19 + 20 against post-§0.5/§1 BT3 stable surfaces.
- **§4 ↔ §5 cross-section round** (Item D closer) — adds `gate_runner.operator_signoff` and binds to §5 CLI.
- **§4 v2.7 coordinated rename round** (Item F closer) — moves Cedar-namespace failure codes to §6.10 specification.

## 4. Lock ceremony

This amendment LOCKs alongside the §4 Group 7 Batch A cycle-2 ledger rows (post-narrow-fix + post-re-dispatch). Lock ceremony fires `pipeline.engineering.lock_ceremony.lock(...)` with `module="pipeline.blueprint.v0.1.section_04_v2_6_deferred_scope_amendment"` and `lock_class="blueprint"`. F-AMDT-12 daily-log block carries seven required non-empty fields; `tests_added_this_module: 0` (blueprint amendment, no test churn — the test surface that exercises the deferrals lives in the §4 Round L capstone or the per-Item closer rounds).

— end amendment v2.6 —
