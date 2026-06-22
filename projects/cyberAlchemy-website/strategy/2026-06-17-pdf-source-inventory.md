# PDF Source Inventory

Status: preliminary scan for the CyberAlchemy website strategy.

The local environment did not expose `pdfinfo` or `pdftotext`, so this inventory
uses filesystem discovery plus page counts reported by `file`. The approved
research run can inspect the PDFs with a PDF extractor when available.

## Search Command Used

```sh
rg --files -g '*.pdf' -g '*.PDF' -g '!node_modules/**' -g '!dist/**' -g '!build/**'
```

## Direct CyberAlchemy PDF

| Path | Pages | Initial Role |
| --- | ---: | --- |
| `cyberAlchemy/agentic-system-ontology-synthesis.pdf` | 8 | Direct CyberAlchemy explanation artifact; compare with the matching HTML for structure, claims, and printable-story choices. |

## Arcanum PDF/Printable Artifacts

| Path | Pages | Initial Role |
| --- | ---: | --- |
| `arcanum/development/user-guide/ARCANUM-DEVELOPMENT-USAGE-GUIDE.print.pdf` | 9 | Printable guide pattern; useful for long-form onboarding and download-friendly site assets. |
| `arcanum/docs/research/dcb-vs-multi-aggregate-append.pdf` | 5 | Research comparison / technical appendix pattern; useful for proof pages, not front-page copy. |

## Adjacent Product or System PDFs

| Path | Pages | Initial Role |
| --- | ---: | --- |
| `validation/poker-team/poker_team_plan.pdf` | 5 | Adjacent plan PDF; sample for concise plan narrative only if public-safe. |
| `projects/zrig/Z-RIG-TURBO-V5.5.3-SPECIFICATION.pdf` | 139 | Large private specification; do not mine for public wording without explicit boundary review. Use only as evidence that long technical packets need compression rules. |
| `projects/goldenquill/docs/features/goldenquill-promotion-governance/team-review/open-questions-and-blockers.pdf` | 4 | Open-questions packet pattern; useful for "what remains open" site sections. |
| `projects/goldenquill/docs/features/goldenquill-promotion-governance/team-review/whole-system-architecture-design.pdf` | 5 | Architecture packet pattern; useful for system-overview page structure. |

## Agent Instructions

PDFs should be classified as:

- `content-source`: contains CyberAlchemy-specific claims or language.
- `printable-guide`: shows a reader-friendly downloadable format.
- `technical-appendix`: supports proof or architecture pages.
- `case-packet`: demonstrates product or governance explanation structure.
- `private-compression-sample`: useful only for learning how to compress dense internal material.

Any claim lifted from a PDF needs an evidence anchor outside the PDF unless the
PDF is itself the authoritative source for that claim.
