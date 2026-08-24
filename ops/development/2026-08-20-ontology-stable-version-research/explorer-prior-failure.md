# Explorer return — prior-failure corpus (Abramsky, Samson)

Read-only report of what happened; no design proposed. Claim ceiling: cited synthesis only — no ontology authority, no runtime authorization, no promotion, no gate lifted. Residue `ontology-authority-not-granted` and `runtime-implementation-not-authorized` still stand.

## 1. Every distinct reason an attempt stopped

Paths are repo-root-relative. `WOR` = `projects/co-op-engine/research/2026-08-05-whisper-ontology-runtime/`; `OEWL` = `cyberAlchemy-v2/development/ontology-evidence-workbench/research/2026-07-29-runtime-rebuild-lessons/`; `ORA` = `cyberAlchemy-v2/ontology/development/2026-07-30-ontology-runtime-api-research/`; `SWU6` = `cyberAlchemy-v2/development/ontology-evidence-workbench-semantic-navigation/research/2026-08-03-swu006-typed-test-failure-prevention/`.

| # | Stop reason | Exact selector |
|---|---|---|
| R1 | Review loop ceiling exhausted with one lane still failing | `WOR/receipts/evidence-closure.json` keys `/status`=`"block"`, `/loop_ceiling`=2, `/loops_used`=2, `/review_receipts/1/verdict`=`"fail_at_loop_ceiling"` |
| R2 | Deterministic state/reducer contract inconsistent (detail in §2) | `WOR/review-final.md:13-18`; `WOR/receipts/evidence-closure.json:/blocker/code`=`"WOR-RUNTIME-STATE-REDUCER-INCONSISTENT"` |
| R3 | Gate consequence: writer/auditor ineligible, no `findings.md` | `WOR/review-final.md:22-23`; `WOR/receipts/evidence-closure.json:/writer_eligible`=false, `/auditor_eligible`=false |
| R4 | Host thread-limit rejected `spawn-0007` (definition-skeptic); replay policy forbids implicit retry → `gate_block`, dispatch closed `exit_reason: error` | `.arcanum/inventory/entries/cyberalchemy-lab-foundation-research-blocked-result-synthesis.md:88-100` (`#blocking-defect`, `#route-consequence`) |
| R5 | Runtime owners absent (contract, implementation, registration, snapshot, run, retention/GC, service) → design blocked | `ORA/findings.md:41-45`; `ORA/CLOSEOUT.json:/residue/0`; `/claim_ceiling/implementation_readiness`=`"blocked"` |
| R6 | Two reviewer `NEEDS_FEEDBACK` rounds consumed both zig-zag loops before the packet could pass | `ORA/reviews.md:9,84,136`; `ORA/CLOSEOUT.json:/registration/feedback_loops_used`=2 |
| R7 | 48 strict-TypeScript errors in three OEW overlay files (`types.ts` 36, `loadOewBundle.ts` 7, `store.ts` 5) | `OEWL/findings.md:10-12`, `:51` |
| R8 | Required `L1-BUILD.lock.json` absent and unowned | `OEWL/findings.md:49` |
| R9 | Incomplete build order — core not explicitly built after `--ignore-scripts` install | `OEWL/findings.md:50` |
| R10 | Registry/write-set ownership mismatch (trust-rail runner outside the exact inventory) | `OEWL/findings.md:46` |
| R11 | Governance admission churn: ≥56 governance path-writes vs 28 runtime writes (≥2:1), four Task Sessions consumed, none reached a browser | `OEWL/findings.md:47`, `:55-63` |
| R12 | Interrupted preflight left incomplete governed state (`selected_swu=null`, `mutation_authorized=false`) | `OEWL/findings.md:53`, `:152-153` |
| R13 | Declaration mistaken for behavior — registry declares materialize/build/browser commands whose script targets are absent | `OEWL/findings.md:35-37`, `:146-147` |
| R14 | Irreversible diagnostic loss: `commandReceipt()` hashed the streams, `buildThinPrototype()` threw only `TYPED_TESTS_FAILED`, mandatory cleanup removed the workroot | `SWU6/findings.md:9` (§Direct answer, 2nd para); code selectors `build-thin-prototype.mjs:869-910,1673-1708,1888-1894,1945-1947` cited at `SWU6/findings.md:24` |
| R15 | Test/config incompatibility: DOM tests run under generated `vitest.oew.config.mjs` `environment: "node"` → `ReferenceError: document is not defined` | `SWU6/findings.md:7` (§Direct answer, 1st para) |
| R16 | One-attempt authorization consumed; SWU006 stays blocked, SWU007 stopped | `.arcanum/inventory/entries/oewsn-swu006-typed-test-failure-research-strategy-result-synthesis.md:46,100` |
| R17 | No working ontology prototype witnessed: relation grammar authored but its instance grounding law is unenforced | `.arcanum/inventory/entries/ontology-working-prototype-gap-research-result-synthesis.md:81-89`, residue `:52-56` |
| R18 | Adjacent baseline drift: Node suite 46/50 with four `SNAPSHOT_CONTRACT_BINDING_MISMATCH`; IOLM A2/A4 projection stale | same entry `:87`, `:130-131` |

R1–R3 are the only stops that killed a deliverable outright; R5–R6 and R17 are owner/evidence stops inside dispatches that still closed `resolved`.

## 2. What `runtime-state-enum-and-reducer-contract-inconsistent` concretely was

Three enum/reducer defects in the proposed Whisper exact fixture, quoted verbatim from `WOR/review-final.md:15-18`:

> - `pending_gate` was declared as `none | editorial_approval | comprehension`, while the sequence uses `intent_freeze`, `editorial`, `mechanical`, `post-apply`, `refreeze`, and `graph`.
> - `outcome_ceiling` was declared as `pass | flag | block`, while the sequence uses undeclared `absent`.
> - `correction_state` changes from `open` to `resolved` at `EV22 MechanicalAssessmentRecorded` without a correction-resolution event or declared reduction rule.
> - Therefore `RS26`, live/replay digest equality, and the exact command→event→state contract have no single valid state schema or deterministic reducer interpretation.

Both sides of the contradiction are on disk. The declarations: `WOR/synthesis-revision-1.md:48` — "`pending_gate`: `none | editorial_approval | comprehension`." — and `:50` — "`outcome_ceiling`: `pass | flag | block`; not approval or terminality." The use: `WOR/synthesis-revision-2.md:85` reduces `CMD01` to "r1 `intake_recorded`; gate `intent_freeze`; correction `none`; ceiling `absent`", and the unexplained correction transition sits between `:92` ("r11 … gate post-apply; none/flag") and `:98` ("r22 … graph/resolved/flag").

Classification: a location-precision failure, not a conceptual one — vocabulary written in one file, instantiated in another, with nothing forcing agreement.

## 3. The smallest acceptance sequence a prior lesson names

Two are named; one is literally titled that.

**Titled "Smallest acceptance sequence"** — `OEWL/findings.md:86-106`, six steps, marked "This sequence is proposed and has not run" (`:88`): (1) verify pinned archive/overlay/patch/fixture digests, unchanged manifest bytes and counts; (2) fresh temporary workroot, extract, copy overlay, apply entry patch exactly once; (3) frozen install with isolated store, explicit core build, forced focused typed-test discovery, Vite dashboard build — any strict-TS or focused-test failure stops before serving; (4) one owned loopback gateway serving `dist` plus token-protected immutable `/oew-data/*`, fail-closed; (5) pinned Playwright/Chromium/token/port, open `/?oew=1&token=<token>`, assert trust rail, F1 grounding trace, Outline/Table parity, inspector source identity and `authority_effect: none`, receipt commit, no console errors, no outbound requests; (6) in `finally`, prove child termination, port release, temp-root removal. Ceiling at `:108-110`: "one local automated Poker-Team journey", not ontology correctness.

**Smaller in scope, different lane** — the "Minimum Finite Witness" at `.arcanum/inventory/entries/ontology-working-prototype-gap-research-result-synthesis.md:104-121`: a five-node fixture `S1,D1,R1,F1,D2` whose grounding closure must be exactly `F1 -> R1 -> D1` with `D2 contradicts D1` outside it, reproducing `policy-pass`, seven `policy-fail` classes, and `policy-indeterminate` / `POLICY_OWNER_UNBOUND` for `C-SPECIALIZES-D2-D1`.

A third, much larger, is `ORA/findings.md:794-812` §9 — a 12-step local-fixture vertical witness, `[ABSENT, BLOCKED]`.

## 4. Repaired versus still live

**Repaired, with evidence.**
- R1/R2/R3 — closed. Vocabulary reclosed at `WOR/synthesis-revision-3.md:9-11` (`not_assessed` replaces `absent`), the EV22 rule bound at `:39`; executed proof at `WOR/receipts/state-contract-validation.json` (`/status`=`"pass"`, 26 accepted events, 10 negative cases, `live_state_sha256` = `replay_state_sha256` = `44dbb8106b5094f388e63e7a6ad363061d0499af93ac1c4523871fe428e1280c`, `projection_mutated_state: false`); independent review `WOR/review-completion.md`; closure `WOR/receipts/evidence-closure-completion.json:/closed_blocker/status`=`"closed"`, `/research_complete`=true; `WOR/RESULT.md:3`.
- R7/R8/R12 — closed. `cyberAlchemy-v2/development/ontology-evidence-workbench/planning/work-pack/session-evidence/SWU-OEW-007T/attempt-002/validation.json` (recorded 2026-07-30T18:55:38Z): `/adoption_evidence/typed_admission/typescript_diagnostic_count`=0; `/validation/fresh_locked_workroot/dashboard_build_exit_code`=0 with `dashboard_build_expanded_script`=`"tsc -b && vite build"`; lock before/after SHAs and roles bound. Session receipt `SWU-OEW-007T/receipt.json`: `/result`=`"pass"`, `/validation/strict_dashboard_build`=`"pass"`, `/blockers`=`[]`.
- Browser witness — `OEWL/findings.md:148` says "No Playwright OEW journey or browser receipt exists", but that dispatch closed at 2026-07-29T05:05:00.187Z (`telemetry/agents/subagents-dispatch.yaml:4397-4400`), and `cyberAlchemy-v2/implementation/ontology-evidence-workbench/generated/runs/SWU-OEWTP-004/20260729T185728Z/browser-acceptance.json` (`/result`=`"pass"`, assertions A01–A06 pass, `/authority_effect`=`"none"`) was written ~14 h later in the thin-prototype lane. The lesson is stale on that one row only.
- R4 — closed by a separate confirmed recovery dispatch `2026-08-08-cyberalchemy-lab-foundation-recovery`; audited `findings.md` at SHA-256 `07a29e2fc62f92b6eb2d28c197b19c2ccc036a9952b75474f52c5ac9a44de11d` (`.arcanum/inventory/entries/cyberalchemy-lab-foundation-research-recovery-result-synthesis.md`, `#direct-result`), which supersedes only the blocked execution state.
- R14/R15 — *diagnosed*, not fixed. `SWU6/closeout-receipt.json`: `/exit_reason`=`"resolved"`, `/auditor_verdict`=`"approve"`. The defect itself is open: `SWU6/findings.md:91` heading "Mandatory later no-network fixture suite — not yet implemented"; ceiling "implementation and retry remain unauthorized".

**Still live.**
- R5/R6 residue verbatim at `ORA/CLOSEOUT.json:/residue`: runtime-contract/implementation/registration/snapshot/run/retention/service owners absent; CAV2 profile and all adapters absent; no implementation, measurement, or local-fixture witness; Augmentor stale-receipt replay/isolation open; Orchestrate coordinator action-ID replay gap.
- R16 — SWU006 blocked and selected, SWU007 stopped.
- R17/R18 — residue `ontology-instance-validator-absent`, `named-relation-policy-evaluator-absent`, `tested-write-isolation-absent`, `iolm-a2-binding-drift`, `current-browser-and-human-evidence-absent` (entry `:51-58`). Whether the four `SNAPSHOT_CONTRACT_BINDING_MISMATCH` failures still reproduce is **unverified by me** — I executed nothing; that belongs to the working-artifact lane.
- R13 and the OEW gaps at `OEWL/findings.md:141-151` other than the ones listed above: `/oew-data/*` routing, absent materialize/build/browser targets, unexecuted like-for-like simplification measurement — I found no repair receipt.
- Whisper's unproved list stands: `WOR/RESULT.md:32` (ontology file/admission, durable journal, SQLite/CAS, activity execution, crash/retry, identity/privacy, graph validation, product integration, promotion, release).

**Record drift worth flagging.** The Inventory read model still carries the *blocked* whisper state: `.arcanum/inventory/entries/whisper-ontology-runtime-research-blocked-result-synthesis.md:6-7` is `updated: 2026-08-05`, `status: blocked`, with `runtime-state-enum-and-reducer-contract-inconsistent` at `:44`. No completion entry exists (`ls .arcanum/inventory/entries/ | grep -i whisper` returns only the blocked and strategy entries). The working folder proves the repair; the index does not know it. This dispatch's own context inherited the stale reading.
