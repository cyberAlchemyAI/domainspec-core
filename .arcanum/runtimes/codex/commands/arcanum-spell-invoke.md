# arcanum-spell-invoke

Run the installed Arcanum `invoke` spell from the canonical repository contract.

## Canonical Source

- Spell contract: [../../../../arcanum/spells/invoke/README.md](../../../../arcanum/spells/invoke/README.md)
- Mode contracts:
  - [../../../../arcanum/spells/invoke/define.md](../../../../arcanum/spells/invoke/define.md)
  - [../../../../arcanum/spells/invoke/design.md](../../../../arcanum/spells/invoke/design.md)
  - [../../../../arcanum/spells/invoke/plan.md](../../../../arcanum/spells/invoke/plan.md)
  - [../../../../arcanum/spells/invoke/full.md](../../../../arcanum/spells/invoke/full.md)
  - [../../../../arcanum/spells/invoke/validate.md](../../../../arcanum/spells/invoke/validate.md)

## Usage

Invoke this command in Codex when the user asks to define, design, plan, fully run, or validate governed development artifacts through `invoke`.

Examples:

```text
arcanum-spell-invoke define <goal>
arcanum-spell-invoke design <approved-spec-and-glossary>
arcanum-spell-invoke validate <artifact-paths>
```

## Process

1. Read the canonical spell contract from `arcanum/spells/invoke/README.md`.
2. Resolve the requested mode. If no mode is named, infer the smallest mode that satisfies the request and state the inference.
3. Read the mode contract for that mode.
4. Apply the spell gates exactly:
   - use one-question clarification when core context is missing,
   - record template or profile selection evidence,
   - do not silently mutate upstream artifacts,
   - record unresolved gaps instead of hiding them,
   - route spell and sigil lifecycle execution to `spellcraft` or `sigil-development`.
5. For deferred modes, return the deferred-mode contract and the required activation gate instead of pretending the mode is implemented.
6. When `.arcanum/observability/` exists, summarize the run using the spell output contract and note whether telemetry was recorded.
7. Return the standard `Invoke Result` from the canonical contract.

## Validation

This adapter is valid when:

- the canonical source links resolve,
- the adapter points to canonical `arcanum/spells/invoke` files instead of copying their full bodies,
- the adapter exposes `define`, `design`, `plan`, `full`, and `validate` routing,
- deferred modes remain deferred until their canonical contracts change,
- dry-run fixture results are recorded in `arcanum/spells/invoke/development/VALIDATION.md`.
