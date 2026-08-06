Definitional-soundness verdict: **FLAG**

The synthesis preserves many correct boundaries, but its retained model still collapses categories that have different owners, states, artifacts, and legal effects.

### Claim dispositions

- **FLAG — SG-STACK-01 / SG-VOC-02 / SG-OWN-01.**  
  `arcanum/definitions/DEFINITIONS.md#authority-rule` governs only Arcanum-wide terms the file actually contains. “Says what a public Arcanum term means” overstates coverage. Constitution, axiom, policy, discipline, method, process, validator, sigil, spell, lifecycle, registry, installation, receipt, Inventory, ontology, telemetry, Craft, and authority lack formal public definition IDs.  
  **Repair:** say “owns normative semantics for terms it contains”; classify all other meanings as operational/local until Definitions Governance accepts them.

- **FLAG — SG-STACK-06.**  
  “Schema / validator” is an impermissible combined category. A schema is a structural representation (`arcanum/definitions/DEFINITIONS.md#def-arc-schema-schema`); a validator is an executable checker governed by the rule owner (`arcanum/arcana/constitution-governance/SKILL.md#validation-model`).  
  **Repair:** create separate schema and validator rows, each with artifact, owner, validation scope, and evidence ceiling.

- **FLAG — SG-STACK-07 / SG-VOC-10 / SG-LIFE-01–04.**  
  “Lifecycle / promotion” collapses governance activity with a specific authority-changing transition. The promotion process frames a patch and runs an owner gate, while Constitution Governance’s `promote` mode only “prepare[s]” adoption (`arcanum/framework/DEVELOPMENT-TO-CANONICAL-PROMOTION.md#process`; `arcanum/arcana/constitution-governance/SKILL.md#modes`). The accepting actor, approval artifact, and exact before/after state are not uniformly defined.  
  **Repair:** distinguish lifecycle, promotion proposal, owner decision, canonical mutation, and projection synchronization. Mark the transition protocol review-bound until each artifact family names approver, approval evidence, source/target state, and rejection behavior.

- **FLAG — SG-STACK-08 / SG-VOC-08 / SG-VOC-11 / SG-ENF-05–07.**  
  Registry, generated skill, installation, and runtime are four distinct categories. A registry is a discoverability catalog (`arcanum/README.md#registry`); generation creates transformed projections; sync copies a selected package from a resolved canonical source (`arcanum/tools/sync-generated-skill-package.sh:106`); installation changes availability; runtime execution yields behavioral evidence.  
  **Repair:** split all four and forbid the transitions `registered → canonical`, `generated → semantically equivalent`, `installed → accepted`, and `executed → promoted` without their separate gates.

- **FLAG — SG-STACK-09 / SG-VOC-09 / SG-OWN-08 / SG-BUILD-03.**  
  Receipt, Inventory, ontology, telemetry, and Craft are not one “evidence/read-model” category. Inventory owns compiled evidence cards and read-model projections (`arcanum/arcana/inventory/SKILL.md#source-and-authority-boundary`). Ontology Vault governs ontology meaning, relations, confidence, and conventions, although its run outputs cannot themselves promote or mutate source (`arcanum/arcana/ontology-vault/SKILL.md#project-runtime-profile-arguments`, process steps 24–26). Craft explicitly says an existing ledger is authoritative within its scope for contexts, blockers, decisions, and gaps (`arcanum/arcana/craft/SKILL.md#process`, step 2), while not rewriting native capability verdicts (`#interaction-boundary`).  
  **Repair:** state authority by scope. “Cannot promote canonical Arcanum source” is defensible; “non-authority coordination/read model” is not.

- **FLAG — SG-VOC-05.**  
  “Method / process” is another undefined combined category. The cited sources describe particular routing and promotion procedures, not a stable distinction between method and process.  
  **Repair:** either define both through Definitions Governance or remove them from the controlled vocabulary and call the cited artifacts named procedures only.

- **FLAG — SG-VOC-03.**  
  Policy is mentioned only as something constitution must remain distinct from; no owner, artifact, state, or transition is supplied. Constitution itself remains operationally described rather than definition-governed.  
  **Repair:** define policy and constitution separately or omit policy from the model. Do not infer that every durable scoped rule is constitutional law.

- **FLAG — SG-STACK-04 / SG-STACK-05 / SG-OWN-04 / SG-OWN-05.**  
  Sigil and spell have usable operational owners, but no formal public definition IDs. Canonical `SKILL.md` and spell `README.md` paths support artifact ownership, not universally governed term semantics.  
  **Repair:** label these operational artifact contracts pending Definitions Governance; do not present the synthesis wording as canonical definitions.

- **FLAG — SG-COMP-01–03.**  
  Precedence is ambiguous. Narrowest-to-broadest ordering is stated, but “explicit selectors outrank path heuristics” and “local override” do not define whether an override defeats the ordering, who may authorize it, or what receipt makes it legal. Decision Gate blocks and records human choices but explicitly leaves promotion and authority hazards with their owning gates (`arcanum/arcana/decision-gate/SKILL.md#authority-rule`).  
  **Repair:** specify applicability selection separately from conflict precedence; define local override issuer, scope, duration, evidence, and non-effects. Do not say Decision Gate itself transfers authority.

- **PASS — SG-OWN-06 / SG-VOC-06 / SG-VOC-07.**  
  Subject to separating their stack row, the schema/validator/authority boundaries match the direct sources.

- **PASS — SG-BUILD-04, with evidence ceiling.**  
  Orchestrate owns preflight, native action scheduling, joins, gates, and closeout, while humans and capability owners retain lifecycle and promotion authority (`.agents/skills/orchestrate/SKILL.md#authority`). The coordinator and evidence validator implement action compilation, exact receipt matching, and gate admission (`.agents/skills/orchestrate/scripts/native_dispatch_coordinator.py:402`; `.agents/skills/orchestrate/scripts/validate_run_evidence.py:260`). This proves coordination mechanics, not artifact authority.

- **PASS — SG-DRIFT-14 / SG-REC-01.**  
  The public definition gap is real. Defining `constitution` is justified; `axiom` should remain private-comparator vocabulary unless Arcanum intentionally adopts it.

- **FLAG — SG-VERDICT-01.**  
  The verdict says schemas and validators and lifecycle and authority are separated, but SG-STACK-06 and SG-STACK-07 still combine them.  
  **Repair:** replace the prose “layer stack” with a typed matrix: category, semantic owner, lifecycle owner, canonical artifact, states, legal transition, emitted evidence, evidence ceiling, and public/private scope.

### Minimum retained transition model

A defensible sequence is:

`candidate evidence → owner-selected claim → promotion proposal → explicit owner decision → canonical source mutation → registry update → generated projection → installation → runtime execution → receipt/telemetry`

None of those arrows is automatic. Inventory, ontology, Craft, and definitions each retain their own scoped authority and cannot be compressed into one evidence bucket.

```json
{
  "ACTION_RECEIPT": {
    "action_id": "spawn-0007",
    "identity": "Quine, Willard Van Orman",
    "role_id": "skeptic-definitional",
    "status": "complete",
    "validation": "flag",
    "blockers": [
      "retained stack collapses categories with different owners and legal effects",
      "promotion transition lacks a uniform accepting actor and typed approval evidence",
      "Craft and Ontology are incorrectly flattened into non-authority read models",
      "several controlled-vocabulary terms lack public definition IDs"
    ],
    "native_return_handle": "native-return:/root/structural_definitional_reviewer",
    "residue": [
      "formal definitions remain owner work",
      "no mutation or promotion performed",
      "implementation inspection was limited to coordinator and evidence-validation claims"
    ],
    "reroute": {
      "next": "synthesis-writer",
      "request": "split collapsed rows, scope authority precisely, and define legal transitions before retaining the structural model"
    }
  }
}
```
