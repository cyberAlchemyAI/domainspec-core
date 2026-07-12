# Manual Session Bridge Automated Proof Matrix

| Obligation | Primary oracle | Supporting oracle |
| --- | --- | --- |
| Preserve v1 projection and mixed replay | `manual-session-bridge-replay.test.mjs` exact-v1 and mixed-version cases | `manual-session-bridge-contracts.test.mjs` legacy branches |
| Reject invalid task, skill, effects, records, and result shapes | `manual-session-bridge-contracts.test.mjs` hostile fixtures | `l0-runtime-schema-enforcement.test.mjs` raw/runtime validation |
| Fail closed for zero, duplicate, stale, or inconsistent target state | `manual-session-bridge-authorization.test.mjs` singleton/restart/stale cases | `manual-session-bridge-replay.test.mjs` singleton history rejection; CLI empty-ready case |
| Admit exactly one concurrent claim without loser disclosure | `manual-session-bridge-claim-recovery.test.mjs` concurrent claim case | `manual-session-bridge-cli.test.mjs` duplicate claim secrecy |
| Reject wrong session, attempt, skill, status, and evidence bindings | `manual-session-bridge-result.test.mjs` hostile result matrix | `l0-artifact-evidence.test.mjs` path and artifact bindings |
| Reject duplicate or post-terminal transitions without extra receipts | authorization, claim-recovery, and result focused suites | `l0-adversarial.test.mjs` disposition races/replay |
| Rebuild ready, claimed, interrupted, and terminal state after restart | authorization, claim-recovery, result, and replay restart cases | `l0-persistence-recovery.test.mjs` repeated restart/race cases |
| Never project success without durable events and evidence | authorization, claim, and result append-failure cases | `l0-persistence-recovery.test.mjs` and `l0-artifact-evidence.test.mjs` |
| Keep authorization and execution receipts distinct | contracts, authorization, result, and workbench suites | resolvable artifact/evidence route checks |
| Preserve operator/session authority split | claim-recovery and workbench suites | CLI exposes no operator release/target command |

The `npm run test:bridge` command executes every primary and supporting oracle
serially. Playwright and the real blind witness are separate evidence owners.
