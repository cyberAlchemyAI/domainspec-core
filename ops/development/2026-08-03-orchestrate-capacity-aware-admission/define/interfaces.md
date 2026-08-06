# Interfaces

## HostCapacityEvidence

Versioned immutable input supplied by the host boundary. The public contract
contains generic scheduling facts only; provider quotas, account tier, private
infrastructure, and unrelated agent context remain outside the artifact.

Required semantic groups:

- identity: evidence, host, capacity scope, run, and wave;
- time: observation and expiry;
- authority: authoritative, advisory, unknown, or unsupported;
- demand: requested fresh-spawn units;
- supply: spawnable or reserved units when authoritative;
- occupancy: active, retained-terminal, reusable, released, and unknown counts
  only when the host can prove those classifications;
- reservation: supported flag and optional lease handle;
- provenance: owner operation/metadata handle and safe residue.

## CapacityEvidenceProvider

Host-profile contract that obtains `HostCapacityEvidence`. The provider owns
facts; Orchestrate owns only schema validation and policy evaluation.

Current Codex constraint: `collaboration.list_agents` can support occupancy
observation but has not been shown to supply a total limit, reservation, or
physical release. Its output alone is therefore not authoritative capacity.

## CapacityAdmissionReceipt

Deterministic output with:

- requested and admitted units;
- evidence identity and digest;
- policy and verdict;
- blockers;
- action emission count, always zero for a blocked verdict;
- optional route option handles added only by the later route-projection
  capability, not by the L0 admission evaluator;
- claim ceiling (`snapshot-only`; `reservation-bound` is reserved for a future
  host-owned extension).

## PreAgentFailureReceipt

Conditional form of the normalized action receipt:

- exact action/dispatch/run/wave/step/role/capability identity;
- `agent_id: null`;
- `receipt_kind: host-spawn-failure`;
- `status: block`, `validation: block`;
- one safe failure class and optional private diagnostic handle;
- timestamps, blockers, residue, and reroute.

## HostReservationProvider

Deferred optional host contract: atomically reserve, consume, expire, and
release exact units. Until this exists, Orchestrate may claim snapshot-bound
admission only and must expose the race residue.
