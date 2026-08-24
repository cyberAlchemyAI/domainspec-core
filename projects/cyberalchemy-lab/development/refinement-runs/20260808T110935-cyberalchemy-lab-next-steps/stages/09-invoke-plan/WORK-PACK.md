---
module: tower-evidence-navigator
version: candidate-l0
status: selection-ready
updatedAt: 2026-08-08
docType: work-pack
---

# WORK-PACK: Tower Evidence Navigator L0

## Control fields

| Field | Value |
| --- | --- |
| workPackId | `WP-CAL-TEN-L0` |
| workPackGateStatus | `pass` — planning/authoring gate only |
| complexity | `medium` |
| outputMode | `split` |
| executionPackRef | `EXECUTION-PACK.md` |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` |
| distillValidationStatus | `pass` |
| swuAtomicityStatus | `pass`; task-shaped count 0 |
| firstUnitNarrownessStatus | `pass`; `SWU-CAL-001` |
| closeoutSyncStatus | `pass` |
| admissionTiming | `selected-unit-at-task-session` |
| executionEntryState | `selection-ready` |
| executionEntryRef | `EXECUTION-ENTRY.json` |
| allowedRoutesDigest | `f7f14dc331a9dbe8c8bec023d72a2fc8c22b1fbf072bcc3bc8d194c4ef10fe25` |
| activeLayerWindow | `L0` |
| readinessProfile | candidate mechanics proof; not release/production |
| implementationStatus | `not-started`; no product command run |
| admissionContractRef | `work-pack/admission/L0-EXECUTION-CONTRACTS.json` |
| finiteFrontierContractRef | `work-pack/admission/FINITE-FRONTIER-CONTRACT.json` |
| readinessAuditConfigRef | `work-pack/admission/WPRA-CONFIG.json` |

`pass` here means the non-executed plan and its first one-unit entry projection validate. It is not implementation authorization, Task Session admission, product evidence, authority, promotion, publication, deployment, release, or production readiness.

## Objective summary

- Objective: create a private Research Tower-shaped candidate package and deterministically prove one complete synthetic tower's identity, relation, privacy, projection, and failure contracts.
- Primary inputs: validated design, Distill Repair, installed Node runtime at future execution time, exact repository files.
- Success condition: all ten SWUs close in order, every source package file is snapshot-bound, two synthetic compiles are byte-identical, all 15 mutants fail with exact codes, and independent receipts retain mechanics-only/no-authority ceilings.
- Delivery boundary: L0 synthetic proof only. Real tower selection, IDE/direct GET, browser/UX/accessibility, multi-tower aggregation, graph storage, public/external effects, and all authority gates are excluded.

## Execution policy and entry

- Machine projection: `EXECUTION-ENTRY.json`
- Authoring validation: `EXECUTION-ENTRY-VALIDATION.json`, status `pass`
- Current captured frontier: `SWU-CAL-001` only
- Current allowed routes: one Task Session implementation route and one exact Invoke Refresh closeout route
- Selected unit: none; Implementation Readiness may select the sole captured unit only after a future direct execution request
- Pre-execution owner prerequisite: none for synthetic L0
- Automatic decisions: installed internal tool selection, owner routing, reversible local defaults, declared fallback, fresh Task Session resumption
- Stop decisions: semantic choice, scope expansion, destructive/irreversible effects, credentials, external/network effects, cost/risk acceptance, authority/promotion/publication/deployment, failed acceptance-critical validation

The one-unit projection is deliberate. Each passing closeout may advance a new selection-ready projection to the unique successor; it cannot expose or run the entire Work Pack from this Refine confirmation.

The full ten-unit admission contract is a separate frozen input to Work Pack Readiness Audit and Implementation Readiness. It does not expand `EXECUTION-ENTRY.json`, select a unit, create Task Session state, bind direct execution intent, or authorize mutation. Its finite-frontier controller is `implementation-readiness`; fresh-session admission is delegated to `task-session-until-blocker`, each unit is executed by Task Session, and Invoke Refresh owns closeout synchronization.

## Delivery slices

| Slice | Outcome | Layer | Waves | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-CAL-01 | deterministic identity and closed record/projection contracts | L0 | W0-W1 | none | canonical/record/projection contract tests |
| S-CAL-02 | candidate Research Tower package and one valid synthetic graph | L0 | W1 | S-CAL-01 | structure, control-state, fixture cardinality tests |
| S-CAL-03 | deterministic compiler and 15 failure proofs | L0 | W2 | S-CAL-02 | valid repeated compile plus exact mutant matrix |
| S-CAL-04 | complete non-circular package identity | L0 | W3 | S-CAL-03 | package snapshot `--check` and M14 |
| S-CAL-05 | independent synthetic witness evidence | L0 | W3 | S-CAL-04 | full suite, two-run byte equality, exact-input records |

## Task board

| Task | Goal | Layer | Waves | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-CAL-CONTRACTS](work-pack/tasks/TASK-CAL-CONTRACTS.md) | identity, records, relations, privacy, projection contracts | L0 | [W0](work-pack/waves/W0.md), [W1](work-pack/waves/W1.md) | selection-ready at 001 | not-started |
| [TASK-CAL-PACKAGE](work-pack/tasks/TASK-CAL-PACKAGE.md) | Research Tower spine and valid synthetic graph | L0 | [W1](work-pack/waves/W1.md) | waits for 003 | not-started |
| [TASK-CAL-COMPILER](work-pack/tasks/TASK-CAL-COMPILER.md) | deterministic transform and mutants | L0 | [W2](work-pack/waves/W2.md) | waits for 006 | not-started |
| [TASK-CAL-SNAPSHOT](work-pack/tasks/TASK-CAL-SNAPSHOT.md) | complete package identity | L0 | [W3](work-pack/waves/W3.md) | waits for 008 | not-started |
| [TASK-CAL-WITNESS](work-pack/tasks/TASK-CAL-WITNESS.md) | independent synthetic witness closeout | L0 | [W3](work-pack/waves/W3.md) | waits for 009 | not-started |

## SWU manifest and navigation

| SWU | Parent task | Primary behavior | Dependencies | Validation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-CAL-001 | [CONTRACTS](work-pack/tasks/TASK-CAL-CONTRACTS.md) | canonical JSON/digest primitive | none | canonical-json Node test | local-fallback | selection-ready |
| SWU-CAL-002 | [CONTRACTS](work-pack/tasks/TASK-CAL-CONTRACTS.md) | closed record/relation contract | 001 | record-contract Node test | local-fallback | not-started |
| SWU-CAL-003 | [CONTRACTS](work-pack/tasks/TASK-CAL-CONTRACTS.md) | privacy/projection contract | 001-002 | projection-contract Node test | local-fallback | not-started |
| SWU-CAL-004 | [PACKAGE](work-pack/tasks/TASK-CAL-PACKAGE.md) | Research Tower spine | 003 | reviewable seven-file/link/ceiling check | local-fallback | not-started |
| SWU-CAL-005 | [PACKAGE](work-pack/tasks/TASK-CAL-PACKAGE.md) | candidate gate/control records | 002,004 | package-structure Node test | local-fallback | not-started |
| SWU-CAL-006 | [PACKAGE](work-pack/tasks/TASK-CAL-PACKAGE.md) | complete valid synthetic graph | 001-005 | fixture-contract Node test | local-fallback | not-started |
| SWU-CAL-007 | [COMPILER](work-pack/tasks/TASK-CAL-COMPILER.md) | deterministic projection compile | 006 | compile-projection Node test | local-fallback | not-started |
| SWU-CAL-008 | [COMPILER](work-pack/tasks/TASK-CAL-COMPILER.md) | 15 exact fail-closed mutants | 007 | negative-mutants Node test | local-fallback | not-started |
| SWU-CAL-009 | [SNAPSHOT](work-pack/tasks/TASK-CAL-SNAPSHOT.md) | normalized complete package snapshot | 008 | package-snapshot Node test + `--check` | local-fallback | not-started |
| SWU-CAL-010 | [WITNESS](work-pack/tasks/TASK-CAL-WITNESS.md) | independently validated synthetic witness | 009 | full suite + two-run byte equality | manual validation owner | not-started |

Task files own exact write scopes, algorithms, split analyses, edge cases, done criteria, acceptance evidence, and handoff notes. Invoke planning does not pre-generate execution-time Context Builder packs.

Machine-normalized commands, exact path-level write partitions, runtime identities, validation limits, receipt schemas, canonical successors, stop classes, and the ten-unit frontier are closed in `work-pack/admission/`. If prose and the admission contract disagree, execution stops and routes to Invoke Refresh; neither source may be silently inferred from the other.

## SWU atomicity review

| SWU | Candidate child units | Why retained boundary is smallest executable unit | Verdict |
| --- | --- | --- | --- |
| 001 | parse restrictions / serialization / hash | digest safety requires one closed profile across all three | pass |
| 002 | record schema / relation registry | graph validity requires typed records and endpoint rules together | pass |
| 003 | projection schema / privacy policy | output cannot validate without applied privacy binding | pass |
| 004 | seven spine files | Research Tower minimum navigation/closure scaffold is incomplete when split | pass |
| 005 | decision / definition / residue / validation / promotion controls | these jointly encode one non-authority blocked gate state | pass |
| 006 | source tree / graph records | one source-backed valid fixture requires exact bytes and records together | pass |
| 007 | validate / build adjacency / filter / revision / atomic write | selected end-to-end transform cannot pass as isolated fragments | pass |
| 008 | M01-M15 | acceptance owns complete single-fault matrix and no-write invariant | pass |
| 009 | enumerate / self-hash / snapshot ID | complete package identity exists only when all agree | pass |
| 010 | input lock / compile / independent validation / result | witness evidence is meaningless unless exact output and ceiling close together | pass |

First-unit narrowness: SWU-CAL-001 is a pure, reversible, three-file trust primitive with no domain fixture, package scaffold, projection, IDE, or external effect. A smaller child cannot independently prove digest identity.

## Task Session closeout synchronization contract

Common baseline/delta/receipt rules are in `work-pack/shared/CLOSEOUT-CONTRACT.md`. Each row is complete only with the task-local exact write scope and command.

| SWU | Lifecycle owner route | Terminal source receipt | Declared closeout target inventory | Baseline | Allowed deltas | Owner validation | Expected closeout receipt | Successor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 001 | `invoke:refresh:apply-approved` | `projects/cyberalchemy-lab/development/execution-receipts/WP-CAL-TEN-L0/SWU-CAL-001.json` | WORK-PACK, CONTRACTS task, W0, EXECUTION-ENTRY, receipt 001 | shared exact hash/absent rule | shared five classes | receipt pass + canonical test + JSON/route validator | `work-pack/receipts/SWU-CAL-001.json` | 002 |
| 002 | same | execution receipt 002 at same root | WORK-PACK, CONTRACTS task, W1, EXECUTION-ENTRY, receipt 002 | shared | shared | receipt pass + record test + route validator | `work-pack/receipts/SWU-CAL-002.json` | 003 |
| 003 | same | execution receipt 003 | WORK-PACK, CONTRACTS task, W1, EXECUTION-ENTRY, receipt 003 | shared | shared | receipt pass + projection contract test + route validator | `work-pack/receipts/SWU-CAL-003.json` | 004 |
| 004 | same | execution receipt 004 | WORK-PACK, PACKAGE task, W1, EXECUTION-ENTRY, receipt 004 | shared | shared | receipt pass + seven-path/link/ceiling review + route validator | `work-pack/receipts/SWU-CAL-004.json` | 005 |
| 005 | same | execution receipt 005 | WORK-PACK, PACKAGE task, W1, EXECUTION-ENTRY, receipt 005 | shared | shared | receipt pass + package-structure test + route validator | `work-pack/receipts/SWU-CAL-005.json` | 006 |
| 006 | same | execution receipt 006 | WORK-PACK, PACKAGE task, W1, EXECUTION-ENTRY, receipt 006 | shared | shared | receipt pass + fixture test + route validator | `work-pack/receipts/SWU-CAL-006.json` | 007 |
| 007 | same | execution receipt 007 | WORK-PACK, COMPILER task, W2, EXECUTION-ENTRY, receipt 007 | shared | shared | receipt pass + compiler test + route validator | `work-pack/receipts/SWU-CAL-007.json` | 008 |
| 008 | same | execution receipt 008 | WORK-PACK, COMPILER task, W2, EXECUTION-ENTRY, receipt 008 | shared | shared | receipt pass + M01-M15 test + route validator | `work-pack/receipts/SWU-CAL-008.json` | 009 |
| 009 | same | execution receipt 009 | WORK-PACK, SNAPSHOT task, W3, EXECUTION-ENTRY, receipt 009 | shared | shared | receipt pass + snapshot test/`--check` + route validator | `work-pack/receipts/SWU-CAL-009.json` | 010 |
| 010 | same | execution receipt 010 | WORK-PACK, WITNESS task, W3, EXECUTION-ENTRY, receipt 010 | shared | shared | receipt pass + full exact-input witness checks + route validator | `work-pack/receipts/SWU-CAL-010.json` | none; stop at L0 |

For rows 002-010, closeout creates a future one-unit `EXECUTION-ENTRY.json` with only the named successor and exact implementation/closeout routes. Any semantic change requires Invoke Refresh review, not closeout inference.

## Validation strategy

| Surface | Planned command/evidence | Current state |
| --- | --- | --- |
| Plan artifacts | JSON parse, link/path/existence checks, scoped whitespace | run during Refine |
| Design admission | exact Design Scope extractor and fixed-point selection validator | pass |
| Execution entry | installed Implementation Readiness authoring validator | pass |
| Canonical/record/projection/package contracts | task-local Node tests | not run; files absent by design |
| Valid fixture/compiler/mutants/snapshot | task-local Node tests and `--check` | not run |
| Synthetic witness | full suite, isolated repeated compile/byte compare, JSON validation | not run |
| IDE/runtime/browser/accessibility/UX | separate L2 Work Pack | out of scope |

## Dispatch technique trace

| Technique | Applied to | Evidence/gate | Status |
| --- | --- | --- | --- |
| `sequence` | Design -> layers -> waves -> tasks -> SWUs -> closeout | every unit has ordered predecessors/successor | pass |
| `scu_swu_reduction` | ten SWUs | split analysis and one primary behavior each | pass |
| `recomposition_proof` | L0 -> L1 -> L2 | projection contract is stable handoff; evidence states stay separate | pass |
| `validation_loop` | every slice/SWU | exact command or reviewable check plus receipt | pass |
| `owner_boundary_check` | Plan/Task Session/Invoke Refresh/corpus/IDE/authority | no owner boundary collapsed | pass |
| `handle_handoff` | task source anchors | paths/selectors, not copied authority | pass |
| `residue_ledger` | L1 selection and deferred product/effect work | named owners/routes | pass |
| `execution_receipt_handoff` | all SWUs | terminal execution and closeout receipts defined before mutation | pass |

Full governed multi-agent dispatch: not required. The confirmed route has no subagents, the Work Pack is sequential, and the current machine projection exposes one local Task Session unit.

## Distill validation summary

- Result: `pass`; full artifact at `DISTILL-VALIDATION.md`.
- Smallest coherent first unit: SWU-CAL-001.
- SWU atomicity: pass, task-shaped count 0.
- Recomposition: pass; each unit builds the L0 package/projection proof and L0 feeds L1 without evidence reclassification.
- Hidden acceptance-critical gaps: none for synthetic L0.
- Named non-blocking gap: corpus-owner real-tower decision belongs to L1.
- Deferred complexity: IDE, browser/UX, multi-tower, graph, external/public/authority effects.

## Blocker and residue ledger

| ID | Class | Scope | Owner | Resolution/route | Current effect |
| --- | --- | --- | --- | --- | --- |
| GAP-CAL-L1-001 | planned owner prerequisite | real representative/mechanics tower | corpus owner | separate decision packet after L0 | no L0 block; blocks L1 |
| GAP-CAL-L2-001 | deferred integration | direct GET and trusted shell | IDE owner | separate L2 Invoke/Work Pack | no L0 block |
| GAP-CAL-COVERAGE-001 | evidence unknown | non-`TOWER.md` denominator and all-research scope | future corpus governance | new bounded research/owner decisions | forbids completeness claim |
| STOP-CAL-AUTH-001 | protected effect | authority/promotion/publication/deployment/release | respective named owners | separate exact decisions | never automatic |

## Current state and next owner

- Work Pack: selection-ready, not execution-authorized.
- First future execution owner after an explicit request: `implementation-readiness:execute`, which may select only SWU-CAL-001 from the current projection.
- Refine confirmation is not that request.
- No product files, commands, Task Sessions, external effects, commits, or pushes occurred.
