---
id: refine-seed-ui-ux-interaction-skill
project: ui-prototyping-studio
title: "Refine Seed — UI/UX Interaction Surface + Operating Skill"
status: seed
node_type: refine-seed
run_id: 20260616-ui-ux-interaction-skill
updatedAt: 2026-06-16
---

# Refine Seed — UI/UX Interaction Surface + Operating Skill

## Target

Divert focus to the **UI/UX side**: design (and author) the two pieces that turn the studio from a
governance backend into a *usable agentic tool* —
1. the **operating `SKILL.md`** — the contract that makes Claude Code the engine (who-leads-when,
   the discipline: generate → `variants register` → stamp `data-od-id` → never self-approve/apply →
   hand the gates to the human), and
2. the **interface of interaction** — the `studio preview --annotate` overlay + the human-agent
   review/gate loop: how a human *sees* variants, *clicks to annotate* directly on components, and
   *disposes* at the gates, with Claude Code proposing.

**Ergonomics is the first principle:** every interaction decision must state who-leads-when,
the cognitive load it imposes, and how it reduces friction (human-agent symbiosis).

## Source context (local-first)

- `SPEC.md` §interaction model + `AC-L0-11/12`; `interfaces.md` (the `studio` CLI + preview `--annotate`).
- Decisions: `DEC-RUNTIME-CLAUDE-CODE-011`, `DEC-CLI-NOT-MCP-012`, `DEC-INPROTO-ANNOTATION-013`,
  `DEC-ATOMIC-IDS-014`; the ergonomics charter in `development/deep-spec-dispatch/CONTEXT-PACK.md`.
- Evidence: `development/deep-spec-dispatch/COLD-START-USABILITY-FINDINGS.md` (the naive-user friction)
  + `UX-EVIDENCE-REPORT.md` (validator-safe UX checks) — the ux-evidence-validator basis.
- The built, runnable `backend/src/cli/studio.ts` (X2) — the surface the human/agent already drive.
- Carried gap: `GAP-ERGONOMICS-UNPROVEN-001` (the first principle is still unmeasured).

## Candidate interaction surfaces (to compare)

- **A — browser preview overlay** (`studio preview --annotate`): render the HTML, inject a
  click-to-annotate overlay, ephemeral local server posts comments back. (The current design.)
- **B — terminal/TUI review**: review + gate entirely in the terminal alongside the CLI.
- **C — minimal local web review page**: a thin served page listing variants + a gate panel.

## What this run must produce

- An authored **operating `SKILL.md`** (the Claude-Code operating contract) — as the design artifact.
- An **interaction-interface design**: the chosen surface, the overlay mechanics (capture
  `data-od-id`, ephemeral server, POST→`CaptureCommentEvent`), and the **human-agent loop** with an
  ergonomics rationale per step (who-leads-when / cognitive load / friction).
- A **non-executed build plan** for the overlay + skill install.
- Each design claim classified against the **ux-evidence-validator** model (hard-gate / soft-flag /
  screenshot-review / human-study), never asserted.

## Run parameters

- **Preset:** `full`.
- **Research:** `research-if-gap-appears` (local-first; one bounded external pass only if a named gap
  appears — e.g. prior art on agentic-tool interaction patterns or click-to-annotate overlays).
- **Write scope:** this run folder; on synthesis, *proposed* `SKILL.md` + interaction design + plan
  (proposals — authoring the live `SKILL.md` is the recommended next route).
- **Validation surface:** the toy-game dual walkthrough (a cold-start naive user AND a Claude Code
  session), the ux-evidence classification, and the ergonomics-charter clauses.

## Planned stage configuration (canonical 10-stage loop)

Context → Define **[x-ray the interaction flow]** → refine-review → research decision → Distill
**[tournament: A vs B vs C]** → Design **[dialectic: agent-autonomy vs human-control / friction vs
accountability]** (authors the SKILL + interaction design) → design-review → Distill Repair
**[toy-game: naive-user + Claude-Code dual walkthrough]** → Plan → Final synthesis. Subagents
**recommended** (interaction-designer + skill-author + ergonomics-critic + naive-user + synthesis).
