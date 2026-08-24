# TASK-RUNTIME / SWU-CAPI-000 — Fresh `-03` staged-filter repair

Status: selected, not yet admitted. Authority class: private. Publication class:
internal. Lifecycle owner: `task-session-local-experiment-runner`.

## Objective

Create one new immutable derived WaveDB snapshot at attempt
`wcli-20260805-node26-0.15.9-03` from the exact selected 28-ledger scope after
excluding every candidate path that contains a literal `staged` directory
component. Use the already verified local `@vijayee/wavedb@0.15.9` package
under Node `v26.6.0`; do not access the network.

## Exact mutation boundary

- Material: the new attempt-local `import-ledgers-byte-normalized.js` only.
- Execution output: the new attempt-local WaveDB `store/` and `receipt.json`
  only.
- The builder must differ from immutable `-02` only by the attempt identity and
  adding `staged` to its discovery exclusion set.
- Source `.craft/ledger.yml` files, prior attempts, API code, public Craft code,
  NVM defaults, Git history/index, publication, and deployment are forbidden
  mutation targets.

## Acceptance

- The discovered Craft inventory is exactly the selected 28-ledger manifest,
  with no generated `staged/` copy and no added, removed, or byte-drifted source.
- The builder writes exactly 57 records with sequential awaited puts and an
  explicit flush/close.
- Every record is read back byte-for-byte immediately and after same-process
  reopen.
- Node, package, tarball, diagnostic receipt, Task Session receipt, and native
  addon identities match their frozen SHA-256/SRI values.
- Protected source snapshots are identical before and after execution.
- A structured pass or block receipt is retained. Attempts `-01` and `-02`
  remain byte-identical, and no successor is selected.

## Closeout

A passing experiment receipt still requires Task Session terminal evidence and
the Work Pack's `invoke:refresh:apply-approved` synchronization. This one-unit
loop terminates after `SWU-CAPI-000`; it does not admit `SWU-CAPI-001`.
