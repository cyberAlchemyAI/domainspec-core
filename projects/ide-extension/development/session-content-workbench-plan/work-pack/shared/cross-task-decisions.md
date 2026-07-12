# Cross-Task Decisions

| ID | Decision | Consequence |
| --- | --- | --- |
| DG-SCC-001 | Manual Refresh first, automatic update immediately after. | W1 proves display before W2 EventSource. |
| DG-SCC-002 | Trusted local interactive HTML artifact. | Serve real project `.html`; no Markdown renderer. |
| DG-SCC-003 | Separate active-session publish and event polling. | Content is not attached to terminal result. |
| PD-SCW-001 | One normalized path identifies one logical surface. | Republish preserves surface id and creates a revision. |
| PD-SCW-002 | One global canvas/event stream in V0. | Multi-session routing is deferred. |
| PD-SCW-003 | Cursor poll is at-least-once with stable event ids. | No destructive acknowledgement protocol in V0. |
| PD-SCW-004 | Workspace file remains canonical. | Detect hash drift; defer immutable snapshots. |
