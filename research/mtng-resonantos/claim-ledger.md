# Claim Ledger

Every load-bearing claim, labeled by source kind. A claim does not rise above this layer
without a label. `primary-source` here means **the packet states it** (it does not mean the
claim is externally true — see the ResonantOS/OKF claims, which are `related-source` because
the packet only *asserts* the external systems).

## A. What MTNG is (design claims)

| # | Claim | Source kind | Anchor |
|---|---|---|---|
| A1 | MTNG is an on-demand engine that turns selected messy work evidence into reviewable artifacts. | primary-source | `01` §1 |
| A2 | The pipeline is `Signal → Mode → Node → Validator → Synthesis`. | primary-source | `01` §5 |
| A3 | A Node is a bounded unit with a contract: accepts/rejects/allowed+blocked context/output artifact/validator/status/merge target/contribution hooks. | primary-source | `01` §5, §14 |
| A4 | Validators are not only quality checks — they are *misrouting detectors* (a failed validator flags a possible reroute). | primary-source | `01` §5, §15 |
| A5 | "Branch only when a boundary changes" (8 enumerated boundary types). | primary-source | `01` §1, §12 |
| A6 | V1 uses binary branch triggers; the numeric Branch Pressure Score is deferred. | primary-source | `01` §12; `05` #4 |
| A7 | "Tone" is renamed "Routing Signature" for V1 implementation language; routing signatures are hints, not proof. | primary-source | `01` §5; `05` #5 |
| A8 | V1 node lifecycle is `proposed → processing → closed`, with `closed_result ∈ {passed, partial, failed, rejected, superseded, needs_human}`. | primary-source | `01` §14; `05` #6 |
| A9 | Misrouting limits: max 1 reroute/signal, max 1 validator failure/node, max 1 new branch after failure; 2nd failure → write uncertainty + stop. | primary-source | `01` §15 |
| A10 | Synthesis must include failed/partial nodes as labeled status; must not hide conflict or assert a winner without evidence. | primary-source | `01` §17 |
| A11 | Memory candidates are review-only; no automatic durable-memory promotion in V1. | primary-source | `01` §18; `04` |
| A12 | Contribution records capture *structure* (who triaged/reproduced/reviewed), never *value* (no compensation/voting/tokenization/leaderboard). | primary-source | `01` §19 |
| A13 | OKF-first for exported knowledge artifacts; MTNG-native YAML/JSON for operational state; explicit `edge_case_flags` when OKF is insufficient. | primary-source | `01` §20 |
| A14 | Specialty tools never mutate graph state directly — they submit proposals the engine accepts/rejects/queues. | primary-source | `01` §9 |
| A15 | Data minimization: process only selected inputs; raw inputs not retained by default; audit log retained by default. | primary-source | `01` §8 |

## B. Problem / motivation claims

| # | Claim | Source kind | Anchor |
|---|---|---|---|
| B1 | Agent failures stem from overloading one context with too many unresolved jobs (not from individual bad model responses). | primary-source | `01` §4; Analog6 §1 |
| B2 | A flat summary of a mixed report loses structure (reproduction uncertainty vs provider failure vs UX vs docs vs contribution). | primary-source | `01` §4 |
| B3 | "Attention thrash / doom loops / hallucinated progress" are real recurring production failure modes. | related-source (Analog6 asserts as reviewer experience) | Analog6 §5 |
| B4 | The same problem is namable as "state-space collapse." | related-source | Gemini §1 |

## C. Claims about external systems — UNVERIFIED by this tower

| # | Claim | Source kind | Anchor | Residue |
|---|---|---|---|---|
| C1 | ResonantOS exists and has Guardian Core, Blackboard, Bridge Server, Event bus, Provider fabric/broker, Living Archive, add-on capability model. | related-source (asserted only) | `01` §10; Analog6 §6.4; Raptor §4 | R-INT |
| C2 | ResonantOS is "browser-first" with safe provider routing, gated memory writes, add-on mediation. | related-source | Raptor §1, §2 | R-INT |
| C3 | "OKF = Google's Open Knowledge Format" is a real interchange format MTNG can target. | related-source (and name is inconsistent — see D2) | `01` §20 | R-OKF |
| C4 | Phase 0 integration mapping has **not yet been performed**. | primary-source (admitted gap) | `05` (remaining gaps) | R-INT |

## D. Tensions / internal inconsistencies (review seeds)

| # | Observation | Source kind | Anchor |
|---|---|---|---|
| D1 | Raptor flags that the proposal cannot fully claim "not making agents more autonomous" while still describing branch-based execution; v2 narrows but the Signal→Mode→Node language still implies an engine that *acts*. | related-source + local-inference | Raptor §6 |
| D2 | Name inconsistency: spec says **Open Knowledge Format**, Gemini says **Open Knowledge Framework**. Unresolved; the spec also admits "exact OKF type names are deferred." | local-inference | `01` §20; `07`; `05` |
| D3 | Analog 6 PDF reviews **v1** (6 phases, Branch Pressure Score, 12 contribution types). v2 defers much of that. So the PDF's praise ("strong foundation") is praise for a *different, larger* design than the v2 being reviewed now. | local-inference | Analog6 vs `01`/`05` |
| D4 | All three reviews converge on the same boundary (sidecar/post-hoc, not live runtime). Convergence is reassuring but also means **no review stress-tested the post-hoc value claim itself** — they bounded scope, they did not prove usefulness. | local-inference | `08` (shared signal) |
| D5 | "Routing Signature" still detects modes from unstructured substrings ("I clicked around"). Renaming reduces metaphor risk but not the underlying classification fragility Analog 6 (§6.1) and Gemini ("Metaphor Trap") both flagged. | local-inference | `01` §5; Analog6 §6.1; Gemini §3 |
| D6 | Pilot success criteria (`01` §21) are largely qualitative ("becomes clearer", "more actionable", "acceptable overhead") with no measurement method or threshold. | local-inference | `01` §21, §25 |

## E. Operator / Arcanum readings (NON-SOURCE — bridge)

| # | Reading | Source kind | Where developed |
|---|---|---|---|
| E1 | MTNG's "branch only on boundary change" is the same discipline as the subagents-strategy **P1 dispatch triggers** (synthesis/context-protection/isolation/parallelism) — both refuse to fan out without a named reason. | analogy | `bridge-decisions.md` |
| E2 | MTNG's "validator as misrouting detector" maps to the **check-tension gate** (a structural check that catches mis-framed work before it propagates). | analogy | `bridge-decisions.md` |
| E3 | MTNG's "capture contribution structure, defer valuation" mirrors `register-dispatch` recording angle/axis without scoring agents. | analogy | `bridge-decisions.md` |
| E4 | MTNG's `closed_result` vocabulary ≈ the dispatch `exit_reason` closed vocabulary. Both make outcome auditable rather than inferred. | analogy | `bridge-decisions.md` |
