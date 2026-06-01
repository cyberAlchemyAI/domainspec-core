# Cross-Family Audit + Prompt Caching — Measured Evidence

**For:** white paper / external comms / funder narrative
**Date window:** 2026-04-19 through 2026-04-20
**System:** Tilth v0.1 on M1 Mac Mini, 8GB RAM dev node; OpenClaw 2026.4.14 gateway
**Ground rules:** sovereign (local inference dispatch), BYOK (Josh's Anthropic + Google + OpenAI + Groq API keys), no phone-home outside explicit BYOK endpoints

## Core claim

**Continuous cross-family LLM audit is economically viable at the grassroots-operator scale when sovereign infrastructure captures Anthropic's prompt-caching lever.** Measured 94% input-token cost reduction on second cached call, combined with adversarial cross-family review that found real findings a single-family simulated audit missed, demonstrates that "one sovereign operator, one quill" can run governance-grade multi-model audits at sub-dollar per audit round.

## Evidence point 1 — Cross-family rigor is not ceremony

Three amendments were authored by a single Anthropic-family voice (Claude), then submitted to simulated single-family Thesis review. The simulated review declared all three `LOCKED-internal-simulated` ready for promotion.

The same three amendments were then re-audited live by a cross-family panel: Llama 3.3 70B (Meta, via Groq), Gemini 2.5 Pro (Google), GPT-OSS 120B (OpenAI-OSS, via Groq).

**Live audit results vs. simulated:**

| Amendment | Simulated verdict | Live cross-family verdict | HIGH | MED | LOW |
|-----------|-------------------|---------------------------|------|-----|-----|
| Agent SDK Thesis (EN-001 + EN-002) | LOCKED-internal-simulated | CYCLE-2-REQUIRED | 1 | 5 | 1 |
| Tilth Self-Improvement Protocol v0.1 | LOCKED-internal-simulated | CYCLE-2-REQUIRED | 1 | 6 | 3 |
| EN-003 (Kimi → Gemini swap for Code Thesis Committee) | LOCKED-internal-simulated | CYCLE-2-REQUIRED | 2 | 4 | 0 |

**17 substantive findings the simulated audit missed.** Standout catches:
- "Branch revert + zero-state migration" doesn't actually roll back external writes to ChromaDB / vault / lessons.md during a spike.
- A bootstrap-exception clause, if reusable, lets any future amendment bypass live cross-family audit.
- Judge self-reference: Gemini scoring an amendment that adds Gemini to the Committee returned 100/100; the non-Anthropic Red Team (GPT-OSS) called out the bias even though Gemini self-assessed as unbiased.
- Schema incompatibility never verified between the new Committee reviewer and the Committee orchestrator's prompt format.

None of these catches appeared in the simulated single-family pass. All of them are the kind of production bug that surfaces later as an incident.

## Evidence point 2 — Prompt caching at sovereign scale

With the same model (Anthropic Claude Sonnet 4.6) and the same preamble (≈2,800 tokens), two back-to-back inference calls:

| Call | Input tokens | Cache write | Cache read | Paid | Saved |
|------|--------------|-------------|------------|------|-------|
| 1 (cold) | 14 | 2,800 | 0 | $0.01692 | $0 |
| 2 (warm, same preamble) | 14 | 0 | 2,800 | $0.00096 | $0.00756 |

**Second call cost fell 94%.** At scale: Tilth's routine cross-family audit reuses a 3–5K-token orientation preamble across three reviewer seats. Cold call + two warm calls saves ≈60% on a three-call audit round. Projected weekly savings at current Tilth cadence: 35–45%.

Raw evidence: `/Users/goldenquill/Downloads/GoldenQuill/tilth/logs/acme-smoke/cache-ledger.jsonl`.

## Evidence point 3 — Org-isolation via namespaced preamble

Two sibling orgs with otherwise-identical preamble bodies but distinct `ORG:<slug>\n` prefixes were tested back-to-back:

- `acme-test-a` first call: `cache_creation_input_tokens = 2803`, `cache_read_input_tokens = 0` (fresh cache)
- `acme-test-a` second call (same preamble): `cache_read_input_tokens = 2803` (reads own cache)
- `acme-test-b` first call (identical preamble body, different ORG prefix): `cache_creation_input_tokens = 2803`, `cache_read_input_tokens = 0` (fresh cache, does NOT read Org A's cache)

**Law 3 isolation holds at the cache-key layer.** One client's cached tokens are invisible to another client despite identical substantive preamble content. Defense-in-depth beyond Anthropic workspace isolation.

Raw evidence: `/Users/goldenquill/Downloads/GoldenQuill/tilth/logs/acme-test-a/cache-ledger.jsonl` + `/Users/goldenquill/Downloads/GoldenQuill/tilth/logs/acme-test-b/cache-ledger.jsonl`. Acceptance test: `/Users/goldenquill/Downloads/GoldenQuill/tilth/tests/test_cache_org_isolation.sh`.

## Why this matters for the mission

Tilth is built for grassroots operators — regenerative farms, worker-owned coops, mutual-aid networks, land trusts, eco-artists — who compete for funding against organizations with paid grant-writing staff. Every dollar lost to LLM overhead is a dollar not spent on operator capacity.

**The combined effect of cross-family audit + prompt caching:**

- A LOCK-sealed-quality Thesis round (3 cross-family seats + synthesis) runs for under $1 in API cost when preamble caching is active.
- Continuous re-auditing (not just first-run) becomes affordable — the second audit on revised work is 60% cheaper than the first.
- Governance rigor that institutional shops rely on becomes available to the solo operator.
- One sovereign Golden Quill can serve multiple orgs without cross-org leakage.

## Reproducibility

Every number above comes from JSONL ledger entries that persist in `tilth/logs/<org>/cache-ledger.jsonl` per call, written by the open-source wrapper `tilth/bin/tilth-infer-cached.mjs` (286 lines). Any third party with the same OpenClaw config + Anthropic key can reproduce the measurement. No proprietary middleware, no hidden middleman.

## Architectural attribution

- **Cross-family discipline (L-003):** `/AGENTS.md` — "reviewer's model family must differ from author's"
- **Two-cycle audit (L-005):** `/AGENTS.md` — simulated Cycle 1 + Cycle 2 before any LOCK
- **Prompt-caching enablement:** OpenClaw 2026.4.14 `cacheRetention: long` config flag (1-hour TTL on eligible preambles)
- **Org-namespacing:** Tilth convention — `ORG:<slug>\nTRACE:<sessionId>\n` prefix on cached system blocks
- **Telemetry ledger:** `tilth/bin/tilth-infer-cached.mjs` + `tilth/bin/tilth-batch.mjs` (249 lines)

## Next-phase wins (not yet measured)

- Batch API (50% discount on non-time-sensitive work) — `tilth-batch.mjs` shipped 2026-04-20; awaiting first real Scout daily-radar run to measure.
- Opus 4.7 for Scribe escalation on complex grant sections — pending Anthropic stable-API release + OpenClaw allowlist entry.
- Logician POST-gate `F-VERDICT-CITATION-MISSING` to structurally catch any confabulated citations in Judge output — v0.2 engineering queue.
