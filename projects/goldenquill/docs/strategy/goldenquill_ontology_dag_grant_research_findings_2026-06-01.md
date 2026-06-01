---
title: GoldenQuill Ontology DAG Grant Research Findings Ledger
date: 2026-06-01
status: synthesized-research-ledger
dispatch: docs/strategy/goldenquill_ontology_dag_grant_research_strategy_2026-06-01.dispatch.json
---

# GoldenQuill Ontology DAG Grant Research Findings Ledger

## Scope

Research question: how should GoldenQuill adapt an ontology-backed DAG model to
grant writing, using Ontology Vault, existing GoldenQuill memory/vault/agent
surfaces, patterns from `domainspec-lean-formalization`, and the Paradigma
"New Age of Research" reference.

This was a read-only research pass. No production schema, card, memory,
ontology, or org-vault mutation is authorized by this ledger.

## Dispatch Receipts

| Lane | Status | Receipt |
| --- | --- | --- |
| GQ1 memory/vault/contracts | complete; late receipt folded in | Memory/vault/card/substrate receipt returned after first synthesis draft; ledger updated with card graph and MemoryEvidencePacket details. |
| GQ2 grant workflow/agents | complete | Scout/Scribe/Editor/Judge/Logician workflow receipt returned with path-cited evidence. |
| OV1 Ontology Vault mapping | complete | Ontology Vault branch-aware mapping receipt returned with path-cited evidence. |
| LF1 Lean-formalization transfer | complete | Transfer pattern receipt returned with path-cited evidence. |
| VAL1 toy validation | complete | Toy validation receipt returned with path-cited evidence and proposed commands. |

## GQ1: Memory, Vault, Cards, Evidence, Contracts

### Findings

- GoldenQuill already distinguishes authority classes for memory and knowledge
  surfaces: `canonical_source`, `signed_contract`, `runtime_index`,
  `derived_summary`, `proposal_only`, `generated_state`, and
  `absent_current_checkout` in
  `projects/goldenquill/docs/MEMORY_KNOWLEDGE_LAYER_INDEX.md:12-22`.
- The existing surface index already maps Arcanum equivalents: memory query maps
  to Inventory, cards/classifications/blueprints map to Ontology Vault,
  decision-gate maps to mutation approval/org isolation/Reflection Packet
  activation, and signal-observer maps to future Reflection Packet telemetry:
  `projects/goldenquill/docs/MEMORY_KNOWLEDGE_LAYER_INDEX.md:70-80`.
- The memory surface architecture already names the missing bridge as a
  `MemoryEvidencePacket`, not a new monolithic memory store. It requires
  `source_path`, `locator`, `authority_class`, `org_scope`, `allowed_uses`,
  `promotion_owner`, and `freshness_signal`:
  `projects/goldenquill/docs/strategy/goldenquill_memory_surface_architecture_synthesis_2026-06-01.md:42-101`.
- A narrower `MemoryEvidencePacket` schema already exists under the
  memory-knowledge mesh plan. It requires `packet_id`, `created_utc`,
  `source_path`, `authority_class`, `org_scope`, `retrieval_surface`,
  `freshness_signal`, `mutation_permission`, and `downstream_consumer`, but not
  `allowed_uses` or `promotion_owner` as first-class fields:
  `projects/goldenquill/docs/strategy/development/memory-knowledge-mesh-plan/schema/memory_evidence_packet.schema.json:7-17`.
- The corresponding work pack marks the fixture, authority classifier,
  Reflection Packet activation experiment, and readiness report as pending:
  `projects/goldenquill/docs/strategy/development/memory-knowledge-mesh-plan/WORK-PACK.md:37-46`.
- GoldenQuill's read-only memory query registry preserves provenance and Law 3
  isolation across 15 registers:
  `projects/goldenquill/pipeline/memory/unified_query.py:1-63`.
  Per-org registers require an explicit org and are skipped when no org is
  supplied: `projects/goldenquill/pipeline/memory/unified_query.py:1229-1269`.
- Vault read helpers are already scoped through brokered, nonce-bearing read
  requests, with identity tuple preservation:
  `projects/goldenquill/pipeline/vault/vault_query_skill.py:1-12` and
  `projects/goldenquill/pipeline/vault/vault_query_skill.py:72-95`.
- Research DB reads reject absolute paths, `..`, `orgs/`, and caller-supplied
  `vault_shared/` or `research_db/` prefixes before broker access:
  `projects/goldenquill/pipeline/vault/research_db_query_skill.py:9-20` and
  `projects/goldenquill/pipeline/vault/research_db_query_skill.py:58-72`.
- Substrate contracts already name relevant operation and resource types:
  `evidence.intake`, `evidence.promote`, `OPPORTUNITY`, `RFA`, `DRAFT`,
  `EVIDENCE`, `MEMORY_RECORD`, and `AUDIT_EVENT` in
  `projects/goldenquill/golden_quill_substrate/contracts.py:82-111`.
- The substrate already has claim/evidence structures: `CitationAnchor`,
  `ProposedClaim`, `RetrievalRequestPayload`, and `EvidenceItem` in
  `projects/goldenquill/golden_quill_substrate/contracts.py:387-410` and
  `projects/goldenquill/golden_quill_substrate/contracts.py:482-510`.
- Retrieval bundles enforce canonical order, max item/token bounds, and
  cross-boundary evidence rejection:
  `projects/goldenquill/golden_quill_substrate/contracts.py:550-563`.
- Scout Channel G already has DAG-like ingredients: opportunity records,
  evidence items, and deterministic import/source/opportunity ids in
  `projects/goldenquill/pipeline/scout/_channel_g_types.py:81-120` and
  `projects/goldenquill/pipeline/scout/_channel_g_parser.py:297-306`.
- Cards are the richest existing ontology-like source. CIC card models encode
  applicant-side runtime knowledge while CLC card models encode funder-side
  underwriting knowledge:
  `projects/goldenquill/pipeline/cards/models.py:99-138` and
  `projects/goldenquill/pipeline/cards/models.py:143-155`.
- The `research_evidence` CLC card includes research-question underwriting,
  commitment tracking patterns, and runtime verification warnings for volatile
  funder facts:
  `projects/goldenquill/pipeline/cards/CLC/research_evidence.yaml:19-34`,
  `projects/goldenquill/pipeline/cards/CLC/research_evidence.yaml:644-655`,
  and
  `projects/goldenquill/pipeline/cards/CLC/research_evidence.yaml:839-844`.
- Card runtime graphing is named but not live. The loader contract names
  "Build the memory profile (concept graph nodes + edges)" as step 6, while
  v0.1 only runs steps 1-4 and raises `NotImplementedError` at runtime
  registration:
  `projects/goldenquill/pipeline/cards/loader.py:8-20` and
  `projects/goldenquill/pipeline/cards/loader.py:275-280`.
- Card validation is declared but not implemented:
  `projects/goldenquill/pipeline/cards/validators.py:60-74`.
- Reflection Packet is authored but dormant. Its sub-kind module states it is
  not registered at v0.1, and the registry intentionally excludes it until a
  v0.2 first-wave lock:
  `projects/goldenquill/pipeline/vault/sub_kinds/reflection_packets.py:1-17`
  and `projects/goldenquill/pipeline/vault/sub_kinds/registry.py:179-185`.
- Logician blocks AI or direct-human memory/evidence promotion outside the
  state-machine route: evidence promotion requires `STATE_MACHINE_RUNNER`, final
  packet authorization requires a capable human, and memory mutation requires
  `STATE_MACHINE_RUNNER`:
  `projects/goldenquill/golden_quill_substrate/logician.py:5-24`.

### Gaps And Tensions

- The exact graph unit does not exist yet. `MemoryEvidencePacket` is proposed,
  while substrate contracts already have pieces of the shape.
- Retrieval rank is not authority. The architecture synthesis explicitly warns
  that generated state, proposal-only designs, cross-org references, unsigned
  card mutations, and retrieval results without source paths should be rejected
  by Logician:
  `projects/goldenquill/docs/strategy/goldenquill_memory_surface_architecture_synthesis_2026-06-01.md:134-143`.
- Reflection Packet is a producer of proposed deltas, not a durable store:
  `projects/goldenquill/docs/strategy/goldenquill_memory_surface_architecture_synthesis_2026-06-01.md:145-156`.
- The memory index classifies cards as signed-contract surfaces, while the
  unified query card adapter walks `pipeline/cards/**/*.yaml` working content,
  not signed bundles. Retrieval can therefore surface useful card content
  without proving signed-bundle authority:
  `projects/goldenquill/docs/MEMORY_KNOWLEDGE_LAYER_INDEX.md:35` and
  `projects/goldenquill/pipeline/memory/unified_query.py:971-978`.
- There is a likely naming drift risk: the CLC card slug is
  `research_evidence`, while Reflection Packet's closed CLC set uses
  `research_and_evidence`:
  `projects/goldenquill/pipeline/cards/CLC/research_evidence.yaml:21-23`
  and
  `projects/goldenquill/pipeline/vault/sub_kinds/reflection_packets.py:76-86`.
- Matrix/intersection card knowledge would be natural DAG material, but matrix
  cards are forward-compatible only and should remain out of the first graph
  contract.

### DAG Candidates

Node families:

- `memory_surface`
- `source_document`
- `memory_evidence_packet`
- `retrieval_result`
- `citation_anchor`
- `proposed_claim`
- `evidence_item`
- `gate_failure`
- `promotion_candidate`
- `reflection_packet_delta`
- `card_concept`
- `compliance_rule`
- `review_signal`
- `learning_signal`

Edge families:

- `retrieved_from`
- `cited_by`
- `evidenced_by`
- `bounded_by_authority`
- `blocked_by_gate`
- `proposed_for_promotion`
- `rejected_for_authority`
- `same_org_scope_as`
- `classified_by_card`
- `requires_evidence`
- `supersedes`
- `forbidden_for_use`

## GQ2: Grant Workflow And Agent Surfaces

### Findings

- Scout owns discovery and verification, not proposal writing. The skill says
  Scout finds, filters, and presents opportunities, and does not write
  proposals: `projects/goldenquill/skills/scout-discovery/SKILL.md:16-20`.
- The implementation-facing Scout protocol is `DISCOVER -> VERIFY -> REVIEW ->
  operator decides -> Phase 0 Intake`:
  `projects/goldenquill/pipeline/engineering/agents/scout_discovery_agent_v1.md:61-65`.
- Scribe extracts RFA structure before drafting and treats the RFA as ground
  truth: program name, eligibility, activities, award limits, match, deadline,
  review criteria, section limits, required attachments, and key terms:
  `projects/goldenquill/skills/scribe-ghostwriter/SKILL.md:51-65`.
- Scribe has KGIE preflight and section-by-section drafting discipline in the
  engineering prompt:
  `projects/goldenquill/pipeline/engineering/agents/scribe_writer_agent_v1.md:72-108`
  and `projects/goldenquill/pipeline/engineering/agents/scribe_writer_agent_v1.md:111-120`.
- Judge scores against the funder's own rubric first and the internal
  12-dimension rubric second:
  `projects/goldenquill/pipeline/engineering/agents/judge_scoring_agent_v1.md:28-32`
  and `projects/goldenquill/pipeline/engineering/agents/judge_scoring_agent_v1.md:113-120`.
- Judge consumes Scribe's draft manifest rather than recomputing it and builds a
  responsiveness map from RFA requirements to draft sections:
  `projects/goldenquill/pipeline/engineering/agents/judge_scoring_agent_v1.md:52-60`.
- Logician is deterministic, fail-closed, zero-LLM policy enforcement:
  `projects/goldenquill/pipeline/engineering/agents/logician_enforcement_agent_v1.md:18-24`.
- Logician's gates include KGIE, RFA traceability, boundary drift,
  admin-risk, overlooked expenses, org isolation, revision loop counter, and
  score validation:
  `projects/goldenquill/pipeline/engineering/agents/logician_enforcement_agent_v1.md:67-120`.
- The capstone pipeline documents an 11-step submission-mode sequence with
  start, pre-gate, Scribe/Editor/Judge loop, post-gate, signoff stub, and
  delivery: `projects/goldenquill/pipeline/loop/run_pipeline.py:13-35`.
- The runtime supports optional Red Team after Judge:
  `projects/goldenquill/pipeline/loop/run_pipeline.py:472-498`.
- The inner loop is a three-iteration Scribe -> Editor -> Judge loop, with an
  iteration-cap failure if convergence never occurs:
  `projects/goldenquill/pipeline/loop/revision_loop.py:419-430` and
  `projects/goldenquill/pipeline/loop/revision_loop.py:774-780`.
- Demo fixtures provide a deterministic VAPG RFA snapshot and demo project
  context:
  `projects/goldenquill/tests/demo/demo_rfa/vapg_fy26_synopsis.json:1-20`
  and
  `projects/goldenquill/tests/demo/demo_project_context/PROJECT_CONTEXT.md:1-17`.

### Gaps And Tensions

- Council cardinality drifts across docs: some surfaces still imply a smaller
  loop while runtime can include Red Team.
- Logician placement differs by artifact: some docs frame PRE before Scout,
  others frame KGIE before Scribe. The DAG should represent named gate events
  rather than one generic Logician node.
- Narrative Spine and TRT are compelling DAG nodes but remain exploratory, not
  current runtime contract.
- Tilth Cards are research-time guidance and runtime design inputs, not live
  program law. The card skill says live eligibility, budget, attachment,
  deadline, and compliance rules belong in Program Rule Packs and must be
  verified against current official sources:
  `projects/goldenquill/skills/tilth-card-research/SKILL.md:57-65`.

### DAG Candidates

Runtime v0.1 nodes:

- `project_context`
- `opportunity_candidate`
- `scout_discovery_record`
- `scout_verification_record`
- `operator_review_decision`
- `rfa_dissection`
- `kgie_preflight`
- `scribe_section_draft`
- `editor_suggestion_report`
- `judge_score_report`
- `responsiveness_map`
- `logician_gate_result`
- `operator_signoff`
- `delivery_envelope`

Exploratory/v0.2 nodes:

- `narrative_spine_stop_point`
- `thesis_review_team_audit`
- `scout_reflection`
- `match_outcome`
- `funder_graph_walk_hypothesis`

## OV1: Ontology Vault Mapping

### Findings

- Ontology Vault exists to make knowledge roles, maturity states, confidence,
  edge rules, and promotion decisions explicit:
  `arcanum/arcana/ontology-vault/README.md:1-13`.
- Branch-aware ontology applies when domain intent and implementation evidence
  both exist:
  `arcanum/arcana/ontology-vault/README.md:13-23`.
- Stable public Ontology Vault docs use `Business`, `System`, and `Bridge`;
  bridge is required when a claim asserts alignment between intent and
  implementation:
  `arcanum/arcana/ontology-vault/README.md:47-57`.
- Starter edge types include `realized_by`, `depends_on`, `constrained_by`,
  `observed_by`, `tested_by`, `drifts_from`, and `traced_to`:
  `arcanum/arcana/ontology-vault/README.md:59-69`.
- The newer branch-aware schema candidate is explicitly exploratory and
  non-canonical:
  `arcanum/arcana/ontology-vault/development/BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md:1-24`.
- The candidate branch discriminator is `meaning | system | operational |
  bridge`, with `business | domain | intent | proposition | philosophy` as
  allowed local aliases:
  `arcanum/arcana/ontology-vault/development/BRANCH-AWARE-ONTOLOGY-SCHEMA-CANDIDATE.md:48-56`.
- The schema validation pass succeeded, but it does not promote Ontology Vault
  templates, Inventory fields, structured-action-schema fields, or external
  system adoption:
  `arcanum/arcana/ontology-vault/development/schema-validation-plan/VALIDATION-REPORT.md:7-14`.
- The validation report documents coverage for branch values, bridge evidence,
  Inventory non-authority, confidence split, promotion boundary, and record
  kind profiles:
  `arcanum/arcana/ontology-vault/development/schema-validation-plan/VALIDATION-REPORT.md:34-50`.

### Branch Mapping

| Branch | GoldenQuill local meaning | Examples |
| --- | --- | --- |
| `meaning` | funder/applicant/grant semantics | RFA requirement, funder priority, rubric criterion, applicant fact, budget claim, compliance obligation, reviewer dialect rule. |
| `system` | Tilth machinery | Scout result, Scribe section, Editor suggestion, Judge score, Logician gate, FID record, Card, PRP, uploader field. |
| `operational` | one bounded grant run | `{org, grant_id, RFA, draft_version, posture, run_id, deadline, route mode}`. |
| `bridge` | alignment evidence | "RFA criterion X is addressed by draft section Y", "budget line Z is constrained by PRP rule Q", "Judge score J tested claim C". |

### Gaps And Tensions

- Naming is unsettled: stable public docs say `business`; candidate schema says
  `meaning`. GoldenQuill should use `meaning` internally for the candidate DAG,
  while preserving `business` as a local alias until Ontology Vault governance
  settles.
- GoldenQuill needs `operational` as a first-class branch because grant truth is
  run-specific: a claim can be true for one RFA/org/deadline and unusable for
  another.
- Bridge evidence is the hard part. A draft paragraph, score, or review is not
  alignment unless the bridge cites evidence from both connected branches.

## LF1: Lean-Formalization Transfer

### Findings

- Lean-formalization's ontology conventions say operational graph authority
  lives in authored `## Connections` blocks; YAML `edges:` is only a migration
  target until a parity validator proves it matches:
  `domainspec-lean-formalization/vault/ontology-conventions.md:20-43`.
- It explicitly forbids collapsing lifecycle `status`, research closure fields,
  and proof state into one field:
  `domainspec-lean-formalization/vault/ontology-conventions.md:27-31`.
- Research closure has its own fields (`closure_mark`, `closure_ref`,
  `closure_note`), and closed/promoted research requires a `closure_ref`:
  `domainspec-lean-formalization/vault/ontology-conventions.md:121-138`.
- Proof truth is claim/declaration-level and cannot be inferred from prose:
  `domainspec-lean-formalization/vault/ontology-conventions.md:140-170`.
- Vague machine edges like `supports`, `suggests`, `related-to`, and vague
  `depends-on` are dangerous unless profile-defined:
  `domainspec-lean-formalization/vault/ontology-conventions.md:281-289`.
- The agents research constitution requires child agents not to write files;
  the parent writes canonical artifacts:
  `domainspec-lean-formalization/vault/agents-research-ontology/agents-research-constitution.md:50-69`.
- The same constitution requires hard register separation and dedicated
  synthesis for 3+ agents:
  `domainspec-lean-formalization/vault/agents-research-ontology/agents-research-constitution.md:101-113`.
- Investigation ontology provides useful node and edge types:
  `investigation`, `strategy`, `agent-report`, `synthesis`,
  `session-synthesis`, with edges like `briefs`, `dispatched-by`, and
  `synthesizes`:
  `domainspec-lean-formalization/vault/agents-research-ontology/ontology.md:37-65`.

### Transfer Rules

- Do not infer source truth, funder compliance, or reuse authority from proposal
  prose.
- Keep `lifecycle_state`, `closure_or_verdict`, `verification_state`, and
  `prose_surface` separate on graph nodes.
- Use visible authored connections first; structured JSON/YAML graph authority
  should come only after a parity validator exists.
- Replace vague `supports` with typed grant edges such as `evidenced_by`,
  `scored_by`, `operator_approved_by`, `source_authorized_by`, and
  `blocked_by_gate`.

## VAL1: Toy Validation

### Findings

- No first-class `grant_dag` or ontology-DAG validator exists yet.
- Scout v0.2 already defines graph-walk hypothesis generation over funder
  portfolios and near-miss vocabulary:
  `projects/goldenquill/pipeline/blueprint/v0.2/scout_v0_2_superscout_spec.md:178-193`.
- That spec explicitly blocks fabricated hypotheses and cross-applicant leakage:
  `projects/goldenquill/pipeline/blueprint/v0.2/scout_v0_2_superscout_spec.md:190-193`
  and `projects/goldenquill/pipeline/blueprint/v0.2/scout_v0_2_superscout_spec.md:228-233`.
- Vector namespace checks distinguish workspace-scoped namespaces from per-org
  namespaces and fail closed on unknown namespaces:
  `projects/goldenquill/pipeline/logician/gates/f_vector_ns_mismatch.py:28-39`
  and `projects/goldenquill/pipeline/logician/gates/f_vector_ns_mismatch.py:127-135`.
- Demo org fixtures explicitly distinguish fabricated demo orgs and no-real
  client data:
  `projects/goldenquill/apps/tilth_demo_v0/fixtures/orgs.json:1-6`.
- Demo RFA and project context fixtures exist, but the current demo project is
  applicant-shaped; a pure non-org DAG toy fixture should use synthetic
  archetypes instead of live org context.

### Toy Acceptance Criteria

- Fixture contains 5-7 nodes: applicant archetype, funder, program, eligibility
  gate, evidence source, research partner, proposed hypothesis.
- Graph is acyclic.
- Every edge has a typed relation, source/provenance, and resolved target.
- Positive case: a SARE-like research grant DAG passes when producer,
  researcher/extension/NGO partner, and outreach evidence exist.
- Negative cases fail closed: missing producer, missing researcher, fabricated
  funder/source, unknown namespace, cross-org source, cycle in DAG, and
  non-org-forbidden program attempted by individual/for-profit.
- Query output includes provenance and never returns per-org records unless
  `--org` is supplied.
- Any hard eligibility failure produces no draft/Scribe path.

## Cross-Lane Tensions

| Tension | Evidence | Resolution |
| --- | --- | --- |
| Workflow DAG vs ontology DAG | Pipeline has ordered runtime steps; Ontology Vault wants branch-owned claims and bridge evidence. | Use two linked graphs: execution DAG for run order, ontology DAG for claim/evidence/authority. |
| `business` vs `meaning` branch label | Stable Ontology Vault docs use business; candidate schema uses meaning. | Use `meaning` as candidate label with `business/domain/intent` aliases. Do not promote globally. |
| `supports` is too vague | Lean conventions flag vague edges. | Use typed grant edges: `evidenced_by`, `tested_by`, `scored_by`, `constrained_by`, `blocked_by_gate`, `approved_by`. |
| Proposal prose can look like truth | Scribe and Judge produce strong prose/reviews, but source truth belongs to RFA/PROJECT_CONTEXT/evidence. | Prose nodes are `consumes` or `realizes`; they do not become evidence nodes. |
| Cards/FID/PRPs are strong but bounded | Cards are not live program law; FID anti-fabrication boundaries exist. | Treat cards/FID/PRPs as source systems with authority classes, not ontology truth by default. |
| Operational context is missing from old ontology templates | GoldenQuill grant truth is run-specific. | Add `operational` branch to the candidate grant DAG model. |

## Open Questions

1. Should GoldenQuill keep both execution DAG and ontology DAG, joined by bridge
   edges, or attempt one unified graph?
2. Which compound state counts as "grant verified": source-resolved evidence,
   Logician pass, Judge score, operator approval, or funder outcome?
3. Should Red Team be first-class in the initial DAG contract or a conditional
   v7/runtime-capability node?
4. What is the minimum parity validator: Markdown connection blocks to JSON, or
   JSON graph to rendered evidence packet?
5. Can the first toy validator use only synthetic demo orgs and public/draft
   funder intelligence charters, avoiding all org-vault reads?
