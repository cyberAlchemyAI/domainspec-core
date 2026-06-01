# Agent SDK Thesis — Live Cross-Family Audit Synthesis

**Date:** 2026-04-19
**Audit subjects:** EN-001 (Scribe-via-Agent-SDK Spike), EN-002 (SDK Lifecycle Vocabulary Reference Table)
**Audit trail:** this directory — editor_verdict_cycle1.md, judge_verdict_cycle1.md, red_team_verdict_cycle1.md
**Author family:** Anthropic (Cowork / Claude authored the amendments + simulated Thesis)
**Reviewer families, live:** Meta (Llama 3.3 70B / Groq), Google (Gemini 2.5 Pro), OpenAI-OSS (GPT-OSS 120B / Groq)
**Handoff spec:** `pipeline/engineering/handoffs/openclaw_cross_family_audit_agent_sdk_2026-04-19.md`

## Promotion recommendation

**CYCLE-2-REQUIRED.** Not `LOCK-SEALED` yet. Live cross-family found substantive findings that the simulated Cycle 2 closed prematurely. Fix the findings, re-run the audit, then re-evaluate promotion.

## Summary

| Seat | Family | Verdict | Score |
|------|--------|---------|-------|
| Editor | Meta (Llama 3.3 70B) | Structured feedback — jargon + voice issues | n/a (exempt per A3) |
| Judge | Google (Gemini 2.5 Pro) | REQUIRES_MINOR_FIXES | 94/100 |
| Red Team | OpenAI-OSS (GPT-OSS 120B) | REQUIRES_MINOR_FIXES | 1 HIGH + 4 MED + 1 LOW |

Simulated Cycle 2 had declared all seats READY with Judge 96/100 and zero in-scope Red Team findings. The live cross-family audit dissents materially. This is the exact pattern L-003 exists to catch.

## Agreement with simulated debate

- **Scope clarity:** Judge agrees — scope in/out explicit, queue position explicit. 20/20.
- **Cross-family rigor preservation:** Judge agrees — Scribe-only spike does not create cross-family issues (Scribe already Anthropic; no change to audit-process cross-family). 20/20.
- **Cedar/Logician integration:** Judge agrees — F-code deferral explicit; Cedar authority over SDK preserved; explicit rejections (canUseTool etc.) correctly reject. 20/20.
- **Sovereignty declaration:** Judge agrees as STATED. Red Team challenges the execution (see below).

## Live dissent — findings the simulated audit missed

### RT-NEW-01 — HIGH — Rollback doesn't address external side-effects

**Finding:** The amendment says "rollback = branch revert + zero-state migration" but never addresses writes to mutable external stores during the spike. If the Scribe SDK agent writes to ChromaDB, the vault, lessons.md, or any external state during its run, a branch revert will NOT undo those changes.

**Simulated Cycle 2 closure was wrong.** Cycle 1 RT-A-01 HIGH was closed by "branch revert + zero-state migration" — but that phrase only covers the code/config axis. External-state writes during spike execution are a separate rollback axis not addressed.

**Required fix (Cycle 2):** Enumerate all external resources the spike may touch during execution. Require either (a) a transactional sandbox that isolates external writes and discards them on abandonment, or (b) an explicit cleanup script that undoes external writes as part of the rollback procedure. The amendment text must cite the sandbox/cleanup mechanism concretely.

### JUDGE-DISSENT — MED — Reversibility cost docked 6/20

**Finding:** Gemini 2.5 Pro agrees that the rollback METHOD ("branch revert + zero-state migration") is low-cost in principle, but dings 6 pts because the PROCEDURE (exact commands, state artifacts to revert, decision gates) isn't concrete in the amendment text. Same axis as RT-NEW-01 but scored rather than attacked.

**Required fix (Cycle 2):** Add a concrete rollback procedure section to EN-001 listing:
- Exact `git` or branch-revert commands
- Specific state artifacts that must be inspected for cleanup (ChromaDB collections, vault paths, lessons.md entries, any temp files, any manifest entries)
- Decision gates (who signs the rollback? operator alone, operator + Da Vinci, or automated on FAIL verdict?)
- Timeline (rollback must complete in ≤ 1 hour; if not, escalation path)

### RT-NEW-02 — MED — No detection mechanism for silent SDK breaking changes

**Finding:** The amendment's "controlled dependency" clause names a quarterly audit and an exit criterion but provides no concrete detection mechanism for silent breaking changes — e.g., a hidden telemetry activation in a minor SDK version bump, or an API signature change that doesn't crash but alters semantics.

**Simulated Red Team RT-A-03 closed this with "controlled dependency declaration + version pin + quarterly audit" — but those are policy statements, not detection mechanisms.**

**Required fix (Cycle 2):** Implement (in the spike manifest) an automated integration test that validates the SDK's public interface against a pinned expected shape AND monitors outbound network traffic during the test. Test runs at spike-open AND on each version bump AND at the quarterly audit. Fails trigger human review before spike continues.

### RT-NEW-03 — MED — "LOCK" status ambiguity in queue preconditions

**Finding:** Queue positioning references `§6 Operating Envelope blueprint LOCK, §4 Logician v2.2 LOCK, §0.5 v4 refresh, real-engineer validator gate` as preconditions but doesn't define what constitutes a "landed" LOCK. Is a merged PR sufficient? Does CI need to pass? Does operator signature required? Each interpretation allows different "spike is ready to start" moments.

**Required fix (Cycle 2):** Require explicit lock-status flags in a shared state file (e.g., `pipeline/engineering/spike_preconditions.yaml`) that must be set to `landed: true` by the operator for each of the four preconditions before the spike manifest can be authored. Ambiguity resolution at the file level, not prose level.

### RT-NEW-04 — MED — Mapping table risks silent vocabulary drift

**Finding:** EN-002's SDK lifecycle map introduces a shared taxonomy. Future contributors might import the table and begin using SDK event names directly in Tilth code, silently merging the vocabularies. The amendment claims "not a substitution" but does not enforce that claim operationally.

**Required fix (Cycle 2):** Add to EN-002 an enforcement hook (ideally a lint rule / pre-commit check) forbidding references to SDK lifecycle identifiers in production Tilth code. Exception: the mapping table itself. References require a review checkpoint acknowledging the drift risk.

### RT-NEW-05 — LOW — Sovereignty verification is asserted, not tested

**Finding:** Sovereignty preservation relies on "no phone-home" as an asserted property. Not tested. SDK default error reporting / diagnostic telemetry could transmit data under specific error conditions without the operator noticing.

**Required fix (Cycle 2):** Add a sovereignty test to the spike exit criteria: force the SDK into common error states (auth failure, timeout, invalid tool arg, network blip) and inspect outbound traffic. All outbound traffic must be to the pinned Anthropic API endpoint (and only there). Any additional destinations = sovereignty violation → spike FAIL.

### RT-NEW-06 — MED — L-003 precedent risk for future SDK adoptions

**Finding:** The amendment focuses exclusively on the Anthropic-family Scribe seat. But success of EN-001 creates precedent for SDK adoption in other seats. Any future SDK adoption for a non-Anthropic seat (Editor, Judge, Red Team) would require LiteLLM translation — which the amendment itself flags as risky — OR create an additional Anthropic-authored layer in a non-Anthropic seat that would violate L-003.

**Required fix (Cycle 2):** Add a policy statement to EN-001 that any future SDK adoption for a non-Anthropic seat must pass its OWN L-003 cross-family audit and its OWN spike — no precedent carries from the Scribe spike. Prevents "Scribe spike passed, now let's do Editor too without re-audit."

### EDITOR NOTES — jargon + voice

Editor's structured feedback flagged:

- Unglossed terms on first use: "deferred engineering queue entry", "time-boxed", "controlled dependency", "skills semantic dispatch", "sdk_lifecycle_map.archive"
- Voice inconsistency: amendment surface mixes declarative/present-tense with reflective past-tense in some passages
- Accessibility: non-LLM-builders would struggle with several sections
- Structural: suggested breaking "controlled dependency" into clear bulleted steps

**Required fix (Cycle 2):** Pass through EN-001 + EN-002 adding one-line glosses for the five flagged terms on first use. Normalize voice to declarative present-tense throughout amendment surface (reflection belongs in the debate doc, not the amendment). Break "controlled dependency" clause into bulleted sub-claims.

## Cycle 2 action items (consolidated, in priority order)

1. **[HIGH]** Concrete rollback procedure in EN-001 — shell commands, state artifacts, decision gates, timeline. Addresses RT-NEW-01 + JUDGE-DISSENT.
2. **[MED]** SDK breaking-change detection mechanism — automated integration test in spike manifest. Addresses RT-NEW-02.
3. **[MED]** Concrete "LOCK landed" definition — shared state file + operator flags. Addresses RT-NEW-03.
4. **[MED]** Vocabulary drift enforcement hook on EN-002's mapping table. Addresses RT-NEW-04.
5. **[MED]** L-003 precedent statement — each future SDK adoption audits independently. Addresses RT-NEW-06.
6. **[LOW]** Sovereignty test covering SDK error states. Addresses RT-NEW-05.
7. **[DOCUMENTATION]** Gloss five jargon terms; normalize voice. Addresses Editor.

## Post-fix re-audit path

Once Cycle 2 fixes land on EN-001 and EN-002, re-run this same cross-family audit via OpenClaw. If all three seats READY with zero new in-scope findings, the amendments promote `LOCKED-internal-simulated` → `LOCKED-sealed` pending operator signature.

## What this audit already vindicated

**L-003 cross-family rigor is not ceremonial.** The ventriloquized Cycle 2 declared READY. The live cross-family audit found 1 HIGH + 5 MED findings of real substance. Without L-003, these would have shipped into LOCKED-sealed artifacts and surfaced later as bugs during spike execution (RT-NEW-01 especially — a rollback that doesn't actually roll back is the exact kind of failure that rolls forward into incidents).

The handoff pattern + CLI remediation + Google plugin enablement this session are all validated by this audit's quality. Infrastructure works; cross-family review produces signal.
