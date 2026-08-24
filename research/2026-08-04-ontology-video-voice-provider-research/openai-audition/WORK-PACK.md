---
module: openai-stock-voice-audition
version: current
status: draft
updatedAt: 2026-08-04
docType: work-pack
---

# WORK-PACK: OpenAI Stock-Voice Audition

## Control fields

| Field | Value | Notes |
|---|---|---|
| workPackGateStatus | pass | Structural Plan gate passes for the active L0 offline slice only. Provider rendering remains blocked. |
| complexity | medium | Four tasks, eight SWUs, five ordered waves, external effect and human decision. |
| outputMode | split | Task and wave contracts are separate. |
| executionPackRef | [EXECUTION-PACK.md](EXECUTION-PACK.md) | Required choreography. |
| layeringArtifactRef | [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md) | Layer governance source. |
| dispatchTechniqueTrace | [DISPATCH-TECHNIQUE-TRACE.md](DISPATCH-TECHNIQUE-TRACE.md) | Define/Design/Plan technique trace. |
| distillValidationStatus | pass | Standard two-round local role simulation; see `PLAN-DISTILL-VALIDATION.md`. |
| swuAtomicityStatus | pass | Each SWU has one independently reviewable behavior. |
| firstUnitNarrownessStatus | pass | `SWU-OAIA-001` is the narrowest reversible trust step. |
| closeoutSyncStatus | pass | Every mutation-capable SWU has an exact closeout row below. |
| activeLayerWindow | L0 | No provider call. |
| selectedSWU | none | Invoke does not select or execute implementation. |
| auditionAdmission | not_ready | Hard owner/account/tool gates remain open. |
| lastUpdatedAt | 2026-08-04T00:00:00Z | Date-stable planning timestamp. |
| readinessProfile | pilot | Local evidence pilot, not release or production. |

## Objective summary

- Objective: deliver a local, reproducible path from one exact admitted OpenAI stock-voice configuration to immutable render, fidelity, blind-listening, and operator-decision evidence.
- Primary inputs: approved Define and Design artifacts, frozen excerpt, official OpenAI contract snapshot, and prior audition protocol.
- Current success condition: the Plan is navigable and L0 can be selected later without reopening discovery; no mutation is selected now.
- Full work-pack success condition: one terminal audition decision exists with all governing hashes and no claim beyond audition evidence.

## Delivery slices

| Slice | Outcome | Layer | Wave | Dependencies | Validation |
|---|---|---|---|---|---|
| S-BASE | Baseline sources, gates, and runtime assumptions frozen | L0 | [W0](work-pack/waves/W0.md) | Design pass | Digest and environment review |
| S-PREFLIGHT | Offline manifest/admission boundary proves fail-closed | L0 | [W1](work-pack/waves/W1.md) | S-BASE | Node tests; transport-spy zero calls |
| S-RENDER | Two immutable raw attempts for one admitted configuration | L1 | [W2](work-pack/waves/W2.md) | S-PREFLIGHT + B-001–B-005 resolved | Explicit live receipt review |
| S-VERIFY | Technical/fidelity and blind-listening evidence | L2 | [W3](work-pack/waves/W3.md) | S-RENDER + B-006/B-007 resolved | Tool receipts, manual review, locked sheets |
| S-DECIDE | Named operator records bounded outcome | L3 | [W4](work-pack/waves/W4.md) | S-VERIFY | Decision schema and hash closure |

## Task status board

| Task | Goal | Layer | Waves | Gate | Status |
|---|---|---|---|---|---|
| [TASK-OAIA-PREFLIGHT](work-pack/tasks/TASK-OAIA-PREFLIGHT.md) | Implement offline source lock and admission evaluator | L0 | W1 | ready-for-selection | not-started |
| [TASK-OAIA-RENDER](work-pack/tasks/TASK-OAIA-RENDER.md) | Capture two exact raw provider attempts safely | L1 | W2 | blocked by B-001–B-005 | not-started |
| [TASK-OAIA-VERIFY](work-pack/tasks/TASK-OAIA-VERIFY.md) | Establish technical and spoken-fidelity evidence | L2 | W3 | blocked by render + B-006 | not-started |
| [TASK-OAIA-DECIDE](work-pack/tasks/TASK-OAIA-DECIDE.md) | Blind, score, and record operator outcome | L2–L3 | W3–W4 | blocked by verification + B-007 | not-started |

## SWU execution handoff

| SWU | Parent | Dependencies | Write scope | Done criteria | Validation | Owner | Handoff |
|---|---|---|---|---|---|---|---|
| SWU-OAIA-001 | [PREFLIGHT](work-pack/tasks/TASK-OAIA-PREFLIGHT.md) | none | `runtime/schemas/*`, `runtime/lib/canonical-json.mjs`, `runtime/lib/validate-manifest.mjs`, `runtime/test/manifest.test.mjs`, `.gitignore` | Exact excerpt/source/schema validation passes causal positive/negative fixtures | `node --test runtime/test/manifest.test.mjs` | local-fallback | ready, unselected |
| SWU-OAIA-002 | [PREFLIGHT](work-pack/tasks/TASK-OAIA-PREFLIGHT.md) | 001 | `runtime/lib/evaluate-admission.mjs`, `runtime/lib/request-preview.mjs`, `runtime/bin/audition.mjs`, `runtime/test/admission.test.mjs` | Deterministic admission and redacted request preview; zero network on block | `node --test runtime/test/admission.test.mjs` | local-fallback | dependency-ready after 001 |
| SWU-OAIA-003 | [RENDER](work-pack/tasks/TASK-OAIA-RENDER.md) | 002 + B-001–B-005 | `runtime/lib/openai-speech-transport.mjs`, `runtime/test/render.test.mjs` | One explicit request produces safe bounded transport result; secrets absent | `node --test runtime/test/render.test.mjs` plus explicit authorized live check | manual | blocked |
| SWU-OAIA-004 | [RENDER](work-pack/tasks/TASK-OAIA-RENDER.md) | 003 | `runtime/lib/attempt-store.mjs`, `runtime/test/attempt-store.test.mjs` | Two unique immutable attempts share admitted request digest and cannot overwrite | `node --test runtime/test/attempt-store.test.mjs` | local-fallback | blocked |
| SWU-OAIA-005 | [VERIFY](work-pack/tasks/TASK-OAIA-VERIFY.md) | 004 + B-006 | `runtime/lib/verify-audio.mjs`, `runtime/test/verify-audio.test.mjs` | Raw and derivative audio metadata/metrics bind to parent hashes | `node --test runtime/test/verify-audio.test.mjs` plus pinned tool commands | manual | blocked |
| SWU-OAIA-006 | [VERIFY](work-pack/tasks/TASK-OAIA-VERIFY.md) | 005 | `runtime/lib/verify-fidelity.mjs`, `runtime/test/fidelity.test.mjs` | Independent word and key-phrase review yields pass or rejection with no unresolved token | `node --test runtime/test/fidelity.test.mjs` plus manual review | manual | blocked |
| SWU-OAIA-007 | [DECIDE](work-pack/tasks/TASK-OAIA-DECIDE.md) | 006 + B-007 | `runtime/lib/blind-listening.mjs`, `runtime/test/blind.test.mjs` | Opaque assets, balanced orders, locked valid score sheets, protected key | `node --test runtime/test/blind.test.mjs` plus three-listener receipt review | manual | blocked |
| SWU-OAIA-008 | [DECIDE](work-pack/tasks/TASK-OAIA-DECIDE.md) | 007 | `runtime/lib/decision.mjs`, `runtime/test/decision.test.mjs`, `runtime/README.md` | Named operator records one legal outcome; disclosure and next-route boundary explicit | `node --test runtime/test/decision.test.mjs` plus owner signature/hash review | manual | blocked |

## SWU atomicity review

| SWU | Primary behavior | Candidate split considered | Retained-boundary rationale | Verdict |
|---|---|---|---|---|
| 001 | Validate exact candidate inputs | Schema vs digest code | Neither is independently useful; the accepted boundary is “source-valid manifest.” | pass |
| 002 | Decide admission and project safe preview | Gate evaluator vs projection | Preview is the observable witness of one admission decision and is emitted only on pass. | pass |
| 003 | Perform one bounded provider request | Auth vs transport vs response | Separating auth would create a secret-handling unit with no behavior; transport owns the external effect. | pass |
| 004 | Bind two immutable repetitions | File store vs repetition join | The task's behavior is repeatability; each attempt helper remains internal. | pass |
| 005 | Establish technical audio validity | Inspect vs normalize | Derivative provenance and format metrics jointly answer technical usability. | pass |
| 006 | Establish exact spoken fidelity | Align vs independent audit | Neither can pass alone under the protocol; independence is an internal invariant. | pass |
| 007 | Produce unbiased listening evidence | Randomize vs score | The blind evidence boundary requires both before unblinding. | pass |
| 008 | Record terminal audition outcome | Decision vs docs | Documentation is evidence of the same bounded decision/handoff. | pass |

## Blockers

| ID | Scope | Description | Owner | Resolution |
|---|---|---|---|---|
| B-001 | W2+ | Common accent/locale or provider-native variation is unset. | audition owner | Record one explicit choice in the immutable manifest. |
| B-002 | W2+ | Exact stock voice is unset. `marin` and `cedar` are recommendations, not a selection. | audition owner | Listen to official demos and select one exact voice ID. |
| B-003 | W2+ | Named production operator is unset. | video owner | Name the person responsible for `approve|reject|defer`. |
| B-004 | W2+ | Actual-account public-use, agreement, data-use, retention/deletion, security, and disclosure decisions are open. | account/legal/data owners | Bind dated owner receipts for the exact account and use. |
| B-005 | W2+ | Exact model availability, voice availability, account tier/region, route token count, and request preview are not live-verified. | provider interface owner | Refresh docs, run offline count/preflight, and freeze admitted manifest without calling the API. |
| B-006 | W3+ | No pinned audio normalization, alignment, independent-fidelity, or VTT tools exist; `ffmpeg`, `ffprobe`, and Whisper CLI were not discovered locally. | verification owner | Select/install through separately authorized route; freeze versions, paths, hashes, commands, tolerances. |
| B-007 | W3+ | Three listeners, common playback setup, randomization tool, and unblinding-key custodian are unset. | production operator | Record the listening operations manifest before blinding. |

## Task Session closeout sync contract

Common rule: each baseline is captured by Task Session immediately before mutation as an exact path digest or explicit `absent`; allowed deltas are only the declared targets. Every terminal receipt conforms to `.agents/skills/task-session/schemas/governance-terminal-receipt.schema.json`. Closeout cannot select or begin the successor.

| SWU | Lifecycle owner route | Terminal source receipt contract | Declared target inventory | Baseline binding | Allowed delta classes | Owner validation | Expected owner receipt | Successor policy |
|---|---|---|---|---|---|---|---|---|
| 001 | `invoke:refresh:apply-approved` | Task Session governance terminal receipt | `.gitignore`; `runtime/schemas/audition-manifest.schema.json`; `runtime/lib/canonical-json.mjs`; `runtime/lib/validate-manifest.mjs`; `runtime/test/manifest.test.mjs` | Pre-execution SHA-256 or `absent` for every target | `files_added`, `tests_added`, `blocker_opened` | `node --test runtime/test/manifest.test.mjs`; JSON parse; secret and scoped whitespace scans | `work-pack/closeouts/SWU-OAIA-001.json` | 002 is the unique dependency-ready successor; explicit selection still required |
| 002 | `invoke:refresh:apply-approved` | Task Session governance terminal receipt | `runtime/lib/evaluate-admission.mjs`; `runtime/lib/request-preview.mjs`; `runtime/bin/audition.mjs`; `runtime/test/admission.test.mjs` | Pre-execution SHA-256 or `absent` for every target | `files_added`, `tests_added`, `blocker_opened` | `node --test runtime/test/admission.test.mjs`; zero-transport assertion; secret scan | `work-pack/closeouts/SWU-OAIA-002.json` | 003 only after B-001–B-005 close and explicit selection |
| 003 | `invoke:refresh:apply-approved` | Task Session governance terminal receipt plus explicit live-effect receipt | `runtime/lib/openai-speech-transport.mjs`; `runtime/test/render.test.mjs`; one exact UUID run receipt path declared at Task Session preflight | Pre-execution SHA-256 or `absent`; run path must be `absent` | `files_added`, `tests_added`, `evidence_added`, `blocker_opened` | `node --test runtime/test/render.test.mjs`; authorized live receipt; outbound/secret review | `work-pack/closeouts/SWU-OAIA-003.json` | 004 is unique; explicit selection required |
| 004 | `invoke:refresh:apply-approved` | Task Session governance terminal receipt | `runtime/lib/attempt-store.mjs`; `runtime/test/attempt-store.test.mjs`; two exact UUID attempt paths declared at Task Session preflight | Pre-execution SHA-256 or `absent`; both attempt paths must be `absent` | `files_added`, `tests_added`, `evidence_added`, `blocker_opened` | `node --test runtime/test/attempt-store.test.mjs`; raw hash and request-digest review | `work-pack/closeouts/SWU-OAIA-004.json` | 005 only after B-006 closes and explicit selection |
| 005 | `invoke:refresh:apply-approved` | Task Session governance terminal receipt | `runtime/lib/verify-audio.mjs`; `runtime/test/verify-audio.test.mjs`; exact technical receipt and derivative paths declared at preflight | Pre-execution SHA-256 or `absent`; generated paths must be `absent` | `files_added`, `tests_added`, `evidence_added`, `blocker_opened` | `node --test runtime/test/verify-audio.test.mjs`; pinned-tool logs/metrics and lineage review | `work-pack/closeouts/SWU-OAIA-005.json` | 006 is unique; explicit selection required |
| 006 | `invoke:refresh:apply-approved` | Task Session governance terminal receipt | `runtime/lib/verify-fidelity.mjs`; `runtime/test/fidelity.test.mjs`; exact alignment, independent-audit, comparison, and manual-review paths declared at preflight | Pre-execution SHA-256 or `absent`; generated paths must be `absent` | `files_added`, `tests_added`, `evidence_added`, `blocker_opened` | `node --test runtime/test/fidelity.test.mjs`; exact mismatch and key-phrase review | `work-pack/closeouts/SWU-OAIA-006.json` | 007 only after B-007 closes and explicit selection |
| 007 | `invoke:refresh:apply-approved` | Task Session governance terminal receipt | `runtime/lib/blind-listening.mjs`; `runtime/test/blind.test.mjs`; exact opaque assets, order, sheets, and key-locator paths declared at preflight | Pre-execution SHA-256 or `absent`; generated paths must be `absent` | `files_added`, `tests_added`, `evidence_added`, `blocker_opened` | `node --test runtime/test/blind.test.mjs`; listener, order, score, and key audit | `work-pack/closeouts/SWU-OAIA-007.json` | 008 is unique; explicit selection required |
| 008 | `invoke:refresh:apply-approved` | Task Session governance terminal receipt | `runtime/lib/decision.mjs`; `runtime/test/decision.test.mjs`; `runtime/README.md`; exact decision receipt path declared at preflight | Pre-execution SHA-256 or `absent`; decision path must be `absent` | `files_added`, `tests_added`, `evidence_added`, `route_changed` | `node --test runtime/test/decision.test.mjs`; named-owner, hash, disclosure, and claim review | `work-pack/closeouts/SWU-OAIA-008.json` | none; later production route requires a new Invoke |

## Validation strategy

See [VALIDATION-STRATEGY.md](VALIDATION-STRATEGY.md). Every executable check is local by default. A live provider request is isolated to SWU-003, manually owned, separately authorized, and never inferred from passing tests.

## Gate checks

- Plan structure, navigation, SWU atomicity, closeout rows, and Distill validation: pass.
- L0 offline work: ready for a future explicit SWU selection.
- Current selection: none; mutation is not admitted by this Invoke run.
- L1 provider rendering: blocked by B-001 through B-005.
- L2 verification/listening: blocked by B-006 and B-007 plus upstream evidence.
- L3 production handoff: conditional and non-releasing.
