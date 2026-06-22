# Distill Repair

## Mode Result

- Mode: validate
- Verdict: pass
- Recomposition: pass
- Gap count: 3 non-blocking
- Next route: invoke plan

## Validated Unit

`auth-access-control-core`

## Repair Actions

| Issue | Repair |
| --- | --- |
| Design could be read as copying HTTP auth guard too. | Explicitly keep HTTP routes/guards outside the core package. |
| Bootstrap could leak generated password logging behavior. | Require bootstrap to return a report and leave logging to consumers. |
| Tests could require Vitest migration decision. | Carry as execution decision: port to `node:test` or add Vitest, but package check must pass. |
| Docs could remain adoption-only and lose source specification authority. | Add docs extraction and normalization as its own SWU before readiness audit. |

## Closure Check

- Responsibility: closed.
- Inputs/outputs: named.
- Dependency ports: named.
- Persistence default: Drizzle/Postgres.
- Tests: source test scaffold identified.
- Docs: source DomainSpec docs identified and routed into the package.
- Consumer recomposition: Body War/TROQAR and future services can import.

## Recomposition Proof

The selected unit can be implemented without Strava or browser cookies. Once
complete, Body War/TROQAR can import the package and add its own web transport
and provider modules. The extracted docs preserve the reusable auth contract
for future services without turning Poker Team routes into package authority.
This preserves the broader auth objective while keeping the first
implementation unit small enough for one Task Session work pack.

## Remaining Gaps

1. Test runner choice: port source tests to `node:test` or install Vitest.
2. Optional concrete helpers: decide during execution whether package includes
   `jsonwebtoken`/`bcrypt` infrastructure helpers or keeps only ports plus
   memory/Drizzle adapters.

Neither gap blocks the work-pack because the SWUs carry acceptance gates.

## Verdict

pass
