# Presentation research synthesis

## Verdict

The package fits fifteen minutes, preserves every load-bearing distinction, uses three repository examples for distinct teaching jobs, and introduces Augmentor within its candidate-local ceiling. It is ready for definitional-soundness and non-vacuity review. It is research synthesis, not the final deck.

## Room thesis

> Ontologies are knowledge spaces—bounded world models of the things a domain cares about and how they interact—and CyberAlchemy v2 sharpens that idea into governed, typed meaning whose evidence, provenance, time, confidence, lifecycle posture, and rules for use remain distinct from authority.

Immediately say that “world model” does not mean a complete model of reality or a truth machine. It is selected for a domain and intended use.

## Audience assumption

Mixed business, product, and technical listeners who understand agents and organizational knowledge at a conceptual level but should not need graph theory, ontology engineering, or repository familiarity.

## Retellable mechanism

Projected shorthand:

> Find evidence. Make meaning. Bound context. Gate action.

Speaker-notes expansion:

> source or event → selected evidence → typed meaning → named relations → time, confidence, and provenance → bounded context with warnings → authority gate → act, ask, or stop

The four verbs preserve the system boundary:

- Inventory or retrieval finds source-backed evidence.
- Ontology interprets selected evidence.
- Context packages the task-relevant slice.
- Authority governs reliance and action.

## Fifteen-minute spine

| Time | Moment | Projected thought | Spoken and visual job |
|---|---|---|---|
| 0:00–1:05 | Approved definition | **Ontologies are knowledge spaces.** | Deliver the approved spoken opening. Immediately bound the “world” as selected and purpose-specific, not total reality. Begin with one grey source record and an empty map. |
| 1:05–2:15 | Failure and vote | **Should the agent proceed?** | An agent retrieves a genuine “approved” pilot record whose validity expired and which may have been superseded. Ask for yes/no and the one fact each answer depends on. Preserve two reasons without resolving them. |
| 2:15–3:05 | Tension | **More memory can make an agent more confidently wrong.** | Retrieval found relevant bytes but did not establish currency, meaning, or permission. Preview the four-beat retell chain. |
| 3:05–4:30 | Typed relations | **An arrow must say what it does.** | Use DomainSpec’s single `Rule --enforces--> Operation` relation. Reveal endpoint kinds, direction, accepted and rejected shapes, then state that semantic validation does not prove runtime enforcement. |
| 4:30–6:40 | Time, confidence, provenance | **Meaning has a time horizon.** | Use Body War’s GeometryCandidate/ScorePreview slice. Reveal lifecycle states, blocking conditions, provenance, two distinct confidence axes, and `does_not_promote`. Show that a current-looking candidate or preview is not a source-backed outcome. |
| 6:40–8:10 | Meaning and authority ladder | **The map is not the authority.** | Build `source → Inventory evidence → ontology candidate → promotion gate → governed projection`. Explain that each arrow is an owner/review transition, never automatic ingestion. Separate evidence confidence from owner commitment. |
| 8:10–9:40 | Agent memory and context | **Retain ≠ select ≠ interpret ≠ authorize.** | Memory retains candidates; context selects a task packet; ontology interprets it; authority governs reliance. Draw a context boundary around only the relevant nodes, carrying source references, expiry, contradiction, uncertainty, omissions, and a stop condition. |
| 9:40–11:00 | Replay the vote | **Act, ask, or stop?** | Add the missing facts to the opening record: expired validity, possible supersession, and no current authority decision. The agent must ask or stop because retrieval alone does not support action. Map the audience’s earlier reasons onto time, confidence, provenance, or authority. |
| 11:00–13:15 | Augmentor bridge | **Context can be bounded. Authority must remain owned.** | Reveal `SourceRecord → DisposableSemanticIndex → ContextSnapshot`, then `MemoryIntakeRequest → review → OntologyCandidate → AuthorityDecision`. Finish on `OntologyCandidate --requests_promotion_gate--> AuthorityDecision`, with `authority_effect: none`. |
| 13:15–14:15 | Whole mechanism | **Find. Make meaning. Bound. Gate.** | Show the completed stable scene once. Point from source through context to the external gate; do not add new terminology. |
| 14:15–15:00 | Audience retell | **What are the four beats?** | Ask one person to repeat the chain. Repair only a missing distinction. Close: “The map informs the route; it does not grant permission.” |

Timing totals exactly fifteen minutes. The vote is genuine because its rationale is supplied by the audience and resolved only after the mechanism is visible.

## Definition ladder

1. **Nouns become typed objects.** Identity, kind, scoped meaning, and role or owner context.
2. **Lines become typed relationships.** Named verbs such as `supports`, `contradicts`, `supersedes`, `constrains`, and `realizes`; adjacency alone explains nothing.
3. **Meaning becomes time-scoped.** Separate observation time, validity interval, expiry, and supersession.
4. **Confidence gains a basis.** Confidence qualifies bounded evidence or interpretation; it is neither a universal truth percentage nor owner commitment.
5. **Claims retain provenance.** A person or agent can inspect the selected source and invalidate the interpretation when it drifts.
6. **Candidates carry lifecycle and use posture.** Candidate, reviewed, promoted, demoted, deferred; permitted use, warnings, contradiction routes, and stop conditions.
7. **Authority stays external.** Ontology may model an authority route or request its gate; it cannot approve or promote itself.

Presentation compression only:

> typed thing + typed relationship + time + evidence confidence + provenance + lifecycle posture + use/stop rule

Do not present this tuple as a canonical schema.

## Three repository examples

### 1. DomainSpec — relation semantics

Teaching job: prove that a relationship is a falsifiable semantic contract, not decorative graph ink.

Show only:

> Rule —enforces→ Operation

Reveal endpoint types, direction, scope, positive/negative examples, and the intended composition obligation. State explicitly that relationship validation does not prove the application calls the rule.

Selectors:

- `projects/domainspec-v2/definitions/relationships/relationships.yml:101-114`
- `projects/domainspec-v2/impl/tools/validate-relationships.ts:24-74`
- `projects/domainspec-v2/development/research/2026-07-30-implementation-structure-enforcement/findings.md:3-38`
- same file `:217-230`

Ceiling: active semantic signature and intended obligation; no runtime-conformance, admission, release, or production claim.

### 2. Body War — temporal meaning, confidence, and non-promotion

Teaching job: show that a typed object’s safe meaning depends on lifecycle state, evidence, confidence, and negative relations.

Show only the GeometryCandidate/ScorePreview slice and this contrast:

> ScorePreview —projects→ Zone Score  
> ScorePreview —does_not_promote→ Source-Backed Track

Selectors:

- `projects/body-war/ontology/business/BUSINESS-VIEWS.md:259-346`
- `projects/body-war/ontology/business/nodes/outcome.score-preview.json:24-44`
- `projects/body-war/ontology/business/lifecycle-policies/score-preview.json:16-77`
- `projects/body-war/ontology/business/relations/relations.json:3183-3214`
- same file `:3678-3742`
- `projects/body-war/ontology/business/profile.json:64-70`

Ceiling: validated, source-bound candidate meaning graph and explanatory projection; no executed workflow, live scoring, authority, privacy resolution, promotion, release, or production claim.

### 3. Augmentor — bounded context and retained authority

Teaching job: demonstrate what an agent can receive and what it cannot decide.

Build the visual directly from source-view sequences:

> SourceRecord → DisposableSemanticIndex → ContextSnapshot

> MemoryIntakeRequest → provider review and Inventory validation → OntologyCandidate → named-owner AuthorityDecision

Decisive edge:

> OntologyCandidate —requests_promotion_gate→ AuthorityDecision  
> `authority_effect: none`

Selectors:

- `projects/augmentor/ontology/unified-agent/README.md:109-129`
- `projects/augmentor/ontology/unified-agent/views/knowledge.json#/sequences/AUG-KNOW-GROUNDING`
- same file `#/sequences/AUG-KNOW-EVOLUTION`
- `projects/augmentor/ontology/unified-agent/views/authority-bridge.json:41-75`
- `projects/augmentor/ontology/unified-agent/profile.json:5-8,69-78`

Ceiling: private, source-bound, candidate-local model with `authority_effect: none` and `release_admission: not-granted`. Current structural checks cannot establish working routing, durable memory, reasoning, promotion, release, or production readiness.

The frozen packet and later worktree checks disagree because bytes changed concurrently. Do not use the generated visualization or stored receipt as settled acceptance evidence. Recheck currentness immediately before deck authoring or delivery and continue to source the compact diagram from the two JSON views.

## Agent-use contract

An ontology-derived context may contain selected typed objects and relations, source references, validity and expiry, confidence and rationale, contradictions, omissions, lifecycle posture, warnings, permitted use, and a stop condition.

The agent must not infer that:

- retrieved means true, current, complete, canonical, or approved;
- high confidence means owner commitment;
- a context snapshot is durable memory;
- a request for memory intake is provider acceptance;
- an ontology candidate is an authority decision;
- traversal is reasoning;
- validation proves runtime behavior;
- absence from the selected context means absence from the source corpus.

Operative rule:

> Give the agent the smallest evidence-bound view needed for its task, including warnings; when validity, evidence, or authority is insufficient, it must abstain or route to the owner.

## Visual and surface contract

Use one persistent scene and reveal layers without moving existing elements:

1. grey source record;
2. typed shapes;
3. verb-labelled arrows;
4. visible provenance receipt;
5. horizontal time axis;
6. confidence badge with textual basis;
7. bounded context frame containing warnings;
8. authority gate physically outside the ontology.

Never rely on color alone. Never encode confidence as glow, opacity, or an unexplained percentage. Label repository images as “a view of the model,” not “the ontology itself.”

Surface separation:

- Projected copy: one thought, minimal words, no private paths or IDs.
- Spoken copy: human explanation and transitions.
- Speaker notes: timing, caveats, interaction handling, and claim ceilings.
- Authoring metadata: exact selectors, validation observations, provenance, and construction intent.

The progressive reveal is evidence-informed, not guaranteed: Mayer and Chandler’s segmented multimedia result is only an analogy to this presenter-paced room. The question-before-reveal interaction is likewise a design hypothesis informed by Richland, Kornell, and Kao’s pretesting experiments, not proof of a live-presentation outcome.

## Forbidden collapses

Reject any wording that implies:

- world model = complete or universally true reality;
- ontology = glossary, taxonomy, database, graph shape, memory store, or context window;
- source = index = context snapshot;
- confidence = probability of truth = owner commitment;
- selected evidence = promotion or approval;
- newest record = currently valid record;
- memory intake request = persisted memory;
- ontology candidate = authority decision;
- graph traversal = reasoning;
- structural validation = working routing or durable memory;
- candidate-local = released or production-ready.

## Core source-selector matrix

| Claim | Exact authoring selector |
|---|---|
| Canonical governed-meaning refinement | `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:873-967` |
| Evidence confidence, commitment, provenance, ownership, and lifecycle non-collapse | same file `:1321-1348`; `:1379-1404` |
| Ontology cannot promote itself | `cyberAlchemy-v2/ontology/README.md:6-31` |
| Authority kinds route review without canonicalizing candidates | `cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md:6-21`; `:37-45` |
| Inventory-to-ontology gated ladder | `.arcanum/inventory/entries/ontology-population-from-inventory-synthesis.md:31-92`; `:109-138` |
| Approved voice | `research/2026-08-03-ontology-authority-agent-context-presentation/live-presentation-language-audition.md` |
| Prior thesis and forbidden overclaims | `cyberAlchemy-v2/development/research/2026-06-22-simple-ontology-presentation-corpus/findings.md:130-208`; `:254-277` |
| Augmentor source/index/context/candidate/authority separation | `research/2026-07-28-authority-memory-augmentor-integration/findings.md:5-43`; `:186-233`; `:296-311` |
| Current drift boundary | `research/2026-08-03-ontology-authority-agent-context-presentation/strategy-inventory-packet.json#/selected/4/live_verification`; explorer 3 current-check receipt |

All repository paths and internal identifiers are authoring-only.

## Remaining operator choices

These do not block the research package:

- Confirm or adjust the mixed business/product/technical audience assumption.
- Choose whether the interaction uses hands, chat, or a quick poll for the actual room.
- Decide whether the Body War witness uses a cropped existing view or a faithful simplified redraw.
- Recheck Augmentor source and generated-artifact currentness immediately before final composition.
- Run the completed deck aloud once; compress transitions if the audience vote consumes more than seventy seconds.

No implementation, ontology mutation, promotion, publication, deployment, release, or final-deck generation was performed.
