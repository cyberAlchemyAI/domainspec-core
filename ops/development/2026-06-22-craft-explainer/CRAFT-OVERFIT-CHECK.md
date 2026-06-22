# Craft ↔ Framework Over-Fit Check

> **Role: over-fit guard.** For each grand-framework concept someone might attach to Craft,
> judge whether Craft *genuinely instantiates* it (FAIR) or whether the connection is
> rhetorical / aspirational / forced. Sources: `arcanum/arcana/craft/{SKILL,README,ARCHITECTURE}.md`
> and `projects/framework-unification/CONCEPT-MAP.md`.

## What Craft actually is (the honest baseline)

A single, project-local, file-backed YAML ledger (`.craft/ledger.yml`) with a derived human
view (`CRAFT.md`). It records contexts, blockers, enablers, decisions, gaps, local definitions,
next moves, and recomposition, each as a typed row with a stable ID and links. Its own docs are
deliberately modest: **"intentionally small… does not yet provide an automated command runner or
full ledger renderer"** — no built validator, no generator, no CLI. `validate` and the
pass/flag/block verdict are a *method contract an operator follows*, not shipped tooling.

## Verdict table

| # | Framework concept (CONCEPT-MAP) | Verdict | Why |
|---|---|---|---|
| 1 | **Residue** — "what wasn't preserved, tracked" (epistemology mechanism / I3) | **FAIR (narrow)** | Craft has first-class `residue` in its output contract, `gaps` rows, and a rule that recomposition residue must surface. It is *one concrete place the system records residue* — but only project-local prose-grade residue (the CONCEPT-MAP's "now" tier), not the typed-signal or Lean tiers. Fair only if scoped to that tier. |
| 2 | **Claim ≤ proof gate** (I4 / epistemology) | **FORCED** | Craft's `validate` returns pass/flag/block and its non-use rules ("route-shape ≠ execution evidence", "recomposition needs evidence") are *evidence-discipline conventions*. But I4 is specifically a mechanical `grade: observed ⇒ non-null proof` check; CONCEPT-MAP marks it "designed (Lean-deferred)". Craft ships no such checker. Saying "Craft implements claim≤proof" oversells an honest discipline rule as a gate. |
| 3 | **Recursive self-application** (I9 — "every stage is the same process at a different altitude") | **PARTLY FAIR** | Craft genuinely nests: child contexts with their own blockers/decisions that must `recompose` into a parent. That *is* same-shape-at-different-altitude for ledger state. But I9 is about the **pipeline running on itself** (research refines a define). Craft is not a pipeline stage, so "Craft realizes recursive self-application" borrows a pipeline invariant for what is really recursive *containment*. Fair as "recursive ledger"; forced as "the I9 mechanism". |
| 4 | **Node envelope** (typed identity + intent + connections + body + residue + epistemic) | **PARTLY FAIR / mostly FORCED** | Craft rows do have typed identity (ID + family), links (`connections`), and residue. Real overlap. But the envelope is a *single uniform schema over ~15 pipeline artifacts* with an `epistemic.grade/proof` slice; Craft rows are heterogeneous per-family schemas with no grade/proof field. CONCEPT-MAP itself says the envelope is "designed, not built". Claiming "Craft implements the node envelope" conflates a family-row ledger with an unbuilt unifying schema. |
| 5 | **Append-only signal ledger** (I8 / communication mechanism, indexed by `dispatch_id`) | **FORCED** | Craft preserves description history and is durable, but it explicitly *mutates* rows (refine_blocker, decide, recompose updates). It is not an append-only monotonic signal stream, and it has no `dispatch_id` / signal envelope. Different mechanism. |
| 6 | **Single owner** (I5 — each term one canonical home) | **FORCED (inverted)** | Craft's hard rule is the *opposite*: "local definitions do **not** become canonical definitions." Craft deliberately holds *non-authoritative, project-local candidates* and routes canonicalization elsewhere. So Craft *respects* I5 by abstaining — it does not *realize* the single-owner mechanism. |
| 7 | **Connection integrity** (I2 — every link resolves) | **FAIR (aspirational-in-Craft)** | Craft's linking-and-indexing contract requires valid ID references and `links {label,target,kind}`. The *intent* matches I2 exactly. But CONCEPT-MAP assigns enforcement to `review`, and Craft ships no validator to enforce non-dangling links. Fair as a stated contract; not as enforced. |
| 8 | **Two-axis model / pipeline stage** | **FORCED** | Craft is not a pipeline stage (define→…→verify) nor one of the three vertical mechanisms. It is an orthogonal local-memory sigil. It does not belong on either axis; placing it there is category error. |
| 9 | **"Craft is the system's epistemology layer"** | **FORCED (overclaim)** | The epistemology layer is residue + claim≤proof across *every node in the engine*. Craft is one local ledger that *records* residue for the work in front of it. Calling it "the epistemology layer" promotes a small honest tool to a system-wide mechanism it does not implement. |

## The pattern in the forced cases

Every FORCED mapping shares one move: the framework concept names a **mechanical, system-wide,
often-unbuilt enforcement** (a gate, an append-only stream, a unifying schema, a canonical
authority), while Craft offers a **local, convention-level, operator-followed discipline** over
one ledger. The overlap is real at the level of *vocabulary and intent* and absent at the level
of *mechanism and scope*. Craft's own status line ("intentionally small… no command runner")
is the tell: a tool that ships no enforcement cannot *be* an enforcement mechanism.

## Recommendation for the public page

Connect Craft to the bigger picture as a **concrete instance of two mechanisms, scoped honestly**,
never as a layer or invariant owner:

- **SAFE:** "Craft is one concrete place the system tracks **residue** and **gaps** — at the
  project-local, prose-grade tier." (maps #1, the honest part of #3)
- **SAFE:** "Craft keeps recursive work visible: nested contexts that must **recompose** into
  their parent with evidence — a recursive *ledger*, mirroring the engine's recursive shape."
  (the fair reading of #3, without claiming I9)
- **SAFE:** "Craft's rows are typed, ID'd, and linked — the same 'typed, connected objects'
  spirit as the node envelope, applied to local memory." (the fair part of #4/#7, as *spirit*)
- **SAFE (and load-bearing):** "Craft deliberately holds **non-canonical** local definitions and
  routes authority elsewhere — it respects single-owner by *not* claiming ownership." (#6 as a
  boundary, which is a strength to advertise, not hide)

- **AVOID:** "Craft IS the residue mechanism / the epistemology layer." (over-scopes #1/#9)
- **AVOID:** "Craft implements claim≤proof / the node envelope / append-only signals." (#2/#4/#5
  name unbuilt or different mechanisms)
- **AVOID:** placing Craft on the two-axis map as a stage or a mechanism. (#8)

One-line framing that stays honest: **"Craft is the local-memory sigil where a project's residue,
nested contexts, and typed decisions live — a small, file-backed instance of the system's
residue-and-provenance discipline, not the system's enforcement engine."**
