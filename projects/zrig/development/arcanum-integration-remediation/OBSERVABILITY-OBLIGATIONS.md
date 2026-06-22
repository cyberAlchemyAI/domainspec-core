# Observability Obligations

Status: design-only
Scope: private Z-Rig remediation planning
No active telemetry, metrics wiring, Signal Observer bridge, or runtime observability readiness is claimed.

## Purpose

Define what evidence Z-Rig must eventually emit or preserve for product-mode claims to be reviewable. These obligations are derived from F1-F14 and remain design obligations until implemented and tested.

## Obligations

| ID | Finding | Obligation | Evidence Needed | Current Status |
| --- | --- | --- | --- | --- |
| OBL-ZRIG-F1-GATE | F1 | Every spec-governed wave must report whether a specific evaluator, fail-closed policy, or explicit passthrough rule decided the gate. | Gate evaluation record includes gate type, policy, and failure reasons. | missing/generic fallback |
| OBL-ZRIG-F2-ASSURANCE | F2 | Dry-run/stub completion must be visibly separate from live governed assurance. | Run summary and docs label stub vs live evidence. | partial, needs stronger language |
| OBL-ZRIG-F3-RESIDUE | F3 | Residue write success/failure must affect product/live assurance according to an explicit policy. | Residue record or degraded/fail-closed event tied to run status. | broken/non-fatal |
| OBL-ZRIG-F4-IDENTITY | F4 | Model/family identity must come from trusted seat metadata or signed runtime metadata, not arbitrary bridge output. | Identity source recorded in manifest/gate evidence. | bridge output can override |
| OBL-ZRIG-F6-DEPLOY-SENTINEL | F6 | W10/W11 must prove whether deploy/sentinel config was intentionally supplied, absent, or blocked. | Context provenance and fail-closed event for missing config. | unreachable from normal context |
| OBL-ZRIG-F8-DEPS | F8 | Verification environment must declare runtime/test dependencies before checks are accepted. | `pyproject.toml` deps/extras and install command evidence. | undeclared |
| OBL-ZRIG-F9-FAILOVER | F9 | Wave failover budget must be visible as shared wave authority. | Concurrent-seat test and run event for each substitution. | per-seat/local authority |
| OBL-ZRIG-F14-METRICS | F14 | Metrics triggers must be wired or marked prototype/non-product. | Metrics record attached to run completion or explicit non-product status. | definitions only |

## Event Shape Recommendation

Future implementation may use a small internal event envelope:

```json
{
  "run_id": "HRR-...",
  "wave_id": "W10",
  "authority_surface": "gate",
  "finding": "F1",
  "policy": "fail_closed_missing_specific_evaluator",
  "result": "failed",
  "evidence_path": "runs/.../manifest.json",
  "assurance_level": "bounded_swu_only"
}
```

This is not a Signal Observer bridge contract. It is only a private design target for later engine observability work.

## Acceptance For Future Wiring

- Every emitted event has an engine source, not only a wrapper artifact.
- Failure/degraded states are distinguishable from success.
- Stub/dry-run evidence cannot be presented as live/deploy/sentinel proof.
- Metrics are either wired and tested or explicitly declared non-product.
