# Cohesive Modular Arcanum — Candidate Glossary

Status: private Refine candidate; not canonical vocabulary.

| Term | Candidate definition | Non-role |
|---|---|---|
| Arcanum Build Protocol (ABP) | The shared, implementation-agnostic vocabulary and validation rules for composing owner-bound capability transitions. | Not a runner, lifecycle owner, or registry. |
| Capability module | One capability with a bounded semantic responsibility, owned inputs/outputs, and explicit effects. | Not an arbitrary code package or agent role. |
| Sovereign effect owner | The sole capability permitted to cause one named class of state or lifecycle effect. | Need not be the validator, router, or evidence store. |
| Owner-Bound Transition Contract (OBTC) | A typed handoff record naming source state, producer, consumer, preconditions, receipt, authority effect, freshness/replay binding, failure result, and legal successor. | Does not execute the transition. |
| Gate | A first-knowable condition whose non-pass result forbids named downstream effects. | Not a vague readiness label. |
| Receipt | Owner-attributed evidence that one bounded operation or validation occurred with a stated result and ceiling. | Not authority outside its declared effect. |
| Projection | A derived read or route view over owner state. | Never replaces its source or grants promotion. |
| Compatibility facade | A legacy or user-facing route that delegates to one canonical owner without retaining a second state machine. | Not a second reducer. |
| Conformance witness | A deterministic trace proving that a declared protocol fixture obeys transition and stop rules. | Fixture proof is not product E2E proof. |
| Material-producer port | An explicit contract slot for the owner that prepares one exact mutation package and receipt. | The port does not identify or impersonate the owner. |
| Registry-release port | An explicit contract slot for the owner that releases a capability into a registry. | Lifecycle judgment or runtime success cannot fill it implicitly. |
| Synchronized result | Task Session's derived overall result after required closeout owner evidence joins or a validated no-op is proven. | Execution-terminal success alone is insufficient. |

