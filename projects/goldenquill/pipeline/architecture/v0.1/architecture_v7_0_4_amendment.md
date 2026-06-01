---
title: Tilth Architecture — Amendment v7.0.4 (Key Facts Register — per-org quantitative substrate, SP0 freshness gate, F-LOGICIAN-FACT-DRIFT, Intake module spec, AWARD_INGEST mode)
filed: 2026-05-08
locked: 2026-05-09
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-09 — substantive architectural addition (new register schema + new pipeline stop point + new failure code family + Intake module formalization with three modes [BULK_INGEST / INCREMENTAL_INGEST / AWARD_INGEST] + Benchmarks Register sibling artifact). L-005 strict two-cycle Thesis CLOSED 2026-05-09 (Cycle 1 audit at pipeline/validation/v7_0_4_thesis_2026-05-09/cycle_1_audit.md; Cycle 2 verification at pipeline/validation/v7_0_4_thesis_2026-05-09/cycle_2_verification.md). **Section E carve-out:** single-Claude (Anthropic) Thesis Cycles 1+2 per v7.0.8 precedent (lock_history row 175); cross-family rigor (Editor=Llama/Groq, Judge=Gemini/Google, Red Team=GPT-OSS/Groq) DEFERRED to operator-driven re-run when multi-provider routing is live.
parent_lock: pipeline/architecture/v0.1/tilth_architecture_locked.md
parent_amendment: pipeline/architecture/v0.1/architecture_v7_0_3_amendment.md
companion_amendments:
  - "pipeline/architecture/v0.1/architecture_v7_0_6_amendment.md (roster — Intake named here in v7.0.6; full module spec lives in v7.0.4)"
  - "pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md (Beta model strategy — KFR schema does NOT carry classification; classification is orthogonal, lives in Classification Register per v7.0.7)"
companion_files_pending_edit:
  - "pipeline/blueprint/v0.1/section_04_logician.md (new POST gate for F-LOGICIAN-FACT-DRIFT; tolerance config; SP0 freshness review integration with PRE-gate sequence)"
  - "pipeline/blueprint/v0.1/section_05_pipeline.md (revision loop accommodates SP0 → KGIE → SP1 → drafting → SP2/SP3/SP4; Intake invocation contract for onboarding mode)"
  - "skills/scribe-ghostwriter/SKILL.md (Phase 1 KGIE Preflight extends with KFR cross-check; F-LOGICIAN-FACT-DRIFT awareness)"
  - "orgs/_TEMPLATE/ (KFR schema template; per-org KFR YAML stub; pending_facts queue template)"
  - "vault_shared/benchmarks/ (Benchmarks Register sibling artifact)"
authority_source: prior conversation 2026-05-06 ("we need a 'critical/key/important' information file/database to ensure bad numbers are not referenced in grants"); admin-risk register precedent (operator-curated, fail-closed, deterministic-gated registers); LDR-pattern for retrieval-augmented document indexing (LearningCircuit/local-deep-research)
version_wording_discipline: "LOCKED" inside this file refers to on-disk LOCKED state at filing time. The KFR schema, SP0 stop point, F-LOGICIAN-FACT-DRIFT failure code family, and Intake module spec are NEW mechanisms introduced by this amendment. All require Thesis-round review before LOCK.
m1_supersession: "M1 LOCKED 2026-05-10 (lock_history row 190) supersedes specific clauses; see architecture_v7_0_4_M1_amendment.md §0.1 for the supersession table."
---

> **[NOTE — SUPERSEDED CLAUSES SINCE 2026-05-10]**
>
> Specific clauses of this amendment are SUPERSEDED by **v7.0.4-M1** (LOCKED 2026-05-10, lock_history row 190). See `pipeline/architecture/v0.1/architecture_v7_0_4_M1_amendment.md` §0.1 for the supersession table.
>
> Superseded clauses include:
> - §1.1 (`F-KFR-SIGNATURE-INVALID` raw-bytes signing) → M1 §2 canonical-JSON signing + §2.6 legacy migration mode
> - §1 schema (admits any YAML construct) → M1 §2.3 anchor / alias / merge-key forbidden
> - §4.5 derivation AST grammar (informal prose) → M1 §3 explicit AST whitelist
> - §4 currency tolerance arithmetic (no type pin) → M1 §6 Decimal mandate; ban-float; explicit-context-required helper
> - §7.2 `F-BENCHMARK-CONTAINS-PER-ORG-REF` (boolean oracle on value-leg) → M1 §5 constant-time + audit-log + signed allowlist
> - §3.2 + §4.4 tamper-gates (no metadata coverage) → M1 §4 tag-mutation gate via on-disk SHA3-512 hash + atomic-read discipline
>
> v7.0.4 clauses NOT listed remain authoritative as written. Cross-family verification audit trail at `pipeline/validation/v7_0_4_thesis_cross_family_2026-05-10/`. M1 audit trail at `pipeline/validation/v7_0_4_m1_thesis_2026-05-10/`.

# Amendment intent

Bad numbers in a grant aren't a quality problem — they're an audit-finding, clawback, "you lied to a federal agency" problem. Worst-case cost is orders of magnitude higher than narrative drift. Tilth's existing v7 architecture has Logician POST-gates that catch citation-missing claims, a verdict-format discipline that requires premises with citations, and a SignedClaimEvidenceMap that operator-signs at review time. None of those mechanisms grounds quantitative claims in operator-validated facts; they ground claims in *retrievable text*, which is a different concern.

A grant claim that says "we trained 200 graduates" is grounded if it appears in PROJECT_CONTEXT or RFA — but PROJECT_CONTEXT is narrative substance, not a structured fact register. A second grant cycle later, the same applicant might claim "we trained 189 graduates" for the same year. Both numbers cited PROJECT_CONTEXT. Both passed POST-gates. Both are wrong: only one can be true, and there's no source-of-truth structure to detect the inconsistency.

This amendment introduces the **Key Facts Register (KFR)** — per-org structured quantitative substrate. Operator-curated, operator-signed, cadence-aware, RFA-required-fields-tagged. KFR is the source of truth for every numerical claim Scribe makes. F-LOGICIAN-FACT-DRIFT is the deterministic fail-closed gate that validates Scribe's quantitative claims against KFR with type-aware tolerance.

**Coherence-as-defensibility framing.** A claim grounded in KFR is structurally cheap to defend: when the funder asks "where did the 197 graduates number come from?", the KFR entry has source_doc + page + verbatim quote, and defense costs zero new energy. A fabricated or imputed claim is structurally expensive: each follow-up requires patching, the patches accumulate, audit drift compounds. Coherence is the architecture; KFR makes it operational.

**Three orthogonal axes per fact in v7.0.4 KFR schema:**

1. **Cadence** — how often does this fact change? (immutable / annual / quarterly / monthly / event-driven) → drives expiry computation
2. **Required-for tags** — which RFA categories or specific funders require this fact? → drives SP0 freshness review surface (which facts the operator must confirm for THIS grant cycle)
3. **NOT classification.** Classification is orthogonal — it's about *flow control* (where does this fact get sent for routing decisions), not about *fact validity*. Classification lives in the Classification Register per v7.0.7, not in KFR.

This amendment is **substantive** — new register schema, new pipeline stop point (SP0), new failure code family (F-LOGICIAN-FACT-DRIFT, F-EXTRACTOR-FABRICATION), new module specification (Intake / KFR ingestion). Requires Thesis round before LOCK.

# §1. KFR schema (new file: `orgs/<slug>/vault/kfr/register.yaml`)

```yaml
schema_version: kfr.v1
org_slug: <client>
populated_at: <utc-timestamp>
populated_by: <operator_key_id>

facts:
  - id: <opaque-uuid>
    who: <subject — org / program / role / partner / etc.>
    what: <fact name; e.g., "Total students enrolled, FY25">
    when_period: <FY25 / Q3-2025 / 2025-04-12 / etc.>
    when_as_of: <date the fact was last verified>
    when_cadence: <immutable | annual | quarterly | monthly | event_driven>
    when_expiry: <derived from when_as_of + when_cadence — set by populator, validated at read>
    where: <location qualifier if relevant — county / state / facility / acreage>
    why: <reason this fact matters; e.g., "RFA Section 2.b enrollment requirement">
    how:
      methodology: <how the value was measured / counted / verified>
      sample_size: <if statistical>
      assumptions: <if any>
    value: <the actual number or string>
    unit: <count | USD | acres | percentage | etc.>
    projection_or_actual: <projection | actual | mixed>
    comparison_anchor:
      prior_year_value: <optional self-comparison>
      benchmark_id: <reference to Benchmarks Register if peer-comparison>
    validation:
      confirmed_by: <operator_key_id>
      confirmed_when: <utc-timestamp>
      source_doc: <path to source document>
      source_page: <page number if applicable>
      source_quote: <verbatim quote that establishes the fact>
    confidence: <high | medium | low>
    required_for_category: [federal_ag, federal_education, state_workforce, ...]
    required_for_funder: [USDA-VAPG, NSF-INCLUDES, ...]

key_credentials:
  # Distinct subset for staff credentials, accreditations, certifications
  - id: <opaque-uuid>
    who: <name / role>
    credential: <credential name>
    granting_body: <institution>
    issued: <date>
    expires: <date or "none">
    source_doc: <path>
    confirmed_by: <operator_key_id>
    confirmed_when: <utc-timestamp>

audit_chain:
  - operator_signature_at_initial_population
  - operator_signature_at_each_sp0_review
```

**Format choice: YAML + Pydantic schema validation.** YAML for operator legibility (operator confirms KFR entries during white-glove and at SP0). Pydantic schema validation runs on every read — ensures schema integrity, catches malformed entries before any seat reads them. Same pattern as the rest of v0.1 substrate (Pydantic AI per v7.0.3).

**Per-org with grant-runtime subset.** One KFR per client. At SP0 (new stop point — see §3), the runtime query reads the RFA dissection's required-fields list and pulls KFR entries where `required_for_category` or `required_for_funder` matches. Operator confirms or refreshes those entries; remaining KFR entries stay in the background.

**No classification tag in the fact body.** KFR's job is fact validity. Classification (Public / Shareable / Confidential / Operator-flagged) is a flow-control concern that lives in the separate Classification Register per v7.0.7. KFR fact IDs are referenced from the Classification Register; the two registers are orthogonal.

## §1.1 KFR signature integrity at read time — F-KFR-SIGNATURE-INVALID PRE-gate (RT-07 closure)

The schema declares `validation.confirmed_by` and `audit_chain` but those declarations are inert without a Logician PRE-gate that **verifies operator Ed25519 signatures on every KFR entry before any seat reads it.** Adding the gate closes a defense-in-depth gap: a compromised KFR entry (operator-keyring-bypassed) would otherwise ship forward unchecked.

**Two new failure codes (Logician PRE-gate, HIGH severity — TAMPER_EVENT):**

| Code | Trigger |
|---|---|
| `F-KFR-SIGNATURE-INVALID` | KFR entry's `validation.confirmed_by` Ed25519 signature fails verification against operator-keyring active-key catalog (Section 1 M9 + key-currency check). |
| `F-KFR-AUDIT-CHAIN-BROKEN` | KFR entry's `audit_chain` has missing or out-of-order operator signatures (initial-population without subsequent SP0-review signatures, or SP0-review entries with non-monotonic timestamps, or signatures from retired keys without operator-confirmed rotation marker). |

PRE-gate runs at **session start** (before SP0) and at **draft-time read** (POST-gate analog when Scribe pulls a fact). Operator-keyring binding mirrors existing M9 per-org BYOK key-scoping discipline. The two new codes register with Logician's PRE/POST gate sequence in §4 LOCKed-blueprint companion edit (pipeline/blueprint/v0.1/section_04_logician.md F-LOGICIAN-FACT-DRIFT family addition).

## §1.2 Classification Register binding — KFR ↔ Classification orthogonal cross-reference (J-05 / RT-10 closure)

KFR entries do not carry a classification tag in the fact body, but **every KFR entry exposes a `classification_register_ref` field referencing the Classification Register entry that governs that fact's routing per v7.0.7.**

Schema addition to §1 (one new top-level field per KFR fact):

```yaml
facts:
  - id: <opaque-uuid>
    # ... existing fields ...
    classification_register_ref: <classification_register_entry_id | null>
    # null defaults to Confidential (fail-closed) — Scribe / Editor / Judge reading the fact
    # routes through the local-only path until a Classification Register binding is filed.
```

**Default-fail-closed posture.** If `classification_register_ref` is absent or null, the fact is treated as **Confidential** for routing purposes (per v7.0.7 §1 — "If any input contains Confidential → route to local agent only"). Operator must explicitly bind to Public / Shareable / Operator-flagged in the Classification Register to enable cloud-frontier routing.

**v7.0.7 companion edit:** Classification Register schema adds `kfr_fact_ref` field mirroring this binding (operator-driven runtime keys both directions). Cross-reference is symmetric.

# §2. Cadence-aware expiry

Each fact's `cadence` drives `expiry` computation:

| Cadence | Expiry rule |
|---|---|
| `immutable` | No expiry. EIN, UEI, founding date, legal entity type. |
| `annual` | as_of + 365 days. Annual revenue, annual enrollment, annual production. |
| `quarterly` | as_of + 92 days. Quarterly metrics, board reports. |
| `monthly` | as_of + 31 days. Monthly metrics, headcount snapshots. |
| `event_driven` | No fixed expiry; refreshed when a triggering event occurs. Last A-133 audit, last accreditation, last leadership change, last lawsuit. |

Stale facts (past expiry) surface at SP0 with a STALE flag. Operator must refresh or mark-as-still-current before the fact can ground a Scribe claim.

# §3. SP0 KFR Freshness Review — new stop point

Position: before KGIE preflight. The stop-point chain becomes:

```
SP0 (KFR freshness review)
  → KGIE preflight
  → SP1 (spine lock)
  → drafting
  → SP2 (per-section operator review)
  → SP3 (pre-Editor)
  → SP4 (post-Editor)
```

SP0 surface to operator:

1. **Stale facts** — facts whose expiry has passed. Operator confirms current value (refresh in place) or marks STALE-ACKNOWLEDGED (acknowledged but not refreshable for this cycle). STALE-ACKNOWLEDGED entries get tolerance-match treatment per §4.6 (F-FACT-DRIFT-EXPIRED-LANDING).
2. **Required-for-this-RFA gaps** — facts the RFA dissection identified as required but not present in KFR. Operator either fills the fact (full schema) or marks NEEDED for operator follow-up.
3. **Newly-confirmed facts** — facts the operator wants to confirm-current at this cycle even if not stale.

SP0 output: operator-signed delta to KFR (Ed25519). Pipeline cannot advance to KGIE without SP0 sign-off.

## §3.1 SP0 review UX shape

White-glove playbook UX is detailed in `playbooks/white_glove/sp0_review.md` (out of scope for this amendment). Data contract pinned here:

- **Three-pane operator surface:** stale-facts list / required-but-missing list / refresh-now picks.
- **Atomic delta:** operator's confirmations and edits batch into a single `sp0_delta` record, Ed25519-signed at sign-out, with a deterministic `delta_id = sha3_512(canonical_json({rfa_hash, kfr_state_pre, kfr_state_post, signed_at_utc}))[:24]`.
- **Ledger entry:** `sp0_delta` writes to admin-risk ledger as `ledger_kind="sp0_delta"`, monotonic `seq_id`, parent-hash chained per existing M8 discipline.
- **Idempotent re-entry:** if operator partially completes SP0 and resumes (per Rule 1 Save State Always), the next session reads the partial delta state and resumes the operator's pending picks.

## §3.2 Required-for-RFA NEEDED hard-block — F-LOGICIAN-FACT-NEEDED-REQUIRED (J-04 / RT-08 closure)

If a fact tagged `required_for_funder` matches the current RFA AND the fact is in NEEDED state at SP0 sign-out, **the pipeline HALTS at SP0 and cannot advance to KGIE.** Operator must either fill the fact in full schema or remove the funder from the in-flight grant cycle.

**New failure code:**

| Code | Trigger | Severity |
|---|---|---|
| `F-LOGICIAN-FACT-NEEDED-REQUIRED` | At SP0 sign-out, a KFR entry with `required_for_funder` matching the current RFA is in NEEDED state. | HARD_BLOCK — pipeline cannot advance |

Closes the silent-skip path where Scribe might draft against an absent required fact (either fabricating or shipping a `[NEEDED]` token; the existing F-PRE-15 catches the `[NEEDED]` token but not silent fabrication when Scribe rephrases around the gap).

# §4. F-LOGICIAN-FACT-DRIFT — new failure code family

Logician POST-gate adds a new check: **every numerical claim in a Scribe draft must trace to a KFR entry within type-aware tolerance, OR be operator-approved as a DERIVED fact with documented derivation.**

**Failure code family (F-LOGICIAN-FACT-DRIFT umbrella, 9 codes total post-Cycle 1 fixes):**

| Code | Trigger |
|---|---|
| `F-FACT-DRIFT-UNTRACED` | Numerical claim in draft does not match any KFR entry, AND has no `derivation_id` annotation per §4.7. |
| `F-FACT-DRIFT-OUT-OF-TOLERANCE` | Numerical claim matches a KFR entry but value is outside type-aware tolerance. |
| `F-FACT-DRIFT-EXPIRED` | Numerical claim cites a KFR entry that's past its expiry without operator-acknowledged STALE. |
| `F-FACT-DRIFT-EXPIRED-LANDING` | Numerical claim tolerance-matches a STALE-ACKNOWLEDGED KFR entry without claim-level operator override per §4.6. (RT-03 closure.) |
| `F-FACT-DRIFT-DERIVATION-UNAUTHORIZED` | Draft contains a value annotated with `derivation_id` per §4.7 that has no matching operator-signed derivation entry in `pipeline/validation/fact_overrides/`. |
| `F-FACT-DRIFT-DERIVATION-CHAIN` | Operator-signed derivation entry's `derivation_formula` references another derivation rather than only KFR entries (per §4.5 — closes RT-01). |
| `F-FACT-DRIFT-DERIVATION-KEY-RETIRED` | Operator-signed derivation entry's `audit_chain_signature` was generated by a key not currently active in the Section 1 key catalog at draft-read time (per §4.4.1 — closes J-02). |

**Sibling failure codes registered with this amendment:**

| Code | Trigger | Owner-§ |
|---|---|---|
| `F-LOGICIAN-FACT-TOLERANCE-DRIFT` | Per-fact `tolerance_pct` widened beyond default at any point in current grant cycle without operator-signed re-confirmation in admin-risk ledger (per §4.4 — closes RT-02). | §4.4 |
| `F-LOGICIAN-FACT-NEEDED-REQUIRED` | At SP0 sign-out, a KFR entry tagged `required_for_funder` matching the current RFA is in NEEDED state. HARD_BLOCK. | §3.2 |
| `F-KFR-SIGNATURE-INVALID` | KFR entry operator Ed25519 signature fails verification at read time. | §1.1 |
| `F-KFR-AUDIT-CHAIN-BROKEN` | KFR entry audit_chain has missing/out-of-order signatures. | §1.1 |
| `F-EXTRACTOR-FABRICATION` | Intake-extracted candidate fact's `source_quote` does not literally appear in `source_doc` at `source_page` per §5.2 exact-match semantics. PRE-queue (rejects pre-operator-review). | §5 |
| `F-EXTRACTOR-AWARD-SIGNATURE-INVALID` | AWARD_INGEST mode invoked but won-proposal artifact signature OR award document signature fails verification (per §5.3 — closes RT-06). | §5.3 |
| `F-BENCHMARK-CONTAINS-PER-ORG-REF` | Benchmark entry in `vault_shared/benchmarks/register.yaml` has source_doc path under `orgs/<slug>/...` OR value tolerance-matches a value in any per-org KFR (per §7.2 — closes RT-05). | §7.2 |

**Tolerance config per fact-type (J-01 closure: tightened currency defaults):**

| Fact type | Tolerance |
|---|---|
| Identifiers (EIN, UEI, license numbers, registration numbers) | Exact match. Zero tolerance. |
| Legal claims (501c3 status, accreditation, certifications) | Exact match. Zero tolerance. |
| Counts (students enrolled, acres planted, head of cattle) | Default ≤2%. Configurable per-fact via `tolerance_pct` field, subject to §4.4 tamper-gate. |
| Currency (revenue, budget, expenses) | **Default ≤0.5% with absolute floor of $2,500.** I.e., the gate fires when `abs(draft_value - kfr_value) > max(0.005 * kfr_value, $2500)`. Operator can widen per-fact via `tolerance_pct` field, subject to §4.4 tamper-gate (admin-risk-ledger logged at HIGH severity, operator re-confirms at next SP0). The prior $100K threshold pattern is **superseded** — federal-grant-scale clawback risk applies below $100K too (J-01). |
| Percentages and rates | Default ±1 percentage point absolute. |
| Dates and time periods | Exact match unless operator marks `tolerance_days`. |
| **Ranges (min/max value pair)** | Tolerance applies to each bound independently per the underlying type's rule. Example: range `5,000–7,500 lb` with count tolerance ≤2% accepts draft values from `4,900` to `7,650` (E-03 closure). |

## §4.4 Tolerance config tamper-gate — F-LOGICIAN-FACT-TOLERANCE-DRIFT (RT-02 closure)

Tolerance widening is the highest-leverage attack surface in the F-LOGICIAN-FACT-DRIFT family. A single `tolerance_pct=50` write on a $5M currency fact passes a $2.5M-off claim. The amendment closes the silent-write path:

- Every per-fact `tolerance_pct` change **beyond** the type-default is admin-risk-ledger logged at HIGH severity (`ledger_kind="kfr_tolerance_widen"`).
- The ledger entry includes: `fact_id`, `prior_tolerance_pct`, `new_tolerance_pct`, `operator_key_id`, `signed_at_utc`, `rationale` (operator-supplied free text).
- At the next SP0 review (current grant cycle), the widened tolerance surfaces as a **re-confirm prompt**; operator must explicitly re-sign.
- **F-LOGICIAN-FACT-TOLERANCE-DRIFT** fires at draft-time read of a KFR entry whose `tolerance_pct` is widened beyond default AND has no operator re-confirmation signature in the current grant cycle's ledger. HARD_BLOCK.

### §4.4.1 Derivation signature key currency (J-02 closure)

Derivation override entries (`pipeline/validation/fact_overrides/<rfa_hash>/<derivation_id>.yaml`) carry an `audit_chain_signature` field. The signature must be generated by a key **currently active** per Section 1 key catalog at **derivation-write time** (verified at write) AND at **draft-time read** (verified at read). Rotated keys whose retirement timestamp precedes a derivation-write timestamp invalidate the derivation; F-FACT-DRIFT-DERIVATION-KEY-RETIRED fires.

This is the same key-currency discipline already applied to claim-evidence map signatures per Section 4 v2.1 §4.5.2.

## §4.5 Derivation chain depth limit — F-FACT-DRIFT-DERIVATION-CHAIN (RT-01 closure)

**Derivations can ONLY reference KFR entries.** Derivation-of-derivation is rejected at write time and at draft-time read.

Allowed `derivation_formula` grammar (Python AST validated at write):

```
derivation_formula: <expr>
<expr>: <kfr_ref> | <expr> <op> <expr> | <literal>
<kfr_ref>: kfr_facts['<fact_id>'].value
<op>: + | - | * | /
<literal>: <int> | <float>
```

**Disallowed:** any reference to `derivations[...]`, `pending_facts[...]`, `benchmarks[...]`, or any other lookup. The grammar permits only `kfr_facts['<fact_id>'].value` references and arithmetic combinations thereof.

Logician PRE-gate (at derivation write) and POST-gate (at draft read) walk the AST and reject any derivation whose formula contains a non-KFR reference. F-FACT-DRIFT-DERIVATION-CHAIN fires; admin-risk-ledger logged at HIGH severity.

**Why depth-1:** depth-N chains compose audit risk multiplicatively. A single bad input fact (operator-mistake class) at depth-1 affects exactly the derivations using it. At depth-2+, a single bad input fact can affect derivations that chain through other derivations, and the operator can no longer trace which downstream values are affected. Depth-1 keeps the dependency graph flat and operator-auditable.

## §4.6 Tolerance-match against stale-acknowledged entries — F-FACT-DRIFT-EXPIRED-LANDING (RT-03 closure)

Existing F-FACT-DRIFT-EXPIRED fires only when the draft **explicitly cites** an expired KFR entry. The amendment extends:

- If a draft value tolerance-matches a STALE-ACKNOWLEDGED KFR entry (entry past expiry but operator marked STALE-ACKNOWLEDGED rather than refreshing), **F-FACT-DRIFT-EXPIRED-LANDING fires.** HARD_BLOCK.
- Operator must either (a) refresh the fact to current value, OR (b) explicitly mark the claim "stale value is the current value" via signed override at draft-review time.

Closes the silent path where Scribe drifts onto a stale value within tolerance of an acknowledged-but-not-refreshed entry — the entry is "still in the KFR" but the value is no longer asserted as current.

## §4.7 Derivation detection mechanism — `derivation_id` annotation (RT-09 closure)

Logician needs a deterministic way to distinguish "derived value (legitimate, computed from KFR entries)" from "untraced claim (illegitimate, no KFR backing)." The amendment formalizes:

- **Scribe MUST annotate any derived value at draft-emit time** with an inline annotation: `<derivation_id="<opaque-id>">value</derivation_id>`. The annotation is HTML-style; stripped before final draft assembly but parsed by Section 4 claim extractor (analog to existing claim-tagging discipline per Section 4 §2.1).
- Claim extractor produces one `ClaimEntry` per annotated value, with `tag="DERIVED"` and `derivation_ref="<opaque-id>"` referencing a derivation entry under `pipeline/validation/fact_overrides/<rfa_hash>/<derivation_id>.yaml`.
- **Logician POST-gate routing:**
  - Value with `derivation_id` annotation + matching derivation entry that passes signature/key-currency/chain-depth checks → PASS.
  - Value with `derivation_id` annotation + missing or invalid derivation entry → F-FACT-DRIFT-DERIVATION-UNAUTHORIZED.
  - Value WITHOUT `derivation_id` annotation that matches no KFR entry within tolerance → F-FACT-DRIFT-UNTRACED.
  - Value WITHOUT `derivation_id` annotation that matches a KFR entry within tolerance → PASS.

This composes with v7 §A3 SFR three-block discipline (Scribe's verdict-block format already supports inline annotations; the `derivation_id` annotation is one more annotation kind).

## §4.8 Range-typed facts (E-03 closure)

KFR schema permits range-typed facts where `value` is `null` and the schema includes `value_min` + `value_max` siblings. Tolerance applies to each bound independently per the underlying type rule (e.g., a count range `5000-7500` with default 2% tolerance accepts draft values within `[4900, 7650]`).

**Override path: DERIVED facts.** Scribe may legitimately derive values that aren't in KFR directly — e.g., draft says "approximately 200 students" when KFR says 197 graduates + 3 transfer-completions per RFA's definition of "students." This is a DERIVATION:

```yaml
# pipeline/validation/fact_overrides/<rfa_hash>/<derivation_id>.yaml
derivation_id: <opaque>
draft_offset: <where in the draft>
draft_value: 200
derivation_formula: "kfr_facts['graduates_fy25'].value + kfr_facts['transfer_completions_fy25'].value"
operator_approval:
  approved_by: <operator_key_id>
  approved_when: <utc-timestamp>
  reason: "RFA defines 'students' as graduates + transfer completions per Section 1.b."
audit_chain_signature: <Ed25519>
```

Logician POST validates: every draft number traces to either (a) a KFR entry within tolerance, or (b) an operator-signed DERIVATION entry. Anything else fails F-FACT-DRIFT.

**Composition with v7.0.7 classification routing.** F-LOGICIAN-FACT-DRIFT fires regardless of which Card / which posture / which routing path produced the draft. Cards × MyCel × Console × Judge composition is preserved — every framed claim still traces to KFR or operator-signed derivation.

# §5. Intake module specification (named in v7.0.6, spec'd here — three modes)

**Intake** is the v0.1 support agent that handles KFR ingestion at client onboarding, continuous operations, and award acceptance. Always-local (sees raw uploaded org docs and won-proposal artifacts; mixed-classification surface).

**Three modes** (mode names use `*_INGEST` convention per E-04 closure for operator-mental-model coherence):

1. **BULK_INGEST** (onboarding) — operator drops a folder of org documents (annual reports, 990s, audited financials, employee rosters, program reports, partnership LOIs, prior grant applications). Intake sweeps the folder, extracts candidate facts. Output: `orgs/<slug>/vault/kfr/pending_facts.yaml` queue.

2. **INCREMENTAL_INGEST** (continuous) — operator adds a single new document during operations. Intake processes it on arrival. Trigger: operator-explicit (drag-drop into `orgs/<slug>/intake/inbox/`) at v0.1; filesystem-watcher trigger deferred to WS-E §11 Intake blueprint round.

3. **AWARD_INGEST** (award acceptance — pre-LOCK addition per dispatch packet §WS-C decision 8h default) — operator marks a submitted proposal as WON. Intake extracts `proposal_commitments.yaml` from the won-proposal artifact at `orgs/<slug>/vault/grants/<grant_id>/submission/draft_<v>.md` (operator-signed at submission per Uploader v0.1) plus the funder's award document (where applicable, funder-signed via PDF or DOCX with embedded signature). Output: `orgs/<slug>/vault/grants/<grant_id>/proposal_commitments.yaml`. WS-J Report Generator consumes this as authoritative for commitment-tracking during reporting cycles. See §5.3 for full contract.

**Substrate (per the LDR-pattern decision):**

- FAISS or Chroma vector store for document indexing
- Embedding model: bge-large-en-v1.5 (already in v0.1 hardware budget)
- Pydantic AI tool composition (per v7.0.3 substrate decision) for orchestration
- Intake calls a small local LLM (Mistral 7B class — same family as Scout's local model) for fact extraction. Always-local.

## §5.1 Extraction discipline (BULK_INGEST + INCREMENTAL_INGEST modes)

For each candidate fact, Intake produces:

```yaml
candidate_fact:
  who: ...
  what: ...
  when_period: ...
  when_as_of: ...
  when_cadence: ...
  ...
  source_doc: <absolute path>
  source_page: <integer>
  source_quote: <verbatim quote>  # CRITICAL — must literally appear in source_doc at source_page
                                    # per §5.2 exact-match semantics
  confidence_score: <0.0 - 1.0 from extractor model>
```

Candidates land in `orgs/<slug>/vault/kfr/pending_facts.yaml` queue.

## §5.2 F-EXTRACTOR-FABRICATION exact-match semantics (J-03 / RT-04 closure)

Before any candidate enters `pending_facts.yaml`, Intake's deterministic post-processor validates `source_quote` against `source_doc` at `source_page` per the following discipline:

**Allowable normalization (PASS):**

- **Unicode normalization:** both quote and source bytes are normalized to NFC before comparison.
- **Whitespace normalization:** runs of `[\t\n\r\f\v ]+` collapse to a single ASCII space; leading/trailing whitespace stripped. (Per RFC 3066 / W3C XML Information Set whitespace normalization.)

**REJECTED (treated as fabrication):**

- **OCR-substitution mapping** ("0" ↔ "O", "1" ↔ "l", "5" ↔ "S", etc.) — REJECTED. PDFs with bad OCR output that produce ambiguous source bytes must be re-OCR'd by operator before Intake processes them; the extractor does NOT silently bridge OCR errors.
- **Page-number off-by-one** — disallowed in `BULK_INGEST` and `INCREMENTAL_INGEST` modes; allowed only in `AWARD_INGEST` mode with operator-confirmation flag (see §5.3 — proposal documents may reflow when re-rendered post-submit, justifying ±1 page tolerance with operator confirmation).
- **Substring-of-claim with ellipsis** — REJECTED. Quote must literally span the start-to-end of the asserted source bytes.

If verbatim match fails per the above semantics, the candidate is rejected pre-queue with `F-EXTRACTOR-FABRICATION` logged to admin-risk ledger at HIGH severity. Cheapest gate in the system; runs before operator review.

**Operator review.** Operator reviews `pending_facts.yaml` queue with side-by-side display: extracted fact / source quote / source document at source page. Operator confirms (promotes to KFR), edits (modifies before promotion), rejects (drops with audit trail in `pipeline/validation/extractor_rejects/`), or merges with existing KFR entry.

**Confirmed facts promote to KFR** with `validation.confirmed_by` and `validation.confirmed_when` populated, and `audit_chain` initialized with `operator_signature_at_initial_population`.

## §5.3 AWARD_INGEST mode contract (RT-06 closure)

The third Intake mode lands at v7.0.4 LOCK per the dispatch packet's pre-LOCK directive. AWARD_INGEST owns the ingestion-discipline boundary at award acceptance time, keeping Intake the single owner across BULK_INGEST / INCREMENTAL_INGEST / AWARD_INGEST modes. WS-J Report Generator consumes the output as authoritative for commitment-tracking.

**Trigger:** operator-explicit only at v0.1. Operator marks a submitted proposal as WON via:
```
tilth intake award-ingest --org <slug> --grant <grant_id> --award-doc <path>
```
No filesystem-watcher / scheduled / inbox-watcher triggers at v0.1. (Defer to v0.2 WS-E.)

**Inputs:**

1. **Won-proposal artifact** — `orgs/<slug>/vault/grants/<grant_id>/submission/draft_<v>.md` (operator-signed at submission per Uploader v0.1; `SignedClaimEvidenceMap` already on disk per Section 4 v2.1).
2. **Award document** (where applicable) — funder's official award notification. Funder signature varies (PDF with digital signature / DOCX with embedded signature / unsigned PDF for funders that don't sign). `--award-doc` operator-supplied path.

**Pre-extraction verification:**

- Won-proposal artifact's operator signature MUST verify (per existing Section 4 §4.5 verify_claim_evidence_map discipline). Failure → AWARD_INGEST refuses + `F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal` logged at HIGH severity.
- Award document signature, where present, MUST verify against funder's published signing key (operator-curated per `vault_shared/funders/<funder_id>/signing_keys.yaml` — populated at first AWARD_INGEST per funder, optional). If award document is unsigned (funder doesn't publish signing keys), operator confirms the document path is the authoritative award notification via attestation flag at the CLI invocation. Failure → AWARD_INGEST refuses + `F-EXTRACTOR-AWARD-SIGNATURE-INVALID.award` logged at HIGH severity.

**Output schema** (`orgs/<slug>/vault/grants/<grant_id>/proposal_commitments.yaml`):

```yaml
schema_version: proposal_commitments.v1
grant_id: <slug>
rfa_hash: <sha3_512 of RFA — copies from the proposal's claim-evidence map>
populated_at: <utc-timestamp>
populated_by: <operator_key_id>

commitments:
  - commitment_id: <opaque-uuid>
    source_section: <RFA section name, e.g., "Section 2.b Outcomes">
    commitment_text: <verbatim quote from the won proposal stating the commitment>
    commitment_proposal_offset: <byte offset in source draft for operator-side highlighting>
    measurable_metric: <what's being measured, e.g., "students enrolled">
    target_value: <numeric target>
    target_unit: <count | USD | acres | percentage | etc.>
    due_period: <FY26 / Q4-2026 / 2026-09-30 / etc.>
    source_proposal_path: <path to draft_<v>.md>
    source_proposal_signature_verified_at: <utc-timestamp>
    source_award_doc_path: <path to award document, or null>
    source_award_doc_signature_verified_at: <utc-timestamp, or null if unsigned funder>

audit_chain:
  - operator_signature_at_award_ingest_completion
```

Each commitment is operator-reviewed (same side-by-side surface as BULK_INGEST candidate review) before it lands as a structured row. Operator can edit `measurable_metric` / `target_value` / `target_unit` / `due_period` to clarify intent (the proposal text may be narrative; the commitment row is structured).

**KFR linkage:** Each commitment's `target_value` may reference an existing KFR fact (e.g., "200 students enrolled FY25" commitment is the same `target_value` as the KFR fact `students_enrolled_fy25`). Where the linkage is explicit, the commitment row carries `kfr_fact_ref: <fact_id>`; F-LOGICIAN-FACT-DRIFT discipline applies during Report Generator's reporting cycles (Report draft values must trace to KFR or to AWARD_INGEST proposal_commitments).

**Failure path:** If any pre-extraction verification fails, AWARD_INGEST refuses the operation, writes `F-EXTRACTOR-AWARD-SIGNATURE-INVALID.{proposal | award}` to the admin-risk ledger at HIGH severity, and emits no `proposal_commitments.yaml`. Operator must re-fetch valid signed artifacts before retrying.

# §6. PROJECT_CONTEXT.md migration

Pre-v7.0.4: PROJECT_CONTEXT.md held both narrative substance (mission, history, partnerships) and quantitative substance ([NEEDED] fields for EIN, UEI, enrollment counts, revenue, etc.).

Post-v7.0.4: PROJECT_CONTEXT.md keeps narrative substance only. Quantitative substance migrates to KFR with structured schema. The `[NEEDED]` placeholder pattern in PROJECT_CONTEXT migrates to `[NEEDED]` entries in KFR's `pending_facts.yaml` queue or to KFR entries with explicit operator-marked NEEDED status.

Migration discipline:

- Existing `[NEEDED]` numeric / quantitative fields in PROJECT_CONTEXT files for current orgs (mycosymbiotics_cooperative, mystic_mamas, run_a_muck_farm, etc.) get migrated to KFR entries by Intake at first operator review post-v7.0.4 LOCK.
- Operator confirms each migration entry — preserves audit trail.
- PROJECT_CONTEXT.md gets edited to remove migrated fields; remaining content is narrative substance only.

## §6.1 Migration sequencing (E-05 closure)

Multi-org sequencing pinned to avoid ambiguity:

- Orgs migrate in `orgs/ORG_INDEX.md` listing order (first-listed first).
- Each org's first SP0 review post-LOCK is the migration trigger for that org.
- PROJECT_CONTEXT.md edits stage in the same operator-signed `sp0_delta` per §3.1 — the migration is one delta per org, not per fact.
- Migration is bounded to one grant cycle per org (operator can defer to a later cycle if SP0 prompts for migration during a deadline-pressed cycle); deferred migrations carry to the next cycle's SP0.

# §7. Benchmarks Register — sibling artifact

External peer benchmarks (state-average teacher retention, comparable charter enrollment, regional small-farm net-revenue median, USDA-published industry averages) are not facts about any specific org. They're external reference data shared across all orgs that need them.

New file: `vault_shared/benchmarks/register.yaml`

```yaml
schema_version: benchmarks.v1
benchmarks:
  - benchmark_id: pa_avg_teacher_retention_2025
    what: "PA state average teacher retention rate, 2025"
    value: 0.84
    unit: percentage
    source_doc: "PA Department of Education Annual Report 2025"
    source_page: 47
    source_quote: "..."
    as_of: 2025-09-30
    cadence: annual
    expiry: 2026-09-30
  - benchmark_id: usda_small_farm_net_revenue_median_2024
    what: "USDA published median net revenue, small farms <$50K gross, 2024"
    value: 12500
    unit: USD
    ...
```

KFR fact's `comparison_anchor.benchmark_id` references a Benchmarks Register entry by ID. Self-comparison anchors (this org's prior-year value) stay in the KFR fact itself. Peer benchmarks are external; sibling registry handles them.

Operator-signed at write; Sovereign Node LLC may seed common benchmarks at white-glove onboarding. Both Tilth and operators can add benchmarks; all entries audit-trailed.

## §7.1 Benchmarks Register Pydantic schema validation (E-06 closure)

Same discipline as KFR §1: Pydantic validates on every read; fail-closed on schema violation. Schema additions to make Pydantic-friendly:

- `audit_chain` field per benchmark entry (analog to KFR §1) — operator/SN-LLC signature at initial population; subsequent updates re-signed.
- `populated_by` (operator_key_id or `sn_llc_seeding_key_id`) per entry.

## §7.2 F-BENCHMARK-CONTAINS-PER-ORG-REF — Logician PRE-gate (RT-05 closure)

Workspace-shared registers are Law-3-sensitive. SN-LLC seeding is workspace-shared write; nothing in §7's prior text prevents an accidental seed where the source data is per-org. The amendment closes the gap with a deterministic gate:

**F-BENCHMARK-CONTAINS-PER-ORG-REF** fires at benchmark-write time AND at every benchmark-read by Scribe/Editor/Judge if either of the following holds:

1. `source_doc` path matches `orgs/<any-slug>/...`. (External sources only; benchmark cannot derive from any per-org vault subtree.)
2. `value` tolerance-matches a `value` in any per-org KFR (within the type-default tolerance from §4). The match check uses workspace-shared canonical-value hashing — no per-org KFR content is exposed cross-org by the gate; the gate computes a value-hash check pair only.

HIGH severity. HARD_BLOCK at write (refuses to add the benchmark); HARD_BLOCK at read (refuses to surface the benchmark to drafting seats). The second leg of the gate is the defense-in-depth catch — even if a benchmark slipped through write-time validation, the read-time check fires the moment any per-org KFR carries a tolerance-matching value.

# §8. Coherence-as-defensibility (preamble framing)

This amendment is grounded in a structural insight: **a claim traceable to KFR is low-energy to defend; an untraceable claim is high-energy and accumulates audit risk monotonically.**

When a funder follow-up asks "where does this number come from," KFR-traceable claims have source_doc + page + verbatim quote ready — defense costs zero. Fabricated or imputed claims require patching at each follow-up, and patches don't always line up; audit drift compounds across the grant lifecycle.

KFR + F-LOGICIAN-FACT-DRIFT operationalize this. The architecture makes the *true* numbers cheap to defend and the *false* numbers expensive to maintain. Truth wins on energy economics.

# §9. Curation-slot reservation for v1.x Archivist

KFR maintenance work — expiry tracking, refresh prompts at SP0, lessons.json append-only audit trail, deprecated-fact archival — is currently operator-owned in v0.1. v1.x adds the Archivist seat per v7.0.6 to take ownership of long-running curation work between grant cycles.

KFR schema reserves the curation slot:

- v0.1: operator handles KFR maintenance via SP0 review at every grant cycle
- v1.x: Archivist owns KFR maintenance + expiry tracking + lessons-delta integration; operator review at SP0 still required for delta confirmation, but Archivist surfaces the work proactively between cycles

KFR schema does NOT bake `curated_by: operator` permanently. The curation function is a named slot, not a named owner. v1.x Archivist amendment fills the slot without requiring KFR schema changes.

## §9.1 Slot transition discipline (J-06 closure)

When v1.x Archivist comes online, the curation slot transitions from operator-owned to Archivist-proposed-operator-confirmed. Discipline:

- Operator-signed migration trigger required at v1.x rollout (no automatic transition).
- Archivist-proposes / operator-applies posture preserved: F-ARCHIVIST-AUTO-APPLY-ATTEMPTED (per §15 Archivist blueprint, WS-K) carries the invariant. Archivist never silently mutates KFR.
- Operator review at SP0 still required for delta confirmation post-v1.x; Archivist surfaces the work proactively between cycles but operator confirms each delta.
- Forward-link to §15 spec (WS-K Archivist round) for full transition contract.

# §10. Composition with Cards × MyCel × Console × Judge (v0.2 + v1.x)

Per v7.0.6 + memory `project_reframer_seat_gap.md`, the reframer function — same project rendered through multiple funding grammars (Farmer / Catalyst / Cooperative / etc.) — is an emergent capability of (Card library × MyCel routing × Console parallel_compare × Judge cross-card comparison). v0.1 ships single-card carded Scribe; multi-card lights up at MyCel + Console deployment.

KFR composition guarantee: regardless of which Card routes Scribe (Farmer Card, Cooperative Card, Catalyst Card), F-LOGICIAN-FACT-DRIFT validates every framed claim against KFR. The same fact (e.g., "200 students enrolled FY25") may be Card-A-relevant or Card-B-relevant, but its underlying truth lives in one KFR entry. Cross-card framing variations don't multiply the truth surface; they multiply the dialect surface.

This means MyCel's `parallel_compare` mode loads two Cards, runs Scribe through each, and the resulting two drafts both validate against the SAME KFR entries. Judge then cross-compares which framing is strongest given fit + evidence + funder logic. The factual ground is unified.

# §11. Companion file edits (paired with this amendment)

## pipeline/blueprint/v0.1/section_04_logician.md

- New POST gate for F-LOGICIAN-FACT-DRIFT family (4 codes per §4 above)
- Tolerance config per fact-type (§4)
- SP0 freshness review integration with PRE-gate sequence — Logician's PRE checks already include `[NEEDED]` token scan; that scan extends to KFR's `pending_facts.yaml` queue and stale-fact surface

## pipeline/blueprint/v0.1/section_05_pipeline.md

- Revision loop accommodates new SP0 → KGIE → SP1 → drafting → SP2 → SP3 → SP4 chain
- SP0 invocation contract: read RFA dissection's required-fields list; query KFR for `required_for_category` + `required_for_funder` matches; surface stale + gap entries to operator; await operator-signed delta before advancing
- Intake invocation contract: BULK mode at onboarding; INCREMENTAL mode on each new document upload; pending_facts.yaml queue management

## skills/scribe-ghostwriter/SKILL.md

- Phase 1 KGIE Preflight extends with KFR cross-check: each Keyword / Geography / Identity / Experience element confirmed in KFR or marked NEEDED
- New rationalization-table row (per the anti-rationalization table I added 2026-05-08): "KFR has the value but it's close enough — round it"; counter: F-LOGICIAN-FACT-DRIFT will catch this regardless

## orgs/_TEMPLATE/

- KFR schema template at `orgs/_TEMPLATE/vault/kfr/register.yaml`
- pending_facts queue template
- Documentation for white-glove onboarding team on populating initial KFR

## vault_shared/benchmarks/

- New directory + Benchmarks Register schema template
- Sovereign Node LLC seeds common benchmarks at white-glove onboarding (state averages, USDA published medians, common funder-published rates)

# §12. What this amendment does not do

- Does not modify A1-A12.
- Does not modify Section K hardware tier mapping.
- Does not modify the Five Operating Laws or the Four Autonomy Rules.
- Does not introduce new council seats — uses v7.0.6 roster (Intake is named in v7.0.6; KFR schema integrates with Intake without modifying v7.0.6 roster).
- Does not modify the v7.0.3 substrate decision (Pydantic AI substrate stands; KFR YAML + Pydantic schema validation aligns).
- Does not modify v7.0.7 classification register or routing pattern (KFR is orthogonal — fact validity, not flow control).
- Does not specify v0.2 Data Collector or Report Generator interaction with KFR (Data Collector gathers post-award data; Report Generator pulls from collected data + KFR; full spec lives in v0.2 amendment).
- Does not specify v1.x Archivist's KFR maintenance protocols (Archivist seat spec lives in v1.x amendment; v7.0.4 reserves the curation slot only).
- Does not specify Card-level KFR integration (which fields each Card considers required for archetype-specific drafting; lives in Capital Logic Library development per ADR-001 alternatives-considered).
- Does not specify pricing-tier implications of KFR + Intake bundling.

# §13. Lock-history note + sequencing

- v7.0.1 (DRAFT): Section E.P Governance Plan Preflight — awaiting Thesis round
- v7.0.2 (SELF-LOCKED 2026-05-04): Section A textual reconciliation
- v7.0.3 (SELF-LOCKED 2026-05-08): Substrate corrective
- v7.0.6 (SCOPING DRAFT 2026-05-08, SELF-LOCK candidate): Roster
- v7.0.7 (SCOPING DRAFT 2026-05-08, requires Thesis): Beta model strategy
- **v7.0.4 (SCOPING DRAFT 2026-05-08, requires Thesis, this file)**: KFR Amendment — schema + SP0 + F-LOGICIAN-FACT-DRIFT + Intake module spec + Benchmarks Register sibling

Forward-pending:
- v7.0.5 Funder Intelligence Database + Match Database SCOPING DRAFT — composes against Archivist's curation slot (v7.0.6 reservation); KFR is orthogonal (per-org facts vs. per-funder discovered docs)

**Thesis-round priorities for v7.0.4 LOCK:**

- Editor pass: clarity of KFR schema for white-glove operator population; SP0 review surface usability
- Judge pass: rubric scoring against the architecture's stated goal (bad numbers cannot reach the funder); does F-LOGICIAN-FACT-DRIFT catch what it claims to catch?
- Red Team pass: adversarial — can an operator legitimately derive a number that drift-evades the gate? Can stale facts pass when SP0 is rushed? What's the worst-case failure where a wrong number ships?

The Red Team pass on v7.0.4 is load-bearing because the entire amendment exists to prevent bad numbers from reaching funders; any path where a wrong number can ship is a P0 architecture bug.

## §13.1 Thesis round closure (L-005 strict two-cycle)

**Cycle 1 audit** at `pipeline/validation/v7_0_4_thesis_2026-05-09/cycle_1_audit.md` filed 2026-05-09 (Cowork Opus 4.7, single-Claude per Section E carve-out, v7.0.8 precedent).

**Cycle 1 findings:** 22 total = 6 Editor (LOW × 6), 6 Judge (HIGH × 2 + MEDIUM × 3 + LOW × 1), 10 Red Team (P0 × 3 + HIGH × 3 + MEDIUM × 3 + LOW × 1). Three P0 items (RT-01 derivation chain, RT-02 tolerance tamper, RT-03 stale-fact silent drift) all addressed pre-LOCK with new failure-code subgates and structural mechanisms.

**Cycle 1 → Cycle 2 fixes applied (14 distinct fixes producing 13 new failure-code entries):**

| Finding | Fix landed in |
|---|---|
| RT-01 (P0) | §4.5 derivation chain depth limit + F-FACT-DRIFT-DERIVATION-CHAIN |
| RT-02 (P0) | §4.4 tolerance tamper-gate + F-LOGICIAN-FACT-TOLERANCE-DRIFT |
| RT-03 (P0) | §4.6 stale-acknowledged tolerance-match + F-FACT-DRIFT-EXPIRED-LANDING |
| J-01 (HIGH) | §4 currency tolerance defaults tightened to 0.5% / $2,500 floor |
| J-02 (MEDIUM) | §4.4.1 derivation key currency check + F-FACT-DRIFT-DERIVATION-KEY-RETIRED |
| J-03 = RT-04 (HIGH) | §5.2 F-EXTRACTOR-FABRICATION exact-match semantics |
| J-04 = RT-08 (HIGH) | §3.2 NEEDED hard-block + F-LOGICIAN-FACT-NEEDED-REQUIRED |
| J-05 = RT-10 (MEDIUM) | §1.2 Classification Register binding |
| J-06 (LOW) | §9.1 slot transition discipline |
| RT-05 (HIGH) | §7.2 F-BENCHMARK-CONTAINS-PER-ORG-REF |
| RT-06 (MEDIUM) | §5.3 AWARD_INGEST mode contract + F-EXTRACTOR-AWARD-SIGNATURE-INVALID |
| RT-07 (HIGH) | §1.1 F-KFR-SIGNATURE-INVALID + F-KFR-AUDIT-CHAIN-BROKEN |
| RT-09 (MEDIUM) | §4.7 derivation_id annotation mechanism |
| E-01..E-06 (LOW) | §1 schema flattening; §3.1 SP0 UX shape; §4 range-typed facts; §5 mode renames (BULK_INGEST / INCREMENTAL_INGEST); §6.1 migration sequencing; §7.1 Benchmarks Pydantic discipline |

**Cycle 2 verification** at `pipeline/validation/v7_0_4_thesis_2026-05-09/cycle_2_verification.md` filed 2026-05-09. Editor READY (zero E-01..E-06 resurfaced; zero new findings); Judge ≥85 (post-fix score 92/100); Red Team READY_TO_LOCK (zero P0/HIGH residuals; zero new P0/HIGH introduced by narrow-edit fixes; AWARD_INGEST contract closes RT-06 cleanly).

**Section E carve-out invocation:** Single-Claude (Anthropic) Thesis Cycles 1+2 per v7.0.8 precedent (lock_history row 175). Cross-family rigor (Editor=Llama 3.3 70B/Groq, Judge=Gemini-2.5-Pro/Google, Red Team=GPT-OSS-120B/Groq + GPT-5.1 escalation) DEFERRED to operator-driven re-run when multi-provider routing is live. Tracked Section E posture exception. Audit trail at `pipeline/validation/v7_0_4_thesis_2026-05-09/` enables operator-driven cross-family re-run with finding-by-finding verification.

## §13.2 Companion files edited at LOCK

Per dispatch packet §WS-C done definition:

- `pipeline/blueprint/v0.1/section_04_logician.md` — F-LOGICIAN-FACT-DRIFT family POST-gate; tolerance config; SP0 freshness review integration with PRE-gate sequence.
- `pipeline/blueprint/v0.1/section_05_pipeline.md` — SP0 stop-point + Intake invocation contract (3 modes).
- `skills/scribe-ghostwriter/SKILL.md` — Phase 1 KGIE Preflight extends with KFR cross-check (E / G / I / E elements confirmed in KFR or marked NEEDED); F-LOGICIAN-FACT-DRIFT awareness in rationalization table.
- `orgs/_TEMPLATE/vault/kfr/` — KFR schema templates (`register.yaml` template + `pending_facts.yaml` template).
- `vault_shared/benchmarks/` — Benchmarks Register sibling artifact + initial seed.
