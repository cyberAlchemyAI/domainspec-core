# Non-vacuity review

Verdict: `FAIL`. Evidence closure must stop before writer admission.

## Denominator defects

- `2/2` transports is false under the pinned README: it lists stdio, WebSocket, Unix socket, and `off`; excluding `off` still leaves three transport mechanisms.
- The synthesis client-request group counts sum to 139, contradicting 137.
- Notification family counts sum to 73, contradicting 72.
- Server requests remain explicitly conflicting: 9 current versus 11 including deprecated variants.
- The 58 schemas, 14 generated packages, and eval evidence are aggregate-only and lack a row ledger proving one classification per member.

Repair owner: protocol inventory plus Experiment Harness denominator-oracle owner; regenerate exact row matrices and arithmetic from the pinned source, with current/deprecated/excluded status and installed-binary parity.

## Required trace defects

None of the nine traces supplies the required exact identities, immutable inputs/digests, policies, ordered events, gates, receipts, first stop, forbidden effects, and proof status:

1. Refine stage: no selected stage, digest, event, gate, receipt, or stop.
2. Invoke-to-Task-Session SWU: no Work-Pack/SWU/ticket/attempt IDs, concrete policy, events, receipts, or stop.
3. Goal/Craft round: no round/node ID, ledger/frontier/receipt/delta hashes, approval token, threshold, or stop receipt.
4. Permission pause: no request/thread/turn IDs, profile, events, frozen admission digest, or receipt.
5. Stale digest: no old/new values, epoch/binding IDs, detection event, rejection receipt, or forbidden replay.
6. Interrupt/resume: no correlated interrupt-terminal-reconcile-resume trace or residue receipt.
7. Replay rejection: no key values, event IDs, mismatch field, journal decision, or blocked effect.
8. Failed closeout: no execution/owner receipts, join, failing invariant/event, terminal state, or forbidden cursor.
9. No progress: no threshold, repeated hashes, round IDs, stop event, or terminal Goal receipt.

The global `specified but unexecuted` ceiling is not a witness or closed negative. The canary matrix confirms the App Server cases are absent.

First stop: non-vacuity evidence closure. Writer admission remains forbidden until denominators and nine traces are closed.

## Terminal recheck

`PASS`. The repaired synthesis closes the declared official protocol denominators, leaves the aggregate local ledgers explicitly open, and supplies nine exact `specified-unexecuted` fixture contracts. F-04 is single-valued and F-06 makes `thread/resume` recovery-only.
