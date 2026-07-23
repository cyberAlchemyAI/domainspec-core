# Experiment Report: SWU-WFE-009

- Verdict: `PASS`
- Causal fixtures: 10/10
- Live overall verdict: `pass`
- Live lookup readiness: `ready`
- Live failures: 0
- Historical uncontrolled-tag warnings: 72
- Enabled live projections: 0

## Live conformance

| Subcheck | Evidence | Result |
| --- | ---: | --- |
| source coverage | 152 configured sources and 152 indexed governed paths | pass |
| stable identity | 208 unique ID/path bindings; 19 embedded source IDs checked | pass |
| existence | 208 indexed paths | pass |
| derived maps | `by_id`, `by_type`, `by_tag`, `by_source`, `by_status`, `by_evidence_card`, `by_evidence_set` | pass |
| human view | 174 represented machine rows and 174 human rows | pass |
| projection freshness | no enabled projection; timestamp parseable | pass |
| tag policy | 72 historical tags outside `tags.md` | warn-only |

The initial live run causally failed on five stale derived maps. Those maps were
regenerated only from the current 208 entries, without changing entry content,
then the same validator passed.

## Fixture matrix

The focused harness proves current complete input, a current enabled
projection, and warn-only uncontrolled tags pass. It proves missing source row,
orphan machine row, missing path, `by_id` mismatch, derived-map drift,
human/machine type mismatch, and stale projection digest/timestamp fail.

## Boundary

This is an Inventory read-model integrity proof. It does not promote source
meaning, close the tag vocabulary, enable a projection, or grant authority to a
human or machine view.
