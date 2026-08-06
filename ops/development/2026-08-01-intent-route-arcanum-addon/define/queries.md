# Queries

The capability supports only deterministic local queries over supplied values:

- Is the request/catalog/protocol valid and digest-bound?
- Which routes are excluded, eligible, dominated, or unresolved, and why?
- Is the terminal disposition `candidate`, `ambiguous`, `no-match`, or `invalid`?
- Which smallest sorted discriminator set can resolve ambiguity?
- Do two profile wrappers produce identical canonical case bytes?

It does not query a network, registry, model, filesystem discovery surface,
authorization service, execution runtime, or effect store.

