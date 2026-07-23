# SWU-WFE-003B Blocker

## Result

`BLOCK`

## Blocking condition

The approved architecture places the material-package validator, receipt
schemas, and fixtures under:

```text
arcanum/spells/invoke/development/
```

The runtime generator intentionally excludes every `development/` directory
from generated skill packages. It also does not install an alternate
`.arcanum/source` tree. Therefore `.agents/skills/invoke/` and
`.claude/skills/invoke/` can receive the new Refresh prose but cannot execute
the deterministic validator that prose would require.

That would make the canonical checkout pass while declared generated runtimes
remain unable to produce a material readiness receipt. This contradicts the
SWU's generated-runtime completion boundary.

## Evidence

- `arcanum/tools/bootstrap_arcanum.sh:821-874` copies top-level files and all
  support directories except `development/`.
- The bootstrap flow removes `$dest_root/source` under `--force` and contains
  no corresponding source-tree installation.
- Isolated Invoke generation produced updated `refresh.md` but no validator,
  receipt schema, fixture runner, or handoff resolver in either generated
  package.
- Whole-package isolated diffs also exposed unrelated runtime/template drift,
  so broad generated-directory replacement is not an admissible workaround.

## Recovery performed

- Reverted every partial SWU-WFE-003B contract, resolver, fixture, and generated
  runtime change.
- Restored canonical, Codex, and Claude `refresh.md` to the shared pre-003B
  digest `9793b9bce9457397316efe9da7247f5fb95bfde2f6f63f94773eec731dc7cdec`.
- Restored the SWU-WFE-003A focused runner and full harness to their closure
  digests.
- Re-ran the 13-case material validator suite and full Invoke harness: pass.

SWU-WFE-003A remains complete and usable as canonical development evidence.
SWU-WFE-003B made no retained implementation mutation.

## Unblock action

Choose one option in [DECISION-GATE.md](DECISION-GATE.md), then refresh the
SWU-WFE-003B write scope and context pack before implementation resumes.
