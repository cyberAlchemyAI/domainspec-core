---
title: Gemini vs canonical Tilth — gap analysis (Tilth-only)
date: 2026-05-19
authored_by: Cowork session
canonical_reference: /Users/goldenquill/Downloads/GoldenQuill/CLAUDE.md
scope: TILTH-ONLY. MyCel + Loom + Loom Console excluded.
---

# §1 — Drifts from canonical (Gemini-side vs Tilth-canonical)

| # | Gemini-claimed Tilth state (in-scope sources) | Canonical Tilth state (CLAUDE.md) | Severity |
|---|------------------------------------------------|------------------------------------|----------|
| D-01 | Tilth's operating legal entity is **"Sovereign Node LLC"** | **FIT Farms LLC** is the current operating legal entity. "Sovereign Node LLC" is stale/provisional entity language from older docs. "Sovereign Node" (no LLC) refers to the Stage-5 commons layer — not a currently active legal entity. (CLAUDE.md "The Product Naming Chain" + "FIT Farms Commons · FIT Farms LLC" sections) | **HIGH — submission risk** |
| D-02 | Tilth's seat roster includes **"Auditor"** alongside Scout / Scribe / Judge / Logician | Canonical six seats: **Scout / Scribe / Editor / Judge / Red Team / Logician** (CLAUDE.md "The Council (Six Seats)"). "Auditor" is not a Tilth seat. The cross-family adversarial role is **Red Team** (per `/router.yaml` and v7.0.6 SELF-LOCK 2026-05-09). | **HIGH — submission risk** |
| D-03 | "FID Sheet" terminology (FID_agent_report.md) | Canonical is **"FID charter"** per `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md`. FID = Funder Intelligence Database; per-funder/per-program/per-cascade/per-reviewer-type artifacts are charters, not sheets. | MEDIUM — internal naming drift |
| D-04 | 5-seat agent architecture (FID_agent_report.md) | 6-seat architecture — **Editor** missing from Gemini's account. Editor's clarity/jargon-stripping/GOO-sort role is critical to Tilth's pipeline and absent from Gemini's specialist-agent design. | MEDIUM — under-specification |
| D-05 | "Consensus Zones" architecture phrasing (supplementary PDF p5, John Templeton framing) | No canonical "Consensus Zones" primitive in Tilth. Closest legitimate primitive: the cross-family Judge ↔ Red Team adversarial pattern with 10-point disagreement → council-split → human-decides mechanism (CLAUDE.md). | LOW — Gemini-invented phrasing |
| D-06 | "Decentralized Agentic Infrastructure" positioning (Gemini PDF p1) | Tilth's brand line is "regenerative grant intelligence" (CLAUDE.md "Brand line"). The decentralized-AI framing is a viable funder-dialect for AI-safety/AI-infrastructure funders, but it is **not Tilth's primary positioning**; using it as the lead frame would scope-creep Tilth out of its food-systems / educator / public-agency / arts / cooperative / ecosystem-intermediary base. | LOW — positioning drift |
| D-07 | Gemini PDF treats MyCel and Loom Console as inseparable from Tilth | Per task spec + CLAUDE.md, **Tilth and Loom are separate workstreams**. MyCel/Loom funding routing decisions are NOT a Tilth decision. Audit re-scopes accordingly. | (out of scope by spec — flagging for completeness) |
| D-08 | "DoW Pace-Setting Projects" (supplementary PDF p1, p3) referenced as January 2026 program | No Tilth-side artifact references this program. Could be genuine but undocumented, or hallucination. **Verification required.** | MEDIUM — depends on verification outcome |

# §2 — Useful_external items worth investigating

Items the Gemini research surfaced that are NOT yet in Tilth's FID lattice and ARE worth surfacing into Phase 1 candidate pipeline:

## 2.1 Highest-leverage (P0)

| # | Funder/program | Lane | Why worth investigating |
|---|----------------|------|--------------------------|
| U-01 | **117 net-new candidate funders** appended to FID research doc | All Tilth-relevant lanes (federal, state, foundation, customer-pass-through, cooperative-native capital) | Largest single value from this audit. See `funder_intelligence_database_research_project_2026-05-16.md` § "Candidate Funders Awaiting Verification — Added 2026-05-19". |
| U-02 | **Coefficient Giving Technical AI Safety RFP** (rolling, 300-word EOI gate) | AI-safety / agent-infrastructure | Workbook Tier A. ~$1B 2026 AI-grantmaking pool; bottlenecked on grantmaker capacity, not capital. Tilth's Judge ↔ Red Team cross-family adversarial design is plausibly responsive — operator P0 #1 decision. |
| U-03 | **DIU Commercial Solutions Opening MYSTIC DEPOT follow-ons** | DoD AI-eval | Tilth's adversarial-eval architecture maps to DIU's "automated red-teaming" + "human-AI team assessment" language. LLC-eligible via FIT Farms LLC — operator P0 #2 decision. |
| U-04 | **NSF I-Corps Mid-Atlantic Hub** (Penn State regional, NOT CMU) | Workforce / commercialization | Pittsburgh route: $50K National Teams unlocked after regional cohort. May/June 2026 cohort accepting applications. |
| U-05 | **IMLS NLG-Libraries FY27** Nov 13, 2026 | Customer-pass-through via Carnegie Library of Pittsburgh | AI literacy is now an explicit IMLS priority. Tilth-as-vendor pattern via library applicant. |
| U-06 | **Forbes Funds MAGs + AI for Social Impact w/ maad labs** | Pittsburgh capacity-building | Cleanest Tilth-as-vendor route in Pittsburgh; rolling deadline. |

## 2.2 Medium-leverage

- AFWERX SBIR Open Topic Phase I (LLC-eligible; Customer Memorandum from USAF needed) — operator P0 #2
- Sloan Foundation Digital Tech / Better Software for Science / OSPO (Josh Greenberg as historical OSPO PO)
- Sovereign Tech Fund (grant program, foundational-infrastructure framing) — distinct from closed Fellowship
- John Templeton Foundation Intelligence Venture 2026 OFI August 14, 2026 ($60M+, academic PI required)
- Andy Warhol Foundation Visual Arts small-organizations track (Feb 2026 launch; Sept 1, 2026 next deadline)
- IES SBIR June 29, 2026 (education-application Tilth framing)

## 2.3 Status changes the workbook should absorb

- **Mozilla Technology Fund DORMANT 2026** → flip workbook row 14 Tier B → Watch-only.
- **Sovereign Tech Fellowship 2026 CLOSED April 6, 2026** → flip workbook row 24 status.
- **OTF v. Lake et al. preliminary injunction Nov 11, 2025** → annotate workbook row 22/23 with litigation context; FOSS Sustainability Fund call open through May 7, 2026 (likely closed by audit date).
- **Creative Capital 2027 Round I CLOSED April 2, 2026** → not currently in workbook, no action.
- **Pew Center for Arts & Heritage Pittsburgh INELIGIBLE** → not currently in workbook, no action.

# §3 — Canonical Tilth items Gemini missed

Items in canonical Tilth state (CLAUDE.md, architecture v7.0.10, FID research doc, Five Laws, Four Autonomy Rules) that the Gemini research either omits, misrepresents, or skips:

| # | Canonical item | Gemini's treatment |
|---|----------------|---------------------|
| M-01 | **Six Customer Identity Categories** (CIC-01 Food Systems / CIC-02 Educator / CIC-03 Public Agency / CIC-04 Arts & Culture / CIC-05 Cooperative / CIC-06 Ecosystem Intermediary) | Gemini does not engage CIC taxonomy. Funder-routing recommendations don't reference the customer worlds Tilth serves. |
| M-02 | **Eight Capital Logic Cards** (Public Purpose & Works / Catalytic Change / Operating Capacity / Research & Evidence / Market Access / Credit & Underwriting / Sponsorship & Corporate Support / Shared Assets) | Gemini does not engage CLC taxonomy. Opportunity-driven CLC matching (not archetype-driven) is canonical per architecture v7.0.8 amendment; Gemini implicitly treats funder routing as flat. |
| M-03 | **Three-posture deployment routing** (Frontier-Eligible / Split-Context Hybrid / Local-Only-Sovereign) per architecture v7.0.10 LOCKED 2026-05-11 | Not engaged. Gemini PDF assumes standard cloud-LLM routing without classification-register awareness. |
| M-04 | **Classification Review white-glove step** (Ed25519-signed register; per-field public/shareable/confidential/operator_flagged tiers) | Not engaged. |
| M-05 | **Five Operating Laws** (RFA-is-truth / No-boundary-drift / Org-isolation / Apolitical-with-admin-risk-scan / Applicant-brings-substance) | Not engaged. Gemini's "Tier A/B/C/D" classifications are strategic-fit assessments, not Law-1-disciplined verified-fit assignments. The PDF's own caveat acknowledges this: "Tier A/B/C/D classifications are strategic-fit assessments, not approval-probability forecasts." |
| M-06 | **Four Autonomy Rules** (Save-state-always / Test-your-own-work / Be-explicit / Clean-output) | Not engaged. |
| M-07 | **`router.yaml` model bindings** (Editor: Groq Llama-3.3-70b; Judge: Google Gemini 2.5 Pro; Red Team: Groq GPT-OSS-120b) | Not engaged. Gemini's "consensus model" framing is provider-agnostic — but Tilth's cross-family discipline (reviewer model family ≠ author model family) is structurally important. |
| M-08 | **Logician F-CLASS-* / F-FID-* / F-WPFA-* / F-PACKET-* / F-REFLECTION-* / F-ARCHIVIST-* failure-code families** | Not engaged. |
| M-09 | **`orgs/` client isolation** (Law 3; one PROJECT_CONTEXT.md per session; MycoSymbiotics Coop vs MycoSymbiotics Inc are separate entities) | Gemini's "Mystic Mamas via Keystone fiscal sponsorship" route is plausible but Tilth would require formal `orgs/` enrollment + PROJECT_CONTEXT.md before any drafting. |
| M-10 | **VAPG FY26 rubric already extracted at `pipeline/rubrics/vapg_fy26.json` (100 pts, 7 criteria)** | FID_agent_report covers USDA-AMS funder profile but does NOT engage the existing VAPG rubric extraction. The 12 charter sections in FID_agent_report would benefit from cross-linking to existing rubric data. |
| M-11 | **`pipeline/institutional_memory/lessons.json` + lessons.md** with L-001 (EPA NEETP-26 list-vs-synopsis distinction), L-002 (path references not content dumps), L-005 (two-audit cycle) | Not engaged. Gemini PDF's verification stance ("verify every federal deadline at source URL before submission") aligns with L-001 spirit but doesn't reference the lesson. |
| M-12 | **Six support agents** (Intake / Uploader v0.1; Data Collector / Report Generator v0.2; Archivist v1.x) | Not engaged. |
| M-13 | **WPFA cycle-close accounting** (`CycleReceipt` artifact + Coefficient Registry signed-asset pattern; §17 v1 LOCKED 2026-05-11) | Not engaged. |
| M-14 | **Reflection Packet v0.1 Beta hook** (§16 v1 LOCKED 2026-05-15) | Not engaged. |
| M-15 | **Hardware tier — Golden Quill 128 GB canonical floor (M3 Ultra Mac Studio / AMD GX-10 / NVIDIA DGX Spark)** | Not engaged. |
| M-16 | **NCBA CLUSA cooperative-authenticity layer** | **FID_agent_report COVERS this correctly** — alignment with canonical CIC-05 Cooperative. Not a gap; flagging as positive alignment. |
| M-17 | **Three-sector scope (food/ag, land/remediation, arts) per SOUL.md** | Not engaged. Gemini PDF's funder universe extends well beyond the three sectors — useful breadth for funder-universe seeding but architectural decisions about scope expansion live with operator. |

# §4 — Top 3 gap-analysis findings

1. **The "Sovereign Node LLC" + "Auditor" drift in the supplementary PDF is a submission-grade risk.** 18+ instances of SN-LLC across routing recommendations for AFWERX, DIU, NLnet, Coefficient Giving, Mystic Mamas-pass-through, Andy Warhol, Craig Neilsen. 2 instances of "Auditor" in the Tilth seat description. Any downstream proposal-drafting that ingests this PDF as a source MUST apply the global substitution **before** any text reaches a funder portal. Recommend Logician PRE-gate (`F-NAMING-SN-LLC-LEAK` + `F-NAMING-AUDITOR-LEAK`).

2. **Gemini provides excellent funder-universe breadth and missing-deadline catches, but zero engagement with Tilth's architectural primitives.** CIC × CLC routing, three-posture deployment, F-CLASS-* gates, Five Laws, Four Autonomy Rules — all absent. The supplementary PDF is best treated as **a raw funder-universe seed**, NOT as a strategic architecture document. The FID_agent_report.md, by contrast, IS architecturally engaged at the seat level (5/6 seats correctly identified, role-specific implications-per-funder correctly stated) and is the highest-value Tilth-relevant Gemini artifact in the bundle.

3. **The master workbook is internally clean and naming-drift-free.** The drift problem is isolated to the supplementary PDF — every cell across all 12+6+7 sheets of the three xlsx files searched 0 hits for "Sovereign Node LLC", "Auditor", and "FID Sheet". The predecessor workbooks even explicitly anchor "FIT Farms LLC is the current operating/legal owner" in their Overview tab. Conclusion: the workbook is canonical-ready; the PDF needs scrubbing or quarantine before downstream use.

# §5 — Operator action surface

Five P0 decisions surfaced in `2026-05-19_gemini_tilth_sanity_audit_redispatch.md` §4:

1. Pursue AI-safety funder cluster? (13 Tier A entries)
2. Pursue DoD AI-eval cluster? (AFWERX / DIU / SOFWERX / xTechSearch / DARPA / IES SBIR)
3. Expand FID `_schema/` to include `capital_raise` (Reg CF)?
4. Verify "DoW Pace-Setting Projects" — typo, real-but-undocumented, or hallucination?
5. Engineering plan substrate decision deferred to LOOM workstream (NOT a Tilth decision) — closure confirmation only.

# §6 — Cross-references

- `pipeline/funder_intelligence/_audits/2026-05-19_gemini_tilth_sanity_audit_redispatch.md` — verdict table + naming sweep (companion to this doc).
- `pipeline/funder_intelligence/_audits/2026-05-19_workbook_dedup_and_conflicts.md` — workbook dedup detail.
- `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` — net-new candidates appended at end.
- `/Users/goldenquill/Downloads/GoldenQuill/CLAUDE.md` — canonical Tilth state (ground truth).
- `/SOUL.md` — Five Operating Laws + Four Autonomy Rules.
