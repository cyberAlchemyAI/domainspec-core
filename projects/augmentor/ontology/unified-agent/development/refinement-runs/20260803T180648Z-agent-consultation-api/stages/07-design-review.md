# Stage 7: Independent API Boundary Review

## Structured Interview Result

- Target scope: `stages/06-design.md` and
  `design-selection/selection-result.json`.
- Mode: `refine-design-review`.
- Reviewer: `api-boundary-reviewer`.
- Questions asked: 0; this was an evidence-backed artifact review.
- Decisions recorded: 10 high-priority repair requirements.
- Artifacts updated by reviewer: none; the helper was read-only.
- Verdict: `flag`.
- Next step: Distill Repair must address H1-H10 before Invoke Plan.

## Review Summary

The reviewer found no critical issue. It confirmed that write, execution,
routing, approval, memory mutation, and authority-effect capabilities are absent
from the response contract. The API and answering-agent separation is clear in
intent, but the design still lets retrieval make two reasoning-like decisions:
whether a partial result can support an answer and whether unstructured prose is
materially conflicting. Those decisions must move out of the API.

## Required Repairs

| ID | Design selector | Finding | Required repair |
| --- | --- | --- | --- |
| H1 | `Low-level Component View / CallerContext`; `Access And Privacy Contract` | Identity appears in the model-visible request. | Inject a verified principal out of band or use an opaque signed handle; never trust model-supplied identity fields. |
| H2 | `ConsultationResponse`; `Decision Flow View` | One response shape can leak protected metadata on denial. | Use status-tagged response variants, a minimal denial shape, and deterministic status precedence. |
| H3 | `EvidenceItem`; `EvidenceSourceHandle`; freshness | Provenance is item-level and freshness depends partly on caller input. | Return atomic statements with source and transformation provenance; bind freshness to a compiler manifest and policy requirements. |
| H4 | relevance and confidence fields | The two fields are separate but not reproducible. | Add algorithm/version/scale/query scope for relevance and owner/basis/time/source for confidence. |
| H5 | decision flow; answer policy; workflow steps 10-12 | Partial-answer fitness and prose conflict detection cross into reasoning. | Report mechanical completeness and structured conflict state only; the answering-agent owner decides answer behavior. |
| H6 | operation contracts; response | Traverse, compare, and explain lack typed results. | Add a tagged result union or defer these operations from MVP. |
| H7 | workflow steps 6-11; limits; limiter | Limits are enforced too late. | Compute effective caps before reads; bound scans and joins; propagate deadline/cancellation; define byte and token accounting. |
| H8 | cache key | Key and cached object are incomplete. | Include schema, operation, selectors, field mask, and access-equivalence class; cache immutable authorized evidence only. |
| H9 | context view; compiler; residue | The neutral projection is asserted but not proven. | Define a one-way allowlisted compiler, opaque IDs, field provenance, leakage tests, manifest coverage, and owner approval gate. |
| H10 | answering-agent policy | Retrieved text is not explicitly untrusted. | Encode it as data and prohibit embedded instructions or tool requests from affecting agent behavior. |

## Boundary Verdict

- API design readiness: repairable `flag`.
- Implementation readiness: blocked until H1-H10 are repaired in the design
  handoff and the future plan preserves them.
- Production readiness: blocked by owner selection, field admission, policy,
  measurement, integration, and end-to-end witness gaps.

## Helper Receipt

```yaml
receipt:api-boundary-review:
  agent_id: api_boundary_reviewer
  role_id: api-boundary-reviewer
  spawn_status: spawned
  join_status: joined
  close_status: closed
  dispatch_id: 20260803T180648Z-agent-consultation-api
  step_id: s7
  capability_ref: interrogation
  capability_mode: refine-design-review
  status: flag
  artifacts:
    - stages/06-design.md
    - design-selection/selection-result.json
  validation: independent selector-level review completed; 0 critical and 10 high findings
  observer_status: not-configured
  blockers: no blocker to stage-8 repair; findings block implementation and production claims until repaired
  residue:
    - production identity and policy owners remain unselected
    - projection owner and admitted field set remain unapproved
    - budgets remain unmeasured
    - no end-to-end witness exists
  reroute: Distill Repair at s8, then recheck H1-H10 before Invoke Plan
  handoff_note: preserve the evidence-only API boundary and repair identity, response variants, provenance, mechanical status, early limits, cache isolation, and neutral projection proof
```

## Native Stage Receipt

- Stage: `s7`.
- Owning capability: `interrogation`.
- Capability handle: `.agents/skills/interrogation/SKILL.md`.
- Runtime surface: one native read-only helper plus parent join.
- Status: `complete`.
- Verdict: `flag`.
- Artifact: `stages/07-design-review.md`.
- Required role receipt: `receipt:api-boundary-review`, joined and closed.
- Observer status: not configured.

