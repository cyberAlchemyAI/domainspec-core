# Feedback loop 02: writer revision

Edit `findings.md` only. Preserve the accepted architecture, verdict matrix,
citations, evidence ceiling, and explicit unverified/unexecuted fixture labels.

Add one compact YAML or JSON fixture-contract schema, then complete bindings for:

- `PBW-01-body-war-swu-001-stable`
- `NBW-01` through `NBW-11`
- `P-PROJ-01`
- `N-SEM-01` through `N-SEM-05`
- `N-RUN-01`

Every fixture must serialize:

- fixture ID and `evidenceStatus: proposed-unverified-unexecuted`;
- frozen input paths, exact selectors, and SHA-256 values;
- zero or one injected fault;
- first-knowable stage;
- first-detected gate;
- expected owner;
- terminal code;
- expected receipt count;
- allowed writes;
- forbidden transitions.

Use shared base bindings/ref reuse where helpful, but each fixture must resolve
deterministically. Inspect the exact Body War handoff to name the three allowed
target paths/digests. Do not imply the fixtures were executed.
