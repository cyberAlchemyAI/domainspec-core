# Nimbalyst Integration Research Findings

Dispatch: `2026-07-11-nimbalyst-integration-research`
Writer: van Lamsweerde, Axel
Date: 2026-07-11
Pinned upstream: [`Nimbalyst/nimbalyst@c8ca207c6004653ba2df3d81e06133ce2e9fad3d`](https://github.com/Nimbalyst/nimbalyst/tree/c8ca207c6004653ba2df3d81e06133ce2e9fad3d)

## One-Sentence Answer

**No Nimbalyst implementation or integration unit is admitted now; retain the pinned upstream as product, protocol, failure, and security precedent while local L0 repair and the existing fake, offline L0.5 witness proceed without a Nimbalyst dependency.**

## Evidence Boundary

This finding is revision-pinned, not a claim about current Nimbalyst. The inspected upstream boundary is the client repository at commit `c8ca207c6004653ba2df3d81e06133ce2e9fad3d`; its code is MIT-licensed subject to the license terms ([`LICENSE`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/LICENSE)). The repository itself says that the collaboration server behind `wss://sync.nimbalyst.com` is a **separate project** ([`README.md#building-from-source`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/README.md#building-from-source), [`LICENSING.md`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/LICENSING.md)). That server was not present, pinned, licensed, or inspected. Client MIT status therefore proves neither server source availability nor self-hostability, deployability, custody behavior, or license.

The local evidence boundary is [the explorer transcript](research.md), [the skeptic-revised synthesis](synthesis.md), the [PRECEDENT](raw/rittel-precedent-review.md), [NON-VACUITY](raw/popper-non-vacuity-review.md), and [DEFINITIONAL-SOUNDNESS](raw/quine-definitional-review.md) reviews, and their cited source files. Product behavior that was documented but not exercised remains documentation evidence. No runtime evaluation, compatibility test, dependency audit, server audit, or symbol-level reuse benchmark was performed.

Gate meanings are deliberately separate:

- **Rittel / PRECEDENT** identifies upstream and local ownership. It is positive evidence and never kills a candidate.
- **Popper / NON-VACUITY** asks for a present consumer, closed dependencies, valid authority boundary, distinguishing executable test, and demonstrated total-lifecycle reduction.
- **Quine / DEFINITIONAL-SOUNDNESS** asks whether the proposed unit is distinct rather than a renamed local interface, ordinary engineering technique, or bundled subsystem.
- **Terminal admission** requires a Popper witness. `precedent`, `build-from-owned`, and `defer` are research classifications, not admissions.

## Nimbalyst Map For `ide-extension`

In plain language, Nimbalyst combines several products in one Electron workspace:

1. **Files and visual editors:** files open in specialized editors, with history, tabs, search, and visual red/green review. Every editor sits behind a broad `EditorHost` extension contract ([README](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/README.md), [`editor.ts`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/packages/extension-sdk/src/types/editor.ts)).
2. **Agent sessions:** Codex, Claude Code, and other providers run as searchable, resumable sessions. Provider-native records are retained and projected into a canonical view ([transcript architecture](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/docs/TRANSCRIPT_ARCHITECTURE.md)).
3. **Tasks and navigation:** markdown plans, tracker items, files, sessions, and workstreams are cross-linked so a person can enter the same work from different views ([planning system](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/docs/PLANNING_SYSTEM.md), [`TRACKER_WORKFLOWS.md`](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/docs/TRACKER_WORKFLOWS.md)).
4. **Execution infrastructure:** provider hosts, permissions, MCP configuration, terminal, Git/worktrees, Electron IPC, storage, migrations, telemetry, and updates supply broad application power.
5. **Collaboration and mobile:** MIT client protocol, sync, crypto, and mobile code talk to the separately operated collaboration server; the extension collaboration guide explicitly assigns transport, relay, queues, reconnection, and key rotation to the host ([guide](https://github.com/Nimbalyst/nimbalyst/blob/c8ca207c6004653ba2df3d81e06133ce2e9fad3d/docs/COLLABORATION_GUIDE.md)).

For `ide-extension`, the useful map is therefore **product grammar, not a platform transplant**. Files, sessions, tasks, changed artifacts, and evidence can be mutually reachable; proposed changes can be shown in the medium a human understands; interruption points can preserve enough context for review or rejection. But the local [architecture](../../ARCHITECTURE.md) assigns grants, approval, durable state, evidence, outcome, and receipts to its kernel. Nimbalyst's provider, process, storage, and collaboration authorities cannot cross that boundary by being wrapped in a UI.

## What Actually Reduces Thinking Time

No candidate demonstrates reduced total development time, and no integration unit is admitted. Two precedent results nevertheless reduce **thinking and design search time** without pretending to remove implementation work:

1. **Triangulated navigation and visual review are credible product grammar.** Nimbalyst is a working, source-visible precedent that users can navigate one body of work through files, agent sessions, and tasks, and can inspect changes through editor-specific diffs. This narrows future local product research toward read-only, owner-qualified links and honest before/after evidence instead of another canonical tracker. It corroborates the local [IDE Ergonomics restraint](../../../ide-ergonomics/UNIFIED-PRODUCT-VIEW.md) and [UI Prototyping Studio review grammar](../../../ui-prototyping-studio/interfaces.md); it does not originate or implement either.
2. **Raw evidence separated from disposable projection is a credible protocol precedent.** The pinned transcript design shows provider-native records retained as source material while canonical UI events are rebuilt. That gives C05 a precise future definition and prevents confusing a renderer's model with evidence or kernel outcome. It removes conceptual ambiguity now, but removes implementation work only after two admitted provider formats demonstrate duplicated parser/projection effort.

These are precedent savings in design exploration. Every claim of implementation-time reduction remains **none demonstrated** until the corresponding reopening witness exists.

## Verdict Matrix

| Candidate | Owner (Rittel) | Witnessed? (Popper) | Sound? (Quine) | Terminal | Typed negative | Reopening condition |
| --- | --- | --- | --- | --- | --- | --- |
| NIM-C01 | build-from-owned | NO | NO | **KILL** | `NEG-NV/no-present-consumer` | A selected renderer consumes exactly `{artifact_ref, content, theme, readOnly}` and demonstrates duplicated host work without save/dirty/subscription authority. |
| NIM-C02 | build-from-owned | NO | NO | **KILL** | `NEG-NV/dependency-without-parent` | C01 passes; a selected editor needs `createFixtureHost(fixedArtifact)`; duplicated fixture setup costs more than a local fixture. |
| NIM-C03 | already-deployed | NO | NO | **KILL** | `NEG-NV/repair-misattributed-as-integration` | A named contribution is unrepresentable by the repaired local schema and one uniquely Nimbalyst-derived case removes demonstrated work. |
| NIM-C04 | build-from-owned | NO | NO | **KILL** | `NEG-NV/no-target-artifact` | A named externally consumed package, exact exports, and consumer exist, and the checks replace demonstrated bespoke work. |
| NIM-C05 | build-from-owned | NO | **YES** | **KILL** | `NEG-NV/threshold-not-met` | Two admitted provider formats demonstrate duplicated parser/projection work and one repeated projection query, with deterministic replay preserving unknown records, redaction, order, correlation, and hashes. |
| NIM-C06 | build-from-owned | NO | NO | **KILL** | `NEG-NV/local-precedent-already-owns-interface` | No standalone reopening; prove a residue fits neither C05 nor C12. |
| NIM-C07 | build-from-owned | NO | NO | **KILL** | `NEG-NV/missing-required-state` | A materialized, hash-validated before/after pair and a measured decision that plain links cannot support, after all cited L0 repairs pass. |
| NIM-C08 | build-from-owned | NO | **YES** | **KILL** | `NEG-NV/no-measured-user-job` | A recurring query, measured baseline navigation cost, named resolver owner, and owner-qualified edges passing broken/foreign/no-write tests. |
| NIM-C09 | build-from-owned | NO | NO | **KILL** | `NEG-NV/no-upstream-contribution` | No Nimbalyst reopening; route the first consumer and minimal fields to the locally owned packet work. |
| NIM-C10 | build-from-owned | NO | NO | **KILL** | `NEG-NV/duplication-not-observed` | Two descriptor producers duplicate normalization after schema repair; a pure parser passes hostile-data and zero-ambient-access tests. |
| NIM-C11 | build-from-owned | NO | NO | **KILL** | `NEG-NV/vocabulary-without-survivor` | An admitted browser `observe` action has an exact Nimbalyst-derived field absent from destination-native Playwright/MCP and removes demonstrated work. |
| NIM-C12 | build-from-owned | NO | **YES** | **KILL** | `NEG-NV/failure-state-without-trigger` | The first real resume/process-capable adapter exposes requested/observed continuation identity, interruption, termination, cleanup, resumability, and residue under mismatch/timeout tests. |
| NIM-C13 | already-deployed | NO | NO | **KILL** | `NEG-NV/subtraction-leaves-no-unit` | A bounded runtime remains after all permission/session/process/storage authority is removed and wins a measured lifecycle-cost comparison. |
| NIM-C14 | build-from-owned | NO | NO | **KILL** | `NEG-NV/no-current-power-requirement` | A required offline operation has bounded CWD/env/HOME, no imported durable state, custody/recovery tests, and positive total-cost evidence. |
| NIM-C15 | precedent-clean | NO | NO | **KILL** | `NEG-NV/open-dependency-closure` | A current collaboration need and owner plus pinned client/server/identity/key/custody closure, proposal-only remote semantics, failure tests, and positive full-stack cost. |
| NIM-C16 | precedent-clean | NO | NO | **KILL** | `NEG-NV/unrelated-capability` | A current criterion separately requires zero-egress observability or signed updating, with an owner, consent/signing/rollback tests, and positive cost evidence. |

### Counts

- **PRECEDENT:** 2 already-deployed (`C03`, `C13`); 12 build-from-owned (`C01`, `C02`, `C04-C12`, `C14`); 2 precedent-clean (`C15`, `C16`).
- **DEFINITIONAL-SOUNDNESS:** 3 sound (`C05`, `C08`, `C12`); 13 unsound.
- **NON-VACUITY witness:** 0 witnessed; 16 unwitnessed.
- **Terminal:** 0 ADMIT; 16 KILL.

## Development-Time Conclusion

The local path remains [the accepted L0 repair set](../architecture-review-2026-07-10/findings.md) followed by the [fake, offline L0.5 MCP witness](../mcp-chat-extension-integration-research/findings.md). Neither depends on Nimbalyst. L0 must first repair exactly-once approval consumption, actor/session attribution, lifecycle consistency, artifact resolution and after-state evidence, runtime schema enforcement, persistence consistency, and receipt/evidence integrity. L0.5 then admits one fake stdio `observe` tool under bounded CWD/env/HOME, no network or mutation, hash-bound evidence, and kernel-only receipts.

Copying Nimbalyst's Electron shell, provider/session runtime, MCP custody, terminal, Git/worktrees, database/storage/sync, mobile, telemetry, or updater does not reduce this work. It adds extraction, authority removal, provenance, dependency closure, security and failure testing, upgrade review, migrations, operations, and abandonment cost. In the current slice, total cost rises even before the separate collaboration server is considered.

## Product And Research Recommendations

1. **Retain the grammar, not the modes.** Research a small read-only projection connecting owner-qualified task, envelope/run, artifact/evidence, and receipt identifiers. Do not create a Nimbalyst-like tracker, workstream, launch, status, or write owner.
2. **Show evidence honestly.** A future review surface may present validated before/after artifacts and explicit disposition, but only after the local repairs materialize and hash-bind the after state. A browser click must not imply human attribution or receipt authority.
3. **Keep projections disposable.** If C05 reopens, provider-native redacted records remain evidence; the canonical view is versioned and rebuildable; neither decides success.
4. **Keep adapters subordinate.** Provider completion, interruption, resume, and cleanup observations are adapter evidence. The kernel alone adjudicates outcome and writes receipts.
5. **Study the user job before the workspace.** Test whether one restrained “next governed step” card and owner-safe links reduce reconstruction time before researching a mode-rich files/sessions/tasks shell.
6. **Use the pinned client as comparative evidence.** Future research may inspect exact SDK symbols, failure fixtures, and product flows, but literal reuse must beat clean-room local expression on total lifecycle cost. Official documentation begins at <https://docs.nimbalyst.com/>; revision-sensitive claims should continue to use immutable commit paths.

These recommendations do not promote implementation. They identify bounded research questions under existing local owners.

## Typed-Negative Appendix

| ID | What it would have contributed | Exact fact that zeroed it |
| --- | --- | --- |
| C01 | A narrow read-only evidence host vocabulary. | No selected renderer needs more than the four-value record; added lifecycle vocabulary has no consumer. |
| C02 | An Electron-free fixture host for visual-editor tests. | Its parent C01 fails and no editor is selected; an ordinary fixture is smaller than pruning upstream no-op mutation/storage behavior. |
| C03 | Closed manifests and hostile validation fixtures. | The local schema already owns the definition; the defect is enforcement of that schema, and no uniquely useful upstream case was named. |
| C04 | Build, pack, export, and minimal-consumer verification. | There is no named public package or external consumer to test. |
| C05 | Immutable provider-native evidence plus replaceable canonical projection. | Only one fake stdio `observe` lane exists; there is no second format, duplicated parser, or repeated projection query. |
| C06 | External-agent lifecycle and event distinctions. | The local envelope already owns `describe/prepare/run/collect/interrupt/inspect`; remaining distinctions belong to C05 or C12. |
| C07 | Visual before/after review with explicit disposition. | No resolvable, validated after artifact or measured decision beyond plain links exists. |
| C08 | A read-only owner-qualified task/session/artifact/receipt join. | No recurring query, baseline navigation cost, consumer, or resolver owner is recorded. |
| C09 | A visual design-feedback context packet. | The packet is already explicitly locally owned; Nimbalyst adds corroboration but no upstream contribution. |
| C10 | A pure, redacted per-run MCP descriptor parser. | Only one producer is planned, normalization is not duplicated, and existing schema enforcement must be repaired first. |
| C11 | Typed browser observation vocabulary. | No admitted browser witness or Nimbalyst-specific term survives comparison with destination-native Playwright/MCP vocabulary. |
| C12 | Fail-loud interruption, termination, resume-identity, cleanup, and residue semantics. | The selected fake witness has no real process/provider resume token or resume operation. |
| C13 | A ready permission/provider/session execution runtime. | Removing permission, session, process, and storage authority leaves no bounded reusable implementation unit. |
| C14 | Terminal, Git/worktree, backend, Electron, and durable storage machinery. | L0/L0.5 requires none of those powers; the grouped services import several separate authorities and recovery programs. |
| C15 | Collaboration, sync, mobile continuation, identity, and credential custody. | No current need or owner exists, and the separate server dependency is absent from the inspected MIT repository. |
| C16 | Product telemetry and executable auto-update plumbing. | Neither capability advances a current acceptance criterion, and they are unrelated governance programs combined only by product packaging. |

## Banked Reopening Hypotheses

### C05: Evidence Projection Pair

`(R, P_v)`: `R` is an immutable, ordered, redacted provider-native record sequence preserving unknown records and correlation; `P_v(R)` is a versioned, deterministic, disposable canonical view. The exact future witness is **two admitted provider-native formats with measured duplicated parser/projection work and one repeated projection query**, plus deterministic replay proving unknown-record retention, redaction, ordering, correlation, and hashes.

### C08: Owner-Qualified Provenance Join

A disposable read-only relation whose cells retain `(owner, schema/version, id)`, preserve unresolved edges, and have no status, lifecycle, launch, promotion, or write semantics. The exact future witness is **one named recurring query, measured baseline navigation cost, an assigned resolver owner, and broken/foreign/no-write acceptance tests over canonical owner-qualified resolvers**.

### C12: Observed Termination Semantics

Separate interruption requested, process termination observed, cleanup, resumability validation, partial residue, and kernel outcome; resume succeeds only when provider and opaque continuation identities match. The exact future witness is **the first admitted real resume/process-capable adapter**, with mismatch and timeout fixtures exposing requested/observed continuation identity, interruption, termination, cleanup, resumability, and residue while proving kernel-only outcome adjudication.

## Exact Next Route

Route the next work to the existing `projects/ide-extension` owner: **complete and independently reverify the accepted L0 architecture-review repairs, then execute the already-defined fake/offline L0.5 `McpChatWitnessAdapter` slice and its negative tests; do not open a Nimbalyst integration task.** Reopen only the matching research candidate when the exact C05, C08, or C12 witness appears; otherwise retain this pinned result as precedent and typed-negative evidence.
