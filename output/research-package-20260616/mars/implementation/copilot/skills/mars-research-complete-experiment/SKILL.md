---
name: mars-research-complete-experiment
description: "Guide any research experiment bundle to completion using staged AskQuestions decision packs, gate checks (G1-G4), adjudication closure, and claim-status propagation."
argument-hint: "<project-key> <experiment-key> [--mode audit|guide|execute] [--strict-gates] [--skip-analysis] [--skip-claim-update]"
agent: mars-research-orchestrator
allowed-tools: Read, Write, Bash, Glob, Grep, AskQuestions, Task
---

<objective>
Guide an experiment from its current state to a defensible completion state with explicit decisions, auditable gates, and clear claim-impact outcomes.

This skill is for experiments that are partially complete, blocked, or inconsistent across context/protocol/sources/data/results/adjudication artifacts.
</objective>

<context>
Target bundle artifacts:
- `research/projects/<project-key>/experiments/<experiment-key>/context.md`
- `research/projects/<project-key>/experiments/<experiment-key>/protocol.md`
- `research/projects/<project-key>/experiments/<experiment-key>/sources.md`
- `research/projects/<project-key>/experiments/<experiment-key>/data/*.jsonl`
- `research/projects/<project-key>/experiments/<experiment-key>/results/*.md`
- `research/projects/<project-key>/experiments/<experiment-key>/README.md`

Project-level contracts:
- `research/projects/<project-key>/experiments/EXPERIMENTS.md`
- `research/projects/<project-key>/experiments/README.md`
- `research/projects/<project-key>/experiments/OPEN-DECISIONS.md`
- `research/projects/<project-key>/claims/CLAIMS.md`
- `research/projects/<project-key>/registry/TRACEABILITY-MATRIX.md`
- `research/projects/<project-key>/results/MARS-EVIDENCE-STATUS.md`

MARS references:
- `implementation/mars/definitions/MARS-PIPELINE.md`
- `implementation/mars/definitions/EXPERIMENT-BUNDLE-CONTRACT.md`
- `implementation/mars/definitions/RESEARCH-KNOWLEDGE-STACK-CONTRACT.md`
</context>

<modes>
- `--mode audit`: Read-only completion audit. Produces a gap map and prioritized next actions.
- `--mode guide` (default): Interactive guided closure. Uses AskQuestions for unresolved decisions and writes completion artifacts.
- `--mode execute`: Guided closure plus deterministic remediations and delegated sub-work where safe.

Optional controls:
- `--strict-gates`: treat any failed G1-G4 condition as hard block.
- `--skip-analysis`: allow completion guidance without re-running analysis.
- `--skip-claim-update`: do not mutate claim/evidence status files.
</modes>

<completion-contract>
An experiment is "completion-ready" only when all conditions below pass:

1. Bundle integrity
- `context.md`, `protocol.md`, `sources.md`, and bundle `README.md` exist.

2. Decision lock
- Blocker-level multi-option decisions are resolved and persisted.

3. Gate readiness
- G1 protocol quality pass.
- G2 source quality pass.
- G3 inventory linkage pass.
- G4 data/schema integrity pass.

4. Execution evidence
- Required run data exists and sampling minimums declared in protocol are met.

5. Analysis and threats
- Analysis output exists with success-criteria evaluation and validity threats.

6. Adjudication closure (when reliability policy requires it)
- Required rater outputs exist.
- Disagreements resolved with explicit rationale.
- Unresolved adjudication count is zero.

7. Claim and status propagation
- Claim/evidence files updated or explicitly deferred with reason.
- Experiment index and open-decisions rollup refreshed.
</completion-contract>

<question-packs>
Use AskQuestions for unresolved decisions in this order. Ask only unresolved items.

Pack A - Scope and finish line
- completion target (pilot closure, publication-grade closure, claim movement)
- decision owner
- required completion date

Pack B - Gate policy
- strict vs conditional gate policy
- allowed provisional evidence modes
- rerun policy (required vs optional)

Pack C - Adjudication policy
- reliability mode (single-rater, dual-rater, dual+rater-three)
- disagreement threshold and tie-break policy
- rationale depth requirement

Pack D - Adjudication closure execution
- raters/verifier identity lock
- frozen subset confirmation
- closure mode (`strict-protocol` vs `policy-override`)
- explicit D4 decision target (`go` or `no-go`)
- claim update scope after adjudication closure

Pack E - Claim movement policy
- claim status update threshold
- conservative vs aggressive adjudication stance
- cross-claim propagation scope
</question-packs>

<process>
1. Resolve target paths.
- Validate bundle path and key project contracts.
- If experiment path is ambiguous, stop and request disambiguation.

2. Build a completion matrix.
- Inspect bundle and project artifacts against completion contract.
- Mark each condition: `pass`, `needs-work`, or `blocked`.

3. Run decision packs (AskQuestions).
- Ask only blocker-level unresolved decisions first.
- During adjudication closure, AskQuestions is mandatory (do not infer rater/verifier choices from existing files alone).
- Persist answers to:
  - `research/projects/<project-key>/experiments/<experiment-key>/results/COMPLETION-DECISIONS.md`
- Include table columns:
  - decision_id
  - decision
  - considered_options
  - selected_option
  - rationale
  - blocking (yes/no)
  - source (AskQuestions/chat)
  - timestamp

4. Stop early for audit mode.
- If `--mode audit`, return completion matrix + blockers + recommended wave plan.

5. Execute dependency-ordered closure waves for guide/execute modes.

Wave W1: Context/protocol hardening
- Fill missing context/protocol declarations and decision locks.
- If canonical semantics are missing, delegate to `mars-research-definitions-governance` before proceeding.

Wave W2: Source/inventory gate readiness
- Validate pins, authority status, and linkage.
- If authority drift exists, delegate to `mars-research-authority-governance`.

Wave W3: Data readiness and run integrity
- Validate run schema and metadata against protocol.
- In execute mode, run deterministic checks and capture verification outputs in results.

Wave W4: Analysis and threat assessment
- Unless `--skip-analysis`, delegate to `mars-research-analyze` for missing or stale analysis.

Wave W5: Adjudication and claim decision
- Enforce reliability-mode requirements from protocol and decisions.
- Require disagreement resolution and final rationale log before claim movement.
- Run AskQuestions adjudication closure pack and persist the outcomes before mutating adjudication artifacts.
- Required AskQuestions-derived fields:
  - closure mode
  - verifier/rater IDs
  - subset lock confirmation
  - D4 decision target
  - claim update scope
- If protocol-required multi-rater artifacts are incomplete:
  - In strict mode: stop and return `blocked`.
  - In guide/execute mode: AskQuestions must capture explicit `policy-override` or `strict-protocol` decision.
  - If `policy-override` is selected, record reason and revisit trigger in `COMPLETION-DECISIONS.md` and adjudication log.
- For closure-mode `strict-protocol` or `policy-override`, ensure these files exist before declaring completion:
  - `results/<experiment>-adjudication-rater-a-human-<date>.csv` (or equivalent)
  - `results/<experiment>-adjudication-rater-b-human-<date>.csv` (or equivalent)
  - `results/<experiment>-adjudication-disagreements-human-<date>.csv` (or equivalent)
  - `results/<experiment>-adjudication-third-rater-human-<date>.csv` (or equivalent)
  - `results/<experiment>-human-adjudication-verification-<date>.md` (or equivalent)
- Update claim/evidence files unless `--skip-claim-update` is set.

Wave W6: Program-level closeout
- Update experiment status in `EXPERIMENTS.md`.
- Refresh indexes using `./tools/update_project_experiments_index.sh <project-key>`.
- Run `./tools/check_research_structure.sh`.

6. Blocking policy
- In strict mode, any failed blocker marks experiment `blocked`.
- In non-strict mode, emit explicit residual risks and no-go conditions.

7. Publish completion artifacts
- `results/COMPLETION-CHECKLIST.md`
- `results/COMPLETION-DECISIONS.md`
- `results/COMPLETION-STATUS.md`
</process>

<quality-bar>
- No claim movement without explicit evidence trail (claim -> experiment -> data -> analysis -> adjudication).
- No gate pass without artifact evidence.
- Decision records must be reproducible and timestamped.
- Adjudication closure must report unresolved count and rationale coverage.
- Any adjudication policy override must include reason, decision owner, and revisit trigger.
- Final status must distinguish `complete`, `blocked`, and `needs-follow-up`.
</quality-bar>

<output-contract>
Return:

```markdown
## Experiment Completion Summary
- Project: <project-key>
- Experiment: <experiment-key>
- Mode: audit | guide | execute
- Completion status: complete | blocked | needs-follow-up
- Decisions captured: <n>
- Blockers: <n>

| Contract Area | Status | Evidence |
|---|---|---|
| Bundle integrity | pass/fail | <artifact> |
| Decision lock | pass/fail | <artifact> |
| G1 | pass/fail | <artifact/check> |
| G2 | pass/fail | <artifact/check> |
| G3 | pass/fail | <artifact/check> |
| G4 | pass/fail | <artifact/check> |
| Analysis | pass/fail | <artifact> |
| Adjudication | pass/fail | <artifact> |
| Claim propagation | pass/fail | <artifact> |

### Residual Risks
1. <risk>

### Next Actions
1. <action>
2. <action>
```
</output-contract>
