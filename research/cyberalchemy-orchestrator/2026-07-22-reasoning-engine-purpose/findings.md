# Is `cyberalchemy-orchestrator` a reasoning engine?

## Evidence boundary

This finding covers the read-only checkout at frozen commit `ca560b866b16440b3186f960ecc41d91e42dd03a`. The source record is the verbatim [explorer transcript](research.md); current capability means capability witnessed in that checkout, not behavior that may be supplied by a separate Claude/Codex session or another runtime.

**Executive answer: no.** The repository's explicit purpose is multi-agent orchestration for decision hygiene, not a stated reasoning-engine project. What it currently contains is best classified as an **agent-workflow governance framework**, a **read-oriented orchestration control plane**, a narrow agent-selection utility, and an experimental publication bus. The repository calls itself an agent-orchestration project and separates today's substrate from an unbuilt scientific loop ([Simon, purpose thesis](research.md#purpose-thesis); [`README.md:29-64`](../../../projects/cyberalchemy-orchestrator/README.md#L29-L64)).

## Purpose, current system, and future direction

**Purpose.** The project treats multi-agent coordination as a decision-quality problem: counter correlated bias and noise with opposed angles, independence, aggregation, and audit. It explicitly marks the premise as a hypothesis, not a settled result ([Simon, purpose thesis](research.md#purpose-thesis); [`README.md:29-43`](../../../projects/cyberalchemy-orchestrator/README.md#L29-L43)). Its plan names the job "decision hygiene" and keeps the category-theoretic typing speculative ([Simon, purpose thesis](research.md#purpose-thesis); [`docs/PLAN.md:44-67`](../../../projects/cyberalchemy-orchestrator/docs/PLAN.md#L44-L67)).

**Current system.** The checkout reads and derives operational dispatch state, exposes that state through APIs, records a confirmation marker, recommends agent personas, and validates append-only publications. It does not contain a deployed transition from confirmation to chain execution: the code says a separate Claude session watches the marker and runs the chain ([Turing, dispatch control-plane reader](research.md#1-dispatch-control-plane-reader); [`implementations/server/main.py:1-11`](../../../projects/cyberalchemy-orchestrator/implementations/server/main.py#L1-L11), [`implementations/server/main.py:229-271`](../../../projects/cyberalchemy-orchestrator/implementations/server/main.py#L229-L271)). Therefore "read-oriented control plane" is precise; "deployed orchestrator" or "autonomous execution engine" is not.

**Future direction.** The repository proposes a deterministic protocol kernel, deliberation bus, aggregator, and typed knowledge/provenance store, while explicitly saying that the kernel would never decide which answer is better ([Simon, reasoning-engine-adjacent aspirations](research.md#reasoning-engine-adjacent-aspirations); [`docs/PLAN.md:171-200`](../../../projects/cyberalchemy-orchestrator/docs/PLAN.md#L171-L200)). It also proposes a claim-refutation-golden-graph loop, but labels the loop and its claim-graph mechanics unbuilt/open ([Hewitt, capability-versus-absence matrix](research.md#capability-versus-absence-matrix); [`docs/PLAN.md:275-301`](../../../projects/cyberalchemy-orchestrator/docs/PLAN.md#L275-L301)). The defensible direction is therefore **a build-from-owned orchestration and epistemic-governance substrate that could support governed collective reasoning**, not a current reasoning engine.

## Repository evidence

| ID | Finding | Explorer record | Exact repository witness |
|---|---|---|---|
| P1 | The declared problem is decision hygiene for multi-agent judgment. | [Simon — Purpose thesis](research.md#purpose-thesis) | [`README.md:29-43`](../../../projects/cyberalchemy-orchestrator/README.md#L29-L43); [`docs/PLAN.md:46-62`](../../../projects/cyberalchemy-orchestrator/docs/PLAN.md#L46-L62) |
| C1 | The control plane parses and joins opening/close rows into operational state; it does not execute group dependencies. | [Turing — Dispatch control-plane reader](research.md#1-dispatch-control-plane-reader) | [`implementations/server/ledger.py:95-221`](../../../projects/cyberalchemy-orchestrator/implementations/server/ledger.py#L95-L221); [`implementations/server/ledger.py:432-474`](../../../projects/cyberalchemy-orchestrator/implementations/server/ledger.py#L432-L474) |
| C2 | Its only server-side write is a confirmation marker; execution remains external to this repo's server. | [Turing — Dispatch control-plane reader](research.md#1-dispatch-control-plane-reader) | [`implementations/server/main.py:1-11`](../../../projects/cyberalchemy-orchestrator/implementations/server/main.py#L1-L11); [`implementations/server/main.py:229-271`](../../../projects/cyberalchemy-orchestrator/implementations/server/main.py#L229-L271); [`implementations/README.md:88-94`](../../../projects/cyberalchemy-orchestrator/implementations/README.md#L88-L94) |
| C3 | Agent selection combines literal/deterministic ranking with an optional Anthropic adjudication of persona fit. This is a narrow target-selection decision, not object-level reasoning over the user's claims. | [Turing — Agent-pool selector](research.md#2-agent-pool-selector) | [`tools/agent-pool-mcp/src/select.mjs:36-96`](../../../projects/cyberalchemy-orchestrator/tools/agent-pool-mcp/src/select.mjs#L36-L96); [`tools/agent-pool-mcp/src/adjudicate.mjs:12-87`](../../../projects/cyberalchemy-orchestrator/tools/agent-pool-mcp/src/adjudicate.mjs#L12-L87) |
| C4 | The publication probe validates, deduplicates, journals, and verifies contributions; its MCP surface exposes publication, not semantic synthesis or peer reading. | [Turing — Publication-bus probe](research.md#3-publication-bus-probe) | [`bus.mjs:141-237`](../../../projects/cyberalchemy-orchestrator/docs/features/agents-communication-infra/experiments/bus-publication-probe/src/bus.mjs#L141-L237); [`mcp-server.mjs:22-81`](../../../projects/cyberalchemy-orchestrator/docs/features/agents-communication-infra/experiments/bus-publication-probe/src/mcp-server.mjs#L22-L81) |
| F1 | The semantic claim graph, veracity propagation, and contradiction handling are candidate bets/open questions rather than executable capability. | [Hewitt — Capability-versus-absence matrix](research.md#capability-versus-absence-matrix) | [`vault/hypothesis/claim-graph.md:28-76`](../../../projects/cyberalchemy-orchestrator/vault/hypothesis/claim-graph.md#L28-L76); [`vault/hypothesis/claim-graph.md:96-121`](../../../projects/cyberalchemy-orchestrator/vault/hypothesis/claim-graph.md#L96-L121) |
| F2 | The scientific claim-to-enrichment loop is explicitly not built. | [Simon — Purpose thesis](research.md#purpose-thesis) | [`README.md:49-53`](../../../projects/cyberalchemy-orchestrator/README.md#L49-L53); [`docs/PLAN.md:64-67`](../../../projects/cyberalchemy-orchestrator/docs/PLAN.md#L64-L67) |

## Definition and minimum witness

For this classification, a **reasoning engine** needs all three of the following:

1. machine-readable epistemic input: premises, claims, evidence, rules, or equivalent;
2. a repository-owned, executable **object-level semantic inference or evaluation procedure**;
3. a semantic output derived from that input with a traceable justification.

This is a deliberately modest witness. Revision, retraction, or enrichment under counterevidence would be stronger epistemic evidence, but it is not universally required for a reasoning engine. Apache Jena, for example, derives additional RDF assertions entailed by data, ontologies, axioms, and rules and can expose derivations ([Jena inference documentation](https://jena.apache.org/documentation/inference/index.html)). Drools executes explicit rules against facts ([Drools rule-engine documentation](https://kie.apache.org/docs/10.0.x/drools/drools/rule-engine/index.html)); Lean checks proof terms in a small trusted kernel ([Lean language reference](https://lean-lang.org/doc/reference/latest/)). These are concrete semantic owners of the category.

An external model may implement part of step 2, but only when the repository defines and executes the object-level evaluation/derivation contract and preserves how the output follows from the input. Persona selection, prompting separate agents to reason, or transporting their answers does not satisfy the witness by delegation alone. That guard is decisive here: the only model-backed path selects agents from a pool, while the planned kernel expressly declines answer-quality judgment ([Turing, agent-pool selector](research.md#2-agent-pool-selector); [`adjudicate.mjs:27-87`](../../../projects/cyberalchemy-orchestrator/tools/agent-pool-mcp/src/adjudicate.mjs#L27-L87), [`docs/PLAN.md:179-188`](../../../projects/cyberalchemy-orchestrator/docs/PLAN.md#L179-L188)).

Workflow ownership is different. Temporal owns durable application execution ([Temporal documentation](https://docs.temporal.io/)); LangGraph calls itself a low-level orchestration framework/runtime for long-running stateful agents ([LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)); AutoGen's runtime manages agent lifecycle, communication, security, and monitoring ([AutoGen runtime documentation](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/framework/agent-and-agent-runtime.html)). Those precedents show why executing or governing reasoning actors is not itself semantic inference.

## Verdict matrix

| candidate | owner (precedent) | witnessed? (non-vacuity) | sound? (definitional) | verdict |
|---|---|---|---|---|
| current reasoning engine | Jena-style semantic inference | No — C1–C4, F1–F2 | Yes, under the minimum witness | **KILL: no executable semantic witness** |
| agent-workflow governance framework | Repo-owned discipline; AutoGen/LangGraph bound the runtime category | Yes — P1, C1–C4 | Yes | **KEEP: strongest current class** |
| read-oriented orchestration control plane | Repo-owned; Temporal/LangGraph provide execution contrast | Yes — C1–C2 | Yes, with “read-oriented” retained | **KEEP: current implementation** |
| autonomous orchestration execution engine | AutoGen, LangGraph, Temporal | No — C2 | Yes | **ROADMAP ONLY: not current** |
| executable knowledge/ontology system | Jena | No — F1 | Yes | **PROPOSED ONLY** |
| epistemic-governance substrate | Repo-owned claim/proof and promotion discipline | Partial — P1, C4, F1–F2 | Yes, if “substrate” does not imply inference | **KEEP, QUALIFIED: direction/current scaffolding** |
| rule engine | Drools; Jena generic rule reasoner | No — C1–C4 | Yes | **NOT CURRENT** |
| theorem prover | Lean | No — C1–C4 | Yes | **NOT CURRENT** |
| hybrid reasoning engine | Jena shows a hybrid still needs defined rule semantics | No | No — “hybrid” merely absorbs orchestration plus delegated agent reasoning | **KILL: tautological category inflation** |

Category ownership never causes a KILL. The two KILLs are evidentiary/definitional: the current reasoning-engine claim lacks the minimum witness, and the hybrid label has no discriminating semantics.

## Banked negative and promotion conditions

**Typed negative.** At this commit, no repository-owned executable path consumes semantic premises, claims, rules, or evidence and derives or selects a substantive conclusion through repository-defined semantics. The witnessed code derives ledger metadata (C1), selects agents (C3), and validates publication/provenance (C4). External or manual agents may still perform reasoning outside the repository; this negative does not claim otherwise.

Promote the project to a current reasoning-engine claim only when the repository can show:

1. a machine-readable epistemic input schema;
2. an executable object-level inference/evaluation procedure, including its semantics and external-model boundary if used;
3. a substantive derived output with provenance linking input, procedure, and result;
4. a reproducible fixture demonstrating the derivation and a negative/control case;
5. if “autonomous orchestration” is also claimed, an owned execution path from confirmation through registration, agent/group execution, and closeout.

Revision, retraction, contradiction handling, and model enrichment should be treated as stronger promotion evidence for an **epistemic** engine, not smuggled into the minimum generic definition.

## Reviewer convergence and validation

- **Lakatos: PASS** after correcting the minimum witness and replacing the deployed-orchestrator label with read-oriented control plane.
- **Gödel: PASS** on the current-reasoning-engine KILL, with the explicit guard that external/manual execution may exist outside this checkout.
- **Quine: PASS** after requiring a repository-owned object-level semantic procedure and rejecting hybrid/category inflation.
- Ledger parser/cache/aggregation checks passed, including the live-ledger smoke read ([Turing — Checks run](research.md#checks-run); [`implementations/tests/test_ledger.py:1-7`](../../../projects/cyberalchemy-orchestrator/implementations/tests/test_ledger.py#L1-L7), [`implementations/tests/test_ledger.py:471-504`](../../../projects/cyberalchemy-orchestrator/implementations/tests/test_ledger.py#L471-L504)).
- The publication-bus probe passed 10/10 tests, including persistence-before-receipt, idempotency, conflict, phase, forgery, concurrency, and publish-only MCP behavior ([Turing — Checks run](research.md#checks-run); [`bus.test.mjs:49-117`](../../../projects/cyberalchemy-orchestrator/docs/features/agents-communication-infra/experiments/bus-publication-probe/test/bus.test.mjs#L49-L117), [`mcp.test.mjs:27-88`](../../../projects/cyberalchemy-orchestrator/docs/features/agents-communication-infra/experiments/bus-publication-probe/test/mcp.test.mjs#L27-L88)).
- Dependency-bound checks were skipped, not failed: API tests lacked `fastapi`, UI tests lacked `playwright`, and agent-pool smoke/RPC tests lacked installed Node dependencies including `js-yaml` ([Turing — Checks run](research.md#checks-run); [`test_main.py:1-28`](../../../projects/cyberalchemy-orchestrator/implementations/tests/test_main.py#L1-L28), [`test_ui.py:1-20`](../../../projects/cyberalchemy-orchestrator/implementations/tests/test_ui.py#L1-L20), [`tools/agent-pool-mcp/package.json:10-18`](../../../projects/cyberalchemy-orchestrator/tools/agent-pool-mcp/package.json#L10-L18)). No dependencies were installed into the read-only target.

## Dispatch closeout

Dedicated auditor Brandenburg returned **ACCEPT**; `exit_reason: resolved`; `agents_spawned.total: 9`, with tree `explorer: 3`, `synthesizer: 1`, `skeptic: 3`, `writer: 1`, `auditor: 1`, and `helpers: 0`; `loops_used: 1`. The two init-gate checkers are infrastructure and excluded from the dispatch count. The target remained frozen and clean.
