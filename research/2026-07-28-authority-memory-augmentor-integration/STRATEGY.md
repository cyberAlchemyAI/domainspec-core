# Augmentor User Understanding, Knowledge Graph, and Reasoning Strategy

Status: revised confirmation-ready proposal, unregistered, unexecuted  
Dispatch: `2026-07-28-authority-memory-augmentor-integration`  
Schema: `0.8.0`  
Final approver: `parent`

The folder and dispatch identifiers retain the first draft's historical slug.
This document and the current sheet replace that draft's authority-and-receipt
emphasis with an agent-experience objective.

## Direct Strategy

Augmentor should not receive a second memory system or a large always-loaded
ontology. It should receive a small, host-composed **reasoning context** made
from four separately owned layers:

```text
protected user handles
        +
existing Human Knowledge / AI Memory / context state
        |
        v
rebuildable typed graph projection -- bounded query --> small relevant subgraph
        |                                                   |
        +---------------- ReasoningContext ------------------+
                                                            |
                                                            v
                                  deterministic checks + model synthesis
                                                            |
                                                            v
                                        useful answer / abstention / next action
                                                            |
                                                            v
                                      visible correction or forget proposal
```

The first slice should use existing ResonantOS storage and prompt-composition
owners. A graph database is not a prerequisite. Start with compact typed records,
incremental deltas, a small adjacency index or direct scan, strict hop/node/token
budgets, and a user-visible explanation of which context changed the answer.

The private CyberAlchemy v2 authority model remains a boundary and design source,
not the feature. Receipts and audit remain minimal supporting mechanics required
by the governed research route; they must not dominate the proposed Augmentor
experience.

## P1 Trigger Decision

Dispatch is warranted on all four P1 triggers:

- **Synthesis:** the result must combine the User/Translate/Guide candidate
  family, CAV2 ontology and executable graph precedents, the bounded reasoning
  evaluator, IDE knowledge-reference ergonomics, and current ResonantOS
  Augmentor/memory behavior.
- **Context protection:** raw design, runtime, fixture, UX, and prior-research
  material is substantially larger than the parent should carry.
- **Isolation:** alternative graph and reasoning boundaries should be attacked
  before any product implementation is proposed.
- **Parallelism:** user understanding, graph evolution, reasoning support, and
  product integration can be investigated independently before synthesis.

This is a `research` dispatch. It does not authorize implementation.

## Lanes, Groups, and Subagents

### Group 1: explorers - parallel

Anti-bias: composite `methodology + source-corpus`.

| Agent | Role | Angle | Expected output |
|---|---|---|---|
| Ahrens, Sönke | explorer | User understanding and adaptive explanation | Minimal protected user model, adaptation loop, correction/forget controls, concrete user journeys, anti-profiling limits |
| Turing, Alan | explorer | Incremental typed knowledge graph | Compact node/edge and delta contracts, query/invalidation model, storage alternatives, hard overhead budgets, evolution path |
| Hewitt, Carl | explorer | Bounded reasoning support | `ReasoningContext`/`ReasoningResult`, deterministic-plus-model loop, useful reasoning operations, fallback and evaluation fixtures |
| Simon, Herbert | explorer | Augmentor experience and host integration | Current/missing matrix, host composition seam, progressive-disclosure UX, implementation increments, unit/browser measures |

Every explorer pair has one digest-owned predicted-disagreement record in
`dispatch-sheet.json`.

### Group 2: synthesizer - after explorers

Shannon reconciles the four returns into one cited Augmentor architecture. The
result must define:

- the layer and data-flow model;
- protected user handles and their lifecycle;
- graph records, deltas, invalidation, and bounded queries;
- reasoning inputs, operations, outcomes, and fallback;
- visible correction, forgetting, and "why this context" UX;
- storage, latency, token, hop, node, and cache budgets;
- three fixture-backed journeys;
- a v0/v1/v2 implementation sequence that reuses existing ResonantOS owners.

### Group 3: reviewers - parallel plus robot-talks

Anti-bias: `attack-vector`.

| Agent | Role | Gate | Expected output |
|---|---|---|---|
| Lakatos, Imre | skeptic | precedent and duplication | Detect second memory stores, duplicate profiles/prompt builders, unnecessary graph infrastructure, and already-owned seams |
| Gödel, Kurt | skeptic | non-vacuity and user-visible benefit | Require an end-to-end graph-grounded behavior improvement with correction controls and measured overhead, or KILL |
| Quine, Willard Van Orman | skeptic | definitional and architectural non-collapse | Keep identity, preference, learning state, memory, graph, retrieval, reasoning, and action distinct |

The synthesizer and reviewers may zig-zag twice. One bounded explorer feedback
route exists for missing current-source evidence.

### Group 4: writer - after reviewer convergence and evidence closure

van Lamsweerde writes `findings.md` as a compact implementation-usable
experience blueprint after the cited-synthesis closure matrix is `ready`. The
strategist, not the writer, appends verbatim explorer returns to `research.md`.

### Group 5: auditor - after writer

Brandenburg performs the research route's mandatory final structural check, but
the check is deliberately narrow: usefulness, economy, evidence support,
non-duplication, privacy, measurable overhead, and dependency-safe increments.
One bounded writer revision is available. The parent remains final approver.

## Dependency Flow

```text
explorers -> synthesizer <-> reviewers -> writer -> auditor -> parent
     ^             |
     +-- feedback -+

auditor -- bounded feedback --> writer
```

- `explorers -> synthesizer`: sequential
- `synthesizer <-> reviewers`: zig-zag, `loop_cap: 2`
- `synthesizer -> explorers`: feedback, `loop_cap: 1`
- `reviewers -> writer`: sequential, after cited-synthesis closure is ready
- `writer -> auditor`: sequential
- `auditor -> writer`: feedback, `loop_cap: 1`
- whole-dispatch `max_loops: 2`

## Strategy Inventory Packet

Packet name: `strategy-inventory-packet`  
Mode: `inventory lookup`  
Authority: none; Inventory is a discovery read model.

### Lookup status

- Owner inventory: `index_json_ok`
  (`.arcanum/inventory/index.json`).
- Consumer product inventory: `machine_index_gap`; no product-local machine
  Inventory index exists in `../workspace-resonant/2.0.0-alpha`.
- Nearby `../workspace-resonant/agentsofthefree/.arcanum/inventory/index.md`
  remains excluded because it belongs to a different nested product.
- User/Translate/Guide: `no_inventory_match`; current files under
  `arcanum/development/user-guide/` must be read directly and retain their
  candidate-development status.

### Query terms

`user guide`, `user ledger`, `domain anchor`, `vocabulary preference`,
`concept state`, `failed analogy`, `active evidence`, `personalization`,
`context memory`, `knowledge graph`, `ontology`, `graph delta`,
`typed relation`, `projection`, `ontology candidate graph`, `reasoning engine`,
`semantic judgment`, `Augmentor`, `IDE knowledge reference`, `low overhead`,
`final approver`, `agent pool`, `predicted disagreement`, and
`confirmation readiness`.

### Selected entries

| Entry | Why selected | Obligation fit |
|---|---|---|
| `ontology-working-prototype-gap-research-result-synthesis` | Leads to the finite candidate-graph contract and current implementation that must be reverified | Graph lane; executable precedent |
| `ontology-population-from-inventory-synthesis` | Supports claim-level selection, small witness slices, bounded projections, and query proof instead of graphing all files | Graph evolution and overhead |
| `entries-resonantos-and-ontology-retrieval-synthesis` | Prior hypothesis that typed traversal can shrink prompt grounding and relocate cost to ingest | Retrieval design; must be challenged |
| `entries-resonantos-living-archive-seam-and-owned-base-synthesis` | Identifies existing ResonantOS host memory and write seams | Consumer non-duplication |
| `agent-reasoning-engine-contract-strategy-result-synthesis` | Defines the bounded semantic evaluator and whole-engine boundary | Reasoning lane |
| `cyberalchemy-orchestrator-reasoning-engine-purpose-strategy-result-synthesis` | Prevents relabeling orchestration or retrieval as object-level reasoning | Definitional gate |
| `entries-unified-ide-ergonomics-spine-synthesis` | Leads to reopenable knowledge-reference and human-facing context primitives | Augmentor/IDE experience |

The current strategy also uses direct User/Translate/Guide source files because
the machine index returned no matching entry for that package.

### Excluded and superseded material

- The first version of this strategy is superseded because it centered
  authority projection, receipts, and audit instead of the user and agent
  experience.
- Generic authority-lifecycle syntheses are supporting boundary evidence, not
  primary explorer lanes.
- Broad graph presentations and interactive maps are excluded as product
  answers: a graph viewer alone does not improve Augmentor reasoning.
- The `agentsofthefree` Markdown-only inventory is wrong product scope.

### Gaps and residue

- User/Translate/Guide is a candidate development family, not a shipped Arcanum
  runtime or durable user-profile implementation.
- ResonantOS has static profile/prompt settings and structured context memory,
  while opt-in learned preference memory remains marked deferred in the
  acceptance matrix.
- ResonantOS has no product-local machine Inventory index.
- The local ResonantOS branch is seven commits behind `origin/dev`, but the
  current origin diff does not touch the identified Augmentor, memory,
  personalization, or ontology-reasoning surfaces; the consumer lane must
  reverify this at execution.
- CAV2 has an executable finite candidate-graph prototype, but it is a private
  no-authority evaluator, not a drop-in ResonantOS graph service.
- The promoted bounded semantic evaluator is not a complete reasoning engine.
- No current artifact proves that the proposed user-plus-graph context improves
  answer quality under a measured latency/token budget.

### Design consequence

The research is partitioned by the four product responsibilities that must stay
separate:

1. protected user understanding;
2. rebuildable semantic structure;
3. bounded reasoning over selected context;
4. ResonantOS-owned agent experience and delivery.

This separation prevents both a monolithic "Augmentor brain" and a collection of
ceremonial components with no visible user benefit.

## Required Research Result

The result is acceptable only if it provides:

1. a direct product thesis and current-versus-missing matrix;
2. a minimal protected user-handle model with edit, forget, stale, and opt-in
   behavior;
3. a compact graph and graph-delta schema that can evolve without graphing
   every file, message, or memory record;
4. bounded retrieval with explicit seed, hop, node, token, latency, storage,
   cache, and invalidation budgets;
5. a reasoning contract that derives conflicts, missing premises, analogies,
   dependencies, comparisons, or abstention rather than merely retrieving;
6. a progressive-disclosure Augmentor UX for context used, correction,
   forgetting, and graph-grounded explanation;
7. at least one runnable end-to-end fixture plus two additional journey
   fixtures;
8. exact unit/browser tests and measurable quality/overhead targets;
9. a v0/v1/v2 implementation order reusing existing ResonantOS memory and
   prompt-composition owners;
10. explicit boundaries against hidden profiling, duplicate memory, private
    source copying, graph-database dependency, and whole-engine inflation.

Evidence closure uses the baseline `cited-synthesis` contract. Exact selectors
are still required for executable fixture and current-code claims, but the
research is not burdened with exact binding for every architectural
recommendation.

## Gate and Ledger State

- Confirmation readiness: pass.
- Live schema: `0.8.0`.
- Current sheet digest:
  `0bd725cd09976d731c650c00b05c50cdf96b7290671f50993277ea9af5ca8e3a`.
- Non-mutating form validation:
  `SHEET_VALIDATION=pass`, `SCHEMA_VERSION=0.8.0`,
  `LEDGER_MUTATION=none`.
- Superseded digest:
  `31485376626d836b76cdd3adb38d18b100feb82d6411959a052dbb3293c2bdf5`;
  its PASS/PASS verdicts cannot support this revision.
- Check-tension: independent checker PASS and reviewer PASS over the current
  digest; all five tests passed for `explorers` and `reviewers`, with no
  apontamentos. See [CHECK-TENSION.md](CHECK-TENSION.md).
- Human confirmation: required now.
- Ledger: unregistered; no dispatch row exists.
- Execution: not started; no product, Arcanum, ontology, authority, or reasoning
  implementation mutation is authorized.

## Next Human Action

The revised sheet is confirmation-ready. The next human action is:

- `confirmed` - register and run this frozen revised dispatch;
- request another revision - which invalidates this digest and gate;
- decline.
