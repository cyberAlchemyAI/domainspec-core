# Gap 5 — Failure modes in buyer language

> **Candidate. Not a contract.** Claims tagged `[proven]` / `[hypothesis]`. Closes the fifth inherited
> GoldenQuill gap: GoldenQuill listed technical gates but never told the buyer, in plain language, *how
> this can fail and what we do about it.* No pricing or named-client commitments.

Each row is written as a buyer would say it, then mapped to the guard that addresses it.

| How the buyer would say it | What is actually failing | Guard / mitigation | Honest residual risk |
| --- | --- | --- | --- |
| "The dashboard dropped something that matters." | Concept erasure — the metric schema dropped a dimension. | Every metric declares its denominator + the dimensions it covers (a *pair, not a number*). **[proven]** the denominator-semantics gate. | The framing is an **interpretive principle, not a proof** — a well-defined metric can still omit a dimension nobody named. `[hypothesis / interpretive]` |
| "The number is just wrong." | Number hallucination — distorted value (wrong denominator, invented rows). | Every metric traces to its source-event chain; source-truth gate rejects unsourced events. **[proven]**. | A reviewer who only checks the number reconciles can still miss a dropped dimension — two separate audits are required. |
| "A lesson got treated as gospel too soon." | Premature promotion. | No reuse without an explicit human owner decision; a metric may not self-promote. **[proven]**. | If the owner approves carelessly, the gate passed but the judgment was poor — owner judgment is irreducible. |
| "Our private data leaked into shared advice." | Privacy-boundary failure. | Classification register, **fail-closed** (unknown = restricted); scoped feedback redacted before shared reuse. **[proven]**. | In pilot-1 the register is **advisory with a manual hash**, not cryptographically signed. `[hypothesis]` |
| "Two lessons contradict and we shipped both." | Unresolved contradiction. | An open `contradicts` edge **blocks** promotion until an owner resolves it. **[proven]**. | A contradiction nobody *declared* is not caught — the system catches declared conflicts, not unknown ones. |
| "The agent did something we didn't sanction." | Ungoverned agent action. | Agents are propose-only on client data; deterministic gates fail-closed; owner decision stays human. **[proven]**. | Self-validation reduces but does not eliminate model error; humans stay in the loop precisely because of this. |
| "It just logs; it never gets smarter." | The feedback edge never closes. | A promoted lesson updates the ontology cards / routing / gates so the *next* run is scored better. **[hypothesis]** — the closing edge is an adaptation validated in the pilot. | This closing edge is the part most dependent on review cadence — set it wrong (D5) and the loop logs instead of learns. `[hypothesis]` |
| "We outgrew the spreadsheet." | Lane-A scale ceiling. | Illustrative order-of-magnitude ceiling ~10k events/month (not a measured limit); migrate to a DB at scale. **[hypothesis]**. | The migration is real work, not automatic. |
| "You promised governance the tools can't enforce." | Lane-B bridge gap. | Two of five Lane-B bridges are NET-NEW; scoped before being promised. **[hypothesis]**. | If a bridge slips, the affected gate is advisory, not runtime-enforced, until built. |
| "The whole metric set is mis-scoped." | Wrong run boundary (esp. cap-factory lot vs order). | Run boundary resolved explicitly in assessment before any layer installs. **[proven]** layer-gating. | This is the single highest-leverage decision (D7 / C7) — get it wrong and everything downstream inherits it. |

## The meta-failure: over-claiming

The largest risk to *this engagement* is overstating what is proven. Mitigation is structural, not
promised: every claim in this package is tagged `[proven]` / `[hypothesis]`, the anti-collapse framing is
labeled interpretive rather than proven, and the cross-vertical generalization is explicitly a
hypothesis the parallel pilots must validate. **[hypothesis]** — this is the "candidates only,
honesty gate" discipline applied to our own marketing.
