# Task Contract: Validation And Real Witness

## Task Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-VALIDATION-WITNESS` |
| Objective | Prove the complete L0 loop under hostile, restart, browser, and one real blind manual execution condition. |
| Layer / slice / wave | L0 / S-004 / W3 |
| Dependencies | W2 exit gate. |
| Execution owner | Task Session for 009-010; human plus active Codex session for 011. |

## Source Handles And Proof Rule

- [Experiment evidence](../../../manual-session-bridge-design/EXPERIMENT-EVIDENCE.md)
- [Approved UX validation](../../../manual-session-bridge-design/UX-PLAN.md#validation-plan)
- [Shared traceability](../shared/traceability.md)
- Fake claimant tests are the automated oracle. The real witness is required
  evidence, but cannot replace race, restart, binding, or secrecy tests.

## SWU-MSB-009: Hostile, Race, Restart, And v1 Regression

**Goal:** Build the complete automated safety/regression suite before browser or
human proof.

**Dependencies:** `SWU-MSB-008` pass.

**Exact write scope:** bridge integration, adversarial, replay, recovery, and
v1 regression tests plus a focused `test:bridge` package script.

**Required cases:**

1. v1 logs/receipts replay to their prior projection without mutation.
2. Invalid skill/task/effect/receipt/result shapes fail at schema and runtime.
3. Zero/multiple ready, second target, stale target, and wrong actor fail closed.
4. Concurrent claims have one winner; losers receive no skill/task/claim token.
5. Wrong session, hash, attempt, authorization, or evidence binding rejects result.
6. Duplicate interrupt/result/requeue and post-terminal calls are idempotently
   rejected without extra receipts.
7. Restart in ready, claimed, interrupted, and terminal states reproduces state,
   singleton target, attempt history, and receipt references.
8. Storage/artifact failure never leaves a projected success without durable evidence.

**Edge cases:** mixed-version logs; response loss after append; malformed JSON;
oversized summary; missing artifact; unknown event version; test race flakiness.

**Done criteria:** deterministic suite passes repeatedly; no test relies on sleep
for ownership correctness; all ten planning obligations have at least one oracle.

**Acceptance evidence / validation:** `npm run test:bridge` plus existing schema,
lifecycle, adversarial, recovery, and runtime enforcement suites.

**Expected result:** `pass` with case-to-obligation matrix. **Handoff:** 010.

## SWU-MSB-010: Desktop And Mobile Browser Proof

**Goal:** Prove the actual workbench workflow and responsive evidence surface in
real Chromium at desktop and mobile viewports.

**Dependencies:** `SWU-MSB-009` pass.

**Exact write scope:** Playwright bridge spec, browser fixtures/assets, and
required `test:e2e` package configuration/scripts.

**Required flow:** prepare with required task -> approve -> inspect authorization
receipt -> ready -> fake claimant claims -> interrupt -> operator release/requeue
-> ready -> fake claimant posts result -> inspect execution receipt/evidence/history.

**Required checks:** singleton conflict; truthful status/action copy; live-region
updates; focus continuity; no pre-claim skill in agent response; no overlaps,
clipping, inaccessible controls, blank page, console errors, or broken evidence
links at representative desktop and mobile viewports.

**Done criteria:** Playwright flow passes on fresh temporary state; screenshots
show usable desktop/mobile states; dynamic controls do not resize the layout
incoherently; no production state is consumed.

**Acceptance evidence / validation:** `npm run test:e2e`, retained failure traces
when applicable, and reviewed screenshot paths.

**Expected result:** `pass` with browser artifact paths. **Handoff:** 011.

## SWU-MSB-011: Real Blind Manual Codex Witness

**Goal:** Demonstrate one human-selected private skill/task that the active Codex
session does not know until manual poll and successful claim, then return the
actual bounded result to the kernel.

**Dependencies:** `SWU-MSB-010` pass and a live loopback server/browser/session.

**Exact write scope:** fresh temporary runtime state and checked-in evidence report
plus review-safe screenshots/receipt references; no private skill payload in
public planning artifacts.

**Procedure:**

1. Start from fresh temporary state and record server/build identity.
2. Human privately chooses a read/preview-safe installed skill and concrete task,
   prepares, approves, verifies authorization receipt, and marks it ready.
3. Human says only `poll` to the active Codex session.
4. Session runs the one-shot ready/claim protocol, learns the skill only from the
   successful claim packet, invokes it within L0, and posts result or interruption.
5. Human verifies terminal state, authorization and execution receipts, skill
   hash, attempt/session bindings, result summary, validations, evidence refs,
   and history; redact private payload where publication boundaries require it.
6. Record observed failures honestly; do not substitute a simulated result.

**Failure/stop conditions:** skill was disclosed before claim; session knew the
private choice from the prompt; request needs writes/network; result exists only
in chat; receipt binding is missing; server/session unavailable. Return `block`
or `interrupted`, preserving partial evidence.

**Done criteria:** one real blind request reaches a kernel-admitted terminal result
with two truthful receipts and no out-of-scope effect. This proves the bounded L0
route only, not arbitrary skill safety or authenticated session control.

**Acceptance evidence / validation:** signed-off witness report, receipt/artifact
resolution review, history screenshot, and exact validation/result references.

**Expected result:** `pass`, `block`, or `interrupted` with no inflated claim.
**Handoff:** `TASK-VERIFY-READINESS` closure audit.

## Synchronization

- Never put the private task/skill or local secrets in public Arcanum surfaces.
- A manual witness failure is evidence and must remain visible; do not edit the
  acceptance bar after observing the result.
