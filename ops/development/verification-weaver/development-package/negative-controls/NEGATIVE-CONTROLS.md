# Negative Controls

Each negative control must fail closed or produce explicit residue. Each future
fixture must include input, expected receipt fields, owning lane, and block/flag
rule.

| Control | Input condition | Owning lane | Expected `VERIFICATION-WEAVE` fields | Rule |
| --- | --- | --- | --- | --- |
| `NC-MIX-001` | Mixed formal spec, frontend route, research SWU, and architecture folder in one target. | parent router | `target_kind: mixed`; `classification.decomposition.required: true`; child lanes listed or gap recorded. | Block if not split into lane receipts. |
| `NC-UNSUPPORTED-001` | Arbitrary file with no recognized oracle. | parent router | `target_kind: unsupported`; `unsupported_reason` present; `status: block`. | Block unsupported. |
| `NC-PRIVATE-001` | Private path target used as public fixture input. | parent public-safety scan | `public_safety.private_path_scan: block`; gap owner `verification-weaver`. | Block or redact before public output. |
| `NC-GENERATED-001` | Generated outputs, run reports, local Playwright output, or observability logs as promotion input. | parent public-safety scan | `public_safety.generated_output_scan: block`; `promotion_action: none`; `status: block`. | Block promotion evidence. |
| `NC-NO-ORACLE-001` | Formal obligation with no checker, fixture, browser evidence, human review, research run data, or explicit gap. | `test-derivation` | `classification.oracle_type: null`; gap reason `missing_oracle`; `status: block`. | Block. |
| `NC-UX-HUMAN-001` | Mechanically passing UI with unresolved human comprehension risk. | `ux-evidence-validator` | `target_kind: frontend_ux`; residue owner `ux-evidence-validator`; `status: flag`. | Flag human residue, not pass. |
| `NC-UX-DENSE-001` | Dense expert UI intentionally scan-heavy but grouped and keyboard-operable. | `ux-evidence-validator` | soft residue or false-positive note; `status: flag` or lane-specific pass-with-flags. | Do not hard-block by density alone. |
| `NC-E2E-FLAKE-001` | Font, data, time, network, animation, or browser instability affects evidence. | `experiment-harness` | gap reason `flaky_evidence`; `status: block`. | Block promotion evidence. |
| `NC-ADAPTER-001` | Unsupported CLI flags or missing browser/runtime. | `experiment-harness` | lane status `block`; gap reason `adapter_failure`; `status: block`. | No evidence upgrade. |
| `NC-RESEARCH-DRYRUN-001` | Synthetic dry-run fixture attempts research claim promotion. | `research-evidence-harness` | `promotion_action: none`; residue `dry_run_only`; `status: flag` or `block`. | Block evidence-status upgrade. |
| `NC-ARCH-FOLDER-ONLY-001` | Architecture claim inferred from folder names only. | `architecture-pattern-inventory` | gap reason `insufficient_source_evidence`; `status: flag`. | Route to architecture inventory. |
| `NC-RECEIPT-PROMOTE-001` | Parent receipt marks registry-ready or promoted. | parent router | `promotion_action` invalid; `status: block`. | Parent receipt cannot promote. |
