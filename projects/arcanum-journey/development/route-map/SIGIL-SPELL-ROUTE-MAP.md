# Arcanum Sigil/Spell Route Map

> Deliverable of Task Session **SWU-AJ-MAP-1** (Wave 0 / S-000), addressing
> **GAP-AJ-SIGIL-MAP-001**. Built by a 6-way dispatch-spec fan-out over the public
> `arcanum/` library on 2026-06-23. Edges are read from each capability's
> README/SKILL, not guessed. This map powers chapter ordering
> (GAP-AJ-CHAPTER-ORDER-001) and the post-session path recommender.
>
> Durability note: making this an `inventory` package is **SWU-AJ-MAP-2** (still
> pending). This file is the source artifact until then.

## 1. Tier taxonomy (the frame)

Source: `arcanum/README.md`, `arcanum/framework/CYBERALCHEMY-METHOD.md`, tier READMEs.

| Tier | What it is | "How much thinking?" |
| --- | --- | --- |
| **Formulae** | Deterministic, stateless rule/validation/conversion. Never interprets. | pure rule-following |
| **Transmutation** | Bounded cognitive synthesis — reshapes ambiguous input into structure. Interprets, doesn't orchestrate. | judgment, no orchestration |
| **Arcana (sigil)** | Atomic orchestration capability — multi-phase/multi-agent reasoning with gates. | stitch voices into a decision |
| **Spell** | A localized workflow that composes multiple sigils with shared state, phases, gates, handoffs. | guided path through sigils |
| **Discipline** | A cross-capability operating practice (planning, schema discipline, observability) — not itself a capability. | meta-practice |

**Cyber Alchemy method (public-level):** governed synthesis, not prompt execution.
Five anchors kept visible — **objective · artifact · discovery · tension · route** —
through a loop: **Orient → Discover → Shape → Stabilize → Evolve**. Source:
`arcanum/framework/CYBERALCHEMY-METHOD.md` (public). Guardrail honored: only public
arcanum material used; private `cyberAlchemy-v2/` excluded.

## 2. Capability catalog (id · tier · purpose · edges)

Edge legend: **⤳inherits** = consumes as input/depends on · **⊕builds** = what the
user gets · **⇄integrates** = composes/routes to.

### Entry & control
| id | tier | purpose | ⤳inherits | ⊕builds | ⇄integrates |
| --- | --- | --- | --- | --- | --- |
| **craft** | arcana | Project-local recursive ledger (contexts, blockers, decisions, gaps, recomposition). | — | a navigable project ledger | *(control surface — every capability returns here)* |
| **refine** | arcana | Run the canonical refinement loop: vague idea → seed + design via staged receipts. | scope-interview, context-builder | refined seed, dispatch route, synthesis | invoke, interrogation, distill, dispatch-spec |
| **invoke** | spell | Intent → governed define / design / plan / handoff / refresh artifacts. | context-builder, structured-interview-kits, inventory, dispatch-spec | spec, architecture, plan, work-pack | interrogation, distill, decision-gate, spellcraft, sigil-development, task-session, implementation-layering |
| **scope-interview** | arcana | Turn a vague idea/repo into a discovery baseline (observed/stated/hypothesized/decided). | — | discovery baseline | refine, discovery-to-inventory |
| **structured-interview-kits** | arcana | One-question-at-a-time evidence-backed interview (a.k.a. interrogation). | — | artifact updates, decision records | whisper, invoke, distill, task-session |

### Knowledge & ontology
| id | tier | purpose | ⤳inherits | ⊕builds | ⇄integrates |
| --- | --- | --- | --- | --- | --- |
| **inventory** | arcana | Repository-local compiled knowledge wiki LLMs can query. | — | inventory wiki + index, evidence cards | context-builder, ontology-vault, architecture-pattern-inventory |
| **context-builder** | transmutation | Compact task-ready context pack from obligation-linked evidence. | — | context pack (+ runtime handoff) | refine, invoke, task-session |
| **ontology-vault** | arcana | Govern a knowledge vault: map, distill, promote confidence, validate. | — | ontology maps, confidence reports | inventory, context-builder, decision-gate, feature-glossary |
| **necronomicon** | spell | Repository working-memory + session router; query inventory before broad search. | inventory, ontology-vault, context-builder | session memory, route/gap ledgers, handoffs | ontology-harness, invoke, task-session, decision-gate, robot-talks |
| **feature-glossary** | transmutation | Evidence-linked plain+formal glossary from scattered sources. | — | glossary artifact | research-tower, discovery-to-inventory |
| **definitions-governance** | arcana | Keep critical terms authoritative (formal/plain/domain voices) + drift audit. | — | definitions index, drift audit | context-builder, inventory |

### Execution & dispatch
| id | tier | purpose | ⤳inherits | ⊕builds | ⇄integrates |
| --- | --- | --- | --- | --- | --- |
| **task-session** | arcana | Execute one bounded task end-to-end with gates + validation. | refine, context-builder, decision-gate | session report, completion evidence | runtime-adapters, experiment-harness, spellcraft |
| **decision-gate** | arcana | Resolve blocker-level multi-option decisions before consequential work. | — | durable decision record | task-session, goal, invoke, robot-talks |
| **dispatch-spec** | formulae | Validate a route chaining sigils/spells/handoffs is explicit + gated. | — | dispatch document, route verdict | task-session, goal, spellcraft, invoke, robot-talks |
| **codex-goal-profile** | transmutation | Work-pack task/SWU → compact native Codex `/goal`. | task-session, context-builder | native goal line + sidecar | decision-gate, task-session |
| **goal** | spell | Autonomous fail-closed work-graph loop with approval gates. | craft, dispatch-spec, observed-invocation-loop, decision-gate, task-session | staged deltas, approvals, promotions | signal-observer, workflow-reflect, spellcraft, experiment-harness |
| **robot-talks** | arcana | Parallel multi-agent investigation surfacing cross-layer tensions. | — | tension findings + human-gate log | task-session, decision-gate |
| **anti-bias-vector-composition** | formulae | Design opposed multi-agent angle sets so correlated bias cancels. | — | angle-set design | dispatch-spec |
| **implementation-readiness** | spell | Stage layers → resolve blockers → prepare one ready task. | implementation-layering, decision-gate, task-session | layer plan, ready task | decision-gate, task-session |
| **implementation-layering** | transmutation | Sequence scope L0→Ln; each layer unlocks one decision. | — | layering artifact | distill |

### Authoring & governance
| id | tier | purpose | ⤳inherits | ⊕builds | ⇄integrates |
| --- | --- | --- | --- | --- | --- |
| **sigil-development** | arcana | Governed sigil lifecycle: new/update/observe/reflect. | invoke | sigil package + evidence | experiment-harness, observability-setup, signal-observer, workflow-reflect, task-session |
| **spellcraft** | arcana | Compose sigils into a spell with phases/gates/handoffs/observability. | invoke | spell package | sigil-development, experiment-harness, task-session, context-builder, inventory |
| **skill-decomposer** | arcana | Extract one reusable capability from a tangled source. | — | decomposition + handoff | skill-transcriptor, sigil-development |
| **skill-transcriptor** | arcana | Convert a coherent external skill into an Arcanum sigil package. | — | sigil package plan | skill-decomposer, sigil-development |
| **constitution-governance** | arcana | Modular constitutions enforcing structure without context bloat. | — | constitution packs | decision-gate, sigil-development, inventory |
| **discipline-governance** | arcana | Formalize recurring cross-capability practices into discipline cards. | — | discipline card + catalog row | constitution-governance, definitions-governance, sigil-development |
| **sigil-maintenance-loop** | spell | signal-observer + workflow-reflect + sigil-development → improve sigils from use. | signal-observer, workflow-reflect, sigil-development | maintenance report | — |
| **sigil-runtime-installer** | arcana | Install legacy Codex command adapters. | — | command adapters + hooks | observability-setup, task-session |
| **arcanum-bootstrap** | spell | Install Arcanum into a consuming repo (native runtime + observability). | sigil-runtime-installer, observability-setup | `.arcanum/`, runtime packages | spellcraft, inventory, experiment-harness |

### Research, distillation & towers
| id | tier | purpose | ⤳inherits | ⊕builds | ⇄integrates |
| --- | --- | --- | --- | --- | --- |
| **research-tower** | arcana | Paper/corpus/question → reproducible source-backed learning tower. | distill, feature-glossary, research-evidence-harness, definitions-governance | tower + claim ledger + learning pack | task-session, codex-goal-profile, experiment-harness |
| **research-evidence-harness** | arcana | Protocols → validated run schemas + fixtures + metrics. | research-tower | schemas, fixtures, summaries | task-session, publication-research-pipeline |
| **distill** | arcana | Reduce to the smallest coherent unit + prove recomposition. | — | optimized unit + closure proof | implementation-layering, robot-talks, decision-gate, invoke, task-session |
| **reading-learning-package** | spell | Tower result → personalized readable learning package (HTML/PDF). | research-tower, whisper | reading package + validation | experiment-harness, task-session |
| **publication-research-pipeline** | spell | Research question → publishable paper through gated lanes. | refine, dispatch-spec, research-tower, context-builder, research-evidence-harness, task-session | paper package | inventory, definitions-governance, spellcraft |
| **residuality-spec** | arcana | Harden a spec via stressors, residue, degradation, attractors. | — | resilience spec | context-builder, decision-gate, inventory |

### Creative, explanation & UX
| id | tier | purpose | ⤳inherits | ⊕builds | ⇄integrates |
| --- | --- | --- | --- | --- | --- |
| **whisper** | spell | Author meaningful text through a governed composition lifecycle. | structured-interview-kits, distill | text substrate, draft, validation | decision-gate, feature-glossary, context-builder, task-session |
| **x-ray** | arcana | Dissect a target into explanation lanes → visual HTML page. | — | layered HTML explanation | *(standalone; consumed by guide-architecture & the Journey surfaces)* |
| **guide-architecture** | spell | Guide a user through an architecture (context→map→translate→validate). | context-builder, x-ray, inventory, decision-gate | guided explanation + user-ledger proposal | architecture-pattern-inventory, task-session |
| **ux-evidence-validator** | arcana | UX/accessibility/browser evidence → validator-safe checks. | — | evidence cards, validator spec | experiment-harness, research-evidence-harness |
| **architecture-pattern-inventory** | arcana | Map a repo into a reusable architecture pattern package. | — | ARCHITECTURE + pattern library | test-derivation, verification-weaver |

### Observability, verification & spec-ops *(advanced / optional chapters)*
| id | tier | purpose | ⇄integrates |
| --- | --- | --- | --- |
| **observability-setup** | formulae | Install the standard telemetry package. | signal-observer, workflow-reflect |
| **signal-observer** | arcana | Derive post-run behavior signals → telemetry row. | workflow-reflect |
| **observability-derivation** | arcana | Derive metric obligations from DomainSpec aspect docs. | audit-alignment, test-derivation |
| **workflow-reflect** | arcana | Accumulated signals → evidence-backed improvement proposals. | signal-observer, observability-setup |
| **observed-invocation-loop** | spell | Wrap invocations with guaranteed post-run telemetry + reflection routing. | signal-observer, workflow-reflect, sigil-development |
| **verification-weaver** | arcana | Route verification to typed owner lanes; join receipts. | test-derivation, ux-evidence-validator, experiment-harness |
| **audit-alignment** | arcana | Audit implementation vs DomainSpec per obligation. | code-tag-audit, task-session |
| **test-derivation** | arcana | Derive test obligations deterministically from aspect docs. | audit-alignment, verification-weaver |
| **code-tag-audit** | arcana | Code↔spec traceability via deterministic tags + drift. | audit-alignment, github-project-issue-loop |
| **integration-spec** | arcana | (spec-ops) integration route shape validation. | dispatch-spec |
| **sync-user-stories** | arcana | DomainSpec aspect docs → capability user stories + coverage matrix. | github-project-issue-loop, task-session |
| **github-project-issue-loop** | arcana | One GH issue → refine → invoke → execute → verified PR. | refine, invoke, task-session |
| **invoke-example-runner** | arcana | Run invoke template validation prompts + save evidence. | invoke |
| **experiment-harness** | arcana | Repeatable profile-aware validation for spells/sigils. | sigil-development, spellcraft, research-tower |
| **discovery-to-inventory** | spell | scope-interview → feature-glossary → inventory. | scope-interview, feature-glossary, inventory |
| **ontology-harness** | spell | inventory + ontology-vault + context-builder → governed ontology. | inventory, ontology-vault, context-builder |
| **repository-harness** | spell | Build inventory + architecture + retrieval substrate from a repo. | inventory, architecture-pattern-inventory, context-builder |

## 3. The spine (inherit/build-on graph, condensed)

```text
                 ┌─────────── CRAFT (control surface) ───────────┐
                 │  every chapter has a place inside Craft        │
                 └───────────────────────────────────────────────┘
  scope-interview ─▶ refine ─▶ invoke ─▶ { task-session, spellcraft, sigil-development }
            │            │         │
   context-builder ◀─────┴─────────┘   (feeds refine, invoke, task-session)
                                  │
  inventory ─▶ ontology-vault ─▶ necronomicon        distill ─▶ implementation-layering
                                  │
  task-session ─▶ goal (autopilot)         research-tower ─▶ reading-learning-package
  decision-gate gates: invoke / task-session / goal     (+ whisper substrate)
  dispatch-spec validates every route;  x-ray renders every explanation
```

## 4. Chapter ordering (resolves GAP-AJ-CHAPTER-ORDER-001, draft→grounded)

Order follows the **inherit/build-on** edges: nothing is taught before what it
depends on. Branches at Ch4 follow the interrogated goal; non-chosen branches stay
offered by the path-recommender.

| # | Chapter | Why here (edge justification) |
| --- | --- | --- |
| 0 | **What is Arcanum / Cyber Alchemy** | the frame: tiers + five anchors + Orient→Evolve (no deps) |
| 1 | **Craft** — control surface | depends on nothing; everything returns here |
| 2 | **Refine** | inherits scope-interview + context-builder; feeds invoke |
| 3 | **Invoke** | inherits context-builder/inventory/dispatch-spec; the authoring front door |
| — | *(branch by goal)* | interrogation picks the first branch |
| 4a | **Whisper** (creative) | inherits interview+distill; no software needed |
| 4b | **Task-Session** (automation) | inherits refine+context-builder+decision-gate |
| 4c | **Inventory** (knowledge) | feeds context-builder, ontology, research |
| 5 | **Decision-Gate** | gates invoke/task-session/goal — teach after they exist |
| 6 | **Dispatch-Spec** | validates routes built in Ch3–5 |
| 7 | **Goal spell** | inherits craft+dispatch-spec+decision-gate+task-session — a capstone of the automation branch |
| 8 | **X-Ray** | renders explanations — self-referential (the Journey's own surfaces) |
| 9 | **Capstone: Research-Tower → Reading-Learning-Package** | inherits distill+glossary (+whisper) → the learner's OWN first tower |

## 5. Goal→first-tool routing (for the onboarder)

| Interrogated goal | Recommended first chapter-tool | Path |
| --- | --- | --- |
| creative / writing | **Whisper** | Ch0→1→4a→9 |
| automation | **Craft + Task-Session → Goal** | Ch0→1→4b→7 |
| knowledge / research | **Inventory → Research-Tower** | Ch0→1→4c→9 |
| unsure | **Craft (control surface)** | Ch0→1, then re-interrogate |

## 6. Coverage & residue

- **Covered:** 37 arcana, 3 formulae, 14 spells, 4 transmutations + tier framing. No
  capability dropped silently.
- **Residue / next:** (a) SWU-AJ-MAP-2 — make this durable as an `inventory` package
  with tagged edges; (b) a few advanced spec-ops sigils (observability-derivation,
  test-derivation, audit-alignment, integration-spec, sync-user-stories, code-tag-audit)
  are DomainSpec-oriented and likely **optional/advanced chapters**, not core arc;
  (c) confirm the Ch0 public Cyber Alchemy depth against `framework/CYBERALCHEMY-METHOD.md`
  during authoring (W1).
