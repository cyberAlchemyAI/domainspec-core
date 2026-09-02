# Agent Reasoning Engine

The Agent Reasoning Engine is the private CyberAlchemy-v2 capability for both
governed reasoning and context management.

## Product thesis

> **Do not merely reuse context. Reuse the explicit reasoning state that
> produced that context.**

Agent systems commonly preserve a transcript, a prompt, or a provider cache but
discard the causal and evidential structure used to assemble it. The next turn
must rediscover why definitions and ontology records were selected, which
sources were current, what was excluded, which contradictions or gaps remained,
and which continuation was still eligible. Identical prompt bytes can conceal a
different reasoning basis; different prompt bytes can contain a still-current
reasoning basis.

ARE makes that explicit reasoning basis a reusable system asset. It records and
seals provenance-bearing reasoning-state epochs, validates only their selected
dependencies, projects bounded Context Envelopes for consumers, binds explicit
semantic and continuation results, and creates successors only when relevant
state changes. This is not storage or exposure of hidden model chain-of-thought.
It is reuse of inspectable system records: request interpretation, route,
definitions, ontology selections, evidence posture, exclusions,
contradictions, gaps, transformations, freshness, admitted observations,
receipts, decisions, and the continuation frontier.

The product promise is that a person or agent can resume complex work from an
exact, reviewable reasoning frontier instead of reconstructing the work from a
conversation. Reuse preserves provenance, temporal scope, residue, claim
ceiling, and authority posture; it never upgrades them.

```text
request
  -> acquire or create reasoning-state epoch
  -> validate selected dependencies
  -> append changed evidence, judgments, and residue
  -> project consumer-specific Context Envelope
  -> reconstruct and dispatch the interaction
  -> bind explicit result and continuation records
  -> seal reusable successor frontier
```

The Context Envelope is therefore a projection of reasoning state, not the
primary durable asset. A model-provider cache is an optimization over exact
request bytes, not evidence that the underlying reasoning state is current.

The first three mechanisms are now bounded candidate implementations in
`implementation/agent-reasoning-engine/packages/reasoning-state-runtime` and
the Codex app-server wrapper: an append-only Reasoning State Ledger, required
risk-aligned checkpoints, and exact outbound request reconstruction. The
repository default is process-memory; an explicit file-log option provides
append-only JSONL plus `fsync`. The successor recovery vertical now verifies a
complete log, rebuilds disposable indexes, selects its final checkpoint, and
continues the exact event chain before Codex accepts a new turn. Cross-process
writer coordination, repair, reduction, and durable CyberAlchemy Session
semantics remain open, so this is not yet the complete product promise.

Its first-class candidate construction package is
[`ontology/`](ontology/README.md). That package separates:

- product meaning and business rules;
- DomainSpec-v2-authored system structure;
- deterministic graph and system-ontology projections;
- evidence-backed links to bounded partial implementations, including the
  request-decision router, Context Basis lifecycle, production-shaped semantic
  input materialization, receipt-constrained continuation, bounded runtime
  journal replay, and a persistent Codex app-server gateway candidate;
- explicit gaps for production semantic activation and catalog adoption,
  general host adoption,
  durable cross-session context, whole-engine integration,
  implementation binding, conformance, and runtime evidence.

The engine manages what a bounded reasoning run may reason over, preserves why
that context was selected, derives a typed semantic result under frozen inputs,
and records when changed context invalidates reuse. It does not grant authority,
approve an effect, or replace CyberAlchemy-v2 routing and governance owners.

## Current posture

This is a private candidate capability. The semantic-judgment evaluator,
intent-route resolver, request-decision router, Context Basis lifecycle, and
Codex app-server wrapper are bounded local realizations. The context lifecycle
preserves usable selected meanings, creates immutable budgeted envelopes,
distinguishes selected-dependency invalidation from unrelated diagnostic drift,
and refreshes live sources before each wrapped Codex turn. It keeps plan-bound
reuse and interaction-bound succession distinct.

The semantic evaluator now has a bounded additive integration with the frozen
Context Envelope. It verifies the envelope and Context Items, derives a sealed
context-bound Problem Frame, evaluates under the existing finite catalog, and
binds the context epoch and selected dependencies into the Reasoning Receipt.

The separate semantic-input runtime now selects exactly one configured semantic
domain, reloads exact-bound authority, catalog, and validator providers, admits
only source-and-validator-bound observations, freezes challenge and journal
state, and emits a sealed evaluator request. Missing domains are explicitly
not applicable; ambiguity, stale providers, missing ownership, malformed
sources, and structural ineligibility block before evaluator execution.

The Codex wrapper can now invoke that lifecycle at `turn/completed`, but only
through an exact opt-in semantic profile and explicit input provider. It binds
preflight context to the actual turn identity, emits compact outcome and receipt
metadata, and evaluates once per immutable turn. The repository default is
disabled and therefore performs no semantic provider or evaluator calls.

For plan-bound proposals that explicitly declare a semantic dependency, the
wrapper verifies the exact Reasoning Receipt, turn, Context Envelope,
materialization, domain, and terminal-outcome binding before deriving a
non-authorizing constraint. A recommendation remains advisory and cannot
override consequence, protected-effect, reversibility, or human-interaction
gates. Duplicate completions replay one verified immutable journal cut without
calling providers or evaluators or starting a second successor.

The separate completion journal is bounded in-memory state with hash-chained compact events,
immutable cuts, deterministic replay, idempotency, and closed-turn-only
eviction. The Reasoning State Ledger can now recover its own checkpointed file,
but that does not make the completion journal durable. No production
semantic-domain catalog or default activation is adopted, and there is no
cross-process or cross-session journal. The complete engine is not admitted,
published, or deployed.

The persistent gateway now separates transport from the reasoning wrapper. It
supports direct stdio, the official managed-daemon proxy, and an isolated
loopback WebSocket app-server backend. Declared plan and human/chat consumers
receive separate wrapper instances and upstream connections; reconnect retains
only the same in-memory consumer session, while lane substitution and concurrent
attachment fail closed. The repository does not install or start a managed
daemon and does not modify Codex Desktop configuration.

Historical specifications, decisions, promotion receipts, and implementation
evidence keep their original claim ceilings. The new ontology does not rewrite
or widen them.
