# Candidate Glossary

These terms are local to this Invoke package. They are not promoted Arcanum or
DomainSpec definitions.

| Term | Meaning | Boundary |
|---|---|---|
| Append transition | One attempted change from exact Inventory baseline projections to a staged candidate and observed outcome. | Not an authority transition. |
| Operation receipt | Canonical digest-bound evidence describing one append attempt. | Historical evidence; not currentness. |
| Candidate B | The selected build-from-owned operation wrapper from the accepted research. | Design target, not implemented runtime. |
| Baseline | Exact pre-operation `index.json` and human-index bytes plus full validator result. | May already contain inherited warnings. |
| Candidate | Staged projections computed before any write. | Must pass full conformance before apply. |
| Warning identity | Digest of stable warning code, subject, and selector. | Does not assign severity or truth. |
| Warning delta | Introduced, resolved, and inherited warning sets between baseline and candidate. | Full reports still expose all warnings. |
| Identical no-op | Existing stable ID whose normalized content equals the request. | Zero writes and unchanged timestamp. |
| ID conflict | Existing stable ID whose normalized content differs from the request. | Blocks before write. |
| Namespace | One stable owner/project scope used as the first physical directory axis. | Retrieval/organization metadata, not definition namespace authority. |
| Record class | One controlled lifecycle or artifact family used as the second physical directory axis. | Separate from existing entry `type`. |
| Concept facet | Multi-valued retrieval label derived into logical indexes. | Never determines physical nesting or governed meaning. |
| Faceted entry | New record carrying namespace, record class, and concept facets. | Legacy records need not be rewritten. |
| Physical path | The single canonical storage location of an entry. | Does not determine all retrieval memberships. |
| Logical projection | Derived machine or human view such as `by_concept`. | Non-authority and reproducible from `index.json`. |
| Legacy entry | Existing record admitted under the pre-facet schema/path policy. | Remains valid and unmoved in this plan. |
| Runtime manifest | Relative-path and digest inventory for generated runtime members. | Excludes consumer-owned mutable state. |
| Partial mutation | Failure state in which one sequential projection may have changed. | Must not be called committed or rolled back. |
| Currentness verifier | Separate future capability that compares a receipt-bound digest with live state. | Excluded and owner unresolved. |

