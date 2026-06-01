---
title: Architecture Proficiency Assessment — Tilth v0.1+v0.2 against the "ultimate grant writing machine" vision
filed: 2026-05-15
status: PROMPT (Part 1 of two-part deliverable)
operator: Josh Inklovich
authoring_agent: Cowork session local_3c8d30a8
companion_result: pipeline/planning/architecture_proficiency_assessment_result_2026-05-11.md
audit_trail: pipeline/validation/architecture_proficiency_2026-05-11/
scope: holistic critique of the architecture as it stands post-row-218, scored against the operator's full vision and 2026-05-15 SOTA agentic-AI baseline
tone: sharp, honest, not deferential — over-engineering and missing surface get called out equally
---

# Architecture Proficiency Assessment — Prompt + Rubric

## Why this exists

The Tilth/Golden Quill architecture has been ground out through 218 LOCK-history rows, ~44+ failure codes in the Logician gate family, 1869 passing tests, and ~13 v0.1+v0.2 cross-family Thesis rounds at full live cross-family rigor. That's a lot of audited surface.

But a Thesis round only audits the surface in front of it. It does **not** audit whether the surface in front of it is the right surface to be building at all. This rubric is the missing audit: a holistic critique of the architecture against the operator's actual end-goal — an "ultimate grant writing machine" — and against the current state-of-the-art for agentic AI systems.

The rubric is deliberately **adversarial to sunk cost**. If a LOCKed surface is load-bearing, it scores well. If it is ceremony — governance theater that doesn't carry weight under real cycle volume — it gets called out. If something the operator's vision requires is **absent** from the architecture entirely, the gap is named explicitly. The point is to inform Josh's roadmap, not flatter the work done.

## Scope of the assessment

**In scope:** the architecture as it stands at lock_history row 218 (2026-05-15 close of business). Includes everything LOCKed through §16 Reflection Packet v1. Includes the v0.2 horizon items that are SPEC LOCKed (Data Collector, Report Generator, Archivist, Funding Goal, Reflection Packet sub-kind). Includes the v7.0.10 three-posture routing model. Includes the WPFA cycle-accounting layer.

**Out of scope (do not score):** Stage 3+ commons-layer architecture (Sovereign Node multi-Tilth federation), §R TDSL content-production track horizon items not yet LOCKed, the Cultivator phone-interface layer beyond §13 substrate.

**Comparison baseline (Dimension 9 cross-cut):** the 2026-05-15 SOTA-agentic-AI snapshot to be filed at `pipeline/research/advancements_scan_2026-05-15.md`. Reviewer must wait for that file before scoring SOTA delta.

## Scoring schema

Each of the eight dimensions receives:
1. **Raw score 0-10.** 0 = absent or actively harmful. 5 = adequate, real on-disk shape but with visible seams. 10 = best-in-class against any AI grant-writing system, sovereign or not.
2. **One-sentence verdict.** Plain English, no hedging.
3. **SOTA delta tag.** One of: `AHEAD` (Tilth is doing something the broader field is not yet doing well) / `AT-PARITY` (Tilth matches current best practice) / `BEHIND` (the field has moved past Tilth here) / `WRONG-DIRECTION` (Tilth is investing in a paradigm the field has abandoned or is abandoning).
4. **Top 3 failure surfaces.** Where this dimension is most likely to crack under real cycle volume or first-paid-customer load.
5. **Top 3 missing-from-architecture items.** Things the operator's vision needs that aren't on disk anywhere.
6. **Recommendation priority tier.** One of: `P0-BLOCK-ALPHA` (must address before first paid client) / `P1-V0.2-FIRST-WAVE` (address in the next compound LOCK round) / `P2-V1.X` (defer to v1.x horizon) / `P3-NICE-TO-HAVE` (real but low-impact).

Total possible score: 80. The total is a coarse summary — the per-dimension narrative is what informs the roadmap.

## Anti-flattery clause

The reviewer must produce at least **three findings tagged `OVER-ENGINEERED`** somewhere in the assessment. If after honest review no over-engineering can be found anywhere in 218 LOCK rows + ~44 F-codes + 8 Thesis cycles per amendment, the reviewer must justify in writing why none of the LOCK ceremony is ceremony. The default prior is that some of it is. The reviewer must also produce at least **three findings tagged `BLIND-SPOT`** — places where the architecture has invested zero design surface that the operator's full vision requires.

---

## Dimension 1 — Token Efficiency

**What's being scored:** is the architecture's token budget per grant cycle sustainable at fleet scale, or is it being burned on ceremony?

**Evidence anchors to inspect:**
- `lessons.md` L-002 (path references, not content dumps) — how strictly enforced in practice across the 80+ session_log.jsonl entries?
- `pipeline/templates/component_analysis_template.md` — does it actually get referenced in handoffs, or do handoffs still re-encode framework structure?
- `pipeline/SESSION_BOOTSTRAP.md` — same question; is the file pulling the weight it was filed to pull?
- Cross-family Thesis bridge: `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh` and successor rounds. Token-per-cycle cost across the three live model IDs (`groq/llama-3.3-70b-versatile`, `google/gemini-2.5-pro`, `groq/openai/gpt-oss-120b`).
- `pipeline/metrics/session_log.jsonl` — token spend per session, self_check_failures column, handoff length.
- Anthropic prompt-caching discipline: `cacheRetention: long` markers in `router.yaml`, the `ORG:<slug>\nTRACE:<sessionId>\n` cache-preamble convention from AGENTS.md § Caching Discipline.
- Logfire span volume per cycle (per `docs/platform_engineer_onboarding.md`). Each F-CLASS / F-WPFA / F-PACKET / F-REPORT gate emits PRE+POST spans.

**Failure surfaces to probe:**
- LOCKed amendments quoted verbatim into handoff prompts (CLAUDE.md instruction violation; common in long compound-LOCK rounds).
- §0.5 Interface Index re-read in full at every Thesis round (218 rows × bytes = nontrivial input tokens per Thesis seat).
- Two-audit cycle's Cycle-2 verification re-issuing nearly-identical prompts when Cycle-1 fixes are small (L-005 transparent-disposition pattern: are RT-fold-ins materially cheaper than re-running?).
- Anthropic prompt caching not firing on `claude-cli/*` OAuth paths (AGENTS.md § Caching Discipline) — does Cowork actually route through `anthropic/*` API keys consistently?
- Logfire span fan-out per cycle: 6 seats × (PRE+POST) × ~44 F-codes is the upper bound. What's the realistic mid-bound at submission_mode end-to-end?

**Gap probes:**
- Is there a per-cycle token budget defined anywhere? If not, on what basis does the operator decide whether a cycle "ran efficiently"?
- Is there a token-cost-per-grant-submitted KPI in the alpha-readiness checklist? Should there be?
- Does the Coefficient Registry (§17 WPFA) cover token cost specifically, or only watt-hours-per-token? The CycleReceipt fields are the answer.

---

## Dimension 2 — Sorting + Parsing Data After Upload at Scale

**What's being scored:** when an operator drops 500 — or 5,000 — documents into Intake, does the architecture absorb them cleanly, or does it saturate?

**Evidence anchors to inspect:**
- §11 Intake v1 LOCKED rows 185 + 209/210 (commitment_id canonical-home). Three modes: BULK_INGEST (white-glove onboarding), INCREMENTAL_INGEST (between-cycle, default `confidential`), AWARD_INGEST (proposal_commitments.yaml).
- `tilth_architecture_locked.md` §D.0 Scout Entity Research Pass [M11] — verbatim-quote-with-page provenance.
- Substrate per ADR-001 / v7.0.3: python-docx, openpyxl, pypdf wrapped as Pydantic AI tools. No external doc-parsing services in the substrate.
- FAISS / ChromaDB usage — actually present in v0.1 Beta or aspirational? Check `pipeline/seats/intake/` and `~/.mempalace` for ChromaDB 1.5.7 footprint.
- Embedding namespacing: `F-INTAKE-EMBEDDING-NS-MISMATCH` (one of the four NEW Cycle-1 closure gates in §11). Per-org Law-3-bound namespacing.
- Mistral 7B / ollama local inference for high-volume parse — `router.yaml` Scout primary. M1 8GB dev floor; 128GB production floor.
- `F-INTAKE-WATCHER-TOCTOU` gate — file-system watcher race condition handling.
- `F-EXTRACTOR-FABRICATION` substrate-dispatched (PDF unique-page-match per RT-01 + DOCX paragraph-index + Markdown single-line) — fabrication-resistance is real, but at what corpus size does it slow to unusable?

**Failure surfaces to probe:**
- 5,000-document BULK ingest on M3 Ultra 128GB: where does parse-time-per-doc cliff? Mistral 7B is fine for a 100-doc onboarding; what's the actual measured wall-clock for an organization with 10 years of legacy file accumulation?
- Operator-confirmation-required step in §11 (KFR fact ingestion): is it BATCHABLE, or does every fact require its own keystroke? At 5,000 docs × 20 facts/doc = 100,000 confirmations.
- Embedding refresh after architecture migration (`F-INTAKE-EMBEDDING-NS-MISMATCH` + config-signature-invalid): how is a re-embed scheduled? Manual? Cron? Does the operator know they need to do it?
- Classification register at scale: per-document classification × thousands of documents = how does the operator review and sign that volume? Is there a bulk-classification-by-folder mechanism, or only per-doc?
- INCREMENTAL_INGEST default-to-`confidential`: under high-volume drop, does this force every newly-dropped doc into local-only routing until operator re-classifies? What's the operator's UX for batch re-classification?

**Gap probes:**
- Is there a "search across the corpus" surface for the operator (text retrieval, semantic retrieval, hybrid)? Or does the operator find documents by browsing the file tree?
- Cross-document deduplication? An operator drops a folder including duplicates; what does Intake do?
- OCR — scanned PDFs are the norm for old grant archives. Is OCR substrate (Tesseract, AWS Textract, etc.) in scope? Per `anthropic-skills:pdf` it's available, but is it wired into Intake?

---

## Dimension 3 — Multi-Modal Data: Sort / Store / Use / Output

**What's being scored:** for each modality the operator's vision needs — audio, video, pictorial, reports, presentations, social-media blurbs, documents — where does the architecture handle it, and where does it not exist on disk?

**Evidence anchors to inspect:**

**Audio:**
- §13 Data Collector v1 LOCKED rows 196/197. Voice channel inbound + Whisper transcription. Outbound voice via Twilio. Four-layer autosend defense.
- Whisper substrate: local model? Cloud routing? Per v7.0.10 posture matrix, voice substance routes local; voice scaffold may route cloud under Split-Context Hybrid (operator-flagged or confidential by default).
- Audio attachments to grants — is this in §12 Uploader scope? Per row 182-184: attachments deferred to v1.1.

**Video:**
- Search `tilth_architecture_locked.md` for any "video" reference. The single hit at line 1115 is a §R-horizon Judge rubric reference for "video script tightness" — meaning video is mentioned only as a future content-production-track output target. No video INPUT, no video STORAGE, no video OUTPUT in any LOCKed surface.
- Some funders accept video pitches. Is this a real customer-blocking gap, or a Stage-3+ horizon? Score honestly.

**Pictorial (images):**
- §2 v7.2 LOCKED rows 186/187 — `photos` sub-kind among the seven SIMPLE schemas.
- §14 Report Generator v1 SPEC LOCKED — `photo_gallery` composer. Caption-hash + cross-section reference enforcement. EXIF / GPS / PII concerns — `F-REPORT-NUMERIC-DRIFT` and `F-REPORT-OUT-OF-SCOPE-DRIFT` may not catch EXIF metadata leak.
- Image generation? Not in scope. Logo/infographic generation for branded submissions? Not in scope. Score the absence.

**Reports:**
- §14 Report Generator v1 SPEC LOCKED — end-to-end shape. 5 sub-sections (narrative + metrics_table + financial_summary + photo_gallery + beneficiary_section). `claim_evidence_map.yaml` per-claim trace + operator Ed25519 single-map signing. **This is the mature multi-modal surface.** Score it accordingly.

**Presentations:**
- WPFA buyer-facing PDF (§17) is the closest thing to a presentation output the architecture currently produces. It's a one-off receipt artifact for sales, not a general presentation surface.
- Board reports, funder pitch decks — not in any LOCKed surface. Compare to `anthropic-skills:pptx` availability. The substrate to do this exists (python-pptx via skill); the architectural slot for "produce a presentation deliverable from operational data" does not.

**Social-media blurbs:**
- Not in current scope. Would belong as a Scribe sub-mode (alternative track in §5 v8 track registry) or a new track row (`content_mode` / `social_mode`). 
- §R content-production-track v0.2 horizon mentions content medium quality rubrics (line 1115) — closest existing pin.
- Post-award announcement generation, LinkedIn-funder-relationship monitoring, Twitter watch — all absent.

**Documents (DOCX/PDF/XLSX):**
- §12 Uploader v1 LOCKED — handles output packaging for 4 portal adapters (Grants.gov Workspace, SAM.gov, Common Grant Application, copy-paste fallback). Foundant / Submittable / Fluxx deferred to v1.1.
- §11 Intake — handles input parsing via python-docx, openpyxl, pypdf wrapped as Pydantic AI tools.
- This is the mature surface. Score accordingly.

**Failure surfaces to probe:**
- Whisper privacy: if audio carries beneficiary PII (a Data Collector outreach call recording), how does the classification register handle the transcript? Does it default to `confidential`? Does the audio file itself live anywhere persistent?
- Photo EXIF / GPS / face-recognition concerns: §14 has caption-hash enforcement but the schema doesn't appear to require EXIF stripping. Operator-confidential PII (a beneficiary's home GPS coordinates in a photo of their farm) would silently flow through.
- Report Generator's `F-REPORT-OUT-OF-SCOPE-DRIFT` and `F-REPORT-COMMITMENT-MISSED` cover narrative drift — do they cover image-content drift (operator uploads a photo of unrelated work)?
- Cross-section privacy audit: §14 says "covers beneficiary + photo references" — does it cover audio transcript references in narrative? Video doesn't exist yet so moot.

**Gap probes:**
- Is video pitch generation needed for any of Josh's three competitive wins in 2026? If not, defer-honestly. If yes, name the funder.
- Slide-deck production for board reports / funder pitches — has any client asked for this? Or is it a vision-creep item?
- Multi-language support (federal grants in Spanish, etc.) — not currently in scope. Is this a hard customer-blocking gap or a v1.x luxury?
- Live grant-writing collaboration (two operators editing simultaneously) — not in scope. v0.1 is single-operator by A1. Score the absence and decide if it's a v0.2 / v1.x / never-build call.

---

## Dimension 4 — Effectiveness of the Grant-Cycle Pipeline End-to-End

**What's being scored:** from RFA discovery to between-cycle learning, does the pipeline actually carry the cycle, or are there seams where the operator picks up disproportionate load?

**Evidence anchors to inspect:**
- The 12-step cycle from `docs/platform_engineer_onboarding.md`: Scout DISCOVER → VERIFY → REVIEW → Phase 0 Intake (P-COHERE-1/2/3) → Scribe drafts (KGIE preflight) → Editor → Judge (rubric-first) → Red Team (cross-family, ≥10pt disagreement triggers council split) → Operator approves → Uploader stages (4 adapters) → operator clicks final submit → WPFA CycleReceipt.
- Between-cycle: Reflection sub-mode of Archivist v0.1 hook (always-local) → Reflection Packet v1 schema (DORMANT until v0.2 first wave) → Archivist proper (v1.x horizon) → institutional_memory/lessons.json + lessons.md.
- §17 WPFA — closes the cycle with accountability artifact. CycleReceipt deterministic; buyer-PDF emission Ed25519-gated.
- L-001 EPA NEETP-26 precedent: VERIFY stage exists specifically because Scout DISCOVER alone produced a false CRITICAL-fit.

**Failure surfaces to probe:**
- **Operator load distribution.** Count operator-required gates per cycle: classification register sign-off (white-glove), per-grant SP0 overrides (per cycle), per-doc classification at Intake (per onboarding + per INCREMENTAL drop), claim_evidence_map.yaml signature (per draft), per-section approval (Editor/Judge/Red Team output review), final Submit click (per submission), per-recipient Data Collector consent (v0.2), Reflection Packet 2 BACKFILL operator-Ed25519 (per decision-observed event), CycleReceipt buyer-PDF operator Ed25519 (per cycle). How many operator touches per cycle, realistically? Where does that load become unsustainable at 12-Tilth Founding-12 fleet scale?
- **Context loss between seats.** Scribe → Editor handoff: how is Scribe's reasoning trace passed to Editor? Per Rule 4 Clean Output, "Strip LLM self-commentary." But Editor sometimes needs Scribe's intent. Is there a structured "rationale carry-over" channel, or does Editor re-derive intent from the draft alone?
- **Judge → Red Team coupling.** Per Section D, Red Team must not share provider family with Scribe OR Judge. Today: Scribe=Anthropic, Judge=Google, Red Team=OpenAI-OSS. If a provider family is down (M13 trigger), what's the next-best Red Team binding that preserves cross-family rigor? Is this written down?
- **Reflection Packet hook is DORMANT.** v0.1 Beta ships with the hook in NotImplementedError state (18 of 19 F-PACKET-* codes). Between-cycle learning is therefore **not actually happening yet** — only lessons.md is. Is that a real gap or an acceptable v0.1 Beta posture?
- **Archivist v1.x horizon.** The Funder Intelligence DB and Match DB are SPEC LOCKED but not built. Between-cycle funder-intelligence learning is operator-manual today. At what cycle count does this become a real bottleneck?

**Gap probes:**
- "What does the operator do during a cycle that the architecture doesn't help with?" — list. Common answers: hunting down the specific PDF page that has the EIN, copy-pasting partner letters of support, reformatting prior-grant boilerplate to match the new funder's tone, manually checking the funder portal for submission confirmation, manually emailing the program officer with a question. Which of these has architectural slot? Which doesn't?
- Funder-relationship continuity across cycles: if Josh submits to USDA SCBGP in 2026 and again in 2027, does the architecture remember the program officer's name, the prior reviewer comments, the prior award amount? Where would that data live? Probably Funder Intelligence DB (SPEC LOCKED, not built).
- Post-award compliance reporting cadence — Report Generator handles individual reports; what about the OPERATOR-FACING calendar of "this report is due in 30 days for this award"? Is that in §13 Data Collector scope, §14 Report Generator scope, or operator-manual?

---

## Dimension 5 — What "Ultimate Grant Writing Machine" Means That We're NOT Covering

**What's being scored:** the gap between the architecture as it stands and the operator's full unspecified vision. The point is to surface things explicitly so they enter the conversation.

**Candidate items to name and decide on:**

1. **Video pitch generation.** Some funders (especially philanthropy + impact-investment) accept or prefer video pitches. Tilth has zero video surface.

2. **Slide-deck production.** Board reports, funder pitch decks, conference talks. `pptx` skill exists as a tool, no architectural slot.

3. **Social-media announcement generation.** Post-award announcements for LinkedIn / Twitter / Facebook. Brand-aligned, drawing on grant abstract + photos. Absent.

4. **LinkedIn / Twitter funder-relationship monitoring.** Watch what program officers and foundation leadership are saying publicly. Absent.

5. **Multi-operator collaboration.** Two operators editing the same draft concurrently with merge semantics. Today: A1 single-operator hard constraint.

6. **Multi-language support.** Federal grants in Spanish (USDA SCBGP some states); UN / international funders in multiple languages. Absent. Real customer-blocking gap for Latino-led co-ops in PA.

7. **Real-time funder Q&A during open RFA windows.** Many funders run pre-application info sessions; some have written-Q&A windows. Capturing the Q&A as authoritative supplement-to-RFA — not in scope (Law 1 says RFA is the source of truth; the architecture doesn't address Q&A windows as adjunct authority).

8. **Automated newsletter / donor-update generation.** Operational data → donor narrative. v0.2 Data Collector + Report Generator are closest but oriented to grantees not donors.

9. **Visual asset generation (logos, infographics).** For branded submissions. `canvas-design` and `algorithmic-art` skills exist; no architectural slot.

10. **Past-grant-portfolio analysis dashboard.** "What did we get funded for in the last 3 years, what fell through, what patterns?" — close to Archivist + Match DB scope but the SURFACE for operator query isn't designed.

11. **Funder-due-diligence rebuttal.** When a funder comes back with reviewer comments asking for clarification, current architecture has no first-class slot. Goes back to Scribe ad-hoc.

12. **Partner-vetting workflow.** A new partnership letter arrives; does Tilth verify the partner exists, has the claimed credentials, has signed comparable letters before? §D.0 Scout Entity Research Pass [M11] is closest; how much of partner-vetting falls out of it vs. operator-manual?

13. **Compliance-report-from-operations data flow.** Operational data (timesheets, expenditure logs, milestone evidence) → quarterly funder report. Data Collector + Report Generator are SPEC LOCKED but not built; the integration with FIT Farms' real operational systems (whatever those are) is undesigned.

14. **Grant-writing pedagogy for the operator.** Tilth assumes the operator already knows what a SMART outcome is, what a logic model is, what an indirect-cost rate is. There's no architectural slot for "operator is new to this funder family and needs a 5-minute primer." Is that a real customer gap (especially for Stage-2 Founding-12 customers who may not be Josh-tier grant veterans)?

15. **Sub-grantee / pass-through workflow.** A primary grant produces sub-awards. The sub-grantee reporting back through is partially covered by Data Collector (v0.2 horizon) but the architectural shape is light.

The reviewer should mark each item as `BLIND-SPOT` (real gap, score it), `SCOPE-EXCLUDED-DELIBERATELY` (gap noted, but explicit operator decision to defer), or `VISION-CREEP` (vision-creep item that genuinely should not be in scope).

---

## Dimension 6 — Technical Design Depth (Architecture Coherence vs. Complexity Tax)

**What's being scored:** is the architecture genuinely coherent at 218 LOCK rows, or is the LOCK ceremony out of proportion to the value-at-risk per surface?

**Evidence anchors to inspect:**
- §0.5 Interface Index — 218 rows, runtime-live. Is it actually consulted as a reasoning surface in mid-design discussions, or only at LOCK time as a paperwork artifact?
- F-code family roster: F-CLASS (16 primitives post-v7.0.10), F-WPFA (12), F-PACKET (19), F-REFLECTION (8 BINDING + 8 HORIZON + 1 PROBE-DEPENDENT), F-INTAKE (11), F-UPLOADER (10), F-DATACOLLECTOR (8), F-REPORT (5 active), F-FG (8), F-ARCHIVIST (5), F-CEDAR (4), F-PIPE (3). **Total: ~110+ failure codes across ~12 families.** Plus seat-owned codes for Scout, Scribe, Editor, Judge, Red Team.
- Cross-family Thesis bridge: economic cost. Three model calls per Audit (Editor + Judge + Red Team), two cycles per amendment, 8 amendments per major surface. Empirically per `pipeline/validation/v7_0_5_thesis_2026-05-09/`: how many input/output tokens per round? Multiply by $ per million.
- Compound LOCK rows: at row 218 we are doing compound triples (§16 v1 + §4 v2.x.y + §0.5 v22) and compound quadruples (§17 v1 + §2 v7.4 + §4 v2.x.z + §0.5 v19). The dependency graph at LOCK time. Is this manageable?
- Lessons proliferation: L-001 through L-019 currently. At what L-NNN count does the pre-check itself become unsustainable?

**Failure surfaces to probe:**
- **§0.5 governance theater check.** Reviewer must read 10 random §0.5 rows (drawn from row 1 through 290) and answer: does each row name an interface that runtime code actually consults? Or are some §0.5 rows ceremonial markers that no code reads? If the latter is non-trivial, score `OVER-ENGINEERED`.
- **F-code family collapse check.** Could F-CLASS / F-WPFA / F-PACKET / F-REFLECTION be a single family `F-RUNTIME-*` with sub-tags, without losing safety? The Path-B-naming-reconciliation discipline (4 orthogonal families with AST-lint cross-family-import ban) is deliberate — does the discipline cash out in runtime separation that matters, or is it organizational neatness that future audits will spend tokens on?
- **LOCK ceremony per amendment.** A single amendment LOCK requires: spec draft + Cycle 1 dispatch (3 seats) + Cycle 1 fix + Cycle 2 dispatch (3 seats) + Cycle 2 fix + LOCK row + paired §0.5 amendment + paired §4 amendment + module skeleton + tests. ~6-12 hours per amendment if a single human is driving. At 8 amendments per major surface × 218 rows … the ledger says ~1500-3000 hours of compound work. Honest verdict: is this scaling with surface, or is it loglinear / linear / superlinear?
- **L-005 two-audit cycle's third-round-by-fold-in workaround.** Row-170 transparent disposition lets Cycle-2 NEW probes be FOLDED-IN at LOCK rather than triggering Cycle 3. Is this functionally a third round in disguise? If so, the L-005 "two-cycle" claim is honest only in form.
- **Cross-family economic check.** Per audit: Llama 3.3 70B + Gemini 2.5 Pro + GPT-OSS 120B × ~3-5k tokens × 2 cycles ≈ how much $? Multiply by 8 amendments per surface, by remaining v0.2 surface count. Is this sustainable from Josh's BYOK envelope?

**Gap probes:**
- Could §0.5 collapse into a generated artifact (derived from F-code declarations + runtime test imports) rather than hand-curated? At what surface size does the manual curation cost exceed the manual curation value?
- Is there a "complexity tax" KPI tracked anywhere? Lines of architecture text per F-code? F-codes per active module? Tests per F-code?
- Cross-family rigor: could a single non-Anthropic seat be sufficient at the lower-stakes amendments (narrow correctives like row 198/199), while reserving the 3-seat dispatch for the substantive amendments? Is there a tiered-rigor pattern in the architecture, or is every amendment 3-seat-mandatory?

---

## Dimension 7 — The Brain: Council Topology + Reasoning

**What's being scored:** is the Scribe → Editor → Judge → Red Team → Logician sequence the right reasoning flow for grant writing? Where does the council fail to catch real-world drift?

**Evidence anchors to inspect:**
- Section D of `tilth_architecture_locked.md` — the six-seat council formally defined.
- `router.yaml` — current model bindings (Scout=mistral:7b local, Scribe=Sonnet 4.6, Editor=Llama 3.3 70B, Judge=Gemini 2.5 Pro, Red Team=GPT-OSS 120B, Logician=Python+Cedar).
- v7.0.10 three-posture routing — how the council degrades under different operator postures.
- Heavy-Judge swap (200B-class local) per v7.0.7 §4 — federal long-form / large-award / operator-flagged grants.
- Operational gears: Sparring Partner / Co-Pilot (DEFAULT) / Synthesizer.

**Failure surfaces to probe:**
- **Funder-mindset modeling.** Scribe's funder-dialect code-switch is a register move, not a mindset move. A USDA reviewer differs from a Surdna Foundation reviewer not just in vocabulary but in what counts as evidence, what counts as risk, what counts as a viable timeline. Does the architecture model funder MINDSETS, or only funder dialects?
- **Applicant-mindset alignment.** Operator brings substance (Law 5) — but the architecture doesn't model the operator's *theory of change*. A regenerative-ag co-op pursuing food-sovereignty has a different theory of change than a vertical-farm tech-stack pursuing market-access. Does the council reason about whether the funder's theory of change and the applicant's theory of change ALIGN? Or does it just match keywords?
- **Stakeholder-perspective rotation.** Best-in-class agentic patterns rotate through stakeholder voices (the reviewer, the program officer, the future grantee, the board, the citizen). Tilth has reviewer (Judge), adversary (Red Team), and writer (Scribe). Does it have a `program_officer` voice? A `future_grantee_three_years_in` voice? A `legal_counsel` voice?
- **Debate / recursive self-correction.** Current SOTA agentic patterns (Anthropic's constitutional AI debate, OpenAI's reasoner self-correction, Claude's extended-thinking) all use multi-pass internal debate. Tilth's two-audit cycle is debate-shaped, but not recursive within a single seat-cycle. Is there value in adding a `judge.self_critique()` step before final scoring?
- **Council split mechanism.** Red Team >10pt disagreement → human decides. What fraction of cycles actually trigger council split in practice? If <5%, the mechanism is theoretical; if >30%, the council is fighting itself.

**Gap probes:**
- Is there a `funder_relationship_voice` seat or sub-mode? The architecture treats funders as evaluators, not partners.
- Multi-agent role-play — letting Scribe and Red Team argue back and forth N rounds — is a SOTA pattern that Tilth does not currently use. The two-audit cycle is structural, not conversational. Is there a v0.2 horizon item for adding intra-cycle debate?
- Reasoning trace persistence: where does Scribe's reasoning go between cycles? Is there a per-org "writer's notebook" that accumulates Scribe's pattern-of-thought across cycles, or does each cycle start cold?

---

## Dimension 8 — Effective Memory

**What's being scored:** is the memory architecture coherent across all the registers in play, or fragmented?

**Memory registers currently in play:**
1. **Cowork session memory** — `memory/MEMORY.md` index + per-topic memory files. User/feedback/project/reference types. Per-session.
2. **lessons.md / pipeline/institutional_memory/lessons.json** — operational lessons L-NNN. Workspace-wide.
3. **daily_logs/YYYY-MM-DD.md** — append-only operational ledger.
4. **lock_history.v1.jsonl** — append-only architectural-change ledger. 218 rows.
5. **PROJECT_CONTEXT.md (per-org)** — applicant substance under `orgs/<slug>/`. Law 3 isolation.
6. **KFR (Key Facts Register, per-org)** — quantitative substrate from Intake. Per-org. v0.1 BULK + INCREMENTAL + AWARD modes.
7. **Classification Register (per-org)** — `orgs/<slug>/vault/classification/register.yaml`. Operator Ed25519-signed.
8. **Reflection Packet (v0.1 hook DORMANT)** — `pipeline/vault/sub_kinds/reflection_packets.py`. 19 F-PACKET-* gates. v0.2 first wave.
9. **Funder Intelligence DB** — Archivist v1.x horizon. SPEC LOCKED.
10. **Match Database** — Archivist v1.x horizon. SPEC LOCKED.
11. **Cache-ledger** — `tilth/logs/<org>/cache-ledger.jsonl` + `cache-tally.json` — Anthropic prompt-cache telemetry.
12. **Session metrics log** — `pipeline/metrics/session_log.jsonl`.
13. **CycleReceipt (WPFA)** — `orgs/<slug>/vault/operational/cycle_receipts/<cycle_id>.json`. Per-cycle artifact.

**Evidence anchors to inspect:**
- Each register's read pattern. Is there a unified `tilth memory query` surface, or does each register require its own grep/path/read?
- Memory at corpus scale: MEMORY.md is already 35.6KB (truncated past 24.4KB load limit per the system warning today). Has memory consolidation actually fired (the consolidate-memory skill exists)?
- Cross-register coupling: when KFR updates (Intake INCREMENTAL), does any other register get notified? When a Reflection Packet would-be-emit (if v0.2 first wave landed), does lessons.json get auto-incremented or is that operator-manual?
- Per-org isolation: Law 3 says one PROJECT_CONTEXT per session. How does memory honor this across the 13 registers? Several are workspace-wide (lessons.md, lock_history, MEMORY.md) and several are per-org (KFR, classification register, CycleReceipt). The boundary should be clean. Is it?

**Failure surfaces to probe:**
- **MEMORY.md truncation today.** "WARNING: MEMORY.md is 35.6KB (limit: 24.4KB) — index entries are too long. Only part of it was loaded." This is happening **right now** in this very assessment session. The memory architecture is overflowing its own context budget. Is that a design failure or a "consolidate-memory hasn't run lately" failure?
- **Consolidate-memory skill execution cadence.** When was it last run? Does it run automatically on any trigger, or only when operator invokes? If the latter, the failure mode is "operator forgets, memory bloats, retrieval degrades." 
- **Cross-cycle learning today.** Without Reflection Packet wired (DORMANT until v0.2 first wave), what genuinely cross-cycle learning is happening? Answer should be honest: lessons.md (operator-curated), L-NNN entries (operator-curated), Match Database (not built). Effectively: operator-curated only, today.
- **Retrieval depth.** "Find every grant we've ever submitted to USDA SCBGP" — what's the retrieval path today? If it goes through `git log` or file-tree-browse, that's not retrieval, that's archaeology.
- **Concurrent-write safety.** Multiple agents writing to lessons.md and lock_history simultaneously — is there a lock or is it last-writer-wins? Check `F-INTAKE-WATCHER-TOCTOU` for the pattern Tilth uses elsewhere; check if it's applied across all append-only ledgers.

**Gap probes:**
- Is there a Cedar policy enforcing per-register Law-3 isolation at READ time? Or is it convention-only?
- Is there a unified retrieval API (vault.query(org, kind, filter)) or does each consumer hand-walk the file tree?
- Does memory survive a Golden Quill hardware swap? (Per Sovereignty Promise: "the operator would still have their machine, their data, their keys, and their grants.") What's the actual backup/restore story across all 13 registers?

---

## Dimension 9 cross-cut — SOTA Delta (read after `advancements_scan_2026-05-15.md` lands)

This is not a standalone dimension but a tag applied to each of dimensions 1-8 in Part 2. For each dimension, after reviewing the advancements scan, tag the dimension's verdict with `AHEAD` / `AT-PARITY` / `BEHIND` / `WRONG-DIRECTION` against the SOTA-2026-05-15 baseline.

Reviewer must not start Part 2 scoring until the advancements scan file exists on disk at `pipeline/research/advancements_scan_2026-05-15.md`.

**SOTA evidence categories to compare against (extracted by the advancements scan, with examples to anchor expectations):**
- Agentic frameworks (LangGraph, AutoGen, CrewAI, OpenAI Swarm, Anthropic Agent SDK)
- Long-context strategies (1M+ context windows, prompt caching, KV-cache-aware routing)
- Memory architectures (Mem0, LangMem, MemGPT, agentic RAG, hybrid retrieval, knowledge graphs)
- Multi-agent reasoning patterns (debate, judge-rubric, recursive self-correction, role-play, constitutional AI)
- Multi-modal substrates (GPT-4 / Claude vision, Whisper, Gemini Flash multimodal, video understanding)
- Local-inference state (Ollama scale, vLLM throughput, MLX on Apple Silicon, llama.cpp)
- Sovereignty / on-prem AI posture (the actual market for "local-only AI" — who else is building it, what they're getting wrong)

For each, ask: is Tilth's choice the consensus-correct call as of 2026-05-15, an early-bet that's looking right, an early-bet that's looking wrong, or a missing-the-wave?

---

## Output schema for Part 2 (assessment result)

The result file at `pipeline/planning/architecture_proficiency_assessment_result_2026-05-11.md` must have, in order:

1. **Executive summary** (max 200 words). The verdict in plain English. Total score X/80. Top 3 things that are right. Top 3 things that are wrong. Top 3 things that are missing.

2. **Per-dimension scoring** (8 sub-sections). Each with the 6-element schema above (raw score, verdict, SOTA delta, top 3 failures, top 3 missing, priority tier).

3. **Over-engineered surfaces** (≥3 findings, tagged `OVER-ENGINEERED`). Each names a specific LOCKed surface or §0.5 rows or F-code family and argues why it's heavier than the value-at-risk justifies.

4. **Blind-spot inventory** (≥3 findings, tagged `BLIND-SPOT`). Each names a thing the operator's vision needs that the architecture currently has zero design surface for.

5. **SOTA delta synthesis.** A short paragraph per dimension's SOTA delta tag — overall, where is Tilth ahead of the field, where is it behind, where might it be pursuing a paradigm the field is leaving behind?

6. **Prioritized roadmap recommendations** (top 10 items, ranked). Each carries a priority tier, a one-sentence "what changes," and a rough effort estimate (sessions / hours / amendments).

7. **Hand-back text** to coordinator (max 150 words). Suitable for direct paste into the coordinator's queue.

## Tone discipline (reviewer agreement)

- No "this is a strong foundation but…" hedging openings. Open with the verdict.
- No "kudos to the team for X" before delivering criticism. The criticism is the deliverable; flattery dilutes it.
- No "in a perfect world…" — name what should be done, in what version, by whom.
- No deferring to LOCK ceremony as proof of correctness. LOCK ceremony proves the surface was audited; this assessment audits whether the surface is the right surface.
- If the architecture is over-engineered in one place and missing entirely in another, both must be called out clearly with equal sharpness.
- If a dimension genuinely is best-in-class against current SOTA, say so — that's evidence, not flattery.

## Reviewer model preference (for the cross-family Part 2 dispatch)

If cross-family dispatch is feasible, route the assessment authoring to a non-Anthropic seat for the synthesis pass:
- Primary: Gemini 2.5 Pro (Google family) — strong synthesis + citation discipline + 2M context fits the 218-row ledger.
- Cross-check: GPT-OSS 120B (OpenAI-OSS family) for adversarial pass on the conclusions.
- Editor: Llama 3.3 70B (Meta family) for clarity / hedging-removal pass.

Section E single-Claude carve-out applies only on logged dispatch failure per `/AGENTS.md`. Document any fall-through with curl/openclaw error capture in the audit-trail directory.

## Done definition

- This prompt file filed.
- Part 2 result file filed at `pipeline/planning/architecture_proficiency_assessment_result_2026-05-11.md` after `pipeline/research/advancements_scan_2026-05-15.md` lands.
- Audit trail at `pipeline/validation/architecture_proficiency_2026-05-11/` if cross-family dispatch invoked (raw model outputs, dispatch logs).
- daily_log entry for 2026-05-15 appended with assessment outcome.
- Session metrics entry appended to `pipeline/metrics/session_log.jsonl`.
- Executive-summary verdict in hand-back text to coordinator.

— end of prompt —
