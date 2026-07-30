# TASK-CLOSURE — Terminal Verification And Audit Receipts

These are output-only/audit-only contracts. They do not repair source
findings and must never declare placeholder material writes.

## TASK-VERIFY

- Primary behavior: verify every required SWU terminal receipt, digest,
  command result, artifact, teardown result, and successor boundary.
- Dependencies: `SWU-OFSP-025`.
- Material writes: none.
- Execution output:
  `work-pack/closeout/TASK-VERIFY.receipt.json`.
- Validation argv: see
  `../shared/COMMAND-MATRIX.json#TASK-VERIFY`.
- Acceptance: output validates against the terminal schema and semantic
  validator; findings block and are never repaired here.
- Successor: `TASK-AUDIT-ALIGNMENT`.

## TASK-AUDIT-ALIGNMENT

- Primary behavior: audit exact spec/design/work-pack/terminal-evidence
  alignment without changing any source.
- Dependencies: `TASK-VERIFY`.
- Material writes: none.
- Execution output:
  `work-pack/closeout/TASK-AUDIT-ALIGNMENT.receipt.json`.
- Validation argv: see
  `../shared/COMMAND-MATRIX.json#TASK-AUDIT-ALIGNMENT`.
- Acceptance: every claim maps to exact current evidence; ambiguity
  blocks and no plan or implementation file is repaired.
- Successor: `TASK-AUDIT-LAYERING`.

## TASK-AUDIT-LAYERING

- Primary behavior: audit owner, layer, authority, publication, and
  candidate-local claim ceilings without changing any source.
- Dependencies: `TASK-AUDIT-ALIGNMENT`.
- Material writes: none.
- Execution output:
  `work-pack/closeout/TASK-AUDIT-LAYERING.receipt.json`.
- Validation argv: see
  `../shared/COMMAND-MATRIX.json#TASK-AUDIT-LAYERING`.
- Acceptance: every boundary passes; findings block and remain owned by
  their lifecycle owner.
- Successor: `SWU-OFSP-026`.

## Runtime Admission Gap

The live Task Session `routed-mutation` request requires at least one
material write. These tasks truthfully have none. They remain
runtime-blocked until the Task Session lifecycle owner admits a bounded
output-only/audit-only mode. This plan does not fabricate a material
path to bypass that gate.
