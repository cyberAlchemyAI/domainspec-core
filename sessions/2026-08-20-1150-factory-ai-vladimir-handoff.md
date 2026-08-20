---
node_type: session-handoff
session_id: factory-ai-vs-domainspec-2026-08-20-1150
date: 2026-08-20
topic: Factory.ai compared with DomainSpec, Arcanum, cyberAlchemy-v2, and the Lean spine
status: review-pending
handoff_type: research-direction
destination: Vladimir
target_project: domainspec-core
authority_level: session-evidence
---

# Session Handoff: Factory.ai and the DomainSpec ecosystem

## Identity

- Source session reference: Codex conversation of 2026-08-19/20 covering Factory.ai and `domainspec-core`
- Destination label: Vladimir
- Handoff type: `research-direction`
- Target project or lifecycle: `domainspec-core`
- Created for: transfer the completed high-level comparison and select the smallest useful follow-up

## New Session Prompt

```text
Vladimir, receive the findings below as the result of the initial Factory.ai comparison.
Do not restart the research from zero.

Review the central complementarity thesis, attack unsupported or inflated claims, and decide
whether a bounded adapter experiment is justified. Preserve DomainSpec, Arcanum,
cyberAlchemy-v2, and Lean ownership boundaries. Do not implement or promote anything from
this handoff alone.
```

## Executive Finding

Factory.ai and the DomainSpec ecosystem currently appear to address complementary layers.

Factory is strongest, in its public product and documentation surfaces, as an operational
software-development runtime: Missions, specialized agents and subagents, organization-level
controls, agent policies, enterprise operation, APIs, and execution analytics.

Our stack is strongest in the layers that determine what work means and when its results count:
typed intent, capability ownership, evidence boundaries, lifecycle and promotion authority,
explicit residue, claim-to-proof discipline, and machine-checked invariants.

The useful strategic model is:

```text
DomainSpec       defines what should exist
Arcanum          governs how capabilities work
Factory-like     can supply an operational execution substrate
cyberAlchemy-v2  governs authority, evidence, and promotion
Lean             checks selected invariants and bounds supported claims
```

This is a complementarity thesis, not an adoption decision and not proof that Factory lacks
internal equivalents to our governance mechanisms.

## What Factory Has That We Can Use

### 1. Missions as an operational work unit

Factory presents Missions as development work that can be planned, executed, and verified by
agents. This is useful because Arcanum already has work-packs, capability routes, gates,
handoffs, and Task Session ownership, but does not yet present the same turnkey operational
runner described by Factory.

Candidate projection:

```text
approved DomainSpec work-pack
  -> Factory-compatible Mission
  -> bounded agent execution
  -> structured execution receipt
  -> Arcanum observability and authority gates
```

The Mission would execute admitted work. It would not decide whether the work is authoritative,
promoted, or semantically correct.

### 2. Specialized agents, subagents, and Custom Droids

Factory exposes configurable agents and subagents with specialized responsibilities. This can
inform how Arcanum capabilities become operational roles without collapsing their contracts.

Candidate mapping:

| Arcanum concept | Factory-like runtime projection | Boundary to preserve |
| --- | --- | --- |
| capability role | specialized agent or Droid | Arcanum remains the capability owner |
| sigil | bounded operation or tool-bearing role | the sigil contract defines inputs and outputs |
| spell | composed execution route | lifecycle gates are not delegated implicitly |
| Dispatch Spec | agent topology and handoff plan | projection is not schema equivalence |
| Context Builder | minimal role context | whole-session context should not be copied by default |

### 3. Hierarchical controls and policy envelopes

Factory documents hierarchical organization settings and controls over models and agents. These
mechanisms can inform the operational enforcement of our authority boundaries.

Possible uses include permissions per capability, protected actions, required human approval,
repository and tool access, autonomy ceilings, and environment separation. The opportunity is to
project our authority rules into executable controls while keeping cyberAlchemy-v2 as the owner
of meaning and promotion.

### 4. Analytics and operational telemetry

Factory exposes analytics and API surfaces for operational use. Arcanum observability is more
semantically concerned with routes, gates, residues, owners, and evidence, but can benefit from
Factory-like runtime signals:

- cost and duration per work-pack or capability;
- retries, failures, and intervention points;
- context and model usage;
- participating agents and route steps;
- execution status and produced receipts;
- failure and rollback reasons.

The integration must preserve three non-equivalences:

```text
successful execution != correct artifact
validated artifact     != promoted artifact
operational approval   != epistemic authority
```

### 5. Product experience for asynchronous work

Factory provides a useful product reference for delegating work, observing background progress,
intervening, and receiving results. This can inform Arcanum and future Saturn/Augmentor surfaces:
active work, agent and dependency state, intervention requests, receipts, resumable sessions,
and execution history.

The lesson is not to copy the interface. The useful pattern is to make the path from intent to
execution, evidence, and decision visible.

## What We Have That Is Not Evidenced In Factory's Public Documentation

The wording here is deliberate. The research did not establish that Factory lacks these
capabilities internally; it established that equivalent mechanisms were not evident in the
public sources inspected.

### 1. Authority as an explicit governed object

cyberAlchemy-v2 separates evidence, ownership, lifecycle state, and promotion. Factory documents
operational and organizational control, but the inspected public material did not show an
equivalent model for deciding when generated content becomes an authoritative definition,
decision, or promoted artifact.

### 2. Separation of intent, method, execution, authority, and proof

Our ecosystem deliberately separates:

| Layer | Current responsibility |
| --- | --- |
| DomainSpec | typed intent and the system to be built |
| Arcanum | method, capabilities, routes, gates, and operational evidence contracts |
| execution runtime | carrying out admitted work |
| cyberAlchemy-v2 | authority spine, evidence boundaries, and promotion |
| Lean spine | machine-checked statements for selected invariants |

Factory integrates a broad operational platform, but the inspected sources did not expose this
same decomposition of semantic and epistemic owners.

### 3. Claim-to-proof discipline

This project requires narrative claims to remain within available proof or cited evidence.
The Lean repository makes proof status and open obligations explicit. No machine-checked
equivalent to this claim-bounding discipline was identified in Factory's public documentation.

### 4. Formalized invariants

The Lean work gives selected system properties a machine-checked spine. Factory-like controls
can reduce operational risk; formal invariants can reduce ambiguity about which properties the
system actually sustains. One does not substitute for the other.

### 5. Residue and gaps as governed state

Our stack preserves blockers, contradictions, insufficient evidence, rejected candidates, and
open obligations rather than silently converting incomplete work into a terminal conclusion.
An equivalent epistemic residue model was not identified in the inspected Factory material.

### 6. Governed capability construction

Arcanum aims to govern how capabilities, sigils, spells, routes, gates, evidence, observation,
and lifecycle ownership are authored and evolved. Custom Droids provide configurable agent
behavior, but the public Factory material inspected did not evidence an equivalent authority and
promotion structure for constructing the capability system itself.

## Strategic Implication

Our strongest route is not to compete with Factory on a generic agent runner. It is to preserve
and deepen the layer a runner does not publicly evidence: typed intent, explicit authority,
governed promotion, evidence-linked decisions, formalized invariants, and the distinction between
execution, validation, and truth.

Factory can therefore be treated as:

- a product and architecture precedent for operational execution;
- a possible external substrate behind an explicit adapter;
- a source of control-plane, analytics, and asynchronous-work patterns.

It must not become the implicit authority owner for DomainSpec, Arcanum, cyberAlchemy-v2, or Lean.

## Recommended Follow-Up

Evaluate three bounded bridges in this order:

1. `execution projection`: determine whether one approved work-pack can become a Mission without
   losing owner, gate, context, acceptance criteria, or non-goals;
2. `receipt bridge`: define how execution results, costs, failures, retries, and interventions
   return to Arcanum without being mistaken for promotion evidence;
3. `policy projection`: determine whether authority kinds and protected boundaries can become
   executable agent controls without transferring lifecycle authority.

The smallest useful experiment is one work-pack, one primary capability, one supporting agent,
and one final receipt. Its question is whether the projection preserves our contracts, not
whether the platform can generate code.

## Risks And Evidence Limits

- Factory is proprietary; public documentation cannot establish its complete internal model.
- Some Software Factory surfaces are described as preview-stage and should not be treated as
  stable integration contracts without a current product check.
- Capabilities declared in our READMEs are not automatically evidence of a fully delivered
  production runtime.
- A runtime adapter could accidentally let operational success impersonate semantic validation
  or promotion authority.
- No valid multi-agent robot-talks investigation was run for the initial comparison; the result
  is a bounded single-agent synthesis over the cited sources.
- The local Inventory contained zero exact `Factory.ai` or `Factory Adapter` entries at lookup
  time. That is absence from the index, not proof of absent repository knowledge.
- Inventory projection validation was not completed because the local Bash command attempted to
  start a broken WSL environment.

## Context Builder Selection

| Obligation | Coverage | Selected source | Why it matters |
| --- | --- | --- | --- |
| O1: compare the systems at high level | covered | source conversation and cited public Factory docs | establishes the layer distinction |
| O2: carry reusable Factory capabilities | covered | Missions, subagents, controls, and analytics docs | supplies the operational findings |
| O3: carry our differentiated capabilities | covered | DomainSpec, Arcanum, cyberAlchemy-v2, and Lean READMEs | supplies the internal findings |
| O4: explain where and how Factory helps | covered | candidate projections in this handoff | gives Vladimir actionable integration seams |
| O5: preserve evidence and ownership limits | covered | repository rules and explicit risk section | prevents adoption claims and authority collapse |
| O6: provide multi-agent confirmation | unresolved | no valid robot-talks dispatch exists | requires independent review, not concealment |

Strict coverage: `flag`. This is sufficient for a research-direction review, not for mutation or
adoption.

## Selected Session Context

- The user requested a high-level comparison focused on reusable Factory capabilities, our
  differentiators, and concrete integration value.
- Factory sources were read as operational platform evidence.
- Local repository READMEs were read as declarations of current architecture, status, and scope.
- The first attempted handoff was rejected because it delegated the research again instead of
  carrying the findings. This artifact carries the findings directly.

## Excluded Context

| Candidate | Reason excluded |
| --- | --- |
| whole conversation transcript | not obligation-linked and too broad |
| previous premature handoff artifact | wrong process and incomplete content transfer |
| claim that Factory definitively lacks our mechanisms | unsupported by public-source research |
| immediate Factory Adapter implementation | no architecture or adoption decision exists |
| detailed Lean theorem development | unnecessary for the high-level integration decision |

## Target Boundary

- In scope: review the findings, correct unsupported claims, and decide whether the smallest
  adapter experiment deserves a governed research or design route.
- Out of scope: implementation, procurement, deployment, definition promotion, authority change,
  public disclosure of private material, and claims of novelty.
- Prior decisions to preserve: external execution may consume an approved contract but may not
  silently become its semantic, lifecycle, or promotion owner.

## Gaps And Blockers

| Gap | Owner | Status | Next action |
| --- | --- | --- | --- |
| public docs cannot prove Factory's complete capability boundary | research owner | open | qualify all negative comparisons |
| no independent attack of the synthesis yet | review dispatch | open | run the requested two-agent review |
| no adapter contract or experiment preregistration | Vladimir / next route | deferred | decide after review |
| no stable source-conversation artifact | Invoke | open | use this handoff as bounded session evidence |
| prior incorrect handoff remains on disk | parent/human | open | supersede or remove only with explicit approval |

## Next-Session Start Prompt

```text
Review the transferred Factory.ai comparison in this handoff. Treat its factual claims as bounded
by the cited public documentation and local READMEs. Attack the complementarity thesis, the
proposed layer mapping, and the three bridge recommendations. Drop refuted findings, preserve
owner boundaries, and recommend either: no further work, a narrower research question, or one
bounded adapter experiment. Do not implement from this handoff.
```

## Dispatch Technique Trace

- `frame_handoff`: carries a bounded synthesis instead of the full conversation.
- `handle_handoff`: points to owner-held local and public sources.
- `residue_ledger`: records missing independent review and environment validation residue.
- `owner_boundary_check`: prevents runtime execution from acquiring semantic or promotion authority.
- `protected_context_flag`: keeps private project material inside the authorized repository context.
- `concrete_path_evidence`: binds the synthesis to inspectable source handles.

## Provenance

Internal sources:

- `README.md`
- `arcanum/README.md`
- `cyberAlchemy-v2/README.md`
- `../domainspec-lean-formalization/README.md`
- `.agents/skills/invoke/SKILL.md`
- `.agents/skills/invoke/handoff.md`
- `.agents/skills/invoke/templates/session-handoff/session-handoff.md`

Factory public sources inspected on 2026-08-19:

- https://factory.ai/
- https://factory.ai/product/software-factory
- https://factory.ai/news/missions
- https://docs.factory.ai/missions/overview
- https://docs.factory.ai/harness/subagents
- https://docs.factory.ai/enterprise/hierarchical-settings-and-org-control
- https://docs.factory.ai/enterprise/llm-safety-and-agent-controls
- https://docs.factory.ai/enterprise
- https://docs.factory.ai/api-reference/analytics

- Context Builder mode: `standard`, dry-run selection
- Evidence date: 2026-08-20
- Output path: `sessions/2026-08-20-1150-factory-ai-vladimir-handoff.md`

## Gate Result

- Status: `flag`
- Reason: the findings are transferred with bounded evidence, but independent review and an
  adoption or adapter decision are still open.
- Recommended next route: two-agent `review`, then `research`, `invoke design`, or `deferred`
- Mutation authority: none

