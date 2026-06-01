---
lane: 1 of 5
target: Hermes Agent (Nous Research) — reflective-phase mechanism
status: research-only — no code, no LOCK
authored: 2026-05-10
output_for: Tilth Reflection design coordinator
license_target: MIT (confirmed)
---

# Lane 1 — Hermes Agent: Reflective Phase

Pure research brief. Maps Hermes Agent's reflection/skill-creation/skill-curation
mechanism against the five questions the Reflection design needs answered. Ends
with a Tilth-implications subsection sketching the F-REFLECTION-* gate family.

## Premise verification before doing the work

The dispatch prompt said "~135K stars, MIT-licensed, code is readable." Two of three check out; the third is roughly right:

- **MIT-licensed.** Confirmed. Footer of every doc page renders "Built by Nous Research · MIT License · 2026." Bundled skill `requesting-code-review/SKILL.md` carries `license: MIT` in its frontmatter.
- **Repo is canonical and code is readable.** Confirmed. `github.com/NousResearch/hermes-agent` is the real, primary repo. The `tools/skill_manager_tool.py` blob renders 747 lines (26.6 KB) — readable, well-commented Python.
- **Star count.** Not 135K. GitHub's own page header on the SKILL.md blob (fetched 2026-05-10) reads **103k stars / 14.8k forks / 2k issues / 3.7k PRs**. The skill_manager_tool.py blob (same fetch session) reads **29.4k stars / 3.9k forks**. The repo root README page returned **946 stars / 152 forks**. Three different numbers from three live GitHub URLs in the same session — almost certainly CDN/cache layer skew, not three different repos. Treat the canonical figure as **~100K stars** (the high-end fetch is most consistent with secondary-source reporting that put it at "60k in 2 months, 95.6k in 7 weeks"). The user's 135K is in the right order of magnitude.

The substantive premise — "Hermes has a reflective phase that writes skill files" — is real, named, and load-bearing in the codebase. Method name is `_spawn_background_review()`, lives in `run_agent.py`, source-cited by an open feature-request issue.

## Q1 — What triggers reflection?

**Three trigger surfaces, none of them token-count thresholds:**

### a. Live-loop self-improvement during conversation (synchronous, agent-driven)

The agent decides for itself whether to call `skill_manage(action="create" | "patch" | "edit")` as a regular tool call during its turn. The triggering criteria are encoded in the function-calling schema description (the model reads them as part of the tool's natural-language docs). From `tools/skill_manager_tool.py` lines 555-572 (`SKILL_MANAGE_SCHEMA["description"]`):

> "Create when: complex task succeeded (5+ calls), errors overcome, user-corrected approach worked, non-trivial workflow discovered, or user asks you to remember a procedure.
> Update when: instructions stale/wrong, OS-specific failures, missing steps or pitfalls found during use. If you used a skill and hit issues not covered by it, patch it immediately.
> After difficult/iterative tasks, offer to save as a skill. Skip for simple one-offs. Confirm with user before creating/deleting."

This is the "Reflective Phase" described in Hermes marketing — but mechanistically it is just **the model deciding to call a tool, prompted by a tool description**. There is no separate reflection state machine; the agent loop is identical whether the agent is solving a task or writing a SKILL.md. Cite: `docs/user-guide/features/skills#when-the-agent-creates-skills`.

### b. Background review fork (asynchronous, periodic, idle-gated)

A separate, named subsystem: `_spawn_background_review()` in `run_agent.py`. From open issue #16761:

> "Hermes has an excellent `_spawn_background_review()` mechanism that periodically spawns a sub-agent to review conversation history and save memories/skills. However, the review prompt is hardcoded:
> - Memory review: 'Has the user revealed things about themselves — their persona, desires, preferences?'
> - Skill review: 'Was a non-trivial approach used to complete a task?'"

So **two hardcoded review prompts** (memory, skills) get appended to a fresh `AIAgent` instance that re-reads conversation history with no tool context, decides what to persist, and writes via the same `memory` and `skill_manage` tools. The reviewer fork **inherits the parent's live runtime (provider, model, credentials)** but starts a clean prompt cache; cite WebSearch result quoting the Hermes self-evolution repo's description of the fork.

### c. Curator pass (asynchronous, calendrical, idle-gated)

Separate from the reflection fork. A maintenance pass on already-written agent-created skills — staleness transitions and consolidation review. Triggered on:
- CLI session start, **and** cron-ticker thread inside the messaging gateway.
- Gates: `interval_hours: 168` (7 days) since last run, **and** `min_idle_hours: 2` (operator not active).
- First-run defer: brand-new install seeds `last_run_at = now`, defers the first real pass by a full interval. Lets operators dry-run / pin / disable before automation touches anything.

Cite: `docs/user-guide/features/curator#how-it-runs`. Two phases per run:

1. Deterministic transitions — no LLM. `stale_after_days: 30` and `archive_after_days: 90`. Archived skills go to `~/.hermes/skills/.archive/` (recoverable; never deleted).
2. LLM review pass — `max_iterations: 8`, runs on an `auxiliary.curator` aux-model slot (default = main chat model, overridable to cheaper aux). Decides per-skill: keep / patch / consolidate / archive.

**Net answer to Q1:** Three triggers, layered. (a) Live in-turn agent-driven via tool-schema prompting on completion of complex tasks. (b) Periodic between-turn background fork driven by hardcoded review prompts. (c) Calendrical (7-day, 2-hour-idle) curator maintenance over the accumulated skill library. None of them is token-count-threshold-based.

## Q2 — What gets extracted?

Three different things from three triggers, into two different on-disk surfaces:

### From live `skill_manage` calls (Q1.a)
- **Full SKILL.md content** synthesized by the model itself from in-context reasoning. The model writes the markdown body — frontmatter, "When to Use," "Procedure," "Pitfalls," "Verification" sections — and submits it as the `content` arg to `skill_manage(action="create", name=..., content=...)`.
- **Not transcript-extracted.** The schema accepts only the finished SKILL.md text, not a conversation slice. The model has to compress the discovered workflow into procedure-ready prose.
- Supporting files (templates, scripts) are separate write_file calls.

### From the background-review fork (Q1.b)
- **Two parallel extraction streams**, hardcoded prompts:
  - Memory stream — "Has the user revealed things about themselves — their persona, desires, preferences?" → writes to `MEMORY.md` / `USER.md` via the `memory` tool.
  - Skill stream — "Was a non-trivial approach used to complete a task?" → writes to `~/.hermes/skills/<name>/SKILL.md` via `skill_manage`.
- A secondary source (WebSearch result quoting the self-evolution repo's commits) describes the fork's discipline as **class-first (rubric-based rather than free-form)** and **active-update biased** (prefers patching the skill the agent just loaded, over creating a new one).
- **Operator-confirmed outcomes are NOT structurally required.** The tool schema does have a soft norm ("Confirm with user before creating/deleting") and a hard rule (`delete` on pinned skills refuses), but `create` writes through without operator approval.

### From the curator pass (Q1.c)
- **Usage telemetry** (deterministic, no LLM): `view_count` / `use_count` / `patch_count` / `last_used_at` / `last_viewed_at` / `created_at` / `state` / `pinned` / `archived_at`, all per-skill, sidecar at `~/.hermes/skills/.usage.json`. Bundled and hub-installed skills are excluded.
- **Aux-model review output** (per-run report): `~/.hermes/logs/curator/<utc-iso>/run.json` (machine) + `REPORT.md` (human).

**Confidence scores: none.** Nothing in the schema or curator output carries an explicit confidence number. The artifact is treated as binary (exists / doesn't, kept / archived). Pattern-with-confidence-score is not the Hermes idiom — Hermes treats the SKILL.md as either present-and-current or stale-and-archivable.

**Failure modes vs. successes: encoded in prose, not flagged structurally.** The recommended SKILL.md template has a "Pitfalls" section, but it's free-text — there's no machine-readable failure-vs-success registry. The `skill_manage` description tells the agent "patch it immediately" when "you hit issues not covered by it" — failure-driven update is a guideline, not a typed field.

## Q3 — On-disk skill-file shape

### Directory layout (from `tools/skill_manager_tool.py` and `docs/user-guide/features/skills#skill-directory-structure`)

```
~/.hermes/skills/                  # Single source of truth — all writes land here
├── <category>/                    # Optional category subdir
│   └── <skill-name>/
│       ├── SKILL.md               # Required — main instructions
│       ├── references/            # Allowed subdir — additional docs
│       ├── templates/             # Allowed subdir — output formats
│       ├── scripts/               # Allowed subdir — helper scripts
│       └── assets/                # Allowed subdir — supplementary files
├── .hub/                          # Skills-Hub install state
│   ├── lock.json
│   ├── quarantine/
│   └── audit.log
├── .bundled_manifest              # Tracks bundled-skill seed hashes
├── .usage.json                    # Curator telemetry sidecar
├── .archive/                      # Curator-archived skills (recoverable)
└── .curator_backups/<iso>/        # Tarball snapshots before curator runs
```

`ALLOWED_SUBDIRS = {"references", "templates", "scripts", "assets"}` is the hard whitelist; anything outside fails validation with "File must be under one of: …" (line 263).

### SKILL.md format — YAML frontmatter + markdown body

Required frontmatter fields (from `_validate_frontmatter`, lines 169-203):
- `name` (string, max 64 chars, regex `^[a-z0-9][a-z0-9._-]*$`)
- `description` (string, max 1,024 chars)

Optional frontmatter:
- `version`, `author`, `license`, `platforms: [macos|linux|windows]`
- `metadata.hermes.tags`, `metadata.hermes.category`
- `metadata.hermes.fallback_for_toolsets` / `requires_toolsets` / `fallback_for_tools` / `requires_tools` — conditional activation
- `metadata.hermes.config[]` — declares config.yaml settings the skill needs
- `metadata.hermes.related_skills`
- `required_environment_variables[]` — declares env vars the skill needs (prompted on first load in CLI; never asked over messaging channels)

Body convention (not enforced by validator, only by skill_view rendering and the agent's own habits):
- `# Skill Title`
- `## When to Use` — trigger conditions
- `## Procedure` — numbered steps
- `## Pitfalls` — known failure modes
- `## Verification` — confirmation steps

Hard size limits:
- `MAX_SKILL_CONTENT_CHARS = 100_000` (~36k tokens) for SKILL.md itself.
- `MAX_SKILL_FILE_BYTES = 1_048_576` (1 MiB) per supporting file.

### Pydantic / JSON-schema?

**No Pydantic model.** Validation is hand-rolled in `_validate_frontmatter` — `yaml.safe_load` parses the frontmatter into a `dict`, then explicit `if "name" not in parsed` / `if "description" not in parsed` checks. This is a deliberate choice: skill files are written by humans and LLMs both, the validator is permissive, and the rejection messages are tutoring ("Frontmatter must include 'name' field." line 192). There is a strict OpenAI-function-calling JSON schema for the `skill_manage` tool itself (lines 555-660) — but that's the parameter contract for the tool call, not the on-disk artifact schema. **The disk format is a YAML-frontmatter convention, not a typed schema.**

### Usage telemetry sidecar shape (`.usage.json`, from `docs/user-guide/features/curator#usage-telemetry`)

```json
{
  "my-skill": {
    "use_count": 12,
    "view_count": 34,
    "last_used_at": "2026-04-24T18:12:03Z",
    "last_viewed_at": "2026-04-23T09:44:17Z",
    "patch_count": 3,
    "last_patched_at": "2026-04-20T22:01:55Z",
    "created_at": "2026-03-01T14:20:00Z",
    "state": "active",
    "pinned": false,
    "archived_at": null
  }
}
```

This **is** machine-readable and per-skill. State enum: `active | stale | archived`. `pinned: true` survives sessions and exempts the skill from both curator transitions and agent `skill_manage(action="delete")`.

## Q4 — Retrieval at next use

**Three-tier progressive disclosure**, NOT embedding similarity:

### Tier 0 — `skills_list()`
From `docs/user-guide/features/skills#progressive-disclosure`:

> "Level 0: `skills_list()` → [{name, description, category}, ...]   (~3k tokens)"

Returns the name + description + category triple for every skill (bundled + hub + agent-created + external). This is the index. The agent reads it during a turn and decides what to load next.

### Tier 1 — `skill_view(name)`
Returns the full `SKILL.md` content of one named skill.

### Tier 2 — `skill_view(name, path)`
Returns one specific supporting file (a `references/foo.md` or `templates/bar.json`).

### Plus: System-prompt skills index (always-on)
At session start, `agent/prompt_builder.py` injects a skills index block (Layer 7 in the assembled system prompt — see `docs/developer-guide/prompt-assembly`). Cite the page's concrete example:

> ```
> ## Skills (mandatory)
> Before replying, scan the skills below. If one clearly matches
> your task, load it with skill_view(name) and follow its instructions.
> ...
> <available_skills>
>   software-development:
>     - code-review: Structured code review workflow
>     - test-driven-development: TDD methodology
>   research:
>     - arxiv: Search and summarize arXiv papers
> </available_skills>
> ```

This is **description-string matching by the LLM itself.** No embedding, no vector store, no exact-match key, no rule-based filter. The skill's description field is the *only* retrieval surface; the LLM scans the list and picks. Conditional-activation fields (`fallback_for_toolsets`, `requires_toolsets`) hide/show skills deterministically before the LLM sees them, which is the closest thing to rule-based gating.

### Slash-command path

Every skill is also auto-registered as a slash command (`/<skill-name>`) on every messaging surface. This is operator-driven retrieval, not agent-driven — the operator types `/plan` and forces the skill into context. From `docs/user-guide/features/skills#using-skills`.

### Cache invalidation on write

When `skill_manage` succeeds, `clear_skills_system_prompt_cache(clear_snapshot=True)` is called (line 545). This invalidates the cached skills-index block so the **next** session's system prompt rebuilds with the new skill listed. Mid-session writes do not change the live system prompt (frozen-snapshot pattern, same as memory) — they just become visible on the next session start. The `skills_list` tool call always returns live disk state.

**Net answer to Q4:** LLM-mediated retrieval by description-string match against a flat catalog the LLM sees in its system prompt. No embeddings. No vector index. Conditional-activation (tool-availability) is the only deterministic filter.

## Q5 — Gate / sanity-check / signature / write-time validation

This is where Tilth's discipline diverges most sharply from Hermes's. Hermes has gates, but they are best-effort security checks, not Logician-style fail-closed semantic correctness gates. Mapping by layer:

### Layer A — Pre-write validation (always runs, deterministic, Python)
From `_create_skill` and `_validate_*` helpers in `tools/skill_manager_tool.py`:

- Name regex (line 23): `^[a-z0-9][a-z0-9._-]*$`, max 64 chars
- Category sanity: no slashes/backslashes, single directory segment only
- Frontmatter must parse as YAML, must be a `dict`, must contain `name` + `description`, description ≤ 1,024 chars, body non-empty
- Content size ≤ 100,000 chars
- Path traversal blocked (`".." in normalized.parts`, line 256)
- Subdirectory whitelist (`{references, templates, scripts, assets}`)
- File size ≤ 1 MiB
- Name uniqueness checked across all skill directories before create

All of these fail with `{"success": false, "error": "..."}` and never touch disk.

### Layer B — Security scan after write, before commit (best-effort)
From `_security_scan_skill`, lines 53-79 — the agent's create/edit/patch/write_file paths all call this after `_atomic_write_text`. It dispatches to `tools.skills_guard.scan_skill(skill_dir, source="agent-created")`, which is the **same scanner** community-hub installs run through:

```
result = scan_skill(skill_dir, source="agent-created")
allowed, reason = should_allow_install(result)
if allowed is False:
    report = format_scan_report(result)
    return f"Security scan blocked this skill ({reason}):\n{report}"
```

The scan checks for "data exfiltration, prompt injection, destructive commands, supply-chain signals, and other threats" (cite `docs/user-guide/features/skills#security-scanning`). **Three verdicts**: `True` (allow), `False` (block), `None` ("ask" — allow with logged warning). For agent-created skills, the `None` verdict **does not block**:

```
if allowed is None:
    # "ask" — allow but include the warning so the user sees the findings
    report = format_scan_report(result)
    logger.warning("Agent-created skill has security findings: %s", reason)
    # Don't block — return None to allow, but log the warning
    return None
```

This is a deliberate softening for self-improvement: the same scanner that gates community installs (where `--force` is needed to override a caution-tier finding) is more permissive when the agent itself is the author. Only `dangerous` verdicts block the agent.

### Layer C — Atomic write with rollback on scan block
From `_atomic_write_text` (lines 280-310): writes to `tempfile.mkstemp` in the same directory, then `os.replace(temp_path, file_path)`. On security-scan block, `_create_skill` calls `shutil.rmtree(skill_dir, ignore_errors=True)` to roll back the whole directory; `_edit_skill` and `_patch_skill` restore the captured `original_content` via a second atomic write. **No partial-write state ever lands**, and a blocked write leaves the on-disk skill unchanged.

### Layer D — Cryptographic signature / hash?
**None.** There is no Ed25519, no SHA-256-of-content-as-id, no provenance chain, no signed manifest. The only hash in the system is the **bundled-skill content hash** in `.bundled_manifest` — used to detect whether a bundled skill has been user-modified (so curator sync doesn't stomp local edits). That hash is provenance-tracking for upstream bundle drift, not author-identity attestation. Agent-created skills carry no cryptographic identity.

### Layer E — Operator approval at write?
**No structural requirement.** The tool description says "Confirm with user before creating/deleting" but that's natural-language guidance to the LLM, not a callback or approval gate. `create` writes through without operator approval. Two operator-driven brakes exist after the fact:

- `pinned: true` (operator must run `hermes curator pin <name>`) — exempts a skill from both curator transitions and `skill_manage(action="delete")`. **`patch` and `edit` still go through on pinned skills** — pin guards deletion, not content drift.
- `hermes curator pause` — disables curator entirely until `hermes curator resume`.

### Layer F — Auto-apply vs. proposes-only
**Auto-apply.** Skills the agent writes are immediately visible in the next session's `skills_list()` and the next session's system-prompt skills-index (after cache invalidation). The curator's review pass can patch, consolidate, or archive without operator review — it logs a `REPORT.md` after the fact. The only "proposes-only" mode is `hermes curator run --dry-run`, which the operator opts into; the default cadence is auto-apply with an after-the-fact REPORT plus a rollback-able tarball snapshot.

**Recoverability over prevention.** Before every real curator pass: `~/.hermes/skills/.curator_backups/<utc-iso>/skills.tar.gz`. `hermes curator rollback` restores the newest snapshot (with confirmation), itself reversible via a pre-rollback snapshot. Snapshots pruned to `curator.backup.keep: 5`.

**Net answer to Q5:** Layer A is genuine deterministic validation (regex + YAML + size + path-traversal). Layer B is a security-scan that downgrades from blocking to logged-warning for agent-created content. Layers C+D are write-discipline (atomic) but with **no cryptographic provenance**. Layer E provides operator brakes (pin, pause) but no per-write approval. Layer F's default is auto-apply with tarball-recoverable history. **Hermes treats skill writes the way Git treats commits — atomic, rollbackable, after-the-fact-auditable — not the way Tilth treats grant claims.** There is no Logician-class semantic gate that says "this proposed skill would violate Law 4 if applied to future drafts."

## Q6 — What can Tilth steal that's idiomatic to MIT + Pydantic AI?

These five primitives port cleanly:

### 1. **Two-tier reflection: live (in-turn) + background fork (between-turn)**
Hermes's split — agent-driven `skill_manage` during the turn, plus a periodic `_spawn_background_review()` that re-reads conversation history with a fresh prompt cache — is exactly the shape Tilth wants. The reviewer fork's "fresh context finds what you miss" discipline (cited verbatim from `requesting-code-review/SKILL.md`: "No agent should verify its own work. Fresh context finds what you miss.") aligns with Tilth's cross-family review pattern. Port as a Pydantic AI agent that the orchestrator can spawn between cycles with the parent's runtime resolver. **What to NOT copy:** Hermes's hardcoded review prompts (cite issue #16761 — operators are already asking for customizability). Tilth should make the review prompt itself a versioned artifact in the architecture (likely §0.5 row, paired with §4 v2.x gates).

### 2. **Progressive-disclosure retrieval (skills_list → skill_view → skill_view+path)**
Three flat tool calls, no vector DB, no embedding pipeline. The whole catalog fits in ~3k tokens at Level 0 because the description field is the *only* retrieval surface. This is dramatically simpler than ChromaDB/RAG and matches the v0.1 substrate ban on marketplace-installed deps. **For Tilth:** Lessons, Card-extracted patterns, and post-cycle reflections all become flat retrievable artifacts indexed by description. Pydantic AI agents would expose `lessons_list()` / `lesson_view()` as deterministic Python tools. **Constraint:** Hermes hits this wall around 8k-15k skills; a single grant cycle can plausibly produce dozens of Pattern artifacts, so Tilth's catalog stays modest unless a higher-tier index is added later.

### 3. **Curator with calendrical + idle-gated cadence, dry-run-first**
The 7-day-interval / 2-hour-idle combination is operator-friendly and load-aware. The first-run-defers-one-interval discipline is exactly the pattern v0.1 needs: do not run autonomous mutation until the operator has had time to inspect, pin, and disable. **Port:** Tilth's lessons-curator pass (probably v1.x Archivist) inherits `interval_hours` + `min_idle_hours` + `first_run_defer` semantics. The deterministic-then-LLM two-phase split (auto-transitions first, LLM review second) is the right ordering — the cheap pass establishes scope before the expensive pass is invoked.

### 4. **Atomic write + tarball backup + rollback as a structural primitive**
`_atomic_write_text` (tempfile + os.replace) and `hermes curator backup` (tar.gz of the entire skills tree, kept-5 ring buffer) are dirt-cheap and they remove the entire class of "the curator deleted my work" failures. **Port:** Tilth's lessons memory and Card library should have the same primitive — write through a Pydantic AI tool that performs atomic write + tarball-of-tree before any mutation. Operator-runnable `tilth curator rollback`. This is L-006 (verify enforcement-layer exists) at the artifact-write layer.

### 5. **Per-artifact usage telemetry sidecar**
`.usage.json` with `use_count` / `view_count` / `patch_count` / `last_used_at` is the structural primitive that lets staleness transitions happen deterministically and lets the LLM review be informed by frequency data ("this skill hasn't been loaded in 90 days"). **Port:** Tilth tracks per-Pattern, per-Lesson, per-Card usage in a counterpart sidecar. The `lessons.json` machine memory in `pipeline/institutional_memory/` is the closest existing artifact and the v0.1 starting point.

### What does NOT port — by deliberate non-decision

- **No cryptographic provenance.** Hermes has none. Tilth needs Ed25519 on reflection artifacts (consistent with v7.0.7 SP0 / KFR canonicalization signature regime). Do not adopt Hermes's "we trust the scanner + atomic write + tarball backup" posture for Tilth — Tilth's classification register and operator sign-off pattern is the right model.
- **No semantic correctness gate.** Hermes's gates are security (exfil / injection) and shape (regex + size + YAML). Tilth needs F-REFLECTION-* gates that check whether the proposed reflected pattern would cause F-LAW-* violations if applied. That's a §4 Logician v2.x extension, not a port.
- **No operator-approval-at-write requirement.** Hermes's "confirm with user before creating" is LLM-prompted guidance. Tilth needs structural approval — at minimum for reflections that would propose new operating guidance, at most for reflections that would touch the Card library.
- **No description-string-only retrieval at high catalog cardinality.** Hermes survives because most operators run 20-200 skills. Tilth's lessons + patterns + cards at v1.x will plausibly hit thousands of artifacts; description-string LLM retrieval will degrade. Plan for embedding-or-deterministic retrieval at a v1.x horizon while shipping Hermes's flat-list pattern at v0.1.

## Verbatim code excerpts illustrating each mechanism

**(1) Reflection trigger — agent-side, via tool-schema natural-language prompt**

```python
# tools/skill_manager_tool.py, SKILL_MANAGE_SCHEMA["description"] (lines 555-572)
"description": (
    "Manage skills (create, update, delete). Skills are your procedural "
    "memory — reusable approaches for recurring task types. "
    "New skills go to ~/.hermes/skills/; existing skills can be modified wherever they live.\n\n"
    "Actions: create (full SKILL.md + optional category), "
    "patch (old_string/new_string — preferred for fixes), "
    "edit (full SKILL.md rewrite — major overhauls only), "
    "delete, write_file, remove_file.\n\n"
    "Create when: complex task succeeded (5+ calls), errors overcome, "
    "user-corrected approach worked, non-trivial workflow discovered, "
    "or user asks you to remember a procedure.\n"
    "Update when: instructions stale/wrong, OS-specific failures, "
    "missing steps or pitfalls found during use. "
    "If you used a skill and hit issues not covered by it, patch it immediately.\n\n"
    "After difficult/iterative tasks, offer to save as a skill. "
    "Skip for simple one-offs. Confirm with user before creating/deleting.\n\n"
    "Good skills: trigger conditions, numbered steps with exact commands, "
    "pitfalls section, verification steps. Use skill_view() to see format examples."
),
```

**(2) Frontmatter validator — no Pydantic, hand-rolled YAML check**

```python
# tools/skill_manager_tool.py, _validate_frontmatter (lines 169-203)
def _validate_frontmatter(content: str) -> Optional[str]:
    if not content.strip():
        return "Content cannot be empty."
    if not content.startswith("---"):
        return "SKILL.md must start with YAML frontmatter (---). See existing skills for format."
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return "SKILL.md frontmatter is not closed. Ensure you have a closing '---' line."
    yaml_content = content[3:end_match.start() + 3]
    try:
        parsed = yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        return f"YAML frontmatter parse error: {e}"
    if not isinstance(parsed, dict):
        return "Frontmatter must be a YAML mapping (key: value pairs)."
    if "name" not in parsed:
        return "Frontmatter must include 'name' field."
    if "description" not in parsed:
        return "Frontmatter must include 'description' field."
    if len(str(parsed["description"])) > MAX_DESCRIPTION_LENGTH:
        return f"Description exceeds {MAX_DESCRIPTION_LENGTH} characters."
    body = content[end_match.end() + 3:].strip()
    if not body:
        return "SKILL.md must have content after the frontmatter (instructions, procedures, etc.)."
    return None
```

**(3) Atomic write with rollback discipline**

```python
# tools/skill_manager_tool.py, _atomic_write_text (lines 280-310)
def _atomic_write_text(file_path: Path, content: str, encoding: str = "utf-8") -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(
        dir=str(file_path.parent),
        prefix=f".{file_path.name}.tmp.",
        suffix="",
    )
    try:
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(content)
        os.replace(temp_path, file_path)
    except Exception:
        try:
            os.unlink(temp_path)
        except OSError:
            logger.error("Failed to remove temporary file %s during atomic write", temp_path, exc_info=True)
        raise
```

**(4) Security scan with rollback on block (within `_create_skill`, lines 327-340)**

```python
# Write SKILL.md atomically
skill_md = skill_dir / "SKILL.md"
_atomic_write_text(skill_md, content)

# Security scan — roll back on block
scan_error = _security_scan_skill(skill_dir)
if scan_error:
    shutil.rmtree(skill_dir, ignore_errors=True)
    return {"success": False, "error": scan_error}
```

**(5) Security-scan softening for agent-created content (lines 53-79)**

```python
def _security_scan_skill(skill_dir: Path) -> Optional[str]:
    if not _GUARD_AVAILABLE:
        return None
    try:
        result = scan_skill(skill_dir, source="agent-created")
        allowed, reason = should_allow_install(result)
        if allowed is False:
            report = format_scan_report(result)
            return f"Security scan blocked this skill ({reason}):\n{report}"
        if allowed is None:
            # "ask" — allow but include the warning so the user sees the findings
            report = format_scan_report(result)
            logger.warning("Agent-created skill has security findings: %s", reason)
            # Don't block — return None to allow, but log the warning
            return None
    except Exception as e:
        logger.warning("Security scan failed for %s: %s", skill_dir, e, exc_info=True)
        return None
```

**(6) Background-review fork — secondary source, code path itself not directly fetched**

From open issue NousResearch/hermes-agent#16761:

> "Hermes has an excellent `_spawn_background_review()` mechanism that periodically spawns a sub-agent to review conversation history and save memories/skills. However, the review prompt is hardcoded:
> - Memory review: 'Has the user revealed things about themselves — their persona, desires, preferences?'
> - Skill review: 'Was a non-trivial approach used to complete a task?'"
>
> "Implementation Approach: 1. Add `reflection_prompt: Optional[str]` to `AIAgent.__init__` (loaded from `config.yaml`) 2. In `_spawn_background_review()`, append `reflection_prompt` to the existing review prompt (memory/skill/combined) 3. The review sub-agent treats this as additional criteria alongside memory/skill review 4. No breaking changes — defaults to current behavior when unset"

Note: the run_agent.py source file (~13,700 lines per `docs/developer-guide/agent-loop`) was not directly fetched line-by-line in this lane. The `_spawn_background_review()` symbol is confirmed by the issue's PR-targeted change description.

**(7) Curator usage-telemetry sidecar shape**

```json
{
  "my-skill": {
    "use_count": 12,
    "view_count": 34,
    "last_used_at": "2026-04-24T18:12:03Z",
    "last_viewed_at": "2026-04-23T09:44:17Z",
    "patch_count": 3,
    "last_patched_at": "2026-04-20T22:01:55Z",
    "created_at": "2026-03-01T14:20:00Z",
    "state": "active",
    "pinned": false,
    "archived_at": null
  }
}
```

(Source: `docs/user-guide/features/curator#usage-telemetry`.)

**(8) System-prompt skills-index injection (Layer 7 in prompt assembly)**

```
# Layer 7: Skills index
## Skills (mandatory)
Before replying, scan the skills below. If one clearly matches
your task, load it with skill_view(name) and follow its instructions.
...
<available_skills>
  software-development:
    - code-review: Structured code review workflow
    - test-driven-development: TDD methodology
  research:
    - arxiv: Search and summarize arXiv papers
</available_skills>
```

(Source: `docs/developer-guide/prompt-assembly#concrete-example-assembled-system-prompt`.)

## Tilth implications — F-REFLECTION-* gate family sketch

What Hermes shows is that the **trigger mechanics** and the **on-disk artifact shape** are cheap and well-understood at MIT-license-readable scale. What Hermes leaves on the table — and what Tilth's Five Laws + classification-driven routing + Logician fail-closed discipline make non-negotiable — is **semantic and provenance gating**. Sketch of the F-REFLECTION-* gate family the architecture lane should be ready to design:

**Trigger / scope gates (PRE-reflection):**

- **F-REFLECTION-TRIGGER-MALFORMED** — proposed reflection lacks the required trigger metadata (which cycle, which seat, which artifacts read, which operator-confirmed outcomes are present). Reflections without trigger provenance fail-closed. Parallels Hermes Q1 but adds typed trigger record.
- **F-REFLECTION-CONTEXT-LEAK** — proposed reflection draws from more than one `org_slug`'s conversation history (Law 3 violation, would create cross-org bleed). Hermes has no equivalent gate — its memory is single-tenant by design.
- **F-REFLECTION-OPERATOR-VOICE-FABRICATION** — proposed reflection encodes "the operator said X" without verbatim-quote-with-source provenance (Law 5 violation, would fabricate). Hermes's tool description says "user-corrected approach worked" but doesn't structurally require operator-quoted evidence.

**Extraction shape gates (DURING reflection):**

- **F-REFLECTION-CLASSIFICATION-MISSING** — proposed reflection artifact lacks `public | shareable | confidential` classification. Routes to `confidential` by default per F-CLASS-NEW-FACT-UNCLASSIFIED's pattern. Hermes has no equivalent — its skill catalog assumes public.
- **F-REFLECTION-CONFIDENCE-UNTAGGED** — Hermes deliberately omits confidence scoring. Tilth probably wants `confidence_tier: observed_once | repeated | confirmed_with_operator` typed in the artifact, with the `confirmed_with_operator` tier required before the reflection can affect downstream Seat behavior.
- **F-REFLECTION-CARDINALITY-EXPLOSION** — flat description-string retrieval (Hermes's Q4 model) degrades past a catalog size threshold. PRE-check on number of active reflections before allowing a new write; failure routes to consolidation rather than create.

**Write-time provenance gates (POST-extraction, PRE-disk):**

- **F-REFLECTION-SIGNATURE-INVALID** — reflection artifact must be Ed25519-signed by the producing seat. Hermes has nothing here.
- **F-REFLECTION-CANONICAL-HASH-DRIFT** — content-addressable hash of the artifact must match a canonicalized re-serialization (parallels v7.0.4-M1 KFR canonicalization regime — supersession row 315 → 334).
- **F-REFLECTION-CONTENT-VIOLATES-LAW-N** — Logician runs all Five Laws as PRE/POST gates on the proposed artifact's *content*, not just its shape. A reflection that proposes "match this funder by softening the project's land-use boundary" trips Law 2 (no boundary drift). Hermes's security scanner checks for prompt injection and shell exec; it does not check whether a skill *would cause* a domain-rule violation if applied.

**Application-time gates (POST-disk, PRE-effect):**

- **F-REFLECTION-AUTO-APPLY-ATTEMPTED** — analogous to existing R-ARCHIVIST-NO-CANONICAL-MUTATE. Reflection-write is proposes-only by default; auto-apply requires explicit operator approval flag in the artifact metadata. Hermes's default is auto-apply; Tilth's must invert.
- **F-REFLECTION-RETRIEVAL-CACHE-STALE** — Hermes invalidates `clear_skills_system_prompt_cache(clear_snapshot=True)` on every write. Tilth's equivalent: any reflection write invalidates the next-session retrieval cache, AND the in-flight cycle's already-loaded reflections (frozen-snapshot pattern is wrong if the operator has just approved a Law-4 dialect substitution mid-cycle).
- **F-REFLECTION-CURATOR-INTERVAL-DRIFT** — operator-configurable interval (Hermes default 7d/2h) must be respected; out-of-band curator runs need a documented `--operator-initiated` flag, audited.

**Cardinality / archive gates (ongoing):**

- **F-REFLECTION-STALE-ABOVE-THRESHOLD** — staleness threshold breach blocks reflection-application (not just curator transition), so a 90-day-untouched lesson doesn't keep silently shaping new drafts.
- **F-REFLECTION-OPERATOR-PIN-VIOLATION** — operator-pinned reflections cannot be patched or edited by the agent without explicit unpin (Hermes pins only block delete; Tilth's pins block all mutation).
- **F-REFLECTION-ROLLBACK-MISSING-BACKUP** — analogous to Hermes's `.curator_backups/` ring buffer. PRE-curator-run: refuse to run if backup target is unwriteable or the keep-N ring buffer is corrupted.

**Net structural takeaway:** Hermes's reflection design is well-engineered for a single-tenant developer-assistant context where the worst-case mutation is a sub-optimal SKILL.md and rollback recovers. Tilth's reflection design serves grant-writing where the worst-case mutation is a fabricated funder commitment or a silently-rewritten Law-4 flagged term. Hermes is a strong model for the **mechanics** (trigger, atomic write, telemetry, curator cadence); Tilth must layer **provenance** (Ed25519, canonicalization, operator-signed register) and **semantic gating** (Five Laws as PRE/POST on content, not shape) on top of Hermes-style mechanics. The F-REFLECTION-* family is the bridge.

## Sources

- [Hermes Agent — main repo (`NousResearch/hermes-agent`)](https://github.com/NousResearch/hermes-agent)
- [Hermes Agent — README at main](https://github.com/NousResearch/hermes-agent/blob/main/README.md)
- [Hermes Agent docs — index](https://hermes-agent.nousresearch.com/docs/)
- [Skills System (docs)](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)
- [Persistent Memory (docs)](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)
- [Curator (docs)](https://hermes-agent.nousresearch.com/docs/user-guide/features/curator)
- [Architecture (developer-guide)](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture)
- [Agent Loop Internals (developer-guide)](https://hermes-agent.nousresearch.com/docs/developer-guide/agent-loop)
- [Prompt Assembly (developer-guide)](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly)
- [`tools/skill_manager_tool.py` — source (747 lines, 26.6 KB, MIT)](https://github.com/NousResearch/hermes-agent/blob/main/tools/skill_manager_tool.py)
- [Bundled `requesting-code-review/SKILL.md` — real-world artifact shape](https://github.com/NousResearch/hermes-agent/blob/main/skills/software-development/requesting-code-review/SKILL.md)
- [Issue #16761 — `_spawn_background_review()` reflection prompt is hardcoded (FR)](https://github.com/NousResearch/hermes-agent/issues/16761)
- [Issue #7816 — Curator design discussion (referenced by curator docs)](https://github.com/NousResearch/hermes-agent/issues/7816)
- [Companion repo: `hermes-agent-self-evolution` — DSPy + GEPA optimization](https://github.com/NousResearch/hermes-agent-self-evolution)
