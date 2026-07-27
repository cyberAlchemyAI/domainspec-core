# Findings: Invoke Design-Phase Coverage

## Goal

Define a bounded, falsifiable Design-phase coverage contract for Invoke without
turning every risk into a mandatory template, inventing absent owners, or
mistaking authored plans for executed evidence.

## TL;DR

The current package has strong authored architecture: six views, typed lifecycle
contracts, role separation, exact-digest joins, fail-closed transition rules,
and a non-authoritative observability boundary. It does **not** have a closed
scope manifest, independent denominator extractor, expanded Design detector or
validator, two-pass fixed-point receipt, or frozen selection fixtures. Those
components do not exist today. Therefore the package can claim only
`authored-complete` coverage; it cannot claim `design-validator-pass`,
validator-backed readiness, or Plan evidence. This diagnosis follows
`research.md` **Agent 2 — van Lamsweerde, Axel**, which distinguishes six-view
shape from concern and evidence sufficiency, and **Agent 4 — Alexander,
Christopher**, whose sample found later blockers behind authored Design
packages; see also the current package’s `DESIGN.md`, `TEMPLATE-SELECTION.md`,
and `GAPS.md`.

The repair is a closed, digest-bound `scope_manifest`, an independently produced
denominator receipt, exact concern ownership, deterministic two-pass selection,
and four dispositions: `required`, `recommended`,
`not-applicable-with-rationale`, and `block`. Existing `architecture`,
`ux-plan`, `research`, and bounded `decision-gate` owners are sufficient for
current routing. Security, privacy, data, reliability, operations,
performance, migration, integration, content, accessibility, and validation
remain triggered extensions or cross-phase obligations, not new universal
families. This is supported by `research.md` **Agent 1 — Tversky, Amos**,
**Agent 2 — van Lamsweerde, Axel**, and **Agent 3 — Ashby, W. Ross**.

## Context

The Inventory packet is useful discovery evidence but explicitly lacks an
independent package denominator and does not decide which concerns merit new
families. Its consequence was to test four lenses and prefer strengthening
owned companions before proposing another family
(`strategy-inventory-packet.md`, “Gaps left for research” and “Strategy
consequence”). The empirical sample is bounded and purposive, not a prevalence
estimate (`research.md`, **Agent 4 — Alexander, Christopher**). Accordingly,
these findings define a candidate contract and a private package delta; they do
not approve canonical mutation or promotion.

## Current coverage diagnosis

The mandatory six-view profile is a useful navigation baseline but is not a
sufficiency proof. The present Design gate can establish headings,
dependency/interface rules, and a decision-log shape while missing stakeholder
concerns, enforcement mechanisms, measurable scenarios, and falsifiable
bindings (`research.md`, **Agent 2 — van Lamsweerde, Axel**; [ISO/IEC/IEEE
42010](https://www.iso.org/standard/74393.html); [SEI
ATAM](https://www.sei.cmu.edu/library/the-architecture-tradeoff-analysis-method-2/)).

The current lifecycle package is stronger than the generic floor:

- `TEMPLATE-SELECTION.md` correctly selects the architecture companion for a
  cross-owner change.
- `DESIGN.md` authors typed epoch, readiness, transition, and change-impact
  contracts; pairwise producer/validator/consumer separation; exact control
  digests; fail-closed transition rejection; and observational-only progress.
- `GAPS.md` honestly records that the local contract schema, control-graph
  completeness validator, change-impact classifier, legacy admission path, and
  live proof do not exist.

These are authored contracts, not witnessed behavior. The sample shows why:
operator projection, formal evidence, lifecycle authority, integration
recovery, and narrow fixture packages can all satisfy document structure while
having different unresolved risks (`research.md`, **Agent 4 — Alexander,
Christopher**). The package’s current truthful status is therefore
`authored-complete`; expanded Design validation is a gap.

## Closed scope and denominator proposal

Classification must begin from a closed `scope_manifest` bound to exact source
and target digests:

```yaml
scope_manifest:
  schema_version: 1
  manifest_id: string
  target_id: string
  target_footprint:
    roots: [{path, digest}]
    inclusions: [{selector, digest}]
    exclusions: [{selector, reason, evidence_ref}]
  source_contracts: [{path, digest, selector}]
  human_actors: [{actor_id, reads, decides, acts, surfaces}]
  rendered_surfaces: [{surface_id, modality, semantic_contract_ref}]
  interfaces: [{interface_id, kind, peer, direction, contract_ref}]
  stores: [{store_id, authority, data_classes, writers}]
  queues: [{queue_id, producers, consumers, ordering}]
  writers: [{writer_id, targets, concurrency}]
  normative_rules: [{rule_id, verb, subject, object, enforcement_hint}]
  effects: [{effect_id, reversible, external, privileged}]
  data_and_log_sinks: [{sink_id, data_classes, retention_hint}]
  deployment_targets: [{target_id, environment, release_mode}]
  compatibility_boundaries: [{boundary_id, old_new_contracts}]
  quality_claims: [{claim_id, source_kind, threshold_or_tradeoff}]
  acceptance_and_readiness_claims: [{claim_id, selector}]
  unknowns: []
  input_digest: sha256
  authored_by: owner_id
```

Closure means all field classes were inspected, exclusions have evidence,
selectors are normalized, and `unknowns` is empty. Missing or unknown inputs
produce `block`, never N/A. This answers the omitted-denominator and false-N/A
counterexamples raised against authored inventories.

A deterministic extractor independent of the manifest author should then emit:

```yaml
design_denominator_receipt:
  schema_version: 1
  manifest_id: string
  manifest_input_digest: sha256
  detector_id: string
  detector_version: string
  detector_owner: owner_id
  inspected_selectors: [selector]
  extracted_signals:
    - {signal_id, signal_class, source_selector, source_digest}
  authored_concern_ids: [string]
  denominator_signal_ids: [string]
  unbound_signal_ids: []
  missing_detector_inputs: []
  verdict: pass | block
  receipt_digest: sha256
  validator_owner: owner_id
```

The denominator is the union of authored concerns and extracted actors,
surfaces, rules, interfaces, dependencies, stores, queues, writers, sinks,
deployment/compatibility signals, effects, and qualifying claims. Every signal
must bind to one primary concern and disposition. The receipt must reject stale
inputs and self-issuance. This directly repairs the non-vacuity defect exposed
by omitted queues, stores, APIs, log sinks, writers, and human surfaces.

The independent-denominator requirement is a converged repair from the
reviewer attacks, grounded in `research.md` **Agent 2 — van Lamsweerde, Axel**
(concern trace and evidence binding) and **Agent 4 — Alexander, Christopher**
(later blockers hidden by authored structure). It is a candidate: no such
extractor or receipt exists.

## Risk taxonomy and exact ownership

Each detected signal receives one primary class. Cross-references are allowed,
but accountability is singular.

| Primary class | Boundary | Current owner |
| --- | --- | --- |
| Authority | who may decide, attest, admit, or mutate | package-local authority owner; architecture places enforcement |
| Security | adversarial violation of trust/resource boundary | package-local security/risk owner; architecture owns trust flow and control placement |
| State/event | legal states, edges, replay, terminality, supersession | architecture workflow/decision extension |
| Persistence | durable-write authority, ordering, idempotency, writers | architecture persistence extension |
| Failure | timeout, partial effect, retry, compensation, rollback | architecture workflow extension |
| Reliability | service-level availability, recovery objective, dependency tolerance | service owner plus architecture; Plan proves |
| Integration | independently evolving API/schema/protocol | architecture dependency/interface view; Plan proves compatibility |
| Migration | old/new representation or persisted-state conversion | exact package-local migration owner; architecture plus Plan |
| Rollout | staged exposure, release rollback, deployment transition | service/release owner; architecture plus Plan/work-pack |
| Privacy/data | purpose, minimization, access, retention, disclosure, deletion | exact package-local data/privacy owner; architecture data-flow extension |
| Performance | measurable resource, capacity, latency, throughput, amplification risk | architecture quality scenario; accountable service owner |
| UX | changed human semantic workflow, decision, recovery, navigation, assistive operation | existing `ux-plan` owner |
| Validation | normative, acceptance, readiness, or externally observable assertion | Design binds; Plan/work-pack executes |

This precedence separates admission authority from adversarial bypass,
durable duplicate effects from per-effect compensation and service recovery,
representation conversion from staged exposure, and human semantics from
machine evidence (`research.md`, **Agent 2 — van Lamsweerde, Axel** and
**Agent 3 — Ashby, W. Ross**).

Every binding must name:

```yaml
ownership:
  accountable_owner: exact-role-or-owner-id
  contributing_owners: [exact-role-or-owner-id]
  artifact_owner: exact-role-or-owner-id
  validator_owner: exact-role-or-owner-id
```

Architecture owns structural placement, interfaces, assumptions, and
enforcement contracts. A specialized package-local owner owns policy or
residual-risk acceptance. Plan/work-pack owns implementation and runnable
evidence. The Design validator owns only manifest, selection, ownership,
binding, and fixture-contract checks. An unresolved accountable owner is
`block`; `decision-gate` is reserved for a consequential multi-option blocker.
No reusable security, privacy, migration, or operability owner is presumed
(`research.md`, **Agent 3 — Ashby, W. Ross**).

## Deterministic two-pass selection

1. Verify eligible Design mode and source contracts.
2. Build and close the digest-bound manifest.
3. Extract the independent denominator immediately.
4. Block on missing inputs, unknowns, or unbound signals.
5. Create concern instances and apply normalized predicates.
6. Assign primary class, exact owners, and default output.
7. Route only consequential unresolved multi-option conflicts to
   `decision-gate`.
8. Re-run extraction and affected predicates against the same or superseding
   digest.
9. Pass only if the manifest, denominator, dispositions, ownership, and outputs
   are unchanged.

Pass 1 is detect/classify/own/select. Pass 2 verifies a fixed point. A new
signal, changed scope, changed disposition, changed owner, or unresolved
conflict after pass 2 is `block`; selection does not loop indefinitely.

The four states are exact:

- `required`: the required predicate is true.
- `recommended`: the required predicate is false, but a bounded deferral
  hypothesis names owner, evidence, and revisit condition.
- `not-applicable-with-rationale`: the predicate is false, the detector is
  negative, and cited manifest selectors establish the boundary.
- `block`: scope/input is missing or unknown, a signal is unbound, ownership is
  unresolved, or fixed point is absent.

A companion is selected only when a mapped concern is `required`;
recommendations remain advisory. This formalizes the risk-triggered outcome
proposed by `research.md` **Agents 1, 3, and 4** while preventing the false N/A
and one-pass circularity exposed in review.

## Architecture and bounded UX contracts

The six-view baseline should remain mandatory navigation and gain:

- system-of-interest and closed-scope reference;
- stakeholder-to-concern-to-view trace;
- component responsibilities, interfaces, authority assumptions, and
  enforcement placement;
- one significant behavior scenario—runtime only when runtime/external effect,
  durable state, or operational claim exists; otherwise a deterministic
  artifact/evidence scenario;
- decisions with status, concern IDs, alternatives, criteria, positive and
  negative consequences, trade-offs, evidence, and revisit trigger;
- four-state dispositions, exact owners, and planned fixture/validator
  contracts.

Risk-triggered architecture extensions cover runtime enforcement,
authority/trust, state/event, persistence/concurrency, failure/compensation,
integration/versioning, migration/rollout, deployment/operability, data
lifecycle/privacy, security/abuse, and measurable
quality/reliability/performance. This follows concern-oriented architecture and
quality scenarios rather than universal headings (`research.md`, **Agent 2 —
van Lamsweerde, Axel**; [ISO 42010 conceptual
model](https://www.iso-architecture.org/ieee-1471/cm/); [SEI quality-attribute
scenarios](https://www.sei.cmu.edu/library/reasoning-about-software-quality-attributes/);
[arc42 runtime view](https://docs.arc42.org/section-6/)).

Select `ux-plan` only when both a natural-person `human_actor` and a
new-or-changed human-facing semantic contract exist. When selected it covers
goals/constraints; success and failure/recovery journeys; confirmation,
correction, and reversibility; visible state/evidence meaning; content and
claim bounds; changed focus, reflow, contrast, names, and assistive operation;
responsive semantic behavior; and acceptance owners. APIs, generated evidence,
files, and receipts do not trigger UX unless their change reaches a human
semantic surface. Styling is not exempt when it changes meaning or accessible
operation (`research.md`, **Agent 1 — Tversky, Amos**; [WCAG
2.2](https://www.w3.org/TR/WCAG22/); [W3C mobile
accessibility](https://www.w3.org/WAI/standards-guidelines/mobile/)).

## Blind-spot dispositions

Pending a closed manifest and denominator for this package:

| Concern | Disposition now | Required closure |
| --- | --- | --- |
| Architecture | `required` | retain selected companion |
| Authority | `required` | resolve `ILP-G01`; forged/self-issued rejection |
| Security/abuse | `required` | privileged mutation, delegation, replay, and bypass contracts |
| State/event | `required` | exhaustive forbidden-edge and terminal/replay rules |
| Persistence/concurrency | `required` | classify durable transitions/receipts, writers, ordering, retries |
| Failure/compensation | `required` | partial admission/mutation/closeout and recovery contracts |
| Integration/versioning | `required` | mode/capability interfaces and compatibility rules |
| Migration | `required` | legacy admission, conversion, rollback, no inference |
| Validation | `required` | bind every normative/readiness claim |
| Privacy/data | `block` | inspect receipts, roles, paths, telemetry, sinks, retention |
| Reliability | `block` | establish whether service/recovery commitments exist |
| Rollout/operations | `block` | establish deployment, exposure, support, operator recovery |
| Performance | `block` | establish measurable acceptance/resource claims |
| UX/content/accessibility | `block` | establish whether progress, approval, receipts, or recovery are human-rendered |

Negative extraction may turn a blocked blind spot into
`not-applicable-with-rationale`; prose assertion may not. The trigger boundaries
and earliest Design detection follow `research.md` **Agent 3 — Ashby, W.
Ross**. The UX boundary follows **Agent 1 — Tversky, Amos**. The need to avoid
both false negatives and universal false positives follows **Agent 4 —
Alexander, Christopher**.

## Design versus Plan evidence states

Design authors planned-witness contracts:

```yaml
fixture_spec:
  fixture_id: string
  claim_id: string
  polarity: positive | negative
  target: string
  input_or_violation: string
  expected_result: string
  execution_owner: owner_id
  execution_phase: plan | implementation | validation
```

```yaml
validator_contract:
  validator_contract_id: string
  claim_id: string
  target_contract: string
  accepted_input_digest: sha256-or-binding-rule
  expected_verdicts: [pass, fail]
  stale_receipt_rule: reject
  self_issue_rule: reject
  validator_owner: owner_id
  receipt_class: string
```

These declarations are not executed witnesses. The evidence states are:

| State | Meaning | Authority |
| --- | --- | --- |
| `authored-complete` | required Design fields and planned contracts exist | may enter Design validation only |
| `design-validator-pass` | manifest, denominator, predicates, selection, ownership, binding, and fixed point pass | may hand off to Plan |
| `plan-evidence-pending` | runnable evidence has not completed | no behavior/readiness claim |
| `plan-evidence-pass` | version-bound runnable fixtures passed | supports only governed downstream claims |
| `plan-evidence-fail` | runnable evidence failed | blocks the affected claim |

Plan/work-pack must materialize validators and fixtures, prove red-before and
green-after where behavior changes, and bind receipts to exact versions. A
Design result can never imply `plan-evidence-pass`. This separation is required
by `research.md` **Agent 2 — van Lamsweerde, Axel** (falsifiable evidence
bindings) and **Agent 3 — Ashby, W. Ross** (Design decisions are not readiness
evidence), and resolves the reviewer’s circular-readiness objection.

## Current-package delta

Retain unchanged in meaning:

- the architecture companion selection;
- six authored views;
- epoch/readiness/transition/change-impact candidate contracts;
- pairwise role separation and exact-digest joins;
- fail-closed transition rules;
- observational-only telemetry and Inventory;
- `ILP-G01` as unresolved rather than assigning authority by inference.

Add only to the private package, after approval:

- the closed manifest over Plan, Refresh, Task Session, validators, receipts,
  projections, observability, modes, writers, legacy interfaces, sinks,
  deployment, and human surfaces—including explicit empty findings;
- independent denominator and second-pass fixed-point receipts;
- concern ledger with precedence and exact owner fields;
- expanded decisions with status, consequences, evidence, and revisit triggers;
- `fixture_spec` and `validator_contract` records;
- explicit evidence-state fields.

The detector and validator do not exist. The package must continue to expose
`ILP-G02` through `ILP-G06` and may claim only authored coverage now
(`GAPS.md`; `research.md`, **Agent 4 — Alexander, Christopher**).

## Alternatives killed

- A universal operating-surface/evidence-risk family: duplicates selection and
  existing owners.
- Universal security, privacy, SRE, support, performance, migration, content,
  accessibility, or validation templates: risk-insensitive and unsupported by
  current owner precedent.
- Standalone state-machine, concurrency, or evidence families: existing
  architecture and cross-phase contracts own the work.
- Mandatory runtime scenarios for static/deterministic artifacts.
- UX selected by words such as “UI,” “evidence,” or “claim” rather than a
  changed human semantic contract.
- N/A established by nonempty prose.
- Three states without `block`; one-pass selection; generic “architecture plus
  owner”; routine use of `decision-gate`.
- Design fixture names treated as executed evidence.
- Privacy or operability companions described as already owned.

These eliminations preserve requisite variety without universal checklist cost
(`research.md`, **Agent 3 — Ashby, W. Ross**) and match the narrow-fixture
counterexample (`research.md`, **Agent 4 — Alexander, Christopher**).

## Reviewer-objection resolution

| Objection | Resolution |
| --- | --- |
| Validator-backed readiness is overclaimed | Detector/validator/fixtures are future work; current claim is authored coverage only |
| Plan execution was required before Plan | Split `authored-complete`, `design-validator-pass`, and `plan-evidence-*` |
| Authored concern list permits vacuous pass | Independent digest-bound denominator unions authored and extracted signals |
| False N/A | Require negative detector result, selectors, and checkable boundary |
| Unknowns hidden by three states | Add `block` |
| Selection can discover new scope endlessly | Two passes, fixed point, then block |
| Runtime scenario excludes static work | Require significant behavior scenario; runtime only when triggered |
| Owners are vague or invented | Singular accountable owner plus artifact/validator/contributors; unresolved is block |
| Taxonomy overlaps | Primary concern precedence with overlays |
| UX is too broad or too narrow | Natural-person actor plus changed human semantic contract |
| Planned fixtures masquerade as proof | Design owns specs/contracts; Plan owns runnable evidence and receipts |
| Baseline makes architecture companion tautological | Keep mandatory six-view baseline distinct from predicate-selected companion |
| New privacy/operability families lack precedent | Keep as future candidates requiring separate governance |

## Validator and frozen-fixture requirements

Future implementation must provide schema validation, deterministic predicates,
digest verification, independent extraction, signal-to-concern totality,
fixed-point comparison, N/A boundary checks, stale/self-issued receipt
rejection, exact expected selections, and per-trigger mutation tests.

Frozen positive/control fixtures must include: pure local function; static
deterministic artifact; semantics-preserving style token; backend protocol with
no human effect; ordinary authenticated CRUD that does not select every
extension; operator governed-state workflow; lifecycle/admission system; and
stored-version conversion.

Frozen negative fixtures must include: omitted queue, store, external API, log
sink, second writer, operator-visible evidence, and changed
focus/reflow/accessible name; false “no durable data”; stale denominator;
fabricated or self-issued validator receipt; N/A without negative extraction;
unbound signal; changed pass-2 result; missing exact owner; and planned fixture
mislabeled as executed.

The package-specific planned negatives additionally include forged/stale owner
or readiness receipts; illegal/skipped/backward/terminal/replayed edges;
same-epoch control change; projection-writer self-classification; omitted
controlling paths; inferred legacy admission; retry duplicates; two-writer
conflict; partial mutation/closeout; and fabricated
`design-validator-pass`. Acceptance requires red-before/green-after, exact
expected disposition per fixture, mutation tests for every predicate, and no
path from Design validation to implied Plan evidence. These requirements
instantiate the falsifiability demanded by `research.md` **Agent 2 — van
Lamsweerde, Axel** and the concrete failure classes catalogued by **Agents 1,
3, and 4**.

## Verdict matrix

| candidate | owner (precedent) | witnessed? (non-vacuity) | sound? (definitional) | verdict |
| --- | --- | --- | --- | --- |
| Six views as navigation baseline | DomainSpec Design profile | yes, authored samples only | yes, if explicitly non-sufficient | retain |
| Closed scope manifest | Design contract; future validator | no; omission fixtures unimplemented | yes | adopt candidate |
| Independent denominator receipt | future Design detector/validator | no; detector does not exist | yes | adopt candidate |
| Minimal architecture core | baseline plus selected `architecture` | partially authored; expanded fixtures absent | yes | adopt candidate |
| Concern trace and precedence | architecture | not yet independently witnessed | yes | adopt candidate |
| Runtime enforcement | architecture | planned package cases only | yes | triggered extension |
| Authority/trust | architecture plus exact package-local owner | package risk authored; negative fixtures not run | yes | triggered extension |
| State/event | architecture workflow/decision | contracts authored; exhaustive fixture proof absent | yes | triggered extension |
| Persistence/concurrency | architecture | not denominator-closed or fixture-proved | yes when triggered | triggered extension |
| Failure/compensation | architecture workflow | failure paths authored; injection proof absent | yes when triggered | triggered extension |
| Security/abuse | architecture plus package-local risk owner | adversarial proof absent | yes without invented family | triggered extension |
| Privacy/data | architecture plus package-local owner | denominator absent | yes as extension | future companion candidate only |
| Reliability/operations | architecture plus Plan/work-pack | deployment/service boundary unknown | yes as extension | operability companion future only |
| Performance | architecture quality scenario | measurable claim boundary unknown | yes when triggered | triggered extension |
| Migration/integration | architecture plus Plan | legacy risk authored; rollback proof absent | yes | triggered extension |
| Human-consequence UX | existing `ux-plan` | sampled precedents; current package surface unknown | yes with actor/semantic predicates | adopt candidate |
| Content/accessibility families | existing `ux-plan` | UX precedent exists | no, duplicates owner | reject new families |
| Design fixture/validator contracts | Design contract | not executed; schemas absent | yes as planned witnesses | adopt candidate |
| Runnable evidence | Plan/work-pack | not yet run | yes | downstream only |
| Universal risk family | no distinct owner | no independent benefit witness | no | reject |

## Public/private boundary

Any later public `arcanum/` change may contain only generic selection schemas,
generic architecture/UX contract improvements, generic detector contracts, and
sanitized fixtures. This private lifecycle package may contain its manifest,
ILP dispositions, private paths, owners, selectors, and evidence. Public
artifacts must not contain private checkout paths, package identifiers, ILP IDs,
private owner identities, or private evidence. Privacy or operability companion
families require a separate governed proposal, authority, fixtures, and
promotion record. The boundary follows the dispatch context and
`research.md` **Agent 3 — Ashby, W. Ross**; these findings authorize neither
public mutation nor promotion.

## Connections

- **Authored state versus authority:** the coverage repair is the Design analogue
  of this package’s lifecycle rule that projections, telemetry, Inventory, and
  self-authored receipts cannot advance authoritative state. Both require an
  independent, digest-bound admission boundary (`research.md`, **Agent 2 — van
  Lamsweerde, Axel** and **Agent 4 — Alexander, Christopher**).
- **Earliest machine-checkable boundary:** detecting actor semantics, trust
  boundaries, stores, writers, failure paths, and compatibility before Plan
  prevents one omission from multiplying into downstream SWUs
  (`research.md`, **Agent 4 — Alexander, Christopher**;
  `strategy-inventory-packet.md`, `most-used-skills-efficiency-review` lead).
- **Requisite variety without checklist inflation:** risk-triggered extensions
  represent only environmental variety capable of invalidating the declared
  boundary, while narrow deterministic artifacts retain a light path
  (`research.md`, **Agent 3 — Ashby, W. Ross** and **Agent 4 — Alexander,
  Christopher**).
- **Human truth is a projection contract:** UX becomes relevant when a natural
  person acts on or trusts rendered state, evidence, approval, recovery, or
  navigation—not when a backend artifact merely contains a claim
  (`research.md`, **Agent 1 — Tversky, Amos** and **Agent 4 — Alexander,
  Christopher**).

## Open Questions and named owners

1. **Who admits `epoch_transition` and owns its public source placement?**
   Owner: **Arcanum governance + Spellcraft** via `ILP-G01`. This remains
   acceptance-critical and blocks canonical mutation handoff.
2. **Who will own and implement the generic Design detector, denominator
   extractor, validator, receipt schemas, and frozen fixtures?** Owner:
   **Invoke/Spellcraft**, with an independent validator owner to be named before
   implementation. Until named and implemented, only authored coverage is
   claimable.
3. **Does the closed package manifest contain a human-rendered semantic
   surface?** Owner: **Invoke Design artifact owner**, independently checked by
   the future detector; if yes, route to the existing **`ux-plan` owner**.
4. **Do receipts, telemetry, paths, or logs trigger privacy/data lifecycle
   obligations?** Owner: an exact **package-local data/privacy accountable
   owner** must be named after extraction; architecture owns flow/control
   placement and Plan owns runnable checks.
5. **Are service-level recovery, deployment, staged exposure, support,
   performance, or multi-writer commitments actually in scope?** Owner:
   **architecture artifact owner** for classification, then exact
   **service/release owners** for any triggered acceptance.
6. **When may privacy or operability become reusable companion families?**
   Owner: **Invoke/Spellcraft governance** through a separate proposal proving
   distinct authority, contract, fixtures, and promotion evidence; this
   research does not create either family.
