# SWU-GSP-003 Validation

- Material package: `pass`
- Mutation admission: `admit`
- Exact applied material parity: `4/4`
- TypeScript no-emit check: `pass`
- Full unit/slice suite: `68/68 pass`
- First focused browser run: `1/2`; external Accept occurred before the poll
  established its initial signature, so the page did not reload.
- Rework: embed the render-time state/head/staged signature.
- Final focused browser run: `2/2 pass`

Current head is now the primary preview. Annotation uses the same current HTML
and revision ID. Historical variants are labeled as lineage/reference.
`/state` retains its previous top-level signal and includes the serializable
application projection.
