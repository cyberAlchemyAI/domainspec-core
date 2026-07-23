# Classified Strategy Runtime Diff

## Classification

| Surface | Owner | Allowed difference | Parity rule | Result |
| --- | --- | --- | --- | --- |
| `arcanum/arcana/subagent-strategy/SKILL.md` | public Arcanum sigil | none; canonical source | source | pass |
| `.agents/skills/subagent-strategy/SKILL.md` | Arcanum bootstrap projection | provenance frontmatter | normalized canonical semantics | pass |
| `.claude/skills/subagent-strategy/SKILL.md` | Arcanum bootstrap projection | provenance frontmatter and declared `Task` to `Agent` tool mapping | normalized canonical semantics | pass |
| private owner `domainspec-subagents-strategy/SKILL.md` | private DomainSpec tooling | DomainSpec constitution, owners, Inventory preflight, research-output split, paths, and publication boundary | declared local overlay source | pass |
| `.claude/skills/domainspec-subagents-strategy/SKILL.md` | private composition projection | provenance frontmatter only | normalized private-owner semantics plus protected local rules | pass after regeneration |
| `.agents/skills/domainspec-subagents-strategy/SKILL.md` | no owner | none | absent because no private Codex adapter is declared | pass |

## Starting defects

- The public Codex and Claude packages already matched their canonical source.
- The private Claude adapter was a stale 58-line copy of a 212-line owner.
- The private installer declared only a Claude target. A missing private Codex
  package was therefore not drift and was not invented.

## Admission behavior

The composition validator:

- ignores only manifest-declared generated metadata;
- applies only the manifest-declared tool-name adaptation;
- compares normalized semantic content, so whitespace and line wrapping pass;
- fails any other body addition or removal;
- reports protected lifecycle, owner, research-output, and public/private rule
  removal explicitly;
- synchronizes the private adapter only to declared runtime targets.

## Result

`PASS`: the public base remains public, the private adapter remains private,
the stale Claude projection is repaired, and every live runtime difference has
one declared owner.
