---
title: v0.1 Beta Deployment Runbook — Josh's Mac (operator dev node)
filed: 2026-05-15
operator: Josh Inklovich
authority:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md (v7 A1–A12 LOCKED 2026-04-19 + v7.0.x amendment line through v7.0.10)
  - pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md (current clearance bar)
  - docs/v0_1_TECHNICAL_LEAD_BRIEF.md (what v0.1 must do)
  - docs/white_glove_v0_1_beta.md (operator-facing white-glove playbook)
scope: Step-by-step deployment of a fully functional v0.1 Beta on the operator's Mac. Verify substrate, build Golden Image deps, configure BYOK envelope, populate test org, run end-to-end submission_mode smoke, bring up observability, hand to operator for portal final-submit.
non-goals:
  - First-customer Beta cut (this runs on Josh's dev node; client deployments derive a per-deployment router from the signed Golden Quill router-template release)
  - v0.2 work (Data Collector runtime / Report Generator runtime / Cultivator / Stage-5 commons)
  - UI buildout (apps/tilth_demo_v0/ is dogfood scaffold, not v0.1 surface)
---

# v0.1 Beta Deployment Runbook

Headless. Single-tenant. BYOK. Local-first. The smoke succeeds when Tilth ingests a seed corpus, completes Classification Review with an Ed25519-signed register, runs Scout→Scribe→Editor→Judge→Red Team→Logician on one section, stages a submission package, and stops at the operator-clicks-final-submit boundary.

Every step has an **observable**. If the observable is absent, the operator stops and surfaces the gap before continuing.

---

## §0. Conventions

- `$ROOT` = `/Users/goldenquill/Downloads/GoldenQuill` (the operator's clone).
- `$VENV` = `$ROOT/.venv` (Python 3.14.4 — pinned interpreter per `scripts/run_tests.sh`).
- Operator runs everything from `$ROOT` unless noted.
- "Operator action" = manual step Josh runs himself (keys, model downloads, test-org bootstrap, portal click). "Automated" = Tilth or this runbook drives it.
- Codes prefixed `F-CLASS-*`, `F-INTAKE-*`, `F-UPLOADER-*` etc. are Logician fail-closed gate identifiers per the architecture LOCK; their predicates live under `pipeline/logician/gates/`.

---

## §1. Prerequisites (verify, do not assume)

### 1.1 Python 3.14 .venv

```
$VENV/bin/python3 --version
```

Observable: `Python 3.14.4` (or ≥ 3.11; pyproject requires `>=3.11`). System `python3` on macOS is 3.9 and cannot collect the codebase — never run pytest with system Python.

If absent, rebuild:

```
/opt/homebrew/bin/python3.14 -m venv .venv
.venv/bin/pip install -e '.[dev]'
```

### 1.2 Pinned substrate (per ADR-001 Golden Image)

`pyproject.toml` lists the v0.1 Golden Image substrate as direct dependencies. Verify the install set:

```
$VENV/bin/pip list | grep -iE 'pydantic|cryptography|pyyaml|feedparser|idna|spacy|rapidfuzz|python-docx|pypdf|openpyxl|weasyprint|jinja2|cssselect2|tinycss2'
```

Expected (current as of `pyproject.toml` 2026-05-11): `pydantic`, `pydantic_core`, `cryptography>=42`, `pyyaml>=6`, `feedparser>=6`, `idna>=3`, `spacy>=3.7`, `rapidfuzz>=3`, `python-docx>=1`, `pypdf>=4`, `openpyxl>=3.1`, `weasyprint>=60`, `Jinja2>=3.1`, `cssselect2>=0.7`, `tinycss2>=1.2`.

If any are missing: `$VENV/bin/pip install -e '.[dev]'` re-pulls the pinned set.

### 1.3 spaCy NER model

The F-LOGICIAN-FABRICATED-ORG gate lazy-loads `en_core_web_sm`. Verify:

```
$VENV/bin/python3 -c "import spacy; spacy.load('en_core_web_sm'); print('ok')"
```

Observable: `ok`. If `OSError: ... not found`:

```
$VENV/bin/python3 -m spacy download en_core_web_sm
```

### 1.4 Observability — Logfire (operator action: install)

Logfire is the canonical observability backend per architecture v7.0.x and the Wake-Up sequence. It is **not yet pinned in `pyproject.toml`**. To bring up observability on this dev node:

```
$VENV/bin/pip install 'logfire>=0.42'
$VENV/bin/python3 -c "import logfire; print(logfire.__version__)"
```

Observable: a version string. Then set the project token (operator action):

```
$VENV/bin/python3 -m logfire auth
# operator follows the device-flow URL in the browser; selects the
# Golden Quill / Tilth project (or creates one); pastes the
# write-token into the prompt
```

Observable: `~/.logfire/default.toml` written. **Subsequent `logfire.configure(...)` calls in Tilth code will pick it up automatically.**

If Josh prefers to defer Logfire wiring, the smoke can run without it; the gap is flagged in §10.

### 1.5 Node + npm + openclaw

```
/opt/homebrew/bin/node --version
/opt/homebrew/bin/npm --version
PATH=$HOME/.npm-global/bin:$PATH openclaw --version
```

Expected: node ≥ 22 (currently 25.9.0), npm present, `OpenClaw 2026.5.7` (or newer — `2026.5.12` is available; update is **optional**, not a blocker).

Update (optional):

```
PATH=$HOME/.npm-global/bin:$PATH npm install -g openclaw@latest
```

### 1.6 openclaw gateway daemon

```
PATH=$HOME/.npm-global/bin:$PATH openclaw status
```

Observable: `Gateway: local · ws://127.0.0.1:18789 (local loopback) · reachable`, plus `Gateway service: LaunchAgent installed · loaded · running`.

The dashboard at http://127.0.0.1:18789/ must respond `200`:

```
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:18789/
```

If down, the LaunchAgent should restart it; if not, see the OpenClaw README under `~/.openclaw/`.

### 1.7 Local LLM substrate — Ollama daemon + Mistral 7B class

```
/usr/local/bin/ollama list
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:11434/api/tags
```

Observable: `mistral:7b` (~4.4 GB) present in the list; HTTP `200` from the local Ollama API.

If `mistral:7b` is missing (operator action):

```
ollama pull mistral:7b
```

8 GB RAM on the M1 dev node fits `mistral:7b` (Q4) plus the OS. The 70B-class local-routable Editor / routine-Judge / Red Team paths under the Golden Quill 128 GB production floor do **not** fit here — that is intentional. The Beta routing on this dev node uses the cloud frontier for those seats when input is Public + Shareable; on a 128 GB client Golden Quill, the operator pulls the 70B-class model the router template names.

### 1.8 Test suite baseline (focused v0.1 smoke bar)

```
scripts/run_tests.sh tests/orchestrator/test_router_classification_boundary.py \
  tests/logician/gates/test_f_class_coverage_incomplete.py \
  tests/logician/gates/test_f_class_outbound_boundary.py \
  tests/logician/gates/test_f_class_routing_indeterminate.py \
  tests/integration/classification_review tests/seats/intake tests/seats/uploader \
  tests/logician/gates/test_f_cic_clc_coupling_violation.py \
  tests/logician/gates/test_f_cic_clc_match_null.py \
  tests/logician/gates/test_f_cic_clc_enum_drift.py -q
```

Observable: `339 passed` (current as of 2026-05-15). Any failure halts the deployment — do not proceed past §1 with a red baseline.

### 1.9 AST-lint clean

```
scripts/run_lint.sh pipeline
```

Observable: exit `0`. The pipeline tree is lint-pinned at every LOCK; a non-zero exit means a recent commit introduced an R-* rule violation that needs surgical fix before a smoke runs.

### 1.10 Architecture + lock_history sanity

```
wc -l pipeline/engineering/lock_history.v1.jsonl
tail -1 pipeline/engineering/lock_history.v1.jsonl | $VENV/bin/python3 -m json.tool | head -10
```

Observable: row count ≥ 214 (most recent LOCK as of this runbook is the §3 v6 Funding Goal quadruple-LOCK 2026-05-11). The tail row should parse as JSON and name `Josh Inklovich` as operator and a 2026-05-1x lock_timestamp_utc.

---

## §2. Golden Image substrate (per ADR-001)

The Golden Image is the frozen substrate the Golden Quill ships with. On the operator's dev node the Golden Image is the `pyproject.toml` install set plus the named subagent assets. No marketplace pulls at runtime — the appliance freezes its substrate at build.

### 2.1 What is already frozen (current tree)

- Pydantic AI + Logfire + Ollama/vLLM + curated Python document parsing utilities (per ADR-001 / v7.0.3 substrate amendment).
- Cedar policy evaluator: deterministic Python authoritative at v0.1; M15-seal at v1.x.
- WeasyPrint + Jinja2 for the WPFA buyer-facing PDF (substrate-frozen per §17.7.4 LOCKED 2026-05-11).
- spaCy `en_core_web_sm` for the F-LOGICIAN-FABRICATED-ORG NER gate.

### 2.2 Pinning gap to close before client cut

Logfire is **architecture-substrate-listed** (Wake-Up Sequence, ADR-001 §Alternatives Considered, white-glove playbook §0) but **not yet pinned in `pyproject.toml`**. Closing the gap is a Code-phase task, not a runbook-time task — surface it in the hand-back and note it here:

- Defect D-RB-01: `pyproject.toml` `dependencies` array does not include `logfire`. Operator's `pip install logfire` in §1.4 is a manual fallback. Engineering should add `"logfire>=0.42"` to `pyproject.toml` and re-LOCK the substrate next cycle.

### 2.3 What stays operator-controlled (not in the image)

- BYOK provider keys (§3).
- Per-deployment `router.yaml` derivation (§4 — dev node uses the workspace `router.yaml` directly).
- Operator's Ed25519 signing key (§5).
- The classification register itself (§7).
- The test org's substrate documents (§6).

---

## §3. BYOK envelope — operator action

The v0.1 Beta substrate is BYOK only. Every provider key belongs to Josh; nothing flows through a Golden Quill-managed billing relationship.

### 3.1 Key file location

```
~/.openclaw/.env
```

Already present on this machine (433 bytes, last modified 2026-04-13). Do not check this file into the repo. Do not paste its contents into prompts.

### 3.2 Required keys for v0.1 Beta dev-node smoke

| Variable | Purpose | Smoke-required? |
|---|---|---|
| `ANTHROPIC_API_KEY` | Scribe primary (Claude Sonnet 4.6) | Yes |
| `GROQ_API_KEY` | Editor primary (Llama 3.3 70B) + Scribe fallback (Qwen 3 32B) + Red Team primary (GPT-OSS 120B) + Scout fallback (Llama 3.1 8B Instant) | Yes |
| `GOOGLE_API_KEY` | Judge primary (Gemini 2.5 Pro) + Scout escalation (Gemini 2.5 Flash) | Yes |
| `OPENAI_API_KEY` | Red Team escalation (GPT-5.1) | No (escalation only) |
| `BRAVE_SEARCH_API_KEY` | Scout Channel F web search (2000 q/month free tier) | No (Channel F is one of six parallel; smoke can run on A–E) |

For v0.2 channels (Twilio / Postmark / MTProto / WhatsApp Business API): **not required for v0.1 Beta**. Surface in §11 as a v0.2 BYOK envelope item.

### 3.3 Verify the keys load (without printing them)

```
$VENV/bin/python3 -c "
import os, pathlib, dotenv
dotenv.load_dotenv(pathlib.Path.home() / '.openclaw' / '.env')
needed = ['ANTHROPIC_API_KEY', 'GROQ_API_KEY', 'GOOGLE_API_KEY']
for k in needed:
    print(k, '=', 'set' if os.environ.get(k) else 'MISSING')
"
```

Observable: every required key prints `set`. Never print the value. If any key prints `MISSING`, operator pastes it into `~/.openclaw/.env` and re-runs.

If `dotenv` is not installed, swap to: `set -a; source ~/.openclaw/.env; set +a; printenv | grep -E '^(ANTHROPIC|GROQ|GOOGLE)_API_KEY' | sed 's/=.*$/=<set>/'`.

---

## §4. Per-deployment router.yaml (dev-node form)

On the dev node, the workspace `router.yaml` is **both** the workspace template and the active dev-node deployment config. A client Golden Quill derives a per-deployment `router.yaml` at white-glove time from (a) this template, (b) the signed Golden Quill router-template release, and (c) the operator's classification register. The `F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID` gate refuses to apply any router-template update whose Ed25519 signature does not verify against the white-glove-pinned publisher public key.

Verify the active router resolves:

```
$VENV/bin/python3 -c "
import yaml, pathlib
r = yaml.safe_load(open('router.yaml'))
seats = r['tilth']
print('Scribe primary:', seats['scribe']['primary'])
print('Judge primary:', seats['judge']['primary'])
print('Editor primary:', seats['editor']['primary'])
print('Red Team primary:', seats['red_team']['primary'])
print('Scout primary:', seats['scout']['primary'])
print('Logician:', seats['logician'].get('implementation'))
"
```

Observable:

```
Scribe primary: anthropic/claude-sonnet-4-6
Judge primary: google/gemini-2.5-pro
Editor primary: groq/llama-3.3-70b-versatile
Red Team primary: groq/openai/gpt-oss-120b
Scout primary: ollama/mistral:7b
Logician: python + cedar-policy
```

If `router.yaml` parses but a seat resolves to a different binding, the **router.yaml is the SOLE source of truth** — no other doc should hardcode a model name. Either router.yaml is the right active state and the runbook expectation is stale (update this section), or router.yaml has drifted (open a daily_log row and reconcile).

---

## §5. Operator Ed25519 signing keypair

The operator's Ed25519 keypair signs every classification register, every per-grant SP0 override chain, every KFR fact at AWARD_INGEST, every WPFA CycleReceipt buyer-facing PDF attestation. The private key never leaves the Golden Quill (or, for dev-node use, never leaves the operator's Mac).

### 5.1 Check whether a keypair already exists

```
ls -la $HOME/.golden_quill/operator_keys/ 2>&1 || echo 'absent'
```

If absent, generate one (operator action; pick a passphrase you will not forget):

```
$VENV/bin/python3 -c "
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization as ser
import pathlib, os, getpass
home = pathlib.Path.home() / '.golden_quill' / 'operator_keys'
home.mkdir(parents=True, exist_ok=True)
priv = Ed25519PrivateKey.generate()
pw = getpass.getpass('passphrase: ').encode()
priv_bytes = priv.private_bytes(
    encoding=ser.Encoding.PEM, format=ser.PrivateFormat.PKCS8,
    encryption_algorithm=ser.BestAvailableEncryption(pw))
(home / 'operator_priv.pem').write_bytes(priv_bytes)
(home / 'operator_priv.pem').chmod(0o600)
pub = priv.public_key().public_bytes(
    encoding=ser.Encoding.PEM, format=ser.PublicFormat.SubjectPublicKeyInfo)
(home / 'operator_pub.pem').write_bytes(pub)
print('wrote', home)
"
```

Observable: `~/.golden_quill/operator_keys/operator_priv.pem` (mode `0600`) and `operator_pub.pem`.

### 5.2 Pin the public key for `F-CLASS-REGISTER-SIGNATURE-INVALID`

The classification register orchestrator and the F-CLASS register-signature gate need the operator's pinned public key. The pinning path is per-org under `orgs/<slug>/vault/classification/` — `tilth_review_classify.py` accepts `--operator-key-id op-001` and writes the pubkey fingerprint into the signed register block. The dev-node smoke uses `op-001`; production deployments may use a more descriptive key id.

---

## §6. Test org bootstrap — operator action

The smoke needs an org folder with PROJECT_CONTEXT.md filled enough to drive one section's worth of drafting. **Do not use an existing client org** — Law 3 (Org Isolation). Use a synthetic-but-plausible dev-node org.

### 6.1 Copy the template

```
cp -R orgs/_TEMPLATE orgs/_test_v0_1_beta
```

### 6.2 Fill the synthetic PROJECT_CONTEXT.md (operator action)

Edit `orgs/_test_v0_1_beta/PROJECT_CONTEXT.md` and replace every `[NEEDED]` field with synthetic-but-plausible values that **do not match any real organization**. Suggested seed:

- Org name: `Verdant Loop Cooperative` (fabricated).
- EIN, UEI, SAM status: any plausible fake — clearly marked `[SYNTHETIC]` in surrounding comments.
- Address / county: a plausible Pittsburgh-region location.
- Production metrics: small-scale ag operation (e.g., 2 acres mushroom cultivation, 150 lb/wk production).
- Financials: dev-scale fake.
- Mission, programs, partnerships: plausible regenerative ag + co-op archetype.
- CIC tag: `cooperative` (per CLAUDE.md six Customer Identity Categories).

Per CLAUDE.md, the runbook does not encode a CIC→CLC binding; matching is opportunity-driven. The test org's CIC tag is **applicant-side** only.

### 6.3 Seed a small document corpus for Intake BULK_INGEST

Place 3–5 plausible synthetic documents under `orgs/_test_v0_1_beta/_intake_inbox/`:

- `mission_statement.md` (≤ 1 page)
- `audited_financials_FY25.txt` (a few synthetic numbers)
- `prior_grant_award_PA_AIG_2025.md` (synthetic, marked `[SYNTHETIC]`)
- `partnership_letter_local_dist.md` (synthetic)
- `board_minutes_2026_q1.md` (synthetic)

Each carries an `[SYNTHETIC — Tilth dev-node smoke 2026-05-15]` header so the audit trail records that this org is not real.

### 6.4 Bootstrap classification scaffold

The `orgs/_TEMPLATE/classification_review/` scaffold copied in §6.1 already includes `proposals/`, `signed/`, and `audit_log.jsonl`. Verify:

```
ls orgs/_test_v0_1_beta/classification_review/
```

Observable: `proposals/`, `signed/`, `audit_log.jsonl`, `README.md`.

---

## §7. End-to-end smoke sequence

The smoke runs one grant cycle on the test org from §6, end-to-end through every seat, stopping at the operator-clicks-final-submit boundary.

### 7.1 Intake BULK_INGEST

```
$VENV/bin/python3 -m pipeline.cli.tilth_intake \
  --org _test_v0_1_beta \
  --mode bulk \
  --inbox orgs/_test_v0_1_beta/_intake_inbox/ \
  --signing-key-file ~/.golden_quill/operator_keys/operator_priv.pem \
  --operator-key-id op-001
```

What this does (per §11 Intake v1 LOCKED 2026-05-10):

1. Reads each file in `_intake_inbox/`.
2. Substrate-dispatches per file format (PDF unique-page-match + DOCX paragraph-index + Markdown single-line + XLSX cell ref).
3. Extracts candidate facts. **Each candidate carries verbatim-quote-with-page provenance** — literal extracted text, source file, page/paragraph/row ref, SHA3-512 over canonicalized source bytes, extractor confidence.
4. Surfaces each candidate **one at a time** to the operator. Operator confirms each fact (TTY prompt; auto-promote four-layer defense refuses non-TTY auto-confirm).
5. Writes confirmed facts to `orgs/_test_v0_1_beta/vault/kfr/register.yaml` and signs.

Observable: `register.yaml` exists with confirmed facts; each entry has `source_provenance` block with `quote`, `source_file`, `page_or_paragraph`, `source_sha3_512`. No fact lacks a citation.

**Fail-closed checkpoints during ingest:**
- `F-EXTRACTOR-FABRICATION` — any candidate whose verbatim quote does not substrate-verify is rejected.
- `F-INTAKE-EMBEDDING-NS-MISMATCH`, `F-INTAKE-CONFIG-SIGNATURE-INVALID`, `F-INTAKE-EMBEDDING-ENDPOINT-INVALID`, `F-INTAKE-WATCHER-TOCTOU` — substrate-integrity gates per §11 v1 Cycle 1 hardenings.

### 7.2 Classification Review

```
$VENV/bin/python3 -m pipeline.cli.tilth_review_classify \
  --org _test_v0_1_beta \
  --signing-key-file ~/.golden_quill/operator_keys/operator_priv.pem \
  --operator-key-id op-001
```

What this does (per architecture v7.0.7 §3 + the wrapper LOCKED 2026-05-10):

1. Reads every Intake proposal under `orgs/_test_v0_1_beta/classification_review/proposals/`.
2. On a TTY: prompts the operator per field — `public` / `shareable` / `confidential` / `operator_flagged`. Confirm Card-archetype default or override.
3. Writes the per-document signed artifact under `signed/classification_review_<doc-hash>.yaml` (schema: `classification_review.signed.v1`).
4. Appends one row to `audit_log.jsonl` per **override** (confirmed defaults do not generate audit rows; the proposal artifact is already on-disk evidence).
5. Upserts the persistent per-org register at `orgs/_test_v0_1_beta/vault/classification/register.yaml` and re-signs with the operator's key.

Observable: `register.yaml` exists with operator's Ed25519 signature block; `audit_log.jsonl` contains an entry per override.

**Fail-closed checkpoints at register sign-off:**
- `F-CLASS-COVERAGE-INCOMPLETE` — required F-CLASS-* enforcement modules and tests are present in the runtime tree (covered by the §1.8 smoke baseline).
- `F-CLASS-REGISTER-UNSIGNED` / `F-CLASS-REGISTER-SIGNATURE-INVALID` / `F-CLASS-REGISTER-HASH-MISMATCH` — the orchestrator runs all four pre-declaration of review success.

### 7.3 Smoke target — one grant section, end-to-end

Pick a plausible synthetic opportunity. The simplest seed is the dev-node `pipeline/rubrics/vapg_fy26.json` rubric and a synthetic 1-section project narrative request.

There is no operator-facing one-shot CLI for "run the whole cycle on one section" at v0.1 Beta — the cycle dispatches through `pipeline/orchestrator/` modules. For the dev-node smoke, the operator drives the seats via the integration test path the lock-and-clear packet already enforces:

```
scripts/run_tests.sh tests/integration/classification_review tests/seats/intake tests/seats/uploader -q
```

Observable: passes per §1.8 baseline.

For a **live** end-to-end (real cloud calls with real keys), the operational dry-run is to dispatch through the openclaw gateway bridge per AGENTS.md "Cross-family review — bridge pattern":

```
PATH=$HOME/.npm-global/bin:$PATH openclaw infer model run --gateway \
  --model anthropic/claude-sonnet-4-6 \
  --prompt "Draft a one-paragraph project narrative for [SYNTHETIC org Verdant Loop Cooperative] applying for [SYNTHETIC VAPG-style planning grant]. Topic: capacity-build for cooperative mushroom hub. ~150 words." \
  --json
```

Observable: a JSON response with `ok: true` and a draft paragraph in the content field. This proves Scribe path is live. Editor / Judge / Red Team can be exercised the same way against the model IDs from `router.yaml`.

The cleaner v0.1 Beta milestone is the **reproducible submission-mode replay packet** (see §10 + the lock-and-clear packet "Reproducible submission dry run" gate). That packet is the next deliverable after this runbook executes.

### 7.4 Uploader staging

```
$VENV/bin/python3 -c "
from pipeline.orchestrator.seats.uploader import stage_for_portal
# stub-form invocation for runbook documentation;
# the actual smoke uses tests/seats/uploader/ paths
"
```

What this does (per §12 Uploader v1 LOCKED 2026-05-10):

1. Reads the operator-approved final draft.
2. Assembles the funder-portal-required formats: DOCX via `python-docx`, PDF validation via `pypdf`, XLSX validation via `openpyxl`.
3. Routes through one of four portal adapters: Grants.gov Workspace, SAM.gov, Common Grant Application, copy-paste fallback. (Foundant / Submittable / Fluxx are Path-b scope; attachments deferred to v1.1.)
4. Writes the staged package to `orgs/_test_v0_1_beta/vault/submissions/<run_id>/`.
5. **Halts before submission.** `F-UPLOADER-AUTOSUBMIT-ATTEMPTED` fail-closes any path that bypasses the operator's manual click. There is no M13 escape — auto-submit is architecturally prohibited.

Observable: a staged package directory exists, file integrity passes, the manifest names the funder portal and lists each file with SHA3-512.

### 7.5 Operator clicks final submit — operator action

On the funder portal, in a browser, the operator uploads the staged package and clicks **Submit**. The system does not do this. The audit trail records the staging timestamp and the operator's manual-submit acknowledgment (a one-line note the operator pastes back into the run directory).

---

## §8. WPFA cycle close (optional for first smoke; required for any client-facing claim)

Per §17 WPFA v1 LOCKED 2026-05-11, every cycle close emits a typed `CycleReceipt` Pydantic artifact with actual dollars + watt-hours vs counterfactual. For the dev-node smoke this is optional; for any deployment that will produce a buyer-facing PDF it is mandatory.

```
$VENV/bin/python3 -m pipeline.cli.tilth_wpfa --help
```

Observable: usage prints. To run the actual cycle-close accountant, follow the CLI's `--org`, `--cycle-id`, and operator-attestation arguments. The `F-WPFA-OPERATOR-SIGNATURE-MISSING` gate refuses buyer-facing PDF emission without operator Ed25519 attestation.

---

## §9. Observability bringup

### 9.1 Logfire spans

If §1.4 installed Logfire and the operator ran `logfire auth`, the dev-node smoke will emit spans automatically on any code path that calls `logfire.configure(...)`. **Today's tree does not yet auto-bootstrap Logfire** — v7.0.4-M1 §8.4.1 mandates a process-wide bootstrap shim that is not yet wired. Until that shim lands:

- Observability is best-effort.
- Spans appear on calls that explicitly configure Logfire (e.g., test harnesses that import `pipeline.observability`).
- The dashboard URL after `logfire auth` is operator-specific; check `~/.logfire/default.toml` for the project token + dashboard URL.

This is defect D-RB-02; flagged in the hand-back.

### 9.2 openclaw dashboard

The OpenClaw dashboard at http://127.0.0.1:18789/ surfaces agent invocations, model dispatches, gateway health. Open it in a browser to watch a live cycle.

### 9.3 daily_log + lock_history

```
ls -1 daily_logs/ | tail -3
tail -1 pipeline/engineering/lock_history.v1.jsonl | $VENV/bin/python3 -m json.tool | head -8
```

Observable: today's daily_log file exists with at least one entry; lock_history tail names a recent operator-signed LOCK.

---

## §10. Verification checklist

The deployment is "done" for dev-node-smoke purposes when **every** observable below is green. If any is missing, the operator surfaces the gap and stops.

| # | Check | Observable | Where |
|---|---|---|---|
| V01 | Python 3.14 .venv usable | `Python 3.14.x` | §1.1 |
| V02 | Pinned substrate installed | every dep in §1.2 list shows in `pip list` | §1.2 |
| V03 | spaCy NER model loads | `ok` | §1.3 |
| V04 | Logfire installed + authed (optional) | version string + `~/.logfire/default.toml` | §1.4 |
| V05 | openclaw 2026.5.7+ + dashboard 200 | `OpenClaw 2026.5.x ...` and HTTP `200` | §1.5/1.6 |
| V06 | openclaw gateway LaunchAgent running | `LaunchAgent installed · loaded · running` | §1.6 |
| V07 | Ollama daemon + `mistral:7b` present | HTTP `200` from `:11434` + `mistral:7b` in list | §1.7 |
| V08 | Focused v0.1 smoke suite green | `339 passed` (or current bar) | §1.8 |
| V09 | AST-lint clean | exit `0` | §1.9 |
| V10 | lock_history sane | tail row parses; row count ≥ 214 | §1.10 |
| V11 | BYOK keys present (no values printed) | `ANTHROPIC_API_KEY=set` etc. | §3.3 |
| V12 | router.yaml resolves to expected seat bindings | seat→model strings match §4 expected | §4 |
| V13 | Operator Ed25519 keypair present | `~/.golden_quill/operator_keys/operator_priv.pem` mode `0600` | §5 |
| V14 | Test org bootstrapped | `orgs/_test_v0_1_beta/PROJECT_CONTEXT.md` with synthetic values | §6 |
| V15 | Intake BULK_INGEST KFR written + signed | `vault/kfr/register.yaml` with provenance per fact | §7.1 |
| V16 | Classification Review register signed | `vault/classification/register.yaml` Ed25519-signed | §7.2 |
| V17 | One live Scribe call returns | openclaw gateway returns `ok: true` with draft text | §7.3 |
| V18 | Uploader stages package without auto-submit | manifest written under `vault/submissions/<run_id>/`; no submit attempted | §7.4 |
| V19 | Operator manual portal submit recorded | one-line acknowledgment in run directory | §7.5 |
| V20 | (Optional) WPFA CycleReceipt emitted + attested | signed receipt under `vault/operational/cycle_receipts/` | §8 |

---

## §11. Operator-action items (the runbook cannot do these — Josh runs them)

| # | Action | Owner | Notes |
|---|---|---|---|
| OP-01 | `pip install logfire` + `logfire auth` (if observability desired this session) | Josh | §1.4. Engineering should pin Logfire in `pyproject.toml` (defect D-RB-01). |
| OP-02 | `ollama pull mistral:7b` (skip if already present) | Josh | §1.7. Currently present per host check. |
| OP-03 | Confirm `ANTHROPIC_API_KEY` / `GROQ_API_KEY` / `GOOGLE_API_KEY` are in `~/.openclaw/.env` and current | Josh | §3.2. Rotate any expired key. |
| OP-04 | (Optional) Add `OPENAI_API_KEY` for Red Team escalation | Josh | §3.2. Smoke does not require escalation path. |
| OP-05 | (Optional) Add `BRAVE_SEARCH_API_KEY` for Scout Channel F | Josh | §3.2. Channels A–E already cover discovery breadth. |
| OP-06 | Generate Ed25519 keypair if absent and pick a passphrase | Josh | §5.1. Write the passphrase down somewhere only Josh can reach. |
| OP-07 | Bootstrap `orgs/_test_v0_1_beta/` with synthetic substance | Josh | §6. **Never use real client data for the dev-node smoke** — Law 3. |
| OP-08 | Seed `_intake_inbox/` with 3–5 synthetic documents | Josh | §6.3. Mark every one `[SYNTHETIC]`. |
| OP-09 | Run Intake BULK_INGEST, confirm each fact at the TTY prompt | Josh | §7.1. The auto-promote four-layer defense refuses non-TTY auto-confirm. |
| OP-10 | Run Classification Review, override per field at TTY | Josh | §7.2. |
| OP-11 | Run one live Scribe call through the openclaw gateway bridge | Josh | §7.3. Proves cloud routing reaches Anthropic via Josh's BYOK. |
| OP-12 | Open the funder portal in a browser, upload staged package, click Submit | Josh | §7.5. Tilth never does this. |
| OP-13 | Paste the operator-submit acknowledgment into the run directory | Josh | §7.5. Closes the audit trail's final-submit row. |
| OP-14 | (Optional) Run WPFA CycleReceipt + sign for buyer-facing PDF | Josh | §8. Required only for any deployment that will surface buyer-facing claims. |

---

## §12. Forward — what the dev-node smoke does *not* yet prove

This runbook proves the dev node can drive one synthetic grant through every seat on local + cloud routes under Josh's BYOK, with classification gating, deterministic Logician fail-closure, and operator-final-submit discipline. It does **not** yet:

1. **Produce the reproducible submission-mode replay packet** named in the lock-and-clear packet ("Reproducible submission dry run" gate, OPEN). That is the next deliverable after this runbook executes — a sanitized replay artifact an outside engineer can reproduce.
2. **Exercise a 70B-class local-routable Editor / Red Team / routine-Judge path.** The 8 GB M1 dev node cannot host those models; that path engages only on the 128 GB production Golden Quill.
3. **Exercise the heavy-Judge swap.** Same hardware constraint — the 200B-class on-demand swap is 128 GB-floor territory.
4. **Exercise Data Collector / Report Generator runtime.** Both are v0.2 horizon.
5. **Exercise Stage-2+ fleet aggregation.** Out of scope for v0.1.

Each of these is a known forward gap. None is a blocker for the dev-node smoke.

---

## §13. Defects surfaced during the safe-step pre-walk (2026-05-15)

| ID | Defect | Severity | Fix path |
|---|---|---|---|
| D-RB-01 | `logfire` not pinned in `pyproject.toml` despite being substrate per Wake-Up + ADR-001 | MEDIUM | Engineering — add `"logfire>=0.42"` to `dependencies`; re-LOCK substrate |
| D-RB-02 | No process-wide Logfire bootstrap shim wired (v7.0.4-M1 §8.4.1 mandates it) | MEDIUM | Engineering — implement the shim; route every council seat through it |
| D-RB-03 | OpenClaw 2026.5.12 available, dev node on 2026.5.7 | LOW | Optional operator action: `npm install -g openclaw@latest` |
| D-RB-04 | OpenClaw gateway "no bootstrap files" (status output) | UNKNOWN | Investigate whether this is expected for the dev-node profile or a missing config |

D-RB-01 and D-RB-02 are paired — without the shim, even a pinned Logfire would not be wired into the council seats. Both are engineering deliverables; neither blocks the §10 verification checklist from passing in its current form.

---

**End of runbook.** Pairs with `docs/white_glove_v0_1_beta.md` (operator-facing onboarding playbook) + `pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md` (clearance bar) + `docs/v0_1_TECHNICAL_LEAD_BRIEF.md` (what v0.1 must do). Update this runbook in place when a step's observable changes or when a defect closes.
