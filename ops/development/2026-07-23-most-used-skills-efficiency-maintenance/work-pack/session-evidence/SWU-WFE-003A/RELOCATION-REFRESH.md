# SWU-WFE-003A Runtime-Support Relocation Refresh

The SWU-WFE-003A validator behavior and bytes are unchanged. Decision Gate
Option 1 moved runtime-required support to generator-visible locations:

| Prior path | Current path | SHA-256 |
| --- | --- | --- |
| `arcanum/spells/invoke/development/material_package_validator.py` | `arcanum/spells/invoke/scripts/material_package_validator.py` | `5012c5767f6dc0e76a0e34a63f4b65342883c7969b52e9b86e910c4c63ee1426` |
| `arcanum/spells/invoke/development/schemas/material-package.schema.json` | `arcanum/spells/invoke/schemas/material-package.schema.json` | `f52810a2b08507f487cfc63e7b8619761a2803613098e6eb7cc46911288dc628` |
| `arcanum/spells/invoke/development/schemas/material-package-receipt.schema.json` | `arcanum/spells/invoke/schemas/material-package-receipt.schema.json` | `2c4ef7c0529f419278a3af530783383d05ccf8e144a40e895f26c2c2d6b77b6b` |

Fixtures and runners remain under `development/`. The current 19-case focused
suite and full Invoke harness pass. The original closure receipt remains
historical evidence of the 13-case producer boundary; this refresh is its
location overlay, not a rewritten execution claim.
