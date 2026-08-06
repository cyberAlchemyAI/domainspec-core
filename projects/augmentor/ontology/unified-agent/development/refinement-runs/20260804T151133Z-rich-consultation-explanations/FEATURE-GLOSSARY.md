# Feature Glossary: Rich Consultation Explanations

This glossary explains terms used by the feature plan. It is not a source of behavior or canonical definitions. Each future API response returns only two to five terms actually used by that answer.

| Term | Plain meaning in this feature | Formal name, if useful | Why it matters | Evidence |
| --- | --- | --- | --- | --- |
| Consultation | A read-only request for reviewed information about Augmentor. | Consultation API | It returns evidence; it does not answer, decide, or write. | consumer API reference, lines 3-20 |
| Evidence | Information returned with source and boundary context to support a claim. | Evidence statement | The answering agent may use it only under the answer policy. | consumer service, `statementFor`; answer policy |
| Source handle | A short opaque code that points back to an approved source without exposing its private path or ID. | `sourceHandle` | It supports citation and provenance while preserving the private boundary. | projection compiler and schemas |
| Neutral projection | A consumer-safe copy containing only allowlisted fields and opaque references. | Consumer projection | The runtime never reads the private ontology directly. | compiler allowlist; API reference lines 22-34 |
| Explanation support | Structured material that helps an agent explain selected evidence. | `ExplanationSupportBundle` | It adds depth without letting the API generate final prose. | this run, `stages/06-design.md` |
| Modeled state | What the reviewed ontology model says about a component's posture, with scope and verification time. | scoped `state` object | It must not be mistaken for proof that a live product feature is deployed. | `profile.json`; reasoning nodes; CR-01 |
| Illustrative scenario | A made-up situation used to show how a contract would behave. | `kind: illustrative` | It is teaching material, not evidence that the scenario happened or is implemented. | beginner corpus; CR-05 |
| Source-derived example | An example whose content is directly bound to an approved source. | `kind: source-derived` | It needs its own source handles and may support a factual claim within its ceiling. | this run, example-kind contract |
| Bounded analogy | A comparison used to explain one relationship and followed by where the comparison stops. | analogy plus `limitation` | It teaches without implying implementation, intelligence, authority, or completeness. | Whisper receipt; CR-05 |
| Answer policy | The rule that says whether an agent may answer, should qualify or clarify, or must abstain. | consultation answer policy | It prevents evidence gaps from becoming confident prose. | consumer answer policy, lines 1-24 |
| Route | An eligible next path for handling a request. | Route decision, when formally modeled | A possible route is not permission to execute it. | beginner ontology and routing Inventory source pointers |
| Authority | The right held by a named owner to make a particular decision. | authority kind/owner in governed sources | Evidence, consultation, a glossary, or a judgment does not create it. | `profile.json`; node boundaries |
| Reasoning request | A future bounded question with fixed inputs, rules, and applicability context. | `ReasoningRequest` | The Augmentor adapter and owners for this flow remain deferred. | `nodes/nodes.json:957-1003` |
| Judgment receipt | A future immutable record of one bounded evaluator result. | `JudgmentReceipt` | A result remains advice; it is not approval or effect permission. | `nodes/nodes.json:1006-1052` |

## Vocabulary Gaps

- The canonical owner of the consumer glossary schema is not yet accepted.
- “Current state” is too broad unless every use names its scope: ontology model, local implementation, deployed service, or production state.
- “Reasoning engine” should be avoided as an unqualified current product label.

## Feature Glossary Result

- Plain-language terms: 14
- Formal concepts: 5 optional mappings
- Cross-scope terms: authority, route, reasoning request, judgment receipt
- Unresolved terms: canonical glossary owner; product-wide meaning of current state
- Validation: duplicate/authority/usage review performed; source links remain file selectors until implementation emits opaque handles
