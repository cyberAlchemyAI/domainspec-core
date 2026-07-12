# Traceability

| Requirement/decision | Plan coverage | Acceptance evidence |
| --- | --- | --- |
| Visible required task | SWU-001 contract, SWU-007 UI | schema/DOM/Playwright tests |
| Manual poll only | SWU-006 protocol, SWU-011 witness | CLI tests and witness report |
| Late skill disclosure | SWU-003 ready projection, SWU-004 claim | pre-claim omission and claim packet tests |
| Read/preview-only effects | SWU-001 grants, SWU-005 blocked result | grant/effect hostile tests |
| Two receipt kinds | SWU-001 schema, SWU-003 authorization, SWU-005 execution | schema/artifact/binding tests |
| Singleton ready target | SWU-003, SWU-008 | race/restart/UI tests |
| Atomic claim | SWU-004 | concurrent claim exact-once test |
| Operator release/requeue | SWU-004, SWU-008 | actor/state/recovery tests |
| Unattested identity | SWU-001, SWU-004, SWU-007 | schema/API/UI assertions |
| Kernel result admission | SWU-005 | mismatch/replay/reference tests |
| v1 replay compatibility | SWU-001/002 | immutable v1 event fixtures |
| Session one-shot tooling | SWU-006 | child-process CLI tests |
| Hostile/restart proof | SWU-009 | `npm run test:bridge` |
| Desktop/mobile workflow | SWU-010 | Playwright screenshots/assertions |
| Real blind witness | SWU-011 | bound receipt + skill hash + report |
| Complete readiness | TASK-VERIFY-READINESS | [PASS closure matrix and full validation report](../../task-sessions/20260712T115410Z-task-verify-readiness/CLOSURE-REPORT.md) |

## Navigation

- First task: [TASK-CONTRACT-MIGRATION](../tasks/TASK-CONTRACT-MIGRATION.md)
- First SWU: `SWU-MSB-001`
- First wave: [W0](../waves/W0.md)
- Source design: [ARCHITECTURE-BUNDLE.md](../../../manual-session-bridge-design/ARCHITECTURE-BUNDLE.md)
- Decisions: [DECISIONS.md](../../../manual-session-bridge-design/DECISIONS.md)

## Execution Evidence

| SWU | Result | Requirement evidence | Remaining boundary |
| --- | --- | --- | --- |
| [SWU-MSB-001](../../task-sessions/20260712T055820Z-swu-msb-001/TASK-SESSION-RESULT.md) | pass | Exact read-only bridge grants; required skill task; v2 state bindings; separate authorization/execution receipts; unattested actor/session request schemas; legacy envelope/receipt fixtures. | v1/v2 event replay and transition behavior remain pending in SWU-MSB-002. |
| [SWU-MSB-002](../../task-sessions/20260712T060816Z-swu-msb-002/TASK-SESSION-RESULT.md) | pass | Pure-v1 exact projection; version dispatch; mixed replay; singleton target; authorization lifetime; rejection/revocation; interruption/release/new attempt; terminal receipt atomicity; restart checksum. | Server/API emission remains pending in SWU-MSB-003..005. |
| [SWU-MSB-003](../../task-sessions/20260712T062325Z-swu-msb-003/TASK-SESSION-RESULT.md) | pass | Nonterminal authorization receipt; exact singleton ready/unready; secret-safe pre-claim inventory; restart; pending rejection; approved/ready revocation; append-failure behavior. | Claim/recovery and result admission remain pending in SWU-MSB-004..005. |
| [SWU-MSB-004](../../task-sessions/20260712T062622Z-swu-msb-004/TASK-SESSION-RESULT.md) | pass | Commit-before-disclosure claim; one race winner; no loser payload; session-bound interrupt; operator release; explicit retarget; attempt history; restart; append-failure safety. | Terminal result and execution receipt remain pending in SWU-MSB-005. |
| [SWU-MSB-005](../../task-sessions/20260712T063105Z-swu-msb-005/TASK-SESSION-RESULT.md) | pass | Bound result admission; authorization consumption; completed claim; execution receipt; four evidence views; restart; mismatch/duplicate/race/append-failure handling. | Session protocol and human UI remain pending in W2. |
| [SWU-MSB-006](../../task-sessions/20260712T063619Z-swu-msb-006/TASK-SESSION-RESULT.md) | pass | Loopback one-shot ready/claim/result/interrupt CLI; process exits; stdout/stderr/exit contracts; no operator commands; documented manual poll sequence. | Human workbench remains pending in SWU-MSB-007/008. |
| [SWU-MSB-007](../../task-sessions/20260712T063929Z-swu-msb-007/TASK-SESSION-RESULT.md) | pass | Visible empty required task; exact bridge grants; truthful authorization copy; typed receipt rows; bounded evidence references; narrow-layout safeguards. | Target, claim, recovery, and result states remain pending in SWU-MSB-008. |
| [SWU-MSB-008](../../task-sessions/20260712T064328Z-swu-msb-008/TASK-SESSION-RESULT.md) | pass | Singleton target indicator; legal-state ready/unready; unattested claims; operator-only release/requeue; attempt history; terminal result, validation, evidence, and both receipts. | Automated hostile aggregation remains pending in SWU-MSB-009. |
| [SWU-MSB-009](../../task-sessions/20260712T064639Z-swu-msb-009/TASK-SESSION-RESULT.md) | pass | Serial 66-case gate run twice; ten-obligation matrix covers contracts, secrecy, authority, races, replay, restart, bindings, and durable evidence failures. | Real Chromium desktop/mobile proof remains pending in SWU-MSB-010. |
| [SWU-MSB-010](../../task-sessions/20260712T064813Z-swu-msb-010/TASK-SESSION-RESULT.md) | pass | 4/4 Chromium journeys prove required task, target conflict, secrecy, recovery, terminal evidence, attempt history, receipts, responsive layout, and error handling. | One real blind human/session witness remains pending in SWU-MSB-011. |
| [SWU-MSB-011](../../task-sessions/20260712T065218Z-swu-msb-011/TASK-SESSION-RESULT.md) | pass | Human sent only `poll`; opaque ready handle preceded atomic disclosure; one unattested claim completed; Invoke hash bound; terminal flagged result admitted; authorization consumed; two receipts and 7/7 evidence routes verified; retained artifact hashes and history screenshot. | Closure/readiness audit remains; L0 still makes no authenticated-session or write-sandbox claim. |

## Closure Evidence

| Task | Result | Readiness claim | Preserved boundary |
| --- | --- | --- | --- |
| [TASK-VERIFY-READINESS](../../task-sessions/20260712T115410Z-task-verify-readiness/TASK-SESSION-RESULT.md) | pass | L0 manual session bridge is ready for a bounded local, manual, read/preview-only pilot. | No authentication, mutation safety, automatic recovery, persistent worker, VSCodium/browser control, arbitrary agent, remote, multi-user, or production claim. |
