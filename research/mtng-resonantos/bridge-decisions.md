# Bridge Decisions (NON-SOURCE)

How MTNG ideas should — and should not — cross into Arcanum. Every row is an
`operator-reading`/`analogy`, never a source claim. **Promotion boundary: local-only.** Nothing
here enters Inventory, Ontology, sigils, spells, or canonical definitions without a separate
governed promotion decision.

Statuses: `borrow-carefully` · `analogy-only` · `block` · `promotion-candidate` · `future-work`.

| # | MTNG idea | Status | Decision + rationale | Arcanum touchpoint |
|---|---|---|---|---|
| BD-1 | **Branch only when a contract boundary changes** (DEF-3) | borrow-carefully | Arcanum already has this instinct in the subagents-strategy **P1 dispatch triggers** (synthesis / context-protection / isolation / parallelism). MTNG's 8 boundary types are a *finer-grained* articulation of "don't fan out without a named reason." Worth studying as a checklist when authoring dispatch sheets — **not** as a replacement for P1. | `domainspec-subagents-strategy` P1; `register-dispatch` |
| BD-2 | **Validator as misrouting detector** (DEF-4) | borrow-carefully | This is the strongest transferable idea: a *structural* check that catches mis-framed work, not just low-quality work. Direct analogue to the **check-tension** gate (verifies a sheet is genuinely tensioned before it propagates). MTNG adds: bound the reroute (1 attempt, then stop + record uncertainty). That bounded-reroute discipline is a clean lesson for any Arcanum gate that can send work back. | `check-tension`; gate loop caps |
| BD-3 | **Capture contribution structure, defer valuation** (DEF-6) | borrow-carefully | Mirrors `register-dispatch` recording each agent's angle + anti-bias axis **without scoring agents**. Reinforces the existing Arcanum stance that telemetry records structure, governance assigns value later. Use as supporting precedent, not new mechanism. | `register-dispatch`; telemetry |
| BD-4 | `closed_result` ↔ `exit_reason` closed vocabularies (E4) | analogy-only | Pleasing parallel (both make outcomes auditable via a fixed vocabulary). Keep them separate — different domains. Do not unify the enums. | dispatch `exit_reason` |
| BD-5 | **Synthesis must not hide conflict** (DEF-5) | analogy-only | Same value as P10 (claim ≤ proof) and P7's "a bare concat is never the final deliverable." MTNG states it for issue packets; Arcanum already states it for dispatch artifacts. Mutually confirming, no new mechanism. | P7, P10 |
| BD-6 | **MTNG as a live runtime orchestrator** | block | Out of scope by the spec's own V1 boundary, and Arcanum already routes work via the dispatch lifecycle. Adopting MTNG-as-runtime would duplicate and conflict. | — |
| BD-7 | **Numeric Branch Pressure Score** (weights/thresholds) | block (for now) | The spec itself defers it pending empirical data; adopting weighted scoring into Arcanum routing would be premature for the same reason. Revisit only if MTNG's evidence harness produces tuning data. | — |
| BD-8 | **OKF as a knowledge-interchange export standard** | future-work | Unverified format with a disputed name (R-OKF). Do not adopt or reference as canonical until the spec is fetched and pinned. | export conventions |
| BD-9 | **Node contract as a delegation primitive** (DEF-2) | promotion-candidate | The accepts/rejects/allowed-blocked-context/validator/closed_result shape is a genuinely good *bounded-task* contract and overlaps `task-session` completion criteria. **Candidate** for a future governed comparison against `task-session` / work-pack contracts — flagged, not promoted. | `task-session`; `invoke` work-pack |
| BD-10 | **"Routing Signature" substring detection** | block | Fragile substring→mode classification (D5, R-CLS). Do not import as a routing mechanism; Arcanum routing is explicit (dispatch_type), not inferred from text. | — |

## Net read for the user

The three ideas worth *carrying into Arcanum thinking* (BD-1, BD-2, BD-3) all happen to be
things Arcanum already does — so MTNG's value here is **confirmatory precedent**, not new
machinery. The one genuinely novel, well-shaped primitive is the **node contract** (BD-9), which
deserves a real comparison against `task-session` someday. Everything runtime-flavored is a
block. Nothing crosses the local-only line without a separate decision.
