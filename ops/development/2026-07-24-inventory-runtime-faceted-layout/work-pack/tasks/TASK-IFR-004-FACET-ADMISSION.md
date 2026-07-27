# TASK-IFR-004: Faceted New-Entry Admission

## Objective And Mapping

- Layer/slice: L2 / S-04.
- SWU: `SWU-IFR-004`.
- Goal: validate namespace, record class, concepts, and namespace-first path for
  new faceted records while preserving all legacy record paths.

## Dependencies

- Passing `SWU-IFR-002` receipt.

## Implementation Detail

Inputs:

- candidate record;
- consumer-controlled namespace and record-class vocabularies;
- existing machine index schema/version.

Outputs:

- canonical facet fields and expected physical path;
- faceted/legacy admission disposition;
- precise `invalid-request` diagnostics.

Algorithm:

1. Detect faceted mode from schema version or complete facet field presence.
2. Legacy mode preserves old validation and current path.
3. Faceted mode requires one normalized kebab-case namespace.
4. Require one controlled record class.
5. Require a non-empty concepts list; normalize, deduplicate, and byte-sort.
6. Require the exact path:
   `entries/<namespace>/<record-class>/<stable-id>.md`.
7. Keep stable ID independent of path.
8. Reject partial facet metadata, path traversal, unknown class, empty concept,
   duplicate normalized concept, and path mismatch.
9. Emit normalized record to the candidate builder.

Precedence:

```text
invalid schema mode
> missing/invalid namespace
> missing/unknown record class
> invalid concepts
> path mismatch
> admitted faceted record
```

## Smallest Working Unit: SWU-IFR-004

- Primary behavior: admit one new faceted record or one unchanged legacy
  record.
- Independent acceptance boundary: all metadata and path rules produce one
  deterministic admission result; legacy fixtures remain byte-stable.
- Candidate children: metadata; path; legacy.
- Split analysis: one admission decision requires their defined precedence, so
  separate acceptance would allow contradictory states.
- Write scope:
  - `arcanum/arcana/inventory/templates/index.schema.yml`
  - `arcanum/arcana/inventory/templates/entry.md`
  - `arcanum/arcana/inventory/templates/schema.md`
  - `arcanum/arcana/inventory/lib/inventory-update.cjs`
  - `arcanum/arcana/inventory/test/facet-admission.test.cjs`
  - `arcanum/arcana/inventory/test/fixtures/facet-admission/`
- Done criteria:
  - new faceted records require exact metadata/path;
  - tag combinations never create directories;
  - legacy records pass unchanged;
  - private namespace values appear only in consumer fixtures, not public
    canonical fixtures.
- Acceptance evidence: `inventory.facet-admission-result.v1`.
- Validation:

```sh
node --test arcanum/arcana/inventory/test/facet-admission.test.cjs
```

- Execution owner: `sigil-development`.

## Closeout

Passing this unit unlocks only `SWU-IFR-005`.

