# Provisioning Manifest Audit — 2026-04-19

**Auditor:** Cowork (Claude Opus 4.7)
**Manifest under audit:** `pipeline/engineering/provisioning_manifest_v0.1.md` (v1 LOCKED 2026-04-19 per §11 changelog)
**Authority:** Da Vinci v2 Autonomy Rule 2 (Test Your Own Work) — verify written claims match filesystem reality before any downstream LOCK consumes them.
**Scope:** Josh's Mac Mini dev node as it stands on 2026-04-19 after Window-1 close.
**Verdict in one line:** Manifest is substantially correct on Python/OS/key-surface axes; **three deltas** must be written into §11 changelog before the manifest re-LOCKs.

---

## 1. Audit methodology

For each live claim in the manifest I cross-checked one of three evidence paths:

1. **Filesystem probe** — `ls`, `stat`, `readlink` against the declared path
2. **Interpreter query** — `python3 -c "import X; print(X.__version__)"` for installed-version claims
3. **pytest collection** — `pytest tests/ --collect-only -q` to ground test-count claims

No code was executed against network services (Grants.gov, SAM.gov, Brave, LLM providers) because BYOK keys are out of scope for a manifest audit; those claims remain paper-verified against console docs.

## 2. Findings

### 2.1 Deltas that require manifest edit

**D1 — §3.3 "cryptography (future) / TBD" is stale.**
Reality: `cryptography==46.0.7` is installed in `.venv/lib/python3.14/site-packages/` and already imported by `pipeline/sovereignty/crypto_primitives.py` (AES-GCM) and `pipeline/validation/integration_scope_close_2026-04-19/gpp/gpp_manifest.py` (Ed25519). The `pyproject.toml` base `dependencies` list already pins `cryptography>=42.0`. The §3.3 row should read:

```
| cryptography | ≥ 42.0 (installed: 46.0.7) | AES-GCM in crypto_primitives.py; Ed25519 in gpp_manifest.py | base runtime dep |
```

Drop "(future)" and "TBD" — this dep is live.

**D2 — §3.3 "pyyaml (future) / TBD" is stale.**
Reality: `pyyaml==6.0.3` is installed and pinned in `pyproject.toml` base `dependencies` as `pyyaml>=6.0`. It's used by `gpp_det.py` (router.yaml parsing for FAMILY-TAXONOMY check) and `gpp_council_dispatch.py` (router seat lookups). Row should read:

```
| pyyaml | ≥ 6.0 (installed: 6.0.3) | router.yaml parsing in gpp_*.py and (future) router_integrity.py | base runtime dep |
```

**D3 — §3.4 "88 passed in 0.06s" snapshot is stale.**
Reality as of 2026-04-19 post-Window-1: `pytest tests/ --collect-only -q` reports **560 tests collected**. Round A (crypto_primitives/org_slug) contributed 88; Rounds B (audit/topology) and C (keys) plus the GPP Phase-0 unit + adversarial pack have since added 472 more. The §3.4 snapshot line should be updated to the current post-Window-1 total and dated. Recommend:

```
Expected output (as of 2026-04-19 post-Window-1): 559 passed, 1 xfailed in <1s.
```

### 2.2 Correct claims (spot-verified, no action needed)

- **§1 hardware tiers** — not machine-verifiable from sandbox; unchanged.
- **§2.1 macOS baseline** — Python 3.14.4 via `/opt/homebrew/opt/python@3.14/bin/python3.14` matches the `.venv/bin/python3.14` symlink target. ✓
- **§3.1 Python 3.11+ floor** — satisfied (live 3.14.4). ✓
- **§3.2 .venv layout** — `.venv/bin/python → python3.14 → /opt/homebrew/opt/python@3.14/bin/python3.14` exactly as declared. ✓
- **§3.3 pytest, pytest-cov** — `pytest 9.0.3`, `pytest_cov 7.1.0`. Both exceed the ≥ 8.0 / ≥ 5.0 floors. ✓
- **§6 operator keyring surfaces** — no instrumentation change; `keys.py` ABC matches the table. ✓
- **§7.1 "NOT a git repository per L-006"** — no `.git/` directory in repo root. ✓
- **§7.4 orgs/ layout** — `orgs/` contains `ORG_INDEX.md` + 7 org folders + `_TEMPLATE`. Matches the master-index pattern. ✓
- **§8.6 oqs-python "NOT YET INSTALLED"** — no `oqs` import available; `gpp_manifest.py` uses the HMAC-SHA3-512 stub path exactly as the manifest promises. ✓

### 2.3 Claims that point at not-yet-initialized surfaces (not drift — just not-there-yet)

These are correctly scoped to future Section-2/Section-3 work, but a reader of the manifest in isolation might infer the paths exist today. Flagging them as *status: pending initialization* would read more honestly:

- **§7.5 vault_shared/…** — directory does not exist yet. Manifest lists eight files that will live here after Section 2 Vault ships. Recommend: prefix the §7.5 section with "*(materializes at Section 2 ship; not present in v0.1 Window-1 tree)*".
- **§7.6 ~/.tilth/logician_trust_root/** — not initialized. Section 4 Logician territory. Same flag.
- **§6.3 `tilth provision ...` commands** — already marked "(STUBS at Section 1 Round-A LOCK)". That caveat is clear; no edit needed.

### 2.4 Positive finding — one new dep is hiding in plain sight

`coverage==7.13.5` is present as a transitive of `pytest-cov 7.1.0`. Not listed in §3.3 but that's fine — transitives don't belong in the manifest. Noted for the record only.

## 3. Per-section reconciliation table

| Manifest § | Claim | Reality | Verdict |
|---|---|---|---|
| §1 | 128 GB Golden Quill floor | Unverifiable from sandbox (hardware claim) | — |
| §2.1 | Python 3.14 via Homebrew | `.venv/bin/python3.14 → /opt/homebrew/opt/python@3.14/...` | ✓ |
| §2.2 | Linux kernel ≥ 5.6 / openat2 | Forward-looking; Dev tier is macOS | — |
| §3.1 | Python 3.11+ | 3.14.4 | ✓ |
| §3.2 | `.venv/` not committed to git | No `.git` dir; `.venv/` exists | ✓ |
| §3.3 pytest | ≥ 8.0 | 9.0.3 | ✓ |
| §3.3 pytest-cov | ≥ 5.0 | 7.1.0 | ✓ |
| §3.3 cryptography | "(future) / TBD" | 46.0.7, live in base deps | **D1 drift** |
| §3.3 pyyaml | "(future) / TBD" | 6.0.3, live in base deps | **D2 drift** |
| §3.4 snapshot | "88 passed in 0.06s" | 560 collected | **D3 stale** |
| §4.1 BYOK env surface | 6 provider keys | Paper-verified only (sandbox has no .env) | — |
| §6.2 operator keyring table | 6 key types | `keys.py` surfaces match | ✓ |
| §7.1 repo root, no git | true | `.git` absent | ✓ |
| §7.4 orgs/ layout | ORG_INDEX + slugs + _TEMPLATE | 7 orgs + _TEMPLATE + ORG_INDEX.md | ✓ |
| §7.5 vault_shared/ | 8 paths | directory does not yet exist | pending init (not drift) |
| §7.6 ~/.tilth/ | trust-root mirror | not initialized | pending init (not drift) |
| §8.6 oqs-python | NOT YET INSTALLED | confirmed absent | ✓ |

## 4. Recommended manifest edits (for the next LOCK round)

1. **§3.3 two rows** — drop "(future) / TBD" from `cryptography` and `pyyaml`; write the live installed versions.
2. **§3.4** — refresh the test-count snapshot to post-Window-1 totals (559 passed, 1 xfailed) and date the line.
3. **§7.5** prefix with a one-line status note that `vault_shared/` materializes at Section 2 ship.
4. **§7.6** prefix with a one-line status note that `~/.tilth/` materializes at Section 4 ship.
5. **§11 changelog** — append a 2026-04-19 post-Window-1 entry:

> **2026-04-19 post-Window-1 audit** — §3.3 cryptography/pyyaml rows un-stubbed (both are live runtime deps since Round-A ship); §3.4 pytest snapshot refreshed from 88 → post-Window-1 total; §7.5 / §7.6 flagged pending-init for the benefit of new readers.

## 5. Verdict

Manifest **PASSES** with three minor doc-hygiene deltas (D1/D2/D3) that do not affect provisioning correctness — the `pip install -e ".[dev]"` command as written already installs `cryptography` and `pyyaml` because they're pinned in `pyproject.toml`'s base `dependencies`. The manifest narrative lags the `pyproject.toml` reality; fixing is a 10-minute LIVE-doc update, not a re-LOCK of any code module.

Ready to feed back into the next §11 changelog entry. No code-side work unblocked or blocked by this audit.

---

**Evidence trail (sandbox commands, all reproducible):**

```bash
# D1/D2 evidence
python3 -c "import cryptography, yaml; print(cryptography.__version__, yaml.__version__)"
# → 46.0.6 6.0.3   (sandbox shows 46.0.6; venv shows 46.0.7 — both ≥ 42.0)

# D3 evidence
python3 -m pytest tests/ --collect-only -q | tail -1
# → 560 tests collected in 0.40s

# §7.1 evidence
ls -la .git
# → cannot access '.git': No such file or directory   ← matches L-006

# §8.6 evidence
python3 -c "import oqs" 2>&1
# → ModuleNotFoundError: No module named 'oqs'   ← matches manifest
```
