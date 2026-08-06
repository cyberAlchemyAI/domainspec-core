---
module: animejs-akv-query-contract-readiness
version: candidate-v1
status: defined
updatedAt: 2026-08-03
docType: specification
discovery_waiver_reason: Closed research, Refine matrices, and a blocked Task Session receipt already identify the exact contract defect and execution-readiness gaps; repeating discovery would not resolve a remaining ambiguity.
authority_effect: none
---

# Anime.js AKV Query Contract Readiness

## What this package owns

This development package owns the candidate-local contract for validating QRY-003 terminal outcomes and QueryReceipt invariants before any Anime.js ontology exists. It turns the closed Refine decision into five atomic implementation units: terminal policy, receipt schema, migration note, semantic validator, and eight-case replay.

It does not own Anime.js documentation truth, relation semantics, ontology admission, knowledge promotion, publication, or runtime deployment.

## Capability map

```text
Refine QRY-003 decision
  -> Query terminal contract + migration note
  -> QueryReceipt validator + eight fixtures
  -> integrated candidate receipt
  -> separate relation-repair package
  -> separately confirmed Ontology Vault/Harness decision
```

## Capabilities

| Capability | Outcome | Evidence boundary |
| --- | --- | --- |
| QueryTerminalContract | Declares the only six abstention codes, their total precedence, and eight terminal paths. | Schema/static checks only until fixtures execute. |
| QueryReceiptContract | Enforces mutually exclusive success and abstention states while retaining subordinate gaps. | Candidate validator receipt, not ontology evidence. |
| AlgorithmVersionMigration | Increments the algorithm contract without rewriting historical receipts. | Migration note and version assertions. |
| TerminalFixtureReplay | Tests the eight planned terminal paths against the candidate validator. | Future Task Session execution receipt. |

## Normative invariants

1. `abstention_code` is either `null` or one member of the closed vocabulary:
   - `ABSTAIN_UNKNOWN_VERSION`
   - `ABSTAIN_RUNTIME_CONTEXT`
   - `ABSTAIN_CONFLICT`
   - `ABSTAIN_PERFORMANCE_EVIDENCE`
   - `ABSTAIN_MISSING_SOURCE`
   - `ABSTAIN_AMBIGUOUS_INTENT`
2. A successful receipt has a non-empty `selected_ids` array and `abstention_code: null`.
3. An abstaining receipt has empty `selected_ids`, exactly one non-null declared primary code, and may preserve subordinate gaps.
4. Simultaneous failures select the first applicable code in the exact order listed in invariant 1.
5. A tie maps to `ABSTAIN_AMBIGUOUS_INTENT`; `ABSTAIN_AMBIGUOUS_CHOICE` is invalid.
6. Historical receipts are immutable. The new contract increments `algorithm_version`; it does not backfill or rewrite old receipts.
7. Candidate validation emits no ontology node, relation, admission, promotion, publication, release, or deployment effect.

## Terminal paths

| Path | Required terminal outcome |
| --- | --- |
| positive-js | select JS animate; non-empty selection; null abstention |
| positive-waapi | select `waapi.animate`; non-empty selection; null abstention |
| tie | `ABSTAIN_AMBIGUOUS_INTENT` and one discriminating next question |
| conflict | `ABSTAIN_CONFLICT` with both propositions preserved |
| missing-version | `ABSTAIN_UNKNOWN_VERSION` |
| unknown-requirement | missing binding uses `ABSTAIN_MISSING_SOURCE`; unrecognized intent uses `ABSTAIN_AMBIGUOUS_INTENT` |
| performance-claim | `ABSTAIN_PERFORMANCE_EVIDENCE` |
| multiple-failures | one primary code by total precedence; subordinate gaps preserved |

## Candidate target boundary

Future material writes are restricted to:

`projects/animejs/development/candidates/agent-knowledge-vault/query-contract/`

That path is a private development candidate, not an ontology root and not a public Arcanum surface.

## Non-goals

- materialize or decide the 25 relation candidates;
- ingest or reproduce the Anime.js documentation corpus;
- create `projects/animejs/ontology/agent-knowledge-vault`;
- change Inventory or ontology authority;
- run a Task Session in this Invoke authoring run;
- publish, deploy, release, or claim production readiness.

## Define acceptance

Define passes when the objective, closed vocabulary, precedence, receipt invariants, migration boundary, terminal paths, candidate path, non-goals, glossary, layering seed, and next owner are explicit and source-bound.
