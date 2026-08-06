# Architecture Plan — Anime.js AKV Query Contract Readiness

## Architecture intent

Make the QRY-003 terminal contract implementable and falsifiable as a private candidate without allowing planning evidence, validation receipts, or user approval for this package to become ontology or execution authority.

## Source contracts

| Contract | Source | Binding |
| --- | --- | --- |
| SC-QRY | Refine `08-query-contract-matrix.json` | SHA-256 `537e05842d2089ceab84b24e936ab0849292465cbabd6ee36f6dda4cab4df342` |
| SC-BLOCK | Blocked Task Session `CLOSEOUT-PREFLIGHT.json` | SHA-256 `8609842f88c8142406381eee0b95e2ec55a83296bde8b1ccd731b436e04245c3` |
| SC-DEFINE | `SPEC.md` | SHA-256 `5f4cbc51d7211b65c5679a3125e3b3f0ed935b32488cf23c516c73663f024530` |

## Closed scope

- System of interest: `animejs.akv.query-contract-readiness`
- DesignScopeManifest: `DESIGN-SCOPE-MANIFEST.json`, input digest `51c6b70bec610a003e024e083a340e08943718204b9468da43c5cc5a7b25e725`
- DesignDenominatorReceipt: `DESIGN-DENOMINATOR-RECEIPT.json`, receipt digest `577c13a5cabf4f96e5dc3199f8b856323a70fbd2173e48bf72191f73ec8b27b3`
- DesignSelectionResult: `DESIGN-SELECTION-RESULT.json`, result digest `4f393169d0487bfe83f4c7c22bbc0d7c3bf4188bee2ebde7296d15b48ccc8722`
- Evidence state: `design-validator-pass`

## View 1 — Context

| Neighbor | Role | Boundary |
| --- | --- | --- |
| Closed Refine run | Supplies the accepted query matrix. | Read-only, digest-bound source evidence. |
| Invoke package | Owns Define, Design, Plan, work-pack, and readiness-audit configuration. | Planning authority only. |
| Material-package producer | Stages exact candidate bytes after an explicit unit decision. | Must produce a current package and producer receipt; no direct candidate mutation. |
| Task Session | Applies one admitted material package and runs exact validation. | One selected SWU, exact write union, joined closeout owner receipt. |
| Invoke Refresh | Synchronizes declared plan/status targets after a terminal Task Session receipt. | Exact target inventory and typed deltas only. |
| Relation-repair package | Consumes the query result as a prerequisite. | Separate Plan and execution receipts. |
| Ontology Vault/Harness | May later decide candidate ontology admission. | Separate confirmation and promotion authority. |

No natural-person UI, rendered surface, network interface, deployment target, durable store, queue, or concurrent writer exists in this design.

## View 2 — High-level structure

```text
planning/
  SPEC + ARCHITECTURE + WORK-PACK
          |
          v
material package (future, content-addressed)
          |
          v
candidate/query-contract/
  schema/query-receipt.schema.json
  policy/qry003-terminal-contract.json
  MIGRATION.md
  validate-query-receipt.mjs
  qry003-terminal-cases.json
  run-terminal-fixtures.mjs
          |
          v
execution evidence (future, exact path)
          |
          v
Invoke Refresh closeout receipt
```

The material package is the only bridge from planning to candidate mutation. Planning artifacts never write candidate files directly.

## View 3 — Low-level components

| Component | Responsibility | Inputs | Outputs |
| --- | --- | --- | --- |
| QueryReceipt schema | Structural XOR and field constraints for success/abstention receipts. | Candidate receipt JSON. | schema verdict. |
| QRY-003 terminal policy | Closed codes, precedence, terminal-path expectations, algorithm version. | Refine query matrix. | immutable policy data. |
| Migration note | Version transition and historical immutability rules. | old/new contract identity. | reviewable migration contract. |
| Receipt validator | Semantic checks not expressible or convenient in the schema. | schema, policy, candidate receipt. | typed pass/fail findings. |
| Terminal fixtures | Eight source-bound positive/negative cases. | policy and Refine planned fixtures. | deterministic case inputs and expected results. |
| Fixture runner | Executes every fixture, rejects missing/extra cases, writes one receipt. | validator and fixtures. | content-addressed validation report. |
| Readiness configuration | Simulates graph, writes, commands, receipts, closeout, and admission without execution. | final Plan artifacts and current schemas. | audit report and Refresh signal pack. |

Dependency direction is inward: runner -> validator -> schema/policy; fixtures are data inputs; planning and source evidence are never imported by candidate runtime code.

## View 4 — Workflow process

1. Invoke authors and validates Define, Design, and Plan.
2. Work Pack Readiness Audit snapshots the final package and simulates both SWUs.
3. The audit exposes `plan_contract_status` separately from `runtime_admission_status`.
4. While the current material package is absent, runtime admission remains blocked and no SWU is selectable.
5. After an explicit unit decision, the material-package owner stages exactly the declared files and returns a schema-valid producer receipt.
6. The audit is rerun against the new immutable frontier.
7. Only a passing runtime-admission result plus explicit SWU selection allows Task Session resolution.
8. Task Session builds a fresh strict context pack, revalidates admission, applies the package, and runs exact commands.
9. A terminal receipt triggers one exact `invoke:refresh:apply-approved` closeout hop.
10. Refresh updates only the declared planning targets, validates them, returns a separate owner receipt, and emits but never executes the unique successor.

Failure at any step preserves receipts and stops before the next mutation boundary. Historical query receipts are never rollback targets.

## View 5 — Decision flow

| Decision | Rule | Outcome |
| --- | --- | --- |
| Is the Plan graph and contract complete? | Readiness audit `plan_contract_status == pass`. | Continue to runtime-admission evaluation; otherwise Invoke Refresh repair. |
| Is current material evidence present and exact? | Package, producer receipt, paths, digests, owner, authority, and validation all match. | Admit candidate mutation; otherwise block before Task Session. |
| Which SWU may run? | Exactly one explicit selection from the dependency-ready frontier. | Select QRY-001 first; never infer QRY-002. |
| Does a receipt represent success? | non-empty selected IDs and null abstention. | accept success shape. |
| Does a receipt represent abstention? | empty selected IDs and one declared primary code. | accept abstention shape. |
| Which simultaneous failure is primary? | First applicable code in the total precedence. | preserve all other gaps as subordinate. |
| May candidate evidence enter an ontology? | Only a separately confirmed Ontology Vault/Harness owner decision. | defer; validation pass has no authority effect. |

## View 6 — Dependency and interface

| Interface | Producer | Consumer | Contract |
| --- | --- | --- | --- |
| Refine query matrix | Refine | Invoke/candidate package | exact source digest and selectors. |
| material package | selected package producer | Task Session admission | package schema, producer receipt schema, exact material writes. |
| mutation-admission request | Task Session | readiness verifier | live control artifacts, dependency frontier, complete write union, commands, owner classes. |
| executor receipt | Task Session executor | governance runner | exact output refs and validation result. |
| governance terminal receipt | Task Session | Continuation Router/Invoke Refresh | canonical terminal receipt schema and semantic checks. |
| refresh report | Invoke Refresh | Task Session closeout join | package-local refresh receipt schema and exact expected path. |
| readiness report | Work Pack Readiness Audit | human selection/Invoke Refresh | audit-only; selected unit remains none. |

## Significant artifact/evidence scenario

| Stimulus | Preconditions | Ordered response | Failure/recovery | Observable evidence | Acceptance owner |
| --- | --- | --- | --- | --- | --- |
| QRY-003 fixture set is proposed for candidate execution. | Design fixed point; final Plan snapshot; explicit SWU selection; current material package and receipt. | verify admission -> apply exact bytes -> run eight cases -> emit terminal receipt -> join Refresh receipt. | Any mismatch blocks; preserve staged package and receipts; do not select successor. | admission receipt, fixture report, governance terminal receipt, Refresh receipt. | Task Session plus Invoke Refresh for closeout. |

## Required extensions selected by Design validator

### Authority and trust

- Planning approval authorizes only this run root.
- Candidate validation has `authority_effect: none`.
- Task Session admission authorizes exact candidate bytes, not ontology admission.
- Ontology selection requires separate owner confirmation and receipts.

### State and event

```text
planned
  -> material-prepared
  -> runtime-admissible
  -> explicitly-selected
  -> executing
  -> validation-pass | blocked
  -> closeout-joined
  -> successor-exposed
```

Forbidden transitions include planned -> executing, material-prepared -> ontology-admitted, validation-pass -> successor-executed, and blocked -> selected without changed evidence.

### Failure and compensation

- No product mutation occurs before material admission.
- Candidate files are applied only from a content-addressed package.
- Failure preserves the package, executor evidence, and blocker fingerprint.
- Compensation is restore-from-admitted-package baseline for candidate bytes only; historical receipts and source research are immutable.
- Closeout failure preserves the execution result but keeps the overall Task Session blocked.

### Integration and versioning

- The candidate contract version is independent of Anime.js library version.
- `algorithm_version` identifies query-selection semantics.
- The fixture runner rejects policy/schema version mismatches.
- Consumer integration must bind exact file digests and cannot depend on planning Markdown at runtime.

### Migration and rollout

- QRY-003 candidate-v1 affects new candidate receipts only.
- Historical receipts retain original bytes and version.
- There is no bulk migration, deployment, publication, or release in this package.
- Later consumers must opt into candidate-v1 through their own owner contract.

### Quality

- exactly six declared abstention codes;
- exactly eight fixture IDs;
- zero undeclared codes;
- total precedence order is byte-identical to the Refine matrix;
- success/abstention XOR holds for every fixture;
- the runner exits nonzero on missing, duplicate, extra, or failing fixtures.

### Validation contracts

See `VALIDATION-CONTRACTS.md`. Design witnesses are planned contracts and do not count as Plan or execution evidence.

## Concern-to-view trace

| Concern | Disposition | Owner | Selected output | Evidence |
| --- | --- | --- | --- | --- |
| authority | required | authority-owner | authority-trust | no-authority normative rule |
| state-event | required | workflow-owner | state-event | terminal precedence rule |
| failure | required | query-contract-workflow-owner | failure-compensation | authored fail-closed concern |
| reliability | required | query-contract-service-owner | quality | eight terminal witnesses |
| integration | required | interface-owner | integration-versioning | two declared interfaces |
| migration | required | migration-owner | migration-rollout | stored historical receipt boundary |
| validation | required | design-owner | validation-contracts | rules, effect, and Define acceptance |

## Decision log

| ID | Status | Decision | Rejected alternative | Evidence |
| --- | --- | --- | --- | --- |
| D-001 | accepted for candidate Plan | Split prior SWU-AKV-NV-001 into five units: policy, schema, migration, validator, and replay. | One bundled schema/validator/migration/fixtures SWU or a still-bundled two-unit split. | Distill atomicity and blocked Task Session evidence. |
| D-002 | accepted for candidate Plan | Use a stable private development candidate root. | Write directly to a future ontology root. | Owner boundary and no admitted ontology. |
| D-003 | accepted for candidate Plan | Node built-ins plus JSON; no new package root. | Add dependencies to obtain validation tooling. | Bounded local contract and repository browser/runtime policy. |
| D-004 | accepted for candidate Plan | Separate plan-contract pass from runtime-admission pass. | Treat completed planning as Task Session readiness. | Work Pack Readiness Audit contract. |

## Risks

| Risk | Mitigation | Owner |
| --- | --- | --- |
| Contract policy and validator diverge. | Runner binds exact policy/schema versions and fails on mismatch. | query-contract-candidate-owner |
| Historical receipts are rewritten. | Migration contract and negative fixture prohibit rewrites. | migration-owner |
| A stale material package is applied. | Digest-bound producer receipt and live admission revalidation. | task-session-owner |
| Plan closeout cannot synchronize. | Exact target inventory, baseline rule, typed deltas, expected Refresh receipt, and successor policy. | invoke-refresh-owner |
| Validation is mistaken for ontology authority. | Explicit authority extension and separate ontology route. | ontology-vault-owner |

## Gate result

- Status: pass
- Six views: complete
- Selected extensions: complete
- Fixed-point Design evidence: pass
- Planned witnesses executed: 0
- Product evidence: none
- Downstream route: Invoke Plan
