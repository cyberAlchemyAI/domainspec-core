# DomainSpec Definitions Index

Purpose: normalize paper-level concepts into reusable, traceable research assets.

## Core Contributions and Named Definitions Mapped From Paper

| Definition ID | Paper Anchor | Definition Summary | Canonical Artifact(s) | Practical Example |
|---|---|---|---|---|
| DS-C1 | Contribution C1 | Dual-track layered meta-architecture (business + operational). | `claims/CLAIMS.md`, `papers/domainspec-paper.md`, `registry/TRACEABILITY-MATRIX.md` | Claim C1 is evaluated through E4/E5/E7/E8 and updated in `results/DOMAINSPEC-EVIDENCE-STATUS.md`. |
| DS-C2 | Contribution C2 | Deterministic derivation from typed ontology. | `claims/CLAIMS.md`, `experiments/E1-derivation-determinism/protocol.md`, `experiments/E6-vocabulary-sufficiency/protocol.md`, `experiments/E9-cross-feature-composition/protocol.md` | E6 and E9 provide current evidence baseline for C2. |
| DS-C3 | Contribution C3 | Governance attenuation bounded by channel capacity and mitigated structurally. | `claims/CLAIMS.md`, `experiments/E4-governance-attenuation-curve/protocol.md`, `experiments/E5-observer-executor-separation/protocol.md`, `experiments/E7-signal-emission-rate/protocol.md` | E4 and E5 are designed as direct tests for attenuation curve + intervention effect. |
| DS-C4 | Contribution C4 | Meta-circular self-governance via signals, reflection, and tuning loops. | `claims/CLAIMS.md`, `experiments/E8-meta-health-convergence/protocol.md`, `telemetry/SIGNAL-SCHEMA.md` | E8 measures convergence of meta-health signals over time. |
| DS-D1 | Definition 1 | Meta-type system for concept classification. | `implementation/domainspec/TAXONOMY.md`, `papers/domainspec-paper.md` | E6 classifies domain concepts against meta-types and reports coverage. |
| DS-D2 | Definition 2 | Typed relationship system for valid concept edges. | `implementation/domainspec/RELATIONSHIPS.md`, `papers/domainspec-paper.md` | E9 tests whether cross-context edges fit current relationship types. |
| DS-D3 | Definition 3 | Concept graph model $G=(V,E,\tau,\lambda)$. | `experiments/*/protocol.md`, `papers/domainspec-paper.md` | E9 run-2-rerun builds cross-context graphs from 6 domains (94 edges). |
| DS-D4 | Definition 4 | Derivation function $T=f(G,\Delta)$. | `implementation/domainspec/TEST-PIPELINE.md`, `experiments/E1-derivation-determinism/protocol.md`, `papers/domainspec-paper.md` | E1 checks run-to-run determinism for fixed feature specs. |
| DS-P1 | Property 1 | Type safety of relationship instances. | `implementation/domainspec/RELATIONSHIPS.md`, `experiments/E6-vocabulary-sufficiency/protocol.md` | E6 strained/uncovered relationship analysis highlights type-signature pressure points. |
| DS-P2 | Property 2 | Backend/UI partition disjointness. | `implementation/domainspec/TAXONOMY.md`, `papers/domainspec-paper.md` | UI and backend classifications remain split across taxonomy groups. |
| DS-P3 | Property 3 | Cross-layer bridging direction (UI -> backend). | `implementation/domainspec/RELATIONSHIPS.md`, `papers/domainspec-paper.md` | UI cross-layer edges (`fetches`, `mutates`, etc.) are directional in relationship signatures. |
| DS-COR-1 | Corollary 1 | Critical governance layer count $k^*$ where adding layers decreases effective governance capacity ($\partial C/\partial k < 0$ for $k > k^*$). | `papers/domainspec-paper.md`, `experiments/E4-governance-attenuation-curve/protocol.md`, `experiments/E5-observer-executor-separation/protocol.md` | E4 estimates attenuation shape and compares fitted behavior with the theoretical $k^* \approx 6$-$7$ range. |

## Formal Constructs and Equations Anchored in Paper

| Definition ID | Paper Anchor | Formal Construct | Canonical Artifact(s) | Practical Example |
|---|---|---|---|---|
| DS-F1 | Section 3.2 | Governance derivation chain $L4 \xrightarrow{justifies} L3 \xrightarrow{implemented\ by} L6$. | `implementation/domainspec/AXIOMS.md`, `implementation/domainspec/CONSTITUTION.md`, `implementation/domainspec/docs/shared/governance-baseline.md` | Alignment/audit gates can be traced to constitution rules and then to axioms before approval decisions. |
| DS-F2 | Section 5.1 | Test derivation function $T=f(G,\Delta)=\bigcup_{i=1}^{|\Delta|}\delta_i(G)$. | `implementation/domainspec/TEST-PIPELINE.md`, `experiments/E1-derivation-determinism/protocol.md` | E1 checks that fixed $G$ and fixed $\Delta$ yield stable test obligations across repeated runs. |
| DS-F3 | Section 5.3 | Test-cardinality equations ($|T|$ exact and lower-bound forms). | `implementation/domainspec/TEST-PIPELINE.md`, `experiments/E2-derivation-vs-manual/protocol.md`, `experiments/E3-mutation-testing/protocol.md` | E2/E3 use obligation counts as baseline for coverage and fault-detection interpretation. |
| DS-F4 | Section 5.4 | Observability derivation cardinality $|O|=\sum_{j=1}^{16}|o_j(G)|$. | `implementation/domainspec/OBSERVABILITY.md`, `implementation/domainspec/TEST-PIPELINE.md`, `experiments/E7-signal-emission-rate/protocol.md` | E7 evaluates whether emitted production signals match expected derived metric obligations. |
| DS-F5 | Section 6.3 | Channel-capacity governance model $C=B\cdot\log_2(1+S/N)$. | `papers/domainspec-paper.md`, `experiments/E4-governance-attenuation-curve/protocol.md` | E4 links observed compliance decay to a signal/noise interpretation instead of ad hoc failure causes. |
| DS-F6 | Section 7.4 | Closed-loop tuning cycle (pipeline -> signals -> thresholds -> proposals -> skill/agent updates). | `implementation/domainspec/TUNING-LOOP.md`, `implementation/domainspec/docs/telemetry/SIGNAL-SCHEMA.md`, `experiments/E8-meta-health-convergence/protocol.md` | E8 measures whether loop outputs reduce orphan and governance-friction indicators over time. |
| DS-F7 | Section 9.2 | Cross-feature composition algebra $G_{A\oplus B}=(V_A\cup V_B, E_A\cup E_B\cup E_{AB}, \tau_A\cup \tau_B, \lambda_A\cup \lambda_B\cup \lambda_{AB})$. | `experiments/E9-cross-feature-composition/protocol.md`, `experiments/E9-cross-feature-composition/results/E9-run2-rerun-results.md` | E9 evaluates practical pressure points before introducing stronger composition operators. |

## Method Definitions Used By Research Execution

| Definition ID | Definition Summary | Canonical Artifact(s) | Practical Example |
|---|---|---|---|
| DS-M1 | Tiered analysis policy (foundation vs full). | `definitions/METHODOLOGY-PROFILE.md` | E11 is explicitly marked full tier with dual-rater adjudication. |
| DS-M2 | Claim evidence vocabulary and status transitions. | `claims/CLAIMS.md`, `results/DOMAINSPEC-EVIDENCE-STATUS.md` | C2 is currently `partially supported`; C1/C3/C4 remain `insufficient evidence`. |
| DS-M3 | Protocol quality gate criteria. | `protocols/DOMAINSPEC-PROTOCOL-CHECKLIST.md` | G1 blocks when methodology linkage or measurable criteria are missing. |
| DS-M4 | Reproducibility metadata contract for experiment rows. | `definitions/METHODOLOGY-PROFILE.md`, `experiments/EXPERIMENTS.md` | A run row is invalid when required metadata fields (`experiment_id`, `run_id`, `timestamp`, `model`, `operator`) are missing. |
| DS-M5 | Validity threat quartet (internal/external/construct/conclusion). | `definitions/METHODOLOGY-PROFILE.md`, `templates/EXPERIMENT-RESULTS-TEMPLATE.md` | Claim upgrades are blocked when critical validity threats are undocumented. |
| DS-M6 | Signal envelope and required signal type vocabulary. | `telemetry/SIGNAL-SCHEMA.md` | Every blocked gate emits a remediation signal and evidence-update signals must reference claim + artifact. |
| DS-M7 | Protocol definition-anchor requirement. | `protocols/DOMAINSPEC-PROTOCOL-CHECKLIST.md` | Protocol review now requires explicit definition anchors from this index. |
| DS-M8 | Context bundle minimum structure for execution readiness. | `experiments/*/context.md`, `experiments/E11-technique-specialization/context.md` | Context bundles map claim target, source-role matrix, terminology map, metrics, and conflict log before execution. |
| DS-M9 | Reference authority levels and promotion states (`primary`, `supporting`, `fallback`; `operationalized`, `waived`, `pending normalization`). | `sources/REFERENCE-LEDGER.md` | Governance-theory references used for C3 are treated as primary authority for E4/E5 decisions. |
| DS-M10 | Claim acceptance threshold semantics and disconfirmation rules. | `claims/CLAIMS.md` | C3 requires attenuation baseline plus intervention recovery without dropping coverage. |
| DS-M11 | Evidence strength vocabulary and update policy semantics. | `results/DOMAINSPEC-EVIDENCE-STATUS.md` | Any downgrade must cite conflicting experiment evidence explicitly. |
| DS-M12 | Emission-rate metric definition for governance attenuation telemetry. | `experiments/E7-signal-emission-rate/protocol.md`, `telemetry/SIGNAL-SCHEMA.md` | Emission rate is computed as `actual_signal_count / expected_signal_count`. |

## Drift Notes (Paper vs Evolving Framework)

| Drift ID | Observation | Current Handling |
|---|---|---|
| DS-DRIFT-001 | Paper text references 24 meta-types and 26 relationships in the initial baseline. | Composition extension evidence (E9 + follow-up changes) is tracked in project artifacts; claim updates should cite run-scoped results and framework version. |
| DS-DRIFT-002 | Many theory references are present in paper but not normalized into source catalog/inventory artifacts. | Track in `sources/REFERENCE-LEDGER.md` and promote authoritative references into source catalog + inventory as needed by active experiments. |

## Usage Rules

1. Every protocol must reference at least one Definition ID (or formal-construct ID) relevant to its claim.
2. Every claim update must cite both experiment evidence and the affected Definition IDs.
3. New paper terms must be added here before being used as protocol-level requirements.
4. New governance or telemetry terms are gate-critical only after a Definition ID is assigned in this index.
