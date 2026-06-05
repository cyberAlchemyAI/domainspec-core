# Surface Cleanup Blocker Decisions

Date: 2026-05-31
Status: accepted
Decision source: `refine` over current surface cleanup blockers and gaps; user approved recommended set through `invoke refresh`

## Scope

This decision record covers blocker-level choices that affect Arcanum/DomainSpec repository surface cleanup after the native-first skill surface decision.

Already accepted:

- Native runtime skills/packages are the primary capability surface.
- `tools/arcanum` is deterministic support.
- Personal Codex refresh is allowed as stage, compare, then promote.

## Decision 1: Personal Codex Promotion Safety

Question: before promoting generated Arcanum skill packages into `/mnt/c/Users/vlad_/.codex/skills`, how should rollback evidence be preserved?

### Option 1A: Backup Replaced Arcanum Skill Packages First

Benefit: safest operational path; active personal skills can be restored if the generated package has a problem.

Cost or risk: creates temporary or archive files that need later cleanup.

Choose when: promotion safety matters more than a perfectly clean working directory.

Downstream impact: `TASK-SURFACE-002` can stage, back up only touched Arcanum packages, promote, and validate.

### Option 1B: Promote Without Backup, Rely On Canonical Regeneration

Benefit: simplest and cleanest promotion path.

Cost or risk: rollback depends on regenerating or recovering from git/cache state rather than a direct backup.

Choose when: the generated package contract is trusted and speed matters.

Downstream impact: `TASK-SURFACE-002` can promote with fewer steps but higher operational risk.

### Option 1C: Stage Only Again

Benefit: avoids mutation despite the earlier option 2 approval.

Cost or risk: leaves active personal Codex skills stale.

Choose when: the review finds unexpected generated diff or naming drift.

Downstream impact: promotion remains blocked.

Selected option: 1A, Backup Replaced Arcanum Skill Packages First.

Rationale: The active personal Codex skill surface is machine-global state. Before promotion, the task session should preserve a narrow rollback copy of only the Arcanum packages and aliases it will replace.

## Decision 2: GitHub/Copilot Runtime Cache Fate

Question: after `.github/skills/arcanum-*` becomes self-provenanced, what should happen to `.arcanum/runtimes/github-copilot`?

### Option 2A: Delete After Self-Provenance

Benefit: cleanest surface; no duplicate runtime cache remains.

Cost or risk: unsafe if any active wrapper or tool still reads the cache.

Choose when: search proves no active dependency after package regeneration.

Downstream impact: enables `TASK-SURFACE-004` deletion cleanup.

### Option 2B: Untrack And Regenerate On Demand

Benefit: keeps the cache available locally without treating it as source.

Cost or risk: requires ignore policy and regeneration documentation.

Choose when: tools still benefit from cache output but it should not be canonical or tracked.

Downstream impact: `TASK-SURFACE-004` updates state classification and ignore rules.

### Option 2C: Keep As Tracked Generator Cache With Manifest

Benefit: preserves reproducible generated runtime package state in the repository.

Cost or risk: keeps duplicate surface area and may invite drift against `.github/skills`.

Choose when: GitHub/Copilot packaging needs tracked generated snapshots.

Downstream impact: requires a manifest and drift validation.

Selected option: 2B, Untrack And Regenerate On Demand.

Rationale: After `.github/skills/arcanum-*` packages are self-provenanced, `.arcanum/runtimes/github-copilot` should not remain a tracked canonical-looking duplicate. Keeping it as an on-demand generated cache preserves utility without making it source.

## Decision 3: Root GitHub Duplicate Skill Fate

Question: what should happen to root `.github/skills` packages classified as DomainSpec/GSD duplicates or personal-overlap entries?

### Option 3A: Keep Until Runtime Confirmation

Benefit: safest for GitHub/Copilot discovery and root distribution.

Cost or risk: preserves noisy duplicate skill surface.

Choose when: the priority is avoiding broken collaboration runtime behavior.

Downstream impact: duplicate cleanup remains mostly classification-only.

### Option 3B: Delete `gate-delete` Duplicates After Owner Confirmation

Benefit: reduces repository noise while respecting DomainSpec/GSD ownership.

Cost or risk: needs owner/runtime confirmation before deletion.

Choose when: root GitHub/Copilot does not need those duplicate packages.

Downstream impact: enables `TASK-DUP-004` or a surface cleanup task to delete candidates.

### Option 3C: Convert Root Duplicates Into Thin Forwarding Adapters

Benefit: preserves root discovery names while preventing copied skill bodies.

Cost or risk: leaves a facade layer that must be validated and documented.

Choose when: GitHub/Copilot benefits from root names but source ownership belongs elsewhere.

Downstream impact: requires generated adapter/provenance pattern.

Selected option: 3A, Keep Until Runtime Confirmation.

Rationale: Root `.github/skills` is an active GitHub/Copilot collaboration surface. Duplicate cleanup should not delete DomainSpec/GSD or personal-overlap packages until runtime confirmation proves those root packages are unnecessary.

## Decision 4: Root `.arcanum` Generated State Policy

Question: how should `.arcanum/observability` generated evidence be handled by default?

### Option 4A: Ignore Generated Ledgers By Default, Promote Selectively

Benefit: clean source tree; only intentional evidence is tracked.

Cost or risk: useful local telemetry may not travel with the repository unless explicitly promoted.

Choose when: source cleanliness and privacy matter most.

Downstream impact: `TASK-SURFACE-006` updates `.gitignore` and classification docs.

### Option 4B: Track Curated Ledgers Only

Benefit: preserves selected durable evidence while excluding noisy runtime state.

Cost or risk: requires criteria and review discipline.

Choose when: some observability history is valuable project evidence.

Downstream impact: needs promotion rules and possibly ledger slicing.

### Option 4C: Track Generated Observability By Default

Benefit: maximum audit trail.

Cost or risk: noisy diffs, possible private/local state leakage, and large churn.

Choose when: auditability overrides repository noise.

Downstream impact: generated-state cleanup becomes a curation and retention task.

Selected option: 4A, Ignore Generated Ledgers By Default, Promote Selectively.

Rationale: Generated observability ledgers and reflection state can be noisy and local/private. Source control should carry config, structure, and intentionally promoted evidence rather than default runtime churn.

## Decision 5: Repository Organization Legacy Path Fate

Question: how should unresolved legacy/project paths be handled before broad repository cleanup?

### Option 5A: Classify Only, No Moves Or Deletes

Benefit: safest; preserves dirty/submodule/project state.

Cost or risk: delays visible cleanup.

Choose when: the priority is finishing runtime surface cleanup first.

Downstream impact: repository organization blockers remain parked with classification evidence.

### Option 5B: Decide Each Legacy Path In Separate Gates

Benefit: precise decisions for `cyberAlchemy/`, `projects/body-war/`, `research/projects/hermes-agent/repo`, and legacy `sigils-library`.

Cost or risk: slower and more decision-heavy.

Choose when: repository shape cleanup should resume now.

Downstream impact: creates separate task sessions for each legacy path.

### Option 5C: Treat Legacy Arcanum Names As Delete Candidates After Diff

Benefit: directly addresses the user's concern about old `sigils-library` naming.

Cost or risk: risky for non-Arcanum legacy/project paths unless each has evidence.

Choose when: only legacy Arcanum-name cleanup is in scope now.

Downstream impact: run targeted diff for `sigils-library` remnants before deletion.

Selected option: 5C, Treat Legacy Arcanum Names As Delete Candidates After Diff.

Rationale: This directly addresses the legacy `sigils-library` naming concern without broad moves/deletes across unrelated project or submodule state. Deletion remains gated by targeted diff evidence.

## Deferrable Decisions

- Exact separate provenance manifest shape for generated packages.
- Whether to create root `.agents/skills/arcanum-*` symlink facades.
- Full runtime-surface inventory JSON format.
- Organization validation script shape.
- README refresh wording.
- DomainSpec-owned runtime helper migration.

## Assumptions

- Root command adapter deletions remain valid.
- Historical evidence is preserved unless a cleanup task explicitly owns it.
- Parent cleanup must not mutate DomainSpec, GSD, nested Arcanum, or project-owned surfaces without a scoped owner task.
- `sigils-library` is a legacy Arcanum name, not a separate canonical source.

## Remaining Blockers

None for the next bounded task session.

## Next Route

Proceed to `task-session` for `TASK-SURFACE-002 / SWU-SURFACE-002` with the selected safety policy:

- stage generated personal Codex packages,
- compare against active personal Codex Arcanum packages,
- back up only replaced Arcanum packages and aliases,
- promote reviewed generated packages,
- validate native-first skill behavior.
