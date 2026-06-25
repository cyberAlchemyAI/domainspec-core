---
tags: [inventory, resonantos, living-archive, cav2, integration, importance, govern-importance, build-from-owned, claim-le-proof, boundary, synthesis]
node_type: synthesis
is_session: false
layer: architecture, governance, market
nature: reference
status: candidate
created: 2026-06-25
sources:
  - development/resonantos-integration/findings.md
  - development/resonantos-integration/RESONANTOS-INTEGRATION-GUIDE.md
  - development/resonantos-integration/owned-base/findings.md
  - development/resonantos-integration/owned-base/BASE-FOR-VICTOR.md
  - "Agent Memory Architecture v7.1 (PDF, Victor Morrow)"
  - arcanum/spells/necronomicon/README.md
  - arcanum/arcana/inventory/
---

# resonantOS Living-Archive — Seam + Owned Base + Importance — Synthesis

Candidate Inventory synthesis (not canonical). Captures two closed research dispatches that
turn the CyberAlchemy↔resonantOS integration from a plan into a concrete, boundary-scrubbed
teammate handoff, and answers the latent question "how does it decide what is important?".
Evidence: [`2026-06-25-resonantos-integration-and-owned-base-cards.md`](evidence-cards/2026-06-25-resonantos-integration-and-owned-base-cards.md).
Extends [`resonantos-and-ontology-retrieval-synthesis`](resonantos-and-ontology-retrieval-synthesis.md)
and [`moat-stack-and-authority-triage-synthesis`](moat-stack-and-authority-triage-synthesis.md).

## The seam (dispatch 1 — living-archive-integration)

resonantOS's **Living Archive is the textbook host the SDK predicted**: it already owns a
memory substrate, so CyberAlchemy does not reimplement inventory — it layers governance on the
WRITE side. **READ decouples, WRITE doesn't.** The addon manifest already exposes the exact seam:
`archive-read`/`memory-provider` back capture+lookup; `archive-intake-write` (intake-only) + the
**Review Queue** (`decide_review` approve/reject/escalate; `promote_review_artifact`) are where
cav2's governed store + promotion lifecycle plug in. Card: `living-archive-write-seam`.

**Honest correction (claim≤proof):** the trusted-write/promotion executor is host-resident and
ABSENT from the example code (portable services 501; `canWriteKnowledgePages:false`). CyberAlchemy
**implements the provider BODY behind resonantOS's owned `promote_review_artifact`/501 boundary** —
not a turnkey drop-in. Card: `promotion-executor-host-resident`.

**Map-vs-decision:** the substrate governs **facts-over-time** (validity windows + supersession,
dream-state contradiction resolution, self-model "I don't know") = OVERLAP, do not rebuild; it has
**no field** for authority/decisions/promotion = the ADDITIVE gap cav2 fills, non-redundant at the
schema level. Card: `additive-vs-overlap-facts-vs-authority`.

## The owned base + importance (dispatch 2 — owned-base-and-importance)

**What we give Victor is a governance blueprint with validators, not a memory service.** Three
honest tiers: COPY-THIS (inventory evidence-card schemas + bash/jq validators + arcanum-bootstrap),
PORT-THE-DESIGN (necronomicon NO-PROMOTION guardrail + gap-ledger + receipt-debt, restraint-floor,
definitions-governance, ontology-vault), YOU-ALREADY-HAVE-THIS (the host's Review-Queue loop +
recall-importance machinery). Card: `owned-arcanum-base-blueprint-with-validators`.

**"How does it decide what is important?" — two senses.** The Living Archive ALREADY solves
**recall-importance** (utility_score, JEPA, the **Aspirational Model** = directional "what it wants
to know", Self-Model density) → telling it what to recall is REDUNDANT. The non-redundant gift is
**govern/promote-importance**: the **evidence-confidence vs commitment-confidence** split ("true but
not strategically important"), **authored / provenance-weighted priors** that override low
statistical mass, and **authority over the thresholds** — a layer that **FEEDS** the existing
salience signals, never replaces them. Card: `two-senses-of-importance`.

**Boundary (radical candor):** `authority-triage` is PRIVATE (repo-root), not public arcanum — the
teammate doc uses the public inventory evidence-card authority-state + `promotion_owner` analog
instead. Card: `authority-triage-private-boundary`.

## Routing (owner gates — Inventory cannot promote)

- **SDK/integration decision-gate**: the seam status (built read+intake+review-queue vs the
  host-side promotion provider to implement); the owned-base copy/port plan.
- **cav2 authority owner**: the map-vs-decision line; the govern-importance axis; the public/private
  boundary (authority-triage).
- **arcanum-bootstrap / sigil-development**: the runnable base (schemas + validators + installers).

## Open residue

- Promotion/trusted-write provider is UNBUILT on the host side; govern-importance runtime is unbuilt
  on BOTH sides (the host's PDF scoring is spec; its shipped retrieval rank is a placeholder).
- necronomicon↔Review-Queue match is structural, not demonstrated end-to-end.
- Some resonantOS line-cites are external-source reads, not re-verified in domainspec-core.

## Downstream use

Use when a task asks "how does CyberAlchemy integrate with a host that already has memory"
(answer: READ decouples, host owns the map; we own the governed WRITE/decision side + implement the
promotion provider behind the host's named seam), "what owned material do we hand a host engineer"
(blueprint + validators; copy-vs-port-vs-already-have), or "does the host already decide what's
important" (recall-importance yes; govern-importance no — and we feed, not replace). Do not cite as
canonical — owners are the SDK decision-gate / cav2 authority / arcanum-bootstrap.
