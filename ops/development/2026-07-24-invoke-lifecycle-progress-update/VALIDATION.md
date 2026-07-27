# Validation

Date: 2026-07-24

## Results

| Check | Result |
| --- | --- |
| execution dispatch JSON parse | pass |
| SWU manifest JSON parse | pass |
| Dispatch Spec schema and governance validation | pass; zero blocks, zero flags |
| local Markdown links | pass; zero missing |
| work-pack/manifest SWU identity parity | pass; eleven versus eleven |
| task contract inventory | pass; ten task files |
| Define required outcomes | pass; ILP-R01 through ILP-R10 |
| design view coverage | pass; six of six |
| same-epoch supersession invariant | pass in design/plan coverage |
| Distill plan validation | pass |
| canonical public source mutation | none |
| generated runtime mutation | none |

## Commands

```text
python3 -m json.tool <package>/execution.dispatch.json
python3 -m json.tool <package>/work-pack/swu-manifest.json
python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py <package>/execution.dispatch.json
```

The link, SWU parity, task inventory, trailing-whitespace, and scoped-path
checks were run read-only against the package.

## Claim boundary

This validates the Invoke authoring package and dispatch shape. It does not
validate the unimplemented protocol, close `ILP-G01`, establish mutation
readiness, promote a capability, or prove the planned live topology.

