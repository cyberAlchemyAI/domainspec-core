# Stage 07 - Interrogation Design Review

Status: flag, locally materialized.

Review:

- The design must name `tilth_memory_query` as live read-only retrieval.
- It must avoid making Arcanum Inventory canonical authority for GoldenQuill facts.
- It must avoid making Ontology responsible for storage or retrieval.
- It must avoid enabling cross-org query expansion.
- It must require operator approval for learning/memory writes.
- It must keep cards as signed shareable knowledge, not per-org memory.

Flag:

The repository's current truth docs need refresh. A design may be correct while the human-facing docs still tell an older story.
