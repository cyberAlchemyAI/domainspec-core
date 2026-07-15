# Plan Transport

## Receipt

- Invoke mode: plan.
- Result: split, high-complexity work-pack created.
- Planning gate: pass for the selected review-only SWU.
- Selected unit: `SWU-SGRM-006-R1`.
- Active layer: L0.
- Mutation performed: planning package only.
- Authority/Craft/implementation mutation: none.
- Production authorization: false.

## Next Route

1. Review this plan and separately authorize execution/registration.
2. Register or link this package under `CTX-DSV2-FIRST-PRODUCTION-RELEASE` without advancing FPR state.
3. Run Task Session for `SWU-SGRM-006-R1`; Context Builder creates the strict runtime pack from its selectors.
4. If the disposition packet has no active-reference finding, select `SWU-SGRM-007-R1`.
5. After the retry guard receipt passes, select `SWU-FPR01-001`.

## Stop Conditions

- Any match is active authority, implementation, or runnable plan content.
- A required owner decision is missing.
- A task would mutate a source outside its declared write scope.
- A generated artifact is treated as semantic or continuation authority.
- A downstream step tries to bypass a missing predecessor receipt.

## Registration Boundary

This Invoke run deliberately did not edit `.craft/ledger.yml`. Craft registration is a separate state mutation and must preserve `FPR-01` as the parent next move until the guard retry and FPR-01 receipt actually pass.

