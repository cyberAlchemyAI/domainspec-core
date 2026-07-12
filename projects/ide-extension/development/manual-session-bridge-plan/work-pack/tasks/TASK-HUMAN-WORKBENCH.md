# Task Contract: Human Workbench

## Task Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-HUMAN-WORKBENCH` |
| Objective | Make preparation, authorization, targeting, claim, recovery, and evidence truthful and operable in the existing HTML workbench. |
| Layer / slice / wave | L0 / S-003 / W2 |
| Dependencies | `SWU-MSB-005`; join `SWU-MSB-006` before 008. |
| Execution owner | Task Session (`local-fallback`). |

## Source Handles And UX Invariants

- [Approved UX plan](../../../manual-session-bridge-design/UX-PLAN.md)
- [Shared traceability](../shared/traceability.md)
- Runtime anchors: `public/demo/l0.html`, workbench/API tests, and existing
  Playwright harness.
- Preserve the dense operational workbench. Use existing controls, live regions,
  status system, and responsive conventions; do not add a marketing surface.
- Never imply that approval executed a skill or that `session_ref` is authenticated.

## SWU-MSB-007: Task, Approval, And Receipt Truthfulness

**Goal:** Repair preparation and approval so the operator supplies an explicit
task and sees authorization and execution as different evidence.

**Dependencies:** `SWU-MSB-005` pass.

**Exact write scope:** `public/demo/l0.html` and focused DOM/workbench/API tests.

**Implementation rules:**

1. Add a visible, labeled, required task field to Prepare; whitespace-only input
   fails before submission and receives accessible inline error/focus behavior.
2. Show selected skill, task, and L0 effect boundary in proposal detail for the
   operator, while keeping agent-facing pre-claim APIs private.
3. Replace no-op/execution approval language with `Approve request` and explain
   that approval authorizes only.
4. Render authorization receipt kind, bindings, assurance, and claim separately
   from execution receipt status/result/evidence.
5. Preserve prepare, connect, history, keyboard, focus, and live-region behavior.
6. Unknown/legacy receipts remain readable with an explicit legacy label.

**Edge cases:** blank task; long unbroken task/skill; legacy proposal; only one
receipt; missing optional evidence; narrow mobile layout; refresh during approval.

**Done criteria:** task is required and persisted; approval UI makes no execution
claim; both receipt types are distinguishable; existing workbench behavior passes.

**Acceptance evidence / validation:** focused DOM/API tests, accessibility name
checks, existing workbench suite, manual narrow-width inspection.

**Expected result:** `pass` with screenshots/test evidence. **Handoff:** join
`SWU-MSB-006`, then route 008.

## SWU-MSB-008: Target, Claim, Recovery, And Result UX

**Goal:** Expose the full operator side of the manual bridge without granting
session-owned actions to the browser UI.

**Dependencies:** `SWU-MSB-006` and `SWU-MSB-007` pass.

**Exact write scope:** `public/demo/l0.html` and bridge-specific workbench tests.

**Implementation rules:**

1. Add ready/unready actions only for legal states and show the singleton ready
   target prominently in Approval Desk.
2. Refuse a second ready action with a visible conflict; never silently replace.
3. Render `claimed` as `Claimed by unattested local session`, with attempt/session
   handles but no authenticated-identity language.
4. Render interruption reason/history and expose `Release and requeue` only to
   the operator in `interrupted` state.
5. After release, show `approved`; require another explicit ready action.
6. Render terminal result summary, validation, evidence refs, and execution
   receipt together, while retaining the authorization receipt.
7. Announce concise state changes without stealing focus and disable stale actions.

**Edge cases:** zero/multiple ready projection; stale action response; claim occurs
while detail is open; refresh after interrupt; missing artifact; terminal result
arrives during polling; mobile action wrapping.

**Done criteria:** every v2 state has truthful status/actions; operator-only
recovery is enforced both visually and by API; receipt/evidence navigation works;
desktop and narrow layouts do not overlap or shift incoherently.

**Acceptance evidence / validation:** workbench state/action tests covering every
transition and error, accessibility assertions, responsive manual inspection.

**Expected result:** `pass` with state matrix evidence. **Handoff:** W2 exit gate,
then `SWU-MSB-009`.

## Synchronization

- Keep session CLI and workbench scopes separate until their join before 008.
- Any request to add timers, auto-polling, IDE chrome, or remote adapters is
  recorded as deferred residue outside active L0.
