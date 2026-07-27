# Distill Validation: Inventory Runtime And Faceted Layout

## Confirmation

- Target context: accepted Candidate B research, the current Inventory
  development package, and the proposed faceted organization for new entries.
- Objective: find the smallest implementation sequence that proves the runtime
  without inflating Inventory authority or hiding lifecycle conflict.
- Output under validation: Define, Design, L0-L3 layering, split work-pack,
  SWUs, execution dispatch, and Sigil Development handoff.
- Mode/budget: Standard/Validate; two rounds, four role invocations.
- Execution path: bounded local Proposer/Balancer role simulation. Repository
  policy requires a governed, user-confirmed dispatch before actual subagents;
  none was requested for this authoring validation.
- Evidence status: role reasoning is recorded here, but no structured Distill
  execution receipt is claimed.

## Round 1: Scope And Abstraction

### Proposer

Implement Candidate B and the facet model as one Inventory update: canonical
receipts, dry-run/apply, new physical paths, derived projections, generated
runtime sync, and installed-consumer proof.

### Balancer

| Objection | Category | Reconciliation |
|---|---|---|
| Combining runtime and layout risks a single oversized task. | decomposition | Split by accepted behavior: receipt kernel, no-write transition, apply observation, facet admission, facet projections, runtime sync, consumer proof. |
| Tags used as folders create combinatorial and unstable paths. | information architecture | Use only single-valued `namespace` and `record_class` physically; keep `concepts` logical and multi-valued. |
| A new schema could invalidate 111 flat legacy entries. | compatibility | Admit new fields and paths for new records only; legacy validation remains unchanged and migration is excluded. |
| Candidate B may be misread as atomic. | claim bound | Make non-atomic sequential apply observable and require `partial_mutation_possible`; defer locks, journals, and recovery. |
| A receipt may be misread as proof of current state. | authority | State that receipts are historical. Currentness verification remains a named, separately owned gap. |

## Round 2: Execution And Ownership

### Proposer

Start implementation with the CLI dry-run so the full operator flow is visible
quickly, then add tests and packaging.

### Balancer

| Objection | Category | Reconciliation |
|---|---|---|
| CLI-first couples semantics, I/O, and packaging before stable evidence bytes exist. | first-unit narrowness | Start with pure receipt schema, serializer, digest, and deterministic tests as `SWU-IFR-001`. |
| The canonical Inventory work-pack already selects `SWU-INT-001`. | lifecycle authority | Add W0 owner reconciliation; block Task Session until Sigil Development explicitly sequences, merges, or supersedes. |
| Apply and facets can interact through shared updater code. | write collision | Keep them dependent on the same dry-run contract, execute sequentially, and join before runtime sync. |
| Generated-package success could conceal consumer-state mutation. | boundary | Add manifest-managed sync plus a negative consumer-state fixture before installed-consumer proof. |
| Seven SWUs can drift from the accepted design. | recomposition | Map every unit to acceptance criteria and require a final VERIFY task over AC-01 through AC-10. |

## Technique Trace

| Technique | Result |
|---|---|
| abstraction-level guard | pass: no workflow engine, database, transaction service, migration, or currentness service |
| SCU/SWU reduction | pass: first unit is pure receipt semantics |
| evolution profile | pass: L0 receipt → L1 dry-run → L2 apply/facets → L3 package proof |
| recomposition proof | pass: `work-pack/shared/TRACEABILITY.md` joins all acceptance criteria |
| navigability | pass: README → Spec → Architecture → Work Pack → Handoff |
| boundary-object check | pass: receipts carry evidence without carrying promotion authority |
| frame expiry | pass: explicit rerun triggers below |

## Closure Checks

| Check | Result | Evidence |
|---|---|---|
| Smallest coherent design | pass | receipt computation precedes mutation and distribution |
| SWU atomicity | pass | seven mutation SWUs, each with one accepted behavior |
| First-unit narrowness | pass | `SWU-IFR-001` has no CLI or consumer mutation |
| Recomposition | pass | `work-pack/shared/TRACEABILITY.md` |
| Hidden gaps | pass | owner integration, atomicity, currentness, migration, and generated companions are explicit |
| Overbuilt abstraction | pass | transactionality, migration, search/UI/storage, and release are excluded |
| Navigation | pass | task/wave/shared artifacts have stable links |
| Dispatch route | pass | `dispatch-validation.json` |

## Premortem

Most likely failure: apply writes the entry, then fails before projections are
complete, while the receipt reports only the terminal error. Guardrail:
failure-injection fixtures must assert observed writes, the failed write, and
`partial_mutation_possible=true`.

Second likely failure: `record_class` is collapsed into the existing `type`
field and mixes storage organization with content semantics. Guardrail: schema
and fixture names must keep both fields distinct and test their independent
projections.

## Frame Expiry

Re-run Distill if:

- Sigil Development chooses a different canonical owner or source placement;
- the owner combines or splits any SWU across a different write boundary;
- atomicity, replacement, migration, or currentness enters scope;
- legacy records become required to adopt the new facet fields; or
- a database, UI, search service, or remote Inventory store is introduced.

## Verdict

- Verdict: `pass` for plan decomposition.
- Plan artifact: `flag` until lifecycle acceptance.
- Mutation readiness: `blocked` by `B-OWNER-INTEGRATION`.
- Current smallest unit after acceptance: `SWU-IFR-001`.
- Next route: `sigil-development inventory --update`; no Task Session yet.
