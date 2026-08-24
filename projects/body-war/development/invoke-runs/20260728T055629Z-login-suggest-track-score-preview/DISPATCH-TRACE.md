---
module: body-war-login-suggest-track-score-preview
version: current
status: pass
updatedAt: 2026-07-28
docType: dispatch-trace
---

# Dispatch Trace

## Trigger

A full Dispatch Spec is required because the planned route crosses:

- Body War feature and application ownership;
- product/privacy decision authority;
- protected provider tokens and private route geometry;
- Strava external API;
- browser and human-participant evidence;
- hosted execution and promotion-sensitive claims.

## Technique Selection

| Technique | Why selected |
| --- | --- |
| `sequence` | Decisions, migrations, local evidence, provider implementation, and live witness have hard dependencies. |
| `frame_handoff` | Each stage returns an explicit bounded receipt to the next owner; HOST admission returns to the parent before a separate witness step. |
| `validation_loop` | Geometry, scoring, UI, and provider failures need positive and negative controls. |
| `owner_boundary_check` | Product decisions and promotion cannot be inferred from implementation. |
| `artifact_contract_bridge` | Exact Design/Plan selectors must bind application changes and receipts. |
| `observability_grouping` | Fixture, participant, and real-provider evidence must stay separable. |

## Subagent Strategy

`none` for future implementation. One Task Session at a time is safer because
the SWUs intentionally sequence changes across the same repository, server,
schema, static UI, and tests.

Distill validation roles used during this Invoke authoring are plan-review
roles, not the implementation dispatch strategy.

## Artifact

`EXECUTION-DISPATCH.json`

Validation:

```sh
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py --json \
  projects/body-war/development/invoke-runs/20260728T055629Z-login-suggest-track-score-preview/EXECUTION-DISPATCH.json
```

Result: `pass`; 0 blocks, 0 flags.

Post-review reconciliation preserved this result after splitting HOST admission
from witness execution and binding both to claim-specific receipt artifacts
inside the generic Dispatch Spec envelope.
