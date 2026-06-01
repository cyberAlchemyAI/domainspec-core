# Reference Review — linkedin_ssi_booster

**Reviewed:** 2026-05-06
**Repo:** github.com/samjd-zz/linkedin_ssi_booster
**License:** MIT
**Version:** alpha-v0.0.2.5
**Commits:** 423
**Reviewer:** Josh (operator review, post-v0.1 PASS)

---

## What was reviewed

An alpha-stage LinkedIn Social Selling Index optimization tool. Multi-agent architecture with domain knowledge packs, per-sentence groundedness diagnostics (DoT/dot-report), beta-smoothed Bayesian priors, noise filtering, and hybrid RAG. Reviewed for design patterns transferable to Tilth, not for code reuse.

## Three things pulled into Tilth roadmap

### 1. NER-based fabricated-org gate (F-LOGICIAN-FABRICATED-ORG)

**Source pattern:** SSI Booster validates entity mentions against known domain ontologies.
**Tilth adaptation:** spaCy NER extracts ORG entities from Scribe drafts; set-membership check against PROJECT_CONTEXT.md org names. Deterministic, zero-token Logician POST-gate. Catches fabricated partnerships (Law 5 enforcement).
**Spec card:** `pipeline/engineering/spec_cards/logician_fabricated_org_ner_gate.md`
**Priority:** v0.2

### 2. Sector knowledge packs

**Source pattern:** `domain_knowledge_*.json` files auto-merged at runtime — each contributes domain-specific terms and scoring criteria.
**Tilth adaptation:** `pipeline/knowledge_packs/<sector>.json` per six sectors. Consumed by Scribe at PRE-gate for sector-specific terminology + funder-dialect vocabulary. Union merge with dedup, keyed by id, precedence by sector ordering.
**Design note:** `pipeline/roadmap/explorations/sector_knowledge_packs_design.md`
**Relationship:** Complements Capital Logic Cards (A6 Option C) — Cards are the strategic layer (what to argue), packs are the vocabulary layer (how to say it).
**Priority:** v0.2 or Phase One contractor work

### 3. Explain-grounding dev diagnostic

**Source pattern:** `--dot-report` generates a per-sentence groundedness gradient showing which claims have evidence backing and which don't.
**Tilth adaptation:** `tilth scribe --explain-grounding` prints per-sentence BM25-scored evidence breakdown against PROJECT_CONTEXT + RFA. Dev diagnostic only — NOT a runtime gate (would violate Logician determinism). Uses existing Scout BM25 retrieval primitives.
**Design note:** `pipeline/roadmap/explorations/explain_grounding_diagnostic.md`
**Priority:** v0.2 dev tooling

## Two overlaps dismissed (already covered)

### Beta-smoothed Bayesian priors
SSI Booster uses beta-smoothed priors for scoring confidence. Tilth's DSPy + GEPA stack (A6, locked) already covers this — GEPA's offline Card refinement handles prior estimation and evidence weighting. No additional value from pulling in a second prior-smoothing approach.

### Noise filtering
SSI Booster filters noisy/low-quality signals before scoring. Editor R2 (clarity pass) already handles this for Tilth — jargon flagging, goal/output/outcome/objective sorting, and structural cleanup serve the equivalent noise-reduction function in the grant-writing domain.

## Two things dismissed outright

### DoT (Diagram of Thought) as runtime gate
SSI Booster's DoT-informed scoring is statistical and non-deterministic. Using it as a Logician gate would violate the determinism contract (Logician = deterministic Python + Cedar, fail-closed, zero LLM tokens). The per-sentence groundedness *pattern* was worth pulling as a dev diagnostic (item 3 above), but the DoT scoring mechanism itself stays out.

### Hybrid RAG
SSI Booster uses hybrid RAG (dense + sparse retrieval). Scribe's evidence needs are served by PROJECT_CONTEXT + RFA text — both are small, structured documents that don't require sophisticated retrieval. BM25 against a known corpus is sufficient. Hybrid RAG adds complexity (embedding model dependency, vector store) without proportional value for Tilth's use case.

## Two design parallels flagged for later stages

### Cultivator person-fact aggregation (Stage 2)
SSI Booster aggregates per-person activity signals into composite profiles. At Stage 2 (Twelve Tilths fleet — each client's Golden Quill runs multi-seat Cultivator for their own employees, per CLAUDE.md § "Five-stage product arc"), Cultivator will aggregate per-employee voice/photo/text captures into per-person work records *within a single client's Tilth*. The aggregation pattern — normalize, dedup, timestamp, attribute — is structurally similar. Worth revisiting when Stage 2 design begins.

### Sovereign Node commons evidence chains (Stage 5)
SSI Booster's multi-source evidence threading (linking claims to multiple supporting signals with confidence scores) maps to the Sovereign Node commons's future role coordinating opt-in cross-Tilth research. At Stage 5, the Sovereign Node commons will need evidence chains that span multiple Tilth instances while respecting consent tiers (my-eyes-only / matchable-to-opportunities / composable-with-others). The chain structure is similar; the consent layer is Tilth-specific. *(Naming updated 2026-05-06: previously "MaatAI" — retired as a name. The Stage-5 commons is now "Sovereign Node" without LLC suffix; disambiguate from "Sovereign Node LLC," the parent legal entity.)*

## Flamewalker Protocol (FWHP) connection

The SSI Booster repo references the Flamewalker Hypothesis Protocol — a multi-AI adversarial epistemology framework designed for scientific workflow integrity. Several conceptual mappings to Tilth:

### Protocol-vs-theory separation
FWHP distinguishes the *protocol* (how knowledge is validated) from the *theory* (the knowledge itself). The Codex Universalis is the theoretical framework FWHP protects. This maps directly to Tilth: the system (Five Laws, Four Rules, Council pipeline) is the protocol; the grants are the output/theory. The protocol validates the output, not the other way around.

### Null-model baseline → future Judge feature
FWHP's null-model baseline concept: score a baseline/null hypothesis against the same criteria, then measure delta as the value metric. Future Judge feature: score a null draft (template-only, no substance) against the same rubric. The delta between null-draft score and real-draft score = the value Scribe actually added. This is a calibration tool, not a gate — helps diagnose when Scribe is adding boilerplate without substance.

### Explicit falsification channels → Law 5 strengthening
FWHP mandates explicit falsification channels — every claim must have a defined way it could be proven wrong. This maps to strengthening Law 5 with per-claim falsifiability criteria: for each substantive claim in a Scribe draft, can the claim be verified or falsified against PROJECT_CONTEXT? The NER gate (item 1) is a first step; per-claim falsifiability is the broader principle.

### "I do not know" discipline → confidence declarations
FWHP requires explicit "I do not know" declarations rather than silent gap-filling. Maps to Tilth: Scribe should declare confidence per section — which sections are grounded in PROJECT_CONTEXT, which are operator-provided framing, which are bridging language that could be wrong. The explain-grounding diagnostic (item 3) is the dev-side implementation; confidence declarations per section would be the production-side expression.

### Code Thesis Committee mapping
FWHP's multi-AI adversarial review maps to Tilth's Code Thesis Committee (§3 of engineering process). Both use multiple independent reviewers from different model families to reduce single-model bias. FWHP formalizes this as epistemology; Tilth implements it as engineering process. The structural parallel validates Tilth's cross-family review requirement (L-003).
