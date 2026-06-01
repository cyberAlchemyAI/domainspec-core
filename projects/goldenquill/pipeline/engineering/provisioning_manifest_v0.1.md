# Tilth v0.1 Provisioning Manifest

**Status:** LIVE document. Updated at every LOCK that adds a new dependency, external service, key, or install step. Every Golden Quill provisioning run (white-glove setup) reads this as the canonical install-and-configure checklist.

**Scope:** Everything required to stand up Tilth v0.1 from scratch on a supported machine tier. Everything referenced, downloaded, bought, linked, keyed, credentialed. If it's needed at runtime, install time, or calibration time, it's listed here.

**Update discipline:** Any module LOCK that changes this manifest (new dep, new service, new key surface) writes the delta to §11 changelog AND updates the relevant §1-§10 table row. Missing a manifest update is a process violation caught by the committee review of the LOCKing PR.

---

## 1. Hardware tiers

From v7 amendment A1 (hardware triple-target). All tiers share the same software stack; tier-specific calibration per A7.3.

| Tier | Hardware | RAM floor | OS | Purpose |
|---|---|---|---|---|
| **Pro** | NVIDIA DGX Spark (Grace Blackwell) | 128 GB | Linux (Ubuntu 24.04+) / CUDA stack | Primary production for clients who prefer NVIDIA |
| **Pro (secondary)** | Apple Mac Studio | 128 GB | macOS 14+ | Alternate production for Mac-native clients |
| **Baseline** | Apple Mac Studio | 128 GB | macOS 14+ | Standard client deployment |
| **Dev** | Apple M1 Mac Mini | 8 GB | macOS 14+ | Josh's dev node; dogfood gate |

**128 GB is the Golden Quill floor per CLAUDE.md retirement of 64 GB and 32 GB references (2026-04-18).** Dev tier is intentionally under-provisioned so "runs clean on Dev" is the ship gate — if it flies on 8 GB it flies on 128 GB.

---

## 2. OS baseline

### 2.1 macOS tiers (Pro-secondary / Baseline / Dev)
- macOS 14.0+ (Sonoma or newer).
- Xcode Command Line Tools — `xcode-select --install`.
- Homebrew — `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`.

### 2.2 Linux tier (Pro / DGX Spark)
- Ubuntu 24.04 LTS (or equivalent glibc ≥ 2.38 distro).
- `build-essential`, `git`, `curl`, `jq`, `flock` (util-linux default).
- Kernel ≥ 5.6 (for `openat2(RESOLVE_NO_*)`) — blueprint §8 `LINUX_KERNEL_FLOOR_VERSION`.
- Filesystem: `apfs` (macOS) / `ext4` / `btrfs` / `zfs` / `xfs` with stable volume UUID. Blueprint §5.1 rejects `tmpfs`, `overlayfs` (except signed-allowlist), `fuse.*`, `hfs+`, `ntfs`, `vfat`, `nfs`, `cifs`, `smb`.

---

## 3. Python runtime

### 3.1 Version floor
- **Python 3.11+** required (per blueprint §5.1 "native in Python 3.11 stdlib" SHA-3-512 + per `@dataclass(kw_only=True)` 3.10+ requirement).
- Current dev node: Python **3.14.4** via `/opt/homebrew/bin/python3.14` — install with `brew install python@3.14`.

### 3.2 Virtual environment
- Project-local venv at `.venv/` — `python3.14 -m venv .venv`.
- Activate: `source .venv/bin/activate` OR use `.venv/bin/python` directly.
- Not committed to git; recreate per fresh install.

### 3.3 Python packages (installed via pip into the venv)

| Package | Version floor | Purpose | Required at |
|---|---|---|---|
| `pip` | latest | package management | install |
| `pytest` | ≥ 8.0 | test runner | dev |
| `pytest-cov` | ≥ 5.0 | coverage | dev |
| `cryptography` (future) | TBD | AES-GCM in `crypto_primitives.py` round B | §4.6 M7 |
| `pyyaml` (future) | TBD | router.yaml parsing in `router_integrity.py` | §4.4 M5 |
| `cedarpy` OR equivalent (future) | TBD | Cedar runtime for Section 4 Logician | v7 A2/A3 |
| `tomli_w` (future) | TBD | pyproject.toml editing from tools | maybe |
| `httpx` OR `urllib3` (future) | TBD | HTTP client for Scout live-synopsis fetch | Section 3 |
| `feedparser` | ≥ 6.0 | Scout Channel E RSS parse (`_feedparser_adapter.py` lazy import) | §4.5 Round 6 |
| `idna` | ≥ 3.0 | Scout Channel F Punycode/UTS46 normalisation (`channel_f_websearch.py` lazy import inside `_registrable_domain`) — A-14 IDN homograph defence | §4.6 Round 7 |

Runtime deps list is SMALL by design. Every addition justified by a blueprint section reference.

**Install command (v0.1 current surface, from repo root):**
```bash
/opt/homebrew/bin/python3.14 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[dev]"
```

`-e .` installs the tilth package in editable mode so code edits are immediately visible without reinstall.

### 3.4 Test framework verification
```bash
.venv/bin/python -m pytest tests/ -v
```
Expected output (as of 2026-04-19 Window-1): `88 passed in 0.06s`.

---

## 4. LLM providers + BYOK API keys

Every provider is **BYOK — client-owned keys, never Sovereign-Node-LLC-managed.** Keys live in `~/.openclaw/.env` on the operator's machine and nowhere else. No cross-client key sharing, no dev/prod sharing, no Cowork/OpenClaw sharing.

### 4.1 Key surfaces per router.yaml

| Env var | Provider | Purpose | Where to obtain |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | Anthropic | Scribe primary (Claude Sonnet 4.6); Scribe escalation (Opus 4.6); code_author (Claude Code) | console.anthropic.com → API Keys |
| `GROQ_API_KEY` | Groq | Editor (Llama 3.3 70B); Judge (Qwen 3 32B); Red Team (GPT-OSS 120B); code_reviewer_2/3/4; Scout fallback (Llama 3.1 8B Instant) | console.groq.com → API Keys; Dev tier ($20/mo) covers v0.1 dev workload |
| `OPENAI_API_KEY` | OpenAI | code_review fallback (GPT-4o); code_reviewer_1 (Codex); Editor fallback (GPT-4o-mini) | platform.openai.com → API Keys |
| `GOOGLE_API_KEY` | Google | Judge fallback (Gemini 2.5 Pro); Reasoner Review (Gemini 2.5 Pro) | aistudio.google.com → Get API Key |
| `BRAVE_SEARCH_API_KEY` | Brave | Scout channel family F (client-material-driven web search) — BYOK default, 2000 q/month free tier | api.search.brave.com |
| `MOONSHOT_API_KEY` | Moonshot | code_reviewer_5 (Kimi K2) | platform.moonshot.ai |

### 4.2 .env format
```
# ~/.openclaw/.env — permission mode 0o600 recommended
ANTHROPIC_API_KEY=sk-ant-...
GROQ_API_KEY=gsk_...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
BRAVE_SEARCH_API_KEY=BSA...
MOONSHOT_API_KEY=sk-...
```

Read by `pipeline/validation/blueprint_option_b_design_2026-04-18/dispatch_round3_v3.py` et al. via simple line-parse (not python-dotenv dep). Keys are **never logged** per §4.10.7.9 token non-logging discipline (applies generally to all credentials).

### 4.3 Key rotation
Per A12.7 crypto-agility commitment, every long-lived credential has a rotation path. API key rotation is provider-controlled (console re-issue); local .env update propagates instantly (no daemon restart required at v0.1).

### 4.4 Cost posture (v0.1 dev)
- **Anthropic:** metered. Scribe drafting dominates costs; typical grant draft consumes $2-15 depending on revision count.
- **Groq Dev tier ($20/mo):** covers Scout (if cloud fallback fires) + Editor + Judge + Red Team + 3 of 5 code reviewers. Rate-limited; hitting ceiling triggers provider-cascade to Anthropic escalation paths.
- **OpenAI:** low volume for code reviewers; $0-5/grant.
- **Google:** low volume for fallbacks; $0-2/grant.
- **Brave Search:** free tier (2000 q/month) sufficient for a single-operator workload.
- **Moonshot:** 1 reviewer slot; $0-2/grant.

**Typical per-grant v0.1 BYOK cost estimate: $5-25 depending on complexity + revision count.**

---

## 5. Local models (Ollama)

Scout's DISCOVER stage runs LOCAL on `mistral:7b` via Ollama per router.yaml — sovereign + zero API cost for the high-volume Monday-cron discovery loop.

### 5.1 Ollama install
```bash
brew install ollama                    # macOS
# OR download from ollama.com for Linux
```

### 5.2 Models to pull
```bash
ollama pull mistral:7b                 # Scout primary (confirmed 2026-04-14: 0.20.6 on M1 8GB)
```

### 5.3 Runtime
- `ollama serve` daemon (LaunchAgent on macOS, systemd on Linux).
- Listens on `127.0.0.1:11434` by default.
- Scout cloud fallback (`groq/llama-3.1-8b-instant`) fires when ollama daemon is down.

### 5.4 Model storage
- `~/.ollama/models/` on macOS. ~4.5 GB for `mistral:7b`.

---

## 6. Operator keys + signing

### 6.1 Operator keyring (macOS Keychain)
Per Section 1 v6 `keys.py` — `MacOSKeychainKeyStore` is the v0.1 default on macOS tiers. Keys live in the login keychain; never in plaintext files on disk.

### 6.2 Key types held

| Key | Purpose | Algorithm at v0.1 | A12 migration target |
|---|---|---|---|
| `operator.signing.ed25519.v1` | Signs operator-signed artifacts (M15 ledger, BT7 claim-evidence, BT13 rails report, N.4.2 trust-root mirror, A7.3 machine-calibration, A9 Commons upload) | Ed25519 | v0.2 hybrid Ed25519 + ML-DSA-65; v0.3 pure ML-DSA-65 |
| `router.signing.hmac.v1` | HMAC-signs router.yaml canonical bytes | HMAC-SHA3-512 (256-bit key) | symmetric — stays as-is through v0.3 |
| `admin_risk.ledger.hmac.v1` | HMAC-signs admin-risk ledger trailer per-rotation | HMAC-SHA3-512 | stays as-is |
| `degradation.log.hmac.v1` | HMAC-signs degradation log per §5.6 BT8 | HMAC-SHA3-512 | stays as-is |
| `m7.session.hmac.{session_id}` | Per-session HMAC for health-tuple signing per §4.6 | HMAC-SHA3-512, ephemeral | stays as-is |
| `fd_broker.hmac.{seat}.{conn}` | Per-connection broker auth per §8 `FD_BROKER_HMAC_KEY_LENGTH_BYTES=32` | HMAC-SHA-256 | may upgrade to HMAC-SHA3-256 v0.2 |

### 6.3 Key-provisioning at white-glove setup
```bash
tilth provision operator-key              # generate operator.signing.ed25519.v1; store in keychain
tilth provision router-hmac-key           # generate router.signing.hmac.v1; sign router.yaml
tilth provision machine-calibration       # A7.3 white-glove bench + sign calibration.v1.json
```

*(These commands are STUBS at Section 1 Round-A LOCK. Implementation lands in later rounds. White-glove flow assumes these exist by Section 1 full-LOCK.)*

---

## 7. On-disk layout (operator-owned)

### 7.1 Repository root
- `/Users/<operator>/<project-dir>/` on macOS (Josh's: `/Users/goldenquill/Downloads/GoldenQuill/`).
- Contains `pipeline/`, `orgs/`, `vault_shared/` (when initialized), `tests/`, `.venv/`, `.openclaw/` symlink, etc.
- **NOT a git repository per L-006** — enforcement is internal via Option-B compound-txn, not external via signed commits.

### 7.2 Operator config
- `~/.openclaw/.env` — BYOK keys per §4.
- `~/.openclaw/agents/` — OpenClaw agent configurations.
- `~/.openclaw/logs/` — daemon logs.
- `~/.mempalace/` — MemPalace v3.1.0 vector store (ChromaDB) for OpenClaw MCP integration.

### 7.3 OpenClaw daemon (external tool — Josh's dev stack)
- OpenClaw installed with LaunchAgent daemon.
- Dashboard at http://127.0.0.1:18789.
- Provides the seat-dispatch infrastructure Claude-family seats (Scribe) ride on.
- Per CLAUDE.md as of 2026-04-14.

### 7.4 Vault layout per org (created on first session for that org)
- `orgs/{slug}/PROJECT_CONTEXT.md` — operator-authored; no `[NEEDED]` tokens at pipeline start.
- `orgs/{slug}/vault/init.marker` — BT14.a per-org init marker (signed).
- `orgs/{slug}/vault/claim_evidence/` — §4.10.4 SIMPLE `claim-evidence-write` target.
- `orgs/{slug}/vault/admin_risk/ledger.jsonl` — §4.10.4 SIMPLE `admin-risk-append` target (and A8 `index-amendment` COMPOUND target per §4.10.5).
- `orgs/{slug}/vault/conversation_log/` — §4.10.4.
- `orgs/{slug}/vault/rails_reports/` — §4.10.4.
- `orgs/{slug}/vault/lessons_delta/` — §4.10.4.
- `orgs/{slug}/vault/rfa/` — A8 RFA ingest store.
- `orgs/{slug}/vault/.write.lock` — Section 2 v7.1 §4.10.7 path-level advisory lock.
- `orgs/{slug}/vault/.compound_txn.lock` — Section 2 v7.1 §4.10.7 staging-dict lock.

### 7.5 Shared vault (operator-wide)
- `vault_shared/section_02.lock.json` — §2 Section 2 lock marker.
- `vault_shared/process_wrappers/` — signed seat launcher wrappers (Section 2 §4.5).
- `vault_shared/sandbox_profiles/` — macOS SBPL per seat kind.
- `vault_shared/seccomp_filters/` — Linux BPF bytecode per seat kind.
- `vault_shared/cached_opportunities/` — Scout channel B cache (mutable).
- `vault_shared/research_db/` — mutable research DB index (seed at `/seed/`).
- `vault_shared/sources/` — M15-signed source material references.
- `vault_shared/rubrics/` — Judge rubric library.
- `vault_shared/rubrics/rfa_dissection_quality.v1.json` — A8.1.e fixed dissection verification rubric (OD-2 resolution).
- `vault_shared/machine_calibration.v1.json` — A7.3 signed calibration output.

### 7.6 Trust-root mirror (operator-wide)
- `~/.tilth/logician_trust_root/router.yaml` — mirror of repo-root router.yaml, `chattr +i` / `chflags uchg`.
- `~/.tilth/logician_trust_root/manifest.json` — TrustRootMirrorManifest.
- `~/.tilth/logician_trust_root/manifest.sig` — operator signature.

---

## 8. External services (client interacts with; Golden Quill never phones home without consent)

### 8.1 Grants.gov (Scout channel family A primary)
- `search2` + `fetchOpportunity` JSON APIs.
- Free; no API key required.
- Rate-limited; Scout respects per-call timing.

### 8.2 SAM.gov (Scout channel family A)
- API key required — grants.gov and SAM.gov link via UEI.
- Env var: `SAM_GOV_API_KEY` (future surface — register at sam.gov/APIs).

### 8.3 USASpending.gov (Scout channel family A)
- Free public API; no key.

### 8.4 Brave Search API (Scout channel family F)
- Key per §4.1.
- Free tier 2000 q/month.

### 8.5 v0.2 Commons transports (A9.6 / A10 / A11 / A12.6 — NOT YET ACTIVE)
- **IPFS** — content-addressed primary.
  - Install: `brew install ipfs` OR `go-ipfs` binary.
  - Daemon: `ipfs daemon`.
  - SN-LLC pinning service endpoint: TBD (registered at v0.2 ship).
- **GitHub mirror** — secondary high-availability fallback.
  - Repo URL: TBD (registered at v0.2 ship under FIT Farms Commons GitHub org).
  - Signed content only; same bytes, same operator signature as the IPFS primary.

### 8.6 Post-quantum crypto libraries (v0.2+ per A12)
- **oqs-python** OR `liboqs` via direct FFI (for ML-DSA-65 / Kyber).
  - Current status: NOT YET INSTALLED; v0.1 uses Ed25519 + SHA-3 stdlib only.
  - v0.2 install command (TBD): `pip install oqs-python` OR equivalent.

---

## 9. Data artifacts (downloaded / seeded / versioned)

### 9.1 Seed corpus (ships with Tilth v0.1)
- `pipeline/institutional_memory/lessons.json` — machine-readable lessons (mirror of `/lessons.md`).
- `vault_shared/rubrics/vapg_fy26.json` — VAPG FY26 extracted rubric (100 pts, 7 criteria).
- `vault_shared/rubrics/rfa_dissection_quality.v1.json` — A8.1.e fixed dissection verification rubric (authored at v7 LOCK).
- `pipeline/institutional_memory/admin_risk_register.yaml` — 18 flagged-term entries per Law 4 axis 2.
- `Sovereign_Node_Handoff/prior_work/` — Grant GPT prompts, 90+ Rubric, funder databases (migrated at v0.1 init).

### 9.2 Seed reference databases
- `vault_shared/research_db/seed/` — signed read-only seed (M15-committed).
- `Funders_Master_PA_NY_NJ_2025_2026_DEDUPED.xlsx` — cached funder dataset referenced in lessons L-001.

### 9.3 Runtime-mutable caches
- `vault_shared/cached_opportunities/` — Scout channel B storage.
- `~/.mempalace/` — MemPalace v3.1.0 vector store (ChromaDB 1.5.7).
- `~/.ollama/models/` — Ollama local model cache.

### 9.4 Versioned artifact paths (schema versioning per engineering_process_v0.1.md §4.2)
- All on-disk artifacts use `<name>.v<N>.<ext>` pattern. Blueprint §0.5 Interface Index v3 is the reference.

---

## 10. Optional tooling (developer convenience, not required)

### 10.1 Code quality
- `ruff` — fast Python linter/formatter. `.venv/bin/python -m pip install ruff`. Future AST-lint enforcement hook per engineering_process_v0.1.md §4.10.
- `mypy` — static type checker. `pip install mypy`.
- `scripts/run_lint.sh` — pinned-interpreter wrapper around `python3 -m pipeline.linting.ast_lint`. Enforces the seven AST-lint rules across `pipeline/`: ARCH-04 R1 LOGICIAN_IMPORT_BAN, R2 LOOP_LOGICIAN_BAN, R3 LOGICIAN_OPEN_BAN, R4 SCOUT_NO_SETATTR_OPERATOR_DECISION, R5 SCOUT_NO_EVAL; ARCH-05 R6 AST_NO_INDIRECT_VAULT_READ (per-module alias walker with `_MAX_ALIAS_WALKER_STEPS=1000` fail-closed), R7 AST_PREFLIGHT_DOMINATES_FD_REQUEST (module-scope `typing.Final[bool]` literal-init sentinel must CFG-dominate every `fd_broker.request(...)` sink under `pipeline/loop/**` + `pipeline/scout/channel_f_*.py`; cross-module sentinel resolution bounded to `pipeline.{scout,section_02,loop,logician}`). Exits 0 on clean, 1 on any violation with `{file}:{line}:{col}: {RULE} [{reason_tag}] {message}` listing on stderr, 2 on env error (missing venv / Python < 3.11). Mirrors the `scripts/run_tests.sh` pattern.

### 10.2 Token-efficiency tools
- `RTK v0.35.0` — token compression (per CLAUDE.md infrastructure line).
- Prompt-cache checks at committee dispatch per engineering_process_v0.1.md §6.

### 10.3 Editor integrations
- VSCode: Python + Pylance extensions.
- Cursor / Zed: same ecosystem.
- Josh uses Cowork / Claude Code CLI — no IDE required.

---

## 11. Changelog

- **2026-04-20 Scout Round 7 Channel F delta** — adds `idna>=3.0` (§3.3) as the single import site `pipeline/scout/channel_f_websearch.py` lazy-loaded inside `_registrable_domain` for UTS46 Punycode normalisation (A-14 IDN homograph defence). No new external services; Brave Search API (§8.4) surface pre-existing. No new key surface.
- **2026-04-19 v1 LOCKED** as the first Window-1 capstone. Captures everything provisioned for Round A (crypto_primitives + org_slug LOCKed 88/88 tests green). Covers Python 3.14 venv setup, pytest install, BYOK key surfaces, router.yaml Code Thesis Committee backfill, provisional on-disk layout references per Section 1 v6 and Section 2 v7.1 blueprints.

**Delta list for future LOCKs that must touch this manifest:**
- Round B (audit.py + topology.py) — no new deps expected; may add log-rotation policy.
- Round C (keys.py) — may add `cryptography` library for AES-GCM; update §3.3 + §6.2.
- Section 2 Round (Vault) — adds `fcntl` usage notes + lock-file paths (stdlib only).
- Section 3 Round (Scout) — adds HTTP client dep + SAM.gov API key + Brave Search integration.
- Section 4 Round (Logician) — adds Cedar runtime dep choice.
- v0.2 Commons — adds IPFS + GitHub mirror infra; adds oqs-python for A12 crypto.
