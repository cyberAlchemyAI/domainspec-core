---
node_type: invoke-transport-report
status: flag
topic: Invoke design transport for Parque Taquaral online MVP
last_updated: 2026-06-14
created_by: codex
invoke_mode: design
---

# Invoke Design Transport

## Invocation

| Field | Value |
| --- | --- |
| Observed capability | `invoke` |
| Mode | `design` |
| Target artifact | `parque-taquaral-online-mvp` feature |
| Target owner | Body War project docs / future `task-session` execution |
| Mode contract | `.agents/skills/invoke/design.md` |
| Template/profile | Module Formulae architecture bundle plus glossary consistency companion |

## Outputs

| Artifact | Status |
| --- | --- |
| `DESIGN.md` | active |
| `GLOSSARY-CONSISTENCY.md` | flag |
| `DESIGN-TRANSPORT.md` | active |

## Gate Status

| Gate | Status | Notes |
| --- | --- | --- |
| Six design views | pass | Present in `DESIGN.md`. |
| Source contracts | pass | Decisions, coverage, backlog, architecture audit, and prototype refs are cited. |
| Glossary consistency | flag | No formal define glossary exists. |
| No upstream mutation | pass | No source code or canonical DomainSpec methods were edited. |
| Plan handoff | pass | `IMPLEMENTATION-LAYERING.md` and work-pack outputs may be authored. |

## Gap Ownership

| Gap | Owner |
| --- | --- |
| Missing formal define glossary | Target feature W0 specs. |
| Hosted provider/storage choice | Target feature `DEPLOYMENT-SECURITY.md`. |
| Source-backed geometry | Target feature `TRACK-GEOMETRY.md`. |

## Next Route

Proceed to `invoke plan` for the same target. Do not route to implementation
until W0 specs are written and the work-pack mutation gate is reopened.

