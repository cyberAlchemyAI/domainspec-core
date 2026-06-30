# Read-Only Observer Example

This example is intentionally non-runtime pseudocode.

Allowed:

```text
status -> search -> read -> emit measurement receipt
```

Blocked:

```text
write_intake
request_ingest
decide_review
promote_review_artifact
trusted knowledge write
```

The first slice proves the seam without creating or promoting candidates.
