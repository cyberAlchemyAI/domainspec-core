---
stage_id: s03-interrogation-refine-review
capability_ref: interrogation
mode: refine-review
status: flag
---

# S03 Interrogation Refine Review

## Review Question

Does the confirmed decision slate close enough product, privacy, schema, and
execution ambiguity to proceed toward a one-go build handoff?

## Verdict

`flag`: no blocker remains, but the review found repairable residue that must be
handled before the plan handoff is considered clean.

## Findings

- Product decision slate closes the major product choices and rejected
  alternatives, but inherited status copy should be polished before UI
  implementation.
- Data/security route preserves consult-before-save, consent-before-persist, and
  the existing Drizzle/Postgres path.
- The one-go scope is plausible, but it must reconcile the older W0
  app-mutation gate before app code changes.
- The future build must not reuse the legacy JSON-file `/api/submissions` path
  as the new evidence-candidate persistence layer.

## Required Repair

1. Sync Body War Craft next move from specs/schema Slice 1 to the confirmed
   decision-build route.
2. Use Portuguese-consistent status copy in the handoff:
   - `needs_evidence`: `Precisamos de uma corrida`
   - `evidence_submitted`: `Evidencia enviada`
   - `operator_review`: `Em analise`
   - `source_backed`: `Fonte confirmada`
   - `pilot_ready`: `Pronta para piloto`
3. Make the future Task Session preflight close/update the W0 work-pack mutation
   gate before app mutation.
4. Name concrete validation commands and SuggestedTrack-specific acceptance
   tests.

