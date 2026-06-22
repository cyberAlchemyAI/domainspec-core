# Governed Definitions

The load-bearing terms that later artifacts (distill, bridge decisions, review) depend on. Each
keeps formal expression + intuition + anti-misuse together. **Local-only.**

---

## DEF-1 · MTNG (Modal Tonal Nodal Graph)

- **Formal (primary-source, `01` §1, §5).** A workflow-shaping engine over the relation
  `Signal → Mode → Node → Validator → Synthesis`, governed by a single boundary rule: *branch
  only when a contract boundary changes*. It is a **graph, not a tree** — signals branch and may
  recombine (Analog6 §2.3).
- **Intuition.** Take one messy report; split it only where the *kind of work* changes; process
  each piece under an explicit contract; validate each; recombine into one auditable artifact
  that still shows what failed.
- **Anti-misuse.** MTNG is a *proposal*, not a shipped system. V1 is explicitly **not** a live
  runtime orchestrator. Do not describe it as controlling agents or memory.

---

## DEF-2 · Node contract

- **Formal (primary-source, `01` §14).** A node declares: `accepts`, `rejects`,
  `allowed_context`, `blocked_context`, `output_artifact{type,path}`, `validator[]`, `state ∈
  {proposed,processing,closed}`, `closed_result ∈ {passed,partial,failed,rejected,superseded,
  needs_human}`, `merge target`, `contribution_hooks[]`.
- **Intuition.** A node is a *promise with edges*: it says what it will and won't take in, what
  it must emit, and how to tell if it succeeded — so delegation is inspectable by construction.
- **Anti-misuse.** A node with no validator, or with `accepts`/`rejects` left implicit, is not a
  valid node. The contract is the point; without it MTNG degrades to a flat summarizer.

---

## DEF-3 · Branch boundary (the V1 binary trigger set)

- **Formal (primary-source, `01` §12).** Create a branch iff one of: output-artifact-type
  changes · validation-contract changes · required-tool changes · context-boundary changes ·
  memory-treatment changes · contribution-record-type changes · safety/authority boundary
  appears · explicit human/operator split. Otherwise **do not branch** (fast path, `01` §13).
- **Intuition.** Fan out only on a *named, structural* reason — never on sentiment, text length,
  or model vibe. This is what keeps the graph from exploding.
- **Anti-misuse.** The deferred numeric *Branch Pressure Score* (v1) is **not** part of V1; do
  not reintroduce weights. Conversely, do not branch "to be safe" — over-branching is a named
  risk (`01` §26).

---

## DEF-4 · Validator (as misrouting detector)

- **Formal (primary-source, `01` §5, §15).** A structural check answering "did this node
  produce the *right kind* of artifact?" A failure may emit `possible_reroute`. Reroute is
  bounded: 1 reroute/signal, 1 validator failure/node; the 2nd failure writes uncertainty to the
  audit log and stops (`01` §15).
- **Intuition.** The validator is both the quality gate *and* the evidence that a signal was
  routed to the wrong mode — a failed `provider.routing` node with no endpoint evidence suggests
  the work was actually `ux.affordance`.
- **Anti-misuse.** Do not treat a validator as a numeric quality score, and do not let reroute
  run unbounded — oscillation is the named failure (Analog6 §6.2, Gemini §3).

---

## DEF-5 · Synthesis (non-hiding recombination)

- **Formal (primary-source, `01` §17).** A synthesis artifact may include passed nodes, partial
  nodes *with explicit missing-info*, and failed/rejected/blocked nodes *as status notes only*.
  Conflicts are recorded `unresolved`; no winner is chosen without evidence; no implementation
  request is generated from a conflict.
- **Intuition.** The merged artifact must read like an honest dossier, not a confident
  paragraph: every gap and disagreement survives the merge.
- **Anti-misuse.** Synthesis that drops failed nodes or flattens a conflict into smooth prose
  violates the contract (P10 claim ≤ proof analogue) and the OKF anti-flattening rule (`01` §20).

---

## DEF-6 · Contribution record (structure without valuation)

- **Formal (primary-source, `01` §19).** A typed attribution
  `{signal_id, branch_node_id, contributor_ref, contribution_type[], artifact_ref,
  validator_status, status}`. V1 must **not** decide compensation, ownership, voting power,
  tokenization, governance weight, economic conversion, or ranking.
- **Intuition.** Record *that* triage/reproduction/review/synthesis happened and by whom; leave
  *what it's worth* to a separate future governance layer.
- **Anti-misuse.** Adding any weight/score makes it a valuation system — explicitly out of scope.

---

## DEF-7 · Phase 0 integration mapping

- **Formal (primary-source, `01` §10; gap admitted in `05`).** A mandatory pre-build pass that
  maps each MTNG concept (Signal/Mode/Node/Branch/Synthesis/Memory/Contribution/Inspection) onto
  existing ResonantOS components, under the assumption *MTNG augments, does not replace*.
- **Intuition.** Don't build until you know where each piece sits relative to Guardian Core, the
  event bus, the Living Archive, etc.
- **Anti-misuse.** Phase 0 is **unperformed** (`05`). Any V1 commitment that assumes a mapping
  exists is premature. This is the single largest open dependency (R-INT).
