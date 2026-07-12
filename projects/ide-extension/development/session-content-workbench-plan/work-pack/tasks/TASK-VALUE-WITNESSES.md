# Task Contract: Value Witnesses

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-VALUE-WITNESSES` |
| Objective | Prove the generic canvas with presentation, Decision Gate, and Craft surfaces, then run real Codex witnesses. |
| Layer / slice / wave | V0-C / S-004-S-005 / W3-W4 |
| Dependencies | `SWU-SCW-006` pass |

## SWU-SCW-007: Automated Three-Surface Matrix

**Goal:** Prove that one publish/event protocol supports three useful HTML forms.

**Exact write scope:** `tests/fixtures/canvas/*.html`, focused Node and
Playwright specs, e2e harness changes, screenshot assets, and package scripts.
No production behavior unless a test exposes an acceptance bug; route such a
bug back to its owning SWU instead of widening this unit.

**Witnesses:**

1. Presentation fixture: keyboard/buttons navigate and republished title/body
   appears automatically.
2. Decision fixture: selection emits `decision.selected` with decision id/value;
   CLI poll receives exact payload once by event id.
3. Craft fixture: action emits `craft.action.requested` with task/action fields;
   same poll route receives it without Craft-specific API code.

**Edge cases:** mobile layout, back-to-back interactions, stale revision action,
reload before poll, duplicate poll, interaction POST failure/retry.

**Done criteria:** desktop/mobile matrix passes; all three surfaces use the same
publish/current/content/event endpoints; source scan finds no specialized
decision/Craft server route.

**Validation:** dedicated Node and Playwright commands plus full bridge/e2e
regression.

**Handoff:** W3 closes; `SWU-SCW-008` becomes ready.

## SWU-SCW-008: Real Generated Presentation Witness

**Goal:** Ask the active Codex session to create a new standalone presentation,
publish it, and republish one visible revision while the workbench is open.

**Dependencies:** `SWU-SCW-007` pass and active Codex/human browser available.

**Exact write scope:** generated presentation inside an approved experiment
evidence folder plus this plan's `work-pack/evidence/SWU-SCW-008-*` report and
screenshots. No runtime source mutation.

**Procedure:** prepare/claim the presentation task; Codex writes complete HTML;
run CLI publish; observe automatic display; request one content change; republish;
confirm revision update; retain path/hash/CLI/browser evidence.

**Done criteria:** the generated project file appears without copy/paste and a
second complete revision updates automatically. Human records whether this is
more useful than chat-only output.

**Stop:** return `block` if no active session/browser exists; do not substitute a
fixture for real witness evidence.

**Handoff:** `SWU-SCW-009`.

## SWU-SCW-009: Real Decision And Craft Round Trip

**Goal:** Prove user interaction changes what the active Codex session does next.

**Dependencies:** `SWU-SCW-008` pass.

**Exact write scope:** HTML witness artifacts and
`work-pack/evidence/SWU-SCW-009-*` reports/assets plus plan status/evidence links
after validation. No runtime source mutation.

**Procedure:** Codex publishes a Decision Gate; human selects an option; Codex
polls and repeats the exact selected payload. Codex then publishes a Craft task
surface; human requests one action; Codex polls it and runs/declines/blocks the
Craft task through its normal skill authority. Preserve the interaction event
separately from any later task result.

**Done criteria:** both interactions arrive through the generic event endpoint;
the session demonstrably continues from the selected action; evidence never
equates request with completion; human records the value result and next-layer
recommendation.

**Validation:** event ids/cursors/payloads, browser screenshots, session output,
separate Craft result evidence, scoped closure audit.

**Stop:** unavailable live environment, mismatched payload, or simulated event.

## Synchronization

Only SWU-009 may close the V0 plan, and only from retained automated plus real
witness evidence.
