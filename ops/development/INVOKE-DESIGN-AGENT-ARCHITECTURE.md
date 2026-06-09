# Invoke Design: Agent Architecture Canonicalization

Date: 2026-06-01
Mode: `invoke design`
Target: DomainSpec Core skill and agent architecture
Status: pass with gated implementation handoff

## Design Objective

Create a Claude/Codex-focused agent architecture that makes every active skill and agent surface read from one clear canonical owner, while preserving runtime-specific adapters, proof-domain guardrails, and owner boundaries.

The architecture has two target runtime surfaces:

1. Claude agents and prompts.
2. Codex agents and skills.

DomainSpec, GSD, and Lean remain owner/domain lanes for canonical meaning and guardrails. GitHub surfaces are no longer target runtime surfaces for this design. They should be treated as removable legacy/distribution residue unless a specific file is needed as source evidence during migration.

## Source Context

Primary evidence:

- `ops/development/domainspec-skill-agent-candidate-ledger.md`
- `ops/development/lean-formalization-skill-agent-candidate-ledger.md`
- `ops/development/domainspec-skill-agent-canonical-candidate-matrix.md`
- `ops/development/domainspec-skill-agent-canonical-owner-decision.md`
- `ops/development/domainspec-skill-agent-reader-refresh-plan.md`
- `ops/CODEX-SKILL-SURFACE-POLICY.md`
- `ops/SURFACE-OWNER-BOUNDARIES.md`
- `ops/ASSET-OWNERSHIP-POLICY.md`

Observed inventory:

- 505 main skill/agent records.
- 47 Lean formalization lane records.
- 140 multi-candidate normalized groups.
- 130 drifted same-slug groups.

## Six Design Views

### 1. Context View

The current repository has overlapping skill and agent surfaces:

- Canonical or near-canonical DomainSpec source: `implementation/domainspec/copilot/skills/*` and `implementation/domainspec/copilot/agents/*`, used as source evidence for current Claude/Codex adapters.
- Active DomainSpec runtime adapters: `implementation/domainspec/.claude/agents/*` and `implementation/domainspec/.codex/agents/*`.
- Local skill runtime/facade surface: `implementation/domainspec/.agents/skills/**/*`.
- Legacy/removable GitHub distribution residue: root `.github/skills/*`, root `.github/agents/*`, and `implementation/domainspec/.github/agents/*`.
- GSD workflow assets only insofar as Claude/Codex still consume them.
- Lean formalization: `domainspec-lean-formalization/.agents/*` plus `CLAUDE.md`.

Problem: the previous plan spent too much design energy preserving GitHub distribution surfaces. The refined target is Claude and Codex; GitHub can be deleted after a migration/deprecation check.

### 2. High-Level Structure View

Use a four-layer architecture:

| Layer | Role | Examples |
| --- | --- | --- |
| Canonical owner source | Where meaning is edited. | `implementation/domainspec/copilot/*` as source evidence, Claude/Codex adapter owners, GSD bundle source when needed, Lean formalization proof-domain files. |
| Source map | Machine-readable authority and reader map. | `ops/development/skill-agent-canonical-map.json`. |
| Active downstream readers | Runtime-specific packages or prompts. | `.claude/agents`, `.codex/agents`, `.agents/skills`. |
| Deletion lane | Surfaces to remove after migration proof. | root `.github/skills`, root `.github/agents`, implementation `.github/agents`. |
| Drift and receipt checks | Prove downstream readers match source or are intentionally divergent. | `tools/check_skill_agent_surface_drift.py` or shell wrapper. |

### 3. Low-Level Component View

Core components:

- `canonical-map`: one record per logical skill/agent, naming canonical owner, downstream readers, generation policy, and blocked owner boundaries.
- `surface-classifier`: classifies each file as canonical-source, claude-reader, codex-reader, shared-skill-facade, residue, delete-candidate, or blocked-owner.
- `drift-checker`: compares canonical and downstream hashes, frontmatter provenance, and runtime-specific body policy.
- `deletion-candidate-ledger`: lists GitHub surfaces that can be removed after Claude/Codex parity is proven.
- `owner-handoff-record`: decision artifact for changes that must occur inside `implementation/domainspec` or `domainspec-lean-formalization`.

### 4. Workflow Process View

1. Inventory surfaces.
2. Build canonical map.
3. Classify each downstream reader.
4. Validate Claude/Codex parity and source existence.
5. Report drift, blocked owner boundaries, and GitHub deletion candidates.
6. Delete or deprecate GitHub surfaces only after Claude/Codex parity and owner approval.
7. Emit DomainSpec-owned and Lean-owned handoff tasks for scoped follow-up.

No workflow step should directly edit child owner surfaces from a parent-level cleanup task.

### 5. Decision Flow View

Decision rules:

- If a DomainSpec skill exists under `implementation/domainspec/copilot/skills`, prefer it as canonical.
- If a DomainSpec agent exists under `implementation/domainspec/copilot/agents`, prefer it as canonical after freshness review.
- If a root skill or agent starts with `mars-research-*`, mark it GitHub-removal blocked only if no Claude/Codex replacement exists and the research agent is still needed.
- If a root skill or agent starts with `gsd-*`, keep only the Claude/Codex runtime copy needed by current workflows; mark GitHub copies as delete candidates after parity check.
- If a file belongs to `domainspec-lean-formalization`, keep proof-domain files canonical there and preserve claim/proof guardrails.
- If a downstream copy differs without provenance, classify as drift, not as newer canonical source.

### 6. Dependency Interface View

Interfaces:

- `ops/development/skill-agent-canonical-map.json`: consumed by Claude/Codex drift checker and deletion-candidate report.
- `tools/check_github_drift.sh`: existing GitHub checker, now useful only as migration evidence before removal.
- `tools/audit_codex_skill_surface.sh`: existing count/audit surface.
- `tools/classify_root_github_skills.sh`: existing classification logic, now useful to seed deletion candidates rather than preserve GitHub as a target.

## Architecture Decisions

| Decision | Status | Rationale |
| --- | --- | --- |
| Focus active architecture on Claude and Codex. | accepted | User clarified GitHub does not matter for this architecture. |
| Treat root `.github/skills` and `.github/agents` as deletion candidates. | accepted | They are not target runtimes and can be removed after parity/deprecation checks. |
| Treat implementation `.github/agents` as deletion candidates. | accepted | Claude/Codex adapters are the active implementation-owned runtimes. |
| Prefer DomainSpec `copilot` surfaces as source candidates. | accepted | Existing owner policy names `implementation/domainspec/copilot` as canonical automation source. |
| Keep Lean formalization separate. | accepted | Lean guardrails are proof-domain-specific and should not be weakened by generic DomainSpec runtime cleanup. |
| Use Claude/Codex parity as deletion gate. | accepted | Deletion is safe only after active runtime equivalents exist or are declared unnecessary. |
| Add deletion-candidate checker before cleanup. | accepted | Deletion/pruning needs source map, parity, and owner-boundary evidence. |

## Risks And Gaps

- GitHub surfaces may still be referenced by local scripts, docs, or external tooling; deletion needs a usage scan.
- GSD plain `.md` and `.agent.md` pairs differ; delete GitHub copies only after Claude/Codex or bundle-source parity is confirmed.
- DomainSpec `.agents/skills` has nested utility residue, including GitNexus copies.
- Lean lane includes off-domain `implement-filter`; active use needs proof before promotion or deletion.
- Arcanum generated GitHub packages may be removable if Codex global skills and Claude/Codex adapters are sufficient.

## Invoke Result

- Mode: design
- Spell: invoke
- Canonical ID: invoke
- Scope: library
- Phase status: pass
- Mode contract: `spells/invoke/design.md`
- Outputs: `ops/development/INVOKE-DESIGN-AGENT-ARCHITECTURE.md`
- Design views: context, high-level structure, low-level components, workflow process, decision flow, dependency interface
- Template/profile selection: architecture family, source contract and dependency/interface focus
- Implementation layering: seed required in plan
- Work-pack: n/a
- Decisions: Claude/Codex active runtime map plus GitHub deletion lane
- Unresolved gaps: GitHub usage scan, GSD Claude/Codex parity, Lean residue active-use proof
- Next route: refine then plan
