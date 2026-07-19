# Open Poll Bridge Findings

Dispatch: `2026-07-15-ide-extension-open-poll-bridge-research`

## Verdict

Use **open singleton availability, claim-bound identity**.

`GET /api/bridge/requests/ready` should be a caller-neutral loopback availability check. It should return zero or one safe ready handle and no private task/skill/context payload. Claimant identity belongs to `POST /api/bridge/requests/:handle/claim`, where the claimant supplies `agent_ref`, `session_ref`, and `assurance`. Result admission should keep using the stored claim/session/attempt bindings rather than trusting any new result-time identity field.

This is not a multi-request queue. The current singleton ready invariant is still the right L0 boundary.

## Evidence Basis

Runtime/API evidence:

- Current ready poll is Codex-gated at `projects/ide-extension/src/server.mjs:1251`.
- Ready targeting itself is generic: an approved bridge envelope moves to `ready_for_poll` in `projects/ide-extension/src/envelopes/manual-session-bridge.mjs:140`.
- Claim creation currently hard-codes Codex identity in `projects/ide-extension/src/envelopes/manual-session-bridge.mjs:204`.
- Projector replay currently rejects non-Codex claims in `projects/ide-extension/src/kernel/projector.mjs:442`.
- Result admission already binds to claim/session/attempt/envelope/run/approval/skill in `projects/ide-extension/src/server.mjs:1496`.
- Execution receipts already copy `agent_ref` from the stored claim in `projects/ide-extension/src/envelopes/manual-session-bridge.mjs:310`.

UX evidence:

- Current workbench copy uses `target`, `selected`, and `exact request` language before claim.
- That wording makes readiness sound like it binds a future session identity too early.
- Approval copy is mostly correct because it says authorization is not execution.
- The UI should say `poll availability`, `open`, and `closed` before claim; `claimed by unattested local session` should appear only after claim.

Adversarial evidence:

- Open polling is safe only as trusted-local, loopback, operator-primed, one-shot ready/claim/result.
- No background poller, retry daemon, visible multi-target queue, pre-claim skill preview, claimant operator actor, or session release/requeue belongs in this slice.
- `/api/state` is a debug/workbench surface with full projection state; session bridge clients must not treat it as a poll API.

Reviewer evidence:

- Precedent gate classified the broader bridge behavior as already deployed with wording/gate repair: existing decisions own manual poll, read/preview-only L0, operator-only recovery, unattested assurance, and singleton `ready_for_poll`.
- Non-vacuity gate rejected any claim that this is already proven for open availability. Existing tests prove the old Codex-bound singleton bridge; a new witness is required.
- Definitional gate passed conditionally: the model is distinct only if ready poll stops selecting by `agent_ref`, claim stores caller-supplied `agent_ref`, replay accepts that non-Codex identity, and receipt identity is copied from the stored claim.

## Recommended Model

Keep:

- one ready request at a time;
- pre-claim secrecy;
- one winning claimant;
- operator-only release/requeue;
- authorization receipt separate from execution receipt;
- trusted-local, unattested, no production auth claim.

Change:

- ready poll discovery is open and caller-neutral;
- claim identity is caller-supplied and stored immutably;
- result identity is derived from the stored claim;
- UI language distinguishes open availability from claimed execution.

## Implementation Surface

Backend:

- In `projects/ide-extension/src/server.mjs`, remove the hard failure when `GET /api/bridge/requests/ready` lacks `agent_ref=codex.current-session`.
- Treat any `agent_ref` query on ready as ignored compatibility metadata, not a selector.
- Keep singleton ready lookup and safe projection.

Bridge helper:

- In `projects/ide-extension/src/envelopes/manual-session-bridge.mjs`, set `claim.agent_ref = request.agent_ref`.
- Keep `assurance: unattested`.
- Do not add `agent_ref` to result requests.

Schemas:

- In `projects/ide-extension/schemas/bridge-claim-request.schema.json`, replace the Codex const with a bounded stable string pattern.
- In `projects/ide-extension/schemas/receipt.schema.json`, allow execution receipt `agent_ref` to be any valid stored claim agent ref.
- If bridge envelope `agent_ref` remains present, stop treating it as claimant identity; prefer a neutral availability value or leave it as legacy metadata with UI copy that does not imply a claimant.

Projector:

- In `projects/ide-extension/src/kernel/projector.mjs`, replace the Codex-only claim assertion with a bounded nonblank/pattern assertion.
- Keep `assertClaimIdentity` so `agent_ref`, `session_ref`, `assurance`, and attempt bindings cannot drift after claim.
- Keep singleton ready replay constraints.

CLI:

- In `projects/ide-extension/scripts/session-bridge.mjs`, make `ready` call `/api/bridge/requests/ready` without the Codex query.
- Add `--agent-ref` to `claim`, defaulting to `codex.current-session` for compatibility.
- Do not add approve, release, requeue, or `/api/state` commands to the bridge session client.

Workbench:

- In `projects/ide-extension/public/demo/l0.html`, rename pre-claim `target` / `selected` language to `availability` / `open` / `closed`.
- Keep `claimed by unattested local session` only for claimed state.
- Preserve authorization-vs-execution receipt separation.

## Required Witness

The implementation should not close as proven until this witness passes:

1. Start a fresh server.
2. Prepare two bridge envelopes.
3. Authorize both.
4. Mark the first ready.
5. `GET /api/bridge/requests/ready` with no query returns `200` and safe availability metadata only.
6. The ready response omits `task`, `requested_skill`, `context_refs`, approval detail, receipt hashes, and claimant identity.
7. Attempt to mark the second ready and receive `409 ready_target_exists`.
8. Claim with a non-Codex `agent_ref`, for example `openrouter.local-session`.
9. Race ten claims against the same handle: exactly one wins, and losers receive no execution packet.
10. Submit a valid result for the winning claim and verify the execution receipt preserves the stored non-Codex `agent_ref`.
11. Submit mismatched result attempts and verify `result_binding_mismatch` without mutation.
12. Restart and replay; completed projection preserves the non-Codex claim identity and receipts.
13. Verify interrupted recovery still requires operator release plus explicit reopen before another claim.
14. Verify the CLI cannot inspect `/api/state` or perform operator recovery.

## Tests To Update

- `projects/ide-extension/tests/manual-session-bridge-authorization.test.mjs`
- `projects/ide-extension/tests/manual-session-bridge-claim-recovery.test.mjs`
- `projects/ide-extension/tests/manual-session-bridge-result.test.mjs`
- `projects/ide-extension/tests/manual-session-bridge-contracts.test.mjs`
- `projects/ide-extension/tests/manual-session-bridge-replay.test.mjs`
- `projects/ide-extension/tests/manual-session-bridge-cli.test.mjs`
- `projects/ide-extension/tests/e2e/manual-session-bridge.spec.mjs`
- schema fixtures for claim and receipt agent refs

## Rejected Paths

- Multi-request visible queue in L0.
- Background polling, auto-claim, or retry daemon.
- Pre-claim skill/task preview.
- Claimant-provided operator actor.
- Session-side release/requeue.
- Result-time `agent_ref` as a trusted input.
- Production authentication or remote multi-agent safety claims.

## Closeout Claim

The next implementation package should claim only this:

> A trusted-local loopback client can discover one operator-open bridge request without identifying as Codex, claim it with its own unattested session identity, receive the private execution packet only after winning the claim, and return a result whose receipt is bound to that stored claim identity.
