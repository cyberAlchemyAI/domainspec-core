# Research Result - Quality, security, and proof

Local-first research execution pass for one Golden Quill Craft node.
Generated: 2026-06-12. Run: `2026-06-12-craft-pipeline-hydration`.
Dispatch: `gq-research-strategy-quality-security-proof-2026-06-12`.

## Node

- Craft node: `quality-security-proof`
- Context ID: `CTX-QSP-ROOT`
- Research lane: quality, security, and proof research
- Owns: workbook Workstream C and the proof evidence required before customer claims.

## Core Question

What evidence package proves guardrails, boundary security, claims, demo
integrity, and instrumentation before first customer node?

## Execution Posture (gates honored)

- **rg02 local-first**: only Golden Quill workspace evidence read; no web search / WebFetch run.
- **rg03 external-approval**: external research **DEFERRED** — no named gap was elevated to an approved external pass; bounded requests recorded below.
- **rg04 org-isolation**: no `orgs/` client PROJECT_CONTEXT read; Golden Quill project evidence only.
- **rg05 claim-evidence**: every finding mapped to a source class + concrete path (see `research-validation-ledger.md`).
- **rg06 owner-boundary**: planning evidence only; only the two RUN_DIR output files written; `.craft/ledger.yml` not mutated.

## r01 — Scope (node-specific, cross-node drift rejected)

The node scope separates cleanly from sibling Craft nodes. Workstream C
(Quality, Security & Proof) is the only workbook workstream this node owns
(`docs/golden-quill-task-role-breakdown-handoff.md` rows 56-61). Adjacent
workstreams are owned elsewhere and are explicitly **out of scope** here:

- A. Hardware & Physical Node (incl. OS hardening, imaging, signing) → hardware/golden-image nodes.
- B. Software — Tilth Build (posture system, sanitization, audit log) → tilth-runtime-build node.
- D-G (cards, sales, white-glove, ops) → their own Craft nodes.

In-scope proof surfaces (the six Workstream C rows): (1) test plan +
guardrails-as-tests, (2) internal deployment test, (3) independent security
review, (4) claims register, (5) canonical demo standard, (6) instrumentation.

Decision boundary: where business judgment is required (security-reviewer
assignment, claims that touch sales material), the strategy stops and routes to
Josh rather than inventing answers.

## r02 — Local Evidence Baseline (cited by path)

Source classes available locally, deduplicated to concrete handles:

| Evidence class | Concrete handle | What it grounds |
| --- | --- | --- |
| Source contract (workbook) | `docs/golden-quill-task-role-breakdown-handoff.md` rows 56-61 (Workstream C); rows 110, 115 (Roles & Gaps) | The six proof surfaces; QA owner = Victor; Security Reviewer = onboard-now, unassigned, one-time + recurring at major releases |
| Craft ledger | `docs/features/quality-security-proof/.craft/ledger.yml` (gaps[0-3], DESC-QSP-001) | Four active gaps + their severity/owner/treatment; "Victor-led where staffed, external security review required for boundary + signing chain" |
| Craft human view | `docs/features/quality-security-proof/CRAFT.md` | Parent space pointer (node-on-desk-readiness); next move |
| Research strategy | `…/RESEARCH-STRATEGY.md` | Core question; local evidence boundary (Five Laws, architecture gates, workbook proof rows, validation templates); bounded external classes |
| Refine seed | `…/REFINE-SEED-PROPOSAL.md` | Desired outcome (proof-first validation route); write-scope boundary; overlays (toy-game falsification, dialectic) |
| Invoke direction | `…/INVOKE-FIRST-ARTIFACTS.md` | Define→Design→Plan intent: convert proof rows into acceptance tests + evidence gates |
| Governance canon (named, not yet read in detail) | `CLAUDE.md` Five Operating Laws + F-CLASS-* / F-WPFA-* fail-closed gate rosters | Existing guardrail primitives the test plan must cover |

Baseline verdict: local evidence **fully scopes the questions** and names the
gaps, but does not by itself **author** the proof artifacts (test plan,
reviewer scope, claims register, instrument definitions). That authoring is the
deferred Refine/Invoke execution, not research.

## r03 — Research Lane Map (per gap)

Each active gap is assigned a lane: `local-only`, `gap-triggered-external`
(needs approval), or `deferred`.

### GAP-QSP-TEST-PLAN (block) — guardrails-as-tests posture/classification/audit/fail-closed coverage
- **Lane: local-only is sufficient to author the spec.** Five Laws + the F-CLASS-* (sixteen) and F-WPFA-* (twelve) fail-closed gate rosters and architecture gates already define the guardrails to be tested. Source: `CLAUDE.md` gate rosters + workbook row 56.
- External value: optional comparison to industry test-plan patterns — **bounded request B2 below**, not required to start.
- Owner: qa-measurement (Victor).

### GAP-QSP-SECURITY-REVIEWER (block) — independent reviewer onboard-now but unassigned
- **Lane: deferred to operator (business judgment).** This is a staffing/assignment decision, not a research question. Source: workbook rows 58, 115 (one-time + recurring at major releases).
- External value: optional reviewer-scope examples — **bounded request B1 below** — useful for drafting the scope-of-work, but the assignment itself is Josh's call.
- Owner: founder (Josh).

### GAP-QSP-CLAIMS-REGISTER (flag) — external claims need evidence-category mapping
- **Lane: local-only for the register schema; gap may open for category exemplars.** Workbook row 59 + WPFA buyer-facing-claim discipline in `CLAUDE.md` (every claim links to coefficient + cycle_id + Logfire trace_id) already model "claim → evidence" mapping. Source: `CLAUDE.md` WPFA §17 + workbook row 59.
- External value: claims-register format examples — **bounded request B3 below**.
- Owner: qa-measurement (Victor). Business judgment when claims touch sales copy → Josh.

### GAP-QSP-INSTRUMENTATION (flag) — support hrs/node, usage baselines, renewal-intent definitions
- **Lane: local-only for definitions.** WPFA CycleReceipt + instrumentation primitives (`CLAUDE.md` §17; workbook row 61; After-Acceleration "measured unit economics, support-load evidence, renewal data" row 96) supply the metric vocabulary. Source: `CLAUDE.md` WPFA + workbook rows 61, 96.
- External value: SaaS instrumentation baseline benchmarks — **bounded request B4 below**, comparison-only.
- Owner: qa-measurement (Victor).

## r04 — External Approval Gate: DEFERRED (rg03)

No external research is executed by this pass. Every gap above can be **opened
locally** without external input; external comparison is value-add, not a
blocker. Per rg03, external research requires a named gap **and** Josh's
explicit approval. None is present, so all external lanes are recorded as
**deferred bounded requests**:

- **B1 — Security-reviewer scope examples.** Bounded ask: representative scope-of-work for an independent security review covering data-boundary enforcement, Sovereign build, and signing chain. Protected-context flag: none (no client/confidential data leaves the node). Trigger to activate: Josh approves + reviewer assignment proceeds.
- **B2 — Test-plan / guardrails-as-tests patterns.** Bounded ask: how comparable systems structure fail-closed enforcement tests and audit-completeness checks. Protected-context flag: none. Trigger: Josh approves; only if local F-CLASS/F-WPFA rosters prove insufficient to author the plan.
- **B3 — Claims-register format examples.** Bounded ask: claim → evidence-category mapping templates used in regulated/sovereign sales contexts. Protected-context flag: none. Trigger: Josh approves before sales material hardens.
- **B4 — Instrumentation baseline benchmarks.** Bounded ask: typical support-hours/node and renewal-intent instrument definitions for white-glove deployments. Protected-context flag: none. Trigger: Josh approves; comparison-only.

Each request is single-purpose, carries no confidential payload, and stays off
until approved.

## r05 — Claim-Evidence Validation

Full ledger in `research-validation-ledger.md`. Summary: every claim in this
result maps to a source class and a concrete path/handle; no claim relies on an
unapproved external source; no claim crosses org isolation. Two items are
correctly classified as **operator-decision, not research** (reviewer
assignment; sales-touching claim approval).

## Residue

- Local governance canon (`CLAUDE.md` Five Laws + F-CLASS-*/F-WPFA-* rosters) is **named** as the guardrail source but was read at index level, not exhaustively cross-walked into a test matrix. That cross-walk is Invoke-Define authoring work, not research — correctly deferred.
- The security-reviewer **assignment** (GAP-QSP-SECURITY-REVIEWER) cannot be closed by research at all; it is a staffing decision held for Josh.
- No claims-register or instrument definitions were authored (owner-boundary rg06 — research does not author lifecycle artifacts).

## Next Move

Research baseline is complete and confirms **local evidence is sufficient to
author all four gap treatments without external input**. Recommend Josh approve
the node's Refine/Invoke-Define execution pass to convert Workstream C proof
rows into acceptance tests + evidence gates (per `INVOKE-FIRST-ARTIFACTS.md`).
Hold external requests B1-B4 as deferred; activate only B1 (reviewer scope) in
tandem with the reviewer-assignment decision if Josh elects it.

## Files Written This Pass

- `docs/features/quality-security-proof/development/refinement-runs/2026-06-12-craft-pipeline-hydration/RESEARCH-RESULT.md`
- `docs/features/quality-security-proof/development/refinement-runs/2026-06-12-craft-pipeline-hydration/research-validation-ledger.md`
