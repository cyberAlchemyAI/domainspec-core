# TASK-W0-SPEC-BASELINE

## Objective

Create the P0 DomainSpec and implementation-contract baseline required before
TypeScript app mutation.

## Layer And Slice

- Layer: L0.
- Slice: S-000.
- Wave: W0.

## Source Contracts

- `../../PILOT-DOMAINSPEC-BACKLOG.md`
- `../../DESIGN.md`
- `../../GLOSSARY-CONSISTENCY.md`
- `../../IMPLEMENTATION-LAYERING.md`

## Dependencies

None for SWU-BWPT-001. Later W0 SWUs depend on the vocabulary and lane baseline.

## Smallest Working Units

| SWU | Goal | Write Scope | Done Criteria | Validation |
| --- | --- | --- | --- | --- |
| SWU-BWPT-001 | Write parent feature contract. | `../../SPEC.md` | Lanes, decisions, non-goals, aspect links, and stale forecast supersession are explicit. | Markdown review. |
| SWU-BWPT-002 | Write domain and state contracts. | `../../domain.md`, `../../states.md` | `preview-accepted` and `verified` are distinct. | Markdown review. |
| SWU-BWPT-003 | Write geometry contract and artifact/link. | `../../TRACK-GEOMETRY.md`, static geometry path | Source, route metadata, format, status, and caveats are explicit. | Review source and caveats. |
| SWU-BWPT-004 | Write deployment/security contract. | `../../DEPLOYMENT-SECURITY.md` | Provider, storage/schema, env, privacy, retention, redaction, access mode are selected. | Markdown review. |
| SWU-BWPT-005 | Write API/domain aspect docs. | `../../interfaces.md`, `../../operations.md`, `../../queries.md`, `../../mappings.md` | Auth, activities, tracks, submissions, controller, redaction contracts exist. | Markdown review. |
| SWU-BWPT-006 | Write UI and test specs. | `../../ui-spec.md`, `../../TEST-SPEC.md` | Hosted friend page and PTV matrix are specified. | Markdown review. |

## Subagent Handoff

Prefer one local or subagent task per SWU. Return:

```yaml
swu_id: <id>
result: pass | flag | block
files_touched: []
validation: []
blockers: []
handoff_note: <summary>
```

## Synchronization Rules

- If SWU-BWPT-003 cannot identify a geometry source, record a blocker instead
  of inventing geometry.
- If SWU-BWPT-004 cannot select provider/storage from available context, route
  through `decision-gate`.
- Reopen work-pack mutation gate only after all W0 SWUs pass.

