# Read-Only Observer Contract

## Objective

Measure archive read/search behavior without performing intake, decide, promote, or trusted-write
operations.

## Allowed Operations

- archive status/readiness check,
- search,
- read,
- local measurement receipt emission.

## Blocked Operations

- intake write,
- request ingest,
- decide review,
- promote review artifact,
- trusted knowledge write.

## Receipt Shape

```json
{
  "observer_id": "observer.read-only.v0",
  "operation": "search",
  "scope": "knowledge-store",
  "status": "observed",
  "trusted_write_attempted": false
}
```

## Validation

Scan observer examples for trusted-write operations before use.
