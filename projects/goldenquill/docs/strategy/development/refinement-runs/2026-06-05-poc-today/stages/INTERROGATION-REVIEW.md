# Interrogation Review: GoldenQuill Same-Day POC Plan

Mode: refine-final / readiness pressure test
Verdict: FLAG

## High-Discrimination Question

What must the POC prove today?

Recommended answer: prove the **workflow learning and promotion-governance
idea**, not the full production grant runtime.

Why this matters: the repo has enough substrate and demo UI to show a compelling
operator story today, but not enough committed integration to honestly claim
production learning-loop activation.

## Pressure Test

### 1. Is the plan too broad?

Yes, if it tries to include live Scout, Scribe, Judge, Logician, org vault,
dashboard, ontology promotion, and client data.

No, if it narrows to:

- existing demo UI;
- synthetic L0 promotion fixtures;
- deterministic validator result;
- visible trace from evidence to owner decision.

### 2. Is there an existing surface to reuse?

Yes. `apps/tilth_demo_v0` is the best same-day surface because it is FastAPI
plus static HTML/JS and already has demo mode. The React/Vite app is likely a
better future product surface, but the README is still template-default and the
same-day risk is higher.

### 3. Is the core claim validator-backed?

Partially. The L0 fixture pack and validator prove promotion governance rules:

- source-backed outcomes;
- KPI denominator semantics;
- stage depth is not outcome truth;
- no approved uses before owner decision;
- no workspace reuse from unredacted org feedback;
- no KPI threshold direct promotion.

This is strong enough for a POC proof, not a production guarantee.

### 4. What would make the POC misleading?

- Using live FIT Farms/customer-like data without source and privacy controls.
- Presenting synthetic validator fixtures as actual grant outcomes.
- Saying Ontology Vault templates are promoted.
- Saying the dashboard can promote lessons.
- Hiding that `pytest` was previously unavailable.

### 5. What is the smallest executable slice?

One new demo endpoint plus one new static UI screen:

```text
GET /api/promotion-governance
  -> reads L0 fixture pack
  -> returns validator-shaped summary
  -> UI renders trace, gates, and owner decision
```

### 6. What can be deferred safely?

- L1 typed models.
- persistent `OwnerDecision` storage.
- dashboard read model.
- live org data integration.
- Ontology Vault companion schema/template promotion.
- client-sendable packaging.

## Blockers

1. POC audience is unresolved.
2. POC surface is unresolved.
3. Data policy is unresolved.

These are real blockers because they change implementation and presentation.

## Gaps

1. Need fresh validation after current dirty worktree state.
2. Need dependency check for FastAPI/uvicorn.
3. Need browser/manual visual validation if the UI is changed.
4. Need commit boundary after L0/POC artifacts are accepted.

## Recommendation

Proceed only after the decision gate resolves:

- audience: internal/product/client;
- surface: `tilth_demo_v0`, static HTML, or both;
- data: synthetic-only or FIT Farms demo overlay.

Recommended defaults:

- audience: product/client concept demo;
- surface: `tilth_demo_v0`;
- data: synthetic-only.

