# Operations V1 Traceability

| Accepted obligation | Plan decision | SWUs | Required evidence |
| --- | --- | --- | --- |
| OV1-D1 separate identity | OV1-PD1 | 004-006 | V0 and operations ids/routes coexist after restart. |
| OV1-D2 immutable bodies | OV1-PD1, PD4 | 003-006 | Blob digest/body/reference and missing-body fail-closed tests. |
| OV1-D3 complete commit | OV1-PD4 | 006-008 | Browser never receives partial fragment bytes. |
| OV1-D4 whole document | OV1-PD11 | 001, 006-008 | Schema rejects region targets; operations use whole document. |
| OV1-D5 parser operations | OV1-PD2 | 002, 006-008 | Golden replace/append/rebuild serializer fixtures. |
| OV1-D6 CAS/idempotency | OV1-PD5 | 005-007 | duplicate/conflict/stale/concurrent matrix. |
| OV1-D7 navigation separation | OV1-PD6, PD7 | 009-010 | Non-selected commits do not redirect; redirect survives restart. |
| OV1-D8 trusted-local authority | OV1-PD12 | 001, 014 | No approval/skill receipt or protected-effect route added. |
| OV1-D9 explicit rebuild | OV1-PD1 | 008 | Later V0 publication does not sync; explicit exact-hash rebuild does. |
| OVG-001 parser/version | OV1-PD2 | 002 | Lockfile pin and golden corpus. |
| OVG-002 limits | OV1-PD3 | 001, 005-008 | minus/exact/plus rejection before commit. |
| OVG-003 retention | OV1-PD8-PD10 | 011-012 | grace/hard/startup/tombstone/shared-ref/410 evidence. |
| OVG-004 navigation | OV1-PD6, PD7 | 009-010 | durable target and transient refresh/ack evidence. |
| Honest user value claim | all | 013-014 | Agent creates/operates/shows interactive HTML; integrated closeout. |

Evidence links are added only by Task Session receipts. Planning paths are not
implementation proof.
