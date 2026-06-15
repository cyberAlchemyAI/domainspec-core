# Cross-Task Decisions

| Decision ID | Status | Selected Option | Applies To |
| --- | --- | --- | --- |
| D-OS-001 | selected | New TypeScript MVP app. | W1+ |
| D-OS-002 | selected | Canonical `projects/body-war/app/`, replacing Python during implementation. | W1 |
| D-OS-003 | selected | Real friend Strava data in runner-facing preview. | W0, W1, W3 |
| D-OS-004 | selected | Existing Parque Taquaral track as pilot geometry target. | W0 geometry |
| D-OS-005 | selected | Auto-accept matching Strava activity for preview controller. | W0 states, W1 operations |
| D-OS-006 | selected | Hosted managed storage with sealed secrets. | W0 security, W2 deploy |
| D-OS-008 | selected | Preview validation only. | W3 |
| D-OS-009 | selected | Hosted public preview URL. | W2 |
| D-OS-012 | selected | Hosted friend preview succeeds. | All waves |

## Implementation Contract Decisions Still Needed

| ID | Status | Owner | Resolution Path |
| --- | --- | --- | --- |
| D-IMPL-001 | open | W0 | Select hosted runtime/provider in `DEPLOYMENT-SECURITY.md`. |
| D-IMPL-002 | open | W0 | Select managed storage provider/schema in `DEPLOYMENT-SECURITY.md`. |
| D-IMPL-003 | open | W0 | Choose preview access control mode. |
| D-IMPL-004 | defaulted | W0 | Default `read,activity:read`; allow `activity:read_all` only if needed. |
| D-IMPL-005 | open | W0 | Name geometry source. |
| D-IMPL-006 | defaulted | W0 | Preview controller shows holder/time/latest accepted submission. |

