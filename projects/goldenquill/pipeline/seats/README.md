# pipeline/seats — Council seat subprocess entries

This directory contains the runtime subprocess entries for the six council seats plus support agents. Scout lives at `pipeline/scout/` (composed across `discover.py` + `verify_stage.py` + `review_stage.py` + `run.py`) for historical reasons; the other seats live here per the `seats/<name>/seat.py` pattern.

Subdirectories:

- `scribe/` — Round 3 subprocess entry, Anthropic-bound (§7 v1.1.1).
- `editor/` — Round 1 subprocess entry, clarity review (§8).
- `judge/` — Round 3 subprocess entry, Google-bound rubric scoring (§9).
- `red_team/` — Adversarial cross-family probe (§10).
- `intake/`, `uploader/`, `archivist/`, `data_collector/`, `report_generator/` — support agents per their respective blueprint sections.

## Per-card behavioral wiring (v0.2 first wave; architecture v7.0.13 §1 DRAFT)

Four runtime seats — **Scout / Scribe / Editor / Judge** — route their behavior off the active CIC × CLC card pair at runtime per blueprint §18.16.B. The wiring contract:

1. **One pair-of-cards object per cycle.** `pipeline.cards.runtime_context.CardRuntimeContext` holds one parsed `CICCard` + one parsed `CLCCard` plus their on-disk paths. Built once at cycle start via `build_card_runtime_context(cic_path=..., clc_path=..., environment=...)` which delegates to `pipeline.cards.loader.load_card` (full lifecycle / coupling / manifest / signature preflight).
2. **One `card_wiring.py` per consuming seat.** Each seat declares a frozen `{Seat}CardView` dataclass + a `build_{seat}_card_view(context)` pure-function projector:
   - `pipeline/scout/card_wiring.py` — `ScoutCardView`
   - `pipeline/seats/scribe/card_wiring.py` — `ScribeCardView`
   - `pipeline/seats/editor/card_wiring.py` — `EditorCardView`
   - `pipeline/seats/judge/card_wiring.py` — `JudgeCardView`
3. **Field reads are statically declared.** `pipeline.cards.seat_dependencies.SEAT_CARD_FIELD_DEPENDENCIES` maps each seat to its per-axis `frozenset` of top-level card-field paths. The view dataclass MUST mirror this declaration — drift between the registry and the view is the lint target for `R-CARDS-SEAT-DEPS-DRIFT` (v0.2 second-wave amendment).
4. **No envelope changes at v0.2 first wave.** Existing `scribe-envelope.v1` / `editor-envelope.v1` / `judge-envelope.v1` are unchanged. Card context is injected at the prompt-assembly layer upstream of the envelope. A `*-envelope.v2` rev that carries the active CIC + CLC slugs explicitly lands at v0.2 second wave alongside the multi-track CLC LOCK.

What each seat reads (top-level field paths from each card axis):

| Seat | From CIC | From CLC |
|------|----------|----------|
| Scout | `search_vocabulary`, `evidence_signals`, `kfr_fact_classes`, `admin_risk_term_register` | `underwriting_criteria` |
| Scribe | `register_defaults`, `dialect_routing_table`, `admin_risk_term_register`, `narrative_sections_typical` | `narrative_section_patterns`, `evidence_weights`, `budget_structure_conventions` |
| Editor | `register_defaults`, `dialect_routing_table`, `admin_risk_term_register` | `common_red_flags`, `reviewer_profile_typical`, `narrative_section_patterns` |
| Judge | `capacity_signals_required`, `compliance_burdens` | `underwriting_criteria`, `scoring_weight_patterns`, `evidence_weights`, `reviewer_profile_typical`, `common_red_flags` |

The Logician-as-consumer / Archivist / Report Generator / Model Router seats are registered in `SEAT_NAMES` but ship empty dependency sets at v0.2 first wave — their first-wave bindings land mid-wave (Logician + Archivist) / horizon (Report Generator). ModelRouter never reads card body fields; it routes by classification posture only.

## Wiring usage example

```python
from pipeline.cards.runtime_context import build_card_runtime_context
from pipeline.seats.scribe.card_wiring import build_scribe_card_view
from pipeline.seats.judge.card_wiring import build_judge_card_view

ctx = build_card_runtime_context(
    cic_path="pipeline/cards/CIC/food_systems.yaml",
    clc_path="pipeline/cards/CLC/operating_capacity.yaml",
    environment="production",
)

scribe_view = build_scribe_card_view(ctx)
# scribe_view.register_defaults → CIC register_defaults dict
# scribe_view.evidence_weights → CLC evidence_weights dict

judge_view = build_judge_card_view(ctx)
# judge_view.underwriting_criteria → CLC underwriting_criteria tuple
# judge_view.common_red_flags → CLC adversarial-probe flags
```

`CardRuntimeContext` and every `{Seat}CardView` are frozen + kw-only + slots dataclasses (A12 mandate). They are immutable and safe to pass through the prompt-assembly call chain.

## Boundaries (binding)

- **Single-track CLC only at v0.2 first wave.** Multi-track CLC (§18.6 v2 Option A `track_a` / `track_b` shape) — `pipeline.cards.loader.load_card` raises `NotImplementedError` at multi-track dispatch until v0.2 second wave.
- **Matrix cards forbidden at v0.2.** Same loader, deferred to v1.x matrix-phase explicit amendment.
- **No org-private data crosses into a `CardRuntimeContext`.** Cards are workspace-shared knowledge per `F-CARDS-PRIVATE-DATA-IN-CARD`; per-org data lives in `orgs/<slug>/` and stays out of the card layer entirely (Law 3).
- **CIC × CLC matching is opportunity-driven at runtime.** Per `F-CIC-CLC-COUPLING-VIOLATION` (architecture v7.0.8) + `F-CARDS-COUPLING-VIOLATION-EXTENSION` (v7.0.11), the card pair feeding a `CardRuntimeContext` is selected per opportunity at runtime — never via design-time archetype binding.
