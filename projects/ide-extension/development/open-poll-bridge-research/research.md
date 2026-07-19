# Open Poll Bridge Research

Dispatch: `2026-07-15-ide-extension-open-poll-bridge-research`

## Explorer 1: Abramsky, Samson — Runtime Contract

Ready poll is Codex-gated at the API edge: `server.mjs` rejects `GET /api/bridge/requests/ready` unless `agent_ref=codex.current-session`.

The ready target itself is not inherently Codex-specific: selection moves an approved bridge envelope to `ready_for_poll`, and server projection returns a sanitized ready packet.

Codex identity is hard-coded at preparation and claim creation: bridge envelopes get `agent_ref: 'codex.current-session'`, and claims overwrite request identity with the same value.

Schemas also encode Codex as the only claimant: `bridge-claim-request.schema.json`, `agent-envelope.schema.json`, and `receipt.schema.json`.

Replay/projector has another hard gate: `assertClaimRecord` requires `claim.agent_ref === 'codex.current-session'`. This must change with the schema or event replay will reject non-Codex claims.

Result binding is already mostly right for claim-time identity: result admission binds to `claim_attempt_id`, `envelope_id`, `run_id`, `approval_id`, `session_ref`, `assurance`, and skill. The execution receipt copies `agent_ref` from the stored claim.

Proposed changes:

- Make `GET /api/bridge/requests/ready` open availability: remove the required `agent_ref` query check, or accept it as optional compatibility metadata and do not filter on it.
- Change `bridge-claim-request.agent_ref` from const Codex to a bounded nonblank/patterned string, then set `claim.agent_ref = request.agent_ref` in `claimBridgeEnvelope`.
- Keep result requests free of `agent_ref`; preserve result identity through the stored claim. The receipt should continue to carry `claim.agent_ref`.
- Adjust bridge envelope meaning: either replace the hard-coded envelope `agent_ref` with a neutral availability value such as `bridge.open-availability`, or add a clearer `availability_ref`/`claim_policy` while treating claim `agent_ref` as the executor identity.
- Update projector validation to require stable/nonblank claim `agent_ref`, not Codex specifically, while preserving immutability via `assertClaimIdentity`.

Regression risks:

- Schema/projector drift is the big one: opening schemas without changing projector replay will break reconciliation.
- Identity confusion: if envelope `agent_ref` remains Codex while non-Codex claims are allowed, UI/API consumers may misread the target as Codex-owned rather than open.
- Existing CLI remains Codex-biased: it polls with Codex query and claims with Codex identity.
- Result security depends on claim binding. If `agent_ref` is added to result requests later, it must be checked against claim, not trusted independently.

Tests to update:

- `manual-session-bridge-authorization.test.mjs`: ready poll should work without `agent_ref`; add optional legacy query test.
- `manual-session-bridge-claim-recovery.test.mjs`: claim with a non-Codex `agent_ref`, verify only one claimant wins and losers still get no execution packet.
- `manual-session-bridge-result.test.mjs`: result from non-Codex claim should produce receipt with that claim's `agent_ref`; mismatched `session_ref`/attempt still rejected.
- `manual-session-bridge-contracts.test.mjs` and schema fixtures: allow non-Codex claim/receipt agent refs and keep invalid empty/malformed refs.
- `manual-session-bridge-replay.test.mjs`: replay non-Codex claim and result to prove projector accepts and preserves identity.
- `manual-session-bridge-cli.test.mjs`: either keep Codex defaults as compatibility, or add `--agent-ref` for open clients.
- E2E bridge spec: change ready poll URL away from `?agent_ref=codex.current-session` and include one non-Codex claim path.

## Explorer 2: Baez, John — Product / UX

Current human model is: approve authorizes only, ready selects one singleton poll target, `poll` reveals only an opaque handle, `claim` establishes unattested session identity and reveals task/skill/grants.

If "ready poll" becomes open availability, the dangerous copy is all "target/selected/exact request" language. It makes the human think readiness binds a specific future session before claim.

Change:

- `Ready target: ...` / `No request is ready for poll` to `Poll availability: open for <id>` / `No request is open for polling`.
- `Approved - select as poll target` to `Authorized - open for poll when ready`.
- `Ready for poll` button/status to `Open poll availability`; `Unready` to `Close poll availability`.
- Action note `Select this exact request as the singleton poll target` to language that says authorization is done, availability is open, ownership/identity happens only after claim.
- `Poll target: Selected/Not selected` to `Poll availability: Open/Closed`; keep `Session ref`, `Claim ID`, and `Session assurance` as `None` / `Not claimed` until claim.

User-facing risks:

- `Ready target` implies routing identity too early.
- `Claimed by unattested local session` is honest post-claim, but should never appear or be implied before claim.
- Approval copy is mostly good because it says no execution happens. Keep that.
- Receipt separation must remain explicit: authorization is not execution.

Controls to change:

- Rename ready/unready controls, announces, and release text.
- Keep `Release and requeue` operator-only; this is still correct.
- If open availability allows multiple available requests, kernel/test contracts must change; current oracle explicitly enforces singleton target and duplicate-ready rejection.

Acceptance checks:

- Browser copy contains no pre-claim `target`, `selected`, or `claimed by session` language for approved/open states.
- Pre-claim poll still omits task/skill; claim reveals them.
- Duplicate claim still has one winner and losers learn nothing.
- Authorization receipt and execution receipt remain separate in UI and evidence.
- Product rule is made explicit: either `open availability but still singleton` or `multiple available requests, claim arbitrates`. The current code is the first; the requested phrase sounds like the second.

## Explorer 3: Capucci, Matteo — Adversarial

Attack result: the current bridge model is close to the L0 invariant set, but only if `open poll` means a loopback, operator-primed, one-shot ready/claim/result protocol. If it drifts into background polling, multi-target queues, or any helpful payload preview before claim, it breaks the core boundary.

Failure modes:

- Payload leakage through alternate read paths: `GET /api/bridge/requests/ready` hides task/skill/context and returns only a handle, but `GET /api/state` exposes full projection state. That is acceptable for local workbench/debug only if the session bridge client never treats `/api/state` as poll surface.
- Singleton ready erosion: projector rejects a second ready target at replay time, and server rejects it live. Any `open poll queue` would be a no unless it keeps exactly one active ready target.
- Loser disclosure: claim response is the first place execution packet appears; losers must receive only conflict/error.
- Recovery privilege confusion: release is operator-shaped in the projector and route emits its own local operator actor. The risk is adding session-side release/requeue to the CLI.
- Execution-before-result inflation: authorization receipt is deliberately not execution; skill execution receipt is minted only in result admission.
- Production-security overclaim: CLI only accepts loopback HTTP origins; protocol says no auth, retry, background poll, or operator actions. Do not market this as authenticated production multi-agent dispatch.

Required negative tests:

- Assert `/api/bridge/requests/ready` never includes `task`, `requested_skill`, `context_refs`, receipt hashes, or approval detail.
- Concurrent ready selection: two approved bridge envelopes, one ready succeeds, all others fail, restart preserves singleton.
- Concurrent claim: exactly one winner, losers contain no execution packet.
- Claim append failure: no payload in failed response, ready target remains, orphan artifact is reported.
- Result before active claim, duplicate result, post-release result, mismatched `session_ref`, `claim_attempt_id`, `requested_skill`, and invalid evidence all fail without mutation.
- Missing test to add: CLI must not expose `release`, `approve`, `ready-target`, or `/api/state` access under bridge session commands.

No-go changes:

- No background poller, retry loop, or daemon.
- No queue of visible ready requests.
- No pre-claim payload, even `just skill name`.
- No claimant-provided operator actor.
- No session-side release/requeue.
- No `failed` result admission unless the result lifecycle is deliberately redesigned.
- No production security/authentication claim beyond trusted-local loopback.

Minimal witness:

A satisfying witness is one end-to-end test bundle that starts a fresh server, prepares two bridge envelopes, authorizes both, marks one ready, proves ready output is handle-only, races 10 claims, proves exactly one execution packet is disclosed, submits one valid result, proves authorization and execution receipts exist, restarts, proves projection replay preserves completed state, then verifies interrupted recovery requires operator release plus explicit retarget before retry. That witness is mostly present across the current bridge tests; add the CLI/operator-surface negative before blessing an `open poll` model as L0-safe.
