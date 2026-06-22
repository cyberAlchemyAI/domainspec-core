# Output Contract: VERIFICATION-WEAVE

`VERIFICATION-WEAVE` is a parent receipt. It records how a testing target was
routed and what owner receipts or gaps resulted.

## Minimal Shape

```yaml
schema_version: "0.1.0"
receipt_type: VERIFICATION-WEAVE
run_id: "<timestamp-or-stable-id>"
target:
  id: "<stable-target-id>"
  target_kind: "spec_derivation|frontend_ux|execution_repeatability|architecture_gap|research_evidence|mixed|unsupported"
  source_refs:
    - "<path-or-public-safe-handle>"
  unsupported_reason: null
classification:
  oracle_type: "deterministic_derivation|fixture_runner|proof_checker|browser_evidence|human_review|research_run_data|explicit_gap|null"
  decomposition:
    required: false
    child_targets: []
lanes:
  - owner_capability_ref: "arcanum/arcana/test-derivation"
    owner_status: "draft|seed|registered|public-sigil|unknown"
    owned_verb: "derive"
    input_contract: "<owner-native-input>"
    output_receipt: "<path-or-handle>"
    status: "pass|flag|block|not_run"
    promotion_boundary: "owner-gated"
obligations:
  - id: "<stable-id>"
    owner: "<owner-capability>"
    source_ref: "<source-or-public-safe-handle>"
    expected_evidence: "<artifact-or-gap>"
evidence:
  - id: "<stable-id>"
    owner: "<owner-capability>"
    artifact: "<path-or-handle>"
    provenance: "<how-created>"
gaps:
  - id: "<stable-id>"
    owner: "<owner-capability>"
    reason: "<missing-or-failed-evidence>"
    next_route: "<owner-or-block>"
residue:
  - id: "<stable-id>"
    owner: "<owner-capability-or-parent>"
    note: "<unresolved-material>"
status: "pass|flag|block"
promotion_action: "none|candidate-request"
public_safety:
  private_path_scan: "pass|flag|block|not_run"
  generated_output_scan: "pass|flag|block|not_run"
  notes: []
next_route:
  recommended_owner: "<capability-or-none>"
  reason: "<short>"
```

## Hard Rules

- `promotion_action` must never be `promote`.
- `lanes[*].status` must be native owner status or `not_run`.
- `status=pass` requires every selected lane to pass or be explicitly
  non-required.
- `status=flag` requires residue or soft evidence limits.
- `status=block` is required for unsupported targets, private leaks, missing
  oracle, generated-only proof, flaky evidence, or adapter failure.
- Public-safe receipts must not include private implementation paths as fixture
  evidence.

## Allowed Owner Lanes

- `arcanum/arcana/test-derivation`
- `arcanum/arcana/ux-evidence-validator`
- `arcanum/arcana/experiment-harness`
- `arcanum/arcana/architecture-pattern-inventory`
- `arcanum/arcana/research-evidence-harness`

More lanes require an explicit design update.
