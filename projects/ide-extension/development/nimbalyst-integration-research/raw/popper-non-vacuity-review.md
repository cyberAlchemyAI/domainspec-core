# Popper Non-Vacuity Review

**Dispatch:** `2026-07-11-nimbalyst-integration-research`
**Identity:** Popper, Karl
**Gate applied:** NON-VACUITY only
**Pinned upstream:** `Nimbalyst/nimbalyst@c8ca207c6004653ba2df3d81e06133ce2e9fad3d`
**Result:** **16 KILL, 0 ADMIT**

## Gate

A candidate passes only if the reviewed evidence identifies a smallest credible
local witness with all five of these properties:

1. an exact interface required by a present local consumer;
2. a closed dependency set available in the present layer;
3. an authority boundary consistent with kernel-owned approval, durable state,
   artifacts, outcome adjudication, and receipts;
4. an executable acceptance test that distinguishes the candidate from existing
   local behavior; and
5. a named mechanism by which the candidate reduces **total** development time,
   including adaptation, negative tests, provenance, upgrades, and abandonment.

`Useful precedent`, `defer`, `future program`, and `may avoid redesign` do not pass.
A hypothetical future trigger is not a present witness. Local re-expression does
not count as Nimbalyst integration unless an exact Nimbalyst-derived mechanism
removes work that the local owners do not already require.

The pinned checkout was verified at the stated commit. Its evidence is real but
does not cure local non-vacuity: the read-only host still implements the broad
`EditorHost` by mutation no-ops and secret-shaped storage
(`packages/extension-sdk/src/createReadOnlyHost.ts:25-119`); the agent protocol
carries workspace, permission, MCP, environment, and tool policy
(`packages/extension-sdk/src/agents/AgentProtocol.ts:64-94`); and its host keeps
provider permission authoritative while exposing raw-log persistence, key lookup,
workspace writes, and MCP registration
(`packages/extension-sdk/src/agents/AgentProtocolHost.ts:45-62,101-219`).

## Exact Disposition Table

| ID | Exact disposition | Smallest witness demanded | Why the witness is not credible now | Typed negative bank |
| --- | --- | --- | --- | --- |
| NIM-C01 | **KILL** | `EvidenceHost = {artifact_ref, content, theme, readOnly}` consumed by one selected renderer; dependencies: supplied artifact plus theme only; no save/filesystem/network/approval/receipt; test renders and proves forbidden ports absent; reducer: avoid renderer-specific host duplication. | No selected renderer requires more than the four-value record, and the proposed interface adds subscriptions, dirty state, and save vocabulary without a consumer. The local browser host is already chosen. | `NEG-NV/no-present-consumer` |
| NIM-C02 | **KILL** | `createFixtureHost(fixedArtifact)` used by a selected editor test; dependencies: C01 plus an editor; immutable supplied updates only; test proves render/no-write/no-network; reducer: replace duplicated fixture setup. | C01 fails and no editor witness is selected. An ordinary fixture object is smaller than adapting upstream behavior, whose no-op mutation and storage surface must be removed. | `NEG-NV/dependency-without-parent` |
| NIM-C03 | **KILL** | One named local contribution rejected or unrepresentable by the current manifest contract; dependencies: the existing Draft 2020-12 owner and runtime validator; registry remains authority; hostile fixture distinguishes the new rule; reducer: reuse a missing validation case. | No contribution is named. The present defect is failure to enforce the existing local schema, not absence of a Nimbalyst-shaped manifest or validator pattern. | `NEG-NV/repair-misattributed-as-integration` |
| NIM-C04 | **KILL** | One externally consumed local package with an exact export list; dependencies: package build, tarball, minimal consumer; packaging only; test pack/import/missing-export; reducer: replace bespoke package checks. | `projects/ide-extension` is private and has no separately packaged public contract or consumer. The proposed test has nothing to test. | `NEG-NV/no-target-artifact` |
| NIM-C05 | **KILL** | Two admitted provider-native formats, one repeated projection requirement, and `project(raw[]) -> canonical[]`; dependencies: immutable raw artifacts, redaction, hashing, two fixture corpora; projection has no outcome authority; deterministic replay test; reducer: remove duplicated parsers. | The only selected lane is one fake stdio `observe` tool. No second format, duplicated parser, or present canonical-view query exists. Raw evidence hashing is already required locally without this candidate. | `NEG-NV/threshold-not-met` |
| NIM-C06 | **KILL** | A fake stdio adapter ambiguity that cannot be represented by local `describe/prepare/run/collect/interrupt/inspect`; exact additional event union; dependencies: existing envelope plus fake process; kernel remains sole state/receipt owner; ambiguity-specific test; reducer: remove duplicated provider adapters. | The local six-verb interface already exists, and the first witness has one `observe` result rather than multiple provider adapters. Adding Nimbalyst event tags creates schema and tests but removes no present work. | `NEG-NV/local-precedent-already-owns-interface` |
| NIM-C07 | **KILL** | One materialized, hash-validated before/after pair and a named decision plain links cannot support; dependencies: repaired artifact resolution, approval attribution, persistence, schema enforcement; presentation only; stale/hash/accessibility/no-side-effect tests; reducer: measurably shorten review. | The reviewed kernel has no resolvable after artifact. The dossier names neither a present decision nor a measured cost of plain artifact links. A deferred viewer is not a witness. | `NEG-NV/missing-required-state` |
| NIM-C08 | **KILL** | One recurring query with baseline latency and exact read model `{owner-qualified task_ref, envelope_id, run_id, artifact_ref, receipt_id}`; dependencies: canonical resolvers; no write-back/status ownership; broken/foreign/no-write tests; reducer: measured navigation-time reduction. | No recurring query, baseline, consumer, or owner-qualified resolver is identified. A seeded join proves implementation possibility, not development-time reduction. | `NEG-NV/no-measured-user-job` |
| NIM-C09 | **KILL** | One first consumer and the minimal packet fields it actually reads; dependencies: local artifact/hash owner; context only; required-field/hash/non-promotion tests; reducer: eliminate demonstrated context reconstruction. | Nimbalyst avoids no schema-authority work, and no consumer uses every proposed required field. The packet is already locally owned by prior research; Nimbalyst is corroboration only, not an integration reducer. | `NEG-NV/no-upstream-contribution` |
| NIM-C10 | **KILL** | Two descriptor producers duplicating normalization and `parse(suppliedRedactedDescriptor)`; dependencies: local schema only; zero ambient I/O/custody; hostile descriptor and zero-access spies; reducer: delete duplicated parser logic. | There is one planned descriptor producer and no duplicated normalization. Existing schema enforcement must be repaired first. The cited upstream services increase extraction work because safe logic must be separated from custody I/O. | `NEG-NV/duplication-not-observed` |
| NIM-C11 | **KILL** | One admitted browser `observe` action with an exact Nimbalyst-derived field absent from destination-native Playwright/MCP vocabulary; dependencies: later browser adapter; kernel approval/receipt authority; deny navigation/mutation test; reducer: avoid a demonstrated design/test task. | The dossier explicitly supplies no implementation witness and names no surviving Nimbalyst term. The current L0.5 witness excludes Chrome and live browsers. | `NEG-NV/vocabulary-without-survivor` |
| NIM-C12 | **KILL** | A present resume-capable adapter exposing `requested_resume_ref`, `observed_resume_ref`, `interrupt_requested`, `termination_observed`, and residue; dependencies: process custody and repaired run typestate; kernel adjudicates; mismatch/timeout test; reducer: prevent a concrete ambiguity in that adapter. | No real provider or resume token is admitted; the fake MCP witness does not resume sessions. Timeout can be tested under the already-owned local run lifecycle. Git residue belongs to an unselected future adapter. | `NEG-NV/failure-state-without-trigger` |
| NIM-C13 | **KILL** | A bounded imported runtime interface that retains a concrete implementation after all permission/session/process/storage authority is removed; closed dependency graph; kernel-only authority; hostile lifecycle suite; positive total-cost comparison. | No such residue is identified. Removing the authority-bearing graph leaves locally expressible vocabulary already evaluated in C05/C06/C12, not a reusable runtime. | `NEG-NV/subtraction-leaves-no-unit` |
| NIM-C14 | **KILL** | One currently required offline operation with a bounded CWD/env/HOME and no imported durable state; exact adapter port; process/Git/storage authority external to kernel; custody/recovery tests; positive total-cost comparison. | No operation is required in L0/L0.5. The cited services import PTY, Git, Electron, IPC, database, migration, and recovery obligations whose total cost is necessarily larger than the current witness. | `NEG-NV/no-current-power-requirement` |
| NIM-C15 | **KILL** | One current local collaboration need plus a complete server/identity/key/custody interface; all client and server dependencies pinned; remote client proposal-only; replay/revocation/conflict tests; positive full-stack cost comparison. | No local need or owner exists, and the pinned MIT checkout explicitly excludes the server behind `wss://sync.nimbalyst.com` (`LICENSING.md:3-8`). The dependency closure is therefore unavailable. | `NEG-NV/open-dependency-closure` |
| NIM-C16 | **KILL** | One current acceptance criterion requiring either zero-egress observability integration or signed update delivery; exact event/feed interface; consent/signing/rollback dependencies; no governance-authority conflation; compromise/rollback tests; positive total-cost comparison. | Neither telemetry nor executable updating advances the current kernel/admission witness. Both add independent egress or supply-chain programs with no present consumer. | `NEG-NV/unrelated-capability` |

## Why C06 And C12 Still Die

These are the strongest-looking candidates, so their negatives need to be
falsifiable rather than rhetorical.

For C06, the current owner already defines `describe`, `prepare`, `run`, `collect`,
`interrupt`, and `inspect` (`projects/ide-extension/ARCHITECTURE.md:102-115`). The
selected L0.5 witness is one offline stdio adapter with one `observe` tool and no
provider (`ARCHITECTURE.md:77-88`; MCP findings `:45-61`). A counterexample that
would reopen C06 is a second admitted agent adapter whose implementation duplicates
the same event correlation or cleanup state, together with a failing fixture that
the existing envelope protocol cannot express.

For C12, upstream genuinely fails loud on resume mismatch, but the local selected
witness has no resume operation. The accepted local review instead requires repair
of the existing ID-addressed lifecycle and a distinct invocation before L0.5
promotion (`architecture-review-2026-07-10/findings.md:171-182`). A counterexample
that would reopen C12 is an admitted resume-capable adapter and a fixture showing
that its requested and observed identities can diverge under the existing local
state vocabulary.

## Required Synthesis Revisions

The synthesis must be revised before it can support an integration decision:

1. Replace the primary disposition count with `KILL: 16`; do not count conditional
   future outcomes as present dispositions.
2. Add a NON-VACUITY rule stating that `precedent`, `defer`, and `build-from-owned`
   are research classifications, not admitted integration candidates.
3. For NIM-C01, remove the claim that editor-host naming avoids work until a
   selected renderer demonstrates a need beyond the four-value record.
4. For NIM-C02, bank the missing selected editor and failed C01 dependency; do not
   retain a standing instruction to port `createReadOnlyHost`.
5. For NIM-C03, classify hostile schema fixtures as part of AR-CAND-008 repair,
   with no Nimbalyst credit absent one uniquely useful copied case.
6. For NIM-C04, require a named public package and consumer before reopening.
7. For NIM-C05, preserve the two-provider trigger as the typed reopening condition,
   not as an adapted candidate.
8. For NIM-C06, acknowledge that the local envelope already owns the lifecycle
   verbs and require a concrete unrepresentable ambiguity before adding event tags.
9. For NIM-C07, convert `defer` to a typed negative keyed to missing materialized
   after-state evidence and a missing user decision beyond artifact links.
10. For NIM-C08, require a recurring query, baseline latency, and canonical resolver
    inventory before reopening.
11. For NIM-C09, remove Nimbalyst from the candidate mechanism. Retain it, if useful,
    only as product corroboration in provenance for the separately owned local work.
12. For NIM-C10, retain the second-producer trigger as a typed negative and route
    present validation work to the existing schema-enforcement repair.
13. For NIM-C11, require one surviving Nimbalyst-specific term after comparison with
    Playwright/MCP; otherwise remove the candidate.
14. For NIM-C12, split resume mismatch, interruption observation, and Git residue
    into adapter-specific future hypotheses. None is admitted without its triggering
    adapter.
15. Keep NIM-C13, NIM-C14, NIM-C15, and NIM-C16 as kills, but bank their precise
    negative types: no residual unit, no current power requirement, unavailable
    dependency closure, and unrelated capability respectively.
16. Replace every `development work avoided` statement with either measured local
    duplication or an explicit `none demonstrated`; speculative redesign avoidance
    is not evidence of reduced total development time.

## Banked Result

This review does not claim that the ideas are false or permanently useless. It
claims the narrower, testable result that **none is presently a credible Nimbalyst
integration unit**. Reopening requires the exact counter-witness named in the table;
until then, implementation, adaptation, or promotion would outrun the evidence.
