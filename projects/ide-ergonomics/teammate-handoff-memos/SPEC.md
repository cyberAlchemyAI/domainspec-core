# SPEC - Teammate Handoff Memos

Status: draft strategy artifact; no runtime implementation
Date: 2026-06-23
Owner if pursued: IDE Ergonomics host-surface owner plus handoff/decision owners
Builds on: [README.md](README.md)

## 1. Problem

Agentic work often crosses teammate boundaries. A session discovers a result that
Vlad, Victor, Josh, Koichi, a future agent, or a role owner needs to consume later.
Today the repository can hold strong addressed memos, but the IDE does not make
them part of the ordinary start-work or handoff flow.

The result:

- addressed memos are easy to miss when starting work;
- session handoffs are mixed with narrative memos and resolution notes;
- the user has to manually remember who owns which open call;
- a memo can look resolved because it is well written, even when the human decision
  is still open;
- agents start working without first checking teammate-bound context.

## 2. Primitive

`teammate-handoff-memo` is a collaboration primitive with two linked surfaces:

1. `teammate_handoff_window` - an IDE panel or popup for addressed memos, session
   handoffs, discussion drafts, and resolutions.
2. `start_work_handoff_check` - a callable skill/check that runs when starting
   substantial work and asks whether addressed handoffs should be read first.

The unit is a memo artifact, not a chat message. The memo can target a person,
role, future session, agent lane, or owner route.

## 3. Source Pattern

Initial local pattern: `cyberAlchemy-v2/TO-VLAD/`.

Observed memo shapes:

| File | Shape | Useful pattern |
| --- | --- | --- |
| `TO-VLAD.md` | addressed argument memo | `to/from/re/date/status`, plain-language result, load-bearing findings, open questions, concrete edits, deliberate non-recommendations. |
| `SESSION-HANDOFF-cav2-primordial-basis.md` | next-session handoff | identity, new-session prompt, route rationale, context selection, excluded context, target boundary, gaps, gate result. |
| `TO-VLAD-residue-typing-in-generation.md` | discussion draft | practical procedure, honest boundary, proposed mechanism, worked example, caveats, "what I'd do". |
| `RESOLUTION.md` | resolution record | inputs, decisions, closed items, still open, validation notes. |

## 4. Memo Schema

```yaml
teammate_handoff_memo:
  memo_id: <stable-host-id-or-path>
  memo_type: incoming | outgoing | session-handoff | discussion-draft | resolution
  to:
    kind: person | role | future-session | agent-lane | owner-route
    label: <recipient>
  from:
    kind: person | agent | session | team | route
    label: <source>
  subject: <short subject>
  status: draft | open | flag | blocked | consumed | resolved | superseded
  created_at: <date-or-timestamp>
  source_path: <repo-relative-path>
  project_scope: <path-or-label>
  why_now: <one-sentence reason this memo matters>
  start_prompt: <optional next-session prompt>
  key_points:
    - <load-bearing finding or instruction>
  open_calls:
    - owner: <person|role|route>
      question: <decision or response needed>
      status: open | deferred | answered | blocked
  boundaries:
    - <what the memo does not authorize>
  next_actions:
    - <concrete action, route, or artifact>
  source_refs:
    - <path-or-selector>
  resolution_ref: <path-or-null>
```

## 5. Start-Work Check

The start-work check runs before substantial work when the active project has
addressed memos, open session handoffs, or unresolved partner calls.

Inputs:

- workspace root;
- active project path or inferred project;
- current user/role/agent lane if known;
- optional recipient filter such as `Vlad`, `Victor`, `owner`, or `future-session`.

Output:

```yaml
start_work_handoff_check:
  project_scope: <path-or-label>
  checked_paths:
    - <memo-folder>
  addressed_to_current_actor:
    - <memo_id>
  open_handoffs:
    - <memo_id>
  stale_or_superseded:
    - <memo_id>
  recommended_first_read: <memo_id-or-null>
  reason: <why this should or should not interrupt start-work>
```

The check is advisory. It may recommend reading a memo first, but the user can
defer it and continue.

## 6. Window States

| State | Meaning | UI behavior |
| --- | --- | --- |
| `empty` | No memos found for the current scope. | Show create-handoff action only. |
| `inbox` | Addressed or open memos exist. | List by recipient, project, status, freshness. |
| `memo-open` | One memo is selected. | Show summary, open calls, boundaries, next actions, source refs. |
| `drafting` | User is leaving a new memo. | Pre-fill recipient, reason, source refs, prompt, unresolved questions. |
| `replying` | User is responding to a memo. | Preserve memo context, require explicit answer vs defer. |
| `resolution` | A memo has been consumed into decisions/artifacts. | Draft resolution record with closed/open split and validation notes. |
| `superseded` | A newer memo or resolution replaces this memo. | Link to replacement and keep old memo read-only. |

## 7. Actions

| Action | Allowed effect | Boundary |
| --- | --- | --- |
| `open_memo` | Open the memo artifact. | No state change. |
| `start_from_prompt` | Use the memo's next-session prompt as current work context. | Does not auto-execute blocked steps. |
| `draft_handoff` | Create an outgoing memo draft. | Requires user review before treating it as a handoff. |
| `draft_reply` | Draft a response or clarification. | Must not impersonate the recipient. |
| `mark_consumed` | Record that the current session read and used the memo. | Does not mean decisions are resolved. |
| `create_resolution` | Draft a resolution artifact with decisions, closed items, still-open items, and validation notes. | Human-owned calls need explicit answers or remain open. |
| `add_to_context_pack` | Add the memo to a Context Builder candidate set. | Context pack is evidence selection, not authority. |
| `park_for_later` | Save the memo as a side node/reminder. | Does not switch active route. |

Disallowed effects:

- sending external messages without a separate explicit communication tool and
  confirmation;
- marking a human response as answered when no answer exists;
- changing canonical definitions, constitutions, ontology, or implementation from
  the memo window alone;
- hiding superseded, draft, flag, or blocked status;
- converting a teammate memo into a generic agent instruction without recipient
  and ownership context.

## 8. Draft Template

```markdown
---
to: <recipient>
from: <source>
re: <project or topic> - <short subject>
date: <YYYY-MM-DD>
status: draft
---

# To <recipient> - <subject>

## Why This Memo Exists

<one short reason>

## What Changed

- <load-bearing fact>

## What I Need From You

1. <owner-bound question or decision>

## Suggested Next Move

<route, prompt, artifact, or decision gate>

## Boundaries

- <what this memo does not authorize>

## Source Refs

- <path or selector>
```

## 9. Pass Conditions

A static proof over fixture memos passes when a reader can answer:

- who is the memo for?
- who or what produced it?
- what work scope it belongs to;
- whether it is draft, open, consumed, resolved, blocked, or superseded;
- what the recipient needs to decide or do;
- what the memo explicitly does not authorize;
- what prompt or route should start the next work session;
- whether a resolution exists and what remains open.

The proof fails if:

- a memo window makes draft text look like an owner decision;
- the system starts work without surfacing a relevant addressed memo;
- a reply is written as if it came from the human recipient;
- the handoff hides blocked decisions or superseded status;
- a teammate memo is reduced to an unowned task list.
