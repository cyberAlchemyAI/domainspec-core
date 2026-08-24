# Orchestrate Capacity-Aware Admission

This is a private Invoke Define, Design, and Plan package for a public Arcanum
Orchestrate update. It responds to the 2026-08-03 native dispatch that reached
`wave_ready`, spawned two agents, then failed its third spawn with
`agent thread limit reached`.

The package does not implement the update. It separates four claims:

1. a host can describe capacity;
2. Orchestrate can decide whether an entire wave is admissible;
3. a reservation can make that decision race-safe;
4. a logical agent close proves physical slot release.

Only the first two are in the active L0/L1 implementation window. Reservation,
release, and reuse remain host-owner extensions until an exact native contract
exists.

## Start here

- [Context pack](CONTEXT-PACK.md)
- [Intent record](INTENT-RECORD.md)
- [Define specification](define/SPEC.md)
- [Design architecture](design/ARCHITECTURE.md)
- [Implementation layering](planning/IMPLEMENTATION-LAYERING.md)
- [Work Pack](planning/WORK-PACK.md)
- [Execution pack](planning/EXECUTION-PACK.md)
- [Validation strategy](planning/VALIDATION-STRATEGY.md)
- [SWU manifest](planning/SWU-MANIFEST.json)
- [Closeout sync inventory](planning/CLOSEOUT-SYNC-INVENTORY.json)
- [Mutation admission contract](planning/MUTATION-ADMISSION-CONTRACT.json)
- [First selected unit](planning/work-pack/tasks/TASK-OCA-01-ADMISSION-SEAM.md)
- [Wave index and choreography](planning/EXECUTION-PACK.md#wave-order)
- [Dispatch and validation](DISPATCH.json)
- [Authoring validation](AUTHORING-VALIDATION.md)
- [Invoke result](INVOKE-RESULT.md)

## Claim ceiling

This package may prove authoring and deterministic validation only. It does not
prove a live host capacity API, reservation, physical release, successful
dispatch recovery, generated-surface synchronization, deployment, or
production readiness.
