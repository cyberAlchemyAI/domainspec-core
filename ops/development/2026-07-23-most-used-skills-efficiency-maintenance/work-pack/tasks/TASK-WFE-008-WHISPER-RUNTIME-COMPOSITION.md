# TASK-WFE-008 — Compose Whisper Canonical Base And Local Presets

- Change: WH-1 / WFE-R10
- Layer/slice/wave: L2 / S2 / W2
- Lifecycle owner: `spellcraft` for Whisper plus repository runtime owner
- Status: complete; SWU-WFE-008A and SWU-WFE-008B passed

## Objective

Generate both Whisper runtimes from the current canonical base plus an explicit
repository-local overlay manifest, preserving canonical controls and legitimate
presets while rejecting undeclared semantic drift.

## Sources

- `arcanum/spells/whisper/README.md`: current `surface_map`,
  `language_audition`, `intent_state`, canonical/local preset descriptions
- `.agents/skills/whisper/SKILL.md`: current base plus
  `product_research_blueprint`, `business_plan`, `live_presentation`
- `.claude/skills/whisper/SKILL.md`: stale runtime missing current controls
- `arcanum/tools/bootstrap_arcanum.sh`: current sole generator copies canonical
  packages but has no declared repository-overlay hook
- accepted findings WH-1

## SWU-WFE-008A — Overlay manifest and parity admission

- Primary behavior: validate one runtime composition manifest against a
  canonical base digest and allowed extension points.
- Acceptance boundary: stale base, missing canonical control, undeclared preset,
  removed gate/status/authority rule, or digest mismatch fails; declared
  metadata and preset addition passes.
- Split analysis: manifest and parity validator are one composition-admission
  behavior and require red/green fixtures.

Manifest fields: runtime targets, canonical source/digest, preset IDs and
payload digests, additive extension point, copied-file destinations, allowed
metadata, forbidden semantic removals, generator version, and validation
command. The machine source is
`.arcanum/runtime/overlays/whisper/manifest.json`; generated `SKILL.md` files
are never authoritative inputs. Migrate `product_research_blueprint` out of the
current `.agents` output into declared local payload source. Canonical
`business_plan` and `live_presentation` remain canonical inputs, not duplicated
local overlays.

## SWU-WFE-008B — Regenerate both runtimes

- Dependency: 008A pass.
- Primary behavior: regenerate `.agents` and `.claude` from current canonical
  source through `arcanum/tools/bootstrap_arcanum.sh`, then apply only validated
  declared additive overlays.
- Acceptance boundary: both runtimes contain all canonical controls and all
  target-eligible declared presets; no undeclared difference remains; public
  canonical does not receive repository-local prose.
- Split analysis: both runtimes are one regeneration transaction because partial
  completion leaves known drift.

## Scope and validation

- Canonical base is read from public `arcanum/spells/whisper/`; change it only if
  Spellcraft finds a real canonical defect, not to absorb local presets.
- Generic overlay schema, validator, fixtures, and the optional bootstrap hook
  live under public `arcanum/runtime/overlays/` and `arcanum/tools/`; they must
  contain no private preset content.
- Repository-local manifest and preset payloads live under
  `.arcanum/runtime/overlays/whisper/`, outside generated bodies.
- Generated targets are `.agents/skills/whisper/` and `.claude/skills/whisper/`.

Exact write split:

- 008A: `arcanum/runtime/overlays/` generic schema/validator/fixtures and
  `.arcanum/runtime/overlays/whisper/` manifest plus local payload source.
- 008B: `arcanum/tools/bootstrap_arcanum.sh` optional overlay integration and
  both generated Whisper runtime packages.

```bash
python3 arcanum/runtime/overlays/tests/test_runtime_overlay.py
python3 arcanum/runtime/overlays/scripts/validate_runtime_overlay.py --manifest .arcanum/runtime/overlays/whisper/manifest.json --target whisper
python3 arcanum/spells/whisper/tools/validate-whisper-run-receipt.py --help
git diff --check -- arcanum/runtime/overlays arcanum/tools/bootstrap_arcanum.sh .arcanum/runtime/overlays/whisper .agents/skills/whisper .claude/skills/whisper
```

The lifecycle owner must add and run the declared deterministic
composition/parity commands as the primary acceptance surface. Existing receipt
fixtures remain regression evidence only. Public generator changes follow
submodule-first commit and validation discipline before the parent records its
private manifest or generated-runtime result.

- Execution owner: `spellcraft`.
- Receipt: manifest digest, per-runtime base/overlay diff, canonical-control and
  preset inventories, public/private scan.

## Done

Both runtimes are current, every local preset is declared, no canonical gate is
removed, and runtime generation is reproducible without manual body edits.
