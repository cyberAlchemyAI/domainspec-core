# Stage 3: Define Review

## Structured Interview Result

- Target scope: `stages/02-define.md`.
- Mode: `refine-review`.
- Questions asked: 0.
- Decisions recorded: 8 review findings.
- Artifacts updated: none; repairs are assigned to Design and Distill Repair.
- Remaining ambiguities: three owner or measurement gaps, all non-blocking for
  design and blocking for production authorization.
- Verdict: `flag`.
- Next step: record the research decision, then distill the smallest coherent
  service boundary.

No user question was necessary. The confirmed route fixes the design target,
and the remaining unknowns belong to later owner decisions or measurement.
Inventing those answers would be less accurate than keeping them explicit.

## Review Findings

| ID | Finding | Severity | Required repair |
| --- | --- | --- | --- |
| DR-01 | `caller` needs a verifiable host-issued identity and policy digest, not caller-supplied labels. | high | Bind identity and policy before query normalization; deny when absent or stale. |
| DR-02 | Stable IDs must be logical record IDs, never repository paths. | high | Map safe IDs through the projection reader; reject path-like selectors. |
| DR-03 | Retrieval relevance and evidence confidence can be confused. | high | Use different fields, vocabularies, and agent instructions. |
| DR-04 | Freshness cannot be one response timestamp. | high | Bind projection version and source digests; return stale when a required digest drifts. |
| DR-05 | A denied response can leak that a protected record exists. | high | Return a policy-safe denial without protected identifiers, counts, or snippets. |
| DR-06 | Caching can cross tenants or policy versions. | high | Key caches by projection, policy digest, caller scope, normalized query, and limits; do not cache denials across identities. |
| DR-07 | `partial` is unsafe without an exact reason. | medium | Include missing classes, excluded IDs, limits hit, and whether a direct answer remains allowed. |
| DR-08 | The API could become an implicit reasoning engine if it generates conclusions. | high | Keep `compare` and `explain` to stored or deterministic record transformations; no conclusion, approval, or recommendation field. |

## Highest-discrimination Finding

DR-08 is the main boundary. If the service generates the user-facing conclusion,
retrieval, reasoning, and answer ownership collapse. The design must return
evidence and answer guidance only. The answering agent remains a separate
consumer whose output can be evaluated independently.

## Readiness Conditions For Design

- Access is checked before the query is resolved.
- A neutral projection, not private files, is the only query data source.
- The response type separates match score, evidence confidence, commitment
  status, freshness, and authority effect.
- Every non-success state has explicit answering-agent behavior.
- No endpoint can write or trigger protected work.

## Native Stage Receipt

- Stage: `s3`.
- Owning capability: `interrogation`.
- Capability handle: `.agents/skills/interrogation/SKILL.md`.
- Runtime surface: parent native Codex session.
- Requested mode: `refine-review`.
- Artifact: `stages/03-review.md`.
- Status: `complete`.
- Verdict: `flag` with bounded design repairs.
- Blockers: none for Design; all high findings must be checked at stage 7.
- Observer status: not configured.

