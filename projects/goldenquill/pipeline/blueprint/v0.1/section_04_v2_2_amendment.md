---
title: Blueprint §4 Logician — Amendment v2.2 Wave 1 (POST-gate predicates F-AMDT-02 + F-AMDT-03)
filed: 2026-04-20
operator: Josh
amendment_status: LOCKED 2026-04-20 (Code Thesis Committee 5/5 PASS cycle-1, zero findings)
parent_lock: pipeline/blueprint/v0.1/section_04_logician.md  (§4 v2.1 LOCKED 2026-04-18, hash e0507e6daaa18676)
supersedes_relationship: non-disruptive extension. Adds two POST-gate predicates to §4.6 POST-gate family. Leaves §4.1-§4.13 semantics unchanged. §4.14a (v2.1.1), §4.2.3 (v2.3), §4.2.4 (v2.4), §4.2.5 (v2.5) are orthogonal parallel amendments; wave-1 pre-dates their LOCK windows but does not conflict with their ordering.
scope: Wave 1 of the Tier 1 policy-lock Logician v2.2 queue (memory ref project_tier1_lock_sealed_2026-04-20.md). Two predicates that detect structural omissions in Judge / RedTeam verdict JSON emissions — the canonical-bytes floor for revision_loop convergence arithmetic and the citation-resolution floor for Editor rubric claims.
companion_code:
  - pipeline/logician/gates/f_verdict_blocking_missing.py  (116 LOC, sha3_512[:16]=ca0d7992ad2cd839)
  - pipeline/logician/gates/f_verdict_citation_missing.py  (235 LOC, sha3_512[:16]=d405ddd9cb7caf53)
  - pipeline/logician/gates/__init__.py                    (42 LOC,  sha3_512[:16]=7c11e98265f967b4)
companion_tests:
  - tests/logician/gates/test_f_verdict_blocking_missing.py        (52 unit)
  - tests/logician/gates/test_adv_f_verdict_blocking_missing.py    (9 adversarial)
  - tests/logician/gates/test_f_verdict_citation_missing.py        (42 unit)
  - tests/logician/gates/test_adv_f_verdict_citation_missing.py    (12 adversarial)
committee_round: logician_v2_2_wave_1 (cycle-1 all-pass, 5/5, zero findings)
version_wording_discipline: "LOCKED" refers to on-disk LOCKED state only. Forward-looking targets use "target-LOCK at" wording.
---

# Amendment intent

Two new POST-gate predicates enforcing structural floors on reviewer verdict JSON:

- **F-AMDT-02 (F-VERDICT-BLOCKING-MISSING).** Reviewer seats (Judge, Editor, RedTeam) emitting verdict JSON must include a top-level `blocking` key whose value is a strict Python `bool`. The §5 revision-loop orchestrator (`pipeline.loop.revision_loop`) reads this field at convergence-check time; silent absence or duck-typed truthy values (`1`, `"true"`, `numpy.bool_`, classes with `__bool__`) would silently pass convergence and ship unblocked work. Gate fails closed — structural omissions and type-confusion DENY.
- **F-AMDT-03 (F-VERDICT-CITATION-MISSING).** Reviewer seats claiming per-dimension evidence in a verdict must resolve every whitespace-split token of each `dimensions[*].evidence` string as a case-sensitive substring of the draft under review. Evidence that names tokens absent from the draft is rubric-fabrication; gate fails closed. Draft access is via injected `DraftReaderCallable` Protocol — the gate never opens files directly (AST-lint R3 discipline, §4.3 no-I/O rule).

Both predicates are deterministic, pure-Python, zero-token, fail-closed POST-gates. They run under the §4 v2.1 `gate_runner` POST-phase orchestrator (§4.9 step ordering preserved; these two rows append to the §4.6 POST-gate row table).

# Proposed §4.6 POST-gate-check table additions

Two new rows append to the §4.6 POST-gate ordered table after the existing F-POST-* family. Both fire at the close of each Scribe→Editor→Judge iteration, before `run_inner_loop` consults the verdict's `blocking` field for convergence arithmetic.

| Order | Check ID | Fires at | Failure code | Source |
|---|---|---|---|---|
| POST-14 | F-VERDICT-BLOCKING-MISSING | per-iteration close (Judge / RedTeam verdict JSON) | `F-AMDT-02` | §4.6 wave-1 |
| POST-15 | F-VERDICT-CITATION-MISSING | per-iteration close (Editor verdict JSON with `dimensions[*].evidence`) | `F-AMDT-03` | §4.6 wave-1 |

Existing §4.6 POST-gate rows (POST-01 … POST-13) retain their ordering relative to each other. The two new rows sit at the tail of the POST phase so they benefit from all prior structural / admin-risk / claim-evidence / dossier-verify floors having cleared first.

# Proposed §6 failure-code family extension

Two new codes in the `F-AMDT-*` family (reserved for forward-looking amendment-landed POST-gate predicates, distinguished from `F-POST-*` which pins pre-existing §4.6 body rows).

| Code | Tier | Fires at | Detail taxonomy |
|---|---|---|---|
| `F-AMDT-02` | POST | per-iteration verdict close | `verdict_not_dict` / `blocking_key_absent` / `blocking_value_not_bool` |
| `F-AMDT-03` | POST | per-iteration verdict close | `verdict_not_dict` / `dimensions_key_absent` / `dimensions_not_list` / `draft_reader_raised` / per-dimension: `dimension_entry_not_dict` / `evidence_key_absent` / `evidence_not_string` / `evidence_empty` / `evidence_whitespace_only` / `evidence_tokens_unresolved` |

Naming convention matches existing `F-PRE-*` / `F-POST-*` patterns; category prefix `F-AMDT-` is reserved for Wave 1+ v2.2 amendment-landed predicates. All fail-closed semantics.

# §4.9 step-ordering note

Wave 1 adds no new POST-phase steps. POST-14 and POST-15 register as additional rows the existing §4.9 `gate_runner` POST orchestrator iterates. No change to pre_gate / between_gate / post_gate / done state machine. No change to §4.12 deep-inspect abort-payload validator. No change to §4.13 cross-org runtime predicate.

# §4.3 no-I/O rule compliance

- `f_verdict_blocking_missing.py`: pure structural predicate over the verdict `dict`. No file I/O. No injected Protocol required.
- `f_verdict_citation_missing.py`: requires draft text. Draft text is injected via `DraftReaderCallable` Protocol (runtime-checkable, single-method `__call__(draft_path: str) -> str`). The gate never calls `open()`. AST-lint R3 (`logician-open-ban`) clean at module load. Pattern consistent with E-017 (injected-callable Protocol for §2 Vault trust primitives).

# Reviewer seat contract

- **Judge / RedTeam:** verdict JSON must be a `dict` with a top-level `blocking` key whose value is a Python `bool` (not `int`, not `str`, not a duck-typed truthy class). Convergence arithmetic in `pipeline.loop.revision_loop.run_inner_loop` consumes this field; a missing or wrong-typed value is a hard-stop POST failure under F-AMDT-02.
- **Editor:** verdict JSON must be a `dict` with a top-level `dimensions` key whose value is a `list` (not `tuple`, not `dict`). Each dimension entry must be a `dict` with a string-valued `evidence` field. Every whitespace-split token of `evidence` must appear as a case-sensitive substring of the draft identified by `draft_path`. Unicode normalization is NOT performed: composed `café` (`\u00e9`) and decomposed `cafe\u0301` are different token byte sequences by design — the gate enforces exact byte/grapheme match.
- **Empty `dimensions: []` is vacuously PASS.** An Editor rubric with no dimensions to score has no citation claim to verify. The gate does not fabricate a floor. This is documented in the §4.6 POST-15 row and tested at `tests/logician/gates/test_f_verdict_citation_missing.py::test_dimensions_empty_list_vacuous_pass`.

# Non-goals for this wave

- Does not validate verdict JSON shape beyond the two structural floors. Rubric-content validation (12-dimension completeness, score ranges, cross-family checks) remains with the seat under review.
- Does not run semantic similarity / normalization on evidence tokens. Strict byte/substring match is the floor; richer resolution (stemming, NFC normalization, fuzzy match) is out of scope for Wave 1 — flag as a v2.2 Wave 2 candidate if a future rubric requires it.
- Does not add a CI hook. Operator-run under `gate_runner` POST phase; §5 v6 pipeline orchestrator invokes the runner.
- Does not introduce a new primitive kind in §0.5. Both rows register as `post-gate-check` + `failure-code` pairs per existing §0.5 v4 schema.

# §0.5 paired-commit rows

This §4 v2.2 wave-1 amendment LOCKs atomically with the following §0.5 paired-commit rows (to be appended in the next §0.5 LOCK window; wave-1 itself does not touch §0.5 — the pointer is authored here so the §0.5 LOCK captures them):

| Row | Kind | Pin |
|---|---|---|
| `logician.gates.f_verdict_blocking_missing` | post-gate-check | `pipeline/logician/gates/f_verdict_blocking_missing.py` sha3_512[:16]=ca0d7992ad2cd839 |
| `logician.gates.f_verdict_citation_missing` | post-gate-check | `pipeline/logician/gates/f_verdict_citation_missing.py` sha3_512[:16]=d405ddd9cb7caf53 |
| `logician.gates.__init__` | interface-contract | re-export surface for F_AMDT_02 / F_AMDT_03 / result dataclasses / DraftReaderCallable Protocol |
| `failure-code.F-AMDT-02` | failure-code | §4.6 POST-14 |
| `failure-code.F-AMDT-03` | failure-code | §4.6 POST-15 |

Forward-looking: F-INDEX-STALE PRE-gate in §0.5 v4 fires-closed if the paired commit is skipped. Authoring discipline: §0.5 v4 target-LOCK absorbs these rows in its next window; the `lock_history.v1.jsonl` rows for wave-1 reference this amendment path as `blueprint_section`.

# Evidence

- Spec cards: `pipeline/engineering/spec_cards/logician_v2_2_f_verdict_blocking_missing.md`, `pipeline/engineering/spec_cards/logician_v2_2_f_verdict_citation_missing.md`
- Code (per companion_code front-matter above).
- Tests (per companion_tests front-matter above): **115 new tests** — 61 Gate-1 (52 unit + 9 adv) + 54 Gate-2 (42 unit + 12 adv). 100% coverage on both modules and the re-export surface (107/107 statements).
- Full suite regression: **2539 pre → 2654 post** (+115). 3 skip, 1 xfail (unchanged). Zero failures.
- AST-lint: R1–R7 clean (`scripts/run_lint.sh` exit 0).
- Code Thesis Committee: 5-family all-pass cycle-1 (groq/qwen3-32b, groq/llama-3.3-70b-versatile, groq/openai/gpt-oss-120b, google/gemini-2.5-pro, google/gemini-2.5-flash). Zero findings at any severity. Synthesis at `pipeline/validation/code_reviews/logician_v2_2_wave_1/synthesis.md`.

# End of amendment
