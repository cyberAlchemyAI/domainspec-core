# Tilth Architecture Overview

**Version:** v7 LOCKED 2026-04-19 (A1–A12) + LOCKED amendments through v7.0.10 (v7.0.1 GPP · v7.0.2 substrate · v7.0.3 Pydantic AI · v7.0.4 + v7.0.4-M1 KFR · v7.0.5 Funder Intel + Match DB · v7.0.6 six-seat council · v7.0.7 Beta classification routing · v7.0.8 CIC × CLC orthogonality · v7.0.9 Reflection v0.1 hook · **v7.0.10 three-posture routing model** LOCKED 2026-05-11)
**v0.1 Beta posture:** lock-and-clear packet active 2026-05-11. The submission workflow architecture is locked; the current clearance target is a reproducible v0.1 run package, safe claim language, Classification Review sign-off, and technical-lead handoff. Current cut packet: [`pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md`](../pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md).
**Audience:** Technical collaborators, Hackers Guild, infrastructure partners

## What Tilth Does

Tilth is a six-seat agentic AI pipeline plus a small set of support agents that discovers grant opportunities, drafts proposals, reviews them for clarity, scores them against funder rubrics, adversarially challenges them, and validates every output through deterministic policy gates — all running with classification-driven routing between local hardware the client physically owns and operator-curated frontier cloud touchpoints.

It serves five sectors: workforce of the future, future-proof education, food systems, land and community development, and eco-art.

## Core Principles: The Five Operating Laws

Every architectural decision traces back to these:

1. **RFA Is Truth** — the Request for Applications is the only authoritative source. Claims that can't be traced to the RFA or applicant's project context don't ship.
2. **No Boundary Drift** — stay inside funder-defined scope. No silent expansion.
3. **Org Isolation** — one client context per session. Cross-referencing between organizations is a hard failure.
4. **Apolitical Language + Admin-Risk** — dialect code-switching per funder profile, plus a live flagged-terms register with severity tiers. Never silently rewrite.
5. **Applicant Brings Substance** — shape existing credentials into funder-ready form. Never fabricate.

## The Six Seats

```
                    ┌─────────────────────────────────────────────┐
                    │              OPERATOR (human)               │
                    │         sets gear · approves outputs         │
                    └──────────────────┬──────────────────────────┘
                                       │
              ┌────────────────────────┼────────────────────────┐
              ▼                        ▼                        ▼
     ┌─────────────┐         ┌─────────────┐          ┌─────────────┐
     │    SCOUT    │         │   SCRIBE    │          │   EDITOR    │
     │  discover   │────────▶│   draft     │─────────▶│   clarity   │
     │  + verify   │         │  sections   │          │   review    │
     └─────────────┘         └─────────────┘          └──────┬──────┘
                                                              │
                                                              ▼
                                                     ┌─────────────┐
                                                     │    JUDGE    │
                                                     │   score vs  │
                                                     │   rubric    │
                                                     └──────┬──────┘
                                                              │
                                                              ▼
                                                     ┌─────────────┐
                                                     │  RED TEAM   │
                                                     │ adversarial │
                                                     │  challenge  │
                                                     └──────┬──────┘
                                                              │
                                              (>10 pt split? human decides)
                                                              │
                    ┌─────────────────────────────────────────┘
                    ▼
           ┌──────────────┐
           │   LOGICIAN   │
           │ deterministic │
           │ PRE/POST     │
           │ policy gates  │
           └──────────────┘
           (wraps every seat)
```

**Scout** runs two stages: DISCOVER reads six parallel channel families (federal APIs, cached datasets, state/foundation portals, federal program pages, RSS watchlists, client-material-driven web search), then VERIFY fetches live synopses before any candidate is elevated. Runs local on Ollama (mistral:7b) — zero API cost for the high-volume discovery loop.

**Scribe** drafts proposals section-by-section with KGIE (Knowledge Gap Identification Engine) preflight, SMART outcomes, an overlooked-expenses checklist, and funder-dialect code-switching. Beta routing follows the operator-selected deployment posture per v7.0.10: under Frontier-Eligible, Scribe routes Public + Shareable input to cloud frontier and composes Confidential-bearing sections locally; under Split-Context Hybrid, Scribe's scaffold composition routes cloud against an operator-signed allow-list (RFA + structural template + dialect keywords only) and substance composition routes local; under Local-Only / Sovereign, every Scribe call routes local.

**Editor** reads Scribe's output through different eyes — flags jargon, offers 2-3 concrete replacement options per issue, sorts goals from outputs from outcomes from objectives. Makes grants accessible to people who know their work but don't write grants professionally. Beta default: Llama 70B Q4 local-routable; cloud frontier when input is Public + Shareable.

**Judge** scores against the funder's own rubric first, then cross-checks related rubrics from the library. Uses Semi-Formal Reasoning (SFR) verdict format: Premises with citations → Execution trace → Conclusion grounded only in declared premises. **Cross-family rigor is mandatory** — Judge must not share a provider family with Scribe. High-stakes grants (federal long-form, large awards, operator-flagged cycles) trigger an on-demand local heavy Judge — a 200B-class model loaded for the cycle under the current signed Golden Quill router template.

**Red Team** runs adversarial challenge against every draft. Cross-family rigor against Scribe and Judge — never shares provider family with either. Disagreement of 10 or more points between Judge and Red Team triggers a council split, and the human decides (Law 4 tie-breaker; boundary inclusive at threshold per §10.6). Beta default: Qwen 32B-class local-routable; cloud frontier when input is Public + Shareable.

**Logician** is not an LLM. It is deterministic Python + Cedar policy validation. Fail-closed. Enforces all Five Laws as PRE-gates (before seat invocation) and POST-gates (after seat output). 30 architectural failure-code primitives. Zero token cost. Cannot be overridden except through M13 (operator emergency bypass, audited, 24-hour expiry, HIGH-severity admin-risk ledger entry).

## Cross-Family Adversarial Rigor

No seat reviews its own model family's work. The current routing enforces at minimum three distinct provider families across the council. Five LLM-using council seats run on five distinct families today (the requirement is overcovered):

- Scribe: cloud frontier (operator's choice; Anthropic Claude Sonnet 4.6 default for current router)
- Judge: routine — Meta (Llama 70B local-routable) / heavy on-demand — best-of-breed 200B-class under the current signed Golden Quill router template
- Editor: Meta (Llama 70B local-routable; cloud frontier when input is Public + Shareable)
- Red Team: OpenAI-OSS (Groq GPT-OSS 120B cloud-routable) / Alibaba (Qwen 32B local-routable) / OpenAI direct (GPT-5.1 escalation)
- Scout: Local (Mistral via Ollama)

A Judge-Red Team disagreement of 10 or more points triggers a council split — the human decides (Law 4 tie-breaker; boundary inclusive at threshold per §10.6).

## Deterministic Validation Layer

The Logician enforces a deterministic gate chain at every pipeline run:

- **PRE-gates** fire before any seat prompt compiles. Ordered by precedence (trust-root → index freshness → router schema → structural invariants → per-seat template → dormant extensibility guards).
- **POST-gates** fire after seat output. Validate verdict format, citation presence, coherence predicates, cross-window contradiction, Commons payload scope.
- **Fail-closed default.** If a gate cannot determine pass/fail, it refuses. The only bypass is M13 (operator emergency override), which is itself gated by admin-risk ledger discipline.

## Phase 0 Intake

Before any drafting begins, each RFA passes through a distinct intake phase: ingest (dual-hash signed RFA) → dissect (rubric-aligned structural analysis) → eligibility check → substance gap analysis → cross-check contracts (RFA ↔ dissection, dissection ↔ project context, dissection ↔ section list). Three coherence predicates (P-COHERE-1/2/3) enforce consistency throughout.

## Support Agents

Beyond the council seats, Tilth runs a small set of support agents that handle work around the grant cycle:

- **Intake** (v0.1, onboarding) — bulk-ingestion of organization documents at white-glove setup. Extracts candidate facts with verbatim-quote-with-page provenance. Operator confirms each fact before it lands in the Key Facts Register. Always-local agent (sees raw uploaded docs).
- **Uploader** (v0.1, submission) — assembles the final operator-approved proposal into the funder-portal-required formats and stages it for submission. **Prepare-and-stage discipline only** — operator clicks final submit on the funder's portal. Always-local agent (assembles final draft with all confidential filled).
- **Data Collector** (v0.2 horizon, post-award) — outreach to grantees and sub-awardees via email, text, and voice for performance data, evidence, and milestone reports. Compliance-first — CAN-SPAM, TCPA, per-recipient consent.
- **Report Generator** (v0.2 horizon, post-award) — generates funder-ready reports using Data Collector's gathered data, under the same Logician PRE/POST discipline as council seats.
- **Archivist** (v1.x horizon, between-cycle) — long-running curation: Funder Intelligence Database, Match Database, KFR maintenance and expiry tracking, lessons memory, audit trail.

## Beta Model Strategy — Three-Posture Classification-Driven Routing

Per architecture **v7.0.10 LOCKED 2026-05-11**, Tilth's Beta deployment runs a per-agent-call routing decision under one of **three customer-facing postures**. Posture is operator-selected at white-glove onboarding alongside the per-field classification register; per-call routing composes posture × per-field class.

1. **Frontier-Eligible** — customer permits selected project data to route to external/frontier models. Tilth assigns the strongest available model to each role per benchmark fit, prior results, task type, and cost/performance. Per-field classification register (public, shareable, confidential, operator_flagged — 4 values unchanged from v7.0.7 §2) drives routing: public + shareable fields route cloud; confidential + operator_flagged remain local (operator override via per-grant SP0 + HIGH-severity admin-risk ledger).
2. **Split-Context Hybrid** — frontier models help with structure, section strategy, prompts, funder-language framing, and generic draft scaffolds. Cloud-routable inputs are restricted to the operator-signed Split-Context allow-list at `orgs/<slug>/vault/classification/split_context_allowlist.yaml` (closed-set check: RFA text + funder agency name + funder rubric + program template name + section-structure-spec + KGIE-checklist keywords + dialect-classification value). Confidential local data stays on the node. A local model inserts restricted facts, evidence, metrics, names, and applicant-specific substance separately. *No opaque-slot rendering round-trip.*
3. **Local-Only / Sovereign** — every seat runs on the local 70B-class stack with on-demand 200B-class heavy-Judge swap. Maximum-custody posture; **marked as performance-dependent / under validation** until proven against real grant workloads. Customer-facing materials carry an explicit under-validation notice; the per-deployment manifest field `local_only_validated: bool` (default false; write-protected; flips only on SN-LLC quarterly validation outcome signature) gates "production-validated" claims on any customer-facing artifact.

For each agent call:

```
posture = deployment_posture()  # one of: frontier_eligible, split_context_hybrid, local_only_sovereign
if posture == local_only_sovereign:
    → route LOCAL (no further checks needed)
elif posture == frontier_eligible:
    if any input contains confidential OR operator_flagged:
        → route LOCAL (unless per-grant SP0 override authorized;
                       F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED applies)
    elif all input is public + shareable:
        → route CLOUD frontier per router template
    else:
        → fail-closed LOCAL default per F-CLASS-ROUTING-INDETERMINATE
elif posture == split_context_hybrid:
    if seat in {scribe_scaffold, scout, intake_classification_review}
    and payload field-paths ⊆ split_context_allowlist
    and applicant-fact pre-cloud scan passes:
        → route CLOUD frontier (scaffold / structure work only)
    else:
        → route LOCAL  (substance composition; class-indeterminate; review-shape seats)
```

Post-substance-assembly drafts (any draft carrying Confidential-bearing substance — the common case under Frontier-Eligible + always under Split-Context Hybrid) route every subsequent seat (Editor / Red Team / routine-Judge) to local execution. The substance/structure boundary under Split-Context Hybrid is the load-bearing separation: cloud sees the funder's RFA + scaffold instructions; cloud never sees the applicant's specific facts, partnerships, financials, or capacity (`F-CLASS-SPLIT-CONTEXT-ALLOWLIST` PRE-gate fail-closes any payload outside the allow-list; `F-CLASS-SPLIT-CONTEXT-LEAK` PRE-gate fail-closes any applicant-fact match in the allowed payload).

**Always-local agents**: Logician (deterministic), Intake, Uploader, Reflection sub-mode of Archivist (v7.0.9 row 202).

**Cloud-routable agents (only when posture permits AND input class permits)**: Scribe, Editor, Judge, Red Team, Scout (per channel). The slot-fill agent module remains in the runtime tree as **defense-in-depth-only** — never invoked in normal-path cycle operation under any v7.0.10 posture.

**On-demand local heavy Judge**: 200B-class model **pre-loaded on the Golden Quill at white-glove onboarding** (operator-signed Golden Image build pin). The swap operation is a local-execution-pointer-switch only — no network fetch, no remote download, no background-sync service. `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD` fail-closes any heavy-Judge swap that would trigger a network fetch (model binary missing from pinned local path, hash mismatch with Golden-Image-signed manifest, operator override to fetch from remote URL, or any background daemon attempting binary update outside the operator-attested router-template flow). The high-stakes flag itself is classified `confidential` (per v7.0.7 §4.1) — stored in per-grant `grant_overrides`, never sent to any cloud-routed seat; `F-CLASS-HIGH-STAKES-FLAG-LEAK` fail-closes any cloud payload referencing it. Heavy-Judge swap timing latency (2-5 min) is observable as a side-channel; v0.1 disposition: known limitation bounded by v7 LOCKED A1 (single-client) + A4 (operator-trusted); v2 multi-tenant mitigation in v7 LOCKED Section O.5; admin-risk ledger entry per heavy-swap event (severity MEDIUM, tag `timing-side-channel-v0.1-known`).

**Three-posture routing diagram:**

```
                  ┌──────────────────────────────┐
                  │   Operator-selected posture  │
                  │   (Ed25519-signed at white-  │
                  │   glove Classification       │
                  │   Review step 3 + step 4)    │
                  └──────────────┬───────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
   ┌──────────────────┐ ┌────────────────────┐ ┌──────────────────┐
   │ Frontier-        │ │ Split-Context      │ │ Local-Only /     │
   │ Eligible         │ │ Hybrid             │ │ Sovereign        │
   │                  │ │                    │ │ (under           │
   │ Public+Shareable │ │ Cloud: scaffold +  │ │  validation)     │
   │ → cloud          │ │ structure only,    │ │                  │
   │ Confidential +   │ │ closed-set         │ │ Every seat →     │
   │ operator_flagged │ │ allow-list +       │ │ local 70B / 200B │
   │ → local          │ │ pre-cloud scan     │ │                  │
   │                  │ │ Substance + post-  │ │                  │
   │                  │ │ assembly → local   │ │                  │
   └──────────────────┘ └────────────────────┘ └──────────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │  Heavy-Judge swap (200B,     │
                  │  on-demand): ALWAYS local;   │
                  │  pre-loaded at white-glove   │
                  │  (F-CLASS-HEAVY-JUDGE-CLOUD- │
                  │  DOWNLOAD fail-closes any    │
                  │  network fetch attempt)      │
                  └──────────────────────────────┘
```

**Sixteen F-CLASS-* gate primitives** under v7.0.10 LOCK: ten legitimate-runtime primitives from v7.0.7 §5.1; two repurposed defense-in-depth (`F-CLASS-SLOT-ID-NON-OPAQUE` + `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED`, broadened regex `\[SLOT_[^\]]*\]`, firing = bug or attack); four new at v7.0.10 (`F-CLASS-POSTURE-MID-CYCLE-CHANGE` + `F-CLASS-SPLIT-CONTEXT-ALLOWLIST` + `F-CLASS-SPLIT-CONTEXT-LEAK` + `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD`). F-CLASS-COVERAGE-INCOMPLETE is a META PRE-cycle gate — its scope expands to the sixteen primitives and prevents Beta deployment if any required module or test is missing from the runtime tree.

> *Historical note.* A fourth "Sanitized" posture (cloud Scribe drafting against `[SLOT_<numeric_id>]` tokens with a local slot-fill agent rendering post-fill drafts) was deprecated at v7.0.10 LOCK. Its enforcement gates remain live as defense-in-depth — no legitimate code path emits slot tokens into cloud prompts under any current posture; either gate firing is a bug-or-attack signal.

## Classification Register + Classification Review

The classification register is the load-bearing primitive that operationalizes the sovereignty story. Per-fact / per-class sensitivity tags (Public, Shareable, Confidential, Operator-flagged) are populated during a named **Classification Review** stage — between Intake (KFR ingestion at client onboarding) and the first grant cycle:

1. Inventory — the Golden Quill white-glove team presents the operator with what data Intake has gathered, organized by Card-archetype default classifications.
2. Operator override pass — operator reviews each classification, confirms or overrides per field.
3. Routing simulation — operator sees what the routing pattern would look like for a typical / representative grant cycle.
4. Test cycle — real or representative grant runs through the full pipeline with classification active. Operator validates that routing matches their sovereignty expectations.
5. Operator sign-off — classification register Ed25519-signed. Customer ships.

Classification Review is mandatory for v0.1 Beta deployments. A Beta deployment without an operator-signed classification register cannot ship — fail-closed by design.

**Three-layer classification defaults**: Card-level archetype defaults → operator overrides at white-glove → per-grant SP0 overrides. Lower layers override higher layers. No HARD-LOCKED postures at the Card level — classification register handles per-client sensitivity case-by-case.

## Signed Router-Template Updates

Golden Quill maintains the router-template release line as the model landscape changes. Each customer's router.yaml is a per-deployment config derived from the current signed template plus the operator's classification register.

- Soft commitment — continuous evaluation; ships router updates as warranted
- Quarterly review at minimum
- 7-day emergency updates for meaningful upgrades (new frontier-class open-weight release, substantially better cost/quality cloud frontier)
- Operator opt-in per update — deployments don't auto-update; operator pins or takes

**Router-template integrity (per §6.1 of v7.0.7):** every router-template release is signed with Ed25519 (per A12 crypto-agility envelope). The Golden Quill verifies the signature against the white-glove-pinned publisher public key BEFORE applying any update — failure → fail-closed: deployment stays on the previous pinned version, admin-risk ledger entry HIGH severity, operator notified. Public-key rotation requires the new key co-signed by the previous (Trust-On-First-Use rotation, audited). F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID PRE-gate enforces.

## Pipeline Track Registry (§5 v8 LOCKED 2026-05-10)

Tilth dispatches every pipeline cycle through a track registry keyed on `track_id`. The dispatcher does not branch on hard-coded modes — it looks up the requested track in the registry and refuses at runtime if the track is not shippable in the current release.

| Track | State | Shipped in | What it does |
|-------|-------|------------|--------------|
| `submission_mode` | ACTIVE | v0.1 Beta | Drafting + package assembly + operator-staged submit |
| `eval_mode` | ACTIVE | v0.1 Beta | Judge + Red Team scoring on existing drafts |
| `report_mode` | FORWARD-COMPAT (refused at runtime) | v0.2 | Post-award Data Collector → Report Generator track. Refuses with `F-PIPE-TRACK-NOT-SHIPPABLE` until WS-J §14 LOCK flips `shippable_in: v0.2` to `true`. |

Six §7 invariants enforce track-registry discipline (§7.16–§7.21): track-frozen at boot, registry shape integrity, dispatcher fall-through to runtime-rebind sentinel, grandfathered-runner bounded, `{org_slug}` required in every track path, lexicographic compare documented. Three runtime failure codes — `F-PIPE-TRACK-NOT-FOUND` / `F-PIPE-TRACK-NOT-SHIPPABLE` / `F-PIPE-TRACK-SHAPE-UNIMPLEMENTED` — fail-closed any call against an unknown / un-shipped / partially-implemented track.

When v0.2 ships, the dispatcher does not need re-edit. The registry row gets updated; the dispatcher reads the new state. R.PF1 commitment honored.

## Operational Data Sub-Kinds (§2 v7.2 LOCKED 2026-05-10)

The Vault stores seven distinct operational data sub-kinds, each with its own schema, Cedar policy, and round-trip discipline. PII discipline lives at the schema layer plus Cedar defense-in-depth.

| Sub-kind | Schema | PII discipline |
|----------|--------|----------------|
| `metrics` | quantitative measurements with units + period | — |
| `financials` | currency Decimal values (no float; F-FINANCIAL-CURRENCY-FLOAT fail-closes) | — |
| `photos` | image references with EXIF stripping | location-stripping at ingest |
| `narrative_entries` | qualitative text with provenance | — |
| `timeline` | dated events with milestone tags | — |
| `beneficiary_records` | individual demographic data | consent_capture required; `F-CEDAR-PII-CONSENT-MISSING` fail-closes write without operator-confirmed consent record |
| `attachments` | binary files with content-hash | — |

Cedar enforces a three-rule cross-product matrix per sub-kind (`F-CEDAR-OPERATIONAL-DENIED` / `F-CEDAR-PII-CONSENT-MISSING` / `F-CEDAR-SCHEMA-INVALID` / `F-CEDAR-ORG-MISMATCH`). Sub-kinds are operator-curated at white-glove onboarding for which channels collect each kind; Data Collector at v0.2 reads the configuration to route inbound data correctly.

## Key Facts Register (KFR) (v7.0.4 + v7.0.4-M1 LOCKED 2026-05-10)

The Key Facts Register is the per-org quantitative substrate. Every fact carries verbatim-quote-with-page provenance, an operator confirmation, an `as_of` date, and an SP0 freshness signature (per-grant override permitted, classified `confidential`).

- **F-LOGICIAN-FACT-DRIFT** family — facts referenced in drafts are checked against the KFR at every cycle; stale facts fail-closed.
- **AWARD_INGEST** — at award acceptance, the system extracts the operator-approved proposal's commitments into `proposal_commitments.yaml`, content-hash-bound to the submitted proposal. This is the substrate Report Generator (v0.2) reads against.
- **Canonical signature** — KFR signatures are computed over canonicalized bytes (YAML anchor / merge-key resolution applied first; `F-KFR-CANONICAL-SIGNATURE-INVALID` supersedes the prior `F-KFR-SIGNATURE-INVALID` per v7.0.4-M1).

## Hardware Stack

| Tier | Target | RAM | Safety Margin |
|------|--------|-----|---------------|
| Pro | GB10 Grace Blackwell class (NVIDIA DGX Spark, Lenovo ThinkStation PGX, other GB10 OEMs as released) | 128 GB+ | 5% |
| Baseline | Apple Mac Studio (M3 Ultra current; M5 Ultra targets 256 / 512 GB unified memory on release) | 128 GB+ | 10% |
| Dev | Apple Mac Mini (M1) | 8 GB | 20% |

Production floor: 128 GB unified memory. Section-aware pipeline windowing with machine-tier calibration ensures the pipeline adapts to available resources. If it runs on 8 GB, it flies on 128 GB.

**Phase One commercial target: Pro tier (GB10 Grace Blackwell class).** Baseline and Dev tiers are engineering-supported targets — not Phase One commercial deployments.

## Sovereignty Model

- **BYOK only.** Client owns all API keys. No managed edition, no metered billing.
- **Headless.** No UI in v0.1. Pipeline is CLI/agent-driven.
- **Local-first, BYOK, explicit approved routes.** Confidential and Operator-flagged data stay local. Public + Shareable content may use approved cloud routes only when the classification register allows it, under operator-owned keys and audit logging.
- **Crypto-agility.** Generic `OperatorSignature` dataclass with algorithm parameter — never hardcoded. v0.2 path: hybrid Ed25519 + ML-DSA-65 (NIST FIPS 204, post-quantum). v0.3: pure post-quantum after fleet-wide key rotation.

## Cycle-close accounting (§17 WPFA, LOCKED 2026-05-11)

At every cycle close, Tilth emits a `CycleReceipt` — a typed Pydantic artifact that proves what the inference path actually consumed (dollars + watt-hours), what 100% routing to the publisher-signed quarterly cloud baseline would have consumed, and the regenerative-savings delta. Every claim links to the published Coefficient Registry version, the cycle_id, and the Logfire trace_ids. Operator Ed25519 attestation gates buyer-facing PDF emission; M13 cannot bypass the attestation boundary.

```
Logfire span tree   Coefficient Registry (publisher signed)   Classification register
        │                       │                                  │
        └────────► Cycle Accountant (always-local, deterministic) ◄┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
       orgs/<slug>/vault/   operator           buyer-facing
       operational/         dashboard          PDF (operator-
       cycle_receipts/      (Cowork HTML)      attested only)
       <cycle_id>.json
```

A12 Decimal mandate extends to energy (`int` micro-watt-hours, never `float`). 12 F-WPFA-* failure codes (10 modules; predicate bodies LIVE at LOCK — the first §4 amendment family with LIVE bodies) enforce the trust floor. Sibling-not-nested with the forthcoming Reflection Packet: both consume the same Logfire span tree, but share zero output, consumer, or schema.

Trust mechanism for the Coefficient Registry mirrors v7.0.7 §6.1 router-template byte-for-byte: the publisher releases it quarterly; operator pins the publisher pubkey at white-glove onboarding; Ed25519 verification fail-closes the deployment on prior version if a published update does not verify against the pinned key. Rollback is operator-direct with audit-ledger entry.

## Substrate

Locked for v0.1. See [ADR-001](decisions/ADR-001.md) for rationale.

- **Orchestration + structured output:** Pydantic AI (multi-model seat invocation, type-safe I/O, schema enforcement — replaces both LangGraph and OpenClaw with less code)
- **Observability:** Logfire (Pydantic-native tracing and metrics)
- **Local inference:** Ollama or vLLM (OpenAI-compatible endpoint)
- **Offline refinement:** DSPy + GEPA (Card refinement, Library development only)

## Cycle-close artifacts (sibling-not-nested)

Two typed Pydantic artifacts emit at every grant cycle close. They consume the same Logfire span tree but have **zero shared output, zero shared consumer, zero shared schema field, and zero F-* code crossing** — sibling-not-nested at every architectural layer.

```
                    ┌─────────────────────────────────────────┐
                    │       Logfire span tree (cycle close)   │
                    └────────────────┬────────────────────────┘
                                     │ shared input substrate only
                          ┌──────────┴───────────┐
                          ▼                      ▼
              ┌─────────────────────┐   ┌──────────────────────────┐
              │ WPFA CycleReceipt   │   │ Reflection Packet         │
              │ (§17 v1 LOCKED)     │   │ (§16 v1 LOCKED 2026-05-15)│
              │ rows 205-208        │   │ rows 216-218              │
              ├─────────────────────┤   ├──────────────────────────┤
              │ Producer:           │   │ Producer:                │
              │ Cycle Accountant    │   │ archivist.               │
              │ (deterministic;     │   │ reflection_submode       │
              │ no LLM)             │   │ (v7.0.9 row 202)         │
              ├─────────────────────┤   ├──────────────────────────┤
              │ Consumer:           │   │ Consumers (3):           │
              │ Operator dashboard  │   │ A — Operator review CLI  │
              │ + buyer-facing PDF  │   │ B — KFR cross-check      │
              │                     │   │ C — v1.x scheduled       │
              │                     │   │     Archivist            │
              ├─────────────────────┤   ├──────────────────────────┤
              │ Audience:           │   │ Audience:                │
              │ Operator + external │   │ Tilth-internal only      │
              │ buyer (sales lever) │   │                          │
              ├─────────────────────┤   ├──────────────────────────┤
              │ Gate family:        │   │ Gate family:             │
              │ F-WPFA-*            │   │ F-PACKET-*               │
              │ (12 codes; LIVE     │   │ (19 codes; 18            │
              │ bodies at LOCK)     │   │ NotImplementedError +    │
              │                     │   │ 1 LIVE META at v0.1 hook)│
              └──────┬──────────────┘   └────────┬─────────────────┘
                     │                            │
                     └──── 1 sibling cross-ref ───┘
              F-WPFA-SPAN-PROVENANCE-MISSING ↔ F-PACKET-SPAN-PROVENANCE-MISSING
              (sibling pattern only; NOT composition; NOT shared module)
```

**Path B naming discipline** (per `pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md`):
- `F-PACKET-*` gates the Reflection Packet artifact (§16; this LOCK).
- `F-REFLECTION-*` gates the producer's behavior (§4 v2.x.2 row 203; v7.0.9).
- `F-ARCHIVIST-*` gates the substrate write (§15 v1).
- `F-WPFA-*` gates the sibling artifact (§17 v1; §4 v2.x.z).
Four orthogonal F-* families. AST-lint enforces no cross-family imports at module-import time. F-PACKET-* and F-WPFA-* are both EXCLUDED from the F-CLASS-COVERAGE-INCOMPLETE META gate (OQ-6-style isolation precedent).

**v0.1 hook DORMANT scope for Reflection Packet** — schema authored but SUB_KIND_REGISTRY entry deferred to v0.2 first wave; 18 of 19 F-PACKET-* predicates raise `NotImplementedError`; one (`F-PACKET-COVERAGE-INCOMPLETE`) carries LIVE META-gate body as dormant-binding lever. v0.2 first wave compound LOCK flips bodies + registers sub-kind + strengthens META-gate to dry-run probe.

## Product Arc

Stage 1: Solo operator (v0.1, current — LOCKED) → Stage 2: Small team (multi-Cultivator seats, one Tilth) → Stage 3: Cooperative org → Stage 4: Contractor federation → Stage 5: Sovereign Node commons online (cooperative-owned compute, opt-in cross-Tilth research at member-set consent tiers). *(Naming updated 2026-05-06: the Stage-5 commons formerly called "MaatAI" is now "Sovereign Node" — no LLC suffix. Current operating legal entity is FIT Farms LLC; Golden Quill is its project until any future spin-off.)*

Stages 2-5 are future scope. v0.1 is the foundation that makes everything else possible.
