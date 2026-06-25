# research.md — collected explorer returns (verbatim)

Dispatch `2026-06-24-resonantos-owned-base-and-importance` (research). Three explorers,
tensioned on source-corpus × methodology. Verbatim returns; cited synthesis in findings.md.

---

## E1 — EMPIRICAL HARVEST of OWNED arcanum base

**Position (defended): substantial OWNED, copyable base exists — but overwhelmingly markdown
design/contract/skill material, not drop-in runnable code.** Runnable surface is real but thin
(bash/jq + python validators). Corpus root: arcanum/ (PUBLIC, MIT — arcanum/LICENSE).

### Tier 1 — memory-governance spine (hand to Victor first)
1. **Necronomicon — knowledge harness spec.** Repo-local working-memory + routing-desk:
   "Inventory And Ontology Substrate Loop." Classifies output as source-backed fact / inventory
   candidate / ontology candidate / premise candidate / contradiction / decision gap / route gap;
   machine-readable gap ledger; owner handoffs; NO-PROMOTION guardrails; explicit
   active_interaction state model. Type: **markdown design/contract** (46KB README, no runtime).
   arcanum/spells/necronomicon/README.md + development/. Public-safe: YES.
2. **Inventory sigil — compiled-knowledge layer (most runnable asset).** Immutable raw sources +
   LLM-maintained markdown pages + machine index.json. Defines **evidence-card** primitive
   (source_refs, authority state, provenance, trace, residue, promotion_owner) + candidate
   EvidenceSet. Type: markdown skill + RUNNABLE validators. arcanum/arcana/inventory/.
   - Runnable bash/jq: scripts/validate-index-json.sh, validate-evidence-card-slice.sh,
     validate-evidence-card-fixtures.sh.
   - Copyable schemas/templates (drop-in): templates/ — evidence-card.schema.yml,
     evidence-set.schema.yml, index.schema.yml, evidence-card-schema.md, index.json, entry.md,
     log.md, tags.md. Public-safe: YES.
3. **Definitions Governance sigil.** Canonical definitions, synced indexes, drift checks — the
   "promote candidate to canonical" owner Necronomicon hands off to. Markdown skill + corpus +
   validators (arcanum/tools/validate-artifact-metadata.py, validate-artifact-constitution.sh).
   arcanum/arcana/definitions-governance/. Public-safe: YES.
4. **Ontology Vault sigil.** Roles, confidence, premises, edge rules, branch-aware ontology —
   promotion target for ontology/premise candidates. Markdown skill + 13 copyable templates
   (confidence-promotion.md, premise-review.md, ontology-drift-report.md, traceability-matrix.md).
   arcanum/arcana/ontology-vault/. Public-safe: YES.

### Tier 2 — composition + install
5. **Ontology Harness spell** — composes inventory + ontology-vault + context-builder. Markdown.
   arcanum/spells/ontology-harness/. Public-safe: YES.
6. **Arcanum Bootstrap** — installs the above into a consuming repo (.arcanum/inventory/,
   .arcanum/observability/, optional .arcanum/necronomicon/). Markdown spec + RUNNABLE installers
   (arcanum/tools/install_arcanum.sh, bootstrap_arcanum.sh, build-skill-registry.py). Public-safe: YES.
7. **Observability / Observed-Invocation-Loop** — one telemetry signal per managed invocation +
   reflection counters. Markdown. arcanum/spells/observed-invocation-loop/,
   arcanum/formulae/observability-setup/. Public-safe: YES.
8. **A live populated inventory instance** to copy as reference impl: arcanum/.arcanum/inventory/
   and arcanum/arcana/inventory/development/pilot/evidence-card/ (fixtures the validators run on).

### Honest accounting — runnable vs design-only
- **Runnable (drop-in):** inventory bash+jq validators, python artifact/metadata validators,
  bootstrap shell installers, .schema.yml/index.json/template files (copyable data contracts).
  That is the WHOLE runnable surface — validators and installers, NOT a memory engine.
- **Design/contract only (the bulk):** Necronomicon, Inventory, Definitions-Governance,
  Ontology-Vault, Ontology-Harness SKILL.md/README bodies are LLM-executed skill prose. There is
  NO compiled memory-governance service to lift; the "engine" runs via an LLM agent following the
  skill. Victor gets format + lifecycle + guardrails + validators — he still builds the runtime.

### Boundary correction (radical candor)
**authority-triage is NOT a public arcanum asset.** It lives at repo-root
development/authority-triage (PRIVATE). Only its evidence-card residue surfaces under
arcanum/.arcanum/inventory/entries/. Do NOT hand authority-triage source to an external engineer.
Public-safe analog for "triage authority of a knowledge claim" = inventory evidence-card
authority-state + promotion_owner model + definitions-governance drift audit.

**Bottom line for Victor:** copyable base = inventory evidence-card/EvidenceSet schemas +
validators (runnable), Necronomicon substrate-loop + no-promotion guardrail design (markdown),
definitions-governance + ontology-vault as promotion owners, bootstrap installers — all
MIT/public. A governance BLUEPRINT WITH VALIDATORS, not a shippable memory service.

---

## E2 — FORMAL SALIENCE ANALYSIS of the Living Archive's existing importance machinery

**Position (defended): the substrate already answers retrieval/keep/prune/surface — the
recall-side of importance — so "we tell it what's important" is REDUNDANT on the recall axis but
NOT against a second axis the machinery deliberately stops short of.**

### Existing machinery (PDF cites)
1. **utility_score — per-edge + utility-thresholded pruning.** First-class edge property (p.3).
   Retrieval-time: Fast Loop "Filter by utility threshold" (p.5). Maintenance: Dream PRUNING
   tombstones utility<threshold, removes orphans, consolidates (p.7). Recall gate + retention gate.
2. **JEPA Relevance Predictor.** ~110M, per chunk/function, "Score semantic relevance" (p.4);
   produces relevance score at write (p.6). The content-importance scorer.
3. **Aspirational Model — directional relevance.** Shared-JEPA encoder, ingestion: "Directional
   relevance — what the agent WANTS to know, not just what it HAS" (p.4); emits a "directional
   score" distinct from JEPA's (p.6). The substrate ALREADY has a notion of desired/wanted
   importance — a learned/inferred direction.
4. **Self-Model density / "I don't know" gate.** Logic over graph stats, query-time; gates
   mind-waking on density, prevents hallucination in sparse regimes (p.1, p.4); percolation
   threshold empirically learned, per-deployment (p.11 §10.6). Meta-importance: do I know enough.
5. **Recency / utility / structural signals.** Default ["semantic","recency"]; code adds
   ["call_distance","import_depth"] (p.7–8).
6. **Dream-state replay re-scoring.** Replays HIGH-utility traces, JEPA re-scores relevance (p.7) —
   importance is a moving estimate, updated offline.
7. **Temporal validity as relevance filter.** [validity_start,validity_end]; default traverses
   validity_end>now; stale demoted but queryable via asOf (p.7).

### What it already answers
The recall/curation axis, at three timescales: what to surface now (Fast Loop), what to keep vs
prune (Dream PRUNING), what to reconsolidate (Dream REPLAY), whether to answer at all (Self-Model).
Includes the "wanted not just had" direction via the Aspirational Model. So naive "tell it what's
important to retrieve/keep" is REDUNDANT.

### Where it STOPS (the non-redundant residue)
Every signal is derived BOTTOM-UP from graph statistics or embedding geometry: utility from access/
replay, JEPA from embedding prediction, recency from timestamps, Self-Model from density, even the
Aspirational Model is a learned encoder inferring direction. There is NO authored, top-down
importance assertion. Three gaps:
1. **Authored priors with no statistical mass.** A net-new/rarely-accessed concept the operator
   KNOWS matters has low utility (prunes) and may sit under the percolation floor → returned "I
   don't know"; no channel to INJECT importance the graph hasn't earned. Aspirational Model is the
   nearest thing but is inferred, not declared.
2. **Threshold calibration is per-deployment and ungoverned.** Percolation/utility cutoffs named
   but no authority over their values (p.11 §10.6, p.5, p.7).
3. **No claim≤proof / provenance weighting on importance.** Importance is purely relevance+utility;
   no notion that importance should track source AUTHORITY/PROVENANCE. (The shipped code is almost
   entirely provenance/intake gating; its retrieval rank is a placeholder substring score
   `max(1,1000-matchIndex)` at living-archive-mcp.mjs:465 — NONE of the PDF scoring machinery is
   implemented yet; the importance spine is SPEC, NOT SHIPPED.)

### Verdict
Redundancy is real on the recall axis — do not re-coin it. The honest opening is the
**top-down / authored-priors / provenance-weighted axis**: the substrate scores importance it can
observe or infer but provides NO governed channel for DECLARED importance that overrides low
statistical mass, and NO authority over its own thresholds. Frame our contribution as
authored/provenance-weighted priors FEEDING the existing utility/Aspirational signals, not
replacing them.

---

## E3 — DESIGN-MAPPING: the GOVERN/promote-importance notion

**Position (defended): a different importance than retrieval-salience — about reliance and
promotion ("can we stand on this?"), not relevance-to-a-query ("bring this forward").** The corpus
never measures relevance-to-a-query; it measures AUTHORITY EARNED AGAINST GUARDRAILS.

### Mapping 1 — necronomicon: importance = authority-level on a promotion ladder
Classification vocabulary (README:33, KNOWLEDGE-SUBSTRATE-FLOW.md:31-43) sorts input into
source-backed fact | inventory/ontology/premise candidate | contradiction | decision gap | route
gap — degrees of TRUSTWORTHINESS/promote-worthiness, not relevance. The ladder (raw → session
evidence → discovery baseline → inventory → ontology candidate → premise → confidence decision →
constitution → axiom, KSF:15-25) is an increasingly strict gradient of "how much may the system
rely on this." NO-PROMOTION guardrails (README:40-44) prove it: "may create candidates … must not
promote by itself." The **confidence split** (KSF:164-177) nails it: evidence confidence ("how well
supported") vs commitment confidence ("how strongly should we rely now"). "High evidence, low
commitment: true but not strategically important" = a fact can be well-supported (recall-findable)
yet NOT important to rely on. Owner handoff (DESIGN.md:196-205, non_authority_note) = governance
routing, not retrieval.

### Mapping 2 — restraint-floor: importance = "may this safely become something?"
Negative/gating filter on agent ACTION (restraint-floor/README.md:23-28). Shared contract
(README:57-66) = table of BLOCKED per primitive: no canonical promotion / does not switch route /
handoff ≠ execution proof / no spawn without approval / no write by default / assembled+green ≠
shipped. Salience-to-promote, not salience-to-recall — "when NOT to act." Sourced to necronomicon
No-Promotion Guardrails. Net-new: graduated-trust dial (expert bypass) + logged non-action — knobs
on the promote-importance threshold, never a relevance score.

### Mapping 3 — lifecycle-progression + dispatch-grammar-routing: promote-worthiness / receipt-debt
lifecycle-progression: importance = graduation-readiness along Discover→Research→Decide→Define→
Design/Plan→Execute (README:29-36). Keystone: converts flat peer routes into a partially-ordered
progression carrying **receipt-debt** (README:38-44) — tracks what evidence a thing OWES before it
may advance (README:59-66). A retrieval ranker has no notion of "owing a receipt before graduating."
dispatch-grammar-routing = routing vocabulary, explicitly LATENT, "carries NO surface-level decision
power" (README:33-49). UNIFIED-PRODUCT-VIEW:101-106: only work-arc lifecycle "does irreducible
card-level decision work" — promote/graduate is load-bearing; restraint is the floor; grammar latent.

### The concrete match to resonantOS (the gift)
necronomicon shape = intake → classify-authority → gated-promote-via-owner, ALREADY MATCHES
resonantOS intake → Review-Queue → promote. Structural: intake = "capture as session evidence with
low authority" (README:32-33); Review-Queue = candidate tier + gaps.json (README:34-36;
DESIGN.md:182-194); promote = owner-gated (README:42-44; KSF:153-161). OPPORTUNITY-INTAKE
generalizes: a captured opportunity is a "default-deny candidate … sits in backlog until triaged"
(OPPORTUNITY-INTAKE.md:24-28, captured→triaged→in-lifecycle→admitted|dropped). They compose (recall
a candidate, still refuse to promote it); neither subsumes the other.

### Honesty caveat (design vs runnable)
Markdown design, NOT running code. Files carry status: strategy-proposal / draft. DESIGN.md is
draft and lists R-DES-001..005 incl. "Necronomicon becomes a thin inventory wrapper" — i.e. the
govern-importance layer collapsing back into retrieval, flagged unproven (DESIGN.md:216-222).
Authority ladder, ide coordinate space, receipt-debt, admission gate are specified, not
demonstrated — no fixture shows a candidate actually promoted. OBSERVABILITY-PROVENANCE-PLAN is
closest to executable (subject + gap_ownership envelope fields, Phase 1:51-95) but is a phased plan.
The NOTION is consistently encoded; the RUNTIME is not yet built. Claim ≤ proof.
