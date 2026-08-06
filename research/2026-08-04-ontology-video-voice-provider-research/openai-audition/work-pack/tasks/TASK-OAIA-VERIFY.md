# TASK-OAIA-VERIFY — Technical and spoken fidelity

## Objective

Establish whether the two raw attempts are technically usable and word-for-word faithful while preserving independent timing, word audit, and manual key-phrase evidence.

## Mapping

- Slice: S-VERIFY
- Layer: L2
- Wave: W3
- Sources: `../../DESIGN.md#quality`, `../../IMPLEMENTATION-DETAILS.md#verification-algorithm`, `../../VALIDATION-CONTRACTS.md`
- Dependencies: SWU-OAIA-004 and B-006 closure.
- Current gate: blocked; required local tools were not discovered.

## SWU-OAIA-005 — Technical audio and derivative provenance

- Primary behavior: prove container/format/duration/normalization facts and derivative lineage.
- Independent boundary: can pass without spoken-word analysis.
- Split analysis: inspection and normalization jointly establish the protocol's technical master/derivative contract.
- Write scope: `runtime/lib/verify-audio.mjs`; `runtime/test/verify-audio.test.mjs`; run-scoped technical receipt and derivative paths.
- Done criteria: pinned tool identity/hash/commands; raw hash recheck; WAV metadata; 75–120 seconds; mono/rate/depth gate; two-pass `-16 LUFS-I` and `<= -1 dBTP`; parent/derivative hashes; no raw mutation.
- Acceptance evidence: valid fixture and malformed/truncated/clipped/wrong-format/stale-tool causal negatives; live logs when available.
- Validation: `node --test runtime/test/verify-audio.test.mjs` plus pinned commands recorded by B-006.
- Execution owner: manual.
- Handoff: tool installation is outside this SWU unless separately authorized; stop if the pinned tool contract is absent.

## SWU-OAIA-006 — Independent word and phrase fidelity

- Primary behavior: decide exact spoken fidelity or reject with every mismatch attributable.
- Independent boundary: consumes a technically accepted derivative and emits one fidelity receipt.
- Split analysis: alignment and independent audit must remain separate passes but neither can satisfy the protocol alone.
- Dependencies: SWU-OAIA-005.
- Write scope: `runtime/lib/verify-fidelity.mjs`; `runtime/test/fidelity.test.mjs`; run-scoped alignment, transcript/audit, comparison, and manual-review paths.
- Done criteria: monotonic alignment; independent transcript/audit; normalized token comparison; no unresolved addition/omission/substitution/reorder/low-confidence token; five phrase groups reviewed; wrong “Body War” rejects.
- Acceptance evidence: exact pass plus one-word omission, substitution, low-confidence, reordered phrase, and Body War failure fixtures; signed manual review.
- Validation: `node --test runtime/test/fidelity.test.mjs` plus independent/manual receipt review.
- Execution owner: manual.
- Handoff: never use reference-fed alignment as independent word evidence; never edit text or invent pronunciation repair.

## Synchronization and completion

005 closes before 006. W3 verification is complete only when both repetitions have passing receipts or the candidate has one explicit terminal rejection. Accepted output may proceed to SWU-007 after B-007 closes.
