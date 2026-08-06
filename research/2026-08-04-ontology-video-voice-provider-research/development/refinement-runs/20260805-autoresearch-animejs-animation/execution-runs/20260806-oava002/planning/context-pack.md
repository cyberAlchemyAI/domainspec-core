# OAVA-002 Planning Context Pack

Session evidence only; this is not planning authority or runtime handoff authority.

## Obligations

| ID | Obligation | Status | Controlling evidence |
| --- | --- | --- | --- |
| C1 | Preserve completed OAVA-001 and admit only its successor | covered | `WORK-PACK.md` — Excluded successor portfolio; `work-pack/closeouts/SWU-OAVA-001.json` |
| C2 | Keep the unit at L0 and exclude runtime/browser work | covered | `IMPLEMENTATION-LAYERING.md` — L0; `stages/09-plan.md` — L0 |
| C3 | Reuse the existing consultation capability and typed negatives | covered | `INTERFACES.md` — consultCandidate; vault `operational/README.md` — Capabilities |
| C4 | Bind exact local evidence for S6 edge-draw planning | covered | `views/task-recipes.json` — timeline/SVG recipes; `views/documentation-coverage.json` — createDrawable |
| C5 | Apply hard gates before scoring and preserve claim ceiling | covered | `stages/06-design.md` — Prechecks; `STATES.md` — consultation states |
| C6 | Declare four exact writes and deterministic validation | covered | `WORK-PACK-OAVA-002.md` — Active SWU; `TASK-OAVA-CONSULTATION.md` — writes/validation |
| C7 | Preserve source, AutoAds, and canonical vault bytes | covered | `VALIDATION-CONTRACTS.md`; OAVA-002 task exclusions |
| C8 | Provide selection-ready machine execution and closeout contracts | covered | `work-pack/execution-contract-oava002.json`; OAVA-002 closeout row |

## Selected context

- `WORK-PACK.md` — completed OAVA-001 boundary and explicit OAVA-002 successor.
- `work-pack/closeouts/SWU-OAVA-001.json` — dependency completion evidence.
- `IMPLEMENTATION-LAYERING.md` — L0 proof target and deferred runtime.
- `stages/06-design.md` — S6 meaning, architecture, prechecks, and proof boundary.
- `stages/09-plan.md` — ordered OAVA-002 before runtime work.
- `INTERFACES.md` and `STATES.md` — transport-neutral API and state transitions.
- `VALIDATION-CONTRACTS.md` — causal negative controls and zero-delta checks.
- `prototype/contracts/animation-hypothesis-candidate.schema.json` and `prototype/lib/validate-candidate.mjs` — completed consumer contract.
- `projects/animejs/ontology/agent-knowledge-vault/operational/README.md` plus named operational modules — existing capability/service/projection boundary.
- Canonical vault task-recipe and documentation-coverage selectors for timeline, SVG, and createDrawable.

## Excluded candidates

- `prototype/vendor/anime.esm.js` — B-001 residue and OAVA-003 input; not evidence that runtime admission occurred.
- `work-pack/tasks/TASK-OAVA-PROTOTYPE.md` — controls OAVA-003–005, outside the captured unit.
- Inventory's 2026-08-03 Anime.js research entries — lookup-ready but historically stale relative to the implemented live vault; useful only as non-authority precedent.
- AutoAds code — design precedent only; no import, mutation, or execution in OAVA-002.

## Coverage verdict

Strict planning coverage: pass, 8/8. Runtime handoff: not emitted; Task Session must build a fresh strict handoff after selection and target-baseline binding.
