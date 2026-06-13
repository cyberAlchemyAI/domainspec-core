# BUILD-SPEC — Sales, Contracting & Legal (Golden Quill Node)

- Node: `sales-contracting-legal`
- Owns: workbook **Workstream E. Selling & Contracting** (4 task rows) + Role Map rows **Legal (fractional)** and **Bookkeeper (fractional)**.
- Status: **Refine→Invoke authored**. Planning/spec only — no runtime stages executed, no binding legal language authored.
- Date: 2026-06-13
- Source-of-truth inputs:
  - `docs/strategy/development/sales-contracting-legal/development/refinement-runs/2026-06-12-craft-pipeline-hydration/RESEARCH-RESULT.md`
  - `docs/strategy/development/sales-contracting-legal/.craft/ledger.yml`
  - `docs/strategy/development/sales-contracting-legal/development/refinement-runs/2026-06-12-craft-pipeline-hydration/REFINE-DISPATCH.json`
  - `docs/golden-quill-task-role-breakdown-handoff.md` (Workstream E rows 66–69; Role Map rows 114, 116, 117)
  - `CLAUDE.md` — BYOK/posture/sovereignty canon, FIT Farms entity naming

## Scope & Guardrails (binding on everything below)

- **Customer-facing label = "FIT Farms" (plain).** Internal file-naming uses "FIT Farms Commons" (owner role) / "FIT Farms LLC" (`orgs/` client role); neither appears in customer-facing copy.
- **No binding legal language authored here.** Fractional Legal counsel owns clause wording. This spec defines *structure, required terms, and the alignment constraints* counsel must satisfy — never the clauses themselves.
- **Law 3 (Org Isolation).** This spec reads no `orgs/` PROJECT_CONTEXT. Sales templates are org-agnostic skeletons; per-customer instances live in white-glove delivery (Workstream F), not here.
- **Every external sales claim traces to the Claims Register** owned by the `quality-security-proof` node (Workstream C, handoff row 59 — QA/Measurement/Victor, "every external claim mapped to its evidence category"). The Claims Register is a cross-node dependency. This node MUST NOT assert a capability/security/sovereignty claim that is not registered there.
- **Sequencing (RESEARCH-RESULT R3):** Legal/LOI work is **first-LOI-gated**; Deposit/invoicing is **first-revenue-gated**. Do not collapse the two triggers.
- **Authority limit (R4):** the block-severity legal gap closes only when fractional counsel is retained. This spec de-risks and scopes; it does not substitute for counsel.

---

## GAP-SCL-SALES-MATERIALS — Sales Materials Structure (REFINE-SOLVABLE, owner: Josh)

Severity: flag. Treatment: coordinate. Founder-owned, substance-ready, not research-blocked. **Authored to Define→Design→Plan + acceptance criteria below.**

### Define

Produce the *structure and templates* (not finished customer copy) for four sales artifacts so Josh can populate them with business judgment:
1. One-pager outline
2. Demo script shell
3. Segment-framing template
4. Pipeline-tracker schema (with disclosure rules)

Load-bearing constraint surfaced in research (F4): the workbook attaches "w/ disclosure rules" to the pipeline-tracker/sales task but never defines them. Disclosure rules couple to the sovereignty/posture promise (what is *claimed* about data handling during sales). Every claim slot in every template carries an explicit **Claims-Register dependency marker** — `[CLAIM-REF: <quality-security-proof claims-register id> | UNREGISTERED-BLOCK]`. A claim with no register id is `UNREGISTERED-BLOCK` and may not ship in customer-facing material.

### Design — Template Structures

**1. One-pager outline** (org-agnostic skeleton; "FIT Farms" plain throughout)
- Header: product name + one-line positioning ("Golden Quill — regenerative grant intelligence"; vendor = "FIT Farms").
- Problem frame (1 short block).
- What it is: the physical node (128 GB desktop appliance) + Tilth software + Cultivator phone interface — described in benefit terms, each capability claim carrying `[CLAIM-REF]`.
- Sovereignty/ownership statement block (data stays local by default; BYOK; nothing held hostage) — every sentence `[CLAIM-REF]`-marked against the Claims Register; mirrors the Sovereignty Promise canon, never exceeds it.
- Who it's for: the six Customer Identity Categories named as "worlds we serve" (Food Systems, Educator, Public Agency, Arts & Culture, Cooperative, Ecosystem Intermediary).
- Disclosure footer (see Disclosure Rules below).
- CTA + contact.

**2. Demo script shell** (sequence-of-beats skeleton, no scripted prose)
- Beat 0 — Framing: what the prospect will see and what it proves.
- Beat 1 — Live Scout population sequence. MUST reference the **Canonical demo standard** owned by quality-security-proof (handoff row 60: "live, never staged-as-live"). Demo script inherits that node's standard; this shell only sequences it. Marker: `[DEMO-STD-REF: quality-security-proof canonical-demo-standard]`.
- Beat 2 — Posture/sovereignty walkthrough (what data leaves the node, what never does) — claims `[CLAIM-REF]`-marked.
- Beat 3 — One council/drafting slice (benefit, not internals).
- Beat 4 — Ownership/export close ("if FIT Farms disappeared tomorrow, you keep machine, data, keys, grants").
- Each beat: {what operator does · what prospect sees · the claim it evidences · its CLAIM-REF}.

**3. Segment-framing template** (one fillable card per Customer Identity Category)
- Fields: Segment name (CIC label) · Operating reality (one line) · The funding-grammar pain · How Tilth configures (Search Vocabulary · Evidence Schema · Language Register · Reporting Rhythm — the four applicant-side primitives) · Proof points (each `[CLAIM-REF]`) · Fit signals · No-fit signals (feeds the Qualification fit/no-fit referral, row 67).
- Constraint: NO CIC→CLC coupling asserted (F-CIC-CLC-COUPLING-VIOLATION canon). Capital-logic activation is opportunity-driven, never pre-mapped per segment.

**4. Pipeline-tracker schema** (org-agnostic field list, not a populated tracker)
- Per-prospect row fields: `prospect_id` · `segment` (CIC) · `stage` (lead / qualified / demo / LOI-sent / LOI-signed / deployed) · `qualification_status` (links Qualification checklist, row 67) · `fit_verdict` (fit / no-fit / referred) · `disclosure_version_shown` (which disclosure-rules version the prospect saw) · `claims_version_shown` (Claims-Register version current at contact) · `next_action` · `owner` · `posture_discussed` (which deployment posture the prospect leans toward — feeds white-glove Classification Review).
- **Disclosure-rules sub-block** (the load-bearing F4 item): a small fixed ruleset, version-stamped, recording (a) what data-handling/sovereignty claims may be stated in sales contact, (b) that each maps to a Claims-Register id, (c) that no claim exceeds the locked posture/BYOK/sovereignty canon, (d) the rule that any unregistered claim is suppressed. Disclosure rules are *constraints on what salespeople may say* — wording of the claims themselves still traces to the register.

### Plan (owner: Josh; ordering)
1. Confirm Claims-Register id scheme with quality-security-proof node owner (cross-node coordination; do not invent ids).
2. Draft the four skeletons above as fillable templates (structure only).
3. Populate claim slots — each must resolve to a registered id or be marked `UNREGISTERED-BLOCK`.
4. Author disclosure-rules v1 block; version-stamp it.
5. Wire demo shell Beat 1 to the canonical demo standard; do not duplicate that standard here.

### Acceptance Criteria
- AC-1: All four template structures exist as fillable skeletons (not finished copy). PASS = each artifact present with all fields above.
- AC-2: Every claim slot in one-pager + demo + segment cards carries a `[CLAIM-REF]` marker; zero unmarked claims. PASS = grep finds no claim sentence without a marker.
- AC-3: No customer-facing string uses "FIT Farms Commons", "FIT Farms LLC", "Sovereign Node", "Tilth"-as-vendor, or "MaatAI". Vendor = "FIT Farms" plain. (Tilth/Cultivator/Golden Quill may name the *product*.)
- AC-4: No segment card asserts a fixed CIC→CLC mapping.
- AC-5: Pipeline-tracker schema includes `disclosure_version_shown` + `claims_version_shown` fields and a version-stamped disclosure-rules sub-block.
- AC-6: Demo Beat 1 references (does not redefine) the quality-security-proof canonical demo standard.
- AC-7: Sovereignty/posture claims do not exceed the locked BYOK + three-posture + "data local by default" canon.

**Verdict: REFINE-SOLVABLE — Define→Design→Plan + acceptance criteria AUTHORED. Owner Josh. Hard dependency on quality-security-proof Claims Register (claim ids) + canonical demo standard.**

---

## GAP-SCL-LEGAL-FIRST-LOI — Legal / First-LOI (OPERATOR-INPUT, counsel-gated)

Severity: **block**. Treatment: onboard. Owner: founder-legal. **Gated on retaining fractional Legal counsel before first LOI signs (handoff row 114).** No clause language authored here. This section specs *what counsel must produce* and *the alignment constraints* — the structural requirement list, not the legal text.

### Required artifacts (counsel owns wording)
Per handoff row 68 + Role Map row 114, counsel carries: customer agreement, LOI template, data-policy terms, procurement language, FERPA / AI-transparency reading.

1. **Customer agreement** — scope, ownership of hardware/data/keys, deliverables, term, termination/export. COUNSEL DRAFTS.
2. **LOI template** — field skeleton only (commercial terms = Josh business judgment; legal form = counsel). Fields to scope: parties (vendor = "FIT Farms"), node/spec, deployment posture selected, deposit terms (links GAP-SCL-DEPOSIT-INVOICING), timeline, conditions precedent (incl. insurance — see below), signature. COUNSEL CONFIRMS FORM.
3. **Data-policy spec** — see alignment constraints below. COUNSEL DRAFTS clause language; this spec supplies the must-align terms.
4. **Procurement notes** — references for public-procurement-buyer requirements (Public Agency / Educator segments). COUNSEL + public-procurement fluency skill (Role Map row 117 "skills to weigh later"). COUNSEL DRAFTS.
5. **Insurance** — scoped here ONLY as a customer-agreement / first-LOI dependency (insurance-as-operating-floor lives in `company-operations-finance`/Workstream G — RESEARCH-RESULT R2). What customers may require at LOI; conditions-precedent. COUNSEL + Workstream G coordinate.
6. **FERPA / AI-transparency reading** — obligation checklist for Educator-segment + AI-disclosure duties. COUNSEL CONFIRMS; research is orientation only.

### Data-policy alignment constraints (this node CAN spec; counsel turns into clauses)
The data-policy terms MUST align to locked canon (RESEARCH-RESULT F5) and may not contradict it. The data-policy must express, in counsel's language:
- **BYOK only.** Customer's own API keys; no managed/metered billing posture.
- **Classification model.** Four field classes — public / shareable / confidential / operator_flagged — govern handling.
- **Three-posture routing.** Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign; confidential + operator_flagged never leave the node; only public/shareable may take approved cloud routes (and only under the customer's selected posture).
- **Sovereignty Promise.** Runs on hardware the customer owns; data local by default; keys belong to the customer; full export; "nothing held hostage" — if FIT Farms disappeared, customer keeps machine/data/keys/grants.
- **Audit posture.** Approved cloud routes are logged (audit-log canon).
- **Posture selection is operator-signed** at white-glove Classification Review (cross-ref Workstream F).

These constraints bound the contract; they are NOT the contract. Counsel writes enforceable terms consistent with them.

### Acceptance Criteria (gate, not authored output)
- AC-L1: Fractional Legal counsel retained and engagement scope confirmed BEFORE any LOI is signed. PASS = counsel engaged; gate is binary.
- AC-L2: Data-policy clauses, when drafted, contain no term contradicting the BYOK / classification / three-posture / sovereignty canon above. PASS = counsel-drafted policy reviewed against this constraint list, zero conflicts.
- AC-L3: LOI conditions-precedent name the insurance requirement and cross-reference Workstream G (operating-floor owner).
- AC-L4: FERPA / AI-transparency checklist confirmed by counsel for Educator-segment deployments.
- AC-L5: Vendor party named "FIT Farms" plain in all customer-facing instruments.

**Verdict: COUNSEL-GATED BLOCK — requirement list + data-policy alignment constraints + acceptance gates SPEC'D. No legal clause language authored (counsel owns). Closes on counsel retention. Owner: Josh.**

Bounded external-research requests already named (DEFERRED, await Josh go/no-go — RESEARCH-RESULT): EXT-SCL-LEGAL-CLAUSE-PATTERNS, EXT-SCL-FERPA-AITRANSPARENCY-CHECKLIST, EXT-SCL-PROCUREMENT-INSURANCE-REFS. All protected-context: no client data leaves local; comparison on generic clause structure only; counsel drafts, research only frames.

---

## GAP-SCL-DEPOSIT-INVOICING — Deposit / Invoicing / Cost-Tracking (OPERATOR-INPUT, bookkeeper-gated)

Severity: flag. Treatment: plan. Owner: bookkeeping. **Gated on retaining Bookkeeper (fractional) at first revenue (handoff row 116) — first-REVENUE-gated, not first-LOI-gated (RESEARCH-RESULT R3).** Requirements derivable locally; mechanics owned by bookkeeper.

### Requirements to spec (bookkeeper executes)
Per handoff row 69 + Role Map row 116, Bookkeeper carries deposits, invoicing, cost tracking, investor schedules.
1. **Deposit handling** — deposit-at-LOI requirement (the term lives in the LOI, owned by GAP-SCL-LEGAL-FIRST-LOI; the *handling/accounting* is bookkeeper's). Define: deposit trigger, holding, application-to-invoice, refund posture.
2. **Invoicing** — cadence + milestones (deposit → deployment → close) mapped to deployment lifecycle; per-node (PER-NODE effort type).
3. **Deployment cost tracking** — per-node cost capture (hardware BOM from Workstream A, install labor from Workstream F) feeding unit economics. Coordinates with Workstream G company-operations-finance (bookkeeping/banking operating floor) — this node owns the per-deal/per-node view, not the company books.

### Acceptance Criteria
- AC-D1: Bookkeeper engaged at first revenue (binary gate; NOT before — do not pull this trigger to first-LOI).
- AC-D2: Deposit terms appear in the LOI (cross-ref GAP-SCL-LEGAL-FIRST-LOI); deposit *accounting* defined by bookkeeper.
- AC-D3: Invoicing cadence mapped to deployment milestones.
- AC-D4: Per-node cost-tracking schema feeds unit economics; coordinates with Workstream G without duplicating company books.

**Verdict: BOOKKEEPER-GATED FLAG — requirements + sequencing + acceptance criteria SPEC'D. Mechanics owned by Bookkeeper, engaged at first revenue. Owner: Josh.**

Bounded external request named (DEFERRED): EXT-SCL-DEPOSIT-INVOICING-NORMS (deposit/escrow + invoicing-cadence norms; comparison only; bookkeeper owns execution).

---

## Cross-Node Dependencies (register, do not pull)
- **quality-security-proof** — Claims Register (claim ids; handoff row 59) + Canonical demo standard (row 60). HARD dependency for GAP-SCL-SALES-MATERIALS. Not authored here.
- **company-operations-finance (Workstream G)** — insurance-as-operating-floor, entity hygiene, company books. This node touches insurance only as an LOI dependency.
- **white-glove-delivery-node-care (Workstream F)** — per-customer instances, Classification Review / posture sign-off, deployment lifecycle that invoicing milestones map to.

## Residue Carried Forward
- R1: Disclosure-rule wording + LOI commercial terms need Josh's business judgment — not resolvable by spec alone.
- R2: Sales claims depend on a Claims Register not yet authored by quality-security-proof; claim ids are placeholders until that node lands.
- R4: Block-severity legal gap closes only on counsel retention.
