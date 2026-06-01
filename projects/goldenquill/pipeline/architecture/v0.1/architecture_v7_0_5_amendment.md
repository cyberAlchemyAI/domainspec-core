---
title: Tilth Architecture — Amendment v7.0.5 (Funder Intelligence Database + Match Database — workspace-shared funder corpus, per-org Scout reasoning trail, Stage-5 cooperative on-ramp)
filed: 2026-05-08
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-10 — substantive architectural addition (two new register schemas + new Scout channel family + Stage-5 cooperative-corpus on-ramp design + Archivist curation-slot binding). L-005 two-audit cycle completed cross-family per AGENTS.md (Editor: Llama 3.3 70B / Groq, Meta family; Judge: Gemini 2.5 Pro / Google; Red Team: GPT-OSS 120B / Groq, OpenAI-OSS family). Audit #1 surfaced 17 findings (3 HIGH + 5 MED + 9 LOW); Cycle 1 fixes applied 2026-05-09. Audit #2 verification 2026-05-10: Editor READY_TO_LOCK + Judge READY_TO_LOCK (100/100) + Red Team REQUIRES_MINOR_FIXES (all Cycle 1 closed; 4 Cycle 2 probes surfaced; 3 P1 FOLDED_IN at LOCK per row-170 precedent; 1 OUT_OF_SCOPE-LATENT forward-tracked). Audit trail at `pipeline/validation/v7_0_5_thesis_2026-05-09/`.
parent_lock: pipeline/architecture/v0.1/tilth_architecture_locked.md
parent_amendment: pipeline/architecture/v0.1/architecture_v7_0_3_amendment.md
companion_amendments:
  - "pipeline/architecture/v0.1/architecture_v7_0_6_amendment.md (roster — Archivist reserved for v1.x curation; Funder Intelligence Database + Match Database curation-slot lives here)"
  - "pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md (Beta model strategy — Funder Intelligence content is typically Public; Match Database may reference confidential client fields and uses classification-aware slot-fill)"
  - "pipeline/architecture/v0.1/architecture_v7_0_4_amendment.md (KFR — Funder Intelligence Database is per-funder factual substrate; KFR is per-org factual substrate; both feed Scribe at different stages)"
companion_files_pending_edit:
  - "pipeline/blueprint/v0.1/section_03_scout.md (new channel family — local discovery corpus query; Match Database integration for de-dup against prior proposals)"
  - "pipeline/blueprint/v0.1/section_04_logician.md (new failure code F-MATCH-DB-CROSS-ORG enforcement; F-FUNDER-CORPUS-STALE; F-FUNDER-CORPUS-INTEGRITY)"
  - "pipeline/blueprint/v0.1/section_05_pipeline.md (Match Database lifecycle integration with grant cycle; consent_tier field handling)"
  - "vault_shared/funder_intelligence/ (new directory; register schema; initial seed of common funder docs)"
  - "orgs/_TEMPLATE/match_database/ (new directory; register schema; consent_tier defaults)"
authority_source: prior conversation 2026-05-06 ("if we can expand searches after initial agency scans on API's and the database we are building everytime we find opportunities, the database that sits on computer will grow that much faster and be so much more valuable"); cooperative sovereignty opt-in memory (consent tiers — my-eyes-only / matchable-to-opportunities / composable-with-others); LDR-pattern decision for retrieval substrate
version_wording_discipline: "LOCKED" inside this file refers to on-disk LOCKED state at filing time. The Funder Intelligence Database, Match Database, new Scout channel family (local corpus), F-MATCH-DB-* failure codes, and Stage-5 cooperative-corpus on-ramp design are NEW mechanisms introduced by this amendment. All require Thesis-round review before LOCK.
---

# Amendment intent

Every Scout cycle finds opportunities. Today's architecture treats those opportunities as ephemeral — the candidate roster passes through REVIEW to the operator, gets acted on (or rejected), and the funder docs Scout fetched live nowhere persistent. The next cycle re-discovers the same docs. The institutional knowledge accumulated across cycles — which funders fund what, which programs are dead, which 990-PFs reveal program officers' priorities, which RFAs amend on a cadence — never compounds.

This amendment introduces two complementary registers that capture and grow that institutional knowledge:

1. **Funder Intelligence Database** — workspace-shared corpus of funder-side documents (RFAs, NOFOs/FOAs, agency program pages, foundation 990-PFs, prior-funded-project lists, technical assistance guides, funder annual reports, agency strategic plans). Cross-org reusable. Self-curating — each Scout cycle adds discovered docs. Year 1 has tens of docs. Year 3 has hundreds. Year 5+ becomes a durable competitive moat: "which funders have funded urban-soilless-ag in the last five years and what's their typical award size" answerable from local corpus without re-scraping the web.

2. **Match Database** — per-org Scout reasoning trail. Per-client (Law 3 segmented). Captures which funders Scout proposed for THIS client + why + match score + operator confirmed-fit / operator-rejected / operator-declined-cycle. Feeds lessons-delta — patterns that emerge across cycles inform Scout's future runs for the same client.

Both registers use the same substrate as KFR Intake (FAISS or Chroma + bge-large-en-v1.5 + Pydantic AI tool composition per v7.0.3). The substrate is shared; the registers are different — funder corpus is per-funder factual, Match Database is per-client matching reasoning.

**Stage-5 cooperative-corpus on-ramp.** Per-client Match Database content is opt-in input to a cooperative shared corpus at Stage 5 (Sovereign Node commons), when client consents. Three consent tiers per the cooperative sovereignty memory: my-eyes-only / matchable-to-opportunities / composable-with-others. v0.1 ships with `consent_tier: my_eyes_only` as default for all Match Database entries; Stage-5 commons is forward-design here, not Stage-1 build.

This amendment is **substantive** — new register schemas, new Scout channel family, new failure code family for Law 3 enforcement on Match Database reads, Stage-5 cooperative-corpus design surface. Requires Thesis round before LOCK.

## §0.1 Register summary at-a-glance (added Cycle 1 — closes Editor E-01)

| Aspect | Funder Intelligence Database (§1) | Match Database (§2) |
|---|---|---|
| Scope | Workspace-shared (cross-org-reusable) | Per-org (Law 3 segmented) |
| On-disk path | `vault_shared/funder_intelligence/` | `orgs/<slug>/match_database/` |
| Content type | Per-funder factual: RFAs / 990-PFs / agency strategic plans / prior-funded lists / etc. | Per-client matching reasoning: which funder, why, match score, operator action, outcome |
| Lifecycle | Additive corpus growth — every Scout cycle adds candidates; quarterly curation prunes / promotes | Per-grant-cycle: Scout proposes → operator confirms / rejects → outcome tracked |
| Default classification | `public` (RFAs / 990-PFs / agency pages are public) | Per-entry; default `shareable`; `narrative_summary_classification` is explicit per-entry |
| Cloud-routable seats can read? | Yes (typically `public`) | Only entries with non-`confidential` classification |
| Stage-5 commons participation | Already public — no consent tier needed at Funder Intel layer | Per-entry consent tier (`my_eyes_only` default; opt-in per cooperative sovereignty memory) |
| Vector substrate | FAISS or Chroma + bge-large-en-v1.5; namespace `funder_intel/` | **No vector index in v0.1 — structured YAML only.** If a future component vectorizes match reasoning, namespace MUST be `match_db/<org_slug>/` and access wrapper validates session slug. |
| Curation owner | Operator in v0.1 (suggested quarterly cadence; companion §5 specifies trigger). v1.x: Archivist seat (per v7.0.6). | Operator in v0.1 (per-cycle, integrated with Scout REVIEW gate). v1.x: Archivist seat (per v7.0.6) for outcome rollup + lessons-delta. |
| Tier of Law 3 sensitivity | LOW (workspace-shared by design) | **P0 — most Law-3-sensitive register in the architecture.** Cross-org reads are blocked by Logician PRE-check (§5 F-MATCH-DB-CROSS-ORG). |

The two registers are orthogonal — Funder Intel grounds claims about THIS funder; Match DB grounds reasoning about THIS client matched against THIS funder. Both feed Scribe at different stages (per §7).

# §1. Funder Intelligence Database schema (new file: `vault_shared/funder_intelligence/register.yaml`)

*(Schema below is illustrative; final field names land alongside §0.5 Interface Index row spec for v7.0.5. Reviewer auditing the schema should treat field names as descriptive of the contract, not as the final on-disk byte-layout.)*

```yaml
schema_version: funder_intelligence.v1
populated_at: <utc-timestamp>
populated_by: <operator_key_id>

# Vector index lives in vault_shared/funder_intelligence/index/ (FAISS or Chroma)
# Register YAML carries metadata; full doc content lives in vault_shared/funder_intelligence/docs/<doc_hash>.{pdf,txt,html}

documents:
  - doc_id: <opaque-uuid>
    funder: <funder name; e.g., "USDA AMS" / "Heinz Endowments" / "Richard King Mellon Foundation">
    funder_type: <federal_agency | regional_authority | state_agency | county | city | private_foundation | community_foundation | corporate_giving | cdfi>
    doc_type: <rfa | nofo | foa | program_page | 990_pf | strategic_plan | annual_report | technical_assistance_guide | prior_funded_list | other>
    doc_title: <e.g., "USDA VAPG FY26 Request for Applications">
    doc_year: <YYYY if applicable>
    discovery:
      channel: <A | B | C | D | E | F | G>  # which Scout channel family found it (G = local corpus discovery via reference from another doc)
      discovered_when: <utc-timestamp>
      discovered_by: <scout_session_id>
      source_url: <where the doc came from on the public web>
    content:
      content_hash: <SHA-3-512 of doc bytes>
      file_path: <vault_shared/funder_intelligence/docs/<doc_hash>.<ext>>
      bytes_size: <integer>
      pages: <integer if applicable>
      ocr_processed: <true | false>
    relevance:
      score: <0.0 - 1.0; computed at indexing>
      decay_curve: <linear | exponential | none>
      last_relevance_event: <utc-timestamp; promoted by operator action or fresh Scout citation>
    classification: public  # Funder Intelligence Database content is typically Public — RFAs, 990-PFs, agency pages
    cadence: <static | annual | event_driven>
    expiry: <derived; for static-doc archive purposes, no hard expiry>
    promoted: <true | false>  # operator confirmed at first ingestion
    promotion_reason: <text>
    sectors_relevant: [federal_ag, federal_education, regen_food_systems, ...]
    funding_worlds_relevant: [farmer, educator, municipal_steward, arts_culture, cooperative_lead, catalyst]
    tags: [vapg, fy26, value_added, specialty_crop, ...]

audit_chain:
  - operator_signature_at_initial_population
  - operator_signature_per_quarterly_curation_review
```

**Lifecycle:**

1. Scout DISCOVER finds a candidate funder doc via channels A-F.
2. Scout VERIFY fetches the live doc (or pulls from cache).
3. Doc passes through F-EXTRACTOR-FABRICATION-equivalent gate (verbatim content matches expected source).
4. Doc lands in `vault_shared/funder_intelligence/docs/<doc_hash>.<ext>` with metadata in register.yaml.
5. Operator reviews at next quarterly curation pass — promotes (operator-confirmed relevance), rejects (drops with audit trail), or leaves un-promoted (relevance score decays over time).

**Storage substrate.** Same FAISS/Chroma + bge-large-en-v1.5 embedding as KFR Intake. One unified vector store for the workspace, with per-register namespace partition (`kfr_facts/<org_slug>/`, `funder_intel/`, and — IF a future component vectorizes match reasoning — `match_db/<org_slug>/` per Cycle 1 RT-02 closure). The Pydantic AI tool wrapping the vector store MUST require an `org_slug` argument that is validated against the session-bound PROJECT_CONTEXT slug; tool calls with missing or mismatched slug fail-closed via `F-VECTOR-NS-MISMATCH` (per §5; closes Cycle 1 RT-04). v0.1 Match DB is structured YAML only — no vector embedding by default — so the leak surface is zero in v0.1; the namespace requirement is forward-design protection for any future vectorization.

**Lifecycle terminal state (Cycle 1 closure of Judge DC-02).** Documents whose `relevance.score` falls below the configurable threshold `funder_doc_low_relevance_threshold` (default `0.1`) are moved to `vault_shared/funder_intelligence/archive/` and excluded from Channel G default queries. Operator can re-promote at quarterly curation pass (or v1.x Archivist surfaces re-promotion candidates). Archived docs retain `audit_chain` provenance; they are not deleted unless operator-confirmed at quarterly review.

# §2. Match Database schema (new file: `orgs/<slug>/match_database/register.yaml`)

*(Schema below is illustrative; final field names land alongside §0.5 Interface Index row spec for v7.0.5.)*

```yaml
schema_version: match_database.v1
org_slug: <client>
populated_at: <utc-timestamp>
populated_by: <operator_key_id>

matches:
  - match_id: <opaque-uuid>
    funder_doc_id: <reference to vault_shared/funder_intelligence/register.yaml document>
    proposed_at: <utc-timestamp>
    proposed_by: <scout_session_id>
    proposed_for_grant_cycle: <rfa_hash if specific cycle, else null>
    match_score: <0.0 - 1.0>
    match_reasoning:
      structured:
        sector_match: <true | false>
        funding_world_match: <true | false>
        eligibility_match: <true | false>
        scale_match: <true | false>
        identity_match: <true | false>  # SDA / BIPOC / Beginning Farmer / etc.
        geography_match: <true | false>
      narrative_summary: <short text — Scout's match reasoning prose>
      narrative_summary_classification: <public | shareable | confidential>  # narrative may reference confidential client fields; classification governs cloud routing
    operator_action:
      action: <confirmed_fit | rejected | declined_cycle | pending>
      action_when: <utc-timestamp>
      action_reason: <text>
    cycle_outcome:
      outcome: <not_pursued | pursued_drafted_unsubmitted | submitted | awarded | declined | withdrawn>
      outcome_when: <utc-timestamp>
      award_amount: <if awarded>
    consent_tier: <my_eyes_only | matchable_to_opportunities | composable_with_others>  # default: my_eyes_only
    
audit_chain:
  - operator_signature_per_match_action
  - operator_signature_per_consent_tier_change  # Cycle 1 RT-05 closure: every consent_tier mutation captures operator signature + utc-timestamp + reason; immutable append-only
  - law_3_isolation_invariant: "This Match Database file is segregated to org_slug. Cross-org reads blocked by Logician F-MATCH-DB-CROSS-ORG."
  - aggregate_inference_note: "structured boolean fields (sector_match / funding_world_match / eligibility_match / scale_match / identity_match / geography_match) MUST be operator-reviewed at white-glove for aggregate-inference risk; for Stage-5 commons routing per §7 they inherit the narrative_summary_classification."  # Cycle 1 Judge DC-01 closure
```

**Per-org isolation (Law 3).** Match Database files live under `orgs/<slug>/match_database/` and are gated by Logician's existing Law 3 cross-org enforcement. New failure code: `F-MATCH-DB-CROSS-ORG` (any read attempt that crosses org boundaries).

**Lifecycle:**

1. Scout proposes a funder for a client. Match Database entry created with `pending` operator_action.
2. Operator reviews at SP0 of grant cycle (or at separate Scout review): confirmed_fit / rejected / declined_cycle.
3. If pursued: outcome tracked (drafted, submitted, awarded, declined, withdrawn).
4. Lessons-delta integration: Match Database outcomes feed `pipeline/institutional_memory/lessons.json` for pattern detection (e.g., "this funder has rejected this client 3 cycles in a row — surface to operator before next proposal").

# §3. Scout channel augmentation — local corpus query (new channel family G)

Current Scout channel families per `pipeline/blueprint/v0.1/section_03_scout.md`:

- A: Federal APIs (Grants.gov search2 / SAM.gov / USASpending)
- B: Curated cached datasets
- C: Seeded state/foundation portals
- D: Federal program pages
- E: RSS / newsletter watchlists
- F: Client-material-driven web search

**New channel family G — Local discovery corpus.** Scout queries the Funder Intelligence Database alongside the existing six channel families. Yields candidates that are:

- Already in the corpus from prior cycles (operator-confirmed relevance, fresh enough)
- Cross-referenced from corpus docs (e.g., a foundation 990-PF mentions another foundation that funds the same sector — that referenced foundation may not be in any other channel)
- Citation-graph derived (RFAs that cite other RFAs as prior-art frameworks)

Channel G is **parallel primary, not fallback** — same architectural posture as channels A-F per the existing scout-discovery memory. Scout reads all channels in parallel, dedupes, returns union as UNVERIFIED candidates; VERIFY stage applies as usual.

**De-dup against Match Database.** When Scout produces a candidate roster, each candidate is checked against the per-org Match Database. If the funder has a `rejected` action in this client's Match Database within the last N cycles (operator-set, default 1 year), Scout flags the candidate as "previously declined; surface for operator confirmation." Avoids re-pitching rejected funders without operator awareness; preserves operator authority.

**De-dup mechanism is structured-only, not vector-similarity-based (Cycle 1 RT-02 closure).** The de-dup query against the per-org Match DB reads the structured YAML register (filename + `funder_doc_id` + `match_id` keys) — it does NOT issue a vector similarity query. Match DB content is structured-only in v0.1 (per §1); there is no Match DB vector namespace to query. This eliminates any cross-org leak surface via vector similarity at v0.1.

**Channel G cross-reference sanitization (Cycle 1 RT-06 closure + Cycle 2 Probe B closure).** Funder Intel docs may contain references to other orgs' match histories embedded as `match_id` strings (e.g., a funder strategic plan published with anonymized prior-funded examples that include `match_id` metadata). Channel G's extraction pipeline SHALL sanitize any `match_id` reference whose target org slug ≠ the current session's org slug — the reference is redacted before the extracted content reaches downstream Scribe context. Sanitization is a deterministic regex-based pre-pass on extracted text; failure to sanitize an extracted reference triggers `F-CHANNEL-G-CROSS-ORG-LEAK` (per §5; family member of F-MATCH-DB-CROSS-ORG).

**Encoding-evasion guard (Cycle 2 Probe B closure).** The sanitization pre-pass SHALL run a deterministic decode-then-rescan cascade for known encodings (base-64, hex, URL-encoding) BEFORE the regex pass. Any decoded payload that surfaces a canonical `match_id` pattern triggers `F-CHANNEL-G-CROSS-ORG-LEAK` the same as raw matches. Downstream components that further transform extracted text (decoders, format converters, render pipelines) MUST invoke the sanitization wrapper as a POST-transform check; bypass surfaces a runtime `F-CHANNEL-G-SANITIZATION-BYPASS` advisory at the next REVIEW gate.

**Channel G classification filter (Cycle 2 Probe F closure).** Channel G query SHALL filter on `classification == public` by default. Funder Intel docs ingested with `classification: shareable` or `classification: confidential` are excluded from default Channel G queries — operator can override per-session with explicit `--include-confidential-funder-intel` flag (operator-key-id signed; logged to admin-risk register). This prevents inadvertent surfacing of a confidential funder doc to Scribe via Scout's discovery roster.

**Composition with KFR.** Scout's match reasoning narrative may reference KFR facts ("client has 200+ acres in production, matches this RFA's small-farm threshold"). Matching uses KFR's `required_for_funder` tags — KFR facts tagged for this funder are surfaced in match reasoning.

# §4. Stage-5 cooperative-corpus on-ramp (forward-design)

**v0.1 ships zero commons participation (Cycle 1 E-04 closure).** The Sovereign Node commons does NOT exist as runtime infrastructure today. The `consent_tier` field is RESERVED in the schema for forward design only — no v0.1 component reads it for commons routing because no commons-routing code path exists. This section documents the schema's forward shape so v7.0.5 schemas don't have to migrate when Stage 5 lands; nothing in v0.1 / v1.x execution depends on commons existing.

Stage 5 is the Sovereign Node commons (per `project_sovereign_node_stage5.md`). Per-client Match Database content can opt-in to a cooperative shared corpus, with three consent tiers per the cooperative sovereignty memory:

| Consent tier | Behavior |
|---|---|
| `my_eyes_only` (default) | Match Database stays in `orgs/<slug>/match_database/` only. No commons participation. |
| `matchable_to_opportunities` | Sovereign Node commons can match THIS client's match-history to NEW opportunities the commons surfaces, in a way that benefits this client. Other commons participants don't see this client's data. |
| `composable_with_others` | Match Database entries become input to commons-wide pattern detection. Other commons participants can benefit from anonymized aggregate patterns. |

v0.1 ships with `consent_tier: my_eyes_only` as default for all Match Database entries. The schema reserves the field; client opt-in happens at white-glove (per-client default) or per-cycle (per-grant override). Stage 5 (cooperative commons) is forward-design, not Stage-1 build.

**Composition guarantee:** classification-aware split-context per v7.0.7 still applies regardless of consent tier. Even at `composable_with_others`, Confidential client fields stay local; only Public + Shareable content participates in the commons.

# §5. New failure code family — F-MATCH-DB-*, F-FUNDER-CORPUS-*, F-VECTOR-NS-MISMATCH, F-CHANNEL-G-CROSS-ORG-LEAK

(Cycle 1 — substantially elaborated from initial filing to address Red Team RT-01 / RT-03 / RT-04 / RT-05 / RT-07 + Judge DC-01.)

Each gate below is implemented as deterministic Python + Cedar policy, fail-closed by default, zero-token cost. Each gate parses the session-bound `org_slug` from the active PROJECT_CONTEXT.md (a Logician PRE-condition) before any I/O is permitted on the relevant register. Implementation lives in `pipeline/blueprint/v0.1/section_04_logician.md` per §8.

## §5.1 F-MATCH-DB-CROSS-ORG (PRE, fail-closed; closes Cycle 1 RT-01)

**Trigger:** any filesystem path or vector-tool argument that resolves to `orgs/<other_slug>/match_database/...` where `<other_slug>` ≠ the session-bound org slug.

**Enforcement specification (RT-01 closure):**

1. Logician PRE-check #17 (extended for v7.0.5) parses the session-bound `org_slug` from the loaded PROJECT_CONTEXT.md at session start (canonical Law 3 source).
2. Every Match DB read — whether by Scout, Scribe, Editor, Judge, Red Team, or any future agent — is intercepted at the I/O wrapper. The wrapper calls `logician.assert_path_session_scoped(path, session_slug)` BEFORE opening the file.
3. The wrapper validates that `path` matches the regex `^orgs/<session_slug>/match_database/[^/]+\.(yaml|yml|json)$` (exact slug match; no `..` traversal; no symlink follow). Mismatch → wrapper raises `F-MATCH-DB-CROSS-ORG` and aborts the I/O.
4. The Cedar policy expressing this rule lives in `pipeline/vault/policies/match_db_session_scoped.cedar` (created at v7.0.5 LOCK; Logician loads at PRE-check init).
5. Audit-chain event emitted on every PRE-check pass AND fail; failure event includes attempted path + session slug + caller seat + UTC timestamp.
6. **Fail-closed semantics:** the failure code RAISES and ABORTS — it does not log-and-continue. Logician returns control to the orchestrator with the failure code, which surfaces to the operator at the next REVIEW gate.

**Audit-trail row:** every PRE-check produces a `match_db_access_attempt` row in `pipeline/logician/audit/<utc-date>.jsonl` (success and failure both logged).

## §5.2 F-VECTOR-NS-MISMATCH (PRE, fail-closed; closes Cycle 1 RT-04)

**Trigger:** any call to the Pydantic AI vector-store tool (wrapping FAISS or Chroma) where the `org_slug` argument is missing OR does not match the session-bound slug, when the tool is being used to query a per-org-namespaced register (currently `kfr_facts/<org_slug>/`; in forward design, `match_db/<org_slug>/`).

**Enforcement specification:**

1. The Pydantic AI tool definition for `vector_store.search()` declares `org_slug: str` as a REQUIRED argument with no default value.
2. Tool invocation passes through Logician PRE-check #18 which validates `org_slug` against session context.
3. Workspace-scoped namespaces (`funder_intel/`) skip the slug check (no per-org content); per-org namespaces enforce strict slug match.
4. Mismatch or missing slug → raises `F-VECTOR-NS-MISMATCH` and aborts the tool call.
5. **v0.1 Match DB scope:** Match DB is structured YAML only in v0.1 (per §1); F-VECTOR-NS-MISMATCH is forward-design protection that activates if any future component vectorizes match reasoning.

## §5.3 F-CHANNEL-G-CROSS-ORG-LEAK (POST-Channel-G-extract, fail-closed; closes Cycle 1 RT-06)

**Trigger:** an extracted Funder Intel doc payload contains `match_id` references whose target org slug ≠ the current session's org slug, AND the sanitization pre-pass (per §3) failed to redact them.

**Enforcement specification:**

1. Channel G extraction pipeline runs the sanitization regex over extracted text (deterministic; no LLM).
2. POST-extraction Logician check scans the sanitized output for any remaining `match_id` patterns (`match_[a-f0-9]{32}` or equivalent).
3. Any remaining cross-org `match_id` → raises `F-CHANNEL-G-CROSS-ORG-LEAK` and the extracted content is rejected from the Scout candidate roster.

## §5.4 F-MATCH-DB-CONSENT-TIER-VIOLATION (PRE, fail-closed; extended for Cycle 1 RT-05)

**Trigger A (forward-design — Stage-5 only):** a commons-side query attempts to read Match Database content beyond what the consent tier permits. v0.1 always fails this check trivially because no commons-side query path exists.

**Trigger B (v0.1-active — RT-05 closure):** any mutation of a Match DB entry's `consent_tier` field that lacks an `operator_signature_per_consent_tier_change` row in the entry's `audit_chain` with a fresh UTC timestamp.

**Enforcement specification:**

1. Match DB write wrapper validates that ANY change to `consent_tier` is accompanied by an `audit_chain` append capturing operator signature + UTC timestamp + reason.
2. Missing operator signature → raises `F-MATCH-DB-CONSENT-TIER-VIOLATION`; the write is rejected.
3. The signature mechanism is the same operator-key-id pattern used by `audit_chain.operator_signature_per_match_action`.
4. **No silent upgrade path:** an entry cannot move from `my_eyes_only` to `composable_with_others` without operator-signed write — even by the operator's own administrator privileges.

## §5.5 F-FUNDER-CORPUS-STALE (POST-Scout-cite, fail-closed; closes Cycle 1 RT-07)

**Trigger:** a Funder Intelligence Database doc cited in Scout match reasoning OR Scribe draft has `last_relevance_event` older than the per-funder-type stale threshold AND lacks an operator-confirmed promotion in the last threshold window.

**Default thresholds per `funder_type` (Cycle 1 RT-07 closure):**

| funder_type | default `funder_doc_stale_days` |
|---|---|
| `federal_agency` | 365 |
| `regional_authority` | 365 |
| `state_agency` | 365 |
| `private_foundation` | 180 |
| `community_foundation` | 180 |
| `corporate_giving` | 90 |
| `cdfi` | 180 |
| `county` / `city` | 365 |

Operator can override per-doc via `expiry` field; the deterministic check is: `now() - last_relevance_event > stale_threshold`.

**Enforcement specification:**

1. POST-check after Scout's match reasoning composition AND POST-check after Scribe's KGIE preflight.
2. Stale doc cited → raises `F-FUNDER-CORPUS-STALE`; the citation is flagged for operator review at next REVIEW gate; downstream draft is held.

## §5.6 F-FUNDER-CORPUS-INTEGRITY (PRE-load and POST-load, fail-closed; closes Cycle 1 RT-03)

**Trigger:** SHA3-512 hash of stored doc bytes does not match the recorded `content_hash` in `vault_shared/funder_intelligence/register.yaml`.

**Enforcement specification (RT-03 closure — per-read verification, not just ingestion):**

1. **At ingestion:** hash computed from incoming bytes and stored as `content_hash` in the register.
2. **At every load — Cycle 1 strengthening:** the Funder Intel read pipeline wrapper SHALL recompute SHA3-512 of the on-disk bytes and compare against the recorded `content_hash` BEFORE the bytes reach Scout / Scribe / Editor / Judge / Red Team. Mismatch → raises `F-FUNDER-CORPUS-INTEGRITY` and the doc is excluded from the seat's working set.
3. **Frequency:** per-read, not periodic. Every consumer call to `funder_intel.load(doc_id)` triggers re-verification. **Cycle 2 Probe C closure — caching tightened.** Process-scope byte caching is FORBIDDEN; the wrapper MAY cache parsed content (post-verification) within a single agent invocation but MUST recompute SHA3-512 of the on-disk bytes on every `load()` call regardless of prior verification state in the same process. This eliminates the cache-then-tamper-then-reload window.
4. **Fail-closed:** mismatch aborts the load; the failure code surfaces to the operator at the next REVIEW gate; the corrupted/tampered doc is quarantined to `vault_shared/funder_intelligence/_quarantine/<doc_hash>.<ext>` for operator forensics.
5. **Audit:** every PRE-load and POST-load check emits an `funder_intel_integrity_check` row in `pipeline/logician/audit/<utc-date>.jsonl`.

## §5.7 Failure code family summary

| Code | When | Severity | Closure cycle |
|---|---|---|---|
| `F-MATCH-DB-CROSS-ORG` | PRE-Match-DB-read | P0 (Law 3) | Cycle 1 RT-01 |
| `F-VECTOR-NS-MISMATCH` | PRE-vector-tool-call | P0 (Law 3) | Cycle 1 RT-04 |
| `F-CHANNEL-G-CROSS-ORG-LEAK` | POST-Channel-G-extract | P0 (Law 3) | Cycle 1 RT-06 |
| `F-MATCH-DB-CONSENT-TIER-VIOLATION` | PRE-Match-DB-write (consent_tier change) + Stage-5 reads | P1 (Law 4 + sovereignty) | Cycle 1 RT-05 |
| `F-FUNDER-CORPUS-STALE` | POST-cite | P2 (RFA-truth) | Cycle 1 RT-07 |
| `F-FUNDER-CORPUS-INTEGRITY` | PRE-load AND POST-load | P0 (Law 5 — fabrication via tamper) | Cycle 1 RT-03 |

# §6. Curation slot binding (per v7.0.6 Archivist v1.x reservation)

Per v7.0.6 amendment, Archivist is the v1.x candidate seat for between-cycle preservation work. v7.0.5 binds the Funder Intelligence Database curation + Match Database lifecycle management to that slot:

- v0.1: operator-owned curation. Operator reviews `vault_shared/funder_intelligence/` quarterly (suggested cadence; configurable). Operator manages Match Database actions per grant cycle. Curation cadence trigger semantics (when does the operator get the curation prompt — Tilth wake-up / Tilth cron / explicit operator command) live in the companion blueprint `pipeline/blueprint/v0.1/section_05_pipeline.md` per §8 (closes Cycle 1 Editor E-02).
- v1.x: Archivist takes ownership. Quarterly curation becomes Archivist's recurring task. Archivist surfaces stale docs, promotion candidates, integrity check results to operator review at scheduled intervals.

**Slot-owner field (Cycle 1 RT-08 closure).** The schema includes a top-level `curated_by: operator | archivist` field that is updated atomically when the slot transfers from operator (v0.1) to Archivist (v1.x). At slot transfer, the existing `audit_chain` entries are annotated (not deleted) with a transition row capturing transfer date + new owner; subsequent curation events log against the new owner. This prevents the provenance confusion where post-transfer auditors might attribute Archivist-driven changes to operator signatures from prior cycles.

The schema does NOT bake `curated_by: operator` permanently. Curation function is a named slot, not a named owner. v1.x Archivist amendment fills the slot without requiring v7.0.5 schema changes — the field is part of the v0.1 schema; the value transitions at v1.x.

# §7. Composition with v7.0.4 KFR + v7.0.7 classification

**KFR is per-org factual substrate. Funder Intelligence Database is per-funder factual substrate.** Both feed Scribe at different stages:

- KFR grounds Scribe's claims about THIS client (revenue, enrollment, partnerships, credentials)
- Funder Intelligence Database grounds Scribe's claims about THIS funder (priorities, dialect, prior-funded projects, eligibility nuances)
- Both feed Editor's funder-language matching pass
- Both feed Judge's funder-rubric scoring (rubric pulled from Funder Intelligence Database; client claims validated against KFR)

**Classification per v7.0.7:**

- Funder Intelligence Database content is typically `public` — RFAs are public, 990-PFs are public, agency pages are public. Default classification: public.
- **Funder Intel classification validation (Cycle 1 RT-09 closure — deferred to Intake-equivalent gate).** Some funder docs may carry confidential context (pre-grant internal guidance, password-protected portals). Classification validation at ingestion is the same shape as KFR Intake's classification step — Intake (per v7.0.6 + v7.0.4 Intake module spec) flags any doc whose source URL requires authentication and forces `classification: confidential`, requiring operator review before promotion. Defer the implementation to v7.0.4 KFR amendment / Intake module spec; v7.0.5 schemas accommodate the field but the validation gate ships with Intake.
- Match Database `match_reasoning.narrative_summary` may reference confidential client fields. Classification per-entry: explicit field with default `shareable` and operator override available.
- **Aggregate-inference closure (Cycle 1 Judge DC-01 closure).** The `match_reasoning.structured` boolean fields inherit the `narrative_summary_classification` for Stage-5 commons routing — even if the narrative is redacted, the structured field combination must respect the same classification posture. White-glove operator review surfaces aggregate-inference risk at first onboarding.
- Cloud-routable agents (Scribe, Editor, Judge, Red Team) can read Funder Intelligence Database freely. Match Database narrative summaries with `confidential` classification stay local-routed.

**Composition narrative (Cycle 1 E-05 — interface-level).** §0.5 Interface Index v6+ amendments (paired commit at LOCK per §6.17 Option-B) carry the interface-row-level composition between v7.0.5 schemas, KFR (v7.0.4), and the classification register (v7.0.7). The amendment-level narrative here describes the conceptual orthogonality; the interface-level composition is enumerated in §0.5.

# §8. Companion file edits (paired with this amendment)

## pipeline/blueprint/v0.1/section_03_scout.md

- New channel family G: local discovery corpus query
- Match Database de-dup integration
- KFR `required_for_funder` tag query for match reasoning composition

## pipeline/blueprint/v0.1/section_04_logician.md

- New PRE check: F-MATCH-DB-CROSS-ORG enforcement (per §5.1; extends existing Law 3 isolation; session-bound `org_slug` parsed from PROJECT_CONTEXT.md; Cedar policy at `pipeline/vault/policies/match_db_session_scoped.cedar`)
- New PRE check: F-VECTOR-NS-MISMATCH (per §5.2; vector-store tool wrapper validates `org_slug`)
- New POST check: F-CHANNEL-G-CROSS-ORG-LEAK (per §5.3; sanitization regex POST-pass)
- New PRE check: F-MATCH-DB-CONSENT-TIER-VIOLATION (per §5.4; consent_tier mutation requires operator-signed audit_chain entry)
- New POST check: F-FUNDER-CORPUS-STALE on funder citations in drafts (per §5.5; per-funder-type stale defaults)
- New PRE-load AND POST-load check: F-FUNDER-CORPUS-INTEGRITY on every Funder Intelligence Database load (per §5.6; SHA3-512 verification on every read, not just ingestion; per-read frequency)

## pipeline/blueprint/v0.1/section_05_pipeline.md

- Match Database lifecycle integration with grant cycle (proposed → operator action → outcome tracking)
- Quarterly curation cadence for Funder Intelligence Database (operator-set; default quarterly)
- Stage-5 consent tier handling (forward-design; v0.1 always `my_eyes_only`)

## vault_shared/funder_intelligence/

- New directory + register schema
- Initial seed of common funder docs (USDA program pages, NSF general program info, foundation 990-PFs for major regional foundations) at white-glove onboarding by Sovereign Node LLC

## orgs/_TEMPLATE/match_database/

- New directory + register schema
- consent_tier defaults documented
- Per-client population pattern documented

# §9. What this amendment does not do

- Does not modify A1-A12.
- Does not modify the Five Operating Laws or the Four Autonomy Rules.
- Does not modify Section K hardware tier mapping (storage requirements grow with corpus; Pro tier 128 GB still sufficient through Year 3+).
- Does not introduce new council seats — uses v7.0.6 roster.
- Does not modify the v7.0.3 substrate decision (Pydantic AI substrate stands; FAISS/Chroma + bge-large-en-v1.5 substrate aligns with KFR Intake per v7.0.4).
- Does not modify v7.0.4 KFR schema or fact validity model (KFR is per-org factual; Funder Intelligence Database is per-funder factual; orthogonal concerns).
- Does not modify v7.0.7 classification register (Match Database has its own classification field per-entry; Funder Intelligence Database content typically Public).
- Does not specify Stage-5 cooperative-commons commons-side architecture (commons-side is out-of-scope-for-v0.1; Stage-5 amendment forthcoming when that work begins).
- Does not specify v1.x Archivist's curation cadence beyond reserving the slot.
- Does not specify pricing-tier implications of Funder Intelligence Database initial-seeding service (Sovereign Node LLC may seed; biz-plan amendment territory).

# §10. Lock-history note + sequencing

- v7.0.1 (DRAFT): Section E.P Governance Plan Preflight — awaiting Thesis round
- v7.0.2 (SELF-LOCKED 2026-05-04): Section A textual reconciliation
- v7.0.3 (SELF-LOCKED 2026-05-08): Substrate corrective
- v7.0.4 (SCOPING DRAFT 2026-05-08, requires Thesis): KFR Amendment
- v7.0.6 (SCOPING DRAFT 2026-05-08, SELF-LOCK candidate): Roster
- v7.0.7 (SCOPING DRAFT 2026-05-08, requires Thesis): Beta model strategy
- **v7.0.5 (SCOPING DRAFT 2026-05-08, requires Thesis, this file)**: Funder Intelligence Database + Match Database — workspace-shared funder corpus + per-org Scout reasoning trail + Stage-5 cooperative on-ramp

**Sequencing:** v7.0.5 lands after v7.0.6 (uses Archivist curation-slot reservation), composes against v7.0.4 (KFR + Funder Intelligence Database both feed Scribe at different stages — orthogonal substrates), composes against v7.0.7 (classification per-entry on Match Database; Funder Intelligence Database typically Public).

**Thesis-round priorities for v7.0.5 LOCK:**

- Editor pass: clarity of two-register distinction (per-funder vs per-client); operator usability of curation cadence
- Judge pass: rubric scoring against architecture's stated goals (compounding institutional knowledge; Law 3 preservation across Match Database; Stage-5 on-ramp without v0.1 commitment)
- Red Team pass: adversarial — can a Match Database read leak across orgs? Can the cooperative consent tiers be bypassed? Can a funder doc be tampered to mislead Scout?

The Red Team pass on v7.0.5 is critical because Match Database is THE most Law-3-sensitive register in the architecture. Any cross-org leak path is a P0 architecture bug.

**Cycle 1 status (2026-05-09).** Cross-family Audit #1 dispatched via openclaw gateway:

- Editor (Llama 3.3 70B / Groq, Meta family): REQUIRES_FIX — 5 documentary findings (E-01..E-05; 2 MED + 3 LOW)
- Judge (Gemini 2.5 Pro / Google): REQUIRES_FIX 97/100 — 2 LOW design concerns (DC-01 + DC-02)
- Red Team (GPT-OSS 120B / Groq, OpenAI-OSS family): ESCALATE / blocking:true — 3 HIGH (RT-01 + RT-02 + RT-03) + 3 MED (RT-04 + RT-05 + RT-06) + 3 LOW (RT-07 + RT-08 + RT-09)

Cycle 1 fixes applied in this amendment text 2026-05-09 (synthesis at `pipeline/validation/v7_0_5_thesis_2026-05-09/audit_v1_synthesis.md`):

- §0.1 register summary added (E-01)
- §1 illustrative-disclaimer + Match-DB-structured-only + lifecycle terminal state + per-org vector namespace (E-03 + DC-02 + RT-02 + RT-04)
- §2 illustrative-disclaimer + audit_chain consent_tier signature + aggregate-inference note (E-03 + RT-05 + DC-01)
- §3 dedup-mechanism-clarification + Channel G sanitization (RT-02 + RT-06)
- §4 Stage-5 boundary strengthening (E-04)
- §5 substantially elaborated — six failure codes with deterministic enforcement specs (RT-01 + RT-03 + RT-04 + RT-05 + RT-06 + RT-07)
- §6 curated_by slot-owner field + cadence companion ref (RT-08 + E-02)
- §7 classification validation defer + aggregate-inference + composition note (RT-09 + DC-01 + E-05)

**Cycle 2 status (2026-05-10).** Cross-family Audit #2 dispatched via openclaw gateway:

- Editor (Llama 3.3 70B / Groq, Meta family): **READY_TO_LOCK** — all 5 Cycle 1 findings CLOSED; zero new findings.
- Judge (Gemini 2.5 Pro / Google): **READY_TO_LOCK** — both Cycle 1 design concerns CLOSED; rubric 100/100; "design is more robust after the fixes than before."
- Red Team (GPT-OSS 120B / Groq, OpenAI-OSS family): **REQUIRES_MINOR_FIXES** — all 9 Cycle 1 findings CLOSED (zero HIGH remaining open); 4 new Cycle 2 probes surfaced:
  - Probe A (latent P0, OUT_OF_SCOPE-LATENT per Red Team's own framing — "out-of-scope for v0.1 because the current code-base has no such plug-in"): raw filesystem bypass not prohibited at OS-sandbox level. **Disposition: OUT_OF_SCOPE-LATENT.** No v0.1 component has unrestricted FS access; future plug-in surface is a v0.2+ ADR concern, not a v7.0.5 amendment defect.
  - Probe B (P1, encoded `match_id` evades regex): **Disposition: FOLDED_IN** at §3 — encoding-evasion guard (decode-then-rescan cascade for base-64/hex/URL-encoding; downstream-transform sanitization re-invocation requirement).
  - Probe C (P1, process-scope cache skips re-hash): **Disposition: FOLDED_IN** at §5.6.3 — process-scope byte caching FORBIDDEN; per-`load()` re-hash required regardless of prior verification.
  - Probe F (P1, Channel G doesn't filter on `classification`): **Disposition: FOLDED_IN** at §3 — Channel G query default-filters on `classification == public`; non-public docs require explicit operator-signed override.

**LOCK posture.** Per row-170 precedent (§4 v2.4/v2.5 LOCKED 2026-05-08 with BLOCKING-dispositioned-REJECTED findings), v7.0.5 LOCKs at this point with the Cycle 2 disposition manifest above. The 3 P1 closures are inline corrective edits at LOCK (not a silent third audit round — transparent disposition matching the v2.4/v2.5 pattern; closures are Red Team's own recommendations, not author-invented). The 1 OUT_OF_SCOPE-LATENT finding is forward-tracked as a v0.2+ ADR concern (not a v7.0.5 defect). All 9 Cycle 1 HIGH/MED/LOW findings closed unambiguously.

**Forward-pending follow-up.** A Stage-5-readiness amendment (v0.2+) will revisit Probe A's raw-FS bypass concern when (a) plug-in / third-party tool surface is being designed, AND (b) commons-side architecture is being scoped. Not blocking for v7.0.5 LOCK.
