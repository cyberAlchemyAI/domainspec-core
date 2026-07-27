# Revised Synthesis — UI Prototyping Studio Architecture Review

Status: candidate review deliverable for final verifier convergence only. No
implementation, admission, promotion, execution, or release claim.

## Per-Artifact KEEP/FIX Matrix

| Stratum | Artifact(s) | Verdict |
|---|---|---|
| Craft | `projects/ui-prototyping-studio/.craft/ledger.yml`; `CRAFT.md` | **FIX** F-01/F-11 |
| Root contracts | `README.md`; `ARCHITECTURE.md`; `SPEC.md` | **FIX** F-01/F-11 |
| Root plans | `WORK-PACK.md`; `development/PLAN-NEXT.md` | **KEEP as lineage/receipt; FIX/retire as current routing** |
| Deep-spec boundary/intent | `development/deep-spec-dispatch/RESULT.md`; `SYNTHESIZED-DEEP-DESIGN.md`; `DEEP-SPEC-PROPOSAL.md`; `RESIDUALITY-STRESSORS.md`; `UX-EVIDENCE-REPORT.md`; `COLD-START-USABILITY-FINDINGS.md` | **KEEP as proposal/historical evidence**; reconcile only conflict-bearing lineage through F-01 |
| Deep-spec execution surfaces | `ONE-SHOT-IMPLEMENTATION-PLAN.md`; `PLAYWRIGHT-TEST-PLAN.md` | **KEEP as traceability/catalog; retire as current executable authority** |
| July architecture | `ARCHITECTURE-UPGRADE.md`; `IMPLEMENTATION-LAYERING.md`; `INVOKE-RESULT.md`; `PLAN-TRANSPORT.md` | **KEEP flagged; FIX** F-01/F-02/F-08/F-09 |
| July execution | `README.md`; `WORK-PACK.md`; `EXECUTION-PACK.md`; all `work-pack/tasks/*.md`; all `work-pack/waves/*.md` | **FIX** F-01/F-02/F-07/F-08/F-09 |
| Current-head resolver | `backend/src/modules/ui-prototyping-studio/application/current-html.ts` | **KEEP** |
| Persistence | `backend/src/modules/ui-prototyping-studio/infrastructure/file-studio-session-store.ts` | **FIX** F-03 |
| Browser projection | `backend/src/cli/studio.ts` | **FIX** F-03/F-04/F-05/F-07 |
| Diff | `backend/src/modules/ui-prototyping-studio/application/admission.ts` | **FIX** F-05 |
| Evidence harness | `backend/e2e/helpers.ts` | **FIX first** F-02/F-06 |
| Handoff readiness | `backend/src/modules/ui-prototyping-studio/application/export-design-handoff.ts`; `domain/models.ts`; `application/ui-prototyping-studio.slice.test.ts` | **FIX** F-14 |

## Authority And Supersession Model

- **Current-state authority:** operator-reconciled Craft ledger. It is
  presently only declared and `candidate-local`; stale routing prevents it from
  establishing the current next unit.
- **Normative architecture:** explicitly owner-admitted `SPEC.md` and
  `ARCHITECTURE.md` versions. Current files are drafts containing superseded
  active prose.
- **Proposal evidence:** June deep-spec and July governed-state package.
  Authority effect remains none.
- **Reproducibility receipts:** code, tests, and probes establish observed
  behavior only.
- **Execution authorization:** explicit owner/gate selection of one stable SWU,
  write scope, dependencies, and receipt path. Currently absent for July.
- **Release authorization:** separate named release owner/gate. Currently
  absent and never implied by export or readiness flags.

Supersession recommendation: reconcile Craft; admit current normative contracts
separately; register July as proposal-only; retain root plans and June deep-spec
as historical lineage; carry only conflicting decisions/residue into the
authority reconciliation. Do not require wholesale deep-spec disposition.

## Dependency-Safe Next Sequence

1. Reconcile Craft, remove July’s unadmitted “canonical” wording, stabilize
   task/SWU IDs, bind a receipt path, and explicitly authorize one
   runner-preflight SWU.
2. Runner preflight: checked-in local `tsx`, preserved stderr/command,
   immediate early-exit rejection; prove the standard 13-test route.
3. Projection SWU: application-owned projection contract plus persisted-state
   reload/version check; prove current-head, annotation identity, Accept/Revert,
   and independent-process visibility.
4. Style evidence SWU: CSS-only unit witness plus browser/handoff assertion
   that a scope-permitted staged visible change cannot display zero evidence.
5. Handoff semantics SWU: separate export confirmation, evidence completeness,
   integration readiness, and implementation readiness before documentation
   synchronization.
6. Owner-decide actor-neutral confirmation semantics against DEC-026; then run
   the approved action/annotation/mobile slice.
7. Synchronize Craft/root documentation from dated receipts.
8. Keep Open Design/evidence-profile work last and non-authoritative.

## Candidate Change Requests

### MAJOR

- **F-01 — Authority/supersession conflict.** Paths: `.craft/ledger.yml`,
  `CRAFT.md`, root contracts/plans, July `README.md`/`WORK-PACK.md`,
  conflict-bearing June lineage. Evidence: ledger declares
  `"status: candidate-local"` and `"source_of_truth"` but routes
  `"Execute extraction"`; July says `"canonical execution plan"` while its
  work-pack says `"status: proposed"` and
  `"distillValidationStatus | flag"`. **Fix:** reconcile the six authority
  relations above, bind or reject July, select one next unit, and retain
  historical proposals without authority. Sources: Russell-I, Schön-I.

- **F-02 — The declared standard proof path is contradictory and underspecified.**
  Paths: July `WORK-PACK.md`, `EXECUTION-PACK.md`,
  `TASK-GSP-001-current-head-projection.md`,
  `TASK-GSP-004-validation-handoff-docs.md`. Evidence: runner repair has
  `"Dependencies: none"` but board says `"ready-after-GSP-001"` and routing
  says `"SWU-GSP-001 only"`, while GSP-001 requires Playwright. The
  not-yet-authored focused spec is not a defect and could invoke checked-in
  local `tsx` directly. **Fix:** choose and document one standard proof route:
  either authorize a shared runner-only prerequisite or bind GSP-001's focused
  spec to the checked-in local executable; align the board, dependencies, and
  validation command with that choice. Sources: Russell-I, Schön-I, Schön-F.

- **F-03 — Persisted-state freshness failure.** Paths:
  `file-studio-session-store.ts`, `studio.ts`. Evidence:
  `"let documentState = loadDocument(filePath)"` loads once; `getSession` reads
  that snapshot, contradicting `"State is read fresh per request"`.
  Two-process probe preserved preview `RevisionApplied/rev-0000` after external
  state reached `RevisionRecorded/rev-0001`. **Fix:** reload or version-check
  per request and prove independent-process visibility/concurrency. Sources:
  Russell-I, Schön-I.

- **F-04 — Preview content and annotation revision identity diverge.** Path:
  `backend/src/cli/studio.ts`. Evidence: cards use `"/raw/variant/"`;
  annotation uses `"/annotate/variant/${session.baseline.label}"`; comments are
  recorded against `snap.revisionHeadId`. **Fix:** make the current-head
  projection primary and annotation-bound; retain variants explicitly as
  history. Sources: Russell-I, Schön-I.

- **F-05 — Scope-permitted staged CSS change can display zero diff.** Paths:
  `application/admission.ts`, `studio.ts`. Evidence:
  `"<style> nodes are excluded"` while UI says
  `"Honest per-component diff"`; reproduced `NOT_REJECT` with zero
  fragments/counts. `NOT_REJECT` means scope-permitted for staging, never
  admitted or promoted. **Fix:** add style/global/unattributed lanes to diff,
  preview, and handoff evidence. Sources: Russell-I, Schön-I.

- **F-06 — Evidence harness is ambient and non-fail-fast.** Path:
  `backend/e2e/helpers.ts`. Evidence: helpers invoke
  `"pnpm", ["exec","tsx"...]`; failure produces nullable JSON; preview exit
  only `"clearTimeout(timer)"` without resolving/rejecting. **Fix:** use
  checked-in local `tsx`, preserve command/stderr, and reject immediately on
  premature exit. Sources: Russell-I, Schön-I.

- **F-07 — Actor-neutral confirmation policy is unresolved.** Paths:
  `.craft/ledger.yml`, `TASK-GSP-003-action-annotation-mobile.md`. Evidence:
  DEC-026 permits agent acceptance; July requires `"I inspected this change"`
  and says history cannot advance without confirmation, but does not establish
  a human-only gate. **Fix:** owner-decide actor-neutral acknowledgment versus
  human gating; otherwise keep the recap advisory. Sources: Russell-I, Schön-I.

- **F-08 — Projection architecture permits adapter-local collapse.** Paths:
  July `ARCHITECTURE-UPGRADE.md`,
  `TASK-GSP-001-current-head-projection.md`. Evidence: architecture says the
  adapter `"should render a projection object"` and must not decide truth; task
  permits `"Add or inline a projection helper"`. **Fix:** require an
  application-owned typed contract or narrow the proposal to a preview-local
  repair. Sources: Russell-I, Schön-I.

- **F-09 — GSP identity/reference drift.** Paths: July `WORK-PACK.md`, tasks,
  waves. Evidence: five slices map to six manifest SWUs; Task 004 defines
  `004`, `005`, and unmanifested `005-DOC`; Task 005 owns `006`. **Fix:**
  publish one stable slice/task/SWU/wave crosswalk with unique scope, owner,
  dependencies, and receipt per executable ID. Sources: Russell-I, Schön-I.

- **F-14 — Confirmed export falsely sets readiness despite missing evidence.**
  Paths: `application/export-design-handoff.ts`, `domain/models.ts`,
  `application/ui-prototyping-studio.slice.test.ts`. Evidence: `missingRefs` is
  computed/stored at lines 103–120, then readiness is unconditionally set to
  `"uiPhaseBridgeReady: true"`, `"generateTestsUiReady: true"`,
  `"uiImplementReady: true"` at 123–129. The test confirms export and expects
  all three true at 421–449; its default archived docs root lacks the five
  nested default refs. **Fix:** persist separate `exportConfirmed` and
  `evidenceComplete`; derive completeness from `missingRefs.length === 0`;
  require independent predicates for integration/implementation readiness;
  keep release authorization separate; add the incomplete-evidence regression.
  Sources: Russell-I, Schön-I, Alexander-FB, Turing-FB, Beer-FB.

### MINOR

- **F-11 — Current-facing documentation/status drift.** Paths: `CRAFT.md`, root
  `README.md`, `ARCHITECTURE.md`, `SPEC.md`, `WORK-PACK.md`,
  `development/PLAN-NEXT.md`. Evidence: `"53 unit tests + 12"` conflicts with
  current 62-unit evidence; `"whole work pack EXECUTED"` appears beside
  `"Non-executed"`; active prose retains read-only/human-only and built
  `[PROPOSAL]` claims. **Fix:** separate dated historical receipts from current
  reproducibility and synchronize active prose only through the owning gate.
  Sources: Russell-I, Schön-I.

## Dropped/Refuted

- **F-10 dropped standalone:** Craft/SPEC already preserve broad June lineage;
  absorb only conflict-bearing decisions/residue into F-01.
- **F-12 dropped:** `/raw/baseline` semantics are disputed and not governed
  strongly enough to require renaming.
- **F-13 refuted:** `CraftEvidencePack` is explicitly evidence-only and forbids
  gate bypass; its name alone does not assert authority.
