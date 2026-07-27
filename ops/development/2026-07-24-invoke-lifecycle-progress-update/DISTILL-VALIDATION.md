# Distill Validation: Invoke Lifecycle Progress Plan

## Confirmation

- Target context: accepted lifecycle-churn research plus current Plan, Refresh,
  and Task Session contracts.
- Objective: prevent late missing-producer discovery and make lifecycle
  progress independently falsifiable.
- Output under validation: Define, Design, layering, split work-pack, task/SWU
  contracts, dispatch, and lifecycle handoff.
- Mode/budget: `validate`; automatic Invoke plan validation.
- Execution path: local Proposer/Balancer role simulation. No subagent dispatch
  was requested for this authoring run.

## Role conversation trace

### Proposer

Use one immutable selected-unit epoch, mode-specific producer contracts, an
independent readiness verdict, an append-only transition relation, and typed
Refresh postconditions. Preserve exact mismatch and Task Session live
admission.

### Balancer

| Objection | Reconciliation |
| --- | --- |
| This resembles a workflow engine. | The protocol has no scheduler, retry, replay, event bus, effect store, or current-state service. It validates one selected-unit identity and append-only edges only. |
| A central transition ledger may become shadow authority. | `SWU-ILP-001` must name an existing legitimate owner and explicitly exclude projections/read models. No mutation starts first. |
| An epoch cannot know every repository dependency. | Completeness is bounded to the declared execution-control graph; live Task Session discovery of an omitted control blocks and requires a successor. |
| Local mode could let Plan or Task Session self-attest. | Producer, validator, and consumer identities are pairwise distinct; Task Session consumes and revalidates but does not produce the contract. |
| Projection-only classification could weaken exact joins. | Exact mismatch always blocks. Classification only determines successor/retained-execution handling and is independent of the writer. |
| The plan might preserve an epoch during semantic plan repair. | The epoch control digest covers plan, unit, roles, paths, dependencies, writes, validations, and receipt classes; any change requires successor/superseded. |
| The first task is not code. | That is intentional: authority selection is the smallest reversible trust-building unit and blocks unauthorized schema placement. |
| Legacy migration could fabricate readiness. | Legacy plans default to `legacy_unadmitted`; only new validation and transition receipts admit them. |

## Closure checks

| Check | Result | Evidence |
| --- | --- | --- |
| Smallest coherent design | pass | selected-unit epoch/readiness/transition protocol closes the demonstrated producer and progress gaps |
| SWU atomicity | pass | eleven units; each has one decision or classifier/admission/integration behavior |
| First-unit narrowness | pass | SWU-ILP-001 changes no source and resolves only owner/source authority |
| Recomposition | pass | `work-pack/shared/TRACEABILITY.md` maps ILP-R01..R10 through live closure |
| Hidden gaps | pass | owner, local schema, path completeness, classifier, legacy, and live proof are explicit |
| Overbuilt abstraction | pass | workflow-engine, replay, retries, generic CAS, build system, and central current-state projection are deferred/rejected |
| Navigation | pass | work-pack links each task, wave, manifest, shared contract, and next route |
| Supersession invariant | pass | same-epoch advance is constrained to unchanged-control evidence completion |
| Dispatch route | pass | `dispatch-validation.json`; zero blocks and zero flags |

## Premortem

Most likely failure: implementation adds new fields but still permits an old
route to select Task Session from authored-plan pass alone. Guardrail: a causal
fixture must invoke the real Plan routing entry point and prove that
authored-valid plus non-ready never emits a Task Session route.

Second likely failure: Refresh updates a controlling plan field but retains the
epoch ID. Guardrail: the transition validator must compare epoch control digest
and reject every same-epoch plan repair whose digest changes.

## Frame expiry

Re-run Distill if the transition owner requires a new capability, if the source
placement differs from the planned ownership split, if an execution mode is
added, or if implementation introduces scheduling/retry/replay semantics.

## Verdict

- Verdict: `pass` for plan quality.
- Mutation readiness: `blocked` by `ILP-G01`.
- Current smallest unit: `SWU-ILP-001`.
- Optimization point: settle authority before encoding contracts.
- Next route: Spellcraft lifecycle design/ratification; no Task Session yet.
