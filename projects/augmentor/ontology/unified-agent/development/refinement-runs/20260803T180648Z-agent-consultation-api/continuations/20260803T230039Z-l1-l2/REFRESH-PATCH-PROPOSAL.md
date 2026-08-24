# L1-L2 Refresh Patch Proposal

This file proposes planning changes only. It is not an admitted material
package and grants no product, route, capability, projection, deployment, or
promotion authority.

## 1. Work-pack status

- Replace the stale B-001 row with an evidence-backed statement that L0 epoch
  `epoch-cdd98012d74d842a5763602f` completed.
- Keep B-002, B-003, B-004, and B-005 open.
- Keep the completed L0 epoch immutable and append-only.
- Add a distinct L1-L2 approval epoch only after this proposal is applied,
  implementation-readiness passes, and the exact digest is presented.

## 2. L1 Alpha route

The existing plan's `src/core/runtime.ts` registration is stale relative to the
current Alpha boundary. Refresh SWU-007 through SWU-009 as follows:

- Pure schemas, result mapping, answer policy, and side-effect-free helpers may
  live under `src/core/augmentor-consultation/`.
- Privileged projection access and verified caller policy belong to one named
  service under `browser-first/host/`.
- The service must expose one exact route, declare one scoped capability, read
  only an explicitly approved projection location, reject caller-supplied
  principal/policy overrides, and return the existing closed result union.
- `run-bridge-minimal.mjs` may compose the service and route only; domain logic
  must not accumulate there.
- `bridge-server.mjs` retains transport authentication and capability checks.
- Focused bridge tests belong under `browser-first/test/`; shared pure-policy
  tests may remain next to `src/core/augmentor-consultation/`.
- The route, capability, readable roots, redaction rules, and primary service
  owner must be reflected in the consumer ownership and Alpha-boundary docs.

The exact service owner is intentionally not selected here. Decision
`DG-L12-001` owns that choice.

## 3. Neutral consumer projection

Refresh the fixture-only projection contract before any consumer bytes are
copied or read:

- replace the fixture-only compiler and `ownerApprovalRef` constraint with a
  versioned consumer projection/manifest contract;
- bind the exact field allowlist digest, source digests, compiler digest,
  projection digest, generated timestamp, opaque-ID policy, and owner approval
  reference;
- reject filesystem paths, private identifiers, instructions, credentials,
  bearer material, write/run/approve/route fields, and undeclared fields;
- decide whether free-form confidence `basis` and raw `ownerRef` are allowed or
  must become controlled/opaque values;
- keep generation one-way from private source to neutral projection; the
  consumer must not query the private repository or ontology directly.

Decision `DG-L12-002` will own the exact fields after the host route is chosen.

## 4. L2 boundary

- Preserve SWU order `010 -> 013 -> 011` after the executed SWU-009 witness.
- Add counters for scans, joins, bytes, result size, elapsed time, cancellation,
  timeout, denial, drift, and failure class.
- Let each request carry an owner-bounded effective deadline and limits, but do
  not publish fixed production defaults until measured evidence is reviewed.
- Keep cache keys bound to principal, policy, access class, projection digest,
  contract version, and effective limit policy.
- Require security-owner review for failure-injection acceptance.

## 5. New finite execution frontier

After decisions and refresh apply, create one new exact package containing only:

1. `SWU-ACAPI-007` verified host context and owned bridge adapter;
2. `SWU-ACAPI-008` total answer/qualify/clarify/abstain policy;
3. `SWU-ACAPI-009` supported/denied/stale/conflict/injection host witness;
4. `SWU-ACAPI-010` access-isolated immutable evidence cache;
5. `SWU-ACAPI-013` deadline and cancellation propagation;
6. `SWU-ACAPI-011` integrated failure-injection and measurement suite.

The exact approval request must show the package ID, canonical digest, consumer
commit and branch, every changed path, every unit dependency, all validation
commands, and the explicit exclusion of deployment, release, and L3.

