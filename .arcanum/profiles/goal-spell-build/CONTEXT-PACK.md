# Codex Goal Handoff Pack: GOAL-SPELL-NEXT-MOVE

## Identity

- Task/SWU: `GOAL-SPELL-NEXT-MOVE`
- Ordered units: `SWU-GOAL-README`, `SWU-GOAL-D3` public schema/default; ADO design move is approval-gated
- Source task/work-pack: `arcanum/spells/goal/.craft/ledger.yml`
- Session/run id: `2026-06-20-goal-spell-build`
- Session evidence path: `.arcanum/profiles/goal-spell-build/`
- Runtime handoff: `codex-goal`
- Repository revision: parent `c0820c59bf9900872543428ec0c349ada400379c`; arcanum `8317c99ef2b3b2fcf98a9337c560d815ca5b72d6`
- Evidence date: `2026-06-20`

## Obligation Coverage

| Obligation | Status | Selected Evidence | Resolution |
| --- | --- | --- | --- |
| `O1-target` | `covered` | `arcanum/spells/goal/.craft/ledger.yml#indexes.next_moves`; `arcanum/spells/goal/CRAFT.md#Quick links` | Build the next goal-spell slice, not the full spell. |
| `O2-public-private-boundary` | `covered` | `arcanum/spells/goal/.craft/ledger.yml#DEC-GOAL-PRIVACY-SPLIT-001`; `.arcanum/profiles/decision-profile.yml#consumed_by` | Public package gets schema/neutral defaults only; private filled profile stays private. |
| `O3-readme-source-contract` | `covered` | `.../stages/s09-plan.md#Package layout to author`; `.../RESULT.md#Convention notes` | Hand-author `README.md`; generated `SKILL.md` is out of scope. |
| `O4-decision-profile-schema` | `covered` | `arcanum/spells/goal/.craft/ledger.yml#GAP-GOAL-SCHEMA-001`; `.../stages/s09-plan.md#SWU-GOAL-D3` | Author `decision-profile.schema` with public shape and neutral default only. |
| `O5-ado-design-move` | `resolved` | `arcanum/spells/goal/.craft/ledger.yml#GAP-GOAL-ADO-MOVE-001`; `arcanum/spells/goal/CRAFT.md#Gaps` | Runtime may defer this unless current-turn approval and public-safety evidence are explicit. |
| `O6-validation-and-promotion` | `covered` | `.../stages/s09-plan.md#Build gates`; `.../RESULT.md#Recommended next routes` | Validate authoring; do not promote the spell or run experiment-harness in this goal. |
| `O7-write-scope` | `covered` | `arcanum/spells/goal/.craft/ledger.yml#artifacts`; `.../stages/s09-plan.md#Package layout to author` | Default writes: `README.md`, `decision-profile.schema`, and narrowly necessary public-safe development notes under `arcanum/spells/goal/`. |
| `O8-capability-policy` | `covered` | `.../stages/s09-plan.md#SWUs`; `.../RESULT.md#Recommended next routes` | Allow `spellcraft`/`invoke` for contract/schema authoring; require approval for decision-gate/ADO move; no subagents unless separately approved. |
| `O9-extra-source-reporting` | `resolved` | `codex-goal-profile` policy | Runtime must report extra sources outside this pack and the named gap that justified each. |
| `O10-stop-condition` | `covered` | `arcanum/spells/goal/.craft/ledger.yml#typed_items`; `.arcanum/profiles/decision-profile.yml#risk-and-approval-policy` | Stop on leak risk, unapproved ADO move, validation outside scope, generated-skill/promotion pressure, or commit/push/gitlink need. |

Strict coverage: `pass` for generating and running the bounded next-move Codex goal. Full spell implementation remains out of scope.

## Selected Sources

- `arcanum/spells/goal/.craft/ledger.yml`
  - Selectors: `indexes.next_moves`, `artifacts`, `typed_items`, `gaps`, `decisions`
  - Obligations: `O1-target`, `O2-public-private-boundary`, `O4-decision-profile-schema`, `O5-ado-design-move`, `O7-write-scope`, `O10-stop-condition`
  - Evidence excerpt: The ledger selects `spells/goal/.craft` as scope, marks the build at `plan`/`flag`, names the next move, and records the active no-leak blocker plus promotion gate.
- `arcanum/spells/goal/CRAFT.md`
  - Selectors: `Quick links`, `Context`, `Blockers & gates`, `Gaps`, `Build SWUs`
  - Obligations: `O1-target`, `O5-ado-design-move`, `O10-stop-condition`
  - Evidence excerpt: Human-readable view of the same ledger, naming `SWU-GOAL-README`, `GAP-GOAL-SCHEMA-001`, and `GAP-GOAL-ADO-MOVE-001`.
- `/home/vrondelli/projects/workspace-resonant/.craft/artifacts/autonomous-dag-orchestration/development/refinement-runs/2026-06-14-dag-loop-to-arcanum-sigils/RESULT.md`
  - Selectors: `Synthesis`, `What the audit changed`, `Convention notes`, `Recommended next routes`, `Decision-mentality model`
  - Obligations: `O2-public-private-boundary`, `O3-readme-source-contract`, `O6-validation-and-promotion`, `O8-capability-policy`
  - Evidence excerpt: Option A composes the goal-loop as one router-only spell and explicitly separates public schema from private filled profile.
- `/home/vrondelli/projects/workspace-resonant/.craft/artifacts/autonomous-dag-orchestration/development/refinement-runs/2026-06-14-dag-loop-to-arcanum-sigils/stages/s09-plan.md`
  - Selectors: `Objective`, `Package layout to author`, `SWUs`, `Build gates`, `Next route`
  - Obligations: `O3-readme-source-contract`, `O4-decision-profile-schema`, `O6-validation-and-promotion`, `O7-write-scope`, `O8-capability-policy`
  - Evidence excerpt: Non-executed plan says to author `README.md`, keep `SKILL.md` generated, and run SWUs under submodule discipline.
- `.arcanum/profiles/decision-profile.yml`
  - Selectors: `risk`, `approval`, `slice`, `ownership`, `gap_filling`, `technique_weights`, `anti_patterns`, `consumed_by`
  - Obligations: `O2-public-private-boundary`, `O10-stop-condition`
  - Evidence excerpt: Private runtime policy informs default-deny, propose-then-promote, small-slice sequencing, immutable public/private boundaries, and named-gap fallback. Contents must not be copied into public package files.

## Architecture Guidance

The target package is a composed Arcanum spell at `arcanum/spells/goal/`. Its
source contract is `README.md`; `SKILL.md` is generated by runtime installation.
The spell design is a router-only, fail-closed control spine with staged deltas
and approval-gated promotion. This goal should create the public source contract
and public profile schema/default only; runtime implementation SWUs and promotion
remain later gated work.

## Related Feature Context

The goal spell composes existing Arcanum owners where possible: `craft` for
read-only frontier/context, `dispatch-spec` for owner/technique routing,
`decision-gate` for durable approvals, and observability capabilities for later
promotion evidence. It owns new inline control mechanisms only where the ADO
audit found no existing owner.

## Constraints And Non-Goals

- Keep private operator profile data out of `arcanum/`.
- Do not hand-author `arcanum/spells/goal/SKILL.md`.
- Do not implement every `SWU-GOAL-*` in this goal.
- Do not promote the spell out of draft.
- Do not commit, push, or move parent gitlinks.
- Treat the ADO design move as gated unless approval and scrubbed/public-safe evidence are explicit in the current turn.
- Report any extra source outside this pack, the named gap that justified it, and whether it changed the result.

## Write Scope

- `arcanum/spells/goal/README.md`
- `arcanum/spells/goal/decision-profile.schema`
- `arcanum/spells/goal/development/` only for public-safe design/handoff notes if current-turn approval covers the ADO move
- `arcanum/spells/goal/.craft/ledger.yml` and `arcanum/spells/goal/CRAFT.md` only for narrow status/evidence updates if the runtime changes readiness state

## Validation Surface

- `test -f arcanum/spells/goal/README.md`
- `test -f arcanum/spells/goal/decision-profile.schema`
- `python3 -m json.tool arcanum/spells/goal/decision-profile.schema`
- README section review for objective, capabilities, spine, modules, gates, observability, and output contract.
- Public-boundary scan on new public files for private profile contents, absolute private paths, private corpus references, and operator-specific data.
- `git -C arcanum diff --check -- spells/goal`
- `make bump-check` only if publication is explicitly requested later.

## Gaps And Blockers

- `BLK-GOAL-SUBMODULE-001`: active governance blocker. Authoring is allowed only while public-safe and uncommitted/unpushed.
- `GATE-GOAL-PROMOTION-001`: active promotion gate. This goal must not mark the spell promoted.
- `GAP-GOAL-SCHEMA-001`: resolve in this goal by authoring `decision-profile.schema`.
- `GAP-GOAL-ADO-MOVE-001`: defer unless current-turn approval and no-leak evidence make the move safe.

## Authority Precedence

1. Repository instructions: `AGENTS.md`, `SUBMODULE-DISCIPLINE.md`, and public/private boundary rules.
2. Goal Craft source: `arcanum/spells/goal/.craft/ledger.yml`.
3. Upstream ADO result and s09 plan.
4. Private decision profile, consumed only as runtime policy summary.
5. Human-readable `arcanum/spells/goal/CRAFT.md` as linked view, not source of truth.

## Fallback Exploration Rule

Broad repository exploration is allowed only for `GAP-GOAL-SCHEMA-001`,
`GAP-GOAL-ADO-MOVE-001`, validation-command availability, or an explicit
runtime blocker named before exploring. Extra sources must be reported in the
runtime result.

## Provenance

- Source refs: `arcanum/spells/goal/.craft/ledger.yml`, `arcanum/spells/goal/CRAFT.md`, ADO `RESULT.md`, ADO `stages/s09-plan.md`, `.arcanum/profiles/decision-profile.yml`
- Git SHA: parent `c0820c59bf9900872543428ec0c349ada400379c`; arcanum `8317c99ef2b3b2fcf98a9337c560d815ca5b72d6`
- Builder mode: `standard`

## Output Paths

- Markdown: `.arcanum/profiles/goal-spell-build/CONTEXT-PACK.md`
- JSON/index: `.arcanum/profiles/goal-spell-build/context-index.json`
