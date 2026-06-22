# Runtime Handoff: IDE Ergonomics Refine

Status: deferred-awaiting-confirmation
Run ID: 20260619T171214Z-ide-ergonomics
Dispatch ID: refine-20260619T171214Z-ide-ergonomics
Target: `projects/ide-ergonomics`

## Runtime Objective

If approved later, run the canonical Refine loop for the `ide-ergonomics`
project so stage owners can produce native artifacts for define, review,
distill, design, repair, plan, and final synthesis.

## Current Permission State

- Runtime-backed stages: not approved in this turn.
- Subagent fanout: recommended, not approved.
- External web or host-specific research: not selected; research mode is
  `no-research`.
- Canonical Arcanum mutations: not approved.

## Proposed Subagents For A Later Approved Run

| Role | Owns | Why |
| --- | --- | --- |
| `action-card-workflow-mapper` | Conversation action model, handoff composer, route menu, receipt expectations. | Keeps the user workflow concrete. |
| `host-surface-constraints-reviewer` | IDE or rules-package constraints and validation evidence. | Prevents designing a UI the host cannot expose. |
| `governance-boundary-guardian` | Definition, ontology, spell, sigil, subagent, and observability boundaries. | Prevents action buttons from becoming unsafe shortcuts. |

## Receipt Requirements

Any future subagent or runtime-backed stage must return:

- `agent_id` or native stage id;
- `role_id` or capability id;
- `dispatch_id`;
- `step_id`;
- spawn/join/close status when delegated;
- artifact paths;
- validation result;
- observer status;
- blockers;
- residue;
- handoff note.

## Next Runnable Prompt

```text
Continue from projects/ide-ergonomics/development/refinement-runs/20260619T171214Z-ide-ergonomics/.

Run the approved Refine loop for IDE Ergonomics. Preserve the project boundary:
do not mutate canonical Arcanum, generated skills, definitions, disciplines, or
runtime packages unless a later owner route approves it.

If subagents are approved, spawn only the three role-bound lanes named in
RUNTIME-HANDOFF.md and collect receipts before parent synthesis.
```

## Blocked Fields

- Host surface not selected.
- Validation surface not selected.
- Runtime-backed stage receipts not produced.
- Subagent lifecycle not executed.
- Spellcraft lifecycle not started.
- Discipline Governance lifecycle not started.
