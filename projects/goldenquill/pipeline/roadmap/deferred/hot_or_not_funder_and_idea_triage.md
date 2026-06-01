# Hot / Not / Hot-If Funder & Idea Triage — Deferred Feature

## Summary

Design a mobile-first, swipe-based interface that lets client teams quickly triage both **funding opportunities** and **program/idea concepts** using a simple scale:

- **HOT** — clear fit, green-light.
- **NOT** — clear no, drop to bottom of stack.
- **HOT… IF** — conditional fit that must carry a short note or voice/clip (e.g., "Hot if we get a fiscal sponsor", "Hot if Patrice wants to lead youth stipends").

Tilth records per-user votes and uses them to refine `org_program_fit` (for funders/programs) and idea rankings (for Scribe) from day one.

## Scope (future stage)

- Runs on **paired tablets/phones**; multiple team members can swipe on the same funder/idea.
- Backed by the normalized DB under `pipeline/db/` and the Population + discovery pipeline (Grants.gov, 990s, websites).
- Two rails:
  - **Funder rail:** triage funders/programs discovered via 990 + APIs + curated lists.
  - **Idea rail:** triage project/program ideas for specific opportunities.
- Votes stored per user (`user_id, org_id, program_id or idea_id, rating {HOT, NOT, HOT_IF}, comment, timestamp`).
- Org-level fit (`org_program_fit`) and idea selection are derived from a combination of votes + owner overrides.

## Rationale

- Replaces spreadsheet torture with a **fast, human-in-the-loop** review step.
- Forces all initial heuristics (Scout’s ratings) to go through explicit human agreement/disagreement clicks.
- Captures team preferences from day one, making future Scout/Scribe suggestions better tuned to the org.

## Dependencies / Notes

- Out of scope for v0.1 (no UI layer per locked decisions); belongs in a later Stage when UI is green-lit.
- Depends on:
  - Stable `pipeline/db/*` schema (funders/programs/calls/org_program_fit/applications).
  - A thin API or query layer to serve candidates to the UI.
  - A simple identity model for team members (user IDs) per org.
