---
module: co-op-engine-browser-app
version: plan-v1-refresh-1
status: approved-l0
updatedAt: 2026-07-26
docType: work-pack
---

# WORK-PACK: Co-Op Engine L0 Trust and HTML Prototypes

## Control Fields

| Field | Value |
| --- | --- |
| workPackGateStatus | pass |
| complexity | medium |
| outputMode | split |
| executionPackRef | `EXECUTION-PACK.md` |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` |
| dispatchTechniqueTrace | `PLAN-DISPATCH-TRACE.md` |
| distillValidationStatus | pass |
| swuAtomicityStatus | pass |
| firstUnitNarrownessStatus | pass |
| closeoutSyncStatus | pass |
| activeLayerWindow | L0 |
| lastUpdatedAt | 2026-07-26 |
| readinessProfile | pilot |

## Objective

L0 contains two serial, independently reviewable proofs:

1. selected `SWU-COOP-001` implements one deterministic `ProjectRecord`
   admission decision for the normalized Poker Agent Arena fixture;
2. planned `SWU-COOP-002` creates one self-contained, research-derived HTML
   content/IA prototype containing the event route and all fourteen projects.

Only `SWU-COOP-001` is selected. The HTML unit requires successful closeout,
explicit later selection, and a new strict context pack. Neither unit proves
the operational exchange, final copy, comprehension, privacy, recruitment,
deployment, or public readiness.

## Source Contracts

- [Architecture bundle](ARCHITECTURE-BUNDLE.md) — `RecordSchema`,
  `AdmissionValidator`, L0 witness
- [Approved specification](SPEC.md) — record, policy, admission, privacy
- [Design acceptance review](DESIGN-ACCEPTANCE-REVIEW.md) — prohibited
  shortcuts and evidence ceiling
- [Implementation layering](IMPLEMENTATION-LAYERING.md) — active L0 boundary
- [Planning context](PLAN-CONTEXT.md) — exact design digests and exclusions

## Delivery Slices

| Slice | Outcome | Layer | Wave | Dependency | Validation |
| --- | --- | --- | --- | --- | --- |
| `S-L0-BASELINE` | exact source, runtime, scope, and absence baseline captured | L0 | [W0](work-pack/waves/W0.md) | approved Plan | strict context-pack/index validation |
| `S-L0-ADMISSION` | Poker record admission contract passes positive and negative fixtures | L0 | [W1](work-pack/waves/W1.md) | W0 pass | `npm --prefix projects/co-op-engine run test:contract` |
| `S-L0-HTML-PROTOTYPE` | one local HTML artifact exposes the event, 45-minute route, and fourteen bounded project opportunities | L0 | [W2](work-pack/waves/W2.md) | `SWU-COOP-001` terminal pass and closeout; explicit `SWU-COOP-002` selection; new strict pack | Playwright desktop/mobile structural and screenshot receipt |

## Task Board

| Task | Goal | Layer | Wave | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-COOP-L0-CONTRACT](work-pack/tasks/TASK-COOP-L0-CONTRACT.md) | admit or reject one `ProjectRecord` under current policy | L0 | W1 | ready after strict pack | not-started |
| [TASK-COOP-L0-HTML-PROTOTYPE](work-pack/tasks/TASK-COOP-L0-HTML-PROTOTYPE.md) | render all fourteen bounded opportunities and the meeting route in one static document | L0 | W2 | blocked until selected-unit closeout and explicit selection | planned |

## SWU Manifest

| SWU | Parent | Primary behavior | Write scope | Validation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `SWU-COOP-001` | [TASK-COOP-L0-CONTRACT](work-pack/tasks/TASK-COOP-L0-CONTRACT.md) | decide whether one candidate project record is admitted | `projects/co-op-engine/package.json`; `projects/co-op-engine/src/contracts/project-record.ts`; `projects/co-op-engine/test/fixtures/poker-record.ts`; `projects/co-op-engine/test/project-record.test.ts` | `npm --prefix projects/co-op-engine run test:contract` | local-fallback | selected |
| `SWU-COOP-002` | [TASK-COOP-L0-HTML-PROTOTYPE](work-pack/tasks/TASK-COOP-L0-HTML-PROTOTYPE.md) | render one complete semantic HTML content/IA prototype | `projects/co-op-engine/prototype.html` | Playwright CLI desktop/mobile black-box review plus scoped diff check | local-fallback | planned-unselected |

Machine-readable authority: `SWU-MANIFEST.json`.

## SWU Atomicity Review

| SWU | Candidate child units | Retained-boundary rationale | Verdict |
| --- | --- | --- | --- |
| `SWU-COOP-001` | structure-only; policy-only; freshness-only; visibility-only validators | none is a safe or useful admission decision alone; the result must either return one admitted record satisfying every invariant or a typed diagnostic set | pass |
| `SWU-COOP-002` | shell-only; project-copy-only; presentation-only; responsive-style-only; interaction | shell or copy alone cannot test whether the full portfolio and meeting narrative cohere; presentation is the same semantic document; responsive styling preserves meaning; interaction is independently verifiable and excluded | pass |

`SWU-COOP-001` continues to exclude every browser concern. `SWU-COOP-002`
excludes interaction, real projection state, admitted-data compilation,
leakage behavior, final copy, persistence, and deployment because each can
pass independently and belongs to a later layer.

## Implementation Detail

The task contract owns the exact algorithm. In summary:

1. define erasable TypeScript record/result/diagnostic types;
2. validate required strings and non-empty source/forbidden-claim arrays;
3. require policy `coop-card-policy-2026-07`, 72-hour SLA, and 30-day
   verification-to-expiry interval;
4. derive staleness from injected `asOf`, never wall-clock time;
5. require the candidate to declare `eligible`;
6. require one known visibility class for every required field path;
7. return all deterministic diagnostics in stable code/path order;
8. admit only when the diagnostic list is empty;
9. test normalized Poker positive and independent negative mutations.

The HTML task owns a separate content/IA algorithm:

1. create one dependency-free `prototype.html`;
2. render the invitation, honesty boundary, loop, 45-minute route, and
   participation choices in semantic order;
3. render exactly fourteen unique project articles from the accepted
   research substrate;
4. give each article a bounded current description, explicit limitation,
   seven-day act, and human contribution ask;
5. preserve domain voice and safe display labels;
6. use anchor navigation and inline responsive/print styling only;
7. omit forms, scripts, network resources, storage, private metadata, hidden
   presenter content, and operational-state claims;
8. validate through a real browser at desktop and mobile viewports.

## Validation Strategy

| Layer | Check | Evidence |
| --- | --- | --- |
| syntax/runtime | Node can load erasable TypeScript with the declared command | test process exit and TAP output |
| positive contract | normalized Poker fixture admitted | test name and assertion |
| negative policy | research-era 48-hour SLA rejected after D-003 | `SLA_POLICY_MISMATCH` |
| negative freshness | fixed `asOf` after expiry rejected | `STALE_RECORD` |
| negative truth | required claim/witness/source absent | exact missing-field diagnostic |
| negative visibility | required path absent or class unknown | `UNCLASSIFIED_FIELD` or `UNKNOWN_VISIBILITY_CLASS` |
| determinism | same input and `asOf` return byte-equivalent result | deep-equality assertion |
| hygiene | scoped diff has no whitespace errors | `git diff --check -- projects/co-op-engine` |

For `SWU-COOP-002`, see the HTML task’s black-box matrix. Its browser receipt
proves only document structure, complete fixture presence, responsive meaning,
console/network cleanliness, and captured appearance.

## Task Session Closeout Sync Contract

Authority: `CLOSEOUT-SYNC-CONTRACT.json`.

| SWU | Owner route | Terminal source receipt | Target inventory | Baseline | Allowed deltas | Owner validation | Expected owner receipt | Successor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SWU-COOP-001` | `invoke:refresh:apply-approved` | `work-pack/receipts/SWU-COOP-001.source-receipt.json` using the task result shape | this work-pack, task, W1, Plan transport, source/closeout receipts | strict pack SHA-256 for existing targets plus asserted absence of receipt files | evidence added; blocker opened/resolved; status/route changed | contract tests, scoped diff check, receipt/index validation | `work-pack/receipts/SWU-COOP-001.closeout.json` | none; require refreshed Plan for L1 |
| `SWU-COOP-002` | `invoke:refresh:apply-approved` | `work-pack/receipts/SWU-COOP-002.source-receipt.json` using the task result shape | this work-pack, HTML task, W2, refresh report, source/closeout receipts | future strict pack SHA-256 plus asserted absence of receipt files | evidence added; blocker opened/resolved; status/route changed | browser structural/mobile/network/screenshot checks, scoped diff, receipt/index validation | `work-pack/receipts/SWU-COOP-002.closeout.json` | none; require refreshed Plan for L1 |

Closeout cannot admit another SWU, public release, deployment, policy change,
promotion, or unrelated target.

## Blockers and Residue

| ID | Scope | State | Owner | Route |
| --- | --- | --- | --- | --- |
| `G-L1-DEFERRED` | real admitted-data page/presentation behavior | non-blocking for L0 | Plan owner | refresh and Plan after L0 |
| `G-D005` | public naming/release | non-blocking for L0; blocks public access | publication owner | Decision Gate before public release |
| `G-AUDITS` | UI/privacy/copy/comprehension evidence | planned, not executed | named validators | L1–L3 work |

`G-L1-DEFERRED` now means the real admitted-data application and interaction;
the L0 HTML content/IA prototype is planned separately. No unresolved gap
affects `SWU-COOP-001`. `SWU-COOP-002` remains non-executable until its
selection and strict-context gates pass.

## Dispatch Technique Trace

See `PLAN-DISPATCH-TRACE.md`. The canonical dispatch remains
`execution.dispatch.json` and validates with zero flags or blocks.

## Distill Validation

See `PLAN-DISTILL-VALIDATION.md`.

- smallest coherent unit: pass;
- SWU atomicity: pass;
- first-unit narrowness: pass;
- recomposition: pass;
- hidden acceptance-critical gaps: none;
- task-shaped count: zero;
- navigation: this file → task → SWU → strict pack → goal profile.

## Execution Handoff

The selected `SWU-COOP-001` may route only through its current validated strict
pack. `SWU-COOP-002` is not selected and may not route from this refresh. A
later operator must select it explicitly, build a fresh strict Markdown and
JSON/index pair, and use its exact one-file write scope.
