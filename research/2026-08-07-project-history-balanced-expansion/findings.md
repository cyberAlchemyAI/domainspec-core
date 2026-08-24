# Diagnosis

The current project history is structurally imbalanced. It gives disproportionate weight to philosophical and formal lineage while underrepresenting the repository history that can actually be witnessed: the parent workspace forming around separately owned repositories; early research, routing, telemetry, guard, and recovery mechanisms; Arcanum gaining separate public ownership and later runtime surfaces; formal invalidations and bounded validation episodes; selective public export; private authority routing; a separately governed DomainSpec v2 candidate program; and local dogfood witnesses.

The repair should therefore organize the history around repository formation, owner transitions, committed mechanisms, bounded executions, documented corrections, and the present claim boundary. Formalization remains important where it invalidated a claim or changed an architectural distinction, but it should no longer operate as the narrative spine. Git dates establish repository events, not idea origins or operational success. Documentation establishes a contract, design, or status assertion, not execution. Source-reported tests remain source-reported where they were not rerun. Candidates, plans, receipts, and bounded passes do not establish authority, promotion, publication, deployment, adoption, production readiness, or closure.

## Recommended history architecture

The revised history should follow this sequence:

1. State the evidence semantics and current public/private claim boundary.
2. Establish pre-parent implementation and validation activity, then the April 20 parent-workspace record.
3. Compress the late-April and early-May definitions, research, routing, planning, telemetry, guard, and recovery mechanisms into one period.
4. Give Arcanum one owner-centered section with two subperiods: separate public repository formation, then runtime and adapter evolution.
5. Retain formal corrections only where a source-bound invalidation or distinction changed what could be claimed.
6. Record validation-repository and dogfood activity without importing unverified outcomes.
7. Describe selective public export before the later private framework-unification synthesis, without collapsing owners.
8. Present deterministic derivation as one scoped build-fail-repair episode, including both its bounded pass and bounded failure.
9. Present CyberAlchemy v2 as private authority-spine design, followed by DomainSpec v2 as a separately governed candidate program.
10. Close the chronology with UI Prototyping Studio and a compact “Bounded local witnesses” subsection.
11. End with one consolidated current boundary and unresolved frontiers.

This architecture restores balance by giving narrative weight to evidence-bearing owner changes and mechanisms, while keeping portfolio breadth compressed and refusing to turn candidate artifacts into system-level accomplishment.

The revised architecture must keep four similarly named but separately evidenced objects distinct. **Legacy DomainSpec** is the implementation under `implementation/domainspec/`, with its changelog and repository evidence. **DomainSpec Core** is the parent workspace whose formation is recorded by root Git and `.gitmodules`. **The private DomainSpec pillar** is the typed-intent owner described by current `AGENTS.md:7-12`. **DomainSpec v2** is the separately governed candidate whose admitted chronology comes from `git log --date=short -- projects/domainspec-v2`. The shared name does not by itself prove continuity, migration, promotion, completion, or release between any of these objects.

## Source-family and theme census

| Source family | Themes it can support | Accepted historical use | Claim limit |
| --- | --- | --- | --- |
| Root Git and `.gitmodules` | Parent formation; early mechanisms; operational controls; selective export; DomainSpec v2 path chronology | Date repository events and topology changes | No idea origin, runtime operation, external effect, or present status unless separately sourced |
| Arcanum nested Git | Separate repository ownership and dated public capability formation | Date the May 14 ownership transition and later committed development | No adoption, parity, reliability, or uniform observation |
| `arcanum/README.md` | Current public capability, observability, and experiment surfaces | Explain the currently documented public surface | Documentation is not execution, deployment, or adoption evidence |
| Arcanum runtime and observability documentation | Runtime model, adapters, event ownership, data model | Describe developing runtime boundaries and uneven seams | No completed integration or operational closure |
| Lean formal history and nested Git | Schema/instance separation, count limits, claim-to-proof correction | Retain decisive invalidations and distinctions | Retrospective dates require commit binding; causal language stays qualified |
| Poker Team nested Git | Pre-parent validation-repository activity and dated artifacts | Establish chronology only | No accepted outcome, effectiveness, profitability, production, or business-success claim |
| Framework unification concept map and current `AGENTS.md` | Private three-pillar synthesis and non-collapse boundary | Separate later synthesis from the current ownership rule | No completed runtime integration or release |
| Deterministic derivation round-trip report | Seven-document repaired pass, original four-document miss, second-feature failure | Present one bounded build-fail-repair episode | Reported execution was not rerun; no universal compiler or production-pipeline claim |
| CAV2 README, source map, Saturn layer map, and root Git | Private authority vocabulary, routing, promotion gates, scrubbing, June design/gap chronology | Describe private authority-spine design | CAV2 and Saturn are not public, shipped, deployed, or production components |
| Root path Git for `projects/domainspec-v2` | June-July candidate-program chronology | Date candidate materials and governed activity | No present completion, legacy-release continuity, or production release |
| UI Studio README and cited commits | Product-like local dogfood interaction surface | One bounded applied-witness paragraph | Recorded checks were not rerun; no accessibility, human validation, publication, or release claim |
| Candidate receipts and owned project READMEs | Ontology carrier, IDE Extension, and Akashic bounded graphs | One compact local-witness subsection | No full ontology, autonomous IDE, source truth, deployment, adoption, or dated Akashic origin |
| Mint candidate documentation | Bounded private implementation and open lifecycle blocks | At most one sentence or fenced paragraph | Intended-not-shipped; promotes nothing; no repository-minted proof |

## Accepted milestones and patch blueprint

Each load-bearing recommendation below carries both the admitted source identity and selector and the explorer return that supplied it. These are evidence pointers admitted by the closure, not a claim that the writer reran the underlying commands.

### 1. Pre-parent roots and parent formation — add and reorder

Lead with the distinction between earlier activity in separately owned implementation/validation repositories and the first cited parent-repository record. Use this patch-ready formulation:

> The earliest cited parent-repository commits are dated April 20 and record the formation of an orchestration and research workspace around separately owned repositories.

Treat the root README as a stale April snapshot, not as a current system description. Do not infer when the idea originated or when any mechanism became operational.

Evidence: source identity `root Git repository`, `.gitmodules`; selectors `git show --stat d96abdc3`, `git show --stat 01f8ed53`, `git log --reverse --date=short --pretty=format:'%ad %h %s' -- .gitmodules`; explorer return `Beer milestones 1-2`.

### 2. Early research, routing, and recovery mechanisms — add and compress

Replace commit-by-commit narration with one early-mechanisms passage. Late-April and early-May commits record definitions-first research, routing, planner/work-pack mechanisms, telemetry, watchdogs, and stall recovery. Join the May guard/telemetry sequence to this passage as evidence that controls were recorded after operational risks appeared. Phrase this as committed mechanisms and recorded controls, not reliable autonomy or universal safety.

Evidence: source identity `root Git repository`; selectors `git show ba0838d8`, `git show b0df101a`, `git show 9bfb7330`, `git show d41d5a0d`, `git show ec0aeded`, `git show 82e6603d`, `git show acad68a4`, `git show ad81cf89`, `git show bd673289`, `git show 451316ad`, `git show 1ce5fe93`; explorer return `Beer milestone 3`.

Guard/observation evidence: source identity `root Git repository`; selectors `git show 39d799ae`, `git show 64744e78`, `git show 1514752f`, `git show f0ff829b`, `git show 0e282e7d`; explorer return `Beer milestone 4`.

### 3. Arcanum’s separate public ownership and runtime development — merge, add, rename, qualify

Create one Arcanum section with two dated subperiods:

- **May 14: separate Git ownership and public capability formation.** Cover tiers, lifecycle, registry, Invoke, observed-run hooks, experiments, and telemetry.
- **May 21 onward: runtime and adapter evolution.** Cover durable handoffs, status/event evidence, adapter boundaries, native-skill migration, and later capability-bound execution and hardening.

Use the historical naming formulation: “From May 19 onward, the cited Arcanum history records reusable method and capability vocabulary under the then-current CyberAlchemy naming.” This prevents the historical label from being mistaken for the separately owned private CyberAlchemy v2 authority spine.

Evidence: source identities `Arcanum Git`, `.gitmodules`, `arcanum/README.md`, `arcanum/framework/runtime/README.md`, `arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md`; selectors `.gitmodules:9-12`, `git -C arcanum show 4a5ede5`, `arcanum/README.md#Capability-Model`, `arcanum/README.md#Observability-Layer`, `arcanum/README.md#Experiment-Harness`, `arcanum/framework/runtime/README.md#Model`, `arcanum/framework/runtime/README.md#Adapters`, `arcanum/framework/runtime/README.md#Event-Ownership`, `arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md#Runtime-Data-Model`; explorer returns `Beer milestones 5-7 and 14`, `Simon Arcanum findings`.

### 4. Formalization as a correction instrument — compress and qualify

Compress construction catalogues and retain only formal work that changes the history’s claims: schema/instance separation, count limits, and claim-to-proof discipline. Bind dates to nested commits where possible; otherwise label the account retrospective. Prefer “exposed,” “invalidated,” or “was followed by” to unsupported causal language such as “forced.”

Evidence: source identities `domainspec-lean-formalization/PROJECT-HISTORY.md`, `domainspec-lean-formalization Git`; selectors `domainspec-lean-formalization/PROJECT-HISTORY.md`, `git -C domainspec-lean-formalization log --date=short`; explorer return `Ashby coverage/gap 8`.

### 5. Validation-repository activity — add chronology only

Place the Poker Team repository’s dated DomainSpec-related activity before the April 20 parent formation where its nested chronology requires it. State only that the repository contains pre-parent validation activity and dated artifacts. Exclude acceptance, effectiveness, profitability, business success, production use, and all other outcomes until an exact owned receipt is available.

Evidence: source identity `validation/poker-team nested Git`; selector `git -C validation/poker-team log --reverse --format='%ad %h %s' --date=short`; explorer return `Ashby gap 2`.

### 6. Selective public export, then framework synthesis without collapse — add and reorder

Let the June commits own the historical export event and describe it narrowly as selective public export. Do not use today’s boundary documentation to backdate current ownership semantics into that event.

Evidence: source identity `root Git repository`; selectors `git show abf64284`, `git show 1495bac7`, `git show fe4c6d42`; explorer return `Beer milestone 9`.

Follow that event with the later private framework-unification synthesis. The concept map owns the synthesis; current `AGENTS.md` owns the present non-collapse boundary. Explicitly state that a documented owner map is not completed runtime integration.

Evidence: source identities `projects/framework-unification/CONCEPT-MAP.md`, `AGENTS.md`; selectors `projects/framework-unification/CONCEPT-MAP.md:30-33`, `AGENTS.md:7-12`; explorer return `Beer milestone 10`.

### 7. Deterministic derivation as a scoped build-fail-repair episode — add and qualify

State that one source-recorded report describes a seven-document repair/pass, preserves the original four-document failure for provenance, and records a second-feature access-control failure. Keep the pass and failure together. Attribute both only to the report and surface the stale implementation README as a conflict rather than corroboration. The sound claim is one bounded reported repair/pass and one bounded reported failure, not a universal compiler or production pipeline.

Evidence: source identity `development/deterministic-test-derivation-engine/L0-ROUNDTRIP-REPORT.md`; selectors `#Gate-verdict-financial-settlement-7-docs`, `#History-the-original-4-doc-FAIL-retained-for-provenance`, `#Second-feature-auth-access-control`, `#Interpretation--promotion-decision`; explorer return `Simon first return milestone 3`.

### 8. CyberAlchemy v2 authority-spine design — add and qualify

Describe CAV2 as the private owner of authority vocabulary, promotion gates, routing, non-collapse, and scrubbing. The dated Saturn layer map supports only the June framing and gap account. Qualify maturity labels such as “stable,” and do not describe CAV2 or Saturn as public, shipped, implemented end-to-end, deployed, or production-ready.

Evidence: source identities `cyberAlchemy-v2/README.md`, `cyberAlchemy-v2/SOURCE-MAP.md`, `SATURN-LAYER-MAP.md`, `root Git`; selectors `git show 7e776e65`, `cyberAlchemy-v2/README.md:96,134-140`, `cyberAlchemy-v2/SOURCE-MAP.md:14-19,25-31,54-58`, `ops/development/2026-06-21-paper-saturn-explainer/SATURN-LAYER-MAP.md:59-81,120-147`; explorer return `Beer milestone 12`.

### 9. DomainSpec v2 candidate program — add, reorder, qualify

Place DomainSpec v2 after CAV2 and distinguish it from legacy DomainSpec under `implementation/domainspec/`, DomainSpec Core as the root-Git/`.gitmodules` parent workspace, and the private DomainSpec pillar described by current `AGENTS.md:7-12`. Use root path Git only for the June-July chronology of DomainSpec v2 candidate materials, contracts, and receipts. Neither the common name nor this chronology proves continuity, migration, promotion, completion, or release; present status and production release remain unbound.

Evidence: source identity `root path Git for projects/domainspec-v2`; selector `git log --date=short -- projects/domainspec-v2`; explorer return `Beer milestone 13`.

### 10. Applied and bounded local witnesses — add compactly

Give UI Prototyping Studio one paragraph as a locally implemented dogfood case with a product-like interaction surface. State that its recorded checks were not rerun, and make no accessibility, human-validation, publication, or release claim.

Evidence: source identity `projects/ui-prototyping-studio/README.md`; selectors `#Proven-implementation-scope`, `#Status`, `git show 46157a70`, `git show 9ded2565`, `git show 8752742c`; explorer return `Simon recovery milestone 4`.

Then create a subsection titled **Bounded local witnesses**. Merge the ontology carrier receipt, IDE Extension status, and undated Akashic bounded graph into a short account of local evidence. Do not infer a full ontology, autonomous IDE, source truth, deployment, adoption, or an Akashic origin date.

Evidence: source identities `cyberAlchemy-v2/development/ontology-candidate-graph-prototype/planning/work-pack/session-evidence/SWU-OCGP-001/TASK-SESSION-RESULT.md`, `projects/ide-extension/README.md`, `projects/akashic-records/README.md`; selectors `cyberAlchemy-v2/development/ontology-candidate-graph-prototype/planning/work-pack/session-evidence/SWU-OCGP-001/TASK-SESSION-RESULT.md#Evidence`, `cyberAlchemy-v2/development/ontology-candidate-graph-prototype/planning/work-pack/session-evidence/SWU-OCGP-001/TASK-SESSION-RESULT.md#Boundary`, `projects/ide-extension/README.md#Current-Status`, `projects/ide-extension/README.md#Boundary`, `projects/akashic-records/README.md#Current-Status`, `projects/akashic-records/README.md#The-Bounded-Graph`; explorer return `Simon witness findings`.

Mint should receive no more than one sentence: its documentation reports bounded private implementation and synthetic validation inside an incomplete, intended-not-shipped lifecycle; it promotes nothing and does not prove a repository was minted.

Evidence: source identities `cyberAlchemy-v2/development/mint/README.md`, `cyberAlchemy-v2/development/mint/runtime/README.md`; selectors `#Problem-solved`, `#Lifecycle-expectations--open-blocks`, `#Effect-and-owner-boundary`, `#Validation`; explorer return `Simon Mint findings`.

### 11. Consolidated present boundary — required close

Use current Arcanum documentation to describe the public capability/runtime surface, and current `AGENTS.md` plus CAV2 routing to describe the private DomainSpec/CAV2/Saturn boundary. End with the following paragraph unchanged in substance:

> The cited repository history records a parent workspace forming around separately owned implementation and validation repositories; Arcanum acquiring separate ownership and developing public capability and runtime surfaces; formal invalidations, operational incidents, deterministic-derivation results, and bounded local prototypes informing documented corrections; and private CAV2, DomainSpec v2, and Saturn-facing architecture being specified without collapsing their owners. This is evidence of repository formation, committed mechanisms, bounded executions, and candidate architecture. It is not evidence that a complete three-pillar system was integrated, publicly shipped, deployed, adopted, production-ready, or operationally closed.

Evidence: source identities `arcanum/README.md`, `arcanum/framework/runtime/README.md`, `AGENTS.md`, `cyberAlchemy-v2/SOURCE-MAP.md`; selectors `arcanum/README.md#Capability-Model`, `arcanum/framework/runtime/README.md#Model`, `AGENTS.md:7-12`, `AGENTS.md:145-149`, `cyberAlchemy-v2/SOURCE-MAP.md:14-19,25-31,54-58`; explorer returns `Beer current-boundary findings`, `Russell repair`.

## Candidate / owner / witnessed / sound / verdict matrix

“Witnessed” identifies the admitted evidence type. “Sound” asks whether the proposed historical statement stays within that evidence’s ceiling.

| Candidate historical claim | Owner | Witnessed by | Sound? | Verdict |
| --- | --- | --- | --- | --- |
| The April 20 parent commits record workspace formation around separate repositories | Root repository and `.gitmodules` topology | Git events and topology history; `Beer milestones 1-2` | Yes, if limited to repository formation | Accept and lead the early chronology |
| Early research, routing, planning, telemetry, guards, and recovery mechanisms entered the record | Root repository | Git events; `Beer milestones 3-4` | Yes, as committed mechanisms and controls | Accept, merge, and compress |
| Arcanum became separately owned and developed public capability/runtime surfaces | Arcanum repository and owned documentation | Nested Git plus current owner docs; `Beer milestones 5-7 and 14`, `Simon Arcanum findings` | Yes, with uneven seams and no adoption/reliability inference | Accept as one two-period section |
| Formalization corrected specific claims and distinctions | Lean formalization repository/history | Formal history and nested Git; `Ashby coverage/gap 8` | Conditional on exact invalidation and date binding | Accept only decisive corrections; compress the catalogue |
| Poker Team activity proves validation outcomes | Poker Team repository | Nested Git chronology only; `Ashby gap 2` | No | Keep chronology; defer all outcomes |
| June commits record selective public export | Root repository | Git events; `Beer milestone 9` | Yes, if “selective” remains narrow | Accept; do not imply public DomainSpec or Saturn |
| The concept map records a private three-pillar synthesis without owner collapse | Framework-unification concept map; current boundary owned by `AGENTS.md` | Private architecture synthesis/current boundary; `Beer milestone 10` | Yes, as documented architecture | Accept; reject completed-integration wording |
| Deterministic derivation universally compiles intent into tests | Round-trip report | Source-reported execution; `Simon first return milestone 3` | No | Replace with one bounded pass plus one bounded failure |
| CAV2 records a private authority-spine design | CAV2 owner sources | Git, private authority sources, dated design; `Beer milestone 12` | Yes, as design and routing | Accept; reject shipped/public/production wording |
| DomainSpec v2 is a separately governed candidate program | Root path chronology for `projects/domainspec-v2` | Git chronology; `Beer milestone 13` | Yes, for June-July chronology only | Accept chronology; defer present status |
| UI Studio is a bounded local dogfood witness | UI Studio owned README | Owned status and source-reported local validation; `Simon recovery milestone 4` | Yes, if checks are marked not rerun | Accept one paragraph |
| Ontology carrier, IDE Extension, and Akashic prove an integrated autonomous system | Candidate receipt and owned READMEs | Bounded local evidence; `Simon witness findings` | No | Keep compact witnesses; reject system-level inference |
| Mint is shipped or promotes authority | Mint candidate documentation | Bounded reported implementation; `Simon Mint findings` | No | Keep at most one qualified sentence |
| The current repository proves complete three-pillar integration and operational closure | Separate current owners | Current owner documentation; `Beer current-boundary findings`, `Russell repair` | No | End by explicitly rejecting the claim |

## Contradictions and attribution gaps

- **Root README versus later repository evidence:** treat the README as a stale April snapshot; do not let it override later owner/topology evidence.
- **Historical CyberAlchemy naming versus private CyberAlchemy v2:** attribute the former to Arcanum’s historical vocabulary and the latter to the private authority spine. Never merge them into one owner or chronology.
- **Deterministic derivation report versus stale implementation README:** the round-trip report owns the scoped reported pass/fail results; the stale README is a surfaced conflict, not corroboration.
- **Current owner documentation versus historical events:** use current sources for today’s boundary only. Root and nested Git own dated historical events.
- **Formal retrospective dates:** retain only commit-bound dates; otherwise label the formal history retrospective.
- **Poker Team outcomes:** chronology is witnessed, outcomes are not. No outcome statement enters the history.
- **Akashic origin:** the bounded graph can be described, but no dated origin is admitted.
- **DomainSpec v2 present status:** path history supplies chronology but not a current completion verdict.
- **Source-reported validations:** deterministic derivation, UI Studio, and Mint evidence was not rerun in this writer step; preserve that attribution.
- **Arcanum seams:** separate public ownership and documented capability/runtime surfaces are witnessed, but parity, uniform observation, reliability, and completed integration are not.
- **Saturn attribution:** the dated layer map owns only design and gap framing. It does not witness a repository, implemented loop, public surface, deployment, or operation.

## Editorial compression and exclusion rules

Compress the Lean construction catalogue, April commit enumeration, repeated owner-boundary prose, routine gitlink updates, DomainSpec v2 inventories, Mint, and broad portfolio itemization. Merge overlapping Arcanum material into the two-period owner-centered section and merge local candidates into **Bounded local witnesses**.

Defer Poker Team outcomes, a dated Akashic origin, unbound Lean dates, current public claims inferred from historical observations, DomainSpec v2 present status without an exact current selector, and strong maturity labels without bounded criteria.

Exclude philosophical prehistory, prohibited source-spine substitutions, category collapses, ambiguous DomainSpec/CyberAlchemy attribution, public DomainSpec or Saturn, completed framework integration, candidate or receipt as authority, and unsupported external outcomes.

## Closure status and remaining uncertainty

The evidence set is sufficient to draft a balanced repository-centered history with non-vacuous accepted changes. It is not sufficient to assert unverified validation outcomes, backfill missing dates, reconcile every stale status document, or elevate local witnesses into integrated-system proof. Those gaps should remain visible rather than being repaired through narrative inference.
