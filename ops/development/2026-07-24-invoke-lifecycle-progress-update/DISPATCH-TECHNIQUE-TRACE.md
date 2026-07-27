# Dispatch Technique Trace

Status: pass

A full dispatch is required because this route crosses a public spell, an
execution sigil, a yet-to-be-ratified transition owner, deterministic
validators, generated surfaces, private evidence, and a reusable lifecycle
protocol.

| Technique | Trigger | Applied to | Validation expectation | Status |
| --- | --- | --- | --- | --- |
| `sequence` | authority and producer contracts must precede consumers | waves and dispatch steps | each non-first step consumes predecessor receipts | pass |
| `scu_swu_reduction` | high-complexity split work-pack | eleven SWUs | one behavior/decision and one acceptance boundary per SWU | pass |
| `recomposition_proof` | local contracts must close one lifecycle topology | traceability and VERIFY | ILP-R01..R10 map to tasks, receipts, and live proof | pass |
| `validation_loop` | current contracts fail late rather than permissively | every implementation SWU | causal negative plus compatible positive controls | pass |
| `owner_boundary_check` | Invoke, Refresh, Task Session, validators, and projections have different authority | tasks and interfaces | no capability claims another owner's mutation or transition authority | pass |
| `handle_handoff` | private research informs public generic work | source handles and sanitized lifecycle handoff | public proposal uses generic invariants, not copied private prose | pass |
| `residue_ledger` | owner, local schema, path completeness, migration, and live proof gaps exist | `GAPS.md` and receipts | every gap has owner, route, and gating effect | pass |
| `execution_receipt_handoff` | one selected unit moves through several owners | tasks and closeout contract | every step returns evidence, blockers, residue, and next route | pass |
| `authority_split_gate` | transition admission cannot be inferred from production or observation | SWU-ILP-001 and all transition steps | unresolved owner blocks canonical mutation |
| `state_namespace_boundary` | private parent, public submodule, generated surfaces, and read models differ | write scopes and privacy checks | owner-local writes and explicit synchronization only | pass |
| `artifact_contract_bridge` | prose lifecycle rules need deterministic rejection | schemas, validators, and fixtures | validator pass proves only its declared axis | pass |
| `concrete_path_evidence` | epochs and exact joins are path-sensitive | declared control graph and task scopes | unresolved globs and missing paths reject readiness | pass |
| `observability_grouping` | churn must be distinguishable from progress | goal/epoch/unit/transition/churn fields | telemetry references admitted transition IDs without owning state | pass |

## Considered and skipped

| Technique | Reason |
| --- | --- |
| `delegation_boundary` | no subagent or delegated implementation is authorized by this authoring run |
| `tournament` / `dialectic` | the research compared alternatives; the remaining owner choice is an explicit lifecycle decision |
| `memory_promotion_split` | no memory or Inventory promotion is in scope |
| `toy_game` | deterministic transition and readiness fixtures are more direct |

## Full dispatch

- Dispatch: `execution.dispatch.json`
- Validator: `arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py`
- Required shape verdict: `pass`
- Mutation readiness remains controlled separately by `WORK-PACK.md`.

