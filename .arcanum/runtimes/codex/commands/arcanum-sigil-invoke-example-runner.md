# arcanum-sigil-invoke-example-runner

Run the installed Arcanum `invoke-example-runner` sigil from Codex.

## Canonical Source

- Sigil contract: [../../../../arcanum/arcana/invoke-example-runner/SKILL.md](../../../../arcanum/arcana/invoke-example-runner/SKILL.md)
- Prompt selector: [../../../../arcanum/spells/invoke/development/select-template-example-prompt.sh](../../../../arcanum/spells/invoke/development/select-template-example-prompt.sh)
- Invoke command bridge: [../../../../.codex/commands/arcanum-spell-invoke.md](../../../../.codex/commands/arcanum-spell-invoke.md)

## Usage

```text
arcanum-sigil-invoke-example-runner next
arcanum-sigil-invoke-example-runner sigil-medium
arcanum-sigil-invoke-example-runner sigil medium
```

## Process

1. Read the canonical sigil contract.
2. Run the selector script with the requested task ID, template and complexity, or `next`.
3. Read the selected prompt.
4. Execute the prompt's **Codex Prompt** section in the current Codex session.
5. Save the resulting `Invoke Result` to the selector's output path.
6. Return the standard Invoke Example Runner Result.
