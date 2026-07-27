# Cross-Task Decisions

| Decision | Binding |
| --- | --- |
| P-01 | Browser whole/region versions are opaque; server construction and contract tests own canonical digest coherence. |
| P-02 | Projection and compatibility fields derive from one accepted coherent snapshot. |
| P-03 | Poll-only calls coalesce; action completion joining an older flight queues one trailing refresh. |
| P-04 | Changed regions and local-context effects prepare before commit; any partial failure restores prior mounts, context, and applied versions. |
| P-05 | Six semantic region identities are stable Design targets, but each region is a separate SWU. |
| P-06 | SWUs sharing `studio.ts` or the workbench shell run serially. |
| P-07 | No framework, push transport, durable draft authority, remote origin, or lifecycle vocabulary change. |
| P-08 | `selected_swu: none` until the human separately authorizes one candidate. |
