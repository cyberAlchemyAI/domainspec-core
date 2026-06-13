# BUILD-SPEC — Tilth Runtime Build (Workstream B)

- Node: `tilth-runtime-build` (Craft `CTX-TRB-ROOT`)
- Authoring mode: Refine → Invoke (Define → Design → Plan), canonical, implementation-ready
- Source contract: `docs/golden-quill-task-role-breakdown-handoff.md` Workstream B (rows 42–55)
- Substrate authority: `CLAUDE.md` (ADR-001 substrate lock; three-posture canon v7.0.10), `router.yaml`, `pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md`
- Refinement basis: `docs/features/tilth-runtime-build/development/refinement-runs/2026-06-12-craft-pipeline-hydration/RESEARCH-RESULT.md` + `.craft/ledger.yml`
- Owners: Vlad (backend: vault, classification, posture enforcement, audit log, rule engine, Golden Image) · Koichi (AI: inference, routing, ingestion, Scout, Mapper, drafting, ensemble, evidence capture)
- Status: REFINE-SOLVABLE gaps authored to Plan + acceptance + first steps; DECISION-GATED gaps listed as callouts only (not resolved).

---

## 0. Scope and guardrails (binding)

This node owns **Workstream B — Software / Tilth Build only**. It does not own hardware (Workstream A), QA/proof (C), card content (D), sales (E), white-glove (F), or company ops (G). The boundary is clean per RESEARCH-RESULT r01.

**Substrate is LOCKED — no alternatives proposed anywhere in this spec (ADR-001 / architecture v7.0.3):**

- Orchestration + structured output + observability: **Pydantic AI + Logfire**
- Local inference (OpenAI-compatible endpoint): **Ollama or vLLM**
- Offline Card refinement (Library dev only, never on-appliance): **DSPy + GEPA**
- Deterministic policy gates (fail-closed, zero-token, all Five Laws PRE/POST/COMMIT): **Logician (Python + Cedar)**
- Document parsing: curated Python utilities (python-docx, openpyxl, pypdf, feedparser, idna, spaCy, rapidfuzz) wrapped as Pydantic AI tools, frozen at Golden Image build with **no marketplace access from the appliance**.
- LangGraph and OpenClaw are REMOVED (absorbed by Pydantic AI primitives).

**Hard guardrails that gate every work pack below:**

1. **Three-posture canon only** — Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign. NEVER revive "Sanitized" or any 4-posture framing. The workbook row 50 wording ("Unrestricted / Hybrid / Sanitized / Sovereign") is STALE; do not propagate.
2. **No `[SLOT_*]` emission** into cloud-routed prompts under any posture. The opaque-slot-token mechanism is DEPRECATED (v7.0.10 §2). `F-CLASS-SLOT-ID-NON-OPAQUE` + `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED` (regex `\[SLOT_[^\]]*\]`) are now defense-in-depth gates; firing indicates bug/attack.
3. **No CIC→CLC coupling** in any code, schema, prompt, knowledge pack, scoring weight, or config. `F-CIC-CLC-COUPLING-VIOLATION` fail-closes (v7.0.8). Matching is opportunity-driven runtime, never archetype-driven design-time.
4. **v0.1 is HEADLESS-ONLY.** No interactive UI. Operator console is read-only projection / deferred phase only (see GATED callout).
5. **Law 3 (Org Isolation)** — one PROJECT_CONTEXT per session; no cross-org reference. This spec touches no `orgs/` data. Cross-org leak gates (`F-WPFA-CROSS-ORG-LEAK`, etc.) are structural.
6. **Fail-closed everywhere** — every Logician gate, every routing-indeterminate path, every unsigned/invalid signature defaults to LOCAL or to refusal.

---

## 1. GAP-TRB-WORK-PACKS — Sequenced implementation work packs

**Owner:** Vlad + Koichi · **Severity:** block · **Verdict:** REFINE-SOLVABLE — authored to full Define → Design → Plan below.

### 1.1 Define (what the gap is)

Workstream B rows 42–55 are a flat *task inventory*, not a *dependency-ordered build plan*. Fourteen rows, two engineers, one Golden Image deadline. The deliverable: decompose the 14 rows into sequenced work packs (WP), each with owner, inputs, outputs, acceptance criteria, and dependency edges, so Vlad and Koichi can run maximum-parallel without colliding on shared interfaces.

Row-to-pack map (14 workbook rows → 13 work packs; rows 49 and 51 are split-ownership packs):

| Row | Workbook task | Primary owner | Work pack |
| --- | --- | --- | --- |
| 42 | Local inference layer (primary model, embeddings, routing model, on-demand checkpoint swap) | Koichi | WP-1 |
| 43 | Multi-model routing layer (policy-driven, card defaults, per-task override) | Koichi | WP-2 |
| 44 | Vault (storage, classification labels, full-text + semantic indexes, classification-aware assembly) | Vlad | WP-3 |
| 45 | Ingestion pipeline (parsing, OCR, evidence extraction, document inventory) | Koichi | WP-4 |
| 46 | Scout (source manifest, governed fetch, fetch ledger, refresh engine, opportunity DB, reality report) | Koichi + Vlad | WP-5 |
| 47 | Grant Module Mapper (RFA decomposition into section plan) | Koichi | WP-6 |
| 48 | Section-by-section drafting workflow with human editorial loop | Koichi | WP-7 |
| 49 | Rubric review + compliance (multi-model ensemble + deterministic rule engine, kept separate) | Koichi (ensemble) + Vlad (rule engine) | WP-8 |
| 50 | Posture system (technically enforced) | Vlad | WP-9 (canon-gated — see §3) |
| 51 | Split-context drafting pattern | Koichi + Vlad | WP-10 (canon-gated — see §3) |
| 52 | Audit log (every invocation, payload class, cross-boundary event, hash) | Vlad | WP-11 |
| 53 | Operator console (read-only projection first) | Koichi | WP-12 (UI-gated — see §4) |
| 54 | Evidence capture & report drafting from captured material | Koichi | WP-13 |
| 55 | Golden Image assembly (one installable, versioned, signed artifact) | Vlad (lead) + Koichi | WP-14 (= §2 handoff) |

Note: workbook row 51 names a "Sanitization pipeline + split-context drafting pattern." The "sanitization pipeline" half maps to STALE canon (opaque-slot/Sanitized posture is deprecated). WP-10 carries the **split-context drafting pattern only**; the sanitization-pipeline half is dropped per guardrail 1/2 and is NOT a work pack.

### 1.2 Design (sequencing rationale and dependency edges)

Three foundation packs unblock the rest and have **no upstream dependency** on each other — run them first, in parallel:

- **WP-1 Inference** (Koichi) — nothing else can call a model until the OpenAI-compatible local endpoint serves.
- **WP-3 Vault** (Vlad) — nothing can store/index/assemble classified material until the vault exists.
- **WP-11 Audit log** (Vlad) — the append-only hash-chained log must exist before any invocation it is supposed to record; built as a thin always-on substrate, then every later pack writes to it.

Dependency edges (`A → B` = B depends on A):

```
WP-1 Inference ──┬─→ WP-2 Routing ──┬─→ WP-6 Mapper ─→ WP-7 Drafting ─→ WP-8 Review ─→ WP-13 Evidence/Report
                 │                  │
WP-3 Vault ──────┼─→ WP-4 Ingestion ┘        WP-9 Posture (canon-gated) ─→ WP-10 Split-context (canon-gated)
                 │                                        ↑
WP-11 Audit ─────┴─→ (all packs write audit events)       │ (WP-2 routing consumes WP-9 posture decision)
                                                          │
WP-3 Vault + WP-1 Inference ─→ WP-5 Scout ────────────────┘
WP-2 Routing + WP-9 Posture ─→ (routing enforcement wiring)
WP-7 + WP-8 + WP-13 + WP-9 + WP-3 + all ─→ WP-14 Golden Image (terminal pack)
```

Critical path: **WP-1 → WP-2 → WP-6 → WP-7 → WP-8 → WP-13 → WP-14**. Posture (WP-9) is on a parallel canon-gated track that must rejoin WP-2 before WP-14 can seal a deployable image.

Lane separation (so the two engineers do not block each other):
- **Vlad (backend lane):** WP-3, WP-9, WP-11, rule-engine half of WP-8, WP-14 (lead). All deterministic / Cedar / storage / signing.
- **Koichi (AI lane):** WP-1, WP-2, WP-4, WP-6, WP-7, ensemble half of WP-8, WP-13, WP-12 (gated). All inference / prompt / ingestion / drafting.
- **Shared-interface packs (joint, contract-first):** WP-5 Scout (Vlad owns fetch ledger + governed-fetch policy; Koichi owns channel adapters + classification), WP-10 split-context (Vlad owns allow-list + leak PRE-scan gate; Koichi owns the local-substance / cloud-scaffold composition).

### 1.3 Plan — work packs (sequenced)

Each pack: inputs → outputs → acceptance criteria → dependency edges. All packs MUST satisfy the Four Autonomy Rules (Save State Always; Test Your Own Work; Be Explicit; Clean Output) and write through WP-11 audit.

---

**WP-1 — Local inference layer** · Owner: Koichi · Phase: Foundation
- Inputs: `router.yaml` seat→model bindings; substrate lock (Ollama/vLLM OpenAI-compatible endpoint); locked model checkpoints (Scout `mistral:7b`, embeddings model, routing model, heavy-Judge 200B-class pre-load).
- Outputs: a Pydantic AI model-provider abstraction serving local inference over an OpenAI-compatible endpoint; embeddings service; on-demand checkpoint-swap mechanism (heavy-Judge pre-loaded local, **no network fetch** — `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD` PRE-gate); boot-time manifest verification of pinned checkpoints.
- Acceptance: local endpoint answers a structured Pydantic AI call with validated output; embeddings return vectors of pinned dimension; checkpoint swap loads the 200B-class Judge model with zero outbound network; `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD` fires on any swap attempting remote fetch; all checkpoints verify against the Golden Image manifest at boot.
- Depends on: none (foundation).

**WP-2 — Multi-model routing layer** · Owner: Koichi · Phase: Foundation+1
- Inputs: WP-1 endpoint; `router.yaml` per-seat bindings + track registry; per-field classification register (public / shareable / confidential / operator_flagged); card-level archetype defaults; per-task override interface.
- Outputs: policy-driven per-agent-call router implementing the three-posture decision tree (local_only_sovereign → LOCAL; frontier_eligible → public/shareable cloud, confidential/operator_flagged LOCAL, indeterminate fail-closed LOCAL; split_context_hybrid → scaffold seats cloud via allow-list, substance LOCAL, else fail-closed LOCAL); card defaults → operator overrides → per-grant SP0 layering; router-template Ed25519 signature verification before applying any update.
- Acceptance: every posture path resolves deterministically; `F-CLASS-ROUTING-INDETERMINATE` fails closed to LOCAL; `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` rejects unsigned/wrong-signed template updates and stays on pinned version; post-substance-assembly drafts force all subsequent seats LOCAL; cross-family rigor preserved (Judge ≠ Scribe family; Red Team ≠ Scribe/Judge family).
- Depends on: WP-1; **consumes WP-9 posture decision** (interface stub acceptable until WP-9 canon-unblocks — see §3).

**WP-3 — Vault** · Owner: Vlad · Phase: Foundation
- Inputs: classification register schema (4 values); canonical vault paths (`orgs/<slug>/vault/...`, `vault_shared/...`); document corpus shape from WP-4.
- Outputs: storage layer with per-field classification labels; full-text index + semantic (vector) index; classification-aware assembly that refuses to assemble confidential fields into a cloud-bound payload; Law-3 path-slug structural guard.
- Acceptance: a stored field carries an immutable classification label; assembly of a cloud-destined context excludes confidential/operator_flagged fields and logs the exclusion; `F-WPFA-CROSS-ORG-LEAK`-class path guard rejects any write whose slug ≠ target org; semantic + full-text retrieval return the same doc by id.
- Depends on: none (foundation). Provides the classification register that WP-2 reads.

**WP-4 — Ingestion pipeline** · Owner: Koichi · Phase: Foundation+1
- Inputs: WP-3 vault; curated parsing utilities (python-docx, openpyxl, pypdf) wrapped as Pydantic AI tools; OCR utility; Intake support-agent contract (BULK_INGEST / INCREMENTAL_INGEST / AWARD_INGEST modes; new INCREMENTAL facts default `confidential`).
- Outputs: parse → OCR → evidence-extraction-with-verbatim-quote-plus-page-provenance → document-inventory pipeline writing into the vault with classification defaults; Key Facts Register population for operator confirmation.
- Acceptance: a DOCX/PDF/XLSX ingests to vault with provenance (verbatim quote + page) on each extracted fact; INCREMENTAL-mode new facts land as `confidential` and `F-CLASS-NEW-FACT-UNCLASSIFIED` defends the default; document inventory enumerates every ingested artifact; all parsing is via the frozen allow-list (no marketplace access).
- Depends on: WP-3.

**WP-5 — Scout** · Owner: Koichi (channels + classification) + Vlad (fetch ledger + governed-fetch policy) · Phase: Mid
- Inputs: WP-1 inference (Scout primary `ollama/mistral:7b`); WP-3 vault (cached datasets, subscribed feeds); six parallel channel families A–F per `router.yaml`; verify-stage live-synopsis fetch.
- Outputs: source manifest; governed fetch with fetch ledger (every fetch recorded, hashed, audit-linked); refresh engine (cron loop); opportunity DB; two-stage DISCOVER (union of A–F, dedup, UNVERIFIED) → VERIFY (live synopsis → VERIFIED_FIT / VERIFIED_NOT_FIT / UNVERIFIED / VERIFICATION_FAILED) → REVIEW human gate; reality report.
- Acceptance: all six channels run as parallel primaries (none a fallback); no candidate reaches CRITICAL-fit without a passed live-synopsis VERIFY (EPA NEETP-26 precedent); fetch ledger records every fetch with hash + timestamp; Scout never auto-files (REVIEW gate); no CIC→CLC coupling in scoring (`F-CIC-CLC-COUPLING-VIOLATION` clean).
- Depends on: WP-1, WP-3, WP-11.

**WP-6 — Grant Module Mapper** · Owner: Koichi · Phase: Mid
- Inputs: WP-2 routing; verified opportunity + RFA from WP-5; rubric/evidence/sensitivity schema.
- Outputs: RFA decomposition into a section plan carrying per-section rubric weights, required evidence, and sensitivity (classification) tags; opportunity-driven CLC identification (funder-side) decoupled from applicant CIC (no design-time binding).
- Acceptance: a section plan is produced from an RFA with rubric weight + evidence list + sensitivity per section; CLC is identified at runtime from the opportunity, never pre-mapped from the applicant archetype (`F-CIC-CLC-COUPLING-VIOLATION` clean); Law 1 traceability — every section claim traces to RFA or PROJECT_CONTEXT.
- Depends on: WP-2, WP-5.

**WP-7 — Section-by-section drafting workflow** · Owner: Koichi · Phase: Mid
- Inputs: WP-6 section plan; Scribe routing (WP-2); WP-3 vault substance; human editorial loop (Co-Pilot default gear).
- Outputs: Scribe per-section draft with KGIE preflight, SMART outcomes, overlooked-expenses checklist, funder-dialect code-switching; Editor pass (clarity, 2–3 replacement options per flag); human editorial loop checkpoints; no `[SLOT_*]` ever emitted into cloud prompts.
- Acceptance: each section drafts with KGIE preflight passing; Editor flags carry 2–3 concrete options; flagged-term substitutions require applicant approval (Law 4 — never silent rewrite); post-substance drafts route Editor/Red Team/routine-Judge LOCAL; zero `\[SLOT_[^\]]*\]` in any cloud-routed payload.
- Depends on: WP-6, WP-2.

**WP-8 — Rubric review + compliance (ensemble + rule engine, kept separate)** · Owner: Koichi (ensemble) + Vlad (rule engine) · Phase: Mid+1
- Inputs: WP-7 draft; funder rubric (Judge); Red Team probe; Logician Cedar policies + Python validators.
- Outputs: **(a) multi-model ensemble review** — Judge scores against funder rubric first then cross-checks library rubrics (cross-family, Judge ≠ Scribe); Red Team adversarial fire on every draft (cross-family vs Scribe + Judge); ≥10-point Judge/Red-Team split → council split → human decides. **(b) deterministic rule engine (Logician)** — Python + Cedar PRE/POST gates enforcing all Five Laws, fail-closed, zero-token, kept architecturally separate from the ensemble.
- Acceptance: Judge scores all rubric dimensions with evidence strings appearing in the draft (Rule 2 magic-step); Red Team fires unconditionally; 10-point split triggers human gate (inclusive at threshold per §10.6); Logician gates run as PRE/POST, fail-closed, no model invocation; ensemble and rule engine remain separate modules (no rule logic inside ensemble prompts, no LLM call inside Logician).
- Depends on: WP-7.

**WP-9 — Posture system (technically enforced)** · Owner: Vlad · Phase: Foundation+1 · **CANON-GATED — see §3**
- Spec authored against the **three-posture canon** (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign). Build execution blocked on `DEC-BC-POSTURE-VOCAB`.
- Inputs: classification register; operator Ed25519 sign-off (white-glove Classification Review step 3 + step 4 posture selection/sign-off); `tilth posture select` CLI; deployment manifest `local_only_validated: bool` (default false, write-protected).
- Outputs: deployment-level posture selection + signature; enforcement hook consumed by WP-2 routing; posture re-selection CLI with mid-cycle change fail-closed (`F-CLASS-POSTURE-MID-CYCLE-CHANGE`); `split_context_allowlist.yaml` consumption.
- Acceptance: posture is operator-signed (Ed25519); unsigned/invalid posture fails closed (`.posture_unsigned` / `.posture_invalid` / `.posture_hash_mismatch` sub-tags); mid-cycle posture change refused; `local_only_validated` gates any "production-validated" claim; **NO "Sanitized"/4th posture admissible** (build does not start until canon decision lands).
- Depends on: WP-3; feeds WP-2, WP-10.

**WP-10 — Split-context drafting pattern** · Owner: Koichi + Vlad · Phase: Mid+1 · **CANON-GATED — see §3**
- Inputs: WP-9 posture (Split-Context Hybrid); operator-signed `orgs/<slug>/vault/classification/split_context_allowlist.yaml`; WP-7 drafting.
- Outputs: split-context composition — cloud frontier operates on RFA + section structure + dialect keywords only (closed-set allow-list, `F-CLASS-SPLIT-CONTEXT-ALLOWLIST` PRE-gate); pre-cloud applicant-fact scan (`F-CLASS-SPLIT-CONTEXT-LEAK` PRE-gate); local model inserts restricted facts/evidence/metrics/names separately. **No opaque-slot rendering round-trip; no `[SLOT_*]`.**
- Acceptance: only allow-listed scaffold fields reach cloud; applicant-fact scan blocks any confidential leak before cloud send; substance composition is LOCAL; the deprecated slot-fill module is present as defense-in-depth only and is never invoked on the normal path; `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED` clean.
- Depends on: WP-9, WP-7.

**WP-11 — Audit log** · Owner: Vlad · Phase: Foundation
- Inputs: invocation stream from every seat/agent; payload classification; cross-boundary (cloud-routing) events.
- Outputs: append-only, hash-chained audit log recording every invocation, payload class, cross-boundary event, and content hash; Logfire span-tree integration (shared substrate for WPFA CycleReceipt + Reflection Packet provenance, `F-*-SPAN-PROVENANCE-MISSING`).
- Acceptance: every model invocation produces an audit record with payload class + hash; cross-boundary cloud routes are logged with the classification that justified them; the chain is tamper-evident (hash links); span-provenance gates have a populated Logfire trace_id.
- Depends on: none (foundation). All later packs write here.

**WP-12 — Operator console (read-only projection)** · Owner: Koichi · Phase: Deferred · **UI-GATED — see §4**
- Scoped as read-only projection over the real backend ONLY; never an interactive v0.1 UI. Build gated on `DEC-BC-UI-BOUNDARY`. v0.1 is headless-only (locked).
- Acceptance (when ungated): renders state read-only; mutates nothing; introduces no interactive control path into the runtime.
- Depends on: backend packs producing projectable state; gated on governance decision.

**WP-13 — Evidence capture & report drafting** · Owner: Koichi · Phase: Late
- Inputs: WP-4 ingested material; WP-7/WP-8 drafting + review; v0.1 vs v0.2 track boundary.
- Outputs: evidence capture from captured material; report drafting scaffold. **v0.1 boundary:** `report_mode` is a FORWARD-COMPAT track row that refuses at runtime (`F-PIPE-TRACK-NOT-SHIPPABLE`) until v0.2. Data Collector + Report Generator are v0.2-only. v0.1 ships evidence capture + the dormant report scaffold, not active post-award reporting.
- Acceptance: evidence capture writes provenance-bearing material to vault; `report_mode` dispatch refuses at v0.1 runtime; no Data Collector / Report Generator path is active in v0.1.
- Depends on: WP-4, WP-8.

**WP-14 — Golden Image assembly** · Owner: Vlad (lead) + Koichi · Phase: Terminal · **= §2 handoff contract**
- Inputs: all preceding packs (substance + runtime tree); frozen substrate set; classification gates; signing keys.
- Outputs: one installable, versioned, signed runtime artifact with manifest; boot-time manifest verification; `F-CLASS-COVERAGE-INCOMPLETE` META-gate clearance (all required F-CLASS-* modules + tests present). See §2 for the full interface spec.
- Acceptance: see §2 acceptance criteria.
- Depends on: WP-1..WP-11, WP-13 (and WP-9/WP-10 once canon-unblocked); WP-12 excluded from v0.1 image unless ungated.

### 1.4 First steps (next session, no operator input required)

1. Stand up the three foundation packs in parallel: WP-1 (Koichi), WP-3 + WP-11 (Vlad). Write the Pydantic AI model-provider abstraction (WP-1), the classification-labeled vault store (WP-3), and the hash-chained audit substrate (WP-11) as the first three spec cards per `engineering_process_v0.1.md` §11.
2. Author the WP-2 routing interface stub with a posture-decision seam so WP-2 can proceed against a stub while WP-9 stays canon-gated.
3. Author the WP-5 Scout interface contract first (joint Vlad/Koichi) — fetch-ledger schema (Vlad) and channel-adapter interface (Koichi) — before either side codes, since it is the largest shared surface.

---

## 2. GAP-TRB-GOLDEN-IMAGE-HANDOFF — Golden Image assembly interface spec

**Owner:** Vlad + Koichi · **Severity:** flag (coordinate) · **Verdict:** REFINE-SOLVABLE — interface spec authored below.

This is the **handoff contract from Workstream B (Tilth runtime build) to Workstream A (`hardware-golden-image`)**. Workstream A's `GAP-HGI-IMAGE-VERIFY` ("Golden Image write process needs repeatable verification evidence per unit") is the *consumer* of this contract: A writes the image onto units and verifies it; B produces the one installable, versioned, signed artifact A writes.

### 2.1 Define

The Golden Image is **one installable, versioned, signed artifact** packaging the entire frozen Tilth runtime tree: substrate (Pydantic AI + Logfire + Ollama/vLLM runtime + curated parsing utilities), all WP modules, Logician Cedar policies + Python gates, pinned model checkpoints (including pre-loaded heavy-Judge), the router-template, and the per-deployment classification register seed. No marketplace access; everything frozen at build.

### 2.2 Design — the artifact contract

**Artifact identity:**
- `image_id`, `version` (semver), `build_timestamp`
- `content_manifest`: ordered list of every packaged component with per-file SHA-256
- `signature`: publisher Ed25519 signature over the manifest (A12 crypto-agility envelope)
- `publisher_pubkey_id`: identifies the white-glove-pinned key the consumer verifies against

**Packaged contents (the "everything" of row 55):**
1. Frozen substrate runtime — Pydantic AI, Logfire, Ollama/vLLM, curated parsing utilities, pinned Python interpreter (3.11+; suite validated on 3.14 venv).
2. All WP module trees (WP-1..WP-11, WP-13; WP-9/WP-10 once canon-unblocked; WP-12 excluded unless ungated).
3. Pinned model checkpoints incl. embeddings, routing model, Scout `mistral:7b`, pre-loaded heavy-Judge 200B-class.
4. Logician Cedar policies + Python gate modules (full F-CLASS-* family — 16 primitives; plus F-WPFA-*, F-PACKET-* registrations as shipped).
5. Router-template (publisher-signed) + classification-register scaffold (`orgs/_TEMPLATE/classification_review/`).
6. Boot-time manifest verifier.

**Boundary verification (the heavy-Judge no-fetch invariant):** the image must satisfy `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD` — the 200B-class Judge is pre-loaded in-image, never network-fetched. The alternative-update-channel ban is baked in: the only update path is a publisher-Ed25519-signed router-template / image update verified against the white-glove-pinned key (`F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` fail-closed).

### 2.3 Plan — handoff interface to Workstream A

Workstream B delivers to Workstream A:

| Deliverable | Form | Consumer-side use (Workstream A) |
| --- | --- | --- |
| Signed image artifact | single installable file + detached signature | A writes it onto each unit (GAP-HGI-IMAGE-VERIFY) |
| `content_manifest` (per-file SHA-256) | manifest file inside artifact | A re-hashes post-write to prove byte-identical install per unit |
| Publisher pubkey fingerprint | out-of-band, pinned at white-glove | A verifies signature before write; mismatch → reject |
| Boot-time verifier | in-image executable | A runs it as part of per-unit acceptance to confirm manifest verifies on the target hardware |
| `local_only_validated` manifest field | bool, default false, write-protected | A surfaces it; flips only on SN-LLC quarterly validation signature |

**Acceptance criteria (B side):**
1. Artifact installs from a single file; version is semver and embedded in the manifest.
2. Manifest carries per-file SHA-256 for every packaged component; re-hash after a clean write reproduces every digest.
3. Ed25519 signature verifies against the pinned publisher key; a tampered byte fails verification (fail-closed, no install).
4. Boot-time manifest verification passes on a clean install and fails on any post-build mutation.
5. `F-CLASS-COVERAGE-INCOMPLETE` META-gate passes — all required F-CLASS-* enforcement modules and tests are present in the image (no deployment with missing gates).
6. Heavy-Judge checkpoint is in-image; a swap attempting remote fetch fires `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD`.
7. No marketplace / network-install dependency exists in the packaged tree (frozen-set audit clean).

**First steps:** define the `content_manifest` schema and the detached-signature format jointly with Workstream A's `GAP-HGI-IMAGE-VERIFY` owner, so the per-unit re-hash/verify procedure (A side) and the manifest-emission procedure (B side) agree on the exact digest list and signature envelope before WP-14 assembly begins. The signing trust mechanism mirrors `router.yaml` v7.0.7 §6.1 byte-for-byte (publisher Ed25519, white-glove-pinned key, TOFU rotation co-signed by previous key).

---

## 3. DECISION-GATED CALLOUT — GAP-TRB-POSTURE-CANON

**Owner: Josh / boundary-and-canon. NOT resolved here.**

- Blocking decision: `DEC-BC-POSTURE-VOCAB` (boundary-and-canon ledger, status `block`).
- The workbook posture row (handoff line 50) names "Unrestricted / Hybrid / Sanitized / Sovereign" — STALE 4-posture vocabulary. Canon is the **three-posture set: Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign** (`DEF-BC-POSTURES-001`, CLAUDE.md, v7.0.10 amendment).
- This spec authors WP-9 (posture system) and WP-10 (split-context) **against the three-posture canon**, but their **build execution is gated** on Josh resolving `DEC-BC-POSTURE-VOCAB`. This node consumes the resolution; it does not author it (RESEARCH-RESULT residue).
- Constraint reaffirmed: NEVER revive "Sanitized" or a 4th posture. The substance/structure split under Split-Context Hybrid (closed-set allow-list + applicant-fact PRE-scan) achieves "power for drafting + privacy on substance" without opaque-slot tokens.

---

## 4. DECISION-GATED CALLOUT — GAP-TRB-UI-PHASE

**Owner: Josh / boundary-and-canon (governance). NOT resolved here.**

- Decision: `DEC-BC-UI-BOUNDARY` (boundary-and-canon ledger, status `flag`, `selected: PENDING`); gap `GAP-BC-UI-SCOPE`.
- v0.1 is **HEADLESS-ONLY (locked)** — no Next.js / no UI layer (CLAUDE.md "What NOT to Do").
- WP-12 (operator console) is scoped here as a **read-only projection / deferred phase ONLY** — never an interactive v0.1 UI. Whether the console is a v0.1 read-only projection, or a later-phase product surface, awaits `DEC-BC-UI-BOUNDARY`.
- WP-12 is **excluded from the v0.1 Golden Image (WP-14 / §2)** unless and until this decision ungates it as a read-only projection.

---

## 5. Per-gap verdict lines

- **GAP-TRB-WORK-PACKS** — REFINE-SOLVABLE → RESOLVED IN SPEC. 14 workbook rows decomposed into 13 sequenced, dependency-ordered work packs (§1) with owner, inputs, outputs, acceptance criteria, dependency edges, lane separation, critical path, and first steps. Owner: Vlad + Koichi.
- **GAP-TRB-GOLDEN-IMAGE-HANDOFF** — REFINE-SOLVABLE → RESOLVED IN SPEC. Golden Image interface contract authored (§2) as the B→A handoff to `hardware-golden-image` (`GAP-HGI-IMAGE-VERIFY` consumer), with artifact schema, signing/verification mechanism, and acceptance criteria. Owner: Vlad (lead) + Koichi.
- **GAP-TRB-POSTURE-CANON** — DECISION-GATED → NOT RESOLVED (callout only, §3). WP-9/WP-10 specced against three-posture canon; build execution blocked on `DEC-BC-POSTURE-VOCAB`. Owner: Josh / boundary-and-canon.
- **GAP-TRB-UI-PHASE** — DECISION-GATED → NOT RESOLVED (callout only, §4). WP-12 scoped as read-only projection / deferred only; excluded from v0.1 image. Blocked on `DEC-BC-UI-BOUNDARY`. Owner: Josh / boundary-and-canon (governance).

---

## 6. Guardrail compliance self-check

- Substrate LOCKED — no alternatives proposed (Pydantic AI + Logfire + Ollama/vLLM + DSPy/GEPA + Logician). ✓
- "Sanitized" / 4-posture NEVER revived — three-posture canon only; WP-10 carries split-context, drops sanitization-pipeline half. ✓
- No `[SLOT_*]` — deprecated mechanism present only as defense-in-depth, never normal-path. ✓
- No CIC→CLC coupling — WP-5/WP-6 are opportunity-driven runtime; `F-CIC-CLC-COUPLING-VIOLATION` clean. ✓
- v0.1 headless — WP-12 read-only projection / deferred only. ✓
- Law 3 — no `orgs/` PROJECT_CONTEXT read; structural cross-org guards retained. ✓
