# Stage 01 — Context Builder

Status: `pass`

## Evidence baseline

- The completed candidate vault contains 418 documentation routes, 16 families, 348 repository-source rows, 1,185 graph nodes, 418 relations, and 766 search entries at graph digest `c38e1e9e2a6dbb5b3c50f874dd0178aecc419db76634fd3dbe8deeb974c827f6`.
- Its profile declares `authority_effect: none`, private visibility, and no release admission.
- `WorkEpisode` is an append-only envelope bound to exactly one Task and VersionContext. Closure is not success and correction uses a distinct superseding episode.
- `Attempt` is ordered action history, not evidence. `Outcome` is a terminal classification with a witness and is never rewritten.
- A `Lesson` may become verified only through a closed episode, succeeded outcome, and admissible executed/test witness; even then it is scoped knowledge, not universal truth.
- Current `query.mjs` exposes only local CLI `coverage` and `decision` operations. No agent consultation or episode-append API exists.
- Augmentor supplies a current, locally verified read-only pattern: `POST /augmentor/consultation`, capability `augmentor-consultation-read`, neutral projection, host-injected context, bounded result union, and separate route authorization.

## Hidden structure

The request crosses seven distinct owners: documentation/source truth, vault projection, query service, principal/policy, episode journal, evidence validation, and Lesson review. The selected design keeps all seven explicit.

## Context verdict

The source and ownership baseline is sufficient. The missing capability is not “write to the ontology”; it is “append a typed operational-evidence event and deterministically project it.”

## Receipt

- dispatch_id: `20260804-agent-consultation-work-episodes-api`
- step_id: `s01-context-builder`
- capability_ref: `context-builder`
- status: `pass`
- artifacts: `context-builder/runtime-handoff.md`, `context-builder/runtime-handoff.index.json`
- validation: strict obligation coverage `pass`
- blockers: none
- residue: future append host and Lesson review owners remain deferred
