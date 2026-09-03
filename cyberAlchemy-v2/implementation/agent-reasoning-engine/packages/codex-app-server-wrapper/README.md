# Codex app-server wrapper candidate

This package implements the selected `ARE-CODEX-OPEN-002` boundary against the
version-bound Codex app-server JSON-RPC protocol. It is a client-owned stdio
proxy around `codex app-server`.

## Reusable reasoning state

Every forwarded `turn/start` passes through an explicit reasoning-state
boundary. The wrapper appends the request interpretation and selected Context
Envelope as immutable reasoning events, seals their exact event digests into a
Reasoning State epoch, materializes the complete canonical JSON-RPC request and
request-series header, reconstructs and verifies those bytes, and checkpoints
the epoch before forwarding.

Accepted effects and automatic continuations have independent required
checkpoints. A sink append, verification, or flush failure blocks that boundary.
The repository profile defaults to explicit process-memory operation. Supplying
`--reasoning-state-log <path>` to `are-codex-app-server` uses the append-only
file sink and `fsync` barriers. Before accepting a client message, the wrapper
verifies the complete existing log, selects its final valid checkpoint,
rebuilds disposable indexes, and resumes the event chain. Empty paths create a
new explicitly identified ledger. Torn, malformed, tampered, mixed-ledger, or
uncheckpointed logs fail startup; existing bytes are never rewritten or
silently truncated. Recovery metadata is recorded without copying event
contents into the diagnostic journal.

At `turn/completed`, the wrapper seals the exact semantic result, continuation
result, completion identity, and relevant context identities into a Reasoning
State Frontier before any automatic successor is forwarded. A recovered
frontier replays the prior client-visible decision with zero semantic provider,
evaluator, continuation-provider, effect, or successor calls. Reusing the same
turn identity with different completion bytes blocks. Automatic continuation is
therefore at-most-once across recovery: a crash after the completion checkpoint
but before forwarding is not silently retried, and delivery reconciliation
remains explicit residue.

The ledger contains explicit system reasoning products, not hidden model
chain-of-thought. Its epochs, dispatch records, and checkpoints have
`authority_effect: none` and do not authorize effects or continuations.
Recovery is currently single-process. Cross-process writer coordination and
operator-directed log repair remain separate capabilities.

It also provides a persistent local gateway. The gateway listens on a
permission-restricted Unix socket, creates one isolated ARE wrapper and
upstream app-server connection per declared consumer, and preserves that
consumer's in-memory Context Views, turn state, and runtime journal across
transport reconnects. A second live attachment for the same consumer, lane
substitution, unknown consumers, oversized messages, and detached-buffer
overflow fail closed.

The currently bound `0.153.0-alpha.5` server accepts JSON-RPC 2.0 client messages but
omits the `jsonrpc` member on its own responses and notifications. The wrapper
admits both exact framings while rejecting any explicit non-2.0 version.
Because the wrapper projects the envelope through `turn/start.additionalContext`,
the connected client must declare `capabilities.experimentalApi: true` in its
`initialize` request. Codex rejects the field when that capability was not
negotiated.

For every `turn/start`, it reloads and structurally verifies the configured live
context sources, constructs an ARE Context Basis, assesses selected-dependency
freshness, and projects an immutable inline Context Envelope before forwarding
the request. A client may supply an exact `are.request-context-hint/v1` so the
human utterance and explicit capability objective remain distinct; malformed
hints block. Deterministic request-term selection adds matching canonical
definitions, ontology nodes and bounded related edges to a minimal baseline.
The repository profile also binds root `AGENTS.md` as an exact
`repository-instruction` item and projects the read-only ontology registry as a
compact `ontology-catalog` item only for matching requests. Direct requests
therefore receive the bounded meanings of selected definitions, instructions,
catalog records, and selector-locked ontology records through the
protocol-supported `params.additionalContext` field, not only their digests.
The carrier uses one compact envelope manifest plus one stable, source-keyed
fragment per selected Context Item. This keeps provenance and envelope identity
visible without burying useful meanings inside one large opaque JSON value.
The default inline budget is 32 KiB. Optional diagnostics are excluded first
and recorded; mandatory overflow blocks without truncation or model-generated
summarization. Gates and blocks are not forwarded.

Plan-bound consumers reuse an envelope identity only after a real currentness
comparison produces a reuse receipt. Interaction-bound consumers always
receive successor view and envelope identities. Selected dependency drift
requires a successor; unrelated source drift remains diagnostic. Diagnostic
state records envelope identity and refresh events without copying full context
contents.

During a turn, command, file-change, and permission approval callbacks are
evaluated before the client response can reach Codex. A direct engine decision
still requires the independent client approval. A gate is forwarded to the
client as the exact human decision boundary. A block is denied locally.

After `turn/completed`, the wrapper joins observed lifecycle evidence with both
continuation lanes. Interaction-bound proposals always gate. Exactly one safe,
reversible plan-bound proposal may start one successor turn, but only after
that successor passes its own preflight.

Semantic evaluation at `turn/completed` is generic and explicitly opt-in. The
repository profile defaults to `{enabled: false}`, which produces no semantic
notification, provider call, evaluator call, or semantic ledger event. An
enabled profile must exact-bind a verified semantic-input profile. The wrapper
then binds the preflight request, route decision, and Context Envelope to the
actual Codex turn identity and asks an explicit input provider for observation,
owner, temporal, challenge, and journal inputs. It never derives those facts
from Codex output or Context Items.

Matching domains invoke the context-bound semantic lifecycle once and emit a
compact `cyberalchemy/semantic` notification containing only disposition,
materialization identity, outcome, and Reasoning Receipt digest. Non-matching
domains are `not-applicable` without calling the input provider or evaluator.
Duplicate completion notifications verify and replay the immutable recorded
result instead of repeating semantic calls.

A plan-bound proposal may explicitly declare `semantic_dependency` with
`required: true` and optional exact `binding_id` or `conclusion_domain`
selectors. For those proposals only, the wrapper recomputes the Reasoning
Receipt digest and verifies its exact turn, Context Envelope, materialization,
domain, and terminal-outcome binding before consequence assessment. Invalid,
unauthorized, defeated, insufficient, or invalidated outcomes make that
proposal ineligible. `EscalateOwner` requires a human gate.
`RecommendedUnderSnapshot` is advisory only: it can never make a structurally
invalid, consequential, protected, unknown, or irreversible proposal direct.
`OutOfDomain`, disabled evaluation, and non-matching domains preserve the
ordinary continuation result. Independent proposals are never constrained by
another proposal's semantic dependency.

Blocked semantic input remains visible and cannot suppress the original Codex
completion or authorize an effect. It constrains continuation only when a plan
proposal explicitly declares the semantic dependency. Constraint records and
ledger events contain identities, digests, outcomes, and reason codes, never
the Reasoning Receipt or context contents.

The wrapper owns a bounded in-memory runtime journal. Events are canonical,
immutable, hash chained, and idempotency-keyed. Before semantic materialization
it cuts the exact current thread and turn; the semantic input runtime verifies
that cut and binds its digest into the Reasoning Receipt metadata. Duplicate
completion uses deterministic external-call-free replay and cannot call the
provider or evaluator or start a second successor. Configured retention evicts
only closed turns and records an eviction receipt; active-turn events are never
evicted to satisfy a bound. This is not durable or cross-session storage.

Run with a repository-bound profile:

```sh
node bin/are-codex-app-server.mjs \
  --config profiles/repository-v1.json \
  --repository-root /absolute/path/to/domainspec-core
```

Run the persistent gateway against an already-running, exact-version managed
app-server daemon:

```sh
node bin/are-codex-gateway.mjs \
  --config profiles/repository-v1.json \
  --repository-root /absolute/path/to/domainspec-core \
  --listen /tmp/are-codex-gateway.sock \
  --backend daemon-proxy
```

The gateway does not install or start the managed daemon. It checks both the
local CLI binding and the running daemon version before listening. For an
isolated app-server process it can instead use `--backend websocket` with an
explicit loopback `--upstream-url`.

An app-server protocol client launches the lane-specific stdio adapter:

```sh
node bin/are-codex-client-proxy.mjs \
  --socket /tmp/are-codex-gateway.sock \
  --consumer codex:human-chat \
  --lane interaction-bound
```

`codex:plan` is separately configured as `plan-bound` with a stable request and
window identity. Exact reconnect resumes the same gateway session; process
restart creates a new runtime epoch. No journal or context state is durable.

Programmatic consumers use `connectGatewayRpcTransport` with
`createAppServerRpcClient`. The shared client owns JSON-line parsing, request
correlation, bounded notification waits, streamed agent-text collection, and
default approval refusal. `spawnAppServerRpcTransport` provides an explicit
strict direct-process transport for diagnostics and tests; it does not bypass
the wrapper's version gate.

Run the controlled version-bound semantic continuation matrix with:

```sh
npm run canary:semantic
```

It exercises recommendation, insufficient evidence, owner escalation,
tampering, disabled evaluation, and interaction precedence against a real
`codex app-server` while requesting no tools, network access, or effects. The
matrix reuses one app-server and one ephemeral thread so startup/index loading
is measured once while each scenario retains its own turn, semantic posture,
continuation decision, and receipt evidence. Each RPC request and completion
wait is bounded, redacted progress is emitted on stderr, and an infrastructure
timeout stops the remaining matrix. Override the defaults with
`ARE_CANARY_REQUEST_TIMEOUT_MS` and `ARE_CANARY_EVENT_TIMEOUT_MS` when the
local state index has known startup latency.

Run the isolated persistent transport canary with `npm run canary:gateway`.
It exercises two exact plan-bound turns across a disconnect/reconnect and two
interaction-bound turns through a real long-lived loopback WebSocket
app-server. The official daemon-proxy command surface is covered separately;
the canary intentionally does not mutate the user-global managed daemon.

The repository default adopts no production semantic-domain catalog. The
wrapper is a candidate implementation. It does not modify Codex desktop
configuration, grant effect authority, treat a recommendation as permission,
adopt a capability, establish conformance, publish, deploy, or start any
successor that is gated or blocked.
