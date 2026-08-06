# Refine Seed Proposal

## Intent

Refine a safe API for consulting Craft data already ingested into the local
WaveDB snapshot. The API must make Craft state useful to agents and tools without
turning WaveDB into Craft authority or implying that the current experiment is a
production runtime.

## Selected interpretation

The smallest coherent first API is read-only and contract-first:

1. discover available Craft spaces from the stored snapshot manifest;
2. retrieve one ledger snapshot with source path, digest, and freshness metadata;
3. retrieve or search stable Craft row IDs only after schema-version-aware
   normalization is designed and validated; and
4. expose status/health without granting ledger mutation, refresh, promotion, or
   deployment effects.

Refresh ingestion and source-ledger mutation are distinct capabilities. They are
not implicit API endpoints. Any future write path must target the owning
`.craft/ledger.yml` through a deterministic, schema-aware owner route and then
regenerate the WaveDB projection.

## Desired output

A non-executed design and implementation package containing:

- an HTTP/API resource and error contract;
- a versioned projection/query data model for Craft `0.1`, `0.2.0`, and `0.3.0`;
- source authority, privacy, authentication, freshness, and provenance rules;
- a WaveDB adapter contract that handles string-or-Buffer readback and avoids the
  currently failing multi-record atomic batch path;
- positive and negative toy scenarios;
- implementation layering, an atomic Work Pack, and an execution handoff.

## Source evidence

- `experiment/craft-ledger-import/execution/wcli-20260805-node26-04/receipt.json`
  proves 27 current owner ledgers and 788,960 source bytes were stored and read
  back exactly after reopen using sequential writes plus explicit flush.
- `experiment/craft-ledger-import/execution/wcli-20260805-node26-01/receipt.json`
  preserves the failing 55-record atomic batch attempt whose manifest reopened as
  `null`.
- `experiment/craft-ledger-import/.work/wcli-20260805-node26-04/import-ledgers-byte-normalized.js`
  is experimental ingestion evidence, not an API implementation or runtime owner.
- `arcanum/arcana/craft/templates/ledger.schema.yml` and
  `arcanum/arcana/craft/templates/schemas/ledger-core.schema.yml` define the
  current canonical Craft schema contract while live ledgers also include older
  schema shapes.

## Scope and ceilings

- Writable before confirmation: this refinement-run directory only.
- Read-only during the confirmed refinement: canonical Craft contracts, current
  owner ledgers, WaveDB npm diagnostic/import receipts, and the disposable test
  store.
- Forbidden during refinement: Craft ledger mutation, WaveDB package/source
  changes, API implementation, refresh execution, deployment, publication,
  promotion, Git commit, Git push, or parent/submodule movement.
- Public/private boundary: private ledger contents and paths must not be copied
  into public `arcanum/`. A generic public Craft API contract and a private
  DomainSpec adapter remain separate placement candidates until the design names
  their owners.
- Result ceiling: refined design and non-executed plan only. No API endpoint,
  service, integration, release, or production-readiness claim is created.

## Done criteria

- The design fixes the read-only MVP resource model, endpoint semantics,
  pagination/filter rules, errors, provenance, snapshot freshness, and access
  control.
- The projection model distinguishes raw ledger bytes, normalized rows, indexes,
  and source-ledger authority.
- Schema compatibility is explicit for `0.1`, `0.2.0`, and `0.3.0`; unsupported
  shapes fail closed.
- The WaveDB adapter contract accounts for the observed batch persistence failure
  and mixed string/Buffer return types.
- Negative scenarios prove that reads cannot mutate Craft, stale snapshots cannot
  masquerade as current truth, private data cannot cross into public surfaces, and
  missing/duplicate row IDs cannot produce false answers.
- The plan is split into implementation-ready SWUs but remains non-executed.

## Validation surface

- Dispatch schema plus governance validator.
- OpenAPI/JSON Schema validation in the future plan.
- Fixture-ledger compatibility matrix across all observed schema versions.
- Byte-digest provenance checks against `.craft/ledger.yml`.
- Fresh-process close/reopen and API contract tests against a disposable WaveDB
  store.
- Negative authorization, stale-snapshot, missing-row, duplicate-ID,
  batch-failure, and public/private-boundary tests.

## Configuration

- Preset: `standard`.
- Research: `research-if-gap-appears`, local-first. External research requires a
  separately named gap and operator confirmation.
- Subagents: three read-only design critics are recommended and require explicit
  permission before spawn.

