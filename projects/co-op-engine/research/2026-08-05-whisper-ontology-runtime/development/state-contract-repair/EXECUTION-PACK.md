# Execution Pack

Selected unit: `SWU-WHISPER-RSCH-STATE-001`.

The Task Session entry must bind `WORK-PACK.md`, the selected task, a strict context pack, `ARCHITECTURE.md`, `VALIDATION-CONTRACTS.json`, exact absent baselines for all six material targets, and the current prior research digests. The material package must reproduce the same write and validation sets.

Execution order inside the admitted unit:

1. confirm baselines and immutable source digests;
2. create all six candidate material files as one bounded change;
3. run the three validation contracts;
4. rerun the checker and compare deterministic receipt bytes;
5. emit terminal Task Session receipt and stop at the research-closeout cursor.

No successor is automatic. The research closeout is eligible only after the terminal receipt passes its own evidence checks.
