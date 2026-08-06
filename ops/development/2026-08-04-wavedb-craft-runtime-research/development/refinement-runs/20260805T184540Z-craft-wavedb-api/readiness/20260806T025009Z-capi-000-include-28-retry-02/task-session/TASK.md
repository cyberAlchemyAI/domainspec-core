# TASK-RUNTIME / SWU-CAPI-000 — One-unit automatic execution

Status: selected, not yet admitted. Authority class: private. Publication class:
internal. Lifecycle owner: `experiment-harness`.

## Objective

Create one new immutable derived WaveDB snapshot at attempt
`wcli-20260805-node26-0.15.9-02` from the exact selected 28-ledger scope: the
preserved 27-ledger baseline plus
`projects/cyberalchemy-orchestrator/tools/test-derivation-engine/.craft/ledger.yml`
at SHA-256
`0effd055c9f25ea3e46de7e5280585f987e9734411ae1639d9c53171b8ed6b84`.
Use the already verified local `@vijayee/wavedb@0.15.9` package under Node
`v26.6.0`; do not access the network.

## Exact mutation boundary

- Material: the new attempt-local `import-ledgers-byte-normalized.js` only.
- Execution output: the new attempt-local WaveDB `store/` and `receipt.json`
  only.
- Source `.craft/ledger.yml` files, prior attempts, API code, public Craft code,
  NVM defaults, Git history/index, publication, and deployment are forbidden
  mutation targets.

## Acceptance

- The discovered Craft inventory is exactly the selected 28-ledger manifest,
  with no added, removed, or byte-drifted ledger.
- The builder writes exactly 57 records with sequential awaited puts and an
  explicit flush/close.
- Every record is read back byte-for-byte immediately and after same-process
  reopen.
- Node, package, tarball, diagnostic receipt, Task Session receipt, and native
  addon identities match their frozen SHA-256/SRI values.
- Protected scope snapshots are identical before and after execution.
- A structured pass or block receipt is retained. Failed attempt `-01` remains
  byte-identical, and no successor is selected.

## Closeout

A passing experiment receipt still requires Task Session terminal evidence and
the Work Pack's `invoke:refresh:apply-approved` synchronization. This one-unit
loop terminates after `SWU-CAPI-000`; it does not admit `SWU-CAPI-001`.
