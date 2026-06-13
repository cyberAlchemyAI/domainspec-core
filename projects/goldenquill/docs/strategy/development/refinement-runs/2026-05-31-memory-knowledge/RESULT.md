---
title: Memory And Knowledge Handling Refine Result
date: 2026-05-31
mode: refine-full
status: pass-with-flags
---

# Refine Result

## Outcome

GoldenQuill's memory/knowledge layer is already partly implemented, but not yet governed as one production layer. The right production direction is a Memory/Knowledge Mesh over existing surfaces, not a new memory subsystem from scratch.

## Current Layer Map

| Surface | Current Role | Maturity Signal | Design Implication |
| --- | --- | --- | --- |
| `MEMORY.md` | Workspace memory index | live wake-up source; under threshold today | Keep as navigation index, not retrieval database |
| `pipeline/memory/unified_query.py` | Read-only multi-register retrieval | live CLI query/list passed | Treat as primary read API |
| `pipeline/memory/consolidate_index.py` | MEMORY.md consolidation writer | tested threshold/hash-pin behavior | Keep as index hygiene, not semantic memory |
| `lessons.md` + `pipeline/institutional_memory/lessons.json` | Operator-curated institutional memory | canonical human/machine pair | Writes require operator approval |
| `pipeline/cards/` | Signed reusable shareable knowledge | asset-signed; loader injection future | Keep distinct from per-org memory |
| `pipeline/knowledge_packs/` | Sector terminology and funder dialect hints | loader exists; Scribe wiring separate | Use through policy/admin-risk gates |
| `pipeline/vault/*query_skill.py` | Gated file reads | FDBroker path and identity tuple | Use for authoritative persisted state |
| `golden_quill_substrate/memory.py` | Prototype memory mutation gate | contract-level prototype | Reuse invariants, not implementation as-is |
| Reflection Packet | Cross-cycle learning producer | spec-locked/dormant | Activate after promotion rules are explicit |

## Improvement Candidates

1. `docs/MEMORY_KNOWLEDGE_LAYER_INDEX.md` current-truth index.
2. Refresh docstrings/docs from "13 registers" to the live 15-register query surface.
3. Add a query-surface parity test that asserts documented register count equals `ALL_REGISTERS`.
4. Define `MemoryEvidencePacket` / Arcanum `EvidenceCard` handoff shape for query results.
5. Add an authority classifier for retrieval results: workspace-shared, per-org, signed, candidate, dormant, historical.
6. Design Reflection Packet activation only after source/promotion rules and operator approval flow are explicit.

## Final Synthesis

The layer should be designed as:

`retrieve -> classify authority -> cite provenance -> decide promotion -> hand off to owner`.

That chain works with Arcanum because it lets Inventory package evidence, Ontology govern meaning, Invoke author designs/plans, Logician enforce gates, and Task Session execute bounded changes without collapsing ownership.
