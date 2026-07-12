# Task Contract: One-Shot Session Protocol

## Task Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-SESSION-PROTOCOL` |
| Objective | Give the active Codex session a small explicit protocol for one manual poll, claim, result, or interruption. |
| Layer / slice / wave | L0 / S-003 / W2 |
| Dependencies | `SWU-MSB-005`. |
| Execution owner | Task Session (`local-fallback`). |

## Source Handles And Boundary

- [Approved UX](../../../manual-session-bridge-design/UX-PLAN.md)
- [Kernel task](TASK-BRIDGE-KERNEL.md)
- Existing package/script conventions in `projects/ide-extension/package.json`
  and `scripts/`.
- This is a one-shot HTTP client/protocol, not an agent executor, skill resolver,
  timer, worker, background poller, browser controller, or authenticated channel.

## SWU-MSB-006: Session Bridge CLI

**Goal:** Implement deterministic `ready`, `claim`, `result`, and `interrupt`
commands that an active session can call only after the human says `poll`.

**Dependencies:** `SWU-MSB-005` pass.

**Exact write scope:** `scripts/session-bridge.mjs`, a bridge protocol document,
`package.json` script entries, and focused child-process/API contract tests.

**Implementation rules:**

1. `ready` returns only the claimable singleton handle and non-secret metadata;
   zero or ambiguous targets exit nonzero without private fields.
2. `claim --session-ref ...` performs one claim and emits the claim packet as
   machine-readable JSON to stdout only on success.
3. `result` reads a bounded JSON request, submits it once, and prints the admitted
   terminal projection/receipt handle; it never invents validation or evidence.
4. `interrupt` records one bounded reason for the bound active attempt.
5. Base URL comes from an explicit argument or documented environment variable
   and defaults only to loopback. Never accept remote hosts in L0.
6. Diagnostics go to stderr; secrets/private packet content are not logged.
7. The CLI has no commands for approve, ready-target selection, unready,
   release, requeue, or receipt minting.
8. Document the human/session sequence and fail-closed exit codes.

**Edge cases and failure modes:** server unavailable; malformed JSON; non-loopback
URL; zero/multiple ready; claim conflict; stale attempt; result rejected;
connection loss; interrupt after terminal; accidental stdout diagnostics.

**Done criteria:** child-process tests prove stdout/stderr/exit-code contracts;
the CLI cannot perform operator actions; one-shot calls interoperate with the
real kernel harness; no daemon remains after invocation.

**Acceptance evidence / validation:** focused CLI tests against a temporary
server plus package-script smoke checks.

**Expected result:** `pass` with command examples and test output, or `block`
naming the kernel contract mismatch. **Handoff:** join with `SWU-MSB-007`, then
route `SWU-MSB-008`.

## Synchronization

- Do not change kernel semantics from this task. Return any mismatch to the
  owning kernel SWU as residue.
- Do not run a real private skill during this SWU; that witness belongs to 011.
