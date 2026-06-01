# Memory / Knowledge Layer Index

Date: 2026-05-31
Status: current-truth index

## Purpose

Golden Quill has several memory and knowledge surfaces, each with different authority. This index makes those boundaries explicit so future work can retrieve evidence, mutate state, and design Reflection Packet behavior without flattening everything into one vague memory layer.

No client org context was read for this index.

## Authority Classes

| Class | Meaning |
| --- | --- |
| canonical_source | File directly governs behavior or workspace law |
| signed_contract | Locked/signed spec, policy, card, router, or contract |
| runtime_index | Query/index layer derived from underlying files |
| derived_summary | Human-readable synthesis that must trace to source |
| proposal_only | Design or patch proposal with no mutation authority |
| generated_state | Runtime/session output; not canonical by default |
| absent_current_checkout | Named surface not present in this checkout |

## Surface Index

| Surface | Paths | Authority | Mutation | Retrieval / Validation | Arcanum Equivalent |
| --- | --- | --- | --- | --- | --- |
| Workspace laws and operator context | `SOUL.md`, `USER.md`, `AGENTS.md` | canonical_source | read-only except Save-On-Decide rules | wake-up read; compaction re-read | constitution-governance |
| Model and seat routing | `router.yaml` | signed_contract | explicit router edit only | direct read before model assumptions | dispatch-spec route binding |
| Memory index | `MEMORY.md` | canonical_source | append/consolidate through memory discipline | `scripts/memory_size_check.sh`; `pipeline.cli.tilth_memory auto-trigger` | inventory index |
| Lessons memory | `lessons.md`, `pipeline/institutional_memory/lessons.json` | canonical_source plus machine mirror | append or increment per Save-On-Decide | direct read; JSON mirror validation | definitions-governance plus inventory |
| Consolidation trigger | `scripts/memory_size_check.sh`, `pipeline/memory/auto_consolidate_trigger.py`, `pipeline/memory/consolidate_index.py` | runtime_index | script/code task only | preflight threshold check; log at `pipeline/institutional_memory/memory_consolidation_log.jsonl` | observability-setup plus workflow-reflect |
| Unified memory query | `pipeline/memory/unified_query.py`, `pipeline/cli/tilth_memory_query.py` | runtime_index | code task with tests | `python3 -m pipeline.cli.tilth_memory_query --format json list-registers` | inventory query surface |
| Agent context index | `docs/AGENT_CONTEXT_INDEX.md` | derived_summary | docs task | path-cited review | context-builder |
| Cards | `pipeline/cards/`, `pipeline/cards/_schema/`, `pipeline/cards/loader.py`, `pipeline/cards/validators.py` | signed_contract | card ceremony or schema task | card validators and lock/signing records | ontology-vault plus definitions-governance |
| Knowledge packs | `pipeline/knowledge_packs/`, `pipeline/seats/scribe/knowledge_packs.py` | runtime_index over curated terminology | code/data task | loader and prompt assembly checks | feature-glossary plus context-builder |
| Vault query helpers | `pipeline/vault/vault_query_skill.py`, `pipeline/vault/research_db_query_skill.py` | runtime_index | code task | query helper smoke or targeted tests | inventory plus ontology-vault |
| Vault policy layer | `pipeline/vault/policies/`, including `reflection_packet.cedar` | signed_contract | policy task with gate validation | Cedar/policy gate checks | constitution-governance |
| Substrate memory contracts | `golden_quill_substrate/memory.py`, `golden_quill_substrate/contracts.py`, `golden_quill_substrate/logician.py` | canonical_source | code task with tests | contract tests and Logician checks | task-session execution substrate |
| Reflection Packet specification | `pipeline/blueprint/v0.1/section_16_reflection_packet.md`, `pipeline/blueprint/v0.1/section_04_v2_x_y_packet_amendment.md`, `pipeline/blueprint/v0.1/section_04_v2_x_y_1_packet_bodies_amendment.md` | signed_contract | blueprint amendment path only | blueprint/policy consistency checks | residuality-spec plus signal-observer |
| Reflection Packet runtime | `pipeline/vault/policies/reflection_packet.cedar` plus blueprint references | proposal_only for activation | blocked until activation task | currently dormant as production consumer | workflow-reflect |
| Daily logs | `daily_logs/` | absent_current_checkout | not available in current checkout | AGENTS expects it, but directory is absent here | observability trail |
| Org project contexts | `orgs/<slug>/PROJECT_CONTEXT.md` | canonical_source per org | single-org only | not loaded for this task | context-builder with Law 3 gate |

## Current Truth Notes

- The live memory query CLI reports 15 registers in this checkout.
- Some text still describes the query surface as 13 registers; parity work is planned but blocked on a runnable test surface.
- `MEMORY.md` is under the early-warning threshold in the current preflight.
- The memory query CLI emits a `logfire not installed` warning in this shell; retrieval still works, observability is degraded.
- No client org context was loaded. Law 3 remains intact.
- `daily_logs/` is required by workspace wake-up instructions but is absent in this checkout.

## Production Risks

1. Authority flattening: retrieval could treat proposal-only or generated files as canonical.
2. Stale count drift: docs can fall out of sync with the runtime register set.
3. Reflection overclaim: Reflection Packet has blueprint/policy presence but not a fully active production consumer path.
4. Observability degradation: missing `logfire` weakens traces for memory queries.
5. Test unavailability: code-adjacent memory work cannot be production-claimed until the test runner is restored or substitute validation is approved.

## Improvement Candidates

1. Add a `MemoryEvidencePacket` fixture and validation path.
2. Add register-count parity tests for `tilth_memory_query`.
3. Add an authority classifier before memory evidence enters drafting.
4. Create a Reflection Packet activation experiment using only non-org, public repository evidence.
5. Add an index freshness check that fails when `MEMORY.md` and CLI register descriptions diverge.

## Arcanum Compatibility

| Arcanum Capability | Golden Quill Mapping |
| --- | --- |
| Inventory | `MEMORY.md`, memory CLI, layer index |
| Ontology Vault | cards, classifications, blueprint definitions |
| Definitions Governance | lessons, terms, posture vocabulary, register descriptions |
| Decision Gate | mutation approval, org isolation, Reflection Packet activation |
| Task Session | bounded SWUs with validation and blocker records |
| Residuality Spec | degraded behavior under missing observability/test surfaces |
| Signal Observer | future Reflection Packet and memory query telemetry |

