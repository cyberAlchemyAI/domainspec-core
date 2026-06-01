---
title: Tilth Architecture — Amendment v7.0.12 (Apolitical Dialect Routing — retire four-axis political enum; re-ground Law 4 in CLC-keyed register state)
filed: 2026-05-15
operator: Josh Inklovich
amendment_status: LOCKED 2026-05-16T14:00:00Z. L-005 strict two-cycle Thesis CLOSED 2026-05-16 PM (Editor=groq/llama-3.3-70b-versatile + Judge=google/gemini-2.5-pro + Red Team=groq/openai/gpt-oss-120b via osascript→openclaw bridge). Verdict: READY_TO_LOCK. 28 fold-ins applied (12 Cycle 1 + 16 Cycle 2) per per-amendment appendix section appended below. Single `lock_timestamp_utc=2026-05-16T14:00:00Z` per §6.17 Option-B (4-amendment compound: architecture v7.0.12 + §18 v1.2 + §4 v2.x apolitical_dialect + §0.5 v28 — rebased from pre-staged v27 due to coordination conflict with CC-007 §0.5 v27 LOCK at lock_history row 233). Cards + admin_risk_register re-sign + Wave 2 LOCK deferred to separate ceremony per operator-confirmed Option B split (22-36 hour pre-ceremony operator work required first). Audit trail: `pipeline/validation/v7_0_12_thesis_2026-05-16/`.
parent_lock: pipeline/architecture/v0.1/tilth_architecture_locked.md
parent_amendments_chain:
  - v7.0.7 (LOCKED 2026-05-10; row 180) — classification-driven routing. **LOAD-BEARING PRECEDENT for §1.4 below — register-state field carries the same operator-signed discipline as the classification register.**
  - v7.0.8 (LOCKED 2026-05-08) — CIC × CLC orthogonality F-CIC-CLC-COUPLING-VIOLATION enforcement. **LOAD-BEARING PRECEDENT for §1.3 below — F-DIALECT-POLITICAL-AXIS-LEAK extends the same static-detection-plus-runtime-fail-closed posture; CLC enum reused unchanged.**
  - v7.0.10 (LOCKED 2026-05-11; row 215) — three-posture routing vocabulary.
  - v7.0.11 (DRAFT — pending L-005) — Card System. **Companion amendment — CIC card schema's `dialect_routing_table.funder_political_axis` enum is retired by this amendment; replaced by `dialect_routing_table.clc` keyed off the CLC enum.**
companion_amendments_pending_LOCK:
  - pipeline/blueprint/v0.1/section_04_logician_v2_x_apolitical_dialect.md      # §4 v2.x.4 F-DIALECT-POLITICAL-AXIS-LEAK predicate (DRAFT)
  - pipeline/blueprint/v0.1/section_00_5_apolitical_dialect_amendment.md         # §0.5 v?? paired-commit (DRAFT)
  - pipeline/blueprint/v0.1/section_18_v1_2_amendment.md                          # §18 v1.2 narrow-corrective CIC schema item-shape extension (DRAFT)
authority_source: Operator directive 2026-05-15 ("Retire the four political axes, route dialect off CLC instead"). Operator recall — direction conceptually decided in earlier session; never amended into lock chain. This amendment closes the gap. Confirms Law 4's own "apolitical sector language" mandate by removing the political-axis enumeration from the system substrate. Universal `per_clc_register` on every admin_risk_register entry per operator scoping 2026-05-15. Runtime fail-closed posture matching v7.0.8's F-CIC-CLC-COUPLING-VIOLATION per operator scoping 2026-05-15.
version_wording_discipline: "DRAFT" inside this file means "not yet LOCKED via L-005 two-cycle audit." The file shape, frontmatter, and section structure are LOCK-ready — Editor / Judge / Red Team can run the cross-family Thesis round directly against this file. Any LOCK ceremony updates this frontmatter to "amendment_status: LOCKED <date> ..." with cycle-1 + cycle-2 dispositions, appends a lock_history row, and triggers the companion-amendment paired-commit per §6.17 Option-B (atomic compound LOCK across the four amendments at the same `lock_timestamp_utc`).
audit_trail: pipeline/validation/v7_0_12_thesis_<date>/  # populated when L-005 round dispatches
session_metrics: pipeline/metrics/session_log.jsonl
---

# Amendment intent

Law 4 of Tilth's Five Operating Laws is titled *"Apolitical Sector Language + Admin-Risk Term Scanning."* The current substrate violates that title at its own load-bearing layer: the CIC card schema (per v7.0.11 DRAFT and the post-Alpha revised source doc) carries a `dialect_routing_table` whose key field is `funder_political_axis` with enum values `conservative | centrist | progressive | soul_fire`. The admin-risk register (v2.2 LOCKED) carries a parallel `progressive_register` field with values `AVOID | OK | EXPECTED | PREFERRED` against the same four-category political taxonomy.

This is a Law 4 self-contradiction. The system claims apolitical sector handling while encoding a four-axis political enumeration in its register-routing primitives. Politics is also a poor proxy for the actual signal: the same funder body uses different acceptable language program-by-program (NEA Challenge America rewards different vocabulary than NEA Our Town — same agency, different register), and that variation is not captured by a single political-axis label per funder.

**Capital Logic is the actual underwriting frame.** Each of the eight CLCs has a coherent reviewer-vocabulary profile rooted in *what the funder is doing with the capital*, not in *what political bucket the funder occupies*. A Catalytic Change reviewer expects systems-change register regardless of whether the funding agency reads as conservative or progressive on other axes. A Sponsorship & Corporate Support reviewer expects audience-and-brand register regardless of who the sponsor is. CLC-keyed register state matches the actual signal.

**v7.0.12 retires the four-axis political enum.** It replaces `funder_political_axis` on the CIC card's `dialect_routing_table` with `clc` (one of the eight canonical CLC slugs from v7.0.8's `CapitalLogicCard` enum). It replaces `progressive_register` on every admin-risk register entry with `per_clc_register` (a map of CLC slug → AVOID|OK|EXPECTED|PREFERRED, defaulting to AVOID for unlisted CLCs). It introduces `F-DIALECT-POLITICAL-AXIS-LEAK` as a runtime fail-closed gate (matching v7.0.8's F-CIC-CLC-COUPLING-VIOLATION posture) plus an AST-lint rule that catches surviving political-axis literals at design time.

The amendment is intentionally narrow:

- **§1 (this amendment)** retires the political-axis enum, specifies the CLC-keyed replacement, and registers the F-* gate.
- **§4 v2.x.4 (paired Logician amendment, DRAFT)** authors the F-DIALECT-POLITICAL-AXIS-LEAK predicate signatures + AST-lint rule.
- **§0.5 (paired interface-index amendment, DRAFT)** registers the new primitive + failure code + AST-lint rule.
- **§18 v1.2 (paired blueprint section, DRAFT)** refines the CIC card schema's `dialect_routing_table` item shape per the §18 v1.1 narrow-corrective + schema-item-shape-extension precedent (§0.5 v26).

All four LOCK atomically at the same `lock_timestamp_utc` per §6.17 Option-B (compound-paired-commit pattern established by §17 WPFA + §16 Reflection Packet + §13 Data Collector + §14 Report Generator).

# What changes

## §1. Apolitical Dialect Routing as architectural primitive

### §1.1 Retirement: four-axis political enum

The following surface vocabulary is RETIRED from the v0.1 architecture, all blueprint sections, all CIC cards, all admin-risk register entries, all seat code, all skill prompts, and all agent specs at v7.0.12 LOCK:

| Retired surface | Location |
|---|---|
| `funder_political_axis` enum field | CIC card schema `dialect_routing_table` items |
| `conservative \| centrist \| progressive \| soul_fire` enum values | Anywhere they appear as routing-relevant literals |
| `progressive_register` field | admin_risk_register entries |
| `funder dialect code-switching (conservative/centrist/progressive/soul-fire)` phrase | CLAUDE.md Law 4 text |

**Excluded from retirement scope** (preserved as historical record, audit trail, or natural-language analytic copy):

- `pipeline/engineering/lock_history.v1.jsonl` — historical record; never edited in place per workspace discipline.
- `pipeline/architecture/v0.1/tilth_architecture_locked_v4_2026-04-16.md` through `tilth_architecture_locked_v7_a1_a6_2026-04-19.md` — version-trail history files; preserved verbatim per architecture audit-trail discipline.
- `pipeline/institutional_memory/admin_risk_register.yaml` `expansion_cycles:` block — taxonomic history of how the register grew (v1 → v2 → v2.1 → v2.2 → v2.3). The block describes the *evolution* of dialect discipline and must mention the retired four-axis framing factually; this is audit copy, not production routing data.
- Any natural-language prose inside doc files that reads "Josh's four-category political taxonomy" or similar as a factual reference to the *prior* state of the system — such prose may be updated for clarity at sweep time but its preservation does not violate Law 4 (description-of-history ≠ encoding-as-routing-primitive).

The F-DIALECT-POLITICAL-AXIS-LEAK gate (§1.3 below) implements the exclusion list as a path allowlist; matches inside the excluded paths do not trip the gate.

### §1.2 Replacement: CLC-keyed register state

**On the CIC card `dialect_routing_table`:**

```yaml
# OLD (retired):
dialect_routing_table:
  - funder_political_axis: "conservative | centrist | progressive | soul_fire"
    dialect: "Scribe sub-mode"
    example_funder: "optional"

# NEW (per v7.0.12):
dialect_routing_table:
  - clc: "<one of the eight canonical CapitalLogicCard slugs per v7.0.8>"
    register: "Scribe sub-mode keyed to this CLC's reviewer expectations"
    example_program: "optional — specific program inside the CLC; useful for cases where program-internal variation exists within one CLC (e.g., NEA Challenge America vs Our Town both under sponsorship_corporate)"
```

**On every admin_risk_register entry** (universal — no per-entry conditional; entries that previously lacked `progressive_register` gain the new field with default `{}` meaning AVOID-everywhere):

```yaml
# OLD (retired):
- flagged_term: "<term>"
  severity: RED | YELLOW | GREEN
  progressive_register: AVOID | OK | EXPECTED | PREFERRED
  # ... other fields unchanged

# NEW (per v7.0.12):
- flagged_term: "<term>"
  severity: RED | YELLOW | GREEN
  per_clc_register:
    <clc_slug_1>: AVOID | OK | EXPECTED | PREFERRED
    <clc_slug_2>: AVOID | OK | EXPECTED | PREFERRED
    # ... only CLCs where the term's acceptability differs from default need to be listed
  # ... other fields unchanged
```

**Default semantics:** any CLC not listed in `per_clc_register` defaults to `AVOID`. Empty `per_clc_register: {}` means "AVOID across all eight CLCs" — the safest default for any newly-added or unmigrated entry. Operator approves every substitution at draft time (Law 4 unchanged).

**Reverse-lookup helper:** the Logician exposes `term_acceptable_under_clc(term: str, clc: CapitalLogicCard) -> Literal["AVOID","OK","EXPECTED","PREFERRED"]` reading the register; this is the only sanctioned read path for dialect-routing decisions at draft time. Direct field access by seat code is forbidden (forces all routing decisions through the Logician audit chain).

### §1.3 F-DIALECT-POLITICAL-AXIS-LEAK (PRE, runtime + AST-lint, fail-closed)

**Fires at:** Tilth startup AND on any config refresh (router.yaml reload, knowledge-pack reload, PROJECT_CONTEXT.md edit, prompt-template recompile, CIC card load, admin_risk_register reload). Also at AST-lint time during commit hooks.

**Detects:** any surviving political-axis literal or field name in production code paths, cards, schemas, prompt templates, knowledge packs, or vault files. Detection runs three layers; any layer's match trips the gate.

**Layer 1 — Lexical pattern (regex on field names and string literals).**

The following patterns are forbidden outside the excluded paths in §1.1:

- Field name regex: `^(funder_political_axis|progressive_register)$` — exact field-name match.
- String-literal regex: `\b(conservative|centrist|progressive|soul_fire|soul-fire)\b` inside YAML/JSON values OR Python string literals OR prompt-template strings, **when the surrounding context is a routing-relevant field** (defined as: any field whose type is `Literal[...]` enumerating two or more of the retired values, OR any field named in a v7.0.12-retired position per §1.1, OR any prompt template substituted into a Scribe/Editor/Judge/Red Team/Scout/Logician runtime call).
- Pure prose references to these words in natural-language doc copy do NOT trip Layer 1 — the regex is gated on routing-relevant context per the surrounding-context check above. A blueprint paragraph that reads "the prior architecture used a conservative/centrist/progressive/soul_fire taxonomy" is fine; a YAML enum or Python `Literal` carrying those values trips closed.

**Layer 2 — Pydantic AST inspection.**

Static AST walk over all files matching `pipeline/**/*.py`. Flags any Pydantic model field whose annotation is `Literal[...]` containing two or more of `"conservative"`, `"centrist"`, `"progressive"`, `"soul_fire"`, or `"soul-fire"`. Same scope as the v7.0.8 F-CIC-CLC-COUPLING-VIOLATION AST walk; same exclusion list.

**Layer 3 — Card + register schema validation.**

CIC card schemas (`pipeline/cards/_schema/card_cic.schema.json`) explicitly forbid the `funder_political_axis` property name on `dialect_routing_table` items. The admin_risk_register schema explicitly forbids the `progressive_register` field on entries. Both schemas explicitly require the new replacement fields (`clc` and `per_clc_register` respectively). Any card or register file failing this validation at load time surfaces as F-DIALECT-POLITICAL-AXIS-LEAK.

**Fail mode:** fail-closed. Tilth refuses to start (Layer 1 + Layer 2 + Layer 3 fire at startup) or refuses to load the offending artifact (card or register reload). F-DIALECT-POLITICAL-AXIS-LEAK ledger entry, HIGH severity, operator escalation. Detection rationale (which layer caught it) + offending file path + line number + matched pattern surface to operator for fix. Subcodes:

- `F-DIALECT-POLITICAL-AXIS-LEAK.field_name` — retired field name found in production schema or vault file (Layer 1 field-name match).
- `F-DIALECT-POLITICAL-AXIS-LEAK.routing_literal` — retired enum literal found in a routing-relevant context (Layer 1 literal + surrounding-context match).
- `F-DIALECT-POLITICAL-AXIS-LEAK.pydantic_literal` — Pydantic `Literal[...]` annotation contains retired values (Layer 2).
- `F-DIALECT-POLITICAL-AXIS-LEAK.schema_property` — CIC card or admin_risk_register schema fails strict-validation per §1.3 Layer 3.

**Recovery:** offending literal is renamed to a CLC slug (for routing fields) or removed entirely (for prose); schema validation passes; Tilth starts. The AST-lint rule R-NO-POLITICAL-AXIS-LITERAL (registered at §0.5 paired-commit) prevents reintroduction via commit hook.

**Why runtime, not static-only:** matches v7.0.8's F-CIC-CLC-COUPLING-VIOLATION posture. Static AST-lint catches design-time bugs at commit time; runtime fail-closed catches vault/card/register reloads that bypass commit hooks (e.g., operator manually edits a card in production). Both layers give the Logician audit teeth.

### §1.4 Operator-signed register-state discipline

Per BT9 hash-chain audit precedent (v7.0.4 KFR + v7.0.7 classification register), every admin_risk_register file under `pipeline/institutional_memory/` carries an operator Ed25519 signature on its canonical-bytes hash. Migration from v2.3 (last LOCKED with `progressive_register`) to a v3.0 release (first LOCKED with `per_clc_register`) requires operator re-signing of the canonical bytes per BT9 discipline.

CIC cards under `pipeline/cards/CIC/` follow the same signed-card discipline per v7.0.11 §1; the schema swap from `funder_political_axis` to `clc` requires re-signing of each card at v7.0.12 LOCK.

### §1.5 Migration: one-shot rewrite, no dormancy window

Unlike v7.0.8's per-org dormancy for F-CIC-CLC-MATCH-NULL, F-DIALECT-POLITICAL-AXIS-LEAK has no dormancy window. The retired surface vocabulary is workspace-wide and design-time, not per-org runtime data. At v7.0.12 LOCK, every file in the touched-file list (§5 below) is updated in a single sweep transaction; failure-to-update on any file fails the LOCK ceremony.

Rationale: dormancy windows exist for per-cycle runtime data conditions that legitimately take time to populate (per-org Intake, per-org CIC selection). The retirement here is a static refactor — every file's edit is determinable at LOCK time from the file's current contents plus the swap rules in §1.2. No legitimate reason to defer.

## §2. What this amendment does not do

- Does not modify Law 4's "Admin-Risk Term Scanning" arm — flagged-term severity tiers, term entries, substitution-candidates discipline, applicant-approves-every-substitution rule all unchanged.
- Does not change CLC enum membership (still 8 per v7.0.8; closed set; F-CIC-CLC-ENUM-DRIFT continues to enforce).
- Does not change CIC enum membership (still 6 per v7.0.8; closed set).
- Does not modify CIC × CLC orthogonality (v7.0.8 territory; CLC slugs are the *key* for dialect routing, not a coupling-binding from CIC archetypes to CLC subsets — every CIC's `dialect_routing_table` may reference any CLC).
- Does not modify routing posture (v7.0.7 territory; classification posture is orthogonal to dialect routing).
- Does not modify the council seat roster (v7.0.6 territory).
- Does not modify the Five Operating Laws — Law 4's *text* updates per §1.1 to reflect the apolitical posture in fact, not just in name; the *substance* of Law 4 was always apolitical, this amendment makes the substrate honest.
- Does not modify Scribe's underlying register-rendering capability — the same four `dialect` sub-modes (formal / conversational / movement / hybrid per §18 CIC schema `register_defaults.language_register`) survive unchanged. Only the *routing key* changes (CLC instead of political axis).
- Does not introduce a fifth or sixth `register_defaults.language_register` value. The schema's `formal | conversational | movement | hybrid` enum is untouched. The dialect codebook at `pipeline/engineering/agents/references/dialect_codebook.yaml` keeps its existing register entries; only the keying mechanism changes.

## §3. Failure-code primitives added

**One new failure code** (total at v7.0.12 = v7.0.8's 34 + v7.0.9's reflection family + v7.0.10's posture family + v7.0.11's F-CARDS-* family + this one):

- **F-DIALECT-POLITICAL-AXIS-LEAK** (PRE, runtime + AST-lint, fail-closed at PRE-gate order 6.55 — between v7.0.8's F-CIC-CLC-COUPLING-VIOLATION at 6.5 and F-CIC-CLC-MATCH-NULL at 6.6, because dialect routing operates on the CLC enum and presumes coupling-violation discipline is already clean). HIGH severity. Subcodes: `.field_name`, `.routing_literal`, `.pydantic_literal`, `.schema_property`. Recovery via static rename + re-sign; AST-lint rule R-NO-POLITICAL-AXIS-LITERAL prevents reintroduction.

**One new AST-lint rule:**

- **R-NO-POLITICAL-AXIS-LITERAL** — commit-hook static check. Same regex as Layer 1 + Layer 2 of F-DIALECT-POLITICAL-AXIS-LEAK. Same exclusion paths. Blocks commits that reintroduce retired vocabulary. Matches the v7.0.8 R-NO-CIC-CLC-COUPLING-LITERAL AST-lint pattern.

Zero new Cedar rules (deterministic Python + AST walk suffices).

Zero new Pydantic enum types (reuses v7.0.8's `CapitalLogicCard` for the CLC slug routing key).

Zero new M-family mechanisms.

## §4. Gate ordering

In v7's PRE-gate precedence table, the new gate inserts as follows:

| Order | Gate | Scope |
|---|---|---|
| 6.45 | F-CIC-CLC-ENUM-DRIFT | Canonical enum integrity (v7.0.8) |
| 6.5 | F-CIC-CLC-COUPLING-VIOLATION | CIC × CLC structural decoupling (v7.0.8) |
| **6.55** | **F-DIALECT-POLITICAL-AXIS-LEAK** | **Political-axis enum residual detection (v7.0.12)** |
| 6.6 | F-CIC-CLC-MATCH-NULL | CIC × CLC runtime presence (v7.0.8) |
| 6.7 | F-MULTI-CIC-CHOICE-UNRESOLVED | Multi-CIC select-one-per-grant (v7.0.8) |

Dialect-axis leak fires after coupling-violation (it presumes the CIC×CLC orthogonality is enforced — the new `clc` routing key uses v7.0.8's enum) and before match-null (orthogonal to whether match data is present).

## §5. Touched files at LOCK (one-shot rewrite per §1.5)

The amendment LOCK ceremony rewrites the following ~25 files in one transaction. Rewrite content is determinable from current contents + §1.2 swap rules.

**Substrate code + schema:**

- `pipeline/cards/_schema/card_cic.schema.json` — drop `funder_political_axis` property; add `clc` property (enum reused from `pipeline/types/identity_capital.py` `CapitalLogicCard`); add `register` + `example_program` properties.
- `pipeline/seats/scribe/dialect.py` — rename routing function signatures; CLC slug as the keying argument.
- `pipeline/engineering/agents/references/dialect_codebook.yaml` — re-key entries from political axis to CLC slug.
- `pipeline/institutional_memory/admin_risk_register.yaml` — bump version to v3.0; rename `progressive_register` → `per_clc_register` on every entry (~75 entries per v2.3); operator re-sign at LOCK.
- All six `pipeline/cards/CIC/*.yaml` cards — rewrite `dialect_routing_table` items per §1.2; operator re-sign at LOCK.

**Blueprint + doc copy:**

- `pipeline/blueprint/v0.1/section_07_scribe.md` — references to political-axis routing rewritten to CLC-keyed routing.
- `pipeline/blueprint/v0.1/section_10_red_team.md` — same.
- `pipeline/blueprint/v0.1/section_18_card_system.md` — schema item-shape extension per §18 v1.2 narrow-corrective.
- `docs/post_alpha/post_alpha_card_system_revised_2026-05-15.md` — source-doc footnote at the bottom flagging the schema swap (this file is a preserved revised source doc; the footnote acknowledges supersession by v7.0.12 LOCK).

**Skill prompts:**

- `skills/scribe-ghostwriter/SKILL.md` and `skills/scribe-ghostwriter/report_mode_prompts/narrative.md`
- `skills/judge-rubric/SKILL.md`
- `skills/red-team/report_mode_probes/narrative.md`
- `skills/site-reviewer/SKILL.md`

**Agent specs:**

- `pipeline/engineering/agents/scribe_writer_agent_v1.md`
- `pipeline/engineering/agents/scout_discovery_agent_v1.md`
- `pipeline/engineering/agents/judge_scoring_agent_v1.md`

**Operator-readable orientation:**

- `CLAUDE.md` — Law 4 text per §1.1 replacement language; "What NOT to Do" list adds: *"Do not use the retired four-axis political enumeration (`conservative | centrist | progressive | soul_fire`) anywhere in routing-relevant code, cards, or registers — F-DIALECT-POLITICAL-AXIS-LEAK enforces fail-closed per v7.0.12."*
- `SOUL.md` — any Law 4 reference brought into alignment.
- `pipeline/SESSION_BOOTSTRAP.md` — orientation copy updated to describe CLC-keyed dialect routing.
- `pipeline/templates/component_analysis_template.md` — Law 4 reference updated.

**Tests:**

- `pipeline/seats/scribe/tests/test_dialect.py` — re-key fixtures.
- Tests under `pipeline/logician/` for the new F-* gate predicate.

Total: ~25 production files + tests + card re-signing + register re-signing.

## §6. Lock-history note + sequencing

- v7.0.11 (DRAFT — pending L-005) — Card System. v7.0.12 is **strongly preferred to LOCK before or alongside v7.0.11**, because v7.0.11's CIC card schema (as drafted) still carries the retired `funder_political_axis` field. If v7.0.11 LOCKs first, v7.0.12 LOCK includes a narrow-corrective edit to the LOCKED v7.0.11 schema (per §18 v1.1 narrow-corrective + schema-item-shape-extension precedent at §0.5 v26). If v7.0.12 LOCKs first, v7.0.11's pending DRAFT updates before its LOCK ceremony.
- **Joint LOCK strongly preferred** if Thesis rounds align — v7.0.11 + v7.0.12 land together as a single compound paired-commit, since the CIC card schema is touched by both. This is the cleanest path.
- v7.0.12 (DRAFT, this file, requires Thesis round before LOCK).

**Thesis-round preparation (for v7.0.12 LOCK):**

- **Editor pass**: clarity of the political-axis retirement scope; clarity of the CLC-keyed replacement schema; clarity of the exclusion-path discipline (audit-history files preserved, prose references preserved, routing-relevant literals retired).
- **Judge pass**: rubric scoring against Law 4's apolitical mandate — does the retirement actually eliminate the political-axis substrate, or does a back-channel survive? Specifically: are there code paths that read political-axis labels from external sources (e.g., funder-database fields) and would survive the retirement by sourcing the routing key from a non-CIC-card location?
- **Red Team pass**: adversarial. Worst-case scenarios:
  1. An operator edits a CIC card to reintroduce `funder_political_axis` after LOCK. Does Layer 3 (schema validation) catch it at card reload? (It should — the schema explicitly forbids the property name.)
  2. An adversary renames `funder_political_axis` to `funder_lean_axis` in a vault file, preserving the four-value enum. Does Layer 1 (regex on enum values) catch it? (It should — the literal regex on `conservative|centrist|progressive|soul_fire` is independent of the field name.)
  3. A skill prompt template carries the retired vocabulary in natural-language prose ("write for a conservative reviewer"). Does Layer 1 fire? (It should NOT — the surrounding-context check requires routing-relevant context; prose inside a prompt template that's not interpolated into a routing decision is fine. **This is a calibration concern for Red Team to test against the edge.**)
  4. The exclusion-path list for `lock_history.v1.jsonl` and archived architecture files lets a malicious edit hide retired vocabulary inside an "audit history" file that's actually re-read at runtime. What's the read-path discipline?
  5. The CLC-keyed routing produces a dialect mismatch (e.g., a `public_purpose_works` opportunity from a private foundation with progressive priors gets the civic-formal register instead of the foundation-friendly register the funder actually expects). How does Editor + Judge + Red Team catch this without falling back to political-axis labels?

The Red Team pass is critical — the Law 4 self-contradiction was load-bearing for years; the retirement is non-negotiable for the apolitical claim, but the new routing must actually produce better drafts than the retired one in practice.

**Companion file edits batch** (lands when v7.0.12 LOCKs, joint with v7.0.11 if Thesis aligns):

The full ~25-file touched list per §5 above lands at LOCK transaction. Failure to update any file fails the LOCK ceremony.


---

# §7. Cycle 1 + Cycle 2 fold-ins applied at LOCK 2026-05-16T14:00:00Z

L-005 strict two-cycle Thesis CLOSED 2026-05-16. Verdict: READY_TO_LOCK (Editor PASS + Judge READY_TO_LOCK 98/100 + Red Team REQUIRES_FIXES blocking yes with ALL probes row-170 fold-in-at-LOCK-addressable). Audit trail: `pipeline/validation/v7_0_12_thesis_2026-05-16/`. Per row-170 transparent disposition, the fold-ins below are baked into this LOCKed canonical bytes.

## Cycle 1 fold-ins applicable to this amendment (verbatim patches in `cycle_1/foldins_applied.md`)

- **FI-1 (closes ED-1)**: §1.3 Layer 1 — add concrete-criteria table distinguishing routing-relevant vs prose-only contexts (path-scope + schema-bound enum field + Pydantic Literal + prompt-template substitution).
- **FI-7 REVISED (closes RT-5)**: §1.2 admin_risk_register replacement — **AVOID-everywhere default**; **NO inherited mapping** from prior `progressive_register` values (operator pushback 2026-05-16: any heuristic mapping re-encodes the retired axis by stealth; per `feedback_no_heuristic_mapping_on_enum_retirement.md`). Mandatory operator audit at LOCK ceremony (~75 terms × 8 CLCs = ~75 operator decisions × 3-5 min each = 4-6 hours). LOCK gate `F-DIALECT-MIGRATION-INCOMPLETE` (new — see §4 v2.x apolitical_dialect §4.X.6) refuses LOCK if un-audited.
- **FI-8 (closes RT-9)**: §1.5b — two-phase commit migration discipline. Phase 1: stage 25+ files in `vault_shared/v7_0_12_lock_staging/`, schema-validate, operator-sign, SHA3-512-pin. Phase 2: atomic POSIX `rename(2)` per file; reverse-rollback (`.pre_v7_0_12.bak` rename-back) on any failure.
- **FI-10 (closes RT-8) §5 dialect_codebook entry**: rewrite each existing top-level key (currently `<axis>.<sub_mode>`) per per-row operator decisions from FI-9 card rewrite + FI-7 admin-risk audit; **NO prescriptive heuristic**.

## Cycle 2 fold-ins applicable to this amendment (verbatim dispositions in `cycle_2/synthesis.md`)

- **C2-H-5 (strengthens FI-8)**: two-phase commit MUST validate `os.statvfs` same-mount before Phase 2; abort + rollback if cross-mount (POSIX `rename(2)` atomicity only guaranteed on same filesystem; staging on network-attached storage breaks the property).
- **C2-NEW-P0-1 (new)**: extend §1.2 admin_risk_register schema to forbid retired strings (`conservative | centrist | progressive | soul_fire | soul-fire`) as ENUM VALUES of the `clc` field (not just as property name). Closed set: 8 CapitalLogicCard slugs only.
- **JD-C2-LOW-2 (operational reframe)**: operator audit + card rewrite (22-36 hours total) reframed from "at LOCK ceremony" to **"mandatory pre-ceremony gating items."** LOCK ceremony itself is short atomic technical execution — verifies completion of signed `*_decisions.md` audit files BEFORE executing the two-phase atomic commit script. Separates long human-review phase from short atomic technical ceremony.

## Verified Cycle 1 findings — no fold-in needed (confirmed working as designed)

- **RT-1 LOW**: Layer 3 schema validation confirmed catches card edit reintroduction at reload.
- **RT-4 LOW**: exclusion-path list (`lock_history.v1.jsonl` + archived architecture files) confirmed not loaded at runtime → no back-door surface.

## Deferred per row-170 transparent disposition

- **ED-3 LOW** (touched-files completeness audit): FOLD-IN-AT-cards-ceremony per Option B split — operator runs `grep -rn 'funder_political_axis\|progressive_register\|\b(conservative|centrist|progressive|soul_fire|soul-fire)\b' pipeline/ skills/ docs/` and ensures every routing-relevant hit is on the touched-files list during pre-ceremony work.
- **ED-5 LOW** (specific replacement text for CLAUDE.md/SOUL.md/SESSION_BOOTSTRAP.md): operator-drafted at cards-ceremony in operator voice.
- **C2-NEW-LOW-5** (external plugin path-scope): DEFER-TO-V0_2 — plugin loader not exposed at v0.1.

## Disposition summary

- Cycle 1 fold-ins applied: 4 (FI-1, FI-7 REVISED, FI-8, FI-10 §5)
- Cycle 2 fold-ins applied: 3 (C2-H-5, C2-NEW-P0-1, JD-C2-LOW-2)
- Deferred per row-170: 3 (ED-3, ED-5, C2-NEW-LOW-5)
- Verified-working: 2 (RT-1, RT-4)
- **This amendment LOCK fold-in count: 7 applied + 3 deferred + 2 verified-working.**
