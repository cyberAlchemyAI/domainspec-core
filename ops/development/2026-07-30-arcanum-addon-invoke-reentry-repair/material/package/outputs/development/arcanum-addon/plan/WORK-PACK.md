---
module: arcanum-addon
version: current
status: draft
updatedAt: 2026-07-30
docType: work-pack
---

# WORK-PACK: Arcanum Add-on

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | block | Planning is authored; execution blockers remain. |
| complexity | high | Cross-repository provenance plus SDK, bridge, state, UI, security, lifecycle, browser, and owner decisions. |
| outputMode | split | Task and wave files are required. |
| executionPackRef | `EXECUTION-PACK.md` | High-complexity schedule. |
| layeringArtifactRef | `IMPLEMENTATION-LAYERING.md` | L0-L3 decision model. |
| dispatchTechniqueTrace | `DISPATCH-TECHNIQUE-TRACE.md` | Selected technique bindings. |
| distillValidationStatus | block | The repair revalidation closed seven findings but preserved `NEW-001`: per-SWU re-entry was prose-only. A machine-bound selection decision is now authored for every exact SWU; fresh exact-byte independent revalidation remains required. |
| swuAtomicityStatus | pass-reconciled-authored | The complete non-exempt SWU set is mapped below; this remains planned evidence, not execution evidence. |
| firstUnitNarrownessStatus | pass-authored | Governance then no-write compatibility precede product mutation. |
| closeoutSyncStatus | pass-authored | Every mutation-capable SWU has a planned closeout row; not executed. |
| activeLayerWindow | L0 | Preview-only trust-building layer. |
| selectedSWU | none | Task Session must ask after all blockers close. |
| lastUpdatedAt | 2026-07-30T00:00:00-03:00 | Planning timestamp, not execution time. |
| readinessProfile | pilot | Release-candidate/production are not claimed. |

## Objective Summary

- Objective: deliver one ResonantOS-native `addon.arcanum` that safely exposes
  selected Bootstrap-managed public Arcanum capabilities through Augmentor and
  the existing authenticated bridge.
- Primary inputs: approved Define, deterministic Design selection, authored
  Design views, current product commit `80dcd796...`, accepted research.
- Success condition: the literal Strategy + Whisper local browser fixture and
  every deterministic/security/lifecycle gate pass, followed by an explicit
  acceptance-owner readiness decision.
- Non-success: manifest validity, unit tests, route success, browser launch,
  receipts, or rollback alone.

## Delivery Slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S0 | Authority, issue, owner, baseline, and compatibility gates are explicit. | L0 | W0 | none | owner decision and compatibility receipts |
| S1 | Valid untrusted catalog entry, redacted status, and pure proposal preview. | L0 | W1 | S0 | SDK/status/resolver/UI zero-effect tests |
| S2 | Exact approval, at-most-once fixture execution, owner state, run tray, reload. | L1 | W2 | S1 | approval/replay/state/reload tests |
| S3 | Stable Strategy/Whisper adapters, clarification, artifacts, and consumption. | L2 | W3 | S2 + accepted Bootstrap compatibility | adapter/isolation/result tests |
| S4 | Lifecycle, security, full validation, and literal browser witness. | L3 | W4 | S3 | repository/security/live Chrome gates |
| S5 | Readiness, promotion, and release decisions remain independent. | L3 | W5 | S4 | explicit owner decisions |

## Task Status Board

| Task | Goal | Layer | Waves | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-0](work-pack/tasks/TASK-0-GOVERNANCE-COMPATIBILITY.md) | Close authority, issue, owner, and Bootstrap compatibility prerequisites. | L0 | [W0](work-pack/waves/W0.md) | blocked | not-started |
| [TASK-1](work-pack/tasks/TASK-1-CATALOG-PREVIEW.md) | Build catalog/status/pure-preview minimum working unit. | L0 | [W1](work-pack/waves/W1.md) | blocked-by-TASK-0 | not-started |
| [TASK-2](work-pack/tasks/TASK-2-APPROVAL-STATE.md) | Prove exact approval and owner-backed fixture state. | L1 | [W2](work-pack/waves/W2.md) | blocked-by-TASK-1 | not-started |
| [TASK-3](work-pack/tasks/TASK-3-ADAPTERS-RESULTS.md) | Bind real public owners and independent result operations. | L2 | [W3](work-pack/waves/W3.md) | blocked-by-TASK-2-and-compatibility | not-started |
| [TASK-4](work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md) | Prove lifecycle, security, and literal browser behavior. | L3 | [W4](work-pack/waves/W4.md) | blocked-by-TASK-3 | not-started |
| [TASK-5](work-pack/tasks/TASK-5-VERIFY-DECIDE.md) | Recompose evidence and route independent owner decisions. | L3 | [W5](work-pack/waves/W5.md) | blocked-by-TASK-4 | not-started |

## SWU Execution Handoff

| SWU | Parent | Dependencies | Write scope | Acceptance | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| SWU-ARC-GOV-001 | TASK-0 | none | GitHub issue/Project 2 only | governing acceptance, owners, and retention decision recorded | manual product owner | blocked |
| SWU-ARC-BOOT-001 | TASK-0 | GOV-001 | compatibility evidence path only | no-write exact current/target receipt | Arcanum Bootstrap compatibility owner | blocked |
| SWU-ARC-BOOT-002 | TASK-0 | BOOT-001 + explicit separate approval | Bootstrap-managed generated paths only | selected packages match pinned source | Arcanum Bootstrap | blocked |
| SWU-ARC-CATALOG-001 | TASK-1 | GOV-001 + BOOT-001 | `public/addons/arcanum.json`, focused SDK tests | valid sideload catalog remains uninstalled/disabled/ungranted | Task Session | blocked |
| SWU-ARC-STATUS-001 | TASK-1 | CATALOG-001 | host status service/routes/tests | redacted profile; no secrets/raw paths | Task Session | blocked |
| SWU-ARC-PROPOSAL-001 | TASK-1 | STATUS-001 | pure resolver/contracts/tests | deterministic bytes; zero effects | Task Session | blocked |
| SWU-ARC-PROPOSAL-UI-001 | TASK-1 | PROPOSAL-001 | extension router/card/tests | explicit precedence and `No actions started` | Task Session | blocked |
| SWU-ARC-L0-DECISION-001 | TASK-1 | PROPOSAL-UI-001 | decision receipt only | explicit continue, preview-only, or stop decision over exact L0 receipts | product acceptance owner | blocked |
| SWU-ARC-APPROVAL-001 | TASK-2 | L0-DECISION-001=`continue` | host approval records/routes/tests | current digest persists; stale/expired fail | Task Session | blocked |
| SWU-ARC-RUN-001 | TASK-2 | APPROVAL-001 | run/child fixture records/routes/tests | at-most-once and owner-ack state | Task Session | blocked |
| SWU-ARC-RUN-UI-001 | TASK-2 | RUN-001 | run tray/session projection/tests | reload exact or `Unknown`; parent chat usable | Task Session | blocked |
| SWU-ARC-STRATEGY-001 | TASK-3 | BOOT-002 + RUN-001 | Strategy adapter/tests | exact stable public owner or zero-attempt block | Task Session | blocked |
| SWU-ARC-WHISPER-001 | TASK-3 | BOOT-002 + RUN-001 | Whisper adapter/tests | exact stable public owner or zero-attempt block | Task Session | blocked |
| SWU-ARC-CLARIFY-001 | TASK-3 | STRATEGY-001 + WHISPER-001 | child clarification route/tests | A-only delivery isolation | Task Session | blocked |
| SWU-ARC-ARTIFACT-READ-001 | TASK-3 | adapters + RUN-UI-001 | artifact read route/client/tests | read is independently non-mutating | Task Session | blocked |
| SWU-ARC-ATTACH-001 | TASK-3 | ARTIFACT-READ-001 | chat attachment controller/store/tests | selected chat only changes | Task Session | blocked |
| SWU-ARC-CONSUME-001 | TASK-3 | ARTIFACT-READ-001 | follow-up context binding/tests | explicit follow-up only | Task Session | blocked |
| SWU-ARC-INTAKE-001 | TASK-3 | ARTIFACT-READ-001 | archive intake adapter/client/tests | intake candidate; no trusted write | Task Session | blocked |
| SWU-ARC-DEGRADE-001 | TASK-4 | TASK-3 accepted candidate | degradation fixtures/tests only | compatibility drift and owner loss cause zero new starts, honest state, preserved history, and explicit recovery | Task Session | blocked |
| SWU-ARC-DISABLE-001 | TASK-4 | CLARIFY-001 + ATTACH-001 + CONSUME-001 + INTAKE-001 | disable/grant route/UI/tests | cached/new launches rejected | Task Session | blocked |
| SWU-ARC-UNINSTALL-001 | TASK-4 | isolated accepted DISABLE-001 snapshot + retention decision | uninstall product state/tests | Bootstrap bytes untouched; retained history follows accepted policy | Task Session | blocked |
| SWU-ARC-ROLLBACK-001 | TASK-4 | separate isolated copy of the same accepted DISABLE-001 snapshot | product rollback fixtures/tests | prior manifest/adapter/profile restored; owner history preserved; failure remains disabled | Task Session | blocked |
| SWU-ARC-SECURITY-001 | TASK-4 | DEGRADE-001 + both isolated lifecycle branch receipts + all mutation SWUs | security/redaction tests | all forbidden-canary, bypass, preservation, and branch-recomposition tests pass | Task Session | blocked |
| SWU-ARC-BROWSER-001 | TASK-4 | security + deterministic gates | browser fixture/evidence only | literal scenario observations captured | browser validation owner | blocked |
| SWU-ARC-VERIFY-001 | TASK-5 | all prior | evidence index/verification docs only | complete claim-to-evidence recomposition | Task Session | blocked |

Detailed source anchors, child split analysis, done criteria, and validation
surfaces live in the linked task files. Runtime Context Builder packs are
created only at Task Session preflight.

## SWU Atomicity Review

| SWU | Primary behavior | Candidate child units | Retained-boundary rationale | Verdict |
| --- | --- | --- | --- | --- |
| GOV-001 | bind one authority admission packet | issue acceptance vs Project synchronization vs owner/retention binding | all fields share one digest-bound owner receipt; partial synchronization is non-pass and cannot authorize successors | pass-reconciled-authored |
| BOOT-001 | no-write compatibility comparison | source pin vs generated hashes | one receipt requires both sides | pass-authored |
| BOOT-002 | one approved content-addressed Bootstrap selection transaction | per-package refreshes | retain only if Bootstrap proves staged all-or-nothing apply or full restoration; otherwise split before execution | pass-reconciled-authored |
| CATALOG-001 | catalog candidate with zero authority | manifest vs test | manifest without separation test is not independently acceptable | pass-authored |
| STATUS-001 | redacted compatibility projection | evaluator vs route | read model is accepted only through its route contract | pass-authored |
| PROPOSAL-001 | pure canonical proposal | resolver vs digest | digest is the resolver's acceptance boundary | pass-authored |
| PROPOSAL-UI-001 | one Augmentor proposal projection | router vs card vs second surface | precedence and shared-state rendering are one observable preview contract | pass-reconciled-authored |
| L0-DECISION-001 | persist one L0 continuation disposition | continue vs preview-only vs stop | exactly one disposition over exact L0 receipt digests is independently reviewable | pass-reconciled-authored |
| APPROVAL-001 | exact host approval | validation vs persistence | atomic compare-and-persist contract | pass-authored |
| RUN-001 | exactly-once owner-backed fixture state | registration vs state | split would hide crash/replay boundary | pass-authored |
| RUN-UI-001 | one host-state projection across both surfaces | tray vs reload vs parent-chat availability | one shared owner-state contract must remain consistent across the projections | pass-reconciled-authored |
| STRATEGY-001 | one Strategy public-owner adapter | probe vs invoke | owner binding plus no-substitution behavior is one acceptance boundary | pass-authored |
| WHISPER-001 | one Whisper public-owner adapter | probe vs invoke | owner binding plus no-substitution behavior is one acceptance boundary | pass-authored |
| CLARIFY-001 | one addressed child delivery | route vs isolation test | isolation is the operation's acceptance boundary | pass-authored |
| ARTIFACT-READ-001 | read one owner artifact reference | route vs client | read/non-mutation is one observable contract | pass-authored |
| ATTACH-001 | attach one selected artifact to one chat | selection vs persistence | selected-chat-only mutation is one acceptance boundary | pass-authored |
| CONSUME-001 | bind one selected artifact to one follow-up | selection vs context binding | explicit follow-up context is one acceptance boundary | pass-authored |
| INTAKE-001 | request one archive intake candidate | request vs archive response | candidate creation with no trusted write is one acceptance boundary | pass-authored |
| DEGRADE-001 | transition safely on compatibility drift or owner loss | drift vs owner-loss fixtures | both stressors share the same fail-closed state transition and recovery contract | pass-reconciled-authored |
| DISABLE-001 | reject new launches while preserving owner history | grant revocation vs UI state | fail-closed launch behavior is one lifecycle effect | pass-authored |
| UNINSTALL-001 | remove product-owned installed state from an isolated disabled snapshot | revoke vs remove vs retention | product-only removal and preservation counters are one branch acceptance boundary | pass-reconciled-authored |
| ROLLBACK-001 | restore pinned product artifacts from a separate isolated disabled snapshot | restore vs failure path | success and failure must prove the same disabled/history invariant | pass-reconciled-authored |
| SECURITY/BROWSER/VERIFY | closure/exempt | n/a | verification SWUs mutate evidence only | exempt |

The four result actions are separate SWUs. None may be recombined for scheduling
convenience.

## Blockers

| Blocker | Scope | Description | Owner | Next action |
| --- | --- | --- | --- | --- |
| B-GOV-001 | all | No governing GitHub issue/Project 2 acceptance record is bound to this work. | product maintainer | create/accept bounded issue and Project fields |
| B-DESIGN-001 | all | The repair revalidation closed F-001-F-006 and `NEW-BAL-001` but preserved `NEW-001`: no executable step consumed the prose-only re-entry gate. The v3 route now binds every exact SWU to a fresh single-use operator-selection decision, but this is authored evidence only. | Invoke operator | keep mutation handoff blocked; run fresh exact-byte independent revalidation before considering closure |
| B-BOOT-001 | L1+ | Strategy is absent; Whisper and other generated packages have unaccepted drift. | Arcanum Bootstrap owner | produce no-write receipt, then separately approve any refresh |
| B-OWNER-001 | L1+ | Proposal/approval, adapter, retention, acceptance, promotion, and release owners are not repository-bound for this feature. | product maintainer | record owners in governing issue/design decision |
| B-ADAPTER-001 | L2+ | Stable public native Strategy/Whisper operation contracts are unproven; nested model CLI is forbidden. | Arcanum capability owners | expose/validate stable operations or retain preview-only |
| B-RETENTION-001 | uninstall | Retention/disposal policy for redacted owner history after uninstall is unresolved. | data/product owner | accept a retention policy before uninstall implementation |

## Dispatch Technique Trace

See `DISPATCH-TECHNIQUE-TRACE.md`.

## Distill Validation

See `DISTILL-VALIDATION.md`. Current verdict remains block: the latest
independent repair revalidation preserved one MAJOR machine-route finding. The
v3 selection binding is authored and validated locally but has not received a
fresh exact-byte independent validation.

## Task Session Closeout

See `work-pack/shared/CLOSEOUT-SYNC.md`. These are planned closeout contracts,
not completed closeout receipts.

## Gate Checks

1. Work-pack remains blocked while any blocker above affects acceptance.
2. No SWU is selected.
3. Task Session must rebind the current `origin/dev` commit, governing issue,
   Project 2 state, Design/Plan digests, and source selectors at preflight.
4. Bootstrap refresh requires separate explicit authority; product enable,
   update, uninstall, or rollback cannot imply it.
5. L2 is killed or remains unavailable if stable public owner operations require
   nested model CLI or fallback substitution.
6. Planned witnesses, validators, and closeout rows are not execution evidence.

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-07-30 | Initial blocked high-complexity Plan authored from current `origin/dev`. | Invoke |
| 2026-07-30 | Reconciled governed Distill findings: durable L0 decision, isolated lifecycle branches, degradation SWU/witnesses, and complete atomicity coverage. Gate remains blocked. | Invoke |
| 2026-07-30 | Reconciled second revalidation findings: replaced generic layer receipts with exact SWU/wave joins and split degradation from disabled-lifecycle validator bindings. Gate and `selectedSWU: none` remain unchanged pending fresh exact-byte review. | Invoke Refresh |
| 2026-07-30 | Reconciled repair-revalidation `NEW-001`: every exact SWU now consumes a fresh source-bound, single-use operator-selection decision with literal SWU/step matching and zero-start rejection. Gate and `selectedSWU: none` remain unchanged pending fresh exact-byte review. | Invoke Refresh |
