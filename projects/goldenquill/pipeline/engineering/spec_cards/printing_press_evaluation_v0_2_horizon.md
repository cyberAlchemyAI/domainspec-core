# Spec card — Printing Press evaluation (Funder Intel DB connector generation)

**STATUS:** PRE-STAGED 2026-05-15 — operator-approved 1-2 hour evaluation task; v0.2 horizon (WS-D / WS-E acceleration candidate).

**Decision class:** Tooling evaluation. NOT a build commitment. Outcome of this card is a yes/no on whether Printing Press accelerates Funder Intel DB connector generation enough to adopt it as v0.2 tooling.

---

## What Printing Press claims

Printing Press (surfaced via The Neuron 2026-05-15) is a tool that turns an API spec, website, or community project into:

- A Go CLI
- A Claude Code skill
- An OpenClaw skill
- An MCP server

The pitch: generated connectors save the hand-coding cost of writing portal scrapers / API clients / RSS parsers from scratch.

## Why we care

Tilth's Scout pipeline (blueprint v0.1 §3 Section 03) routes through six channel families (A federal APIs / B curated caches / C state portals / D federal program pages / E RSS / F websearch). Channels C, D, and E are the channels where connector generation cost is highest because each state portal / federal program page / RSS feed needs its own adapter logic. v0.2 WS-D / WS-E expand this coverage substantially.

If Printing Press generates working scrape-or-API connectors faster than hand-writing them, it accelerates v0.2 portal seeding. If it generates connectors that need significant manual cleanup, it costs more than hand-writing them. Evaluation is needed to decide.

## Target portals for the evaluation

Four portals chosen to span the cost spectrum:

1. **PA DCED** (Pennsylvania Department of Community and Economic Development) — state portal; Channel C seeded target; known structure; medium scrape complexity.
2. **PA Ag** (Pennsylvania Department of Agriculture) — state portal; Channel C seeded target; lighter structure than DCED; smaller endpoint surface.
3. **Foundant** (foundation portal platform, used by many PA / NY / NJ community foundations) — vendor portal; same shape across many foundations; high-leverage if it works.
4. **Submittable** (foundation portal platform, similar shape) — vendor portal; complementary to Foundant; tests whether the tool generalizes across vendor platforms with similar shapes.

The four portals stress different generation paths:
- PA DCED + PA Ag stress raw-website / HTML-scrape generation (no public API spec).
- Foundant + Submittable stress vendor-portal generation where the vendor may or may not publish a usable API spec.

## Evaluation protocol (1–2 hours)

1. **Setup (15 min)** — install Printing Press locally on dev node. Verify `--help` and a smoke "hello world" generation on a trivial input (e.g., a public REST API like JSONPlaceholder).
2. **Generation pass 1 — PA DCED (20 min)** — point Printing Press at the PA DCED grants page (URL or sitemap). Capture the output (connector module + any companion files). Measure: did it produce something parseable? Did it identify the right endpoints? Did it carry over the right fields?
3. **Generation pass 2 — Foundant (20 min)** — same, against a Foundant-hosted foundation portal of choice (Pittsburgh Foundation or Heinz Endowments are candidates).
4. **Cleanup-cost pass (20–30 min)** — pick the better of the two outputs and walk through what manual edits would be needed before the connector could plug into Scout's Channel C / D dispatcher. Don't actually do the cleanup; estimate the cost.
5. **Verdict (10 min)** — write findings in `pipeline/validation/printing_press_eval_2026-MM-DD/01_verdict.md`. The verdict is one of three outcomes:
   - **ADOPT** — generated connectors require less manual cleanup than hand-writing from scratch. Recommend integrating Printing Press into v0.2 WS-D / WS-E workflow.
   - **REJECT** — generated connectors require equal or more cleanup. Hand-writing stays the canonical path.
   - **DEFER** — outcome is ambiguous; recommend re-testing after Printing Press releases a major version, or against different target portals.

## Decision criterion

If Printing Press meaningfully reduces connector-generation time (e.g., 60-min hand-write → 20-min generate + 10-min cleanup), ADOPT. If it requires more cleanup than the saved generation time, REJECT.

The bar is real time savings on real Scout target portals, not "the tool works on demo inputs."

## Cost of the evaluation

1–2 hours of Josh's time at dev-node, or delegate to a Cowork / Claude Code session with operator review of the verdict packet at the end.

No infrastructure cost beyond Printing Press install (likely free per The Neuron snippet — "free to try" was the marketing copy for similar tools in the same Treats to Try list).

## What this card does NOT commit to

- Building any Printing Press integration.
- Replacing any Scout channel adapter.
- Locking the WS-D / WS-E roadmap around Printing Press output.

This card commits to an evaluation. The verdict packet drives the next decision.

## Source

External signal: Printing Press surfaced via The Neuron daily newsletter 2026-05-15 "Treats to Try" section. Pre-staged as eval candidate the same day per operator approval (Josh, 2026-05-15).
