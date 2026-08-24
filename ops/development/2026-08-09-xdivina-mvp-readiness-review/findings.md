# xDivina MVP Readiness Review — Consolidated Findings

## Evidence and claim ceiling

This synthesis is bound to `projects/xdivina` commit `755b09aa6681e0a6ef2d7fed3707dcfe877efc39` and the 55/55 paths resolved from `review-corpus.txt`. The owner Inventory match and target-local Inventory are absent; the strategy Inventory packet is discovery context only and is not target proof. Evidence comprises current pinned bytes, attacker reproductions, governance replay, historical browser/GIMP records, fixtures, and one reported bounded human completion. It does not establish implementation acceptance, packaging, publication, release, deployment, production, or commercial readiness.

The replayed explicit suite exited **1**: 103 tests passed and six socket-dependent tests errored because the sandbox prohibited socket creation. Those six are unavailable here, neither passed nor product failures. `python3 -m unittest discover -v` exited **5** with zero tests; `XDM-EXEC-004` is therefore dropped, not retained as a green-discovery finding.

## Executive verdict

xDivina contains a technically substantial candidate-local browser/editor-core workflow, but it is not currently proven as a fresh-machine, non-developer MVP. A distributable desktop MVP is blocked by an undefined end-to-end acceptance contract, shell/package/install gaps, retention semantics, security/offline controls, and licensing. Production/commercial readiness is blocked by those gaps plus control-plane audit loss, broad compatibility, operational, support, and release evidence. The smallest responsible next move is contract reconciliation and one representative Tier B outcome—not a readiness declaration.

## Three-tier MVP status matrix

| Tier | Status | Evidence that survives | Missing or blocking evidence |
|---|---|---|---|
| A — bounded browser workflow | **Implemented candidate; readiness blocked** | Broad static and fixture/unit coverage; historical local GIMP/browser evidence; one reported bounded completion | Current live replay, editor-specific fresh-machine launch, durable-save communication, modal keyboard behavior, and measured usability evidence |
| B — distributable desktop MVP | **BLOCKED** | Provisional Linux Electron spike; a future clean-install outcome is documented | One coherent acceptance contract, selected/packageable shell, installer and clean-machine proof, second platform, isolation, offline enforcement, and license/notices |
| C — production/commercial readiness | **BLOCKED** | Threat, compatibility, and dependency risks are explicitly recorded | All Tier B gates; audit integrity, broad PSD evidence, production AI/security/performance, privacy/support/commercial terms, deployment and release proof |

## Deduplicated surviving findings

| Stable ID | Source-ID crosswalk | Severity / tier | Verdict | Exact current-target evidence | Why it matters | Smallest requested change | Falsifiable acceptance check |
|---|---|---|---|---|---|---|---|
| `XD-F001` | `XDMVP-PC-001`, `XDMVP-PC-003`, `XDM-EXEC-003`, `AHR-009` | MAJOR / A | **FIX** | `README.md:120` — “A human usability trial is still pending”; `docs/research/mvp-human-ui-trial-2026-08-02.md:3,87-94` — “BOUNDED HUMAN TRIAL PASSED” but exact timing/affordance measurements remain separate; `docs/runbooks/mvp-human-ui-plan.md:283-291` requires those measurements. | Current status contradicts the evidence, while unqualified “passed” would inflate one reported completion into usability validation. | Reconcile the root status as one reported bounded workflow completion and list the missing usability evidence and Tier B/C exclusions. | Root, plan, and trial use compatible wording; a text check rejects both “trial pending” and an unqualified general-usability claim. |
| `XD-F002` | `XDMVP-PC-002` | MAJOR / A-B | **FIX** | `docs/research/phase0-gate-review-2026-08-02.md:42-43,55-57` permits narrow UI only after blocker disposition and preserves NOT PASSED; `docs/research/mvp-human-ui-trial-2026-08-02.md:3` later opens feature expansion. | The authority edge from failed Phase 0 to expanded Tier A work is undocumented. | Add a dated addendum defining the Tier A-only exception and preserving the closed Tier B gate. | A current authority record names scope, owner, date, permitted tier, excluded tiers, and unresolved blockers; no text implies Phase 0 passed. |
| `XD-F003` | `XDMVP-PC-004`, `AHR-007`, part of `AHR-005` | MAJOR / C, and any broad PSD Tier B claim | **FIX** | `AGENTS.md:92-95` makes `docs/project-spec-v1.md` the baseline; that spec at `:79,87,103` makes categorical aggregation/legal and full-PSD claims. `README.md:31` rejects standalone libgimp embedding; `docs/research/phase0-gate-review-2026-08-02.md:19-20` records 14 advanced PSD unknowns and open distribution review. | The designated baseline conflicts with current architecture and evidence ceilings. | Mark v1 as historical intent or supersede it with a current contract that routes legal and fidelity claims to evidence gates. | Every baseline-level architecture, legal, and PSD claim resolves to a current ADR/evidence status; no categorical legal conclusion or unproved full-fidelity promise remains current. |
| `XD-F004` | `XDMVP-PC-005`, `AHR-001`, `AHR-006` | MAJOR / B | **FIX** | `docs/plans/foundation-and-mvp.md:437` requires a clean-install non-developer outcome; `docs/plans/editor-core-and-feature-roadmap.md:104-110` defines browser implementation work without package/install/offline closure; `docs/research/shell-benchmark-2026-08-02.md:23-24,52-57,63-66` records non-interactive 100MP zoom and a provisional Linux Electron fallback. | Capability accumulation does not yet compose into a distributable desktop outcome. | Define one Tier B contract spanning install, prerequisite diagnosis, launch, representative edit, durable save/reopen/export, offline behavior, and uninstall on named platforms. | A clean machine executes the contract without manual GIMP/ComfyUI setup; each step has an observable pass/fail receipt and selected shell/package identity. |
| `XD-F007` | `AHR-002` | MAJOR / A | **FIX** | `scripts/mvp_gateway.py:309-320,355-368` owns inputs/outputs in a temporary session and cleans it at shutdown; the UI action is presented as “Save XCF.” | A user may infer durable persistence even though retention depends on downloading the artifact before cleanup. | Relabel the action as creating a downloadable XCF and visibly warn/confirm before closing with an undownloaded artifact. | Browser test proves warning and focus behavior; after shutdown the session artifact is absent, while a downloaded XCF remains and reopens successfully. |
| `XD-F008` | `AHR-008` | MAJOR / A | **FIX** | `apps/mvp-ui/index.html:227-269`; `apps/mvp-ui/app.js:1375-1399,1559-1564,1821-1828`: dialogs have initial/Escape focus handling but no Tab containment or inert-background behavior, and scope close returns focus to a hidden control. | Keyboard users can leave the active modal or lose a reliable focus return point. | Add modal focus containment, inert background, and invoker restoration. | Browser keyboard tests prove Tab/Shift-Tab remain within each modal, background controls cannot activate, Escape closes, and focus returns to the invoker. |
| `XD-F009` | `AHR-003` | CRITICAL / B-C only | **FIX** | `docs/security/local-network-policy.md:23,29-38,67-69` says ComfyUI is loopback-only with no authentication and another same-user process can connect. | Loopback locality is not principal isolation for a shipped desktop or production claim. It does not invalidate the disposable Tier A harness. | Put ComfyUI behind a per-session authenticated proxy or a verified OS-private transport/sandbox. | An unauthorized same-user process cannot reach or invoke ComfyUI; authorized xDivina flow succeeds; credentials/endpoints are not browser-visible. |
| `XD-F010` | `AHR-004` | CRITICAL / B-C only | **FIX** | `docs/security/local-network-policy.md:80-82` explicitly says current tests do not prove offline network enforcement or a complete sandbox. | “Local-first/offline” distribution claims require observed, fail-closed behavior across shell and sidecars. | Implement a fail-closed offline profile covering updates, downloads, telemetry, models, providers, and custom nodes. | Negative observation records zero unapproved outbound attempts across the packaged workflow; attempted forbidden access fails closed and visibly. |
| `XD-F011` | `AHR-005`, part of `XDMVP-PC-004/005` | MAJOR / B-C | **FIX** | `LICENSES/README.md:9-14` records no root license and rejects legal inference from process boundaries; `docs/research/dependency-matrix.md:42-57` leaves application/model terms, notices, legal review, and release checking open. | Distribution has no reviewed license/notice basis. | Freeze the shipped graph, decide distribution licensing, generate notices/source obligations, and add a release gate. | Package manifest and hashes match reviewed records; notice/license check passes and blocks any unknown component or model. |
| `XD-F012` | `XDM-EXEC-001` | MAJOR / C control-plane | **FIX** | `scripts/event_store.py:5` promises idempotency keyed on `(source,event_id)`, while `:52-54` declares global `event_id TEXT PRIMARY KEY` and `:92-100` silently ignores collisions. The focused reproducer stored only one of two same-ID events from different sources. | Legitimate producer events can be silently discarded. This does not block Tier A or necessarily a Tier B editor that excludes this store. | Make `(source,event_id)` the uniqueness key and return persisted/duplicate truth. | A regression appends the same event ID from two sources and observes two rows; a same-source duplicate remains one row with explicit duplicate status. |
| `XD-F013` | `XDM-EXEC-002` | MAJOR / C control-plane | **FIX** | `scripts/event_store.py:23-24,145-157` derives transition IDs from second-resolution time; `scripts/test_event_store.py:141-154` checks final state but not event count. In the focused reproducer, one of four rapid transition events survived, yielding two total events including the seed, while final state became `done`. | The append-only lifecycle audit can lose valid rapid transitions while state appears correct. | Use collision-resistant transition IDs, keep state/event atomic, and assert audit cardinality. | Four valid rapid transitions persist four ordered transition events in addition to the seed and final state is `done`; forced event failure rolls back the state update. |

## Dropped after verification

The following are not findings and are not change requests:

- `XD-F005` was dropped because the current UI README already defines a coherent 19-step workflow and the trial records one human completion; a named cohort or numerical success budget is future usability evidence, not an established blocking requirement.
- `XD-F006` was dropped because the broad surface is an explicit design choice, planned controls are honestly disabled, and no calibrated comparison or observed cognitive-load failure proves harm to the completed bounded workflow.

## Per-artifact disposition

| Artifact | Surviving IDs | Disposition |
|---|---|---|
| `README.md`; human trial/plan records | `XD-F001` | Reconcile status and claim ceiling. |
| Phase 0 gate and later trial | `XD-F002` | Record the bounded exception; do not rewrite Phase 0 as passed. |
| `AGENTS.md`; product spec; PSD/license evidence | `XD-F003` | Supersede or demote obsolete baseline claims. |
| Foundation plan; editor roadmap; shell benchmark | `XD-F004` | Define and prove one coherent Tier B outcome. |
| Gateway/UI | `XD-F007`, `XD-F008` | Repair retention communication and modal keyboard behavior. |
| Network policy | `XD-F009`, `XD-F010` | Tier B/C isolation and offline gates remain closed. |
| License/dependency records | `XD-F011` | Distribution remains closed pending reviewed package records. |
| Event store/tests | `XD-F012`, `XD-F013` | Tier C/control-plane audit integrity remains blocked. |

## Severity-ordered minimal change requests

1. **CRITICAL for B/C:** close same-user ComfyUI access (`XD-F009`) and prove fail-closed offline behavior (`XD-F010`).
2. **MAJOR contract gate:** reconcile status, Phase 0 exception, and baseline authority (`XD-F001`–`XD-F003`).
3. **MAJOR Tier B definition:** define and prove one install-to-uninstall desktop outcome before further readiness claims (`XD-F004`).
4. **MAJOR Tier A operability:** make artifact retention explicit and modal keyboard behavior complete (`XD-F007`, `XD-F008`).
5. **MAJOR distribution:** close license, notices, model/custom-node, and component-record gates (`XD-F011`).
6. **MAJOR Tier C/control-plane:** repair both silent event-loss modes with atomic regression tests (`XD-F012`, `XD-F013`).

## Preserved dissent

- `XD-F007` is an operability/communication defect even though the underlying save/reopen mechanism has static and fixture support.
- `XD-F009` and `XD-F010` are CRITICAL only at Tier B/C claim boundaries; no CRITICAL Tier A defect was established.
- `XD-F012` and `XD-F013` belong to Tier C/control-plane integrity unless a selected Tier B package explicitly ships and depends on that store.
- PSD breadth blocks broad PSD migration/fidelity promises, not an explicitly scoped XCF-first Tier B MVP.
- The optional feedback edge to attackers was not traversed: the verifier conflict was adjudicable from current evidence, and missing future acceptance artifacts are expected change-request checks rather than missing review evidence.

## Validation limits

The review did not rerun current live GIMP, gateway, browser, visual quality, real XCF fidelity, latency, crash cleanup, process isolation, packaging, installer, second-platform, or offline observations. Six socket-backed checks remain unavailable in this sandbox. Historical evidence was not promoted to current execution proof. Default discovery collects zero and exits 5; a fail-on-zero explicit runner remains unapplied workflow residue. Aggregate line totals are intentionally omitted because they were disputed; 55/55 pinned-path resolution is the accepted coverage fact.

## No-implementation statement

This document is a read-only review artifact. No finding authorizes product mutation, lifecycle acceptance, packaging, publication, release, deployment, promotion, or a production/commercial claim. Every requested change requires a separately authorized candidate and fresh validation against its exact bytes.
