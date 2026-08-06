# Subagent Receipt: Whisper Explanation Designer

- Agent: `Shannon, Claude`
- Runtime agent ID: `/root/rich_explanation_whisper`
- Role: `whisper-explanation-designer`
- Dispatch: `20260804T151133Z-rich-consultation-explanations`
- Step: `p2-whisper-language-design`
- Capability: `whisper`
- Status: pass with claim ceiling
- Observer: not run; no invocation envelope supplied
- Blocker carried forward: exact current posture must come from verified current bytes
- Residue: glossary contract and payload, latency, and comprehension budgets are unmeasured

## Composition Contract

1. Direct answer.
2. Verified current posture.
3. Process as input, bounded transformation, immediate consequence, and later limit.
4. Exactly one scenario labeled `Illustrative` or `Source-derived`.
5. At most one analogy, immediately followed by `Where this stops matching:`.
6. Two to five plain-first glossary entries actually used by the answer.
7. Boundary statement and source handles.

Missing current-posture evidence fails closed: say that available support does not establish the claim, omit it, or route for verification. Never turn `proposed`, `partial`, `deferred`, or `unknown` into current capability.

## Profiles

| Profile | Contract |
| --- | --- |
| `brief` | One or two sentence answer, one current-state sentence, two to four process steps, optional scenario/analogy, two glossary terms, compact boundary and handles. |
| `guided` | Default: direct answer, explicit current/proposed distinction, three to six process steps, one scenario, one bounded analogy, two to five terms, boundary and handles. |
| `deep` | Component-by-component posture, complete retell chain, one scenario, one bounded analogy, two to five terms, limits, open gaps, and field-level handles. |

## Audition Decision

The guided profile wins for the question “How does the Augmentor reasoning engine work?” It gives a direct mental model and a retellable process without hiding the whole-engine gap. Brief compresses the ownership lifecycle too far; deep is useful for follow-up but introduces more terms than most users initially need.

Winning language direction:

> The accurate answer is that Augmentor does not currently have one proven, all-purpose reasoning engine. Today, its consultation service can find reviewed evidence and tell an answering agent whether to answer, qualify, clarify, or abstain. The ontology also describes a future bounded reasoning flow, but the adapter and action path are still deferred.

Illustrative scenario and analogy must follow only when they clarify the requested depth. The analogy may explain one relationship, never establish implementation, intelligence, authority, or completeness.

## Handoff

Use this as candidate composition guidance. Current-state handles come from the mapper. The API should return explanation support, not final prose.
