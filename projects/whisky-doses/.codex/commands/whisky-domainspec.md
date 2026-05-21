# whisky-domainspec

Project-local DomainSpec entrypoint.

Use the installed DomainSpec orchestrator skill:

[../../.Codex/skills/domainspec-orchestrate/SKILL.md](../../.Codex/skills/domainspec-orchestrate/SKILL.md)

Default scope:

- Target project: this repository
- Framework bundle: `domainspec/`
- Runtime assets: `.codex/agents/`, `.Codex/skills/`, `.Codex/get-shit-done/`

Route natural-language project work through `domainspec-orchestrate` unless the user explicitly names a direct `domainspec-*` command.
