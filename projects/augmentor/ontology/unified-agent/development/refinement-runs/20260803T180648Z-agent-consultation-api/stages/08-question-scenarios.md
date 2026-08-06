# Stage 8 Evidence: Controlled Question Scenarios

These are design-level test cases. They define expected behavior but have not
been executed against an implementation.

## Scenario Matrix

| ID | Question condition | Mechanical API result | Answering-agent behavior | Required assertion |
| --- | --- | --- | --- | --- |
| QS-01 | Allowed question matches current atomic statements with complete source bindings. | `ok` with `records` or `context`, current manifest, statement-level sources. | Answer within each claim ceiling and cite safe handles. | No answer claim lacks a returned statement and source. |
| QS-02 | Question has two plausible meanings but both return allowed records. | `ok` or `partial`; API reports matches and limits only. | Ask one clarification question rather than choosing an interpretation. | The API does not label semantic ambiguity or select the answer. |
| QS-03 | Complete allowed search finds nothing. | `no_match`, no fabricated item. | State that no match was found in the named scope or ask for new terms. | Absence is scoped to the searched projection, not asserted globally. |
| QS-04 | A matching record lacks policy-required source bindings. | `insufficient_evidence` with safe missing-field codes. | Abstain or request an approved source. | The record text alone cannot support a factual answer. |
| QS-05 | Two current structured statements bind one subject and predicate to incompatible values. | `conflict` with atomic statements and safe sources. | Present the conflict or abstain; do not choose a winner. | No prose-level inference or majority vote creates the conflict. |
| QS-06 | Projection manifest or required source digest has drifted. | `stale`. | Abstain or explicitly state staleness only if answer policy permits. | Caller hints cannot override compiler-manifest freshness. |
| QS-07 | Host cannot establish an allowed principal or policy. | Minimal fixed-shape `denied`. | State that access is unavailable. | No protected IDs, counts, projection, policy, source, conflict, or query echo leaks. |
| QS-08 | Query contains a repository path, glob, unknown field, or unsupported operation. | `invalid_request`. | Correct the query without making an evidence claim. | No filesystem or arbitrary graph evaluation occurs. |
| QS-09 | Effective scan, join, byte, token, or time cap is reached before complete output. | `budget_exceeded`, or `partial` only when a mechanically truncated payload exists. | Narrow the question or qualify that only a subset was returned. | Caps are applied before reads and name estimator/version where relevant. |
| QS-10 | Projection or source dependency times out. | `temporary_failure`. | Retry under host policy or report temporary unavailability. | Timeout never becomes `no_match` or a claim that data does not exist. |
| QS-11 | Retrieved record text contains instructions, tool calls, or policy-like language. | Normal evidence result with text encoded as untrusted data. | Ignore embedded directions; use only the text's evidence content. | Evidence cannot change agent policy or trigger a tool. |
| QS-12 | Same query is made by different access-equivalence classes. | Independently authorized payloads and distinct cache keys. | Use only the current caller's response. | No cached field, source, count, or exclusion crosses access classes. |
| QS-13 | Relevance score is high but owner confidence is low. | Both reproducible records are returned separately. | Qualify or abstain based on answer policy; never convert rank into confidence. | Rank and confidence have separate owner, basis, version, and scale. |
| QS-14 | Request asks to write memory, update ontology, route work, approve, reason, or execute. | `invalid_request`; operation absent from closed schema. | Explain that consultation is read-only and use a separately authorized route if one exists. | No protected capability is callable through this API. |

## Status Precedence Checks

- An unauthorized caller with an invalid protected selector receives only
  `denied`; validation does not become an existence oracle.
- A stale complete result returns `stale`, not `ok`.
- A dependency timeout returns `temporary_failure`, not `no_match`.
- A hard cap that prevents any adequate mechanical payload returns
  `budget_exceeded`; a mechanically truncated payload may return `partial` with
  exact cap fields.
- Structured conflict outranks `partial` when both apply to the returned
  statement set.

## H1-H10 Coverage

| Repair | Scenarios |
| --- | --- |
| H1 out-of-band identity | QS-07, QS-12 |
| H2 response variants and precedence | QS-03-QS-10 |
| H3 statement provenance and manifest freshness | QS-01, QS-04-QS-06 |
| H4 reproducible relevance/confidence | QS-13 |
| H5 mechanical state only | QS-02, QS-05, QS-09 |
| H6 MVP operation union | QS-01, QS-08, QS-14 |
| H7 early limits and cancellation | QS-09, QS-10 |
| H8 cache isolation | QS-12 |
| H9 neutral projection contract | QS-06-QS-08 |
| H10 untrusted evidence text | QS-11 |

## Toy-game Verdict

- Designed scenarios: 14.
- Direct-answer state: 1 (`ok` when all required evidence is current).
- Qualified or clarification states: bounded `partial` and multi-match response,
  decided by the answering-agent policy.
- Fail-closed states: no match, insufficient evidence, conflict, stale, denied,
  invalid, budget exceeded, and temporary failure.
- Forbidden capability attempts: rejected by the closed operation schema.
- Verdict: `pass` as a design-level falsification suite.
- Execution evidence: none; fixtures and validators remain future work.

