## s6 Validator Model — Mutation Execution Mechanics

Artifact written to:
`/home/vrondelli/projects/domainspec-core/implementation/domainspec/docs/features/ui-prototyping-studio/development/refinement-runs/20260615T205403Z-mutation-execution-mechanics/stages/06-validator-model.md`

### Where determinism MUST live (approach-independent)
In the **validator/recorder lane inside the pure orchestration core** — never in the producer, never in the persist step alone. Grounded: the core (`apply-approved-batch.ts`, `synthesize-mutation-batch.ts`) is already LLM-free/port-only (s1 §4); the existing `sha256` checksum binds inputs only (F3) and `createdAt = new Date()` is wall-clock — so only the validators can bind a candidate HTML to the contract. Two purity obligations: no clock/entropy, and canonical-parse comparison (not byte compare).

### The deterministic validator set (each: input · rule · check · failure code)
- **V1 target-exists** — anchor resolves to exactly one element in currentHtml → `MUTATION_VALIDATOR_TARGET_NOT_FOUND`
- **V2 target-changed** — addressed subtree hash differs current→candidate → `MUTATION_VALIDATOR_TARGET_UNCHANGED`
- **V3 no-out-of-scope-change** (scope-bounded) — `ChangedSet ⊆ (TaskScope ∪ S)` via symmetric set-diff of `odIndex` → `MUTATION_VALIDATOR_OUT_OF_SCOPE_CHANGE`
- **V4 data-od-id-preserved** — dropped/appeared od-ids ⊆ owned removal/addition tasks → `MUTATION_VALIDATOR_ODID_NOT_PRESERVED`
- **V5 acceptanceText-satisfiable-proxy** — structural shadow keyed on changeType (add⇒+nodes, remove⇒absent, change⇒hash-differs-and-exists); intent never re-parsed (G7) → `MUTATION_VALIDATOR_ACCEPTANCE_PROXY_UNMET` (soft/pivotal)
- **V6 well-formed-HTML** — parse + parse-reparse fixpoint → `MUTATION_VALIDATOR_MALFORMED_HTML`
- **V7 text-escaped/sanitized** — no *new* injection vector vs current; escaped round-trip → `MUTATION_VALIDATOR_UNSAFE_CONTENT`
- **V8 idempotency** (of the suite) — double-run verdict-hash equality, clock-free → `MUTATION_VALIDATOR_NONDETERMINISTIC` (this is what makes replay-by-verdict true)
- **V9 diff-bounded** — `changeMagnitude <= B(taskCount)`, fixed monotone bound → `MUTATION_VALIDATOR_DIFF_OUT_OF_BOUNDS`
- **V9b ops-vs-output-reconciliation** — opportunistic, A-subset only → `MUTATION_VALIDATOR_OPS_OUTPUT_MISMATCH`

### Calibration fidelity to prior stages
- Approach-independent (per the charge): same validators/codes/determinism-location under A (thin backstop), B (the missing fail-closed gate — "B-with-this-set is C"), C (load-bearing admission boundary).
- Honors F3 (excludes `createdAt` from validator hashes), F4/F7 (honest diff is a byproduct of V2, not a B/C differentiator), F6 (fail-closed default, validate-then-persist), G7 (V5 never reinterprets intent).
- Wires the s5 condition **C-1** explicitly: V5 + V3 tightness are the documented soft-degradation levers that flip C→B; **C-2** supported via V9b becoming routinely applicable.
- Codes use the existing `createUiPrototypingStudioError(...)` SCREAMING_SNAKE convention, prefixed `MUTATION_VALIDATOR_*` for grep-isolation.

### Determinism budget (honest about the s5 "auditability 4 not 5")
Reproducible: admission *verdict* (replay-by-verdict, all approaches via V8); byte-identical candidate only under A (replay-by-rerun). Not reproducible: the B/C proposal itself — the set makes it *safe + auditable*, not deterministic.

### Hard prerequisites (carried, not re-decided)
GAP-1 (od-id into MutationTask) for V2/V3/V4/V5/V9 at od-id granularity; GAP-2 (HTML pointer+hash on RevisionManifestEntry) for replay-by-record; ExecutionProvenance must carry per-validator verdicts.