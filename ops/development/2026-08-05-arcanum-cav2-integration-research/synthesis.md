# Candidate relationship model — Arcanum ↔ CyberAlchemy v2

## Plain-language answer

CyberAlchemy v2 currently consumes public Arcanum methods, capability contracts, and governance patterns while keeping its own private, project-local authority. It can cite, stage, adapt, and—through its own narrow owner gates—promote distinct CAV2-local rules. It cannot redefine Arcanum, inherit DomainSpec authority, declare Saturn complete, or make Inventory, ontology, execution receipts, validation, generation, or Git commits perform promotion.

The verified relationship is therefore a collection of bounded seams, not one integrated runtime:

```text
public Arcanum source/method
  -> CAV2 reference or staged import
  -> locally adapted candidate
  -> CAV2 narrow-owner decision
  -> bounded implementation
  -> validation and observability evidence
  -> possible CAV2-local promotion
```

The first unproved step differs by seam. For artifact governance, the stop is before local constitutions, validator port, and hook wiring. For authority objects, the stop is before ontology amendment and schema stabilization. For end-to-end execution, the stop is before one frozen positive Invoke → Task Session → Refresh/join witness. For standalone/runtime claims, the stop is before extraction, generated-package parity, installation, behavioral acceptance, release, or deployment.

## Four-system role map

| System | Verified current role | Intended role | Current status and ceiling | Direct source binding |
|---|---|---|---|---|
| DomainSpec | Private structured-intent and implementation evidence; supplies baselines and owner-issued prerequisites | Precise intent/contracts against which Saturn could compare reality | Private; not independently established as a public or shipped product | `cyberAlchemy/agentic-system-deep-dive.md#domainspec`; `ops/development/2026-06-21-paper-saturn-explainer/SATURN-LAYER-MAP.md:17-49`; explorer `SYS-002`, `EDGE-001`; architectural/private scope; direct-source-observed |
| Arcanum | Public reusable capability, lifecycle, governance-method, generation, and observability framework | Execution substrate for bounded work in a broader loop | Public repository/docs surface; no live external deployment or holistic CAV2 integration proved | `arcanum/README.md`; `arcanum/definitions/DEFINITIONS.md#DEF-ARC-CANONICAL-ARTIFACT`; explorer `AUTH-003`, `SYS-002`, `OP-002`; public framework scope; direct-source-observed, committed foundation at `07b01c9dd4e918ae0b0d83f6a2cde52ea8f9a295` plus separately dirty-current contracts |
| Saturn | Architectural convergence/control-loop framing: observe, compare, decide, route, verify | Regulator closing intent ↔ observed reality | Current docs say the loop is being assembled; no shipped closed-loop witness | `arcanum/docs/saturn.html#loop`; `SATURN-LAYER-MAP.md`; explorer `SYS-002`, `FB-001`, `CON-002`; public-documentation/private-architecture scope; direct-source-observed, intended/partial |
| CyberAlchemy v2 | Private source-ledgered consolidation surface with an active local authority model | Owner-reviewed downloadable base repository for downstream construction | Project-local and pre-extraction; not standalone, released, deployed, or a workspace apex authority | `cyberAlchemy-v2/README.md#Repository-Objective`, `#Current-Gate`; `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md#Authority-Rule`; explorer `AUTH-001`, `AUTH-002`, `SYS-001`; private local scope; direct-source-observed |

Two feedback loops exist but must remain distinct:

```text
System convergence:
DomainSpec intent -> Arcanum bounded execution -> validation/evidence
       ^                                           |
       |-------- Saturn intended regulator --------|

CAV2 local authority:
source/import -> candidate -> narrow owner -> local authority/implementation
      ^                                         |
      |---- review, block, defer, demote --------|
```

Saturn’s intended regulator is not CAV2’s promotion loop. CAV2’s local promotion loop is not a System-5 controller for the workspace.

## Ownership and source-direction matrix

| Object / movement | Exact direction and CAV2 relation | Authoritative owner and legal transition | Forbidden effect | Direct source, explorer, scope, privacy, proof |
|---|---|---|---|---|
| Arcanum definitions | Public Arcanum → CAV2 reference/import ledger | Arcanum definitions governance retains upstream authority; only a distinct CAV2-local term may move through CAV2 definitions governance | CAV2 cannot redefine an Arcanum term for Arcanum | `arcanum/definitions/DEFINITIONS.md#DEF-ARC-CANONICAL-ARTIFACT`, `#DEF-ARC-PROMOTION-PATCH`; `cyberAlchemy-v2/authority/imports/definitions/MANIFEST.md#Purpose`; explorer `AUTH-003`, `AUTH-004`; vocabulary ownership; public → private; direct-source-observed, manifest scan stale as of 2026-06-19 |
| Framework constitutions | Public Arcanum → staged CAV2 import → scoped adaptation | Arcanum owns originals; CAV2 constitution governance may promote a provenance-bearing local rule | A manifest row or candidate constitution has no local force by itself | `cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md#CAV2-C11`, `#Promotion-Boundary`; `authority/promotion-policy.md#Required-Gates`; explorer `AUTH-005`, `AUTH-006`; local-rule adoption; public → private; candidate/direct-source-observed |
| Artifact validator | Arcanum implementation → planned re-rooted CAV2 adaptation | Constitution owners first; Task Session may implement only after owner gates | Copying Arcanum-root predicates or passing form tests cannot create CAV2 authority enforcement | `cyberAlchemy-v2/development/artifact-governance-import/PLAN.md#Implementation-layering`; `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md#Rules`; explorer `AUTH-006`, `OP-015`, `OP-016`; validator seam; public → private; committed plan at `fad671aed4ebf6c1405e4264a40d14e3ee33e740`, implementation unverified |
| CAV2 definitions, constitutions, disciplines, decisions | CAV2 candidates/evidence → narrow local owner | Definitions, constitution, discipline, or decision governance owns its own class | One authority kind cannot absorb another; validation and repetition do not promote | `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md#Authority-Kinds`, `#Narrowest-Owner-Rule`, `#Non-Collapse-Rules`; explorer `AUTH-002`, `SYS-001`; local governance; private; direct-source-observed, kind closure validator pending |
| DomainSpec evidence or prerequisite | Private DomainSpec owner → CAV2 evidence/required receipt | DomainSpec/compiler owner must issue the capability or support receipt; CAV2 may only consume it | Craft, Task Session, or a passing blocker test cannot manufacture upstream support | `cyberAlchemy-v2/SOURCE-MAP.md#Source-Cohorts`; IOLM `execution-receipt.json`; explorer `TRACE-OP-NEG-001`, `EDGE-005`; external-owner prerequisite; private → private; committed historical execution at `3c12cc0f39a16e95751e7be6a6d108a2fc21060a` |
| Inventory | Parent Inventory → discovery packet → direct-owner rebind | Inventory owner maintains the read model; destination owner interprets direct sources | Inventory cannot select, decide, or promote | `cyberAlchemy-v2/SOURCE-MAP.md#Ingest-Rules`; `authority/AUTHORITY-MODEL.md#Non-Collapse-Rules`; explorer `OP-007`, `OP-019`, `EDGE-006`; discovery only; mixed private/public metadata; current parent validation with warnings, no CAV2 machine index |
| Ontology | Source-ledgered candidate/evidence → ontology map/projection → owner-facing request | Ontology route owns candidate structure; source authority owner decides any state change | Projection cannot write authority, issue a verdict, or self-promote | `cyberAlchemy-v2/ontology/README.md`; `ontology/projections/README.md#Allowed-Projection-Inputs`; `arcanum/arcana/ontology-vault/SKILL.md:274-305`; explorer `AUTH-008`, `OP-008`; knowledge projection; private candidate using public method; direct-source-observed, exact Arcanum clauses partly dirty-current |
| Craft | Owner receipts/references → ledger → derived human/machine views | Craft owns record integrity and navigation, not semantic authority | It cannot make a plan executable, repair an external blocker, or promote a result | `cyberAlchemy-v2/.craft/ledger.yml`; `cyberAlchemy-v2/CRAFT.md#Contexts`; explorer `OP-005`, `OP-018`; project coordination; private; committed and clean at `32ee3c2c5a8e1c9f43f34017549cf1bea4fcf539` |
| Generated host skills | Accepted canonical Arcanum source → generation → sync/install → runtime acceptance | Public canonical owner precedes generator, host synchronization, installation, and behavioral owner | Generated `.agents`/`.claude` bytes are not canonical and cannot prove runtime parity | Arcanum generation contracts and August 5 building-system findings cited by explorer `OP-011`, `OP-012`, `OP-021`; host projection; public source → generated local package; direct-source-observed with known dirty/generated drift |
| Public/private publication | Private CAV2 or DomainSpec → scrubbed proposal → public owner review | Decision gate/source owner/public Arcanum owner must explicitly accept any public mutation | Naming a private concept publicly does not authorize copying its prose or claiming it shipped | `cyberAlchemy-v2/authority/boundaries.md#Public-And-Private`, `#Public-Disclosure`; `STABLE-REPOSITORY-CONSTITUTION.md#CAV2-C5`; explorer `AUTH-012`, `EDGE-008`; disclosure boundary; private → public; direct-source-observed, explicit gate required |

## Structural instantiation and import crosswalk

| Structure | Verified relation | Current witness | First absent transition | Evidence binding |
|---|---|---|---|---|
| Authority kind ↔ local authority surface | A CAV2 authority object/surface instantiates one locally owned authority kind; evidence supplies input to that owner | Active `AUTHORITY-MODEL.md` enumerates definition, constitution, discipline, decision, spec, runtime, and projection classes | Deterministic closure over all kinds remains pending | `authority/AUTHORITY-MODEL.md#Authority-Kinds`, `#Core-Flow`; explorer `AUTH-002`; private local authority; direct-source-observed |
| Proposed authority-object node ↔ ontology | Proposal requests an `instantiates` edge and provenance-bearing schema | Promotion-request document and worked example exist | `NODE-MODEL` amendment, stabilization decision, and validator do not | `ontology/promotion-requests/2026-06-23-authority-object-schema-proposal.md#The-structural-fix`, `#Gaps--next-route`; explorer `AUTH-009`; private candidate; non-executed |
| Arcanum definition ↔ CAV2 definition | Reference upstream identity; define only a distinct `CAV2-D*` local term | Definition import ledger contains 149 candidates | Current rescan and per-term owner promotion | `authority/imports/definitions/MANIFEST.md#Result`; explorer `AUTH-004`; public → private; candidate-only/stale scan |
| Arcanum constitution ↔ CAV2 local rule | Import then adapt with provenance, scope, owner, examples, non-examples, and validation mode | Artifact-governance frozen partition and committed Invoke plan | Two planned local constitutions and owner promotion | Artifact findings `#FROZEN-import-plan`; artifact `PLAN.md#Shared-SWU-manifest`; explorer `AUTH-006`, `OP-015`; public → private; planned/not executed |
| Arcanum validator ↔ CAV2 tool | Adapt/re-root rather than copy | Public validator exists; CAV2 landing path appears only in planning | Local tool, hook wiring, adversarial validation | `arcanum/framework/ARTIFACT-METADATA-CONSTITUTION.md#Rules`; artifact `PLAN.md`; explorer `AUTH-006`, `DEF-OP-005`, `DEF-OP-006`; implementation; public source/private target; unverified target |
| Ledger ↔ ontology ↔ authority | Ledger records evidence; ontology projects relations; authority owner decides | Existing lifecycle envelope and projection rules | Exact common machine schema and validator binding | Authority-harness findings `#What-the-skeptics-changed`; `ontology/projections/README.md`; explorer `AUTH-010`; private; historical research rebound to current rules |
| Canonical Arcanum ↔ generated packages | Generation projects accepted canonical capability contracts into hosts | Canonical and generated working surfaces exist | Clean parity, release, consumer install, behavioral runtime witness | Explorer `OP-011`, `OP-021`, `OP-022`; public canonical/generated host scope; dirty-current and divergent |

The candidate parallel “authority harness + separate ledger object + ontology object” was correctly rejected where it duplicated the existing lifecycle envelope. Shared fields do not make the three roles identical: authority owns state, ledger preserves evidence, and ontology projects relationships.

## Evidence, promotion, and control flows

### Evidence flow

```text
direct source / execution result
  -> receipt, validation report, telemetry, or ledger reference
  -> optional Inventory discovery card or ontology projection
  -> context selected for a named owner
```

This flow can increase confidence but never changes authority.

### Promotion flow

```text
candidate + provenance + direct source + bounded validation
  -> narrow owner identified
  -> owner-specific governance route
  -> explicit decision
  -> canonical owner mutation
  -> generation/synchronization/install only if separately required
```

Git commits, validator passes, repeated use, ontology representation, execution completion, and observability signals remain evidence—not owner decisions.

### Operational control flow

| Seam | Inputs and owner order | Output / first stop | Evidence binding |
|---|---|---|---|
| Invoke | Intent and source anchors → Define → Design evidence/validator → Plan → optional Distill/Dispatch validation | Candidate Define/Design/Plan and bounded handoff; stop on missing design evidence, invalid SWUs, or failed planning validation | Current Invoke contracts and CAV2 examples; explorer `OP-003`; private project/public method; direct-source-observed, examples mixed committed/dirty |
| Task Session | Exact selected SWU → readiness/context → mutation admission → one bounded execution → critical validation → closeout join | Execution terminal; synchronized result only after owner join | Current Task Session contract; explorer `OP-004`; execution control; direct-source-observed, full CAV2 chain unverified |
| Dispatch / Orchestrate | Persisted dispatch sheet → route validation → exact confirmation → spawn/join/gate/close | Coordination/action receipts; stop on missing correlation, result, or gate | Current confirmed dispatch and August 5 findings; explorer `OP-006`, `DEF-OP-008`; coordination; direct-current plus historical causal defects |
| Craft | Valid ledger and owner receipts → derived `CRAFT.md`/index | Record and navigation; stop on invalid reference/external blocker | CAV2 Craft files; explorer `OP-005`, `OP-018`; private; committed-clean |
| Inventory | Lookup/validate parent index → caller selects evidence → direct-source rebind | Discovery packet; stop on stale/missing direct owner | Parent Inventory and absent `cyberAlchemy-v2/inventory/index.json`; explorer `OP-007`, `OP-019`; non-authority; executed-current diagnostic |
| Ontology | Source-ledgered candidates → map/validate → owner proposal | Candidate graph; stop at attempted self-promotion or absent owner | CAV2 ontology and public Ontology Vault; explorer `AUTH-008`, `OP-008`; private candidate/public method; direct-source-observed |
| Validation | Frozen contract/fixtures/bytes → bounded runner → owner interpretation | Pass/block receipt; stop on failed or unrun critical validation | Positive/negative traces and upstream artifact validator; explorer `OP-009`, `DEF-OP-006`; bounded evidence; historical/candidate, never general acceptance |
| Observability | Invocation envelope/result → signal → possible reflection → explicit maintenance-owner decision | Signal/recommendation only; stop without maintenance authority | Sampled Invoke receipt with `authority_effect: none`; explorer `OP-010`; evidence; direct/historical |
| Runtime integration | Canonical acceptance → generation → sync → release → install → behavioral acceptance | Callable installed capability; stop at earliest absent transition | Intent-router absence witness and generated drift; explorer `OP-011`, `OP-012`, `OP-017`; runtime; no deployed proof |
| Continuation/Refresh | Terminal receipt + exact prerequisite → one-hop route → owner execution → receipt join | Joined result and continuity cursor; stop on stale, ambiguous, repeated, or non-pass receipt | Continuation contracts/negative fixtures; explorer `OP-013`, `DEF-OP-001`; workflow continuity; direct-source-observed, full real CAV2 join absent |
| Promotion | Proposal + direct source + validation → CAV2 narrow owner → decision → canonical mutation | Local authority artifact | `authority/AUTHORITY-MODEL.md`, `promotion-policy.md`; explorer `OP-014`, `AUTH-002`; private local authority; normative active route, no automatic transition |

## Current, candidate, intended, and deployed status

| Surface | Current | Candidate / intended | Deployed proof |
|---|---|---|---|
| CAV2 authority model | Active local source and owner routing; kind enforcement partly review-mode | Deterministic kind/closure validation | None beyond repository-local sources |
| Stable Repository Constitution | Declares both `candidate` and `project-local constitution`; safest reading is locally scoped but not proven fully promoted | Rule-specific promotion and deterministic validation | None |
| Artifact-governance integration | Research partition and committed Define/Design/Plan | Local schema/retention constitutions, adapted validator, hook | None |
| Authority-object schema | Promotion request only | Ontology amendment, stabilization decision, validator | None |
| CAV2 ontology | Candidate mapping/projection surface | Consequential generated projections after owner acceptance | No authority-writing runtime |
| Craft | Real committed project-local ledger and derived views | Continued coordination | Local repository operation only; not semantic authority |
| Inventory | Parent machine index is available with 146 historical uncontrolled-tag warnings | Decide whether CAV2 owns an index | No CAV2 machine index |
| Typed-test recovery | Untracked candidate-local receipt reports 25 tests and V-OEWFR-01..13 passing | Governance reconciliation via `HN-7362EC2F08B7` | No synchronized lifecycle, browser acceptance, release, or deployment |
| Intent-router | Private historical tests only | Canonical Arcanum owner, generated package, adapter | No Bootstrap selection, install, runtime adapter, or deployment |
| Saturn | Public documentation describes intended loop and says it is assembling | Closed causal convergence loop | No shipped closed-loop witness |
| CAV2 standalone base/mold | Pre-extraction private consolidation surface | Owner-reviewed downloadable base | No extraction, release, downstream cast, or deployment |

## Finite traces

### Positive trace: bounded candidate-local recovery

```text
CAV2 recovery intent
  -> Invoke Define/Design/Plan
  -> design validator fixed point
  -> seven bounded SWUs
  -> explicitly authorized candidate-local fast lane
  -> implementation within declared targets
  -> no-network V-OEWFR-01..13
  -> 25 builder tests reported pass
  -> consolidated prototype receipt
  -> Handoff Notice HN-7362EC2F08B7
  -> STOP at candidate-local validation
```

Evidence: typed-test-recovery `INVOKE-RECEIPT.json`, `planning/SWU-MANIFEST.json`, and fast-lane receipt; explorer `TRACE-OP-POS-001`; private, untracked, dirty-worktree-only candidate evidence. It does not prove current postimages, lifecycle reconciliation, browser acceptance, promotion, release, deployment, or production readiness.

### Negative trace: external support correctly stops work

```text
IOLM SWU-00C-B selected
  -> DomainSpec/compiler cross-feature support required
  -> targeted regression confirms CROSS_FEATURE_UNSUPPORTED
  -> Decision Gate option 1 remains selected
  -> required upstream support receipt absent
  -> Task Session blocks
  -> Craft exposes blocker
  -> no mutation, no successor, authority effect none
```

Evidence: IOLM `execution-receipt.json`, `DECISION-GATE.md`, `BLK-DSV2-BTE-SWU-READINESS-CONTRADICTION-001`; explorer `TRACE-OP-NEG-001`; private, committed historical execution at `3c12cc0f39a16e95751e7be6a6d108a2fc21060a`. It proves the historical fail-closed route, not current upstream behavior.

### Import trace: first unproved transition

```text
Arcanum constitution/tool
  -> CAV2 manifest staging
  -> frozen Tier-1/Tier-2/skip partition
  -> committed Invoke Define/Design/Plan
  -> STOP
  -> future local constitution promotion
  -> future validator Task Session
  -> future hook and adversarial validation
```

No inspected evidence crosses the stop.

## Conflicts, duplication, stale state, defects, and missing links

| ID | Finding | Adjudication and owner |
|---|---|---|
| `C-01` | `STABLE-REPOSITORY-CONSTITUTION.md` says both candidate and project-local authority | Treat as locally scoped candidate, not fully promoted canon; constitution governance must reconcile wording |
| `C-02` | Import ledgers call themselves active but the definition/constitution scan dates are old | “Active ledger” does not mean current inventory; CAV2 definitions/constitution owners must rescan |
| `C-03` | Artifact plan says Tier-1 staging occurred while original manifest is stale | Staging evidence survives, comprehensive current coverage does not |
| `C-04` | Active authority model versus candidate ontology authority table | Authority model owns state; ontology table is a non-authority routing view |
| `C-05` | `CAV2-C17 build-from-owned` is useful but still candidate | Use as research discipline, not deterministic promoted enforcement |
| `C-06` | Proposed parallel authority harness/ledger/ontology object | Reject duplicate authority rail; preserve authority, record, and projection as distinct roles |
| `C-07` | Already-owned promotion and hygiene principles appear in import candidates | Skip duplicate promotion; cite existing owner and adapt only the missing integration |
| `C-08` | Generated Arcanum packages diverge from canonical dirty-current sources | No runtime inference until clean parity is restored or divergence explicitly rejected |
| `C-09` | Full upstream Artifact Constitution validation is red while bounded self-tests pass | Import only as a limited form mechanism; do not label it comprehensive authority enforcement |
| `C-10` | Metadata enforcement/parser remains advisory or candidate | Separate metadata decision from schema-form validation |
| `C-11` | Historical Orchestrate action-ID/input/correlation defects | Coordinator receipt does not prove task semantics; require exact correlation and joined result |
| `C-12` | No CAV2 machine Inventory index | Decide explicitly whether CAV2 consumes parent discovery or owns a standalone index |
| `C-13` | Stored candidate-local postimages may differ from current modified bytes | Freeze and rerun against one attributed baseline before further claims |
| `C-14` | Layer map says public docs omit Saturn/DomainSpec, but current docs contain them | Layer-map deployed-surface claim is stale; publication owner must reconcile it, and current docs still do not prove loop deployment |
| `C-15` | Broader Git history traversal hit malformed `refs/codex/turn-diffs/...` | Repository-maintenance residue; it limits stronger historical conclusions but did not block this synthesis |
| `C-16` | No complete positive Invoke → selected SWU → admission → execution → validation → Refresh join witness | Build and freeze exactly one trace before claiming end-to-end integration |
| `C-17` | Intent-router private tests exist without canonical Arcanum capability, generated package, install, or adapter | Runtime integration stops at missing public canonical ownership |
| `C-18` | Standalone CAV2/base/mold claim lacks extraction witness | Route through CAV2-C10 and public/private review; do not infer existence from objective prose |

The systems explorer’s three “blockers”—no meta-authority edge, no standalone witness, and exclusion of dirty user-owned bytes—are research negatives or evidence ceilings, not coordinator blockers. They did not prevent the explorer or this synthesis from returning.

## Hypothesis verdicts

| Hypothesis | Verdict |
|---|---|
| CAV2 is an Arcanum consumer | Qualified verified: it consumes public framework evidence, methods, routes, and import candidates while upstream owners retain authority |
| CAV2 is an adapter | Verified at bounded seams: local paths, predicates, scope, and privacy require adaptation rather than verbatim authority transfer |
| CAV2 is a private authority spine | Verified locally: active local owners, definitions, constitutions, decisions, import ledgers, and promotion policy; no workspace-wide scope |
| CAV2 is a consolidation surface | Verified: direct sources describe source-ledgered consolidation without automatic ownership |
| CAV2 should consolidate all four systems into one authority | Rejected: DomainSpec intent, Arcanum execution, Saturn regulation, and CAV2 local promotion have separate owners and effects |
| CAV2 is a meta-authority | Contradicted as a current fact: no edge authorizes it to govern Arcanum, DomainSpec, Saturn, or source owners |
| CAV2 is a Beer System-5 implementation | Analogy only: no repository proof makes CAV2 the regulator of the four-system loop, and the two recursive control loops must not be collapsed |
| CAV2 is a reusable mold | Candidate metaphor only: a future owner-reviewed base may carry reusable patterns, but there is no extracted mold, enforcement package, or downstream cast |
| CAV2 is a standalone downloadable base | Intended only; CAV2-C10 requires a separate extraction decision and witness |
| CAV2 can reverse-import private prose into public Arcanum | Forbidden absent scrub, source-owner review, decision gate, and explicit public-owner mutation |

## Owner-routed operator playbooks

### Adopt an Arcanum pattern into CAV2

1. Re-scan current public owner sources.
2. Classify each item as reference, local adaptation, or already-owned/skip.
3. Preserve source identity, provenance, privacy, scope, owner, examples, non-examples, and validation mode.
4. Route the local rule through definitions or constitution governance.
5. Only after promotion, route validator code through Task Session.
6. Run bounded self-tests plus an adversarial write/hook witness.
7. Record the owner decision separately from validation and Git history.

### Execute bounded CAV2 work

1. Select one exact SWU against a frozen baseline.
2. Require current producer and external-owner receipts.
3. Admit mutation only after readiness/context validation.
4. Execute within declared scope.
5. Run acceptance-critical validation.
6. Join the exact Refresh/closeout owner receipt.
7. Update Craft as record/navigation.
8. Route any promotion separately.

### Advance an ontology candidate

1. Bind every node/edge to direct sources and source owners.
2. Validate projection-only effects.
3. Submit a named owner-facing promotion request.
4. Stabilize contested schema through decision gate.
5. Patch the canonical owner artifact.
6. Only then implement a validator or generated projection.
7. Preserve the invariant that ontology output never writes authority.

### Establish runtime integration

1. Obtain canonical public Arcanum owner acceptance.
2. Freeze a clean canonical commit.
3. Generate and checksum host packages.
4. Synchronize and install into the explicit consumer.
5. Test callable behavior with exact inputs.
6. Add the CAV2 adapter only through its owner.
7. Keep release and deployment as later witnessed transitions.

### Resolve a DomainSpec/compiler prerequisite

1. Stop CAV2 mutation.
2. Preserve the failing fixture and exact required capability.
3. Route to the DomainSpec/compiler owner.
4. Accept only an owner-issued support receipt.
5. Rerun readiness against current bytes.
6. Resume the selected CAV2 unit without letting Craft or a test result substitute for authority.

### Extract or publish CAV2

1. Invoke CAV2-C10 through decision gate/constitution governance.
2. Define the standalone boundary and owners.
3. Scrub private DomainSpec, CAV2, and Saturn material.
4. Obtain source-owner and public-owner review.
5. Produce an extraction witness and independent validation.
6. Separately establish release, installation, downstream use, and deployment before using those terms.

## Verdict

The defensible model is:

- Arcanum owns public portable capability and governance machinery.
- DomainSpec remains a private structured-intent and implementation owner.
- Saturn remains the intended convergence loop, not a proved shipped regulator.
- CyberAlchemy v2 is the private consolidation and local-authority spine that consumes evidence from those systems without becoming their owner.

CAV2 is already more than a passive folder: its local authority model, import ledgers, promotion routes, Craft surface, and bounded implementation evidence are real. It is less than a meta-system: no evidence establishes standalone extraction, cross-system authority, one integrated runtime, System-5 operation, reusable downstream molds, synchronized end-to-end execution, or deployment.

## Residue and reviewer routing

1. Reconcile candidate/project-local constitution status and decide whether `CAV2-C17` becomes promoted/deterministic — constitution-governance reviewer.
2. Re-scan definition and constitution imports; execute or retire artifact-governance Tier 1 — import owners, then Task Session reviewer.
3. Stabilize or reject the authority-object schema before closure validation — ontology and decision-gate reviewers.
4. Freeze one clean positive Invoke-to-synchronized-Task-Session witness — operational/runtime reviewer.
5. Reconcile fast-lane evidence through `HN-7362EC2F08B7` without retroactive claim inflation — lifecycle reviewer.
6. Restore or reject canonical/generated parity and rerun bounded validation on one frozen snapshot — Arcanum generation/runtime reviewer.
7. Decide whether CAV2 owns a machine Inventory index or intentionally consumes the parent read model — Inventory/CAV2 owner reviewer.
8. Reconcile stale Saturn publication claims and separately verify any live publication — publication reviewer.
9. Repair the malformed Codex Git ref before extending history-sensitive claims — repository-maintenance reviewer.
10. Preserve all negative edges: Inventory/ontology/validation/observability/generated projection/Git commit → promotion are forbidden; private prose → public Arcanum requires explicit owner-reviewed extraction.

```json
{
  "ACTION_RECEIPT": {
    "action_id": "spawn-0004",
    "assigned_identity": "Noether, Emmy",
    "role": "synthesizer",
    "dispatch_id": "2026-08-05-arcanum-cav2-integration-research",
    "run_id": "cav2-integration-run-01",
    "status": "complete",
    "scalar_validation": "pass",
    "validation_details": {
      "explorer_receipts_joined": 3,
      "explorer_receipts_passed": 3,
      "required_relationship_model_included": true,
      "four_system_role_map_included": true,
      "ownership_and_source_direction_included": true,
      "structural_and_import_crosswalk_included": true,
      "operational_seams_and_finite_traces_included": true,
      "hypotheses_adjudicated": true,
      "public_private_boundary_preserved": true,
      "canonical_generated_boundary_preserved": true,
      "evidence_ceilings_preserved": true,
      "repository_writes": 0,
      "external_web_used": false,
      "memory_used": false
    },
    "blockers": [],
    "native_return_handle": "agent-return://2026-08-05-arcanum-cav2-integration-research/cav2-integration-run-01/spawn-0004/synthesizer",
    "residue": [
      "constitution candidate and project-local status requires owner adjudication",
      "definition and constitution import manifests require current rescans",
      "artifact-governance Tier-1 remains planned rather than implemented",
      "authority-object schema remains unstabilized and unvalidated",
      "full positive Invoke-to-synchronized-Task-Session witness is absent",
      "candidate-local fast-lane evidence awaits lifecycle reconciliation",
      "canonical and generated Arcanum surfaces require clean parity resolution",
      "CyberAlchemy-v2 has no local machine Inventory index",
      "standalone extraction, runtime installation, release, deployment, System-5, meta-authority, and mold claims remain unproved",
      "malformed Codex Git reference limits broader history traversal"
    ],
    "reroute": [
      {
        "target": "reviewer-authority",
        "reason": "Review ownership, promotion, privacy, constitution status, and hypothesis adjudications."
      },
      {
        "target": "reviewer-operational",
        "reason": "Review Invoke, Task Session, Craft, validation, observability, runtime seams, finite traces, and dirty-versus-committed ceilings."
      },
      {
        "target": "reviewer-systems",
        "reason": "Review the four-system model, causal-loop separation, stale publication claim, and rejection of meta-authority/System-5/mold as current facts."
      }
    ]
  }
}
```
