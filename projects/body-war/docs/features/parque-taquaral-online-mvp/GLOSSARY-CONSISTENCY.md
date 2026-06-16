---
node_type: glossary-consistency-report
status: flag
topic: Parque Taquaral online MVP vocabulary consistency
last_updated: 2026-06-14
created_by: codex
invoke_mode: design
---

# Glossary Consistency: Parque Taquaral Online MVP

## Result

Status: `flag`

No formal Invoke define glossary exists for this feature. The design can proceed
using the decision record and coverage backlog, but candidate vocabulary must be
stabilized in `domain.md`, `states.md`, and `SPEC.md` before app mutation.

## Candidate Vocabulary

| Term | Intended Meaning | Source | Consistency Note |
| --- | --- | --- | --- |
| `Runner` | Consenting person connecting Strava and submitting activity evidence. | Decision record, coverage backlog | Stable enough for W0. |
| `StravaSession` | Runtime auth/session state linked to Strava OAuth/token references. | Security and API backlog | Must not include raw token values in docs. |
| `StravaActivity` | Redacted activity summary visible to the friend preview. | Strava prototype, mappings backlog | Needs field-level mapping. |
| `PilotTrack` | Parque Taquaral track object used by preview submissions. | Geometry backlog | Must replace `park-track-alpha` placeholder. |
| `TrackGeometry` | Source-backed static route geometry and metadata. | Geometry reviewer | Missing authoritative source. |
| `EvidenceSubmission` | Friend activity submitted as preview evidence for a track. | Strava pilot, decision D-OS-005 | Must separate submission from verification. |
| `PreviewAccepted` | State where evidence updates preview controller without final validation. | Parent synthesis | Preferred over `verified` for MVP. |
| `PreviewControllerState` | Read model shown after accepted preview submission. | UI/test backlog | Must define holder/time/latest evidence fields. |
| `Verified` | Later pilot-ready/operator/GPS validation state. | Discovery, forecast | Deferred; do not use for preview auto-accept. |

## Conflicts To Resolve In W0

| Conflict | Resolution Rule |
| --- | --- |
| `submitted` vs `preview-accepted` vs `verified` | W0 `states.md` must define all three and forbid treating preview acceptance as verification. |
| `Park Track Alpha` vs Parque Taquaral | W0 geometry and domain specs must replace placeholder identity. |
| fixture activity vs real friend activity | Fixtures may support tests only; visible hosted preview uses real friend data. |
| local token JSON vs managed storage | Hosted preview uses sealed secrets and managed storage only. |

## Handoff

Use this report as candidate vocabulary input for `SPEC.md`, `domain.md`, and
`states.md`. Do not promote these terms as canonical outside the feature until
the W0 specs are written and reviewed.

