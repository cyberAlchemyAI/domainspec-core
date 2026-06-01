---
title: §3 Scout — v7.0.5 companion delta (Channel G + Match DB de-dup + KFR query + sanitization)
filed: 2026-05-10
parent_section: pipeline/blueprint/v0.1/section_03_scout.md
parent_amendment: pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md
status: COMPANION — v7.0.5 LOCKED 2026-05-10 (lock_history row 179)
---

# §3 Scout v7.0.5 companion delta

This companion catalogs the §3 Scout changes registered by architecture amendment v7.0.5 (LOCKED 2026-05-10). Full mechanism specs live in the amendment; this file pins the §3-specific binding for blueprint reviewers.

## §3.G Channel family G — Local discovery corpus query (NEW per v7.0.5 §3)

Scout's existing six channel families (A: Federal APIs / B: Curated cached datasets / C: Seeded portals / D: Federal program pages / E: RSS-newsletter watchlists / F: Client-material-driven web search) gain a seventh **parallel-primary** channel:

**Channel G — Local discovery corpus.** Scout queries the Funder Intelligence Database (`vault_shared/funder_intelligence/`) alongside channels A-F. Yields candidates from prior cycles, cross-references in corpus docs, and citation-graph derivations. Channel G is parallel-primary, not fallback — same architectural posture as A-F.

**De-dup against Match Database.** When Scout produces a candidate roster, each candidate is checked against the per-org Match Database (`orgs/<slug>/match_database/`). If the funder has a `rejected` action in this client's Match Database within the last N cycles (operator-set, default 1 year), Scout flags the candidate as "previously declined; surface for operator confirmation."

**De-dup mechanism is structured-only, not vector-similarity-based.** The de-dup query reads structured YAML keys (filename + funder_doc_id + match_id); it does NOT issue a vector similarity query. Match DB content is structured-only in v0.1 (per v7.0.5 §1); there is no Match DB vector namespace to query at v0.1. Forward-design protection: if a future component vectorizes match reasoning, the namespace MUST be `match_db/<org_slug>/` and the access wrapper validates session slug.

## §3.G.1 Channel G classification filter (Cycle 2 Probe F closure)

Channel G query SHALL filter on `classification == public` by default. Funder Intel docs ingested with `classification: shareable` or `classification: confidential` are excluded from default Channel G queries.

Operator can override per-session with explicit `--include-confidential-funder-intel` flag (operator-key-id signed; logged to admin-risk register). This prevents inadvertent surfacing of a confidential funder doc to Scribe via Scout's discovery roster.

## §3.G.2 Channel G cross-reference sanitization (Cycle 1 RT-06 + Cycle 2 Probe B closures)

Funder Intel docs may contain references to other orgs' match histories embedded as `match_id` strings. Channel G's extraction pipeline SHALL sanitize any `match_id` reference whose target org slug ≠ the current session's org slug — the reference is redacted before the extracted content reaches downstream Scribe context.

**Sanitization pre-pass (deterministic, no LLM):**

1. Decode-then-rescan cascade for known encodings (base-64, hex, URL-encoding) BEFORE the regex pass. Any decoded payload that surfaces a canonical `match_id` pattern (`match_[a-f0-9]{32}` or equivalent) triggers `F-CHANNEL-G-CROSS-ORG-LEAK`.
2. Regex pass on the (now decoded) text scanning for any cross-org match_id reference.
3. POST-extraction Logician check (`F-CHANNEL-G-CROSS-ORG-LEAK`) scans the sanitized output for any remaining patterns; non-empty match → reject candidate from Scout roster.
4. Downstream components that further transform extracted text (decoders, format converters, render pipelines) MUST invoke the sanitization wrapper as a POST-transform check; bypass surfaces a runtime `F-CHANNEL-G-SANITIZATION-BYPASS` advisory at the next REVIEW gate.

## §3.G.3 KFR `required_for_funder` query (composition with v7.0.4)

Scout's match reasoning narrative may reference KFR facts ("client has 200+ acres in production, matches this RFA's small-farm threshold"). When composing match reasoning, Scout queries KFR (`orgs/<slug>/vault/kfr/register.yaml`) for facts tagged `required_for_funder` matching the candidate funder; tagged facts are surfaced in match reasoning.

Match Database `match_reasoning.narrative_summary` is composed with KFR-grounded claims; classification per-entry. v7.0.7 classification routing applies — `confidential` narrative summaries stay local-routed.

## Composition with §5 Pipeline + §4 Logician

- §5 Pipeline calls Scout per cycle; Scout writes Match Database entries with `pending` operator_action.
- §4 Logician's PRE-check #17 (extended for v7.0.5) intercepts Match DB I/O across all six council seats + both support agents that touch Match DB; raises `F-MATCH-DB-CROSS-ORG` on session-slug mismatch.
- §4 Logician's PRE-check #18 (NEW per v7.0.5 §5.2) gates the Pydantic AI vector-store tool with `F-VECTOR-NS-MISMATCH`.

## Failure codes registered (per v7.0.5 §5)

- `F-MATCH-DB-CROSS-ORG` (PRE; closes Cycle 1 RT-01)
- `F-VECTOR-NS-MISMATCH` (PRE; closes Cycle 1 RT-04)
- `F-CHANNEL-G-CROSS-ORG-LEAK` (POST-extract; closes Cycle 1 RT-06)
- `F-CHANNEL-G-SANITIZATION-BYPASS` (advisory; closes Cycle 2 Probe B)

Full enforcement specs at `pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md` §5.
