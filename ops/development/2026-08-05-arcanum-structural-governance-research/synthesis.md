# Candidate structural model

Status: synthesis evidence for adversarial review. It is not canonical authority, promotion, publication, deployment, release, or production proof.

## 1. Plain-language stack

| Claim | Layer | Plain-language role | Owner / authority | Exact binding | Explorer | Scope / class / proof |
|---|---|---|---|---|---|---|
| SG-STACK-01 | Definition | Says what a public Arcanum term means. | Canonical definitions own meaning; Definitions Governance maintains them. | `arcanum/definitions/DEFINITIONS.md#authority-rule`; `arcanum/arcana/definitions-governance/SKILL.md:40-63,66-109` | lifecycle, constitution | Public Arcanum; observed |
| SG-STACK-02 | Constitution | States durable, scoped rules about artifact structure, form, or behavior. | Each constitution owns rules in its scope; Constitution Governance owns selection, composition, lifecycle, and promotion preparation. | `arcanum/arcana/constitution-governance/SKILL.md#objective`, `#process`, `#composition-rules`, `#validation-model` | constitution, lifecycle | Public Arcanum; observed |
| SG-STACK-03 | Discipline | Names a recurring cross-capability way of working and routes it to the smallest hardening owner. | Discipline card/catalog own description and maturity status; Discipline Governance owns that lifecycle. | `arcanum/disciplines/README.md#boundary`; `arcanum/arcana/discipline-governance/SKILL.md#chain-boundary`, `#routing-model`, `#process` | discipline, lifecycle | Public Arcanum; observed |
| SG-STACK-04 | Sigil | Owns one reusable executable capability contract. | Canonical `<formulae\|transmutations\|arcana>/<id>/SKILL.md`; Sigil Development owns lifecycle readiness. | `arcanum/arcana/sigil-development/SKILL.md:55-73,97-160,207-220` | lifecycle | Public Arcanum; observed |
| SG-STACK-05 | Spell | Owns composition among capabilities, without redefining constituent sigils. | `arcanum/spells/<id>/README.md`; Spellcraft owns lifecycle readiness. | `arcanum/spells/README.md:39-61`; `arcanum/arcana/spellcraft/SKILL.md:92-163,181-194` | lifecycle | Public Arcanum; observed |
| SG-STACK-06 | Schema / validator | Describes instance shape and checks bounded declared rules. | Rule owner supplies authority; validator supplies enforcement evidence only. | `arcanum/definitions/DEFINITIONS.md#def-arc-schema-schema`; `arcanum/arcana/constitution-governance/SKILL.md#validation-model` | all three | Public Arcanum; observed, with bounded checks executed |
| SG-STACK-07 | Lifecycle / promotion | Decides how evidence may alter canonical source. | Artifact-specific lifecycle owner; cross-artifact protocol frames the smallest reviewed patch. | `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md#process`; artifact lifecycle bindings above | constitution, lifecycle | Public Arcanum; observed prose/process contract |
| SG-STACK-08 | Projection / runtime | Makes an accepted canonical contract discoverable and executable. | Registries, generated packages, installers, and runtime are downstream projections. | `arcanum/README.md:171-177`; `arcanum/tools/build-skill-registry.py:2-10,323-345,411-413`; `arcanum/tools/sync-generated-skill-package.sh:106-229` | lifecycle | Public source plus generated runtime; observed |
| SG-STACK-09 | Evidence / coordination | Shows what happened, was tested, or is planned. | Task Session, Craft, experiments, telemetry, receipts, Inventory, and ontology do not inherit semantic or promotion authority. | `arcanum/arcana/task-session/SKILL.md:295-302,418-420`; `arcanum/formulae/dispatch-spec/SKILL.md:75-86`; `arcanum/arcana/workflow-reflect/SKILL.md:61-129` | lifecycle | Public Arcanum and repository-local read models; observed |
| SG-STACK-10 | Private comparison | Shows that other governed stacks can use axioms and private constitution namespaces. | Their private owners only. | `implementation/domainspec/AXIOMS.md#axiom-a1-semantic-authority-precedes-implementation`; `implementation/domainspec/CONSTITUTION.md#rule-catalog`; `cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md#candidate-kinds` | constitution | Private comparator; observed; not public doctrine |

## 2. Controlled vocabulary and non-collapse rules

| Claim | Term | Keep distinct from | Non-collapse rule | Exact binding | Explorer | Scope / class / proof |
|---|---|---|---|---|---|---|
| SG-VOC-01 | Axiom | Constitution | An axiom supplies a foundational premise; public Arcanum does not currently require an axiom-to-constitution derivation. | Private comparator: `implementation/domainspec/AXIOMS.md#axiom-a1-semantic-authority-precedes-implementation` through A6; public absence reported against `arcanum/definitions/DEFINITIONS.md` | constitution | Private comparison plus public gap; observed |
| SG-VOC-02 | Definition | Constitution / discipline | A definition owns stable meaning; other artifacts use it and must not silently redefine it. | `arcanum/definitions/DEFINITIONS.md#authority-rule` | constitution, lifecycle | Public; observed |
| SG-VOC-03 | Constitution | Policy / schema / discipline | A constitution is durable, scoped, rule-shaped, selection-aware, authority-bounded, and validation-linked; mere preference, shape, or practice is insufficient. | `arcanum/arcana/constitution-governance/SKILL.md#objective`, `#applicability`, `#non-applicability`, `#anti-patterns` | constitution | Public; observed |
| SG-VOC-04 | Discipline | Capability | A discipline describes recurring practice and routing; it does not execute the capability it references. | `arcanum/disciplines/README.md#boundary`; `discipline-governance/SKILL.md#chain-boundary` | discipline | Public; observed |
| SG-VOC-05 | Method / process | Law / execution | A method explains how work proceeds; it neither creates constitutional force nor proves execution. | `discipline-governance/SKILL.md#routing-model`; `DEVELOPMENT-TO-CANONICAL-PROMOTION.md#process` | discipline, lifecycle | Public; observed |
| SG-VOC-06 | Schema | Semantic authority | Schema checks structural form; it cannot establish meaning, owner legitimacy, execution, or promotion. | `arcanum/definitions/DEFINITIONS.md#def-arc-schema-schema`, especially `#boundary` | constitution | Public; observed |
| SG-VOC-07 | Validator | Rule owner | A validator detects a bounded condition; passing it does not create or promote the rule. | `constitution-governance/SKILL.md#validation-model`; `ARTIFACT-CONSTITUTION.md#promotion-boundary-rules` | all three | Public; observed and partly executed |
| SG-VOC-08 | Registry / generated package | Canonical source | Registry presence means discoverability; generated packages are non-canonical projections. | `arcanum/README.md:171-177`; generated package headers; `sync-generated-skill-package.sh:106-229` | lifecycle, constitution | Public/generated; observed |
| SG-VOC-09 | Receipt / telemetry / Inventory / ontology / Craft | Authority | These are evidence, read models, or coordination state; none can promote canonical source. | `dispatch-spec/SKILL.md:75-86`; `task-session/SKILL.md:295-302,418-420`; `workflow-reflect/SKILL.md:61-129` | lifecycle | Public/repository-local; observed |
| SG-VOC-10 | Validation | Promotion | Validation is necessary where declared, but promotion remains an owner decision and may be review-bound. | `DEVELOPMENT-TO-CANONICAL-PROMOTION.md:28-84`; `constitution-governance/SKILL.md#validation-model` | constitution, lifecycle | Public; observed |
| SG-VOC-11 | Installation | Lifecycle closure | Installing a projection makes it runnable; it does not prove semantic parity, acceptance, or promotion. | `bootstrap_arcanum.sh`; `install_arcanum.sh`; generated package headers | lifecycle | Public/generated; observed |

Public vocabulary gap: neither `constitution` nor `axiom` has a formal public definition ID. Their current meaning is operationally described, not definition-governed.

## 3. Constitution and axiom catalog

| Claim | Artifact / namespace | Status and role | Exact binding | Explorer | Scope / class / proof |
|---|---|---|---|---|---|
| SG-CON-01 | Constitution Governance | Canonical sigil `0.1.0`; lifecycle/process owner. | `arcanum/arcana/constitution-governance/SKILL.md#objective`, `#modes`, `#process` | constitution, lifecycle | Public; observed |
| SG-CON-02 | Constitution templates | Candidate common constitution shape, composition pack, and validation-adapter plan. Composition pack is explicitly non-canonical. | `templates/constitution.md`; `templates/composition-pack.md#handoff`; `templates/validation-adapter.md` | constitution | Public candidate/template; observed |
| SG-CON-03 | Artifact Constitution | Governs artifact classes and promotion boundary; its own top-level status/owner metadata is absent. | `arcanum/framework/ARTIFACT-CONSTITUTION.md#classes`, `#promotion-boundary-rules` | constitution | Public; observed; validator executed and full run failed |
| SG-CON-04 | Schema Constitution | Declared canonical; owns `.yml` schema format and prose boundary. | `arcanum/framework/SCHEMA-CONSTITUTION.md#rules`, rules `schema.format.yml`, `schema.format.prose-boundary`, `schema.format.legacy-migration` | constitution | Public canonical; observed; validator executed |
| SG-CON-05 | Artifact Metadata Constitution | Candidate metadata, selectors, and profiles; end-to-end selection remains future. | `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md#composition`, `#validation`, `#promotion-boundary` | constitution | Public candidate; parser self-test executed |
| SG-CON-06 | Gitignore Constitution | Candidate review rules without deterministic validator. | `arcanum/framework/GITIGNORE-CONSTITUTION.md#validation` | constitution | Public candidate; observed; prose review only |
| SG-CON-07 | Markdown Linking Constitution | Candidate linking/citation rules; local link/anchor subset is executable. | `arcanum/framework/MARKDOWN-LINKING-CONSTITUTION.md`; `tools/check_markdown_links.sh` | constitution | Public candidate; bounded checker executed |
| SG-CON-08 | Receipt ID Legend Constitution | Candidate receipt rules; only `gloss-on-cite` fixture coverage was witnessed. | `arcanum/framework/RECEIPT-ID-LEGEND-CONSTITUTION.md#validation`; `tools/validate-receipt-legend.py` | constitution | Public candidate; bounded self-test executed |
| SG-CON-09 | Development-to-Canonical Promotion | Active cross-artifact process, not an independent authority-transfer engine. | `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md#process` | constitution, lifecycle | Public active process; observed |
| SG-CON-10 | Public axiom catalog | None found. | Absence reported after inspection of public definitions and constitution-governance surfaces | constitution | Public; unimplemented/unverified-as-universal-absence |
| SG-CON-11 | DomainSpec axioms / constitution | Private `A1–A6 → C1–C11 → gates` comparison chain. | `implementation/domainspec/AXIOMS.md`; `implementation/domainspec/CONSTITUTION.md#rule-catalog`, `#derivation-chain-l4---l3---l6` | constitution | Private comparator; observed; not public Arcanum authority |
| SG-CON-12 | CyberAlchemy v2 constitutions | Private candidate authority namespace; preserves imported conflicts and promotion boundaries. | `cyberAlchemy-v2/authority/constitutions/CONSTITUTION-IMPORT-PACK.md#precedence`, `#conflicts-preserved`; `STABLE-REPOSITORY-CONSTITUTION.md#validation-adapters`, `#promotion-boundary` | constitution | Private comparator; observed; not public Arcanum authority |

Six public framework constitutions were found. There is no distinct constitution catalog beyond filesystem/registry discovery.

## 4. Discipline, method, and recurring-practice catalog

| Claim | Status | Count / members | Exact binding | Explorer | Scope / class / proof |
|---|---|---|---|---|---|
| SG-DIS-01 | canonical | 4: `schema`, `artifact-constitution`, `quality-bar`, `validation-experiment` | `arcanum/disciplines/DISCIPLINES.md#catalog` | discipline | Public catalog; observed; syntactic validation executed |
| SG-DIS-02 | implemented | 1: `observability` | Same catalog selector | discipline | Public catalog; observed; syntactic validation executed |
| SG-DIS-03 | active-pattern | 11: `planning`, `dispatch`, `context-selection`, `evidence-inventory`, `definition-governance`, `decision-gating`, `interview`, `research-evidence`, `runtime-boundary`, `development-package-promotion-gate`, `two-lane-dialectic` | Same catalog selector | discipline | Public catalog; observed; recurrence/evidence status not machine-proven |
| SG-DIS-04 | candidate | 8: `craft`, `ontology`, `residuality`, `distillation`, `ux-evidence`, `gitignore`, `receipt-id-legend`, `two-lane-representation` | Same catalog selector | discipline | Public catalog; observed |
| SG-DIS-05 | deprecated | 1: `implementation-readiness` → `planning` | `DISCIPLINES.md#catalog`; `cards/implementation-readiness.md#purpose`; `CURATION-RUN-2026-06-21.md#part-b-validate--deprecate-curation-over-arcanums-22` | discipline | Public plus historical evidence; observed, not newly executed |
| SG-DIS-06 | Card shape | All 25 IDs were manually observed to have cards; cards carry purpose, non-owner boundary, evidence, validation, quality bar, and promotion guardrail. | `arcanum/disciplines/templates/discipline-card.md#discipline-name`; `disciplines/cards/` | discipline | Public; manual observation; parity not validator-proven |
| SG-DIS-07 | Candidate schema | Defines a future machine-readable discipline object but is not consumed by the live catalog validator. | `arcanum/disciplines/discipline.schema.yml#description`; `scripts/validate-discipline-catalog.py#main` | discipline, lifecycle | Public candidate; observed |
| SG-DIS-08 | Quality-bar qualification | Catalog says canonical, but direct backing is owner prose without the explicit constitution status/owner/validator shape seen in Schema Constitution. | `cards/quality-bar.md`; `framework/QUALITY-BAR.md` | discipline | Public; observed; canonical backing needs tighter binding |

## 5. Owner, authority, and dependency matrix

| Claim | Object | Semantic owner | Lifecycle/change owner | Depends on / projects to | Exact binding | Explorer | Scope / proof |
|---|---|---|---|---|---|---|---|
| SG-OWN-01 | Definition | `DEFINITIONS.md` | Definitions Governance | Consumers reference IDs | `definitions-governance/SKILL.md:40-109` | lifecycle | Public; observed |
| SG-OWN-02 | Constitution rule | Specific constitution | Constitution Governance | Validators, composition packs | `constitution-governance/SKILL.md:68-170` | constitution, lifecycle | Public; observed |
| SG-OWN-03 | Discipline | Card/catalog | Discipline Governance | May hand off to constitution, validator, sigil, or spell owner | `discipline-governance/SKILL.md:65-150` | discipline, lifecycle | Public; observed |
| SG-OWN-04 | Sigil | Canonical `SKILL.md` | Sigil Development | Registry, generated package, installation | `sigil-development/SKILL.md:97-160` | lifecycle | Public; observed |
| SG-OWN-05 | Spell | Canonical spell `README.md` | Spellcraft | Spell registry, generated package, installation | `spells/README.md:39-61`; `spellcraft/SKILL.md:92-194` | lifecycle | Public; observed |
| SG-OWN-06 | Validator | No independent semantic authority | Rule/lifecycle owner governs its intended rule | Produces pass/flag/block evidence | `constitution-governance/SKILL.md#validation-model` | all | Public; observed/executed subset |
| SG-OWN-07 | Dispatch | Dispatch document / user confirmation | Dispatch Spec validates; Orchestrate schedules and joins | Receipts and telemetry | `dispatch-spec/SKILL.md:55-146`; `.agents/skills/orchestrate/SKILL.md:59-143` | lifecycle | Public/generated runtime; observed |
| SG-OWN-08 | Evidence/read model | Its named producer | Separate owner consumes evidence | Inventory, ontology, Craft, telemetry, receipts | `dispatch-spec/SKILL.md:75-86`; `workflow-reflect/SKILL.md:61-129` | lifecycle | Non-authority; observed |
| SG-OWN-09 | Private comparator | DomainSpec / CyberAlchemy v2 owner | Private owner gates | Must not be copied into public Arcanum as doctrine | `cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md#candidate-kinds` | constitution | Private; observed |

## 6. Precedence, composition, conflict, and versioning

| Claim | Rule | Exact binding | Explorer | Scope / class / proof |
|---|---|---|---|---|
| SG-COMP-01 | Select only applicable constitutions; explicit selectors/metadata outrank path heuristics where available. | `constitution-governance/SKILL.md#process`; `ARTIFACT-METADATA-CONSTITUTION.md#composition` | constitution | Public; observed prose |
| SG-COMP-02 | Constitution order is narrowest to broadest: task-specific → artifact type → domain/capability → framework → repository fallback. | `constitution-governance/SKILL.md#composition-rules` | constitution, lifecycle | Public; observed prose |
| SG-COMP-03 | Preserve conflicts; classify as blocker, deferrable, or local override. Consequential precedence/canonicality blockers route to Decision Gate. | Same selector, especially conflict rules; `SKILL.md#process` step 11 | constitution, lifecycle | Public; observed prose |
| SG-COMP-04 | “Newest wins” and “broader wins” are invalid shortcuts. | `constitution-governance/SKILL.md#composition-rules`, `#anti-patterns` | constitution | Public; observed |
| SG-COMP-05 | No deterministic selector registry, composition schema, conflict solver, precedence validator, or version resolver was found. | Compared `constitution-governance` process/templates with current tools | constitution | Public gap; observed search result, no execution claim |
| SG-COMP-06 | Constitution version selection is under-specified: template has status/authority/update time but no version; live metadata shapes differ; `supersedes` is candidate metadata only. | `templates/constitution.md`; framework constitutions; `ARTIFACT-METADATA-CONSTITUTION.md` | constitution | Public; observed |
| SG-COMP-07 | Discipline composition is routing, not rule merging: choose the smallest owner route, then hand off. | `discipline-governance/SKILL.md#routing-model`, `#process` step 5 | discipline | Public; observed prose |
| SG-COMP-08 | Spell composition preserves sigil ownership and cannot redefine constituent contracts. | `spellcraft/SKILL.md:141-163`; `spells/README.md:39-61` | lifecycle | Public; observed |
| SG-COMP-09 | Retirement/deprecation is review-bound: disciplines retain a deprecated row and superseding route; constitutions lack an enforced retirement state machine. | `discipline-governance/SKILL.md#process` step 8; constitution template maintenance fields | constitution, discipline | Public; observed prose/historical example |

## 7. Lifecycle and promotion paths

### Constitution — SG-LIFE-01

Classify reusable structural rule → invoke Constitution Governance (`create`, `add-rule`, `split`, or `promote`) → draft in development → declare scope, owner, selectors, examples, validation mode, adapter, and promotion boundary → compose narrow-to-broad → preserve/escalate conflicts → execute named checks → frame smallest promotion patch → owner review → mutate canonical constitution → synchronize dependent projections.

Binding: `constitution-governance/SKILL.md:68-170`; `DEVELOPMENT-TO-CANONICAL-PROMOTION.md:28-84`.  
Explorer: constitution and lifecycle. Public; observed process, not executed promotion.

### Discipline — SG-LIFE-02

Establish recurring cross-capability evidence → classify `public-safe` or `private-parent` and prefer local-first for consuming-repository practices → create/update card and catalog row as `candidate` → choose catalog/template/validator/constitution/sigil/spell route → run catalog validation plus currently manual semantic review → change status only with owner, evidence, validation surface, and mutation boundary → deprecate by preserving rationale and superseding route → hand off any foreign artifact mutation to its lifecycle owner.

Binding: `discipline-governance/SKILL.md:77-150`; `DISCIPLINES.md#growth-rule`.  
Explorer: discipline and lifecycle. Public; observed process; catalog validator executed.

### Sigil — SG-LIFE-03

Invoke defines/designs/plans and hands off → Sigil Development owns canonical package lifecycle → define contract and experiment regimes → Task Session executes one admitted unit → Experiment Harness tests reusable behavior → Signal Observer records signals → Workflow Reflect proposes changes → Sigil Development reviews → smallest canonical patch → registry update → targeted generation/synchronization → semantic parity verification.

Binding: `sigil-development/SKILL.md:55-94,97-160`; `task-session/SKILL.md:295-302,418-420`; `sync-generated-skill-package.sh:106-229`.  
Explorer: lifecycle. Public; observed, not executed end to end.

### Spell — SG-LIFE-04

Invoke hands off → Spellcraft resolves ID/aliases and owns composition lifecycle → draft canonical composition plus development evidence → declare components, phases, state, gates, handoffs, and failure policy → Task Session executes bounded work → experiments/observation/reflection produce evidence → Spellcraft reviews → smallest canonical patch → spell registry and generated projections synchronize → parity verification.

Binding: `spells/README.md:39-61`; `spellcraft/SKILL.md:45-75,78-194`.  
Explorer: lifecycle. Public; observed, not executed end to end.

Promotion invariant — SG-LIFE-05: classify evidence, resolve exact owner, select smallest durable claim, frame patch, normalize to target voice, run owner gate, validate, synchronize only required projections, and record residue. Validation, registration, generation, installation, or receipt existence alone cannot advance authority.

## 8. Enforcement map

| Claim | Stage | What it establishes | What it does not establish | Exact binding | Explorer | Scope / proof |
|---|---|---|---|---|---|---|
| SG-ENF-01 | Prose rule | Normative intent and owner boundary | Mechanical compliance | Constitution/discipline SKILL and framework documents cited above | all | Public; observed |
| SG-ENF-02 | Schema | Intended structural shape | Semantic truth or lifecycle transition | `DEFINITIONS.md#def-arc-schema-schema`; `discipline.schema.yml:1-73` | constitution, discipline | Public; observed |
| SG-ENF-03 | Validator | Bounded detected conditions | Owner legitimacy, promotion, full semantic coverage | `validate-artifact-constitution.sh`; `validate-discipline-catalog.py:14-80` | all | Public; executed |
| SG-ENF-04 | Receipt/test | Evidence that a named action/check occurred | Canonicality or authority transfer | `dispatch-spec/SKILL.md:75-86`; promotion boundary rules | lifecycle | Public/repository evidence; observed |
| SG-ENF-05 | Registry/catalog | Discoverability and declared status | Canonical semantic ownership or runtime parity | `registry/SIGILS.md`; `registry/SPELLS.md`; `DISCIPLINES.md#catalog` | discipline, lifecycle | Public; observed |
| SG-ENF-06 | Generation | Produces runtime-specific copies with permitted transforms | Semantic parity merely from byte difference or generation success | `build-skill-registry.py`; `sync-generated-skill-package.sh` | lifecycle, constitution | Public/generated; observed |
| SG-ENF-07 | Installation/runtime | Makes a projected capability available for execution | Promotion, acceptance, or production readiness | `bootstrap_arcanum.sh`; `install_arcanum.sh`; generated headers | lifecycle | Public/generated; observed |
| SG-ENF-08 | Observation/reflection | Records behavior and proposes maintenance | Direct mutation of the observed capability | `signal-observer/SKILL.md:65-126`; `workflow-reflect/SKILL.md:61-129` | lifecycle | Public; observed |

Executed proof must retain its disagreement:

- SG-PROOF-01: discipline catalog validation passed with 25 rows. Both discipline and lifecycle explorers agree.
- SG-PROOF-02: bounded self-tests/checks passed for Artifact Constitution, artifact metadata parser, receipt legend, and Markdown local links/anchors, when run from the Arcanum root. Constitution explorer.
- SG-PROOF-03: the full Artifact Constitution validator failed on the current tree. The constitution explorer reported 20 listed new `.schema.json` failures and 241 total warnings (25 displayed plus 216 omitted); the lifecycle explorer reported 19 schema-format failures and 216 additional warnings. This synthesis does not average or silently reconcile those counts. The stable conclusion is only “full validation failed on current source”; exact counts require one frozen rerun.
- SG-PROOF-04: invoking the validator from the parent root produces path-related false failures; its current command contract depends on running from the Arcanum submodule root.
- SG-PROOF-05: raw canonical/generated byte equality is not expected because runtime packages add metadata and may translate tools. It is not a semantic parity test.

## 9. Invoke–Task Session–Craft integration

```text
Invoke
  defines, designs, plans, and emits context-only lifecycle handoff
    ↓
Artifact-specific lifecycle owner
  Constitution Governance | Discipline Governance | Sigil Development | Spellcraft
    ↓
Task Session
  executes exactly one admitted task/SWU; returns bounded evidence
    ↓
Craft, when selected by the route
  tracks/stages approved work-graph deltas; remains coordination state
    ↓
Experiment Harness → Signal Observer → Workflow Reflect
  behavior evidence → signals → proposals
    ↓
Lifecycle owner
  decides whether evidence supports the smallest promotion patch
    ↓
Canonical source
    ↓
registry/catalog → generation → installation/runtime
```

| Claim | Boundary | Exact binding | Explorer | Scope / proof |
|---|---|---|---|---|
| SG-BUILD-01 | Invoke handoff is context, not mutation or lifecycle authority. | `arcanum/spells/invoke/plan.md:83-85`; `handoff.md:60-64` | lifecycle | Public; observed |
| SG-BUILD-02 | Task Session execution cannot acquire promotion authority. | `task-session/SKILL.md:295-302,418-420` | lifecycle | Public; observed |
| SG-BUILD-03 | Craft ledger/projection records coordination state; a delta or receipt cannot promote canonical source. | Build-protocol comparison in lifecycle return, bounded by promotion rule and Dispatch Spec authority exclusions | lifecycle | Repository-local/public boundary; observed, no runtime Craft execution |
| SG-BUILD-04 | Dispatch Spec validates route shape; Orchestrate schedules, joins, gates, and closes; neither becomes artifact owner. | `dispatch-spec/SKILL.md:55-146`; `.agents/skills/orchestrate/SKILL.md:59-143` | lifecycle | Public/generated runtime; observed |
| SG-BUILD-05 | Experiments, signals, and reflection inform the lifecycle owner; they do not bypass it. | `experiment-harness/SKILL.md:53-142`; `signal-observer/SKILL.md:65-126`; `workflow-reflect/SKILL.md:61-129` | lifecycle | Public; observed |

## 10. Finite operator playbooks

### SG-PLAY-01 — Add/change a definition

1. Resolve whether the term is public Arcanum-wide.
2. Route to Definitions Governance.
3. Edit canonical definition and synchronized indexes through that owner.
4. Validate references.
5. Record unresolved aliases or private-only meanings as residue.
6. Stop if another artifact attempts to redefine it.

### SG-PLAY-02 — Add/change a constitution

1. Confirm reusable structural rule.
2. Route to Constitution Governance.
3. Draft exact scope, selectors, owner, rule IDs, examples, validation mode, adapter, and promotion boundary.
4. Compose narrow-to-broad.
5. Preserve conflicts; Decision Gate handles blocker precedence.
6. Run exact validators from their required working directory.
7. Stop on failed required validation.
8. Owner reviews smallest promotion patch.
9. Only after canonical acceptance, synchronize dependent projections.

### SG-PLAY-03 — Add/change a discipline

1. Gather recurrence beyond one capability.
2. Classify public-safe/private-parent; consuming-repository evidence stays local-first.
3. Create/update card and catalog row as candidate.
4. Select smallest hardening owner.
5. Run catalog validator and manually check card/schema, evidence, Growth Rule, and claimed validator until tooling exists.
6. Promote/deprecate only with owner, evidence, validation, mutation boundary, and superseding route.
7. Hand off constitution/sigil/spell mutations separately.

### SG-PLAY-04 — Add/change a sigil

1. Invoke for definition/design/plan.
2. Hand off to Sigil Development.
3. Edit canonical package only.
4. Preserve experiment regimes.
5. Execute bounded SWUs through Task Session.
6. Gather experiment/telemetry/reflection evidence.
7. Lifecycle owner decides smallest patch.
8. Update registry after canonical change.
9. Regenerate targeted runtime packages.
10. Verify semantic, not raw-byte, parity.

### SG-PLAY-05 — Add/change a spell

1. Resolve stable ID and aliases.
2. Hand off to Spellcraft.
3. Define composition without redefining sigils.
4. Specify phases, shared state, gates, handoffs, and failure policy.
5. Execute bounded adaptation/implementation through Task Session.
6. Gather composition evidence.
7. Spellcraft reviews smallest patch.
8. Update registry and projections after canonical acceptance.
9. Verify parity.

### SG-PLAY-06 — Handle conflict or drift

1. Freeze exact source and projection identities.
2. Classify mismatch as permitted transform, stale projection, rule conflict, or validator defect.
3. Preserve all conflicting claims.
4. Route semantic conflict to current owner; blocker precedence to Decision Gate.
5. Run owner-declared validation.
6. Do not repair unrelated dirty-tree failures.
7. Record remaining residue and proof ceiling.

## 11. Drift, duplication, bug, and missing-link map

| Claim | Finding | Impact | Current owner / recommendation | Exact binding | Explorer | Scope / proof |
|---|---|---|---|---|---|---|
| SG-DRIFT-01 | Canonical `discipline-governance` is `0.2.2` with local-first routing; `.agents` and `.claude` projections are `0.2.1`. | Runtime agents can omit the consuming-repository boundary. | Sigil Development / generated-package owner: perform targeted regeneration only after current canonical state and transforms are verified. | `arcanum/arcana/discipline-governance/SKILL.md`; generated counterparts; reproducible `diff -u` | lifecycle | Public/generated; observed |
| SG-DRIFT-02 | Full Artifact Constitution validation currently fails. | Canonical schema-format gate is not green. | Artifact/Schema Constitution owners: freeze tree and rerun from `arcanum/`; classify each failure before repair. | `tools/validate-artifact-constitution.sh`; `SCHEMA-CONSTITUTION.md#rules` | constitution, lifecycle | Public; executed fail; count disagreement preserved |
| SG-DRIFT-03 | Validator working-directory sensitivity. | Parent-root invocation produces misleading missing-path failures. | Tool owner: document or enforce repository root. | `tools/validate-artifact-constitution.sh` observed invocation behavior | constitution, lifecycle | Public; executed |
| SG-DRIFT-04 | Discipline schema is not consumed by catalog validator. | Card semantics, required fields, and `additionalProperties` are not enforced. | Discipline Governance: either add an owner-approved card parser/validator or narrow prose claims. | `discipline.schema.yml`; `validate-discipline-catalog.py#main` | discipline, lifecycle | Public; observed |
| SG-DRIFT-05 | Growth Rule and active-pattern cross-capability test are prose-only. | Status may be syntactically valid without required evidence. | Discipline Governance: create deterministic checks where representable; retain review-bound remainder explicitly. | `DISCIPLINES.md#growth-rule`; `discipline-governance/SKILL.md#validation-model` | discipline | Public; observed |
| SG-DRIFT-06 | Artifact metadata example claims Schema Constitution metadata that live source lacks. | Example misrepresents current adoption. | Constitution Governance / metadata constitution owner: repair example or adopt metadata through a separate reviewed change. | `ARTIFACT-METADATA-CONSTITUTION.md#examples`; live `SCHEMA-CONSTITUTION.md` header | constitution | Public; observed |
| SG-DRIFT-07 | Artifact Constitution lacks its own explicit status/date/owner/ID/version. | Governing artifact’s authority metadata is ambiguous. | Constitution Governance: decide and record through owner gate, not silent cleanup. | `ARTIFACT-CONSTITUTION.md` top level; constitution template | constitution | Public; observed |
| SG-DRIFT-08 | Framework constitutions diverge from the candidate template. | Selection/composition metadata cannot be assumed uniformly present. | Constitution Governance: decide whether template is normative, migrate incrementally, or narrow claims. | `templates/constitution.md`; six live framework constitutions | constitution | Public; observed |
| SG-DRIFT-09 | No constitution composition/version/conflict engine or catalog. | Current composition and precedence remain manual/review-bound. | Constitution Governance: first define stable representation and owner-approved semantics; do not infer an engine from templates. | `constitution-governance/SKILL.md#composition-rules`; templates and current tools | constitution | Public; observed gap |
| SG-DRIFT-10 | No executable constitution retirement or general discipline promotion/deprecation state machine. | Lifecycle transitions depend on review and manual edits. | Relevant lifecycle owners: define receipts/state transitions only if repeated operational need justifies them. | Constitution template maintenance fields; `discipline-governance/SKILL.md#process` | constitution, discipline | Public; observed gap |
| SG-DRIFT-11 | Raw byte comparison conflates permitted generation transforms with semantic drift. | False parity failures can hide the real stale-version defect. | Generation owner: define transform-aware semantic parity validation and receipt. | Generated headers; `sync-generated-skill-package.sh:106-229` | constitution, lifecycle | Public/generated; observed |
| SG-DRIFT-12 | Some discipline cards are thin one-per-sigil pointers. | Documentation duplication without independent recurring-practice evidence. | Discipline Governance: retain only where cross-capability evidence exists; `ontology`, `distillation`, and `residuality` already preserve downgrades. | Relevant cards; `CURATION-RUN-2026-06-21.md` | discipline | Public; observed historical/manual evidence |
| SG-DRIFT-13 | `quality-bar` canonical backing is weaker than catalog wording implies. | Canonical status may be over-read as constitutionally/deterministically backed. | Discipline Governance plus current framework owner: supply exact backing or qualify status rationale. | `cards/quality-bar.md`; `framework/QUALITY-BAR.md` | discipline | Public; observed |
| SG-DRIFT-14 | Public `constitution` and `axiom` lack definition IDs; no public axiom layer exists. | Vocabulary relies on operational prose and private comparison can be accidentally generalized. | Definitions Governance for terms; Constitution Governance for any public axiom relationship proposal. | `DEFINITIONS.md`; constitution-governance README/SKILL; private comparator selectors | constitution | Public gap/private comparison; observed |

## 12. Verdict, consolidation, and residue

### Candidate verdict

SG-VERDICT-01: The initial structural hypothesis survives with one correction: schemas and validators are not a single layer and lifecycle processes are not themselves authority. The defensible model is:

`meaning → scoped law / recurring practice / executable capability / composition → artifact-specific lifecycle decision → bounded enforcement evidence → canonical mutation → discovery and runtime projection → execution evidence and reflection`.

No layer may inherit authority merely by being later in that sequence.

### Recommended consolidation by current owner

| Claim | Owner | Recommendation | Proof ceiling |
|---|---|---|---|
| SG-REC-01 | Definitions Governance | Define public `constitution`; define `axiom` only if public Arcanum intentionally adopts that concept. | Candidate recommendation only |
| SG-REC-02 | Constitution Governance | Normalize constitution identity/status/owner/version semantics before attempting a composition engine. Preserve manual conflict routing until representation is stable. | Candidate recommendation only |
| SG-REC-03 | Discipline Governance | Align validation claims with actual catalog-only coverage; decide whether machine-readable cards are worth implementing. | Candidate recommendation only |
| SG-REC-04 | Sigil Development / generation owner | Repair `discipline-governance` projection drift through the targeted generation route and produce transform-aware parity evidence. | Candidate recommendation only; no mutation authorized |
| SG-REC-05 | Artifact/Schema Constitution tool owner | Freeze and rerun the full validator from `arcanum/`, reconcile the 19/20 count discrepancy, and distinguish current source violations from tool-path defects. | Candidate recommendation only |
| SG-REC-06 | Artifact lifecycle owners | Add transition machinery only where repeated failure warrants it; do not create a universal promotion engine that overrides target owners. | Candidate recommendation only |
| SG-REC-07 | Decision Gate | Continue to own blocker-level precedence, canonicality, status, and scope decisions. | Existing observed route; no decision executed |

### Residue

- No formal public definition IDs for constitution or axiom.
- No public axiom layer.
- No constitution catalog, schema, selector registry, conflict solver, version resolver, compatibility policy, or executable retirement state machine.
- Constitution metadata and template adoption are inconsistent.
- Artifact Constitution’s own authority metadata is ambiguous.
- Metadata example/live-source contradiction remains.
- Discipline cards are not schema-validated; card/catalog parity, Growth Rule, cited-validator existence, and cross-capability evidence are not machine-enforced.
- Discipline promotion/deprecation and composition remain review/prose routes.
- `quality-bar` backing needs tighter authority binding.
- Full Artifact Constitution validation is red; exact failure count differs between explorer observations.
- Validator invocation is root-sensitive.
- Generated `discipline-governance` runtime packages are substantively stale.
- General transform-aware generated-package semantic parity is unproven.
- Most promotion and retirement gates are prose/review-bound.
- Private DomainSpec and CyberAlchemy v2 evidence remains comparison-only.

```json
{
  "ACTION_RECEIPT": {
    "action_id": "spawn-0004",
    "assigned_identity": "Noether, Emmy",
    "role_id": "synthesizer",
    "status": "complete",
    "validation": {
      "evidence_contract": "exact-binding",
      "inputs": [
        "research.md complete explorer returns",
        "explorer-constitution normalized receipt: pass",
        "explorer-discipline normalized receipt: pass",
        "explorer-lifecycle normalized receipt: pass",
        "STRATEGY.md required findings shape"
      ],
      "synthesis_checks": {
        "all_three_returns_joined": "pass",
        "public_private_boundary": "pass",
        "owner_non_collapse": "pass",
        "failed_full_validator_preserved": "pass",
        "generated_discipline_governance_drift_preserved": "pass",
        "prose_only_gates_preserved": "pass",
        "explorer_disagreement_preserved": "pass: full-validator counts remain 20/241 versus 19/216-additional pending frozen rerun"
      },
      "mutation": "none",
      "authority_effect": "none",
      "proof_ceiling": "candidate synthesis from observed sources and explorer-executed checks; no lifecycle approval, promotion, publication, deployment, release, or production claim"
    },
    "blockers": [],
    "native_return_handle": "native-return:/root/structural_synthesizer",
    "residue": [
      "public-constitution-and-axiom-definition-gap",
      "no-public-axiom-layer",
      "constitution-composition-version-retirement-tooling-gaps",
      "constitution-metadata-drift",
      "discipline-semantic-validation-gap",
      "quality-bar-backing-needs-exact-binding",
      "artifact-constitution-full-validator-failure-count-disagreement",
      "artifact-validator-working-directory-sensitivity",
      "discipline-governance-generated-runtime-drift",
      "generated-semantic-parity-unverified",
      "review-bound-promotion-and-retirement"
    ],
    "reroute": {
      "next": "three adversarial reviewers",
      "gates": [
        "precedent-owner",
        "non-vacuity",
        "definitional-soundness"
      ],
      "authority_effect": "none"
    }
  }
}
```
