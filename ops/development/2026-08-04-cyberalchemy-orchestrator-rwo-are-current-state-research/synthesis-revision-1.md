# Synthesis Revision 1

Status: `pass`; validation: `pass`; zig-zag loop used: 1.

## Frozen evidence boundary

The evidence lanes and identities are unchanged:

- E1: tracked orchestrator commit
  `b42228fcf4a5a6dadefbbfb53dfaa3c3edb28108`; direct source observed;
  protocol compilation freshly executed; FastAPI-dependent suites remain
  execution-unverified.
- E2: untracked RWO design SHA-256
  `28b6fca81693a5c6bd10dbe2e74df816312d9e1955e076c950eacd49a86a9419`,
  ontology SHA-256
  `1c6d417c4f0cdfc73c7c42f016c05fd6f8fbccd738a35bf7454472d3cee3b920`,
  and view-research SHA-256
  `3b1de2f21406e2a265012bc3ca0dd540817aa0f6a3fa66d04217cd0d6ac4b568`;
  proposal/research only.
- E2-WG: workflow-discovery blob
  `f07c6d0d92d60ffb239a2ef733f43d20850140f4` and autonomous-target blob
  `92584e7dd3b30b512994dcdf31cc9cd62dd7e619`; draft hypotheses only.
- E3: private ARE architecture SHA-256
  `1958758a104c19af9966fd1460097c18fbf919e480da45e5c8dcc0b5f4ffe0de`,
  ACI-binding architecture
  `02eaede41676bcf19e45cb8cf9b7130bddf297d6ae786d81fdb67ee456bb2c8c`,
  bounded-L0 `execute.mjs`
  `72de12f61b8450dc28bce29ce592787c912e99cb2eb781a9481f71998ddc03b5`,
  and `reducer.mjs`
  `e2a50b3db67ec47476a0a5bf14179535bfff3073a9228894439658b4b602fcaf`;
  bounded local L0 witness only.

No seam is precedent-clean merely because an intended owner can be named. All
future ACI/ARE ownership allocations below are conditional targets requiring
cross-repository conformance, named artifact and typed-gate owners,
compatibility evidence, and owner receipts.

## Current capability by proof tier

| Tier | Capability | Strongest permissible claim |
|---|---|---|
| Freshly executed | Protocol compilation at blob `4624f9d`; PC1–PC12 plus frozen golden manifest | 13/13 passed in 0.567s. This bounded compiler does not confirm, bind, dispatch, reason, authorize, or effect. |
| Observed implementation | Dispatch validation/initial bound launch plan, `dispatch_workflow.py` blob `aaeb01e`, selectors `61/94/231` | Current target implementation; no executed end-to-end host lifecycle or recursive graph expansion. |
| Observed implementation | Host-seat binding, exact redelivery, divergent conflict, parent-close block, output constraints; migration `009`, service selectors `5427/5736/5829` | Existing target boundary, not RWO; current tests were not executed because FastAPI was unavailable. |
| Observed implementation | ACI-accepted command/event history in journal blob `94d4d23`, `accept:145`, `verify_store:560` | Lifecycle acceptance/idempotency/verification exist; this is not semantic replay or production proof. |
| Observed implementation | Reference Scout/BUS reveal, APT projections, recovery, and Control Center read boundaries | Tracked implementations exist; provider delivery, agent use, external effects, restore, authoritative mutation, browser acceptance, and production remain unproved. |
| Proposal only | Generic recursive sequence/fan-in/composite/sidecar/cursor/repeat | Not current capabilities. |
| Bounded private witness | L0 semantic evaluation, typed outcomes, challenge closure, semantic exact replay | Promoted local L0 only; no actor-protocol umbrella, integrated ReplayBridge, real effects, whole ARE, or L1–L3. |

The implementation lane’s `validation=block` described execution coverage, not
research failure. Twelve protocol tests and one golden-manifest test passed;
ten broader modules could not import because FastAPI was absent. Those modules
are neither passed nor failed. A dependency-complete end-to-end
confirmation→binding→journal verification remains required.

## Typed vocabulary

| Term | Unique meaning and owner | Forbidden substitution |
|---|---|---|
| `WorkDefinition` | Prospective RWO owner; versioned bytes → reusable topology | confirmed Dispatch, run plan, or runtime record |
| `RunPlan` | Confirmation/Dispatch owner; confirmed definition/bindings → addressed instance plan | a new definition or inherited authority |
| `WorkRun` | Prospective work-lifecycle owner; addressed plan → run identity/work attempts | existing seat identity as semantic equivalence; domain success |
| Root orchestrator | Lifecycle owner; accepted lifecycle records plus typed route-eligibility verdicts → addressed commands | semantic, domain, or effect verdict owner |
| ACI lifecycle command | Target ACI owner; exact requested transition → accept/reject | accepted fact or authorization |
| Accepted lifecycle event | Target ACI owner; admitted command/outcome → immutable lifecycle record | domain truth or semantic observation |
| ACI-accepted command/event history | Journal owner; admitted lifecycle records → durable history | semantic judgment |
| Journal replay cursor | Conditional future ACI integration owner; accepted offsets/versions → journal reconstruction position | orchestration eligibility or refreshed truth |
| Derived orchestration routing cursor | Prospective RWO/orchestrator projection owner; history plus typed route verdicts → eligible addresses | source history or domain status |
| Domain status | Invoked work/domain owner; domain evidence → typed status | route completion, journal presence, process terminality, projection, or quorum |
| Admitted semantic observation | Observation-admission owner; source evidence/posture → admitted/rejected observation | raw lifecycle data |
| Semantic verdict | Evaluator; frozen admitted inputs → typed outcome/residue | route or effect authorization |
| Semantic exact replay | Bounded evaluator; immutable exact inputs → exact receipt bytes | journal reconstruction or current revalidation |
| Current revalidation | Current source/rule/gate owners; prior refs plus current state → new run | overwriting historical receipts |
| Work attempt | Work lifecycle/executor; addressed work command → outcome or honest unknown | effect authorization |
| External-effect attempt | Conditional adapter owner; ACI-accepted exact intent → outcome or honest unknown | semantic recommendation or gate pass |
| Idempotent redelivery | ACI/lifecycle owner; identical identity/bytes → same accepted identity | changed bytes under same identity |
| New attempt | Work/Dispatch lifecycle owner; new identity under allowed policy → separate attempt | redelivery |

Bare decision, gate, retry, replay, execution, event, evidence, and authority are
prohibited in load-bearing claims. Use typed confirmation, entry, semantic,
artifact-admission, exact-effect, route-eligibility, and evidence-closure
verdicts/gates; source evidence, accepted lifecycle record, admitted semantic
observation, and execution witness; and specific source, confirmation,
semantic-rule, lifecycle-acceptance, artifact, effect, and promotion owners.

`CompositeWork` is deferred until expansion, boundary projection, child failure
propagation, cancellation, and topology-confirmation contracts exist. The
actor-protocol umbrella is deferred; only the narrower evidenced `ACI
actor-command/event protocol` may be named.

## Proposal and blocker state

- Candidate proposal only: uniform outer Work contract, root-only orchestration,
  explicit selectors, command/lifecycle-event separation, fail-closed unknowns.
- Deferred: CompositeWork, generic sidecars, generic fan-in, generic routing
  cursor, and recursive bounded repeat.
- Open: RWO-OQ-001–010, ontology residue 011–014, and WGQ-1–10.
- Blocked: artifact-admission owner and receipt (`GAP-ARE-ART-001`),
  cross-repository schemas and typed-gate adapters, recursive compiler and
  reducer fixtures, and dependency-complete target execution.

## Current implementation → Recursive Work verdicts

| Candidate mapping | Verdict | Required discriminator |
|---|---|---|
| Confirmed dispatch row ↔ WorkDefinition | NARROW analogy only | RWO may not replace registration/confirmation; accepted definition schema required. |
| Bound seat/attempt ↔ WorkRun address | SELECT identity precedent only | Address is not authority or semantic status. |
| Leaf host adapter | NARROW translation precedent | Target-owner conformance required; binding is not permission to invoke. |
| Generic recursive sequence | KILL as current capability; DEFER proposal | Accepted definition, expansion, typed routing-readiness reducer, blocked/wrong-artifact paths, replayable cursor. |
| Finite fan-out | SELECT observed implementation shape; execution-unverified | Does not prove RWO or equal authority. |
| Generic fan-in | KILL as current capability; DEFER proposal | Typed reconciliation and missing/wrong-artifact negatives. |
| Generic gate | KILL term/capability | Replace with typed gates and blocked-path fixtures. |
| Generic sidecar | KILL as current capability; DEFER proposal | Lifecycle contract and sidecar-independence negative. |
| CompositeWork | DEFER | Expansion, boundaries, propagation, cancellation, topology confirmation. |
| Bounded repeat | NARROW governed follow-up precedent | Split redelivery/new attempt; preserve exhaustion and topology. |
| Command/lifecycle-event lanes | SELECT target protocol precedent | Lifecycle admission is not domain truth. |
| ACI journal | SELECT current owner; future relation conditional | Any second integrated RWO/ARE writer is KILL. |
| Generic routing cursor | DEFER | Split and fixture journal replay versus orchestration routing. |
| Generic effect adapter | DEFER | Artifact owner, exact-effect owner, ACI acceptance, real adapter, unknown-outcome and compensation evidence. |

## Conditional RWO/orchestrator → ARE mapping

This is a documentation candidate, not selected executable integration.

| Typed edge | Conditional allocation and failure | Status |
|---|---|---|
| ConfirmedDispatch proposes ACI lifecycle command | Target confirmation remains external to RWO; future adapter proposes, target ACI admits/rejects; missing receipt blocks. | Current inputs observed; cross-repo mapping candidate. |
| ACI history → verified journal cut | Future materializer may read the one target writer after conformance; unknown schema/digest/cut blocks. | Journal observed; integration unverified. |
| Verified cut/source evidence → admitted observations | Observation admitter independently admits/rejects; lifecycle events are not automatically observations. | Bounded L0 component; producer integration candidate. |
| Observations/rules → semantic verdict/receipt | Local evaluator owns bounded derivation only. | Promoted local L0; invocation compatibility unverified. |
| Receipt → artifact-admission verdict | External artifact owner unselected; missing/rejected/mismatched receipt blocks all downstream work. | Blocked by `GAP-ARE-ART-001`. |
| Exact receipt/envelope → exact-effect verdict | Distinct effect owner must be named/adapted; recommendation cannot substitute. | Fixed-test-double witness only. |
| Effect pass proposes ACI effect intent | Future ACI adapter separately admits/rejects; gate pass creates no accepted intent. | Candidate. |
| ACI intent → external-effect attempt | Adapter attempts only admitted intent and records outcome/honest unknown through ACI. | Real adapter absent. |
| Immutable semantic inputs → semantic exact replay | Local replay exists; integrated ReplayBridge is unselected. | Local executable; integrated deferred. |
| Current refs/state → revalidation | Fresh current owners/inputs; history immutable. | Bounded local branch; integrated deferred. |

## Topology verdicts

- SELECT only as documentation analysis: bounded evaluator adjacent to typed
  gates.
- KILL as current executable integration; DEFER as candidate: cross-repository
  seam.
- NARROW to documentation candidate: ARE as an ACI-subordinate leaf facade.
- DEFER: ARE as CompositeWork and integrated ReplayBridge.
- NARROW to candidate: read-only non-authorizing semantic audit sidecar.
- KILL as current capability; DEFER proposal: generic sidecar.
- KILL: orchestrator-owned reasoning scheduler, second RWO/ARE journal, or any
  merge of journal, routing cursor, semantic receipt, and domain status.
- DEFER as fallback: no integration, if owner/conformance gates fail.

## Smallest documentation-only contract

The candidate document allocates no present-tense cross-repository authority
and is not promotion input:

1. Pin exact source, proposal, architecture, evaluator, and schema identities;
   declare `authority_effect: none`.
2. Define candidate envelopes for confirmed Dispatch reference, ACI lifecycle
   command, verified journal cut, semantic observations, semantic receipt,
   artifact reference, exact-effect envelope, ACI effect intent, and observed
   outcome.
3. For each envelope, name proposed producer/consumer and every source,
   lifecycle, semantic, typed-gate, artifact, effect, and promotion owner—or
   mark the relation blocked.
4. Require separate receipts for ACI conformance, ARE invocation compatibility,
   artifact admission, entry/exact-effect adapters, and runtime compatibility.
5. Require this typed path:

   `ConfirmedDispatch → proposed ACI lifecycle command → ACI accept/reject →
   verified journal cut → observation admit/reject → semantic verdict/receipt →
   artifact admit/reject → exact-effect pass/block → proposed ACI effect intent
   → ACI accept/reject → external-effect attempt → recorded outcome or honest
   unknown`.

6. Missing owners/receipts, unknown versions/digests, cross-run substitution,
   stale inputs, divergent redelivery, rejected artifacts, or non-pass verdicts
   fail closed.
7. Journal reconstruction, semantic exact replay, and current revalidation stay
   separate.
8. No compatibility, implementation, registration, promotion, effect,
   publication, deployment, or production claim follows.

## Required finite fixtures before implementation selection

- Recursive expansion; routing-readiness pass/block; wrong/missing artifact;
  bounded new attempt/exhaustion; cursor rebuild; fan-in reconciliation;
  sidecar independence.
- Dependency-complete confirmation→binding→journal execution.
- Missing-owner receipt; cross-run substitution; divergent redelivery; stale
  cut; rejected artifact; recommendation without effect pass; effect pass
  without ACI acceptance.
- Owner conformance receipts from target ACI, ARE, typed-gate adapters,
  artifact-admission owner, and runtime owner.

Only then may an implementation Work Pack be selected.

## Reviewer-defect closure

| Defect | Closure |
|---|---|
| Ownership sounded settled | All ACI/ARE allocations are conditional and owner-receipted. |
| RWO risked owning confirmation/host binding | Existing target boundary; RWO may neither own nor replace it. |
| Lifecycle routing was generic | Generic sequence killed as current capability and deferred. |
| Second journal ambiguity | Existing target journal retained; any second writer killed. |
| Artifact admission omitted | Added blocked stage, owner receipt, and negative fixture. |
| Bounded evaluator inflated | Local L0 retained; cross-repo compatibility unverified. |
| Integrated replay overstated | Local semantic exact replay separated from journal reconstruction and deferred ReplayBridge. |
| Generic fan-in/sidecar/composite | Killed as current or deferred pending exact fixtures/contracts. |
| Cross-repository seam selected early | Killed as selected executable integration; documentation candidate only. |
| Accepted history/event ambiguous | Renamed ACI history and accepted lifecycle event. |
| Cursor/replay collapsed | Split both cursor and replay/revalidation families. |
| Bare gate/decision/evidence/authority | Replaced with typed vocabulary. |
| Retry/execution collapsed | Split redelivery/new attempt and work/effect attempt. |
| Actor protocol broad | Narrow ACI command/event protocol only; umbrella deferred. |
| 13/13 collapsed with blocked suites | Freshly executed witness and import-blocked modules remain separate. |

Claim ceiling: revised evidence-bounded documentation synthesis only; no
executable integration selection, implementation, authorization, binding
registration, promotion, publication, deployment, production readiness, or
external effect.
