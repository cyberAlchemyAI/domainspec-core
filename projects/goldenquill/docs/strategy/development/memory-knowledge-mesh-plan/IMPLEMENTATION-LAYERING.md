# Memory / Knowledge Mesh Implementation Layering

Date: 2026-05-31
Invoke mode: plan
Source design: `docs/strategy/goldenquill_memory_knowledge_invoke_design_2026-05-31.md`
Refine source: `docs/strategy/development/refinement-runs/2026-05-31-memory-knowledge/RESULT.md`

## Purpose

Turn Golden Quill's existing memory and knowledge surfaces into a production-ready layer without collapsing different authority classes into one vague "memory" bucket.

This plan keeps the first implementation unit documentation-only, then moves through validation parity, evidence packets, and Reflection Packet activation.

## Layer Map

| Layer | Name | Outcome | Entry Gate | Exit Gate |
| --- | --- | --- | --- | --- |
| L0 | Current-truth index | One repo-local map of memory and knowledge surfaces, authority, mutation path, and validation | Existing research/design artifacts present | `docs/MEMORY_KNOWLEDGE_LAYER_INDEX.md` exists and passes static review |
| L1 | Retrieval parity | Register counts and query docs match runtime behavior | L0 complete | memory CLI smoke passes and docs no longer claim stale register counts |
| L2 | Evidence packet contract | A portable packet shape for traceable memory/knowledge retrieval | L1 complete | JSON schema and at least one fixture validate |
| L3 | Authority classifier | Clear canonical vs derived vs proposal-only classification before retrieval enters drafting | L2 complete | classifier design maps each layer-index surface to allowed read/write actions |
| L4 | Reflection activation | Reflection Packet becomes a governed consumer of memory evidence, not a dormant concept | L3 complete | activation brief names gates, failure modes, and first experiment corpus |

## Progressive Hardening

L0 is intentionally small. It creates shared language and reduces duplicate rediscovery.

L1 aligns documentation with live CLI output. This includes the known `13 registers` vs `15 registers` drift.

L2 introduces `MemoryEvidencePacket` as an Arcanum-compatible object:

- evidence excerpt path and optional line span
- authority class
- org boundary scope
- retrieval source
- freshness signal
- mutation permission
- downstream consumer

L3 and L4 should not begin until L2 has at least one validated fixture. Reflection Packet activation is too easy to overstate without a packet contract.

## Active Layer Window

Current active layer: L0.

Allowed now:

- create memory/knowledge layer index
- validate with static grep and live memory CLI
- record blockers for later layers

Deferred:

- code mutation outside docstring/count parity
- new runtime classifiers
- Reflection Packet dispatch integration

