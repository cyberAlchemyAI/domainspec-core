# Base for host collaborator — the owned governance layer for resonantOS memory

Audience: resonantOS engineer. This is the concrete, MIT/public base we're handing you, what's
runnable vs design, how it maps onto your intake → Review Queue → promote flow, and one honest
caveat about importance. **Claim ≤ proof: where a piece is markdown design, it says so — do not treat
it as a drop-in runtime.**

---

## 1. What we're handing you

All of the following is public (MIT). Per artifact, an honest column: **COPY-THIS** (runnable today),
**PORT-THE-DESIGN** (markdown contract you implement against), or **YOU-ALREADY-HAVE-THIS**.

| Artifact | What it gives you | Status |
|---|---|---|
| **Inventory evidence-card / EvidenceSet schemas** (`templates/evidence-card.schema.yml`, `evidence-set.schema.yml`, `index.schema.yml`) | A typed candidate record: `source_refs`, authority-state, provenance, trace, residue, **promotion_owner** | **COPY-THIS** — drop-in data contract |
| **Inventory validators** (`scripts/validate-index-json.sh`, `validate-evidence-card-slice.sh`, `validate-evidence-card-fixtures.sh`) | bash/jq that checks cards/index conform; run against your queue records | **COPY-THIS** — runnable |
| **Arcanum bootstrap installers** (`install_arcanum.sh`, `bootstrap_arcanum.sh`, `build-skill-registry.py`) | Stand up `.arcanum/inventory/` + observability in a repo | **COPY-THIS** — runnable installers |
| **Live inventory instance + fixtures** (`.arcanum/inventory/`, `development/pilot/evidence-card/`) | Worked reference the validators run on green | **COPY-THIS** — reference |
| **Necronomicon — the guardrails on your loop** (`spells/necronomicon/README.md`) | NOT the intake→classify→promote loop (you already have that — see below). The portable residue: the **NO-PROMOTION guardrail** (capture may never self-promote), the **machine gap-ledger**, owner handoffs, the **restraint floor**, and **receipt-debt** (what a candidate *owes* before it may advance) | **PORT-THE-DESIGN** — markdown, no runtime |
| **Definitions-governance** (`arcana/definitions-governance/`) | The "promote candidate → canonical" owner with drift checks (+ runnable metadata/constitution validators) | **PORT-THE-DESIGN** (validators COPY-THIS) |
| **Ontology-vault** (`arcana/ontology-vault/`) | A **typed** premise/ontology promotion target (roles, confidence, premises, 13 templates) — distinct from your existing knowledge-page promote target, not a replacement for it | **PORT-THE-DESIGN** (templates COPY-THIS) |
| **Review Queue intake→classify→promote** | — | **YOU-ALREADY-HAVE-THIS** — your Review Queue already implements necronomicon's intake→classify→promote shape |
| **Recall-importance** (utility / JEPA / Aspirational / Self-Model) | — | **YOU-ALREADY-HAVE-THIS** — your machinery already decides what to recall |

**Honest accounting:** the runnable surface is **validators + installers + schemas only**. The
substrate-loop, definitions-governance, and ontology-vault *bodies* are LLM-executed skill prose —
a governance **blueprint with validators**, not a shippable memory service. You get the format, the
lifecycle, the guardrails, and the validators; you build the runtime.

---

## 2. The importance design, plainly

There are **two different things both called "importance,"** and you already own one of them:

- **RECALL importance — what to bring forward / keep / prune.** Your Living Archive already decides
  this: utility_score, the JEPA relevance predictor, the Aspirational Model (what the agent *wants*
  to know, not just what it *has*), and the Self-Model "I don't know" density gate. **We are NOT
  adding to this — telling your archive what's important to recall would be redundant.**

- **GOVERN / RELY-ON importance — what may we stand on and promote.** This is what the base adds, and
  your substrate has no field for it. It's a different question: not "bring this forward" but
  **"can we rely on this?"** The key idea is the **evidence-confidence vs commitment-confidence
  split**: a fact can be *well-supported* (your archive finds it fine) yet **not strategically
  important to rely on** — "high evidence, low commitment." Two more pieces:
  - **Authored / provenance-weighted priors** that can **override low statistical mass** — when an
    operator KNOWS a net-new or rarely-accessed concept matters, it should be injectable even though
    your graph hasn't earned it utility yet (today such a concept prunes or falls under the
    percolation floor and returns "I don't know").
  - **Authority over the thresholds** — your percolation/utility cutoffs are currently
    per-deployment and ungoverned; this layer gives them an owner.

**It FEEDS your existing signals, never replaces them.** An authored prior injects importance your
graph hasn't earned; threshold-authority calibrates your own cutoffs. Both feed inward into the
utility/Aspirational scoring you already run.

**Honest both ways:** none of this importance machinery is running yet — on either side. Your PDF
scoring (utility/JEPA/Aspirational/Self-Model) is spec; the shipped retrieval rank is still a
placeholder substring score. And our govern-importance layer is markdown design (status
`strategy-proposal`/`draft`) with no promoted-candidate fixture. This is a shared design target, not
a drop-in.

---

## 3. How each owned piece maps onto your intake → Review Queue → promote

The necronomicon shape is **intake → classify-authority → gated-promote-via-owner**, which already
matches **your intake → Review Queue → promote**:

| Your step | Owned piece that maps onto it | What it adds |
|---|---|---|
| **Intake** | Inventory: "capture as session evidence with low authority" → an **evidence-card** (candidate, default-deny) | A typed candidate record with provenance + promotion_owner, validated by bash/jq |
| **Review Queue** | Necronomicon candidate tier + machine gap-ledger; ontology-vault as promotion target | A classification vocabulary (fact / candidate / contradiction / decision-gap) and the receipt-debt a candidate OWES before it may advance |
| **Promote (decide step)** | Necronomicon **NO-PROMOTION guardrail** + definitions-governance as the promotion owner | The restraint floor: "may create candidates … must not promote by itself"; promotion is owner-gated, never automatic |

The two compose: your archive can **recall** a candidate while the governance layer still **refuses
to promote** it. Neither subsumes the other.

---

## 4. First-slice recommendation

Smallest real step that proves the seam:

1. **COPY the evidence-card schema + validators** (`evidence-card.schema.yml`,
   `evidence-set.schema.yml`, the three `validate-*` bash/jq scripts). Make your Review Queue records
   conform; run the validators in CI. This is runnable today.
2. **PORT the NO-PROMOTION guardrail into your Review Queue decide step** — promotion stays
   owner-gated and default-deny; recall stays free. This is the load-bearing guarantee, and it slots
   directly into your existing decide enum.

Everything else (definitions-governance promotion owner, ontology-vault targets, authored-prior /
threshold-authority importance) layers on after this slice is green.

---

## 5. Boundary notes (what is in scope to share)

- **Public and fine to explain in full:** the necronomicon spell, inventory (evidence-card /
  EvidenceSet / promotion_owner), definitions-governance, ontology-vault, arcanum-bootstrap, and the
  cav2 governed-store / promotion / scope-tags vocabulary.
- **The "triage the authority of a claim" function** is handled here by the **inventory evidence-card
  authority-state + promotion_owner model** plus definitions-governance drift checks — that is the
  public, shareable analog, and it is what you build against.
- **Out of scope / not shared:** no internal layer-map, no moat or engine-algorithm internals, no
  private codenames. **Saturn** and **DomainSpec** are mentioned only as *intended, not shipped*.
