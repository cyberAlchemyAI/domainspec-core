---
title: Tilth Architecture — Amendment v7.0.13 (Card Runtime Wiring — DRAFT, pending L-005)
filed: 2026-05-18
operator: Josh Inklovich
amendment_status: DRAFT — LOCK-READY. Pending L-005 strict two-cycle Thesis dispatch (Editor=Llama-3.3-70B/Groq + Judge=Gemini-2.5-Pro/Google + Red Team=GPT-OSS-120B/Groq via openclaw bridge per AGENTS.md). Not authoritative until LOCK ceremony completes with audit trail at pipeline/validation/v7_0_13_thesis_<date>/ and lock_history row appended.
parent_lock: pipeline/architecture/v0.1/tilth_architecture_locked.md
parent_amendments_chain:
  - v7.0.11 (LOCK-READY DRAFT; row pending) — Card system architectural primitive (schema + lifecycle + loader contract + memory namespace + signed-asset publisher trust + F-CARDS-* family). **LOAD-BEARING PRECEDENT for this amendment — v7.0.13 lifts the v7.0.11 §5 v0.2-first-wave NotImplementedError boundary at the seat-injection step (§1.5 step 8) to a LIVE body.**
  - v7.0.12 (LOCK-READY DRAFT) — apolitical dialect amendment
companion_amendments_pending_LOCK:
  - pipeline/blueprint/v0.1/section_00_5_section_18_card_runtime_wiring_amendment.md   # §0.5 paired-commit (DRAFT)
authority_source: Operator directive 2026-05-18 ("Wire the 4 runtime seats (Scribe / Scout / Judge / Editor) to read per-card behavioral differentiation at runtime"). Specified branch and scope. v0.2 first wave LOCK ceremony per existing precedent — DRAFT lands the architecture amendment + paired §0.5 + code + tests; thesis dispatch + Ed25519 signature ceremony run post-PR.
version_wording_discipline: "DRAFT" inside this file means "not yet LOCKED via L-005 two-cycle audit." The file shape, frontmatter, and section structure are LOCK-ready — Editor / Judge / Red Team can run the cross-family Thesis round directly against this file. Any LOCK ceremony updates this frontmatter to "amendment_status: LOCKED <date> ..." with cycle-1 + cycle-2 dispositions, appends a lock_history row, and triggers the companion-amendment paired-commit per §6.17 Option-B.
audit_trail: pipeline/validation/v7_0_13_thesis_<date>/   # populated when L-005 round dispatches
session_metrics: pipeline/metrics/session_log.jsonl
---

# Amendment intent

v7.0.11 (Card System) introduced the Card as an architectural primitive — signed YAML on disk, schema-validated, lifecycle-gated, manifest-membership-gated, coupling-discipline-enforced. v7.0.11 §5 deferred the seat-injection runtime registration step (loader step 8 per §1.5) to v0.2 first wave, marked at the loader as `raise NotImplementedError(...)` so a valid runtime card that passed all preflight gates would still fail closed at the final step. The four runtime seats (Scout / Scribe / Editor / Judge) carried no per-card behavioral differentiation at v0.1 Beta LOCK — the cards existed on disk but did not yet route seat behavior.

**v7.0.13 graduates that step LIVE for v0.2 first wave.** A valid card now returns a `LoadedCard` with the parsed `CICCard` / `CLCCard` model + the consuming-seat roster computed from the static seat-dependency registry. A new `CardRuntimeContext` primitive composes one CIC + one CLC into a cycle-bound pair-of-cards object. Each consuming seat carries a `card_wiring.py` module that projects the seat-relevant subset of the context into a frozen, kw-only, slots `{Seat}CardView` consumed by the seat's prompt assembly.

The amendment is intentionally narrow:

- **§1 (this amendment)** lifts the loader NotImplementedError, adds `CardRuntimeContext`, populates the `Editor` seat into the consuming-seat roster, and populates the four runtime seats' card-field dependency declarations.
- **§0.5 (paired amendment)** registers `pipeline.cards.runtime_context` + four `card_wiring.py` modules + the v0.2-first-wave-populated `pipeline.cards.seat_dependencies` registry as interface-index entries.

The §18 blueprint §B "v0.2 first wave scope" content is realized at this LOCK; the §18 narrative does not need to change because §18.16.B was authored as binding spec at v7.0.11 LOCK.

# What changes

## §1. Loader graduates step 8 from NotImplementedError to LIVE body

### §1.1 LIVE seat-injection runtime registration

`pipeline.cards.loader.load_card` now returns a `LoadedCard` whose:

- `namespace` is the canonical `cards:cic:<slug>` / `cards:clc:<slug>` shape per v7.0.11 §1.9.
- `card` is a parsed frozen `CICCard` / `CLCCard` dataclass instance (per `pipeline.cards.models`).
- `card_path` is the resolved on-disk absolute path the card was loaded from.
- `runtime_registered_seats` is the per-axis seat roster computed by walking `pipeline.cards.seat_dependencies.SEAT_CARD_FIELD_DEPENDENCIES` and listing every seat whose declared dependency set for the loaded card's axis is non-empty.
- `canonical_bytes_sha256` is the same byte recipe as the lifecycle.content_hash invariant verified during preflight (deterministic key ordering, signature + content_hash fields excluded).

### §1.2 Multi-track CLC + matrix cards stay NotImplementedError

The §18.6 v2 Option A multi-track CLC shape (`track_a` + `track_b` containers) remains v0.2-second-wave scope. `load_card` detects multi-track at the post-preflight step and raises NotImplementedError with the v0.2-second-wave deferral message. Matrix cards remain forbidden until the v1.x explicit amendment lifts the v7.0.11 §1.8 boundary; if `v1_x_matrix_phase_active=True` is ever passed, the loader still raises NotImplementedError because matrix runtime context injection is independent v1.x scope.

### §1.3 Lifecycle / coupling / manifest preflight unchanged

All pre-step-8 invariants — F-CARDS-SCHEMA-INVALID, F-CARDS-MALFORMED-LIFECYCLE, F-CARDS-COUPLING-VIOLATION, F-CARDS-COUPLING-VIOLATION-EXTENSION, F-CARDS-UNSIGNED-PRODUCTION-LOAD, F-CARDS-NOT-IN-ACTIVE-MANIFEST — fire identically. A draft / malformed / coupled / unregistered card never reaches the LIVE step 8 body.

## §2. CardRuntimeContext primitive (blueprint §18.16.B step 1)

`pipeline.cards.runtime_context.CardRuntimeContext` is a frozen + kw-only + slots dataclass holding:

- `cic: CICCard` — active applicant-side card.
- `clc: CLCCard` — active funder-side card.
- `cic_path: str` — resolved on-disk path.
- `clc_path: str` — resolved on-disk path.

`__post_init__` asserts axis invariants (CIC slot carries CIC, CLC slot carries CLC). The convenience constructor `build_card_runtime_context(cic_path=, clc_path=, environment=, manifest_path=)` delegates to `load_card` for each axis and assembles the context.

`CardRuntimeContext` is bound to one cycle for one org per Law 3 — cross-org reuse is structurally impossible because cards carry workspace-shared knowledge only.

## §3. Per-seat card_wiring modules (blueprint §18.16.B steps 2-4)

Four new modules ship at this amendment, one per v0.2-first-wave runtime seat:

| Module | View | Reads from CIC | Reads from CLC |
|--------|------|----------------|----------------|
| `pipeline.scout.card_wiring` | `ScoutCardView` | search_vocabulary, evidence_signals, kfr_fact_classes, admin_risk_term_register | underwriting_criteria |
| `pipeline.seats.scribe.card_wiring` | `ScribeCardView` | register_defaults, dialect_routing_table, admin_risk_term_register, narrative_sections_typical | narrative_section_patterns, evidence_weights, budget_structure_conventions |
| `pipeline.seats.editor.card_wiring` | `EditorCardView` | register_defaults, dialect_routing_table, admin_risk_term_register | common_red_flags, reviewer_profile_typical, narrative_section_patterns |
| `pipeline.seats.judge.card_wiring` | `JudgeCardView` | capacity_signals_required, compliance_burdens | underwriting_criteria, scoring_weight_patterns, evidence_weights, reviewer_profile_typical, common_red_flags |

Each module exports a `{Seat}CardView` frozen dataclass and a `build_{seat}_card_view(context)` pure function. Views are immutable per A12 mandate.

## §4. Existing v1 envelopes unchanged at v0.2 first wave

`scribe-envelope.v1` / `editor-envelope.v1` / `judge-envelope.v1` carry their LOCKed shape. Card-context injection happens at the prompt-assembly layer upstream of envelope construction. An envelope rev (`*-envelope.v2`) carrying the active CIC + CLC slugs explicitly lands at v0.2 second wave alongside the multi-track CLC LOCK + the heavy-Judge swap card-substrate hardening — out of scope for this amendment.

## §5. Editor joins the consuming-seat roster

Blueprint §18.16.B as authored at v7.0.11 enumerated Scout / Scribe / Judge / Logician / Report Generator as consuming seats. The operator directive 2026-05-18 added Editor to the v0.2-first-wave runtime-seat set because Editor's clarity review reads voice / register / tone from CIC and reviewer-pov red flags from CLC — the same card-substrate as Scribe + Judge. `pipeline.cards.seat_dependencies.SEAT_NAMES` extends from 7 entries to 8 with `"Editor"` added; the `SEAT_CARD_FIELD_DEPENDENCIES` registry gains an `"Editor"` row populated with the field paths Editor's wiring module reads.

## §6. F-CARDS-* predicate bodies — partial graduation

The F-CARDS-* family roster from v7.0.11 §1.6 carries ten primitives. v0.2 first wave is **not** the LOCK that graduates every predicate body NotImplementedError → LIVE; that scope is the v0.2 mid-wave Logician hardening amendment (§4 v2.x.y, paired). What v7.0.13 graduates:

- F-CARDS-SCHEMA-INVALID — already LIVE at v7.0.11 LOCK candidate.
- F-CARDS-MALFORMED-LIFECYCLE — already LIVE at v7.0.11.
- F-CARDS-COUPLING-VIOLATION-EXTENSION — already LIVE at v7.0.11.
- F-CARDS-NOT-IN-ACTIVE-MANIFEST — already LIVE at v7.0.11.

The remaining six (F-CARDS-COVERAGE-INCOMPLETE, F-CARDS-UNSIGNED-PRODUCTION-LOAD, F-CARDS-SIGNATURE-INVALID, F-CARDS-PRIVATE-DATA-IN-CARD, F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY, F-CARDS-CROSS-ORG-NAMESPACE-LEAK, F-CARDS-LOAD-IN-WRONG-NAMESPACE) graduate per the v0.2 mid-wave Logician hardening amendment, which carries its own L-005 round.

## §7. AST-lint drift gate — R-CARDS-SEAT-DEPS-DRIFT

The v7.0.11 §7.3 R-CARDS-SEAT-DEPS-DRIFT AST-lint rule that cross-checks declared dependencies against actual seat reads ships as **paired-with v0.2 second wave** (not at this amendment). At v0.2 first wave the cross-check is enforced by per-seat unit tests at `tests/cards/test_seat_dependencies.py` that verify each populated seat row matches its `card_wiring.py` module's view-dataclass field roster. The AST-lint pattern lands later because the source-of-truth-side declarations are still landing; the test-side check is sufficient bridge.

# §8 — Compound transaction at LOCK ceremony (§6.17 Option-B)

When L-005 LOCKs this amendment, the following files paired-commit at the same `lock_timestamp_utc`:

- `pipeline/architecture/v0.1/architecture_v7_0_13_card_runtime_wiring_amendment.md` (this file)
- `pipeline/blueprint/v0.1/section_00_5_section_18_card_runtime_wiring_amendment.md` (paired §0.5)
- `pipeline/cards/loader.py` (load_card live body)
- `pipeline/cards/runtime_context.py` (CardRuntimeContext)
- `pipeline/cards/seat_dependencies.py` (Editor + populated runtime-seat rows)
- `pipeline/scout/card_wiring.py`
- `pipeline/seats/scribe/card_wiring.py`
- `pipeline/seats/editor/card_wiring.py`
- `pipeline/seats/judge/card_wiring.py`
- `pipeline/seats/README.md` (wiring contract docs)
- `tests/cards/test_runtime_context.py` (new)
- `tests/cards/test_models_and_schemas.py` (NotImplementedError → LoadedCard tests)
- `tests/cards/test_lifecycle_truth.py` (NotImplementedError → LoadedCard test)
- `tests/cards/test_active_card_registry_gate.py` (three NotImplementedError → LoadedCard tests)
- `tests/cards/test_seat_dependencies.py` (empty-registry tests → populated-registry tests)
- `tests/seats/scribe/test_card_wiring.py` (new)
- `tests/seats/editor/test_card_wiring.py` (new)
- `tests/seats/judge/test_card_wiring.py` (new)
- `tests/scout/test_card_wiring.py` (new)
- `tests/seats/test_card_wiring_integration.py` (new)
- `lock_history.yaml` (new row appended at LOCK ceremony)
