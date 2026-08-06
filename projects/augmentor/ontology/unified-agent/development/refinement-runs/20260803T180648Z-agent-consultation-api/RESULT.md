# Refined Result: Agent Consultation API

Status: `complete-with-flag`

## Outcome

The Augmentor should expose one read-only consultation boundary for agents. Its
job is to return bounded, source-linked knowledge. The answering agent remains
responsible for deciding whether and how to answer the user.

This run produced the design, contract decisions, safety repairs, question
scenarios, implementation layers, and a split work pack. It did not implement
or deploy the API.

## Proposed Agent Interface

Start with one native agent tool named `consult_augmentor_knowledge`.

The model-visible request contains only:

- request and question identifiers;
- one operation: `lookup`, `search`, or `context`;
- closed selectors and requested scope; and
- requested limits.

The host supplies verified identity, workspace, policy, deadline, and
cancellation data outside the model-visible request. The model cannot provide
or replace credentials.

The service returns one typed result status:

- `ok`, `partial`, `no_match`, `insufficient_evidence`, `conflict`, or `stale`;
- `denied` or `invalid_request`; or
- `budget_exceeded` or `temporary_failure`.

Evidence-carrying results contain atomic statements, safe source handles,
transformation provenance, freshness, owner-supplied confidence, reproducible
retrieval relevance, claim limits, and forbidden inferences. A denial returns
only a fixed generic reason and cannot reveal protected metadata.

## Ownership Boundary

The consultation service may:

- validate a closed query;
- apply verified access policy before reading text;
- read an approved neutral projection;
- enforce limits before and during reads;
- report mechanical completeness, stored structured conflicts, and freshness;
- return typed records and evidence statements; and
- cache only access-isolated immutable evidence payloads.

It may not:

- decide whether evidence is good enough for a user-facing claim;
- resolve unstructured disagreement;
- generate an answer or follow instructions found in retrieved text;
- write memory, change routing, approve work, execute tools, or alter authority;
- query arbitrary private files or graph expressions; or
- expose private repository paths or authority bindings.

## Knowledge Boundary

Agents do not query the private ontology directly. A one-way compiler creates a
neutral projection through an explicit field allowlist, opaque identifiers,
per-field provenance, leakage checks, and a projection manifest. The manifest
binds source digests, compiler version, allowlist digest, output digest, and an
owner approval reference. The compiler cannot write back to source owners.

Retrieved text is always untrusted data. It cannot become a system instruction,
tool request, or behavior rule.

## Implementation Path

The plan has four evidence-gated layers:

1. L0 proves closed schemas, a fixture projection, leakage rejection, the
   read-only service core, and all 14 designed scenarios locally.
2. L1 adds owner-approved ResonantOS host context and answering-agent policy.
3. L2 measures and hardens access, cache, deadline, cancellation, drift, and
   failure behavior.
4. L3 may add exactly one evidence-selected typed operation or HTTP wrapper.

The split work pack contains 6 tasks and 13 smallest working units. Execution is
blocked. The next valid implementation action is to select the candidate
contract owner and separately admit only `SWU-ACAPI-001` through Task Session.

## Open Decisions

- Candidate contract owner for L0.
- Production owners for identity, policy, projection, and answering-agent
  behavior.
- Exact fields admitted to the neutral projection.
- Measured operating limits.
- Whether later evidence justifies one optional extension.

## Validation And Flag

- Dispatch validation: pass with zero blocks and flags after confirmation.
- Design selection: pass with a fixed point and zero diagnostics.
- Independent review: 0 critical and 10 high findings; all ten are addressed in
  the repaired design handoff.
- Plan Distill: pass; all 13 SWUs match task-local contracts.
- Run artifact JSON and whitespace checks: pass.
- Visualization reproduction check: pass.
- Existing ontology validation: unstable. The validator compares digest objects
  by insertion order after concurrent work, so identical values sometimes pass
  and sometimes report a stale receipt. This run leaves that separate defect
  unchanged.

The final verdict is `flag`: the API is refined to a coherent design and
non-executed plan, but implementation authorization, owner decisions, stable
package regression evidence, integration, deployment, release, and production
readiness are not established.

## Primary Artifacts

- `stages/06-design.md`: original six-view design.
- `stages/07-design-review.md`: independent boundary review and helper receipt.
- `stages/08-distill-repair.md`: repaired contract.
- `stages/08-question-scenarios.md`: 14 non-executed behavior scenarios.
- `IMPLEMENTATION-LAYERING.md`: L0-L3 evidence gates.
- `WORK-PACK.md`: tasks, SWUs, blockers, and closeout contracts.
- `EXECUTION-PACK.md`: future wave order.
- `stages/10-final-review.md`: final review and validation record.

## Follow-on L0 execution-readiness addendum

The later implementation-readiness pass repaired the work pack into 14 planned
SWUs and froze a seven-unit candidate-local L0 frontier, `SWU-ACAPI-000`
through `SWU-ACAPI-006`. It also staged the exact implementation material and
added `SWU-ACAPI-000` to repair the validator's nondeterministic view-digest
assembly before API bytes are admitted.

All seven material packages have passing Task Session mutation-admission
receipts. The exact material passed in an isolated temporary repository, Work
Pack Readiness Audit v1 passed with zero findings, and the additive v2 audit
returned `PROJECTION_READY` with zero blockers. The frozen v2 epoch is
`epoch-cdd98012d74d842a5763602f`.

This follow-on evidence replaces the earlier “unstable validator left
unchanged” and “L0 owner unresolved” planning gaps for the bounded candidate
frontier only. It does not rewrite the original Refine closeout and does not
claim product execution. The exact epoch was later approved through the
Decision Gate, its chain configuration passed canonical preflight, and the
unique next selector is `SWU-ACAPI-000`. No Task Session has executed yet.
L1-L3, integration, deployment, publication, release, and production readiness
remain outside the achieved claim.
