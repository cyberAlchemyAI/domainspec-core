# Research Dependency Graph

Cross-project dependencies must be explicit and version-pinned.

## Graph

- mars depends on domainspec (claim baseline and protocol methods)
- meta-meta depends on domainspec (method baseline for signal/governance experiments)

## Edge List

| Consumer | Dependency Type | Provider | Provider Artifact | Gate |
|---|---|---|---|---|
| mars | claim_dependency | domainspec | exports/claims/C2-baseline.md | G1 |
| mars | method_dependency | domainspec | exports/methods/protocol-analysis-minimum.md | G1 |
| meta-meta | method_dependency | domainspec | exports/methods/signal-observation-baseline.md | G2 |

## Rules

1. No consumer may read provider internal files directly.
2. Every edge must exist in the consumer deps/DEPENDENCIES.yaml.
3. Provider artifact must include version or commit pin.
4. Broken edges block execution at the declared validation gate.
