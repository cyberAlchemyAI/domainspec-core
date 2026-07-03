---
module: r3-closeout-plan
feature_code: R3C
version: current
status: draft
updatedAt: 2026-07-02
docType: work-pack
---

# WORK-PACK: R3 Closeout Plan

Canonical executable plan for the post-R3A residue. It does not reopen R3A. It turns the remaining
work into SWUs with owner boundaries and validation surfaces.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | flag | First L0/L1 SWUs are executable; full closeout includes deferred owner gates. |
| complexity | medium | Crosses APE, definitions, Craft, and authority closeout, but remains in one project. |
| outputMode | split | Task and wave files are provided under `work-pack/`. |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) | Wave choreography only; SWUs remain here and in task files. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | Layer governance and promotion decisions. |
| dispatchTechniqueTrace | [r3-closeout.dispatch.json](r3-closeout.dispatch.json) | Full dispatch JSON required because this plan crosses capabilities and owner routes. |
| distillValidationStatus | flag | Executable first unit exists; future candidates/category laws/attestation remain owned gaps. |
| activeLayerWindow | L0 | Start with dynamic DS-D8 code-tag composability enforcement. |
| lastUpdatedAt | 2026-07-02 | |
| readinessProfile | pilot | R3 closeout readiness, not public/release packaging. |

## Objective Summary

- Objective: finish the actionable post-R3A closeout path by wiring dynamic DS-D8 enforcement, broadening
  evidence, triaging pattern-card context, and routing non-R3 residues to their proper owners.
- Primary inputs: [../../CRAFT.md](../../CRAFT.md), [../reformulate-batch1/task-sessions/2026-07-02-swu-r3a/TASK-SESSION-RESULT.md](../reformulate-batch1/task-sessions/2026-07-02-swu-r3a/TASK-SESSION-RESULT.md), [../architecture-pattern-enforcement/WORK-PACK.md](../architecture-pattern-enforcement/WORK-PACK.md), [../../definitions/relationships/relationships.yml](../../definitions/relationships/relationships.yml).
- Success condition: R3 current-state artifacts agree that relationship authority is complete; APE has dynamic DS-D8 enforcement evidence; remaining deferred relation/category/attestation items are explicitly routed, not listed as R3 blockers.

## Planning Mapping

| Planning Source | Work-Pack Target | Mapping Rule |
| --- | --- | --- |
| R3A receipt | L0 input and non-reopen boundary | Consume root authority and validator evidence; do not re-decide signatures. |
| Craft current state | Active gaps and task board | Keep `GAP-DSV2-COMPOSABILITY-ENFORCE`, `GAP-DSV2-EXERCISE`, and `GAP-DSV2-APE-CARD-TRIAGE` visible. |
| APE package | TASK-R3C-EDGE, TASK-R3C-CORPUS, TASK-R3C-CARDS | Convert R3A-unblocked APE work into executable SWUs. |
| Definitions/relationships | Source contract for edge law | Read root DS-D8; never make implementation projection authoritative. |
| Deferred candidates | TASK-R3C-FUTURE | Evidence route only; no automatic promotion. |
| Attestation blocker | TASK-R3C-AUTHORITY | Human/capability gate; no false closure. |

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-R3C-001 | Dynamic DS-D8 code-tag composability enforcement | L0 | [W0](work-pack/waves/W0.md) | R3A receipt | `npm --prefix projects/domainspec-v2/impl run tags:test`; seeded strict failure |
| S-R3C-002 | Evidence breadth over a second pack/corpus | L1 | [W1](work-pack/waves/W1.md) | S-R3C-001 | `validate`, `validate:content`, `validate:rels`, `tags:composability` |
| S-R3C-003 | Pattern-library cards triaged into v2 evidence | L1 | [W1](work-pack/waves/W1.md) | S-R3C-002 can run in parallel after source selection | `validate:docs`; manifest/evidence links resolve |
| S-R3C-004 | Future candidates and category laws routed | L2 | [W2](work-pack/waves/W2.md) | S-R3C-001 | Review packets exist; owner gates named |
| S-R3C-005 | R3 closeout ledger/observer/attestation handoff | L3 | [W3](work-pack/waves/W3.md) | S-R3C-001..004 | Craft YAML parse, docs validate, observability JSONL parse |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [TASK-R3C-EDGE](work-pack/tasks/TASK-R3C-EDGE.md) | Refactor code-tag composability to consume root DS-D8 | L0 | medium | [W0](work-pack/waves/W0.md) | DS-D8, APE C-B | ready | not-started |
| [TASK-R3C-CORPUS](work-pack/tasks/TASK-R3C-CORPUS.md) | Add/select a second corpus and prove edge checks beyond financial-settlement | L1 | medium | [W1](work-pack/waves/W1.md) | Craft `GAP-DSV2-EXERCISE` | ready-after-edge | not-started |
| [TASK-R3C-CARDS](work-pack/tasks/TASK-R3C-CARDS.md) | Triage v1 pattern-library cards into v2 evidence | L1 | medium | [W1](work-pack/waves/W1.md) | APE `TASK-CARDS` | ready | not-started |
| [TASK-R3C-FUTURE](work-pack/tasks/TASK-R3C-FUTURE.md) | Route deferred relation candidates and category laws | L2 | medium | [W2](work-pack/waves/W2.md) | R3A residue | ready-after-edge | not-started |
| [TASK-R3C-AUTHORITY](work-pack/tasks/TASK-R3C-AUTHORITY.md) | Sync closeout ledger/observer and route attestation | L3 | medium | [W3](work-pack/waves/W3.md) | Craft + authority blocker | blocked-on-attestation-for-final-seal | not-started |
| [TASK-R3C-VERIFY](work-pack/tasks/TASK-R3C-VERIFY.md) | Completion verification and recomposition check | L3 | low | [W3](work-pack/waves/W3.md) | all tasks | ready-after-implementation | not-started |

## SWU Manifest

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-R3C-001 | [TASK-R3C-EDGE](work-pack/tasks/TASK-R3C-EDGE.md) | `impl/governance/tags/tools/check-code-tag-composability.ts`; `impl/tools/lib/relationship-signatures.ts`; `definitions/relationships/relationships.yml` | APE C-B, DS-D8 | none | `projects/domainspec-v2/impl/governance/tags/tools/check-code-tag-composability.ts`; optional shared helper imports | Checker loads root DS-D8 active signatures instead of static pre-R3 rule table; generated/deprecated/deferred labels do not become active authored checks. | Diff shows static rules removed or generated from authority; JSON report names authority path and active signature count. | `npm --prefix projects/domainspec-v2/impl run tags:test`; focused `tags:composability -- --json` on fixtures | local-fallback | selected-first |
| SWU-R3C-002 | [TASK-R3C-EDGE](work-pack/tasks/TASK-R3C-EDGE.md) | `impl/governance/tags/tools/tests/code-tag-composability.test.ts`; relationship fixtures | R3A invalid endpoint fixtures | SWU-R3C-001 | `projects/domainspec-v2/impl/governance/tags/tools/tests/`; `impl/governance/tags/examples/composability/` | Tests cover active edge pass, bad endpoint fail, `owned-by` noncanonical, `enforces-cross` deprecated, and at least one deferred candidate not enforced as active. | `tags:test` fails before fix/pass after fix for seeded cases. | `npm --prefix projects/domainspec-v2/impl run tags:test` | local-fallback | ready-after-001 |
| SWU-R3C-003 | [TASK-R3C-EDGE](work-pack/tasks/TASK-R3C-EDGE.md) | `impl/package.json`; `CODE-TAG-COMPOSABILITY-PATTERNS.md`; APE docs | aggregate validation | SWU-R3C-001, SWU-R3C-002 | docs/scripts only if needed | Dynamic DS-D8 composability is documented and, if appropriate, wired into `npm run validate` without breaking existing gates. | `validate`, `engine:test`, `typecheck` pass; docs state root authority, not implementation projection. | `npm --prefix projects/domainspec-v2/impl run validate`; `engine:test`; `typecheck` | local-fallback | ready-after-002 |
| SWU-R3C-004 | [TASK-R3C-CORPUS](work-pack/tasks/TASK-R3C-CORPUS.md) | `impl/spec/features/financial-settlement/`; toy graph; APE work-pack | second-corpus gap | SWU-R3C-001 | new or selected `impl/spec/features/<second-pack>/` plus tests if new | A second corpus/pack exercises additional DS-D8 signatures or records why no owned corpus is suitable. | Valid pack passes node and edge validation; seeded invalid edge fails. | `validate:content`; `validate:rels`; `tags:composability` if code tags exist | subagent | ready-after-001 |
| SWU-R3C-005 | [TASK-R3C-CARDS](work-pack/tasks/TASK-R3C-CARDS.md) | `implementation/domainspec/architecture/pattern-library/concepts/backend/`; `IMPORT-MANIFEST.md` | APE TASK-CARDS | none | v2 card layer path chosen inside `projects/domainspec-v2/`; `IMPORT-MANIFEST.md` rows | Backend concept cards are copied/linked as evidence without making v1 authoritative; manifest records provenance. | Links resolve; each imported card has owner/evidence note. | `npm --prefix projects/domainspec-v2/impl run validate:docs` | subagent | ready |
| SWU-R3C-006 | [TASK-R3C-CARDS](work-pack/tasks/TASK-R3C-CARDS.md) | v1 relationship cards; `definitions/relationships/relationships.yml` | DS-D8 active/generated/deferred sections | SWU-R3C-005 | v2 relationship-card evidence/staging path | Relationship cards are triaged against active/generated/deprecated/deferred DS-D8 states; deferred candidates stay staged. | Triage table exists; no deferred card is marked active. | review check + `validate:docs` | subagent | ready-after-005 |
| SWU-R3C-007 | [TASK-R3C-FUTURE](work-pack/tasks/TASK-R3C-FUTURE.md) | R3A residue; `definitions/relationships/relationships.yml` deferred candidates | definitions-governance | SWU-R3C-001 | `definitions/reviews/` or `development/reformulate-batch1/governance/` review packet | `depends-on`, Operation-returned Value Object, and Event payload/publisher each get promote/defer/reject evidence criteria. | Review packet names witness needed and owner route; no authority mutation. | review check; `validate:docs` | manual | ready-after-001 |
| SWU-R3C-008 | [TASK-R3C-FUTURE](work-pack/tasks/TASK-R3C-FUTURE.md) | category-boundary research; DS-D8; D16/D17 | research/definitions-governance | SWU-R3C-001 | category-law plan/review packet | Category-law formalization scope is separated from R3A and gets candidate laws, examples, non-examples, and validation owner. | Packet says whether next route is research-tower, definitions-governance, or decision-gate. | review check; `validate:docs` | manual | ready-after-001 |
| SWU-R3C-009 | [TASK-R3C-AUTHORITY](work-pack/tasks/TASK-R3C-AUTHORITY.md) | `.craft/ledger.yml`; `CRAFT.md`; observability streams | Craft + observer | SWU-R3C-001..008 as applicable | Craft/observer closeout files only | Ledger and human view agree; observability records closeout; attestation blocker remains explicit if unavailable. | Craft YAML parses; JSONL parses; stale active wording scan passes. | `python3 -c` YAML parse; JSONL parse; `git diff --check` | local-fallback | ready-after-execution |
| SWU-R3C-010 | [TASK-R3C-AUTHORITY](work-pack/tasks/TASK-R3C-AUTHORITY.md) | `BLK-DSV2-L2-ATTESTATION`; authority model | constitution-governance/human | SWU-R3C-009 | attestation handoff artifact | If attestation capability exists, produce seal request; otherwise leave blocker with exact closure condition. | Attestation receipt or explicit blocked handoff. | manual review | manual | blocked-until-capability |
| SWU-R3C-011 | [TASK-R3C-VERIFY](work-pack/tasks/TASK-R3C-VERIFY.md) | all receipts | task-session closeout | all non-deferred SWUs | no source mutation except result artifact | Final closeout report distinguishes complete R3A, completed downstream work, and future non-blocking routes. | `validate`, `engine:test`, `typecheck`, `validate:docs`, YAML/JSONL parse pass. | command suite + review | local-fallback | ready-after-implementation |

## Blockers And Gaps

| ID | Scope | Type | Owner | State | Repair Path |
| --- | --- | --- | --- | --- | --- |
| GAP-DSV2-COMPOSABILITY-ENFORCE | TASK-R3C-EDGE | active gap | APE / validation governance | executable | SWU-R3C-001..003 |
| GAP-DSV2-EXERCISE | TASK-R3C-CORPUS | active gap | Spec-ontology / APE | executable after L0 | SWU-R3C-004 |
| GAP-DSV2-APE-CARD-TRIAGE | TASK-R3C-CARDS | active gap | APE | executable | SWU-R3C-005..006 |
| R3C-GAP-FUTURE-RELATIONS | TASK-R3C-FUTURE | evidence gap | definitions-governance | not promotion-ready | SWU-R3C-007 |
| R3C-GAP-CATEGORY-LAWS | TASK-R3C-FUTURE | formalization gap | research/definitions-governance | not R3 blocker | SWU-R3C-008 |
| BLK-DSV2-L2-ATTESTATION | TASK-R3C-AUTHORITY | blocker | human/capability | blocks final authority seal only | SWU-R3C-010 |

## Dispatch Technique Trace

Full route document: [r3-closeout.dispatch.json](r3-closeout.dispatch.json).

| Technique ID | Applied To | Validation Expectation | Status |
| --- | --- | --- | --- |
| sequence | R3A receipt -> L0 enforcement -> L1 evidence -> L2 routing -> L3 closeout | Each later step consumes explicit receipts. | pass |
| scu_swu_reduction | SWU manifest | First unit is SWU-R3C-001; each SWU has one parent task and write scope. | pass |
| recomposition_proof | Layering and final verification | Downstream residue recomposes into Craft current state without reopening R3A. | pass |
| validation_loop | every delivery slice | Each slice has command or review evidence. | pass |
| owner_boundary_check | APE vs definitions/constitution/Craft | Plan does not claim promotion or attestation authority. | pass |
| delegation_boundary | task-session/manual/subagent execution | Each SWU names execution owner and return shape. | pass |
| execution_receipt_handoff | expected Task Session receipts | Receipts must record files, validation, blockers, residue. | pass |
| residue_ledger | blockers/gaps table | Future candidates and category laws stay owned. | pass |

## Distill Validation

| Check | Result | Evidence Or Gap |
| --- | --- | --- |
| Smallest coherent unit or SWU boundary | pass | SWU-R3C-001 is the first executable unit and does not require broader discovery. |
| Recomposition proof | pass | L0-L3 map directly to Craft active gaps and APE capabilities. |
| Hidden acceptance-critical gaps | flag | Attestation capability and category-law scope cannot be completed by this execution plan alone. |
| Deferred complexity | pass | Future candidates, category laws, and attestation are explicit owner routes. |
| Navigation to first executable unit | pass | Next route is `task-session` on SWU-R3C-001. |

**Verdict: flag.** Mutation-capable work may start with SWU-R3C-001; full R3 closeout remains flagged until
deferred owner gates are resolved or explicitly recorded as future non-blocking routes.

## Required Links

- [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md)
- [EXECUTION-PACK.md](EXECUTION-PACK.md)
- [PLAN-TRANSPORT.md](PLAN-TRANSPORT.md)
- [r3-closeout.dispatch.json](r3-closeout.dispatch.json)
- [work-pack/shared/context.md](work-pack/shared/context.md)
- [work-pack/shared/cross-task-gaps.md](work-pack/shared/cross-task-gaps.md)
- [work-pack/shared/traceability.md](work-pack/shared/traceability.md)

## Gate Checks

1. Do not execute more than one SWU without an execution receipt and work-pack sync.
2. SWU-R3C-001 is the selected first unit.
3. Parallel work is allowed only for disjoint write scopes: SWU-R3C-005 can run beside SWU-R3C-001; SWU-R3C-004 waits for L0 edge enforcement.
4. Deferred relation candidates and category laws cannot promote authority during this plan.
5. Attestation remains blocked unless a real attestation capability/receipt exists.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-07-02 | Initial Invoke plan package created after R3A follow-up closeout. | invoke |
