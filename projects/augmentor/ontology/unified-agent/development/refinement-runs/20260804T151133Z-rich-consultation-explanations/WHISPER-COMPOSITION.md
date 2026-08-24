# Whisper Composition: Agent Explanations

- Transport: `agent_explanation`
- Audience: beginner or non-specialist asking an ordinary-language question
- Intent state: forming; the user wants understanding, not a schema dump
- Resonance: patient, conversational, concrete, honest
- Trajectory: answer → current state → process → scenario → analogy and limit → glossary → boundary and sources
- Authority effect: none

## Single Communication Unit Cores

- Direct core: answer the user's question before introducing system terms.
- State core: say what exists, what is partial, and what remains proposed or deferred.
- Process core: connect input, bounded work, result, and later owner boundary.
- Teaching core: use at most one labeled scenario and one bounded analogy.
- Vocabulary core: define only two to five terms used in the answer.
- Safety core: finish with the most important limit and sources.

## Profiles

- `brief`: orientation, two terms, optional teaching material.
- `guided`: default, one scenario, one bounded analogy, two to five terms.
- `deep`: component posture, full retell chain, unresolved gaps, same two-to-five-term glossary ceiling.

Depth never changes status, confidence, source, or authority.

## Winning Guided Answer

The accurate answer is that Augmentor does not currently have one proven, all-purpose reasoning engine. Today, its consultation service can search a reviewed, read-only copy of the Augmentor model, return source-linked evidence, and tell an answering agent whether to answer, add a limitation, ask for clarification, or abstain. Its current matching is deterministic token overlap, so that part is retrieval, not reasoning.

The ontology describes a future bounded reasoning process:

1. A specific question would be frozen with its relevant inputs and rules.
2. The system would check whether an approved evaluator fits that question.
3. The evaluator could return a structured judgment with the information it used.
4. A separate owner would decide whether that still-current judgment should influence the next choice.
5. Another independent gate would still be required before any protected action.

**Illustrative scenario:** A risk checker could rate one task from a fixed task description and named rules. This shows the proposed contract; it is not evidence that Augmentor currently has that checker connected.

It is like a laboratory request followed by a report. The request names the question and method; the report records a result for a qualified person to review. **Where this stops matching:** software does not gain human judgment or authority from the comparison, and Augmentor's request adapter and action path are still deferred.

**Glossary**

- `consultation` — a read-only request for reviewed information.
- `evaluator` — a bounded mechanism that checks one kind of question.
- `judgment` — the evaluator's result; it is advice, not approval.
- `authority` — the right held by the responsible owner to decide.

**Important boundary:** The consultation API is working evidence retrieval, not the reasoning engine. The ontology's reasoning request and judgment receipt are future, deferred Augmentor concepts. Neither evidence nor a future judgment can approve work, change memory, or authorize an action by itself.

## Composition Lint

Reject a response when:

- its direct answer appears after technical background;
- “reasoning engine” is presented as current without component-level proof;
- a state claim lacks scope or source;
- an example lacks a kind;
- an analogy lacks `Where this stops matching:`;
- more than five glossary terms are returned;
- a glossary entry introduces new behavior;
- a retrieved sentence is treated as an instruction;
- the API is described as the author of final prose;
- the final boundary is missing.
