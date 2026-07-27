# L0 Validation Strategy

## Principle

Evidence must distinguish an admitted record from each seeded invalid state.
A green process without negative-discrimination assertions is a false green.

## Matrix

| Claim | Positive | Negative | Exact check |
| --- | --- | --- | --- |
| current policy | 72-hour fixture admitted | 48-hour mutation rejected | `SLA_POLICY_MISMATCH` at SLA path |
| current freshness | fixed `asOf` before expiry admitted | `asOf` after expiry rejected | `STALE_RECORD` at expiry path |
| truth completeness | current witness present | blank witness rejected | `REQUIRED_FIELD` at witness path |
| visibility completeness | all required paths classified | missing path rejected | `UNCLASSIFIED_FIELD` at exact path |
| visibility vocabulary | one of five classes | unknown class rejected | `UNKNOWN_VISIBILITY_CLASS` |
| determinism | repeated run equals first result | n/a | deep equality and stable diagnostic ordering |

## HTML Prototype Matrix

This matrix applies only after `SWU-COOP-002` is explicitly selected.

| Claim | Positive browser probe | Negative boundary | Exact check |
| --- | --- | --- | --- |
| one artifact | invitation, agenda, catalog, and actions share one document | no second deck or copied page | one `prototype.html`; one `main` |
| catalog completeness | fourteen unique project articles render | duplicate or missing project | exactly fourteen unique `data-project-id` values |
| bounded cards | every article exposes current state, limitation, seven-day act, and human ask | missing field or unsupported maturity language | required `data-field` values per article |
| page/presentation continuity | anchor navigation reaches the same semantic sections used for projection | separate hidden truth or presenter copy | links target in-document IDs; no hidden presenter region |
| responsive meaning | 1440×900 and 390×844 preserve all content and reading order | horizontal clipping or missing CTA/field | `scrollWidth <= clientWidth`; desktop/mobile snapshots |
| browser cleanliness | local file renders without errors or external requests | script, remote resource, storage, or network activity | console review, request review, no `script`, `form`, remote `src`/`href` |
| copy boundary | proper-name “Co-Op Engine” plus claim-bounded project language | autonomous matching, AI collaborator, generic knowledge graph, final-copy claim | forbidden-phrase scan and human copy residue |
| meta-narration | structure and labels carry meaning | “this page/section shows/explains” residue | exact phrase review |
| reviewability | desktop and mobile screenshots exist | screenshot substituted for DOM/semantic proof | screenshots accompany, never replace, snapshots and probes |

## Evidence Ceiling

The admission matrix validates only `SWU-COOP-001` record behavior.

The HTML matrix validates only `SWU-COOP-002` fixture completeness, semantic
browser structure, responsive preservation, console/network cleanliness, and
review screenshots. It does not validate admitted multi-record projection,
interaction, accessibility conformance, privacy across observable surfaces,
copy quality, comprehension, coherence, recruitment efficacy, meeting
efficacy, deployment, or public readiness.
