# Context Pack: SWU-SCW-008

## Selection

- Task/SWU: `TASK-VALUE-WITNESSES / SWU-SCW-008`
- Mode: live local Task Session
- Dependency: SWU-SCW-007 PASS

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Active Codex authors a new standalone presentation. | Live-session procedure. | covered |
| O2 | CLI publishes the real project file without copy/paste. | SWU procedure. | covered |
| O3 | Open workbench displays the first revision. | Browser witness. | covered |
| O4 | Active Codex changes the file and republishes while browser stays open. | SWU procedure. | covered |
| O5 | Browser automatically swaps to the second complete revision. | Done criteria. | covered |
| O6 | Retain path/hash/CLI/browser evidence and human value judgment. | Done criteria. | partial-human-gate |

## Execution Decisions

- Place the generated presentation and witness assets inside the approved
  `SWU-SCW-008` evidence folder.
- Use a dedicated persistent witness state and port so existing local Approval
  Desk state is not changed.
- Keep one Chromium page open between the two CLI publishes; the witness waits
  for a changed iframe revision id and revised visible content.
- Stop at the human usefulness judgment rather than manufacturing it.

## Gates

- Dependency/context/write scope: pass.
- Live Codex/browser availability: pass.
- Human value review: pending.

## Required Evidence

- Initial and revised CLI JSON responses with distinct revision ids/hashes.
- Initial and final browser screenshots from one continuous page.
- Browser witness JSON binding both observed revisions.
- Human judgment comparing this loop with chat-only output.
