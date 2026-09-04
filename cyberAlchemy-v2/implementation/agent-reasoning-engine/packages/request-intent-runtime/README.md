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

Run with Node v26.8.1:

```text
npm test
npm run benchmark
```

All returned records are canonical, deeply frozen, digest-bound, and carry
`authority_effect: none`.
