# BUILD-SPEC — White-Glove Delivery and Node Care

- **Node:** `white-glove-delivery-node-care`
- **Craft ledger:** `docs/strategy/development/white-glove-delivery-node-care/.craft/ledger.yml` (`craft.goldenquill.white_glove_delivery_node_care`)
- **Owns:** Workbook Workstream F (White-Glove Delivery, every customer) + the Node Care handoff into Workstream G operations.
- **Authoring mode:** Refine→Invoke (Define→Design→Plan). **Planning/spec only — no runtime, no execution.**
- **Status:** GAP-WGD-PLAYBOOK authored (block→ready); GAP-WGD-DAY60 authored with marked dependency; GAP-WGD-CS-HANDOFF authored with marked gating.
- **Filed:** 2026-06-13.

## 0. Frame and boundary

This node turns the first founder-led installs into a **repeatable service**. The *technical* onboarding spine is already locked in `docs/white_glove_v0_1_beta.md` (BULK_INGEST → Classification Review + posture selection → first grant cycle → AWARD_INGEST → INCREMENTAL_INGEST, with the F-CLASS fail-closed gate set). This BUILD-SPEC authors the **human-facing service wrapper delta over that spine** — the artifacts the workbook names but the v0.1 playbook does not flesh out — plus the Day-60 review structure and the CS/Field-Tech transition checklist.

**Guardrails carried into every artifact below:**

- **v0.1 is headless.** No UI deliverables. Every operator-facing surface is a document, a CLI invocation, or a side-by-side white-glove session. Do not author a console screen.
- **Classification Review is mandatory before Beta.** No artifact may describe a deployment reaching its first grant cycle without a completed Classification Review and operator Ed25519 sign-off (`white_glove_v0_1_beta.md` §2; CLAUDE.md v7.0.7/v7.0.10). The F-CLASS register/routing gates fail-close unsigned.
- **Law 3 (Org Isolation).** No artifact reads, references, or templates against any client `orgs/` PROJECT_CONTEXT. All artifacts in this node are org-agnostic templates that a delivery operator fills *per node* without cross-referencing other clients.
- **Sovereignty Promise is the acceptance bar.** Every wrapper artifact must demonstrate the promise concretely at the test cycle (operator owns hardware/keys/data; cloud routing only by selected posture + per-field class; nothing held hostage).
- **Owner boundaries (do not author here):** Golden Image / imaging mechanics (`hardware-golden-image`); the posture/classification *engine* (`quality-security-proof` + locked architecture); CS/Field-Tech *hiring trigger threshold* and budget (`staffing-budget-and-triggers`); Day-60 *metric definitions/instrumentation* (`quality-security-proof` Workstream C); contracting/LOI (`sales-contracting-legal`); entity/banking (`company-operations-finance`); volume-repeatability hardening curriculum (`after-acceleration-roadmap`).

**Source evidence:** `docs/golden-quill-task-role-breakdown-handoff.md` Workstream F rows 70–76, Node Care row 79, support row 78, Repeatability row 90, Roles & Gaps rows 110–112; `docs/white_glove_v0_1_beta.md` §§0–7; `.craft/ledger.yml` gaps[0–2] + DESC-WGD-001; CLAUDE.md (Beta Model Strategy, Sovereignty Promise, v0.1 Beta Deployment Posture).

## 1. The seven delivery stages (the spine this wrapper attaches to)

The wrapper delta maps onto the locked spine. Each workbook stage already has a technical anchor; this node owns the human-facing artifact for each.

| # | Workbook stage (row) | Technical anchor (`white_glove_v0_1_beta.md`) | Wrapper artifact this node owns |
|---|---|---|---|
| 1 | Pre-deployment: doc request, questionnaire, posture conversation, deployment record (r70) | §0 pre-arrival checklist | Document-Request Kit · Onboarding Questionnaire · Posture-Conversation Script · Deployment Record |
| 2 | Day 0 install: hardware, network, accounts, posture, Applied As, orientation, branded closeout (r71) | §0 + §2.3 | Day-0 Install Runbook · Branded Closeout |
| 3 | Vault build: ingestion, classification, applicant profile, evidence ledger, missing-doc list (r72) | §1 BULK_INGEST + §2 Classification Review | Vault-Build Worksheet · **Missing-Doc List** |
| 4 | Source universe: manifest, search grammar, refresh cadence, first Scout scan, scored opportunities (r73) | §3.1 step 1 (Scout DISCOVER+VERIFY) | Source-Universe Manifest Worksheet |
| 5 | First opportunity packet: selection, decomposition, evidence map, blockers, draft plan (r74) | §3 first cycle dispatch | First-Opportunity Packet Template |
| 6 | First draft workflow + training sessions 2–4 (r75) | §3.2–§3.3 cycle structure | Training Curriculum (Sessions 1–4) |
| 7 | Day-60 use review: metrics, support load, renewal signal, next-cycle plan (r76) | §5 between-cycle | Day-60 Review Template (GAP-WGD-DAY60) |
| — | Node Care: updates, source-index maintenance, quarterly check-ins, vault care (r79) | §5 + update-and-signing (r41) | Node Care recurring schedule (in §2.10) |

---

# GAP-WGD-PLAYBOOK — Delivery Service Wrapper

**Severity:** block · **Owner:** Josh / Customer Success · **Treatment:** author · **Verdict: AUTHORED (block → ready-to-build).**

## 2.D — DEFINE

**Problem.** The seven delivery stages exist as workbook task rows and the technical spine is locked, but there is no repeatable, human-facing service wrapper. A trained non-founder cannot today pick up a kit and run an install the way Josh runs it. The deliverables named in row 70–76 (document-request kit, questionnaire, posture script, deployment record, training curriculum, branded closeout, missing-doc list) are unfleshed.

**Scope (in).** The seven wrapper artifacts listed in §1, authored as org-agnostic, fill-per-node templates that wrap — never replace — the locked technical spine.

**Scope (out).** The technical mechanics they wrap (BULK_INGEST extractor, Classification Review engine, posture enforcement, Scout channels, Uploader adapters) — those are locked sibling-owned components. This node references them by path; it does not redesign them.

**Definition of done.** Each of the seven artifacts has: (a) a named template structure, (b) the stage it attaches to, (c) the technical anchor it wraps, (d) a Sovereignty-Promise demonstration point, (e) acceptance criteria. A delivery operator (founder first, then CS/Field Tech) can run an end-to-end install from the kit with no tacit founder knowledge.

## 2.X — DESIGN (the seven wrapper artifacts)

Each artifact is specified as: purpose → structure → wraps → sovereignty demonstration.

### 2.1 Document-Request Kit
- **Purpose:** the pre-arrival ask that tells the operator exactly what to gather so BULK_INGEST has substance. Sent before the white-glove team arrives.
- **Structure:** categorized checklist — (a) Identity & legal (EIN, UEI, SAM status, formation docs, address, county); (b) Financials (audited financials, IRS 990, last-3-years budgets); (c) Programmatic (strategic plan, program descriptions, beneficiary aggregate data, photos, narrative essays); (d) Relationships (MOUs, partnership letters, board roster); (e) Prior grant history (last 3 years of applications, win/loss). Each row marks: *required for first cycle* vs *strengthens vault*, and *expected classification hint* (advisory only — Card-archetype default; operator confirms at Classification Review).
- **Wraps:** §0 pre-arrival + §1 BULK_INGEST input list.
- **Sovereignty demonstration:** kit states plainly that documents are ingested locally, fact-by-fact operator-confirmed, and never auto-uploaded anywhere. Classification hints are advisory, not binding.

### 2.2 Onboarding Questionnaire
- **Purpose:** capture the operator's organizational profile, grant goals, and the inputs the questionnaire-driven artifacts need (Applied-As identity, customer identity category, dialect register, gears per seat).
- **Structure:** sections — (a) Org snapshot + Customer Identity Category self-placement (the six CICs, advisory); (b) "Applied As" legal-applicant identity (the exact legal name + EIN used on submissions); (c) grant goals / target funders / timelines; (d) per-seat operating gear preference (Sparring / Co-Pilot default / Synthesizer); (e) sensitivity pre-flags (anything the operator already knows is confidential). No CIC→CLC binding is recorded (F-CIC-CLC-COUPLING-VIOLATION; CICs/CLCs are orthogonal, opportunity-driven at runtime).
- **Wraps:** §0 + feeds §2 Classification Review defaults + §3 cycle gear settings.
- **Sovereignty demonstration:** questionnaire answers stay on the operator's machine; CIC self-placement drives configuration, not eligibility constraint.

### 2.3 Posture-Conversation Script
- **Purpose:** a guided, plain-language conversation that lands the operator on one of the three deployment postures **with informed consent**, before the test cycle.
- **Structure:** (a) explain the three postures (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign) in operator language with the "what stays on your box" column from §2.1.bis; (b) walk the four per-field classes (public / shareable / confidential / operator_flagged); (c) present the routing-simulation summary for a representative cycle (the three side-by-side narratives from §2.2 step 3); (d) surface the Local-Only under-validation caveat explicitly (`local_only_validated` defaults false); (e) record the operator's selection for the Deployment Record, to be Ed25519-signed at Classification Review step 5. **Three postures only** — never revive a fourth/"Sanitized"; no opaque-slot vocabulary.
- **Wraps:** §2.1.bis + §2.2 step 3 (posture selection) + §2.3 surprises list.
- **Sovereignty demonstration:** this *is* the sovereignty conversation made concrete — the operator chooses, with eyes open, exactly what may leave the box.

### 2.4 Deployment Record
- **Purpose:** the per-node canonical record of what was delivered, configured, and signed. The audit anchor for the install.
- **Structure:** node ID / operator slug; hardware SKU + Golden Image version (referenced from `hardware-golden-image`, not authored here); BYOK envelope confirmed (keys present, operator-owned — values never recorded); operator Ed25519 public-key fingerprint; selected posture + classification-register hash + sign-off timestamp; router-template release + publisher-pubkey pin; seeded `vault_shared/funder_intelligence/` corpus version; first-cycle grant ID + outcome; install team + date. Stored as a delivery artifact (org-agnostic schema; no cross-org data).
- **Wraps:** §0 + §2.4 sign-off artifact + §3 first cycle.
- **Sovereignty demonstration:** records *that* keys are operator-owned and the private key never left the box — without ever recording key material.

### 2.5 Vault-Build Worksheet + Missing-Doc List
- **Purpose:** drive the side-by-side BULK_INGEST + Classification Review session, and produce the explicit list of documents the operator still owes for a complete vault.
- **Structure:** (a) ingestion tracker (doc → KFR candidate count → operator-confirmed count); (b) classification pass tracker (field → class → confirmed/overridden); (c) applicant profile completeness checklist (which `[NEEDED]` PROJECT_CONTEXT fields are still blank — EIN, UEI, SAM, county, production metrics, financials, boilerplate); (d) evidence ledger (fact → verbatim-quote-with-page provenance present yes/no); (e) **Missing-Doc List** — the gap between what the Document-Request Kit asked for and what was actually ingested, with impact note ("blocks federal eligibility" / "strengthens narrative"). Operator confirms each fact (no silent ingestion; F-EXTRACTOR-FABRICATION).
- **Wraps:** §1 BULK_INGEST done-condition + §2 Classification Review procedure.
- **Sovereignty demonstration:** every confirmed fact carries provenance the operator can trace; nothing enters the vault the operator did not confirm.

### 2.6 Source-Universe Manifest Worksheet
- **Purpose:** configure and validate the operator's Scout source universe and run the first scan.
- **Structure:** (a) source manifest (which of the six+seeded channel families are active for this operator); (b) search grammar / seed vocabulary tied to the operator's CIC search-vocabulary primitive; (c) refresh cadence setting; (d) first-Scout-scan results table (candidate → VERIFY status → fit); (e) scored-opportunity shortlist that feeds the First-Opportunity Packet. Scout is local-routable, zero API cost.
- **Wraps:** §3.1 step 1 (Scout DISCOVER+VERIFY).
- **Sovereignty demonstration:** discovery runs locally; the operator sees every routing decision and live-synopsis VERIFY before any candidate is elevated.

### 2.7 First-Opportunity Packet Template
- **Purpose:** structure the selection and decomposition of the first grant the operator will run end-to-end.
- **Structure:** selected opportunity + rationale; RFA decomposition into section plan (rubric weights, evidence needs, sensitivity per section — sourced from RFA per Law 1); evidence map (section → KFR facts available / missing); blockers (missing facts, `[NEEDED]` fields, deadline risk); draft plan (gear per seat, posture-driven routing expectation per section).
- **Wraps:** §3 first cycle dispatch (the input to the run).
- **Sovereignty demonstration:** every claim in the packet traces to RFA or operator-confirmed KFR fact (Law 1, Law 5 — applicant brings the substance).

### 2.8 Training Curriculum — Sessions 1–4
- **Purpose:** the standardized teaching arc that turns the operator into a self-sufficient Tilth user, delivered across the first cycle. Session 1 is the live first-cycle dispatch (founder-led); Sessions 2–4 are the named deliverable in row 75.
- **Structure:**
  - **Session 1 — First cycle, observed.** Operator watches the full pipeline run (§3.3): routing decisions, Editor flags, Judge score, Red Team probe, Logician PRE/POST, Uploader staging, operator clicks final submit. (This is the test cycle; doubles as Classification Review validation.)
  - **Session 2 — Scout & source universe.** Operator runs DISCOVER+VERIFY themselves; tunes manifest, search grammar, refresh cadence; reads a reality report.
  - **Session 3 — Drafting workflow.** Operator drives a section-by-section draft: gears, dialect register, KGIE preflight, the human editorial loop, council split tie-breaker, the approve/revise gate.
  - **Session 4 — Capture / report / remember.** AWARD_INGEST (proposal-commitments extraction at award), INCREMENTAL_INGEST (new facts default confidential), and operator-curated lessons. (Data Collector / Report Generator are v0.2 — taught as forward-compat, not live.)
- **Wraps:** §3.2–§3.3 + §4 AWARD_INGEST + §5 INCREMENTAL_INGEST.
- **Sovereignty demonstration:** by Session 4 the operator can run, route, draft, submit, and maintain their vault on hardware they own without the white-glove team present.

### 2.9 Branded Closeout
- **Purpose:** the end-of-install deliverable that hands the operator a tangible record and reinforces the sovereignty promise.
- **Structure:** branded summary referencing the Deployment Record — what was installed, what they own (hardware, keys, data, audit trail), the posture they chose and what it means, the first-cycle outcome, the Node Care cadence ahead, and a plain restatement of the Sovereignty Promise ("if FIT Farms disappeared tomorrow, you still have your box, data, keys, grants, and audit trail"). Headless: a document/PDF artifact, not a UI.
- **Wraps:** §7 closing (sovereignty promise made concrete).
- **Sovereignty demonstration:** the closeout *is* the promise in writing, node-specific.

### 2.10 Node Care recurring schedule (delivery tail)
- **Purpose:** the ongoing delivery tail (row 79) — what recurs after Day 0.
- **Structure:** signed updates (via the update-and-signing mechanism, `hardware-golden-image`/Backend-owned — referenced, not authored; router-template updates verified against pinned publisher pubkey per §6.1); source-index maintenance + refresh-cadence review; quarterly check-ins; vault care (INCREMENTAL_INGEST hygiene — new facts default confidential, mini-Classification-Review per add). Schedule is trigger-agnostic re: who runs it until GAP-WGD-CS-HANDOFF resolves.
- **Wraps:** §5 between-cycle + handoff row 41 (update-and-signing).
- **Sovereignty demonstration:** updates are operator-attested and signature-verified; no silent background model-sync (`F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD` bans alternative update channels).

## 2.P — PLAN (first steps)

1. Author the four pre-deployment artifacts first (Document-Request Kit, Onboarding Questionnaire, Posture-Conversation Script, Deployment Record) — they gate the install and have zero external dependencies.
2. Author the Vault-Build Worksheet + Missing-Doc List and Source-Universe Manifest Worksheet — they wrap already-locked §1/§2/§3.1 mechanics.
3. Author the First-Opportunity Packet Template and Training Curriculum (Sessions 1–4).
4. Author the Branded Closeout and Node Care schedule.
5. Dogfood the full kit on FIT Farms' own node (FIT Farms LLC as the `orgs/` client — Law 3 respected) as the first end-to-end repeatability proof.

## 2.A — Acceptance criteria (GAP-WGD-PLAYBOOK)

- [ ] All ten artifacts (2.1–2.10) exist as fill-per-node templates.
- [ ] Each names its stage, its technical anchor in `white_glove_v0_1_beta.md`, and one concrete Sovereignty-Promise demonstration point.
- [ ] No artifact describes reaching a first grant cycle without completed Classification Review + operator Ed25519 sign-off.
- [ ] No artifact contains a UI surface (headless guardrail).
- [ ] No artifact reads or templates against a client `orgs/` PROJECT_CONTEXT (Law 3).
- [ ] Posture script names exactly three postures; no "Sanitized"/opaque-slot vocabulary.
- [ ] **Toy-game falsification:** a delivery operator who did **not** author the kit can run a full install end-to-end from the artifacts alone (this is the repeatability proof; mirrors workbook row 57 "full install from checklist by someone who didn't write it"). Failure routes back to artifact repair.
- [ ] The branded closeout restates the Sovereignty Promise node-specifically.

---

# GAP-WGD-DAY60 — Day-60 Review Template

**Severity:** flag · **Owner:** Victor (QA) + Customer Success · **Treatment:** author · **Verdict: AUTHORED — STRUCTURE READY; metric definitions BLOCKED on `quality-security-proof` instrumentation.**

## 3.D — DEFINE

**Problem.** Day-60 review (row 76) needs four named outputs — metrics, support-load evidence, renewal signal, next-cycle plan — but the *metric definitions* depend on Workstream C instrumentation (row 61: "support hrs/node, usage metrics, baselines, renewal-intent capture"), owned by the `quality-security-proof` node. This node authors the **review structure and the renewal-signal capture shape**; it cannot finalize metric numbers/definitions.

**Dependency (marked):** Day-60 metric definitions and their measurement instrumentation are owned by `quality-security-proof` (Workstream C, row 61). This template specifies the *slots*; the metric schema fills them. **Coordinate, do not author the definitions here.**

## 3.X — DESIGN (review structure)

A per-node Day-60 review document with four sections:

1. **Metrics.** Slots fed by Workstream C instrumentation — support hours/node, usage metrics (cycles run, drafts produced, submissions staged), and baselines. **Metric *definitions* are placeholders pending the `quality-security-proof` schema; this template names the slots, not the formulas.**
2. **Support-load evidence.** Triage log summary (support-absorbed vs engineering-escalated per the row-78 triage rules), recurring issue patterns, time-to-resolution. Feeds the after-acceleration unit-economics data room (row 96).
3. **Renewal signal.** Renewal-intent capture shape (structured prompt + operator response + signal classification: strong / conditional / at-risk). Captures the signal; does not set commercial terms (sales-owned).
4. **Next-cycle plan.** Upcoming target opportunities (from refreshed Scout scan), vault gaps still open (carried from Missing-Doc List), training reinforcement needs, posture re-selection if requested (`tilth posture select`, between-cycle only).

## 3.P — PLAN (first steps)

1. Author the four-section template with metric slots as named placeholders.
2. Open a coordination item against `quality-security-proof` for the metric schema (row-61 instrumentation) — the template's metrics section binds to it when it lands.
3. Author the renewal-signal capture shape (this node owns it fully — no external dependency).

## 3.A — Acceptance criteria (GAP-WGD-DAY60)

- [ ] Template has all four sections (metrics / support-load / renewal signal / next-cycle plan).
- [ ] Metrics section marks every definition as a placeholder bound to `quality-security-proof` instrumentation (dependency explicit, not silently invented).
- [ ] Renewal-signal capture shape is fully specified and self-contained.
- [ ] Next-cycle plan reuses the Missing-Doc List and refreshed Scout scan (no duplicate authoring).
- [ ] No Law-3 cross-org data; per-node only.

---

# GAP-WGD-CS-HANDOFF — CS / Field-Tech Transition Checklist

**Severity:** flag · **Owner:** Josh → Customer Success · **Treatment:** author (trigger-agnostic) · **Verdict: AUTHORED — CHECKLIST READY; activation GATED on `staffing-budget-and-triggers`.**

## 4.D — DEFINE

**Problem.** Delivery starts founder-led and must become a CS + Field-Tech repeatable process (DESC-WGD-001; rows 90, 111–112). This node authors the **executable transition checklist** a trained non-founder follows. The **trigger threshold** (deployed-node count at which Josh stops doing installs) is owned by `staffing-budget-and-triggers` — this checklist is **trigger-agnostic** until that decision lands.

**Gate (marked):** the activation trigger (when to invoke this handoff) is owned by `staffing-budget-and-triggers`. This checklist names the trigger as an input placeholder and is otherwise complete; it does not set the threshold.

## 4.X — DESIGN (transition checklist)

A handoff checklist a trained non-founder completes to take over an install role:

1. **Prerequisite — trigger fired.** `[GATED: deployed-node-count threshold owned by staffing-budget-and-triggers]`. Checklist activates only when that node signals the trigger.
2. **Knowledge transfer.** Trainee has shadowed N founder-led installs (count TBD by the gating node); can run each of the ten GAP-WGD-PLAYBOOK artifacts unaided.
3. **Capability proof (the row-57 standard).** Trainee runs a full install end-to-end from the kit on a test/dogfood node with the founder observing-only. This is the same falsification bar as the playbook toy-game.
4. **Role split.** Field Tech owns burn-in, imaging execution, on-site hardware/peripherals (row 112 — imaging mechanics referenced from `hardware-golden-image`). Customer Success owns intake, weeks-1–4 cadence, training delivery, support front line, Node Care, Day-60 reviews (row 111).
5. **Sovereignty + Law-3 discipline check.** Trainee demonstrates correct posture conversation, classification sign-off handling (never signs on the operator's behalf), and Law-3 isolation (never cross-references client orgs).
6. **Sign-off.** Founder attests the trainee can deliver unsupervised; recorded against the Deployment Record schema for trainee-run nodes.

## 4.P — PLAN (first steps)

1. Author the six-step checklist with step 1 as an explicit `[GATED]` placeholder.
2. Bind step 3's capability proof to the same toy-game falsification as GAP-WGD-PLAYBOOK (single shared bar).
3. Open a coordination item against `staffing-budget-and-triggers` for the trigger threshold + shadow-install count.

## 4.A — Acceptance criteria (GAP-WGD-CS-HANDOFF)

- [ ] Checklist is complete and executable except for the explicitly-marked `[GATED]` trigger threshold.
- [ ] Trigger threshold is named as an input owned by `staffing-budget-and-triggers` — never invented here.
- [ ] Capability proof reuses the playbook toy-game falsification bar (row-57 standard).
- [ ] Role split matches Roles & Gaps rows 111–112; imaging mechanics referenced to `hardware-golden-image`, not authored.
- [ ] Sovereignty + Law-3 discipline is an explicit checklist item.

---

## 5. Residue and cross-node coordination

- **Posture vocabulary drift (not this node's to fix).** `docs/golden-quill-task-role-breakdown-handoff.md` row 50 still lists the stale four-posture "Unrestricted / Hybrid / Sanitized / Sovereign" naming. Superseded by the three-posture model (CLAUDE.md v7.0.10). Owner boundary: flag for the canon/quality node; the Posture-Conversation Script (2.3) uses only the current three.
- **Day-60 metric definitions** — hard dependency on `quality-security-proof` Workstream C instrumentation. Coordinate; do not author definitions.
- **CS/Field-Tech trigger threshold** — open `staffing-budget-and-triggers` decision. Checklist is trigger-agnostic until it lands.
- **Imaging / Golden Image version** referenced in the Deployment Record and Field-Tech role — owned by `hardware-golden-image`; referenced by path only.
- **External benchmarking passes (EXT-WGD-01/02/03)** remain DEFERRED enhancement-only; not required to reach a runnable wrapper.

## 6. Per-gap verdicts

- **GAP-WGD-PLAYBOOK** — **AUTHORED (block → ready-to-build).** Define→Design→Plan + acceptance criteria authored for all ten wrapper artifacts as a delta over the locked spine. No blocker; ready for Invoke-Plan work-pack.
- **GAP-WGD-DAY60** — **AUTHORED — structure ready; metric definitions BLOCKED on `quality-security-proof` instrumentation (dependency marked).** Renewal-signal shape self-contained and complete.
- **GAP-WGD-CS-HANDOFF** — **AUTHORED — checklist ready; activation GATED on `staffing-budget-and-triggers` trigger threshold (gate marked).** Otherwise executable.

**Output file:** `docs/strategy/development/white-glove-delivery-node-care/BUILD-SPEC.md`
