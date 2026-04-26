# MARS Reference Ledger

Purpose: operational registry of references used as authority in protocols, analysis, and claim adjudication.

## Ledger

| Reference ID | Citation (Short) | Authority Level | Usage Scope | Source ID | Pin | Status |
|---|---|---|---|---|---|---|
| REF-WOHLIN-2012 | Wohlin et al. Experimentation in Software Engineering | primary | methodology | PAPER-WOHLIN-2012 | book:springer-2012 | operationalized |
| REF-BASILI-1996 | Basili GQM | primary | methodology | PAPER-BASILI-GQM-1996 | paper:gqm-1996-basili | operationalized |
| REF-RUNESON-2009 | Runeson and Host case-study triangulation | supporting | analysis | PAPER-RUNESON-HOST-2009 | book:guidelines-case-study-2009 | operationalized |
| REF-KITCHENHAM-2002 | Kitchenham empirical SE guidelines | supporting | analysis | PAPER-KITCHENHAM-2002 | paper:kitchenham-2002-guidelines | operationalized |

## Authority Levels

- primary: required to justify protocol criteria or claim update decisions
- supporting: used for triangulation or interpretive support
- fallback: optional backup when primary sources are unavailable

## Status Values

- operationalized: source ID + pin + inventory linkage complete
- pending normalization: citation exists but not yet source-cataloged/pinned
- waived: accepted temporary exception with rationale
