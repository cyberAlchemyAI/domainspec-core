---
tags: [inventory, strategy-result, dispatch, subagents, review-change-request, html-builder, ide-extension]
node_type: synthesis
is_session: false
layer: strategy
nature: reference
status: closed
created: 2026-07-12
dispatch_id: 2026-07-12-html-builder-architecture-review
dispatch_type: review
working_folder: projects/ide-extension/development/html-builder-architecture-review/
sources: [projects/ide-extension/development/html-builder-architecture-review/attacks.md, projects/ide-extension/development/html-builder-architecture-review/findings.md, telemetry/agents/subagents-dispatch.yaml]
---

# IDE Extension HTML Builder Architecture Review Strategy Result

This non-authority Inventory read model records the closed architecture review
dispatch `2026-07-12-html-builder-architecture-review`. It preserves the
difference between demonstrated V0 defects and obligations for a future
incremental HTML-builder surface. It does not apply the change requests or
authorize a new API.

## Strategy Summary

**P1 trigger decision:** dispatch was justified by synthesis, isolation, and
parallel adversarial review. The proposal spans compatibility, operation
semantics, filesystem admission, effect authority, and later region-scoped
mutation, so a single linear review would not provide adequate tension.

**Goal:** review whether the existing complete-file canvas API can evolve into
an HTML builder and consolidator supporting whole-document operations first and
named regions later without changing the original API behavior.

## Lanes And Subagents

- `attackers`: Abramsky, Samson tested formal compatibility and operation laws;
  Ashby, W. Ross tested control, authority, and failure containment; Turing,
  Alan tested executable counterexamples and implementation mechanics.
- `synthesizer/writer`: Shannon, Claude consolidated the attacks and revised the
  candidate once after verifier and auditor returns.
- `verifiers`: Rittel, Horst tested scope and counterexamples; Schon, Donald
  tested architectural fit and definitions.
- `coverage-auditor`: Loregian, Fosco checked all five review targets and all
  attack classes, rejected the first candidate with five required revisions,
  then returned `ACCEPT`.

## Dependency Flow

- `attackers -> synthesizer`: sequential after robot talks.
- `synthesizer -> verifiers`: one bounded revision loop.
- `verifiers -> coverage-auditor`: sequential.
- `final_approver`: Loregian, Fosco.

## Gate And Ledger State

Two independent tension checks returned `PASS` and `PASS`. The human confirmed
the frozen dispatch, it was registered before working agents ran, seven agents
were spawned and closed, and the final auditor accepted the revised result.
Closeout uses `exit_reason: resolved`.

## Accepted Result

The existing V0 remains a complete-file publication surface. The accepted
evolution does not promote that surface in place. Instead, an explicitly
selected V0 revision derives a new `operations_v1` surface identity. The new
surface begins with whole-document `append`, `replace`, and `rebuild`
operations using revision compare-and-set, idempotent operation IDs, and
durable operation records. Named regions may later become an additive target on
that derived surface. Navigation and display refresh remain separate from
content transformation and do not create content revisions.

The review also retained two current V0 defect classes: canvas publication does
not satisfy the specification's approval boundary or the architecture's stated
receipt boundary, and lexical path containment permits an in-workspace symlink
to admit an external HTML file. Separate `stat()` and `readFile()` observations
were demoted to clarification/hardening; replay-integrity and same-byte metadata
claims were not retained as demonstrated V0 defects.

## Durable Outputs

- [Collected attacks](../../../projects/ide-extension/development/html-builder-architecture-review/attacks.md)
- [Accepted findings](../../../projects/ide-extension/development/html-builder-architecture-review/findings.md)

## Next Human Action

Resolve approval-versus-trusted-local publication and receipt semantics, then
route the accepted derived-surface model through Invoke design before planning
implementation. Realpath-safe V0 admission can be repaired independently.
