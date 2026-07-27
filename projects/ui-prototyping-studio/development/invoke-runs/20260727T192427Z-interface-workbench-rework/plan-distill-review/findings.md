# Plan Distill Findings

Dispatch:
`2026-07-27-ui-prototyping-studio-plan-distill-review`

## Verdict

**BLOCK.** Schön's bounded verifier zig-zag sustained **PD-01–08 and
PD-10 as MAJOR**, corrected PD-08's ownership rule, and reduced PD-09 to a
non-blocking MINOR. Nine MAJOR defects remain.

The architectural recomposition survives. The current literal Plan does not
yet support safe execution. `selected_swu: null` remains exact; all UPW
witnesses remain unexecuted; `authority_effect: none`.

## Verified Change Requests

| ID | Finding and literal evidence | Severity | Exact one-line repair | Affected scope | Blocks Plan pass |
| --- | --- | --- | --- | --- | --- |
| PD-01 | Mutation scopes are not exhaustive: `WORK-PACK.md:88-104` uses "coordinator/shell," "shell/projection," and "labels/copy"; `TASK-UPW-COORDINATOR.md:17-18` uses "same shell/coordinator," although preflight hashes every declared target at `WORK-PACK.md:116-117`. | MAJOR | Replace every SWU scope with exhaustive repo-relative existing paths, explicit `create-if-absent` paths, forbidden paths, and "all omitted paths unauthorized," then bind those exact targets to preflight hashes. | 001–017; mutation tasks; closeout | yes |
| PD-02 | 002 names only a "stable input identity/epoch" and "bounded constant," without token owner, equality rule, retry value, or terminal error at `TASK-UPW-PROJECTION.md:48-53`. | MAJOR | Name the authoritative token producer, exact equality rule, numeric retry bound, and typed exhaustion error in 002's algorithm and receipt. | 002; W0; UPW-FIX-016 | yes |
| PD-03 | 003 promises invalid-route failure at `TASK-UPW-PROJECTION.md:82-83`, while new route validation appears only in dependent 017 at `TASK-UPW-HARDENING.md:32-41` and `SWU-MANIFEST.json:10,24`. | MAJOR | Either move route-family validation before 003 and leave sandbox rendering in 017, or constrain 003 to already-valid existing route data and reserve new route admission for 017. | 003, 017; W0/W4; manifest | yes |
| PD-04 | 006 computes and restores a context plan at `TASK-UPW-COORDINATOR.md:50-53` before 007 defines its identity bindings and reconciliation at `:61-66`. | MAJOR | Either define a typed context-plan interface before 006, or have 006 journal/restore opaque context while 007 alone introduces identity-specific planning. | 006–007; W1; DDR-02 | yes |
| PD-05 | 016 bundles keyboard/pointer, focus, live scopes, color, contrast, and target size at `TASK-UPW-HARDENING.md:11-30`, with acceptance spanning UPW-FIX-008–012 and 021–022 at `:24-25`. | MAJOR | Split 016 into independently receipted children, at minimum interaction/focus/live behavior versus visual perceivability/target size, and verifier-test whether scoped-status semantics require a third child. | 016; W4; L2; manifest/closeout | yes |
| PD-06 | 017 combines server route admission with iframe sandbox/safe rendering at `TASK-UPW-HARDENING.md:32-48`. | MAJOR | Split 017 into route-family validation and iframe sandbox/safe-sink enforcement, positioning route admission consistently with the repaired 003 contract. | 017; W0/W4; L2; manifest/closeout | yes |
| PD-07 | 008–013 promise only a "named focused Playwright slice" at `TASK-UPW-REGIONS.md:35-40`; their rows provide prose rather than exact spec, selector/grep, positive assertion, negative mutant, and receipt field at `:14-21`. | MAJOR | Bind each of 008–013 to one exact spec path, grep/selector, positive assertion, negative mutant, and expected receipt field. | 008–013; W2 validation | yes |
| PD-08 | Acceptance assertions overlap ambiguously: 010 cites FIX-008, 012 cites FIX-009–010 at `TASK-UPW-REGIONS.md:18-20`, and 016 cites FIX-008–012 at `TASK-UPW-HARDENING.md:24`; traceability is only Design→SWU and lacks direct acceptance witnesses for 008/009/013 at `work-pack/shared/traceability.md:3-18`. | MAJOR | Add an inverse SWU→Design→assertion matrix, assign one primary acceptance owner per assertion, and add direct acceptance witnesses for 008/009/013 while retaining lawful shared witness, recomposition, and regression checks. | 008–013, 016; traceability/recomposition | yes |
| PD-09 | The manifest's single dependency chain at `SWU-MANIFEST.json:8-24` and wave prose mix semantic prerequisites with safe serialization ordering; W1–W4 explicitly justify serialization through overlapping writes at `W1.md:6-8`, `W2.md:6-9`, `W3.md:6-9`, and `W4.md:6-8`. | MINOR | Clarify in the existing manifest and waves which edges are semantic prerequisites and which are serialization-only; add new fields only if the local schema is intentionally revised and validated. | manifest; W0–W4 | no |
| PD-10 | Refresh receipts are declared at `WORK-PACK.md:113-126` but omitted from row inventories at `:128-150`, as are `EXECUTION-PACK.md` and `PLAN-TRANSPORT.md`; W5 gives no exact report path, schema, writable fields, or synchronization inventory at `TASK-UPW-VERIFY.md:37-41`. | MAJOR | Enumerate execution/refresh receipts plus work-pack, manifest, task, wave, execution-pack, and transport targets with schemas, field permissions, and successor effect, and give W5 an exact report path/schema/sync inventory. | 001–017 closeout; W5; transport | yes |

## Verifier Disposition

- Sustained MAJOR: PD-01–08 and PD-10.
- Corrected: PD-08 requires one primary acceptance owner per assertion, not
  globally unique witness ownership. Shared recomposition and regression use
  remains lawful.
- Refuted as framed and reduced: PD-09 is MINOR because the current serial
  order is safe and no mandatory field names are imposed.
- Overall: BLOCK remains because nine MAJOR findings survive.

## SWU Disposition

- KEEP: 001 after PD-01. It remains the narrowest reversible trust-building
  candidate and is recommended, not selected.
- KEEP after blocking repair: 002–007.
- KEEP after validation and acceptance repair: 008–015. Early split demands
  for 010–012 are withdrawn.
- SPLIT/BLOCK: 016 and 017.
- PD-09 changes no SWU disposition.

Stable dissent remains explicit:

- 003: Abramsky requires route validation before 003; Rittel also permits
  constraining 003 to existing-valid route input.
- 006: Abramsky requires a typed context-plan interface before 006; Rittel
  permits opaque context journaling in 006 with identity planning introduced
  by 007.
- 016: Abramsky's minimum is two children; Rittel argues scoped-status
  semantics may justify a third.

## Per-Artifact Verdict

| Artifact group | Verdict |
| --- | --- |
| `DESIGN-DISTILL.md`, `PLAN-CONTEXT.md`, `PLAN-TEMPLATE-SELECTION.md`, `PLANNED-WITNESSES.json` | KEEP authority and evidence ceilings |
| `IMPLEMENTATION-LAYERING.md`, `IMPLEMENTATION-PLAN.md` | FIX 003/006 ordering and 016/017 decomposition |
| `WORK-PACK.md`, `SWU-MANIFEST.json` | FIX sustained contracts and PD-09 clarification; preserve `selected_swu: null` |
| `EXECUTION-PACK.md`, W0–W5 | FIX regenerated decomposition, ordering, and closeout choreography |
| `PLAN-VALIDATION-STRATEGY.md`, `WITNESS-CONTRACTS.md` | FIX exact per-SWU assertions, primary acceptance ownership, and receipt bindings; semantic witness contracts otherwise KEEP |
| Projection, Coordinator, Regions, Responsive/Copy, Hardening, Verify task files | FIX under PD-01–08 and PD-10 |
| `shared/context.md`, `cross-task-decisions.md` | KEEP boundary; FIX exact scopes and edge clarification |
| `shared/traceability.md`, `cross-task-gaps.md` | FIX inverse assertion coverage and unsupported completeness claim |
| `PLAN-TECHNIQUE-TRACE.md`, `PLAN-TRANSPORT.md`, `PLAN-DISTILL.md` | FIX after repair, regeneration, and literal verification |
| Inventory packet | KEEP discovery-only; no authority effect |

## Recomposition, Deferred Complexity, And Expiry

Recomposition remains:

`001 digest → 002 coherent read → 003 transport → 004 inert shell → 005 action
freshness → 006 atomic commit → 007 context → 008–013 regions → 014 responsive
order → 015 copy → repaired 016 interaction semantics → repaired 017 content
boundary → W5 closure`.

Deferred complexity remains correctly outside the Plan: framework migration,
push transport, durable browser authority, remote origins, human study,
cross-browser generalization, accessibility certification, release,
deployment, and production readiness.

This verdict binds the rechecked current bytes and expires if SWU boundaries,
dependency meaning, mutation targets, assertion mappings, closeout schemas, or
Design contracts change.

