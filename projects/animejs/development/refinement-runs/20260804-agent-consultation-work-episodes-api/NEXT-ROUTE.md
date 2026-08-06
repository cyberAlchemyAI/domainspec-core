# Next Route: One Frozen Frontier, One Selected SWU

This run ends at a plan artifact. It does not start Task Session.

To avoid readiness-refresh loops, the downstream route must treat this package
as one immutable frontier:

1. run `work-pack-readiness-audit` once against the package digest recorded by
   this run;
2. approve or reject that exact digest;
3. select exactly one SWU, beginning with the recommended `SWU-AKVE-001`;
4. start `task-session` for only that SWU;
5. let Task Session recapture the live target presence/SHA-256 baseline and
   block only on real drift; and
6. use the terminal and Continuation Router receipts to advance to the unique
   successor without redesigning or replanning unchanged material.

A refresh is required only when the frozen Work Pack/design digest changes,
the declared target inventory drifts, or an owner/acceptance blocker appears.
Ordinary handoff from a passing terminal receipt to its declared successor is
already represented in the package and should not regenerate readiness.

This is a route contract, not an approval or runtime admission receipt.

