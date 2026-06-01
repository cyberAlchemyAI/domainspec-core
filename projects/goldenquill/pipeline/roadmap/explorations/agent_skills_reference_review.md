# Reference Review — addyosmani/agent-skills

**Reviewed:** 2026-05-06
**Repo:** github.com/addyosmani/agent-skills
**License:** MIT
**Author:** Addy Osmani (ex-Google, web performance, Software Engineering at Google contributor)
**Reviewer:** Josh (operator review, post-v0.1 PASS)

---

## What was reviewed

A production-grade engineering-discipline skills pack for AI coding agents. 20 skills, 7 slash commands mapping to development lifecycle (spec / plan / build / test / review / code-simplify / ship), 3 specialist agent personas (code-reviewer, test-engineer, security-auditor), 4 reference checklists (testing, security, performance, accessibility). Skills follow a uniform anatomy: frontmatter, overview, when-to-use, process, rationalizations, red flags, verification.

Reviewed for design patterns transferable to Tilth, not for code reuse. Tilth is to grant-writing what agent-skills is to engineering.

## Strategic observation

This repo's existence is signal that Tilth's design philosophy is on solid ground. Same DNA: process-not-prose, anti-rationalization, verification non-negotiable. Worth saying explicitly when pitching Tilth to outside audiences (CDFIs, foundations, funders) — Addy Osmani built this for engineering; Tilth is the analog for grant-writing in regenerative agriculture and adjacent sectors.

## Four high-leverage pulls

### 1. Anti-rationalization tables

**Source pattern:** Every skill embeds a structured table of excuses agents use to skip steps, paired with documented counter-arguments. ("I'll add tests later" → rebuttal explaining why later means never.)

**Tilth adaptation:** Add an anti-rationalization table to every Tilth skill (scout-discovery, scribe-ghostwriter, judge-rubric, editor, logician, council-pipeline). Also add to admin-risk register entries (per-term rationalization for why an operator might want to use a flagged term, with the counter-argument). Also adopt the format in `lessons.md` entries — each lesson includes the rationalizations that lead to its violation.

**Doctrinal connection:** Maps directly to FWHP "I do not know" discipline — anti-rationalization is the structural opposite of confident-but-wrong. The pattern *enforces* honest acknowledgment of when a step is being skipped.

**Priority:** v0.2 — retrofit existing skills.

### 2. "Red Flags" sections in skills

**Source pattern:** Skills include a "Red Flags" section listing pre-defined stop-signals: "If you observe X, stop and reassess." Predictive, not reactive.

**Tilth adaptation:** `lessons.md` is Tilth's closest equivalent but it's reactive — lessons accumulate after failures. Red Flags are predictive, baked into skill design at the moment the skill is authored. Add Red Flags sections to every Tilth skill, populated initially from existing `lessons.md` entries and updated as new patterns emerge.

**Priority:** v0.2 — retrofit existing skills.

### 3. `source-driven-development` skill

**Source pattern:** Verbatim from the README: "ground every framework decision in official documentation — verify, cite sources, flag what's unverified."

**Tilth adaptation:** That is Law 1 (RFA is truth) generalized to engineering. The pattern's existence in another mature project validates Tilth's design — the same discipline applied to a different domain. Worth structurally inheriting for non-grant Tilth contexts (infrastructure decisions, architecture changes, library selection). When Tilth's engineering team makes a choice ("use Pydantic AI"), the choice traces to official documentation, not folklore.

**Priority:** v0.2 — formalize as engineering-process addition.

### 4. `git-workflow-and-versioning` skill

**Source pattern:** Trunk-based development, atomic commits, change sizing (~100 lines per commit), commit-as-save-point pattern, no long-lived branches.

**Tilth adaptation:** Immediately applicable to the GitHub repo init. Concrete decisions for the first commit and going forward:
- Trunk-based: `main` branch only; tags for milestones (v0.1.0, v0.2.0).
- Atomic commits: one logical change per commit.
- Commit sizing: ~100 lines per commit where feasible.
- Commit-as-save-point: every commit is a recoverable state.

**Priority:** Immediately applicable. Apply at repo init.

## Worth borrowing eventually (queued, not v0.2)

### `code-review-and-quality` — severity labels and change sizing

Severity labels (Nit / Optional / FYI) and change-sizing rules (~100 lines per review with splitting strategies) — could integrate into CTC (Code Thesis Committee) review verdict format. Current SFR format has verdicts but not severity granularity.

### `documentation-and-adrs` — ADR pattern

Architecture Decision Records as a formal pattern. Tilth's `pipeline/architecture/v0.1/` audit trails are functionally similar but less formalized. Promoting major decisions to formal ADRs would clarify the historical record — ADR-001 candidate: "v0.1 substrate locked at Pydantic AI + Logfire + OpenClaw curated + Ollama/vLLM + DSPy/GEPA" (note: LangGraph removed per session 2026-05-06 correction; CLAUDE.md still references it and needs update).

### `debugging-and-error-recovery` — five-step triage

Reproduce, localize, reduce, fix, guard. Stop-the-line rule. Pairs naturally with FWHP's "stop and verify" doctrine. Worth formalizing as Tilth engineering-process discipline.

### `code-simplification` — Chesterton's Fence + Rule of 500

Useful as Tilth grows. The Rule of 500 (a function over 500 lines is suspect) is a clean heuristic.

## Skip — not relevant to Tilth

| Skill | Why skip |
|---|---|
| `frontend-ui-engineering` | v0.1 is headless. No UI until Stage 2+. |
| `browser-testing-with-devtools` | N/A — no browser surface. |
| `performance-optimization` | Premature for v0.1. Address when telemetry shows actual hotspots. |
| `api-and-interface-design` (as standalone skill) | Tilth's seat interfaces are internal Python protocols. Pattern is useful; the skill as standalone isn't. |
| `shipping-and-launch` | Stage 2+ when Tilth ships beyond Josh. |
| `ci-cd-and-automation` | Premature — Tilth has no CI yet. Revisit when there is. |
| `deprecation-and-migration` | Useful concepts (code-as-liability) but the skill is engineering-CI-flavored. Apply principles, not skill structure. |

## Skip — namespace collision with Tilth process

| Skill / artifact | Tilth equivalent |
|---|---|
| 7 slash commands (`/spec`, `/plan`, `/build`, `/test`, `/review`, `/ship`, `/code-simplify`) | Tilth engineering process E1-E7 phases |
| 3 personas (code-reviewer, test-engineer, security-auditor) | CTC five-seat is more rigorous (cross-family L-003) |

## Roadmap placement

| Pull | Stage | Effort |
|---|---|---|
| Anti-rationalization tables retrofit | v0.2 | Medium — touch every existing skill |
| Red Flags sections retrofit | v0.2 | Medium — touch every existing skill |
| `source-driven-development` pattern adoption | v0.2 | Low — engineering process addition |
| `git-workflow-and-versioning` discipline | Immediate | Low — applied at repo init |
| Severity labels + change sizing for CTC | v0.2 or v0.3 | Low — format addition |
| ADR pattern formalization | v0.2 | Medium — retrofit `pipeline/architecture/` history |

## Files to consult (not committed to Tilth)

The agent-skills repo's `skills/spec-driven-development/SKILL.md`, `skills/test-driven-development/SKILL.md`, and `skills/code-review-and-quality/SKILL.md` are the three worth reading directly when retrofitting Tilth skills. Format reference, not content reuse.
