# Cross-Task Decisions

| Decision ID | Selection | Rationale | Consequence |
| --- | --- | --- | --- |
| DEC-IDEAD-001 | Record `local_operator_action` with `assurance: unattested`; accept no caller-selected approver identity. | L0 needs honest attribution, not authentication theater. | Effectful L1 remains blocked until kernel-attested principal/session separation exists. |
| DEC-IDEAD-002 | Use immutable ID-addressed envelopes and approval records; keep `current_envelope` only as an optional derived selection if retained. | Multiple pending proposals must remain reachable. | API and UI select by envelope/approval ID. |
| DEC-IDEAD-003 | Approval and rejection are terminal compare-and-transition commands. | Exactly-once disposition is the L0 authority boundary. | Replays and conflicting dispositions return a stable conflict without writes. |
| DEC-IDEAD-004 | Use Ajv's Draft 2020-12 class behind a local `schema-validation.mjs` adapter. | Existing schemas declare Draft 2020-12; official Ajv docs require the dedicated export. | Library API remains isolated and package-lock pinned. |
| DEC-IDEAD-005 | Treat the event log as authoritative mutation history and `workbench.json` as a rebuildable projection. | This gives one recovery direction after partial projection writes. | Startup/read reconciliation replays committed events before serving state. |
| DEC-IDEAD-006 | Commit one complete disposition event after exclusive evidence artifacts exist; update projection afterward. | An event can rebuild state; orphan artifacts are non-authoritative and detectable. | No receipt is authoritative unless present in a committed event. |
| DEC-IDEAD-007 | Keep the frontend framework-free for L0. | The current single HTML page is sufficient and minimizes migration risk. | Add accessible semantic controls and stable selectors in-place. |

## Rejected Alternatives

- Trust `approved_by` from the browser: rejected because it repeats AR-CAND-001.
- Add login/authentication in L0: rejected as premature and insufficient for effectful actor separation.
- Use the workbench JSON file as sole authority: rejected because current races already diverge it from events.
- Adopt Electron, Nimbalyst, or a database: rejected because none is needed for the local pilot decision.
- Begin with Playwright polish: rejected because browser evidence over a defective kernel would only prove the wrong behavior more convincingly.
