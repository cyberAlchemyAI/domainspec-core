# Pre-Task-Session Readiness Gap — Explorer Returns

## Agent 1 — Hewitt, Carl

### Finding

The August 3 route exposed a producer-side readiness false positive that was safely contained by the consumer preflight.

Invoke Plan described `WP-AUG-CANVAS-001` as “complete and executable in shape,” claimed its Work Pack contained a Task Session closeout contract, and presented `task-session → SWU-CANVAS-001`. The current Invoke Plan and Work Pack template, however, require a complete closeout-sync row before mutation-capable handoff. The produced Work Pack contains only generic Task Session admission/reporting instructions; it omits the exact synchronization inventory, baselines, allowed delta classes, owner validation, expected Invoke receipt, and deterministic successor contract.

`SWU-CANVAS-001` also declares material writes. That made its material-bound profile knowable during planning, but no Invoke-owned `materialPackage`, `materialReceipt`, or `producerReceiptSchema` existed. The Until Blocker preflight detected both omissions, validated the resulting request as schema-invalid, and stopped before Task Session or product mutation.

This independently re-verifies the Inventory lead against current sources: deterministic omissions were required to block before Task Session. Inventory itself supplies no authority for this conclusion.

### Timestamped owner-hop chronology

Times below are UTC. The first two use exact filesystem birth timestamps because those Markdown artifacts contain no embedded creation time; subsequent chain times are artifact timestamps or embedded chain fields.

1. **17:38:08.800Z — Invoke Plan producer.** `stages/09-plan.md` and `WORK-PACK.md` were created. Stage 09 claimed the Work Pack contained “Task Session closeout contract,” called the plan “complete and executable in shape,” and exposed `task-session → WP-AUG-CANVAS-001 / SWU-CANVAS-001` (`stages/09-plan.md`, `## Plan artifacts`, `## Admission ceiling`, `## Next route`). The Work Pack marked the package “ready for owner admission” and named one future Task Session per SWU (`WORK-PACK.md`, header fields).

2. **17:39:08.618Z — Refine synthesis/user-facing route.** `RESULT.md` repeated: “Explicitly admit task-session” for SWU-001, while noting implementation remained outside Refine (`RESULT.md`, `## Recommended next route`).

3. **17:50:06Z — Task Session Until Blocker owner.** The direct user invocation created chain `20260803T175006Z-augmentor-canvas`, captured all seven SWUs, selected SWU-001, set budget 7, and began with zero sessions (`chain.json`, `/created_at`, `/captured_frontier`, `/sessions_used`).

4. **17:51:21.181Z — Context/preflight owner.** The strict context pack bound live hashes, classified O5 and O6 as blocked, and identified:
   - incomplete closeout-sync contract;
   - absent material package, material receipt, and producer receipt schema.
   (`context-pack.md`, `## Blocking gaps`; `context-pack.json`, `/obligations/4`, `/obligations/5`.)

5. **17:51:54.019Z — Mutation-admission request construction.** The request declared three material-write paths plus one generated execution output but omitted `/materialPackage`, `/materialReceipt`, and `/producerReceiptSchema` (`mutation-admission-request.json`, `/materialWrites`, `/executionOutputs`).

6. **17:52:00.919Z — Task Session schema verifier.** The verifier returned `admissionVerdict=block`, `mutationReady=false`, `writeProfile=invalid`; all three material digests were null and the reason recorded root-schema failure (`mutation-admission-receipt.json`, `/admissionVerdict`, `/materialPackageDigest`, `/materialReceiptDigest`, `/producerSchemaDigest`, `/reasons/0`).

7. **17:52:14Z embedded chain update — Until Blocker terminal decision.** Preflight recorded `block-missing-exact-owner-sync-contract` and `block-missing-invoke-material-handoff`, with stop reason `preflight-block-before-first-task-session-and-before-product-mutation` (`chain.json`, `/preflight`, `/stop_reason`).

8. **17:53:31.364Z — Continuation Router.** It selected one proposal-only `invoke:refresh` candidate to author the missing artifacts, but `/dispatch/status` remained `not-requested`; no owner hop executed (`continuation-route.json`, `/selection`, `/dispatch`, `/returned_next_route`).

9. **17:54:50.187Z — Chain result publication.** The result reported ordered selectors invoked: none; Task Session receipts: none; product files changed: none; all seven SWUs remained (`chain RESULT.md`, lines 8–17).

### Requirement matrix

| Requirement | Producer promise | Exact missing artifact or field | First knowable | First detected | User-visible route presented | Safety effect | Exact selector |
|---|---|---|---|---|---|---|---|
| Complete closeout-sync contract for every mutation-capable SWU | Stage 09 said `WORK-PACK.md` contained a “Task Session closeout contract” and was executable in shape | Missing `closeoutSyncStatus` and per-SWU lifecycle route, terminal source receipt contract, declared target inventory, baseline binding, allowed delta classes, owner validation, expected owner receipt, and deterministic successor policy | Invoke Plan/Work Pack production: the current Plan contract makes these handoff-blocking inputs | Until Blocker strict preflight, O5/B1 | `task-session → WP-AUG-CANVAS-001 / SWU-CANVAS-001` | Blocked before implementation and routed proposal-only to Invoke Refresh | `.agents/skills/invoke/plan.md#Purpose` lines 25–30; `#Mode Gates` lines 314–317; `.agents/skills/invoke/templates/work-pack.md#Task Session Closeout Sync Contract` lines 60–75; actual `WORK-PACK.md#Task Session admission and closeout contract` lines 152–176; `context-pack.md#B1 — closeout synchronization contract` |
| Material-bound routed-mutation evidence | Work Pack marked SWU-001 ready-first, declared material writes, and Stage 09 recommended Task Session | `/materialPackage`, `/materialReceipt`, `/producerReceiptSchema`; corresponding receipt digests are null | Invoke Plan/handoff preparation, once SWU-001’s nonempty material-write set was authored | Context preflight O6/B2; concretely confirmed by the schema verifier | Same Task Session route | `admissionVerdict=block`; no mutation could cross the gate | `WORK-PACK.md#SWU-CANVAS-001` lines 36–50; `.agents/skills/task-session/SKILL.md#Step 5A` lines 232–254; mutation request schema `/allOf/0/then/oneOf/0/required`; request root; receipt `/reasons/0` |
| Preflight closeout completeness before first session | The route implied the first Task Session was the next owner | No admissible first-session envelope because both closeout and material prerequisites were absent | At Stage 09 handoff: Until Blocker requires every candidate’s complete closeout contract before mutation | Chain preflight | Refine result told the user to explicitly admit Task Session | The outer spell stopped without invoking its Phase 3 “Run One Fresh Task Session” | `.agents/skills/task-session-until-blocker/SKILL.md#Preconditions` lines 75–88 and `#Preflight The Frontier` lines 146–150; `chain.json#/preflight` |

### Did any Task Session start?

No.

The mutually reinforcing receipts are:

- `chain.json#/sessions_used = 0`
- `chain.json#/visited_selectors = []`
- `chain.json#/joined_task_session_receipts = []`
- `chain.json#/effects/task_sessions_started = 0`
- `chain.json#/effects/product_files_changed = []`
- `chain.json#/stop_reason = "preflight-block-before-first-task-session-and-before-product-mutation"`
- chain `RESULT.md`: “Ordered selectors invoked: none” and “Task Session receipts: none.”

The persisted mutation-admission request and receipt are outer preflight evidence, not evidence that a Task Session began.

```json
{
  "action_id": "spawn-0001",
  "dispatch_id": "2026-08-03-pre-task-session-readiness-gap-research-orchestration",
  "run_id": "pre-task-readiness-20260803T183017Z",
  "wave_id": "explorers",
  "step_id": "s1-explore",
  "role": "explorer-incident",
  "capability_ref": "research",
  "status": "pass",
  "artifacts": [],
  "validation": "pass",
  "blockers": [],
  "started_at": "2026-08-03T18:32:25.732550572Z",
  "finished_at": "2026-08-03T18:36:47Z",
  "residue": [
    "Stage 09 and Refine timestamps are filesystem birth metadata because their Markdown bodies contain no embedded timestamps",
    "No implementation, repair, owner dispatch, or lifecycle synchronization was performed"
  ],
  "reroute": "synthesizer",
  "handoff_note": "Use the exact current-source selectors above to distinguish the producer-side false-positive handoff from the consumer-side fail-closed containment; preserve the proof that zero Task Sessions started."
}
```

## Agent 2 — Beer, Stafford

### Adoption archaeology result

The accepted design existed, and its central WPRA/approved-epoch mechanisms were implemented and mirrored, but they were not activated on the normal Invoke → Refine → route-presentation path. The August 3 run therefore evaluated Stage 09 as a plan-shape success and recommended Task Session without producing or consuming a WPRA v2 verdict. The later Task Session Until Blocker preflight independently found the omissions and stopped safely before any Task Session or product mutation.

One correction to the dispatch premise: current Invoke Plan explicitly requires the complete closeout synchronization contract, but its Plan contract/template do **not** require the WPRA material tuple—package, producer owner, producer receipt, schema, inventory, and digest. Those material requirements currently live in accepted research, WPRA v2, and Invoke’s separate runtime-readiness resolver. That ownership split is itself part of the adoption gap.

| Proposed invariant | Owner | Implemented artifact | Validating fixture | Actual caller / consumer | Activation | August 3 evidence | Gap class |
|---|---|---|---|---|---|---|---|
| Deterministic owner, material, receipt, closeout, and successor omissions must block before any Task Session request. | Invoke Plan authors; exact producer supplies material; WPRA verifies. | WPRA v2 `_v2_preflight_blockers()` and `audit_v2()` return stable blockers and no manifest (`arcanum/spells/work-pack-readiness-audit/scripts/audit_work_pack.py:1156-1286,1433-1618`). | Synthetic deterministic projection plus ten single-fault negatives (`development/test_work_pack_readiness_v2.py:247-342`). | CLI/manual consumers and the July 30 private prototype; no normal Invoke or Refine caller. | Implemented candidate; not mandatory. | Stage 09 recommended Task Session (`stages/09-plan.md:33-43`) while the Augmentor run contains no `audit-config-v2`, report, or manifest. | `implemented-not-invoked`, `missing-route-edge` |
| Exact per-SWU material must bind package, producer owner, producer receipt, schema, target inventory, baseline, and digest. | Exact `producerOwnerRef`; WPRA verifies; Invoke owns its runtime handoff contract. | WPRA stable material codes (`audit_work_pack.py:1161-1245`); Invoke resolver requires a valid material receipt plus runtime receipt (`arcanum/spells/invoke/scripts/capability_status_resolver.py:140-185`). | WPRA `WPA2-F02..11`; Invoke capability resolver material/runtime-axis tests (`test_capability_status_resolver.py:120-228`). | Optional explicit resolver/WPRA requests only. No Refine Stage 09 call. | Validator machinery active; producer integration absent from Plan. | Mutation admission records `materialPackageDigest:null`, `materialReceiptDigest:null`, `producerSchemaDigest:null` and `mutationReady:false` (`.../mutation-admission-receipt.json:21-34`). | `owner-ambiguity`, `prose-absent-from-plan`, `implemented-not-consumed` |
| Every mutation-capable SWU has exact closeout inventory, baselines, admitted deltas, owner validation, expected owner receipt, and successor. | Invoke Plan / canonical `WORK-PACK.md`. | Plan mode gate (`arcanum/spells/invoke/plan.md:25-30,169-171,314-317`) and template (`templates/work-pack.md:60-75,192-194`). WPRA checks baseline, delta policy, closeout receipt contract, and unique successor. | WPRA closeout/baseline/successor negatives (`test_work_pack_readiness_v2.py:299-325`). | August 3 Stage 09 used authored prose and Distill shape review, not a machine closeout validator. | Prose contract present; enforcement absent at Plan exit. | Work Pack’s “closeout contract” only specifies Task Session start/terminal evidence (`WORK-PACK.md:152-176`), omitting exact Invoke Refresh targets/owner receipt; nevertheless Stage 09 passed. Outer preflight later reports `block-missing-exact-owner-sync-contract` (`chain.json:48-57`). | `prose-not-validated`, `false-positive-plan-handoff` |
| Authored Plan status must remain separate from mutation runtime readiness. | Invoke capability-status resolver. | Three-axis contract and resolver (`arcanum/spells/invoke/README.md:46-70`; `plan.md:414-422`). | All active modes prove artifact-only does not open later axes (`test_capability_status_resolver.py:120-143`). | Only callers that explicitly request capability status. | Implemented, optional. | Refine recorded `Invoke Plan: pass` and directly recommended Task Session (`RESULT.md:23-34,71-76`); no capability-status request/result exists in the run. | `implemented-not-invoked`, `status-consumer-missing` |
| A passing WPRA projection remains authority-none, unselected, mutation-not-ready, and unapproved until Decision Gate/human approval. | WPRA, then Decision Gate/human. | WPRA v2 projection (`README.md:273-306`; `audit_work_pack.py:1523-1618`). | Determinism/no-command test (`test_work_pack_readiness_v2.py:247-270`). | Approved-epoch chain runner can consume it. | Implemented candidate. | No Augmentor manifest or approval-bound chain config exists. | `missing-route-edge` |
| Task Session Until Blocker exposes one selector only from an exact approved epoch and valid manifest. | Task Session Until Blocker. | `run_chain.py` verifies exact manifest/approval, epoch digests, frontier, budget, and risk before returning a selector (`arcanum/spells/task-session-until-blocker/scripts/run_chain.py:106-183,205-248`). | Approved-epoch chain suite (`development/validate-chain-v2.py:196-330`). | Explicit approved-epoch CLI configuration. It never launches Task Session itself. | Candidate runtime available and generated; not used by this Augmentor chain. | The August 3 chain directory has neither `chain-config.json` nor an objective-execution manifest. It used the broader skill preflight instead. | `implemented-not-invoked` |
| Refine Stage 09 must consume a machine readiness verdict before final synthesis may recommend Task Session. | Proposed: Invoke via Spellcraft produces; Refine/router consumes. | **Not implemented.** Refine’s Stage 09 template consumes only `repair-frame`, emits a plan artifact, and has no WPRA gate (`arcanum/arcana/refine/templates/refine-dispatch.json:258-267,281-323`). | None for readiness. Existing checks validate dispatch shape, native receipt presence, and artifact existence. | Refine final synthesis consumes Stage 09 prose. | Absent. | August 3 dispatch Stage 09 stops only for product mutation or missing validation commands and then records pass/recommends Task Session (`REFINE-DISPATCH.json:337-339`; native receipt at lines 214-215). | `missing-route-edge`, `prose-not-validated` |
| Downstream containment must remain fail-closed even after an upstream false-positive. | Context Builder, routed-mutation admission, Task Session Until Blocker, Task Session. | Existing strict context and mutation-admission gates. | Existing Task Session and chain suites. | August 3 outer preflight. | Active and effective. | `sessions_used:0`, no joined Task Session receipts, no changed product files; block occurred before first Task Session (`chain.json:24-29,65-75,105-110`). | `correct-downstream-enforcement`, not a defect |

Generated-package inspection does not reveal a stale-copy explanation. WPRA and chain runners are byte-identical across canonical, Codex, and Claude packages; Invoke Plan/template are also byte-identical. Refine’s dispatch template is semantically identical across profiles. A targeted search found no WPRA, `audit-config-v2`, or objective-manifest consumption edge in canonical or generated Invoke/Refine packages. The missing behavior is wiring, not mirror drift.

Why the prior accepted work did not prevent the run:

1. The July 22 review was accepted as a change request only; it explicitly changed no audited skill (`ops/development/2026-07-22-most-used-skills-efficiency-review/findings.md:1-7,74-87`).
2. The July 23 lifecycle work was explicitly `CANDIDATE`, with no post-repair live proof, and said its requests were not claims that Arcanum had changed (`ops/development/2026-07-23-invoke-lifecycle-churn-research/findings.md:7-20,192-199`).
3. The July 30 research audit accepted only `frozen-input-contractual-readiness`, not implementation (`ops/development/2026-07-30-invoke-one-shot-workflow-research/receipts/audit.json:1-19`). Its WPRA and approved-chain verdicts remained conditional and fixtures were proposed/unexecuted at research close (`findings.md:321-347,701-727`).
4. The subsequent implementation was deliberately candidate-local. Its report says normal lifecycle synchronization, real Task Session launch, and Invoke integration were not proven; its work pack explicitly forbade changes to `arcanum/spells/invoke/**` (`ops/development/2026-07-30-one-shot-admission-prototype/PROTOTYPE-VALIDATION.md:58-83`; `WORK-PACK.md:90-105`).
5. August 1 diagnosed the same false-positive and proposed `INVOKE-WPRA-001`, but approved change scope was `none`, accepted changes were empty, and canonical/generated files were unchanged (`ops/development/2026-08-01-task-session-execution-readiness-maintenance/MAINTENANCE-REPORT.md:10-28`; `MAINTENANCE-INVOCATION-ENVELOPE.json:75-87`).
6. Consequently, August 3 exercised the old route semantics: Stage 09 proved decomposition and plan shape, Refine treated the artifact receipt as sufficient for a next-route recommendation, and only the downstream preflight consumed the actual mutation-admission contract.

The evidence supports an adoption/wiring diagnosis, not a need for a new readiness capability and not an implementation claim.

---

`action_id=spawn-0002; dispatch_id=2026-08-03-pre-task-session-readiness-gap-research-orchestration; run_id=pre-task-readiness-20260803T183017Z; wave_id=explorers; step_id=s1-explore; role=explorer-adoption; capability_ref=research; status=pass; artifacts=[]; validation=pass; blockers=[]; started_at=2026-08-03T18:30:17Z; finished_at=2026-08-03T18:38:23Z; residue=["no Augmentor WPRA positive or single-fault fixture","Invoke material producer ownership is not expressed in Plan template","normal Refine-to-WPRA admission edge remains absent"]; reroute=synthesizer; handoff_note="Use this matrix to separate implemented candidate controls from absent normal-path consumption; preserve the downstream block and do not claim implementation."`
