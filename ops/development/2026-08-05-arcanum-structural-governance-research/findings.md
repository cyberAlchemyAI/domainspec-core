# Arcanum Structural Governance: Holistic Findings

Status: evidence-closed research report for dispatch `2026-08-05-arcanum-structural-governance-research`, run `structural-governance-run-01`.

This report explains the public Arcanum structural system against an exact closure of 54 hashed direct sources plus six hashed run-evidence handles. Its claims retain their individual `observed`, `executed-pass`, `executed-fail`, `historical-observed`, `normative-unverified`, or `run-local-reproduced` proof labels; the closure does not make every claim observed. This is not canonical doctrine, implementation approval, promotion, publication, synchronization, installation, deployment, release, or production proof. Private DomainSpec and CyberAlchemy v2 sources appear only as labelled comparison evidence; their concepts do not become public Arcanum rules here.

Evidence keys used throughout:

- `E-CON`: Alexander, Christopher — constitution and axiom explorer.
- `E-DIS`: Beer, Stafford — discipline and recurring-practice explorer.
- `E-LIFE`: Simon, Herbert — lifecycle and enforcement explorer.
- `R-PREC`: Russell, Bertrand — precedent and owner reviewer, final `PASS`.
- `R-NONVAC`: Popper, Karl — non-vacuity reviewer, final `PASS`.
- `R-DEF`: Quine, Willard Van Orman — definitional-soundness reviewer, final `PASS`.
- `observed`: read directly in the named source.
- `executed-pass` or `executed-fail`: the named bounded check was run.
- `historical-observed`: recorded prior behavior, not rerun here.
- `normative-unverified`: a source prescribes the route, but this dispatch lacks an immutable end-to-end witness.
- `run-local-reproduced`: reproduced in this dispatch evidence; not repaired in canonical Arcanum.

The exact-binding gate is `ready`: retained claims have source paths/selectors, explorer or reviewer bindings, scope, and proof status. The 54 direct-source hashes and six run-evidence hashes are frozen in `ops/development/2026-08-05-arcanum-structural-governance-research/receipts/source-snapshot.json`; the closure decision and deliberately deferred claims are in `ops/development/2026-08-05-arcanum-structural-governance-research/receipts/evidence-closure.json`.

## 1. Plain-language structural stack

Arcanum does not have one ladder where each lower layer automatically authorizes the next. It has different owners doing different jobs, connected by gated transitions.

```text
meaning, when formally defined
  Definitions Governance + DEFINITIONS.md

scoped reusable structural rules
  each constitution + Constitution Governance

recurring practice and declared maturity
  each discipline card/catalog row + Discipline Governance

executable capability contracts and compositions
  sigil source + Sigil Development
  spell source + Spellcraft

bounded mechanical checks
  schemas represent shape
  validators test named rules

authority-changing path
  evidence -> proposal -> explicit target-owner decision -> canonical mutation

sigil/spell availability path
  canonical mutation -> registry -> generation -> synchronization
    -> installation -> runtime -> receipt/telemetry

discipline maturity path
  recurring-practice evidence -> Discipline Governance decision
    -> card/catalog status mutation -> bounded validation and review evidence
```

The decisive boundary is between evidence and authority. A schema, validator pass, receipt, registry entry, generated package, installed skill, runtime success, Inventory page, ontology result, Craft record, or telemetry signal proves only what its own contract says. None can silently substitute for the target owner's decision. Conversely, these surfaces are not “non-authority” in the abstract: Inventory, Ontology Vault, Craft, receipts, and telemetry each own something inside their declared scope. They simply cannot spend that authority outside it. Binding: `arcanum/definitions/DEFINITIONS.md#authority-rule`; `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md#process`; `arcanum/arcana/inventory/SKILL.md#authority-rule`; `arcanum/arcana/ontology-vault/SKILL.md#project-runtime-profile-arguments`; `arcanum/arcana/craft/SKILL.md#process`, step 2 and `#interaction-boundary`; `arcanum/arcana/signal-observer/SKILL.md#authority-rule` — `E-CON`, `E-LIFE`, `R-DEF`; public, observed.

The stack branches after canonical mutation. Sigils and spells have discoverability and runtime-projection machinery. Discipline status instead remains a controlling card/catalog mutation under Discipline Governance; the discipline catalog is not the sigil/spell registry in disguise. Binding: `arcanum/registry/SIGILS.md`; `arcanum/registry/SPELLS.md`; `arcanum/disciplines/DISCIPLINES.md#catalog`; `arcanum/arcana/discipline-governance/SKILL.md:95-128` — `E-DIS`, `E-LIFE`, all reviewers; public, observed contract; discipline transition normative-unverified.

## 2. Controlled vocabulary and non-collapse table

Most structural labels are currently operational terms, not public formal definitions. `DEFINITIONS.md` is normative only for terms it actually contains. This research cannot formalize a word by using it repeatedly.

| Term used here | Exact meaning in this report | Must not collapse into | Binding | Evidence |
|---|---|---|---|---|
| Definition | A formal public meaning only when the term exists in `DEFINITIONS.md` | Any local description or convention | `arcanum/definitions/DEFINITIONS.md#authority-rule` | `E-CON`, `R-DEF`; public, observed |
| Axiom | A private-comparator term; no formal public Arcanum axiom ID was located | Constitution | `implementation/domainspec/AXIOMS.md#axiom-a1-semantic-authority-precedes-implementation`; public definitions inspected by `E-CON` | Private comparison/public inspected-corpus gap, observed |
| Constitution | An operational public artifact class that owns reusable, scoped structural rules | Axiom, schema, validator, discipline, arbitrary policy, or promotion | `arcanum/arcana/constitution-governance/SKILL.md#objective`, `#applicability`, `#non-applicability`, `#anti-patterns` | `E-CON`, `R-DEF`; public, observed |
| Discipline | An operational recurring-practice artifact whose card/catalog declares maturity | Executable capability or constitutional force | `arcanum/disciplines/README.md#boundary`; `arcanum/arcana/discipline-governance/SKILL.md#chain-boundary` | `E-DIS`; public, observed |
| Named procedure | The exact owned procedure, such as Development-to-Canonical Promotion | A new generic `method/process` authority category | `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md#process`; `arcanum/arcana/discipline-governance/SKILL.md#routing-model` | `E-DIS`, `E-LIFE`, `R-DEF`; public, observed |
| Schema | A formally defined structural representation | Validator, semantic owner, execution proof, or approval | `arcanum/definitions/DEFINITIONS.md#def-arc-schema-schema`, especially `#boundary` | `E-CON`, `R-DEF`; public, observed |
| Validator | An executable checker for a bounded owner-declared rule | Rule owner, schema, owner approval, or promotion | `arcanum/arcana/constitution-governance/SKILL.md#validation-model` | All explorers/reviewers; public, observed and bounded execution |
| Lifecycle activity | Propose, gather evidence, validate, review, revise, deprecate, or retire within one artifact owner's route | Promotion, owner acceptance, or mutation | `arcanum/arcana/constitution-governance/SKILL.md:68-170`; `arcanum/arcana/discipline-governance/SKILL.md:95-150`; `arcanum/arcana/sigil-development/SKILL.md:55-160`; `arcanum/arcana/spellcraft/SKILL.md:45-194` | `E-LIFE`, `R-DEF`; public contracts observed; transition completeness varies and constitution/discipline routes are normative-unverified |
| Promotion proposal | A proposed authority change | Owner decision or canonical mutation | `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md:28-84`; `arcanum/arcana/constitution-governance/SKILL.md#modes` | `E-CON`, `R-DEF`; public, observed |
| Owner decision | Exact acceptance, rejection, or block by the current target owner | Validator pass or generic Decision Gate override | `arcanum/arcana/decision-gate/SKILL.md#authority-rule`, `#override-consumption` | `R-DEF`; public, observed |
| Sigil/spell registry | Discoverability projection for accepted sigils and spells | Canonical source or discipline maturity authority | `arcanum/README.md:171-177`; `arcanum/registry/SIGILS.md`; `arcanum/registry/SPELLS.md` | `E-LIFE`, `R-DEF`; public, observed |
| Discipline catalog/status | Controlling declaration of discipline maturity under Discipline Governance | Sigil/spell registry or syntax-validator authority | `arcanum/arcana/discipline-governance/SKILL.md:95-128`; `arcanum/disciplines/DISCIPLINES.md#catalog`; `arcanum/disciplines/scripts/validate-discipline-catalog.py:14-80` | `E-DIS`, `R-DEF`; public, observed; transition review-bound |
| Generation | Production of a transformed runtime projection | Semantic equivalence or promotion | `arcanum/tools/sync-generated-skill-package.sh:106-165` | `E-LIFE`, `R-PREC`; public/generated, observed |
| Synchronization | Copying one staged package into a runtime surface under explicit apply authorization | Installation, promotion, or acceptance | `arcanum/tools/sync-generated-skill-package.sh:168-229` | `E-LIFE`, `R-PREC`; public/generated, observed |
| Installation | Making a projected package available | Canonicality, acceptance, or runtime correctness | `arcanum/tools/bootstrap_arcanum.sh`; `arcanum/tools/install_arcanum.sh` | `E-LIFE`, `R-DEF`; public/runtime, observed |
| Runtime execution | Behavior of the installed projected contract | Lifecycle closure or promotion | `arcanum/arcana/task-session/SKILL.md:295-302,418-420` | `E-LIFE`, `R-DEF`; public/runtime, observed |
| Authority | Always the exact authority of a named owner over a named scope | A universal scalar inherited by downstream evidence | `arcanum/arcana/decision-gate/SKILL.md#authority-rule`; `arcanum/arcana/inventory/SKILL.md#authority-rule`; `arcanum/arcana/ontology-vault/SKILL.md#project-runtime-profile-arguments`; `arcanum/arcana/craft/SKILL.md#interaction-boundary`; `arcanum/arcana/signal-observer/SKILL.md#authority-rule` | `R-DEF`; operational usage only, source boundaries observed |

`Policy` is deliberately omitted as a structural class: the inspected public corpus did not establish a public definition or lifecycle owner for that generic category. Binding: `arcanum/arcana/constitution-governance/SKILL.md#non-applicability`; `ops/development/2026-08-05-arcanum-structural-governance-research/reviews/definitional-revision-2.md` — `R-DEF`; removed from the candidate taxonomy.

## 3. Constitution and axiom catalog

Six public framework constitution files were observed. That is a filesystem result, not evidence of a complete registry-backed constitution catalog.

| Constitution surface | Current role/status | Enforcement or gap | Binding | Evidence |
|---|---|---|---|---|
| Artifact Constitution | Owns artifact classes and promotion boundaries; no explicit top-level ID/status/date/owner/version metadata | Full Artifact Constitution validator was red | `arcanum/framework/ARTIFACT-CONSTITUTION.md#classes`, `#promotion-boundary-rules` | `E-CON`; public, observed; full check executed-fail |
| Schema Constitution | Declared canonical; owns `.yml` schema format and prose boundary | Bounded self-test passed | `arcanum/framework/SCHEMA-CONSTITUTION.md#rules` | `E-CON`; public, observed/executed-pass subset |
| Artifact Metadata Constitution | Candidate metadata rules | Parser and advisory integration already exist even though the document labels parser checks as future; selector/profile identity resolution and composition are still absent | `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md:106-176`; `arcanum/tools/validate-artifact-metadata.py:15-40,183-269`; `arcanum/tools/validate-artifact-constitution.sh:351-352,391-405` | `E-CON`, `R-PREC`; public, observed; parser self-test executed-pass |
| Gitignore Constitution | Candidate | Explicitly review-bound; no deterministic validator located | `arcanum/framework/GITIGNORE-CONSTITUTION.md#validation` | `E-CON`; public, observed |
| Markdown Linking Constitution | Candidate | Local link/anchor checks are a bounded executable subset | `arcanum/framework/MARKDOWN-LINKING-CONSTITUTION.md`; `arcanum/tools/check_markdown_links.sh` | `E-CON`; public, executed-pass subset |
| Receipt ID Legend Constitution | Candidate | Only the reported `gloss-on-cite` fixtures were executed | `arcanum/framework/RECEIPT-ID-LEGEND-CONSTITUTION.md#validation`; `arcanum/tools/validate-receipt-legend.py` | `E-CON`; public, executed-pass subset |

Constitution Governance is the existing process/lifecycle owner. Its templates provide candidate constitution, composition-pack, and validation-adapter shapes; a task-local composition pack is not canonical source. Binding: `arcanum/arcana/constitution-governance/SKILL.md#objective`, `#modes`, `#process`; `arcanum/arcana/constitution-governance/templates/constitution.md`; `arcanum/arcana/constitution-governance/templates/composition-pack.md#handoff`; `arcanum/arcana/constitution-governance/templates/validation-adapter.md` — `E-CON`, `E-LIFE`; public, observed.

No formal public axiom catalog or axiom definition ID was found in the inspected public sources. This is not a universal repository-absence claim. Private DomainSpec axioms/constitution and CyberAlchemy v2 authority kinds prove only that private owners use related structures; they cannot be copied into public Arcanum as doctrine. Binding: `arcanum/definitions/DEFINITIONS.md#authority-rule`; `arcanum/arcana/constitution-governance/SKILL.md#objective`, `#non-applicability`; private comparison selectors `implementation/domainspec/AXIOMS.md#axiom-a1-semantic-authority-precedes-implementation`, `implementation/domainspec/CONSTITUTION.md#rule-catalog`, and `cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md#candidate-kinds` — `E-CON`, `R-PREC`; public inspected-corpus gap/private comparison, observed.

## 4. Discipline, method, and recurring-practice catalog

The live catalog contains 25 discipline rows and the catalog validator passed with `DISCIPLINE_COUNT=25`. The pass proves only table structure, ID/status syntax, uniqueness, and local evidence-link checks. It does not validate card content, consume the discipline schema, authorize status transitions, or prove recurrence and maturity.

| Declared status | Count | Discipline IDs | Binding | Evidence |
|---|---:|---|---|---|
| canonical | 4 | `schema`, `artifact-constitution`, `quality-bar`, `validation-experiment` | `arcanum/disciplines/DISCIPLINES.md#catalog` | `E-DIS`; public catalog, observed; syntax executed-pass |
| implemented | 1 | `observability` | `arcanum/disciplines/DISCIPLINES.md#catalog` | `E-DIS`; public, observed |
| active-pattern | 11 | `planning`, `dispatch`, `context-selection`, `evidence-inventory`, `definition-governance`, `decision-gating`, `interview`, `research-evidence`, `runtime-boundary`, `development-package-promotion-gate`, `two-lane-dialectic` | `arcanum/disciplines/DISCIPLINES.md#catalog` | `E-DIS`; public, observed; semantics not machine-proven |
| candidate | 8 | `craft`, `ontology`, `residuality`, `distillation`, `ux-evidence`, `gitignore`, `receipt-id-legend`, `two-lane-representation` | `arcanum/disciplines/DISCIPLINES.md#catalog` | `E-DIS`; public, observed |
| deprecated | 1 | `implementation-readiness` → `planning` | `arcanum/disciplines/DISCIPLINES.md#catalog`; `arcanum/disciplines/cards/implementation-readiness.md#purpose`; `arcanum/arcana/discipline-governance/development/CURATION-RUN-2026-06-21.md#part-b-validate--deprecate-curation-over-arcanums-22` | `E-DIS`, `R-PREC`; public, historical-observed/manual |

All 25 IDs were manually observed to have cards, but the live validator does not prove card/catalog parity. The candidate `discipline.schema.yml` is not consumed by `validate-discipline-catalog.py`. Growth Rule evidence, recurrence, cross-capability recurrence, referenced-validator existence, and card/catalog semantic parity remain manual review obligations. Binding: `arcanum/disciplines/templates/discipline-card.md#discipline-name`; `arcanum/disciplines/discipline.schema.yml#description`; `arcanum/disciplines/scripts/validate-discipline-catalog.py:14-80`; `arcanum/arcana/discipline-governance/SKILL.md:95-150` — `E-DIS`, `E-LIFE`, `R-NONVAC`; public, observed and bounded executed-pass.

Disciplines document recurring practice and recommend the smallest existing hardening owner. They are not duplicate executable sigils. Named procedures remain owned where they already live: Development-to-Canonical Promotion owns its specific promotion procedure; Sigil Maintenance Loop owns its maintenance composition; Invoke owns define/design/plan/handoff context production; Task Session owns one bounded execution session. No generic `method` layer with independent promotion power was established. Binding: `arcanum/arcana/discipline-governance/SKILL.md#routing-model`, `#chain-boundary`; `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md#process`; `arcanum/spells/sigil-maintenance-loop/README.md:1-148`; `arcanum/spells/invoke/plan.md:83-85`; `arcanum/spells/invoke/handoff.md:60-64`; `arcanum/arcana/task-session/SKILL.md:295-302,418-420` — `E-DIS`, `E-LIFE`, `R-PREC`, `R-DEF`; public, observed.

The `quality-bar` row is declared canonical, but its located backing is weaker than the Schema Constitution-style owner/status/validator package. Its rationale needs tighter owner binding or narrower wording; this report does not downgrade it. Binding: `arcanum/disciplines/cards/quality-bar.md`; `arcanum/framework/QUALITY-BAR.md` — `E-DIS`; public, observed gap.

## 5. Owner, authority, dependency, and public/private matrix

| Surface | Authority it holds | What it cannot do | Dependency/transition | Scope and binding | Evidence |
|---|---|---|---|---|---|
| Definitions Governance | Review and synchronize public formal definitions actually admitted to `DEFINITIONS.md` | Turn every operational word into a definition automatically | Candidate wording → review → accepted definition/index sync | Public: `arcanum/definitions/DEFINITIONS.md#authority-rule`; `arcanum/arcana/definitions-governance/SKILL.md:40-109` | `E-CON`, `E-LIFE`, `R-DEF`; observed |
| Each constitution + Constitution Governance | Own scoped structural rules; select/compose/validate/split; prepare promotion | Accept its own promotion proposal without target-owner gate | Applicability → precedence/conflict → validation → proposal → owner decision | Public: `arcanum/arcana/constitution-governance/SKILL.md#objective`, `#modes`, `#process`, `#composition-rules` | `E-CON`, `E-LIFE`, `R-NONVAC`; observed contract; lifecycle normative-unverified |
| Discipline card/catalog + Discipline Governance | Own recurring-practice description and declared maturity | Let syntax validation authorize maturity | Evidence → explicit status decision → card/catalog mutation → bounded checks | Public: `arcanum/arcana/discipline-governance/SKILL.md:95-150`; `arcanum/disciplines/DISCIPLINES.md#catalog` | `E-DIS`, reviewers; observed contract; lifecycle normative-unverified |
| Canonical sigil + Sigil Development | Own executable capability contract mutation | Let telemetry/reflection mutate the contract by itself | Evidence/approval → targeted update → validation → projections | Public: `arcanum/arcana/sigil-development/SKILL.md:55-160,207-220` | `E-LIFE`, `R-DEF`; observed |
| Canonical spell + Spellcraft | Own composition, phases, shared state, gates, handoffs, and failure policy | Redefine constituent sigils | Draft/evidence → readiness decision → accepted mutation → projections | Public: `arcanum/spells/README.md:39-61`; `arcanum/arcana/spellcraft/SKILL.md:92-194` | `E-LIFE`, `R-DEF`; observed |
| Schema owner | Own represented structure | Prove semantics, behavior, or promotion | Accepted shape → schema use/versioning | Public: `arcanum/definitions/DEFINITIONS.md#def-arc-schema-schema`; `arcanum/framework/SCHEMA-CONSTITUTION.md#rules` | `E-CON`, `R-DEF`; observed |
| Validator/tool owner | Execute bounded checks | Establish target-owner legitimacy or approval | Input → pass/flag/block evidence | Public: `arcanum/tools/validate-artifact-constitution.sh`; `arcanum/tools/validate-artifact-metadata.py:15-40,183-269`; `arcanum/disciplines/scripts/validate-discipline-catalog.py:14-80`; `arcanum/tools/check_markdown_links.sh`; `arcanum/tools/validate-receipt-legend.py` | `E-CON`, `E-DIS`, `E-LIFE`, all reviewers; observed implementations/executed subsets |
| Inventory | Own evidence cards, indexes, lint findings, and handoff projections | Own ontology relations, definitions, or promotion | Source-linked compilation → non-authority downstream handoff | Public: `arcanum/arcana/inventory/SKILL.md#authority-rule` | `R-DEF`; observed |
| Ontology Vault | Own ontology semantics, relations, confidence, conventions, and its review recommendations | Mutate upstream source/spec or emit runtime-conformance/promotion verdicts without another owner | Evidence → ontology result/recommendation | Public: `arcanum/arcana/ontology-vault/SKILL.md#project-runtime-profile-arguments`, steps 24-38 | `R-DEF`; observed |
| Craft | When selected, own its ledger scope for contexts, blockers, decisions, and gaps | Rewrite native capability verdicts or external owner gates | Existing ledger → scoped coordination record | Public/local: `arcanum/arcana/craft/SKILL.md#process`, step 2; `#interaction-boundary` | `R-DEF`; observed |
| Receipt | Prove the bounded fields/action/result its producer declares | Transfer authority merely by existing | Action/check → durable bounded evidence | Public: `arcanum/formulae/dispatch-spec/SKILL.md:65-90`; `arcanum/arcana/task-session/SKILL.md:295-302,418-420` | `E-LIFE`, `R-DEF`; observed |
| Signal Observer / telemetry | Own append-only behavior signals and counters | Mutate application source, user artifacts, or the observed sigil | Runtime signal → later reflection route | Public: `arcanum/arcana/signal-observer/SKILL.md#process`, `#authority-rule` | `E-LIFE`, `R-DEF`; observed |
| Workflow Reflect | Own evidence-backed reports/proposals | Edit the target capability | Signals/evidence → proposal | Public: `arcanum/arcana/workflow-reflect/SKILL.md:61-129`; maintenance spell authority boundaries | `E-LIFE`, `R-PREC`; observed |
| Decision Gate | Block consequential mutation and record exact bounded human decisions; consume exact one-use non-protected overrides | Override destructive, authority, promotion, publication, or spend hazards | Exact decision → pass/block/one-use override | Public: `arcanum/arcana/decision-gate/SKILL.md#authority-rule`, `#override-consumption` | `R-DEF`; observed |
| Dispatch Spec / Orchestrate | Validate route shape and persist/schedule/join/reduce/gate/close native actions | Inherit target-artifact lifecycle or promotion authority | Valid route → coordinated execution evidence | Public/generated runtime: `arcanum/formulae/dispatch-spec/SKILL.md:65-90`; `.agents/skills/orchestrate/SKILL.md:59-143` | `E-LIFE`, `R-PREC`, `R-DEF`; observed |
| Private DomainSpec / CyberAlchemy v2 owners | Own their private axioms, constitutions, and authority kinds | Become public Arcanum authority by comparison or citation | Private owner transitions only | `implementation/domainspec/AXIOMS.md#axiom-a1-semantic-authority-precedes-implementation`; `implementation/domainspec/CONSTITUTION.md#rule-catalog`; `cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md#candidate-kinds` | `E-CON`; private, observed comparison only |

## 6. Precedence, composition, conflict, versioning, deprecation, and retirement rules

Applicability and precedence are two separate decisions. First determine which constitutions apply; only then order the applicable rules. Explicit selectors are preferred when present, while path heuristics are fallback evidence. The deployed metadata parser verifies presence/list shape but does not resolve selector or profile identities. Binding: `arcanum/arcana/constitution-governance/SKILL.md#process`; `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md#composition`; `arcanum/tools/validate-artifact-metadata.py:15-40,183-269` — `E-CON`, `R-PREC`, `R-DEF`; public, observed prose/parser boundary; automatic resolution unverified.

After applicability, the declared order is narrowest to broadest:

```text
task-specific
  -> artifact type
    -> domain or capability
      -> framework
        -> repository fallback
```

“Newest wins” and “broader wins” are forbidden shortcuts. Conflicting claims must remain visible and classified. An unresolved blocker conflict stops consequential mutation and routes to a human decision surface. Binding: `arcanum/arcana/constitution-governance/SKILL.md#composition-rules`, `#anti-patterns`; `arcanum/arcana/decision-gate/SKILL.md#authority-rule` — `E-CON`, `E-LIFE`, `R-NONVAC`, `R-DEF`; public, normative-unverified. No conflicting-rule fixture or matching Decision Gate receipt was produced.

The Constitution Governance phrase `local override` is under-typed. A defensible record must name issuer/owner, exact target, rule/conflict, scope, duration or expiry, evidence, and explicit non-effects. A generic Decision Gate override is one-use and only for an exact non-protected decision; it cannot override authority or promotion hazards. Binding: `arcanum/arcana/constitution-governance/SKILL.md#composition-rules`; `arcanum/arcana/decision-gate/SKILL.md:123-156` — `R-DEF`; public, observed generic boundary; constitution-specific override artifact unverified.

Versioning and retirement are incomplete:

- No general constitution catalog, selector-to-owner map, conflict solver, or version resolver was located. This finding does not erase the deployed metadata parser. Binding: `arcanum/arcana/constitution-governance/SKILL.md#process`, `#composition-rules`; `arcanum/arcana/constitution-governance/templates/constitution.md`; `arcanum/arcana/constitution-governance/templates/composition-pack.md#handoff`; `arcanum/arcana/constitution-governance/templates/validation-adapter.md`; `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md:30-60,159-166`; `arcanum/tools/validate-artifact-metadata.py:15-40,183-269`; `arcanum/tools/validate-artifact-constitution.sh:351-405` — `E-CON`, `R-PREC`; public source-comparison gap, observed.
- Constitution templates expose status/update/authority fields but no version; live metadata shapes differ and `supersedes` remains candidate metadata. Binding: `arcanum/arcana/constitution-governance/templates/constitution.md`; `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md:30-60`; `arcanum/framework/ARTIFACT-CONSTITUTION.md`; `arcanum/framework/SCHEMA-CONSTITUTION.md`; `arcanum/framework/GITIGNORE-CONSTITUTION.md`; `arcanum/framework/MARKDOWN-LINKING-CONSTITUTION.md`; `arcanum/framework/RECEIPT-ID-LEGEND-CONSTITUTION.md` — `E-CON`, `R-PREC`; public, observed.
- Constitution retirement has prose triggers but no located executable state machine, dependency check, or retirement receipt. Binding: `arcanum/arcana/constitution-governance/SKILL.md:88-113`; `arcanum/arcana/constitution-governance/templates/constitution.md` maintenance fields — `E-CON`; public prose, enforcement unverified.
- Discipline deprecation does exist as a manual owner-routed procedure: mark deprecated, cite rationale, and name the superseding route. Missing is deterministic transition enforcement. Binding: `arcanum/arcana/discipline-governance/SKILL.md:107-128`; `arcanum/disciplines/DISCIPLINES.md#catalog`; `arcanum/disciplines/cards/implementation-readiness.md#purpose`; `arcanum/arcana/discipline-governance/development/CURATION-RUN-2026-06-21.md#part-b-validate--deprecate-curation-over-arcanums-22` — `E-DIS`, `R-PREC`; public, observed/manual/historical.

## 7. Lifecycle and promotion paths

Every path below distinguishes proposal, owner decision, canonical mutation, and downstream projection. Constitution and discipline paths are `normative-unverified`; sigil maintenance is an observed deployed composition but was not executed here.

### Constitution change

```text
one reusable structural rule
  -> Constitution Governance mode and exact target/owner/selectors/rule
  -> applicability
  -> narrow-to-broad precedence
  -> conflict preservation/classification
  -> required validation
  -> smallest promotion proposal
  -> explicit target-owner decision
  -> accepted canonical mutation
  -> target validation
  -> only required downstream synchronization
```

First stop: unresolved blocker conflict, missing owner, `none-yet` critical validation, or failed required validator. Binding: `arcanum/arcana/constitution-governance/SKILL.md:68-170`; `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md:28-84` — `E-CON`, `E-LIFE`, `R-NONVAC`; public, normative-unverified. Missing: immutable input fixture, composition pack, conflict receipt, owner approval, promotion patch, canonical diff, and synchronization receipt.

### Discipline change

```text
recurring-practice evidence + public-safe/private-parent classification
  -> local-first candidate card/catalog row
  -> smallest existing hardening owner
  -> catalog syntax validation
  -> separate manual schema/recurrence/Growth Rule/validator/parity review
  -> explicit Discipline Governance status decision
  -> controlling card/catalog mutation
  -> bounded validation and review evidence
```

First stop: missing recurrence, privacy mismatch, invalid catalog, inadequate active-pattern evidence, or missing owner/validation/mutation boundary. Foreign constitution/sigil/spell changes are handed to their owners. Binding: `arcanum/arcana/discipline-governance/SKILL.md:95-150`; `arcanum/disciplines/scripts/validate-discipline-catalog.py:14-80` — `E-DIS`, `E-LIFE`, `R-PREC`, `R-NONVAC`, `R-DEF`; public, normative-unverified end to end. Catalog syntax passed and manual deprecation has historical evidence; neither authorizes a current status change.

### Sigil change

The existing `sigil-maintenance-loop` already composes the maintenance route:

```text
Inventory lookup
  -> Signal Observer
  -> Workflow Reflect
  -> explicit human approval
  -> Sigil Development targeted update
  -> validation and maintenance report
```

Inventory is evidence, reflection proposes, and mutation blocks without approved scope. Spellcraft owns the composition; Sigil Development owns the approved contract mutation. If accepted canonical source changes, use the existing targeted package generator/synchronizer. Binding: `arcanum/spells/sigil-maintenance-loop/README.md:1-20,28-39,44-148`; `arcanum/arcana/sigil-development/SKILL.md:55-94`; `arcanum/tools/sync-generated-skill-package.sh:106-229` — `E-LIFE`, `R-PREC`; public deployed contract, observed; no maintenance run executed.

### Spell change

Invoke may prepare context, then Spellcraft resolves the canonical ID and composition; the spell declares components, phases, state, gates, handoffs, and failure policy; bounded evidence precedes a Spellcraft readiness decision and accepted canonical mutation. Only then follow sigil/spell registry update, generation, synchronization, and separate installation/runtime checks. Constituent sigils retain ownership. Binding: `arcanum/spells/README.md:39-61`; `arcanum/arcana/spellcraft/SKILL.md:45-194` — `E-LIFE`, `R-DEF`; public observed process; end-to-end unverified.

### Promotion boundary

A promotion proposal, owner decision, canonical mutation, sigil/spell registry update, discipline catalog/status mutation, generation, synchronization, installation, and runtime execution are distinct transitions. No later artifact retroactively authorizes an earlier arrow. Binding: `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md:28-84`; `arcanum/arcana/decision-gate/SKILL.md#authority-rule`; `arcanum/registry/SIGILS.md`; `arcanum/registry/SPELLS.md`; `arcanum/arcana/discipline-governance/SKILL.md:95-128`; `arcanum/disciplines/DISCIPLINES.md#catalog`; `arcanum/tools/sync-generated-skill-package.sh:106-229`; `arcanum/tools/bootstrap_arcanum.sh`; `arcanum/tools/install_arcanum.sh`; `arcanum/arcana/task-session/SKILL.md:295-302,418-420` — `R-PREC`, `R-NONVAC`, `R-DEF`; public, observed transition boundaries; lifecycle realization and unauthorized-promotion rejection remain unverified.

## 8. Enforcement map: prose to runtime

| Surface | Implemented effect | Proof ceiling | Binding | Evidence |
|---|---|---|---|---|
| Prose contract | Declares rules, owners, routes, gates, and review obligations | Normative intent, not mechanical compliance | Constitution, discipline, and lifecycle owner sources above | All explorers; observed |
| Schema | Represents intended instance shape | Shape only | `arcanum/definitions/DEFINITIONS.md#def-arc-schema-schema`; `arcanum/disciplines/discipline.schema.yml#description` | `E-CON`, `E-DIS`; observed |
| Metadata parser | Extracts Markdown/YAML/JSON/script/sidecar metadata and checks required fields, list shape, status, companion requirement, and non-empty selector/profile lists | Does not resolve identities, choose constitutions, invoke profiles, or solve conflicts | `arcanum/tools/validate-artifact-metadata.py:15-40,183-269` | `E-CON`, `R-PREC`; observed; self-test executed-pass |
| Artifact Constitution validator | Checks bounded artifact/schema/link/metadata surfaces | Full current run is red; does not prove all constitution semantics | `arcanum/tools/validate-artifact-constitution.sh:351-405` | `E-CON`, `E-LIFE`; executed-fail full run |
| Discipline catalog validator | Checks table columns, ID/status syntax, uniqueness, and evidence links | No card parsing, schema/Growth Rule/recurrence enforcement, status authorization, or promotion proof | `arcanum/disciplines/scripts/validate-discipline-catalog.py:14-80` | `E-DIS`, `E-LIFE`, `R-NONVAC`; executed-pass, 25 rows |
| Receipt/test | Records bounded action/check outcome | No independent authority transfer | `arcanum/formulae/dispatch-spec/SKILL.md:65-90`; `arcanum/arcana/task-session/SKILL.md:295-302,418-420` | `E-LIFE`, `R-DEF`; observed |
| Sigil/spell registries | Make accepted sigils/spells discoverable | Do not create source canonicality or runtime parity | `arcanum/README.md:171-177`; `arcanum/registry/SIGILS.md`; `arcanum/registry/SPELLS.md` | `E-LIFE`, `R-DEF`; observed |
| Discipline catalog/status | Controls declared discipline maturity after its owner-gated mutation | Syntax check cannot authorize transition or prove evidence obligations | `arcanum/arcana/discipline-governance/SKILL.md:95-128`; `arcanum/disciplines/DISCIPLINES.md#catalog` | `E-DIS`, reviewers; observed contract; transition normative-unverified |
| Targeted generation/synchronization | Resolves canonical package, stages runtime projection, previews checksum diff, applies only under `--apply`, and rolls back failures | Host-transform semantic equivalence remains unproved; synchronization remains distinct from installation | `arcanum/tools/sync-generated-skill-package.sh:106-229` | `E-LIFE`, `R-PREC`; observed; stale repair unexecuted |
| Installation | Makes projected package available | No acceptance, promotion, or runtime proof | `arcanum/tools/bootstrap_arcanum.sh`; `arcanum/tools/install_arcanum.sh` | `E-LIFE`, `R-DEF`; observed |
| Runtime | Executes the projected contract | Behavior evidence only | `arcanum/arcana/task-session/SKILL.md:295-302,418-420`; `arcanum/arcana/signal-observer/SKILL.md#authority-rule` | `E-LIFE`, `R-DEF`; observed |
| Maintenance spell | Composes lookup, signal, reflection, approval, mutation, and validation | Only its declared sigil-maintenance scope; not a universal observability loop | `arcanum/spells/sigil-maintenance-loop/README.md:1-148` | `R-PREC`; deployed contract, observed |

Executed evidence, without inflation:

- The discipline catalog validator passed with 25 rows, proving only its implemented syntactic/link checks. Binding: `arcanum/disciplines/scripts/validate-discipline-catalog.py:14-80`; `arcanum/disciplines/DISCIPLINES.md#catalog` — `E-DIS`, `E-LIFE`, `R-NONVAC`; executed-pass.
- Artifact Constitution self-test, metadata parser self-test, Receipt Legend self-test, and Markdown local-link/anchor check passed from the `arcanum/` root. Binding: `arcanum/tools/validate-artifact-constitution.sh`; `arcanum/tools/validate-artifact-metadata.py`; `arcanum/tools/validate-receipt-legend.py`; `arcanum/tools/check_markdown_links.sh`; `arcanum/framework/ARTIFACT-CONSTITUTION.md`; `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md#validation`; `arcanum/framework/RECEIPT-ID-LEGEND-CONSTITUTION.md#validation`; `arcanum/framework/MARKDOWN-LINKING-CONSTITUTION.md` — `E-CON`; executed-pass subsets.
- Full Artifact Constitution validation failed. `E-CON` reported 20 listed new `.schema.json` failures and 241 total warnings; `E-LIFE` reported 19 schema-format failures and 216 additional warnings. Only “full validation failed” is closed. Exact failure/warning cardinality is unresolved pending one frozen-tree rerun. Binding: `arcanum/tools/validate-artifact-constitution.sh`; `arcanum/framework/SCHEMA-CONSTITUTION.md#rules` — `E-CON`, `E-LIFE`, `R-NONVAC`; executed-fail, count deferred.
- Parent-root invocation produced misleading path failures because the validator derives the outer Git root while using `framework/` and `tools/` repository-relative paths. Binding: `arcanum/tools/validate-artifact-constitution.sh:1-11` — `E-CON`, `R-PREC`; executed behavior.
- Canonical `discipline-governance` `0.2.2` differs substantively from generated Codex/Claude `0.2.1`; this is a witnessed stale projection, not a raw-byte-only inference. Binding: `arcanum/arcana/discipline-governance/SKILL.md`; `.agents/skills/discipline-governance/SKILL.md`; `.claude/skills/discipline-governance/SKILL.md`; `arcanum/tools/sync-generated-skill-package.sh:106-229` — `E-LIFE`, `R-PREC`, `R-NONVAC`; observed stale projection; repair unexecuted.

## 9. Integration with Invoke, Task Session, Craft, and the building protocol

```text
Invoke
  define/design/plan context + lifecycle handoff
    -> artifact-specific lifecycle owner
       selects the claim and the owner route
      -> Task Session
         executes one admitted task/SWU and returns bounded evidence
        -> Craft, only when selected
           governs its ledger scope for contexts/blockers/decisions/gaps
          -> owner-specific evidence or maintenance route
            -> promotion proposal
              -> explicit target-owner decision
                -> canonical mutation
                  -> sigil/spell registry
                    -> generation -> synchronization -> installation -> runtime
```

The discipline branch diverges: an explicit Discipline Governance decision precedes the controlling card/catalog status mutation and bounded validation/review. It does not inherit the sigil/spell registry/runtime path merely because both use indexes.

| Integration point | Exact boundary | Binding | Evidence |
|---|---|---|---|
| Invoke | Its handoff is context, not mutation or lifecycle authority | `arcanum/spells/invoke/plan.md:83-85`; `arcanum/spells/invoke/handoff.md:60-64` | `E-LIFE`; public, observed |
| Artifact lifecycle owner | Selects the claim, legal transition, validation, and owner gate | `arcanum/arcana/constitution-governance/SKILL.md:68-170`; `arcanum/arcana/discipline-governance/SKILL.md:95-150`; `arcanum/arcana/sigil-development/SKILL.md:55-160`; `arcanum/arcana/spellcraft/SKILL.md:45-194` | All explorers/reviewers; public contracts observed; constitution/discipline realization normative-unverified |
| Task Session | Executes one admitted bounded task/SWU; its evidence does not grant promotion authority | `arcanum/arcana/task-session/SKILL.md:295-302,418-420` | `E-LIFE`, `R-DEF`; public, observed |
| Craft | If selected, owns its ledger scope but cannot overwrite native verdicts or external gates | `arcanum/arcana/craft/SKILL.md#process`, step 2; `#interaction-boundary` | `R-DEF`; public/local, observed |
| Sigil maintenance | Must use the existing Sigil Maintenance Loop, including Inventory lookup and explicit human approval before mutation | `arcanum/spells/sigil-maintenance-loop/README.md:1-148` | `R-PREC`; already-deployed contract, not executed |
| Dispatch Spec / Orchestrate | Own coordination evidence, not the artifact's semantics or promotion | `arcanum/formulae/dispatch-spec/SKILL.md:65-90`; `.agents/skills/orchestrate/SKILL.md:59-143` | `E-LIFE`, `R-PREC`, `R-DEF`; observed |
| Sigil/spell registry | Separate post-acceptance discoverability transition | `arcanum/registry/SIGILS.md`; `arcanum/registry/SPELLS.md`; `arcanum/README.md:171-177` | `E-LIFE`, reviewers; observed; not discipline maturity authority |
| Discipline catalog/status | Separate owner-gated maturity transition, not a sigil/spell registry | `arcanum/arcana/discipline-governance/SKILL.md:95-128`; `arcanum/disciplines/DISCIPLINES.md#catalog`; `arcanum/disciplines/scripts/validate-discipline-catalog.py:14-80` | `E-DIS`, reviewers; contract observed; transition normative-unverified and syntax non-authorizing |
| Generation and synchronization | Generate a transformed projection, then separately copy it under explicit apply authorization | `arcanum/tools/sync-generated-skill-package.sh:106-229` | `E-LIFE`, reviewers; observed; semantic equivalence unproved |
| Installation and runtime | Separately make a synchronized package available, then execute it | `arcanum/tools/bootstrap_arcanum.sh`; `arcanum/tools/install_arcanum.sh`; `arcanum/arcana/task-session/SKILL.md:295-302,418-420` | `E-LIFE`, reviewers; observed boundaries; end-to-end unverified |

This makes the earlier Invoke–Task Session–Craft model cohesive without creating a new universal coordinator: Invoke prepares, the artifact owner routes, Task Session executes, Craft coordinates only its selected ledger, and existing owner-specific maintenance/promotion machinery governs any durable change.

## 10. Reproducible drift, duplication, bugs, and missing links

| Finding | Consequence | Existing-owner disposition | Binding | Proof |
|---|---|---|---|---|
| Canonical `discipline-governance` is `0.2.2`; generated Codex/Claude packages are `0.2.1` | Generated runtime routes can omit the local-first consuming-repository boundary | Preview and, only when authorized, apply the existing targeted package synchronization; separately verify expected transforms and substantive version/content before installation | `arcanum/arcana/discipline-governance/SKILL.md`; `.agents/skills/discipline-governance/SKILL.md`; `.claude/skills/discipline-governance/SKILL.md`; `arcanum/tools/sync-generated-skill-package.sh:106-229` | `E-LIFE`, `R-PREC`, `R-NONVAC`; observed stale projection; repair unexecuted |
| Full Artifact Constitution validation is red | Required schema-format validation is not green | Freeze one tree, rerun from `arcanum/`, reconcile exact counts, then route failures to existing owners | `arcanum/tools/validate-artifact-constitution.sh`; `arcanum/framework/SCHEMA-CONSTITUTION.md#rules` | `E-CON`, `E-LIFE`; executed-fail; count unresolved |
| Validator is root-sensitive | Parent-root invocation can obscure real failures with misleading paths | Harden or document the existing validator's root contract, not a duplicate wrapper by default | `arcanum/tools/validate-artifact-constitution.sh:1-11` | `E-CON`, `R-PREC`; executed behavior |
| Metadata Constitution calls deployed parser checks future | Owner document understates current implementation while selector/profile resolution truly remains future | Reconcile the candidate constitution with deployed parser behavior through Constitution Governance | `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md:106-176`; `arcanum/tools/validate-artifact-metadata.py:15-40,183-269`; `arcanum/tools/validate-artifact-constitution.sh:351-405` | `R-PREC`; observed doc/implementation drift |
| Metadata Constitution's Schema Constitution example does not match the live header | Example claims adoption not present in source | Repair example or separately adopt metadata through the exact owner gate | `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md:116-122`; `arcanum/framework/SCHEMA-CONSTITUTION.md` header | `E-CON`, `R-PREC`; observed |
| Artifact Constitution lacks top-level identity/status/owner/version metadata; live constitutions diverge from template | Applicability/version assumptions cannot be generalized | Decide through Constitution Governance and the existing metadata owner before new catalog/schema machinery | `arcanum/framework/ARTIFACT-CONSTITUTION.md` top level; `arcanum/arcana/constitution-governance/templates/constitution.md`; `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md:30-60` | `E-CON`, `R-PREC`; observed |
| Discipline schema is disconnected from catalog validator | Card semantics and Growth Rule are not mechanically enforced | Extend the existing validator only with owner approval, or narrow governance claims | `arcanum/disciplines/discipline.schema.yml#description`; `arcanum/disciplines/scripts/validate-discipline-catalog.py:14-80` | `E-DIS`, reviewers; observed |
| Active-pattern recurrence, validator existence, card/catalog parity, and Growth Rule are review-only | Syntax pass is easy to overread | Preserve manual checks and their proof ceiling | `arcanum/arcana/discipline-governance/SKILL.md:95-150`; `arcanum/disciplines/scripts/validate-discipline-catalog.py:14-80` | `E-DIS`; observed |
| Manual discipline deprecation exists; deterministic transitions do not | “No lifecycle exists” is false, but automatic enforcement is also false | Build from Discipline Governance if repeated failures justify automation | `arcanum/arcana/discipline-governance/SKILL.md:107-128`; `arcanum/disciplines/DISCIPLINES.md#catalog`; `arcanum/disciplines/cards/implementation-readiness.md#purpose`; `arcanum/arcana/discipline-governance/development/CURATION-RUN-2026-06-21.md#part-b-validate--deprecate-curation-over-arcanums-22` | `E-DIS`, `R-PREC`; observed/manual/historical |
| No general constitution catalog, selector-owner map, conflict solver, or version resolver | Composition remains review-bound despite deployed metadata parsing | Extend existing Constitution Governance/Metadata Constitution only after representation and need decisions | `arcanum/arcana/constitution-governance/SKILL.md#process`, `#composition-rules`; `arcanum/arcana/constitution-governance/templates/composition-pack.md#handoff`; `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md:30-60,159-166`; `arcanum/tools/validate-artifact-metadata.py:15-40,183-269` | `E-CON`, `R-PREC`; observed gap |
| Targeted staging/checksum synchronization already exists; transform-aware semantic equivalence is unproved | “Parity tooling absent” and “raw bytes must match” are both false | Use existing preview first; add bounded semantic checks only for a repeated defect preview cannot distinguish; installation remains separate | `arcanum/tools/sync-generated-skill-package.sh:106-229`; `arcanum/tools/bootstrap_arcanum.sh`; `arcanum/tools/install_arcanum.sh` | `E-LIFE`, `R-PREC`; observed synchronization/installation boundary; equivalence unverified |
| Thin one-per-sigil discipline cards risk duplicating capability descriptions without cross-capability recurrence | Catalog can become a shadow skill index | Retain/downgrade through Discipline Governance; prior curation already downgraded `ontology`, `distillation`, and `residuality` | `arcanum/disciplines/DISCIPLINES.md#catalog`; `arcanum/arcana/discipline-governance/development/CURATION-RUN-2026-06-21.md` | `E-DIS`; historical-observed |
| `quality-bar` backing is weaker than its catalog status suggests | Maturity can be overread as deterministic/constitution-backed | Tighten exact existing-owner backing or qualify rationale | `arcanum/disciplines/cards/quality-bar.md`; `arcanum/framework/QUALITY-BAR.md`; `arcanum/disciplines/DISCIPLINES.md#catalog` | `E-DIS`; observed |
| Most structural labels lack public definition IDs | Explanatory language can be mistaken for canonical semantics | Define only through Definitions Governance; keep `axiom` private unless explicitly adopted | `arcanum/definitions/DEFINITIONS.md#authority-rule`; `arcanum/arcana/constitution-governance/SKILL.md#objective`; `arcanum/disciplines/README.md#boundary`; `arcanum/arcana/sigil-development/SKILL.md:55-94`; `arcanum/spells/README.md:39-61` | `E-CON`, `R-DEF`; observed gap |
| End-to-end constitution/discipline changes, conflict block, and unauthorized-promotion rejection lack immutable fixtures | The operating paths are not discriminating execution proof | Keep `normative-unverified`; add fixtures only within current lifecycle owners | `arcanum/arcana/constitution-governance/SKILL.md:68-170`; `arcanum/arcana/discipline-governance/SKILL.md:95-150`; `arcanum/arcana/decision-gate/SKILL.md#authority-rule`; `ops/development/2026-08-05-arcanum-structural-governance-research/reviews/non-vacuity-revision-2.md` | `R-NONVAC`; open negative; no fixture invented |
| One canonical run-global action-ID allocation defect reproduced at reviewer, writer, and auditor wave boundaries | Global causal identity and receipt admission became ambiguous three times | Preserve the three raw outputs and their three run-local remaps; route one run-global allocation fix and multi-wave regression fixture to the existing coordinator owner | `.agents/skills/orchestrate/scripts/native_dispatch_coordinator.py:320-350,493-514`; exact raw/remap handles below | `R-DEF`; run-local-reproduced at three boundaries; no canonical repair |

The Orchestrate workaround is evidence, not a product fix. One canonically open run-global allocation defect reproduced at three boundaries:

- Reviewer boundary: raw collision `ops/development/2026-08-05-arcanum-structural-governance-research/native-run/run-01/wave-02-reduction/next-actions.json`; run-local remap to `spawn-0005..0007` in `ops/development/2026-08-05-arcanum-structural-governance-research/native-run/run-01/wave-03-plan/coordinator-action-id-extension.json`.
- Writer boundary: raw collision `ops/development/2026-08-05-arcanum-structural-governance-research/native-run/run-01/wave-03-reduction-route/next-actions.json`; run-local remap to `spawn-0008` in `ops/development/2026-08-05-arcanum-structural-governance-research/native-run/run-01/wave-04-plan/coordinator-action-id-extension.json`.
- Auditor boundary: raw collision `ops/development/2026-08-05-arcanum-structural-governance-research/native-run/run-01/wave-04-reduction/next-actions.json`; run-local remap to `spawn-0009` in `ops/development/2026-08-05-arcanum-structural-governance-research/native-run/run-01/wave-05-plan/coordinator-action-id-extension.json`.

The canonical cause binding is `.agents/skills/orchestrate/scripts/native_dispatch_coordinator.py:320-350,493-514`. All six run handles are hashed in `ops/development/2026-08-05-arcanum-structural-governance-research/receipts/source-snapshot.json`. Canonical coordinator bytes were not changed: `run-local-reproduced` at three boundaries, canonical repair open.

## 11. Finite operator playbooks for structural changes

These playbooks are owner-routed interpretations of current contracts. Constitution and discipline playbooks remain `normative-unverified`.

### Definition

1. Confirm the term is intended to be Arcanum-wide and check whether it already exists.
2. Route wording and index changes through Definitions Governance.
3. Validate exact references.
4. Stop if the wording imports a private-only hierarchy or silently redefines an owned term.

Binding: `arcanum/definitions/DEFINITIONS.md#authority-rule`; `arcanum/arcana/definitions-governance/SKILL.md:40-109` — `E-CON`, `R-DEF`; observed owner route; no mutation executed.

### Constitution

1. Name exact target, owner, selectors, rule ID, examples/non-examples, validation mode, and promotion boundary.
2. Resolve applicability separately from precedence; do not treat metadata field validation as selector resolution.
3. Apply narrow-to-broad order and preserve conflicts.
4. Stop on unresolved conflict, missing owner, absent critical validation, or failed required check.
5. Frame the smallest proposal and require explicit target-owner acceptance.
6. Only after acceptance, mutate canonical source, validate, and synchronize required projections.

Binding: `arcanum/arcana/constitution-governance/SKILL.md:68-170`; `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md:28-84` — `E-CON`, `E-LIFE`, `R-NONVAC`; normative-unverified; end-to-end witness absent.

### Discipline

1. Supply recurring-practice evidence and classify it `public-safe` or `private-parent`; consuming-repository practice stays local-first.
2. Draft the exact candidate card and catalog row.
3. Choose the smallest existing hardening owner and run the catalog validator.
4. Record manual card/schema, recurrence, Growth Rule, validator-reference, and cross-capability review separately.
5. Stop on any missing obligation; obtain an explicit Discipline Governance status decision.
6. Mutate card/catalog only after that decision. Deprecation must cite rationale and superseding route.
7. Hand off foreign constitution/sigil/spell changes to their owners.

Binding: `arcanum/arcana/discipline-governance/SKILL.md:95-150`; `arcanum/disciplines/scripts/validate-discipline-catalog.py:14-80`; `arcanum/disciplines/DISCIPLINES.md#catalog` — `E-DIS`, reviewers; normative-unverified; catalog syntax non-authorizing.

### Sigil

1. Resolve exact canonical sigil and run the existing Sigil Maintenance Loop.
2. Attempt Inventory lookup, capture behavior signal, and reflect with evidence/inference/gaps separated.
3. Stop without explicit approved mutation scope.
4. Route a bounded approved change through Sigil Development and validate it.
5. If canonical source changed, preview and then explicitly authorize only the affected targeted generated package sync.

Binding: `arcanum/spells/sigil-maintenance-loop/README.md:1-148`; `arcanum/arcana/sigil-development/SKILL.md:55-160`; `arcanum/tools/sync-generated-skill-package.sh:106-229` — `E-LIFE`, `R-PREC`; deployed contract observed; not executed here.

### Spell

1. Resolve canonical ID/aliases and route through Spellcraft.
2. Declare components, phases, state, gates, handoffs, and failure policy while preserving constituent ownership.
3. Gather bounded composition evidence and require Spellcraft's decision.
4. Mutate canonical spell source only after acceptance.
5. Then update sigil/spell registry, generate, synchronize, separately install, and verify runtime behavior.

Binding: `arcanum/spells/README.md:39-61`; `arcanum/arcana/spellcraft/SKILL.md:45-194`; `arcanum/registry/SPELLS.md`; `arcanum/tools/sync-generated-skill-package.sh:106-229`; `arcanum/tools/install_arcanum.sh` — `E-LIFE`, `R-DEF`; observed transition boundaries; end-to-end unverified.

### Conflict, drift, or projection mismatch

1. Freeze exact source and projection identities.
2. Separate applicability from precedence.
3. Classify the mismatch as permitted transform, stale projection, rule conflict, validator defect, or owner-document drift.
4. Preserve conflicts; type any local override by issuer, target, rule, scope, duration, evidence, and non-effects.
5. Never use a generic override for authority/promotion hazards.
6. Stop mutation on failed required validation or missing owner gate; preserve unrelated dirty-tree residue.

Binding: `arcanum/arcana/constitution-governance/SKILL.md#composition-rules`; `arcanum/arcana/decision-gate/SKILL.md:123-156`; `arcanum/tools/sync-generated-skill-package.sh:106-229` — `E-CON`, `E-LIFE`, all reviewers; observed generic boundaries; conflict fixture coverage incomplete.

## 12. Verdict, consolidation, residue, and next owners

### Verdict

Arcanum's defensible structural model is a typed network of scoped owners and legal transitions, not one authority stack. Definitions govern only the public terms they formally contain. Constitutions own reusable scoped rules; disciplines own recurring-practice descriptions and declared maturity; sigils own executable capability contracts; spells own compositions. Schemas represent shape and validators provide bounded detection. Lifecycle activity can prepare a promotion proposal, but an explicit target-owner decision must precede canonical mutation.

After acceptance, sigil/spell registry update, generation, synchronization, installation, and runtime are separate downstream transitions. Discipline maturity instead changes through an explicit Discipline Governance decision and the controlling card/catalog mutation; its syntax validator cannot authorize that transition. Inventory, Ontology Vault, Craft, receipts, and telemetry retain their distinct scoped authorities but cannot promote unrelated canonical source. Binding: `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md:28-84`; `arcanum/registry/SIGILS.md`; `arcanum/registry/SPELLS.md`; `arcanum/arcana/discipline-governance/SKILL.md:95-128`; `arcanum/disciplines/DISCIPLINES.md#catalog`; `arcanum/disciplines/scripts/validate-discipline-catalog.py:14-80`; `arcanum/tools/sync-generated-skill-package.sh:106-229`; `arcanum/tools/bootstrap_arcanum.sh`; `arcanum/tools/install_arcanum.sh`; `arcanum/arcana/task-session/SKILL.md:295-302,418-420`; `arcanum/arcana/inventory/SKILL.md#authority-rule`; `arcanum/arcana/ontology-vault/SKILL.md#project-runtime-profile-arguments`; `arcanum/arcana/craft/SKILL.md#interaction-boundary`; `arcanum/arcana/signal-observer/SKILL.md#authority-rule` — all explorers and final reviewers; observed boundaries, with constitution/discipline realization normative-unverified.

All three adversarial gates passed `synthesis-zig-zag-02`:

| Gate | Final disposition | What it established | Binding |
|---|---|---|---|
| Precedent/owner | `PASS` | The model builds from the deployed metadata parser, Sigil Maintenance Loop, manual deprecation, and targeted synchronization route; it keeps sigil/spell registries distinct from the Discipline Governance maturity catalog and synchronization distinct from installation; it introduces no duplicate universal registry/lifecycle/validator/promotion machinery | `ops/development/2026-08-05-arcanum-structural-governance-research/reviews/precedent-revision-2.md`; `R-PREC` |
| Non-vacuity | `PASS` | Missing end-to-end/conflict/unauthorized-promotion fixtures remain explicit; registry is not maturity authority, catalog syntax is non-authorizing, synchronization is not installation, and no absent witness is represented as executed evidence | `ops/development/2026-08-05-arcanum-structural-governance-research/reviews/non-vacuity-revision-2.md`; `R-NONVAC` |
| Definitional soundness | `PASS` | Definition scope, schema/validator, proposal/decision/mutation, sigil-spell registry/discipline-maturity catalog, synchronization/installation, scoped evidence authorities, and applicability/precedence remain separate | `ops/development/2026-08-05-arcanum-structural-governance-research/reviews/definitional-revision-2.md`; `R-DEF` |

### Consolidation by existing owner

| Current owner | Build-from-owned next action | Proof ceiling |
|---|---|---|
| Definitions Governance | Decide whether public Arcanum needs a formal `constitution` definition; adopt `axiom` only after a separate explicit public concept decision | Candidate recommendation; no definition/promotion |
| Constitution Governance / Metadata Constitution | Reconcile the document with deployed parser behavior; decide whether metadata plus filesystem discovery is sufficient; address version semantics before new machinery | Candidate recommendation; selector/composition still unproved |
| Discipline Governance | Preserve manual deprecation; either extend the existing validator with approval or narrow maturity claims—do not create a second catalog/lifecycle | Candidate recommendation; lifecycle normative-unverified |
| Sigil Development / generation owner | Repair stale `discipline-governance` projections through targeted preview/apply only when separately authorized | Existing route; repair unexecuted |
| Artifact/Schema Constitution tool owner | Freeze a tree, rerun from `arcanum/`, reconcile counts, then harden/document root resolution in the existing validator | Executed-fail current snapshot; no repaired check |
| Spellcraft / Sigil Development | Use the existing Sigil Maintenance Loop; do not add a universal Inventory/telemetry/reflection coordinator | Deployed contract observed, not run |
| Decision Gate + exact artifact owners | Keep generic override exact, one-use, and non-protected; promotion hazards remain with owner gates | Observed boundary |
| Orchestrate coordinator owner | Make action identity run-global and add a multi-wave collision regression fixture | Run-local reproduced defect; no canonical repair |
| Each artifact lifecycle owner | Add immutable end-to-end and closed-negative fixtures only inside the owned route | Candidate recommendation; do not centralize into universal engine |

### Residue

- Formal public definition IDs remain absent for most structural labels; no public axiom layer was found in the inspected corpus.
- Metadata parsing is deployed, but selector/profile identity resolution and conflict composition are unproved.
- Constitution catalog, version resolution, deterministic retirement, and consistent metadata/template adoption remain absent or review-bound.
- Artifact Metadata Constitution drifts from the deployed parser/integration and from its Schema Constitution example.
- Discipline card/schema, Growth Rule, recurrence, validator-reference, and card/catalog parity enforcement remain disconnected.
- Manual discipline deprecation exists; deterministic transition enforcement does not.
- Catalog syntax validation remains non-authorizing; `quality-bar` backing remains weakly bound.
- Full Artifact Constitution validation remains failed; exact failure/warning counts are unresolved and validator root sensitivity remains.
- Generated `discipline-governance` packages remain stale; targeted staging/checksum sync exists, but transform-aware semantic equivalence is unproved.
- Immutable end-to-end constitution and discipline witnesses, a conflict-block fixture, and an unauthorized-promotion rejection fixture remain absent.
- Canonical Orchestrate cross-wave action-ID allocation remains defective; only run-local remaps exist.
- Private DomainSpec and CyberAlchemy v2 evidence remains comparison-only.

### Final evidence ceiling

This report is an evidence-backed current explanation and an owner-routed consolidation proposal. It proves no canonical source repair, promotion, publication, generated-package synchronization, installation, deployment, release, or production readiness.
