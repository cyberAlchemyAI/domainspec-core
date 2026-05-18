# arcanum-sigil-experiment-harness

Use the canonical Arcanum sigil at:

`arcanum/arcana/experiment-harness/SKILL.md`

## Command Intents

- `init <artifact-path> --type spell|sigil`
- `next <artifact-path>`
- `run <artifact-path> <example-id|next|--all>`
- `validate <artifact-path>`
- `report <artifact-path>`
- `observe <artifact-path> [report-path]`

## Process

1. Read the canonical sigil contract.
2. Resolve the requested intent and artifact path.
3. Prefer the deterministic script for the intent:
   - `arcanum/arcana/experiment-harness/scripts/init-harness.sh`
   - `arcanum/arcana/experiment-harness/scripts/select-prompt.sh`
   - `arcanum/arcana/experiment-harness/scripts/run-with-codex.sh`
   - `arcanum/arcana/experiment-harness/scripts/validate-harness.sh`
   - `arcanum/arcana/experiment-harness/scripts/report-harness.sh`
   - `arcanum/arcana/experiment-harness/scripts/observe-harness.sh`
4. Return the selected task, output path, report path, validation state, and next unrun prompt.

## Guardrails

- Do not run every prompt unless the user explicitly supplies `--all`.
- Do not overwrite existing example outputs unless `RERUN=1` is set.
- Treat save-summary outputs as invalid evidence.
- Observability telemetry is non-blocking and should append exactly one event per report.
- Observer hook activity belongs in `.arcanum/observability/hooks/`, not in the capability telemetry ledger.
- Keep artifact-specific contract changes routed through `spellcraft` or `sigil-development`.
