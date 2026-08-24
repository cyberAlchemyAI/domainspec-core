# Verified change requests: tower exam learning graph

Dispatch: `2026-08-02-tower-exam-learning-graph-review`  
Review type: read-only red team  
Final approver: parent  
Evidence boundary: current local tower artifacts and the persisted Refine seed; no PDF-body reread, network research, implementation, or browser execution

## Artifact: Refine seed and candidate graph model

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| CR-01 | `/home/vrondelli/projects/direito-romano/development/refinement-runs/20260802T013629Z-tower-exam-learning-graph/REFINE-SEED-PROPOSAL.md` | The candidate model at lines 40-64 leaves node-versus-relation identity unresolved. Current towers provide durable local IDs mainly for claims, definitions, and residues; topics, prerequisites, examples, and routes do not all have equal identity evidence. See `attacks.md`, Structure findings 1-3 and Memory ambiguities 1-4. | MAJOR | Reduce the knowledge model to `SourceSnapshot`, `TowerSnapshot`, typed `KnowledgeRecord`, `EvidenceAnchor`, and `StudyRoute`; use four relation families with typed roles. Treat topic as a facet and prerequisite as an evidenced relation. |
| CR-02 | same | The seed's supported-question acceptance at lines 91-100 requires source-backed expected elements. Moreira uses “p. 308 and the chapter sequence following”; Marky uses “p. 91 onward”; Casos lacks page-local worked-example records for Cases 6-7. See tower ledgers and `attacks.md`, Structure findings 5-6. | MAJOR | Type unbounded locators as `orientation-only` and forbid them from `answer-support`. Narrow the first prototype to evidence-routing questions, or route a bounded Research Tower extension for page-local pilot fixtures before doctrinal grading. |
| CR-03 | same | Stable input-order-independent identity is a falsification criterion, but no cross-tower ID contract exists. Worked examples and learning routes lack durable local IDs. See `STRATEGY-INVENTORY-PACKET.md:45-50` and `attacks.md`, Structure finding 3. | MAJOR | Separate logical IDs, immutable snapshot IDs, and content digests; add a projection-side ID registry for heading-derived records; sort by canonical IDs; define deterministic edge IDs from predicate, ordered endpoints, and provenance. |
| CR-04 | same | `Open Residue` and learner `Knowledge Gap`, plus `Study Route` and `Next Review Route`, can collapse distinct authority/lifecycle concepts. See seed lines 42-64 and `attacks.md`, Memory ambiguities 1-2. | MAJOR | Store questions, attempts, missing elements, and next-question routes in a learner-session overlay keyed to tower snapshot and question-set digest. Forbid overlay mutation of the knowledge snapshot. |
| CR-05 | same | The proposed “next study route” can degrade into browsing. `DR-TG-04` shows that useful remediation requires one missing element converted into one bounded interrogative with an exact evidence target. See `attacks.md`, Falsification main finding and toy game. | MAJOR | Make `NextQuestion` the output contract: `missing_element_id`, question text, target artifact, page-or-residue, reason, and stop condition. Reject generic “study more,” clusters, or unranked destination lists. |

Verdict: **FIX**.

## Artifact: provenance and evidence contract

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| CR-06 | `/home/vrondelli/projects/direito-romano/CORPUS-MANIFEST.md` plus `towers/*/claims/claim-ledger.md` | The manifest binds immutable source hashes and OCR modes; ledgers distinguish `primary-source`, `related-source`, `local-inference`, `analogy`, `operator-reading`, and `open-residue`. The seed does not yet freeze both provenance layers. See `attacks.md`, Structure finding 4. | MAJOR | Require tower provenance (artifact path, selector/local ID, artifact digest, evidence taxonomy) and source provenance (source hash, one-based physical PDF page/closed range, extraction mode, verification requirement) on every knowledge node and supporting edge. |
| CR-07 | `/home/vrondelli/projects/direito-romano/COMPARATIVE-INDEX.md` | Lines 26-30 prohibit treating two-source agreement as consensus and require disagreement to remain residue. | MAJOR | Make cross-tower links curated `local-inference` records backed by named records. Never generate semantic edges from labels, order, or apparent agreement. |
| CR-08 | `/home/vrondelli/projects/direito-romano/README.md`, `CORPUS-MANIFEST.md`, tower residue files | OCR is access only; Marky has 12 OCR-empty pages; Casos provenance and text are noisy; Moreira coverage is sampled. See `attacks.md`, Memory OCR/source-status risks. | MAJOR | Carry evidence ceiling and verification requirements into data, inspector, scoring, and abstention. Missing or stale evidence must fail closed to residue. |

Verdict: **KEEP** for source artifacts; **FIX** the graph contract that consumes them.

## Artifact: toy-game and evaluation boundary

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| CR-09 | Refine seed pilot slice | Cases 6-7 are identified as application probes, but scoped artifacts contain neither verified proposition-level answer keys nor page-local worked-example records. See Casos `learning-pack.md:39` and `attacks.md`, Falsification receipt. | CRITICAL | Prohibit doctrinal correctness scoring in the first prototype. Score only deterministic trace completion and missing expected elements for evidence-discipline questions. Keep page-specific content extension as a separately authorized tower route. |
| CR-10 | Refine seed toy-game plan | The unsupported current-Brazilian-law question can elicit plausible model memory unless abstention is deterministic. | MAJOR | Include `DR-TG-07` with exact `ABSTAIN_UNSUPPORTED`, a separately scoped comparison question, and no legal answer generation. |
| CR-11 | Refine seed acceptance evidence | Browser interaction/accessibility evidence is absent. The prior DomainSpec prototype proves only reusable interaction shape. | MAJOR | Plan later keyboard-only, no-hover, grayscale/high-contrast, reduced-motion, focus-return, rapid-switch atomicity, missing-target fail-closed, and shuffled-input persistence checks. Keep all as `NOT_RUN` until browser evidence exists. |
| CR-12 | Refine seed desired outcome | Graph use is framed for exam preparation, but no learner study exists. | MAJOR | Ban mastery, readiness, comprehension, and exam-effectiveness claims. The prototype claim ceiling is deterministic tower projection and evidence-route usability only. |

Verdict: **FIX**.

## Artifact: rejected DomainSpec prototype

| # | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| CR-13 | `cyberAlchemy-v2/development/research/2026-08-01-learning-graph-next-route-guide/invoke/LEARNING-GRAPH-PROTOTYPE.html` | Its graph data is DomainSpec ontology/profile/TypeScript evaluation content, while the Refine seed forbids DomainSpec content authority. Search, filtering, focus, inspector, abstention, and route-display mechanics are separable. See `attacks.md`, Memory receipt. | MAJOR | Reuse interaction mechanics only. Rebuild every data record, ID, relation, question, gap witness, and provenance binding from Direito Romano tower artifacts. Add a validator that fails on DomainSpec type/relation leakage. |

Verdict: **KEEP as interaction precedent only; FORBID as knowledge source**.

## Ordered change-request list

1. CR-09 — block doctrinal answer scoring until page-local tower evidence exists.
2. CR-01 — freeze the five-family tower schema and four typed relation families.
3. CR-06 — freeze two-layer provenance and machine-visible evidence taxonomy.
4. CR-03 — separate logical/snapshot/content identity and create sidecar IDs where tower IDs are absent.
5. CR-04 — isolate learner overlay from source knowledge and source residue.
6. CR-05 — require an exact bounded next-question record, not generic navigation.
7. CR-02 — reject orientation-only page locators for answer support.
8. CR-07 — curate cross-source inference and prohibit inferred consensus.
9. CR-08 — fail closed on OCR, missing, stale, or unverified evidence.
10. CR-10 — make unsupported-question abstention deterministic.
11. CR-11 — carry browser/accessibility controls as `NOT_RUN` future witnesses.
12. CR-12 — preserve the study-navigation claim ceiling.
13. CR-13 — reuse prototype interaction shape only and reject DomainSpec content leakage.

## Parent verification and acceptance

- Current source selectors cited by all surviving findings were inspected by the parent.
- No reviewer finding was treated as proof solely because Inventory mentioned it.
- No refuted findings survived; the three returns converged on the same content-depth block and complementary design repairs.
- Zero-findings flag: not triggered; each reviewer returned material findings.
- Change-request list: **accepted**.
- Review close meaning: accepted FIX findings are the resolved deliverable; implementation remains a later owner route.
