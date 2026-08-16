# Findings: agent orchestration for a beginner

## Status and scope

These are the writer-owned findings admitted by the Recovery 003 evidence-closure decision. They are a repository-local research artifact, not the final beginner guide. They still require an independent audit, parent final disposition, Orchestrate terminal closeout, and the dispatch-ledger close transition.

The central finding is simple:

> Agent orchestration is best understood as a sequence of owner-controlled transitions, not as one powerful agent doing everything. At every point, ask: what is the last transition directly supported by evidence, who owns the next decision, and what remains unproved?

Evidence: `receipts/synthesis.json#/synthesis/governing_rule`, `#/synthesis/owner_transitions`; `recovery-003/receipts/evidence-closure-recovery-003.json#/evidence_rows/1` (`C02`).

All evidence paths cited below are bound to exact SHA-256 values in `recovery-003/receipts/evidence-closure-recovery-003.json#/completed_inputs`. Explorer claims are additionally bounded by `receipts/synthesis.json#/evidence_bindings`; direct owner precedents are bound by `recovery-002/precedent-repair-packet.json#/direct_source_bindings`. A citation transfers only the evidence scope stated at that selector.

## Review verdicts and dispositions

| Review | Preserved verdict | Disposition for these findings | What it does not prove |
|---|---|---|---|
| Original precedent review | `FLAG` | Historical verdict preserved. Its six defects required direct-source bindings, a component status matrix, a repaired owner graph, typed gates and closeouts, adjacent-owner exclusions, and an export allowlist. | Writer admission, semantic correctness, publication, or deployment. |
| Non-vacuity review | `KILL` | The claim that the synthesis worked example is one complete, evidence-backed successful dispatch witness is killed. Its narrower lifecycle model and fail-closed examples survive. | That any earlier recovery or the present run is a complete success witness. |
| Recovered definitional review | `PASS` with bounded wording repairs | The operational distinctions survive exact freeze admission and comparison. They remain operational explanations, not invented canonical definitions. | Current runtime conformance or canonical vocabulary promotion. |
| Fresh precedent recheck | `PASS` | All six original precedent defects pass against the exact current direct-source bytes. | Writer execution by itself; parent evidence closure was still required. |
| Parent evidence closure | `ready`; writer `admit` | Every required claim was bound, killed, or deferred, so writing may proceed at this ceiling. | Audit, parent final approval, run closeout, ledger close, Craft state, or publication. |

Evidence: `receipts/skeptic-precedent.json#/review_verdict`, `#/defects`; `receipts/skeptic-non-vacuity.json#/review/verdict`, `#/review/killed_candidate`; `recovery-003/receipts/skeptic-definitional-recovered.json#/review_verdict`, `#/comparison_summary`; `recovery-003/receipts/skeptic-precedent-recheck.json#/defect_reviews`; `recovery-003/receipts/evidence-closure-recovery-003.json#/review_dispositions`, `#/status`, `#/writer_admission`.

The evidence-closure ledger must remain visible:

- `C01` through `C08`, `C11`, and `C12` are bound within their stated evidence scopes.
- `C09` is killed only as a complete-success-witness claim; the narrower preserved transitions and fail-closed examples remain usable.
- `C10` is deferred because Recovery 003 cannot be a complete successful witness before writer, audit, parent disposition, Orchestrate closeout, and dispatch-ledger close are evidenced.
- `C13` is deferred as a negative ceiling: nothing in this research lifecycle establishes canonical promotion, publication, release, deployment, production, or semantic authority.

Evidence: `recovery-003/receipts/evidence-closure-recovery-003.json#/evidence_rows`.

## 1. Start with the coordination need

One bounded worker inside the parent’s already-bounded scope is a **helper**. When the work genuinely needs independent viewpoints, synthesis, context protection, isolation, or dependency-gated parallelism, it may justify a governed **dispatch**. A dispatch adds a lifecycle: strategy, an exact route, checks, authorization, registration, execution, evidence admission, review, and terminal accounting. It does not give agents more semantic authority.

The distinction matters because delegation alone should not trigger a scheduler, ledger entry, or multi-agent claim. The parent first decides whether the work can stay bounded to one helper. Only a materially presented multi-agent route becomes a dispatch candidate.

Evidence: `receipts/synthesis.json#/synthesis/operational_vocabulary/helper`, `#/synthesis/operational_vocabulary/dispatch`; `research.md:9-58`; `research.md:1804-1837`; direct binding `PUB-03` in `recovery-002/precedent-repair-packet.json#/direct_source_bindings`.

## 2. The useful vocabulary is operational, not magically authoritative

For this guide, the terms below are safe as operational explanations:

| Term | Beginner-safe meaning | Authority ceiling |
|---|---|---|
| Helper | One worker inside an already-bounded parent scope. | Not a governed dispatch or an independent authority. |
| Dispatch | A governed multi-agent lifecycle justified by a real coordination need. | Not proof that the route is good, authorized, executed, or true. |
| Strategy | The explanation of why work is divided, where disagreement belongs, and what each lane may prove. | Not the machine-readable route and not permission. |
| Dispatch sheet | The exact topology binding roles, scopes, dependencies, gates, stops, and outputs. | Candidate bytes until readiness, review, confirmation, and registration occur. |
| Role | A responsibility slot bound to one capability and scope. | Not an agent identity or independent authority. |
| Wave | Actions eligible to run together after their dependencies pass. | Eligibility is not execution. |
| Receipt | One attributable bounded action result. | Evidence, not semantic truth, admission, or acceptance. |
| Join | Admission of a checked receipt into reduction. | More than waiting; still not semantic acceptance. |
| Gate | A named owner’s transition decision over admitted evidence. | A pass does not prove the dependent wave ran. |
| Closeout | Terminal accounting for a bounded lifecycle. | Not truth, promotion, publication, deployment, or production. |

Many of these terms have usable owner-local meanings but no standalone Arcanum-wide definition entry. In particular, **sigil**, **spell**, and **capability** are descriptive README vocabulary; the open formal-definition gap must be stated rather than filled by the guide.

Evidence: `receipts/synthesis.json#/synthesis/operational_vocabulary`, `#/synthesis/non_implications`; `research.md:9-87`; `recovery-003/receipts/evidence-closure-recovery-003.json#/evidence_rows/3` (`C04`), `#/evidence_rows/10` (`C11`); `recovery-002/precedent-repair-packet.json#/direct_source_bindings/0` (`PUB-01`), `#/direct_source_bindings/1` (`PUB-02`).

## 3. The lifecycle is a chain of distinct owners

The beginner guide should teach the following transition chain without compressing it into a single idea called “approval”:

| Transition | Owner | What the transition establishes | What remains unproved |
|---|---|---|---|
| Request → helper-or-dispatch decision | Parent plus Subagent Strategy | Whether governed coordination is justified. | Route quality, permission, or execution. |
| Strategy → exact sheet | Strategy and repository-local form owners | Material rationale and exact topology. | Readiness, tension, authorization, or execution. |
| Candidate sheet → confirmation readiness | Repository-local form owner | Exact bytes pass form, identity, and scope checks. | Tension approval or human permission. |
| Ready sheet → two tension verdicts | Two independent tension owners | The exact route has been challenged for differentiation and coherence. | Human authorization. |
| Reviewed proposal → confirmation | Human | The exact material strategy is authorized. | Registration, preflight, execution, or truth. |
| Confirmed sheet → registration | Repository-local registrar | One durable open dispatch record binds the authorized topology. | That any agent ran. |
| Registered candidate → route-shape verdict | Dispatch Spec | The draft graph is structurally valid at its declared boundary. | Strategy selection, native execution, or semantic correctness. |
| Validated route → runtime preflight | Orchestrate | The first wave may be compiled under a valid route, authorization, and available host operations. | A spawn attempt or agent result. |
| Persisted action → native host result | Orchestrate plus the host | One exact job is attempted and either receives a real agent binding or records failure. | Terminal completion or a valid receipt. |
| Host result → terminal observation | Parent host loop under Orchestrate | The actual worker reaches a known terminal branch. | Logical close, receipt admission, or join. |
| Terminal observation → logical agent close | Orchestrate | One worker is accounted for or interrupted. | Wave completion or dispatch closeout. |
| Returned result → receipt admission | Orchestrate | Exact expected receipt shape, identity, and digest are accepted. | Join, gate pass, or semantic truth. |
| Admitted receipt → join | Orchestrate | The action result enters one reduction. | Gate outcome. |
| Joined wave → reducer gate | Orchestrate reducer | The declared next transition is admitted or blocked. | Dependent-wave execution. |
| Explorer evidence → reviewed synthesis | Research synthesizer and differentiated skeptics | A cited account and distinct precedent, non-vacuity, and definitional verdicts. | Writer eligibility until evidence closure. |
| Reviewed synthesis → research evidence closure | Parent acting under the research contract | Required rows are bound, deferred, killed, or unresolved; only `ready` admits writing. | Audit, parent final approval, or publication. |
| Closed evidence → findings | Writer | A cited `findings.md` at the admitted ceiling. | Audit or terminal acceptance. |
| Findings → research audit | Auditor | A bounded verdict on the exact findings artifact. | Parent final disposition. |
| Audit plus terminal evidence → final disposition | Parent | Acceptance, blockage, or limitation within the declared ceiling. | Authority outside that ceiling. |
| Causal run → Orchestrate run closeout | Orchestrate/parent closeout boundary | Exact bounded runtime history receives terminal accounting. | Dispatch-ledger closure or Craft state. |
| Final dispatch outcome → close row | Repository-local registrar | Exactly one close record pairs with the open dispatch record. | Publication, deployment, production, or Craft closure. |
| Project evidence → Craft state | Craft | Separate durable project work-ledger state, when explicitly invoked. | It is not changed by a dispatch close row. |
| Accepted research handoff → learning-guide candidate | Whisper | Downstream editorial composition. | Research acceptance, runtime proof, publication, or authority. |

Evidence: `recovery-002/precedent-repair-packet.json#/owner_transition_candidate`, `#/typed_gates_and_closeouts`; `recovery-003/receipts/evidence-closure-recovery-003.json#/evidence_rows/2` (`C03`), `#/evidence_rows/5` (`C06`); `research.md:135-183`, `research.md:381-657`, `research.md:893-1072`.

## 4. Dispatch Spec and Orchestrate solve different problems

**Dispatch Spec** is a draft route-shape validator. It checks that steps, roles, dependencies, waves, joins, gates, evidence obligations, scopes, stops, and promotion guardrails form an explicit composition. It neither chooses the material strategy nor executes agents.

**Orchestrate** owns the native coordination boundary after validation and authorization: preflight, persisted actions, host spawn and wait handshakes, terminal accounting, receipt admission, joins, reducer gates, dependent-wave planning, causal evidence, partial-wave recovery, and bounded run closeout. Delegated capabilities still own their semantic work.

Orchestrate specifically does **not** own material strategy, route-shape validation, research semantics, bounded SWU execution semantics, Craft work-ledger state, one-hop continuation routing, Inventory knowledge, post-run behavior telemetry, semantic truth, promotion, or publication.

Evidence: `recovery-003/receipts/evidence-closure-recovery-003.json#/evidence_rows/4` (`C05`); `recovery-002/precedent-repair-packet.json#/component_status_matrix/4`, `#/component_status_matrix/5`, `#/adjacent_owner_exclusions/0`; `#/direct_source_bindings/3` (`PUB-04`), `#/direct_source_bindings/4` (`PUB-05`), `#/direct_source_bindings/5` (`PUB-06`).

## 5. Runtime evidence is a chain, not a success flag

The current mechanism is an evidence-locked handshake:

1. **Preflight** validates route shape, authorization, and host operations, then persists only the first eligible wave. It records zero spawn attempts.
2. A **persisted action** binds the exact run, wave, role, capability, scope, and inputs for one job.
3. `action_attempted` is recorded before the native host call. The return becomes either `host_spawn_returned` with a real agent ID or `host_spawn_failed`.
4. Wait registration and `wait_attempted` precede mailbox waiting. A known result becomes terminal observation; unresolved work follows the typed timeout and interrupt path.
5. Logical close accounts for the worker. It does not admit a receipt.
6. Exact expected receipts undergo schema, identity, and digest admission. A structurally valid non-pass receipt is still evidence and blocks dependents.
7. `receipt_joined` admits the result into reduction; `gate_decided` opens or blocks the transition.
8. Even after a passed gate, dependent actions require a fresh exact persisted wave plan before spawn.
9. Terminal closeout separately binds the bounded history and result ceiling.

Evidence: `receipts/synthesis.json#/synthesis/runtime_sequence`; `research.md:1073-1284`; `recovery-003/receipts/evidence-closure-recovery-003.json#/evidence_rows/7` (`C08`).

The evidence types must not be substituted for one another:

| Evidence says | It does not yet say |
|---|---|
| Route validated | Route authorized or executed. |
| Human confirmed | Dispatch registered or running. |
| Preflight passed | A spawn was attempted. |
| Spawn returned | The agent completed. |
| Agent terminal | The agent was logically closed or its receipt admitted. |
| Receipt exists | Receipt admitted or joined. |
| Receipt joined | Exact receipt bytes are bound by the event alone, or the gate passed. |
| Gate passed | A dependent wave executed. |
| Findings audited | Claims became semantic or canonical authority. |
| Dispatch closed | Artifact was promoted, published, deployed, or accepted in production. |

Sequence numbers support recorded causal order, not wall-clock time. The causal stream does not by itself prove receipt contents or semantic truth; exact receipt hashes live in separate admission evidence. Residue may explain a failure but cannot reconstruct a missing causal event.

Evidence: `receipts/synthesis.json#/synthesis/evidence_distinctions`, `#/synthesis/non_implications`; `research.md:1285-1552`.

## 6. Failure is safest when the missing transition remains missing

The research corpus repeatedly supports one fail-closed rule: preserve what was directly evidenced, fabricate nothing downstream, and recover through a separately bounded route.

- If a dependent-wave plan is missing, the next worker must not start.
- If a worker never started, no receipt may be invented for it.
- If only part of a wave started, every started sibling must be accounted for or interrupted, the wave must close blocked, and earlier completed evidence must retain its narrower status.
- A schema-incomplete causal stream can block orchestration proof without erasing a separately supported research result.
- A stale Inventory projection cannot outrank current direct receipts.
- Historical prose and initial state snapshots must retain their original time layer rather than being rewritten with later knowledge.
- A final gate or complete reducer state is not terminal closeout.

Evidence: `research.md:1553-1799`; `receipts/synthesis.json#/synthesis/failure_atlas`.

### What the earlier recoveries actually prove

**Recovery 001 is a fail-closed partial recovery, not a complete success witness.** It preserved the ten-explorer substrate, produced the cited synthesis and two differentiated reviewer returns, then blocked because the definitional reviewer’s first-read order violated the independence contract. Evidence closure, writer, auditor, and later composition remained unopened.

Evidence: `recovery-001/receipts/dispatch-closeout.json#/status`, `#/blocker`, `#/execution`, `#/claim_ceiling`.

**Recovery 002 is also a fail-closed partial recovery, not a complete success witness.** It preserved a clean synthesis-only definitional freeze, but the comparator correctly withheld freeze admission because no external parent-owned exact-byte digest binding had been supplied. Precedent recheck, evidence closure, writer, auditor, and later composition remained unopened.

Evidence: `recovery-002/receipts/dispatch-closeout.json#/status`, `#/blocker`, `#/execution`, `#/claim_ceiling`.

**Recovery 003 repairs those governance mechanics but is not yet a complete success witness.** Exact external freeze admission passed, the recovered definitional distinctions survived, the fresh precedent recheck passed all six defects, and parent evidence closure admitted this writer. Audit, parent disposition, Orchestrate closeout, and dispatch-ledger close are still downstream.

Evidence: `recovery-003/receipts/skeptic-definitional-recovered.json#/binding_admission`, `#/comparison_summary`; `recovery-003/receipts/skeptic-precedent-recheck.json#/review_verdict`, `#/defect_reviews`; `recovery-003/receipts/evidence-closure-recovery-003.json#/status`, `#/open_obligations`.

This preserves the non-vacuity `KILL`: the corpus offers useful partial and fail-closed examples, but it does not admit the synthesis’s worked example as one complete, evidence-backed successful dispatch witness.

Evidence: `receipts/skeptic-non-vacuity.json#/review`, `recovery-003/receipts/evidence-closure-recovery-003.json#/evidence_rows/8` (`C09`), `#/evidence_rows/9` (`C10`).

## 7. Inventory and adjacent capabilities stay in their lanes

Inventory is a discovery-oriented knowledge read model. It can point toward sources, but it cannot authorize a dispatch, prove native execution, establish semantic truth, or promote meaning. The selected snapshot for this research is stale relative to direct receipts, so both time layers must remain explicit and direct evidence controls the claim.

The adjacent ownership map is equally important:

- **Craft** owns project work-ledger state, not native dispatch run state or registration.
- **Task Session** owns one bounded task or SWU’s execution semantics, not multi-agent scheduling.
- **Continuation Router** owns one explicit next-owner hop, not recursive or parallel orchestration.
- **Signal Observer** owns post-run behavior signals; telemetry is not dispatch or promotion authority.
- **Whisper** owns downstream editorial composition after an accepted research handoff; it does not accept the research, prove runtime execution, or authorize publication.

Evidence: `recovery-003/receipts/evidence-closure-recovery-003.json#/evidence_rows/6` (`C07`); `recovery-002/precedent-repair-packet.json#/component_status_matrix/8`, `#/component_status_matrix/9`, `#/component_status_matrix/10`, `#/component_status_matrix/11`, `#/component_status_matrix/12`, `#/component_status_matrix/13`, `#/adjacent_owner_exclusions`; `#/direct_source_bindings/6` (`PUB-07`), `#/direct_source_bindings/7` (`PUB-08`), `#/direct_source_bindings/8` (`PUB-09`), `#/direct_source_bindings/9` (`PUB-10`), `#/direct_source_bindings/10` (`PUB-11`), `#/direct_source_bindings/11` (`PUB-12`).

## 8. How the eventual beginner guide should teach this

The strongest pedagogical route is need-before-name:

1. Begin with one familiar question and ask whether one helper is enough.
2. Introduce a dispatch only when independent viewpoints or dependent stages create a real need.
3. Use one controlled-relay example to show the input, each owner transition, the evidence produced, and what remains unproved.
4. Explain the exact sheet as a call sheet and persisted actions as work tickets, while stating that neither proves permission or execution.
5. Trace one action through persisted ticket, attempt, host return, wait, terminal observation, logical close, receipt admission, join, and gate.
6. At every transition, state both what changed and what did not follow.
7. Use the earlier recoveries as fail-closed counterexamples, not as a complete success witness.
8. End by asking the reader to identify the last directly evidenced transition, the next owner, and the remaining residue.

The relay analogy has a hard break point: passing a baton does not prove the message carried by the baton is true. A gate can authorize the next move without establishing semantic correctness.

Only two visuals are necessary in the eventual guide: one lifecycle flow and one compact “evidence says / does not yet say” table. A catalogue-first opening or a large state vector would hide the practical mechanism.

Evidence: `research.md:190-379`; `research.md:1804-1955`; `receipts/synthesis.json#/synthesis/worked_example`; `receipts/skeptic-non-vacuity.json#/review/required_repairs`.

This is a pedagogical recommendation, not comprehension evidence. No human comprehension test or Whisper delivery experiment has occurred.

Evidence: `receipts/synthesis.json#/residue`; `recovery-003/receipts/evidence-closure-recovery-003.json#/open_obligations`.

## 9. Public-retell boundary

A later portable public Arcanum retell may use only these admitted concepts:

- Subagent Strategy’s dispatch trigger, material confirmation, and lifecycle boundary.
- Dispatch Spec as a draft route-shape validator that does not execute.
- Orchestrate preflight, persisted actions, native spawn/wait/join/gate, causal evidence, and fail-closed partial-wave recovery.
- Inventory as a discovery read model rather than proof.
- Craft, Task Session, Continuation Router, and Signal Observer as adjacent owners with distinct scopes.
- Whisper’s need-before-name, earned progression, transformed ending, and retell-chain guidance.
- Public normative evidence-state terms that actually exist in Arcanum Definitions.
- Sigil, spell, and capability only as descriptive README vocabulary, with the formal-definition gap stated.

It must exclude:

- DomainSpec or Saturn architecture, definitions, prose, status, or claims.
- Private authority-spine material.
- Repository-local strategy, registrar, research, agent-pool, ledger, and constitution prose.
- Telemetry paths or row contents.
- Development-run artifacts, receipt paths, run or event identifiers, hashes, private identities, emails, and product details.
- Any assertion of canonical promotion, publication, release, deployment, production, or semantic authority.

This repository-local findings file may cite private evidence internally. That does not convert the private source into public Arcanum authority and does not authorize copying it into `arcanum/`.

Evidence: `recovery-002/precedent-repair-packet.json#/public_arcanum_export_allowlist`; `recovery-003/receipts/skeptic-precedent-recheck.json#/defect_reviews/5`; `recovery-003/receipts/evidence-closure-recovery-003.json#/public_arcanum_export_allowlist`, `#/evidence_rows/11` (`C12`).

## 10. Open obligations and final claim ceiling

The following remain unproved or incomplete after this writer action:

- This exact `findings.md` has not yet been audited.
- The parent has not issued the final research disposition.
- Recovery 003 has not yet received terminal Orchestrate closeout or its paired dispatch-ledger close row.
- Craft state was not changed or closed by this dispatch.
- Focused runtime tests were inspected by an explorer but not executed; test presence is regression intent, not a fresh pass.
- The deterministic coordinator does not itself enforce ambient host capacity.
- The successful terminal-closeout edge remains parent-owned in the inspected runtime contract.
- The selected Inventory snapshot remains stale relative to direct receipts.
- No human comprehension test or Whisper delivery experiment has occurred.
- The formal Arcanum definition gap for sigil, spell, and capability remains open.
- No final beginner learning guide has been composed.
- No canonical authority, promotion, publication, release, deployment, production, or semantic-truth status follows from these findings or from a later audit.

Evidence: `receipts/synthesis.json#/synthesis/contradictions_and_residue`, `#/residue`; `research.md:1073-1284`; `recovery-003/receipts/evidence-closure-recovery-003.json#/open_obligations`, `#/claim_ceiling`, `#/evidence_rows/9` (`C10`), `#/evidence_rows/12` (`C13`).

Whisper handoff: compose a repository-local beginner learning guide from these audited findings using only the admitted public-retell allowlist; preserve all KILL, deferred, privacy, and authority ceilings.
