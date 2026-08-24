# Context Pack: SWU-ACAPI-007

This is strict session evidence for an implementation-readiness dry-run. It is
not a runtime handoff, material package, admission receipt, or mutation
authority.

## Identity

- Task: `SWU-ACAPI-007`.
- Mode: `standard`, strict.
- Source work-pack: `20260803T180648Z-agent-consultation-api`.
- Consumer baseline: `workspace-resonant/2.0.0-alpha` on clean `dev` at
  `80dcd79677ad73b21dbaded12e0e9cd47aace82b`.
- Selected files: 12.
- Obligation coverage: 6 covered, 2 blocked.
- Strict coverage: `block`.

## Obligation Matrix

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O-007-01 | L0 predecessor must be complete without extending its epoch. | `one-go/execution/completion-receipt.json`; L0 approval receipt | covered |
| O-007-02 | Principal, policy, deadline, and cancellation must be host-derived and absent from model arguments. | `TASK-ACAPI-04-HOST.md#SWU-ACAPI-007`; L0 query schema | covered |
| O-007-03 | The live Alpha route must have one primary owner service, exact method/path, scoped capability, readable roots, validation, and focused tests. | consumer `MODULE-OWNERSHIP.md#Host Route Contract`; `ALPHA_RUNTIME_BOUNDARY.md#Route Owners` | covered |
| O-007-04 | Capability tokens must be minted and requested consistently. | `bridge-capability-tokens.mjs`; `bridge-client.js`; capability consistency and audit tests | covered |
| O-007-05 | Domain behavior must stay out of the composition root and bridge authentication layer. | consumer `MODULE-OWNERSHIP.md`; `run-bridge-minimal.mjs`; `bridge-server.mjs` | covered |
| O-007-06 | Exact consumer branch, commit, absence baseline, and touched-file digests must be frozen before admission. | `CONSUMER-BASELINE.json` | covered |
| O-007-07 | One owner route must be selected. | `decision/HOST-ROUTE-DECISION.md` | blocked by `DG-L12-001` |
| O-007-08 | The exact consumer projection fields, leakage rules, manifest approval, and readable location must be approved. | L0 projection schemas; `decision/PROJECTION-POLICY-DECISION.md` | blocked by `DG-L12-002` |

## Selected Evidence

| Source | Selector | Obligations |
| --- | --- | --- |
| `WORK-PACK.md` | SWU manifest rows 007-011; blockers B-002-B-004 | O-007-01, O-007-07, O-007-08 |
| `work-pack/tasks/TASK-ACAPI-04-HOST.md` | SWU-007 behavior, write scope, validation | O-007-02 |
| `one-go/execution/completion-receipt.json` | status, unit count, validation, exclusions | O-007-01 |
| `one-go/decision/decision-gate-approval-receipt.json` | `l1_or_later=false` | O-007-01 |
| `consultation-api/schemas/query.schema.json` | closed model-visible request shape | O-007-02 |
| `consultation-api/schemas/projection.schema.json` | current fixture projection fields | O-007-08 |
| `consultation-api/schemas/projection-manifest.schema.json` | fixture-only compiler and owner approval | O-007-08 |
| consumer `docs/architecture/MODULE-OWNERSHIP.md` | shared-core boundary and Host Route Contract | O-007-03, O-007-05 |
| consumer `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md` | two-component Alpha path and route owners | O-007-03, O-007-05 |
| consumer `browser-first/host/bridge-capability-tokens.mjs` | canonical token specification | O-007-04 |
| consumer `browser-first/resonantos-side-panel-extension/src/lib/bridge-client.js` | route-to-capability map and runtime allowlist | O-007-04 |
| consumer capability consistency/audit tests | launcher-extension-route agreement | O-007-04 |

## Constraints

- Evidence-only, read-only, and no reasoning/authority effects.
- No private repository path or arbitrary filesystem query may be model-visible.
- No trusted principal, policy, approval, route, or capability token may come
  from model arguments.
- The consumer reads only a separately approved neutral projection.
- `src/core/` may own pure contracts but not privileged host behavior.
- `run-bridge-minimal.mjs` composes; `bridge-server.mjs` authenticates and
  enforces capabilities; the selected service owns consultation policy.
- No product write until DG-L12-001, DG-L12-002, refreshed material validation,
  mutation admission, and exact epoch approval all pass.

## Write Scope Status

The exact write set is not yet valid because it depends on DG-L12-001. The two
admissible action profiles share these paths:

- `src/core/augmentor-consultation/**` for pure contracts and policy;
- `browser-first/host/run-bridge-minimal.mjs` for composition only;
- `browser-first/host/bridge-capability-tokens.mjs`;
- `browser-first/resonantos-side-panel-extension/src/lib/bridge-client.js`;
- focused `browser-first/test/**` capability and host-route tests;
- `docs/architecture/MODULE-OWNERSHIP.md` and
  `docs/architecture/ALPHA_RUNTIME_BOUNDARY.md`.

The selected owner profile determines whether the service target is a new
`augmentor-consultation-host-service.mjs` or an admitted extension of the
memory host service. Those alternatives cannot coexist in one material
package.

## Validation Surface

- Targeted Node tests for context validation and the selected host service.
- `node --test browser-first/test/bridge-route-capability-audit.test.mjs`.
- `node --test browser-first/test/bridge-capability-token-consistency.test.mjs`.
- `npm test -- --run`.
- `npm run build`.
- `npm run test:module-ownership` when ownership docs change.
- `npm run verify:alpha` at the L1 integration witness and final L2 terminal.
- Security pipeline at SWU-011 and for any earlier security-sensitive repair.

## Gate Result

- Context artifact: complete.
- Runtime handoff: `BLOCK` because O-007-07 and O-007-08 are unresolved.
- Next route: Decision Gate `DG-L12-001`.

