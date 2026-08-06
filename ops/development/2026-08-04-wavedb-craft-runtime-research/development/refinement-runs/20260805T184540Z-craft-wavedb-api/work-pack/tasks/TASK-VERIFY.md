# TASK-VERIFY — Closure audit

SWU-exempt closure task. After all admitted mutation SWUs, independently verify:

- source ledgers and experiment inputs are byte-unchanged;
- every implementation file is inside the owner-approved private root;
- all unit, fixture, contract, negative, resource, and fresh-process checks pass;
- no write/refresh/rebuild/replacement route or WaveDB writer is reachable;
- every completed Task Session has an accepted Invoke Refresh closeout;
- claims remain candidate-local and derived, with no deployment/publication;
- unresolved locking, OS sealing, replacement, recovery, environment matrix,
  real authentication, and legacy adapter gaps remain explicit.

This task cannot convert test success into deployment, production, authority, or
source-truth evidence.
