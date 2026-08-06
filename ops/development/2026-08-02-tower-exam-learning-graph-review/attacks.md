# Verbatim reviewer returns

Dispatch: `2026-08-02-tower-exam-learning-graph-review`  
Confirmed sheet: `2461719c8a1411f0f312549e2633a554f0793ea5f10292eb882306ae502bba29`

The three returns below are preserved as received. Parent synthesis and change-request ranking live in `findings.md`.

## Structure review receipt

- `agent_id`: `/root/tower_structure_review`
- `role_id`: `structure-explorer`
- `dispatch_id`: `2026-08-02-tower-exam-learning-graph-review`
- `parent_refine_run_id`: `20260802T013629Z-tower-exam-learning-graph`
- `spawn_status`: `pass`
- `join_status`: `ready_for_parent_join`
- `close_status`: `complete_read_only`
- `mutation_status`: none
- `forbidden-scope_status`: pass; no PDF bodies, network, DomainSpec content authority, or unrelated files inspected

### Scope reviewed

The root README, corpus manifest, comparative index, all six specified artifact types for the three towers, the Refine seed, and the strategy-inventory packet. Current target bytes were checked because Inventory is explicitly non-authoritative and has no Direito Romano target entry (`STRATEGY-INVENTORY-PACKET.md:3-7,45-51`).

### Findings

1. **The minimum coherent tower-derived schema is five node families.**

   - `SourceSnapshot`: one immutable PDF-byte identity.
   - `TowerSnapshot`: boundary, cutoff, status, learning spine, and the exact artifact snapshot used.
   - `KnowledgeRecord`: a typed record with only four initial kinds: `claim`, `definition`, `worked-example`, and `open-residue`.
   - `EvidenceAnchor`: source hash plus normalized physical PDF page or closed page range.
   - `StudyRoute`: tower-derived navigation from learning-pack entry points/operator models, explicitly non-authoritative.

   `Topic` should initially be a facet/tag, not a knowledge node. `Exception/counterexample` should be a field or typed relation unless independently identified. `Prerequisite` should be a relation, not a node. This reduction follows the artifact-to-node allocation required by the Refine seed, lines 15-25, while reducing the larger candidate list at lines 40-64.

2. **Four relation families are sufficient, provided each relation has an explicit role and provenance.**

   - `scopes/contains`: source -> tower and tower -> record/route.
   - `evidence-binding`: record/route -> evidence anchor, with role `supports`, `bounds`, or `points-to`.
   - `semantic-link`: record -> record, with role such as `derived-from`, `illustrates`, `limits`, or `requires-prerequisite`.
   - `navigation`: study route -> record/evidence/residue.

   No semantic edge should be generated from label similarity or list order. The root comparison explicitly says source agreement is only `local-inference`, disagreement remains residue, and no source outranks another (`COMPARATIVE-INDEX.md:26-30`).

3. **Stable identity requires logical IDs and immutable snapshot IDs to remain separate.**

   - Source ID: `source:<sha256>`. The manifest supplies hashes, byte counts, page counts, and extraction characteristics (`CORPUS-MANIFEST.md:13-22`).
   - Tower logical ID: stable repository-relative tower slug.
   - Tower snapshot ID: source hash + projection schema version + digests of the selected tower artifacts.
   - Claim/definition/residue IDs: namespace the existing local IDs by tower logical ID; examples include `MRA-C01`, `MRA-D1`, and `MRA-R1`.
   - Content digest/version: separate from semantic ID so wording changes do not silently create a new entity.
   - Edge ID: deterministic function of predicate, ordered endpoint IDs, and provenance selector.
   - Output order: sort by canonical IDs; never assign identities from ingestion or display order.

   Worked examples and learning-pack routes currently have numbered headings but no explicit durable IDs. They require a projection-side ID registry with artifact selector and reconciliation-on-drift; heading text or content hashes alone are insufficient. This is a real unresolved contract, consistent with the packet's statement that no stable cross-tower node-ID contract has been proved (`STRATEGY-INVENTORY-PACKET.md:45-50`).

4. **Provenance must preserve two distinct layers.**

   Every knowledge node needs:

   - tower provenance: repository-relative artifact path, record ID or heading selector, artifact digest, and evidence taxonomy;
   - source provenance: source hash, one-based physical PDF page locator, extraction mode, and page-image verification requirement.

   `primary-source`, `related-source`, `local-inference`, `analogy`, `operator-reading`, and `open-residue` must remain machine-visible; all three ledgers declare that taxonomy. Local inference should depend on named source-backed records, not masquerade as a direct PDF citation. OCR is only an access aid, and close quotation requires page-image checking (`README.md:25-36`; `CORPUS-MANIFEST.md:31-38`).

5. **The pilot topic is structurally present but not deep enough for the proposed supported-question acceptance.**

   - Moreira has only the orientation-level `MRA-C08`: possession as protected factual power, with “PDF p. 308 and the chapter sequence following” (`claim-ledger.md:15`). Its cutoff says the relevant sections were sampled, and narrow questions require chapter-specific work (`TOWER.md:25-31`; `open-residue.md:3-7`).
   - Marky supplies a curriculum-map statement covering ownership, possession, acquisition, and protection, but its ownership claim is only “PDF p. 91 onward,” not an element-level closed citation (`learning-pack.md:20-24`; `claim-ledger.md:16`).
   - Casos has exact case-range claims for Case 6 and Case 7 (`claim-ledger.md:13-14`), but its `worked-examples.md` contains only Cases 8, 9, and 1 (`worked-examples.md:3-28`).
   - None of the three definition-card files defines possession, ownership, acquisition, or protection as a pilot concept.
   - No artifact declares semantic prerequisite edges. Learning-spine order and the comparative reading paths are navigation, not proof of prerequisite dependency (`COMPARATIVE-INDEX.md:12-24`).

6. **Unbounded page locators cannot satisfy exact-evidence acceptance.**

   `p. 308 and the chapter sequence following` and `p. 91 onward` may be retained as `orientation-only` evidence anchors, but they cannot support expected answer elements under the seed's requirement that each supported question map to an exact source citation (`REFINE-SEED-PROPOSAL.md:91-100`). A validator should reject them for `answer-support` until converted into closed page-local claim extensions.

7. **Questions and attempts should be stored outside the tower snapshot.**

   The learner overlay should key itself to one immutable tower snapshot and question-set digest. Expected answer elements may link to tower nodes, but neither questions nor attempts may become source claims; this is an explicit authority boundary in the seed (`REFINE-SEED-PROPOSAL.md:25`). Deterministic element matching can be authoritative for the toy witness; any later model-generated feedback must be labelled advisory and unable to create knowledge nodes or evidence edges.

### Validation impact

A later graph validator should fail closed on:

- duplicate or ingestion-order-derived IDs;
- missing artifact selectors/digests;
- supported expected elements without closed page anchors;
- source hashes absent from evidence anchors;
- inference/analogy/operator-reading presented as primary-source;
- OCR residue presented as settled content;
- semantic edges without explicit provenance and derivation status;
- prerequisites inferred merely from document order;
- cross-source agreement presented as consensus;
- learner-overlay records entering the tower knowledge layer;
- any DomainSpec ontology type or relation used as content authority.

Required negative witnesses should include input permutation, missing/ambiguous citation, OCR-empty/noisy evidence, unsupported question abstention, generic “study more” rejection, and DomainSpec-type leakage. UI/browser claims remain `NOT_RUN` until the later browser witness, as required by the strategy packet (`STRATEGY-INVENTORY-PACKET.md:23-29`).

### Block verdict

- **No block** to completing the Refine design and implementation plan with the five-family schema and explicit validation contract.
- **Block** to claiming that the current tower artifacts can already support the proposed 5-10-question possession/ownership/acquisition/protection pilot at element-level traceability. The implementation must either:
  1. narrow supported questions to the few propositions with closed existing citations, or
  2. authorize page-specific claim/definition/example extensions for the pilot before implementation acceptance.

### Residue and reroute

- Stable IDs for worked examples and study routes remain unproved.
- Pilot-specific definition cards and prerequisite relations are absent.
- Moreira and Marky pilot citations need closed page ranges.
- Cases 6-7 need explicit worked-example records if they are to appear as worked-example nodes.
- Cross-tower mappings must be separately curated and labelled `local-inference`.

Reroute those content gaps to a bounded Research Tower extension before Task Session implementation; keep the current Refine route responsible for schema, sidecar-ID contract, validation rules, toy-question constraints, and handoff.

### Handoff note

The next designer should treat the graph as a deterministic, regenerable projection over one immutable tower snapshot. Preserve source-byte identity, tower-artifact provenance, evidence taxonomy, abstention, and non-executing study routes. Do not promote inferred topics, prerequisites, comparisons, questions, or model feedback into source-backed knowledge.

## Falsification-review receipt

- `role_id`: `falsification-reviewer`
- `route`: confirmed Refine review
- `stage_status`: `complete`
- `review_verdict`: `FLAG`
- `implementation_gate`: `BLOCK` for doctrinal answer scoring; `PASS` for an evidence-routing prototype
- `research_mode`: local-only; no network used
- `mutation_status`: none
- `claim_ceiling`: design falsification and deterministic interaction criteria only; no legal-answer, learner-effectiveness, promotion, or browser-success claim
- `inputs_verified`: current bytes of the seed, comparative index, nine tower files, and strategy-inventory packet; SHA-256 recorded during review
- `blocked_reason`: Cases 6-7 are identified as possession/property probes, but the permitted evidence does not contain their facts, proposition-level answers, or page-specific doctrinal claim pairs
- `next_owner`: Refine synthesis; later evidence owner must create page-specific Case 6-7 fixtures before doctrinal evaluation
- `receipt_artifact`: inline response; no file written

### Main finding

The graph can currently be tested as a tool for finding the next evidence-bearing question, but not as a grader of Roman-law doctrine.

The scoped artifacts support:

- the topic grouping “ownership, possession, acquisition/protection”;
- Cases 6-7 as the selected application probes;
- the dimensions a disciplined property answer must identify;
- local-inference, OCR, provenance, and current-law boundaries.

They do not support a correct doctrinal answer for Cases 6-7. The case tower explicitly says no proposition-level adjudication exists and directs deeper work to page-specific verification (`learning-pack.md:39`). Inventing an answer key would violate the seed's own falsification criteria (`REFINE-SEED-PROPOSAL.md:78`).

### Smallest toy game: seven questions

The score is “trace completion,” never mastery, readiness, or exam effectiveness.

| ID | Mode | Prompt | Deterministic expected elements and route |
|---|---|---|---|
| `DR-TG-01` | Recall | “Which subtopics does Marky's compact map place under Things?” | `ownership`, `possession`, `acquisition/protection`, `limited rights`, `security`; evidence: Marky learning pack lines 20-24. |
| `DR-TG-02` | Source selection | “Which local cases are the possession/property probes, and what must be recorded before using one?” | Cases `6-7`, plus issue-bearing facts, persons/statuses, object/event, competing classifications, asserted source/rule/period, remedy/effect, proposed result, and uncertainty/OCR needs; evidence: Casos learning pack lines 5-23. |
| `DR-TG-03` | Distinction | “Before presenting a 'Roman property rule,' which dimensions must the answer state?” | Historical phase; civil/praetorian/imperial source or protection; actor status; object; acquisition form; remedy; physical PDF page; analogy label where applicable; evidence: Moreira worked example lines 3-17. |
| `DR-TG-04` | Wrong-answer application | Learner attempt: “Case 6 proves possession is ownership.” Ask: “What is missing before this can count as a supported answer?” | Mark missing: Case 6 fact/page binding, phase, source/protection, actors/statuses, object/event, acquisition form, remedy/effect, evidence status, OCR/adjudication status. Route to Cases 6-7, PDF pp. 16-24, then `CAS-R2` and `CAS-R4`; do not supply a doctrine answer. |
| `DR-TG-05` | Cross-source reasoning | “If Marky and Moreira appear to agree, what may the graph claim, and what must be checked next?” | Only `local-inference`, never historical consensus; next question must request a specific page pair. Route to `MRA-R4`, with a chapter-specific extension under `TM-R4`; evidence: comparative index lines 26-30 and Moreira residue lines 11-13. |
| `DR-TG-06` | Provenance control | “A close quotation from Marky appears relevant to acquisition or protection. May it be used immediately?” | No. Require page-image verification, exact page, evidence status, and independent checking of cited Roman material. Route to `TM-R2`/`TM-R3`; evidence: Marky learning pack lines 15-18 and 36-40, residue lines 6-9. |
| `DR-TG-07` | Unsupported control | “Does current Brazilian law treat possession and ownership exactly as these Roman sources do?” | Exact outcome: `ABSTAIN_UNSUPPORTED`. Explain that current-law advice is outside the corpus. Next bounded question: “Which jurisdiction, cutoff date, and primary-law source corpus should govern a separately authorized comparison?” No Roman-law or modern-law answer may be generated. |

`DR-TG-04` is the critical falsifier. If the graph merely opens Case 6 or a topic node, it has produced browsing. It helps formulate the next question only if it names one missing element and turns it into an answerable, evidence-bounded interrogative.

Required next-question record:

```text
missing_element_id
next_question_text
target_artifact
target_page_or_residue
why_this_is_next
stop_condition
```

Example, without supplying a legal answer:

```text
missing_element_id: case6.source_page
next_question_text: Which page in Case 6 supports the claimed possession/title distinction?
target_artifact: casos-resolvidos-direito-romano
target_page_or_residue: PDF pp. 16-24; CAS-R2
why_this_is_next: the attempt cites a case number but no proposition-bearing page
stop_condition: stop and preserve residue if page-image verification cannot establish the proposition
```

### Exact acceptance criteria

The toy game passes only if all are true:

1. All seven question IDs and expected-element IDs are stable across identical compilations.
2. Permuting source, tower, question, or answer-element input order produces identical normalized node IDs, edge triples, evidence bindings, and question semantics.
3. `DR-TG-01` through `DR-TG-06` resolve only to the cited local artifacts; no answer text comes from prompt wording or model memory.
4. `DR-TG-04` computes missing elements as a deterministic set difference and returns at least one exact artifact/page-or-residue route.
5. Every wrong attempt yields one primary bounded next question containing a missing-element identifier, evidence target, reason, and stop condition.
6. `DR-TG-07` always returns `ABSTAIN_UNSUPPORTED`; it never generates Roman or Brazilian doctrine.
7. Every visible knowledge node exposes artifact path, source identity, page or residue reference, and evidence status.
8. Cross-source agreement is labelled `local-inference`; it is never rendered as consensus.
9. OCR, unverified quotation, and unadjudicated booklet answers cannot be upgraded to settled doctrine by rendering or scoring.
10. Learner attempts remain a separate overlay: changing an attempt cannot change the knowledge-graph hash.
11. The result reports trace completion and missing elements only; it contains none of `mastery`, `ready`, `exam-effective`, or equivalent claims.
12. The rendered knowledge layer contains zero DomainSpec ontology nodes or relations.

### Exact failure criteria

Fail immediately if any occurs:

- Case 6 or 7 receives a doctrinal answer key from the currently scoped files.
- “Study more,” “review possession,” a neighbor list, or a cluster highlight is returned without a bounded interrogative and exact evidence target.
- A recommendation names several destinations but does not select the missing element that makes one route next.
- Any citation drops its physical PDF page or residue identifier.
- An unsupported question produces a plausible answer before abstaining.
- A disagreement is harmonized, or two-source agreement is called consensus.
- Input shuffling changes identity, relation meaning, missing-element ordering, or abstention behavior.
- The score is described as knowledge, mastery, readiness, or likely exam performance.
- Attempt data mutates source-backed nodes.
- A stale/missing evidence reference silently renders as supported.
- Browser interaction requires hover, pointer use, color perception, animation, or loss of current question/attempt state.

### Browser and accessibility controls

These remain `NOT_RUN`; they are acceptance requirements for later implementation.

- Complete select-question -> enter attempt -> inspect missing element -> open provenance -> return-to-question using keyboard only.
- Every interactive node and relation has visible focus and works with Enter/Space.
- Provenance opened as a dialog or panel returns focus to its invoker on close.
- Disable hover and repeat the full evidence-inspection path; no information may disappear.
- Force grayscale/high-contrast presentation; supported, inference, residue, and unsupported states remain distinguishable through text and non-color cues.
- Enable `prefers-reduced-motion`; no meaning, state transition, or focus movement depends on animation.
- Switch questions rapidly and reopen the prior question; selection, attempt, relation state, and provenance target remain atomic and uncorrupted.
- Inject a missing evidence target; the UI fails closed to residue and exposes no answer.
- Recompile with shuffled inputs; saved question selection and evidence links still resolve through stable IDs.

### Readiness conclusion

The proposed graph is falsifiable only when “next route” means an exact next question, not a collection of links. The seven-question game above can test that interaction now. Doctrinal grading should remain blocked until Case 6-7 facts and propositions are bound to verified pages and the open exact-elements-versus-model-assisted evaluation decision is resolved.

## Memory-residue review receipt

- `agent_id`: `/root/tower_memory_review`
- `role_id`: `memory-residue-reviewer`
- `dispatch_id`: `2026-08-02-tower-exam-learning-graph-review`
- `spawn_status`: `spawned`
- `join_status`: `completed`
- `close_status`: `closed`
- `capability_handle`: `/root/tower_memory_review`
- `receipt_kind`: `bounded-native-helper-review`
- `runtime_surface`: native subagent
- `requested_mode`: local/read-only/current-bytes
- `status`: `complete`
- `verdict`: `FLAG_NO_BLOCK`
- `output_artifact`: none (chat receipt)
- `mutations`: none
- `network`: none
- `observer_status`: not emitted
- `blocked_reason`: none

No-block boundary: Refine design may continue. This review does **not** admit HTML implementation or claims of stable IDs, corpus completeness, correctness, comprehension, mastery, or exam effectiveness. Current run is still waiting exact dispatch confirmation (`RUN-MANIFEST.md:3-13`).

Reusable interaction mechanics (shape only): search, layer filtering, node/relation selection, focus highlighting, inspector with stable ID/binding/status/claim ceiling, guided Ask -> Inspect -> Abstain -> Name missing witnesses -> Revise question -> Suggest display-only destination, and focus state that does not record comprehension. Verified in `LEARNING-GRAPH-PROTOTYPE.html:432-468,490-549,1008-1043`. Inventory independently selects regenerable projection, evidence bindings, abstention, non-executing route suggestions, shared selection/provenance, and graph-accessibility controls (`STRATEGY-INVENTORY-PACKET.md:15-37`).

Forbidden knowledge content: do not reuse DomainSpec semantic/profile/evaluation/TypeScript nodes, IDs, digests/bindings, relations, question text, gap witnesses, or `TypeScript adapter owner`. The prototype's actual graph source is `ontology.json`, candidate profiles, TS observations/evaluation, and DomainSpec session records (`LEARNING-GRAPH-PROTOTYPE.html:560-720,723-786`); Refine explicitly rejects DomainSpec nodes/relations as content authority (`REFINE-SEED-PROPOSAL.md:13-25,78-100`; `RUN-MANIFEST.md:22-24`). Preserve only interaction patterns, rebuilt from tower artifacts.

Duplicate/ambiguous assumptions to resolve before schema freeze:

1. `Open Residue` (tower knowledge) vs `Knowledge Gap` (learner overlay) must have disjoint identity/lifecycle; otherwise the graph turns a learner miss into source uncertainty (`REFINE-SEED-PROPOSAL.md:42-64`).
2. `Study Route` vs `Next Review Route` likely duplicate route semantics unless one is immutable tower guidance and the other session-derived projection (`REFINE-SEED-PROPOSAL.md:53-64`).
3. `Source` vs `Evidence or Page Citation`, and `Concept or Definition`, need explicit record/binding distinctions; do not mint separate nodes merely because two tower files mention the same page/concept (`REFINE-SEED-PROPOSAL.md:13-23,42-64`).
4. `Topic`, `Prerequisite`, `Exception/Counterexample` may be node classes or typed relations; candidate list itself says minimum schema and provenance per relation remain unresolved (`REFINE-SEED-PROPOSAL.md:40-64,112-119`).
5. Stable cross-tower node IDs are unproved, so source order independence is still only a falsification criterion, not evidence (`REFINE-SEED-PROPOSAL.md:78-100`; packet `:45-51`).

OCR/source-status risks:

- Entire project is `local-research-only`; OCR is access aid and page image is authority; no terms or bridges are promoted (`README.md:25-36`).
- Moreira is 879/883 embedded-text pages but long-work coverage is sampled, not exhaustive (`README.md:38-48`; Moreira `TOWER.md:25-31`).
- Casos is noisy OCR, unknown author/date/edition, and proposed solutions are booklet claims, not adjudicated truth (`CORPUS-MANIFEST.md:17-19`; Casos `TOWER.md:3-9,28-33`); Case 1 may be omitted/truncated (`CAS open-residue.md:3-10`).
- Marky has 12 OCR-empty pages and all quotations/Latin terms/dates/source references require page-image verification (`Marky TOWER.md:23-29`; `open-residue.md:3-11`).
- OCR text was transient, not preserved as substitute source; deterministic extraction/node identity cannot be assumed merely from the PDF digest (`CORPUS-MANIFEST.md:31-38`).
- Cross-source agreement is local inference, never consensus; disagreement must remain residue (`COMPARATIVE-INDEX.md:26-30`).

Owner-routed residue:

- Future researcher: CAS provenance/corrected text/Case 1; Moreira bounded chapter coverage/front matter; Marky OCR-empty pages/corrected text/full coverage.
- Future comparative/source-critical tower: Casos adjudication, Moreira cross-text reconciliation and source criticism, Marky source criticism (`towers/*/residue/open-residue.md`, all current).
- Refine/graph-contract owner + explicit operator decision: minimum schema, question storage, stable IDs, answer-evaluation boundary, reusable input contract, prototype supersession (`REFINE-SEED-PROPOSAL.md:112-119`).
- Separate learner-study owner: any comprehension/mastery/exam-effectiveness claim (`REFINE-SEED-PROPOSAL.md:27-38,91-100`; packet `:45-51`).

Handoff: preserve the prototype only as an interaction precedent. Freeze a tower-derived identity/provenance contract that separates source residue from learner gap and immutable study route from session route; carry every OCR/source-status ceiling visibly; route unsupported questions to abstention plus a bounded future-research owner. Do not let standard-depth tower closure imply proposition-complete coverage.
