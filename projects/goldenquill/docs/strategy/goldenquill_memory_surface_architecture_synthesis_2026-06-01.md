---
title: GoldenQuill Memory Surface Architecture Synthesis
date: 2026-06-01
status: refined-synthesis
source_context:
  - docs/MEMORY_KNOWLEDGE_LAYER_INDEX.md
  - docs/strategy/goldenquill_memory_knowledge_research_synthesis_2026-05-31.md
  - docs/strategy/goldenquill_memory_knowledge_invoke_design_2026-05-31.md
---

# Memory Surface Architecture Synthesis

## Core Finding

Yes: Golden Quill has many memory surfaces. That is not automatically a problem. The problem is that the surfaces are not yet unified by a first-class architectural contract that tells agents:

- which surface to consult,
- what authority that surface has,
- whether the result is canonical, signed, derived, generated, proposal-only, or absent,
- how the result may be used as context,
- how a candidate insight becomes durable memory,
- and which owner is allowed to mutate it.

The repository does not need a brand-new monolithic memory store first. It needs a Memory Context Architecture: a routing, authority, and evidence-packet layer over the memory and knowledge surfaces already mapped.

## What We Mapped

| Surface Family | Existing Anchors | Current Role | Architecture Risk |
| --- | --- | --- | --- |
| Workspace canonical context | `SOUL.md`, `USER.md`, `AGENTS.md`, `router.yaml` | Laws, operator model, routing truth | Agents may remember these narratively instead of rereading canonical files |
| Memory index | `MEMORY.md`, `docs/AGENT_CONTEXT_INDEX.md` | Wake-up and context navigation | Index can become stale or overbroad |
| Lessons memory | `lessons.md`, `pipeline/institutional_memory/lessons.json` | Operator-confirmed recurring lessons | Lessons can be confused with source truth |
| Unified memory query | `pipeline/memory/unified_query.py`, `pipeline/cli/tilth_memory_query.py` | Retrieval across registers with provenance | Retrieval may be treated as authority rather than evidence |
| Memory hygiene | `scripts/memory_size_check.sh`, `pipeline/memory/auto_consolidate_trigger.py`, `pipeline/memory/consolidate_index.py` | Keeps memory loadable and consolidated | Hygiene checks are not yet tied to architecture readiness |
| Cards | `pipeline/cards/`, `pipeline/cards/_schema/`, validators | Signed shareable domain/product knowledge | Signed reusable knowledge can be mistaken for per-org context |
| Knowledge packs | `pipeline/knowledge_packs/`, `pipeline/seats/scribe/knowledge_packs.py` | Terminology and sector framing | Packs can bias writing if not scoped and cited |
| Vault query helpers | `pipeline/vault/vault_query_skill.py`, `pipeline/vault/research_db_query_skill.py` | Gated read access and identity preservation | Query helper outputs need explicit context packaging |
| Substrate contracts | `golden_quill_substrate/memory.py`, `golden_quill_substrate/contracts.py`, `golden_quill_substrate/logician.py` | Memory mutation and Logician invariants | Prototype authority exists but is not yet the front door for all memory mutation |
| Reflection Packet | `pipeline/blueprint/v0.1/section_16_reflection_packet.md`, `pipeline/vault/policies/reflection_packet.cedar` | Cross-cycle learning design | Dormant runtime status can be overclaimed |
| Org project contexts | `orgs/<slug>/PROJECT_CONTEXT.md` | Single-org source truth | Law 3 breach if memory routing crosses orgs |

## Better Architecture Shape

The better architecture is not "one memory." It is a layered memory context system:

```text
Canonical Sources
  SOUL / USER / router / PROJECT_CONTEXT / RFA / signed cards / locked specs
        |
        v
Memory Surface Registry
  current map of surfaces, authority class, owner, read path, write path
        |
        v
Retrieval Gateway
  local-only query, register filters, org boundary checks, provenance
        |
        v
Authority Classifier
  canonical_source | signed_contract | runtime_index | derived_summary
  proposal_only | generated_state | absent_current_checkout
        |
        v
Memory Evidence Packet
  query + source path + locator + authority + allowed uses + promotion owner
        |
        v
Consumers
  Scout / Scribe / Judge / Logician / Context Builder / Arcanum Inventory
        |
        v
Promotion Gate
  operator approval, Logician validation, card ceremony, lessons update,
  org vault route, or decision gate
        |
        v
Reflection Packet
  proposes future memory deltas; does not silently write canonical memory
```

This architecture lets every agent use memory aggressively as context while staying conservative about authority.

## Context Reference Contract

Every retrieved memory item should move through the architecture as a context reference, not as loose prose.

Minimum contract:

```json
{
  "source_path": "path/to/source.md",
  "locator": "line range, key, section, or register id",
  "authority_class": "canonical_source | signed_contract | runtime_index | derived_summary | proposal_only | generated_state",
  "org_scope": "workspace_global | single_org | no_org_loaded | cross_org_forbidden",
  "allowed_uses": ["orient", "cite", "draft_support", "decision_input", "promotion_candidate"],
  "promotion_owner": "operator | logician | card_ceremony | lessons_memory | org_vault | decision_gate | none",
  "freshness_signal": "live_check | dated_snapshot | signed_lock | generated_run | absent_current_checkout"
}
```

This is the missing bridge between "we found relevant context" and "the architecture may safely use this context."

## How The Whole Architecture Should Use It

### 1. Wake-up Uses Canonical Context Only

Wake-up should continue reading canonical files directly:

- `SOUL.md`
- `USER.md`
- `router.yaml`
- `MEMORY.md`
- `lessons.md`
- task-specific `PROJECT_CONTEXT.md` only when an org is named

Memory query can help find relevant context, but it should not replace canonical wake-up reads.

### 2. Planning Uses Evidence Packets

Planning agents should query memory and receive `MemoryEvidencePacket` outputs. Plans should cite packets by path and authority class. This prevents stale summaries from quietly becoming source truth.

### 3. Drafting Uses Allowed Uses, Not Raw Retrieval

Scribe and related drafting flows should not ingest all memory hits equally. A result from a signed card, a lesson, a knowledge pack, and a proposal-only design should have different allowed uses.

Example:

- signed card: reusable domain framing, within card scope
- PROJECT_CONTEXT: org-specific claims
- knowledge pack: terminology support, not factual claim source
- research synthesis: orientation only unless backed by cited paths
- Reflection Packet proposal: never canonical until approved

### 4. Logician Enforces Promotion Boundaries

The Logician should not merely validate final outputs. It should also reject memory misuse:

- generated state used as canonical source,
- proposal-only design used as production authority,
- cross-org context reference,
- unsigned card mutation,
- Reflection Packet writing directly to lessons memory,
- retrieval result without source path.

### 5. Reflection Packet Becomes A Producer, Not A Store

Reflection Packet should become the cross-cycle learning producer. It should propose deltas such as:

- new lesson candidate,
- stale register warning,
- card update candidate,
- knowledge pack drift candidate,
- operator decision candidate,
- task-session residue.

It should not be the durable memory store. Durable writes still belong to lessons, cards, org vault, router, or other owning surfaces.

## Improvement Candidates

### P0: Memory Surface Registry

Promote `docs/MEMORY_KNOWLEDGE_LAYER_INDEX.md` into a maintained registry contract.

Add:

- stable IDs for each surface,
- authority class,
- owner,
- read command,
- write command,
- validation command,
- freshness check,
- Arcanum equivalent.

Why: every other improvement depends on knowing which surface is allowed to mean what.

### P1: MemoryEvidencePacket

Implement the packet shape first as JSON fixtures and validation, then wire retrieval outputs into it.

Why: the architecture needs a portable unit of context reference that can move through Context Builder, Invoke, Task Session, and Scribe without losing authority.

### P1: Authority Classifier

Add a pure classifier that labels retrieval results before any consumer sees them.

Why: retrieval rank is not the same as truth. A high-ranking proposal-only artifact must not outrank a lower-ranking canonical file.

### P1: Register Parity Guard

Fix and test the known `13 registers` vs `15 registers` drift.

Why: if the retrieval front door lies about its own register set, agents cannot trust architecture-facing docs.

### P2: Context Reference Gate In Logician

Teach Logician to validate context references on drafting and promotion surfaces.

Why: Law 1 and Law 3 are easier to enforce when every memory input carries source path, authority, and org scope.

### P2: Reflection Packet Activation Experiment

Run Reflection Packet only on non-org repository evidence first.

Experiment:

- input: task-session reports and validation logs,
- output: proposed lessons or registry drift candidates,
- gate: no direct write to `lessons.md`,
- success: useful candidate with exact owner and evidence path.

Why: activates cross-cycle learning safely without risking client-data or authority drift.

## Arcanum Alignment

| Arcanum Capability | Golden Quill Use |
| --- | --- |
| Inventory | Package context references and retrieval evidence |
| Ontology Vault | Govern meaning, roles, and authority classes |
| Definitions Governance | Keep memory vocabulary stable |
| Decision Gate | Resolve unclear promotion ownership |
| Task Session | Execute bounded memory improvements |
| Residuality Spec | Define degraded behavior when observability/tests are missing |
| Workflow Reflect | Consume Reflection Packet signals after approval |

Arcanum should not replace Golden Quill authority. It should provide the governance vocabulary and artifact discipline for how Golden Quill memory evidence moves.

## Production Readiness Path

1. Keep `docs/MEMORY_KNOWLEDGE_LAYER_INDEX.md` as the current map.
2. Add `memory_surface_registry.json` generated from or synchronized with the index.
3. Add `MemoryEvidencePacket` schema, fixture, and validator.
4. Update memory query output to optionally emit evidence packets.
5. Add authority classifier.
6. Add Logician gate for context-reference misuse.
7. Activate Reflection Packet as proposal-only producer.
8. Add operator approval routes for each promotion owner.

## Final Synthesis

The repository already has enough memory infrastructure to support a serious architecture. The missing layer is not storage; it is context authority.

Better architecture means every memory/knowledge surface becomes a named, governed context reference source. Retrieval finds candidates. Authority classification says what they are. Evidence packets carry them. Consumers use them within allowed scope. Promotion gates decide whether they become durable memory. Reflection proposes improvements, but owners approve mutations.

That shape preserves Golden Quill's sovereignty and Law 3 isolation while making the whole architecture much smarter at reusing what it already knows.
