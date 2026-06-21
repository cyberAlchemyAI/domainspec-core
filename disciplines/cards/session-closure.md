# Session Closure Discipline

Status: candidate
Steward: vault / close-session
Scope: PRIVATE (umbrella root only)

## Purpose

Govern the practice that a multi-turn agent session is closed into a recorded, edge-wired vault session node (forward-only edges), so work is provenance-traceable rather than lost at the end of a conversation.

## Boundary

Names the session-closure practice. It does not own the vault ontology/edge catalog itself, the content of the work being closed, or the observability signal emission (a private profile of the public `observability` discipline).

## Evidence

- [sessions/](../../sessions/) - 20+ recorded session nodes (evidence the practice recurs).
- [close-session skill](../../implementation/domainspec/.claude/skills/close-session/SKILL.md) - the capability that creates the vault session node and wires edges.

## Validation

- Mode: prose-review
- Check: review that a closed session produced a vault node with legal forward-only edges.
- Latest result: not-run (this session)

## Quality Bar

A useful entry must: name when closure is required (multi-turn / concrete outputs), require a recorded session node with legal edges, keep it distinct from signal emission, and stay private to the umbrella vault.

## Promotion Guardrail

Can recommend a catalog-only or edge-legality-validator route; cannot promote vault, ontology, registry, glossary, sigil, or spell knowledge. Candidate until closure has a named validation surface.
