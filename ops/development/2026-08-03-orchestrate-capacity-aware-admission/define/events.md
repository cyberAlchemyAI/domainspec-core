# Events

## CapacityEvidenceBound

Records the capacity evidence ID/digest bound to the exact run and wave before
admission. It carries no raw host-private detail.

## CapacityAdmissionDecided

Records verdict, policy, requested/admitted units, blocker classes, and the
evidence handle. A blocked decision precedes action compilation and therefore
has zero spawn attempts.

## PreAgentFailureReceiptAdmitted

Canonical causal branch:

```text
action_attempted
  -> host_spawn_failed
  -> pre_agent_failure_receipt_admitted
  -> gate_decided(gate_block)
```

The failure-receipt event uses `agent_id: null`. It proves that the required
action reached a terminal blocked evidence state; it does not pretend an agent
existed or allow `gate_pass`.

## CapacityReservationChanged

Deferred host-owned event for reservation acquired, consumed, expired, or
released. It becomes executable only with an admitted provider contract.

## SlotReleaseObserved

Deferred host-owned observation. It is distinct from `agent_closed` and must
name the capacity scope it affects.

