ORG:goldenquill
TRACE:v7-0-5-thesis-cycle-1-2026-05-09

You are reviewing **architecture amendment v7.0.5** for Tilth (the agentic grant-intelligence software running inside the Golden Quill 128 GB hardware appliance). Author family: Anthropic (Claude). Reviewer family per L-003: non-Anthropic. Cross-family rigor applies.

## Project context (concise — canonical references by path)

- Tilth's v0.1 council is six seats: Scout (discovery), Scribe (drafting), Editor (clarity pre-Judge), Judge (rubric scoring), Red Team (adversarial), Logician (deterministic Python + Cedar gates, fail-closed, zero-token). Plus support agents Intake (v0.1, KFR ingestion at onboarding), Uploader (v0.1, submission package — operator clicks final submit), Data Collector + Report Generator (v0.2 horizon), Archivist (v1.x horizon).
- Five Operating Laws (non-negotiable): (1) RFA-is-truth, (2) No-boundary-drift, (3) **Org Isolation** — one PROJECT_CONTEXT per session, no cross-org reads ever, (4) Apolitical-language + admin-risk register, (5) Applicant-brings-substance — no fabricated credentials/data/partnerships.
- Substrate per v7.0.3 / ADR-001: Pydantic AI (orchestration + structured output) + Logfire + Ollama or vLLM (local inference, OpenAI-compatible endpoint) + DSPy/GEPA (offline Card refinement only) + Logician (deterministic) + curated Python utilities (python-docx, openpyxl, pypdf) wrapped as Pydantic AI tools. **Frozen at Golden Image build; no marketplace access.** FAISS or Chroma + bge-large-en-v1.5 is the on-disk vector substrate already adopted by v7.0.4 KFR.
- v7 architecture LOCKED 2026-04-19 (A1-A12). v7.0.6 SELF-LOCKED 2026-05-09 (council + support-agent roster). v7.0.4 KFR + v7.0.7 classification routing are parallel SCOPING DRAFTs awaiting Thesis (concurrent with this round).
- Cooperative sovereignty consent tiers (per `memory/project_cooperative_sovereignty_optin.md`): `my_eyes_only` / `matchable_to_opportunities` / `composable_with_others`. Stage 5 = Sovereign Node cooperative-owned compute commons, **forward-design only — out-of-scope-for-v0.1 / v1 / v1.x**. v0.1 ships `my_eyes_only` default; commons does not exist yet.
- Sequencing: v7.0.5 lands AFTER v7.0.6 (uses Archivist curation-slot reservation), composes against v7.0.4 (orthogonal substrates — KFR per-org / Funder Intel per-funder), composes against v7.0.7 (classification per-entry on Match DB).

## Cross-cutting invariants the amendment must preserve

- **Law 3 (Org Isolation)** — the most Law-3-sensitive register in the architecture is being introduced here. Any cross-org read path or schema-level coupling is a **P0** architecture bug.
- **Substrate freeze** — no new infra dependencies. Must reuse FAISS/Chroma + bge-large-en-v1.5 + Pydantic AI from v7.0.3 / v7.0.4. No marketplace access.
- **Logician fail-closed** — every new failure code must be deterministic Python + Cedar, fail-closed by default, zero token cost.
- **Sovereignty Promise** — nothing phones home. Stage-5 commons participation is opt-in per consent tier; v0.1 ships defaults that guarantee zero exfil.
- **CIC × CLC orthogonality (v7.0.8 LOCKED)** — Customer Identity Categories (applicant-side, 6) and Capital Logic Cards (funder-side, 8) are orthogonal axes. No design-time coupling. Match logic is opportunity-driven runtime, never archetype-driven design-time. New schemas must pass F-CIC-CLC-COUPLING-VIOLATION audit.

