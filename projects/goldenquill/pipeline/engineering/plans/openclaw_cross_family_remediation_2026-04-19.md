# OpenClaw Cross-Family Audit — Remediation Plan

**Date:** 2026-04-19
**Author:** Plan subagent (Opus) — Anthropic family
**Status:** Ready for execution; awaiting operator go-ahead
**Context:** Designs the permanent fix for Tilth L-003 cross-family audit via OpenClaw 2026.4.14 on Josh's M1 Mac Mini. All CLI verbs + flags quoted from live `--help` output captured 2026-04-19, not invented.

---

## A. Root cause

**The override is rejected because `agents.defaults.models` in `~/.openclaw/openclaw.json` currently contains exactly one entry: `anthropic/claude-sonnet-4-6`. Per OpenClaw docs, when that field is set it becomes the allowlist for `/model` and for session overrides. Any `--model groq/...` falls outside that allowlist, so the CLI refuses before any HTTP call is made.**

Evidence chain:
- Live config excerpt (keys redacted): `"agents": { "defaults": { ..., "models": { "anthropic/claude-sonnet-4-6": { "alias": "scribe" } } }, "list": [{ "id": "tilth", ..., "model": "anthropic/claude-sonnet-4-6" }] }`
- `openclaw config get agents.defaults.models` returns `{ "anthropic/claude-sonnet-4-6": { "alias": "scribe" } }`
- `OPENCLAW_AGENT_DIR=.../tilth/agent openclaw infer model auth status` reports `"allowed": ["anthropic/claude-sonnet-4-6"]`
- Docs (`openclaw docs "agent model override allowlist"` and `/concepts/models#model-is-not-allowed-and-why-replies-stop`): *"If `agents.defaults.models` is set, it becomes the allowlist for `/model` and for session overrides."*
- Error text observed: `Error: Model override "groq/llama-3.3-70b-versatile" is not allowed for agent "tilth".` — exact match to documented failure.

**Secondary:** The `tilth` per-agent block (`agents.list[0]`) has no `models` field, so it inherits `agents.defaults.models` as its allowlist. No narrower per-agent allowlist is fighting us.

**Non-findings (NOT the root cause):**
- `~/.openclaw/agents/tilth/agent/models.json` is the `models.providers` shape — custom provider endpoints registered with the agent, NOT an allowlist. Groq is a bundled plugin loaded from `~/.npm-global/lib/node_modules/openclaw/dist/extensions/groq/` and does not need an entry there. **Prior hypothesis of "edit models.json to add Groq block" is wrong.**
- `GROQ_API_KEY` is already readable: `openclaw infer model auth status` reports `"provider": "groq", "effective": {"kind": "env", ...}, "source": "env: GROQ_API_KEY"`. Key pipeline works.
- `plugins.google` is `"enabled": false`; does not affect Groq.

---

## B. Options evaluated

### Option 1 — Extend global allowlist in `openclaw.json` (RECOMMENDED component)

```
openclaw config set 'agents.defaults.models["groq/llama-3.3-70b-versatile"]' '{}' --strict-json
openclaw config set 'agents.defaults.models["groq/qwen/qwen3-32b"]' '{}' --strict-json
openclaw config set 'agents.defaults.models["groq/openai/gpt-oss-120b"]' '{}' --strict-json
```

**Pros:** canonical per-docs path. Minimal surface change. Reversible with `openclaw config unset`. No daemon restart known to be required.
**Cons:** widens allowlist globally; future agents inheriting defaults get Groq access too.
**Reversibility:** high — each added key removable via `openclaw config unset`.
**Risk:** low. Config write atomic; `.bak` rotation observed in `~/.openclaw/`.

### Option 2 — Per-agent scoping via `agents.list[].models`

Same `config set` pattern under `agents.list[0].models.<key>`. Index-based addressing is brittle if `agents.list` reorders. Docs suggest `agents.list[].models` replaces defaults non-merging — risk of accidentally stripping `anthropic/claude-sonnet-4-6` primary if forgotten.
**Rejected:** adds fragility (array index) without meaningful isolation gain (one agent today).

### Option 3 — Dedicated `auditor` agent

```
openclaw agents add auditor --workspace /Users/goldenquill/Downloads/GoldenQuill \
  --model groq/llama-3.3-70b-versatile --non-interactive --json
```

**Pros:** clean role separation.
**Cons:** audit seats are Tilth's seats per `router.yaml`; splitting into a sibling agent contradicts document of record. Scripts forget `--agent auditor`. Doesn't solve allowlist problem on its own.
**Rejected:** solves an identity-separation problem Tilth doesn't have; adds orchestration burden.

### Option 4 — Model aliases for role names (RECOMMENDED component)

```
openclaw models aliases add editor   groq/llama-3.3-70b-versatile
openclaw models aliases add judge    groq/qwen/qwen3-32b
openclaw models aliases add red_team groq/openai/gpt-oss-120b
```

**Pros:** scripts use `--model editor` etc., matching `router.yaml` seat names. Self-documenting.
**Cons:** aliases don't bypass allowlist — must combine with Option 1.
**Risk:** none on its own.

### Option 5 — Clear allowlist entirely

`openclaw config unset agents.defaults.models`. Policy regression. **Rejected on principle.**

### Docs-surfaced features worth knowing

- `openclaw config set --batch-file` + `--batch-json` — atomic multi-key write
- `openclaw config set --dry-run` — validates batch without writing
- `openclaw models fallbacks add` — global fallback chain (not needed here; `router.yaml` handles seat-level fallback)

---

## C. Recommended path

**Option 1 + Option 4, applied as a single atomic batch via `openclaw config set --batch-file`.**

Justification:
- Matches docs' canonical remedy verbatim
- Atomic batch minimizes half-modified-config window if gateway hot-reloads
- Aliases give scripts the role-name handles `router.yaml` already uses
- No new agent; `agents.list` untouched

---

## D. Concrete command sequence

### D.0 Pre-flight (read-only)

```
openclaw config file
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.pre-groq-allowlist-$(date -u +%Y%m%dT%H%M%SZ)

openclaw health

openclaw config get agents.defaults.models --json
OPENCLAW_AGENT_DIR=/Users/goldenquill/.openclaw/agents/tilth/agent \
  openclaw infer model auth status 2>&1 | grep -A 6 '"provider": "groq"'

openclaw infer model inspect --model groq/llama-3.3-70b-versatile --json
openclaw infer model inspect --model groq/qwen/qwen3-32b --json
openclaw infer model inspect --model groq/openai/gpt-oss-120b --json
```

### D.1 Dry-run the batch

```
cat > /tmp/openclaw-cross-family-allowlist.batch.json <<'EOF'
[
  { "path": "agents.defaults.models[\"groq/llama-3.3-70b-versatile\"]", "value": {} },
  { "path": "agents.defaults.models[\"groq/qwen/qwen3-32b\"]",          "value": {} },
  { "path": "agents.defaults.models[\"groq/openai/gpt-oss-120b\"]",     "value": {} }
]
EOF

openclaw config set --batch-file /tmp/openclaw-cross-family-allowlist.batch.json --dry-run --strict-json
openclaw config validate --json
```

### D.2 Apply the batch

```
openclaw config set --batch-file /tmp/openclaw-cross-family-allowlist.batch.json --strict-json
openclaw config validate --json
```

### D.3 Register role-name aliases

```
openclaw models aliases add editor   groq/llama-3.3-70b-versatile
openclaw models aliases add judge    groq/qwen/qwen3-32b
openclaw models aliases add red_team groq/openai/gpt-oss-120b
openclaw models aliases list --plain
```

### D.4 Re-verify

```
openclaw health
openclaw config get agents.defaults.models --json
OPENCLAW_AGENT_DIR=/Users/goldenquill/.openclaw/agents/tilth/agent \
  openclaw infer model auth status 2>&1 | grep -E '"allowed"' -A 6
```

Expected `allowed`:
```
["anthropic/claude-sonnet-4-6",
 "groq/llama-3.3-70b-versatile",
 "groq/qwen/qwen3-32b",
 "groq/openai/gpt-oss-120b"]
```

---

## E. Rollback procedure

**Scenario 1 — schema validation fails or sanity check fails:**
```
cp ~/.openclaw/openclaw.json.bak.pre-groq-allowlist-<timestamp> ~/.openclaw/openclaw.json
openclaw config validate --json
openclaw health
```

**Scenario 2 — targeted rollback of just the three entries:**
```
openclaw config unset 'agents.defaults.models["groq/llama-3.3-70b-versatile"]'
openclaw config unset 'agents.defaults.models["groq/qwen/qwen3-32b"]'
openclaw config unset 'agents.defaults.models["groq/openai/gpt-oss-120b"]'
openclaw models aliases remove editor
openclaw models aliases remove judge
openclaw models aliases remove red_team
openclaw config validate --json
```

**Scenario 3 — gateway unresponsive:**
```
openclaw health
openclaw logs   # tail via RPC
# If unhealthy AND config is suspect: restore .bak from Scenario 1.
# DO NOT call `openclaw reset` (destroys state).
# DO NOT blindly restart LaunchAgent — escalate to operator.
```

---

## F. Post-fix validation

Three one-shot calls, one per `router.yaml` audit seat:

```
# Editor (Meta family)
openclaw infer model run --gateway \
  --model groq/llama-3.3-70b-versatile \
  --prompt "Respond with the single word OK so I can confirm reachability." \
  --json

# Judge (Alibaba family)
openclaw infer model run --gateway \
  --model groq/qwen/qwen3-32b \
  --prompt "Respond with the single word OK so I can confirm reachability." \
  --json

# Red Team (OpenAI-OSS family)
openclaw infer model run --gateway \
  --model groq/openai/gpt-oss-120b \
  --prompt "Respond with the single word OK so I can confirm reachability." \
  --json
```

Alias-form equivalent:
```
openclaw infer model run --gateway --model editor   --prompt "ping" --json
openclaw infer model run --gateway --model judge    --prompt "ping" --json
openclaw infer model run --gateway --model red_team --prompt "ping" --json
```

Failure diagnostics:
- `Error: Model override ... is not allowed` → allowlist write didn't land. Re-check §D.4.
- 401 / auth error → `GROQ_API_KEY` delivery issue. Either ensure shell env has it, or use `--gateway` to route via daemon (daemon has the key from its LaunchAgent env).

---

## G. Risks identified

1. **Hot-reload vs. daemon restart.** Docs did not state definitively whether `agents.defaults.models` is hot-reloaded. `.bak` rotation suggests OpenClaw routinely rewrites config while gateway is live, so it *should* observe its own writes. Smoke test will reveal a stale cache immediately. Mitigation if stale: escalate to operator — this plan does NOT authorize LaunchAgent reload.
2. **Race on `openclaw.json` write.** CLI and gateway both mutate this file. `--batch-file` applies atomic write. Don't hand-edit during the same minute.
3. **Allowlist widening.** Option 1 widens globally. Future second agent inherits Groq. Acceptable today; flag in handoff docs.
4. **Alias collision.** `editor`, `judge`, `red_team` are common. Alias list is flat and global. Low risk today. Mitigation: track aliases under change control.
5. **Key delivery for non-gateway CLI.** Without `--gateway`, calls may execute locally using invoking shell's env. If shell lacks `GROQ_API_KEY`, 401 ensues. Mitigation: always pass `--gateway` for audit invocations.
6. **`shellEnvFallback.enabled: false` observed.** `GROQ_API_KEY` resolves from process env, not shell profile import. Not a bug; be aware.
7. **`agents.list[0].model` must stay as `anthropic/claude-sonnet-4-6`.** Scribe primary. Do NOT change it as part of this fix.
8. **Orphan agent dirs.** `openclaw doctor` flagged 2 orphans (`main`, `mycosymbiotics`) without `agents.list` entries. Unrelated to this fix; separate cleanup. Use `OPENCLAW_AGENT_DIR=.../tilth/agent` explicitly OR `--gateway` to avoid orphan-dir resolution.

---

## H. Handoff-doc patches

The two existing handoff files reference an `openclaw infer --provider groq --model X` form that does not exist in 2026.4.14. Replace their CLI blocks with:

```markdown
## Cross-family audit — CLI invocation (OpenClaw 2026.4.14)

Real command shape (as of 2026.4.14, verified 2026-04-19):

    openclaw infer model run --model <provider/model> --prompt <text> [--json] [--gateway]

The `--provider` flag referenced in AGENTS.md is obsolete in 2026.4. The
`--model` value carries the provider prefix.

Seat-to-model mapping (source of truth: router.yaml):

| Seat      | Family      | Model id                           | Alias      |
|-----------|-------------|------------------------------------|------------|
| Editor    | Meta        | groq/llama-3.3-70b-versatile       | editor     |
| Judge     | Alibaba     | groq/qwen/qwen3-32b                | judge      |
| Red Team  | OpenAI-OSS  | groq/openai/gpt-oss-120b           | red_team   |

Canonical invocations (use `--gateway` to reuse the daemon env):

    openclaw infer model run --gateway --model editor   --prompt "<text>" --json
    openclaw infer model run --gateway --model judge    --prompt "<text>" --json
    openclaw infer model run --gateway --model red_team --prompt "<text>" --json

Equivalent without aliases:

    openclaw infer model run --gateway --model groq/llama-3.3-70b-versatile --prompt "<text>" --json
    openclaw infer model run --gateway --model groq/qwen/qwen3-32b          --prompt "<text>" --json
    openclaw infer model run --gateway --model groq/openai/gpt-oss-120b     --prompt "<text>" --json

Prerequisite: `agents.defaults.models` in ~/.openclaw/openclaw.json must
include the three Groq model ids. Verify with:

    openclaw config get agents.defaults.models --json

Prerequisite: `GROQ_API_KEY` in gateway LaunchAgent env. Verify:

    openclaw infer model auth status 2>&1 | grep -A 4 '"provider": "groq"'
```

---

## Discrepancies flagged

1. **AGENTS.md `--provider` flag is obsolete.** Separate change: update AGENTS.md to the real CLI shape. Not blocking this fix.
2. **Earlier theory ("edit models.json to add Groq block") was wrong.** `models.json` is custom-providers, NOT allowlist. Plan corrects the theory.
3. **`openclaw docs` is powerful.** Worth using as a permanent investigation tool.

---

## Critical Files for Implementation

- `/Users/goldenquill/.openclaw/openclaw.json` — the allowlist lives here (NOT in `models.json`)
- `/Users/goldenquill/Downloads/GoldenQuill/router.yaml` — source of truth for seat → model
- `/Users/goldenquill/.openclaw/agents/tilth/agent/models.json` — custom providers (codex + ollama); untouched by this plan
- `/Users/goldenquill/Downloads/GoldenQuill/pipeline/engineering/handoffs/openclaw_cross_family_audit_agent_sdk_2026-04-19.md` — needs CLI block replacement per §H
- `/Users/goldenquill/Downloads/GoldenQuill/pipeline/engineering/handoffs/openclaw_cross_family_audit_tsip_v0.1_2026-04-19.md` — needs CLI block replacement per §H
