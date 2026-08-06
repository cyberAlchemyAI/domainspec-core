# Stage 4: Research Decision

- Research policy: `research-if-gap-appears`.
- Decision: `no external research` for this run.
- Status: `pass`.

## Why Local Evidence Is Enough

The review identified access, projection ownership, caching, freshness, and
answer-boundary questions. The current local sources already establish the
required safety and ownership constraints. External material cannot select a
local owner, approve a disclosure policy, or provide measurements for a system
that has not been implemented.

The design can therefore:

- define an access-policy port while leaving its owner unselected;
- define a neutral projection contract while leaving compilation and storage
  unimplemented;
- define configurable limits without claiming validated defaults;
- define a native agent-tool adapter without claiming host integration; and
- record HTTP, protocol comparisons, and production hardening as future work.

## Named Gaps And Disposition

| Gap | Needs external research now? | Disposition |
| --- | --- | --- |
| Agent-tool protocol details | no | Define a host-neutral application interface; select the concrete host protocol during implementation discovery. |
| Authentication mechanism | no | Require a verified identity and policy input; owner selects the mechanism later. |
| Retrieval quality thresholds | no | Use fixtures and measurements before setting thresholds. |
| Cache and freshness defaults | no | Make them configuration with fail-closed behavior; validate later. |
| Neutral projection owner | no | Route to a future owner decision; do not infer ownership. |

## Research Trigger That Would Reopen The Gate

Reopen bounded research only if a future implementation owner names one exact
protocol or security question whose answer is not present in the selected host
contracts. That pass requires separate user confirmation.

## Native Stage Receipt

- Stage: `s4`.
- Owning capability: `refine`.
- Capability handle: `.agents/skills/refine/SKILL.md#research-policy`.
- Mode: `research-if-gap-appears` resolved to `no-research`.
- Artifact: `stages/04-research-decision.md`.
- Status: `complete`.
- Verdict: `pass`.
- External calls: 0.
- Observer status: not configured.
- Handoff note: Distill may select the smallest design unit from local evidence.

