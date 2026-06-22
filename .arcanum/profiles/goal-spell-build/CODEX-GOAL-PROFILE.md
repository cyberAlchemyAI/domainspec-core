# Codex Goal Profile: Goal Spell Build Next Move

## Codex Goal Profile Result

- Source work-pack: `arcanum/spells/goal/.craft/ledger.yml`
- Selected unit: `GOAL-SPELL-NEXT-MOVE` (`SWU-GOAL-README`, `SWU-GOAL-D3`; ADO design move gated/deferred)
- Readiness: pass
- Goal budget: 4000 characters; pass, measured 1387 characters
- Decision profile: `.arcanum/profiles/decision-profile.yml`; consumed fields are `risk`, `approval`, `slice`, `ownership`, `gap_filling`, `technique_weights`, `anti_patterns`, and `consumed_by` as operational policy summary only.
- One-shot mode: yes
- Capability policy: `spellcraft`/`invoke` allowed for README contract and public schema/default authoring; `task-session` allowed only as the bounded runtime execution frame for this selected next move; `decision-gate` only if the ADO design move needs explicit approval; no subagents or external research without separate operator approval and receipts; no experiment-harness promotion in this goal.
- Sidecar profile: `.arcanum/profiles/goal-spell-build/CONTEXT-PACK.md`
- Native Goal:

  ```text
  /goal Execute GOAL-SPELL-NEXT-MOVE for arcanum/spells/goal: using .arcanum/profiles/goal-spell-build/CONTEXT-PACK.md and context-index.json, author the public goal spell source contract README.md and decision-profile.schema with neutral defaults only, from the ADO Option A plan. Keep writes inside arcanum/spells/goal/README.md, arcanum/spells/goal/decision-profile.schema, and narrowly necessary public-safe development notes; do not hand-author SKILL.md, commit/push, move parent gitlinks, copy private profile data, or promote the spell. Treat the scrubbed ADO design move as gated: do it only if already public-safe from the pack and approval is explicit in the current turn; otherwise record it as deferred. Verify README section coverage, JSON parse/schema shape for decision-profile.schema, no private-path/profile-data leaks in new public files, git -C arcanum diff --check -- spells/goal, and make bump-check only if publication is explicitly requested. Iterate by reading pack/index first, editing one bounded slice, validating, and reporting extra sources used outside the pack with the named gap that justified each. Stop with BLOCK if private data or absolute private paths would enter new public files, validation fails outside write scope, approval is needed for the ADO move, generated SKILL or promotion is requested, or commits/push/gitlink movement become necessary.
  ```

- Verification surface: `test -f arcanum/spells/goal/README.md`; `test -f arcanum/spells/goal/decision-profile.schema`; `python3 -m json.tool arcanum/spells/goal/decision-profile.schema`; README section review; public-boundary scan on new public files; `git -C arcanum diff --check -- spells/goal`; `make bump-check` only if publication is explicitly requested.
- Boundaries: write scope is `arcanum/spells/goal/README.md`, `arcanum/spells/goal/decision-profile.schema`, and narrowly necessary public-safe notes under `arcanum/spells/goal/development/` only when the ADO move is approved; no generated `SKILL.md`, no promotion, no commit/push/PR/gitlink movement, no private profile/corpus content in public files.
- Handoff pack: `.arcanum/profiles/goal-spell-build/CONTEXT-PACK.md` and `.arcanum/profiles/goal-spell-build/context-index.json`
- Strict coverage: pass for the bounded next-move profile; full `SWU-GOAL-*` implementation and promotion remain gated.
- Fallback exploration: named gaps only: `GAP-GOAL-SCHEMA-001`, `GAP-GOAL-ADO-MOVE-001`, validation-command availability, or a runtime blocker named before exploring.
- Extra-source reporting: required
- Stop condition: stop with `BLOCK` if no-leak authoring cannot be proven, validation fails outside scope, ADO move approval is needed, private data would enter `arcanum/`, generated `SKILL.md` or promotion becomes necessary, or publication/gitlink movement is required.
- Validation: handoff pack created from selected ledger row, ADO result/plan, and private decision-profile policy summary. Runtime implementation was not executed by this profile generation.
