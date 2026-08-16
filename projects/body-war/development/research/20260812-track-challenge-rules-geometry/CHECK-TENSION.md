# Check-Tension Gate Receipt

## Exact Binding

- Dispatch sheet: `DISPATCH-SHEET.json`
- Schema: `0.8.0`
- Sheet SHA-256: `a4f386bcdbcdbdb3cebeeb4b6c5820346e556a25066f2fff02a8bf83e5ab10d1`
- Sheet form validation: `PASS`
- Capability-bound route validation: `PASS`
- Material strategy projection SHA-256: `12095fa9368c230ad426daeb93c83c4ed22431291df5fd197b1524b985902721`
- Projection equivalence: `same`

## Independent Verdicts

| Role | Infrastructure helper | Bound digest verified | Partition | Verdict |
|---|---|---:|---:|---:|
| Checker | `/root/tension_check` | `PASS` | `PASS` | `PASS` |
| Reviewer | `/root/tension_review` | `PASS` | `PASS` | `PASS` |

The reviewer performed an independent phase and did not inspect or compare the
checker return. Neither helper spawned a research agent or mutated repository
files.

## Gate Result

`PASS + PASS`. The exact material strategy is confirmation-ready. This receipt
does not register the dispatch, authorize research execution, adopt game rules,
or change product authority.
