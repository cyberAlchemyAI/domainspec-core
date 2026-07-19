# Distill Validation — Backend type test-engine completeness plan

## Run

- Mode: Validate
- Depth: Standard planning budget
- Execution: local Proposer/Balancer role passes; no subagent dispatch is authorized by this planning run
- Input: `PLAN.md`, `IMPLEMENTATION-LAYERING.md`, `WORK-PACK.md`, and the shared planning contracts
- Verdict: **flag**

The plan is coherent and recomposable after the accepted FPR-02B decision. Implementation is not executed by this refresh: one dependency-ready SWU still requires a separate Task Session, the independent edge/consumer proof surfaces remain unexecuted, and FPR-02U is explicitly not a dependency.

## Smallest coherent unit

SWU-BTE-001 is the smallest independently useful implementation unit. It consolidates the existing YAML interpretation without deciding which profile is admitted, changing node storage, or claiming completeness.

It is coherent because it has:

- one contract input: the existing 13 meta-type YAML schemas;
- one internal boundary object: `CriterionSubject`;
- one observable result: all current content and instance validation use the same strict evaluator;
- independent tests and rollback scope.

## Proposer pass

The proposed result is an eight-SWU chain across four proof layers:

1. one shared YAML criterion kernel and three source adapters;
2. one versioned exact-13 node profile plus exact-16 backend edge profile and discriminating corpus;
3. one independent obligation catalogue reconciled with derived, executed, and mutation-tested sets;
4. one fail-closed required check plus integrated IOLM/Body War consumer proof and independent replay.

The plan preserves the selected one-JSON-file-per-node source layout and treats the YAML schema files as criterion authority rather than replacing them with duplicated formation JSON schemas.

## Balancer pass

| Tension | Response | Disposition |
|---|---|---|
| The FPR-02B supported profile owner gate is accepted. | Keep W0 as a verified decision receipt and name SWU-BTE-001 as the first unit after separate Task Session selection; exclude FPR-02U from the dependency. | Accepted; follow-up execution. |
| `instances.ts` and `validate-content.ts` contain duplicated YAML interpretation. | Put kernel extraction first and forbid a third evaluator in the minted compiler. | Accepted; plan revised. |
| The derivation engine could define both expected and generated obligations. | Freeze digest-bound `O_spec` under an independent owner before deriving `O_gen`. | Accepted; authority split added. |
| “All backend types” could inflate into all relationships, semantics, or universal correctness. | Define the exact claim as 13 backend kinds, 16 backend signatures, causal proof, and integrated read-only consumer evidence; defer UI, semantic, and universal correctness. | Accepted; scope bounded. |
| Eight SWUs and several evidence sets create navigation load. | Organize work into L0–L3, W0–W4, task files, exact handoffs, and a single next executable unit. | Accepted; navigation revised. |

## Technique trace

| Technique | Result | Evidence |
|---|---|---|
| Abstraction-level guard | pass | Plan stays at formation-contract and evidence architecture; algorithms live in task-local SWUs. |
| SCU/SWU reduction | pass | SWU-BTE-001 is independently executable and valuable. |
| Recomposition proof | pass | Kernel → adapter/profile → corpus → independent obligations → derivation/execution → required check. |
| Evolution map | pass | L0 through L3 each add a distinct proof capability. |
| Cognitive-load budget | pass | Five waves, six task files, one exact next unit. |
| Requisite variety | pass | Eight YAML rule forms, three input shapes, 13 kinds, and fail-closed negative cases are represented. |
| Boundary-object check | block | Profile/version and adapter ownership are named, but the FPR02 receipt is not complete. |
| Concept-vs-knowledge check | flag | Exact successor profile/version is still proposed rather than ratified knowledge. |
| Premortem | pass | Highest-risk failure and guard are explicit below. |
| Frame-expiry check | pass | Revalidation triggers are explicit below. |
| Navigable-result check | pass | Root result, shared contracts, tasks, waves, dispatch, and next route are linked from `WORK-PACK.md`. |

## Recomposition proof

The units recompose without hidden authority changes:

```text
13 YAML schemas
  -> shared criterion kernel
  -> Markdown / instance / minted-node adapters
  -> approved exact-13 profile + all-kind corpus
  -> independent O_spec
  -> compiled graph/source manifest -> O_gen
  -> generated tests -> executed tests -> killed mutants
  -> fail-closed required-check receipt
  -> independent release-owner evidence
```

Removing any unit makes the final claim weaker in a named way: no common meaning, no all-kind witness, no independent denominator, no executed proof, or no integration gate.

## Premortem

Most likely failure: the implementation adds another formation truth—either hand-authored per-kind JSON schemas or kind branches in the compiler—so the YAML contracts and test engine drift while all local tests remain green.

Guard: one shared criterion kernel, versioned profile bindings with schema digests, adapter conformance tests, an independently frozen denominator, and exact-set comparison.

## Frame expiry

Re-run planning/distillation when any of these changes:

- a ninth YAML rule form or a 17th criterion is introduced;
- the active backend kind set changes;
- UI kind admission becomes part of the target profile;
- UI/cross-layer, semantic, or code-conformance proof enters the claim;
- the one-file-per-node canonical source layout changes;
- independent edge schema, resolver, or source-root rules change;
- semantic or code-conformance proof is requested;
- the FPR-02B owner selects a materially different profile/body mapping.

## Verdict and next move

- Plan quality: pass.
- Recomposition: pass.
- Execution authorization: separate Task Session required; no SWU selected by this refresh.
- Next route: select exactly one dependency-ready SWU, then execute through Task Session with strict context and receipt.
