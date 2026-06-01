# Tilth Lessons Memory — What It Does

Every grant cycle teaches your organization something. Which proposals won. Which funders responded to which kind of framing. Where the review caught a problem before it went out. Where the proposal claimed something that needed updating before the next round.

Most of that learning lives in the heads of the people who did the work. When they leave, it leaves. When the cycle is long enough, even they forget.

**Lessons Memory** is the part of Tilth that keeps that learning where the organization can use it. It watches what happens across grant cycles, proposes lessons the operator can confirm, and warns when a new proposal is repeating a pattern that already didn't work. Operator approves every change. Nothing gets remembered without the operator saying so.

## What it learns from

- **Prior grant cycles** — which proposals were funded, declined, or sent back for revision
- **Approval decisions** — what the operator confirmed during review, and what they overrode
- **Review catches** — places where Tilth's internal review found a problem before submission
- **Funder outcomes** — what each funder actually awarded, declined, or asked to revise
- **Fact updates** — when something a proposal claimed turned out to need correcting

These are *outcomes*. Real signals from the world, not Tilth's own opinion of how it did.

## What it produces

- **Proposed lessons** — never auto-applied; always reviewed by the operator before they land
- **Pattern digests** — recurring strengths, recurring failure modes, organized by funder and by program
- **Funder-signal summaries** — what this funder seems to respond to, with the evidence cited
- **Warnings** — when a new draft is repeating a pattern that didn't work last time

A concrete example: if a foundation funded three of the operator's proposals that all emphasized partnership structure, Lessons Memory proposes flagging partnership framing as a pattern for the next draft to that funder. The operator confirms before anything changes. If the operator says no, nothing changes.

## What it never does

- Never changes live memory on its own
- Never authorizes its own changes
- Never learns from its own internal review scores alone — the classic self-improvement trap, where an AI system convinces itself it's getting better because it's the one grading its own work
- Never moves customer-specific learning outside the customer's own Golden Quill
- Never invents lessons from insufficient evidence — patterns need enough cycles behind them to be real

## Safety architecture, translated

Three plain-language layers, all structural — not policy, not promises:

1. **Operator approves every change.** Lessons Memory proposes; the operator confirms. There is no path for the system to write to its own memory without an explicit operator sign-off. Every approval is captured in a verified record the operator can audit later.
2. **Evidence required.** A proposed lesson has to point to real outcomes — funder decisions, operator approvals, review catches, fact updates — not just to Tilth's own evaluators agreeing with each other. This rule is built into the gate that lets a lesson reach the operator's review queue.
3. **Local by default.** Customer-specific learning stays on the customer's own Golden Quill. Nothing leaves the box. Pattern-level signals (with personally-identifying detail stripped) become shareable only if the operator explicitly opts in.

## How Lessons Memory respects the deployment posture

Lessons Memory is **always-local** under every Tilth deployment posture. It does not change behavior based on which of the three customer-facing routing postures the deployment is operating under:

- **Frontier-Eligible** — the deployment permits selected Public + Shareable project data to route to external/frontier models for drafting / review work. Lessons Memory still runs entirely on the operator's Golden Quill; lesson proposal reasoning never leaves the box.
- **Split-Context Hybrid** — the deployment lets frontier models help with structural / scaffold composition only, on an operator-signed allow-list. Lessons Memory operates the same way: local-only, operator-approved.
- **Local-Only / Sovereign** — every Tilth seat runs local. This posture is **performance-dependent / under validation** until proven against real grant workloads; customer-facing materials note this caveat explicitly. Lessons Memory's behavior is unchanged because it was already always-local.

The pattern is structural, not policy: Lessons Memory's producer (the Reflection sub-mode of the Archivist) is always-local under all three v7.0.10 postures, by architectural-amendment row (v7.0.9 Reflection v0.1 hook + v7.0.10 §3 retentions footer addendum). Customers selecting Frontier-Eligible or Split-Context Hybrid get cloud-frontier help *on drafting* without changing how lessons are proposed or approved.

## How it fits the rest of Tilth

Lessons Memory is a third cadence under Tilth's existing between-cycle review work — alongside the weekly and quarterly passes. It doesn't add a new agent. It extends what's already there. The operator's existing review surface is where lessons land for confirmation. The existing audit trail is where every approval is recorded.

## Why this matters commercially

The honest framing: most AI agent systems either *don't learn* — and stay shallow, repeating the same mistakes across customers and across cycles — or they *do learn from their own outputs* — and quietly drift toward gaming their own evaluators, looking better on internal metrics while doing worse in the real world.

Industry-standard self-improvement features ship without these constraints. Tilth's chooses to add them.

The system gets better over time *because* operators approve real lessons grounded in real outcomes — not because the AI told itself it did well. That's the difference between a tool that compounds with use and a tool that drifts with use. Funders notice the difference. So does the operator who has to live with the proposals year after year.

Tilth is built for the second kind. Lessons Memory is how it stays that way.
