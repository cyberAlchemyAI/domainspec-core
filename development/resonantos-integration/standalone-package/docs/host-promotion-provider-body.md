# Host Promotion Provider Body Contract

## Status

Specification only. The provider body is not implemented in this package.

## Responsibility

The host-side trusted-write provider body runs behind the host's existing promotion seam. It must
not be implemented in an intake-only or portable read/write shim.

## Inputs

- approved Review Queue artifact,
- decision receipt,
- source candidate,
- scope tag,
- promotion owner,
- validation result,
- target trusted-write destination.

## Outputs

- trusted write result,
- audit receipt,
- failure receipt when blocked,
- residue entry when validation is incomplete.

## Ordered Rules

1. Load the approved review artifact.
2. Verify the decision is `approve`.
3. Verify the promotion owner is allowed to authorize this target.
4. Verify the candidate has exactly one scope tag.
5. Verify source references and validation receipts exist.
6. Refuse promotion when any required field is missing.
7. Perform trusted write through the host boundary only.
8. Emit an audit receipt.

## Failure Modes

- missing approval,
- unsupported scope tag,
- missing source reference,
- owner mismatch,
- validation missing or failed,
- attempted trusted write outside host boundary.

## Validation

Provider implementation must include tests for approve, reject, escalate, missing source, owner
mismatch, and attempted portable-layer trusted write.
