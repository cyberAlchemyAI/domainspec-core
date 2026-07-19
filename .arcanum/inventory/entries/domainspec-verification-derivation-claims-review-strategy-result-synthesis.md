---
tags: [inventory, strategy-result, dispatch, subagents, review-change-request, audit, claim-le-proof, domainspec, formalization, determinism, observability]
node_type: synthesis
is_session: false
layer: strategy
nature: reference
status: closed
created: 2026-07-17
dispatch_id: 2026-07-17-verification-derivation-claims-review
dispatch_type: review
working_folder: research/domainspec/2026-07-17-verification-derivation-claims-review/
sources: [research/domainspec/2026-07-17-verification-derivation-claims-review/attacks.md, research/domainspec/2026-07-17-verification-derivation-claims-review/findings.md, research/projects/domainspec/papers/domainspec-paper.md, research/projects/domainspec/claims/CLAIMS.md, research/projects/domainspec/experiments/E1-derivation-determinism/protocol.md, implementation/domainspec/OBSERVABILITY.md, telemetry/agents/subagents-dispatch.yaml]
---

# DomainSpec Verification-Derivation Claims Review Strategy Result

This non-authority Inventory read model records the accepted review dispatch
`2026-07-17-verification-derivation-claims-review`. It does not change the paper,
the claims catalog, the observability specification, the undisclosed deterministic
engine, or any DomainSpec definition.

## P1 Trigger and Strategy

Dispatch was warranted by synthesis, context protection, isolation, and parallelism.
The target combined formal definitions, rule catalogs, cardinality equations,
observability semantics, evidence status, and alert policy; independent attacks could
run concurrently and had to be verified before synthesis.

The confirmed lanes were:

1. Three whole-corpus attackers in parallel with robot-talks:
   - Abramsky, Samson — formal semantics and fidelity/governance;
   - van Lamsweerde, Axel — computational enumeration and traceability;
   - Ashby, W. Ross — adversarial systems, operability, and gaming.
2. Tarski, Alfred — one writer/synthesizer that reconciled initial and final attacker
   positions without majority voting.
3. Two parallel skeptics in a bounded zig-zag:
   - Gödel, Kurt — definitional verification;
   - Popper, Karl — minimal-counterexample verification.
4. Loregian, Fosco — dedicated coverage auditor and final approver.

Dependency flow was `attackers → synthesizer ↔ verifiers → coverage auditor`, with one
conditional feedback edge to attackers. The feedback edge did not fire. The verifier
zig-zag converged in its second turn with `NO OBJECTION` / `NO OBJECTION`.

## Gate and Ledger State

- Check-tension gate: `PASS` / `PASS` from two independent gate agents.
- Human confirmation: explicit `confirmed`; the sheet then froze.
- Registration: one schema `0.6.0` dispatch row appended through the deterministic
  appender.
- Closeout: one close row appended with `exit_reason: resolved`, seven registered
  agents, zero helpers, and one whole-dispatch loop.
- Final approval: `ACCEPT` from the dedicated auditor.

## Accepted Result

The target verdict is **FIX** with seven **MAJOR** findings and no CRITICAL or MINOR
findings. The review preserves the narrow pure-function proposition and the reported
byte-stable backend engine, but rejects stronger inference to exact LLM reproducibility,
independent public executability, additive set cardinality, exhaustive test/monitor
symmetry, uniform observability evaluation, and layer-determined alert severity.

The seven verified findings are:

1. the section does not define an independently executable derivation over its declared
   graph input;
2. abstract extensional determinism does not justify exact reproducibility on the LLM
   path;
3. exact cardinality and composition need a stated obligation identity/disjointness
   invariant;
4. the text does not provide the advertised computable 20-rule count;
5. the listed catalogs refute exhaustive behavioral-coverage symmetry;
6. observability derivation is substantial but not uniformly specified across all sixteen
   rules;
7. layer-wide severity universals conflict with rule-level severity policy.

## Verified Change Requests

1. Separate claims for the abstract calculus, deterministic backend engine, and LLM
   generator.
2. Publish the derivation interface: document-to-graph encoding or explicit document
   input, typed rule signatures, canonical obligation equality, and typed composition.
3. Replace ordinary-union cardinality assumptions with a defined tagged or multiset
   algebra.
4. Distinguish exact counts, complete minima, and partial floors for all twenty rules.
5. Retain co-origin traceability but require an explicit property-level `T↔O` relation
   before claiming exhaustive symmetry.
6. Normalize O-rule instruments/cardinalities and close correlation, denominator,
   threshold/window, and missing-telemetry gaps.
7. Move severity authority from metric layers to one rule-level decision table.
8. Reconcile E1's exact `1.0` criterion with C2's `>=0.95` research threshold.

## Durable Outputs

- [Collected attacks and verifier transcript](../../../research/domainspec/2026-07-17-verification-derivation-claims-review/attacks.md)
- [Auditor-accepted findings](../../../research/domainspec/2026-07-17-verification-derivation-claims-review/findings.md)

## Residue and Next Human Action

No target source was changed. The paper owner must decide which accepted requests to
route through the paper/claims/observability owners. E1 remains unrun for the LLM path;
the backend engine algorithm remains undisclosed; and this Inventory entry cannot promote
any claim, definition, implementation, or observability contract.

Next human action: route a bounded paper repair through the owning lifecycle, preserving
the engine-specific KEEP claim while narrowing the LLM, cardinality, symmetry, and
severity statements to what the evidence sustains.
