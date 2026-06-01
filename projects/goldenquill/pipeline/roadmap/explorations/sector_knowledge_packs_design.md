# Design Note — Sector Knowledge Packs

**Status:** EXPLORATION (not committed)
**Stage:** v0.2 or Phase One contractor work
**Created:** 2026-05-06
**Origin:** SSI Booster reference review — pattern pulled from `domain_knowledge_*.json` auto-merge in linkedin_ssi_booster repo

---

## Problem

Scribe drafts across six sectors (workforce of the future, future-proof education, regenerative agriculture, urban/soilless ag, land and community development, eco-art) without sector-specific vocabulary loaded. Today, sector terminology enters via the RFA itself and PROJECT_CONTEXT — but Scribe has no persistent, curated vocabulary layer that accumulates across grants within a sector.

Result: Scribe reinvents sector framing each time. Funder-dialect matching (Law 4) works at the political-register level but not at the domain-terminology level. A USDA SARE reviewer expects different technical vocabulary than an NEA eco-art reviewer, even when both are "progressive" register.

## Pattern Source

The SSI Booster repo uses `domain_knowledge_*.json` files that auto-merge at runtime — each file contributes domain-specific terms, patterns, and scoring criteria. The merge is additive with dedup. This is a clean pattern for Tilth: per-sector JSON files consumed at a known pipeline point.

## Proposed Design

### File layout

```
pipeline/knowledge_packs/
├── workforce_of_the_future.json
├── future_proof_education.json
├── regenerative_agriculture.json
├── urban_soilless_ag.json
├── land_community_development.json
└── eco_art.json
```

### Schema (per pack)

```json
{
  "sector": "regenerative_agriculture",
  "version": "1.0.0",
  "entries": [
    {
      "id": "regen-ag-001",
      "term": "cover cropping",
      "definition": "Planting non-cash crops to protect and enrich soil between production seasons",
      "funder_contexts": ["USDA_SARE", "USDA_NRCS_EQIP", "USDA_AFRI"],
      "dialect_notes": {
        "conservative": "soil conservation practice",
        "progressive": "regenerative soil management",
        "soul_fire": "land healing practice"
      },
      "related_terms": ["green manure", "living mulch", "no-till"],
      "source": "operator-curated"
    }
  ]
}
```

### Consumption point

Scribe PRE-gate. Before Scribe begins drafting, the pipeline:

1. Identifies the sector from the RFA metadata or PROJECT_CONTEXT sector field.
2. Loads the matching knowledge pack JSON.
3. Injects the vocabulary as a structured context block in Scribe's prompt — not as freeform text, but as a keyed reference Scribe can draw from.
4. Law 4 dialect matching operates on top: the pack provides the vocabulary, the dialect register selects which framing to use.

### Merge semantics

When multiple packs apply (e.g., a grant spanning regenerative agriculture + land/community development):

- **Union:** all entries from both packs included.
- **Dedup:** by `id` field. If same `id` appears in two packs, the pack listed first in the RFA's sector tags wins (precedence by sector ordering).
- **No cross-contamination:** packs are read-only at runtime. Scribe does not write back to packs.

### Relationship to Capital Logic Cards (A6 Option C)

Capital Logic Cards are the *strategic* layer — they encode funding patterns, eligibility logic, and funder relationship maps. Knowledge packs are the *vocabulary* layer — they encode what words and concepts belong in a given sector's grant language. The two are complementary:

- A Capital Logic Card might say "SARE values farmer-led research design."
- The knowledge pack provides the terminology: "farmer-led research," "participatory action research," "on-farm trials."

Cards inform *what to argue*. Packs inform *how to say it*.

### Curation model

- Initial packs seeded by operator (Josh) from existing grant experience.
- Scribe does NOT auto-populate packs — that would violate the principle that packs are curated reference, not LLM-generated content.
- Future (v0.3+): Scout could propose new entries based on successful grant language patterns, but additions require operator approval before merge.

## Open questions

1. **Pack size limits?** Scribe context window budget is finite. If a pack grows to 500+ entries, do we paginate or score-rank for relevance to the specific RFA?
2. **Cross-sector terms?** Some terms (e.g., "food sovereignty") appear in multiple sectors. Do we dedup across packs or let each pack carry its own entry with sector-specific dialect notes?
3. **Versioning cadence?** Packs version independently. Semver or date-based?

## Non-goals

- This is not a knowledge graph or ontology. It's a flat vocabulary list with dialect annotations.
- This does not replace RFA-specific terminology extraction — that remains a Scribe PRE-gate responsibility.
- This does not auto-update from external sources. Packs are operator-curated artifacts.
