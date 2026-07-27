# TASK-ILP-009: Generic Live Topology Proof

## Objective

Demonstrate, with no private product fixture, that one authored-valid selected
unit reaches Task Session admission without a repair Refresh while exact drift
still blocks an obsolete join.

- Layer/slice/wave: L3 / S3 / W3
- Lifecycle owners: bounded Task Session plus Spellcraft, Sigil Development,
  and transition owner
- Dependencies: SWU-ILP-008A and SWU-ILP-008B
- Source contracts: all prior lifecycle receipts, `../../DESIGN.md`
- Write scope:
  - generic synthetic fixture/run paths approved by the public lifecycle owner;
  - private session evidence under
    `work-pack/session-evidence/SWU-ILP-009/`;
  - no private witness copied into public source

## Algorithm

1. Create or select a generic one-file reversible mutation SWU.
2. Run Invoke Plan to authored pass and produce one epoch.
3. Produce and validate the applicable mode contract.
4. Admit `handoff_ready` through the transition owner.
5. Run one Task Session and prove live admission before first write.
6. Apply the bounded mutation and validate it.
7. Complete exact closeout and terminal transition without any repair Refresh
   before admission.
8. Independently alter a declared projection copy or synthetic join target.
9. Prove the old exact join blocks.
10. Classify impact and prove the classifier cannot override the exact block.
11. Preserve the complete receipt chain and observational progress event.

## Smallest Working Unit

### SWU-ILP-009

- Primary behavior: prove the repaired lifecycle topology.
- Acceptance boundary: one live receipt chain plus retained exact-drift
  negative control.
- Candidate children: happy path; drift negative.
- Retained rationale: the claim is specifically that progress improves without
  weakening the existing safety property; either half alone is insufficient.
- Execution owner: `local-fallback` via one bounded Task Session.
- Done criteria:
  - ready/admitted/mutation/execution/closeout/terminal receipts bind one epoch;
  - no pre-admission repair Refresh occurs;
  - exact obsolete join rejects;
  - progress event references admitted transition IDs;
  - public fixture contains no private product name/path/evidence.
- Validation: owner-approved live run command plus exact receipt audit.
- Handoff context: all W1-W3 receipts and `../shared/TRACEABILITY.md`.

## Closeout

Use `../shared/CLOSEOUT-CONTRACT.md`. Live evidence does not itself promote or
publish the capability.

