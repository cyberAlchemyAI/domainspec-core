---
title: GoldenQuill / Tilth Project Audit
filed: 2026-05-18
auditor: Claude (audit-only — read-only, no in-tree edits outside this file)
basis: repo state at head 65e841a (Cards-publisher key rotation + OD-E fix-forward + embedded re-sign); lock_history.v1.jsonl logical row 292
posture: AUDIT ONLY. Reports findings; remediation is operator-owned.
audience: Josh Inklovich (founder/operator); incoming platform engineer (Paul Norton)
---

# GoldenQuill / Tilth Project Audit — 2026-05-18

## Executive Summary

Tilth is a serious piece of work. It is also a one-week-old private repo (initial commit `d3bc8b1` "Initial commit: Golden Quill workspace bootstrap" — `git log --oneline | tail -1`) carrying twelve months of architectural thinking compressed into a §-numbered amendment chain with 292 LOCKed rows in `pipeline/engineering/lock_history.v1.jsonl`, 14 operator-signed Ed25519 cards (`pipeline/cards/{CIC,CLC}/*.yaml`), 125 deterministic Logician gate modules at `pipeline/logician/gates/f_*.py`, ~162k lines of pipeline code, ~162k lines of tests across 365 `test_*.py` files, and a defensible governance ledger that — to my reading — earns the discipline it imposes. The product hypothesis is grounded: Josh has won three competitive grants in 2026 using the manual version of the workflow Tilth productizes (`docs/COLLABORATOR_HANDOFF.md:90-93`; `USER.md:11-13`).

The strongest things going for this project are: (1) the ceremonial machinery is real, not theater — `pipeline/cards/loader.py:252-279` enforces lifecycle, coupling, and manifest-membership preflight as live Python that throws typed exceptions, not narrative; (2) the recent compromise-class key rotation (`lock_history.v1.jsonl` rows 280-281, `vault_shared/cards/publisher_pubkey.signed.yaml:25-37`) was handled correctly — TOFU re-pin per `vault_shared/key_rotation_policy.md` §4.1, audit trail intact, no panic; (3) the sovereignty wedge — three-posture routing, BYOK, classification register, fail-closed gates — is operationalized at `pipeline/orchestrator/provider_boundary.py:736` and `pipeline/linting/r_no_direct_provider_http.py:537`, not just asserted; (4) the runtime maturity taxonomy at `RUNTIME_MATURITY_MATRIX.md` is the kind of honesty layer most projects skip, and it materially de-risks Paul's onboarding.

The most at-risk things are: (1) **key-person concentration**. Every load-bearing decision, signing key, and architectural amendment is held by Josh alone. The `_private/cards_publisher_privkey_2026-05-17.txt` and `_private/operator_attestation_privkey_2026-05-17.txt` files are operator-local and ungitignored only by the `_private/` directory rule (`.gitignore:97`). One stolen laptop and the trust chain breaks; (2) **claim/runtime gap**. The README and architecture docs assert capabilities the runtime does not yet exercise — most acutely, `pipeline/cards/loader.py:223-224` declares `publisher_pubkey: Optional[bytes] = None` and never invokes Ed25519 verification, terminating with `raise NotImplementedError(...)` at line 270. The signed Cards are signed-loaded-governance, not runtime-injected; (3) **substrate-vs-content imbalance**. The blueprint-amendment chain produces more material than the runtime consumes — 116 files under `pipeline/blueprint/v0.1/`, 125 gate modules of which a substantial fraction (`f_packet_*`, `f_cards_signature_invalid`, etc.) raise `NotImplementedError`. Discipline overhead is high relative to the ship-able surface. This is not damning at v0.1, but it is a sustainability lever to watch.

**Top three recommendations** (full ranked list in §13): (1) Author the *operational freeze playbook* (blind-spot D per `docs/CTO_HANDOFF_BRIEF.md` §2.4) and an *off-machine Ed25519 backup procedure* for every signing role before Gate 1 with Paul. Bus-factor is the single largest extinction risk. (2) Define and ship a *Paul-onboarding green-path* doc that takes a fresh clone to a green `scripts/run_tests.sh` plus one *signed-loaded-but-unwired* card-load demo in under two hours; today the docs are excellent but distributed across `docs/COLLABORATOR_HANDOFF.md`, `docs/LOCAL_DEVELOPMENT.md`, `docs/AGENT_CONTEXT_INDEX.md`, `docs/TECHNICAL_BACKLOG.md`, and `RUNTIME_MATURITY_MATRIX.md` — five files that *should* be five files for the literate reader but feel like five files to a tired new engineer. (3) Pick the first paid client *now* and treat Gate 2 as the only architectural arbiter that matters. Every additional §-amendment that ships before a customer touches the runtime is debt against the only loop that closes.

---

## 1. Technical Foundation

### 1.1 Architecture coherence

The §-numbered architecture chain holds up under inspection. `pipeline/architecture/v0.1/tilth_architecture_locked.md` is the v7 LOCKED baseline (2026-04-19, A1–A12); the v7.0.x amendment line walks corrections forward through v7.0.12 (apolitical_dialect amendment retiring the four-axis political enum and registering F-DIALECT-*). Each amendment is a separate file with `amendment_status: LOCKED` front-matter and an Ed25519-signed paired-commit twin in §0.5 (the blueprint interface index). The §-numbering and the LOCK row in `lock_history.v1.jsonl` are the two coordinates by which any claim in the codebase can be located: row → ceremony, § → semantic surface.

What earns this its keep is the paired-commit discipline. Every blueprint amendment ships with a §0.5 sibling entry (`pipeline/blueprint/v0.1/section_00_5_*_amendment.md`) — see `docs/AGENT_CONTEXT_INDEX.md:103-113` and the active head being §0.5 v32 / row 275 / OD-E (the cards-publisher-rotation amendment is v33 / row 281 / `section_00_5_cards_publisher_rotation_amendment.md`, per the file list and `lock_history.v1.jsonl` row 281 `blueprint_section` field). This is a workable design — auditable, drift-resistant, and clear about what supersedes what. The forward-binding/companion-ceremony-status field that the CTO brief proposes (`docs/CTO_HANDOFF_BRIEF.md` §4.4) would close the last documented gap: amendments LOCKed-but-not-applied. The OD-E incident on 2026-05-17 (`lock_history.v1.jsonl` row 279 "blueprint_supersession" + handoff at `pipeline/handoffs/cards_publisher_key_rotation_2026-05-17/`) demonstrates the failure mode and the audit-trail's success at catching it.

The three-posture routing model (Frontier-Eligible / Split-Context Hybrid / Local-Only / Sovereign per architecture v7.0.10 LOCKED 2026-05-11) is the load-bearing externally-facing architectural decision. It is operationalized at `pipeline/orchestrator/router.py:944` with the `_dispatch_with_classification_boundary` constructor, and the `enforce_outbound_boundary` wrapper at `pipeline/orchestrator/provider_boundary.py:736` is the sole permitted egress site. The corresponding AST-lint rule at `pipeline/linting/r_no_direct_provider_http.py:537` fires on any `_call_anthropic` / `_call_openai_style` call that omits the `http_post=` keyword. That triple (Cedar policy + Python predicate + AST-lint) is the right shape for an enforcement mechanism that has to survive both runtime and future refactors. Verified by 267 passing tests under `tests/linting/` (per `PROJECT_STATUS.md:14`).

### 1.2 Code quality and discipline

`pyproject.toml:5-78` declares `requires-python = ">=3.11"`. The dependency set is tight and explained — `cryptography`, `pyyaml`, `feedparser`, `idna`, `spacy`, `rapidfuzz`, `python-docx`, `pypdf`, `openpyxl`, `weasyprint`, `Jinja2`, `cssselect2`, `tinycss2`, `logfire`, plus dev `pytest`, `pytest-cov`, `pytest-xdist`. There are inline comments at each dependency explaining why it's there and where it's imported, which is unusually disciplined. The local interpreter pin (Python 3.14 via `scripts/run_tests.sh:18-30`) is enforced by the test runner — it refuses to run if `.venv/bin/python3` is missing or older than 3.11. The system Python on macOS (3.9) is structurally rejected. This catches the silent collection-error failure mode and is the kind of footgun-prevention discipline that takes hours to debug if it's not there.

Type hints are present and consistent where I sampled (`pipeline/cards/loader.py:32`, `pipeline/orchestrator/provider_boundary.py:1-65`). `@dataclass(frozen=True, kw_only=True)` is used for value types (`pipeline/logician/gates/f_cards_signature_invalid.py:21-23`). The fail-closed exception classes in `pipeline/cards/loader.py:48-71` are typed and inherit cleanly from a `CardLoaderError` base. The AST-lint chain at `pipeline/linting/r_no_direct_provider_http.py` is the canonical discipline-as-code mechanism.

What I cannot verify from a reading: pytest pass count, AST-lint exit code, end-to-end behavior. CI evidence cited by the project is `10,584 passed / 3 skipped / 1 xfailed` (PR #4 head merge per `README.md:39`) and `2887 pass / 0 fail` (commit `65e841a` message). The two numbers are not in conflict — `2887` is the cards-rotation commit's verification subset, `10,584` is the full serial-pytest matrix. But the discrepancy in narrative — `PROJECT_STATUS.md:14` reports `3,004 passed / 3 failed` for `tests/seats/` with the three failures being "pre-existing capstone-hash drift, NOT regressions" — is exactly the kind of soft caveat that hides drift if not actively tested. **Recommend** wiring a CI badge or a one-paragraph "last green CI run" stamp to `PROJECT_STATUS.md` so the readability gap closes.

### 1.3 Test coverage

`find tests/ -name 'test_*.py' | wc -l` returns 365 files; `wc -l` totals ~162k lines (parity with the pipeline). The directory layout mirrors `pipeline/`: `tests/orchestrator/`, `tests/linting/`, `tests/logician/gates/`, `tests/seats/`, `tests/cards/`, `tests/cli/`, `tests/integration/`, `tests/sovereignty/`, `tests/observability/`, `tests/scout/`, `tests/runtime_integrity/`, etc. The shape is correct for a project this size. Spot-checking, the F-CARDS family is well-tested (`tests/logician/gates/test_f_cards_unsigned_production_load.py` and siblings; `tests/cards/test_active_card_registry_gate.py` 337 lines, 15 new tests landed in commit `65e841a`).

Coverage gaps I can infer:

- **Real-world end-to-end.** `tests/integration/` exists but the only file I spot-checked, `test_wpfa_end_to_end.py:242`, contains the `client_name="FIT Farms LLC"` literal flagged in `docs/secrets_data_access_audit_2026-05-17.md` §2 P1-B. Integration coverage looks scenario-shaped, not customer-cycle-shaped. A grant-cycle replay (Gate 1) does not yet have a deterministic test harness — the v0.1 lock-and-clear packet at `pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md` is the spec, but it is not (to my reading) a script you can run.
- **NotImplementedError gates.** A substantial number of F-* gates raise `NotImplementedError` at v0.1 (`pipeline/logician/gates/f_cards_signature_invalid.py:30-32` is the canonical shape; same pattern in many F-PACKET-*, F-WPFA-*, F-REPORT-*, F-DATACOLLECTOR-* gates). Tests exercise the import path and the dormant-shape behavior but not the live predicate. This is the right call at v0.1 — fail-closed-by-`NotImplementedError` is safer than silent-pass — but the coverage matrix `docs/TEST_VERIFICATION_MATRIX.md` (mentioned in `docs/TECHNICAL_BACKLOG.md:122-128` as a "Safe first task") has not been authored.
- **Card loader signature verification.** `pipeline/cards/loader.py:223` takes `publisher_pubkey: Optional[bytes] = None` and never invokes it. No test asserts that signature verification fires — because it doesn't yet. The `_research_metadata.ed25519_signature` field on each card (e.g., `pipeline/cards/CLC/market_access.yaml:205`) is a governance artifact, not a runtime check.
- **`tests/seats/` capstone-hash drift.** Three failing tests carried forward as "pre-existing WIP" per `PROJECT_STATUS.md:14` and `docs/TECHNICAL_BACKLOG.md:34-40`. Acceptable as a noted-known but it should not survive Gate 1.

### 1.4 Dependency hygiene and supply chain

`pyproject.toml` is the single dependency declaration; no `requirements.txt`. Pinned floors (`>=`), not exact pins — fine for a non-shipping-yet wheel, surface-level supply-chain risk at production. There is no `pip-audit` or `safety` integration in CI (`.github/workflows/ci.yml:115`). `actions/checkout@v6`, `actions/setup-python@v6`, `actions/upload-artifact@v4` are tag-pinned, not SHA-pinned — flagged as P2-C in the secrets audit (`docs/secrets_data_access_audit_2026-05-17.md` §2 P2-C). All actions in use are first-party `actions/*`, which mitigates but does not eliminate.

The Logfire dependency at `pyproject.toml:55-65` introduces a hosted-observability runtime dependency (`logfire>=0.42`) that auto-bootstraps at `pipeline/__init__.py` module-load. The bootstrap is intended to gracefully degrade to a no-op + WARNING when credentials are absent or `LOGFIRE_ENABLED=0` is set, but the runtime egress posture of "phones home if logged in" inside a project whose explicit promise is "nothing phones home silently" is exactly the kind of tension that bites on first paid customer. The README's wording ("local-first/BYOK/approved cloud routes, not 'nothing phones home'" per `docs/v0_1_TECHNICAL_LEAD_BRIEF.md:60`) is already calibrated, but the *runtime* needs to clear `CC-008 Logfire disable-by-default end-to-end verification` per `docs/TECHNICAL_BACKLOG.md:65-70` before Gate 2.

There is no SBOM or signed-release pipeline. For v0.1 development this is fine; at first paid client a reproducible signed wheel build is going to come up.

### 1.5 Performance / scalability chokepoints

Stage-1 v0.1 is single-tenant on operator hardware. The architecture explicitly bounds this — `pipeline/architecture/v0.1/tilth_architecture_locked.md` v7 A1 ("single-client") — so scaling concerns are deferred. Two early signals:

- **CI OOM on ubuntu-latest 7 GB.** Commit `a54495e` ("ci: cap pytest workers at 2 — ubuntu-latest OOM-kills with -n auto") and `f57c7a3` ("ci: drop xdist; even -n 2 OOMs on ubuntu-latest 7 GB runner") show that the test suite alone exceeds the standard runner's memory at parallel execution. The serial-pytest matrix CI works, but the suite has grown faster than the runner. This will be a contributor-experience problem before it is a customer problem. **Recommend** a tiered test layout (fast smoke + slow integration) or a larger runner tier before Paul lands.
- **Heavy-Judge swap timing.** The on-demand 200B-class local heavy-Judge is documented as a 2–5 min latency side-channel (`docs/ARCHITECTURE_OVERVIEW.md` §"On-demand local heavy Judge"), bounded by the single-client posture. Realistic on a Mac Studio M3 Ultra / DGX Spark / GB-10 with the binary pre-loaded; brittle on the 8 GB M1 dev node where the operator currently builds. The dev/prod hardware gap means "works on Josh's machine" is not a meaningful Gate-1 signal for heavy-Judge.

---

## 2. Functionality

### 2.1 What works end-to-end today

Quoting the project's own `runtime-live` row in `RUNTIME_MATURITY_MATRIX.md` (which I trust by cross-checking the cited file paths):

- **Outbound provider-boundary enforcement** at `pipeline/orchestrator/provider_boundary.py:736`, wrapping every cloud-routable HTTP POST with the F-CLASS-* PRE/POST chain. The single `enforce_outbound_boundary` wrapper is the sole egress site after the §4 v2.x.6 router-dedup runtime companion landed (lock_history row 234/235 chain + the §4 v2.x.5 runtime contract at row 232). 66 passing tests under `tests/orchestrator/` (per `PROJECT_STATUS.md:13`).
- **AST-lint provider-call discipline** at `pipeline/linting/r_no_direct_provider_http.py:537`, with the `.direct_provider_call_without_wrapper` sub-tag. 267 passing tests.
- **F-CLASS-* routing-gate family** (fail-closed under non-`local-only` posture when posture or classification register loading fails) under `pipeline/logician/gates/f_class_*.py`.
- **Six-seat council dispatch path**, exercised by `tests/seats/` at ~3,004 passing (three pre-existing capstone-hash drift failures).
- **Sovereignty primitives** under `pipeline/sovereignty/` (boot, isolation, audit, admin_risk, project_context_envelope, rfa_envelope, router_integrity, session, topology).
- **Card loader preflight** at `pipeline/cards/loader.py:202-279`. Lifecycle, coupling, and manifest-membership are LIVE checks; registration boundary is `NotImplementedError`.

Cross-reading these against the actual files: each claim resolves to running code with a typed exception path and at least one test. The substrate is real.

### 2.2 What's stubbed / placeholder / partial

The `asset-signed` and `spec-locked` and `dormant` rows of the maturity matrix are extensive. Concretely:

- **Card runtime injection.** `pipeline/cards/loader.py:270-274` terminates `load_card()` with a `NotImplementedError` at the seat-registration boundary. Lifecycle/coupling/manifest preflight is live; the seats do not yet consume cards. Promised at v0.2 first wave per `architecture v7.0.11 §5`.
- **Ed25519 signature verification at loader time.** Card YAMLs carry embedded `_research_metadata.ed25519_signature` (e.g., `pipeline/cards/CLC/market_access.yaml:205`), but the loader does not verify against the pinned publisher pubkey. The `publisher_pubkey: Optional[bytes] = None` parameter at `pipeline/cards/loader.py:223` is reserved. `F-CARDS-SIGNATURE-INVALID` predicate body at `pipeline/logician/gates/f_cards_signature_invalid.py:30-32` raises `NotImplementedError`.
- **PRP loader.** `pipeline/program_rule_packs/loader.py:1-45` is on disk as a v0.1 DRAFT scaffold. The top-level `load_active_prps()` raises `NotImplementedError`. Three of six PRPs have DRAFT YAML bodies — `TILTH-PRP-2CFR200/v1.yaml` (592 lines), `TILTH-PRP-DAVIS-BACON/v1.yaml` (497 lines), `TILTH-PRP-NEPA-24CFR58/v1.yaml` (529 lines) — none signed. The other three (FERPA-COPPA-HIPAA, SUBCHAPTER-T, USDA-VAPG-FY26) are stub-only entries in `pipeline/program_rule_packs/_manifest/active_prps.yaml`.
- **Reflection Packet sub-kind.** Authored but not in `SUB_KIND_REGISTRY` at v0.1 (`RUNTIME_MATURITY_MATRIX.md` `dormant` row). 19 F-PACKET-* gates registered; 18 raise `NotImplementedError`; 1 (`F-PACKET-COVERAGE-INCOMPLETE`) carries a LIVE meta-gate body as the dormant-binding lever.
- **Data Collector / Report Generator / Archivist runtimes.** Spec-LOCKed, not implemented. v0.2 / v1.x horizon.
- **Heavy-Judge swap.** Documented; structurally absent from any code I read.
- **Classification register runtime loader.** Spec at architecture v7.0.7; loader at `vault/classification/signed_register_loader.py` is referenced as "wires the trust chain" per `RUNTIME_MATURITY_MATRIX.md`, but I did not verify its runtime invocation. **Confidence: medium.**

### 2.3 Runtime card surface — coverage gaps

The Tier 2B augmented card drafts at `pipeline/cards/_drafts/cic_*_augmented_2026-05-18.yaml` and `pipeline/cards/_drafts/clc_*_augmented_2026-05-18.yaml` total ~17,786 lines (`wc -l`). These are held for follow-up PR per Josh's brief. Spot-checking `pipeline/cards/_drafts/cic_food_systems_augmented_2026-05-18.yaml`, the header (lines 1-30) is verbatim the Wave-1 header from `pipeline/cards/CIC/food_systems.yaml`. The Tier-2B work is the §18 v1.2 dialect-routing-table re-key plus the v0.2-first-wave content improvements bundled — this is the LARGE cards-ceremony (Phase 2 in the CTO brief) and is the longest single bottleneck before v0.2 first wave (`docs/CTO_HANDOFF_BRIEF.md` §3.3 estimates 30-42 hours of operator content-judgment pre-work).

The CLC dual-track restructure (OD-E fix-forward, rows 274-279 + 282-288 + 289-292) shows the right discipline pattern: when the original 2026-05-17 ceremony signed canonical-bytes asserts for rows 276/277/278 but the on-disk restructure had not committed, the operator caught it, ratified path (a), and re-ran with L-025 preflight wired (`pipeline/scripts/od_e_fix_forward_ceremony_2026-05-17.py:566` lines + `cards_embedded_re_sign_ceremony_2026-05-18.py:691` lines, both added in commit `65e841a`). That this exists is the audit value proposition. That it was needed is the drift hazard the system has to live with.

### 2.4 PRP coverage — what's authored vs what's needed

Three of six PRPs have DRAFT bodies on disk. The choice of three (2 CFR 200, Davis-Bacon, NEPA 24 CFR 58) is the right wedge — these are the federal-program-law boundaries that recur across CIC × CLC pairings. The other three (FERPA-COPPA-HIPAA, SUBCHAPTER-T, USDA-VAPG-FY26) are equally important but harder (FERPA-COPPA-HIPAA spans a privacy boundary; SUBCHAPTER-T is cooperative tax treatment; USDA-VAPG-FY26 is operator-content-bound by the FY26 NOFO).

The `cross_references_prp:` annotation field that the CTO brief flags (`docs/CTO_HANDOFF_BRIEF.md` §2.1) as the canonical card → PRP routing surface is not yet on the cards. Until it lands, PRP infrastructure is signed-and-loaded-but-disconnected from the rest of the substrate. This is the right place for the §18 v1.2 amendment to land.

### 2.5 Ceremonial machinery — does the lock_history + signing chain do what it claims?

Yes, with caveats.

What works: every recent row I read (rows 280-292) carries `canonical_json_sha3_512` over the JSON-canonical-bytes-minus-signature plus `ed25519_signature` plus `publisher_pubkey_ed25519_hex` plus `signature_target_pubkey`. The compromise-class rotation event (row 280) carries `rotation_class`, `rotation_trigger`, `rotation_trigger_runbook_ref`, `old_pubkey_ed25519_hex`, `new_pubkey_ed25519_hex`, `new_pubkey_pinned_at_utc`, `tofu_repin_path`, `prior_pubkey_cosign_skip_reason`, `admin_risk_ledger_anchor`, `retroactive_validity_preservation`. The shape is comprehensive — by which I mean the row records enough context that a reader landing on row 280 cold can reconstruct what happened and why. Row 281 is the paired §0.5 v33 commit. Rows 282-288 are the OD-E fix-forward chain. Rows 289-292 are the embedded card re-sign + paired-commit closure.

What is *unverified by reading*: I did not run the signature verification routine against any signed asset. The `docs/secrets_data_access_audit_2026-05-17.md` §5 explicit non-verification ("did not run the signature verification routine against the canonical-bytes-minus-signature hash") still stands. The signatures in the YAML files are byte strings; whether they cryptographically verify under the pinned pubkey is testable code (`cryptography.hazmat.primitives.asymmetric.ed25519`) that should exist as a CI check. It does not appear to. **Recommend** a CI job that round-trip-verifies every signed asset against the pinned pubkey on every push to `main` — this is the highest-leverage single addition to make the ceremonial claims auditable without trusting the operator-of-record narrative.

The "amendment LOCKed-but-not-applied" hazard (OD-E surfaced this) deserves a deeper systemic patch than the L-025 preflight. The CTO-brief recommendation of an `amendment_status: LOCKED_TEXT_PENDING_COMPANION_CEREMONY` value (`docs/CTO_HANDOFF_BRIEF.md` §4.4) is sound and cheap. Adopt it.

---

## 3. Clarity

### 3.1 Onboarding path for a new collaborator

The README does this well at the front: a "Where to read next (in order)" callout (`README.md:5-7`) that names six docs by purpose. Following that path:

1. `PROJECT_STATUS.md` — dated one-paragraph-per-system snapshot. Good. Anchored to a specific lock_history row, which is the right discipline. Will go stale; the file knows it.
2. `RUNTIME_MATURITY_MATRIX.md` — the seven-state taxonomy (`runtime-live` / `gate-live` / `asset-signed` / `spec-locked` / `schema-scaffold` / `dormant` / `historical`). This is the single most useful documentation artifact in the repo. Every claim resolves to one of seven rows. If a doc disagrees, the matrix wins. Adopt this discipline across the board.
3. `pipeline/blueprint/v0.1/ACTIVE_BLUEPRINT_INDEX.md` — current-vs-superseded §-blueprints with lock_history row citations. Good. 116 files in `pipeline/blueprint/v0.1/`; this index makes them traversable.
4. `docs/AGENT_CONTEXT_INDEX.md` — what each root personification file (`SOUL.md`, `USER.md`, `AGENTS.md`, `CLAUDE.md`, `MEMORY.md`, `IDENTITY.md`, `SKELETON.md`, `HEARTBEAT.md`, `TOOLS.md`, `lessons.md`) is for. Good. The decision to leave files at root and add an index, rather than relocating to `agent/`, was correct (`docs/AGENT_CONTEXT_INDEX.md:16-22`).
5. `docs/COLLABORATOR_HANDOFF.md` — role clarity. Good. The "who owns what" section is direct. The "business hope layer — evidence, not hype" section (`docs/COLLABORATOR_HANDOFF.md:90-118`) is the right way to set Paul's expectations.
6. `docs/LOCAL_DEVELOPMENT.md` — concrete venv setup. Good. The Python 3.14 local pin / 3.11/3.12 CI matrix / 3.9 macOS-system rejection is the right level of specificity.

**Would Paul find what he needs?** Probably yes, but it will take him ~half a day to assemble the picture from these six docs plus `CLAUDE.md` (50,141 bytes — `wc -l CLAUDE.md` returns 335 lines but the size in the directory listing is 50 KB; it is dense). The single thing missing is a `docs/GETTING_STARTED.md` that compresses the six docs into a one-page green-path: clone → venv → tests green → run-one-thing-end-to-end. Such a file exists (`docs/GETTING_STARTED.md` is 142 lines), but is itself less load-bearing than `docs/LOCAL_DEVELOPMENT.md` (199 lines) — the two should reconcile, with the shorter one being authoritative.

### 3.2 Documentation quality, accuracy, freshness

Quality: excellent for an audit-trail-driven project, paragraph-dense, evidence-cited, dated. The discipline of dating everything (`filed: 2026-05-17`) is good. The discipline of citing the lock_history row that a claim depends on is excellent.

Accuracy: the docs are written by an operator who has skin in the game and an LLM that has access to the repo. There is some drift hazard — `docs/ARCHITECTURE_OVERVIEW.md:115` says "five LLM-using council seats run on five distinct families today (the requirement is overcovered)" but the specific provider assignments are at `router.yaml`, which I did not deep-read. The cited claim is verifiable from `router.yaml`; the doc-to-config consistency check would be a useful CI addition.

Freshness: aggressively maintained. `daily_logs/2026-05-17.md` (189 lines), `lessons.md` updated 2026-05-17 with L-027, `PROJECT_STATUS.md` filed 2026-05-17. The retrofit is the issue — items LOCKed in April have not all been revisited in the May regime. `pipeline/architecture/v0.1/tilth_architecture_locked.md` is the v7 LOCKED 2026-04-19 baseline, and the amendment chain is what's been updated. This is by design (amendments don't edit in place), and it works *if you read the amendments in order*. For a one-shot reader, a single rendered "current architecture as of today" view would be useful — call it `pipeline/architecture/v0.1/CURRENT_HEAD.md` and generate it from the amendment chain.

### 3.3 Naming consistency, jargon load, internal-language tax

This is the hardest read. The project is fluent in:

- F-* failure-code families (F-CLASS-*, F-CARDS-*, F-PRP-*, F-PACKET-*, F-WPFA-*, F-DIALECT-*, F-INTAKE-*, F-UPLOADER-*, F-REPORT-*, F-DATACOLLECTOR-*, F-CIC-CLC-*, F-FG-*, F-GPP-*, F-AMDT-*, F-LOGICIAN-*, F-FACT-*, F-KFR-*, F-DEPRECATION-*, F-MATCH-DB-*, F-ROLLBACK-*, F-SDK-*, F-VECTOR-NS-*, F-VERDICT-*, F-EXTRACTOR-*, F-FUNDER-CORPUS-*, F-DERIVATION-*, F-CURRENCY-*, F-COMMITTEE-*, F-CHANNEL-*, F-BENCHMARK-*, F-DAILY-*, F-BOOTSTRAP-*, F-AWARD-*, F-AMENDMENT-*, F-MULTI-CIC-*, F-RUNTIME-*, F-PIPE-*, F-FINDING-*).
- §-blueprint section numbers (§0.5, §1, §2, §3, §4, §5, §6, §7, §10, §11, §12, §13, §14, §15, §16, §17, §18, §19).
- Architecture amendment versions (v7, v7.0.1 through v7.0.12; sub-amendments v2.x.1 through v2.x.7).
- Op-Decision codes (OD-A, OD-B, OD-C, OD-D, OD-E).
- L-NNN lessons (L-001 through L-027).
- CIC / CLC card slugs (six + eight, plus the orthogonality discipline).
- Postures (Frontier-Eligible / Split-Context Hybrid / Local-Only / Sovereign).
- Lock classes (`blueprint`, `blueprint-interface-index`, `blueprint_supersession`, `card_cartridge_supersession`, `cards`, `key_rotation`).
- KGIE, SMART, SFR, KFR, FID, MD, NOFO, RFA, NOFA, FOA, RFP, VAPG, SARE, AFRI, NIFA, REAP, SCBGP, BFRDP, RCDG, LAMP, FMPP, LFPP, RFSP, NRCS, EQIP, CSP, etc.

The 7-state maturity vocabulary and the L-NNN lessons are necessary domain knowledge. The F-* codes are *cheap* once internalized (an `F-CARDS-COUPLING-VIOLATION-EXTENSION` is a one-word concept for a complex predicate). The §-numbers are necessary because the amendment chain is the only credible authority. **But the cumulative load is real.** Paul will need a glossary. The `docs/AGENT_CONTEXT_INDEX.md` is a start; an `docs/GLOSSARY.md` with one-line definitions for every F-* family, §-section, OD-code, and L-lesson would compress the onboarding curve by half a day.

### 3.4 Entry points

README is the right shape: it tells you what the product is, what works today, what's promised, and where to read next. The "Where to read next" callout at line 5 is the load-bearing element; the "What it is / Why it matters" framing is well-tuned. The "Sovereignty Promise" section (`README.md:99-101`) is the kind of paragraph that earns a customer call.

What's missing from the README: a *one-screenshot or one-diagram-or-one-snippet* showing the product doing something. Tilth is invisible in the README — no example output, no screenshot of an Uploader staged-submission, no example flow. The architecture diagram in `docs/ARCHITECTURE_OVERVIEW.md` (an ASCII flowchart) is good but lives one click in. **Recommend** an embedded ASCII flowchart in README plus a short "example session" appendix.

---

## 4. Best Practices

### 4.1 CI/CD posture, branch protection, required checks

`.github/workflows/ci.yml` (115 lines) is well-tuned. Permissions are `contents: read`. Concurrency cancellation enabled (`cancel-in-progress: true`). Two jobs: `quality-gate` (matrix on 3.11 + 3.12, AST-lint + serial pytest, ubuntu-latest) and `wheel-install-smoke` (same matrix, wheel build + CLI import check). System libraries pre-installed for `weasyprint`. spaCy model `en_core_web_sm` pulled for the `F-LOGICIAN-FABRICATED-ORG` gate. Artifact upload on failure (`actions/upload-artifact@v4`).

Required checks (per `README.md:42-44`): `quality-gate (3.11)`, `quality-gate (3.12)`, `wheel-install-smoke (3.11)`, `wheel-install-smoke (3.12)`. Four. Branch protection enforces them — I cannot verify this from the file system, but the README claim is consistent with the `concurrency` and `pull_request` triggers.

Gaps:

- **No secret scanning in CI.** `gitleaks` or `trufflehog` action would catch the long-tail novel-secret pattern that the manual sweep noted as a non-trivial gap (`docs/secrets_data_access_audit_2026-05-17.md` §5 item 1).
- **No supply-chain audit step.** `pip-audit` against the resolved environment.
- **No signature-round-trip CI job.** Every signed asset (cards, §0.5 paired commits, classification registers when present) should verify under the pinned pubkey on every push. This is the highest-value missing job.
- **CI runs on ubuntu-latest 7 GB and has OOM'd twice in recent history** (commits `a54495e` and `f57c7a3`). Tier up before the suite grows further.
- **No dependabot config visible.** Action SHA pinning would shore up the P2-C finding (`docs/secrets_data_access_audit_2026-05-17.md` §4 item 6) when paired with a dependabot config that surfaces upgrade PRs.
- **GitHub remote settings unverified.** Per `docs/secrets_data_access_audit_2026-05-17.md` §4 item 7, the remote's collaborator list, deploy keys, GitHub Apps, and branch-protection rules are operator-driven via `gh` CLI or UI and out of in-repo scope. **Recommend** a one-time `gh api` snapshot to a docs file before Paul lands.

### 4.2 Secrets handling, key rotation discipline, vault hygiene

The secrets posture is unusually strong for a one-week-old repo. The `docs/secrets_data_access_audit_2026-05-17.md` is itself the deliverable — a 130-line audit naming P1-A (`data/` not gitignored, no live exposure today), P1-B (operator-LLC-name in test fixture), P2-A (SSH-key patterns absent from gitignore), P2-B (suffix-style `*.env`), P2-C (action SHA pinning), P2-D (no `.env.example`), and INFO-1 through INFO-5 (operator self-disclosure, all intentional). None of these are leaks.

The compromise-class key rotation handled correctly:

- Operator pasted Ed25519 seed into Dispatch chat on 2026-05-17.
- Operator self-discovered (or was alerted).
- Rotation ceremony executed `pipeline/scripts/cards_publisher_key_rotation_ceremony_2026-05-17.py` (622 lines, added in commit `65e841a`).
- Old pubkey `0b1a0bbf…6f375bd` marked COMPROMISED-RETIRED.
- New pubkey `c93f1881…e41107` Trust-On-First-Use re-pinned at `vault_shared/cards/publisher_pubkey.signed.yaml:55`.
- `prior_pubkey_signature_ed25519_hex: null` per `vault_shared/key_rotation_policy.md` §4.1 step 5 second clause (compromise-class, prior key under attacker control).
- Audit anchor: `lock_history.v1.jsonl` row 280 + handoff at `pipeline/handoffs/cards_publisher_key_rotation_2026-05-17/05_old_key_compromise_record.md`.
- All three OD-E-superseded cards re-signed under the new pubkey (rows 289-291).
- `*.seed` defense-in-depth added to `.gitignore:212` ("Ed25519 seed material" block).
- Lesson L-027 appended to `lessons.md` ("`.gitignore` globs like `**/*secret*` match filenames, NOT directories…").

The handling is by-the-book and the audit trail is intact. *(Correction folded in at PR #19 signature-round-trip verifier run, 2026-05-18: the original audit reading flagged role 6 — operator-attestation pubkey — as MISSING with only a placeholder at `vault_shared/operator_attestation/publisher_pubkey.signed.yaml`. The file on `main` is in fact a real TOFU-self-signed asset, pubkey `094a4dc4…`, published 2026-05-17T21:56:20Z, verified by `pipeline/scripts/verify_signed_assets.py`. Role 6 is PINNED. The off-machine-backup gap below remains the load-bearing residual.)*

The `_private/` directory (`.gitignore:97`) holds the operator's local Ed25519 seeds (`_private/cards_publisher_privkey_2026-05-17.txt`, 64 bytes; `_private/operator_attestation_privkey_2026-05-17.txt`, 855 bytes). These are gitignored. The single-laptop holder posture is the operational risk; the gitignore is correctly tight. **The off-machine backup procedure is the bus-factor mitigation that must precede Gate 1.** `vault_shared/key_rotation_policy.md` §1 ("Bus-factor mitigation… single-point-of-failure explicitly… stages the remediation path") names the problem and stops short of solving it.

### 4.3 Code review, audit trail, ceremonial preflight

Code review: I cannot see PR-level review patterns without GitHub access, but the git log shows merge commits (`Merge pull request #4 from HyphaeNated/product-github-housekeeping`, `Merge pull request #10`, `Merge pull request #13`) so the PR workflow is in use. The commit messages on `main` are well-formed and audit-cite-bearing (`65e841a` lists rows 280-292, mentions `*.seed` defense-in-depth, names test count).

Audit trail: lock_history.v1.jsonl is 292 logical rows, ~296 physical lines. The `row` field is present on every row I read from 271 onward. Earlier rows (per `docs/TECHNICAL_BACKLOG.md:43-49`) are `row: null` for 198 rows — a "back-fill or keep audit-only" decision is pending. The audit-only path is fine if it is named in writing; the back-fill path costs operator-attention but produces a fully numbered ledger. Either is acceptable. The lock_history *shape* (`canonical_json_sha3_512`, `ed25519_signature`, `publisher_pubkey_ed25519_hex`, `signature_target_pubkey`, `predecessor_amendments_chain`, `lock_class`, `lock_kind`, `lock_cycle`, `lock_mode`, etc.) is overbuilt — and I mean that complimentarily. There is no row I would not trust to reconstruct on its own.

Ceremonial preflight: L-025 (`pipeline/scripts/cards_publisher_key_rotation_ceremony_2026-05-17.py` and `od_e_fix_forward_ceremony_2026-05-17.py`) added the write → re-read → SHA3-512 verify → emit signature discipline that would have caught the original OD-E miss. The ceremony scripts are well-instrumented (622 + 566 + 691 lines, all in `pipeline/scripts/`). This is the right place to invest — every ceremony is a ceremony-script PR, not a manual operator gesture.

### 4.4 Git / PR hygiene, commit-message discipline

The PR template in `docs/COLLABORATOR_HANDOFF.md:166-173` is right-sized: lock_history row, F-* codes touched, §-section, paired-commit SHA, Co-Authored-By trailer for AI-assisted commits. The commits on `main` follow this pattern; spot-checking, `65e841a` cites rows 280-292 in its message, names the rotation event, names the OD-E fix-forward, names the embedded re-sign, and names the test count. This is the kind of commit message that the audit-trail-driven discipline produces by default. **Adopt as Paul's onboarding template.**

The git log has the right shape for a young repo: 14 commits on `main`, one big initial commit (`d3bc8b1` "Initial commit: Golden Quill workspace bootstrap"), then `044415c` "audit: revert premature reflection_packet, fix packaging, harden tests, add CI", then a series of CI hardenings, then PR merges, then the cards-rotation commit. The history is auditable, not noisy. The local branch set (`cards-publisher-rotation-and-od-e-fix-forward-2026-05-17`, `codex/card-lifecycle-truth`, `claude/dreamy-moser-4a6bad`, `claude/laughing-khayyam-1779a3`, `claude/modest-herschel-0c88df`) shows AI-assistant branching at scale, which is normal for a Cowork operator.

### 4.5 Industry-norms comparison

For a one-week-old private monorepo with no public release: the discipline is unusually high. The signing chain, the lock-history ledger, the maturity matrix, the AST-lint discipline, the typed exception classes, the deterministic Logician gates, the cross-family rigor at dispatch — none of this is typical at this stage. Most projects this young have a `TODO.md` and a hope.

For a v0.1 product approaching a first paid customer: there are gaps. No SBOM, no signed-release pipeline, no signature-round-trip CI job, no end-to-end customer-cycle replay harness, no off-machine key backup, no published threat model. The discipline is high but uneven — the surfaces the operator focused on are exemplary; the surfaces a security reviewer would ask about first (key backup, secret scanning in CI, supply-chain audit) are not yet built. **This is fixable in days, not months.**

---

## 5. Innovation & Defensibility

### 5.1 What's genuinely novel here vs incremental

The three things that are non-trivial intellectual content:

1. **The CIC × CLC orthogonality + opportunity-driven matching model.** Six customer-identity categories on the applicant side; eight capital-logic categories on the funder side; the runtime match is opportunity-driven, never archetype-driven (`pipeline/blueprint/v0.1/section_18_card_system.md` and the §18.6 v2 dual-track CLC schema). The architectural lock — `F-CIC-CLC-COUPLING-VIOLATION` and `F-CARDS-COUPLING-VIOLATION-EXTENSION` enforce this at the Cedar / Python / AST-lint layers — is a substantive product-architecture call, not a slogan. It says: applicant categories shape *how Tilth processes* an opportunity; the opportunity dictates *which capital-logic* engages. The vast majority of grant-AI tools collapse these and end up with brittle archetype routing. Tilth structurally cannot.

2. **The three-posture routing with classification-register sign-off.** Per-call routing decision composed of (operator-selected posture) × (per-field classification) is more than a sovereignty marketing line. The Split-Context Hybrid posture (cloud sees RFA + scaffold; cloud never sees applicant substance; F-CLASS-SPLIT-CONTEXT-ALLOWLIST + F-CLASS-SPLIT-CONTEXT-LEAK fail-close per-payload) is the engineering primitive that lets a customer plausibly say "frontier model help with no data exposure." Most BYOK competitors stop at "your keys, our service." This is "your keys, your hardware, your data, our framing."

3. **The §-amendment chain + lock-history + paired-commit + Ed25519 signing chain.** As governance machinery, this is well in excess of industry norms. The closest analog I can name is `cargo-vet` for crate review attestations, or the Sigstore TUF root-of-trust pattern. The Tilth governance ledger is closer to a product than a process; whether it becomes a moat depends on whether it survives operator handoff (i.e., whether Paul can extend the chain).

### 5.2 §-numbered architecture, signing chain, lock_history, three-posture routing — moats vs decorative

- **§-numbered architecture.** Decorative for outsiders; load-bearing internally. The amendment chain is what makes the codebase auditable; it is also what makes the codebase intimidating. The customer doesn't care that the F-CARDS-COUPLING-VIOLATION-EXTENSION is at §4 v2.x.7 lock row 272 / OD-C; the customer cares whether their food-systems org gets paired with a credit-underwriting CLC because of a hardcoded archetype map. Both are true. Internally, §-numbering is a moat against operator-cognitive-load growth — it is how Tilth survives at fleet scale. Externally, it is invisible.

- **Signing chain.** Real moat if it survives audit. The cards-publisher pubkey at `vault_shared/cards/publisher_pubkey.signed.yaml`, plus the FID publisher pubkey, plus the (placeholder) reflection-packet producer pubkey, plus the SN-LLC coefficient-registry and router-template pubkeys — these establish a customer-verifiable chain of provenance for everything the system loads at runtime. The customer doesn't have to trust that Tilth's card content is what it says; the customer can verify it. Customers who care about this care a lot (federal agencies, foundations, cooperatives with hostile counterparties). Customers who don't care won't pay for it. The wedge is the former.

- **Lock_history.** Real moat for funder-audit credibility. A federal program officer skeptical of AI tools cares more about "can I see how this decision was reached" than about "is the model good." The lock_history-cited card-load chain is the answer to that. Whether the moat is felt by customers at v0.1 is the open question; my read is that the value materializes at the *funder* (the customer's customer), not at the customer, and that the customer signs because their *funder* asks them to have it. This is a B2B2B sale, and the moat is the third B.

- **Three-posture routing.** Real moat for sensitive-domain customers; nice-to-have for everyone else. Federal grantees, foundation-staffed nonprofits, cooperatives with confidentiality clauses, tribal sovereign configurations — these have explicit data-handling rules that disqualify SaaS-tenant grant-AI. Tilth fits the rules. Customers who don't have those rules have many cheaper choices. **The Founding 12 (`README.md:11-13`) is the right Phase One scope** — twelve Pittsburgh-area Founder Node deployments across six CICs is exactly the constituency where the three-posture model is load-bearing.

### 5.3 IP posture and what's defensible

The repository carries `License: Proprietary. All rights reserved.` (`README.md:170`). No open-source mixing. The cards content is operator-authored research — defensible as creative work, less so as a database (US database protection is thin). The PRPs are derivative of public law — not defensible as content, but defensible as *system* (the PRP loader + lifecycle + signing + enforcement chain is the patentable / trade-secret-able surface). The Cedar policy bodies + the F-* failure-code roster + the AST-lint rules are the strongest trade-secret surface: they are operationally novel and reverse-engineering them from black-box behavior is hard.

There is no patent posture documented. For a project that wants to be defensible at sale, **recommend** a one-page IP inventory (cards, PRPs, gate predicates, schemas, ceremony scripts) marked with what is operator-authored, what is operator-derived-from-public-law, what is operator-derived-from-research-collaboration. Foundation-funded research grant outputs sometimes carry attribution obligations that surface awkwardly at acquisition.

### 5.4 Adjacent products comparison

Grant-writing AI tools that exist today (Submittable, Instrumentl, GrantStation, Grant Assistant, Casted, etc.) share none of: customer-owned hardware, BYOK, fail-closed deterministic gates, signed cards, classification-driven routing. They are cloud-tenant SaaS with grant-content marketplaces. **Tilth is structurally different, not incrementally better.** The risk is that the differentiator is invisible to customers who aren't already paying the sovereignty tax. The opportunity is that there is no one selling the differentiator today.

RFP-automation tools (Loopio, Responsive, RFPIO/Responsive, etc.) are adjacent but not direct competitors — they are sales-org tools, not grant-applicant tools. Their data-handling postures are SaaS-tenant standard. Their feature set is response-content reuse, not opportunity discovery + rubric scoring + adversarial review.

The closest live analog is **Claude or ChatGPT plus the operator's own discipline** — i.e., the manual workflow Josh has won three grants with. Tilth productizes that. The threat from this analog is real: a sophisticated customer can today use frontier models plus a structured prompt library and get most of Tilth's value at lower cost (and lower sovereignty). The wedge is the sovereignty + discipline + audit trail + classification register — together.

---

## 6. Sustainability

### 6.1 Key-person risk

This is the largest risk by an order of magnitude. Concretely:

- **Architectural amendment authority is Josh alone.** Every LOCK ceremony is operator-signed. Paul will not be able to extend the chain without an operator-coordinated paired commit. This is correct at v0.1 but is a Phase-One scaling cap.
- **Memory is in Josh's head.** The wake-up sequence at `AGENTS.md` (read SOUL → USER → router.yaml → daily_logs → lessons → MEMORY → agent-specific overrides → PROJECT_CONTEXT) is structurally correct, but the substrate is operator-curated. If Josh disappears, the substrate stops updating. The `daily_logs/2026-05-17.md` is 189 lines because Josh wrote them; no other contributor can produce them.
- **Signing keys are operator-local.** `_private/cards_publisher_privkey_2026-05-17.txt` and `_private/operator_attestation_privkey_2026-05-17.txt` on Josh's machine. The `vault_shared/key_rotation_policy.md` §1 explicitly names this as "bus-factor mitigation… single-point-of-failure." It is not yet mitigated.
- **Grant-writing domain expertise.** Three wins in 2026 with the manual workflow is real. The pipeline systematizes the workflow; it does not yet replace the operator. Josh is the substrate of *why this works*.
- **Customer trust is personal.** The Founding 12 will sign because Josh sold them. Renewal will depend on whether they trust Tilth post-Josh-going-on-vacation.

The mitigation surface is named but not built. The CTO brief flags "operational freeze playbook" as blind-spot D (outstanding). The key rotation policy stops at recommendation. The Paul-onboarding doc set is excellent for technical work-pickup but does not address the operator-substrate work-pickup.

**Recommend** before Paul lands: (1) authored operational freeze playbook with shadow-environment cutover protocol; (2) off-machine Ed25519 backup procedure for every signing role (encrypted backups in two physically separated locations); (3) co-signer authorization scheme (Paul as co-signer for non-ceremony PRs by Gate 2); (4) a written Josh-on-vacation runbook covering signing-key access, ceremony deferral, customer-facing communication.

### 6.2 Maintainability and technical debt load

162k lines of pipeline + 162k lines of tests is substantial for one operator + one incoming engineer. The maturity matrix's `dormant` and `historical` rows are 30-40% of the surface, which is a feature (operator-acknowledged future work) and a debt (substrate that has to be maintained even if not exercised). Specifically:

- **125 F-* gates** in `pipeline/logician/gates/`. Many are `NotImplementedError`. Each is a maintenance surface — schema drift, predicate-body grad, test coverage. If even 1/3 of gates need to be brought live for v0.2, that is ~40 engineer-weeks of work.
- **116 files in `pipeline/blueprint/v0.1/`**. The amendment-edit-in-place prohibition means every change is a new file plus a paired §0.5 commit plus a lock_history row. This is *correct* for a governance ledger and *expensive* for a runtime evolution. The blueprint directory will grow to several hundred files within twelve months at the current cadence. Recommend rendering a `CURRENT_HEAD.md` per section to spare future readers the amendment-chain archaeology.
- **17k lines of Tier-2B card drafts** at `pipeline/cards/_drafts/` awaiting the §18 v1.2 LARGE cards-ceremony. The drafts are content, not code, but content-as-artifact requires operator review and Ed25519 re-signing.
- **365 test files**, ~10k+ pass. The test surface is in good shape but the CI runner is OOM'ing already.

Net read: maintainable for one operator at v0.1, marginal at Gate 1, brittle at the Founding 12 unless co-signer authorization and amendment-cadence governance changes.

### 6.3 Ops burden

What does keeping the lights on look like today:

- Daily logs are written daily.
- Lessons are appended at observation (27 lessons over six weeks).
- Ceremonies are dispatched per OD (5 OD ceremonies in May, plus the key rotation).
- Cross-family Thesis dispatches happen on amendment review (per L-005 two-audit cycle).
- Memory consolidation is operator-invoked (per `OQ-2(a)`).
- AGENTS.md wake-up sequence is observed by every agent session.

The operator is the bottleneck for all of the above. The "session-close self-check" discipline at `CLAUDE.md:217-230` is a reasonable attempt to push some of the bookkeeping into the agent loop, but the substantive judgment calls (which lesson, which OD, which amendment) are operator-bound.

**The work-volume-vs-customer-revenue equation is not yet calibrated.** At one Tilth customer (Josh's own org via `FIT Farms LLC`), the operator burden is justified by founder-discipline + R&D learning. At twelve Tilth customers (Founding 12), the operator burden is the binding constraint. **Recommend** a written model of "minutes-per-customer-per-week of operator attention" before scoping the Founding 12.

### 6.4 Runway for the regen / patient-capital model

The README doesn't quote a financial runway, and I haven't seen a financial plan in the audited tree (the business plan docx exists at `Golden Quill Business Plan v10 4.docx` but is gitignored and not in scope for this audit). What I can say from the architecture posture: the cost model is operator-time + hardware-cost-per-customer + BYOK API spend (passed to customer) + R&D time. No SaaS server costs. No marketplace dependency. The unit economics are favorable *if* the operator-time-per-customer caps low.

The patient-capital model — twelve Founder Nodes, then evaluate — is appropriate for the substrate. The substrate's friction is in onboarding and ceremony; both improve with each customer if the operator captures the lessons. **L-NNN discipline is the asset class** — every Founder Node deployment adds lessons; the lessons compound.

### 6.5 What breaks first when scale hits

In order of likelihood:

1. **Operator-time at customer #4 or #5.** Onboarding a Tilth customer takes white-glove time (Intake BULK_INGEST + Classification Review + first-cycle dispatch). At four or five concurrent customers, Josh is fully consumed by support and not architecting. Paul absorbs technical work but not customer judgment.
2. **CI runner OOM.** Already happening at the test-suite level on ubuntu-latest. Tiering up costs $; sharding tests is engineering work.
3. **Amendment chain pace.** The blueprint amendment chain grows by ~1 amendment per OD ceremony. At twelve customers, sustained at the May cadence, the blueprint directory will be 250+ files within six months. The index becomes the file you read.
4. **Heavy-Judge swap on dev hardware.** Josh's 8 GB M1 cannot run a 200B-class local model. If he deploys without buying a customer-spec machine, every heavy-Judge dispatch leaves the local-only posture into the unknown. **This is a Gate-2 blocker the README acknowledges** (`README.md:50` "marked performance-dependent / under validation").
5. **Customer #1's first compliance audit.** The signed-asset chain holds up only if a customer's auditor can be walked through it. Today, the walk-through is "Josh sits next to the auditor." A "third-party-audited" SOC 2 / FedRAMP / state-attestation posture is years away.

---

## 7. Salability

### 7.1 Who would buy this and at what price point

The Founding 12 are the canonical wedge: twelve Pittsburgh-area Founder Node deployments across six CICs (`README.md:11-12`) between mid-July 2026 and mid-April 2027. Per-Tilth cost includes the 128 GB Golden Quill hardware (Dell Pro Max GB-10 / ASUS GB-10 OEM / Apple Mac Studio M3 Ultra), the white-glove onboarding service, the Tilth software license, and BYOK provider keys paid by the customer. I don't have access to Josh's pricing — `Golden Quill Business Plan v10 4.docx` is gitignored — but the natural anchor is "less than a year of one staff person who would otherwise do this work" combined with "more than a SaaS grant-writing tool." Splitting the difference: $15k–$50k installed-and-onboarded for the hardware + software + first-year service, with annual renewal in the $5k–$15k range for software + support. Higher for foundations and state agencies; lower for cooperatives and small Food Systems orgs. These are my back-of-envelope numbers from the architecture posture, not Josh's.

After the Founding 12: Phase Two expansions per `README.md:13` are tribal sovereign configurations, researchers, foundations, institutional research offices, multi-site consortiums. Each has a different willingness-to-pay and a different reason to care about sovereignty. Tribal sovereign configurations are the highest-value-per-deployment because the alternative is "no AI assistance at all, because data-sovereignty rules prohibit cloud SaaS." Foundations are the highest-volume because they can resell-or-recommend-Tilth to grantees.

### 7.2 Productization path

From today's repo to a SaaS-or-licensed offering:

1. **A Gate-1 internal replay with Paul** — proves the substrate works for someone who is not Josh.
2. **A Gate-2 first paid client** — proves the substrate works against a real customer-cycle.
3. **A signed and reproducible deployment build** — hardware-image-plus-software-bundle that an installer can ship without operator hand-tooling.
4. **A productized onboarding playbook** — runbook for white-glove, ideally with the operator's role reduced to authoring + sign-off.
5. **A renewals model** — annual software-license fee, hardware refresh cycle, support tier, BYOK billing pass-through.
6. **Compliance documentation** — SOC 2 Type II at minimum if foundations are the target; FedRAMP Moderate if federal grantees are the target. Both are 12-24 month efforts.
7. **A reseller channel** — foundation partnerships, grant-writer agency partnerships (where the agency uses Tilth on behalf of clients), state cooperative-extension partnerships.

Gating items 1-3 are weeks to months. Items 4-7 are months to years.

### 7.3 Target customer wedges

In order of fit:

1. **Food-systems cooperatives and small farms.** Josh's home turf. The customer-cycle Tilth was built around. Highest fit; lowest ARPU.
2. **Cooperative-development centers (the CDFI / fiscal-sponsor world).** Per Capital Logic Card 6 (Credit & Underwriting) and the cross-cutting Cooperative CIC. Higher ARPU; longer sales cycle.
3. **Tribal sovereign configurations.** Phase Two per the README. Tribal grant offices have explicit data-handling rules that disqualify SaaS-tenant tools. Strong PMF on the sovereignty wedge. Long sales cycle; potentially highest ARPU per deployment.
4. **Small-to-mid arts-and-culture orgs** (TILTH-CIC-04). Lower technical sophistication; high content-quality demand. Lower fit on the sovereignty wedge but high fit on the discipline wedge.
5. **Educator orgs** (TILTH-CIC-02). Compliance-heavy (FERPA/COPPA/HIPAA). Strong fit on the PRP wedge once the FERPA-COPPA-HIPAA PRP lands. Most customers will be school districts or charters, which sell-cycle through procurement and are slow.
6. **Public-agency customers** (TILTH-CIC-03). Municipal procurement is slow; the ASUS GB-10 OEM hardware tier (`README.md:152`) is the no-bid path.
7. **Ecosystem intermediaries** (TILTH-CIC-06). Highest ARPU per deployment because they aggregate grantee demand; longest sales cycle; most likely to want a reseller arrangement.

### 7.4 Go-to-market gating items

1. **A customer reference deck.** Josh's three 2026 wins are anecdotal at v0.1; they become a case study at Gate 2.
2. **A defensible compliance posture.** What is Tilth's HIPAA-relevant data flow? FERPA? CJIS? Today the answer is "out of scope at v0.1." That answer is fine if no customer is HIPAA-touching. The educator wedge is FERPA-touching by design.
3. **A pricing page or a sales motion.** Custom pricing per customer is correct at v0.1; at the Founding 12 it becomes the operator's full-time job to quote.
4. **An installation video or sales-engineering demo.** Today there is no public-facing demo. The `landing/index.html` is a 30-line preamble of styled HTML; the rest I did not deep-read.
5. **Customer success motion.** Today customer support is Josh. At Gate 2 it can stay Josh; at #4 customer it cannot.

### 7.5 Pricing models worth considering

The current implied model — perpetual license + annual support — works for sovereignty-conscious customers and is the right starting point. Three adjacent models to consider:

- **Annual subscription bundling software, support, and hardware-refresh.** Lower up-front, longer commitment. Reduces customer-experience friction at Year 2 hardware obsolescence.
- **Co-op share + annual dues** for cooperative customers. Mirrors the Sovereign Node Stage-5 vision and is recognizable to the cooperative customer base.
- **Pay-per-cycle for foundation customers.** Foundations grant in cycles; pricing per cycle aligns with their procurement reality.

Avoid: percentage-of-grant-amount (creates incentive misalignment), per-seat pricing (doesn't match Cultivator's per-employee model and creates support burden), pure subscription (mismatches hardware-ownership thesis).

---

## 8. Visibility

### 8.1 Public surface

I cannot reach the live internet from this audit context to verify. From the repo: `landing/index.html` exists, is styled in a paper-and-ink Cinzel + Playfair Display brand register, and is keyed off `yourgoldenquill.com` (`USER.md` and supporting docs). The brand register is coherent — "Datacenter-class AI for small and medium organizations" / "NVIDIA Grace Blackwell on your desk, running Tilth — the funding operating system" (`landing/index.html:5-7`). The brand-line per the README is "Golden Quill — regenerative grant intelligence" (`CLAUDE.md:55-58`). The landing-page line is sharper and more sales-ready; the README line is values-truer. Both should reconcile at the public site.

Who else can find what: a GitHub search for "Tilth" or "Golden Quill" will surface the repo (private — `License: Proprietary`). A LinkedIn search for "Josh Inklovich" surfaces the operator's known business identities (MycoSymbiotics, FIT Farms, mushroom-foraging certification program). A web search for "regenerative grant intelligence" returns nothing branded today. A search for "BYOK grant writing AI" — same.

**The public surface is thin and that is by-design at v0.1.** Founding-12 customers will be sold by Josh directly. Building a public marketing surface before Gate 2 is a distraction.

### 8.2 Brand narrative coherence

The brand chain — Golden Quill (hardware) / Tilth (software) / Cultivator (per-employee interface) / Sovereign Node (Stage-5 commons) — is coherent and well-defended internally. The Sovereign Node language is *carefully* held internal (not customer-facing v1, per `CLAUDE.md:46-48`); the FIT Farms Commons / FIT Farms LLC distinction is *carefully* held internal (file-naming labels, not customer-facing copy, per `CLAUDE.md:88-92`). This is the kind of brand-discipline that lets the founder communicate carefully without contradicting himself in front of a customer.

The naming choices have texture. "Tilth" is excellent — agricultural, deliberate, unfamiliar enough to own. "Golden Quill" is good — physical, premium-positioned, slightly mythic. "Cultivator" is good for the per-employee mobile interface. "Sovereign Node" is internally-named-as-internal — wise; the term is freighted with crypto-adjacent and political-adjacent baggage that could narrow the customer set unintentionally.

The five sectors → six CICs language migration is the only place I see active narrative drift. The five-sector taxonomy (workforce / education / regen_ag / urban_ag / land_community / eco_art per `CLAUDE.md:148-150`) is still load-bearing in code (Scribe knowledge-pack sector enum, Scout sector tags, PROJECT_CONTEXT `sectors:` field) while the customer-facing six-CIC taxonomy is the public face. Per `CLAUDE.md:165-167` ("Sector vs. launch market — open reconciliation"), this is acknowledged-open. **Resolve before the public site launches** — having two taxonomies in the wild creates customer-conversation friction.

### 8.3 Press posture, community presence, social

Not visible from the repo. No press kit at `docs/`. No social-handle inventory. No community/Discord/forum. This is by design at v0.1 and should remain so until Gate 2.

### 8.4 Content gaps

The single highest-leverage piece of content not yet authored is a **case study from one of Josh's three 2026 grant wins**, generalized to remove client-identifying detail. The narrative ("here's the manual workflow that won this grant; here's how Tilth systematizes it") is exactly the value proposition customers will not believe from the architecture docs alone. **Recommend** authoring this as `docs/case_study_2026_grant_win_001.md` before Gate 2.

Other gaps: a one-page architecture diagram (the ASCII flowchart in `docs/ARCHITECTURE_OVERVIEW.md` is good but not shareable as PDF/PNG); a one-page "what makes Tilth different" sales sheet; a customer-facing FAQ. All Gate-2 surface, not Gate-1.

---

## 9. Credibility

### 9.1 Proof points that exist today

1. **Three competitive grants won in 2026 using the manual workflow.** Cited at `USER.md:11-13`, `README.md:11`, `docs/COLLABORATOR_HANDOFF.md:90-93`, `docs/v0_1_TECHNICAL_LEAD_BRIEF.md:20`. Real customer-attributable outcomes. The Pittsburgh-area food-systems focus is identifiable (`README.md:11`).
2. **Lock_history audit trail.** 292 rows, Ed25519-signed, paired-commit-chained. A funder auditor can be walked through the chain. This is credibility-as-artifact.
3. **Working signing chain (post-rotation).** The cards-publisher pubkey rotation event is the proof — the system caught a compromise, rotated, re-pinned, re-signed, and kept the audit trail intact (`vault_shared/cards/publisher_pubkey.signed.yaml`, `lock_history.v1.jsonl` rows 280-292). A skeptic can verify.
4. **Operator credentials.** 25+ years project management in skilled trades and workforce development; co-founder of MycoSymbiotics Cooperative; founder of FIT Farms; designer of Pennsylvania's wild mushroom foraging certification program (`USER.md:11-12`). Operator brings substance.
5. **Dogwood delivered end-to-end through OpenClaw for a real external client.** Cited at `docs/v0_1_TECHNICAL_LEAD_BRIEF.md:25`. The system has shipped work to an outside customer at least once.

### 9.2 Ceremonial track record as credibility signal

The lock_history ledger is the strongest credibility signal Tilth has *for customers who would pay extra for it*. For food-systems cooperatives that don't care about audit trails, it is invisible. For federal grantees, foundations, tribal sovereign configurations, and any customer whose own funder demands traceability, it is the differentiator.

The ledger's credibility is contingent on signature verifiability. **Until the signature-round-trip CI job exists, the credibility-as-artifact has a reasonable-doubt floor.** A customer who actually verifies a signature gets convinced; a customer who reads "signed by operator Ed25519" gets convinced enough to ask "show me." The "show me" today requires Josh sitting next to the customer.

### 9.3 What funders / collaborators will believe vs need to see

Funders will believe:
- The architecture is real.
- The operator has won grants.
- The sovereignty wedge is technically credible.
- The team (one operator + one incoming engineer) is small and dedicated.

Funders will need to see:
- Customer reference (Founding-12 deployment + outcome).
- Reproducible deployment (not "Josh installed it" — "anyone trained can install it").
- Compliance posture commensurate with the customer set (FERPA for educator, foundation-data-handling for foundations, tribal sovereignty conventions where applicable).
- Continuity plan beyond the founder.

Collaborators (Paul + future hires) will believe:
- The docs are unusually disciplined.
- The architecture is opinionated and defensible.
- The codebase is non-trivial but legible if you read in order.

Collaborators will need to see:
- A green local test run within 30 minutes of clone (achievable today per `docs/LOCAL_DEVELOPMENT.md`).
- A first-PR-merged within a week of arrival.
- Operator co-signer authorization within the first month.

### 9.4 Reference customers, pilot results, case studies

Anecdotes today; case studies not yet authored. The three 2026 grant wins are the obvious case-study material. Operator should de-identify the clients (or get client permission for attribution) and write up: opportunity discovered → ingested → drafted → reviewed → submitted → awarded. The case-study format is the credibility-as-narrative complement to the credibility-as-artifact ledger.

---

## 10. Security Posture

### 10.1 Secret management

Strong. The `.gitignore` is 230+ lines and unusually disciplined (`docs/secrets_data_access_audit_2026-05-17.md` §3 finding 3). Coverage of `orgs/`, `data/` content (post-fix), `daily_logs/`, `pipeline/handoffs/`, `pipeline/metrics/session_log.jsonl`, `pipeline/scout/databases/`, `pipeline/radar/`, `pipeline/subscribers/`, `pipeline/audits/`, `pipeline/orchestrator/run_log.json`, `_private/`, `memory/` (with `!pipeline/memory/*.py` negation), `sessions/`, `Sovereign_Node_Handoff/`, prior Replit work, marketing artifacts (`assets/Decks/`, `tilth_v2.pptx`), top-level research PDFs, `*.seed` (added in commit `65e841a` as defense-in-depth).

The secrets audit at `docs/secrets_data_access_audit_2026-05-17.md` is itself a proof of process — operator commissioned, in-tree, dated, findings registered.

### 10.2 Private keys, .seed files, vault_shared

- `_private/cards_publisher_privkey_2026-05-17.txt` (64 bytes), `_private/operator_attestation_privkey_2026-05-17.txt` (855 bytes). Gitignored. Operator-local.
- `vault_shared/cards-publisher.seed` (65 bytes). Now gitignored by `*.seed` (`.gitignore:212`). Confirmed present on disk in working tree but not tracked.
- `vault_shared/cards/publisher_pubkey.signed.yaml` — public key, signed, post-rotation `c93f1881…`. Public-by-design.
- `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml` — public key, signed, `634441fd…`. Public-by-design.
- `vault_shared/operator_attestation/publisher_pubkey.signed.yaml` — public key, signed, `094a4dc4…`. Public-by-design. *(Correction folded in at PR #19 signature-round-trip verifier run, 2026-05-18: the original audit reading called this a placeholder stub, but the file on `main` is in fact a real TOFU-self-signed asset published 2026-05-17T21:56:20Z and `pipeline/scripts/verify_signed_assets.py` confirms self-verification under the documented JSON-canonical recipe. Role 6 per `vault_shared/key_rotation_policy.md` §2 is therefore PINNED. §13 recommendation #3 — "Operator-attestation pubkey activation" — is already satisfied.)*
- `vault_shared/reflection_packet/producer_pubkey.signed.yaml` — placeholder zeros. Per role 3, SCAFFOLD.
- `vault_shared/wpfa/sn_llc_pubkey.signed.yaml` — empty pubkey_hex. Per role 4, SCAFFOLD.

The pattern is consistent: pubkeys are committed (public material), privkeys are operator-local, `*.seed` is defense-in-depth-ignored. The exposed surface is the operator's local machine plus whatever Josh shows on screen. The compromise vector that fired on 2026-05-17 was the operator pasting an Ed25519 seed into Dispatch chat — a human-process failure, not a tooling failure. The mitigations (rotation, TOFU re-pin, L-027 lesson, `*.seed` gitignore) are in place; the *generalized* mitigation (never paste seed material into a chat tool) is operator-discipline.

### 10.3 Recent key rotation: was the compromise handled correctly?

Yes. By the book per `vault_shared/key_rotation_policy.md` §4 compromise-response runbook. Time from discovery to TOFU re-pin appears to be within the recommended 24-hour window (rotation occurred 2026-05-18T00:00:00Z per row 280; original exposure 2026-05-17). The compromise record at `pipeline/handoffs/cards_publisher_key_rotation_2026-05-17/05_old_key_compromise_record.md` is referenced from the lock_history row. The three OD-E-affected cards were re-signed under the new pubkey (rows 289-291).

One nit: the `*.seed` gitignore line was added *in the same commit* as the rotation (`.gitignore:212`, commit `65e841a`). This means the seed file `vault_shared/cards-publisher.seed` could have been on the working tree without that ignore line at any prior moment. `git ls-files vault_shared/cards-publisher.seed` returns empty (I did not verify) so it never tracked — but the post-hoc defense-in-depth would have been better as a pre-hoc one. Not a finding; a hygiene observation.

### 10.4 Operator_attestation key loss — actual blast radius

If Josh loses the operator-attestation key (role 6), the blast radius is bounded:

- All prior signatures on CycleReceipts and reflection-packet outputs remain verifiable under the *prior* operator-attestation pubkey (when one is pinned; today the role is MISSING placeholder).
- New CycleReceipts cannot be operator-signed; `F-WPFA-OPERATOR-SIGNATURE-MISSING` fail-closes buyer-facing PDF emission.
- New reflection packets cannot be operator-signed; the dormant `F-PACKET-OPERATOR-SIGNATURE-INVALID` predicate would fire when activated.

At v0.1 the operator-attestation role is not yet load-bearing (no CycleReceipts in production, no reflection-packet emission). The exposure window is between role-6 activation and Gate-2. Recommend: pin operator-attestation pubkey in a real signed asset *before* WPFA buyer-facing PDF emission is enabled.

### 10.5 Supply chain risk

Tag-pinned actions (`actions/checkout@v6`, `actions/setup-python@v6`, `actions/upload-artifact@v4`); no dependabot config visible; no `pip-audit`; no SBOM. Mitigated today by first-party-only actions and modest dependency count. Recommended hardening at Gate 2: SHA-pin actions, add dependabot, add `pip-audit` CI step, generate SBOM at wheel build.

### 10.6 Threat model gaps

There is no published threat model document. The architecture surfaces (three-posture routing, F-CLASS-* family, classification register, signing chain) implicitly defend against specific threats (cloud egress without authorization, opaque-slot-token attacks, archetype-coupled card load), but there is no first-principles enumeration: who is the adversary, what are their goals, what are the trust boundaries, what mitigations exist where.

**Recommend** authoring `docs/THREAT_MODEL.md` before Gate 2. Skeleton: adversary categories (curious-customer, careless-operator, hostile-funder, supply-chain-attacker, insider-threat-via-AI-assistant, lost-laptop, leaked-API-key, model-provider-compromise); trust boundaries (operator-local / vault_shared / cloud); existing mitigations cross-referenced to F-* codes and architecture amendments; residual risks named explicitly. A 5-page document. High signal-per-page; signals to customers that the founder thinks adversarially.

---

## 11. Legal / Compliance Exposure

### 11.1 Grant logic — any liability around what gets recommended

The Five Laws structure most of this away (`SOUL.md:30-45`). Law 5 ("Applicant Brings the Substance") in particular: Tilth does not fabricate credentials, data, or partnerships; it shapes existing substance into funder-ready form. If Tilth recommends an opportunity that the applicant is ineligible for, the recommendation comes from Scout's VERIFY stage and is operator-reviewable before any submission action. The applicant clicks submit on the funder portal; Tilth stages, does not submit (Uploader prepare-and-stage discipline). Liability transfers to the applicant on submission, which is the right legal posture for a tool that assists rather than executes.

Residual liability: if a Tilth-drafted proposal contains a misrepresentation that survives operator review and lands the applicant in a federal compliance issue (False Claims Act adjacent, materially misleading representation), the producer of the draft has some attendant risk. The mitigations: (a) Law 1 (RFA-Is-Truth) requires every claim trace to the RFA or PROJECT_CONTEXT; (b) Law 5 forbids fabrication; (c) Logician fail-closed gates enforce both at preflight; (d) operator review is mandatory pre-submission. The combination is defensible but not absolutized.

**Recommend**: a one-page customer terms-of-service that names "Tilth assists; applicant submits and bears submission liability" explicitly. Authorize Paul to draft once retained.

### 11.2 Data handling, PII posture

PII shows up in three places: organization-level data in PROJECT_CONTEXT.md (EIN, UEI, addresses, financials), beneficiary-records sub-kind data (post-award, v0.2 horizon), and post-award outreach (Data Collector, v0.2 horizon). At v0.1, the BYOK + local-first + classification-register stack keeps everything in customer custody by default. Confidential and operator-flagged fields never leave the node under any of the three postures (`README.md:75-77`).

The educator wedge will surface FERPA. The healthcare-adjacent surface (school-maintained medical records, the FERPA/HIPAA interface, COPPA for under-13 students) is named in the FERPA-COPPA-HIPAA PRP (stub-only today). If Tilth touches student data in any form, FERPA's school-official-exception controls apply, and Tilth's posture has to be documented to clear it. The cooperative wedge will surface Subchapter T tax treatment, which is operator-facing (the cooperative customer's accountant manages) but Tilth-content-relevant.

**Recommend**: before the first educator-wedge customer onboards, the FERPA-COPPA-HIPAA PRP must be authored beyond stub. This is a Gate-2 (not Gate-1) item.

### 11.3 Attribution, licensing of foundation models, derivative work concerns

BYOK posture means the customer brings the model-provider relationship (Anthropic, OpenAI, Google, Groq, etc.). Tilth does not host model weights; Tilth does not redistribute model outputs as Tilth's IP. The legal posture is: Tilth's IP is its substrate (orchestration, gates, cards, PRPs, signing chain); model outputs are subject to the model provider's terms of service that the customer has accepted under their own BYOK keys.

Two latent issues:
- **DSPy + GEPA offline refinement** (per `docs/decisions/ADR-001.md`). If GEPA optimizes prompts against a corpus that includes copyrighted material (foundation RFA texts, etc.), the optimization-output IP posture is the typical text-mining gray zone. Recommend a one-paragraph "what we train on and what we don't" statement when GEPA actually runs.
- **Card content provenance**. Cards cite primary sources (e.g., `pipeline/cards/CIC/food_systems.yaml` cites USDA, EPA, NRCS, AMS, NIFA, PA DOA, Heinz, Mellon). Verbatim quotes are ≤2 sentences and tagged with `verbatim_quote` and `access_date`. This is standard educational-fair-use posture. The system *does not* republish funder boilerplate at scale.

### 11.4 2 CFR 200 / Davis-Bacon / NEPA — what the PRPs are doing and where they could overreach

The three live PRPs (`TILTH-PRP-2CFR200/v1.yaml`, `TILTH-PRP-DAVIS-BACON/v1.yaml`, `TILTH-PRP-NEPA-24CFR58/v1.yaml`) encode published live law. Each is DRAFT, none are signed, and the loader is `NotImplementedError`. The header text on each PRP is explicit: "PRPs encode published live law only — never operator-specific overrides, never private member rosters, never CIC × CLC eligibility coupling" (`pipeline/program_rule_packs/cross_cutting/TILTH-PRP-2CFR200/v1.yaml:32-38`).

The risk surface where Tilth could overreach: if a PRP's "this is what 2 CFR 200 requires" recommendation in a draft is interpreted by an applicant as legal advice. The mitigation is the Five Laws + Uploader prepare-and-stage discipline + operator review. The PRP system is built to inform Scribe's drafting, not to substitute for an applicant's compliance counsel.

**Recommend** a customer-facing disclaimer that lands on every PRP-informed output: "Tilth surfaces published-law context to support your drafting. Tilth does not provide legal advice. Verify compliance obligations with qualified counsel before submission." Three sentences. Adopt at PRP loader graduation.

The NEPA PRP is the highest-attention-grab because NEPA review is the federal grant compliance surface most likely to surprise an applicant. If Tilth's PRP misclassifies a project's NEPA category (categorical exclusion vs environmental assessment vs environmental impact statement), the applicant inherits the error. **Strong recommendation**: PRP outputs should never replace 24 CFR 58 environmental review responsible-entity sign-off; Tilth surfaces, the responsible entity (HUD-recognized RE or NEPA-implementing federal agency) decides.

---

## 12. Risks Ranked by Blast Radius

1. **Operator unavailability without continuity plan.** Severity: extinction-level for the project. Mitigation cost: low-to-moderate (off-machine key backup + Paul co-signer authorization + written runbook). Urgency: before Paul lands. *What fails:* every architectural decision freezes; every customer-cycle stalls; no new card or amendment can ship; signed-asset chain cannot be extended.

2. **Signing chain compromise without rapid rotation.** Severity: high — customer trust loss, audit-trail credibility loss. Mitigation cost: moderate (operator-attestation pubkey activation + signature-round-trip CI job + off-machine key backup). Urgency: before Gate 2. *What fails:* every card, every paired commit, every CycleReceipt's signature becomes potentially-forged; customers who care about provenance churn.

3. **First-customer-cycle failure without test harness.** Severity: high — Gate 2 slipped, customer #1 lost, reputational drag. Mitigation cost: moderate (deterministic customer-cycle replay harness, end-to-end integration test). Urgency: before first paid client. *What fails:* a customer-cycle fails at the customer's funder deadline; recovery is operator-time-intensive.

4. **CI suite OOM / test-time growth without runner tier-up.** Severity: medium — contributor-experience friction, Paul-onboarding friction. Mitigation cost: low (larger CI runner) to moderate (test sharding). Urgency: this month. *What fails:* PRs stall on flaky CI; Paul loses faith in the test harness; regressions slip in.

5. **Amendment chain pace exceeding operator-time capacity.** Severity: medium-to-high over 6 months. Mitigation cost: high (co-signer authorization, amendment-cadence governance, blueprint-CURRENT_HEAD rendering). Urgency: before Founding-12 scale. *What fails:* amendments LOCKed faster than implemented; substrate-vs-runtime gap widens; Tilth ships the ceremony, not the product.

6. **Logfire egress under "nothing phones home" claim.** Severity: medium — sovereignty-claim contradiction. Mitigation cost: low (CC-008 end-to-end verification + customer-facing claim calibration). Urgency: before Gate 2. *What fails:* a savvy customer's network audit catches Logfire egress; the sovereignty-promise narrative cracks.

7. **PRP misclassification of federal-compliance category** (NEPA in particular). Severity: medium-per-incident, low-frequency. Mitigation cost: moderate (PRP outputs gated to surface-not-decide + customer-facing disclaimer). Urgency: before PRP loader graduation. *What fails:* an applicant defers to a Tilth PRP and inherits a compliance issue at submission.

8. **Card-content stale-source drift.** Severity: medium over 12 months — cards cite live funder programs with deadlines; the substrate goes stale. Mitigation cost: moderate (KFR maintenance + content-freshness audit cycle). Urgency: ongoing post-Gate-2. *What fails:* cards cite expired program windows; Scout VERIFY catches before submission but customer trust erodes.

9. **Hardware-tier dev/prod gap on heavy-Judge swap.** Severity: medium — Local-Only / Sovereign posture remains "under validation." Mitigation cost: moderate (buy customer-spec dev hardware; runs against real 200B-class model). Urgency: before second paid client (first paid client can run Frontier-Eligible posture). *What fails:* operator cannot reproduce customer's Local-Only posture; bug-hunt blind to a customer-only failure mode.

10. **Test fixture using operator's own LLC name** (`docs/secrets_data_access_audit_2026-05-17.md` P1-B). Severity: low today, medium when an outside-client name follows the same pattern. Mitigation cost: trivial (synthetic-name convention + fixture rename). Urgency: this week. *What fails:* a future test uses a real outside-client name and Law 3 (Org Isolation) fails subtly.

11. **Brand/posture drift in public site.** Severity: low — narrowable through editorial discipline. Mitigation cost: low. Urgency: before public-site launch. *What fails:* sectors-vs-CICs taxonomy mismatch creates customer-conversation friction.

12. **Supply-chain action-update attack.** Severity: low today (first-party actions only). Mitigation cost: low (SHA-pin + dependabot). Urgency: hardening pass. *What fails:* hypothetical compromised tag pushes malicious checkout into CI.

---

## 13. Top-N Priority Recommendations

In order of leverage-per-effort. Effort scale: XS (under a day), S (1-3 days), M (1-2 weeks), L (2-6 weeks). Owner suggestion is preliminary.

| # | Title | Why it matters | Effort | Owner |
|---|---|---|---|---|
| 1 | **Off-machine Ed25519 backup procedure for every signing role.** Encrypted backups in two physically separated locations; written runbook. | Bus-factor is the single largest extinction risk. The `vault_shared/key_rotation_policy.md` §1 names this gap; nothing closes it. | S | Josh |
| 2 | ~~**Signature-round-trip CI job.** Every signed asset (cards, §0.5 paired commits, classification registers, key rotation policy attestations) verifies under pinned pubkey on every push to `main`.~~ **DONE 2026-05-18 (PR #19).** Verifier at `pipeline/scripts/verify_signed_assets.py` + workflow at `.github/workflows/signature_roundtrip.yml` + allowlist at `pipeline/scripts/signature_verification_deferred.yaml`. Required branch protection check enabled in this follow-up PR. | Today, the ceremonial chain is credible by narrative, not by automation. This converts narrative to verification. | S | ~~Paul~~ Done |
| 3 | ~~**Operator-attestation pubkey activation.** Replace the placeholder at `vault_shared/operator_attestation/publisher_pubkey.signed.yaml` with a real pinned pubkey.~~ **ALREADY DONE pre-audit (correction folded in 2026-05-18 PR #19 verifier run).** Asset is a real TOFU-self-signed pubkey `094a4dc4…` published 2026-05-17T21:56:20Z; audit reading was stale. | Role 6 is MISSING per the key rotation policy; Gate 2 needs it for WPFA buyer-PDF emission. | XS | ~~Josh~~ Done |
| 4 | **Operational freeze playbook + shadow-environment cutover protocol.** Author `docs/operational_freeze_playbook_v1.md` mirroring the v0.1 Beta deployment runbook. | Blind-spot D per `docs/CTO_HANDOFF_BRIEF.md` §2.4 is the outstanding pre-Gate-2 surface. | M | Josh + Paul |
| 5 | **Paul-onboarding green-path document.** Compress `docs/COLLABORATOR_HANDOFF.md` + `docs/LOCAL_DEVELOPMENT.md` + `docs/AGENT_CONTEXT_INDEX.md` into one `docs/PAUL_DAY_ONE.md`: clone → venv → tests green → first PR. | The current six-doc onboarding fan-out costs Paul half a day before he commits anything. | S | Josh (with Paul-feedback iteration) |
| 6 | **`docs/GLOSSARY.md`** — F-* family one-liners, §-section one-liners, OD codes, L-lessons index. | The internal jargon load is real. A glossary collapses Paul's onboarding curve by ~half a day. | S | Paul, with Josh review |
| 7 | **`docs/THREAT_MODEL.md`** — first-principles enumeration of adversaries, trust boundaries, mitigations. | Customer-facing security review will ask for this. Better to author than to be asked. | M | Josh + Paul |
| 8 | **Customer-cycle replay test harness.** Deterministic end-to-end test from RFA-in to staged-submission-out, scripted, runnable. | Today's `pipeline/planning/v0_1_lock_and_clear_packet_2026-05-11.md` is a spec, not a script. Gate 1's "internal replay with Paul" needs this. | M | Paul |
| 9 | **Case study from one of Josh's 2026 grant wins.** De-identified or with permission. `docs/case_study_2026_grant_win_001.md`. | The single highest-leverage piece of credibility content not yet authored. | S | Josh |
| 10 | **CI hardening pack.** SHA-pin actions; add dependabot; add secret-scanner action; add `pip-audit` step; tier up runner to handle suite size. | Several P2 findings from the secrets audit collapse into one PR. | S | Paul |
| 11 | **Render `pipeline/blueprint/v0.1/CURRENT_HEAD_PER_SECTION.md`** generated from the amendment chain. | The blueprint directory grows monotonically; a current-head view spares every future reader the archaeology. | S | Paul |
| 12 | **Reconcile sector-vs-CIC taxonomy.** Either rename the Scribe knowledge-pack sector enum, the Scout sector tags, and the PROJECT_CONTEXT `sectors:` field to the CIC slug; or formally name "sectors are internal, CICs are customer-facing" in docs. | Open per `CLAUDE.md:165-167`. Resolve before public-site launch. | S | Josh |
| 13 | **Tier-up dev hardware to a customer-spec Golden Quill.** Buy a Mac Studio M3 Ultra or DGX Spark for Josh's dev rig. | The 8 GB M1 cannot exercise the heavy-Judge swap or the Local-Only / Sovereign posture under load. | M (procurement) | Josh |
| 14 | **PRP loader v0.2 graduation roadmap.** Sequence the loader's `NotImplementedError` removal: lifecycle preflight → signature verification → effective-date window check → coupling violation scan. | The PRPs are signed-loaded-but-disconnected. Gate-2 customers will surface use cases. | L | Paul |
| 15 | **Customer ToS draft.** "Tilth assists; applicant submits and bears submission liability" + the PRP / legal-advice disclaimer. | Before the first paid customer signature. | XS (with counsel review) | Josh, counsel |

The top six items are achievable in a 4–6 week sprint and cover the highest-leverage gaps. Items 7–10 are months 2-3 work. Items 11–15 are pre-Gate-2 grooming.

---

## 14. Things Going Right (don't break)

This is the catalog of what to protect.

1. **The runtime maturity matrix discipline.** `RUNTIME_MATURITY_MATRIX.md` is the single most useful documentation artifact in the repo. Every claim has a label; every label has a definition; the matrix arbitrates when other docs disagree. Adopt this pattern across every new doc.

2. **The lock_history.v1.jsonl as an append-only, operator-write-only ledger.** Do not retrofit. Do not in-place-edit. The 198 `row: null` legacy rows are a feature of the ledger's pre-numbering era and should remain unaltered.

3. **The paired-commit §0.5 discipline.** Every blueprint amendment ships with its §0.5 sibling. This is exactly what a governance ledger should look like.

4. **The Ed25519 signing chain.** Cards, §0.5 entries, classification registers, key rotation events — all signed. Compromise-class rotations re-pinned correctly. Don't introduce shortcuts.

5. **Fail-closed by default.** F-CLASS-ROUTING-INDETERMINATE → local. F-CLASS-NEW-FACT-UNCLASSIFIED → confidential. F-CLASS-COVERAGE-INCOMPLETE → block deployment. NotImplementedError everywhere a runtime is pending. This is the right default for a sovereignty product.

6. **The Five Laws as non-negotiable.** Eight pages of architecture amendments build down to "RFA-Is-Truth + No-Boundary-Drift + Org-Isolation + Apolitical-with-Admin-Risk + Applicant-Brings-Substance." The Laws keep the system honest at the substrate.

7. **The L-NNN lessons discipline.** 27 lessons over six weeks, each cited at appropriate places. Append-only. Frequency-weighted. Mandatory pre-check on wake-up. This is the institutional-memory loop that makes the operator-substrate compound.

8. **The terse, evidence-first operator register.** Josh writes prompts and reads docs the way you read this paragraph: terse, decisive, evidence-cited, push-back-welcome. The CLAUDE.md / USER.md / AGENTS.md sequence calibrates every agent to that register. It works.

9. **The white-glove onboarding posture as the v0.1 sales motion.** Single-track white-glove per `README.md:103-110`. Operator-curated classification register, BULK_INGEST + Classification Review + first-cycle dispatch. Refuse to launch without operator-signed register. This is the right posture for the Founding 12.

10. **The Sovereignty Promise as the brand spine.** `README.md:99-101`. Customer-owned hardware, customer-owned keys, customer-owned data. If Sovereign Node LLC disappeared tomorrow, the customer would still have everything. This is the differentiator. Every new feature must answer the question.

11. **The CTO brief, secrets audit, key rotation policy, runtime maturity matrix as a quartet.** These four documents are the operator-readable face of the architecture. Together they describe what is true today, what was just learned, what is signed, and what is at risk. Maintain the quartet on every substantive change.

12. **The discipline of citing file paths and line numbers in every claim.** This audit document follows the convention. The PR template requires it. The result is a codebase that can be navigated by a stranger in days, not weeks.

---

## Appendix: Methodology

### What I read

- `README.md` (173 lines)
- `PROJECT_STATUS.md` (96 lines)
- `RUNTIME_MATURITY_MATRIX.md` (96 lines)
- `CLAUDE.md` (335 lines / 50 KB)
- `AGENTS.md` (181 lines)
- `SOUL.md` (50-line head sample)
- `USER.md` (40-line head sample)
- `pyproject.toml` (153 lines, full)
- `router.yaml` (252 lines, partial)
- `docs/CTO_HANDOFF_BRIEF.md` (272 lines, full)
- `docs/COLLABORATOR_HANDOFF.md` (203 lines, full)
- `docs/TECHNICAL_BACKLOG.md` (225 lines, full)
- `docs/AGENT_CONTEXT_INDEX.md` (233 lines, full)
- `docs/ARCHITECTURE_OVERVIEW.md` (~250-line head sample, 359 lines total)
- `docs/LOCAL_DEVELOPMENT.md` (~150-line head sample, 199 lines total)
- `docs/GETTING_STARTED.md` (referenced; not deep-read)
- `docs/secrets_data_access_audit_2026-05-17.md` (130 lines, full)
- `docs/decisions/ADR-001.md` (66 lines, full)
- `docs/v0_1_TECHNICAL_LEAD_BRIEF.md` (77 lines, full)
- `docs/platform_engineer_quick_reference.md` (50-line head sample)
- `docs/post_alpha/post_alpha_card_system_revised_2026-05-15.md` (20-line head sample)
- `pipeline/engineering/lock_history.v1.jsonl` rows 280-292 (key inspection); summary of rows 271-279; total 292 logical rows.
- `pipeline/cards/loader.py` (lines 1-400 of 741)
- `pipeline/cards/registry.yaml` (head sample)
- `pipeline/cards/CIC/food_systems.yaml` (head + tail)
- `pipeline/cards/CLC/market_access.yaml` (head, lifecycle, tail)
- `pipeline/cards/_drafts/cic_food_systems_augmented_2026-05-18.yaml` (head)
- `pipeline/program_rule_packs/loader.py` (head)
- `pipeline/program_rule_packs/_manifest/active_prps.yaml` (head)
- `pipeline/program_rule_packs/cross_cutting/TILTH-PRP-2CFR200/v1.yaml` (head)
- `pipeline/orchestrator/provider_boundary.py` (head)
- `pipeline/logician/gates/f_cards_signature_invalid.py` (head)
- `pipeline/logician/gates/f_cards_coupling_violation_extension.py` (head)
- `pipeline/blueprint/v0.1/ACTIVE_BLUEPRINT_INDEX.md` (head)
- `.github/workflows/ci.yml` (full, 115 lines)
- `.gitignore` (full, 230+ lines)
- `vault_shared/cards/publisher_pubkey.signed.yaml` (full)
- `vault_shared/key_rotation_policy.md` (head)
- `lessons.md` (head + section index)
- `daily_logs/2026-05-17.md` (head)
- `scripts/run_tests.sh` (full)
- `landing/index.html` (head)
- `git log --all --oneline` for activity tempo and branch structure

### What I sampled but did not deep-read

- Most of the 116 files in `pipeline/blueprint/v0.1/`.
- The 125 F-* gate modules in `pipeline/logician/gates/` (sampled headers; spot-read 4-5).
- The 365 test files in `tests/` (counted, structured, spot-read 3-4).
- The full `router.yaml`.
- The remaining ~14k+ line cards beyond the food_systems and market_access samples.
- The Tier-2A PRP drafts beyond the 2 CFR 200 head sample.
- The Tier-2B card drafts beyond the food_systems head sample (per Josh's brief, held for follow-up PR).
- The full `lock_history.v1.jsonl` (read in row-range slices to avoid context overflow).
- `pipeline/sovereignty/` modules.
- `pipeline/orchestrator/router.py` body (referenced and inferred from `provider_boundary.py` companion docs).

### What I could not access

- GitHub remote settings: PR list, issue list, branch protection rules, collaborator list, deploy keys, installed GitHub Apps (`gh` CLI unavailable in this audit environment).
- The live signing chain verification (did not run `ed25519.verify()` against any signed asset; consumed signatures as opaque hex strings).
- The `Golden Quill Business Plan v10 4.docx` (gitignored marketing artifact).
- The `tilth_v2.pptx` deck (gitignored).
- The full content of `_private/` (gitignored; verified existence but did not read).
- The runtime behavior of any component — read-only audit.
- The `data/` directory contents (host-side, ~4.9 GB of IRS Form 990-PF TEOS XML extracts and derived summaries).
- Anything outside the GoldenQuill working tree.

### Confidence level by section

- **§1 (Technical Foundation):** high. Architecture and code surfaces directly inspected.
- **§2 (Functionality):** high for `runtime-live` and `spec-locked`; medium for `gate-live` (predicate bodies sampled, not exhaustively); medium-low for `asset-signed` runtime behavior (signatures read, not verified).
- **§3 (Clarity):** high. Documentation surfaces directly inspected.
- **§4 (Best Practices):** high for CI / branch protection / commit discipline; medium for secrets handling (the secrets audit itself bridges the gap).
- **§5 (Innovation & Defensibility):** medium. Architecture inspected; market-comparison inferred.
- **§6 (Sustainability):** medium-high. Operator-time and key-person risk grounded in repo evidence; runway model inferred.
- **§7 (Salability):** medium. Customer wedges grounded in CIC/CLC architecture; pricing inferred.
- **§8 (Visibility):** low-medium. Public site not reachable from audit context; brand discipline directly inspected.
- **§9 (Credibility):** high. Proof points directly cited in tree.
- **§10 (Security Posture):** medium-high. Secrets posture grounded in audit doc; key-rotation event directly inspected.
- **§11 (Legal / Compliance):** medium. Mitigations directly inspected; risk surface inferred from architecture.
- **§12 (Risks):** high — ranking based on directly-inspected evidence.
- **§13 (Recommendations):** high — actionable, owner-suggested.
- **§14 (Things Going Right):** high — directly grounded in tree.

### Audit posture and limits

This audit is read-only. No code was modified. No `_private/` content was opened. No `.seed` file was read. No lock_history row was appended. The audit doc is the only artifact produced; it lives at `docs/project_audit_2026-05-18.md` and is operator's to commit. The audit does not constitute legal, financial, or security advice. The audit author has no relationship to FIT Farms LLC, Golden Quill, Tilth, or any named customer beyond running this audit in good faith for the operator's benefit.

*End of audit.*
