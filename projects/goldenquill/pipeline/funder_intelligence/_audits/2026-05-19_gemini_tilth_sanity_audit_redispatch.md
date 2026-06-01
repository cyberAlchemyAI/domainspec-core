---
title: Gemini sanity audit — Tilth-only redispatch
date: 2026-05-19
authored_by: Cowork session (Anthropic-family author); Synthesizer mode
predecessor: local_13c5a799 (analysis complete; 6 reports wiped by Pass-3-Scribe commit race 2026-05-18)
scope: TILTH-ONLY. MyCel / Loom Console / Loom Workstream content excluded (separate workstream).
in_scope_sources:
  - pipeline/funder_intelligence/_inbound_unverified/gemini_funding_sources.pdf (md5 ca4cbc0b2a78c756ce7a48b9a5ab3a9a; 1 page; truncated text-only snippet)
  - pipeline/funder_intelligence/_inbound_unverified/SN_LLC_Supplementary_Funding_Research_Net_New_Funders_May_2026.pdf (md5 d164836a6e17c7032314ffaab6d248ce; 23 pages)
  - pipeline/funder_intelligence/_inbound_unverified/FID_agent_report.md (209 lines)
  - research/funder_intelligence_seed/tilth_golden_quill_master_funding_command_workbook.xlsx (12 sheets; 02 Opportunity Universe = 46 rows; 07 Integrated Funder Metadata = 123 unique funders)
  - pipeline/funder_intelligence/_master_workbook/_predecessors/tilth_golden_quill_funding_opportunity_universe_2026.xlsx (6 sheets; predecessor of master)
  - pipeline/funder_intelligence/_master_workbook/_predecessors/funder_metadata_and_search_seeds.xlsx (7 sheets; predecessor of master 07/08)
out_of_scope_sources:
  - research/mycel/* (Loom workstream — separate audit)
  - research/gemini-code-1779059804703.html (Loom-content-heavy; scanned only for Tilth-naming drift; none found; 4 Tilth mentions all in passing context)
canonical_reference: /Users/goldenquill/Downloads/GoldenQuill/CLAUDE.md
---

# §1 — Verdict table

Verdict legend:
- `verified` — matches canonical Tilth (CLAUDE.md)
- `drifted` — related Tilth concept, wrong naming/scope
- `hallucinated` — fabricated Tilth system names/sections/gates
- `scope_creep` — real Tilth concept, framing exceeds locked scope
- `useful_external` — Gemini-discovered insight worth investigating, not yet in Tilth

## 1.1 Supplementary PDF (SN_LLC May 2026)

| # | Claim | Verdict | Notes |
|---|-------|---------|-------|
| S-01 | "Sovereign Node LLC" is the operating legal entity | drifted | Canonical is FIT Farms LLC. SN-LLC was provisional/stale entity language; CLAUDE.md explicitly disambiguates. HIGH severity — appears 18+ times in submission-grade routing recommendations. |
| S-02 | Tilth Scout/Scribe/Judge/Logician/**Auditor** architecture (p1, p8) | drifted | Canonical six seats are Scout, Scribe, Editor, Judge, Red Team, Logician. "Auditor" is not a Tilth seat. Likely a Gemini confusion of Red Team + Judge. HIGH severity — would be miswritten into AFWERX / DIU / Coefficient Giving applications. |
| S-03 | Tilth maps to DIU MYSTIC DEPOT AI-eval harness | useful_external | DIU CSO is a legitimate funder lane; Tilth's Judge + Red Team adversarial-eval architecture is plausibly responsive. Surface to operator. |
| S-04 | DoD/IC AFWERX SBIR/STTR Open Topic as Tier A | useful_external | Federal SBIR is in-scope. AFWERX Open Topic LLC-eligibility makes this a clean route via FIT Farms LLC (not "Sovereign Node LLC"). Re-route in any downstream draft. |
| S-05 | DoW "Pace-Setting Projects" Jan 2026 (p1, p3) | hallucinated (suspect) | Operator-flagged P0 verification item — could be Gemini fabrication or genuine DoW/DoD posture. No Tilth-side artifact references this program. Primary-source URL not provided in PDF. |
| S-06 | NLnet NGI Zero Commons Fund June 1, 2026 12:00 CEST | useful_external | Legitimate EU funder; appears in workbook row 1 (master) as Tier A. Out-of-scope as Tilth route (MyCel-framed in PDF) — but the deadline is verified. |
| S-07 | Coefficient Giving (formerly Open Philanthropy) Technical AI Safety RFP rolling | useful_external | Workbook row 3 (master). Substantial Tilth-relevance for cross-family Judge / Red Team adversarial architecture once Auditor drift is corrected. |
| S-08 | Mozilla Technology Fund DORMANT 2026 → Mozilla Foundation Incubator "Democracy x AI" cohort locked | verified (status change) | Material status change; workbook row 14 should flip Tier B → Watch-only. |
| S-09 | OTF v. Lake et al. preliminary injunction Nov 11, 2025; FOSS Sustainability Fund call open through May 7, 2026 | useful_external | OTF politico-litigation context affects Tilth's open-source-funder pipeline. Primary-source verification needed (case citation 2025 WL 3289166 — verifiable). |
| S-10 | Creative Capital 2027 Round I closed April 2, 2026 | verified (status change) | Out-of-scope for Tilth (Loom Console framing in PDF) — but workbook may carry; flag if it does. Workbook does not currently list Creative Capital → no action. |
| S-11 | Sovereign Tech Fellowship 2026 closed April 6, 2026; STF grant program remains open rolling | verified (status change) | Workbook row 24 (Tier B) — status flip required. |
| S-12 | ISOC Foundation Research Grant April 7–May 22, 2026 21:00 UTC | useful_external | Workbook row 25 (Tier B) — deadline confirmation. |
| S-13 | IMLS NLG-Libraries FY27 Nov 13, 2026 deadline | useful_external | Customer-pass-through route via Carnegie Library of Pittsburgh. Tilth-as-vendor pattern — Section §1F-style routing matches Tilth architecture. |
| S-14 | Forbes Funds MAGs + AI for Social Impact track with maad labs | useful_external | Pittsburgh-region pass-through; HIGH-fit Tilth-as-vendor route per Section 9 Customer Pass-Through sheet. |
| S-15 | USDA CFPCGP via Mystic Mamas / Keystone fiscal sponsorship | useful_external | Mystic Mamas is a Josh-known client per CLAUDE.md `orgs/` index. Route is plausible. Operator should validate Keystone Development Center fiscal-sponsor relationship before action. |
| S-16 | NSF I-Corps Mid-Atlantic Hub (Penn State regional partner, NOT CMU) | useful_external | Corrects a workbook assumption that may have implied CMU is the regional partner. $50K National Teams pathway after regional graduation. |
| S-17 | Andy Warhol Foundation small-organizations track launched Feb 2026; next deadline Sept 1, 2026 | useful_external | 501(c)(3)-only — Tilth route is customer-pass-through via Pittsburgh art-space partner. Workbook does not currently list AWF; surface as candidate. |
| S-18 | Craig H. Neilsen Foundation CO&I — out-of-scope (Loom Console accessibility framing) | out_of_scope | Loom workstream. |
| S-19 | Hackaday Prize $50K Grand Prize — out-of-scope (Loom Console) | out_of_scope | Loom workstream. |
| S-20 | American Craft Council / CERF+ / Center for Craft — out-of-scope (Loom craft framing) | out_of_scope | Loom workstream. |
| S-21 | Wellcome Leap FORM/VISIBLE/Focused Antibiotics — MyCel-reframe required | out_of_scope | Loom/MyCel workstream. |
| S-22 | John Templeton Foundation Intelligence Venture 2026 OFI Aug 14, 2026 | useful_external | Plausible Tilth-philosophy fit ("Consensus Zones" Gemini-language is hallucinated phrasing — Tilth has no "Consensus Zones" primitive; the philosophical-pluralism angle is real but framing needs Tilth-native vocab). |
| S-23 | NVIDIA Inception (free credits, not grant) | useful_external | Infrastructure subsidy, not grant. Surface for operator infrastructure pipeline. |
| S-24 | Pew Center for Arts & Heritage — Pittsburgh INELIGIBLE (5-county Philly only) | verified (status correction) | Workbook should flag if Pew is listed; spot-check — Pew not in workbook so no action. |
| S-25 | NGI TALER, Fediversity, Wellcome Leap framings | out_of_scope | MyCel workstream. |

## 1.2 Gemini funding sources PDF

| # | Claim | Verdict | Notes |
|---|-------|---------|-------|
| G-01 | "Decentralized Agentic Infrastructure, Open-Source Commons, and Localized Sovereign Ecosystems" framing | scope_creep | Tilth's positioning is "regenerative grant intelligence" per CLAUDE.md brand line, not "decentralized agentic infrastructure for the AI ecosystem." Useful as funder-dialect hook for tech-focused funders, but not Tilth's primary frame. |
| G-02 | Text truncated mid-paragraph at "structural lack of administrative infrastructure, severe context decay, and the !Report unsafecontent" | hallucinated (extraction error) | The "!Report unsafecontent" trailing string is a Gemini export artifact, not content. PDF is a 1-page Gemini Deep Research snippet, not the full report — operator should obtain the full report or replace this source. |

## 1.3 FID_agent_report.md

| # | Claim | Verdict | Notes |
|---|-------|---------|-------|
| F-01 | "FID Sheet" terminology (4 occurrences) | drifted | Canonical is "FID charter" per task spec + FID research project doc. HIGH severity — appears in title, intro, and section headers. Rename throughout before any operational use. |
| F-02 | 5-seat agent architecture: Scout / Scribe / Judge / Red Team / Logician | drifted (under-specified) | Canonical Tilth six seats include **Editor** (clarity / jargon-stripping / GOO-sort). Editor missing from this report. Adding Editor brings architecture in alignment. |
| F-03 | "Specialised agents across sections, not per-sheet" architecture proposal | verified (aligned) | Matches Tilth's section-specialist seats-do-cross-program-learning model. |
| F-04 | USDA-RD / RBDG / CFP / RCDG / NIFA / SARE / AMS / PA Dept of Ag / Heinz / RKM / NCBA CLUSA charter content | verified (substantive) | Twelve funder/program charters with eligibility, deadlines, evaluation criteria, and per-seat implications. **This is the highest-value Tilth-relevant artifact in the bundle.** Strong FID exemplar-pair seed material per `funder_intelligence_database_research_project_2026-05-16.md` §1.1. |
| F-05 | USDA-RD RBDG FY26 deadlines: SECD June 15, 2026 / RBDG June 30, 2026 | useful_external | Workbook does not currently carry RBDG. Should be added; deadline verifiable via Grants.gov primary source per Law 1. |
| F-06 | PA Ag Innovation Grant FY25–26 round closed April 18, 2026 | verified (status change) | Cross-confirmed against CLAUDE.md ("Do not propose PA Ag Innovation Grant as a dogfood target — off the table") — Gemini reading is consistent with operator's posture. |
| F-07 | RCDG only nonprofit institutions eligible | verified | Correct citation 7 CFR 4284.520(a). |
| F-08 | "Cooperative Authenticity Layer" reusable overlay for cooperative programs | verified (aligned with CIC-05 Cooperative) | Maps cleanly to canonical CIC-05 Cooperative card primitives. |

## 1.4 Master workbook + predecessors

| # | Claim | Verdict | Notes |
|---|-------|---------|-------|
| W-01 | 46 opportunities in Opportunity Universe sheet, 21 in Priority Pipeline | verified | Counts confirmed via openpyxl extraction. |
| W-02 | 123 unique funders in Integrated Funder Metadata sheet | verified | Counts confirmed. |
| W-03 | 21 of 46 Opportunity Universe entries are also in Priority Pipeline | verified | Subset relationship intentional. |
| W-04 | Workbook headers: Tier, Opportunity/Program, Funder, Funder Type, Opportunity Type, Amount/Support, Status/Deadline, Applicant Route, Geography, Best-Fit Components, Proposed Project Angle, Eligibility/Fit Notes, Constraints/Risks, Immediate Next Step, Source URL, Source Basis, Fit Score, Owner, Track, Due Priority, Route Class, Fundable Package, Western PA Value, Route Discipline, Action Bucket, Submission Stance | verified | 26-column schema; comprehensive. |
| W-05 | "FIT Farms LLC is the current operating/legal owner unless changed. Keep MyCel and Loom as separately fundable R&D layers" (predecessor opp_universe Overview!B3) | verified (aligned) | Matches CLAUDE.md disambiguation of FIT Farms LLC = current operating legal entity. **The master workbook explicitly does NOT carry the "Sovereign Node LLC" drift — only the supplementary PDF does.** |
| W-06 | "Best-Fit Components" lists MyCel + Loom Console + Brain/open memory alongside Tilth | out_of_scope (mixed) | Workbook bundles Tilth + MyCel + Loom into a single funder universe. For this audit (Tilth-only), MyCel + Loom rows are out of scope. Operator may want a Tilth-only re-slice. |
| W-07 | Tier A: NGI Zero Commons, NSF PESOSE, Coefficient Giving, NSF SBIR/STTR Phase I, Astera Residency, AI Grant, a16z Open Source, LTFF, SFF, GitHub Secure OSS, GitHub Accelerator, Cosmos Grants, Cosmos Fellowship | useful_external | 13 Tier A entries. Most are not yet in canonical Tilth FID lattice (see §3 candidate funder list). |
| W-08 | No "Sovereign Node LLC" string in any workbook cell | verified (clean) | All 3 workbook files searched; zero hits. Drift is isolated to the supplementary PDF. |
| W-09 | No "Auditor" string in any workbook cell | verified (clean) | Drift isolated to supplementary PDF. |
| W-10 | No "FID Sheet" string in any workbook cell | verified (clean) | Drift isolated to FID_agent_report.md. |

## 1.5 Tally (Tilth-only)

| Verdict | Count |
|---------|-------|
| verified | 16 (incl. 4 status-change confirmations) |
| drifted | 5 |
| hallucinated | 2 (1 extraction artifact + 1 suspect DoW program) |
| scope_creep | 1 |
| useful_external | 16 |
| out_of_scope (Loom/MyCel) | 5 |

# §2 — Naming-drift sweep (HIGH severity — submission risk)

Specific instances with file + page/sheet/cell:

| Drift | Should be | Occurrences | Severity |
|-------|-----------|-------------|----------|
| "Sovereign Node LLC" | "FIT Farms LLC" | `SN_LLC_Supplementary_Funding_Research_Net_New_Funders_May_2026.pdf` pages 1, 3, 4, 5, 8, 13, 15, 17, 18, 20 (18+ instances; routing recommendations across multiple federal lanes) | HIGH — submission risk |
| "Auditor" (as a Tilth seat) | "Red Team" or "Judge" (depending on context); canonical six seats are Scout / Scribe / Editor / Judge / Red Team / Logician | `SN_LLC_Supplementary_Funding_Research_Net_New_Funders_May_2026.pdf` p1 ("Scout/Scribe/Judge/Logician/Auditor"); p8 ("Auditor/Judge consensus model") | HIGH — submission risk |
| "FID Sheet" / "FID sheet" | "FID charter" | `FID_agent_report.md` line 1 (title), line 4 (intro), line 187 (architecture section), line 209 (conclusion) | MEDIUM — internal naming drift, not submission-facing |
| Missing Editor seat in 5-seat architecture | Add Editor to Scout/Scribe/**Editor**/Judge/Red Team/Logician | `FID_agent_report.md` lines 187, 192–198, 209 (4 occurrences of 5-seat list) | LOW — under-specification, easy to correct |
| "Consensus Zones" architecture phrasing | No canonical Tilth primitive by this name; closest is the Judge-vs-Red-Team cross-family adversarial pattern + "council split" mechanism | `SN_LLC_Supplementary_Funding_Research_Net_New_Funders_May_2026.pdf` p5 (John Templeton framing) | LOW — Gemini-invented phrasing, not yet in Tilth |
| "Decentralized Agentic Infrastructure" positioning | "Regenerative grant intelligence" (CLAUDE.md brand line) | `gemini_funding_sources.pdf` p1 | LOW — positioning drift, not naming drift |

**Operational implication:** Any downstream proposal-drafting that reads from the supplementary PDF as a source must apply the global substitution **before** any text reaches a funder portal. Recommend Logician PRE-gate `F-NAMING-SN-LLC-LEAK` + `F-NAMING-AUDITOR-LEAK` for any draft that ingests this PDF as a source. This audit doc + the rename pass cover the immediate risk.

# §3 — Net-new funder candidates

See appended section in `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` under heading `## Candidate Funders Awaiting Verification — Added 2026-05-19 (from operator-supplied seeds)`. Counts:

- 117 net-new candidate entries appended (Workbook Tier 2 = 89 unique funder-program rows from `02 Opportunity Universe` + `07 Integrated Funder Metadata` not already canonical; Gemini PDF Tier 3 = 28 net-new Tilth-relevant entries not already in workbook).
- Source authority applied per task spec:
  - Workbook entries → TIER 2 (operator-derived, pending primary-source verification).
  - Gemini PDF entries → TIER 3 (conjecture, pending primary-source verification).
  - Primary URL verification (Scout VERIFY pass) promotes individual rows to TIER 1.
- All Loom/MyCel-only candidates excluded from the appended list.

# §4 — Five P0 operator decisions

For Josh to decide before downstream FID exemplar-pair Phase 1 kickoff:

1. **Pursue AI-safety funder cluster?** (Coefficient Giving, Manifund AISTOF, LTFF, SFF, Astera, Cosmos, AI Grant, a16z OSS Grant, Schmidt Sciences AI2050). 13 Tier A entries cluster around AI-safety / agent-infrastructure / open-source-AI thesis. Tilth's Scout / Scribe / Editor / Judge / Red Team / Logician architecture is plausibly responsive but the framing is a sector-shift from regenerative-grant-intelligence to AI-safety-infrastructure. Yes/no/conditional.

2. **Pursue DoD AI-eval cluster?** (AFWERX SBIR Open Topic Phase I, DIU CSO MYSTIC DEPOT follow-ons, SOFWERX, xTechSearch, DARPA YFA / I2O BAA, IES SBIR June 29 2026). Tilth's Judge + Red Team cross-family adversarial-eval architecture maps to "automated red-teaming" + "human-AI team assessment" DIU language. LLC-eligible via FIT Farms LLC route. Higher administrative load (Customer Memorandum from USAF program office for AFWERX). Yes/no/conditional.

3. **Expand FID `_schema/` to include `capital_raise` (Reg CF)?** Republic / SeedInvest / StartEngine / Wefunder Reg CF surface in the Gemini PDF as "non-grant non-dilutive-ish capital." Currently FID schema covers funders/programs/compliance-cascades/reviewer-heuristics — not capital-raise instruments. Question: is Reg CF in scope for Tilth's grant-intelligence stack (or out-of-scope as a different capital-stack layer)?

4. **Verify "DoW Pace-Setting Projects"** (Gemini PDF p1, p3). Suspected hallucination or genuine-but-undocumented program. No primary-source URL in PDF. Scout VERIFY required. Yes-verify / no-skip / conditional-on-finding-source.

5. **Engineering plan substrate decision deferred to LOOM workstream (NOT a Tilth decision).** Per task spec, Loom substrate decisions are out of scope for this audit. Flagged here only to confirm closure — no Tilth action required.

# §5 — Cross-references

- `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` — net-new candidates appended.
- `pipeline/funder_intelligence/_audits/2026-05-19_workbook_dedup_and_conflicts.md` — workbook dedup detail.
- `pipeline/funder_intelligence/_audits/2026-05-19_gemini_vs_tilth_gap_analysis.md` — gap-analysis detail.
- `/Users/goldenquill/Downloads/GoldenQuill/CLAUDE.md` — canonical Tilth state (ground truth).
- `pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md` — three-posture routing (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign).
- `/SOUL.md` — Five Operating Laws (Law 1: RFA is truth — applied to "verify before adopt" discipline on every Gemini candidate).

# §6 — Predecessor dispatch notes

Prior dispatch `local_13c5a799` completed analysis (per task spec) but the 6 emitted reports were wiped by a parallel Pass-3-Scribe commit race on 2026-05-18. This redispatch:
- Corrects scope to TILTH-ONLY (prior dispatch comingled Tilth + Loom material).
- Produces three audit outputs + one FID-research-doc append (vs prior dispatch's 6 reports).
- Cuts branch `gemini-sanity-audit-tilth-only-redispatch-2026-05-19` to isolate from the parallel commit cascade.
