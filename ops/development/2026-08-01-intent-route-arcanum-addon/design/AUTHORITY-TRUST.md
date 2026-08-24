# Authority and trust

| Decision | Accountable owner | Required evidence | Resolver effect |
|---|---|---|---|
| permit public extraction | private source owner plus public maintainer | digest-bound boundary/license/API receipt | none |
| accept canonical sigil | public Arcanum authority | candidate witness and public-boundary review | none |
| generate runtime package | Bootstrap owner | canonical source and closure digests | projection only |
| admit catalog projection | named capability and confirmed Dispatch owners | IDs, revisions, content digests, projector owner | read-only input |
| choose route | human through existing Dispatch/group/seat | confirmed canonical binding | resolver does not choose |
| bind workflow | existing orchestrator owner | separately confirmed binding | resolver cannot bind |
| authorize and execute | retained auth/runtime owners | their native gates and receipts | resolver cannot authorize or execute |
| retain artifacts | existing ACI journal owner | bound content-addressed fields | no resolver persistence |
| admit private integration | CAV2 authority | private conformance/promotion receipt | no public authority transfer |

Static and dynamic negative controls must prove zero Dispatch open/append,
zero ACI `dispatch-open`, zero compatibility fallback, zero workflow bind from
advice alone, and zero host spawn for every non-confirmed path.

The wire `receipt_digest` is renamed only conceptually as a disposition
integrity digest; compatibility retains the field name. It is never an
approval or authority receipt.

