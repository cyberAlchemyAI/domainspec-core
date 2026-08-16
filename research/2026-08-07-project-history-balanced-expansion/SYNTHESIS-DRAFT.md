# DomainSpec Core: balanced project-history revision candidate

## Scope and evidence rules

The revised history should be organized around repository formation, ownership transitions, implemented machinery, validation and dogfooding, formal correction, and the continuing boundary between candidate evidence and authority.

Dates must retain their evidence semantics:

- Git dates establish when a repository state was committed, not when an idea originated or became operational.
- Changelogs establish recorded release surfaces, not deployment or production use.
- README and architecture sources establish documented contracts or current boundaries, subject to identified staleness.
- Test and acceptance receipts establish only the bounded cases they report. Unrerun results remain source-reported.
- Plans, candidate packages, specifications, and validated receipts do not establish promotion, release, deployment, adoption, or production readiness.
- Business Philosopher must not be restored as the narrative or source spine. If intellectual lineage is retained at all, it should be a short, explicitly non-authoritative prehistory note.

The history should preserve three tensions rather than averaging them:

1. Product significance: what became executable or usable enough to provide feedback.
2. Repository and architectural transition: what acquired an owner, boundary, runtime, or governance contract.
3. Git and formal chronology: what can be dated and what corrections were actually proved.

## Coverage diagnosis

The existing history is structurally imbalanced. Ashby measured 5,337 words overall and 2,909 chronology words, with about 57.3% of the chronology assigned to the excluded philosophical lineage and Lean correction arc. It has no dedicated chronological section or links for Arcanum, Poker Team, or root development, and no Arcanum source link at all.

The principal defect is therefore not simply “too much Lean.” It is the absence of the system-building history around it: the parent repository’s April 20 formation; the early research, definitions, task-routing, and failure-recovery substrate; Arcanum’s independent public ownership and executable runtime/observability development; validation and dogfooding; deterministic derivation’s failure-and-repair story; the public/private export decision; framework unification without owner collapse; CyberAlchemy v2’s authority spine; DomainSpec v2 as a distinct governed program; and applied product and ontology witnesses.

Formalization should remain a major correction lens, but not the organizing spine for the whole project.

## Current theme and period coverage matrix

| Period | Primary historical theme | Distinct lenses that must appear | Recommended treatment |
|---|---|---|---|
| Before 2026-04-20 | Pre-parent implementation and validation roots | DomainSpec v1; Poker Team as pre-existing validation repository | Short contextual opening; distinguish nested-repository history from parent birth |
| 2026-04-20 to 2026-05-07 | Parent formation and governance substrate | Repository topology; research ownership; canonical definitions; task routing; telemetry and recovery | New substantial opening section |
| 2026-04-25 to 2026-07-23 | Formal audit and correction | Lean proof results; schema/instance separation; count-wall correction; claim ≤ proof | Retain one strong cross-cutting strand; compress construction catalogues |
| 2026-05-11 to 2026-06-12 | Arcanum formation and operational learning | Guard failures; observed runs; independent public repository; runtime-neutral execution; native skill migration | New central strand |
| 2026-06-14 to 2026-06-21 | Boundary and architecture pivot | Open-core export; three-pillar concept; framework unification; deterministic derivation correction | Treat as the central ownership-and-engineering turn |
| 2026-06-21 to 2026-07-23 | Authority spine and v2 reformulation | CAV2; DomainSpec v2; validation/dogfood; capability-bound execution | Separate authority architecture from product and runtime evidence |
| 2026-07-24 to 2026-08-07 | Bounded applied witnesses and runtime hardening | UI Studio; ontology carrier; Akashic Records; IDE workbench; later Arcanum gates; portfolio experiments | Select representative witnesses; avoid feature inventory |
| Present boundary | What exists versus what remains unproved | Public Arcanum; private DomainSpec/CAV2/Saturn; local witnesses; unresolved promotion and adoption | One consolidated close instead of repeated warnings |

## Source-family census

| Source family | Historical contribution | Evidence status and ceiling |
|---|---|---|
| Root Git and `.gitmodules` | Parent birth, topology, owner transitions, public export, native-skill cutover | Observed repository-event evidence; not idea origin, integration success, or adoption |
| Legacy DomainSpec repository | v1 releases and deterministic derivation machinery | Commit/release evidence; no universal compiler or production claim |
| Validation/Poker Team | Pre-parent validation lineage and later DomainSpec dogfood | Commit chronology is observed; acceptance outcomes remain unverified pending receipt-level evidence |
| Arcanum Git and owned docs | Independent public repository, capability lifecycle, runtime, observability, later governance hardening | Implemented/documented public repository surfaces; not universal route success or external adoption |
| Lean formalization | Major invalidations and proof-bounded corrections | Formal proof and repository chronology; retrospective milestone dates require commit binding where absent |
| Framework-unification sources | Explicit three-pillar owner map and non-collapse | Private architecture/design evidence; not completed runtime integration |
| CyberAlchemy v2 authority sources | Vocabulary, promotion gates, source routing, public/private scrubbing | Private authority architecture; no public shipment or production proof |
| DomainSpec v2 sources | Separately governed reformulation and candidate implementation program | Candidate contracts, code, and receipts; not a continuation of legacy release numbers and not production release |
| Applied project sources | Concrete feedback environments and bounded product-shaped witnesses | Prototype or locally validated evidence only; status varies by project |
| Operations, sessions, telemetry, and research | Evidence of repeated governed work, incidents, and architectural learning | Operational evidence, not authority or generalized reliability |
| Existing root README | Historical April operating model | Stale snapshot; current ownership must come from current owner sources |

## Proposed chronological narrative

### 1. Pre-parent roots and the April 20 repository formation

The history should begin by separating the histories of the nested implementation and validation repositories from the birth of DomainSpec Core itself. The parent repository was initialized on April 20 as an orchestration and research workspace around separately owned implementation and validation repositories.

**Evidence package:** Beer, “System-evolution milestones,” items 1–2; `git show --stat d96abdc3`, `git show --stat 01f8ed53`, `.gitmodules` history, and historical `README.md:1-181`. Evidence type/status: observed Git repository events plus a committed but now stale operating-model document.  
**Recommendation:** **ADD** the April 20 birth as the organizing event; **COMPRESS** April 21–28 into one formation passage.  
**Claim ceiling:** repository formation, topology, and asserted operating model only.

This corrects two errors at once: the parent was not the original implementation repository, and May corpus imports were not its first meaningful event.

### 2. Research, definitions, routing, and operational recovery become architecture

Between late April and early May, canonical definitions, definitions-source-first research, interactive task sessions, planner gates, work-pack routing, delegation telemetry, watchdogs, and stall recovery appeared. These establish the early architecture of a repository intended to coordinate work across owned systems.

The May 11–18 terminal guard and telemetry sequence adds an important correction story. Observability and hardened command surfaces emerged in response to concrete terminal and stall risks.

**Evidence package:** Beer items 3–4; root commits `ba0838d8`, `b0df101a`, `9bfb7330`, `d41d5a0d`, `ec0aeded`, `82e6603d`, `acad68a4`, `ad81cf89`, `bd673289`, `451316ad`, `1ce5fe93`, followed by `39d799ae`, `64744e78`, `1514752f`, `f0ff829b`, and `0e282e7d`. Evidence type/status: observed commit chronology and repository artifacts.  
**Recommendation:** **ADD** one medium-size section joining governance formation to operational failure and correction.  
**Claim ceiling:** committed workflows, guards, and telemetry; not reliable autonomous operation or universal invocation safety.

### 3. Formalization becomes a correction instrument, not the whole history

Lean should remain prominent because it forced important corrections: schema and instance had to be separated; numerical alignment was not semantic entailment; descriptive structure did not automatically carry authority; and every claim had to remain below the proof actually obtained.

What should shrink is the catalogue of individual formal constructions. Preserve the decisive corrections and their consequences for v2 architecture, while removing duplicated exposition.

**Evidence package:** Ashby, “Coverage matrix” and “Chronological gaps and corrections,” items 8 and 10; `domainspec-lean-formalization/PROJECT-HISTORY.md`, nested Git span 2026-04-25 through 2026-07-23. Evidence type/status: formal repository history, with high commit-date confidence but medium confidence for retrospective dates not commit-bound.  
**Recommendation:** **COMPRESS**, **QUALIFY**, and **REORDER** as a cross-cutting correction strand from April through July.  
**Claim ceiling:** proved statements and bounded formal invalidations only; do not infer product completeness or system-wide implementation.

### 4. Arcanum becomes an independently owned public capability system

On May 14 Arcanum acquired separate Git ownership. The subsequent sequence added capability tiers, lifecycle, registry, Invoke, observed-run hooks, experiment infrastructure, telemetry, and the Observed Invocation Loop. From May 19 onward, CyberAlchemy became a reusable method and capability vocabulary rather than a renamed command bundle.

This is an owner transition and an implementation story. It precedes the polished August three-pillar account and shows the public “how” being built through runtime and feedback machinery.

**Evidence package:** Beer items 5–6 and Simon recovery items 1–3; `.gitmodules:9-12`, Arcanum commits `4a5ede5` onward, `arcanum/README.md#Capability-Model`, `#Observability-Layer`, `#Experiment-Harness`, and `arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md#Current-Architecture-In-One-Sentence`, `#Source-Inventory`, `#Runtime-Data-Model`. Evidence type/status: observed Git history plus implemented/documented public framework surfaces.  
**Recommendation:** **ADD** a central May strand with high narrative weight.  
**Claim ceiling:** independent public repository and local framework/runtime implementation; no external adoption, production convergence, or proof every capability succeeds.

### 5. Arcanum pivots from host adapters to capability-bound execution

From May 21 through July 23, Arcanum separated workflow meaning from specific hosts through durable handoffs, status and event evidence, adapters, and eventually capability-bound native execution. The June 5–12 cleanup of root runtime clutter and installation of native Arcanum skills belongs in this same evolution.

**Evidence package:** Simon recovery items 2–3 and Beer items 7 and 14; `arcanum/framework/runtime/README.md#Model`, `#Run-Folder`, `#Status-Model`, `#Adapters`, `#Event-Ownership`; commits `91e5a8c`, `fb4079d`, `7149609`, `40e12db`, plus root commits `eba0b4bc`, `8e7ab86f`, `b08d5085`, `3c2deba3`. Evidence type/status: observed Git events and documented runtime contract.  
**Recommendation:** **ADD** a compact evolution paragraph in June and return to later hardening near the close; **QUALIFY** uniform observability.  
**Claim ceiling:** implemented generic substrate and adapter boundary; no universal host parity, generalized reliability, or route-by-route deployment proof.

### 6. Validation and dogfooding become a separate historical lens

Poker Team predates the parent repository, adds DomainSpec in April, continues pilot stabilization, and later records deterministic settlement derivation and an SFOL adapter. Its significance is validation and dogfooding, not product or business success.

Because Ashby found no receipt-level corroboration for the outcomes, the revision should initially cite the chronology and mark the stronger interpretation as unresolved.

**Evidence package:** Ashby, “Coverage matrix” and gap item 2; `git -C validation/poker-team log --reverse --format='%ad %h %s' --date=short`, with observed events from 2026-01-08, DomainSpec addition on 2026-04-08, settlement derivation on 2026-06-21, and SFOL adapter on 2026-07-27. Evidence type/status: observed nested Git chronology; dogfood outcomes unverified.  
**Recommendation:** **ADD** a bounded validation strand; use the explorer feedback edge before making acceptance or outcome claims.  
**Claim ceiling:** repository validation activity and dated artifacts only; no profitability, production success, or verified acceptance outcome.

### 7. June’s central pivot: public export without ownership collapse

The June 14–15 open-core cut exported selected reusable definitions and capabilities to public Arcanum while DomainSpec implementation and the later CAV2/Saturn material remained private. The June 15–16 framework-unification work then articulated DomainSpec as the “what,” Arcanum as the public “how,” and Saturn as the evidence loop, without merging their owners.

**Evidence package:** Beer items 9–10; commits `abf64284`, `1495bac7`, `fe4c6d42`, `db391d55`, `ae590b53`, `709d5d23`, `4345024b`; `projects/framework-unification/CONCEPT-MAP.md:31-32`; current boundary sources `AGENTS.md:7-12,124-149` and `cyberAlchemy-v2/SOURCE-MAP.md:14-18,30,56-57`. Evidence type/status: observed repository boundary events, private architecture synthesis, and current owner contracts.  
**Recommendation:** **ADD** with very high weight; **REORDER** before the v2/CAV2 chronology.  
**Claim ceiling:** deliberate export and private architectural synthesis; never claim DomainSpec or Saturn shipped publicly, or that unification was implemented.

### 8. Deterministic derivation supplies an honest build–fail–repair milestone

On June 15, deterministic derivation exposed a concrete semantic failure. A four-document input missed 11 obligations; expanding the parser to the full seven-document feature reached `MISSING = 0`, 33/33 tests, and byte-identical repeated output. A second feature remained an honest failure with 30 misses localized to identity-convention drift.

**Evidence package:** Simon first return, milestone 3; `development/deterministic-test-derivation-engine/L0-ROUNDTRIP-REPORT.md#Gate-verdict-financial-settlement-7-docs`, `#History-the-original-4-doc-FAIL-retained-for-provenance`, `#Second-feature-auth-access-control`, `#Interpretation--promotion-decision`. Corroborating but conflicting source: Simon recovery item 1, `implementation/domainspec/tools/test-derivation-engine/README.md#Pipeline` and stale `#Status`. Evidence type/status: source-recorded executed validation; no current rebuild.  
**Recommendation:** **ADD** one substantial paragraph; **QUALIFY** README drift and avoid merging distinct derivation-engine scopes without writer verification.  
**Claim ceiling:** passing scoped validation for one seven-document feature and bounded failure for another; not a universal compiler or production pipeline.

### 9. CyberAlchemy v2 forms the private authority spine

From June 21 onward, CAV2 made canonical vocabulary, promotion gates, source routing, non-collapse, and public/private scrubbing explicit. This is a governance and authority milestone, not a product release. Contemporary sources also record the gap between public Arcanum’s “how” and the private/intended DomainSpec and Saturn framing.

**Evidence package:** Beer item 12; CAV2 birth and authority commits beginning `7e776e65`, `cyberAlchemy-v2/README.md:96,134-140`, `cyberAlchemy-v2/SOURCE-MAP.md:14-18,30,56-57`, and `ops/development/2026-06-21-paper-saturn-explainer/SATURN-LAYER-MAP.md:59-81,120-147`. Evidence type/status: observed Git chronology and private authority/design sources; June public-surface observations are historical and not live-verified.  
**Recommendation:** **ADD** with high weight; **QUALIFY** “stable repository” and historical public-surface language.  
**Claim ceiling:** private authority architecture and gap analysis; no public shipment, promotion, or production proof.

### 10. DomainSpec v2 is a distinct governed program

The June 30–July 23 v2 work should not be narrated as the next release number in the legacy DomainSpec sequence. It is a separately governed reformulation involving definitions, meta-type formalism, relationship authority, spec homing, non-collapse, attestations, residue receipts, runtime/IDE work, and proof/minting primitives.

**Evidence package:** Beer item 13; `git log -- projects/domainspec-v2`, especially commits `b0f35d43`, `a10f0de3`, `abf03f66`, `ce49f4cd`, `b0ae56b8`, `bf88890b`, `789261ef`, `25a665a5`, `f0116e66`, `076be658`, `edce4249`, `35b7d2ca`, `9036334c`. Evidence type/status: observed committed candidate programs, contracts, and receipts.  
**Recommendation:** **REORDER** after CAV2 formation and **COMPRESS** low-level catalogue detail.  
**Claim ceiling:** candidate implementation and governed program evidence; a production-release contract is not a production release.

### 11. Applied witnesses show feedback without proving products

UI Prototyping Studio is the strongest product-shaped dogfood case: it records a governed selection, annotation, mutation-draft, approval, Accept/Revert, evidence, and handoff loop, with source-reported TypeScript, unit/slice, and Playwright results.

**Evidence package:** Simon recovery item 4; `projects/ui-prototyping-studio/README.md#Proven-implementation-scope`, `#Status`; commits `46157a70`, `9ded2565`, `8752742c`. Evidence type/status: locally reproducible implementation with recorded, not rerun, validation.  
**Recommendation:** **ADD** one full applied paragraph.  
**Claim ceiling:** scoped local implementation; no full accessibility, human ergonomics, publication, or release proof.

The ontology candidate carrier supplies a narrower authority-safe implementation witness: a five-node fixture, rejection boundaries, eight recorded passing tests, and byte stability.

**Evidence package:** Simon recovery item 5; `cyberAlchemy-v2/development/ontology-candidate-graph-prototype/planning/work-pack/session-evidence/SWU-OCGP-001/TASK-SESSION-RESULT.md#Evidence`, `#Boundary`; commit `29c5dc52`. Evidence type/status: executed candidate-local receipt.  
**Recommendation:** **ADD** as a short July milestone.  
**Claim ceiling:** carrier validation only; excludes relation semantics, grounding, persistence, admission, and promotion.

Akashic Records and the IDE Extension can appear as bounded local witnesses, but should not displace the main chronology.

**Evidence package:** Simon first return, milestones 4–5; `projects/ide-extension/README.md#Current-Status`, `#Boundary`, `#First-Witness`; `projects/akashic-records/README.md#Current-Status`, `#The-Implemented-Contract`, `#The-Bounded-Graph`. Evidence type/status: source-reported runnable or locally validated witnesses; Akashic tests were not rerun and its first-commit date needs verification.  
**Recommendation:** **ADD/COMPRESS** into a short applied-witness subsection; **QUALIFY** aggressively.  
**Claim ceiling:** trusted-local prototype or experimental graph witness; no autonomous IDE agent, provider runtime, deployment, source truth, or accountable adoption.

Body War, co-op-engine, Whisky Doses, and Equalizator should remain compact ecosystem examples unless their exact validation receipts are audited. Mint should not be narrated as a completed milestone. Explorer returns conflict on maturity; the safe synthesis is that bounded implementation exists inside an explicitly incomplete private lifecycle.

## Recommended narrative proportions

| Strand | Target share |
|---|---:|
| Scope, date semantics, and evidence boundary | 7% |
| Pre-parent roots, parent formation, and initial topology | 14% |
| Research, definitions, task routing, operational failure, and recovery | 11% |
| Validation and dogfooding | 10% |
| Arcanum public capability/runtime evolution | 15% |
| Formal audit and major corrections | 16% |
| Open-core cut, framework unification, CAV2, and DomainSpec v2 | 17% |
| Applied witnesses and late runtime hardening | 7% |
| Current state and open frontiers | 3% |

## Concrete editorial operations

### ADD

- April 20 parent birth and original owned topology.
- Late-April research/governance substrate.
- Operational failure → guard/observability correction.
- Arcanum’s May 14 independent public-repository formation.
- Runtime-neutral and capability-bound Arcanum evolution.
- Poker Team as bounded validation/dogfood chronology.
- June open-core/public-export decision.
- Framework unification as a private conceptual pivot.
- Deterministic derivation’s failure-and-repair episode.
- CAV2 authority-spine formation.
- DomainSpec v2 as a distinct governed program.
- A selected applied-witness subsection.

### COMPRESS

- Business Philosopher-derived chronology and links.
- Lean construction catalogues while retaining major corrections.
- Repeated public/private and authority warnings.
- Routine submodule pointer bumps.
- Product feature inventories and unaudited portfolio chronology.
- Mint into a bounded incomplete-work example.
- Repeated current-state summaries.

### REORDER

- Begin with pre-parent roots and April 20 parent formation.
- Place research/governance formation before the later theoretical synthesis.
- Introduce Arcanum in May, not first in the August present-state account.
- Put the public export decision before framework unification.
- Put CAV2 formation before DomainSpec v2.
- Interleave formal corrections with the repository and implementation consequences they caused.

### QUALIFY

- Root README as an April 28 snapshot, not current authority.
- Historical public-site observations as unrefreshed.
- Commit subjects as repository evidence, not proof of behavior.
- Recorded tests that were not rerun.
- Poker Team outcome interpretations pending receipt evidence.
- Retrospective Lean dates pending commit binding.
- “Stable,” “production contract,” “implemented,” and “complete” according to their exact evidence scopes.
- Mint, IDE, ontology, and applied-project claims to their candidate/local boundaries.

### EXCLUDE

- Business Philosopher as a source spine.
- Any suggestion that DomainSpec or Saturn shipped publicly.
- Any claim that framework unification was a completed runtime integration.
- Production, market, adoption, profitability, or user-validation claims without exact evidence.
- Routine repository activity that establishes no owner, boundary, correction, failure/recovery, or material implementation milestone.
- Application specifications presented as implemented products.
- Candidate packages or validated receipts presented as authority or promotion.

## Cited-synthesis closure-candidate matrix

| Proposal | Live source identity / selector | Explorer-return reference | Evidence type / status | Recommendation | Claim ceiling | Closure |
|---|---|---|---|---|---|---|
| Parent repository birth | `git show --stat d96abdc3`; `git show --stat 01f8ed53`; `.gitmodules` history | Beer, milestones 1–2 | Git events, observed | ADD, REORDER | Formation/topology only | Ready |
| Early governance substrate | Root commits `ba0838d8` through `1ce5fe93` as enumerated by Beer | Beer, milestone 3 | Git events, observed | ADD | Committed workflow artifacts, not autonomy | Ready |
| Failure-driven guards | Root commits `39d799ae`, `64744e78`, `1514752f`, `f0ff829b`, `0e282e7d` | Beer, milestone 4 | Git and repository controls, observed | ADD | No universal invocation-safety claim | Ready |
| Lean correction strand | `domainspec-lean-formalization/PROJECT-HISTORY.md`; nested Git history | Ashby, coverage matrix and gap 8 | Formal/Git; retrospective dates partly unverified | COMPRESS, QUALIFY | Exact proof only | Ready with date qualification |
| Arcanum independent birth | `.gitmodules:9-12`; Arcanum commit `4a5ede5` onward | Beer, milestones 5–6 | Git, observed | ADD | Public repository formation, not adoption | Ready |
| Arcanum observability | Arcanum observability architecture selectors | Simon recovery, item 3; Simon first return, item 1 | Implemented/documented; uneven seams | ADD, QUALIFY | Repository-local substrate only | Ready |
| Runtime-neutral execution | Arcanum runtime README selectors | Simon recovery item 2; Beer items 7 and 14 | Git plus owned contract | ADD | No universal parity/reliability | Ready |
| Poker Team validation | `git -C validation/poker-team log --reverse --format='%ad %h %s' --date=short` | Ashby, gap 2 | Git observed; outcomes unverified | ADD, QUALIFY | Validation activity only | Needs feedback for outcome claims |
| Public/private export cut | Commits `abf64284`, `1495bac7`, `fe4c6d42`; `AGENTS.md:7-12,124-149` | Beer, milestone 9 | Git plus current owner contract | ADD, REORDER | Selected export only | Ready |
| Three-pillar concept without collapse | Commits and `CONCEPT-MAP.md:31-32` | Beer, milestone 10 | Private architecture synthesis | ADD, QUALIFY | Not runtime integration/release | Ready |
| Deterministic derivation correction | Roundtrip report named sections; engine README `#Pipeline` and stale `#Status` | Simon first return item 3; Simon recovery item 1 | Source-recorded execution; no rebuild; drift | ADD, QUALIFY | One bounded pass and one bounded failure | Ready if scopes stay separate |
| CAV2 authority spine | CAV2 README, source map, Saturn layer map selectors | Beer, milestone 12 | Git/private sources; public view historical | ADD, QUALIFY | Private architecture only | Ready |
| DomainSpec v2 distinct program | `git log -- projects/domainspec-v2`; commits enumerated by Beer | Beer, milestone 13 | Git, observed | ADD, REORDER | Candidate program/contracts only | Ready |
| UI Studio dogfood | UI Studio README selectors | Simon recovery item 4 | Recorded local validation, not rerun | ADD, QUALIFY | Local implementation only | Ready |
| Ontology carrier | OCGP task-session evidence and boundary | Simon recovery item 5 | Executed candidate-local receipt | ADD | Carrier validation only | Ready |
| IDE Extension witness | IDE Extension README selectors | Simon first return item 4 | Runnable local witness | ADD/COMPRESS | No autonomous agent/provider runtime | Ready |
| Akashic Records witness | Akashic Records README selectors | Simon first return item 5 | Source-reported tests, not rerun | ADD/COMPRESS, QUALIFY | Local experimental witness | Needs exact date |
| Mint incomplete runtime | Mint README and runtime README selectors | Simon first and recovery returns | Candidate validation plus open blocks | COMPRESS, QUALIFY | Intended-not-shipped | Ready conservatively |
| Portfolio ecosystem | Body War, co-op, Whisky Doses, Equalizator selectors | Simon returns | Mixed artifacts | COMPRESS/EXCLUDE | No product success/adoption | Ecosystem sentence only |
| Later Arcanum hardening | Arcanum commits enumerated by Beer | Beer, milestone 14 | Git plus evidence artifacts | ADD compactly | Mechanisms, not reliability | Ready |

## Synthesis close

The revised history should tell how DomainSpec Core became a repository that coordinates separately owned systems and uses evidence to constrain claims. Its center of gravity should move from a joined philosophical/formal lineage to a balanced account of formation, implementation, validation, public capability ownership, authority architecture, formal correction, applied feedback, and unresolved boundaries.

The strongest supported thesis is:

> DomainSpec Core evolved from separately owned implementation and validation roots into a governed parent workspace; built Arcanum as the independently owned public capability and runtime layer; used formal failures, operational incidents, deterministic derivation, and applied prototypes as correction signals; and formed private DomainSpec v2, CyberAlchemy v2, and Saturn-facing architecture without collapsing ownership or claiming shipment beyond the available evidence.

That thesis is supported as repository and bounded execution history. It is not evidence that the complete three-pillar system is shipped, deployed, adopted, production-ready, or operationally closed.
