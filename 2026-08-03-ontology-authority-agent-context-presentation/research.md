# Explorer returns

The sections below preserve the explorer returns verbatim as joined by the dispatch owner. Receipt envelopes live in `receipts/`.

## Agent 1 — Meaning and authority

## Meaning and authority explorer return

Read-only result. No artifact was written.

### Classification key

- **AUTHOR VOICE** — the requested accessible opening; not canonical terminology.
- **CANONICAL** — directly governed by the active private definition or authority contract.
- **PRESENTATION SYNTHESIS** — source-backed wording composed for this room; not a replacement definition.
- **INFERENCE** — a bounded explanatory deduction or hypothetical witness, explicitly not repository fact.

### 1. Smallest coherent definition for the room

**AUTHOR VOICE + PRESENTATION SYNTHESIS**

> Ontology is a bounded knowledge space—a working model of the part of the world we care about—where important things and their relationships carry evidence, time, confidence, and rules for use.

Immediately bound “world model” with:

> It is not a complete model of reality or a truth machine. It represents a selected domain for an intended use, and it keeps what something means separate from whether anyone has authorized relying on it.

**CANONICAL REFINEMENT**

The active private definition is stricter: ontology is a governed meaning layer over selected evidence, containing typed knowledge objects and relations together with ownership or role context, provenance, confidence, lifecycle posture, contradiction or drift routes, and downstream-use obligations. A pointer list, index, transcript, memory store, or graph shape alone is insufficient.

### 2. Minimum object/relation/time/confidence/provenance/promotion/use-rule model

| Element | Minimum room model | Classification |
|---|---|---|
| Object | A typed thing with identity, kind, claim or meaning, scope, and role/owner context. | **CANONICAL**, simplified |
| Relation | A typed connection whose meaning is named, such as `supports`, `constrains`, `contradicts`, `supersedes`, or `realizes`. The relation—not merely adjacency—explains consequence. | **CANONICAL + PRESENTATION SYNTHESIS** |
| Time | Record when evidence was observed, the interval or scope for which it is valid, when it expires, and what supersedes it. `observed_at` and `valid_from/to` are explanatory field names, not prescribed canonical schema. | **CANONICAL requirement + INFERENCE for field names** |
| Confidence | Keep evidence confidence separate from owner commitment. Confidence answers how strongly evidence supports the interpretation; commitment answers whether an owner chooses to rely on it. | **CANONICAL** |
| Provenance | Point back to the selected source or Inventory evidence selector so the interpretation can be inspected and invalidated. | **CANONICAL** |
| Promotion | Carry candidate/reviewed/promoted/demoted/deferred posture, next gate, and owner route. Useful or well-evidenced does not mean promoted. | **CANONICAL** |
| Use rule | State permitted use, warnings, contradiction/drift/invalidation routes, and the condition under which a human or agent must stop or abstain. | **CANONICAL + PRESENTATION SYNTHESIS** |

The smallest retellable tuple is:

**PRESENTATION SYNTHESIS**

`typed thing + typed relationship + time + evidence confidence + provenance + lifecycle posture + use/stop rule`

This is a presentation compression, not a new canonical data schema.

### 3. Concrete temporal-confidence example

**INFERENCE — illustrative presentation witness, not an actual repository event**

At 09:00, a test report says rollback is available for **Build A**. The ontology records:

- the report was observed at 09:00;
- it supports the claim “rollback is available for Build A”;
- it is valid only for Build A and until its declared expiry or a superseding build;
- its evidence confidence is high for that bounded claim;
- deployment still requires the release owner’s decision route.

At 14:30, **Build B supersedes Build A**. The 09:00 report remains valid historical evidence about Build A, but it is no longer valid evidence for deploying Build B. Current-use confidence becomes unknown until Build B is retested. Even strong owner commitment cannot substitute for the missing evidence or silently promote the deployment claim.

This example distinguishes:

`observed time → validity interval → expiry/supersession → current confidence → owner-gated action`

It also supports a concrete agent response: “I cannot recommend deployment yet because the selected evidence does not establish rollback support for the current build.”

### 4. Inventory versus ontology versus authority

**CANONICAL + PRESENTATION SYNTHESIS**

| Layer | Its job | What it cannot establish |
|---|---|---|
| Source | Holds the owned record or event. | Its presence alone does not establish the selected interpretation. |
| Inventory | Makes source-backed evidence and selectors findable; groups evidence for retrieval and handoff. | An index row, evidence card, or EvidenceSet is not an ontology node or authority. |
| Ontology | Types selected meaning, relations, evidence posture, time/confidence, lifecycle state, and use boundaries. | It cannot approve, promote, or make itself canonical. |
| Authority route | The responsible owner or gate decides what may count and where it may be relied upon. | A decision does not retroactively make every source, view, or inference authoritative. |
| Projection/read model | Presents a bounded view for a person or agent. | A useful view, dashboard, graph, or receipt is not authority. |

Room shorthand:

> Inventory finds the receipts. Ontology explains what they mean and how they may be used. Authority decides what may count.

The safe internal ladder is:

`source selector → Inventory evidence → ontology candidate → promotion record/gate → governed artifact or projection → generated read model`

The arrows represent review and ownership transitions, not automatic ingestion.

### 5. What an agent may receive and what it must not assume

**CANONICAL + PRESENTATION SYNTHESIS**

An agent may receive a bounded ontology-derived context containing:

- selected typed objects and relations;
- source references or digests;
- scope, validity, expiry, freshness, and contestation;
- evidence confidence and lifecycle posture;
- selected and excluded items, omissions, truncation, and match reasons;
- contradictions, drift, residue, and invalidation routes;
- permitted-use guidance, warnings, and an explicit stop or abstention condition.

It must not assume:

- retrieved means true, current, complete, canonical, or approved;
- high evidence confidence means high owner commitment;
- evidence or a validation receipt grants authority;
- a graph projection is the source record;
- traversal is reasoning;
- a model explanation can add premises, change a deterministic result, repair a source, or authorize action;
- no retrieved match means the source corpus contains nothing;
- a pending correction is accepted or persisted;
- ontology-derived context is durable agent memory;
- a useful candidate, projection, or presentation proves implementation, promotion, release, or production readiness.

The operative agent rule is:

**PRESENTATION SYNTHESIS**

> Receive the smallest evidence-bound view needed for the task, including its warnings; act only within its stated use posture, and abstain or route to the owner when evidence, validity, or authority is insufficient.

### 6. Exact selector matrix

These are private authoring selectors and must not appear as projected or spoken audience copy.

| Load-bearing claim | Classification | Exact selector |
|---|---|---|
| “Knowledge space/world model” is the author’s opening, not canonical wording. | **AUTHOR VOICE** | `research/2026-08-03-ontology-authority-agent-context-presentation/dispatch-sheet.json` → `context`; `groups[group_id="explorers"].agents[agent_name="Ashby, W. Ross"].initial_prompt` |
| Ontology is a governed typed meaning layer with provenance, confidence, promotion posture, and use obligations. | **CANONICAL** | `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:873-895` |
| Ontology is selected and intended-use-bound; confidence includes scope, validity, and expiry. | **CANONICAL** | `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:897-919` |
| Ontology supports usable meaning after source discovery and Inventory lookup. | **CANONICAL** | `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:921-932` |
| “Map of meaning with typed links, receipts, and rules for use,” plus the non-collapse boundary. | **CANONICAL** | `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:934-967` |
| Evidence confidence, commitment, provenance, ownership, and lifecycle status must not impersonate one another. | **CANONICAL** | `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:1321-1348`; `:1379-1404` |
| Authority kinds route review but do not decide or canonicalize candidates. | **CANONICAL candidate contract** | `cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md:6-21`; `:37-45` |
| Ontology can model authority but cannot promote itself or replace owner routes. | **CANONICAL candidate-package boundary** | `cyberAlchemy-v2/ontology/README.md:6-18`; `:20-31` |
| Inventory-to-ontology-to-authority is a gated ladder, not automatic promotion. | **PRESENTATION SYNTHESIS, source-backed** | `.arcanum/inventory/entries/ontology-population-from-inventory-synthesis.md:31-68`; `:70-92`; `:109-138` |
| Prior accepted room thesis and Inventory/ontology/authority distinction. | **PRESENTATION SYNTHESIS** | `cyberAlchemy-v2/development/research/2026-06-22-simple-ontology-presentation-corpus/findings.md:130-149`; `:187-208` |
| Relations, evidence, commitment, consequence, and refusal must remain distinct. | **PRESENTATION SYNTHESIS** | `cyberAlchemy-v2/development/research/2026-06-22-simple-ontology-presentation-corpus/findings.md:55-72`; `:175-185` |
| Agents may receive typed context with warnings, but retrieval does not authorize action. | **PRESENTATION SYNTHESIS** | `cyberAlchemy-v2/development/research/2026-06-22-simple-ontology-presentation-corpus/findings.md:199-208`; `:228-235`; `:237-252` |
| Explicit ontology overclaim prohibitions. | **PRESENTATION SYNTHESIS, auditor-repaired** | `cyberAlchemy-v2/development/research/2026-06-22-simple-ontology-presentation-corpus/findings.md:254-277` |
| The prior presentation EvidenceSet is a candidate read model, not definition or presentation authority. | **CANONICAL inventory posture** | `.arcanum/inventory/entries/evidence-sets/2026-06-22-simple-ontology-presentation-sets.md:17-20`; `:22-55` |
| Bounded projection, reasoning result, presentation, and source ownership must not collapse. | **PRESENTATION SYNTHESIS from design evidence** | `research/2026-07-28-authority-memory-augmentor-integration/findings.md:5-19`; `:32-43`; `:186-233` |
| Deployment refusal witness and its specification-only ceiling. | **PRESENTATION SYNTHESIS basis; temporal overlay is INFERENCE** | `research/2026-07-28-authority-memory-augmentor-integration/findings.md:235-265` |
| Missing match, stale context, model explanation, correction, and authorization boundaries. | **PRESENTATION SYNTHESIS from design evidence** | `research/2026-07-28-authority-memory-augmentor-integration/findings.md:296-311`; `:342-344` |

### Claim ceiling

This return supports presentation research and synthesis only. It does not replace the canonical definition, prescribe a complete ontology schema, prove agent memory or reasoning implementation, promote any candidate, authorize reliance, refresh stale Augmentor evidence, grant release, or establish production readiness.

## Agent 2 — Pedagogy and agent memory

## Pedagogy and agent-memory explorer return

### Evidence posture

This is a composition recommendation for an assumed mixed business, product, and technical audience. It is not a complete deck, a canonical definition, or evidence that an agent-memory runtime exists. The first authored artifact must remain the three-moment language audition; full generation stays blocked until operator voice approval.

### Concrete opening problem

Open on one operational failure:

> An agent finds a record marked “approved” and prepares to act. The record is genuine—but it describes an earlier pilot, its validity has expired, and a later review may supersede it.

Do not name ontology yet. Let the room first feel the difference between finding the right noun and understanding what may currently be done.

Ask:

> “Should the agent proceed? Vote yes or no—and name the one fact your answer depends on.”

Take the vote and two short reasons. Record the reasons verbally without judging them. Promise to return to the question after the map has acquired meaning, relations, time, confidence, and a gate. This is genuine interaction because the audience supplies the dependency they consider decisive; the presenter later locates those dependencies in the mechanism rather than revealing a canned answer immediately.

A question-before-reveal structure has relevant experimental support: Richland, Kornell, and Kao found a pretesting benefit across five experiments even when initial retrieval failed. That study concerns learning from an essay, not live presentations, so it supports the interaction as a design hypothesis rather than guaranteeing this room’s outcome. [Richland, Kornell, and Kao, “The pretesting effect: do unsuccessful retrieval attempts enhance learning?”, 2009, DOI 10.1037/a0016496](https://pubmed.ncbi.nlm.nih.gov/19751074/).

### Retell chain

Give the room four beats:

1. **Find evidence.** Sources and events produce records; retrieval locates a relevant subset.
2. **Make meaning.** Ontology types the things, names their relations, attaches provenance, and states what time and confidence qualify the interpretation.
3. **Bound context.** The agent receives only the task-relevant slice, including contradictions, expiry, uncertainty, and explicit warnings.
4. **Gate use.** An authority route decides whether the agent may act, must ask, or must stop.

Short retell:

> “Find the evidence. Make the meaning. Bound the context. Gate the action.”

The expanded chain must remain visible in notes:

> source/event → selected evidence → typed meaning → relations → time and confidence → bounded context with warnings → authority gate → act, ask, or stop.

This preserves the prior distinction that Inventory finds receipts, ontology interprets their meaning, and ontology cannot approve itself.

### Recommended 15-minute spine

| Time | Moment | Audience job |
|---|---|---|
| 0:00–1:20 | Failure and vote | Decide whether the agent should act from the found record. |
| 1:20–2:40 | Tension | See that retrieval found relevant bytes but did not establish current permission. |
| 2:40–4:20 | First reveal | Earn “ontology” as a bounded knowledge space or world model: a model of this domain’s important meanings, not a complete model of reality. |
| 4:20–6:20 | Objects and relations | Add typed things and verb-labelled relations such as supports, contradicts, supersedes, and governs. |
| 6:20–8:10 | Time, confidence, provenance | Add observed time, validity interval, expiry/supersession, confidence with rationale, and source receipt. |
| 8:10–10:30 | Memory, context, ontology | Separate retained material, task-selected material, interpretation, and permission. |
| 10:30–12:20 | Replay the opening | Construct the bounded context and reveal: the agent cannot act from the retrieved record alone. |
| 12:20–13:50 | Augmentor bridge | Introduce the private candidate ontology only as a concrete attempt to encode these separations; preserve its candidate-local, no-authority, no-release ceiling and do not use stale visualization receipts as proof. |
| 13:50–15:00 | Audience retell | Ask one person to repeat the four beats; repair only the missing distinction, then close on “the map informs the route; it does not grant permission.” |

Nine audience moments are plausible; they are not nine mandatory slides. The first audition should sample the opening, the retrieval-is-not-permission tension, and the bounded-world-model reveal.

### Memory, context, ontology, and authority

Use one stable spatial analogy, then leave the analogy behind:

- **Memory is retained material:** prior events, claims, observations, and interaction history that may be available again. Retention does not make it correct, current, or authoritative.
- **Context is the selected working packet:** the bounded subset placed before the agent for this task, with source references and warnings. Context is temporary and purpose-specific.
- **Ontology is the meaning contract:** it states what kinds of things those records concern, how they relate, when interpretations apply, how confidence is represented, and what use constraints travel with them. It is not the storage system or the context window.
- **Authority is the decision boundary:** it determines what may be relied upon or changed. Neither retrieval, memory, context selection, nor ontology admission grants that permission by itself.

The pedagogical contrast is:

> Memory preserves candidates. Context selects candidates. Ontology interprets candidates. Authority governs reliance.

“Candidates” matters: memory may contain both valid and invalid material, and context selection may still retrieve stale or contradictory evidence.

### Visual grammar and progressive disclosure

Use one persistent scene. Do not replace it with successive unrelated graphs.

- Sources are grey document/event rectangles.
- Typed meanings are labelled shapes whose form distinguishes kind; never rely on color alone.
- Relations are arrows labelled with verbs. An unlabeled edge is not explanatory.
- Provenance is a visible receipt link back to a source.
- Time is a horizontal axis showing observed-at, valid-from/to, expiry, and supersession as distinct marks.
- Confidence is a textual badge plus a short basis, not opacity, glow, or a universal “truth percentage.”
- Context is a clearly bounded frame around the selected subset. Anything excluded remains faintly visible only when exclusion itself matters.
- Warnings travel inside that frame.
- The authority gate is physically outside the ontology view. The audience should see that the map reaches the gate but cannot open it.
- Keep node positions stable and reveal one semantic layer at a time: record → type → relation → provenance → time/confidence → context boundary → gate.
- Keep one visible thought per moment. Put timing, evidence selectors, claim ceilings, and construction intent in notes or authoring metadata, never projected copy.
- Label every repository rendering as a **view of a model**, not “the ontology itself.”

Mayer and Chandler’s two multimedia-learning experiments found transfer advantages for part-first, learner-paced presentations compared with whole-first or uninterrupted presentations. Applying that finding to a presenter-paced live room is an inference, but it supports revealing the stable model in meaningful segments before showing the whole mechanism. [Mayer and Chandler, “When Learning Is Just a Click Away: Does Simple User Interaction Foster Deeper Understanding of Multimedia Messages?”, 2001, DOI 10.1037/0022-0663.93.2.390](https://doi.org/10.1037/0022-0663.93.2.390).

### Likely misconceptions and bounded repairs

| Misconception | Repair |
|---|---|
| “World model” means a complete or true model of reality. | Say “a bounded model of the meanings this domain currently needs, with explicit evidence, time, uncertainty, and use limits.” |
| A node-edge picture is automatically an ontology. | A graph is a view; ontology requires typed semantics, meaningful relations, provenance, and use constraints. |
| Confidence means probability of truth. | Confidence qualifies a scoped interpretation and must carry its basis; it is not approval. |
| The newest record is necessarily current. | Separate observation time, validity interval, expiry, and supersession. |
| Memory and ontology are the same store. | Memory retains; ontology interprets; context selects. |
| More retrieved context is always safer. | Irrelevant, stale, or contradictory material can mislead; selection must be bounded and warning-bearing. |
| Retrieval or graph insertion grants permission. | Evidence is not permission, and the map is not the government. |
| A validated view proves working memory or reasoning. | Structural or visualization validation proves only its named checks, not routing, durable memory, reasoning integration, promotion, release, or runtime effect. |

### Exact source selectors

Authoring-only; do not project private paths or identifiers.

- Prior thesis and meaning/authority boundary: `cyberAlchemy-v2/development/research/2026-06-22-simple-ontology-presentation-corpus/findings.md` → `## Presentation Thesis`, lines 130–149.
- Prior narrative and agent-context language: same file → `## Five-Slide Spine`, lines 151–208; `## Presentation Script Seeds`, lines 210–235.
- Forbidden collapses and authority ceiling: same file → `## Forbidden Overclaims`, lines 254–277.
- Mixed-audience assumption and required metaphors/boundaries: same file → `## Presentation Intake Substrate`, lines 279–325.
- Source/index/context/candidate/authority separation: `research/2026-08-03-ontology-authority-agent-context-presentation/strategy-inventory-packet.json` → JSON Pointer `/selected/3`, especially `/selected/3/obligation_fit` and `/selected/3/lane_effect`.
- Required retell mechanism, terminology order, time/confidence treatment, and Augmentor ceiling: same packet → `/design_consequences/1` through `/design_consequences/5`.
- Current Augmentor drift boundary: same packet → `/selected/4/live_verification` and `/unresolved_gaps/5` through `/unresolved_gaps/6`.
- Live-room surface separation, genuine-question rule, audition gate, and one-thought rule: `.claude/skills/whisper/presets/live-presentation/preset.yaml` → `/surface_contract`, `/audition_gate`, `/composition_contract`, and `/validation`.
- Interaction research: [Richland, Kornell, and Kao 2009, DOI 10.1037/a0016496](https://pubmed.ncbi.nlm.nih.gov/19751074/).
- Segmented-reveal research: [Mayer and Chandler 2001, DOI 10.1037/0022-0663.93.2.390](https://doi.org/10.1037/0022-0663.93.2.390).

## Agent 3 — Repository examples

## Repository-example explorer: selected presentation witnesses

### Verdict

Use exactly three examples:

1. Body War’s GeometryCandidate-to-ScorePreview slice for temporal meaning, confidence, provenance, and explicit non-promotion.
2. DomainSpec’s `Rule --enforces--> Operation` signature for typed relations as implementation-facing obligations without implementation proof.
3. Augmentor’s knowledge and authority-bridge views for bounded agent context, memory intake, ontology candidates, and retained owner authority.

The examples perform different teaching jobs. The prior simple-ontology corpus and CAV2-D19 remain framing and definition evidence, not additional examples.

### Example 1 — Body War: meaning changes with state, confidence, and use limits

**Audience question:** How can the same graph say what something means now, how confident we are, what may happen next, and what must not be concluded?

**Show:** Use `projects/body-war/ontology/business/generated/views/candidate-geometry-to-score-preview.svg`, but progressively spotlight only:

- `body-war.business.entity.geometry-candidate`;
- `body-war.business.outcome.score-preview`;
- `body-war.business.policy.score-policy`;
- `body-war.business.outcome.source-backed-track`;
- the `available`, `blocked-policy`, `blocked-geometry`, and `superseded` ScorePreview states.

Use these exact relations:

- `body-war.relation.preview-governed-policy`;
- `body-war.relation.score-preview-projects-zone-score`;
- `body-war.relation.geometry-does-not-promote`;
- `body-war.relation.preview-does-not-promote`.

The key visible contrast is:

```text
ScorePreview --projects--> Zone Score
ScorePreview --does_not_promote--> Source-Backed Track
```

**Exact selectors:**

- `projects/body-war/ontology/business/BUSINESS-VIEWS.md:259-346`
- `projects/body-war/ontology/business/nodes/entity.geometry-candidate.json:23-43`
- `projects/body-war/ontology/business/nodes/outcome.score-preview.json:24-44`
- `projects/body-war/ontology/business/lifecycle-policies/score-preview.json:16-77`
- `projects/body-war/ontology/business/relations/relations.json:1742-1762`
- `projects/body-war/ontology/business/relations/relations.json:3183-3214`
- `projects/body-war/ontology/business/relations/relations.json:3678-3742`
- `projects/body-war/ontology/business/profile.json:64-70`
- `projects/body-war/ontology/business/receipts/validation-receipt.json:2-53`

**Current validation:** Read-only validation at 2026-08-03T17:14Z returned `pass` with 237 nodes, 231 relations, 11 lifecycle policies, 34 bound sources, and no diagnostics. The six structural tests passed, and `generate-views.mjs --check` reported all six graph views, five lifecycle views, and three HTML projections current.

**Claim ceiling:** A validated, source-bound candidate business-meaning graph and current generated explanatory projection. It does not establish implementation, live data, scoring authority, privacy-policy resolution, promotion, release, or production behavior.

**Time value:** About 2 minutes 15 seconds. It earns the time because one concrete object demonstrates typed meaning, two independent confidence axes, lifecycle change, blocking conditions, provenance, and a negative relation that prevents an attractive but false conclusion.

**Must not imply:**

- that the diagram is an executed workflow;
- that candidate geometry is source-backed or public geometry;
- that an available preview is a verified score or controller verdict;
- that green validation promotes any node or resolves its owner residue.

### Example 2 — DomainSpec: a relation carries obligations, not just a line

**Audience question:** What does a typed relation add beyond drawing an arrow between two nouns?

**Show:** One relation card only:

```text
Rule --enforces--> Operation
```

Reveal its endpoint types, direction, same/cross-feature scope, positive and negative examples, rejection obligations, and implementation-facing composition: `operation_checks_rule_before_mutation`.

**Exact selectors:**

- `projects/domainspec-v2/definitions/relationships/relationships.yml:101-114`
- `projects/domainspec-v2/impl/tools/validate-relationships.ts:24-74`
- `projects/domainspec-v2/development/research/2026-07-30-implementation-structure-enforcement/findings.md:3-38`
- `projects/domainspec-v2/development/research/2026-07-30-implementation-structure-enforcement/findings.md:217-230`
- `projects/domainspec-v2/research/2026-07-17-spec-ontology-node-layering/findings.md:144-151`

**Current validation:** `npm run validate:rels` passed against six current specs, 34 checked edges, and 31 canonical signatures.

**Claim ceiling:** The active relationship registry defines and validates a typed semantic signature and records an intended composition obligation. It does not prove that application code calls the rule, that the proposed `ImplementationConformanceProfile` exists, or that runtime behavior conforms. The implementation-structure findings explicitly classify the proposed fixture as `[EXECUTED] none`.

**Time value:** About 1 minute 30 seconds. It earns the time because it turns “relations matter” into a falsifiable contract: wrong endpoint, wrong direction, or invented verb is rejected, while implementation conformance remains a separate evidence problem.

**Must not imply:**

- that relationship validation is code-conformance validation;
- that `composition` proves a runtime call;
- that the proposed implementation profile is implemented or admitted;
- that semantic admission grants release or production authority.

### Example 3 — Augmentor: ontology-derived context without memory or authority collapse

**Audience question:** What should an agent receive from an ontology, and what must remain outside the agent’s authority?

**Show:** Do not use the generated HTML visualization. Build the closing reveal from the source view’s two small sequences:

```text
SourceRecord
→ DisposableSemanticIndex
→ ContextSnapshot
```

and:

```text
MemoryIntakeRequest
→ provider review and Inventory validation
→ OntologyCandidate
→ named-owner AuthorityDecision
```

Then reveal the decisive edge:

```text
OntologyCandidate --requests_promotion_gate--> AuthorityDecision
```

with `authority_effect: none`.

**Exact selectors:**

- `projects/augmentor/ontology/unified-agent/README.md:109-129`
- `projects/augmentor/ontology/unified-agent/views/knowledge.json#/sequences/AUG-KNOW-GROUNDING`
- `projects/augmentor/ontology/unified-agent/views/knowledge.json#/sequences/AUG-KNOW-EVOLUTION`
- `projects/augmentor/ontology/unified-agent/views/knowledge.json:56-67`
- `projects/augmentor/ontology/unified-agent/views/authority-bridge.json:41-75`
- `projects/augmentor/ontology/unified-agent/nodes/nodes.json` concepts `aug.concept.source_record`, `aug.concept.disposable_semantic_index`, `aug.concept.context_snapshot`, `aug.concept.memory_intake_request`, `aug.concept.ontology_candidate`, and `aug.concept.authority_decision`
- `projects/augmentor/ontology/unified-agent/relations/relations.json` relations `aug.relation.index_derives_from_source`, `aug.relation.context_uses_bounded_index_projection`, `aug.relation.source_supports_context`, `aug.relation.intake_requests_provider_review`, `aug.relation.source_supports_candidate`, and `aug.relation.candidate_requests_named_owner`
- `projects/augmentor/ontology/unified-agent/profile.json:5-8,69-78`

**Current validation and drift boundary:** The frozen strategy packet records a blocked check: stale stored receipt and stale generated visualization (`strategy-inventory-packet.json:112-121`). This explorer did not regenerate or repair either artifact.

A later read-only check of the concurrently modified working-tree bytes at 2026-08-03T17:14Z returned:

- package validator: pass, 25 sources, 22 nodes, 28 relations, five views, seven residue items;
- structural tests: 6/6 pass;
- visualization check: pass, SHA-256 `201ff207de9927b59af918471c5e9205ae5c55a5d60b01f401c1598050f46827`;
- visualization tests: 6/6 pass.

That discrepancy is a time-scoped worktree-drift observation, not proof that an authorized owner refresh, lifecycle reconciliation, or stable acceptance occurred. The presentation should therefore source the compact chain directly from `views/knowledge.json` and `views/authority-bridge.json`, not treat the generated visualization or stored receipt as settled acceptance evidence.

**Claim ceiling:** A private, source-bound, candidate-local model with `authority_effect: none` and `release_admission: not-granted`. Current checks establish structural consistency only. They do not establish working routing, durable memory, a reasoning engine, promotion, release, or production readiness.

**Time value:** About 2 minutes. It earns the time because it converts the preceding ontology concepts into an agent-use boundary: retrieval can select context; intake can request review; ontology can propose meaning; only a named owner can decide authority.

**Must not imply:**

- that an index or selected context is source truth;
- that displaying or consuming a result writes durable memory;
- that a MemoryIntakeRequest is provider acceptance;
- that Inventory validation is ontology promotion;
- that an OntologyCandidate is an AuthorityDecision;
- that routing, memory, reasoning, promotion, or release is implemented.

### Clean transition into Augmentor

Suggested audience-facing transition:

> “The first example showed why meaning needs time, confidence, and limits. The second showed why an arrow needs a type and a testable obligation. Now ask what happens when an agent must use that map. The agent should not receive the whole repository or permission to rewrite it. It receives a bounded context snapshot with provenance and warnings; it may propose new meaning, but it cannot turn that proposal into memory or authority by itself. That is the boundary the Augmentor ontology is designed to make visible.”

### Compared but not selected

- **CAV2-D19 and the prior simple-ontology corpus:** retain as internal definition and narrative evidence. They are the explanatory frame, not repository examples. Relevant selectors are `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:873-967` and `cyberAlchemy-v2/development/research/2026-06-22-simple-ontology-presentation-corpus/findings.md:130-208`.
- **Interactive ontology learning map:** do not spend presentation time on it. Its current work pack records a stale historical A2 generation, gated A3/A4 validation, no browser-acceptance handle, and multiple blocked/not-started primary slices (`WORK-PACK.md:48-82,90-98`). It is useful projection-design precedent, not the cleanest current witness.
- **DomainSpec implementation-conformance proposal:** do not treat it as a fourth example. Its useful current piece is the already-active `enforces` relationship; the broader conformance model remains evidence-closed research and implementation-open.
- **Body War whole atlas:** do not tour it. The selected GeometryCandidate/ScorePreview slice already supplies the domain teaching job; more views would add visual coverage without adding a distinct mechanism.

No repository or external artifact was written by this explorer.
