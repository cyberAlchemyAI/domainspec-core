# Intent Route Resolver candidate

This directory is a project-neutral candidate closure for a deterministic,
zero-authority intent-routing relation. It is not canonical, generated,
installed, released, or production-ready.

The contract accepts a normalized request and one digest-bound finite catalog.
It returns `candidate`, `ambiguous`, `no-match`, or `invalid`. It does not
discover capabilities, repair intent, rank semantically, authorize work, bind a
workflow, execute anything, or persist effects.

## Contract-only stage

This sanitized closure freezes schemas, fixtures, manifest, scan mechanics,
license, API boundary, and the JSON process contract. Executable resolver
semantics and portability witnesses are a separate candidate stage.

## Local checks

```bash
node scripts/validate-contract.mjs
node scripts/scan-boundary.mjs
node scripts/validate-contract.mjs --check source-license-api
```

All checks emit one JSON document on stdout and no stderr on success.
