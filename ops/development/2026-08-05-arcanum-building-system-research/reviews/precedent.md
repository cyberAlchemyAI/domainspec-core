# Skeptic-Precedent Reviewer Report

`PRECEDENT_GATE: FAIL`

The synthesis cannot advance unchanged. Its main precedent failure is an unresolved duplicate runner/owner boundary: `CAP-002` assigns finite-frontier coordination to Implementation Readiness, while `CAP-007` assigns an ordered until-blocker series to Task Session Until Blocker. Current source gives both capabilities an overlapping bounded Work-Pack loop, including an “until real blocker” mode.

No proposed capability or repair was ownerless. Every integration maps to an existing source owner, so this review returns no `kill` verdict. Repairs must modify or compose existing owners rather than introduce another compiler, runner, ledger, readiness stage, closeout path, or lifecycle owner.

Repository identity inspected: parent `ab46061bf14db23a01054c2fd3fafec60fb5eb2f`; Arcanum `07b01c9dd4e918ae0b0d83f6a2cde52ea8f9a295`, with relevant live-uncommitted changes.

## Existing-owner and integration gate

| Synthesis IDs | Verdict | Existing owner and direct selector |
|---|---|---|
| `CAP-001`, `OWN-001..004` | sustain | Invoke Plan owns planning/handoff in `arcanum/spells/invoke/plan.md:13-32,137-165,333-397`; Implementation Layering already owns the layer model in `arcanum/transmutations/implementation-layering/SKILL.md:12-18`. |
| `CAP-002`, `OWN-005..006`, `SYS-002` | repair | WPRA is a distinct audit-only owner: `arcanum/spells/work-pack-readiness-audit/README.md:17-18,194-210`. Implementation Readiness already owns an executable outer-loop reducer: `arcanum/spells/implementation-readiness/README.md:11-16,47-84`. |
| `CAP-003`, `OWN-007..009`, `SYS-003` | sustain | Task Session owns one SWU and admission/closeout in `arcanum/arcana/task-session/SKILL.md:260-320,328-420`; Context Builder owns evidence selection at `arcanum/transmutations/context-builder/SKILL.md:14-20`. |
| `CAP-004`, `OWN-010`, `SYS-004` | sustain | Continuation Router already owns one-hop admission, dispatch, and join—not owner work—at `arcanum/arcana/continuation-router/SKILL.md:14-19,136-164`. |
| `CAP-005`, `OWN-008` | sustain | Decision Gate owns blocker decisions, not protected-owner validity: `arcanum/arcana/decision-gate/SKILL.md:14-19,123-155`. |
| `CAP-006`, `OWN-004`, `BUG-005` | repair | Distill owns `pass|flag|block`, while Invoke Plan owns mutation-capable handoff: `arcanum/arcana/distill/SKILL.md:135-137`; `arcanum/spells/invoke/plan.md:137-165,360-361`. Criticality must be bound in Plan/Work-Pack data, not by adding another readiness gate. |
| `CAP-007` | repair | `task-session-until-blocker` already claims bounded serial orchestration and an immutable chain runner at `arcanum/spells/task-session-until-blocker/README.md:1-18,21-37,79-115,211-217`. This overlaps Implementation Readiness’s `finite-frontier`/`until-real-blocker` loop. One owner must be selected; the other should hand off rather than duplicate reduction. |
| `CAP-008`, `BUG-014` | repair | Goal is already source-bound and deployed: `arcanum/spells/goal/README.md:1-17,176-178`; `.agents/skills/goal/SKILL.md:3-9` explicitly binds `canonical_source: spells/goal/README.md`. |
| `CAP-009`, `OWN-013` | sustain | Dispatch Spec validates routes; Subagent Strategy governs dispatch; Orchestrate owns scheduling/join/closeout: `arcanum/formulae/dispatch-spec/SKILL.md:3`; `arcanum/arcana/subagent-strategy/SKILL.md:14-20`; `arcanum/runtime/orchestrate/SKILL.md:59-68`. |
| `CAP-010`, `OWN-014` | sustain | Sigil Development and Spellcraft are the existing, type-specific lifecycle owners: `arcanum/arcana/sigil-development/SKILL.md:51-67`; `arcanum/arcana/spellcraft/SKILL.md:32-48`. Experiment Harness owns mechanics only: `arcanum/arcana/experiment-harness/SKILL.md:98`. |
| `CAP-011`, `SYS-005`, `CRAFT-001..003` | sustain | Craft owns only project-local ledger state: `arcanum/arcana/craft/SKILL.md:15-18,33-69,312-317`. |
| `CAP-012`, `BUG-010` | sustain | Inventory is an existing non-authority read-model owner: `arcanum/arcana/inventory/SKILL.md:335-339`. |
| `CAP-013` | sustain | Observability Setup already owns deterministic package installation/verification: `arcanum/formulae/observability-setup/SKILL.md:14-20`. |
| `BUG-001..004`, `BUG-006..011` | sustain | Existing boundaries are already owned by WPRA, Implementation Readiness, Invoke producer validation, Task Session admission/closeout, Continuation Router, and Invoke Refresh. No new stage is warranted. |
| `BUG-012..013` | sustain | Both reducer defects belong to the existing Orchestrate coordinator, `arcanum/runtime/orchestrate/scripts/native_dispatch_coordinator.py`; do not create a replacement reducer. |

## Attack ledger verdicts

| Attack ID | Related synthesis IDs | Verdict | Result and bounded repair |
|---|---|---|---|
| `ATTACK-001` | `CHG-003`, `BUG-008`, `CAP-002` | sustain | Canonical/generated WPRA hashes differ for all three named scripts. Regenerate only the existing spell package through `arcanum/tools/sync-generated-skill-package.sh:4-25,106-121,180-242`, then validate parity. |
| `ATTACK-002` | `CHG-004`, `BUG-009`, `CAP-003..004` | sustain | Task Session and Continuation Router canonical/generated `SKILL.md` hashes differ. Use the same selective generation owner; do not create a second runtime contract. |
| `ATTACK-003` | `CHG-002` | sustain | `git -C arcanum status --short` confirms the August 4–5 paths are live-uncommitted. |
| `ATTACK-004` | `SYS-006`, `GATE-011`, `TRACE-NORMAL-001` | sustain | The existing closeout owner path is Task Session → Continuation Router → Invoke Refresh at `task-session/SKILL.md:351-420`; supply one real product-through-owner-closeout witness rather than another closeout implementation. |
| `ATTACK-005` | `BUG-005`, `CAP-006` | sustain | Plan permits a flagged route with named gaps but lacks a machine-bound noncriticality field. Add and validate that binding in the existing Plan/Work-Pack contract; Task Session already treats unclassified obligations as critical at `task-session/SKILL.md:328-350`. |
| `ATTACK-006` | `BUG-003`, `LIN-004` | repair | Cross-owner compatibility test source exists: `arcanum/arcana/task-session/development/test_plan_once_admission.py:21-38,61-72,282-327,332-352` loads the Invoke material validator and Task Session admission resolver together. Repair the claim to “test source exists; current dispatch execution proof was not supplied.” |
| `ATTACK-007` | `BUG-014`, `CAP-008` | repair | Goal canonical binding is not missing; both canonical README identity and generated `canonical_source` are explicit. Treat Goal as already deployed, while preserving its router-only boundary. |
| `ATTACK-008` | `BUG-009`, `CHG-003..004` | repair | Source identity is explicit in generated frontmatter (`canonical_source`); currentness/parity is the actual defect. Replace “identity ambiguous” with “provenance known, generated bytes stale/divergent.” |
| `ATTACK-009` | `CRAFT-003`, `CAP-011` | sustain | Craft explicitly lacks an automated runner/renderer and defers route-exchange, projection, row-update, validation, and artifact-manifest schemas: `craft/SKILL.md:15-18`; `craft/templates/ledger.schema.yml:24-47`. |
| `ATTACK-010` | `TRACE-FAIL-005`, `GATE-012` | sustain | Fixture/validator tests do not prove an actual host timeout. Retain the evidence ceiling. |
| `ATTACK-011` | `BUG-012..013` | sustain | Run evidence and coordinator source reproduce the receipt-scope defect. Repair `_load_receipts_directory` in the existing coordinator to accept an exact required-action set or exact receipt list, with unrelated-JSON regression coverage. |
| `ATTACK-012` | explorer-runtime receipt identity | defer | Current durable `receipts/explorer-runtime.json:4` contains the correct `-route` dispatch ID. The alleged verbatim native return is not a persisted reproducible artifact available to this review. |
| `ATTACK-013` | all `EXECUTED` claims | sustain | Contract and closure rows remain source-observed unless backed by an execution receipt. |
| `ATTACK-014` | `CHG-006` | sustain | Development fixtures and receipts remain candidate evidence; no promotion, publication, release, deployment, or production claim is admissible. |
| `R-ATTACK-ACTION-ID-001` | reviewer-added; absent from synthesis | sustain | The coordinator calls `_compile_named_wave_actions(..., start_action_number=len(actions)+1)` at `native_dispatch_coordinator.py:499-507`, using current-wave cardinality rather than run-global history. This reproduced `spawn-0002..0004`; the parent’s deterministic mapping to `spawn-0005..0007` was semantic-preserving. Repair the existing coordinator to derive the next ordinal from persisted run-global action identities and add unequal-cardinality multi-wave tests. |

## Run-local defect evidence

Receipt scope:

- `native-run/run-01/wave-01-reduction/driver-correction.json` records unrelated confirmation/tension JSON being enumerated as receipts, valid agent receipts, and no retry/respawn.
- `arcanum/runtime/orchestrate/scripts/native_dispatch_coordinator.py:560-571` confirms the loader blindly reads every `*.json`.
- `wave-01-reduction-repaired/gate-decision.json` passes when given an action-only directory.

Action-ID collision:

- `wave-02-reduction/actions/spawn-0002.json` through `spawn-0004.json` are the stock reviewer actions.
- `wave-03-plan/coordinator-action-id-extension.json` records the exact deterministic mapping `0002→0005`, `0003→0006`, `0004→0007`, with no semantic changes.
- The responsible owner is the current Orchestrate coordinator, not a missing compiler or ledger.

## Evidence gaps

- No real product-through-Invoke-Refresh closeout witness was supplied.
- Generated parity was checked by current hashes, not repaired or executed.
- The Invoke/Task Session cross-owner test exists, but this review did not execute it.
- The native verbatim explorer return needed to resolve `ATTACK-012` is unavailable as a repository artifact.
- The duplicate `implementation-readiness` versus `task-session-until-blocker` loop owner requires an explicit owner-boundary decision before the synthesis can pass.

```json
{
  "schema_version": "arcanum.native-dispatch-runner.receipt.v0.1",
  "action_id": "spawn-0005",
  "dispatch_id": "2026-08-05-arcanum-building-system-research-route",
  "run_id": "arcanum-building-system-research-run-01",
  "wave_id": "reviewers",
  "step_id": "s3-review",
  "role": "skeptic-precedent",
  "capability_ref": "research",
  "status": "pass",
  "validation": "fail",
  "blockers": [
    "CAP-002 and CAP-007 currently assign overlapping bounded Work-Pack execution loops to implementation-readiness and task-session-until-blocker",
    "The synthesis must repair ATTACK-006, ATTACK-007, and ATTACK-008 against current source",
    "The synthesis does not yet include the reproduced run-global action-ID collision"
  ],
  "artifacts": [
    "returned reviewer report in this markdown response"
  ],
  "output_artifact": {
    "kind": "native-agent-return",
    "description": "Self-contained skeptic-precedent reviewer report returned by spawn-0005; no repository file was written"
  }
}
```
