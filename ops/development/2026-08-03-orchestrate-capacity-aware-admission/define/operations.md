# Operations

## EvaluateWholeWaveAdmission

Purpose: decide whether the exact validated wave may emit spawnable actions.

Inputs:

- dispatch ID, run ID, host ID, wave ID;
- requested fresh-spawn units;
- execution policy (`strict_whole_wave` by default);
- one immutable `HostCapacityEvidence` record.

Algorithm:

1. Validate the evidence schema and identity binding.
2. Reject an evidence record for another host, capacity scope, run, or wave.
3. Reject expired, advisory, unknown, or internally inconsistent evidence for
   strict admission.
4. In the active snapshot-only contract, block any reservation-required policy
   as unsupported. Reservation verification is a deferred host-owned extension.
5. Compare requested units with the evidence's authoritative spawnable or
   reserved units.
6. Emit one `CapacityAdmissionDecision`.
7. Only `admitted` may feed action compilation. Every blocked result emits zero
   spawn actions and zero spawn attempts.

Output: immutable capacity admission receipt. The later route-projection
capability may consume a blocked receipt; L0 emits no route-option handles.

### Whole-wave policy

- No partial action set is emitted from an insufficient record.
- No implicit retry, serial conversion, reuse, or fresh-session transition.
- The decision does not change Dispatch Spec validity or approval.
- A snapshot without reservation is advisory when the host allows concurrent
  allocation races; it cannot support a race-free claim.

## AdmitPreAgentFailure

Purpose: normalize a native spawn rejection when no agent identifier exists.

Inputs: persisted action, prior `action_attempted`, `host_spawn_failed`, safe
cause class, timestamps, and optional host-private diagnostic handle.

Output: `PreAgentFailureReceipt` with `status: block`, `validation: block`,
`agent_id: null`, and no dependent actions.

The receipt satisfies evidence completeness for the attempted action but can
never be admitted by a passing gate.

## ProjectCapacityRouteOptions

Purpose: translate a blocked admission into feasible choices without executing
or approving any choice.

Possible options, each conditional on an existing owner capability:

- revalidate a smaller parallel wave;
- revalidate a serial route;
- route a role to an allowed local fallback;
- hand off to a fresh session with immutable context;
- use an owner-backed queue;
- defer or cancel.

Unavailable capabilities are omitted. Any material route change produces new
bytes and invalidates the prior execution approval.

## ReconcilePhysicalSlotLifecycle

Deferred host-owner operation. It may classify a known thread as active,
terminal-retained, reusable, released, or unknown only from host-owned
evidence. Orchestrate never upgrades `agent_closed` to `released` by itself.
