# Private Disciplines (umbrella root)

This is the **private** disciplines layer for the `domainspec-core` umbrella repo. It is the counterpart to the **public** [`arcanum/disciplines/`](../arcanum/disciplines/README.md) catalog, and it exists to hold recurring cross-capability practices that are **specific to this private umbrella** and must **never** be placed in the public arcanum catalog.

## Why a separate, private home

`arcanum` is public; the umbrella root, `implementation/domainspec`, and `validation/*` are private. The [open/private boundary](../SUBMODULE-DISCIPLINE.md) forbids private content in the public submodule. Some practices recur across this umbrella but are tied to its private composition (submodule orchestration, asset ownership across the 3-repo topology, vault session closure). Those are real disciplines, but they belong here, not in `arcanum/disciplines/`.

## Boundary against the public catalog

- A practice that generalizes beyond this repo → formalize in **public** [`arcanum/disciplines/`](../arcanum/disciplines/) via the [discipline-governance](../arcanum/arcana/discipline-governance/) sigil.
- A practice tied to this private umbrella → formalize **here**.
- A practice that is just a private *profile* of an existing public discipline (e.g. domainspec signal emission ⊂ arcanum `observability`) → do **not** mint a new discipline; note it as a profile of the public one.

## Contents

- [DISCIPLINES.md](DISCIPLINES.md) — the private catalog (same row shape as the public one).
- `cards/` — one card per private discipline.

Cards mirror the arcanum card shape so the same review discipline applies. (A private catalog validator can be added later; until then, review cards by hand and keep evidence links resolving within the umbrella.)

## Origin

Created 2026-06-21 from a `discipline-governance scan` over the umbrella root, which found that the umbrella's most drift-prone recurring practice (submodule orchestration) had no formal home and could not go into the public catalog.
