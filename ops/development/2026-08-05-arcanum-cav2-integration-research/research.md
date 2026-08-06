# Research: Arcanum ↔ CyberAlchemy v2 integration

Dispatch: `2026-08-05-arcanum-cav2-integration-research`  
Run: `cav2-integration-run-01`  
Evidence rule: the explorer returns below are preserved verbatim. They are research evidence, not authority, promotion, implementation, deployment, or publication proof.

## Explorer return — authority and lineage

# Explorer report — authority and lineage

Identity: MacIntyre, Alasdair  
Role: `explorer-authority`  
Dispatch: `2026-08-05-arcanum-cav2-integration-research`  
Run: `cav2-integration-run-01`  
Mutation: none

## Verdict

CyberAlchemy v2 is currently a private, project-local authority spine and consolidation surface. It owns its local definitions, constitutions, disciplines, decisions, authority model, import ledgers, promotion policy, ontology candidates, and local boundary decisions. It does not own public Arcanum’s definitions or capabilities, private DomainSpec implementation authority, or a shipped Saturn loop.

The verified Arcanum-to-CAV2 direction is:

```text
public Arcanum owner
  -> cited or staged import candidate
  -> locally adapted rule proposal
  -> narrow CAV2 owner gate
  -> CAV2-local authority, if promoted
```

No verified reverse authority edge exists. CAV2 does not redefine Arcanum for Arcanum, and public Arcanum does not inherit CAV2’s private prose. Inventory, ontology, research, generation, validation, execution, and Git commits cannot perform the owner-gated transition themselves.

The strongest concrete integration precedent—the artifact-governance import—has reached source discovery, a frozen candidate partition, and a non-executed Invoke plan. It has not reached the planned local constitution files, validator port, or hook enforcement described by that plan.

## Stable claims

### AUTH-001 — CAV2 is a private consolidation surface, not yet a standalone repository

- Relationship: CAV2 `references` and selectively `imports` dispersed sources; it does not acquire their authority by proximity.
- Direction: source systems → CAV2 source ledger.
- Narrow owner: CyberAlchemy v2.
- Legal transition: source reference → import candidate → owner-routed local authority.
- Privacy: CAV2 is private; referenced Arcanum material is public; DomainSpec implementation evidence remains private.
- Current state: project start; future standalone candidate.
- Proof:
  - `cyberAlchemy-v2/README.md`, `# CyberAlchemy v2`, lines 3–16.
  - `cyberAlchemy-v2/README.md`, `# Repository Objective`, lines 36–47.
  - `cyberAlchemy-v2/README.md`, `# Current Gate`, lines 119–127.
  - `cyberAlchemy-v2/SOURCE-MAP.md`, `# Source Cohorts`, lines 8–21.
- Proof status: direct current source.
- Non-effects: no extraction, release, deployment, publication, or inheritance of upstream authority.
- Residue: standalone extraction and the broader public-safe slice remain open.

### AUTH-002 — The local authority model is active, but its movements remain owner-routed and partly review-mode

- Relationship: CAV2 authority surfaces `instantiate` locally owned authority kinds; evidence `supplies evidence to` those owners.
- Direction: evidence/candidate → definitions, constitution, discipline, decision, spec, runtime, or projection owner.
- Narrow owner: the owner named per kind; CAV2 authority owner maintains the model.
- Legal transition:
  - definition → `definitions-governance`;
  - constitution → `constitution-governance`;
  - discipline → `discipline-governance`;
  - decision → `decision-gate`;
  - spec → spec owner plus decision gate;
  - runtime contract → owner gates then `task-session`;
  - projection → ontology route plus source owner.
- Privacy: private local authority.
- Current state: authority model active; unenumerated kinds default-deny; kind-enumeration enforcement remains review-mode.
- Proof:
  - `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md`, `# Authority Rule`, lines 23–29.
  - Same file, `# Core Flow`, lines 31–46.
  - Same file, `# Authority Kinds`, lines 48–72.
  - Same file, `# Narrowest Owner Rule`, lines 90–103.
- Proof status: direct current source; deterministic closure validator explicitly pending.
- Non-effects: a candidate’s usefulness, repetition, ontology representation, execution, or validation does not grant authority.
- Residue: authority-kind validator and invariant/axiom kind decisions remain open.

### AUTH-003 — Public Arcanum remains the owner of Arcanum vocabulary and portable capability machinery

- Relationship: CAV2 `references`, `imports`, or `adapts` Arcanum material; it does not supersede its public owner.
- Direction: Arcanum public canonical source → CAV2 evidence/import/adaptation.
- Narrow owner:
  - Arcanum definitions → `arcanum/definitions/DEFINITIONS.md` via Arcanum definitions governance.
  - Arcanum constitutions → their framework sources via Constitution Governance.
  - Arcanum disciplines → `arcanum/disciplines/` via Discipline Governance.
  - ontology method → `arcanum/arcana/ontology-vault/`.
- Legal transition: cite/reference for Arcanum scope; stage and locally promote through CAV2 if a CAV2 rule is needed.
- Privacy: public → private is permitted, subject to local admission; private → public is not implied.
- Current state: live public owners exist.
- Proof:
  - `cyberAlchemy-v2/SOURCE-MAP.md`, `# Source Cohorts`, lines 14–18: Arcanum is public canonical only for Arcanum terms and capabilities; private implementation remains private evidence.
  - `arcanum/definitions/DEFINITIONS.md`, `# DEF-ARC-CANONICAL-ARTIFACT`, lines 340–379: canonical authority is scoped to the owning contract.
  - Same file, `# DEF-ARC-PROMOTION-PATCH`, lines 396–435: promotion is a reviewed owner mutation, not copying or committing.
  - `arcanum/arcana/discipline-governance/README.md`, `# Core Stance`, lines 19–21: a discipline names a way of working; it does not execute it.
- Proof status: direct current public source.
- Non-effects: CAV2 terminology cannot silently become Arcanum vocabulary; a CAV2 local rule cannot modify Arcanum authority.

### AUTH-004 — Definitions are referenced, not redefined across the boundary

- Relationship: CAV2 `references` Arcanum definition IDs/sources and may define CAV2-local terms.
- Direction: Arcanum definitions → CAV2 reference; CAV2 definitions → local consumers.
- Narrow owner: Arcanum definitions governance for Arcanum terms; CAV2 definitions governance for `CAV2-D*`.
- Legal transition: an upstream term remains upstream authority; a locally load-bearing term must enter CAV2 definitions through definitions governance.
- Privacy: public source / private local definition split.
- Current state: the definition import ledger is an active ledger but its 2026-06-19 scan is old.
- Proof:
  - `cyberAlchemy-v2/authority/imports/definitions/MANIFEST.md`, `# Purpose`, lines 7–11.
  - Same file, `# Result`, lines 37–43: 149 candidates, candidate-only, canonical destination named.
  - `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md`, `# Authority Kinds`, line 52.
- Proof status: current manifest plus direct owner files.
- Contradiction/staleness: “active import ledger” does not mean the scan is current; its declared scan date is 2026-06-19.
- Non-effects: being listed does not promote any of the 149 sources.

### AUTH-005 — CAV2 constitutions are local rules, not a takeover of public Arcanum constitutions

- Relationship: CAV2 `imports` public patterns and may `adapt` them into project-local rules.
- Direction: public framework constitution → CAV2 import ledger → extracted local constitution proposal → constitution-governance.
- Narrow owner: CAV2 constitution governance for local rules; Arcanum Constitution Governance for public originals.
- Legal transition: import-before-promotion, then local extraction with provenance, scope, owner, examples, non-examples, and validation mode.
- Privacy: public source → private local adaptation.
- Current state: `STABLE-REPOSITORY-CONSTITUTION.md` labels itself candidate and project-local.
- Proof:
  - `cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md`, header, lines 1–10.
  - Same file, `# CAV2-C11. Import Before Promotion`, lines 177–203.
  - Same file, `# Promotion Boundary`, lines 501–505.
  - `cyberAlchemy-v2/authority/promotion-policy.md`, `# Required Gates`, lines 20–29.
- Proof status: direct current source.
- Contradiction: the constitution says “Authority level: project-local constitution” while its status is “candidate.” This supports local scope, but not fully promoted/canonical status.
- Non-effects: candidate rules cannot claim cross-repository authority.

### AUTH-006 — The artifact-governance seam is a verified import/adaptation precedent, but implementation remains unexecuted

- Relationship classes:
  - Arcanum schema and retention patterns → CAV2 `imports`.
  - Arcanum-root-specific validator → CAV2 planned `adaptation`, not copy.
  - Already-owned promotion/non-collapse rules → `forbidden/no verified edge` for duplicate import.
- Direction: Arcanum public framework → CAV2 Tier-1 candidate pack.
- Narrow owners:
  - local constitutions → CAV2 constitution governance;
  - validator port/hook → task session after owner gates;
  - metadata adoption → decision gate;
  - edge vocabulary → ontology/definitions governance.
- Legal transition:
  1. stage in import ledger;
  2. strip Arcanum-specific bindings;
  3. promote local rule through constitution governance;
  4. execute code port only through task session;
  5. validate with self-test and adversarial write.
- Privacy: safe public-to-private direction.
- Current state:
  - frozen research partition exists;
  - Invoke define/design/plan artifacts exist;
  - plan explicitly says “intended-not-shipped; non-executed”;
  - planned files `authority/constitutions/SCHEMA-FORMAT-CONSTITUTION.md`, `authority/constitutions/ARTIFACT-RETENTION-CONSTITUTION.md`, and `cyberAlchemy-v2/tools/` do not exist in the inspected target.
- Proof:
  - `cyberAlchemy-v2/development/research/2026-07-01-arcanum-artifact-governance-import/findings.md`, `# Headline`, lines 23–31.
  - Same file, `# FROZEN import plan`, lines 41–74.
  - Same file, `# Mapping status`, lines 76–80.
  - Same file, `# Import path`, lines 82–86.
  - `cyberAlchemy-v2/development/artifact-governance-import/PLAN.md`, frontmatter, lines 1–12.
  - Same file, `# Implementation layering`, lines 17–23.
  - Same file, `# Shared SWU manifest`, lines 25–33.
  - Same file, `# Distill validation`, lines 41–44.
  - `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md`, `# Rules`, lines 106–114: its enforcement/parser remains candidate/future in the public source too.
- Proof status: direct-source observed planning; not executed-current.
- Non-effects: no CAV2 validator-enforced authority, no always-on hook, no completed Tier-1 constitution promotion.
- Residue: implement SWU-I1 through I4 in declared order; Tier-2 remains separately gated.

### AUTH-007 — “Build-from-owned” forbids duplicate authority but does not kill work

- Relationship: candidate `references` or `adapts` an existing owner rather than re-promoting the same principle.
- Direction: precedent sweep → found narrow owner → build from that owner.
- Narrow owner: existing definition, constitution, discipline, decision, validator, or lifecycle owner.
- Legal transition: label `build-from-owned`, cite owner, continue with adaptation/integration if needed.
- Privacy: respects the source owner’s class.
- Current state: CAV2-C17 remains explicitly candidate.
- Proof:
  - `cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md`, `# CAV2-C17`, lines 371–398.
  - Artifact-governance findings, lines 65–74, skip already-owned promotion and hygiene rules.
- Proof status: direct current candidate constitution plus concrete research application.
- Non-effects: finding precedent neither promotes the candidate nor ends all implementation; it changes the implementation basis.
- Contradiction: treating CAV2-C17 as a fully promoted, deterministic rule would exceed its declared candidate status.

### AUTH-008 — Ontology models, projects, and requests promotion; it does not decide

- Relationship:
  - ontology `projects` source and owner-approved state;
  - ontology `supplies evidence to` owner routes;
  - ontology `requests promotion from` the narrow owner.
- Direction: evidence/authority records → ontology read model → owner-facing request.
- Narrow owner: CAV2 ontology route for models; source/authority owner for any state change.
- Legal transition: candidate map or proposal → explicit owner decision → canonical owner mutation.
- Privacy: private CAV2 candidate package; generic Ontology Vault method is public.
- Current state: candidate authority-model boundary; generated projection runtime flagged and gated.
- Proof:
  - `cyberAlchemy-v2/ontology/README.md`, lines 3–18.
  - Same file, `# Repository Objective Role`, lines 20–31.
  - `cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md`, lines 23–40.
  - `cyberAlchemy-v2/ontology/projections/README.md`, lines 6–19 and 37–57.
  - `arcanum/arcana/ontology-vault/SKILL.md`, lines 123–126, 274–287, 291–305.
  - `arcanum/arcana/ontology-vault/README.md`, `# Project-Local Runtime Profiles`, lines 134–157.
- Proof status: direct current source; note that the inspected Arcanum Ontology Vault files have uncommitted modifications, so those exact working-tree clauses are dirty-current rather than committed proof.
- Non-effects: ontology output cannot mutate canonical sources, issue promotion verdicts, or establish runtime conformance.

### AUTH-009 — The authority-object schema remains a proposal, not the active schema or validator

- Relationship: Invoke-authored proposal `requests promotion from` the ontology route, then a decision gate.
- Direction: development proposal → ontology owner → decision gate → possible validator implementation.
- Narrow owner: ontology route for `NODE-MODEL`; decision gate for stabilization; task session for validator.
- Legal transition: amend owned ontology artifact with schema witness → stabilize by decision → build validator.
- Privacy: private candidate development evidence.
- Current state: non-executed.
- Proof:
  - `cyberAlchemy-v2/ontology/promotion-requests/2026-06-23-authority-object-schema-proposal.md`, header, lines 1–7.
  - Same file, `# The structural fix`, lines 11–18.
  - Same file, `# Dispatch technique trace`, lines 98–105.
  - Same file, `# Gaps / next route`, lines 107–111.
- Proof status: direct current candidate proposal.
- Non-effects: it does not amend `NODE-MODEL`, stabilize authority kinds, or create a closure validator.

### AUTH-010 — Authority harness, ledger, and ontology are related but not identical

- Relationship:
  - authority lifecycle envelope `carries` owner/state/provenance fields;
  - ledger `records` events/evidence;
  - ontology `projects` relations and state for inspection.
- Allowed taxonomy under the requested edge vocabulary:
  - ledger `supplies evidence to` authority owners and projections;
  - ontology `projects` authority/ledger evidence;
  - candidate schemas `request promotion from` their owner;
  - ledger-equals-ontology is `forbidden/no verified edge`.
- Narrow owners: authority owner for state; ledger owner for record integrity; ontology route for projections.
- Legal transition: a ledger event or ontology view must reach the named authority owner and promotion gate.
- Privacy: private CAV2 surfaces, with public Arcanum ontology method precedent.
- Current state: prior research concluded that proposed new rails duplicated an existing lifecycle envelope and rejected a parallel object.
- Proof:
  - `cyberAlchemy-v2/development/research/2026-06-21-authority-harness-ledger-ontology-unification/findings.md`, `# What the skeptics changed`, lines 8–35.
  - `cyberAlchemy-v2/ontology/projections/README.md`, `# Allowed Projection Inputs`, lines 12–19.
  - `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md`, `# Non-Collapse Rules`, lines 122–133.
- Proof status: historical research rebound to current authority and projection rules.
- Non-effects: append-only recordkeeping is not promotion; projection is not verdict; shared fields do not prove object identity across all roles.
- Residue: exact current machine schema and validator binding remain incomplete.

### AUTH-011 — CAV2 is a consumer and adapter of Arcanum; “meta-authority” and “mold” remain bounded analogies

- Verified:
  - consumer: yes, for public framework evidence, methods, and owner routes;
  - adapter: yes, where local bindings must replace Arcanum-specific paths or predicates;
  - authority spine: yes, as a local private governance arrangement;
  - consolidation surface: yes, explicitly stated.
- Candidate/intended:
  - downloadable base repository: intended, not extracted;
  - mold: defensible only as an intended downstream construction metaphor.
- Not established:
  - meta-authority over Arcanum, DomainSpec, or Saturn;
  - shipped System-5 controller;
  - canonical cross-system unification owner.
- Proof:
  - `cyberAlchemy-v2/README.md`, lines 8–16 and 36–47.
  - `cyberAlchemy-v2/SOURCE-MAP.md`, lines 10–21.
  - `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md`, lines 23–29 and 122–133.
- Non-effects: CAV2’s ability to route local reliance does not grant sovereignty over source repositories or system pillars.

### AUTH-012 — Public/private movement is asymmetric

- Relationship:
  - public Arcanum → private CAV2: `references`, `imports`, or `adapts`, with local gates;
  - private CAV2/DomainSpec → public Arcanum: forbidden absent scrub, owner review, and explicit public owner action.
- Narrow owner: decision gate for contested disclosure; source owner for reuse.
- Legal transition: boundary scrub + owner review + explicit publication/promotion route.
- Current state: Saturn/DomainSpec naming has a bounded disclosure decision; mechanisms and specified private systems remain private.
- Proof:
  - `cyberAlchemy-v2/authority/boundaries.md`, `# Public And Private`, lines 6–14.
  - Same file, `# Public Disclosure`, lines 58–65.
  - `cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md`, `# CAV2-C5`, lines 85–99.
- Proof status: direct current local boundary rule and decision reference.
- Non-effects: public explanation is not evidence of shipping; a public-safe summary does not authorize copying private prose or implementation detail.

## Owner/source/authority matrix

| Object | Source owner | CAV2 relation | CAV2 narrow owner | Current state | Legal next transition | Proof ceiling |
|---|---|---|---|---|---|---|
| Arcanum definitions | Arcanum definitions governance | references/imports | CAV2 definitions governance | upstream canonical; ledger candidate | promote only a distinct local term or explicit local adaptation | no upstream redefinition |
| Arcanum framework constitutions | Arcanum Constitution Governance | imports/adapts | CAV2 constitution governance | public source; local candidates | extract scoped local rule, preserve provenance, validate | no local force before promotion |
| Arcanum artifact validator | Arcanum tool owner | adapts | task session after constitution gates | upstream implementation; CAV2 plan only | re-root, self-test, validate, wire hook | no CAV2 enforcement today |
| CAV2 `CAV2-D*` terms | CAV2 definitions governance | instantiates local definition authority | definitions governance | local authority file | definitions governance mutation | no Arcanum authority |
| CAV2 stable repository constitution | CAV2 constitution governance | local constitution package | constitution governance | candidate/project-local | rule-specific promotion and validation | no cross-repository force |
| CAV2 disciplines | CAV2 discipline governance | local recurring-practice catalog | discipline governance | local surface | evidence-backed formalization/hardening | does not execute or define terms |
| CAV2 decisions | CAV2 decision gate | local scope/promotion decisions | decision gate | record-specific | execute only through downstream owner | decision is not implementation |
| CAV2 ontology | CAV2 ontology route | projects/requests promotion | ontology route plus source owner | candidate | owner decision and canonical patch | cannot self-promote |
| Inventory | Inventory owner | supplies discovery evidence | destination owner | non-authority read model | context selection or candidate handoff | cannot promote |
| DomainSpec implementation | DomainSpec/private owner | supplies private evidence | DomainSpec owner plus CAV2 boundary gate | private | scrub and owner review for any derivative | no public leakage |
| Saturn intent/loop | private architectural owner | referenced framing only | Saturn/architecture owner | intended/private, not shown shipped here | separate owner proof | CAV2 does not own whole loop |

## Import trace: artifact governance

```text
Arcanum public constitution/tool source
  -> CAV2 constitution manifest path staging
  -> 2026-07-01 frozen research partition
     - Tier 1: schema form, retention/gitignore, adapted validator
     - Tier 2: metadata prose pending decision; edge vocabulary rerouted
     - Skip: already-owned promotion and hygiene rules
  -> Invoke DEFINE/DESIGN/PLAN
  -> STOP: plan is non-executed
  -> future constitution-governance for two local rules
  -> future task-session for validator port and hook
  -> adversarial validation
```

First current stop: no execution of the plan’s L1/L2/L3 outputs is evidenced.

Forbidden effects:

- copying Arcanum-root predicates unchanged;
- treating a staged path as a promoted constitution;
- calling form validation authority-aware enforcement;
- importing already-owned promotion rules again;
- allowing a successful validator run to promote authority;
- leaking private CAV2 framing into public Arcanum.

## Promotion trace: authority-object proposal

```text
refine gaps + active authority model
  -> Invoke-authored candidate proposal
  -> ontology-route requested amendment
  -> STOP: proposal says NODE-MODEL is not amended
  -> decision-gate requested stabilization
  -> future task-session closure validator
```

First current stop: ontology owner amendment is absent from the proposal’s own proof.

Forbidden effects:

- treating proposed `instantiates` as an active mandatory field;
- treating the worked example as an emitted node;
- treating an Invoke artifact as a decision;
- implementing closure before schema stabilization.

## Contradiction and stale-state ledger

1. **Candidate versus “authority level.”**  
   `STABLE-REPOSITORY-CONSTITUTION.md` is both “Status: candidate” and “Authority level: project-local constitution.” Safest reading: it is scoped locally but not proven fully promoted/canonical.

2. **Active ledger versus stale scan.**  
   Definition and constitution manifests call themselves active ledgers while declaring a 2026-06-19 scan. The artifact-governance research explicitly calls the constitution scan stale and identifies missing framework documents and validator tooling.

3. **Plan L0 says staging done, while the original manifest is stale.**  
   The non-executed plan says Tier-1 pieces were recorded during a re-scan. The historical manifest contains a re-scan appendix, but this is still staging evidence, not a fresh comprehensive manifest regeneration.

4. **Ontology candidate models versus active authority model.**  
   `AUTHORITY-MODEL.md` is active local authority; `ontology/AUTHORITY-KINDS.md` remains candidate. The ontology table is a routing view and must not be mistaken for the owner table.

5. **Public Arcanum working tree is dirty.**  
   Current Ontology Vault owner text includes uncommitted modifications. Claims depending on those exact modified clauses are dirty-current. The older committed public boundary still has supporting precedent, but synthesis must distinguish commit-bound from working-tree-only evidence.

6. **CAV2 product worktree is dirty outside this authority seam.**  
   Current ontology-evidence-workbench changes do not establish changes to CAV2 authority. Proximity must not inflate them into governance proof.

7. **CAV2-C17 is candidate.**  
   “Build-from-owned” is a strong current design rule and was used in prior research, but should not be represented as deterministically enforced project canon without a later promotion/validation record.

## Git evidence

Relevant current parent history includes:

- `e347b738` — `feat(ontology): split canonical kinds into meaning and permission`
- `86dcce63` — `feat(ontology): rule canonical_kind the one label, flag the edge fork`
- `16f1909e` — `feat(definitions): define schema as admissible structure (CAV2-D56)`
- `fa602eb3` — `docs(reviews): record the definitions-rebuild review — overturned, not adopted`
- `adca3fe9` — `docs(research): record ontology implementation studies`

Relevant Arcanum history includes:

- `0490dbc` — `docs(arcanum): sync definitions + add framework dev-to-canonical promotion`
- `9121e0d` — `feat(ontology-vault): add project-local runtime profiles`
- `89f9a96` — `docs: require local-first discipline promotion`
- `b280678` — `Revert the two commits pushed without an owner gate`

These commits corroborate active evolution and owner-gate sensitivity. A commit is historical evidence of a mutation, not by itself proof of promotion, deployment, or current conformance.

## Residue and owner routing

- Re-scan both definition and constitution import ledgers against current public Arcanum; owner: CAV2 definitions/constitution governance.
- Reconcile candidate/project-local wording for `STABLE-REPOSITORY-CONSTITUTION.md`; owner: CAV2 constitution governance.
- Decide whether CAV2-C17 is to be promoted and deterministically validated; owner: constitution governance.
- Execute or explicitly retire the artifact-governance Tier-1 plan; owners: constitution governance, then task session.
- Keep metadata adoption separate from form validation; owner: decision gate before Tier-2 implementation.
- Route typed edge vocabulary to ontology plus definitions governance; do not hide it inside a constitution.
- Stabilize or reject the authority-object schema proposal before any closure validator; owners: ontology route, decision gate, then task session.
- Produce immutable movement records if authority states change; do not infer them from Git commits.
- Rebind public Ontology Vault claims to a clean commit or explicitly preserve dirty-current status.
- Retain explicit negative edges:
  - Inventory → promotion: forbidden.
  - ontology → self-promotion: forbidden.
  - generated projection → canonical authority: forbidden.
  - validation success → promotion: forbidden.
  - private CAV2/DomainSpec prose → public Arcanum: forbidden absent owner-reviewed extraction.
  - CAV2 → meta-authority over Arcanum/DomainSpec/Saturn: no verified edge.

```json
{
  "ACTION_RECEIPT": {
    "action_id": "spawn-0001",
    "assigned_identity": "MacIntyre, Alasdair",
    "role_id": "explorer-authority",
    "status": "complete",
    "validation": "pass",
    "validation_details": {
      "mutation_policy_observed": true,
      "repository_writes": 0,
      "inventory_leads_limited_to_contract": true,
      "load_bearing_claims_rebound_to_direct_current_sources": true,
      "git_history_inspected_read_only": true,
      "external_web_used": false,
      "memory_used": false,
      "claim_ids_stable": true,
      "proof_ceiling_preserved": true,
      "dirty_worktree_distinguished": true
    },
    "blockers": [],
    "artifacts": {
      "kind": "native-return",
      "handle": "agent-return://2026-08-05-arcanum-cav2-integration-research/cav2-integration-run-01/spawn-0001/explorer-authority",
      "written_paths": []
    },
    "residue": [
      "Import manifests require a current owner-led rescan.",
      "Artifact-governance Tier-1 remains a non-executed plan.",
      "Authority-object schema remains a non-executed promotion request.",
      "CAV2-C17 remains candidate rather than proven deterministic authority.",
      "Exact current Arcanum Ontology Vault wording is dirty-worktree evidence.",
      "Standalone extraction and broader public-safe publication remain open."
    ],
    "reroute": [
      {
        "target": "synthesizer",
        "reason": "Integrate the owner/source matrix, import traces, contradictions, and proof ceilings."
      },
      {
        "target": "constitution-governance",
        "reason": "Resolve candidate authority status and artifact-governance import residue only if separately authorized."
      },
      {
        "target": "ontology-route",
        "reason": "Adjudicate the authority-object schema proposal before validator work."
      }
    ]
  }
}
```

## Explorer return — operational integration

# Operational Integration Explorer Report

Identity: Hewitt, Carl  
Role: `explorer-operational`  
Action: `spawn-0002`  
Dispatch: `2026-08-05-arcanum-cav2-integration-research`  
Run: `cav2-integration-run-01`  
Mutation: none

## Executive verdict

`OP-001` — CyberAlchemy v2 uses Arcanum primarily as a public method and execution-capability supplier, while CyberAlchemy v2 retains local private authority, project state, and candidate implementation evidence.

The verified operational relationship is not one integrated runtime. It is a collection of bounded seams:

1. Arcanum Invoke authors candidate Define/Design/Plan material.
2. CyberAlchemy v2 stores project-local plans, manifests, receipts, and Craft state.
3. Task Session or the explicitly authorized prototype fast lane may execute bounded work.
4. Validation and observability produce evidence.
5. Craft may record references and next state.
6. Promotion remains a separate CyberAlchemy v2 owner decision.
7. Generation, synchronization, installation, runtime execution, publication, and deployment remain distinct later transitions.

No inspected receipt transfers authority. No current evidence proves a holistic CyberAlchemy v2 runtime driven end to end by Invoke, Task Session, Craft, ontology, Inventory, Bootstrap, and Orchestrate.

## Proof taxonomy

- `executed-current`: a command was executed in this exploration against current bytes.
- `direct-source-observed`: current source or contract was inspected, but its workflow was not executed.
- `historical-executed`: an immutable committed receipt records an earlier execution.
- `candidate-local`: implementation or validation evidence explicitly capped below governance synchronization/promotion.
- `generated`: a runtime/package projection, not canonical authority.
- `dirty-worktree-only`: uncommitted or untracked current evidence.
- `deployed`: an installed and behaviorally witnessed surface; none established here.
- `unverified`: required operational witness absent.

## Current source and projection chain

`OP-002` — The owner-directed chain is:

```text
public Arcanum canonical method/capability contract
  -> generated host skill package, if synchronized
  -> CyberAlchemy v2 project-local invocation
  -> candidate Define/Design/Plan artifacts
  -> selected bounded execution route
  -> implementation attempt
  -> validation / observability evidence
  -> optional Craft references and derived index
  -> explicit CyberAlchemy v2 authority-owner review
  -> possible local promotion
```

Non-effects:

- Public Arcanum does not acquire private CyberAlchemy v2 prose.
- A generated skill does not become canonical source.
- An Invoke receipt does not authorize implementation.
- A Task Session receipt does not authorize promotion.
- Craft does not reinterpret owner verdicts.
- Inventory does not select or promote.
- Ontology does not write authority.
- Validation success does not establish release or deployment.
- Observability does not authorize maintenance.
- Bootstrap presence does not prove behavioral parity.

Direct selectors:

- `cyberAlchemy-v2/README.md#Import-Spine`
- `cyberAlchemy-v2/README.md#Stable-Thesis`
- `cyberAlchemy-v2/README.md#Repository-Shape`
- `cyberAlchemy-v2/README.md#Current-Gate`
- `cyberAlchemy-v2/SOURCE-MAP.md#Source-Cohorts`
- `cyberAlchemy-v2/SOURCE-MAP.md#Ingest-Rules`
- `cyberAlchemy-v2/CRAFT.md#Contexts`
- `ops/development/2026-08-05-arcanum-building-system-research/findings.md#4-owner-and-integration-matrix`
- `ops/development/2026-08-05-arcanum-building-system-research/findings.md#6-artifact-and-receipt-lineage`
- `ops/development/2026-08-05-arcanum-structural-governance-research/findings.md#9-integration-with-invoke-task-session-craft-and-the-building-protocol`

## Runtime and integration matrix

| Claim | Seam | Inputs | Ordered owners and gates | Artifact / output | First stop | Proof |
|---|---|---|---|---|---|---|
| `OP-003` | Invoke | intent, source anchors, design denominator, planning constraints | Invoke Define → Design evidence/validator → Plan → optional Distill/Dispatch validation | Define/Design/Plan package and bounded handoff | missing/failed design evidence, invalid SWU shape, failed planning validation | Direct contract observed; CyberAlchemy v2 historical and dirty candidate examples |
| `OP-004` | Task Session | exact selected SWU, bindings, context, admission evidence | selected unit → fast entry/readiness → context → mutation admission → one-SWU execution → critical validation → closeout owner join | execution terminal and, only after join, synchronized result | stale/ambiguous selection, missing producer receipt, changed baseline, failed validation, missing closeout join | Direct contract observed; full CyberAlchemy v2 end-to-end chain unverified |
| `OP-005` | Craft | `.craft/ledger.yml`, native owner receipts/references | Craft validates ledger scope and derives views | `CRAFT.md`, `.craft/index.json` | invalid ledger/reference or external blocker | Historical committed operational surface; Craft is record/navigation, not authority |
| `OP-006` | Dispatch Spec / Orchestrate | persisted dispatch sheet, exact action contracts, confirmation | Dispatch Spec validates route → user confirmation → Orchestrate spawn/join/gate/close | action and dispatch receipts | invalid binding, missing result, timeout/correlation failure | Direct current dispatch observed; coordination authority only |
| `OP-007` | Inventory | parent machine index and selected evidence cards | Inventory lookup/validation → caller interpretation → direct owner rebind | discovery packet/read model | missing/stale match or absent direct owner | Parent index validated with warnings; no CyberAlchemy v2 machine index |
| `OP-008` | Ontology Vault | source-ledgered candidates and owner routes | map/validate candidate structure → owner-specific proposal | candidate graph/projection | attempted ontology self-promotion or absent authority owner | Direct non-authority contract observed; no write edge verified |
| `OP-009` | Validation | exact contract, fixture, implementation bytes | validator/test runner → bounded result → consuming owner interprets | report/receipt | failed/unrun critical check | Multiple historical bounded passes and blocks; no general acceptance inference |
| `OP-010` | Observability | invocation envelope and bounded result | observer records signal → reflection may recommend → explicit owner decides | signal/reflection evidence | no approved maintenance scope | Observability references exist; authority effect explicitly `none` in sampled Invoke receipt |
| `OP-011` | Generated packages | accepted canonical Arcanum source | generator → checksum/sync → install → runtime acceptance | Claude/Codex skill projection | stale projection, missing apply authority, missing install/runtime witness | Current generated/canonical divergence reported by direct Arcanum findings; parity blocked |
| `OP-012` | Bootstrap/runtime projection | canonical public capability closure and runtime profile | canonical acceptance → generation → synchronization → release → consumer install → runtime tests | installed callable capability | no canonical public owner or missing acceptance transition | Intent-router precedent kills current Bootstrap integration |
| `OP-013` | Handoff / continuation | terminal receipt plus exact owner prerequisite | Continuation Router validates one-hop route → owner executes → join validates receipt | joined result / continuity cursor | missing, stale, repeated, ambiguous, or non-pass owner receipt | Direct contract and bounded negative fixtures observed; CyberAlchemy v2 full real join unverified |
| `OP-014` | Promotion | proposal, direct source, validation, owner decision | narrow CyberAlchemy v2 authority owner → decision gate → canonical mutation → downstream sync if required | local authority artifact | absent owner, unresolved conflict, failed critical validation, private/public risk | Normative local authority route; no promotion inferred from execution evidence |

## Finite positive trace

`TRACE-OP-POS-001` — Candidate-local failure-recovery implementation:

```text
CyberAlchemy v2 recovery intent
  -> Invoke define/design/plan
  -> design validator fixed point
  -> seven bounded SWUs planned
  -> explicit candidate-local fast lane
  -> two implementation targets plus bounded planning targets
  -> no-network validation V-OEWFR-01..13
  -> 25 builder tests pass
  -> consolidated prototype receipt
  -> governance reconciliation deferred to HN-7362EC2F08B7
  -> STOP
```

Inputs:

- `cyberAlchemy-v2/development/ontology-evidence-workbench-typed-test-recovery/INVOKE-RECEIPT.json`
- `.../planning/SWU-MANIFEST.json`
- `.../planning/work-pack/session-evidence/FAST-LANE/20260803T222716Z/receipt.json`

Owners/gates:

1. Invoke owns Define/Design/Plan evidence.
2. Design validator reports a fixed point.
3. Dispatch and Distill validations pass.
4. Candidate-local fast lane owns only the declared prototype scope.
5. Validation owns V-OEWFR-01..13 and 25 tests.
6. Handoff Notice owns deferred reconciliation routing.
7. CyberAlchemy v2 authority owners still own any later promotion.

Artifacts:

- Invoke receipt digest `db0713d9993ef7c0cf17dcc9b3a45d582ae3355751f8f1f87c2597a515645204`
- fast-lane receipt
- Handoff Notice `HN-7362EC2F08B7`

First stop:

- Candidate-local prototype validation.

Forbidden effects after stop:

- no retry authority;
- no generalized build claim;
- no browser acceptance;
- no promotion;
- no release, deployment, or production claim;
- no claim that Task Session lifecycle reconciliation occurred.

Proof classification:

- The whole typed-test-recovery package is currently untracked, hence `dirty-worktree-only + candidate-local`.
- Its receipt reports historical execution but is not immutable committed repository evidence.
- Current product files are modified, so the receipt’s stored postimages must not be assumed to describe current bytes without a fresh baseline comparison.

## Finite negative trace

`TRACE-OP-NEG-001` — Cross-feature support missing:

```text
selected CyberAlchemy v2 IOLM SWU-00C-B
  -> upstream cross-feature support required
  -> current compiler contract reviewed
  -> targeted regression test confirms CROSS_FEATURE_UNSUPPORTED
  -> Decision Gate option 1 remains selected
  -> required upstream support receipt absent
  -> Task Session result = block
  -> Craft exposes blocking state
  -> no prototype mutation
  -> authority effect = none
```

Exact input:

- `cyberAlchemy-v2/development/interactive-ontology-learning-map/work-pack/session-evidence/SWU-IOLM-00C-B/execution-receipt.json`

Owners/gates:

1. IOLM work pack selects the bounded candidate unit.
2. DomainSpec/compiler owner supplies or withholds cross-feature support.
3. Decision Gate records the chosen upstream route.
4. Task Session stops because the required support receipt does not exist.
5. Craft records the blocker; it does not repair the external owner’s state.

Artifacts:

- `DECISION-GATE.md`
- execution receipt
- `BLK-DSV2-BTE-SWU-READINESS-CONTRADICTION-001`
- synchronized Work Pack, execution pack, Dispatch record, ledger, index, and `CRAFT.md`

First stop:

- missing upstream support receipt plus contradictory SWU readiness state.

Forbidden effects:

- no prototype mutation;
- no guessed compiler capability;
- no substitution of a passing regression test for support;
- no authority effect;
- no successor execution.

Proof classification:

- Receipt is tracked and clean in the current worktree.
- Last repository commit touching it: `3c12cc0f39a16e95751e7be6a6d108a2fc21060a`.
- `historical-executed + committed`; it proves the blocked route and the test confirming the blocker, not current upstream behavior after later unrelated changes.

## Import seam: public Arcanum artifact governance to private CyberAlchemy v2

`OP-015` — The July 1 research identified a safe import direction and a real but narrow enforcement opportunity.

Historical plan:

```text
public Arcanum rule/tool
  -> stage under CyberAlchemy v2 authority/imports
  -> strip Arcanum-specific path bindings
  -> extract smallest local rule
  -> local promotion-policy + decision gate
  -> CyberAlchemy v2 constitution or runtime contract
  -> implementation Task Session for validator code
```

Current verification:

- The import manifest now names the Tier-1 validator, schema format, retention taxonomy, and gitignore candidates.
- `cyberAlchemy-v2/development/artifact-governance-import/{DEFINE.md,DESIGN.md,PLAN.md}` exists and is committed; the latest commit touching the plan is `fad671aed4ebf6c1405e4264a40d14e3ee33e740`.
- Searches found the intended local landing paths in planning material, but no verified `cyberAlchemy-v2/tools/validate-artifact-constitution.sh` implementation and no verified promoted local schema/retention constitutions.
- Therefore the seam has advanced from frozen research into committed Define/Design/Plan, but not into verified implementation, hook wiring, or promotion.

`OP-016` — The old “validator exists” claim remains true only for public Arcanum. It does not establish CyberAlchemy v2 enforcement.

First stop:

- Separate local constitution promotion and runtime-contract implementation are absent.

Forbidden inference:

- A public Arcanum validator, an import manifest row, or a CyberAlchemy v2 plan is not a local enforcement gate.

## Bootstrap and runtime non-integration precedent

`OP-017` — The intent-router Inventory result supplies a discriminating absence witness:

- private resolver: 34 tests passed historically;
- public Arcanum canonical sigil/spell owner: absent;
- Bootstrap selection: killed;
- generated packages: absent;
- release archive: absent;
- consumer install: absent;
- CyberAlchemy v2/Augmentor/orchestrator adapter: absent;
- deployed behavior: absent.

This is a valid negative precedent because the first missing owner is explicit: canonical public Arcanum capability acceptance. Successful private tests cannot cross that stop.

The Inventory entry itself is untracked in the current worktree. It is a dirty non-authority projection and was used only to locate its stated direct boundary, not as current authority.

## Craft state

`OP-018` — CyberAlchemy v2 has a real project-local Craft surface:

- source of truth: `cyberAlchemy-v2/.craft/ledger.yml`;
- human view: `cyberAlchemy-v2/CRAFT.md`;
- derived machine view: `cyberAlchemy-v2/.craft/index.json`;
- current root context: `CTX-CAV2-ROOT`, stage `define`, gate `flag`;
- current ledger includes candidate implementation contexts, decisions, blockers, and owner routes.

The three sampled Craft files are currently clean. The latest commit touching `CRAFT.md` and the ledger is `32ee3c2c5a8e1c9f43f34017549cf1bea4fcf539`.

Craft’s verified role is local coordination and derived navigation. It does not:

- make an Invoke plan executable;
- manufacture a missing owner receipt;
- promote ontology or Inventory content;
- override DomainSpec/compiler authority;
- turn a candidate-local completion into synchronized governance.

## Inventory machine-index gap

`OP-019` — Executed-current diagnostic:

```text
test -f cyberAlchemy-v2/inventory/index.json
=> absent
find cyberAlchemy-v2/inventory -maxdepth 2 -type f
=> cyberAlchemy-v2/inventory/README.md only
```

Therefore:

- CyberAlchemy v2 has no project-local machine Inventory index.
- The active parent `.arcanum/inventory/index.json` is the discovery surface.
- Parent Inventory validation passed with 146 historical uncontrolled-tag warnings.
- This gap prevents a claim of a standalone CyberAlchemy v2 Inventory runtime or independently indexed knowledge surface.
- It does not prevent direct owner-source inspection.

## Dirty versus committed classification

`OP-020` — Current repository evidence is mixed and must remain frozen by class.

Committed and clean sampled evidence:

- CyberAlchemy v2 `README.md`, `SOURCE-MAP.md`, `CRAFT.md`, `.craft/ledger.yml`, `.craft/index.json`;
- artifact-governance import plan;
- IOLM `SWU-IOLM-00C-B` blocked execution receipt;
- direct August 5 findings and their immutable native-run evidence.

Dirty or untracked evidence:

- extensive canonical Arcanum changes under Task Session, Invoke, WPRA, continuation, implementation-readiness, ontology, and subagent surfaces;
- matching generated `.agents/` and `.claude/` changes;
- modified CyberAlchemy v2 ontology-evidence-workbench implementation files;
- untracked typed-test-recovery package and receipts;
- untracked semantic-navigation and reasoning-engine work;
- modified parent Inventory projections and many untracked Inventory entries;
- dirty Arcanum submodule state.

Consequences:

1. Current canonical Arcanum contracts may be directly observed but cannot be attributed to the committed Arcanum snapshot.
2. Generated packages cannot be presumed in parity with canonical Arcanum.
3. Untracked CyberAlchemy v2 receipts are candidate evidence, not immutable historical proof.
4. Modified implementation bytes may have advanced past the stored receipts.
5. No current test result should be generalized across these mixed baselines.

## Current versus historical Arcanum proof

`OP-021` — The August 5 building-system report distinguishes:

- committed foundation at Arcanum commit `07b01c9dd4e918ae0b0d83f6a2cde52ea8f9a295`;
- live uncommitted candidate closure for selection, admission, prerequisite routing, continuation, and finite loops;
- bounded executed fixture fragments;
- no complete exact positive path from Invoke through real execution and Refresh join;
- stale/divergent generated surfaces.

`OP-022` — The August 5 structural-governance report distinguishes:

- observed public owner contracts;
- bounded validator passes;
- failed full Artifact Constitution validation;
- a stale generated `discipline-governance` projection;
- normative but unverified constitution/discipline lifecycle realization;
- separate promotion, registry, generation, synchronization, installation, and runtime transitions.

Those reports are accepted direct comparison inputs, but their claims remain bound to their recorded snapshots and selectors.

## Defects and stale seams

`DEF-OP-001` — No full positive operational witness.

There is no executed chain binding exact Invoke output through selection, context, mutation admission, product execution, critical validation, real Refresh-owner join, synchronized result, and continuity cursor.

`DEF-OP-002` — Candidate-local reconciliation gap.

The strongest sampled recent CyberAlchemy v2 implementation receipt deliberately deferred lifecycle reconciliation to a Handoff Notice.

`DEF-OP-003` — Generated/canonical drift.

Current canonical Arcanum and generated `.agents`/`.claude` packages are dirty and known to diverge on several building-system capabilities. Runtime behavior cannot be inferred from canonical source inspection.

`DEF-OP-004` — CyberAlchemy v2 machine-index absence.

Only `inventory/README.md` exists locally; parent Inventory remains the discovery dependency.

`DEF-OP-005` — Artifact-governance import not realized.

A committed import plan exists, but the local validator, hook wiring, and promoted local constitutions were not found.

`DEF-OP-006` — Full Artifact Constitution validation is red upstream.

Arcanum’s bounded self-tests can pass while the full validator fails. Importing it would import a limited file-form mechanism, not comprehensive authority enforcement.

`DEF-OP-007` — Metadata enforcement remains absent.

The metadata parser/frontmatter route is advisory/candidate and requires a CyberAlchemy v2 convention decision plus enforceable parser mode.

`DEF-OP-008` — Orchestrate causal evidence defects remain historically relevant.

The building-system report records action-ID and exact-input/correlation defects. Coordinator evidence must not be equated with task semantic completion.

`DEF-OP-009` — Intent-router runtime seam absent.

Private tests exist, but canonical Arcanum ownership, generated projection, consumer install, and runtime adapter do not.

`DEF-OP-010` — Dirty implementation postimages.

Modified ontology-evidence-workbench files mean prior stored hashes and passing receipts do not prove current implementation state.

## Residue

- `RES-OP-001`: execute and freeze one exact positive Invoke-to-synchronized-Task-Session witness.
- `RES-OP-002`: reconcile candidate-local fast-lane results through their Handoff Notice owner without retroactive claim inflation.
- `RES-OP-003`: choose and execute the existing owner route for the artifact-governance import, including local promotion and separate validator implementation.
- `RES-OP-004`: decide whether CyberAlchemy v2 owns a local machine Inventory index or deliberately consumes the parent read model.
- `RES-OP-005`: restore or explicitly reject canonical/generated parity before runtime claims.
- `RES-OP-006`: rerun bounded validation against one frozen clean source snapshot.
- `RES-OP-007`: bind observability signals to explicit maintenance-owner decisions; do not let signals mutate source.
- `RES-OP-008`: establish a real canonical Arcanum owner before any Bootstrap/runtime integration claim for the intent router.
- `RES-OP-009`: keep DomainSpec/compiler support receipts external and owner-issued; Craft cannot substitute them.
- `RES-OP-010`: preserve public-to-private import direction and prohibit private CyberAlchemy v2 prose from entering public Arcanum.
- `RES-OP-011`: resolve current dirty-worktree ownership before attributing or promoting any recent implementation.
- `RES-OP-012`: keep ontology and Inventory as no-authority projections unless and until a separate owner accepts a proposal.

```json
{
  "ACTION_RECEIPT": {
    "action_id": "spawn-0002",
    "assigned_identity": "Hewitt, Carl",
    "role_id": "explorer-operational",
    "status": "complete",
    "validation": "PASS",
    "validation_details": "Read-only operational exploration completed against the exact persisted agent-1 prompt and permitted Inventory leads. Direct current owners, committed representative receipts, dirty-worktree boundaries, one finite positive candidate-local trace, one finite committed negative trace, current machine-index absence, and historical Arcanum run evidence were independently inspected. No files were written and no mutable workflow was executed.",
    "blockers": [],
    "artifacts": {
      "kind": "native-return",
      "handle": "agent-final://cav2_operational_explorer/spawn-0002",
      "content": "Operational integration report with claim IDs OP-001..OP-022, TRACE-OP-POS-001, TRACE-OP-NEG-001, DEF-OP-001..DEF-OP-010, and RES-OP-001..RES-OP-012"
    },
    "residue": [
      "missing-full-positive-invoke-to-synchronized-task-session-witness",
      "candidate-local-governance-reconciliation-deferred",
      "artifact-governance-import-planned-not-realized",
      "cyberalchemy-v2-machine-index-gap",
      "canonical-generated-arcanum-drift",
      "dirty-worktree-evidence-boundary",
      "intent-router-bootstrap-runtime-seam-absent",
      "full-artifact-validator-red",
      "ontology-and-inventory-remain-no-authority"
    ],
    "reroute": {
      "target": "parent-synthesizer",
      "reason": "Integrate the operational matrix and finite traces with the authority-lineage and systems-boundary explorer reports while preserving proof ceilings and dirty-versus-committed classifications."
    }
  }
}
```

## Explorer return — systems boundaries

## Explorer report — `cav2-integration-run-01`

### Bottom line

`SYS-001` — CyberAlchemy v2 is currently a private, project-local consolidation and local-authority surface. It consumes source evidence from Arcanum, DomainSpec, Inventory, ontology, research, validation, and operations, but does not absorb their authority automatically. Its local authority applies only after its own owner routes. Evidence: `cyberAlchemy-v2/README.md`, `authority/definitions/DEFINITIONS.md#cav2-d9-cyberalchemy-v2`, `authority/AUTHORITY-MODEL.md#authority-rule`.

`SYS-002` — The four-system model is valid only as a bounded architecture interpretation:

| System | Current verified role | Intended role | Deployed/public evidence | Ceiling |
|---|---|---|---|---|
| DomainSpec | Private structured-intent/modeling evidence and baseline | Precise intent/contracts Saturn can compare reality against | Not independently established as a public product | Private/spec evidence; do not call shipped |
| Arcanum | Public reusable capability framework: method, lifecycle, skills, observability | Execution substrate for the broader loop | `arcanum/README.md`; current docs source calls Arcanum the public working surface | Repository/docs evidence, not live-site verification |
| Saturn | Convergence/control-loop framing: observe → evaluate → decide → route → verify | Cross-layer regulator closing intent↔evidence | Current `arcanum/docs/saturn.html` presents it as “we are building”; closed loop explicitly still assembling | Public documentation claim only; not a shipped closed-loop witness |
| CyberAlchemy v2 | Private source-ledgered consolidation and active local authority model | Downloadable stable base repository for downstream construction | None; explicitly pre-extraction/private | Local authority model, not standalone/released/deployed |

### Four-system edges

| Claim | Edge | Status | Proof and ceiling |
|---|---|---|---|
| `EDGE-001` | DomainSpec → Saturn: supplies structured intent/baseline | verified as intended/spec relationship | `cyberAlchemy/agentic-system-deep-dive.md#domainspec`; `SATURN-LAYER-MAP.md:17-49`; not public-product proof |
| `EDGE-002` | Arcanum → Saturn: execution routes and bounded work | verified as architectural role | `agentic-system-deep-dive.md#arcanum`; Arcanum does not thereby implement the whole Saturn loop |
| `EDGE-003` | Evidence/telemetry → Saturn: comparison and correction feedback | intended; partially evidenced only | `arcanum/docs/saturn.html#loop`; current documentation says the closed loop is still being assembled |
| `EDGE-004` | Arcanum → CAV2: public-framework source/reference/import candidate | verified | `cyberAlchemy-v2/SOURCE-MAP.md#source-cohorts`; `authority/imports/constitutions/MANIFEST.md#re-scan-2026-07-01` |
| `EDGE-005` | DomainSpec/private evidence → CAV2: private source evidence, boundary constrained | verified | `cyberAlchemy-v2/SOURCE-MAP.md#source-cohorts`; `authority/boundaries.md#public-and-private` |
| `EDGE-006` | Inventory/ontology → CAV2: candidate/read-model input | verified, explicitly non-authoritative | `SOURCE-MAP.md#ingest-rules`; `authority/AUTHORITY-MODEL.md#non-collapse-rules`; `ontology/README.md` |
| `EDGE-007` | CAV2 → its local definitions/constitutions/decisions/specs | verified, owner-routed local authority | `authority/AUTHORITY-MODEL.md#authority-rule`, `#authority-kinds`, `authority/promotion-policy.md` |
| `EDGE-008` | CAV2 → public Arcanum authority | contradicted/forbidden | `DEFINITIONS.md#cav2-d9-cyberalchemy-v2` says it does not automatically absorb Arcanum authority; `authority/boundaries.md` forbids private-to-public inheritance |
| `EDGE-009` | Ontology/Inventory → promotion or authority | forbidden | `authority/AUTHORITY-MODEL.md#non-collapse-rules`; `ontology/README.md`; CAV2-C4 |
| `EDGE-010` | CAV2 → standalone base repository | intended, absent as an executed transition | `README.md#repository-objective`, CAV2-D1, CAV2-C10; no extraction decision/witness bound |

### Recursion and causal feedback

```text
R0: Domain/project work
  intent (DomainSpec) -> bounded execution (Arcanum) -> validation/evidence
       ^                                                    |
       |---------------- Saturn intended regulator ----------|

R1: CAV2 repository consolidation
  source evidence/import -> candidate map -> narrow owner route -> local authority
       ^                                                            |
       |------------ residue, review, demotion, reroute ------------|

R2: CAV2 as a possible meta-authority / System-5
  This remains an analogy only. No verified repository edge makes CAV2
  the governing controller of R0, nor authorizes it to promote other owners.
```

`FB-001` — Saturn’s intended loop is causal: observe reality, compare to intent, decide, route a correction through execution, verify, feed evidence back. `arcanum/docs/saturn.html#loop`.

`FB-002` — CAV2’s local authority loop is review-oriented, not automatic: source → import candidate → inventory/ontology candidate → owner-routed local authority → implemented/validated behavior → stable asset, with block/defer/demote/reroute available. `authority/AUTHORITY-MODEL.md#core-flow`; `authority/promotion-policy.md`.

`FB-003` — These loops must not be collapsed. The former governs system convergence; the latter governs whether a private consolidation artifact may count locally.

### Hypothesis verdicts

| ID | Hypothesis | Verdict |
|---|---|---|
| `H-CONSUMER-001` | CAV2 is a consuming repository | **Qualified verified.** It consumes/references source cohorts and import candidates, but source owners remain authoritative until owner-routed promotion. |
| `H-SPINE-001` | CAV2 is a private authority spine | **Verified locally.** Its active local authority model, local definitions, constitutions, import ledgers, and promotion routes support this. Scope is CAV2, not the entire workspace. |
| `H-CONSOLIDATION-001` | CAV2 is a consolidation surface | **Verified.** README and CAV2-D9 explicitly define source-ledgered consolidation without copying/automatic ownership. |
| `H-BASE-001` | CAV2 is the downloadable base repository | **Intended only.** CAV2-D1/D9 and README make this the target; CAV2-C10 requires an owner-reviewed extraction. |
| `H-META-001` | CAV2 is a meta-authority | **Contradicted as a current repository fact.** Candidate Inventory calls it a “MOLD”/apex posture, but direct CAV2 authority is scoped local and forbids automatic cross-scope transfer. |
| `H-S5-001` | CAV2 is a Beer System-5 analogue | **Candidate analogy only.** The Inventory synthesis itself says the link is not a cited repository fact and records a two-System-5 recursion contradiction. |
| `H-MOLD-001` | CAV2 is a reusable authority mold | **Candidate method metaphor only.** Direct sources support a future base with local authority patterns; they do not establish an exported, enforced mold or downstream casts. |

### Contradictions and proof ceilings

`CON-001` — The assigned Inventory entries characterize CAV2 as missing System-5/meta-authority/mold, while direct CAV2 authority documents define a bounded local authority model and retain owner separation. The direct documents prevail. Sources: `.arcanum/inventory/entries/machine-map-and-moat-synthesis.md#decision-spine`; `cav2-authority-and-determinism-synthesis.md#part-1--how-cav2-authority-works`; `authority/AUTHORITY-MODEL.md`.

`CON-002` — `SATURN-LAYER-MAP.md` says the deployed Arcanum site does not mention Saturn or DomainSpec, but current `arcanum/docs/index.html:489-506` and `arcanum/docs/saturn.html` do. Treat the layer map’s deployed-surface section as stale. The current docs still qualify Saturn as under construction, so this does not establish a deployed closed loop.

`CON-003` — CAV2’s constitution-import manifest says the 2026-06-19 scan is stale and zero candidates were extracted into a local rule. Therefore historical import research cannot prove current local adoption. `authority/imports/constitutions/MANIFEST.md#re-scan-2026-07-01`.

`CON-004` — Current CAV2 implementation/development worktree contains user-owned modified and untracked bytes. I did not attribute those as CAV2 authority, execution, deployment, or history evidence. `git status --short -- cyberAlchemy-v2`.

`CEIL-001` — Local “active” definitions/authority model establish only CAV2-local authority. They do not establish cross-repository governance, public release, automatic import, or a running Saturn regulator.

`CEIL-002` — Arcanum’s public repository and documentation prove public framework material and declared capability boundaries; they do not prove an external live deployment, CAV2 integration, or Saturn closure.

`CEIL-003` — History was partially inspectable: current Arcanum submodule HEAD is `07b01c9dd4e918ae0b0d83f6a2cde52ea8f9a295`; a parent CAV2 path query resolved `224331e46aaaa8af4a1138fd44f0205c1721eaaa` (2026-06-24). A broader `git log --all` was blocked by malformed `refs/codex/turn-diffs/...`; no stronger history conclusion is warranted.

### Forbidden collapses

- DomainSpec intent ≠ CAV2 local authority.
- Arcanum execution ≠ Saturn’s whole regulation loop.
- CAV2 local authority ≠ workspace apex/meta-authority.
- Inventory/ontology/projection/evidence/receipt ≠ promotion.
- Generated projection ≠ canonical source.
- Public Arcanum ≠ private CAV2 prose or private DomainSpec evidence.
- A future base repository ≠ a present standalone/downloadable/released repository.
- System-5/mold terminology ≠ an owner-routed repository edge.

### Owner-routed residue

- `RES-001`: CAV2 authority owner must decide whether any System-5/meta-authority claim is a local, bounded definition or remains rejected analogy.
- `RES-002`: `decision-gate`/constitution-governance must resolve any standalone extraction and public/private transfer; CAV2-C10 is the direct gate.
- `RES-003`: ontology route plus source owner must demonstrate that every candidate projection lacks authority write effects before it becomes a consequential machine surface.
- `RES-004`: CAV2 import owner must re-scan/reconcile stale import manifests before asserting an Arcanum pattern is locally adopted.
- `RES-005`: publication owner must reconcile the stale Saturn-layer-map deployment claim with current `arcanum/docs/` bytes, then separately verify live publication if needed.
- `RES-006`: repository/Git-maintenance owner should repair the malformed Codex ref before history-sensitive claims are extended.

```json
{
  "ACTION_RECEIPT": {
    "action_id": "spawn-0003",
    "assigned_identity": "Beer, Stafford",
    "role_id": "explorer-systems",
    "status": "complete",
    "scalar_validation": "pass",
    "validation_details": {
      "mode": "read-only",
      "writes": 0,
      "external_web": false,
      "memory_used": false,
      "direct_sources_rechecked": true,
      "candidate_inventory_treated_as_non_authority": true,
      "required_role_matrix": "included",
      "hypothesis_verdicts": "included",
      "history_limit": "broader git history traversal blocked by malformed refs/codex/turn-diffs reference"
    },
    "blockers": [
      "No owner-routed CAV2-to-System-5/meta-authority edge was found.",
      "No CAV2 standalone extraction/release/deployment witness was found.",
      "Current dirty CAV2 bytes are user-owned and excluded from authority claims."
    ],
    "artifacts": {
      "native_return_handle": "agent-return:/root/cav2_systems_explorer/cav2-integration-run-01",
      "report_claims": [
        "SYS-001",
        "SYS-002",
        "EDGE-001",
        "EDGE-010",
        "H-CONSUMER-001",
        "H-SPINE-001",
        "H-CONSOLIDATION-001",
        "H-BASE-001",
        "H-META-001",
        "H-S5-001",
        "H-MOLD-001",
        "CON-001",
        "CON-002",
        "CON-003",
        "CON-004"
      ]
    },
    "residue": [
      "RES-001",
      "RES-002",
      "RES-003",
      "RES-004",
      "RES-005",
      "RES-006"
    ],
    "reroute": [
      "cyberAlchemy-v2 authority owner",
      "decision-gate",
      "constitution-governance",
      "ontology route plus source owner",
      "CAV2 import owner",
      "publication owner",
      "repository Git-maintenance owner"
    ]
  }
}
```
