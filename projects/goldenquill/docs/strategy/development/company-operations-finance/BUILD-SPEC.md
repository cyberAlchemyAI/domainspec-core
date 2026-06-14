# BUILD-SPEC — Company Operations & Finance (Node `company-operations-finance`)

**Status:** REFINE-authored, implementation-ready (planning/spec only — no runtime execution).
**Authored:** 2026-06-13.
**Craft node:** `company-operations-finance` (`CTX-COF-ROOT`).
**Owns:** workbook Workstream G (Company Operations), rows 77–80.
**Source contract:** `docs/golden-quill-task-role-breakdown-handoff.md` (`ART-COF-HANDOFF`), Workstream G + §2 After Acceleration + §3 Roles & Gaps.
**Refine evidence:** `docs/strategy/development/company-operations-finance/development/refinement-runs/2026-06-12-craft-pipeline-hydration/RESEARCH-RESULT.md` (verdict PASS, local-first sufficient) + `.craft/ledger.yml` + `REFINE-DISPATCH.json`.
**Refine route consumed:** Define → Design → Plan per `INVOKE-FIRST-ARTIFACTS.md`; `GAP-COF-SUPPORT-TRIAGE` (block severity) leads.

---

## Scope & Guardrails

**In scope (this node):** the FIT Farms Commons / Golden Quill business operating floor — entity hygiene, banking, bookkeeping, contracts filing, insurance; support channel + issue log + triage; Node Care operating cadence; investor/funder validation-packet maintenance.

**Out of scope (do NOT pull in):**
- Client orgs under `orgs/` — Law 3 (Org Isolation). This node concerns FIT Farms Commons' own business operations, never client-applicant data.
- Selling & Contracting (Workstream E: deposit handling, invoicing mechanics, customer agreement, LOI) → `sales-contracting-legal` node. (This node *consumes* the bookkeeping outputs of E's deposit/invoice events but does not own the contracting instruments.)
- White-Glove Delivery per-customer Day 0 / Day 60 (Workstream F) → `white-glove-delivery-node-care` node. (Node Care here is the *ongoing operating cadence after handoff*, not the per-customer install.)
- Quality/Security/Proof claims register + instrumentation (Workstream C) → `quality-security-proof` node. The validation packet (G) **consumes** C's evidence; it does not own or produce it. **Cross-node dependency, not scope merge** (see §VP).

**Operator-input boundary:** the fractional **Bookkeeper** is unstaffed (trigger: first revenue) and **Customer Success** is fractional (trigger: deployments stack). These specs encode the **trigger conditions and the work each role assumes on activation** — they do not make the hire decision. Until triggers fire, Josh (Founder/Ops) carries the floor.

**Entity framing (per CLAUDE.md):** FIT Farms LLC is the current operating legal entity; "FIT Farms Commons" is the owner/operator file-label resolving to FIT Farms LLC today. BYOK-only, no metered billing, sovereignty promise. Bookkeeping/billing specs must NOT assume metered usage revenue or any hosted-service billing model — revenue is hardware sale + deposit + (later) Node Care subscription.

---

## GAP-COF-SUPPORT-TRIAGE [block] — Support channel, issue-log schema, triage routing

**Owner:** Customer Success + Engineers (`customer-success-engineering`). Until CS staffs, Josh runs L1; escalation reaches Vlad (Backend) / Koichi (AI). **Effort:** BUILD-then-ONGOING.
**Leads the node** (highest severity; the support-vs-engineering boundary other ops depend on).

### Define
The single intake-and-routing surface for everything a deployed-node customer reports: questions, breakage, feature asks, and security/data-boundary concerns. The load-bearing decision is the **routing boundary**: which issues *support absorbs* (answered/resolved without consuming engineer time) versus which *engineering sees* (escalated to Vlad/Koichi). This boundary directly governs the support-load instrumentation that feeds the validation packet (renewal/unit-economics story), so it must be explicit and logged from node #1.

### Design

**Support channel (v0.1, founder-run, scales to fractional CS):**
- Single intake address per the sovereignty posture — a dedicated support email/inbox owned by FIT Farms Commons (not a per-customer engineer's personal contact). Phone/text optional as a documented escalation for Day-0/critical only.
- One issue thread per reported problem; channel is the *capture* surface, the issue log is the *system of record*.
- No customer confidential/vault content leaves the customer node into the support log — support log records the *problem and resolution metadata*, not applicant grant data (Law 3 + sovereignty).

**Issue-log schema** (one row per issue; flat file / spreadsheet at v0.1, structured table when CS staffs):

| Field | Type | Notes |
| --- | --- | --- |
| `issue_id` | string | Sequential, e.g. `ISS-0001`. |
| `opened_at` / `closed_at` | datetime | For support-hrs/node and time-to-resolve metrics. |
| `node_id` / `customer` | string | Which deployed Golden Quill. Maps to instrumentation (Workstream C). |
| `reporter` | string | Customer contact. |
| `category` | enum | `how-to` · `config` · `data/vault` · `hardware` · `model/inference` · `posture/security` · `feature-request` · `billing/ops` · `unknown`. |
| `severity` | enum | `S1-down` (node unusable / data-boundary breach) · `S2-degraded` · `S3-question` · `S4-cosmetic/enhancement`. |
| `tier` | enum | `L1-support-absorbs` · `L2-engineering-sees` · `L3-security-review` (see routing rules). |
| `routed_to` | string | `support` · `Vlad` · `Koichi` · `Victor (QA)` · `security-reviewer`. |
| `disposition` | enum | `resolved` · `workaround` · `escalated` · `feature-logged` · `wont-fix` · `duplicate`. |
| `support_minutes` | int | Effort attributed to support (feeds support-load evidence). |
| `engineering_minutes` | int | Effort attributed to engineering when L2/L3 (feeds true cost-to-serve). |
| `linked_release` | string | Update/version that fixes it, if applicable (ties to Node Care updates). |
| `renewal_signal` | enum-nullable | `positive` · `neutral` · `at-risk` — captured when an issue surfaces a renewal-relevant signal (feeds validation packet). |

**Routing rules — the "support absorbs vs. engineering sees" boundary:**

*Support absorbs (L1)* — resolve without engineer time:
- `how-to`, orientation, training-recap, "where is X" questions answerable from the deployment record / white-glove playbook.
- `config` changes inside documented, customer-permitted settings (posture re-selection guidance, source-index refresh trigger, account/peripheral issues).
- Known issues with a published workaround in the support knowledge base.
- Triage + reproduction + complete issue-log entry for everything (support always opens the row, even when it escalates).

*Engineering sees (L2 — Vlad/Koichi)* — escalate when:
- `severity` is `S1-down` or `S2-degraded` AND not resolvable by documented config.
- Category is `hardware`, `model/inference`, or `data/vault` AND the cause is suspected in the Golden Image / runtime, not customer action.
- A defect reproduces (not one-off), OR ≥2 nodes report the same symptom (fleet signal → release fix → `linked_release`).
- `feature-request` that requires a code/Card change (log it; route to roadmap, not an immediate fix).
- **Routing split:** Backend/infra/vault/posture/imaging → **Vlad**; inference/routing/Scout/Mapper/drafting/console → **Koichi**. Ambiguous → support pings Josh to assign.

*Security review (L3 — escalate immediately, do not absorb)* — any of:
- `posture/security` category, OR any suspected data-boundary breach / cross-boundary leak / signing-chain anomaly.
- Route to Vlad (boundary enforcement / audit-log owner) AND flag the external Security Reviewer for major-release re-audit per Workstream C.
- S1 by definition; opens an incident note alongside the issue row.

**Absorb-vs-escalate one-line test:** *"Can support resolve this from documented, customer-permitted settings and the knowledge base without an engineer touching the runtime or the data boundary?"* Yes → L1. No → L2. Touches the data boundary or signing chain → L3.

### Plan (first steps)
1. Stand up the support inbox + the issue-log file (schema above) before the first customer node ships. (`stages/02-invoke-define` → `09-invoke-plan` equivalent: this is the Plan artifact.)
2. Seed the L1 knowledge base from the white-glove playbook how-to content (`docs/white_glove_v0_1_beta.md`) as it lands.
3. Write the escalation contact card (Vlad/Koichi/Victor/security-reviewer + the routing split) and pin it to the support surface.
4. Every issue, from #1, gets a full row including `support_minutes` / `engineering_minutes` — this is the instrumentation feed, not optional.

### Acceptance criteria
- [ ] A single named support intake surface exists and is documented in the customer closeout.
- [ ] Issue-log schema is instantiated with all fields above; row #1 capturable before first node ships.
- [ ] Routing rules enumerate L1/L2/L3 with the absorb-vs-escalate test and the Vlad/Koichi domain split.
- [ ] `support_minutes` and `engineering_minutes` are mandatory per row (no closed issue without effort attribution).
- [ ] Every escalation records `routed_to` + `disposition`; security-class issues fail-closed to L3 (never absorbed).
- [ ] No customer vault/applicant content is written to the support log (Law 3 / sovereignty check).

---

## GAP-COF-ENTITY-HYGIENE [flag] — Entity, banking, bookkeeping, filing, insurance checklist

**Owner:** Founder + Bookkeeper (`founder-bookkeeper`). Bookkeeper unstaffed; **trigger: first revenue** (few hrs/month). Josh carries until then. **Effort:** ONGOING.

### Define
The recurring administrative floor that keeps FIT Farms LLC (= FIT Farms Commons owner-role) in good standing and financially legible: clean entity separation, banking discipline, monthly bookkeeping close, contract/document filing, and insurance cadence. Output is an **operating checklist with cadences**, not a one-time setup.

### Design — operating checklist (cadence-tagged)

**Entity hygiene (annual + event-driven):**
- LLC registered-agent + annual report / franchise filing on the state calendar (filing-calendar entry with due date + reminder lead time).
- Operating agreement, EIN, and entity documents filed in the contracts/legal filing store.
- Entity-separation discipline: no commingling of FIT Farms LLC funds with personal or with any client org. (Reinforces Law 3 at the financial layer.)

**Banking (monthly + event-driven):**
- Dedicated business operating account; deposits (hardware/deposit revenue from Workstream E) land here and are reconciled monthly.
- Separate reserve/tax-set-aside discipline as revenue starts.
- Banking access list reviewed at each role-staffing event (bookkeeper onboarding triggers an access-grant review).

**Bookkeeping (monthly close + quarterly):**
- Monthly close: categorize transactions, reconcile bank/credit accounts, capture deployment cost tracking (BOM, peripherals, shipping per node — sourced from Workstream A/E cost events).
- Track per-node deployment cost vs. revenue to feed **unit economics** (validation packet input).
- Quarterly: estimated-tax checkpoint, financial snapshot for the investor schedule.
- **Bookkeeper-staffing trigger = first revenue.** On trigger: hand the monthly-close checklist + chart of accounts + access to the fractional bookkeeper; Josh retains review/sign-off.

**Contracts filing (event-driven):**
- Single filing store for signed customer agreements, LOIs, data-policy specs (instruments owned by `sales-contracting-legal` node — this node files and tracks them), insurance policies, vendor/supplier accounts (Workstream A procurement).
- Each filed instrument has: counterparty, effective/expiry date, renewal-reminder.

**Insurance (annual review + event-driven):**
- Categories to carry/review: general liability, professional/E&O (grant-writing service + AI output), cyber/data (sovereignty posture-relevant), property/equipment (hardware inventory + in-transit), and procurement-required coverage named in customer agreements.
- Annual policy review; event-driven re-check when a new customer agreement names a coverage requirement (handoff seam with `sales-contracting-legal`).

### Plan (first steps)
1. Build the **filing calendar** (entity filings, insurance renewals, quarterly tax checkpoints) as a single dated reminder list.
2. Confirm business account + chart of accounts exist; if not, that is the first founder action.
3. Author the monthly-close checklist as the bookkeeper-handoff package (dormant until first-revenue trigger).
4. Create the contracts/insurance filing store with the per-instrument metadata fields.

### Acceptance criteria
- [ ] Checklist enumerates all five domains (entity, banking, bookkeeping, filing, insurance) each tagged with a cadence (monthly / quarterly / annual / event-driven).
- [ ] Filing calendar exists with due dates + reminder lead times for entity filings, insurance renewals, tax checkpoints.
- [ ] Monthly-close checklist is authored and packaged as a bookkeeper-handoff, gated on the first-revenue trigger (encodes trigger, not hire).
- [ ] Deployment cost tracking produces per-node cost data consumable by the validation packet's unit-economics section.
- [ ] No commingling of FIT Farms LLC funds with personal or any client-org funds (entity-separation check).

---

## GAP-COF-NODE-CARE-OPS [flag] — Node Care operating cadence

**Owner:** Customer Success + Backend (`customer-success-backend`). CS fractional (trigger: deployments stack); Josh + Vlad carry early. **Effort:** ONGOING. **Treatment:** coordinate (with `white-glove-delivery-node-care` node, which owns per-customer install; this node owns the steady-state cadence).

### Define
The recurring care of a deployed Golden Quill *after* white-glove handoff: keeping it updated, keeping its source index fresh, checking in on a fixed cadence, and tending the vault. Output is an **operating cadence** (who does what, how often, on what trigger) for the four named activities — updates, source-index maintenance, quarterly check-ins, vault care.

### Design — Node Care cadence

| Activity | Cadence | Owner | What it does | Cross-refs |
| --- | --- | --- | --- | --- |
| **Updates** | Event-driven (release) + verify quarterly | Backend (Vlad) → CS executes | Apply signed router-template / Golden Image updates via the update-and-signing mechanism (Workstream A). Verify Ed25519 signature against pinned publisher key (F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID fail-closed). Log to issue-log `linked_release`. | Workstream A update mechanism; CLAUDE.md router-template signing |
| **Source-index maintenance** | Per the customer's refresh cadence (set at white-glove) | CS → Backend if fetch/ingest breaks | Trigger Scout source-index refresh; confirm fetch ledger healthy; surface stale/broken sources. Customer-facing config, support-absorbable (L1) unless ingest pipeline breaks (→ L2 Koichi). | Workstream F source universe; Scout |
| **Quarterly check-in** | Quarterly | CS (Josh early) | Scheduled customer touchpoint: usage review, support-load recap, surface renewal signal (`renewal_signal` → validation packet), confirm posture still fits, collect next-cycle needs. | Day-60 review (Workstream F) is the *first* one; this is the recurring successor |
| **Vault care** | Quarterly + event-driven | Backend (Vlad) → CS surfaces | Backup/export-posture verification (customer-owned export works, recovery tested), classification register health, KFR/fact expiry awareness, audit-log integrity spot-check. Stays on the customer node (sovereignty) — care is verification, not data extraction. | Workstream A backup/export; classification register |

**Boundary with white-glove node:** white-glove (`white-glove-delivery-node-care`) owns Day 0 install and Day 60 first review. Node Care here is the **steady-state quarterly cadence that begins after Day 60**. The quarterly check-in is the recurring continuation of the Day-60 review template.

**Sovereignty rule:** all Node Care is verification/maintenance performed with customer consent; nothing extracts customer vault content off-node. Care confirms the customer's own export/backup works — it does not centralize their data.

### Plan (first steps)
1. Author the quarterly check-in template (reuse the Day-60 review structure; add renewal-signal capture).
2. Define the update-application runbook referencing the signed-update mechanism + signature-verification fail-closed gate.
3. Define the vault-care verification checklist (backup/export test, classification health, audit-log spot-check).
4. Map each activity's L1/L2 routing into the support triage tiers (consistency with `GAP-COF-SUPPORT-TRIAGE`).

### Acceptance criteria
- [ ] All four activities (updates, source-index maintenance, quarterly check-ins, vault care) have an explicit cadence + owner + trigger.
- [ ] Update application requires Ed25519 signature verification against the pinned publisher key (fail-closed) and logs to the issue-log `linked_release`.
- [ ] Quarterly check-in template captures usage, support-load, and `renewal_signal` (feeds validation packet).
- [ ] Vault care verifies customer-owned export/backup + recovery without extracting vault content off-node (sovereignty check).
- [ ] CS-staffing trigger ("as deployments stack") is encoded; Josh/Vlad carry until then.
- [ ] Boundary with `white-glove-delivery-node-care` is stated: this node = post-Day-60 steady state.

---

## GAP-COF-VALIDATION-PACKET [flag] — Validation / investor packet structure

**Owner:** Josh (Founder) + Victor (QA/Measurement) (`founder-qa`). **Effort:** ONGOING. **Treatment:** coordinate.
**CROSS-NODE DEPENDENCY (explicit):** the packet **consumes** the `quality-security-proof` node's **claims register** (Workstream C, row 59) and **instrumentation** (row 61: support-hrs/node, usage metrics, baselines, renewal-intent capture). This node owns the *packet structure and maintenance cadence*; it does **not** own or produce the underlying QA evidence. The hand-off seam is specified below.

### Define
The maintained evidence package presented to the next financing round / investors / funders. Per Workstream §2 (After Acceleration → Next financing), its contents are: **data room, measured unit economics, support-load evidence, renewal data, channel plan.** Output is the **packet structure + the per-section evidence source + maintenance cadence**, with each evidentiary claim traceable to its producing node.

### Design — packet structure & evidence sourcing

| Section | Contents | Evidence source | Cadence |
| --- | --- | --- | --- |
| **Data room** | Entity docs, cap structure, signed customer agreements/LOIs, insurance, key contracts, financials | This node (entity hygiene + contracts filing) + `sales-contracting-legal` (instruments) | Continuous; snapshot per raise |
| **Unit economics** | Per-node cost-to-serve (BOM + deployment labor + support cost) vs. revenue; gross margin per node | This node (deployment cost tracking + bookkeeping) + **instrumentation (C, support-hrs/node)** | Quarterly |
| **Support-load evidence** | Support hrs/node, L1-absorb vs L2-engineering ratio, time-to-resolve trend | **Instrumentation (C)** ← fed by this node's **issue-log** (`support_minutes`/`engineering_minutes` from `GAP-COF-SUPPORT-TRIAGE`) | Quarterly |
| **Renewal data** | Renewal-intent capture, renewal signals, retention | **Instrumentation (C, renewal-intent)** ← fed by Node Care quarterly check-in `renewal_signal` + Day-60 review | Per check-in cycle |
| **Channel plan** | Partner channels (ag/municipal/co-op/arts), reference case studies (with written permission), segment campaigns, pipeline | Founder (§2 After Acceleration) + `sales-contracting-legal` pipeline | Per raise |
| **Claims register linkage** | Every external/investor claim mapped to its evidence category | **Claims register (C, row 59)** — authoritative; packet cites, does not restate | Continuous (C-owned) |

**Cross-node hand-off seam (the unresolved residue, now specified):**
- The **claims register (Workstream C, Victor)** is the authoritative map of claim → evidence category. The validation packet **references** register entries by handle; it must not assert any external claim that lacks a register entry. (Mirrors Law 1: every claim traces to its source.)
- **Instrumentation (Workstream C, Victor)** is the authoritative metrics store (support-hrs/node, usage, baselines, renewal-intent). The packet's unit-economics / support-load / renewal sections **pull from instrumentation**; this node *feeds raw inputs* (issue-log effort minutes, Node Care renewal signals, deployment cost) into instrumentation but does not compute the published metrics.
- **Direction of flow:** `company-operations-finance` (raw ops data: cost, support minutes, renewal signals) → `quality-security-proof` (instrumentation + claims register: measured, claim-mapped) → `company-operations-finance` (validation packet: assembled, cited). The packet is the consumer at the end of that chain.
- **Coordination owner:** Josh (packet assembly) + Victor (evidence production). Seam is a coordinate-treatment, not a merge — neither node owns the other's artifacts.

### Plan (first steps)
1. Author the packet skeleton (six sections above) as a living document with per-section evidence-source pointers (no fabricated data — sections empty until instrumentation produces real numbers).
2. Confirm with Victor the claims-register handle format and instrumentation field names so packet sections can cite them (cross-node coordination task — flag for the `quality-security-proof` node's spec to expose these).
3. Wire the issue-log effort fields + Node Care renewal signals as named inputs to instrumentation (define the input contract; C owns the store).
4. Set the maintenance cadence (quarterly refresh; full snapshot per raise).

### Acceptance criteria
- [ ] Packet skeleton enumerates all five §2 sections (data room, unit economics, support-load, renewal data, channel plan) + claims-register linkage.
- [ ] Each section names its evidence source and producing node; cross-node-sourced sections are marked as consuming C's instrumentation/claims register.
- [ ] The hand-off seam (raw ops data → C instrumentation/claims → packet) is documented with direction of flow and coordinate-ownership (no artifact merge).
- [ ] No packet claim exists without a claims-register entry (Law 1 alignment); no fabricated/placeholder metrics presented as real.
- [ ] Maintenance cadence defined (quarterly + per-raise snapshot).
- [ ] **Cross-node dependency flagged for `quality-security-proof` BUILD-SPEC:** that node must expose claims-register handles + instrumentation field names this packet consumes.

---

## Residue & Cross-Node Flags

- **EXT-COF-01 / EXT-COF-02** (deferred external research, awaiting Josh): generic bookkeeping-cadence reference (hardens ENTITY-HYGIENE) and generic support-tiering pattern (hardens SUPPORT-TRIAGE). Both pattern-level, no protected data. This spec is authorable without them; they are optional hardening, not blockers.
- **Cross-node dependency (open):** `GAP-COF-VALIDATION-PACKET` depends on `quality-security-proof` exposing claims-register handles + instrumentation field names. Flagged here; must be picked up in that node's BUILD-SPEC.
- **Staffing triggers (encoded, not decided):** Bookkeeper → first revenue; Customer Success → deployments stack. Specs are dormant-ready handoff packages until triggers fire.
- **Owner-boundary:** this spec is planning/authoring only. It does not claim Task Session / Sigil / Inventory / Ontology authority and executes no runtime stage. Client orgs under `orgs/` untouched (Law 3).
