# Agent Reasoning Engine

The Agent Reasoning Engine is the private CyberAlchemy-v2 capability for both
governed reasoning and context management.

## Product thesis

> **The Agent Reasoning Engine makes CyberAlchemy better at solving problems
> over time. It remembers the reasoning state behind previous work, measures
> results with benchmarks, finds useful new research and technology, tests
> improvements, and upgrades the engine when they perform better.**

ARE is an engine because it runs two connected feedback loops:

```text
work loop
request -> context -> reasoning -> action -> result -> reusable state

improvement loop
results -> problems -> research -> new technique -> implementation
        -> benchmark -> upgrade -> new results
```

The work loop handles the current request. It finds the necessary context,
reuses the reasoning state that produced that context, reasons from the current
evidence, records the result, and leaves a useful state for the next turn.

The improvement loop makes the engine itself better. It detects weaknesses in
benchmarks and real use, searches papers, repositories, tools, and agent
techniques, reproduces promising ideas, integrates them into a new engine
version, and compares that version with the current one. An upgrade must improve
the target result without making speed, quality, reliability, or safety worse.

This creates three clear parts:

```text
serving engine
  handles current requests quickly and uses one stable engine version

evolution engine
  researches, builds, and benchmarks better engine versions

upgrade controller
  replaces the serving version when a new version performs better
```

The product is therefore more than a router, context manager, or agent
framework. ARE reasons about the user's work, measures how well its reasoning
works, discovers better ways to operate, and improves through measured software
evolution.

Its central context principle remains:

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

## Research and evolution pipeline

The improvement loop follows one concrete pipeline:

1. Collect benchmark failures, slow paths, user corrections, unresolved gaps,
   and recovery failures.
2. Turn each recurring weakness into a measurable improvement target.
3. Search for papers, repositories, releases, tools, and techniques related to
   that target.
4. Record the exact source, version, mechanism, evidence, and limitations of
   each promising technique.
5. Reproduce the technique and determine where it fits in ARE.
6. Build one or more new engine versions.
7. Compare them with the current engine using fixed development, regression,
   holdout, performance, and failure tests.
8. Keep useful versions, discard regressions, and preserve the evidence from
   both.
9. Upgrade the serving engine when a version performs better.
10. Monitor the upgrade, roll it back when declared failures appear, and feed
    the new results into the next improvement cycle.

The evolution runtime now implements the complete bounded mechanism chain:
diagnosis signals, deterministic target selection, provider-neutral research,
technique and reproduction records, content-addressed isolated variant
workspaces, exact benchmark comparisons, recommend-only upgrade decisions,
atomic controlled-local serving selection, canary rollback, and one-cycle-at-a-
time scheduling. The real-reasoning benchmark includes a deterministic full
cycle canary. The mechanisms do not invent research sources or code changes:
production providers, reproduction protocols, mutation runners, schedules, and
activation remain explicit configuration.

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

The completed-turn frontier vertical now seals the explicit semantic result,
continuation result, completion identity, and context bindings into the same
recoverable Reasoning State source before automatic continuation. After a
restart, the wrapper can replay that exact decision without rediscovering it or
starting a second successor. Delivery acknowledgement remains a separate gap,
so recovery uses an explicit at-most-once posture rather than guessing.

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
context-bound Problem Frame, verifies exact agreement among that frame, its
entry gate, authority snapshot, Context Envelope binding, selected Context Item
digests, freshness, and claim ceiling, then evaluates under the existing finite
catalog. Context-bound receipts preserve the context epoch, envelope, binding,
and selected-item identities; historical unbound receipt bytes remain unchanged.

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

The wrapper can also emit immutable Improvement Signals at `turn/completed`.
This path is separately opt-in and requires both an explicit signal provider
and sink. Disabled mode makes zero calls. Completion-frontier replay prevents a
duplicate completion from emitting the same signal twice, and the diagnostic
journal stores only signal identities and counts rather than turn contents.

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
