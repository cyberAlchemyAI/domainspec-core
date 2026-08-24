# Arcanum–CAV2 integration wayfinding atlas

## Operator outcome

**Verdict:** `PASS / NO_DEPENDENCY_CLOSED_VERTICAL_WITNESS / RETAIN_SELECTION_GATE / DECISION_READY_ONLY`.

This atlas is ready for an operator to use as bounded input to Invoke define/design/plan. It is not a selection record, admission, mutation authorization, synchronization record, implementation-readiness finding, runtime-install receipt, release, deployment, publication, production acceptance, or whole-integration proof.

The nearest legal progress is to close the exact semantic-owner decision and the other `NV-001..006` evidence obligations. Until then:

- do not select `VS-IRO-001`, the Orchestrate canary, UOVARR-006, or any other candidate for execution;
- do not infer CAV2 canonicality from owner acceptance, or owner acceptance from CAV2 canonicality;
- do not infer installation from target presence, invocation from resolution, domain validity from controls, or synchronization from any projection;
- do not create a projection join owner, artifact, registry, validator, gate, or authority; and
- do not enter release, deployment, publication, or production branches without their own exact owners and selectors.

## Exact evidence boundary

| Evidence | Exact identity | What it proves | Ceiling |
|---|---|---|---|
| Parent | `3fe0d8399de8f8e75aebea4bf5e88a64f8b38184` | Parent source identity used by the synthesis | No authority or current-state inference outside the bounded evidence |
| Private CAV2 subtree | `b721be9134335c6816467cbb9d0df5a859f1eb2e` | Identity for the inspected private authority route | Documentary/reference/classification evidence only |
| Public Arcanum | HEAD `c67e06aabce6471169bc335f8a734987d907d692`; tree `902b5b234735abfed369b0c3d4fc122967b6a55e` | Identity for inspected public capability sources | No private semantic authority, import, release, or publication effect |
| Accepted Orchestrate candidate set | `b9eddd5cc97855b3e67aa60b474fc4728dd080d906184194f800ed821b9abbb4` | Accepted/applied source and generated repair plus reported focused 66-test receipt | Source/generated repair only; no repaired repo-local install or terminal live run |
| Repo-local Orchestrate | driver `80882d9d08857b9315ff3d63bda161ebca59414b37b46f3b6eb12d47c40d8d90`; validator `1d62bcab426029cd2a576e2a3a94820bde32ed4aecf0a4cd565c480621d098e1` | Runtime bytes are present | Present-but-stale; no reversible installation, resolution, invocation, or control proof for repaired identity |
| Historical UOVARR-005 | epoch `epoch-c01bcd6bad6dcb5e10bc312f`; unit `fdddfc686007af0a8227e3c5e40dacc0dcb1f096900db3ed3ffaa4eab1f26645`; token `0e0ea9f706f3b632de99b65ed5564f60f4bf6b813aa2ce4974928ac254229f4d`; executor `e85420601dbe7ae6450c788bfe82748c490d66780c57dbf1ce03d46c3648ab0f` | Exact historical terminal-first execution under older profiles | Not current-byte, current semantic, new-protocol, or UOVARR-006 proof |
| Continuity state file | untracked worktree `.arcanum/task-session/continuity/uovarr-reference-digest-repair.json`; sha256 `f0b66b88c381d8795aa7d91c9120d929389d3534e20e5a29927d986c3b353c0d` | Exact stale-state evidence inspected by the lifecycle explorer | Not bound to parent commit `P`; not a transition selector, current cursor, or canonical state |
| IRO candidate | closure `5ff017abf7bf98880b4a0dab7095a7dc59a9aac08993e04fbaa31b808e09ab8f` | Candidate-local behavior and validation evidence | `SWU-IRO-004` remains `admissionVerdict:block`, `mutationReady:false` |
| R2 evidence closure | feedback loops `2/2`; synthesis and three final reviewer receipts `pass`; writer handoff `ready` | The writer edge may produce a decision-ready research artifact | Does not prove writer/auditor joins, a validator-clean terminal stream, unique closeout, or live whole-route completion |

Selector notation below is `repository-identity::path#selector`. `C` denotes the fixed private CAV2 identity above. The continuity state file is explicitly untracked worktree evidence at the digest above, not evidence bound to the fixed parent identity `P`. An evidence-local heading, digest, file type, mechanism, or generic role is not an exact transition selector.

## Drift and provenance ledger

Explorer-return bindings point through each normalized receipt's `/artifacts/0` locator. A structured receipt pointer is a provenance locator, not a semantic selector or authority grant.

| Claim/evidence IDs | Drift | Explorer return binding | Immutable selector or structured pointer | Current finding and ceiling |
|---|---|---|---|---|
| `A0-A8`, `E-AUTH`, `E-AUTH-ROUTE` | survived | `receipts/explorer-authority.json#/artifacts/0`; corroborating lifecycle/runtime explorer locators at the same pointer | CAV2 subtree `b721be9134335c6816467cbb9d0df5a859f1eb2e`; Arcanum tree `902b5b234735abfed369b0c3d4fc122967b6a55e`; `C::SOURCE-MAP.md:10-33`; `C::authority/boundaries.md:8-14`; `C::authority/imports/README.md:3-32`; `C::authority/AUTHORITY-MODEL.md:48-103` | Reference, import/classification, semantic acceptance, planning, runtime, projections, and external effects remain separate owner-controlled predicates. |
| `D-CONST-001`, `CS-CONST-001`, `EC-CONSTITUTION` | changed from the 2026-08-06 interpretation; unchanged from R1 | `receipts/explorer-authority.json#/artifacts/0` | `receipts/evidence-closure.json#/claim_rows/2`; `receipts/synthesis.json#/artifacts/5` | Project-local constitution is kind/scope; candidate is lifecycle maturity; C18 remains non-causal guidance. |
| `D50`, `D51` | survived unresolved | `receipts/explorer-authority.json#/artifacts/0` | `receipts/synthesis.json#/artifacts/5` | Cross-owner terminology conflict remains routed to Definitions Governance. |
| `D-RUN-001`, `E-ORCH`, `EC-ORCHESTRATE-SOURCE` | changed/advanced | `receipts/explorer-runtime.json#/artifacts/0` | candidate-set digest `b9eddd5cc97855b3e67aa60b474fc4728dd080d906184194f800ed821b9abbb4`; `receipts/evidence-closure.json#/claim_rows/4` | Source/generated repair and focused tests survive; installed parity and terminal live proof remain absent. |
| R1 claim “repo-local runtime absent” | died | `receipts/explorer-runtime.json#/artifacts/0` | driver `80882d9d08857b9315ff3d63bda161ebca59414b37b46f3b6eb12d47c40d8d90`; validator `1d62bcab426029cd2a576e2a3a94820bde32ed4aecf0a4cd565c480621d098e1` | Repo-local runtime is present-but-stale; presence proves neither repaired installation nor invocation. |
| R1 claim “observability mismatch invalidated” | died; configuration-drift claim survived | `receipts/explorer-lifecycle.json#/artifacts/0`; `receipts/explorer-runtime.json#/artifacts/0` | installed format `0.1.0`; canonical template `0.2.0`; `receipts/evidence-closure.json#/claim_rows/9` | Exact append/dedupe witness remains absent; no observed-integration or synchronization claim follows. |
| `E-LIFE`, `E-UOVARR`, `EC-LIFECYCLE-CURRENT` | survived with narrower ceiling | `receipts/explorer-lifecycle.json#/artifacts/0` | epoch `epoch-c01bcd6bad6dcb5e10bc312f`; unit `fdddfc686007af0a8227e3c5e40dacc0dcb1f096900db3ed3ffaa4eab1f26645`; `receipts/evidence-closure.json#/claim_rows/7` | UOVARR-005 is historical terminal-first evidence only; current-byte and new-protocol inferences died. |
| continuity-file parent binding | changed/corrected | `receipts/explorer-lifecycle.json#/artifacts/0` | untracked worktree `.arcanum/task-session/continuity/uovarr-reference-digest-repair.json`; sha256 `f0b66b88c381d8795aa7d91c9120d929389d3534e20e5a29927d986c3b353c0d` | Stale-state evidence only; not parent-commit evidence, a transition selector, or a UOVARR-005-to-006 cursor. |
| `EC-LIFECYCLE-CANDIDATE`, split-precloseout live inference | candidate design survived; live inference died | `receipts/explorer-lifecycle.json#/artifacts/0` | `receipts/evidence-closure.json#/claim_rows/8`; `receipts/synthesis.json#/artifacts/5` | Schema/fixture evidence only; exact owner decision or live admitted witness remains open under `NV-004`. |
| `E-IRO`, `VS-IRO-001` | survived as leading candidate; readiness inference died | `receipts/explorer-lifecycle.json#/artifacts/0` | closure `5ff017abf7bf98880b4a0dab7095a7dc59a9aac08993e04fbaa31b808e09ab8f`; `SWU-IRO-004` values `admissionVerdict:block`, `mutationReady:false` | Candidate-local behavior only; semantic acceptance, admission, and implementation readiness remain blocked. |
| `EC-JOIN-METAOWNER`, `JOIN-01` | killed | final definitional review at `receipts/skeptic-definitional.json#/artifacts/0` | `receipts/evidence-closure.json#/claim_rows/10`; `receipts/synthesis.json#/artifacts/5` | Only an ephemeral non-authoritative same-tuple Boolean is permitted; no join infrastructure exists. |
| `NO_DEPENDENCY_CLOSED_VERTICAL_WITNESS`, `EC-VERTICAL-WITNESS`, `NV-001..006` | survived; vertical-witness claim killed | all three explorer return locators plus `receipts/skeptic-non-vacuity.json#/artifacts/0` | `receipts/evidence-closure.json#/claim_rows/12`; `receipts/evidence-closure.json#/open_obligations` | Decision-ready research only; no implementation readiness or whole integration. |
| `R2-ADVANCEMENT`, `E-R2`, `EC-ORCHESTRATE-LIVE` | advanced beyond the failed prior run; terminal claim remains deferred | `receipts/explorer-runtime.json#/artifacts/0` | `receipts/synthesis.json#/action_id` = `spawn-0004`; reviewer receipts `/action_id` = `spawn-0005..0007`; `receipts/evidence-closure.json#/writer_ready`; `orchestration/run-002/feedback/auditor-writer-round-001.json#/audited_findings_sha256` = `bb8cfe250a854f1045c53521623aa6d8c13de5eecdaa4ca4cd38a5e333680db7` | The failed prior run did not advance beyond the first wave. R2 passed the explorer gate, bound and completed synthesis, admitted three passing final reviews, exposed the writer, persisted the audited writer artifact, and reached one bounded auditor-to-writer feedback. It still lacks admitted revised-writer/auditor receipts and validator-clean unique terminal closeout, so `NV-006` remains open. |

## Independent typed state vector

For semantic slice `s`, runtime target `t`, environment `e`, and publication channel `h`:

```text
V(s,t,e,h) = {
  authority: {
    referenced,
    import_disposition,
    semantic_acceptance,
    cav2_artifact_owner_acceptance
  },
  planning: {
    invoke_plan,
    readiness,
    selection,
    task_session_admission
  },
  repository: {
    canonical_in_arcanum,
    cav2_canonical_kind_membership,
    cav2_declared_production_process_completed,
    canonical_in_cav2,
    implemented_in_owner_repo
  },
  runtime: {
    generated_for_runtime,
    present_at_target,
    reversibly_installed_at_target,
    resolved_at_target,
    invoked_at_target,
    control_validated_at_target,
    domain_validated_at_target
  },
  lifecycle: {
    current_terminal_first_closed,
    candidate_split_precloseout_closed,
    continuity_cursor
  },
  projections: {
    craft_projected,
    inventory_projected,
    ontology_projected,
    observability_appended
  },
  dispositions: {
    public_owner_disposition,
    private_owner_disposition
  },
  external: {
    released_to_target,
    deployed_to_environment,
    published_to_channel,
    production_accepted_in_environment
  }
}
```

Each coordinate is independently tagged `absent | described | candidate | observed | executed | owner_accepted | validated | blocked | stale | unverified_current`. No coordinate advances another.

The corrected CAV2 predicates are:

```text
CanonicalKindMemberInCAV2(a,k) :=
  kind(a) = k
  AND k belongs to the existing enumerated CAV2 canonical-kind set

ProducedByDeclaredCAV2Process(a,id,p) :=
  p is the declared CAV2 production process for kind(a)
  AND p produced exact identity id

CanonicalInCAV2(a,id) := EXISTS k,p:
  CanonicalKindMemberInCAV2(a,k)
  AND ProducedByDeclaredCAV2Process(a,id,p)

OwnerAcceptedInCAV2(a,id,o,d) :=
  exact owner o issued bounded decision d over identity id
```

`CanonicalInCAV2` and `OwnerAcceptedInCAV2` are independent. The exact kind-enumeration and declared-process selectors were not exposed to this bounded evidence loop. For `VS-IRO-001`, canonical-kind membership, process completion, and derived CAV2 canonicality are therefore `unverified_current`, not false; semantic acceptance remains absent.

Correlation keys remain descriptive, not promotion machinery:

```text
K-task = (
  source_identity, plan_epoch, unit_id, attempt_id,
  admission_token_digest, execution_receipt_digest,
  owner_receipt_digest, terminal_receipt_digest, cursor_digest
)

K-runtime = (
  canonical_digest, generated_digest, target_id,
  install_receipt_digest, invocation_id, input_digest, output_digest
)

K-dispatch = (dispatch_id, run_id, wave_id, action_id, agent_id)
```

For this research closeout only, `EvidenceClosureConjunctionNow(K-task)` may be calculated ephemerally as continuity AND Craft AND Inventory AND ontology AND observability evidence for one tuple. It has no owner, artifact, repository state, legal transition, gate, or authority. Its current value is `unestablished`; “synchronized” is prohibited as a durable inference.

## Current location by axis

| Axis | Current state | Operator stop |
|---|---|---|
| Public-to-private reference | `observed` | No authority transfer or semantic acceptance |
| Import disposition | `candidate/stale` | No import admission; stale provenance or conflict returns to the CAV2 route owner |
| IRO semantic acceptance | `blocked/absent` | Exact domain-semantic owner and selector are unresolved (`NV-001`) |
| Invoke plan/readiness | `described`; selected IRO frontier blocked | WPRA is non-selecting and non-mutating |
| Selection | `absent` | Retain the explicit selection gate |
| Task Session admission | `blocked` for `SWU-IRO-004` | No token consumption or execution |
| Arcanum Orchestrate source/generated | `owner_accepted/validated` for canonical, repo-Codex, and Claude candidate bytes | No repaired repo-local install or terminal live execution |
| Repo-local Orchestrate presence | `observed/stale` | Presence is not reversible installation |
| Repaired target resolution/invocation/controls/domain | `unverified_current` | Host agent allocation proves none of these predicates |
| IRO behavior | `executed candidate` | Candidate tests cannot substitute for acceptance/admission |
| Current terminal-first UOVARR route | `historically executed`, `unverified_current` | Drifted bytes and absent 005-to-006 cursor prevent current claims |
| Candidate split-precloseout route | `candidate/fixture-validated` | No live exact end-to-end attempt |
| Continuity | `stale` | UOVARR-004-to-005 exists; UOVARR-005-to-006 is absent |
| Craft | `absent` exact projection | Receipts do not imply Craft |
| CAV2 machine Inventory | `absent` | README is not a machine index |
| Ontology | `candidate projection only` | No authority and no same-tuple evidence closure |
| Observability | `stale/absent witness` | Installed format `0.1.0` versus canonical template `0.2.0`; exact append/dedupe unproved |
| Public/private dispositions | `unentered` | One owner cannot decide the other branch |
| Release/deployment/publication/production | `absent` | Target-specific branches and owners remain dormant |

## Current and candidate lifecycle routes

### Current terminal-first route

```text
semantic acceptance
  -> Invoke plan
  -> readiness
  -> explicit selection
  -> Task Session baseline lock
  -> single-use admission
  -> execution and validation
  -> task-session.executor-receipt.v1 terminal result
  -> invoke-refresh.closeout-owner-receipt.v1
  -> Continuation Router join
  -> successor continuity cursor
```

UOVARR-005 is historical evidence for this route under older profiles. It does not prove current bytes, current semantic acceptance, a live split-precloseout protocol, or a current UOVARR-006 cursor.

### Candidate split-precloseout route

```text
semantic acceptance
  -> Invoke plan
  -> readiness
  -> explicit selection
  -> Task Session baseline lock
  -> single-use admission
  -> execution, validation, and reconciliation
  -> task-session.precloseout-execution-receipt.v1
     (must not contain closeout_join)
  -> invoke.precloseout-refresh-closeout-receipt.v1
  -> final Task Session terminal receipt
     (joins exactly one Invoke receipt)
  -> emit successor cursor; never execute successor
```

This route has schema/fixture evidence only. The operator must either obtain a separately admitted live witness or retain terminal-first behavior through an exact owner decision. C18 is non-causal candidate guidance and participates in neither route as a gate, selector, token, admission, or authority source.

## Exact owner and selector transition audit

Absent owners and selectors are stops, not blanks an operator may fill by inference.

| Edge | Exact current owner status | Exact selector | Disposition and operator consequence |
|---|---|---|---|
| `AUTH-01` | unresolved exact upstream/CAV2 recorder | `C::SOURCE-MAP.md:10-33`; `C::authority/boundaries.md:8-14` | Retain reference-only. Selectors prove behavior, not owner identity. |
| `AUTH-02` | named CAV2 authority-import owner | `C::authority/imports/README.md:3-32` | Retain classification route. D7/D8 are labels without an exposed path here. |
| `AUTH-03` | unresolved narrow-kind disposition owner; Decision Gate is conditional escalation | `C::authority/AUTHORITY-MODEL.md:48-103` | Retain default-deny requirement without an exact owner claim. |
| `AUTH-04` | unresolved exact domain-semantic owner (`NV-001`) | absent | Block semantic acceptance. Process receipts cannot substitute. |
| `AUTH-G1` | none | absent | Remove from graph. C18 is non-causal candidate guidance. |
| `PLAN-01` | Invoke Plan | absent | Retain planned edge; no direct path exposed. Does not select or admit. |
| `PLAN-02` | Work Pack Readiness Audit | absent | Retain non-selecting audit edge. |
| `PLAN-03` | unresolved authorized selector | absent | Block selection. |
| `PLAN-04` | Task Session | absent | Retain single-use admission contract; exact path absent. |
| `RUN-01` | Task Session; executor unresolved pending selection | absent | Conditional execution only; no executable route exists yet. |
| `LIFE-CUR-01` | Task Session | absent | Historical terminal-first edge; receipt type is not a selector. |
| `LIFE-CUR-02` | Invoke Refresh | absent | Historical owner-closeout edge. |
| `LIFE-CUR-03` | Continuation Router; cursor-persistence owner unresolved | route selector absent; untracked worktree `.arcanum/task-session/continuity/uovarr-reference-digest-repair.json` at sha256 `f0b66b88c381d8795aa7d91c9120d929389d3534e20e5a29927d986c3b353c0d` is stale-state evidence only | Retain historical route with narrowed ceiling; 005-to-006 cursor absent. |
| `LIFE-SPLIT-01` | Task Session | absent | Retain candidate precloseout edge; fixture-only. |
| `LIFE-SPLIT-02` | Invoke Refresh | absent | Retain candidate owner hop; no live exact transition. |
| `LIFE-SPLIT-03` | Task Session | absent | Retain candidate terminal join; no live exact transition. |
| `RT-01` | unresolved exact public canonical and projection owners | absent | Retain evidenced source/generated relation, not owner-complete route. |
| `RT-02` | unresolved target consumer/install owner | absent | Retain presence predicate only. |
| `RT-03` | unresolved reversible-install owner | absent | Retain blocked predicate under `NV-003`. |
| `RT-04` | unresolved; host resolver is mechanism, not owner | absent | Retain resolution predicate only. |
| `RT-05` | unresolved; host invoker is mechanism, not owner | absent | Retain invocation predicate only. |
| `RT-06` | unresolved runtime-validation owner | absent | Retain control predicate only. |
| `RT-07` | unresolved semantic/product-validation owners | absent | Retain blocked predicate under `NV-001/002`. |
| `PROJ-00` | unresolved durable cursor owner | transition selector absent; stale continuity file is state evidence only | Retain independent predicate; never execute successor. |
| `PROJ-01` | Craft | absent | Retain independent predicate; current exact projection absent. |
| `PROJ-02` | CAV2 Inventory | absent | Retain independent predicate; README is no machine index. |
| `PROJ-03` | unresolved exact ontology owner | absent | Retain candidate/read-model predicate only. |
| `PROJ-04` | Signal Observer | absent | Retain independent observation predicate. |
| `JOIN-01` | none | none | **Killed.** No transition, meta-owner, durable artifact, module, registry, validator, gate, receipt, or authority may be created or inferred. |
| `DISP-01` | unresolved exact public artifact owner | absent | Retain required public branch; CAV2 cannot decide it. |
| `DISP-02` | unresolved exact private artifact owner | absent | Retain required private branch; Arcanum cannot decide it. |
| `EXT-REL-PUB` | unresolved public release owner | absent | Dormant target-specific branch. |
| `EXT-REL-PRIV` | unresolved private release owner | absent | Dormant target-specific branch. |
| `EXT-DEP` | unresolved named-environment deployment owner | absent | Dormant environment branch. |
| `EXT-PUB` | unresolved publisher and boundary owner | absent | Dormant channel branch. |
| `EXT-PROD` | unresolved environment acceptance owner | absent | Dormant environment branch. |

## Preserved evidence-closure dispositions

These rows are the writer handoff contract. Deferred and killed rows remain deferred and killed; nothing in this atlas revives them.

| Claim row | Disposition | Binding | Ceiling |
|---|---|---|---|
| `EC-AUTH-ROUTE` | bound | CAV2 source-map, boundary, imports, and authority-model selectors under exact parent/CAV2 identities | Documentary/reference/classification route only |
| `EC-SEMANTIC-OWNER` | **deferred** | Owner unresolved; selector absent | Blocks semantic acceptance and implementation readiness |
| `EC-CONSTITUTION` | bound | Project-local constitution is kind/scope while candidate is lifecycle maturity; C18 is non-causal candidate guidance | No current constitutional gate or blanket canon |
| `EC-CANONICALITY` | bound | Arcanum and CAV2 canonical predicates are repository-qualified; CAV2 canonicality is enumerated-kind plus declared-process completion and independent of owner acceptance | CAV2 canonicality of IRO remains `unverified_current` |
| `EC-ORCHESTRATE-SOURCE` | bound | Candidate-set digest `b9eddd5cc97855b3e67aa60b474fc4728dd080d906184194f800ed821b9abbb4` and focused 66-test apply receipt | Source/generated repair only |
| `EC-ORCHESTRATE-LIVE` | **deferred** | R2 causal stream must reach terminal auditor and closeout | No completed live multi-wave claim |
| `EC-RUNTIME-PREDICATES` | bound | Generation, presence, reversible installation, resolution, invocation, control validation, and domain validation are independent | Repo-local is present-but-stale; repaired target predicates unverified |
| `EC-LIFECYCLE-CURRENT` | bound | UOVARR-005 terminal-first route is historical evidence under older profiles | Not current-byte or new-protocol evidence |
| `EC-LIFECYCLE-CANDIDATE` | **deferred** | Split precloseout route has schema/fixture evidence with no live exact attempt | Candidate protocol only |
| `EC-PROJECTIONS` | bound | Continuity, Craft, CAV2 Inventory, ontology, and observability are independent predicates | Same-tuple conjunction unestablished; no durable synchronized state |
| `EC-JOIN-METAOWNER` | **killed** | `JOIN-01`, evidence join owner, durable join artifact, module, registry, validator, gate, and authority removed | Research may calculate only an ephemeral non-authoritative Boolean |
| `EC-EXTERNAL` | **deferred** | Release, deployment, publication, and production acceptance are target-specific branches with unresolved owners/selectors | All unentered |
| `EC-VERTICAL-WITNESS` | **killed** | `NV-001..006` remain open and all final reviewers preserve the no-witness verdict | No implementation readiness or whole integration |

## Candidate ranking without selection

1. Orchestrate portion of `CAN-CANARY-001`: strongest predecessor canary; terminal R2 witness remains open.
2. `VS-IRO-001`: leading semantic slice; blocked by source-frontier mismatch, exact semantic acceptance, and fresh Task Session admission.
3. UOVARR-006 attempt-004: leading lifecycle-witness candidate; cannot substitute for the semantic slice.
4. Inventory: byte canary only.
5. `CAN-AOV-001`: **deferred**.
6. `CAN-AGI-001`: **hold**.

This ordering is research prioritization only. It makes no execution selection.

## Critical path and parallel lanes

### Critical path

```text
freeze exact identities and privacy boundaries
  -> obtain exact domain-semantic acceptance
  -> author finite Invoke plan
  -> pass non-selecting readiness audit
  -> explicitly select exactly one unit and attempt
  -> obtain attempt-bound Task Session admission
  -> prove exact generation, reversible installation, resolution,
     invocation, and controls at every declared runtime target
  -> execute and domain-validate under frozen inputs
  -> complete the current lifecycle, or separately admit and prove
     the candidate split-precloseout route
  -> emit the exact successor continuity cursor
  -> independently prove Craft, Inventory, ontology, and observability
     for the same K-task tuple
  -> obtain independent public and private dispositions
  -> enter any release, deployment, publication, or production branch
     only through its separately named owner and selector
```

### Parallel lanes

- Definitions Governance resolves D50/D51 without redefining across public/private owners.
- The constitution owner adjudicates selected candidate rules; the project-local constitution remains candidate.
- Runtime owners close repo-local repaired identity, durable restoration, resolution, invocation, and control evidence.
- The R2 route closes its writer, auditor, causal validation, and unique terminal closeout.
- Lifecycle owners decide the split protocol and prepare UOVARR-006 attempt-004 plus a 005-to-006 cursor.
- Each projection owner specifies and validates its own tuple correlation and discriminating negatives.
- Public/private disposition and external owners remain dormant until their prerequisites and exact selectors exist.

Parallel progress cannot bypass a critical-path gate or imply another lane's predicate.

## Finite negative contract and owner-local rollback

| Phase | Must fail closed when | Stop or rollback |
|---|---|---|
| Source/reference | Identity or target is stale; selector is absent; provenance conflicts; private prose would cross into public Arcanum | Stop before admission; refresh or defer the private reference |
| Import/semantic authority | Import is rejected; owner is missing, wrong, ambiguous, or inferred; effect/non-effects are not exact | Reject, defer, or revise under the actual owner |
| Invoke/readiness | Entry/closeout inventory is incomplete; readiness fails; WPRA is treated as selection | Return defects to Invoke; do not select or mutate |
| Selection | Zero or multiple units/attempts; implicit selection; selector absent | Block Task Session; revoke only a pre-admission selection if authorized |
| Admission | Token replay; stale or mismatched attempt; baseline drift; non-atomic consumption | Preserve the failed attempt; do not retry implicitly |
| Runtime delivery | Generated/target identity mismatch; target presence lacks pre-state or durable restore material | Abort activation or restore the exact target baseline |
| Resolution/invocation/controls | Wrong capability resolves; invocation is missing/duplicated; invalid or missing controls are accepted; collision/replay is mishandled | Disable/uninstall or restore under the target owner; retain failure evidence |
| Domain behavior | Positive, ambiguity, invalidity, mismatch, privacy, replay, or zero-effect case is wrong; data leaks or undeclared side effects occur | Disable the adapter and restore product pre-state under the semantic/product owners |
| Execution evidence | Validation, reconciliation, identity, digest, or declared-inventory check fails | Stop before owner closeout; preserve the exact attempt evidence |
| Precloseout/owner hop | Premature `closeout_join`; missing, wrong, or duplicate owner receipt | Block terminal closure; never fabricate the owner hop |
| Terminal/continuity | Missing or duplicate join; stale cursor; successor auto-executes | Preserve evidence; invalidate/expire only the bad cursor and repair through owners |
| Projections | Invalid Craft/Inventory/ontology projection; observer duplicate or missing append; same-tuple mismatch | Rebuild or expire only the failed projection; no generic join rollback exists |
| Orchestrate route | Action/agent identity mismatch; receipt contamination; timeout/interrupt defect; partial-wave failure; invalid causal prefix; missing join/gate/close; duplicate or non-unique terminal closeout | Fail closed through the declared Orchestrate recovery/closeout path; do not reconstruct missing causal events |
| Public/private disposition | One owner is treated as universal or the public/private boundary is crossed | Keep branches separate; return to the affected artifact owner |
| External branch | Release/environment/publisher/production owner or selector is absent; rollback target is unspecified | Remain at the prior state; use separately owned withdrawal, environment rollback, retraction, or acceptance revocation only |

There is no generic demotion runner, integration rollback owner, or meta-owner. Rollback is finite and owner-local: defer references, reject candidates, preserve failed attempts, restore exact runtime/product pre-state, disable adapters, expire only failed projections, and use separately authorized external rollback.

## Open non-vacuity obligations

| ID | Required witness | Current stop | What closes it |
|---|---|---|---|
| `NV-001` | Exact domain-semantic acceptance bound to current source, privacy, effect, and non-effects | Process owners are named, but exact semantic owner/selector and acceptance are missing | A bounded exact decision by the actual semantic owner; lifecycle receipts cannot substitute |
| `NV-002` | Current IRO frontier closure and fresh successful Task Session admission | `SWU-IRO-004` remains blocked | Reconcile current frontier, explicitly select one attempt, pass fresh preflight, and obtain the exact single-use admission |
| `NV-003` | Repaired identity at every declared target with durable restoration, resolution, invocation, and controls | Repo-local bytes are stale; presence only is observed | Exact target identity plus pre-state/restore receipt, resolution receipt, invocation receipt, and discriminating control results |
| `NV-004` | Live split-precloseout chain, or exact owner decision retaining terminal-first behavior, plus UOVARR-005-to-006 cursor | Split route is fixture-only; behavior bytes drifted; cursor absent | One live exact admitted route and an emitted, non-executed successor cursor |
| `NV-005` | Independent same-tuple continuity, Craft, CAV2 Inventory, ontology, and observability evidence with mismatch/dedupe negatives | Constituents are absent, candidate, or stale | Independent exact receipts/evidence for one `K-task`; only then may the ephemeral conjunction evaluate true |
| `NV-006` | Validator-clean terminal R2 evidence across joins, gates, later waves, failure closure, and unique closeout | Synthesis and reviewers passed; writer/auditor/terminal closeout remain unproved by the supplied evidence | Admit the exact writer and auditor receipts, close the causal stream uniquely, and pass terminal validation |

`NV-001..006` block implementation readiness. They do not block use of this atlas as decision-ready research.

## R2 route live state

| Route point | Supplied evidence | Live interpretation |
|---|---|---|
| Synthesis `spawn-0004` | normalized receipt `pass`; base synthesis plus feedback rounds 1 and 2 persisted | Synthesis is complete at the research ceiling |
| Review `spawn-0005` | precedent reviewer receipt `pass` | Precedent review passed; round-2 corrections remain binding |
| Review `spawn-0006` | non-vacuity reviewer receipt `pass` | `NV-001..006` remain open; no witness was manufactured |
| Review `spawn-0007` | definitional reviewer receipt `pass` | Corrected canonicality and no-join semantics remain binding |
| Evidence closure | `ready`; feedback loops used `2`, remaining `0`; `writer_ready:true` | Writer edge is authorized only at the decision-ready research ceiling |
| Writer `spawn-0008` | this `findings.md` is the declared artifact | Parent runner must normalize and admit the writer receipt; this file is not its own receipt |
| Auditor/final route | no terminal auditor receipt, join, gate, or unique closeout in the supplied evidence | Open. `EC-ORCHESTRATE-LIVE` stays deferred and `NV-006` stays open |

The live route may advance only through the parent-owned native receipt/join/gate/closeout machinery. This artifact cannot self-certify the writer action or terminal R2 run.

## Open operator gates

1. **Semantic gate:** identify the exact domain-semantic owner and selector; obtain exact acceptance (`NV-001`).
2. **IRO frontier/admission gate:** reconcile current IRO bytes and admit one explicitly selected attempt (`NV-002`).
3. **Runtime target gate:** prove repaired identity, durable restoration, resolution, invocation, and controls at every declared target (`NV-003`).
4. **Lifecycle decision/witness gate:** retain terminal-first by exact owner decision or separately admit and prove split-precloseout; emit 005-to-006 cursor (`NV-004`).
5. **Projection evidence gate:** independently prove same-tuple continuity, Craft, CAV2 Inventory, ontology, and observability, without introducing join infrastructure (`NV-005`).
6. **R2 terminal gate:** admit writer/auditor results and obtain a validator-clean, uniquely closed causal stream (`NV-006`).
7. **Definitions/constitution gates:** resolve D50/D51 through Definitions Governance and adjudicate any chosen constitutional candidate; C18 remains guidance.
8. **Disposition/external gates:** obtain independent public/private decisions, then name exact target owners/selectors for any release, deployment, publication, or production branch.

## Claim ceiling and next legal use

This is a **decision-ready research atlas** with **no dependency-closed vertical witness**. It may be supplied to Invoke define/design/plan to freeze evidence, record unresolved owner decisions, preserve the current/candidate lifecycle split, construct a finite Work Pack, and encode the acceptance, negative, and rollback contracts.

It authorizes no selection, admission, token consumption, implementation, mutation, synchronization, installation, invocation, semantic adaptation, promotion, release, deployment, publication, production acceptance, or whole-integration claim. Inventory, Git state, tests, ontology, receipts, candidate canonicality, and agent allocation cannot be promoted beyond their explicitly typed predicates.
