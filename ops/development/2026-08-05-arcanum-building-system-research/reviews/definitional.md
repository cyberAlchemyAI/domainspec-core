# Definitional-Soundness Review

`DEFINITIONAL_GATE: FAIL`

The synthesis generally recognizes the necessary owner boundaries, but it does not define them consistently enough to pass. Its most serious defects are:

1. Invoke phase status is not explicitly separated from the three capability axes.
2. The material producer and registry-release owner are not precisely bound.
3. “Selection,” “readiness,” and “completion” remain overloaded.
4. Inventory’s valid internal lookup proof is incorrectly flattened into “never proof.”
5. The attack ledger omits the newly observed action-ID collision defect.
6. Both orchestration corrections are run-local workarounds, not canonical repairs.

## Stable-ID audit

The synthesis declares 100 IDs across `SYS`, `OWN`, `GATE`, `LIN`, `CHG`, `TRACE`, `BUG`, `CRAFT`, `CAP`, `PLAY`, and `ATTACK`. Each occurs exactly once; no declared ID is duplicated.

The numbering is syntactically stable. Semantic stability is weaker because several IDs use overloaded nouns. Existing IDs should not be renumbered. The action-ID collision defect should be appended as `ATTACK-015`.

## Definition, owner, state, artifact, and evidence-ceiling matrix

| Attacked collapse | Precise definition and owner | Distinct states | Distinct artifacts | Evidence ceiling | Synthesis IDs | Verdict |
|---|---|---|---|---|---|---|
| Invoke phase status vs three-axis capability evidence | A mode run owns `phase_status`. The capability resolver separately evaluates `artifact_authored`, `registry_released`, and `mutation_runtime_ready`; the registry owner is not identified by the synthesis. | `phase_status=pass/flag/block/no-op`; authored axis `pass/flag/block/unsupported`; release/runtime axes boolean | Mode report; artifact receipt; registry-owner receipt; material-package receipt; mode-runtime receipt | A phase pass proves current mode-artifact completion only. Each capability receipt opens only its own axis. `arcanum/spells/invoke/README.md:46-70` | `SYS-001`, `OWN-003`, `GATE-002` | `repair` |
| Design vs Plan evidence | Design author, extractor, and selection validator own the Design manifest, denominator, fixed-point result, and Design evidence state. Invoke Plan owns runnable Plan evidence. | `authored-complete`; `design-validator-pass`; separately `plan-evidence-pending/pass/fail` | `DesignScopeManifest`; `DesignDenominatorReceipt`; `DesignSelectionResult`; Plan artifact/receipt | Design validation never proves Plan execution evidence. `design.md:104-140,160-173` | `SYS-001`, `OWN-002`, `GATE-001`, `LIN-001` | `repair` for the vague model/owner language; `sustain` for `GATE-001` and the lineage boundary |
| WPRA selection vs mutation authority | WPRA owns frozen audit/semantic-manifest evidence. The selection verifier emits a non-authoritative selected-unit receipt. Task Session owns live mutation admission. | audit `pass/flag/block`; semantic plan `pending-selection`; selected-unit verified; mutation `admit/block`; all WPRA artifacts retain `authority_effect:none` | Readiness report; semantic manifest; selection handoff; selected-unit receipt; mutation-admission receipt | Frozen contractual readiness and semantic selection only; no mutation authority. `work-pack-readiness-audit/README.md:194-210,290-340` | `SYS-002`, `OWN-005`, `GATE-005`, `LIN-002`, `BUG-001`, `BUG-002` | `sustain` boundaries; `repair` `OWN-005` by replacing “readiness/current selection” with the exact two artifacts and states |
| Material producer vs Task Session consumer validation | The material producer owns package construction, package validation, receipt, and receipt schema. Task Session owns consumer revalidation, live target hashing, binding, single-use consumption, and the only mutation-admission verdict. The synthesis does not name the concrete producer owner. | producer validation `pass/block`; consumer admission `admit/block/not-applicable`; post-write validation separate | Material package; producer receipt/schema; admission request/receipt; consumption ledger; execution ticket | Producer evidence proves package integrity only. Admission is execution evidence, not mutation, lifecycle, promotion, or publication authority. `task-session/SKILL.md:260-319` | `SYS-003`, `GATE-009`, `LIN-004`, `BUG-003`, `ATTACK-006` | `repair`; defer any compatibility claim until the exact producer and cross-owner fixture are bound |
| Task Session execution vs closeout synchronization | Task Session owns one-SWU execution evidence and the derived overall result. Invoke Refresh owns closeout mutation. Continuation Router dispatches and joins the owner receipt. | execution `pass/block`; closeout `pass/block/no-op`; overall Task Session is blocked when required closeout does not join | Execution ticket; execution-terminal receipt; `CloseoutSync`; closeout authorization; Refresh owner receipt; continuity cursor | Execution can be preserved after closeout failure, but does not prove synchronized Task Session completion. `task-session/SKILL.md:351-419` | `SYS-006`, `GATE-010`, `GATE-011`, `LIN-005`, `LIN-006`, `BUG-004`, `BUG-011`, `ATTACK-004` | `sustain` except `LIN-005`: `repair` “terminal Task Session receipt” to “execution-terminal receipt” |
| Continuation Router vs owner work | Router owns ranking, exact admission, bounded dispatch, join, and route receipt. The selected capability owns all semantic work and mutation. | route `not-authorized/ambiguous/admitted/block`; owner result remains separate | Source receipt; authorization/binding; route receipt; separate terminal owner receipt | Route/join evidence only. A route string is destination evidence, not mutation authority. `continuation-router/SKILL.md:118-170` | `SYS-004`, `OWN-010`, `CAP-004` | `sustain` |
| Craft ledger state vs Work Pack authority | Craft owns `.craft/ledger.yml` as source of truth only inside its selected ledger scope. Invoke Plan’s `WORK-PACK.md` owns the executable plan/current execution contract. Called capabilities retain native artifact and verdict ownership. | Craft structural validity/readiness/pending state; Work Pack task/SWU/gate state | `.craft/ledger.yml`; derived `CRAFT.md`/index; separate `WORK-PACK.md`; native receipts | Craft proves local ledger state/structure, not SWU selection, mutation admission, native success, or Work Pack authority. `craft/SKILL.md:56-72,277-317` | `SYS-005`, `OWN-012`, `LIN-008`, `CRAFT-001`, `CRAFT-002`, `CAP-011` | `sustain` |
| Inventory discovery vs proof | Inventory owns cards, indexes, lookup projections, lint, and handoff read models. Direct sources and downstream governance owners own semantic proof and promotion. | candidate/captured/index-current; downstream accepted/promoted remains separate | Evidence card/set; index; lookup projection; source reference; downstream owner artifact | Inventory can prove its own index/projection conformance and provenance, but not source truth, ontology/definition authority, lifecycle readiness, or promotion. `inventory/SKILL.md:247-285,335-339` | `BUG-010`, `CAP-012` | `repair`; “never proof” is overbroad |
| Execution evidence vs lifecycle promotion | Task Session owns execution/admission receipts. Sigil Development or Spellcraft owns reusable-capability lifecycle judgment. A separately bound registry owner must issue registry-release evidence. | execution passed; lifecycle evidence pending/reviewed; promotion readiness decision; registry released/not released; runtime ready/not ready | Task Session receipt; experiment/observer/reflection evidence; lifecycle-owner decision; registry-owner receipt; runtime receipt | Execution proves one admitted unit only. It cannot prove promotion readiness, registry release, publication, deployment, or production. | `OWN-014`, `CHG-005`, `PLAY-002`, `PLAY-003`, `ATTACK-014` | `repair` `OWN-014` to separate lifecycle judgment from registry release; sustain the remaining ceilings |

## Claim verdicts

| Exact IDs | Verdict | Reason |
|---|---|---|
| `SYS-001`, `OWN-002`, `OWN-003`, `GATE-002` | `repair` | Missing explicit phase-versus-axis state model; “mutation-handoff eligibility” is a collapsed label rejected by the Invoke contract. |
| `GATE-001`, `LIN-001` | `sustain` | Design and Plan evidence are correctly kept distinct. |
| `SYS-002`, `GATE-005`, `LIN-002`, `BUG-001`, `BUG-002` | `sustain` | Audit, selection, entry, and mutation remain distinguishable. |
| `OWN-005` | `repair` | Name frozen audit and non-authoritative selected-unit verification separately. |
| `SYS-003`, `LIN-004` | `repair` | Correct boundary, but the concrete producer owner/schema identity is missing. |
| `GATE-009` | `repair` | Sustain the contract, but scope `EXECUTED` to fixture/integration consumer evidence until cross-owner compatibility exists. |
| `BUG-003` | `sustain` | Correctly rejects producer/consumer collapse. |
| `SYS-006`, `GATE-010`, `GATE-011`, `LIN-006`, `BUG-004`, `BUG-011` | `sustain` | Correct two-stage execution/synchronization model. |
| `LIN-005` | `repair` | “Terminal Task Session receipt” is misleading before required synchronization. |
| `SYS-004`, `OWN-010`, `CAP-004` | `sustain` | Router and selected owner remain separate. |
| `SYS-005`, `OWN-012`, `LIN-008`, `CRAFT-001`, `CRAFT-002`, `CAP-011` | `sustain` | Craft’s authority is properly scoped to its local ledger. |
| `BUG-010`, `CAP-012` | `repair` | Preserve Inventory-native lookup/projection proof while denying downstream semantic authority. |
| `OWN-014` | `repair` | Lifecycle judgment and registry release are separate owners/evidence axes. |
| `CHG-005`, `PLAY-002`, `PLAY-003` | `sustain` | These do not claim promotion, provided lifecycle-owner decision is not relabeled registry release. |
| `LIN-007`, `GATE-012` | `repair` | Native lineage omits global action-ID uniqueness and exact receipt-directory admission. |
| `BUG-012`, `BUG-013` | `sustain` | Correctly place the first reducer failure on driver input scope, not explorer execution. |

## ATTACK ledger verdicts

| Attack ID | Verdict | Disposition |
|---|---|---|
| `ATTACK-001` | `sustain` | Generated WPRA parity remains blocked. |
| `ATTACK-002` | `sustain` | Generated Task Session/Continuation Router parity remains unproved. |
| `ATTACK-003` | `sustain` | Live-uncommitted evidence cannot be promoted to canonical/immutable proof. |
| `ATTACK-004` | `sustain` | Real product-through-owner-closeout E2E remains absent. |
| `ATTACK-005` | `sustain` | Distill criticality binding remains missing. |
| `ATTACK-006` | `sustain` | Producer/consumer compatibility remains untested and producer identity unbound. |
| `ATTACK-007` | `sustain` | Goal canonical owner binding remains absent. |
| `ATTACK-008` | `sustain` | Canonical/generated source identity remains ambiguous. |
| `ATTACK-009` | `sustain` | Deferred Craft schemas prohibit automated-loop claims. |
| `ATTACK-010` | `sustain` | Event-contract tests are not host-timeout proof. |
| `ATTACK-011` | `repair` | Explicitly say the isolated-directory rerun is a run-local workaround; canonical reducer repair is absent. |
| `ATTACK-012` | `sustain` | Dispatch-ID transcription mismatch remains bounded provenance residue. |
| `ATTACK-013` | `sustain` | Only directly test-backed runtime rows may be `EXECUTED`. |
| `ATTACK-014` | `sustain` | Development receipts and fixtures prove neither lifecycle promotion nor production. |
| Proposed `ATTACK-015` | `defer` | Append: canonical coordinator reuses wave-local action IDs; the deterministic extension repairs this run’s plan identity only. Keep open until canonical code and regression tests change. |

## Duplicate and overloaded concept findings

- “Selection” currently names Design concern selection, profile/template selection, WPRA selected-unit verification, and route selection. These require distinct artifact-qualified names.
- “Readiness” currently names frozen WPRA readiness, capability `mutation_runtime_ready`, fast-entry eligibility, and Task Session mutation admission. No single readiness scalar is valid.
- “Completion” currently names execution completion, synchronized Task Session completion, lifecycle-owner judgment, and registry release. These must remain separate states.
- “Terminal receipt” is used before required closeout has completed. Use “execution-terminal receipt” and reserve “synchronized Task Session result” for the joined/no-op closeout state.
- “Owner” must always be role-qualified: Design author, material producer, Task Session consumer, closeout owner, lifecycle owner, registry owner, or router.
- The three closeout checks in `BUG-004` are not duplicate validators: Plan authors the contract, preflight checks synchronizability before writes, and post-run closeout joins current owner evidence.
- Selection verification and fast entry in `BUG-002` are also not duplicates: one proves semantic unit identity; the other proves current consumer entry binding.

## Orchestration-defect classification

### Reducer receipt-directory overreach

The canonical loader enumerates every `*.json` in the supplied directory without filtering to required action IDs (`native_dispatch_coordinator.py:562-570`). The failed gate admitted `spawn-0001` through `spawn-0003` but also produced schema errors for unrelated JSON.

`driver-correction.json` correctly classifies the event as invalid reducer input scope and records no retry or respawn. The action-only rerun passed from the same valid receipts.

Classification: **canonical driver-interface defect; successful run-local workaround; canonical repair not completed**. The correction is incident evidence, not authority to declare the reducer repaired.

### Cross-wave action-ID collision

The canonical reducer derives the next wave’s start number from the current wave’s action count (`native_dispatch_coordinator.py:500-508`) and then generates IDs from that value (`:334-340`). After the one-action synthesis wave, this produced reviewer IDs `spawn-0002` through `spawn-0004`, colliding with earlier run actions.

`coordinator-action-id-extension.json` deterministically remaps them to `spawn-0005` through `spawn-0007`. Normalized diffs confirm the three action documents differ only in matching action-ID references.

Classification: **canonical global-identity allocation defect; deterministic run-local plan correction; no canonical code repair or completed regression proof**. The extension preserves this run’s causal audit but is neither canonical authority nor lifecycle promotion.

## Bounded repair guidance

1. Add one vocabulary matrix defining every `phase_status`, evidence axis, selection, admission, execution, closeout, lifecycle, and registry state.
2. Replace `OWN-003`’s “mutation-handoff eligibility” with “Plan artifact/handoff status”; mutation readiness belongs only to its independent receipt axis.
3. Bind the exact material producer, producer validator, receipt schema, and consumer compatibility fixture before sustaining `ATTACK-006`.
4. Bind the registry-release owner separately from Sigil Development/Spellcraft lifecycle judgment.
5. Rename pre-closeout “terminal Task Session receipt” to “execution-terminal receipt.”
6. Qualify Inventory as discovery/lookup proof only, not semantic or lifecycle proof.
7. Amend `ATTACK-011` to say “workaround, not repair” and append `ATTACK-015`; do not renumber existing attacks.
8. Require canonical reducer changes plus regression tests for mixed receipt directories and globally monotonic action IDs before either orchestration defect can be closed.
9. For live-uncommitted evidence, bind exact content digests or patch identity; repository commit plus mutable line selectors is not immutable source identity.

## Evidence gaps

- No exact registry-owner contract or current registry-owner receipt.
- No exact material-producer owner binding or producer-to-consumer compatibility witness.
- No real product-through-Refresh-owner closeout E2E witness.
- Generated parity remains blocked or unverified.
- Several `EXECUTED` labels rely on fixtures without explicitly limiting the evidence ceiling to the tested adapter/consumer path.
- Live-uncommitted selectors lack immutable byte or patch identities.
- Neither orchestration defect has a canonical implementation repair or regression receipt.

## ACTION_RECEIPT

```json
{
  "action_id": "spawn-0007",
  "dispatch_id": "2026-08-05-arcanum-building-system-research-route",
  "run_id": "arcanum-building-system-research-run-01",
  "wave_id": "reviewers",
  "step_id": "s3-review",
  "role": "skeptic-definitional",
  "status": "pass",
  "validation": "fail",
  "blockers": [
    "INVOKE_PHASE_AND_CAPABILITY_AXES_NOT_EXPLICITLY_MODELED",
    "MATERIAL_PRODUCER_OWNER_AND_COMPATIBILITY_UNBOUND",
    "REGISTRY_RELEASE_OWNER_UNBOUND",
    "INVENTORY_PROOF_CEILING_OVERBROAD",
    "SYNTHESIS_ATTACK_LEDGER_MISSING_ACTION_ID_COLLISION",
    "CANONICAL_REDUCER_DEFECTS_NOT_REPAIRED"
  ],
  "output_artifact": {
    "kind": "returned-reviewer-report",
    "description": "Self-contained definitional-soundness reviewer report returned in the native agent response",
    "repository_write": false
  }
}
```
