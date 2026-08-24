# Augmentor unified agent architecture — final synthesis repair

This is synthesis revision `2/2` for action `spawn-0004`. It incorporates
`synthesis-revised.md`; the material below supersedes that file where the final
reviewers required more exact terminology or fixture detail. Unchanged architecture,
connection, UX, boundary, capability-gap, dependency, verdict, and open-owner
sections remain part of the final synthesis.

Status: `PASS_AS_RESEARCH_ARCHITECTURE_WITH_NO_EXECUTED_V0`.

No fixture, test, browser run, production adapter, runtime integration, evaluator,
effect runtime, promotion, or measurement was executed. The fixture contract below
is a research-specified future artifact, not a current repository implementation.

## Final semantic and owner corrections

- `InventoryCandidateEvidenceSet` is a selector package pending Inventory
  validation.
- `InventoryValidatedCandidateEvidenceSet` is an Inventory-validated handoff
  candidate. It remains non-canonical and non-promotional.
- `AUA-C18a`: accepted source/evidence produces an
  `InventoryCandidateEvidenceSet` for Inventory validation. Inventory owns
  discovery and validation only.
- `AUA-C18b`: Inventory validation produces an
  `InventoryValidatedCandidateEvidenceSet` for ontology handoff. Validation
  failure blocks handoff; pass proves candidate fitness only.
- `AUA-C19`: ontology review consumes an Inventory-validated candidate EvidenceSet
  and may produce a non-authoritative `OntologyCandidate`.
- `AUA-C21`: operation-specific effect-owner/gate selection and the effect runtime
  are `ABSENT`; an evaluator can never supply any of them. This path remains
  excluded from v0.

The knowledge lifecycle is:

```text
MemoryIntakeRequest
→ provider review
→ AcceptedSourceChange or ProviderAdmittedEvidence
→ InventoryCandidateEvidenceSet
→ InventoryValidatedCandidateEvidenceSet
→ OntologyCandidate
→ authority-kind-specific named owner and selector
→ AuthorityDecision
→ PromotionRecordCompatibleTransition
→ CanonicalAuthorityArtifact
→ optional GovernedProjection
```

Inventory validation is handoff fitness, not canonical admission, authority, or
promotion. A transition record is not canonical authority; a projection is not its
source.

## Proposed immutable fixture payload

Proposed future path: `fixtures/aua-local-fixture-0.1.0.json`. UTF-8 string fields
include the displayed final newline. SHA-256 values are over exactly those bytes.
The parent mechanically rechecked the byte lengths and hashes in this section.

```json
{
  "schema": "aua.local-fixture@0.1.0",
  "identity": {
    "threadId": "THREAD-0001",
    "otherThreadId": "THREAD-OTHER",
    "parentRunId": "RUN-PARENT-0001",
    "actionA": "ACT-A-0001",
    "actionB": "ACT-B-0001",
    "runA": "RUN-A-0001",
    "runB": "RUN-B-0001"
  },
  "sources": {
    "SRC-TRAVEL": {
      "bytes": "Travel by rail only.\n",
      "length": 21,
      "sha256": "d1254ac0d209cb33cd7cf2649dfd01a8539eccf4951d194ebb8342e143e5b842"
    },
    "SRC-WORKSPACE": {
      "bytes": "Workspace is quiet and closes at 18:00.\n",
      "length": 40,
      "sha256": "4d46a65b30bffa794522ca98bd70df5e9c3afc953c62d4d83bd6e615beeed64e"
    }
  },
  "handlesBefore": [
    "H-QUIET@r1=quiet workspace",
    "H-RAIL@r1=rail only",
    "H-LATE@r1=late-night work allowed"
  ],
  "contextBefore": {
    "bytes": "turn=T1\nselected=H-QUIET,H-RAIL,H-LATE,SRC-TRAVEL,SRC-WORKSPACE\nexcluded=\nhandle:H-QUIET=quiet workspace\nhandle:H-RAIL=rail only\nhandle:H-LATE=late-night work allowed\nsource:SRC-TRAVEL=Travel by rail only.\nsource:SRC-WORKSPACE=Workspace is quiet and closes at 18:00.\n",
    "length": 267,
    "sha256": "c9ad07cc7d5063297b48394d44f5b7206bc9c4692e0e5a949fd9a2bf66d8820f"
  },
  "contextAfterTombstone": {
    "bytes": "turn=T5\nselected=H-QUIET,H-RAIL,SRC-TRAVEL,SRC-WORKSPACE\nexcluded=H-LATE@r2:tombstoned\nhandle:H-QUIET=quiet workspace\nhandle:H-RAIL=rail only\nsource:SRC-TRAVEL=Travel by rail only.\nsource:SRC-WORKSPACE=Workspace is quiet and closes at 18:00.\n",
    "length": 242,
    "sha256": "577f2bd79d53503170dd3cdd2777e75bb608593aab4b4fd13a19897f5121acf6"
  },
  "resultBefore": {
    "bytes": "Use rail travel; choose the quiet workspace; late-night work is allowed.\n",
    "length": 73,
    "sha256": "d366710327212b54afc9b13e88c68e0ad034a74ebcf652b6cda3580020b6f486"
  },
  "resultAfter": {
    "bytes": "Use rail travel; choose the quiet workspace; do not schedule late-night work.\n",
    "length": 78,
    "sha256": "5245b8e31ae35e425d2b2ccf0ae6829ec48838674f2633e5b1b71cc602af5019"
  },
  "routeConfig": {
    "bytes": "route-config@0.1.0\ninline-grounded:T1\nstrategy:T2\naddressed:T3A\ninline:T3P\nconsume:T4\ncorrect:T5\nblock-missing:T6\n",
    "length": 114,
    "sha256": "f68969e64b04e0850374d47ab5ba046cec017820d746dda52799a0d2705ae366"
  },
  "turns": {
    "T1": {
      "bytes": "Plan a quiet two-day writing retreat using my explicit preferences and the two supplied records.\n",
      "sha256": "72e7014b03aac2e0c01e17851c7833afb56f0535aa8628e1ad83d161af2700a3",
      "route": "INLINE_GROUNDED"
    },
    "T2": {
      "bytes": "Run two independent checks: A travel constraints, B workspace suitability.\n",
      "sha256": "a62ead0399f172f2dedd66522250065d3ec1beb6fc975a9328e617b43a5f6976",
      "route": "STRATEGY_PROPOSAL"
    },
    "T3P": {
      "bytes": "While they run, summarize the grounded retreat plan in one sentence.\n",
      "sha256": "1fd5cc5aa14a30ad52e30fe2caeac635c463de62def85746e4d0bf9f6ece5c6e",
      "route": "INLINE_PARENT_CONTINUATION"
    },
    "T3A": {
      "bytes": "A: rail only.\n",
      "sha256": "7a061b4d7efaedd2113bf0c17781c869495d8a802f21a4bf03ae50bbbbf8deff",
      "route": "ADDRESSED_REVISION"
    },
    "T4": {
      "bytes": "Attach only B.\n",
      "sha256": "a12e79224318b5a9eb68328a656f2d171addfbf6aebccd7744835e348f6b692c",
      "route": "RESULT_CONSUMPTION"
    },
    "T5": {
      "bytes": "Draft a session correction: remove late-night work.\n",
      "sha256": "29401ce5e1bb041340802fc95ca34c01b6a3a246cd65d7c4af412b180d7a1937",
      "route": "HANDLE_TOMBSTONE_AND_LOCAL_INTAKE_DRAFT"
    },
    "T6": {
      "bytes": "Publish the result with host.operation.not-installed.\n",
      "sha256": "69791577a2d133ab4e54f38e58e96b65f2fc2718a1896dd5d483cf11a5090e05",
      "route": "CAPABILITY_GAP_BLOCK"
    }
  },
  "snapshots": {
    "A": {
      "bytes": "parentRunId=RUN-PARENT-0001\nownerRunId=RUN-A-0001\nactionId=ACT-A-0001\nmarker=MARKER-A\ncontextDigest=c9ad07cc7d5063297b48394d44f5b7206bc9c4692e0e5a949fd9a2bf66d8820f\ntask=check travel constraints\n",
      "sha256": "f80a4f48909078b7cc04b5f8666e47a34fdcfd1bb27b47f4b8427802076652f1"
    },
    "B": {
      "bytes": "parentRunId=RUN-PARENT-0001\nownerRunId=RUN-B-0001\nactionId=ACT-B-0001\nmarker=MARKER-B\ncontextDigest=c9ad07cc7d5063297b48394d44f5b7206bc9c4692e0e5a949fd9a2bf66d8820f\ntask=check workspace suitability\n",
      "sha256": "d2541bcf0e8472ce511a99e0b634c85656fe9aa0274ace2c9e155dde2745946c"
    }
  },
  "proposalInitial": {
    "bytes": "{\"proposalId\":\"PROP-0001\",\"roles\":[{\"actionId\":\"ACT-A-0001\",\"ownerRunId\":\"RUN-A-0001\",\"task\":\"check travel constraints\"},{\"actionId\":\"ACT-B-0001\",\"ownerRunId\":\"RUN-B-0001\",\"task\":\"check workspace suitability\"}],\"parallel\":true,\"forbiddenEffects\":[\"memory-write\",\"publish\"]}\n",
    "sha256": "838866e8d450e79ffb66c2866f9543752a5c27e99ce83b33c21bdfebdb93a2a6"
  },
  "proposalEdited": {
    "bytes": "{\"proposalId\":\"PROP-0001\",\"roles\":[{\"actionId\":\"ACT-A-0001\",\"ownerRunId\":\"RUN-A-0001\",\"task\":\"check rail travel constraints\"},{\"actionId\":\"ACT-B-0001\",\"ownerRunId\":\"RUN-B-0001\",\"task\":\"check workspace suitability\"}],\"parallel\":true,\"forbiddenEffects\":[\"memory-write\",\"publish\"]}\n",
    "sha256": "4d228e5ba8cd85d5f5c199a810ba4207dc28a445ec667558289df283c8840502"
  },
  "dispatch": {
    "bytes": "{\"dispatchId\":\"DISPATCH-0001\",\"proposalId\":\"PROP-0001\",\"actions\":[\"ACT-A-0001\",\"ACT-B-0001\"],\"parallel\":true}\n",
    "sha256": "5486389debd693c2311230343636385d10887dd3d0a9c08a188e37fefb41aedc"
  },
  "approval": {
    "bytes": "{\"approvalId\":\"APPROVAL-0001\",\"proposalDigest\":\"4d228e5ba8cd85d5f5c199a810ba4207dc28a445ec667558289df283c8840502\",\"dispatchDigest\":\"5486389debd693c2311230343636385d10887dd3d0a9c08a188e37fefb41aedc\",\"decision\":\"approve\"}\n",
    "sha256": "27f041e1a8579b03d8fab9508932f3b2bd28e3a34ac172a58a040c5929d356f4"
  },
  "addressedRevision": {
    "bytes": "ownerRunId=RUN-A-0001\nrevisionId=REV-A-0001\nbaseSnapshotDigest=f80a4f48909078b7cc04b5f8666e47a34fdcfd1bb27b47f4b8427802076652f1\nanswer=rail only\n",
    "sha256": "1601d1c790ad5d7042eb43b732221826148a5178ed789dfd93404c2a482afe34"
  },
  "join": {
    "inputBytes": "{\"joinId\":\"JOIN-0001\",\"inputs\":[{\"actionId\":\"ACT-A-0001\",\"ownerRunId\":\"RUN-A-0001\",\"terminal\":\"blocked\",\"handle\":\"BLOCK-A-001\"},{\"actionId\":\"ACT-B-0001\",\"ownerRunId\":\"RUN-B-0001\",\"terminal\":\"done\",\"handle\":\"ART-B-001\"}]}\n",
    "inputSha256": "2b79c8ea88ff94ece225cb12d9403291007ae048dd1d8df7d9b34470b00c771c",
    "outputBytes": "{\"joinId\":\"JOIN-0001\",\"status\":\"blocked_with_consumable_result\",\"blocked\":[\"BLOCK-A-001\"],\"consumable\":[\"ART-B-001\"]}\n",
    "outputSha256": "4f18322e1d2cc287c8f525c05273a9b6cd7e09468dd46fc48f099f04d3d00b1e",
    "receiptBytes": "{\"receiptId\":\"JOIN-RECEIPT-0001\",\"joinInputDigest\":\"2b79c8ea88ff94ece225cb12d9403291007ae048dd1d8df7d9b34470b00c771c\",\"joinOutputDigest\":\"4f18322e1d2cc287c8f525c05273a9b6cd7e09468dd46fc48f099f04d3d00b1e\"}\n",
    "receiptSha256": "29172edf63ea64852fc365d55f68df323632ef0946967978ae832503529da58f"
  },
  "commands": {
    "consumeBytes": "{\"commandId\":\"CONSUME-0001\",\"operation\":\"attach\",\"artifactRef\":\"ART-B-001\",\"targetInteractionId\":\"T4\"}\n",
    "consumeSha256": "34b81ef7422132286f35a45dc2283f85eefd1b8c47bb3d4c6afff17c77e24eed",
    "tombstoneBytes": "{\"commandId\":\"TOMBSTONE-0001\",\"handleId\":\"H-LATE\",\"fromRevision\":1,\"toRevision\":2,\"posture\":\"tombstoned\"}\n",
    "tombstoneSha256": "f35e92a4b78735ae102d12b8c6a7e18bcec86e3566622bf89c82b89d76d33308",
    "intakeDraftBytes": "{\"intakeId\":\"MemoryIntakeDraft-001\",\"posture\":\"local_draft\",\"scopeTag\":\"session\",\"sourceRef\":\"H-LATE\",\"requestedChange\":\"remove late-night work\",\"trustedWriteRequested\":false}\n",
    "intakeDraftSha256": "422020627e5d8796a4028da0c6cc53bfa4384651d067d458060fb546a11f8988"
  },
  "reloadSeed": {
    "bytes": "{\"schema\":\"aua.reload-seed@0.1.0\",\"threadId\":\"THREAD-0001\",\"activeThreadId\":\"THREAD-OTHER\",\"parentRunId\":\"RUN-PARENT-0001\",\"runs\":[{\"ownerRunId\":\"RUN-A-0001\",\"state\":\"blocked\",\"handle\":\"BLOCK-A-001\"},{\"ownerRunId\":\"RUN-B-0001\",\"state\":\"done\",\"handle\":\"ART-B-001\"}],\"notifications\":[{\"id\":\"NOTE-A-001\",\"read\":true},{\"id\":\"NOTE-B-001\",\"read\":false}],\"counters\":{\"registration\":1,\"spawn\":2,\"ownerCall\":2,\"announcement\":2,\"duplicateAnnouncement\":0,\"attachment\":0,\"memoryWrite\":0,\"effect\":0,\"evaluatorCall\":0}}\n",
    "sha256": "5251f2a1ce9358abf89a9a1a3f0a25a7c6e547287a31a93935296ef82d426162"
  }
}
```

Every RouteDecision is minified one-line JSON plus final newline, with keys
`decisionId,turnId,turnDigest,configDigest,mode`, and
`decisionId = "ROUTE-" + turnId`. Its values come from `turns` and
`routeConfig.sha256`.

| Turn | Decision record SHA-256 |
|---|---|
| T1 | `0c8e86a5a00818fe3fbb67fe23d3568aabb60d4d6ffe2715658c9314937eca63` |
| T2 | `9e559ebcd866bf53dafd35f860c620d00d8b771d265fac70e35d717150b0b8ad` |
| T3P | `a742d617bf481004e3df0270cedded9cb37743cad7d00080253e6914b7e535e8` |
| T3A | `319b68f1709d5cca11d0e2d1023e994ab23455005d85c9c48ea4567409e66386` |
| T4 | `9c481b33c20152cafbd7dacd2dccc74c87438ccb0a75313e0aba91ad0fc3deea` |
| T5 | `dc8df635c14204a2e37a9af07e5d19197705e96f169df507e669b2566880e2a5` |
| T6 | `3fdea23c02175a4ce1f1d1844c42feeb376173e0bce6a56b6dab1e885401db64` |

## Ordered parent/child event protocol

Each canonical JSONL event is minified, has one final newline, and uses key order:

```text
schema,eventId,seq,orderKey,kind,parentRunId,ownerRunId,actionId,payload
```

`schema` is `aua.event@0.1.0`; `parentRunId` is `RUN-PARENT-0001`;
`orderKey` is the six-digit zero-padded sequence. In the table, A/A means
`RUN-A-0001`/`ACT-A-0001`, and B/B means
`RUN-B-0001`/`ACT-B-0001`. Full digests are the values in the fixture above.
The resulting 20-line JSONL is 4,774 bytes with SHA-256
`5bb37e0f6d0f56be9651924fe54bc7378bab3564da434daccc4ae001a5e91191`;
the parent mechanically rechecked both values.

| Event | Seq/key | Kind | Owner/action | Exact payload |
|---|---:|---|---|---|
| `EVT-001` | `1/000001` | `parent.registered` | null/null | `{"threadId":"THREAD-0001"}` |
| `EVT-002` | `2/000002` | `child.spawn_requested` | A/A | `{"snapshotDigest":"f80a4f48909078b7cc04b5f8666e47a34fdcfd1bb27b47f4b8427802076652f1"}` |
| `EVT-003` | `3/000003` | `child.accepted` | A/A | `{}` |
| `EVT-004` | `4/000004` | `child.spawn_requested` | B/B | `{"snapshotDigest":"d2541bcf0e8472ce511a99e0b634c85656fe9aa0274ace2c9e155dde2745946c"}` |
| `EVT-005` | `5/000005` | `child.accepted` | B/B | `{}` |
| `EVT-006` | `6/000006` | `child.running` | A/A | `{}` |
| `EVT-007` | `7/000007` | `child.running` | B/B | `{}` |
| `EVT-008` | `8/000008` | `parent.turn_accepted` | null/null | `{"turnId":"T3P","marker":"MARKER-P-LATE"}` |
| `EVT-009` | `9/000009` | `child.attention_requested` | A/A | `{"attentionRef":"ATT-A-001"}` |
| `EVT-010` | `10/000010` | `child.input_revision_addressed` | A/A | `{"revisionId":"REV-A-0001","revisionDigest":"1601d1c790ad5d7042eb43b732221826148a5178ed789dfd93404c2a482afe34"}` |
| `EVT-011` | `11/000011` | `child.input_revision_accepted` | A/A | `{"revisionId":"REV-A-0001"}` |
| `EVT-012` | `12/000012` | `child.artifact_published` | B/B | `{"artifactRef":"ART-B-001"}` |
| `EVT-013` | `13/000013` | `child.done` | B/B | `{"artifactRef":"ART-B-001"}` |
| `EVT-014` | `14/000014` | `child.blocked` | A/A | `{"blockerRef":"BLOCK-A-001"}` |
| `EVT-015` | `15/000015` | `join.reduced` | null/null | `{"receiptId":"JOIN-RECEIPT-0001","receiptDigest":"29172edf63ea64852fc365d55f68df323632ef0946967978ae832503529da58f"}` |
| `EVT-016` | `16/000016` | `thread.switched` | null/null | `{"from":"THREAD-0001","to":"THREAD-OTHER"}` |
| `EVT-017` | `17/000017` | `reload.requested` | null/null | `{"seedDigest":"5251f2a1ce9358abf89a9a1a3f0a25a7c6e547287a31a93935296ef82d426162"}` |
| `EVT-018` | `18/000018` | `reconciliation.observed` | A/null | `{"state":"blocked","handle":"BLOCK-A-001"}` |
| `EVT-019` | `19/000019` | `reconciliation.observed` | B/null | `{"state":"done","handle":"ART-B-001"}` |
| `EVT-020` | `20/000020` | `reload.completed` | null/null | `{"activeThreadId":"THREAD-OTHER","spawnDelta":0,"effectDelta":0,"duplicateAnnouncementDelta":0}` |

Reconciliation observes A as blocked with `BLOCK-A-001` and B as done with
`ART-B-001`; active thread stays `THREAD-OTHER`. Hydration performs no owner call,
spawn, effect, read-state mutation, or duplicate announcement and never reconstructs
terminal truth from cards or transcript text.

## Counter checkpoints

| Checkpoint | registration | spawn | ownerCall | addressed A/B | announcement | duplicate | attachment | intakeDraft | trustedWrite | effect | evaluatorCall |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Initial | 0 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Preview/edit/stale approval | 0 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Valid approval registered | 1 | 0 | 0 | 0/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| After `EVT-005` | 1 | 2 | 2 | 0/0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| After `EVT-011` | 1 | 2 | 2 | 1/0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| After `EVT-015` | 1 | 2 | 2 | 1/0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| After reload | 1 | 2 | 2 | 1/0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| After T4 attach | 1 | 2 | 2 | 1/0 | 2 | 0 | 1 | 0 | 0 | 0 | 0 |
| After T5 | 1 | 2 | 2 | 1/0 | 2 | 0 | 1 | 1 | 0 | 0 | 0 |
| After T6 gap block | 1 | 2 | 2 | 1/0 | 2 | 0 | 1 | 1 | 0 | 0 | 0 |

T4 attachment changes neither A, B, the join receipt, notification state,
parent/child snapshots, nor memory/effect counts. T5 changes composed-context and
deterministic-result digests while trusted writes remain zero.

## Fixture adapters and commands

The exact proposed local adapter identities are:

- `FixtureThreadInteractionAdapter@0.1`
- `FixtureHandleSourceAdapter@0.1`
- `FixtureSnapshotComposer@0.1`
- `FixtureDeterministicRouteAdapter@0.1`
- `FixtureProposalApprovalRegistrar@0.1`
- `FixtureTwoChildHostAdapter@0.1`
- `FixtureLifecycleJoinReducer@0.1`
- `FixtureReloadReconciler@0.1`
- `FixtureResultConsumptionAdapter@0.1`
- `FixtureLocalIntakeDraftAdapter@0.1`

They are future fixture adapters, not current production owners. Proposed future
commands, whose paths do not exist and were not run:

```text
node --test tests/augmentor/aua-local-fixture-0.1.0.contract.test.mjs
playwright test tests/augmentor/aua-local-fixture-0.1.0.browser.spec.ts --project=chromium --workers=1
```

## Browser contract

Required selectors:

```text
[data-testid="augmentor-transcript"]
[data-testid="composer-input"]
[data-testid="composer-submit"]
[data-testid="parent-continuation-T3P"]
[data-testid="source-chip"]
[data-testid="source-row-H-QUIET"]
[data-testid="source-row-H-LATE"]
[data-testid="source-row-SRC-TRAVEL"]
[data-testid="strategy-proposal"]
[data-testid="proposal-edit"]
[data-testid="proposal-approve"]
[data-testid="proposal-digest"]
[data-testid="thread-THREAD-0001"]
[data-testid="thread-THREAD-OTHER"]
[data-testid="thread-switch-THREAD-OTHER"]
[data-testid="reload-trigger"]
[data-testid="run-RUN-A-0001"]
[data-testid="run-RUN-B-0001"]
[data-testid="run-status-RUN-A-0001"]
[data-testid="run-status-RUN-B-0001"]
[data-testid="blocker-BLOCK-A-001"]
[data-testid="attention-ATT-A-001"]
[data-testid="attention-input-RUN-A-0001"]
[data-testid="artifact-ART-B-001"]
[data-testid="attach-ART-B-001"]
[data-testid="notification-NOTE-A-001"]
[data-testid="notification-NOTE-B-001"]
[data-testid="notification-read-state"]
[data-testid="knowledge-handle-H-LATE"]
[data-testid="correct-H-LATE"]
[data-testid="tombstone-H-LATE"]
[data-testid="intake-draft-MemoryIntakeDraft-001"]
[data-testid="capability-gap-host.operation.not-installed"]
[data-testid="fixture-counters"]
[data-testid="fixture-event-log"]
[data-testid="focus-sentinel"]
[data-testid="polite-live-region"]
```

The browser journey must assert:

1. T1 exact selected IDs plus before-context and result digests.
2. Immutable source digests and H-LATE posture.
3. T2 route/proposal digest and zero launch counters.
4. Edited proposal digest, stale approval rejection, and zero calls.
5. Exact approval/Dispatch digests and one registration.
6. Two fixed Run identities and `EVT-001`–`EVT-007`.
7. T3P in the parent transcript while child snapshots remain byte-identical.
8. Attention scoped to A; T3A increments A only and restores focus.
9. B Done, A Blocked, exact handles and join receipt, polite non-color-only status.
10. Switch to `THREAD-OTHER` without reparenting or transcript merge.
11. Reload with `EVT-017`–`EVT-020`, unchanged active thread/read state, and zero
    spawn/effect/duplicate deltas.
12. Return to `THREAD-0001` and attach B only; unrelated state is unchanged.
13. Tombstone H-LATE and assert after-context/result digests.
14. One session-local intake draft and zero trusted writes.
15. T6 exact missing-operation block and zero counter deltas.
16. Inspect machine counters/event log; cards alone are insufficient.
17. Keyboard-only visible/restored focus, polite live-region behavior, no reload
    duplicate, and reduced-motion textual equivalence.

Witness posture: `SPECIFIED FUTURE WITNESS; UNIMPLEMENTED AND UNEXECUTED`.

## Fully pinned, unexecuted measurements

For timing, use one process/worker, fixed seed, no network, a monotonic
high-resolution clock, 100 unrecorded warm-ups, and 1,000 recorded samples per
operation. Nearest-rank percentile means sorting ascending and selecting
`ceil(p × 1000) - 1`; delete no outliers. Report min, median, p95, max, failures,
timeouts, runtime/environment lock, and fixture digest.

| Operation | Fixed corpus | Target |
|---|---|---:|
| Provider lookup | Alternate the exact two SourceRecords | Hard timeout `800 ms` |
| Bounded composition/result | Alternate exact before/after contexts | Warm p95 `≤20 ms` |
| Route classification | Cycle T1, T2, T3P, T3A, T4, T5, T6 under the fixed config | Warm p95 `≤50 ms` |
| Proposal projection | Exact initial/edited pair to committed digest text | p95 `≤100 ms` |
| Approval acknowledgement | Approval click to registrar acknowledgement before host progress | p95 `≤250 ms` |

v0 has zero model calls and no tokenizer; byte lengths and SHA-256 values govern.
A later model lane requires a separate lock naming provider, model revision,
tokenizer implementation/version/vocabulary digest, prompt-template digest, and
sample corpus.

v0 uses no graph database. The future projection bound is 24 nodes, 48 edges, one
hop by default/two hard, and at most eight session handles. Serialize canonical
UTF-8 JSON after derived partition serialization and before compression/transport.
A partition is all derived index/projection, event, reload, and notification state
for exactly one `threadId`; target size is `≤25 MB`. Report serialized bytes,
objects, node/edge counts, and corpus digest.

`ATTENTION-CORPUS-001` is 1,000 deterministic one-turn synthetic sessions:
001–800 inline/no card; 801–990 routed/card/no clarification; 991–1000 routed/card
plus one clarification. Observe from submit through terminal UI stabilization.
Targets: cards ≤200/1,000; clarifications ≤10/200 routed attempts; ≤2 extra actions
and exactly one approval per consequential launch; ≤1 announcement per meaningful
transition and zero replay announcements. This is a proposed synthetic corpus, not
real-user evidence.

## Final verdict and residue

| Claim | Verdict |
|---|---|
| Candidate architecture | `GO — BUILD_FROM_OWNED + EXPLICIT ABSENT ADAPTERS` |
| Current v0 | `NO` |
| Future fixture contract | `SPECIFIED; NOT IMPLEMENTED OR EXECUTED` |
| Production integration | `BLOCKED — adapters absent` |
| Executed vertical/browser witness | `NO_WITNESS_CURRENT` |
| Evaluator implementation | `KILL` |
| Evaluator research contract | `UNWITNESSED CANDIDATE` |
| Evaluator supplies effect gate/owner/runtime | `KILL` |
| Generic memory owner | `KILL — owner selection required` |
| Inventory-validated candidate as canonical/promoted | `KILL` |
| Durable correction/forgetting | `BLOCKED — trusted provider absent` |
| End-to-end authority promotion | `BLOCKED — owner/selector/schemas unresolved` |
| Transition record as authority | `KILL` |
| Public leakage of private authority semantics | `KILL` |

Open selections remain: durable index/projection owner; production route/proposal/
approval owners; Orchestrate-to-Resonant bindings; trusted provider; authority-kind
resolver, named owner, selector, registrar, writer, and generator; decision/
transition identities and schemas; evaluator applicability/catalog owner; independent
effect owner/gate/runtime; cancellation, late-result, and notification owners.

## Repair closure

| Reviewer requirement | Closure |
|---|---|
| Inventory terminology | Candidate and validated-candidate objects are distinct; neither is canonical/promoted |
| C21 effect ownership | Owner/gate selection and runtime explicitly absent and independent of evaluator |
| Literal bytes/hashes | Sources, contexts, results, turns, snapshots, proposal, Dispatch, approval, revision, join, commands, and reload seed specified |
| Route decisions | Fixed key order, identity rule, values, and digests |
| Event protocol | Fixed schema/key order, event order/payloads, byte length, and digest |
| Counters/invariants | Before/after checkpoints and unchanged-state requirements |
| Browser coverage | Selectors and step-to-observation assertions |
| Timing | Warm-up/sample/percentile/corpora and targets pinned |
| Token/model | v0 none; later lock requirement explicit |
| Storage/partition | Canonical boundary and one-thread partition explicit |
| Attention | Exact synthetic cohort, window, denominators, and targets |
| Honesty | All proposed artifacts remain unimplemented/unexecuted |

Remaining uncertainty requires owner decisions or new executable evidence, not
another interpretation of the explorer reports.
