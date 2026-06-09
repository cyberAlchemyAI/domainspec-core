# DomainSpec Skill And Agent Canonical Owner Decision

Generated: 2026-06-01T10:28:23Z
Dispatch: `domainspec-skill-agent-canonicalization-20260601`
Status: proposed; requires operator approval before mutation

## Evidence Base

- Main ledger records: 505
- Lean lane records: 47
- Multi-candidate normalized groups: 140
- Drifted same-slug groups: 130

## Proposed Decisions

1. DomainSpec implementation skills with matching `implementation/domainspec/copilot/skills/<id>/SKILL.md` should use that path as the canonical source candidate.
2. DomainSpec agents with matching `implementation/domainspec/copilot/agents/<id>.agent.md` should use that path as the canonical source candidate after freshness review against `.github`, `.claude`, and `.codex` adapters.
3. DomainSpec local `.agents/skills`, `.github/agents`, `.claude/agents`, and `.codex/agents` entries should be treated as owner-local runtime/readiness surfaces. They can supply freshness evidence, but parent-level copy or deletion requires a DomainSpec-owned task.
4. Root `.github/skills` entries that duplicate DomainSpec or GSD skills should become downstream generated packages, thin readers, or deletion candidates after runtime need is confirmed.
5. Root `.github/agents` DomainSpec entries should be downstream distribution prompts; MARS research agents are root-owned canonical candidates; GSD root agent files should be treated as bundle/manifest-backed generated formats.
6. Lean formalization skills and agent prompts stay canonical under `domainspec-lean-formalization` for proof-domain work. Shared utilities may be deduped only after preserving Lean-specific guardrails.
7. Machine-global Codex home remains out of scope for this run.

## Approval Question

Approve the next task-session to implement reader/provenance/drift-check changes for root-owned downstream surfaces only, while leaving `implementation/domainspec` and `domainspec-lean-formalization` untouched except for explicit owner-scoped handoffs?

## Blocked Or Deferred

- Any rewrite inside `implementation/domainspec/` needs a DomainSpec-owned task scope.
- Any rewrite/copy of Lean proof-domain skills needs Lean formalization owner approval and guardrail preservation review.
- Any deletion of root `.github` packages needs runtime-need confirmation.
- Root `.github/agents/README.md` says the directory is for research orchestration agents, but the contents include DomainSpec and GSD runtime agents; this policy/content mismatch needs a decision gate.
