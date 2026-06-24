---
tags: [ide, ergonomics, inventory, ontology, knowledge-system, references]
node_type: feature
layer: product, workflow, knowledge
nature: design-seed
status: strategy-proposal
created: 2026-06-23
---

# Knowledge Entry References

An IDE-side ergonomic primitive for reusing the last inventory and ontology
searches as clickable knowledge references.

The current IDE Ergonomics project already treats files, spans, handoffs, and
route moments as things the user can act on. This primitive adds the missing
knowledge-system version: a user should be able to search the local Inventory or
Ontology surface once, keep the recent result set cached, and reopen any result
through a small popup that behaves like a file-reference preview.

## Why it belongs here

When the user knows the knowledge system already contains something, the friction
is not only search. It is re-finding the same inventory cards, EvidenceSets,
ontology-map nodes, source refs, and promotion boundaries while the conversation is
moving.

The ergonomic target is:

- cached recent searches over `.arcanum/inventory/index.json`,
  `.arcanum/inventory/index.md`, evidence-card files, EvidenceSet files, and
  `.arcanum/ontology-vault/` maps;
- inline handles that can be inserted into chat, handoffs, route menus, or source
  fields;
- a reference popup that shows what the entry says, where it came from, how fresh
  the cached result is, and what authority boundary applies.

## User Experience

The user searches once:

```text
knowledge: operational ontology lifecycle
```

The IDE keeps the result set in a recent-search cache. Later, typing or clicking a
knowledge handle opens a small popup:

```text
operational-ontology-authority-lifecycle
Type: evidence-card / EvidenceSet
Status: candidate read model
Source refs: ...
Authority: inventory evidence, not definition promotion
Actions: Open entry, Open source refs, Add to handoff, Add to context pack
```

The popup is intentionally close to a file-reference hover: it lets the user inspect
and reuse a known thing without leaving the current workflow.

## Owner-Safe Route

```text
inventory or ontology query
  -> recent search cache
  -> selected knowledge entry handle
  -> reference popup
  -> optional insert into route, handoff, context pack, or side node
  -> no authority promotion
```

The popup can make knowledge visible and reusable, but it does not decide that the
knowledge is canonical. Inventory entries remain read models; ontology maps remain
candidate condensations unless their owner route promotes them.

## Popup Contents

Each popup should show:

- entry title and stable handle;
- source surface: inventory, ontology-vault, evidence-card, EvidenceSet, query, or
  source manifest;
- summary and matching snippet;
- tags, status, confidence, and updated date when available;
- source refs or selectors;
- authority level and promotion owner;
- unresolved residue, contradiction, or stale-cache warning;
- actions to open the entry, open source refs, copy a knowledge handle, add to a
  handoff, add to a context pack, or park as a side node.

## Cache Rules

- Cache recent query text, filters, result handles, matched snippets, index version,
  and source paths.
- Treat cached results as convenience, not proof. If `index.json`, `index.md`, or
  the referenced entry changed after the cache was built, the popup marks the entry
  stale and offers refresh.
- Keep inventory and ontology result classes separate in the UI; a combined search
  may rank across both, but the popup must show which surface supplied the result.
- Never synthesize a new entry from the cache alone.

## Files

- [SPEC.md](SPEC.md) - UX contract, cache model, popup fields, actions, and pass
  conditions.

## Boundaries

- Strategy proposal only; no IDE extension, indexer, or runtime cache is built in
  this folder.
- The primitive reads inventory and ontology artifacts; it does not mutate
  `.arcanum/inventory/` or `.arcanum/ontology-vault/`.
- Promotion remains with the downstream owner: inventory, ontology-vault,
  definitions-governance, constitution-governance, decision-gate, or another
  explicitly selected route.
