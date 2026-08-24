---
module: animejs-agent-knowledge-vault
version: current
status: candidate-local-complete
updatedAt: 2026-08-03
docType: work-pack
---

# WORK-PACK: Anime.js Agent Knowledge Vault

## Control fields

| Field | Value |
| --- | --- |
| Work Pack ID | `WP-AKV-001` |
| workPackGateStatus | `candidate-local-complete` |
| complexity | `medium` |
| outputMode | `split` |
| executionPackRef | `EXECUTION-PACK.md` |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` |
| readinessProfile | `selected-unit-at-task-session` |
| selection candidate | none; terminal sentinel reached |
| distillValidationStatus | `pass` |
| swuAtomicityStatus | `pass` |
| firstUnitNarrownessStatus | `pass` |
| closeoutSyncStatus | `joined-pass` |
| activeLayerWindow | complete through `L3` |

## Objective and delivery boundary

Build a candidate-local, source-bound Anime.js knowledge vault that agents can
query while working. Cover every observed official documentation route and
every row of the pinned v4.5.0 repository manifest, preserve evidence and
version boundaries, capture later WorkEpisodes and Lessons without promoting
them automatically, and return deterministic abstentions when evidence is
missing, stale, conflicting, unexecuted, or unsafe to reproduce.

The package may store identifiers, selectors, headings, structured pointers,
digests, original paraphrases, and short compliant quotations. It must not
mirror documentation prose or code, claim runtime behavior from source
presence, promote ontology meaning, publish, deploy, or claim production
readiness.

## Source design

- `../../refinement-runs/20260803T175423Z-animejs-blocking-defects/stages/08-query-contract-matrix.json`
- `../../refinement-runs/20260803T175423Z-animejs-blocking-defects/stages/08-relation-behavior-witness-matrix.json`
- `../../refinement-runs/20260803T175423Z-animejs-blocking-defects/stages/10-final-interrogation-and-synthesis.md`
- `../../research/2026-08-03-animejs-agent-knowledge-vault/receipts/knowledge-vault-synthesis-reviewer-repair.json`
- `../../research/2026-08-03-animejs-agent-knowledge-vault/receipts/explorer-official-source-feedback-1.json`

## SWU manifest

| Order | SWU | Parent task | Layer | Primary behavior | Dependencies | Unique successor |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `SWU-AKV-NV-001` | `TASK-AKV-CONTRACTS` | L0 | implement the closed QRY-003/QueryReceipt contract and eight fixtures | none | `SWU-AKV-NV-002` |
| 2 | `SWU-AKV-NV-002` | `TASK-AKV-CONTRACTS` | L1 | canonicalize five merge relations and exclude three deferred relations | 001 | `SWU-AKV-NV-003` |
| 3 | `SWU-AKV-NV-003` | `TASK-AKV-CONTRACTS` | L1 | execute one discriminating baseline/mutant witness for each retained relation | 002 | `SWU-AKV-NV-004` |
| 4 | `SWU-AKV-NV-004` | `TASK-AKV-SOURCES` | L2 | materialize the complete official documentation manifest | 003 | `SWU-AKV-NV-005` |
| 5 | `SWU-AKV-NV-005` | `TASK-AKV-SOURCES` | L2 | materialize the complete pinned v4.5.0 repository manifest | 004 | `SWU-AKV-NV-006` |
| 6 | `SWU-AKV-NV-006` | `TASK-AKV-GRAPH` | L2 | build the populated typed graph from the two source manifests | 005 | `SWU-AKV-NV-007` |
| 7 | `SWU-AKV-NV-007` | `TASK-AKV-GRAPH` | L2 | build deterministic consultation views and search indices | 006 | `SWU-AKV-NV-008` |
| 8 | `SWU-AKV-NV-008` | `TASK-AKV-VALIDATE` | L3 | validate the complete package and emit a digest-bound terminal receipt | 007 | none |

The machine companion represents the final `none` successor with the required
`__complete__` terminal sentinel. The sentinel is not an executable SWU and
must produce a null continuation cursor successor.

## Task board

| Task | Contract | Layer | Gate | Status |
| --- | --- | --- | --- | --- |
| `TASK-AKV-CONTRACTS` | `work-pack/tasks/TASK-AKV-CONTRACTS.md` | L0-L1 | receipts 001-003 pass | complete |
| `TASK-AKV-SOURCES` | `work-pack/tasks/TASK-AKV-SOURCES.md` | L2 | receipts 004-005 pass | complete |
| `TASK-AKV-GRAPH` | `work-pack/tasks/TASK-AKV-GRAPH.md` | L2 | receipts 006-007 pass | complete |
| `TASK-AKV-VALIDATE` | `work-pack/tasks/TASK-AKV-VALIDATE.md` | L3 | receipt 008 passes both terminal commands | complete |

## Task Session closeout synchronization

Every SWU uses lifecycle owner `invoke:refresh:apply-approved`. The exact
closeout target inventory is this file, `WORK-PACK.json`, the owning task file,
and `HANDOFF-STATE.json`. Task Session captures their live present/absent SHA-256
baselines before mutation. Allowed closeout deltas are `evidence_added`,
`blocker_opened`, `blocker_resolved`, `status_changed`, and `route_changed`.
Owner validation is JSON parse, scoped whitespace validation, the SWU command,
and successor uniqueness. The expected owner receipt is
`task-sessions/<run-id>/INVOKE-REFRESH-RECEIPT.json`. Successors are exactly the
ordered rows above; closeout returns but never executes the successor.

## Frozen relation representation decisions

The five `MERGE` rows are resolved before the semantic epoch:

- `addresses`: `WorkEpisode.task_id` is canonical; any edge is derived only.
- `contains`: `Attempt.episode_id` is canonical; `WorkEpisode.attempt_ids` is a sorted derived index; no stored edge.
- `yields`: `Outcome.attempt_id` is canonical; `Attempt.outcome_id` is a unique reverse lookup; no stored edge.
- `suggestsNextQuestion`: `NextQuestion.gap_id` is canonical; receipt question IDs are derived and sorted; no stored edge.
- `citesEvidence`: `QueryReceipt.evidence_record_ids` is canonical; no stored edge.

The three `DEFER` rows (`observes`, `applies`, `exposesGap`) are excluded from
the stored relation vocabulary until a future contract gives each an
observable consumer delta.

## Source snapshot expectations

- Documentation: 418 materialized routes reproduce the exact recovered
  semantic JSONL SHA-256
  `681f004e04a91ab1a3462e882edff24d09454297f34a41863e81df06e20066fb`
  and raw page-set SHA-256
  `63125e931350f5dbf8552a289ac80d687bb1867e7c94c1e2d6e33904f16befcd`.
  The earlier approximate candidate serialization is superseded, not equated.
- Repository: v4.5.0 commit
  `2c9cf8ea00329f6768c7d7902252ed977d75ce42`, 348 rows, manifest SHA-256
  `f4026dec178de523262aca34dcddc5e419681b3494f37f496d9da8553d3ebcc0`.
  The exact recovered serialization is now materialized and validated; the
  earlier approximate candidate serialization is superseded, not equated.

Any later mismatch blocks the source SWU and requires an explicit snapshot
decision; status-only progress does not trigger another readiness audit.

## Validation strategy

- JSON/schema: closed JSON shapes, unique IDs, endpoint resolution, exact digests.
- Query: eight QRY-003 terminal fixtures and deterministic replay.
- Relations: 17 baseline/mutant comparisons; five merges have one canonical representation; three deferred edges are absent.
- Sources: 418/418 official documentation routes and 348 pinned source rows, with mutable/pinned contexts kept distinct.
- Graph: node/relation invariants, state transitions, cycles, source coverage, authority guards, and copyright checks.
- Views: generated from one graph digest; no view may become source authority.
- Terminal: deterministic rebuild and digest-bound validation receipt.

## Distill validation

Pending the formal Validate pass. The proposed optimization point is
`SWU-AKV-NV-001`: it changes one closed query behavior and can pass before any
source crawl or graph population. Each later SWU has one independent acceptance
boundary and recomposes into the complete consultation loop:
query contract -> relation semantics -> source evidence -> graph -> views -> receipt.

## Dispatch technique trace

| Technique | Applied to | Validation expectation |
| --- | --- | --- |
| `sequence` | eight-unit frontier | one unique dependency-ready successor |
| `scu_swu_reduction` | SWU manifest | one primary behavior and independent acceptance per SWU |
| `recomposition_proof` | query-to-receipt chain | every SWU contributes to the final agent-consultation loop |
| `validation_loop` | every SWU | command and acceptance evidence declared before execution |
| `owner_boundary_check` | Invoke -> Task Session -> Ontology Vault | planning, execution, and ontology validation remain distinct |
| `handle_handoff` | source design and generated receipts | use repository paths and digests, not copied context |
| `residue_ledger` | deferred relations and unverified lessons | residue remains explicit and queryable |
| `execution_receipt_handoff` | Task Session closeout | exact terminal and owner receipts required |

## Blockers and residue

- No Work Pack blocker remains; all eight bounded SWUs passed.
- Six candidate-local knowledge gaps remain in the package residue ledger,
  including exact symbol extraction, executed behavior, verified lessons,
  performance, accessibility, and copyright threshold review.
- There are currently zero verified Anime.js operational Lessons; that is an intentional truthful result, not a coverage failure.
- Promotion, publication, deployment, runtime integration, performance, accessibility, and production readiness remain outside this Work Pack.

## Next route

The terminal sentinel is reached and no successor is authorized. Agents may
consult the candidate package directly. A future owner can open a new Work Pack
for one named residue item; status-only consultation and work-episode additions
must not rerun this completed readiness frontier.
