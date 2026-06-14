# Research Result - Sales, Contracting, and Legal

- Dispatch ID: `gq-research-strategy-sales-contracting-legal-2026-06-12`
- Run: `2026-06-12-craft-pipeline-hydration`
- Mode: LOCAL-FIRST research execution (r01-r06)
- Date: 2026-06-12
- Overall verdict: **PASS (local-first baseline complete; external research DEFERRED, bounded requests named)**

## Node

- Craft node: `sales-contracting-legal`
- Owns: workbook **Workstream E. Selling & Contracting** (4 task rows) plus the **Legal (fractional)** and **Bookkeeper (fractional)** role rows from the Role Map.
- Sibling boundary (NOT this node): Workstream F (white-glove-delivery-node-care), Workstream G (company-operations-finance), Workstream C external Security Reviewer (quality-security-proof). Entity hygiene / banking / insurance-as-operating-floor live in Workstream G; this node covers insurance **only** as a customer-agreement / first-LOI dependency.

## Core Question

What legal, sales, qualification, disclosure, insurance, deposit, and invoicing evidence is needed before the first LOI or customer agreement?

## Findings (with source paths)

All findings drawn from Golden Quill PROJECT evidence only (rg04 satisfied; no orgs/ PROJECT_CONTEXT read).

- **F1 — Workstream E has exactly four tasks, two onboard-now-critical.** Sales materials (one-pager, demo, segment framing, pipeline tracker **w/ disclosure rules**) and Qualification (readiness checklist, org-fluency test, fit/no-fit referral) are Founder-owned; Customer agreement + LOI + data-policy + procurement + insurance is "Legal (fractional) + Founder, Onboard NOW"; Deposit/invoicing/cost-tracking is "Bookkeeper (fractional), Onboard at first revenue." Source: `docs/golden-quill-task-role-breakdown-handoff.md` rows 66-69.
- **F2 — Legal scope is pre-named in the Role Map and is the gating dependency.** Legal (fractional) "Carries: Customer agreement, LOI, data-policy terms, procurement language, **FERPA / AI-transparency reading**" with trigger "Fractional, **before first LOI signs**." This is the only role whose onboard trigger is explicitly tied to the first LOI. Source: `docs/golden-quill-task-role-breakdown-handoff.md` row 114.
- **F3 — Bookkeeper scope and trigger are pre-named.** Bookkeeper (fractional) "Carries: Deposits, invoicing, cost tracking, investor schedules," trigger "Few hrs/month **at first revenue**." Deposit/invoicing is therefore first-revenue-gated, not first-LOI-gated — a sequencing distinction the research must preserve. Source: `docs/golden-quill-task-role-breakdown-handoff.md` rows 69, 116.
- **F4 — Disclosure rules are a load-bearing, under-specified term.** The workbook attaches "w/ disclosure rules" to the sales/pipeline-tracker task (row 66) but does not define them. Disclosure here plausibly couples to the sovereignty/posture promise (what is claimed about data handling during sales). This is local-evidence-thin and is the core of `GAP-SCL-SALES-MATERIALS`. Source: `docs/golden-quill-task-role-breakdown-handoff.md` row 66 + claims-register dependency (Workstream C, row 59, owned by quality-security-proof node — cross-node, not pulled here beyond noting the dependency).
- **F5 — Data-policy spec must align to the locked posture model + sovereignty promise.** Customer-facing data-policy terms (row 68) cannot be drafted free-hand; they must reflect the locked BYOK-only + classification (public/shareable/confidential/operator_flagged) + three-posture routing model and the Sovereignty Promise ("data stays local by default; nothing held hostage"). Source: CLAUDE.md "Beta Model Strategy" + "Sovereignty Promise" sections (Golden Quill project canon). This bounds — but does not itself supply — the contract language.
- **F6 — "Skills to weigh later" pre-flags two legal-adjacent external needs.** The Role Map lists "public-procurement fluency" and "privacy/compliance counsel" as skills to fold in later. Both are this node's downstream legal-research surface (procurement notes; FERPA/privacy). Source: `docs/golden-quill-task-role-breakdown-handoff.md` row 117.
- **F7 — Three active gaps map cleanly to the core question's clauses.** `GAP-SCL-SALES-MATERIALS` (flag) = sales/disclosure clause; `GAP-SCL-LEGAL-FIRST-LOI` (block) = legal/LOI/data-policy/procurement/insurance clause; `GAP-SCL-DEPOSIT-INVOICING` (flag) = deposit/invoicing clause. The qualification clause has no dedicated gap — it is Founder-owned and substance-ready, not research-blocked. Source: `.craft/ledger.yml` gaps[0-2].

## Lane Map (per gap)

| Gap | Severity | Local lane (do first) | Local evidence sufficiency | External lane (gap-triggered, DEFERRED) |
| --- | --- | --- | --- | --- |
| GAP-SCL-SALES-MATERIALS | flag | Derive disclosure rules from sovereignty promise + posture canon; cross-link claims register (Workstream C dependency). | Partial — frame exists locally; disclosure-rule wording needs Josh's business judgment (r01 stop-condition). | Competitor/peer one-pager + disclosure-language patterns (comparison only). |
| GAP-SCL-LEGAL-FIRST-LOI | **block** | Assemble the local requirement list (LOI fields, data-policy terms anchored to posture model, procurement notes, insurance-as-LOI-dependency, FERPA/AI-transparency reading scope). | Insufficient for execution — local evidence names *what is needed* but contains **no template, benchmark, or statutory text**. This is a classic external-gap. | Fractional-legal scope norms; AI/data-policy clause patterns; FERPA/AI-transparency checklist; procurement + insurance checklist references. **All require Josh approval + retained fractional counsel — research informs, counsel drafts.** |
| GAP-SCL-DEPOSIT-INVOICING | flag | Define deposit-handling + invoicing + cost-tracking requirements; mark first-revenue trigger (not first-LOI). | Partial — requirements derivable locally; mechanics need bookkeeper. | Deposit/escrow norms + invoicing-cadence benchmarks (comparison only; bookkeeper owns execution). |

## External-Research Decision (rg03 / r04)

**DECISION: DEFERRED.** No external research executed. Selected route per dispatch = `gap_triggered_external`, which requires a named local-evidence gap **and** Josh's explicit approval before any external pass. Approval is NOT present in this run, so all external lanes stay gated. Legal templates/benchmarks are explicitly a record-not-fetch item per the dispatch hard rules.

Bounded external requests (named, awaiting Josh's go/no-go — one or more may be approved independently):

1. **EXT-SCL-LEGAL-CLAUSE-PATTERNS** (for GAP-SCL-LEGAL-FIRST-LOI, **block**) — bounded comparison of AI/data-policy contract clause patterns + fractional-legal engagement scope norms. Protected-context flag: no client/applicant data leaves local; comparison is on generic clause structure only. Best paired with retained fractional counsel (counsel drafts; research only frames).
2. **EXT-SCL-FERPA-AITRANSPARENCY-CHECKLIST** (for GAP-SCL-LEGAL-FIRST-LOI, **block**) — bounded checklist references for FERPA + AI-transparency obligations relevant to Educator-segment customers. Counsel-confirm required; research is orientation only.
3. **EXT-SCL-PROCUREMENT-INSURANCE-REFS** (for GAP-SCL-LEGAL-FIRST-LOI, **block**) — public-procurement language references + insurance-requirement checklists customers may impose at LOI. Comparison only.
4. **EXT-SCL-DISCLOSURE-LANGUAGE-PATTERNS** (for GAP-SCL-SALES-MATERIALS, flag) — peer disclosure-rule / sovereignty-claim language patterns for sales materials. Must reconcile to local claims register before any use.
5. **EXT-SCL-DEPOSIT-INVOICING-NORMS** (for GAP-SCL-DEPOSIT-INVOICING, flag) — deposit/escrow + invoicing-cadence norms for hardware+service deployments. Bookkeeper owns execution; research is comparison only.

## Residue

- **R1 (owner-input required):** Disclosure-rule wording and any LOI commercial terms need Josh's business judgment (r01 stop-condition) — cannot be resolved by research alone.
- **R2 (cross-node dependency, not pulled):** Sales-material claims depend on the Claims Register owned by the quality-security-proof node (Workstream C). Insurance-as-operating-floor + entity hygiene live in company-operations-finance (Workstream G). This node touches insurance only as an LOI dependency; the operating-floor view stays with G. Flagged, not read.
- **R3 (sequencing):** Deposit/invoicing is first-**revenue**-gated; legal/LOI is first-**LOI**-gated. Research and any onboarding must not collapse these into one trigger.
- **R4 (authority limit):** The block-severity legal gap is not closable by research — it closes when a fractional counsel is retained. Research can de-risk and scope, not substitute.

## Next Move

Single next move: **surface the five bounded external requests to Josh for go/no-go**, with EXT-SCL-LEGAL-CLAUSE-PATTERNS + the retain-fractional-counsel decision prioritized (block-severity gap). On approval, execute the approved external lane(s) under protected-context flags and feed results into the node's Refine route (`REFINE-DISPATCH.json`) toward Invoke first-artifact direction. No ledger mutation in this run (rg06).

## Files Written

- `docs/strategy/development/sales-contracting-legal/development/refinement-runs/2026-06-12-craft-pipeline-hydration/RESEARCH-RESULT.md`
- `docs/strategy/development/sales-contracting-legal/development/refinement-runs/2026-06-12-craft-pipeline-hydration/research-validation-ledger.md`
