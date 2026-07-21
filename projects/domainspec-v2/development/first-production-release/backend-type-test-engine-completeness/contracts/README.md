# Candidate Backend Structural Verification Contract

This folder is a planning target for `SWU-BTE-005`, `SWU-BTE-009`, and
`SWU-BTE-010`. It is not current definition, profile, ledger, or release authority.

The planned catalogue must record:

- the selected profile ID/version/digest;
- the successor profile `feature-with-independent-node-and-edge-files@1` and
  its candidate posture;
- the exact 13 admitted backend kinds;
- the exact 16 admitted backend relationship signatures;
- one exact schema path and digest per kind;
- one shared edge schema, same-feature edge root, project-level cross-feature edge
  root, and resolver scope rules;
- one stable obligation ID per current criterion entry;
- criterion rule, expected source representation, and source anchor;
- expected positive and mutation fixture IDs;
- execution and mutation evidence requirements;
- causal node-to-pattern and edge-to-composition/removal requirements;
- IOLM and Body War consumer receipt identities, projection/redaction posture, and
  the integrated manifest binding;
- owner approval record and explicit `release_admission: not-granted`.

The catalogue is the independent `O_spec` denominator. Engine output may consume or compare against it, but engine output may not silently rewrite it. The exact comparator is `O_spec = O_gen = T_gen = E_run`; a consumer receipt never defines `O_spec` or grants profile/release authority.

## SWU-BTE-003 Adapter Handoff

`impl/tools/minted-project/meta-type-body-adapter.ts` now owns the
`minted-node-body-adapter/v1` representation boundary:

- `body.fields[*].name/type/required/identity/description` project to canonical
  `Field/Type/Required/Identity/Description` criterion columns;
- `body.values` projects to a `Value` table;
- direct scalar body keys project to criterion attributes without collapsing
  missing, empty, whitespace, `false`, or `0`;
- `body.equality` is the named prose projection for `section-contains`;
- profile-admitted kinds resolve to the unique canonical YAML schema by
  `meta_type`; explicit `attribute-map` profile paths are honored and checked;
- optional schema SHA-256 expectations fail closed for the digest-pinned profile
  binding added by a later SWU.

The compiler reports formation failures under `FORMATION_INVALID`. Each emitted
violation carries `adapterVersion`, `schemaPath`, `criterionId`, `rule`, `code`,
and `subjectPath`; node-envelope failures remain `NODE_SCHEMA_INVALID`. The
adapter delegates evaluation to `impl/tools/lib/meta-type-criteria.ts` and does
not retain the former private attribute-map parser.

Direct evidence is in
`impl/tools/tests/minted-project-meta-type-body-adapter.test.ts` and
`impl/tools/tests/minted-project-compiler.test.ts`. The Task Session receipt is
under
`work-pack/session-evidence/SWU-BTE-003/20260720T205600Z-minted-node-body-adapter/`.
This handoff records implementation evidence only; it does not admit the
successor profile or satisfy `O_spec`, corpus, edge, consumer, or release gates.
