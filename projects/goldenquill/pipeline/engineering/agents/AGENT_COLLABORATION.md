# Tilth Council — Agent Collaboration Protocol (V1)

**Canonical path:** `pipeline/engineering/agents/AGENT_COLLABORATION.md`
**Scope:** V1 stable operations — interface contracts, conflict resolution, check-in structure.
**Deferred to V2:** Cross-seat learning, skill-share sessions, retrospective-driven self-improvement.

---

## 1. The Council

Six seats (per v7.0.6 SELF-LOCKED 2026-05-09). No seat outranks another. The applicant decides.

| Seat | Role | Model Family | Domain |
|------|------|-------------|--------|
| **Scout** | Discovery radar | Local-first (Ollama) | Find opportunities, verify against live sources |
| **Scribe** | Grant ghostwriter | Anthropic (Claude) | Section-by-section drafting with dialect control |
| **Editor** | Clarity lens | Different from Scribe (cross-family) | Readability, jargon detection, GOOO sorting |
| **Judge** | Funder-eye scorer | Different from Scribe (cross-family) | 12-dimension rubric scoring with evidence strings |
| **Logician** | Policy enforcement | None (deterministic Python + Cedar) | Eight validation gates, fail-closed |

**Cross-family constraint (architectural):** Editor and Judge MUST NOT share provider family with Scribe. This is not preference — it's the mechanism that catches same-model blind spots. Bindings live in `router.yaml`.

---

## 2. Pipeline Flow — Who Talks to Whom

```
Scout ──DISCOVER──→ Scout ──VERIFY──→ Operator ──REVIEW──→ Phase 0 Intake
                                                              │
                                                    ┌────────┘
                                                    ↓
                                          Logician ──KGIE Gate──→ Scribe
                                                                    │
                                                    ┌───────────────┘
                                                    ↓
                                          Logician ──POST Gates──→ Editor
                                                                     │
                                                    ┌────────────────┘
                                                    ↓
                                          Applicant reviews suggestions
                                                    │
                                                    ↓
                                          Scribe incorporates accepted edits
                                                    │
                                                    ↓
                                          Logician ──POST Gates──→ Judge
                                                                     │
                                          ┌──────────────────────────┘
                                          ↓
                                  Score ≥ 110/120? ──YES──→ Operator ──P8 Final Sign-off
                                          │
                                          NO
                                          │
                                          ↓
                                  Logician ──Revision Loop──→ Scribe (cycle N of 3 max)
                                          │
                                  cycle ≥ 3?
                                          │
                                          YES → Operator escalation
```

### Direct interfaces (V1)

| From | To | What passes | Format |
|------|----|-------------|--------|
| Scout | Logician | Discovery results + HMAC health tuple | JSON (`discovery.json`) |
| Logician | Scribe | KGIE PASS/RED/YELLOW | JSON (gate result) |
| Scribe | Logician | Draft sections | Markdown + claim tags |
| Logician | Editor | Draft cleared POST gates | Pass-through (draft md) |
| Editor | Applicant | Suggestion report | JSON (`{version}_editor.json`) |
| Applicant | Scribe | Accepted/rejected suggestions | Decision list |
| Scribe | Logician | Revised draft | Markdown + claim tags |
| Logician | Judge | Draft cleared POST gates | Pass-through (draft md) |
| Judge | Logician | Score report | JSON (`{version}_score.json`) |
| Logician | Scribe | Revision directive (if score < 110) | JSON (priority fixes + cycle count) |

### What does NOT pass between seats

- Raw LLM output (Rule 4: Clean Output — always structured data)
- Org data from a different client (Law 3: Org Isolation)
- Fabricated claims or credentials (Law 5: Applicant Brings Substance)
- Untagged claims (Law 1: RFA Is Truth — every claim needs a source tag)
- Admin-risk substitutions without applicant approval (Law 4)

---

## 3. Conflict Resolution

Seats disagree. That's by design — cross-family review exists to catch blind spots. Here's how disagreements resolve.

### Scenario 1: Editor wants clarity, Judge wants rubric keywords

**Example:** Editor flags "value-added" as jargon. Judge would deduct points for removing a rubric keyword.

**Resolution protocol:**
1. Editor's suggestion report includes `rubric_term: true/false` for every flagged term
2. If `rubric_term: true`, Editor flags it as [RUBRIC-TERM: keep] — suggestion is informational only
3. If Editor still believes the term needs context, Editor suggests ADDING a plain-language explanation alongside the rubric term, not replacing it
4. Applicant sees both perspectives and decides
5. If applicant removes a rubric keyword, Judge will deduct points — that's accurate scoring, not conflict

**Rule:** Editor never removes rubric vocabulary. Judge never inflates scores to compensate for jargon. The applicant sees the tradeoff.

### Scenario 2: Scribe's dialect choice conflicts with admin-risk terms

**Example:** Scribe uses "equity" (progressive register) but Logician flags it RED.

**Resolution protocol:**
1. Logician's flag takes precedence over dialect preference (Law 4 > dialect codebook)
2. Logician presents: term, severity, context, alternatives
3. Applicant decides: substitute, keep with justification, or use a different framing
4. Scribe rewrites ONLY after applicant approves the substitution
5. If applicant keeps the flagged term, Logician notes it in validation report but does not re-flag

**Rule:** Logician blocks; applicant unblocks. Scribe does not override Logician. Logician does not override applicant.

### Scenario 3: Judge scores low, Scribe disagrees with fix

**Example:** Judge deducts 3 points on Dimension 7 (Organizational Capacity) and prescribes adding prior grant history. Scribe believes the narrative already covers it.

**Resolution protocol:**
1. Judge's score stands — evidence-string citation is the arbiter
2. If Scribe believes the evidence IS in the draft, Scribe cites the specific paragraph in the revision
3. Judge re-scores with the cited evidence — if it genuinely addresses the criterion, score improves
4. If after 2 cycles they still disagree, Logician Gate 7 fires at cycle 3 → operator escalation
5. Operator reads both positions and decides

**Rule:** Score is based on what's written, not what's implied. If the evidence is there but Judge missed it, the revision cycle surfaces it. If it's truly not there, Scribe writes it. Three cycles max.

### Scenario 4: Scout's discovery conflicts with Logician's eligibility check

**Example:** Scout tags a candidate VERIFIED_FIT but Logician's entity-type check says the org doesn't qualify.

**Resolution protocol:**
1. Logician's gate result takes precedence (deterministic > inferential)
2. Scout's VERIFIED_FIT was based on live-synopsis reading; Logician's check is against PROJECT_CONTEXT entity type
3. If the conflict is genuine (e.g., RFA says "nonprofits only" and org is LLC), Logician is correct
4. If the conflict is a data issue (PROJECT_CONTEXT entity type outdated), operator updates PROJECT_CONTEXT
5. Scout does NOT override Logician's eligibility gate

**Rule:** Logician is deterministic. Scout is inferential. When they conflict on a deterministic question (entity type, geography, deadline), Logician wins. When they conflict on a judgment question (fit quality, relevance), Scout's assessment goes to operator for REVIEW.

### General escalation path

```
Seat disagrees with another seat's output
    ↓
Is the disagreement about a deterministic fact? (entity type, deadline, term severity)
    YES → Logician's determination stands
    NO ↓
Is it within the 3-cycle revision limit?
    YES → Next revision cycle resolves it with cited evidence
    NO ↓
Operator escalation (Logician Gate 7: F-REVISION-LOOP-EXCEEDED)
    ↓
Operator reads both positions, decides, pipeline continues
```

---

## 4. Weekly Check-In Structure (V1)

Purpose: operator visibility into pipeline health. NOT a learning/improvement session (V2).

### Format

**When:** Weekly, operator-initiated (or skipped if no pipeline activity that week)

**Duration:** Single-pass report, not a meeting. Each seat writes its section; operator reads.

**Report structure (saved to `pipeline/reports/weekly/{YYYY-MM-DD}_checkin.md`):**

#### Scout Section
- Channels: health status per channel (A-F)
- Candidates: discovered / verified / elevated this week
- Urgency distribution: RED / YELLOW / GREEN counts
- Issues: degraded channels, verification failures, stale cache

#### Scribe Section
- Drafts: sections produced this week, grant IDs
- KGIE status: any blocked grants (F-KGIE-INCOMPLETE)
- Dialect distribution: which registers used
- Open flags: unresolved [INFERRED] or [UNSOURCED] count

#### Editor Section
- Reviews: drafts reviewed, suggestion counts
- Readability: average FK grade, passive voice %, acronym density
- GOOO sorts: corrections made (goals mislabeled as outcomes, etc.)
- Acceptance rate: what % of suggestions did applicant accept

#### Judge Section
- Scores: grants scored, average score, threshold met/not-met
- Revision cycles: grants in cycle 1 / 2 / 3 / escalated
- Top deduction dimensions: which of the 12 are weakest across grants
- Cross-rubric notes: any rubric library gaps identified

#### Logician Section
- Gates: total executions, PASS / RED / YELLOW counts
- Blocking violations: F-* codes fired this week
- Admin-risk: terms flagged, approvals pending, new terms added to register
- Revision loops: any F-REVISION-LOOP-EXCEEDED events
- Org isolation: any F-ORG-ISOLATION-BREACH events (should always be zero)

#### Operator Action Items
- Autogenerated from: RED blocks pending resolution, [NEEDED] fields in PROJECT_CONTEXTs, operator escalations from Gate 7, admin-risk approvals pending

---

## 5. V1 Operating Constraints

These are the boundaries for V1. They exist to keep the pipeline stable before adding complexity.

1. **No cross-seat learning.** Seats do not modify their own behavior based on other seats' outputs. Judge's scoring patterns do NOT automatically inform Scribe's writing. Editor's clarity fixes do NOT feed back into Scribe's voice model. Each seat operates from its prompt + reference databases + operator direction. Cross-seat adaptation is V2 scope.

2. **No autonomous self-improvement.** Seats do not rewrite their own prompts, update their own reference databases, or modify their own gate thresholds. All updates go through operator review and version-controlled commits. Hermes-style skill acquisition is V2.

3. **No inter-seat negotiation.** Seats do not argue with each other. They produce outputs, Logician validates, operator decides. The conflict resolution protocol (Section 3) is a HUMAN-mediated process, not an automated negotiation loop.

4. **Revision cap is hard.** Three Scribe-Judge cycles, then operator. No seat can vote to extend. The operator can reset, but the pipeline cannot.

5. **Weekly check-in is reporting, not retrospective.** Seats report metrics and issues. They do not propose process changes, vote on improvements, or self-organize. Process evolution is operator-directed.

---

## 6. Reference Database Ownership

Each seat has reference databases it reads. Ownership determines who can propose updates.

| Database | Path | Owner | Read By |
|----------|------|-------|---------|
| Channel Registry | `references/channel_registry.yaml` | Scout + Operator | Scout, Logician |
| Dialect Codebook | `references/dialect_codebook.yaml` | Scribe + Operator | Scribe, Logician (Gate 4) |
| Jargon Registry | `references/jargon_registry.yaml` | Editor + Operator | Editor |
| Rubric Library Index | `references/rubric_library_index.yaml` | Judge + Operator | Judge, Logician (Gate 8) |
| Gate Registry | `references/gate_registry.yaml` | Logician + Operator | Logician, all seats (read-only) |
| Admin-Risk Register | `references/admin_risk_register.yaml` | Logician + Operator | Logician (Gate 4), Scribe (awareness) |
| Overlooked Expenses | `references/overlooked_expenses_checklist.yaml` | Scribe + Operator | Scribe, Logician (Gate 5) |

"Owner" means: the seat can PROPOSE updates (new entries, corrections, severity changes). The OPERATOR approves all changes. No seat modifies a reference database unilaterally.

---

## 7. V2 Roadmap Preview (deferred — not implemented in V1)

For operator awareness only. These are planned V2 capabilities, not V1 features.

- **Cross-seat learning protocol:** Judge's scoring patterns inform Scribe's writing priorities. Editor's top-flagged jargon feeds back into Scribe's dialect codebook. Scout's verification failures update channel health predictions.
- **Skill-share sessions:** Each seat presents its constraints, interfaces, and what it needs from others. Structured format for knowledge transfer.
- **Retrospective loops:** Weekly check-in evolves into a learning session where seats propose process improvements, operator approves, and reference databases update.
- **Autonomous skill acquisition:** Seats can create reusable skills from experience (Hermes pattern). Gated by operator approval.
- **Calibration drift detection:** Judge monitors its own scoring consistency across grants and flags drift to operator.

---

*V1 — 2026-04-20 — Initial collaboration protocol. Stable operations focus. Cross-seat learning and self-improvement deferred to V2 per operator direction.*
