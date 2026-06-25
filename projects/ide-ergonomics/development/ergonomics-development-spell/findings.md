---
tags: [ide, ergonomics, spell, spellcraft, dialectic, reconciliation, cyberalchemy-v2, redirect]
node_type: findings
is_session: false
layer: workflow
nature: design-reconciliation
status: hardened
created: 2026-06-24
craft_scope: projects/ide-ergonomics/.craft/
craft_context: CTX-ERGO-SPELL-ROOT
supersedes_input: REQUIREMENTS.md (the proposed net-new 8-phase `ergonomics-development` engine)
method: design-dialectic — Lane V (validate) × Lane A (attack), both ran robot_talks, CONVERGED on REDIRECT
---

# Findings: `ergonomics-development` spell — reconciled (hardened) design

This reconciles a two-lane design dialectic over the proposed `ergonomics-development`
spell (the artifact under review = `REQUIREMENTS.md` in this folder). Lane V validated;
Lane A attacked. Both ran `robot_talks` and **converged on REDIRECT**. Below is the
hardened design — settled points are not re-opened; the one genuine residual disagreement
is preserved as a noted resolution.

Claim ≤ proof throughout: every binding and every break is file-cited.

---

## 1. VERDICT: REDIRECT (not redesign, not author-as-proposed)

**Do not author** the proposed net-new, 8-phase `ergonomics-development` engine
(REQUIREMENTS.md "Proposed phases" table, phases 0–7 + adversarial lane).

**Instead author** the `ide-action-surface` discipline's **step-2 spell**,
`ide-assisted-arcanum-routing` — **build-from-owned** (built from the discipline + the
validated dispatch contract, not net-new), **gated on step-1 discipline formalization**.

The spell already exists as a candidate:
`projects/ide-ergonomics/SPELL-IDE-ASSISTED-ARCANUM-ROUTING.md`
(`Canonical ID: ide-assisted-arcanum-routing`, `Lifecycle owner if pursued: spellcraft`).
The discipline already exists as a candidate:
`projects/ide-ergonomics/DISCIPLINE-CANDIDATE.md`
("Discipline Candidate: IDE Action Surface", `Steward: Discipline Governance`).

So the REDIRECT does not invent anything — it **points the requirements at two owned
candidates already in the repo** and rescopes them to a hardened shape.

**Movement recorded (claim ≤ proof on the dialectic itself):**

- Lane A collapsed **reject → redirect**: its initial verdict was REJECT/REDESIGN on
  five flaws; its final verdict downgraded V1/V2/V3 to *rename/rescope grounds* and
  conceded the HMI half of V5, holding only five must-fix conditions — i.e. the design
  is salvageable by redirection, not by rejection.
- Lane V conceded **V5, V4a, V4b, V1** fully (initial "bindable + owner-consistent"
  position did not survive on executable bindings).
- Lane V **refuted V2** (the "just rename self-assembling-ergonomics" claim) as a
  category error — this is the single residual disagreement, resolved in §3.

---

## 2. What VALIDATED (Lane V) — the bound concept set that survived

Lane V's surviving contribution: the spell is a **pure Spellcraft composition** whose
every capability maps to an existing governing CAV2 authority — confirmed to exist on
disk. The composition itself (sigils compose, do not re-define) is sound.

| Capability the spell composes | Governing CAV2 authority | Confirmed at |
| --- | --- | --- |
| Authority-kind closure / default-deny | `CAV2-D49` Closed Authority-Kind Enumeration | `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md:3245` |
| Authority promotion lifecycle | `CAV2-D48` (referenced by D49) | DEFINITIONS.md (D49 cites D48) |
| Interface evidence boundary | `CAV2-C15` Interface Evidence Boundary | `cyberAlchemy-v2/authority/constitutions/STABLE-REPOSITORY-CONSTITUTION.md:330` |
| UX/UI knowledge governance | `CAV2-D45` UX/UI Knowledge Governance | DEFINITIONS.md:2946 |
| Experience evidence lifecycle | `CAV2-D46` Experience Evidence Lifecycle | DEFINITIONS.md:3030 |
| Interface evidence boundary (def) | `CAV2-D47` Interface Evidence Boundary | DEFINITIONS.md:3107 |
| Gate ownership / circular fence | `PRODUCT-VIEW.md` owner / governance review | `projects/ide-ergonomics/UNIFIED-PRODUCT-VIEW.md:156–161` |

**Strongest proven point (held by both lanes): HMI is served-not-promoted.**
`grep -i "HMI"` over `DEFINITIONS.md` returns **0 occurrences** — HMI
(`CAV2-CAND-HMI-001`) is a *candidate*, not a promoted definition. The spell therefore
**produces HMI proof surface; it does not promote HMI**. This is correct and final; the
spell must keep this fence.

What V validated was **internal consistency + owner-consistency**, NOT
**executable-correctness**. That gap is the live residue in §6.

---

## 3. What the ATTACK broke (Lane A) + resolution

Five must-fix conditions survived to Lane A's final verdict, each file-cited.

### MF-1 — Forbid coordinate-gate ownership [CRITICAL]
The proposed phase 7 ("Admit … through the coordinate-admission gate",
REQUIREMENTS.md) lets the spell **own/route** the admission gate. This is **circular**:
the spell IS the governed engine behind `self-assembling-ergonomics`, and per
`UNIFIED-PRODUCT-VIEW.md:156–161` that loop is **explicitly fenced** —
*"routing model-level admission through it would be circular. The loop builds primitives;
it cannot admit coordinates to the model that governs it."* The gate is owned by the
**`PRODUCT-VIEW.md` owner / a governance review — not the loop**.
**Fix:** the spell **produces admission-PROOF** (fixture / receipt / pre-registered
verdict) and **hands it to the owner-held gate**. It never owns or routes the gate. The
"Admit" phase is **deleted** from the spell.

### MF-2 — Declare the spell's authority-kind; make default-deny explicit [HIGH]
A spell-as-authority-bearing-artifact is an **unenumerated authority kind** under
`CAV2-D49` (DEFINITIONS.md:3245): *"An artifact whose kind is not in that enumeration may
not acquire or exercise authority — it defaults to blocked pending an owner decision."*
**Fix:** route the authority-kind acknowledgement through **`decision-gate` +
`constitution-governance`**, and add the explicit default-deny clause (§4). Resolution:
the spell **promotes nothing**; the spell-as-composition is fine *because* it claims no
authority of its own — every output's authority comes from its owner's gate.

### MF-3 — Fix the D46 mis-binding; route the absent "ergonomics" definition [MEDIUM]
REQUIREMENTS.md binds *"`CAV2-D46` (UI/experience)"* and *"The ergonomics/experience
definition … `CAV2-D46` (UI/experience)"*. **D46 is NOT "UI/experience"** — it is
**"Experience Evidence Lifecycle"** (DEFINITIONS.md:3030), a *lifecycle*, not a
term-definition for the UX surface. And **no "ergonomics" definition exists**:
`grep -i "ergonomic"` over DEFINITIONS.md = **0 occurrences**.
**Fix:** drop "D46-as-UI"; bind **D45 + D46 + D47 + C15 as the governance cluster** (the
correct experience-evidence governance surface), and route the undefined term
**"ergonomics" to `definitions-governance`** as residue.

### MF-4 — Name it build-from-owned, the discipline's step-2, sequenced after step-1 [MEDIUM]
The proposed identity ("net-new `ergonomics-development` engine", REQUIREMENTS.md) is the
**wrong problem framing** — the recurring practice is already owned by the
`ide-action-surface` **discipline candidate** (DISCIPLINE-CANDIDATE.md). The spell is its
**step-2**, `ide-assisted-arcanum-routing` (the existing candidate). It is
**build-from-owned** and **blocked until step-1 (discipline formalization) completes**.
**Fix:** §5 sequencing.

### MF-5 — Thin the phase set [MEDIUM]
The 8-phase map **re-narrates** workflows already owned elsewhere. Phase 2 re-narrates the
subagent dispatch contract; phase 6 re-narrates `experiment-harness`.
**Fix:** **reference** owned sub-workflows as handoffs; don't re-narrate them. Thinned map
in §4.

### The ONE residual disagreement + RESOLUTION
**A wanted:** "this is a duplicate of the `self-assembling-ergonomics` loop — just rename
that loop to a runtime spell" (initial V2, CRITICAL).
**V refuted** this as a **CATEGORY ERROR**, and the refutation holds:
- `self-assembling-ergonomics` is the **MACHINE-LED autonomous meta-loop** — "the surface
  improving the surface" (`self-assembling-ergonomics/README.md`: *"suggests its own next
  ergonomics improvement, assembles it, tests it, and then notifies the user"*).
- The discipline's step-2 spell is the **HUMAN-LED routing composition**
  (`SPELL-IDE-ASSISTED-ARCANUM-ROUTING.md`: turns conversation spans into bounded actions
  the human drives).
- They share a skeleton but differ on **WHO-LEADS-WHEN** — the ergonomics-first
  distinction (machine-led vs human-led). That is a real type difference, not duplication.

**RESOLUTION (noted, not re-opened): sibling, not rename.**
`self-assembling-ergonomics` is a **sibling primitive** the spell **may compose** as its
*autonomous variant* — not the thing being renamed, and not the spell's parent. The
**common owner of both is the `ide-action-surface` discipline.** "Build-from-owned" means
build from the **discipline + the validated dispatch contract**, with
`self-assembling-ergonomics` available as a composable sibling.
*(Lane A's V3 "over-reach" stands as a real symptom — fixed by thinning, MF-5 — not by
rejection. That part of A was accepted, not refuted.)*

---

## 4. The corrected (hardened) design

**Identity.** `ide-assisted-arcanum-routing` — **step 2** of the `ide-action-surface`
discipline. A **Spellcraft composition**. Blocked until step-1 discipline formalization
completes.

**Thinned phase set (~6) — compose vs reference:**

| # | Phase | Owner sigil(s) | Compose / Reference |
| --- | --- | --- | --- |
| 1 | **Frame + requirements** | `craft` (+ `distill`) | compose |
| 2 | **Two-lane harvest** | — | **REFERENCES** `domainspec-subagents-strategy` as handoff (don't re-narrate the dispatch contract) |
| 3 | **Design + bind** | `invoke` (define/design) | compose; **glossary-consistency gate** |
| 4 | **Plan + first SWU** | `invoke` plan / `implementation-layering` → `task-session` | compose |
| 5 | **Test** | — | **REFERENCES** `experiment-harness` as handoff |
| 6 | **Emit admission-PROOF** | the spell produces fixture/receipt/pre-registered verdict | hands proof to the **owner-held coordinate-admission gate** — **NO admission phase; spell never owns the gate** (MF-1) |

The deleted phase 7 ("Admit") is the single biggest change: the spell **stops at producing
proof**; admission is the owner's act.

**Gate ownership.** Produce-proof, never own-the-gate. The coordinate-admission gate is
owned by the `PRODUCT-VIEW.md` owner / governance review (UNIFIED-PRODUCT-VIEW.md:156–161).
The spell hands it a proof packet; the owner admits.

**Corrected CAV2 bindings:**
- **DROP** "D46-as-UI" (D46 = Experience Evidence Lifecycle, DEFINITIONS.md:3030).
- **BIND** `CAV2-D45` + `CAV2-D46` + `CAV2-D47` + `CAV2-C15` as the **governance cluster**
  (DEFINITIONS.md:2946/3030/3107; STABLE-REPOSITORY-CONSTITUTION.md:330).
- **BIND** `CAV2-D49` (default-deny) + `CAV2-D48` (promotion lifecycle) for authority-kind.
- **ROUTE** the undefined term **"ergonomics" → `definitions-governance`** (0 occurrences
  in DEFINITIONS.md).
- **HOLD** HMI served-not-promoted (`CAV2-CAND-HMI-001`; 0 occurrences in DEFINITIONS.md).

**Default-deny clause (verbatim, to embed in the spell contract):**
> *"This spell is a Spellcraft composition; it promotes nothing — every promotion routes
> to its owner; outputs acquire authority only through owner gates (`CAV2-D49`
> default-deny)."*

**Relation to siblings:**
- `self-assembling-ergonomics` = **sibling** (the autonomous/machine-led variant the spell
  may compose) — not parent, not rename.
- `ide-action-surface` discipline = **common owner / parent practice**; this spell is its
  step-2 instantiation.

---

## 5. Sequencing / next move

1. **Step 1 — `discipline-governance` formalize `ide-action-surface`.**
   This is the owner gate that (a) enumerates the step-2 spell and (b) **discharges the
   unenumerated-authority-kind concern** (MF-2) by giving the spell a card + catalog entry
   under an owned discipline. **Blocking precondition** for everything below.
   (Source: DISCIPLINE-CANDIDATE.md, `Status: candidate`.)
2. **Step 2 — `spellcraft` design `ide-assisted-arcanum-routing`** to the §4 corrected
   shape (thinned 6-phase, produce-proof-not-own-gate, corrected bindings, default-deny
   clause). (Source: SPELL-IDE-ASSISTED-ARCANUM-ROUTING.md, `Status: candidate`.)
3. **Then** `invoke` define → `task-session` for the first bounded SWU.

---

## 6. Residue routed to owners

| Residue | Owner it routes to | Why |
| --- | --- | --- |
| "ergonomics" is an **undefined term** | `definitions-governance` | 0 occurrences in DEFINITIONS.md; spell must not coin it |
| The spell's **authority-kind** acknowledgement | `decision-gate` + `constitution-governance` | unenumerated kind under `CAV2-D49` (DEFINITIONS.md:3245) — default-deny until owner amends Kinds |
| **Executable-correctness** — does the thinned route chain actually compose? | `spellcraft` design + `dispatch-spec` validation | **unproven** until Spellcraft composes the contract and dispatch-spec validates route shape; Lane V validated consistency, NOT executability |

---

## Provenance of this reconciliation

- Lane V refuted V2-rename (category error: machine-led vs human-led); conceded
  V5/V4a/V4b/V1.
- Lane A collapsed reject → redirect; conceded V1/V2/V3 as rescope grounds and the HMI
  half of V5; held MF-1…MF-5.
- Both lanes converged on **REDIRECT**.
- Settled points above are not re-opened. The single residual disagreement (V2-rename) is
  resolved as **sibling, not rename** (§3).
