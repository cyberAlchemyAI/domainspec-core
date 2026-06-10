# Decision Record — B1 branch naming & pilot promotion-method template

- Scope: CyberAlchemy first product (project `ontologize`)
- Date: 2026-06-10
- Source of decision: user (operator, Victor), via `decision-gate`
- Gate result: PASS

Resolves open residue [R12, R15](../residue/open-residue.md). Candidate-only: no canonical
promotion, no pricing/contracts/named-client commitments.

---

## Decision 1 — Canonical name of ontology branch B1 (R12)

**Question:** What is the canonical name of branch B1 — "meaning" or "business"?

**Options considered:**

- **"business"** — aligns with every promotable Arcanum surface: the `ontology-vault` sigil's only
  branch token (`--branch business`), `arcanum/BUSINESS-ONTOLOGY.md`, and the ONTOLOGY-ARCHITECTURE
  stable-branch table. Cost: "business" reads narrower than the intent the branch carries.
- **"meaning"** — ontologize's own intuition gloss; more evocative for clients. Cost: no prior-art
  file names the branch "meaning"; it would create a label-vs-runtime mismatch the moment a client
  touches the sigil.

**Selected: "business"** (carrying "meaning / domain / intent" as documented client-facing aliases).

**Rationale:** Every promotable runtime surface already calls it `business`. Aligning the canonical
name avoids a silent label-vs-runtime divergence at the exact point of value — the moment a client
operates the `ontology-vault` sigil. "meaning" survives as the client-facing intuition gloss only.

**Downstream impact:** Use "business" as the canonical B1 token in all executable/spec surfaces
(assessment instrument, ENGINE, deliverable template). Keep "meaning/domain/intent" as aliases in
client-facing intuition copy. `ONTOLOGY-BRANCHES.md` updates from owner edit, not silent rewrite.

## Decision 2 — Pilot promotion-method template (R15)

**Question:** For the two pilots (cap factory + logistics), reuse the existing
`cyberAlchemy/ontology/entries/knowledge-governance-authority-ladder.md` as the promotion-method
template, or design fresh per pilot? (Existing entries as *content* already stay separate — this is
only about reusing the ladder as a *method* template.)

**Options considered:**

- **Reuse the authority-ladder** — already a coherent, high-evidence-confidence ladder (evidence →
  inventory → ontology candidate → premise/confidence review → promoted entry). Accelerates both
  pilots; keeps the method consistent across verticals. Cost: tagged `candidate`, built for
  CyberAlchemy's internal agentic system; needs per-vertical adaptation.
- **Design fresh per pilot** — tailored to each vertical. Cost: reinvents an existing coherent
  ladder; slower; risks inconsistency between the two pilots.
- **Hybrid (reused baseline + per-vertical fork)** — common baseline, fork only where a vertical
  requires it. Cost: must track what diverged.

**Selected: Reuse the authority-ladder as the method template, adapting per vertical.**

**Rationale:** The ladder already models exactly the raw-evidence → governed-reuse progression the
pilots need, at `high` evidenceConfidence. Reusing it accelerates both pilots and keeps the promotion
method consistent across cap factory and logistics — which strengthens the cross-vertical
generalization claim (R1) by holding the method fixed while the verticals vary. Per-vertical
adaptation is expected; divergences are recorded against the shared baseline.

**Downstream impact:** The assessment instrument and ENGINE reference the authority-ladder as the
canonical promotion method. The deliverable template instantiates it per vertical. Adaptation deltas
per vertical are tracked, not silently forked (captures the hybrid concern as a discipline, not a
separate path).

---

## Remaining blockers

None for these two decisions. Note that product-level residue R1 (cross-vertical generalization),
R8 (per-vertical proof metric), R9 (KPI denominator authority), R11 (N2→N3 gate coverage), and the
inherited-gap residue R4/R5/R6/R7 remain open and are routed to assessment / ENGINE / pilot per
[NEXT.md](../NEXT.md).

## Assumptions recorded

None new.
