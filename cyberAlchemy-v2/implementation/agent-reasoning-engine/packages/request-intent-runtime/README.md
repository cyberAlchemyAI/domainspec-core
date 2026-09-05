# ARE Request Intent Runtime

This package compiles one request plus bounded reusable reasoning context into
an immutable Intent Contract. It distinguishes instructions about constructing
an artifact from content that should appear in the artifact, binds conversational
references, classifies corrections, materializes reflections, and projects the
same state at `quiet`, `explain`, `inspect`, or `control` depth.

The runtime owns interpretation records. It does not own routing, transport,
reasoning-state storage, benchmark promotion, or engine upgrades. Model-backed
interpretation is an optional provider behind the same verified record boundary;
the default fast path makes zero provider calls.

Public operations include:

- `compileRequestIntent`
- `materializeIntentContract` and `verifyIntentContract`
- `assessIntentRealization`
- `detectCorrection` and `materializeIntentReflection`
- `applyReflectionDisposition`
- `projectIntentInspection` and `applyIntentControl`
- `appendIntentLifecycleEvents`
- `toImprovementSignalCandidate`
- `materializeObjectiveState`, `verifyObjectiveState`, and `resolveObjectiveTransition`
- `materializeRequirementSnapshot`, `verifyRequirementSnapshot`, and `assessRequirementChange`

The opt-in [requirement-change contract](REQUIREMENT-CHANGE.md) preserves explicit
retained/added/removed requirements across active-objective continuation and
refinement. It does not infer semantic correctness or change wrapper defaults.

The [objective-resolution prototype](OBJECTIVE-RESOLUTION.md) adds scoped active
and suspended objectives, immutable transitions, and an optional bounded provider.
It is a library prototype: Codex preflight and persistent reasoning-state integration
remain the next construction steps. No wrapper behavior changes in this slice.

Run with Node v26.8.1:

```text
npm test
npm run benchmark
npm run benchmark:objectives
```

All returned records are canonical, deeply frozen, digest-bound, and carry
`authority_effect: none`.
