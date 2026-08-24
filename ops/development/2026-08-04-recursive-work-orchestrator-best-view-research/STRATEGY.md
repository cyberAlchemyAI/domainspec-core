# Recursive Work Orchestrator Best-View Research Strategy

Status: `confirmation-readiness candidate`  
Dispatch type: `research`  
Evidence contract: `exact-binding`  
Authority effect: `none`

## P1 Trigger Decision

Dispatch is required. The question is small in wording but cross-disciplinary in
proof: a faithful answer must reconcile formal software architecture, temporal
and causal workflow explanation, information visualization, learner navigation,
accessibility, local owned precedents, and the design's strict authority
boundaries. Those lanes can proceed independently, and their likely biases need
adversarial comparison before a writer chooses a view.

The working hypothesis is a synchronized **Structure / Flow / Ownership** view
system with one part inspector. It is a hypothesis, not the dispatch conclusion.
The explorers must compare it against other credible grammars and may reject it.

## Intended Result

The research will recommend one primary view architecture through which a reader
can:

1. see the whole system and its owner boundaries;
2. understand why leaf work and a composite pipeline share one `Work` contract;
3. inspect sequence, fan-out, fan-in, gates, sidecars, bounded repetition, and
   explicit graph composition;
4. replay how commands, events, routing state, work-owned status, confirmation,
   and effects relate in a concrete run;
5. distinguish bus transport, journal persistence, orchestration decisions, work
   execution, and external effects;
6. move from overview to every named design and ontology part without duplicating
   semantic truth; and
7. see what is proposed, implemented, validated, unknown, or forbidden.

The durable result is `findings.md`: a source-bound recommendation, compact
wireframe, part atlas, scenario walkthroughs, interaction grammar, MVP boundary,
negative controls, and separated validation plans. It is not an HTML prototype
or human-comprehension result.

## Groups And Subagents

| Group | Execution | Anti-bias purpose | Agents and outputs |
| --- | --- | --- | --- |
| `explorers` | three lanes in parallel | Formal structure vs causal time vs learner-centered progressive disclosure | **Abramsky, Samson** — architecture notation, recursive composition, and component anatomy. **Hewitt, Carl** — commands/events, state, gates, retries, sidecars, and replay. **Alexander, Christopher** — coordinated views, progressive disclosure, accessibility, and novice/expert journeys. |
| `synthesizer` | after all explorers | Compare rather than average the grammars; preserve topology, time, ownership, and proof ceilings | **Simon, Herbert** — candidate comparison, recommended view architecture, complete mapping, scenarios, negative controls, and MVP boundary. |
| `reviewers` | three lanes in parallel after synthesis, with one bounded zig-zag | Precedent vs explanatory non-vacuity vs definitional and authority non-collapse | **Hacking, Ian** — owner and pattern precedent. **Popper, Karl** — finite scenarios and misleading-view mutants. **Wittgenstein, Ludwig** — semantic distinctions, legend, owner, and misuse pressure. |
| `writer` | after exact-binding evidence closure | Produce a clear guide without inventing evidence or implementation | **Senge, Peter** — `findings.md` only. |
| `auditor` | after writer | Independent completeness, evidence, semantics, and claim-ceiling audit | **Bourbaki, Nicolas** — `ACCEPT` or one bounded writer revision. |

Nine target agents are declared: three explorers, one synthesizer, three
reviewers, one writer, and one final auditor. The two independent pre-confirm
tension agents are gate infrastructure and are not part of this count.

## Dependency Flow

```text
explorers (parallel)
  -> synthesizer
  <-> reviewers (parallel; zig-zag cap 1)
  -> exact-binding evidence closure
  -> writer
  -> auditor
  -> one bounded writer repair if required
```

A conditional synthesizer-to-explorer feedback edge may obtain a missing source
binding. The writer cannot repair missing evidence with prose.

## Inventory Preflight

- Machine index: `.arcanum/inventory/index.json`
- Validation: `lookup_readiness=ready`, 290 entries, zero failures, 146 tag
  warnings; Inventory remains a non-authority read model.
- Target-local machine index: absent at
  `projects/cyberalchemy-orchestrator/.arcanum/inventory/index.json`.
- Selected evidence: Interactive Ontology Learning Map; IOLM workable example;
  Body War novice-comprehension review; learning-graph next-route guide; current
  orchestrator purpose and reasoning-engine boundary.
- Primary consequence: do not assume one large graph. Compare structural anatomy,
  causal replay, and coordinated learner projections while keeping one semantic
  source and stable cross-view identity.
- Proof consequence: browser structure, accessibility behavior, agent tasks, and
  human comprehension remain four separate evidence layers.

The full lookup packet, selectors, exclusions, gaps, and claim ceilings are in
`strategy-inventory-packet.json`.

## Evidence Closure

The dispatch uses `exact-binding` because the recommendation must map every
load-bearing visual decision back to:

- the frozen local file identity and exact heading or structured selector;
- the direct external standard, official documentation, or original research
  source supporting the view principle;
- the explorer and reviewer receipt that carried the claim;
- its evidence scope, uncertainty, and proposal-only ceiling.

Missing source evidence blocks writing. It cannot be repaired by rhetorical
confidence.

## Capability-Bound Route

`DISPATCH-ROUTE.json` binds the roles to the `research` owner capability and
places them in five gated waves under `orchestrate`: exploration, synthesis,
review, writing, and audit. Only the writer may mutate, and only the exact
`findings.md` path. All other roles are read-only. The parent owns deterministic
`research.md` compilation, evidence closure, spawning, joins, gates, observability,
and closeout.

Authorization remains `requires_user_permission`. Orchestrate preflight and all
spawn attempts are forbidden until confirmation.

## Gates And Ledger State

- Live research schema: `0.8.0`.
- Candidate sheet: `dispatch-sheet.json`; it intentionally omits
  `evidence_binding` before confirmation.
- Candidate capability route: `DISPATCH-ROUTE.json`.
- Confirmation-readiness validation: `pass`; schema `0.8.0`; ledger mutation
  `none`; sheet SHA-256
  `71d472a581c142ea9edf0b8a8b721b70bd52faa9428604e98053bd605250b99f`.
- Material strategy projection: SHA-256
  `96acb6f84ef433ff32b0f2837edc0cc7b5b4530cb408750b31c906cf838b65af`;
  receipt in `material-strategy-receipt.json`.
- Dispatch Spec validation: `pass` for `DISPATCH-ROUTE.json`.
- Independent tension checker/reviewer: `PASS/PASS` at the frozen sheet digest;
  both passed tests 1-5 with no apontamentos. See `CHECK-TENSION.md`,
  `tension-checker.json`, and `tension-reviewer.json`.
- Human confirmation: direct explicit `confirmed` received at
  `2026-08-04T17:21:07-03:00`, bound to the frozen sheet and material digests in
  `confirmation-record.json`.
- Registration: not started. The append-only dispatch ledger must not change
  before confirmation.
- Execution: not started. No research subagent has been spawned.
- Inventory post-result hook: blocked without writes. Baseline lookup readiness
  is `ready`, but the deterministic appender's candidate stage cannot resolve 32
  already-indexed repository-relative `../../...` sources outside its temporary
  `.arcanum/inventory` copy. The query source and record are preserved for retry;
  `index.json` and `index.md` were not changed. See
  `INVENTORY-HOOK-RECEIPT.json`.

## Boundaries

- The target `DESIGN.md` and `ONTOLOGY.md` remain immutable inputs at their
  recorded SHA-256 digests.
- No edits to target design, ontology, product code, canonical definitions,
  Arcanum sources, Inventory, ledger, Git, publication, promotion, release,
  deployment, or runtime.
- The working folder may receive strategist-owned `research.md`, the single
  writer-owned `findings.md`, and bounded run receipts only after confirmation.
- Local Inventory entries are discovery leads; direct source artifacts remain
  decisive.
- The result may specify a prototype contract, but implementation requires a
  separate explicit route.
- Paper execution traces are design witnesses, not observed runtime evidence.
- Human comprehension remains unproven until separately authorized and measured.

## Stop Conditions

- Any pre-confirm readiness or tension gate does not pass.
- A target digest changes without rebuilding, revalidating, and re-tensioning the
  strategy.
- A role cannot access direct sources or returns uncited load-bearing claims.
- The reviewer zig-zag or auditor repair exceeds its one-loop cap.
- The recommendation loses a named design part, collapses an authority boundary,
  or inflates proposal evidence.
- Runtime capacity cannot preserve the declared roles, joins, and closeout.

## Next Human Action

After readiness, Dispatch Spec, and both tension gates pass, the parent will show
the final material strategy and frozen digest. Only an explicit `confirmed`
authorizes registration and execution. Any other reply is discussion, revision,
or decline.
