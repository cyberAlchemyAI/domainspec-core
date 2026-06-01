---
title: GoldenQuill Memory And Knowledge Handling Research Synthesis
date: 2026-05-31
status: synthesized
---

# Memory And Knowledge Handling Research Synthesis

## Main Finding

The repository already contains a serious memory and knowledge-handling substrate, but it is spread across multiple authority layers. The production gap is not "no memory." The gap is a missing current-truth model that tells agents which memory/knowledge surface to use, what authority it has, how retrieval is proven, and how candidate evidence becomes canonical.

## Layers Found

| Layer | Primary Paths | Role | Authority |
| --- | --- | --- | --- |
| Workspace memory index | `MEMORY.md`, `docs/AGENT_CONTEXT_INDEX.md` | Wake-up memory map and repository navigation | Human-maintained; canonical as index only |
| Institutional lessons | `lessons.md`, `pipeline/institutional_memory/lessons.json` | Operator-confirmed recurring lessons | Canonical only after operator confirmation |
| Unified retrieval | `pipeline/memory/unified_query.py`, `pipeline/cli/tilth_memory_query.py` | Read-only BM25 retrieval across registers | Retrieval/provenance authority, not write authority |
| Memory hygiene | `pipeline/memory/consolidate_index.py`, `pipeline/memory/auto_consolidate_trigger.py`, `scripts/memory_size_check.sh` | Keep `MEMORY.md` below loader limits | Operational utility |
| Vault read skills | `pipeline/vault/vault_query_skill.py`, `pipeline/vault/research_db_query_skill.py` | Gated file access and identity tuple preservation | Vault-owned read authority |
| Cards | `pipeline/cards/` | Signed shareable domain/product knowledge | Signed asset, not per-org memory |
| Knowledge packs | `pipeline/knowledge_packs/`, `pipeline/seats/scribe/knowledge_packs.py` | Sector terminology and dialect facts | Candidate/scaffolded drafting support |
| Substrate memory contract | `golden_quill_substrate/memory.py`, `golden_quill_substrate/contracts.py`, `golden_quill_substrate/logician.py` | Memory mutation invariants | Prototype contract authority |
| Reflection Packet | `pipeline/blueprint/v0.1/section_16_reflection_packet.md`, packet gates | Cross-cycle learning and lessons proposal | Spec-locked/dormant producer |

## Live Checks

- `tilth_memory_query list-registers` returned 15 registers.
- `tilth_memory_query query` returned ranked, path-provenance results under `local-only`.
- `scripts/memory_size_check.sh` reported `MEMORY.md` under threshold.
- `logfire` is missing, so observability is degraded but not query-blocking.

## Production Gaps

- Current-truth docs are stale relative to live memory CLI behavior.
- CLI/docstrings use both 13-register and 15-register language.
- Per-org registers are structurally supported but absent in this checkout without an org slug.
- Reflection Packet is not activated as the runtime cross-cycle learning producer.
- Knowledge packs and cards need clear consumption boundaries before they shape outputs.
- No Arcanum handoff packet exists for exporting GoldenQuill query results as non-authoritative evidence cards.

## Recommended First Task

Create `docs/MEMORY_KNOWLEDGE_LAYER_INDEX.md` before implementing new memory behavior. It should map every surface by:

- scope,
- authority,
- mutability,
- maturity,
- retrieval path,
- mutation path,
- approval requirements,
- Arcanum equivalent,
- next-route owner.

