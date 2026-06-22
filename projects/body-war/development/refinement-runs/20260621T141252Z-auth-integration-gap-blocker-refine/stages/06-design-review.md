# Invoke Design Review

Stage: `s06-invoke-design-review`
Owner: `invoke`
Status: `flag`
Mode: `design-review`
Mode contract: `spells/invoke/design.md`

## Review Target

Existing design artifact:

- `projects/body-war/development/invoke-runs/20260621T131933Z-auth-user-management-integration/AUTH-INTEGRATION-DESIGN.md`

## Six-View Coverage

| View | Status |
| --- | --- |
| Context view | pass |
| High-level structure view | pass |
| Low-level component view | pass |
| Workflow process view | pass |
| Decision flow view | pass |
| Dependency interface view | pass |

## Design Verdict

The design is sound and plan-ready for local integration. It correctly separates
the auth package from BodyWar browser/OAuth/provider/profile ownership.

## Flags

| Flag | Owner | Repair Path |
| --- | --- | --- |
| Current `server.ts` is still single-file and imports unavailable helpers. | BodyWar app | `SWU-BWAUTH-003` |
| BodyWar-owned Postgres provider/profile tables and generated migrations do not exist yet. | BodyWar app | `SWU-BWAUTH-002` |
| Real Strava/VPS/friend proof is not design-ready without operator choices. | Operator/BodyWar infra | existing VPS decision gate, later L3 proof |

## Glossary Consistency

`flag`

The design consistently defines runner principal, provider account, browser
session, trusted session, and Strava profile link. Existing older docs remain
out of sync and are routed to `SWU-BWAUTH-007`.

## Invoke Result

- Mode: `design-review`
- Spell: `invoke`
- Canonical ID: `invoke`
- Scope: `library`
- Phase status: `flag`
- Outputs: `AUTH-INTEGRATION-DESIGN.md`
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface.
- Template/profile selection: DomainSpec six-view Functional TypeScript design.
- Dispatch techniques: `owner_boundary_check`, `state_namespace_boundary`.
- Distill validation: stage 08 will validate repair residue.
- Implementation layering: existing `IMPLEMENTATION-LAYERING.md` in invoke packet.
- Work-pack: n/a for this stage.
- Decisions: no new design blocker prevents the first SWU.
- Unresolved gaps: BodyWar DB/schema implementation, route adapter implementation, stale docs, online proof decisions.
- Next route: `refine-design-review`

## Receipt

```yaml
run_id: 20260621T141252Z-auth-integration-gap-blocker-refine
session_id: session-20260621T141252Z
capability_ref: invoke
receipt_kind: native-stage
artifact: stages/06-design-review.md
status: flag
validation_result: six views pass; implementation and online-proof residue named
blockers:
  - current app still blocked until planned adapter/schema SWUs execute
handoff_note: Interrogate whether each acceptance-critical design gap has an owner and repair path.
```
