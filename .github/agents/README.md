# Research Orchestration Agents

Place Type B research orchestration agent definitions in this directory.

Rules:

- Keep reusable implementation agents out of this directory.
- Promote only research-focused automation (for example inventory, sourcing, synthesis, experiment analysis).
- Mirror ownership and synchronization rules from `ops/ASSET-OWNERSHIP-POLICY.md`.

Current lifecycle-critical agents:

- `domainspec-research-scientist` — orchestration and paper integration
- `domainspec-research-planner` — MARS-context planning and gate-ready execution decomposition
- `domainspec-research-sourcer` — source discovery and quality gate
- `domainspec-research-inventorist` — inventory readiness gate
- `domainspec-research-analyst` — data analysis and validity assessment
- `domainspec-research-protocol-designer` — protocol design and pre-execution protocol gate
- `domainspec-research-evidence-auditor` — claim evidence coverage and next-run prioritization
