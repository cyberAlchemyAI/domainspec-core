# TASK-WEG-009 — Local Preset Externalization and Regeneration

## Objective and mapping

- Layer/slice/wave: L3 / S3 / W3.
- Decision: regenerate the native Whisper skill from public canonical source without erasing or publishing the repository-local product research preset.
- Dependencies: SWU-WEG-006 and SWU-WEG-008; W2 gate passed.
- Blockers: none.

## Inputs and outputs

- Inputs: canonical Whisper changes, current generated `.agents/skills/whisper/SKILL.md`, local `product_research_blueprint` divergence.
- Outputs: local preset files under `.arcanum/spells/whisper/presets/product-research-blueprint/`, generic canonical local-preset resolution rule, regenerated native skill, drift/privacy receipt.
- State touched: canonical public spell, private host-local preset, generated host package.

## Ordered migration

1. Extract only the host-local preset identity/instructions into the local preset root; preserve its behavior with a local fixture.
2. Add a generic canonical discovery rule for `.arcanum/spells/whisper/presets/`; local profiles cannot raise proof status or weaken canonical gates.
3. Remove host-specific preset prose from the generated skill by regenerating from canonical source.
4. Verify the local runtime can discover the externalized preset.
5. Diff canonical versus generated after stripping generated frontmatter; only approved generation transforms may remain.
6. Sweep public Arcanum for the local preset ID and private evidence strings; any hit outside generic lookup documentation blocks.

Failure modes: never regenerate before the local preset fixture passes; preserve dirty unrelated files; do not create a general overlay merge engine; public leakage blocks closeout.

## Smallest Working Unit: SWU-WEG-009

- Primary behavior: migrate one local preset across canonical regeneration without behavioral loss or public leakage.
- Independent acceptance boundary: preset resolves locally after native regeneration and public/generated diffs satisfy the declared boundary.
- Split analysis: extraction, discovery, and regeneration were considered separately; executing any alone risks data loss or stale generated behavior, so the migration closes atomically.
- Source anchors: `../../DESIGN.md#38-local-preset-resolution`, decision D-06, current canonical/generated diff.
- Related context: repository `SUBMODULE-DISCIPLINE.md` if publication occurs; this SWU itself does not authorize commit/push.
- Write scope: `.arcanum/spells/whisper/presets/product-research-blueprint/**`, generic lookup text in `arcanum/spells/whisper/README.md`, regenerated `.agents/skills/whisper/**`, approved bootstrap profile inputs only if required by the existing generator.
- Done criteria: local behavior fixture passes, generated package includes generic gates, private ID is absent from public Arcanum, and unrelated worktree changes remain untouched.
- Acceptance evidence: before/after inventory, generation command/result, local resolution test, canonical/generated diff, privacy sweep.
- Verification:

```bash
rg -n "product_research_blueprint" arcanum/spells/whisper .agents/skills/whisper .arcanum/spells/whisper
git diff --check -- arcanum/spells/whisper .agents/skills/whisper .arcanum/spells/whisper
```

- Execution owner: `local-fallback` through Spellcraft's install/adapt stage.
- Handoff note: resolve and document the repository's actual bootstrap command before running it; follow submodule-first discipline if public Arcanum changes are later committed.

## Synchronization

Do not close W3 until TASK-WEG-VERIFY inspects the post-regeneration state. No commit or push is implied by task completion.
