# White-Glove Onboarding Playbook — v0.1 Beta

**Scope:** Operator-facing procedure for a v0.1 Beta deployment. Covers Classification Review, deployment-posture selection, AWARD_INGEST, classification register seeding, and first grant cycle dispatch.
**Authority:** Architecture v7.0.7 (Beta classification-driven routing) + **v7.0.10 LOCKED 2026-05-11** (three-posture routing model — Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign; supersedes the v7.0.7 four-posture-implicit framing) + §11 Intake v1 (BULK_INGEST + INCREMENTAL_INGEST + AWARD_INGEST) + §12 Uploader v1 (prepare-and-stage, four portal adapters).
**Filed:** 2026-05-10; posture-vocabulary refresh 2026-05-15. Pairs with `pipeline/planning/v0_1_beta_readiness_2026-05-10.md`.

A Beta deployment without an operator-signed classification register cannot ship. The F-CLASS register and routing gates fail-close the first cycle. This playbook is the procedure that gets the register signed.

## 0. Pre-arrival checklist (Golden Quill / FIT Farms side)

Before the white-glove team arrives at the operator's site:

- Hardware delivered: 128 GB Golden Quill provisioned with Golden Image (frozen substrate per ADR-001).
- Operator's BYOK envelope confirmed: Anthropic + Groq + Google + OpenAI keys, all operator-owned.
- Operator's per-deployment `router.yaml` derived from the current Golden Quill router-template release + signed with the pinned router-template publisher Ed25519 key. Golden Quill is pinned with the publisher public key at boot.
- Operator's Ed25519 keypair generated on the Golden Quill itself (private key never leaves the box). Public key is what signs every register from this point forward.
- `vault_shared/funder_intelligence/` is seeded with the launch corpus (USDA VAPG program page, NSF general program info, named foundation 990-PFs, etc.). Per v7.0.5 LOCK.

The operator now has a Golden Quill that boots, runs Tilth, and refuses any cycle until Classification Review completes.

## 1. Intake BULK_INGEST

**Mode:** Intake `BULK_INGEST`. Runs once at white-glove onboarding.

**Operator input:** organization documents — strategic plans, last three years of grant applications, board minutes, audited financials, IRS Form 990, deeds, leases, MOUs, beneficiary aggregate data, photos, narrative essays, project plans. Anything the operator has.

**What Intake does:**

1. Reads every uploaded document. Substrate dispatch per file format (PDF unique-page-match + DOCX paragraph-index + Markdown single-line + XLSX cell reference, per §11 Intake v1 + v7.0.4-M1 §4.2).
2. Extracts candidate facts to the Key Facts Register (KFR). Each candidate carries verbatim-quote-with-page provenance: the literal extracted text, the source file, the page or paragraph or row reference, the SHA3-512 of the canonicalized source bytes, and the extractor confidence.
3. Surfaces every candidate to the operator one at a time. **Operator confirms each fact** before it lands in the KFR. No silent ingestion. No fabrication (F-EXTRACTOR-FABRICATION fail-closes any candidate that cannot be substrate-verified).
4. Tags each fact with a draft classification per Card-archetype defaults (Card-level defaults are advisory, not HARD-LOCKED). Operator can override at any time and will revisit every classification in step 2.
5. Writes facts to `orgs/<operator_slug>/vault/key_facts_register/` with content-hash binding.

**Time estimate:** 4–8 hours for an organization with ~150 documents. White-glove team and operator work side-by-side; this is not unattended.

**Done condition:** every operator-confirmed fact has a KFR entry. Operator signs the KFR bootstrap with their Ed25519 key. The auto-promote four-layer defense (TTY check + Cedar policy + AST-lint + runtime guard) refuses to advance to step 2 without a signed bootstrap.

## 2. Classification Review

**Authority:** v7.0.7 §3 + §3.6 + §3.7. Mandatory for v0.1 Beta deployments.

The classification register is the load-bearing primitive that operationalizes the sovereignty story. Per-fact / per-class sensitivity tags drive routing decisions on every agent call.

### 2.1 Four per-field classes (per v7.0.7 §2)

| Class | What it means | Where it routes (composes with posture per §2.1.bis) |
|-------|---------------|-----------------|
| `public` | Information already publicly disclosed by the operator or compelled by law (state-filed annual reports, 990s, posted strategic plan, public website copy) | Cloud frontier admissible under Frontier-Eligible; restricted to allow-list payloads only under Split-Context Hybrid; always local under Local-Only |
| `shareable` | Information the operator would willingly send to a peer organization or grant reviewer (programmatic descriptions, named partnerships, named board members) | Cloud frontier admissible under Frontier-Eligible; restricted to allow-list payloads only under Split-Context Hybrid; always local under Local-Only |
| `confidential` | Information the operator does not want any cloud provider to ever see (annual revenue, EIN, UEI, SAM banking info, beneficiary PII, donor-restricted financials, internal disputes, attorney correspondence) | Always local; composed into drafts by local seats — never routed cloud under any posture (operator override requires per-grant SP0 + HIGH-severity admin-risk ledger entry) |
| `operator_flagged` | Operator-defined "I don't trust this one yet" tag — case-by-case sensitive content that defaults to confidential routing until operator re-classifies | Always local |

A new fact ingested via Intake INCREMENTAL after onboarding defaults to `confidential` until the operator re-classifies (`F-CLASS-NEW-FACT-UNCLASSIFIED` fail-closes any cloud-routed call that touches it).

### 2.1.bis Three deployment postures (per v7.0.10 LOCKED 2026-05-11)

The four per-field classes compose with **one operator-selected deployment posture** chosen at step 3 below. The posture sets the deployment's stance toward cloud routing; the per-field classes set what content is eligible to flow where under that posture.

| Posture | What it means | What stays on the operator's Golden Quill |
|---------|---------------|------------------------------------------|
| **Frontier-Eligible** | Customer permits selected project data to route to external/frontier models under BYOK. Tilth assigns the strongest available model to each role per benchmark fit. | Confidential + operator_flagged fields. Operator override → per-grant SP0 + HIGH-severity admin-risk ledger entry. |
| **Split-Context Hybrid** | Frontier models help with structure, section strategy, prompts, funder-language framing, and generic draft scaffolds — operating only on an operator-signed allow-list (RFA text + funder agency name + funder rubric + program template name + section structure + KGIE keywords + dialect classification). | All applicant-specific substance. Confidential + operator_flagged fields. Editor / Red Team / routine-Judge on the assembled draft. *No opaque-slot round-trip.* |
| **Local-Only / Sovereign** | Every Tilth seat runs on the local 70B-class stack with on-demand 200B-class heavy-Judge swap. Maximum-custody posture. **Performance-dependent / under validation** until proven against real grant workloads. | Everything. No cloud routing at all. |

The Local-Only / Sovereign posture carries an explicit under-validation caveat in v0.1 Beta deployments. The per-deployment manifest field `local_only_validated: bool` (default `false`; write-protected; flips only on SN-LLC quarterly validation outcome signature) gates "production-validated" claims on any customer-facing artifact. Customers selecting Local-Only at white-glove see this caveat in their Classification Review test cycle output and can run the representative-grant test cycle end-to-end on local-stack-only routing before signing off.

> *Historical note.* A fourth "Sanitized" posture (cloud Scribe drafting against opaque `[SLOT_<numeric_id>]` tokens with a local slot-fill agent rendering post-fill drafts) was deprecated at v7.0.10 LOCK. The two enforcement gates (`F-CLASS-SLOT-ID-NON-OPAQUE` + `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED`) remain live as defense-in-depth — no legitimate code path emits slot tokens into cloud prompts under any current posture; either gate firing is a bug-or-attack signal.

### 2.2 The review procedure

1. **Inventory.** White-glove team presents the operator with what Intake has gathered, organized by Card-archetype default classification. Operator sees the full data picture in one view.
2. **Operator override pass.** Operator reviews each classification, confirms or overrides per field. Examples the operator should expect:
   - Annual revenue, EIN, UEI, SAM banking → typically `confidential`.
   - Mission statement, programmatic descriptions → typically `public` or `shareable`.
   - Beneficiary aggregate counts → typically `shareable`; individual demographic records → typically `confidential` and only with consent_capture.
   - Strategic plan PDF (public-website-hosted) → `public`; same plan with handwritten internal margin notes → `confidential`.
3. **Routing simulation + posture selection (v7.0.10).** The CLI presents the three posture options (Frontier-Eligible / Split-Context Hybrid / Local-Only / Sovereign) with one-paragraph descriptions and a side-by-side routing-simulation summary for a representative grant cycle:
   - *Frontier-Eligible:* Scribe Phase 0 RFA extraction → cloud frontier (public RFA text); Scribe Phase 2 drafting → cloud frontier for Public + Shareable sections; Confidential-bearing sections drafted locally; Editor / Red Team / Judge → cloud where input is non-Confidential, local 70B for post-substance drafts.
   - *Split-Context Hybrid:* Scribe scaffold composition → cloud frontier reading the RFA + section structure + dialect keywords only (no applicant facts); Scribe substance composition → local 70B; Editor / Red Team / Judge → local 70B.
   - *Local-Only / Sovereign:* Every seat → local 70B; heavy-Judge swap to 200B for federal long-form RFAs. **Performance-dependent / under validation** notice surfaced inline.
   Operator selects the deployment posture at step 3 *before* the test cycle runs.
4. **Test cycle.** A real or representative grant runs through the full pipeline under the operator-selected posture. Operator validates that routing matches their sovereignty expectations. If something feels wrong, the operator overrides the classification of the offending fact OR re-selects the posture and re-runs.
5. **Operator sign-off.** Classification register Ed25519-signed with operator's keypair; the signature attests to **both** per-field classifications **and** the selected posture (`selected_posture` field added at top level per v7.0.10 §1.4). The signed register becomes the input to every subsequent cycle. `F-CLASS-REGISTER-UNSIGNED` (sub-tag `.posture_unsigned`), `F-CLASS-REGISTER-SIGNATURE-INVALID` (sub-tag `.posture_invalid`), and `F-CLASS-REGISTER-HASH-MISMATCH` (sub-tag `.posture_hash_mismatch`) fail-close any cycle that runs without a valid signature over both surfaces.

### 2.3 What the operator should not be surprised by

- **No HARD-LOCKED postures at the Card level.** The Card defaults are advisory. The operator's overrides are authoritative.
- **No opaque slot tokens in cloud prompts under any v7.0.10 posture.** The earlier mechanism whereby cloud-routed Scribe drafts contained `[SLOT_<numeric_id>]` tokens at Confidential field positions (and a local slot-fill agent rendered the post-fill draft after cloud Scribe returned) is **deprecated entirely**. Under Frontier-Eligible, Confidential-bearing sections are drafted locally end-to-end and cloud frontier only sees Public + Shareable content; under Split-Context Hybrid, cloud sees only the operator-signed allow-list payload (RFA + structural template + dialect keywords). The two enforcement gates (`F-CLASS-SLOT-ID-NON-OPAQUE` + `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED`) remain live as defense-in-depth — firing = bug or attack.
- **Substance vs. structure under Split-Context Hybrid.** Cloud sees the funder's RFA + structural template + dialect keywords + KGIE-checklist keywords. Cloud does not see the applicant's legal name, EIN, address, KFR production-metric numerics, or partnership names. `F-CLASS-SPLIT-CONTEXT-ALLOWLIST` PRE-gate fail-closes any payload whose field-paths fall outside the operator-signed allow-list; `F-CLASS-SPLIT-CONTEXT-LEAK` PRE-gate fail-closes any applicant-fact match in the allowed payload.
- **Posture cannot change mid-cycle.** Re-selecting posture post-onboarding requires a per-deployment SP0-equivalent flow (`tilth posture select`). Posture changes within an open cycle window are fail-closed by `F-CLASS-POSTURE-MID-CYCLE-CHANGE`; changes take effect at the next cycle's start.
- **High-stakes flag is itself confidential.** If the operator flags a grant cycle as high-stakes (federal long-form, large award, sensitive politics), the heavy-Judge swap fires for that cycle. The flag itself stays in `grant_overrides` and never appears in cloud payloads. `F-CLASS-HIGH-STAKES-FLAG-LEAK` fail-closes any cloud payload that references it.
- **Heavy-Judge swap never reaches the network.** The 200B-class heavy-Judge model binary is pre-loaded on the Golden Quill at white-glove (Golden-Image-build-time-signed manifest). `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD` fail-closes any heavy-Judge swap that would trigger a network fetch — missing binary, manifest hash mismatch, operator override to fetch from remote URL, or any background model-sync daemon attempting binary update outside the operator-attested router-template flow.

### 2.4 Sign-off artifact

The signed classification register is stored at the canonical gate-checked path `orgs/<operator_slug>/vault/classification/register.yaml` with the operator's Ed25519 signature appended. The signature includes timestamp, register hash, and operator public key fingerprint. Per-grant SP0 overrides chain to this signature.

## 3. First grant cycle dispatch

After Classification Review sign-off, the first cycle is the operational dry run.

### 3.1 Cycle structure

1. **Scout DISCOVER + VERIFY** — Scout runs the two-stage discovery against six parallel channel families (federal APIs, cached datasets, state/foundation portals, federal program pages, RSS watchlists, client-material-driven web search, plus Channel G against the seeded `vault_shared/funder_intelligence/` corpus). Live synopsis fetch verifies any candidate before it reaches the operator. Local-routable; zero API cost.
2. **Scribe draft** — Scribe drafts section-by-section under the operator-selected posture. Under Frontier-Eligible, Public + Shareable sections route cloud per the current signed router template; Confidential-bearing sections are drafted locally end-to-end. Under Split-Context Hybrid, Scribe's scaffold composition routes cloud against the operator-signed allow-list (RFA + section structure + dialect keywords only) and substance composition routes local; the final draft is assembled via deterministic merge with no opaque-slot round-trip. Under Local-Only / Sovereign, every Scribe call routes local.
3. **Editor / Judge / Red Team review** — On any draft carrying Confidential-bearing substance (the common case under Frontier-Eligible + every case under Split-Context Hybrid), Editor / Red Team / routine-Judge route local 70B-class. Under Local-Only / Sovereign, every review seat routes local regardless of class. For high-stakes grants, the heavy-Judge swap fires under any posture — a 200B-class model **pre-loaded on the Golden Quill at white-glove** is loaded from NVMe for the cycle (2–5 minute wall load), runs the Judge pass, then unloads. No network fetch at swap time. Cross-family rigor is enforced: no seat shares model family with the seat that authored the work it reviews.
4. **Council split tie-breaker** — Judge / Red Team disagreement of 10+ points triggers a council split. The operator decides.
5. **Operator approval** — operator reviews the draft, requests revisions, approves.
6. **Uploader stages the submission package** — Uploader runs in `submission_mode` track. Assembles the operator-approved draft into the funder-portal-required formats. Four portal adapters at v0.1: Grants.gov Workspace, SAM.gov, Common Grant Application, copy-paste fallback (Foundant / Submittable / Fluxx are Path-b scope). Attachments deferred to v1.1.
7. **Operator clicks final submit on the funder portal.** Uploader is prepare-and-stage discipline only — `F-UPLOADER-AUTOSUBMIT-ATTEMPTED` fail-closes any submission package that bypasses the operator's manual final-submit click (no M13 escape valve; architecturally prohibited).

### 3.2 Pre-cycle gate ordering

The Logician fires PRE-cycle gates in this order before any Scout call leaves the box:

1. `F-CLASS-COVERAGE-INCOMPLETE` — the required F-CLASS-* enforcement modules and tests are incomplete or missing from the runtime tree.
2. `F-CLASS-REGISTER-SIGNATURE-INVALID` — register signature verifies against operator's pinned public key.
3. `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` — current router.yaml signature verifies against the pinned router-template publisher public key.
4. `F-KFR-CANONICAL-SIGNATURE-INVALID` — KFR signature verifies over canonicalized bytes.
5. `F-PIPE-TRACK-NOT-SHIPPABLE` — requested track is in the registry and `shippable_in: v0.1`.
6. Track-shape gates per requested track (`submission_mode` or `eval_mode` at v0.1 Beta).

Any failure here halts the cycle and surfaces an actionable error to the operator. No silent failure mode.

### 3.3 What the operator does in their first cycle

- Picks one grant to run end-to-end. White-glove team is present.
- Watches the routing decision on every agent call. Verifies cloud routing only happens consistent with the operator-selected posture: under Frontier-Eligible, cloud only on Public + Shareable input; under Split-Context Hybrid, cloud only on the operator-signed allow-list payload; under Local-Only / Sovereign, no cloud routing at all.
- Reviews Scribe's draft. Sees Editor's clarity flags + replacement options. Sees Judge's score against the funder's own rubric. Sees Red Team's adversarial probe. Sees Logician's PRE/POST results.
- Approves a final draft. Watches Uploader assemble the submission package. Opens the funder portal. Clicks final submit.

The cycle is recorded in the audit trail with full provenance: every fact citation, every routing decision, every signed register state. The operator can answer "where did this number come from?" for every claim in the proposal.

## 4. AWARD_INGEST (post-award)

When the operator wins a grant, the system runs Intake `AWARD_INGEST` once.

**What it does:**

1. Reads the operator-approved final proposal (the one Uploader staged + the one that won).
2. Extracts the proposal's commitments — every promised deliverable, every promised SMART outcome, every promised milestone, every promised data point.
3. Writes `proposal_commitments.yaml` content-hash-bound to the submitted proposal. The hash binding is the audit anchor: any future Report Generator (v0.2) call against this commitment is verifiable against the exact submitted bytes.
4. Surfaces every commitment to the operator for confirmation. **Operator confirms each commitment** before it becomes a reporting obligation. No silent expansion of scope (Law 2).
5. Adds the commitments to the per-grant `grant_overrides` for the duration of the grant period.

This is the substrate Report Generator reads against at v0.2. At v0.1 Beta, AWARD_INGEST runs and writes the substrate; the operator can manually reference it for their own reporting workflow until v0.2's `report_mode` track ships.

**When AWARD_INGEST does not run:** if the operator does not win the grant, AWARD_INGEST does not fire. The submitted proposal is retained in the audit trail as a historical artifact.

## 5. Between-cycle: INCREMENTAL_INGEST + lessons

Between grant cycles, the operator may add new facts (a new partnership, a new board member, a new funded program, an updated audited financial). Intake `INCREMENTAL_INGEST` handles these.

- Same provenance discipline as BULK_INGEST: verbatim-quote-with-page, operator confirmation per fact.
- **New facts default to `confidential`** until the operator re-classifies. `F-CLASS-NEW-FACT-UNCLASSIFIED` fail-closes any cloud-routed call that touches an unclassified fact.
- Operator runs a mini-Classification Review on the new facts as part of confirmation. Single-fact, fast.

The Archivist (v1.x horizon) curates lessons across cycles — patterns of what worked, what didn't, what to pre-check on future cycles. At v1.x, Archivist proposes lessons; it never applies them automatically (proposes-only AST assertions structurally enforced per §15 v1 SPEC). At v0.1 Beta, the lessons file is operator-curated.

## 6. What can go wrong + operator-actionable recovery

| Failure | What it means | Operator action |
|---------|---------------|-----------------|
| `F-CLASS-COVERAGE-INCOMPLETE` | Required F-CLASS-* enforcement modules/tests are missing from the runtime tree | Deployment does not proceed; engineering restores the missing gate/test coverage before any grant cycle runs |
| `F-CLASS-REGISTER-SIGNATURE-INVALID` | Register has been tampered with OR operator key was rotated without re-signing | Operator re-signs the register on the Golden Quill |
| `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` | A router-template update does not verify against the pinned publisher public key, or the operator's pinned key is stale | Deployment stays on prior pinned version; operator decides whether to rotate to a new publisher key per Trust-On-First-Use rotation discipline |
| `F-EXTRACTOR-FABRICATION` | An Intake candidate could not be substrate-verified back to source bytes | Operator reviews the source document manually; if the fact is real, operator confirms manually with a new substrate reference |
| `F-PIPE-TRACK-NOT-SHIPPABLE` | Operator requested `report_mode` track at v0.1 Beta | Track is v0.2-only; operator can manually run reporting workflow against `proposal_commitments.yaml` until v0.2 ships |
| `F-UPLOADER-AUTOSUBMIT-ATTEMPTED` | Submission package was generated with an auto-submit path — this is a code-side bug, not an operator error | Filed as HIGH-severity admin-risk ledger entry; Golden Quill/FIT Farms investigates |
| `F-CLASS-HIGH-STAKES-FLAG-LEAK` | Heavy-Judge swap flag leaked into a cloud payload — code-side bug | Filed as HIGH-severity admin-risk ledger entry; cycle halts pending Golden Quill/FIT Farms fix |
| `F-CLASS-POSTURE-MID-CYCLE-CHANGE` | Operator attempted to re-select deployment posture mid-cycle | Cycle continues under the posture locked at cycle start; new posture takes effect at the next cycle's start (operator uses `tilth posture select` between cycles) |
| `F-CLASS-SPLIT-CONTEXT-ALLOWLIST` | Under Split-Context Hybrid, a cloud-routed prompt contained a field-path outside the operator-signed allow-list | Cycle halts; operator reviews the prompt payload and either extends the allow-list (dual-signed) or marks the field as substance routing |
| `F-CLASS-SPLIT-CONTEXT-LEAK` | Under Split-Context Hybrid, the applicant-fact scan detected legal-name / EIN / address / partnership name in a Public + Shareable payload | Cycle halts; operator reviews the offending fact (likely embedded in RFA-keywords or template); HIGH-severity admin-risk ledger entry |
| `F-CLASS-HEAVY-JUDGE-CLOUD-DOWNLOAD` | Heavy-Judge swap attempted a network fetch — model binary missing from pinned local path, hash mismatch, or background daemon update attempt | Filed as HIGH-severity admin-risk ledger entry; cycle halts; engineering re-pins the Golden Image manifest |
| `F-CLASS-SLOT-ID-NON-OPAQUE` / `F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED` | A `[SLOT_*]` token was emitted into a cloud-routed prompt or detected on a cloud response. **No legitimate code path under v7.0.10 emits these tokens** — firing means bug, regression, or attempted prompt injection | Filed as HIGH-severity admin-risk ledger entry; cycle halts pending engineering review |

Every fail-closed event is recorded in the per-grant audit trail with timestamp, gate name, predicate inputs (redacted per classification), and recovery action taken.

## 7. Closing — the sovereignty promise made concrete

White-glove onboarding is where the sovereignty story stops being abstract and starts being a procedure the operator runs on hardware they own. By the end of this playbook, the operator has:

- A Golden Quill they physically own, with a Golden Image they did not have to assemble.
- A Key Facts Register populated only with facts they confirmed, each with verbatim-quote-with-page provenance.
- A classification register they signed with their own Ed25519 key, after seeing exactly what the routing pattern does on a representative cycle.
- A first grant cycle in their audit trail with full provenance, full routing transparency, and a submission that they (not the system) clicked final submit on.
- A clear v0.1 → v0.2 capability map so they know what ships when (and know that no scope-drift surprise will appear mid-deployment).

If FIT Farms LLC or any future Golden Quill spin-off disappeared tomorrow, the operator would still have their Golden Quill, their data, their keys, their grants, and the audit trail to prove it. Nothing held hostage. No customer content leaves silently; approved cloud routes are explicit, BYOK-backed, classification-allowed, and audit-recorded.

That is what v0.1 Beta ships.
