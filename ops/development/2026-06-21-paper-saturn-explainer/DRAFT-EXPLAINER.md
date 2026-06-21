---
node_type: explainer
title: CyberAlchemy — what it is, and what is built
status: draft
created: 2026-06-21
audience: public
voice: victor
---

# CyberAlchemy — what it is, and what is built

Give the same specification to an LLM agent twice. You get two different test suites, two different implementations, two different ideas of "done." The agent is fast. It is not reproducible. At one feature this is a nuisance. Across a system of features and a team of agents, it is the whole problem.

CyberAlchemy is the response. It is an operating system for humans and agents: a way to turn intent into governed, evidenced, reusable tools, where the same artifact is legible to a person and executable by a machine. It rests on three pillars. **DomainSpec** says what is meaningful in a domain. **Arcanum** says how the work is done. **Saturn** closes the loop with evidence.

The three are not the same thing wearing three names. They are different layers with different jobs. Keeping them distinct is the point.

## DomainSpec — the structured-intent layer

DomainSpec is where meaning is made explicit. A domain is described with a closed vocabulary: 25 meta-types (Entity, Operation, Rule, Event, Workflow, State Machine, and the rest) and 29 typed relationships between them (`enforces`, `produces`, `transitions`, `contains`, …). Every concept maps to exactly one type. Every connection is one of the named edges, with a fixed signature — `enforces` runs Rule → Operation, never the reverse.

That constraint buys determinism. From a typed domain model you can *derive* the test obligations, the observability metrics, and the implementation contracts — by rule, not by guess. The paper states this as a function: `T = f(C, R, Δ)` — tests from concepts, relationships, and derivation rules. Same model in, same obligations out.

This is the layer that removes the stochastic gap. Not by asking the agent to be more careful, but by making the spec formal enough that a deterministic function can do the derivation instead.

## Saturn — the convergence loop

A spec is a baseline. Reality drifts from it. Saturn is the loop that closes that gap: observe what was actually built, compare it to the DomainSpec baseline, detect the drift, correct, verify, and feed the result back into governance.

DomainSpec owns the intent end of that loop. Saturn owns the evidence end. Where DomainSpec says "this is what should be true," Saturn says "here is what is true, and here is the distance between them." Drift becomes a measured quantity, not a surprise.

## Arcanum — the execution layer

Arcanum is how the work actually gets done. It is the public framework: reusable agent capabilities (called sigils), composed routes (spells), and a development loop that takes a wild idea to a validated working slice — prompt, refine, invoke, route, execute, learn. Each serious output leaves receipts: sources, decisions, validators, residue, and the next route.

Arcanum is what you can open and read today. It is one layer of the system, not the whole of it.

## The agentic system

Humans and agents operate through these layers together. The coordination is explicit. Multi-agent work goes through a dispatch system with a hard rule: agents that are meant to disagree are paired so they actually do, and nothing runs until a human confirms the plan. The system assumes governance has a cost — adding rules to agents can *lower* compliance, an effect the paper formalizes as governance attenuation — and it answers that with structure (separating the agent that observes from the agent that acts, detecting drift deterministically) rather than with more rules.

## How they compose

```
        intent  ───▶  DomainSpec   (what is meaningful: typed concepts + relationships)
                          │  derives
                          ▼
                       Arcanum     (how the work is done: sigils, spells, the loop)
                          │  produces
                          ▼
                        Saturn     (evidence: observe → compare → drift → correct → verify)
                          │  feeds back to governance
                          └──────────────▶ (tunes DomainSpec + Arcanum)

   CyberAlchemy = the whole loop, for humans and agents.
```

## What is built so far

The claims here are scoped to what exists and was validated. Where something is planned, it says so.

- **A deterministic test-derivation engine is built.** It implements `T = f(C, R, Δ)` in code: it parses canonical feature docs into a typed graph, derives obligations by pure rules, gives each a content-addressed id, and emits a byte-stable TEST-SPEC. Same docs in, byte-identical output. 95 tests pass; 0 type errors.
- **It refuses rather than fabricates.** When a spec expression is not formal enough to derive a real test, the engine emits a counted, visible gap (`needs_formal`), it does not invent a plausible test. That refusal is itself a measurement: the gap count is a spec-formalization metric. On the pilot feature it reads 96%.
- **Fault-detection was measured.** Mutation testing (E3) ran on the pilot. After authoring one closed-form rule the spec had left implicit, the derived suite's mutation score moved from 38.75% to 54.37%, and the makeup-policy module doubled (17.2% → 36.56%). The regenerated suite passed 13/13 against the real, unmutated code — the gap was unwritten spec, not divergent code.
- **The engine derives its own feature.** Run on its own DomainSpec docs, it produces its own TEST-SPEC. The self-application is a fixpoint, not a slogan.
- **A conformance validator is specified.** A pre-registered experiment defines a check that the types and edges in a generated spec are valid against the taxonomy and the relationship signatures. Defined and frozen; not yet built.
- **Multi-agent dispatch is in use.** The dispatch ledger records real runs, each human-gated, dominated by research and review work.

## Roadmap

Planned, not done: widen the engine's grammar to more document classes; give it a value-asserting oracle for the hardest arithmetic; build the conformance validator; run the deterministic engine as the live test-spec stage in place of the LLM for the backend-domain slice; take mutation testing from one pilot to a corpus. The paper's larger experiments on governance attenuation and self-governance remain open.

The shape is the argument. We absorb the complexity into the structure so the people working inside it do not have to carry it.
