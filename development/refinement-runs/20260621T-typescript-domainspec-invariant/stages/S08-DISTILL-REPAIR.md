# S08 - Distill Repair

Owner: `distill`
Mode: `validate`
Verdict: `pass`

## Validation Target

Validate the design before planning:

- selected unit: `SWU-AUTH-001`,
- recomposition target: full auth/user-management TypeScript package and Body War Strava login,
- hidden gaps: Body War Python consumer, production store, Strava secrets, invariant enforcement.

## Repair Matrix

| Gap | Repair |
| --- | --- |
| Body War still imports Python auth | Add `SWU-BW-001` to replace consumer auth boundary after package baseline/use-cases exist. |
| TypeScript invariant could stay prose-only | Add `SWU-INV-001` for `tools/check-runtime-language-policy.sh` and policy doc. |
| Strava could be mixed into auth domain | Keep Strava in provider module; domain owns provider-account abstractions, infrastructure owns HTTP. |
| Package could overbuild production storage too early | L0/L1 use memory/JSON adapters; L2 plans durable store/encryption. |
| Tasks could be too broad | Split into SWUs with one write scope and validation surface each. |

## Distill Validation

| Check | Result | Evidence Or Gap |
| --- | --- | --- |
| Smallest coherent unit | pass | `SWU-AUTH-001` establishes language/package boundary first. |
| Recomposition proof | pass | Later SWUs build domain, application, infrastructure, interface, consumer integration, and invariant checks. |
| Hidden acceptance-critical gaps | pass | Body War and invariant enforcement represented as named SWUs. |
| Deferred complexity | pass | Durable production store and live Strava smoke are assigned to L2/L3. |
| Navigation to first executable unit | pass | Start with `SWU-AUTH-001`. |

## Distill Result

- Mode and budget: validate
- Verdict: pass
- Current smallest coherent unit: `SWU-AUTH-001`
- Tension ledger: TypeScript migration vs Body War current Python runtime remains visible but non-blocking for planning
- Next route: invoke plan
