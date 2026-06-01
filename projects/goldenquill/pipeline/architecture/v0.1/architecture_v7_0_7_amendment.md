---
title: Tilth Architecture — Amendment v7.0.7 (Beta model strategy — classification-driven routing, white-glove Classification Review stage, on-demand heavy local Judge, Sovereign Node LLC continuous best-of-breed routing)
filed: 2026-05-08
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-10 — substantive architectural addition (classification register as load-bearing primitive + new Classification Review stage + heavy-Judge on-demand swap + per-deployment router.yaml derivation + twelve F-CLASS-* failure-code primitives at architectural layer). Audit #1 cleared 2026-05-09 (11 findings → 8 author edits). Audit #2 split verdict 2026-05-10: Editor READY_TO_LOCK + Judge READY_TO_LOCK (score 96/100, up from 67) + Red Team NEEDS_THIRD_ROUND on F-GPTOSS-005 (high-stakes-flag handling + heavy-Judge swap timing side-channel). Per L-005 architecture-domain disagreement branch: operator + synthesis-tier disposition produced rev3 narrow-fix (§4.1 mechanism-level + §4.2 v0.1-known-limitation-with-v0.2-extension-marker). Operator confirmed Path C-LOCK 2026-05-10. LOCKED. Twelfth F-CLASS-* primitive (F-CLASS-HIGH-STAKES-FLAG-LEAK) added at narrow-fix.
parent_lock: pipeline/architecture/v0.1/tilth_architecture_locked.md
parent_amendment: pipeline/architecture/v0.1/architecture_v7_0_3_amendment.md
companion_amendment: pipeline/architecture/v0.1/architecture_v7_0_6_amendment.md (roster — v7.0.7 references seat names from v7.0.6)
companion_files_pending_edit:
  - "Golden Quill Business Plan v10 4.docx (Appendix D + Hardware Budget Table 29 reasoning paragraph rewrites to reflect classification-driven routing rather than all-local-except-Scribe; introduces classification register and Classification Review stage in v0.1 product description)"
  - "router.yaml (becomes a template per-deployment; per-customer derivation from classification register + Sovereign Node LLC's current best-of-breed cloud routing)"
  - "CLAUDE.md (Beta model strategy section; reference to classification register; Sovereign Node LLC continuous-tracking commitment language)"
  - "docs/ARCHITECTURE_OVERVIEW.md (Beta model strategy section; classification-driven routing diagram; on-demand heavy Judge swap discipline)"
  - "skills/scribe-ghostwriter/SKILL.md (Phase 0 RFA Extraction extends to surface classification context per claim slot; what Scribe sees vs what gets locally slot-filled)"
  - "pipeline/blueprint/v0.1/section_07_scribe.md (split-context drafting pattern formalized as classification-aware-split-context; slot-fill agent invocation contract)"
  - "pipeline/blueprint/v0.1/section_05_pipeline.md (revision loop accommodates classification-driven routing per agent call; on-demand heavy Judge swap discipline)"
authority_source: v10.3 four-posture data-boundary doctrine (operator-curated boundary between local and cloud); ADR-001 substrate decision; v7.0.3 substrate corrective; operator directive 2026-05-08 ("we need the power with the privacy" — collapses Posture L/S/F framing into single classification-driven routing pattern)
version_wording_discipline: "LOCKED" inside this file refers to on-disk LOCKED state at filing time. The classification register is a NEW mechanism this amendment introduces; the Classification Review stage is a NEW pipeline stage; per-deployment router.yaml is a NEW config-derivation pattern. All three require Thesis-round review before LOCK.
---

# Amendment intent

The v0.1 architecture as locked has a sovereignty story ("nothing phones home, BYOK only") but no operationalized data-boundary discipline beyond per-org Law 3 isolation. The v10.3 business plan names a "four-posture data-boundary doctrine" but does not specify the mechanism that operationalizes it. The Beta product needs both *power* (frontier model capability) and *privacy* (data sovereignty for what genuinely needs it) — not a tradeoff between the two.

This amendment introduces three load-bearing primitives that together operationalize the power-with-privacy commitment:

1. **Classification register** — per-fact / per-class sensitivity tags populated during white-glove onboarding. Drives per-agent-call routing decisions: input that is Public + Shareable can route to cloud frontier seats; input containing Confidential content stays in local-only seats and confidential values get local-slot-filled before any post-fill seat sees the assembled draft.

2. **Classification Review stage** — named pipeline stage between Intake (KFR ingestion at onboarding) and first-grant-cycle. Operator + Sovereign Node LLC walk through the populated classification register, simulate the cloud-routing pattern on a real or representative grant cycle, and operator confirms classification + routing implications BEFORE customer ships. Sovereignty is operationalized here, not asserted.

3. **Per-deployment router.yaml derivation** — current `router.yaml` is one canonical file at workspace root with global model bindings. Beta makes it a per-deployment config derived from operator's classification register + Sovereign Node LLC's current best-of-breed cloud routing per task. Sovereign Node LLC ships router-template updates as the LLM landscape evolves; operator opts in or stays pinned per update.

This amendment also formalizes the **on-demand heavy Judge swap** for high-stakes grants (federal long-form, large award size, operator-flagged) — a 200B-class local model loaded on demand for routine-Judge runs that warrant max model capability without cloud routing.

# What changes

## §1. Single architectural pattern — classification-driven routing (replaces L/S/F posture framing)

Earlier exploration considered Posture L (local-default with Scribe cloud) / Posture S (selective per-agent) / Posture F (full-frontier cloud) as three operator-selectable tiers. That framing collapses under the operator directive 2026-05-08: 100% local sacrifices too much model capability and doesn't match the actual sensitivity profile of most clients; classification register does the work case-by-case.

Single pattern: **per-agent-call routing decision based on input classification.**

```
For each agent call:
  if any input contains Confidential OR operator_flagged:
    → route to local agent only
  elif all input is Public + Shareable:
    → route to cloud frontier (best-of-breed per Sovereign Node LLC's current router template)
  else (any class is indeterminate / unset):
    → route to local agent only (fail-closed default per §5)

Slot-fill agent:
  → ALWAYS local (touches Confidential by definition)
  → renders OPAQUE [SLOT_<numeric_id>] tokens to actual values from KFR + classification register
  → opaque slot IDs (e.g., [SLOT_001], [SLOT_002]) replace semantically-named placeholders
    BEFORE any cloud-routed seat sees the slot template; the mapping
    {slot_id → confidential_field_path} stays in local slot-fill agent's context only.
    Rationale: a cloud LLM that sees [SLOT_ANNUAL_REVENUE] may (a) hallucinate a plausible
    literal value into the slot position before slot-fill renders it, and (b) infer that
    "this organization has an annual_revenue field that is confidential" — both are leak surfaces.
    Opaque IDs eliminate (a) and reduce (b) to "this draft has N slots."

Once a draft is "post-fill" (Confidential values now embedded as text):
  → all subsequent seats that read it MUST be local routing
  → enforced structurally, not by policy
```

This is structural sovereignty. The data-flow design itself prevents Confidential content from reaching cloud routing; the classification register defines what counts as Confidential per client.

## §1.1 Post-fill power-tradeoff — explicit acknowledgment

The "all subsequent seats local-only on post-fill drafts" rule has a structural consequence the operator must understand: **for any grant draft that contains Confidential content** (which is the common case for real grants — financials, partnerships under negotiation, internal capacity assessments), the review-time seats (Editor, Red Team) and routine-Judge run on **local models only**. The cloud frontier's full capability is available during the **drafting phase** (Scribe sees the slot template + Public + Shareable input, returns a draft with opaque slot positions), but is structurally unreachable during the **review phase** (Editor / Red Team / routine-Judge read the post-fill draft, which carries Confidential text inline).

The operator directive "we need the power with the privacy" is delivered as **power for drafting + privacy for review** — not as both axes simultaneously for every seat. The architectural rationale: Scribe is the heaviest token consumer per cycle (full proposal generation, ~50–200K tokens), so frontier-cloud capability there is highest-leverage; review seats can deliver cross-family rigor on a 70B-class local stack without compromising rubric scoring quality (per A3 Semi-Formal Reasoning verdict format + cross-family ensemble). For high-stakes grants, the on-demand heavy-Judge swap (§4) restores frontier-equivalent capability locally on Judge specifically; Editor and Red Team continue at 70B-class local capacity.

**v0.2 / v1.x extension marker (NOT in v0.1 scope):** review-time anonymized-draft routing is a future architectural surface — render the post-fill draft back to opaque-slot form for cloud-routed Editor / Red Team passes, then re-render for operator review. This is a non-trivial extension (anonymization round-trip introduces drift surfaces, prompt-injection surfaces, and Logician gate obligations) and is explicitly out-of-scope-for-v0.1. Captured here so downstream architecture rounds know the surface exists.

The operator must understand and accept this tradeoff at Classification Review (§3 step 3 routing simulation surfaces it concretely). Operators uncomfortable with 70B-class local review on Confidential-bearing drafts have two options at v0.1: (a) classify more fields as Shareable (operator override per §7) so fewer drafts are post-fill-Confidential, or (b) accept review at local capacity for cycles where Confidential content is unavoidable. Option (b) is the default — the architecture does not steer the operator toward (a).

## §2. Classification register schema (new file: `vault_shared/classification/register.yaml`)

```yaml
schema_version: classification_register.v1
populated_at: <utc-timestamp>
populated_by: <operator_key_id>
populated_via: white_glove_onboarding | per_grant_sp0_override | operator_override

org_slug: <client>
classification_defaults:
  source: card_archetype  # which Capital Logic Card supplied defaults
  card_id: <e.g., farmer / educator / municipal_steward / arts_culture / cooperative_lead / catalyst>

field_classifications:
  - field_path: project_context.org.ein
    class: public
    locked_by: card_default
    operator_override: false
  - field_path: project_context.org.annual_revenue_audited
    class: confidential
    locked_by: card_default
    operator_override: false
  - field_path: project_context.org.location.address
    class: shareable
    locked_by: operator_override
    operator_override: true
    override_reason: "Org's address is on website; safe to share with cloud Scribe."
  ...

class_definitions:
  public:
    definition: "On the org's website, in funder-facing prior grants, in regulatory filings."
    routing: "Cloud-routable when ALL input is public + shareable; otherwise local."
    examples:
      - "Org name, EIN (SAM.gov-public), street address visible on website"
      - "Mission statement printed on annual report"
      - "Federal RFA text + agency-published rubric"
  shareable:
    definition: "Not public but operator-comfortable to share with cloud frontier models."
    routing: "Cloud-routable when ALL input is public + shareable; otherwise local."
    examples:
      - "Project narrative paragraphs the operator has previously sent to other funders"
      - "Aggregated, non-identifying outcome statistics"
      - "Acres in production / production volume rounded to nearest order of magnitude"
  confidential:
    definition: "Stays local. Slot-filled into post-fill drafts only after cloud agents return."
    routing: "Always local. Cloud routing structurally prevented at outbound boundary (§5)."
    examples:
      - "Audited annual revenue figures"
      - "Specific partnership names that are not publicly disclosed (e.g., fiscal sponsor relationship pending)"
      - "Internal capacity assessments / staff-comp-versus-budget detail"
      - "EIN of clients served by the applicant organization (when applicant is an intermediary)"
  operator_flagged:
    definition: "Operator marked sensitive in onboarding regardless of default class. Routes identically to confidential."
    routing: "Always local. Treated as confidential by §1 routing rule."
    examples:
      - "A field the operator wants tighter posture on for reasons specific to this grant cycle (e.g., a foundation that flagged a competitor)"
      - "Custom organizational data the Card archetype defaults didn't anticipate (e.g., recipe IP for a value-added farmer)"

grant_overrides:
  - grant_id: <rfa_hash>
    fields_overridden:
      - field_path: project_context.org.budget_detail_unaudited
        class_for_this_grant: confidential
        operator_reason: "This RFA is small foundation; budget detail not requested; tighter posture for this cycle."

audit_chain:
  - operator_signature_at_white_glove_completion
  - operator_signature_at_each_grant_sp0_review
```

The classification register is operator-signed (Ed25519) at white-glove completion + at each per-grant SP0 confirmation. Hash-chained per BT9 audit discipline. Lives in `vault_shared/classification/register.yaml` (cross-org defaults + class definitions) plus `orgs/<slug>/vault/classification/register.yaml` (per-client overrides + grant-level overrides).

## §3. Classification Review — new named pipeline stage

Position: between Intake (KFR ingestion at client onboarding) and first-grant-cycle (Scout discovery).

```
ONBOARDING (per-client, one-time)
  Intake → KFR populated + raw org docs catalogued
  ↓
  CLASSIFICATION REVIEW (named stage; operator + Sovereign Node LLC)
  ↓
DISCOVERY (per-cycle)
  Scout → ...
```

Steps within Classification Review:

1. **Inventory.** Sovereign Node LLC presents the operator with what data Intake has gathered, organized by Card-archetype default classifications.
2. **Operator override pass.** Operator reviews each classification, confirms or overrides per field.
3. **Routing simulation.** Sovereign Node LLC presents what the routing pattern *would* look like for a typical / representative grant cycle: which fields flow to cloud frontier, which slot-fill locally. Operator sees actual routing in real terms before customer ships.
4. **Test cycle.** Operator runs a real or representative grant through the full pipeline with classification active. Operator validates that routing matches their sovereignty expectations.
5. **Operator sign-off.** Classification register Ed25519-signed. Customer ships.

This stage is **mandatory for v0.1 Beta deployments**. It's where the sovereignty story actually gets operationalized for each client. Skipping it ships a deployment with un-validated classification, which is fail-closed by §5 below.

## §3.6 Incremental classification — fail-closed handling for new facts after onboarding

Classification Review runs **once at onboarding**. After onboarding, new facts continue to enter the system via Intake INCREMENTAL mode (a single new doc on arrival; per v7.0.4 architecture amendment + v7.0.6 Intake support agent role). New facts have no classification at the moment they land; allowing them to participate in routing decisions before classification is set would create a leak surface.

Discipline:

1. **Default to confidential.** Every fact extracted by Intake INCREMENTAL mode is tagged `class: confidential` at write time. The Logician PRE-gate `F-CLASS-NEW-FACT-UNCLASSIFIED` (per §5.1 below) blocks any pipeline run that attempts to consume a fact whose classification is `confidential` AND whose `locked_by: pending_operator_review` flag is set. This treats unclassified-by-default-as-confidential as the architectural floor.

2. **Operator review queue.** Newly-ingested facts surface in an operator review queue. Operator confirms or downgrades the classification on next pass.

3. **Per-grant pre-flight check.** Before each grant cycle's Scout/Scribe sees the fact, the pipeline confirms the fact has been operator-classified post-ingest. Unclassified facts STOP the cycle until reviewed.

4. **No silent promotion.** A fact's class can only DROP (more sensitive → less) by explicit operator action. The system never silently downgrades a `confidential` default to `shareable`.

This pattern delivers the structural-sovereignty invariant for the post-onboarding lifecycle: an unclassified fact is treated as confidential and cannot leak to cloud routing, regardless of what the routing rule sees.

## §3.7 Sign-off artifact format

The operator-signed classification register record is the load-bearing audit artifact. Schema:

```yaml
operator_signature_at_white_glove_completion:
  signed_at_iso8601: <utc-timestamp>
  signing_key_id: <Ed25519 key fingerprint per A12 crypto-agility envelope>
  signed_field_classifications_hash: <sha3_512:16 of canonical-form field_classifications block>
  signed_class_definitions_hash: <sha3_512:16 of class_definitions block>
  signed_card_default_card_id: <which Card archetype supplied defaults>
  signed_routing_simulation_artifact_path: <path to the §3 step 3 simulation output the operator reviewed>
  signed_test_cycle_artifact_path: <path to the §3 step 4 test-cycle pipeline run the operator validated>
  attestation_string: |
    "I, <operator_name>, have reviewed the classification register at the field level,
    confirmed routing simulation matches my sovereignty expectations, and validated a
    test cycle with classification active. I authorize this register as the load-bearing
    classification authority for this Golden Quill deployment as of <signed_at_iso8601>."

per_grant_sp0_signature:
  grant_id: <rfa_hash>
  signed_at_iso8601: <utc-timestamp>
  signed_overrides_hash: <sha3_512:16 of grant_overrides block for this grant_id>
  attestation_string: "I confirm the classification overrides for grant <grant_id> for this cycle."
```

Each per-grant SP0 signature appends to the chain. The Logician verifies signature freshness per the F-CLASS-* family (§5.1 below) on every cycle start.

## §4. Heavy on-demand Judge swap

Current `router.yaml` Judge is `google/gemini-2.5-pro` (cloud). Beta default Judge for routine grants is `groq/llama-3.3-70b-versatile` (local-routable when input is Confidential, cloud-routable when input is Public + Shareable). For high-stakes grants, a 200B-class local model loads on demand:

**Heavy Judge candidates (Sovereign Node LLC picks current best-of-breed; updated per quarterly review or 7-day emergency update):**

| Model | Architecture | Memory at Q4 | Notes |
|---|---|---|---|
| **DeepSeek V3** | 236B MoE / 37B active | ~140 GB total, ~50 GB active with offloading | Strongest reasoning in tier; comparable to GPT-4 / Claude Sonnet on rubric tasks |
| **Qwen 3 235B-A22B** | 235B MoE / 22B active | ~120 GB | Strong multilingual + reasoning |
| **Mistral Large 2 (123B)** | dense | ~80 GB | Smaller than 200B but strong instruction-following |
| **GPT-OSS 120B** | MoE / 5B active | ~70-80 GB | Already in router.yaml as Red Team primary; local version available |

Sovereign Node LLC tracks releases continuously and picks current best-of-breed; operator router-template update follows.

**Routing trigger discipline (when does heavy Judge fire):**

- Federal long-form RFA (NSF / NIH / USDA AFRI / SBIR Phase II / DOE / similar large federal programs)
- Award size > operator-set threshold (default $500K)
- Operator manually flags this grant as high-stakes during SP0 review
- Operator override in Classification Register's `grant_overrides` block

Routine grants stay on Llama 70B Judge. Heavy swap fires only on the criteria above; routing layer enforces.

**Memory choreography for heavy swap:**

```
ROUTINE MODE (always loaded):
  Substrate + embedding + Scout (Mistral 7B):  ~16 GB
  Editor + Judge primary (Llama 70B Q4):        ~45 GB
  Red Team (Qwen 32B Q4):                       ~22 GB
  Headroom + OS:                                ~45 GB
  Total:                                       ~128 GB

HIGH-STAKES JUDGE MODE (on-demand swap; ~2-5 min model load from NVMe):
  Substrate + embedding + Scout:                ~16 GB
  Editor (Llama 70B Q4 — stays loaded):         ~45 GB
  Heavy Judge (DeepSeek V3 active or chosen):   ~50 GB
  Red Team:                                     PAUSED (unloads, reloads after Judge run)
  Headroom + OS:                                ~17 GB
  Total:                                       ~128 GB

Latency: 2-5 min model load per swap. Acceptable because high-stakes Judge runs are reviewed by operator for an hour anyway. Intolerable for routine work — routing layer enforces.
```

## §4.1 High-stakes flag classification (closes F-GPTOSS-005 sub-issue 1)

The operator-set high-stakes flag (per §4 routing trigger discipline: "Operator manually flags this grant as high-stakes during SP0 review") is **itself sensitive operational metadata**. A list of which grants the operator has flagged high-stakes leaks the operator's risk perception, competitive positioning, and which funder relationships warrant heavy review. Without explicit handling this metadata could flow to a cloud-routed Judge run on a non-high-stakes grant in the same cycle, defeating the structural-sovereignty invariant for adjacent metadata.

Discipline:

1. **Storage location:** the high-stakes flag for grant `<rfa_hash>` lives in that grant's `grant_overrides` block of the per-org classification register at `orgs/<slug>/vault/classification/register.yaml` — the same audit-trailed structure as per-grant SP0 overrides (§7).

2. **Classification:** the high-stakes flag value is stored as `class: confidential` with `field_path: project_context.grants.<grant_id>.high_stakes`. Treated identically to any other Confidential field by §1 routing rule — never sent to any cloud-routed seat.

3. **Operator UX:** the high-stakes flag is set via the same per-grant SP0 override path (§3 step 4 + §3.7 sign-off chain). Setting it requires the operator's per-grant SP0 signature, which audit-trails the decision.

4. **Heavy-Judge swap dispatch:** when the routing layer determines a Judge call should swap to heavy mode, the routing decision happens **locally** based on the local-only classification register lookup. The "high-stakes" condition is never expressed in any prompt or routing decision message that crosses the cloud boundary. The cloud Judge (when running) sees its scoped input only; it cannot determine from its own input whether the Judge call is "routine" or "high-stakes."

5. **Failure code:** `F-CLASS-HIGH-STAKES-FLAG-LEAK` (POST-gate, per-call outbound boundary) — fail-closed if any cloud-routed payload contains the literal string `high_stakes` OR a tagged value referencing a high-stakes flag from the register. Added to the §5.1 F-CLASS-* family table as the twelfth primitive.

This closes Red Team Audit #2's F-GPTOSS-005 sub-issue 1.

## §4.2 Heavy-Judge swap timing side-channel — known v0.1 limitation

The heavy-Judge swap takes 2-5 min wall-clock. This latency is observable to:

- **Network-egress patterns:** from the same network the Golden Quill is on, an observer can detect the sustained-but-different traffic shape during model load (NVMe streaming if the model lives off-disk; specific port patterns if the heavy model invokes a distinct local endpoint).
- **Power / thermal / acoustic signatures:** an observer with physical proximity to the machine can detect sustained CPU / NVMe activity from fan noise + power draw.
- **Timing of operator workflow completion:** an observer with task-pacing visibility can correlate "operator took ~5 min longer on grant X" with "grant X was high-stakes."

**v0.1 disposition: operator-acknowledged known limitation, NOT a structural-sovereignty blocker.**

Reasoning:

1. **Threat-model alignment.** The Sovereignty Promise is about confidentiality of the data and operator control over keys/hardware. Behavior-pattern metadata side-channels are an operationally adjacent concern but do not violate the data-confidentiality invariant — the data itself never reaches cloud routing. The promise as written ("data stays local") holds.

2. **A1 single-client-per-Golden-Quill.** v7 LOCKED preflight assumption A1 explicitly scopes v0.1 to single-client deployments. The "external observer on same network" is on the operator's own network — observability there is a network-trust concern the operator already manages, not a Tilth-architectural failure.

3. **A4 operator is trusted.** The same machine + network that hosts the Golden Quill is non-adversarial to the operator's own work. v2 multi-tenant deployments (mutually-adversarial clients sharing one machine) DO change this threat model and DO require side-channel mitigation — which is why v2 hardening in v7 LOCKED Section O.5 already names "constant-time response padding" and "cache-flush per-org isolation" as v2 work.

4. **v0.2 / v1.x extension marker.** A future architectural surface for timing-side-channel mitigation: introduce padding latency (always inject 2-5 min delay on Judge calls regardless of swap status) so the swap event is masked. This trades quality-of-life (operator waits for routine Judge runs too) for side-channel hardening. v0.1 declines the trade; v0.2+ deployments serving multi-tenant or higher-threat-model clients may opt in. Tracked here as a forward extension, not a v0.1 blocker.

5. **Admin-risk ledger entry on first heavy-swap per cycle.** Each cycle's first heavy-swap event writes an entry to the per-org admin-risk ledger with severity `MEDIUM` and tag `timing-side-channel-v0.1-known`. Operator reviews on next pass; this surfaces the limitation without halting the cycle.

This is the explicit operator-acknowledged tradeoff. Operators uncomfortable with the known limitation can:
- (a) Decline to flag any grant high-stakes (heavy-swap never fires; routine 70B Judge handles all grants);
- (b) Enable the v0.2-style padding latency option once v7.0.x extension lands (out of scope for v0.1);
- (c) Run heavy-stakes Judge runs offline / off-hours to reduce observability.

This closes Red Team Audit #2's F-GPTOSS-005 sub-issue 2 by explicit acknowledgment + bounded-threat-model justification + v0.2 extension marker, not by mechanism. Operator + synthesis-tier disposition per L-005 (recorded in `pipeline/validation/v7_0_7_thesis_2026-05-09/audit_2_disposition.md`).

## §5. Fail-closed defaults (Logician-equivalent gate for routing)

- **Classification Review not signed → Beta deployment cannot ship.** Operator-signed classification register is a hard precondition. Pipeline halts on first run if `vault_shared/classification/register.yaml` lacks operator signature.
- **Classification register hash mismatch → all gates fail.** BT9 hash-chain integrity per existing Logician discipline.
- **Routing decision indeterminate → ROUTE LOCAL.** If the routing layer cannot determine whether a piece of input is Public / Shareable / Confidential, default is local. Cloud routing requires affirmative classification.
- **Cloud agent receives Confidential content → fail-closed at outbound boundary.** A Confidential value flowing to cloud is a P0 incident; pipeline halts; admin-risk ledger entry with HIGH severity; operator escalation.

## §5.1 F-CLASS-* failure-code family — architectural primitives

Per L-006 (preflight enforcement-layer existence), a v7.0.7 LOCK that depends on aspirational Logician code violates the lesson. v7.0.7 LOCK names the F-CLASS-* primitives at the **architectural-primitive layer** here; the §4 Logician v2.x amendment realizes the Cedar policy text and Python predicates in a **paired-LOCK** with this amendment per WS-L (architecture v7.0.7 + §4 Logician v2.x amendment LOCK as a compound transaction; neither lands without the other).

This pattern matches v7 LOCKED's discipline (A6 R.PF1 + R.PF2 named PRE-gates F-PIPELINE-TRACK-FROZEN + F-VAULT-ARTIFACT-ONLY as architectural primitives at v7 LOCK with implementation deferred to §5 v6 + §2 v7.2 spins; A7 named F-A7-CALIBRATION-* family; etc.). v7.0.7 carries the same shape: architecture amendment names primitives, blueprint amendment realizes them.

**F-CLASS-* family (twelve primitives — eleven baseline + F-CLASS-HIGH-STAKES-FLAG-LEAK added at Audit #2 narrow-fix per §4.1):**

| Code | Stage | Scope | Failure mode |
|---|---|---|---|
| F-CLASS-REGISTER-MISSING | PRE | onboarding gate | classification register file absent (vault_shared/classification/register.yaml or orgs/<slug>/vault/classification/register.yaml) |
| F-CLASS-REGISTER-UNSIGNED | PRE | onboarding gate | register present but operator_signature_at_white_glove_completion field missing or empty |
| F-CLASS-REGISTER-SIGNATURE-INVALID | PRE | every cycle start | Ed25519 signature verification on register fails |
| F-CLASS-REGISTER-HASH-MISMATCH | PRE | every cycle start | signed_field_classifications_hash or signed_class_definitions_hash does not match recomputed hash from current register content (silent edit detected) |
| F-CLASS-NEW-FACT-UNCLASSIFIED | PRE | per-cycle | a fact extracted by Intake INCREMENTAL mode is `confidential` AND `locked_by: pending_operator_review` AND being consumed by routing — operator must classify before consume |
| F-CLASS-ROUTING-INDETERMINATE | PRE | per-call | routing layer cannot resolve input to (public + shareable) OR (confidential / operator_flagged) — fail-closed default ROUTE LOCAL applies, but the call is also logged for operator review |
| F-CLASS-CLOUD-RECEIVED-CONFIDENTIAL | POST | per-call outbound boundary | a cloud-routed seat's request payload contains a value tagged `confidential` or `operator_flagged` — P0 fail-closed (request blocked, admin-risk ledger HIGH) |
| F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED | POST | per-call outbound boundary | a cloud-routed seat's request payload contains a literal value at a position registered as a slot template (cloud Scribe response embedded a synthesized value into a slot position before slot-fill ran) |
| F-CLASS-SLOT-ID-NON-OPAQUE | PRE | per-call outbound boundary | a cloud-routed prompt contains a slot identifier that is NOT of form [SLOT_<numeric_id>] (e.g., [SLOT_ANNUAL_REVENUE]) — fail-closed, prompt rejected |
| F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED | PRE | per-grant gate | grant_overrides block exists but per_grant_sp0_signature for the grant_id is missing or invalid |
| F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID | PRE | router.yaml derivation | per-deployment router.yaml derivation tried to apply an SN-LLC template whose Ed25519 signature did not verify (per §6.1) |
| F-CLASS-HIGH-STAKES-FLAG-LEAK | POST | per-call outbound boundary | a cloud-routed payload contains a literal `high_stakes` reference or a tagged value referencing the per-grant high-stakes flag (per §4.1) — fail-closed |

**Architectural commitment binding the §4 v2.x amendment (dormant pattern per A6 R.PF1 / R.PF2 precedent):** the twelve F-CLASS-* primitives above are named at v7.0.7 LOCK with **dormant Cedar / Python realization**. The §4 Logician v2.x amendment that closes WS-L is bound at its OWN LOCK time to realize all eleven gates with their declared stage, scope, and failure mode; any §4 v2.x amendment that omits, reorders, or weakens these primitives fails the v7.0.7 architectural commitment and cannot LOCK. The dormant-PRE-gate enforcement matches the proven A6 R.PF1 (F-PIPELINE-TRACK-FROZEN) and R.PF2 (F-VAULT-ARTIFACT-ONLY) pattern from v7 LOCKED 2026-04-19 — architectural names primitives at v0.1 LOCK; the binding fires at the future spin's LOCK ceremony.

**Why this is L-006-compliant.** L-006 prohibits "locking around ASPIRATIONAL infrastructure" but allows architectural primitives "scoped to the future phase that brings the ASPIRATIONAL mechanism online." v7.0.7 §5.1 names the EXISTS-tier architectural primitives (this table is on-disk evidence — not aspirational). The Cedar / Python realization is the named future phase (§4 v2.x at WS-L). The structural-sovereignty claim of v7.0.7 §5 is anchored by the on-disk primitive table here, not by code that doesn't yet exist.

**No-cycle-without-coverage gate (PRE-cycle Logician check).** Until §4 v2.x LOCKs and binds the eleven Cedar policies, the routing layer's structural enforcement runs through the dormant PRE-gate **F-CLASS-COVERAGE-INCOMPLETE** which fail-closes at every cycle start: any pipeline cycle that attempts to run with classification-driven routing active and the §4 v2.x amendment NOT LOCKed is rejected. This is the v0.1 Beta hard precondition: until WS-L closes, classification-driven routing is architecturally inactive and the deployment cannot ship Beta. Operator-visible: the Classification Review stage at white-glove cannot complete its step-4 test cycle without this coverage. This is the architectural lever that prevents Beta deployment from shipping with un-realized F-CLASS-* enforcement.

## §6. Per-deployment router.yaml derivation

Current `router.yaml` is one canonical file at workspace root with global model bindings. Beta makes router.yaml *per-deployment*, derived from:

1. **Sovereign Node LLC's router template** for the current best-of-breed routing per task (cloud frontier model per Scribe / Editor / Judge / Red Team / heavy-Judge-candidate)
2. **Operator's classification register** — defines per-call routing (cloud-when-non-sensitive, local-otherwise)
3. **Operator's posture preferences** — operator can opt to more-local for any agent (e.g., "I want Editor always local for our deployment")

`router.yaml` at customer deployment is generated, not hand-edited. Sovereign Node LLC ships template updates; operator opts in to take updates or stays pinned per release.

**Sovereign Node LLC continuous-tracking commitment:**

- **Soft commitment**: continuous evaluation of LLM landscape; ships router updates "as the landscape warrants"
- **Cadence promise**: quarterly review at minimum
- **Emergency updates**: within 7 days of meaningful upgrade emergence (e.g., new frontier-class open-weight release, new cloud frontier with substantially better cost/quality)
- **Operator opt-in**: every router template update is an operator decision; deployments don't auto-update

This continuous-tracking is part of the Sovereign Node LLC value-add. Customers paying for the curated stack get ongoing routing intelligence.

## §6.1 SN-LLC router-template integrity — Ed25519 signing + Golden Quill verification

The per-deployment router.yaml is derived from a template SN-LLC ships. The template is the trust root for cloud-routing decisions: it determines which model receives which classification of input. A compromised template (spear-phish on Josh's signing workstation, supply-chain attack on a release artifact, MITM on the update channel) could remap classifications to cloud destinations and silently leak Confidential content. v7.0.7 closes this surface structurally:

1. **SN-LLC signs every template release.** SN-LLC maintains an Ed25519 signing key (canonical fingerprint published at the architecture v7 LOCK lockfile + every Tilth release manifest, per A12 hybrid-crypto envelope). Every router.yaml template release is signed at release time; the signature accompanies the template artifact (detached `.sig` file or inline `signature:` field per release-format choice).

2. **Golden Quill verifies the signature before applying.** When the operator opts to take a router-template update, the Golden Quill verifies the Ed25519 signature against SN-LLC's pinned public key BEFORE applying the new template. Failure to verify → fail-closed: the update is REJECTED, the deployment stays on the previous pinned version, an admin-risk ledger entry with HIGH severity is appended, and the operator is notified.

3. **Public-key pinning + rotation discipline.** SN-LLC's signing key fingerprint is pinned at white-glove onboarding to the operator's classification register sign-off artifact (§3.7). Key rotation requires the new key to be co-signed by the previous key OR explicitly re-pinned at operator discretion (Trust-On-First-Use rotation, audited). A signature signed by a non-pinned key fail-closes regardless of provenance claims.

4. **A12 crypto-agility binding.** The `algorithm:` field on every router-template signature is hybrid-aware per A12. v0.1: Ed25519 only (signing infrastructure baseline). v0.2+: hybrid Ed25519 + ML-DSA-65 verifier accepts only signatures where BOTH legs verify, with `legacy_v0_1_migration_tail: true` exception for v0.1-era templates pre-dating ML-DSA rollout.

5. **Failure code:** F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID (§5.1).

**Why this is non-trivial.** A naïve "trust the SN-LLC URL" router-update flow puts the entire fleet's privacy posture on the security of the SN-LLC web infrastructure. The signing-key pin makes the trust root local-to-deployment: even if SN-LLC's web infrastructure is compromised, an attacker would need the SN-LLC signing key to ship a malicious template that the Golden Quill would accept. The signing key lives in SN-LLC's offline signing infrastructure (HSM or air-gapped workstation), not on the same machine that hosts the update channel.

**Operator-visible touchpoints:**

- White-glove onboarding pins the SN-LLC public key to the deployment.
- Operator opts in to template updates via a documented CLI flow (v0.1 headless): `tilth router-template update --pin-version <new_pinned_version>` verifies signature, surfaces a diff (which classifications changed routing), operator confirms.
- Rejected updates surface as admin-risk ledger entries the operator reviews on their next pass.
- Key rotation: SN-LLC publishes the new public key signed by the previous key; operator opts in via `tilth router-template rotate-signing-key`. Failed rotation leaves the deployment on the old key.

This closes the supply-chain trust surface Red Team flagged at Audit #1 (F-GPTOSS-003).

## §7. Card-archetype classification defaults (three-layer model)

Each Capital Logic Card carries default classifications for fields typical to that archetype:

- **Card-level defaults** (per archetype): "for Farmer Card, `annual_revenue_audited` defaults to confidential; `acres_in_production` defaults to shareable"
- **Operator overrides at white-glove**: "for THIS Mystic Mamas deployment, address is on the website so it's shareable not confidential"
- **Per-grant SP0 overrides**: "for THIS RFA cycle, treat budget_detail as confidential because this small foundation doesn't ask for budget at this granularity and exposing it weakens posture"

All three layers are operator-signed and audit-trailed. Lower layers override higher layers; per-grant overrides are most specific.

**No HARD-LOCKED postures at the Card level.** The classification register handles per-client sensitivity case-by-case. White-glove onboarding is the discipline; Card defaults are a starting point, not a ceiling.

## §8. Hardware Budget Table 29 reasoning paragraph rewrites

The 128 GB Pro tier hardware allocation stands. The justification paragraph in `Golden Quill Business Plan v10 4.docx` Appendix D / Hardware Budget gets rewritten:

OLD (current text in v10 4): hardware sized for primary 70B local model + on-demand 200B-class swap; substrate + embedding + small fast model; based on "sovereign substrate stack."

NEW: hardware sized for (a) always-local agents (Logician + slot-fill + Intake + Uploader + Scout); (b) local Editor / Judge / Red Team for sensitive-content routing per classification register; (c) on-demand heavy Judge (200B-class) for high-stakes runs; (d) data vault + classification register + KFR + Match Database storage; (e) offline capability when network is down; (f) local 70B+ stack covers cases where operator opts to more-local for specific cycles. Justification: power-with-privacy requires both the local stack (for sensitive content + offline + heavy-Judge-on-demand) AND the cloud frontier routing for non-sensitive content (max model capability). Hardware enables the local half of that equation.

## §9. What this amendment does not do

- Does not modify A1-A12.
- Does not modify the Five Operating Laws or the Four Autonomy Rules.
- Does not modify Section K hardware tier mapping (128 GB Pro tier stands).
- Does not introduce new council seats — uses v7.0.6 roster.
- Does not modify v7.0.3 substrate decision (Pydantic AI substrate stands).
- Does not specify the slot-fill agent's implementation details (which local model, prompt design, performance characteristics) — that lives in v7.0.7 companion blueprint section (Scribe Section 7 amendment).
- Does not specify the Classification Review stage's tooling (interview script, simulation harness, sign-off UI) — that lives in v7.0.7 companion onboarding playbook (separate doc).
- Does not specify v0.2 Data Collector or Report Generator routing — Data Collector / Report Generator inherit the same classification-driven pattern but their full specs live in v0.2 amendment.
- Does not specify v1.x Archivist routing — same.
- Does not modify the KFR schema or fact validity model (that's v7.0.4 scope; classification stays orthogonal to KFR).
- Does not modify the Funder Intelligence Database or Match Database schemas (v7.0.5 scope).
- Does not specify pricing-tier implications of classification-driven routing (different-posture customers may have different cost profiles; that's a biz-plan amendment, not v7.0.7).

## §10. Lock-history note + sequencing

- v7.0.1 (DRAFT): Section E.P Governance Plan Preflight — awaiting Thesis round before LOCK
- v7.0.2 (SELF-LOCKED 2026-05-04): Section A textual reconciliation
- v7.0.3 (SELF-LOCKED 2026-05-08): Substrate corrective (Pydantic AI absorbs LangGraph + OpenClaw)
- v7.0.6 (SCOPING DRAFT 2026-05-08, SELF-LOCK candidate after operator review): Roster — Red Team surfaced + Intake / Uploader added + v0.2 / v1.x slots reserved
- **v7.0.7 (REVISION DRAFT 2026-05-09 post-Audit #1, this file)**: Beta model strategy — classification-driven routing + Classification Review stage + heavy on-demand Judge + per-deployment router.yaml + Sovereign Node LLC continuous-tracking commitment. Audit #1 cleared 2026-05-09 with REQUIRES_FIXES from all three cross-family reviewers (Editor / Judge / Red Team); 8 author edits applied per §11. Awaiting Audit #2 verification.

Forward-pending:
- v7.0.4 KFR Amendment SCOPING DRAFT — composes against Intake (v7.0.6) + classification register (v7.0.7); KFR stays focused on fact validity, classification is orthogonal
- v7.0.5 Funder Intelligence Database + Match Database SCOPING DRAFT — composes against Archivist's curation slot (v7.0.6 reservation)

**Companion file edits batch** (lands when v7.0.6 + v7.0.7 SELF-LOCK / LOCK):
- README.md (Council table 5→6 rows; Support Agents section; Beta model strategy mention; classification register reference)
- docs/ARCHITECTURE_OVERVIEW.md (Five Seats → Six Seats; Support Agents section; Beta model strategy section; classification-driven routing diagram; on-demand heavy Judge swap discipline)
- CLAUDE.md (council enumeration; Beta model strategy section; classification register reference; What NOT to Do guards)
- pipeline/architecture/v0.1/tilth_architecture_locked.md (Section A council enumeration; new Section relating to classification register if appropriate)
- Golden Quill Business Plan v10 4.docx (Appendix D + Hardware Budget reasoning rewrites; Beta model strategy in customer-facing language)

**Thesis-round preparation** (for v7.0.7 LOCK):
- Editor pass: clarity of classification register schema; Classification Review stage operability for white-glove team
- Judge pass: rubric scoring against the architecture's stated goal (power-with-privacy); does the classification-driven routing deliver?
- Red Team pass: adversarial — can the classification register be misconfigured? Can a Confidential value leak to cloud through a path the architecture doesn't catch? What's the worst-case compromise scenario?

The Red Team pass is especially important — the sovereignty promise is load-bearing for the v0.1 Beta product, and any leakage path is a P0 architecture bug.

## §11. Author response log — Audit #1 closure (2026-05-09)

Audit #1 ran 2026-05-09 with cross-family roster per L-003: Editor=Llama 3.3 70B/Groq (Meta family), Judge=Gemini 2.5 Pro/Google, Red Team=GPT-OSS 120B/Groq (OpenAI-OSS family). Author=Anthropic (Claude). All three reviewers returned `REQUIRES_FIXES`; Judge score 67/100 (below the 85 LOCK bar); 11 raw findings consolidated into 8 author-response edit operations after L-005 §10b severity auto-promotion (two findings independently surfaced by two reviewers triggered promotion: F-CLASS-* aspirational-infrastructure stayed BLOCKING; slot-token semantic leak promoted from MEDIUM/LOW pair to HIGH).

Per-finding disposition:

| Audit #1 finding (after auto-promote) | Disposition | Edit landing in v7.0.7 revision |
|---|---|---|
| BLOCKING — F-CLASS-* enforcement in non-existent companion file (Judge F-GEMINI-001 + Red Team F-GPTOSS-001, L-006 violation) | CLOSED | NEW §5.1 enumerates twelve F-CLASS-* primitives at architectural layer (matches A6 R.PF1/R.PF2 dormant-PRE-gate precedent); F-CLASS-COVERAGE-INCOMPLETE PRE-cycle gate prevents Beta deployment shipping with un-realized §4 v2.x coverage |
| HIGH — Post-fill power-tradeoff for Editor + Red Team (Judge F-GEMINI-002) | CLOSED with explicit-tradeoff acknowledgment | NEW §1.1 explicitly reframes the operator directive as "power for drafting + privacy for review"; v0.2 review-time anonymization marked as future architectural surface, out-of-scope-for-v0.1 |
| HIGH — Classification Review one-time onboarding leaves new facts unclassified (Red Team F-GPTOSS-002) | CLOSED | NEW §3.6 incremental-classification discipline: Intake INCREMENTAL defaults new facts to `confidential`; F-CLASS-NEW-FACT-UNCLASSIFIED PRE-gate blocks pipeline runs that consume unclassified new facts |
| HIGH (auto-promoted) — Slot-token semantic leak (Judge F-GEMINI-003 + Red Team F-GPTOSS-004) | CLOSED | §1 routing rule rewritten to require opaque [SLOT_<numeric_id>] identifiers BEFORE any cloud-routed seat sees the slot template; F-CLASS-SLOT-ID-NON-OPAQUE PRE-gate enforces; F-CLASS-CLOUD-RECEIVED-OPAQUE-SLOT-FILLED POST-gate catches cloud-Scribe synthesis-into-slot fabrication |
| MEDIUM — Classification register schema clarity (Editor F-LLAMA-001) | CLOSED | §2 `class_definitions` block extended with definition + routing + worked-examples per class for all four class values |
| MEDIUM — Classification Review steps lack sign-off artifact format (Editor F-LLAMA-002) | CLOSED | NEW §3.7 sign-off artifact format names operator_signature_at_white_glove_completion record schema with attestation_string and per-grant SP0 signature chain |
| MEDIUM — Router.yaml supply-chain integrity (Red Team F-GPTOSS-003) + LOW — Router.yaml derivation clarity (Editor F-LLAMA-003) | CLOSED | NEW §6.1 SN-LLC Ed25519 signing of router-template releases + Golden Quill signature verification before applying + public-key pinning + A12 crypto-agility binding; F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID PRE-gate enforces fail-closed |
| LOW — `operator_flagged` class coverage gap (Judge F-GEMINI-004) | CLOSED | §1 routing rule explicitly handles `operator_flagged`: routes identically to `confidential` (always local); §2 class_definitions confirms routing semantics |

Eight edits, eleven findings closed. The architecture's central claim ("structural sovereignty, not policy") is now anchored by the on-disk F-CLASS-* primitive table (§5.1) plus the dormant-binding pattern that prevents Beta shipping with un-realized enforcement.

**Audit trail:** Audit #1 dispatch logs + per-reviewer prompts + raw responses + synthesis at `pipeline/validation/v7_0_7_thesis_2026-05-09/`.

## §12. Companion file edits at LOCK

Pending Audit #2 verification, the following companion edits land at v7.0.7 LOCK (paired-commit pattern):

- **CLAUDE.md** — adds Beta model strategy section + classification register reference + What-NOT-to-Do guards on opaque-slot-ID requirement.
- **docs/ARCHITECTURE_OVERVIEW.md** — adds Beta model strategy section + classification-driven routing diagram + on-demand heavy Judge swap discipline + §6.1 SN-LLC signing flow.
- **router.yaml** — header annotation that this file is now a per-deployment template (per §6 + §6.1); workspace router.yaml stays as Josh's dev-node deployment.
- **skills/scribe-ghostwriter/SKILL.md** — Phase 0 RFA Extraction extension surfaces classification context per claim slot; cloud-routable Scribe context distinguishes Public+Shareable input from Confidential-slot-template input.
- **pipeline/blueprint/v0.1/section_07_scribe.md** — formalizes classification-aware-split-context drafting pattern (cloud Scribe sees opaque slot template; local slot-fill agent renders Confidential values into post-fill draft).
- **pipeline/blueprint/v0.1/section_05_pipeline.md** — revision-loop accommodation: on revision, the routing layer re-evaluates classification per-call (input may have changed); Classification Review stage placement (between Intake and Discovery) named in pipeline phase diagram.
- **pipeline/architecture/v0.1/tilth_architecture_locked.md** — locked architecture file gets a new section reference to v7.0.7 if appropriate (matches v7.0.6 SELF-LOCK precedent).

The Logician §4 v2.x amendment realizing the twelve F-CLASS-* gates is NOT a v7.0.7 LOCK companion — it lands at WS-L per the dispatch plan. v7.0.7 LOCK + dormant-binding pattern is sufficient per L-006 architectural-corollary.
