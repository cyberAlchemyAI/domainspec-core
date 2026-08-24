# SWU-IRO-004 strict context

- Stream: `IRO-FULL-STREAM`
- Epoch label: `20260802T021738Z`
- Frozen epoch ID: `epoch-a696eda26311d39018e7ac8f`
- Task: `TASK-IRO-CANONICAL-001`
- Unit: `SWU-IRO-004`
- Capability allowlist: `task-session`, `sigil-development`
- Lifecycle owner: `public-arcanum-owner`
- Authorization: local unmerged public-canonical implementation is authorized by the direct owner instruction; merge, push, publication, release, deployment, and production remain blocked.

## Exact material scope

The logical owner scope is `arcanum/arcana/intent-route-resolver/**`. It is
bound to the isolated worktree
`/home/vrondelli/projects/arcanum-intent-route-resolver` on branch
`codex/intent-route-resolver-addon` at base
`07b01c9dd4e918ae0b0d83f6a2cde52ea8f9a295`.

Only `arcana/intent-route-resolver/**` may change in that worktree. Generated
Codex or Claude packages, registries, formulae, other Arcana packages, the
dirty parent submodule checkout, consumers, orchestrators, and private runtime
sources are outside this unit.

## Required result

Promote the reviewed public-safe candidate closure as the canonical
`intent-route-resolver` Arcana package. Exclude candidate runtime witness
records from the public source closure. Update only lifecycle labels needed to
state canonical-source ownership; preserve the behavior, protocol versions,
closure digest, zero-authority contract, tests, fixtures, and license/API
boundary exactly.

## Required validation

- the clean-worktree receipt remains true before mutation;
- the promoted source inventory is exact and excludes `development/runs/**`;
- contract, source/license/API, boundary, Node test, closure-digest, JSON-port,
  public repository whitespace, and private-identifier scans pass;
- no generated package or unrelated public path changes;
- the worktree remains local and unmerged.

## Evidence ceiling and successor

A pass proves canonical public-source acceptance on one unmerged local branch
and rerun source-level validation. It does not prove generated Codex/Claude
parity, installation, consumer admission, orchestrator integration, release,
deployment, production, or reasoning-engine advancement. Project exactly
`SWU-IRO-005` for isolated dual-runtime generation and wrapper parity.
