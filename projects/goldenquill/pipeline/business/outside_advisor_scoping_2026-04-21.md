# Outside Advisor Scoping — 2026-04-21

**Filed:** 2026-04-21
**Purpose:** Week 2 advisor onboarding prep. Source: Da Vinci v2 §13 DV-F-10 + `pipeline/engineering/outside_engineer_advisor_brief.md` + roadmap Group 10.
**Kickoff:** Week 2 Day 12 (2026-05-10 target); candidate outreach begins Week 1 Day 4-5.

---

## 1. Candidate Criteria (DV-F-10)

Per `pipeline/engineering/da_vinci_engineer_prompt_v2.md` §13 + `outside_engineer_advisor_brief.md`:

**Required:** senior (10+ years) in at least one of:
- Distributed systems
- AI/ML operations
- Cryptography (Ed25519 + ML-DSA-65 hybrid review is load-bearing per Architecture v7 A12)
- Language-model runtime infrastructure

**Independence constraints (from existing brief):**
- Not an Anthropic employee (cross-family review of Anthropic-authored stack)
- Not a Groq / OpenAI / Google employee (provider-independent per BYOK sovereignty posture)
- Willing to sign NDA acceptable to Josh
- Willing to review Python + markdown artifacts async
- Accessible for 2-3 hour review sessions per section

**Soft preference `[NEEDED confirmation from operator]`:**
- Familiarity with agentic-AI safety posture (not required; helpful)
- Comfort reviewing Cedar policy language
- Prior grant-world / nonprofit-infrastructure exposure (not required; useful)

---

## 2. Five-Doc Review Queue (per MVP doc §5 Tier 5 Group 10)

| # | Scope | Artifact advisor receives | Signed output file |
|---|---|---|---|
| 10.2 | Architecture v7 + amendments v7.0.1 | `pipeline/architecture/v0.1/tilth_architecture_locked.md` + v7.0.1 amendment | `pipeline/engineering/real_engineer_validation_arch_<date>.md` |
| 10.3 | All blueprints §0.5 / §1 / §2 / §3 / §4 (inc. v2.2) / §5 (inc. v6) / §6 / §7 | `pipeline/blueprint/v0.1/` directory snapshot | `real_engineer_validation_blueprint_<date>.md` |
| 10.4 | §§1-5 code + test suites | `pipeline/` code tree + `tests/` | `real_engineer_validation_code_<date>.md` |
| 10.5 | GPP tool chain | `gpp_det.py`, `gpp_council_dispatch.py`, `gpp_manifest.py` | `real_engineer_validation_gpp_<date>.md` |
| 10.5b | Cedar policies | `org_isolation.cedar`, `compound_commit.cedar`, manifest SHA256 | `real_engineer_validation_cedar_<date>.md` |

Roadmap notes "5 min, 8 expected" — the three additional docs beyond the 5-doc minimum are amendment sidecars (EN-001/002/003, TSIP v0.1) and provisioning manifest. Advisor can bundle or sign separately per their scheduling.

---

## 3. NDA Outline (scope only — full legal doc post-operator review)

Three-paragraph scope frame for the drafting pass Josh + counsel will finalize:

**Paragraph 1 — Confidentiality.** Advisor will review internal Tilth v0.1 engineering artifacts (architecture, blueprints, code, tests, policy files, operational memory). Workspace contents — including but not limited to Thesis-round transcripts, lock_history, review_lessons, admin_risk register, agent prompts, and client PROJECT_CONTEXT fragments — are proprietary to FIT Farms Commons (legal entity: FIT Farms LLC). Advisor agrees not to disclose, reproduce, or discuss these artifacts outside the review engagement without written operator consent.

**Paragraph 2 — No Derivative Rights.** Advisor gains no license, stake, or claim to the reviewed work product. Review is a ground-truth audit service; advisor's judgment is delivered in the form of signed validation docs (`real_engineer_validation_<section>_<date>.md`). Patterns, techniques, and frameworks visible in the review do not transfer to advisor for use in competing products, services, or advisory engagements. Advisor represents they are not currently engaged with — and will disclose any future engagement with — competing agentic-AI products, grant-writing systems, or the product families of the provider tier (Anthropic, Groq, Google, OpenAI, Alibaba) during the engagement.

**Paragraph 3 — Findings Authority.** Advisor signs each validation doc (pass / needs-revision per section) with a reasoned rationale + evidence pointers. Operator may reject findings but cannot alter or suppress them. Validation docs are retained in `pipeline/engineering/` as part of the permanent Tilth audit trail. Termination of the engagement does not terminate the validity of signed findings; prior signed docs remain binding record.

`[NEEDED legal review]` before advisor sign. Josh's existing NDA template from prior engagements may be adaptable; if not, counsel drafts from this outline.

---

## 4. Engagement Budget Sketch

**Window:** 2-4 weeks per roadmap §7 contingency. Audit runs Week 3 (2026-05-06 to 2026-05-12); seal in Week 4 (2026-05-13 to 2026-05-19).

**Per-doc hour estimate (8 expected artifacts):**

| Artifact | Read hours | Review / finding hours | Write-up hours | Total |
|---|---|---|---|---|
| Architecture v7 | 2 | 2 | 1 | 5 |
| Blueprints (§§0.5, 1-7) | 6 | 4 | 2 | 12 |
| §§1-5 code + tests | 8 | 6 | 2 | 16 |
| GPP tool chain | 2 | 2 | 1 | 5 |
| Cedar policies | 1 | 2 | 1 | 4 |
| Amendment sidecars (EN-001/002/003, TSIP) | 2 | 2 | 1 | 5 |
| Provisioning manifest | 1 | 1 | 1 | 3 |
| Findings consolidation + signed manifest | — | 1 | 2 | 3 |
| **Total** | **22** | **20** | **11** | **~53 hours** |

**Rate frame `[NEEDED operator decision]`:** hourly vs per-section flat. Brief notes "Open. Not equity." Standard senior-advisor rates in distsys / cryptography / LM-runtime run $200-$400/hr on rough market feel; per-section flat ($2-5k each) may be cleaner for scope discipline. Josh sets this.

**Re-audit budget:** reserve ~30% on top for cycle-2 verification after operator addresses any needs-revision findings.

---

## 5. Candidate Sourcing — Channels (no fabricated names)

Surface channels for candidate search. Do not contact until NDA outline is finalized. All candidates must pass the DV-F-10 qualification filter AND the independence constraint (not from a provider family in the router).

**Primary channels:**
- **Anthropic engineering alumni network** — former Anthropic staff now independent or at non-provider companies. Cross-family qualified by definition (they are outside the current-author family).
- **Distributed-systems practitioner networks** — e.g., Jepsen-adjacent community (Kyle Kingsbury's peer network), Papers We Love chapter organizers, academic distsys faculty doing industry consulting.
- **Cryptography review community** — Trail of Bits alumni, NCC Group alumni, cr.yp.to-adjacent peer network (for Ed25519 review), post-quantum community (for ML-DSA-65 review). `[NEEDED operator confirmation: whether paid audit shops vs individual consultants is the preferred posture.]`
- **YC / Accel / similar-vintage network** — operator-to-operator referrals from founders who have engaged senior technical advisors for infrastructure audits. Ask Josh's existing grant + cooperative contacts for their engineer-advisor references.
- **AI safety / agentic-AI community** — researchers at non-provider labs (e.g., Redwood, MIRI-adjacent, academic safety groups) familiar with LM-runtime + safety posture.
- **Cooperative-tech network** — Platform Coop Consortium engineering contacts, Drivers Cooperative engineering network, broader co-op-movement technologists.

**Do NOT source from:**
- LinkedIn cold-outreach to unvetted names
- Twitter / social platforms without prior-work pointer
- AI-generated candidate lists (the advisor selection itself must not be AI-confection per DV-F-10's spirit)

**Verification gate before outreach:** each candidate's public work (GitHub, publications, prior engagements) must show concrete artifacts matching at least one DV-F-10 qualification domain. A marketing-tier profile fails this gate.

---

## 6. Red-Flag Advisors to Avoid

Do not engage candidates who:

1. **Are employed by a provider in the router** — Anthropic, Groq, Google, OpenAI, Alibaba (Qwen). Independence is load-bearing per cross-family rigor.
2. **Work on competing agentic-AI products** — grant-writing LLM products, multi-seat agentic-council systems, agent-frameworks marketing themselves for similar workflows. Active conflicts of interest.
3. **Disagree with the sovereignty principle at a values level** — advisors who advocate phone-home telemetry, managed-edition gated features, or cross-client data pooling as default posture. CLAUDE.md sovereignty promise is non-negotiable.
4. **Push LangGraph / vLLM / local 70B / NemoClaw / Phase 3 orchestration** — the "What NOT to do" list in CLAUDE.md. Advisor who cannot audit the v0.1 scope without trying to expand it is not a fit.
5. **Have fabrication-tolerant review posture** — advisors who sign off on things they did not actually verify. Ground-truth audit is the whole point; credentialism without read-through is worse than no audit.
6. **Refuse async markdown review** — engagement shape is async artifacts, not synchronous calls. An advisor who needs live walkthroughs to form judgment is a bandwidth drain on solo-operator Josh.
7. **Require equity or stake** — `outside_engineer_advisor_brief.md` is explicit: "Not equity. Sovereignty principle — outside advisor is not a stakeholder in ship pressure."
8. **Have signed NDAs with provider-family legal teams** that could be construed as restricting honest findings about provider-consuming architectures. Ask directly; do not assume.

---

## 7. Handoff Timing

**Week 1 (2026-04-22 to 2026-04-28) — Prep.**
- Day 4-5: Surface candidate pipeline (3-5 names from channels §5). Verify each against DV-F-10 + independence filter.
- Day 6-7: Finalize NDA draft with counsel. Resolve `[NEEDED]` rate-frame decision (hourly vs per-section).

**Week 2 (2026-04-29 to 2026-05-05) — Onboarding.**
- Day 12 (2026-05-10 target): NDA signed. Scope packet delivered (5-doc review queue per §2). Kickoff call or async orientation.
- Day 13: Advisor acknowledges receipt + confirms review window. Dry-run of ship-gate criteria against advisor's reading.

**Week 3 (2026-05-06 to 2026-05-12) — Review execution.**
- Day 15-18: Advisor reviews architecture + blueprints (docs 10.2 + 10.3).
- Day 19-21: Advisor reviews code + GPP + Cedar (docs 10.4 + 10.5 + 10.5b). Operator addresses any needs-revision findings in parallel.

**Week 4 (2026-05-13 to 2026-05-19) — Seal.**
- Day 22-24: Audit findings closed. Cycle-2 re-review if any section landed needs-revision. All LOCK-internal rows promoted to LOCK-sealed in `lock_history.v1.jsonl`.
- Day 25-26: First-run acceptance — live RFA E2E. Advisor not required for first-run; applicant sign-off captured.
- Day 27: Daily log **"v0.1 SHIP. Last character of code outside-audited and sealed."**

---

## 8. Open Items for Operator

`[NEEDED]` items Josh must resolve before advisor outreach:

1. Rate frame — hourly ($200-$400/hr estimate) OR per-section flat OR alternative.
2. Single-advisor vs small-panel posture (existing brief §"Open items for Josh" lists this as undecided).
3. Soft-preference confirmation — agentic-AI safety familiarity, Cedar comfort, nonprofit-infra exposure (§1).
4. NDA legal review — adapt Josh's prior template vs counsel draft from §3 outline.
5. Paid audit shops vs individual consultants (§5 — primary-channel posture).
6. Compensation cap — if advisor review surfaces enough findings to require cycle-3, is there budget ceiling?

---

*Living document. Update when candidate pipeline surfaces names, NDA finalizes, rate-frame resolves.*
*Pair document: `pipeline/business/operator_decision_queue_2026-04-21.md` §3.6.*
*Canonical brief: `pipeline/engineering/outside_engineer_advisor_brief.md` (2026-04-19).*
