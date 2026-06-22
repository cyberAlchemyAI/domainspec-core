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

Current canonical synced MARS skills:

- `mars-research-start` — unified startpoint for greenfield project initialization and brownfield baseline audits
- `mars-research-foundations` — create project-level domain-context and methodology/theory baselines backed by source catalog, reference ledger, and library-grade inventory coverage
- `mars-research-emit-signals` — append structured telemetry signals for workflow gaps, contract gaps, evidence gaps, and reflection proposals
- `mars-research-authority-governance` — authority-source governance for experiment readiness
- `mars-research-knowledge-stack-normalization` — brownfield research artifact normalization
- `mars-research-complete-experiment` — end-to-end experiment completion workflow
