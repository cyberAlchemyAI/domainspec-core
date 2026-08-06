# Runtime evidence contract

Every unit receives nine exact Task Session support outputs: strict Context
Markdown/JSON, closeout preflight, mutation-admission request/receipt, terminal
receipt, closeout-sync request, joined owner receipt, and Continuation Router
receipt. Each unit also writes one exact repository-local continuity cursor.
IRO-001 adds the four Decision Gate artifacts plus `decision-bundle.json`.

The outer chain writes a Goal-start approval receipt, chain config, preflight,
immutable `chain.json`, and ten numbered transition receipts. These paths are
templates in `EXECUTION-CONTRACT.json` and are concretized by the strict
Context/WPRA epoch. They are execution evidence, never owner material.

No Task Session write is admitted unless its strict Context JSON repeats the
complete `materialWrites`, `executionOutputs`, `allowedWrites`, validation,
lifecycle owner, authority, and publication tuple consumed by
`verify-mutation-readiness.py`.
