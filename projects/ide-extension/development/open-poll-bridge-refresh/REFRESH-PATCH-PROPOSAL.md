# Refresh Patch Proposal: Open Poll Bridge

Mutation mode: `proposal-only`

This proposal should be applied through a successor `invoke plan`, not by
directly editing the completed manual-session-bridge plan.

## Proposed Successor Package

Create:

```text
projects/ide-extension/development/open-poll-bridge-plan/
```

Purpose:

```text
Convert the existing Codex-bound singleton bridge into open singleton
availability with claim-bound identity, while preserving L0 loopback,
pre-claim secrecy, singleton ready, operator-only recovery, and separate
authorization/execution receipts.
```

## Proposed Work Items

### OPB-001: Contract And Schema Identity Split

Targets:

- `schemas/bridge-claim-request.schema.json`
- `schemas/receipt.schema.json`
- claim/receipt schema fixtures

Required deltas:

- Replace Codex-only claim `agent_ref` with a bounded stable string.
- Preserve `assurance: unattested`.
- Keep result requests free of `agent_ref`.
- Ensure execution receipts accept the stored claim `agent_ref`.

Acceptance:

- Schema fixtures accept `openrouter.local-session`.
- Empty, malformed, or unstable `agent_ref` values fail.

### OPB-002: Projector And Bridge Helper Replay

Targets:

- `src/envelopes/manual-session-bridge.mjs`
- `src/kernel/projector.mjs`
- bridge replay tests

Required deltas:

- Set `claim.agent_ref = request.agent_ref`.
- Replace Codex-only projector assertion with bounded identity validation.
- Keep `assertClaimIdentity` immutable across interrupt, release, result, and replay.
- Preserve singleton ready target.

Acceptance:

- Non-Codex claim replays successfully.
- Replay rejects claim identity drift.
- Singleton ready replay still rejects two ready targets.

### OPB-003: Caller-Neutral Ready And Claim API

Targets:

- `src/server.mjs`
- authorization/claim/result tests

Required deltas:

- `GET /api/bridge/requests/ready` succeeds without query params.
- Any `agent_ref` query is ignored as compatibility metadata, not used to filter.
- Ready response remains safe: no task, skill, context refs, approval detail,
  receipt hashes, or claimant identity.
- Claim with a non-Codex `agent_ref` succeeds once and discloses execution
  packet only to the winner.

Acceptance:

- Ready no-query returns the same handle-only availability as legacy query.
- Ten-way claim race has one winner and loser payload secrecy.
- Wrong result binding still fails without mutation.

### OPB-004: Session CLI Compatibility

Targets:

- `scripts/session-bridge.mjs`
- `SESSION-BRIDGE-PROTOCOL.md`
- CLI tests

Required deltas:

- `ready` calls `/api/bridge/requests/ready` without the Codex query.
- `claim` accepts `--agent-ref`, defaulting to `codex.current-session`.
- CLI does not add approve, release, requeue, ready-target mutation, or
  `/api/state` inspection.

Acceptance:

- Non-Codex claim works through CLI.
- Unknown operator/state commands remain rejected.

### OPB-005: Workbench Language Repair

Targets:

- `public/demo/l0.html`
- workbench UI tests
- Playwright bridge spec

Required deltas:

- Pre-claim states say `poll availability`, `open`, and `closed`.
- Remove pre-claim implication that the ready request is selected for a specific
  claimant.
- Keep `claimed by unattested local session` only after claim.
- Preserve authorization-vs-execution receipt distinction.

Acceptance:

- Browser copy contains no pre-claim `target`, `selected`, or claimant language
  for open availability states.
- Responsive layout remains stable.

### OPB-006: Required Witness

Targets:

- focused Node bridge tests
- e2e bridge test
- task-session evidence report

Required witness:

1. Fresh server.
2. Two bridge envelopes prepared and authorized.
3. First opened for poll.
4. No-query ready poll returns safe metadata only.
5. Second ready attempt fails with `ready_target_exists`.
6. Non-Codex claim wins.
7. Ten-way claim race has one winner and no loser disclosure.
8. Valid result admits execution receipt preserving stored non-Codex `agent_ref`.
9. Binding mismatches reject without mutation.
10. Restart replay preserves claim identity and receipts.
11. Interrupted recovery still requires operator release and explicit reopen.
12. CLI cannot inspect `/api/state` or perform operator recovery.

## Non-Goals

- Multi-request visible queue.
- Background polling, daemon, auto-claim, or retry loop.
- Pre-claim skill/task preview.
- Authenticated production identity.
- Session-side release/requeue.
- Runtime mutation in refresh mode.

## Recommended Next Command

```text
[$invoke] plan open-poll-bridge from projects/ide-extension/development/open-poll-bridge-refresh/REFRESH-REPORT.md
```
