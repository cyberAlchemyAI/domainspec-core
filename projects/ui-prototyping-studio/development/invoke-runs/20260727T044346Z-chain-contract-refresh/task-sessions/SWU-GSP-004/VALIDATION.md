# SWU-GSP-004 Validation

- Material package: `pass`
- Mutation admission: `admit`
- Exact applied material parity: `9/9`
- TypeScript no-emit check: `pass`
- Full unit/slice suite: `71/71 pass`
- Focused CSS-only browser witness: `1/1 pass`

The CSS-only candidate has zero per-component structural counts but non-zero
visible-change evidence. Its explicit `style` lane is projected in `/state`,
rendered separately in preview, stored on the accepted revision, and carried
into the exported handoff. Unattributed structural evidence also has its own
lane; no selector-to-component ownership is invented.
