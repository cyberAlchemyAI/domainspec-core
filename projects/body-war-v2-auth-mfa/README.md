Archive migration has been removed. See [current next steps](NEXT-STEPS.md) and
[removal scope](REMOVAL-PLAN.md). The pilot uses ordinary activity evidence.

# Body War v2 — TROQAR pilot rebuild

Candidate local repository. Private. Product approval and operational authority: none.

This rebuild preserves the existing pilot: Strava-only login/profile, activity
consultation, suggested tracks, explicit consent, redacted evidence, logout,
Postgres migrations and browser UI. Local validation uses fake Strava exclusively.
No account data, tokens, GPS histories or runtime stores were imported.

The pilot is described by [body-war.alch](body-war.alch), eight imported application
modules and the existing [consent model](model/pilot.alch): ten `.alch` files.
AlchLang lowers the candidate `bound-application-v1` syntax into a shared
[application ontology input](model/application-ontology.json). DomainSpec checks
and generates it through one backend, emitting the [compiled view](model/system-ontology.json), HTTP dispatcher,
authorization calls, domain types, JSON success-response guards, lifecycle,
redaction projection, defaults and browser route/view configuration.

Current API routes are modeled; archive migration and legacy submission endpoints are removed.
Identity, activities, tracks, evidence, six storage bindings, UI and TDE/EVF/ORODI
have explicit declarations. OAuth, crypto, database IO, migrations, HTTP handlers
and browser rendering are source-bound adapters. Rebuilding needs both `.alch`
and these adapter sources; it does not synthesize arbitrary application logic.
The consent submodel goes through the actual DomainSpec checked graph and direct
CLI verification. The application profile now belongs to the DomainSpec compiler
as a candidate extension; its existing frozen meta-type catalog is unchanged.
The native `application-check` / `application-build` commands consume JSON without
importing AlchLang. Byte-equivalence and live mutation tests exercise both paths.

## Run locally

Requires Node 26.8.1, npm, Docker with Compose for Postgres tests, and the local
DomainSpec/CyberAlchemy sources. `npm ci --ignore-scripts` installs pinned packages.

```bash
npm run build:model
npm run build
npm test
npm run test:postgres
npm run test:ui
npm run validate:pilot
```

`npm run validate:pilot` performs the complete supported local rebuild and test
campaign, collects all stage failures, binds source and artifact hashes, and reports
remaining coverage separately. `npm run validate` runs the same campaign and returns
exit 2 when whole-flow coverage remains incomplete. Neither command manufactures
product approval or an enterprise compliance result.

To check the shared JSON input directly after `build:model`:

```bash
node .tools/compiler/dist/cli/main.js application-check \
  "$PWD/model/application-ontology.json" --root "$PWD"
```

`application-build <absolute-json> --root <absolute-app-root> --target-root
<absolute-output>` requires an absent target matching the ontology's authored
output path. The compiler rejects stale bound sources and unsafe source/core paths.
The JSON document is an explicit compiler input, not a signed assertion that its
semantics match some other independently edited source.

For the browser suite, run `python3 scripts/setup-browser.py`. This prepares the
pinned Chromium archive and required Ubuntu libraries under `.tools/` without root
changes. On this Ubuntu 26.04 host, Playwright 1.59.1 has no native platform entry;
the Ubuntu 24.04 Chromium distribution is used explicitly. The npm installer stalled
during extraction, so the setup script uses Python ZIP extraction. This compatibility
choice is recorded in `provenance/browser.json`; it is not a platform qualification.
The integrated validator binds the executable and library path automatically.

EVF preparation verifies and extracts the exact local 0.4 archive, then uses its
supported contained CLI. Bubblewrap/user namespaces must work. No unsafe execution
fallback is provided. Formal solver installations are not required for the selected
finite executable consent, lifecycle and response-field checks.

To serve the built pilot locally:

```bash
cd app
BODY_WAR_STRAVA_FAKE=1 BODY_WAR_AUTH_BACKEND=memory BODY_WAR_PORT=5184 node dist/server.js
```

Open http://127.0.0.1:5184. This uses synthetic identities and memory-backed auth.
Do not interpret it as a deployed or durable production service.

## Source and evidence map

- [EVF contract plan](EVF-CONTRACT-PLAN.md): exact finite oracle cases and generated-source mutants.
- [Contract bindings](evidence/contract-bindings.json): selected keys, case counts and mutant hashes.
- [Identity/query plan](IDENTITY-QUERY-PLAN.md): closed identity records and generated pagination.
- [Domain contract plan](DOMAIN-CONTRACT-PLAN.md): generated normalization and closed nested pilot contracts.
- [Critical integrity plan](CRITICAL-PLAN.md): modeled requests, atomic persistence and exact security evidence.
- [Critical evidence](evidence/critical-coverage.json): eleven authored requirement/case bindings.
- [Next-step plan](NEXT-STEPS.md): shared compiler, runtime mutations and assurance coverage.
- [Construction plan](PLAN.md): scope, D65 stages, validation denominator and remaining work.
- [Definitions](model/DEFINITIONS.md): candidate meaning and preserved source boundaries.
- [Application bindings](model/application-bindings.json): generated, retained and unbound capabilities.
- [Compiled system ontology](model/system-ontology.json): checked application contracts with the embedded two-node DomainSpec consent graph.
- [Source imports](provenance/imports.json): exact imported file identities, before adaptations.
- [Compiler provenance](provenance/compiler.json): freshly compiled DomainSpec source and Alch source bindings.
- [Validation result](evidence/validation.json): most recent integrated campaign, once run.
- [TDE evidence](evidence/tde.json): application and critical integrity obligations, the separate consent obligation and inherited-document diagnostics.
- [Mutation evidence](evidence/model-runtime.json): byte-equivalent generation plus live route/permission/response and executable lifecycle changes.
- [EVF evidence](evidence/evf.json): exact obligation checks, negative controls, repeats and separate verifier.
- [Obligation coverage](evidence/obligation-coverage.json): current denominator with 33 finite EVF witnesses and 11 critical integration witnesses; zero general formal discharges.
- [ORODI evidence](evidence/orodi.json): local health/recovery/collector observations and explicit full-readiness rejection.

Upstream: [original Body War](../body-war/README.md),
[DomainSpec](../domainspec-v2/README.md), and
[enterprise audit](../../../cyberAlchemy-v2/research/2026-09-07-enterprise-application-coverage/REPORT.md).
The original whole-system ontology is an observed inventory. It is not relabeled
as a compiler input here. Generated runtime files retain the compiler's own receipts.
The application backend generates the consent consumer directly through DomainSpec;
the old unused Alch convenience wrapper is no longer part of this application build.

The runner submits activity evidence directly to a suggested track with fresh
consent. No archive import or migration workflow is supported.

## Open Questions

- Which bound IO/rendering adapters should receive deeper executable semantics next?
  Request shape, byte limits and track/evidence normalization are generated. Public identity, track/evidence and activity receipt nesting is closed. Activity query bounds are generated; broader adapter effects still need coverage.
- Which providers should discharge the newly derived TDE obligations? Canonical
  projections now parse, but suite bindings alone do not discharge every obligation.
- Which exact independent production deployment and observation bindings should
  complete ORODI? Local fault/rollback/restart and collector export are now exercised.
- Which live Strava, hosting, availability and security requirements define the
  later operational campaign? No live account access was needed for this rebuild.
- Which private remote and parent submodule registration should eventually host
  this repository? Local Git is initialized; no remote, commit or gitlink is created.
