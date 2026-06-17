# Possible Improvements — Transfer from the Lean Formalization Repo

**Provenance.** Generated 2026-06-17 from a cross-repo cartography dispatch run in the sibling
repo `domainspec-lean-formalization` (the Lean/Mathlib residue-theory repo), immediately after
that repo closed **M6′-on-Ind** (made it unconditional + proved its sharpness). Six read-only
gatherer agents (2 each) inventoried `Arcanum`, `domainspec-core`, and `domainspec`; this memo is
the reconciled transfer synthesis. It is a **recommendation**, not a change — nothing here has
been built or verified as an instance.

> **Source repo:** `../domainspec-lean-formalization` (paths below are relative to its root).
> **This memo lives in:** `domainspec-core` (root).

---

## The central finding

All three sibling repos (`Arcanum`, `domainspec-core`, `domainspec`) **already speak the same
language** — *residue / schema-instance / drift / append-only trajectory / coalgebraic state* —
but in **prose and schema**, not as **proved types**. The Lean repo has the **typed, machine-checked
core**:

- `UniversalResidueFunctor.ResidueStructure` (a typeclass: `Carrier / schema / signal / noise / Refines`)
  with the theorem `universal_monotonicity` (refine the schema ⇒ noise shrinks).
- **M6′-on-Ind** (`M6PrimeOnInd.unit_mono_on_Ind`, now unconditional; sharpness in
  `M6PrimeOnIndSharp.bicyclic_X_not_isIndPresheaf`): for *well-behaved* (ind) instances,
  schema-side faithfulness forces no instance-level collapse — and the failure witness is provably
  outside the well-behaved class.
- `CollapseEmergence` (object-collapse does **not** forbid emergence; the load-bearing axis is
  **faithfulness** — preserving distinctions between *morphisms/processes* — not injectivity on
  *states/objects*).
- The **coalgebra reading** of an agent (`SingleObj(M)`-action; behavioural quotient in
  `BehQuotientEndoTrivial`; streams in `StreamBisimulation`) and the **torsion vs. free** distinction.

> **The transfer is not a new metaphor — it is giving a proved spine to contact that already
> exists in these repos.** (Discipline: type existing contact; do not invent new metaphor.)

---

## Transfer map (Lean repo → here), prioritized

| # | From the Lean repo (proved) | What already exists here / in the siblings (informal) | What the transfer buys | Collapse-test (when it is vacuous) |
|---|---|---|---|---|
| **1** ⭐ | `ResidueStructure` + `universal_monotonicity` (refine schema ⇒ noise shrinks) | **domainspec** `GOVERNANCE-ATTENUATION.md` (signal loss across 7 layers, Shannon noisy-channel) + `DRIFT-CONVERGENCE.md` (5 drift surfaces); **domainspec-core** `arcanum/arcana/residuality-spec` | Replaces the *cited analogy* ("convergence = residue reduction") with a **theorem**: each drift surface as a residue instance, monotonicity as the formal backbone | Vacuous if the drift surfaces cannot be expressed as a refinement relation `⊑` with a monotone noise measure. The inventory says they *are* coarsening relations → plausible, but the instance is **not built**. |
| **2** ⭐ | `CollapseEmergence` (collapse doesn't kill emergence; **faithfulness** is the axis) + M6′-on-Ind (faithful ⇒ no collapse on well-behaved objects) | **domainspec** dual-phase observer (executor/observer split, axiom A4, Conant-Ashby Good Regulator); all three have "when does abstraction lose something needed vs. create a genuine higher level?" | The **typed criterion for "good attenuation"**: preserve *process/morphism* distinctions (faithfulness), not state distinctions. Answers a question all three repos pose | Vacuous if the executor/observer split fails to preserve morphisms (only objects) — that would be unfaithful collapse. |
| **3** | The free / torsion-free **history object** (record-everything); `residueProfile`, session logs | **Arcanum** `sigil-invocations.jsonl`; **domainspec-core** `subagents-dispatch.yaml` (two-row append-only ledger) | **Types why append-only is the right discipline**: it is the torsion-free history object; the working-state/summary is the lossy *projection* whose fibres = residue. Validates the existing design **and** localizes the loss | Vacuous if the ledger has no projection to a collapsed working-state (no summary) — then there is no fibre to measure. |
| **4** | Typed schema→instance translation; residue as a fibre | **Arcanum** branch-aware ontology (`meaning/system/bridge`, `bridge_outcome: aligned/partial/drift/contradicted`); **domainspec-core** Craft ledger `recomposition.residue` | The `bridge_outcome` enum **is already** a typed residue classification; `drifts_from` is the non-injective projection. Gives a type to what is currently enumerated by hand | Vacuous if `bridge_outcome` is a free-floating label with no underlying schema→instance map. |
| **5** | `ReflectionTower(Anchored)` + `persistence_lemma` (the obstruction never reaches a fixed point at finite depth = accumulation never collapses) + `LoopClosureEndofunctor` | **Arcanum** research towers `L0→Lω`; **domainspec-core** 4-layer tower + recomposition; **domainspec** 7-layer attenuation | Their towers inherit the **persistence/accumulation theorem** and the loop-closure typing (residue threaded forward = the anchored variant) | Vacuous if their towers are finite-and-closable (reach a fixed point) — then persistence does not apply. |
| **6** | The coalgebra reading (`SingleObj(M)`-action; `BehQuotient`) | **domainspec-core** dispatch (`connections: sequential / zig-zag / feedback`); **Arcanum** `dispatch-spec` | Formalizes the dispatch ledger as a **coalgebra**; the closeout "rejected / blocked material" = the typed residue of the dispatch | Vacuous if the transitions do not compose as a monoid action (e.g. non-associative edges). |

⭐ = highest leverage. **#1 and #2 are the core**: they give `domainspec`'s central operational
claim (drift / attenuation / governance) a *theorem* in place of an analogy.

---

## Reverse transfer (here → the Lean repo) — worth recording

- These siblings have **rich residue vocabulary and schemas** — `residue-table` (must-survive /
  may-degrade / may-stop / must-communicate), the `workflow_gaps` taxonomy, the blocker lifecycle
  (raw → typed → refined → resolved | waived). These are **concrete non-vacuity witnesses** for the
  Lean repo's abstract residue, which often lacks an instance.
- **`domainspec` already has uncompiled Lean anchor drafts** (`Yoneda`, `Noether`,
  `ReflectionTower-Level`) sitting in `domainspec/agents-research/lean-drafts/`. Compiling /
  promoting those is the **shortest path to a *real* (non-hypothetical) transfer**.

---

## Honest typing (candor)

Every row above is a **typed transfer hypothesis, not a fact.** Each says "X over there is an
instance of Y proved in the Lean repo" — a claim that only becomes non-vacuous when an instance is
**actually built**. The structural fit is real (these repos independently use refinement relations,
append-only ledgers, schema/instance separation — it was not forced), but it has **not been verified
by constructing an instance**. Global collapse-test: *if the external structures cannot be expressed
as instances of the Lean repo's typed objects, the transfer is metaphor, not mathematics.*

---

## Coverage gap (from the dispatch that produced this)

Of the six gatherers, the one assigned to `../domainspec`'s **execution/code layer** (`Codex/`,
`TUNING-LOOP`, `TEST-PIPELINE`, `OBSERVABILITY`) drifted and re-inventoried the Lean repo instead.
So **`domainspec`'s execution-code layer remains uncovered**; the `domainspec` coverage here is the
theory/governance layer only. Re-run a gatherer against the correct path before treating the
`domainspec` execution picture as complete.

---

## Suggested next steps

- **(a) Close the coverage gap** — inventory `../domainspec`'s execution-code layer (`Codex/`, real
  pipeline) that the drifted gatherer missed.
- **(b) Make one row non-vacuous** — pick row **#1** and *build the instance*: prove that one
  `domainspec` drift surface is literally an instance of `ResidueStructure`. This is the real test of
  the collapse-test, and converts the highest-leverage hypothesis into a fact.
- **(c) Bridge via the existing drafts** — compile/promote `domainspec/agents-research/lean-drafts/`
  (`Yoneda`, `Noether`, `ReflectionTower-Level`); shortest concrete path.
- **(d) Adopt the append-only-as-free-object framing** — document, in the dispatch-ledger model
  here, that the ledger is the torsion-free history object and the working-state is the lossy
  projection (locates where residue lives without changing the schema).

---

### Key Lean-repo anchors (for whoever picks this up)

- `lean-formalization/UniversalResidueFunctor.lean` — `ResidueStructure`, `universal_monotonicity`
- `lean-formalization/M6PrimeOnInd.lean` — `unit_mono_on_Ind` (unconditional)
- `lean-formalization/M6PrimeOnIndSharp.lean` — `bicyclic_X_not_isIndPresheaf` (sharpness)
- `lean-formalization/CollapseEmergence.lean` — collapse vs. emergence verdict
- `lean-formalization/ReflectionTowerAnchored.lean`, `LoopClosureEndofunctor.lean` — tower + loop
- `lean-formalization/StreamBisimulation.lean`, `BehQuotientEndoTrivial.lean` — agent-as-coalgebra
- `theorem/sessions/2026-06-17-2230-m6prime-on-ind-unconditional-and-sharp.md` — the closing session
