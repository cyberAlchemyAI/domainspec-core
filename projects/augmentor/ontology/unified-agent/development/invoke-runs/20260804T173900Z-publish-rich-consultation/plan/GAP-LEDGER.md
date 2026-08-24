# Gap and Residue Ledger

| ID | State | Owner | Resolution or next route |
| --- | --- | --- | --- |
| G-01 | closed by design | deployment packager owner | Current two-file packaging is incompatible with the seven-file loader; repair in AUGPUB-001. |
| G-02 | planned evidence | validation owner | Prove missing/mixed bundle failures before SSH in AUGPUB-001/003. |
| G-03 | explicit gate | production operator | Authorize exact candidate and rollback only after AUGPUB-003. |
| G-04 | possible residue | human operator | Public authenticated browser replay may remain unrun because the plaintext password is intentionally unavailable to the agent. |
| G-05 | monitoring residue | production operator | Observe post-release health after closeout; no monitoring platform change is included. |

No unresolved ambiguity blocks the plan. G-03 is required later authority, and
G-04 is a deliberately separated evidence layer.

