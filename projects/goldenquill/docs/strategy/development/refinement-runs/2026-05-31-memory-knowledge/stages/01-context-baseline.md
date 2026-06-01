# Stage 01 - Context Builder Evidence Baseline

Status: pass, locally materialized.

The repository has a fragmented but substantial memory/knowledge layer:

- `MEMORY.md` is the workspace memory index and wake-up memory map.
- `pipeline/memory/unified_query.py` is a read-only retrieval registry across workspace and per-org registers.
- `pipeline/cli/tilth_memory_query.py` exposes operator query/list/inspect.
- `pipeline/memory/consolidate_index.py` and `auto_consolidate_trigger.py` handle MEMORY.md threshold/consolidation.
- `pipeline/cards/` contains signed reusable knowledge artifacts.
- `pipeline/knowledge_packs/` contains sector terminology packs.
- `pipeline/vault/*query_skill.py` exposes gated read skills.
- `golden_quill_substrate/memory.py` and contracts prototype memory mutation constraints.
- Reflection Packet is spec-locked/dormant for cross-cycle learning.

Live checks passed for list-registers, query, and memory size. `logfire` is not installed, so CLI calls emit an observability warning while still succeeding.

