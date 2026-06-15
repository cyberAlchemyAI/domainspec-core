# s6 — Architecture Graph (x-ray)

- Capability: `invoke` (design) · technique `x_ray` · role: `structure-mapper`
- Receipt: native-stage · Status: `pass`
- Source: subagent `structure-mapper` (Explore), reconciled by parent against the source doc.

## Nodes (typed by what they MAY own)

| id | owner | type | may own | must NOT own | verification |
|----|-------|------|---------|--------------|--------------|
| **N1 Library** | entity-home (TBD) | public-benefit-collection | accessions, DNA vouchers, host cultures, accession DB, backup/redundancy, public-access interface, accession governance | MycoSymbiotics IP/formulas, FIT Farms revenue, co-op member-only benefit | unverified (depends on entity-home) |
| **N2 PA capacity** | Padilla-Brown / MycoSymbiotics / .coop / MycoFest | cooperative + private-IP | cultivation protocols, grower education, MycoFest platform, community relationships | core accessions (licensed user only), library governance | verified (existing op) |
| **N3 Field** | Epp Schmidt | private-IP (services/protocols) | sentinel-plot data, soil/mycorrhizal datasets, field protocols, agroforestry evidence | core accessions, library governance | verified (expertise) |
| **N4 Houston** | Balan / University of Houston | university-research | publications, student projects, comparative/bioprocess protocols, sponsored-research IP | accessions (MTA-access only), library governance | **unverified — written structure/MTA required (O2)** |
| **N5 Funding-OS** | Inklovich / FIT Farms / Golden Quill / Tilth | funding-OS-**authority** | funder relationships, grant matching, proposal archive, partner memory, routing, QC | **any public-benefit asset; the commercial brand inside the public lane** | verified (operational role) |

## Asset classes → owner + lock + boundary

| asset | owner | lock | boundary |
|-------|-------|------|----------|
| sequence-vouchered accessions | N1 | mission-locked | O1, O4 |
| DNA vouchers | N1 | mission-locked | O1, O4, O5 |
| host cultures | N1 | mission-locked | O4 |
| accession governance policy | N1 | mission-locked (public) | O4, O5 |
| backup/redundancy DB | N1 | mission-locked | O4 |
| public-access/education interface | N1 | mission-locked | O4, O6 |
| field protocols + soil/mycorrhizal data | N3 | licensed to N1 via service agreement | O3, O4 |
| cultivation/grower education | N2 | private/licensed | O4 |
| MycoFest platform | N2 | private/licensed | O4, O6 |
| bioprocess/lab methods, comparative protocols | N4 | university-research, MTA | O3, O5 |
| donor relationships, funder memory, proposal archive | N5 | **authority, not owned** | O5, O6 |

## Asks → node + asset + entity-home + go/no-go owner

| ask | node | builds | entity-home | go/no-go owner | amount |
|-----|------|--------|-------------|----------------|--------|
| A1 Bridge + governance seed | N1 | governance policy, board, verified-partner language, top-20 queue | entity-home (TBD) | N5 routes; legal vets | $75K–$250K |
| A2 Public living-library infra | N1 | accessions, vouchers, cultures, backup, access interface | same as A1 | N1 curator; N5 vendor mgmt | $300K–$900K |
| A3 Field evidence network | N3 | protocols, sentinel data | service agreement w/ N1 | N3; N5 (SARE/NRCS/NIFA) | $50K–$300K |
| A4 Houston Research Node pilot | N4 | bioprocess/comparative protocols, student projects | MTA + UH sponsored-research acct | N4 director; N5 routing | $100K–$750K |
| A5 MycoFest public-science + donor | N2 | accession desk, donor conversion, education | co-hosted w/ N1; .coop runs event | N2; N5 sponsor match | $25K–$150K |

## Edges — minimum spine + three-connector recomposition

- **Minimum spine = N1 alone** + {A1 Bridge, A2 Infrastructure} + entity-home.
- Every extension lane (N2, N3, N4 + Lanes 4/6/7) attaches to the spine through exactly **three connectors**: (C1) shared accession/verification standard, (C2) declared asset-ownership lane, (C3) entity-home relationship (same home / fiscal-sponsored sub-lane / licensed-services / MTA). A lane that cannot declare all three does **not** recompose → flag.

## Authority vs ownership split (F1 resolved)

N5 (Funding-OS) holds **coordination authority** — routing, QC, partner memory, funder comms — and **must never hold title** to N1 public assets, must never direct the N1 board, and must never bind a partner (O2) or pitch funders (O6) without N1 owner sign-off. If FIT Farms is involved operationally, the relationship is a **written service agreement** ("provides routing/QC services; does not own accessions; defers to N1 board on asset disposition"), never ownership.
