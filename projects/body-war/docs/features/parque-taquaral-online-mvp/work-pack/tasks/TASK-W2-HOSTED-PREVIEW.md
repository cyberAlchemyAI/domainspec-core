# TASK-W2-HOSTED-PREVIEW

## Objective

Deploy the TypeScript MVP to a hosted preview URL with sealed secrets and
managed storage.

## Layer And Slice

- Layer: L2.
- Slice: S-003.
- Wave: W2.

## Source Contracts

- `../../DEPLOYMENT-SECURITY.md`
- `../../TEST-SPEC.md`
- `../../interfaces.md`

## Dependencies

- W1 app flow passes.
- Hosted provider and storage are configured.

## Smallest Working Units

| SWU | Goal | Write Scope | Done Criteria | Validation |
| --- | --- | --- | --- | --- |
| SWU-BWPT-009 | Deploy hosted preview and validate callback/storage. | Deploy config, env docs, provider settings | Hosted URL loads, Strava callback returns, connected state appears without token exposure. | PTV-001..PTV-003 and no-secret check. |

## Implementation Detail

- Use provider secret store for Strava client secret and session secret.
- Use managed storage for token references, submissions, controller state, and
  audit metadata.
- Do not write raw tokens or private activity payloads to repository docs.

## Blockers

Blocked until W1 passes.

