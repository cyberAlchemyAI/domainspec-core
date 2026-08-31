# Independent Semantic Review Receipt

Review type: read-only semantic closure check
Result: `block` for operation-level FormalClaim admission
Candidate usefulness: `pass` for continuing business decision work
Files changed by reviewer: none

## Finding

The R3 path is valid in concept, but the specification does not define where
effect-bearing DENY grants come from when `AuthorizeRequest` decides. Existing
code and tests demonstrate one implementation choice; they cannot silently
settle business meaning.

## Recommended Proposition Shape

```text
For every AuthorizeRequest r, let DecisionGrantSet(r) be the complete set of
current grants applicable to r under the owner-selected carrier.

If DecisionGrantSet(r) contains an exact matching DENY grant, the decision is
DENY regardless of any matching ALLOW grant.
```

`DecisionGrantSet` must remain unresolved until the business/domain owner
selects its carrier, applicability, and currentness rules.

## Required Split

1. Carrier completeness: every applicable current DENY is visible to the
   operation's decision.
2. Deny precedence: a visible matching DENY beats matching ALLOW grants.
3. Forbidden outcome: a DENY maps to the operation's `FORBIDDEN` contract.
4. Non-trivial ALLOW control: no DENY plus an exact ALLOW returns ALLOW.

The first two are both required for operation-level R3. The third and fourth
come from neighboring postcondition/R2/policy commitments. A pure decision
claim is safe only as the smaller precedence subclaim.

## Excluded Residue

- wildcard correctness, which has a separate open contradiction;
- role/group DENY behavior;
- complete grant currentness and distributed snapshot semantics;
- canonical FormalClaim acceptance;
- deterministic obligation derivation and mutation evidence;
- EVF receipt, proof, or discharge; and
- security, release, deployment, or production readiness.

## Next Owner Route

Use `decision-gate` to select the DENY carrier. Then obtain exact formal-owner
assertion and independent business-owner fidelity acceptance before creating an
admitted `FormalClaimSourcePayload/v2` or canonical `derived_from` relations.
