# TASK-VTM-005 - Integration, Validation, And Readiness

## Objective

Validate the view-triad method pilot, propose safe integration with optimization chains and deliverables, and produce readiness evidence for a second run.

## Layer And Slice

- Layer: L2/L3.
- Slice: S4.
- SWU: SWU-VTM-005.

## Source Contracts

- [OPTIMIZATION-CHAIN-METHOD.md](../../../../OPTIMIZATION-CHAIN-METHOD.md)
- [BRANCH-MATERIALIZATION.md](../../BRANCH-MATERIALIZATION.md)
- [SKILL-ROUTING.md](../../SKILL-ROUTING.md)
- Pilot triad artifacts from TASK-VTM-002 through TASK-VTM-004.

## Implementation Detail

Algorithm:

1. Check system-view: verdicts stated count must be 0; every stance has exactly one engineer-view target or explicit blocker.
2. Check engineer-view: every row has status and authority; RESOLVED rows have verified authority.
3. Check ontology-view: every term/edge has source and legality status; forbidden relationships have type or guard rationale.
4. Check branch materialization: B1/B2/B3/B4 register rows are covered or blocked; B3 run-context record is complete; B4 bridge ledger respects the edge catalog and authority map.
5. Trace one sample BI claim through optimization chain, branch register, and the triad.
6. Produce integration proposal for product docs; do not apply without owner approval.
7. Emit readiness recommendation: second safe corpus, client pilot, or remediation.

## Smallest Working Units

### SWU-VTM-005

- Goal: produce `view-triad/validation-report.md` and integration proposal.
- Dependencies: SWU-VTM-004.
- Write scope: proposed `projects/ontologize/view-triad/validation-report.md`; proposed patches only for product-facing docs.
- Done criteria:
  - validation report covers branch coverage, stance coverage, authority verification, B3 run-context, B4 bridge ledger, typed ontology, no-double-decision, and claim trace;
  - integration proposal identifies exact docs/headings to patch or explicitly defers them;
  - readiness route is selected.
- Acceptance evidence: validation report with pass/flag/block status and next route.
- Validation surface: manual review plus `rg` checks for duplicate verdict or definition text if patches are proposed.
- Execution owner: local-fallback.
- Handoff note: route unresolved product-facing changes through owner approval or `domainspec-decision-gate`.

## Synchronization

Update [WORK-PACK.md](../../WORK-PACK.md) and emit `domainspec-emit-signals` only after actual view authoring has occurred.
