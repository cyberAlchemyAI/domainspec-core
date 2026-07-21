---
tags: [domainspec-v2, task-session, graph-composability, test-derivation]
node_type: session
is_session: true
layer: implementation
nature: execution-preflight
status: blocked
created: 2026-07-20
timestamp: 2026-07-20T00:13:43-03:00
expires: 2026-09-18
conversation_id: null
decisions_made: false
contradictions_found: true
specs_updated: []
promoted_candidates: []
expected_importance: 7
importance_rationale: "Identified the missing authored formal predicate that prevents the first graph-to-test receipt from being honest, and separated current v2 enforces authority from the legacy engine dialect."
---

# SWU-GCP-001 key-and-door proof preflight

## Summary

Task Session resolved the first graph-composability SWU and built a strict
context pack. The source graph and relationship signature are sufficient for a
structural proof, but not for the required executable assertion: the key-and-door
Rule declares a boolean return type without authoring its predicate or fixture
inputs. The legacy engine's `enforces` direction also differs from current v2
authority, so current v2 authority must control any adapter.

## Result

Blocked before implementation mutation pending `DEC-GCP-001`.

## Evidence

- `projects/domainspec-v2/development/evolvable-validation-framework/runs/SWU-GCP-001/CONTEXT-PACK.md`
- `projects/domainspec-v2/development/evolvable-validation-framework/runs/SWU-GCP-001/TASK-SESSION-RESULT.md`
- `projects/domainspec-v2/development/evolvable-validation-framework/decisions/2026-07-20-key-and-door-formal-source.md`

## Next step

Resolve where the formal predicate lives, then resume the same Task Session.
