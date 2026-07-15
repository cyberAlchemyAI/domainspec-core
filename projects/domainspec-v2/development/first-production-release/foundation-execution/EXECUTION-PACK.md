# Execution Pack: DomainSpec v2 Foundation Execution

## Planning Controls

| Field | Value |
|---|---|
| planningGateStatus | pass for selected `SWU-FPR01-001` preparation only |
| complexity | high |
| baselineWave | W1 |
| activePlanRef | `work-pack/waves/W1-AUTHORITY-BASELINE.md` |
| workPackManifest | `WORK-PACK.md` |
| layeringArtifact | `IMPLEMENTATION-LAYERING.md` |
| specRef | accepted FPR decision + ROADMAP + expected manifest |
| activeLayerWindow | L1 |
| lastPlannedAt | 2026-07-14 |
| readinessProfile | pilot |

## Wave Schedule

| Wave | Task | Selected/ready unit | Entry | Exit | Promotion |
|---|---|---|---|---|---|
| [W0](work-pack/waves/W0-GUARD-REPAIR.md) | SGRM guard reopen | completed | accepted 006 review receipt + four exact candidates | accepted `SWU-SGRM-007-R1` retry receipt | W1 opened by proof refresh |
| [W1](work-pack/waves/W1-AUTHORITY-BASELINE.md) | FPR-01 | `SWU-FPR01-001` selected | accepted W0 receipt | ratified baseline + mutants | open W2 |
| [W2](work-pack/waves/W2-SUPPORTED-PROFILE.md) | FPR-02 | none | FPR-01 receipt | stable profile digest + negatives | open W3 |
| [W3](work-pack/waves/W3-BUSINESS-SPEC.md) | FPR-03 | none | FPR-02 receipt | accepted direction + total map | open W4 |
| [W4](work-pack/waves/W4-SPEC-PROJECTION.md) | FPR-04 | none | FPR-03 receipt | tiny Sg + separate retraction proof | allow read-only consumer evaluation |

## Execution Protocol

For each SWU:

1. Select exactly one SWU in the current wave.
2. Use Context Builder strict mode to materialize an execution-time pack from its source anchors.
3. Run Decision Gate first when the SWU owns a consequential choice.
4. Constrain writes to the declared paths.
5. Produce the named receipt and acceptance evidence.
6. Run positive and negative validation.
7. Synchronize continuation state only from a verified receipt and only with separate approval.
8. Stop on authority ambiguity, missing input, false-green success, or write-scope expansion.

## Commands by Wave

Commands for future tools are planned interfaces; they become executable only after their owning SWU creates them.

| Wave | Core verification |
|---|---|
| W0 | `npm --prefix projects/domainspec-v2/impl run audit:retired-orchestration`; focused guard test; `npm --prefix projects/domainspec-v2/impl run typecheck` |
| W1 | `node projects/domainspec-v2/development/first-production-release/tools/validate-authority-baseline.cjs --baseline .../authority-baseline.yml --mutants .../fixtures/authority-baseline` |
| W2 | `node projects/domainspec-v2/development/first-production-release/tools/validate-supported-profile.cjs --contract .../product-contract.yml --profile .../supported-profile.yml --pilot-dir .../pilot` |
| W3 | `node projects/domainspec-v2/development/first-production-release/tools/validate-business-spec-map.cjs --manifest .../graphs/business-graph-manifest.json --map .../graphs/b-s-map.json --mutants .../fixtures/business-spec` |
| W4 | `node projects/domainspec-v2/development/first-production-release/tools/verify-spec-projection.cjs --source-manifest .../manifests/spec-source-manifest.json --semantic-manifest .../graphs/semantic-manifest.json --mutants .../fixtures/spec-projection` |

## Ownership Handoffs

```text
Invoke plan
  -> Task Session (review/execute one SWU)
  -> Decision Gate where named
  -> canonical owner review/promotion
  -> independent validation receipt
  -> Craft status synchronization by separate approved action
```

## Current Execution State

- Ready for a later Task Session: `SWU-FPR01-001` only.
- Completed dependency: W0, including accepted `SWU-SGRM-006-R1` and `SWU-SGRM-007-R1` retry receipts.
- Blocked: `SWU-FPR01-002` and every later FPR SWU until their declared predecessors close.
- Authorization: `DEC-DSV2-FPR-W0-PROOF-SYNC` authorizes proof synchronization and selection only; it does not execute `SWU-FPR01-001`.
