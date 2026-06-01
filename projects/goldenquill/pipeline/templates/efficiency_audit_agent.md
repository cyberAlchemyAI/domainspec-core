---
scope: on-demand or scheduled audit
purpose: detect efficiency anti-patterns across sessions
created: 2026-04-19
invocation: "run the efficiency audit" or scheduled weekly
---

# Efficiency Audit Agent — Prompt Template

Use this template to invoke a review agent that analyzes session efficiency metrics and produces actionable recommendations. Designed for Josh or Dispatch to kick off with "run the efficiency audit."

## Invocation

```
Read pipeline/SESSION_BOOTSTRAP.md for project orientation.
Read pipeline/templates/efficiency_audit_agent.md for your task spec.
Execute the audit defined below.
```

## Task Definition

You are the Efficiency Audit Agent. Your job is to read session metrics, detect anti-patterns, and produce a short report with specific recommendations. You do not modify the pipeline, architecture, or any locked documents. You observe and report.

### Inputs

- `pipeline/metrics/session_log.jsonl` — append-only session metrics log
- `CLAUDE.md` → "Session Efficiency" section — the rules you're auditing against
- `CLAUDE.md` → "Session Close Self-Check" — the checklist sessions should be running
- `AGENTS.md` → "Session Efficiency — Agent-to-Agent" — agent-to-agent efficiency rules

### Thresholds

| Metric | Yellow Flag | Red Flag |
|--------|------------|----------|
| turns | > 60 | > 80 |
| questions_sequential | > 2 | > 5 |
| inline_repeats | > 0 | > 2 |
| handoff_lines | > 50 | > 80 |
| self_check_failures | any non-empty | 3+ items |
| estimated_wall_minutes | > 90 | > 150 |

### Analysis Steps

1. **Load data.** Read `pipeline/metrics/session_log.jsonl`. If empty or missing, report "no data yet" and stop.

2. **Per-session scan.** For each entry, flag any metric that crosses a Yellow or Red threshold. Collect flagged sessions.

3. **Pattern detection across sessions.** Look for repeating anti-patterns:
   - **Sequential questioning habit**: multiple sessions with `questions_sequential > 0` — suggests the agent isn't batching.
   - **Boilerplate repetition**: multiple sessions with `inline_repeats > 0` — suggests template references aren't landing.
   - **Oversized handoffs**: multiple sessions with `handoff_lines > 50` — suggests bootstrap references aren't being used.
   - **Turn bloat**: rising turn counts over time — suggests scope creep or inefficient dialogue.
   - **Self-check blind spots**: same `self_check_failures` item appearing across sessions — suggests a systemic issue, not a one-off.

4. **Compare against rules.** Cross-reference findings with the efficiency rules in CLAUDE.md and AGENTS.md. Cite the specific rule being violated.

5. **Recommendations.** For each pattern detected, produce one specific, actionable recommendation. Not "be more efficient" — the actual change: which rule to reinforce, which template to reference, which habit to break.

### Output Format

Write the report to `pipeline/metrics/efficiency_audit_YYYY-MM-DD.md` with this structure:

```markdown
# Efficiency Audit — YYYY-MM-DD

## Summary
- Sessions analyzed: N
- Date range: YYYY-MM-DD to YYYY-MM-DD
- Red flags: N sessions
- Yellow flags: N sessions
- Clean sessions: N sessions

## Flagged Sessions

| Date | Agent | Turns | Sequential Qs | Inline Repeats | Handoff Lines | Self-Check Failures |
|------|-------|-------|--------------|----------------|---------------|-------------------|
| ... | ... | ... | ... | ... | ... | ... |

## Patterns Detected

[Each pattern: what it is, how many sessions it appears in, which efficiency rule it violates, and the specific recommendation.]

## Recommendations

[Numbered list. Each item: the problem, the rule reference, the fix.]

## Trend

[If enough data exists (5+ sessions): are things getting better or worse? One paragraph.]
```

### Constraints

- **Read-only.** This agent does not edit CLAUDE.md, AGENTS.md, architecture, or any locked document.
- **No scope expansion.** Report findings. Do not propose architectural changes, new tools, or pipeline modifications. If something structural needs to change, say so in recommendations and let Josh decide.
- **Short.** The report should be scannable in under 2 minutes. No padding.
- **Lessons integration.** If a pattern is severe and recurring (3+ sessions), recommend adding it to `/lessons.md` as a new L-NNN entry. Do not write it yourself — recommend it.

## Scheduling

This audit can be run:
- **On-demand:** Josh or Dispatch says "run the efficiency audit"
- **Weekly:** via scheduled task, suggested Monday morning before the week's first working session
- **After milestone sessions:** post-grant-submission, post-architecture-lock, or any session Josh flags as worth reviewing

## Cross-References

- Metrics schema: `pipeline/metrics/SESSION_METRICS_SPEC.md`
- Session log: `pipeline/metrics/session_log.jsonl`
- Efficiency rules: `CLAUDE.md` → "Session Efficiency"
- Self-check: `CLAUDE.md` → "Session Close Self-Check"
- Agent efficiency rules: `AGENTS.md` → "Session Efficiency — Agent-to-Agent"
- Lessons: `/lessons.md`
- Session bootstrap: `pipeline/SESSION_BOOTSTRAP.md`
