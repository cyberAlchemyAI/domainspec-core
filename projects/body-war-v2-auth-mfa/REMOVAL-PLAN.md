# Remove unused archive migration

## Product construction

Owner decision: archive migration is not a product requirement. Remove the queue,
legacy API aliases, UI controls, archive reader, request field and application
repository linkage. The supported loop is connected account -> suggested track ->
activity -> explicit consent -> evidence candidate. Mock activities remain clearly
labeled and scoped to the staging runner.

D65: existing pilot definitions -> revised Alch declarations -> shared DomainSpec
compilation -> application adapters -> removal regression and normal-flow tests.
No ontology-runtime record or selector is required. Removed legacy contract witnesses
are removed from the TDE/EVF catalog rather than retained as current coverage.

## Operational support

The agent validates and updates only the private VPS staging service. Remove its
synthetic archive overlay; preserve ordinary mock runs, the mock track, existing
consented evidence, credentials and original files. Old checksum-tracked SQL files
and the unused physical legacy_submission_id column are retained for rollback.
Active application schemas and requests no longer expose or use that column.
Database schema migrations remain necessary infrastructure, separate from the
removed archive-import feature. No live TROQAR or co-op deployment is changed.

## Validation

Removed API routes return 404; the retired legacy_submission_id input is rejected.
Browser checks show no migration panel, while ordinary evidence submission remains
covered. Re-run unit, PostgreSQL, compiler parity, TDE, EVF and local ORODI checks.
Deploy the tested candidate and verify the same removal on VPS staging.

## Open Questions

Next product work is the ordinary evidence lifecycle: inspect, remove/withdraw,
and clearly explain submitted evidence. Live activity, geometry and scoring need
separate evidence. Archive migration is no longer an open product requirement.
