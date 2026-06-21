---
title: DomainSpec as a Layer of Saturn — Reconciled Map (Spec vs Deployed)
status: draft
created: 2026-06-21
purpose: Give a paper/explainer one defensible "DomainSpec is a layer of Saturn" statement, grounded in what is specified AND what is actually published, with public-safety flags.
---

# DomainSpec as a Layer of Saturn — Spec vs Deployed

> Reconciles the **intended** layer model (private spec material) against what is
> **actually published** today (public Arcanum site). Where they disagree, prefer the
> honest current state and note the intended target. Read the public-safety flags (§5)
> before copying any line into a public surface.

---

## 1. What the SPEC says (intended layer model)

Two private sources agree on the spine but use different vocabularies:

- **`agentic-system-deep-dive.md` (cyberAlchemy/, private):** the canonical prose. Three
  pillars: **DomainSpec** = *what* is meaningful (structured intent), **Arcanum** = *how*
  the work is done (reusable capabilities), **Saturn** = the **top-level convergence /
  control loop** that closes intent↔reality with evidence. Saturn "becomes the top-level
  control loop"; ontology "should know which lower-level concepts realize it: **DomainSpec
  structured intent**, Arcanum execution routes, inventory evidence, bridge drift,
  telemetry, reflection, promotion gates." Saturn *does not own* ontology storage, memory
  mechanics, or every execution route.
- **`framework-unification/CONCEPT-MAP.md` (private):** "DomainSpec says *what*, Arcanum
  says *how*, **Saturn closes the loop with *evidence***." Adds the **two-axis** refinement:
  one **horizontal pipeline** (define→…→verify→emit-signals) and **three vertical
  mechanisms** (representation / communication / epistemology) cutting every node.
- **`cyberalchemy-shareable.html` (private deck):** names **Project Saturn** as
  "Continuous Cybernetic Alignment" and gives Saturn an explicit **8-layer stack** it
  traverses as a meta-loop (see §4). Notably the deck **never names DomainSpec** — the
  layers it lists (Foundation/Ontologies, Formalization/Feature Contracts, Agentic
  Substrate, etc.) are *what DomainSpec produces*, but the word "DomainSpec" is absent.

**Intended layer relationship (spec):** Saturn is the convergence loop (the whole). Its
stack has layers for intent-modeling, formalization, execution, and perception. **DomainSpec
is the layer (the discipline) that owns the intent/modeling/formalization layers** —
typed concepts, relationships, feature contracts, tests, observability signals — i.e. it
produces the **reference baseline** Saturn measures reality against. Arcanum is the agentic
substrate layer; inventory/ontology are the knowledge layers; telemetry/reflection are the
perception layers Saturn reads back.

---

## 2. What the DEPLOYED site says (actually published today)

The only published GitHub Pages surface is **`arcanum/docs/index.html`** (+ the deep-dive
`arcanum-development-loop.html`), served at `cyberalchemyai.github.io/Arcanum/`.

- The site brands the product as **"CyberAlchemy — an operating language for agentic
  creation."** Its content is the **Arcanum loop only**: Prompt → Refine → Invoke → Route →
  Execute → Learn (name / shape / prove).
- It presents **Arcanum** (sigils, guides, validators, work-packs, task-sessions, residue)
  as the working surface.
- **It does NOT mention "Saturn" anywhere.** (grep: 0 hits in `arcanum/docs/`.)
- **It does NOT mention "DomainSpec" anywhere on the published page.** (DomainSpec appears
  only in internal `arcanum/docs/vault/conversations/…` and `arcanum/TO-VLAD/…`, which are
  in-repo but not part of the landing surface.)
- The public deck `cyberalchemy-shareable.html` *does* present Saturn richly — but that
  deck is **private** (lives under `cyberAlchemy/`, not in the published `arcanum/docs/`).

**Net:** The thing the public can actually see (the Arcanum site) presents the **"how"
layer (Arcanum) standalone**, with **no Saturn frame and no DomainSpec layer named at all.**

---

## 3. Reconciliation table

| Concept | Spec says | Deployed (published arcanum/docs) says | Divergence / gap |
|---|---|---|---|
| **Saturn** | Top-level convergence/control loop; the whole system's rhythm (observe→compare→drift→correct→verify→update). 8-layer stack in the deck. | **Not mentioned at all.** | **MAJOR.** The organizing frame is invisible on the public site. Saturn lives only in private deck + internal dev docs. |
| **DomainSpec** | The structured-intent discipline; owns the intent/formalization layers; produces the reference baseline Saturn measures against. | **Not mentioned on the landing page** (only buried internal vault refs). | **MAJOR.** The "what" layer is absent from public branding; site reads as Arcanum-only. |
| **Arcanum** | The "how" — reusable agent capability substrate; one layer realizing Saturn. | The **entire public product** ("operating language for agentic creation"). | **Framing inversion.** Spec treats Arcanum as one layer; deployed presents it as the whole product. |
| **The loop** | Saturn meta-loop across all layers (intent down, evidence up). | Arcanum dev loop (Prompt→Refine→Invoke→Route→Execute→Learn). | **Scope mismatch.** Deployed loop is the capability-authoring inner loop; Saturn's convergence meta-loop is not shown. |
| **Layer model** | Two-axis (pipeline × 3 mechanisms) OR Saturn's 8-layer stack. | No layer model published; flat list of Arcanum tools. | Layered architecture is spec-only. |
| **Drift / convergence** | Core thesis ("drift is actionable; evidence flows back into governance"). | Implied by "prove / keep evidence / residue / next route" but **drift is never named**. | Partial: vocabulary present, the Saturn drift-defense thesis is not. |
| **DomainSpec ⊂ Saturn relation** | Explicit: DomainSpec is a lower-level concept that *realizes* Saturn. | Unstatable — neither term published. | The whole claim this map exists to support is **absent from the public surface.** |

---

## 4. Crisp statement + reusable ASCII diagram

**Defensible one-liner (honest, spec-grounded):**

> **DomainSpec is the structured-intent layer of Saturn.** Saturn is the convergence
> control loop that keeps intent and reality in contact (observe → compare → detect
> drift → correct → verify → update governance). DomainSpec owns the *intent* end of that
> loop: it turns domain understanding into typed concepts, relationships, feature
> contracts, tests, and observability signals — the **reference baseline** Saturn measures
> reality against. Arcanum is the *execution* layer that does the work; inventory/ontology
> are the *knowledge* layers; telemetry/reflection are the *perception* layers Saturn
> reads back. (Source: private spec. **Caveat: this Saturn↔DomainSpec framing is not yet
> published on the public CyberAlchemy/Arcanum site — it is the intended target, not the
> current public state.**)

```
                          SATURN  (convergence / control meta-loop)
        intent flows DOWN  │                              ▲  evidence flows UP
                           ▼                              │
   ┌───────────────────────────────────────────────────────────────────────┐
   │ MODELING & INTENT      ── DomainSpec ──  typed concepts, relationships, │  ◄ DomainSpec
   │                                          feature contracts, tests,      │    is THIS layer
   │                                          observability specs            │    (the baseline)
   ├───────────────────────────────────────────────────────────────────────┤
   │ OPERATION & EXECUTION  ── Arcanum ────  sigils / spells / task-sessions │  ◄ the "how"
   │                          (+ inventory / ontology = knowledge substrate) │    (publicly shipped)
   ├───────────────────────────────────────────────────────────────────────┤
   │ VERIFICATION & PERCEPTION ── tests, drift telemetry, reflection ───────│  ◄ evidence Saturn reads
   ├───────────────────────────────────────────────────────────────────────┤
   │ REGULATION & INTERFACE ── governance gates, human harness, dashboards ─│  ◄ Saturn acts here
   └───────────────────────────────────────────────────────────────────────┘
        Saturn traverses every layer: reads perception, evaluates vs intent,
        routes corrections through execution & regulation, verifies closure.

   Honest status today: only the "Arcanum" (execution) layer is PUBLICLY shipped.
   Saturn (the frame) and DomainSpec (the intent layer) are spec/private only.
```

(Deck's full 8-layer enumeration, for reference: Foundation/Ontologies · Formalization/
Feature Contracts · Agentic Substrate · Infrastructure · Quality/Tests · Observability ·
Governance · Human Harness — grouped above into the deck's four bands.)

---

## 5. Public-safety flags (flag, do NOT resolve)

A later auditor must treat these as **PRIVATE source — never copy verbatim into the public
site without a boundary scrub** (per SUBMODULE-DISCIPLINE.md and cyberAlchemy-v2 SOURCE-MAP):

| Source | Location | Visibility | Risk if copied public |
|---|---|---|---|
| `agentic-system-deep-dive.md` | `cyberAlchemy/` | **PRIVATE** | Internal pillar model, promotion gates, ontology branches. |
| `cyberalchemy-shareable.html` | `cyberAlchemy/` | **PRIVATE deck** (despite "shareable" name — not on the published site) | Names Project Saturn/MARS/MOGT + 8-layer architecture. Confirm intended audience before reuse. |
| `framework-unification/*` | `projects/` | **PRIVATE** | Two-axis architecture, invariants, Lean/PermGuard honesty bounds, open questions. |
| `cyberAlchemy-v2/*` | parent repo | **PRIVATE** | Consolidation/authority spine; explicitly pre-extraction, boundary scrub pending (OQ-2). |
| `cyber-alchemy-lean-fusion/*` | `projects/.../layers/` | **PRIVATE** | Lean novelty, PermGuard kernel, CERTIFIED-vs-ASSUMED border. Overclaim risk. |
| `arcanum/docs/index.html` + dev-loop | `arcanum/` | **PUBLIC (deployed)** | Safe — already the published surface. |
| `arcanum/docs/vault/…`, `arcanum/TO-VLAD/…` | `arcanum/` | in public repo but **NOT published page**; treat as internal | Contains DomainSpec refs; in-repo public but not landing-surface. |

**The boundary rule (from VISION §8 + SOURCE-MAP):** only **concept-level** material goes to
public Arcanum; private research stays in `domainspec-*` / `cyberAlchemy*`. The honest line:
the public face is **Arcanum (the "how")**; Saturn and DomainSpec are the intended **frame**
not yet promoted to the public surface — say "intended/target," never "shipped," in public copy.

---

## 6. Open questions (carried, not resolved here)

- **OQ-1.** Is Saturn *deliberately* withheld from the public site (staged rollout) or is
  the site simply behind the spec? Decide before an explainer claims Saturn is "the product."
- **OQ-2.** Does the deck's 8-layer stack reconcile with framework-unification's two-axis
  model, or are these two competing layer ontologies? (Deck = stack; CONCEPT-MAP = pipeline×
  mechanisms.) The diagram in §4 picks the deck's 4-band grouping as the explainer-facing one.
- **OQ-3.** "Shareable" deck is filed PRIVATE — confirm its true distribution status before
  any auditor treats its Saturn content as already-public.
