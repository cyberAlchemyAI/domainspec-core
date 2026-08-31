# DomainSpec v2 model

This candidate example uses the CyberAlchemy Governance language without
claiming a direct translation from business meaning to implementation type.

| Governance meaning | DomainSpec v2 realization in this example | Rust realization |
| --- | --- | --- |
| Governance Program | `DS-D1.1 Entity` — stable program ID and version | `GovernanceProgram` |
| Governance Request | `DS-D1.2 Value Object` — immutable proposed consequence | `GovernanceRequest` |
| Governance Fact | `DS-D1.2 Value Object` — proposition, scope, source, verifier, and value | `GovernanceFact` |
| Governance Fact Set | `DS-D1.2 Value Object` — finite immutable evaluation input | `GovernanceFactSet` |
| Governance Verdict | `DS-D1.3 Enum` — `allow`, `deny`, `abstain`, `error` | `GovernanceVerdict` |
| Evaluate Governance | `DS-D1.6 Calculation` — pure deterministic value return | `evaluate` |

`GovernanceVerdict` is not modeled as `DS-D1.7 Rule`: a DomainSpec Rule returns
a Boolean, while this kernel deliberately returns four distinct outcomes.
`evaluate` is not an `Operation` because it changes no state.

The Program refers to exact rule, Constitution, binding, selector, and authority
requirements. Those references are synthetic test data. They are not adoption,
authority, an active Constitution, or an enforcement binding in CyberAlchemy.

