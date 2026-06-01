# Blueprint Section 2 v7.2 — Operational-Data Sub-Kinds

**Status: LOCKED 2026-05-10.** L-005 strict two-audit cycle closed with FULL live cross-family rigor (Editor=Llama 3.3 70B/Groq Meta family + Judge=Gemini 2.5 Pro/Google + Red Team=GPT-OSS 120B/Groq OpenAI-OSS family). Cycle 1: Editor REQUIRES_FIX (7 documentary findings) + Judge READY_TO_LOCK 98/100 (2 LOW DCs) + Red Team ESCALATE (3 HIGH disposed as REJECT — 1 MISREAD + 1 FRAMING_DISAGREEMENT + 1 WRONG_SEVERITY — see `pipeline/validation/v2_v7_2_thesis_2026-05-10/audit_v1_synthesis.md`); 11 documentary fixes applied at rev2. Cycle 2: Editor READY_TO_LOCK (all 7 CLOSED) + Judge READY_TO_LOCK 100/100 (both DCs CLOSED) + Red Team ESCALATE (RT-01 maintained on raw-FS write bypass; 7 of 8 CLOSED). **L-005 architecture-domain disagreement branch fired** — operator confirmed Path C-LOCK 2026-05-10 (precedent: v7.0.7 row 180); rev3 narrow-fix added §10 OOS probe-checklist table (RT-C1-01..04) binding Red Team's forward probes to v0.2 multi-tenant Section O.5 work track. Cross-family rigor preserved both cycles; Section E carve-out NOT invoked. Code-phase deliverables (`pipeline/vault/sub_kinds/` 1568 LOC + `pipeline/vault/policies/operational_subkinds.cedar` 93 LOC + `tests/vault/sub_kinds/` 1506 LOC; 102 new tests per Code-phase done-definition) are byte-faithful to rev3.

F-VAULT-ARTIFACT-ONLY architectural commitment activates against this text at LOCK time.

**Parent blueprint:** `pipeline/blueprint/v0.1/section_02_vault_topology.md` (v7.1 LOCKED 2026-04-19; §2 LOCKED-as-a-whole 2026-04-22). v7.2 is a strict-superset additive amendment — every v7.1 invariant carries forward byte-identically. No v7.1 SIMPLE caller, no COMPOUND life-cycle, no boot-sequence step is altered.

**Architectural authority (binding):** `pipeline/architecture/v0.1/tilth_architecture_locked.md` §R.PF2 (v7 A6) — "§2 Vault topology MUST accommodate operational data alongside funder/grant artifacts" with a non-exhaustive list (metrics / financials / photos / narrative entries / timeline of activities / beneficiary records). F-VAULT-ARTIFACT-ONLY PRE-gate (v7 LOCKED) audit-binds this round: a §2 spin that rejects operational data sub-kinds at the schema level fails the audit.

**WS-F coordination (per dispatch plan):** `attachments` is added here as recommendation (a) — full schema + Cedar gate + vault subtree path land at v7.2; Uploader (§12) consumption lands when §12 v1.1 follows. The substrate is concrete, so §12 v1.1 LOCKs against a real file shape rather than a placeholder.

---

## 0. Reading map (Cycle-1 closure: E-02 / E-03 / E-07)

Single-table reference linking the R.PF2 architectural commitment to every implementation surface for each operational sub-kind. Use this when a builder or reviewer needs to walk one sub-kind end-to-end.

| R.PF2 type | §1 row | Schema (this doc) | Cedar policy (this doc) | Failure codes (this doc) | Code module | Test module | Severity |
|------------|--------|-------------------|--------------------------|---------------------------|-------------|-------------|----------|
| metrics (numerical time-series) | 1 | §2.11.1 | §6 Rule 1 | §7 (general) | `pipeline/vault/sub_kinds/metrics.py` | `tests/vault/sub_kinds/test_metrics.py` | GREEN |
| financials | 2 | §2.11.2 | §6 Rule 1 | §7 (general) | `…/financials.py` | `…/test_financials.py` | YELLOW |
| photos (binary media + EXIF) | 3 | §2.11.3 | §6 Rule 1 | §7 (general) | `…/photos.py` | `…/test_photos.py` | YELLOW |
| narrative entries | 4 | §2.11.4 | §6 Rule 1 | §7 (general) | `…/narrative_entries.py` | `…/test_narrative_entries.py` | YELLOW |
| timeline of activities | 5 | §2.11.5 | §6 Rule 1 | §7 (general) | `…/timeline_of_activities.py` | `…/test_timeline_of_activities.py` | YELLOW |
| **beneficiary records** | 6 | §2.11.6 | §6 Rules 1+2+3 | §7 + F-OPERATIONAL-PII-CONSENT-MISSING | `…/beneficiary_records.py` (PII discipline at `__post_init__`) | `…/test_beneficiary_records.py` (Cedar enforcement test class) | **RED if pii_present, YELLOW if anonymized** |
| attachments (Uploader §12 binding) | 7 | §2.11.7 | §6 Rule 1 | §7 (general) | `…/attachments.py` | `…/test_attachments.py` | YELLOW |

The single source of severity truth is `SUB_KIND_REGISTRY` (§2.12) — `severity_default` for the static value and `severity_for(record)` for the `BeneficiaryRecord.pii_present` dispatch.

---

## 1. Scope (v7.2 delta only)

v7.2 adds **seven SIMPLE sub-kind rows** to the §4.10.4 post-gate allowlist, **seven new vault subtree paths** under `orgs/{slug}/vault/operational/`, **seven frozen-dataclass record schemas** with canonical-JSON encode/decode, and **one Cedar policy file** at `pipeline/vault/policies/operational_subkinds.cedar` codifying per-kind admin-risk severity + per-org isolation + beneficiary PII discipline.

| # | Sub-kind | Vault subtree | Intent | Permitted modes | Admin-risk severity |
|---|---|---|---|---|---|
| 1 | `metrics` | `operational/metrics/` | `operational-metrics-write` | `write-if-absent` | GREEN |
| 2 | `financials` | `operational/financials/` | `operational-financials-write` | `write-if-absent` | YELLOW |
| 3 | `photos` | `operational/photos/` | `operational-photos-write` | `write-if-absent` | YELLOW |
| 4 | `narrative_entries` | `operational/narratives/` | `operational-narrative-write` | `write-if-absent` | YELLOW |
| 5 | `timeline_of_activities` | `operational/timeline/` | `operational-timeline-write` | `write-if-absent` | YELLOW |
| 6 | `beneficiary_records` | `operational/beneficiaries/` | `operational-beneficiary-write` | `write-if-absent` | RED if `pii_present == true`, else YELLOW |
| 7 | `attachments` | `operational/attachments/` | `operational-attachment-write` | `write-if-absent` | YELLOW |

All seven are SIMPLE-class (no compound transaction; one record = one file). The `write-if-absent` constraint is uniform: each record is keyed by a unique opaque `record_id`, written exactly once. Re-writes require operator-explicit re-key; in-place mutation is by design impossible.

**Why `write-if-absent` for every sub-kind:** operational data feeds the Report Generator (v0.2 R.3 horizon — see architecture §R.3). Reports work backward from documented substance. If a metric or beneficiary record could be silently overwritten, the report's substance becomes a moving target. Fail-closed on collision preserves auditability. (The same rationale that gave `claim-evidence-write` `write-if-absent` semantics in v5 — A-v1-02 — applies verbatim here.)

**Worked operator re-key path (Cycle-1 closure: E-04, DC-01).** When an operator finds a record was written with the wrong substance (typo'd metric value, wrong consent_tier on a beneficiary record, wrong opaque_id):

1. Operator mints a fresh `record_id` (UUID4 or per-org namespaced UUID — see §2.11.6 opaque-id scoping note).
2. Operator writes the corrected record under the new `record_id`. F-VAULT-WRITE-EXISTS does not fire because the path is fresh.
3. Operator appends an admin-risk-ledger entry naming both `record_id`s and the supersession reason. The ledger entry is the audit trail; downstream consumers (Report Generator v0.2) read from the ledger to know which record_id to honor.
4. The original record is NOT deleted. v7.2 has no delete path. The original sits at its path; the ledger entry is the disambiguator.

A v0.2 operator-CLI (`tilth-vault rekey-record <old_id> <new_id>`) is named in §10 OOS to wrap steps 1-3 into one command + auto-stamp the ledger entry. v7.2 itself ships the manual path; the CLI is convenience, not architecture.

## §2.11 Sub-kind schemas (additive to v7.1 §2)

All schemas live at `pipeline/vault/sub_kinds/<sub_kind>.py`. Each module:

* Defines a single `@dataclass(frozen=True, kw_only=True)` record class.
* Defines a `to_canonical_bytes(record) -> bytes` encoder (sorted keys, compact separators, UTF-8) — matches the v7.1 `serialize_manifest` discipline (§2.4).
* Defines a `from_canonical_bytes(payload) -> record` decoder that re-validates the schema invariants. Round-trip equality is a property tested per sub-kind.
* Declares `INTENT: str`, `VAULT_SUBTREE: str`, `ADMIN_RISK_SEVERITY: str` as module-level constants — these are read by the registry.
* Declares the per-record `record_id_for(record) -> str` key derivation; the canonical on-disk filename is `{record_id}.json` under the sub-kind's vault subtree.

**Schema design rule (v7.2):** schemas are intentionally minimal at v0.1 — only the fields needed to ground the record's existence and provenance. Extension is operator-driven; schema bumps require a new audit round per L-005.

**Naming convention rationale (Cycle-1 closure: E-01).** v7.2 sub-kind schemas deliberately do NOT reuse the KFR convention pair (`populated_at` / `populated_by` / `audit_chain`). KFR is a per-fact reasoning trail with provenance citations; vault sub-kinds are operational records with capture-time and minimal provenance. Reusing the names across two semantic surfaces would invite the wrong mental model. The v7.2 convention follows §2 v7.1 dataclass patterns: `record_id` (caller-minted), `captured_at` / `posted_at` / `authored_at` / `started_at` (kind-specific time field; uniformly UTC ISO-8601 ending in `'Z'`), `source` / `author` / `vendor` (origin field; kind-specific). The `'Z'` invariant is uniform across every time field. `content_hash` (SHA-3-512, 128 lowercase hex chars) is uniform across `PhotoRecord` and `AttachmentRecord`.

**Operator-discipline boundary (Cycle-1 closure: RT-04, RT-05).** v7.2 schemas validate **structure** (types, ISO-8601 trailing `'Z'`, currency three-letter, hash length, consent-tier ↔ pii_present consistency). v7.2 schemas do NOT validate **content** of free-form text fields:

| Sub-kind | Free-text fields not content-validated |
|----------|----------------------------------------|
| `MetricsRecord` | `metric_name`, `unit`, `source`, `tags` |
| `FinancialsRecord` | `category`, `description`, `vendor` |
| `PhotoRecord` | `caption`, `mime_type` |
| `NarrativeEntry` | `body`, `author`, `tags` |
| `TimelineActivity` | `summary`, `participants`, `location`, `outcome` |
| `BeneficiaryRecord` | `service`, `outcome`, `beneficiary_opaque_id`, `pii_fields` (label list) |
| `AttachmentRecord` | `filename`, `mime_type`, `proposal_section_anchor` |

This is by design at v0.1: operator (or operator's Cultivator pipeline) is responsible for ensuring that opaque-id fields carry opaque ids (not raw names), tag fields carry structured tags (not embedded PII strings), narrative bodies carry sanitized substance. Content-pattern validators (regex / NER / Logician POST-write content scanners) are downstream concerns named in:

- **§13 Data Collector blueprint** — outbound and inbound channel discipline; consent ledgers; per-state TCPA / CAN-SPAM rules card.
- **§14 Report Generator blueprint** — pre-publish content scan against the Original Proposal Commitments rubric.
- **§4 Logician v2.x amendment** — POST-write content-pattern gates as new failure-code families (e.g., `F-OPERATIONAL-RAW-NAME-IN-TAGS`, `F-OPERATIONAL-EMBEDDED-PII`) when the reviewer-side decision lands.

v7.2 carries the operator-discipline boundary as a documented contract; future spins promote operator-discipline contracts to enforced gates as the cost-benefit case is made (false-positive risk vs. PII-leak severity).

### 2.11.1 `MetricsRecord` (sub-kind: `metrics`)

```python
@dataclass(frozen=True, kw_only=True)
class MetricsRecord:
    record_id: str          # opaque caller-minted ID; must match filename
    metric_name: str        # canonical metric label (e.g. "soil_moisture_pct")
    value: float            # numeric reading
    unit: str               # SI / canonical unit string (e.g. "percent")
    captured_at: str        # UTC ISO-8601 with trailing 'Z'
    source: str             # capture method or instrument label
    tags: tuple[str, ...]   # ordered sortable string tags
```

Invariants: `metric_name` must not be empty; `unit` must not be empty; `captured_at` must end with `'Z'`; `tags` must be a tuple of strings (no nested mutables). Admin-risk severity: GREEN.

### 2.11.2 `FinancialsRecord` (sub-kind: `financials`)

```python
@dataclass(frozen=True, kw_only=True)
class FinancialsRecord:
    record_id: str
    amount_minor_units: int        # smallest currency unit (e.g. cents)
    currency: str                  # ISO-4217 alpha-3
    posted_at: str                 # UTC ISO-8601 'Z'
    category: str                  # operator-chosen ledger category
    description: str               # free-form line-item description
    vendor: str                    # vendor / counterparty (may be empty)
```

Invariants: `currency` is exactly three uppercase letters; `posted_at` ends with `'Z'`; `amount_minor_units` is integer (no float drift). Admin-risk severity: YELLOW.

### 2.11.3 `PhotoRecord` (sub-kind: `photos`)

```python
@dataclass(frozen=True, kw_only=True)
class PhotoRecord:
    record_id: str
    blob_relative_path: str        # path under operational/photos/blobs/ (caller-managed)
    content_hash: str              # SHA-3-512 hex of the binary blob (128 chars)
    mime_type: str                 # canonical MIME ("image/jpeg" / "image/png" / "image/heic")
    captured_at: str               # UTC ISO-8601 'Z'
    caption: str                   # operator-supplied caption (may be empty)
    geo_lat: float | None          # optional latitude; None if unspecified
    geo_lon: float | None          # optional longitude; None if unspecified
```

Invariants: `content_hash` is 128 lowercase hex chars; `mime_type` matches `^image/[a-z0-9.+-]+$`; `(geo_lat, geo_lon)` are both-None-or-both-set. Admin-risk severity: YELLOW (geolocation + face-bearing media).

**Note on the binary blob:** the photo blob itself is a separate write through `vault_write` with `intent="operational-photos-write"`; the on-disk record file is the metadata wrapper. v7.2 keeps the blob storage callable-managed and points the record at it via `blob_relative_path`. A v7.3 spin can promote a dedicated blob-binding compound-kind if metadata-blob atomicity becomes a felt need.

### 2.11.4 `NarrativeEntry` (sub-kind: `narrative_entries`)

```python
@dataclass(frozen=True, kw_only=True)
class NarrativeEntry:
    record_id: str
    authored_at: str               # UTC ISO-8601 'Z'
    author: str                    # operator id or sub-awardee opaque id
    body: str                      # free-form narrative text
    tags: tuple[str, ...]
```

Invariants: `body` is non-empty; `author` is non-empty; `tags` is a string tuple. Admin-risk severity: YELLOW (free-form text may surface PII; classification register applies).

### 2.11.5 `TimelineActivity` (sub-kind: `timeline_of_activities`)

```python
@dataclass(frozen=True, kw_only=True)
class TimelineActivity:
    record_id: str
    started_at: str                # UTC ISO-8601 'Z'
    ended_at: str | None           # UTC ISO-8601 'Z' or None for ongoing
    summary: str                   # one-line activity summary
    participants: tuple[str, ...]  # opaque participant ids; never raw names
    location: str                  # human-readable location label (may be empty)
    outcome: str                   # operator-supplied outcome description
```

Invariants: `started_at` ends with `'Z'`; if `ended_at` is set it ends with `'Z'` and is lexicographically greater than `started_at`; `participants` is a string tuple. Admin-risk severity: YELLOW.

**Note (Cycle-1 closure: RT-04 explicit).** `participants` is operator-discipline opaque-id-only — the schema validates tuple-of-str only. v7.2 does NOT enforce content patterns on participant strings; an operator (or buggy Cultivator) writing `participants=("John Doe", ...)` would leak PII into a YELLOW-severity record. Per §2.11 "Operator-discipline boundary," content scanning is a downstream §13 / §14 / §4 v2.x concern. Operators sourcing participants from Cultivator should rely on Cultivator's per-employee opaque-id mint (Cultivator v0.1 maps `telegram_user_id` → opaque internal id; raw names never enter).

### 2.11.6 `BeneficiaryRecord` (sub-kind: `beneficiary_records`)

```python
@dataclass(frozen=True, kw_only=True)
class BeneficiaryRecord:
    record_id: str
    beneficiary_opaque_id: str     # operator-minted opaque key (NOT a name)
    service: str                   # service or program label
    outcome: str                   # outcome / impact label
    consent_tier: str              # "anonymized" | "operator-authorized-identified"
    pii_present: bool              # True if any PII fields populated
    pii_fields: tuple[str, ...]    # list of PII field names actually populated
    captured_at: str               # UTC ISO-8601 'Z'
```

Invariants: `consent_tier` is one of the two allowed values; if `pii_present` is True then `pii_fields` is non-empty AND `consent_tier == "operator-authorized-identified"` (anonymized records cannot carry PII fields — fail-closed in `_validate_pii_consent_consistency`); if `pii_present` is False then `pii_fields` is empty. Admin-risk severity: **RED** when `pii_present` is True; YELLOW when `pii_present` is False (anonymized).

**PII discipline (architectural commitment from R.PF2):** Cedar policy `operational_subkinds.cedar` rule `beneficiary_pii_consent_required` denies any beneficiary write where the schema validator says `pii_present` and the principal session is not flagged operator-authorized for PII. The Python evaluator is authoritative at v0.1 (mirrors §2 v7.1 §3.4 lifecycle for `org_isolation.cedar`).

**Opaque-id scoping (Cycle-1 closure: RT-03 documentary).** `beneficiary_opaque_id` is per-org-scoped — uniqueness is enforced relative to the vault path (`orgs/{slug}/vault/operational/beneficiaries/{record_id}.json`), NOT global. Two different orgs MAY mint the same `beneficiary_opaque_id` value (e.g., both use `BEN-001`); each appears under its own org's vault subtree, and Cedar Rule 1 plus the per-session Law 3 Org Isolation gate prevent any single Tilth from reading both. Cross-org analytics or joins would be a Law 3 violation independently caught by the `principal.org_slug == resource.org_slug_hint` gate; opaque-id scheme is not the integrity boundary.

Operator practice: where opaque ids may be exchanged across orgs at Stage-5 commons participation (consent_tier `composable_with_others`), use UUID4 or namespaced UUID (e.g., `uuid5(NAMESPACE_ORG, f"{org_slug}:{local_id}")`) to avoid accidental cross-org id collision in shared aggregates. v7.2 documents this; v0.1 does not enforce because v0.1 has no Stage-5 surface.

### 2.11.7 `AttachmentRecord` (sub-kind: `attachments`)

```python
@dataclass(frozen=True, kw_only=True)
class AttachmentRecord:
    record_id: str
    filename: str                  # operator-facing display filename
    mime_type: str                 # MIME type (canonical)
    content_hash: str              # SHA-3-512 hex of the attached binary (128 chars)
    size_bytes: int                # attached binary size
    attached_to_grant_id: str      # foreign key into the grant-cycle vault subtree
    proposal_section_anchor: str   # provenance anchor (e.g. "narrative.outcomes")
    blob_relative_path: str        # path under operational/attachments/blobs/
```

Invariants: `content_hash` is 128 lowercase hex chars; `size_bytes >= 0`; `mime_type` is non-empty; `attached_to_grant_id` is non-empty. Admin-risk severity: YELLOW.

**WS-F coordination:** the `attached_to_grant_id` field anchors attachments to a grant cycle the Uploader (§12 v1.1 horizon) will assemble. Until §12 v1.1 LOCKs, attachments may be written via this sub-kind — Uploader consumption is a downstream binding, not a v7.2 dependency.

**Coordinated-binding risk (Cycle-1 closure: DC-02).** The `attached_to_grant_id` + `proposal_section_anchor` fields create an early binding to the grant-cycle vault structure (`orgs/{slug}/vault/grants/{grant_id}/...`). If §12 v1.1 LOCKs a grant-cycle path change between v7.2 LOCK and v1.1 LOCK, this schema requires a v7.x bump. The current binding is acceptable given the tight WS-F / WS-H coordination at §0.5 v9 LOCK 2026-05-10 (Uploader §12 v1 LOCKED today, row 184). A more decoupled design (generic `tags` tuple or abstract link) was rejected at scoping because the structured field gives Uploader's §12 v1.1 a stable read shape rather than a string-parsing dependency.

## §2.12 Sub-kind registry (additive)

`pipeline/vault/sub_kinds/registry.py` exposes a single canonical mapping `SUB_KIND_REGISTRY: dict[str, SubKindDescriptor]` keyed by sub-kind name. Each descriptor carries `intent`, `vault_subtree`, `record_class`, `to_canonical_bytes`, `from_canonical_bytes`, `record_id_for`, `severity_default`, and `severity_for(record)` (for sub-kinds whose severity depends on a record-level flag, e.g. `BeneficiaryRecord.pii_present`).

The registry is read at module import time; it is the single source of truth that downstream callers (Data Collector v0.2, Report Generator v0.2, Uploader v0.1.1, Archivist v1.x) bind against. Hardcoding intent names downstream is discouraged — go through the registry.

## §2.13 Post-gate allowlist extensions (additive to v7.1 §4.10.4)

Seven new SIMPLE rows are appended to `POST_GATE_ALLOWLIST` in `pipeline/vault/vault_write.py`:

```python
"operational-metrics-write":     PostGateAllowlistEntry(prefix="operational/metrics/",      modes={"write-if-absent"}, kind_class=SIMPLE),
"operational-financials-write":  PostGateAllowlistEntry(prefix="operational/financials/",   modes={"write-if-absent"}, kind_class=SIMPLE),
"operational-photos-write":      PostGateAllowlistEntry(prefix="operational/photos/",       modes={"write-if-absent"}, kind_class=SIMPLE),
"operational-narrative-write":   PostGateAllowlistEntry(prefix="operational/narratives/",   modes={"write-if-absent"}, kind_class=SIMPLE),
"operational-timeline-write":    PostGateAllowlistEntry(prefix="operational/timeline/",     modes={"write-if-absent"}, kind_class=SIMPLE),
"operational-beneficiary-write": PostGateAllowlistEntry(prefix="operational/beneficiaries/",modes={"write-if-absent"}, kind_class=SIMPLE),
"operational-attachment-write":  PostGateAllowlistEntry(prefix="operational/attachments/",  modes={"write-if-absent"}, kind_class=SIMPLE),
```

All seven preserve v7.1 §4.10.4 step 4.5/5/6/7 semantics — type validation, intent allowlist, prefix match, mode match. The §4.10.6 kind-class hard-gate denies any caller that passes `txn_token` to a SIMPLE operational intent.

Total POST_GATE_ALLOWLIST shape post-v7.2: **12 SIMPLE + 2 COMPOUND = 14 entries** (v7.1 baseline was 5 + 2 = 7).

## §5 VaultLayout extensions

`pipeline/vault/layout.py` gains seven `org_vault_operational_*` properties returning canonical paths under `orgs/{slug}/vault/operational/{<sub_kind>}/`. The shared `org_vault_operational_root(slug)` helper centralises the `operational/` prefix so future sub-kinds add one row, not two paths.

## §6 Cedar policy `operational_subkinds.cedar` (new file)

Lives at `pipeline/vault/policies/operational_subkinds.cedar`. Three rules:

1. **`operational_org_isolation`** — permits operational writes when the principal's `org_slug` matches the resource's `org_slug_hint`. Mirrors `org_isolation.cedar` Rule 2 surface for the operational subtree. Excludes `sub_kind == "beneficiary_records"` so beneficiary writes are forced through the explicit PII rules below; default-permit for non-beneficiary sub-kinds.
2. **`beneficiary_pii_anonymized`** — permits beneficiary writes when `resource.consent_tier == "anonymized"` AND **`resource.pii_present == false`** (Cycle-1 RT-02 closure: this rule is explicitly conjunctive on `pii_present`; an anonymized record carrying `pii_present == true` does NOT match Rule 2 and falls through to the implicit deny). Default-permit for the truly-anonymized case.
3. **`beneficiary_pii_with_consent`** — permits beneficiary writes when `resource.consent_tier == "operator-authorized-identified"` AND `resource.pii_present == true` AND `principal.operator_authorized_pii == true`. Operator must hold the explicit PII flag for the session.

Anything not matching these three rules → deny → `F-CEDAR-OPERATIONAL-DENIED`. Per the v7.1 lifecycle (§2 v7.1 §3.4 note): the Python evaluator at `pipeline/vault/sub_kinds/policy_eval.py` is authoritative at v0.1 until the file is M15-sealed. Cedar text is the human-auditable surface.

**Cross-product enforcement matrix (Cycle-1 RT-01 / RT-02 verification surface).** Every (consent_tier, pii_present, operator_authorized_pii) combination resolves to a single deterministic verdict at both layers:

| consent_tier | pii_present | operator_authorized_pii | Schema (`__post_init__`) | Cedar (Rules 1+2+3) | Combined verdict |
|--------------|-------------|--------------------------|---------------------------|----------------------|--------------------|
| `anonymized` | `False` | * | accept | Rule 2 permits | **PERMIT** |
| `anonymized` | `True` | * | reject (`F-OPERATIONAL-PII-CONSENT-MISSING` precursor; ValueError) | falls to deny (no rule matches) | **DENY** at schema; **DENY** at Cedar |
| `operator-authorized-identified` | `False` | * | reject (empty pii_fields invariant) | falls to deny (no rule matches) | **DENY** at schema; **DENY** at Cedar |
| `operator-authorized-identified` | `True` | `True` | accept | Rule 3 permits | **PERMIT** |
| `operator-authorized-identified` | `True` | `False` | accept | Rules 2+3 fall through; deny | **PERMIT** at schema; **DENY** at Cedar (`F-OPERATIONAL-PII-CONSENT-MISSING`) |
| any other consent_tier value | * | * | reject (allow-list invariant) | falls to deny | **DENY** at schema; **DENY** at Cedar |

Defense-in-depth: schema-bypass attack hits Cedar; Cedar-bypass attack hits schema. The two layers cover orthogonal threat surfaces. The matrix is regressively tested in `tests/vault/sub_kinds/test_beneficiary_records.py` and `test_policy_eval.py`.

**Schema-Cedar drift detection — v0.2 work item.** The Python evaluator and Cedar text encode the same semantics. v7.2 keeps the Python evaluator authoritative until M15-sealing; drift between the two surfaces is caught by manual review at every audit round. A v0.2 CI policy-equivalence test (parses `operational_subkinds.cedar`, asserts logical equivalence against `policy_eval.py` for the cross-product above) is named in §10 OOS as a v0.2 / M15.x sealing-side work item (Cycle-1 RT-07 closure).

## §7 Failure-code additions (additive to §6.12)

* `F-CEDAR-OPERATIONAL-DENIED` — Cedar deny on operational write (org-isolation / PII consent). Catch-all for any combination not matching one of the three permit rules.
* `F-OPERATIONAL-PII-CONSENT-MISSING` — schema validator caught a beneficiary record claiming `pii_present=True` without the matching consent tier OR with empty `pii_fields`. ALSO surfaces from the Cedar evaluator when a schema-valid record (consent_tier=operator-authorized-identified + pii_present=True) is presented by a principal without `operator_authorized_pii`. Fail-closed at both `BeneficiaryRecord.__post_init__` and `policy_eval.evaluate_operational_write`.
* `F-OPERATIONAL-SCHEMA-INVALID` — generic schema validation failure at decode (round-trip rejection); the decoder re-runs every `__post_init__` invariant, so a tampered-on-disk record claiming `pii_present=False` while carrying `pii_fields` non-empty hits this code at read-time.
* `F-OPERATIONAL-ORG-MISMATCH` (Cycle-1 closure: RT-08) — `policy_eval.py` raises this when the path-derived org slug (parsed from `orgs/{slug}/vault/operational/...`) ≠ `resource.org_slug_hint`. Surfaces the path-vs-resource-attribute consistency violation as a distinct, debuggable failure rather than the generic `F-CEDAR-OPERATIONAL-DENIED`. Operators receive a precise error pointing at the malformed call site, removing the incentive to bypass `vault_write` with a raw FS write.

All four exception classes inherit from `VaultError` per §6 family taxonomy.

## §8 Test surface

Every sub-kind ships with a round-trip test class under `tests/vault/sub_kinds/`:

* Unit — schema invariant tests (each invariant has a positive + negative case).
* Round-trip — `from_canonical_bytes(to_canonical_bytes(record)) == record`.
* Vault round-trip — write through `vault_write` → read raw bytes → decode → equal.
* Cedar enforcement — beneficiary-records test class includes a PII-consent-mismatch case that fail-closes via `F-OPERATIONAL-PII-CONSENT-MISSING` at the schema layer AND a Cedar-level deny case via the policy evaluator.
* Cross-org rejection — every sub-kind regresses `VaultCrossOrgAccess` when the path resolves outside `org_vault_root`.

## §9 v7.1 carry-forward (no behaviour change)

* All 826 existing tests under `tests/vault/` pass byte-identically against v7.2.
* **Three pinned-count tests update to 14-entry shape with v7.2 amendment citation (Cycle-1 closure: E-06):**
  - `tests/vault/test_section_2_integration.py::test_post_gate_allowlist_count` — assert `len(POST_GATE_ALLOWLIST) == 14` (was 7); citation comment `# v7.2 §2.13: 5 v7.1 SIMPLE + 7 v7.2 SIMPLE + 2 COMPOUND = 14`.
  - `tests/vault/test_section_2_bt_properties.py::test_simple_kind_count` — assert SIMPLE-class entry count == 12; citation comment as above.
  - `tests/vault/test_section_2_boot_sequence_property.py::test_allowlist_shape_post_boot` — assert post-boot allowlist shape matches the §2.13 table; citation comment as above.
  No other v7.1 test changes shape; the 826 v7.1-baseline survives byte-identically.
* AST-lint R1-R7 remains exit-0 across `pipeline/vault/`.
* COMPOUND life-cycle (§4.10.5/6/7) is unchanged.
* `index_amendment` COMPOUND kind remains the only compound kind in v0.1.
* §9 vault boot sequence (steps 1-11) is unchanged — operational subtrees are caller-created on first write (parent `mkdir(parents=True, exist_ok=True)` already in `vault_write`).
* New tests at `tests/vault/sub_kinds/` (1506 LOC, 102 tests per Code-phase done-definition) cover schema invariants, round-trip equality, vault round-trip via `vault_write`, Cedar enforcement (cross-product matrix per §6), and cross-org rejection. Full test surface enumerated in §8.

## §10 Out of scope for v7.2 (Cycle-1 closure: E-05 restructure)

| Item | Horizon | Driver |
|------|---------|--------|
| Pydantic (the library) as direct dataclass replacement | future v7.x amendment | Substrate is locked at Pydantic AI per CLAUDE.md / ADR-001, but Pydantic itself is not a direct dependency at v0.1. v7.2 uses `@dataclass(frozen=True, kw_only=True)` with `__post_init__` validation, matching the rest of §2. The registry abstraction (§2.12) makes a future swap a one-row-per-sub-kind change. |
| Photo-blob (metadata, blob) compound-kind binding | future v7.x amendment | v7.2 keeps blob storage callable-managed (§2.11.3 explicitly). If atomicity surfaces as a felt need (operator reports of dangling-pointer failures, or §13/§14 substrates demand atomic capture), promote `(metadata, blob)` to a new COMPOUND sub-kind row. Closes RT-06. |
| Beneficiary record PII redaction-at-rest | v0.2 Report Generator (§14) | v7.2 enforces consent at write-time only. PII redaction transforms for export, sharing, or aggregate-publish are a Report Generator concern under separate gating. |
| Operational data quotas / TTL / retention | v1.x Archivist (§15) | v7.2 has no per-sub-kind quota or retention policy. Archivist owns long-term curation, expiry, and per-sub-kind retention windows. |
| Operator re-key CLI (`tilth-vault rekey-record`) | v0.2 operator-CLI work | Wraps the manual re-key path documented in §1 into one command; auto-stamps the admin-risk-ledger entry. v7.2 ships the manual path. Closes E-04 + DC-01. |
| Cedar/Python-evaluator drift-detection CI | v0.2 / M15.x sealing | Until `operational_subkinds.cedar` is M15-sealed and the Cedar runtime becomes authoritative, the Python evaluator at `policy_eval.py` carries the canonical semantics. A CI test that parses the Cedar text and asserts logical equivalence against the Python evaluator (across the §6 cross-product matrix) is named here as a v0.2 work item. Closes RT-07. |
| Content-pattern PII validators on free-text fields | §13 Data Collector / §14 Report Generator / §4 Logician v2.x | v7.2 schemas validate structure only. Free-text content (tags, body, narrative, participants, opaque-id slot, etc.) is operator-discipline at v0.1. Future spins promote operator-discipline contracts to enforced gates as cost-benefit case is made. Closes RT-04 + RT-05. |
| **FS-write-gating threat model boundary** | **v0.2 multi-tenant per v7 LOCKED Section O.5** | v7.2's Cedar + schema gates are at the `vault_write` call path. Direct filesystem writes (`cp`, `mv`, `vim`, raw `open()` outside `vault_write`) are NOT gated at v0.1 because v0.1 ships under v7 LOCKED **A1 single-client + A4 operator-trusted** preflight assumptions — the operator owns the appliance and the runtime; there is no separate-pod / process-isolation boundary. Stage-2+ multi-tenant deployments need FS-write gating at the kernel layer (mount-namespace, capability-drop, FS-level allow-list); v7 LOCKED Section O.5 names this as the v0.2 multi-tenant work track. Closes RT-01 framing. |
| Global / cross-org `beneficiary_opaque_id` uniqueness | Stage-5 commons consent-tier `composable_with_others` design | v7.2 enforces per-org uniqueness via vault path. Cross-org analytics is a Law 3 violation independently caught. Stage-5 cross-Tilth aggregates need a uniqueness scheme (UUID4 / namespaced UUID); operator practice is documented in §2.11.6, not enforced. Closes RT-03 framing. |
| Confidential-classification of operational sub-kinds at the routing layer | §13 Data Collector / §14 Report Generator | v7.2 declares no routing posture for the agents that read these records. Each downstream blueprint (§13, §14) declares its own routing posture per v7.0.7 LOCKED 2026-05-10. v7.2 stays neutral; the per-call classification register on the Beta deployment routes per §13/§14 declarations. |

### §10.1 Forward-tracked v0.2 multi-tenant probe checklist (rev3 — operator Path C-LOCK 2026-05-10)

The Cycle-2 L-005 architecture-domain disagreement (RT-01 maintained on raw-FS write bypass) is dispositioned as Path C-LOCK with the following probes binding to the v0.2 multi-tenant Section O.5 work track. v7 LOCKED A1 (single-client) + A4 (operator-trusted preflight) bound v0.1's threat model; kernel-layer FS-write gating is the v0.2 mitigation surface. v7.2 LOCKs schema + Cedar + admin-risk + path layers per R.PF2's literal commitment; kernel-layer mitigation lands at v0.2.

| Probe | v0.2 / v2 owner | Test scope at v0.2 LOCK |
|-------|-----------------|--------------------------|
| RT-C1-01 | v7 LOCKED Section O.5 — mount-namespace isolation | No process can create `*.json` files under `orgs/*/vault/operational/*` without invoking `vault_write`. Tested via mount-namespace + capability-drop sandbox; raw FS writes from a non-vault process surface as `EACCES`. |
| RT-C1-02 | §13 Data Collector + §14 Report Generator — read-side validation | A deliberately malformed file placed by `cp` is rejected by Data Collector / Report Generator on read. Tested via fixture corpus of malformed records under each sub-kind path; `from_canonical_bytes` re-runs `__post_init__` invariants and Cedar evaluator re-runs the cross-product matrix. |
| RT-C1-03 | §4 v2.x Logician — F-OPERATIONAL-ORG-MISMATCH expansion | Failure code surfaces on read paths, not just writes. `evaluate_operational_write` is currently write-time; v0.2 adds a read-time companion `evaluate_operational_read` that validates path-derived slug ↔ resource-attribute consistency. |
| RT-C1-04 | M15.x sealing CI — Cedar/Python equivalence | CI policy-equivalence test runs before any M15 seal of `operational_subkinds.cedar`. Test parses Cedar text and asserts logical equivalence against `policy_eval.py` across the §6 cross-product enforcement matrix. (Also closes RT-07 forward track.) |

These probes are NOT v0.1 / v7.2 deliverables. They are the operator-confirmed forward-binding from v7.2 LOCK to v0.2 / v2 multi-tenant work, ensuring Red Team's escalation is captured in binding documentation rather than buried in synthesis-tier disposition. Future v0.2 multi-tenant cycles MUST read this list as a mandatory sub-task at LOCK ceremony.

## §11 Audit prompt for the Cowork Thesis round (LOCKED — historical record)

The L-005 two-audit cycle (cross-family per WS-B) audited this draft against:

1. **F-VAULT-ARTIFACT-ONLY rubric (binding).** Does v7.2 expose the schema such that future operational sub-kinds register via a registry row + new module + new allowlist row only? Or does it hard-code a closed set that would force a §2 round to add an eighth kind?
2. **PII discipline (architectural emphasis).** Beneficiary records carry RED-severity admin-risk per R.PF2. Does the v7.2 schema + Cedar gate combination prevent a same-org caller from silently shipping PII without consent? Specifically: does the schema validator fire BEFORE bytes touch disk, and does Cedar fail-closed when Python evaluator agrees?
3. **CIC × CLC orthogonality (per v7.0.8 LOCK).** No operational sub-kind schema implies a CIC subset (e.g. `BeneficiaryRecord` is reachable for every customer-identity category — a school can have students, a co-op can have member-beneficiaries, a public agency can have program participants). No sub-kind implies a CLC subset.
4. **Carry-forward integrity.** v7.1 SIMPLE and COMPOUND callers are not regressed. Boot sequence is unchanged. AST-lint clean. Existing 826 vault tests + 7 new sub-kind round-trip suites green (with three pinned-count tests updated to 14-entry shape).

---

End of v7.2 amendment — LOCKED 2026-05-10.
