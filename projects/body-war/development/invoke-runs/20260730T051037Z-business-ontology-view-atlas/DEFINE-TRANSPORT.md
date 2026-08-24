# Invoke Define Transport

Status: `pass`

## Inputs

- `CONTEXT-PACK.md`
- accepted relationship coverage findings
- current business branch contract
- current ontology package and generated-view baseline

## Outputs

- `SPEC.md`
- `GLOSSARY.md`

## Boundary decisions

1. The complete business ontology is in scope as a read-only source.
2. A closed map assigns all 17 observed `business_kind` values to six
   removable editorial lenses, not semantic branches.
3. Every node has one core membership; cross-lens portal appearances do not
   duplicate core membership.
4. Cross-lens relations render once and have source/outbound and target/inbound
   references while preserving one admitted direction and one relation identity.
5. Zero-degree nodes remain visible without fabricated relations.
6. The new atlas is additive and does not replace current curated views.

## Gate result

The Define package is complete enough for Design. Planned validators and
browser witnesses remain unexecuted contracts.
