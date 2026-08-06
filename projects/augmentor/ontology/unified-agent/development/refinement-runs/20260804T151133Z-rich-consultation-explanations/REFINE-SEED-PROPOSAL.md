# Refine Seed Proposal: Rich Consultation Explanations

- Target: `projects/augmentor/ontology/unified-agent` and its read-only consumer in `/home/vrondelli/projects/workspace-resonant/2.0.0-alpha`
- Run ID: `20260804T151133Z-rich-consultation-explanations`
- Seed needed: yes
- Preset: deep
- Research mode: `research-if-gap-appears`; local evidence first; external research requires a separate explicit confirmation
- Mutation scope: this refinement-run folder and required append-only dispatch ledger rows only
- Product mutation: forbidden
- Deployment: forbidden
- Authority or ontology promotion: forbidden

## Desired Outcome

Produce an implementation-ready, non-executed plan that lets an answering agent explain Augmentor accurately and warmly. Consultation results should support a direct answer, an honest current-state description, a step-by-step mechanism, one clearly marked illustrative scenario, one bounded analogy with its limitation, a small glossary of only the terms actually used, and source/boundary context.

The consultation API remains a read-only evidence service. It supplies verified explanation support; the answering agent owns prose composition. Neither layer may invent runtime capability, authority, memory state, or reasoning behavior.

## Current Tension

The current system is safe but terse. Existing beginner material already contains useful plain-language fields, yet the consumer projection and API appear to expose only a smaller subset. The refinement must improve explanatory depth without leaking private records, inflating current-state claims, turning examples into evidence, or making payloads unbounded.

## Candidate Contract

The leading candidate is an explanation pack beside each retrieved record:

- `plainMeaning`
- `currentState.posture` and `currentState.explanation`
- `process`
- `illustrativeExample.text` and `illustrativeExample.kind`
- `analogy.text` and `analogy.limitation`
- `boundary`
- `glossaryRefs`
- `keywords`
- field-level provenance/source handles

A glossary sidecar defines plain terms first and formal names only when needed. Each response returns only the two to five terms it actually uses.

## Response Sequence

1. Direct answer.
2. What exists today.
3. How the process moves.
4. One illustrative real-life scenario, explicitly marked as illustrative.
5. One analogy, followed immediately by where it stops matching.
6. A two-to-five-term glossary.
7. Important boundary and source handles.

Three profiles must be designed: `brief`, `guided`, and `deep`. They vary depth, not truth or authority.

## Alternatives To Test

- A: enrich every projected record only.
- B: use a glossary sidecar plus a bounded explanation pack. This is the leading candidate.
- C: make the API generate final prose. This should be rejected unless evidence shows the agent-owned composition boundary is unworkable.

## Representative Questions

- How does the Augmentor reasoning engine work?
- What happens when Augmentor does not know enough?
- How does Augmentor choose a route?
- How can Augmentor memory evolve without becoming too heavy?
- Who decides whether a proposed meaning or action is accepted?

## Done Criteria

- Every current-state statement is verified against current source bytes.
- No unexplained jargon appears in the response-support contract or examples.
- Every example is labeled `illustrative` or `source-derived`.
- Every analogy includes a limitation.
- Glossary entries are evidence-linked and non-authoritative.
- Private ontology fields remain excluded from the neutral projection.
- The work pack names exact source files, schemas, tests, task order, and stop conditions.
- Payload and latency overhead have bounded measurement targets, not unverified success claims.

## Confirmed Delegation

The operator explicitly confirmed the deep Refine strategy with three proposed subagents: a current-state mapper, a Whisper explanation designer, and a contract/safety critic. All are read-only. The parent writes and validates the target-local artifacts.
