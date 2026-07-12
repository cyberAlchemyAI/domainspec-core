---
id: ide-extension-session-content-canvas-decisions
project: ide-extension
title: "Session Content Workbench Decision Ledger"
status: accepted
node_type: decision-record
updatedAt: 2026-07-12
decision_gate_result: pass
---

# Decision Ledger: Session Content Workbench

## Approved Core Intent

V0 is a trusted-local value experiment. A Codex session can create or select an
HTML file in the project, publish it to the local workbench, and receive user
interaction events from that HTML surface.

The target is not a document viewer. It is an agent-created work surface. The
first representative uses are:

- a generated HTML presentation;
- an interactive decision gate whose answer returns to the session;
- a Craft task surface whose requested action returns to the session.

V0 does not attempt to prove arbitrary HTML safety, hostile-session isolation,
remote multi-user operation, or publication security. Those are promotion
concerns after the value loop is witnessed.

## DG-SCC-001: Browser Update Policy

**Question:** How should the already-open browser learn that session content is
available?

- Selection: **Manual Refresh for the first transport witness, followed
  immediately by automatic update.**
- Source: operator answer, "manual but right after validating it we should test
  automatic too", 2026-07-12.
- Automatic update means a kernel-owned state-change notification followed by
  browser fetch/reload. It does not mean sending partial HTML tokens.
- A complete saved revision is the unit of display so the browser does not load
  a half-written file.

## DG-SCC-002: Content Representation

**Question:** What content format should V0 admit?

- Selection: **Trusted local HTML artifact.**
- Source: operator clarification that the end product is asking the agent to
  create a presentation and stream it to the local workbench, followed by the
  instruction to prioritize value over V0 security hardening, 2026-07-12.
- The session writes or selects a real `.html` file under an approved project
  root and publishes a file reference, not the full HTML body in a result field.
- The local server resolves and serves the file; the workbench loads it as an
  interactive HTML surface.
- Inline JavaScript, CSS, forms, links, and normal HTML interaction are allowed
  in this trusted-local experiment.
- Existing project HTML, including a presentation already on disk, is a valid
  input to the same path.

Markdown, structured blocks, sanitization, CSP hardening, and external-resource
policy are deferred. V0 must not claim those controls exist.

## DG-SCC-003: Session Coupling

**Question:** How does a session publish surfaces and receive interactions?

The earlier atomic-terminal-result recommendation is withdrawn because it
cannot support a decision gate or task surface while the session is active.

Recommended V0 contract:

1. The session writes a complete HTML revision to the project.
2. The session calls a separate `canvas publish` operation with its path and
   optional title/kind metadata.
3. The kernel records the current canvas revision and notifies the workbench.
4. The workbench loads or reloads that revision.
5. HTML interactions emit small typed events through the workbench to the
   kernel.
6. The session retrieves those events through manual polling first.

- Selection: **Separate active-session `canvas publish` and `canvas events`
  polling operations.**
- Source: operator confirmation, "yes", 2026-07-12, in response to the explicit
  publish/poll contract question.
- Rationale: presentation display needs publication before terminal completion,
  while Decision Gate and Craft surfaces need user interactions to return while
  the session can still continue its work.

## V0 Boundaries

- Trusted local operator, trusted local session, loopback server.
- HTML remains a real workspace artifact and is not copied into the bridge log.
- A published revision must be complete before the workbench loads it.
- Interaction events carry a surface id, revision id, event name, and JSON
  payload.
- A browser click is an interaction request, not proof that a Craft task or
  other effect completed.
- The workbench may use an iframe for layout/lifecycle isolation, but V0 makes no
  hostile-content security claim.
- No remote access, marketplace execution, arbitrary third-party sessions, or
  production security claims.

## Gate Result

- Result: `PASS`.
- Decisions resolved: DG-SCC-001, DG-SCC-002, and DG-SCC-003.
- Blockers remaining: none.
- Current bundle: trusted local HTML artifact + complete-revision publish +
  workbench display + typed interaction event + manual session poll.
- Next route: `invoke refresh`, then `invoke plan` around the three value
  witnesses.
