# MARS Copilot Pack

This folder is the canonical pack location for reusable MARS Copilot assets.

Ownership and flow:

- Canonical reusable pack assets originate under [implementation/mars](..).
- Root [/.github](../../../.github) contains orchestration-local agent behavior for this repository.
- Research-project execution uses projected artifacts under [research/projects/mars](../../../research/projects/mars).

Synchronization command:

```bash
./tools/sync_mars_canonical_assets.sh
```

This command keeps canonical definitions/templates and managed canonical copilot skills aligned with runtime copies.