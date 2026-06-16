Artifact written to: /home/vrondelli/projects/domainspec-core/implementation/domainspec/docs/features/ui-prototyping-studio/development/refinement-runs/20260615T205403Z-mutation-execution-mechanics/stages/06-design.md

Covers all 7 required sections:
1. Execution model — 4 lanes (synthesis / Claude Code proposer / pure validator / recorder); D1-D2 keep generation the only impure lane, strictly upstream of admission, value-in/value-out across the CLI seam; sessionContext bounded (F2 closed).
2. WHERE DETERMINISM LIVES — D3: validator/recorder lane in the pure core; D3a purity obligations, D3b one shared canonicalizer, D3c determinism at admission not production.
3. Schema changes — GAP-1 (odId + typed MutationChangeType on MutationTask), DiffSummaryHonest with per-od-id OdDiffFragment unit (D5, buildDiffSummary deleted), GAP-2 (htmlArtifactRef + candidateHtmlHash + provenance on RevisionManifestEntry), ExecutionProvenance shape (F9).
4. Apply state machine — D7 activates the dormant RevisionApplied as the preview/saw-the-diff gate; D8 two gates (approve-intent + accept-diff); D9-D10 fail-closed reject + bounded retry + deferred repair (O1); D11-D13 produce-then-persist, whole-batch all-or-nothing, hash-bound idempotency-at-verdict; D14 composite admission rule.
5. Validator set — V1-V9b adopted verbatim from s6 with required/soft criticality, deterministic run order, two A-mechanics imported (V9b + same-od-id conflict).
6. Engine contract — D15: frozen ProposeInput envelope (hashed to promptHash) in, ProposeOutput candidate out; engine forbidden the store/clock/record path.
7. INV-3/4/5/6/8 + saw-the-diff — mapped to concrete code-enforced analogues and new mechanics.

Honors C's s5 conditional verdict: C-1 (->B) and C-2 (->A) are reachable as configuration from the same machine (O2/O3), no redesign.