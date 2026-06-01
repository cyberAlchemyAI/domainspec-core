---
title: Platform Engineer Onboarding Pack
audience: Paul Norton (incoming platform/ops engineer)
authored: 2026-05-15
authored_by: Tilth core (Cowork session, opus 4.7)
register: engineer-facing — not customer-facing, not operator-facing
companion: docs/platform_engineer_quick_reference.md
status: living document
---

# Platform Engineer Onboarding Pack — Tilth / Golden Quill

Welcome, Paul. This document orients you to the project surface in operations terms: deployment topology, observability stack, test playbook, file tree, ceremony vocabulary, and per-seat runbook. The companion file `docs/platform_engineer_quick_reference.md` is the 1-page daily-driver. Read this once end-to-end; bookmark the quick-reference.

The customer-facing playbook at `docs/white_glove_v0_1_beta.md` is operator-and-customer register — different audience, different vocabulary. Do not use it as your reference; use this pack.

---

## 0. Paul's context — what we know about your incoming surface

You bring 13+ years Linux + AWS, Kubernetes at scale (Smith Micro — 200+ microservices, 26M+ daily requests), Terraform/Ansible/Python/GitOps, observability across CloudWatch/Grafana/Elastic/Zabbix/ELK, security hardening, and AI-Ops *tooling* (Claude, Cursor, Copilot — used for ops, not building AI from scratch). Heavy self-hosted HomeLab background (ProxMox, Docker, Home Automation). You run **Norton Consulting** (Linux/BSD/AWS production workloads since 2017) and **Amnesia Labs** (`https://amnesia-labs.com`) as self-driven infrastructure work.

Two consequences for this pack:

1. **We do not re-explain SRE primitives.** Linux, Docker, Postgres, systemd, observability, key management, GitOps, signing, CI: assumed. If something looks under-explained, it's because we trust you've shipped it.
2. **We *do* translate every internal vocabulary item** that wouldn't appear in a typical SRE handbook — LOCK ceremony, F-code, Cedar, AST-lint, §0.5 Interface Index, Thesis cross-family rigor, KFR, etc. That's §1 below. If something here uses a term not in the glossary, that's a doc bug — flag it.

What this project is *not*: it is not a Kubernetes fleet, not a microservices estate, not a multi-region AWS deployment. It is a **single-tenant appliance** (one box, one customer, customer-owned hardware) running a fixed-graph AI pipeline + a deterministic policy gate layer. Closer to "well-instrumented single-node Python service with strong supply-chain discipline" than to anything you ran at Smith Micro. Your AWS + K8s muscle is highly relevant for **v2 multi-tenant horizon** (cooperative-owned compute, Stage 5); for v0.1 + v0.2 the discipline that maps best is your HomeLab + Norton Consulting work.

---

## 1. Glossary — internal vocabulary, in operations terms

Every term in this glossary appears in the body of this doc, and every internal term used in the body appears here. If you find one missing in either direction, that's a doc bug.

| Term | Plain translation |
|------|-------------------|
| **Tilth** | The software intelligence stack that ships on the Golden Quill appliance. Six-seat AI pipeline + support agents + Logician gate layer + Cedar policies + Vault data substrate. "Tilth" is the runtime; "Golden Quill" is the hardware. |
| **Golden Quill** | The physical hardware product. 128 GB-RAM-floor desktop appliance (Apple M3 Ultra Mac Studio, AMD GX-10, or NVIDIA DGX Spark / ASUS Ascent GX10). One per customer; customer-owned. |
| **Seat** | One agent role in the Tilth pipeline. Six **council** seats (Scout, Scribe, Editor, Judge, Red Team, Logician) plus support agents (Intake, Uploader, Data Collector, Report Generator, Archivist, WPFA Cycle Accountant). Each seat has a code module under `pipeline/orchestrator/seats/<seat>/`. |
| **Council** | The six core seats that handle a grant cycle. Modeled like a small editorial committee — no seat outranks another; operator decides ties. |
| **Cycle** | One end-to-end run: RFA (request-for-applications) ingested → Scout discovers → Scribe drafts → Editor/Judge/Red Team review → operator approves → Uploader stages submission → operator clicks final submit on funder portal. Post-award the cycle continues into AWARD_INGEST + (v0.2) reporting. |
| **RFA** | Request For Applications — the source document a funder publishes. Equivalent to a spec document. Per Law 1, every claim Tilth makes must trace to the RFA. |
| **PROJECT_CONTEXT** | The per-organization context file (`orgs/<slug>/PROJECT_CONTEXT.md`) that holds applicant-side facts the council reads. Equivalent to a tenant-config file. Law 3 forbids cross-reading between orgs. |
| **KFR (Key Facts Register)** | Per-org structured fact store with verbatim-quote-with-page provenance. Built from Intake BULK_INGEST at white-glove onboarding. Each fact has a freshness tag (SP0), a derivation chain, and a currency tolerance. Lives at `orgs/<slug>/vault/kfr/`. Architecturally LOCKED at v7.0.4 + v7.0.4-M1. |
| **SP0** | "Session Preflight 0" — the per-cycle context-freshness check Logician runs against the KFR before drafting begins. SP0 review surfaces stale facts the operator should refresh. |
| **AWARD_INGEST** | The Intake mode that fires when a grant is *awarded*. Extracts `proposal_commitments.yaml` (the promises the applicant made in the proposal) and binds them content-hash to the submitted draft so post-award reporting can verify against the actual commitments. |
| **proposal_commitments.yaml** | The list of "we said we would do X, Y, Z" the applicant promised in the proposal. Bound to the submitted draft by content hash so reporting cannot drift from what was actually promised. v0.2 Report Generator reads this. |
| **classification register** | Per-org file at `orgs/<slug>/vault/classification/register.yaml` that tags every fact as `public` / `shareable` / `confidential` / `operator_flagged`. The tags drive the routing decision (see §3). Operator Ed25519-signs the register at white-glove onboarding; new facts default to `confidential`. |
| **Classification Review** | The mandatory white-glove onboarding stage where the operator walks every per-org fact and assigns its class. Five sub-steps (Inventory → operator override → routing simulation → test cycle → Ed25519 sign-off). Without a signed register, the deployment fails closed. Wrapper at `pipeline/orchestrator/classification_review.py` + CLI `pipeline/cli/tilth_review_classify.py`. |
| **Logician** | The deterministic policy-gate layer. Not an LLM. Python predicates + Cedar policy evaluator. Runs PRE and POST every seat invocation. Fail-closed by default. Lives at `pipeline/logician/`. The only architectural primitive in Tilth that is *not* an AI seat. |
| **F-code / failure code** | A Logician gate identifier. Format: `F-<DOMAIN>-<NAME>` (e.g., `F-CLASS-REGISTER-UNSIGNED`, `F-INTAKE-EMBEDDING-NS-MISMATCH`, `F-WPFA-OPERATOR-SIGNATURE-MISSING`). Roughly 50 codes ship in v0.1 Beta. Each code is a Python predicate that returns PASS or FAIL with audit-log payload. When a code fails, the cycle stops. |
| **Cedar** | [AWS Cedar policy language](https://www.cedarpolicy.com/). Used here for declarative authorization decisions on data access (e.g., "Scribe may read fact F iff F.classification ∈ {public, shareable}"). Bootstrapped by Python at module-load; engine is mandatory at load — refusing to load any policy fail-closes the process. Policies live under `pipeline/vault/policies/`. |
| **AST-lint** | A static-analysis layer above pytest that walks the Python AST and refuses commits that violate structural invariants. Rule IDs format `R-<DOMAIN>-<NAME>` (e.g., `R-UPLOADER-NO-SUBMIT`, `R-ARCHIVIST-NO-CANONICAL-MUTATE`, `R-WPFA-DECIMAL-MANDATE-ENERGY`). Runner at `pipeline/linting/ast_lint.py`; runs via `scripts/run_lint.sh`. Used to enforce, e.g., "no module under `pipeline/orchestrator/seats/uploader/` may import `requests.post`" — structural prohibition, not policy. |
| **§0.5 Interface Index** | A spreadsheet-style ledger of every type, schema, signature, and module interface in the blueprint. Each row has a `kind` (e.g., `failure_code`, `pydantic_model`, `seat_method`, `ast_lint_rule`, `signed_asset`). When any blueprint section LOCKs, its interface contributions land as new §0.5 rows in a paired-commit. Lives at `pipeline/blueprint/v0.1/section_0_5_interface_index.md`. "runtime-live row count" = number of rows actually wired through to runtime. Currently 470 (rising). |
| **runtime-live row count** | The number of §0.5 Interface Index rows whose interfaces are wired through to runtime code (i.e., not v0.2-SPEC-ONLY stubs or HORIZON markers). Treat as a build-progress signal. Up from 232 (after §12 Uploader LOCK) to 470 today. |
| **paired-commit** | The discipline that any section LOCK lands its §0.5 amendment in the same commit / same lock_history row pair. No "blueprint LOCK without interface ledger update." Pair members get sequential lock_history rows (e.g., row 193 + row 194 for §4 v2.x + §0.5 v14). |
| **compound LOCK** | A LOCK that spans 3+ rows because one section change cascades into multiple paired commits (architecture + blueprint + §0.5 + sometimes §4 Logician). E.g., the §17 WPFA LOCK on 2026-05-11 was a compound quadruple: rows 205-208. |
| **LOCK ceremony** | The audit-trail-protected procedure that promotes a spec from DRAFT → LOCKED. Requires: a Thesis round (cross-family review), a verdict per L-005 two-cycle discipline (Editor / Judge / Red Team all weighing in), then an append to `pipeline/engineering/lock_history.v1.jsonl`. Once LOCKED, the text is immutable — changes are a new amendment, not an in-place edit. See §11 of this doc. |
| **lock_history.v1.jsonl** | The architectural-change ledger. Append-only JSONL. Each row is one LOCK event with `row`, `date`, `kind`, `verdict`, `parent_lock_row`, `model_tier`, plus payload. Currently 214 rows. Your single most useful file for "what changed recently in architecture." |
| **Thesis round** | The cross-family review cycle a LOCK candidate goes through. Editor + Judge + Red Team review the candidate independently, each running on a *different model family* (Llama/Groq, Gemini/Google, GPT-OSS/Groq). Two cycles per L-005 (no silent third round). Audit trail lands at `pipeline/validation/<topic>_thesis_<date>/`. |
| **cross-family rigor** | The discipline that no two seats sharing a model family review each other's work. Prevents same-family blind spots. Enforced operationally via the **osascript → openclaw bridge** — Cowork sessions dispatch to a local openclaw gateway running on Josh's M1; openclaw fans out to Groq/Google/Anthropic with different model selections per seat. Templates at `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh`. |
| **L-005** | "Lesson 005" — the two-audit-cycle discipline. Audit #1 scoping → fix → Audit #2 verification → LOCK or escalate. No silent third round. Lives in `pipeline/institutional_memory/lessons.json` (machine) and `lessons.md` (human). |
| **L-006** | "Lesson 006" — verify enforcement-layer existence on-disk before locking around it. (E.g., do not LOCK a gate code that has no implementing predicate yet.) |
| **Logfire spans** | The observability primitive. Tilth instruments every seat invocation, every Logician gate, every Cedar evaluation as a Logfire span. Logfire is Pydantic's hosted tracer (OpenTelemetry-compatible). Spans live in `pipeline/observability/`. |
| **opaque slot** | Privacy primitive at the cloud-routing boundary. Cloud-routed prompts may never contain semantic slot names like `[SLOT_ANNUAL_REVENUE]`. They contain only opaque numeric tokens like `[SLOT_001]`. The `slot_id → confidential_field_path` mapping lives in the local slot-fill agent, which renders confidential values into the post-fill draft *after* cloud-routed seats return. Enforced by `F-CLASS-SLOT-ID-NON-OPAQUE`. |
| **three-posture routing** | The deployment-topology choice each customer makes. Three postures (see §3): Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign. Locked at v7.0.7. |
| **M13** | The audited bypass mechanism. The *only* way to override a Logician fail-closed verdict. Requires operator-signed Ed25519 attestation in the audit log. Treat as a fire-extinguisher — present in case of emergency, expensive to use. |
| **A1, A4, A12** | "Architectural assumption N" from v7 LOCKED. **A1**: single-client per Golden Quill. **A4**: operator-trusted (operator has root on their own box). **A12**: Decimal mandate (no float arithmetic on money or other quantities that must canonicalize). These assumptions bound the threat model. v2 multi-tenant work opens A1+A4. |
| **bounded-by-A1+A4** | A failure mode that exists in the abstract but is acceptable in v0.1+v0.2 because A1 (single-client) and A4 (operator-trusted) make it not-exploitable in our deployment shape. Catalogued at `pipeline/architecture/v0.1/section_o_5_v2_known_limitations.md` (the "Section O.5" register) for the v2 amendment to revisit. |
| **CIC** | "Customer Identity Card." Six taxonomy entries describing what kind of organization the applicant is (Food Systems / Educator / Public Agency / Arts & Culture / Cooperative / Ecosystem Intermediary). Drives applicant-side primitives (vocabulary, evidence schema, language register, reporting rhythm). Cards at `assets/cards/customer_identification/`. |
| **CLC** | "Capital Logic Card." Eight taxonomy entries describing how funding flows (Public Purpose / Catalytic Change / Operating Capacity / Research & Evidence / Market Access / Credit & Underwriting / Sponsorship / Shared Assets). Drives funder-side primitives. Cards at `assets/cards/capital_logic/`. |
| **CIC × CLC orthogonality** | CIC and CLC are **orthogonal axes** — any pair is reachable. Tilth must not hardcode any CIC→CLC mapping. Enforced by `F-CIC-CLC-COUPLING-VIOLATION` at the Logician layer (architecture v7.0.8). |
| **WPFA** | "Watts Per Funding Action." The cycle-close accounting subsystem (§17, LOCKED 2026-05-11). Emits a typed `CycleReceipt` per cycle close with actual dollars + watt-hours consumed vs counterfactual (100% routed to the quarter's flagship cloud baseline) vs regenerative-savings delta. Powers the buyer-facing PDF — the sales lever. Cycle receipts at `orgs/<slug>/vault/operational/cycle_receipts/<cycle_id>.json`. |
| **CycleReceipt** | The typed Pydantic artifact §17 emits per cycle close. Signed by operator with Ed25519 before buyer-facing PDF emission. Decimal mandate extends to energy quantities (int micro-watt-hours; no float). |
| **Coefficient Registry** | The signed asset that holds the per-model dollars-per-million-tokens + watt-hours-per-token coefficients. Lives at `vault_shared/wpfa/coefficient_registry/active.yaml`. Publisher (router/coefficient operator) Ed25519-signs each release; white-glove pins the publisher pubkey at onboarding. Same trust mechanism as the router-template signing (byte-for-byte). |
| **router-template** | The signed asset that holds per-deployment routing configuration. `router.yaml` ships as a derived per-deployment template; updates ship Ed25519-signed; the Golden Quill verifies against the white-glove-pinned publisher key before applying. Pinned operator opts in per release (no auto-update). |
| **BYOK envelope** | "Bring Your Own Key" — the customer's BYOK API keys for Anthropic / Groq / Google / OpenAI (v0.1) and Twilio / Postmark / Mailgun / MTProto / WhatsApp Business API (v0.2). All keys are customer-owned; Tilth never holds keys; the keyring loader at `pipeline/orchestrator/keyring_loader.py` reads from operator-provided keystore. If FIT Farms vanished tomorrow, the customer keeps their keys. |
| **Golden Image** | The frozen substrate that ships at appliance build time. Pydantic AI + Logfire + Ollama/vLLM + curated Python document-parsing utilities (python-docx, openpyxl, pypdf). No package-manager access from the appliance post-build. Per ADR-001. Updates ship as signed Golden Image rebuilds. |
| **ADR-001** | The Architecture Decision Record that froze the v0.1 substrate. Locks Pydantic AI as orchestration + Logfire as observability + Ollama/vLLM for local inference + DSPy/GEPA offline only + Logician deterministic. Lives at `pipeline/architecture/v0.1/adr_001_substrate.md`. |
| **Ed25519** | The signing scheme used throughout for operator attestation, classification register signing, router-template signing, Coefficient Registry signing, CycleReceipt signing, WPFA buyer-PDF signing. Plan to extend to hybrid Ed25519+ML-DSA-65 at v0.2, pure post-quantum at v0.3 (crypto-agility envelope A12). |
| **spec card** | A planning artifact under `pipeline/planning/` that describes a workstream's goals, OQs (open questions), defaults if under-specified, and dispatch handoff. Equivalent to a design doc + RFC + ticket rolled into one. |
| **OQ** | "Open Question" — an unresolved decision flagged on a spec card. Has a default for under-specification. Operator resolves; spec card updates; LOCK proceeds. |
| **handoff** | A self-contained dispatch packet at `pipeline/handoffs/<workstream>.md` that a downstream Cowork session reads to begin work. Written by the upstream session as a pre-staging discipline. Targets <50 lines + bootstrap reference. |
| **daily_log** | The operational-change ledger. One file per day at `daily_logs/YYYY-MM-DD.md`. Holds what shipped, what broke, what's pre-staged. Distinct from `lock_history.v1.jsonl` (architectural changes) — the daily_log is broader. |
| **MEMORY.md** | The user-memory index at `memory/MEMORY.md`. One line per memory file. Names the project state, locked decisions, operator preferences, lessons. Loaded into every new session for institutional continuity. |
| **lessons.md** | The mandatory pre-check list at `/lessons.md`. Lessons (L-001…L-018+) that any session must respect. Includes L-002 "no content dumps, path references only," L-003 "cross-family review," L-005 "two-audit cycle," L-006 "verify enforcement on disk before locking." |
| **Cowork** | The Claude desktop application Josh uses to drive Tilth development. (Specifically, the "Cowork" feature that gives Claude file + shell access.) Sessions are operator-driven; Claude is the worker. |
| **openclaw** | A local LLM-gateway daemon that runs on Josh's M1 Mac Mini. Provides an OpenAI-compatible API plus a CLI (`openclaw infer model run --gateway --model X --prompt P --json`). Used as the cross-family Thesis dispatch bridge: Cowork → `osascript do shell script "openclaw ..."` → Groq/Google/Anthropic. Dashboard at `http://127.0.0.1:18789`. |
| **MaatAI** | Retired internal name (retired 2026-05-06). If you see it in old docs, mentally substitute "Sovereign Node" (no LLC). |
| **Sovereign Node** | The future Stage-5 cooperative-owned compute commons. Out of scope for v0.1, v0.2, v1.x. Internal-only naming. Never appears in customer-facing copy. |
| **FIT Farms / FIT Farms LLC / FIT Farms Commons** | Josh's operating legal entity is **FIT Farms LLC**. "FIT Farms Commons" is a file-naming label for the *owner-operator role*. Today both labels resolve to the same legal entity. Don't propagate any "Sovereign Node LLC" reference — that's stale. |

Anything else you hit in the docs that isn't in this glossary: flag it. Either the doc references a stale term, or the glossary needs an entry.

---

## 1.5. Rules vs Guidance — Calibration Invitation

The Tilth architecture is dense by design. 80+ failure codes across four orthogonal Logician gate families (F-CLASS / F-WPFA / F-PACKET / F-REFLECTION) plus six seat-owned families. Structured Cedar policies. AST-lint rules. Paired §0.5 rows. Compound LOCK ceremonies. Some of that density is genuinely load-bearing — Law-3 org isolation, Law-4 admin-risk (silent rewrites forbidden), fail-closed on auto-submit, KFR verbatim-quote provenance. Those are operator-protective and stay rigid.

But some of it may be ceremony that constrains the LLM's reasoning without commensurate safety gain. The architecture was specified during a single intense build cycle by an operator + AI pair who tended toward *more* rules rather than fewer when ambiguous. Rules that should have been *guidance* can quietly make the system slower, more brittle, or less able to absorb edge cases. The operator put it directly: "Paul knows many things I don't especially surrounding minimizing what is necessary to guide the intelligence."

**Explicit invitation.** If you read a rule and your gut says "this would work better as guidance to the model than a fail-closed gate" — surface it. Bring the candidate to the operator with:

- The rule's location (file + line / `F-CODE` / `R-RULE` ID).
- What it currently forecloses.
- What guidance language would replace it.
- What the failure mode looks like if guidance turns out to be enough.

The operator will weigh sovereignty preservation + Law-protection per change. This is not blanket permission to soften — it's an explicit invitation to surface candidates. Some rules will stay rigid even after your read. The point is to get them on the table.

---

## 2. Architecture summary in operations terms

### The shape of the system

Tilth is **one Python process** (or a small handful of long-running processes, depending on deployment posture — see §3) that runs a fixed graph of AI agent invocations with a deterministic policy-gate layer wrapping each agent call. Substrate is Pydantic AI for orchestration + Logfire for observability + Ollama/vLLM for local inference + Cedar + custom Python for policy. No microservices. No K8s. No service mesh. One box per customer.

A grant cycle, end-to-end:

1. **Scout DISCOVER** — reads seven channel families in parallel (federal APIs / cached datasets / state+foundation portals / federal program pages / RSS+newsletter / client-material-driven web search / local funder-intel corpus). Outputs candidate opportunities.
2. **Scout VERIFY** — for any candidate flagged CRITICAL-fit, hits the live funder endpoint to confirm synopsis matches. Tags each candidate VERIFIED_FIT / VERIFIED_NOT_FIT / UNVERIFIED / VERIFICATION_FAILED.
3. **Scout REVIEW** — operator gate. Operator approves which opportunities advance.
4. **Phase 0 Intake** — for each approved opportunity, Intake validates the RFA against the org's KFR + PROJECT_CONTEXT. Three coherence predicates fire (P-COHERE-1/2/3).
5. **Scribe drafts** — section by section. Pulls from KFR. Runs KGIE preflight (Knowledge Gap & Inflation Edit — flags places where the draft is making claims the KFR doesn't support). Hits funder-dialect register-matching.
6. **Editor reviews** — clarity, jargon, goal/output/outcome/objective sorting.
7. **Judge scores** — against funder's own rubric first, then cross-checks the rubric library at `pipeline/rubrics/`.
8. **Red Team challenges** — adversarial review. Must run on a different model family than Scribe AND Judge. If Judge and Red Team disagree by ≥10 points, council splits and operator decides.
9. **Operator approves the draft.**
10. **Uploader stages submission** — assembles the package for the funder portal (Grants.gov Workspace / SAM.gov / Common Grant Application / copy-paste fallback). **Operator clicks final submit** on the funder portal. Auto-submit is architecturally prohibited.
11. **Logician runs PRE and POST every seat** with the full Five Laws + classification gates + seat-owned gates. Any FAIL stops the cycle.
12. **WPFA Cycle Accountant emits a CycleReceipt** at close: actual $ and Wh consumed, counterfactual vs the quarter's flagship cloud baseline, savings delta.

Post-award: **AWARD_INGEST** extracts `proposal_commitments.yaml` from the won draft. v0.2 ships Data Collector (grantee outreach across 5 channels) and Report Generator (funder-ready reports using `report_mode` track). v1.x ships Archivist (long-running curation, lessons memory).

### Five v0.2+ support agents (one sentence each)

- **Intake** (v0.1) — bulk-ingests organization documents at white-glove setup; extracts candidate facts with verbatim-quote-with-page provenance for operator confirmation; three modes (BULK / INCREMENTAL / AWARD).
- **Uploader** (v0.1) — assembles operator-approved final proposal into funder-portal-required formats and stages submission; four portal adapters; operator clicks final submit.
- **Data Collector** (v0.2 horizon) — grantee/sub-awardee outreach across email + SMS + voice + Telegram + WhatsApp; compliance-first (CAN-SPAM, TCPA, per-recipient consent); spec LOCKED, code-phase wiring underway.
- **Report Generator** (v0.2 horizon) — generates funder-ready reports from Data Collector data under the same Logician PRE/POST discipline as council seats; spec LOCKED, code phase Slice 2 landed 2026-05-11.
- **Archivist** (v1.x horizon) — long-running curation: Funder Intel DB, Match DB, KFR maintenance, lessons memory; **proposes-only** — never auto-applies (enforced by three-layer defense: AST-lint + runtime guard + Cedar policy).

### The Logician is not an LLM

This is the one detail that surprises every infrastructure engineer who joins. The Logician seat is the policy-gate layer. It is **pure Python + Cedar**. Zero LLM calls. Zero token cost. Deterministic. Fail-closed by default. Runs PRE and POST every other seat invocation. Enforces the Five Operating Laws + classification gates + per-seat gates as deterministic predicates.

If a Logician gate fails, the cycle stops. The only override is M13 — operator-signed Ed25519 attestation in the audit log, single-use, audited.

You will hear the Logician described as "a seat" because architecturally it sits next to Scout/Scribe/Editor/Judge/Red Team in the council diagram. Mentally tag it as **the firewall** — it runs alongside but does a different kind of work.

---

## 3. Three-posture routing model

Locked at architecture v7.0.7 (2026-05-10). Each customer's classification register drives a *per-call* routing decision: cloud frontier or local. The three postures are the three coherent shapes that decision pattern takes at deployment time.

| Posture | What it means | Deployment topology | Customer-facing fit |
|---------|---------------|---------------------|---------------------|
| **Frontier-Eligible** | Customer has tagged most facts as `public` or `shareable`. Almost all calls route to cloud frontier models (Anthropic / Google / Groq). Local LLM exists for slot-fill agent (always local) + Logician. | Golden Quill node + cloud API keys (Anthropic + Groq + Google + OpenAI BYOK). Local Ollama/vLLM still present but mostly used for slot-fill. Lightest local-model footprint. | Customers with low confidentiality requirements (e.g., a public-agency applicant whose facts are already FOIA-able). Fastest, cheapest, best quality at draft time. |
| **Split-Context Hybrid** | Customer has a mix. `public+shareable` facts route to cloud; `confidential+operator_flagged` facts route to local 70B-class model. High-stakes grants trigger on-demand 200B-class heavy-Judge swap (loaded from NVMe; ~2-5 min wall). | Golden Quill node + cloud API keys + local LLM (70B-class via Ollama/vLLM, e.g., Llama 3.3 70B; on-demand 200B-class heavy-Judge swap from NVMe). Largest deployment shape — runs both worlds. | Default for most customers. Privacy on confidential facts, frontier capability on public-shareable inputs. The "power for drafting + privacy for review" pattern. |
| **Local-Only-Sovereign** | Customer wants nothing leaving the box. All seats route to local LLM. No cloud keys configured. | Golden Quill node + local LLM only. No BYOK cloud keys. Slot-fill agent + Logician + Cedar all local. | Customers with strict data-residency requirements (regulated industries, sensitive populations). Slower, more compute-intensive, but no cloud trust assumption at all. |

The classification register is the **load-bearing primitive**. Without a signed register, the gate `F-CLASS-REGISTER-UNSIGNED` fail-closes the cycle. The Classification Review stage (mandatory in white-glove onboarding) is where the operator walks every fact and assigns its class.

A few specifics for ops:

- **Indeterminate routing fails closed to local.** If the classifier can't decide for a given call, `F-CLASS-ROUTING-INDETERMINATE` fires; cycle routes that call to local LLM rather than guessing cloud.
- **New facts default to `confidential`.** Any fact ingested via Intake INCREMENTAL after onboarding starts as `confidential` until the operator re-classifies. Enforced by `F-CLASS-NEW-FACT-UNCLASSIFIED`.
- **Cloud-routed prompts use opaque slot tokens only.** No semantic slot names like `[SLOT_ANNUAL_REVENUE]` — those leak structure even when the value is hidden. Cloud prompts use `[SLOT_001]` etc.; the local slot-fill agent holds the mapping and renders post-fill drafts. Enforced by `F-CLASS-SLOT-ID-NON-OPAQUE`.
- **Heavy-Judge swap flag itself is classified `confidential`.** Knowledge that a customer triggered a high-stakes grant is itself a side-channel. Enforced by `F-CLASS-HIGH-STAKES-FLAG-LEAK` (POST-call gate on cloud payloads).

Cite: architecture v7.0.7 LOCKED 2026-05-10 (`pipeline/architecture/v0.1/architecture_v7_0_7_locked.md`). The §6.1 signed-router-template trust mechanism mirrors the same Ed25519 pattern that WPFA Coefficient Registry uses (byte-for-byte).

---

## 4. Deployment topology

### Hardware tiers

| Tier | Spec | Use |
|------|------|-----|
| **Dev** | Apple M1 Mac Mini, 8 GB RAM | Josh's dev node. The full test suite + AST-lint + smoke must pass here. "If it runs on 8 GB, it flies on 128 GB." |
| **Baseline** | Apple Mac Studio M3 Ultra, 128 GB RAM (floor) | Customer Golden Quill baseline. The 128 GB floor was set 2026-04-19; older 32 GB / 64 GB references are stale. |
| **Pro** | NVIDIA DGX Spark / ASUS Ascent GX10 / AMD GX-10 — 128 GB+ unified memory | Customer Golden Quill Pro tier. Same software, more headroom for heavy-Judge swaps. |

Phase 1 commercial target ("Founding 12" — mid-Jul 2026 → mid-Apr 2027, 12 Pittsburgh deployments across the six CICs) is Pro tier GB10-class.

### Software substrate (frozen at Golden Image)

Per ADR-001 (locked in v0.1):

- **Orchestration**: Pydantic AI (agent primitives + structured output)
- **Observability**: Logfire (OpenTelemetry-compatible, Pydantic-hosted)
- **Local inference**: Ollama (default) or vLLM (alt) — OpenAI-compatible endpoint
- **Document parsing**: python-docx, openpyxl, pypdf wrapped as Pydantic AI tools
- **Offline training/refinement**: DSPy + GEPA (Library development only — does not run on the appliance at runtime)
- **Policy gates**: Logician = Python + Cedar (deterministic, fail-closed, zero-token)

**LangGraph and OpenClaw are *not* in the substrate.** LangGraph was never wired. OpenClaw is a separate local LLM gateway used for **cross-family Thesis dispatch during development** — it does not run on the customer appliance. (Confusable: openclaw the dev-tool ≠ Tilth the runtime.)

### BYOK envelope

Customer-owned, never held by FIT Farms:

| Provider | Use | v0.1 / v0.2 |
|----------|-----|-------------|
| Anthropic | Scribe primary | v0.1 |
| Groq | Editor / Red Team / Scout fallback | v0.1 |
| Google | Judge primary | v0.1 |
| OpenAI | Red Team escalation / fallback | v0.1 |
| Postmark or SendGrid or Mailgun | Data Collector email channel | v0.2 |
| Twilio | Data Collector SMS + voice channels | v0.2 |
| MTProto (Telegram Bot API) | Data Collector Telegram channel + Cultivator | v0.2 |
| WhatsApp Business API | Data Collector WhatsApp channel | v0.2 |

Keys loaded by `pipeline/orchestrator/keyring_loader.py` from the operator-provided keystore. Keys are never logged, never written to disk outside the keystore, never sent in audit payloads.

### Golden Image rebuild cadence

Soft commitment: quarterly template review minimum; 7-day emergency updates for meaningful upgrades. Every router-template release is Ed25519-signed by the Golden Quill publisher. Customer appliances verify against the white-glove-pinned publisher pubkey *before* applying an update. Failure → `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` → stay on the prior pinned version.

Public-key rotation requires the new key co-signed by the previous (Trust-On-First-Use rotation, audited).

---

## 5. Observability stack

### Logfire spans

Every seat invocation, every Logician gate evaluation, every Cedar policy decision, every Vault read/write, every cycle step emits a Logfire span. Trace IDs propagate end-to-end across a cycle. Logfire is OpenTelemetry-compatible — if you want to ship spans elsewhere (Grafana Tempo, Honeycomb, Datadog), the export path is configurable. Default is Pydantic-hosted Logfire.

Instrumentation lives at `pipeline/observability/`. The process-wide Logfire bootstrap shim landed in v7.0.4-M1 (forces span emission at process start so Logician PRE-gates always have a span context to attach to).

### What spans to watch

| Span name | What it tells you |
|-----------|-------------------|
| `seat.scout.discover` | Scout's 7-channel parallel discovery completion + per-channel timing |
| `seat.scout.verify` | Live funder endpoint calls + per-candidate verdict |
| `seat.scribe.draft.<section>` | Per-section drafting; pulls the model_id and token count |
| `seat.editor.review` / `seat.judge.score` / `seat.red_team.challenge` | Cross-family review; check that model families on these three differ |
| `seat.logician.pre.<F-CODE>` / `seat.logician.post.<F-CODE>` | Gate evaluations; FAIL spans carry the audit payload |
| `seat.intake.<mode>` | BULK / INCREMENTAL / AWARD ingest progress |
| `seat.uploader.stage.<portal>` | Per-portal package assembly |
| `seat.wpfa.cycle_close` | WPFA accountant emitting the cycle receipt |
| `vault.read.<sub_kind>` / `vault.write.<sub_kind>` | Operational data substrate access |
| `cedar.evaluate.<policy_id>` | Cedar policy evaluations |

### Alerts to set

| Condition | Severity | Why |
|-----------|----------|-----|
| Any `seat.logician.*` span with status=FAIL | HIGH | Cycle stopped. Operator needs to know. |
| `seat.scribe.draft` model_id matches `seat.judge.score` model_id at the family level | HIGH | Cross-family rigor violated. Investigate routing. |
| `vault.write` to `confidential` classification with cloud-routed parent span | CRITICAL | Classification leak. Should be impossible (F-CLASS gates catch it); if it fires, something bypassed. |
| `seat.scout.verify` returns >50% VERIFICATION_FAILED in a single cycle | MEDIUM | Funder endpoints flaky; check Grants.gov / SAM.gov status. |
| `seat.uploader.stage` span without subsequent operator-action span within 24h | LOW | Draft staged but not submitted. Maybe stale. |
| Logfire bootstrap fails at process start | CRITICAL | Span context will not attach; gate audit log incomplete. Process must restart. |
| Local LLM (Ollama/vLLM) endpoint unreachable | HIGH (Split-Context / Local-Only) or LOW (Frontier-Eligible) | Posture-dependent. |
| Disk usage on `vault/` partition >80% | MEDIUM | Cycle receipts + KFR + Cedar audit logs accumulate. Plan retention. |

### Logs as ledgers

Two append-only ledgers are themselves observability:

- **`pipeline/engineering/lock_history.v1.jsonl`** — architectural changes (LOCKs). Append-only JSONL, hash-chain-friendly. Treat as your "what shape did the system have on date X."
- **`daily_logs/YYYY-MM-DD.md`** — operational changes, by day. What shipped, what broke, what's pre-staged. Treat as your "what happened on date X."

When something breaks, tail both. The `lock_history` tells you what *structurally* changed; the `daily_log` tells you what *operationally* changed.

### Per-seat critical metrics

| Seat | Metric | Why |
|------|--------|-----|
| Scout | Per-channel completion rate, VERIFY pass rate | DISCOVER without VERIFY → bad downstream candidates |
| Scribe | KGIE preflight pass rate, section completion %, model_id distribution | KGIE catches inflation; track drift |
| Editor | Replacement-option count per flagged issue | Quality signal |
| Judge | Score distribution, rubric coverage | Drift detection |
| Red Team | Disagreement-with-Judge magnitude | >10pts triggers council split |
| Logician | Gate evaluations/sec, FAIL rate by code | The most useful health signal |
| Intake | Verbatim-quote-with-page coverage, NEEDED-tag count | Coverage gap |
| Uploader | Per-portal stage success rate | Operator-side reliability |
| WPFA | Cycle receipt emission rate, $ + Wh deltas | The accounting signal |

---

## 6. Per-seat runbook (v0.1 + v0.2 seats)

Concise scan-format. For deep dive on any seat, go to its blueprint at `pipeline/blueprint/v0.1/section_<NN>_<name>.md`.

### Scout (v0.1, council)
- **Code:** `pipeline/orchestrator/seats/scout/` + `pipeline/scout/`
- **Reads:** RFA inputs, funder corpus at `vault_shared/funder_intelligence/`, classification register
- **Writes:** Candidate roster to `pipeline/radar/`, VERIFY results, REVIEW staging
- **Known bounded:** Per-channel rate-limit handling assumes single-customer (A1); fleet-wide rate-limit pooling is v2.
- **Known open:** Channel G (local funder-intel corpus) sanitization is fresh — watch `F-FUNDER-CORPUS-*` gate rates.

### Scribe (v0.1, council)
- **Code:** `pipeline/orchestrator/seats/scribe/` + `pipeline/drafts/`
- **Reads:** RFA, PROJECT_CONTEXT, KFR (`orgs/<slug>/vault/kfr/`), funder rubric, Scribe knowledge pack
- **Writes:** Section-by-section drafts at `pipeline/drafts/<grant_id>/`
- **Routing posture:** Cloud-frontier for `public+shareable` input; local 70B for any `confidential` input bearing post-fill draft (always-local once post-fill)
- **Known bounded:** Heavy-Judge swap timing side-channel bounded by A1+A4 (operator-trusted, single-client); v0.2 padding-latency extension marker.
- **Known open:** None at v0.1 LOCK quality.

### Editor (v0.1, council)
- **Code:** `pipeline/orchestrator/seats/editor/` + `pipeline/editor/`
- **Reads:** Scribe draft
- **Writes:** Annotated draft + clarity report
- **Routing:** Local 70B for any post-fill draft (the common case). Cloud only if input is post-fill-clean (rare).

### Judge (v0.1, council)
- **Code:** `pipeline/orchestrator/seats/judge/` + `pipeline/scores/`
- **Reads:** Scribe draft, funder rubric (`pipeline/rubrics/<rubric>.json`), rubric library
- **Writes:** Per-dimension score + evidence-string trace to `pipeline/scores/<grant_id>/`
- **Family rule:** Must not share family with Scribe. Current default: Scribe=Anthropic, Judge=Google.
- **Heavy-Judge swap:** High-stakes grants flip to local 200B-class (e.g., DeepSeek V3 / Qwen 3 235B / Mistral Large 2 / GPT-OSS 120B). 2-5 min wall. Flag itself is `confidential`.

### Red Team (v0.1, council)
- **Code:** `pipeline/orchestrator/seats/red_team/`
- **Reads:** Scribe draft, Judge score, funder rubric
- **Writes:** Challenge report
- **Family rule:** Must not share family with Scribe AND Judge. Default: GPT-OSS via Groq.
- **Trigger:** Disagreement with Judge ≥10 pts triggers council split — operator decides per Law 4 tie-breaker.

### Logician (v0.1, council)
- **Code:** `pipeline/logician/` (predicates) + `pipeline/vault/policies/` (Cedar)
- **Reads:** Everything every other seat reads or writes
- **Writes:** Gate verdicts to audit log (`pipeline/logician/audit/`)
- **Runtime cost:** Zero tokens. Pure Python + Cedar.
- **Known bounded:** Several gate families have v0.2 stub predicate bodies (`F-FG-*`, parts of `F-REPORT-*` v1) that raise `NotImplementedError` until v0.2 flips them LIVE.
- **The fire-extinguisher:** M13 is the only bypass. Treat as audited emergency stop.

### Intake (v0.1, support, always-local)
- **Code:** `pipeline/orchestrator/seats/intake.py`
- **Modes:**
  - **BULK_INGEST** — white-glove onboarding bulk doc absorption with verbatim-quote-with-page provenance
  - **INCREMENTAL_INGEST** — between-cycle fact additions; new facts default `confidential`
  - **AWARD_INGEST** — post-award; extracts `proposal_commitments.yaml` content-hash-bound to the won draft
- **Owned gates:** 11 F-INTAKE-* codes (`-EMBEDDING-NS-MISMATCH`, `-CONFIG-SIGNATURE-INVALID`, `-EMBEDDING-ENDPOINT-INVALID`, `-WATCHER-TOCTOU`, etc.)
- **Known bounded:** Watcher TOCTOU bounded by A1+A4.
- **Known open:** None at LOCK quality (v1.1 narrow-corrective landed 2026-05-11 for commitment_id sanitization, RT-C2-02 closure).

### Uploader (v0.1, support, always-local)
- **Code:** `pipeline/orchestrator/seats/uploader/`
- **Adapters:** Grants.gov Workspace, SAM.gov, Common Grant Application, copy-paste fallback. Foundant / Submittable / Fluxx are v1.1 (Path-b scope).
- **Owned gates:** 10 F-UPLOADER-* codes + `R-UPLOADER-NO-SUBMIT` AST-lint rule
- **Three-layer auto-submit defense:** AST-lint allow-list + network-namespace isolation (ASPIRATIONAL at v0.1) + `@typing.final` invariant
- **Discipline:** Prepare-and-stage only. **Operator clicks final submit on funder portal.** This is architectural, not policy.
- **Known bounded:** Network-namespace isolation (Layer 2) is ASPIRATIONAL in v0.1 — Layers 1 + 3 carry the load.
- **Known open:** Attachment family deferred to v1.1.

### Data Collector (v0.2 horizon, support)
- **Code:** `pipeline/orchestrator/seats/data_collector/` (Slice landed 2026-05-10)
- **Channels:** email + SMS + voice + Telegram + WhatsApp
- **Owned gates:** 8 F-DATACOLLECTOR-* codes incl. `-BENEFICIARY-CONSENT-TIER` (Cycle 1 RT-28 closure) + `-OPT-OUT-PROPAGATION-FAILED` (Cycle 2 RT-C2-02 closure)
- **Four-layer autosend defense:** AST-lint + dispatcher signature + Cedar policy + TTY check
- **Per-recipient channel-bound shared-secret tokens** with AEAD nonces + `revoked` field
- **Cross-channel opt-out propagation:** all-or-nothing copy-on-write rollback (Cycle 2 RT-C2-02 closure)
- **Known bounded:** Cultivator-vs-DC shared MTProto substrate with four structural separations; operator override available
- **Known open:** State-rules card (PA/CA/FL/TX/NY first wave) is SN-LLC-signed v0.2 first wave; not v0.1

### Report Generator (v0.2 horizon, support)
- **Code:** `pipeline/orchestrator/seats/report_generator/` (Slice 2 landed 2026-05-11; Slice 3 wiring pre-staged)
- **Track:** `report_mode` in §5 v8 track registry — currently **refuses at runtime via `F-PIPE-TRACK-NOT-SHIPPABLE`** until WS-J flips `shippable_in: v0.2` to `true`
- **Five sub-sections:** narrative + metrics_table + financial_summary + photo_gallery + beneficiary_section
- **Reads:** `proposal_commitments.yaml` (claim → evidence trace) + Data Collector outputs + KFR
- **Writes:** `claim_evidence_map.yaml` per-claim trace + operator Ed25519-signed report
- **Owned gates:** 5 F-REPORT-* codes (`-UNTRACED`, `-COMMITMENT-MISSED`, `-OUT-OF-SCOPE-DRIFT`, `-NUMERIC-DRIFT`, `-TEMPLATE-MISMATCH`)
- **AST-lint:** `R-REPORT-DECIMAL-MANDATE` extends Decimal mandate to report composers
- **Known bounded:** Post-sign draft immutability via flock + chmod (Layer 2 mitigation)
- **Known open:** Slice 3 wiring pending (`run_report_pipeline` + `finalize_operator_signed_report` + first-wave marker hash binding)

### Archivist (v1.x horizon, support, between-cycle)
- **Code:** `pipeline/orchestrator/seats/archivist/__init__.py` (skeleton only at v0.1)
- **Cadences:** weekly + quarterly (workspace-shared + per-org submode split per §15.4.2)
- **Discipline:** **Proposes-only.** Never auto-applies. Operator approves every change.
- **Three-layer defense:** AST-lint (`R-ARCHIVIST-NO-CANONICAL-MUTATE`) + runtime guard + Cedar policy
- **Owned gates:** 5 F-ARCHIVIST-* codes (`-CROSS-ORG-LEAK`, `-LESSON-INSTANCE-LEAK`, `-AUTO-APPLY-ATTEMPTED`, `-CADENCE-DRIFT`, `-READ-WITHOUT-VAULT-INTENT`)
- **Known bounded:** Several dynamic-call evasion classes bounded by A1+A4 (catalogued at Section O.5 v2 for the v2 multi-tenant amendment)
- **Known open:** Runtime implementation deferred to v1.x; v0.2 cadence is operator-driven manual invocation

### WPFA Cycle Accountant (v0.1, support, always-local, cycle-close)
- **Code:** `pipeline/orchestrator/seats/wpfa/` (Code phase pre-staged after §17 v1 LOCK 2026-05-11)
- **Reads:** Logfire span tree of the cycle, Coefficient Registry (`vault_shared/wpfa/coefficient_registry/active.yaml`)
- **Writes:** `orgs/<slug>/vault/operational/cycle_receipts/<cycle_id>.json` + (operator-signed) buyer-facing PDF
- **Owned gates:** 12 F-WPFA-* codes with **LIVE predicate bodies at LOCK** (first §4 amendment with live bodies)
- **A12 Decimal mandate extended to energy:** int micro-watt-hours; no float
- **Three-layer buyer-PDF defense:** AST-lint + Cedar + runtime gate
- **Operator Ed25519 attestation gates buyer-facing PDF emission** (`F-WPFA-OPERATOR-SIGNATURE-MISSING` — M13 NOT permitted; structural attestation boundary)
- **Sibling-not-nested with Reflection Packet** (shared input substrate = Logfire span tree; zero shared output)

---

## 7. Known failure modes — bounded vs open

### "Bounded-by-A1+A4" — intentionally not defended against at v0.1+v0.2

The v7 LOCKED assumptions A1 (single-client per Golden Quill) and A4 (operator-trusted on their own box) bound an entire class of threat models that v0.1+v0.2 do not defend against. The v2 multi-tenant amendment opens them. Catalogued at `pipeline/architecture/v0.1/section_o_5_v2_known_limitations.md`.

Examples — these are **not defects**, they are deliberate scope boundaries:

| Surface | What's not defended | Why bounded |
|---------|---------------------|-------------|
| Heavy-Judge swap timing | Cloud observer could infer "this customer is filing a high-stakes grant" from swap latency pattern | A1: only one customer per box; A4: operator chose to load the heavy-Judge themselves |
| Cross-channel opt-out propagation timing | Race window during opt-out rollout | A1: single org per box; rollback is atomic per-org |
| Per-channel rate-limit handling | No pool-wide rate limit coordination | A1: only one Scout instance per box |
| Logfire bootstrap shim attack surface | If an attacker can run code at process start before bootstrap, span context misses | A4: operator-trusted root; no untrusted code path at process start |
| Dynamic-call evasion of AST-lint enforcement | An attacker writing Python can dynamically resolve forbidden imports | A4: no untrusted code in the runtime tree |
| Watcher TOCTOU on Intake INCREMENTAL | File-rewrite-during-watch race | A1+A4: single operator on box |

These are documented in commit messages as `bounded-by-A1+A4` for grep-ability. When v2 multi-tenant lands, the catalogued items get re-opened as work items.

### Known + open — defects to be aware of

| Surface | Status | Mitigation |
|---------|--------|-----------|
| Uploader network-namespace isolation (Layer 2 of three-layer defense) | ASPIRATIONAL at v0.1 | Layers 1 (AST-lint allow-list) + 3 (`@typing.final` invariant) carry load |
| `report_mode` track runtime-shippable | DORMANT at v0.1 | `F-PIPE-TRACK-NOT-SHIPPABLE` refuses any attempt to dispatch a report cycle |
| `F-FG-*` family predicate bodies | STUB at v0.1 | Will raise `NotImplementedError` if FundingGoal is exercised; v0.2 SPEC-ONLY by design |
| `R-FG-STUB-ONLY-AT-V0_2` AST-lint | active | Refuses any code that tries to call FundingGoal in v0.1 |
| Test `tests/gpp/*` GROQ_API_KEY env-dependence | known | These tests require GROQ_API_KEY in env; skip if absent. Not a real failure. |
| Test interference from §11 v1.1 reload protocol | known per 2026-05-11 daily log | Reload-protocol contract is stateless; tests that import `_commitment_id` should run in fresh interpreter or use `importlib.reload`. Failure mode: stale module reference. |

### What "fail-closed" looks like in practice

When a Logician gate fails, the cycle stops at that point. The audit log captures the gate code, the payload, the seat that triggered it, and the operator-visible reason. No partial state advances downstream. The operator either fixes the underlying condition (e.g., re-sign the classification register, refresh a stale KFR fact) or invokes M13 (audited bypass — Ed25519-signed attestation).

This is intentional. The system would rather refuse to file a grant than file one with a structurally broken trace.

---

## 8. Test-running playbook

### Pinned interpreter (NON-NEGOTIABLE)

```sh
scripts/run_tests.sh [tests/subdir] [-k keyword]
```

That script pins `.venv/bin/python3` (Python 3.14). **Do not run `python3 -m pytest`** — system Python on macOS is 3.9 and cannot even *collect* the test suite (`@dataclass(frozen=True, kw_only=True)` requires 3.10+; pyproject pins `>=3.11`). System Python will report 8 collection errors that look like real failures. They are not. Always use `.venv/bin/python3` directly or via `scripts/run_tests.sh`.

If `.venv/bin/python3` is missing, the script prints rebuild instructions. Rebuild the venv with Python 3.14 before continuing.

### Linting

```sh
scripts/run_lint.sh [pipeline] [tests]
```

That runs `pipeline.linting.ast_lint` on the given paths. Exit codes: `0` = clean, `1` = violations, `2` = environment error. Output format: `<file>:<line>:<col>: <RULE_NAME> [<reason_tag>] <message>`. All AST-lint rules (R-UPLOADER-NO-SUBMIT, R-ARCHIVIST-NO-CANONICAL-MUTATE, R-WPFA-DECIMAL-MANDATE-ENERGY, etc.) live under `pipeline/linting/`.

### Smoke vs full

- **Smoke:** the per-seat skeleton-test subsets. Runs in seconds. Good for "did I break the wiring?"
- **Full:** the entire suite, ~340+ tests at current count. Required green before any LOCK ceremony.

### Pre-existing failures to ignore

These are not your fault and not your problem unless we ask:

1. **`tests/gpp/*` requiring `GROQ_API_KEY`** — env-dep; passes when GROQ_API_KEY is exported, skips/fails otherwise. Don't chase.
2. **Cross-test interference from `pipeline/orchestrator/seats/_commitment_id`** — flagged in daily_log 2026-05-11. The reload-protocol contract is stateless, but pytest's import caching can leave a stale reference. If a single test passes in isolation but fails in suite, this is the suspect. Workaround: `importlib.reload` or run that test file alone.

### CI status

There is no CI yet beyond the local dev node. Setting up GitHub Actions (or your preferred CI) on the public repo is a candidate item for your first sprint — see §14 v0.2 production cut path.

---

## 9. File-tree map

```
/Users/goldenquill/Downloads/GoldenQuill/             ← workspace root
├── SOUL.md             ← operating principles (Five Laws, Four Rules)
├── USER.md             ← operator identity + decision framework
├── AGENTS.md           ← agent wake-up + invocation rules
├── CLAUDE.md           ← Cowork-specific supplement (the file you've already read)
├── MEMORY.md           ← memory index (loaded into every session)
├── lessons.md          ← mandatory pre-check list (L-001..L-018+)
├── router.yaml         ← seat-model bindings (SOLE source of truth)
├── README.md           ← public-facing description
├── pyproject.toml      ← Python ≥3.11; .venv must use 3.14
├── docs/               ← THIS DOC + architecture overview + white-glove + customer one-pagers
├── orgs/               ← per-org folders (Law 3 isolation)
│   ├── _TEMPLATE/      ← blank PROJECT_CONTEXT for new clients
│   ├── ORG_INDEX.md    ← master index of clients
│   └── <slug>/
│       ├── PROJECT_CONTEXT.md
│       └── vault/
│           ├── kfr/             ← Key Facts Register (signed)
│           ├── classification/  ← classification register (operator-signed)
│           └── operational/     ← metrics, financials, photos, etc.
├── pipeline/                       ← the runtime + specs
│   ├── SESSION_BOOTSTRAP.md        ← new-session orientation (read first)
│   ├── architecture/v0.1/          ← LOCKED architecture (v7 + amendments)
│   ├── blueprint/v0.1/             ← seat blueprints (§NN_<name>.md)
│   ├── engineering/
│   │   ├── lock_history.v1.jsonl   ← THE ARCHITECTURAL CHANGE LEDGER
│   │   ├── engineering_process_v0.1.md
│   │   └── spec_cards/             ← per-workstream design docs
│   ├── orchestrator/seats/         ← runtime seat code
│   │   ├── scout/ scribe/ editor/ judge/ red_team/
│   │   ├── intake.py
│   │   ├── uploader/
│   │   ├── data_collector/
│   │   ├── report_generator/
│   │   ├── archivist/
│   │   └── _commitment_id.py       ← shared canonical module
│   ├── orchestrator/
│   │   ├── classification_review.py  ← Classification Review orchestrator
│   │   ├── keyring_loader.py
│   │   ├── routing.yaml
│   │   └── audit_assembler.py
│   ├── cli/                        ← CLI entry points
│   │   └── tilth_review_classify.py
│   ├── logician/                   ← gate predicates (F-CODE-*.py)
│   │   ├── audit/                  ← gate audit logs
│   │   └── gates/<F-DOMAIN-NAME>.py
│   ├── linting/                    ← AST-lint rules + runner
│   │   ├── ast_lint.py
│   │   └── r_<rule>_<name>.py
│   ├── vault/                      ← substrate + Cedar policies
│   │   ├── policies/               ← *.cedar files
│   │   └── schemas/                ← sub-kind Pydantic models
│   ├── validation/                 ← Thesis audit trails (per topic per date)
│   │   └── <topic>_thesis_<date>/
│   ├── planning/                   ← spec cards, dispatch plans, scoping drafts
│   │   ├── v0_1_lock_and_clear_packet_2026-05-11.md  ← current
│   │   ├── v0_2_dispatch_plan_2026-05-09.md
│   │   └── ...
│   ├── handoffs/                   ← pre-staged session dispatch packets
│   │   └── ws_<workstream>_<date>.md
│   ├── institutional_memory/
│   │   ├── lessons.json            ← machine-readable
│   │   └── (lessons.md at root is human-readable)
│   ├── metrics/
│   │   ├── SESSION_METRICS_SPEC.md
│   │   └── session_log.jsonl       ← per-session metrics (efficiency tracking)
│   ├── observability/              ← Logfire instrumentation
│   ├── rubrics/                    ← Judge rubrics (vapg_fy26.json, etc.)
│   ├── radar/ drafts/ editor/ scores/  ← per-cycle outputs
│   ├── rfa/                        ← RFA staging
│   ├── knowledge_packs/            ← Scribe knowledge packs
│   ├── scout/                      ← Scout-specific databases
│   ├── delivery_log/               ← Tilth feed delivery records
│   ├── subscribers/                ← Tilth feed subscriber roster
│   ├── seats/_commitment_id.py     ← shared (the canonical home)
│   └── templates/                  ← component analysis, efficiency audit, etc.
├── tests/                          ← pytest tree
├── daily_logs/                     ← daily operational change ledger
│   └── YYYY-MM-DD.md
├── memory/                         ← user memory files (auto-memory)
├── scripts/
│   ├── run_tests.sh                ← PINNED INTERPRETER — use this
│   └── run_lint.sh
├── skills/                         ← Cowork skills (scout-discovery, scribe-ghostwriter, ...)
├── assets/cards/                   ← CIC + CLC + MyCel + Console cards
├── vault_shared/                   ← workspace-shared signed assets
│   ├── funder_intelligence/        ← funder corpus
│   └── wpfa/coefficient_registry/active.yaml  ← signed Coefficient Registry
├── Sovereign_Node_Handoff/         ← long-form design docs + prior work assets
└── _private/                       ← out-of-tree private materials
```

Quick rules of thumb:

- **Architecture changed?** Check `pipeline/architecture/v0.1/` + the lock_history tail.
- **Blueprint changed?** Check `pipeline/blueprint/v0.1/` + the lock_history tail.
- **Runtime broke?** Check `pipeline/orchestrator/` + the daily_log + Logfire spans.
- **Gate failed?** Check `pipeline/logician/gates/<F-CODE>.py` + `pipeline/logician/audit/`.
- **Cedar refused?** Check `pipeline/vault/policies/*.cedar` + `cedar.evaluate.<policy_id>` spans.
- **AST-lint refused a commit?** Check `pipeline/linting/r_*.py` for the rule body.
- **Need to know what's planned next?** Check `pipeline/planning/` + `pipeline/handoffs/`.
- **Need full project context?** Read `pipeline/SESSION_BOOTSTRAP.md` + `MEMORY.md` + last two daily_logs.

---

## 10. The LOCK ceremony — what it is and why ops should care

A **LOCK** promotes a spec from DRAFT → immutable. It is the project's structural change-control discipline. Until something LOCKs, it's a candidate; once it LOCKs, the text cannot be edited in place — changes are a new amendment that compounds onto the existing LOCK.

This matters operationally because:

1. **The audit trail is the source of truth for architecture state on date X.** When you need to know "what shape did the system have when we cut Beta?" — you tail `lock_history.v1.jsonl` and look at parent_lock_row pointers.
2. **Paired commits are atomic.** A section LOCK lands its §0.5 Interface Index amendment in the same row pair. Never edit one without the other.
3. **The `parent_lock_row` field is a forward-reference graph.** If row 190 (`architecture_amendment_M1`) has `parent_lock_row=178`, that means row 190 is a corrective on row 178. Pop the corrective if you ever revert; or in M1's case, `parent_lock_row=178` documents that row 178 is "LOCKED but NEEDS_M1" until 190 cleared the gate.

### How to read a lock_history row

```json
{
  "row": 193,
  "date": "2026-05-10",
  "kind": "blueprint_amendment",
  "verdict": "LOCKED",
  "parent_lock_row": null,
  "model_tier": "opus_4_7",
  "topic": "§4 Logician v2.x WS-L (~44 codes; F-CLASS-COVERAGE-INCOMPLETE activated; v0.1 Beta gate CLEARED)"
}
```

Fields:

- **`row`** — monotonic integer
- **`date`** — author timezone
- **`kind`** — one of `architecture_amendment`, `blueprint_amendment`, `blueprint_section`, `blueprint_amendment_companion`, `architecture_amendment_M1` (narrow corrective), `external_review_disposition`, `architecture_amendment_verif` (cross-family verification), and a few rare ones
- **`verdict`** — `LOCKED`, `SELF_LOCKED`, `CONFIRMED`, `VERIFICATION_PASS_NEEDS_M1`, `DISPOSITIONED`
- **`parent_lock_row`** — for amendments + corrections + verifications + companions
- **`model_tier`** — the model tier the LOCK ceremony ran on (current default: `opus_4_7`)
- **`topic`** — human-readable summary

### Today's cascade for context

Today (2026-05-11) and yesterday (2026-05-10) saw ~37 LOCKs in 36 hours — `rows 178 → 214`. The cascade closed the v0.1 Beta architectural gate at row 193 (§4 Logician v2.x; `F-CLASS-COVERAGE-INCOMPLETE` activated). Today's tail (rows 200-214) is the v0.2 SPEC-LOCK wave (§14 Report Generator, §17 WPFA, §2 v7.5 FundingGoal, §11 v1.1 narrow-corrective) plus paired interface index amendments. The system has not been this dense with LOCKs before; the cadence will normalize after the v0.1 Beta cut.

You don't need to internalize every LOCK. You need to **know how to read the ledger when something is on fire**.

---

## 11. Cross-family Thesis — what it is and why ops should care

The project's review discipline requires that no two seats reviewing each other's work share a model family. **Cross-family rigor** = the structural commitment + the operational mechanism that enforces it.

### Structural commitment

When Scribe drafts on Anthropic, Judge must score on a different family (currently Google/Gemini), and Red Team must challenge on a third family (currently Groq/GPT-OSS). Same applies at LOCK ceremony review time: Editor reviewer + Judge reviewer + Red Team reviewer all run on different families. Same-family review is treated as no-review.

### Operational mechanism — the openclaw bridge

Cowork sessions (where Josh + Claude do most of the development) run inside the Claude desktop app. To dispatch to a non-Anthropic model family, the session uses `osascript` → `do shell script` → the local `openclaw` gateway running on Josh's M1:

```sh
osascript -e 'do shell script "PATH=$HOME/.npm-global/bin:$PATH openclaw infer model run \
  --gateway --model groq/llama-3.3-70b-versatile --prompt @prompt.json --json" \
  with timeout of 600 seconds'
```

The three live model IDs:

- **Editor** — `groq/llama-3.3-70b-versatile`
- **Judge** — `google/gemini-2.5-pro` (timeout 600s for thinking-mode)
- **Red Team** — `groq/openai/gpt-oss-120b`

Working dispatch templates at `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh`.

### Section E carve-out (rare, disciplined)

There's a single-Claude carve-out for cases where the openclaw bridge is unavailable. **It requires a logged dispatch failure to invoke** — captured curl/openclaw error in the audit trail. Not a default fallback. Discipline lives at `/AGENTS.md` § "Section E carve-out — invocation discipline."

### Why this matters for ops

If something in your area touches review dispatch (e.g., openclaw daemon down, Groq quota exhausted, Gemini thinking-mode timeout): the cross-family path is the project's enforcement mechanism for review quality. If it falls through to single-Claude silently, the project's structural review discipline degrades. The fix is to restore the bridge, not to paper over with carve-out.

---

## 12. v0.1 Beta cut readiness

Current source-of-truth packet: `pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md` (supersedes the 2026-05-10 readiness audit).

### Architectural gate — CLEARED 2026-05-10

The v0.1 Beta architectural gate was the `F-CLASS-COVERAGE-INCOMPLETE` META PRE-cycle gate at architecture v7.0.7. It refuses to deploy Beta until §4 Logician v2.x realizes the twelve F-CLASS-* primitives. **§4 v2.x LOCKED at row 193 on 2026-05-10**, clearing the gate.

### What's LOCKED for v0.1 Beta

- **Architecture:** v7 LOCKED (A1-A12) + amendments v7.0.1 GPP + v7.0.2 substrate + v7.0.3 Pydantic AI + v7.0.4 KFR + v7.0.4-M1 corrective + v7.0.5 Funder Intel + Match DB + v7.0.6 six-seat council canonical + v7.0.7 Beta classification routing + v7.0.8 CIC × CLC orthogonality
- **Blueprint:** §2 v7.2 operational sub-kinds + §5 v8 track registry + §11 v1 + v1.1 Intake + §12 v1 Uploader + §15 v1 Archivist SPEC + §4 v2.x + v2.x.1 Logician + companion §0.5 amendments
- **WPFA §17 v1** with LIVE predicate bodies, Coefficient Registry, buyer-PDF substrate
- **Classification Review wrapper** (orchestrator + CLI) — LANDED 2026-05-10
- **Intake + Uploader full implementations** — smoke green 2026-05-11
- **Submission_mode track + eval_mode track** — ACTIVE

### What's still in flight

- **WS-J §14 Report Generator code phase** — Slice 2 LANDED 2026-05-11; Slice 3 (`run_report_pipeline` wiring + `finalize_operator_signed_report` + AST-lint rules + first-wave marker hash binding) is pre-staged. v0.2 horizon — does NOT block v0.1 Beta cut.
- **WS-WPFA code phase** — predicate-body finalization + orchestrator wiring + buyer-PDF substrate. Parent rows 205-208. Pre-staged.
- **Reflection Packet** — DISPATCH_SPEC_DRAFT promoted from SCOPING_DRAFT on 2026-05-11. Compound triple LOCK target = §16 v1 + §4 v2.x.y F-PACKET-* (19 codes; 18 NotImplementedError + 1 LIVE META) + §0.5 v20. v0.1 Beta hook ships dormant primitives only.
- **v7.0.10 architecture sweep** — in flight; parallel surface; no conflict with onboarding pack work
- **First dogfood Beta deployment dry-run** — 1-2 sessions; integration probe

### Cut ceremony (what it entails operationally)

Roughly the order of operations Paul should expect when the v0.1 Beta first-customer cut fires:

1. Verify full pytest suite green on `.venv/bin/python3` (~340+ tests)
2. Verify AST-lint clean on `pipeline/` + `tests/`
3. Verify the active classification register on `orgs/_TEMPLATE/` round-trips through `pipeline/cli/tilth_review_classify.py`
4. Run smoke on Intake BULK + INCREMENTAL + AWARD modes
5. Run smoke on Uploader 4 portal adapters + copy-paste fallback
6. Verify `vault_shared/wpfa/coefficient_registry/active.yaml` signature against pinned publisher pubkey
7. Verify per-org `vault/classification/register.yaml` signs and verifies end-to-end
8. Run a synthetic end-to-end cycle on the dev node and confirm cycle receipt emission
9. Tag the cut in `lock_history.v1.jsonl` (kind: `release_cut`, currently nonexistent — we'll add)
10. Author the public release announcement

This is your candidate sprint surface once you're ramped.

---

## 13. v0.2 production cut path

Per `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md` §6 — the v0.2 production cut readiness checklist:

### What v0.2 adds beyond v0.1

- **Data Collector** — 5 channels (email/SMS/voice/Telegram/WhatsApp). Channel modules + BYOK envelope (Twilio + Postmark/SendGrid + MTProto + WhatsApp Business API) + state-rules card (PA/CA/FL/TX/NY first wave; SN-LLC-signed)
- **Report Generator** — `report_mode` track flips `shippable_in: v0.2` to `true`; 5 sub-section composers + Cedar bootstrap + legacy migration shim
- **FundingGoal** (v0.2 first wave per spec card; pending OQ-1) — per-org persistent funding intent; Scout DISCOVER goal-aware ranking; Match DB goal-aware composite score
- **Reflection Packet** (v0.2 horizon per default; pending operator scope decision) — typed Pydantic BaseModel emitted at cycle close; feeds Archivist learning loop
- **WS-N integration testing** — 6 end-to-end scenarios on M1 8GB dev node (scenarios 1-2 are v0.1-derivable; 3-6 are v0.2)
- **Crypto-agility migration** — Ed25519 → hybrid Ed25519 + ML-DSA-65 (A12 envelope)

### v0.2 cut readiness boxes (subset for ops)

Most boxes are LOCKED at spec. The work remaining is **integration + smoke + dogfood**.

| Box | Status |
|-----|--------|
| WS-N six end-to-end scenarios pass on M1 8GB | 🔴 not dispatched |
| CIC × CLC orthogonality regression on every new schema | 🟡 baseline 84 tests passing; new schemas need re-run |
| Full pytest suite green | 🟡 presumed green at each LOCK commit; needs current-commit verification |
| AST-lint clean across pipeline/ + tests/ | 🟡 presumed clean; needs current-commit verification |
| State-rules card ships PA/CA/FL/TX/NY first wave | 🔴 depends on WS-I (Data Collector) full code phase |
| BYOK envelope documented for Twilio + Postmark + MTProto + WhatsApp | 🔴 depends on WS-I |
| First opted-in client for v0.2 R.3 reporting pilot | 🔴 operator decision |

v0.2 cut is weeks-to-months out at current cadence. v0.1 Beta cut is the immediate horizon.

---

## 14. Pointer index — where to look for what

### Architecture + blueprint

- Architecture v7 LOCKED: `pipeline/architecture/v0.1/tilth_architecture_locked.md`
- Architecture amendments (v7.0.1 → v7.0.9+): `pipeline/architecture/v0.1/architecture_v7_0_<N>_<status>.md`
- Blueprint sections: `pipeline/blueprint/v0.1/section_<NN>_<name>.md`
- §0.5 Interface Index: `pipeline/blueprint/v0.1/section_0_5_interface_index.md`
- ADR-001 substrate: `pipeline/architecture/v0.1/adr_001_substrate.md`

### Planning + dispatch

- Current v0.1 lock-and-clear packet: `pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md`
- v0.1 Beta launch posture: `pipeline/planning/v0_1_beta_launch_posture_2026-05-10.md`
- v0.1 Beta readiness: `pipeline/planning/v0_1_beta_readiness_2026-05-10.md` (superseded but useful historical context)
- v0.2 dispatch plan: `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md`
- Spec cards: `pipeline/planning/spec_card_*.md`
- Handoff packets: `pipeline/handoffs/ws_<workstream>_*.md`

### Audit trails

- Lock history (architectural change ledger): `pipeline/engineering/lock_history.v1.jsonl`
- Thesis audit trails: `pipeline/validation/<topic>_thesis_<date>/`
- Cross-family dispatch templates: `pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v{1,2}.sh`
- Logician gate audit logs: `pipeline/logician/audit/`
- Daily logs: `daily_logs/YYYY-MM-DD.md`
- Session metrics: `pipeline/metrics/session_log.jsonl`

### Memory + institutional knowledge

- MEMORY.md (memory index): `memory/MEMORY.md`
- Lessons (mandatory pre-checks): `lessons.md` (root) + `pipeline/institutional_memory/lessons.json`
- Session bootstrap: `pipeline/SESSION_BOOTSTRAP.md`

### Runtime

- Orchestrator seats: `pipeline/orchestrator/seats/<seat>/`
- Logician gates: `pipeline/logician/gates/<F-CODE>.py`
- AST-lint rules: `pipeline/linting/r_<rule>_<name>.py`
- Cedar policies: `pipeline/vault/policies/*.cedar`
- Vault schemas: `pipeline/vault/schemas/*.py`
- Router (seat → model bindings): `router.yaml` (root) + `pipeline/orchestrator/routing.yaml` (derived)

### Customer-facing docs (different register — don't use for engineering)

- White-glove playbook: `docs/white_glove_v0_1_beta.md`
- Architecture overview: `docs/ARCHITECTURE_OVERVIEW.md` (cleaner-than-engineering, useful for ramp)
- Lessons-memory one-pager: `docs/lessons_memory_external_one_pager.md`
- Public README: `README.md`

### Paul-specific companion doc

- **`docs/paul_norton_memory_alignment_brief_2026-05-15.md`** — read after this onboarding pack. Maps where your Amnesia Labs work (Brain + JIT) lands against Tilth's weakest dimension (Memory = 4/10). Three deployment shapes named (A: Brain hosted public/shareable layer; B: self-hostable inside Golden Quill; C: port architecture into local substrate). First-90-day load-bearing focus areas.

### Operator identity (these define what Tilth *is* — read once)

- `SOUL.md` (Five Operating Laws, Four Autonomy Rules)
- `USER.md` (operator identity, decision framework)
- `AGENTS.md` (agent wake-up rules)
- `CLAUDE.md` (Cowork supplement — referenced as authoritative project context)

---

## 15. First-week ramp plan (suggested)

Order, not prescription:

1. **Day 1 morning** — Read this doc end-to-end + the quick-reference. Tail `lock_history.v1.jsonl` (last 50 rows). Tail `daily_logs/` (last 3 entries). Tail `pipeline/metrics/session_log.jsonl` (last 10 entries).
2. **Day 1 afternoon** — Read `SOUL.md` + `USER.md` + `AGENTS.md` + `CLAUDE.md`. Skim `pipeline/SESSION_BOOTSTRAP.md`. Get the venv built and `scripts/run_tests.sh` green.
3. **Day 2** — Read `docs/ARCHITECTURE_OVERVIEW.md` + skim a couple of locked blueprint sections (§11 Intake + §17 WPFA recommended — concrete, recent). Read `docs/white_glove_v0_1_beta.md` to know what the customer experience is.
4. **Day 3** — Stand up Logfire local dev. Run a synthetic cycle through the orchestrator and watch spans. Tail `pipeline/logician/audit/`. Get familiar with the gate-audit-log shape.
5. **Day 4-5** — Read one Thesis audit trail end-to-end (recommend `pipeline/validation/v7_0_5_thesis_2026-05-09/`). This is the shape of how decisions get made in this project. Run a dispatch template locally to feel the bridge pattern.

By end of week 1, you should be able to:

- Tail the change ledgers and know what shipped this week
- Run the test + lint commands on the pinned interpreter
- Identify which seat owns a runtime issue from a Logfire span tree
- Read a `F-CODE` gate and find its predicate body
- Read a `R-RULE` AST-lint and find its enforcement
- Find the spec card or handoff for any in-flight workstream
- Know the difference between bounded-by-A1+A4 and a real defect

What you do NOT need to internalize yet:

- The full set of ~50 F-codes (look them up by domain when you need them)
- The CIC × CLC card details (assets/cards/* — read when relevant)
- The Stage-2 → Stage-5 cooperative model (read when v2 multi-tenant lands)

---

## 16. How to escalate

- **Architecture question** ("can I change X?") — read the relevant LOCKED amendment first. If the question survives the read, surface it to Josh. Do not edit LOCKED text in place.
- **Runtime defect** — file in daily_log + create a spec card if the fix needs structural change. Triage: bounded-by-A1+A4 vs real defect.
- **Tooling gap** — write the tool. Land in `tools/` or `scripts/` or `pipeline/cli/` per fit.
- **Doc gap** — flag it. This pack is a living document; we'd rather find the gaps than ship them.
- **Cross-family dispatch broken** — debug openclaw daemon first; check `http://127.0.0.1:18789` dashboard. Do not silently fall through to single-Claude.

Josh runs the operator agenda. He's terse and decisive. Don't redirect his focus to what you think the priority should be; answer the question he asks. If you disagree with a priority, push back constructively in one message, then execute. He'll override hard when he thinks you're wrong; expect it and don't sandbag.

---

**End of onboarding pack.** Companion file: `docs/platform_engineer_quick_reference.md`.

For project orientation in a new session, read `pipeline/SESSION_BOOTSTRAP.md` first.
