# Distill Validate — OAVA-002 Work Pack

## Run profile

- Target context: close the L0 consultation gate between completed OAVA-001 and runtime admission OAVA-003.
- Output artifact: one medium/split Work Pack with one executable SWU and four exact implementation files.
- Mode: Validate.
- Proposal tracks: one Invoke Plan proposal; one true background Balancer receipt.
- Recursive rounds: one critique and one reconciliation.
- Evidence emission: not configured; the repository-local artifact and helper receipt are preserved as planning evidence.

## Proposer claim

Builder, vault adapter, eligibility evaluator, and their causal test are the smallest coherent unit because the externally observable behavior is one fail-closed decision: consult one source-bound candidate and either return exact evidence-bound eligibility or a typed block. Runtime and browser work remain separately testable.

## Balancer objections and reconciliation

| Category | Objection | Decision |
| --- | --- | --- |
| structural | Four files are one decision but no subset closes W1. | accept; keep one SWU and four exact writes. |
| correctness | Current evidence and request/receipt correlation were underspecified. | revise; bind request ID, host request ID, version context, graph digest, projection digest, policy epoch, records, evidence handles, and explanation path. |
| hidden glue | The draft did not name callable vault exports, schemas, fingerprint, or authorization binding. | revise; name `createCapabilityAdapters`, `createConsultationService`, `compileNeutralProjection`, the request/result contracts, exact audience, host authorization port, and current projection fingerprint in the task contract. |
| schema | The closed candidate schema has no pending status and requires non-empty evidence bindings. | revise; start from the schema-valid OAVA-001 seed, preserve typed negatives outside the candidate, and derive a new candidate only from a current non-empty `ok` receipt. No schema repair. |
| resource | No runtime, browser, network, package install, or Playwright is needed. | accept. |
| usability | Stable result codes and a bounded decision envelope were missing. | revise; add ordered codes and expected shape. |
| governance | The completed OAVA-001 Work Pack cannot authorize OAVA-002. | revise; add sibling `WORK-PACK-OAVA-002.md`, selection-ready entry, machine contract, and complete closeout row. |

## Technique trace

- Abstraction-level guard: pass; OAVA-002 remains L0 consumer integration, not runtime animation.
- Recomposition proof: pass; OAVA-001 validation plus OAVA-002 consultation closes W1 and exposes OAVA-003 without executing it.
- Evolution profile: the adapter may later select other evidence nodes, but exact node selection stays a consumer input within the same closed request contract; no generic plugin or HTTP layer is introduced.
- Boundary-object check: pass after repair; the unchanged service request/result and consumer envelope are shared evidence objects across candidate, vault, and eligibility owners.
- Premortem: most likely failure is silently treating an empty or stale vault result as documentation success; ordered hard gates and causal typed-negative tests prevent it.
- Frame expiry: a vault request/result schema change, Anime.js version change, S6 semantic change, or new candidate consultation state invalidates this plan epoch.
- Navigable result: start at `WORK-PACK-OAVA-002.md`; execute only after Work Pack Readiness, Implementation Readiness selection, and Task Session admission.

## Verdict

Pass after reconciliation. No blocker-level user decision remains. The first visible animation is still outside this unit.
