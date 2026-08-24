# Explorer Feedback — Denominator and Durability Cuts

Status: complete, read-only. Sample window: `2026-08-14T14:20:00Z..2026-08-14T14:25:29Z`. No Git, provider execution, or writes by the explorer. Claim level: source-grounded current-byte package; readiness not claimed.

## Search closure

Expression: `Eve(?=$|[^a-z])|EVE(?=$|[^A-Za-z])|eve(?=$|[^a-z])`.

Method: `rg -a -n -o --pcre2 --hidden` with `.git`, `target`, `__pycache__`, and `*.pyc` excluded over the exact current RWO Go, RWO Rust, RWO planning/definitions/docs, handoff-notice, and four named unrelated-history roots. A path-only check used the same roots and `(^|[/_.-])eve([/_.-]|$)`. A semantic check searched `attempts.go` for `SessionID|LastEventID|AttemptSessionKnown|AttemptStreamAttached|MapSession|CorrelateLateSession|AttachStream|DetachStream|RequestCancel`.

```yaml
literal_occurrences: 2378
literal_hit_files: 284
path_only_fixture_files: 3
semantic_only_eve_shaped_files: 1
unique_files_classified: 288
unclassified_occurrences: 0
duplicate_occurrences: 0
rust_source_occurrences: 0
recursive_definition_occurrences: 0
```

| Class | Occurrences |
|---|---:|
| `active-provider` | 122 |
| `provider-neutral-Eve-named` | 3 literal plus 1 semantic-only selector family |
| `test-fixture` | 113 |
| `current-doc` | 68 |
| `generated-lifecycle` | 265 |
| `immutable-history` | 1,630 |
| `unrelated-history` | 177 |
| Total literal | 2,378 |

## Active Eve ledger

`GO` is `projects/cyberalchemy-orchestrator/implementations/rwo-sidecar-go`.

| Selector | Current SHA-256 | Class | Disposition |
|---|---|---|---|
| `GO/eve_leaf.go:17-215` | `a5bbe6699bac0d3a8e26e74f6a092cead0c061f0feac82d6803c531212471845` | `active-provider` | `replace-with-private-codex-leaf` |
| `GO/seat_material.go:29,344-465` | `4024b9146a28bfa74ea6614cb3c87c1a0a78b7bdcde10870e9b0e85995893688` | `active-provider` | `replace-provider-request-layer` |
| `GO/terminal.go:19,30-47,96-146,203-322` | `4ad73df8c5064f056105646914d3e3d84187b16c6039c2d93f2a1c5701e80a27` | `active-provider` | `version-separate-active-path-preserve-v1` |
| `GO/seat_material.go:28,308-341` | `4024b9146a28bfa74ea6614cb3c87c1a0a78b7bdcde10870e9b0e85995893688` | `provider-neutral-Eve-named` | `generalize-name-retain-decoder` |
| `GO/attempts.go:15-41,97-132,396-610,830-859,867-899` | `d77bfb4779f7126e790236d1c43896bf5d19e0496d9e89ff022a2b7be51f0144` | `provider-neutral-Eve-named` | `generalize-v2-preserve-v1` |
| `GO/attempts_test.go` | `0a4798500b56475e264d0932ec7038d679ba4581c6aec40406520bd19b786100` | `test-fixture` | `port-to-provider-handle-tests` |
| `GO/durable_e2e_test.go` | `48edff41ecb8c41d86b7b52c1eef364a6323185c60a921033bb9448bf417272b` | `test-fixture` | `replace-with-codex-fixture-e2e` |
| `GO/eve_leaf_test.go` | `f9f5ac26c709d28c3520d6db97cf3bfbeea309531609ba1e7245ea658c2d81a2` | `test-fixture` | `replace-with-app-server-protocol-tests` |
| `GO/failure_injection_test.go:25-30,41-42,52` | `5a370b5adf3c816408b6fae891ee6cf4342f2560687b3d740cf4fd668bc1f51c` | `test-fixture` | `replace-eve-rows-retain-generic-matrix` |
| `GO/seat_material_test.go:138-176` | `762dee78a5b7a868772ff5d7262ee5a1cf58a9601cf4d808ea61138774a38560` | `test-fixture` | `replace-exact-eve-request-case` |
| `GO/terminal_test.go` | `a591e8616e40334fbf660938f055f75a43249305d21ff770b72fb04d5e3587aa` | `test-fixture` | `port-provider-grammar-retain-convergence-tests` |
| `GO/testdata/eve-one-seat/*` | member hashes below | `test-fixture` | `replace-active-import-preserve-old-fixture-history` |
| `GO/README.md:6,41,50-51,89-99` | `2774e205cffa0d4e9a18e09e956690f086e203c83f9159a0144d6936e28132af` | `current-doc` | `update-only-after-new-proof` |

Fixture members:

```text
authorization-event.json  b6bd2d0844a5ed0c71d288a55d38ed5b97bc63cd60e78f6b96f2f6377e18bad8
composition-tuple.json    8f42cea6395c1d8a7a73952a73cb00e53a40309373a7f209e8498412b1623aab
composition.json          0f8bb97262774eb7471563c503150a0501a72562948f1ede7e2b2c25f90a7c3b
output-schema.json        c9c047a65cbe3a70021493137d28d94d8913ea06b6dc7b13ca4254a1909d07bb
seat-manifest.json        7e792eba8811c01d1a2964207c86c30ab630d2f8afe6c7562d2f24fe24d50787
```

## Docs, lifecycle, and history families

| Selector family | Binding | Class | Disposition |
|---|---|---|---|
| `docs/features/recursive-work-orchestrator/README.md:92-93` | `db819beb9117ef51878328ab36878bac0e94a71726db2497c97f9e4e4ce64f78` | `current-doc` | `update-only-after-new-proof` |
| `docs/features/recursive-work-orchestrator/ontology/**` excluding migrations; 11 files, 57 occurrences | `e6b229cf526b1d6e69dc4bde17bbb2104510d165dae81da93c6b818b51454bd7` | `current-doc` | `version-supersede-after-new-proof` |
| `RWO-IMPLEMENTATION-EVIDENCE-2026-08-13.md` | `af7f2cea938e128e404359db6d718fa30b89362d6c6947cdff4af8eeab6b53f4` | `immutable-history` | `preserve-immutable` |
| `implementations/rwo/DURABLE-RUNTIME-VALIDATION-REPORT.md` | `cea43a94279f31798ccb9dfb08a1b4d94523dfd30c3a5a16fe674c7b5e9ea5be` | `immutable-history` | `preserve-immutable` |
| ontology migration `0.2.0-to-0.3.0/**`; 16 files, 79 occurrences | `d691a5739142b27e5dc46f41699370fcc4ab352b044b563e5f286d83a7802db7` | `generated-lifecycle` | `preserve-applied-migration-create-new-version` |
| dated run `20260813T141038Z...`; 60 files, 708 occurrences | `7c4a0594f1752f59855b8c2b67af11f9de716f7239a9360eb80c01e1f2646de1` | `immutable-history` | `preserve-immutable` |
| dated run `20260813T172339Z...`; 37 files, 368 occurrences | `0e2916cf0960ea6d03205f9b817348f6e82f2dc33536203e0a95a14bfd8944b6` | `immutable-history` | `preserve-immutable` |
| dated run `20260813T190813Z...`; 62 files, 502 occurrences | `b63fb4159dfe18319391e48baaeb589c695fe94c6d1aede939efec42b77f9732` | `immutable-history` | `preserve-immutable` |
| dated run `20260813T215634Z...`; 12 files, 20 occurrences | `ef3974690992344e7f5699794b908472c24150c572fa6f547a7c50896679f708` | `immutable-history` | `preserve-immutable` |
| dated run `20260814T073949Z...`; 14 files, 69 occurrences | `52fa1f3671a38a3ac11de4b6fc0ef91c8d123f1102c071b90ee7b7fdce242217` | `generated-lifecycle` | `preserve-id-route-supersession-through-owner` |
| dated run `20260814T133756Z...`; 30 files, 98 occurrences | `a8ee15634d1a6bcb725f3693bb499f28c620720ec6627292d487915806b21f96` | `generated-lifecycle` | `preserve-id-route-supersession-through-owner` |
| handoff notice index and notice members | hashes in explorer return | `generated-lifecycle` | `preserve-lifecycle-id` |
| four enumerated external-tool/agent-infra history roots; 177 occurrences | manifests in explorer return | `unrelated-history` | `retain-unrelated-untouched` |

Family bindings are SHA-256 over sorted current `sha256sum <path>` rows for exactly the hit files in that family.

## Inherited Go durability-cut manifest

Each Codex validator is a required subtest of `TestCodexDurabilityCutMatrixComplete`.

| Cut | Current pre/post selectors | Existing witness | Codex status |
|---|---|---|---|
| `DUR-STORE-APPEND-SYNC` | `durable_store.go:257-307` / `313-337,461-465` | poison/reopen tests | specified-unexecuted: `store-append-sync-pre/post` |
| `DUR-CURSOR-CAS` | `durable_store.go:281-289,317-335`; `durable_runtime.go:217-247` | stale/CAS and runtime rebuild tests | specified-unexecuted: `cursor-cas-pre/post` |
| `DUR-LEASE-FENCE` | `attempts.go:223-249,614-622,659-697,803-813` | stale-fence and single-scheduler ablation tests | specified-unexecuted: `lease-fence-pre/post` |
| `DUR-ARM-BEFORE-SEND` | `attempts.go:252-283,396-429` | prepared-reopen, crash-after-armed, E2E tests | specified-unexecuted: `arm-before-send-pre/post` |
| `DUR-PROVIDER-WRITE` | Eve-only `eve_leaf.go:84-126` | Eve leaf and dangerous-cut E2E | specified-unexecuted for Codex initialize, thread/start, turn/start, permission, interrupt, reconciliation pre/post cuts |
| `DUR-RAW-EVIDENCE` | `eve_leaf.go:160-177`; `terminal.go:128-146` | uninterpreted-before-persistence and per-line reopen tests | specified-unexecuted: `raw-evidence-pre/post` per JSON-RPC message |
| `DUR-TERMINAL-CONVERGENCE` | `terminal.go:203-322,347-398` | terminal suite and E2E | specified-unexecuted: `terminal-convergence-pre/post` |
| `DUR-RUST-REDUCTION-ADMISSION` | `durable_runtime.go:144-180,201-247` | crash-before-semantic-append and synced-before-ack tests | specified-unexecuted integrated Codex: `rust-reduction-pre`, `rust-admission-post` |
| `DUR-OUTER-PROJECTION` | no implementation; `cmd/rwo-local-runtime/main.go:118-134` stops before outer projection | none | specified-unexecuted: `outer-projection-pre/post` |

Current source hashes:

```text
durable_store.go          87fa9b90f5b19d9d798dbcbf20faa1025ba033967d428d4840d7dce7f932993f
durable_store_test.go     b03e3b89e6f579698c42c7fe305e2ff9e47aa4cd3388167ca39dcf2a486a9fa4
durable_runtime.go        b40a401d1b0f5532049572671870880d425dc2674197d57835ac55a709251778
durable_runtime_test.go   1fc1b4e7e116091e6df4d9298d5cc28d790ce30a684c89d90426edd4e9565f31
attempts.go               d77bfb4779f7126e790236d1c43896bf5d19e0496d9e89ff022a2b7be51f0144
attempts_test.go          0a4798500b56475e264d0932ec7038d679ba4581c6aec40406520bd19b786100
eve_leaf.go               a5bbe6699bac0d3a8e26e74f6a092cead0c061f0feac82d6803c531212471845
eve_leaf_test.go          f9f5ac26c709d28c3520d6db97cf3bfbeea309531609ba1e7245ea658c2d81a2
terminal.go               4ad73df8c5064f056105646914d3e3d84187b16c6039c2d93f2a1c5701e80a27
terminal_test.go          a591e8616e40334fbf660938f055f75a43249305d21ff770b72fb04d5e3587aa
durable_e2e_test.go       48edff41ecb8c41d86b7b52c1eef364a6323185c60a921033bb9448bf417272b
failure_injection_test.go 5a370b5adf3c816408b6fae891ee6cf4342f2560687b3d740cf4fd668bc1f51c
cmd/.../main.go           344ef37f09d4cedece0e45162a5056d98dc126916afd56cc21e1f39f89dfa0a8
```

Existing named tests are historical witnesses for the older fake-Eve candidate; none ran in this feedback action. Current drift prevents treating them as current-byte acceptance. Every Codex cut remains specified-unexecuted.

## Limitation and ceiling

Closure covers readable filesystem bytes only in the enumerated roots and sample window. Without Git it cannot prove tracked/untracked/deleted lineage, ignored material outside the roots, or post-window stability. It proves no App Server compatibility, migration readiness, lifecycle synchronization, publication, deployment, or production property.
