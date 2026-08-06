# Closure Gates

Status: `pass`

| Gate | Criterion | Evidence | Status |
| --- | --- | --- | --- |
| G1 | Exact corpus identified and reproducible | `sources/source-record.md` | `pass` |
| G2 | Human prompts and assistant prose distinguished | `sources/source-map.md` | `pass` |
| G3 | Source-kind labels used consistently | Claim and related-work tracks | `pass` |
| G4 | Technical notation explained before use | `NOTATION.md` | `pass` |
| G5 | Local glossary and definitions include misuse warnings | `GLOSSARY.md`, `DEFINITIONS.md` | `pass` |
| G6 | Related work closes named residue only | Related-work crosswalk | `pass` |
| G7 | Legal, health, and technical overclaims blocked or qualified | Adjudication tracks | `pass` |
| G8 | Borrow, analogy-only, block, and future-work decisions explicit | Bridge decisions | `pass` |
| G9 | All helper work reconciled | Helper closeout ledger | `pass` |
| G10 | Open residue has owners/routes | `residue/open-residue.md` | `pass` |
| G11 | Required artifacts and relative links validate | `VALIDATION.md` | `pass` |
| G12 | No canonical promotion or implementation claim | Repository diff and boundary scan | `pass` |

## Fail-Closed Rule

An absent source, unreviewed helper lane, broken relative link, unlabeled claim,
or promotion-boundary violation blocks closure. Open empirical or legal work does
not block local research closure when it is explicitly recorded as residue.
