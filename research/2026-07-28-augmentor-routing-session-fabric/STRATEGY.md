# Augmentor Routing And Session Fabric Research Strategy

Status: proposed, unconfirmed, unregistered, unexecuted.

This is a research strategy, not a product decision or implementation plan. It
does not change Necronomicon, Spellcraft, IDE Ergonomics, CyberAlchemy v2, or
ResonantOS.

## Direct strategy

The candidate direction to test is **one shell, not one global session**.
Augmentor should present one conversational interface while keeping project,
thread, active interaction, background run, artifact, notification, and memory
as separate owned states.

The dispatch must test, rather than assume, the following route behavior:

1. explicit commands and clear interruptions win;
2. an awaiting interaction normally consumes the next answer;
3. side notes are captured without switching the active route;
4. a fresh request creates or selects a route inside the current thread;
5. broad or concurrent work becomes an isolated child/background run with a
   frozen context snapshot and parent link;
6. missing capability fit can offer a light **easy** path, a bounded **test**
   path, or a lifecycle-owned **hardening** path when those are materially
   different;
7. reusable composition routes to Spellcraft only when repetition or reuse
   warrants a spell;
8. current ResonantOS thread, project, goal-workspace, delegation, and
   persistence owners are extended rather than replaced.

The literal witness keeps a main architecture conversation active while the user
starts a governed subagent-strategy proposal and a Whisper page in parallel,
switches to another thread, then returns to consume one success and one blocker
without context bleed.

## P1 trigger decision

Dispatch is required.

- **Synthesis:** Necronomicon, Spellcraft/Dispatch Spec, IDE Ergonomics, and the
  current ResonantOS consumer surface are separate source and ownership domains.
- **Context protection:** current consumer code, design documents, route
  contracts, and UX evidence would overflow a single parent analysis.
- **Isolation:** formal state design, human-factor design, and current-runtime
  verification should be independently discardable and adversarially checked.
- **Parallelism:** the four explorer lanes can run independently before
  synthesis.

Dispatch type is live `research`, schema `0.8.0`.

## Lanes, groups, and subagents

### Group 1 — explorers, parallel

Anti-bias axis: formal concurrency/session semantics versus bounded route
decision versus human one-interface ergonomics versus current consumer-runtime
verification.

| Agent | Role | Angle | Expected output |
| --- | --- | --- | --- |
| Hewitt, Carl | explorer | Formal session, interaction, parent-child run, cancellation, join, resume, context-isolation, and attention state. | Minimal state machine, invariants, global-session comparison, and concurrent witness fixtures. |
| Simon, Herbert | explorer | Free-language route decisions, confidence, missing capabilities, easy/test/hardening offers, and lifecycle escalation. | `RouteDecision`/`RouteOffer` contracts, owner map, ambiguity rules, and fallback fixtures. |
| Ahrens, Sönke | explorer | Human one-interface flow, transition cards, session switching, background attention, handoffs, knowledge references, and artifacts. | Progressive-disclosure journeys, surface allocation, accessibility, notification limits, and browser fixtures. |
| Turing, Alan | explorer | Current ResonantOS threads, projects, branching, run guards, goal workspaces, delegation, persistence, and browser seams. | Implemented-versus-missing matrix, additive integration seam, compatibility risks, and exact tests. |

### Group 2 — synthesizer, sequential

| Agent | Role | Expected output |
| --- | --- | --- |
| Shannon, Claude | synthesizer | One cited candidate architecture joining state, route, UX, and consumer evidence; explicit disagreement, contracts, budgets, fixtures, and v0/v1/v2 increments. |

### Group 3 — reviewers, parallel with bounded zig-zag

Anti-bias axis: precedent/duplication versus non-vacuity/observable route
quality versus definitional/state-model non-collapse.

| Agent | Role | Gate | Expected output |
| --- | --- | --- | --- |
| Lakatos, Imre | skeptic | precedent | Owner and duplication map; build-from-owned corrections; no KILL from precedent. |
| Gödel, Kurt | skeptic | non-vacuity | Runnable concurrent witness and measurable classification, isolation, control, and overhead; KILL if absent. |
| Quine, Willard Van Orman | skeptic | definitional-soundness | Non-collapse proof for interface/project/thread/interaction/route/run/artifact/memory and real easy/test/hardening distinctions; KILL if tautological. |

### Group 4 — writer, sequential after evidence closure

| Agent | Role | Expected output |
| --- | --- | --- |
| van Lamsweerde, Axel | writer | `findings.md` only, containing the evidence-closed implementation-usable blueprint and verdict matrix. |

The strategist, not the writer, mechanically appends verbatim explorer returns
to `research.md`.

### Group 5 — auditor, sequential

| Agent | Role | Expected output |
| --- | --- | --- |
| Brandenburg, Martin | auditor | Audit of `findings.md` only; `RECOMMEND_ACCEPT` or one bounded writer revision request. |

The parent remains the final approver.

## Dependency flow

```text
4 explorers in parallel
  -> join all
  -> synthesizer
  -> 3 reviewers in parallel
  -> bounded synthesizer/reviewer zig-zag, max 2
  -> optional synthesizer-to-explorer evidence feedback, max 1
  -> cited-synthesis evidence closure
  -> writer
  -> auditor
  -> optional auditor-to-writer revision, max 1
  -> parent final approval and closeout
```

The writer stays blocked unless evidence closure returns `ready`. Missing source
bytes, provenance, or selectors route only through the already-declared explorer
feedback edge while capacity remains; they cannot be repaired as prose by the
writer.

## Inventory preflight

Machine-index validation passed with `lookup_readiness=ready`; 102 uncontrolled
historical-tag warnings did not block lookup.

Selected:

- `augmentor-user-graph-reasoning-research-result-synthesis` — fixes the
  accepted Augmentor memory, disposable graph, bounded reasoning, user-control,
  and consumer-owner boundaries.
- `entries-unified-ide-ergonomics-spine-synthesis` — supplies the candidate
  transition-card, side-note, route-menu, handoff, subagent-preview, and
  lifecycle vocabulary.
- `entries-resonantos-living-archive-seam-and-owned-base-synthesis` — preserves
  host-owned memory and intake seams.

Excluded:

- both unexecuted earlier Augmentor strategy entries, because their verified
  result is stronger;
- the Whisper copy-maintenance review, because it does not cover route/session
  state;
- ontology-presentation cards, because they do not answer continuation or
  consumer routing.

Current-source checks changed the dispatch materially: the requested
`../workspace-resonantos` path does not exist, while
`../workspace-resonant/2.0.0-alpha` does. That consumer already has
`conversationThreads`, `chatProjects`, thread/project branching, a goal-workspace
state machine, and bounded delegation packets. Its `dev` branch is seven commits
behind `origin/dev`, but those seven commits affect Agent Control/public-submit,
not the inspected chat/session scope.

Open gaps include the missing binding between Necronomicon
`active_interaction` and current consumer state, no route-quality benchmark, no
accepted easy/test/hardening contract, no accepted parent-child background-run
model, and no product-local machine Inventory index.

Full packet:
[`strategy-inventory-packet.json`](strategy-inventory-packet.json).

## Spellcraft and Necronomicon boundary

Necronomicon supplies the continuation order, active-interaction owner,
side-note behavior, route confidence, fallback discovery, and capability-update
precedent. It does not automatically become ResonantOS's storage model.

Spellcraft supplies the lifecycle test for a reusable composition: named phases,
inputs, outputs, gates, failure policy, handoffs, observability, and experiment
evidence. The dispatch must decide whether the surviving route is:

- consumer-local routing behavior;
- a local spell composition;
- a reusable spell;
- a changed sigil contract;
- or only a one-off route pattern.

No spell is authored by this research.

## Gate and ledger state

- Candidate sheet:
  [`dispatch-sheet.json`](dispatch-sheet.json).
- Capability-bound execution route:
  [`DISPATCH-ROUTE.json`](DISPATCH-ROUTE.json).
- Confirmation readiness: `PASS`, schema `0.8.0`, ledger mutation `none`.
- Frozen sheet SHA-256:
  `78849ca1bd09a13daab93629d9ac2bf1ac5d6571063d75a6d05397242065235e`.
- Dispatch Spec validation: `PASS`.
- Check-tension: independent checker `PASS` and reviewer `PASS` on the exact
  frozen digest; see [`CHECK-TENSION.md`](CHECK-TENSION.md).
- Human confirmation: required now.
- Registration: not appended.
- Execution: no research agent launched.
- Closeout expectation after a run: join and close every spawned agent, append
  one dispatch row and one close row, preserve partial residue, and inventory the
  durable result.

## Next human action

The proposal is fully ready. To authorize registration and execution of this
exact frozen dispatch, reply:

`confirmed`

Any requested sheet revision will produce a new digest and repeat readiness,
both tension checks, and confirmation.
