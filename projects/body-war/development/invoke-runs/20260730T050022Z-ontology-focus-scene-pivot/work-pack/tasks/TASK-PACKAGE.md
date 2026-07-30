# TASK-PACKAGE — Reproducible Local Prototype Handoff

## SWU-OFSP-026 — Package the admitted local prototype

- Primary behavior: publish a repository-local reproduction guide and
  digest-bound prototype manifest that selects the admitted adapter/build/
  browser receipts and separates a later human-comprehension research handoff.
- Independent acceptance: a clean isolated local reproduction uses the
  existing package root and global Playwright, verifies every bound input, opens
  the exact local route, and emits a new reproduction receipt.
- Split analysis: manifest, guide, and reproduction receipt are one local
  handoff contract; upstream publication, deployment, and human research are
  explicitly separate routes.
- Dependencies: 025, `TASK-VERIFY`, `TASK-AUDIT-ALIGNMENT`, and
  `TASK-AUDIT-LAYERING`, each with a passing exact receipt.
- Source anchors: `IMPLEMENTATION-LAYERING.md#layer-decision-table`,
  `ARCHITECTURE.md#integrationversioning-extension`.
- Write scope:
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/FOCUS-SCENE-PROTOTYPE.md`
  - `cyberAlchemy-v2/implementation/ontology-evidence-workbench/contracts/focus-scene-prototype-manifest.schema.json`
  - new immutable
    `cyberAlchemy-v2/implementation/ontology-evidence-workbench/generated/runs/SWU-OFSP-026/{attempt_id}/`
- Done: reproduction receipt passes and the guide states the exact structural,
  candidate-local, local-only claim ceiling.
- Validation: exact argv, runtime, attempt ID, collision, and teardown
  contracts are owned by `../shared/COMMAND-MATRIX.json#SWU-OFSP-026`.
- Owner: `local-fallback` through Task Session.

## Excluded Successors

- Upstream contribution requires a separate upstream-owner decision and route.
- Remote deployment/release requires a separate release-admission route.
- Human comprehension requires a separate blinded study with new evidence and
  is not a successor automatically selected by this SWU.
