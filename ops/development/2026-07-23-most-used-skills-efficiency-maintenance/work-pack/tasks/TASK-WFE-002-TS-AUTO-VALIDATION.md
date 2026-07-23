# TASK-WFE-002 — Narrow Task Session Auto And Validation Outcomes

- Change: TS-1 / WFE-R01
- Layer/slice/wave: L0 / S0 / W0
- Lifecycle owner: `sigil-development` for Task Session
- Status: complete — [receipt](../session-evidence/SWU-WFE-002/receipt.json)

## Objective

Remove subjective auto-consent and prevent unmet acceptance-critical validation
from returning a completion-capable `FLAG`, while preserving recovery and named
noncritical residue.

## Sources

- `arcanum/arcana/task-session/SKILL.md`: steps 19–24 and 41–48
- `.agents/skills/task-session/SKILL.md` and installed declared runtime mirrors
- `../../DESIGN.md`: Task Session decision/completion guard
- accepted findings TS-1

## Dependencies and write scope

- Program-order dependency: TASK-WFE-001 closure receipt.
- Technical dependency: none.
- Canonical first: `arcanum/arcana/task-session/` contract and new focused fixtures.
- Generated second: only runtime targets declared by the generator manifest.
- Forbidden: application tasks, changing `FLAG` for noncritical residue, or
  weakening live validation/recovery.

## SWU-WFE-002

- Primary behavior: classify automatic choices and validation completion so
  consequential choice or acceptance-critical failure cannot appear complete.
- Acceptance boundary: blocker auto-choice and critical-validation red fixtures
  fail; reversible nonconsequential auto-choice and named noncritical `FLAG`
  positive controls pass.
- Split analysis: choice and validation are two clauses in the same Task Session
  admission/completion contract and the accepted repair requires their combined
  status semantics; either clause alone would preserve a false-ready route.

### Implementation rules

1. Delete “or where a recommendation is clearly safe.”
2. Auto-select only an explicitly classified nonconsequential and reversible
   option; otherwise ask or block.
3. Add done-criterion criticality or an equivalent explicit classification.
4. Required validation failure, or inability to run it without an accepted
   equivalent, returns `BLOCK`.
5. `FLAG` remains for named noncritical residue that cannot falsify any done
   criterion.
6. Add contract-level negative and positive fixtures and generated parity checks.

### Validation

```bash
bash arcanum/arcana/task-session/development/run-validation-fixtures.sh
git diff --check -- arcanum/arcana/task-session .agents/skills/task-session .claude/skills/task-session
```

If no focused harness exists, creating it is part of this SWU and its absence
before mutation is the red baseline, not permission to use prose-only review.

- Execution owner: `sigil-development`.
- Handoff: exact contract selectors, generated manifest, fixture command, and
  public submodule boundary.
- Receipt: new fixture names and outcomes, canonical/generated parity, residue.

## Done

Canonical contract and declared runtimes agree semantically; the negative suite
proves the two prior escape paths fail; existing valid flows remain green.
