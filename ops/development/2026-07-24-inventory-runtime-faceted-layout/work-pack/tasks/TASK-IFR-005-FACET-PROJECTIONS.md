# TASK-IFR-005: Facet Projections

## Objective And Mapping

- Layer/slice: L2 / S-05.
- SWU: `SWU-IFR-005`.
- Goal: derive exact machine and human lookup views for namespace, record class,
  and concept without making those views authoritative.

## Dependencies

- Passing `SWU-IFR-004` receipt.

## Implementation Detail

Inputs:

- candidate entry list containing legacy and faceted records;
- existing exact derived maps and human-index rules.

Outputs:

- `indexes.by_namespace`;
- `indexes.by_record_class`;
- `indexes.by_concept`;
- namespace/record-class grouping in the human index;
- full conformance result.

Algorithm:

1. Initialize the three derived maps.
2. Iterate entries in canonical entry order.
3. Skip facet maps for legacy records lacking all facet fields.
4. Append each faceted entry ID once to its namespace and record-class keys.
5. Append the ID once to every normalized concept key.
6. Preserve entry order inside arrays and deterministic insertion order for
   new keys.
7. Render human groups from the same admitted records.
8. Rebuild all required maps independently in the validator and compare exact
   equality.
9. Check every represented human path/class against the machine index.

Edge cases:

- mixed legacy/faceted index;
- two concepts normalize to one value;
- faceted entry missing from one map;
- orphan map ID;
- human group contains a path absent from machine index.

## Smallest Working Unit: SWU-IFR-005

- Primary behavior: reproduce all facet lookup views from admitted entries.
- Independent acceptance boundary: machine and human projections equal an
  independent rebuild over mixed fixtures.
- Candidate children: three map writers; human grouping.
- Split analysis: each output is testable, but conformance must prove them as
  one projection family from the same source.
- Write scope:
  - `arcanum/arcana/inventory/lib/inventory-update.cjs`
  - `arcanum/arcana/inventory/scripts/validate-index-json.sh`
  - `arcanum/arcana/inventory/scripts/validate_projection_conformance.py`
  - `arcanum/arcana/inventory/templates/index.json`
  - `arcanum/arcana/inventory/templates/index.md`
  - `arcanum/arcana/inventory/test/facet-projection.test.cjs`
  - `arcanum/arcana/inventory/test/fixtures/facet-projection/`
- Done criteria:
  - exact maps reproduce;
  - legacy entries remain indexed by existing maps;
  - human and machine paths/classes conform;
  - all maps remain Inventory read models.
- Acceptance evidence: `inventory.facet-projection-result.v1`.
- Validation:

```sh
node --test arcanum/arcana/inventory/test/facet-projection.test.cjs
bash arcanum/arcana/inventory/scripts/validate-index-json.sh \
  arcanum/arcana/inventory/test/fixtures/facet-projection/index.json
```

- Execution owner: `sigil-development`.

## Closeout

Passing this unit satisfies the facet dependency of `SWU-IFR-006`.

