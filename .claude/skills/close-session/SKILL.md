---
name: close-session
description: Close a session and create a vault conversation node
---

# Close Session Workflow

> **Save location:** session nodes live at `sessions/YYYY-MM-DD-HHMM-{slug}.md` at the repo root.
> Classification guidance is self-contained in this skill (see Step 2) — no external files to load and no edge-graph machinery.

---

## Step 0 — Triage

**Create a node if any is true:** spec/doc changed/created/deleted, domain code changed, architectural decision made, tests added/modified, contradiction found/resolved.

**Skip if:** no doc/code changes AND purely Q&A with no decisions. Say *"Q&A-only session. No vault node created."* and stop.

**Scratchpad (optional):** Check `/Users/victorboscaro/.claude/current_conversations/` for a session file. If found, use it as primary input and delete it after saving the node. If absent, proceed from the live conversation context.

---

## Step 1 — Write Summary, Next Steps, Open Questions (do this yourself)

You hold the session context — write all three yourself; do **not** delegate them to the classifier (Step 2 does classification only).

- **Summary** — **2–4 sentences**: what the session set out to do, what was decided (and why), what was done. No sub-headings, no per-file detail. A reader should grasp the arc without access to the conversation.
- **Next Steps (recommendation)** — **1–5 bullets, priority-ordered**: the concrete recommended next actions, each a pointer (*what* + *where* — a file, command, skill, or decision owed). This is a recommendation, not a backlog dump — only steps that genuinely follow from this session. If none, write `- None.`
- **Open Questions** — the questions this session **raised but did not settle**, one line each, pointing at the artifact that would answer each where possible. Forward-only: a later session may resolve them. If none, write `- None.`

Keep all three pointer-style and tight — they live under the body cap.

---

## Step 2 — Classify (self-contained)

Classification is self-contained in this skill. You may do it inline, or **optionally** delegate to a Sonnet subagent (Agent, model: sonnet) briefed with your summary + the list of files touched **and the field schema below** — the subagent has no external source-of-truth files to load, so it must be given the schema in its brief.

Produce values for every frontmatter field. The schema and observed allowed values:

| Field | Meaning / guidance | Observed values |
| --- | --- | --- |
| `tags` | Topical tags, lowercase, list form. | e.g. `[ontology, architecture]`, `[ontologize, ontology, assessment, deliverable, engine, consulting]` |
| `node_type` | Kind of node. First match wins on priority order: constitution → premise → conceptual → test → discovery → implementation-plan → audit → spec (fallback). | e.g. `discovery` |
| `is_session` | Always `true` for a session node. | `true` |
| `layer` | Which layer(s) the work touched. Comma-separated string. | e.g. `domain, market`, `ontology, architecture` |
| `nature` | Character of the work. Comma-separated string. | e.g. `procedural, technical`, `explanatory, reference` |
| `status` | Lifecycle state. | `active` |
| `created` | Date the node was created. | `YYYY-MM-DD` |
| `timestamp` | Full local timestamp with offset. | `YYYY-MM-DDTHH:MM:SS±HH:MM` |
| `expires` | `created` + 60 days. | `YYYY-MM-DD` |
| `conversation_id` | Stable id for the conversation, usually `{date}-{slug}`. | e.g. `2026-06-08-ontologize-ontology-hardening` |
| `decisions_made` | Were load-bearing decisions made? | `true` / `false` |
| `contradictions_found` | Was a prior node validated/contradicted/questioned? | `true` / `false` |
| `specs_updated` | List of spec/doc paths updated, or `[]`. | list of paths |
| `promoted_candidates` | Nodes promoted to canonical this session, or `[]`. | list or `[]` |
| `expected_importance` | Integer `0–10` estimate of lasting importance. | e.g. `7` |
| `importance_rationale` | One sentence justifying the importance score. | quoted sentence |

Classifier output (inline or from the subagent) must include:

1. **node_type** — first match wins per the priority order above.
2. **tags, layer, nature** — per the schema and observed values above.
3. **expected_importance** (0–10) + **importance_rationale** (one sentence).
4. **Contradictions** — only if a prior node was validated, contradicted, or questioned. One short prose bullet per finding (e.g. "validates `path/to/node.md` — reason"). Omit section if none.
5. **Files touched** — flat list of paths, no descriptions. Git has the detail.

---

## Step 3 — Assemble the node

File: `sessions/YYYY-MM-DD-HHMM-{short-slug}.md` (at the repo root).

```markdown
---
tags: [{tag1}, {tag2}]
node_type: {type}
is_session: true
layer: {layer}
nature: {nature}
status: active
created: YYYY-MM-DD
timestamp: YYYY-MM-DDTHH:MM:SS±HH:MM
expires: {created + 60 days}
conversation_id: {id}
decisions_made: true | false
contradictions_found: true | false
specs_updated: [paths or []]
promoted_candidates: [nodes or []]
expected_importance: {0-10}
importance_rationale: "{sentence}"
---

# {Title}

## Summary

{2–4 sentences from Step 1}

## Contradictions

{Omit if none. One bullet per finding: "validates/contradicts/questions {node} — reason."}

## Next Steps

{1–5 priority-ordered bullets from Step 1, each a what+where pointer. "- None." if none.}

## Open Questions

{Questions raised but not settled, one line each, pointing at the resolving artifact where possible. "- None." if none.}

## Files touched

{Flat bullet list of paths. No table, no descriptions.}
```

> **Hard cap:** The body (everything below the frontmatter) must not exceed **40 lines**. Next Steps and Open Questions stay pointer-style — if the body runs over, you are writing too much; cut.

The node body ends at `## Files touched`. Save the file and the session is closed.
