# AlchLang local runtime and CLI — execution results

The confirmed local envelope is implemented end to end. A Markdown AlchLang
source can now be parsed, compiled, written to disk, packaged as a local npm
tarball and used to execute a guarded action through an injected adapter.

## Delivered

- Explicit Markdown/text parser for domain, owner, entity fields, actors,
  states/transitions, typed rules, boundaries, permissions, actions, events and
  examples.
- Predicate grammar for typed comparisons, `and`, `or`, `not`, `exists`,
  `absent`, `in` and `contains`.
- Fail-closed legacy predicate bridge: an opaque identifier executes only when
  the caller supplies its exact AST in a registry.
- Deterministic compiler and atomic local writer producing the generated
  TypeScript/JSON set, carrier and digest manifest.
- Action runtime that checks actor, inputs, rules, permissions, exact authority
  grant, adapter binding and emitted-event contract before returning success.
- Memory, local SQLite and HTTP adapters. HTTP requires an explicit allowlist;
  only injected and loopback behavior was tested.
- `domainspec build` and `domainspec run` executable surfaces.
- Deterministic registry compiler that exposes a pattern only when its meta-type,
  integration binding, generator and executable conformance dependencies close.
- Explicit `effect` and `performs` language clauses; effectful code generation is
  never inferred from an event or action name.
- Concrete `transactional-outbox/sqlite` generation with a port, SQLite
  implementation, migration, retry worker, executable tests and generation
  manifest.
- Local npm tarball `@cyberalchemy/domainspec-cli-candidate@0.2.0-candidate.0`.

## Demonstrated command

```bash
domainspec build customer-approval.md --out generated
```

The source-build and packed-tarball paths both produced 11 byte-identical files
with tree SHA-256
`1a702a7160785ba2809551cdd4f07602a7799825a3de7127c7238b23ed9ad74f`.

`ReleaseCredit` also executed with explicit `CreditOperator`, approved facts and
the `credit-release-authority` grant. The runtime recorded both its rule and
permission as `true` and emitted only the declared `credit-released` event.

## Evidence

| Surface | Result |
| --- | --- |
| Extension D65 source | PASS — 27 nodes, 22 relationships |
| Deterministic source manifest | `42356153974f62c380f002ab2f4850fd5d65fa2622cf355df68ed5f26a3246b5` |
| Registry closure | PASS — 2 available patterns; 0 blocked |
| Generated SQLite Outbox | PASS — atomic commit, rollback and at-least-once retry |
| Tests | PASS — 34 compiler tests plus 3 generated Outbox tests |
| TypeScript typecheck/build | PASS |
| Exact binding | `176c0918784a086bb7b291b37aaba6901b5c6de9646410ca2a1bb5d59924b188` |
| Implementation material tree | `8cd388e881635cc6b937542428beb56beece1129de997b9100441230ebd2c0ad` |
| Built dist tree | `8f9859846cd6c078f51c8775162e8c76d587753cd477d93b038fd3e45fa26a7b` |
| Local npm tarball | `bcfffe5fcb19666aad12e39c6aedb5176415b53510f887b0f63823bdf1b1c287` — 32 entries |
| Independent conformance | PASS — 22 checks |

## Limits

- This is a bounded formal grammar, not unrestricted natural-language parsing.
- SQLite uses the experimental built-in module in Node 26.
- The transactional Outbox binding is SQLite-specific and provides at-least-once
  delivery; it does not claim exactly-once delivery.
- No external database, credentials or remote HTTP endpoint was used.
- `npm pack` was performed locally; `npm publish` was not performed.
- No canonical language admission, owner acceptance of the extension, release,
  deployment, production-readiness or product-value claim is implied.

## Reproduce

```bash
python3 validate.py
python3 validate-work-pack.py
npm --prefix implementation test
npm --prefix implementation run typecheck
npm --prefix implementation run build
PATH=/home/vrondelli/.nvm/versions/node/v26.8.1/bin:$PATH \
  /home/vrondelli/projects/domainspec-core/projects/domainspec-v2/impl/node_modules/.bin/tsx \
  execution/scripts/validate-conformance.ts
```

Claim ceiling: source-local conformant registry/compiler/SQLite-Outbox and
local-runtime/CLI candidate. The patterns remain candidates rather than stable
architecture authority. No admission, external publication or effect authority.
