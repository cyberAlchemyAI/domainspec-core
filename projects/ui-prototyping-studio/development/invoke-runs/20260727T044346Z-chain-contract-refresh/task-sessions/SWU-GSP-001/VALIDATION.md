# SWU-GSP-001 Validation

- Material package: `pass`
- Mutation admission: `admit`
- Exact applied material parity: `2/2`
- TypeScript no-emit check: `pass`
- Focused helper witness: `2/2 pass`
- First full Playwright run: `14/15`, acceptance-critical compatibility
  failure because failed CLI stderr was no longer mirrored through the legacy
  `stdout` field.
- Rework: retained legacy combined `stdout`, added exact `rawStdout`, preserved
  separate `stderr`, regenerated material and mutation admission.
- Final full Playwright run: `15/15 pass`
- Named accepted equivalent: startup polls the existing `/state` route because
  it proves listener plus session-backed HTTP readiness without adding a
  product `/health` route outside this SWU’s scope.

No `/tmp` shim or ambient `pnpm`/Corepack route is used.
