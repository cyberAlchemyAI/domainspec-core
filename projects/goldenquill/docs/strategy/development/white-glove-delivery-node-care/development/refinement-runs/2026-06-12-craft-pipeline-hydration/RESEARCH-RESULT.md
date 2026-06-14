# Research Result — White-Glove Delivery and Node Care

- **Dispatch ID:** `gq-research-strategy-white-glove-delivery-node-care-2026-06-12`
- **Run:** `2026-06-12-craft-pipeline-hydration`
- **Mode:** research (LOCAL-FIRST executed; external DEFERRED)
- **Craft node:** `white-glove-delivery-node-care`
- **Lenses applied:** local-evidence-reviewer (r01–r02) · external-boundary-reviewer (r03–r04) · claim-validation-reviewer (r05–r06)

## Core Question

What delivery, onboarding, training, vault build, source universe, first packet, support, and Day 60 evidence turns first installs into a repeatable service?

## r01 — Scope

This node owns **workbook Workstream F (White-Glove Delivery, every customer)** plus the **Node Care** handoff into operations (Workstream G's Node Care / support rows where they touch delivery). Scope boundary holds against siblings:

- **In scope:** pre-deployment questionnaire, Day 0 install closeout, vault build, source universe + first Scout scan, first opportunity packet, training sessions 2–4, support loop, Day 60 use review, and the founder-led → Customer Success + Field Tech repeatability transition.
- **Out of scope (sibling-owned, do not author here):** Golden Image / imaging mechanics (`hardware-golden-image`); posture/classification *engine* build (`quality-security-proof` + locked architecture); CS/Field-Tech *hiring* triggers and budget (`staffing-budget-and-triggers` — this node only consumes the handoff trigger); contracting/LOI (`sales-contracting-legal`); entity/banking ops (`company-operations-finance`); volume-repeatability hardening curriculum (`after-acceleration-roadmap`).
- No cross-node drift detected. No client `orgs/` PROJECT_CONTEXT read (rg04 / Law 3 honored).

The node scope separates cleanly; no item required Josh's business judgment to *scope* (stop-conditions clear). Business-judgment items surface only inside the gaps below.

## r02 — Local Evidence Baseline (cited)

| Evidence handle | Source path | What it grounds |
|---|---|---|
| Workbook Workstream F rows (7 PER-NODE delivery tasks) | `docs/golden-quill-task-role-breakdown-handoff.md` (rows 70–76) | The seven delivery stages: pre-deployment, Day 0 install, vault build, source universe, first packet, first-draft+training, Day 60 review |
| Workbook Workstream G Node Care + support rows | `docs/golden-quill-task-role-breakdown-handoff.md` (rows 78–79) | Support channel + triage rules; Node Care delivery (updates, source-index maintenance, quarterly check-ins, vault care) |
| Workbook "After Acceleration" Repeatability row | `docs/golden-quill-task-role-breakdown-handoff.md` (row 90) | Target end-state: non-founder runs install end-to-end; training curriculum standardized |
| Workbook Roles & Gaps (CS, Field Tech, QA) | `docs/golden-quill-task-role-breakdown-handoff.md` (rows 110–112) | Who carries delivery; "Josh absorbs first nodes → part-time contract as deployments stack" |
| v0.1 Beta white-glove playbook | `docs/white_glove_v0_1_beta.md` | Existing canonical procedure: pre-arrival checklist, BULK_INGEST, Classification Review + posture selection, first cycle dispatch, AWARD_INGEST, INCREMENTAL_INGEST, failure-recovery table |
| Craft ledger gaps + descriptions | `.craft/ledger.yml` (gaps[0–2], DESC-WGD-001) | Three active gaps; founder-led → CS/Field-Tech repeatability framing |
| Project posture / sovereignty / classification doctrine | `CLAUDE.md` (Beta Model Strategy; Sovereignty Promise; v0.1 Beta Deployment Posture) | Three-posture model, classification register, F-CLASS gates that the delivery procedure must enforce |

**Dedup note:** `docs/white_glove_v0_1_beta.md` already substantially covers GAP-WGD-PLAYBOOK's *technical* spine (pre-arrival → BULK_INGEST → Classification Review → first cycle → AWARD_INGEST). The remaining playbook gap is the **delivery-service wrapper** around it (document-request kit, onboarding questionnaire, posture conversation script, deployment record, branded closeout, training-session curriculum, missing-doc list), which the workbook names but the v0.1 playbook does not flesh out. This is a *delta* gap, not a from-scratch gap.

## Findings (line → source)

1. The seven delivery stages and their PER-NODE/role assignments already exist as workbook rows — delivery is specified at task granularity, not yet as a runnable playbook. — `docs/golden-quill-task-role-breakdown-handoff.md` rows 70–76
2. The *technical* onboarding spine (BULK_INGEST → Classification Review → posture selection → first cycle → AWARD_INGEST) is already a locked, written procedure; the playbook gap is the human-facing service wrapper, not the engine. — `docs/white_glove_v0_1_beta.md` §§1–4
3. Delivery is explicitly founder-led first and must become a CS + Field-Tech repeatable process — the central tension this node exists to resolve. — `.craft/ledger.yml` DESC-WGD-001; `docs/golden-quill-task-role-breakdown-handoff.md` row 111
4. The CS/Field-Tech *handoff trigger* (when Josh stops doing installs) is owned by `staffing-budget-and-triggers`; this node only needs the trigger + a checklist a trained non-founder can execute. — `.craft/ledger.yml` gaps[1] (GAP-WGD-CS-HANDOFF, owner `staffing-budget-and-triggers`); `docs/golden-quill-task-role-breakdown-handoff.md` rows 90, 111–112
5. Day 60 review needs four named outputs — metrics, support-load evidence, renewal signal, next-cycle plan — and those metrics are QA-instrumentation-sourced (Workstream C "support hrs/node, usage metrics, baselines, renewal-intent capture"). — `.craft/ledger.yml` gaps[2] (GAP-WGD-DAY60); `docs/golden-quill-task-role-breakdown-handoff.md` rows 61, 76
6. Node Care (updates, source-index maintenance, quarterly check-ins, vault care) is the *ongoing* tail of delivery and ties to the update-and-signing mechanism + classification re-review (INCREMENTAL_INGEST defaults new facts to confidential). — `docs/golden-quill-task-role-breakdown-handoff.md` rows 41, 79; `docs/white_glove_v0_1_beta.md` §5
7. The sovereignty promise (operator owns hardware/keys/data; classification-gated cloud routing) is the non-negotiable acceptance criterion every delivery artifact must preserve and demonstrate at the test cycle. — `CLAUDE.md` Sovereignty Promise; `docs/white_glove_v0_1_beta.md` §§2.3, 7

## r03 — Research Lane Map (per gap)

Route menu selection from dispatch: **`gap_triggered_external`** (local-first; external only on named gap + approval).

| Gap | Severity | Lane decision | Local coverage | Residual external need |
|---|---|---|---|---|
| **GAP-WGD-PLAYBOOK** — repeatable delivery playbook, pre-deployment → training | block | **LOCAL-FIRST sufficient to author the delta.** Synthesize workbook rows 70–76 + 90 into a stage-by-stage playbook wrapping the existing `white_glove_v0_1_beta.md` spine. | Workbook F rows + v0.1 playbook + ledger | OPTIONAL external comparison: customer-success onboarding playbook patterns for sovereign/regulated hardware deployments — *to benchmark stage structure, not to author it*. DEFERRED. |
| **GAP-WGD-CS-HANDOFF** — CS/Field-Tech transition trigger + checklist training | flag | **LOCAL + COORDINATE.** Trigger/budget owned by `staffing-budget-and-triggers`; this node authors the *executable checklist* a trained non-founder follows. | Roles & Gaps rows 111–112; row 90; ledger gaps[1] | OPTIONAL external: field-tech install-checklist / runbook handoff templates. DEFERRED. |
| **GAP-WGD-DAY60** — Day 60 metrics, support-load, renewal signal, next-cycle plan | flag | **LOCAL + COORDINATE with QA.** Metric definitions sourced from Workstream C instrumentation (row 61); this node authors the *review structure* and renewal-signal capture shape. | Rows 61, 76; ledger gaps[2] | OPTIONAL external: post-deployment QBR / health-score and renewal-intent survey patterns. DEFERRED. |

## r04 — External Approval Gate (DEFERRED)

**Decision: DEFERRED. No external research executed.** Per rg03, external research requires a named local gap AND Josh's explicit approval (`requires_user_permission`). Local evidence is sufficient to author all three gap treatments at delta granularity; external passes are *enhancement-only* benchmarking, not blockers. Protected-context flag: none of the bounded requests below carry Golden Quill confidential data — they are generic-industry pattern lookups.

**Bounded external requests (each fires only on explicit Josh approval):**

1. **EXT-WGD-01** — Customer-success white-glove onboarding playbook patterns for sovereign / on-prem / regulated-hardware deployments (stage structure, document-request kits, branded closeout norms). Bounds: industry pattern survey only; no client data egress. Serves GAP-WGD-PLAYBOOK.
2. **EXT-WGD-02** — Field-tech install runbook / checklist-handoff templates enabling a non-author to run an install end-to-end. Bounds: template/format survey only. Serves GAP-WGD-CS-HANDOFF.
3. **EXT-WGD-03** — Post-deployment Day-60 QBR / health-score / renewal-intent capture patterns (B2B SaaS + hardware). Bounds: metric-design and survey-shape patterns only; no benchmark-number claims imported as fact. Serves GAP-WGD-DAY60.

All three are **optional comparison passes** — the node can reach a runnable playbook without them. They sharpen, not unblock.

## r05 — Claim-Evidence Validation

See `research-validation-ledger.md` for the full claim → source → validation table. Overall verdict: **PASS** — every claim maps to a local Golden Quill source class + concrete path; no claim depends on un-approved external research; owner-boundary respected on all three gaps.

## Residue

- The v0.1 playbook (`white_glove_v0_1_beta.md`) uses the older four-posture "Sanitized" vocabulary in one workbook row (`docs/golden-quill-task-role-breakdown-handoff.md` row 50: "Unrestricted / Hybrid / Sanitized / Sovereign") — superseded by the three-posture model (`CLAUDE.md` v7.0.10). Not this node's artifact to mutate (owner boundary); flag for the canon/quality node.
- Day 60 metric *definitions* are a hard dependency on Workstream C instrumentation (`quality-security-proof` node) — this node cannot finalize Day 60 review numbers without that node's metric schema. Coordinate, do not author.
- CS/Field-Tech handoff *trigger threshold* (deployed-node count) is a `staffing-budget-and-triggers` decision still open — this node's checklist is trigger-agnostic until that lands.

## Next Move

Hand off to the node's **Refine** route (`REFINE-DISPATCH.json`, permission-gated) with this finding: GAP-WGD-PLAYBOOK is authorable now from local evidence as a delta over `white_glove_v0_1_beta.md` (the service wrapper: document-request kit, onboarding questionnaire, posture-conversation script, deployment record, training-session 2–4 curriculum, branded closeout, missing-doc list). GAP-WGD-CS-HANDOFF and GAP-WGD-DAY60 stay coordinate-flagged pending `staffing-budget-and-triggers` (trigger) and `quality-security-proof` (Day 60 metric schema). Surface EXT-WGD-01/02/03 to Josh as optional benchmarking passes only.
