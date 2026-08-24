# research.md — verbatim explorer returns

Dispatch: `2026-08-20-ontology-stable-version-and-runtime-research`
Sheet digest: `cc788e4f3d615543cdc4de954cc0519a83f3f6aeac5e8e520735ca73a2599ddc`

Appended mechanically by the strategist from the three explorer output files.
No synthesis, no editing, no reordering. Synthesizer and reviewer output is NOT
transcribed here — it is digested into findings.md by the writer.

See also `CONTEXT-CORRECTION.md`: the sheet's context asserted a stale premise
which explorer 0 falsified with evidence.

---

## Verbatim return: `explorer-prior-failure.md`

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

---

## Verbatim return: `explorer-working-artifact.md`

# Explorer return — working artifact (what builds and passes today)

Agent: Bénabou, Jean · role explorer · dispatch `2026-08-20-ontology-stable-version-and-runtime-research`

**Claim ceiling.** Cited synthesis only. No ontology authority granted, no runtime
implementation authorized, nothing promoted, no decision gate lifted. Residue
`ontology-authority-not-granted` and `runtime-implementation-not-authorized` stand.
Every result below marked EXECUTED was run by me today; OBSERVED means read, not run.

---

## 1. Executable machinery and exactly what it verifies

### A. `cyberAlchemy-v2/implementation/ontology-candidate-graph-prototype`
EXECUTED `npm test` (= `node --test test/*.test.mjs`, `package.json:10`):
`# tests 59 / # pass 59 / # fail 0 / # skipped 0`.
Per-file (each run separately): candidate-v1 8, determinism 2, edge-grammar 10,
grounding 5, policy-disposition 12, research-lineage 5, run-writer 4,
terminal-receipt 8, write-isolation 5.

What it actually verifies:
- **Carrier shape** (`src/contracts/candidate-v1.mjs:286`): exact-field closure
  (`exactFields`, line 80), 4 node kinds only (`NODE_KINDS`, line 2), SHA-256
  `source_digest` (line 150), repository-relative selector (line 67), duplicate ids
  (line 268), unresolved endpoints (line 231), and `authority_effect === "none"`
  everywhere (`validateAuthorityEffect`, line 109).
- **Edge grammar** (`src/evaluator/edge-grammar.mjs:38`): a 12-entry hardcoded
  `ALLOWED_TRIPLES` Map (line 11), inverse-storage refusal (line 48-56 region,
  `INVERSE_EDGE_DECLARATION`), the session rule (`SESSION_CLAIM_FORBIDDEN`,
  `SESSION_EVIDENCE_FORBIDDEN`), and per-source cardinality.
- **Grounding** (`src/evaluator/grounding.mjs:13`): DFS cycle detection on
  `derives-from` only; root/path closure.
- **Evidence** (`src/evidence/run-writer.mjs:27`): `open(path,"wx",0o600)` refuses
  overwrite (line 9), fsync of file and directory, digest-map binding inputs →
  evaluators → outputs, terminal receipt written last (line 91).
- **Write isolation** (`scripts/verify-write-isolation.mjs:5`): hashes a protected
  selector set (EDGES.yaml, ALLOWED-EDGES.yaml, `cyberAlchemy-v2/authority/**`,
  `arcanum/**`, …) before/after and attests no mutation.

EXECUTED `sha256sum cyberAlchemy-v2/ontology/canonical-kinds/{EDGES,ALLOWED-EDGES}.yaml`
→ `f3ed1ed8…52e0d1` and `500851b1…0224b8`, which match the pinned constants at
`src/evaluator/edge-grammar.mjs:3` and `:5`. They agree **today**.

### B. `arcanum/arcana/ontology-vault/development/schema-validation-plan/tests/`
EXECUTED `python3 tests/validate_branch_schema.py` → `branch-schema-fixtures: PASS`
(exit 0). EXECUTED `python3 tests/validate_branch_json_schema.py` →
`branch-json-schema-fixtures: PASS` (exit 0). Scope: 11 valid + 9 invalid fixtures
under `fixtures/`, checked against `schema/branch-aware-ontology-candidate.schema.yml`
via `jsonschema.Draft202012Validator`. Its own docstring (line 3-4) says it is
"development-only … not a canonical Ontology Vault runtime contract."

### C. `cyberAlchemy-v2/implementation/ontology-evidence-workbench`
Everything I ran builds. EXECUTED, all exit 0:
`./node_modules/.bin/tsc -b --pretty false`; `vitest run` → `Test Files 26 passed (26) /
Tests 35 passed (35)`; `vite build` → `dist/assets/index-GH1VXHVj.js 403.60 kB … built
in 721ms`; `node scripts/validate-standalone-oew.mjs` →
`{"result":"pass","journeys":10,"errors":0}`; `node scripts/audit-active-frontend.mjs`
→ `{"result":"pass","findings":0,"migration":"51/51","historical_unchanged":true}`;
the `test:legacy` command → `# tests 212 / # pass 211 / # skipped 1`. The two
`historical:` suites I probed also pass (`test/upstream-lock.test.mjs` 6/6,
`test/l1-toolchain-bootstrap.test.mjs` 6/6). **Nothing here is broken.**

### D. Production corpus — the one validator over real data
EXECUTED `node projects/body-war/ontology/business/scripts/validate.mjs` →
`{"counts":{"lifecycle_policies":11,"nodes":237,"relations":231,"residue_items":6,
"sources":34},"receipt":"projects/body-war/ontology/business/receipts/
validation-receipt.json","status":"pass"}`. Its 16 diagnostic codes
(`scripts/validate.mjs:6-21`) include `BWO_SOURCE_DIGEST_MISMATCH`, and it really
hashes files on disk (`sha256File`, line 216; call site line 550). EXECUTED
`node --test tests/business-ontology.test.mjs tests/business-views.test.mjs` →
`# tests 15 / # pass 15`.

---

## 2. What none of it verifies

1. **No code parses the governed YAML.** `grep -rn "EDGES.yaml"` over the prototype's
   `src/`, `test/`, `scripts/` returns only digest constants and protected-path
   strings. `ALLOWED_TRIPLES` (12 entries) is a **hand transcription** of
   `ALLOWED-EDGES.yaml:16-48`. I compared them by eye — faithful today.
2. **The digest pin is not checked against the file.** Test 19, "binds the finite
   table to the governed source digests" (`test/edge-grammar.test.mjs:103-110`),
   asserts the constant equals a *literal*. It never reads the YAML. Editing
   EDGES.yaml breaks nothing in the suite. The only file-hashing guard is
   write-isolation, which proves the file *didn't change* — the opposite obligation.
3. **Scope is 4 kinds and 4 predicates.** `ALLOWED-EDGES.yaml:3`: "Every other kind
   is deferred." `specializes` has no law — `policy-disposition.mjs:57` hardcodes
   `policy-indeterminate` / `POLICY_OWNER_UNBOUND`.
4. **The prototype never touches the production corpus.** Its universe is one
   5-node/4-edge carrier plus 8 one-condition mutation descriptors and 1 additive
   descriptor (`fixtures/cases/`).
5. **No cross-package coherence anywhere.** OBSERVED: 76 directories named
   `ontology` (find, excluding node_modules/.git); ~12 are non-staged production
   ones. Their `schema_version` families are disjoint — `body-war-business-node/v1`
   (237) and `body-war-whole-system-relation/v1` (301); `animejs.agent-knowledge-vault.*`;
   `ontology.graph.v0.1` (auth-user-management); `rwo-*` (orchestrator); bare
   semver `1.0.0`/`2.0.0` (augmentor). No tool checks any of them against
   `cyberAlchemy-v2/ontology/canonical-kinds/`.
6. **No query, no update, no identity over time.** Every writer is create-only
   (`open(...,"wx")`); there is no merge, revision, or read-by-predicate path.

---

## 3. Load-bearing vs scaffolding

**Load-bearing** (real, reusable law): `candidate-v1.mjs` (closed-field contract);
`edge-grammar.mjs` (the session rule + inverse refusal are the sharpest rules in the
repo); `grounding.mjs`; `canonical-json.mjs` + `run-writer.mjs` (append-only,
digest-bound evidence); `verify-write-isolation.mjs`; **`body-war/.../validate.mjs`
— the only executable ontology check that runs over a 237-node real corpus and
verifies source digests.**

**Scaffolding**: `policy-disposition.mjs` — `POLICY_DIGEST` (line 1) and `EXPECTED`
(line 4) are both literals in the same file, so "rejects stale policy digest"
verifies a constant against itself; the only genuine branch is `specializes` →
indeterminate. `projection/research-lineage.mjs` and `cli.mjs` are single-fixture:
`evaluatePokerTeamO13` (`cli.mjs:15`) takes no argv and hardcodes one case.
The workbench's `historical:*` scripts, `upstream/` (620K) and `generated/` (55M)
are the README's own "historical evidence only" — dead weight that still passes.

---

## 4. What a runtime would have to add

1. **Read the law instead of transcribing it** — parse ALLOWED-EDGES.yaml, and hash
   it at test time. This is the single largest gap and it is small work.
2. **Ingest the real corpus.** Nothing today evaluates a production ontology
   directory through the candidate grammar.
3. **Kind and predicate coverage** past the 4 Evidence kinds, plus an owner binding
   so `specializes` resolves instead of returning indeterminate forever.
4. **Mutation semantics** — revise, supersede, merge. Every current writer is
   create-once; a runtime needs node identity that survives an edit.
5. **A parameterized read surface.** `projectResearchLineage` is one hardcoded view;
   a runtime needs query-by-request.
6. **Cross-family resolution** across the disjoint `schema_version` vocabularies
   above — or an explicit decision that they stay separate.

---

## Verbatim return: `explorer-governance.md`

# explorer-governance.md — what governance permits and forbids

Agent: Banach, Stefan (explorer, governance lane) · Dispatch: `2026-08-20-ontology-stable-version-and-runtime-research`
Claim ceiling: cited synthesis only. Grants no ontology authority, authorizes no runtime
implementation, promotes nothing, lifts no gate. Residue `ontology-authority-not-granted` and
`runtime-implementation-not-authorized` stand. No design is proposed below.

---

## 1. What "stable" can mean here

**There is no authority kind and no lifecycle status named `stable`.** Three enumerations were
checked exhaustively:

- Authority kinds — nine rows, none `stable` (`cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md:25-35`;
  authoritative table at `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md#authority-kinds`).
- Workflow states — `source-evidence, import-candidate, inventory-candidate, ontology-candidate,
  review-candidate, active, drift-flagged, superseded, deprecated`
  (`cyberAlchemy-v2/ontology/LIFECYCLE-MODEL.md:26-34`). The promoted state is `active`, not stable.
- Node `candidate_status` — `candidate, reviewed-candidate, deferred, blocked, projected`
  (`cyberAlchemy-v2/ontology/NODE-MODEL.md:83-89`).
- Schema `lifecycle_status` enum — `raw, catalogedEvidence, reviewableSignal, promotionRecordDraft,
  candidate, premise, reviewed, promoted, contradicted, retired, rejected, deferred`
  (`arcanum/arcana/ontology-vault/development/schema-validation-plan/schema/branch-aware-ontology-candidate.schema.yml:44-57`,
  key path `$defs.lifecycle_status.enum`). No `stable` member.

The term that **is** defined is `CAV2-D1: Stable Repository`, `Status: active`
(`cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:18-30`): "A stable repository is a
maintainable repository surface whose authority, source evidence, promoted contracts, validation
evidence, implementation work, and operating traces can be understood without hidden conversation
context…". Its operational test is repository-scoped, not version-scoped: "The repository is not
stable merely because files exist; it is stable when its authority model, source spine, promotion
gates, and validation surfaces are navigable and reviewable" (`:34-38`). Boundary: "This term does
not mean finished product, public repository, automatic ownership of every historical CyberAlchemy
source, or implementation complete" (`:56-59`).

Two informal uses exist and neither is a status:

- `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md:155-159` — OQ-1 uses "stable enough": "write a
  deterministic check only after the authority object schema and promotion records are stable
  enough to avoid freezing the wrong shape. **Status: OPEN.**"
- `cyberAlchemy-v2/ontology/promotion-requests/2026-06-23-authority-object-schema-proposal.md:111`
  — "then **decision-gate** to declare the schema stable → OQ-1 clears → build the closure
  validator." That document is `Status: **candidate proposal** (non-executed…)` (`:3`) and states
  "**Non-executed.** This proposal does not amend NODE-MODEL" (`:109`).

**Reading permitted by the corpus:** "stable" is (a) a defined property of a *repository*
(CAV2-D1), and (b) an owner act reserved to **decision-gate** that has never been performed for any
schema or ontology version. It is not a value an artifact may carry, and nothing in the corpus lets
an ontology version self-declare it. Note also
`arcanum/arcana/ontology-vault/development/schema-validation-plan/GOVERNED-CANDIDATE-BUNDLE.md:12`
calls the bundle "one stable reference point" while its own header reads `Status: published
candidate` (`:3`) — prose, not a status claim.

## 2. Gates that must clear first, and their current status

| Gate / question | Selector | Status |
|---|---|---|
| OQ-1 — should authority kinds become validator-backed | `cyberAlchemy-v2/authority/AUTHORITY-MODEL.md:155-159` | **OPEN** |
| OQ-2 — `invariant`/`axiom` as first-class kinds | `AUTHORITY-MODEL.md:161-165` | **OPEN** |
| NODE-MODEL instance layer (the "declare the schema stable" precondition) | `promotion-requests/2026-06-23-authority-object-schema-proposal.md:109-111` | **non-executed candidate**; ontology-route amendment not made |
| OVS-GATE-001 promotion boundary | `arcanum/…/decision-gates/OVS-GATE-001-promotion-boundary.md:3`, `:256-264` | **PASS** (bundle only) |
| OVS-GATE-002 PromotionRecord companion boundary | `…/OVS-GATE-002-promotion-record-companion-boundary.md:3`, `:245-250` | **PASS** (record-kind only) |
| OVS-GATE-003 DomainSpec handoff route | `…/GOVERNED-CANDIDATE-BUNDLE.md:154` | **pending**; no gate file exists (`decision-gates/` holds 001, 002, 004 only) |
| Template promotion gate | `GOVERNED-CANDIDATE-BUNDLE.md:155` | **pending** |
| Label governance gate (`meaning` as branch label) | `GOVERNED-CANDIDATE-BUNDLE.md:156` | **deferred** |
| OVS-GATE-004 default output declaration | `…/OVS-GATE-004-default-output-declaration.md:3`, `:157-165` | **PASS**, narrow: `json-primary-sigil-written-only` (`:100-106`) |

OVS-GATE-004 is explicit that it moved nothing else: "It touches neither gate that is still open"
(`:117-118`), and reaffirms the 001 prohibitions verbatim (`:129-135`).

Unactioned review change-requests that bear on any stability claim
(`cyberAlchemy-v2/ontology/reviews/2026-07-13-authority-vs-canonical-kinds/findings.md:219-240`):

- CR-1 **[CRITICAL]**, still live — route 3 must point at `authority/AUTHORITY-MODEL.md`, not
  `ontology/AUTHORITY-KINDS.md`. Verified unfixed: `CLAUDE.md:67`, `AGENTS.md:176`.
- CR-2 **[CRITICAL]**, still live — no definition card exists for `authority kind` or `canonical
  kind`. Verified: 56 `CAV2-D` cards, no `Term: authority kind` / `Term: canonical kind` line.
- CR-3 **[MAJOR]** — delete `ontology/AUTHORITY-KINDS.md`; file still present, `Status: candidate`
  (`AUTHORITY-KINDS.md:3`).
- CR-4 **[MAJOR]** — `canonical_kind`/`authority_kind` carry no `enum` in the admission schema;
  "CAV2-D49's 'closed, default-deny' exists in exactly one place: review prose" (`findings.md:96`).
- CR-9 **[DISPATCH DEFECT]** — three fabricated quotes propagated through `attacks.md`; that file
  "**must not be cited as independent confirmation**" (`findings.md:238-240`).

`CANONICAL-KINDS.md:6-9` carries its own warning: "**Uncited by construction.** … Do not read an
unattributed claim here as ratified."

## 3. What a runtime may and may not decide

May: emit read models. "Projections are read models… They do not create authority"
(`ontology/projections/README.md:8-10`); allowed kinds and their blocked uses at `:39-45`; emission
rule at `:47-50` — "A projection may emit owner-approved state only when the owner decision permits
the use scope. Blocked, deferred, or unknown candidates may appear only as such." Relation
`emits_projection_when_allowed` is permitted with effect `projection` (`RELATION-MODEL.md:55`).

May not: fill the verdict. "Ontology may represent the rail and projection. It must not fill the
verdict hole" (`LIFECYCLE-MODEL.md:48-49`); "The package models authority. It does not decide
authority" (`PACKAGE-MODEL.md:14`); "Ontology can model authority, but it cannot decide authority"
(`AUTHORITY-MODEL.md:125`). Generated output is posture `posture.generated`, blocked use
"Canonical source" (`AUTHORITY-POSTURES.md:30`). `kind.runtime_contract` is owned by "task-session
after owner gates", forbidden collapse "Not generated mirror output" (`AUTHORITY-KINDS.md:32`).
Identity is local, not global: `concept_id` / `relation_id` are "Local stable identifier"
(`NODE-MODEL.md:18`; `RELATION-MODEL.md:15`).

Ingest rule 5 binds any runtime projection: "Generated runtime projections must point back to
canonical sources before they influence capability contracts" (`SOURCE-MAP.md:32-33`).

## 4. Currently FORBIDDEN (quoted, with selectors)

- `PACKAGE-MODEL.md:46-54` out of scope: "live vault `node_type` creation · vault `## Connections`
  edge creation · schema amendment · movement-edge creation · **runtime contract definition** ·
  generated mirror authority · promotion verdicts · public/private release decisions".
- `RELATION-MODEL.md:62-71` — not allowed as live relations: `witnesses_authority_movement`,
  `promotion_movement_edge`, `ledger_row_as_subgraph`, `promotion_event_as_node`, `movement_as_node`;
  "They require schema governance, edge law, and authority-ledger validation before any executable
  or vault effect."
- `RELATION-MODEL.md:40-43` — value-constraining + cycle-permitted relations are "blocked until
  schema governance records a contextuality-obstruction review and an explicit exception. Unknown
  values are typed residue, not permission." Constitution source: `CAV2-C13`
  (`STABLE-REPOSITORY-CONSTITUTION.md:247-264`).
- `OVS-GATE-001…:240-247` still disallowed: "promoting canonical Ontology Vault templates; requiring
  Inventory to emit ontology fields; mutating structured-action-schema; **treating the JSON Schema
  candidate as final canonical schema**; mutating DomainSpec or CyberAlchemy source packages;
  requiring future systems to adopt the fields."
- `OVS-GATE-004…:129-135` still disallowed: the 001 items unchanged, plus "Importing `meaning` or
  any other label under deferred governance; Requiring any consuming repository to emit, adopt, or
  migrate to these keys; Rewriting records held by owners."
- `GOVERNED-CANDIDATE-BUNDLE.md:87-96` disallowed use, including "treat this bundle as final
  canonical Ontology Vault schema".
- `CAV2-D49` (`DEFINITIONS.md:3247-3261`): an artifact whose kind is not in the closed enumeration
  "may not acquire or exercise authority — it defaults to **blocked** pending an owner decision".
- `CAV2-C2` (`STABLE-REPOSITORY-CONSTITUTION.md:34-51`) non-examples: "Letting an ontology candidate
  redefine a project term. Letting observability signals become design authority without review."
- `promotion-requests/README.md:8-10` — "A request is not a verdict, not a PromotionRecord-compatible
  decision, and not an authority artifact."

## Residue

- No owner route exists for cross-project ontology migration (`OVS-GATE-004…:142-144`).
- Authority-ledger validator missing (`LIFECYCLE-MODEL.md:58-62`).
- Two CRITICAL review change-requests (CR-1, CR-2) remain unactioned as of this read.
