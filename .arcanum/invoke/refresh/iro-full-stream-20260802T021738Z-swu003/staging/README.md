# Intent Route Resolver candidate

This directory is a project-neutral candidate closure for a deterministic,
zero-authority intent-routing relation. It is not canonical, generated,
installed, released, or production-ready.

The contract accepts a normalized request and one digest-bound finite catalog.
It returns `candidate`, `ambiguous`, `no-match`, or `invalid`. It does not
discover capabilities, repair intent, rank semantically, authorize work, bind a
workflow, execute anything, or persist effects.

## Executable candidate stage

This sanitized closure includes schemas, sealed fixtures, the pure resolver,
canonical JSON and SHA-256 support, a strict JSON process port, static boundary
checks, Node tests, and a real-browser witness page. Its evidence remains
candidate-local.

## Local checks

```bash
node scripts/validate-contract.mjs
node scripts/scan-boundary.mjs
node scripts/validate-contract.mjs --check source-license-api
node --test test/*.test.mjs
```

All checks emit one JSON document on stdout and no stderr on success.
