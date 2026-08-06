# Arcanum Structural Governance Research Transcript

Dispatch: `2026-08-05-arcanum-structural-governance-research`

This parent-owned artifact preserves the complete native explorer returns. It is research evidence, not canonical Arcanum authority, lifecycle approval, promotion, publication, deployment, release, or production proof.

## Alexander, Christopher — Constitution and Axiom Lane

## Explorer return: constitution and axiom lane

### Bottom line

In current public Arcanum, a constitution is a durable, scoped governance artifact containing reusable structure/form/artifact-behavior rules, selection predicates, an authority boundary, and a declared validation mode. Constitution Governance owns creation, selection, composition, validation planning, splitting, and promotion preparation.

It is not itself:

- an axiom or epistemic premise;
- a definition of vocabulary;
- a schema describing instance shape;
- a recurring operating discipline;
- a method describing how work proceeds;
- a validator executing a check;
- a policy merely because it expresses a preference;
- an authority-transfer event merely because it exists, is indexed, is installed, or passes validation.

The public implementation is materially incomplete: composition, conflict handling, promotion, splitting, retirement, and metadata-based selection are process contracts/templates, not deterministic engines. Deterministic enforcement exists for a bounded subset of rules.

### 1. Public catalog

| Artifact | Class/status | Owner | Actual role | Proof |
|---|---|---|---|---|
| `arcanum/arcana/constitution-governance/SKILL.md` | Canonical Arcana sigil, version `0.1.0` | Constitution Governance | Process owner for `create`, `add-rule`, `select`, `compose`, `validate`, `split`, `promote` | observed |
| `arcanum/arcana/constitution-governance/templates/constitution.md` | Candidate template | Constitution Governance | Proposed common shape: identity, scope, selectors, rules, validation, promotion, maintenance | observed |
| `arcanum/arcana/constitution-governance/templates/composition-pack.md` | Generated/candidate pack template | Constitution Governance | Task-local projection of selected rules; explicitly not canonical source | observed |
| `arcanum/arcana/constitution-governance/templates/validation-adapter.md` | Plan template | Constitution Governance | Binds a rule to prospective detection logic, fixtures, and promotion evidence | observed |
| `arcanum/framework/ARTIFACT-CONSTITUTION.md` | Framework constitution; document has no explicit top-level status/date/owner | Implicit framework/Constitution Governance; promotion process says `artifact-constitution` | Artifact classes, retention, visibility, generated/runtime rules, promotion boundary, rendering rules | observed; validator executed |
| `arcanum/framework/SCHEMA-CONSTITUTION.md` | `canonical` | Constitution Governance | New canonical schema format and prose-boundary rules | observed; validator executed |
| `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md` | `candidate` | Constitution Governance | Intended typed artifact metadata and selector/profile mechanism | observed; parser self-test executed, but constitution states end-to-end selection remains future |
| `arcanum/framework/GITIGNORE-CONSTITUTION.md` | `candidate` | Constitution Governance | Reviewable ignore-policy rules | observed; explicitly no deterministic validator |
| `arcanum/framework/MARKDOWN-LINKING-CONSTITUTION.md` | `candidate` | Constitution Governance | Markdown navigation, citations, typed relation-like links | observed; local link/anchor checker executed |
| `arcanum/framework/RECEIPT-ID-LEGEND-CONSTITUTION.md` | `candidate` | Constitution Governance | Receipt ID glossing and related review rules | observed; one rule’s validator self-test executed |
| `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md` | `active` process | `artifact-constitution, definitions-governance` | Cross-artifact promotion process; evidence-to-authority boundary | observed |
| `arcanum/registry/SIGILS.md` | Registry/read surface | Registry | Discovers Constitution Governance; does not promote constitutions | observed |
| `.agents/skills/constitution-governance/SKILL.md` | Generated Codex runtime package | Generated from canonical source | Runtime projection | observed |
| `.claude/skills/constitution-governance/SKILL.md` | Generated Claude runtime package | Generated from canonical source | Runtime projection with runtime-specific transformations | observed |

Framework constitution count found: six.

### 2. Exact source bindings

Load-bearing selectors:

- Definition and modes: `arcanum/arcana/constitution-governance/SKILL.md#objective`, `#modes`, `#applicability`, `#non-applicability`.
- Required constitution fields and lifecycle concerns: `arcanum/arcana/constitution-governance/SKILL.md#process`, steps 5–11.
- Precedence/conflicts: `arcanum/arcana/constitution-governance/SKILL.md#composition-rules`.
- Validation categories: `arcanum/arcana/constitution-governance/SKILL.md#validation-model`.
- Non-collapse constraints: `arcanum/arcana/constitution-governance/SKILL.md#anti-patterns`.
- Plain-language definition: `arcanum/arcana/constitution-governance/README.md#core-concepts`.
- Canonical/source pack separation: `arcanum/arcana/constitution-governance/SKILL.md#quality-bar`; `templates/composition-pack.md#handoff`.
- Artifact classes: `arcanum/framework/ARTIFACT-CONSTITUTION.md#classes`, including `#source-artifacts`, `#durable-evidence-artifacts`, `#generated-artifacts`, `#local-runtime-artifacts`.
- Promotion rule: `arcanum/framework/ARTIFACT-CONSTITUTION.md#promotion-boundary-rules`, rule `artifact.promotion.development-to-canonical`.
- Promotion algorithm: `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md#process`, steps 1–9.
- Schema meaning boundary: `arcanum/definitions/DEFINITIONS.md#def-arc-schema-schema`, especially `#boundary`.
- Development/canonical/promotion terms: `arcanum/definitions/DEFINITIONS.md#def-arc-development-artifact-development-artifact`, `#def-arc-canonical-artifact-canonical-artifact`, `#def-arc-promotion-patch-promotion-patch`.
- Schema enforcement: `arcanum/framework/SCHEMA-CONSTITUTION.md#rules`, rule IDs `schema.format.yml`, `schema.format.prose-boundary`, `schema.format.legacy-migration`.
- Metadata precedence: `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md#composition`.
- Metadata enforcement ceiling: `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md#validation` and `#promotion-boundary`.
- Receipt enforcement ceiling: `arcanum/framework/RECEIPT-ID-LEGEND-CONSTITUTION.md#validation`.
- Gitignore enforcement ceiling: `arcanum/framework/GITIGNORE-CONSTITUTION.md#validation`.
- Public authority rule for terms: `arcanum/definitions/DEFINITIONS.md#authority-rule`.

### 3. Namespace and artifact-class map

There is no single repository-wide universal “constitution namespace.”

| Namespace | Meaning/owner | Boundary |
|---|---|---|
| Public Arcanum `framework/*CONSTITUTION.md` | Public reusable framework rules | Public Arcanum authority only |
| Public task-local composition packs | Selected projection for one target | Candidate/generated context; not canonical constitution replacement |
| Private DomainSpec `implementation/domainspec/AXIOMS.md` + `CONSTITUTION.md` | Private governance chain `A1–A6 -> C1–C11 -> gates` | DomainSpec-only; not public Arcanum law |
| Private CyberAlchemy v2 `cyberAlchemy-v2/authority/constitutions/` | Private candidate authority namespace using `CAV2-*` | Candidate/private; not public Arcanum truth |
| Project-local constitutions under `projects/**` | Local project authority or candidate rules | Do not generalize without owner-routed promotion |
| Runtime `.agents/` / `.claude/` copies | Generated projections | Never edit/promote as canonical source |

Private comparison selectors:

- `implementation/domainspec/AXIOMS.md#axiom-a1-semantic-authority-precedes-implementation` through A6.
- `implementation/domainspec/CONSTITUTION.md#rule-catalog` and `#derivation-chain-l4---l3---l6`.
- `cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md#candidate-kinds`, especially `kind.constitution`, `kind.definition`, `kind.discipline`, `kind.projection`, `kind.evidence`.
- `cyberAlchemy-v2/authority/constitutions/CONSTITUTION-IMPORT-PACK.md#precedence` and `#conflicts-preserved`.
- `cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md#validation-adapters` and `#promotion-boundary`.

These were used only to label namespaces and non-collapse boundaries.

### 4. Constitution versus adjacent concepts

| Concept | Distinguishing role | Constitution relationship |
|---|---|---|
| Axiom | Epistemic/foundational premise explaining why rules should exist | May justify a constitution rule, but public Arcanum Constitution Governance does not require axiom derivation. The Axiom→Constitution→Gate chain is private DomainSpec practice. |
| Definition | Owns stable meaning and vocabulary | A constitution uses terms; it must not redefine Arcanum-wide terms. |
| Policy | Broad normative decision or preference | A policy becomes constitution-like only when durable, scoped, selected, rule-shaped, authority-bounded, and linked to validation/review. |
| Schema | Structural form that instances must fit | Can validate shape; cannot by itself establish semantic authority, execution, or promotion. |
| Discipline | Recurring practice and operating habit | May motivate or operationalize a constitution, but does not acquire constitutional force automatically. Gitignore and receipt examples explicitly “harden” disciplines into constitutions. |
| Method | How work proceeds | Constitution constrains artifacts/behavior; method organizes work. |
| Validation | Evidence that a declared rule/check passed | Validator cites/enforces a rule; it does not own or create the rule. |
| Authority | Owner/scope/promotion state determining where a rule counts | A constitution declares an authority boundary, but authority is not earned merely by file presence, registry listing, generation, validation, or Inventory projection. |

### 5. Composition and conflict algorithm

Current normative algorithm:

1. Resolve target task/artifact and classify the request.
2. Gather only applicable constitution sources and validation surfaces.
3. Select by explicit predicates/metadata where available; use path heuristics only as fallback.
4. Build a minimal task-specific composition pack.
5. Sort applicable rules from narrowest to broadest:

   1. task-specific constitution pack;
   2. artifact-type constitution;
   3. domain/capability constitution;
   4. framework constitution;
   5. repository-wide default/fallback heuristic.

6. Preserve every conflict; do not silently apply “newest wins” or “broader wins.”
7. Classify each conflict as `blocker`, `deferrable`, or `local override`.
8. Send blocker conflicts and consequential canonicality/precedence choices to Decision Gate.
9. Bind each selected rule to `deterministic`, `review`, `hybrid`, or `none-yet`.
10. Run named validators and return `pass`, `flag`, or `block`.

Important gap: this algorithm is prose/template-driven. No public composition schema, selector registry, conflict solver, version resolver, or deterministic composition validator was found.

### 6. Versioning, promotion, retirement

Versioning is under-specified:

- The sigil itself has semantic-looking version `0.1.0`.
- The constitution template has `updated_at`, `status`, and `authority_level`, but no `version` field.
- Existing framework constitutions use inconsistent metadata: frontmatter, prose headers, or no explicit status/owner at all.
- “Newest wins” is explicitly rejected, but no replacement version-selection algorithm exists.
- `supersedes` exists only as candidate artifact metadata.

Promotion is better specified:

1. classify source/evidence;
2. resolve exact canonical owner;
3. select the smallest durable claim;
4. frame a promotion patch;
5. normalize to target voice;
6. run the owner gate;
7. validate target;
8. sync indexes/registries/generated surfaces only as required;
9. record result and residue.

For constitutions, the owner gate is Constitution Governance; consequential authority choices route to Decision Gate. Validation is necessary but not sufficient.

Retirement is weakly implemented:

- Template requires split and retirement triggers.
- Individual constitutions state local triggers.
- No retirement command behavior, registry state transition, archival convention, dependency check, supersession validator, or retirement receipt was found.
- `authority_level` permits `deprecated`, but there is no enforced state machine.

### 7. Actually enforced validation

Executed from the `arcanum` submodule root:

- `bash tools/validate-artifact-constitution.sh --self-test` → pass.
- `python3 tools/validate-artifact-metadata.py --self-test` → pass.
- `python3 tools/validate-receipt-legend.py --self-test` → pass.
- `bash tools/check_markdown_links.sh framework/MARKDOWN-LINKING-CONSTITUTION.md --check-anchors` → pass.
- Full `bash tools/validate-artifact-constitution.sh` → fail on current working tree, with 20 listed untracked/new `.schema.json` failures and 241 total warnings (25 displayed plus 216 omitted).

The parent-root invocation of `arcanum/tools/validate-artifact-constitution.sh --self-test` fails because the script resolves the outer Git root and invokes `tools/check_markdown_links.sh`; this is an invocation-context limitation. The documented command is valid only from the Arcanum repository root.

Deterministic coverage actually witnessed:

- generated/local-runtime path and ignore classification;
- chart/visual literal `\n` detection;
- new schema extension enforcement;
- schema-Markdown companion/noncanonical boundary;
- Markdown local link and anchor existence;
- artifact metadata parser fixtures;
- receipt `gloss-on-cite` fixtures.

Not deterministically enforced:

- general constitution structure/template conformance;
- scope or selector correctness;
- composition order/conflict classification;
- authority level;
- owner legitimacy;
- promotion approval;
- retirement/supersession;
- rule examples/non-examples;
- reviewer decisions;
- full metadata-driven selection;
- Gitignore constitution;
- most Markdown relation semantics;
- receipt `define-on-mint`, `no-orphan-cite`, and `bulk-legend`.

### 8. Contradictions and drift

1. **Metadata example contradicts live source.**  
   `ARTIFACT-METADATA-CONSTITUTION.md#examples` says `SCHEMA-CONSTITUTION.md` declares artifact metadata, selectors, and validation profile. The live Schema Constitution has only prose `Status/Date/Owner`; it has no such frontmatter.

2. **Artifact Constitution lacks its own declared governance metadata.**  
   It contains no explicit top-level status, date, owner, constitution ID, authority level, or version, despite governing classification and promotion.

3. **Template/live-shape divergence.**  
   Only Markdown Linking substantially follows the constitution template/frontmatter shape. Other framework constitutions use reduced prose headers or no header metadata.

4. **Metadata validator exists, but advertised end-to-end selection does not.**  
   The candidate constitution still correctly calls the parser/profile mapping future work. A passing parser self-test must not be inflated into constitution selection enforcement.

5. **Full validator currently blocks the dirty Arcanum tree.**  
   New `.schema.json` files conflict with canonical `schema.format.yml`. This is current validation evidence, not proof those unrelated changes should be altered.

6. **Installed projection hashes differ from canonical.**  
   Canonical SHA-256: `2ba2d5...`; Codex projection: `d534b2...`; Claude projection: `6b26d9...`. Codex differs only by generated-runtime frontmatter. Claude additionally translates tool names and introduces formatting whitespace. Therefore byte parity is neither expected nor an authority test; semantic generation parity requires a dedicated validator, which this lane did not find.

7. **No formal public definition of “constitution.”**  
   `arcanum/definitions/DEFINITIONS.md` formally defines schema, development artifact, canonical artifact, and promotion patch, but not constitution or axiom. Constitution is defined operationally in the sigil README/SKILL.

8. **No public axiom layer.**  
   Axiom-to-rule derivation is demonstrable in private DomainSpec, not established as public Arcanum’s required model.

### 9. Direct history

Observed Arcanum history:

- `4106e52` (2026-06-01), “Add constitution governance and schema validation”: introduced the sigil, templates, Schema Constitution, Artifact Metadata Constitution, validator expansion, and registry entry.
- `7de3fd3` (2026-06-08): added Markdown Linking Constitution, definitions index, and link checker.
- `1ed2afb` / `adbac67` / `7b9b3df` / `a10f209` (2026-06-11 through 2026-06-21): introduced discipline surface, Gitignore/receipt constitution coupling, and receipt validator.
- `0490dbc` (2026-06-25): added canonical promotion vocabulary and Development-to-Canonical Promotion.

History supports an incremental family assembled around concrete validator needs, not a completed unified constitutional runtime.

### 10. Residue

- `constitution` and `axiom` lack formal public definition IDs.
- No constitution catalog distinct from filesystem/registry discovery.
- No schema for constitutions or composition packs.
- No deterministic composition/conflict/precedence engine.
- No version-selection or compatibility policy.
- No executable promotion/retirement state machine or receipt.
- No general rule-to-validator coverage registry.
- Metadata adoption is inconsistent across current framework constitutions.
- Artifact Constitution’s own status/owner is ambiguous.
- Current working tree fails the canonical schema-format validator.
- Invocation assumes execution from Arcanum’s Git root.
- Generated runtime projection semantic-parity validation remains unproven.
- Private/project constitutions demonstrate additional models but cannot be promoted into public Arcanum by comparison.

```json
{
  "ACTION_RECEIPT": {
    "action_id": "spawn-0001",
    "assigned_identity": "Alexander, Christopher",
    "role_id": "explorer-constitution",
    "status": "complete",
    "validation": {
      "proof_contract": "exact-binding",
      "mutation_policy": "read-only",
      "self_tests": {
        "artifact_constitution": "pass from arcanum submodule root",
        "artifact_metadata": "pass",
        "receipt_legend": "pass",
        "markdown_links": "pass"
      },
      "full_artifact_constitution_validation": "fail on current dirty tree: new non-YML schema artifacts; warnings also present",
      "proof_ceiling": "observed canonical sources plus executed bounded validators; no authority or promotion claim"
    },
    "blockers": [],
    "artifacts": [
      "native-return:/root/structural_constitution_explorer"
    ],
    "residue": [
      "no-formal-public-constitution-definition",
      "no-public-axiom-layer",
      "no-composition-schema-or-engine",
      "no-version-resolution-policy",
      "no-executable-retirement-state-machine",
      "inconsistent-constitution-metadata",
      "artifact-constitution-owner-status-implicit",
      "current-full-validator-failure",
      "submodule-root-invocation-dependency",
      "generated-projection-semantic-parity-unverified"
    ],
    "reroute": "synthesizer"
  }
}
```

## Beer, Stafford — Discipline and Practice Lane

## Discipline governance: exact-binding research return

Scope read: persisted `spawn-0002` action; dispatch agent-1 prompt; strategy inventory packet; research dispatch contract; direct public `arcanum/arcana/discipline-governance`, `arcanum/disciplines`, cited discipline-development records, direct constitution/lifecycle comparators, and direct `arcanum` history. No files were changed.

### Finding

A discipline is a public, source-level description of a recurring cross-capability way of working. It owns its card, catalog row, evidence/routing note, and maturity status—not the executable behavior, canonical term, constitution, or capability it references.

The implemented deterministic surface is much narrower: `validate-discipline-catalog.py` checks only the catalog’s six-column table, ID/status syntax, and local evidence-link existence. It does not parse cards, validate them against `discipline.schema.yml`, check card/catalog parity, enforce the Growth Rule, verify cross-capability recurrence, verify a cited validator, or enact promotion/deprecation.

### Catalog / taxonomy

Direct catalog: `arcanum/disciplines/DISCIPLINES.md#catalog`; validator execution observed:

```text
VALIDATION=pass
CATALOG=disciplines/DISCIPLINES.md
DISCIPLINE_COUNT=25
```

| Status | Count | IDs |
|---|---:|---|
| canonical | 4 | `schema`, `artifact-constitution`, `quality-bar`, `validation-experiment` |
| implemented | 1 | `observability` |
| active-pattern | 11 | `planning`, `dispatch`, `context-selection`, `evidence-inventory`, `definition-governance`, `decision-gating`, `interview`, `research-evidence`, `runtime-boundary`, `development-package-promotion-gate`, `two-lane-dialectic` |
| candidate | 8 | `craft`, `ontology`, `residuality`, `distillation`, `ux-evidence`, `gitignore`, `receipt-id-legend`, `two-lane-representation` |
| deprecated | 1 | `implementation-readiness` → `planning` |

All 25 catalog IDs have a corresponding card under `arcanum/disciplines/cards/`, but this parity is a manual observation; the validator does not establish it.

The cards share the template’s documentation structure: purpose, non-owner boundary, evidence links, stated validation, quality bar, and promotion guardrail. Exact template: `arcanum/disciplines/templates/discipline-card.md#discipline-name`.

### Boundary matrix

| Object | Semantic / mutation owner | What it does | What it cannot establish |
|---|---|---|---|
| Discipline card and catalog | `discipline-governance` | Name recurring practice; gather evidence; state boundary/status; choose hardening route | Enforce a capability, define canonical terms, promote a sigil/spell/registry/ontology/glossary |
| Constitution | `constitution-governance` | Own modular structural/form law, rule selection/composition, validation modes | Be replaced by a discipline card; selection itself is not enforcement |
| Validator | Rule owner plus `tools/` | Check a bounded, implemented rule | Supply semantic authority absent an owned rule |
| Sigil/spell | `sigil-development` / `spellcraft` | Execute lifecycle behavior | Be promoted merely because a discipline recommends it |
| Definition | `definitions-governance` | Own canonical vocabulary | Be defined or renamed from a discipline card |
| Inventory/context evidence | Their named owners | Supply/retrieve source-backed leads | Become authority simply through cataloging |

Bindings: `arcanum/arcana/discipline-governance/SKILL.md#chain-boundary`, `#routing-model`; `arcanum/disciplines/README.md#boundary`; `arcanum/arcana/constitution-governance/SKILL.md#validation-model`; `arcanum/framework/ARTIFACT-CONSTITUTION.md#promotion-boundary-rules`; `arcanum/definitions/DEFINITIONS.md#def-arc-canonical-artifact`.

### Exact operating traces and current proof

1. **Discover / propose**
   - Declared trace: `scan` → concrete recurrence evidence → `public-safe` or `private-parent` plus target catalog → candidate.
   - Owner: Discipline Governance.
   - Public/private guard: consuming-repository evidence is local-first; private-parent practices must not enter public catalog.
   - Sources: `arcanum/arcana/discipline-governance/SKILL.md#modes`, `#process` steps 1–3; `arcanum/arcana/discipline-governance/development/CURATION-RUN-2026-06-21.md#part-a-scan-over-the-private-umbrella-root`.
   - Proof: historical documentation and a reported scan/curation run, not a present executable scan command.

2. **Formalize**
   - Declared trace: create card from template + add row, default `candidate`; then validate.
   - Sources: `SKILL.md#process` step 4; `#default-output`; `disciplines/templates/discipline-card.md`.
   - Proof: historical worked examples (`gitignore`, `receipt-id-legend`) are documented in `development/EXPERIMENT-HARNESS-REPORT.md#regime-set`; no direct formalize runner exists in inspected sources.

3. **Route / compose**
   - Declared smallest hardening route: catalog-only, template, validator, constitution, spell, or sigil; each names a separate owner.
   - Sources: `SKILL.md#routing-model`, `#process` step 5.
   - Proof: route taxonomy is observed prose. No discipline-card composition algorithm, composition artifact, or route resolver is provided. Constitution composition is separately owned by `constitution-governance`, not this layer.

4. **Validate**
   - Declared: catalog validator plus a card/schema check; active-pattern-or-higher requires evidence outside its owning sigil.
   - Actual executable: `arcanum/disciplines/scripts/validate-discipline-catalog.py#main`.
   - Observed execution: pass, 25 rows.
   - Gap: the script reads only `DISCIPLINES.md`; `discipline.schema.yml` is never loaded. Thus its schema/card/cross-sigil claims are not enforced by this validator.
   - Schema is explicitly candidate: `arcanum/disciplines/discipline.schema.yml#description`.

5. **Promote / deprecate**
   - Declared promotion guard: owner + evidence + validation surface + mutation boundary; blocker decisions route through `decision-gate`.
   - Declared retirement: mark `deprecated`, state rationale and superseding route.
   - Sources: `SKILL.md#process` steps 7–8; `#discipline-model`; `DISCIPLINES.md#growth-rule`.
   - Observed historical deprecation/merge: `implementation-readiness` → `planning`, retained for provenance, in `CURATION-RUN-2026-06-21.md#part-b-validate--deprecate-curation-over-arcanums-22` and `cards/implementation-readiness.md#purpose`.
   - Proof ceiling: no promotion/deprecation receipt schema, status-transition validator, or current promotion command was found in the direct sources.

### Representative exact card findings

- `cards/schema.md#validation` correctly routes canonical schema form to `framework/SCHEMA-CONSTITUTION.md#rules` and `tools/validate-artifact-constitution.sh`; the discipline card does not itself enforce it.
- `cards/receipt-id-legend.md#validation` has a real additional deterministic validator, `tools/validate-receipt-legend.py`; it remains `candidate` because its own stated broader promotion requirements remain unfinished.
- `cards/distillation.md#status` and `cards/residuality.md#status` preserve a curation downgrade from active-pattern because their evidence was only their owning sigil; this is an honest thin-pointer diagnosis.
- `cards/two-lane-dialectic.md#boundary` distinguishes opposed-lane investigation from `cards/two-lane-representation.md#boundary`’s human-prose/machine-structure invariant. They are not a direct duplicate, though both rely on prose review only.
- `cards/development-package-promotion-gate.md#boundary` is unusually owner-explicit and local-first, but its stated validation is still catalog validation plus human changed-file review.

### Drift / duplication / authority findings

1. **Schema-validation gap — observed, reproducible.** The schema declares required fields and `additionalProperties: false`, but Markdown cards do not instantiate that YAML/JSON object, and the sole catalog validator never opens any card or schema. “Check a card against the discipline schema” is currently a process claim, not an executable route.

2. **Growth Rule is advisory — observed.** No inspected validator verifies named owner/evidence/validation/mutation boundary before a status edit. Catalog status is syntactic only.

3. **Active-pattern cross-capability test is not enforced.** `SKILL.md#validation-model` promises a flag for own-sigil-only evidence, yet script behavior has no card parsing/evidence ownership logic. The 2026-06-21 curation is valuable historical manual evidence, not a standing control.

4. **Cards are documentation, not duplicate executable skills.** They mostly summarize owner capabilities and route away from mutation. This is deliberate and generally bounded. Duplication risk is “thin one-per-sigil pointer,” which the curation explicitly found for ontology, distillation, and residuality. The catalog/card layer still duplicates short capability descriptions by design; it does not duplicate executable implementation.

5. **`quality-bar` canonical backing needs tighter binding.** The card/catalog call it canonical and describe constitution support, while `framework/QUALITY-BAR.md` is a framework guidance document with no explicit status/owner/validator declaration like `SCHEMA-CONSTITUTION.md`. Curation calls its backing a “Quality Bar constitution.” Treat the discipline’s canonical claim as owner-backed prose unless a more direct constitutional selector is supplied.

6. **Historical claims must remain historical.** `EXPERIMENT-HARNESS-REPORT.md` reports v0.2.0 promotion and documents telemetry/reflection; later `SKILL.md` reports v0.2.2. These establish a history and declared lifecycle, not a newly executed lifecycle result in this run.

7. **Working tree residue is outside this lane.** `git -C arcanum status --short` shows extensive existing modifications/untracked files in other Arcana/spell areas; none touch the inspected discipline catalog/sigil sources, and none were authored or validated here.

### History / direct ownership

- Initial layer: `1ed2afb Add Arcanum disciplines framework surface`.
- Lifecycle sigil added/formalization: `adbac67`.
- 2026-06-21 curation and receipt legend: `7b9b3df`.
- v0.2.1 and receipt validator: `a10f209`.
- local-first promotion policy: `89f9a96`.
- latest discipline additions: `bd2c91c` adds both two-lane cards.

No private source was used as public Arcanum authority.

```json
{
  "ACTION_RECEIPT": {
    "action_id": "spawn-0002",
    "assigned_identity": "Beer, Stafford",
    "role_id": "explorer-discipline",
    "status": "complete",
    "validation": {
      "catalog_validator": {
        "command": "python3 arcanum/disciplines/scripts/validate-discipline-catalog.py",
        "result": "pass",
        "discipline_count": 25
      },
      "exact_binding": "direct public sources, direct history, and executed catalog validator inspected"
    },
    "blockers": [],
    "artifacts": {
      "native_return_handle": "spawn-0002/explorer-discipline/complete"
    },
    "residue": [
      "discipline.schema.yml is not consumed by catalog validator",
      "card/catalog parity and Growth Rule are not machine-enforced",
      "active-pattern cross-sigil evidence rule is prose-only in inspected validator",
      "no finite executable promote/deprecate or composition route found",
      "quality-bar canonical backing requires a more direct constitutional binding"
    ],
    "reroute": [
      "discipline-governance for card/catalog and route-status changes",
      "constitution-governance for structural-law hardening",
      "definitions-governance for canonical terms",
      "sigil-development or spellcraft for executable capability lifecycle",
      "decision-gate for blocker-level status or scope decisions"
    ]
  }
}
```

## Simon, Herbert — Structural Lifecycle and Enforcement Lane

## Structural lifecycle finding

Arcanum has distinct semantic, lifecycle, validation, projection, execution, and evidence surfaces. They form a usable chain, but they are not one authority system:

1. Canonical source defines the durable contract.
2. The artifact-specific lifecycle owner decides how that source may change.
3. Validators test declared rules; they do not create those rules.
4. Promotion applies the smallest reviewed change to canonical source.
5. Registries and generated packages are synchronized projections.
6. Installed runtime packages execute the projected contract.
7. Telemetry, experiments, receipts, Inventory, and ontology provide evidence/read models only.

The strongest reproducible defect is current source/runtime drift: canonical `discipline-governance` is version `0.2.2` with local-first routing, while both generated native packages remain `0.2.1`.

## Surface classification

| Surface | Classification | Exact binding | Evidence ceiling |
|---|---|---|---|
| Canonical definitions | semantic owner | `arcanum/definitions/DEFINITIONS.md`; Definitions Governance resolves this at `arcanum/arcana/definitions-governance/SKILL.md:40-63,102-109` | Canonical public Arcanum semantics |
| Definitions Governance | process owner | `arcanum/arcana/definitions-governance/SKILL.md:66-99` | Maintains authority; is not itself the definitions authority |
| Constitution files | semantic/rule owners for their scopes | `arcanum/framework/*-CONSTITUTION.md`; routing and precedence at `arcanum/arcana/constitution-governance/SKILL.md:68-72,75-113,119-130` | Rule authority is constitution-specific |
| Constitution Governance | process owner and promotion gate | `arcanum/arcana/constitution-governance/SKILL.md:23-29,75-113,135-144` | Owns lifecycle, composition, validator mapping, and promotion preparation |
| Constitution validators | validators | `arcanum/tools/validate-artifact-constitution.sh`; other constitution-specific tools | Enforcement evidence, not rule authority |
| Discipline catalog/cards | method-level semantic/catalog owner | `arcanum/disciplines/README.md:5-33`; `DISCIPLINES.md:6-17`; cards under `disciplines/cards/` | Own recurring-practice descriptions, not capability contracts |
| Discipline Governance | process owner and discipline-status gate | `arcanum/arcana/discipline-governance/SKILL.md:65-75,95-110,113-150` | Cannot promote sigils, spells, definitions, ontology, or registry knowledge |
| Discipline schema | candidate structural specification | `arcanum/disciplines/discipline.schema.yml:1-73` | Describes future machine-readable cards; Markdown cards are not comprehensively schema-validated |
| Discipline catalog validator | validator | `arcanum/disciplines/scripts/validate-discipline-catalog.py:14-80` | Checks catalog columns, statuses, rows, and local links; not full card semantics |
| Sigil canonical package | capability semantic owner | `<formulae|transmutations|arcana>/<id>/SKILL.md`; lifecycle at `arcanum/arcana/sigil-development/SKILL.md:97-160` | Canonical reusable capability contract |
| Sigil Development | lifecycle/process owner and promotion-readiness gate | `arcanum/arcana/sigil-development/SKILL.md:55-73,133-160,207-220` | Consumes runtime and experiment evidence; does not turn evidence into authority automatically |
| Spell canonical contract | composition semantic owner | `arcanum/spells/<id>/README.md`; spell boundary at `arcanum/spells/README.md:39-61` | Owns composition, never constituent sigil internals |
| Spellcraft | lifecycle/process owner and promotion-readiness gate | `arcanum/arcana/spellcraft/SKILL.md:92-139,141-163,181-194` | Owns spell lifecycle, installation/adaptation, validation, observation, reflection |
| Development-to-canonical process | cross-artifact promotion protocol | `arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md:19-84` | Process contract; target lifecycle owner still decides |
| Sigil/spell Markdown registries | runtime lookup projection | `arcanum/registry/SIGILS.md`, `arcanum/registry/SPELLS.md`; boundary at `arcanum/README.md:171-177` | Registry presence is discoverability, not authority or proof |
| Web/download registry | generated runtime projection | `arcanum/tools/build-skill-registry.py:2-10,94-102,323-345,411-413` | Generated from manifests; never hand-edited |
| Generated Codex/Claude packages | runtime projection | `.agents/skills/<id>/`, `.claude/skills/<id>/`; generated headers name canonical source and regeneration policy | Executable copies, explicitly non-canonical |
| Targeted package synchronizer | projection/parity mechanism | `arcanum/tools/sync-generated-skill-package.sh:106-130,136-165,168-229` | Stages through Bootstrap and checksum-syncs one package; only `--apply` mutates |
| Bootstrap/installer | runtime installation projection | `arcanum/tools/bootstrap_arcanum.sh`; `arcanum/tools/install_arcanum.sh` | Installs/adapts canonical packages; installation is not promotion |
| Dispatch Spec | route validator | `arcanum/formulae/dispatch-spec/SKILL.md:55-101,103-146` | Validates executable dispatch shape; does not execute or grant artifact promotion |
| Orchestrate | process owner for native dispatch execution | `.agents/skills/orchestrate/SKILL.md:59-70,79-105,108-143` | Owns preflight, scheduling, joins, gates, closeout; humans/lifecycle owners retain promotion authority |
| Experiment Harness | evidence producer | `arcanum/arcana/experiment-harness/SKILL.md:15-19,53-59,76-88,127-142` | Reusable-behavior evidence, not promotion |
| Signal Observer | evidence producer | `arcanum/arcana/signal-observer/SKILL.md:15-19,65-90,103-126` | Appends signals/counters only; non-blocking by default |
| Workflow Reflect | evidence producer and proposal process | `arcanum/arcana/workflow-reflect/SKILL.md:61-129` | Produces proposals/reports; cannot modify observed capability without separate maintenance authority |
| Inventory, ontology, telemetry, receipts, tests | non-authority read models/evidence | Dispatch Spec explicitly bars direct promotion at `arcanum/formulae/dispatch-spec/SKILL.md:75-86` | May discover, validate, or support a decision; cannot own it |

## Finite lifecycle traces

### Add or revise a constitution

1. Identify whether the proposed rule is reusable structure/form rather than a definition, discipline, task note, or already-complete deterministic check.
2. Invoke Constitution Governance in `create`, `add-rule`, `split`, or `promote` mode.
3. Draft under `arcana/constitution-governance/development/` until accepted; canonical framework destination is `framework/<NAME>-CONSTITUTION.md` (`constitution-governance:68-72`).
4. Declare scope, owner, authority level, selectors, examples/non-examples, validation mode, adapter, and promotion boundary (`:84-97`).
5. Compose with narrower constitutions first: task-specific → artifact type → domain/capability → framework → repository default (`:119-123`).
6. Preserve conflicts and route blocker precedence/canonicality decisions through Decision Gate (`:111,127-130`).
7. Add or revise a validator only within the constitution’s scope; validator remains enforcement, not authority (`:135-170`).
8. Apply a reviewed promotion patch using the target owner, evidence, rationale, validation, and approval state (`DEVELOPMENT-TO-CANONICAL-PROMOTION.md:28-84`).
9. Synchronize dependent indexes/generated surfaces only after canonical mutation.

### Add or revise a discipline

1. Establish recurrence, scattered rules, drift, rework, or confusion from concrete evidence.
2. Tag the candidate `public-safe` or `private-parent`; consuming-repository practice is local-first (`discipline-governance:77-83,95-99`).
3. Create/update `disciplines/cards/<id>.md` and one row in `disciplines/DISCIPLINES.md`; default new status is `candidate` (`:85-100`).
4. Choose the smallest hardening route: catalog-only, template, validator, constitution, sigil, or spell (`:100-105,127-138`).
5. Run the catalog validator and inspect the card against the candidate schema; a claimed validator must exist (`:106,141-150`).
6. Promote status only when owner, evidence, validation surface, and mutation boundary are named (`:107,113-124`).
7. Deprecation marks `deprecated`, cites rationale, and names the superseding route (`:108`).
8. Any constitution/sigil/spell change is a separate handoff to its lifecycle owner.

### Add or revise a sigil

1. Invoke may define/design/plan and provide a handoff, but Sigil Development takes lifecycle ownership (`sigil-development:55-60`).
2. Select tier and create/revise the canonical `<tier>/<id>/SKILL.md`; keep planning and experiments under `<tier>/<id>/development/` (`:97-117,133-145`).
3. Define the human-facing contract, machine-facing skill contract, quality bar, anti-patterns, and output.
4. Initialize/preserve low, medium, and complex Experiment Harness regimes (`:139-145`).
5. Task Session executes one approved SWU; any Codex Goal/runtime lane returns execution evidence only (`:62-94`).
6. Experiment Harness supplies reusable-behavior evidence.
7. Signal Observer emits telemetry; Workflow Reflect proposes changes; neither edits authority by itself (`:146-159`).
8. Sigil Development reviews execution, experiment, observability, and reflection evidence and decides lifecycle progress.
9. Apply the smallest promotion patch to canonical source.
10. Update `registry/SIGILS.md`, then regenerate `.agents/skills/<id>/`, `.claude/skills/<id>/`, and downloadable/web projections.
11. Verify source/projection parity; installation does not close the lifecycle.

### Add or revise a spell

1. Invoke may prepare definition/design/plan/handoff; Spellcraft owns composition lifecycle (`arcanum/spells/README.md:59-61`).
2. Resolve stable canonical ID and aliases; ambiguous aliases block (`spellcraft:92-100`).
3. Draft reusable source at `spells/<id>/README.md`, with development evidence under `spells/<id>/development/`; repository-local adaptation belongs under `.arcanum/spells/<id>/README.md` (`:78-90`).
4. Declare required/optional sigils, phases, inputs, outputs, shared state, gates, handoffs, and failure policy (`:109-119,141-158`).
5. Preserve sigil ownership: the spell references, never redefines, sigil contracts (`:161-163`).
6. Task Session executes bounded implementation/adaptation SWUs; runtime receipts are execution evidence only (`:50-75`).
7. Experiment Harness validates reusable composition; observe and reflect separately (`:121-138`).
8. Spellcraft decides lifecycle readiness.
9. Apply a promotion patch to canonical spell source.
10. Update `registry/SPELLS.md`, synchronize generated packages, and verify parity.

## Integration with Invoke, Task Session, and Craft

The structural lifecycle extends the existing build protocol without replacing its owners:

```text
Invoke
  defines/designs/plans and emits a lifecycle handoff
        ↓
Sigil Development / Spellcraft / Constitution Governance / Discipline Governance
  owns the artifact-specific lifecycle and promotion decision
        ↓
Task Session
  executes exactly one admitted task or SWU and returns bounded evidence
        ↓
Craft
  tracks/stages approved work-graph deltas where the route uses Craft
        ↓
Experiment Harness → Signal Observer → Workflow Reflect
  proves behavior, records signals, proposes maintenance
        ↓
Lifecycle owner
  reviews evidence and frames the smallest promotion patch
        ↓
Canonical source
        ↓
registry/index/generated package/install projections
```

Bindings:

- Invoke explicitly says its handoff is context only and routes sigil/spell mutation to the lifecycle owners: `arcanum/spells/invoke/plan.md:83-85` and `handoff.md:60-64`.
- Task Session does not acquire lifecycle or promotion authority from execution: `arcanum/arcana/task-session/SKILL.md:295-302,418-420`.
- Sigil Development’s concrete closure loop is `sigil-development/SKILL.md:62-94`; Spellcraft’s equivalent is `spellcraft/SKILL.md:45-75`.
- Dispatch Spec validates route shape; Orchestrate executes admitted native actions; neither replaces the target lifecycle owner.
- Craft ledger/projection state is coordination state. It cannot promote canonical source merely because a delta or receipt exists.

## Executed proof

Executed read-only checks:

- `python3 arcanum/disciplines/scripts/validate-discipline-catalog.py`
  - `VALIDATION=pass`
  - `DISCIPLINE_COUNT=25`
- From the public Arcanum root: `./tools/validate-artifact-constitution.sh`
  - failed with 19 current new-schema `.schema.json` violations
  - emitted 216 additional warnings before truncation
- Byte comparisons between canonical `SKILL.md` files and `.agents`/`.claude` projections:
  - every raw comparison differs because generated packages intentionally add runtime metadata
  - substantive diff confirmed for `discipline-governance`: canonical `0.2.2` local-first behavior versus generated `0.2.1`
- Direct history:
  - latest located synchronization history is July 19–30 (`3954dccc`, `581edcfe`, `9d4a90d9`, `9ce797f2`, `7a81c519`)
  - discipline-governance’s located mirror commit is `4d05ee0d` from 2026-06-21

Everything else above is source-observed contract behavior, not a claim that a complete constitution, discipline, sigil, or spell promotion was executed.

## Reproducible residue

1. **Generated discipline runtime drift**
   - Canonical: `arcanum/arcana/discipline-governance/SKILL.md`, version `0.2.2`, local-first routing.
   - Generated: `.agents/skills/discipline-governance/SKILL.md` and `.claude/skills/discipline-governance/SKILL.md`, version `0.2.1`.
   - Reproduce:
     `diff -u arcanum/arcana/discipline-governance/SKILL.md .agents/skills/discipline-governance/SKILL.md`
   - Effect: installed/native agents can omit the newer consuming-repository boundary.

2. **Artifact Constitution currently blocks**
   - Reproduce from `arcanum/`: `./tools/validate-artifact-constitution.sh`.
   - Current failures include new `.schema.json` artifacts under continuation-router, task-session, implementation-readiness, task-session-until-blocker, work-pack-readiness-audit, and a research evidence package.
   - This is validation failure evidence, not proof that those artifacts are semantically invalid.

3. **Discipline validation is narrower than lifecycle prose**
   - The live catalog validator passes 25 rows, but it does not prove every Markdown card conforms to the candidate machine-readable schema or the `active-pattern` cross-sigil evidence rule.
   - The lifecycle contract says both should be checked; deterministic enforcement covers primarily catalog structure/local links.

4. **Raw byte parity is not a valid generated-package test**
   - Generated packages intentionally add canonical-source/runtime metadata and may adapt tool names.
   - Parity must distinguish permitted generation transforms from stale semantic content. The targeted synchronizer supplies checksum staging, but no single checked-in semantic-parity receipt was found for all inspected packages.

5. **Global artifact validator has invocation-root sensitivity**
   - Running `arcanum/tools/validate-artifact-constitution.sh` from the parent repository produced false “missing constitution/tool” failures because it expects the Arcanum repository root.
   - Running it from `arcanum/` resolves those path failures and exposes the actual schema violations.
   - Its command contract should name or enforce the required working directory.

6. **Promotion remains partly review-bound**
   - Constitution rules can declare `review`, `hybrid`, or `none-yet`; discipline cards can use `prose-review` or `observability`.
   - Therefore a passing catalog, registry, generated package, test, or receipt cannot independently establish promotion.

```json
{
  "ACTION_RECEIPT": {
    "action_id": "spawn-0003",
    "assigned_identity": "Simon, Herbert",
    "role_id": "explorer-lifecycle",
    "status": "completed",
    "validation": {
      "contract": "exact-binding",
      "source_trace": "pass",
      "discipline_catalog": "pass; 25 rows",
      "artifact_constitution": "fail; 19 current schema-format failures and 216 warnings",
      "runtime_parity": "flag; discipline-governance canonical 0.2.2 versus generated 0.2.1",
      "mutation": "none"
    },
    "blockers": [],
    "artifacts": [
      "native-return:spawn-0003"
    ],
    "residue": [
      "discipline-governance-generated-runtime-drift",
      "artifact-constitution-schema-format-failures",
      "discipline-card-semantic-validation-gap",
      "generated-package-semantic-parity-check-gap",
      "artifact-validator-working-directory-sensitivity",
      "review-bound-promotion-surfaces"
    ],
    "reroute": {
      "owner": "parent strategist",
      "next": "evidence closure and synthesis",
      "authority_effect": "none"
    }
  }
}
```
