# Implementation Layering: Verification Weaver

## Layer Decision

| Layer | Scope | Promotion stance |
| --- | --- | --- |
| L0: contract | README, SKILL, parent receipt schema, definitions, anti-patterns. | Candidate only. |
| L1: routing fixtures | Synthetic positive and negative fixture inputs. | Candidate validation evidence. |
| L2: validator | Shell-first runner with optional TypeScript structured checks. | Local validation evidence only. |
| L3: lifecycle | Experiment-harness report and sigil-development review. | Required before registry/runtime exposure. |

## Owner Boundary

`verification-weaver` owns the parent route and receipt. It does not own the
lane implementations. Each lane remains status-qualified:

- `test-derivation`: draft/repository-local; public L0 derivation lane.
- `ux-evidence-validator`: seed/not promoted; browser/UX evidence lane.
- `experiment-harness`: mechanics owner; repeatable validation evidence lane.
- `architecture-pattern-inventory`: mapping owner; architecture-to-test-gap lane.
- `research-evidence-harness`: public sigil surface; claim-status-limited lane.

## Public/Private Layer Split

Internal private evidence may inform this package. Public implementation may
only carry abstracted lessons and synthetic fixtures.

Blocked from public package content:

- private implementation paths as evidence;
- private fixtures or examples;
- private pass/fail result claims;
- generated runtime outputs as authority;
- local observability logs as source evidence.

## Smallest Coherent Unit

`SWU-VW-001`: create the candidate public package with public docs, receipt
schema, synthetic fixtures, negative controls, and validation runner. The unit
is large enough to prove the route and small enough to avoid registry/runtime
promotion.

## Recomposition Proof

If `SWU-VW-001` completes, it recomposes into the design by producing:

- target classifier;
- owner lane table;
- parent `VERIFICATION-WEAVE` schema;
- runnable positive fixtures;
- runnable negative controls;
- public-boundary checks;
- a local validation report;
- explicit residue and next `sigil-development` route.
