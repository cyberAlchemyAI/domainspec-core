---
id: result-m2-wire-two-gate
project: ui-prototyping-studio
title: "RESULT — M2-wire: live two-gate apply over real HTML"
status: pass
node_type: refinement-result
run_id: 20260617-m2-wire-two-gate
dispatch_id: refine-ups-m2-wire-two-gate-20260617
capability_ref: refine
updatedAt: 2026-06-17
---

# RESULT — M2-wire

## The crux this run surfaced
The current single-gate apply is **HTML-free**: it appends a revision whose `diffSummary` is *inferred*
from `task.changeType`, never reading the (now real, post-MR1) variant HTML. So M2-wire must introduce
the **HTML data-flow the apply path never had** — current-HTML resolution + candidate ingestion — plus a
place to hold the staged candidate between `apply` and `accept`, plus an **honest diff**. The engine,
the dormant `RevisionApplied` state, and the M0a `candidateHtmlHash`/`diffSummaryHonest` fields already
exist (added for exactly this).

## Decisions
1. **Staged-candidate persistence = store methods** (`saveStagedCandidate`/`get`/`clear`), NOT a session
   field — the staged candidate is admission-boundary infra, not session identity; keeps the entity clean,
   no schema migration. (Tournament A.)
2. **Candidate ingestion = full mutated document via `apply --candidate-from <file>`** — `admitScope` is
   whole-tree; the scope fence rejects out-of-scope; no merge logic. (Tournament B.)
3. **Honest diff** — the two-gate apply holds both current + candidate HTML, so it computes
   `DiffSummaryHonest` (od-id fragment diff) and records it + `candidateHtmlHash`. Discharges the review's
   inferred-diff finding. Idempotency-at-verdict already enforced by `acceptStaged`.
4. **`batch apply` stays as legacy/deprecated single-gate**; the two-gate path is `apply --candidate-from`
   + `accept` + `discard`.

## Toy-game (falsification)
ADMIT (in-scope) → staged, head unchanged; REJECT (out-of-scope) → no stage; ACCEPT → committed, head+1,
honest diff recorded; MISMATCH → CANDIDATE_HASH_MISMATCH; DISCARD → MutationApproved. The gates fire;
head advances only on accept.

## Plan
SWU **MW1** (a: persistence · b: 3 use-cases + honest diff · c: CLI `apply --candidate-from`/`accept`/
`discard`). Deps all exist; no F2 dependency. **Chain dep: MW1's live path requires MR1-registered
variants** (real HTML); stub `generate` variants leave current-HTML unresolvable. See stages/09-plan.md.

## Stage evidence
s1 context / s2 x-ray (HTML-free gap) / s3 review / s4 no-research / s5 tournament / s6 dialectic
(honest diff) / s7 design-review / s8 toy-game / s9 plan / s10 synthesis — all pass
(stages/05-design.md + stages/09-plan.md).

## Recommended next routes
- `task-session` to build **MW1** (a→b→c). The highest-value remaining build — makes the mutation loop
  real end-to-end and ships the honest diff.
- Post-MW1 follow-ons: refresh the live SKILL (accept/discard now exist; apply is two-gate); harness
  scenario for the two-gate verbs; `preview --annotate` so the human SEES the honest diff.
