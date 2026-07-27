# Verification And Feedback — UI Prototyping Studio Architecture Review

This file preserves the initial verifier returns and the one declared
synthesizer-to-attacker feedback round. These are inputs to the single
synthesis revision, not final findings.

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

## Declared Feedback Prompt

> Verifiers identified possibly missing material. Inspect current
> `projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/application/export-design-handoff.ts`
> around lines 103-129 and the corresponding slice test around lines 421-449.
> Determine whether a confirmed handoff with nonempty `missingRefs` can still
> set integration/implementation readiness flags true, and whether that is a
> literal current review defect. Distinguish export confirmation, evidence
> completeness, integration readiness, implementation readiness, and release
> authorization. Return SUPPORT or REFUTE, exact quote/path evidence,
> CRITICAL/MAJOR/MINOR if supported, and one-line fix. Do not reopen unrelated
> findings; do not edit files or spawn agents.

## Alexander, Christopher — Feedback Return

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

## Turing, Alan — Feedback Return

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

## Beer, Stafford — Feedback Return

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
- F-14 is literally verified: confirmed export records nonempty `missingRefs`
  yet unconditionally sets all readiness flags true.
- Current-state authority, normative architecture, proposal evidence,
  reproducibility receipts, execution authorization, and release authorization
  remain distinct.
- June and July remain non-authoritative proposals/historical evidence.

Changed position: I now fully drop standalone F-10 and accept F-14 as MAJOR. No
blocking objection remains.

## Schön, Donald — Final Verifier Return

- **F-02 remains overstated.** “Blocks the required first receipt” is not
  proven: `TASK-GSP-001:23-26` permits a new focused Playwright spec, which
  could directly invoke checked-in local `tsx` and satisfy the literal
  validation command without modifying `helpers.ts`. Runner-first is the safer
  normalization order, but it is a plan amendment—not a logically necessary
  dependency. Revise F-02 to “the declared standard proof path is
  contradictory/underspecified” and avoid claiming the current order cannot
  produce any receipt.

## Zig-Zag Cap Resolution

The declared zig-zag loop cap was exhausted. The parent applied Schön's exact
final narrowing mechanically in `SYNTHESIS-REVISION.md`:

- F-02 no longer claims the first receipt is impossible.
- It records a contradictory/underspecified standard proof route.
- Its fix requires the owner to select either a shared runner prerequisite or
  a focused GSP-001 test bound directly to checked-in local `tsx`, then align
  the board, dependencies, and command.

No further verifier turn was launched. The coverage auditor must check that the
final finding contains no stronger claim than Schön's objection permits.
