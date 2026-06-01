# Charter Fidelity Cross-Check Audit — Methodology

> **Status:** v1.0 — piloted on `HEINZ-FOUNDATION` charter on PR #33 (branch `fid-week-1-pillar-1-charters-2026-05-18`), 2026-05-18.
> **Authority:** operator-commissioned 2026-05-18 after a P0 geo-scope fidelity break was caught in the Heinz charter.
> **Ownership:** Pillar-1 Depth Charter quality assurance. Runs **before** operator Ed25519 sign-off.
> **Output paths:** per-charter findings at `pipeline/funder_intelligence/_audits/charter_fidelity_audit_<artifact_id_kebab>_<YYYY-MM-DD>.md` + aggregate roll-up at `pipeline/funder_intelligence/_audits/charter_fidelity_audit_aggregate_<YYYY-MM-DD>.md`.

---

## §1 — Why this audit exists

The Pillar-1 Depth Charters are **load-bearing**. They drive Scout DISCOVER eligibility filtering, Scribe scaffold composition, Judge cross-checks, Red Team probe selection, and Logician PRE-gate firing. A single fidelity break in a charter can:

- Falsely reject good applications (P0 hard-gate fidelity break — e.g., narrowing Heinz scope from SWPA-10-county to Allegheny-only would reject 9 of 10 valid counties)
- Coach Scribe to draft against stale taxonomy (P1 unsupported assertion — e.g., legacy 4-area Heinz taxonomy when funder has refreshed to 7)
- Leave Scribe blind to material constraints (P2 material omission — e.g., individuals/for-profits ineligibility)

The Pillar-1 README's CONJECTURE marker covers Pillar-2-corpus-pending claims, but **does not excuse fidelity breaks against publicly verifiable funder material**. If the funder's own website contradicts the charter, the charter is wrong — `[CONJECTURE]` is not a defense.

This audit fires once per charter, before operator Ed25519 sign-off, with the goal of catching every fidelity break that publicly verifiable sources can reveal.

---

## §2 — Scope

**In scope:**
- All §A `runtime_consumer` `decision_changed` strings (these drive seat behavior at runtime)
- All §B `stage_behavior.screen.pass_fail_triggers` (these drive Scout DISCOVER + Logician PRE-gates)
- All §B `language_register` preferred_terms + suspicious_terms (these drive Scribe register + Editor flags)
- All §B `logician_gate_candidates` (these become Logician PRE-gates after Pillar 2/3)
- All §B `source_backing.corpus_refs` (these anchor F-FID-FACT-ORPHAN promotion at L-005)
- All hard-gate / disqualifier / common-rejection claims in prose
- Geographic scope language
- Funding-range language (median grant size, max award, match %, length)
- Eligibility-entity language (501(c)(3) vs 509(a) vs government vs individuals vs for-profits)
- Application-process language (LOI vs full app, portal, timelines)
- Strategic / thematic / program-area taxonomy

**Out of scope:**
- Codex same-prompt-with/without quality (separate Codex external-validity audit covers this)
- Signature-roundtrip canonicalization (separate `sign_charter` test suite covers this)
- Pillar-2 corpus completeness (separate Pillar-2 dispatch covers this)
- Per-applicant fit (lives in `orgs/<slug>/PROJECT_CONTEXT.md`, not in the charter)
- Reviewer-type heuristics (separate `reviewer_heuristics/` workstream)

---

## §3 — Method

### Step 1 — Inventory load-bearing claims

Read the charter end-to-end. For each load-bearing claim, write a row in the findings table with these columns:

| # | Claim (verbatim from charter) | Charter line | Claim type | Severity if wrong |
|---|-------------------------------|--------------|------------|-------------------|

Claim types:
- **HARD_GATE** — failure condition that Scout DISCOVER or Logician PRE will reject closed on
- **DISQUALIFIER** — failure condition that downgrades but does not reject
- **GEO_SCOPE** — applicant primary service area requirement
- **ELIG_ENTITY** — applicant entity-type requirement (501(c)(3), 509(a), gov, individual, for-profit)
- **MATCH_PERCENT** — matching-funds requirement
- **FUNDING_RANGE** — typical grant size, max award, length
- **PORTFOLIO_PATTERN** — recent giving pattern (geographic, demographic, sectoral)
- **PROGRAM_AREA** — strategic / thematic taxonomy
- **APPLICATION_PROCESS** — LOI vs full app, portal, timelines, response cadence
- **COMMON_REJECTION** — typical Scout / Logician rejection mode
- **LANGUAGE_FLAG** — register preferred_terms or suspicious_terms

### Step 2 — Cross-reference each claim against authoritative sources

Sources, in order of authority:

1. **Funder's own public website** (`/about-us`, `/grants`, `/strategic-areas`, `/eligibility`, `/apply`, equivalent)
2. **Operator-supplied authoritative documents** (Grantee Perception Reports, annual reports, strategic plans, white papers from the funder itself — these often exceed website precision)
3. **Recent grant awards** — last 2-3 years from the funder's "Grants Awarded" page or 990-PF Schedule I
4. **IRS Form 990 / 990-PF** (foundations) — Schedule I (grants paid), Part XV (grantmaking program description), Schedule O
5. **Federal NOFO / RFA / FOA documents** (federal programs) — current-fiscal-year and immediately prior
6. **Federal agency program pages** (e.g., USDA AMS, USDA RD, USDA NIFA, NSF, SBA, EPA, EDA) — eligibility tables, FAQ, recorded webinars
7. **Tertiary references** (Candid, ProPublica Nonprofit Explorer, GuideStar, Devex, Grantmakers.io) — used only when primary 1-6 are silent; tertiary is never authoritative against a primary contradiction

For each claim, write:

| # | Source consulted | Source authority tier (1-7) | Source text (verbatim ≤2 sentences) | Source URL / file path | Retrieved date |
|---|------------------|------------------------------|--------------------------------------|------------------------|----------------|

### Step 3 — Compare and classify

For each claim, compare the charter language against the source text. Classify the result:

- **MATCH** — charter language and source align materially
- **PARTIAL** — charter is correct but incomplete; source reveals additional material to add (typically P2)
- **STALE** — charter uses outdated taxonomy / framing that the funder has since refreshed (typically P1)
- **UNSUPPORTED** — charter makes an assertion the source does not back; needs a corpus citation or removal (typically P1)
- **CONTRADICTED** — charter language directly contradicts the source (typically P0)
- **NOT_APPLICABLE** — claim is operator-defined process logic (e.g., Logician PRE-gate naming convention), not a funder-fact claim

### Step 4 — Severity classification

- **P0 — hard-gate fidelity break.** The charter has a HARD_GATE, GEO_SCOPE, ELIG_ENTITY, or DISQUALIFIER claim that is CONTRADICTED by the authoritative source. This category will cause Scout DISCOVER or Logician PRE to reject closed on applicants who are in fact eligible — or admit applicants who are in fact ineligible. **P0 blocks operator sign-off until fixed.** The Heinz "Pittsburgh-metro / Allegheny-County HARD GATE" was P0.

- **P1 — unsupported assertion or stale framing.** UNSUPPORTED or STALE claim. Will not directly cause Scout to reject a valid applicant, but will degrade Scribe register fidelity, leak stale taxonomy into Heinz-facing drafts, or feed Logician gates that don't match current funder reality. **P1 should be fixed pre-sign; can ship with documented exception if Pillar-2 dispatch is queued to resolve.** The Heinz "rural" suspicious-term flag was P1.

- **P2 — material omission.** PARTIAL claim. The charter is correct as far as it goes but is missing material the source contains (typical examples: median grant size, application portal name, response timeline, DEI portfolio pattern). **P2 should be fixed pre-sign when source is in hand; can defer to Pillar-2 corpus when not.** The Heinz "no funding-range context" gap was P2.

Severity ties break upward: when uncertain between P1 and P0, treat as P0.

### Step 5 — Apply fixes

For each finding:

- Cite the source in the charter `source_backing.corpus_refs` (with URL + retrieval date + verbatim quote excerpt)
- Update the inline charter language
- If a Logician gate is being renamed (e.g., `F-HEINZ-NOT-PITTSBURGH-METRO` → `F-HEINZ-NOT-SWPA-OR-PA`), add a `note:` field on the gate explaining the rename + why the previous gate was a fidelity break
- Update the charter status header to note `[FIDELITY-FIX-<ARTIFACT>] applied <YYYY-MM-DD>`
- Demote any per-fact `[CONJECTURE — Pillar-2 corpus pending]` tags whose claims are now corpus-backed
- Preserve §7 signature block (placeholders only — do not touch field order or whitespace, the signing helper's canonicalization depends on it)

### Step 6 — Verify

- Re-run `sign_charter --dry-run` on the amended charter — confirm content_hash_sha3_512 computes successfully (canonicalization not broken)
- Run `tests/funder_intelligence/test_sign_charter.py` — confirm 14/14 still pass (signing logic not broken)
- Grep the amended charter for any remaining instance of the broken framing — confirm only intentional historical notes survive (e.g., in the renamed-gate `note:` field)
- Commit with `[FIDELITY-FIX-<ARTIFACT>]` prefix on the existing PR branch — do not open a new PR

---

## §4 — Output format

### Per-charter findings doc

Path: `pipeline/funder_intelligence/_audits/charter_fidelity_audit_<artifact_id_kebab>_<YYYY-MM-DD>.md`

Sections:

1. **Header** — artifact_id, branch, PR ref, audit date, auditor, charter file path, charter SHA before fix, charter SHA after fix
2. **Sources consulted** — table of authoritative-source URLs / file paths + retrieval dates + which claims they back
3. **Findings table** — every load-bearing claim, before-text, source text, classification, severity, fix-applied flag
4. **P0 details** — narrative explanation of each P0 finding (what was wrong, what the source said, what the fix is, downstream consumers affected)
5. **P1 details** — narrative for each P1 finding
6. **P2 details** — narrative for each P2 finding (briefer; aggregated by theme)
7. **Discrepancies surfaced** — anywhere the operator-supplied framing differed from the authoritative source (e.g., operator said "9 counties," primary source confirmed 10)
8. **Fix summary** — git diff summary, gate-rename list, source_backing.corpus_refs additions
9. **Verification** — sign_charter dry-run output, test suite pass count, post-fix grep results
10. **Sign-off readiness** — green / yellow / red, with explanation

### Aggregate roll-up

Path: `pipeline/funder_intelligence/_audits/charter_fidelity_audit_aggregate_<YYYY-MM-DD>.md`

Sections:

1. **Roster** — table of all 14 charters with status (audited / pending) and P0/P1/P2 counts per artifact
2. **P0 inventory** — cross-charter list of every P0 finding with current fix status
3. **P1 inventory** — same for P1
4. **P2 inventory** — same for P2
5. **Cross-charter patterns** — fidelity breaks that recur across multiple charters (e.g., stale program-area taxonomy across several foundation charters)
6. **Next-charter dispatch shape** — for the queued charters, recommended source-list per charter and estimated audit budget

---

## §5 — Worked example: Heinz (P0 GEO_SCOPE fidelity break)

See `pipeline/funder_intelligence/_audits/charter_fidelity_audit_heinz_2026-05-18.md` for the full Heinz audit. Headline findings:

- **P0 × 1** — `runtime_consumer.scout.decision_changed` + `runtime_consumer.logician.decision_changed` + `stage_behavior.screen.pass_fail_triggers` + `logician_gate_candidates.F-HEINZ-NOT-PITTSBURGH-METRO` + multiple prose mentions all framed scope as "Pittsburgh-metro / Allegheny-County HARD GATE." **CONTRADICTED** by `https://www.heinz.org/grants`: "We concentrate our efforts and resources in southwestern Pennsylvania (SWPA). Given our primarily regional focus, the foundation is generally unable to consider applications for funding outside the Commonwealth of Pennsylvania, unless the proposal is expressly for the benefit of residents of the SWPA region or state." Confirmed by Heinz's 2026 Workforce announcement on `https://www.heinz.org/`: "These Workforce grants span 10 counties." Fix: renamed gate to `F-HEINZ-NOT-SWPA-OR-PA`; rewrote scope to SWPA 10-county + PA-Commonwealth envelope; added `note:` documenting the rename.

- **P1 × 3** —
  - Legacy 4-area taxonomy ("Sustainability / Creativity / Learning / Community & Economic Development") — **STALE**; Heinz refreshed to 7 areas (Arts & Culture; Civic Participation; Climate, Environment & Health; Community & Economic Development; Food Systems; Veterans; Workforce) per `https://www.heinz.org/strategic-areas`. Fix: replaced taxonomy throughout; added `F-HEINZ-LEGACY-TAXONOMY-LEAK` LOW gate.
  - "rural" flagged as suspicious_term — **UNSUPPORTED**; SWPA includes 6 counties with rural / small-town communities Heinz actively funds (Beaver, Greene, Indiana, Fayette, Armstrong, Lawrence, Butler, Washington, Westmoreland). Fix: removed "rural" from suspicious_terms with inline comment documenting the removal.
  - `F-HEINZ-501C3-MISSING` Logician gate — **PARTIAL/UNSUPPORTED**; Heinz also funds 509(a) public charities + federally-tax-exempt government entities per the public grants page. Fix: renamed to `F-HEINZ-ELIGIBLE-ENTITY-MISSING`; added `F-HEINZ-INDIVIDUAL-OR-FORPROFIT` P0 gate.

- **P2 × 4** —
  - No funding-range context (median grant size, average length, annual volume) — **PARTIAL**; GPR 2024 + Heinz home page supply $100K median, 1.7yr avg length, ~$90M annual volume. Fix: added all to `mission_framing.one_paragraph_summary`.
  - No DEI portfolio pattern — **PARTIAL**; GPR 2024: >2/3 grantees serve at least one historically disadvantaged group, particularly Black communities. Fix: added to `stage_behavior.consensus.portfolio_considerations`.
  - No application-process detail (Blackbaud portal, 45-day LOI ack, 60-90 day decision) — **PARTIAL**; Heinz public grants page details these. Fix: added to `stage_behavior.screen.time_budget` + `pass_fail_triggers`.
  - No program staff load context (53 active grants + 50 apps per staffer) — **PARTIAL**; GPR 2024. Fix: added to red_team_probe_seeds (informs the cold-outreach probe weighting).

**Sign-off readiness:** green after fixes applied.

**Worked-example note — multi-commit amendments are normal.** The Heinz audit landed across TWO commits. Commit 1 corrected the geo-scope error + 7-area taxonomy + GPR-backed eligibility/funding/portfolio adds. Commit 2 (after operator + collaborator GPR re-parse) restructured the charter around three distinct GPR-derived `behavior_mechanisms` (regional_legitimacy_capital + transition_sensitive_relationship_clarity + capacity_partnership_beyond_grant), DEMOTED the universal-Pittsburgh-fail-close gate to a MED warning at the funder layer (because GPR respondent geography includes outside-PA respondents — a universal funder-layer geo P0 over-restricts against the corpus), DOWNGRADED the "outcomes-vs-outputs is most-common downgrade" claim to general foundation-officer heuristic (not Heinz-specific), and REPLACED "innovative is suspicious" with "unsupported_innovation is suspicious" (because GPR p.2 explicitly praises Heinz's backed-innovation portfolio). Auditors of subsequent charters should expect that a deep GPR / annual-report / strategic-plan re-parse may surface additional commits beyond the initial fidelity fix — this is normal, and the per-charter findings doc should be updated with commit-history sections that document each amendment in turn.

---

## §6 — Cloning this audit for the other 13 charters

Each charter gets its own findings doc following the §4 per-charter format. **Do not aggregate findings across multiple charters into a single doc**; the per-charter file is what operator signs the fix-amendment commit against.

For each of the remaining 13 charters, source list is artifact-dependent:

| Artifact family | Primary sources to consult |
|-----------------|-----------------------------|
| Federal funder (USDA-RD, USDA-NIFA, USDA-AMS) | Agency program page; recent NOFOs (FY25 + FY26); agency strategic plan |
| State funder (PA-DEPT-AG, PA-DCED) | Agency website; current fiscal-year funding announcements; state budget appropriations |
| Foundation funder (RICHARD-KING-MELLON-FOUNDATION) | Funder website; recent IRS Form 990-PF; published grant guidelines; Candid profile (tertiary) |
| Cooperative-development funder (NCBA-CLUSA) | NCBA-CLUSA website; current CCD-EDP and CCDP RFAs from USDA Rural Business; recent award announcements |
| Federal program (USDA-AMS-VAPG-FY26, USDA-RD-RBDG-FY26, USDA-RD-RCDG-FY26, USDA-NIFA-SARE-NE-FY26, USDA-RD-CFP-FY26) | Current-FY NOFO / RFA; immediately prior FY NOFO; agency program page; recorded applicant webinars; awarded-grant rosters |
| State program (PA-DEPT-AG-AGINNOV-FY26) | Current-FY guidelines; PDA Ag Innovation Grant program page; prior-cycle award announcements |

**Audit budget per charter:** ~45-75 minutes for federal-program charters (NOFO PDFs are dense); ~30-45 min for federal-funder charters (program-page scrape + 1-2 prior NOFOs); ~30 min for foundation / state / cooperative charters. The Heinz audit took ~60 min because the GPR memo is dense and the geo-scope fix touched many sites in the charter — most charters won't have a P0 of equivalent breadth.

**Recommended next dispatch shape:** parallel dispatch of all 13 audits (no shared dependencies; each charter is independent). Each gets its own `[FIDELITY-FIX-<ARTIFACT>]` commit to the same PR #33 branch. Aggregate roll-up authored once all 13 land. Re-run signature-roundtrip CI after each commit. Re-run aggregate after all commits to surface cross-charter patterns (especially: do any of the other foundation charters carry the same legacy-taxonomy leak Heinz did?).

---

## §7 — What this audit does NOT replace

- **Codex same-prompt-with/without quality test** — separate audit at the Codex external-validity layer
- **Pillar-2 corpus assembly** — this audit only fixes what publicly verifiable sources can prove; deeper claims (per-strategy priority weighting, program-officer relationship cadence, fiscal-sponsorship acceptance norms) wait for Pillar-2
- **L-005 Pillar-3 extraction audit** — separate downstream
- **Operator review of the fix itself** — the auditor proposes; operator signs

---

## §8 — Versioning

- **v1.0 (2026-05-18)** — initial methodology after Heinz P0 catch
- Future revisions when audit catches a class of break this template missed

