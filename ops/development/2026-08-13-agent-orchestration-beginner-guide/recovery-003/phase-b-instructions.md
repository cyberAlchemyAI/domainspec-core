# Recovery 003 definitional comparison instructions

Work read-only. Read exactly these six repository files and no others:

1. this instruction file;
2. `recovery-003/freeze-binding.json`;
3. the pinned `receipts/synthesis.json`;
4. the preserved `recovery-002/receipts/definitional-freeze-recovery-002.json`;
5. the pinned `receipts/skeptic-precedent.json`;
6. the pinned `receipts/skeptic-non-vacuity.json`.

Do not search the repository, inspect dispatch or recovery documents, consult memory, or read prior comparison output. Attest to the exact read set in your return.

## External binding admission

The parent-owned binding file must have exact SHA-256 `c2766a25f6729378ae52b8e2065c4a22010e23701070cb8fc1e03528a08ef454`. Parse it, then independently hash the preserved frozen receipt. Admit the freeze only when all of these checks pass:

- binding owner is `parent/coordinator`;
- bound artifact path is `ops/development/2026-08-13-agent-orchestration-beginner-guide/recovery-002/receipts/definitional-freeze-recovery-002.json`;
- expected and observed frozen SHA-256 are both `9cb0f28dc5ac28db07ec20d2cf20f64cbaaeaec29ab03ed06f8d179295975cba`;
- expected and observed frozen byte length are both `17862`;
- source action is Recovery 002 `spawn-0001` and its freeze gate is recorded as `gate_pass`;
- the frozen receipt's read-set attestation names only the Phase-A instructions and pinned synthesis;
- the reviewed synthesis digest is `e1014941ea55e97a40a61c294ab48cf38b72b32b654f5bc890bf88a508bf9368` and matches current synthesis bytes.

This is an external binding. Do not require or invent a digest declared inside the frozen file. Block before semantic comparison on any mismatch, unanchored field, extra read, parse failure, or changed byte.

## Comparison

After binding admission, compare the immutable freeze with the supplied precedent and non-vacuity receipts. Preserve the frozen verdict byte-for-byte; do not rewrite it. Return:

- binding-file expected and observed digest;
- frozen-receipt expected and observed digest and byte length;
- exact read-set attestation;
- claim-by-claim agreement, disagreement, and missing coverage;
- disposition of every definitional collapse;
- explicit treatment of precedent `FLAG` rows and the non-vacuity `KILL` of the complete-witness candidate;
- bounded repairs that parent evidence closure can classify as bound, deferred, killed, or unresolved;
- a normalized recovered definitional-review receipt for Recovery 003.

Do not write findings, decide writer admission, replace parent evidence closure, publish, promote, or infer runtime, product, production, or semantic authority.
