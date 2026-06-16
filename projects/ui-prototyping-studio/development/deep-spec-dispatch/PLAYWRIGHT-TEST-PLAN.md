---
id: ui-prototyping-studio-playwright-test-plan
feature: ui-prototyping-studio
title: "PLAYWRIGHT-TEST-PLAN.md — Whole-suite UI test plan (s7, PLANNED MODE / design-only)"
summary: >
  Design-only Playwright UI test suite for the UI Prototyping Studio, organized by studio surface
  (7 panels + state indicator + workbench shell) and by the studio workflow
  (init -> prompt -> generate -> select/commit baseline -> confirm identity/DNA -> comment ->
  synthesize -> approve -> apply -> revision -> handoff). Every scenario carries: id, user goal,
  preconditions/mock-API state, steps, locator strategy (user-facing roles/names), expected evidence
  (screenshot/trace/axe/DOM-measurement/console-network), assertion, failure interpretation, and a
  mapping to the s6 ux-evidence-validator layers (L0..L6). Governance invariants are first-class tests
  (auto-apply forbidden, server-side gate checks, one manifest append per apply, variantCount bounds,
  escaped text). Includes accessibility interaction detail (tab order, focus trap, ARIA live) and
  error/recovery flows. DO NOT RUN — this is the plan, not the execution.
status: draft
node_type: design
dispatch_id: ui-prototyping-studio-deep-spec-001
step_id: s7-playwright-test-plan
lane: validator
owners:
  - web-core
reads:
  - handle.synthesized-deep-design   # SYNTHESIZED-DEEP-DESIGN.md (s4)
  - handle.validator-layers          # UX-PLAYWRIGHT-VALIDATOR-SPEC.md (s6 layer model L0..L6)
  - implementation                   # apps/web components, hook, layout, e2e mock-api
updatedAt: 2026-06-15
---

# PLAYWRIGHT-TEST-PLAN.md — UI Prototyping Studio (s7, PLANNED MODE)

> **Mode: DESIGN ONLY. Nothing in this document is run.** This is the whole-suite plan that a later
> execution stage implements against the live mock-API harness. Where a scenario already exists in
> the repo it is annotated `[EXISTS: <file>::<test>]` and is folded in (kept, extended, or hardened),
> so the plan is the *complete* target suite, not a delta.

## 0. Grounding, conventions, and the s6 layer model

### 0.1 What this suite tests (the real surface)
The Studio is a single route `/ui-prototyping-studio` rendered by `StudioWorkbenchLayout`
(`apps/web/src/layouts/StudioWorkbenchLayout.tsx`). It mounts an `AppSidebar` plus a `<main>` with a
header (`<h1>UI Prototyping Studio</h1>`, eyebrow `domainspec.ui-prototyping.read`, and a
`SessionStateIndicator` once a session exists), two error `role="alert"` slots, a loading note, and
two `<section>` grids of panels.

**Studio surfaces (DOM order = baseline tab order):**
1. `AppSidebar` (nav landmark)
2. Header: `<h1>` + eyebrow + `SessionStateIndicator` (`aria-live="polite"`)
3. Primary grid: **S1 SessionControlsPanel** → **S2 VariantCanvas** → **S3 AnnotationPanel**
4. Secondary grid: **S4 MutationApprovalPanel** → **S5 RevisionTimeline** → **S6 HandoffSummaryPanel**
5. Footer: committed-branch note (`data-testid='ups-committed-branch'`, variantCount=1 only)

Each panel `<section>` is `aria-labelledby` its `<h3>`: "Session Controls", "Variant Canvas",
"Annotation Panel", "Mutation Approval Panel", "Revision Timeline", "Handoff Summary Panel".

### 0.2 Mock-API state (the only backend the suite sees)
The suite drives `installUiPrototypingStudioApiMocks(page)`
(`apps/web/e2e/ui-prototyping-studio/mock-api.ts`). It is an in-memory route fulfiller for
`**/api/ui-prototyping-studio/**`. Preconditions are expressed as **which mock branch the request
will hit**. The hook auto-starts a session on mount (`useUiPrototypingStudio` `useEffect(startSession)`),
so by default the page loads already in `SessionInitialized` with `?variantCount=3` unless `?variantCount=1|2`
is set. Key mock states and their canonical error codes:

| Mock branch | Trigger | Status | Error code (durable contract) |
|---|---|---|---|
| create session | POST `/sessions`, `requestedVariantCount` out of 1..3 | 422 | `VARIANT_COUNT_OUT_OF_RANGE` |
| submit prompt | empty/whitespace prompt | 422 | `PROMPT_REQUIRED` |
| generate | prompt not set | 409 | `PROMPT_NOT_SET` |
| baseline | `variantCount>1` and no `selectedLabel` | 409 | `BASELINE_SELECTION_REQUIRED` |
| baseline | label not A/B/C | 422 | `BASELINE_LABEL_INVALID` |
| comment | selectionGate != satisfied | 409 | `BASELINE_GATE_UNSATISFIED` |
| comment | missing field / bad severity | 422 | `COMMENT_SCHEMA_INVALID` |
| comment / synth | revisionId != head | 422 | `SOURCE_REVISION_INVALID` |
| synth | no comments on revision | 409 | `COMMENT_SET_EMPTY` |
| approve | missing approvedBy/approvedAt | 422 | `APPROVAL_METADATA_REQUIRED` |
| approve | batch not draft | 409 | `BATCH_NOT_DRAFT` |
| approve | source != head | 409 | `APPROVAL_STALE` |
| apply | `applyRequestedBy == "system:auto"` | 409 | `AUTO_APPLY_FORBIDDEN` |
| apply | batch not approved | 409 | `BATCH_APPROVAL_REQUIRED` |
| apply | batch source stale | 422 | `BATCH_STALE_FOR_HEAD` |
| handoff export | no applied revisions | 409 | `HANDOFF_REVISION_REQUIRED` |
| handoff get | bundle not yet exported | 409 | `HANDOFF_BUNDLE_NOT_READY` |
| any session route | unknown sessionId | 404 | `SESSION_NOT_FOUND` |

**Important planning note (mock fidelity).** Several error/recovery and governance branches in this
plan require mock states the current `mock-api.ts` does NOT yet emit (e.g. `GenerationFailed`,
`SynthesisTimedOut`, `SourceStale` surfaced as UI state, `ApplyConflicted`, generic 5xx/network drop,
duplicate-apply manifest re-append, escaped-text round-trip from server). Those scenarios are flagged
`[MOCK-EXT]` and carry the exact mock extension they need. This is by design: s7 specifies the whole
suite the implementation must satisfy, including the failure surface the s4 synthesis (D5) made
first-class. Where the UI does not yet render a named failure state, the scenario asserts the
**current** observable degraded behavior AND records a residue to add the named state.

### 0.3 Locator strategy (global rule)
Per s6 L3 ("flows driven by role, label, text, test id, or approved scoped locators") and Playwright
best practice, **prefer user-facing locators** in this priority:
1. `getByRole('heading'|'button'|'textbox'|'combobox'|'alert'|'status', { name })`
2. `getByLabel(...)` for form fields (every field has an explicit `<label htmlFor>`).
3. `getByText(...)` for evidence strings the user actually reads.
4. `data-testid` **only** for machine-readable evidence strings that are intentionally not
   role-addressable (e.g. `ups-selection-gate`, `ups-apply-gate`, gate badges, raw artifact refs).

testid is a deliberate evidence channel here, not a crutch — it exposes gate/state truth for
assertion. Buttons are reachable by accessible name; fields by label. The plan lists the **preferred**
locator first and the existing testid as a fallback in parentheses.

### 0.4 s6 validator layer map (the classification every scenario inherits)
From `UX-PLAYWRIGHT-VALIDATOR-SPEC.md`:

| Layer | Purpose | Hard-gate? | This suite uses it for |
|---|---|---|---|
| **L0 Smoke** | scenario is inspectable | block on load/runtime failure | route loads, no fatal console errors, trace on failure |
| **L1 Accessibility** | semantic + a11y contracts | block on serious/critical axe, unnamed controls, keyboard failure | axe scans, role/name, ARIA snapshots, tab order, focus trap, aria-live, disabled-reason |
| **L2 Layout Integrity** | physically fits / no clip-overflow | block on overflow/clip/overlap | 7-panel grid fits 1280×800 + mobile; no clipped gate/badge text |
| **L3 Interaction Flow** | primary tasks via user-facing contracts | block on task failure / invisible transition | the whole workflow happy path + each gate transition |
| **L4 Cognitive/Attention** | risk proxies | **soft flag / screenshot review** (no block w/o calibration) | choice count (variant cards ≤3), gate salience, summary persistence, decision-count proxies for D2/Q6 |
| **L5 Domain Practice** | declared design-system/domain packs | soft flag | governance-workbench pack (gate vocabulary, append-only evidence rendering) |
| **L6 Human Evidence** | unprovable-by-automation claims | residue only | ergonomics floor (R-5): "is override as cheap as ratify *felt*", naive-user stall points → s8 |

**Governance invariants are L3 (deterministic interaction) + L1 (a11y of the gate) and, where they
assert a server truth the UI cannot fake, an L0/L3 network-evidence check** (direct `fetch` against
the mock to prove the server-side gate, exactly as the existing UPS-UI-008 does for auto-apply).

### 0.5 Evidence channels (what each scenario captures)
- **screenshot** — full-page baseline + clipped region (panel/gate/badge) for L2/L4.
- **trace** — `trace: 'on-first-retry'` (config) for any failing/evidence-required flow (L0/L3).
- **axe** — `@axe-core/playwright` `AxeBuilder().analyze()` scoped to route or panel (L1). *(suite
  dependency to add; flagged in residue.)*
- **DOM-measurement** — `boundingBox()`, `scrollWidth>clientWidth` overflow probe, target-size
  (≥24×24 / profile), `getComputedStyle` for focus-visible (L2/L4).
- **console-network** — `page.on('console')` / `page.on('requestfailed')` collected per scenario;
  assert zero fatal console errors (L0); assert governance request status codes directly (L3).
- **ARIA snapshot** — `expect(locator).toMatchAriaSnapshot()` for the workbench landmarks, the
  approval region, and the state indicator live region (L1).

### 0.6 Scenario id scheme
`UPS-PW-<AREA>-<n>`. AREA ∈ {SHELL, S1..S6, IND (indicator), FLOW, GOV (governance invariant),
A11Y, ERR (error/recovery), L4 (cognitive)}. Existing repo ids (`UPS-UI-00x`) are cross-referenced.

---

## PART A — BY STUDIO SURFACE

### A.0 SHELL — workbench route, landmarks, auth eyebrow, panel presence

#### UPS-PW-SHELL-1 — Route exposes the authenticated workbench shell  `[EXISTS: wp01::UPS-UI-001]`
- **User goal:** Land on `/ui-prototyping-studio` and see I am in the Studio with my read scope.
- **Preconditions / mock state:** mocks installed; auto-start creates `ups-session-0001` (variantCount=3, `SessionInitialized`).
- **Steps:** goto `/ui-prototyping-studio`.
- **Locator strategy:** `getByRole('heading', { name: 'UI Prototyping Studio', level: 1 })`; `getByText('domainspec.ui-prototyping.read')`; `getByRole('heading', { name: 'Session Controls' })`.
- **Expected evidence:** baseline full-page screenshot; console-network (zero fatal); axe scan of route.
- **Assertion:** h1 + scope eyebrow + Session Controls heading all visible; axe has no serious/critical.
- **Failure interpretation:** if h1 missing → route/render regression (L0 block). If scope eyebrow missing → auth contract regression. If axe serious → a11y regression (L1 block).
- **Layers:** L0 + L1.

#### UPS-PW-SHELL-2 — All seven required panels render  `[EXISTS: wp01::UPS-UI-002]`
- **User goal:** See every workbench surface present in one view.
- **Preconditions:** default load.
- **Steps:** goto route.
- **Locator strategy:** `getByRole('heading', { name })` for the 7 panel titles ("Session Controls", "Variant Canvas", "Annotation Panel", "Mutation Approval Panel", "Revision Timeline", "Handoff Summary Panel") + landmark `getByRole('main')`.
- **Expected evidence:** full-page screenshot; ARIA snapshot of `<main>` (landmark + 6 region headings).
- **Assertion:** all 7 headings visible; `<main>` ARIA snapshot matches the 7-region structure (extend existing test, which omits Handoff Summary).
- **Failure interpretation:** missing panel → layout composition regression; extra/renamed heading → ARIA snapshot drift, breaks screen-reader navigation expectations.
- **Layers:** L1 (semantics) + L2 (all fit).

#### UPS-PW-SHELL-3 — Workbench grid fits required viewports without overflow/clip
- **User goal:** Use the workbench on desktop and a small laptop without horizontal scroll or clipped controls.
- **Preconditions:** default load; then drive to a fully-populated revision (use FLOW-1 fixture) so panels carry max content.
- **Steps:** goto; run happy path to one applied revision + exported handoff; measure at 1280×800 and 768×1024 (mobile emulation per s6 minimum matrix).
- **Locator strategy:** measurement on `getByRole('main')` and each panel `<section>`.
- **Expected evidence:** responsive full-page screenshots per viewport; `measurements/*.json` (scrollWidth vs clientWidth; bounding boxes of gate/badge text nodes).
- **Assertion:** `document.scrollingElement.scrollWidth <= clientWidth + 1` (no horizontal overflow); no gate/badge text node clipped (`scrollWidth <= clientWidth` per node); panels do not incoherently overlap.
- **Failure interpretation:** overflow → grid breakpoint regression (L2 block); clipped `selectionGate=`/`applyGate=` text → the user can no longer read governance state, a governance-legibility failure, not cosmetic.
- **Layers:** L2 (block) + L4 screenshot-review for density.

### A.1 S1 — SessionControlsPanel (variantCount selector, prompt, start/submit/generate)

#### UPS-PW-S1-1 — variantCount selector offers exactly 1, 2, 3  `[EXISTS: wp01::UPS-UI-003]` (GOV — see GOV-1)
- **User goal:** Choose how many variants, bounded to the allowed set.
- **Preconditions:** default load.
- **Steps:** goto.
- **Locator strategy:** `getByLabel('Variant count')` (combobox) (testid `ups-variant-count`); read its `option` children.
- **Expected evidence:** clipped screenshot of the select; DOM list of option texts.
- **Assertion:** options exactly `['1','2','3']` in order; no `0`/`4`+.
- **Failure interpretation:** an out-of-range option appearing means the **variantCount bounds invariant** has leaked into the UI affordance — a governance regression (see GOV-1 for the server-side twin).
- **Layers:** L3 + governance (GOV).

#### UPS-PW-S1-2 — Prompt + action buttons are labelled, keyboard-reachable, and correctly disabled pre-session
- **User goal:** Type a prompt and trigger generation only when allowed.
- **Preconditions:** to test the disabled-pre-session state, intercept/abort the auto-start so `sessionId` is null `[MOCK-EXT: allow auto-start to be suppressed via ?noAutostart or failing POST /sessions]`. Otherwise assert the post-start enabled state.
- **Steps:** goto; (suppressed-start variant) observe Submit/Generate disabled; (normal) observe enabled after start.
- **Locator strategy:** `getByLabel('Prompt')` (textbox); `getByRole('button', { name: 'Start Session' | 'Submit Prompt' | 'Generate Variants' })`; session id evidence via `getByText(/sessionId=/)` (testid `ups-session-id`).
- **Expected evidence:** focus screenshots (visible focus ring), axe scan of panel, trace.
- **Assertion:** prompt textbox has accessible name "Prompt"; Submit/Generate `disabled` while `sessionId` null; enabled after `SessionInitialized`; `sessionId=ups-session-0001` shown.
- **Failure interpretation:** Submit/Generate enabled with no session → would send to `SESSION_NOT_FOUND`; user gets a confusing 404 instead of a guard. Missing label → L1 block.
- **Layers:** L1 + L3.

#### UPS-PW-S1-3 — Busy state disables controls during in-flight requests
- **User goal:** Not double-submit while a request is running.
- **Preconditions:** add latency to POST `/sessions` or `/variants/generate` `[MOCK-EXT: route delay]`.
- **Steps:** click Generate; during the delay, assert buttons disabled and "Starting..."/busy affordance.
- **Locator strategy:** roles as above; the Start button text toggles to "Starting...".
- **Expected evidence:** trace spanning the in-flight window; screenshot mid-flight.
- **Assertion:** all action buttons `disabled` while `busy`; re-enabled after resolution.
- **Failure interpretation:** controls enabled mid-flight → race / duplicate generation; in governance terms a second uncontrolled draft.
- **Layers:** L3 (async transition visibility).

### A.2 S2 — VariantCanvas (candidate cards, baseline select/commit, selection gate)

#### UPS-PW-S2-1 — Generates exactly variantCount candidate cards (≤3 ceiling)
- **User goal:** Compare a bounded number of candidates.
- **Preconditions:** `?variantCount=3`; prompt submitted; generate.
- **Steps:** select 3 → Start → fill Prompt → Submit → Generate.
- **Locator strategy:** the grid `getByRole('list')` within Variant Canvas (testid `ups-variant-grid`); cards `getByRole('heading', { name: /Variant [ABC]/ })`.
- **Expected evidence:** screenshot of the 3-card grid; choice-count measurement (L4).
- **Assertion:** exactly 3 cards labelled A/B/C; never 4 (mirrors UPS-OP-002, "emits exactly variantCount").
- **Failure interpretation:** >3 cards → variantCount ceiling violated (D-006 bound). Wrong count vs requested → generation determinism break.
- **Layers:** L3 + L4 (choice count proxy for cognitive load, soft flag if >3 but server returned them).

#### UPS-PW-S2-2 — Multi-variant locks annotation until explicit baseline selection  `[EXISTS: wp01::UPS-UI-004]`
- **User goal:** Be forced to pick a baseline before commenting (human disposes the durable select — tier-2).
- **Preconditions:** `variantCount=3`; generated; `selectionGate=pending`, `baseline=null`.
- **Steps:** Start(3) → Prompt → Submit → Generate; assert gate pending + annotation locked; click "Select Baseline B"; assert satisfied + unlocked.
- **Locator strategy:** `getByRole('button', { name: 'Select Baseline B' })`; gate evidence `getByText('selectionGate=pending'|'selectionGate=satisfied')` (testid `ups-selection-gate`); annotation gate via `getByText(/Annotation gate (locked|unlocked)/)` (testid `ups-annotation-gate`).
- **Expected evidence:** before/after screenshots; trace.
- **Assertion:** pre-select: `selectionGate=pending`, annotation "locked"; post-select: `satisfied`, "unlocked"; selected card gets `is-baseline`.
- **Failure interpretation:** annotation unlocked before a baseline → the human-disposes gate (tier-2) collapsed to agent-may-act; first-principle governance violation.
- **Layers:** L3 + governance (gate sequencing).

#### UPS-PW-S2-3 — Single-variant commits baseline automatically, no Select button  `[EXISTS: wp01::UPS-UI-005]`
- **User goal:** With one option, proceed without a pointless selection step (graceful degradation, D2 guardrail-2).
- **Preconditions:** `?variantCount=1`; generated → mock auto-sets `baseline=committed:A`, `selectionGate=satisfied`, `revisionHeadId=rev-0000`, `BaselineReady`.
- **Steps:** load `?variantCount=1` (or select 1) → Prompt → Submit → Generate.
- **Locator strategy:** absence: `getByRole('button', { name: /Select Baseline/ })` should have count 0; single-branch note `getByText(/Single-variant branch committed baseline/)` (testid `ups-single-variant-branch`); badge `getByText('baseline=committed:A')` (testid `ups-baseline-badge`).
- **Expected evidence:** screenshot; trace.
- **Assertion:** no Select-Baseline buttons; committed-branch note present; annotation unlocked; badge `baseline=committed:A`.
- **Failure interpretation:** a Select button appearing at count=1 → manufactured decision (D2 "no champion to nominate at count=1" violated → unnecessary cognitive load).
- **Layers:** L3 + L4 (decision-count proxy = 0, the good outcome).

#### UPS-PW-S2-4 — Selected card carries baseline status in text and accessible name
- **User goal:** A screen-reader user can tell which card is the baseline.
- **Preconditions:** multi-variant, baseline B selected.
- **Steps:** select B.
- **Locator strategy:** card heading "Variant B"; per UI-SPEC A11y row, baseline status must be exposed via `aria-label` + text.
- **Expected evidence:** ARIA snapshot of the variant grid; screenshot of `is-baseline` card.
- **Assertion:** the B card exposes baseline status both visually and to AT (text "status=selected" present; **residue:** add `aria-label` — current component only does class + text).
- **Failure interpretation:** baseline distinguishable only by CSS class → invisible to AT (L1). This is a real gap in the current `VariantCanvas` (no `aria-label`), so the scenario is partly a **gap-detector**.
- **Layers:** L1 (block if AT cannot perceive baseline).

### A.3 S3 — AnnotationPanel (canonical comment capture, gate, comment stream)

#### UPS-PW-S3-1 — Comment form fields are labelled and gated by baseline
- **User goal:** Capture a canonical comment only after baseline.
- **Preconditions:** multi-variant generated, NOT yet selected (locked); then selected (unlocked).
- **Steps:** before select → fields disabled; after select → fields enabled; fill & capture.
- **Locator strategy:** `getByLabel('Target selector'|'Element label'|'OD ID (optional)'|'Severity'|'Intent'|'Note')`; `getByRole('button', { name: 'Capture Comment' })`.
- **Expected evidence:** axe scan of the form (label association, `aria-describedby` for errors per UI-SPEC); focus screenshots; trace.
- **Assertion:** all fields `disabled` while locked; enabled & labelled when unlocked; capture appends to stream.
- **Failure interpretation:** fields editable while locked → the baseline gate is cosmetic; comments could be captured against a null revision head.
- **Layers:** L1 (labels) + L3 (gate) + governance.

#### UPS-PW-S3-2 — Captured comment renders in append-only stream with severity + intent
- **User goal:** See my comment recorded canonically `{target,severity,intent,note}`.
- **Preconditions:** unlocked baseline (`revisionHeadId=rev-0000`).
- **Steps:** fill selector `#root`, label "Root panel", intent "Improve clarity", note "Increase spacing", severity medium; Capture.
- **Locator strategy:** stream `getByRole('list')` in Annotation Panel (testid `ups-comment-stream`) → list items by text.
- **Expected evidence:** screenshot of stream; trace.
- **Assertion:** one list item containing `#root`, `[medium]`, `Improve clarity`, and the note; note field clears after capture (hook behavior); state badge → `CommentsCaptured`.
- **Failure interpretation:** comment not appended or overwriting a prior one → breaks append-only canonical-comment contract (D-003) on which deterministic synthesis depends.
- **Layers:** L3 + L5 (append-only evidence pack).

#### UPS-PW-S3-3 — Comment severity selector exposes the four canonical severities
- **User goal:** Classify a comment by severity that drives task priority.
- **Preconditions:** unlocked.
- **Locator strategy:** `getByLabel('Severity')` → options.
- **Expected evidence:** option DOM list.
- **Assertion:** options exactly `['blocker','high','medium','low']` (drives `inferPriority` p0..p3 ordering used by synthesis).
- **Failure interpretation:** missing/extra severity → synthesis ordering (blocker→low) is no longer well-defined (Q10 determinism risk).
- **Layers:** L3.

### A.4 S4 — MutationApprovalPanel (synthesize, approve, apply, apply-gate, task list)

#### UPS-PW-S4-1 — Synthesize produces a deterministic draft task list from comments  `[partly EXISTS via prepareDraftFlow]`
- **User goal:** Turn my comments into reviewable draft tasks.
- **Preconditions:** ≥1 comment on head revision.
- **Steps:** Capture a comment → click "Synthesize Draft".
- **Locator strategy:** `getByRole('button', { name: 'Synthesize Draft' })` (testid `ups-synthesize-batch`); draft list `getByTestId('ups-draft-task-list')`; status `getByText(/draftStatus=draft/)` (testid `ups-approval-status`).
- **Expected evidence:** screenshot of task list; trace.
- **Assertion:** `draftStatus=draft`; task list non-empty; one task per distinct comment target; state badge `MutationDrafted`.
- **Failure interpretation:** empty/duplicated tasks → the deterministic fold (`CommentEvent→MutationTask`, Q10) is broken; user approves a draft that does not represent their comments.
- **Layers:** L3 + L5 (domain: deterministic synthesis).

#### UPS-PW-S4-2 — Apply is disabled until manual approval (manual governance D-004)  `[EXISTS: wp02wp03::UPS-UI-006]`
- **User goal:** Be unable to apply an unapproved draft.
- **Preconditions:** draft synthesized, not approved → `applyGate=pending`.
- **Steps:** observe Apply disabled + `applyGate=pending`; click "Approve Draft"; observe Apply enabled + `applyGate=satisfied`.
- **Locator strategy:** `getByRole('button', { name: 'Apply Approved Batch' })` (testid `ups-apply-batch`); `getByRole('button', { name: 'Approve Draft' })` (testid `ups-approve-batch`); gate text `getByText(/applyGate=(pending|satisfied)/)` (testid `ups-apply-gate`).
- **Expected evidence:** before/after screenshots; trace; axe of disabled button (disabled-reason exposure per UI-SPEC).
- **Assertion:** Apply `disabled` while draft; enabled only after approve; gate flips pending→satisfied.
- **Failure interpretation:** Apply enabled pre-approval → **draft-first / manual-approval invariant broken** (tier-2 disposal bypassed). This is a top governance test (see GOV-3).
- **Layers:** L3 + L1 (disabled-reason) + governance.

#### UPS-PW-S4-3 — Approve is disabled when there is no draft
- **User goal:** Not approve nothing.
- **Preconditions:** session with baseline but no synthesized draft.
- **Locator strategy:** `getByRole('button', { name: 'Approve Draft' })` (`approvalPending=false`).
- **Assertion:** Approve disabled until a draft exists; Synthesize enabled.
- **Failure interpretation:** approve-without-draft → could approve a phantom batch.
- **Layers:** L3.

### A.5 S5 — RevisionTimeline (append-only manifest)

#### UPS-PW-S5-1 — Successful apply appends exactly one revision row  `[EXISTS partial: wp02wp03::UPS-UI-007 asserts count 1]`
- **User goal:** See one immutable record per apply.
- **Preconditions:** full flow to apply (single-variant fixture is shortest).
- **Steps:** run init→...→apply once.
- **Locator strategy:** timeline `getByRole('list')` in Revision Timeline (testid `ups-revision-list`) → items.
- **Expected evidence:** screenshot of timeline; trace; network log of the apply response (revision payload).
- **Assertion:** exactly **one** new row after one apply; row shows `revision=rev-0001 parent=rev-0000`, `batch=…`, `diff=a/c/r`.
- **Failure interpretation:** zero rows → manifest not appended; two rows → **one-manifest-append-per-apply invariant (I7) violated** (see GOV-4 for the double-apply twin).
- **Layers:** L3 + governance.

#### UPS-PW-S5-2 — Timeline is a semantic ordered list (screen-reader order)
- **User goal:** AT reads revisions newest-first in order.
- **Preconditions:** ≥2 applied revisions `[MOCK-EXT: re-comment on new head + apply again — requires comment against rev-0001]`.
- **Locator strategy:** `getByRole('list')` → `getByRole('listitem')` ordering; component uses `<ol>` (good).
- **Expected evidence:** ARIA snapshot of the `<ol>`; screenshot.
- **Assertion:** rows are `<li>` under `<ol>`, ordered newest-first (manifest `newestFirst=true`).
- **Failure interpretation:** non-list markup → screen-reader cannot convey revision sequence (L1); wrong order → lineage misread.
- **Layers:** L1 + L3.

### A.6 S6 — HandoffSummaryPanel (export, refresh, bundle refs)

#### UPS-PW-S6-1 — Export handoff after a revision yields bundle references
- **User goal:** Export downstream refs (stories/requirements/acceptance/uiSpec/testSpec).
- **Preconditions:** ≥1 applied revision (else mock returns 409 `HANDOFF_REVISION_REQUIRED`).
- **Steps:** complete apply → click "Export Handoff".
- **Locator strategy:** `getByRole('button', { name: 'Export Handoff' })` (testid `ups-export-handoff`); status `getByText(/handoff=(pending|refresh-required|ready)/)` (testid `ups-handoff-status`); bundle list `getByTestId('ups-handoff-list')`.
- **Expected evidence:** screenshot of bundle list; trace; network log of export response.
- **Assertion:** `handoff=ready`; list shows `stories=`, `requirements=`, `acceptance=`, `uiSpec=…UI-SPEC.md`, `testSpec=…TEST-SPEC.md`.
- **Failure interpretation:** export succeeding with no revision → would violate `HANDOFF_REVISION_REQUIRED` precondition (handoff of an empty session).
- **Layers:** L3.

#### UPS-PW-S6-2 — Export before any revision shows a recoverable error, not a bundle  (ERR — see ERR-7)
- **User goal:** Be told I need a revision first, with my work intact.
- **Preconditions:** baseline set, no apply yet.
- **Steps:** click "Export Handoff".
- **Locator strategy:** error `getByRole('alert')`.
- **Expected evidence:** screenshot of alert; trace.
- **Assertion:** `role="alert"` shows "Export requires at least one applied revision." (mapped from `HANDOFF_REVISION_REQUIRED`); no bundle list rendered; session/comments preserved.
- **Failure interpretation:** silent failure or lost session → D5 "never lose the human's work" violated.
- **Layers:** L1 (alert) + L3.

### A.7 IND — SessionStateIndicator (aria-live state, gate badges, baseline badge)

#### UPS-PW-IND-1 — Indicator reflects every domain state transition  `[EXISTS: wp02wp03::UPS-UI-007]`
- **User goal:** Always see the current session state.
- **Preconditions:** `?variantCount=1` (shortest path to all states).
- **Steps:** drive Prompt→Generate→Comment→Synthesize→Approve→Apply, asserting badge after each.
- **Locator strategy:** badge `.ups-state-badge` (consider exposing as `getByRole('status')` — see A11Y-3); gate metas via testids `ups-apply-gate-badge`, `ups-baseline-badge`.
- **Expected evidence:** screenshot per transition; trace of full sequence.
- **Assertion:** sequence `SessionInitialized → PromptCaptured → BaselineReady → CommentsCaptured → MutationDrafted → MutationApproved → RevisionRecorded`.
- **Failure interpretation:** a skipped/wrong state → state machine regression; the user loses the "where am I" anchor (D5 cognitive-load).
- **Layers:** L3.

#### UPS-PW-IND-2 — State changes are announced once via aria-live="polite"  (A11Y — see A11Y-3)
- See A11Y-3.

---

## PART B — BY STUDIO WORKFLOW (end-to-end spine)

### UPS-PW-FLOW-1 — Full multi-variant happy path (init→handoff), the golden trace
- **User goal:** Complete one full evolution cycle and hand off.
- **Preconditions:** default `variantCount=3`.
- **Steps (the named spine):**
  1. **init** — auto-start (`SessionInitialized`).
  2. **prompt** — fill Prompt "Prototype onboarding dashboard" → Submit (`PromptCaptured`).
  3. **generate** — Generate (`VariantsReady`, 3 cards, `selectionGate=pending`).
  4. **select/commit baseline** — "Select Baseline B" (`BaselineReady`, `selectionGate=satisfied`, annotation unlocked).
  5. **confirm identity/DNA** — *(MVP surface)* assert the selected card's status/evidence is the durable selection (no auto-select happened: baseline only set by the click). **[MOCK-EXT for full DNA confirm panel — see residue R-DNA.]**
  6. **comment** — fill canonical comment → Capture (`CommentsCaptured`).
  7. **synthesize** — Synthesize Draft (`MutationDrafted`, draft task list).
  8. **approve** — Approve Draft (`MutationApproved`, `applyGate=satisfied`).
  9. **apply** — Apply Approved Batch (`RevisionRecorded`, +1 revision row).
  10. **revision** — assert timeline row `rev-0001 parent=rev-0000`.
  11. **handoff** — Export Handoff (`handoff=ready`, bundle refs).
- **Locator strategy:** entirely user-facing roles/labels/text per panel sections above; testids only for gate/badge evidence.
- **Expected evidence:** one continuous **trace** of the whole cycle; screenshots at each spine step; console-network (zero fatal); axe scan at the start and at the `MutationApproved` decision point.
- **Assertion:** each spine step lands its named state + gate; exactly one revision appended; bundle ready.
- **Failure interpretation:** the first step to break localizes the regression to a workflow stage; a gate that flips without its prerequisite click localizes a governance regression.
- **Layers:** L0 + L1 + L3 (the suite's spine).

### UPS-PW-FLOW-2 — Single-variant committed path (shortest cycle)
- **User goal:** Same cycle with the committed-baseline branch (variantCount=1).
- **Preconditions:** `?variantCount=1`.
- **Steps:** Prompt→Generate (auto `BaselineReady`, committed:A)→Comment→Synthesize→Approve→Apply→Export.
- **Assertion:** committed-branch note present; no Select-Baseline button used; one revision; handoff ready.
- **Failure interpretation:** if a select step is required at count=1 → degraded-graceful contract broken.
- **Layers:** L3.

### UPS-PW-FLOW-3 — Second cycle on the new head (revision lineage)
- **User goal:** Iterate again after apply, against the new revision head.
- **Preconditions:** after FLOW-2 apply, `revisionHeadId=rev-0001`.
- **Steps:** comment against `rev-0001` → synthesize (`sourceRevisionId=rev-0001`) → approve → apply → assert 2 revisions, `rev-0002 parent=rev-0001`.
- **Locator strategy:** revision-head evidence `getByText(/revisionHead=rev-0001/)` (testid `ups-revision-head`).
- **Expected evidence:** trace; timeline screenshot (2 rows).
- **Assertion:** comment/synthesis use the new head; exactly one new append; parent chain correct.
- **Failure interpretation:** commenting/synthesizing against the stale head → `SOURCE_REVISION_INVALID` recovery path (see ERR-3); a silent wrong-parent append → lineage corruption.
- **Layers:** L3 + governance (append-once across cycles).

---

## PART C — GOVERNANCE INVARIANTS AS TESTS (first-class)

These mirror TEST-SPEC invariants I6/I7 and the s4 lead-when matrix. Each has a **UI test** (the
affordance) and, where the claim is a server truth, a **direct-network test** (prove the gate is
server-side, independent of UI state — exactly the pattern UPS-UI-008 established).

### UPS-PW-GOV-1 — variantCount bounds enforced both in UI and server  `[server twin EXISTS in mock; UI EXISTS: UPS-UI-003]`
- **User goal:** Cannot create a session outside 1..3.
- **Preconditions:** mocks installed.
- **Steps:** (UI) assert selector options `[1,2,3]`; (server) `page.evaluate` POST `/sessions` with `requestedVariantCount: 4`.
- **Locator strategy:** UI via `getByLabel('Variant count')`; server via `fetch`.
- **Expected evidence:** option DOM list; network response JSON.
- **Assertion:** UI offers only 1/2/3; server returns **422 `VARIANT_COUNT_OUT_OF_RANGE`** for 4 and for 0.
- **Failure interpretation:** server accepting 4 → bounds invariant is UI-only (bypassable); the UI guard is necessary but not sufficient.
- **Layers:** L3 + L0 (direct network).

### UPS-PW-GOV-2 — Auto-apply is forbidden server-side  `[EXISTS: wp02wp03::UPS-UI-008]`
- **User goal:** No actor (including `system:auto`) can apply without manual disposition.
- **Preconditions:** approved batch in mock.
- **Steps:** drive to a draft; read sessionId from `getByText(/sessionId=/)`; `page.evaluate` POST `…/apply` with `applyRequestedBy: "system:auto"`.
- **Expected evidence:** network response JSON; trace.
- **Assertion:** **409 `AUTO_APPLY_FORBIDDEN`**; no revision appended.
- **Failure interpretation:** a 2xx here → the deepest first-principle violation ("never an unaccountable action"); the agent could mutate durable state without the human. Highest-severity governance test.
- **Layers:** L3 + L0 (direct network) + governance.

### UPS-PW-GOV-3 — Apply requires prior approval (no apply of a draft)
- **User goal:** A draft can never be applied.
- **Preconditions:** synthesized draft, NOT approved.
- **Steps:** (UI) assert Apply disabled; (server) `page.evaluate` POST `…/apply` on the draft batch.
- **Expected evidence:** disabled-button screenshot; network JSON.
- **Assertion:** UI Apply `disabled`; server returns **409 `BATCH_APPROVAL_REQUIRED`** if forced.
- **Failure interpretation:** server applying a draft → draft-first invariant (D-004) is UI-only; tier-2 disposal bypassed.
- **Layers:** L3 + L0 + governance.

### UPS-PW-GOV-4 — One manifest append per apply (no double-append on re-apply)  `[MOCK-EXT]`
- **User goal:** Re-clicking apply (or a retried request) does not append twice.
- **Preconditions:** one applied batch (now `status=applied`).
- **Steps:** (UI) after apply, Apply button is disabled (draft cleared) — assert; (server) `page.evaluate` POST `…/apply` again on the same now-applied batch.
- **Expected evidence:** timeline screenshot (still 1 row); network JSON of the second attempt.
- **Assertion:** second apply returns **409 `BATCH_APPROVAL_REQUIRED`** (batch no longer `approved`) — i.e., it is structurally idempotent-by-state; timeline still has exactly 1 row (I7).
- **Failure interpretation:** a second 2xx + second row → **I7 violated** (manifest append duplicated); lineage/diff accounting corrupted.
- **Layers:** L3 + L0 + governance. *(MOCK-EXT only to assert the re-apply branch explicitly; the mock already transitions batch→applied so the 409 should hold.)*

### UPS-PW-GOV-5 — Escaped text rendering (no injection from prompt/comment)  `[EXISTS: wp02wp03::UPS-UI-008]`
- **User goal:** A malicious comment note renders as inert text, never executes.
- **Preconditions:** unlocked baseline.
- **Steps:** capture a comment with note `<script>alert('x')</script>` and a selector with HTML; observe the stream.
- **Locator strategy:** comment stream (testid `ups-comment-stream`); also `page.on('dialog')` to assert no alert fires.
- **Expected evidence:** screenshot of stream showing literal text; console-network (no dialog event); DOM check that no `<script>` node was injected into the stream.
- **Assertion:** the literal string `<script>alert('x')</script>` is visible as text; `page.on('dialog')` never triggers; `streamLocator.locator('script')` count is 0.
- **Failure interpretation:** an alert dialog or injected `<script>` → stored-XSS via canonical comments; breaks the "escape untrusted text" security constraint and poisons the deterministic synthesis input.
- **Layers:** L3 + L0 (console/dialog) + L5 (security pack).

### UPS-PW-GOV-6 — Comment gate requires satisfied baseline server-side
- **User goal:** Comments cannot be captured before a baseline.
- **Preconditions:** generated, baseline NOT selected (`selectionGate=pending`).
- **Steps:** (UI) fields disabled; (server) `page.evaluate` POST `…/comments` with a full payload.
- **Assertion:** UI fields disabled; server returns **409 `BASELINE_GATE_UNSATISFIED`**.
- **Failure interpretation:** server accepting a pre-baseline comment → annotation gate is cosmetic; a comment binds to a null revision head.
- **Layers:** L3 + L0 + governance.

### UPS-PW-GOV-7 — Lead-when matrix smoke: reversible ops never produce durable rows until tier-2 click
- **User goal:** Encode the s4 D-S0 three-tier matrix as an observable invariant.
- **Preconditions:** run init→prompt→generate→synthesize-draft (all tier-1, reversible).
- **Steps:** perform only tier-1 ops; assert NO revision row and NO committed baseline exist yet; then perform the two tier-2 clicks (Select Baseline, Approve+Apply) and assert durability appears only then.
- **Expected evidence:** screenshots before/after the tier boundary; timeline empty→1-row.
- **Assertion:** before any tier-2 click: `selectionGate=pending` OR committed only via explicit click; revision count 0. After tier-2: durability present.
- **Failure interpretation:** durable state (baseline committed for multi-variant, or a revision) appearing from a tier-1 op → the lead-when boundary leaked; the agent acted durably without human disposition.
- **Layers:** L3 + governance (the matrix as a test).

---

## PART D — ACCESSIBILITY INTERACTION DETAIL (L1, the gate must be keyboard-first)

### UPS-PW-A11Y-1 — Tab order follows reading order across all panels  (maps Q9)
- **User goal:** Keyboard user reaches every control in the natural top-to-bottom, left-to-right order.
- **Preconditions:** full flow rendered (all panels populated, FLOW-1 fixture) so all controls exist.
- **Steps:** focus body; repeatedly press `Tab`; record `document.activeElement` accessible name at each stop.
- **Locator strategy:** capture `page.evaluate(() => document.activeElement…)` accessible name/role; expected order: sidebar links → Variant count select → Start Session → Prompt → Submit Prompt → Generate Variants → Select Baseline {A,B,C} → annotation fields (selector→label→odId→severity→intent→note) → Capture Comment → Synthesize Draft → Approve Draft → Apply Approved Batch → Export Handoff → Refresh Bundle.
- **Expected evidence:** ordered list of focused accessible names (DOM-measurement); focus-ring screenshots at each governance control; trace.
- **Assertion:** observed tab sequence equals the DOM reading order; no positive `tabindex` jumps; no focus trap outside a modal; every gate control (Select/Approve/Apply/Export) is reachable by Tab alone.
- **Failure interpretation:** a governance control unreachable by keyboard → "governance is a mouse-only privilege" (s4 Q9 violation), an L1 block; out-of-order focus → cognitive disorientation for AT users.
- **Layers:** L1 (block) + L3.

### UPS-PW-A11Y-2 — Governance actions operable by keyboard (Enter/Space activate gates)
- **User goal:** Dispose durable actions (Select, Approve, Apply) using only the keyboard.
- **Preconditions:** at each gate step.
- **Steps:** Tab to "Select Baseline B" → Enter; Tab to "Approve Draft" → Space; Tab to "Apply Approved Batch" → Enter.
- **Expected evidence:** trace; screenshots of resulting state transitions.
- **Assertion:** each keyboard activation produces the same state transition a mouse click does (gate flips; row appends).
- **Failure interpretation:** keyboard activation no-op while mouse works → tier-2 disposal not keyboard-accessible (L1 block).
- **Layers:** L1 + L3 + governance.

### UPS-PW-A11Y-3 — State indicator announces transitions once via aria-live="polite"  (maps Q9)
- **User goal:** A screen-reader user hears each state change, exactly once, not spammed.
- **Preconditions:** drive a few transitions.
- **Steps:** observe the `aria-live="polite"` container (`.ups-state-indicator`) across transitions.
- **Locator strategy:** assert the live region exists with `aria-live="polite"`; capture ARIA snapshot before/after a transition; verify the badge text node is inside the live region.
- **Expected evidence:** ARIA snapshots pre/post transition; DOM check `aria-live="polite"` present on the indicator; (announcement-once) assert the live region's text changes exactly once per transition, no duplicate re-render churn.
- **Assertion:** indicator container has `aria-live="polite"`; state badge text updates inside it; no double-announce. **Recommendation residue:** also expose the badge as `role="status"` and give the indicator an `aria-label`.
- **Failure interpretation:** missing/`assertive` live region → state changes silent or spammy for AT (D5 "announce once" violated).
- **Layers:** L1.

### UPS-PW-A11Y-4 — Focus trap + return-focus on the apply/approval confirmation  (maps Q9 focus-trap)
- **User goal:** When the irreversible apply requires confirmation, focus is trapped in the dialog and returns to the trigger on close.
- **Preconditions:** **[MOCK-EXT / GAP]** — the current `MutationApprovalPanel` applies via a plain button, NOT a modal. s4 Q9 specifies a focus-trapped return-focus approval modal on `ApplyApprovedBatch`.
- **Steps (target design):** open the apply confirmation; Tab cycles only within the dialog; Esc/Cancel returns focus to "Apply Approved Batch".
- **Locator strategy:** `getByRole('dialog', { name: /Apply/ })`; first/last focusable probe.
- **Expected evidence:** focus screenshots (in-dialog, post-close); ARIA snapshot of the dialog.
- **Assertion:** Tab from the last dialog control wraps to the first (trap); Esc closes and focus returns to the trigger.
- **Failure interpretation:** no trap → keyboard user can Tab "behind" an irreversible confirmation and act on a stale background; no return-focus → user is lost after the most consequential action.
- **Layers:** L1 (block once the modal exists). **This scenario doubles as a gap-detector: the modal does not exist yet (residue R-MODAL).**

### UPS-PW-A11Y-5 — Disabled gate controls expose their reason
- **User goal:** Understand *why* Apply is disabled.
- **Preconditions:** draft not approved (Apply disabled).
- **Locator strategy:** Apply button; per UI-SPEC "Approve/apply buttons expose disabled reasons when gated".
- **Expected evidence:** axe scan; ARIA snapshot of the button + its describing text (`applyGate=pending` note is adjacent — should be wired via `aria-describedby`).
- **Assertion:** the disabled Apply has an accessible disabled-reason (currently only adjacent text `applyGate=pending`; **residue:** associate via `aria-describedby`).
- **Failure interpretation:** disabled with no reason → user stuck, doesn't know the gate is awaiting approval (s4 disabled-reason contract / D-005).
- **Layers:** L1 (gap-detector).

### UPS-PW-A11Y-6 — Route-level axe scan (baseline + post-flow)
- **User goal:** No serious/critical automated a11y findings anywhere in the workbench.
- **Preconditions:** baseline load; and after FLOW-1.
- **Steps:** `AxeBuilder({ page }).analyze()` at load and at `MutationApproved`.
- **Expected evidence:** `accessibility/*.json` per state.
- **Assertion:** zero serious/critical (color-contrast, label, region, landmark-unique, aria-valid).
- **Failure interpretation:** serious findings → L1 block per s6 hard-gate policy.
- **Layers:** L1 (block).

---

## PART E — ERROR / RECOVERY FLOWS (D5: never lose the human's work)

Each asserts: a named/clear error surface (`role="alert"`), preserved work, and a safe single action.
Several need mock extensions to emit the s4 D5 named states (`GenerationFailed`, `SynthesisTimedOut`,
`SourceStale`, `ApplyConflicted`) which the current UI/mock do not yet model — those are `[MOCK-EXT]`
and double as gap-detectors for the D5 deepening.

### UPS-PW-ERR-1 — Submit empty prompt → recoverable validation error
- **Preconditions:** session started, prompt blank.
- **Steps:** click Submit Prompt with empty Prompt.
- **Locator strategy:** `getByRole('alert')`.
- **Expected evidence:** alert screenshot; trace.
- **Assertion:** server 422 `PROMPT_REQUIRED`; UI alert "Prompt is required."; session intact; prompt field retains focus/value.
- **Failure interpretation:** crash or lost session → error not handled as recoverable.
- **Layers:** L1 + L3.

### UPS-PW-ERR-2 — Generate before prompt → `PROMPT_NOT_SET` recovery
- **Preconditions:** session started, prompt never submitted (clear it server-side or skip submit).
- **Steps:** click Generate Variants.
- **Assertion:** server 409 `PROMPT_NOT_SET`; alert "Submit a prompt before generating variants."; no variants rendered.
- **Failure interpretation:** variants appearing without a prompt → determinism/source contract broken.
- **Layers:** L3.

### UPS-PW-ERR-3 — Stale revision on comment/synthesis → `SOURCE_REVISION_INVALID` recovery  (maps D5 SourceStale)
- **Preconditions:** head advanced to `rev-0001`, but client attempts comment/synthesis against `rev-0000` `[MOCK-EXT: drive a head advance then force stale sourceRevisionId via evaluate]`.
- **Steps:** attempt synthesis with stale source.
- **Assertion:** server 422 `SOURCE_REVISION_INVALID`; alert "Revision is stale. Refresh session state and retry."; draft + comments preserved; user can re-anchor and retry.
- **Failure interpretation:** silent acceptance → mutation applied against the wrong baseline (lineage corruption); lost comments → D5 violation. **Residue:** add a named `SourceStale` state + a one-click re-anchor action.
- **Layers:** L3 + ERR.

### UPS-PW-ERR-4 — Approve stale batch → `APPROVAL_STALE` recovery
- **Preconditions:** batch source != current head.
- **Steps:** force approve via evaluate (or drive head advance after synth).
- **Assertion:** 409 `APPROVAL_STALE`; recoverable alert; batch preserved.
- **Failure interpretation:** stale approval succeeding → apply against stale source (I7/lineage risk).
- **Layers:** L3.

### UPS-PW-ERR-5 — Generation failure → preserved prompt, safe retry  `[MOCK-EXT]`  (maps D5 GenerationFailed)
- **Preconditions:** force POST `/variants/generate` to 5xx or network-abort `[MOCK-EXT: route.fulfill 500 / route.abort]`.
- **Steps:** Generate.
- **Locator strategy:** `getByRole('alert')`; prompt textbox retains value.
- **Expected evidence:** alert screenshot; console-network (failed request logged); trace.
- **Assertion:** generic recoverable alert ("Unexpected request failure. Please retry." via `toUiMessage`); prompt + session preserved; re-clicking Generate retries deterministically (same genome → same output, D-002).
- **Failure interpretation:** lost prompt or wedged session → D5 violation; no retry affordance → user stuck. **Residue:** add named `GenerationFailed` state + explicit retry/discard.
- **Layers:** L3 + L0 (requestfailed evidence) + ERR.

### UPS-PW-ERR-6 — Synthesis timeout/failure → comments + draft preserved  `[MOCK-EXT]`  (maps D5 SynthesisTimedOut)
- **Preconditions:** force synthesize route to slow/fail.
- **Steps:** Synthesize.
- **Assertion:** recoverable alert; append-only comment stream intact; user can retry synthesis or discard draft without losing comments.
- **Failure interpretation:** comments lost on synthesis failure → the durable source (D-003) was discarded; D5 violation. **Residue:** named `SynthesisTimedOut` state.
- **Layers:** L3 + ERR.

### UPS-PW-ERR-7 — Export before revision → `HANDOFF_REVISION_REQUIRED` (see S6-2)
- Covered in A.6; classified ERR + L1.

### UPS-PW-ERR-8 — Network/runtime fatal during load → L0 smoke block with trace
- **Preconditions:** abort the initial auto-start `/sessions` POST `[MOCK-EXT: route.abort]`.
- **Steps:** goto route.
- **Locator strategy:** `getByRole('alert')`; the page must still render the shell (header + panels render before async hydration per UI-SPEC perf constraint).
- **Expected evidence:** console-network; trace; screenshot.
- **Assertion:** shell still renders (no white screen); an alert explains the failure; no fatal uncaught console error blocks interaction.
- **Failure interpretation:** white screen / uncaught error → L0 block (scenario not inspectable, baseline-layout-before-hydration constraint violated).
- **Layers:** L0 (block) + L1.

---

## PART F — COGNITIVE / ATTENTION (L4, soft flags → s8/L6)

Per s6, L4 is **soft flag / screenshot review only** — never a hard gate without fixture calibration.
These encode the s4 ergonomics proxies (D2/Q6 decision-count, D-006 ceiling) as *reviewable signals*,
and explicitly defer the felt-ergonomics claim to L6/s8 (residue R-5).

### UPS-PW-L4-1 — Variant choice count is bounded (≤3) — decision-breadth proxy
- **Assertion (soft flag):** visible candidate cards ≤ 3; flag if a champion-vs-challenger framing is absent and the user must rank from scratch (D2). Evidence: choice-count measurement + grid screenshot. **Not a block** — names source card "cognitive_load_theory", proxy limit "count is not difficulty".
- **Layers:** L4.

### UPS-PW-L4-2 — Governance gate salience — are disabled-reason and gate state visually prominent?
- **Assertion (screenshot review):** the `applyGate`/`selectionGate` state and disabled Apply reason are within the critical region and not low-salience. Evidence: clipped region screenshots + density measurement.
- **Layers:** L4.

### UPS-PW-L4-3 — Persistent session-state summary across the multi-step flow
- **Assertion (soft flag):** the `SessionStateIndicator` remains visible (sticky/persistent) through all steps so the user keeps a summary anchor (D5 cognitive load). Evidence: per-step screenshots showing the indicator in view.
- **Layers:** L4.

### UPS-PW-L4-4 — Override-as-cheap-as-ratify (D-S1) — reviewer prompt only
- **Assertion (L6 residue):** automation cannot prove "override costs exactly what ratify costs" subjectively. Generate a human-review prompt + task script for s8 naive-user lane. Evidence: `residue-ledger.yml` entry.
- **Layers:** L6 (residue, not automatable).

---

## PART G — Suite organization, fixtures, and CI shape (planning)

### G.1 File layout (target)
```
apps/web/e2e/ui-prototyping-studio/
  mock-api.ts                          # extend with [MOCK-EXT] branches below
  fixtures.ts                          # NEW: composable flow helpers (startToBaseline, toDraft, toApplied, toHandoff)
  ups.shell.spec.ts                    # SHELL-1..3
  ups.s1-controls.spec.ts              # S1-1..3
  ups.s2-canvas.spec.ts                # S2-1..4
  ups.s3-annotation.spec.ts            # S3-1..3
  ups.s4-mutation.spec.ts              # S4-1..3
  ups.s5-revision.spec.ts              # S5-1..2
  ups.s6-handoff.spec.ts               # S6-1..2
  ups.indicator.spec.ts                # IND-1..2
  ups.flow.spec.ts                     # FLOW-1..3 (golden traces)
  ups.governance.spec.ts               # GOV-1..7 (UI + direct-network)
  ups.a11y.spec.ts                     # A11Y-1..6 (axe + keyboard + aria-live + focus trap)
  ups.errors.spec.ts                   # ERR-1..8
  ups.cognitive.spec.ts               # L4-1..4 (tagged @soft-flag / @review)
```
Existing `ui-prototyping-studio.wp01.spec.ts` and `…wp02wp03.spec.ts` are absorbed (their tests map to SHELL/S2/S4/IND/GOV ids above) and can be split into the per-surface files.

### G.2 Fixture helpers (deterministic, reused)
- `startToBaseline(page, {variantCount, baseline})` → init→prompt→generate→(select|commit).
- `toDraft(page, comment)` → adds baseline + one comment + synthesize.
- `toApplied(page)` → toDraft→approve→apply (returns revisionId).
- `toHandoff(page)` → toApplied→export.
Each uses **only user-facing locators**; testids reserved for gate/badge evidence assertions.

### G.3 Determinism controls (s6 implementation note)
Freeze fonts/motion (`prefers-reduced-motion`), seed data via the mock (already deterministic),
fixed viewport (1280×800 desktop, 768×1024 mobile), and stub `Date` for approval timestamps so
screenshots/checksums are stable.

### G.4 Required suite dependencies / extensions (residue, see below)
- Add `@axe-core/playwright` for L1 axe scans.
- Extend `mock-api.ts` with `[MOCK-EXT]` branches: route delay/abort/5xx injection; head-advance for
  stale tests; re-apply-on-applied-batch assertion; (target) D5 named-state responses.
- Add ARIA snapshot baselines for `<main>`, the approval region, and the live indicator.

---

## PART H — Coverage matrix (scenario → surface → workflow stage → s6 layer → governance)

| Scenario | Surface | Workflow stage | s6 layers | Governance invariant |
|---|---|---|---|---|
| SHELL-1/2/3 | shell | (all) | L0,L1,L2 | — |
| S1-1 / GOV-1 | SessionControls | init/generate | L3,L0 | variantCount bounds |
| S1-2/3 | SessionControls | prompt | L1,L3 | — |
| S2-1 | VariantCanvas | generate | L3,L4 | variantCount ceiling |
| S2-2 / GOV-7 | VariantCanvas | select baseline | L3 | gate sequencing / lead-when |
| S2-3 | VariantCanvas | commit baseline | L3,L4 | degraded-graceful |
| S2-4 / A11Y | VariantCanvas | confirm identity | L1 | — |
| S3-1 / GOV-6 | Annotation | comment | L1,L3,L0 | baseline gate (server) |
| S3-2/3 | Annotation | comment | L3,L5 | append-only comments |
| S4-1 | Mutation | synthesize | L3,L5 | deterministic fold |
| S4-2 / GOV-3 | Mutation | approve | L1,L3,L0 | manual approval / draft-first |
| S5-1 / GOV-4 | Revision | apply | L3,L0 | one append per apply (I7) |
| S5-2 | Revision | revision | L1,L3 | — |
| S6-1 / S6-2 / ERR-7 | Handoff | handoff | L1,L3 | revision-required precond |
| IND-1 / A11Y-3 | Indicator | (all) | L3,L1 | — |
| FLOW-1/2/3 | (all) | full spine | L0,L1,L3 | append-once across cycles |
| GOV-2 | Mutation | apply | L3,L0 | **auto-apply forbidden** |
| GOV-5 | Annotation/stream | comment | L3,L0,L5 | escaped text |
| A11Y-1/2/4/5/6 | (gates) | (all) | L1 | keyboard-first governance |
| ERR-1..8 | (varies) | (varies) | L0,L1,L3 | preserve work / recoverable |
| L4-1..4 | (varies) | (varies) | L4,L6 | ergonomics proxies (soft) |

---

## PART I — Residue (owned, not hidden)

- **R-MOCK:** `mock-api.ts` lacks D5 named-state responses and failure-injection; several ERR/GOV
  scenarios are `[MOCK-EXT]`. Owner: execution stage. Until added, those scenarios assert current
  degraded behavior + flag the gap.
- **R-DNA:** No dedicated "confirm identity/DNA" panel exists in the implemented UI; the workflow's
  "confirm identity/DNA" stage currently == the baseline-selection/variant-status surface. FLOW-1
  step 5 asserts the available surface; full DNA-confirm coverage waits on that UI (s4 D1/D-XC).
- **R-MODAL:** `ApplyApprovedBatch` is a plain button, not the focus-trapped return-focus modal s4 Q9
  specifies. A11Y-4 is a gap-detector; the trap test activates once the modal lands.
- **R-ARIA-BASELINE:** `VariantCanvas` exposes baseline status via class+text but no `aria-label`
  (UI-SPEC requires it); S2-4 will fail until added — intentional gap-detector.
- **R-DESCRIBEDBY:** disabled Apply has adjacent reason text but no `aria-describedby` wiring;
  A11Y-5 gap-detector.
- **R-AXE-DEP:** `@axe-core/playwright` not yet a dependency; all L1 axe scans blocked on adding it.
- **R-ERGONOMICS (= s4 R-5):** No L4/L6 scenario *proves* an ergonomic gain; override-cheapness,
  decision-paralysis reduction, and naive-user stalls are explicit L6 residue routed to s8.
- **R-STATE-RENAME:** the mock emits `RevisionRecorded` after apply (not `RevisionApplied`); the plan
  follows the mock. If the domain machine intends a distinct `RevisionApplied→RevisionRecorded` pair,
  IND-1's expected sequence must be revisited.
