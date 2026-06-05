# Task Session Handoff: DomainSpec Skill And Agent Canonicalization

Generated: 2026-06-01T10:28:23Z
Dispatch: `domainspec-skill-agent-canonicalization-20260601`
Status: ready after operator approval

## Inputs

- `ops/development/domainspec-skill-agent-candidate-ledger.md`
- `ops/development/lean-formalization-skill-agent-candidate-ledger.md`
- `ops/development/domainspec-skill-agent-canonical-candidate-matrix.md`
- `ops/development/domainspec-skill-agent-canonical-owner-decision.md`
- `ops/development/domainspec-skill-agent-reader-refresh-plan.md`

## Completion Criteria

- Root-owned downstream surfaces have provenance or an explicit blocked/deletion-candidate classification.
- No parent-level task mutates `implementation/domainspec` or `domainspec-lean-formalization` without an owner-scoped decision.
- A drift-check command exists and reports status without changing files.
- Lean formalization proof-domain guardrails remain stronger or equal to current `CLAUDE.md` instructions.
- Root `.github/agents` policy/content mismatch is resolved or explicitly deferred.

## Stop Conditions

- Block if a generated adapter is selected as canonical source without approval.
- Block if a Lean formalization proof-domain skill would be merged into generic DomainSpec skills.
- Ask before deleting any root `.github/skills` or `.github/agents` package.
