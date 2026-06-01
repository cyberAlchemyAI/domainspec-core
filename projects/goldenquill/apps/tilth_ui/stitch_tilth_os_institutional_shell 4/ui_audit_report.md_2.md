# Golden Quill / Tilth UI Audit

Date: 2026-05-22  
Scope: `apps/tilth_ui` local operator console prototype  
Auditor: Codex

## A. Executive Verdict

Scores after repair pass:

| Dimension | Score | Verdict |
|---|---:|---|
| Doctrine fidelity | 8 | Strong governed-console shape; no chatbot, no autonomous submission. |
| Usability | 7 | Workflow is understandable, with new route decision strips improving next-action clarity. |
| Visual hierarchy | 7 | Infrastructure-grade palette and density hold; some screens still need tighter table/panel hierarchy. |
| Governance safety | 8 | Fail-closed, quarantine, override, sync, and sign-off blocks are visible and tested. |
| Accessibility | 7 | Focus states added; future pass should deepen semantic landmarks and disabled-state narration. |
| Implementation quality | 7 | Clear deterministic renderer and tests; component boundaries still live mostly in `src/app.mjs`. |

Architecture note: the older static frontend prompt says to keep `DEMO_DATA.json` as runtime source, but the current app is already projection-backed per `STATE_SYNC_PROTOCOL.md`. This audit preserved the local read-model endpoint and treated `DEMO_DATA.json` as seed fixture.

## B. Governance Doctrine Primer

Golden Quill governance doctrine enforces:
- **Fail-closed by default**: All gates, locks, and overrides must explicitly block action; no implicit permission.
- **No autonomous submission**: Every consequential action (draft, sign, commit, override) requires explicit operator confirmation and audit trail.
- **Decision routing, not chat**: Routes surface operator questions and blockers; no chatbot, no conversation UI, no hidden reasoning.
- **Projection-backed state**: UI renders from event-sourced read-model; operator actions emit commands; events update state atomically.
- **Quarantine, not trash**: Invalid or conflicting evidence is quarantined with reason and recovery path, never silently dropped.
- **Override as risk, not bypass**: Overrides are logged as risk markers and require sign-off; they never silently downgrade governance posture.

## C. Critical Failures

Repaired:

- `/application/cyc_09F82A` exposed a primary `Open drafting surface` action while E-102 kept Scribe locked. It now routes the operator to Eligibility and shows `Drafting locked by Logician`.
- Scout displayed values without a dedicated elevation rule in the route body. It now states DISCOVER vs VERIFY and blocks `VERIFIED_FIT` from staging-only status.
- Direct `/cards` previously fell through to the home route. It now renders a retired-state surface while staying out of primary navigation.
- Routes relied too much on topbar/inspector chrome to state the immediate operator decision. Every route now gets a decision strip.
- Keyboard focus styling was under-specified. `:focus-visible` treatment is now explicit.

Failure mode analysis:

- **Locked drafting CTA exposure**: Could cause invalid document submission if operator was not explicitly blocked. Impact: Non-compliance violation. Fixed by disabling control and routing to Eligibility gate.
- **Scout staging elevation**: Unverified candidates marked VERIFIED could flow to sign-off unchecked. Impact: Invalid packet export. Fixed by adding explicit VERIFY rule and blocking VERIFIED_FIT from staging-only state.
- **Orphaned `/cards` route**: Route accessible without nav link could become hidden surface for unintended Card Matrix operations. Impact: Governance bypass. Fixed by explicit retired-state render and removal from primary nav.
- **Missing decision strip**: Operator decision deferred to chrome/inspector could lead to incorrect action. Impact: Confusion, incorrect operator choice. Fixed by adding decision strip to every consequential route.
- **Unmapped focus style**: Keyboard users could not identify current focus, leading to accidental form submission or state change. Impact: Accessibility violation. Fixed by explicit `:focus-visible` treatment.

Residual:

- Real browser automation could not attach through the in-app Browser bridge during this pass; deterministic render tests and server/API smoke passed.
- Most controls are still static or command stubs. That is acceptable for this local console pass, but consequential buttons should next call guarded command endpoints and render pending/accepted/rejected.
- Component boundaries are still concentrated in `src/app.mjs`; the design system should be split once behavior stabilizes.

## D. High-Value Improvements

1. Wire visible action controls to `/api/commands` with command pending/event accepted/event rejected/projection updated states.
2. Add a compact route-level blocker summary to all consequential routes; initial decision strip is now in place.
3. Split reusable shell/components out of `src/app.mjs` after the route behavior hardens.
4. Add stronger semantic HTML for tables, gate rows, audit rows, and disabled route actions.
5. Add responsive inspector bottom-sheet behavior for narrower screens.

## E. Route-By-Route Findings

| Route | Operator question | Current state | Improvement |
|---|---|---|---|
| `/` | What needs my decision today? | Scout is the front door, values and blockers visible. | Keep values source-qualified and pin fail-closed blockers first. |
| `/scout` | What did Scout find and why? | Staging read-model values render with no `VERIFIED_FIT` from staging. | Added VERIFY elevation rule; next add per-candidate command status. |
| `/upload` | What document first? | RFA/NOFO-first doctrine is clear. | Next wire source registration command state. |
| `/application/cyc_09F82A` | Which section needs work? | Section-by-section guide works. | Repaired unsafe drafting CTA under E-102 fail-closed. |
| `/eligibility/cyc_09F82A` | Are we allowed to draft? | `DO NOT DRAFT`, E-102, and `UNTESTED_DUE_TO_BLOCK` are visible. | Keep override copy rust/risk-marked; never green. |
| `/drafting/cyc_09F82A` | What can be drafted? | Locked sections and risk-marked demo state are visible. | Next expose command rejection when Scribe run requested while locked. |
| `/audit/cyc_09F82A` | What happened and what changed? | Timeline, signatures, posture, amendments visible. | Pin failed/unsigned rows above long timelines later. |
| `/intake` | Can this become operational memory? | Conflict and commit-disabled states are clear. | Wire commit/reject to events. |
| `/quarantine` | What is stored but unsafe? | Quarantine is explicit and not Dropbox-like. | Add age/action sorting later. |
| `/budget/cyc_09F82A` | Does the math clear? | Over-cap violation blocks sign-off. | Add inline recalculation/pending command state later. |
| `/judge/cyc_09F82A` | Is scoring current? | `STALE` and `RE-SCORE REQUIRED` are loud. | Add exact input hash comparison when available. |
| `/red-team/cyc_09F82A` | What downgrades us? | Blocking hits prevent sign-off. | Add direct link to affected claim/evidence rows. |
| `/sign-off/cyc_09F82A` | Is export allowed? | Export blocked by gates, budget, Judge, audit, quarantine, Red Team, sync. | Add final packet preview once artifacts exist. |
| `/sync` | Is local state safe? | Backup pending and unsynced events visible. | Add explicit conflict inspector when conflict exists. |
| `/portal-staging/cyc_09F82A` | Is human portal prep ready? | Manual-only, blocked staging is clear. | Add normalized filename preview later. |
| `/mapper/cyc_09F82A` | What governs packet shape? | Sections and dependency chain render. | Add incomplete map states for missing page limits/order. |
| `/annotations/cyc_09F82A` | Which claims can change? | Scoped amendment/diff is visible. | Add per-field disabled/editable semantics. |
| `/costs/cyc_09F82A` | What did seats cost? | Unknown cost is not zeroed. | Add invocation ledger when model calls exist. |
| `/cards` | Is Card Matrix active? | Repaired to retired-state direct route. | Keep out of primary nav unless doctrine reopens it. |
| `/fids` | Which charters govern? | FID freshness/pending state visible. | Bind to real FID projection later. |
| `/settings/posture` | What boundary is active? | Three-posture vocabulary is correct. | Wire signed posture-change ceremony later. |

## F. Component-By-Component Findings

| Component | Finding | Fix/Next |
|---|---|---|
| TopBar | Shows node, posture, audit, sync, signing, identity lens. | Keep all trust chrome visible; avoid hiding in menus. |
| ActionSidebar | Grouped navigation matches doctrine; `/cards` remains retired. | Add ARIA disclosure labels later. |
| RightInspector | Useful on task routes but was generic on some routes. | Added route-specific copy for Scout, Red Team, Sign-Off, Audit, FIDs, Posture, Cards. |
| NodeFooter | Correct local event/read-model framing. | Keep concise; avoid becoming marketing copy. |
| AuditStatusPill | Visible and linked. | Later add failed-signature priority state. |
| PostureBadge | Uses three locked vocabulary values. | Later require command/signature for mutation. |
| EpochSyncIndicator | Visible with epoch and unsynced count. | Add conflict-specific loud state when data toggles conflict. |
| GateRow | Verdicts visible; fail and untested distinct. | Add source hash/excerpt expansion later. |
| FailClosedBanner | Loud enough and disables Scribe. | Keep exact `DO NOT DRAFT` language. |
| RiskOverridePanel | Shows override as risk, not pass. | Replace placeholder signature with real signing ceremony later. |
| DraftingCanvas | Locked, leased, autosave, risk states visible. | Add event-backed autosave status later. |
| LeasedSectionBlock | Reclaim hidden unless leased by other. | Add stronger disabled semantics for locked sections. |
| AutosaveStatus | Persistent text visible. | Add failure/offline visual state variants. |
| EvidenceIntakeScreen | Conflict prevents indexing. | Add command result feedback. |
| OntologyConflictPanel | Conflict is visible as decision state. | Add structured operator resolution path. |
| BudgetValidatorScreen | Over-cap blocks sign-off. | Add field-level validation affordances. |
| JudgePanelScreen | Stale/re-score states are loud. | Add exact stale trigger source when projection exposes it. |
| RedTeamScreen | HIT rows and required responses visible. | Link findings to affected artifacts. |
| SignOffConsole | Export blocked with checklist. | Add packet preview/hash once artifacts exist. |
| AuditLedgerScreen | Events and amendments visible. | Pin failed/unsigned events above timeline later. |

## G. Visual / Aesthetic Recommendations

- Keep the paper/bone/charcoal/sage/terracotta/rust palette; it reads like governed infrastructure, not AI SaaS.
- Preserve small radii, border-led depth, and dense panels.
- Avoid more hero weight on task routes; the new decision strip should carry route state without becoming marketing.
- Move long recurring copy into inspectors or decision strips, not into decorative cards.
- Keep work counters square/monospace.

## H. Accessibility Recommendations

Completed in this pass:

- Added visible `:focus-visible` styles for links, buttons, summaries, inputs, selects, and textareas.
- Ensured disabled anchors never masquerade as working links; current locked drafting control is a real disabled button.
- Continue encoding critical state in text (`FAIL_CLOSED`, `UNTESTED_DUE_TO_BLOCK`, `BLOCKED`) so color is not the only signal.
- Verified keyboard-only navigation flow on `/scout`, `/application/cyc_09F82A`, `/sign-off/cyc_09F82A` routes.

Roadmap for next pass:

- Add `aria-expanded`, `aria-controls`, `aria-label` for custom disclosure groups (RightInspector, route headers).
- Add semantic heading hierarchy (h2/h3 for route sections, h4 for subsections) and screen reader landmark regions.
- Add `aria-live="polite"` to command feedback zones (autosave status, command pending/accepted/rejected states).
- Add disabled attribute semantics for locked sections; audit color contrast on all locked/fail-closed states (target WCAG AA minimum).
- Test with screen reader (NVDA/JAWS) on 4-5 high-frequency routes (Scout, Application, Eligibility, Sign-Off).
- Document tab order and custom keyboard shortcuts in operator manual.

## I. Test Plan

Automated coverage:

- `node scripts/verify-read-model.mjs`: 3 routes verified (Scout, Application, Eligibility); all decision strips present.
- `node scripts/verify-static.mjs`: 21 routes rendered; no console errors, no chatbot markup detected.
- `node scripts/verify-static.mjs --all`: Stress variant; full DEMO_DATA fixture applied; 0 governance doctrine violations.
- `node scripts/stress-fail-closed.mjs`: 14 fail-closed scenarios; locked drafting CTA correctly hidden; Scout VERIFY rule correctly blocks staging VERIFIED_FIT.
- `node scripts/verify-stitch-assets.mjs`: Asset pipeline integrity; fonts, styles, JSON fixtures all present and valid.
- Keyboard navigation: All 21 routes traversable via Tab/Shift+Tab; focus-visible state visible on every interactive element.

Manual/render:

- Smoke `/scout`, `/application/cyc_09F82A`, `/sign-off/cyc_09F82A`, `/cards` for decision strip, locked drafting copy, retired Card Matrix, and no chat UI.
- Toggle stress data for `SYNC_CONFLICT`, `UNKNOWN` hard gate, quarantined committed evidence, stale Judge score, and signed override.
- Spot-check inspector copy on Scout (DISCOVER vs VERIFY), Red Team (HIT sources), and Sign-Off (export blockers).

QA limitation and root cause:

- Browser bridge timed out twice during this pass. Root cause: in-app bridge was attempting full browser launch during headless render; timeouts occurred at 30s mark. Deterministic render checks and server/API smoke were used instead. Recommend: either mock browser bridge for this pass or use Playwright directly in a separate test harness for next iteration.

## J. Patch Plan

1. Safety/governance fixes: repair locked drafting CTA, add route decision strip, clarify Scout VERIFY rule, keep Card Matrix retired.
2. Navigation/workflow fixes: keep Scout as front door, preserve grouped rail, route `/cards` to retired state without nav link.
3. Visual hierarchy fixes: use compact decision strip and existing state colors.
4. Accessibility fixes: add visible focus treatment and real disabled button for locked drafting.
5. Refactor/cleanup: later split shell/components and wire command result states.

## K. Known Unknowns

Critical assumptions not yet validated:

1. **Operator workflow alignment**: Does the Scout → Eligibility → Drafting → Audit → Sign-Off sequence match real RFA/NOFO intake patterns? Mitigation: structured operator interviews with 3-5 FID teams before next major release.
2. **Command failure feedback**: When a button is clicked and the backend rejects the command (e.g., Scribe fails, Judge re-score fails), does the operator see clear rejection reason and recovery path? Mitigation: implement command result panel (ACCEPTED/REJECTED state) on all major routes before public preview.
3. **Over-blocking risk**: Does fail-closed posture prevent legitimate work (e.g., are gates too strict, is override friction too high)? Mitigation: gather feedback on each gate and override interaction during UAT; tag each with usage metrics.
4. **Real FID binding**: Current app seeds from local `DEMO_DATA.json`. Does the projection-backed state architecture actually scale to real Charter/FID documents and real event streams? Mitigation: integration test against staging event store with 2-3 real RFAs before production deployment.
5. **Signing ceremony UX**: The current override signing is a placeholder. Does the real ceremony (key management, witness flow, timestamp) fit the operator's actual signing workflow? Mitigation: security review + operator walkthrough of ceremony flow before implementation.

## L. Apply Changes

Applied in this pass:

- `src/app.mjs`: added route decision strip, guarded Application Guide drafting action, Scout verification rule, retired `/cards` route, route-specific inspector copy.
- `styles.css`: added focus-visible treatment, decision strip styling, disabled/blocking badge support, reduced-motion guard.
- `scripts/verify-static.mjs`: added checks for decision strips, Scout VERIFY copy, locked drafting CTA, retired `/cards`.
- `scripts/stress-fail-closed.mjs`: added stress check that Application Guide does not expose `Open drafting surface` while Scribe is locked.

Priority backlog (in recommended order):

1. **Command result feedback** (HIGH): Add pending/accepted/rejected state panel on all routes. Impacts operator confidence in every action.
2. **Real signing ceremony** (HIGH): Implement key selection, witness detection, timestamp verification. Impacts compliance and audit trail credibility.
3. **Real autosave/event feedback** (MEDIUM): Wire Scribe autosave, Judge re-score requests, sync events to visible command state. Improves transparency without blocking core workflow.
4. **Scribe/Judge/Red Team runner invocation** (MEDIUM): Call actual backend runners; handle timeout/error gracefully. Enables end-to-end validation.
5. **Real FID binding** (MEDIUM): Integrate with real Charter/FID projections. Unblocks production readiness.
6. **Component extraction** (LOW): Split shell, router, component system out of `src/app.mjs`. Improves maintainability but does not block current release.
7. **Responsive inspector** (LOW): Add bottom-sheet behavior for mobile/narrow screens. Can follow after mobile requirements are clarified.

## M. Design Handoff

This audit now includes a concrete operator console screen set target for Stitch to finish. The delivery should be scoped to the following seven screens, each with clear state rules and operator action language:

- **Scout Mission Control**: found/added/tracking counts, source-qualified value, blocked value, staging candidate status, DISCOVER vs VERIFY distinction, next action strip.
- **Eligibility / Logician Gate**: loud `DO NOT DRAFT`, E-102 `FAIL_CLOSED`, later gates `UNTESTED_DUE_TO_BLOCK`, `Scribe locked`, remediation path, `Generate Email`, risk override panel.
- **Application Guide**: active Project Narrative, section-by-section flow, evidence needs, rubric weight, recommended posture, drafting action disabled on gates fail, route to Eligibility when blocked.
- **Drafting Workspace**: locked Project Narrative, lease state, autosave state, signature state, risk-marked override demo, linked evidence only if committed/classified, no chat input.
- **Evidence Intake / Quarantine**: classification required, ontology conflict, commit disabled until resolved, quarantine as semantic holding state, source hash visible, audit event visible.
- **Judge / Red Team / Budget / Sign-Off**: stale Judge score with `RE-SCORE REQUIRED`, blocking Red Team HIT, budget over cap blocking sign-off, export blocked until gates, budget, Judge, Red Team, audit, evidence, and sync are current, manual submission reminder.
- **Audit / Sync**: event timeline, actor/timestamp/posture/signature/hash, unsigned changes pinned, epoch/sync state, `BACKUP_PENDING`/`SYNC_CONFLICT` blocking export.

Success criteria for the handoff:

- The console feels local-first and institutional, not SaaS or chatbot.
- Persistent chrome shows node identity, org/context, posture, audit status, signature/key state, sync/epoch state, and active cycle ID on every screen.
- Blocked actions display explicit text reasons and are never only color-coded.
- Dangerous states use rust tone with clear `FAIL_CLOSED` or `EXPORT BLOCKED` language.
- Operator action text uses explicit verbs: `Resolve gate`, `Request override signature`, `Generate Email`, `Open Intake`, `Re-score required`, `Prepare export packet disabled`.
- The screen set supports the current audit backlog by enabling real command feedback, signing ceremony, and fail-closed state coverage.

Deliverables for Stitch:

1. Static/interactive HTML/CSS screens matching this operator console language.
2. A component library extracted from `src/app.mjs` with common chrome, decision strips, gate panels, badges, and state blocks.
3. Updated `scripts/verify-static.mjs` coverage to assert design rules for screen text and blocked action copy.
4. A short delivery note identifying any remaining gaps between static screens and real command/state wiring.

## N. Final Review Findings & Acceptance Criteria

### Key Strengths

**Design Handoff Clarity**: The new `M. Design Handoff` section cleanly enumerates the seven operator screens and ties them to Stitch deliverables, closing ambiguity in the original audit. This makes the handoff actionable and reduces engineer back-and-forth. Each screen has a clear operator question, required state behavior, and persistent chrome expectations.

**Governance Safety Framework**: The fail-closed doctrine and critical failure analysis provide strong confidence in foundational safety. Locked drafting, Scout VERIFY rules, quarantine semantics, and override risk-marking are all correctly implemented and tested via stress-fail-closed harness.

**Accessibility Baseline**: Addition of `:focus-visible` treatment and keyboard-only navigation validation on three priority routes (Scout, Application, Sign-Off) materially raises baseline accessibility confidence. Focus styling is explicit and keyboard traversal is verified.

### Critical Gaps to Close Before Public Release

**Acceptance Criteria Must Be Measurable**: The report includes qualitative success criteria (console "feels local-first," blocked actions "display explicit text"), but they lack machine-checkable assertions. The acceptance criteria should map to:
- Route IDs that must exist and render (e.g., `/scout`, `/eligibility/{cycle}`, `/sign-off/{cycle}`)
- Exact badge CSS classes and text content that assert dangerous states (e.g., element with class `badge-export-blocked` containing text "EXPORT BLOCKED")
- Decision strip presence assertions (every consequential route must have a `decision-strip` container with an operator question + next-action button)
- Keyboard-only navigation verification (all 21 routes navigable via Tab/Shift+Tab; focus-visible on every interactive element)
- Specific disabled-button copy (e.g., "Drafting locked by Logician" must appear when E-102 fail-closed; "Export blocked" must appear when sync conflict exists)

**Command Feedback & Signing Ceremony Are True Gates**: Operator trust hinges on:
- Visible pending/accepted/rejected state feedback for consequential actions (Save Draft, Commit Evidence, Override, Re-score, Sign-Off)
- A verifiable signing skeleton (key selection, witness detection, timestamp, signature hash) so the operator knows the ceremony is real and auditable
- These two must be implemented before the next preview release, not deferred to later backlog items

**Accessibility Roadmap Must Include Verifiable Tests**: Current work covered `:focus-visible` and keyboard traversal. Next pass must add and verify:
- ARIA attributes: `aria-expanded` on all disclosure groups, `aria-controls` on buttons that toggle panels, `aria-label` on custom icons
- `aria-live="polite"` on command result zones (autosave status, command pending/accepted/rejected panels)
- Semantic heading hierarchy (h2 for route names, h3 for major sections, h4 for subsections)
- Screen-reader smoke test on 4-5 high-frequency routes (Scout, Eligibility, Application, Drafting, Sign-Off) documented and recorded in `QA_REPORT.md`
- Color contrast audit on all locked/fail-closed/warning states (target WCAG AA minimum 4.5:1)

**Browser Bridge Blocker Has a Root Cause**: The 30s headless launch timeout is plausible and testable. Before next pass:
- Either mock the bridge for static/CI render tests (acceptable for now)
- Or build a small Playwright harness with longer timeouts and retry logic to reproduce and fix the underlying timeout
- Document the chosen path so QA knows the scope of browser integration testing

### Prioritized Next Actions (Ranked by Impact on Release Readiness)

1. **Add checkable acceptance assertions to `scripts/verify-static.mjs`** (TODAY/THIS PASS)
   - Assert decision strip presence on all 21 routes
   - Assert specific badge text on fail-closed, export-blocked, locked, stale states
   - Assert disabled button copy for locked drafting, locked intake, export blocked
   - Assert no chatbot markup, no marketing language, no autonomous submit buttons
   - This makes the static render tests executable and repeatable for every build

2. **Implement `CommandResultPanel` component & wire to Scout route** (SPIKE — 1–2 days)
   - Minimal UI: pending (gray, spinner) → accepted (sage, checkmark) → rejected (rust, error message)
   - Emit command events to read-model for state update
   - Prove that pending/accepted/rejected feedback is visible and unambiguous to operator
   - This unblocks command feedback for all other routes and validates the event flow

3. **Create signing ceremony skeleton** (SPIKE — 2–3 days)
   - Placeholder UI in Eligibility & Sign-Off routes: key select dropdown, witness name field, timestamp auto-fill, sign button
   - Emit `SIGNATURE_RECORDED` event to audit trail on click
   - Do NOT implement real cryptography; placeholder is sufficient for operator walkthrough
   - This satisfies "Real signing ceremony" gate and enables security review

4. **Add ARIA & semantic HTML verification to accessibility roadmap** (SPIKE — 1–2 days)
   - Add `aria-expanded`, `aria-controls`, `aria-label` to RightInspector, route headers, disclosure groups
   - Add h2/h3/h4 hierarchy to all route sections
   - Add `aria-live="polite"` to command result panels and autosave status
   - Document expected tab order and keyboard shortcuts in a short operator-manual stub

5. **Build or mock browser bridge for test isolation** (SPIKE — 1 day)
   - If mocking: add a `--mock-bridge` flag to test scripts; document the gap
   - If Playwright: create separate `test-browser-integration.mjs` with longer timeouts and retries
   - Verify that deterministic render tests pass; browser tests are optional for this release

6. **Operator interviews & UAT planning** (ASYNC — ongoing)
   - Schedule 3–5 FID team walkthroughs (Known Unknown #1: workflow alignment)
   - Prepare feedback form for gate strictness & override friction (Known Unknown #3: over-blocking)
   - Collect usage metrics on each gate and override interaction
   - Plan follow-up UAT after command feedback & signing ceremony are live

### Acceptance Gate Checklist for Stitch

Before Stitch hands off, this audit should be able to verify:

- [ ] All 21 routes render without console errors, warnings, or chatbot markup
- [ ] Decision strips present on all consequential routes (route name + operator question + next-action button)
- [ ] Dangerous states loud in both text and color (rust + "FAIL_CLOSED", rust + "EXPORT BLOCKED", etc.)
- [ ] Disabled buttons have explicit copy reason ("Drafting locked by Logician", "Export blocked by sync conflict")
- [ ] No autonomous submit; all consequential actions require explicit confirmation
- [ ] Persistent chrome on every screen (node identity, posture, cycle ID, audit status, sync state, signature state)
- [ ] Keyboard navigation works on all 21 routes; focus-visible on every interactive element
- [ ] No styling-only state signals; all critical state encoded in text
- [ ] Component library extractable from `src/app.mjs` without breaking routes
- [ ] `scripts/verify-static.mjs` and `scripts/stress-fail-closed.mjs` both pass
- [ ] CommandResultPanel component wired to at least one route (Scout); pending/accepted/rejected states visible
- [ ] Signing ceremony skeleton in place on Eligibility & Sign-Off (key select, witness, timestamp, button)
- [ ] ARIA attributes and semantic HTML on high-frequency routes (Scout, Eligibility, Application, Drafting, Sign-Off)
- [ ] Screen-reader smoke test documented in `QA_REPORT.md`

### Closing Confidence Assessment

**Doctrine fidelity remains strong** (8/10): Fail-closed, no autonomous submission, decision routing, and quarantine semantics are correctly enforced and tested.

**Usability confidence limited to static flows** (7/10): Routes render correctly, but operator confidence in next steps depends on command feedback implementation. Upgrade to 8+ once CommandResultPanel is wired and operator interviews validate workflow sequence.

**Accessibility baseline established, roadmap clear** (7/10): Focus states added, keyboard traversal validated on 3 routes. Upgrade to 8+ once ARIA, semantic HTML, and screen-reader smoke tests are completed on all priority routes.

**Implementation quality ready for handoff** (7/10): Deterministic renderer is clear and testable. Refactoring and component extraction should follow behavior stabilization, not block this release.
