# PHASED_CARD_SYSTEM_RESEARCH_AUDIT

**Pointer file — full content lives at `docs/phased_card_system_research_audit_extracted_2026-05-17.md` (operator-specified save location, 2026-05-17 Cowork dispatch).**

| Field | Value |
|---|---|
| Filed | 2026-05-17 |
| Original | `7a9f14e9-Phased_Card_System_Research_Audit.docx` (operator upload, Cowork) |
| Extracted | `docs/phased_card_system_research_audit_extracted_2026-05-17.md` (381 lines, 5 tables, ~56KB text, 60+ .gov/.edu citations) |
| Workspace | `/Users/goldenquill/Downloads/GoldenQuill/` |
| Self-description | "Multi-run deep-research audit of the Golden Quill / Tilth Card System" (per §Architectural Synthesis and Recommendations) |
| Authored by | External research output (Gemini-style deep-research style); core props blank, no human author |
| Scope | External compliance + architecture audit of the Card System workstream — orthogonal to the on-disk Run 1 / Run 2 phased-research siblings in this folder. NOT a continuation of the Run 1 lifecycle/loader audit. |
| Constraints honored | Read-only extraction; no edits to LOCKed files, cards, blueprints, schemas, or gate modules. |

---

## §0. Why this is the 5th sibling in this folder — AND the canonical research feedstock for the v0.2 first-wave PRP manifest

The four existing siblings (`CANONICAL_NAMING_AND_ORTHOGONALITY_AUDIT.md`, `CARD_LIFECYCLE_AND_LOADER_GOVERNANCE_AUDIT.md`, `FILE_BY_FILE_PATCH_QUEUE_PRE_V0_2.md`, `INITIAL_CTO_HANDOFF_BLOCKERS.md`) are **on-disk inspection audits** of the live Tilth card runtime (loader.py, models.py, schemas, gate modules, blueprint amendments). They speak the F-CARDS-* / draft_status / runtime_loadable vocabulary.

**This audit is the explicit content source for 5 of the 6 entries in the active Program Rule Pack manifest.** The PRP manifest at `pipeline/program_rule_packs/_manifest/active_prps.yaml` (generated 2026-05-17T22:00:00Z) **references the extracted .md by exact path** and maps each PRP entry to a specific audit recommendation:

| PRP entry | Audit synthesis recommendation | Audit section |
|---|---|---|
| `TILTH-PRP-FERPA-COPPA-HIPAA` | #1 Decouple Student Profiles | §Privacy Protections, COPPA, and the HIPAA Interface + §Golden Quill Identity Gateway and FERPA Compliance |
| `TILTH-PRP-2CFR200` | #4 Programmatic Compliance Locks (procurement) | §Uniform Guidance and 2 CFR 200 Procurement Tiers |
| `TILTH-PRP-DAVIS-BACON` | #3 Automate Davis-Bacon Checking | §Davis-Bacon Act and Labor Compliance Integration |
| `TILTH-PRP-NEPA-24CFR58` | #4 Programmatic Compliance Locks (NEPA) | §NEPA and HUD 24 CFR Part 58 Environmental Review |
| `TILTH-PRP-SUBCHAPTER-T` | #5 Enforce Cooperative Equity Rules | §Subchapter T Tax Neutrality and State Cooperative Statutes |
| `TILTH-PRP-USDA-VAPG-FY26` | (not from audit; program_specific exemplar) | — |

The audit's content is canonical PRP material — live program law that the workspace correctly receives as PRP bodies, NOT as card content. The doc's own "Tilth Card platform" framing is the deep-research author's metaphor (it conflates cards / PRPs / runtime gates into one fintech card abstraction); the workspace's canonical separation (per `research/golden_quill_card_system_run_bundle/CTO_HANDOFF_BRIEF.md` §"What the CTO should not let drift") is preserved by routing this content to PRPs.

The doc is filed in this folder because synthesis recommendation #2 (Standardize Underwriting Ratios) lives at the CDFI-underwriting layer that intersects the CLC `credit_underwriting` card surface, and because the doc's tables (state machine, risk matrix) touch the lifecycle vocabulary the existing four siblings audit.

---

## §1. Document structure (full content at extracted path)

Five top-level sections:

1. **Architectural Orthogonality and Multi-Tenant Isolation** — FERPA School Official / Audit-Evaluation / Studies Exceptions; COPPA; HIPAA interface; Section 508 / WCAG 2.1 AA. Threads "Golden Quill Identity Gateway" as the student-PII isolation boundary distinct from "Tilth Card platform" transactional ledger.
2. **Lifecycle Governance and Federal Compliance Flow-Downs** — 2 CFR 200 procurement tiers (micro-purchase / SAT / formal bid); Build America Buy America Act material rules + waivers; Davis-Bacon weekly pay + WH-347; NEPA / HUD 24 CFR Part 58 environmental review levels (Exempt / CENST / CEST / EA / EIS) + Choice-Limiting Action Blocker.
3. **FinTech Integration, Multi-Stakeholder Capitalization, and Underwriting** — Subchapter T patronage allocation; Virginia Code Title 13.1 cooperative limits ($1,000 par, single-vote, 10% reserve, two-thirds non-voting stock consent); equity redemption methodologies (revolving fund / percent-of-all-equities / special); CDFI underwriting standardization (DSCR, NOI, days cash) for secondary-market sales; LIHTC + charter school facilities monitoring.
4. **Regional Food Systems and Federal Grant Alignment** — USDA Community Facilities + Economic Impact; ARC Local Food Systems; philanthropic arts frameworks (Mellon, NEA disability-forward grantmaking, Rhode Island arts).
5. **CTO-Grade Technical Handoff Artifacts and Executables** — full relational DB schema (~150 lines SQL DDL), lifecycle state machine routing, risk + compliance matrix, architectural synthesis with 5 named recommendations, Works Cited (60+ sources).

## §2. Load-bearing directives (operator-reviewable; not yet a backlog item)

Verbatim from §Architectural Synthesis and Recommendations:

1. **Decouple Student Profiles** — identity DB separate from transactional ledger; external gateways reference tokens, not PII (FERPA School Official Exception).
2. **Standardize Underwriting Ratios** — DSCR, NOI, days cash on hand exposed in active loan dashboards to bridge community-lending flexibility ↔ institutional secondary-market structure.
3. **Automate Davis-Bacon Checking** — WH-347 form ingestion, weekly payroll verification, Statement of Compliance audit, prevailing-wage delta flagging.
4. **Deploy Programmatic Compliance Locks** — micro-purchase threshold checkout block (quotes required); construction payout block until Environmental Review Record signed.
5. **Enforce Cooperative Equity Rules** — Subchapter T patronage allocation; Virginia Code Title 13.1 stock + voting limits enforced at the corporate-registry-module level.

## §3. Routing posture (Dispatch orchestrator, 2026-05-17 Cowork — REVISED)

- **Primary route**: canonical PRP content source for the v0.2 first-wave Program Rule Pack graduation ceremony, per the audit-referencing `active_prps.yaml` manifest authored 22:00Z today. PRP body authoring at v0.2 first wave draws from this audit's regulatory sections.
- **Secondary route (this folder)**: filed alongside the four Card System runtime audits because the audit's CDFI underwriting standardization content (synthesis #2) touches the CLC `credit_underwriting` surface and its state-machine/risk-matrix tables share lifecycle vocabulary with the existing siblings.
- **Not folded** into Run 2 CIC handbacks, Run 4 batch supervisor brief, or the just-landed issue-posting script (orthogonal in-flight work).

## §4. Unaddressed next steps (surfaced for operator decision)

Now that the audit is on disk and the PRP manifest references it, several next steps unblock. None of these are taken yet — each requires an operator call:

1. **Draft the 6 PRP YAML bodies** against `pipeline/program_rule_packs/_schema/program_rule_pack.schema.json` using the audit as research source. Five of six bodies are derivable from the audit; the sixth (`TILTH-PRP-USDA-VAPG-FY26`) requires the published FY26 NOFO. Operator sign-off and Ed25519 signature gate the v0.2 first-wave ceremony.
2. **Sample-verify the audit's 60+ .gov/.edu citations** before any PRP body claims rest on them. Deep-research-output hygiene per L-005 / L-023 precedent — fail fast on hallucinated URLs before they propagate into signed PRP bodies.
3. **Run the codex repo-verification pass** pre-staged at `research/golden_quill_card_system_run_bundle/NEXT_COMMAND.md`. That pass is the runtime-side complement; this audit is the law-side feedstock. They likely converge at the v0.2 first-wave ceremony.
4. **Reconcile the doc's "Tilth Card platform" framing** with the canonical product naming chain in CLAUDE.md. The audit author treats Golden Quill + Tilth + identity gateway + transactional fintech as a single platform; the canonical model separates hardware (Golden Quill) / AI council (Tilth) / phone interface (Cultivator) / Stage-5 commons (Sovereign Node). PRP bodies authored from this audit must use canonical names, not the audit author's framing.
5. **Promote synthesis recommendations #1-#5 to `docs/TECHNICAL_BACKLOG.md`** as Gate-2 / post-Gate-2 entries (or note explicitly that they live as PRP bodies and don't need backlog rows). Currently neither — operator call.

---

**End of pointer file. Full extracted text at `docs/phased_card_system_research_audit_extracted_2026-05-17.md`.**
