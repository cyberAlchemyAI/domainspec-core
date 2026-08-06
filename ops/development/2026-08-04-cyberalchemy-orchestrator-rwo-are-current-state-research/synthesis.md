# Preserved Synthesizer Return

action_id=spawn-0004; role=state-synthesizer; status=pass; validation=pass; artifacts=inline-synthesis-return; blockers=none

## Evidence boundary and reconciliation rule

This synthesis preserves four non-interchangeable evidence lanes:

| Ref | Lane and immutable identity | Explorer return | Evidence scope/status |
|---|---|---|---|
| E1 | Tracked orchestrator implementation at commit `b42228fcf4a5a6dadefbbfb53dfaa3c3edb28108`; implementation docs blobs `03b39f04…5c0`, `e3da5c20…c7c` | `research.md#agent-1--turing-alan--implementation-explorer`; receipt `spawn-0001`; normalization `implementation-explorer-normalization.json` | Direct source observed. Only protocol compilation freshly executed. FastAPI-dependent suites remain execution-unverified. |
| E2 | Untracked RWO `DESIGN.md`, SHA-256 `28b6fca8…9419`; ontology SHA-256 `1c6d417c…920`; research view SHA-256 `3b1de2f2…b568` | `research.md#agent-2--simon-herbert--proposal-explorer`; receipt `spawn-0002` | Observed proposal/research semantics only; no implementation, canonical, runtime, or promotion effect. |
| E2-WG | Tracked workflow discovery blob `f07c6d0d…f4`; autonomous target blob `92584e7d…19`, both at `b42228f…28108` | E2, “Hypotheses and tensions,” “Explicit decisions vs preserved non-decisions” | Observed draft discovery/target hypotheses, not accepted schemas or implementation. |
| E3 | Private ARE architecture SHA-256 `1958758a…f0de`; ACI binding architecture `02eaede4…c8c`; bounded L0 `execute.mjs` `72de12f6…3b5`, `reducer.mjs` `e2a50b3d…fcaf` | `research.md#agent-3--hewitt-carl--integration-explorer`; receipt `spawn-0003` | Architecture observed. Bounded L0 has promoted local witness; whole engine and cross-repository integration remain unverified/candidate. |

No disagreement is averaged. E1 establishes what currently exists in tracked target bytes; E2 establishes proposal and hypothesis content; E3 establishes a bounded semantic witness and candidate owner-preserving integration contract.

## 1. Current capability map by proof tier

| Proof tier | Current capability and strongest claim | Immutable selector | Ref; scope/status | Explicit non-claim |
|---|---|---|---|---|
| Freshly executed | Deterministic closed-schema protocol compilation, frozen golden manifest, DAG rejection, restart independence, unsupported-requirement handling, and candidate/non-authority separation | commit `b42228f`; `protocol_compilation.py` blob `4624f9d`, `compile_candidate:368`, `compile_dispatch_candidate:489`; tests blob `280e8a7`, PC1–PC12; golden-manifest test | E1; **executed: 13/13 passed in 0.567s** | Does not authorize dispatch, invoke a host/provider, execute effects, or constitute semantic reasoning. |
| Observed implementation; execution blocked | Per-seat/per-turn host workflow binding, exact retry identity, divergent retry rejection, continuity, terminal completion, output-byte constraints | commit `b42228f`; migration `009` blob `1f6e4c2`; `service.py` blob `5ba442e`, methods at `5427/5736/5829`; tests blob `9ad8c5a`, lines `262–383` | E1; source/tests observed, FastAPI import blocked | No real host adoption, authenticated authorship, universal interception, or authority for this research dispatch. |
| Observed implementation; execution blocked | Dispatch validation and bound launch-plan compilation | `dispatch_workflow.py` blob `aaeb01e`, `validate_opening_record:61`, `compile_bound_launch_plan:94`, `run:231`; test blob `aaf17a3`, lines `69–168` | E1; observed, execution-unverified | No end-to-end native host launch or external effect. |
| Observed implementation | Hash-chained transactional SQLite journal with command acceptance, idempotency/conflict handling, events, heads, receipts, and verification | `journal.py` blob `94d4d23`, `accept:145`, `verify_store:560`; migrations `001–011` | E1; observed, dependent execution blocked | Not proof every action enters the journal, of semantic replay, global recovery, or production operation. |
| Observed implementation; execution blocked | Exact Reference Scout and BUS/reveal input materialization with transactional persistence and pending-effect modeling | `reference_delivery.py` blob `594d269`, lines `15/45/72/113/200`; migration `010` blob `de4a8dd`; `reveal_delivery.py` blob `1e8c9cd`, lines `36/52/106/140`; migration `011` blob `9a2b166` | E1; observed, execution-unverified | No provider delivery, agent use, independent judgment, or completed external effect; same-seat false quorum remains a counterexample. |
| Observed implementation; execution blocked | Rebuildable APT projections and ACI-owned bounded research acceptance | `projections.py` blob `c6a59d6`, `ProjectionManager:33`; `service.py:4224,5856–6092`; migrations `004–008` | E1; observed, execution-unverified | Projection, ingestion, or lineage is not authority, prompt use, or semantic reasoning. |
| Observed implementation; execution blocked | Verification, non-overwriting backup, and recoverable retirement | `operator_recovery.py` blob `b37f831`, lines `51/141/180`; tests blob `7ca033e`, lines `41–144` | E1; observed, execution-unverified | No restore/reinstate command, full harness checkpoint, or production recovery drill. |
| Observed fail-closed UI boundary | Six read-oriented Control Center routes with interface-identity gating; preview store rejects authoritative effects | `control_center/api.py` blob `aa6907b`, lines `75–226`; `main.py` blob `ea72c32`, lines `91–109`; tests blobs `a162b6a`, `aad1a95` | E1; observed, execution-unverified | No approve/apply/retry/reconcile/promotion; local store is not wired as authoritative state. |
| Observed closed serving boundary | Production runtime/provenance/health readers disabled; loopback pilot separately gated | `main.py` blob `ea72c32`, lines `68–76`; `service.py:6289` | E1; observed | No deployment, production serving/readiness, non-loopback service, browser proof, or external effect. |
| Proposal only | Recursive `WorkDefinition`/`WorkRun`, leaf/composite closure, event edges, root expansion, generic cursor, sidecars, bounded repeat | RWO hashes above; `DESIGN.md:19–32,54–68,87–220,287–330`; ontology `rwo:f.no-nested-orchestrator-invocation` | E2; observed proposal, unverified runtime | No tracked RWO implementation exists. |
| Bounded private implementation | Deterministic L0 semantic evaluator, typed outcomes, challenge closure, exact replay; exact-effect integration only through fixed test double | ARE hashes above; `reducer.mjs:159–320+`; `execute.mjs:102–221`; `replay.mjs:5–22` | E3; promoted bounded local witness; whole-engine integration unverified | Not whole-engine promotion, real effects, external ACI integration, or L1–L3 completion. |

### Executed-witness reconciliation

The implementation explorer’s original `validation=block` describes execution coverage, not research failure. Exactly thirteen protocol-compilation checks passed. Ten broader modules—including host binding, dispatch workflow, delivery, APT, recovery, and Control Center coverage—failed during import because FastAPI was unavailable. These are neither passed nor implementation failures.

The parent normalization therefore correctly records research `status=pass; validation=pass`, because the audit delivered the required exact-binding classification while retaining the dependency-limited suites as execution-unverified residue. No dependency installation was authorized.

## 2. Proposals, hypotheses, decisions, non-decisions, blockers, and questions

| Classification | Item | Immutable selector | Ref; status | Consequence |
|---|---|---|---|---|
| Candidate proposal decisions | Uniform outer Work contract; composite closure; one root runtime; explicit event selector/input mapping; bounded cycles; command/event separation; derived projections; no inherited authority; fail-closed unknowns | RWO `DESIGN.md:19–32,87–330`; ontology hash `1c6d…920` | E2; observed proposal only | Coherent candidate kernel, not target behavior. |
| Hypothesis | RWO `WorkNode` can be structural without being an agent | RWO `DESIGN.md:87–146`; WGQ-2/3; target blob `92584e…19`, lines `369–389` | E2/E2-WG; unresolved | Choose a layer boundary; do not encode operations, joins, or gates as agents merely for uniformity. |
| Hypothesis | One root kernel can execute a confirmed Dispatch while confirmation, semantic status, and effects remain externally owned | RWO `DESIGN.md:54–68,287–330`; target SP-1–SP-5 | E2; plausible/unverified | Requires total authority mapping and negative tests. |
| Hypothesis | Event-triggered bounded rework can coexist with finite protocol DAG compilation | RWO `DESIGN.md:148–220`; WGQ-8; compiler blob `4624f9d` | E1/E2; unresolved | Define generation/repetition/state-transition semantics before adoption. |
| Hypothesis | Journal plus reducer can reconstruct routing without becoming authoritative domain state | RWO `DESIGN.md:287–330`; RWO-OQ-001/006; WGQ-1/7/8 | E2; unresolved | Requires journal/state ownership and migration decisions. |
| Non-decision | Universal graph, node taxonomy, communication placement, completion model, rework model, compilation/confirmation mapping | Workflow discovery WGQ-1–10, blob `f07c6d…f4` | E2-WG; observed draft residue | Discovery must not be treated as a selected architecture. |
| Non-decision | Journal authority, dynamic topology, delivery, cancellation/compensation, quorum, migration, minimum authority reference, stream closure, promotion owner | RWO-OQ-001–010 and ontology residue 011–014 | E2; observed open proposal residue | Blocks implementation-ready status for a generic RWO. |
| Non-decision | Detailed schemas, storage/provider/sandbox/credential implementation, migration and compatibility | autonomous target blob `92584e…19` | E2-WG; target hypothesis | Target prose cannot retroactively promote RWO. |
| Integration blocker | No accepted cross-repository command, journal-cut, semantic-artifact, or effect-intent schemas | E3 “Open owner decisions” | E3; unverified | Blocks executable integration. |
| Integration blocker | No recursive-work compiler/fixture, real-effect witness, integrated replay bridge, or whole-engine witness | E3 matrices/topology | E3; absent/unverified | Blocks composite and production claims. |
| Validation blocker | FastAPI missing for broader selected suites | E1 “Validation executed”; normalization receipt | E1; execution-unverified residue | Re-run in an authorized environment; do not reinterpret as test failure. |

## 3. Delta from prior Inventory classification

Prior Inventory remains directionally correct: the target is a governed orchestration/control-plane and evidence runtime, not a semantic reasoning engine. It is now materially incomplete.

At `b42228f`, tracked bytes add or concretize eleven migrations, transactional journaling, host-seat binding, launch-plan compilation, deterministic protocol compilation, Reference Scout and BUS/reveal delivery seams, APT acceptance/projections, operator preservation, and six fail-closed Control Center read routes. E1 directly observes these selectors, and protocol compilation alone was freshly executed.

Unchanged ceilings: host adoption is unproved; semantic judgment remains absent from the orchestrator; provider/effect paths remain unwitnessed; production readers remain closed; the RWO subtree is untracked proposal material; and no executable target-to-private-ARE binding exists. Inventory has no target-local machine index and remains discovery evidence only.

## 4. Current implementation → recursive-work mapping

All rows inherit orchestrator commit `b42228f`, RWO design hash `28b6…9419`, E1 observed implementation scope, and E2/E3 proposal-mapping scope.

| RWO concept | Current exact analogue | Verdict; status | Boundary |
|---|---|---|---|
| `WorkDefinition` | Validated confirmed dispatch row; `dispatch_workflow.py:24–28,61–113` | **NARROW**; observed partial analogue | Dispatch row is not a promoted recursive definition. |
| `WorkRun`/stable address | `dispatch_id/group_id/seat_index/turn_ordinal/attempt_id`; `host_dispatch_hook.py:42–54`; host-binding test `262–300` | **SELECT** reusable identity surface; implementation observed, test unexecuted here | Address grants no authority. |
| Leaf executor | Bound launch → native host operation; hook `332–343,439–512`; compiler `137–181` | **NARROW**; observed | ACI validates binding; invoked work retains semantics. |
| Composite expansion | Current initial seat launch compilation | **DEFER**; gap | No recursive flattening, boundary projection, or arbitrary event-edge interpretation. |
| Sequence | Declared group dependency plus typed handoff | **NARROW**; governed precedent | Artifact existence is not readiness. |
| Fan-out | One parent dispatch to multiple bound seats; test `262–283` | **SELECT** finite shape; observed test bytes, not freshly executed | Parallel arrival is not equal authority or consensus. |
| Fan-in/join | Declared stage join consumed by synthesizer/verifier | **NARROW** partial | Arrival/quorum cannot replace semantic reconciliation. |
| Gate/route label | Capability-owner verdict followed by orchestrator traversal | **SELECT** precedent | Router transports a verdict; it does not create it. |
| Sidecar | APT/telemetry/read projections; `service.py:655–714` | **NARROW** observation; **DEFER** generic lifecycle | Projection cannot own source state. |
| Bounded repeat | Declared follow-up/zig-zag with loop cap; hook `:512` | **NARROW** | Retry cannot alter topology, scope, or authority silently. |
| Command/event lanes | ACI acceptance and journal; hook `212–258`, bridge `143–248` | **SELECT** protocol precedent | Acceptance is persistence, not semantic judgment. |
| Journal/cursor | One accepted journal plus derived projections | **SELECT** journal; **DEFER** generic RWO cursor | Domain status remains work/gate-owned. |
| External effect adapter | No RWO-wide adapter; ARE fixed test double only, `execute.mjs:150–221` | **DEFER** | Semantic positivity and route completion cannot permit effects. |

## 5. RWO/orchestrator → reasoning-engine mapping

All rows use E3 architecture and executable hashes above; cross-repository bindings remain candidate unless explicitly bounded-L0.

| Stage | Exact mapping and selector | Owners and failure rule | Status |
|---|---|---|---|
| Entry | Confirmed dispatch/bound seat → proposed reasoning command; host-binding test `262–300`; ARE ACI binding §§2–4 | Confirmation owner authorizes dispatch; entry gate admits reasoning; mismatch blocks with zero evaluator calls | Candidate cross-repo mapping; current inputs separately observed |
| Intent | Expression/local record → route projection; `intent-route-resolver/src/resolve.mjs:103–185`, `authority_effect:none:172–180` | Intent/revision owner retains meaning; unresolved sources remain unresolved | Local resolver implemented; whole projector candidate |
| Actor cut | ACI commands/events → immutable verified journal span | ACI is the sole integrated writer; unknown schemas/digests or cross-run substitution block | ACI precedent observed; cross-repo mapper candidate |
| L0 evaluation | Frozen frame/catalog/observations/challenges/cut → semantic receipt; `reducer.mjs:159–320+` | External catalog/authority owners; evaluator owns admission, derivation, outcome, residue | Promoted bounded local witness |
| Exact effect | Persisted `RecommendedUnderSnapshot` receipt → fresh exact-effect gate → ACI effect intent; `execute.mjs:125–221` | Effect gate authorizes; ACI accepts lifecycle; evaluator never authorizes | Executed only with fixed test double |
| Replay | Verified immutable cut/artifacts → exact receipt; `replay.mjs:5–22` | Zero providers/tools/gates/effects; byte mismatch fails | Executable local L0; integrated bridge candidate |
| Revalidation | Prior references plus current authority/catalog/evidence → new run; `reducer.mjs:196–200,261–271` | Fresh IDs and gates; history immutable | Temporal branch implemented; integration unverified |
| L1–L3 | L0 receipt → future protocol/integration/effect layers | Each layer requires its owner’s conformance receipt | **DEFER**; whole-engine promotion absent |

## 6. Integration topology verdicts

| Topology | Verdict | Evidence and discriminator |
|---|---|---|
| Gate-adjacent bounded semantic evaluator | **SELECT** | E3 `execute.mjs:102–183`: entry block yields zero evaluation; recommendation still requires fresh effect gate. |
| ARE as ACI-subordinate leaf facade | **NARROW** | Retain addressed command in and semantic artifact reference out. KILL any variant that writes a second journal or emits effects directly. |
| Read-only semantic audit/replay sidecar | **NARROW** | May consume immutable cuts and emit non-authorizing artifacts. KILL any sidecar whose result directly releases routing/effects. |
| ARE as recursive composite body | **DEFER** | No accepted RWO definition, recursive compiler, or cross-repository composite fixture. |
| Generic RWO sidecars/cursor/effect adapters | **DEFER** | Current projections and fixed test doubles are insufficient. |
| Separate orchestrator-owned reasoning scheduler | **KILL** | Duplicates lifecycle/ACI authority and turns routing into semantic ownership. |
| “No relationship” | **KILL** as general answer; retain fallback | It discards the useful bounded evaluator witness, but becomes correct if owner conformance fails or standalone operation is selected. |
| Merge orchestrator journal and evaluator semantic state | **KILL**, not MERGE | Accepted history and semantic admission/outcome have distinct owners and failure modes. No safe MERGE candidate is evidenced. |

Selected shape:

`confirmed dispatch/leaf address → ACI acceptance and one journal → verified actor cut → gate-adjacent L0 evaluator → persisted semantic artifact → fresh exact-effect gate → ACI effect intent → external adapter`

## 7. Smallest safe documentation-only contract and recomposition path

The contract must contain:

1. Exact orchestrator commit, RWO hashes, ARE hashes/evaluator version, and `authority_effect: none`.
2. A versioned envelope containing confirmed dispatch ID/digest, bound seat address, ACI command ID/digest, verified journal span, semantic run ID, and frozen input digests.
3. An ownership table: ACI owns command/event acceptance, one journal, concurrency, replay cursor, and effect-intent lifecycle; evaluator owns semantic admission, applicability, derivation, typed outcome, residue, and receipt content; entry/effect gate owners retain their verdicts.
4. Ordering: confirmed topology → persisted entry decision → accepted actor facts → evaluator → persisted receipt → fresh exact-effect decision → ACI effect acceptance. Every mismatch/non-pass/persistence failure stops.
5. Historical replay uses exact immutable facts with zero mutable/external calls. Current revalidation creates a new run.
6. Unknown versions, missing digests, stale temporal state, cross-run substitution, or locally invented ACI identifiers fail closed.
7. Claim ceiling: documentation candidate only—no compatibility, implementation authorization, binding registration, integration, promotion, effect, publication, deployment, or production claim.

Recomposition path: resolve owner decisions → approve schemas/authority matrix → add paper-executable positive and negative fixtures → implement only the ACI-subordinate leaf seam → verify zero-evaluator blocked entry, non-authorizing positive result, effect-gate failure, retry/idempotency, replay, and revalidation → obtain owner conformance receipts → separately consider composite representation after an accepted RWO compiler exists.

## 8. Mandatory negative controls

| Control | Failing witness | Required behavior |
|---|---|---|
| Nested scheduler authority | Composite/leaf invokes another orchestrator or changes confirmed topology | Block; root alone routes, and topology changes require new confirmation. |
| Journal/semantic-owner collapse | Journal acceptance treated as admitted semantic fact or domain success | Block; evaluator independently admits and derives; work/gate owner retains status. |
| Routing-as-reasoning | Positive route label treated as a semantic verdict | Block; router may traverse only a separately owned typed verdict. |
| Result-as-authorization | `RecommendedUnderSnapshot` directly triggers an effect | Zero effect; persist receipt, obtain fresh exact-effect pass, then ACI acceptance. |
| Proposal-as-implementation | RWO hash/ontology term presented as tracked runtime | Reject claim; require tracked code, test selector, and execution receipt. |
| Target-host-binding spoofing | Parent research dispatch registers or invokes target binding | Block; target binding is an analyzed integration surface, not parent authority. |

## 9. Residue ledger

| Residue | Owner | Required evidence |
|---|---|---|
| RWO-OQ-001–010 and ontology 011–014 | Work-state, journal, protocol, policy, ontology, and promotion owners named in E2 | Accepted decisions, schemas, migration/replay rules, counterexamples, promotion receipt |
| WGQ-1–10 | Workflow discovery plus identity, Bus, Run, schema, and projection owners | Evidence-backed graph/taxonomy decisions and total confirmation→Dispatch→Run mapping |
| FastAPI-backed suite coverage | Target implementation/test-environment owner | Authorized dependency-complete rerun with exact module results |
| Host/provider adoption | Host adapter/provider owners | Versioned host witness, authenticated lifecycle, exact effect/output receipts |
| Cross-repository schemas | ACI, ARE, artifact, and effect owners | Versioned command, journal-cut, artifact-ref, and effect-intent contracts |
| One-journal conformance | ACI lifecycle owner | Proof no second integrated writer exists; recovery/replay fixtures |
| Domain catalog/challenge ownership | Catalog, applicability, precedence, challenge owners | Non-fixture catalogs, closure policies, owner receipts, negative fixtures |
| Recursive compiler/composite | RWO promotion/runtime owner | Accepted `WorkDefinition`, compiler, expansion fixture, cursor/replay tests |
| Real effects and integrated replay | Exact-effect, adapter, retention owners | Non-test-double effect witness, compensation/incident policy, exact integrated replay |
| Higher ARE layers | ARE/ACI/Bus/ACP/APT owners | Separate L1–L3 maturity and conformance receipts |
| Production/readiness | Deployment/security/operator owners | Explicitly scoped deployment, recovery, browser, security, and operational evidence |

## Claim ceiling

Evidence-bounded synthesis only; no implementation, authorization, selection, promotion, publication, deployment, production readiness, target binding, or external effect.
