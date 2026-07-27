# SWU-GSP-002 Validation

- Material package: `pass`
- Mutation admission: `admit`
- Exact applied material parity: `2/2`
- TypeScript no-emit check: `pass`
- Independent child-process freshness witness: `3/3 pass`
- Full unit/slice suite: `65/65 pass`

The witness constructs the reader before any file exists, then uses real child
CLI processes to stage, Accept, and Revert. The reader observes each new state,
staged record, revision head, and append-only revision count without restart.
Sequential store instances allocate `0001`, `0002`, `0003`; post-construction
corruption and an external writer lock both fail closed.
