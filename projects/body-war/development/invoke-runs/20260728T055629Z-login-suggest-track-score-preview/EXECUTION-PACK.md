---
module: body-war-login-suggest-track-score-preview
version: current
status: blocked-pending-decisions-and-selection
updatedAt: 2026-07-28
docType: execution-pack
selected_swu: none
---

# Execution Pack

## Status

This package is execution-shaped but not mutation-ready:

- DEC-JSP-001 and DEC-JSP-002 block L0; DEC-JSP-003 blocks L2;
- no SWU is selected;
- no Task Session preflight has run;
- no deployment or participant/live-provider action is authorized.

## First Safe Route

First run `decision-gate` for DEC-JSP-001 and DEC-JSP-002 against:

- `ARCHITECTURE.md#blocking-decisions`;
- `SPEC.md#proposed-scorepolicy-v0-decision-shape`;
- `WORK-PACK.md#task-jsp-w0-resolve-prototype-policies`.

After those two owner decisions are recorded, select exactly one SWU,
beginning with `SWU-JSP-001`, and start a separate Task Session. Resolve
DEC-JSP-003 separately before selecting `SWU-JSP-008`.

## Frozen Inputs for a Future Task Session

- `SPEC.md`
- `ARCHITECTURE.md`
- `UX-PLAN.md`
- `IMPLEMENTATION-LAYERING.md`
- `WORK-PACK.md`
- exact decision artifacts
- current `projects/body-war/app` source and tests

The future Task Session must re-check digests and current repository state. This
Invoke run does not freeze mutable application bytes for execution.

## Required Closeout

Every coding SWU must return:

- changed paths and scoped diff;
- exact test commands/results;
- positive and negative control results;
- secret/raw-stream leak check;
- claim ceiling;
- blockers/residue;
- next SWU eligibility;
- no Craft or promotion mutation unless separately authorized.

## Stop Conditions

- missing or ambiguous decision artifact;
- stale Design/Plan selector;
- unselected SWU;
- secret or raw provider data exposure;
- automatic `source_backed`, verified control, pilot, release, or production
  claim;
- real/fake provider ambiguity;
- human/live witness attempted before its admission gate.
