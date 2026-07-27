# Attacks — UI Prototyping Studio Architecture, Plan, And Deep-Spec Review

Dispatch:
`2026-07-27-ui-prototyping-studio-architecture-plan-review`

This file preserves the attacker returns verbatim. They are candidate review
evidence, not accepted findings. Verifier returns are appended after the
synthesis gate.

## Alexander, Christopher — Initial Return

## INITIAL POSITION

**BLOCK execution in the published order and block all release/promotion claims.** The July proposal is salvageable, but `SWU-GSP-004`’s e2e-runner repair must precede `SWU-GSP-001`, and the authority/supersession graph must be reconciled. This is not a final position.

### CRITICAL

1. **There is no coherent current authority/supersession hierarchy.**

   - `.craft/ledger.yml:5`: `"source_of_truth: projects/ui-prototyping-studio/.craft/ledger.yml"`.
   - Yet `.craft/ledger.yml:88,90` still route extraction, while `:169` says N1–N11 are done and `:744` records the executed work pack.
   - `CRAFT.md:18-23,66-92` still presents extraction and already-closed decisions as current.
   - The ledger contains no July governed-state package reference.
   - July `README.md:16` calls its work-pack the `"canonical execution plan"`, despite `WORK-PACK.md:6,22,83` saying `proposed`/`flag`.

   **Fix:** Admit one explicit ledger-owned authority/supersession map and remove “canonical” from every unadmitted proposal.

### MAJOR

2. **Current normative prose contradicts the implemented operating model.**

   - `ARCHITECTURE.md:18-20`: `"the human disposes every durable change"`.
   - `ARCHITECTURE.md:53`: Claude Code `"Never approves/applies (skill-enforced + server-enforced)"`.
   - `ARCHITECTURE.md:58`: preview is `"Read-only view; no gate authority"`.
   - Later, `ARCHITECTURE.md:132-144` says those claims are superseded and AUTO may accept.
   - Live code confirms AUTO acceptance at `studio.ts:390-415`, and browser mutation controls at `:220-253,280-315`.

   **Fix:** Replace superseded normative text in place with one current contract; retain old language only in a clearly historical decision record.

3. **The live browser projection remains semantically false even though the resolver exists.**

   - `studio.ts:204-208` renders historical variants as primary cards.
   - `studio.ts:230-233` annotates `session.baseline.label`, not current head.
   - `studio.ts:334-335` proves current-head HTML is separately available.
   - `admission.ts:181,204,211` excludes `<style>` from `diffByOdId`.
   - `studio.ts:215-217` nevertheless labels that result `"Honest per-component diff"`; a CSS-only visible change can display zero evidence.

   **Fix:** Implement the projection spine and a separate global/style/unattributed diff lane before calling browser evidence honest.

4. **The July dependency graph deadlocks its first required receipt.**

   - July `WORK-PACK.md:87-88` permits only `SWU-GSP-001` first.
   - `TASK-GSP-001:48-53` requires Playwright proof.
   - `helpers.ts:22,74` invokes `pnpm exec tsx`.
   - `TASK-GSP-004:19-30` independently owns fixing that helper.
   - Fresh reproduction: typecheck and **62/62 unit/slice passed**, but **13/13 e2e failed before browser behavior** with Corepack `ERR_VM_DYNAMIC_IMPORT_CALLBACK_MISSING`.

   **Fix:** Split out `GSP-004A e2e-runner preflight` with no dependency and make it a prerequisite of GSP-001.

5. **The July plan silently drops the June deep-spec disposition problem.**

   - Deep-spec `RESULT.md:15` correctly says every artifact is proposal-only.
   - `RESULT.md:53-55` carries R1–R7, proposed invariants, open decisions, and state drift.
   - July `ARCHITECTURE-UPGRADE.md:28-39` cites root docs/research/code but neither the deep-spec package nor ledger; corpus search found no deep-spec/R1–R7/Inv1–8 crosswalk.

   **Fix:** Add a non-promoting crosswalk marking every deep-spec intent `retained`, `superseded by DEC-026/027`, `deferred`, or `still-open`.

### MINOR

6. **Status and evidence labels are stale enough to mislead readers.**

   - Root `WORK-PACK.md:14-15` says nothing executed.
   - `SPEC.md:115-117` says 53 unit/12 e2e; `PLAN-NEXT.md:13-25` says 61/13.
   - `SPEC.md:127-139` and `ARCHITECTURE.md:148-158` list gaps already recorded as resolved.
   - Built schema/admission/two-gate mechanisms remain tagged `[PROPOSAL]` in `SPEC.md:213-221,240-248,296-299` and `ARCHITECTURE.md:115-130`.

   **Fix:** Preserve proposal lineage in history, but label current mechanisms from admitted code receipts and report reproducible evidence separately from historical pass counts.

## Recommended authority hierarchy

1. Reconciled `.craft/ledger.yml`: scoped lifecycle/state authority.
2. Explicitly admitted current `SPEC.md` and `ARCHITECTURE.md`: normative product/architecture contracts.
3. Live code plus immutable receipts: implementation evidence only.
4. July governed-state package: newest proposal, never authority until admitted.
5. June deep-spec package: historical proposal/design evidence.
6. Research and Inventory packet: discovery context only.
7. Release authorization: separate named owner/gate; currently absent.

## KEEP/FIX candidates

- Packet: **KEEP** non-authority boundary.
- `.craft/ledger.yml`, `CRAFT.md`: **FIX**.
- `ARCHITECTURE.md`, `SPEC.md`: **FIX**.
- Root `WORK-PACK.md`, `PLAN-NEXT.md`: **FIX** into explicitly historical/superseded records.
- Full deep-spec package: **KEEP** as proposal evidence; **FIX** only its supersession crosswalk.
- July architecture/layering/result/transport: **KEEP** as flagged proposals.
- July work-pack/execution/tasks/waves: **FIX** dependencies, task/SWU naming, and “canonical” wording.
- `current-html.ts`: **KEEP**.
- `studio.ts`, `admission.ts`, `helpers.ts`: **FIX**.

## Survived attacks

- June proposal/promotion guardrail is explicit.
- July package remains `proposed`/`flag` and avoids a release-readiness claim.
- Open Design remains subordinate and non-authoritative.
- `resolveCurrentHtml` correctly prefers committed head content.
- Unit/type evidence is healthy, while browser evidence is honestly blocked.
- Verification side effects were removed; no scoped repository changes remain.

## Alexander, Christopher — Final Robot-Talk Return

## FINAL POSITION

### What changed

- **The July execution-order defect rises from MAJOR to CRITICAL.** `SWU-GSP-001` requires a Playwright witness, its literal planned spec path does not exist, the normal helper cannot start the CLI, and the plan forbids running the independent helper repair first. This is an execution-blocking contract failure.
- The 13/13 normal e2e failures are now bounded as a **harness-path failure, not product-behavior failure**: the temporary local-`tsx` shim passing 13/13 proves that distinction.
- The external-write issue becomes a separate **MAJOR runtime defect**: `/state` cannot satisfy GSP-001 because the preview process retains an in-memory store snapshot.
- Beer’s confirmation objection adds a **MAJOR governance finding**: GSP-003’s mandatory “I inspected” state would reintroduce a durable-action gate that DEC-REVERSIBILITY-NOT-GATING-026 explicitly removed, without Craft admission.
- GSP identifier drift and the “inline helper” escape hatch are added as contract defects.

### What survived

- **CRITICAL — authority and supersession remain incoherent.** The declared ledger authority is stale, omits the July package, and conflicts with CRAFT/root plans; the proposed July README self-labels its work-pack “canonical.” No proposal may be promoted from this corpus.
- **MAJOR — current-head projection is false.** Historical variants remain primary, annotation remains baseline-bound, and cross-process writes remain invisible.
- **MAJOR — CSS-visible changes can still produce zero displayed diff evidence.**
- **MAJOR — the July package does not disposition deep-spec decisions/residue.**
- **MINOR — stale test counts, proposal labels on built mechanisms, obsolete blockers, and executed plans presented as unexecuted remain documentation defects.**
- The June and July proposal/non-promotion boundaries, Open Design subordination, and “no release-readiness claim” survived.

### Explicit disagreements

- **With Turing:** 13/13 red under the standard command must not be reported as 13 product failures. The shim result proves browser behavior passes under a corrected runner. The cross-process stale-state witness, however, is a genuine product defect.
- **With Beer:** I agree the current “inline helper” wording undercuts the promised shared projection spine. Inline code is not inherently invalid, but adapter-local ownership or duplicated truth resolution is; the task must require an application-owned shared projection contract.
- The ledger remains the *declared* scoped authority, but because it is `candidate-local` and internally stale, it cannot currently establish admission, supersession, or release authorization without reconciliation.

### Compact finding set

- **CRITICAL — Missing authority/supersession map:** reconcile ledger, canonical contracts, historical plans, July proposal, receipts, and release owner; remove “canonical” from unadmitted artifacts.
- **CRITICAL — First SWU is non-executable as specified:** create a real `GSP-004A` runner preflight, make it precede GSP-001, bind an existing test path, then require the current-head and external-write witnesses.
- **MAJOR — Cross-process projection staleness:** preview must reload/version-check the file-backed store per request; `/state` must observe external CLI stage/apply.
- **MAJOR — Browser truth defects:** current head must become primary and annotation-bound; CSS/global changes require a separate visible-change lane.
- **MAJOR — Unauthorized policy reversal:** GSP-003 cannot require “I inspected” as a gate unless Craft explicitly changes DEC-026; otherwise confirmation is advisory framing only.
- **MAJOR — Plan identity/service drift:** stabilize TASK/SWU IDs and meanings; require the shared application projection service rather than permitting adapter-local inline truth.
- **MAJOR — Deep-spec lineage gap:** disposition each deep-spec decision/invariant/residue as retained, superseded, deferred, or open without promoting it.
- **MINOR — Historical/status drift:** regenerate CRAFT, correct counts and resolved gaps, and mark root work-packs/PLAN-NEXT as historical receipts rather than active execution authority.

## Turing, Alan — Initial Return

## INITIAL POSITION

**BLOCK / FIX before any task-session.** The architecture direction is sound, but the plan is not executable in its declared order, and current browser-state projection is demonstrably false under external CLI writes.

### Findings

- **CRITICAL — external writes never reach the running preview.** `studio.ts` claims state is read fresh per request ([studio.ts:180](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/backend/src/cli/studio.ts:180)), but the file store loads once ([file-studio-session-store.ts:47](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/infrastructure/file-studio-session-store.ts:47)) and reads only in-memory state ([file-studio-session-store.ts:82](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/infrastructure/file-studio-session-store.ts:82)). Isolated probe: preview before=`BaselineReady`; external CLI after apply=`RevisionApplied`; preview `/state` after=`BaselineReady`, `stagedHash:null`. This falsifies SWU-001’s external-write criterion ([TASK-GSP-001:37](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/development/invoke-runs/20260710T012443Z-governed-state-projection/work-pack/tasks/TASK-GSP-001-current-head-projection.md:37)).  
  **Fix:** reload/version-check the persisted document on each preview request, then test with two independent processes.

- **CRITICAL — dependency deadlock.** SWU-001 requires Playwright proof ([TASK-GSP-001:48](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/development/invoke-runs/20260710T012443Z-governed-state-projection/work-pack/tasks/TASK-GSP-001-current-head-projection.md:48)); SWU-004 owns the broken helper and explicitly has no dependency ([TASK-GSP-004:19](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/development/invoke-runs/20260710T012443Z-governed-state-projection/work-pack/tasks/TASK-GSP-004-validation-handoff-docs.md:19)). Yet the board says TASK-004 is ready only after GSP-001 and orders “SWU-001 only” ([WORK-PACK:53](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/development/invoke-runs/20260710T012443Z-governed-state-projection/WORK-PACK.md:53), [WORK-PACK:85](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/development/invoke-runs/20260710T012443Z-governed-state-projection/WORK-PACK.md:85)).  
  **Fix:** extract helper repair as prerequisite `SWU-GSP-000`; make SWU-001 depend on it.

- **MAJOR — CSS-only visible changes are admitted with zero diff.** `admitScope` handles style separately, while `diffByOdId` skips style nodes ([admission.ts:147](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/application/admission.ts:147), [admission.ts:203](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/application/admission.ts:203)). Probe returned `admission:"NOT_REJECT"` plus `{fragments:[],added:0,changed:0,removed:0}`.  
  **Fix:** add an explicit global/style/unattributed lane; SWU-002 need not depend on projection work for its unit slice.

- **MAJOR — e2e failure is harness failure, not current product-test failure.** Both helper paths shell through Corepack-managed `pnpm` ([helpers.ts:18](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/backend/e2e/helpers.ts:18), [helpers.ts:71](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/backend/e2e/helpers.ts:71)). `cli()` masks startup failure as `json:null`, and `startPreview()` clears its timer on early exit without rejecting.  
  **Fix:** invoke local `tsx`, fail fast with stderr/command, and reject on premature preview exit.

- **MAJOR — preview/annotation remain historical variants.** Cards use `/raw/variant/*` and annotation uses the baseline variant ([studio.ts:200](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/backend/src/cli/studio.ts:200), [studio.ts:229](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/backend/src/cli/studio.ts:229)); only `/raw/baseline` uses `resolveCurrentHtml` ([studio.ts:334](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/backend/src/cli/studio.ts:334)). `resolveCurrentHtml` itself survived inspection ([current-html.ts:11](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/application/current-html.ts:11)).

- **MAJOR — authority/docs drift.** The ledger omits the July plan and retains extraction-era next moves ([ledger.yml:86](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/.craft/ledger.yml:86)); Architecture calls preview read-only despite mutating POST routes ([ARCHITECTURE.md:58](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/ARCHITECTURE.md:58)); PLAN-NEXT says both “whole work pack executed” and “Non-executed,” and records 61 rather than current 62 unit tests ([PLAN-NEXT.md:13](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/development/PLAN-NEXT.md:13), [PLAN-NEXT.md:28](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/development/PLAN-NEXT.md:28)).

- **MINOR — identifier crosswalk is unstable.** Five TASK files contain six SWUs plus `SWU-GSP-005-DOC`; TASK-004 owns SWUs 004/005/DOC, TASK-005 owns SWU-006 ([WORK-PACK:58](/home/vrondelli/projects/domainspec-core/projects/ui-prototyping-studio/development/invoke-runs/20260710T012443Z-governed-state-projection/WORK-PACK.md:58)).  
  **Fix:** one canonical SWU ID per executable unit; align tasks, slices, waves, dependencies, and commands.

### Reproducibility

- `./node_modules/.bin/tsc -p tsconfig.json --noEmit` → pass.
- `./node_modules/.bin/tsx --test "src/**/*.test.ts"` → **62/62 pass**.
- Local Playwright full suite → **13/13 fail before browser assertions**, Corepack `ERR_VM_DYNAMIC_IMPORT_CALLBACK_MISSING`.
- Temporary `/tmp` local-tsx shim → **13/13 pass in 1.8m**. Diagnostic only; not admissible checked-in browser proof.
- SWU-001’s literal command → exit 1, `No tests found`; planned `e2e/governed-state-projection.spec.ts` does not yet exist.
- Corepack attempted a package manifest edit; that exact line was removed immediately and manifest diff is clean.

### Per-artifact candidates

- **FIX:** `.craft/ledger.yml`, `CRAFT.md`, `ARCHITECTURE.md`, `SPEC.md`, root `WORK-PACK.md`, `PLAN-NEXT.md`.
- **KEEP as historical proposal/evidence:** `RESULT.md`, `SYNTHESIZED-DEEP-DESIGN.md`, `DEEP-SPEC-PROPOSAL.md`, `RESIDUALITY-STRESSORS.md`, `UX-EVIDENCE-REPORT.md`, `COLD-START-USABILITY-FINDINGS.md`.
- **FIX/supersede stale execution surfaces:** `ONE-SHOT-IMPLEMENTATION-PLAN.md`, `PLAYWRIGHT-TEST-PLAN.md`.
- **FIX:** all six July top-level plan artifacts, all five task files, and all three wave files—primarily dependency/order/ID/acceptance-command reconciliation.
- **Implementation:** `current-html.ts` **KEEP**; `studio.ts`, `admission.ts`, `e2e/helpers.ts` **FIX**.

### Survived attacks

Proposal/flag boundaries are generally honest; deep-spec RESULT correctly limits historical readiness and UX Evidence keeps automation separate from human proof. `resolveCurrentHtml` correctly prefers committed revision content then baseline. Existing unit behavior and existing browser scenarios pass when the harness alone is bypassed. None of that establishes SWU-001, external-write coherence, style-diff integrity, or release readiness.

## Turing, Alan — Final Robot-Talk Return

## FINAL POSITION

### What changed

- I upgrade the missing authority/supersession map to **CRITICAL**. The defect is not stale wording itself; it is that a proposed/flag July package can be called canonical while the Craft authority neither binds nor orders it against root and deep-spec artifacts.
- I upgrade unstable GSP numbering from MINOR to **MAJOR** because TASK/SWU/slice/wave mismatches can select the wrong dependency, owner, or write scope.
- I add two **MAJOR** contract conflicts:
  - The architecture requires one application-level projection service, while GSP-001 permits an inline `studio.ts` helper.
  - Mandatory “I inspected” confirmation may conflict with the accepted reversibility policy that permits agent-driven accept. This requires an owner decision before implementation.
- I agree a flagged Craft child context and explicit non-promoting crosswalk must precede execution.

### What survived

- **Product behavior failures:** independent direct-process probing proves the preview does not observe external CLI writes. Static and functional evidence also confirms historical-variant primary cards/annotation and CSS-only mutation admitted with zero displayed diff.
- **Harness-only failure:** the standard 13-test browser suite fails before browser assertions because helpers invoke broken Corepack/pnpm. A temporary local-tsx shim yielded 13/13 passing existing scenarios. This does not prove GSP behavior or create an admissible receipt.
- **Plan-blocking evidence:** SWU-001 requires Playwright proof while the helper repair is owned by SWU-004 and forbidden by the declared “SWU-001 only” ordering. The named GSP-001 spec is also absent, although creating it is legitimately within the SWU.
- **Unit proof only:** typecheck and 62/62 unit/slice tests pass. They establish neither browser projection nor external-process coherence.
- Deep-spec UX fixtures, failure states, identity work, conflict algebra, and residuality analysis remain useful promote-later references, not current authority.

### Explicit disagreements

- I agree with Alexander’s CRITICAL authority finding, but stale counts and proposal labels alone remain **MINOR**. Criticality comes from their interaction with missing authority and supersession routing.
- I agree with Beer that the “I inspected” requirement is unadmitted. I do not call it a proven policy reversal yet: it becomes one only if implemented as a mandatory human-only accept gate. As written, it is a **MAJOR unresolved contract conflict**.
- I agree with Beer’s flagged Craft child context and projection-service objection.
- I revise my earlier ID-mapping severity upward to **MAJOR**.

### Compact finding set

- **CRITICAL — Authority vacuum:** establish a Craft-bound authority/supersession crosswalk: ledger/current contract → July proposed repair plan → historical deep-spec evidence. Remove any “canonical” implication from proposed/flag artifacts.
- **CRITICAL — Dependency inversion:** execute a Corepack-independent e2e-helper prerequisite before SWU-001; otherwise its mandatory browser receipt is unobtainable through the admitted route.
- **MAJOR — Runtime projection failure:** reload/version-check persisted state per request and prove external CLI apply/stage through an independent-process browser witness.
- **MAJOR — Projection architecture mismatch:** require the promised application-level projection service; disallow preview-local current-head decisions unless the architecture is explicitly amended.
- **MAJOR — Policy conflict:** owner-adjudicate mandatory inspection confirmation against DEC-026 reversibility/autonomous accept before changing action semantics.
- **MAJOR — Visible-diff integrity:** add a global/style/unattributed lane; CSS-only admitted changes currently report zero diff.
- **MAJOR — Identifier instability:** normalize one executable SWU identity across manifest, task files, slices, waves, owners, dependencies, and acceptance commands.
- **MAJOR — Harness operability:** use checked-in local executables, surface child-process stderr directly, and reject preview startup on early exit.
- **MINOR — Documentary drift:** reconcile stale test counts, executed/non-executed wording, read-only-preview wording, and historical mock/web paths after receipts exist.

## Beer, Stafford — Initial Return

## INITIAL POSITION — Beer/Stafford attacker

The June deep spec is a valuable historical design/fixture corpus, explicitly non-canonical. The standalone CLI implementation realized much of its L0/L2 intent under different seams, but not its full L0–L6 design. The July governed-state package is the newest coherent proposal, but it is still `phase_status: flag`, absent from Craft, and not dependency-safe enough to execute as written. This is an initial position, not a final verdict.

## Severity-ranked findings

1. **CRITICAL — Three incompatible “next moves” coexist with no supersession authority.** Craft indexes still prescribe extraction, `CRAFT.md` says approve extraction and resolve already-closed decisions, root `WORK-PACK.md` says nothing has executed/start X1, while the ledger itself records the closed standalone loop and N1–N11 completion (`.craft/ledger.yml:86-90,118-169,739-744`; `CRAFT.md:18-38,66-92`; `WORK-PACK.md:12-15,152-156`).  
   **Fix:** admit one current context/next move in Craft, mark the root work-pack executed/superseded-by-receipts, regenerate `CRAFT.md`, and bind or reject the July package explicitly.

2. **HIGH — July L0 has a validation dependency inversion.** `SWU-GSP-001` requires a Playwright receipt, but every e2e CLI/preview launch still shells through `pnpm` (`backend/e2e/helpers.ts:18-26,71-86`), whose repair is assigned to dependency-free `SWU-GSP-004`; nevertheless the board says GSP-004 is “ready-after-GSP-001” and W3 depends on GSP-001 (`WORK-PACK.md:50-65`; `W3-L2-evidence-semantics.md:13-16`).  
   **Fix:** execute a narrowly split `GSP-000/004a e2e-runner` first, then GSP-001; do not treat a manual shim as its receipt.

3. **HIGH — GSP identifiers silently change meaning.** Delivery slices stop at S-GSP-005; SWU manifest has 001–006; `TASK-GSP-004` contains SWU-004, SWU-005, and `SWU-GSP-005-DOC`; `TASK-GSP-005` owns SWU-006; wave W3 names Task 004 and Task 005 while mixing L2/L3 (`WORK-PACK.md:36-65`; `TASK-GSP-004...md:17-61`; `TASK-GSP-005...md:13-38`).  
   **Fix:** use one stable task↔SWU mapping, split runner/handoff/docs, and publish a migration table rather than renumbering silently.

4. **HIGH — GSP-003 reverses an accepted control decision without authority linkage.** Current accepted policy says reversibility, not identity/action gating; Accept/Revert are intentionally browser buttons (`.craft/ledger.yml:1413-1419`; `studio.ts:220-227,304-315`). July makes “I inspected this change” confirmation mandatory before reversible history advance (`TASK-GSP-003...md:25-40`) without a Craft decision or evidence that this friction is non-theatrical.  
   **Fix:** route mandatory confirmation through decision-gate; otherwise make the recap informative and preserve one-action reversibility.

5. **HIGH — The claimed projection spine can degrade into another preview-local patch.** Architecture requires a single application projection service (`ARCHITECTURE-UPGRADE.md:60-96`), but GSP-001 permits an inline helper and mostly edits `studio.ts` (`TASK-GSP-001...md:23-39`). That does not establish the shared contract for preview, annotation, diff, and handoff.  
   **Fix:** require a typed read-only projection contract plus focused unit witness in GSP-001, or narrow the architecture claim to a tactical preview repair.

6. **HIGH — Neither the July decisions nor their owner are bound into scoped authority.** Source contracts omit the Craft ledger and root work-pack; ownership is only “Studio development cycle”; no context, decision IDs, artifact record, handoff, or receipt appears in Craft. The package itself admits missing define approval (`ARCHITECTURE-UPGRADE.md:24-26`; `PLAN-TRANSPORT.md:27-39`).  
   **Fix:** add a flagged Craft child context with operator-owned decisions for current-head primacy, visible-style evidence, reversible-action framing, and handoff readiness semantics before execution.

7. **HIGH — “Deep spec fully implemented/canonical” is false.** The result says every artifact is a proposal, SPEC unmutated, only L0–L2 realistic, and L3–L6 net-new/unproven (`RESULT.md:13-32`). Obsolete seams include the seven-panel React/mock API, human-only durable operations, irreversible Apply/baseline, and required modal. Still absent or unpromoted are failure states, identity/DNA surface, WorkflowStep projection, FX/axe calibration, full conflict algebra, and human ergonomics evidence (`UX-EVIDENCE-REPORT.md:369-376`; `PLAYWRIGHT-TEST-PLAN.md:709-728`).  
   **Fix:** preserve it as historical design/probe evidence with per-decision dispositions; never promote wholesale.

8. **MEDIUM — Active root contracts retain superseded text beside correction appendices.** `ARCHITECTURE.md` and `SPEC.md` still say the human disposes every durable change and the preview is read-only, then later supersede those claims; `[PROPOSAL]` labels remain on implemented artifact storage/two-gate mechanics (`ARCHITECTURE.md:18-22,53-58,115-140`; `SPEC.md:19-26,65-98,213-221`).  
   **Fix:** move superseded prose to lineage notes and state one current contract in the active sections.

9. **MEDIUM — The visible-diff defect is real and narrowly evidenced.** Admission handles CSS for rejection, but `diffByOdId` explicitly excludes `<style>` nodes, so a visible theme change can yield zero review evidence (`admission.ts:133-164,177-221`).  
   **Fix:** retain component fragments and add an explicit global/style/unattributed lane; do not pretend CSS is component-attributed.

## Authority/supersession map candidate

```text
Craft ledger + operator decisions
  ├─ active contract: lean SPEC / ARCHITECTURE (after sync)
  ├─ runtime evidence: standalone backend + admitted receipts
  └─ flagged child proposal: July Governed-State Projection package

June deep-spec RESULT
  └─ historical proposal/evidence
      ├─ distilled into lean SPEC + root WORK-PACK
      ├─ partially realized by standalone extraction/reversible core
      ├─ superseded: React/mock seams, human-only disposal, Apply-as-irreversible
      └─ promote-later references: UX fixtures, failure states, identity/DNA,
         conflict algebra, human-study and invariant calibration

Root WORK-PACK / PLAN-NEXT
  └─ historical execution plans; superseded by implementation receipts

July package
  └─ newest coherent proposal, not admitted; may supersede only the next-plan
     projection/diff/docs slices after Craft binding and dependency repair
```

## Per-artifact KEEP/FIX candidates

- `.craft/ledger.yml` — **FIX** chronology, active blockers, July indexing, next move.
- `CRAFT.md` — **FIX/regenerate**; it is materially stale.
- `ARCHITECTURE.md`, `SPEC.md` — **KEEP/FIX**; consolidate current model and remove implemented `[PROPOSAL]` labels.
- Root `WORK-PACK.md` — **KEEP as executed lineage / RETIRE as executable**.
- `PLAN-NEXT.md` — **KEEP as completion receipt / remove from “next” routing**.
- Deep-spec `RESULT` — **KEEP** as the clearest claim boundary.
- `SYNTHESIZED-DEEP-DESIGN`, `DEEP-SPEC-PROPOSAL`, `RESIDUALITY-STRESSORS` — **KEEP/FIX** with explicit per-decision supersession and promote-later labels.
- `ONE-SHOT-IMPLEMENTATION-PLAN` — **RETIRE as executable; KEEP fixture/traceability reference**.
- `UX-EVIDENCE-REPORT`, `PLAYWRIGHT-TEST-PLAN` — **KEEP as calibration catalogs; FIX obsolete SPA/mock paths and promotion status**.
- `COLD-START-USABILITY-FINDINGS` — **KEEP as historical baseline; require a current-head re-test before current UX claims**.
- July architecture/invoke result — **KEEP flagged**.
- July layering/work-pack/execution/transport/tasks/waves — **FIX** authority binding, numbering, dependency order, and write-scope collisions.
- `current-html.ts` — **KEEP** as implemented current-head resolver.
- `studio.ts` — **KEEP/FIX** primary current-head/annotation projection and route naming.
- `admission.ts` — **KEEP/FIX** visible style/global evidence.
- `e2e/helpers.ts` — **FIX first** as the proof-production prerequisite.

## Survived attacks

- June’s explicit proposal/non-canonical boundary and conditional L0–L2 verdict.
- HTML-first artifacts, CLI seam, deterministic admission boundary, exact staged-hash acceptance, append-only reversible lineage, and stable `data-od-id` intent.
- UX claim discipline: hard gates vs soft flags vs human-study residue.
- July’s diagnosis of current-head projection drift and style-diff blindness.
- Open Design remaining subordinate evidence only.
- Export confirmation remaining distinct from evidence completeness and implementation readiness.

## Beer, Stafford — Final Robot-Talk Return

# FINAL POSITION

## Changed beliefs

- The authority defect is **CRITICAL**, not merely major: the July package is internally `flag/proposed`, absent from Craft, yet its README calls it canonical. A README label cannot promote an unadmitted plan.
- Cross-process freshness is now a **confirmed product defect**, not just an acceptance risk: the preview’s long-lived store snapshot leaves `/state` stale after external CLI writes.
- The e2e problem is a **proof-production defect**, not evidence that the existing 13 browser behaviors fail. Normal 13/13 fail before browser assertions; a local-tsx shim yields 13/13 pass. That isolates Corepack/pnpm as the harness failure.
- The shim does **not** produce an admissible standard receipt, validate the nonexistent literal SWU-001 spec path, or prove the new current-head/external-write/CSS behaviors.
- Alexander’s requested per-intent crosswalk is necessary; file-level “keep/fix” alone is insufficient because individual deep-spec documents mix live intent, superseded seams, and promote-later material.

## Surviving findings

### CRITICAL

1. **Authority and chronology are incoherent.** Craft/root routing still prescribes completed extraction/F2 work; July is unindexed and unowned; its README overcalls a flagged proposal canonical.  
   **Conclusion:** no implementation plan is currently admitted as the authoritative next plan.

2. **The governed-state browser projection is observably false under external writes.** The core can contain newer persisted truth while preview `/state` reports its load-time snapshot. This violates the July proposal’s central current-state claim.

3. **The declared first SWU is not executable as specified.** Its literal Playwright file does not exist, and its witness depends on the broken checked-in runner assigned later to GSP-004. The graph must be repaired before GSP-001 can produce a valid receipt.

### MAJOR

4. **Silent GSP numbering changes destroy reference integrity:** slice, task, and SWU IDs do not map one-to-one; Task 004 contains 004/005/005-DOC while Task 005 owns 006.

5. **The projection “spine” can collapse into another adapter-local patch:** GSP-001 permits inline `studio.ts` logic instead of requiring the shared projection contract claimed by the architecture.

6. **GSP-003 silently reverses accepted reversibility policy:** mandatory “I inspected” confirmation gates reversible Accept/Revert without a new owner decision or evidence that the friction is non-theatrical.

7. **CSS-only changes can pass admission yet produce zero review fragments.** This is a product trust defect independent of the e2e runner.

8. **Active SPEC/ARCH documents retain superseded contracts beside append-only corrections:** human-only disposal, read-only preview, old irreversible boundaries, and implemented mechanics still marked proposal.

9. **Any “deep spec canonical” or “fully implemented” claim is rejected.** The deep spec self-identifies as proposal and conditional. Much of its intent survives, but its original surfaces, authority model, and L3–L6 implementation claims do not.

### MINOR

10. Route names such as `/raw/baseline` now resolve current head and perpetuate semantic drift; introduce explicit current-head naming.

11. `CraftEvidencePack` risks confusion with Craft authority; keep it deferred and name its evidence-only, non-authoritative status explicitly.

## Explicit disagreements

- I disagree that 13/13 normal e2e failures establish broken product behavior: they terminate in Corepack before browser assertions.
- I disagree that 13/13 shim-green establishes current browser readiness: it proves only that existing tests pass when the runner defect is bypassed.
- I disagree that a README can declare the July plan canonical against `phase_status: flag` and no Craft admission.
- I disagree with deleting the June corpus. Preserve it through explicit `implemented-as`, `superseded-by`, `reference-only`, and `promote-later` relations.
- I disagree with executing mandatory Accept/Revert confirmation without reopening the reversibility decision.
- I agree with Alexander that the authority hierarchy is the primary governance defect and with Turing that external freshness and CSS-zero-diff are independent runtime counterexamples.

## Deep-spec intent disposition

- **Live/current:** HTML-first artifacts; CLI/no-MCP seam; stable `data-od-id`; deterministic admission; exact staged-hash acceptance; append-only revisions; revert/discard; export confirmation.
- **Implemented under different seams:** local no-build preview; click annotation; before/after review; in-browser Accept/Discard/Revert; standalone file-backed backend; Playwright closed-loop fixtures.
- **Superseded:** React seven-panel/mock-api surface as primary product; human-only durable operations; identity gating; Apply/baseline as irreversible boundaries; mandatory Apply modal; full L0–L6 one-shot framing.
- **Promote later:** identity/DNA and `UIIdentityIndex` implementation; WorkflowStep projection; named failure/recovery states; full fitness/token model; calibrated accessibility/layout corpus.
- **Still live residue:** ergonomics unproven; FX/axe promotion absent; conflict algebra incomplete; CSS/node-identity limits; cross-process freshness/concurrency; acceptance text not machine-checked; handoff readiness semantics unresolved.

## Authority and next-order conclusion

```text
Authority:
Craft ledger + explicit operator decisions
  -> synchronized lean SPEC/ARCH
  -> admitted receipts as implementation evidence

Historical reference:
June deep-spec corpus
  -> never canonical wholesale
  -> disposition per intent

Current proposal:
July governed-state package
  -> flagged and unadmitted
  -> cannot supersede root routing until Craft binds it
```

Dependency-safe next order:

1. Admit a flagged July child context in Craft and publish the supersession crosswalk.
2. Split and run `GSP-000/004a`: deterministic checked-in local-tsx runner plus a real focused spec path.
3. Run GSP-001 with a required application projection contract and cross-process reload/version witness.
4. Run GSP-002 for global/style/unattributed diff evidence.
5. Re-decide action confirmation, then run the approved annotation/mobile/action slice.
6. Separate handoff readiness semantics.
7. Synchronize SPEC, ARCH, Craft indexes/view, root work-pack, and PLAN-NEXT from receipts.
8. Keep Open Design evidence-pack work last and non-authoritative.

## Russell, Bertrand — Initial Verifier Return

## INITIAL VERIFIER RESULT — Russell

Inventory was used only to locate artifacts; no finding relies on it as validation.

| ID | Verdict | Objection / verified evidence | Severity | Corrected one-line fix |
|---|---|---|---|---|
| F-01 | **REVISE** | There is no authority “vacuum”: `.craft/ledger.yml:4-6` declares a `candidate-local` source of truth. The defect is that this lifecycle ledger is stale (`:86-90`), while July is `proposed`/`flag` (`WORK-PACK.md:6,22`) yet its README calls the plan “canonical” (`:16`). `SPEC.md` and `ARCHITECTURE.md` remain drafts, so normative admission is also unproved. | **MAJOR**, execution-blocking governance defect; not CRITICAL runtime/release failure. | Operator-reconcile Craft state, explicitly admit normative SPEC/ARCH versions, register July as proposal-only, and issue separate execution authorization; release remains unbound. |
| F-02 | **REVISE** | The contradiction survives: `SWU-GSP-004` has no dependency (`WORK-PACK.md:63`; Task 004 `:19-30`), but the task board places it after GSP-001 (`:53`) and routing says GSP-001 only (`:87-88`), although GSP-001 requires Playwright (`Task 001:48-53`). The absent focused spec is not itself a defect because creating one is in scope (`:23-26`). | **MAJOR**, plan non-executability; CRITICAL is inflated. | Split/authorize the runner preflight before GSP-001, then create and run the focused GSP-001 witness. |
| F-03 | **ACCEPT** | Store state loads once (`file-studio-session-store.ts:51`); `getSession` reads only that snapshot (`:82-84`), contradicting “fresh per request” (`studio.ts:184`). “Current” cannot mean current persisted state here. | **MAJOR** | Reload or compare persisted version per request and prove independent-process visibility/concurrency behavior. |
| F-04 | **ACCEPT** | Cards render `/raw/variant/*` (`studio.ts:204-208`), annotation renders the original baseline variant (`:230-233`), but comments are recorded against the current revision (`:287-291`). This is more than visual hierarchy: content and revision identity can disagree. | **MAJOR** | Project and annotate the current head; retain variants explicitly as historical lineage. |
| F-05 | **REVISE** | `<style>` is excluded from diff (`admission.ts:181,203-211`) while the UI labels counts “Honest per-component diff” (`studio.ts:215-217`). `NOT_REJECT` means the scope fence permitted staging, not final acceptance/promotion. | **MAJOR** | Add an explicit style/global/unattributed lane and describe the witness as “scope-permitted and staged with zero displayed diff,” not “admitted.” |
| F-06 | **ACCEPT** | Helpers invoke ambient `pnpm` (`helpers.ts:22,74`); CLI failure collapses parsing to nullable JSON (`:24-31`); preview early exit clears the timer without resolving or rejecting (`:77-85`). | **MAJOR** | Use a checked-in executable path, preserve command/stderr, and reject immediately on premature process exit. |
| F-07 | **REVISE** | DEC-026 removes identity gating and allows agent acceptance (`ledger.yml:1413-1419`). July requires confirmation state (`Task 003:25-27,38-40`) but does not say it must be human-only. This is an unresolved policy ambiguity, not a proven reversal. | **MAJOR** | Specify confirmation as agent-compatible advisory acknowledgment, or obtain an owner decision before introducing a human-only gate. |
| F-08 | **ACCEPT** | Architecture requires an application projection service and says the adapter must not decide truth (`ARCHITECTURE-UPGRADE.md:15-18,83-96`); GSP-001 permits an inline helper (`Task 001:28-29`). | **MAJOR** | Require an application-owned typed projection contract, or narrow the proposal to a preview-local repair. |
| F-09 | **ACCEPT** | Five delivery slices (`WORK-PACK.md:40-44`) map to six manifest SWUs (`:60-65`); Task 004 contains `004`, `005`, and `005-DOC`, while Task 005 owns `006`. `005-DOC` is absent from the manifest. | **MAJOR** | Publish one stable task/SWU/slice/wave crosswalk with unique executable IDs and dependencies. |
| F-10 | **REVISE** | July contains no deep-spec reference, but “no disposition path” is too strong: Craft retains the June context and `SPEC.md:318-328` broadly defers L3-L6 and proposed invariants. What is missing is a complete per-intent lineage map, and July does not yet claim supersession. | **MINOR** until July is admitted | Require a non-promoting per-intent crosswalk only as a prerequisite to admitting July or declaring supersession. |
| F-11 | **REVISE** | Current-facing docs drift: `SPEC.md:115` says 53/12, `CRAFT.md:147` says 62/62, and `PLAN-NEXT.md:13-14` says executed while `:28` says non-executed. Historical counts are valid only when explicitly timestamped as receipts. | **MINOR** | Separate dated historical receipts from current reproducibility, and synchronize authority/status prose only through the owning gate. |
| F-12 | **REJECT** | `/raw/baseline` is used as the “before (current)” comparison (`studio.ts:218`) and resolves the current comparison baseline (`:334-335`). “Baseline” is not proven to mean original variant in this route context. | **DROP** | No change request; add `/raw/current` only if an admitted route vocabulary requires it. |
| F-13 | **REJECT** | The artifact explicitly calls itself an evidence/profile slice, requires evidence buckets, and forbids gate bypass (`Task 005:5-6,17-36`). Its name alone does not assert Craft authority. | **DROP** | No finding; an optional `authority_effect: none` stamp may improve clarity but is not corrective evidence. |

Authority must be expressed as six separate relations:

- **Current-state authority:** operator-reconciled Craft ledger; presently only declared and `candidate-local`.
- **Normative architecture:** owner-admitted SPEC/ARCH versions; current files are drafts with superseded text.
- **Proposal evidence:** June deep-spec and July package; authority effect is none.
- **Reproducibility receipts:** code, tests, and probes; evidence of observed behavior only.
- **Execution authorization:** explicit selected SWU plus owner/gate; currently absent.
- **Release authorization:** separate named release owner/gate; currently absent.

Convergence blockers: no admitted authority/supersession map; no execution authorization for July; runner ordering prevents the first required receipt; DEC-026 confirmation semantics are unresolved; task/SWU identities are unstable; and runtime readiness vocabulary remains unsafe—`export-design-handoff.ts:103-129` can set `uiImplementReady: true` even while `missingRefs` is nonempty, which is neither release authorization nor proof of implementation readiness.

## Schön, Donald — Initial Verifier Return

# INITIAL VERIFIER RESULT — Schön

Independent checks reproduced: 62/62 unit tests; 13 Playwright tests listed; planned GSP spec absent; helper returns `code:1,json:null` from Corepack while no browser assertion runs; early preview exit remains pending; CSS-only change yields `NOT_REJECT` with zero diff; `resolveCurrentHtml` returns committed head; two-process preview stays `RevisionApplied/rev-0000` after external state reaches `RevisionRecorded/rev-0001`; confirmed handoff with five `missingRefs` still sets all three integration-ready flags `true`. Probes used `/tmp`; no Studio target diff was introduced.

| ID | Result | Objection / exact evidence | Supported severity | Corrected one-line fix |
|---|---|---|---|---|
| F-01 | ACCEPT | Ledger is `candidate-local` and declared source at `.craft/ledger.yml:4-5`, but routes completed extraction at `:86-90`; completion is recorded at `:169,739-744`. July README calls its plan canonical while `WORK-PACK.md:6,22,83` says proposed/flag, and July is absent from ledger indexes. | CRITICAL governance blocker | Bind or reject July in Craft, select exactly one next unit, mark superseded plans historical, and remove “canonical” from the unadmitted README. |
| F-02 | REVISE | Helper failure and contradictory order are real (`WORK-PACK:53,63,87-88`; task 001 `:48-53`). But “non-executable” is too absolute: task 001 explicitly permits a new focused spec (`:23-26`), which could launch local `tsx` without the shared helper; absence of that not-yet-authored spec is not itself a defect. | MAJOR, not CRITICAL | Split/select a runner-only prerequisite to avoid duplicated test launch logic, then execute GSP-001 through that checked-in route. |
| F-03 | ACCEPT | Store loads once at `file-studio-session-store.ts:51`; reads use memory at `:82-84`. Exact staged probe reproduced external `RevisionRecorded/rev-0001` versus preview `RevisionApplied/rev-0000`. | MAJOR | Reload/version-check persisted state per request and prove Accept/Revert/external-write coherence with two processes. |
| F-04 | ACCEPT | Primary cards use `/raw/variant/*` and annotation baseline at `studio.ts:204-208,229-233`; only `/raw/baseline` resolves current head at `:334-335`. | MAJOR | Make a current-head projection primary and annotation-bound; retain variant cards only as history. |
| F-05 | ACCEPT | `<style>` is excluded at `admission.ts:181,203-211`; fresh probe returned `NOT_REJECT` and zero fragments/counts while CSS visibly changed. | MAJOR | Add an explicit style/global/unattributed lane to diff, preview, and handoff evidence. |
| F-06 | ACCEPT | `helpers.ts:22,74` invokes Corepack `pnpm`; isolated helper reproduced the stated error. `:84` clears the timer without resolve/reject; forced early exit remained pending after 500 ms. This is proof-path failure, not product-red. | MAJOR | Invoke checked-in local `tsx`, preserve stderr/command, and reject preview startup immediately on child exit. |
| F-07 | REVISE | DEC-026 permits agent acceptance (`ledger:1413-1419`); task 003 requires confirmation before history advances (`:25-27,38-40`). This proves an unresolved policy change, but not necessarily identity-gating—the confirmation could be actor-neutral. | MAJOR | Owner-decide actor-neutral acknowledgement versus a human gate before implementing; otherwise keep recap advisory. |
| F-08 | ACCEPT | Architecture requires an application projection object (`ARCHITECTURE-UPGRADE:62-96`), while task 001 permits an inline helper (`:28-29`). | MAJOR | Require an application-owned typed projection contract, or explicitly narrow the architecture to a preview-only repair. |
| F-09 | ACCEPT | Manifest maps `005` to docs and `006` to Task 005, while Task 004 defines `004`, `005`, and `005-DOC`; slices stop at five (`WORK-PACK:40-65`). | MAJOR | Publish one stable slice/task/SWU crosswalk with one scope, dependency set, owner, and receipt per executable ID. |
| F-10 | REJECT | June proposal status and absent July crosswalk are verified, but no admitted obligation requires every historical proposal intent to be dispositioned in July. The ledger already tracks many decisions/gaps; a full per-intent crosswalk is not independently execution-blocking. | None standalone; absorbed by F-01 | Crosswalk only conflict-bearing authority/decision/residue during F-01 reconciliation; do not mandate wholesale historical disposition. |
| F-11 | ACCEPT | `PLAN-NEXT:13-14` says executed 61/13 beside “Non-executed” at `:28`; SPEC says 53/12 at `:115`; active sections retain read-only/human-only and built `[PROPOSAL]` text. | MINOR | Synchronize active prose only after fresh receipts; retain old claims in explicit lineage sections. |
| F-12 | ACCEPT | `/raw/baseline` serves `resolveCurrentHtml` at `studio.ts:334-335`; the route no longer reliably means historical baseline. | MINOR | Add `/raw/current`; preserve `/raw/baseline` only as a documented compatibility alias if needed. |
| F-13 | REJECT | The name alone does not establish implied authority: layering explicitly says Open Design helpers are “never authority” (`IMPLEMENTATION-LAYERING:39`), and task 005 forbids gate bypass and subjective hard gates (`:30-36`). | None | No mandatory change; an `authority_effect:none` stamp is optional defense-in-depth. |

A separate handoff defect is verified: `export-design-handoff.ts:104-129` records `missingRefs` but unconditionally sets all readiness flags true. The current test at `ui-prototyping-studio.slice.test.ts:421-449` reinforces that conflation. This deserves a MAJOR handoff-semantics finding rather than hiding inside documentation drift.

Fresh-operator walkthrough: starting from the claimed authority, no executable GSP SWU can be selected without invention. Craft selects stale extraction, not July. Jumping to July yields GSP-001’s dependency, scope, validation, and done criteria, but no bound receipt artifact and a broken standard helper. GSP-004 has `dependencies:none`, yet the board and “001 only” route prohibit selecting it. Thus authority, selection, and receipt binding do not converge.

Smallest reproducible acceptance sequence:

1. Operator binds/rejects July, stabilizes IDs, names a receipt path, and explicitly selects a runner-only SWU.
2. Runner SWU: local `tsx` plus early-exit test; pass `playwright test --reporter=list`; receipt includes command, stderr behavior, and 13-test result.
3. Projection SWU: application projection plus store freshness; pass typecheck, 62-unit suite, focused checked-in Playwright spec, and two-process Accept/Revert witness.
4. Style SWU: CSS-only unit plus browser/handoff assertion proving visible change cannot report zero evidence.
5. Handoff SWU: missing refs must keep implementation readiness false; issue semantic receipt before documentation sync.

Convergence blockers: no admitted current plan/SWU, no stable ID map or receipt artifact, DEC-026 confirmation semantics unowned, focused GSP browser spec absent, and release/human-ergonomics authorization still unbound.

## Feedback Returns

### Alexander, Christopher

**SUPPORT — MAJOR.** This is a literal current claim/proof defect.

- `export-design-handoff.ts:103-120` computes and preserves `missingRefs`.
- `export-design-handoff.ts:123-129` then unconditionally sets:

  > `uiPhaseBridgeReady: true`  
  > `generateTestsUiReady: true`  
  > `uiImplementReady: true`

  There is no `missingRefs.length === 0` condition.

- The slice test confirms export at `ui-prototyping-studio.slice.test.ts:421-425` and asserts all readiness flags true at `:447-449`.
- Its default docs root is `provenance/legacy-domainspec-spec` (`:566-573`), while default refs are nested `docs/features/ui-prototyping-studio/...` paths (`export-design-handoff.ts:8-14`); those paths are absent, so this exercised handoff has nonempty `missingRefs`. The test never asserts that contradiction.

Semantic boundary:

- **Export confirmation:** only proves a confirming actor authorized bundle creation.
- **Evidence completeness:** false when `missingRefs` is nonempty.
- **Integration readiness:** cannot follow from confirmation alone; requires complete integration evidence.
- **Implementation readiness:** stronger still and must remain false absent its own evidence.
- **Release authorization:** is not represented or granted here and must never be inferred from any of these flags.

**One-line fix:** Persist separate `exportConfirmed`, `evidenceComplete`, `integrationReady`, and `implementationReady` values with monotone evidence predicates—leaving release authorization to a separate owner/gate—and add a test asserting confirmed export plus nonempty `missingRefs` keeps all readiness flags false.

### Turing, Alan

**SUPPORT — MAJOR.**

A confirmed export with nonempty `missingRefs` still unconditionally marks all integration fields true.

Evidence:

- `confirmedBy` only confirms the irreversible export action; it does not establish evidence completeness (`export-design-handoff.ts:20`).
- Missing references are computed and retained in the bundle (`export-design-handoff.ts:103`).
- Regardless of `missingRefs`, the session sets `uiPhaseBridgeReady`, `generateTestsUiReady`, and `uiImplementReady` to `true` (`export-design-handoff.ts:123`).
- The model explicitly labels `missingRefs` “advisory” and “non-gating” (`models.ts:143`).
- The slice test confirms export, then asserts all three readiness flags true without asserting evidence completeness or empty `missingRefs` (`ui-prototyping-studio.slice.test.ts:421`). Its default docs root points at the archived root-level files, while the exported nested `docs/features/...` paths are absent (`ui-prototyping-studio.slice.test.ts:566`).

Semantic distinction:

- `exportConfirmed`: a person authorized export.
- `evidenceComplete`: all required references exist and bind.
- `integrationReady`: downstream integration prerequisites are satisfied.
- `implementationReady`: implementation prerequisites and evidence are complete.
- `releaseAuthorized`: a separate promotion decision; no evidence here establishes it.

This is a literal current readiness false-positive, but not demonstrated release-authorization bypass.

**One-line fix:** persist separate fields and derive `evidenceComplete = missingRefs.length === 0`; never set integration or implementation readiness from export confirmation alone, and keep release authorization behind an independent gate.

### Beer, Stafford

**SUPPORT — MAJOR**

A confirmed export with incomplete evidence currently sets all integration/implementation readiness flags to `true`.

Evidence:

- `missingRefs` is computed from unresolved references and stored in the bundle: `export-design-handoff.ts:103-120`.
- The same operation then unconditionally sets:

  > `uiPhaseBridgeReady: true`  
  > `generateTestsUiReady: true`  
  > `uiImplementReady: true`

  at `export-design-handoff.ts:123-129`, without checking `missingRefs`.

- The slice test confirms export via `confirmedBy`, then explicitly expects all three readiness flags to be true: `ui-prototyping-studio.slice.test.ts:421-449`.
- That test uses the archived docs root (`...slice.test.ts:566-573`), while default refs resolve beneath `docs/features/ui-prototyping-studio/...`; those nested paths are absent in the current checkout. Thus this is literally a confirmed export with nonempty `missingRefs` and true readiness flags.

Semantic distinction:

- **Export confirmation:** proven only by nonempty `confirmedBy`; authorizes creation of the handoff bundle.
- **Evidence completeness:** false when `missingRefs.length > 0`.
- **Integration readiness:** not established merely by exporting; must remain false/indeterminate until required integration evidence exists.
- **Implementation readiness:** falsely asserted by `uiImplementReady: true` despite missing references.
- **Release authorization:** not represented or granted here; it must never be inferred from export or readiness flags.

**One-line fix:** Set `exportConfirmed` independently, derive `evidenceComplete` from `missingRefs.length === 0`, keep integration/implementation readiness false until separate admitted checks pass, and add a regression test proving confirmed export + missing refs cannot set readiness true.

## Russell, Bertrand — Final Verifier Return

FINAL PASS.

The revision correctly applies all prior objections:

- F-01/F-02/F-05/F-07/F-11 are properly narrowed and severity-bounded.
- F-10 is correctly absorbed into F-01; F-12 and F-13 are correctly dropped.
- F-14 is literally verified: confirmed export records nonempty `missingRefs` yet unconditionally sets all readiness flags true.
- Current-state authority, normative architecture, proposal evidence, reproducibility receipts, execution authorization, and release authorization remain distinct.
- June and July remain non-authoritative proposals/historical evidence.

Changed position: I now fully drop standalone F-10 and accept F-14 as MAJOR. No blocking objection remains.

## Schön, Donald — Final Verifier Return

- **F-02 remains overstated.** “Blocks the required first receipt” is not proven: `TASK-GSP-001:23-26` permits a new focused Playwright spec, which could directly invoke checked-in local `tsx` and satisfy the literal validation command without modifying `helpers.ts`. Runner-first is the safer normalization order, but it is a plan amendment—not a logically necessary dependency. Revise F-02 to “the declared standard proof path is contradictory/underspecified” and avoid claiming the current order cannot produce any receipt.

## Zig-Zag Cap Resolution

The declared zig-zag loop cap was exhausted. The parent applied Schön's exact final narrowing mechanically in `SYNTHESIS-REVISION.md` and `findings.md`. No further verifier turn was launched. The coverage auditor must check that F-02 contains no stronger claim than Schön's objection permits.
