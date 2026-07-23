# Template Selection Record

| Stage | Selected template/profile | Eligibility evidence | Alternatives rejected | Status |
| --- | --- | --- | --- | --- |
| Define | `arcanum/spells/invoke/templates/spell/spell.md` | Target is an existing spell revision; identity, triggers, shared state, gates, and Spellcraft handoff are required. | Generic module spec would misstate lifecycle ownership. | candidate template retained |
| Design | `arcanum/spells/invoke/templates/architecture/architecture.md` | Source contracts, six design views, interfaces, decisions, and risks are material. | DomainSpec aspect-doc architecture is optimized for Concept Registry modules, not spell runtime evidence. | candidate template retained |
| Plan | `arcanum/spells/invoke/templates/implementation-layering.md` | Plan mode requires L0-L3 decision boundaries. | No alternative. | implemented companion |
| Plan | `arcanum/spells/invoke/templates/work-pack.md` | High complexity and more than five tasks require a split executable work pack. | Single-file mode fails complexity rules. | implemented companion |
| Plan | `arcanum/spells/invoke/templates/domainspec-spec/execution-pack.md` | High-complexity wave scheduling is required even though the target is a spell. Only the planning structure is reused. | An ad hoc wave document would duplicate the existing Invoke contract. | implemented companion |

No template tie remained after applying target type and complexity. No template is promoted by this selection.
