# BUILD-SPEC — Staffing, Budget, and Triggers

- Craft node: `staffing-budget-and-triggers`
- Source contract: `docs/golden-quill-task-role-breakdown-handoff.md` (ledger id `ART-SBT-HANDOFF`)
- Research basis: `docs/strategy/development/staffing-budget-and-triggers/development/refinement-runs/2026-06-12-craft-pipeline-hydration/RESEARCH-RESULT.md` (verdict PASS, local-first)
- Ledger: `docs/strategy/development/staffing-budget-and-triggers/.craft/ledger.yml`
- Status: **planning/spec** — scaffold authored; VALUES are operator-input. No hours, rates, or thresholds invented here.
- Guardrails honored: Law 3 (no `orgs/` read); planning-only (no runtime stages executed, no canonical/lifecycle artifact mutated).

---

## 0. Purpose and what this spec is

This node converts the workbook's role rows and empty budget columns into a **budgetable staffing state**. The workbook (`ART-SBT-HANDOFF`) carries every task, effort type, role, and assignment but leaves **every `Est. Hrs` and `Notes / Rate` cell blank** (RESEARCH-RESULT F1) and states all onboarding triggers **qualitatively only** (F5).

The two REFINE-SOLVABLE items below are authored now as fill-ready scaffolds:

- **GAP-SBT-HOURS-RATES** → §2 Budget Worksheet Template (every workbook task row × fillable {Est. Hrs, Rate, cost-type} + computed roll-up structure).
- **DEC-SBT-TRIGGER-MODEL** → §3 Trigger-Model Options (deployment-count vs revenue vs hybrid, with tradeoffs; Josh picks).

The two OPERATOR-INPUT items are surfaced as decision callouts:

- **GAP-SBT-ONBOARD-NOW** → §4 (Domain Experts, Legal, Security Reviewer — procurement shape + cost; Josh decides).
- **GAP-SBT-ONBOARD-LATER** → §3 (CS, Field Tech, Bookkeeper trigger thresholds; consumes the §3 model choice).

What is **out of scope** for this node (RESEARCH-RESULT r01 — adjacent-node content, do not pull in): hardware build/install work content (`hardware-golden-image` / `node-on-desk-readiness`), security-review/QA proof content (`quality-security-proof`), sales/legal/contracting content (`sales-contracting-legal`), white-glove delivery content (`white-glove-delivery-node-care`), team build-out narrative (`after-acceleration-roadmap`). This node reads those only as **role rows that need hours/rates/triggers**.

---

## 1. Staffing baseline (from the Role Map, no invention)

Staffed core — already filled, treated as fixed labor (RESEARCH-RESULT F2; handoff `:107-110`):

| Role | Person | Carries (summary) | Status |
| --- | --- | --- | --- |
| Founder / Grant Strategy / Deployment Lead | Josh | Sales, qualification, Capital Logic synthesis, first-opportunity strategy, early installs, capital track | Staffed |
| AI Engineer (full-stack) | Koichi | Inference, routing, ingestion, Scout, Mapper, drafting workflow, ensemble review, console UI, evidence capture | Staffed |
| Backend Engineer / Domain Modeler | Vlad | Vault, classification, posture enforcement, audit log, rule engine, OS baseline, imaging, signing, Golden Image | Staffed |
| QA / Measurement / Epistemics | Victor | Guardrails-as-tests, deployment test, claims register, demo standard, instrumentation, Day 60 evidence | Staffed |

Onboard-NOW / near-now (unfilled; §4 callout — F3; `:113-115`):

| Role | Carries | Workbook trigger (qualitative) | Decision needed |
| --- | --- | --- | --- |
| Domain Experts (×4 segments) | Structured input + field correction on Educator, Municipal, Arts, Cooperative cards | "Contract, paid structured input" | Engagement form + cost band |
| Legal (fractional) | Customer agreement, LOI, data-policy, procurement, FERPA / AI-transparency reading | "Fractional, before first LOI signs" | Engagement form + rate band |
| Security Reviewer | Independent audit of boundary enforcement + signing chain | "One-time, recurring at major releases" | Engagement form + cost band |

Onboard-LATER (founder-absorbed today; §3 thresholds — F4; `:111-112,:116`):

| Role | Carries | Currently absorbed by | Workbook trigger (qualitative) |
| --- | --- | --- | --- |
| Customer Success | Intake, weeks 1–4 cadence, training delivery, support front line, Node Care, Day 60 reviews | Josh (first nodes) | "Part-time contract as deployments stack" |
| Field / Install Tech | Burn-in, imaging execution, on-site hardware, peripherals | Engineers + Josh early | "Part-time at volume; trained from checklist" |
| Bookkeeper (fractional) | Deposits, invoicing, cost tracking, investor schedules | — | "Few hrs/month at first revenue" |

"Skills to weigh later" (F7; `:117`) — tech writing, instructional design, public-procurement fluency, hardware logistics, privacy/compliance counsel — are **not yet distinct budget lines** ("fold into above roles where possible"). Do not add budget rows for them unless the fold-in assumption breaks.

---

## 2. Budget Worksheet Template — GAP-SBT-HOURS-RATES [block, owner: Josh]

**Verdict:** REFINE-SOLVABLE scaffold authored. Every workbook task row appears below as a fillable line. Josh fills the bracketed `[…]` fields; the roll-up structure (§2.3) computes from them. **No hours or rates are supplied here** — all numeric cells are `[FILL]`.

### 2.1 Cost-type legend (from workbook `:22-29`, F6)

- **BUILD** = one-time (capital requirement)
- **PER-NODE** = repeats per customer (deployment cost)
- **ONGOING** = operating floor (recurring)

Each row carries the workbook's stated effort type. Where the workbook marks a compound type (e.g. "BUILD, then PER-NODE"), the row's cost splits across two buckets — fill an `Est. Hrs` for each applicable bucket (the `Hrs (BUILD)` / `Hrs (PER-NODE)` / `Hrs (ONGOING)` columns below). `Rate` is per-hour for the role assigned.

**Fillable field key (per row):**
- `Hrs (BUILD)` — one-time hours, blank if not BUILD
- `Hrs (PER-NODE)` — hours each deployment repeats, blank if not PER-NODE
- `Hrs (ONGOING)` — recurring hours per ONGOING period (set period in §2.3), blank if not ONGOING
- `Rate` — $/hr for the assigned role (use §2.4 role-rate table to avoid retyping; or per-row override)
- Row cost is computed, not filled (formulas in §2.3).

### 2.2 Sheet 1 — "Node on the Desk" task rows (workbook `:34-80`)

> Workstream A — Hardware & Physical Node

| # | Task | Cost type(s) | Assigned role | Hrs (BUILD) | Hrs (PER-NODE) | Hrs (ONGOING) | Rate ($/hr) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | Final hardware spec + certification of reference workstation; validate one approved alternative | BUILD | AI Engineer (Koichi) | [FILL] | — | — | [FILL] |
| A2 | Procurement process: supplier accounts, ordering, receiving, inventory | BUILD + PER-NODE | Founder/Ops (Josh) | [FILL] | [FILL] | — | [FILL] |
| A3 | Burn-in & acceptance test procedure per unit | BUILD, then PER-NODE | AI Eng → Field Tech | [FILL] | [FILL] | — | [FILL] |
| A4 | OS baseline: hardened config, disk encryption, accounts, drivers, network profile | BUILD | Backend Engineer (Vlad) | [FILL] | — | — | [FILL] |
| A5 | Imaging/cloning process — write Golden Image repeatably with verification | BUILD, then PER-NODE | Backend Eng → Field Tech | [FILL] | [FILL] | — | [FILL] |
| A6 | Peripherals kit + branded kit incl. cast-vinyl insignia | BUILD + PER-NODE | Founder/Ops (Josh) | [FILL] | [FILL] | — | [FILL] |
| A7 | Backup & export posture: local backup, customer-owned export, recovery | BUILD | Backend Engineer (Vlad) | [FILL] | — | — | [FILL] |
| A8 | Update-and-signing mechanism for deployed nodes | BUILD | Backend Engineer (Vlad) | [FILL] | — | — | [FILL] |

> Workstream B — Software / Tilth Build

| # | Task | Cost type(s) | Assigned role | Hrs (BUILD) | Hrs (PER-NODE) | Hrs (ONGOING) | Rate ($/hr) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B1 | Local inference layer: primary model, embeddings, routing model, on-demand checkpoint swap | BUILD | AI Engineer (Koichi) | [FILL] | — | — | [FILL] |
| B2 | Multi-model routing layer: policy-driven selection, card defaults, per-task override | BUILD | AI Engineer (Koichi) | [FILL] | — | — | [FILL] |
| B3 | Vault: storage, classification labels, full-text + semantic indexes, classification-aware assembly | BUILD | Backend Engineer (Vlad) | [FILL] | — | — | [FILL] |
| B4 | Ingestion pipeline: parsing, OCR, evidence extraction, document inventory | BUILD | AI Engineer (Koichi) | [FILL] | — | — | [FILL] |
| B5 | Scout: source manifest, governed fetch, fetch ledger, refresh engine, opportunity DB, reality report | BUILD | AI + Backend Eng (Koichi+Vlad) | [FILL] | — | — | [FILL] |
| B6 | Grant Module Mapper: RFA decomposition into section plan | BUILD | AI Engineer (Koichi) | [FILL] | — | — | [FILL] |
| B7 | Section-by-section drafting workflow with human editorial loop | BUILD | AI Engineer (Koichi) | [FILL] | — | — | [FILL] |
| B8 | Rubric review + compliance: multi-model ensemble + deterministic rule engine | BUILD | AI + Backend Eng (Koichi+Vlad) | [FILL] | — | — | [FILL] |
| B9 | Posture system: Unrestricted / Hybrid / Sanitized / Sovereign, technically enforced | BUILD | Backend Engineer (Vlad) | [FILL] | — | — | [FILL] |
| B10 | Sanitization pipeline + split-context drafting pattern | BUILD | AI + Backend Eng (Koichi+Vlad) | [FILL] | — | — | [FILL] |
| B11 | Audit log: every invocation, payload class, cross-boundary event, hash | BUILD | Backend Engineer (Vlad) | [FILL] | — | — | [FILL] |
| B12 | Operator console UI: read-only projection first, then interactive | BUILD | AI Engineer (Koichi) | [FILL] | — | — | [FILL] |
| B13 | Evidence capture & report drafting from captured material | BUILD | AI Engineer (Koichi) | [FILL] | — | — | [FILL] |
| B14 | Golden Image assembly: one installable, versioned, signed artifact | BUILD | Backend (lead) + AI Eng (Vlad+Koichi) | [FILL] | — | — | [FILL] |

> Workstream C — Quality, Security & Proof

| # | Task | Cost type(s) | Assigned role | Hrs (BUILD) | Hrs (PER-NODE) | Hrs (ONGOING) | Rate ($/hr) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | Test plan + guardrails-as-tests | BUILD | QA/Measurement (Victor) | [FILL] | — | — | [FILL] |
| C2 | Internal deployment test: full install from checklist by someone who didn't write it | BUILD | QA/Measurement (Victor) | [FILL] | — | — | [FILL] |
| C3 | Independent security review: data boundary, Sovereign build, signing chain | BUILD | External Security Reviewer (onboard NOW — see §4) | [FILL] | — | — | [FILL] |
| C4 | Claims register: every external claim mapped to its evidence category | BUILD + ONGOING | QA/Measurement (Victor) | [FILL] | — | [FILL] | [FILL] |
| C5 | Canonical demo standard (Scout population sequence) | BUILD | QA/Measurement (Victor) | [FILL] | — | — | [FILL] |
| C6 | Instrumentation: support hrs/node, usage metrics, baselines, renewal-intent capture | BUILD, then ONGOING | QA/Measurement (Victor) | [FILL] | — | [FILL] | [FILL] |

> Workstream D — Capital Logic Content

| # | Task | Cost type(s) | Assigned role | Hrs (BUILD) | Hrs (PER-NODE) | Hrs (ONGOING) | Rate ($/hr) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D1 | Card schema + governance: structure, section-level defaults, testability rules | BUILD | Founder + Backend Eng (Josh+Vlad) | [FILL] | — | — | [FILL] |
| D2 | Author & validate five launch cards with paid expert review | BUILD | Founder + Domain Experts (Josh + onboard NOW — see §4) | [FILL] | — | — | [FILL] |
| D3 | Search seed libraries + source universes per segment | BUILD | Founder (Josh) | [FILL] | — | — | [FILL] |
| D4 | Program rule packs for recurring funders | BUILD + ONGOING | Founder + Backend Eng (Josh+Vlad) | [FILL] | — | [FILL] | [FILL] |

> Workstream E — Selling & Contracting

| # | Task | Cost type(s) | Assigned role | Hrs (BUILD) | Hrs (PER-NODE) | Hrs (ONGOING) | Rate ($/hr) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | Sales materials: one-pager, demo, segment framing, pipeline tracker w/ disclosure rules | BUILD | Founder (Josh) | [FILL] | — | — | [FILL] |
| E2 | Qualification: readiness checklist, fluency test, fit/no-fit referral | PER-NODE | Founder (Josh) | — | [FILL] | — | [FILL] |
| E3 | Customer agreement, LOI template, data-policy spec, procurement notes, insurance | BUILD | Legal (fractional, onboard NOW — see §4) + Founder | [FILL] | — | — | [FILL] |
| E4 | Deposit handling, invoicing, deployment cost tracking | PER-NODE | Bookkeeper (fractional, onboard at first revenue — see §3) | — | [FILL] | — | [FILL] |

> Workstream F — White-Glove Delivery (every customer)

| # | Task | Cost type(s) | Assigned role | Hrs (BUILD) | Hrs (PER-NODE) | Hrs (ONGOING) | Rate ($/hr) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Pre-deployment: document request, onboarding questionnaire, posture conversation, deployment record | PER-NODE | Customer Success (Josh early → onboard later — §3) | — | [FILL] | — | [FILL] |
| F2 | Day 0 install: hardware, network, accounts, posture, Applied As, orientation, branded closeout | PER-NODE | Deployment Lead (Josh early → CS + Field Tech — §3) | — | [FILL] | — | [FILL] |
| F3 | Vault build: ingestion, classification, applicant profile, evidence ledger, missing-doc list | PER-NODE | Customer Success + Founder (Josh early → onboard later — §3) | — | [FILL] | — | [FILL] |
| F4 | Source universe: manifest, search grammar, refresh cadence, first Scout scan, scored opportunities | PER-NODE | Founder + Customer Success (Josh early → onboard later — §3) | — | [FILL] | — | [FILL] |
| F5 | First opportunity packet: selection, decomposition, evidence map, blockers, draft plan | PER-NODE | Founder (Josh) | — | [FILL] | — | [FILL] |
| F6 | First draft workflow + training sessions 2–4 | PER-NODE | Customer Success (Josh early → onboard later — §3) | — | [FILL] | — | [FILL] |
| F7 | Day 60 use review: metrics, support load, renewal signal, next-cycle plan | PER-NODE | Customer Success + QA (Josh/Victor → onboard later — §3) | — | [FILL] | — | [FILL] |

> Workstream G — Company Operations

| # | Task | Cost type(s) | Assigned role | Hrs (BUILD) | Hrs (PER-NODE) | Hrs (ONGOING) | Rate ($/hr) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| G1 | Entity hygiene, banking, bookkeeping, contracts filing, insurance | ONGOING | Founder + Bookkeeper (Josh + onboard later — §3) | — | — | [FILL] | [FILL] |
| G2 | Support channel + issue log; triage rules | BUILD, then ONGOING | Customer Success + Engineers (team early → onboard later — §3) | [FILL] | — | [FILL] | [FILL] |
| G3 | Node Care delivery: updates, source-index maintenance, quarterly check-ins, vault care | ONGOING | Customer Success + Backend (team early → onboard later — §3) | — | — | [FILL] | [FILL] |
| G4 | Investor/funder relations, validation packet maintenance | ONGOING | Founder + QA/Measurement (Josh + Victor) | — | — | [FILL] | [FILL] |

### 2.2b Sheet 2 — "After Acceleration" theme rows (workbook `:88-97`)

These are forward (post-acceleration) themes, owned downstream by `after-acceleration-roadmap`. They are listed here as **fillable budget lines only if Josh wants to pre-budget them**; otherwise leave blank — they are not part of the v0.1 node-on-desk capital ask. Cost-type is theme-level (mostly BUILD/ONGOING transition); fill at theme granularity.

| # | Theme | Role | Est. Hrs | Rate ($/hr) | Cost type |
| --- | --- | --- | --- | --- | --- |
| AA1 | Repeatability (deployment playbook hardened; install labor driven down; training curriculum) | CS lead + Field Tech | [FILL or blank] | [FILL or blank] | [FILL] |
| AA2 | Sales beyond founder network (partner channels; case studies; segment campaigns) | Founder → Sales/Partnerships role | [FILL or blank] | [FILL or blank] | [FILL] |
| AA3 | Product hardening (Sovereign-mode audited; sanitization GA; multi-seat; fleet updates) | AI + Backend Eng; full-time tech hire | [FILL or blank] | [FILL or blank] | [FILL] |
| AA4 | Capital Logic Library (outcome-data opt-in; pattern feedback; offline refinement; expert bench) | Founder + AI Eng + Domain Experts | [FILL or blank] | [FILL or blank] | [FILL] |
| AA5 | Service line validation (grant-admin pilots; measure labor/risk; conditional admin hire) | Founder; Admin Lead (conditional) | [FILL or blank] | [FILL or blank] | [FILL] |
| AA6 | New markets (Tribal-nation Sovereign pilots; institutional research; consortiums) | Founder + Backend Eng; Security Reviewer | [FILL or blank] | [FILL or blank] | [FILL] |
| AA7 | Next financing (data room, unit economics, support-load + renewal evidence, channel plan) | Founder + QA/Measurement | [FILL or blank] | [FILL or blank] | [FILL] |
| AA8 | Team build-out (full-time tech hire; CS hire; field tech; possibly sales — sequenced vs node count) | Founder (hiring); whole team | [FILL or blank] | [FILL or blank] | [FILL] |

### 2.3 Computed roll-up structure

These are the **computed** fields — Josh fills §2.2 cells, these derive. Definitions are explicit so a spreadsheet (or downstream Invoke-plan stage) can implement them deterministically.

**Per-row cost (by bucket):**
- `row_build_cost   = Hrs(BUILD)   × Rate`
- `row_pernode_cost = Hrs(PER-NODE) × Rate`   (cost **per deployment**)
- `row_ongoing_cost = Hrs(ONGOING) × Rate`    (cost **per ONGOING period**, period set below)

**ONGOING period** (set once, applies to all ONGOING rows): `[FILL — monthly | quarterly | annual]`. All `Hrs (ONGOING)` are entered against this period.

**Workstream subtotals** (sum across rows within A…G, per bucket):
- `WS_build[X]   = Σ row_build_cost   for rows in workstream X`
- `WS_pernode[X] = Σ row_pernode_cost for rows in workstream X`
- `WS_ongoing[X] = Σ row_ongoing_cost for rows in workstream X`

**Node-on-desk totals (the three headline numbers):**
- `TOTAL_BUILD   = Σ WS_build[A..G]`     → one-time capital requirement (the build ask)
- `TOTAL_PERNODE = Σ WS_pernode[A..G]`   → marginal cost to deploy one additional node
- `TOTAL_ONGOING = Σ WS_ongoing[A..G]`   → operating floor per ONGOING period

**Scenario projections (derive, do not fill):**
- `cost_at_N_nodes = TOTAL_BUILD + (N × TOTAL_PERNODE) + (deployment_window_periods × TOTAL_ONGOING)`
  where `N` = number of deployed nodes and `deployment_window_periods` = how many ONGOING periods the projection spans. Use this with §3 trigger thresholds to compute the staffing-cost step at each trigger point.

### 2.4 Role-rate reference table (fill once, reuse)

To avoid retyping a rate on every row, fill each role's blended $/hr here; §2.2 rows may reference it or override per-row. Staffed-core "rates" may be a loaded cost, founder opportunity cost, or $0 if equity-only — Josh decides the accounting convention (note it).

| Role | Blended $/hr | Accounting note |
| --- | --- | --- |
| Founder (Josh) | [FILL] | [FILL — e.g. loaded cost / opportunity cost / $0 equity] |
| AI Engineer (Koichi) | [FILL] | [FILL] |
| Backend Engineer (Vlad) | [FILL] | [FILL] |
| QA/Measurement (Victor) | [FILL] | [FILL] |
| Customer Success (contract) | [FILL] | rate band — see §4 / EXT-2 if external comparison approved |
| Field / Install Tech (contract) | [FILL] | rate band — see EXT-2 if approved |
| Domain Experts (×4) | [FILL] | honorarium/contract — see EXT-3 if approved |
| Legal (fractional) | [FILL] | retainer or hourly — see EXT-1 if approved |
| Security Reviewer | [FILL] | one-time + recurring — see EXT-1 if approved |
| Bookkeeper (fractional) | [FILL] | few hrs/month — see EXT-1 if approved |

> **Rate-band research is deferred, not invented.** RESEARCH-RESULT r04 names three bounded external passes (EXT-1 fractional legal/security/bookkeeping bands; EXT-2 field-tech/install labor benchmarks; EXT-3 domain-expert honoraria). These run **only after Josh approves the rg03 external-research gate**. Until then, every `[FILL]` rate is operator-input.

---

## 3. Trigger-Model Options — DEC-SBT-TRIGGER-MODEL [owner: Josh] + GAP-SBT-ONBOARD-LATER [flag]

**Verdict:** REFINE-SOLVABLE options framing authored. The model is presented; **Josh picks**. The workbook states triggers qualitatively only ("as deployments stack", "at volume", "at first revenue") with no numeric thresholds (F5). This section gives the option set; the chosen model's thresholds then feed the §2.3 scenario projection.

**Roles governed by this decision** (the onboard-later set, F4): Customer Success, Field / Install Tech, Bookkeeper.

### 3.1 The three trigger models

**Option A — Deployment-count triggers.** Each absorbed role moves to paid staffing at a node-count threshold (e.g. CS contract at node #__, Field Tech at node #__).
- *Pro:* Directly tied to the operational load that actually creates the work (each node = a fixed slug of install + onboarding + Node Care hours). Easy to forecast against the pipeline. Matches workbook language for CS ("as deployments stack") and Field Tech ("at volume").
- *Con:* A node can be high-revenue or low-revenue; count ignores whether the revenue exists to pay the hire. Risk of triggering a cost before cash supports it. Weak fit for Bookkeeper, whose work tracks money flow, not node count.

**Option B — Revenue triggers.** Each role moves to paid staffing at a revenue threshold (e.g. Bookkeeper at first revenue $__/mo, CS at $__ ARR/run-rate).
- *Pro:* Cash-safe — never triggers a cost before the revenue to fund it exists. Natural fit for Bookkeeper ("at first revenue"). Aligns spend to ability to pay.
- *Con:* Decouples staffing from operational load. Several deployments could pile up unpaid-for (slow-paying or deposit-deferred customers) and overload Josh before the revenue line trips. Weak fit for Field Tech, whose load is physical-node-driven.

**Option C — Hybrid (first-of / both-of) triggers.** Per role, combine a count threshold and a revenue threshold with an explicit OR / AND rule:
- *OR (whichever first):* triggers on operational pressure **or** cash availability, whichever comes first — protects Josh's time aggressively.
- *AND (both required):* triggers only when load **and** cash both justify it — protects cash conservatively.
- *Pro:* Lets each role use the trigger that fits its work — Field Tech on count, Bookkeeper on revenue, CS on a hybrid. Most faithful to the workbook, which already mixes "as deployments stack" with "at first revenue".
- *Con:* More thresholds to set and track; needs the §2 instrumentation (C6 support-hrs/node) live to evaluate. Slightly more bookkeeping of the triggers themselves.

### 3.2 Tradeoff summary

| Model | Protects | Risks | Best-fit roles |
| --- | --- | --- | --- |
| A — Count | Josh's time vs operational load | Cost before cash | CS, Field Tech |
| B — Revenue | Cash position | Founder overload before revenue trips | Bookkeeper |
| C — Hybrid | Both (per-role tuned) | Setup + tracking complexity | All three, per-role |

### 3.3 Threshold worksheet (fill after model chosen) — OPERATOR-INPUT [GAP-SBT-ONBOARD-LATER]

> **OPERATOR DECISION — Josh:** (1) pick a trigger model (A / B / C), then (2) fill the thresholds for the chosen model. Do not fill the columns belonging to a model you did not pick.

| Absorbed role | Count threshold (Option A/C) | Revenue threshold (Option B/C) | Hybrid rule (Option C: OR / AND) | Target engagement at trigger |
| --- | --- | --- | --- | --- |
| Customer Success | [FILL — node #] | [FILL — $/period] | [FILL — OR / AND / n.a.] | [FILL — part-time contract hrs/wk] |
| Field / Install Tech | [FILL — node #] | [FILL — $/period] | [FILL — OR / AND / n.a.] | [FILL — part-time/per-install] |
| Bookkeeper | [FILL — node #] | [FILL — $/period] | [FILL — OR / AND / n.a.] | [FILL — hrs/month] |

Chosen model: `[FILL — A | B | C]`. Once filled, each threshold marks the point on the §2.3 `cost_at_N_nodes` curve where that role's §2 PER-NODE/ONGOING hours shift from founder-absorbed (rate per §2.4 founder convention) to the paid contract rate.

---

## 4. Onboard-NOW staffing decisions — GAP-SBT-ONBOARD-NOW [flag] — OPERATOR-INPUT

**Verdict:** OPERATOR-INPUT callout authored. These three roles are needed at/near now (F3); each needs a **procurement shape** (engagement form) and a **cost band** from Josh. Cost bands may draw on deferred external research (EXT-1/EXT-3) only after rg03 approval — not invented here.

> **OPERATOR DECISION — Josh:** for each role, set the engagement form and either a rate/cost band now, or mark "await EXT-1/EXT-3" if you want the bounded external comparison first.

| Role | Workbook trigger | Engagement form (decide) | Cost band (decide / defer) | Feeds budget row(s) |
| --- | --- | --- | --- | --- |
| Domain Experts (×4 segments) | "Contract, paid structured input" | [FILL — per-card honorarium / hourly contract / retainer] | [FILL — $ per card or $/hr; or "await EXT-3"] | D2 (and AA4 later) |
| Legal (fractional) | "Fractional, before first LOI signs" | [FILL — flat package for agreement set / hourly / monthly retainer] | [FILL — $; or "await EXT-1"] | E3 |
| Security Reviewer | "One-time, recurring at major releases" | [FILL — one-time audit fee + recurring per-release] | [FILL — $ one-time + $/release; or "await EXT-1"] | C3 (and AA6 later) |

These costs are predominantly **BUILD** (one-time, capital) with a recurring tail for Security Reviewer (per major release) — enter them in the matching §2.2 rows once decided.

---

## 5. Per-gap verdicts (summary)

- **GAP-SBT-HOURS-RATES** [block, owner: Josh] — REFINE-SOLVABLE: scaffold authored. §2 gives every workbook task row (Sheets 1 & 2) as fillable {Hrs×bucket, Rate, cost-type} lines + a deterministic roll-up structure (§2.3) and a reusable role-rate table (§2.4). VALUES are operator-input; no hours/rates invented. Rate-band external research (EXT-1/2/3) remains rg03-gated.
- **DEC-SBT-TRIGGER-MODEL** [owner: Josh] — REFINE-SOLVABLE: options framing authored. §3 presents three models (deployment-count / revenue / hybrid) with pros, cons, and best-fit roles; Josh selects and fills the §3.3 threshold worksheet. Selection still PENDING (operator decision).
- **GAP-SBT-ONBOARD-NOW** [flag, owner: Josh] — OPERATOR-INPUT: §4 callout authored for Domain Experts, Legal, Security Reviewer (engagement form + cost band). Decision open.
- **GAP-SBT-ONBOARD-LATER** [flag, owner: operations/founder] — OPERATOR-INPUT: §3.3 threshold worksheet authored for Customer Success, Field Tech, Bookkeeper; consumes the §3 model choice. Decision open.

## 6. Residue / constraints (carried from RESEARCH-RESULT)

- The **hours** dimension of GAP-SBT-HOURS-RATES and all of GAP-SBT-ONBOARD-LATER are operator-input residue — no research closes them; they require Josh's numbers and the trigger-model decision.
- External rate research (EXT-1/2/3) is **deferred** pending Josh's rg03 approval; no external lookup performed in this spec.
- "Skills to weigh later" (F7) are not budget lines yet; revisit only if the fold-into-existing-roles assumption breaks.
- Law 3 held: no `orgs/` PROJECT_CONTEXT read; all content is Golden Quill project scope. Planning/spec only — no canonical or lifecycle artifact mutated; `.craft/ledger.yml` untouched.
