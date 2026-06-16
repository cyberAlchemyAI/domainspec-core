# TARGET UNDER REVIEW — assistant inline answer

**Source:** assistant chat reply to "what are the differences between /dispatch-spec and /domainspec-subagents-strategy" (2026-06-16).
**Verify against (literal artifacts):**
- `.claude/skills/dispatch-spec/SKILL.md`
- `.claude/skills/domainspec-subagents-strategy/SKILL.md`
- `.claude/skills/review/SKILL.md`, `.claude/skills/research/SKILL.md`, `.claude/skills/experiment/SKILL.md`
- `formulae/dispatch-spec/scripts/validate-dispatch.py` (existence + "25 rules" claim)

---

## The one-line difference
- **dispatch-spec** validates a route over sigils/spells — "is this chain of capabilities explicit enough to run safely?"
- **domainspec-subagents-strategy** governs a subagent dispatch — "should we spawn parallel AI agents, and is the fan-out honestly tensioned?"

One is about composing tools; the other is about spawning agents.

## Side by side

| | dispatch-spec | domainspec-subagents-strategy |
|---|---|---|
| Tier / kind | Formulae — a deterministic validator (SKILL L11-29) | A router — routes a dispatch to a type skill (SKILL L1-4) |
| What it operates on | A dispatch.json describing a route over named sigils/spells (craft → research → whisper → x-ray) | A dispatch sheet describing a fan-out of AI subagents with roles |
| Core question | "Is this composition schema-valid, gated, observable, handoff-ready?" | "Is this dispatch genuinely tensioned, and which type owns it?" |
| Does it execute? | No — it only validates shape; returns pass/flag/block (L31-32) | No — it routes; the type skill (research/review/experiment) owns judgment |
| Trigger | "I want to chain sigils by name into a repeatable route" (Use When) | One of: synthesis / context-protection / isolation / parallelism (P1) (L10) |
| Human gate | None inherent — it's a linter | Yes — one mandatory human confirm before agents run (L17) |
| Signature concept | capability_ref, pattern, handoff, boundary_evidence, subagent_strategy/lifecycle | dispatch_type, pairwise tension (P5), final_approver, exit_reason, the four-step lifecycle |
| Quality mechanism | 25 numbered validation rules + a Python validator script | The check-tension gate: two independent agents verify the sheet is real before the human sees it |
| Output | Dispatch Spec Result + "Next route" pointer | Routes by dispatch_type table (research/review/experiment LIVE) |

## The mental model that makes it click
Think of it as two layers of the same pipeline:

```
dispatch-spec  →  governs the PIPELINE   (craft → research → whisper → x-ray)
                  "are the tool handoffs explicit?"

domainspec-    →  governs ONE STAGE       (the research fan-out: 5 agents
subagents-        inside that pipeline     sweeping the user-guide in parallel)
strategy          "is the fan-out honestly tensioned, did the human approve?"
```

Notice the connection point: dispatch-spec actually has a subagent_strategy block (L98-120). When a route's step needs parallel agents, dispatch-spec recommends the subagent strategy but explicitly does not execute it — it hands off. That handoff is precisely where domainspec-subagents-strategy takes over and runs its gated lifecycle.

## Concretely, for the manual idea
- The whole chain (craft space → research → whisper → x-ray) is a dispatch-spec route — validate its shape once.
- The research stage inside that chain — "spawn agents to gather all Arcanum knowledge from the user-guide and synthesize it" — is a domainspec-subagents-strategy dispatch_type: research, because it hits the synthesis trigger (many sources to combine) and therefore needs tension design + the human gate.

They don't compete — dispatch-spec is the outer contract, domainspec-subagents-strategy is the governed engine for one step in it.
