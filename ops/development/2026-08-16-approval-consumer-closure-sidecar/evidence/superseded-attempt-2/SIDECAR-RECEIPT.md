# Approval Consumer Closure Sidecar Receipt

Status: **staged and validated; not applied**.

## Result

The approval churn was a governance-only workflow defect. R1 reached owner
approval before its exact bytes had crossed Implementation Readiness and Task
Session Until Blocker's WPRA binder. The acceptance builder inventoried a
compatibility report but did not require that report to be current, passing,
no-authority, and bound to the live inputs and consumer versions.

The affected invariant is:

> Acceptance-critical validation must exercise the actual staged bytes through
> every declared downstream consumer before an owner acceptance inventory or
> request can be emitted.

R1 remains frozen at accepted digest
`cb0656f8340c6fbf4a0edd45a7dfa6cd2333d61434b4a2444ec07f46b665aca0`.
Its exact closure replay blocks before acceptance with both noncanonical stop
decisions, canonical IR rejection, zero closeout routes for the 12-unit
frontier, incomplete terminal/closeout unit contracts, and no current WPRA v2
chain binding.

R2 remains frozen and unapproved at digest
`a3e92a87da5e1e80d553eb587b1eabb1ffa6646b25f9df662771024d335b2409`.
Its exact closure replay passes all seven required checks: IR policy 1.1.0,
24 compiled routes, eight canonical stop decisions, 12 Task Session routes,
12 Invoke closeout routes, 12 normalized chain bindings, receipt/closeout
separation, and nonterminal plus terminal successor semantics. No unit was
selected, no mutation occurred, and no configured unit command ran.

## Staged repair

The six-file public Arcanum overlay is enumerated, with preimages and SHA-256
values, in [`candidate/APPLY-MANIFEST.json`](candidate/APPLY-MANIFEST.json).
It adds:

- one exact-byte consumer-closure validator that calls the canonical IR
  initializer and chain binder;
- one closed receipt schema;
- one guarded exclusive writer that rejects missing, blocked, incomplete,
  stale-input, stale-consumer, stale-validator, or authority-bearing receipts;
- ten permanent public guard regressions wired into the existing WPRA fixture
  runner; and
- mandatory choreography in the existing WPRA README.

No duplicate producer-side stop taxonomy is added. The gate reads the canonical
Implementation Readiness taxonomy and invokes that consumer directly.

## Validation

[`evidence/COMMAND-RESULTS.json`](evidence/COMMAND-RESULTS.json) records eight
commands with their argv, stdout, stderr, expected exit, and actual exit. All
matched:

- existing canonical WPRA suite: 24 tests pass;
- new public guard suite: 10 tests pass;
- exact R1/R2 replay suite: 4 tests pass;
- R1 closure: expected exit 2;
- R2 closure: exit 0;
- R1 guarded emission: expected exit 3 and no output;
- R2 synthetic guard probe: exit 0. The probe is explicitly not an acceptance
  request.

The final receipts are
[`R1-CONSUMER-CLOSURE-RECEIPT.json`](evidence/R1-CONSUMER-CLOSURE-RECEIPT.json)
and
[`R2-CONSUMER-CLOSURE-RECEIPT.json`](evidence/R2-CONSUMER-CLOSURE-RECEIPT.json).

The terminal compatibility probe uses the canonical chain semantic function.
Future dependency receipts do not exist before acceptance, so the final-unit
dependency byte lookup is shape-only in this probe; dependency IDs, declared
paths, receipt shape, and terminal successor semantics are still checked.
Execution-time exact dependency bytes remain the chain's responsibility.

## Owner gate and required revalidation

Fresh owner acceptance is required for the exact six-file public repair before
canonical apply or promotion. R2 remains a separate unapproved epoch. The old
R1 approval cannot stretch over either the repair or R2, and this sidecar does
not introduce semantic-equivalence approval carry-forward.

After that repair acceptance, the apply owner must:

1. recheck the apply-manifest preimages and create-target absences;
2. assemble the exact candidate into canonical Arcanum and run the full WPRA
   fixture runner on those bytes;
3. replay R1 as a pre-acceptance block and an R2-equivalent input as a seven-check
   pass;
4. run
   `arcanum/tools/sync-generated-skill-package.sh --target . --spell work-pack-readiness-audit --profiles repo-codex,claude --apply`
   and verify source/generated parity—`arcanum` remains canonical while
   `.agents` and `.claude` are generated;
5. regenerate changed-byte, input, consumer, validator, and schema hashes; and
6. create only an unpublished epoch draft, then let the current passing guard
   be its exclusive writer before asking the owner.

No new approval was requested here. No canonical Arcanum, generated skill,
R1, R2, product, telemetry, Git, or external-system write was performed by the
sidecar. Concurrent Arcanum and telemetry dirt exists in the shared worktree;
it was left untouched.

Claim ceiling: staged local governance repair and exact-byte compatibility
evidence only—no apply, promotion, approval, selection, admission, product
execution, publication, deployment, release, or production proof.
