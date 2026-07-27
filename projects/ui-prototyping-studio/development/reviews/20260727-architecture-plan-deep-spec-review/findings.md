# Findings — UI Prototyping Studio Architecture, Plan, And Deep-Spec Review

Dispatch:
`2026-07-27-ui-prototyping-studio-architecture-plan-review`

Status: accepted review change requests; implementation not authorized

This review is read-only. FIX verdicts are change-request deliverables, not
implementation authorization. Nothing here promotes the June deep-spec package,
admits the July plan, mutates Craft, selects an SWU, or establishes release
readiness.

## Evidence Boundary

- Typecheck passed.
- Unit/slice tests passed: 62/62.
- The standard Playwright helper failed before browser assertions with
  `ERR_VM_DYNAMIC_IMPORT_CALLBACK_MISSING`.
- A temporary local-`tsx` diagnostic route passed the 13 existing browser
  scenarios. That is diagnostic evidence only, not a checked-in receipt and not
  proof of the new governed-state behaviors.
- Independent-process probing reproduced stale preview state after an external
  CLI change.
- A CSS-only probe was scope-permitted for staging and produced zero displayed
  diff fragments.
- A confirmed handoff with five missing references still set all three current
  readiness flags true.
- Diagnostic side effects were removed; Studio target artifacts were not
  changed by the review.

Inventory supplied selectors and earlier risks only. It supplied no Evidence
Card or EvidenceSet and is not finding evidence.

## Governance And Current Contracts — FIX

| ID | File(s) | Evidence | Severity | Proposed fix |
|---|---|---|---|---|
| F-01 | `.craft/ledger.yml`; `CRAFT.md`; root `README.md`, `ARCHITECTURE.md`, `SPEC.md`, `WORK-PACK.md`; July `README.md`, `WORK-PACK.md` | The ledger declares `"status: candidate-local"` and `"source_of_truth"` but still routes `"Execute extraction"`. July calls its work-pack `"canonical execution plan"` while that work-pack says `"status: proposed"` and records a flagged distill result. | MAJOR | Reconcile current-state authority, normative architecture, proposal evidence, receipts, execution authorization, and release authorization separately; bind or reject July and select exactly one next unit. |
| F-11 | `CRAFT.md`; root `README.md`, `ARCHITECTURE.md`, `SPEC.md`, `WORK-PACK.md`; `development/PLAN-NEXT.md` | `"53 unit tests + 12"` conflicts with current 62-unit evidence; `"whole work pack EXECUTED"` appears beside `"Non-executed"`; active prose retains read-only/human-only and built `[PROPOSAL]` claims. | MINOR | Separate dated historical receipts from current reproducibility and synchronize active prose only through the owning gate. |

Sources: Alexander initial/final, Turing initial/final, Beer initial/final,
Russell initial/final, Schön initial/final.

Authority verdict: the Craft ledger is the declared scoped state authority, but
its `candidate-local` and stale routing cannot currently establish admission,
supersession, execution authorization, or release authorization. Current
SPEC/ARCH files also require explicit owner admission before being treated as
the normative contract.

## July Governed-State Architecture And Execution Plan — FIX

| ID | File(s) | Evidence | Severity | Proposed fix |
|---|---|---|---|---|
| F-02 | July `WORK-PACK.md`, `EXECUTION-PACK.md`, `TASK-GSP-001-current-head-projection.md`, `TASK-GSP-004-validation-handoff-docs.md` | Runner repair declares `"Dependencies: none"`, the board says `"ready-after-GSP-001"`, routing says `"SWU-GSP-001 only"`, and GSP-001 requires Playwright. A focused GSP-001 spec could bind local `tsx` directly, so the defect is contradictory/underspecified standard proof routing, not logical impossibility. | MAJOR | Choose one checked-in proof route—shared runner prerequisite or focused GSP-001 local-executable binding—and align board, dependencies, and validation command. |
| F-07 | `.craft/ledger.yml`; July `TASK-GSP-003-action-annotation-mobile.md` | DEC-026 permits agent acceptance; July requires `"I inspected this change"` and prevents history advance without confirmation, but does not establish whether acknowledgment is actor-neutral or human-only. | MAJOR | Owner-decide actor-neutral acknowledgment versus human gating; otherwise keep the recap advisory. |
| F-08 | July `ARCHITECTURE-UPGRADE.md`; `TASK-GSP-001-current-head-projection.md` | Architecture says the adapter `"should render a projection object"` and must not decide truth; the task permits `"Add or inline a projection helper"`. | MAJOR | Require an application-owned typed projection contract or narrow the architecture to a preview-local repair. |
| F-09 | July `WORK-PACK.md`; all task and wave files | Five slices map to six manifest SWUs; Task 004 defines `004`, `005`, and unmanifested `005-DOC`; Task 005 owns `006`. | MAJOR | Publish one stable slice/task/SWU/wave crosswalk with unique scope, owner, dependencies, and receipt per executable ID. |

The July architecture direction is worth keeping, but it remains a flagged,
unadmitted proposal. Its execution surfaces require FIX before an owner selects
a task-session.

## Live Current-State Projection — FIX

| ID | File(s) | Evidence | Severity | Proposed fix |
|---|---|---|---|---|
| F-03 | `backend/src/modules/ui-prototyping-studio/infrastructure/file-studio-session-store.ts`; `backend/src/cli/studio.ts` | `"let documentState = loadDocument(filePath)"` loads once; `getSession` reads the snapshot despite `"State is read fresh per request"`. Two-process probing left preview at `RevisionApplied/rev-0000` after persisted state reached `RevisionRecorded/rev-0001`. | MAJOR | Reload or version-check persisted state per request and prove independent-process visibility and concurrency behavior. |
| F-04 | `backend/src/cli/studio.ts` | Primary cards use `"/raw/variant/"`; annotation uses `"/annotate/variant/${session.baseline.label}"`; comments are stored against `snap.revisionHeadId`. | MAJOR | Make current-head projection primary and annotation-bound; retain variants explicitly as historical lineage. |

`backend/src/modules/ui-prototyping-studio/application/current-html.ts` is
**KEEP**: its current-head resolution order survived attack. The projection and
store consumers around it are FIX.

## Visible-Change Evidence — FIX

| ID | File(s) | Evidence | Severity | Proposed fix |
|---|---|---|---|---|
| F-05 | `backend/src/modules/ui-prototyping-studio/application/admission.ts`; `backend/src/cli/studio.ts` | `"<style> nodes are excluded"` while the UI says `"Honest per-component diff"`; a CSS-only change returned `NOT_REJECT` with zero fragments/counts. `NOT_REJECT` means scope-permitted for staging, not admitted or promoted. | MAJOR | Add explicit style/global/unattributed lanes to diff, preview, and handoff evidence. |

## Evidence Harness — FIX FIRST

| ID | File(s) | Evidence | Severity | Proposed fix |
|---|---|---|---|---|
| F-06 | `backend/e2e/helpers.ts` | Helpers invoke `"pnpm", ["exec","tsx"...]`; failure becomes nullable JSON; preview exit only calls `"clearTimeout(timer)"` without resolving or rejecting. | MAJOR | Use checked-in local `tsx`, preserve command and stderr, and reject immediately on premature process exit. |

The normal 13/13 red result is a harness-path failure, not 13 demonstrated
product failures. The temporary shim-green result does not create a standard
receipt or prove GSP behavior.

## Handoff Readiness Semantics — FIX

| ID | File(s) | Evidence | Severity | Proposed fix |
|---|---|---|---|---|
| F-14 | `backend/src/modules/ui-prototyping-studio/application/export-design-handoff.ts`; `backend/src/modules/ui-prototyping-studio/domain/models.ts`; `backend/src/modules/ui-prototyping-studio/application/ui-prototyping-studio.slice.test.ts` | `missingRefs` is computed and stored, then readiness is unconditionally set to `"uiPhaseBridgeReady: true"`, `"generateTestsUiReady: true"`, and `"uiImplementReady: true"`. The current test confirms export with missing nested refs and expects all three true. | MAJOR | Persist `exportConfirmed` and `evidenceComplete` separately; derive completeness from `missingRefs.length === 0`; require independent integration/implementation predicates; keep release authorization separate; add an incomplete-evidence regression. |

This finding was raised by both verifiers and supported by all three attackers
through the declared feedback edge.

## Deep-Spec Disposition — KEEP AS HISTORICAL EVIDENCE

| Artifact | Verdict |
|---|---|
| `development/deep-spec-dispatch/RESULT.md` | KEEP as the explicit proposal/non-promotion and conditional-readiness boundary. |
| `SYNTHESIZED-DEEP-DESIGN.md`; `DEEP-SPEC-PROPOSAL.md`; `RESIDUALITY-STRESSORS.md` | KEEP as historical and promote-later intent, never canonical wholesale. |
| `UX-EVIDENCE-REPORT.md`; `COLD-START-USABILITY-FINDINGS.md` | KEEP as calibration/historical evidence; require current retest for current claims. |
| `ONE-SHOT-IMPLEMENTATION-PLAN.md`; `PLAYWRIGHT-TEST-PLAN.md` | KEEP as traceability/fixture catalogs; retire as current executable authority. |

The standalone deep-spec crosswalk finding was dropped. Craft and SPEC already
preserve broad June lineage, and no admitted law requires July to disposition
every historical intent. Only decisions or residue that conflict with the
current authority reconciliation must be carried into F-01.

## Authority And Supersession Recommendation

```text
operator-reconciled Craft ledger
  ├─ current-state and lifecycle authority
  ├─ explicitly admitted SPEC/ARCH versions
  │    └─ normative product and architecture contracts
  ├─ selected SWU + dependency/write-scope/receipt binding
  │    └─ execution authorization
  └─ separate release owner/gate
       └─ release authorization

live code + immutable receipts
  └─ observed implementation evidence only

July governed-state package
  └─ newest flagged proposal; authority effect none until admitted

June deep-spec + root work-packs
  └─ historical proposal, intent, and execution lineage

Inventory + this review
  └─ non-authority discovery/audit read models
```

## Dependency-Safe Next Recommendation

1. Reconcile Craft, remove unadmitted canonical wording, stabilize IDs, bind a
   receipt path, and explicitly select one proof-route/SWU.
2. Normalize the checked-in browser proof route: either a shared runner
   preflight or a focused GSP-001 spec directly bound to local `tsx`; require
   stderr preservation and early-exit rejection.
3. Execute the projection/current-state SWU with an application-owned contract,
   per-request freshness, and independent-process Accept/Revert/external-write
   witnesses.
4. Execute the CSS/global/unattributed evidence slice; its unit proof can be
   independent, while browser/handoff integration follows the projection
   witness.
5. Repair handoff evidence/readiness semantics.
6. Owner-decide actor-neutral confirmation semantics, then run the approved
   action/annotation/mobile slice.
7. Synchronize Craft and root documentation from dated receipts.
8. Keep Open Design/evidence-profile work last and non-authoritative.

## Ordered Change Requests

1. F-01 — reconcile authority, admission, execution, and supersession.
2. F-02 — select and normalize one checked-in browser proof route.
3. F-03 — make persisted state fresh across processes.
4. F-04 — project and annotate the governed current head.
5. F-05 — represent CSS/global visible changes honestly.
6. F-06 — make the evidence harness deterministic and fail-fast.
7. F-07 — owner-decide confirmation semantics.
8. F-08 — preserve the claimed application projection boundary.
9. F-09 — stabilize all executable identities and receipts.
10. F-14 — separate export confirmation from evidence and readiness.
11. F-11 — synchronize current-facing documentation after receipts.

## Dropped Or Refuted Candidates

- F-10: dropped standalone; only conflict-bearing deep-spec lineage remains
  under F-01.
- F-12: dropped because `/raw/baseline` semantics are disputed and no governed
  vocabulary requires a rename.
- F-13: refuted because the proposed evidence pack explicitly forbids authority
  or gate bypass; its name alone does not establish a defect.

## Verifier Convergence State

- Russell final verdict: `PASS`.
- Schön final objection: F-02 overstated logical impossibility.
- Resolution at the declared zig-zag cap: the exact objection was applied.
  F-02 now says the standard proof route is contradictory and underspecified;
  it does not claim no receipt can be produced.

## Approval

- Coverage auditor: `ACCEPT`; no coverage blockers.
- Parent final approver: `ACCEPT`.
- Accepted change requests: 11 total — 10 MAJOR and 1 MINOR.
- No CRITICAL finding survived verification.
- F-10, F-12, and F-13 remain dropped or refuted as recorded above.
- This approval accepts the review result only. It does not authorize
  implementation, admit the July plan, promote the June deep spec, mutate
  Craft, select an SWU, or establish release readiness.
