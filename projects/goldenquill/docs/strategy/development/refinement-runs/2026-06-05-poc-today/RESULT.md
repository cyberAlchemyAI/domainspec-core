# Refine Result: GoldenQuill Same-Day POC Plan

## Result

Status: BLOCKED-BY-DECISION-GATE

The plan is execution-ready once three operator choices are made:

1. audience;
2. POC surface;
3. data policy.

## Refined POC

Build a local **GoldenQuill Promotion Governance POC** that shows one complete
synthetic grant-learning trace:

```text
run context
  -> evidence and outcome event
  -> KPI observation
  -> promotion candidate
  -> Ontology Vault projection
  -> owner decision
  -> validator result
```

## Recommended Path

Use:

- audience: client-facing concept demo;
- surface: `apps/tilth_demo_v0`;
- data: synthetic-only;
- proof: existing L0 `grant_dag` fixture pack and validator.

This is the smallest same-day POC that is honest, demonstrable, and grounded in
current artifacts.

## Execution Tasks After Gate Pass

1. Validate the L0 fixture pack.
2. Add `GET /api/promotion-governance` to `apps/tilth_demo_v0/server.py`.
3. Add a promotion-governance screen to the static UI.
4. Add a short operator script.
5. Run API/UI smoke and validator proof.
6. Commit the POC artifacts.

## Do Not Touch

- production org memory;
- signed cards;
- LOCKed blueprint files;
- production dashboard authority;
- canonical ontology templates;
- DomainSpec;
- CyberAlchemy;
- live client data unless explicitly approved.

## Artifacts

- `RUN-MANIFEST.md`
- `REFINE-SEED-PROPOSAL.md`
- `REFINE-DISPATCH.json`
- `stages/INTERROGATION-REVIEW.md`
- `projects/goldenquill/docs/decisions/goldenquill-poc-today-decision-gate-2026-06-05.md`
