# Interfaces

The candidate adapter exposes only:

```text
buildGeneration(workspaceRoot, expectedLedgerDigest)
verifyGeneration(workspaceRoot, expectedLedgerDigest)
queryGeneration(workspaceRoot, expectedLedgerDigest, query)
renderFromYaml(workspaceRoot)
quarantineGeneration(expectedLedgerDigest, reason)
rebuildGeneration(workspaceRoot, expectedLedgerDigest)
```

All operations return structured results with `status`, `code`, exact input
identities, evidence paths, and zero/complete output. No interface accepts
database bytes or a derived view as a Craft mutation input.

The WaveDB Node binding is an internal native dependency. Graph, GraphQL,
vector, subtree deletion, database export as authority, and unscoped raw-prefix
access are outside the adapter surface.
