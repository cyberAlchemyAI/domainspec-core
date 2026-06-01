---
title: Tilth Architecture — Amendment v7.0.2 (Substrate-text reconciliation — Section A v0.1 scope-locks + Section A hardware paragraph)
filed: 2026-05-04
operator: Josh Inklovich
amendment_status: SELF-LOCKED 2026-05-04 — textual amendment; zero mechanism change; the locked Section 5, Section 6, and Section 7 blueprints already implement the v10 substrate; this file aligns Section A copy with what is already on disk.
parent_lock: pipeline/architecture/v0.1/tilth_architecture_locked.md
companion_amendment: pipeline/architecture/v0.1/architecture_v7_0_1_amendment.md
companion_files_edited:
  - CLAUDE.md
  - pipeline/engineering/king_midas_implementation_prompt_v2_1.md
scope_source: Improvement_Plan_2026-05-04.md  # Track A item A1
authority_source: CTO_Review_2026-05-04/02_Architecture_Document.md  # §2.3 substrate-framing delta + §3 v10 substrate enumeration
version_wording_discipline: "LOCKED" inside this file refers to on-disk LOCKED state at filing time. Forward-looking version targets use TARGET-LOCK wording and are excluded from VERSION-RESOLVE per GPP-DET Bug-2 fix.
---

# Amendment intent

Architecture v7 LOCKED 2026-04-19 carries a stale Section A v0.1 scope-locks line and a stale Section A hardware paragraph that contradict the locked downstream blueprints and the v10 product copy that the operator has filed in `Improvement_Plan_2026-05-04.md` and `CTO_Review_2026-05-04/02_Architecture_Document.md`.

Section A still reads:

> Golden Quill = hardware (Mac Studio-class, 64GB baseline; Golden Quill Pro at 128GB).

> v0.1 scope locks (closed): headless only; no LangGraph / vLLM / local 70B / NemoClaw / Phase 3; no metered billing; no Managed Edition; no Next.js.

The first paragraph contradicts Section K (already widened in v7 to a 128 GB floor with Pro / Baseline / Dev tiers). The second paragraph contradicts the v10 substrate — LangGraph (orchestration), Pydantic AI (structured-output + Logfire observability), OpenClaw curated (document-parsing skill set), Ollama or vLLM (local inference), DSPy + GEPA (offline Card refinement, Library development only) — which the LOCKED `pipeline/blueprint/v0.1/section_05_pipeline.md`, `pipeline/blueprint/v0.1/section_06_operating_envelope.md`, and `pipeline/blueprint/v0.1/section_07_scribe.md` already implement.

This amendment is **textual reconciliation only**. No A-letter mechanism is modified. No new failure code is introduced. No new Cedar rule, no new admin-risk register row, no new out-of-model anchor. The reconciliation closes the contradiction a reader would otherwise spot between Section A and Section K / v10 substrate before the next outside review.

# What changes (proposed Section A textual updates)

## Edit 1 — Section A hardware paragraph

**Replace** (Section A first sentence, currently stale):

> Golden Quill = hardware (Mac Studio-class, 64GB baseline; Golden Quill Pro at 128GB).

**With**:

> Golden Quill = hardware (Apple Mac Studio M3 Ultra or NVIDIA DGX Spark Grace Blackwell GB10 class, 128 GB unified-memory floor; Dev tier is the Apple M1 Mac Mini 8 GB development node only). The 128 GB floor matches Section K v7 widened triple-target. All v3-era 64 GB and 32 GB references are retired.

**Authority.** Section K v7 widened table; CTO Review §3 target-state hardware paragraph; v10 Appendix D memory budget on a 128 GB Pro tier.

## Edit 2 — Section A v0.1 scope-locks line

**Replace** (currently stale):

> v0.1 scope locks (closed): headless only; no LangGraph / vLLM / local 70B / NemoClaw / Phase 3; no metered billing; no Managed Edition; no Next.js.

**With**:

> v0.1 substrate (LOCKED in downstream blueprints): orchestration is LangGraph (state graph plus human-in-the-loop interrupts at section boundaries, multi-model routing, posture enforcement, audit-log generation, the Grant Module Mapper, the split-context drafting pattern); structured-output and observability is Pydantic AI plus Logfire (per-section schema validation, Capital Logic Card schema enforcement, type-safe tool integration, OpenTelemetry-native and self-hostable for Sovereign mode); document substrate is OpenClaw curated, frozen at Golden Image build with no marketplace access from the appliance; local inference is Ollama or vLLM serving an OpenAI-compatible endpoint (a 70B-class primary model plus an embedding model plus on-demand larger checkpoints); offline Card refinement is DSPy plus GEPA, used in Library development not in customer deployments; compliance is Logician (deterministic Python plus Cedar policy engine, fail-closed, zero-token, all Five Laws as PRE / POST / COMMIT gates).

> v0.1 scope locks (closed, additive on top of the substrate above): headless only — no UI in v0.1; BYOK only — no Managed Edition, no metered billing; PA Ag Innovation Grant is not a dogfood target; Phase 2+ horizon items (Marketplace OpenClaw skill installs from the appliance; Stage 2 multi-Cultivator seats; Stage 3 cooperative-org Law 3 extension; Stage 4 contractor federation; Stage 5 MaatAI on Sovereign Node) stay out-of-scope-for-v0.1.

**Authority.** Improvement Plan A1; CTO Review §3 target-state software-stack enumeration; v10 Appendix D substrate canon; LOCKED `pipeline/blueprint/v0.1/section_05_pipeline.md` (orchestration + run-lifecycle); LOCKED `pipeline/blueprint/v0.1/section_06_operating_envelope.md` (router schema + SFR parser + context-placement enforcement); LOCKED `pipeline/blueprint/v0.1/section_07_scribe.md` (claim-evidence map + Five-Laws enforcement mapping).

# Companion file edits (paired with this amendment)

## CLAUDE.md `What NOT to Do`

The line "Do not propose LangGraph, vLLM, local 70B models, NemoClaw, or Phase 3 orchestration for v0.1" is retired and replaced with a substrate-replacement guard plus a Phase 2+ horizon guard. The locked substrate is the v10 stack named above; the prohibition that survives is on substrate replacement and on Phase 2+ horizon work.

## King Midas v2.1 §13 `Never do`

The clause "propose LangGraph/vLLM/local 70B/NemoClaw" is retired and replaced with a substrate-replacement clause matching CLAUDE.md. King Midas continues to refuse Phase 2+ horizon work, Managed Edition, metered billing, UI, marketplace OpenClaw skill installs, and Sovereign Node / MaatAI v0.1 references.

# What this amendment does not do

- Does not modify A1-A12.
- Does not modify Section K (Section K already carries the 128 GB floor; this amendment aligns Section A to Section K, not the other way around).
- Does not modify the Five Operating Laws or the Four Autonomy Rules.
- Does not introduce any new council seat, failure code, or Cedar rule.
- Does not modify any LOCKED blueprint (Section 5 / Section 6 / Section 7 already carry the v10 substrate; this amendment closes the architecture-text gap, not the implementation gap).
- Does not modify `router.yaml`.
- Does not change the BYOK posture, the headless posture, the fail-closed posture, or the cross-family rigor posture.
- Does not change the Sovereignty Promise.
- Does not propose Phase 2+ horizon work as in-scope. Phase 2+ items remain out-of-scope-for-v0.1; the amendment's purpose is to retire stale guard text, not to widen the v0.1 fence.

# Predecessor blockers acknowledged out-of-scope

This amendment is a textual reconciliation of Section A. It does not carry, defer, or resolve predecessor existence-audit blockers tracked elsewhere — `F-PRIVACY-*` failure-code family, `F-CANARY-*` failure-code family, `F-ROUTER-FAMILY-COLLISION` failure-code, `F-RAILS-REPORT-EMISSION-FAIL` failure-code, `F-KEY-PRESENCE-PREFLIGHT-FAIL` failure-code, `F-RUNTIME-DRIFT-FROM-LOCKED-ROUTER` failure-code, Content-scan classifier technology candidate, the `§5` per-invocation record schema with token-count-input, token-count-output, success-flag, and seat fields, the `§5` telemetry-record hook for per-seat invocation, and the STR derivation formula for the ratio of success_flag to token sum aggregated as a rolling distribution. Each blocker stays owned by its respective amendment round per `pipeline/validation/integration_scope_close_2026-04-19/05_preflight_existence_audit.md` and `pipeline/validation/blueprint_sequencing_preflight_2026-04-19/existence_audit.md`.

# Tier 1 GPP-DET — single-file scope

This amendment is dispatched at Tier 1 GPP-DET as a single-file plan-layer artifact per the `Improvement_Plan_2026-05-04.md` Track A item A1 done-criteria. Tier 2 / Tier 3 GPP do not apply because v7.0.1 (the GPP amendment itself) has not yet LOCKed; v7.0.2 is filed under the same single-cycle textual-amendment discipline that v6 revision 2 used (no mechanism change, no new failure code, no new Cedar rule). Once v7.0.1 LOCKs, future textual reconciliation amendments will pass through full Tier 1 + Tier 2 + Tier 3.

# What a reviewer should expect

A reader of `pipeline/architecture/v0.1/tilth_architecture_locked.md` after this amendment will see Section A's hardware paragraph match Section K and v10, and Section A's v0.1 scope-locks line name the LOCKED v10 substrate explicitly rather than carry a stale prohibition against it. CLAUDE.md `What NOT to Do` and King Midas v2.1 §13 `Never do` will mirror the same substrate framing. No code is touched. No test is added or removed.

# End of amendment
