# Definitional and Authority Review — Quine, Willard Van Orman

dispatch_id: `2026-07-30-intent-router-bootstrap-runtime-integration`  
step_id: `s3`  
capability_ref: `research`  
capability_target: `dispatch-sheet.json`  
capability_mode: `review`  
wave_id: `review`  
write_scope: `[]`  
status: `BLOCK`  
artifacts: `[]`  
validation: `Read-only definitional and authority non-collapse review of synthesis.md, research.md, synthesis receipt, three explorer receipts, and only synthesis-cited source selectors. No mutation, runtime execution, fetch, install, generation, or service use.`  
observer_status: `not-invoked-read-only-review`

blockers:

- Receipt and evidence are not adequately distinguished.
- Public extraction, promotion, and release are not modeled as separate authority transitions.
- Dispatch and execution/effect ownership need one explicit non-substitution statement in the proposed integration sequence.

residue:

- `disposition-integrity-vs-receipt-vocabulary`
- `evidence-authority-noncollapse`
- `extraction-promotion-release-gates`
- `dispatch-execution-effect-boundary`

reroute: `Bounded synthesis repair only; no new corpus or implementation is needed.`  
handoff_note: `The architecture is mostly owner-preserving, but the synthesis cannot pass definitional non-collapse until receipt/evidence and extraction/promotion/release are explicitly separated and dispatch is stated not to authorize execution or effects.`

Verdict: `BLOCK`.

## Collapse tests

1. **Bootstrap installation vs native-wrapper generation — PASS.**
2. **Resolver candidate vs ambiguity vs human selection — PASS.**
3. **Human selection vs orchestrator dispatch — PASS.**
4. **Semantic judgment vs object-level inference vs adapter witness — PASS.**
5. **Private authority vs public Arcanum — PASS.**
6. **Receipt vs evidence — FAIL.** The request carries evidence references while the resolver result carries `receipt_digest`. `resolve.mjs:188-192` shows that this is a self-integrity digest over disposition material, while source/support evidence and lifecycle/reasoning receipts have different meanings.

   **Bounded repair:** rename the target field to `disposition_digest`, or formally define existing `receipt_digest` as a non-authorizing integrity checksum that is neither support evidence nor a reasoning/lifecycle receipt. Evidence references retain provenance and admissibility ownership. No digest or receipt existence upgrades candidate confidence or authority.
7. **Extraction vs promotion vs release — FAIL.** The target lifecycle must distinguish:
   - reviewed generic extraction candidate;
   - accepted canonical Arcanum source;
   - promoted generated/runtime package;
   - published release;
   - installed consumer projection.

   **Bounded repair:** add a five-state lifecycle with separate owner, gate, artifact, and witness for each transition. Extraction approval does not equal canonical acceptance; canonical acceptance does not equal promotion; promotion does not equal release; release does not equal installation; installation does not equal deployment or production readiness.
8. **Dispatch vs execution/effect — FAIL narrowly.** Opening or binding a Dispatch must not substitute for execution authorization, and an execution attempt must not substitute for successful effect delivery.

   **Bounded repair:** add one explicit non-substitution sentence and one acceptance fixture proving `selection -> dispatch binding -> authorization gate -> execution attempt -> observed effect/receipt` remain separately recorded and independently fail closed.

The proof ceiling is sound. The block is terminological and authority-contract precision, not rejection of the topology.
