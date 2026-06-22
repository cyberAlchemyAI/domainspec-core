# Anti-Patterns: Verification Weaver

## All-In-One Tester

Bad: `verification-weaver` claims to derive tests, run commands, validate UX,
map architecture, and promote evidence.

Repair: it routes to owners and joins receipts.

## Promotion By Parent Receipt

Bad: a `VERIFICATION-WEAVE` receipt marks a lane output as promoted.

Repair: use `promotion_action: none` or `candidate-request`; owner capability
must decide promotion.

## Private Fixture Leakage

Bad: public `arcanum` fixtures copy private DomainSpec or poker-team examples.

Repair: use synthetic public-safe fixtures that preserve the abstract shape.

## Generated-Only Proof

Bad: generated runtime output, run logs, or local observability files are treated
as source authority.

Repair: generated outputs may be evidence of a run, but durable contract
examples must be explicit fixtures.

## No-Oracle Formal Claim

Bad: a formal/testing target passes without deterministic derivation, fixture,
proof checker, browser evidence, human review, research run data, or explicit
gap.

Repair: block or flag with residue.

## UX Automation Overclaim

Bad: browser automation claims to prove comprehension, trust, delight, or
real-user success.

Repair: preserve human-review or user-study residue.

## Opaque Adapter

Bad: every command shape is hidden behind one generic adapter.

Repair: owner lanes declare explicit adapters and receipt contracts.

## Folder-Name Architecture

Bad: architecture claims are inferred from folder names alone.

Repair: route to `architecture-pattern-inventory` for source-backed mapping.
