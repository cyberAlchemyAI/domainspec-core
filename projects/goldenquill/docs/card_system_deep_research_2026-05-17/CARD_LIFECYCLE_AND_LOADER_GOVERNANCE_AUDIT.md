# CARD_LIFECYCLE_AND_LOADER_GOVERNANCE_AUDIT

**Phase 1 of the Tilth Card System Deep Research run, 2026-05-17.**

| Field | Value |
|---|---|
| Filed | 2026-05-17 |
| Workspace | `/Users/goldenquill/Downloads/GoldenQuill/` |
| Scope | Phase 1 of operator-directed deep-research scan. Run 1 cap. |
| Phase boundary | Stops cleanly at end of Phase 1; Phases 2, 3, 8.1-5 follow in the same run; Phases 4-CIC, 4-CLC, 5, 6, 7, 8.6-8 fire as separate dispatches. |
| Authority | On-disk inspection of `pipeline/cards/loader.py`, `pipeline/cards/models.py`, `pipeline/cards/_schema/*.schema.json`, `pipeline/cards/registry.yaml`, `pipeline/cards/README.md`, all 14 card YAMLs under `pipeline/cards/CIC/` + `pipeline/cards/CLC/`, the F-CARDS-* gate module family at `pipeline/logician/gates/`, architecture amendment v7.0.11, and §18 v1.2 amendment text. |
| Constraints honored | No LOCKed-file edits. No git operations. Sidecar-only writes under `docs/card_system_deep_research_2026-05-17/`. |
| Master prompt deltas surfaced in this phase | (1) The 8-phase research constitution the operator's corrective references is not present in the workspace; this audit reverse-engineers Phase 1 scope from the deliverable title plus the on-disk master-prompt (`docs/cic_clc_unified_master_prompt_2026-05-17.md`) §5. (2) The master prompt §5's central factual claim — "All 14 card YAMLs carry `lifecycle.draft_status: 'draft'`" — is FALSIFIED on disk: all 14 carry `draft_status: "signed"`. See §3.2 below. |

---

## §0. Findings summary (by severity)

| ID | Severity | One-liner | Surface | Detail § |
|---|---|---|---|---|
| L1-F0 | **P0** | Master prompt §5 lifecycle-gap claim is stale. All 14 cards on disk are already `draft_status: signed`. The "14-card supersession-re-sign draft_status normalization" ceremony proposed in `cic_clc_unified_batch_supervisor_prompt_2026-05-17.md` §6 is unnecessary — that work is done. | docs vs. disk | §3.2 |
| L1-F1 | **P0** | Three sources of truth on the lifecycle `draft_status` enum disagree. Architecture v7.0.11 §1.4 says 6 values (`draft \| reviewed \| thesis_passed \| signed \| loaded \| deprecated`); the JSON Schema files, `models.py`, and `loader.py` agree on 4 values (`draft \| review_passed \| signed \| deprecated`). The runtime/schema 4-tuple is the authoritative on-disk truth; the architecture amendment text is stale. | enum drift | §3.1 |
| L1-F2 | **P0** | Master prompt §5 also conflates two distinct state machines: `draft_status` (lifecycle progression) and `runtime_load_status` (legacy load-state label). The actual binding runtime flag is the boolean `runtime_loadable`, which the master prompt never mentions. | docs vs. disk | §3.3 |
| L1-F3 | **P0** | F-CARDS-COUPLING-VIOLATION-EXTENSION predicate body in `pipeline/logician/gates/f_cards_coupling_violation_extension.py` STILL raises `NotImplementedError`, even though `pipeline/blueprint/v0.1/section_04_v2_x_7_card_coupling_value_position_amendment.md` (filed LOCKED 2026-05-17 row 272 in its frontmatter) explicitly says the body was graduated to LIVE with field-name + value-position + matrix-structural scanners. Amendment-vs-code drift. | gate body | §6.3 |
| L1-F4 | **P1** | F-CARDS-UNSIGNED-PRODUCTION-LOAD and F-CARDS-SIGNATURE-INVALID gate modules are stubs — both raise `NotImplementedError`. The loader.py partially compensates by raising `CardLifecycleError` with the same gate-ID string (`F-CARDS-UNSIGNED-PRODUCTION-LOAD`) embedded, but **never actually invokes those gate modules** and **never verifies the embedded `_research_metadata.ed25519_signature` against the pinned publisher pubkey**. Loader-time signature verification is described as "v0.2 first-wave scope" — but architecture v7.0.11 §1.5 already lists publisher-pubkey verification as a Step-3 production requirement. | gate-vs-loader gap | §6 |
| L1-F5 | **P1** | At least 4 of 14 cards (food_systems, public_agency, cooperative, ecosystem_intermediary) carry **stale header comments** that read `# Lifecycle: draft. NO Ed25519 signature.` while their lifecycle body blocks at the end of the file declare `draft_status: signed` + `signed_at: <UTC timestamp>` + `content_hash: sha256:…`. The header comments lie about the file's state. | doc drift inside YAML | §5 |
| L1-F6 | **P1** | The loader at `pipeline/cards/loader.py:163-167` raises `NotImplementedError` at the seat-registration boundary after all preflight checks pass. This is intentional per the v0.1/v0.2 scope split (architecture v7.0.11 §5), but means **no card is currently runtime-loadable** in the literal sense — every `load_card()` invocation that passes preflight terminates with `NotImplementedError`, even cards correctly marked `runtime_loadable: true`. registry.yaml's `truth_invariant` ("Only signed, runtime_loadable cards may be active") is therefore aspirational at v0.1 Beta. | loader scope | §6.1 |
| L1-F7 | **P2** | The loader's `enforce_lifecycle_truth` at line 295 verifies `content_hash` against a freshly computed `sha256:` digest of the canonical card body (signature/hash fields excluded). This check is LIVE. However: the canonical-bytes computation **excludes `_research_metadata.ed25519_signature`** + **excludes `lifecycle.signature_status` and `lifecycle.content_hash`** but does NOT exclude `lifecycle.lock_history_row` / `lock_timestamp_utc` / `supersession_lock_history_row`. Future lock-history housekeeping rows could silently invalidate `content_hash`. Document the canonical-bytes-exclusion set explicitly. | hash discipline | §6.2 |
| L1-F8 | **P2** | The four `lifecycle.lock_history_row` / `lifecycle.lock_timestamp_utc` / `lifecycle.supersession_lock_history_row` schema fields are documented as `additionalProperties: true` on the lifecycle block (CIC schema line 521, CLC schema line 371) but never required, never enumerated for the loader, and not present in `models.py`'s `Lifecycle` dataclass at all. Either drop them from the JSON schema or graduate them into the dataclass + loader. | schema-vs-model drift | §3.4 |
| L1-F9 | **P2** | The loader's `enforce_lifecycle_truth` at lines 302-306 fail-closes on `runtime_loadable=False AND runtime_load_status='loaded'`. Cards in deprecated state would fail this check the moment an operator flips `runtime_loadable` to `false` without also flipping `runtime_load_status`. Document the deprecation procedure. | deprecation procedure unspecified | §7 |

---

## §1. Scope, sources, methodology

This audit reads the lifecycle/loader/governance surface of the Tilth Card System against three layers of authority:

1. **Architecture amendment v7.0.11** at `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md` — declared spec.
2. **JSON Schema files** at `pipeline/cards/_schema/card_cic.schema.json` + `pipeline/cards/_schema/card_clc.schema.json` — schema-of-record.
3. **Python implementation** at `pipeline/cards/loader.py` + `pipeline/cards/models.py` + the `pipeline/logician/gates/f_cards_*.py` module family — runtime enforcement.

Plus:

- **The 14 LOCKed cards** at `pipeline/cards/CIC/*.yaml` (6 files) + `pipeline/cards/CLC/*.yaml` (8 files).
- **The active-card registry** at `pipeline/cards/registry.yaml`.
- **The directory README** at `pipeline/cards/README.md`.
- **The cross-card §18 main + amendments** at `pipeline/blueprint/v0.1/section_18_card_system.md` + the three referenced amendments (v1.1, v1.2, v18.6 v2, v18.11 v1.1).
- **The §4 v2.x.7 amendment** at `pipeline/blueprint/v0.1/section_04_v2_x_7_card_coupling_value_position_amendment.md` (read in full).

Out of scope for Phase 1: research-content quality, funder-program currency, registers/dialects, admin-risk register consolidation, multi-track CLC content (Track A vs Track B). Those land in later phases.

---

## §2. The lifecycle state machine — design intent

Per architecture v7.0.11 §1.4 (`architecture_v7_0_11_card_amendment.md:80-89`):

> Every card carries lifecycle metadata:
> ```yaml
> lifecycle:
>   draft_status: draft | reviewed | thesis_passed | signed | loaded | deprecated
>   review_status: pending | passed | changes_requested
>   cross_family_thesis_status: pending | passed | failed
>   signature_status: unsigned | signed | revoked
>   runtime_load_status: not_loaded | loaded | disabled
> ```
> These five states are independent. A card can be `draft_status: thesis_passed` but `signature_status: unsigned` and `runtime_load_status: not_loaded`. The loader (§1.5) enforces lifecycle-gate-to-environment correspondence.

The loader contract (§1.5) declares production-environment behavior:

> Production: `draft_status` MUST be `signed`; `review_status` MUST be `passed`; `cross_family_thesis_status` MUST be `passed`; `signature_status` MUST be `signed` and the signature MUST verify against the operator-pinned Ed25519 publisher public key.

That is the spec. The next three sections audit what's actually on disk.

---

## §3. Lifecycle state — sources of truth disagree

### §3.1 Three-source enum drift (L1-F1)

| Source | `draft_status` enum | File:line |
|---|---|---|
| Architecture v7.0.11 §1.4 | `draft \| reviewed \| thesis_passed \| signed \| loaded \| deprecated` (6 values) | `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md:82` |
| JSON Schema (CIC) | `["draft", "review_passed", "signed", "deprecated"]` (4 values) | `pipeline/cards/_schema/card_cic.schema.json:391-398` |
| JSON Schema (CLC) | `["draft", "review_passed", "signed", "deprecated"]` (4 values) | `pipeline/cards/_schema/card_clc.schema.json:241-248` |
| `models.py` `Lifecycle.draft_status` | `Literal["draft", "review_passed", "signed", "deprecated"]` (4 values) | `pipeline/cards/models.py:71` |
| `loader.py` `DRAFT_STATUS_VALUES` | `frozenset({"draft", "review_passed", "signed", "deprecated"})` (4 values) | `pipeline/cards/loader.py:63-68` |

The schema/model/loader trio is byte-for-byte consistent and represents the **on-disk truth**. The architecture amendment text is stale relative to it:

- "reviewed" was renamed to "review_passed" somewhere in the amendment chain (likely §18 v1.1).
- "thesis_passed" was collapsed into the separate `cross_family_thesis_status` field.
- "loaded" was moved to the separate `runtime_load_status` field (line 425 of the CIC schema).

The architecture amendment text was never updated to reflect this consolidation. A reader who consults the architecture amendment as authoritative will write code or guidance against a 6-value enum that doesn't exist.

**Master prompt §5 cites `§18.12` as the source of the 6-value enum.** I have not been able to locate `§18.12` on disk as a discrete section header (a full read of `section_18_card_system.md` would be required to confirm). If `§18.12` does exist and matches the architecture text, the drift is doubled: both the architecture amendment AND a section of §18 main disagree with the schemas, the models, and the loader.

### §3.2 Master-prompt §5 factual error — the 14-card "draft_status: draft" claim is false (L1-F0)

The master prompt at `docs/cic_clc_unified_master_prompt_2026-05-17.md:398-411` says:

> **Verified on disk 2026-05-17.** All 14 card YAMLs (6 CIC + 8 CLC) carry `lifecycle.draft_status: "draft"` while every other lifecycle gate is at its pass-state.

This is false. Direct grep of all 14 cards' lifecycle blocks (search results from `^lifecycle:|^  draft_status:` across `pipeline/cards`):

| Card | Lifecycle block file:line | `draft_status` |
|---|---|---|
| `CIC/food_systems.yaml` | 641-650 | `"signed"` |
| `CIC/educator.yaml` | 1026-1035 | `"signed"` |
| `CIC/public_agency.yaml` | 1007-1016 | `"signed"` |
| `CIC/arts_culture.yaml` | 1039-1048 | `"signed"` |
| `CIC/cooperative.yaml` | 908-917 | `"signed"` |
| `CIC/ecosystem_intermediary.yaml` | 1071-1080 | `"signed"` |
| `CLC/public_purpose_works.yaml` | 731-740 | `"signed"` |
| `CLC/catalytic_change.yaml` | 625-634 | `"signed"` |
| `CLC/operating_capacity.yaml` | 434-443 | `"signed"` |
| `CLC/research_evidence.yaml` | 696-705 | `"signed"` |
| `CLC/market_access.yaml` | 789-798 | `"signed"` |
| `CLC/credit_underwriting.yaml` | 770-779 | `"signed"` |
| `CLC/sponsorship_corporate.yaml` | 684-693 | `"signed"` |
| `CLC/shared_assets.yaml` | 699-708 | `"signed"` |

All 14 cards uniformly carry:

```yaml
lifecycle:
  draft_status: "signed"
  review_status: "passed"
  cross_family_thesis_status: "passed"
  signature_status: "signed"
  runtime_load_status: "loaded"
  runtime_loadable: true
  signed_at: "<UTC timestamp; Wave 1 cards 2026-05-15T20:30Z, Wave 2 cards 2026-05-16T16:00Z>"
  signed_by: "founder"
  content_hash: "sha256:<hex>"
```

**Implication.** The §CC-N supersession-re-sign ceremony to "flip draft_status: draft → signed across all 14 cards" proposed in the unified supervisor prompt is **unnecessary**. The work has already been done on disk; the master prompt §5 was authored from out-of-date state.

This also means that the loader's `enforce_lifecycle_truth` discipline at `loader.py:259-263` (which fail-closes on `draft_status == "draft"`) would PASS every card today rather than reject every card as the master prompt implies. A researcher dispatched against the master prompt's §5 would surface a false-positive concern.

### §3.3 The two state machines + the binding runtime flag (L1-F2)

The lifecycle block holds two structurally similar but distinct state machines:

- `draft_status` — the canonical lifecycle progression. Values: `draft | review_passed | signed | deprecated`. Used by the loader to gate runtime-loadability.
- `runtime_load_status` — described in the schema as "Legacy load-state label retained for audit continuity; must align with runtime_loadable" (`card_cic.schema.json:432`). Values: `not_loaded | loaded | disabled`.

The schema's `allOf` conditional (CIC lines 468-520, CLC lines 318-369) pins them together when `runtime_loadable: true`:

- `runtime_loadable: true` → `draft_status == "signed"` AND `signature_status == "signed"` AND `runtime_load_status == "loaded"` AND `signed_at`/`signed_by`/`content_hash` present.
- `draft_status != "signed"` → `runtime_loadable: false`.

The **boolean `runtime_loadable`** is the binding runtime truth flag, not `draft_status` and not `runtime_load_status`. The master prompt never mentions `runtime_loadable` — it conflates `draft_status` and `runtime_load_status` in the §5 analysis and proposes a normalization ceremony for `draft_status` that addresses neither the boolean nor the real binding contract.

A correct mental model for any researcher or CTO:

> A card is runtime-loadable IFF `lifecycle.runtime_loadable == true`. That boolean implies (and is implied by, transitively through the schema conditional) `draft_status == "signed"` AND `signature_status == "signed"` AND `runtime_load_status == "loaded"`. The other three fields are descriptive of how it got there.

### §3.4 lock_history_row / lock_timestamp_utc / supersession_lock_history_row drift (L1-F8)

The CIC + CLC schemas both allow three optional lifecycle fields (CIC `card_cic.schema.json:458-466`, CLC `card_clc.schema.json:308-316`):

```json
"lock_history_row": { "type": "integer" },
"lock_timestamp_utc": { "type": "string" },
"supersession_lock_history_row": { "type": "integer" }
```

But:

- `models.py` `Lifecycle` dataclass (`models.py:59-79`) does not declare these fields. The dataclass is `kw_only=True` + `frozen=True`; an unknown field would raise `TypeError` at parse if the loader ever tried to instantiate `Lifecycle(**lifecycle_block)`.
- `loader.py`'s `LIFECYCLE_REQUIRED_FIELDS` (`loader.py:70-77`) does not include them.
- `loader.py`'s `validate_card_schema_shape` (`loader.py:181-237`) does not pass through.

The fields are documented in the schema only, ignored everywhere else. A card author could add or omit them at will. They are also not excluded from the canonical-bytes hash input (see L1-F7 / §6.2).

Recommendation: either graduate these fields into the dataclass + loader explicitly, or remove them from the JSON schema. They smell like provenance/audit-trail data that belongs in `_research_metadata` rather than `lifecycle` (since lifecycle is otherwise a tight state machine).

---

## §4. The 14 cards' actual state — full table

| Card ID | Slug | Axis | `draft_status` | `signed_at` | `signed_by` | `signed_at` lifecycle bucket |
|---|---|---|---|---|---|---|
| TILTH-CIC-01 | food_systems | CIC | signed | 2026-05-15T20:30:00Z | founder | Wave 1 |
| TILTH-CIC-02 | educator | CIC | signed | 2026-05-16T16:00:00Z | founder | Wave 2 |
| TILTH-CIC-03 | public_agency | CIC | signed | 2026-05-16T16:00:00Z | founder | Wave 2 |
| TILTH-CIC-04 | arts_culture | CIC | signed | 2026-05-16T16:00:00Z | founder | Wave 2 |
| TILTH-CIC-05 | cooperative | CIC | signed | 2026-05-16T16:00:00Z | founder | Wave 2 |
| TILTH-CIC-06 | ecosystem_intermediary | CIC | signed | 2026-05-16T16:00:00Z | founder | Wave 2 |
| TILTH-CLC-01 | public_purpose_works | CLC | signed | 2026-05-16T16:00:00Z | founder | Wave 2 |
| TILTH-CLC-02 | catalytic_change | CLC | signed | 2026-05-16T16:00:00Z | founder | Wave 2 |
| TILTH-CLC-03 | operating_capacity | CLC | signed | 2026-05-15T20:30:00Z | founder | Wave 1 |
| TILTH-CLC-04 | research_evidence | CLC | signed | 2026-05-16T16:00:00Z | founder | Wave 2 |
| TILTH-CLC-05 | market_access | CLC | signed | 2026-05-16T16:00:00Z | founder | Wave 2 |
| TILTH-CLC-06 | credit_underwriting | CLC | signed | 2026-05-16T16:00:00Z | founder | Wave 2 |
| TILTH-CLC-07 | sponsorship_corporate | CLC | signed | 2026-05-16T16:00:00Z | founder | Wave 2 |
| TILTH-CLC-08 | shared_assets | CLC | signed | 2026-05-16T16:00:00Z | founder | Wave 2 |

`registry.yaml:4` says: *"Only signed, runtime_loadable cards may be active. Draft/review/deprecated cards must not appear in active_cards."* All 14 cards appear in registry.yaml's `active_cards` list with `required_draft_status: signed` + `required_runtime_loadable: true`. All 14 card bodies satisfy both requirements. **The lifecycle invariant declared in registry.yaml HOLDS on disk today.**

The `registry.yaml:3` timestamp `generated_at: 2026-05-17T20:30:00Z` is later than every card's `signed_at`. The registry was rebuilt after the last supersession-re-sign.

---

## §5. Header-comment drift (L1-F5)

YAML files allow free-form `# …` comments above the data block. Four cards still carry stale lifecycle commentary in their headers:

| File | Line | Header comment | Body lifecycle truth |
|---|---|---|---|
| `pipeline/cards/CIC/food_systems.yaml` | 28 | `# Lifecycle: draft. NO Ed25519 signature. Operator review pending before Wave 1 LOCK` | line 642: `draft_status: "signed"` |
| `pipeline/cards/CIC/public_agency.yaml` | 36 | `# Lifecycle: draft. NO Ed25519 signature. Operator review pending before Wave 2` | line 1008: `draft_status: "signed"` |
| `pipeline/cards/CIC/cooperative.yaml` | 45 | `# Lifecycle: draft. NO Ed25519 signature. Operator review pending before Wave 2` | line 909: `draft_status: "signed"` |
| `pipeline/cards/CIC/ecosystem_intermediary.yaml` | 113 | `# Lifecycle: draft. NO Ed25519 signature. Operator review pending before Wave 2` | line 1072: `draft_status: "signed"` |

These header comments were authored during draft authorship and were never updated through the LOCK + supersession-re-sign ceremonies. They lie about the card's current state.

Comments are not part of the canonical-bytes signature input (the loader's `canonical_bytes()` at `loader.py:347-362` operates on the parsed YAML body, not the raw bytes). Updating the comments is therefore a documentation-only edit that **does not** invalidate the existing `content_hash`. The patch is mechanical: change `# Lifecycle: draft. NO Ed25519 signature.` → `# Lifecycle: signed (Wave N LOCK; supersession-re-sign 2026-05-15/16). Ed25519 signature present in lifecycle.content_hash and _research_metadata.ed25519_signature.`

Recommend: do this in the same ceremony as any other comment-only updates that come out of Phase 2 + Phase 8, to minimize ceremony count.

(The other 10 cards may have similar drift; full audit of all 14 header comments is in scope for Phase 2.)

---

## §6. Loader enforcement posture (`pipeline/cards/loader.py`)

The loader is the trust-boundary surface. Architecture v7.0.11 §1.5 declares a nine-step contract; the actual implementation status:

| Step | Spec | Status on disk | File:line |
|---|---|---|---|
| 1 | Read YAML card from disk | LIVE | `loader.py:170-178` (`read_card_body`) |
| 2 | Validate against `*_card.schema.json` | PARTIAL — `validate_card_schema_shape` checks a hand-curated subset, NOT the full schema. The module docstring (`loader.py:181-187`) is explicit: *"This intentionally does not replace the JSON schema files; it is the small fail-closed shape check the loader can run without adding another runtime dependency."* | `loader.py:181-237` |
| 3 | Verify lifecycle state matches environment | LIVE | `loader.py:240-306` (`enforce_lifecycle_truth`) |
| 4 | Reject private-org-data cards | NOT IN LOADER | F-CARDS-PRIVATE-DATA-IN-CARD gate exists at `f_cards_private_data_in_card.py` (not read in this audit); loader does not invoke it. |
| 5 | Reject CIC×CLC coupling | LIVE (partial — top-level field-name + recursive nested-key scan only; no value-position regex). | `loader.py:309-344` (`enforce_no_forbidden_coupling` + `_find_forbidden_keys`) |
| 6 | Resolve card to memory namespace | LIVE | `loader.py:383-410` (`resolve_card_namespace`) |
| 7 | Build memory profile | NOT REACHED — `load_card` raises `NotImplementedError` at line 163 before this step. |
| 8 | Register runtime defaults with seats | NOT REACHED — same boundary. |
| 9 | Record load event in audit log | NOT REACHED — same boundary. |

### §6.1 `NotImplementedError` at the seat-registration boundary (L1-F6)

`loader.py:163-167`:

```python
raise NotImplementedError(
    "Card runtime registration graduates LIVE at v0.2 first wave per "
    "architecture v7.0.11 §5. Lifecycle/coupling preflight is already LIVE "
    "so draft or malformed cards fail before this boundary."
)
```

This is intentional and documented (architecture v7.0.11 §5 declares full seat-runtime-registration as v0.2 first-wave scope). The practical implication for v0.1:

- `load_card()` callable but never returns a `LoadedCard`. Every successful preflight terminates with `NotImplementedError`.
- `registry.yaml`'s `truth_invariant` and `active=true` entries describe what cards *would* be active if the seat-registration boundary were graduated. At v0.1 they're aspirational.
- The `tests/cards/test_lifecycle_truth.py` test surface (exists per the initial filesystem scan — not read in this audit) almost certainly exercises preflight + asserts the `NotImplementedError` boundary as expected behavior.

This is not a bug, but it should be surfaced clearly to a CTO. The card-system runtime is "instrumented but not yet wired."

### §6.2 `content_hash` verification — what's in, what's out (L1-F7)

`loader.py:293-300`:

```python
if verify_content_hash:
    actual_hash = str(lifecycle.get("content_hash"))
    expected_hash = f"sha256:{canonical_bytes_sha256(card_body=card_body)}"
    if actual_hash != expected_hash:
        raise CardLifecycleError(...)
```

`canonical_bytes()` at `loader.py:347-362` normalizes by sorting keys (`sort_keys=True`) + removing whitespace (`separators=(",", ":")`) + encoding UTF-8. Before serialization, `_without_signature_and_hash_fields` (`loader.py:371-380`) deepcopies the body and removes:

- `lifecycle.signature_status`
- `lifecycle.content_hash`
- `_research_metadata.ed25519_signature`

NOT excluded:

- `lifecycle.lock_history_row`
- `lifecycle.lock_timestamp_utc`
- `lifecycle.supersession_lock_history_row`
- `lifecycle.signed_at`, `lifecycle.signed_by`

This is fine *today* because lock-history rows are pinned at LOCK ceremony time and don't change post-LOCK without a supersession. But: if a future operator workflow adds purely-housekeeping lock-history references to a card body (e.g., a "this card was last validated by row 999 health-check ceremony" pointer), every such write invalidates `content_hash` and forces a re-sign.

Recommendation: document the canonical-bytes-exclusion set explicitly in the loader docstring (currently silent at `loader.py:347-354`), and add `lifecycle.lock_history_row` / `lock_timestamp_utc` / `supersession_lock_history_row` to the exclusion set if they're meant to be operational-housekeeping rather than identity-binding. Otherwise, leave them in and treat any change as a re-sign event.

### §6.3 F-CARDS-* gate module family graduation status (L1-F3, L1-F4)

`pipeline/logician/gates/f_cards_*.py` modules on disk:

| Module | GATE_ID | Body status | File:line |
|---|---|---|---|
| `f_cards_malformed_lifecycle.py` | F-CARDS-MALFORMED-LIFECYCLE | **LIVE** — body delegates to `enforce_lifecycle_truth` | `f_cards_malformed_lifecycle.py:25-43` |
| `f_cards_coupling_violation_extension.py` | F-CARDS-COUPLING-VIOLATION-EXTENSION | **STUB** — body raises `NotImplementedError`. FORBIDDEN_FIELD_REGISTRY constant IS live for build-time AST-lint. | `f_cards_coupling_violation_extension.py:63-82` |
| `f_cards_unsigned_production_load.py` | F-CARDS-UNSIGNED-PRODUCTION-LOAD | **STUB** — body raises `NotImplementedError`. | `f_cards_unsigned_production_load.py:26-41` |
| `f_cards_signature_invalid.py` | F-CARDS-SIGNATURE-INVALID | **STUB** — body raises `NotImplementedError`. | `f_cards_signature_invalid.py:26-41` |
| `f_cards_coverage_incomplete.py` | F-CARDS-COVERAGE-INCOMPLETE | Not read in this audit; presumed LIVE per architecture v7.0.11 §1.6 #1 ("META PRE-cycle gate"). |  |
| `f_cards_cross_org_namespace_leak.py` | F-CARDS-CROSS-ORG-NAMESPACE-LEAK | Not read; stub likely per "Phase B v0.2 wiring." |  |
| `f_cards_load_in_wrong_namespace.py` | F-CARDS-LOAD-IN-WRONG-NAMESPACE | Not read; stub likely. |  |
| `f_cards_private_data_in_card.py` | F-CARDS-PRIVATE-DATA-IN-CARD | Not read; stub likely. |  |
| `f_cards_schema_invalid.py` | F-CARDS-SCHEMA-INVALID | Not read; loader has partial implementation, gate body status unconfirmed. |  |

(The architecture v7.0.11 §1.6 roster lists 10 codes including F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY; the actual on-disk module name for that one was not found in the glob and may live under `f_cic_clc_*.py` rather than `f_cards_*.py`.)

**Critical finding (L1-F3).** The §4 v2.x.7 amendment at `pipeline/blueprint/v0.1/section_04_v2_x_7_card_coupling_value_position_amendment.md` declares (line 5) `amendment_status: LOCKED 2026-05-17 — paired with §0.5 v31 amendment`. The amendment's §1 declares (lines 38-47):

> 1. **Field-name registry scan graduated to LIVE.** ... This amendment turns the runtime predicate body itself into a callable scan over `card_body.keys()` against `FORBIDDEN_FIELD_REGISTRY[axis]`.
> 2. **Value-position regex scan added.** Recursive walk over all string values in the card body matches the four canonical coupling-language patterns and emits one violation per hit ...
> 3. **Matrix-card structural rule graduated to LIVE.** ...

The amendment's §2 (lines 74-89) gives the post-LOCK body pseudocode.

The amendment's `companion_code_landed` (line 15) explicitly claims:

> `pipeline/logician/gates/f_cards_coupling_violation_extension.py (UPDATED — predicate body graduated from NotImplementedError to LIVE three-layer scan ...)`

The module on disk at `pipeline/logician/gates/f_cards_coupling_violation_extension.py:78-82`:

```python
raise NotImplementedError(
    f"{GATE_ID} predicate body graduates LIVE at v0.2 first wave per "
    f"architecture v7.0.11 §5. FORBIDDEN_FIELD_REGISTRY constant is LIVE "
    f"at v0.1 Beta LOCK for AST-lint scan support."
)
```

**The amendment's LOCK frontmatter and §1/§2 prose claim the graduation happened. The module on disk is the pre-graduation stub.** Possible explanations:

- The amendment was LOCKed but the companion code patch was reverted post-LOCK.
- The amendment LOCK ceremony fired against a different branch.
- The amendment frontmatter was filled out aspirationally and the actual ceremony never executed.
- The companion code lives somewhere else (an unmerged outputs/ patch?) and was never copied into `pipeline/logician/gates/`.

Operator should reconcile. The "operator-runnable script (e.g., pipeline/scripts/od_c_backfill_scan.py or equivalent)" referenced at amendment §6 line 187 also does not exist at that path — there is an `outputs/od_c_backfill_scan.py` referenced in the amendment's cross-references (`section_04_v2_x_7_*.md:238`), suggesting the backfill scan was authored in a Cowork workspace `outputs/` directory and never pre-staged into `pipeline/scripts/` at the ceremony.

**Compensating control.** The `loader.py:309-344` `enforce_no_forbidden_coupling` does the top-level + nested field-name scan correctly using the live FORBIDDEN_FIELD_REGISTRY. So the field-name-scan layer of the §4 v2.x.7 amendment is effectively LIVE in the loader, just not in the named gate module. The value-position regex scan and the matrix-card structural rule are NOT live anywhere — they're spec-only.

This is a real CTO-level finding: an amendment of record claims runtime enforcement that doesn't exist. The next stub graduation ceremony (likely at v0.2 first wave per architecture v7.0.11 §5) needs to land the §4 v2.x.7 spec into the gate module, or the amendment needs to be re-LOCKed with corrected `companion_code_landed`.

### §6.4 Loader-time Ed25519 verification

Architecture v7.0.11 §1.5 step 3 production requirement:

> the signature MUST verify against the operator-pinned Ed25519 publisher public key.

The loader does NOT do this. `enforce_lifecycle_truth` checks `signature_status == "signed"` (string equality) and `content_hash` (SHA-256 of canonical bytes) but never decodes `_research_metadata.ed25519_signature` (hex string per `models.py:94`) and never invokes `nacl.signing.VerifyKey.verify` against the pinned publisher pubkey.

The publisher pubkey itself lives at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml` per the README and the initial filesystem scan. The loader has a `publisher_pubkey: Optional[bytes] = None` parameter (`loader.py:127`) that is never consumed (never passed to a verify call) anywhere in the module.

The `F-CARDS-SIGNATURE-INVALID` gate module body raises `NotImplementedError`. There is no other on-disk surface that verifies the signature.

**Therefore: the embedded `ed25519_signature` field in every card's `_research_metadata` is currently unverified at load time.** The master prompt §8 acknowledges this (item 4: "Embedded `ed25519_signature` is intentionally stale on the 3 OD-E-restructured CLC cards"). The corollary is broader than the master prompt admits — *every* card's signature is currently unverified, not just the three that were restructured. The trust model relies on `content_hash` (loader-checked SHA-256) plus the registry-yaml + lock-history audit trail.

For v0.2 first-wave loader graduation, the patch shape is:

1. Add `publisher_pubkey: bytes` as a required (not optional) parameter to `load_card()` in production environments.
2. Add `enforce_signature_validity()` between Step 3 and Step 5 of the loader contract — decode the hex `ed25519_signature`, recompute canonical_bytes, call `VerifyKey(publisher_pubkey).verify(canonical_bytes, decoded_sig)`, raise `CardLifecycleError` with gate ID `F-CARDS-SIGNATURE-INVALID` on failure.
3. Graduate `f_cards_signature_invalid.py` body and `f_cards_unsigned_production_load.py` body in parallel.

---

## §7. Deprecation procedure unspecified (L1-F9)

Both schemas allow `draft_status: "deprecated"` but neither documents the transition:

- What `signature_status` is `deprecated` paired with? Still `signed`? Or `revoked`?
- What `runtime_load_status`? `disabled` (the third value in the runtime_load_status enum)?
- Does `runtime_loadable` go to `false`? The schema conditional says yes (`draft_status != signed → runtime_loadable: false`) but does not specify the entry of deprecation.
- Does `lifecycle.signature_status: "revoked"` (the third value of that enum) flip the card out of the registry?
- Does the loader's `enforce_lifecycle_truth` line 302-306 check (`runtime_loadable=false AND runtime_load_status='loaded'` → fail-closed) fire incorrectly on a half-deprecated card?

Operator-facing concern: the deprecation path is the most likely surface to surface inconsistencies under real operations. The current spec covers the happy path (signed, runtime-loaded) and the entry path (draft → review_passed → signed) but is silent on retirement.

Recommendation: write a deprecation procedure note in a new §18 v1.x amendment, or in `pipeline/cards/README.md` under a new "Deprecating a card" section. Cover: flipping `runtime_loadable` to `false` BEFORE flipping `runtime_load_status` (avoids the L302-306 trap), updating the `registry.yaml` to remove the entry from `active_cards` (or add a `deprecated_at` field), and the supersession lock-history-row pattern.

---

## §8. Forward-pointers to other Phase 1 outputs (Run 1)

This audit's findings feed into:

- **Phase 2 (CANONICAL_NAMING_AND_ORTHOGONALITY_AUDIT.md)** — the L1-F3 gate-body drift is also a coupling-discipline finding. The L1-F4 loader-vs-gate ownership of signature/unsigned-load enforcement is also a naming/ownership clarity issue.
- **Phase 3 (INITIAL_CTO_HANDOFF_BLOCKERS.md)** — L1-F0, L1-F1, L1-F3, L1-F4 are all P0 CTO blockers.
- **Phase 8.1-5 (FILE_BY_FILE_PATCH_QUEUE_PRE_V0_2.md)** — concrete patch shapes for L1-F1 (architecture v7.0.11 §1.4 enum reconciliation), L1-F3 (gate-body graduation), L1-F4 (loader signature verification), L1-F5 (header-comment update), L1-F7 (canonical-bytes exclusion documentation), L1-F8 (lock-history field disposition), L1-F9 (deprecation procedure).

---

## §9. Files cited

| File | Lines referenced | Purpose |
|---|---|---|
| `pipeline/cards/loader.py` | 63-77, 123-167, 170-178, 181-237, 240-306, 309-344, 347-380, 383-410 | Loader contract implementation |
| `pipeline/cards/models.py` | 27-54, 59-79, 84-95, 99-138, 143-175, 180-207, 212-222 | Dataclass mirror of schemas |
| `pipeline/cards/_schema/card_cic.schema.json` | 24-554, esp. 380-521 lifecycle block | Schema-of-record (CIC) |
| `pipeline/cards/_schema/card_clc.schema.json` | 23-415, esp. 230-372 lifecycle block | Schema-of-record (CLC) |
| `pipeline/cards/registry.yaml` | 1-118 | Active-card manifest |
| `pipeline/cards/README.md` | 1-99 | Directory documentation |
| `pipeline/cards/CIC/*.yaml` (6 files) | Lifecycle blocks at lines 641-650, 1026-1035, 1007-1016, 1039-1048, 908-917, 1071-1080 | On-disk lifecycle truth |
| `pipeline/cards/CLC/*.yaml` (8 files) | Lifecycle blocks at lines 731-740, 625-634, 434-443, 696-705, 789-798, 770-779, 684-693, 699-708 | On-disk lifecycle truth |
| `pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md` | 76-124 (§1.4-§1.6) | Design-intent spec |
| `pipeline/blueprint/v0.1/section_18_v1_2_amendment.md` | 56-140, 207-209 | dialect_routing_table re-keying (cross-ref to Phase 2) |
| `pipeline/blueprint/v0.1/section_04_v2_x_7_card_coupling_value_position_amendment.md` | 1-241 | OD-C value-position scan amendment (L1-F3 source) |
| `pipeline/logician/gates/f_cards_malformed_lifecycle.py` | 1-43 | LIVE lifecycle gate |
| `pipeline/logician/gates/f_cards_coupling_violation_extension.py` | 1-82 | STUB — claimed live by amendment, not live in module |
| `pipeline/logician/gates/f_cards_unsigned_production_load.py` | 1-41 | STUB |
| `pipeline/logician/gates/f_cards_signature_invalid.py` | 1-41 | STUB |
| `pipeline/logician/gates/f_cic_clc_coupling_violation.py` | 1-328 | LIVE four-layer v7.0.8 coupling gate (cross-ref to Phase 2) |
| `docs/cic_clc_unified_master_prompt_2026-05-17.md` | §5 lines 394-420 | Master prompt's stale lifecycle-gap claim |
| `docs/cic_clc_unified_batch_supervisor_prompt_2026-05-17.md` | §6 lines 160-172 | Proposed-but-unnecessary supersession ceremony |

---

*End of Phase 1 deliverable.*
