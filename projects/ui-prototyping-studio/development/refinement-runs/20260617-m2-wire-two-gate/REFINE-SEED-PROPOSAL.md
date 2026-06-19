---
id: refine-seed-m2-wire-two-gate
project: ui-prototyping-studio
title: "Refine Seed — M2-wire: live two-gate apply over real HTML"
status: seed
node_type: refine-seed
run_id: 20260617-m2-wire-two-gate
updatedAt: 2026-06-17
---

# Refine Seed — M2-wire

## Target
Wire the existing two-gate engine (`two-gate-apply.ts`: validateAndStage/acceptStaged/discardStaged)
into a live `apply -> stage -> accept-diff -> record` flow over real HTML. Removes the SKILL's
single-gate caveat and replaces the inferred diff with an honest one.

## Source context (local-first)
- `application/apply-approved-batch.ts` — the current SINGLE-gate apply: HTML-FREE; appends a revision
  with `diffSummary` inferred from `task.changeType`; advances head in one call.
- `application/two-gate-apply.ts` — the pure engine over (currentHtml, candidateHtml, scopeOdIds, port).
- `application/admission.ts` (od-id scope fence + diff), `domain/canonicalize.ts` (M0c).
- `domain/models.ts` — `RevisionApplied` state (dormant), `RevisionManifestEntry.candidateHtmlHash` +
  `diffSummaryHonest` (optional, added in M0a FOR this), `MutationTask.odId`.
- `application/register-variants.ts` (MR1) — variants now carry REAL committed HTML refs (readHtml).
- `application/ports.ts` — StudioSessionStorePort (no staged-candidate persistence yet).

## What this run must produce
- An x-ray of the apply->stage->accept->record state + HTML data-flow (exposing the HTML-free gap).
- A tournament: staged-candidate persistence (store-methods vs session-field) + candidate ingestion.
- A dialectic: domain purity vs pragmatism; inferred vs honest diff (discharge the review finding).
- A toy-game: admit/reject/accept/hash-mismatch/discard.
- A build-ready SWU (non-executed).

## Run parameters
- Preset standard, Research no-research, Subagents recommended -> INLINE (confirmed).
- No F2 dependency (interim accepted). Building is a later task-session.
