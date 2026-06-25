# Authority Triage (sigil candidate)

Status: **candidate** (parent-repo dev location; promotion target
`arcanum/arcana/authority-triage/` after experiment-harness validation)
Tier: arcana · Domain: authority-governance · Contract: [SKILL.md](SKILL.md)

## What it is

The **executable front-door** of the authority system: given any candidate (a
claim, term, principle, rule, practice, decision, artifact — *or a note captured
only in chat / Claude Code memory*), it decides:

1. **does this need authority at all?** (or is it just evidence/a note),
2. **is it already owned?** (precedent sweep → build-from-owned, never reinvent),
3. **what kind of authority is it?** (Definition / Constitution / Discipline /
   Decision / Axiom-candidate / Proposition / …),
4. **which owner's governance cycle does it route to?**

It **promotes nothing** — it classifies and hands off to the narrowest owner
(`definitions-governance`, `constitution-governance`, `discipline-governance`,
`decision-gate`, or the VALUE doc).

## Why it exists

Important principles keep getting **captured in low-authority surfaces** — chat,
side-notes, the opportunity intake, Claude Code memory — and either (a) get
silently treated as authority they don't have, or (b) never get routed to a real
owner. This sigil is the bridge from *capture* → *governed authority*, and it
enforces the two things people skip: **build-from-owned** (sweep before creating)
and **default-deny** (an unenumerated authority kind is blocked until an owner
adds it).

## Build-from-owned

The classification + routing logic is **owned** by
`cyberAlchemy-v2/authority/AUTHORITY-MODEL.md` (the Authority Rule, the Authority
Kinds table, the Narrowest-Owner Rule) + `CAV2-D48` (promotion lifecycle) +
`CAV2-D49` (closed-kind default-deny). This sigil *executes* that model; it does
not redefine it.

## Status / next

- `candidate` — not yet validated. Next: initialize an `experiment-harness`
  (low/medium/complex candidates incl. a definition, a constitution-rule, a
  value-proposition, an unenumerated-kind default-deny case, and a build-from-owned
  case) before promoting to `arcanum/arcana/`.
- First worked example (in SKILL.md): the **build-from-owned principle** itself →
  verdict `build-from-owned` (already authority via CAV2-D48), consolidation
  optional, **do not create new**.
