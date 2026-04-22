# Research Orchestration Agents

Place Type B research orchestration agent definitions in this directory.

Rules:

- Keep reusable implementation agents out of this directory.
- Promote only research-focused automation (for example inventory, sourcing, synthesis, experiment analysis).
- Mirror ownership and synchronization rules from `ops/ASSET-OWNERSHIP-POLICY.md`.

Current lifecycle-critical agents:

- `mars-research-scientist` — orchestration and paper integration
- `mars-research-planner` — MARS-context planning and gate-ready execution decomposition
- `mars-research-sourcer` — source discovery and quality gate
- `mars-research-inventorist` — inventory readiness gate
- `mars-research-analyst` — data analysis and validity assessment
- `mars-research-protocol-designer` — protocol design and pre-execution protocol gate
- `mars-research-evidence-auditor` — claim evidence coverage and next-run prioritization
