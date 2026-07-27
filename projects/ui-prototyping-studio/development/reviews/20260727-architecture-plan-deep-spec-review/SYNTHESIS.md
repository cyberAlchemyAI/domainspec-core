# Candidate Synthesis — UI Prototyping Studio Architecture Review

This is a read-only candidate set for verifier attack, not an accepted finding,
implementation authorization, admission decision, or promotion.

Scope stayed on the selected Studio authority/root/deep-spec/July/live
artifacts. Body War/TROQAR remain excluded; Open Design remains subordinate
comparison evidence only.

## Fresh Checks

- Typecheck passed; unit/slice suite passed **62/62**.
- The checked-in harness path reproduced
  `ERR_VM_DYNAMIC_IMPORT_CALLBACK_MISSING`; the helper returned
  `code:1, json:null`.
- Playwright lists 13 existing tests, but the planned
  `e2e/governed-state-projection.spec.ts` is absent and its literal command
  returns `No tests found`.
- Independent two-process probe: external CLI advanced to
  `RevisionRecorded/rev-0001`; running preview remained
  `RevisionApplied/rev-0000`.
- CSS-only probe returned `admission:"NOT_REJECT"` with zero fragments/counts.
- `resolveCurrentHtml` itself correctly prefers committed head content.
- Diagnostic side effects were removed; no Studio target diff remains.

Gaps and residue are preserved: no Inventory Evidence Card or EvidenceSet; no
fresh checked-in browser receipt; human ergonomics remain unproven; release
authorization is unbound. Unit-green is not browser proof; harness-red is not
product-red; the two runtime counterexamples above are independent of
Playwright.

## Per-Artifact KEEP/FIX Matrix

| Stratum | Artifact(s) | Verdict |
|---|---|---|
| Craft | `.craft/ledger.yml`; `CRAFT.md` | **FIX** — F-01/F-11 |
| Root contracts | `README.md`; `ARCHITECTURE.md`; `SPEC.md` | **FIX** — consolidate current contract/status |
| Root plans | `WORK-PACK.md`; `development/PLAN-NEXT.md` | **KEEP as lineage/receipt; FIX/retire as executable routing** |
| Deep-spec boundary | `development/deep-spec-dispatch/RESULT.md` | **KEEP** as proposal/non-promotion boundary |
| Deep-spec intent | `SYNTHESIZED-DEEP-DESIGN.md`; `DEEP-SPEC-PROPOSAL.md`; `RESIDUALITY-STRESSORS.md` | **KEEP** as historical/promote-later intent; disposition externally via F-10 |
| Deep-spec execution | `ONE-SHOT-IMPLEMENTATION-PLAN.md` | **FIX/RETIRE as executable; KEEP as traceability reference** |
| Deep-spec evidence | `UX-EVIDENCE-REPORT.md`; `COLD-START-USABILITY-FINDINGS.md` | **KEEP** as calibration/historical evidence; require current retest for current claims |
| Deep-spec tests | `PLAYWRIGHT-TEST-PLAN.md` | **KEEP as fixture catalog; FIX** obsolete SPA/mock seams and promotion status |
| July proposal | `ARCHITECTURE-UPGRADE.md`; `IMPLEMENTATION-LAYERING.md`; `INVOKE-RESULT.md`; `PLAN-TRANSPORT.md` | **KEEP flagged; FIX** lineage, first-route, and dependency claims |
| July execution | `README.md`; `WORK-PACK.md`; `EXECUTION-PACK.md` | **FIX** F-01/F-02/F-09 |
| July tasks/waves | all `work-pack/tasks/*.md`; `work-pack/waves/*.md` | **FIX** ordering, ownership, IDs; keep useful intent |
| Live resolver | `backend/.../application/current-html.ts` | **KEEP** |
| Live persistence | `backend/.../infrastructure/file-studio-session-store.ts` | **FIX** F-03 |
| Live browser | `backend/src/cli/studio.ts` | **FIX** F-04/F-07/F-12 |
| Live diff | `backend/.../application/admission.ts` | **FIX** F-05 |
| Evidence harness | `backend/e2e/helpers.ts` | **FIX first** F-06 |

## Authority And Supersession Recommendation

After operator reconciliation, `.craft/ledger.yml` should be scoped
lifecycle/state authority; admitted `SPEC.md`/`ARCHITECTURE.md` should be
current normative contracts. Live code plus immutable receipts remain
implementation evidence, not authority or release authorization.

The July package remains the newest **flagged proposal**; June deep-spec
remains historical proposal/evidence, dispositioned per intent rather than
promoted wholesale. Root work-packs and `PLAN-NEXT` become historical execution
lineage. Inventory and this review remain discovery/audit evidence. A separate
named owner/gate must authorize release.

Until reconciliation, the ledger is only the declared authority: its
`candidate-local` and stale state cannot prove current admission or
supersession.

## Dependency-Safe Next-Plan Recommendation

1. Operator-admit a flagged July Craft child context and non-promoting
   authority/deep-spec crosswalk.
2. Split `GSP-000/004A`: checked-in local-`tsx` runner, stderr propagation,
   early-exit rejection; prove the standard route.
3. Run GSP-001 with an application-owned projection contract, per-request
   reload/version check, and independent-process Accept/Revert/external-write
   witness.
4. Run GSP-002: unit-level style/global/unattributed lane may proceed
   independently; browser integration follows GSP-001.
5. Decision-gate confirmation semantics against DEC-026 before GSP-003.
6. Separate handoff semantics and documentation synchronization; issue receipts
   before rewriting current status.
7. Keep evidence-profile/Open Design work last, explicitly non-authoritative.

## Candidate Change Requests

Attacker sources: AI/AF = Alexander initial/final; TI/TF = Turing
initial/final; BI/BF = Beer initial/final.

- **F-01 — CRITICAL — Authority/supersession vacuum.** Paths:
  `projects/ui-prototyping-studio/.craft/ledger.yml`, `CRAFT.md`, root plans,
  July `README.md`/`WORK-PACK.md`. Evidence: ledger says `"source_of_truth"` but
  routes `"Execute extraction"`; July says `"canonical execution plan"` while
  work-pack says `"status: proposed"` and `"Verdict: flag"`. **Fix:**
  operator-admit one authority/supersession map and remove canonical language
  from unadmitted artifacts. Sources: AI/AF, TI/TF, BI/BF.

- **F-02 — CRITICAL — First SWU dependency inversion.** Paths: July
  `WORK-PACK.md`, `EXECUTION-PACK.md`,
  `TASK-GSP-001-current-head-projection.md`,
  `TASK-GSP-004-validation-handoff-docs.md`. Evidence:
  `"Run ... SWU-GSP-001 only"` requires a Playwright receipt, while
  dependency-free runner repair is `"ready-after-GSP-001"`. **Fix:** extract
  runner preflight and make it a prerequisite of GSP-001. Sources: AI/AF,
  TI/TF, BI/BF.

- **F-03 — MAJOR — Cross-process state freshness failure.** Paths:
  `backend/.../file-studio-session-store.ts`, `backend/src/cli/studio.ts`.
  Evidence: `"let documentState = loadDocument(filePath)"` occurs once;
  `getSession` reads that snapshot. Probe preserved stale preview state after
  external acceptance. **Fix:** reload/version-check persisted state per
  request with an independent-process test. Sources: AF, TI/TF, BF.

- **F-04 — MAJOR — Primary preview/annotation are historical.** Path:
  `backend/src/cli/studio.ts`. Evidence: cards use `"/raw/variant/"`;
  annotation uses `"/annotate/variant/${session.baseline.label}"`, although
  `/raw/baseline` calls `resolveCurrentHtml`. **Fix:** make current head primary
  and annotation-bound; demote variants to history. Sources: AI/AF, TI/TF,
  BI/BF.

- **F-05 — MAJOR — Visible CSS changes can display zero evidence.** Paths:
  `backend/.../application/admission.ts`, `backend/src/cli/studio.ts`. Evidence:
  `"<style> nodes are excluded"` while UI labels output
  `"Honest per-component diff"`; reproduced admitted zero-diff. **Fix:** add
  explicit global/style/unattributed evidence lane. Sources: AI/AF, TI/TF,
  BI/BF.

- **F-06 — MAJOR — Evidence harness is non-operable and non-fail-fast.** Path:
  `backend/e2e/helpers.ts`. Evidence: `"pnpm", ["exec","tsx"...]`; process exit
  only `"clearTimeout(timer)"`, never rejects. **Fix:** invoke checked-in local
  executable, propagate command/stderr, reject premature preview exit. Sources:
  AF, TI/TF, BI/BF.

- **F-07 — MAJOR — Unadmitted action-policy change.** Paths:
  `.craft/ledger.yml`, July `TASK-GSP-003-action-annotation-mobile.md`.
  Evidence: DEC-026 says `"Control is reversibility, not identity-gating"`;
  task requires `"I inspected this change"` and history cannot advance without
  confirmation. **Fix:** decision-gate mandatory confirmation; otherwise keep
  recap advisory. Sources: AF, TF, BI/BF.

- **F-08 — MAJOR — Projection spine can collapse into adapter-local logic.**
  Paths: July `ARCHITECTURE-UPGRADE.md`,
  `TASK-GSP-001-current-head-projection.md`. Evidence: architecture says
  adapter `"should render a projection object"`; task permits
  `"Add or inline a projection helper"`. **Fix:** require an application-owned
  typed projection contract or narrow the architecture claim. Sources: AF, TF,
  BI/BF.

- **F-09 — MAJOR — GSP identity/reference drift.** Paths: July `WORK-PACK.md`,
  tasks, waves. Evidence: Task 004 owns `SWU-GSP-004`, `005`, and `005-DOC`;
  Task 005 owns `006`, while slices stop at 005. **Fix:** one stable executable
  identity and migration crosswalk across slices/tasks/SWUs/waves. Sources: AF,
  TI/TF, BI/BF.

- **F-10 — MAJOR — Deep-spec intent has no disposition path.** Paths:
  deep-spec `RESULT.md`, July `ARCHITECTURE-UPGRADE.md` and package. Evidence:
  RESULT says `"every artifact ... is a proposal"` and carries R1–R7/Inv1–8;
  July source contracts contain no deep-spec reference or disposition. **Fix:**
  add `retained / implemented-as / superseded / deferred / open` per-intent
  crosswalk without promotion. Sources: AI/AF, TF, BI/BF.

- **F-11 — MINOR — Current documentation/status drift.** Paths: `CRAFT.md`,
  root `README.md`, `ARCHITECTURE.md`, `SPEC.md`, `WORK-PACK.md`,
  `PLAN-NEXT.md`. Evidence: `"53 unit tests + 12"` vs reproduced 62;
  `"whole work pack EXECUTED"` beside `"Non-executed"`; active prose still says
  preview is read-only/human-only. **Fix:** synchronize from receipts and move
  superseded prose to explicit history. Sources: AI/AF, TI/TF, BI/BF.

- **F-12 — MINOR — Current-head route is semantically misnamed.** Path:
  `backend/src/cli/studio.ts`. Evidence: `/raw/baseline` serves
  `resolveCurrentHtml(...)`. **Fix:** introduce `/raw/current` and
  deprecate/alias the historical name. Source: BF.

- **F-13 — MINOR — `CraftEvidencePack` implies authority it does not have.**
  Paths: July `IMPLEMENTATION-LAYERING.md`,
  `TASK-GSP-005-craft-evidence-pack.md`. Evidence: proposed
  `"CraftEvidencePack"` is merely candidate/revision evidence. **Fix:** rename
  or stamp `authority_effect: none`; keep deferred behind L0–L2 receipts.
  Source: BF.
