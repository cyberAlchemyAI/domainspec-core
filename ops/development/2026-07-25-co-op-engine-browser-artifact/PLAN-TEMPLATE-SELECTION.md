# Plan Template and Profile Selection

## Inventory Evidence

| Template | SHA-256 | Eligibility | Selection |
| --- | --- | --- | --- |
| `arcanum/spells/invoke/templates/implementation-layering.md` | `73a2765a32d5cc937818274dd8eb4e433e92aeb28fe617340ef4b27781d3f7c3` | mandatory for every Plan | selected |
| `arcanum/spells/invoke/templates/work-pack.md` | `dda86f74da4563af2e85aa32dcc6a4d665491c472bbcb4697b9bc97c4586d0a5` | mandatory for every Plan | selected |
| `arcanum/spells/invoke/templates/domainspec-spec/execution-pack.md` | `1f6c9deeb72caa72271bc32493bc0da84a9bd728180c01f6bc57265e34b8e585` | medium complexity requires wave choreography | selected |

The deprecated Module Formulae execution pack is ineligible because the active
Invoke contract names the DomainSpec execution pack.

## Result

Use split mode:

- global `IMPLEMENTATION-LAYERING.md`;
- canonical `WORK-PACK.md`;
- `EXECUTION-PACK.md`;
- useful task and wave contracts under `work-pack/`;
- one machine-readable SWU manifest and one closeout synchronization contract.

No template tie or missing companion blocks Plan.
