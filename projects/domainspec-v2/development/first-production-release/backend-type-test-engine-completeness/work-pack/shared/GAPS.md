# Cross-Task Blockers And Gaps

| ID | Class | Affects | State | Owner | Repair |
| --- | --- | --- | --- | --- | --- |
| R-BTE-001 | resolved dependency | lane routing | closed | FPR-02 coordination owner | Backend and UI are separate; FPR-02U admission or completion is not an input to any BTE SWU. |
| B-BTE-001 | acceptance blocker | all SWUs | resolved | FPR-02B owners | Accepted by DEC-FPR02-SUPPORTED-PROFILE; no decision blocker remains. |
| B-BTE-002 | contract blocker | BTE-002 onward | resolved | FPR-02B profile + node/edge contract owners | Successor profile, roots, and mapping accepted; implementation remains Task Session-owned. |
| G-BTE-001 | scope gap | FPR-02B | active | relationship owner | Exercise all 16 backend signatures with causal composition/removal evidence. |
| G-BTE-002 | claim gap | FPR-07/FPR-09 | deferred | semantic/conformance owners | Structural checks cannot claim business correctness. |
| G-BTE-003 | evolution gap | future | deferred | cross-feature owner | Trigger only when a cross-feature product claim exists. |
| G-BTE-004 | tooling residue | BTE-001 | accepted | tooling owner | Keep the YAML subset bounded; broaden only from an actual unsupported schema. |
| G-BTE-005 | consumer gate | IOLM | active | IOLM owner | Preserve `G-DSV2-SG: BLOCKED` until exact owner receipts and bounded Sg proof pass. |
| G-BTE-006 | consumer contract | Body War | active | Body War consumer owner | Add private read-only fixture/adapter and redaction proof under the consumer home. |
| G-BTE-007 | continuation sync | Craft/Inventory | active | Craft + Inventory owners | Register the applied refresh and new consumer proof artifacts. |
| G-BTE-008 | authority drift | engine path | needs-review | engine owner | Resolve legacy/v2 path and local source-of-truth wording before implementation handoff. |

## Stable Non-Claims

- `13/13` backend kinds is not full-language coverage.
- `16/16` backend relationship signatures and structural criteria are not semantic satisfiability.
- Empty minted projects may remain valid at compiler altitude; an empty release witness must fail at coverage altitude.
- No passing Task Session or test receipt grants release admission.
- FPR-02U progress, blockage, or completion cannot change backend BTE readiness.

## Define-Stage Contract-Completeness Overlay — 2026-07-21

This overlay imports the surviving result of accepted audit 002 into the BTE
authoring package. It is the current readiness view until Invoke Design and Plan
regenerate the older rows above. It does not change machine authority, reopen
fixed findings, select an implementation SWU, or invalidate completed
`SWU-BTE-001`/`SWU-BTE-003` receipts.

| Audit gap | Severity/scope | State here | Owner/next repair |
| --- | --- | --- | --- |
| `GAP-002` | critical successor profile | active | Profile owner: admit a versioned exact-13 successor; current v1 remains separate. |
| `GAP-004` | major relationship breadth | admission-blocked | Relationship/profile owners: decide exact 16-family admission; 21/29 variants stay derived/unselected. |
| `GAP-005` | critical identity/digest chain | active | Compiler/evidence owners: propagate every governing identity/version/digest through graph, obligations, results, receipts, and replay. |
| `GAP-006` | critical required structure | active | Kernel/compiler owners: evaluate literal `required_structure` across all 13 schemas with targeted negatives. |
| `GAP-007` | major discriminator domains | active | Definitions/compiler owners: replace presence-only Interface/Mapping checks with admitted closed domains. |
| `GAP-008` | major Value Object equality | active | Definitions/compiler owners: replace substring equality with a structural declaration and discriminating controls. |
| `GAP-011` | blocker, key-and-door only | pending local decision | EVF semantic owner: resolve or explicitly defer `DEC-GCP-001`; it does not block unrelated formation work. |
| `GAP-012` | critical edge source/layout | active | Source-contract owner: define versioned independent edge source schema and roots. |
| `GAP-013` | critical relationship causality | admission-blocked | Graph/relationship owners: prove selected endpoint/root/scope/direction/lifecycle and composition/removal effects. |
| `GAP-014` | major ordered orchestration | active | Graph owner: preserve and replay `orchestrates` ordinal. |
| `GAP-016` | critical canonical graph input | active | Engine owner: feed minted graph/source manifest into canonical derivation and reject disconnected empty derivation. |
| `GAP-017` | critical exact obligations | active | Independent validation owner: freeze nonempty exact `O_spec` and compare stable IDs to `O_gen`. |
| `GAP-018` | critical bindings | active | Binding owner: require unique role-typed digest-bound matches; reject empty/first/ambiguous/stale matches. |
| `GAP-019` | critical executable evidence | active | Test owner: forbid skip/todo as proof and require every exact generated test to execute. |
| `GAP-020` | critical denominator gate | active | Validation owner: fail empty/missing/extra/duplicate/stale exact sets and enforce `O_spec=O_gen=T_gen=E_run=M_killed`. |
| `GAP-021` | critical evaluators | active | Evaluator owner: add independent bounded evaluators for every selected criterion/effect. |
| `GAP-022` | critical replay joins | active | Receipt/replay owners: independently join the complete source-to-result identity/digest chain. |
| `GAP-023` | critical aggregates | active | Integration owner: implement fail-closed core, consumer, and terminal required-check manifests/commands. |
| `GAP-024` | major mutations | active/admission-dependent | Test owner: select, execute, and kill exact formation/family mutants without inflating 21/29. |
| `GAP-025` | critical IOLM proof | blocked-after-core | IOLM owner: add `graph_hierarchy_table_get_parity`, consumer-owned execution, fresh receipt, and replay. |
| `GAP-026` | major integrated manifest | blocked-after-core | Integration owner: replace pending/self-asserted 13/16 handles with exact accepted core and fresh consumer receipts. |
| `GAP-027` | major Body War proof | blocked-after-core | Body War owner: replace Markdown source contract with a machine contract/schema/runner/receipt/replay lane. |
| `GAP-029` | critical current-v1 formation authority | **decision resolved; design/proof open** | Option 2 selected: Design a distinct versioned YAML-owned replacement, JSON retirement map, migration/compatibility proof, and rejection of the false-green control. Current v1 remains frozen and cannot claim full formation conformance meanwhile. |
| `GAP-030` | critical exact-16 compiler parity | active after replacement contract design | Compiler/test owners: positive plus discriminating-negative compiler execution for all exact 16 kind-scoped criteria against the versioned replacement. |

### Non-Surviving Findings

- Old `GAP-009` remains fixed: the compiler reaches the shared criterion kernel.
- `GAP-028` remains repaired/fixed: the corrected freeze supplies
  machine-addressable selectors and a matching 55-entry effective catalogue.
- `GAP-003`, `GAP-010`, and `GAP-015` remain dropped.
- `GAP-001` remains superseded by the `GAP-028` traceability history.

### Readiness Consequence

The older `ready-after-decision-gate`/accepted-successor wording above and in the
current Plan is insufficient after audit 002. The formation decision now
unblocks Invoke Design, but `GAP-029` remains open until machine contracts,
migration, the false-green negative, and replay proof exist. No continuation
SWU is exposed.
