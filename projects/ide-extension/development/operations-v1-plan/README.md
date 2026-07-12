# Operations V1 Plan

Governed, non-executed implementation package for the accepted Operations V1
HTML builder architecture.

## Entrypoints

- [Work pack](WORK-PACK.md)
- [Implementation layering](IMPLEMENTATION-LAYERING.md)
- [Execution pack](EXECUTION-PACK.md)
- [Plan transport](PLAN-TRANSPORT.md)
- [Distill validation](DISTILL-VALIDATION.md)
- [Invoke result](INVOKE-RESULT.md)
- [Dispatch](operations-v1-plan.dispatch.json)

## State

- Planning gate: `pass`
- Complexity: `medium`
- Output mode: `split`
- Active implementation window: L0 through L2
- First executable unit: `SWU-OV1-001`
- Implementation performed by this package: none

Execution must use Task Session on exactly one ready SWU and synchronize its
receipt back into the work pack before the next SWU starts.
