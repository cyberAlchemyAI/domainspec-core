# States

## Run state

| State | Entry condition | Legal next states |
| --- | --- | --- |
| `unfrozen` | run created | `package-gate-pass`, `package-gate-blocked` |
| `package-gate-pass` | exact artifact/source correspondence proven | `fixture-frozen` |
| `fixture-frozen` | all constants and manifests independently frozen | `built` |
| `built` | isolated payload written, manifest not yet admitted | `verified`, `verification-failed` |
| `verified` | complete independent readback passes | `observed` |
| `observed` | required positive and negative controls complete | `closed` |
| `package-gate-blocked` | provenance/toolchain gate fails | terminal |
| `verification-failed` | any exact oracle fails | `quarantined` |
| `quarantined` | external receipt recorded | terminal for that generation |
| `closed` | bounded closeout recorded | terminal |

No state transition mutates canonical YAML. A new sibling run starts at
`unfrozen`; it does not resume a blocked or quarantined generation.
