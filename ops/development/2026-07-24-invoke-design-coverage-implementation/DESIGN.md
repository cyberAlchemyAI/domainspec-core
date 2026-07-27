# Design: Invoke Design Coverage

Status: approved L1 authoring output.

Evidence state: `authored-complete`.

Source contracts: `DEFINE.md`, `GLOSSARY.md`, `DESIGN-SCOPE-MANIFEST.yaml`,
`CONCERN-LEDGER.md`, `UX-PLAN.md`.

## 1. Context view

```text
approved Define artifacts + exact target footprint
  -> Invoke author writes DesignScopeManifest
  -> independent design-scope extractor
  -> DesignDenominatorReceipt
  -> design-selection validator
       | union authored + extracted signals
       | classify + own + disposition
       | select baseline + extensions/companions
       | run pass two and compare fixed point
  -> DesignSelectionResult
       | authored-complete / design-validator-pass
       v
     Invoke Plan
       -> runnable validators, fixtures, and plan-evidence state
```

Inventory and observability may reference receipts but cannot set any evidence
state.

## 2. High-level structure view

| Component | Responsibility | Explicit non-authority |
| --- | --- | --- |
| `DesignScopeManifest` schema | close normalized inputs, exclusions, signals, unknowns, and input digest | cannot prove completeness by itself |
| `design_scope_extractor.py` | extract signals from exact selectors and emit a denominator receipt | cannot select outputs or validate its own receipt |
| `DesignDenominatorReceipt` schema | bind detector identity/version, inputs, signals, and missing inputs | cannot advance Design evidence state |
| `design_selection_validator.py` | verify schemas/digests, total binding, ownership, predicates, two-pass fixed point, and evidence-state legality | cannot author the manifest or claim Plan evidence |
| `DesignSelectionResult` schema | carry concerns, ownership, dispositions, selected outputs, diagnostics, fixed point, and evidence state | cannot promote templates |
| Design mode contract | order phases and enforce gate behavior | cannot execute Plan evidence |
| architecture templates | preserve six views and add concern/extension bindings | cannot create universal concern families |
| UX template | represent changed human semantic meaning and recovery | does not trigger without actor plus semantic change |
| frozen fixture corpus | independent denominator and exact expected selection | test evidence only |
| Invoke validation runner | execute schemas, controls, mutations, parity, and leakage checks | cannot release registry or runtime readiness |

### Planned public contracts

```yaml
design_scope_manifest:
  schema_version: 1
  manifest_id: string
  target_id: string
  target_footprint: object
  source_contracts: [source_binding]
  human_actors: [actor]
  rendered_surfaces: [surface]
  interfaces: [interface]
  stores: [store]
  queues: [queue]
  writers: [writer]
  normative_rules: [rule]
  effects: [effect]
  data_and_log_sinks: [sink]
  deployment_targets: [deployment]
  compatibility_boundaries: [boundary]
  quality_claims: [claim]
  acceptance_and_readiness_claims: [claim]
  unknowns: []
  input_digest: sha256
  authored_by: owner_id
```

```yaml
design_denominator_receipt:
  schema_version: 1
  manifest_id: string
  manifest_input_digest: sha256
  detector_id: invoke-design-scope-extractor
  detector_version: string
  detector_owner: spellcraft
  inspected_selectors: [selector]
  extracted_signals: [signal]
  authored_concern_ids: [concern_id]
  denominator_signal_ids: [signal_id]
  unbound_signal_ids: []
  missing_detector_inputs: []
  verdict: pass | block
  receipt_digest: sha256
  validator_owner: invoke-design-selection-validator
```

```yaml
design_selection_result:
  schema_version: 1
  manifest_id: string
  manifest_input_digest: sha256
  denominator_receipt_digest: sha256
  concerns: [concern_binding]
  selected_outputs: [output_id]
  pass_1_digest: sha256
  pass_2_digest: sha256
  fixed_point: true
  evidence_state: authored-complete | design-validator-pass
  diagnostics: [diagnostic]
  result_digest: sha256
```

## 3. Low-level component view

### Manifest closure

1. Normalize paths and selectors relative to the repository root.
2. Reject unresolved globs, duplicate identities, missing referenced inputs,
   malformed exclusions, or any non-empty `unknowns`.
3. Canonically sort sets by stable identity.
4. Compute `input_digest` over all normalized fields except the digest itself.
5. Preserve the author identity and exact source digests.

### Independent extraction

For each manifest field class, emit normalized signals:

```text
actor/surface -> human-semantics candidates
interface/compatibility -> integration or migration candidates
store/queue/writer -> persistence, ordering, and concurrency candidates
rule/claim -> authority, validation, or quality candidates
effect -> authority, security, failure, or reversibility candidates
sink -> privacy/data candidate
deployment -> rollout/operations candidate
```

The extractor rejects a manifest written by its own detector identity, stale
input digests, selectors it cannot inspect, and duplicate signal IDs. It does
not decide the final concern class.

### Primary concern precedence

Apply the first matching primary boundary:

1. authority/admission;
2. security/adversarial trust violation;
3. state/event legality;
4. persistence/order/idempotency;
5. failure/compensation;
6. reliability/service commitment;
7. integration/evolving contract;
8. migration/representation conversion;
9. rollout/deployment transition;
10. privacy/data lifecycle;
11. performance/measurable resource claim;
12. UX/human semantic consequence;
13. validation/normative observable claim.

Cross-references may be added only after one primary owner is bound.

### Disposition and selection

```text
if input missing or unknown, signal unbound, owner unresolved,
   receipt stale/self-issued, or prior result inconsistent:
    disposition = block
elif required predicate is true:
    disposition = required
elif bounded hypothesis has owner + evidence + revisit condition:
    disposition = recommended
elif detector is negative and cited selectors prove the boundary:
    disposition = not-applicable-with-rationale
else:
    disposition = block
```

Only `required` selects a companion or extension.

### Two-pass fixed point

```text
pass1 = extract -> classify -> own -> disposition -> select -> digest
pass2 = repeat from the same manifest and receipt inputs -> digest
if pass1.digest != pass2.digest:
    block CHANGED_PASS_TWO
else:
    emit fixed_point=true
```

There is no automatic pass three. Changed inputs require a superseding manifest
and a new run.

### UX predicate

```text
ux_required =
  exists human_actor where actor is a natural person
  and exists rendered_surface whose semantic contract is new or changed
  and the actor reads, decides, acts, recovers, navigates,
      or performs assistive operation through that surface
```

Files, APIs, receipts, or generated evidence alone do not trigger UX.

### Evidence-state rule

- Manifest and planned contracts complete: `authored-complete`.
- Validator passes exact manifest, denominator, ownership, selection, and fixed
  point: `design-validator-pass`.
- Plan executes version-bound witnesses: separate
  `plan-evidence-pending|pass|fail` receipt; never stored in the Design result.

## 4. Workflow process view

```text
Spellcraft freezes independent fixture denominator
  -> add schemas
  -> implement extractor
  -> implement selection validator
  -> prove negative, positive, bounded, and mutation fixtures
  -> revise Design contract
  -> revise architecture and UX templates
  -> integrate aggregate validation
  -> regenerate runtime projections
  -> run generic Define -> Design -> Plan example
  -> audit public/private boundary and lifecycle receipts
```

Every source mutation is one SWU and uses a predeclared closeout contract.

## 5. Decision flow view

```text
approved Define and exact source contracts?
  no -> block MISSING_DESIGN_INPUT
  yes -> close manifest

manifest closed and digest valid?
  no -> block MANIFEST_NOT_CLOSED
  yes -> independent extraction

denominator receipt current and non-self-issued?
  no -> block INVALID_DENOMINATOR_RECEIPT
  yes -> total concern binding

every signal bound and every required owner exact?
  no -> block UNBOUND_SIGNAL | OWNER_UNRESOLVED
  yes -> select required outputs

pass two unchanged?
  no -> block CHANGED_PASS_TWO
  yes -> design-validator-pass

Plan evidence present?
  no -> plan-evidence-pending
  yes -> Plan validates independently
```

## 6. Dependency and interface view

| Producer | Consumer | Contract | Failure rule |
| --- | --- | --- | --- |
| Invoke Design author | extractor | `DesignScopeManifest` | unknown, missing, unresolved, or digest mismatch blocks |
| extractor | selection validator | `DesignDenominatorReceipt` | stale, self-issued, partial, or duplicate signal receipt blocks |
| selection validator | Invoke Design | `DesignSelectionResult` | unbound signal, missing owner, false N/A, or no fixed point blocks |
| Invoke Design | architecture/UX companions | selected output IDs and concern bindings | recommended or N/A cannot select a required companion |
| Invoke Design | Invoke Plan | `design-validator-pass` plus planned witness contracts | authored-only state routes only to remediation Plan |
| Plan | fixture runner | versioned schemas, scripts, fixtures, expected results | planned fixture names are not evidence |
| canonical Invoke | bootstrap | validated canonical source | generated-first edits reject |
| Spellcraft | promotion owner | lifecycle receipts and public/private audit | test pass alone cannot promote |

## Decisions

| ID | Decision | Alternatives rejected | Consequence and revisit trigger |
| --- | --- | --- | --- |
| DVC-D01 | three schemas plus two deterministic components | one opaque result document | interfaces remain independently testable; revisit only if receipt joins duplicate data |
| DVC-D02 | exactly two passes | open-ended convergence | bounded execution and deterministic block; revisit only with a proved monotonic algorithm |
| DVC-D03 | primary concern precedence plus overlays | multi-owner first classification | singular accountability; revisit when a counterexample cannot be represented |
| DVC-D04 | human semantic predicate selects UX | UI keyword or all evidence artifacts | bounded UX coverage; revisit on a missed human-consequence fixture |
| DVC-D05 | six views plus triggered extensions | universal headings/families | preserves navigation without checklist inflation |
| DVC-D06 | remediation Plan may implement missing validator | require validator before planning it | avoids bootstrap deadlock while preserving evidence-state ceiling |
| DVC-D07 | first SWU freezes fixtures | implement schemas first | denominator remains independent of implementation |
| DVC-D08 | Spellcraft owns public lifecycle | Invoke self-mutation | preserves owner chain and generated-surface discipline |

## Risks and controls

| Risk | Control |
| --- | --- |
| authored fixtures mirror implementation omissions | freeze research-derived fixtures before schemas/scripts |
| detector becomes a general repository scanner | inspect only manifest-declared selectors and field classes |
| every project selects every extension | bounded positive controls with exact expected selections |
| false N/A returns through prose | require detector-negative receipt and cited selectors |
| UX becomes UI-only | operator-visible evidence and recovery fixtures |
| validator pass implies runnable behavior | separate Design result from Plan evidence receipt |
| dirty canonical files absorb unrelated changes | per-SWU baseline bundle and admitted-delta check |
| private paths leak into public package | generic fixture corpus and public/private scan |
| generated mirrors become source authority | canonical-first mutation and parity receipt |

## Design gate

- Six required views: complete.
- Scope manifest: authored candidate, exact selected-source digests present.
- Independent denominator: not implemented; evidence ceiling remains
  `authored-complete`.
- Concern ledger: complete as authored remediation input.
- UX companion: required and complete.
- Glossary consistency: pass with candidate-term boundary.
- Design Distill: pass; one coherent selection admission boundary.
- Upstream/canonical mutation: none.
- Next route: Invoke Plan for implementation remediation, then Spellcraft.

