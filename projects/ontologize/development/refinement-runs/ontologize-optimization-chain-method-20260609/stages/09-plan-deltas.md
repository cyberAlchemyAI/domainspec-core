# Stage 09 — Plan Deltas

## Plan changes

- `SPEC.md`: add R-G for optimization chains.
- `DESIGN.md`: add G-chain and insert optimization chains into artifact flow.
- `PLAN.md`: update IDS-3 to produce a chain fixture.
- `WORK-PACK.md`: update T5 proof harness to require schema-valid optimization chain.
- `NEXT.md`: require chain expression during pilot thin slices.

## Execution impact

T5 now has an additional acceptance check: validate the optimization-chain fixture against
`schemas/optimization-chain-method.schema.json`.
