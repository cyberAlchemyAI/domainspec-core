---
tags: [ide, ergonomics, handoff, teammate, communication, agent-human-partnership]
node_type: feature
layer: product, workflow, collaboration
nature: design-seed
status: strategy-proposal
created: 2026-06-23
---

# Teammate Handoff Memos

An IDE-side ergonomic primitive for agent + human partnership between teammates:
the system can open, draft, and resume role-bound communication handoffs in the
style of the local `TO-VLAD` memos.

The current IDE Ergonomics project already routes workflow moments to Arcanum
owners. This primitive adds the human collaboration layer: when work crosses from
one teammate, session, role, or agent lane to another, the IDE should surface a
memo-like handoff window that preserves context, open questions, boundaries,
proposed next steps, and resolution status.

## Why it belongs here

The repository already has teammate handoff examples under
[`cyberAlchemy-v2/TO-VLAD/`](../../../cyberAlchemy-v2/TO-VLAD/). They are not generic
summaries. They are addressed memos with a clear recipient, source, status,
argument, next-session prompt, open calls, concrete edits, and later resolution.

The ergonomic gap is that the user still has to remember to open or write these
memos at the right time. The IDE can help by offering:

- a teammate handoff window beside the active session;
- a start-work check that asks whether there are addressed memos to read first;
- a draft action when the current work should be handed to a human teammate,
  future agent, or role owner;
- a resolution action when a memo has been consumed and converted into decisions,
  artifacts, or blocked residue.

## User Experience

At the start of work, the IDE or skill runs a small partnership check:

```text
Start-work handoff check
Project: cyberAlchemy-v2
Recipient: Vlad

Open addressed memos:
- TO-VLAD.md - resolved locally by RESOLUTION.md
- SESSION-HANDOFF-cav2-primordial-basis.md - flag, safe to open new thread
- TO-VLAD-residue-typing-in-generation.md - draft for discussion
```

Opening one memo shows a compact window:

```text
To Vlad - typing residue, and automating it during generation
Status: draft for discussion
Why now: residue type blocks the ledger and code-generation route
Open calls: schema facet location, generator instrumentation, register field
Actions: Open memo, Start from prompt, Draft reply, Mark consumed, Create resolution
```

During work, the same window can be invoked when a route reaches a natural split:

```text
Create teammate handoff
To: <person or role>
From: <agent/session/team>
Reason: decision, implementation handoff, research finding, blocker, resolution
Include: source refs, next-session prompt, open questions, boundaries, proof
```

## Owner-Safe Route

```text
active work or start-work check
  -> addressed memo scan
  -> teammate handoff window
  -> user chooses read, draft, reply, resolve, or defer
  -> memo artifact or resolution draft
  -> owner decision remains explicit
```

The memo can guide a teammate or agent, but it does not become a decision merely by
existing. Human-owned calls stay open until the owner answers or a governed
decision route records the result.

## Memo Types

- `incoming` - a memo addressed to the current user, role, or agent lane.
- `outgoing` - a memo the current session should leave for someone else.
- `session-handoff` - a next-session starter with prompt, context selection, gaps,
  and gate result.
- `discussion-draft` - a memo that frames an argument or open call before a
  decision.
- `resolution` - a follow-up artifact that records what was accepted, rejected,
  changed, and still open.

## Surfaces

The primitive may appear as:

- an IDE window beside chat and files;
- a command palette action such as `Open teammate handoffs`;
- a start-work skill/check called before substantial work begins;
- an action card when a route reaches a handoff boundary;
- a companion to the evidence rail, showing which memos were consumed or produced.

## Files

- [SPEC.md](SPEC.md) - memo schema, window states, start-work hook, actions, and
  pass conditions.

## Boundaries

- Strategy proposal only; no IDE extension or skill runtime is built here.
- The primitive may draft or surface memos, but it does not send messages outside
  the repository.
- The primitive must not impersonate a human teammate.
- A memo can request, recommend, or preserve a decision; it cannot close a
  human-owned decision without an explicit owner response or governed decision
  record.
