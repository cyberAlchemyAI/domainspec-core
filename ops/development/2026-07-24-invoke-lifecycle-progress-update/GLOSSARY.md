# Glossary: Invoke Lifecycle Progress Protocol

Status: package-local candidate vocabulary

| Term | Meaning | Authority boundary |
| --- | --- | --- |
| authored-plan validity | Whether Invoke Plan produced a structurally and semantically acceptable planning artifact. | Invoke Plan receipt only; does not imply execution readiness. |
| execution epoch | Immutable identity and control snapshot for exactly one selected SWU. | Authored by Plan, independently validated, and not authoritative until admitted by the named transition owner. |
| epoch control digest | Digest over the epoch identity, selected unit, execution mode, role identities, controlling path identities and digests, dependencies, allowed writes, validation surface, and required artifact/receipt classes. | Any change creates a successor epoch; it cannot be repaired in place. |
| controlling path | Concrete artifact whose identity or content can alter the selected unit, authority, dependencies, writes, validation, or execution semantics. | Must be enumerated and exact-digest bound before epoch issuance. |
| non-controlling projection path | Declared generated or human-facing view that does not determine execution semantics. | Content drift requires classification but does not rewrite the epoch. |
| local execution contract | Immutable contract that authorizes Task Session to author effects inside a declared write scope for one epoch; it contains no pre-authored output bytes. | Produced before Task Session by the Plan-side contract producer and independently validated. |
| material package | Exact pre-materialized output package used by external, delegated, or reusable mutation modes. | Existing exact package and receipt validation remains fail-closed. |
| material producer | Role that emits the mode-required local execution contract or material package. | Must be compatible with the execution mode. |
| producer validator | Role independent of the producer that validates completeness, identity, owners, paths, dependencies, publication class, and validation surface. | Cannot be the producer or consumer for the same epoch. |
| material consumer | Role that verifies validated inputs and authors or applies effects. | Task Session is the local-mode consumer; it is not the producer or producer validator. |
| handoff readiness | Epoch-bound verdict `ready`, `gated`, or `blocked`. | Independent from authored-plan validity; only `ready` permits mutation-execution routing. |
| byte drift | Observed exact digest mismatch. | Always invalidates the old exact join; it says nothing by itself about semantic impact. |
| change impact | Independent verdict `execution_invalidating`, `projection_only`, `unrelated`, or `unclassified`. | Computed by a validator distinct from the projection writer; `unclassified` fails closed. |
| epoch transition | Append-only record of one allowed lifecycle edge backed by owner receipts. | Only the named transition-admission owner may admit it. |
| successor epoch | New epoch created when any epoch-control field changes. | Old epoch is retained and moves to `superseded` through an admitted transition. |
| same-epoch advancement | Forward transition whose epoch control digest is unchanged and whose only new fact is evidence or material satisfying an already-declared requirement. | Cannot change plan, unit, roles, paths, dependencies, writes, validation, or receipt classes. |
| transition kind | One explicit Refresh postcondition: `plan_repair`, `material_production_validation`, `projection_synchronization`, or `route_selection`. | A Refresh declares exactly one kind and performs no target implementation. |
| progress denominator | `goal_id + epoch_id + unit_id + authoritative_from_state + authoritative_to_state + mutation_crossed + blocker_fingerprint`. | Derived from admitted transitions; run counts and read models are not substitutes. |
| churn key | `goal_id + epoch_id + unit_id + authoritative_from_state + requested_to_state + blocker_fingerprint`. | Repetition without changed preconditions admits no transition and reports `churn_blocked`. |
| legacy unadmitted | Existing plan lacking a current epoch and readiness receipt. | It gains no inferred readiness and must be revalidated through the new admission path. |
| transition-admission owner | Named owner that admits or rejects epoch transitions after validating producer receipts. | Unresolved in this package; selecting it is the first lifecycle decision. |

These terms are candidates for sanitized public definition or local schema
fields. They are not canonical Arcanum vocabulary until their owning lifecycle
accepts them.

