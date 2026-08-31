---
module: invoke-preacceptance-governance-defect
version: draft-3
status: proposal-only
updatedAt: 2026-08-26
docType: work-pack
---

# WORK-PACK: Invoke Preacceptance Governance Defect

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| planAuthoringStatus | pass | The repair boundary and validation plan are complete enough for lifecycle-owner review. |
| workPackGateStatus | block | W0 is frozen, but canonical mutation remains unadmitted until the isolated candidate is complete, validated, independently reviewed, and exactly accepted. |
| complexity | medium | Multiple authority-bearing schemas, validators, fixtures, and generated projections are affected. |
| outputMode | split | Layering, execution, validation, and Distill artifacts are separate. |
| executionPackRef | `EXECUTION-PACK.md` | Ordered waves and stop gates. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0-L3 decisions. |
| distillValidationStatus | pass | Seven units recompose and W0 selected a fail-closed parallel-v2 encoding. |
| swuAtomicityStatus | pass | Each SWU owns one primary behavior; verification is a closure task. |
| firstUnitNarrownessStatus | pass | SWU-IGD-001 repairs only staged-candidate representation and authority semantics. |
| executionDesignation | execution-candidate | Draft only; it is not readiness-proven or accepted. |
| implementationReadinessStatus | block | WPRA/Implementation Readiness were not run and Task Session is not the next route. |
| exactAcceptanceStatus | unapproved | A later request must bind the final repaired bytes and fresh executable digests. |
| mutationReady | false | This plan grants no source mutation authority. |
| nextRoute | `spellcraft:update -> spellcraft:validate` | Spellcraft owns Invoke spell revision. |

## Objective Summary

- Objective: make Invoke preacceptance truthfully represent and validate an exact,
  nonempty candidate before one exact owner request is emitted.
- Success condition: a synthetic candidate crosses
  `proposal -> staged -> closure -> independent review -> request emission` with no
  authority effect, while every declared negative case blocks at the correct edge.
- Non-goal: make Body War Work Packs executable. Their WPRA and Implementation
  Readiness gaps remain separate.

## Root Causes In Scope

| ID | Defect | Current consequence |
| --- | --- | --- |
| IGD-STATE-001 | The material-package schema couples nonempty material to `apply-approved` and `explicit-apply`. | A truthful staged candidate cannot enter the standard validator. |
| IGD-CONTENT-001 | Final postimages are unconditionally parsed as JSON and assertions expose only JSON Pointer. | Markdown and YAML candidates are `not_evaluable`. |
| IGD-EFFECT-001 | Request emission embeds the base request without comparing its requested effect to the frozen manifest effect. | A divergent owner-facing request can bypass the effect binding already proven by eligibility. |
| IGD-CONSUMER-001 | The integration fixture invokes several consumers with `--help`, and exit code zero is accepted as stage PASS. | Consumer availability can be mistaken for validation of the exact candidate. |
| IGD-BLOCKERSET-001 | Stage execution breaks after the first nonzero exit. | Reachable blockers are omitted and causal `not_evaluable` results are unavailable. |

## Candidate Contract Requirements And W0 Decision

W0 is frozen by `W0-COMPATIBILITY-DECISION.md`. The three legal rows are:

| Derived state | Material | Approval | Required receipt meaning | Authority |
| --- | --- | --- | --- | --- |
| proposal | empty | `none`; empty scope | v1 or v2 `not-applicable + deferred` | none |
| staged candidate | nonempty exact candidate | `none`; empty scope | v2 `candidate-pass + gated` | none |
| apply-authorized material | nonempty exact candidate | exact `explicit-apply` | v1 or v2 `pass + ready` | bounded by the separate approval |

The staged row uses `mutation_mode=proposal-only` and `mutation_state=staged` in a
parallel v2 package schema. It does not add a run-level mode. Existing v1 schema IDs,
filenames, packages, receipts, and CLI behavior remain unchanged. The v2 receipt
schema closes verdict/handoff pairings, so `candidate-pass + ready`, `pass + gated`,
and arbitrary cross-pairings are invalid. The generic verdict-only prerequisite
reader cannot mistake `candidate-pass` for approved material.

For postimages, add an explicit `content_kind` discriminator with a closed minimum
assertion union:

- `json`: JSON Pointer with `equals`, `not_equals`, or `absent`;
- `utf8-text`: literal `equals`, `contains`, or `not_contains`.

No type is inferred from an extension. Digest/size checks remain universal. Invalid
encoding, unknown content kind, or an incompatible assertion operator blocks. A YAML
path can be declared `utf8-text` and checked literally. Structural `yaml` is added
only if Spellcraft pins the parser owner and exact version, requires safe loading,
rejects custom tags and non-JSON-compatible values, and adds dependency-absence
fixtures; otherwise it remains deferred.

Request emission must require `base_request.requested_effect` and prove exact
structural equality and canonical-digest equality with
`manifest.requested_effect`. No new duplicate effect field is needed in the emitted
request.

## Smallest Working Unit Manifest

| SWU | Parent | Primary behavior | Dependencies | Independently reviewable acceptance boundary | Status |
| --- | --- | --- | --- | --- | --- |
| SWU-IGD-001 | TASK-IGD-STATE | Represent a non-authorizing nonempty staged candidate. | Owner accepts the three-row state table and exact token/version encoding; live target bytes classified. | Candidate package validates with the accepted distinct non-authorizing outcome; existing proposal/apply meanings are unchanged; legacy and single-axis consumers fail closed. | implemented-candidate; targeted PASS |
| SWU-IGD-002 | TASK-IGD-CONTENT | Validate declared JSON and UTF-8 text postimage semantics, including YAML files declared as text. | SWU-IGD-001 contract stable. | One JSON/Markdown/YAML-file closure passes; wrong type/encoding/assertion/stale bytes block; structural YAML remains gated on a pinned parser contract. | implemented-candidate; targeted PASS |
| SWU-IGD-003 | TASK-IGD-EFFECT | Bind the base-request effect to the frozen manifest effect. | None beyond current request/manifest schemas. | Missing or divergent base effect blocks both emission and canonical revalidation. | implemented-candidate; targeted PASS |
| SWU-IGD-004 | TASK-IGD-STAGE-GRAPH | Collect every reachable stage result with causal `not_evaluable` and first-nonzero preservation. | Stage dependency contract accepted. | Independent later failures are retained; dependents are not executed or called PASS; later success cannot mask the first failure. | implemented-candidate; targeted PASS |
| SWU-IGD-005 | TASK-IGD-REAL-CONSUMER | Exercise the exact staged material package through the real validator. | SWU-IGD-001 and SWU-IGD-004. | Exact package/output/operation/baseline transition and receipt bind; `--help`, a different package, or exit-zero/no-receipt adapter blocks. | implemented-candidate; targeted PASS |
| SWU-IGD-006 | TASK-IGD-VERIFY | Prove the canonical full-lifecycle regression without generated-package mutation. | SWU-IGD-001 through SWU-IGD-005. | Synthetic full chain passes twice deterministically and every negative fixture blocks on canonical bytes. | validation-in-progress |
| SWU-IGD-007 | TASK-IGD-PACKAGE | Synchronize generated Invoke packages and prove canonical parity. | SWU-IGD-006 and exact owner authorization for generated targets. | Canonical sync changes only declared generated targets; generated suites and exact parity pass. | gated on SWU-IGD-006 and exact acceptance |

## SWU Atomicity Review

| SWU | Candidate child units | Why retained | Verdict |
| --- | --- | --- | --- |
| SWU-IGD-001 | schema condition; validator branch; receipt fixture | Separating them would leave an accepted state with no truthful producer/consumer outcome. | pass |
| SWU-IGD-002 | JSON; UTF-8 text; structural YAML | JSON and literal text are the minimum dispatcher behavior; structural YAML is explicitly deferred unless its parser contract is owned and pinned. | pass |
| SWU-IGD-003 | schema-required field; emitter equality; validator replay | All three are one effect-binding invariant across emission and revalidation. | pass |
| SWU-IGD-004 | dependency model; scheduler; receipt state | A dependency graph without scheduler/receipt semantics cannot prove reachable closure. | pass |
| SWU-IGD-005 | package binding; transition/baseline binding; real invocation; receipt verification | Any split permits an exit-zero process, unrelated package, or contradictory filesystem transition to masquerade as the bound consumer. | pass |
| SWU-IGD-006 | positive lifecycle; negative lifecycle | Closure-only verification exemption; it changes no canonical or generated production behavior. | pass |
| SWU-IGD-007 | generated sync; generated validation; parity | These actions share one material packaging boundary and exact generated-target inventory. | pass |

## Frozen Candidate Write Scope

This is an inventory for Spellcraft preflight, not authority to edit:

- `arcanum/spells/invoke/schemas/material-package-v2.schema.json` (create)
- `arcanum/spells/invoke/schemas/material-package-receipt-v2.schema.json` (create)
- `arcanum/spells/invoke/schemas/refresh-material-handoff-result-v2.schema.json` (create if the result remains versioned)
- `arcanum/spells/invoke/scripts/material_package_validator.py`
- `arcanum/spells/invoke/scripts/refresh_material_handoff.py`
- `arcanum/spells/invoke/schemas/preacceptance-closure-manifest-v2.schema.json` (create)
- `arcanum/spells/invoke/schemas/preacceptance-closure-receipt-v2.schema.json` (create)
- `arcanum/spells/invoke/schemas/owner-acceptance-request-v3.schema.json` (create; the late strengthened v2 schema is adopted byte-exact as a baseline prerequisite, not rewritten by this candidate)
- `arcanum/spells/invoke/scripts/preacceptance_closure.py`
- `arcanum/spells/invoke/development/run_material_package_fixtures.py`
- `arcanum/spells/invoke/development/fixtures/material-package-cases.json`
- `arcanum/spells/invoke/development/fixtures/refresh-material-handoff-cases.json`
- `arcanum/spells/invoke/development/test_capability_status_resolver.py`
- one new Invoke-owned downstream no-collapse test
- `arcanum/spells/invoke/development/run-validation-fixtures.sh`
- `arcanum/spells/invoke/development/preacceptance-closure/test_preacceptance_closure.py`
- `arcanum/spells/invoke/development/preacceptance-closure/test_owner_request_requested_effect.py`
- `arcanum/spells/invoke/development/preacceptance-closure/test_execution_entry_negative_cases.py`
- `arcanum/spells/invoke/development/preacceptance-closure/fixtures/negative-cases.json`
- `arcanum/spells/invoke/development/preacceptance-closure/real_consumer_rehearsal.py`
- `arcanum/spells/invoke/development/run-preacceptance-closure-fixtures.sh`
- `arcanum/spells/invoke/preacceptance-closure.md`
- `arcanum/spells/invoke/refresh.md`
- `arcanum/spells/invoke/README.md`

Test-only downstream regression scope:

- `arcanum/arcana/task-session/development/test_live_execution_entry.py`
- `arcanum/arcana/task-session/development/run-validation-fixtures.sh`

These two Task Session development files keep the existing live-entry fixture bound
to the v3 owner-request graph and make that fixture reachable from its validation
wrapper. They do not change the Task Session runtime contract. Task Session generated
packages remain outside the repair target inventory.

Generated `.agents/skills/invoke/` and `.claude/skills/invoke/` paths are downstream
sync outputs, never primary edit targets.

The late live requested-effect regression is retained as an independently reachable
test and evolved from the v2 top-level representation to the v3 base-request,
manifest, digest, and canonical-replay binding. This adds one canonical test target;
it does not add a runtime or generated Task Session target.

## Task Session Closeout Sync

Task Session is intentionally not available from this draft. Before any later Task
Session handoff, Spellcraft must freeze exact paths and baselines, declare the
accepted delta classes, name the canonical validation commands, bind the expected
Spellcraft receipt, and set the successor policy to `none` until exact repaired bytes
are independently reviewed. Missing closeout bindings keep
`workPackGateStatus=block`.

## Blockers And Gates

| ID | Scope | Blocker | Owner | Resolution |
| --- | --- | --- | --- | --- |
| IGD-GATE-001 | baseline | Current canonical preacceptance files contain unattributed live changes. | Spellcraft lifecycle owner | Resolved for candidate authoring: adopt the exact W0 live-byte inventory in an isolated clone; never overwrite live bytes during construction. |
| IGD-GATE-002 | contract | The staged-candidate token/version encoding was open. | Spellcraft lifecycle owner | Resolved by the parallel-v2 `candidate-pass + gated` decision; content and stage contracts are frozen in this Work Pack. |
| IGD-GATE-003 | execution | No exact WPRA/Implementation Readiness proof or owner acceptance exists for repair bytes. | Invoke Plan/Decision Gate after Spellcraft candidate | Generate only from final byte-current candidate artifacts. |
| IGD-GATE-004 | resumption | The repair changes authority-bearing validators/runners. | Body War continuation owner | Regenerate tool refs, closure graph, review, and owner request; do not consume the prior resume token. |

## Dispatch Technique Trace

| Technique | Applied to | Validation expectation | Status |
| --- | --- | --- | --- |
| `sequence` | state -> content/effect -> stage graph -> real consumer -> closure | No unit claims evidence owned by a later wave. | pass |
| `scu_swu_reduction` | seven-unit manifest | Each unit owns one primary behavior and one acceptance boundary. | pass |
| `recomposition_proof` | complete preacceptance chain | Removing any unit reopens a known false block or false pass. | pass |
| `validation_loop` | `VALIDATION-MATRIX.md` | Every repair unit has positive and negative evidence. | pass |
| `owner_boundary_check` | Invoke Plan -> Spellcraft | Planning does not mutate or claim spell lifecycle completion. | pass |
| `handle_handoff` | private plan paths and canonical public targets | Spellcraft receives locators; private Body War content is not copied. | pass |
| `residue_ledger` | four gates above | Dirty-byte and renewed-acceptance residue stays visible. | pass |
| `authority_split_gate` | validation vs request vs acceptance vs apply | A candidate-valid receipt grants no apply, selection, or execution authority; parallel-v2 no-collapse controls preserve the split. | pass |

A full multi-agent dispatch is not required for this planning result: one bounded
read-only audit assisted the parent, one lifecycle owner is next, no execution graph
was started, and private evidence remains outside the public target. A future
multi-agent implementation route must be separately specified and accepted.

## Recomposition Proof

SWU-IGD-001 makes the candidate representable. SWU-IGD-002 makes its declared
document semantics evaluable. SWU-IGD-003 makes the owner-facing effect equal the
frozen effect. SWU-IGD-004 makes failure evidence complete. SWU-IGD-005 proves the
actual candidate and filesystem transition crossed the actual consumer. SWU-IGD-006
proves those guarantees compose through canonical request emission. SWU-IGD-007 then
packages the verified canonical result. No smaller subset closes the recorded defect
family without conflating verification and generated mutation.

## Claim Ceiling

This Work Pack proves only that a bounded repair is planned. It does not prove the
repair works, authorize canonical mutation, make Body War executable, or grant any
provider, personal-data, privacy, deployment, geometry, scoring, Git, publication,
release, or production authority.
