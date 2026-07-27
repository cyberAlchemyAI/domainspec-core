# Dispatch Technique Trace

| Technique | Applied to | Effect | Validation expectation | Status |
|---|---|---|---|---|
| `sequence` | Define → Design → Plan → Sigil Development → SWUs | Enforces artifact and receipt dependencies. | Every non-first step consumes a prior handle or receipt. | pass |
| `scu_swu_reduction` | Plan and first SWU | Selects receipt kernel before CLI, mutation, facets, or packaging. | First unit is independently reviewable and reversible. | pass |
| `recomposition_proof` | All SWUs | Maps receipt kernel through installed consumer proof. | Each unit preserves the approved architecture and acceptance criteria. | pass |
| `validation_loop` | Every SWU and layer gate | Requires deterministic evidence before promotion. | Named commands and failure fixtures exist. | pass |
| `owner_boundary_check` | Invoke → Sigil Development → consumer state | Prevents Invoke or Inventory receipts from claiming lifecycle/promotion authority. | Existing canonical work-pack conflict is visible. | pass |
| `handle_handoff` | Private evidence to public lifecycle owner | Uses paths/selectors, not copied private prose. | Public changes contain sanitized generic contracts only. | pass |
| `residue_ledger` | Currentness, atomicity, migration, generated-package gaps | Keeps excluded work visible. | Each residue has an owner or deferred route. | pass |
| `execution_receipt_handoff` | SWU closeout | Defines expected receipt before source mutation. | Every mutation SWU has a closeout sync row. | pass |
| `authority_split_gate` | Canonical integration and non-authority state | Separates authoring, lifecycle, execution, evidence, and promotion owners. | Sigil Development acceptance precedes Task Session. | pass |
| `state_namespace_boundary` | public canonical, generated runtime, consumer state, private plan | Prevents cross-boundary overwrite/leakage. | Managed paths and forbidden paths are explicit. | pass |
| `artifact_contract_bridge` | Receipt schema and facet maps | Connects design contracts to schema/tests. | Every acceptance criterion has an artifact and validation surface. | pass |
| `concrete_path_evidence` | Tests, manifests, receipts, tasks | Removes unresolved implementation globs from acceptance. | Exact proposed paths and commands are named. | pass |
| `observability_grouping` | Invoke and Distill child signals | Preserves parent/child run lineage. | One Invoke row and one Distill child row. | pass |

## Full Dispatch Decision

A full dispatch document is required because the reusable route crosses Invoke,
Sigil Development, generated runtime distribution, consumer state, and a
private/public boundary. See [execution.dispatch.json](execution.dispatch.json).

Subagent strategy is `none`: implementation is intentionally one SWU at a time.

