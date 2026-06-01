# Tilth v0.1 Engineering Process

**Status:** LOCKED 2026-04-19 as the operating discipline for v0.1 implementation. Authoritative until explicitly superseded. Minor corrections append to §15 changelog.

**Scope:** This document describes HOW code gets written, reviewed, and LOCKed for Tilth v0.1. It does NOT describe WHAT code gets written — that is the blueprint (`pipeline/blueprint/v0.1/section_*.md`) and the v7 architecture amendments (A1-A12 per signed-off addendum 2026-04-19).

**Effective dimensions.** Every decision in this process trades across: Effectiveness (does the code do what the blueprint says), Efficiency (tokens + wall-clock + operator attention), Stability (doesn't regress under change), Security (actually enforces the Five Laws), Sovereignty (the operator owns their stack). When two dimensions conflict, Sovereignty is the tie-breaker; Security is second; Stability third; Effectiveness fourth; Efficiency last.

---

## 1. Module engineering cycle (per module)

| Phase | Who | Output | Operator-visible? |
|---|---|---|---|
| E1 Spec card | Author (Claude Code) | `pipeline/engineering/spec_cards/<module>.md` — line-by-line derivation from blueprint | **Yes** — operator can edit before implementation |
| 1 Failure-code tests | Author | `tests/<section>/test_<module>_failures.py` — one failing test per `F-*` code from blueprint §6 | No |
| 2 Implementation | Author | `pipeline/<section>/<module>.py` | No |
| 3 Property + corpus tests | Author | `tests/<section>/test_<module>.py` + `tests/corpus/<module>/v<N>/` | No |
| 4 Self-audit (Rule 2 Magic Step) | Author | Spec card every-row check + pytest green + AST-lint clean | No |
| 5 Committee dispatch | Author | 5 reviewers parallel via Groq/OpenAI per router.yaml `code_*` rows | No |
| 6 Narrow-edit loop | Author | v2 module if structural finding; in-place fix if documentary; bailout file if OUT-OF-MODEL | No |
| 7 LOCK | Author | Preserve prior; write memory entry; append `pipeline/engineering/lock_history.v1.jsonl` telemetry + `review_lessons.v1.md` findings | **Yes** — E2 summary |

**Blocking conditions.** Stop and escalate (E3 operator synthesis) if: (a) retry cap 1 exhausted with substantive disagreement; (b) any reviewer surfaces a finding classified OUT-OF-MODEL; (c) blueprint-code drift detected; (d) spec card has a row not satisfiable under current blueprint.

---

## 2. Round granularity (grouping modules)

A "round" covers 1-3 modules dispatched to the committee together. Grouping rule:

> **Batch if** (a) combined module + test bytes under 40 KiB (≈10K tokens), (b) modules share no public-API boundary drift, (c) no module carries a CRIT-class failure mode under review.

Section 1 target: 6-8 rounds. Committee reviewer count stays fixed at five per round; total reviewer calls ≈ 30-40 for Section 1.

---

## 3. Code Thesis Committee (per router.yaml `code_*` rows — LOCKED A2 Block 2)

| Role | Model | Probes |
|---|---|---|
| code_author | anthropic/claude_code | Author of the module + tests |
| code_reviewer_1 | openai/codex | Correctness + idiom |
| code_reviewer_2 | alibaba/qwen3-32b | General-purpose cross-check (deliberately NOT a coder model — outside-perspective) |
| code_reviewer_3 | meta/llama-3.3-70b | Algorithm + blueprint adherence |
| code_reviewer_4 | openai_oss/gpt-oss-120b | Adversarial / security surface |
| code_reviewer_5 | moonshot/kimi-k2-instruct-0905 | Cross-module coherence + long-context |

Merge rule: **all_pass**. Retry cap: **1**. SFR-format verdicts per A3. Findings routed to `pipeline/validation/code_reviews/<round-id>/`.

### 3.1 Reviewer payload-size disciplines (added 2026-04-22)

Empirical finding, three rounds: **Qwen3-32B on Groq degrades non-linearly with consolidated-payload prompt-token count.**

| Round | Payload (prompt tokens, est.) | Qwen output | Format compliance |
|---|---|---|---|
| logician_v2_2_wave_3_4 (small per-gate dispatches) | ~15k–30k | full SFR, rubric `PASS`/`FAIL` | clean |
| vault_batch_1_2026-04-20 parent (consolidated, 5 modules) | ~120k | truncated; partial findings | degraded |
| vault_batch_1_redispatch_2026-04-22 (consolidated, 5 modules) | ~124k | `"verdict": "LOCKED"` (non-rubric token), 20 completion tokens; identical result on L-011 transport-retry with `reasoning_effort="none"` + verdict-token reinforcement addendum | malformed |

The other 4 seats (llama-3.3-70b, gemini-2.5-pro, gemini-2.5-flash, gpt-oss-120b) returned clean rubric-compliant verdicts on the identical 124k payload — this is a qwen3-32b-specific ceiling, not a payload-size issue writ large. Reasoning-mode tokens silently consume the completion budget even when `reasoning_effort="none"` suppresses the `<think>` stream.

**Discipline (pre-dispatch gate):** when `code_reviewer_2 = qwen3-32b` and the consolidated prompt-token estimate exceeds **~80k tokens** (≈ 300k chars at 3.7 chars/tok), do ONE of:

1. **Split the dispatch** — fire the committee per-module instead of consolidated. Each dispatch is an independent 5-seat fire; findings aggregate across dispatches at synthesis time.
2. **Accept semantic-PASS convention for qwen only** — pre-declare in the dispatch README that `{"verdict": "LOCKED"}` from qwen is interpreted as semantic-PASS (promote-intent, zero findings) per the redispatch precedent, and document the soft spot in the promotion row's `committee_tally` citation.
3. **Substitute for this round** — swap qwen3-32b out for a different cross-family general-purpose reviewer for the affected round only, log the substitution as a round-local deviation (not a roster amendment).

Options 1 and 3 preserve strict-rubric reading; Option 2 preserves slate stability at the cost of cosmetic rubric strictness. Default to Option 1 when modules admit clean per-module split; Option 2 when per-module split would fragment cross-module findings; Option 3 only when 1 and 2 are both unavailable.

Router self-fallback reality (2026-04-22): Groq Dev tier has no same-family fallback for qwen3-32b — `router.yaml` line 77 resolves fallback to itself (transport-retry only). Same for llama-3.3-70b at line 81. Cross-family fallback would violate reviewer-diversity invariants and is not wired.

**Tracking lesson:** see `review_lessons.v1.md` E-027.

---

## 4. Futureproofing disciplines (baked in from Round A)

These apply to every module, not just Section 1.

### 4.1 Public-API boundary
Every module's `__init__.py` declares `__all__` with ONLY stable public symbols. Downstream sections import from `pipeline.<section>`, never from `pipeline.<section>.<internal_module>`. Internal refactoring is free; public API change is a LOCK-cycle event (spec card row: "public API contract").

**Enforcement.** Custom AST-lint script walks every file under `pipeline/<section>/` and verifies no cross-section import reaches into another section's internal module. Runs in the test suite — drift is a test failure.

### 4.2 Schema versioning
Every JSON artifact, signed manifest, on-disk struct carries a `schema_version: "vN"` field. Version format: short string `"v1"`, `"v3"`, etc. Matches blueprint §0.5 Interface Index convention. `Section 1` ships `versioned_load(path, migrations: dict[version, callable])` primitive; every module with on-disk artifacts uses it. Unknown version → `F-SCHEMA-UNKNOWN-VERSION` fail-closed.

### 4.3 Backwards-compat corpus (monotonic)
Every LOCKed module keeps `tests/corpus/<module>/v<N>/` with preserved input + expected output pairs. Every future version MUST pass the combined corpus from v1 forward. Deletion requires an explicit `# BEHAVIOR_REMOVED per spec amendment X` comment in the test file. Accidental regression on old vectors surfaces as test failure.

### 4.4 Crypto-agility types (A12 made concrete)
Section 1 ships generic crypto types from v0.1 — `OperatorSignature`, `HashDigest` (alongside the blueprint §2.1 `HashPair`) — each carrying an `algorithm` field. Dispatch on algorithm via lookup table, never pattern-match on hardcoded string. v0.1 populates `algorithm = "ed25519"` / `"sha3-512"`; v0.2 ML-DSA addition is a row append, not a refactor.

### 4.5 Provider-adapter layer
Section 5 seat calls go through `pipeline.providers.<provider>.<version>.complete(...)`, not direct SDK calls. SDK drift (Anthropic, Groq, OpenAI, Google) is isolated to one adapter file per provider. Adapter version bumps are named events with corresponding lessons entries.

### 4.6 Blueprint-code drift detection
Every module top-of-file declares:

```python
BLUEPRINT_DEPS = {
    "section_1_sovereignty_envelope.md": {
        "sections_implemented": ["§4.3 M3", "§2.1 HashPair"],
        "hash_at_lock": "<sha3_512_hex_prefix>",   # 16-char prefix for human readability
        "hash_source_version": "v6",
    },
}
```

A drift-check script (`scripts/check_blueprint_drift.py`) walks modules, recomputes current blueprint hash, compares to recorded hash. Mismatch → `drift_possible` tag and re-review required before any code-lock operation on that module.

### 4.7 Key rotation primitives from v0.1
`keys.rotate(key_id, *, new_algorithm=None)` exists even though v0.1 only rotates Ed25519-to-Ed25519. Signature carries `new_algorithm` so v0.2 ML-DSA rotation is drop-in. Every long-lived key type has a rotation test in its suite.

### 4.8 Versioned on-disk paths
Pattern established: `<artifact_name>.v<N>.<ext>`. Apply to every artifact: `machine_calibration.v1.json`, `rfa_dissection.v2.json`, `lock_history.v1.jsonl`, `review_lessons.v1.md`. Old versions persist forever alongside new.

### 4.9 Regression-discipline on tests
Every test written stays. Deletion requires justification. Tests accumulate the regression corpus. Property tests strongly preferred over example tests where expressible.

### 4.10 Type hints everywhere
Every public function has a full type hint. Enforced by ruff + mypy. Missing type hint → test failure.

### 4.11 Docstring references blueprint
Every public function / class has a docstring citing its blueprint anchor:

```python
def canonical_slug(s: str) -> str:
    """Canonicalize an org slug deterministically. [§4.3 M3]"""
```

Short. The `[§X.Y M_N]` anchor is the link.

### 4.12 Engineering lessons accumulate
Every committee finding writes an entry to `pipeline/engineering/review_lessons.v1.md`. Future spec cards pre-check against accumulated lessons. Mirrors A11 telemetry-feedback pattern internal to engineering.

### 4.13 Upgrade command exists from v0.1
`tilth upgrade` command exists in v0.1 even as near-no-op. Grows behavior in v0.2+. Operators learn the command muscle-memory before migration is load-bearing.

### 4.14 No git-dependency in enforcement (L-006 discipline)
No engineering process step assumes `.git/` exists. No pre-commit hook. No signed-commit requirement. All integrity checks run against filesystem primitives (`flock`, hash, signed manifests). Confirmed by pre-exec preflight 2026-04-18.

---

## 5. Operator surface points (during code work)

Only four. Everything else is internal to this window / next window / subsequent windows.

- **E1 Spec card delivered.** Before any code, operator sees the one-page checklist derived from the blueprint. Can say "add X" / "out of scope" / "wrong anchor."
- **E2 LOCK summary.** After each module LOCKs: one-paragraph summary — what LOCKed, pytest count + green, 5/5 reviewer PASS, artifacts at path, telemetry line.
- **E3 Operator synthesis.** Only triggers on L-005 two-retry failure or OUT-OF-MODEL finding. Operator + Opus 4.7 decide next move. Rare.
- **E4 Milestone boundary.** Section fully LOCKed → section summary + next-section handoff.

Grantwriter context-discipline directive (`feedback_grantwriter_context_discipline.md`) applies recursively here: Josh does NOT track per-phase progress; the engineering flow swallows the ceremony.

---

## 6. Prompt-caching discipline (efficiency lever)

For the committee fan-out of 5 reviewers per module, the blueprint section + spec card + module bytes are identical across reviewers. Anthropic beta header `task-budgets-2026-03-13` enables ephemeral prompt caching. Dispatch pattern:

  - First reviewer call primes the cache.
  - Reviewers 2-5 hit cache for the identical prefix; only the per-reviewer system prompt + output tokens bill.
  - Groq caching (if available at dispatch time) used identically.
  - Net saving: ~60-70% input tokens per round vs naive fan-out.

On cache-miss the flow is correct-but-expensive — not a failure mode, just a cost event.

---

## 7. Delta reviews on retry

Round-2 reviews after narrow edits pass:
  - The diff (not the full module).
  - The original findings list.
  - A one-line operator comment (if escalation happened mid-round).
  - "Did the author address these? Yes / no / partially (with residuals)?"

Never re-review unchanged code. Focuses the reviewer + saves tokens + matches human code-review practice.

---

## 8. Telemetry per LOCK

Append to `pipeline/engineering/lock_history.v1.jsonl` one record per module LOCK:

```json
{
  "module": "pipeline.sovereignty.crypto_primitives",
  "blueprint_section": "section_1_sovereignty_envelope.md",
  "blueprint_version": "v6",
  "lock_timestamp_utc": "2026-04-19T18:30:00Z",
  "author_tokens": 12450,
  "reviewer_tokens_total": 47800,
  "reviewer_tokens_per_seat": {"codex": 9200, "qwen3-32b": 9100, "llama-3.3-70b": 9600, "gpt-oss-120b": 9900, "kimi-k2": 10000},
  "wall_clock_seconds": 312,
  "lines_of_code": 217,
  "tests_added": 18,
  "failure_codes_covered": ["F-CRYPTO-01", "F-CRYPTO-02", "F-HASH-INVALID"],
  "committee_rounds": 1,
  "retry_count": 0,
  "findings_surfaced": 0,
  "review_verdict": "all_pass"
}
```

This provides the empirical basis the A7.3 white-glove calibration needs at ship time. Operator sees trend lines.

---

## 9. Engineering lessons file format

`pipeline/engineering/review_lessons.v1.md` format mirrors `lessons.md` in structure (L-NNN entries with frequency, severity, pattern, pre-check, origin). Engineering-lesson IDs prefixed `E-NNN` to distinguish from grant-lessons `L-NNN`. Example:

```
## E-001 — Hash-binding primitives missing constant-time comparison
- First observed: 2026-04-19
- Frequency: 1 occurrence
- Severity: HIGH
- Pattern: Primitive hashes + equal compares using `==` instead of `hmac.compare_digest` opens timing side channel.
- Pre-check: Every hash-binding module spec card MUST have a "constant-time compare" row. Author's self-audit verifies it.
- Origin: Round A Code Thesis Committee, Kimi K2 finding on crypto_primitives.py v1.
```

---

## 10. Risk register (for the engineering flow itself)

| Risk | Mitigation |
|---|---|
| Over-engineering pressure (especially on crypto) | Blueprint is the forcing function. Stub-and-move-on when spec says stub. Reviewers flag over-implementation. |
| Reviewer disagreement | L-005 two-audit-then-escalate. Disagreement is expected; treat as signal not failure. |
| Context decay per window | Per-module LOCK is a natural handoff. Close current window + fresh next window when context > 65%. |
| Blueprint-code drift | §4.6 BLUEPRINT_DEPS declarations + drift-check script. |
| Provider SDK drift | §4.5 adapter layer. |
| Committee-review cost | §6 prompt caching + §7 delta reviews + §2 module batching. |
| Test environment drift | `.venv/` pinned Python version; `pyproject.toml` declares deps. |
| Git-dependency regression | §4.14 explicit rule; L-006 reminder in every spec card. |

---

## 11. Spec card template

Every module spec card follows this structure:

```markdown
# Spec card — pipeline.<section>.<module>

**Blueprint anchor:** `pipeline/blueprint/v0.1/section_N_*.md` §X.Y (version vN)
**Blueprint hash-at-card:** `<16-char-sha3-512-prefix>`
**Spec-card version:** v1
**Round:** <round-id>
**Futureproofing scope:** <which §4 disciplines apply>

## Public API (goes in `__all__`)

- `foo(arg: type) -> return_type` — [§X.Y.a] description
- `Bar` frozen dataclass — [§X.Y.b] description

## Data structures

- Full dataclass definitions with field-by-field blueprint citations

## Algorithms

- Step-by-step derivation from blueprint §4.X with line-number anchors

## Failure codes

Every `F-*` code from blueprint §6 relevant to this module, with trigger + reason-tag.

## Test surface

### Property tests
- Invariants to express

### Failure-code tests
- One test per F-* code, red-first

### Corpus tests
- Preserved v1 input-expected-output pairs under `tests/corpus/<module>/v1/`

### Shared-Protocol lineage checks (E-026 formal, applies when importing Protocols/types from sibling modules)
- `TestSharedProtocolReuse::test_<symbol>_origin_is_<source_module>` — assert `<symbol>.__module__ == "<fully.qualified.source.module>"`. NEVER `is` identity. NEVER `importlib.reload(module_under_test)` in adversarial tests that later shared-Protocol tests depend on. Under full-suite `sys.modules` eviction, `is` identity fails; `__module__` lineage is the stable contract.

## Test-count and LOC sizing (E-024 formal — 1.5× multiplier)

When the module applies ANY TWO of {E-017 injected Protocols, V1 inline-literal rebind-resistance, E-023 deferred-scope `test_adv_*` docs}, declare the naive floor THEN multiply by 1.5× for the expected ceiling. State explicitly: `floor ≥ N tests, expect ~1.5N given E-024 multiplier`. Spec-card LOC target applies ±25% to the 1.5× figure, not the naive figure. LOC at 1.5× is expected; LOC under-run is the genuine investigation signal.

## Futureproofing commitments

- Public-API surface declared
- Schema version (if artifact-producing)
- Crypto-agile types used
- Drift detection BLUEPRINT_DEPS populated

## Done definition

- All pytest green
- All F-* codes covered
- Spec card every row satisfied or justified
- Lines-of-code within blueprint target ±25% (target = naive floor × 1.5× per E-024 when the trident applies)
- Shared-Protocol lineage tests use `__module__` not `is` (per E-026)
- Live-tree smoke pass (per E-025 candidate) when shipping AST-lint rules
```

---

## 12. When to cut a v0.1.x vs wait for v0.2

Patches to LOCKed v0.1 code that do NOT change the public API or the blueprint are eligible for v0.1.x cut (narrow-edit, no audit round). Changes to public API or semantic behavior are v0.2 candidates and require architecture-level handling (v7-style amendment flow). When in doubt, wait for v0.2 and file under the addendum structure.

---

## 13. Ingress into this process from the existing handoff stack

- Parent handoff: `pipeline/handoffs/v7_round_handoff_2026-04-19.md` (A1-A6 scope)
- Addendum: `pipeline/handoffs/v7_round_handoff_addendum_A7_A8_A9_2026-04-19.md` (AUTHORITATIVE; A1-A12 scope)
- Engineering plan (parent handoff §9): this document replaces §9's sketch as the canonical engineering process.
- v7 Cycle 1/2 (parent handoff §5): still scheduled; this document does not depend on v7 LOCK being done first. Action-over-planning per CLAUDE.md decision framework.

---

## 14. First round — Round A (crypto_primitives + org_slug)

Both modules are pure-function, zero-upstream-dep, stdlib-only. Natural first batch. Spec cards delivered at `pipeline/engineering/spec_cards/round_a_crypto_primitives.md` and `pipeline/engineering/spec_cards/round_a_org_slug.md`. Implementation + tests authored Window-1 Tail 2026-04-19. Committee dispatch to follow after operator reviews spec cards (E1 surface).

---

## 15. Changelog

- 2026-04-19 v1 LOCKED as operating discipline for Tilth v0.1. Authored Window-1 Tail after A7-A12 addendum sign-off.
- 2026-04-21 §11 Spec card template amended to cite E-024 formal (1.5× LOC/test-count multiplier when the Protocols + V1 rebind-resistance + E-023 trident applies; elevated after 6th firing at Scout R7) and E-026 formal (`__module__` lineage inspection for shared-Protocol provenance, not `is` identity under `sys.modules` reload; elevated after 3rd firing at Scout R7, matching E-023's promote-at-second-firing precedent). Done-definition rows added for both. No breaking change to v1 discipline — these are the current-practice rows baked into spec cards scout_round_6..8 already.
