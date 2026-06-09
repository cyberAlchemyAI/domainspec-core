# Refine Seed Proposal: GoldenQuill Same-Day POC

## Refine Run Strategy Proposal

Selected route: same-day POC execution plan with `baseline_sequence`,
`xray_for_hidden_structure`, `toy_game_for_low_cost_falsification`, and
`memory_residue_for_context_recovery`.

Why this route fits:

- GoldenQuill has a real demo shell in `apps/tilth_demo_v0/`.
- GoldenQuill has a new PromotionRecord L0 fixture/validator proof, but it is
  not yet shown in the UI or committed as a product-facing POC.
- Project status says the engineering surface is ahead of the human-readable
  surface, so the POC should make the existing capability legible instead of
  pretending to finish every runtime integration.
- Runtime maturity docs warn that several surfaces are future/dormant or
  gate-live only, so the plan must label what is demo, validator-backed, and
  production-live.

## Recommended POC Concept

Build a local operator demo called:

**GoldenQuill Promotion Governance POC**

The POC should show one complete synthetic grant run trace:

```text
grant run context
  -> opportunity and evidence snapshot
  -> outcome event
  -> KPI observation
  -> promotion candidate
  -> Ontology Vault projection
  -> owner decision
  -> validator result
```

The user experience should be simple:

1. Open the existing Tilth demo UI.
2. Navigate to a new or adapted "Learning Trace" / "Promotion Governance"
   surface.
3. See the work-run timeline, validator pass/fail cases, and owner decision.
4. Run or display the deterministic L0 validator result.
5. Explain clearly that this is a synthetic/demo POC and not production memory
   mutation.

## Same-Day Scope

In scope:

- local demo-only read model;
- UI panel or static route that visualizes the existing L0 fixture pack;
- validator command surfaced in the plan and optionally in the demo server;
- clear labels: synthetic data, source-backed evidence, KPI-not-promotion,
  owner decision required;
- short operator script for presenting the POC.

Out of scope:

- production org-vault mutation;
- signed-card mutation;
- live customer data;
- dashboard promotion authority;
- canonical ontology template promotion;
- full Scout/Scribe/Judge/Logician live cycle;
- LOCKed blueprint edits;
- provider/model integration.

## Best Execution Path

Use a two-layer POC:

### Layer A: Demonstrable Interface

Use `apps/tilth_demo_v0` because it already has:

- FastAPI server;
- static UI;
- demo mode;
- existing navigation and evidence screens;
- routeable front-end without a full React build dependency.

Add one demo-only API endpoint and one UI screen:

```text
GET /api/promotion-governance
```

It should read the synthetic L0 fixture pack and return:

- positive case count;
- negative case count;
- rule registry;
- validator status;
- work-run timeline projection;
- owner-decision summary;
- blocked false-promotion examples.

### Layer B: Validator-Backed Proof

Use the existing L0 validator:

```bash
PYTHONPATH=projects/goldenquill python3 \
  projects/goldenquill/pipeline/grant_dag/validate.py \
  projects/goldenquill/pipeline/grant_dag/fixtures/promotion_record_l0_fixture_pack.json
```

This proves the POC story is not just UI prose.

## Execution Plan

### Task POC-001: Validate L0 Baseline

Goal: prove current L0 artifacts still pass.

Commands:

```bash
python3 -m json.tool \
  projects/goldenquill/pipeline/grant_dag/fixtures/promotion_record_l0_fixture_pack.json

PYTHONPATH=projects/goldenquill python3 \
  projects/goldenquill/pipeline/grant_dag/validate.py \
  projects/goldenquill/pipeline/grant_dag/fixtures/promotion_record_l0_fixture_pack.json
```

Done when:

- JSON parses;
- validator returns `status: pass`;
- output is copied or summarized into the POC validation report.

### Task POC-002: Add Demo Read Model Endpoint

Goal: expose the synthetic promotion-governance fixture pack to the demo UI.

Files:

- `projects/goldenquill/apps/tilth_demo_v0/server.py`
- optional helper under `projects/goldenquill/apps/tilth_demo_v0/`

Rules:

- read only synthetic fixture files;
- do not read `orgs/`;
- do not mutate memory/cards/dashboard/ontology;
- no subprocess execution required for first slice unless the endpoint is
  explicitly a manual validator trigger.

Done when:

- `/api/promotion-governance` returns structured JSON;
- endpoint works in `TILTH_DEMO_MODE=demo`;
- missing fixture file fails gracefully.

### Task POC-003: Add UI Screen

Goal: show the promotion-governance trace in the existing static UI.

Files:

- `projects/goldenquill/apps/tilth_demo_v0/static/index.html`
- `projects/goldenquill/apps/tilth_demo_v0/static/app.js`
- `projects/goldenquill/apps/tilth_demo_v0/static/style.css`

Minimum screen content:

- "Synthetic POC" label;
- work-run timeline;
- evidence-state discipline;
- KPI observations;
- promotion candidates;
- blocked negative cases;
- owner decision;
- validator status.

Done when:

- route opens from sidebar;
- data loads from endpoint;
- UI explains that KPI/stage/retrieval are not promotion authority;
- no text overflows obvious containers.

### Task POC-004: Add Operator Script

Goal: make the POC presentable today.

Artifact:

- `projects/goldenquill/docs/strategy/goldenquill_poc_operator_script_2026-06-05.md`

Minimum sections:

- what this proves;
- what it does not prove;
- three-minute demo path;
- validator command;
- next engineering step.

### Task POC-005: Validate Demo

Commands:

```bash
cd projects/goldenquill/apps/tilth_demo_v0
TILTH_DEMO_MODE=demo uvicorn server:app --port 8000
```

Then browser-check:

- home loads;
- promotion-governance screen loads;
- endpoint response renders;
- validator status is visible.

If browser automation is available, capture one screenshot. If not, use static
HTML review plus API smoke.

## Blockers And Gaps

### Blocker B1: POC Audience

Decision needed: who is this POC for today?

Options:

- client-facing concept demo;
- internal technical validation;
- investor/product narrative demo.

This changes the UI copy and how much implementation detail is shown.

### Blocker B2: POC Surface

Decision needed: should today's POC extend `tilth_demo_v0`, create a separate
static HTML explainer, or do both?

Recommendation: extend `tilth_demo_v0` first, then optionally create a client
sendable HTML after the POC works.

### Blocker B3: Data Policy

Decision needed: synthetic-only or include FIT Farms demo references?

Recommendation: synthetic-only today. FIT Farms/live data introduces privacy and
truth-status questions that slow the POC.

### Gap G1: Pytest Availability

L0 has validator proof, but previous runs found `pytest` unavailable. The POC
can proceed with direct validator proof; a full test run should happen before
commit or client send.

### Gap G2: L1 Typed Model Not Landed

Typed local models are useful, but not required for a same-day POC. The UI can
consume the L0 fixture pack directly.

### Gap G3: OwnerDecision Storage Deferred

The POC can show owner decision as a synthetic fixture. Persistent owner-decision
storage should wait until after the POC.

### Gap G4: Existing Demo Dependencies

FastAPI/uvicorn may not be installed in the local shell. If unavailable, use a
static HTML fallback or install the app package in a virtualenv.

## Recommendation

Proceed with a **demo-only UI extension over L0 fixtures**.

This is the smallest honest POC that can be shown today:

- it uses an existing app surface;
- it uses existing validator-backed governance fixtures;
- it avoids live data and production mutation;
- it demonstrates the core GoldenQuill idea clearly.

