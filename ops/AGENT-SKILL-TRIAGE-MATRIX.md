# Agent/Skill Triage Matrix

Source comparison used for this matrix:

- Consumer overlay repo: `validation/poker-team/.github`
- Implementation install target: `implementation/domainspec/.github`
- Canonical Type A source: `implementation/domainspec/copilot`

Migration status (2026-04-20):

- File-by-file verification completed for all poker-team-only mismatches.
- Where poker-team content diverged from canonical Type A files, poker-team version was treated as latest and promoted.
- Type B research assets were promoted to `domainspec-core/.github`.

## Agents only in poker-team (vs implementation/domainspec .github)

| Asset | In canonical copilot | Proposed Type | Action | Notes |
|---|---|---|---|---|
| domainspec-infra-architect.agent.md | yes | Type A | sync to implementation `.github` from canonical | Consumer should not be unique owner |
| domainspec-otel-instrumenter.agent.md | yes | Type A | sync to implementation `.github` from canonical | Consumer should not be unique owner |
| domainspec-otel-verifier.agent.md | yes | Type A | sync to implementation `.github` from canonical | Consumer should not be unique owner |
| domainspec-research-analyst.agent.md | no | Type B | promote to `domainspec-core/.github` | Research orchestration candidate |
| domainspec-research-inventorist.agent.md | no | Type B | promote to `domainspec-core/.github` | Research orchestration candidate |
| domainspec-research-scientist.agent.md | no | Type B | promote to `domainspec-core/.github` | Research orchestration candidate |
| domainspec-research-sourcer.agent.md | no | Type B | promote to `domainspec-core/.github` | Research orchestration candidate |
| domainspec-story-sync.agent.md | yes | Type A | sync to implementation `.github` from canonical | Consumer should not be unique owner |
| domainspec-ui-architect.agent.md | yes | Type A | sync to implementation `.github` from canonical | Consumer should not be unique owner |

## Skills only in poker-team (vs implementation/domainspec .github)

| Asset | In canonical copilot | Proposed Type | Action | Notes |
|---|---|---|---|---|
| domainspec-infra-architecture/SKILL.md | yes | Type A | sync to implementation `.github` from canonical | Consumer should not be unique owner |
| domainspec-infra-deploy/SKILL.md | yes | Type A | sync to implementation `.github` from canonical | Consumer should not be unique owner |
| domainspec-instrument-otel/SKILL.md | yes | Type A | sync to implementation `.github` from canonical | Consumer should not be unique owner |
| domainspec-otel-verify/SKILL.md | yes | Type A | sync to implementation `.github` from canonical | Consumer should not be unique owner |
| domainspec-pilot-readiness/SKILL.md | yes | Type A | sync to implementation `.github` from canonical | Consumer should not be unique owner |
| domainspec-pipeline/SKILL.md | yes | Type A | sync to implementation `.github` from canonical | Consumer should not be unique owner |
| domainspec-reflect/SKILL.md | yes | Type A | sync to implementation `.github` from canonical | Consumer should not be unique owner |
| domainspec-research-analyze/SKILL.md | no | Type B | promote to `domainspec-core/.github` | Research orchestration candidate |
| domainspec-research-inventory-generic/SKILL.md | no | Type B | promote to `domainspec-core/.github` | Research orchestration candidate |
| domainspec-research-inventory/SKILL.md | no | Type B | promote to `domainspec-core/.github` | Research orchestration candidate |
| domainspec-research-sources-generic/SKILL.md | no | Type B | promote to `domainspec-core/.github` | Research orchestration candidate |
| domainspec-research-sources/SKILL.md | no | Type B | promote to `domainspec-core/.github` | Research orchestration candidate |
| domainspec-sync-user-stories/SKILL.md | yes | Type A | promoted to canonical and synced to implementation `.github` | Promoted after file-by-file verification |
| domainspec-ui-audit-bridge/SKILL.md | yes | Type A | promoted to canonical and synced to implementation `.github` | Promoted after file-by-file verification |
| domainspec-ui-implement/SKILL.md | yes | Type A | promoted to canonical and synced to implementation `.github` | Promoted after file-by-file verification |
| domainspec-ui-phase-bridge/SKILL.md | yes | Type A | promoted to canonical and synced to implementation `.github` | Promoted after file-by-file verification |
| domainspec-ui-pipeline/SKILL.md | yes | Type A | sync to implementation `.github` from canonical | Consumer should not be unique owner |
| feature-workflow/SKILL.md | no | Type C | keep local overlay | Generic workflow likely validation-specific |

## Immediate Execution Tasks Derived from Matrix

1. Keep Type A sync one-way from canonical `implementation/domainspec/copilot` to consumer install targets.
2. Keep Type B research ownership in `domainspec-core/.github`.
3. Keep Type C local overlay allowlist minimal (`feature-workflow/SKILL.md` at present).
4. Keep failing drift checks enabled via `tools/check_github_drift.sh` and `.github/workflows/drift-check.yml`.
