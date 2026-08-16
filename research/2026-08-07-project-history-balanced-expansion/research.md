# Verbatim explorer returns

## Explorer Simon — empirical/product/runtime lane

### Source-family census

- Legacy DomainSpec: release chronology and claimed delivery surface are well represented, but README scenarios are illustrative, not product evidence.
- Arcanum: substantial implemented public capability/runtime history exists from May onward and is almost absent from the narrative chronology.
- Root implementation experiments: deterministic test derivation provides the clearest build–fail–repair milestone.
- Applied projects: IDE Extension and Akashic Records provide bounded executable witnesses; Body War, co-op-engine, and ontology workbench artifacts show dogfooding/prototype evolution but require careful ceilings.
- CyberAlchemy v2 development: Mint is unusually mature candidate-local runtime work, while still explicitly private and intended-not-shipped.
- Ops/telemetry: receipts demonstrate repeated governed workflow use and maintenance, but are operational evidence, not proof of product outcomes or production adoption.

### Milestone candidates

1. **2026-05-14 to 2026-05-18 — Arcanum becomes an executable and observable public capability system**
   - Evidence: `git -C arcanum log --reverse --date=short --format='%ad %h %s'`; commits `4a5ede5` through `871d902`, including tier structure, lifecycle, registry, Invoke runtime assets, observed-run hooks, experiment harness, centralized telemetry, and Observed Invocation Loop promotion.
   - Primary selectors: `arcanum/README.md#Observability-Layer`, `#Experiment-Harness`, `#Capability-Model`; `arcanum/framework/observability/README.md#What-To-Observe`; `arcanum/framework/observability/OBSERVED-RUNS.md#Run-Bundle-Layout`.
   - Why it matters: the current history jumps from philosophy/formalization to the August three-pillar synthesis, leaving the public “how” pillar looking declarative rather than built through concrete runtime and feedback machinery.
   - Claim ceiling: released repository capability and implemented local framework surfaces; not proof every capability works, is adopted, or runs in production.
   - Recommendation: **ADD**, with medium-high narrative weight immediately after the May Lean spine section; **REORDER** the first substantive Arcanum explanation from August into this chronology.

2. **2026-06-01 to 2026-07-23 — Arcanum’s runtime pivots from host-specific adapters toward capability-bound native execution**
   - Evidence: `git -C arcanum log --date=short --format='%ad %h %s' -- framework/runtime framework/observability tools`; relevant events include `fb4079d` “runtime adapter handoff surface” (2026-06-01), `7149609` runtime-support installer fix (2026-06-12), and `40e12db` “capability-bound native runtime” (2026-07-23).
   - Primary selector: `arcanum/framework/runtime/README.md#Model`, `#Adapters`, `#Event-Ownership`; especially the deprecated `tools/arcanum-runtime-run` wrapper and statement that Codex/Claude/Copilot are host surfaces, not the runtime model.
   - Why it matters: this is an engineering pivot toward portable workflow ownership and durable evidence, not merely a taxonomy of sigils and spells.
   - Claim ceiling: implemented generic execution substrate and adapter boundary; native dispatch capability exists, but this does not prove deployment, universal host parity, or successful execution of every route.
   - Recommendation: **ADD** as a compact evolution paragraph; **QUALIFY** the current “public capability surface” statement with the distinction between implemented substrate and route-by-route deployment.

3. **2026-06-15 — deterministic derivation succeeds only after an honest coverage failure**
   - Evidence type/date: document frontmatter and validation report, 2026-06-15.
   - Primary selector: `development/deterministic-test-derivation-engine/L0-ROUNDTRIP-REPORT.md#Gate-verdict-financial-settlement-7-docs`, `#History-the-original-4-doc-FAIL-retained-for-provenance`, `#Second-feature-auth-access-control`, `#Interpretation--promotion-decision`.
   - Evidence: the first four-document run missed 11 obligations; expanding the parser to all seven aspect documents yielded `MISSING = 0`, 33/33 tests, and byte-identical consecutive runs. A second feature remained `FAIL (honest)` with 30 misses localized to identity-convention drift.
   - Why it matters: this is the strongest empirical realization of v1’s central deterministic spec-to-test claim, and it shows a concrete correction: input scope and identity conventions were part of the semantics.
   - Claim ceiling: passing scoped validation for one seven-document feature and an honest bounded failure on another; not a universal compiler, production pipeline, or proof all DomainSpec documentation is derivable.
   - Recommendation: **ADD** after the v2-program opening or v1-import discussion; medium-high weight. It materially balances the formal Lean failures with an implementation failure-and-repair story.

4. **2026-06-08 to 2026-07-21 — applied dogfooding produces a local workbench, not an autonomous IDE agent**
   - Evidence: root Git command `git log --date=short --format='%ad %h %s' -- projects/ide-extension`; milestones include `35b7d2ca` “Implement DomainSpec runtime and IDE updates” (2026-07-15), `65f70399` open-poll bridge (2026-07-19), and `f71276ab` workbench interaction surfaces (2026-07-21).
   - Primary selector: `projects/ide-extension/README.md#Current-Status`, `#Running`, `#Boundary`, `#First-Witness`.
   - Evidence: local-only server witness, bounded manual session bridge, complete workbench bridge demo, and trusted-local whole-document operations; provider execution, browser control, VS Code wrapper, and autonomy remain deferred or unproven.
   - Why it matters: this is direct evidence that governance concepts were tested at a human approval and durable-state boundary, revealing that “IDE agent” was too large a claim and forcing an L0 witness strategy.
   - Claim ceiling: runnable trusted-local prototype and bounded interaction witness; not an autonomous worker, IDE integration, provider-backed runtime, or production tool.
   - Recommendation: **ADD**, low-medium weight as applied-project evidence; **QUALIFY** aggressively.

5. **2026-07-26 onward — Akashic Records becomes a bounded executable knowledge-governance witness**
   - Evidence: root Git history should be cited with `git log --date=short --format='%ad %h %s' -- projects/akashic-records`; current primary status is in `projects/akashic-records/README.md#Current-Status`, `#The-Implemented-Contract`, `#How-Agents-Participate`, and `#The-Bounded-Graph`.
   - Evidence: schemas, validators, deterministic projections, inverse source lookup, six graph questions, two isolated periodic-table runs, skill dry runs, and passing `npm test` / `npm run accept:periodic-table-v1` are reported on current bytes.
   - Why it matters: it demonstrates the evidence/authority separation in a concrete product-shaped system: retrieval, review, and receipts are built while truth, fair interpretation, legal permission, and operational ownership remain outside proof.
   - Claim ceiling: implemented local experimental witness with reported passing tests and offline acceptance; not production readiness, source truth, live Git transport, deployment, or accountable adoption.
   - Recommendation: **ADD**, medium weight in a short “applied witnesses” subsection rather than expanding the main theory chronology.

6. **2026-07-02 to 2026-08-06 — Mint evolves from an intended sigil into a bounded transactional private runtime**
   - Evidence: root `git log --date=short --format='%ad %h %s' -- cyberAlchemy-v2/development/mint`, including `fad671ae` (2026-07-02) and research/audit receipts on 2026-08-06.
   - Primary selectors: `cyberAlchemy-v2/development/mint/README.md#Problem-solved`, `#Lifecycle-expectations--open-blocks`; `cyberAlchemy-v2/development/mint/runtime/README.md#Effect-and-owner-boundary`, `#Validation`.
   - Evidence: deterministic package checks, render/plan, create-only application, exact recovery, transition checks, and synthetic fixture tests are implemented; scaffolding, repository attachment, ratification, signing, public attachment, and complete Mint remain excluded.
   - Why it matters: this is the clearest example of the authority spine constraining implementation effects, including explicit recovery and no-overwrite behavior.
   - Claim ceiling: candidate-local private runtime validation and synthetic create/recover evidence; intended-not-shipped, promotes nothing, and does not prove a repository was minted.
   - Recommendation: **ADD** only as a carefully fenced implementation case; otherwise **COMPRESS** into the CyberAlchemy v2 section. Never expose private semantic details in a public history.

7. **2026-06-08 to 2026-08-06 — Body War/co-op prototypes show iterative product visualization, but mixed evidence maturity**
   - Evidence: `git log --date=short --format='%ad %h %s' -- projects/body-war projects/co-op-engine`, including Body War scaffold (2026-06-08), pilot fixtures (2026-06-09), auth/runtime work (2026-06-22 to 06-30), reproducible ontology–DomainSpec proof (2026-07-27), business ontology views (2026-07-29/30), and whole-system explorer (2026-08-06); co-op collaboration evidence (2026-07-27), deployment hardening (2026-07-30), canvas evidence (2026-08-06).
   - Primary selectors: `projects/body-war/README.md#Current-Baseline` explicitly says the initial pass contained no application prototype; later claims require their specific receipts, not that README. Co-op currently exposes `projects/co-op-engine/index.html` plus `infra/`.
   - Why it matters: these projects are feedback environments where views, deployment packaging, and ontology explanations were iterated. They prevent a history composed only of framework documents.
   - Claim ceiling: repository milestones and bounded prototype/evidence artifacts; no general product success, user validation, live service, or production adoption.
   - Recommendation: **COMPRESS** into a small ecosystem paragraph; **EXCLUDE** detailed feature chronology unless corresponding validation receipts are individually audited.

### Main omission and proposed narrative weight

The largest imbalance is not too much Lean by itself; it is that the empirical “how” and applied feedback loops are nearly absent. Suggested new weight:

- Arcanum executable/observable evolution: 2–3 paragraphs.
- Deterministic derivation fail–repair milestone: 1 substantial paragraph.
- Applied witnesses (IDE Extension, Akashic Records, Body War/co-op): 1–2 paragraphs total.
- Mint: at most 1 tightly fenced paragraph, or a sentence in CyberAlchemy v2.
- Keep release/prototype/validation/production distinctions explicit in every paragraph.

### Explorer receipt residue

- Applied-project census was bounded to historically strongest witnesses; not every `projects/` subtree was audited.
- Current README-reported test passes were not rerun because the lane requested historical research, not live execution validation.
- Two requested child spawns for actions `spawn-0002` and `spawn-0003` failed with `agent thread limit reached` and were reported to the parent.
- Writer should verify the exact Akashic Records first-commit date and audit project-specific validation receipts before assigning stronger-than-prototype claims.

## Explorer Simon — recovery run, independent product/runtime result

The history is intellectually and governance-heavy but underweights the repository’s concrete engineering arc after May. The largest omissions are the deterministic test-derivation engine, Arcanum’s runtime/observability substrate, the UI Prototyping Studio dogfood loop, and bounded CyberAlchemy prototype execution. These should be added as applied milestones with strict evidence ceilings.

### Source-family census

| Source family | Live evidence | Historical value | Ceiling |
|---|---|---|---|
| Legacy DomainSpec releases | `implementation/domainspec/CHANGELOG.md` release sections `1.0.0`–`2.1.0`; `README.md#The-Pipeline-at-a-Glance` through `#Stage-10` | Shows rapid vertical expansion from typed kernel to delivery framework | Release/changelog evidence for repository capability, not deployment or production success |
| Deterministic derivation engine | `implementation/domainspec/tools/test-derivation-engine/README.md#Pipeline`; Git history dated 2026-06-15–29 | Concrete pivot from LLM-backed generation to deterministic compilation | Implemented repository machinery; live README is stale at L0, and no current test run was performed |
| Arcanum runtime | `arcanum/framework/runtime/README.md#Model`, `#Run-Folder`, `#Status-Model`, `#Adapters`; Arcanum Git 2026-05-21 and 2026-06-01 | Explains how the “how” became a runtime-neutral handoff/evidence substrate | Public framework/runtime contract, not proof every route is deployed |
| Arcanum observability | `arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md#Current-Architecture-In-One-Sentence`, `#Source-Inventory`, `#Runtime-Data-Model`; Arcanum Git 2026-05-18 | Concrete feedback-loop infrastructure predates the August synthesis | Implemented/documented telemetry architecture with explicitly planned and uneven seams, not production convergence |
| UI Prototyping Studio | `projects/ui-prototyping-studio/README.md#Proven-implementation-scope`, `#Status`; root Git 2026-06-19, 2026-07-06, 2026-07-27 | Best evidence of governed tooling applied to a usable local product loop | Locally reproducible implementation and scoped browser checks; not human ergonomics, accessibility completion, publication, or release |
| Whisky Doses | `projects/whisky-doses/prototype/index.html`; Git commit `72a8d4b7` dated 2026-05-24; `projects/whisky-doses/domainspec/README.md` | Early project-facing DomainSpec application/prototype bundle | Prototype and thin runtime-reference bundle only |
| Equalizator | `projects/equalizator/docs/features/nl-eq-translation/CHANGELOG.md#2026-04-25` | Concrete application domain used to exercise specification structure | Specification/experiment-ready boundaries, not implemented translator |
| Ontology candidate graph | `.../SWU-OCGP-001/TASK-SESSION-RESULT.md#Evidence`, `#Boundary`; Git `29c5dc52` dated 2026-07-27 | Concrete candidate-local execution of authority-safe ontology tooling | Eight passing carrier tests and byte stability only; no relation semantics, grounding, persistence, admission, or promotion |
| Mint | `cyberAlchemy-v2/development/mint/README.md#Lifecycle-expectations-open-blocks` | Records intended authority-casting direction and open blocks | In-development design; not shipped implementation |
| Recent research/dogfood receipts | `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/execution/ACCEPTANCE-AUDIT.md`; 2026-08-05 native-run receipts | Evidence that orchestration and Task Session machinery were exercised against repository work | Bounded experiment/run evidence, not generalized reliability or production proof |

### Milestone recommendations

#### 1. Deterministic derivation becomes real repository machinery

- **Date/evidence:** 2026-06-15–29, Git repository events: `git -C implementation/domainspec log -- tools/test-derivation-engine`; `23b6840` (2026-06-15), `5631765`, `53d8f08`, `0fe69b6` (2026-06-21), `33859b5` (2026-06-29).
- **Primary selector:** `implementation/domainspec/tools/test-derivation-engine/README.md#Pipeline`.
- **Claim:** The project implemented a no-LLM/no-network compiler path from canonical Markdown through typed graph and pure derivation rules to byte-stable obligations and runnable tests, replacing the earlier LLM-backed generator.
- **Why it changes understanding:** The current history says only that two import seams were present. It misses the key engineering pivot from aspirational deterministic derivation to an actual compiler-shaped tool.
- **Ceiling:** Implemented repository capability. The README’s `#Status` still says L0 stubs, contradicting later Git events; do not claim current completeness without rebuilding.
- **Recommendation:** **ADD**, immediately after the v2 program begins or inside the June 29–July 13 migration section.

#### 2. Arcanum acquires a runtime-neutral execution substrate

- **Date/evidence:** Arcanum Git: `git -C arcanum log --follow -- framework/runtime/README.md`; `91e5a8c` (2026-05-21), `fb4079d` (2026-06-01).
- **Primary selectors:** `arcanum/framework/runtime/README.md#Model`, `#Run-Folder`, `#Status-Model`, `#Adapters`.
- **Claim:** Arcanum separated workflow meaning from runtime-specific execution through durable handoffs, status/event evidence, and adapters; native `local-skill` became the default while model-backed CLI execution remained explicit legacy behavior.
- **Why it changes understanding:** The current narrative jumps from philosophy and DomainSpec releases to the August owner map. It does not explain how Arcanum became more than a collection of prompts.
- **Ceiling:** Public framework/runtime contract and repository implementation, not evidence every capability route ran successfully.
- **Recommendation:** **ADD**, as a May 21–June 1 engineering milestone.

#### 3. Observability becomes append-only capability evidence

- **Date/evidence:** Arcanum Git: `git -C arcanum log --follow -- framework/observability/README.md`; `aba53dc` and `2983e72`, both 2026-05-18.
- **Primary selectors:** `arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md#Current-Architecture-In-One-Sentence`, `#Source-Inventory`, `#Runtime-Data-Model`.
- **Claim:** Arcanum gained observed-run bundles, a canonical append-only invocation ledger, rebuildable indexes, privacy boundaries, and reflection routing.
- **Why it changes understanding:** This is the empirical precursor to the later Saturn-style evidence loop, while still respecting that Saturn itself is private and unshipped.
- **Ceiling:** Repository-local observability substrate. The architecture explicitly retains planned components and uneven direct-skill observation.
- **Recommendation:** **ADD** alongside the runtime milestone; **QUALIFY** any wording suggesting a closed or uniform feedback loop.

#### 4. UI Prototyping Studio becomes the strongest applied dogfood case

- **Date/evidence:** Root Git: `46157a70` (2026-06-19), `9ded2565` (2026-07-06), `8752742c` (2026-07-27), from `git log --follow -- projects/ui-prototyping-studio/README.md`.
- **Primary selectors:** `projects/ui-prototyping-studio/README.md#Proven-implementation-scope`, `#Status`.
- **Claim:** A standalone local product implemented a governed variant-selection, annotation, mutation-draft, approval, Accept/Revert, evidence, and handoff loop. Its recorded audit reports TypeScript passing, unit/slice 72/72, and Playwright 21/21.
- **Why it changes understanding:** It supplies the clearest concrete use case for the project’s ideas: governance embedded in an interactive tool rather than existing only as prose and schemas.
- **Ceiling:** Recorded locally reproducible scoped validation. It explicitly does not establish full accessibility, human ergonomics, publication, or release.
- **Recommendation:** **ADD** substantial narrative weight in June–July; this deserves more space than several individual formalization constructions.

#### 5. Candidate ontology tooling crosses from plan to bounded code

- **Date/evidence:** 2026-07-27 repository event, `git log -- .../TASK-SESSION-RESULT.md`, commit `29c5dc52`.
- **Primary selectors:** `cyberAlchemy-v2/development/ontology-candidate-graph-prototype/planning/work-pack/session-evidence/SWU-OCGP-001/TASK-SESSION-RESULT.md#Evidence`, `#Boundary`.
- **Claim:** SWU-OCGP-001 implemented a closed candidate carrier that accepted a five-node fixture and rejected unknown kinds, authority-bearing candidates, duplicate IDs, unresolved endpoints, and unknown fields; the receipt records 8 passing tests and byte stability.
- **Why it changes understanding:** It shows the authority discipline affecting executable design—especially the prohibition on authority-bearing candidates—without pretending ontology admission exists.
- **Ceiling:** Carrier validation only; explicitly excludes semantics, grounding, policy disposition, projection, persistence, ontology admission, and promotion.
- **Recommendation:** **ADD** as a short July applied milestone.

#### 6. Early applied projects should appear, but compactly

- **Whisky Doses:** Git `72a8d4b7`, 2026-05-24; `projects/whisky-doses/prototype/index.html` and `projects/whisky-doses/domainspec/README.md`. **COMPRESS** into one sentence as an early project-facing planning/prototype bundle. Ceiling: prototype/reference bundle.
- **Equalizator:** `projects/equalizator/docs/features/nl-eq-translation/CHANGELOG.md#2026-04-25`. **QUALIFY** as a specified application domain, not an implemented NL-to-EQ system.
- **Mint:** `cyberAlchemy-v2/development/mint/README.md#Lifecycle-expectations-open-blocks`. **EXCLUDE** from completed milestones; mention only as current in-development direction if needed.

### Narrative-weight correction

Recommended ordering:

1. Keep the March–April philosophical and formal-audit origins.
2. After the v1 release expansion, insert the May Arcanum observability/runtime formation.
3. Place Whisky Doses as a compact early applied example.
4. In June, give the deterministic derivation engine a full paragraph.
5. In June–July, give UI Prototyping Studio a full applied/dogfood paragraph.
6. In late July, add the candidate ontology carrier as bounded execution.
7. Compress some Lean milestone enumeration so implemented product history is not visually subordinate to proof chronology.

### Technical failures and pivots worth naming

- **LLM derivation replaced by deterministic compilation:** exact engine README and 2026-06 Git sequence above. **ADD**.
- **Runtime decoupled from Codex Goal/model-specific state:** runtime `#Model` and `#Adapters`. **ADD**.
- **Direct native-skill observation remains uneven:** observability architecture plus inventory residue. **QUALIFY**.
- **Generated/staged evidence is not authority:** OCGP receipt `#Boundary`. **ADD** as a concrete enforcement example.
- **README/status drift exists:** derivation engine `#Status` describes L0 stubs despite later implementation commits. **QUALIFY** and identify as documentary drift, not tool failure.
- **Application artifacts can be specs without products:** Equalizator changelog. **EXCLUDE** from implementation claims.

### Receipt residue

- No live rebuild of the deterministic derivation engine was performed.
- UI Studio test counts are source-recorded and were not rerun.
- The derivation-engine README status is stale relative to later Git commits.
- The project corpus contains many plans and receipts; only the strongest bounded applied examples were promoted into recommendations.

## Explorer Beer — repository/system history findings

### Source-family census

- Root Git history: primary repository-event evidence from `git log --reverse --date=short --pretty=format:'%ad %h %s' -- . ':(exclude)business-philosopher'`. Observed span begins `2026-04-20 d96abdc3` and continues through 2026-08-07. Strong for when repository states entered this checkout; not proof of idea birth, deployment, or production use.
- Root README/manifests: `README.md:1-181`, `.gitmodules:1-20`, and their file-specific Git histories. README is a dated legacy operating-model snapshot; `.gitmodules` is current topology evidence.
- Current owner/boundary sources: `AGENTS.md:7-12,124-149`; `cyberAlchemy-v2/SOURCE-MAP.md:14-18,30,56-57`; `cyberAlchemy-v2/README.md:96,134-140`. These outrank old README prose for current public/private and authority boundaries.
- Arcanum: independent submodule Git history via `git -C arcanum log --reverse --date=short --pretty=format:'%ad %h %s'`, plus `arcanum/README.md`. Primary evidence for the public capability repository’s formation and later runtime work.
- DomainSpec v2/CAV2: path histories via `git log ... -- projects/domainspec-v2` and `git log ... -- cyberAlchemy-v2`; current owner prose and definitions are corroboration, not shipment evidence.
- Architecture reconciliation: `cyberAlchemy/agentic-system-deep-dive.md:100-187`; `projects/framework-unification/CONCEPT-MAP.md:31-32`; `ops/development/2026-06-21-paper-saturn-explainer/SATURN-LAYER-MAP.md:39-45,59-81,89-98,120-147`.
- Operations/telemetry/sessions: census found 580 files under `ops/development` (depth ≤2), 2 under `telemetry` (depth ≤3), and 46 top-level session files. Sampled only where Git chronology or architecture reconciliation established a material transition. These are evidence records, not authority by volume.
- `PROJECT-HISTORY.md` was reviewed as the target under revision. Business Philosopher was not used as a history source.

### System-evolution milestones and recommendations

1. **2026-04-20 — DomainSpec Core repository birth and initial owned topology**
   - Evidence: `git show --stat d96abdc3`; `git show --stat 01f8ed53`; `git log --reverse --date=short --pretty=format:'%ad %h %s' -- .gitmodules`.
   - Result: `d96abdc3 Task 1: Initialize domainspec-core repo structure`; the same day `01f8ed53` wired implementation and validation submodules.
   - Significance: the current root was born as an orchestration/research workspace around separately owned implementation and validation repositories, not as the original DomainSpec implementation repository.
   - Claim ceiling: repository formation/topology only.
   - **ADD**, with high narrative weight. Current history incorrectly centers May corpus imports and omits the root repository’s actual April 20 birth.

2. **2026-04-21 to 2026-04-28 — root becomes a governed research/orchestration hub**
   - Evidence: root Git sequence `e4bcb199`, `d717befd`, `6aab2a50`, `3b03562b`, `6158e841`, `7e17ad9c`; `README.md:1,8-18,27-50,109-160`; `git log --follow --date=short -- README.md`.
   - Result: asset governance, canonical research paths, a research planner/ID-link constitution, MARS naming, removal of root implementation mirrors, and research workflow contracts.
   - Significance: establishes an early owner split: root orchestration/research versus implementation submodule.
   - Claim ceiling: repository operating model as asserted and committed then; not current authority.
   - **ADD/COMPRESS** into one early-formation passage.

3. **2026-04-26 to 2026-05-07 — definitions-first governance and telemetry-backed task routing emerge**
   - Evidence: root Git commits `ba0838d8`, `b0df101a`, `9bfb7330`, `d41d5a0d`, `ec0aeded`, `82e6603d`, `acad68a4`, `ad81cf89`, `bd673289`, `451316ad`, `1ce5fe93`.
   - Result: canonical definitions ownership, definitions-source-first research, interactive task sessions, planner gates, work-pack routing, delegation telemetry, watchdog and stall recovery.
   - Significance: governance and operational recovery were core architecture by early May, not later administrative additions.
   - Claim ceiling: committed workflows and telemetry artifacts; does not establish reliable autonomous operation.
   - **ADD**, medium-high weight.

4. **2026-05-11 to 2026-05-18 — operational failures drive guard and observability architecture**
   - Evidence: root commits `39d799ae` (terminal guard), `64744e78`/`1514752f`/`f0ff829b` (guard telemetry), `0e282e7d` (hook-run package), `7cb99bdd` and `8d76b219` (Arcanum experiment bridges/validation).
   - Arcanum evidence: `git -C arcanum log --reverse ...`, commits `aba53dc`, `0cf171d`, `145d1ff`, `2983e72`, `37537c4`, `a85a34e`, `9060676`, `871d902`.
   - Significance: observed-run telemetry and hardened command surfaces came from concrete terminal/stall risks; this is a correction story worth retaining.
   - Claim ceiling: repository controls and recorded experiments, not proof that every invocation was safe.
   - **ADD**, medium weight.

5. **2026-05-14 — Arcanum becomes an independently owned public repository**
   - Evidence: `.gitmodules:9-12`; `.gitmodules` Git event `2026-05-14 0e9d5e71 Link Arcanum command bundle`; Arcanum commits beginning `2026-05-14 4a5ede5 Initial commit`, followed by sigil tiers, lifecycle, registry, and Necronomicon.
   - Significance: Arcanum’s separate Git ownership precedes the later polished three-pillar framing. It evolved from sigil/runtime work into the reusable public “how.”
   - Claim ceiling: independent repository and committed public framework history; not proof of external adoption.
   - **ADD**, high weight.

6. **2026-05-19 to 2026-05-24 — CyberAlchemy method and capability lifecycle consolidate**
   - Evidence: Arcanum commits `e18c5e6 Define CyberAlchemy method`, `648bb93 Refocus Arcanum README on framework method`, `91e5a8c Add task session runtime goal adapter`, `75b01f5 Promote concept optimizer as distill`, `895317d Add refine sigil lifecycle package`, `2217328 Add task session context handoff contract`; root `0b11ffde` and `32bab1d9`.
   - Significance: formation of a reusable capability vocabulary and lifecycle, not merely a renamed command pack.
   - Claim ceiling: repository capability model and runtime artifacts.
   - **ADD/COMPRESS**, medium-high weight.

7. **2026-06-05 to 2026-06-12 — migration from root command clutter to native Arcanum skills**
   - Evidence: root commits `eba0b4bc Clean root runtime command surface`, `8e7ab86f Add native Arcanum skill/agent packages`, `b08d5085 remove legacy sigils-library superseded by native skills`, `3c2deba3 Expose canonical Craft skill`.
   - Significance: a material operating-model transition from mirrored/root runtime assets toward native, separately owned capability packages.
   - Claim ceiling: committed repository cutover; not universal consumer migration.
   - **ADD**, medium weight.

8. **2026-06-10 onward — submodule discipline becomes explicit architecture**
   - Evidence: `.gitmodules` history: April 20 implementation/validation; May 14 Arcanum; June 10 orphan gitlink removal; June 17 Savvy; August 7 ZAGR; current `.gitmodules:1-20`; root commits `ce1bb259` and `9a9a4739`.
   - Significance: owned system boundaries expanded while publication order and gitlink integrity became governed.
   - Claim ceiling: declared/current repository topology; presence as submodule is not product integration or endorsement.
   - **ADD** a concise topology timeline; **EXCLUDE** routine pointer bumps except when they embody a transition or rollback.

9. **2026-06-14 to 2026-06-15 — open-core/public-export boundary is deliberately cut**
   - Evidence: root commits `abf64284 feat(keystone): land DomainSpec wedge in public arcanum + record open-core split`, `1495bac7 publish DomainSpec wedge definitions as canonical in arcanum`, `fe4c6d42 install repo-local native runtime surface`; current owner `AGENTS.md:7-12,124-149`; CAV2 routing `cyberAlchemy-v2/SOURCE-MAP.md:14-18,30,56-57`.
   - Significance: selected reusable definitions/capabilities were exported to public Arcanum while DomainSpec implementation and later CAV2/Saturn material remained private.
   - Claim ceiling: deliberate repository boundary and selected export; never “DomainSpec or Saturn shipped publicly.”
   - **ADD**, very high weight.

10. **2026-06-15 to 2026-06-16 — three systems are unified conceptually without collapsing ownership**
    - Evidence: root commits `db391d55`, `ae590b53`, `709d5d23`, `4345024b`; `projects/framework-unification/CONCEPT-MAP.md:31-32`.
    - Significance: establishes “DomainSpec says what, Arcanum says how, Saturn closes the loop with evidence.”
    - Claim ceiling: private architecture synthesis. It is not a runtime integration or release.
    - **ADD**, high narrative weight, explicitly after the open-core split.

11. **2026-06-16 to 2026-06-17 — subagent dispatch becomes governed and append-only**
    - Evidence: root commits `5d336aa7`, `788ec733`, `f197c9b2`, plus later `809e8204`/`64b25515`/`a87b7f3` refinements.
    - Significance: multi-agent work acquired confirmation, registration, attack-vector, and closure-evidence gates.
    - Claim ceiling: repository workflow governance, not proof all historical dispatches complied.
    - **ADD**, medium weight.

12. **2026-06-21 to 2026-06-30 — CAV2 authority spine and honest spec-vs-public distinction form**
    - Evidence: path birth `2026-06-21 7e776e65`; authority events `91d63252`, `6016e033`, `7dcdf8db`, `66c17bf8`, `3359af7a`, `5662be19`; `cyberAlchemy-v2/README.md:96,134-140`; `SOURCE-MAP.md:14-18,30,56-57`; `SATURN-LAYER-MAP.md:59-81,120-147`.
    - Significance: canonical vocabulary, promotion gates, source routing, non-collapse, and public/private scrubbing become explicit. The June 21 layer map contemporaneously records that public Arcanum presented the “how” alone while Saturn/DomainSpec framing remained private/intended.
    - Claim ceiling: private authority architecture and gap analysis; no public shipment or production proof.
    - **ADD**, very high weight.

13. **2026-06-30 to 2026-07-23 — DomainSpec v2 is a new governed program, not the legacy release-number sequence**
    - Evidence: path history for `projects/domainspec-v2`, especially `b0f35d43`, `a10f0de3`, `abf03f66`, `ce49f4cd`, `b0ae56b8`, `bf88890b`, `789261ef`, `25a665a5`, `f0116e66`, `076be658`, `edce4249`, `35b7d2ca`, `9036334c`.
    - Significance: definitions, meta-type formalism, relationship authority, spec homing, non-collapse, attestations, residue receipts, runtime/IDE work, and proof/minting primitives accumulate in a separately governed v2 effort.
    - Claim ceiling: committed candidate implementations, contracts, and receipts. A “production release contract” is a contract, not released production.
    - **ADD/REORDER** after CAV2 formation.

14. **2026-07-27 to 2026-08-06 — Arcanum runtime hardens into explicit chained governance**
    - Evidence: Arcanum commits `9c05b1f`, `71c5b8b`, `a87b7f3`, July 30 readiness/goal/task-session deterministic execution series, `c09f11d`, and August 6 `decae2e`, `ced0ac4`, `a5c8bc5`.
    - Significance: later Arcanum history formalizes admission, immutable readiness, bounded joins, reconciliation, crash-safe resume, confirmation, and portable execution entry.
    - Claim ceiling: committed runtime mechanisms plus evidence artifacts, not generalized reliability.
    - **ADD**, medium-high weight near the present-state close.

### Stale-versus-current source conflicts

- **Root README is stale.** `README.md:1` still calls the checkout a “Unified 3-Project Workspace”; `README.md:12-18` points to `/home/vrondelli/projects/poker-team/domainspec` and says implementation changes happen there; `README.md:112` describes `implementation/domainspec` as a symlink. Current `.gitmodules:1-4` makes it a Git submodule, and current owner routing is in `AGENTS.md`. **QUALIFY** README as a 2026-04-28 operating-model snapshot.
- **June 21 Saturn/public map is historically valuable but partially stale.** `SATURN-LAYER-MAP.md:59-81` describes what the public site exposed then. Its durable boundary warning at `120-147` agrees with current `AGENTS.md:7-12`, but public-surface details require live publication checking before current claims. **QUALIFY**.
- **“Stable repository” is a commit label, not maturity proof.** CAV2 birth commit `7e776e65` says “stable repository,” while `cyberAlchemy-v2/README.md:134-140` still marks extraction/publication questions open. **QUALIFY**.
- **PROJECT-HISTORY framing is imbalanced.** `PROJECT-HISTORY.md:10-16` says it joins Business Philosopher and Lean histories, then gives repository formation only a short May subsection. This omits the April 20 root birth, April–May governance operations, Arcanum’s independent formation, open-core cut, CAV2 authority spine, and dispatch/submodule evolution. **REORDER** around repository events.
- **Current public/private correction:** `AGENTS.md:7-12` is unambiguous: DomainSpec is private “what,” Arcanum public “how,” Saturn private/spec and not a folder, CAV2 private authority spine. Any narrative suggesting the three-pillar system is publicly shipped must be **EXCLUDED**.

### Proposed narrative weight

- 15% root birth, original submodule topology, and early research/orchestration model.
- 15% definitions-first governance, task routing, operational failures, guards, and observability.
- 20% Arcanum’s independent birth and evolution into public reusable capability/runtime ownership.
- 15% open-core/public-export decision and framework-unification without ownership collapse.
- 15% CAV2 authority spine, promotion/non-collapse/source-routing gates.
- 10% DomainSpec v2 as a distinct governed reformulation/implementation program.
- 5% dispatch governance and append-only operational evidence.
- 5% current claim boundary and unresolved public/spec gap.

Routine commits, portfolio project additions, and pointer bumps should be **COMPRESSED** or **EXCLUDED** unless they establish a boundary transition, failure/recovery, or owner change.

### Receipt residue

- A full commit-by-commit operational incident audit was outside this bounded synthesis.
- Current public-site contents were not live-verified; June 21 publication observations remain historical evidence only.
- Several commit subjects assert implementation or validation; claims remain capped at committed repository evidence unless separately rebuilt.

## Explorer Ashby — coverage and chronology audit

### Executive finding

`PROJECT-HISTORY.md` is not yet a balanced history of DomainSpec Core. It is a 5,337-word synthesis whose 2,909-word chronology gives roughly 1,667 words (57.3%) to the excluded Business Philosopher/formal-philosophical lineage and Lean correction arc, while giving no dedicated chronological section to Arcanum, Poker Team validation/dogfooding, the root research program, the development program, or the broader project portfolio.

That allocation makes the document read primarily as the intellectual and formal history of residue plus the v1→v2 authority transition. It does not yet explain how the repository became a system that builds and tests other systems.

Business Philosopher was excluded from the comparison corpus as instructed. Its 17 path references and at least 565 dedicated chronology words are reported only as target-corpus allocation that should be removed or compressed, not as comparative evidence.

### Reproducible corpus measurements

Commands:

```bash
wc -w -l PROJECT-HISTORY.md
awk '/^## /{if(h) print h "\t" n; h=$0;n=0;next}{n+=NF}END{print h "\t" n}' PROJECT-HISTORY.md
awk '/^## /{if(h) print h "\t" n; h="";n=0;next} /^### /{if(h) print h "\t" n; h=$0;n=0;next}{if(h)n+=NF}END{if(h)print h "\t" n}' PROJECT-HISTORY.md
rg -o '\[[^]]+\]\([^)]+\)' PROJECT-HISTORY.md | sed -E 's/.*\(([^)#]+).*/\1/' | cut -d/ -f1 | sort | uniq -c | sort -nr
```

Observed:

| Measure | Count |
|---|---:|
| Total words | 5,337 |
| Total lines | 648 |
| Chronology words | 2,909 / 54.5% |
| Short version | 280 |
| v1→v2 comparison | 318 |
| Concept-correction table | 459 |
| Present evidence boundary | 287 |
| Open frontiers + refused claims | 352 |
| Source map + connections | 359 |
| Markdown source links to excluded Business Philosopher | 15 |
| Links to `projects/` | 11 |
| Links to `cyberAlchemy-v2/` | 9 |
| Links to `implementation/` | 5 |
| Links to Lean history | 2 |
| Links to Arcanum | 0 |
| Links to `validation/poker-team/` | 0 |
| Links to root `research/` or `development/` | 0 |

The path-token check also found 17 `business-philosopher` mentions, 13 `projects/domainspec-v2`, 10 `cyberAlchemy-v2`, six `implementation/domainspec`, four Lean, two framework-unification, two research, one development, and no lowercase `arcanum` occurrence.

### Coverage matrix

| Historical family | Live evidence inspected | Current allocation | Date confidence | Recommendation |
|---|---|---:|---|---|
| Root repository formation | Root Git: `2026-04-20 d96abdc3`; `2026-04-20 01f8ed53` wired implementation and validation submodules | About 75 words in “repositories take shape,” but focused on the excluded corpus | High for Git event | **ADD**, **REORDER** |
| DomainSpec v1 | `implementation/domainspec/CHANGELOG.md`, `README.md`; nested Git begins `2026-03-29 fce5bdf` | 169 chronology words plus tables | High for commits/releases | Retain but **QUALIFY** and modestly **COMPRESS** |
| Poker Team validation/dogfood | `validation/poker-team/README.md`; nested Git begins 2026-01-08, adds DomainSpec 2026-04-08, pilot work through April/May, engine-derived settlement tests June 21, SFOL adapter July 27 | 0 dedicated words; 0 links | High for commits; medium for dogfood interpretation until receipts are cited | **ADD** |
| Arcanum public capability system | `arcanum/README.md`; nested Git begins 2026-05-14, adds Invoke May 16, observability/experiment May 18, CyberAlchemy method May 19, bounded execution/confirmation hardening through July/August | No chronological section and no source link | High | **ADD**, **REORDER** |
| Lean formalization | `domainspec-lean-formalization/PROJECT-HISTORY.md`; nested Git spans 447 commits, 2026-04-25 through 2026-07-23 | At least 981 dedicated formal chronology words, about 1,102 including joined-register section | High for Git; retrospective milestone dates medium unless commit-bound | **COMPRESS**, **QUALIFY** |
| DomainSpec v2 | `projects/domainspec-v2/README.md`, import and authority sources; parent path begins June 14 with 65 path commits | 385 chronology words plus tables | High for Git | Retain, slight **COMPRESS** |
| CyberAlchemy v2 | `cyberAlchemy-v2/README.md` and authority sources; parent path begins June 21 with 81 path commits | 215 chronology words plus tables | High for Git; candidate/stable status correctly qualified | Retain, **QUALIFY** |
| Framework unification | `projects/framework-unification/README.md`, `CONCEPT-MAP.md`; path begins June 15 with six commits | Only present-state references | High for Git; README says representation is design and communication Phase 2b blocked | **ADD** as pivot, not completed unification |
| Root research program | `research/system-theory-achievements/2026-06-19-domainspec-core-root-coverage/findings.md`; path begins with root April 20; 59 path commits | No historical section | High for events; findings interpretations are synthesis | **ADD** |
| Root development program | Live `development/` sources and path-limited Git; parent path begins June 22 with six path commits | No historical section | High for Git; significance source-dependent | **ADD** selectively |
| Broader projects/products | 28 immediate directories under `projects/` | Essentially absent except DomainSpec v2/framework-unification | High for directory count; status varies | **ADD** bounded strand; **EXCLUDE** market/prod claims |

### Chronological gaps and corrections

1. **Root birth is missing as the organizing event — ADD / REORDER.** Root Git records initialization and submodule topology on 2026-04-20. Add an April 20 section explaining parent repository, implementation owner, validation owner, research structure, and later public Arcanum submodule.
2. **Validation predates the parent and becomes DomainSpec dogfood — ADD.** `git -C validation/poker-team log --reverse --format='%ad %h %s' --date=short` shows the project from 2026-01-08, DomainSpec added 2026-04-08, pilot stabilization through April–May, deterministic settlement derivation June 21, and SFOL adapter July 27. Present as validation/dogfood, not profitability or production proof.
3. **Arcanum’s birth and evolution are absent — ADD / REORDER.** Give it a 350–500-word strand while keeping public Arcanum distinct from private DomainSpec/Saturn.
4. **April’s research/governance formation is almost entirely absent — ADD.** April 20–28 commits establish repository initialization, canonical research paths, research planner/ID-link constitution, experiment migration, knowledge-stack foundations, canonical definitions, dashboard/open-decisions automation, and governance skills.
5. **Framework unification is treated only as current context — ADD / QUALIFY.** Add it as the moment duplicated concepts and owner ambiguity became explicit; do not call unification achieved.
6. **Late July/August is compressed to current state — ADD.** Dated research directory counts are two June, nine July, and eight August. Add a thematic late-period section based on selected owned findings, not a commit list.
7. **The project/product portfolio is erased — ADD / EXCLUDE inflated claims.** Select only historically material, source-corroborated cases such as Poker Team, Ontologize, UI Prototyping Studio, and late ontology/intent-routing prototypes.
8. **Formalization dominates beyond its repository role — COMPRESS / QUALIFY.** Eight clearly formal sections total 981 words; including joined-register material reaches about 1,102 words, 37.9% of chronology. Preserve M6, schema/instance separation, count-wall correction, and claim≤proof discipline; compress construction catalogues.
9. **The excluded corpus structurally controls the opening — EXCLUDE / COMPRESS.** Remove Business Philosopher as source spine. At most retain one explicitly non-authoritative idea-lineage paragraph if final scope requires it.
10. **Current synthesis repeats authority boundaries — COMPRESS.** Consolidate repeated v2/CAV2/public-private warnings into one evidence-boundary section to make space for formation, execution, validation, products, and research.

### Candidate structure and proportions

| Strand | Proposed share |
|---|---:|
| Scope, date semantics, evidence boundary | 7–9% |
| Root formation and early DomainSpec v1 | 13–15% |
| Research/governance foundations | 9–11% |
| Validation and dogfooding, especially Poker Team | 10–12% |
| Arcanum’s public capability/runtime evolution | 12–15% |
| Formal audit and major corrections | 15–18% |
| DomainSpec v2 and CyberAlchemy v2 ownership split | 14–17% |
| Framework unification, projects, and late-July/August prototypes | 12–15% |
| Current state and open frontiers | 7–9% |

Recommended chronology:

1. Pre-parent implementation and validation roots.
2. March–April v1 delivery framework.
3. April 20 root formation and research/governance substrate.
4. April–July formal audit as one correction strand.
5. May Arcanum birth and public capability-system formation.
6. June framework unification, DomainSpec v2, and CyberAlchemy v2.
7. June–July dogfood, deterministic derivation, products, and local validation.
8. Late July–August ontology, intent-routing, work-pack, and architecture-realization phase.
9. Current evidence boundary and unresolved work.

### Receipt residue

- Portfolio projects beyond selected examples need individual owned-source inspection before narrative claims.
- Poker Team commit chronology is strong, but acceptance and dogfood outcomes require exact receipt-level corroboration.
- Retrospective Lean milestone dates remain medium-confidence until bound to exact commits or primary theorem files.
- Directory and commit counts establish presence and activity, not importance, release, adoption, or production status.
