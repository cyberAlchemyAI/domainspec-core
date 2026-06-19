---
id: operating-skill-validation
project: ui-prototyping-studio
node_type: validation-guide
updatedAt: 2026-06-17
---

# Validation — how to run the operating-SKILL harness

## Run (dry-run, default)

```bash
cd projects/ui-prototyping-studio/development/operating-skill-harness
./run-validation-fixtures.sh <transcript.jsonl>
```

- Checks M1–M5 (mechanizable) against a supplied session transcript.
- Records `QUALITY_BAR_STATUS`, `ANTI_PATTERN_HITS_JSON`, `WORKFLOW_GAPS_JSON` and a per-check report
  under `runs/<ts>.md` (git-ignored).
- Exits **non-zero** on any anti-pattern hit (M1/M5 block) or QB fail (M2/M3/M4).
- R1–R3 are recorded `not_checked` — they need human judgment (authorship/narration honesty).

## Pass criteria (frozen in VALIDATION-EXPERIMENT.md)

- `RESULT=pass` requires: no agent-actor durable gate verb (M1), `data-od-id` on registered variants (M2),
  comment `selector`+`elementLabel` present (M3), no `preview`/`accept`/`discard` (M4), a human-actor
  disposition observed (M5) — AND a human confirms R1–R3 are not `fail`.

## Live capture (explicit, separate — owned by experiment-harness / sigil-development)

Run a scripted Claude Code session under the SKILL against the `studio` CLI with
`STUDIO_ACTOR=agent:claude-code`, log each invocation as one JSON line (schema in VALIDATION-EXPERIMENT.md),
then feed the transcript to the runner. Live AI execution is never implicit.

## Status

Proposal scaffold authored by `invoke`. Lifecycle owner for running/promotion: `experiment-harness` /
`sigil-development`. The runner's mechanizable path is self-tested (see `runs/` after a run); the rubric
path is intentionally human.
