---
title: v0.1 Beta launch posture — one-pager scope-pin
filed: 2026-05-10
operator: Josh
audience: operator + Golden Quill/FIT Farms white-glove team + future Beta customers
authority: consolidates the v0.1 Beta deployment scope across README + CLAUDE.md + ARCHITECTURE_OVERVIEW.md + `pipeline/planning/v0_1_beta_readiness_2026-05-10.md`
purpose: single-document scope-pin describing what v0.1 Beta ships, what it does not, and what unblocks each remaining gate
disposition: superseded by `pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md` for current v0.1 clearance; retained as historical launch-posture snapshot
git_remote: https://github.com/HyphaeNated/GoldenQuill.git
initial_commit: d3bc8b100b30e75f37afcf59483d565ec6ac69e2 (2026-05-15 16:58 EDT — "Initial commit: Golden Quill workspace bootstrap")
---

# v0.1 Beta Launch Posture — what Tilth ships and what it does not

## What v0.1 Beta is

Tilth v0.1 Beta is a sovereign grant-intelligence appliance shipped on a Golden Quill (128 GB hardware floor: Apple M3 Ultra Mac Studio · AMD GX-10 · NVIDIA Spark). One Tilth per client, owned by the client, runs on hardware the client owns. The software intelligence is **Tilth** — a six-seat AI council (Scout / Scribe / Editor / Judge / Red Team / Logician) plus two v0.1 support agents (Intake + Uploader). BYOK only: the client owns every API key.

## What v0.1 Beta ships

### Core pipeline (active)

- **Six-seat council** routing per architecture v7.0.7 classification-driven pattern: cloud frontier for Public + Shareable input; local-routable 70B/200B-class for Confidential / Operator-flagged input; opaque-slot discipline at the cloud boundary.
- **Submission_mode track** — Scout DISCOVER (seven parallel channel families) → Scout VERIFY (live synopsis) → Scout REVIEW (operator gate) → Scribe section-by-section drafting with KGIE preflight → Editor clarity review → Judge funder-rubric scoring → Red Team adversarial challenge → operator approval → Uploader prepare-and-stage → operator clicks final submit on funder portal.
- **Eval_mode track** — Judge + Red Team scoring on operator-supplied drafts; same cross-family rigor as submission_mode.
- **Operator gears per seat**: Sparring Partner / Co-Pilot (default) / Synthesizer.

### Operational substrate

- **Key Facts Register (KFR)** per architecture v7.0.4 + v7.0.4-M1 — per-org quantitative substrate with SP0 freshness review, derivation-chain integrity, currency tolerance gates, NEEDED hard-block, AWARD_INGEST signature verification.
- **Funder Intelligence Database + Match Database** per architecture v7.0.5 — workspace-shared funder corpus + per-org reasoning trail; Scout channel G adds local funder-intel corpus reads with sanitization + classification-filter gates.
- **Classification register** per architecture v7.0.7 — operator-curated four-class set (Public / Shareable / Confidential / Operator-flagged); Ed25519-signed at white-glove + per-grant SP0 chain; new-fact-default-Confidential per F-CLASS-NEW-FACT-UNCLASSIFIED PRE-gate.
- **Operational data sub-kinds** per §2 v7.2 — metrics / financials / photos / narrative_entries / timeline / beneficiary_records / attachments; SIMPLE write-if-absent; canonical-JSON round-trip; PII discipline on beneficiary_records.

### Support agents

- **Intake (v0.1, always-local)** — three-mode dispatch: BULK_INGEST (white-glove onboarding bulk doc absorption with verbatim-quote-with-page provenance) + INCREMENTAL_INGEST (between-cycle fact additions; new facts default to `confidential`) + AWARD_INGEST (proposal_commitments.yaml extraction at award acceptance).
- **Uploader (v0.1, always-local)** — submission package assembly per §12 v1; four portal adapters (Grants.gov Workspace · SAM.gov · Common Grant Application · copy-paste fallback); three-layer auto-submit defense (AST-lint allow-list + network-namespace isolation + `@typing.final` invariant); prepare-and-stage discipline only.

### Logician deterministic gates

- ~50 failure codes across F-LOGICIAN-* (Five Laws PRE/POST), F-CLASS-* (12 classification primitives per v7.0.7), F-CIC-CLC-COUPLING-VIOLATION (orthogonality enforcement per v7.0.8), F-INTAKE-* (11 codes), F-UPLOADER-* (10 codes), F-ARCHIVIST-* (5 codes proposes-only enforcement), F-DATACOLLECTOR-* (8 codes — v0.2 active but v0.1 dormant), F-REPORT-* (5 codes — v0.2 SPEC-locked), F-FACT-DRIFT-* (9 codes), F-MATCH-DB-* + F-CHANNEL-G-* + F-FUNDER-CORPUS-* (7 codes from v7.0.5).
- Three-layer defense pattern applied wherever an auto-apply boundary exists (Uploader auto-submit · Archivist canonical-mutate · DataCollector autosend · Reflection attach when v1.x lands).
- Cedar policy evaluator: deterministic Python authoritative at v0.1; M15-seal at v1.x.

### Classification Review wrapper (white-glove gate)

Per architecture v7.0.7 + the wrapper landed at the Classification Review operator UX wrapper LOCK earlier today (`pipeline/orchestrator/classification_review.py` + CLI at `pipeline/cli/tilth_review_classify.py`):

1. Inventory of every per-org document → operator review queue.
2. Per-class operator override pass.
3. Routing simulation — what a representative grant cycle would route cloud vs local.
4. Test cycle — first-pass dispatch on a synthetic RFA + classification-bound prompts.
5. Operator Ed25519 sign-off on the classification register at `orgs/<slug>/vault/classification/register.yaml`.

Without a completed Classification Review stage + operator Ed25519 signature, the F-CLASS register and routing gates refuse to run a grant cycle. Structural sovereignty, not policy. F-CLASS-COVERAGE-INCOMPLETE separately prevents deployment if any required F-CLASS-* enforcement module or test is missing.

## v0.1 Beta deployment fail-closed gates

Any one of these refuses to run a grant cycle:

| Gate | Fail-closed at | Trigger |
|---|---|---|
| `F-CLASS-COVERAGE-INCOMPLETE` | PRE-cycle META | required F-CLASS-* enforcement modules and tests are incomplete or missing from the runtime tree |
| `F-CLASS-REGISTER-UNSIGNED` | PRE-cycle | register exists but operator Ed25519 signature missing |
| `F-CLASS-REGISTER-SIGNATURE-INVALID` | PRE-cycle | signature verification fails against pinned operator public key |
| `F-CLASS-ROUTING-INDETERMINATE` | PRE-call | per-call routing decision cannot determine cloud-vs-local |
| `F-CLASS-NEW-FACT-UNCLASSIFIED` | PRE-write | new fact ingested via Intake INCREMENTAL has no classification |
| `F-CLASS-SLOT-ID-NON-OPAQUE` | PRE-prompt | cloud-routed prompt contains a semantic slot name |
| `F-CLASS-HIGH-STAKES-FLAG-LEAK` | POST-call | heavy-Judge swap flag leaked into a cloud payload |
| `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` | PRE-load | router-template update signature does not verify against the white-glove-pinned publisher public key |

## What v0.1 Beta does NOT ship (v0.2 / v1.x horizon)

- **Data Collector** (v0.2) — grantee outreach via email + SMS + voice + Telegram + WhatsApp; spec LOCKED today but channel substrate wiring is v0.2 Code phase work.
- **Report Generator** (v0.2) — funder-ready reports via `report_mode` track; spec LOCKED today but `report_mode` track currently refuses at runtime via F-PIPE-TRACK-NOT-SHIPPABLE until v0.2.
- **Archivist runtime** (v1.x) — long-running curation, lessons memory, audit trail; spec LOCKED today as proposes-only; runtime activation at v1.x per §15 J-06 slot transition.
- **Reflection sub-mode** (v1.x runtime; v0.1 Beta hook ships dormant primitives only when WS-Reflection LOCKs).
- **Watts per Funding Action (WPFA)** (v0.1 Beta scope per 2026-05-10 operator directive; Thesis dispatch pending) — per-cycle dollars + watt-hours actually consumed + counterfactual + delta; signed by operator for buyer-facing PDF; sales lever for the regenerative-buyer thesis.
- **Funding Goal** (v0.2 first wave per spec card default; pending operator OQ-1) — per-org persistent funding intent across grant cycles; Scout DISCOVER goal-aware ranking; Match DB goal-aware composite score.
- **Reflection Packet** (v0.2 horizon per default; pending operator scope decision) — typed Pydantic BaseModel emitted at cycle close; sibling-not-nested with WPFA; feeds Archivist learning loop.
- **State-rules card** (v0.2) — PA / CA / FL / TX / NY first wave for Data Collector compliance.
- **BYOK envelope** for Twilio / Postmark/SendGrid / MTProto / WhatsApp Business API (v0.2).
- **Stage-2+** multi-Tilth fleet aggregation, Stage-5 Sovereign Node commons consent-tier on-ramp (out of scope for v0.1 + v0.2).

## Five Operating Laws (canonical reference)

Non-negotiable. No prompt, skill, or model can override.

1. **RFA Is the Source of Truth** — every claim traces to the RFA or PROJECT_CONTEXT.
2. **No Boundary Drift** — stay inside the RFA's defined scope.
3. **Org Isolation** — one PROJECT_CONTEXT per session; never cross-reference orgs.
4. **Apolitical Language + Admin-Risk Term Scanning** — funder dialect code-switching; live flagged-terms register; operator approves every substitution.
5. **Applicant Brings the Substance** — shape existing credentials/data/partnerships into funder-ready form; never fabricate.

## Sovereignty Promise

- Hardware: operator-owned (128 GB floor).
- Data: stays local; opt-in cross-Tilth signals require operator consent at Stage-5 onward.
- API keys: BYOK only; operator owns every key.
- Updates: router-template releases ship signed; operator opts in per release; deployment stays on prior pinned version on signature-verify-fail.
- If FIT Farms LLC disappeared tomorrow: operator still owns their machine, data, keys, and grants.

## What unblocks Beta first-customer cut

Per `pipeline/planning/v0_1_beta_readiness_2026-05-10.md` post-WS-L state:

| Item | Status | Estimate |
|---|---|---|
| Intake full-impl code phase (three modes beyond skeleton) | CLEARED IN CURRENT TREE; keep in smoke tests | — |
| Uploader full-impl code phase (real adapter wiring beyond skeleton) | CLEARED IN CURRENT TREE; keep in smoke tests | — |
| Classification Review operator UX wrapper | **LANDED 2026-05-10** | — |
| README + CLAUDE.md + ARCHITECTURE_OVERVIEW v0.1 Beta launch posture section | **THIS DOCUMENT + co-edits** | — |
| White-glove playbook subset for Classification Review + AWARD_INGEST | LANDED at `docs/white_glove_v0_1_beta.md` | — |
| First dogfood Beta deployment dry-run + integration probe | RED | 1-2 sessions |

Estimated remaining sessions to v0.1 Beta cut: ~3-5 sessions of Code-phase + integration work + operator dry-run.

## What is NOT a v0.1 Beta blocker

- §13 Data Collector channel substrates (v0.2)
- §14 Report Generator track-mode (v0.2)
- §15 Archivist runtime implementation (v1.x)
- WS-N integration scenarios 3-6 (v0.2 work)
- State-rules card first wave (v0.2)
- BYOK envelope for Twilio / Postmark / MTProto / WhatsApp Business API (v0.2)
- WS-Reflection v0.1 Beta hook (parallel; LOW cost; dormant primitives only)
- WS-WPFA (parallel; operator-LOCKED at v0.1 Beta scope but parallel work-stream to Beta close-out)

## Operator decision surface remaining

| Decision | Question | Default if under-specified |
|---|---|---|
| Funding Goal ship window | v0.1 / v0.2 first wave / v0.2 second wave | v0.2 first wave |
| Reflection Packet scope | v0.1 Beta sibling-with-WPFA / v0.2 horizon sibling-with-§15 | TBD — Q2 in spec-card-status report |
| Reflection Packet code-family | F-PACKET-* separate / fold into F-REFLECTION-* | F-PACKET-* separate (Path B from naming reconciliation) |
| First Beta deployment client identification | per Josh, Law 3 boundary | — |
| Heavy-Judge swap analog for Reflection | v1.x ship or defer indefinitely | ship at v1.x |
| Reflection cadence | third top-level cadence / sub-mode of quarterly | third cadence |
| Inoculation-frame template wording | operator-voice required | — |

---

**Filed:** 2026-05-10. Living document. Supersedes prior internal-audit one-pager candidates.
