# CyberAlchemy v2 Agent Instructions

This project is staged inside the private `domainspec-core` umbrella. Parent
repository submodule discipline still applies.

## Local Authority Model

- Canonical local definitions source:
  [authority/definitions/DEFINITIONS.md](authority/definitions/DEFINITIONS.md)
- Definitions lookup:
  [authority/definitions/DEFINITIONS-INDEX.md](authority/definitions/DEFINITIONS-INDEX.md)
- Authority import ledgers:
  [authority/imports/README.md](authority/imports/README.md)
- Stable repository constitution:
  [authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md](authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md)
- Project discipline catalog:
  [disciplines/DISCIPLINES.md](disciplines/DISCIPLINES.md)
- Source map:
  [SOURCE-MAP.md](SOURCE-MAP.md)

Narrative, research, observability, inventory, ontology, and ops artifacts may
explain these surfaces, but they do not redefine them.

## Working Rules

- Keep source evidence linked by path. Do not copy large upstream documents into
  this project unless a later import plan requires it.
- Stage scattered definitions, glossaries, constitutions, axioms, quality rules,
  and anti-patterns under `authority/imports/` before promoting them.
- Treat [../.arcanum/inventory/](../.arcanum/inventory/) and
  [../.arcanum/ontology-vault/](../.arcanum/ontology-vault/) as read models and
  candidate maps, not promoted authority.
- Keep public Arcanum patterns separate from private DomainSpec evidence.
- Generated runtime mirrors are evidence of projection, not canonical source.
- Research may propose; authority decides; implementation waits for a gate.
- Every durable informational artifact should carry an Open Questions section or
  link to the artifact that owns its unresolved questions.

## Route Defaults

- Use definitions-governance for new load-bearing terms.
- Use discipline-governance when a recurring project practice needs a catalog
  entry or hardening route.
- Use constitution-governance when a rule should constrain future artifacts.
- Use decision-gate for public/private, promotion, naming, or repository
  extraction decisions that change authority.
- Use task-session only after the relevant design or execution pack exists.
