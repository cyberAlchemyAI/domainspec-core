---
title: Tilth Architecture — Amendment v7.0.3 (Substrate corrective — Pydantic AI absorbs LangGraph + OpenClaw)
filed: 2026-05-08
operator: Josh Inklovich
amendment_status: SELF-LOCKED 2026-05-08 — textual amendment; zero mechanism change; the substrate decision was made in ADR-001 (2026-04-14 initial / 2026-04-19 final lock) and the on-disk codebase carries no LangGraph or OpenClaw imports; this file aligns the v7.0.2 substrate paragraph with the actual decision.
parent_lock: pipeline/architecture/v0.1/tilth_architecture_locked.md
parent_amendment: pipeline/architecture/v0.1/architecture_v7_0_2_amendment.md
companion_files_edited:
  - "CLAUDE.md (substrate paragraph + What NOT to Do guard)"
  - "Golden Quill Business Plan v10 3.docx → v10 4 (Appendix D paragraph + Table 28 substrate division of labor + Table 29 Hardware Budget) — coordinated edit; corrected file preserved as v10 4 so v10 3 stays as audit trail"
  - "docs/decisions/ADR-001.md, docs/ARCHITECTURE_OVERVIEW.md — already reflect Pydantic-only substrate per repo-init scaffolding 2026-05-06"
authority_source: docs/decisions/ADR-001.md  # full alternatives-considered for LangGraph and OpenClaw removal
version_wording_discipline: "LOCKED" inside this file refers to on-disk LOCKED state at filing time. The substrate is LOCKED at the spec layer (ADR-001); pyproject.toml integration of `pydantic-ai` and `logfire` is implementation work that lands when downstream blueprint sections that depend on it begin execution.
---

# Amendment intent

The v7.0.2 textual amendment (SELF-LOCKED 2026-05-04) named the v0.1 substrate as "LangGraph (orchestration) + Pydantic AI (structured-output) + OpenClaw (document substrate) + Ollama/vLLM (local inference) + DSPy/GEPA (offline refinement) + Logician (compliance)." That paragraph is stale.

ADR-001 (locked 2026-04-19) names the v0.1 substrate as "Pydantic AI (orchestration + structured output) + Logfire (observability) + Ollama/vLLM (local inference) + DSPy/GEPA (offline refinement) + Logician (compliance)." LangGraph and OpenClaw are removed; Pydantic AI absorbs both roles. ADR-001 carries full alternatives-considered for both removals (§Alternatives Considered, "LangGraph" and "OpenClaw" entries).

The on-disk codebase confirms: `pyproject.toml` does not declare `langgraph` or any OpenClaw runtime as a dependency. The repo-init files `docs/decisions/ADR-001.md` and `docs/ARCHITECTURE_OVERVIEW.md` already reflect the Pydantic-only substrate.

This amendment is **textual reconciliation only**. No A-letter mechanism is modified. No new failure code is introduced. No new Cedar rule, no new admin-risk register row, no new out-of-model anchor. The reconciliation closes the substrate divergence between the v7.0.2 amendment text, the v10.3 business plan Appendix D, CLAUDE.md, and the actual ADR-001 decision + on-disk codebase.

# What changes (Section A v0.1 substrate paragraph)

**Replace** (the v7.0.2 substrate paragraph, currently stale):

> v0.1 substrate (LOCKED in downstream blueprints): orchestration is LangGraph (state graph plus human-in-the-loop interrupts at section boundaries, multi-model routing, posture enforcement, audit-log generation, the Grant Module Mapper, the split-context drafting pattern); structured-output and observability is Pydantic AI plus Logfire (per-section schema validation, Capital Logic Card schema enforcement, type-safe tool integration, OpenTelemetry-native and self-hostable for Sovereign mode); document substrate is OpenClaw curated, frozen at Golden Image build with no marketplace access from the appliance; local inference is Ollama or vLLM serving an OpenAI-compatible endpoint (a 70B-class primary model plus an embedding model plus on-demand larger checkpoints); offline Card refinement is DSPy plus GEPA, used in Library development not in customer deployments; compliance is Logician (deterministic Python plus Cedar policy engine, fail-closed, zero-token, all Five Laws as PRE / POST / COMMIT gates).

**With**:

> v0.1 substrate (LOCKED at the spec layer per ADR-001): orchestration plus structured output plus observability is Pydantic AI plus Logfire (multi-model seat invocation, type-safe pipeline I/O between stages, per-section schema validation, Capital Logic Card schema enforcement, structured-output retry on validation failure, type-safe tool integration, agent lifecycle management, human-in-the-loop interrupts at section boundaries, multi-model routing, the Grant Module Mapper, the split-context drafting pattern, audit-log generation, OpenTelemetry-native tracing, self-hostable for Sovereign mode); document parsing is a curated set of Python utilities (python-docx, openpyxl, pypdf, and equivalents) wrapped as Pydantic AI tools, frozen at Golden Image build, no marketplace access from the appliance; local inference is Ollama or vLLM serving an OpenAI-compatible endpoint (a 70B-class primary model plus an embedding model plus on-demand larger checkpoints); offline Card refinement is DSPy plus GEPA, used in Library development not in customer deployments; compliance is Logician (deterministic Python plus Cedar policy engine, fail-closed, zero-token, all Five Laws as PRE / POST / COMMIT gates). LangGraph and OpenClaw — initially selected for orchestration and document substrate respectively — are removed; Pydantic AI's agent primitives and structured-output capabilities cover the same ground with less code, fewer dependencies, and a single auditable integration boundary.

**Authority.** ADR-001 §Decision and §Alternatives Considered (LangGraph removed: "Pydantic AI's agent primitives handle the same seat-invocation and state-passing patterns with less code. LangGraph's graph topology abstraction doesn't map to Tilth's linear pipeline with revision loops"; OpenClaw removed: "Pydantic AI's structured output and validation capabilities cover the same ground — type-safe document schemas, structured skill invocation, validation gates — without a separate dependency"); on-disk `pyproject.toml`; repo-init `docs/ARCHITECTURE_OVERVIEW.md` Substrate section.

# Companion file edits (paired with this amendment)

## CLAUDE.md substrate paragraph

The CLAUDE.md substrate paragraph that names "LangGraph (orchestration) + Pydantic AI (structured-output) + OpenClaw (document substrate)" is updated to match the v7.0.3 substrate text above. The substrate-replacement guard in `What NOT to Do` is updated to read "Do not re-propose LangGraph or OpenClaw — both removed per ADR-001 and v7.0.3 amendment; substrate replacements require a new architecture audit round."

## Golden Quill Business Plan v10 3.docx → v10 4

The v10.3 plan's Appendix D first technical paragraph (currently "LangGraph is selected as the orchestration core because..."), Table 28 (substrate division of labor across LangGraph / Pydantic AI / OpenClaw / Local inference / DSPy+GEPA), and Table 29 (Hardware Budget memory allocation, "Substrates and orchestration overhead ~8 GB" line) are updated to reflect the Pydantic-only substrate. The corrected file is saved as `Golden Quill Business Plan v10 4.docx` so the v10.3 original is preserved as audit trail.

This edit must land before the plan circulates to IF Ventures, Idea Foundry community, or any external investor / funder reader. Otherwise the plan contradicts the repo files and ADR-001 on a load-bearing technical decision.

# What this amendment does not do

- Does not modify A1-A12.
- Does not modify Section K hardware tier mapping.
- Does not modify the Five Operating Laws or the Four Autonomy Rules.
- Does not introduce any new council seat, failure code, or Cedar rule.
- Does not modify any LOCKED blueprint (Section 5 / Section 6 / Section 7 do not depend on a specific orchestration framework name; their pipeline contracts are framework-agnostic).
- Does not modify `router.yaml`.
- Does not change the BYOK posture, the headless posture, the fail-closed posture, or the cross-family rigor posture.
- Does not change the Sovereignty Promise.
- Does not propose Phase 2+ horizon work as in-scope.
- Does not modify the v7.0.2 amendment file itself (locked artifact preserved); supersedes its substrate paragraph by reference.

# Lock-history note

This amendment is the third v7.0.x corrective in the v7-Lock-line:

- v7.0.1 (DRAFT): Section E.P Governance Plan Preflight — awaiting Tier 1/2/3 GPP review + L-005 Thesis round before LOCK
- v7.0.2 (SELF-LOCKED 2026-05-04): Section A textual reconciliation — hardware paragraph + scope-locks line aligned with Section K v7 widened triple-target and v10 substrate enumeration as it stood at filing time
- v7.0.3 (SELF-LOCKED 2026-05-08, this file): Section A substrate paragraph aligned with ADR-001 Pydantic-only decision; supersedes v7.0.2's substrate text only

Forward-pending: v7.0.4 (KFR Amendment SCOPING DRAFT) and v7.0.5 (Funder Intelligence Database + Match Database SCOPING DRAFT).
