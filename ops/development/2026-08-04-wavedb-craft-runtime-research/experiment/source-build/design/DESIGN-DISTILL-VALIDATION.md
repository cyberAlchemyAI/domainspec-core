# Design Distill validation

- Mode: `Standard`, two role-simulated passes; no subagents were authorized.
- Objective: select the smallest complete architecture for one reviewed-source
  local addon and its evidence handoff.
- Proposer: use distinct source, dependency, generated-source, build, test, and
  handoff components behind one terminal receipt.
- Balancer objection (`split-pressure`): separate components could become
  independent SWUs and create partial artifacts mistaken for readiness.
- Reconciliation: components remain ordered acceptance stages of one
  `SourceBuildReceipt`; no intermediate stage is parent-consumable.
- Balancer objection (`authority-boundary`): the parent could treat a local
  build as corrected npm provenance.
- Reconciliation: parent consumption requires a separate Invoke Refresh and
  the failed npm receipt remains immutable history.
- Smallest coherent unit: one source-built addon attempt, because source,
  dependency, build, load, and test evidence lose meaning if any is absent.
- Recomposition: the unit closes SourceClosure, DependencyClosure, NativeBuild,
  BuildVerification, and ArtifactBinding from Define without adding Craft or
  publication behavior.
- Premortem: node-gyp/Python/Node/OpenSSL incompatibility; block without
  toolchain substitution or implicit retry.
- Frame expiry: a different root commit, lockfile, recursive submodule, Node,
  compiler, OS, architecture, or OpenSSL mode requires a new Design/Plan epoch.
- Verdict: `pass`; Plan may define one low-complexity selected SWU.
