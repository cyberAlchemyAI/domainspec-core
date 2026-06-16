# s1 — Context Builder Evidence Baseline

- Capability: `context-builder` · Mode: `standard`
- Receipt kind: native-stage · Status: `pass`
- Source (read-only): `projects/alpha-grant/decentralized-living-library-summary.md`

## Coverage map (architecture components present in source)

| Component | Source section | Evidence quality |
|-----------|---------------|------------------|
| Network thesis (distributed public-benefit infra, not a single farm/brand) | Executive Summary | high — explicit |
| 4 capacity nodes (PA culture / field-methods / Houston Research Node / funding-OS) | Executive Summary | high — named owners |
| Package contents (00–08 kit) | What The Package Contains | medium — inventory only |
| 7 project lanes w/ first asks | Core Project Lanes | high — amounts + needs |
| 5 grant-facing asks (amount/route/buys) | Five Grant-Facing Asks | high — table |
| Funding DB (368 rows, top-50 queue, priority routes) | Funding Database | high |
| Entity/partner routing rules | Entity And Partner Routing | high — lane-clean rules |
| Non-negotiable boundaries | Non-Negotiable Boundaries | high — hard limits |
| 90-day execution path | 90-Day Execution Path | high — 10 steps |
| Risks + controls | Main Risks And Controls | high — table |
| Recommended immediate move (internal decision package) | Recommended Immediate Move | high |

## Obligation-linked excerpts (constraints that any refined design must honor)

- O1 — KU/INVAM: "Do not imply KU/INVAM partnership, strain access, MTA, services, or name-use authorization." AMF lane "must remain concept-only unless KU/INVAM authorization exists."
- O2 — Unverified partners: "Do not claim any partner is committed without written confirmation." Josh/FIT Farms "partner commitments must not be represented before written confirmation."
- O3 — Balan framing: "Do not frame Dr. Balan or the University of Houston as an automation module; frame them as the Houston Research Node." Lane 5 correction: "not an automation-first lane."
- O4 — Public/private separation: "Do not commingle public collection assets with private MycoSymbiotics, FIT Farms, or co-op revenue assets." Routing: public assets need a "mission-locked home"; MycoSymbiotics IP stays "private or licensed-services lane."
- O5 — Claims review: no "health, ecological miracle, endorsement, or partner-status claims without scientific, legal, and relationship review."
- O6 — Funder exposure: "Do not send a broad spreadsheet to funders before selecting a clean ask, entity route, owner, and go/no-go status." Lead with top-50 + five asks.

## Coverage gaps (no external research yet; local-first)

- G1 — Entity-home decision is named but unresolved (fiscal sponsor / nonprofit / co-op / FIT Farms service lane). Architectural fork, not yet decided.
- G2 — Authority/ownership per lane is implied by routing rules but never drawn as a single graph (which node owns which asset/ask/data/IP).
- G3 — Dependency ordering among the 7 lanes / 5 asks is not stated (which asks unlock which; what the minimum viable spine is).
- G4 — Verification status is a control ("add verification status to every partner and opportunity") but no current per-partner status is recorded in the summary.

## Handoff frame for downstream stages

The architecture is a **node × lane × ask × entity-home** structure bound by six
hard obligations (O1–O6). The refinement must (a) make ownership/authority
explicit, (b) resolve or ledger the public-benefit vs private/commercial tension,
(c) turn the entity-home gap (G1) into an approvable decision, and (d) preserve
O1–O6 as gates. Gaps G1–G4 are the live uncertainty surface.
