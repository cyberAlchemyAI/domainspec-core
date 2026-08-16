## Agent 1 - Empirical visual-cognition audit

```yaml
RECEIPT:
  action_id: spawn-0001
  dispatch_id: 2026-08-09-cyberalchemy-naturalized-interface-design
  run_id: run-001
  wave_id: w1-explorers
  role: explorer-empirical
  agent_name: "Tversky, Amos"
  status: pass
  validation: pass
  blockers: []
```

### Source/version verification

- Verified `domainspec-lean-formalization/origin/main` resolves to frozen commit `a4655d938c92e25be8ffd31b6f92b7e544f86e66`.
- Verified SHA-256:
  - `research/findings.md`: `144a11ec198c019318400dd1687b70044e3d100a769397758c3a60a74ddbcb00`
  - `research-initial-definitions.md`: `a0e47281bf8c324743181998afb35496d629b37a5eaa133015550e50efea2501`
  - `research-initial-definitions-review/review.md`: `98f520c052565302dee1d5002ce5ffcef8396e09f5d539062f68b1aac2b03296`
- The findings remain a `draft`, `working-synthesis-needs-audit`, with `exit_reason: reviewer_rejected_twice` and `audit_status: rejected-after-loop-2`. The numerical evidence coverage passed, but durable provenance failed.
- Upstream records contain known attribution errors: agents 02, 06, and 07 misname You et al. (2023) as Yin et al.; agent 03 misnames Robles et al. (2021) as Roe et al. and dates the DOI `10.1057/s41599-020-00648-y` incorrectly. The corrected names in `findings.md` are used here, without treating them as repaired provenance.

Selector keys:

- `F` — `domainspec-lean-formalization/research-psychology/naturalized-digital-environments/research/findings.md`
- `ID` — `domainspec-lean-formalization/research-psychology/naturalized-digital-environments/research-initial-definitions.md`
- `IR` — `domainspec-lean-formalization/research-psychology/naturalized-digital-environments/research-initial-definitions-review/review.md`
- `E1/E2/E3` — corresponding `agents/01-explorer-gentner.md`, `02-explorer-helmholtz.md`, and `03-explorer-kay.md`
- `S1/S2/S3` — corresponding `agents/05-skeptic-tetlock.md`, `06-skeptic-kahneman.md`, and `07-skeptic-gigerenzer.md`
- `CS` — `projects/cyberalchemy-lab/development/research/2026-08-09-naturalized-interface-design/STRATEGY.md`

### C1-C4 intervention distinctions

| Class | Operational distinction | Empirical status | CyberAlchemy interpretation |
|---|---|---|---|
| C1 — task-relevant structure | A visual relation carries prespecified task information: signaling, causal links, compatible mappings, representation choice, or work-domain constraints. | Conditionally witnessed. Effects depend on task, relation, expertise, representation, incident, redesign, and measured outcome. | Test one named semantic relation, not a generally “natural” representation. |
| C2 — task-irrelevant ambient character | A specified property or scene bundle—texture, fractal statistics, spectral character, decorative detail, nature/biophilic scene—does not carry task information. | Narrow preference, discomfort, self-report, and contested bundle effects are witnessed. General cognition or wellbeing benefit is not. | Ambient presentation must remain a separate variable. It cannot justify information-architecture changes. |
| C3 — functional/ambient boundary | Relevance is assigned ex ante so the effect of a perceptual property in functional versus decorative use can be distinguished. | Witnessed only for color placement. Same-item role reversal and non-color texture/depth/irregularity/multiscale cases are unwitnessed. | Use a factorial or counterbalanced role test. Do not generalize the color result into a cross-property taxonomy. |
| C4 — coupled intervention | A current-dispatch analytical class: C1 structure and C2 ambient character change together in one redesign. | Not a source-authored C1-C3 candidate and has no direct class-level witness. Existing bundle failures show why component attribution would be impossible. | Treat as a confounded compound. Decompose it into C1 × C2 factorial cells or ablations before making any causal claim. |

Citations: `ID :: ## Context`, `ID :: ## Research Question`, `F :: ## Candidate verdict matrix`, `S3 :: # Definitional-soundness gate`. C4 is introduced by the current dispatch’s “coupled interventions” angle at `CS :: ## Groups And Subagents`; its empirical ceiling is inferred from `F :: ## Candidate verdict matrix :: C2` and `S3 :: C2/C3`, not asserted by the source package.

### Eligible evidence and failed distinctions

Eligibility required human participants, an identifiable visual manipulation/comparator, and a behavioral, cognitive, affective, comfort, or interaction outcome. Reviews were citation indexes only. Neural-only evidence, advocacy, local design artifacts, and physical-environment studies without a digital bridge were ineligible. Coverage means at least two independent eligible samples per requested family; it does not establish the intervention classes or an exhaustive search. Citation: `F :: ## Method and claim boundary`.

| Evidence | Eligible scope | Failed distinction or ceiling |
|---|---|---|
| Désiron et al.: randomized digital signaling, 91 adolescents plus independent 47-student sample | C1 signaling effects on global inference and attention | Independent comprehension result was null; signaling is not “naturalness.” `F :: ## Evidence matrix :: Visual cognition / C1 — Désiron` |
| Heiser–Tversky: 67 completers, arrows in mechanical diagrams | Arrow convention shifted functional/causal interpretation and production | Labeling and familiarity remain rivals; no universal causal-fidelity claim. `F :: ## Evidence matrix :: Visual cognition / C1 — Heiser & Tversky` |
| Jungk: 16 anesthetists plus redesign sample 8 | Specialist incident detection under an ecological display | Blood-loss result was initially null; effects depended on incident, redesign, and expertise. `F :: ## Evidence matrix :: HCI / C1 — Jungk` |
| Ghoniem: 36 participants, matrix versus node-link | Representation × task × graph size/density | Matrices were not universally superior; path finding favored node-link. `F :: ## Evidence matrix :: Visualization / C1` |
| Viengkham–Spehar: analyzed samples 171 and 179; Robles 2020: 178 | Fractal-dimension preference and aesthetic ratings | Preference clusters differed by category and person; preference cannot proxy comprehension, wellbeing, or performance. `F :: ## Evidence matrix :: Empirical aesthetics / C2` |
| Juricevic: 61 participants | Spectral slope × discomfort | This is visual comfort evidence, not proof for fractality, naturalness, merit, or wellbeing. `F :: ## Evidence matrix :: Visual comfort / C2 adverse` |
| Berto 32 versus Hicks 180 | Screen-scene restoration bundle, with positive/limited versus Bayesian-null results | Nature/restorativeness remained bundled and contested; results cannot be averaged into “nature helps.” `F :: ## Evidence matrix :: Environmental psychology / C2` |
| Yin 2019 and You 2023: independent VR samples of 30 each | Short-term bundled office/classroom interventions | Objective results diverged; plants, materials, views, lighting, and scene semantics were not isolated. `F :: ## Evidence matrix :: Biophilic design / C2` |
| Désiron–Schneider: randomized samples 128 and 140 | C3 color relevance × learning/load | Relevant contrast helped; overall color and decorative salience were learning nulls. No texture/depth/general role-switch transfer. `F :: ## Evidence matrix :: C3-color` |
| Strobel: 68 analyzed | Task-irrelevant graph details increased processing time | Accuracy was null; slower responses do not establish general harm. `F :: ## Evidence matrix :: Graph-detail adverse boundary` |
| Harp–Mayer: four experiments | Interesting task-irrelevant details impaired recall and transfer | Supports a relevance/load mechanism, not a generally harmful ambient class. `F :: ## Evidence matrix :: C1/C2 adverse boundary` |

### Transfer and claim ceilings

- Transfer is relation-and-task specific. Signaling, matrices, node-link diagrams, compatible mappings, and ecological displays are not interchangeable C1 mechanisms.
- Attention change cannot be promoted to comprehension; preference cannot become wellbeing; self-reported stress cannot become objective cognition; reaction-time reduction cannot become generally reduced effort or general benefit.
- Specialist simulation results do not transfer automatically to novice evidence navigation.
- Short screen or VR exposure does not establish sustained-use effects.
- Student, adolescent, convenience, and specialist samples do not establish population-wide effects.
- Accessibility reporting is largely absent: migraine, dyslexia, sensory sensitivity, motion sensitivity, assistive technology, and subgroup harms remain unmeasured. Default-on ambient complexity is unsupported.
- Fan/Hawkins pictorial-communication evidence is adjacent: context changes communicative drawings, but those studies do not test interfaces or ambient screen effects.
- Automated browser witnesses could verify that an intervention exists and preserves state, but cannot establish comprehension, usability, trust, comfort, preference, or learning.

Citations: `F :: ## Nulls, adverse effects, accessibility, and dissent`; `E1 :: # Controlled human evidence`; `E2 :: evidence_records[id=Judy-Fan-lead]`; `S2 :: # Non-vacuity gate`; `S3 :: # Definitional-soundness gate`.

### Interface consequence table

| Possible consequence | Source selector | Evidence class | Intervention class | Supported scope | Forbidden generalization | Discriminating experiment / disposition |
|---|---|---|---|---|---|---|
| Add explicit visual links between a source, derived claim, and consequence when the link carries task meaning | `F :: ## Evidence matrix :: Visual cognition / C1 — Désiron`; `E1 :: # Controlled human evidence` | Eligible controlled human evidence, mixed replication | C1 | A prespecified link may affect inference or visual attention | “Visible links improve comprehension” across tasks or users | Hold content and ambiance constant; randomize explicit links on/off; measure relation-identification accuracy, inference accuracy, time, and errors separately |
| Select matrix, node-link, or hierarchy views according to the task | `F :: ## Evidence matrix :: Visualization / C1 — Ghoniem` | Eligible controlled HCI evidence | C1 | Representation choice can interact with path finding, graph size, and density | One representation is globally more intuitive, natural, or efficient | Cross representation × task × graph density; measure completion time and error together |
| Expose work-domain constraints or functional relations in a specialist display | `F :: ## Evidence matrix :: HCI / C1 — Jungk`; `E2 :: evidence_records[id=C1-EID]` | Eligible specialist simulation evidence; conceptual owner separate | C1 | Named incident-detection tasks, with expertise and redesign tracked | Ecological displays are universally superior or reduce effort generally | Compare conventional versus constraint-preserving view on named anomaly/source-tracing tasks; stratify expertise and preserve per-incident results |
| Use contrast color only to mark task-relevant evidence relations | `F :: ## Evidence matrix :: C3-color`; `S2 :: # Non-vacuity gate :: C3` | Eligible randomized digital learning evidence | C3-color | Ex-ante relevant color contrast may improve retention/transfer and reduce reported extraneous load | More color improves learning; decorative color is beneficial; color findings transfer to texture/depth | Factor relevant-item contrast and decorative-item color independently; hold content, luminance, and layout stable |
| Add decorative images, labels, or texture around evidence graphs | `F :: ## Evidence matrix :: Graph-detail adverse boundary`; `F :: C1/C2 adverse boundary` | Eligible adverse/trade-off evidence | C2 | Irrelevant details may add processing time or impair transfer in specified tasks | Decoration always reduces accuracy or is always harmful | Details on/off with equal occupied area; measure completion time, error, recall/transfer, and fixation on irrelevant elements |
| Introduce fractal or multiscale ambient backgrounds to improve cognition, restoration, or learning | `F :: ## Evidence matrix :: Empirical aesthetics / C2`; `E3 :: evidence_rows[viengkham-spehar-2018-*]` | Eligible preference evidence; outcome-mismatched for task design | C2 | Preference or discomfort only, under exact stimuli and populations | Fractals improve cognition, wellbeing, calm, productivity, comprehension, or reduced effort | **NO_DESIGN_EFFECT** |
| “Biophilic” or nature-themed styling as a cognitive-performance feature | `F :: ## Evidence matrix :: Environmental psychology / C2`; `F :: Biophilic design / C2 null/mixed` | Eligible but contested/bundled short-term evidence | C2 | Exact VR scene bundles may alter some self-reports | Biophilia, greenery, or nature styling improves objective cognition or wellbeing | **NO_DESIGN_EFFECT** |
| Use the identical non-color property as functional information in one view and ambiance in another | `F :: ## Candidate verdict matrix :: C3 same-item role reversal`; `S1 :: Candidate lines :: C3 same-item/non-color` | No eligible witness; testable definition only | C3 non-color | Establishes an experimental question, not an effect | Texture, depth, irregularity, or multiscale form has a known role-dependent effect | Counterbalance the identical property and item between informational and non-informational roles; hold intensity/content constant; measure task and comfort outcomes separately |
| Ship a “naturalized redesign” changing semantic hierarchy, links, texture, depth, color, and ambiance together | `CS :: ## Groups And Subagents :: coupled interventions`; `F :: ## Candidate verdict matrix :: C2`; `S3 :: C2/C3` | Derived experimental-control requirement; no direct class witness | C4 | None as a causal effect; only as a compound prototype subject to ablation | Any observed change was caused by naturalness, structure, ambiance, fractality, or biophilia | Use a 2×2 design: C1 structure unchanged/changed × C2 ambiance absent/present; keep content and interaction states fixed |
| Default-on high-contrast, repetitive, moving, or complex ambiance | `F :: ## Nulls, adverse effects, accessibility, and dissent`; `F :: Visual comfort / C2 adverse` | Narrow discomfort evidence plus substantial missing subgroup evidence | C2/C4 safety boundary | Supports measuring tolerability and preserving controls | Such patterns are universally harmful, or user controls are already proven beneficial | Stratified tolerability study with sensory-profile reporting and intensity levels; until then, no mandatory/default-on exposure |

### Rejected claims

- “Naturalness” is one measurable beneficial cause.
- Preserving structure or causality generally improves understanding or interaction.
- Fractal preference establishes cognition, restoration, calm, wellbeing, or task performance.
- Biophilic or nature imagery generally improves objective cognition or wellbeing.
- Reduced reaction time, fixation change, or subjective load establishes generally reduced effort or overall benefit.
- Color generally improves learning.
- The same perceptual property is known to switch effects between functional and ambient roles.
- C3-color evidence generalizes to texture, depth, irregularity, or multiscale organization.
- Positive Berto/Yin results outweigh or average away Hicks/You null or mixed results.
- Task-irrelevant detail always harms accuracy.
- A coupled “naturalized” redesign permits attribution to any constituent feature.
- This corpus supplies human proof for the present CyberAlchemy interface.

Primary selector: `F :: ## Gating answer and exit`; corroboration: `S3 :: # Definitional-soundness gate`.

### Open gaps

- No eligible same-item C3 role-reversal study.
- No eligible non-color C3 witness for texture, depth, irregularity, or multiscale structure.
- No direct C4 coupled-intervention witness; factorial decomposition is required.
- Long-duration exposure, display variation, task transfer, and expert/novice transfer remain unresolved.
- Accessibility and sensory-profile effects are largely unreported.
- Database-wide negative-search denominators were unavailable.
- Direct transfer to CyberAlchemy requires a separately defined current task/selector model and new human evidence; this lane did not inspect or claim current interface behavior.
- The source package’s rejected audit and unresolved upstream provenance prevent promotion of this return into validated scientific authority.

## Agent 2 - Categorical boundary audit

```yaml
RECEIPT:
  action_id: spawn-0002
  dispatch_id: 2026-08-09-cyberalchemy-naturalized-interface-design
  run_id: run-001
  wave_id: w1-explorers
  role: explorer-schema
  agent_name: "Spivak, David"
  status: pass
  validation: pass
  blockers: []
```

### Source/version verification

- `projects/framework-unification/discovery/schema-based-learning-crosswalk.md`
  - Commit: `41deffcd2bcf1adfbaedb894dc5b6e92c36be51b`
  - Observed SHA-256: `17851e18ad3c42a99e44449d92a200fece60919e56e2d9ecd0a37f04ccbe7b5d`
  - Expected SHA-256: same
  - Boundary: candidate architecture discovery, explicitly not a promoted definition, implementation plan, theorem, or formal correspondence (`## Status and evidence boundary`, lines 14–18).
- `domainspec-lean-formalization/research-ai/schema-based-learning-category-theory/research/findings.md`
  - Commit: `a5e7887d07e0915098f7bc8a3b12021b5e0a3d0c`
  - Observed SHA-256: `8fc4823a9f62ccb9cace52523f28eedd74dac13b011d1bc21497ca4d1e4c69de`
  - Expected SHA-256: same
  - Boundary: exact repository claims are limited to named Lean declarations; the upper workflow, memory, Mind, Body–Mind, and agent structures are not proved reusable results (`## Scope and evidence boundary`, lines 3–7).

No repository file was written.

### Boundary laws

1. **Declared structure does not collapse into implementation or observation.** A consumer must be able to distinguish what a schema declares, how a concrete adapter realizes or transports it, and what behavior was actually observed. One shared prose field or status cannot stand for all three. Source: `schema-based-learning-crosswalk.md` → `### 1. A three-boundary pressure test`, lines 48–56; `findings.md` → `## Candidate 1 — three-boundary schema contract`, lines 18–34.
2. **Schema compatibility does not entail instance fidelity.** A compositional schema transport law can hold while an instance round trip loses information. Fidelity therefore needs its own visible result and evidence. Source: `findings.md` → `Candidate 1 / Smallest witness`, lines 24–30, selectors `SchemaInstance.pullback_comp` and `Bicyclic.lanUnit_app_not_mono_bicyclic`.
3. **Read capability does not entail update dynamics.** An existing schema-indexed read seam does not establish a nonidentity write, persistence behavior, conflict policy, or read-after-write law. Source: `findings.md` → `## Candidate 2 — schema-indexed memory interface`, lines 36–52, selectors `KnowledgeAsFunctor.Knowledge.read` and `KnowledgeAsFunctor.Knowledge.total_read`.
4. **Stored memory is not active capability.** Inventory, memory, and evidence remain passive sources until a distinct capability interprets or mutates them through named operations and observable execution. Source: `schema-based-learning-crosswalk.md` → `## Crosswalk`, rows `Memory` and `Cognitive modules`, lines 42–43; `### 2. A stricter memory/cognition separation`, lines 58–62.
5. **Workflow specification is not execution.** A declarative route or workflow can be displayed without implying that a runtime interpreted it, that a run occurred, or that effects succeeded. Source: `schema-based-learning-crosswalk.md` → `### 3. Workflow specification versus execution`, lines 64–68.
6. **A static view cannot imply learning.** A source, relation, or visual rearrangement supplies no evidence of update dynamics, adaptation, or learning. A learning state requires a witnessed state transition and named consumer-visible law; neither inspected source provides that witness. Source: `findings.md` → `Candidate 2 / Smallest witness` and `Dissent`, lines 44–52; `## FINAL AUDITED VERDICT`, rows C1–C2 and typed negatives, lines 76–82.

### Candidate mapping table

“White Tower object” below names only the requested conceptual UI object class. No matching implementation selector was inspected or is claimed.

| Exact source selector | White Tower object | Precondition | Consumer-visible law | Collapse test | Disposition |
|---|---|---|---|---|---|
| `schema-based-learning-crosswalk.md` → `### 1. A three-boundary pressure test`, numbered items 1–3, lines 48–56; `findings.md` → final-verdict row `C1`, line 78 | **Tower** — three-boundary overview | A named schema-bearing adapter exists, with separately retrievable declaration, implementation binding, and observed evidence | The tower exposes three independently sourced states: **declared**, **implemented**, and **observed**. None inherits another’s status | If the three regions repeat one description, share one undifferentiated status, or cannot change/reject a real adapter for a named consumer, the tower adds documentation only | **EXPERIMENT** — admit only with a named adapter, typed fields, and consumer |
| `findings.md` → selectors `SchemaInstance.pullback_comp` and `Bicyclic.lanUnit_app_not_mono_bicyclic`, lines 24–30; selector `KnowledgeAsFunctor.Knowledge.read`, lines 42–48 | **Floor** — schema, fidelity, and dynamics ledger | A floor represents one schema choice or adapter boundary | It renders schema transport, instance fidelity, and update support as separate results. “Schema-compatible” must coexist with “fidelity failed/unknown” or “write unavailable” | If schema success automatically paints fidelity or update as successful, the floor destroys the counterexample boundary; if update is only identity/precomposition, the dynamics field is vacuous | **EXPERIMENT** — useful only if independent evidence can populate each result |
| `schema-based-learning-crosswalk.md` → `### 3. Workflow specification versus execution`, lines 64–68; `## Discovery`, lines 24–30 | **Scene** — one workflow/run projection | A concrete runtime binding or run identity is available separately from the workflow specification | The scene may show a workflow as specified before execution; only run-bound observation changes execution/effect state | If no run identity or execution evidence distinguishes the scene from the static workflow, it must remain “specified / not observed” | **KEEP** — retain as an interface invariant, not as proof of current deployment |
| `schema-based-learning-crosswalk.md` → `## Crosswalk`, row `Memory`, line 42; `### 2. A stricter memory/cognition separation`, lines 58–62 | **Source** — passive memory/evidence object | The object represents inventory, session memory, ontology evidence, or another stored read model | The source exposes provenance and readable content but no intrinsic “acts,” “learns,” or “mutates” state. Action belongs to a separately bound capability | If selecting or rendering the source alone is presented as execution, mutation, or learning, memory and capability have collapsed | **KEEP** — strong negative boundary |
| `findings.md` → `## Candidate 2 — schema-indexed memory interface`, selectors `Knowledge.read`, `Knowledge.total_read`, and absent `write`, lines 38–52; final-verdict row `C2`, line 79 | **Relation** — typed read/write relation | A named consumer and one nonidentity write operation are supplied | Read and write are different directed relations; the UI states which operation occurred and which law, if any, relates them | If write is identity/precomposition, or no consumer can distinguish it from read, the relation adds zero structure | **EXPERIMENT** — blocked from KEEP until a nonidentity write and consumer law exist |
| `schema-based-learning-crosswalk.md` → `## Crosswalk`, row `Cognitive modules`, line 43; `### 2. A stricter memory/cognition separation`, lines 58–62 | **Interaction** — capability invocation from a source | A separately identified capability has typed input/output, success conditions, and observable execution | The interaction visibly crosses from passive source to active capability; source provenance remains distinct from invocation status and effect evidence | If the source card itself owns the action semantics, or invocation has no observable result, the interface only relabels memory as capability | **EXPERIMENT** — requires one real capability/consumer witness |
| `schema-based-learning-crosswalk.md` → `### 3. Workflow specification versus execution`, lines 64–68; `findings.md` → `## Candidate 3 — duoidal workflow identification`, lines 54–70, and final-verdict row `C3`, line 80 | **Interaction** — execute a workflow specification | A runtime explicitly binds a selected specification and creates a run-local observation surface | Editing/selecting the specification does not mark it executed; execution may independently be pending, running, failed, or observed | If the interaction merely imports two-product, interchange, `Mind`, or categorical labels without their missing witnesses, it contributes no consumer behavior | **KEEP** the specification/execution split; **REJECT** the categorical identification |
| `schema-based-learning-crosswalk.md` → `## Crosswalk`, row `Mind / Body / agent / world`, line 44; `findings.md` → layer row `Body/agent/world`, line 16 | **Tower** — categorical Mind/Body hierarchy | Would require application-specific typed `Mind`, `Body`, agent, world, and coupling witnesses | No consumer-visible law is presently available | All required application-specific structures are absent; a hierarchy would be decorative ontology presented as implementation | **REJECT** |
| `findings.md` → final-verdict row `C2` and `Typed negatives and collapse-tests`, lines 79–82 | **Scene/Source** — static learning visualization | Would require a nonidentity state update, before/after evidence, and a named consumer law | A static projection remains a view; it cannot acquire a “learned,” “adapted,” or “updated” state from arrangement or rereading alone | If the only witness is `Knowledge.read`, `total_read`, a refreshed render, or identity/precomposition, the learning claim is vacuous | **REJECT** |

### Vocabulary constraints

- Use plain UI terms such as **declaration**, **implementation binding**, **observation**, **schema transport**, **instance fidelity**, **read**, **write**, **workflow specification**, **execution**, and **evidence**.
- Do not label White Tower objects as the paper’s free multicategory, implementation fibre, total category, memory category, `Mind`, `Body`, agent/world hierarchy, or cognitive module.
- Do not import duoidal, interchange, or action vocabulary into consumer-facing contracts.
- Do not use “learning,” “adaptation,” or “update” for a static view, read operation, rerender, or identity transformation.
- A `KEEP` disposition preserves a boundary invariant only. It does not assert that the corresponding White Tower UI contract is implemented, validated, promoted, or deployed.

### Rejections

- Reject a single “schema valid” status that silently covers implementation availability, instance fidelity, and observed semantics.
- Reject inference of lossless instance behavior from compositional schema transport.
- Reject a write/update affordance backed only by read, identity, or precomposition.
- Reject active-capability controls on passive memory/source objects unless a distinct executable capability is bound.
- Reject marking a workflow executed merely because its specification exists or is selected.
- Reject a categorical Mind/Body tower, duoidal workflow representation, or categorical cognitive-module label under the current evidence.
- Reject any learning badge or animation whose only evidence is a static projection or reread.

### Open gaps

- The permitted corpus contains no White Tower implementation, object schema, current UI selector, named adapter, or named end consumer. Consequently, these are source-grounded contract tests, not findings about deployed UI behavior.
- No typed adapter currently changes or rejects behavior under the three-boundary contract.
- No nonidentity write, update law, conflict rule, persistence rule, or read-after-write witness is supplied.
- No run-binding or receipt schema was available to establish how a scene should prove execution.
- No application-specific workflow hierarchy, second product, typed action, `Mind`, `Body`, or agent/world witness exists.
- Promotion from `EXPERIMENT` to `KEEP` requires a real named consumer, independently observable states, and a collapse test that rejects at least one concrete mapping.

## Agent 3 - Implemented interface applicability audit

```text
RECEIPT
action_id: spawn-0003
dispatch_id: 2026-08-09-cyberalchemy-naturalized-interface-design
run_id: run-001
wave_id: w1-explorers
role: explorer-interface
agent_name: Alexander, Christopher
status: pass
validation: pass (pinned-byte and selector audit only; no new browser run)
blockers: none; direct-source content was intentionally out of this read-only packet scope
```

### Source/version verification

- `projects/ide-extension/public/demo/research-tower.html` SHA-256 is `13cf08281195dafdc3b8ad5a53a0b7963da63d5ef2ab61b60c5a4e133017659f`, matching `strategy-inventory-packet.json` (`source_preflight.white_tower_consumer.html`, lines 83–87).
- `projects/cyberalchemy-lab/development/goal-runs/20260809T200945Z-white-tower-view/EXECUTION-RECEIPT.md` SHA-256 is `10e2bfc172e652fa6a2fcf3ccd2df303ecfd592214d2e7fe213adbea8499aae2`, matching the packet (lines 88–93).
- The current evidence ceiling is candidate-local synthetic interface evidence only: automated structure/interaction is supported; human comprehension, screen-reader conformance, literal zoom, real data, authority, publication, deployment, release, and production are not proved (`strategy-inventory-packet.json:92-94`; `EXECUTION-RECEIPT.md:100-113`).
- The direct schema-learning source is only bound as candidate architecture discovery; the naturalized-environment package’s key synthesis is marked “rejected-after-loop-2 working synthesis” (`strategy-inventory-packet.json:33-81`). Neither status licenses a visual/cognitive-benefit claim.
- The usable local design precedents are: distinct semantic/learner/navigation views (`.arcanum/inventory/entries/interactive-ontology-learning-map-strategy-result-synthesis.md:81-104`); a non-executing learner loop (`learning-graph-next-route-guide-research-strategy-result-synthesis.md:73-85`); and selection/focus/state continuity requirements (`ui-prototyping-studio-interface-rework-review-result-synthesis.md:69-99`).

### Current task/selector map

| User job | Current mechanism | Exact selector/citation | Current boundary |
|---|---|---|---|
| Orient to evidence progression | Three ordered, selectable floors and a live selected-state announcement | `#lab-canvas [data-list="levels"]`; generated `[data-scene-id]`; `#selection-status` (`research-tower.html:428,433,651-690`) | Orienting is tied to one synthetic fixture, not corpus coverage. |
| Choose a floor | Floor button sets pressed state and bound detail fields | `[data-scene-id]`, `#evidence-detail`, `[data-panel="scene-ceiling"]` (`research-tower.html:616-632,657-686`) | It exposes evidence/implementation status and blocker, but does not formulate the next evidence question. |
| Inspect source/candidate | Source buttons show locator/digest; candidate button shows status, meaning, ceiling, contradiction path and revision | `[data-list="sources"]`, `[data-action="show-candidate"]`, `#source-detail` (`research-tower.html:447-453,559-582,725-742`) | Source and candidate are inspectable, but their different planes are implicit. |
| Inspect relations | Filtered relation table and count | `[data-field="relation-filter"]`, `[data-list="relations"]`, `#relation-count` (`research-tower.html:456-463,584-599`) | It shows paths, not a claim/authority interpretation. |
| Understand claim ceilings | Per-floor fact list and persistent footer ceiling | `[data-panel="scene-ceiling"]`, `[data-panel="claim-ceiling"]` (`research-tower.html:437-444,601-614,721`) | Ceiling is visible; its relation to a next admissible question is not. |
| Distinguish unavailable System capability | Separate reference section; five controls replace detail with a refusal explanation | `[data-panel="system-atlas"]`, `[data-system-level-id]` (`research-tower.html:474-479,634-648,692-710`) | It correctly promises no execution, scoring, verdict, promotion, or authority effect. Selecting it currently clears visible floor selection. |

### Ranked experiment table

| Rank | Current selector | Proposed change | Source rationale | Observable browser witness | Human-study residue | Accessibility risk | No-effect/regression counterexample |
|---:|---|---|---|---|---|---|---|
| 1 | `#evidence-detail`, `#selection-status`, `[data-panel="residue-detail"]` | Add a compact, display-only **evidence-gap card** after floor detail: “what is known,” “what remains unbound,” “verification question,” and a clearly labeled candidate owner-route string. It must be separate from floor/source/candidate semantics and must never be an execution control. | The learner loop is `orient → focus → inspect → identify evidence gap → revise question → suggest non-executing owner route` (`learning-graph...md:73-85`); its route display does not dispatch or execute (`:95-102`). | Select each `[data-scene-id]`; assert one bound gap card changes with the selected floor, exposes no action endpoint, and preserves source/candidate/relation inspection. Network witness remains GET-only. | Test whether participants can state the missing evidence and distinguish a candidate route from a command. No comprehension claim until studied. | The card must have a stable heading, normal DOM order, explicit state text, and must not add a second noisy live region. | A generic “Next step” button that looks executable, or a static motivational hint identical across floors, neither establishes gap recognition nor preserves the no-execution ceiling. |
| 2 | `[data-list="sources"]`, `[data-action="show-candidate"]`, `[data-list="relations"]` | Make the inspection surface explicitly plane-labeled: **source snapshot**, **candidate meaning**, **relation record**, **claim/proof ceiling**, and **navigation aid**. Add exact locator/digest to source inspection and maintain candidate contradiction/residue as distinct evidence. | The accepted architecture separates source, semantic, epistemic, governance, Craft, and learner planes; learner/navigation removal must not change semantic bytes (`interactive-ontology...md:86-104`). | Candidate/source/relation toggles expose their plane label and immutable binding. A DOM test confirms removing an optional navigation cue changes neither displayed source digest nor candidate ceiling. | Test whether people stop treating “candidate” as an admitted semantic fact or a governance decision. | Repeated plane labels can become verbose; use concise visible labels and one complete accessible name rather than duplicated announcements. | Recoloring panels “blue for source / gold for candidate” without text or stable labels hides meaning from non-visual users and does not prove a comprehension benefit. |
| 3 | `.tower-shell`, `[data-list="levels"]`, `#evidence-detail` | Add a small, persistent **investigation-path landmark**: “1 Orient in the evidence floors → 2 Inspect source/candidate/relations → 3 Read ceiling and residue.” It is a task map, not a new semantic graph or decorative tower layer. | The current view already implements the first three learner-loop actions but not their explicit connection (`research-tower.html:419-468`); the route-guide precedent supports a learner-facing projection over separately owned records (`learning-graph...md:75-85`). | At desktop and 320px, tabbing from a selected floor reaches the named task map and its target links/anchors in order; floor selection and `aria-labelledby` still update the detail panel. | Compare ability to start the requested inspection task, time to locate claim ceiling, and erroneous System-capability expectations. | Anchor targets must preserve visible focus and not create focus traps; link wording cannot imply the user has “completed” an evidence stage. | A large illustrated tower, ambient progress animation, or reordered cards with no task-specific target/selection witness is decoration, not an interface experiment. |
| 4 | `[data-system-level-id]`, `#evidence-detail`, `[data-scene-id]` | Preserve the prior evidence-floor context while a System reference is open: show “Reference opened from Evidence floor N,” retain the floor’s selected/inspectable context, and provide a visible “Return to floor detail” control. Keep System content marked unavailable and non-executing. | The continuity review found loss of selected target/focus a critical defect class (`ui-prototyping...md:75-85`) and recommends a stable shell with a persistent action spine (`:87-99`). Current code clears floor pressed state when System is selected (`research-tower.html:634-648`). | Floor → source/candidate → System reference → return: assert the same floor, source/candidate selection, relation filter, and focus restoration; assert System still has `Unavailable in this Lab` and no non-GET request. | Test whether users can correctly report that the System reference did not act on the tower and can resume their prior investigation. | Two simultaneous “selected” states require explicit labels; otherwise screen-reader users may not know whether context or reference is active. | Simply moving System controls above the floor selection, or changing dashed amber borders, risks collapsing unavailable reference into active workflow and loses continuity. |
| 5 | `[data-panel="witness-binding"]`, `[data-panel="claim-ceiling"]`, `.bottomline` | Keep a concise **fixture/provenance strip** visible with the active detail: validation-record ID, “synthetic fixture only,” and the specific unsupported inference (for example, “not representative-source selection”). Do not add environmental ambiance. | Exact immutable bindings are a required load-bearing constraint (`learning-graph...md:124-132`); the current header already says fixture validation does not establish representativeness (`research-tower.html:713-721`). | Changing floor/source/candidate updates no provenance identity incorrectly; a viewport/scroll witness confirms the ceiling remains reachable without losing selection. | Test whether people accurately distinguish “validated bytes” from “validated research conclusion.” | Avoid sticky overlays that conceal content at zoom/reflow; the strip must wrap in normal flow. | A warmer palette, paper texture, “natural” illustrations, or claims of calm/attention with unchanged provenance and task behavior have no valid cognitive witness. |

### Accessibility and continuity constraints

- Preserve the existing native controls, 44px minimum controls, visible `:focus-visible`, `aria-pressed`, `aria-controls`, one atomic polite status region, and reduced-motion parity (`research-tower.html:45-49,112-125,389-396,657-686`; `EXECUTION-RECEIPT.md:55-61,74-77`).
- New task-map or gap content must be normal-flow and available at 320px. The receipt only proves CSS-viewport reflow, not literal 200%/400% browser zoom (`EXECUTION-RECEIPT.md:104-106`).
- Treat active evidence context and an opened System reference as two explicitly named states. Do not remove current source/candidate/filter state without an intentional reset and a focus witness.
- Do not add a second live region merely to narrate learner progress. The current contract has exactly one `aria-live`, `role=status`, polite, atomic region (`EXECUTION-RECEIPT.md:74-75`).
- Automated ARIA/focus evidence is not screen-reader conformance; a real assistive-technology matrix remains open (`EXECUTION-RECEIPT.md:102-107`).

### No-effect/regression counterexamples

- A naturalized visual treatment with the same floor/source/candidate/System behavior changes atmosphere, not the evidence task. The packet explicitly separates task-relevant structure from ambient character and prohibits cognitive-benefit claims for the latter (`strategy-inventory-packet.json:182`).
- Replacing explicit source digest, candidate status, or claim ceiling with a cleaner visual summary hides provenance and weakens the current evidence boundary.
- Treating a relation row as an admitted semantic relation, or a candidate card as an authority decision, collapses the distinct planes prohibited by the interactive ontology map (`interactive-ontology...md:96-104`).
- Making a suggested owner route clickable-to-execute violates the route guide’s explicit non-executing boundary (`learning-graph...md:95-102`).
- Clearing selection/focus when opening a System reference repeats the verified continuity defect class even if all layout screenshots look better (`ui-prototyping...md:75-85`).

### Rejected decoration

Reject proposals whose only change is a warmer/natural palette, photographic or organic background, scenic tower silhouette, motion, “calm/focus” copy, or decorative graph geometry. The naturalized-environment binding is a rejected working synthesis, and no human comprehension, usability, delight, or cognitive outcome has been studied. The current implementation deliberately rejected scenic/photographic/orbit/robot surfaces (`EXECUTION-RECEIPT.md:55-57,74`).

### Open gaps

- No direct content finding from either external-source binding was read under this action’s frozen packet-only scope; their metadata is not a substitute for source-grounded design claims.
- No human study demonstrates comprehension, trust, workload, delight, task success, or any naturalized-environment effect (`strategy-inventory-packet.json:178-182`; `ui-prototyping...md:120-125`).
- No screen-reader/browser matrix or literal browser-zoom evidence exists.
- Representative source selection, real tower data, real System capability, ontology admission, promotion, publication, deployment, release, and production remain outside this interface experiment.
