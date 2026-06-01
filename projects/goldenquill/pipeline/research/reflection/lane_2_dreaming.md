---
lane: 2 of 5
target: Anthropic "Dreaming" — overnight session processing into memory
researcher: Cowork session 2026-05-10
time_budget: 30-45 min, web research only
status: filed; no LOCK
---

# Lane 2 — Anthropic Dreaming (overnight session→memory consolidation)

## TL;DR

"Dreaming" is two things under one metaphor, shipped by Anthropic on **2026-05-06** at the Code with Claude developer event:

1. **Dreams (Managed Agents API)** — a **research-preview**, gated, server-side asynchronous job exposed under `beta.dreams.create` on the Claude Platform. Takes one existing **memory store** plus up to 100 past **session** transcripts, runs a separate Claude session that produces a *new, second* memory store with duplicates merged, contradictions resolved, and new insights surfaced. **Input store is never modified.** Beta header `dreaming-2026-04-21`. ([Dreams - Claude API Docs](https://platform.claude.com/docs/en/managed-agents/dreams))

2. **Auto Dream (Claude Code, client-side)** — a quietly-shipped (not yet officially announced as of the secondary source's writing) feature in Claude Code that runs the same four-phase consolidation pass over the local `~/.claude/projects/<project>/memory/` directory and `MEMORY.md` index, gated on **24 hours since last run** AND **>5 sessions since last run**. Has a `/memory` toggle (`Auto-dream: on`) and a forthcoming `/dream` slash command. The full system prompt is public via claudefa.st. ([Claude Code Dreams](https://claudefa.st/blog/guide/mechanics/auto-dream))

Both share the same conceptual shape: **reflection-as-batch-job over accumulated session artifacts → curated memory artifact** — the REM-sleep analogy is explicit in Anthropic's own framing and inherited by every secondary source.

Production status: **research preview, gated access via `claude.com/form/claude-managed-agents`** for the API. Claude Code Auto Dream is rolling out per plan tier (no separate access form mentioned).

## 1. What is "Dreaming" specifically?

### The problem it solves

> "Agents write to their memory stores as they work, but these writes are local and incremental: over many sessions a memory store accumulates duplicates, contradictions, and stale entries." ([Anthropic Dreams docs](https://platform.claude.com/docs/en/managed-agents/dreams))

The independent secondary source frames the same problem more vividly:

> "But after 20+ sessions, those notes become a mess. Contradictory entries pile up. Relative dates like 'yesterday' lose meaning. Stale debugging solutions reference files that no longer exist. The notebook that was supposed to help Claude remember instead becomes noise that confuses it." ([claudefa.st](https://claudefa.st/blog/guide/mechanics/auto-dream))

### What it operates on

Two distinct deployment shapes for the same idea:

- **Managed Agents API (server-side, gated preview):** operates on a Memory Store resource + 0..100 Session resources. ([Anthropic Dreams docs](https://platform.claude.com/docs/en/managed-agents/dreams))
- **Claude Code (local, client-side):** operates on the local memory directory `~/.claude/projects/<project>/memory/` + JSONL session transcripts in `~/.claude/projects/<project>/`. ([claudefa.st full system prompt](https://claudefa.st/blog/guide/mechanics/auto-dream))

Crucially: **dreaming does not modify model weights.** From the VentureBeat coverage paraphrasing Anthropic's Mike Krieger / Aaron Albert at the event:

> "We're not changing the model itself through dreaming — it's not doing updates to the weights or anything like that." (VentureBeat / Code with Claude 2026-05-06 — surfaced in web search, full article URL not in provenance set)

This is reflection-as-artifact-curation, not online learning. The artifact is a memory store; the model is unchanged.

### Why "dreaming"

Explicit REM-sleep analogy from claudefa.st (which appears to mirror Anthropic's own framing):

> "During REM sleep, your brain replays the day's events, strengthens connections that matter, discards what doesn't, and organizes everything into long-term memory. People who don't get enough REM sleep struggle to form lasting memories. ... Auto Dream is the REM sleep cycle. It reviews what Auto Memory has collected, strengthens what's still relevant, removes what's outdated, and reorganizes the rest into clean, indexed topic files." ([claudefa.st](https://claudefa.st/blog/guide/mechanics/auto-dream))

## 2. Trigger model

### Managed Agents API (server-side Dreams)

**Explicit operator invocation.** No automatic trigger. Caller invokes `client.beta.dreams.create(...)`. Dreams are submitted asynchronously and the lifecycle is `pending → running → completed | failed | canceled`. ([Anthropic Dreams docs](https://platform.claude.com/docs/en/managed-agents/dreams))

This is important for Tilth: at the API tier, dreaming is **a developer-triggered job, not a daemon**. Anthropic does not run it for you.

### Claude Code (client-side Auto Dream)

**Dual-gate automatic trigger** per claudefa.st (verbatim):

> "Two conditions must both be true before a consolidation cycle triggers:
> 1. 24 hours have passed since the last consolidation
> 2. More than 5 sessions have occurred since the last consolidation
>
> Both conditions are required. If you had one long session over two days, Auto Dream won't trigger (not enough sessions). If you ran 10 quick sessions in two hours, it won't trigger either (not enough time). This dual-gate prevents unnecessary consolidation runs on projects with light usage while ensuring active projects get regular cleanup."

The community replica skill (`grandamenium/dream-skill`) confirms the 24-hour timer via a Claude Code Stop hook that fires on session exit and flags the next session to run `/dream`. ([dream-skill README](https://github.com/grandamenium/dream-skill))

**Manual override available:** users can say "dream" / "auto dream" / "consolidate my memory files" or use the forthcoming `/dream` slash command. ([claudefa.st](https://claudefa.st/blog/guide/mechanics/auto-dream))

### When the dream actually runs

Both deployments run **after sessions end**, not during. The API docs say dreams "typically take minutes to tens of minutes depending on input size." Claudefa.st notes one observed case where Claude Code consolidated 913 sessions in "roughly 8-9 minutes" and runs in the background without blocking. The marketing framing of "overnight" is approximate — these are minutes-scale jobs, not hours-scale, so they fit overnight comfortably but don't require it.

## 3. Write format

### Managed Agents API

Output is a **new Memory Store resource** (separate from input), referenced in `dream.outputs[]` as `{ type: "memory_store", memory_store_id: "memstore_..." }`. The store is "an ordinary memory store in your workspace" — same schema as any other memory store, manipulable via the standard Memory Stores API. ([Anthropic Dreams docs](https://platform.claude.com/docs/en/managed-agents/dreams))

Memory-store schema details aren't dumped on the Dreams page — they live at the Memory Stores API reference (`platform.claude.com/docs/en/managed-agents/memory`). Not fetched this lane; flagged for lane reuse if Tilth-Reflection needs to mirror the schema.

**Versioning / signing:** No mention of cryptographic signing or version pinning of the output memory store at the API level. The store has an ID; that's the only versioning surfaced. The lifecycle has `archived_at` semantics, so retain-or-discard is binary, not multi-version.

### Claude Code (Auto Dream)

Writes **markdown files** to `~/.claude/projects/<project>/memory/` — same directory Auto Memory writes to. The pattern is:

- `MEMORY.md` — index file, hard-capped at 200 lines (because that's the cutoff for what gets loaded at session startup). Pointer entries only — one line per topic file with a short description. Never raw memory content.
- Topic files (e.g., `debugging.md`, `api-conventions.md`, `build-commands.md`, `user-preferences.md`) — actual memory content, organized semantically by topic.

The system prompt (quoted in full at claudefa.st) explicitly instructs:

> "Update `MEMORY.md` so it stays under 200 lines. It's an **index**, not a dump — link to memory files with one-line descriptions. Never write memory content directly into it."

> "For each thing worth remembering, write or update a memory file at the top level of the memory directory. Use the memory file format and type conventions from your system prompt's auto-memory section — it's the source of truth for what to save, how to structure it, and what NOT to save."

**No signing, no formal versioning.** Plain markdown, plain filesystem. The lock-file convention (see §5 Safety) is the only concurrency primitive.

## 4. Read-back path

### Managed Agents API

The output store is **not auto-attached**. The caller has to explicitly attach it to a future session via `resources=[{"type": "memory_store", "memory_store_id": output_store_id}]` when creating the session. ([Anthropic Dreams docs](https://platform.claude.com/docs/en/managed-agents/dreams))

This is a deliberate seam: the dream produces an artifact, the developer reviews it, the developer chooses to attach it (or delete/archive it). **No always-on RAG, no automatic context injection.** Pure operator-mediated.

### Claude Code (Auto Dream)

`MEMORY.md` is loaded at session startup ("First 200 lines of MEMORY.md" per the four-memory-systems table in claudefa.st). Topic files are **referenced from MEMORY.md** and presumably read on demand or via Claude's normal file-tool access — not eagerly pre-loaded.

Practically: **Auto Dream's output is always-on-by-default once it lands on disk.** Unlike the API path, Claude Code doesn't require the user to explicitly attach the consolidated artifact — the artifact replaces the messy version in place.

## 5. Gates / safety mechanisms

### Managed Agents API

From the docs verbatim:

> "The input store is never modified, so you can review the output and discard it if you don't like the result."

> "The dream itself never deletes or modifies its inputs. On `failed` or `canceled` the output store persists with partial contents so you can inspect what was produced before stopping; clean it up via the Memory Stores API if you don't need it."

> "While a dream is `pending` or `running`, archiving or deleting its output store is rejected with a 400. Archiving or deleting an *input* store or session mid-run will cause the dream to fail with `input_memory_store_unavailable` or `input_session_unavailable`."

Safety architecture:

- **Read-only on input store.** Always. Input store is immutable from dreaming's perspective.
- **Write-only to a fresh output store.** Never overwrites prior state.
- **Operator review-and-attach.** The output store is a candidate, not a fait accompli.
- **Fail-soft.** Partial output preserved on failure for inspection.
- **In-flight protection.** Can't delete the output mid-run.
- **Cancellation primitive.** `client.beta.dreams.cancel(dream.id)` available on `pending` or `running`.
- **Archive without delete.** `archived_at` for completed/failed/canceled dreams; no unarchive (deliberate finality).
- **`instructions` parameter** caps at 4,096 characters and lets the operator scope what the dream attends to (e.g., "Focus on coding-style preferences; ignore one-off debugging notes.").
- **Model lock.** Only `claude-opus-4-7` and `claude-sonnet-4-6` are supported as the dreaming-pipeline model during research preview.

**Notably absent from the Anthropic docs:**

- **No explicit PII redaction discipline** documented for dreaming-time. Whatever PII is in the input sessions or input store will be visible to the dreaming model. No mention of differential privacy, classification gates, or content-type allowlists.
- **No signing or attestation** of the output memory store.
- **No diff/audit primitive** — you can read the output store via the Memory Stores API, but the docs don't surface a "what changed vs input" diff endpoint.

### Claude Code (Auto Dream)

Three safety guarantees, verbatim from claudefa.st:

> "**Read-only mode for project code.** During a dream cycle, Claude can only write to memory files. It cannot modify your source code, configuration, tests, or any other project file. The dream process is sandboxed to the memory directory."

> "**Lock file prevents concurrent runs.** If two Claude Code instances are open on the same project, only one can run Auto Dream. A lock file ensures no two consolidation processes operate simultaneously, preventing merge conflicts in your memory files."

> "**Background execution.** You can keep working in Claude Code while Auto Dream runs. It doesn't block your session or require you to wait. The consolidation happens in a separate process."

Plus the structural safety from the system prompt itself:

> "**Memory directory:** `~/.claude/projects/<project>/memory/` — This directory already exists - write to it directly with the Write tool (do not run mkdir or check for its existence)."

> "Don't exhaustively read transcripts. Look only for things you already suspect matter."

The system prompt instructs **narrow grep over JSONL transcripts**, not exhaustive read — this is a token-budget / focus discipline, not a privacy gate, but it has the side effect of reducing surface area.

**Auto-detected memory layouts** in the GitHub replica (`grandamenium/dream-skill`):
- Native Claude Code (`~/.claude/projects/*/memory/`)
- OpenClaw-style (`./memory/` with daily logs) — note the Golden Quill workspace uses this layout
- Project-root (`./MEMORY.md` in project root)

### What Anthropic does NOT describe

After reading the public sources thoroughly, the following are **not documented**:

1. No PII / classification discipline at dream-time (Anthropic-side). What goes into the dream is whatever's in the session transcripts; what comes out is whatever the model decides to retain.
2. No operator-approval gate **before persistence**. The dream writes its output store unconditionally on success; the operator decides whether to *attach* it, not whether to *create* it.
3. No rollback primitive beyond "delete the output store." There's no "revert to previous dream" or version history of dreams over time.
4. No multi-operator / multi-tenant isolation discipline documented. (At the API tier, you get whatever workspace-level isolation Managed Agents provides.)

## 6. Production status

| Surface | Status | Access |
|---|---|---|
| **Managed Agents API — Dreams** | Research preview | Gated. Request via `claude.com/form/claude-managed-agents`. Beta header `dreaming-2026-04-21` required. |
| **Managed Agents API — Memory stores, Outcomes, Multiagent orchestration, Webhooks** | Public beta | All developers. Header `managed-agents-2026-04-01`. |
| **Claude Code Auto Dream** | Rolling out per plan tier (not officially announced) | Check `/memory` toggle. `/dream` slash command not yet fully rolled out. |

Per Build Fast with AI: "Dreaming is currently in research preview. You need to request access via the Claude Platform to use it." ([Build Fast with AI](https://www.buildfastwithai.com/blogs/claude-managed-agents-dreaming-explained))

## Quoted case study (corroborating value, not feature spec)

> "Legal AI company Harvey saw task completion rates increase roughly 6x after implementing dreaming." (multiple sources)

> "Harvey uses Managed Agents to coordinate complex legal work including long-form drafting and document creation. With dreaming enabled, their agents remember filetype workarounds and tool-specific patterns between sessions. Completion rates went up approximately 6x in their internal tests — not from a model change, but purely from the agents carrying institutional knowledge across sessions." ([Build Fast with AI](https://www.buildfastwithai.com/blogs/claude-managed-agents-dreaming-explained))

Important context for Tilth: the 6x is **completion rate**, not **quality**, and Anthropic specifically calls out *filetype workarounds and tool-specific patterns* — i.e., the dream surfaces engineering-level pattern memory, not editorial judgment.

## Documentation thinness — what's knowable vs. speculation

**Solid (primary source on Anthropic's own docs):**
- API surface and lifecycle (Dreams docs are explicit and code-sample-backed)
- Trigger model (operator-invoked API; dual-gate auto in Claude Code)
- Input/output schema at the resource level (memory_store, sessions, output memory_store)
- Safety primitives (input immutability, output discardability, fail-soft)
- Production status (research preview, gated)
- Billing model (standard API token rates against the pipeline model)
- Limits (100 sessions per dream, 4096-char instructions, two-model whitelist)

**Solid (secondary source with verbatim system-prompt evidence):**
- Four-phase prompt structure (Orient / Gather Signal / Consolidate / Prune & Index)
- Auto Dream dual-gate trigger
- 200-line MEMORY.md cap
- Lock-file concurrency control
- Narrow-grep discipline over transcripts

**Speculation / not in docs:**
- **PII handling at dream-time.** Anthropic does not describe what NOT to dream about. Inference: dreaming sees whatever the model can see in the input transcripts/store; nothing more, nothing less.
- **Cross-tenancy isolation.** Not addressed beyond workspace-level isolation inherent to Managed Agents.
- **Diff/audit primitive.** Not present in the API.
- **Whether the operator can require approval BEFORE persistence.** Build Fast with AI claims: "You can set it to update memory automatically after each session, or you can require human review before any changes land." This statement is *not* corroborated by the Anthropic docs as written — the docs describe dream output as always persisting to a new store, with operator review-then-attach being the discipline. The "require human review" framing may be marketing-paraphrase; the structural gate is the *attach* step, not the *write* step.

**Unknown / not researched this lane:**
- Memory-store schema (lives at `platform.claude.com/docs/en/managed-agents/memory` — separate fetch needed if Tilth wants to mirror)
- Outcomes-grader interaction with Dreams (Outcomes is a separate Managed Agents feature; whether dreams can use Outcomes-style rubric grading on their own output is unclear from the docs)
- The full Anthropic announcement blog post at `claude.com/blog/new-in-claude-managed-agents` — referenced by every secondary source but not in this session's web-fetch provenance set

## Tilth implications

Read against Golden Quill's Five Laws / Four Rules / classification-driven routing posture (CLAUDE.md + architecture v7.0.7 LOCKED), Anthropic's Dreaming design choices land on Tilth as follows:

### 1. Lane-2 architecture: Reflection as a separate seat or a Logician-mediated pipeline stage?

Anthropic's Dreams API treats dreaming as **a separate session running the dreaming pipeline model** — a distinct agent invocation with its own session-id and event stream. This maps cleanly to either (a) a new support agent ("Reflector") in the seat taxonomy alongside Archivist, or (b) a Logician-orchestrated Cedar gate over an existing seat's idle-time invocation. The Anthropic answer is "separate dedicated job." For Tilth that argues for **Reflector as a named support agent**, not a side-effect of another seat.

**Naming hazard:** Tilth's existing v1.x-horizon **Archivist** seat (per §15 v1 LOCKED 2026-05-10) is already specced as a between-cycle curator of the Funder Intelligence Database, Match DB, KFR, lessons memory, audit trail. Reflection-as-memory-consolidation has nontrivial overlap with what Archivist does. Two options:

- **Option A:** Subsume Reflection into Archivist's existing scope as a sub-mode (workspace-cadence Reflection + per-org-cadence Reflection). Pros: no new seat; respects §15 v1 LOCK. Cons: Archivist is "proposes-only" per its three-layer defense (AST-lint + runtime guard + Cedar policy) — Reflection writing curated memory would need the same fail-closed proposes-only discipline.
- **Option B:** Define Reflection as a new ninth-position support agent. Pros: cleaner conceptual seam matching Anthropic's API. Cons: new seat = new audit round, blast radius into §0.5, §4 Logician v2.x.

Recommend Option A as default, paired with explicit reframing: "Archivist proposes ALL memory mutations including Reflection-class. Operator approves at the boundary." Anthropic's design supports this: the dream output is *proposed* (sits in a separate store) until the operator attaches it.

### 2. Input-immutability is a load-bearing safety primitive

The Anthropic-docs-mandated "input memory store is never modified" maps directly onto Tilth's Save State Always (Rule 1) + Logician fail-closed posture. For Tilth-Reflection:

- The "live" memory state Reflection reads must be treated as read-only during the Reflection pass.
- Output goes to a *staging* path (mirror of Anthropic's separate output store) — `pipeline/reflection/staging/<run_id>/` or equivalent.
- A separate Logician gate (call it `F-REFLECTION-INPUT-MUTATED-DURING-RUN`) enforces input-immutability.
- A second gate (`F-REFLECTION-OUTPUT-AUTOAPPLIED`) prevents auto-promotion to live memory without operator approval — mirroring Anthropic's "operator attaches the output store, dream doesn't" pattern.

This is structural sovereignty, not policy — matches the architecture v7.0.7 doctrine.

### 3. The trigger model is a forcing function on classification posture

Anthropic's API tier is **operator-invoked** (no daemon). Anthropic's Claude Code tier is **dual-gate auto** (24h + >5 sessions). For Tilth's headless-only v0.1 + classification-driven routing posture, **operator-invoked is the right default** — it composes naturally with:

- Per-grant SP0 classification (operator decides per-cycle whether Reflection runs)
- The "operator clicks final submit" discipline already established for Uploader
- Law 4's apolitical-sector / admin-risk register (Reflection over confidential content has heavy F-CLASS-* implications)

Auto-trigger via dual-gate is a v0.2 horizon proposal at earliest, contingent on Classification Review wrapper + a per-org Reflection cadence policy.

### 4. Classification-driven routing applies to Reflection too

This is the load-bearing Tilth-specific implication. Reflection reads:

- Past session transcripts (almost certainly contain a mix of `public` + `shareable` + `confidential` content)
- Existing memory state (may contain Confidential facts from KFR)

Per v7.0.7 classification-driven routing: if *any* input contains `confidential` OR `operator_flagged`, **the Reflection invocation must route to local-only.** Anthropic's "claude-opus-4-7 / claude-sonnet-4-6" pipeline-model lock would be the *cloud* path; the equivalent for Tilth-Reflection is the on-demand local heavy-Judge swap pattern (200B-class local model loaded for the cycle).

Concretely:

- A `Reflection` invocation MUST run through the same per-call classification gate as Scribe/Editor/Red Team.
- Input classification = `max(classification(input_memory_store), max(classification(session) for session in input_sessions))`.
- The opaque `[SLOT_<numeric_id>]` post-fill discipline (per F-CLASS-SLOT-ID-NON-OPAQUE) extends to Reflection's input prep — slot-fill agent renders Confidential values only into the post-Reflection draft, never into the cloud-routed prompt.

### 5. The "instructions" parameter is the right primitive for per-cycle scoping

Anthropic's 4096-char `instructions` parameter — "Focus on coding-style preferences; ignore one-off debugging notes" — maps directly to Tilth's per-grant SP0. A per-cycle Reflection instructions field, signed by the operator's Ed25519 key, scoped by classification, lets Reflection do *funder-intelligence consolidation* in one cycle and *KFR maintenance* in another without conflating the two. This is the Cards-vs-Cards-resolved-at-the-visual-layer pattern again: same machinery, different cards.

### 6. The 200-line MEMORY.md cap is an interface-index discipline Tilth already has

Anthropic's "MEMORY.md is an index, not a dump — link to memory files with one-line descriptions" matches Golden Quill's existing `§0.5 Interface Index` discipline (v16 amendment LOCKED 2026-05-10 at 378 runtime-live rows). The lesson transfer:

- Tilth's lessons.md / MEMORY.md analogues should remain index-only by Reflection-time discipline, not by Reflection's enforcement. (Reflection prunes; an upstream invariant — possibly a Logician gate — refuses commits that violate the 200-line / index-only contract.)
- The current MEMORY.md "26.8KB over 24.4KB limit" warning in the user-auto-memory system is exactly the kind of drift Reflection is designed to fix on a cadence.

### 7. Cross-family review for Reflection output

The Council's Editor/Judge/Red Team are deliberately cross-family per L-003. If Reflection writes curated memory and that memory will influence future drafts, **Reflection's output should pass through at least one cross-family seat before the operator's attach step.** This is *more* discipline than Anthropic ships — Anthropic relies on operator review at attach time. Tilth's discipline could mandate a Logician PRE-attach gate that requires either (a) operator-approval signature OR (b) Editor+Red-Team review-PASS, before the staged Reflection output is allowed to displace the live memory state.

Mirrors §13/§14/§15 v0.2 SPEC-ONLY discipline: ship the seat-spec without auto-mutation; let the operator be the final attach-step actor.

### 8. What Anthropic does NOT do that Tilth must do

- **PII / admin-risk-term scanning on Reflection input.** Anthropic's Dreams sees whatever's in the session transcripts. Tilth's Law 4 (Apolitical Language + Admin-Risk Term Scanning) means Reflection over content containing flagged terms must run through the same scanner discipline as Scribe — including the operator-approves-each-substitution gate.
- **Provenance preservation.** Anthropic's dream merges duplicates but doesn't explicitly preserve per-fact provenance to the source session/document. Tilth's Intake KFR pattern is verbatim-quote-with-page provenance — Reflection MUST NOT strip that provenance during consolidation. Likely a new gate: `F-REFLECTION-PROVENANCE-STRIPPED`.
- **Audit trail.** Anthropic's dream-id + session-id is the only audit primitive. Tilth needs append-only audit-log entries for each Reflection run, signed, with input-hash + output-hash + operator-attach-decision + timestamp.

### Open questions for follow-up lanes / operator decision

1. **Reflection-as-Archivist-submode vs. Reflection-as-new-seat** — Option A vs B above; operator decision.
2. **Cadence:** Anthropic's dual-gate (24h + >5 sessions) for Auto Dream — does Tilth want time-based, count-based, or per-cycle-explicit? Per-org policy or workspace-wide?
3. **Read-back path:** Does Reflection's output displace live memory automatically once attached, or is there a "shadow Reflection memory" that Scout/Scribe consult alongside live state (mirroring Anthropic's "attach a separate store" pattern)?
4. **Memory-store schema parity:** Should Tilth's memory-store representation mirror Anthropic's API schema (in case we ever want to use Dreams-as-a-service for offline batches), or stay markdown-on-disk-only? The headless-only / sovereignty-promise constraint says markdown-on-disk; but the cross-compat is worth noting.
5. **Heavy-Judge swap analog for Reflection:** Should Reflection have an on-demand "heavy" variant — 200B-class local model loaded for end-of-quarter consolidations — analogous to the heavy-Judge swap pattern? The Anthropic answer is yes (they pick opus-4-7 for the pipeline model precisely because consolidation is non-trivial reasoning); the Tilth answer probably mirrors this.

## Sources

- **[Dreams - Claude API Docs](https://platform.claude.com/docs/en/managed-agents/dreams)** — primary API reference, code samples, lifecycle, limits, errors, billing. (canonical)
- **[Claude Code Dreams: Anthropic's New Memory Feature — claudefa.st](https://claudefa.st/blog/guide/mechanics/auto-dream)** — secondary; quotes the full Claude Code Auto Dream system prompt verbatim, four-phase structure, dual-gate trigger, safety guarantees, before/after illustration.
- **[Claude Managed Agents Dreaming Explained — Build Fast with AI](https://www.buildfastwithai.com/blogs/claude-managed-agents-dreaming-explained)** — secondary; Code with Claude 2026-05-06 launch context, Harvey/Netflix/Wisedocs/Spiral case studies, dreaming-vs-memory framing.
- **[dream-skill — grandamenium/dream-skill on GitHub](https://github.com/grandamenium/dream-skill)** — third-party community replica of Auto Dream as a Claude Code skill; confirms trigger model, four-phase structure, hook pattern.
- **[Anthropic introduces "dreaming" — VentureBeat (search result, full URL not in provenance set)](https://venturebeat.com/technology/anthropic-introduces-dreaming-a-system-that-lets-ai-agents-learn-from-their-own-mistakes)** — surfaced via web search, contains the "not changing model weights" quote from Anthropic's Aaron Albert; cited from search-results summary, not direct page fetch.
- **Referenced but not fetched this lane:**
  - `claude.com/blog/new-in-claude-managed-agents` — official Anthropic announcement post (not in provenance set)
  - `platform.claude.com/docs/en/managed-agents/memory` — Memory Stores API reference (schema details for lane reuse)
  - `simonwillison.net/2026/May/6/code-w-claude-2026/` — Simon Willison's live blog of the launch event (cited by Build Fast with AI)

---

**Filed:** 2026-05-10, lane 2 of 5. No code edits. No LOCK ceremony. Hand-back to operator for synthesis with lanes 1, 3, 4, 5.
