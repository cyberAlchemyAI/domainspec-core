# Operational-analysis fanout receipts

Step `fanout-operational-analysis` (`robot-talks`). 5 role-bound lanes, parallel, parent-synthesis.
Operator approved delegated execution 2026-06-12. All lanes read-only. Tags **[SB]/[H]/[T]**.

## Lifecycle ledger

| agent_id | role_id | spawn | join | close | receipt |
| -------- | ------- | ----- | ---- | ----- | ------- |
| op-lane-1 | authority-hierarchy-reader | spawned | completed | closed | this file §1 |
| op-lane-2 | discipline-authority-reader | spawned | completed | closed | this file §2 |
| op-lane-3 | telemetry-derivation-reader | spawned | completed | closed | this file §3 |
| op-lane-4 | branch-schema-reader | spawned | completed | closed | this file §4 |
| op-lane-5 | axiom-coherence-adversary | spawned | completed | closed | this file §5 |

## §1 authority-hierarchy-reader — VERDICT-INPUT: NO (only via promotion). Confidence HIGH

- A discipline cannot directly reach L6/L7. [SB DISCIPLINES.md:53-55 Growth Rule: "Discipline evidence can recommend a route, but it cannot directly promote registry, ontology, glossary, sigil, or spell knowledge."]
- Axiom bar (L7): invariant-bearing test, dependency review, strong evidence, contradiction review, explicit commitment. [SB PROMOTION-LIFECYCLE.md:99]
- Constitution bar (L6): governed artifact/form/model/transformation, preserved invariant/gate, owner, rollback. [SB PROMOTION-LIFECYCLE.md:98]
- Disciplines run a *separate* maturity ladder (candidate→active-pattern→implemented→canonical), independent of L0-L7. [SB DISCIPLINES.md:44-51]
- A discovery→PromotionRecord→Candidate/Premise/Policy/Constitution/Axiom pipeline exists; disciplines are excluded from directly traversing it to ontology authority. [SB PROMOTION-LIFECYCLE.md:18-61]

## §2 discipline-authority-reader — VERDICT-INPUT: reframing SUPPORTED. Confidence HIGH (95%)

- MUST NOT: claim promotion authority for sigils/spells; mutate capability contracts without the owning route; treat execution evidence as canonical without owner review; duplicate sigil/spell internals. [SB disciplines/README.md:28-33]
- **PRECEDENT:** `schema` and `artifact-constitution` are `canonical` disciplines with steward **Constitution Governance** — disciplines *backed by* constitutions; the constitution holds authority, the discipline describes the practice. [SB DISCIPLINES.md:25-26]
- Purpose of the layer: "decide whether a practice needs a constitution, validator, template, spell, sigil, or only a catalog entry." [SB disciplines/README.md:14]
- ⇒ "disciplines are the disciplined SOURCE that feeds an operational axiom/constitution set, not the authority itself" is precedent-backed.
- Residue: the Schema/Artifact Constitution docs themselves not read (mirror-side evidence).

## §3 telemetry-derivation-reader — only L0-L3 derivable. Confidence HIGH for nodes, MED for edges

- Derivable candidate NODES (max authority): sigil-invocation L1 (high) · capability-contract L1 · mode-transition L1 (temporal only) · workflow-gap/failure-mode L0 · reflection-trigger L0 · route/dispatch L1 (design artifact, telemetry only verifies). [SB envelopes, sigil-invocations.jsonl, *.dispatch.json]
- Derivable EDGES: `observed_by` (structural, L1) and `triggers` (temporal, L1) reliable; `derived_from` L0; `governed_by` NOT derivable (needs literature + owner). 
- **GAPS (zero telemetry):** "discipline hardened" and "lesson promoted" — these are source-backed, not telemetry-derived. Also no context-solution-reuse, no decision-record owner/rationale field.
- Caveat [SB]: unreviewed telemetry is not branch-owned — L0-L2 evidence that may seed L3 candidates only; L4+ requires Constitution Governance + ontology-harness review (enforced by `telemetry-evidence-boundary`).

## §4 branch-schema-reader — schema shape clear; ⚠️ key distinction. Confidence HIGH

- Branch-aware node minimal fields: `node_id, node_type, branch, label, source, veracidade, evidence_refs, status, edges` (+type-specific). [SB projects/ontologize/schemas/ontology-node.schema.json:14-97]
- Single edge catalog is source of truth (source-type→target-type, cardinality, inverse, acyclicity). Do not invent a new one. [SB DAG-AND-METRICS.md §3]
- **⚠️ Distinction the lane surfaced:** the existing ontologize node schema (N1-N6 → B1/B2/B3/B4) is the **product / run-context** ontology. The **operational** (agent-operation) ontology is arcanum's separate "Operational Ontology", a **candidate extension** — "not a permanent fourth branch until user or ontology-harness review accepts that branch shape." [SB ONTOLOGY-ARCHITECTURE.md:79,139]
- ⇒ The seed must REUSE the branch-aware node-schema *shape* + edge catalog, but declare a new candidate branch with operational node types, labeled candidate pending review. Keep distinct from B3 run-context. [SB RECONCILIATION.md §1]

## §5 axiom-coherence-adversary — H0 literal REFUTED; softer form survives narrowly. Confidence 9.5/10

- Strongest refutation of literal H0: DISCIPLINES.md:55 forbids disciplines from promoting ontology knowledge; the operational branch is ontology ⇒ disciplines cannot establish it as a tier. [SB]
- Three problems with the softer reframing:
  1. **Circular governance** — `artifact-constitution` discipline already lists `disciplines/**` in its constitution scope; a discipline feeding a constitution that governs disciplines is self-referential. [SB DISCIPLINES.md:26 + ARTIFACT-CONSTITUTION.md:21]
  2. **Premature branch promotion** — operational branch is candidate pending user/ontology-harness review. [SB ONTOLOGY-ARCHITECTURE.md:79,139]
  3. **Telemetry laundering** — ReviewableSignal "cannot become 'truth' without review." [SB ONTOLOGY-ARCHITECTURE.md:323]
- Failure conditions for seeding now: no review gate closed; no discipline owns an ontology branch; branch status unresolved; no validation surface; telemetry non-authoritative.
- **Narrowest unrefutable claim:** disciplines may *catalog observed operational patterns as candidates flagged for later ontology-harness review* — recommend a route, not promote.

## Parent synthesis (convergence)

All five lanes converge: **the literal hypothesis is false; the reframing is true and precedent-backed; seeding is allowed only as a labeled candidate that recommends, never promotes.** No lane dissents. The adversary's narrowest-unrefutable claim and the discipline lane's reframing are the same shape. → feeds `decisions/disciplines-as-axiom.md`.
