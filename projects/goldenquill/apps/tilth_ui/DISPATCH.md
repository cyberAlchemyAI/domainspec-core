# Dispatch Prompt: Claude Code vs Cowork

A reusable router for deciding which Claude surface to throw a task at, with a copy-paste prompt template at the bottom.

## The split, at a glance

| | Claude Code (CLI) | Cowork (this desktop app) |
|---|---|---|
| **Lives where** | A terminal sitting inside the repo. | The Claude desktop app, with access to a folder you pick and a sandboxed Linux shell. |
| **Sees** | The whole repo as filesystem + git. | The selected folder + the open browser + open native apps (with permission). |
| **Touches** | Files in the repo. Runs scripts. Reads git history. | Files in the selected folder, runs shell commands in a sandbox, drives Chrome, controls native apps (with permission), uses connected MCPs (Gmail, Calendar, etc.). |
| **Best at** | Long, structured code work where the answer is in the codebase. | Cross-app work: web research, browser automation, native-app workflows, file deliverables, audit reports informed by external context. |
| **Worst at** | Anything that requires looking outside the repo, browsing live, or producing rich deliverables for non-developers. | Long focused code work on a large repo (it can do it but it's slower and the context is per-session). |

## Decision rules

Use this order. Stop at the first match.

1. **Is the task "modify the codebase, then verify with the repo's own tests"?** → **Claude Code.** It has the whole repo, git, and shell at native speed.
2. **Is the task "tell me what's happening on the live UI / live data / live web right now"?** → **Cowork.** Code can't drive a browser, can't open Slack, can't read your Gmail.
3. **Does the answer require both code analysis AND external context (live UI, web docs, a connector)?** → **Cowork drives, Code executes.** Cowork does the research and produces the spec; you paste the spec into Code for the implementation. (See "Hand-off pattern" below.)
4. **Is the deliverable a code change?** → **Code.** Even if Cowork could write the patch, Code is closer to the test loop and the diff is review-ready.
5. **Is the deliverable a document, report, screenshot set, slide deck, or anything a non-developer will consume?** → **Cowork.** It has the document skills and the file-presentation tooling.
6. **Is it a one-off shell command on the repo (rename file, run a script, check git log)?** → **Whichever you have open.** Both can do it; don't switch tools for a one-liner.
7. **Are you spending more than 30 seconds reading the response in the wrong surface to decide whether to switch?** → **You should have switched. Switch now.**

## Examples

| Task | Tool | Why |
|---|---|---|
| "Fix the stale signOff checklist" | Code | Pure repo change with a test loop. |
| "Audit the UI for click-through bugs" | Cowork | Needs the browser. |
| "Reconcile this Codex audit against what I see live" | Cowork | Needs to drive the browser and produce a report. |
| "Refactor app.mjs into modular files" | Code | Long structured edit; git diff is the artifact. |
| "Make a PDF summary of the audit for the funder" | Cowork | Document deliverable. |
| "Find which routes use `data.judge` unsafely" | Either, but lean Code | Pure repo grep; Code is faster on a fresh start. |
| "Should we drop the Stitch shell or keep it?" | Cowork | Needs to compare live behavior + read multiple files + produce a recommendation. |
| "Add a `:focus-visible` rule and verify with `verify-static.mjs`" | Code | Edit + run test. |
| "Take screenshots of every route at three viewports" | Cowork | Needs a browser. |
| "What's the WCAG ratio on this color pair?" | Either | Trivial; whichever is open. |

## Hand-off pattern (when both are needed)

The right flow when a task spans both surfaces:

1. **Cowork investigates and writes a spec.** Produces a markdown file in the repo describing the problem, the evidence (screenshots, file paths, line numbers), and the proposed change.
2. **Code implements the spec.** Reads the markdown, makes the edits, runs tests, commits.
3. **Cowork verifies the live result.** Reloads the browser, screenshots the fixed state, updates the spec or files a follow-up.

Avoid the inverse (Code writes a spec for Cowork to implement) — Cowork's edit-then-verify loop is slower for code than Code's.

## Anti-patterns

- **Asking Code to interpret a screenshot of a browser bug.** Code can't see the screen. Either paste the rendered HTML or the visible text, or do it in Cowork.
- **Asking Cowork to refactor a 1,000-line file.** It works but takes more turns; Code is better suited.
- **Running the same long audit in both surfaces.** Pick one. If you want a second opinion, run the audit once, hand the report to the other tool, and ask it to challenge specific claims — not to redo the audit.
- **Switching mid-task without telling either surface.** If you move work from Cowork to Code, paste the relevant Cowork outputs (filenames, findings, decisions) into the Code session so it starts with context.

## Copy-paste router prompt

Use this when you have a task and you're not sure where to send it. Paste it into whichever surface you have open; it will tell you to stay or switch.

```
ROUTER MODE — decide whether this task belongs in Claude Code or Cowork.

Task: <one or two sentences describing what you want done>

Apply these rules in order and stop at the first match:
1. If the task is "modify the codebase, then verify with the repo's tests" → Code.
2. If the task requires reading the live browser / live data / web docs / connected MCPs → Cowork.
3. If both are needed: Cowork investigates + writes a spec, Code implements.
4. If the deliverable is a code change → Code.
5. If the deliverable is a document, slide deck, PDF, screenshot set, audit report → Cowork.
6. If it's a one-off shell command on the repo → whichever is open.

Output:
- TOOL: <Code | Cowork | Cowork→Code | Code→Cowork>
- ONE-LINE REASON: <which rule fired>
- IF YOU NEED ME TO SWITCH: <exact first prompt to paste into the other surface, including any context the other surface won't have>
- IF YOU STAY HERE: <the first step I should take>
```

## Notes on this specific project (Tilth UI)

Based on the audit so far, here's the mapping for the work in flight:

- **Patching `app.mjs` bugs** (sign-off checklist, focus-visible, badge fall-through, primary-nav always-active) → **Code.** Discrete file edits with a test loop.
- **The 178-directory spec-library consolidation** → **Cowork** to decide which to keep, **Code** to actually move/delete files.
- **Picking the canonical UI path (integrated renderer vs. component app vs. Stitch shell)** → **Cowork.** This is a product decision informed by code, browser, and posture. Then handoff to Code for execution.
- **Sovereignty fix on Stitch CDN loads** → **Code.** Replace CDN refs with local assets, verify with a no-network test.
- **Producing the human-readable QA report and findings JSON** → **Cowork.** Document deliverables.
