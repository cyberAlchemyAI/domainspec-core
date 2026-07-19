# Invoke Distill Enforcement Review - Candidate Findings

Dispatch: `2026-07-17-invoke-distill-enforcement-review`

Status: accepted by the final independent auditor after the single verifier zig-zag; no
reviewed target has been mutated.

## Revised Candidate Verdict

**FIX.** Invoke names the right Distill operation for plan mode, but the current
contracts, fixture runner, and Workbench observability accept a verdict label without
proving a contract-complete Distill execution. The Workbench decomposition is not thereby
disproved; its preserved Distill status is **unverified** and must be replayed after the
enforcement path exists.

## 1. Distill Runtime And Role Contract

| Finding | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| The governing role boundary is sound: use true Proposer/Balancer subagents when the active runtime supports them; use labeled single-agent role passes only when subagents are unavailable. Both paths owe the same role trace. | `arcanum/arcana/distill/SKILL.md` | Attack source: Abramsky final, **Rejected Claims** and **Stable Disagreement** (`attacks.md`, lines 169-180); Ashby final, **Rejected Claims** (`attacks.md`, lines 243-248). Target: runtime policy at lines 83-92. | N/A (KEEP) | Keep this policy. Make runtime capability and selected execution path independently attestable; do not invent agent identities for fallback. |
| A successful Distill execution has semantic obligations that an unqualified verdict cannot satisfy: finite budget, preserved role trace, categorized objections, techniques, reconciliation, and navigable result. | `arcanum/arcana/distill/SKILL.md` | Attack source: Abramsky initial **F1** and final **Highest-Severity Findings** (`attacks.md`, lines 15-40 and 102-111); Shannon initial **Finding 1** (`attacks.md`, lines 300-305). Target: process at lines 95-128, technique trace at lines 131-143, quality bar at lines 172-185, output contract at lines 220-245. | MAJOR | Define a contract-complete, validator-checkable evidence projection and require Invoke to validate it whenever Distill runs. Select the concrete schema architecture through lifecycle acceptance. |

**Verdict: KEEP** for the true-subagent/fallback role policy itself. The enforcement
projection is missing in Invoke and runtime validation, not contradicted by Distill's
role definition.

### True-Subagent And Fallback Boundary

True subagents are mandatory **when the active runtime supports them**. The only permitted
fallback is explicit `role-simulation` with labeled Proposer and Balancer pass boundaries
when subagents are unavailable. The repository's review registration says the runtime
supported subagents (`telemetry/agents/subagents-dispatch.yaml`, lines 3456-3468), but that
later declaration is not a runtime-owned receipt for the historical Workbench execution.
The Workbench execution path therefore remains **unknown**: neither “true subagents ran”
nor “subagents were unavailable” is proved. Attack source: Abramsky initial **F4** and
final **Stable Disagreement** (`attacks.md`, lines 72-82 and 178-180); target role boundary:
`arcanum/arcana/distill/SKILL.md`, lines 83-92.

## 2. Invoke Root And Plan Contracts

| Finding | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| Invoke correctly specifies the logical call for plan mode: run Distill in Validate mode over the objective, design boundary, layering artifact, plan, work-pack/SWU manifest, handoff, and gap ledger before pass/flag. It does not require execution evidence covering Distill's literal output contract. | `arcanum/spells/invoke/plan.md` | Attack source: Abramsky initial **F2** and Ashby initial **Finding 1** (`attacks.md`, lines 42-55 and 200-205); Shannon initial **Finding 3** (`attacks.md`, lines 314-318). Target: call inputs at lines 116-126 and mandatory gate at lines 297-298; output records only verdict/recomposition/gap count at lines 360-373. | CRITICAL | Require validator-issued, contract-complete execution evidence in every applicable pass/flag; missing or invalid evidence blocks mutation-capable routing. |
| The root contract can report Distill outcome data without proof of execution. | `arcanum/spells/invoke/README.md` | Attack source: Abramsky final **Highest-Severity Findings** (`attacks.md`, lines 102-111); Ashby final **Surviving Findings 1** (`attacks.md`, lines 250-253). Target: automatic validation and routing rule at lines 134-144, result fields at lines 205-221, and global gate at lines 223-235. | CRITICAL | Replace authored verdict trust with validated contract-complete evidence; only the validator result may unlock mutation-capable handoff. |

**Verdict: FIX.** Invoke called for Distill correctly at the prose/route level, but the
review cannot establish that the Workbench run actually invoked Distill correctly. The
observable call and its role-separated execution are unproved.

## 3. Validation Fixture Runner

| Finding | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| Current fixtures admit Markdown-only false passes by checking labels, headings, and selected phrases rather than execution evidence. | `arcanum/spells/invoke/development/run-validation-fixtures.sh` | Attack source: Abramsky initial **F2** and final **Highest-Severity Findings** (`attacks.md`, lines 42-55 and 102-111); Ashby final **Surviving Findings 2** (`attacks.md`, lines 255-256); Shannon initial **Finding 1** (`attacks.md`, lines 300-305). Target: generic checks at lines 337-359, plan checks at lines 505-557, integration checks at lines 640-648. A passing expected file contains only `Distill validation: pass; recomposition proof pass; gap count 0` at `arcanum/spells/invoke/development/fixtures/INV-PLAN-PASS-001.expected.md`, lines 1-24. | CRITICAL | Add executable positive, missing-evidence, and fabricated-evidence cases. Reject unresolved or same role IDs, mutable inputs without exact immutable-content identity, inconsistent verdicts/counts, invalid round accounting, uncategorized objections, and missing reconciliation/technique evidence. |

**Verdict: FIX.** A schema-presence check alone would merely move the gameable assertion
from Markdown to JSON. The validator must perform semantic, provenance, and cross-artifact
checks.

## 4. Execution Evidence, Provenance, And Semantic Validation

| Finding | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| Invoke has no contract-complete, validator-checkable evidence projection that binds a Distill result to its roles, reviewed inputs, and downstream result. | `arcanum/spells/invoke/README.md`; `arcanum/arcana/distill/SKILL.md` | Attack source: Abramsky final **Minimal Enforcement Architecture** and **Stable Disagreement** (`attacks.md`, lines 113-167 and 178-180); Ashby final **Minimal Enforcement Architecture** and **Stable Disagreement** (`attacks.md`, lines 267-294); Shannon final **Changed From Initial View** and **Minimal Enforcement Architecture** (`attacks.md`, lines 328-371). Target: Invoke result fields stop at verdict/gaps/recomposition at `README.md`, lines 205-221, while Distill requires role/technique/result traces at `SKILL.md`, lines 202-245. | MAJOR | Require contract-complete evidence and an executable validator. Treat a versioned receipt plus runtime event ledger as the recommended architecture, not as already-mandated law. |

**Verdict: FIX.** Mandatory evidence coverage, independent of serialization:

- parent Invoke run identity, Invoke mode, Distill mode, finite round budget, rounds
  completed, and termination reason;
- `role_execution_path: true-subagents | role-simulation` and labeled
  Proposer/Balancer role trace;
- categorized Balancer objections, reconciliation decision per objection, and stable
  disagreement;
- techniques run and techniques skipped with reason, verdict, gaps, recomposition result,
  and next route;
- exact immutable-content identity for every reviewed input that can unlock mutation;
- evidence that both role paths actually occurred, without fabricated native-agent fields.

The **recommended new architecture, requiring lifecycle acceptance**, is a versioned
`DistillExecutionReceipt` backed by runtime-owned append-only execution events for **both**
paths. True-subagent events should resolve distinct invocation IDs/handles, outputs, parent
run linkage, and governed dispatch/helper lineage. Role-simulation events should record an
ordered capability probe, labeled role-pass boundaries, transcript/output digests, and
parent run linkage. The capability probe is a proposed enforcement strengthening; current
Distill law does not require recorded proof of runtime unavailability. Labeled fallback
fields alone do not prove that simulation occurred.

Schema validation is necessary but insufficient. Semantic/provenance validation must
resolve both execution paths against runtime-owned events; enforce distinct role passes;
check finite rounds and termination; require an objection category and reconciliation for
each objection; validate required/skipped techniques; recompute transcript/output and input
identity evidence; and require the evidence verdict, Invoke result, observability state,
work-pack identity, and counts to agree. `flag` requires owned repair routes; `block` cannot
unlock mutation.

**Conditional source-digest boundary:** source digests are not a violated obligation in the
current Distill prose (`arcanum/arcana/distill/SKILL.md`, lines 83-245). They are one
proposed mechanism for the new evidence design. Mutation-capable readiness nevertheless
requires exact immutable-content identity for every mutable reviewed artifact: recomputed
content digests are required unless another reference identifies the content exactly and
immutably. A mutable path or non-exact repository state is insufficient. Attack source:
Abramsky final **Changed View** and Ashby final **Stable Disagreement** (`attacks.md`, lines
93-100 and 290-294).

## 5. Invoke Mode Contracts

| Finding | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| `handoff` omits the root-required Dispatch trace and conditional Distill status/skip rationale from its required sections, gates, observability, and output. | `arcanum/spells/invoke/handoff.md` | Attack source: Ashby initial **Finding 4** and final **Surviving Finding 4** (`attacks.md`, lines 214-216 and 261-262); Shannon final **Changed From Initial View** (`attacks.md`, lines 328-332). Target: required sections and gates at lines 95-122, observability at lines 134-147, output at lines 149-170. Root obligations are `arcanum/spells/invoke/README.md`, lines 117-144 and 223-231. | MAJOR | Add mode-local Dispatch trace, conditional Distill trigger/skip rationale, execution-evidence reference when run, and pass-blocking gates. |
| `refresh` likewise omits root-required Dispatch and conditional Distill fields while allowing pass/flag/no-op outputs. | `arcanum/spells/invoke/refresh.md` | Attack source: Ashby initial **Finding 4** and final **Surviving Finding 4** (`attacks.md`, lines 214-216 and 261-262); Shannon final **Surviving Findings 3** (`attacks.md`, lines 348-349). Target: result object at lines 120-130, gates at lines 133-145, observability at lines 165-178, output at lines 180-204. Root obligations are `arcanum/spells/invoke/README.md`, lines 117-144 and 223-231. | MAJOR | Add the same mode-local fields and gates; preserve `not required` only with a bounded reason. |
| Root governance presents `full` and `validate` as automatic-Distill participants although both mode files are deferred and have only future output contracts. | `arcanum/spells/invoke/full.md`; `arcanum/spells/invoke/validate.md` | Attack source: Ashby initial **Finding 5** and final **Surviving Finding 5** (`attacks.md`, lines 218-220 and 264-265); Abramsky final **Highest-Severity Findings** (`attacks.md`, lines 102-111). Target: deferred status and activation gates at `full.md`, lines 1-27, and `validate.md`, lines 1-27; root mandatory wording at `README.md`, lines 134-142 and 223-231. | MAJOR | Add an explicit mode capability table. Deferred modes must return `unsupported/deferred` before lifecycle processing; implementing them is separate work. |
| `define` and `design` state when Distill applies, but their outputs preserve status/rationale rather than validated execution evidence. | `arcanum/spells/invoke/define.md`; `arcanum/spells/invoke/design.md` | Attack source: Shannon initial **Finding 3** and final **Surviving Findings 3** (`attacks.md`, lines 314-318 and 348-349). Target: `define.md`, lines 56-79; `design.md`, lines 115-140 and 185-189. | MAJOR | Project the common execution-evidence and execution-path fields into each mode. Keep `not applicable` only for the explicitly bounded applicability case with reason. |

**Verdict: FIX.** Add one mode capability table with
`implementation_status`, `dispatch_trace: required|conditional|unavailable`,
`distill: required|conditional|unavailable`, and `mutation_handoff_allowed`. A validator
must not infer obligations absent from a mode contract.

## 6. Anti-Bias Placement

| Finding | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| The anti-bias contract is internally bounded to subject groups with `n >= 2` in investigate/evaluate roles; it does not govern a single synthesizer/auditor or automatically govern local Proposer/Balancer simulation. | `.claude/skills/anti-bias-vector-composition/SKILL.md` | Attack source: Abramsky initial **Surviving Targets**, final **Rejected Claims** (`attacks.md`, lines 84-89 and 169-176); Ashby initial **Finding 6** and final **Rejected Claims** (`attacks.md`, lines 222-224 and 243-248); Shannon final **Rejected** (`attacks.md`, lines 334-338). Target: declared scope at lines 27-37. | N/A (KEEP) | Keep bounded placement. Apply anti-bias/check-tension only when Invoke creates a qualifying governed multi-agent investigate/evaluate group. Enforce Distill role opposition and trace universally without importing dispatch anti-bias vocabulary into local simulation. |

**Verdict: KEEP.** Blanket anti-bias enforcement is rejected as an overreach.

## 7. Workbench UI V1 Status And Replay Route

| Finding | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| Workbench is a concrete false-pass witness at the enforcement layer: it declares pass through a check table, repeats the verdict, and routes to Task Session without preserving role path, rounds, categorized objections, technique trace, or contract-complete execution evidence. | `projects/ide-extension/development/workbench-ui-v1/DISTILL-VALIDATION.md`; `projects/ide-extension/development/workbench-ui-v1/INVOKE-RESULT.md` | Attack source: Abramsky initial **F1/F3** and final **Highest-Severity Findings** (`attacks.md`, lines 15-70 and 102-111); Ashby final **Changed Position** and **Surviving Finding 3** (`attacks.md`, lines 237-241 and 258-259); Shannon initial **Finding 2** (`attacks.md`, lines 307-312). Target: validation assertion/table at `DISTILL-VALIDATION.md`, lines 1-20; repeated pass and Task Session route at `INVOKE-RESULT.md`, lines 1-20. | CRITICAL | Mark the preserved Distill status `unverified` for governance purposes and block mutation-capable handoff until replay succeeds through the new validator. Do not infer that the repaired SWUs are wrong. |
| Observability records five SWUs while the current repaired work-pack contains eleven; without immutable input binding, the historical record cannot identify the current package. This does not prove the historical count was false when emitted. | `.arcanum/observability/runs/invoke-20260717T080501Z-workbench-ui-v1.json`; `projects/ide-extension/development/workbench-ui-v1/WORK-PACK.md` | Attack source: Abramsky initial **F3** (`attacks.md`, lines 57-70); Shannon final **Surviving Finding 2** (`attacks.md`, lines 345-346). Target: historical verdict/count/route at JSON lines 33-41; current repaired manifest at `WORK-PACK.md`, lines 47-61. | CRITICAL | Preserve the run as historical evidence. Replay, recompute counts, and append a superseding evidence record bound to the repaired work-pack by exact immutable-content identity. |

**Verdict: FIX** for the claimed status and handoff eligibility, not for the substantive
eleven-SWU decomposition. Replay route: Invoke `plan` enforcement -> Distill `Validate` over
the repaired plan/layering/work-pack/handoff/gaps -> semantic/provenance validator -> only
then `task-session` on `SWU-WUI-001` if the validated verdict permits it.

## 8. Generated Mirrors And Ownership

| Finding | File | Evidence | Severity | Proposed fix |
| --- | --- | --- | --- | --- |
| No attacker found canonical/generated drift as the cause; synchronized mirrors share the same under-enforced contract. | `.agents/skills/invoke/SKILL.md` and generated per-mode Invoke files | Attack source: Abramsky initial **Surviving Targets** and final **Rejected Claims** (`attacks.md`, lines 84-89 and 169-176); Ashby initial **Defended Zero-Findings** and final **Rejected Claims** (`attacks.md`, lines 226-231 and 243-248); Shannon initial **Defended Zero Findings** (`attacks.md`, lines 320-324). Target: generated ownership metadata at `.agents/skills/invoke/SKILL.md`, lines 1-8; canonical obligations at `arcanum/spells/invoke/README.md`, lines 117-144. | N/A (KEEP) | Keep canonical ownership in public `arcanum/`; regenerate mirrors after accepted canonical/runtime changes. Do not place private DomainSpec or Saturn prose in public artifacts. |

**Verdict: KEEP.** Mirror fidelity is not the failure source.

## Ordered Change Requests

1. **CRITICAL - Gate mutation on executable proof.** Require contract-complete,
   validator-checkable execution evidence. Select the concrete schema through lifecycle
   acceptance; the recommended design is a versioned receipt backed by runtime-owned
   append-only events for both execution paths. Invoke pass/flag may route onward only from
   the validator result.
2. **CRITICAL - Kill fixture gaming.** Add one valid positive evidence fixture, one
   missing-evidence negative fixture, and one schema-complete fabricated-evidence fixture
   with unresolved/same role IDs, missing runtime events, invalid immutable-content binding,
   or cross-artifact mismatch. All invalid cases must block.
3. **CRITICAL - Replay Workbench.** Treat the current Distill pass as unverified, preserve
   the historical record, replay the repaired eleven-SWU package through Invoke plan plus
   Distill Validate, and emit a superseding exact-content-bound evidence record in the
   accepted design before Task Session routing.
4. **MAJOR - Compose mode contracts.** Add execution-evidence/path fields to `define`,
   `design`, and `plan`; add Dispatch plus conditional-Distill fields/gates to `handoff`
   and `refresh`.
5. **MAJOR - Fail closed for deferred modes.** Add a mode capability table and return
   `unsupported/deferred` for `full` and `validate` before lifecycle processing. Their
   implementation remains out of scope.
6. **MAJOR - Preserve bounded governance.** Retain true subagents when supported and
   labeled role simulation only when unavailable; do not claim current law requires a
   recorded unavailability proof. In the proposed enforcement design, event-back both paths
   and add a capability probe. Apply anti-bias/check-tension only to qualifying governed
   subject groups.
7. **MAJOR - Regenerate public mirrors.** After canonical changes are accepted, regenerate
   and validate installed Invoke/Distill surfaces without importing private authority prose.

## Preserved Disagreement And Rejected Claims

- **Historical runtime availability remains unsettled.** The dispatch context declares
  support, but no Workbench runtime receipt proves availability or use. Candidate language
  is “contract-complete execution unproven” and “execution path unknown,” never “Distill
  definitely did not run.” Attack source: Abramsky final **Stable Disagreement** and
  Shannon final **Stable Disagreement** (`attacks.md`, lines 178-180 and 386-388); target:
  `telemetry/agents/subagents-dispatch.yaml`, lines 3456-3468, versus the receipt's absent
  role evidence at `.arcanum/observability/runs/invoke-20260717T080501Z-workbench-ui-v1.json`,
  lines 1-41.
- **Source digests remain conditional.** They strengthen immutable source binding but are
  not a current Distill obligation. In the proposed enforcement, use recomputed digests for
  mutable reviewed artifacts unless another reference identifies exact immutable content;
  paths or non-exact repository state are insufficient for mutation readiness. Attack
  source: Abramsky final **Changed View** and Ashby final **Stable Disagreement**
  (`attacks.md`, lines 93-100 and 290-294); target:
  `arcanum/arcana/distill/SKILL.md`, lines 83-245.
- **Rejected:** receipt schema alone proves execution; true subagents are universally
  mandatory; blanket anti-bias applies to every Distill role pair; Workbench's repaired
  decomposition is substantively disproved; mirror drift caused the defect; implementing
  deferred `full`/`validate` belongs in this remediation.

## Verifier Reconciliation

| Verifier refutation | Disposition in this revision |
| --- | --- |
| Rittel: CR1 incorrectly made a versioned JSON receipt/runtime-owned index mandatory architecture. | **Accepted.** Current law now requires contract-complete, validator-checkable evidence. A versioned receipt plus runtime event ledger is labeled a recommended design requiring lifecycle acceptance, not a pre-existing mandate. |
| Rittel: CR6 incorrectly made recorded runtime unavailability a current Distill obligation. | **Accepted.** The current boundary remains true-subagents-when-supported and labeled fallback when unavailable. A capability probe is labeled a proposed enforcement strengthening only. |
| Schön: the candidate architecture could accept fabricated `role-simulation` fields because runtime resolution covered only true subagents. | **Accepted.** The recommended design now requires runtime-owned append-only events for both paths, including ordered simulated-role boundaries, transcript/output digests, parent linkage, and validator recomputation. Labeled fallback fields alone are explicitly insufficient. |
| Schön: conditional digests plus mutable paths/non-exact revision state cannot safely identify mutation-unlocking inputs. | **Accepted with the preserved contract distinction.** Digests remain a proposed mechanism rather than current Distill law, but every mutable reviewed artifact must have recomputed digests or another exact immutable-content identity before mutation-capable readiness. |
| Schön: “stale five-versus-eleven identity” implied the historical count was false. | **Accepted and narrowed.** The five-SWU record is preserved as historical evidence; absent immutable binding, it cannot identify the current eleven-SWU package. Replay appends a superseding exact-content-bound record and recomputes counts. |

## Final Approval

**ACCEPT.** The final independent auditor found coverage for the root cause, Distill
role/runtime policy, fixture exploit, mode parity, Workbench status, bounded anti-bias
placement, and verifier objections.

Rittel's remaining dissent controls the stronger provenance wording: exact immutable-content
identity is mandatory only as a condition of the proposed enforcement architecture after
lifecycle acceptance. It is not existing Distill law or a presently binding
contract-derived obligation. Before lifecycle acceptance, the requirement is reviewed-input
provenance sufficient for the validator design that is accepted.

No private DomainSpec or Saturn prose is proposed for public Arcanum surfaces.
