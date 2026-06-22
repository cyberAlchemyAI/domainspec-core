# Plan Transport - BodyWar Auth Integration

Status: `invoke-pass`
Mode: define + design + plan
Target artifact owner: `projects/body-war`

## Outputs

- `CONTEXT-PACK.md`
- `AUTH-INTEGRATION-SPEC.md`
- `AUTH-INTEGRATION-DESIGN.md`
- `IMPLEMENTATION-LAYERING.md`
- `WORK-PACK.md`
- `DISPATCH.json`
- `PLAN-TRANSPORT.md`

## Dispatch Technique Trace

| Technique | Used For | Evidence |
| --- | --- | --- |
| `sequence` | Context feeds spec, design, plan, and handoff. | `DISPATCH.json` steps `s01` through `s05`. |
| `artifact_contract_bridge` | Bind invoke outputs to concrete artifact contracts. | Spec/design/work-pack paths are explicit. |
| `owner_boundary_check` | Separate auth package ownership from BodyWar adapters. | Spec capability boundary and design decisions. |
| `authority_split_gate` | Preserve operator gate for real deployment and credentials. | Work-pack blockers and dispatch gates. |
| `state_namespace_boundary` | Keep secrets/provider data out of tracked artifacts. | Dispatch boundary evidence. |
| `scu_swu_reduction` | Select local integration SWU before VPS proof. | Work-pack SWU manifest. |
| `recomposition_proof` | Show local auth proof recomposes into online preview. | Implementation layering L0-L3. |
| `validation_loop` | Map every SWU to commands and reviewable checks. | Work-pack validation strategy. |
| `execution_receipt_handoff` | Make Task Session receipt fields explicit. | Dispatch receipts and work-pack next route. |
| `residue_ledger` | Preserve deployment and consent blockers. | Context pack and work-pack blockers. |
| `concrete_path_evidence` | Cite real source paths and check results. | Context pack selected sources and current app check failure. |
| `observability_grouping` | Group follow-up evidence under this invoke run. | Dispatch observability section. |

Full dispatch document:

- `DISPATCH.json`

## Distill Validation

Verdict: `pass`.

Current smallest coherent unit:

- `SWU-BWAUTH-001`: add generic trusted-session support to the auth package.

Why this is the right size:

- Smaller work, such as only changing BodyWar imports, cannot create a session
  after Strava identity proof without duplicating package session/token logic.
- Larger work, such as real VPS deployment, is blocked by operator decisions and
  would hide the current compile failure.
- The unit recomposes into BodyWar browser sessions, Strava callback handling,
  profile routes, local Postgres E2E, and later online proof.

## Decisions

| Decision | Selected Default | Reason |
| --- | --- | --- |
| Shared package browser/OAuth ownership | Do not move browser/OAuth/Strava into the shared package. | Keeps package reusable and matches adoption boundary. |
| Session after Strava callback | Add generic trusted-session use case to auth package. | Prevents BodyWar from duplicating session/token lifecycle. |
| BodyWar provider/profile storage | BodyWar-owned Drizzle schema and migrations. | Provider accounts and profile projections are product/runtime-specific. |
| First executable layer | Local compile and E2E integration. | Real deployment remains operator-gated. |

## Unresolved Gaps

Invoke gaps: none.

Target-artifact gaps:

- Current BodyWar app check fails until implementation starts.
- Existing BodyWar docs contain stale ownership statements and need a later doc
  patch SWU.
- Real deployment decisions remain blocked in
  `docs/decisions/vps-deployment-readiness.md`.
- Friend activity validation remains blocked until consent exists.

## Recommended Next Route

Run `task-session` on `SWU-BWAUTH-001`:

```text
[$task-session] projects/body-war/development/invoke-runs/20260621T131933Z-auth-user-management-integration/WORK-PACK.md --swu SWU-BWAUTH-001
```

Do not start VPS deployment, real Strava callback configuration, or friend
activity validation until the existing operator gates are resolved.
