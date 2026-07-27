# Tester Brief — read before you test

Thank you for testing UI Prototyping Studio. This is the safety and consent
boundary for the guided local protocol in [TEST-PROTOCOL.md](TEST-PROTOCOL.md).

## What you are testing

You are testing a **governance and control loop**: can an authorized actor
understand what is current, inspect a proposed UI change, acknowledge the exact
Accept/Revert context, preserve an append-only history, and distinguish export
confirmation from readiness?

The locally implemented surface includes:

- current-head preview and labeled history;
- click-to-annotate on actual `data-od-id` targets;
- staged before/after evidence;
- browser Accept/Revert with live action-context acknowledgment; and
- terminal-confirmed handoff export.

The protocol is not a release trial and is not evidence that the styling,
accessibility, or human ergonomics are production-ready.

## The authority caveat

The Studio does not infer a human-vs-agent identity from a CLI or browser
caller. Its core enforces state, scope, staleness, exact candidate/revision
identity, and the required acknowledgment, but caller identity alone grants no
authority.

In particular:

- Browser Accept/Revert stays disabled until the exact live action context is
  acknowledged; the server also rejects missing acknowledgment and stale
  candidate/revision or target state.
- That acknowledgment records inspection intent. It does not prove who clicked
  or authorize an otherwise unauthorized route.
- Direct CLI operations remain governed by the route/operator context; the core
  does not manufacture a human-vs-agent identity gate.
- Handoff export requires explicit confirmation in the core, but confirmation
  does not set evidence, integration, implementation, or release readiness.

For this supervised protocol, you should know which actor or route is issuing
each durable command. If a revision is recorded outside the route you intended
to authorize, stop and report it.

## Why the local trial is bounded

- Admission rejects required out-of-scope or stale candidates.
- A staged candidate is not head until accepted.
- Accept and Revert bind current identity/state and append history.
- Everything runs locally under a fresh `STUDIO_DATA` directory.
- Handoff output contains explicit missing-reference and readiness fields.

These controls support a bounded trial. They are not a substitute for a bound
human-study owner, accessibility audit, or release owner.

## Ground rules

- Use a fresh `STUDIO_DATA` file inside a fresh directory per run.
- Keep the preview on its printed loopback address.
- Know which authorized route is driving durable operations.
- Treat confusion, unexpected state, or a revision you did not intend as a
  finding.
- Do not interpret a passing local run or `implementationReady: true` as
  release authorization.

Ready? Continue with [TEST-PROTOCOL.md](TEST-PROTOCOL.md).
