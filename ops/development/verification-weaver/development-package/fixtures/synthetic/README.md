# Synthetic Fixture Families

These fixture families are required for the future public package. They must be
synthetic and public-safe.

## Required Families

| Family | Purpose | Owner lane |
| --- | --- | --- |
| `spec-derivation-basic` | DomainSpec-like formalized input with a simple oracle. | `test-derivation` |
| `frontend-ux-basic` | Browser-observable UI behavior with accessibility and layout evidence. | `ux-evidence-validator` |
| `execution-repeatability-basic` | Command manifest and fixture runner with pass/fail receipts. | `experiment-harness` |
| `architecture-gap-basic` | Architecture claim with source-backed testing alignment gap. | `architecture-pattern-inventory` |
| `research-evidence-basic` | Dry-run fixture and claim evidence boundary. | `research-evidence-harness` |
| `mixed-target-basic` | Parent target that decomposes into multiple owner lanes. | `verification-weaver` |
| `unsupported-target-basic` | Target that must fail closed. | `verification-weaver` |

## Fixture Rule

Do not copy private implementation examples. Preserve only public-safe abstract
shape and expected behavior.
