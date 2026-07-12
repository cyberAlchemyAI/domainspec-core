# Task Contract: V0 Canvas Repair Verification

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-VERIFY` |
| Objective | Prove the retained review findings are repaired without widening scope. |
| Layer / slice / wave | L3 / VCR-S4 / W3 |
| Execution owner | Task Session on one SWU |

## SWU-VCR-004: Integrated Audit And Closeout

**Goal:** produce one review-linked evidence report and synchronize plan state.

**Dependencies:** SWU-VCR-003 pass.

**Exact write scope:** `work-pack/evidence/`, statuses in this plan package, and
Task Session result. Runtime/source edits are forbidden.

**Ordered checks:**

1. Run canvas contract, publish, replay, and focused path suites.
2. Run bridge regression and schema validation.
3. Confirm policy clauses distinguish protected effects, exception, audit
   event, and receipt.
4. Confirm `/api/canvas/publish` schema and response behavior remain unchanged.
5. Confirm external-target errors reveal neither canonical external path nor
   file bytes.
6. Map G1-A/G1-R/G1-I/K1/P1/K2/P2 to evidence.
7. Confirm no Operations V1 source/schema/route exists in the repair diff.
8. Run scoped `git diff --check`.

**Done criteria:** one evidence report contains commands, outcomes, review-ID
mapping, scoped changed files, residue, and honest claim boundary; work-pack
statuses match evidence.

**Validation:** reviewable report plus machine command outputs summarized in
the Task Session result.

**Expected result:** pass or flag with named platform residue; never claim
hostile race immunity or Operations V1 readiness.
