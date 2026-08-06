# Invoke Refresh: SWU-CAPI-000 `-03` Pass Closeout

- Mode: `refresh`
- Mutation mode: `apply-approved`
- Result: owner closeout `pass`; source Task Session remains `pass`
- Activation source: terminal continuation plus direct closeout authorization
- Scope: exactly `WORK-PACK.md` and the attempt-specific owner receipt

The refresh synchronized the accepted immutable
`wcli-20260805-node26-0.15.9-03` snapshot. SWU-CAPI-000 is complete, its
automatic route is consumed, and CAPI-B005 is resolved. CAPI-B003 remains open
only for a separately launched reader. SWU-CAPI-001 is dependency-ready but was
not selected or started.

The validated material package digest is
`d1f2fea85bcf2f0b7e02aae4223438483418f71e5262280f214aa401ee78fe98`.
The applied target hashes are:

- `WORK-PACK.md`: `72ca5698a2bbcba8dc70c707c5cfac914d36cebc4efeadea41df11cab49f1174`
- `SWU-CAPI-000.wcli-20260805-node26-0.15.9-03.refresh.json`: `b5a1a1abb012ba9db9ab5563b3ebf2ea3cf71f5de61eb758c54277044b6559d0`

No API code, canonical Craft source, prior attempt, network integration,
publication, deployment, promotion, or successor was changed or admitted.
