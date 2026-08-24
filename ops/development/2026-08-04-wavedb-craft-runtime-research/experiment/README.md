# WaveDB Craft Projection Experiment

This candidate-local package turns the WaveDB/Craft research verdict into a
governed Define -> Design -> Plan -> Task Session execution path.

The experiment is deliberately narrower than a Craft runtime migration:

- `.craft/ledger.yml` remains the only Craft source of truth;
- WaveDB may hold only a disposable, digest-addressed projection;
- every query fresh-reads and revalidates canonical YAML first;
- no database-to-YAML or derived-view ingestion path exists;
- receipts and quarantine evidence stay outside WaveDB;
- no canonical or historical Craft source is edited;
- publication, promotion, deployment, and production claims are excluded.

## Navigation

- [Define](define/DEFINE.md)
- [Architecture](design/ARCHITECTURE.md)
- [Implementation layering](plan/IMPLEMENTATION-LAYERING.md)
- [Work Pack](plan/WORK-PACK.md)
- [Execution evidence](execution/README.md)

## Current execution boundary

WP-0 is fail-closed. The registry metadata for `@vijayee/wavedb@0.15.8`
declares a Git head whose checked source still reports `0.15.7`. The reviewed
`0.15.8` source is a different commit. Until an owner selects and binds an
exact source/package correspondence, native installation is forbidden.
