---
scope: pipeline-wide
purpose: define session efficiency metrics schema and logging discipline
created: 2026-04-19
---

# Session Metrics Specification

Lightweight self-monitoring for session efficiency. No bureaucracy — just structured visibility so the system gets leaner over time.

## Storage

- **Log file:** `pipeline/metrics/session_log.jsonl` (append-only, one JSON object per line)
- **Format:** JSON Lines — each session appends exactly one line on close
- **Retention:** indefinite. The efficiency audit agent reads this file for pattern detection.

## JSON Schema

Each session close entry conforms to this schema:

```json
{
  "session_id": "string — ISO 8601 timestamp of session start (YYYY-MM-DDTHH:MM:SS)",
  "date": "string — YYYY-MM-DD",
  "agent": "string — which agent/seat (e.g., 'cowork', 'scout', 'scribe', 'dispatch')",
  "org": "string|null — org folder name if Law 3 scoped, null otherwise",
  "turns": "integer — total turn count (user + agent exchanges)",
  "estimated_wall_minutes": "integer — rough wall-clock estimate in minutes",
  "questions_asked": "integer — total clarifying questions sent to operator",
  "questions_batched": "integer — questions sent in batched messages (multiple Qs per message)",
  "questions_sequential": "integer — questions sent one-at-a-time (inefficient pattern)",
  "files_read": "integer — distinct files read during session",
  "files_written": "integer — distinct files created or edited during session",
  "template_references": "integer — times a shared template was referenced instead of restating framework",
  "inline_repeats": "integer — times framework/boilerplate was restated inline (should be 0)",
  "handoff_lines": "integer|null — line count of any handoff prompt produced (null if no handoff)",
  "self_check_failures": ["string — list of failed self-check items, empty if all passed"],
  "notes": "string|null — optional free-text for unusual session context"
}
```

### Field Rules

- **turns**: count every user→agent and agent→user exchange as one turn. Tool calls within a single agent response do not increment.
- **estimated_wall_minutes**: best estimate. Precision is not critical — order of magnitude matters for pattern detection.
- **questions_batched vs sequential**: a message containing 3 questions counts as 1 batched, 0 sequential. Three separate single-question messages count as 0 batched, 3 sequential.
- **template_references**: increment when citing `pipeline/templates/component_analysis_template.md`, `pipeline/SESSION_BOOTSTRAP.md`, or any other shared template by path instead of restating its content.
- **inline_repeats**: increment when the Five Laws, Four Rules, product naming chain, or other shared framework is restated verbatim instead of referenced. Target: 0.
- **handoff_lines**: if a handoff prompt is produced, count its lines. Threshold: 50 lines max (excluding the bootstrap reference line). Over 50 = self-check failure.
- **self_check_failures**: populated from the Session Close Self-Check in `CLAUDE.md`. Empty array = clean session.

## Closing Discipline

Every session — Cowork, OpenClaw agent, or any Tilth seat — writes its metrics entry as its **last act before signing off**. This is mandatory, not optional.

### Procedure

1. Run the Session Close Self-Check (defined in `CLAUDE.md`).
2. Collect metrics values from session state.
3. Populate any failed self-check items into `self_check_failures`.
4. Append one JSON line to `pipeline/metrics/session_log.jsonl`.
5. Sign off.

### Exceptions

- Sessions that crash or are force-killed obviously cannot log. The efficiency audit agent detects gaps by comparing daily_log entries against session_log entries.
- Sessions under 3 turns (quick lookups, single-question answers) may skip metrics if no files were read/written and no handoff was produced. Use judgment — if it was trivial, don't log it.

## Cross-References

- Session Close Self-Check: `CLAUDE.md` → "Session Close Self-Check" section
- Efficiency audit agent: `pipeline/templates/efficiency_audit_agent.md`
- Session efficiency rules: `CLAUDE.md` → "Session Efficiency" section
- Agent closing discipline: `AGENTS.md` → "Session Close" section
