# Candidate structural model — synthesis zig-zag revision 1

Status: complete replacement synthesis for `synthesis-zig-zag-01`. This is read-only research evidence for renewed adversarial review. It is not canonical Arcanum authority, lifecycle approval, promotion, publication, deployment, release, or production proof.

## 1. Evidence and terminology contract

Explorer references:

- `E-CON`: Alexander, Christopher — constitution and axiom explorer.
- `E-DIS`: Beer, Stafford — discipline and practice explorer.
- `E-LIFE`: Simon, Herbert — lifecycle and enforcement explorer.
- `R-PREC`, `R-NONVAC`, `R-DEF`: the three first-pass adversarial reviews.

Proof labels:

- `observed`: directly read in a named source.
- `executed-pass` / `executed-fail`: a named check was run by an explorer.
- `historical-observed`: a recorded earlier change or curation, not rerun here.
- `normative-unverified`: a source prescribes a route, but this dispatch has no immutable end-to-end witness.
- `run-local-reproduced`: reproduced in this dispatch’s persisted run evidence; not a canonical product repair.
- `unverified`: neither directly executed nor proven complete.

The word “canonical” below is used only when a source itself declares or occupies an owner-recognized canonical surface. Publication of this synthesis cannot make any claim canonical.

## 2. Typed structural and transition matrix

| Claim | Category | Semantic owner | Lifecycle/change owner | Canonical or controlling artifact | States / legal transition | Emitted evidence and ceiling | Exact binding | Return | Scope / proof |
|---|---|---|---|---|---|---|---|---|---|
| SG-STACK-01R | Formally defined term | `DEFINITIONS.md`, but only for terms actually present there | Definitions Governance | `arcanum/definitions/DEFINITIONS.md` | Candidate wording → Definitions Governance review → accepted definition/index synchronization | Definition entry establishes normative public meaning only for its declared scope | `arcanum/definitions/DEFINITIONS.md#authority-rule`; `arcanum/arcana/definitions-governance/SKILL.md:40-63,66-109` | E-CON, E-LIFE, R-DEF | Public Arcanum; observed |
| SG-STACK-02R | Operational concept | The artifact/process owner that currently describes it | Definitions Governance only if later formalized | Current README, SKILL, framework document, or tool contract | Operational description remains local to its source; it does not become a formal definition by synthesis | Source-backed operational meaning; no repository-wide semantic claim | Constitution, discipline, sigil, spell, lifecycle, registry, installation, validator, receipt, Inventory, ontology, telemetry, Craft, policy, method, process, and authority lack located formal public definition IDs | E-CON, R-DEF | Public operational vocabulary; observed gap |
| SG-STACK-03R | Constitution | The specific constitution owns its scoped rules | Constitution Governance owns create/select/compose/validate/split and promotion preparation | `arcanum/framework/*CONSTITUTION.md`; governance contract in `arcanum/arcana/constitution-governance/SKILL.md` | Candidate rule → applicability review → composition/conflict review → validation → promotion proposal; acceptance remains owner-gated | Rule selections, composition pack, validation result; no end-to-end promotion witness here | `constitution-governance/SKILL.md#objective`, `#modes`, `#process`, `#composition-rules`, `#validation-model` | E-CON, E-LIFE, R-NONVAC | Public; observed contract; lifecycle normative-unverified |
| SG-STACK-04R | Discipline | Card/catalog own recurring-practice description and declared maturity | Discipline Governance | `arcanum/disciplines/cards/<id>.md`; `arcanum/disciplines/DISCIPLINES.md` | Candidate → active-pattern / implemented / canonical, or manual deprecation; each status change requires owner review | Catalog validation proves only implemented table/link checks; broader status semantics are review-bound | `arcanum/arcana/discipline-governance/SKILL.md:95-128`; `arcanum/disciplines/DISCIPLINES.md#catalog` | E-DIS, E-LIFE, R-PREC, R-NONVAC | Public; observed; full lifecycle normative-unverified |
| SG-STACK-05R | Sigil contract | Canonical tier package owns executable capability contract | Sigil Development | `<formulae\|transmutations\|arcana>/<id>/SKILL.md` | Development evidence → owner review → approved canonical change → downstream projection | Experiments, execution receipts, telemetry, reflection; none independently promote | `arcanum/arcana/sigil-development/SKILL.md:55-94,97-160,207-220` | E-LIFE, R-DEF | Public operational artifact contract; observed |
| SG-STACK-06R | Spell contract | Canonical spell owns composition | Spellcraft | `arcanum/spells/<id>/README.md` | Draft/adaptation → composition validation → Spellcraft readiness decision → accepted source change → projections | Composition evidence; cannot redefine constituent sigils | `arcanum/spells/README.md:39-61`; `arcanum/arcana/spellcraft/SKILL.md:92-163,181-194` | E-LIFE, R-DEF | Public operational artifact contract; observed |
| SG-STACK-07R | Schema | Schema owner for the represented structure | Rule/artifact lifecycle owner | Schema source plus any governing constitution | Proposed structure → owner acceptance → schema use/versioning | Shape constraints; no semantic authority, execution proof, or promotion effect | `arcanum/definitions/DEFINITIONS.md#def-arc-schema-schema`, especially `#boundary`; `arcanum/framework/SCHEMA-CONSTITUTION.md#rules` | E-CON, R-DEF | Public; formally defined term; observed |
| SG-STACK-08R | Validator | No independent semantic authority; it checks an owner-declared rule | Rule/tool owner | Named executable checker | Input → bounded check → pass/flag/block | Detection evidence only; cannot establish owner legitimacy or promotion | `arcanum/arcana/constitution-governance/SKILL.md#validation-model`; `arcanum/tools/validate-artifact-constitution.sh`; `arcanum/disciplines/scripts/validate-discipline-catalog.py:14-80` | All explorers, all reviewers | Public; observed; bounded checks executed |
| SG-STACK-09R | Lifecycle activity | Artifact-specific owner | Constitution Governance, Discipline Governance, Sigil Development, or Spellcraft | Owner’s lifecycle contract | Propose, gather evidence, validate, review, revise, deprecate, or retire as supported by that owner | Lifecycle artifacts and recommendations; lifecycle activity is not itself an authority-changing transition | Lifecycle bindings in SG-STACK-03R through SG-STACK-06R | E-LIFE, R-DEF | Public; observed; transition coverage varies |
| SG-STACK-10R | Promotion proposal | Proposing lifecycle/process route | Target canonical owner remains decisive | Promotion patch framed under `DEVELOPMENT-TO-CANONICAL-PROMOTION.md` | Evidence → smallest durable claim → proposed target change and approval state | Proposal/patch; Constitution Governance `promote` prepares adoption rather than completing it | `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md#process`; `constitution-governance/SKILL.md#modes` | E-CON, E-LIFE, R-DEF | Public process; observed; review-bound |
| SG-STACK-11R | Owner decision | Exact target owner or protected owning gate | Same owner | Owner-specific approval or rejection evidence | Proposal → explicit accept/reject/block | Decision evidence; no uniform accepting actor or approval schema was found across artifact families | `DEVELOPMENT-TO-CANONICAL-PROMOTION.md:28-84`; `arcanum/arcana/decision-gate/SKILL.md#authority-rule` | E-CON, R-NONVAC, R-DEF | Public; observed boundary; uniform mechanism unverified |
| SG-STACK-12R | Canonical mutation | Exact canonical-source owner | Exact lifecycle owner under accepted scope | Existing canonical source file | Explicit owner acceptance → smallest source mutation → target validation | Source diff plus validation; mutation must not precede acceptance | `DEVELOPMENT-TO-CANONICAL-PROMOTION.md:28-84`; `ARTIFACT-CONSTITUTION.md#promotion-boundary-rules` | E-CON, E-LIFE, R-DEF | Public; normative-unverified end to end |
| SG-STACK-13R | Registry/catalog update | Registry or catalog owner | Relevant lifecycle/projection owner | `arcanum/registry/SIGILS.md`, `arcanum/registry/SPELLS.md`, or discipline catalog | Accepted canonical change → registry/catalog update | Discoverability/status projection; never creates canonicality | `arcanum/README.md:171-177`; `arcanum/disciplines/DISCIPLINES.md#catalog` | E-DIS, E-LIFE, R-DEF | Public; observed |
| SG-STACK-14R | Generation | Canonical package remains source authority | Existing generator/synchronizer owner | Bootstrap-generated staging package | Resolve canonical package → generate runtime-specific staged projection | Generated bytes with permitted host transforms; generation does not prove semantic equivalence | `arcanum/tools/sync-generated-skill-package.sh:106-165` | E-LIFE, R-PREC, R-NONVAC, R-DEF | Public tool/generated output; observed |
| SG-STACK-15R | Synchronization | Existing targeted generator/sync route | Generator owner under explicit `--apply` authorization | Target `.agents/skills/<id>/` or `.claude/skills/<id>/` package | Preview staged diff → authorized package-scoped checksum sync → rollback on failure | Preview/apply output and changed package; structural staging/diff exists, transform-aware semantic equivalence remains unproved | `arcanum/tools/sync-generated-skill-package.sh:168-229` | E-LIFE, R-PREC, R-NONVAC | Public tool/generated output; observed; repair not executed |
| SG-STACK-16R | Installation | Installer/runtime-surface owner | Installation route | Installed runtime package | Existing generated package → installation/availability | Availability evidence only; not acceptance or promotion | `arcanum/tools/bootstrap_arcanum.sh`; `arcanum/tools/install_arcanum.sh`; generated package headers | E-LIFE, R-DEF | Public tool/runtime; observed |
| SG-STACK-17R | Runtime execution | Runtime contract and current invocation owner | Task/session or capability execution route | Installed projected package | Installed capability → invocation → behavior/result | Behavioral evidence only; execution does not promote source | `arcanum/arcana/task-session/SKILL.md:295-302,418-420`; `arcanum/arcana/signal-observer/SKILL.md#authority-rule` | E-LIFE, R-DEF | Public/runtime; observed |
| SG-STACK-18R | Private comparison | Private DomainSpec or CyberAlchemy v2 owner | Its private gates | Private axioms, constitutions, and authority-kind sources | Private owner transitions only | Comparison evidence; cannot become public Arcanum doctrine by citation | `implementation/domainspec/AXIOMS.md#axiom-a1-semantic-authority-precedes-implementation`; `implementation/domainspec/CONSTITUTION.md#rule-catalog`; `cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md#candidate-kinds` | E-CON | Private; observed; comparison only |

The minimum defensible transition is:

```text
candidate evidence
  → owner-selected claim
  → promotion proposal
  → explicit owner decision
  → canonical source mutation
  → registry/catalog update
  → generated projection
  → authorized synchronization/installation
  → runtime execution
  → receipt and telemetry
```

None of these arrows is automatic. A later artifact cannot retroactively authorize an earlier transition.

## 3. Controlled vocabulary and non-collapse table

| Claim | Label used here | Classification | Must not collapse into | Exact binding | Return | Scope / proof |
|---|---|---|---|---|---|---|
| SG-VOC-01R | Definition | Formal only when the term exists in `DEFINITIONS.md`; otherwise operational | Any prose description or local convention | `DEFINITIONS.md#authority-rule` | E-CON, R-DEF | Public; observed |
| SG-VOC-02R | Axiom | Private-comparator term; no located formal public ID | Constitution | `implementation/domainspec/AXIOMS.md`; absence reported against public definitions | E-CON, R-DEF | Private comparison/public gap; observed |
| SG-VOC-03R | Constitution | Operational public artifact class with scoped rule ownership | Axiom, schema, validator, discipline, arbitrary policy, or promotion | `constitution-governance/SKILL.md#objective`, `#applicability`, `#non-applicability`, `#anti-patterns` | E-CON, R-DEF | Public operational meaning; observed |
| SG-VOC-04R | Discipline | Operational recurring-practice artifact | Executable capability or constitutional force | `disciplines/README.md#boundary`; `discipline-governance/SKILL.md#chain-boundary` | E-DIS | Public operational meaning; observed |
| SG-VOC-05R | Named procedure | Use the actual procedure name, such as Development-to-Canonical Promotion | Undefined generic “method/process” categories | `DEVELOPMENT-TO-CANONICAL-PROMOTION.md#process`; `discipline-governance/SKILL.md#routing-model` | E-DIS, E-LIFE, R-DEF | Public; observed; generic taxonomy withdrawn |
| SG-VOC-06R | Schema | Formally defined structural representation | Validator or semantic authority | `DEFINITIONS.md#def-arc-schema-schema#boundary` | E-CON, R-DEF | Public; formally defined; observed |
| SG-VOC-07R | Validator | Operational executable checker | Rule owner, schema, approval, or promotion | `constitution-governance/SKILL.md#validation-model` | All | Public; observed/executed subset |
| SG-VOC-08R | Promotion proposal | Proposed authority change | Owner acceptance or canonical mutation | `DEVELOPMENT-TO-CANONICAL-PROMOTION.md:28-84`; `constitution-governance/SKILL.md#modes` | E-CON, R-DEF | Public; observed |
| SG-VOC-09R | Owner decision | Exact acceptance/rejection by current owner | Generic Decision Gate override or validator pass | `decision-gate/SKILL.md#authority-rule`, `#override-consumption` | R-DEF | Public; observed |
| SG-VOC-10R | Registry | Discoverability projection | Canonical source | `arcanum/README.md:171-177` | E-LIFE, R-DEF | Public; observed |
| SG-VOC-11R | Generation | Production of transformed runtime projection | Semantic equivalence | `sync-generated-skill-package.sh:106-165` | E-LIFE, R-PREC | Public/generated; observed |
| SG-VOC-12R | Synchronization | Copying one staged package into a runtime surface | Promotion or installation acceptance | `sync-generated-skill-package.sh:168-229` | E-LIFE, R-PREC | Public/generated; observed |
| SG-VOC-13R | Installation | Runtime availability change | Acceptance, canonicality, or promotion | Installer sources and generated headers | E-LIFE, R-DEF | Public/runtime; observed |
| SG-VOC-14R | Runtime execution | Actual projected-contract behavior | Lifecycle closure or promotion | `task-session/SKILL.md:295-302,418-420` | E-LIFE, R-DEF | Public/runtime; observed |
| SG-VOC-15R | Policy | Omitted as a structural category because no public owner/definition was established | Constitution | Reviewer correction against SG-VOC-03 | R-DEF | Removed from candidate taxonomy |
| SG-VOC-16R | Authority | Always qualified by exact scope and owner | A universal scalar inherited by evidence or projections | Scoped authority rows below | R-DEF | Operational usage only |

## 4. Constitution and axiom catalog

| Claim | Artifact | Status / role | Exact binding | Return | Scope / proof |
|---|---|---|---|---|---|
| SG-CON-01R | Constitution Governance | Canonical sigil `0.1.0`; process/lifecycle owner | `arcanum/arcana/constitution-governance/SKILL.md#objective`, `#modes`, `#process` | E-CON, E-LIFE | Public; observed |
| SG-CON-02R | Constitution, composition-pack, and validation-adapter templates | Candidate/common shapes; task-local composition pack is not canonical source | `templates/constitution.md`; `templates/composition-pack.md#handoff`; `templates/validation-adapter.md` | E-CON | Public candidate/template; observed |
| SG-CON-03R | Artifact Constitution | Owns artifact classes and promotion boundary; lacks explicit top-level status/date/owner/ID/version | `arcanum/framework/ARTIFACT-CONSTITUTION.md#classes`, `#promotion-boundary-rules` | E-CON | Public; observed; full validator failed |
| SG-CON-04R | Schema Constitution | Declared canonical; owns `.yml` schema format and prose boundary | `arcanum/framework/SCHEMA-CONSTITUTION.md#rules` | E-CON | Public canonical; observed; bounded validator executed |
| SG-CON-05R | Artifact Metadata Constitution plus deployed parser | Candidate constitution still labels parser work “future,” but `validate-artifact-metadata.py` already extracts Markdown/YAML/JSON/script/sidecar metadata and validates required fields, list shape, status, companion requirement, and non-empty selector/profile lists; Artifact Constitution invokes it in advisory changed-file mode | `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md:106-176`; `arcanum/tools/validate-artifact-metadata.py:15-40,183-269`; `arcanum/tools/validate-artifact-constitution.sh:351-352,391-405` | E-CON, R-PREC | Public candidate plus deployed validator; observed; parser self-test executed |
| SG-CON-06R | Metadata resolution ceiling | Existing parser does not resolve selector/profile identities, choose constitutions, invoke named profiles, or solve conflicts | Same sources, especially constitution future checks at `:159-166` versus parser implementation at `:183-269` | R-PREC | Public; observed implementation boundary; resolution unverified |
| SG-CON-07R | Gitignore Constitution | Candidate; explicitly review-bound without deterministic validator | `arcanum/framework/GITIGNORE-CONSTITUTION.md#validation` | E-CON | Public candidate; observed |
| SG-CON-08R | Markdown Linking Constitution | Candidate; local links/anchors are a bounded executable subset | Constitution plus `arcanum/tools/check_markdown_links.sh` | E-CON | Public candidate; executed-pass subset |
| SG-CON-09R | Receipt ID Legend Constitution | Candidate; only the reported `gloss-on-cite` fixtures were executed | `RECEIPT-ID-LEGEND-CONSTITUTION.md#validation`; `validate-receipt-legend.py` | E-CON | Public candidate; executed-pass subset |
| SG-CON-10R | Development-to-Canonical Promotion | Active named procedure; target owner remains decisive | `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md#process` | E-CON, E-LIFE | Public active procedure; observed |
| SG-CON-11R | Public axiom catalog | None found in the inspected public corpus; not a universal repository absence claim | Public definitions and Constitution Governance surfaces inspected by E-CON | E-CON, R-PREC | Public corpus finding; observed |
| SG-CON-12R | Private axiom/constitution namespaces | DomainSpec chain and CyberAlchemy v2 candidate constitutions are comparator evidence only | Private selectors listed in SG-STACK-18R | E-CON | Private; observed |

Six public framework constitutions were observed. This is a filesystem finding, not proof of a universal or registry-backed constitution catalog.

## 5. Discipline and recurring-practice catalog

| Claim | Status | Count / IDs | Exact binding | Return | Scope / proof |
|---|---:|---|---|---|---|
| SG-DIS-01R | canonical | 4: `schema`, `artifact-constitution`, `quality-bar`, `validation-experiment` | `arcanum/disciplines/DISCIPLINES.md#catalog` | E-DIS | Public catalog; observed; catalog syntax executed-pass |
| SG-DIS-02R | implemented | 1: `observability` | Same selector | E-DIS | Public catalog; observed |
| SG-DIS-03R | active-pattern | 11: `planning`, `dispatch`, `context-selection`, `evidence-inventory`, `definition-governance`, `decision-gating`, `interview`, `research-evidence`, `runtime-boundary`, `development-package-promotion-gate`, `two-lane-dialectic` | Same selector | E-DIS | Public catalog; status semantics not machine-proven |
| SG-DIS-04R | candidate | 8: `craft`, `ontology`, `residuality`, `distillation`, `ux-evidence`, `gitignore`, `receipt-id-legend`, `two-lane-representation` | Same selector | E-DIS | Public catalog; observed |
| SG-DIS-05R | deprecated | 1: `implementation-readiness` → `planning` | `DISCIPLINES.md#catalog`; `cards/implementation-readiness.md#purpose`; `CURATION-RUN-2026-06-21.md#part-b-validate--deprecate-curation-over-arcanums-22` | E-DIS, R-PREC | Public; manual owner-routed deprecation exists; historical-observed |
| SG-DIS-06R | Card surface | All 25 IDs were manually observed to have cards | `disciplines/templates/discipline-card.md#discipline-name`; `disciplines/cards/` | E-DIS | Public; manual observation; parity not validator-proven |
| SG-DIS-07R | Candidate schema | Defines intended machine-readable shape but is not consumed by the live catalog validator | `disciplines/discipline.schema.yml#description`; `scripts/validate-discipline-catalog.py:14-80` | E-DIS, E-LIFE | Public candidate; observed |
| SG-DIS-08R | Validation ceiling | Live validator checks table columns, ID/status syntax, uniqueness, and local evidence links; it does not parse cards, enforce schema/card parity, Growth Rule, validator existence, or cross-capability recurrence | `scripts/validate-discipline-catalog.py:14-80`; `discipline-governance/SKILL.md:95-128` | E-DIS, R-NONVAC | Public; executed-pass only for implemented subset |
| SG-DIS-09R | Quality Bar qualification | Catalog declares `quality-bar` canonical, while located backing remains owner prose without Schema Constitution-like status/owner/validator metadata | `cards/quality-bar.md`; `framework/QUALITY-BAR.md` | E-DIS | Public; observed; backing requires tighter owner binding |

## 6. Scoped authority map

| Claim | Surface | Authority it actually holds | Boundary | Exact binding | Return | Scope / proof |
|---|---|---|---|---|---|---|
| SG-AUTH-01R | Inventory | Owns evidence cards, indexes, lint findings, and handoff projections | Generated pages remain source-linked; handoff packets are non-authority until downstream acceptance; Inventory does not own ontology relations or canonical definitions | `arcanum/arcana/inventory/SKILL.md#authority-rule` | R-DEF | Public capability; observed |
| SG-AUTH-02R | Ontology Vault | Owns governed ontology meaning, relations, confidence, conventions, and its own review/promotion recommendations | Runtime-profile outputs and delegated returns are evidence; they cannot emit source/spec mutation, runtime-conformance verdicts, or upstream promotion without separate owner permission | `arcanum/arcana/ontology-vault/SKILL.md#project-runtime-profile-arguments`; process steps 24–38 | R-DEF | Public capability; observed |
| SG-AUTH-03R | Craft | An existing selected ledger is authoritative within its scope for contexts, blockers, open decisions, and gaps | It does not rewrite native capability verdicts or assign external authority merely through lane/role fields | `arcanum/arcana/craft/SKILL.md#process`, step 3; `#interaction-boundary`; `add_blocker` invariants | R-DEF | Public capability / local ledger; observed |
| SG-AUTH-04R | Receipt | Proves the bounded fields/action/result its producer contract declares | Receipt existence cannot authorize promotion or replace owner approval | `arcanum/formulae/dispatch-spec/SKILL.md:65-90`; `task-session/SKILL.md:295-302,418-420` | E-LIFE, R-DEF | Public evidence contract; observed |
| SG-AUTH-05R | Telemetry / Signal Observer | Owns append-only behavior signals and reflection counters | Non-blocking by default; cannot mutate application source, user artifacts, or observed sigil without a separate maintenance workflow | `arcanum/arcana/signal-observer/SKILL.md#process`, `#authority-rule` | E-LIFE, R-DEF | Public evidence capability; observed |
| SG-AUTH-06R | Workflow Reflect | Owns evidence-backed proposals/reports | It proposes; it does not edit the target capability | `arcanum/arcana/workflow-reflect/SKILL.md:61-129`; `sigil-maintenance-loop/README.md#authority-boundaries` | E-LIFE, R-PREC | Public capability; observed |
| SG-AUTH-07R | Decision Gate | Blocks consequential mutation and records bounded human decisions; can consume exact one-use non-protected overrides | Destructive, authority, promotion, publication, and spend hazards stay with owning gates; generic override receipt is not reusable authority | `arcanum/arcana/decision-gate/SKILL.md#authority-rule`, `#override-consumption` | R-DEF | Public capability; observed |
| SG-AUTH-08R | Dispatch Spec / Orchestrate | Validate dispatch shape; persist, schedule, join, reduce, gate, and close native actions | Coordination mechanics do not confer artifact lifecycle or promotion authority | `dispatch-spec/SKILL.md:65-90`; `.agents/skills/orchestrate/SKILL.md:59-143` | E-LIFE, R-PREC, R-DEF | Public/generated runtime; observed |

The corrected boundary is not “all are non-authority.” Each surface has authority inside its declared scope. None can independently promote canonical Arcanum source outside that scope.

## 7. Applicability, precedence, conflict, override, versioning, and retirement

| Claim | Rule | Exact binding | Return | Scope / proof |
|---|---|---|---|---|
| SG-COMP-01R | Applicability selection happens before precedence. Gather candidate constitutions from explicit selectors when present; path heuristics are fallback evidence. | `constitution-governance/SKILL.md#process`; `ARTIFACT-METADATA-CONSTITUTION.md#composition` | E-CON, R-DEF | Public; observed prose; automatic selector resolution unverified |
| SG-COMP-02R | The deployed metadata parser validates field presence and list shape but does not resolve selector/profile identities. | `validate-artifact-metadata.py:15-40,183-269`; `ARTIFACT-METADATA-CONSTITUTION.md:159-166` | R-PREC | Public; observed |
| SG-COMP-03R | After applicability is established, precedence is narrowest to broadest: task-specific → artifact type → domain/capability → framework → repository fallback. | `constitution-governance/SKILL.md#composition-rules`; `ARTIFACT-METADATA-CONSTITUTION.md#composition` | E-CON, E-LIFE | Public; normative-unverified |
| SG-COMP-04R | Conflicts must be preserved and classified; unresolved blocker conflicts stop consequential mutation and route to a human decision surface. | `constitution-governance/SKILL.md#composition-rules`; `decision-gate/SKILL.md#authority-rule` | E-CON, R-NONVAC, R-DEF | Public; normative-unverified; no conflicting-rule fixture/receipt |
| SG-COMP-05R | Constitution Governance’s phrase `local override` is under-typed in the located composition contract. A defensible override must name issuer/owner, exact target, rule/conflict, scope, duration or expiry, evidence, and non-effects. | Constitution Governance conflict rules compared with `decision-gate/SKILL.md#override-consumption` | R-DEF | Public; operational requirement; constitution-specific artifact unverified |
| SG-COMP-06R | A Decision Gate generic override applies only to an exact non-protected decision and is one-use; it cannot override promotion or authority hazards. | `decision-gate/SKILL.md:123-156` | R-DEF | Public; observed |
| SG-COMP-07R | “Newest wins” and “broader wins” are forbidden shortcuts. | `constitution-governance/SKILL.md#composition-rules`, `#anti-patterns` | E-CON | Public; observed |
| SG-COMP-08R | No general constitution catalog, selector-to-owner mapping, composition/conflict solver, or version resolver was found. This does not negate the existing metadata parser. | Constitution Governance/templates, metadata constitution/parser, current tools | E-CON, R-PREC | Public gap; observed source comparison |
| SG-COMP-09R | Version semantics remain genuinely under-specified: constitution template has update/status/authority fields but no version; live metadata shapes differ; `supersedes` is candidate metadata. | `templates/constitution.md`; framework constitutions; `ARTIFACT-METADATA-CONSTITUTION.md:30-60` | E-CON, R-PREC | Public; observed |
| SG-COMP-10R | Discipline deprecation exists as an owner-routed manual procedure: mark deprecated, cite rationale, name superseding route. What is missing is deterministic transition enforcement. | `discipline-governance/SKILL.md:107-128`; historical `implementation-readiness` deprecation | E-DIS, R-PREC | Public; observed/manual/historical |
| SG-COMP-11R | Constitution retirement has declared triggers but no located executable state machine, dependency check, or retirement receipt. | `constitution-governance/SKILL.md:88-113`; constitution template maintenance fields | E-CON | Public; observed prose; enforcement unverified |

## 8. Lifecycle paths and evidence ceilings

### SG-LIFE-01R — Constitution change

Normative route:

1. Classify one proposed reusable structural rule.
2. Select Constitution Governance mode.
3. Name exact target, owner, selectors, rule ID, examples/non-examples, validation mode, and promotion boundary.
4. Determine applicability.
5. Apply narrow-to-broad precedence.
6. Preserve and classify conflicts.
7. Stop on unresolved blocker conflict, missing owner, `none-yet` critical validation, or failed required validator.
8. Frame the smallest promotion proposal.
9. Obtain explicit target-owner decision.
10. Only after acceptance, mutate canonical source.
11. Validate the accepted target.
12. Synchronize only required downstream projections.

Binding: `constitution-governance/SKILL.md:68-170`; `DEVELOPMENT-TO-CANONICAL-PROMOTION.md:28-84`.  
Proof: public normative-unverified. No exact input fixture, composition pack, conflict receipt, owner approval artifact, promotion patch, canonical diff, or sync receipt was produced in this dispatch.

### SG-LIFE-02R — Discipline change

Normative route:

1. Supply concrete recurring-practice evidence.
2. Classify `public-safe` or `private-parent`; consuming-repository practice is local-first.
3. Draft/update the exact card and catalog row, initially `candidate`.
4. Choose the smallest existing hardening owner: catalog, template, existing validator, constitution, sigil, or spell.
5. Run the existing catalog validator.
6. Separately perform the currently manual card/schema, recurrence, Growth Rule, validator-reference, and cross-capability review.
7. Stop on missing recurrence, privacy mismatch, invalid catalog, inadequate active-pattern evidence, or missing owner/validation/mutation boundary.
8. Obtain Discipline Governance status decision.
9. For deprecation, preserve rationale and superseding route.
10. Hand off any constitution/sigil/spell mutation to its own owner.

Binding: `discipline-governance/SKILL.md:95-150`; `validate-discipline-catalog.py:14-80`.  
Proof: public normative-unverified end to end. Catalog syntax has an executed-pass witness; manual deprecation has historical evidence; no complete current lifecycle witness exists.

### SG-LIFE-03R — Sigil change through the existing maintenance composition

Already-deployed composition:

```text
Inventory lookup
  → Signal Observer
  → Workflow Reflect
  → explicit human approval gate
  → Sigil Development targeted update
  → validation and maintenance report
```

The existing `sigil-maintenance-loop` requires Inventory lookup before reflection, treats Inventory as non-authority evidence, and blocks mutation without approved scope. Spellcraft owns the composition; Sigil Development alone owns approved contract mutation.

Binding: `arcanum/spells/sigil-maintenance-loop/README.md:1-20,28-39,44-109,112-148`; `sigil-development/SKILL.md:55-94`.  
Proof: public already-deployed contract; observed. This dispatch did not execute a maintenance run.

### SG-LIFE-04R — Spell change

Invoke may prepare context → Spellcraft resolves ID and owns composition lifecycle → canonical spell draft/evidence → declare components, phases, shared state, gates, handoffs, failure policy → bounded execution evidence → Spellcraft readiness decision → accepted canonical mutation → registry/generation/synchronization.

Binding: `spells/README.md:39-61`; `spellcraft/SKILL.md:45-75,78-194`.  
Proof: public observed process; no end-to-end witness in this dispatch.

### SG-LIFE-05R — Promotion boundary

Promotion proposal, owner decision, canonical mutation, registry update, generation, synchronization, installation, and runtime execution are separate transitions. A validation pass, receipt, registry row, generated package, installation, runtime success, Inventory result, ontology report, Craft decision, or telemetry signal cannot substitute for the exact owner decision required by another transition.

Binding: SG-STACK-10R through SG-STACK-17R and SG-AUTH-01R through SG-AUTH-08R.  
Proof: observed authority boundary; unauthorized-promotion rejection fixture remains absent.

## 9. Enforcement map

| Claim | Surface | Implemented effect | Evidence ceiling | Exact binding | Return | Proof |
|---|---|---|---|---|---|---|
| SG-ENF-01R | Prose contract | Declares rules, routes, owners, gates, and review obligations | Normative intent, not mechanical compliance | Constitution/discipline/lifecycle sources above | All | Observed |
| SG-ENF-02R | Schema | Represents intended instance shape | Shape only | `DEFINITIONS.md#def-arc-schema-schema`; `discipline.schema.yml` | E-CON, E-DIS | Observed |
| SG-ENF-03R | Metadata parser | Extracts supported metadata encodings; checks required fields, list shape, status, companions, and non-empty selector/profile lists | Does not resolve selector/profile identities or compose constitutions | `validate-artifact-metadata.py:15-40,183-269` | R-PREC | Observed; self-test executed-pass |
| SG-ENF-04R | Artifact Constitution validator | Checks bounded artifact/schema/link/metadata surfaces | Full current run is red; it does not prove all constitution semantics | `validate-artifact-constitution.sh`, especially metadata integration at `:351-405` | E-CON, E-LIFE | Executed-fail full run |
| SG-ENF-05R | Discipline catalog validator | Checks table structure, IDs/statuses, uniqueness, and evidence links | No card parsing, schema enforcement, Growth Rule, recurrence, or promotion proof | `validate-discipline-catalog.py:14-80` | E-DIS, E-LIFE, R-NONVAC | Executed-pass; 25 rows |
| SG-ENF-06R | Receipt/test | Records bounded action or check outcome | No independent authority transfer | `dispatch-spec/SKILL.md:65-90`; owner promotion boundary | E-LIFE | Observed |
| SG-ENF-07R | Registry/catalog | Makes artifacts discoverable and records declared catalog status | Does not create semantic authority or parity | `arcanum/README.md:171-177`; `DISCIPLINES.md#catalog` | E-DIS, E-LIFE | Observed |
| SG-ENF-08R | Targeted generation and sync | Resolves canonical source, stages runtime packages, previews checksum-aware diffs, applies only under `--apply`, and rolls back failures | Permitted host-transform semantic equivalence remains unproved | `sync-generated-skill-package.sh:106-229` | E-LIFE, R-PREC | Observed; stale-package repair not executed |
| SG-ENF-09R | Installation | Makes projected package available | No acceptance or promotion | Bootstrap/installer sources | E-LIFE | Observed |
| SG-ENF-10R | Runtime | Executes projected contract | Behavior evidence only | Task Session and Signal Observer bindings | E-LIFE | Observed |
| SG-ENF-11R | Maintenance spell | Composes Inventory, signal, reflection, approval, mutation, and validation | Applies only to its declared sigil-maintenance scope; not a universal observability loop | `sigil-maintenance-loop/README.md:1-148` | R-PREC | Observed already-deployed composition |

Executed evidence retained without inflation:

- SG-PROOF-01R: discipline catalog validator passed with `DISCIPLINE_COUNT=25`; this proves only its implemented checks.
- SG-PROOF-02R: Artifact Constitution self-test, metadata parser self-test, receipt-legend self-test, and Markdown local-link/anchor check passed from the Arcanum root.
- SG-PROOF-03R: full Artifact Constitution validation failed on the then-current tree. E-CON reported 20 listed new `.schema.json` failures and 241 total warnings; E-LIFE reported 19 schema-format failures and 216 additional warnings. The closed negative is “validation failed.” Exact cardinality remains unresolved pending one frozen rerun.
- SG-PROOF-04R: parent-root invocation produced misleading path failures because the validator derives the outer Git root and uses repository-relative `framework/` and `tools/` paths. The existing validator owner should document or harden this behavior.
- SG-PROOF-05R: canonical `discipline-governance` `0.2.2` differs substantively from generated Codex and Claude `0.2.1` packages. This is a witnessed stale projection, not a raw-byte-only inference.
- SG-PROOF-06R: no end-to-end constitution change, discipline change, conflict/precedence block, unauthorized-promotion rejection, or repaired projection receipt exists in this dispatch.

## 10. Integration with Invoke, Task Session, Craft, and maintenance

```text
Invoke
  produces definition/design/plan context and lifecycle handoff
    ↓
artifact-specific lifecycle owner
  selects the claim and prepares owner-specific work
    ↓
Task Session
  executes one admitted task or SWU and returns bounded evidence
    ↓
Craft, only when selected
  governs its chosen ledger scope for contexts, blockers, decisions, and gaps
    ↓
existing maintenance/evidence routes where applicable
  Sigil Maintenance Loop for sigil maintenance
  other owner-specific experiment/observation/reflection routes
    ↓
promotion proposal
    ↓
explicit target-owner decision
    ↓
canonical mutation
    ↓
registry → generation → synchronization/installation → runtime
```

| Claim | Boundary | Exact binding | Return | Scope / proof |
|---|---|---|---|---|
| SG-BUILD-01R | Invoke handoff is context, not mutation or lifecycle authority | `arcanum/spells/invoke/plan.md:83-85`; `handoff.md:60-64` | E-LIFE | Public; observed |
| SG-BUILD-02R | Task Session execution evidence does not grant lifecycle or promotion authority | `task-session/SKILL.md:295-302,418-420` | E-LIFE | Public; observed |
| SG-BUILD-03R | Craft has scoped ledger authority when selected, but cannot overwrite native capability verdicts or external owner gates | `craft/SKILL.md#process`, step 3; `#interaction-boundary` | R-DEF | Public/local ledger; observed |
| SG-BUILD-04R | Dispatch Spec and Orchestrate own dispatch coordination, not target-artifact authority | `dispatch-spec/SKILL.md:65-90`; `.agents/skills/orchestrate/SKILL.md:59-143` | E-LIFE, R-PREC | Public/generated runtime; observed |
| SG-BUILD-05R | Sigil maintenance must bind to the existing `sigil-maintenance-loop`; it includes Inventory lookup and explicit human approval before Sigil Development mutation | `sigil-maintenance-loop/README.md:1-148` | R-PREC | Public; already-deployed contract; not executed here |
| SG-BUILD-06R | Inventory, ontology, Craft, receipts, and telemetry retain the separate scoped authorities in section 6 | SG-AUTH-01R through SG-AUTH-05R | R-DEF | Mixed public/local evidence surfaces; observed |

## 11. Finite operator playbooks

These are operator interpretations of current owner contracts. Constitution and discipline playbooks are explicitly `normative-unverified`; they are not claimed as executable end-to-end lifecycle proof.

### SG-PLAY-01R — Definition change

1. Verify that the term is intended to be Arcanum-wide.
2. Check whether it already exists in `DEFINITIONS.md`.
3. Route wording and index changes through Definitions Governance.
4. Validate exact references.
5. Stop if the proposed definition would import a private-only hierarchy or silently redefine an owned term.

Proof: observed owner route; no definition mutation executed here.

### SG-PLAY-02R — Constitution change (`normative-unverified`)

1. Supply exact target constitution and proposed rule.
2. Declare owner, selectors, examples/non-examples, validation mode, and promotion boundary.
3. Select applicable sources; do not treat parser field validation as selector resolution.
4. Apply narrow-to-broad precedence.
5. Preserve conflicts.
6. Stop before mutation on unresolved conflict, missing owner decision, `none-yet` critical validation, or failed required validator.
7. Frame the smallest proposal.
8. Require explicit owner acceptance.
9. Mutate canonical source only after acceptance.
10. Validate and then synchronize required projections.

Missing witness: immutable input fixture, composition pack, conflicting-rule record, Decision Gate receipt, owner approval artifact, promotion patch, canonical diff, and sync receipt.

### SG-PLAY-03R — Discipline change (`normative-unverified`)

1. Supply exact recurring-practice evidence and privacy classification.
2. Keep consuming-repository practice local-first.
3. Draft exact card and catalog row.
4. Choose the smallest existing hardening owner.
5. Run the catalog validator.
6. Separately record manual card/schema, recurrence, Growth Rule, validator-reference, and cross-capability review.
7. Stop on any failed or missing obligation.
8. Require Discipline Governance status decision.
9. For deprecation, manually mark `deprecated`, cite rationale, and name the superseding route.
10. Never mutate a foreign constitution, sigil, or spell from the discipline route.

Missing witness: complete current candidate, before/after status, connected card-schema receipt, manual-review receipt, owner approval, and final diff. Historical manual deprecation does not fill that gap.

### SG-PLAY-04R — Sigil maintenance through deployed machinery

1. Resolve exact canonical sigil.
2. Run the existing Sigil Maintenance Loop.
3. Attempt Inventory lookup before reflection.
4. Record current signal.
5. Produce reflection that distinguishes evidence, inference, and gaps.
6. Stop without explicit approved mutation scope.
7. Route approved bounded update through Sigil Development.
8. Validate and emit maintenance report.
9. If canonical source changes, use the existing targeted generation/sync tool for affected runtime packages.

Proof: deployed contract observed; no run executed here.

### SG-PLAY-05R — Spell change

1. Resolve canonical ID and aliases.
2. Route through Spellcraft.
3. Declare components, phases, state, gates, handoffs, and failure policy.
4. Preserve constituent sigil ownership.
5. Gather bounded composition evidence.
6. Require Spellcraft owner decision.
7. Mutate canonical spell source only after acceptance.
8. Update registry, generate, synchronize, and verify separately.

Proof: observed owner process; end-to-end execution unverified.

### SG-PLAY-06R — Conflict or drift

1. Freeze exact source and projection identities.
2. Separate applicability from precedence.
3. Classify mismatch as permitted transform, stale projection, rule conflict, validator defect, or owner-document drift.
4. Preserve every conflicting claim.
5. For a local override, require typed issuer, target, rule/conflict, scope, duration, evidence, and non-effects.
6. Do not use a generic override for authority or promotion hazards.
7. Stop required mutation on failed validation or missing owner gate.
8. Record residue without repairing unrelated dirty-tree findings.

## 12. Drift, duplication, bugs, and missing links

| Claim | Finding | Consequence | Owner-routed disposition | Exact binding | Return | Proof |
|---|---|---|---|---|---|---|
| SG-DRIFT-01R | Canonical `discipline-governance` is `0.2.2` with local-first behavior; generated Codex/Claude packages remain `0.2.1` | Runtime projections can omit the consuming-repository boundary | Use the existing targeted staged generator: preview exact package diff, apply only when authorized, then verify expected generated metadata transforms plus substantive canonical version/content | Canonical/generated files; `sync-generated-skill-package.sh:106-229` | E-LIFE, R-PREC, R-NONVAC | Observed stale projection; repair unexecuted |
| SG-DRIFT-02R | Full Artifact Constitution validator is red | Required canonical schema-format validation is not green | Freeze a tree and rerun from `arcanum/`; classify failures through existing owners | `validate-artifact-constitution.sh`; `SCHEMA-CONSTITUTION.md#rules` | E-CON, E-LIFE | Executed-fail; exact count unresolved |
| SG-DRIFT-03R | Validator resolves the outer Git root when invoked from parent repository | Misleading path failures can obscure actual schema violations | Harden or document the existing validator’s root contract; do not add a duplicate wrapper by default | `validate-artifact-constitution.sh:1-11` | E-CON, R-PREC | Executed behavior |
| SG-DRIFT-04R | Artifact Metadata Constitution says parser checks are future while parser and advisory integration already exist | Owner document understates deployed implementation and overstates the future boundary | Constitution Governance should reconcile the candidate constitution with deployed parser behavior; retain selector/profile resolution as future | `ARTIFACT-METADATA-CONSTITUTION.md:106-176`; parser and integration bindings in SG-CON-05R | R-PREC | Observed owner-document/implementation drift |
| SG-DRIFT-05R | Metadata Constitution’s Schema Constitution example does not match the live header | Example claims adoption not present in source | Repair example or separately adopt metadata through owner gate | `ARTIFACT-METADATA-CONSTITUTION.md:116-122`; live `SCHEMA-CONSTITUTION.md` header | E-CON, R-PREC | Observed |
| SG-DRIFT-06R | Artifact Constitution lacks explicit top-level identity/status/owner/version metadata; live constitutions diverge from template | Applicability and version assumptions cannot be generalized | Decide through Constitution Governance and existing metadata owner before adding new catalog/schema machinery | Artifact Constitution top level; `templates/constitution.md`; `ARTIFACT-METADATA-CONSTITUTION.md:30-60` | E-CON, R-PREC | Observed |
| SG-DRIFT-07R | Discipline schema is disconnected from catalog validator | Card semantics and Growth Rule are not mechanically enforced | Extend the existing validator only if owner-approved, or narrow governance claims; do not create another discipline lifecycle | `discipline.schema.yml`; `validate-discipline-catalog.py:14-80` | E-DIS, R-PREC, R-NONVAC | Observed |
| SG-DRIFT-08R | Active-pattern recurrence, validator existence, card/catalog parity, and Growth Rule are review-only | Syntactic catalog pass can be overread | Preserve explicit manual checks and proof ceiling | `discipline-governance/SKILL.md:95-150`; validator implementation | E-DIS | Observed |
| SG-DRIFT-09R | Manual discipline deprecation exists; deterministic transition enforcement does not | “No discipline lifecycle” would be false, while automated enforcement remains absent | Build from Discipline Governance if repeated failure justifies automation | `discipline-governance/SKILL.md:107-128`; historical deprecation record | E-DIS, R-PREC | Observed/manual/historical |
| SG-DRIFT-10R | No general constitution catalog, selector-to-owner mapping, conflict solver, or version resolver | Composition remains review-bound despite deployed metadata parsing | Extend Constitution Governance and Artifact Metadata Constitution only after representation/need decision | Constitution sources, metadata parser, current tools | E-CON, R-PREC | Observed gap |
| SG-DRIFT-11R | Targeted generator already provides staging, checksum preview/apply, package scope, backup, and rollback; transform-aware semantic equivalence remains unproved | “Parity infrastructure absent” would be false; raw byte equality is also invalid | Use existing preview first; add a bounded semantic check only if staged diff cannot distinguish a real repeated defect | `sync-generated-skill-package.sh:106-229` | E-LIFE, R-PREC | Observed existing mechanism; semantic equivalence unverified |
| SG-DRIFT-12R | Thin one-per-sigil discipline cards remain a duplication risk | Catalog documentation can repeat capability descriptions without independent recurrence | Retain/downgrade through Discipline Governance based on cross-capability evidence; prior curation already downgraded `ontology`, `distillation`, and `residuality` | Relevant cards; `CURATION-RUN-2026-06-21.md` | E-DIS | Historical-observed |
| SG-DRIFT-13R | `quality-bar` canonical backing remains weaker than catalog wording implies | Status can be overread as deterministic or constitution-backed | Supply exact existing-owner backing or qualify rationale | `cards/quality-bar.md`; `framework/QUALITY-BAR.md` | E-DIS | Observed |
| SG-DRIFT-14R | Many structural labels lack public definition IDs | Synthesis language can be mistaken for normative semantics | Define only through Definitions Governance; keep `axiom` private unless explicitly adopted | `DEFINITIONS.md`; current operational sources | E-CON, R-DEF | Observed gap |
| SG-DRIFT-15R | No immutable end-to-end constitution change, discipline change, conflict block, or unauthorized-promotion rejection fixture exists | The proposed operating paths are not discriminating execution proof | Preserve `normative-unverified`; future fixture work belongs to current lifecycle owners | R-NONVAC review against lifecycle sources | R-NONVAC | Open negative; no fixture invented |
| SG-DRIFT-16R | Stock Orchestrate reducer generated cross-wave reviewer IDs `spawn-0002..0004`, colliding with already-used explorer/synthesis IDs | Global causal action identity and exact receipt admission would be ambiguous | This run used a persisted run-local mapping to `spawn-0005..0007`; route the canonical defect to the Orchestrate coordinator owner, but do not call this mapping a canonical repair | `.agents/skills/orchestrate/scripts/native_dispatch_coordinator.py:320-350,493-514`; `native-run/run-01/wave-03-plan/coordinator-action-id-extension.json` | Run-local coordinator evidence, R-DEF | Run-local-reproduced; no canonical mutation |
| SG-DRIFT-17R | Reducer seeds the next wave with `start_action_number=len(actions)+1`, where `actions` is the current reduced wave, while `_compile_named_wave_actions` numbers from that local seed | Cross-wave numbering can restart from a wave-local count | Canonical owner should make action identity run-global and add a multi-wave collision regression fixture; this synthesis does not implement it | Same coordinator selectors and run-local extension | Run-local coordinator evidence | Observed implementation plus reproduced collision; proposed owner repair only |

## 13. Consolidation by current owner

| Claim | Current owner | Classification | Recommendation | Proof ceiling |
|---|---|---|---|---|
| SG-REC-01R | Definitions Governance | Build from owned | Define `constitution` if public Arcanum needs normative semantics; adopt `axiom` only after an explicit public concept decision | Candidate recommendation |
| SG-REC-02R | Constitution Governance / Artifact Metadata Constitution | Build from owned | Reconcile document with deployed parser, decide whether current metadata plus filesystem discovery is sufficient, and address version semantics before proposing new machinery | Candidate recommendation |
| SG-REC-03R | Discipline Governance | Build from owned | Preserve manual deprecation; extend the existing validator or narrow claims rather than creating a second catalog/lifecycle | Candidate recommendation |
| SG-REC-04R | Sigil Development / existing generation owner | Already deployed route | Repair stale `discipline-governance` projections through targeted preview/apply only when authorized | Candidate recommendation; repair unexecuted |
| SG-REC-05R | Artifact/Schema Constitution tool owner | Build from owned | Frozen rerun from `arcanum/`, reconcile exact counts, then harden/document root resolution in the existing validator | Candidate recommendation |
| SG-REC-06R | Spellcraft / Sigil Development | Already deployed route | Use `sigil-maintenance-loop`; do not invent another universal Inventory/telemetry/reflection coordinator | Candidate recommendation |
| SG-REC-07R | Decision Gate and artifact owners | Already deployed boundary | Keep generic override typed and non-protected; authority/promotion hazards remain with their owning gates | Observed boundary |
| SG-REC-08R | Orchestrate coordinator owner | Build from owned | Repair run-global action-ID allocation and add a multi-wave collision regression fixture; preserve current mapping only as run-local evidence | Candidate recommendation; no canonical repair |
| SG-REC-09R | Each lifecycle owner | Build from owned | Add immutable end-to-end and closed-negative fixtures only within that owner’s route; reject a universal promotion/retirement engine | Candidate recommendation |

## 14. Candidate verdict and residue

SG-VERDICT-01R: The defensible model is a typed set of owners and legal transitions, not one authority stack. Formal definitions govern only terms they contain. Constitutions, disciplines, sigils, and spells currently have operational artifact contracts. Schemas represent shape; validators produce bounded enforcement evidence. Lifecycle activity may produce a promotion proposal; an explicit target-owner decision must precede canonical mutation. Registry, generation, synchronization, installation, and runtime are separate downstream transitions. Inventory, Ontology Vault, Craft, receipts, and telemetry each retain scoped authority but cannot use that scope to promote unrelated canonical Arcanum source.

The model is evidence-backed as an explanation of current owner routes and observed gaps. Constitution and discipline lifecycle coordination are not proven executable end to end.

Residue:

- Formal public definition IDs remain absent for most structural labels.
- No public axiom layer was found.
- Metadata parsing exists, but selector/profile identity resolution and conflict composition remain unproved.
- Constitution catalog, version resolution, and deterministic retirement remain absent or review-bound.
- Constitution metadata/template adoption remains inconsistent.
- Artifact Metadata Constitution drifts from deployed parser/integration.
- Discipline card-schema, Growth Rule, recurrence, validator-reference, and card/catalog parity enforcement remain disconnected.
- Manual discipline deprecation exists; deterministic state-transition enforcement does not.
- `quality-bar` backing requires tighter binding.
- Full Artifact Constitution validation remains failed with unreconciled exact count.
- Validator root sensitivity remains.
- Generated `discipline-governance` packages remain stale.
- Targeted staging/checksum sync exists; permitted-transform semantic equivalence remains unproved.
- Constitution/discipline end-to-end witnesses, conflict-block fixture, and unauthorized-promotion rejection fixture remain absent.
- The Orchestrate action-ID collision has only a run-local extension; canonical coordinator repair remains open.
- Private DomainSpec and CyberAlchemy v2 evidence remains comparison-only.

```json
{
  "REVISION_RECEIPT": {
    "loop_id": "synthesis-zig-zag-01",
    "action_id": "spawn-0004",
    "assigned_identity": "Noether, Emmy",
    "role_id": "synthesizer",
    "status": "complete",
    "validation": {
      "replacement_synthesis": "complete",
      "mutation": "none",
      "authority_effect": "none",
      "repaired_claim_groups": [
        "metadata-parser-and-integration-acknowledged",
        "schema-validator-split",
        "lifecycle-proposal-decision-mutation-sync-split",
        "registry-generation-synchronization-installation-runtime-split",
        "inventory-ontology-craft-receipt-telemetry-scoped-separately",
        "definition-authority-restricted-to-defined-terms",
        "operational-vocabulary-labelled",
        "applicability-precedence-separated",
        "local-override-typed-and-protected-hazards-preserved",
        "constitution-playbook-marked-normative-unverified",
        "discipline-playbook-marked-normative-unverified",
        "manual-discipline-deprecation-preserved",
        "sigil-maintenance-loop-bound-as-existing-composition",
        "targeted-generator-and-checksum-sync-preserved",
        "failed-full-validator-closed-negative-preserved",
        "stale-discipline-governance-projection-preserved",
        "orchestrate-cross-wave-action-id-collision-preserved",
        "run-local-action-id-extension-labelled-non-canonical"
      ],
      "proof_ceiling": "read-only candidate synthesis from direct sources, three explorer returns, three adversarial reviews, and persisted run-local coordinator evidence; no implementation, promotion, publication, deployment, release, or production claim"
    },
    "blockers": [],
    "residue": [
      "no-end-to-end-constitution-change-witness",
      "no-end-to-end-discipline-change-witness",
      "no-conflict-precedence-block-fixture",
      "no-unauthorized-promotion-rejection-fixture",
      "artifact-validator-failure-count-unreconciled",
      "selector-profile-resolution-unproven",
      "constitution-version-resolution-unproven",
      "discipline-card-semantic-validation-unconnected",
      "generated-transform-semantic-equivalence-unproven",
      "orchestrate-canonical-action-id-repair-open"
    ],
    "native_return_handle": "native-return:/root/structural_synthesizer/synthesis-zig-zag-01",
    "next_reviewer_gates": [
      "precedent-owner",
      "non-vacuity",
      "definitional-soundness"
    ]
  }
}
```
