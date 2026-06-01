# Spec card — Scout sovereignty watch-cluster (keyword expansion)

**STATUS:** PRE-STAGED 2026-05-15 — awaiting integration with the round that introduces seeded-keyword expansion (likely Channel A grants.gov search expansion or Channel D federal program-page seeds).

**Owner:** WS-D / WS-E (Funder Intel DB seeding) — this spec card seeds the keyword expansion that the eventual seeded-keyword config will absorb. Not a runtime change today; a forward-binding contract for when Scout grows a seeded-keyword expansion layer.

**Blueprint anchors:**
- `pipeline/blueprint/v0.1/section_03_scout.md` §4.1 (Channel A federal APIs) — Grants.gov search2 keyword sweep
- `pipeline/blueprint/v0.1/section_03_scout.md` §4.3 (Channel C state portals) — state-portal seeded queries
- `pipeline/blueprint/v0.1/section_03_scout.md` §4.4 (Channel D federal program pages) — program-page seeded URLs and keyword sweep
- `pipeline/blueprint/v0.1/section_03_scout.md` §4.5 (Channel E RSS / newsletter watchlists) — RSS feed seeded watch terms

---

## Summary

Add an eight-term sovereignty / community-AI / local-compute watch-cluster to Scout's seeded keyword expansion. The cluster is **cheap to add and costless if it doesn't land** — Scout already runs the keyword sweep across channels A / C / D / E; adding eight terms to the seeded list does not add a new channel or change the dispatcher shape.

The market signal driving the cluster: Gallup 2026 reported 7 in 10 Americans oppose AI data centers in their neighborhood (48% strongly opposed). The policy environment is shifting toward local-compute / community-AI / digital-sovereignty themes at federal, state, and foundation funding levels. Foundations and state agencies funding community-tech / community-broadband / community-data work over the next 12–18 months are the expected target population.

---

## The cluster

| # | Term                  | Channel A | Channel C | Channel D | Channel E |
|---|-----------------------|-----------|-----------|-----------|-----------|
| 1 | `digital_sovereignty` | ✓         | ✓         | ✓         | ✓         |
| 2 | `community_ai`        | ✓         | ✓         | ✓         | ✓         |
| 3 | `local_compute`       | ✓         | ✓         | ✓         | ✓         |
| 4 | `local_ai`            | ✓         | ✓         | ✓         | ✓         |
| 5 | `private_ai`          | ✓         | —         | ✓         | ✓         |
| 6 | `community_compute`   | ✓         | ✓         | ✓         | ✓         |
| 7 | `data_sovereignty`    | ✓         | ✓         | ✓         | ✓         |
| 8 | `edge_compute_grant`  | ✓         | ✓         | ✓         | ✓         |

Channel-specific notes:
- **Channel A (Grants.gov + SAM + USASpending):** add as Grants.gov search2 keyword expansion terms. Each term is sent as an independent `keyword=` query; results merge via the standard channel-A dedup.
- **Channel C (state portals):** add to seeded query expansion for PA DCED, PA Ag, NY Empire State Development, NJ EDA, and any other state portals already in the seeded-portal list. Coverage prioritizes PA / NY / NJ at v0.1; expand to additional states as portal coverage grows.
- **Channel D (federal program pages):** add as keyword sweep terms for DOE community-energy program pages, NSF community-tech / community-broadband program pages, Commerce community-tech program pages, NTIA digital-equity program pages, and EDA community-development program pages. `private_ai` is excluded from Channel C (state portals rarely carry the exact phrase) but included on D + E.
- **Channel E (RSS / newsletter watchlists):** add to the seeded watch-term list applied across all subscribed RSS feeds and newsletter mirrors.

---

## Why now

Three concurrent signals:

1. **Gallup 2026 — 70% local-data-center opposition** (48% strongly opposed). This is a market signal: local-compute deployments will become politically advantageous for funders to support over the next 12–18 months. Foundation theory-of-change language will follow.
2. **Trump-Xi 2026-05 AI safety protocol direction** — nonstate-actor preventive framing creates regulatory tailwind for sovereign / on-premise / customer-owned deployments. State and federal funders aligning to this direction will use terms like `data_sovereignty` and `digital_sovereignty` in RFA copy.
3. **NTIA Digital Equity programs + state-level digital-inclusion appropriations** — already operating in this space; the watch-cluster catches them with consistent vocabulary.

The cluster is **opportunity-driven, not archetype-driven** (per CLC orthogonality discipline). Any of the six CICs may legitimately tap an opportunity surfaced by this cluster.

---

## Integration plan

When Scout's seeded-keyword expansion layer lands (whether as part of a new Channel A amendment, a Channel D round expansion, or a dedicated keyword-config module), the eight terms in this cluster get absorbed into the seeded-term YAML / Python constant.

Recommended file structure if a dedicated keyword config is created:

```
pipeline/scout/keyword_clusters/
├── __init__.py
├── sovereignty_v1.yaml          # this cluster
├── food_systems_v1.yaml         # placeholder for future clusters
└── ...
```

Each cluster YAML carries: `cluster_id`, `version`, `terms[]` (list of strings), `channel_mask` (bitfield for A/B/C/D/E/F), `effective_date`, `provenance` (URL / origin doc).

---

## Done definition

- [ ] Eight terms appear in Scout's seeded-keyword expansion list (location TBD when expansion layer lands)
- [ ] Channel mask reflects the table above (private_ai excluded from C)
- [ ] Provenance points to this spec card and to The Neuron 2026-05-15 + Gallup 2026 source
- [ ] One full Scout cycle has run with the cluster active; result count by term is captured in `pipeline/orchestrator/run_log.json` (or wherever Scout's per-keyword diagnostics land)

---

## Cost / risk

- **Cost:** ~30 minutes of integration when the keyword expansion layer lands. Zero new channels, zero new code paths.
- **Risk if it doesn't land (no funder activity in the cluster):** zero — terms produce empty result sets, channel state unchanged, no false-positive load.
- **Risk if it does land (funder activity in the cluster):** standard Scout dedup + VERIFY discipline applies; no special handling needed.

---

## Source

External market signal: Gallup 2026 (7 in 10 oppose local AI data centers); Trump-Xi 2026-05 summit AI safety protocol direction. Surfaced via The Neuron daily newsletter 2026-05-15. Pre-staged the same day.
