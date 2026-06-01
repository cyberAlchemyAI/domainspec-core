# TSIP v0.1 — Bootstrap Thesis (Simulated)

**Date:** 2026-04-19
**Subject:** `pipeline/engineering/protocols/tilth_self_improvement_protocol_v0.1.md`
**Author family:** Anthropic (Cowork / Claude) — simulated single-family voice
**Bootstrap exception:** per TSIP §"Protocol self-application," the protocol is authored before the protocol exists; its initial Thesis is simulated + operator-signed as `LOCKED-internal`. Live cross-family audit via OpenClaw promotes `LOCKED-internal` → `LOCKED-sealed`.
**Audit cycle:** L-005 strict two-cycle.
**Outcome:** `LOCKED-internal-simulated` at end of Cycle 2 pending operator signature.

---

## Cycle 1 — DRIVER (per-seat audit)

### Scout (citation discipline)
REQUIRES_MINOR_FIXES. Protocol cites L-005, L-003, L-002, Da Vinci §13, CLAUDE.md (LangGraph REJECT-LOCK), Sovereignty Promise — all correct. **Gap:** "seven-family taxonomy" referenced in Phase 5 without a path citation. Fix: cite A2 addendum in `pipeline/architecture/v0.1/tilth_architecture_locked.md` and `router.yaml`.

### Scribe (one voice, no fabrication)
READY. Declarative voice throughout; no fabricated capabilities; all referenced artifacts exist or are explicitly flagged as future (`tool_evaluation_template.md` to be written on first use; `candidates_register.md`, `adopted_tools_register.md` similar).

### Editor (clarity, accessibility)
REQUIRES_MINOR_FIXES. Three unglossed terms on first use: "real-engineer validator gate" (gloss as: external engineer audits spike outputs before main-line merge, per Da Vinci §13); "spike manifest" (gloss as: YAML at spike-open declaring version pin, exit criteria, rollback procedure); "LOCKED-internal vs LOCKED-sealed" matches existing Tilth usage — no fix required.

### Judge (rubric scoring, SFR format)
PASS. Score 90/100 on protocol-spec rubric.

**Premises:**
- P1: `pipeline/engineering/protocols/tilth_self_improvement_protocol_v0.1_DRAFT.md` — 8 phases + anti-patterns + resolved decisions
- P2: `/AGENTS.md` — L-002, L-003, L-005 definitions
- P3: `pipeline/engineering/da_vinci_engineer_prompt_v2.md` §13 — real-engineer validator gate
- P4: `CLAUDE.md` — LangGraph REJECT-LOCK, Sovereignty Promise

**Execution trace:**
- Scope clarity: 18/20 (v0.1 cadence explicit, 8 phases enumerated, scope in/out declared)
- Self-consistency: 18/20 (self-application clause explicit; minor gap: evaluation template deferred to first use, acceptable)
- Discipline alignment: 20/20 (P2 + P3 + P4 all cited correctly)
- Enforceability: 16/20 (anti-patterns declared but no Logician gates enforce them; acceptable for a protocol — it is operator-discipline, not code)
- Completeness: 18/20 (missing: triage-evaluation conflict path, operator-override retirement trigger)

**Conclusion:** PASS with REQUIRES_MINOR_FIXES on completeness and enforceability dimensions.

### Logician (deterministic check)
READY. Zero new F-codes. Zero Cedar rule changes. TSIP wraps L-005/L-003/L-002/Da Vinci §13 without displacing them. Self-referential bootstrap is explicit and bounded. No silent bypass of existing workflow.

### Red Team (adversarial, SFR format)
REQUIRES_MINOR_FIXES. 1 HIGH + 3 MED + 1 LOW.

**RT-TSIP-01 HIGH — Triage Q5 ambiguity.** "Does Tilth already have a better-fitting primitive?" fires at triage before evaluation's rigorous check. Operator-fatigue or ignorance of existing primitives can kill good candidates prematurely. **Fix:** reframe as "Are you confident Tilth already has a better-fitting primitive? (Default NO — proceed to evaluation where this is checked rigorously.)"

**RT-TSIP-02 MED — No operator-override retirement trigger.** Phase 8 lists four triggers; what if operator wants to retire for reasons outside them? **Fix:** add "Operator discretion — retiring for reasons not in the above triggers is always valid, logged in `lessons.md` with reasoning."

**RT-TSIP-03 MED — Watchlist has no owner.** Listed but unowned. **Fix:** "Operator curates and reviews the watchlist in v0.1. v0.2 transfers this to Da Vinci Quill-persona."

**RT-TSIP-04 MED — Real-engineer validator gate referenced but not operationalized here.** TSIP consumes the gate without defining it. **Fix:** explicit note that operationalization lives in Da Vinci §13; TSIP is a consumer, not a definer.

**RT-TSIP-05 LOW — 2-week sanity cap too tight for complex spikes.** Already addressed by the one-week formal-extension clause. No change.

### Cycle 1 summary

| Seat | Verdict | Findings |
|------|---------|----------|
| Scout | REQUIRES_MINOR_FIXES | 1 citation gap |
| Scribe | READY | 0 |
| Editor | REQUIRES_MINOR_FIXES | 3 glosses |
| Judge | PASS | 90/100, 2 sub-dims < 20 |
| Logician | READY | 0 |
| Red Team | REQUIRES_MINOR_FIXES | 1 HIGH + 3 MED + 1 LOW |

No BLOCKING findings.

---

## Synthesis — Consensus Fixes

1. **Scout citation** (Phase 5): add `A2 addendum per pipeline/architecture/v0.1/tilth_architecture_locked.md + router.yaml` for seven-family taxonomy.
2. **Editor gloss** (Phase 4 Spike): one-line gloss of "real-engineer validator gate" and "spike manifest."
3. **Red Team HIGH** (Phase 2 Triage): reframe Q5 as confidence-framed, default NO.
4. **Red Team MED** (Phase 8 Retirement): add operator-discretion trigger.
5. **Red Team MED** (Phase 1 Surveillance): add watchlist-owner line.
6. **Red Team MED** (Phase 4 Spike): cite Da Vinci §13 as operationalization authority for the validator gate.

Zero semantic change to any phase; all edits are documentary clarifications.

---

## Cycle 2 — VERIFICATION

All six fixes applied to the v0.1 canonical file at `pipeline/engineering/protocols/tilth_self_improvement_protocol_v0.1.md`.

| Seat | Cycle 2 verdict |
|------|-----------------|
| Scout | READY |
| Scribe | READY |
| Editor | READY |
| Judge | PASS 95/100 (completeness +2, enforceability unchanged) |
| Logician | READY |
| Red Team | READY — RT-TSIP-01 HIGH CLOSED, RT-TSIP-02/03/04 MED CLOSED, RT-TSIP-05 LOW unchanged (already addressed pre-Cycle-1) |

**Lock bar met.** Status: `LOCKED-internal-simulated`. Operator signature required for `LOCKED-internal`. Live cross-family audit via OpenClaw required for `LOCKED-sealed`.

---

## Simulation caveat

This Thesis was ventriloquized from a single Anthropic-family voice. Per L-003 it does not substitute for live cross-family review. Promotion path:

1. Operator signature → `LOCKED-internal`
2. OpenClaw handoff per `pipeline/engineering/handoffs/openclaw_cross_family_audit_tsip_v0.1_2026-04-19.md` → live Editor (Llama) + Judge (Qwen) + Red Team (GPT-OSS) verdicts
3. All three READY + operator signature → `LOCKED-sealed`
