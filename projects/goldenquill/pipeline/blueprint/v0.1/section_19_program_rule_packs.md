# §19 — Program Rule Packs (PRPs)

**Status:** DRAFT (v0.1 scaffold). NOT LOCKED. No paired-commit to §0.5
fires at v0.1 because this section is DRAFT, not LOCKED. The §0.5
paired-commit will fire later when §19 graduates to LOCKED at the v0.2
first-wave ceremony.

**Authored:** 2026-05-17.
**Operator authorization:** post docx review of
`docs/phased_card_system_research_audit_extracted_2026-05-17.md`.

---

## 19.1 Purpose

Program Rule Packs (PRPs) are a new data category in the Golden Quill / Tilth
pipeline. A PRP encodes **live law**: the rules that a published funding
program, a federal regulation, or a domain compliance framework asserts at
a given moment in time, with explicit `effective_date` and `expiry_date`
bounds.

PRPs exist because the system currently has no clean place to put time-bounded
regulatory truth. CIC cards encode durable customer-identity grammar — the
patterns by which a Food Systems applicant, an Educator applicant, a
Cooperative applicant present themselves across years. CLC cards encode
durable capital-logic grammar — the patterns by which Public Purpose Works
funding, Catalytic Change funding, Credit Underwriting flow across years.
Both card families describe durable patterns and carry no expiry date.

Live law is structurally different. A NOFO publishes on a date and closes on
a date. Davis-Bacon's $2,000 covered-contract threshold is fixed today but is
amendable by Congress. BABA effective May 14, 2022 is a hard boundary. The
five environmental-review classifications under 24 CFR Part 58 are stable
today but could be reorganized by a future rulemaking. Encoding that kind of
content inside a card would couple the card's durable grammar to a moving
regulatory floor and would lose the audit-trail required to answer "what
rules did the system enforce on date X?".

PRPs hold that content. The system loads the active PRPs at runtime, verifies
each is in-window, and exposes the live-law rules to the Intake (§11),
Scribe (§7), and Logician (§4) seats as a separate channel from card content.

## 19.2 Distinction from CICs and CLCs

| Property | CIC / CLC card | PRP |
|---|---|---|
| What it encodes | Durable funder-population grammar | Live law (program rules, regulations, compliance frameworks) |
| Time bounds | None | `effective_date` required; `expiry_date` nullable |
| Loader | `pipeline/cards/loader.py` | `pipeline/program_rule_packs/loader.py` |
| Manifest | `pipeline/cards/registry.yaml` | `pipeline/program_rule_packs/_manifest/active_prps.yaml` |
| Publisher pubkey | `vault_shared/cards/publisher_pubkey.signed.yaml` | `vault_shared/program_rule_packs/publisher_pubkey.signed.yaml` |
| CIC × CLC coupling fields | Forbidden | Forbidden |
| Private-org data | Forbidden (Law 3) | Forbidden (Law 3) |
| Lifecycle states | draft, review_passed, signed, deprecated | draft, review_passed, signed, deprecated |
| Signature chain | Ed25519, operator-controlled | Ed25519, operator-controlled (separate key) |

The two loader families share lifecycle/signing/manifest-binding discipline
byte-for-byte. They are deliberately separable so the operator may delegate
PRP authorship (regulatory research) without delegating card authorship
(funder grammar curation).

PRPs MUST NOT carry CIC × CLC coupling fields, MUST NOT contain
private-organization-data fields, and MUST NOT inline card content. CIC and
CLC cards MUST NOT inline PRP content. The two channels meet only at the
seats — Intake, Scribe, Logician — that consume both.

## 19.3 Lifecycle discipline

PRP lifecycle truth mirrors card lifecycle truth (§18) exactly:

  1. A PRP is authored as a YAML body and placed on disk under
     `pipeline/program_rule_packs/<prp_kind>/<slug>.yaml`. At this point
     `lifecycle.draft_status` is `draft` and `lifecycle.runtime_loadable` is
     `false`.
  2. The PRP is reviewed (manual review for v0.2 first wave; structured
     review at later phases). `draft_status` transitions to `review_passed`.
  3. At a LOCK ceremony, the operator signs the PRP's canonical-JSON bytes
     with the prp-publisher Ed25519 key. `draft_status` transitions to
     `signed`. `signed_at`, `signed_by`, and `content_hash` populate.
  4. The PRP is added to
     `pipeline/program_rule_packs/_manifest/active_prps.yaml` with
     `status: signed` and `required_runtime_loadable: true`.
  5. At loader startup, the active manifest is read and each entry is
     validated by the seven F-PRP-* gates in §19.4 order.

A PRP whose `draft_status` is not `signed` MUST NOT be runtime-loadable. A
PRP whose effective window does not contain today MUST NOT be
runtime-loadable. These two invariants together define the live-law
boundary.

## 19.4 The F-PRP-* gate family

The PRP loader at `pipeline/program_rule_packs/loader.py` defines seven
fail-closed primitive gates. The names mirror the F-CARDS-* family on the
cards side so that the Logician (§4) can compose them into the same kind of
preflight invariants. At v0.1 DRAFT all gate bodies raise
`NotImplementedError("v0.2 first wave")` and the top-level
`load_active_prps()` itself raises `NotImplementedError` so any seat that
wires PRP loading before v0.2 first wave fails-closed with a clear refusal.

Order matters — this is the order in which gates run at v0.2 first wave:

  1. **F-PRP-NOT-IN-ACTIVE-MANIFEST** — the PRP file on disk has no matching
     entry in `pipeline/program_rule_packs/_manifest/active_prps.yaml`.
     Unbound PRP YAMLs may exist on disk for review purposes but MUST NOT be
     runtime-loaded.
  2. **F-PRP-SCHEMA-VERSION-MISMATCH** — `schema_version` in the PRP body
     does not match the loader-pinned `1.0-prp`.
  3. **F-PRP-LIFECYCLE-ENV-MISMATCH** — lifecycle truth is malformed
     (draft loaded into production, runtime_loadable=true without signed
     status, etc.). Mirrors the cards `enforce_lifecycle_truth` body shape.
  4. **F-PRP-CONTENT-HASH-INVALID** — the PRP's
     `lifecycle.content_hash` does not match the canonical-JSON SHA-256 of
     the PRP body with signature/hash fields stripped. Same canonical-bytes
     discipline as cards `canonical_bytes_sha256`.
  5. **F-PRP-SIGNATURE-INVALID** — the PRP's
     `_research_metadata.ed25519_signature` does not verify against the
     pinned prp-publisher pubkey from
     `vault_shared/program_rule_packs/publisher_pubkey.signed.yaml`.
     **Note**: this is a separate pubkey from the cards publisher pubkey.
  6. **F-PRP-EXPIRED** — today's date falls outside
     `[effective_date, expiry_date]`. Sub-tags `PRP-NOT-YET-EFFECTIVE` and
     `PRP-PAST-EXPIRY` distinguish the two failure shapes for audit-trail
     readability.
  7. **F-PRP-COUPLING-VIOLATION** — the PRP body contains forbidden
     CIC↔CLC coupling fields, OR private-organization-data fields (per
     Law 3: PRPs encode published live law only — never operator-specific
     overrides, never private member rosters).

These seven primitives are exported from the loader module as
`F_PRP_PRIMITIVE_NAMES` so that the Logician seat (§4) can register them
once the v0.2 first wave ceremony graduates the gate bodies to live.

### 19.4.1 Loader-realized sub-tags (v0.2 first wave)

Six invariants that the JSON Schema cannot enforce structurally — because
they depend on runtime context (today's date, cross-PRP graph state,
per-property uniqueness across array items) — are realized as sub-tags
under the seven F-PRP-* primitives at v0.2 first wave. Each sub-tag is
emitted under the parent primitive's error code, not registered as a new
primitive.

| Sub-tag | Parent primitive | Invariant |
|---|---|---|
| `PRP-NOT-YET-EFFECTIVE` | F-PRP-EXPIRED | today < `effective_date` |
| `PRP-PAST-EXPIRY` | F-PRP-EXPIRED | `expiry_date` != null AND today > `expiry_date` |
| `PRP-INVERTED-WINDOW` | F-PRP-EXPIRED | `effective_date` > `expiry_date` |
| `PRP-DUPLICATE-RULE-ID` | F-PRP-LIFECYCLE-ENV-MISMATCH | two `live_law_rules` items share a `rule_id` |
| `PRP-SELF-REFERENCE` | F-PRP-NOT-IN-ACTIVE-MANIFEST | `cross_references[i].referenced_prp_id` equals the PRP's own `prp_id` |
| `PRP-NOVEL-COUPLING-FIELD` | F-PRP-COUPLING-VIOLATION | loader walk catches a field name not in the schema's enumerated forbidden list (e.g., `tactical_interpretation_for_<org>` Law-3 escape) |

These sub-tags are documented here because the schema is deliberately
silent on them; an operator reading the schema alone might assume the
checks don't exist. They do — they're loader-side. Schema + loader
together are the defense-in-depth boundary.

## 19.5 Cross-references with other sections

  - **§4 Logician** — fail-closed if a PRP referenced by an active funding
    program is missing from the active manifest or has expired. The Logician
    composes F-PRP-NOT-IN-ACTIVE-MANIFEST and F-PRP-EXPIRED into the same
    preflight invariant family it uses for F-CARDS-* gates today.
  - **§7 Scribe** — consumes PRP `live_law_rules` during drafting. When
    Scribe drafts a USDA VAPG FY26 narrative, it pulls the active
    TILTH-PRP-USDA-VAPG-FY26 PRP's page-limit, attachment, and form rules
    plus the inherited TILTH-PRP-2CFR200 budget-allowability rules. Scribe
    MUST refuse to draft for a funding program whose PRP is not in the
    active manifest or has expired.
  - **§11 Intake** — at intake time, an applicant declares a target funding
    program. Intake resolves the program to its `program_specific` PRP and
    verifies the PRP's effective window contains today. Intake also resolves
    the program's inherited `cross_cutting_regulation` and
    `compliance_framework` PRPs via `cross_references` and verifies each is
    in-window. Intake MUST refuse to open a project for a program whose
    PRP has expired or is missing from the active manifest.

## 19.6 v0.1 DRAFT status — what is on disk, what is not live

On disk at v0.1 DRAFT (this commit):

  - `pipeline/program_rule_packs/_schema/program_rule_pack.schema.json` —
    JSON Schema for PRP bodies.
  - `pipeline/program_rule_packs/loader.py` — loader skeleton; all gate
    bodies raise `NotImplementedError("v0.2 first wave")`; top-level
    `load_active_prps()` raises `NotImplementedError` so any seat that
    wires PRP loading before v0.2 first wave fails-closed.
  - `pipeline/program_rule_packs/_manifest/active_prps.yaml` — manifest
    skeleton with six TBD entries (five framework/cross-cutting drawn from
    the audit synthesis recommendations + one program-specific exemplar).
  - `vault_shared/program_rule_packs/publisher_pubkey.signed.yaml` —
    pubkey-asset shape stub; key value is `<PENDING_OPERATOR_KEY_GENERATION>`.
  - `pipeline/blueprint/v0.1/section_19_program_rule_packs.md` — this
    section (DRAFT, no LOCK).

NOT on disk at v0.1 DRAFT:

  - No PRP YAML bodies. Authoring PRP content for any specific program is
    v0.2 first wave operator-content work.
  - No prp-publisher Ed25519 keypair. Operator generates separately when
    ready to issue the first PRP.
  - No Logician F-PRP-* gate bodies. Logician registration of the seven
    primitives happens at v0.2 first wave.
  - No Intake / Scribe seat wiring to consume PRPs at runtime.

NOT in any production code path at v0.1:

  - `load_active_prps()` is never called. Its top-level
    `NotImplementedError` is the fail-closed primitive that protects the
    boundary.

## 19.7 v0.2 first-wave graduation ceremony

The v0.2 first-wave ceremony will graduate this section to LOCKED. At that
ceremony, in order:

  1. Operator generates the prp-publisher Ed25519 keypair, fills
     `vault_shared/program_rule_packs/publisher_pubkey.signed.yaml`, and
     self-signs it (Trust-On-First-Use).
  2. Operator (or delegated regulatory-research role) authors the six PRP
     YAML bodies listed in the active manifest. Each body validates against
     `program_rule_pack.schema.json`.
  3. Operator signs each PRP body, populating `signed_at`, `signed_by`, and
     `content_hash`.
  4. Operator transitions each manifest entry from `status: draft` to
     `status: signed` and replaces `content_hash: TBD` with the canonical
     SHA-256.
  5. Operator graduates each gate body in `pipeline/program_rule_packs/loader.py`
     from `NotImplementedError` to a live body.
  6. Operator graduates the top-level `load_active_prps()` from
     `NotImplementedError` to a live call.
  7. Logician (§4) registers the seven F-PRP-* primitives.
  8. Intake (§11) and Scribe (§7) wire PRP consumption into their runtime
     paths.
  9. §0.5 paired-commit fires when this section transitions from DRAFT to
     LOCKED.

The v0.2 first wave graduation runs in lockstep with cards v0.2 loader
graduation. Both ceremonies happen at the same operator session to keep
the lifecycle-governance pattern uniform across the two data families.

## 19.8 Content scope seed — Phased Card System Research Audit

The six PRP entries in the v0.1 DRAFT active manifest are seeded directly
from `docs/phased_card_system_research_audit_extracted_2026-05-17.md`. That
document's five synthesis recommendations map naturally to PRP rule sets:

  1. **Decouple Student Profiles** → TILTH-PRP-FERPA-COPPA-HIPAA
     (compliance_framework). Encodes the School Official Exception, the
     45-day inspection window, COPPA under-13 verifiable parental consent,
     and the FERPA/HIPAA classification boundary for school-maintained
     medical records.
  2. **Standardize Underwriting Ratios** → folded into existing CLC card
     work at v0.2 (the audit's DSCR/NOI/LTV ratios are durable capital-
     logic grammar; they belong in `pipeline/cards/CLC/credit_underwriting.yaml`,
     not in a PRP). Noted here so the audit's five-recommendation list is
     fully reconciled against the PRP scope.
  3. **Automate Davis-Bacon Checking** → TILTH-PRP-DAVIS-BACON
     (cross_cutting_regulation). Encodes the $2,000 threshold, weekly
     prevailing-wage payment, the four weekly-pay compliance pathways,
     WH-347 + Statement of Compliance, three-year retention, and the $10M
     prime contractor certification trigger.
  4. **Deploy Programmatic Compliance Locks** → split across
     TILTH-PRP-2CFR200 (procurement tiers + splitting prohibition +
     drafting-contractor blacklist) and TILTH-PRP-NEPA-24CFR58 (Choice-
     Limiting Action Blocker + five review classifications + comment +
     objection windows + Certifying Officer liability).
  5. **Enforce Cooperative Equity Rules** → TILTH-PRP-SUBCHAPTER-T
     (compliance_framework). Encodes the Subchapter T patronage allocation
     formula, the consumer-member-as-primary-patron rule for hybrid
     cooperatives, state cooperative statutory caps (Virginia Code Title
     13.1 exemplar), and the three equity redemption methodologies.

The sixth PRP, TILTH-PRP-USDA-VAPG-FY26, is the program_specific exemplar.
It is not directly drawn from the audit synthesis recommendations (those
are framework/cross-cutting in scope), but is included so the v0.2 first
wave ceremony has at least one PRP of each `prp_kind` to validate the
schema against.

The audit is the single seed document for v0.2 first wave PRP content. Each
PRP body will cite the audit as a `_research_metadata.primary_sources`
entry, alongside the primary statutory / regulatory / NOFO citations.

## 19.9 Audit posture and known schema/loader split

A Red Team adversarial audit of this v0.1 DRAFT scaffold was performed at
authoring time (`pipeline/audits/prp_v0_1_red_team_audit_2026-05-17.md`).
The audit ran 26 adversarial probe bodies against the schema:

  - **14 HOLE-class probes** flipped to CAUGHT after schema hardening
    (cross-kind invariants, signed-PRP signature requirement,
    forbidden-coupling-fields enumeration at every nesting level,
    `accessed_date` required on `primary_sources`, ISO 8601 pattern on
    date fields, etc.).
  - **5 originally-CAUGHT probes** stay CAUGHT (no regression).
  - **6 LOADER-REALIZED probes** stay correctly silent at schema layer —
    the schema cannot enforce today's-date checks, cross-PRP graph
    traversal, or per-property uniqueness. F-PRP-* loader gate bodies at
    v0.2 first wave realize the §19.4.1 sub-tags.

**Methodology weakness flagged by the audit**: this audit was authored by
the same model that wrote the scaffold, in the same session. Per Cross-
Family Rigor (CLAUDE.md), a real Red Team pass against this scaffold
should route to a different provider family from the author. This audit
catches the obvious holes but should NOT be the final adversarial pass
before any v0.2 LOCK. Operator should dispatch a cross-family Red Team
cycle through the openclaw bridge against the hardened schema before
sign-off — the v0.2 first wave handoff at
`pipeline/handoffs/ws_prp_v0_2_first_wave_handoff_2026-05-17.md` includes
this as a prerequisite.

The adversarial test script at
`tests/program_rule_packs/test_schema_adversarial.py` captures all 14
HOLE-class probes so future regressions cannot slip in silently. The
script also captures the 6 LOADER-REALIZED probes as positive cases at
schema layer (they pass at schema; the corresponding loader gates land at
v0.2 first wave).
