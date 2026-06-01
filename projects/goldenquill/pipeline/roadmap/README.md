# Roadmap — Tilth Pipeline

Post-v0.1 explorations, design notes, and reference reviews. Nothing here is committed — these are candidates for v0.2+ scoping.

## Explorations

| File | Topic | Stage | Created |
|---|---|---|---|
| `explorations/narrative_spine_design.md` | Per-grant operator-approved spine + 4 stop points (SP1-SP4) + human-in-the-mix doctrine | v0.2 | 2026-05-06 |
| `explorations/key_facts_register_design.md` | Per-org structured 5W1H register + SP0 + F-LOGICIAN-FACT-DRIFT | v0.2 (high priority) | 2026-05-06 |
| `explorations/thesis_review_team_runtime_design.md` | Runtime 3-seat TRT board for grant sections (Option B + strong cross-family + Editor/Judge/Red-Team) | v0.2 | 2026-05-06 |
| `explorations/sector_knowledge_packs_design.md` | Per-sector JSON vocabulary packs for Scribe PRE-gate | **BUILT 2026-05-08** — schema diverges from this exploration (richer: domains + facts + relationships, mirrored from SSI Booster prior art); loader at `pipeline/seats/scribe/knowledge_packs.py`; six seed packs at `pipeline/knowledge_packs/<sector>/`; merge helper wired into `pipeline/orchestrator/scribe_envelope_builder.py` | 2026-05-06 |
| `explorations/explain_grounding_diagnostic.md` | Per-sentence BM25 evidence diagnostic for Scribe drafts (dev-only) | v0.2 dev tooling | 2026-05-06 |
| `explorations/ssi_booster_reference_review.md` | Reference review of linkedin_ssi_booster repo — patterns, dismissals, FWHP connections | reference | 2026-05-06 |
| `explorations/agent_skills_reference_review.md` | Reference review of addyosmani/agent-skills — anti-rationalization tables, Red Flags, source-driven dev, git workflow | reference | 2026-05-06 |

## Spec Cards (v0.2 queue)

| File | Gate/Module | Stage | Status |
|---|---|---|---|
| `../engineering/spec_cards/logician_fabricated_org_ner_gate.md` | F-LOGICIAN-FABRICATED-ORG — spaCy NER org validation | v0.2 | **BUILT 2026-05-08** — gate at `pipeline/logician/gates/f_logician_fabricated_org.py`; wired into `post_gate.run_post_gate_skeleton`; spaCy + rapidfuzz added to pyproject.toml |
| `../engineering/spec_cards/logician_spine_drift_gate.md` | F-LOGICIAN-SPINE-DRIFT — narrative spine adherence | v0.2 | **BUILT 2026-05-08** — gate at `pipeline/logician/gates/f_logician_spine_drift.py`; loader + 5 check axes (framing recall, anti-contradiction, dialect, admin-risk-avoid, schema); wired into `post_gate.run_post_gate_skeleton`; pure-stdlib (pyyaml only) |
| `../engineering/spec_cards/logician_fact_drift_kfr_gate.md` | F-LOGICIAN-FACT-DRIFT — KFR numeric drift gate | v0.2 | **BUILT 2026-05-08** — gate at `pipeline/logician/gates/f_logician_fact_drift.py`; KFR loader + numeric-claim extractor + 5-char prefix stemmer + per-fact tolerance; **v0.2.B spaCy POS augmentation landed 2026-05-08** (NOUN/PROPN/ADJ filter via lazy-loaded `en_core_web_sm`, regex fallback when spaCy unavailable); wired into `post_gate.run_post_gate_skeleton` |
| `../engineering/spec_cards/orchestrator_scribe_prompt_assembler.md` | Scribe prompt-assembler — produces `compiled_prompt + shell_hash` for envelope-builder | v0.2 | **SPEC** — open questions resolved 2026-05-08; ~250-350 LOC across 3 sub-rounds; consumes `RfaExtractedRecord` + `SectionSpec` + project_context + sector pack; output feeds `build_scribe_envelope(...)` |

## Failure codes proposed (v0.2)

| Code | Source | Triggers | Status |
|---|---|---|---|
| `F-LOGICIAN-FABRICATED-ORG` | NER gate spec card | ORG entity in draft not in PROJECT_CONTEXT allowlist | **BUILT + wired** |
| `F-LOGICIAN-SPINE-DRIFT` | Spine spec card | Scribe revision or Editor edit removes/weakens locked spine element | **BUILT + wired** |
| `F-LOGICIAN-FACT-DRIFT` | KFR spec card | Numeric claim in draft doesn't trace to KFR within tolerance | **BUILT + wired** |

## Stop points proposed (v0.2)

| Stop Point | When | Operator Reviews |
|---|---|---|
| SP0 | Before KGIE preflight | KFR freshness — fact expiries, RFA-required gaps |
| SP1 | After KGIE, before drafting | Spine lock — framings, dialect register, SMART shape |
| SP2 | Per section boundary | TRT findings + drafted section |
| SP3 | Pre-Editor (whole draft) | Scribe confidence declarations per section |
| SP4 | Post-Editor / Pre-Judge | Editor's clarity changes + spine adherence delta |

## Doctrine additions proposed (v0.2)

- **Human-in-the-mix stop points are critical.** Time saved by stopping > time required to remediate contaminated memory downstream. Promote to numbered Lesson.
- **Tilth reviews grants the way Tilth was built.** Cross-family thesis review at runtime, not "trust the model."

## Pending CLAUDE.md / SESSION_BOOTSTRAP.md cleanup

- Remove LangGraph from substrate enumeration (never wired) — *handled in v7.0.3 substrate amendment per CLAUDE.md line 205*
- ~~Rewrite Stage 2 description: 12 Tilths (12 deployments), not within-org scaling~~ — **DONE.** CLAUDE.md and SESSION_BOOTSTRAP.md both canonical on "Twelve Tilths." Stale "small team" references in LOCKED architecture docs (pre-amendment) and pre-LOCK validation snapshots are left in place — they reference "per CLAUDE.md" so the canonical lookup remains correct.
