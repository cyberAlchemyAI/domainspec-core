---
title: Alpha Readiness Checklist — first paid Golden Quill deployment
authored: 2026-05-15
authored_by: Tilth core (Cowork session, opus 4.7)
audience: Josh (operator) + Paul (incoming platform engineer) — read together
register: operator-facing — honest, not marketing
status: living planning surface — no LOCK ceremony
supersedes: none (first Alpha-class checklist filed)
companions:
  - docs/white_glove_v0_1_beta.md             # customer-facing onboarding playbook
  - docs/platform_engineer_onboarding.md       # Paul's operations pack
  - docs/v0_1_TECHNICAL_LEAD_BRIEF.md          # technical-lead brief (outside-review artifact)
  - docs/lessons_memory_external_one_pager.md  # customer-facing Lessons Memory explainer
  - pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md  # active v0.1 clearance packet
  - pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md  # WPFA §17 v1 LOCKED 2026-05-11
  - pipeline/handoffs/ws_wpfa_code_phase_handoff_2026-05-11.md  # Code-phase dispatch packet
---

# Alpha Readiness Checklist — what stands between "v0.1 Beta cuts" and "first paid client deployed"

## 0. How to read this document

This is not a launch announcement. It is a punch list of everything that must be true before Golden Quill carries a paying client. It is honest about what is not yet ready, what has not yet been decided, and what cannot ship until SN-LLC (today resolved to FIT Farms LLC — see §1.3) publishes its inaugural Coefficient Registry.

Read it the way you would read a pre-flight checklist for a small aircraft: nothing here is optional, but most items are cheap once you know they exist. The expensive items — Coefficient Registry publication, operator key custody, contract surface — are flagged.

Josh and Paul should read this together once and decide who owns each row in §8. After that, this is Paul's daily driver alongside `docs/platform_engineer_onboarding.md` and `docs/platform_engineer_quick_reference.md`.

---

## 1. Alpha definition — what "Alpha" means here

### 1.1 The boundary

v0.1 Beta cuts is a milestone for the *code tree*: when the v0.1 Lock-and-Clear Packet's open gates close, the v0.1 substrate is "locked enough" that primary build attention moves to v0.2 (`pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md`). At that point the system is reproducible on Josh's M1 8 GB dev node with the focused smoke suite green and a sanitized replay packet in the repo.

Alpha is a separate milestone for the *deployment*: a real Golden Quill node, on a real customer's desk, running real customer data through the locked substrate, against a real BYOK envelope, with real money flowing through a real contract. v0.1 Beta cuts is a prerequisite. Alpha is what happens after.

### 1.2 The transition

```
v0.1 Beta cuts ───┐
                  ├──→ Alpha (first paid client deployed)
SN-LLC inaugural ─┤
Coefficient Registry
publication
```

Both prerequisites are non-negotiable. Without v0.1 Beta cuts, the substrate is not stable enough to hand a customer. Without an inaugural Coefficient Registry publication, the WPFA Cycle Accountant cannot emit a CycleReceipt — which means the buyer-facing PDF (the sales lever) cannot ship, which means there is no audit-grade artifact backing the "regenerative dividend" claim that the price tag is built around.

### 1.3 "SN-LLC" naming — disambiguation for this document

Per the operator's 2026-05-09 disambiguation pin in `MEMORY.md`, **SN-LLC does not legally exist today**. The only operating legal entity is FIT Farms LLC. "Sovereign Node" (no LLC) is the Stage-5 internal-only name for the cooperative-owned compute commons that will not exist until Stage 5.

For the Coefficient Registry publisher role (per WPFA §17 + §2 v7.4), "SN-LLC" is a *file-naming label* for the publisher role. Today the publisher role resolves to FIT Farms LLC. When the project spins out into a dedicated entity, the label can resolve to that new entity. Trust mechanism does not change: a single white-glove-pinned publisher Ed25519 pubkey verifies the registry release; the entity behind that key is what changes over time.

For this checklist, "SN-LLC publisher role" = "FIT Farms LLC acting as Coefficient Registry publisher" until further notice. Customer-facing copy says "FIT Farms"; internal file labels say "SN-LLC."

### 1.4 What Alpha is NOT

- Not Founding 12 cohort launch (that's the next twelve deployments, mid-July 2026 → mid-April 2027 per README §Roadmap).
- Not Stage-2 fleet (twelve Tilths under coordinated Law 3 isolation).
- Not multi-tenant.
- Not managed-edition or metered-billing.
- Not a marketing event. Alpha is the *first* paid deployment; the launch announcement attaches to Founding 12, not to Alpha-of-one.

---

## 2. SN-LLC inaugural Q3-2026 Coefficient Registry path

Per §17 v1 LOCK row 205 + the WPFA Code Phase handoff (`pipeline/handoffs/ws_wpfa_code_phase_handoff_2026-05-11.md`), the inaugural Coefficient Registry publication is what unblocks the buyer-facing PDF as a sales lever. Without it, every CycleReceipt fails `F-WPFA-COEFFICIENT-SIGNATURE-INVALID` at PRE-emission load.

### 2.1 What "publication" actually means

A Coefficient Registry release is a signed YAML asset at `vault_shared/wpfa/coefficient_registry/active.yaml` containing:

- Per-model coefficient entries (`dollars_per_million_input_tokens`, `dollars_per_million_output_tokens`, `watt_hours_per_token`, hardware SKU bindings).
- A `baseline_model_id` field — the quarter's flagship cloud baseline against which counterfactual savings are measured.
- A `baseline_quarter` tag (e.g., `Q3-2026`).
- An Ed25519 signature over the canonicalized bytes, by the publisher key.

The white-glove team pins the publisher public key on the customer Golden Quill at onboarding. Every subsequent registry release is signature-verified against that pinned key before any CycleReceipt loads it.

### 2.2 What has to ship for the inaugural publication

1. **Empirical coefficient measurements.** Per-model dollars-per-million-tokens (taken from current Anthropic / Groq / Google / OpenAI pricing pages, with a snapshot date). Per-model watt-hours-per-token — this is the harder one. Sources: Patterson et al. (Google) and Epoch AI energy estimates, with explicit methodology citation. The honest path is: cloud models = best public estimate with citation + uncertainty range; local models = bench-measured on the deployment hardware. Methodology must be defensible to a regenerative buyer's procurement team.
2. **Baseline-model decision.** Q3-2026's flagship baseline. Likely candidates: `claude-sonnet-4-6` or `claude-opus-4-6`. Operator decides. The choice gates the counterfactual size — picking the cheapest flagship inflates "savings"; picking the most expensive deflates them. Pick the one that's *honest* given that the customer would have routed there if they'd gone fully cloud-frontier.
3. **Publisher Ed25519 key generation.** The publisher key lives on whatever box does the registry releases. For Alpha, this is plausibly Josh's M1 — but the key must never leave that box, and the key must be auditable to "FIT Farms LLC acting in the publisher role." A signed attestation of who controls the key, on FIT Farms LLC letterhead, is the legal-paper companion to the cryptographic key.
4. **Registry canonicalization + signing tooling.** A small CLI: `tilth wpfa registry publish` reads the candidate YAML, canonicalizes, signs with the publisher key, writes `active.yaml` + signature sidecar, appends to a publication log. Per the Code Phase handoff this lands as `tilth wpfa registry update` + `tilth wpfa registry rollback` + `tilth wpfa registry pin-pubkey` argparse-level TTY-gated verbs.
5. **First-customer pinning ceremony.** White-glove team imports the publisher pubkey into the customer Golden Quill before the first cycle. Pubkey fingerprint goes into the customer's onboarding contract as an addendum so there is paper showing exactly which key the customer trusted.

### 2.3 Estimated work

- Empirical measurement + coefficient YAML drafting: 1–2 sessions (engineer-led; methodology citations to attach).
- Publisher key generation + key-custody attestation paper: 0.5 session (Paul + Josh together).
- Registry CLI ship: ~2 sessions per the WPFA Code Phase handoff.
- First-customer pinning ceremony rehearsal on Josh's M1 before first paid deployment: 0.5 session.

Total: ~4–5 sessions of work between v0.1 Beta cuts and the inaugural publication actually landing as a signed `active.yaml` on disk.

### 2.4 What this unblocks

- Buyer-facing PDF emission for any cycle that runs after the registry pin. Without registry, no PDF. Without PDF, no sales lever.
- Quarterly Coefficient Registry updates become the cadence — Q3-2026 inaugural → Q4-2026 rev1 → Q1-2027 rev2. Updates ship signed, customer opts in per release (no auto-update). Same trust mechanism as router-template signing.

---

## 3. Production-node deployment topology

Beyond Josh's M1 8 GB dev node, what does the first paying client's node look like?

### 3.1 Hardware

128 GB unified-memory floor is non-negotiable per the v7 LOCK. Three SKU choices that satisfy the floor:

- **Apple Mac Studio M3 Ultra, 128 GB.** Most predictable customer experience; Apple hardware stability is well-understood. Smallest learning curve for a customer who is not a Linux operator. Default recommendation for the first paid Alpha client.
- **NVIDIA DGX Spark / ASUS Ascent GX10.** GB10-class. Strongest local-model throughput. Better if the customer's posture leans `local-only-sovereign` (everything routes local) or expects heavy use of the 200B-class heavy-Judge swap.
- **AMD GX-10.** Same hardware tier; alternative supply path.

The Founding 12 commercial target is Pro tier GB10-class (per `docs/platform_engineer_onboarding.md` §4). For *Alpha-of-one* — first paid deployment as proof — pick whichever SKU the first paying client wants. The point is to ship the substrate against real hardware against a real customer, not to pre-decide the fleet shape.

### 3.2 Software substrate — Golden Image

Per ADR-001 (locked in v0.1, `pipeline/architecture/v0.1/adr_001_substrate.md`):

- Pydantic AI (orchestration + structured output)
- Logfire (observability — OpenTelemetry-compatible)
- Ollama (default) or vLLM (alt) — OpenAI-compatible local inference endpoint
- python-docx, openpyxl, pypdf wrapped as Pydantic AI tools
- DSPy + GEPA for offline Library refinement (does not run on the appliance at runtime)
- Logician deterministic Python + Cedar policy gates
- weasyprint (per WPFA Code Phase) for buyer-facing PDF rendering

Frozen at Golden Image build. No package-manager access from the appliance post-build. Updates ship as signed Golden Image rebuilds; the customer opts in per release.

### 3.3 Routing posture — three choices

Per architecture v7.0.7 (`pipeline/architecture/v0.1/architecture_v7_0_7_locked.md`), the customer picks one of three postures at white-glove. The choice is the customer's, made visible during Classification Review:

- **Frontier-Eligible** — most facts `public`/`shareable`; almost all calls route to cloud frontier. Lightest local-model footprint. Fastest, cheapest, best quality at draft time. Fits customers whose data is already FOIA-able (public agency, school district).
- **Split-Context Hybrid** — mix of `public+shareable` and `confidential+operator_flagged`. Cloud for the first; local 70B for the second; on-demand 200B heavy-Judge swap for high-stakes grants. Default for most customers. "Power for drafting + privacy for review."
- **Local-Only-Sovereign** — nothing leaves the box. All seats route local. No cloud keys configured. For customers with strict data-residency requirements.

For the first paid Alpha, the *most likely* posture is Split-Context Hybrid — it stresses the most code paths in production for the first time and produces the most useful WPFA receipt (a savings claim against a fully-cloud counterfactual). Frontier-Eligible would understate the savings story; Local-Only-Sovereign would dodge half the code paths.

### 3.4 Customer onboarding kit

What the white-glove team ships with the Golden Quill on day-of-arrival:

- The Golden Quill itself, factory-fresh Golden Image installed.
- Pinned publisher public keys: (a) router-template publisher pubkey, (b) WPFA Coefficient Registry publisher pubkey. Fingerprints printed on the contract addendum.
- A USB key with the customer's BYOK envelope template (empty), to be filled in during the onboarding session.
- The white-glove playbook (`docs/white_glove_v0_1_beta.md`) in printed + digital form.
- The Lessons Memory one-pager (`docs/lessons_memory_external_one_pager.md`) in printed form — for the customer to read between sessions.
- The customer's CIC card preselection (Food Systems / Educator / Public Agency / Arts & Culture / Cooperative / Ecosystem Intermediary) per Josh's pre-onboarding intake conversation. The CIC card configures Search Vocabulary / Evidence Schema / Language Register / Reporting Rhythm — but does NOT pre-bind capital logic (CIC × CLC orthogonality is structural).

### 3.5 Network posture

Per the v0.1 Lock-and-Clear Packet §Safe Public Language, the appliance is **local-first + BYOK + explicit approved cloud routes**. Not "no cloud dependency," not "nothing phones home" — those are claims the appliance does not yet enforce at the OS/firewall layer.

What the customer's network needs to look like:

- The appliance reaches the internet for: Anthropic / Groq / Google / OpenAI BYOK endpoints; Grants.gov + SAM.gov + USASpending for Scout VERIFY; Logfire ingestion endpoint; the Golden Image update channel (signed releases only).
- Egress is recorded in the audit trail; every cloud route is `classification_register` + `router_template` + `cycle_id` + `trace_id` traceable.
- No inbound from the public internet. The appliance is not a server.
- If the customer wants OS-enforced "Sovereign mode" (firewall + namespace isolation + cloud-route allow-list at the kernel), that's a v0.2 deliverable. At Alpha it's customer-network-policy-enforced; the public language must match.

---

## 4. BYOK envelope for the first client

The first client provisions their own keys before the first cycle runs. Tilth never holds keys. The keyring loader at `pipeline/orchestrator/keyring_loader.py` reads from an operator-provided keystore that never leaves the appliance.

### 4.1 v0.1 BYOK accounts the client must provision

| Provider | Why | Who signs up | Notes |
|---|---|---|---|
| Anthropic | Scribe primary (cloud-routable when input is `public+shareable`) | Customer | Console at console.anthropic.com; usage tier 1 acceptable at Alpha |
| Groq | Editor / Red Team / Scout fallback (cloud-routable when input is `public+shareable`) | Customer | console.groq.com; the $20/mo dev tier is sufficient at Alpha cadence |
| Google (Gemini API) | Judge primary (cloud-routable when input is `public+shareable`) | Customer | aistudio.google.com or Vertex; Gemini 2.5 Pro is the current Judge default |
| OpenAI | Red Team escalation / fallback | Customer | platform.openai.com; optional at Alpha, recommended for Red Team disagreement edge cases |
| Logfire (Pydantic-hosted) | Observability ingest | Customer | logfire.pydantic.dev; OpenTelemetry-compatible, so the customer can re-export to their own stack later if they want |

All five provisioned per the customer's own billing relationship. FIT Farms LLC does not see invoices for any of these. The customer can audit usage on each provider's own dashboard.

### 4.2 v0.2 BYOK envelope (not Alpha blockers)

The following are v0.2-only — Data Collector and Cultivator channel substrates. If the first paid client wants pre-award-only services, none of these apply at Alpha:

- Postmark or SendGrid or Mailgun — email channel
- Twilio — SMS + voice
- Telegram Bot API (MTProto) — Telegram channel + Cultivator interface
- WhatsApp Business API — WhatsApp channel

If the first paid client wants post-award reporting at deployment time, that's a v0.2 conversation — not an Alpha v0.1 deliverable. Be honest about this in the sales conversation: at Alpha, what ships is the submission workstation, not the post-award reporting system.

### 4.3 Per-provider sign-up walkthrough

A standalone document at `docs/byok_signup_walkthrough.md` (NOT yet authored — pre-staged) walks the customer through the five v0.1 accounts in plain language: where to sign up, what tier to pick, where to find the API key after sign-up, how to import it into the keystore. Estimated 3–4 pages. ~1 session to author. Should be authored by the white-glove team in collaboration with Paul before the first paid Alpha.

### 4.4 Key rotation + custody

- Each customer key is operator-owned. Customer rotates on whatever cadence they want.
- Tilth's keyring loader does not log keys, does not write keys to disk outside the keystore, does not include keys in audit payloads.
- If the customer rotates a key, they update the keystore; the next cycle picks up the new value. No restart required for most providers.
- If the customer wants to revoke FIT Farms entirely (Alpha-extreme case: customer wants to operate the Golden Quill standalone), every key is theirs; FIT Farms has nothing to hand back. That is what the sovereignty promise means in practice.

---

## 5. Customer-facing materials index

### 5.1 What already exists

- **`docs/white_glove_v0_1_beta.md`** — Operator-facing onboarding playbook. Covers Intake BULK_INGEST + Classification Review + first cycle dispatch + AWARD_INGEST + INCREMENTAL_INGEST. Good as-is for the first paid Alpha. Filed 2026-05-10, updated for the Classification Review wrapper landing.
- **`docs/lessons_memory_external_one_pager.md`** — Customer-facing explainer for Lessons Memory. Honest framing about what self-improvement features in AI systems do wrong, and why Tilth's proposes-only discipline is different. Good for handing to a customer between onboarding sessions.
- **`docs/GETTING_STARTED.md`** — Operator orientation. Mostly developer-facing today; may need a customer-facing re-cut before Alpha (open question).
- **`README.md`** — Project root. Customer-discoverable. Already says local-first/BYOK/approved-cloud-route per the v0.1 Lock-and-Clear claim grep.

### 5.2 What is still needed

| Document | Audience | Status | Estimated effort |
|---|---|---|---|
| Client onboarding pack (cover letter + welcome packet + day-of-arrival agenda) | Customer | NOT-STARTED | 1 session |
| First-cycle expectations document ("what to expect in your first grant cycle") | Customer | NOT-STARTED | 1 session |
| "What changes when you click Submit" plain-language guide | Customer | NOT-STARTED | 0.5 session |
| Billing + contracting touchpoints (invoice cadence, payment terms, refund policy, contract addendum template) | Customer | NOT-STARTED | 1 session — needs operator + accountant + lawyer alignment first |
| SLA expectations (uptime, response time, escalation path, security incident notification) | Customer | NOT-STARTED | 1 session — needs Paul on-board to author |
| Support contact protocol (how to reach Paul + Josh + the white-glove team, what each path is for) | Customer | NOT-STARTED | 0.5 session |
| BYOK sign-up walkthrough (§4.3 above) | Customer | NOT-STARTED | 1 session |
| Audit-trail explainer ("how to read your audit log" — for the customer's compliance team) | Customer compliance officer | NOT-STARTED | 1 session |
| Crypto-key custody addendum template (publisher pubkey fingerprints, operator key generation procedure) | Customer + customer counsel | NOT-STARTED | 1 session — Paul + legal counsel review |
| Termination / off-boarding procedure ("what happens if you stop being a customer") | Customer | NOT-STARTED | 0.5 session — load-bearing for the sovereignty promise |

Total customer-facing authoring backlog: ~8–10 sessions. Mostly low-cost paper work, but Paul should author the SLA + key custody pieces because they reflect his operational shape.

### 5.3 Authoring principles

- Operator-voice. Not marketing copy. Not "delight." Not "magic." Plain English.
- Honest about what doesn't ship at v0.1 (no post-award reporting until v0.2; no Cultivator phone interface; no OS-firewall-enforced Sovereign mode).
- Honest about Manual-vs-Automated. White-glove onboarding is *manual* — Josh + Paul + the customer at a table. The audit trail is explicit. Manual hidden inside claims of automation is not acceptable.
- Cross-reference internal docs by path. Customer doesn't need to read them, but the customer's compliance counsel might want to.

---

## 6. Legal + compliance pre-flight

For the first paid deployment with real customer data, the following must be in writing before the contract signs.

### 6.1 PII discipline — beneficiary records

Per §2 v7.2 LOCK + Cedar PII enforcement, the `beneficiary_records` sub-kind has special read-path discipline: Cedar policy + `__post_init__` schema invariants on both directions. Confidential PII never appears in cloud-routed prompts (`F-CLASS-SLOT-ID-NON-OPAQUE` + `F-CLASS-HIGH-STAKES-FLAG-LEAK` + `F-WPFA-PDF-CONFIDENTIAL-LEAK`).

What this means for the contract: the customer warrants that beneficiary data is collected with appropriate consent, and Tilth warrants that the data does not leave the appliance except via classification-allowed routes that the customer has approved during Classification Review. State-specific PII regimes (CCPA, NYSHIELD, others as relevant to the customer's beneficiaries) are the customer's responsibility; Tilth does not provide legal advice. The contract addendum should say this explicitly.

### 6.2 TCPA + CAN-SPAM — Data Collector

At Alpha (v0.1 only), Data Collector does NOT run. No SMS, no voice, no email outreach. So TCPA + CAN-SPAM are not Alpha contract surface — they're v0.2 conversations. If the customer wants post-award outreach at Alpha-time, defer to v0.2 explicitly; do not promise.

When v0.2 ships:
- TCPA discipline is enforced via `consent_ledger` + `state_rules_card` + per-recipient channel-bound shared-secret tokens (§13 v1 LOCK).
- CAN-SPAM is enforced via Cedar dispatcher signature + AST-lint `R-DATACOLLECTOR-NO-AUTOSEND` + TTY check.
- The four-layer autosend defense is structural, not policy.
- The customer remains the legal addresser; Tilth is the substrate.

### 6.3 Crypto key custody

Three sets of keys exist by Alpha:

- **Publisher keys (FIT Farms LLC, acting in SN-LLC publisher role).** Router-template publisher pubkey + WPFA Coefficient Registry publisher pubkey. Generated on Josh's M1; kept on Josh's M1; rotated per Trust-On-First-Use rotation discipline (new pubkey co-signed by previous). Fingerprints printed on customer contract addendum.
- **Operator keys (customer).** Operator Ed25519 keypair generated on the customer Golden Quill itself; private key never leaves the box. Used to sign: classification register, KFR bootstrap, AWARD_INGEST acceptance, WPFA CycleReceipt (when the customer wants a buyer-facing PDF). Key rotation is the customer's call.
- **Logfire ingest key (customer BYOK).** Customer-owned; no special custody beyond §4.

The contract addendum should specify:
- Both publisher key fingerprints + which entity controls each.
- That operator keys are generated on the customer's box and that FIT Farms LLC does not have a copy. (This is the sovereignty promise made legally explicit.)
- The rotation procedure for publisher keys + customer-facing notification cadence.
- The crypto-agility envelope at A12: Ed25519 today; hybrid Ed25519+ML-DSA-65 at v0.2; pure post-quantum at v0.3. The customer's box will accept signed Golden Image upgrades to extend the envelope, but does not have to rotate to v0.2 or v0.3 hybrid until the customer chooses to.

### 6.4 Coefficient Registry trust model — buyer-facing PDF

When the customer signs a CycleReceipt and emits a buyer-facing PDF, the receipt cryptographically commits to:

- The active Coefficient Registry version (`coefficients_registry_version` SHA3-512 hex hash + Ed25519 signature).
- The classification register version at cycle start.
- The set of Logfire trace IDs covered.

This means the buyer (e.g., a board reviewing the customer's grant report, a foundation reviewing the customer's regenerative-dividend claim) can in principle audit the receipt against the Coefficient Registry's publication log. The publication log lives at FIT Farms LLC; access for buyer audit is on a request basis. Procedure for buyer-audit requests should be documented in `docs/buyer_audit_procedure.md` (NOT yet authored, pre-staged) before the first paid Alpha customer signs.

### 6.5 Liability + indemnification

These are conversations with FIT Farms LLC's counsel, not for this checklist to resolve. Items to flag with counsel before the first paid contract:

- What does FIT Farms LLC warrant about Tilth's behavior? (Reasonable: "the substrate ships with the documented gate behavior + the audit trail enables the customer to verify"; not-reasonable: "no false positives ever.")
- What is the customer's recourse if a Logician gate fails-closed during a critical submission window? (Reasonable: prompt support response + audit-trail forensics; not-reasonable: missed-deadline indemnity.)
- What does the customer warrant about their own data? (Standard: data they upload was lawfully collected.)
- Force-majeure on cloud provider outages (Anthropic / Groq / Google / OpenAI). The Local-Only-Sovereign posture is the architectural answer; customers in that posture are unaffected. Split-Context Hybrid customers may degrade to local-only-fallback during cloud outage — discipline already exists per v7.0.7 §F-CLASS-ROUTING-INDETERMINATE → local fail-closed.

### 6.6 Audit trail retention

Every cycle generates: Scout candidate roster, RFA snapshot, Scribe drafts (per-section), Editor / Judge / Red Team artifacts, Logician audit log, Uploader staged package, AWARD_INGEST commitments (if won), WPFA CycleReceipt. Plus Logfire spans for the cycle.

Retention is the customer's decision. The default per `pipeline/blueprint/` is "retain indefinitely on the appliance." Practical answer: appliance has plenty of disk (NVMe is the default Golden Image substrate), and audit-trail compression is cheap. The customer's compliance team may have its own retention requirements; the contract should defer to those.

---

## 7. Operational handoff to Paul

Paul is the incoming platform / ops engineer. His onboarding pack is `docs/platform_engineer_onboarding.md` (~30 KB, comprehensive). This section is the *Alpha-specific overlay* on his onboarding: what Paul owns specifically for the first paid deployment.

### 7.1 Day-1 responsibilities

- Read `docs/platform_engineer_onboarding.md` end-to-end. Bookmark `docs/platform_engineer_quick_reference.md` if it exists; if not, author it (1 session).
- Run the v0.1 smoke suite per `pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md` §v0.1 Smoke Test Bar. Confirm 339-passing baseline. Confirm AST-lint clean.
- Read `pipeline/engineering/lock_history.v1.jsonl` from row 178 forward (today's LOCK count) to understand the architectural-change cadence of the last month.
- Tail the last two `daily_logs/*.md` files for operational context.
- Set up Logfire ingest for Paul's own observability box (separate from any customer ingest); validate that Logfire spans render correctly across a synthetic dry-run cycle on Josh's M1.

### 7.2 Week-1 responsibilities

- Author or co-author the customer-facing docs backlog in §5.2 — at least the SLA expectations document, the support contact protocol, the key-custody addendum template, and the BYOK sign-up walkthrough.
- Build the sanitized replay packet per `docs/v0_1_TECHNICAL_LEAD_BRIEF.md` §First Engineer Tasks #2. This is the v0.1 clearance artifact and the first reproducible run packet that an outside engineer can replay.
- Run the SN-LLC inaugural Coefficient Registry publication ceremony rehearsal on Josh's M1 (per §2.3 above). Validate: registry signs cleanly; pinning ceremony works; WPFA cycle-close emits a CycleReceipt that signature-verifies.
- Confirm `docs/v0_1_TECHNICAL_LEAD_BRIEF.md` is accurate. Edit where it's drifted.
- Identify what observability the first paid customer needs (Logfire is the default; the customer may want a re-export path to their own stack — Grafana Tempo / Honeycomb / Datadog / etc.). Document any export plumbing.

### 7.3 Month-1 responsibilities

- Own the customer-facing Alpha deployment end-to-end alongside Josh. The expectation is that Paul drives the technical setup; Josh drives the customer relationship + grant-strategy + Classification Review walk-through.
- Build the day-of-arrival checklist (deploy.md / customer_deployment_runbook.md). What gets unboxed, plugged in, set up, validated on day 1. Estimated 1 session to author + 1 session to rehearse on Josh's M1.
- Establish the on-call / support cadence with the customer. Initial proposal: business-hours-only, 24h response SLA for non-critical, 4h response for any Logician gate fail-closed event blocking a submission deadline. Adjust per customer needs.
- Lead the first cycle's WPFA receipt emission for the customer. Walk the customer through the receipt: what it says, what it commits to, where the Coefficient Registry came from, how to read the buyer-facing PDF. The first receipt is the first time the regenerative-dividend story becomes audit-grade for a paying client; it deserves attention.

### 7.4 Boundaries

- Paul does NOT touch the LOCK ceremony cadence — that's Josh + the Thesis dispatch pattern. Paul observes; if Paul wants to author a LOCK candidate, that's a separate workflow.
- Paul does NOT change architecture in v0.1 — substrate is frozen per ADR-001. Bug fixes against locked specs go through the standard narrow-corrective-amendment pattern (e.g., §11 v1.1, §4 v2.x.1, v7.0.4-M1).
- Paul does NOT make customer-facing promises that aren't in the white-glove playbook or this checklist. If a customer asks something that isn't covered, Paul logs the question + escalates to Josh.
- M13 (audited bypass) is operator-only. Paul does not invoke M13; if a gate fails-closed and the customer needs to ship, Paul surfaces the situation to Josh for the bypass decision.

---

## 8. Pre-flight checklist — every item that must be true before Alpha cuts

| # | Item | Owner | Status (2026-05-15) | Unblockers |
|---|---|---|---|---|
| 1 | v0.1 Beta cuts (per Lock-and-Clear Packet §Move-To-v0.2 Rule) | Josh | IN-FLIGHT | one reproducible submission-mode replay packet exists; smoke suite green; live language clean |
| 2 | Reproducible submission-mode replay packet in the repo | Paul (sanitized version of Dogwood-shape run) | NOT-STARTED | Paul on-boarded; sanitization rules agreed |
| 3 | v0.1 smoke suite stays green across all post-Beta-cut commits | Paul | IN-FLIGHT (339/339 PASS recorded 2026-05-11) | CI cadence (Paul to set up) |
| 4 | WPFA Code phase landed (predicate bodies LIVE, orchestrator wired, weasyprint substrate, CLI verbs, dashboard, Cedar bootstrap, indirect-template-data scan, Logfire export canonicalization, end-to-end synthetic emission test green) | Cowork Code-phase sessions | NOT-STARTED (handoff pre-staged at `pipeline/handoffs/ws_wpfa_code_phase_handoff_2026-05-11.md`) | ~2-3 sessions per the handoff |
| 5 | SN-LLC (FIT Farms LLC) inaugural Coefficient Registry Q3-2026 published + signed + auditable | Josh + Paul | NOT-STARTED | empirical coefficient measurements; baseline-model decision; publisher key generation; registry CLI ship (item 4); key-custody attestation paper |
| 6 | Publisher Ed25519 keypair generated; fingerprint documented for customer contract addendum | Josh | NOT-STARTED | item 4 (CLI verbs ready) |
| 7 | Router-template publisher Ed25519 keypair generated; fingerprint documented for customer contract addendum | Josh | LIKELY DONE (per architecture v7.0.7 §6.1 trust mechanism) — verify on-disk before Alpha | confirm on disk |
| 8 | First paid Alpha client identified | Josh | NOT-STARTED (deliberately deferred per Law 3 + sales cycle) | sales conversations |
| 9 | First Alpha client's CIC card preselected | Josh + client | NOT-STARTED | item 8 |
| 10 | First Alpha client's hardware SKU selected (Mac Studio M3 Ultra / DGX Spark / GX-10) | Josh + client | NOT-STARTED | item 8 |
| 11 | First Alpha client's BYOK envelope provisioned (Anthropic + Groq + Google + OpenAI + Logfire accounts) | client | NOT-STARTED | item 8; BYOK sign-up walkthrough (§4.3) |
| 12 | BYOK sign-up walkthrough document authored | Paul + white-glove team | NOT-STARTED | ~1 session |
| 13 | Customer onboarding pack (cover letter / welcome / day-of-arrival agenda) authored | Paul + Josh | NOT-STARTED | ~1 session |
| 14 | First-cycle expectations document authored | Paul + Josh | NOT-STARTED | ~1 session |
| 15 | "What changes when you click Submit" guide authored | Paul | NOT-STARTED | ~0.5 session |
| 16 | SLA expectations document authored | Paul | NOT-STARTED | ~1 session |
| 17 | Support contact protocol authored | Paul | NOT-STARTED | ~0.5 session |
| 18 | Audit-trail explainer authored | Paul | NOT-STARTED | ~1 session |
| 19 | Crypto-key custody addendum template authored + counsel-reviewed | Paul + Josh + counsel | NOT-STARTED | ~1 session + counsel review |
| 20 | Termination / off-boarding procedure documented | Paul + Josh | NOT-STARTED | ~0.5 session |
| 21 | Buyer-audit procedure for Coefficient Registry documented | Paul | NOT-STARTED | ~0.5 session |
| 22 | Contract template + addendums drafted (entity = FIT Farms LLC; product = Golden Quill) | Josh + counsel | NOT-STARTED | counsel engagement |
| 23 | Liability / indemnification language reviewed (§6.5) | Josh + counsel | NOT-STARTED | counsel engagement |
| 24 | Billing + payment infrastructure live (invoice cadence, payment terms, accounting setup) | Josh + accountant | NOT-STARTED | accountant engagement |
| 25 | Day-of-arrival deployment runbook authored | Paul | NOT-STARTED | ~1 session |
| 26 | Day-of-arrival runbook rehearsed end-to-end on Josh's M1 with synthetic customer | Paul + Josh | NOT-STARTED | item 25 |
| 27 | First-cycle WPFA receipt emission rehearsed end-to-end on Josh's M1 | Paul + Josh | NOT-STARTED | items 4 + 5 |
| 28 | OS-level "Sovereign mode" (firewall + namespace + egress allow-list) — DEFERRED to v0.2 per Lock-and-Clear Safe Public Language; public language must match | n/a | DEFERRED | document deferral in contract |
| 29 | Logfire ingest configured + verified for Paul's own observability | Paul | NOT-STARTED | item 1 |
| 30 | claim grep clean across README + docs + website assets before first paid contract signs | Paul | IN-FLIGHT (per Lock-and-Clear DONE for live docs 2026-05-11) | re-run before contract sign |

DONE-criteria for "Alpha ready": every NOT-STARTED row above is DONE or DEFERRED-with-customer-acknowledgement; v0.1 Beta cuts (item 1) is DONE; the inaugural Coefficient Registry (item 5) is published.

Estimated work between today (2026-05-15) and Alpha-ready: 12–15 Cowork sessions of doc + ceremony work + 4–5 sessions of WPFA Code phase + sales-cycle time on item 8 (out-of-band). Items 22, 23, 24 require counsel + accountant time and are likely the longest critical-path items.

---

## 9. Stage-1 → Stage-5 forward path — what Alpha enables

Per the dispatch plan §7 watch list + the README §Roadmap:

- **Stage 1 — Solo operator.** Today. v0.1 Beta is the substrate. Alpha is the proof. *We are here.*
- **Stage 2 — Twelve Tilths (Founding 12).** Mid-July 2026 → mid-April 2027. Twelve Pittsburgh-area Founder Node deployments across the six CICs. Phase One productizes the founder-led methodology into a repeatable Golden Image + deployment playbook + paid expert review of the launch Capital Logic Cards. Unit-economics proof for wider rollout.
- **Stage 3 — Cooperative org.** Post-Founding 12. Multiple orgs share hardware-tier infrastructure; Law 3 isolation extended to cooperative shared-hardware boundary. v2 multi-tenant amendment opens here. Items currently bounded-by-A1+A4 (`pipeline/architecture/v0.1/section_o_5_v2_known_limitations.md`) get re-opened as work.
- **Stage 4 — Contractor federation.** Independent operators, each own Golden Quill, selective shared posture. Federation discipline; cross-Tilth signal sharing on opt-in.
- **Stage 5 — Sovereign Node commons online.** The cooperative-owned compute commons (today internally named "Sovereign Node" — no LLC yet; future entity to be formed). Cross-Tilth network effect engages per consent tier. Tagline: "A cooperative of member-owners, sharing only what they choose, on the terms they set."

### 9.1 What v2 multi-tenant work Alpha unblocks

Alpha is the first stress test on the v0.1 single-client assumption (A1) + operator-trusted assumption (A4). What it reveals about real customer behavior bounds the v2 multi-tenant amendment scope. Things to watch during the first paid Alpha:

- How does a real customer use the heavy-Judge swap? (Bounded-by-A1+A4 timing side-channel becomes a real defense surface when multiple customers share infrastructure.)
- How does a real customer use the AST-lint discipline? (Dynamic-call evasion class becomes a real defense surface when the runtime tree is shared.)
- How does the watcher TOCTOU on Intake INCREMENTAL behave under realistic customer file cadence?
- Per-channel rate-limit handling — does the single-customer Scout rate-limit posture hold up under real Grants.gov / SAM.gov usage?

These observations become input to the v2 multi-tenant amendment Thesis when Stage 3 work opens. The current `pipeline/architecture/v0.1/section_o_5_v2_known_limitations.md` register is the placeholder for that future Thesis.

### 9.2 What Alpha does NOT enable

- Founding 12 cohort launch — that's a separate cohort-readiness packet (not authored, pre-staged for a future session when Alpha is closer to running).
- Stage-2 Sovereign Node commons — not until Stage 5 by definition.
- v0.2 post-award reporting — separate v0.2 lane per the Lock-and-Clear v0.2 First Target.

Alpha is the proof point. Founding 12 is the cohort. Stages 3–5 are the org-shape evolution. They are sequential, not concurrent, and that ordering should hold in any sales conversation about timelines.

---

## 10. Pointer index — every relevant artifact

### 10.1 LOCKed amendments (v0.1)

- `pipeline/architecture/v0.1/tilth_architecture_locked.md` — v7 LOCKED 2026-04-19 (A1–A12). The architectural floor.
- `pipeline/architecture/v0.1/architecture_v7_0_4_locked.md` + `_M1_amendment.md` — KFR substrate + Decimal mandate.
- `pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md` — Funder Intel DB + Match DB + Scout channel G + Stage-5 consent on-ramp.
- `pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md` — Classification-driven routing + Classification Review stage + heavy-Judge swap + per-deployment router.yaml + 12 F-CLASS-* primitives.
- `pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md` — CIC × CLC orthogonality structural enforcement.
- `pipeline/architecture/v0.1/section_o_5_v2_known_limitations.md` — Bounded-by-A1+A4 register for v2 multi-tenant Thesis.

### 10.2 LOCKed blueprints (v0.1)

- `pipeline/blueprint/v0.1/section_02_v7_2_amendment.md` — Operational-data sub-kinds (LOCKED rows 186/187).
- `pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md` — Coefficient Registry signed-asset class (LOCKED row 206).
- `pipeline/blueprint/v0.1/section_04_v2_x_amendment.md` + `_v2_x_1_amendment.md` + `_v2_x_z_wpfa_amendment.md` — Logician failure-code families.
- `pipeline/blueprint/v0.1/section_05_v8_amendment.md` — Track registry (submission_mode ACTIVE, eval_mode ACTIVE, report_mode FORWARD-COMPAT v0.2).
- `pipeline/blueprint/v0.1/section_11_intake.md` + `_v1_1_amendment.md` — Intake three-mode dispatch.
- `pipeline/blueprint/v0.1/section_12_uploader.md` — Uploader prepare-and-stage + four portal adapters.
- `pipeline/blueprint/v0.1/section_15_archivist.md` — Archivist proposes-only SPEC (runtime deferred to v1.x).
- `pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md` — WPFA Cycle Accountant (LOCKED 2026-05-11).
- `pipeline/blueprint/v0.1/section_0_5_interface_index.md` — runtime-live interface ledger (470 rows + rising).

### 10.3 v0.2 horizon blueprints (SPEC LOCKED)

- `pipeline/blueprint/v0.1/section_13_data_collector.md` — Data Collector 5-channel SPEC.
- `pipeline/blueprint/v0.1/section_14_report_generator.md` — Report Generator track-mode SPEC (Slice 2 landed 2026-05-11; Slice 3 pre-staged).

### 10.4 Active planning artifacts

- `pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md` — **active v0.1 clearance packet** (supersedes 2026-05-10 readiness + posture docs).
- `pipeline/planning/v0_2_dispatch_plan_2026-05-09.md` — 14-workstream v0.2 dispatch plan.
- `pipeline/planning/watts_per_funding_action_spec_2026-05-10.md` — WPFA spec card + Thesis input.
- `pipeline/planning/funding_goal_amendment_spec_2026-05-10.md` — FundingGoal v0.2 SPEC.

### 10.5 Active handoffs

- `pipeline/handoffs/ws_wpfa_code_phase_handoff_2026-05-11.md` — WPFA Code phase (predicate-body finalization + orchestrator wiring + buyer-PDF substrate + CLI verbs + dashboard + Cedar bootstrap).
- `pipeline/handoffs/` (folder) — other v0.2-lane handoffs.

### 10.6 Customer-facing materials

- `docs/white_glove_v0_1_beta.md` — operator-facing onboarding playbook.
- `docs/lessons_memory_external_one_pager.md` — customer-facing Lessons Memory explainer.
- `docs/v0_1_TECHNICAL_LEAD_BRIEF.md` — technical-lead brief (outside-review artifact).
- `docs/GETTING_STARTED.md` — operator orientation (developer-facing today).
- `README.md` — project root (customer-discoverable; claim-grep-clean per 2026-05-11).

### 10.7 Operations-facing materials

- `docs/platform_engineer_onboarding.md` — Paul's comprehensive operations pack.
- `docs/platform_engineer_quick_reference.md` — Paul's 1-page daily driver (companion to onboarding pack).
- `docs/ARCHITECTURE_OVERVIEW.md` — engineering architectural overview.
- `docs/GIT_WORKFLOW.md` — git discipline.
- `docs/decisions/ADR-001.md` — v0.1 substrate decision record.

### 10.8 Operational ledgers

- `pipeline/engineering/lock_history.v1.jsonl` — append-only architectural-change ledger (214 rows).
- `daily_logs/YYYY-MM-DD.md` — operational-change ledger (per-day).
- `pipeline/metrics/session_log.jsonl` — session-metrics ledger.
- `pipeline/institutional_memory/lessons.json` + `lessons.md` — mandatory pre-check lessons (L-001 through L-018+).

### 10.9 Memory + identity

- `MEMORY.md` — user-memory index.
- `SOUL.md` — operating principles (Five Laws, Four Rules).
- `USER.md` — operator identity + decision framework.
- `AGENTS.md` — agent wake-up + invocation rules.
- `router.yaml` — model bindings (sole source).
- `lessons.md` — mandatory pre-checks.
- `CLAUDE.md` — Cowork-specific supplement (this conversation's project context).

### 10.10 Validation audit trails

- `pipeline/validation/wpfa_thesis_2026-05-10/` — WPFA §17 v1 LOCK audit trail.
- `pipeline/validation/v7_0_5_thesis_2026-05-09/` — Architecture v7.0.5 LOCK audit trail (cross-family bridge-pattern reference).
- Other `pipeline/validation/<topic>_thesis_<date>/` folders — per-LOCK audit trails.

---

## 11. Honest closing — what is NOT yet ready

For the avoidance of doubt, here is the punch list of items that are NOT yet ready for Alpha, in priority order:

1. **v0.1 Beta cuts** — the substrate prerequisite. One reproducible replay packet stands between today and "v0.1 clear" per the Lock-and-Clear Packet.
2. **WPFA Code phase** — predicate bodies are LIVE at LOCK; orchestrator wiring, buyer-PDF substrate, CLI verbs, dashboard, Cedar bootstrap are NOT YET in the runtime. 2–3 sessions of work per the handoff packet.
3. **Inaugural Coefficient Registry** — coefficient measurements not yet taken; baseline-model decision not yet made; publisher key not yet generated; key-custody attestation paper not yet written.
4. **Customer-facing materials** — ~10 documents in §5.2 are NOT-STARTED.
5. **Contract + legal infrastructure** — contract template, addendums, liability language all NOT-STARTED; counsel not engaged.
6. **Billing + payment infrastructure** — accountant not engaged.
7. **Paul's onboarding** — pack exists; Paul has not yet been onboarded against it.
8. **First paid Alpha client** — not yet identified.

None of these is a blocker individually. Sequenced realistically: Paul onboards while WPFA Code phase ships. Coefficient Registry inaugural ceremony rehearses on Josh's M1 once items 2 + 3 land. Customer-facing docs and legal infrastructure run in parallel during the sales cycle for item 8. Day-of-arrival deployment rehearsal completes the loop before the first contract signs.

Realistic Alpha-ready window: **August–October 2026** (best case), given:
- Item 1 closes within the next ~2 weeks at current cadence.
- Items 2 + 3 close within ~4 weeks of item 1.
- Items 4 + 5 + 6 close within 4–6 weeks of Paul on-boarding (item 7).
- Item 8 is sales-cycle-dependent; cannot be force-scheduled.

That window puts Alpha in front of Founding 12 launch (mid-July 2026 target per README) — which is the right ordering: Alpha-of-one proves the deployment shape before twelve simultaneous deployments stress the same shape. If Alpha slips past mid-July, the Founding 12 calendar slips with it. Don't pretend otherwise in any sales conversation.

This is the punch list. Work it.

---

**Filed:** 2026-05-15. Living document. Update as items in §8 flip status. Re-author the cohort-readiness packet when Alpha is closer to running.
