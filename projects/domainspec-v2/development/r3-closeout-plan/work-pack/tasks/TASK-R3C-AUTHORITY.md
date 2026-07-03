# TASK-R3C-AUTHORITY: Closeout, Craft, Observability, And Attestation

Layer: L3.
Slice: S-R3C-005.
Wave: [W3](../waves/W3.md).

## Objective

Keep the project control plane honest after execution and preserve the attestation boundary.

## Source Contracts

- `projects/domainspec-v2/.craft/ledger.yml`
- `projects/domainspec-v2/CRAFT.md`
- `.arcanum/observability/`
- `projects/domainspec-v2/authority/`

## Dependencies

Run after executed SWUs have receipts, or explicitly record which SWUs are deferred.

## Implementation Detail

Closeout must separate:

- R3A complete,
- downstream APE enforcement complete or still active,
- future relation/category-law routes,
- L2 attestation seal blocked or received.

## Smallest Working Units

### SWU-R3C-009

- Goal: sync Craft and observability after executed SWUs.
- Dependencies: completed/deferred SWU receipts.
- Write scope: `.craft/ledger.yml`, `CRAFT.md`, `.arcanum/observability/` only.
- Done criteria: active gaps/blockers reflect receipts; no stale R3-blocked wording in active surfaces.
- Acceptance evidence: YAML/JSONL parse and stale scan pass.
- Validation: `python3 -c` YAML parse; JSONL parse; `git diff --check`.
- Execution owner: local-fallback.
- Handoff note: do not edit historical receipts except with dated follow-up notes.

### SWU-R3C-010

- Goal: route L2 attestation.
- Dependencies: SWU-R3C-009.
- Write scope: attestation handoff artifact or blocker update.
- Done criteria: attestation receipt exists or blocker has exact closure condition.
- Acceptance evidence: receipt or explicit blocked handoff.
- Validation: manual review.
- Execution owner: manual.
- Handoff note: this can block final seal but not R3A relationship completion.

## Synchronization

If attestation remains unavailable, the result is `flag` with blocker preserved.
