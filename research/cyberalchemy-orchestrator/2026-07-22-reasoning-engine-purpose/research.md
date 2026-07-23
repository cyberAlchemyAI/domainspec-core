# Explorer Returns

## Agent 1 — Turing, Alan

Turing explorer report — frozen commit `ca560b866b16440b3186f960ecc41d91e42dd03a`

## Implementation verdict

The executable repository is not presently a general reasoning engine. It implements:

1. a dispatch-ledger read model and human-confirmation marker;
2. deterministic/LLM-assisted persona selection;
3. an experimental append-only publication bus.

These are orchestration/control-plane primitives. No executable path demonstrates a problem-state model, inference/search cycle, hypothesis revision, solver loop, autonomous dispatch scheduler, or evidence-based conclusion formation. The only model call delegates a bounded candidate-selection judgment to Anthropic.

## Code-path map

### 1. Dispatch control-plane reader

```text
filesystem ledgers
  → parse_ledger()
  → join_rows()
  → derived open/closed/live/legacy fields
  → snapshot/overview/repo/dispatch APIs
```

- `implementations/server/config.py:46-77` resolves explicit or auto-discovered repositories.
- `implementations/server/ledger.py:95-160` structurally parses ledger rows, leniently warning/skipping malformed content.
- `implementations/server/ledger.py:163-221` joins dispatch and close rows; state is the rule `close exists → closed`, otherwise `open` (`:197-203`).
- `implementations/server/ledger.py:284-337` caches parsed read models by file mtime/size.
- `implementations/server/ledger.py:432-474` serves recent rows or one dispatch; it does not execute groups/connections.
- `implementations/server/main.py:57-71`, `:93-174`, `:177-221` expose snapshots, aggregates, filters, and drill-downs.
- The only operational write is confirmation: `implementations/server/main.py:229-271` validates a pending filename and writes `<sheet>.confirmed`.
- Crucially, confirmation does not launch agents: the module says another Claude session watches the marker and runs the chain (`implementations/server/main.py:1-11`); the implementation roadmap repeats that delegation (`implementations/README.md:88-94`).

Concrete transition: pending sheet → confirmed marker. There is no confirmed marker → registered dispatch → spawned agents transition in this codebase.

### 2. Agent-pool selector

```text
query tags/role
  → load canonical YAML pool
  → vocab check / tag-overlap prefilter
  → optional external LLM adjudication
  → validate returned names against global pool
```

- `tools/agent-pool-mcp/src/pool.mjs:23-36` loads and mtime-caches pool entries, names, and closed tag vocabulary.
- `tools/agent-pool-mcp/src/select.mjs:7-34` performs literal vocabulary membership and substring/token suggestions.
- `tools/agent-pool-mcp/src/select.mjs:39-61` ranks by exact tag overlap, role rank, citation flag, then lexical name.
- `tools/agent-pool-mcp/src/select.mjs:67-96` constructs a broader candidate/neighborhood set for adjudication.
- `tools/agent-pool-mcp/src/adjudicate.mjs:12-25` falls back to deterministic candidates without an API key.
- `tools/agent-pool-mcp/src/adjudicate.mjs:27-51` prompts Anthropic for persona fit and one possible missing concept.
- `tools/agent-pool-mcp/src/adjudicate.mjs:58-87` parses the answer, accepts known pool names, and rejects a “new” tag if already in the vocabulary.
- `tools/agent-pool-mcp/src/server.mjs:14-52` exposes only `recommend_agents`, `search_pool`, and `check_vocab`.

This is a bounded recommendation mechanism, not a general reasoning substrate. Hardening gap: returned names are checked against the global pool, not the prefiltered candidate set/exclusions, and the code does not itself cap the parsed list to `n` (`adjudicate.mjs:70-86`).

### 3. Publication-bus probe

```text
publication
  → payload/context validation
  → phase-open check
  → idempotency replay/conflict check
  → logical-duplicate check
  → append accepted event
  → receipt
```

- `docs/features/agents-communication-infra/experiments/bus-publication-probe/src/bus.mjs:28-75` validates context and publication shape.
- `.../src/bus.mjs:141-167` rejects closed phases, conflicting idempotency keys, and duplicate logical messages.
- `.../src/bus.mjs:169-210` appends an accepted journal event before returning its receipt.
- `.../src/bus.mjs:214-237` verifies receipts against persisted events.
- `.../src/mcp-server.mjs:22-38`, `:52-81` exposes publish only.
- Tests explicitly prove publication rules and deny peer-read access: `.../test/bus.test.mjs:49-117`; `.../test/mcp.test.mjs:27-88`.

This transports and validates contributions; it neither interprets nor synthesizes them.

## Checks run

- `python3 -m implementations.tests.test_ledger` — PASS; parser/cache/aggregation suite passed and current ledger smoke read 48 dispatches.
- Bus probe `npm test` — PASS, 10/10.
- `python3 -m implementations.tests.test_main` — not executed: environment lacks `fastapi`.
- `python3 -m implementations.tests.test_ui` — not executed: environment lacks `playwright`.
- Agent-pool `npm run smoke` / RPC test — not executed: dependencies absent (`js-yaml`); I did not install into the read-only checkout.
- HEAD before and after: exact frozen commit; working tree remained clean.

The strongest implementation-level classification is: **an early orchestration/control-plane repository with one narrow outsourced semantic selector, not a demonstrated reasoning engine**.

## Agent 2 — Simon, Herbert

Simon explorer report — frozen commit `ca560b866b16440b3186f960ecc41d91e42dd03a` verified before and after; worktree remained clean.

Verdict: **No, not explicitly or currently a “reasoning engine.”** The strongest evidence supports a more precise classification:

> **A governed multi-agent orchestration system intended to improve collective judgment through decision hygiene, anti-bias structure, provenance, and eventually an auditable deliberation runtime.**

It is reasoning-engine-adjacent in the broad sense that it structures how LLM agents reason together. But the repo does not claim to implement an inference engine, theorem prover, cognitive architecture, or autonomous answer-producing reasoner. A repo-wide search found no occurrence of the phrase “reasoning engine.”

### Purpose thesis

The explicit purpose is to treat multi-agent coordination as a decision-quality problem rather than mere plumbing:

- The project calls itself an “agent-orchestration project” and says its founding hypothesis concerns correlated bias, noise, and framing in multi-agent judgment: `README.md:27-43`.
- Its proposed countermeasures are opposed agent angles, independence, aggregation, and audit: `README.md:37-43`.
- The plan names the job as “decision hygiene,” with category-theoretic typing as the more speculative second half: `docs/PLAN.md:44-62`.
- The envisioned scientific loop is claim → probe → retain → enrich, but it is explicitly “not built yet”: `docs/PLAN.md:64-67`.
- The repo’s strongest conceptual label is “the orchestrator as a noise-reduction machine,” explicitly marked candidate/exploratory: `vault/hypothesis/anti-noise-orchestration.md:1-18`.

### Why “reasoning engine” overstates it

The proposed deterministic kernel explicitly owns protocol—identity, barriers, phases, visibility, transitions—and **“never decid[es] which answer is better”**: `docs/PLAN.md:171-185`. Judgments remain products of the participating LLM agents; the system governs their conditions, sequencing, exposure, aggregation, and audit.

Its current implemented surface is narrower:

- Dispatch discipline, append-only ledger, anti-bias gate, and read-only control plane: `README.md:55-64`.
- Phase 1 is a FastAPI/SSE reader; the write/confirm button is deliberately disabled: `implementations/README.md:1-9`.
- Current code consists of ledger parsing, aggregation, and read endpoints: `vault/constitution/engine-constitution.md:12-15`, `vault/constitution/engine-constitution.md:27-39`.
- Most decision-science, category-theory, and communications-runtime claims remain thesis or proposal: `docs/PLAN.md:220-246`.

The repo’s use of **engine** therefore means “orchestrator backend/core,” not a cognitive or inference engine. Its constitution asks how authoritative facts are safely read, written, cached, and aggregated: `vault/constitution/engine-constitution.md:27-48`.

### Reasoning-engine-adjacent aspirations

A future version could reasonably be described as an **engine for governed collective reasoning**, provided that phrase is carefully qualified:

- Proposed deliberation bus with sealed judgments, reveal barriers, deterministic aggregation, and a typed knowledge/provenance store: `docs/PLAN.md:179-195`.
- Proposed claim → refutation → golden-graph loop, including contradiction handling and epistemic promotion: `docs/PLAN.md:275-301`.
- Candidate assertion-level claim graph with typed premise, contradiction, and corollary edges: `vault/hypothesis/claim-graph.md:28-50`.
- Proposed mechanical veracity propagation and surfacing of contradictions to a human gate: `vault/hypothesis/claim-graph.md:65-76`.

All are proposal/candidate surfaces rather than present capability.

### Declared boundaries

- **Portable substrate vs repo-specific thesis:** dispatch schema, skills, ledger, control plane, and pool are intended to be generic; category theory and epistemic content are specific to this repository: `README.md:377-388`.
- **Protocol vs answer judgment:** the kernel coordinates but does not judge which answer is best: `docs/PLAN.md:179-180`.
- **Operational vs thesis:** current dispatch/read infrastructure is built; anti-noise, CT typing, and most runtime infrastructure are not: `docs/PLAN.md:220-235`.
- **Engine code vs semantics:** the engine constitution governs treatment of records, not what dispatch constructs mean: `vault/constitution/engine-constitution.md:103-109`.
- **Human authorization remains central:** confirmed opening must be persisted before agents may start: `README.md:198-215`.

### Relevant vocabulary

- **Decision hygiene:** opposed lenses, independence, aggregation, freeze-before-discussion, fork guard: `docs/PLAN.md:46-62`.
- **Residue / shadow / probe / verb:** candidate vocabulary for loss, lossy metrics, active interrogation, and transformations: `definitions/DEFINITIONS.md:10-35`, `definitions/DEFINITIONS.md:64-84`, `definitions/DEFINITIONS.md:88-125`, `definitions/DEFINITIONS.md:129-150`.
- **ORCH:** proposed category whose objects are dispatch groups and morphisms are connections; still OPEN: `OBLIGATIONS.md:8-22`, `OBLIGATIONS.md:33-51`.
- **Dispatch / deliberation / composition:** capability flow names orchestration responsibilities rather than intrinsic machine reasoning: `README.md:76-101`.

### Material tensions and contradictions

1. `README.md:531-535` says synthesis under tension “literally” produces residue, but `OBLIGATIONS.md:1-4` and `OBLIGATIONS.md:50-51` say the identification remains unreviewed and OPEN. “Literally” exceeds the repository’s own proof boundary.

2. The repo calls its concrete layer generically droppable into any repository (`README.md:66-72`, `README.md:377-408`), while admitting the substrate is currently hardwired to one Windows operator and unproven on a second machine: `docs/PLAN.md:244-246`.

3. Target architecture proposes a durable mediation substrate, but current mediation is described as an ephemeral transcript-centered act whose center forgets: `vault/hypothesis/orchestration-infra.md:21-32`.

4. Root status says “local (no remote, no push)” at `README.md:14`, but this frozen checkout came from a GitHub remote. That status text is stale relative to the present repository state.

Recommended label: **“multi-agent judgment orchestration and epistemic-governance engine”** for the long-term project; **“dispatch governance plus read-only control plane”** for what exists today.

## Agent 3 — Hewitt, Carl

Verdict: **not currently a reasoning engine**. Its explicit purpose is a decision-science-informed **multi-agent orchestrator**; it contains a credible roadmap toward an epistemic/reasoning engine, but the claim/refutation/revision machinery is explicitly unbuilt.

### Capability-versus-absence matrix

| Capability | Current witness | Assessment |
|---|---|---|
| Coordinate reasoning actors | Dispatch sheets define groups, roles, dependencies, loops, gates, synthesis, and audit: `.claude/skills/domainspec-subagents-strategy/SKILL.md:16-37` | **Yes**, primarily prompt/runtime orchestration |
| Human-gated decisions | Explicit confirmation precedes registration/execution: same file `:18-21`; API writes only a confirm marker: `implementations/server/main.py:229-271` | **Yes**, authorization decision, not inference |
| Store/query execution history | Ledger parser joins opening/close rows and derives state/counts: `implementations/server/ledger.py:95-221`; APIs summarize and filter: `implementations/server/main.py:57-71,93-221` | **Yes**, operational metadata |
| Enforce message provenance | Publication bus validates, journals, deduplicates, and verifies receipts: `docs/features/agents-communication-infra/experiments/bus-publication-probe/src/bus.mjs:141-237` | **Yes**, provenance/protocol, not semantic reasoning |
| Make one bounded semantic decision | Agent-pool MCP asks Haiku to select candidates and judge vocabulary coverage, then validates output: `tools/agent-pool-mcp/src/adjudicate.mjs:12-87` | **Partial**; outsourced model judgment for agent selection only |
| Deterministic ranking | Tag-overlap and role-fit scoring: `tools/agent-pool-mcp/src/select.mjs:39-61` | **Yes**, retrieval/ranking, not inference |
| Derive conclusions from premises | Claim graph, premise/conclusion edges, veracity propagation, and decompositor are all candidate bets/open questions: `vault/hypothesis/claim-graph.md:43-76,96-121` | **No executable witness** |
| Revise/retract conclusions under counterevidence | The desired claim→refutation→golden loop is explicitly “still unbuilt”: `docs/PLAN.md:275-301` | **No** |
| Enrich its model from failures | Engineering correspondence lacks the `enrich` operation: `vault/audit/faces-instance-frozen-map.md:28-43` | **No** |
| Generate conjectures internally | The repo explicitly says the method disciplines conjectures but does not produce them: `vault/axioms/axioms.md:64-80` | **No** |
| Decide which answer is better | Proposed deterministic kernel is specified to “never” make that judgment: `docs/PLAN.md:179-188` | **No; delegated to agents/aggregators/humans** |

### Minimum-witness test

A minimally convincing reasoning engine would need:

1. machine-readable premises, claims, evidence, or rules;
2. an executable inference/evaluation operation;
3. a derived conclusion with traceable justification;
4. revision, retraction, or model enrichment when counterevidence arrives.

This repository has proposals for items 1 and 4, and invokes external LLMs that can perform item 2 inside agent turns, but it has no repository-owned executable path demonstrating all four. The README itself makes the distinction: its purpose is agent orchestration around bias/noise/framing (`README.md:27-53`), while what exists today is the dispatch/control-plane substrate (`README.md:55-64`).

So the precise classification is:

> **A decision-hygiene orchestration framework around reasoning actors, with an intended evolution toward a governed reasoning/epistemic engine—not yet a reasoning engine itself.**

Under a very loose definition—“a system that gets LLM agents to reason together”—it qualifies. Under an architectural definition where the engine itself represents claims, derives conclusions, preserves inference provenance, and revises beliefs, it does not.

### Reproducible checks

```bash
git rev-parse HEAD
git ls-tree -r --name-only HEAD
rg -n -i "reason|infer|conclusion|revise|decision|claim|probe" \
  README.md docs vault implementations tools .claude
PYTHONDONTWRITEBYTECODE=1 python3 implementations/tests/test_ledger.py
(cd docs/features/agents-communication-infra/experiments/bus-publication-probe && node --test)
git status --short
```

Validation:

- Frozen HEAD before and after: `ca560b866b16440b3186f960ecc41d91e42dd03a`
- Ledger suite: passed
- Bus probe: 10/10 passed
- API suite could not run because `fastapi` is not installed
- Agent-pool smoke was skipped because `node_modules` is absent
- Working tree remained clean; no files written.
