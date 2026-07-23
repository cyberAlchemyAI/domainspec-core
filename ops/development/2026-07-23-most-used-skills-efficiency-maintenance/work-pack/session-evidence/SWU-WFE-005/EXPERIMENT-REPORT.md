# Experiment Report: Task Session Mutation Admission

- Run: `task-session-mutation-admission-20260723T034836Z`
- Result: `PASS`
- Lifecycle owner: `sigil-development`
- Scope: routed/reusable mutation admission and standalone non-mutating compatibility

## Controls

| Regime | Result |
| --- | --- |
| Existing decision/completion and closeout policy | 19/19 pass |
| Existing nearest-SWU resolution | 11/11 pass |
| New mutation-admission matrix | 9/9 pass |
| Producer-owned receipt schema digest | `2c4ef7c0529f419278a3af530783383d05ccf8e144a40e895f26c2c2d6b77b6b` |
| Canonical/Codex/Claude contract and support parity | pass |

The new matrix causally covers exact admission, absent receipt, producer-schema
failure, stale controlling source, mismatched task, changed dependency,
expanded write scope, missing authority class, and standalone non-mutating
compatibility. The admitted case also asserts that live validation remains
required and preserves its command surface.

## Verdict

The routed mutation gate is fail-closed and independently reproducible. The
receipt proves admission only; it grants no lifecycle, promotion, publication,
or mutation authority and does not replace live post-mutation validation.
