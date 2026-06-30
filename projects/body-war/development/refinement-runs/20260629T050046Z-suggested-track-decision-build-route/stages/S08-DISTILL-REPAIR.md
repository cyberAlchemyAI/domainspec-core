---
stage_id: s08-distill-repair
capability_ref: distill
mode: validate
status: pass
---

# S08 Distill Repair

## Repairs Applied

| Residue | Repair |
| --- | --- |
| Craft still pointed at Slice 1 specs/schema only. | Update Craft ledger/view to point `CTX-BODY-WAR-SUGGESTED-TRACKS` at the confirmed decision-build route and one-go Task Session handoff. |
| Portuguese status copy was inconsistent. | Handoff uses `Em analise` for operator review and keeps source-backed/pilot-ready copy deferred. |
| W0 work-pack gate conflicts with app mutation. | One-go Task Session must include preflight docs/gate update before app code mutation. |
| Validation was generic. | Plan names concrete npm commands and SuggestedTrack-specific tests. |
| Legacy JSON submission path could be misused. | Plan blocks reuse of `/api/submissions` JSON store for new evidence candidates. |

## Repaired Build Boundary

```text
Task Session:
  0. Preflight docs/gate update
  1. SuggestedTrack docs/contracts
  2. Drizzle schema + generated migration
  3. Idempotent Taquaral seed
  4. SuggestedTrack API
  5. Connected-runner UI
  6. SuggestedTrack tests + existing auth/e2e validation
```

## Closure And Recomposition Proof

The repaired unit is small enough for one bounded Task Session because it avoids
source-backed geometry, pilot-ready verification, territory scoring, economy,
and public route claims. It recomposes into Body War as the next child-context
work item under `CTX-BODY-WAR-SUGGESTED-TRACKS`.

## Verdict

`pass`: repaired route can advance to Invoke Plan and final Refine synthesis.

