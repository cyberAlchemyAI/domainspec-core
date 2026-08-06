# Stage 08 — Distill Repair

## Repair result

Verdict: `pass-with-residue`. The smallest coherent L0 remains a private,
read-only consultation API over one fully verified derived snapshot. The repair
does not enlarge it into a refresh, search, replacement, or recovery system.

## Accepted repairs

1. Row routes now have distinct list/read actions, opaque resources, and a fixed
   authorization-before-observation order.
2. Space identifiers use a byte-exact, secret-keyed, snapshot-local HMAC;
   private paths are not testable from IDs without the key.
3. Exact content digests, sizes, and paths are split from base metadata by
   provenance/path permissions.
4. Space and row cursors bind principal/session, policy revision, visible set,
   snapshot, route scope, limit, position, version, expiry, and integrity.
5. Resource ceilings are mandatory and candidate defaults are explicit.
6. Error precedence, concealed denials, duplicate behavior, and schema behavior
   are deterministic.
7. Cache ETags and the explicit snapshot precondition are separate mechanisms.
8. Freshness compares each current source digest with its manifest entry and is
   valid only under a complete, authorized, unexpired observation.
9. WaveDB evidence is narrowed to same-process reopen and expected-key closure.
10. Handles are called logically immutable; any runtime anomaly invalidates the
    whole handle. Builder/service overlap is prohibited.
11. Replacement, recovery, and stronger durability remain outside L0.

## Distill rounds

Round 1 proposed absorbing a builder, source observer, replacement protocol,
and recovery path so the runtime critic's operational gaps could be closed.
Round 1 balancing rejected that expansion: those effects require different
owners and evidence, and would destroy the read-only API unit.

Round 2 retained only the consultation boundary and converted unsupported
operational claims into explicit prohibitions and deployment prerequisites. The
unit survives: an authorized caller can consult exact manifest-bound bytes while
every refresh, mutation, publication, replacement, and recovery effect stays
outside it.

## Validation ceiling

The Markdown contracts now answer every critic finding, but this is design
validation only. HMAC vectors, cursor fixtures, schemas, adapters, policy ports,
resource-limit tests, separate-process WaveDB reopen, concurrency experiments,
and HTTP tests do not yet exist. The design is suitable for planning, not for an
implementation-ready or deployment-ready claim.
