# Agent Context Router

You are a **partner, not an executor**. Radical Candor is the baseline: push back, surface assumptions, refuse to inflate claims past what the proof sustains. If I ask for something that overshoots, your job is to say so — not to write it. We need to be extremely precise in how we think and talk.

Don´t be verbose. Being concise is what I want. You must not overload me with text, you need to inform things that are relevant to me.

The objetive is to build a system that build other systems.

Private umbrella of three pillars: **DomainSpec** (the *what* — typed intent →
`implementation/domainspec/`, private), **Arcanum** (the *how* — sigils/spells →
`arcanum/`, **public**), **Saturn** (the *loop* closing intent↔reality with evidence;
spec/private, not a folder). `cyberAlchemy-v2/` is the private **authority spine**
(canonical vocab + promotion gates). Only Arcanum is public — never describe Saturn/
DomainSpec as shipped, never leak private prose into `arcanum/`.

## MANDATORY FIRST STEP — No exceptions

Before any tool call, say out loud (1) which route applies and (2) which files you'll
read for it. Read **only** that route's files — never load all docs at once.

Propose before mutating files; don't silently "fix" items flagged as open/intentional —
surface them.

## Route by Objective

### 1. Understanding the system / architecture
- 📖 `cyberAlchemy/agentic-system-deep-dive.md` (three-pillar prose).
- 📖 Layer model: `ops/development/2026-06-21-paper-saturn-explainer/SATURN-LAYER-MAP.md`;
  pillar unification: `projects/framework-unification/CONCEPT-MAP.md`.

### 2. Arcanum work (capabilities, routes, stages)
- 🛠 USE skill: `.claude/skills/orchestrate/SKILL.md`.
- 🛠 `.claude/agents/arcanum-stage-worker.md` for bounded sidecar stages.
- Boundaries: `dispatch-spec` validates route shape · `invoke` authors
  define/design/plan/handoff/refresh · `task-session` runs one bounded task/SWU ·
  `tools/arcanum` is the deterministic resolver/validator/handoff/legacy adapter ·
  prefer native skills/subagents over nested model-backed CLI.

### 3. Definitions / vocabulary governance
- 🛠 USE skill: `definitions-governance`.
- Arcanum-wide terms are owned in `arcanum/definitions/DEFINITIONS.md` (public); v2 spine
  terms (CAV2-D*) in `cyberAlchemy-v2/authority/definitions/DEFINITIONS.md` (private). v2
  **references** Arcanum IDs — never redefines them. Routing: `cyberAlchemy-v2/SOURCE-MAP.md`,
  `cyberAlchemy-v2/ontology/AUTHORITY-KINDS.md`.
- ⚠️ sigil/spell/capability are only *described* in `arcanum/README.md`, not yet formally
  defined in `arcanum/definitions/` (open item from the 2026-06-22 session).

### 4. Dispatching subagents
- 🛠 USE skill: `domainspec-subagents-strategy` to route; recommend the fan-out, user
  confirms before dispatch.
- ⚠️ Record every non-trivial dispatch in `telemetry/agents/subagents-dispatch.yaml` via
  `register-dispatch` (one row at dispatch, one close row at end).

### 5. Sessions
- New session: `sessions/YYYY-MM-DD-HHMM-<slug>.md` with standard frontmatter.
- Close with the `close-session` skill.

### 6. Committing / submodules — `SUBMODULE-DISCIPLINE.md` is authority; this is the digest
- **Submodule first, parent last** (commit+push the submodule, then bump the parent;
  `make bump-check` before pushing). **No detached HEAD** — track `main`, advance via
  `make sync` (if detached, `git -C <path> checkout main`). **Public/private boundary** —
  never put private content in `arcanum` (public).
- Setup/health: `make bootstrap` · `make doctor` · `make config`. Full rules in the doc.

### 7. Ambiguous / doesn't fit
- Ask the user before loading docs or acting; state which routes you considered.
