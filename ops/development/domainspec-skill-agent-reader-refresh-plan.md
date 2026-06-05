# DomainSpec Skill And Agent Reader Refresh Plan

Generated: 2026-06-01T10:28:23Z
Dispatch: `domainspec-skill-agent-canonicalization-20260601`
Status: proposed implementation plan after approval

## Target Mechanics

| Surface | Treatment | Validation |
| --- | --- | --- |
| `implementation/domainspec/copilot/skills/*` | Canonical source candidate for Type A DomainSpec skills. | Owner-scoped DomainSpec validation. |
| `implementation/domainspec/copilot/agents/*` | Canonical source candidate for DomainSpec agent prompts. | Freshness compare against `.github`, `.claude`, and `.codex` adapters. |
| `implementation/domainspec/.agents/skills/*` | DomainSpec-owned local runtime surface. | Compare against canonical and record drift; do not parent-edit. |
| `implementation/domainspec/.github/.claude/.codex agents` | DomainSpec-owned runtime adapters. | Classify and hand off; do not parent-edit. |
| `.github/skills/*` | Downstream generated package, thin reader, root-owned keep, or deletion candidate. | Provenance header plus hash/drift check. |
| `.github/agents/*` | Downstream/root research agent distribution surface. | Split DomainSpec downstream, GSD bundle-generated, and MARS root-owned. |
| `domainspec-lean-formalization/.agents/*` | Separate Lean lane. | Preserve claim/proof and precedent-search guardrails; do not copy without approval. |

## Provenance Header For Generated Packages

```yaml
surface_kind: generated-native-runtime-package
canonical_source: <repo path>
generated_by: <script or task-session id>
mutation_policy: regenerate-from-canonical-source
alias_of: null
```

## Drift Check Shape

A follow-up script should emit rows with:

`logical_id, canonical_path, downstream_path, canonical_sha256, downstream_sha256, status, action`

Statuses:

- `in-sync`: exact body or generated metadata confirms source hash.
- `runtime-rewrite`: downstream package is intentionally runtime-native but cites source.
- `drift`: downstream content differs without provenance.
- `orphan`: downstream package has no canonical candidate.
- `blocked-owner`: candidate crosses `implementation/domainspec` or Lean formalization boundary.

## First Implementation Slice

1. Add or update provenance for root `.github/skills` entries already classified as Arcanum distribution adapters.
2. Add a root drift-check script that compares `.github/skills` and `.github/agents` against selected canonical paths without mutating child owner scopes.
3. Produce a deletion/thin-reader candidate report for duplicates, not immediate deletion.
4. Create owner-scoped handoffs for DomainSpec and Lean formalization changes.
5. Resolve whether root `.github/agents` is only Type B research orchestration or also a generated DomainSpec/GSD distribution surface.
