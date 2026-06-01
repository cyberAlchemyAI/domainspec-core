---
title: GoldenQuill Ontology + DAG Grant Research Strategy
date: 2026-06-01
status: proposed-research-strategy
dispatch: docs/strategy/goldenquill_ontology_dag_grant_research_strategy_2026-06-01.dispatch.json
---

# GoldenQuill Ontology + DAG Grant Research Strategy

## Objective

Design a governed research route for adapting the Paradigma "knowledge as DAG"
model to GoldenQuill / Tilth grant writing, using Arcanum Ontology Vault,
GoldenQuill's existing memory and vault surfaces, and useful patterns from
`domainspec-lean-formalization`.

The target is not a new monolithic memory store. The target is a grant-writing
research graph where claims, evidence, funder rules, objections, reviewer
signals, replications, and downstream proposal decisions are first-class nodes
with explicit provenance and authority.

## Reference Frame

The Paradigma article argues that research becomes more useful when the unit of
knowledge is a directed acyclic graph rather than a paper. In that graph,
experiments know their parents, replications are first-class branches, agents
can traverse and extend the graph, and consensus emerges from verification,
replication, stress-testing, and extension.

For grant writing, translate the article this way:

| Research DAG idea | Grant-writing adaptation |
| --- | --- |
| Hypothesis node | A funder-fit hypothesis, theory-of-change claim, eligibility claim, budget assumption, or reviewer-risk claim. |
| Experiment node | A draft section, evidence search, rubric scoring pass, budget/proforma calculation, outreach test, or compliance check. |
| Replication node | A second source, second seat, second model family, prior-award precedent, or repeated scoring pass that tests whether the claim holds. |
| Objection node | Red Team/Judge challenge, admin-risk warning, missing-evidence warning, or rule conflict. |
| Extension node | A proposal variant, adjacent opportunity, reused evidence packet, or next funder strategy. |
| Consensus | Signed/operator-approved confidence state, not mere model agreement. |

The grant graph should answer: what was claimed, why it was believed, what
evidence supported it, what contradicted it, which agent or human reviewed it,
what proposal surface consumed it, and whether it may be reused later.

## Existing Groundwork To Reuse

### GoldenQuill

GoldenQuill already has the ingredients for a graph-shaped grant knowledge
system:

- `docs/MEMORY_KNOWLEDGE_LAYER_INDEX.md` maps authority classes across memory,
  lessons, cards, vault helpers, knowledge packs, substrate contracts, and
  Reflection Packet.
- `docs/strategy/goldenquill_memory_surface_architecture_synthesis_2026-06-01.md`
  already proposes a `MemoryEvidencePacket` contract with source path, locator,
  authority class, org scope, allowed uses, promotion owner, and freshness.
- `pipeline/vault/vault_query_skill.py` and
  `pipeline/vault/research_db_query_skill.py` are natural read gateways for
  evidence nodes.
- `pipeline/cards/CLC/research_evidence.yaml` and the broader card system are
  candidate ontology nodes for reusable domain/funder knowledge, subject to
  signed-asset boundaries.
- `golden_quill_substrate/contracts.py` already names evidence operations such
  as `evidence.intake` and `evidence.promote`, which are close to graph events.
- `pipeline/engineering/agents/` and `skills/` already define Scout, Scribe,
  Editor, Judge, Logician, and related surfaces that can become graph producers
  or validators.

The main gap is not absence of memory. It is absence of a first-class grant
DAG contract that tells agents how to create, link, validate, reuse, and retire
grant knowledge nodes without flattening authority.

### Ontology Vault

Ontology Vault is directly relevant because its branch-aware model already
separates:

- meaning: what the system means, values, defines, frames, or tries to make true,
- system: machinery that realizes meaning,
- operational: situated use in context,
- bridge: trace, validation, constraint, contradiction, and drift.

For GoldenQuill, use local aliases:

| Ontology Vault branch | GoldenQuill local alias | Example |
| --- | --- | --- |
| meaning | grant meaning / funder intent | "This applicant advances rural food-system resilience." |
| system | Tilth machinery | Scout source adapter, Scribe draft, Judge rubric score, Logician gate. |
| operational | proposal run context | Specific RFA, applicant, org vault, deadline, budget reality. |
| bridge | claim-evidence-funder trace | RFA clause, source evidence, draft paragraph, score, risk flag. |

The validated branch-aware schema candidate is good enough for research
experiments, but it remains non-canonical. Use it as a pressure-tested candidate
shape, not as an immediate production schema.

### Lean Formalization

`domainspec-lean-formalization` contributes a governance pattern, not grant
math:

- keep research closure, proof/verification state, ontology state, and prose
  separate;
- dispatch by concern/register rather than dumping whole folders into one
  context;
- treat formalization/proof as validation state, not narrative authority;
- preserve objections and counterexamples as load-bearing graph nodes.

For GoldenQuill, the translation is:

- proposal prose is not evidence;
- Judge score is not truth;
- Logician pass is not funder success;
- operator approval is not ontology promotion;
- reusable grant knowledge requires a bridge from claim to source evidence,
  tests/review, and allowed-use scope.

## Proposed Grant DAG Model

Minimum node families:

| Node family | Purpose | Example owners |
| --- | --- | --- |
| `opportunity` | Funder/RFA/opportunity facts. | Scout, vault query, source adapter. |
| `eligibility_claim` | Applicant or project satisfies a rule. | Scout, Logician. |
| `funder_fit_hypothesis` | Why this project fits this funder. | Scout, Scribe, Judge. |
| `evidence_item` | Source-backed fact or artifact. | Vault, MemoryEvidencePacket, project context. |
| `proposal_claim` | Claim that appears in draft prose. | Scribe. |
| `rubric_criterion` | Funder scoring or review dimension. | Judge. |
| `objection` | Missing evidence, contradiction, admin-risk, rule conflict. | Red Team, Logician, Editor. |
| `replication_check` | Independent confirmation or second-pass review. | Judge, Red Team, cross-family model. |
| `decision` | Operator or gate decision. | Operator, Logician, decision-gate. |
| `reuse_candidate` | Candidate durable lesson, card update, knowledge-pack item, or org memory. | Reflection Packet, ontology-vault. |

Minimum edge families:

| Edge | Meaning |
| --- | --- |
| `motivates` | A funder or applicant signal motivates a hypothesis. |
| `supports` | Evidence supports a claim. |
| `contradicts` | Evidence or review challenges a claim. |
| `realized_by` | A business/grant claim is realized by a system artifact or draft section. |
| `tested_by` | A claim is checked by a gate, score, test, or review. |
| `replicated_by` | A claim survives an independent review/source/model-family pass. |
| `constrained_by` | A claim is limited by RFA, budget, privacy, org, or posture constraints. |
| `consumed_by` | A proposal draft, report, or decision used the node. |
| `promoted_to` | A candidate became a signed card, lesson, org memory, or canonical source after owner approval. |
| `retired_by` | A claim was invalidated, superseded, or no longer reusable. |

## Research Route

1. Recover current GoldenQuill memory, vault, card, evidence, and agent
   surfaces.
2. Map Ontology Vault's branch-aware candidate schema against grant-writing
   concepts.
3. Inspect Lean formalization's agent/ontology/proof-state split for reusable
   research discipline.
4. Design a small grant DAG contract that can represent one proposal run from
   opportunity intake to claim-evidence map to final decision.
5. Run parallel research lanes:
   - GoldenQuill memory/vault/call-site lane,
   - Ontology Vault schema lane,
   - grant workflow lane,
   - agent/seat production lane,
   - validation/Logician lane,
   - Lean governance-transfer lane,
   - Paradigma/DAG analogy lane.
6. Synthesize a `GrantKnowledgeGraph` candidate with node/edge vocabulary,
   authority classes, allowed uses, and validation gates.
7. Validate with one toy case using only non-org demo/public fixtures.
8. Decide next route: `ontology-vault` convention candidate, `task-session`
   implementation of fixtures, or `decision-gate` if production authority is
   unresolved.

## First Toy Case

Use non-org demo/public fixtures only:

- a demo RFA from `tests/demo/demo_rfa/`,
- a demo project context from `tests/demo/demo_project_context/`,
- one Scout opportunity fact,
- one Scribe proposal claim,
- one Judge rubric result,
- one Logician objection,
- one operator-style decision stub.

Done means the toy graph can show:

- every proposal claim has source evidence or a named gap;
- every reusable claim has an authority class;
- every objection remains visible;
- no generated or proposal-only node becomes canonical memory;
- no org-private context is read;
- the graph can produce a compact evidence packet for Scribe/Judge/Logician.

## Subagents And Skills To Use

Arcanum:

- `dispatch-spec` for route shape and gates.
- `ontology-vault` for branch-aware ontology mapping and promotion boundaries.
- `context-builder` for compact evidence packs.
- `inventory` for reusable source summaries after owner review.
- `decision-gate` for authority choices.
- `task-session` for a bounded implementation SWU.
- `experiment-harness` for toy-case validation.
- `robot-talks` for parallel lane research.
- `x-ray` for architecture and graph explanation.
- `feature-glossary` for the eventual grant DAG vocabulary.

GoldenQuill:

- `skills/scout-discovery/SKILL.md`
- `skills/scribe-ghostwriter/SKILL.md`
- `skills/editor/SKILL.md`
- `skills/judge-rubric/SKILL.md`
- `skills/logician/SKILL.md`
- `skills/tilth-card-research/SKILL.md`
- `pipeline/engineering/agents/scout_discovery_agent_v1.md`
- `pipeline/engineering/agents/scribe_writer_agent_v1.md`
- `pipeline/engineering/agents/judge_scoring_agent_v1.md`
- `pipeline/engineering/agents/logician_enforcement_agent_v1.md`

Lean-formalization:

- `.agents/agent-prompts/theorem-ontology-researcher.agent.md`
- `.agents/agent-prompts/theorem-discovery-writer.agent.md`
- `.agents/agent-prompts/theorem-robot-dialogue-mediator.agent.md`
- `.agents/skills/theorem-ontology-research/SKILL.md`
- `.agents/skills/theorem-discovery-writing/SKILL.md`
- `.agents/skills/theorem-robot-dialogue/SKILL.md`

## Promotion Guardrails

- A graph node is not canonical because an agent produced it.
- A replicated claim is not reusable unless its source authority and allowed
  use permit reuse.
- A proposal claim cannot outrank the RFA, project context, signed card, or
  source evidence it depends on.
- Reflection Packet may propose memory deltas; it must not silently write
  canonical memory.
- Ontology Vault may map and validate candidate conventions; promotion requires
  the owning governance route.
- Research uses demo/public fixtures unless an explicit single-org context is
  authorized.

## Recommended Next Move

Run the dispatch route in
`docs/strategy/goldenquill_ontology_dag_grant_research_strategy_2026-06-01.dispatch.json`.

If the user approves subagents, use the proposed fanout. If not, run the same
steps locally with a parent-led synthesis and keep the subagent lanes as
research sections.
