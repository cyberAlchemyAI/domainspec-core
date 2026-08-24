# IRO-001 Decision Gate Result

- Target scope: `IRO-001-PUBLIC-BOUNDARY-BINDINGS`
- Result: `PASS`
- Decisions resolved: `1`
- Blockers remaining: `0`
- Admissibility routing: `gate`
- Selected option: `OPT-BIND-EXACT`
- Selection source: direct user message from Vladimir Vrondelli
- Admissibility receipt: `OPTION-ADMISSIBILITY-RECEIPT.json`
- Decision artifact: `DECISION.json`
- Override: not requested
- Authority effect: `none`
- Next step: project `SWU-IRO-002`, then pause for its separate candidate-mutation approval

## Bound seams

1. Public extraction is a fresh behavior-only, public-safe candidate under
   `candidate-sigil/`; private implementation remains read-only comparison
   evidence and canonical Arcanum remains separately gated.
2. The canonical capability is `intent-route-resolver` under
   `arcanum/arcana/intent-route-resolver/`, using the three fixed `@1`
   protocols, lowercase SHA-256 identities, and Arcanum's PolyForm
   Noncommercial 1.0.0 license and Required Notice.
3. Catalog projection is consumer-owned, exact, digest-bound, and read-only;
   it cannot discover, repair, register, persist, approve, dispatch, bind, or
   execute.
4. Request normalization is runtime-owned and either constructs
   `intent-route.request@1` from captured input or returns a typed rejection;
   semantic inference and compatibility fallback are forbidden.
5. Private ACI compatibility may reference only content-addressed request and
   disposition artifact refs/digests. Exact private implementation scope and
   field admission remain gated at IRO-009.
6. The disposable witness locator is
   `/home/vrondelli/projects/intent-route-resolver-disposable-consumer`.
   Repository creation remains gated at IRO-006.

No code, public source, generated package, consumer repository, ResonantOS,
orchestrator, or private runtime mutation is authorized by this decision.
