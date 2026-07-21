# Execution Pack — Backend Type Test Engine Completeness

## Planning Control Fields

| Field | Value |
| --- | --- |
| planningGateStatus | `ready-after-decision-gate` |
| complexity | `high` |
| baselineWave | W0 |
| activePlanRef | `WORK-PACK.md` |
| workPackManifest | `WORK-PACK.md` |
| layeringArtifact | `IMPLEMENTATION-LAYERING.md` |
| activeLayerWindow | `n/a` |
| lastPlannedAt | `2026-07-17T05:20:00-03:00` |
| readinessProfile | release-candidate evidence; non-admission |

## Wave Board

| Wave | Layer | Question | Tasks/SWUs | Entry gate | Exit evidence | State |
| --- | --- | --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0-OWNER-GATE.md) | gate | Is the exact backend profile, node/edge topology, and claim boundary owner-selected? | accepted FPR-02B Decision Gate | FPR-01 and lane split closed | accepted decision receipt | pass |
| [W1](work-pack/waves/W1-SHARED-KERNEL.md) | L0 | Can one kernel serve Markdown, instance, and node surfaces? | CONTRACT 001; NODE 003 | W0 pass | eight rule-form parity proof | in-progress — 001 complete; 003 next |
| [W2](work-pack/waves/W2-ALL-BACKEND-KINDS.md) | L1 | Can the node/edge style represent and discriminate every backend kind and signature? | CONTRACT 002; NODE 004; EDGE COVERAGE | W1 pass | 13 positive nodes, 16 positive edges, causal mutants | pending predecessor |
| [W3](work-pack/waves/W3-OBLIGATION-PROOF.md) | L2 | Does the engine execute exactly an independent structural obligation set? | OBLIGATIONS 005; DERIVATION 006–007 | W2 pass | exact-set and execution/mutation receipts | pending predecessor |
| [W4](work-pack/waves/W4-INTEGRATE-VERIFY.md) | L3 | Do BTE and both consumer proofs fail closed and replay reproducibly? | INTEGRATION 008 core; external IOLM and Body War receipt gates; 010 consumer manifest; VERIFY exemption | W3 pass + W2 edge/16-signature receipt | core, consumer, terminal, and independent replay receipts | pending predecessor |

## Ordering And Parallelism

- W0 is strictly sequential and human-owned.
- Within W1, `SWU-BTE-003` depends on `SWU-BTE-001`; no parallel execution.
- Within W2, profile binding precedes corpus completion because fixtures must declare one exact profile.
- Within W3, the independent catalogue precedes engine exact-set comparison; derivation precedes emission.
- W4 is sequential: 008 core, independently owned IOLM run, independently owned Body War run, 010 consumer validation, then independent verification. Consumer work cannot begin before the green core receipt exists.
- No whole-wave execution is authorized. Select one SWU at a time through Task Session; the UI lane is never joined.

## Closure Obligations

1. Exact 13-kind profile, exact 16-signature backend profile, and no UI admission.
2. Exactly one YAML schema per admitted kind.
3. All current criterion rule forms evaluated through one kernel.
4. Positive exercise for every kind and killed mutation for every criterion.
5. Independent `O_spec` and exact derived/executed equality.
6. Zero skip/todo/orphan/unrunnable/surviving-mutant residue.
7. Missing and empty release witnesses fail closed.
8. `verify:bte:core` records and replays source/profile/schema/tool/core evidence and remains non-admitting.
9. Fresh, independently produced IOLM and Body War receipts exist after core; fixture/schema-only evidence is rejected.
10. `verify:bte:consumers` validates the external receipt handles and their exact identities, raw digests, posture, and non-admission.
11. Terminal `verify:bte` composes `verify:bte:core + verify:bte:consumers` before independent replay.
