# Planning Context

## Obligation Matrix

| ID | Planning Obligation | Evidence | Coverage |
| --- | --- | --- | --- |
| O-001 | Preserve the loopback, local, no-op L0 boundary. | `SPEC.md` In/Out Of Scope; `ARCHITECTURE.md` Host Strategy. | covered |
| O-002 | Close all accepted present-L0 findings without pulling promotion work forward. | Architecture review AR-CAND-001 through AR-CAND-008 and severity-ordered requests. | covered |
| O-003 | Produce a human-workable queue, disposition, history, and evidence workflow. | Existing `public/demo/l0.html`; Nimbalyst finding recommends restrained next-step/evidence grammar only. | covered |
| O-004 | Use a real Draft 2020-12 runtime validator. | Review AR-CAND-008; Ajv official Draft 2020-12 documentation. | covered |
| O-005 | Define task/SWU write scope, dependencies, evidence, and verification. | `invoke plan` mode contract and work-pack template. | covered |
| O-006 | Keep Invoke, Task Session, kernel, UI, adapters, and Craft authorities separate. | Invoke lifecycle chain; architecture kernel responsibilities; Craft source-of-truth rule. | covered |
| O-007 | Provide a smallest coherent first unit and recomposition proof. | Distill validate pass in `PLAN-TRANSPORT.md`. | covered |

## Selected Context

The planning pass used a standard strict context set with selector-level emphasis:

1. `SPEC.md`: L0 scope, typestate, receipt contract, and acceptance.
2. `ARCHITECTURE.md`: kernel ownership, host strategy, adapter boundary, and layer order.
3. `development/architecture-review-2026-07-10/findings.md`: accepted defects, strengths, and promotion-only gates.
4. `src/server.mjs`: current routes, singleton state, write ordering, and approval flow.
5. `src/envelopes/dry-run-envelope.mjs`: lifecycle and receipt construction.
6. `src/kernel/grants.mjs`: current open grant behavior and approval classifier.
7. `src/kernel/audit.mjs`: append-only event implementation.
8. `src/kernel/artifacts.mjs`: non-exclusive artifact writes.
9. `src/kernel/registry.mjs`: handwritten manifest validation.
10. `scripts/validate-schemas.mjs`: parse-only schema command.
11. `public/demo/l0.html`: current prepare/approve UI and caller-supplied attribution.
12. `tests/l0-smoke.test.mjs`: cooperative happy-path coverage.
13. `package.json`: Node baseline and available validation scripts.

## Excluded Candidates

- MCP/chat, browser-control, Kernel, and Nimbalyst implementation research: useful for later-layer boundaries, but not needed to repair present L0.
- OpenRouter adapter: descriptor-only and explicitly outside the active layer.
- Module manifests: registry boundary is planned from the schema/review contract; individual module semantics are unchanged.
- Generated runtime handoff packs: execution-time session evidence, not planning artifacts.

## Authority Precedence

1. Accepted architecture review controls the repair order and defect wording.
2. `SPEC.md` and `ARCHITECTURE.md` control the existing product boundary.
3. This work-pack controls implementation sequencing, not upstream product authority.
4. Source code and tests show current behavior but do not override accepted findings.
