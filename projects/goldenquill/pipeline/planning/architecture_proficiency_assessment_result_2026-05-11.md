---
title: Architecture Proficiency Assessment — Result
filed: 2026-05-15
author: Cowork Opus 4.7
parent_prompt: pipeline/planning/architecture_proficiency_assessment_prompt_2026-05-11.md
evidence_pack: pipeline/validation/architecture_proficiency_2026-05-11/evidence_pack.md
sota_baseline: pipeline/research/advancements_scan_2026-05-15.md (60-day window mid-March → mid-May 2026)
authoring_posture: single-Claude synthesis; advancements scan was Cowork Opus 4.7 in a parallel session (same model family, different surface) — recommend operator dispatch cross-family verify if adversarial rigor on the scoring is wanted; per /AGENTS.md, Section E carve-out is for LOCKed amendments and this is an informational assessment, not an amendment
status: complete; final scores below
beta_thesis: Beta = 128 GB Golden Quill units on real customer desks. The assessment is read through that lens — what makes the unit on a desk effective, stable, token-efficient, and memory-competent — not against dev hardware or Stage-5 horizons.
---

# Architecture Proficiency Assessment — Result

## The Beta thesis (operator pin, leads the assessment)

**A Beta deployment is a 128 GB Golden Quill on a real customer's desk, running real cycles for real grants under real BYOK bills.** It is not Josh's M1 8 GB dev box. It is not a Founding-12 fleet rollout. It is not Stage-5 commons. It is one machine, one operator, one Tilth, in one office — and that unit needs to be **the most effective, stable, token-efficient, memory-competent unit possible** before it ships.

Re-read each dimension below through that lens. *"Effective"* means the cycle ends with a fundable proposal. *"Stable"* means F-code gates fail closed without taking the appliance down. *"Token-efficient"* means the customer's BYOK bill is small enough not to be a buying objection. *"Memory-competent"* means cycle N+1 starts with everything cycle N learned, not from scratch.

Against that thesis, the scoring below highlights three load-bearing realities:

1. **Memory competence is the weakest dimension (4/10) and it is the most exposed in a desk-Beta deployment.** A customer who drops 500 documents at onboarding and then submits 6 grants in the first quarter will hit MEMORY.md overflow, fragmented-13-register retrieval, and dormant Reflection Packet within weeks. The architecture has the shape; it does not have the running surface.
2. **Token-efficiency is sound at the substrate layer but blind at the cycle layer.** The customer's BYOK bill is the buying objection — and Tilth has no per-cycle cost KPI to show "this proposal cost you $X to write." That's a sales gap as much as an engineering gap.
3. **Stability is the strongest implicit dimension** — 1869 tests pass, Cedar fails closed, Logician deterministic gates have no token cost, signed-asset trust chain is genuinely ahead of where industry just-realized-it-needs-to-be. **This is what Beta currently ships well on.**

The roadmap section is reordered around the Beta lens at the bottom of this document.

## Executive Summary

**Verdict: Tilth's architecture is stable and structurally past adolescence, but it is not yet memory-competent enough to ship on a customer's desk and survive their first year of cycles. Total score 47 / 80.**

The substrate choices (Pydantic AI + Logfire + Ollama/vLLM + GEPA + Cedar Logician) are convergent with where the field landed in 2026 Q1-Q2 — not lucky bets, correct ones. The signed-asset trust chain + classification-register discipline + deterministic Logician gates are *ahead* of where industry just-discovered-it-needs-to-go after the MCP tool-poisoning disclosures. The Hermes Reflective Phase shipping in May validates the Reflection Packet design LOCKed today.

But operationally, Beta-readiness has a memory-competence problem. The Reflection Packet is LOCKed but DORMANT — cross-cycle learning is operator-curated only today. Memory spans 13 registers with no unified retrieval API and is overflowing its own context budget in **this very session**. Multi-modal coverage is documents-only (audio coming v0.2; video, image generation, presentation generation, social-media output have zero design surface). The §0.5 Interface Index at 505 runtime-live rows / 102 KB and ~110 F-codes across ~20 families is, by any honest read, partially ceremonial. The KnowQL 1:1-mapping claim from the advancements scan is too generous — Tilth shares **directional** convergence with KnowQL's six primitives, not primitive-level equivalence.

**Top 3 right (what Beta ships well on):** sovereignty + signed-asset trust chain (ahead of industry post-MCP-poisoning); Logician deterministic gates (zero token cost, fail-closed stability); cross-family Thesis rigor as default (catches what same-family review misses).
**Top 3 wrong (what threatens Beta on a real desk):** memory architecture fragmented across 13 registers without unified API (Dim 8 = 4/10); per-cycle token-cost KPI absent (Dim 1 — sales objection); §0.5 ceremony at 505 rows exceeds value-at-risk per surface (Dim 6).
**Top 3 missing (real customer-blocking gaps):** Reflection Packet runtime-on (LOCKed but dormant — cross-cycle learning today is operator-curated only); OCR / VLM-based parsing for legacy scanned RFAs (real onboarding-corpus degradation); operator-facing past-grant portfolio query surface (a Founding-12 customer with 5+ years of history will ask in onboarding hour 1).

---

## Per-Dimension Scoring

### Dimension 1 — Token Efficiency

- **Raw score: 6 / 10**
- **Verdict:** Substrate choice is the cost leader and the discipline is institutionalized; but no per-cycle KPI surface assembles the win into something Josh or a paying customer can quantify.
- **SOTA delta: AT-PARITY** (substrate); **BEHIND** (KPI surface).

**Top 3 failure surfaces:**
1. **No token-spend-per-cycle KPI.** session_log.jsonl tracks turns, files, template references, self_check_failures — but **not input/output tokens by provider, not $-cost per cycle, not cache-hit rate joined against the spend.** The Coefficient Registry (§17 WPFA) computes per-CALL watt-hours-per-token + counterfactual dollars; the per-CYCLE rollup that answers *"what did this grant cost to write"* does not appear to be assembled from CycleReceipt today. Verify: read `pipeline/vault/sub_kinds/__init__.py` for CycleReceipt fields.
2. **LOCKed amendment text pasted verbatim into handoff prompts.** L-002 forbids this; compound-LOCK rounds at rows 205-208 / 211-214 / 216-218 still risk it because of paired-commit volume. The transparent-disposition pattern (row-170 FOLD-IN-at-LOCK) compounds the surface area each Cycle 2 audit must absorb.
3. **MEMORY.md actively overflowing in this very session.** System reminder this turn: "35.6KB (limit: 24.4KB) — only part of it was loaded." The memory architecture is exceeding its own context budget. The consolidate-memory skill exists but does not appear to run on any trigger other than operator invocation.

**Top 3 missing items:**
1. A `tilth metrics cycle-cost <cycle_id>` CLI surface that joins session_log + cache-ledger + Coefficient Registry into one number.
2. LLMLingua-class prompt compression (20×) in the council inner loop — industry-standard, not yet adopted.
3. Semantic caching (Redis LangCache pattern: ~73% cost reduction on high-repetition workloads) — Anthropic prompt-caching covers some of this for `anthropic/*` paths; nothing covers Groq + Google paths.

**Priority tier: P1-V0.2-FIRST-WAVE** for the cycle-cost CLI; **P2-V1.X** for compression + semantic cache.

---

### Dimension 2 — Sorting + Parsing Data After Upload at Scale

- **Raw score: 5 / 10**
- **Verdict:** Sound architecture for clean documents at small scale; absent OCR + absent dedup + absent batch-classification UX means messy real-world drops will degrade or fail.
- **SOTA delta: BEHIND** — industry moved to VLM-based parsing (PaddleOCR VL, IBM Granite 4.0 3B Vision at ~99% accuracy on mixed-layout PDFs). Tilth's pypdf + python-docx + openpyxl substrate is a fixed-quality lower bound.

**Top 3 failure surfaces:**
1. **Scanned PDF / OCR substrate is absent.** Legacy grant archives — exactly the corpus a Founding-12 customer will drop on white-glove — are dominated by scanned submissions. `pipeline/blueprint/v0.1/section_11_intake.md` lines 366-378 specify FAISS-or-Chroma + bge-large-en-v1.5, but nothing in the substrate handles `pypdf.extract_text()` returning empty on a scanned PDF. The fabrication-resistance gates (F-EXTRACTOR-FABRICATION sub-tags) catch hallucinated extractions but cannot rescue extractions that don't happen.
2. **Substrate not pinned in pyproject.toml.** `chromadb`, `faiss-cpu`, `sentence-transformers`, `bge-large-en-v1.5` — none of these are in `[project.dependencies]`. §11 spec calls for them. Same shape as the Logfire D-RB-01 finding from the 2026-05-15 daily log: the spec leads the pin. This is finalizable, not architectural rot — but it is a v0.1 Beta finalization residual that should land before first paid customer.
3. **No documented scale benchmark.** 500-doc and 5,000-doc BULK_INGEST wall-clock on M3 Ultra 128GB are unknown. Mistral 7B is fine for a 100-doc onboarding; what happens at 10 years × 50 docs/year × hand-scanned files? Unknown. No measured cliff.

**Top 3 missing items:**
1. **VLM fallback path at Intake.** When pypdf / python-docx returns degraded confidence, invoke local VLM (PaddleOCR VL or IBM Granite 4.0 3B Vision) as a second pass. The advancements scan already flagged this as a medium refactor (§9 item 6). Sovereignty preserved (local VLM); broadens document floor materially.
2. **Cross-document deduplication.** Drop a folder containing 3 copies of the same RFA (a real onboarding scenario); current behavior is unknown. The compound-key collision-detect at F-INTAKE-EMBEDDING-NS-MISMATCH `.compound_key_collision` covers cross-org leakage but not intra-org duplicates.
3. **Batch-classification UX.** INCREMENTAL_INGEST defaults each new doc to `confidential` per F-CLASS-NEW-FACT-UNCLASSIFIED. At 5,000-doc onboarding, one-keystroke-per-doc reclassification is unworkable. A batch-by-folder / batch-by-pattern surface is missing.

**Priority tier: P0-BLOCK-ALPHA** for VLM fallback (real customer-blocking on scanned RFAs); **P1-V0.2-FIRST-WAVE** for batch-classification UX; **P1** for substrate pinning.

---

### Dimension 3 — Multi-Modal Data: Sort / Store / Use / Output

- **Raw score: 5 / 10**
- **Verdict:** Documents are mature; audio has spec + Code Slice 3 landed; everything else (video, image generation, presentation output, social-media output) has **zero design surface**.
- **SOTA delta: BEHIND** on video / image-gen / presentation / social-media (industry shipped: Sora 2 limited release, Krea 2 image-gen, Adobe Firefly Assistant, Magic Pointer interaction model); **AT-PARITY** on audio with Voxtral 3B drop-in pending; **AT-PARITY** on documents; **AHEAD** on signed-PDF buyer-receipt (WPFA).

**Modality-by-modality (per evidence pack matrix):**

| Modality | Status | Honest read |
|---|---|---|
| Audio inbound (voice) | §13 v1 LOCKED, Slice 3 landed | Mature. Voxtral 3B upgrade is a small adjustment per scan §9. |
| Audio outbound (Twilio voice) | §13 v1 LOCKED | Mature. |
| Audio attachment to grant | None | Real but rare gap. |
| Video inbound | None | Zero surface. Some funders accept video pitches. Real but bounded gap. |
| Video outbound (pitch generation) | None | Zero surface. Magic Pointer / TML / Perceptron Mk1 interaction-model class is emerging; v1.x distraction risk per scan §8. |
| Images (photos in reports) | §2 v7.2 + §14 photo_gallery | Spec present; **EXIF / GPS / PII handling is undocumented**. Drop a photo of a beneficiary's farm with embedded GPS → unknown silent leak. Real gap. |
| Images (generation, branded submissions) | None | Zero surface. `canvas-design` / `algorithmic-art` skills available as tools, no architectural slot. |
| Reports (DOCX/PDF) | §14 v1 SPEC LOCKED + Slice 3 LANDED | Mature. |
| Presentations (PPTX) | None | Zero surface. WPFA buyer-PDF is the closest, but it's a single-page sales receipt, not a board-report deck. |
| Social-media blurbs (post-award) | None | Zero surface. Would belong as Scribe sub-mode or new track in §5 v8 track registry. |
| Documents (DOCX/PDF/XLSX in/out) | §11 + §12 | Mature; attachments + Foundant/Submittable/Fluxx deferred to v1.1. |

**Top 3 failure surfaces:**
1. **EXIF / GPS / PII metadata leak through `photos` sub-kind.** A beneficiary's home GPS would silently flow through §14 photo_gallery into a funder-facing report. F-REPORT-OUT-OF-SCOPE-DRIFT covers narrative drift; nothing covers image-metadata drift.
2. **Whisper privacy.** §13 Data Collector outbound-voice substance routes local under all postures per v7.0.10. But the *audio file itself* — does it persist? Where? Under what classification? Unclear from the LOCKed §13 surface.
3. **Video and presentation are absent.** No graceful-degradation path. A funder that accepts only video pitches gets a "we don't do that" response.

**Top 3 missing items:**
1. EXIF / GPS strip enforcement on `photos` sub-kind insert.
2. PPTX output track in §5 v8 track registry (board reports, pitch decks).
3. Social-media-blurb track (or Scribe sub-mode) for post-award announcements.

**Priority tier: P0-BLOCK-ALPHA** for EXIF strip (real PII leak path); **P1-V0.2-FIRST-WAVE** for Voxtral 3B drop-in; **P2-V1.X** for PPTX / social-media tracks.

---

### Dimension 4 — Effectiveness of the Grant-Cycle Pipeline End-to-End

- **Raw score: 6 / 10**
- **Verdict:** The submission half is mature and structurally sound; the between-cycle half is LOCKed but largely dormant — cross-cycle learning is operator-curated today.
- **SOTA delta: AT-PARITY** on the council-of-six + cross-family + rubric-bank pattern (Harvey LAB validates the shape); **BEHIND** on shipping the reflective loop (Hermes v0.13.0 ships automatic reflection in May 2026; Tilth's Reflection Packet is LOCKed-but-DORMANT until v0.2 first wave).

**Operator-touch count, honest read:**
- v0.1 Beta active path: ~5-8 touches per cycle (classification sign-off, per-doc class at Intake INCREMENTAL drop, Scout candidate review, KGIE preflight review, section approvals, claim-evidence map signature, final Submit click).
- v0.2 first wave (Data Collector + Report Generator landing): ~10-15 touches per cycle.
- At Stage-2 Founding-12 fleet: 12 × ~10 touches × N cycles/year = unsustainable for a solo operator. The architecture assumes one operator per Tilth at Stage 1; multi-seat Cultivator per Tilth is Stage 2 — that's the right call, but the operator-load arithmetic should be in the alpha-readiness checklist explicitly.

**Top 3 failure surfaces:**
1. **Reflection Packet is DORMANT (18 of 19 F-PACKET-* gates raise NotImplementedError).** Cross-cycle learning between grant 1 and grant 2 is **operator-curated only today** via lessons.md + L-NNN. The infrastructure is LOCKed and pre-staged (`pipeline/handoffs/ws_reflection_packet_v0_2_first_wave_handoff_2026-05-15.md`); the runtime is not on.
2. **Funder Intelligence DB + Match DB not built.** Architecture v7.0.5 + Archivist v1.x carry both as SPEC LOCKED. A repeat USDA SCBGP submission in 2027 will not benefit from the 2026 submission's accumulated funder intelligence except by operator memory.
3. **Context loss Scribe → Editor.** Rule 4 "Clean Output" strips LLM self-commentary; this is correct for the artifact handoff but means Scribe's *rationale* doesn't reach Editor. Editor re-derives intent from the draft alone. The intra-cycle reasoning continuity is structurally lossy.

**Top 3 missing items:**
1. Ship the Reflection Packet v0.2 first-wave compound LOCK (rows 216-218 → live; pre-staged handoff exists).
2. Cross-cycle funder-officer continuity surface (program officer's name from cycle N → reviewer comment context in cycle N+1).
3. Scribe-to-Editor rationale-carry-over channel (a structured "writer's intent" sidecar that Editor can read without violating Clean Output discipline).

**Priority tier: P0-BLOCK-ALPHA** for Reflection Packet v0.2 first wave (the architecture is ceremonial without it); **P1-V0.2-FIRST-WAVE** for funder-officer continuity; **P2-V1.X** for rationale-carry-over.

---

### Dimension 5 — What "Ultimate Grant Writing Machine" Means That We're NOT Covering

- **Raw score: 7 / 10** (this is an inventory-completeness score, not a quality score)
- **Verdict:** The gap inventory is thoroughly mapped; the question is which gaps are real customer-blockers vs vision-creep.
- **SOTA delta:** N/A — this is the missing-from-architecture dimension; SOTA delta is folded into the specific items.

**Gap inventory (ranked by likelihood-of-real-customer-blocking):**

| # | Gap | Tag | Likely-blocking? |
|---|---|---|---|
| 1 | Multi-language support (Spanish for federal grants in PA → Latino-led co-ops) | BLIND-SPOT | **Yes — real customer blocker.** |
| 2 | OCR / VLM-based parsing for scanned legacy archives | BLIND-SPOT | **Yes — degrades silently on real customer corpora.** |
| 3 | Operator-facing past-grant portfolio query surface | BLIND-SPOT | Likely. Founding-12 customers with 5+ years of submission history will ask. |
| 4 | Funder-due-diligence rebuttal slot (reviewer-comment cycle) | SCOPE-EXCLUDED | Goes back through Scribe ad-hoc today. Workable. |
| 5 | Slide-deck production from operational data | BLIND-SPOT | Some customers will ask for board reports. |
| 6 | Social-media post-award announcement generation | BLIND-SPOT | Likely. |
| 7 | Video pitch generation | SCOPE-EXCLUDED | Rare blocker. Decline politely. |
| 8 | Image / infographic generation | SCOPE-EXCLUDED | Rare blocker. |
| 9 | Live multi-operator collaboration | SCOPE-EXCLUDED | A1 single-operator constraint structurally rules out at v0.1. |
| 10 | Real-time funder Q&A capture | SCOPE-EXCLUDED | Operator-manual is workable. |
| 11 | Automated donor-newsletter generation | VISION-CREEP | Donor work is not grant work. |
| 12 | Partner-vetting workflow beyond M11 Entity Research Pass | SCOPE-EXCLUDED | M11 + operator-manual is workable. |
| 13 | Sub-grantee / pass-through reporting | SCOPE-EXCLUDED | Light coverage at Data Collector v0.2 horizon. |
| 14 | Grant-writing pedagogy for new-to-funder operators | BLIND-SPOT | Real for Founding-12 customers who are not Josh-tier veterans. |

**Top 3 real customer-blocking gaps:** multi-language, OCR/VLM, past-grant portfolio query.

**Priority tier: P0-BLOCK-ALPHA** for OCR/VLM (per Dim 2 P0); **P1-V0.2-FIRST-WAVE** for past-grant portfolio query (Match DB is SPEC-LOCKED — needs operator-facing surface); **P1** for multi-language (real customer blocker for a known PA segment).

---

### Dimension 6 — Technical Design Depth (Architecture Coherence vs Complexity Tax)

- **Raw score: 7 / 10**
- **Verdict:** Real design depth, but the LOCK ceremony is borderline-out-of-proportion to value-at-risk per surface; §0.5 Interface Index has crossed the threshold where governance theater is likely present.
- **SOTA delta: AHEAD** on signed-asset trust chain + Cedar + Logician (industry is scrambling to add this post-MCP-poisoning); **AT-PARITY** on rubric-bank pattern (Harvey LAB validates).

**Quantitative state:**
- 218 lock_history rows; 13 v0.1+v0.2 rounds at full live cross-family rigor between 2026-05-09 and 2026-05-15 (six days, ~one round per half-day at peak).
- §0.5 Interface Index: 505 runtime-live rows / 818 lines / 102 KB.
- ~110 F-code modules across ~20 families.
- 1869 tests passing on .venv 3.14.
- Cross-family Thesis economic cost: ~2 cycles × 3 seats × ~5K tokens × Gemini-pricing-dominated × 13 rounds = real money. Compute exact $ in Part 2 follow-up if useful.

**Top 3 failure surfaces:**
1. **§0.5 Interface Index has crossed the governance-theater threshold.** 505 runtime-live rows is more than any single agent can hold; the index is being curated by paired-commit ritual at every section LOCK without a verifiable runtime-import-test that each row maps to imported code. The reviewer should grep-sample 10 random rows from rows 471-505 (newest); if even 30% fail to map to an importing module, the index is partially paperwork.
2. **Four orthogonal F-* gate families (F-CLASS / F-WPFA / F-PACKET / F-REFLECTION) with AST-lint cross-family-import ban (Path B naming reconciliation).** The orthogonality is organizational hygiene; the AST-lint ban is real enforcement; but the *runtime isolation payoff* of having four families instead of one with sub-tags is not obvious. Could collapse to a single `F-RUNTIME-*` family with `family=class|wpfa|packet|reflection` discriminator without losing safety. Saving: less paired-commit volume per amendment.
3. **L-005 two-audit cycle's "fold-in-at-LOCK" workaround is a third round in disguise.** The transparent-disposition pattern from row 170 lets Cycle 2 NEW probes be FOLDED-IN at LOCK rather than triggering Cycle 3. Functionally: the audit didn't stop at two cycles, it just renamed the third pass. The L-005 "two-cycle" claim is honest only in form. This is fine — the discipline catches more — but the framing should match the reality.

**Top 3 missing items:**
1. A `tilth governance audit` CLI that randomly samples §0.5 rows and verifies each maps to a runtime import. Would convert §0.5 from paperwork-prone to paperwork-resistant.
2. A complexity-tax KPI: F-codes per active module, lines of §0.5 per F-code, $-per-round of cross-family Thesis. The Alpha Readiness Checklist tracks ops items; the architecture itself has no self-instrumentation for ceremony cost.
3. A tiered-rigor pattern: full 3-seat cross-family dispatch for substantive amendments; single-non-Anthropic seat for narrow correctives (rows 198-199 / 209-210 / 211-214 style). The "every amendment is 3-seat-mandatory" default isn't articulated in /AGENTS.md; should be.

**Priority tier: P2-V1.X** — none of this is alpha-blocking, but the trajectory at 218 rows is steep enough that a governance-audit pass at v1 would be wise.

---

### Dimension 7 — The Brain: Council Topology + Reasoning

- **Raw score: 7 / 10**
- **Verdict:** The council substrate is real on disk (full module trees for Scribe / Editor / Judge / Red Team with cross_rubric_dispatch + sfr_emitter + provider adapters); the cross-family rigor + deterministic Logician + >10pt-split escalation is genuinely ahead of MAR / A-HMAD in auditability; what's missing is funder-mindset modeling and intra-cycle debate.
- **SOTA delta: AHEAD** on cross-family rigor + Logician determinism; **AT-PARITY** on rubric-bank pattern (Harvey LAB); **BEHIND** on intra-cycle multi-agent debate (A-HMAD consensus-optimizer; MAR persona-guided critics).

**Substrate verification:** `pipeline/seats/{scribe,editor,judge,red_team}/` each has a full module tree on disk including `logician_wiring.py`, `sfr_emitter.py`, `cross_rubric_dispatch.py`, and provider adapters (anthropic / groq / google). This is not a sketch — it's a built substrate.

**Top 3 failure surfaces:**
1. **Funder-mindset is not modeled.** Scribe's funder-dialect code-switch (conservative / centrist / progressive / soul-fire per Law 4) is a *register* move, not a *mindset* move. A USDA reviewer and a Surdna Foundation reviewer differ not just in vocabulary but in what counts as evidence, what counts as risk, what counts as a viable timeline. The architecture has dialect; it does not have mindset.
2. **No intra-cycle debate.** Cross-family rigor operates across audit cycles (Cycle 1 → Cycle 2). Within a single seat-cycle there is no Scribe-vs-Red-Team back-and-forth. MAR and A-HMAD let agents argue N rounds before consensus; Tilth has one-shot Scribe → Editor → Judge → Red Team → Logician. The audit cycle catches the gross errors; the conversational debate would catch the subtle ones.
3. **Stakeholder-perspective rotation is thin.** The council has reviewer-voice (Judge), adversary-voice (Red Team), and writer-voice (Scribe). It does *not* have program-officer-voice, future-grantee-three-years-in-voice, board-voice, legal-counsel-voice. Pre-submission "what would a program officer ask about this" review is operator-manual.

**Top 3 missing items:**
1. **Funder-mindset card per CIC × CLC.** The Capital Logic Cards taxonomy (TILTH-CLC-00) names eight funder logics; the *mindset* of each (what counts as evidence, what counts as risk) is not encoded.
2. **Intra-cycle debate option for high-stakes submissions.** A "deliberation mode" where Scribe and Red Team argue N rounds before Judge scores, gated to federal long-form / large-award by operator selection.
3. **Stakeholder rotation seat or sub-mode.** "Pre-submission, rotate through 3 stakeholder voices for any unaddressed concerns" — could be a Scribe sub-mode or a Red Team sub-mode.

**Priority tier: P2-V1.X** for funder-mindset card (real value, not alpha-blocking); **P2** for intra-cycle debate (track A-HMAD); **P3** for stakeholder rotation.

---

### Dimension 8 — Effective Memory

- **Raw score: 4 / 10**
- **Verdict:** The memory architecture is the weakest dimension — 13 registers, no unified retrieval API, MEMORY.md actively overflowing right now, Reflection Packet LOCKed but DORMANT. The architecture exists; the integration is fragmented.
- **SOTA delta: AT-PARITY** in concept (Anthropic Memory + Hermes three-layer pattern + Letta three-tier all converge on the same shape Tilth has); **BEHIND** on shipping (Hermes Reflective Phase is automatic and live; Tilth's is LOCKed and dormant); **BEHIND** on unified retrieval (Mem0 is a "bolt-on memory layer"; Tilth makes consumers walk 13 registers).

**13 registers verified on disk:** Cowork session memory, lessons.md + lessons.json, daily_logs, lock_history, PROJECT_CONTEXT per-org, KFR per-org, classification register per-org, Reflection Packet (DORMANT), Funder Intel DB (not built), Match DB (not built), cache-ledger, session_log, CycleReceipt.

**Top 3 failure surfaces:**
1. **MEMORY.md is overflowing in this very session.** System reminder this turn: "35.6KB (limit: 24.4KB) — index entries are too long. Only part of it was loaded." This is happening **during the assessment**. The memory architecture is exceeding its own context budget, observably, today. consolidate-memory exists as a skill; it does not appear to fire on any threshold trigger. This is a Dim-8 failure visible in real-time.
2. **No unified retrieval API.** "Find every grant we've submitted to USDA SCBGP" — the path today is operator browses `orgs/<slug>/vault/grants/` tree by hand. There is no `tilth memory query` surface. Each register has its own access pattern (grep / read / yaml.load / sqlite open). Per-cycle this is fine; cross-cycle this is archaeology.
3. **Cross-cycle learning is operator-curated only.** Reflection Packet DORMANT. Funder Intel DB not built. Match DB not built. Today's cross-cycle learning surface = lessons.md + L-NNN. Both are operator-written. The infrastructure for automated cross-cycle learning is LOCKed at row 218; the runtime is not on.

**Top 3 missing items:**
1. **A `tilth memory query` CLI** that takes (org, kind, filter) and queries the appropriate register or unions across registers under Law 3 isolation. Mem0-shape "bolt-on memory layer" but local-sovereign-only.
2. **MEMORY.md auto-consolidation trigger** on size threshold (e.g., >20 KB → run consolidate-memory skill). Today: operator-manual.
3. **Backup/restore story across all 13 registers.** Sovereignty Promise says "the operator would still have their machine, their data, their keys, and their grants" — but what's the actual procedure if the M3 Ultra's SSD fails? Per-register restore? Single-snapshot? Encrypted offsite? Customer contract item per Alpha Readiness Checklist item 28; not architectural — but the architecture should at least name what survives the restore.

**Priority tier: P0-BLOCK-ALPHA** for Reflection Packet v0.2 first wave (memory architecture is performative without it); **P0** for backup/restore story (customer-contract item); **P1-V0.2-FIRST-WAVE** for unified retrieval CLI; **P1** for MEMORY.md auto-consolidation.

---

## KnowQL Critical Assessment — Is the Tilth ↔ KnowQL Mapping Genuinely 1:1?

The advancements scan §8 surface map claims KnowQL's six primitives "map almost one-to-one onto Tilth primitives." The operator surfaced this as the **load-bearing question**: validation or superficial similarity?

**Honest answer: it's directional convergence, not primitive-level equivalence. The "1:1" claim is too generous and should not be used in customer-facing copy without qualification.**

Primitive-by-primitive:

| KnowQL primitive | Claimed Tilth analog | Honest read |
|---|---|---|
| **intent** | RFA-derived intent (Law 1) | **Different granularity.** KnowQL `intent` is an *explicit per-query parameter* — the agent declares "I want to know X about Y." Tilth's intent is set at the *cycle level* (write a proposal for this RFA) and is not a per-retrieval-call parameter. **Same concept, different granularity. Conceptual match, not primitive match.** |
| **filter** | Classification register | **Different semantic.** KnowQL `filter` is a *per-query content selector* (only USDA-funded grants from 2024+). Tilth classification register is an *access-control matrix* (this fact is confidential, never route to cloud). **Adjacent surface, different primitive.** |
| **provenance** | KFR verbatim-quote-with-page + content-hash | **Genuine 1:1.** Both systems require every retrieved fact to carry its trace back to source. Tilth's M11 Entity Research Pass + KFR are doing exactly what KnowQL provenance does. |
| **output shape** | Pydantic AI structured output | **Conceptually equivalent.** Pydantic AI is a generic structured-output runtime; KnowQL is a query-shape declarative. The mechanism is shared (structured schemas over LLM output). **True match.** |
| **confidence** | Judge dimension scores + KGIE preflight | **Wrong layer.** KnowQL `confidence` is the *system's confidence in the retrieved knowledge* (pre-draft). Tilth's Judge scores are *post-draft evaluation*. The honest Tilth analog is **M11's HIGH/MEDIUM/LOW confidence tier** on each fact dossier, not Judge. **Adjacent surface, wrong layer in the mapping.** |
| **budget** | Classification-driven routing (v7.0.10) | **Weak match.** KnowQL `budget` is a *per-query cost cap*. Tilth's classification-driven routing is *which model to call*, not *how much it costs*. Tilth has no per-call $-budget primitive — it has deployment-level posture. **Different primitive; sovereignty posture is not a budget control.** |

**Tally: 2 of 6 are genuine matches (provenance, output shape). 3 of 6 are conceptually adjacent but structurally different (intent, filter, confidence). 1 of 6 is weakly related (budget).**

**Implication for Tilth strategy:**
- The architectural *direction* is convergent — Tilth's pipeline does the work KnowQL standardizes (compile knowledge upstream of agent retrieval). This is real validation.
- The *primitive set* is not equivalent. Tilth would need to add: (a) explicit per-query intent declaration, (b) per-query content filter, (c) per-fact confidence-tier exposure to consumers, (d) per-call cost cap. None are large additions; none exist today.
- The "RAG era is ending" VentureBeat framing is correct directionally; Tilth's Scout DISCOVER → VERIFY (live re-fetch, not pre-chunked top-k) is the right architectural posture, but Tilth doesn't *expose its retrieval contract* as a documented schema.

**Recommendation:** Add a v1.x architecture amendment that documents Tilth's retrieval contract as an explicit KnowQL-analog schema. Don't claim 1:1 in customer copy until the four missing primitives are real. The Pinecone-Marketplace "Grants vertical unoccupied" observation is genuine strategic opportunity — but the move that makes it actionable is documenting the retrieval contract, not asserting the mapping.

---

## Hermes Reflective Phase — Convergence Read

Hermes Agent v0.13.0 shipped automatic reflection-after-task in May 2026 with 30% migration from OpenClaw in <90 days. The pattern: 15 tool calls → pause → reflect on what worked → write a Markdown skill file capturing the pattern → refine next time. Three memory layers (session / episodic SQLite / procedural skills).

**Tilth's Reflection Packet (LOCKed today rows 216-218):** structurally more rigorous than Hermes — Ed25519 signed, classification-register cross-checked, CycleReceipt-sibling, 19 F-PACKET-* gate primitives. **But: DORMANT.** 18 of 19 gates raise NotImplementedError at v0.1 hook.

**Honest verdict:** Hermes validates the *bet* (automatic reflection-after-task is the right shape for cross-cycle learning). Tilth's *discipline* (signed packets + classification-cross-check) is the differentiator. **But discipline without shipping is paperwork.** The v0.2 first-wave compound LOCK that activates Reflection Packet producer-flip is pre-staged at `pipeline/handoffs/ws_reflection_packet_v0_2_first_wave_handoff_2026-05-15.md` — getting that into runtime is **the highest-leverage Dim-4 + Dim-8 unblock in the roadmap**.

---

## Trillion Dollar Defensibility Framework — Tilth Map

Nate B Jones's four-axes squeeze (frontier labs moving down stack + consultancies moving up + systems of record exposing interfaces + PE as distribution) names five defensibility primitives that survive the squeeze:

| Defensibility primitive | Tilth posture | Honest verdict |
|---|---|---|
| **Workflow design** | Council of six + classification-driven routing + three postures + track registry | **Real, on disk.** |
| **Data access** | Local-only sovereignty + BYOK + per-org Vault + Law 3 isolation | **Real, on disk; differentiator vs all SaaS competitors.** |
| **Authority** | Cedar policy + operator Ed25519 sign-off + signed-asset trust chain | **Real, on disk; ahead of MCP ecosystem post-tool-poisoning.** |
| **Evals** | Judge rubric library + Red Team adversarial + Logician deterministic gates + 1869 tests | **Real, on disk; rubric-bank pattern Harvey LAB validates.** |
| **Audit trails** | lock_history + classification register signing + WPFA CycleReceipt + Reflection Packet schema | **Real, on disk; Reflection Packet DORMANT but other 3 live.** |

**Tilth checks every primitive Nate names.** This is the cleanest analytical frame for v1 Beta customer-facing differentiation. The frame is more useful than any single competitor comparison (Instrumentl / Grantable / Granted AI / Grant Assistant) because it predicts which competitors *will not survive the squeeze* — the SaaS-wrappers around third-party LLM APIs without their own data access / authority / audit infrastructure.

**Recommendation:** website + pitch deck + sales playbook should lean into this framing. Cite the source when used externally. The competitor table from advancements scan §7 plus this map is enough for a one-page sales differentiator.

---

## Over-Engineered Findings (≥3 required per rubric anti-flattery clause)

### OE-1 — §0.5 Interface Index at 505 runtime-live rows / 102 KB / 818 lines (Dim 6)

The §0.5 Interface Index is paired-commit'd at every section LOCK. It has grown from ~290 rows (row 187) to 505 rows (row 218) in 31 LOCKs — average 7 rows per amendment. **No automated test verifies that each row maps to a runtime import.** The amendment narrative at LOCK time names which rows are appended; nothing structurally prevents a row from being a ceremonial marker that no runtime module imports. At 505 rows this is below the threshold where any single Thesis seat can hold the index in working memory.

**Argument for heaviness exceeding value-at-risk:** the section LOCK protects the *interface contract*; the §0.5 row is an *index entry* about the contract. The index is one level of abstraction above the contract. If a row is wrong, the contract is still right. If a row is missing, the contract is still right. The §0.5 row is documentation, not enforcement. Treating it as enforcement-grade paired-commit is heavier than the failure surface justifies.

**Lighter alternative:** generate §0.5 from runtime declarations (Pydantic models + F-code module file names + AST-lint rule names) at LOCK time, rather than hand-curating it. The hand-curation cost compounds with surface size; the auto-gen cost is constant.

### OE-2 — Four orthogonal F-* gate families with AST-lint cross-family-import ban (Dim 6)

The Path B naming reconciliation discipline (F-CLASS / F-WPFA / F-PACKET / F-REFLECTION as four orthogonal families with AST-lint preventing cross-family imports) is organizational hygiene presented as enforcement. The *runtime isolation payoff* of having four families instead of one with sub-tags is not visible:
- F-CLASS-* and F-WPFA-* never interact at runtime (different surfaces entirely).
- F-PACKET-* and F-REFLECTION-* are explicitly sibling-not-nested with one cross-reference (`F-PACKET-SPAN-PROVENANCE-MISSING` ↔ `F-WPFA-SPAN-PROVENANCE-MISSING`).

Could collapse to `F-RUNTIME-*` with `family=class|wpfa|packet|reflection` discriminator without losing safety. Savings: less paired-commit narrative volume per amendment; lower Thesis Cycle 2 surface area; fewer rows to consolidate at consolidate-memory time.

**Counterargument:** Path B precedent was established to prevent semantic collision between F-CLASS-SPLIT-CONTEXT-LEAK and a hypothetical future F-PACKET-LEAK. The discriminator-collapse loses one bit of namespace separation. **Acceptable trade.**

### OE-3 — L-005 two-audit cycle's "fold-in-at-LOCK" workaround is a third round in disguise (Dim 6)

The row-170 transparent disposition pattern lets Cycle 2 NEW probes be FOLDED-IN at LOCK rather than triggering Cycle 3. In the recent §16 Reflection Packet LOCK (rows 216-218): "Cycle 2 Editor PASS + Judge PASS + Red Team PASS blocking:no (1 LOW F001 REJECTED-with-rationale)." In the recent §17 WPFA LOCK: "5 Cycle-2 NEW probes (RT-C2-05 path-traversal regex FIX-IN-PLACE LANDED + 4 documentary FOLD-INs)." The pattern is now standard.

Functionally: the audit didn't stop at two cycles. The third pass happens at LOCK time, just named differently. The L-005 "two-cycle, not three-round silent revision" claim is honest only in form.

**This is not necessarily wrong** — the discipline catches more findings than two strict cycles would, and the LOCK-time fold-in keeps the L-005 retry-cap from blocking on minor NEW probes. But the framing should match the reality: it's a three-pass audit with one pass folded into the LOCK commit rather than fired as a separate dispatch. Customer-facing or new-engineer-facing docs should not assert "we only do two audit cycles" when in practice the LOCK fold-in is a normalized third pass.

### OE-4 (bonus) — Compound-LOCK quadruples at peak velocity (Dim 6)

Row 205-208 (§17 v1 WPFA LOCKED 2026-05-11) was a compound *quadruple*: §17 v1 + §2 v7.4 Coefficient Registry + §4 v2.x.z F-WPFA-* + §0.5 v19. Four paired-commit siblings landing at the same lock_timestamp_utc. The amendment-dependency graph at LOCK time requires every seat in the Thesis dispatch to absorb all four sibling amendments. **Cognitive load at LOCK time scales with sibling count.**

Lighter pattern: serial-LOCK siblings with explicit ordering (LOCK §17 v1, then LOCK §2 v7.4, then LOCK §4, then LOCK §0.5) and forward-references between them. Trades atomicity for cognitive load. Atomicity may not be load-bearing if the runtime test suite enforces the integration anyway.

---

## Blind-Spot Inventory (≥3 required per rubric anti-flattery clause)

### BS-1 — Multi-language support (Spanish, federal grants) (Dim 5)

Zero architectural slot. USDA SCBGP in PA serves Latino-led co-ops where the operator is more fluent in Spanish than English. Federal grants accept Spanish submissions. Tilth's Scribe is English-only; Editor is English-only; Judge rubrics are English-only. This is not a v1.x luxury — it's a real PA-customer-segment blocker.

**Smallest move that helps:** Voxtral 24B (per advancements scan §3) is 100+ languages and Apache 2.0; landing Voxtral on inbound voice gets the bilingual operator voice → text path. The reverse path (English RFA → Spanish draft for operator → final review) needs Scribe to be bilingual or Editor to be a translator. The architecture has no slot for either.

### BS-2 — OCR / VLM-based parsing for scanned legacy RFAs (Dim 2 + Dim 5)

Per advancements scan §3 + §8: VLM-based document parsing (PaddleOCR VL, IBM Granite 4.0 3B Vision) is production-ready at 99% accuracy on mixed-layout PDFs. Tilth's substrate is pypdf + python-docx + openpyxl. A scanned RFA returns near-empty text via pypdf. The fabrication-resistance gates (F-EXTRACTOR-FABRICATION) catch hallucinated extractions but cannot rescue extractions that don't happen.

**Real customer scenario:** a Founding-12 customer with 10 years of legacy submissions, 60% scanned. Onboarding extracts 40% of usable history.

**Smallest move that helps:** medium refactor at §11 v1.2 to add a VLM fallback path when pypdf returns degraded confidence. Local VLM preserves sovereignty.

### BS-3 — Operator-facing past-grant portfolio query surface (Dim 4 + Dim 8)

Match DB is SPEC-LOCKED per v7.0.5; Funder Intel DB is SPEC-LOCKED; Reflection Packet is LOCKed. None of these have an **operator-facing query surface**. "Show me every USDA submission I've ever made, the award amount, the program officer, the reviewer comments, the lessons learned" is a question a Founding-12 customer with 5+ years of submission history will ask in the first onboarding call. The data shape to answer it is mostly LOCKed; the query CLI is undesigned.

**Smallest move that helps:** a `tilth portfolio query <filter>` CLI that joins org-level grant submissions across cycles. Doesn't need the Reflection Packet runtime to be on; can ship against existing KFR + lock_history + CycleReceipt + lessons.md.

### BS-4 — EXIF / GPS / PII metadata strip on `photos` sub-kind (Dim 3)

§2 v7.2 specifies `photos` as one of 7 SIMPLE sub-kinds. §14 v1 has `photo_gallery` composer. Neither specifies EXIF stripping. A beneficiary photo with embedded home GPS coordinates would silently flow through into a funder-facing report. F-REPORT-OUT-OF-SCOPE-DRIFT covers narrative drift; nothing covers image-metadata drift. This is a **real PII leak path**.

**Smallest move that helps:** a single AST-lint or pre-write hook on `photos` insert that strips EXIF unless operator explicitly opts to retain.

### BS-5 — Cross-document deduplication at Intake (Dim 2)

Drop a folder of 200 docs that includes 30 duplicate copies (a real onboarding scenario when an org dumps multiple Drive folders). Current behavior is unknown. The compound-key collision-detect at F-INTAKE-EMBEDDING-NS-MISMATCH `.compound_key_collision` covers cross-*org* leakage; nothing covers intra-org duplicates. Result: 30 redundant embeddings, 30 redundant KFR extractions for the operator to confirm.

**Smallest move that helps:** content-hash dedup at BULK_INGEST PRE-gate before embedding. Cheap.

---

## SOTA Delta Synthesis

| Dimension | Tilth posture vs SOTA 2026-05-15 |
|---|---|
| Dim 1 Token efficiency | AT-PARITY substrate; BEHIND on per-cycle KPI surface |
| Dim 2 Scale parsing | BEHIND — VLM-based parsing is now production-ready; Tilth pypdf-only |
| Dim 3 Multi-modal | BEHIND on vision-parse / video / image-gen / presentation / social-media; AT-PARITY on audio (Voxtral upgrade pending); AHEAD on signed-PDF receipt |
| Dim 4 End-to-end cycle | AT-PARITY council pattern; BEHIND on shipping reflective loop (Hermes shipped automatic; Tilth's is LOCKed-but-dormant) |
| Dim 5 Vision gaps | (inventory dimension; SOTA delta folded per gap) |
| Dim 6 Technical depth | AHEAD on signed-asset / Cedar / Logician determinism (post-MCP-poisoning industry-scramble); AT-PARITY on rubric-bank pattern |
| Dim 7 Council topology | AHEAD on cross-family rigor + Logician; BEHIND on intra-cycle multi-agent debate (MAR / A-HMAD consensus-optimizer) |
| Dim 8 Memory | AT-PARITY in concept; BEHIND on shipping (Hermes Reflective Phase live; Reflection Packet dormant); BEHIND on unified retrieval (Mem0 bolt-on; Tilth 13 fragmented registers) |

**Overall posture vs SOTA:**
- **Where Tilth is AHEAD:** sovereignty + signed-asset trust chain + Cedar/Logician determinism. The MCP tool-poisoning event (CrowdStrike 2026-05) and the Trillion Dollar defensibility framework converge on Tilth's structural posture. This is the strongest single positive signal in the brief.
- **Where Tilth is AT-PARITY:** substrate choices (Pydantic AI + Logfire + Ollama/vLLM + GEPA), council-of-six pattern, rubric-bank pattern, audio-channel substrate.
- **Where Tilth is BEHIND:** VLM-based parsing, intra-cycle multi-agent debate, shipping the reflective loop, unified memory-retrieval API.
- **Where Tilth is WRONG-DIRECTION:** **none identified in this window.** The SubQ subquadratic attention is a closed cloud product that Tilth correctly cannot adopt; the architectural insight (linear-scaling context) is on v1.x watchlist. KnowQL convergence is directional, not 1:1 — but the direction is right, not wrong.

---

## Prioritized Roadmap Recommendations — Beta-Thesis Ordered

The list below is **reordered around the desk-Beta thesis**: what makes the unit on a customer's desk effective, stable, token-efficient, and memory-competent. Items in bold are the four-axis pillars.

### Tier 0 — Beta-blocking, in priority order

| # | Pillar | Recommendation | Effort | Why this is desk-Beta-blocking |
|---|---|---|---|---|
| 1 | **MEMORY-COMPETENT** | Ship Reflection Packet v0.2 first-wave compound LOCK (handoff pre-staged at `pipeline/handoffs/ws_reflection_packet_v0_2_first_wave_handoff_2026-05-15.md`). Turn the LOCKed-but-dormant architecture on. | 1-2 sessions + 1 LOCK round | Without this, cycle N+1 starts from scratch on the customer's desk. Cross-cycle learning is the value prop. |
| 2 | **MEMORY-COMPETENT** | `tilth memory query` unified retrieval CLI — Mem0-shape, Law-3-isolated, joins KFR + lessons + lock_history + CycleReceipt + classification register. Replaces "operator browses 13 registers by hand." | 2-3 sessions | A Founding-12 customer asks *"show me every USDA submission I've ever made"* in onboarding hour 1. Tilth currently has no answer. |
| 3 | **MEMORY-COMPETENT** | MEMORY.md auto-consolidation trigger on size threshold (e.g., >20 KB → run consolidate-memory skill automatically). | <1 session | This file is overflowing **in this very session**. On a customer's desk after 3 months of cycles, retrieval will silently degrade. |
| 4 | **TOKEN-EFFICIENT** | `tilth metrics cycle-cost <cycle_id>` CLI joining session_log + cache-ledger + Coefficient Registry into single $-cost number. Gives the customer a bill they can quote. | 1 session | The customer's BYOK bill is the buying objection. Show them what each grant cost to write. |
| 5 | **STABLE** | Backup/restore story across 13 memory registers (customer-contract item per Alpha Checklist #28). Single-snapshot, encrypted, restorable on a new appliance. | 1 session doc + 1 session impl | Sovereignty Promise says "still have your machine, your data, your keys, your grants" if SN-LLC vanishes. M3 Ultra SSD fails on day 90. What's the actual procedure? Today: undefined. |
| 6 | **EFFECTIVE** | VLM fallback path at Intake (PaddleOCR VL or Granite 4.0 3B Vision) when pypdf returns degraded confidence. §11 v1.2 amendment. Local VLM preserves sovereignty. | 2 sessions | Real onboarding corpora are 40-70% scanned. Without VLM, Tilth extracts a fraction of customer's history. |
| 7 | **STABLE** | EXIF / GPS strip on `photos` sub-kind insert. Pre-write hook; opt-in retain. | <1 session | Beneficiary GPS leak into funder report is a structural PII path. One incident on a real desk damages trust irrecoverably. |
| 8 | **STABLE** | Pin `logfire`, `chromadb`-or-`faiss-cpu`, `sentence-transformers`, `bge-large-en-v1.5` in `pyproject.toml`. Close D-RB-01 + §11 substrate-pinning gap. | <1 session | Repro-deployable Golden Image requires every substrate dep pinned. Today: spec leads pin. |
| 9 | **TOKEN-EFFICIENT** | Cross-document content-hash dedup at BULK_INGEST PRE-gate. 30 duplicate copies in a customer's Drive dump should not produce 30 redundant embeddings + 30 redundant KFR extractions. | <1 session | Onboarding-time token waste compounds with corpus size. Cheap fix; large savings. |

### Tier 1 — Sales-enabling, not desk-Beta-blocking

| # | Pillar | Recommendation | Effort |
|---|---|---|---|
| 10 | EFFECTIVE | Voxtral 3B drop-in for Whisper in Data Collector voice channel. Apache 2.0; sovereignty-preserving; beats Whisper v3 on benchmarks. | <1 session |
| 11 | DIFFERENTIATION | Customer-facing copy uplift: lead with Trillion Dollar defensibility framework (workflow design / data access / authority / evals / audit trails — Tilth checks every primitive). Website + pitch deck + sales playbook. | <1 session |
| 12 | EFFECTIVE | Operator-facing `tilth portfolio query` CLI — joins KFR + lock_history + CycleReceipt + lessons.md across cycles. Surfaces what Tier-0 item 2 makes queryable. | 2 sessions |

### Tier 2 — V1.X horizon watchlist (do not pursue at Beta)

- KnowQL-shaped retrieval-contract documentation (after Pinecone Nexus stabilizes; useful for Stage-5 cross-Tilth signal exchange).
- §0.5 governance-audit CLI (random-sample 10 rows, verify runtime imports).
- Funder-mindset card per CIC × CLC pair.
- Intra-cycle multi-agent debate option for federal long-form / large-award (track A-HMAD).
- Multi-language Scribe + Editor support (real PA segment blocker, not Beta urgent unless that specific customer lands first).
- Pinecone Marketplace "Grants vertical" claim — business-model conversation, not engineering decision.
- PPTX / social-media-blurb tracks in §5 v8 registry.

---

## Total Score: 47 / 80

| Dim | Score | Beta-thesis read |
|---|---|---|
| 1 Token efficiency | 6 | Substrate sound; missing cycle-cost KPI (sales gap on a customer's desk). |
| 2 Scale parsing | 5 | Clean-doc parsing is fine; scanned-doc onboarding will degrade silently. |
| 3 Multi-modal | 5 | Documents mature; audio coming; everything else absent — Beta-acceptable if scope is communicated. |
| 4 End-to-end cycle | 6 | Submission half mature; between-cycle half DORMANT. |
| 5 Vision gaps inventory | 7 | Well-inventoried; 3 real customer-blockers identified. |
| 6 Technical depth | 7 | Real depth; ceremony at borderline of value-at-risk. |
| 7 Council topology | 7 | Real substrate on disk; cross-family rigor is AHEAD. |
| 8 Memory | **4** | **The Beta-blocking dimension. 13 registers, no unified retrieval, overflow today, Reflection dormant.** |
| **Sum** | **47 / 80** | |

**Coarse interpretation through the Beta-thesis lens:** the architecture is *structurally past adolescence* — real substrate, real council, real signed-asset discipline, real Five Laws. It is *operationally pre-Beta* in exactly one load-bearing dimension: memory competence. **Six of eight dimensions clear the Beta bar; memory does not.** The architecture's worst dimension (4/10) is also its most exposed in a desk-Beta deployment, because cross-cycle learning is the value prop and it isn't running yet. **The v0.2 first-wave dispatch plan is well-aligned to this exact gap** — landing Reflection Packet producer-flip + the unified memory-query CLI + auto-consolidation is the single highest-leverage Beta-readiness move.

**What "ship Beta" looks like at the score level:** Dim 8 needs to move from 4 to 7 minimum. Tier-0 items 1-3 above are the path. Once those land, the overall total moves to roughly 50/80 — and Beta is shippable.

---

## Hand-back to coordinator

Architecture proficiency assessment complete. Total 47/80 across 8 dimensions, read through the Beta thesis (128 GB Golden Quill on a real customer's desk).

- **Six of eight dimensions clear the Beta bar; memory does not (4/10) and it is the single load-bearing gap between "ready to ship" and "ship-shaped."** Reflection Packet is LOCKed but DORMANT; 13 registers have no unified retrieval API; MEMORY.md is overflowing during this very session.
- **Stability is the strongest implicit Beta dimension** — 1869 tests pass, Cedar fails closed, Logician deterministic gates have no token cost, signed-asset trust chain is *ahead* of where the industry just-realized-it-needs-to-be after the MCP tool-poisoning disclosures. Lean into the Trillion-Dollar-defensibility frame for customer copy.
- **Token-efficiency is sound at the substrate (Logfire 8-40× cheaper than LangSmith); blind at the cycle layer (no `tilth metrics cycle-cost` KPI today).** The customer's BYOK bill is the sales objection.
- **KnowQL 1:1-mapping claim from advancements scan is too generous: 2 of 6 primitives are genuine (provenance, output shape); 3 of 6 are conceptually adjacent (intent, filter, confidence); 1 of 6 is weak (budget).** Don't put 1:1 in customer copy; document Tilth's retrieval contract at v1.x.
- **Top 9 Beta-blocking items reordered around the four-axis thesis** (effective / stable / token-efficient / memory-competent). Items 1-3 are all MEMORY-COMPETENT; items 4-5 are STABLE + TOKEN-EFFICIENT; items 6-9 are EFFECTIVE + STABLE.
- **3 OVER-ENGINEERED findings + 5 BLIND-SPOT findings filed per anti-flattery clause.** §0.5 at 505 rows is the most surface-area-vs-value-at-risk question.

**Path to ship Beta:** land Tier-0 items 1-3 (Reflection Packet v0.2 first wave + unified memory-query CLI + auto-consolidation trigger) → Dim 8 moves from 4 → 7 → total ≈ 50/80 → Beta is shippable on the four-axis thesis.

Result file: `pipeline/planning/architecture_proficiency_assessment_result_2026-05-11.md`. Evidence pack: `pipeline/validation/architecture_proficiency_2026-05-11/evidence_pack.md`. Single-Claude synthesis posture; advancements scan was same-family parallel session; cross-family verify recommended-but-not-fired given this is informational, not LOCKable.

— end of result —
