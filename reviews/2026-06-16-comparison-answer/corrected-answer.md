# dispatch-spec vs domainspec-subagents-strategy — corrected comparison

> Corrected per review `2026-06-16-comparison-answer-review` (findings #1–#7). Changelog at the bottom.

They sound similar but govern different things.

## The one-line difference
- **dispatch-spec** validates a route over sigils/spells — "is this chain of capabilities explicit enough to run safely?"
- **domainspec-subagents-strategy** governs a subagent dispatch — "should we spawn parallel AI agents, and is the fan-out honestly tensioned?"

One is about composing tools; the other is about spawning agents.

## Side by side

| | dispatch-spec | domainspec-subagents-strategy |
|---|---|---|
| Tier / kind | Formulae — a deterministic validator (tier: L11; "Deterministic Validator" section: L56-68) | A router — routes a dispatch to a type skill (L1-4) |
| What it operates on | A dispatch.json describing a route over named sigils/spells (craft → research → whisper → x-ray) | A dispatch sheet describing a fan-out of AI subagents with roles |
| Core question | "Is this composition schema-valid, gated, observable, handoff-ready?" | "Is this dispatch genuinely tensioned, and which type owns it?" |
| Does it execute? | No — it only validates shape; returns pass/flag/block (Output Contract L148; Failure Policy L166-169) | No — it routes; the type skill (research/review/experiment) owns judgment |
| Trigger | "I want to chain sigils by name into a repeatable route" (Use When) | One of: synthesis / context-protection / isolation / parallelism (P1, L10) |
| Human gate | None for invoking the skill — it's a linter¹ | Yes — one mandatory human confirm before agents run (L17) |
| Signature concept | capability_ref, pattern, handoff, boundary_evidence, subagent_strategy/lifecycle | dispatch_type, pairwise tension (P5), final_approver, exit_reason, the four-step lifecycle |
| Quality mechanism | 25 numbered validation rules + a Python validator script | Invokes the check-tension gate — a separate skill it points to: two independent agents verify the sheet before the human sees it |
| Output | Dispatch Spec Result + "Next route" pointer | Routes by dispatch_type table (research/review/experiment LIVE) |

¹ Still a linter, but dispatch-spec *enforces* a human gate on subagent routes: Rule 22 (L93) requires `authorization=requires_user_permission` on any `subagent_strategy` block, so it flags/blocks routes that bypass it.

## How they relate (analogy — stated by neither skill)
The two are **peers under a shared register-dispatch / constitution stack**, not a containing pipeline. Neither SKILL establishes a hierarchy: dispatch-spec "does not decide which sigils should be used" (L31); domainspec-subagents-strategy "defines no field and no type-specific judgment — it routes" (L3).

One way to *picture* the division of labor (a mental model, not something either doc asserts):

```
dispatch-spec   —  validates the SHAPE of a route over capabilities
                   (craft → research → whisper → x-ray): are the handoffs explicit?

domainspec-     —  routes & gates ONE subagent dispatch
subagents-         (e.g. the research fan-out): is it honestly tensioned,
strategy           did the human confirm?
```

**The connection point — corrected.** dispatch-spec *does* have a `subagent_strategy` block (L98-120), and it explicitly does **not** execute subagents. But it does not hand off to domainspec-subagents-strategy. Its own text (L104-106) names **"the orchestrating capability, usually Refine"** as what must show the strategy and ask permission. domainspec-subagents-strategy is never named in dispatch-spec. So: dispatch-spec hands its validated route to the **orchestrator (usually Refine)**; if that orchestrator then spawns a tensioned subagent fan-out, *that* fan-out is separately governed by domainspec-subagents-strategy.

## Concretely, for the manual idea
- The whole chain (craft → research → whisper → x-ray) is a **dispatch-spec** route — validate its shape once.
- The research stage inside it — "spawn agents to gather all Arcanum knowledge and synthesize it" — is a **domainspec-subagents-strategy** `dispatch_type: research` (synthesis trigger → tension design + the human gate).

They don't compete: dispatch-spec validates the route's shape; domainspec-subagents-strategy routes and gates a subagent dispatch the orchestrator may run inside it.

---

## Changelog (review findings applied)
- **#1 (MAJOR):** "domainspec-subagents-strategy takes over" → corrected to "hands off to the orchestrator (usually Refine); the fan-out is separately governed by domainspec-subagents-strategy."
- **#2 (MAJOR):** "two layers / outer contract / governed engine for one step" → demoted from asserted fact to an explicit analogy; added peers-under-shared-constitution framing.
- **#3 (MAJOR):** pass/flag/block cite L31-32 → L148 / L166-169.
- **#4 (MINOR):** "governs / governed engine" → "routes / gates" for the router.
- **#5 (MINOR):** check-tension "quality mechanism" → "invokes (a separate skill it points to)."
- **#6 (MINOR):** "deterministic validator (L11-29)" → tier L11; section L56-68.
- **#7 (MINOR):** added Rule 22 footnote on the dispatch-spec subagent gate.
- **Unchanged (verified accurate):** 25 rules + Python validator, "A router" (L1-4), P1 triggers (L10), human confirm (L17), LIVE table (L43/45/48), subagent_strategy block existence (L98-120).
