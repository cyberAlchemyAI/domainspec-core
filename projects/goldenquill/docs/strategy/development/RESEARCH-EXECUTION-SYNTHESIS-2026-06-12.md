# Cross-Node Research Execution — Synthesis

- Date: 2026-06-12
- Operation: `/craft execute all research strategies using subagents`
- Scope: all 11 Golden Quill Craft nodes (7 under `docs/strategy/development/`, 4 under `docs/features/`)
- Execution mode: **local-first**, one subagent per node (covering the three dispatch role lenses: local-evidence-reviewer, external-boundary-reviewer, claim-validation-reviewer)
- Gates held across all nodes: `rg02` local-first · `rg03` external research DEFERRED (no web/external lookup run) · `rg04` org-isolation (no `orgs/` client PROJECT_CONTEXT read) · `rg05` claim→source-path mapping · `rg06` owner-boundary (only per-node `RESEARCH-RESULT.md` + `research-validation-ledger.md` written; canonical/lifecycle artifacts untouched)
- Result: **11/11 PASS**. Per-node outputs in each node's `development/refinement-runs/2026-06-12-craft-pipeline-hydration/`. Each ledger `next_move` advanced to post-execution state.

## Per-node verdicts

| Node | Verdict | Core finding | Binding residue (not closable by research) |
|---|---|---|---|
| capital-logic-library | PASS | Card schema/governance is a local BUILD task; 5 launch cards (1 at v1, 4 authoring) | **Block:** 4 segment domain-experts unfilled (contracting action) |
| hardware-golden-image | PASS | Doctrine names SKUs + 128GB floor but no testable spec/burn-in thresholds | Image-verify + backup-recovery procedures unwritten (locally authorable) |
| quality-security-proof | PASS | Guardrails-to-test already exist as Five Laws + F-CLASS-*(16) + F-WPFA-*(12) | Security-reviewer **assignment** is a staffing decision |
| tilth-runtime-build | PASS | Substrate LOCKED (Pydantic AI/Logfire/Ollama/DSPy/Logician); Workstream B work-packs authorable | Posture-canon + UI-phase decisions owned by boundary-and-canon |
| after-acceleration-roadmap | PASS | 8 post-capital themes enumerated but unsequenced; only 2 carry explicit triggers | `DEC-AAR-STAGE-GATES` threshold values are founder judgment |
| boundary-and-canon | PASS | 5 workbook↔canon conflicts (posture vocab "Sanitized", sanitization pipeline, console UI, "Municipal", "Sovereign-mode") | F3 UI-phase + F5 disambiguation are governance calls |
| company-operations-finance | PASS | 4 ops gaps map 1:1 to Workstream G; 2 authorable now, 2 have optional external hardening | Validation packet depends on quality-security claims register; fractional roles unstaffed |
| node-on-desk-readiness (parent) | PASS | Readiness path is mappable but NOT yet proven — no child runtime receipts recomposed upward | `GAP-NOD-HOURS-RATES` (block) needs operator input |
| sales-contracting-legal | PASS | Workstream E = 4 tasks; Legal (fractional) is the gating role before first LOI | **Block:** legal clauses close only when fractional counsel retained |
| staffing-budget-and-triggers | PASS | Every Est.Hrs / Rate cell blank → budget not computable; all triggers qualitative | Hours, later-roles, `DEC-SBT-TRIGGER-MODEL` are operator input |
| white-glove-delivery-node-care | PASS | Technical onboarding spine already locked in `white_glove_v0_1_beta.md`; gap is the human service wrapper | Day-60 metrics depend on quality-security instrumentation |

## Consolidated external-research approval surface (gate rg03 — needs Josh)

No external research ran. Each node recorded the bounded external classes it would request **only on explicit approval**. Grouped:

1. **Funder / capital references** (capital-logic-library): segment source-universe lists, recurring funder rule references, expert-input scoping norms.
2. **Hardware references** (hardware-golden-image): current reference-SKU spec sheets; burn-in/thermal/inference threshold references.
3. **Market-rate / labor benchmarks** (staffing-budget-and-triggers, after-acceleration-roadmap, company-operations-finance): fractional legal/security/bookkeeping rates, install/support labor benchmarks, domain-expert compensation norms.
4. **Legal / compliance patterns** (sales-contracting-legal): legal-clause patterns, FERPA/AI-transparency checklist, procurement/insurance refs, disclosure language, deposit/invoicing norms.
5. **Service-delivery / proof patterns** (white-glove-delivery-node-care, quality-security-proof): CS onboarding playbooks, field-tech runbooks, Day-60 QBR patterns, security-reviewer scope, claims-register formats, instrumentation baselines.

All are public-reference, no protected-context / no org data. Each is gap-triggered and optional — none blocks the local-first Refine authoring lanes below.

## Cross-node residue themes

- **Stale posture vocabulary** ("Sanitized" / 4-posture) recurs in the workbook (`docs/golden-quill-task-role-breakdown-handoff.md:50`) and is flagged by boundary-and-canon, tilth-runtime-build, node-on-desk-readiness, and white-glove. Canon is the v7.0.10 three-posture model. Single fix: close `DEC-BC-POSTURE-VOCAB`.
- **Operator-input blocks** that no research can clear: hours/rates, onboarding trigger thresholds, stage-gate threshold values, domain-expert + fractional-counsel + security-reviewer staffing decisions.
- **Cross-node dependency:** the quality-security-proof claims/instrumentation register feeds company-operations-finance's validation packet and white-glove's Day-60 metrics.

## Next moves (local-first, no approval needed)

Each node's Refine route is now unblocked for local-first authoring:
- boundary-and-canon → close `DEC-BC-POSTURE-VOCAB` (clears stale-vocab residue fleet-wide) + take UI-phase decision.
- node-on-desk-readiness → author the parent recomposition sequence from encoded child dependency edges.
- tilth-runtime-build → Invoke `plan` on `GAP-TRB-WORK-PACKS`.
- white-glove → author the service-wrapper delta over `white_glove_v0_1_beta.md`.
- company-operations-finance → begin authoring led by block-severity `GAP-COF-SUPPORT-TRIAGE`.

## Pending operator decisions (batched for Josh)

1. Approve / defer the five external-research classes above (per node or globally).
2. Provide per-row hours + numeric onboarding trigger thresholds (`staffing-budget-and-triggers`).
3. Staffing go/no-go: segment domain-experts, fractional legal counsel, security reviewer.
4. Stage-gate threshold values for the after-acceleration roadmap.
5. UI-phase call (`DEC-BC-UI-BOUNDARY`) — read-only projection vs. interactive console vs. v0.1 headless-only.
