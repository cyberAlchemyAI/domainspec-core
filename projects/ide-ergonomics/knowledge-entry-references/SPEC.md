# SPEC - Knowledge Entry References

Status: draft strategy artifact; no runtime implementation
Date: 2026-06-23
Owner if pursued: IDE Ergonomics host-surface owner plus Inventory/Ontology owners
Builds on: [README.md](README.md)

## 1. Problem

The repo-local knowledge system is useful only when its entries can be found,
recognized, and reused while work is happening. Today, inventory and ontology
lookup is mostly a file or shell activity. The IDE can reference files easily, but
it has no equivalent reference popup for knowledge entries such as inventory cards,
EvidenceSets, ontology-map nodes, query findings, or source manifests.

This produces repeated friction:

- the same searches are run again across a session;
- promising results are lost when the user returns to the conversation;
- handoffs and context packs cite broad files instead of precise knowledge handles;
- the user cannot quickly inspect authority, freshness, or residue before reusing
  an entry.

## 2. Primitive

`knowledge-entry-reference` is a read-only IDE primitive with two linked parts:

1. `recent_knowledge_search_cache` - a local cache of the user's last inventory and
   ontology searches.
2. `knowledge_entry_popup` - a small reference popup for one cached or directly
   resolved knowledge entry.

The primitive is analogous to file references, but its unit is a knowledge-system
entry rather than a filesystem path.

## 3. Source Surfaces

Initial source surfaces:

| Surface | Role |
| --- | --- |
| `.arcanum/inventory/index.json` | Primary machine-readable inventory catalog. |
| `.arcanum/inventory/index.md` | Human-readable inventory catalog and summaries. |
| `.arcanum/inventory/entries/evidence-cards/` | Selector-level candidate evidence cards. |
| `.arcanum/inventory/entries/evidence-sets/` | Reusable EvidenceSets for repeated lookup. |
| `.arcanum/inventory/queries/` | Query findings and search sequences. |
| `.arcanum/inventory/raw/manifests/` | Source manifests and ingest boundaries. |
| `.arcanum/ontology-vault/` | Candidate ontology maps and branch condensations. |

The host may add generated projections later, but only if each projection declares
its source and freshness.

## 4. Cache Model

```yaml
recent_knowledge_search:
  cache_id: <stable-host-id>
  query: <user query text>
  source_scope:
    - inventory
    - ontology-vault
  filters:
    tags: []
    status: []
    entry_type: []
  searched_at: <timestamp>
  index_versions:
    inventory_index_json_mtime: <timestamp-or-hash>
    inventory_index_md_mtime: <timestamp-or-hash>
    ontology_map_mtimes: {}
  results:
    - handle: <stable-entry-handle>
      title: <entry title>
      source_surface: inventory | ontology-vault | evidence-card | evidence-set | query | manifest
      path: <repo-relative-path>
      selector: <heading-or-card-id-or-null>
      summary: <short summary>
      match_snippet: <bounded text>
      tags: []
      status: <candidate|verified|draft|flag|stale|open-question|unknown>
      authority: <read-model|candidate|source-evidence|unknown>
      confidence: <high|medium|low|unknown>
```

Cache behavior:

- Cache is local to the workspace and user session profile.
- Cache stores result metadata and bounded snippets, not whole source files.
- Cache entries are marked `stale` when the indexed source has changed since
  `searched_at`.
- Cache invalidation does not delete the user's last result set; it marks it stale
  and offers refresh.

## 5. Entry Handle

Knowledge handles should be short, stable, and source-qualified:

```text
knowledge:<surface>/<handle>
```

Examples:

```text
knowledge:inventory/evset-operational-ontology-definition-decision
knowledge:evidence-card/knowledge-governance-inventory-authority-contract
knowledge:ontology-vault/inventory-evidence-substrate
```

The handle is not a canonical ID unless the source entry already declares one. It is
an IDE reference target.

## 6. Popup Contract

```yaml
knowledge_entry_popup:
  handle: <knowledge-handle>
  title: <entry title>
  source_surface: <inventory|ontology-vault|evidence-card|evidence-set|query|manifest>
  path: <repo-relative-path>
  selector: <heading-or-card-id-or-null>
  cached_from_query: <query-or-null>
  freshness: fresh | stale | missing | unknown
  summary: <short summary>
  match_snippet: <bounded snippet>
  tags: []
  status: <status>
  confidence: <confidence-or-unknown>
  authority_boundary: <plain sentence>
  promotion_owner: <owner-or-none>
  source_refs:
    - <repo-relative-path-or-selector>
  residue:
    - <open issue, contradiction, stale note, or missing evidence>
  actions:
    - open_entry
    - open_source_refs
    - copy_handle
    - add_to_handoff
    - add_to_context_pack
    - park_as_side_node
    - refresh_search
```

## 7. Interaction States

| State | Meaning | UI behavior |
| --- | --- | --- |
| `empty` | No recent search cache exists. | Search input invites inventory/ontology query. |
| `results` | Recent query has usable results. | Show top results and allow popup open. |
| `popup-open` | One entry is selected. | Show compact reference card and actions. |
| `stale` | Source index or entry changed after search. | Badge the popup and offer refresh. |
| `missing` | Cached path or selector no longer resolves. | Preserve handle, show missing state, offer search again. |
| `inserted` | Handle was added to handoff/context/side node. | Show receipt with target artifact or draft. |

## 8. Owner-Safe Actions

| Action | Allowed effect | Boundary |
| --- | --- | --- |
| `open_entry` | Open the source file or entry selector. | No write. |
| `open_source_refs` | Open cited source paths when available. | Source refs remain evidence, not authority. |
| `copy_handle` | Copy the `knowledge:<surface>/<handle>` token. | Token is a reference, not a claim. |
| `add_to_handoff` | Insert handle, summary, and residue into a handoff draft. | Handoff owner still decides route. |
| `add_to_context_pack` | Add the entry to a Context Builder candidate set. | Context pack is generated evidence, not promotion. |
| `park_as_side_node` | Save the entry as a non-interrupting side node. | Does not switch the active task. |
| `refresh_search` | Re-run the cached query against current indexes. | Refresh may change ranking and stale status. |

Disallowed effects:

- creating or editing inventory cards;
- creating or editing ontology nodes;
- promoting a definition, term, or authority claim;
- hiding stale or missing source state;
- collapsing inventory and ontology authority into one generic "knowledge" badge.

## 9. Ranking Hints

The first implementation can rank simply:

1. exact handle or title match;
2. tag match;
3. summary match;
4. source-ref match;
5. recency/freshness;
6. status confidence.

Ranking must remain explainable in the popup through a short `matched because`
field. If the host later adds embedding search, it still needs source path,
freshness, and authority display.

## 10. Pass Conditions

A static proof over fixture searches passes when a reader can answer:

- what query produced this result?
- which source surface supplied it?
- whether the cached result is fresh, stale, missing, or unknown;
- what source refs back it;
- what authority boundary applies;
- how to reuse it in a handoff or context pack without promoting it.

The proof fails if:

- stale cached results look authoritative;
- ontology and inventory entries are visually indistinguishable;
- the popup copies large source bodies instead of bounded snippets and refs;
- an action writes to canonical knowledge artifacts;
- the user cannot tell why a result matched.
