# W0: Closed Contracts

- Layer question: are the projection, command, event, receipt, status, and code
  languages closed before behavior or storage exists?
- Ordered units: SWU-AKVE-001 → SWU-AKVE-002.
- Task: [TASK-AKVE-01](../tasks/TASK-AKVE-01-CONTRACTS.md).
- Entry: readiness audit passes and the user selects SWU-AKVE-001.
- Gate between units: terminal, owner, and Continuation Router receipts for 001.
- Exit: all positive/negative schema fixtures pass; no implementation module or
  current vault artifact changed.
- Parallelization: none; 002 consumes the exact 001 allowlist vocabulary.

