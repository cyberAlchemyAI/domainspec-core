# Anime.js Agent API Design Review Strategy

## P1 trigger

Dispatch. The API has two independent failure surfaces: authority leakage across read/write/projection boundaries, and state-integrity failure across append/replay/recovery. Both need isolated attacks against the same exact design bytes and must join before repair.

## Lanes

- `Popper, Karl`: scope-authority attack.
- `Quine, Willard Van Orman`: counter-example state-integrity attack.

Both are read-only skeptics. Neither owns design changes or final approval. The parent consumes their returns, persists the review evidence, repairs the design, and owns the final Work Pack.

## Inventory effect

Inventory is lookup-ready and points to the earlier Anime.js vault and Augmentor owner-preserving architecture. Direct current bytes remain decisive. No external research is required or permitted.

## Gates

1. schema-0.8.0 readiness on the exact sheet;
2. two independent check-tension PASS verdicts on the exact digest;
3. confirmation carried only because the sheet is a faithful deterministic serialization of the already-confirmed two-critic material strategy;
4. append one registration row;
5. spawn both reviewers, join both, preserve receipts;
6. append one close row.

## Boundaries

No reviewer writes files, browses, mutates Git, changes the vault or consumer, performs deployment, or claims planned fixtures executed. Review acceptance means the requested attacks completed; it does not mean the reviewed design passed.
