---
title: Tilth Architecture — Amendment v7.0.8 (Customer Identity × Capital Logic orthogonality — applicant-side CIC selection + funder-side CLC assignment + structural decoupling enforcement)
filed: 2026-05-08
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-08 (single-Claude Thesis Cycles 1 + 2 cleared; cross-family rigor deferred to operator-driven re-run when multi-provider routing is live; audit trail at `pipeline/validation/v7_0_8_thesis_2026-05-08/`). Substantive architectural addition. Introduces (a) canonical CIC and CLC enums as Pydantic literal types, (b) `cic_active` field in PROJECT_CONTEXT.md (applicant-side, per-org), (c) `clc_assigned` field per opportunity in Funder Intelligence Database + Match Database (funder-side, workspace + per-org respectively), (d) FOUR new Logician PRE-gates enforcing structural decoupling (F-CIC-CLC-ENUM-DRIFT, F-CIC-CLC-COUPLING-VIOLATION, F-CIC-CLC-MATCH-NULL, F-MULTI-CIC-CHOICE-UNRESOLVED), (e) Scout VERIFY-stage delta (CLC assignment with hard-floor confidence), (f) Intake delta (CIC selection at white-glove with composition-implications surface). Cycle-1 audit found 2 HIGH (RT-01 enum drift, RT-02 regex evasion), 2 MED (RT-03 confidence floor, RT-04 multi-CIC choice), 1 LOW-resolved (RT-05), 1 LOW-new (RT-06 per-org dormancy) plus 5 documentary findings (E-01..E-05). All applied as Cycle-1 fixes. Cycle-2 verification: Editor READY, Judge PASS 98/100 ready_to_lock=true, Red Team READY zero in-scope (5 LOW out-of-scope or delegated). Cross-cuts v7.0.4 (KFR Intake substrate), v7.0.5 (Funder Intelligence DB + Match DB), v7.0.6 (roster — Scout, Intake), v7.0.7 (classification register — orthogonal to this; runs alongside).
parent_lock: pipeline/architecture/v0.1/tilth_architecture_locked.md
parent_amendment: pipeline/architecture/v0.1/architecture_v7_0_3_amendment.md
companion_amendments:
  - pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md (KFR — CIC selection lives next to KFR fact extraction at Intake)
  - pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md (Funder Intelligence DB — CLC tag is per-opportunity field; Match DB — per-match record stores both CIC active list and CLC assigned)
  - pipeline/architecture/v0.1/architecture_v7_0_6_amendment.md (roster — Scout adds CLC assignment at VERIFY; Intake adds CIC selection at white-glove)
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md (classification register — strictly orthogonal; CIC/CLC do not influence routing posture and routing posture does not influence CIC/CLC selection)
companion_files_pending_edit:
  - "CLAUDE.md (Six Customer Identity Categories block already updated 2026-05-08 PM; add §The Five Operating Laws note that orthogonality is enforced; add to What NOT to Do list)"
  - "docs/ARCHITECTURE_OVERVIEW.md (CIC × CLC orthogonality diagram; matching-is-opportunity-driven flow)"
  - "orgs/_TEMPLATE/PROJECT_CONTEXT.md (add cic_active: [...] field with the six canonical IDs documented inline)"
  - "orgs/<every existing client>/PROJECT_CONTEXT.md (one-time backfill of cic_active per Intake re-pass; until backfilled, F-CIC-CLC-MATCH-NULL is dormant per §10 below)"
  - "pipeline/seats/scribe/knowledge_packs.py (sector enum reconciliation — out of scope for v7.0.8 itself; tracked separately as the 21-file sweep)"
  - "pipeline/scout/* (DISCOVER + VERIFY stages add clc_assigned output)"
  - "pipeline/logician/gates/_clc_coupling.py (new — F-CIC-CLC-COUPLING-VIOLATION static check)"
  - "pipeline/logician/gates/_cic_clc_match.py (new — F-CIC-CLC-MATCH-NULL runtime check)"
authority_source: TILTH-CIC-REVIEW-01 drawing 2026-05-08; TILTH-CLC-00 drawing 2026-05-08; operator directive 2026-05-08 PM ("Any customer could conceivably access any capital stream. It really depends on the opportunity at hand"); operator directive 2026-05-08 PM ("lets get this wired in"); `memory/feedback_cic_clc_orthogonal.md`; `memory/project_six_launch_markets_2026-05-08.md`; `memory/project_capital_logic_cards_v9_state.md`
version_wording_discipline: "LOCKED" inside this file refers to on-disk LOCKED state at filing time. The CIC and CLC enums, the orthogonality principle, the two new Logician gates, and the schema fields are NEW; all require Thesis-round review before LOCK. The PNG cards (`assets/cards/customer_identification/*.png`) are stale at filing — operator regeneration tracked under `memory/project_six_launch_markets_2026-05-08.md` "Card regeneration TODO" — but card-level staleness is a content matter, not an architecture-LOCK blocker.
---

# Amendment intent

The 2026-05-08 PM operator directive identified a category error in earlier drafts of the Customer Identity Category cards: the "Primary Capital Logic Activations" footer band on each CIC card pre-bound a customer archetype to a CLC subset. That binding is conceptually wrong. *Any customer can conceivably access any capital stream — the opportunity at hand drives which CLC engages, not the customer archetype.*

CICs and CLCs are orthogonal axes:

- **CIC** = applicant-side configuration. Who applies, with what Operating Reality, Tilth Configuration, Evidence Signals, and Funding/Reporting Rhythm. Drives Tilth's per-applicant primitives: Search Vocabulary · Evidence Schema · Language Register · Reporting Rhythm · Capital Logic Activation (where "activation" is opportunity-time, not archetype-time).
- **CLC** = funder-side mechanism. How funding flows from a funder. Drives Tilth's per-opportunity framing: eligibility logic, stated priorities, example sources, required attachments per program rule pack.

The match is determined at runtime by the opportunity, not at design time by archetype-to-mechanism pre-binding.

Removing the binding from CLAUDE.md and the memory files (done 2026-05-08 PM) is necessary but insufficient — without structural enforcement, future drafts, knowledge packs, scoring weights, prompt templates, or PROJECT_CONTEXT schemas could reintroduce the coupling. This amendment wires the orthogonality into Tilth itself: canonical enums, separate substrate fields, two Logician gates that fail-closed on coupling violations or null matches.

# What changes

## §1. Canonical enums (Pydantic literal types)

Two closed enumerations become canonical Pydantic types. They live in `pipeline/types/identity_capital.py` (new module). This amendment establishes a new top-level package `pipeline/types/` as a sibling of `pipeline/seats/`, `pipeline/logician/`, `pipeline/scout/`, etc. — package home for cross-cutting canonical types that don't belong to any single seat or stage. The package's `__init__.py` re-exports the canonical types for convenient import (`from pipeline.types import CustomerIdentityCategory, CapitalLogicCard`). [Editor F-06 fix.]

```python
# pipeline/types/identity_capital.py

from typing import Literal

CustomerIdentityCategory = Literal[
    "food_systems",
    "educator",
    "public_agency",
    "arts_culture",
    "cooperative",
    "ecosystem_intermediary",
]

CapitalLogicCard = Literal[
    "public_purpose_works",
    "catalytic_change",
    "operating_capacity",
    "research_evidence",
    "market_access",
    "credit_underwriting",
    "sponsorship_corporate",
    "shared_assets",
]

# Display-name lookup tables (used by Editor + customer-facing copy only;
# never used in routing decisions, scoring weights, or coupling logic)
CIC_DISPLAY: dict[CustomerIdentityCategory, str] = {
    "food_systems": "Food Systems",
    "educator": "Educator",
    "public_agency": "Public Agency",
    "arts_culture": "Arts & Culture",
    "cooperative": "Cooperative",
    "ecosystem_intermediary": "Ecosystem Intermediary",
}

CLC_DISPLAY: dict[CapitalLogicCard, str] = {
    "public_purpose_works": "Public Purpose & Works",
    "catalytic_change": "Catalytic Change",
    "operating_capacity": "Operating Capacity",
    "research_evidence": "Research & Evidence",
    "market_access": "Market Access",
    "credit_underwriting": "Credit & Underwriting",
    "sponsorship_corporate": "Sponsorship & Corporate Support",
    "shared_assets": "Shared Assets",
}
```

**Sources of truth:**
- `CustomerIdentityCategory` ← TILTH-CIC-REVIEW-01 (`assets/cards/customer_identification/Customer Identification Cards.png`); per-CIC operational profile cards TILTH-CIC-01..06.
- `CapitalLogicCard` ← TILTH-CLC-00 (`assets/cards/capital_logic/Capital Logic Cards.png`); per-CLC funding-mechanism cards TILTH-CLC-01..08.

**Closed sets.** Both enums are closed. Per operator directive 2026-05-08 PM ("we need all capital logic references to come from the existing set. There will be no new ones"), CLC stays at 8. CIC stays at 6 in v0.1 — the four "additional pathways" (Inventor / Scientist / Researcher; Workforce Developer; Conservationist; Tribal / First Nations) are next-step research, not enum entries.

**Adding a new CIC or CLC requires a new architecture amendment**, not a config edit. Editing `identity_capital.py` to add an entry without an amendment is a P0 lock-violation; **F-CIC-CLC-ENUM-DRIFT** fires (per §4.0 below) at the static check. The reference hash for the canonical enum module is operator-signed at amendment LOCK time and lives in `vault_shared/canonical_enum_hashes.yaml` per BT9 audit-chain discipline.

## §2. PROJECT_CONTEXT.md schema delta — `cic_active` field (applicant-side)

Each org's PROJECT_CONTEXT.md gets a new top-level field:

```yaml
cic_active:
  - <one_or_more_of_six_canonical_ids>
cic_active_set_at: <iso8601_utc>
cic_active_set_by: <operator_signature_or_intake_module>
cic_active_set_via: white_glove_intake | operator_override | suggested_by_intake_confirmed_by_operator
```

**Multi-CIC orgs are valid.** A worker-owned food hub may be `[cooperative, food_systems]` — both seat-configurations apply when the active grant cycle's seat-configuration primitives are computed (per §6 below).

**`cic_active` is mandatory.** No grant cycle proceeds without it (per F-CIC-CLC-MATCH-NULL in §4 below).

**Operator-signed.** Per BT9 hash-chain audit discipline. Set at white-glove Intake and any subsequent operator-override is signed and ledger-recorded.

**Sector-enum reconciliation is OUT OF SCOPE for v7.0.8.** The legacy six-sector enum (workforce / education / regen_ag / urban_ag / land_community / eco_art) used in `pipeline/seats/scribe/knowledge_packs.py` and elsewhere is structurally distinct from `cic_active`. Sectors describe *kind of work*; CICs describe *who applies*. The 21-file sector-enum sweep (logged in `memory/project_six_launch_markets_2026-05-08.md`) proceeds on its own track. v7.0.8 does NOT require sector enum changes; the two coexist until the sector enum is separately retired or remapped.

## §3. Funder Intelligence Database + Match Database schema deltas — `clc_assigned` (funder-side)

Per v7.0.5 (Funder Intelligence Database + Match Database), v7.0.8 adds the following fields. **Schema fragments below are illustrative for amendment-review purposes; final Pydantic field names land in v7.0.5's schema PR composing with this amendment's spec.** [Editor F-07 fix.]

**Funder Intelligence Database** (workspace-shared, Law-3-safe — funder-side data, no client info):

```yaml
# Per-opportunity record extension
clc_assigned: <one_of_eight_canonical_ids>
clc_assignment_confidence: <float 0.0-1.0>
clc_assignment_rationale: <string — how Scout VERIFY identified this CLC; cites synopsis text + program-rule-pack signals>
clc_assignment_at: <iso8601_utc>
clc_assignment_by: scout_verify_stage | operator_override
clc_assignment_provenance: <hash of source synopsis + program rule pack version>
```

**Match Database** (per-org, Law-3-isolated — applicant × opportunity reasoning trail):

```yaml
# Per-match record (Scout-discovered opportunity × this org's PROJECT_CONTEXT)
match_id: <opportunity_hash>__<org_slug>
opportunity_clc_assigned: <inherited from Funder Intelligence DB>
applicant_cic_active: [<one_or_more_of_six>]   # snapshotted at match time
fit_score: <Scout's fit assessment>
fit_rationale: <string — why this opportunity fits this applicant>
seat_configuration_resolved: 
  search_vocabulary: <derived from applicant_cic_active>
  evidence_schema: <derived from applicant_cic_active>
  language_register: <derived from applicant_cic_active>
  reporting_rhythm: <derived from applicant_cic_active>
funder_framing_resolved:
  eligibility_logic: <derived from opportunity_clc_assigned>
  stated_priorities: <from synopsis + program rule pack>
  example_sources: <from CLC's example_sources list>
  required_attachments: <from program rule pack>
```

**Critical invariant — Match record fields stay independent.** `opportunity_clc_assigned` is derived from the opportunity, not the applicant. `applicant_cic_active` is derived from the applicant, not the opportunity. The two fields are independent inputs. There is no field that encodes "is this CIC × CLC pair allowed" — the answer is always "yes in principle; fit_score is the operational signal."

## §4. New Logician PRE-gates

### §4.0 F-CIC-CLC-ENUM-DRIFT (PRE, static, fires earliest of the four gates) [NEW per Cycle-1 RT-01 / F-01 fix]

**Fires at:** Tilth startup AND on every reload of `pipeline/types/identity_capital.py`.

**Detects:** any drift in the canonical enum module from its operator-signed reference state. Two checks:

1. **Hash check.** SHA3-512 of `pipeline/types/identity_capital.py` against the value in `vault_shared/canonical_enum_hashes.yaml`. The reference hash is operator-signed (Ed25519 + ML-DSA-65 hybrid per A12 crypto-agility) at amendment LOCK time and at any amendment that intentionally modifies the enum.
2. **Count check.** `len(CustomerIdentityCategory.__args__)` MUST equal 6 AND `len(CapitalLogicCard.__args__)` MUST equal 8. Counts are also validated against the values declared in this amendment file's text (parser pulls the canonical counts from `architecture_v7_0_8_amendment.md` §1 to defend against amendment-text/code drift).

**Fail mode:** fail-closed. Tilth refuses to start. `F-CIC-CLC-ENUM-DRIFT` ledger entry, HIGH severity, operator escalation. Subcodes:

- `F-CIC-CLC-ENUM-DRIFT.hash_mismatch` — file hash differs from signed reference (file was edited)
- `F-CIC-CLC-ENUM-DRIFT.signature_invalid` — reference hash signature failed verification (vault tampered or key rotation incomplete)
- `F-CIC-CLC-ENUM-DRIFT.count_cic` — `CustomerIdentityCategory` arg count != 6
- `F-CIC-CLC-ENUM-DRIFT.count_clc` — `CapitalLogicCard` arg count != 8

**Recovery:** legitimate enum modification (e.g., adding a 7th CIC after the four "additional pathways" research lands) requires (a) a new architecture amendment that resolves §1 closed-set discipline, (b) operator re-signing of `vault_shared/canonical_enum_hashes.yaml` against the new module, (c) Cycle-2 verification of the new amendment. Until all three complete, enum drift is fail-closed.

**Why earliest:** RT-01 (Cycle 1 Red Team) showed that coupling-violation detection (§4.1) does not catch closed-set drift in the canonical enum itself. Enum drift is the pre-condition for every other identity/capital invariant; it gates earliest in the PRE order.

### §4.1 F-CIC-CLC-COUPLING-VIOLATION (PRE, static check) [STRENGTHENED per Cycle-1 RT-02 / F-02 fix]

**Fires at:** Tilth startup AND on any config refresh (router.yaml reload, knowledge-pack reload, PROJECT_CONTEXT.md edit, prompt-template recompile).

**Detects:** any code path, schema, prompt template, knowledge pack, scoring weight, or config that encodes a CIC→CLC subset binding. **Detection runs four layers; any layer's match trips the gate.**

**Layer 1 — Lexical pattern (regex on field/function names; primary detection, not exclusive).**

- Any field name in PROJECT_CONTEXT.md or any vault file matching the regex `^(primary|preferred|allowed|activated|enabled|valid)_(capital_logic|clc).*$`
- Any function in `pipeline/seats/*` or `pipeline/logician/*` whose signature includes both `cic` and `clc` as inputs and returns a boolean (would imply coupling validation)
- Any prompt template in `pipeline/seats/*/prompts/` that interpolates both `{{cic_active}}` and `{{clc_subset}}` (or any `{{*_clc_*}}` matching the field-name regex above) in the same template

**Layer 2 — Pydantic AST inspection (catches structural coupling regardless of field name).**

Static AST walk over all files matching `pipeline/**/*.py`. Flags any Pydantic model field whose annotation is structurally-equivalent to `Mapping[CustomerIdentityCategory, Collection[CapitalLogicCard]]` — including but not limited to:

- `dict[CustomerIdentityCategory, list[CapitalLogicCard]]`
- `dict[CustomerIdentityCategory, set[CapitalLogicCard]]`
- `Mapping[CustomerIdentityCategory, Sequence[CapitalLogicCard]]`
- Any `dict`/`Mapping` with key type matching `CustomerIdentityCategory` or its alias and value type that resolves to a collection of `CapitalLogicCard` or its alias
- The reverse direction (`dict[CapitalLogicCard, Collection[CustomerIdentityCategory]]`) — also forbidden, same coupling

**Layer 3 — Value-set check (catches creative renamings whose values are subset of canonical enums).**

For every YAML file under `vault_shared/`, `orgs/<slug>/`, `pipeline/knowledge_packs/`, and `vault_*/`, and every Pydantic schema, check every list-typed field. If a field's value-list is a non-empty strict subset of `CapitalLogicCard.__args__` (e.g., `funding_streams: [public_purpose, operating_capacity]`) AND that field appears in a context keyed by CIC (per-CIC config file, knowledge-pack-per-CIC subdirectory, or alongside a `cic_active`-bearing record), the gate trips. Same applies symmetrically to CIC subset under CLC keying.

This catches the §11.2 evasion pattern from Cycle 1 Red Team where an adversary renames `primary_clc` to `funding_streams` to avoid Layer 1's regex.

**Layer 4 — Knowledge-pack schema validation.**

The knowledge-pack YAML schema (Pydantic model `KnowledgePackManifest`) explicitly forbids any top-level field whose annotation includes `CapitalLogicCard` or its alias. Knowledge packs may carry CIC tags (a knowledge pack is allowed to be tagged "applies to Educator") but may NOT carry CLC eligibility lists (a knowledge pack may NOT say "applies only to Catalytic Change opportunities"). Any forbidden field is a schema-validation failure at pack load time, which surfaces as F-CIC-CLC-COUPLING-VIOLATION.

**Fail mode:** fail-closed. Tilth refuses to start. F-CIC-CLC-COUPLING-VIOLATION ledger entry, HIGH severity, operator escalation. Detection rationale (which layer caught it) + offending file path + line number surface to operator for fix.

**Recovery:** offending coupling is removed; static check passes; Tilth starts.

**Why static, not runtime:** coupling violations are design-time bugs, not data-time anomalies. They get caught before any grant cycle starts, not during one.

### §4.2 F-CIC-CLC-MATCH-NULL (PRE, runtime check) [CLARIFIED per Cycle-1 E-04 fix]

**Fires at:** start of every grant cycle, before any seat invocation; also at any seat invocation that reads either field if the cycle was somehow entered without them set.

**Detects:** either (a) `PROJECT_CONTEXT.cic_active` is unset, empty, or contains an ID not in `CustomerIdentityCategory`, OR (b) the active opportunity's `clc_assigned` is unset, empty, or contains an ID not in `CapitalLogicCard`.

**Fail mode:** fail-closed *after the per-org migration dormancy expires per §10*. During the dormancy window for a given org, this gate emits WARNING logs (admin-risk LOW severity ledger entry) but does NOT block the grant cycle. Once dormancy expires for that org, fail-closed is enforced and the pipeline halts before Scribe or any other seat sees the input. Specific failure subcode names which side is missing:

- `F-CIC-CLC-MATCH-NULL.cic_unset` — applicant CIC not selected (Intake hasn't run, or operator didn't sign off, or PROJECT_CONTEXT.md is malformed)
- `F-CIC-CLC-MATCH-NULL.cic_invalid` — applicant CIC contains a non-canonical ID
- `F-CIC-CLC-MATCH-NULL.clc_unset` — opportunity CLC not assigned (Scout VERIFY hasn't run, or assigned with confidence below threshold)
- `F-CIC-CLC-MATCH-NULL.clc_invalid` — opportunity CLC contains a non-canonical ID

**Recovery:** operator runs Intake (for cic_*) or Scout VERIFY (for clc_*); pipeline resumes.

**Why runtime, not static:** match-null is a per-cycle data condition. It catches "Intake hasn't been re-run for this org since the cic_active field was added," "Scout's CLC assignment dropped below confidence threshold," "operator manually invalidated the assignment for this cycle and needs to re-confirm."

### §4.3 F-MULTI-CIC-CHOICE-UNRESOLVED (PRE, runtime check at seat-config resolution) [NEW per Cycle-1 RT-04 / F-04 fix]

**Fires at:** seat-configuration resolution time, per-grant, when an applicant has multi-CIC `cic_active` and the §7 composition encounters a select-one primitive (Language Register / narrative voice / tone) without operator selection for the active grant.

**Detects:** §7's composition encounters a primitive type whose composition rule is `select-one-per-grant` (per the v7.0.8 §7 fix below) AND the active grant's PROJECT_CONTEXT does not carry an operator-set selection in the per-grant `match_overrides:` block.

**Fail mode:** fail-closed. Pipeline halts at seat-config resolution, before Scribe is invoked. Operator must select per-grant via SP0 review or a `match_overrides:` block edit; pipeline resumes.

**Why runtime per-grant, not at Intake:** the choice may legitimately differ per grant — a multi-CIC `[educator, food_systems]` org may want academic-formal voice for an NIH grant and agricultural-plainspoken voice for a USDA grant. Forcing a single static choice at Intake would over-constrain.

### §4.4 Gate ordering

In v7's PRE-gate precedence table (locked architecture §Cycle-2 PRE-gate precedence ordering), the four new gates insert as follows:

| Order | Gate | Scope |
|---|---|---|
| 6 | F-SECTION-R-INCOMPLETE, F-TDSL-LEAK-V01 | Architecture structural invariants |
| **6.45** | **F-CIC-CLC-ENUM-DRIFT** | **Canonical enum integrity (static; pre-condition for everything else)** |
| **6.5** | **F-CIC-CLC-COUPLING-VIOLATION** | **CIC × CLC structural decoupling (static, four detection layers)** |
| **6.6** | **F-CIC-CLC-MATCH-NULL** | **CIC × CLC runtime presence (per-cycle, post-dormancy)** |
| **6.7** | **F-MULTI-CIC-CHOICE-UNRESOLVED** | **Multi-CIC select-one-per-grant resolution (per-grant)** |
| 7 | F-CONTEXT-PLACEMENT | Per-seat prompt template structure |

Enum-drift fires earliest — every other identity/capital invariant assumes the canonical enum is intact. Coupling violation fires next — design-time bug. Match-null fires after coupling-clean is confirmed. Multi-CIC choice resolution fires last among the four — only relevant for multi-CIC orgs with grants in flight.

## §5. Scout DISCOVER + VERIFY deltas (delegates to Section 3 Scout v5.x blueprint)

**DISCOVER stage** (channel families A-G per v7.0.5): no change to channel logic, but each candidate opportunity record now carries a tentative `clc_assigned_provisional` field set by the LLM-based DISCOVER pass. Provisional assignments do NOT enter Funder Intelligence DB; they're scratch state.

**VERIFY stage**: when an opportunity is elevated from candidate to verified, Scout computes the canonical `clc_assigned` value:

1. Fetch live synopsis (per existing VERIFY discipline — Grants.gov fetchOpportunity / SAM.gov / state portal scrape).
2. Match synopsis against canonical CLC `description` and `example_sources` fields from TILTH-CLC-00.
3. Compute confidence (top-1 score / sum-of-all-scores, with calibration against held-out labeled set).
4. If confidence ≥ threshold (provisional 0.70, operator-tunable per `vault_shared/scout_config.yaml`), assign `clc_assigned` and store with provenance hash.
5. If confidence < threshold, mark as `clc_assigned: null` and surface to operator for manual assignment in REVIEW.

**REVIEW (operator)** can override Scout's CLC assignment. Operator override is ledger-recorded; the override + rationale travel into the Match DB record's `clc_assignment_rationale` field.

**Performance budget for VERIFY's CLC step:** ≤ 2 seconds per opportunity on baseline hardware. Implementation note: structured-output Pydantic AI call against the active Scout-tier model (per router.yaml); Logician validates output structure POST.

**Confidence threshold hard floor (per Cycle-1 RT-03 / F-03 fix):** the operator-tunable threshold has a HARD FLOOR of 0.50. Operator override below 0.50 is NOT allowed via standard config edit; below-floor override requires (a) operator signature on the override entry (Ed25519 + ML-DSA-65 hybrid per A12), (b) HIGH-severity admin-risk ledger entry per BT9 audit-chain discipline, (c) explicit time-bounded TTL on the below-floor setting (default 30 days, max 90 days). Without all three, attempting to set threshold < 0.50 fails-closed at config validation. Default value stays 0.70.

## §6. Intake CIC selection (delegates to v7.0.6 Intake module spec + v7.0.4 KFR substrate)

**White-glove Intake** (per v7.0.6 + v7.0.4) gains a CIC Selection step:

1. **Inventory.** Intake presents the operator with the six canonical CICs + their tagline + their `Includes` sub-categories (per CLAUDE.md § Six Customer Identity Categories).
2. **Suggest.** Intake's BULK-mode extraction over the org's documents may suggest one or more CICs based on document signal (e.g., school-district board minutes suggest `educator`; cooperative bylaws suggest `cooperative`; combined signals suggest multi-CIC). Suggestions cite verbatim quote with provenance per v7.0.4 F-EXTRACTOR-FABRICATION discipline.
3. **Operator confirm or override.** Operator selects one or more `CustomerIdentityCategory` IDs. Multi-select valid.
4. **Composition implications surface (per Cycle-1 E-05 / F-10 fix).** When operator selects multi-CIC at step 3, Intake immediately surfaces the §7 composition rule the operator is opting into: which primitives merge by union, which take most-stringent, which require per-grant select-one resolution (and will trip F-MULTI-CIC-CHOICE-UNRESOLVED on every grant cycle until operator resolves them via `match_overrides:`). Operator confirms the multi-CIC composition profile is understood + acceptable, OR backs out to single-CIC, before proceeding to step 5.
5. **Sign and persist.** PROJECT_CONTEXT.md `cic_active` field populated; operator signature recorded; ledger entry filed.

**CIC selection precedes Classification Review** (v7.0.7) — CIC active list informs the Card-archetype default classifications. The two stages are sequential at white-glove.

**CIC change post-onboarding** is allowed but requires operator signature + ledger entry. Use case: org evolves (e.g., a Food Systems farm forms a co-op and now needs `[food_systems, cooperative]`).

## §7. Seat-configuration resolution at draft time

When the council pipeline activates for a given (applicant, opportunity) pair, seat-configuration primitives resolve as follows:

```python
def resolve_seat_config(
    applicant_cic_active: list[CustomerIdentityCategory],  # from PROJECT_CONTEXT
    opportunity_clc_assigned: CapitalLogicCard,             # from Match DB
) -> SeatConfig:
    """Composes applicant-side primitives from CIC; funder-side framing from CLC.

    These two streams are INDEPENDENT inputs. There is no function in this
    pipeline that takes (cic, clc) and returns a 'is this allowed' boolean.
    """

    # Applicant-side (from CIC) — seat operational primitives
    applicant_side = compose_applicant_primitives(applicant_cic_active)
    # Returns: search_vocabulary, evidence_schema, language_register,
    #          reporting_rhythm — each derived from CIC operational profile

    # Funder-side (from CLC) — opportunity framing
    funder_side = compose_funder_framing(opportunity_clc_assigned)
    # Returns: eligibility_logic, stated_priorities, example_sources,
    #          required_attachments — each derived from CLC mechanism

    return SeatConfig(applicant=applicant_side, funder=funder_side)
```

**Multi-CIC composition rule** (when applicant has multiple `cic_active` IDs) — **three composition modes per primitive type, not two** [updated per Cycle-1 RT-04 / F-04 fix]:

1. **Identical across all active CICs.** Use directly.
2. **`union` mode — for additive primitives.** Search Vocabulary unions; Evidence Schema requires union (applicant must satisfy all schemas).
3. **`most-stringent` mode — for posture primitives.** Reporting Rhythm = highest cadence; data sensitivity = strictest classification.
4. **`select-one-per-grant` mode — for choice primitives** (Language Register, narrative voice, tone, register dialect). No automatic resolution; operator must select per-grant via SP0 review or `match_overrides:` block in PROJECT_CONTEXT for the active grant. F-MULTI-CIC-CHOICE-UNRESOLVED PRE-gate (§4.3) fires fail-closed at seat-config resolution if a select-one primitive lacks operator selection for the active grant.
5. **Per-grant operator override available across all modes** via `match_overrides:` block — useful when one CIC dominates for a particular opportunity, or when a select-one resolution differs from the typical pattern.

**Primitive-to-mode mapping** (per primitive type):

| Primitive | Composition mode | Rationale |
|---|---|---|
| Search Vocabulary | `union` | Additive — broader vocabulary helps Scout find more relevant opportunities |
| Evidence Schema | `union` | Additive — applicant must satisfy all evidence requirements across CICs |
| Reporting Rhythm | `most-stringent` | Posture — highest cadence wins; faster reporting always satisfies slower |
| Language Register | `select-one-per-grant` | Choice — academic-formal vs agricultural-plainspoken cannot blend; operator selects per-grant |
| narrative voice / tone | `select-one-per-grant` | Choice — same reason as Language Register |
| Capital Logic Activation | N/A — driven by opportunity, not CIC | This primitive is opportunity-driven (per the orthogonality principle); no CIC-level composition needed |

**No multi-CLC composition.** An opportunity belongs to exactly one CLC at a time. Edge cases (e.g., an RFA that funds market access AND research) get assigned the dominant CLC by Scout VERIFY; operator override available.

## §8. What this amendment does not do

- Does not pre-bind CIC to CLC subset. Does not introduce any "primary activations" list. Does not add any field that encodes (CIC → allowed CLCs) or (CLC → eligible CICs).
- Does not introduce a 9th CLC. The set is closed at 8 (per operator directive 2026-05-08 PM).
- Does not introduce a 7th CIC. The set is closed at 6 in v0.1 (the four "additional pathways" are next-step research per `memory/project_six_launch_markets_2026-05-08.md`).
- Does not retire the legacy sector enum. Sector enum reconciliation is on a separate track (the 21-file sweep). v7.0.8 enum (`CustomerIdentityCategory`) and the legacy sector enum coexist until separately reconciled.
- Does not modify routing posture (v7.0.7 territory). CIC and routing posture are orthogonal — a `food_systems` org may run any classification posture; an `educator` org may run any classification posture.
- Does not modify the council seat roster (v7.0.6 territory).
- Does not modify the Five Operating Laws or A1-A12.
- Does not specify the exact mapping from CIC to operational primitives (Search Vocabulary content, Evidence Schema content, etc.) — that lives in the per-CIC operational profile cards (TILTH-CIC-01..06) and the corresponding blueprint sections that compose against them. v7.0.8 wires the architecture; the per-CIC content lives in cards + blueprint.
- Does not specify the exact mapping from CLC to funder-side framing (eligibility logic content, stated-priorities content, etc.) — that lives in the per-CLC operational profile cards (TILTH-CLC-01..08) and the program rule packs.
- Does not modify the KFR schema or fact validity model (v7.0.4 territory). CIC selection composes against KFR but stays orthogonal to KFR's per-fact freshness/provenance discipline.
- Does not modify the Funder Intelligence DB or Match DB schemas beyond the two new fields specified in §3 (v7.0.5 territory).

## §9. Failure-code primitives added

**Four new failure codes** (total at v7.0.8 = 34: A1-A12 thirty + v7.0.4 KFR codes pending + v7.0.5 funder-DB codes pending + v7.0.7 classification codes pending + v7.0.8 four):

- **F-CIC-CLC-ENUM-DRIFT** (PRE, static, fail-closed at PRE-gate order 6.45) — canonical enum module hash drift OR signed-reference signature failure OR arg count != 6 (CIC) / != 8 (CLC). HIGH severity. Subcodes: `.hash_mismatch`, `.signature_invalid`, `.count_cic`, `.count_clc`. Recovery requires new architecture amendment + operator re-sign + Cycle-2 verification. [NEW per Cycle-1 RT-01.]
- **F-CIC-CLC-COUPLING-VIOLATION** (PRE, static, fail-closed at PRE-gate order 6.5) — code path/schema/template encodes CIC→CLC subset binding. Detection runs four layers: lexical regex (Layer 1), Pydantic AST (Layer 2), value-set check (Layer 3), knowledge-pack schema validation (Layer 4). Any layer's match trips the gate. HIGH severity. Operator escalation. [STRENGTHENED per Cycle-1 RT-02.]
- **F-CIC-CLC-MATCH-NULL** (PRE, runtime, fail-closed at PRE-gate order 6.6 *after per-org dormancy expires*) — applicant CIC or opportunity CLC unset/invalid at cycle start. Subcodes: `.cic_unset`, `.cic_invalid`, `.clc_unset`, `.clc_invalid`. Recovery via Intake or Scout VERIFY rerun. [CLARIFIED per Cycle-1 E-04.]
- **F-MULTI-CIC-CHOICE-UNRESOLVED** (PRE, runtime, fail-closed at PRE-gate order 6.7) — multi-CIC org's `cic_active` triggers a select-one-per-grant primitive without operator selection in `match_overrides:` for the active grant. Recovery via per-grant operator selection. [NEW per Cycle-1 RT-04.]

Zero new Cedar rules (deterministic Python suffices for all four gates).

Zero new M-family mechanisms.

Zero new admin-risk register entries (existing BT9 audit-chain discipline carries the operator-signature workflow for enum-drift recovery and below-floor confidence overrides per §5).

## §10. Migration path for existing orgs (one-time backfill)

At amendment LOCK, every existing client folder under `orgs/` carries a PROJECT_CONTEXT.md without a `cic_active` field. F-CIC-CLC-MATCH-NULL would fail-closed every grant cycle for every org until backfilled.

**Migration discipline (per-org dormancy clock — fixed per Cycle-1 RT-06 / F-05):**

1. **F-CIC-CLC-MATCH-NULL is dormant per-org for 14 calendar days starting at the org's first attempted grant cycle post-LOCK** — NOT workspace-wide from LOCK time. Each org gets its own 14-day window from its first cycle attempt. This respects Law 3 (per-org isolation) and avoids the failure mode where a monthly-cadence org hits fail-closed at day 15+ without operator-visible warning windows.
2. **During the per-org dormancy window**, the gate emits WARNING logs (admin-risk LOW severity ledger entry) per cycle attempt, surfacing the missing-input condition to operator without blocking the cycle.
3. **Within the org's 14-day window, operator runs Intake CIC Selection (§6) for that client.** Adds `cic_active` to PROJECT_CONTEXT.md. Operator-signed.
4. **At the org's day 14, F-CIC-CLC-MATCH-NULL becomes fail-closed for that org.** Any subsequent grant cycle without `cic_active` halts at PRE-gate; operator fixes by running CIC Selection.
5. **For Scout's `clc_assigned` backfill on existing Funder Intelligence DB records:** Scout runs a one-shot REVERIFY pass over the existing corpus once (workspace-wide, not per-org — funder corpus is shared). Computes `clc_assigned` for each record. Records below confidence threshold (≥ 0.50 per §5 hard floor; default 0.70) surface to operator for manual REVIEW. Backfill kicked off at LOCK; runs in background.

The per-org dormancy window is tracked in `orgs/<slug>/vault/migration_state.yaml:: f_cic_clc_match_null.first_attempt_iso8601` and `f_cic_clc_match_null.dormancy_expires_iso8601`. Operator-extendable per the standard admin-risk dormancy-extension procedure (HIGH-severity ledger entry required for extension beyond 30 days).

## §11. Lock-history note + sequencing

- v7.0.1 (DRAFT): Section E.P Governance Plan Preflight — awaiting Thesis round before LOCK
- v7.0.2 (SELF-LOCKED 2026-05-04): Section A textual reconciliation
- v7.0.3 (SELF-LOCKED 2026-05-08): Substrate corrective (Pydantic AI absorbs LangGraph + OpenClaw)
- v7.0.4 (SCOPING DRAFT 2026-05-08): KFR Amendment — per-org structured quantitative substrate
- v7.0.5 (SCOPING DRAFT 2026-05-08): Funder Intelligence Database + Match Database
- v7.0.6 (SCOPING DRAFT 2026-05-08, SELF-LOCK candidate): Roster — Red Team surfaced + Intake / Uploader added + v0.2 / v1.x slots reserved
- v7.0.7 (SCOPING DRAFT 2026-05-08): Beta model strategy — classification-driven routing
- **v7.0.8 (SCOPING DRAFT 2026-05-08, this file, requires Thesis round before LOCK)**: Customer Identity × Capital Logic orthogonality — applicant-side CIC + funder-side CLC + structural decoupling enforcement

**Sequencing relative to v7.0.4 / v7.0.5 / v7.0.6 / v7.0.7:**

v7.0.8 composes against all four but does not block any of them:

- **v7.0.4 (KFR)**: CIC selection lives at Intake alongside KFR fact extraction. Both populate PROJECT_CONTEXT.md. Independent fields. v7.0.4 LOCK is not blocked by v7.0.8; v7.0.8 LOCK is not blocked by v7.0.4. Joint LOCK convenient if Thesis rounds align.
- **v7.0.5 (Funder Intelligence DB + Match DB)**: `clc_assigned` per opportunity is a v7.0.5 schema field with v7.0.8 semantics. v7.0.5 must add the field name; v7.0.8 specifies how it gets populated and what constraints apply. Joint LOCK strongly preferred.
- **v7.0.6 (Roster)**: Scout adds CLC assignment at VERIFY; Intake adds CIC selection at white-glove. v7.0.6 names the support agents; v7.0.8 specifies a step in each. Joint LOCK convenient.
- **v7.0.7 (Classification register)**: strictly orthogonal. CIC/CLC do not influence routing posture; routing posture does not influence CIC/CLC. The two amendments don't interact at the substrate level. Independent LOCK paths fine.

**Thesis-round preparation (for v7.0.8 LOCK):**

- **Editor pass**: clarity of CIC/CLC enums; clarity of the `cic_active` and `clc_assigned` schemas; clarity of the orthogonality principle for someone reading just this amendment without prior context.
- **Judge pass**: rubric scoring against the architecture's stated goal — does the structural decoupling actually enforce orthogonality, or does it leave a back-channel? Specifically: can a knowledge pack, a Cedar rule, a router config, or a seat prompt sneak in a CIC→CLC binding without F-CIC-CLC-COUPLING-VIOLATION catching it?
- **Red Team pass**: adversarial. Worst-case scenarios:
  1. An operator maliciously edits `pipeline/types/identity_capital.py` to add a 9th CLC. Does F-CIC-CLC-COUPLING-VIOLATION catch the add at startup? (It should — adding to a closed enum without a corresponding amendment is a coupling violation by definition.)
  2. A knowledge pack lists a CLC field but uses different wording (e.g., `funding_streams: [public_purpose]`) to evade the regex check in §4.1. What's the detection?
  3. Scout's CLC confidence threshold is set too low (operator over-tunes) and noise CLC assignments get accepted. What's the calibration discipline?
  4. Multi-CIC composition produces seat configurations that contradict each other (e.g., one CIC says "narrative voice formal" and another says "narrative voice plainspoken"). What's the conflict-resolution path beyond §7's union/most-stringent rules?
  5. A grant cycle starts with `cic_active: [educator]` but the opportunity's CLC is `sponsorship_corporate` — the seat configuration produces a draft that sounds nothing like an educator-sponsorship grant should. How does Editor + Judge + Red Team catch this without falling back to "educator can't access sponsorship," which is the binding we're forbidding?

The Red Team pass is critical — orthogonality is a load-bearing claim and any back-channel that re-couples CIC and CLC undoes the architectural commitment.

**Companion file edits batch** (lands when v7.0.8 LOCKs, can land alongside v7.0.4/v7.0.5/v7.0.6/v7.0.7 batches):

- CLAUDE.md (already updated 2026-05-08 PM with the orthogonality language; add cross-reference to v7.0.8 in the "What NOT to Do" section: "Do not encode any CIC→CLC subset binding in any code, schema, prompt, or knowledge pack — F-CIC-CLC-COUPLING-VIOLATION enforces fail-closed.")
- docs/ARCHITECTURE_OVERVIEW.md (CIC × CLC orthogonality diagram; matching-is-opportunity-driven flow)
- orgs/_TEMPLATE/PROJECT_CONTEXT.md (add `cic_active: [...]` field with the six canonical IDs documented inline)
- pipeline/types/identity_capital.py (new module — the canonical enums + display tables)
- pipeline/logician/gates/_clc_coupling.py (new — F-CIC-CLC-COUPLING-VIOLATION static check)
- pipeline/logician/gates/_cic_clc_match.py (new — F-CIC-CLC-MATCH-NULL runtime check)
- pipeline/scout/verify.py (CLC assignment step at VERIFY)
- pipeline/intake/cic_selection.py (new step in Intake's white-glove flow per v7.0.6)

The 21-file sector-enum sweep is OUT OF SCOPE for this amendment and lands separately.
