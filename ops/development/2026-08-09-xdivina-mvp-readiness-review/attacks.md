# xDivina MVP Review — Verbatim Attacker Returns

Dispatch: `2026-08-09-xdivina-mvp-readiness-review`

The six sections below preserve the three initial returns and three robot-talk final positions verbatim. Section headings are parent-added locators and are not part of the returns.

## Fong initial

dispatch_id: `2026-08-09-xdivina-mvp-readiness-review`  
step_id: `s1-attack-current-mvp`  
capability_ref: `distill`  
status: `complete_with_major_findings`

Verified target state:

- `projects/xdivina` HEAD: `755b09aa6681e0a6ef2d7fed3707dcfe877efc39`
- Branch: `main`
- `origin/main`: `755b09aa6681e0a6ef2d7fed3707dcfe877efc39`
- `git status --short`: empty
- No files changed.

Corpus resolution and coverage:

- Manifest entries: 55
- Existing: 55/55
- Tracked at pinned commit: 55/55
- Missing: 0
- Every manifest file was traversed in full and SHA-256-accounted.
- Inventory consequence honored: the packet supplied routing only; findings below derive from pinned xDivina files.

Exact commands:

```text
git -C projects/xdivina rev-parse HEAD
git -C projects/xdivina branch --show-current
git -C projects/xdivina status --short
git -C projects/xdivina rev-parse origin/main
awk ... review-corpus.txt | while read p; do test -f ...; git -C projects/xdivina ls-tree ...; done
awk ... review-corpus.txt | wc -l
while read p; do nl -ba projects/xdivina/$p; done
rg -n -i "<product/status terms>" <bounded corpus files>
awk ... review-corpus.txt | while read p; do sha256sum projects/xdivina/$p; done
```

Observed-vs-missing three-tier matrix:

| Tier | Observed | Missing / claim ceiling |
|---|---|---|
| A — bounded local browser/GIMP workflow | Real local GIMP 3.0.4 through authenticated adapter; browser gateway; open/upload/preview; semantic layers, selections, bounded history, masks, move/90-degree transforms; XCF save/reopen; PNG export; cancellation/recovery; one reported human completion | Large-document usability, task-level timing, observed affordance/confusion record, production isolation, complete layer reconciliation, representative prosumer outcome |
| B — distributable single-user desktop MVP | Electron Linux spike and a future clean-install/non-developer gate are documented | No selected shell, installer/package, clean-machine proof, bundled dependency setup, second-platform result, offline enforcement, production same-user isolation, finalized notices/license decision, or representative end-user workflow acceptance |
| C — production/commercial readiness | Target audience, threat model, staged PSD/AI/licensing plans, and explicit non-readiness warnings exist | Production editor, commercial distribution basis, beta evidence, support/privacy/license terms, broad PSD fidelity, production AI, performance envelope, deployment/release proof |

Findings:

- `XDMVP-PC-001` — **MAJOR** — Tier A — contradictory current status.  
  Evidence: `README.md:120`: “A human usability trial is still pending”; `docs/research/mvp-human-ui-trial-2026-08-02.md:3`: “**Status:** BOUNDED HUMAN TRIAL PASSED — feature expansion approved”; lines 85–90 say the user completed it.  
  Attack: the root status is stale and understates completed bounded evidence, making the current product contract internally inconsistent.  
  Fix: update the root status to say the bounded trial passed, while retaining its explicit Tier B/C exclusions.

- `XDMVP-PC-002` — **MAJOR** — Tiers A/B — gate chronology is unreconciled.  
  Evidence: `docs/research/phase0-gate-review-2026-08-02.md:42-43`: “A narrow human feasibility UI may begin only after the security and shell blockers have an evidence-backed disposition”; lines 55–57 preserve the NOT PASSED result. Yet `docs/research/mvp-human-ui-trial-2026-08-02.md:3` says the bounded trial passed and feature expansion is approved, and `apps/mvp-ui/README.md:65-88` claims a substantially expanded Editor Core surface.  
  Attack: the later work may be valid as a deliberately disposable exception, but no reviewed contract explicitly explains why it crossed the earlier “may begin only after” prohibition.  
  Fix: add a dated gate addendum that authorizes only Tier A browser experimentation and states that Phase 0 remains closed for Tier B shell/distribution work.

- `XDMVP-PC-003` — **MAJOR** — Tier A — unsupported human-trial completion strength.  
  Evidence: `docs/research/mvp-human-ui-trial-2026-08-02.md:3`: “BOUNDED HUMAN TRIAL PASSED — feature expansion approved”; lines 87–90 rely on “reported that it works”; lines 92–94 admit “exact human timing/affordance measurements remain separate evidence items.” The governing plan `docs/runbooks/mvp-human-ui-plan.md:283-291` required exact timings, confusion, affordances, latency, and projection-change evidence.  
  Attack: the record proves a human completed the path, but not the planned usability acceptance dataset; “trial passed” overstates what was captured.  
  Fix: rename the result to “bounded workflow completion observed” or attach the missing timing/affordance record before using “trial passed.”

- `XDMVP-PC-004` — **MAJOR** — Tier C — authoritative baseline contradicts current architecture and fidelity evidence.  
  Evidence: `AGENTS.md:92` says `docs/project-spec-v1.md` is the product baseline. That spec says at line 79 the proprietary UI/libgimp arrangement is “explicitly” mere aggregation, line 87 says it is “explicitly permitted,” and line 103 promises “PSD (full read/write with layer fidelity).” In contrast, `README.md:31` says xDivina will not assume standalone libgimp embedding, while `docs/research/phase0-gate-review-2026-08-02.md:19` says fourteen advanced PSD capabilities remain Unknown and distribution/license review is open at line 20.  
  Attack: a still-authoritative baseline contains obsolete architecture, categorical legal conclusions, and unsupported PSD capability wording.  
  Fix: mark the original spec as historical intent and publish a current product contract that references ADR/evidence outcomes and labels legal/fidelity claims as unresolved.

- `XDMVP-PC-005` — **MAJOR** — Tier B — no single coherent desktop-MVP acceptance contract.  
  Evidence: `docs/plans/foundation-and-mvp.md:437` defines the relevant user outcome: “A non-developer can complete the vertical slice from the proprietary UI on a clean test installation with no manual GIMP or ComfyUI configuration.” But `docs/plans/editor-core-and-feature-roadmap.md:104-110` calls Phase A plus a Phase B browser slice the “current implementation task,” without connecting it to packaging, clean install, sidecar setup, or offline acceptance.  
  Attack: substantial Editor Core work can accumulate without moving the product toward the distributable single-user MVP gate.  
  Fix: define one Tier B MVP work package whose exit is clean-machine install → launch → representative edit → save/reopen/export → uninstall, with explicit platform and offline criteria.

- `XDMVP-PC-006` — **MAJOR** — Tiers A/B — feature-surface expansion precedes the smallest user outcome.  
  Evidence: `docs/plans/editor-core-and-feature-roadmap.md:63-67` requires a “complete tool/panel/menu inventory” before its exit, while `apps/mvp-ui/README.md:69-72` exposes paint, retouch, vector/type, Channels, Paths, AI, etc.; lines 90–97 acknowledge many are disabled.  
  Attack: this is excessive Tier A surface and false-affordance risk while Tier B’s clean-install representative workflow is absent. It spends scope on professional-editor comprehensiveness rather than proving one distributable user outcome.  
  Fix: demote comprehensive chrome to later discovery; keep only controls needed for the chosen representative MVP task plus a compact capability/limitations view.

- `XDMVP-PC-007` — **MAJOR** — Tiers A/B — acceptance is operation-centric rather than user-outcome-centric.  
  Evidence: `apps/mvp-ui/README.md:20-63` defines a 19-step verified workflow dominated by individual controls; `docs/plans/editor-core-and-feature-roadmap.md:383-387` requires per-capability technical evidence. Neither defines a representative prosumer composition, expected visual artifact, completion time, recoverability expectation, or user-success threshold.  
  Attack: extensive contract tests can pass without showing that the product solves a meaningful editing task for its named audience.  
  Fix: add one fixture-backed prosumer task with expected XCF/PNG outcome, preservation assertions, time/error budget, and novice completion criterion.

Defended zero-finding coverage:

- CRITICAL findings: zero. Defended because root, AGENTS, trial, UI README, security, and roadmap consistently disclaim production shell, commercial readiness, broad PSD parity, and production security; no pinned file claims release/deployment.
- Enabled UI honesty: zero additional finding beyond `XDMVP-PC-006/007`. `apps/mvp-ui/README.md:90-97` explicitly marks crop, free transform, content painting, text, shapes, filters, PSD breadth, and AI disabled/planned, and narrows Eraser to masks.
- Tier C gate inflation: zero additional finding. Distribution licensing, isolation, second-platform, PSD fidelity, and beta/support gates are appropriately withheld for commercial readiness; the defect is their unresolved relationship to a narrower Tier B MVP, captured in `XDMVP-PC-005`.
- Privacy/local-first fidelity: zero additional finding. The corpus consistently limits current endpoints to loopback and explicitly denies hard same-user isolation; no cloud or private-data readiness claim was found.
- Product implementation/readiness claim: zero. This review is read-only and does not establish implementation, packaging, publication, release, deployment, or production readiness.

Blockers:

- No blocker to completing the review.
- Tier B readiness itself is blocked by missing shell selection/package/install proof, offline enforcement, same-user isolation disposition, distribution licensing, and a coherent representative workflow gate.
- Tier C remains intentionally unproven.

Residue:

- No owner or target-local Inventory match.
- Current commit post-dates the original trial/gate records through extensive editor-core expansion.
- No tests were executed because this attacker lane assessed product-contract fidelity; executable verification belongs to the designated verifier lanes.
- No mutation or external access occurred.

handoff_note: Route `XDMVP-PC-001` through `XDMVP-PC-004` to contract/status reconciliation first. Then require an owner decision on the exact Tier B product slice before using the current roadmap as an MVP-readiness plan; `XDMVP-PC-005` is the central product decision, while `XDMVP-PC-006/007` are scope and acceptance consequences.

## Turing initial

dispatch_id: `2026-08-09-xdivina-mvp-readiness-review`  
step_id: `s1-attack-current-mvp`  
capability_ref: `distill`  
status: `complete_with_findings`

Verified target state:

- Repository: `projects/xdivina`
- `HEAD`: `755b09aa6681e0a6ef2d7fed3707dcfe877efc39`
- Branch: `main`
- `origin/main`: same commit
- `git status --short`: empty
- Index/worktree diffs: clean
- No files written; temporary SQLite test data was confined to an auto-cleaned `/tmp` directory.

Corpus resolution and coverage:

- The manifest has 55 actual target paths plus 3 boundary metadata lines.
- All 55/55 paths are unique, tracked, and resolve at the pinned commit.
- Entire resolved corpus accounted for: 12,865 lines, approximately 653 KB.
- The initial naive parser treated `repository:`, `commit:`, and `required_state:` as paths; corrected parser explicitly excluded metadata before coverage accounting.
- Inventory evidence was treated only as discovery context, not xDivina proof.

Commands and results:

- `git -C projects/xdivina rev-parse HEAD; branch --show-current; status --short; rev-parse origin/main; diff --quiet; diff --cached --quiet` — PASS, exact clean pinned state.
- Per-path `git ls-tree` resolution — PASS, 55/55 tracked targets.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest scripts.test_mvp_gateway scripts.test_gimp_adapter scripts.test_event_store tests.integration.security.test_network_policy tests.integration.psd.test_report tests.integration.comfy_smoke.test_run_smoke -v` — 109 tests: 103 PASS, 6 ERROR because this review sandbox denies socket creation (`PermissionError: [Errno 1] Operation not permitted`). The affected checks are four gateway HTTP tests, one adapter TCP-authentication test, and one loopback-listener test; classified unavailable here, not product failures.
- `node --check` on the MVP UI and all Electron JS/CJS files — PASS.
- Python `ast.parse` over all 16 corpus Python files — PASS.
- `git diff --check` — PASS.
- `python3 -m unittest discover -v` — exits successfully but reports `Ran 0 tests`; this confirms the documented discovery limitation.
- Two focused temporary-DB probes reproduced event-loss bugs described below.

Evidence-kind labels:

- `static`: complete over the declared corpus.
- `unit`: 103 passing assertions; 6 socket-dependent checks unavailable.
- `fixture`: gateway/adapter doubles, PSD report fixture, Comfy harness fixture, and temporary SQLite probes only.
- `browser`: unavailable; no already-running bounded service.
- `live-GIMP`: unavailable; no already-running bounded service and persistent process startup forbidden.
- Historical browser/GIMP records were read but not promoted to current execution evidence.

Enabled-action trace matrix:

| Enabled MVP action | UI selector / route | Gateway → adapter | State/persistence evidence | Current evidence |
|---|---|---|---|---|
| Open fixture/upload | `#open-fixture`, `#file-input`; `/api/document/open` | `document.open` | staged session input; normalized document/layers/history | static + fixture unit |
| Preview | preview projection; `/api/preview/{document_id}` | `document.preview` | opaque document ID; path-redacted response | static; HTTP test unavailable |
| Layer create/rename/visibility/opacity/reorder/duplicate/group/delete | selectors at `app.js:1762-1792` | semantic `/api/layers/*` → `layer.*` | gateway layer tree plus adapter history | static + fixture unit |
| Move/rotate/flip | canvas drag/buttons | semantic transform routes → adapter operations | bounds reconciled; selection guards | static + fixture unit |
| Rectangle/ellipse/polygon selections | marquee/lasso canvas handlers | `/api/selection/*` → `selection.*` | semantic selection in history and document projection | static + fixture unit |
| Masks | add/remove/toggle/show/density/invert/brush/eraser selectors | `/api/layers/mask/*` → `layer.mask-*` | semantic mask projection and bounded history | static + fixture unit |
| Undo/redo | `#undo-document`, `#redo-document`, keyboard | history route → `document.undo/redo` | adapter history adopted; local fallback exists | static + fixture unit |
| Save/reopen/export | `#save-xcf`, `#close-reopen`, `#export-png` | `document.save/close/open/export` | opaque artifacts; XCF canonical; PNG export | static + fixture unit; live persistence unavailable |
| Cancellation/recovery | `#cancel-operation` | operation request ID → cancel route → adapter restart | active-operation state cleared and health refreshed | static + fixture unit; live recovery unavailable |
| Error recovery | `runMutationOperation`/sanitized gateway errors | structured semantic errors | previous document retained by tested paths | static + fixture unit |
| Event store | control-plane write API, not editor UI action | direct SQLite `EventStore` | intended append-only activity/task transitions | static + unit + reproducer; defects below |
| Planned/disabled affordances | menu inventory at `app.js:49-55`; UI disable rules | no semantic route | visible planned/disabled labels | static only |

Findings:

1. `XDM-EXEC-001` — **MAJOR**, affected tier: Tier 3 production/control-plane readiness  
   File/selector: `scripts/event_store.py:1-6`, “Idempotent event writes keyed on `(source, event_id)`”; schema at `scripts/event_store.py:52-54`, `event_id TEXT PRIMARY KEY`.  
   Command evidence: appending ID `same` from `source-a` then `source-b` returned two apparent success objects but stored only one row, from `source-a`.  
   Impact: events from distinct producers collide globally, contradicting the declared identity contract and silently dropping activity.  
   Fix: make `(source, event_id)` the database uniqueness key and return the persisted row/explicit duplicate result; add a cross-source collision regression test.

2. `XDM-EXEC-002` — **MAJOR**, affected tier: Tier 3 production/control-plane readiness  
   File/selector: `scripts/event_store.py:155-157`, `event_id=f"transition-{task_id}-{now}"`; `utc_now()` has one-second precision at lines 23-24. Test gap: `scripts/test_event_store.py:141-154` validates final state but never event count.  
   Command evidence: four valid transitions `planned → ready → active → review → done` in one second produced final state `done` but only one stored event, “planned -> ready.”  
   Impact: the advertised append-only lifecycle audit trail silently loses later transitions during ordinary rapid updates; the 17-test suite passes this false positive.  
   Fix: generate collision-resistant transition IDs (UUID or monotonic/nanosecond identity), transact state+event atomically, and assert four persisted events in the full-chain test.

3. `XDM-EXEC-003` — **MAJOR**, affected tier: Tier 1 bounded browser MVP claim  
   File/quote: `README.md:120`, “A human usability trial is still pending”; contradicted by `docs/runbooks/mvp-human-ui-plan.md:3`, “PHASE 4 COMPLETE — bounded human trial passed,” and `docs/research/mvp-human-ui-trial-2026-08-02.md:3-10`, “BOUNDED HUMAN TRIAL PASSED.”  
   Command evidence: exact `nl -ba` comparison at the pinned commit.  
   Impact: the primary current-status entry point understates completed bounded evidence and conflicts with its linked authority record. It also makes the repository’s current gate state ambiguous.  
   Fix: update README to say the bounded trial passed while retaining the explicit non-production, non-shell, non-parity ceiling.

4. `XDM-EXEC-004` — **MINOR**, affected tier: all test/readiness reporting tiers  
   File/quote: `docs/runbooks/mvp-human-ui-plan.md:331-332`, “repository-wide `unittest discover` limitation”; `docs/research/mvp-human-ui-trial-2026-08-02.md:61-62`, “intentionally does not use automatic test discovery.”  
   Command evidence: `python3 -m unittest discover -v` returned success with `Ran 0 tests`.  
   Impact: a conventional green discovery command is a false positive and can be mistaken for test coverage by fresh agents or CI.  
   Fix: add a repository-owned test runner/Make target that invokes explicit modules and fails when zero tests are collected, or package tests for discovery.

Defended zero-finding coverage:

- Gateway/semantic-adapter contract: no additional finding after tracing every enabled UI route; no raw GIMP IDs, PDB expressions, capability tokens, or session paths were found in browser projections.
- Editor state ownership: no additional finding; browser owns transient viewport/tool/dialog state, gateway owns sanitized document projection, adapter owns semantic backend/history state.
- Save/reopen/export: no static/fixture defect found; opaque artifact registration and XCF/PNG boundaries are explicit. Live fidelity remains unavailable.
- History/selections/masks: no additional contract mismatch found in current code; gateway and adapter unit paths cover semantic projection, guards, and bounded history. Live GIMP fidelity unavailable.
- Cancellation/error recovery/cleanup: no additional static or fixture finding; temporary session and incomplete-output cleanup paths exist and unit tests cover cancellation cleanup. Process cleanup was not live-verified.
- Disabled/planned affordances: no false enabled routes found for PSD, cut/copy/paste, image/canvas size, color/profile, advanced selection, filters, or rulers/snapping.
- Shell/distribution: no executable distributable desktop claim found; Electron remains a spike and Tauri/second-platform gates remain open.
- Network/security: literal loopback validation exists; socket-backed verification unavailable in this sandbox and was not substituted with fixtures.
- Live browser/GIMP: explicitly unavailable, therefore no zero-finding claim about current visual behavior, real XCF fidelity, latency, process cleanup, or same-user isolation.

Blockers:

- Sandbox prohibits socket creation, preventing six bounded HTTP/TCP checks.
- No already-running bounded browser or GIMP service; starting persistent services was forbidden.
- Therefore current live browser/GIMP, process cleanup, and visual/usability claims remain unverified in this dispatch.

Residue:

- Re-run the six socket-backed tests in a host permitting loopback sockets.
- Run the three declared live suites and browser suite on the pinned commit with GIMP 3.0.4 and pinned Chromium.
- Fix and regression-test the two event-store loss modes.
- Reconcile README human-trial wording.
- No implementation, publication, deployment, distribution, or production-readiness authority follows from this receipt.

handoff_note: Current static and dependency-free evidence supports a substantial candidate-local browser/editor-core contract, but the event store loses legitimate events and the current README contradicts the passed bounded human trial. Tier 3 readiness is blocked; Tier 1/2 live confidence remains bounded by unavailable socket, browser, and GIMP execution.

## Ahrens initial

dispatch_id: `2026-08-09-xdivina-mvp-readiness-review`  
step_id: `s1-attack-current-mvp`  
capability_ref: `distill`  
status: `complete_with_findings`

## Verified target state

- Repository: `projects/xdivina`
- `HEAD`: `755b09aa6681e0a6ef2d7fed3707dcfe877efc39`
- Branch: `main`
- `origin/main`: `755b09aa6681e0a6ef2d7fed3707dcfe877efc39`
- `git status --porcelain=v1`: empty
- Result: exact pinned commit, clean, and aligned with `origin/main`.

## Commands executed

- `git rev-parse HEAD`
- `git branch --show-current`
- `git rev-parse origin/main`
- `git status --porcelain=v1`
- `git cat-file -e <commit>:<path>` for every manifest target
- `git show <commit>:<path>` and bounded line/selector inspection across the corpus
- `rg -n` operability/security/distribution/accessibility searches
- `python3 -m unittest scripts.test_mvp_gateway scripts.test_gimp_adapter scripts.test_event_store tests.integration.security.test_network_policy tests.integration.comfy_smoke.test_run_smoke tests.integration.psd.test_report -v`
- `node --check apps/mvp-ui/app.js`
- `python3 -m py_compile scripts/mvp_gateway.py scripts/gimp_adapter.py scripts/event_store.py scripts/serve_control_plane.py scripts/network_policy.py`
- `git diff --check`
- Runtime discovery with `command -v python3 node npm git gimp-console gimp`
- `python3 scripts/mvp_gateway.py --host 127.0.0.1 --port 4174`

No dependency installation, network access, writes, Git mutation, or live external sidecar use occurred.

## Corpus resolution and coverage

- Manifest targets: 55
- Resolved at pinned tree: 55
- Missing: 0
- Aggregate corpus size: 19,798 lines
- Coverage: root contracts, plans/runbooks/research, architecture/security/ADRs, browser and Electron surfaces, five runtime modules, unit/live/security/PSD/ComfyUI tests.
- Target-local Inventory is absent; no Inventory claim was treated as authority.

## Fresh-machine / first-user walk

The repository’s general bootstrap works for documentation/control-plane review: Python, Node, npm, and Git are present. It does not provide a fresh-machine path to the actual editor MVP.

The documented MVP launch command failed immediately with sanitized output:

> `{"status": "error", "error": {"code": "gateway_start_failed", "message": "Gateway failed to start"}}`

Neither `gimp-console` nor `gimp` was available. The failure was safe and did not expose paths, but gave the user no actionable prerequisite diagnosis.

The static Python/JavaScript checks passed. The combined test run executed 109 tests: 103 passed and six errored solely because this review sandbox prohibits socket creation (`PermissionError: [Errno 1] Operation not permitted`). This is validation residue, not evidence of a product regression.

## Boundary evidence matrix

| Attacked area | Evidence | Conclusion |
|---|---|---|
| Launch/understanding | Fresh runbook covers control plane, not editor gateway prerequisites | Browser tier not fresh-machine operable |
| Work retention | Session and artifacts live under `TemporaryDirectory`; shutdown cleans it | Safe cleanup, but retention requires explicit download |
| Recovery | Cancellation/restart and prior-document preservation are tested | Bounded browser recovery supported |
| Loopback vs same-user | Policy explicitly says loopback is not authentication | Desktop/production blocker remains |
| Offline | Policy requirements exist; enforcement explicitly unproved | Desktop/production blocker |
| ComfyUI | Model-free smoke only; direct same-user reachability confirmed | Not production-authorized |
| Temp/logs | Owned temporary roots clean on orderly shutdown; GIMP log is inside runtime root | Orderly cleanup supported; crash/log negative proof incomplete |
| Shell/platform | Electron Linux-only spike; 100MP zoom non-interactive; Tauri/second platform absent | No distributable shell decision |
| PSD | One 32×24 composite; advanced features unknown/degraded | Honest narrow evidence only |
| Licensing | No root license; transitive/sidecar notices and distribution decision open | Distribution blocked |
| Accessibility | Semantic labels exist; dialog keyboard containment is absent | Baseline, not conformance |
| Human evidence | One user reports bounded flow works; no exact timing/affordance measurements | Capability signal, not usability readiness |

## Three-tier status

- Bounded browser tier: **BLOCKED for fresh-machine/non-developer MVP readiness**, though the implemented local workflow has substantial contract evidence.
- Distributable desktop tier: **BLOCKED**.
- Production readiness: **BLOCKED**.

## Findings

**AHR-001 — MAJOR — bounded browser tier**  
`docs/runbooks/fresh-machine-agent.md:42`: “GIMP ... [is] not required for the current documentation and control-plane prototype.” The runbook then launches only the control plane at lines 123–135. Conversely, `apps/mvp-ui/README.md:12-17` instructs launching `mvp_gateway.py`, which requires GIMP. Actual command returned `gateway_start_failed`, with no prerequisite guidance.  
Fix: add a dedicated editor-MVP bootstrap section with GIMP version/path probe, expected failure messages, exact launch/stop steps, and a no-GIMP fallback explanation.

**AHR-002 — MAJOR — bounded browser tier**  
`scripts/mvp_gateway.py:309-320,355-368` creates session inputs/outputs in a temporary directory and deletes the owned root on shutdown. The UI calls the operation “Save XCF,” while durable retention exists only if the user follows the artifact download link. A non-developer can reasonably interpret “Save” as persisted locally and lose work on shutdown/crash.  
Fix: label the action “Create downloadable XCF,” require/confirm download before close, and visibly warn that gateway-session artifacts are ephemeral.

**AHR-003 — CRITICAL — distributable desktop and production tiers**  
`docs/security/local-network-policy.md:29-38`: “Another process running as the same user can connect” and ComfyUI needs “an authenticated proxy, sandbox, or verified private network namespace.” Lines 67–69 confirm no token/proxy. Loopback is network locality, not principal isolation.  
Fix: place ComfyUI behind a per-session authenticated xDivina proxy or verified OS-private transport/sandbox, then add unauthorized same-user tests.

**AHR-004 — CRITICAL — distributable desktop and production tiers**  
`docs/security/local-network-policy.md:80-82`: tests “do not prove ... offline network enforcement.” The threat model requires disabling update checks, downloads, telemetry, cloud nodes, and unapproved custom nodes, but contains no enforced runtime profile.  
Fix: implement a fail-closed offline execution profile with observed negative network tests covering shell, sidecars, updates, models, and custom nodes.

**AHR-005 — MAJOR — distributable desktop and production tiers**  
`LICENSES/README.md:9-14`: no root license; process separation is “not a legal conclusion”; software/model/custom-node terms require separate review. `docs/research/dependency-matrix.md:45-58` leaves pins, notices, legal review, and release checking open.  
Fix: freeze the shipped component graph, generate transitive notices/source obligations, decide the application license/distribution model, and gate packaging on reviewed records.

**AHR-006 — MAJOR — distributable desktop tier**  
`docs/research/shell-benchmark-2026-08-02.md:23-24` records 862 ms average and 1017.2 ms maximum 100MP zoom. Lines 34–41 show no Tauri launch or second platform; lines 56–59 leave accessibility, packaging, dialogs, and sidecar permissions unproved.  
Fix: test a tiled/preview rendering path, complete native Tauri and second-platform probes, then select and package one shell.

**AHR-007 — MAJOR — distributable desktop and production tiers**  
`docs/compatibility/psd-capability-matrix.md:15-31` proves only a 32×24 composite while most layer, mask, text, color, profile, and metadata behavior is Target/Unknown/Degrade.  
Fix: keep PSD import/export outside general MVP claims until representative fixtures produce user-visible per-feature loss reports and confirmation gates.

**AHR-008 — MAJOR — bounded browser tier**  
`apps/mvp-ui/index.html:227-269` declares modal dialogs. `apps/mvp-ui/app.js:1375-1399,1559-1564,1821-1828` manages initial/Escape focus but contains no Tab/Shift-Tab focus trap or inert background handling; the scope dialog closes by focusing its own now-hidden close button rather than the invoking control.  
Fix: implement standards-based modal focus containment, background inertness, and reliable invoker-focus restoration; add keyboard browser tests.

**AHR-009 — MAJOR — bounded browser evidence integrity**  
`README.md:120` says “A human usability trial is still pending,” while `docs/research/mvp-human-ui-trial-2026-08-02.md:3,87-94` says the bounded trial passed but exact timing/affordance measurements remain separate. The contradiction prevents a first user from knowing the current gate.  
Fix: reconcile status language and name the result precisely as one bounded workflow acceptance, not general usability validation.

## Defended zero-finding coverage

- GIMP semantic boundary: zero additional finding; adapter capability, session-root confinement, semantic projection, and path-redaction evidence are coherent.
- Orderly temporary cleanup: zero additional finding; gateway and adapter-owned temporary roots are explicitly cleaned on normal shutdown.
- Gateway logging: zero additional finding; HTTP request logging is suppressed and runtime paths are tested absent from projections.
- PSD warning honesty: zero claim-inflation finding; the matrix consistently labels unknown/degraded features. The blocker is breadth, not dishonest wording.
- Current browser dependency footprint: zero finding; the UI is dependency-free and avoids packaging assumptions.
- Cancellation/basic recovery: zero finding; contract and browser tests cover cancellation, adapter restart, health recovery, and preservation of prior projection.
- Enabled-vs-planned UI controls: zero finding; unsupported tools are disabled or marked planned.

## Blockers and residue

Blockers: editor-specific fresh-machine bootstrap, durable-save semantics, ComfyUI same-user protection, enforced offline mode, desktop rendering/shell/platform evidence, distribution/license closure, PSD breadth, modal accessibility, and reconciled human-trial status.

Residue: live socket tests could not run under the sandbox; GIMP/ComfyUI/browser live behavior was not rerun; no second-platform, packaging, installer, crash-cleanup, or real offline observation occurred.

handoff_note: Route fixes to separately authorized browser-operability, security/offline, distribution, and desktop-shell work. This receipt provides review evidence only and grants no implementation, promotion, distribution, or production-readiness authority.

## Fong robot-talk final

dispatch_id: `2026-08-09-xdivina-mvp-readiness-review`  
step_id: `s2-robot-talk-final-position`  
identity: `Fong / Brendan — product-contract attacker`  
status: `complete_with_reconciled_position`

changed_or_corrected:

- I withdraw my initial “zero CRITICAL findings” conclusion for Tiers B/C. Ahrens establishes two release-boundary failures—same-user ComfyUI access and absent enforced offline mode—that are CRITICAL if xDivina is represented as a distributable or production-ready local-first product. They do not invalidate the bounded Tier A browser harness.
- Turing’s statement that `python3 -m unittest discover -v` “exits successfully” is rejected. Governance revalidation proves exit `5`, `Ran 0 tests`, `NO TESTS RAN`. The zero-test discovery hazard remains real, but no green-command premise survives.
- My initial contract analysis did not include executable event-store defects, fresh-machine launch failure, ephemeral-save semantics, or modal focus defects. I accept those findings within their stated tiers after confronting the other lenses.
- Tier A is narrower than my initial matrix implied: substantial historical/static/fixture evidence exists, but current live browser/GIMP execution was unavailable and fresh-machine non-developer launch failed in Ahrens’s environment.

held:

- The three-tier distinction remains mandatory:
  - Tier A: bounded local browser/GIMP workflow evidence only.
  - Tier B: distributable single-user desktop MVP.
  - Tier C: production/commercial readiness.
- The repository has credible Tier A capability evidence but no basis for Tier B or Tier C readiness.
- `XDMVP-PC-005` remains the central product-contract defect: there is no single coherent, current Tier B MVP acceptance package connecting install, launch, representative editing, durable retention, offline behavior, save/reopen/export, and uninstall.
- Honest disabled controls do not cure excessive scope. I retain `XDMVP-PC-006`: Ahrens/Turing correctly found no falsely enabled backend routes, but a comprehensive professional-editor shell can still distract from the smallest distributable user outcome.
- No receipt grants implementation, acceptance, distribution, release, deployment, or production authority.

Crosswalk:

| Finding ID | Position | Evidence-grounded reason |
|---|---|---|
| `XDMVP-PC-001` | MERGES | Same contradiction as `XDM-EXEC-003` and part of `AHR-009`: root README says trial pending while the trial record says bounded trial passed. |
| `XDMVP-PC-002` | ACCEPTS | Neither executable nor operability lens resolves the chronology: Phase 0 says even narrow UI must wait, yet the bounded trial and Editor Core expansion occurred while Phase 0 remained NOT PASSED. A dated Tier A exception/addendum is still missing. |
| `XDMVP-PC-003` | MERGES | Merge with `AHR-009`: the record supports one human completing the flow, while exact timing and affordance measurements remain explicitly absent; “passed” must remain narrowly qualified. |
| `XDMVP-PC-004` | ACCEPTS | The baseline spec’s categorical libgimp/legal and full-PSD language conflicts with the later adapter direction, open distribution review, and narrow PSD evidence summarized by both other lenses. |
| `XDMVP-PC-005` | ACCEPTS | Ahrens materially strengthens it: editor bootstrap, shell/platform, isolation, offline enforcement, licensing, and packaging are all unresolved. The future clean-install gate is not a current executable Tier B contract. |
| `XDMVP-PC-006` | ACCEPTS | Turing/Ahrens defend enabled-vs-disabled honesty, which I accept; the finding concerns prioritization and false expectation from comprehensive surface breadth, not fabricated routes. |
| `XDMVP-PC-007` | ACCEPTS | Neither other receipt supplies a representative prosumer composition, artifact-quality expectation, completion budget, or novice success criterion. Capability checks remain operation-centric. |
| `XDM-EXEC-001` | ACCEPTS | Turing’s focused reproducer shows the declared `(source,event_id)` identity contract is not represented by the global `event_id` primary key and loses a distinct producer event. Tier C/control-plane impact only. |
| `XDM-EXEC-002` | ACCEPTS | Turing’s four-transition reproducer shows one-second IDs collapse an append-only lifecycle audit trail despite final state reaching done. Tier C/control-plane impact only. |
| `XDM-EXEC-003` | MERGES | Duplicate of `XDMVP-PC-001`; retain one root-status reconciliation finding. |
| `XDM-EXEC-004` | ACCEPTS AS CORRECTED | The zero-test discovery hazard is valid, but its evidence must read: command exited `5`, not successfully. Governance revalidation expressly refutes the green-zero-test premise. |
| `AHR-001` | ACCEPTS | The documented editor launch needs GIMP, but the fresh-machine path covers the control plane and the actual editor launch failed without actionable prerequisite diagnosis. Tier A fresh-machine readiness is therefore blocked. |
| `AHR-002` | ACCEPTS | Gateway state is temporary and durable retention depends on downloading an artifact, while the UI label “Save XCF” can imply persistence. This is a Tier A user-outcome defect, not merely internal cleanup behavior. |
| `AHR-003` | ACCEPTS | Explicit same-user ComfyUI reachability defeats a hard principal-isolation claim. CRITICAL for Tiers B/C; not projected backward onto the disposable Tier A harness. |
| `AHR-004` | ACCEPTS | Policy tests do not prove offline enforcement. A local-first distributable/commercial claim requires fail-closed observed enforcement across shell and sidecars. CRITICAL for Tiers B/C only. |
| `AHR-005` | ACCEPTS | Root licensing, component notices, model/custom-node terms, and release review remain open; therefore packaging/distribution cannot cross Tier B. |
| `AHR-006` | ACCEPTS | Linux Electron evidence is non-interactive at 100MP, with no native Tauri or second-platform proof. It blocks shell selection and Tier B packaging, not Tier A contract work. |
| `AHR-007` | MERGES | Merge its general-MVP claim warning with `XDMVP-PC-004`; current PSD evidence is one narrow composite and cannot support the baseline’s full-fidelity language. PSD need not block a deliberately scoped XCF-first MVP if explicitly excluded. |
| `AHR-008` | ACCEPTS | Static inspection identifies missing modal focus containment/inert background and unreliable focus restoration. This is a bounded Tier A accessibility defect; no broader conformance claim is inferred. |
| `AHR-009` | MERGES | Consolidates `XDMVP-PC-001` and `XDMVP-PC-003`: reconcile the contradiction and describe the evidence as one bounded workflow completion, not general usability readiness. |

Shared conclusions:

- Tier A: substantial semantic editor/gateway capability is supported by pinned static, fixture, historical browser/GIMP, and one bounded human-completion record. It is not currently proven as a fresh-machine/non-developer MVP; current live socket/browser/GIMP replay remained unavailable.
- Tier B: BLOCKED by the absent coherent desktop-MVP contract, editor bootstrap, durable-save semantics, shell/platform choice, packaging, same-user isolation, offline enforcement, and distribution/license closure.
- Tier C: BLOCKED by all Tier B residue plus event-store audit loss, PSD breadth, beta/usability evidence, commercial terms/support/privacy, and production security/performance proof.
- Test claim: the explicit suite is not green in this sandbox—103 passed and six socket-dependent tests errored. Discovery is also not green: exit `5`, zero tests. Neither result is a product regression by itself, and neither may be reported as full validation.
- Unsupported tools are generally marked disabled/planned; the concern is roadmap scope and user-outcome focus, not evidence of fake enabled backend behavior.

remaining dissent:

- I retain CRITICAL severity for `AHR-003/004` only at the Tier B/C claim boundary. Calling the candidate-local Tier A harness itself critically unsafe would exceed the receipts.
- I retain `XDMVP-PC-006` despite the other lenses’ zero false-enabled findings: honest disabling answers truthfulness, while the finding attacks premature surface breadth.
- `XDM-EXEC-001/002` are serious control-plane/production defects but do not block the bounded editor workflow or, absent a requirement to ship that domain store, necessarily block a narrowly defined Tier B editor.
- PSD breadth should block broad PSD migration promises, not automatically an explicitly XCF-first Tier B MVP.
- Corpus line totals conflict between Turing (`12,865`) and Ahrens (`19,798`); 55/55 path resolution is shared, but aggregate line count should not be used as acceptance evidence until separately reconciled.

residue:

- Six socket-dependent tests remain unavailable under the review sandbox.
- Current live GIMP/browser behavior, visual quality, real XCF fidelity, latency, cleanup, and same-user isolation were not replayed.
- The reusable fail-on-zero-tests wrapper remains unapplied governance residue.
- Findings require separately authorized remediation and revalidation; accepted review findings are not accepted product bytes.

handoff_note: Consolidate duplicates into four decision surfaces: (1) current-status/gate reconciliation, (2) one explicit Tier B MVP definition and representative user outcome, (3) Tier B/C security-offline-distribution gates, and (4) executable defects/accessibility/retention repairs. Preserve the Tier A evidence ceiling and reject any summary that calls either the explicit suite or `unittest discover` green.

## Turing robot-talk final

dispatch_id: `2026-08-09-xdivina-mvp-readiness-review`  
step_id: `s1-attack-current-mvp-final-position`  
identity: `Alan Turing — executable-mechanics attacker`  
status: `complete_with_corrected_position`

## changed_or_corrected

- I withdraw `XDM-EXEC-004` as stated. Governance replay proves `python3 -m unittest discover -v` exits **5**, not successfully green. Zero discovery remains a test-layout/workflow limitation, but the command itself fails closed and is not the false-positive success I reported.
- My corpus line total was wrong: the correct accounting is 55/55 files and 19,798 newline-delimited lines. My script incorrectly added one line per file and my receipt then reported an unrelated lower aggregate.
- The explicit 109-test suite’s preserved status is exit **1**: 103 pass and six socket-dependent errors caused by sandbox `PermissionError`. Those six remain unavailable here, not passed and not established product regressions.
- I strengthen my human-trial conclusion after Fong’s attack: the evidence supports one reported bounded workflow completion, not the full timing, confusion, affordance, and latency dataset required by the plan. Merely changing README from “pending” to unqualified “passed” would still overshoot.

## held

- `XDM-EXEC-001` and `XDM-EXEC-002` remain independently reproduced event-loss defects.
- Static and fixture evidence supports a substantial candidate-local Tier A browser/editor-core slice, but current live browser/GIMP fidelity, visual behavior, latency, and cleanup were not re-executed.
- Tier B distributable desktop readiness and Tier C production/commercial readiness remain blocked.
- Inventory, historical receipts, and passing candidate checks confer no implementation, packaging, publication, release, deployment, or production authority.

## finding crosswalk

| Finding | Position | Evidence-grounded reason |
|---|---|---|
| `XDM-EXEC-001` | **ACCEPTS** | The receipt’s temporary-DB reproducer showed two sources using the same event ID collapse to one stored row despite the stated `(source, event_id)` identity contract. |
| `XDM-EXEC-002` | **ACCEPTS** | Four same-second task transitions reached final state `done` while persisting only the first event; the full-chain test checks state but not audit-event cardinality. |
| `XDM-EXEC-003` | **MERGES** with `XDMVP-PC-001`, `XDMVP-PC-003`, `AHR-009` | README says the trial is pending, while later records call it passed; Fong correctly adds that the record lacks several planned usability measures, so the reconciled phrase must be “one bounded workflow completion reported,” not general usability validation. |
| `XDM-EXEC-004` | **REJECTS** as stated | Governance replay records exit 5 with `NO TESTS RAN`; the premise that discovery exits successfully green is false. A dedicated runner remains optional workflow residue. |
| `XDMVP-PC-001` | **MERGES** into the human-evidence/status cluster | It identifies the same exact README-versus-trial contradiction as `XDM-EXEC-003` and `AHR-009`. |
| `XDMVP-PC-002` | **ACCEPTS** | The earlier Phase 0 record conditions even narrow UI work on blocker disposition, while later Tier A expansion lacks an explicit dated exception/addendum preserving the Tier B gate. |
| `XDMVP-PC-003` | **MERGES** into the human-evidence/status cluster | The plan required timings, confusion, affordance, and latency evidence; the trial record admits those remain separate, materially lowering the permissible claim. |
| `XDMVP-PC-004` | **ACCEPTS** | The still-designated product baseline contains categorical libgimp/legal and full-PSD wording contradicted by the current process-boundary architecture, open license review, and mostly unknown PSD matrix. |
| `XDMVP-PC-005` | **ACCEPTS** | The clean-install, non-developer outcome exists in the foundation plan, but the current editor-core roadmap does not bind its browser capability work to one package/install/offline desktop exit contract. |
| `XDMVP-PC-006` | **MERGES** into `XDMVP-PC-005/007` | The broad disabled chrome is honestly labeled, so it is not a false enabled capability; its material defect is scope diversion from the still-undefined Tier B outcome and representative task. |
| `XDMVP-PC-007` | **ACCEPTS** | The documented 19-step path and per-capability evidence are operation-centric and do not specify a representative prosumer artifact, time/error budget, or novice success threshold. |
| `AHR-001` | **ACCEPTS** | The fresh-machine runbook covers documentation/control-plane startup, while the editor gateway requires GIMP and the attempted launch returned only sanitized `gateway_start_failed`; Tier A is not fresh-machine operable from current guidance. |
| `AHR-002` | **ACCEPTS** | Gateway-owned session artifacts are deleted on shutdown, while the UI calls the action “Save XCF”; durable retention depends on a separate download that a non-developer may not understand. |
| `AHR-003` | **ACCEPTS** | The security contract explicitly says another same-user process can connect and ComfyUI lacks the authenticated proxy/private isolation required for Tier B/C. |
| `AHR-004` | **ACCEPTS** | Current tests expressly do not prove offline enforcement; no fail-closed profile establishes that shell and sidecars cannot perform unapproved network activity. |
| `AHR-005` | **ACCEPTS** | Root licensing, transitive notices, model/custom-node obligations, and the distribution decision remain open, directly blocking Tier B/C distribution. |
| `AHR-006` | **ACCEPTS** | The only shell evidence is Linux Electron with non-interactive 100MP zoom; Tauri, packaging, accessibility, permissions, and a second platform remain unproved. |
| `AHR-007` | **MERGES** with `XDMVP-PC-004` | The matrix itself is honest about one tiny composite and unknown/degraded advanced features; the sharper defect is the conflict with the still-authoritative baseline’s full-fidelity promise. |
| `AHR-008` | **ACCEPTS** | The cited dialog code handles opening and Escape but lacks Tab containment, inert background behavior, and reliable invoker-focus restoration; Tier A accessibility evidence is incomplete. |
| `AHR-009` | **MERGES** into the human-evidence/status cluster | It independently establishes the same contradictory gate wording and correctly limits the evidence to one bounded workflow report. |

## shared conclusions

- **Tier A — bounded browser/editor-core slice:** implemented candidate behavior has broad static and fixture-unit coverage, plus historical local GIMP/browser evidence and one reported human workflow completion. It is not yet established as current live, fresh-machine, generally usable, durable-by-default, or accessibility-complete. Current blockers include editor bootstrap, ephemeral-save communication, modal keyboard behavior, and unrerun live checks.
- **Tier B — distributable single-user desktop MVP:** blocked by the absent coherent acceptance package, shell/platform/performance gaps, clean-install proof, same-user isolation, fail-closed offline enforcement, licensing closure, and a representative user-outcome gate.
- **Tier C — production/commercial readiness:** blocked. The authoritative baseline needs reconciliation; PSD breadth, security isolation, offline enforcement, distribution obligations, production AI, support/privacy, deployment, and release evidence remain unproved.
- Event-store defects independently block production-grade control-plane audit claims: legitimate cross-source and rapid-transition events can be silently discarded.
- Unsupported UI affordances are generally labeled planned or disabled. The concern is prioritization and outcome alignment, not evidence that those planned tools secretly execute.
- No CRITICAL Tier A defect was established. The CRITICAL security findings apply to Tier B/C principal isolation and offline guarantees.

## remaining dissent

- I do not retain `XDM-EXEC-004` as a finding: exit 5 defeats the alleged green false positive.
- I treat `XDMVP-PC-006` as a consequence of the missing Tier B/user-outcome contract, not a standalone proof that comprehensive chrome is inherently wrong.
- “Trial passed” remains too strong unless the missing planned measurements are attached. “Trial pending” is also false. The defensible current wording is one reported bounded workflow completion with explicit missing usability evidence.
- Tier A code existence is not itself blocked; **Tier A fresh-machine/non-developer readiness** is blocked. This distinction avoids erasing the substantial bounded implementation evidence while respecting Ahrens’s operability attack.

## residue

- Re-run the six socket-backed checks with loopback sockets permitted, preserving exit status.
- Re-run pinned live GIMP, gateway, and browser suites; capture current cleanup, latency, visual, selection, mask, history, save/reopen, cancellation, and recovery evidence.
- Repair event identity and transition-event generation with regression tests.
- Reconcile Phase 0, root status, trial wording, product baseline, and current roadmap under the three-tier model.
- Define one Tier B clean-install representative-workflow acceptance contract before treating further editor-core expansion as MVP-readiness progress.
- Route security/offline, licensing, shell/platform, durable-save semantics, accessibility, and PSD work through separately authorized follow-up; no repair is authorized by this review.

handoff_note: The attackers converge on a bounded but non-distributable editor-core candidate. Preserve Tier A evidence without inflating it: one reported workflow completion is not general usability readiness. Tier B and Tier C remain blocked, and the event-store loss defects plus unreconciled contracts must be resolved before stronger lifecycle or readiness claims.

## Ahrens robot-talk final

dispatch_id: `2026-08-09-xdivina-mvp-readiness-review`  
step_id: `s1-robot-talk-final-position`  
identity: `Ahrens, Sönke — operability and boundary attacker`  
status: `complete_with_reconciled_findings`

## changed_or_corrected

- I retract my initial statement that “No files were written.” My Python test and `py_compile` commands created ignored `__pycache__/*.pyc` files inside the target. The parent detected and quarantined those bytes at `/tmp/xdivina-review-quarantine.GoQFw5`.
- Governance revalidation then ran with bytecode disabled and caches/output redirected to `/tmp`; its pre/post manifest proves the target is now byte-identical, with no tracked, untracked, ignored, `*.pyc`, or `__pycache__` residue.
- I preserve the explicit-suite result as sandbox-bounded unavailability: 109 tests attempted, 103 passed, six socket-dependent errors, overall exit 1.
- I correct Turing’s claim that `python3 -m unittest discover -v` “exits successfully.” Governance revalidation establishes exit **5**, with `Ran 0 tests` and `NO TESTS RAN`. It is not a green false positive.
- I no longer rely on my 19,798-line aggregate or Turing’s differing 12,865-line aggregate as a substantive claim. All three receipts agree on the material coverage fact: 55 unique manifest targets resolved at the pinned commit.

## held

My final three-tier position remains:

- Tier A — bounded browser/GIMP capability tier: substantial candidate-local workflow evidence exists, but fresh-machine/non-developer readiness is blocked by editor-specific bootstrap, retention semantics, accessibility, status/gate ambiguity, and missing representative task evidence.
- Tier B — distributable single-user desktop MVP: blocked by the absence of one coherent acceptance contract, selected/packageable shell, clean-install proof, second-platform evidence, offline enforcement, same-user isolation disposition, and distribution records.
- Tier C — production/commercial readiness: blocked. Current evidence does not establish production security, commercial distribution, broad PSD fidelity, model-backed AI, support/privacy terms, performance envelope, deployment, or release.

The other lenses strengthen rather than overturn the central operability conclusion: a technically substantial browser contract is not yet a non-developer desktop MVP.

## Crosswalk

| Finding | Position | Evidence-grounded reason |
|---|---|---|
| `AHR-001` | **MERGES** with `XDMVP-PC-005` | The fresh runbook launches the control plane, while the editor gateway requires unavailable GIMP and failed only with sanitized `gateway_start_failed`; this is the bootstrap manifestation of the missing Tier B clean-install contract. |
| `AHR-002` | **ACCEPTS** | Turing found no static save/reopen defect, but that does not answer the usability boundary: owned session outputs are temporary and cleaned at shutdown, so “Save XCF” is durable only after the user downloads the artifact. |
| `AHR-003` | **ACCEPTS** | All lenses preserve the documented distinction between loopback locality and same-user authorization; direct ComfyUI access remains possible without an authenticated proxy/private transport. |
| `AHR-004` | **ACCEPTS** | The corpus explicitly states that offline enforcement is unproved; endpoint validation does not establish a fail-closed offline shell/sidecar profile. |
| `AHR-005` | **MERGES** with `XDMVP-PC-004/005` | No root license, frozen component graph, reviewed transitive notices, or distribution decision exists; the obsolete baseline’s legal conclusions amplify the packaging blocker. |
| `AHR-006` | **MERGES** with `XDMVP-PC-005` | Linux Electron evidence is provisional, 100MP zoom is non-interactive, and Tauri/second-platform/package/install proof is absent. |
| `AHR-007` | **MERGES** with `XDMVP-PC-004` | The current matrix honestly proves only a tiny composite fixture, while the authoritative baseline still promises full PSD read/write with layer fidelity. |
| `AHR-008` | **ACCEPTS** | Semantic labels do not cure the missing modal focus containment/background inertness and unreliable scope-dialog return focus; no other receipt supplied contrary keyboard evidence. |
| `AHR-009` | **MERGES** with `XDMVP-PC-001`, `XDMVP-PC-003`, and `XDM-EXEC-003` | All identify the same status/evidence defect: README says pending, later records say passed, and the record lacks the plan’s timing/affordance dataset. |
| `XDMVP-PC-001` | **MERGES** | Same contradiction as `AHR-009`; reconcile the root status without inflating one bounded completion into general usability readiness. |
| `XDMVP-PC-002` | **ACCEPTS** | The Phase 0 review says narrow UI may begin only after security/shell disposition, yet later browser expansion proceeds without a dated exception/addendum explaining the Tier A-only authority. |
| `XDMVP-PC-003` | **ACCEPTS** | “Reported that it works” proves bounded completion, not the planned timing, confusion, affordance, latency, and projection-change acceptance dataset. |
| `XDMVP-PC-004` | **ACCEPTS** | The still-authoritative original spec conflicts with current process-boundary architecture, unresolved legal review, and narrow PSD evidence; it must be demoted or superseded. |
| `XDMVP-PC-005` | **ACCEPTS** | This is the central Tier B defect: no single contract connects clean install, launch, representative editing, persistence/export, offline behavior, and uninstall. |
| `XDMVP-PC-006` | **ACCEPTS** | Turing correctly found planned controls disabled, so this is not a false-enabled-route defect; it remains a scope/affordance finding because comprehensive professional chrome precedes the smallest user outcome. |
| `XDMVP-PC-007` | **ACCEPTS** | The 19-step operation inventory and per-capability tests do not define a representative prosumer artifact, completion threshold, time/error budget, or novice-success criterion. |
| `XDM-EXEC-001` | **ACCEPTS** | The receipt’s focused reproducer shows the declared `(source,event_id)` identity contract conflicts with a globally primary `event_id`, silently collapsing cross-source events. Keep it Tier C/control-plane, not a Tier A editor blocker. |
| `XDM-EXEC-002` | **ACCEPTS** | The reproducer shows second-resolution transition IDs collapse multiple valid transitions while final state advances; this breaks append-only audit evidence. Keep it Tier C/control-plane. |
| `XDM-EXEC-003` | **MERGES** | Same current-status contradiction as `AHR-009`/`XDMVP-PC-001`; it survives as one consolidated finding. |
| `XDM-EXEC-004` | **REJECTS as phrased** | Revalidation proves discovery exits 5, not successfully. Retain only the narrower residue that default discovery collects zero tests and a repository-owned explicit runner would improve operability; do not call the exact command green. |

## Shared conclusions

- Tier A has meaningful static, fixture/unit, historical live-GIMP/browser, and one-user completion evidence, but none of those automatically establish current fresh-machine or general usability readiness.
- Enabled editor actions are semantically routed and planned actions are visibly disabled; no reviewer found raw GIMP IDs, capability tokens, or local paths exposed to the browser.
- Honest limitations are broadly present, but lifecycle wording is internally inconsistent and the Phase 0-to-browser-expansion authority edge is unreconciled.
- Tier B lacks the owner-level definition that would turn capability accumulation into a distributable non-developer outcome.
- Loopback is not same-user isolation; offline enforcement remains unproved.
- Tier C remains blocked by security, licensing/distribution, PSD breadth, shell/platform/performance, and now two event-store audit-loss defects.
- No receipt proves implementation acceptance, packaging, publication, release, deployment, or production readiness.

## Remaining dissent

- I retain `AHR-002` as an operability finding despite Turing’s zero static defect for save/reopen. We agree the mechanism works; the dissent is whether “Save XCF” adequately communicates that persistence depends on downloading an ephemeral artifact.
- I retain `AHR-008` despite the semantic accessibility baseline. Named controls and live regions are positive evidence, but they do not establish modal keyboard behavior.
- I accept Fong’s `XDMVP-PC-006` only as scope/cognitive-load risk, not as evidence that disabled controls falsely execute.
- Event-store findings are serious but belong to Tier C/control-plane integrity; they should not be used to erase the bounded Tier A editor evidence.

## Residue

- Six socket-backed tests remain unavailable in this sandbox; live browser, GIMP, current visual behavior, real XCF fidelity, latency, crash cleanup, and process isolation were not re-executed.
- Default `unittest discover` collects zero and exits 5; the proposed explicit test wrapper remains unapplied governance residue.
- The bytecode contamination from my initial commands was quarantined and the target was proven byte-identical afterward.
- Corpus line-count disagreement is non-material; use 55/55 pinned-path resolution as the coverage claim.
- No target-local Inventory exists, and Inventory would not substitute for pinned-source evidence in any case.

handoff_note: Consolidate overlapping findings before verification: one status/human-evidence finding; one Phase 0 exception/authority finding; one current-product-contract finding; one Tier B acceptance-contract finding; then retain the distinct bootstrap, ephemeral-retention, modal-accessibility, same-user, offline, shell, licensing, PSD, representative-task, scope, and two event-store findings. Any fixes require a separately authorized candidate and revalidation; this final position grants no mutation, acceptance, packaging, publication, release, deployment, or production authority.

## Gödel verifier initial

dispatch_id: `2026-08-09-xdivina-mvp-readiness-review`  
step_id: `s3-verify-findings`  
capability_ref: `ux-evidence-validator`  
identity: `Gödel, Kurt — scope-attack verifier`  
status: `complete`

Target / coverage checks:

- `git -C projects/xdivina rev-parse HEAD` → `755b09aa6681e0a6ef2d7fed3707dcfe877efc39`
- `git -C projects/xdivina status --short` → empty
- Corpus path count from `review-corpus.txt` → `55`
- Finding IDs → contiguous `XD-F001`–`XD-F013`
- No product tests, Python, writes, network, or mutation performed.

| ID | Decision | Citation result | Tier / severity result | Exact reason |
|---|---|---|---|---|
| `XD-F001` | **KEEP** | Confirmed: `README.md:120` says trial pending; trial record `:3,87-94` says bounded trial passed while timing/affordance evidence remains separate; plan `:283-291` requires those measurements. | MAJOR / A is proportionate as a readiness-status contradiction, not a general usability failure. | Current root status is stale and conflicts literally with the completed bounded trial. The finding preserves the correct claim ceiling. |
| `XD-F002` | **KEEP** | Confirmed: Phase 0 `:42-43` permits narrow UI only after blocker disposition; `:55-57` explicitly preserves unresolved blockers and unchanged gate result; later trial `:3` approves feature expansion. | MAJOR / A-B is proportionate because this is a missing authority/scope edge, not proof Phase 0 passed. | The current corpus contains no dated authority record explaining how “feature expansion approved” remains bounded under the unchanged failed gate. |
| `XD-F003` | **KEEP** | Confirmed: target `AGENTS.md:92-95` names v1 baseline; spec `:79,87,103-104` makes categorical legal/full-PSD claims; `README.md:31` rejects standalone libgimp embedding; Phase 0 `:19-20` records PSD/license gaps. | MAJOR / C and broad-PSD Tier B only is correctly bounded. | The authoritative-baseline wording conflicts with current architecture and evidence ceilings. |
| `XD-F004` | **KEEP** | Confirmed: foundation plan `:437` requires clean-install non-developer completion and offline test; roadmap `:104-110` is browser/editor work; benchmark `:56-59` leaves shell, packaging, permissions, and second-platform evidence open. | MAJOR / B is correct. | No current distributable desktop end-to-end acceptance contract or proof exists. “Uninstall” is a proposed gate detail, not an already-authoritative requirement, but does not refute the core finding. |
| `XD-F005` | **DROP** | Cited facts are accurate, but the conclusion is unsupported. `apps/mvp-ui/README.md:20-63` already defines a coherent 19-step representative workflow, and the trial `:87-90` records one human completion. | MAJOR / A-B is inflated; a named novice cohort and numerical success budget are not established current MVP requirements. | This converts absent usability research into a blocking defect and duplicates `XD-F004`. The evidence supports residue/future study, not this standalone MAJOR finding. |
| `XD-F006` | **DROP** | Citations confirm deliberate breadth: roadmap `:63-67,104-110`; UI README `:67-72,90-97` says only verified actions are enabled and planned actions remain disabled. No observed cognitive-load failure is cited. | MAJOR / A-B is inflated. Under the validator contract, subjective cognitive-load claims remain soft/human-study residue without calibration. | The requested narrowing directly contests an explicit current design goal without user evidence. Honest disabled controls and completed bounded workflow refute a defect claim. |
| `XD-F007` | **KEEP** | Confirmed: gateway `:309-320,355-368` owns and deletes temporary inputs/outputs; UI labels the operation “Save XCF”; README `:59-60` separately instructs downloading the artifact. | MAJOR / A is defensible as destructive-close/retention communication, not persistence implementation failure. | The downloadable path exists, but there is no cited warning before shutdown/close with an undownloaded temporary artifact. |
| `XD-F008` | **KEEP** | Confirmed: dialogs are modal in HTML `:227-269`; JS `:1375-1399,1559-1564,1821-1828` has initial/Escape handling but no Tab trap/inert behavior. Scope close focuses `#close-scope` after hiding its dialog. `git grep` found no `inert` or Tab containment. | MAJOR / A is appropriate keyboard-access severity. | Literal implementation defect: focus can escape and scope-dialog close returns focus into hidden content. |
| `XD-F009` | **KEEP** | Confirmed: network policy `:23,29-38,67-69` states unauthenticated ComfyUI and demonstrated same-user reachability. | CRITICAL only at B-C is correctly constrained; it does not block disposable Tier A. | The policy itself calls this an explicit production blocker. Tier B relevance remains conditional on the shipped graph including ComfyUI. |
| `XD-F010` | **KEEP** | Confirmed: policy `:80-82` explicitly disclaims offline enforcement and complete sandbox proof. | CRITICAL only at B-C is correct for a packaged local-first/offline claim. | Required negative enforcement evidence is absent; no Tier A invalidation is claimed. |
| `XD-F011` | **KEEP** | Confirmed: `LICENSES/README.md:9-14`; dependency matrix `:42-57` leaves app/model licenses, notices, legal review, and release checks open. | MAJOR / B-C is correct. | Distribution clearance is explicitly absent. |
| `XD-F012` | **KEEP** | Defect confirmed. `event_store.py:52-54` uses globally unique `event_id`; `:92-100` silently ignores collisions. The draft’s cited range omits the contract text, but the same file `:5` and control-plane contract `:149` specify `(source,event_id)`. | MAJOR / C control-plane is correct and does not block Tier A/B unless selected packaging depends on this store. | Cross-source same-ID loss follows directly from schema plus `INSERT OR IGNORE`; current returned payload does not disclose persistence truth. |
| `XD-F013` | **KEEP** | Confirmed: `utc_now()` at `:23-24` has one-second resolution; transition ID at `:155-157` therefore collides for same-task rapid transitions; test `:141-154` checks final state only, not audit cardinality. | MAJOR / C control-plane is correct. | Silent audit loss can coexist with correct final state. The collision defect is statically established; the earlier focused reproducer is supporting evidence, not required for the inference. |

Disposition: **11 KEEP, 2 DROP**. `XD-F005` and `XD-F006` must not survive in softened form.

Three-tier/status verification:

- Tier A: “implemented candidate; readiness blocked” is supportable. It must not be rewritten as “trial pending,” general usability validation, fresh live replay, or shell readiness.
- Tier B: **BLOCKED** is supported by clean-install, shell/package, offline/security, and licensing gaps.
- Tier C: **BLOCKED** is supported. Event-store findings remain C/control-plane only unless a Tier B package explicitly depends on that store.
- The two CRITICAL findings are valid only at B/C claim boundaries. No CRITICAL Tier A defect was established.
- PSD breadth blocks broad migration/fidelity claims, not a scoped XCF-first MVP.

Missing-current-evidence / feedback edge:

- Dropped `XD-F005` would require an owner-selected representative prosumer outcome plus current cohort/task-threshold evidence before resurrection.
- Dropped `XD-F006` would require calibrated browser comparison or human usability evidence showing that the deliberate disabled-control inventory harms the selected task.
- Therefore the declared feedback edge is necessary only if authors seek to restore either finding; neither can remain in the present consolidated set.
- Current live browser/GIMP replay remains missing but is already disclosed as residue; it does not refute the static contradictions and deterministic code findings retained here.

Zero-findings red flag: tested and not triggered. A nonzero result is not intrinsically proof of review quality; after scope attack, 11 independently supportable findings remain. Retaining all 13 would itself violate the anti-inflation requirement.

Claim ceiling: this receipt verifies current pinned text/code evidence only. It does not establish implementation acceptance, packaging, publication, release, deployment, production, commercial readiness, comprehensive accessibility, or user success.

Blockers: none for verification completion.  
Residue: no current runtime/browser replay; no independent legal determination; no calibrated usability study.  
handoff_note: Wave 3 synthesis should remove `XD-F005` and `XD-F006` entirely, retain the remaining 11 with their existing tier ceilings, and ensure `XD-F012` cites the actual `(source,event_id)` contract line rather than implying that declaration occurs at schema lines `52-54`.

## Popper verifier initial

dispatch_id: `2026-08-09-xdivina-mvp-readiness-review`  
step_id: `s3-verify-findings`  
capability_ref: `ux-evidence-validator`  
identity: `Popper / executable counter-example lens`  
status: `complete`

Target/tree integrity:

- `git -C projects/xdivina rev-parse HEAD` → `755b09aa6681e0a6ef2d7fed3707dcfe877efc39`
- Complete file SHA-256 manifest before/after all checks → `cmp` exit `0`
- Final `git status --short --ignored` → empty
- No target writes, services, network, dependency installation, or subagents.

| Finding | Verdict | Exact command/evidence and counterexample result | Evidence kind |
|---|---|---|---|
| XD-F001 | KEEP | `rg -n "pending|BOUNDED HUMAN|timing|affordance" README.md docs/research/mvp-human-ui-trial-2026-08-02.md docs/runbooks/mvp-human-ui-plan.md` reproduces root “trial pending,” trial “BOUNDED HUMAN TRIAL PASSED,” and separate missing timing/affordance measurements. Neither extreme wording survives reconciliation. | Current static contract contradiction; human-study residue |
| XD-F002 | KEEP | `rg -n "NOT PASSED|feature expansion" docs/research/phase0-gate-review-2026-08-02.md docs/research/mvp-human-ui-trial-2026-08-02.md` reproduces failed Phase 0 and later feature-expansion approval without a current authority addendum. | Current governance evidence |
| XD-F003 | KEEP | `rg -n "full PSD|legal|libgimp|Unknown" AGENTS.md docs/project-spec-v1.md README.md docs/research/phase0-gate-review-2026-08-02.md` reproduces baseline-level broad promises against current architecture, legal uncertainty, and 14 unknown PSD capabilities. | Current static contract/evidence conflict |
| XD-F004 | KEEP | `rg -n "clean test installation|Electron|offline|uninstall" docs/plans/foundation-and-mvp.md docs/research/shell-benchmark-2026-08-02.md` shows the clean-install contract but only a provisional Linux Electron spike; no package/install/uninstall proof. | Current contract plus missing live/package evidence |
| XD-F005 | KEEP | `apps/mvp-ui/README.md:20-63` and roadmap `:383-387` remain operation/capability inventories, not a fixture-backed representative prosumer outcome with budgets or novice evidence. | Current static evidence; human-study residue |
| XD-F006 | KEEP | `rg -n "disabled|planned" apps/mvp-ui/index.html apps/mvp-ui/app.js` reproduces broad professional chrome and honest disabled/planned states. No disabled action was treated as executable. Standalone scope dissent remains valid. | DOM/source-observable proxy; usability residue |
| XD-F007 | KEEP | `nl -ba scripts/mvp_gateway.py \| sed -n '280,390p'` shows temporary session ownership and cleanup at shutdown; `index.html` still labels the action “Save XCF.” Fixture test `test_save_close_reopen_export_use_opaque_artifacts` passed, but it cannot falsify loss after cleanup without prior download. | Deterministic static/runtime-fixture boundary |
| XD-F008 | KEEP | `nl -ba apps/mvp-ui/app.js \| sed -n '1360,1410p;1545,1570p;1810,1835p'` shows initial focus and Escape handling, but no Tab containment/inert background; scope close focuses `#close-scope` after hiding its dialog. | Deterministic source counterexample; browser replay unavailable |
| XD-F009 | KEEP | `rg -n "loopback|authentication|same user" docs/security/local-network-policy.md` confirms ComfyUI loopback-only/no authentication and same-user reachability. Correctly CRITICAL only for Tier B/C. | Current security contract; live isolation unavailable |
| XD-F010 | KEEP | `rg -n "offline|complete process sandbox" docs/security/local-network-policy.md` explicitly says tests do not prove offline enforcement or complete sandboxing. Correctly CRITICAL only for Tier B/C. | Explicit evidence gap; live offline observation unavailable |
| XD-F011 | KEEP | `rg -n "root LICENSE|legal review|Open" LICENSES/README.md docs/research/dependency-matrix.md` reproduces absent root license and unresolved distribution/model/notices review. | Current release-governance evidence |
| XD-F012 | KEEP | `python3 -B` counterexample using unique `/tmp/xdivina-popper-*` DB: append `event_id=same` from sources `a` and `b`; query returned only `[('same','a')]`. This directly falsifies promised `(source,event_id)` idempotency. Tier C/control-plane only. | Executable deterministic counterexample |
| XD-F013 | KEEP | Same isolated reproducer seeded `planned`, then transitioned `ready→active→review→done` inside one second. Final state was `done`, but event count was `2`, not `4`; rapid valid audit transitions were silently lost. Tier C/control-plane only. | Executable deterministic counterexample |

Additional reproduced checks:

- `node --check` on MVP UI and all Electron shell JavaScript → all exit `0`; syntax does not falsify the findings.
- Exact explicit suite:  
  `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest scripts.test_mvp_gateway scripts.test_gimp_adapter scripts.test_event_store tests.integration.security.test_network_policy tests.integration.psd.test_report tests.integration.comfy_smoke.test_run_smoke -v`  
  → exit `1`, `Ran 109 tests`, six socket-backed errors, therefore **103 passed + 6 unavailable**. The errors are sandbox `PermissionError: [Errno 1] Operation not permitted`, not established product failures.
- `PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -v` → exit `5`, `Ran 0 tests`, `NO TESTS RAN`. The dropped `XDM-EXEC-004` must remain dropped.

Unavailable checks:

- Current live GIMP/gateway/browser behavior, modal keyboard interaction, real save/download/reopen, crash cleanup, packaging/install/uninstall, second platform, same-user process isolation, and outbound-network observation.
- Dependency-absence behavior beyond documented missing GIMP/Chromium/live-service prerequisites.
- Fixture/unit successes are not live-service, usability, packaging, or offline proof.

Feedback edge:

- Yes. Every surviving finding still lacks the current evidence or corrective artifact named by its acceptance check, so the declared feedback edge is required.
- No finding was dropped. `XDM-EXEC-004` remains outside the candidate set and dropped.
- Tier B/C-only CRITICAL scope and Tier C event-store scope are preserved.

blockers: Live services and socket creation unavailable; no authorization for persistent services, browser launch, packaging, or network observation.  
residue: Modal behavior, durable downloaded-artifact survival, clean-machine distribution, offline enforcement, and same-user isolation require later authorized live evidence.  
handoff_note: Wave 4 may retain all `XD-F001`–`XD-F013`; none was falsified. Preserve the exact evidence ceilings and unavailable classifications above.

## Gödel verifier final recheck

`ACCEPT_REVISION`

Digest matches: `d49eff79086a93c817ebf09a3e12fca350a016d61b66c4a9a46dd2a604689714`.

All objections are resolved:

- `XD-F005` and `XD-F006` are absent from the surviving table and action lists; they appear only as explicitly dropped non-findings.
- `XD-F012` cites `scripts/event_store.py:5`.
- `XD-F013` states that one of four rapid transition events survived, producing two total events including the seed, while final state reached `done`.
- Surviving count is 11.
- The optional feedback edge is explicitly recorded as not traversed; future acceptance artifacts remain change-request checks, not missing review evidence.

Final KEEP set: `XD-F001`, `XD-F002`, `XD-F003`, `XD-F004`, `XD-F007`, `XD-F008`, `XD-F009`, `XD-F010`, `XD-F011`, `XD-F012`, `XD-F013`.

Residual objection: none. Verifier role closed.

## Popper verifier final recheck

`ACCEPT_REVISION`

- `findings.md` hash matches `d49eff79086a93c817ebf09a3e12fca350a016d61b66c4a9a46dd2a604689714`.
- `XD-F005` and `XD-F006` are absent from surviving findings, dispositions, and change-request actions; both are explicitly dropped.
- `XD-F012` correctly cites the `(source,event_id)` promise at `scripts/event_store.py:5` and the conflicting implementation.
- `XD-F013` correctly states that one of four rapid transition events survived, producing two total events including the seed.
- Future acceptance artifacts are correctly treated as change-request checks. The optional attacker feedback edge remains untraversed.

Residual objection: none.

Final KEEP set: `XD-F001`, `XD-F002`, `XD-F003`, `XD-F004`, `XD-F007`, `XD-F008`, `XD-F009`, `XD-F010`, `XD-F011`, `XD-F012`, `XD-F013`.

Popper verifier role closed.

