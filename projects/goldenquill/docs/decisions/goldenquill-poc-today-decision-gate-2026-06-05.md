# Decision Gate: GoldenQuill Same-Day POC

Date: 2026-06-05
Status: BLOCK pending operator choices
Target scope: GoldenQuill same-day POC

## Gate Result

Result: BLOCK

Reason: three blocker-level choices materially affect the POC implementation,
copy, validation bar, and risk posture. Consequential implementation should wait
until these are selected.

## Decision 1: POC Audience

Question: Who is the POC for today?

### Option A: Client-Facing Concept Demo

Benefit: strongest external story; shows why GoldenQuill is different.
Cost/risk: copy must avoid overclaiming production readiness.
Choose when: the goal is to send/show a compelling product concept today.
Downstream impact: emphasize workflow, governance, learning trace, and safety.

### Option B: Internal Technical Validation

Benefit: strongest engineering clarity; easiest to validate.
Cost/risk: less persuasive to nontechnical viewers.
Choose when: the goal is to prove architecture correctness before polish.
Downstream impact: emphasize validator output, rule IDs, fixture coverage, and
execution commands.

### Option C: Investor/Product Narrative Demo

Benefit: strongest narrative for the product category and roadmap.
Cost/risk: can drift into pitch-deck abstraction.
Choose when: the goal is to show product direction and defensibility.
Downstream impact: emphasize moat, workflow traceability, ontology governance,
and future learning loop.

Recommended: Option A if you need to show a client today; Option B if today is
mainly for execution readiness.

Selected: pending

## Decision 2: POC Surface

Question: Where should the POC live?

### Option A: Extend `apps/tilth_demo_v0`

Benefit: fastest real app surface; existing FastAPI/static UI/demo mode.
Cost/risk: older static UI may need careful styling work.
Choose when: the goal is an interactive local POC today.
Downstream impact: implement endpoint plus screen; run local server.

### Option B: Create A Separate Static HTML Explainer

Benefit: fastest sendable artifact; low runtime dependency risk.
Cost/risk: less convincing as a real product POC.
Choose when: the goal is a client-sendable artifact today.
Downstream impact: no server integration; package as HTML.

### Option C: Do Both, App First

Benefit: app proves interaction; HTML becomes sendable summary.
Cost/risk: more work today.
Choose when: both live demo and sendable artifact are required.
Downstream impact: implement app first, then generate static sendable.

Recommended: Option A for today; Option C only if there is enough time after
the app screen validates.

Selected: pending

## Decision 3: Data Policy

Question: What data should the POC use?

### Option A: Synthetic-Only

Benefit: safest; aligns with L0 fixture proof; no privacy/source ambiguity.
Cost/risk: less emotionally concrete than FIT Farms.
Choose when: speed and safety matter most.
Downstream impact: POC reads only synthetic fixture files.

### Option B: FIT Farms Demo Overlay

Benefit: more concrete and product-like.
Cost/risk: must avoid implying live truth or leaking private context.
Choose when: the audience needs a recognizable scenario and the operator is
comfortable with the demo context.
Downstream impact: UI copy must clearly label demo data; validation must avoid
reading production org memory.

### Option C: Live Data

Benefit: strongest realism.
Cost/risk: too risky for same-day POC; source, privacy, and mutation boundaries
become blockers.
Choose when: a controlled internal replay has already been approved.
Downstream impact: not recommended today.

Recommended: Option A.

Selected: pending

## Deferred Decisions

- Whether L1 typed models are required before demo. Recommendation: defer.
- Whether `OwnerDecision` is standalone JSON or append-only projection.
  Recommendation: defer until after POC.
- Whether to package a client-sendable ZIP. Recommendation: decide after the
  app/demo artifact exists.

## Assumptions If Operator Chooses Recommended Path

- Audience: client-facing concept demo.
- Surface: `apps/tilth_demo_v0`.
- Data: synthetic-only.
- Execution mode: local demo.
- Validation: L0 validator plus manual/browser smoke.

## Next Step

Ask the operator to select:

1. POC audience: A, B, or C.
2. POC surface: A, B, or C.
3. Data policy: A, B, or C.

After selection, run one bounded task-session to implement the selected same-day
POC.
