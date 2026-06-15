# Arcanum Sigil: ux evidence validator

<!-- arcanum:capability-id ux-evidence-validator -->
<!-- arcanum:capability-kind sigil -->
<!-- arcanum:capability-tier arcana -->
<!-- arcanum:command ux-evidence-validator -->

<!-- arcanum:runtime codex -->

## Observer Envelope: Task Zero

Before doing domain work, establish the observer envelope for this Arcanum invocation.

- `run_id`: use an existing hook-provided run id when present; otherwise use `arcanum-ux-evidence-validator-<UTC timestamp>`.
- `capability.id`: `ux-evidence-validator`
- `capability.kind`: `sigil`
- `capability.tier`: `arcana`
- `capability.mode`: `command`
- `target_artifact`: this command file
- request summary: summarize the user request before execution.
- expected outputs: list intended artifacts before execution when known.

Closeout is mandatory but must not hide the primary result. At the end, report:

- `OBSERVATION`
- `LEDGER`
- `REFLECTION_TRIGGER`
- `RECOMMENDATION`
- `DEDUPE_KEY`

If deterministic hook or wrapper telemetry is unavailable, preserve the result and report the observability gap.


## Objective

Run the installed Arcanum sigil `ux-evidence-validator` using the canonical definition snapshot embedded below.

## Process

1. Use the embedded canonical README and SKILL snapshots as the execution contract.
2. Execute only this installed sigil unless the definition explicitly delegates or the user asks to route elsewhere.
3. Preserve the selected sigil's process, quality bar, anti-patterns, output contract, validation gates, gaps, and next route.
4. Return artifact used, command used, validation result, observability result, and next action.

## Guardrails

- Keep this command focused on `ux-evidence-validator`.
- Do not silently add, remove, or refresh capabilities.
- Do not treat generated observer telemetry as a substitute for the primary result.

## Canonical README Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/ux-evidence-validator/README.md

````markdown
# UX Evidence Validator

`ux-evidence-validator` is an Arcana sigil seed for turning UX research, accessibility standards, market-tested practice, and browser automation into a Playwright-backed evidence system for finished frontend interfaces.

It is meant for the awkward but important middle ground between "the UI works in the browser" and "the UI is good." The sigil keeps those claims separate: deterministic browser failures can become hard gates, while cognitive, perception, market, and subjective UX claims remain soft flags, screenshot review, human-study prompts, or residue until calibrated.

## Status

Status: seed.

This package defines the research basis, evidence-card model, validator taxonomy, fixture plan, and lifecycle direction. It is not promoted and does not yet include executable Playwright validator code or calibrated fixture evidence.

## Problem It Solves

Frontend review often mixes several kinds of truth:

- accessibility standards,
- browser-observed behavior,
- responsive layout integrity,
- cognitive and perception risk,
- market and design-system heuristics,
- subjective user evidence.

When these are collapsed into one "UX score," the result becomes untrustworthy. `ux-evidence-validator` instead creates a layered evidence contract so a finished interface can produce reviewable artifacts: screenshots, traces, ARIA snapshots, accessibility output, DOM measurements, finding JSON, and a residue ledger.

## Use When

- a frontend interface needs browser-level evidence before being treated as finished,
- UX guidance needs to be translated into validator-safe claims,
- Playwright should capture screenshots, traces, accessibility output, ARIA snapshots, and measurements,
- cognitive science, neuroscience, and market practice should inform checks without being overclaimed,
- a team needs known-good and known-bad fixtures before promoting hard gates,
- an interface review needs a residue ledger for claims that require human judgment or user research.

## Do Not Use When

- the user only wants a quick visual opinion,
- a full usability study is required and no browser evidence is needed,
- the project has no runnable frontend or inspectable interface,
- the request is only accessibility compliance auditing without UX evidence synthesis,
- a subjective product-quality decision is being forced into deterministic automation.

## Evidence Model

| Layer | Purpose | Default Status |
| --- | --- | --- |
| L0 Smoke | Page load, assets, console/network, trace availability. | Hard gate after calibration. |
| L1 Accessibility | axe output, ARIA snapshots, role/name/state, keyboard flow, forms. | Hard gate plus manual review. |
| L2 Layout Integrity | Overflow, clipping, overlap, target size, responsive screenshots. | Hard gate after calibration. |
| L3 Interaction Flow | User-facing locators, task completion, visible state changes. | Hard gate after calibration. |
| L4 Cognitive and Attention Risk | Density, memory burden, salience, visual hierarchy, change visibility. | Soft flag or screenshot review. |
| L5 Domain Practice | Ecommerce, service, dashboard, design-system, or platform rule packs. | Domain-specific soft flag unless deterministic. |
| L6 Human Evidence | Workload, comprehension, trust, confidence, real task success. | Human-study or review residue. |

## Development Artifacts

| Artifact | Purpose |
| --- | --- |
| [UX-PLAYWRIGHT-EVIDENCE-RESEARCH-STRATEGY.md](development/UX-PLAYWRIGHT-EVIDENCE-RESEARCH-STRATEGY.md) | Original research route and source lanes. |
| [ux-playwright-evidence-research.dispatch.json](development/ux-playwright-evidence-research.dispatch.json) | Dispatch route that shaped the research pass. |
| [UX-EVIDENCE-REFERENCE-CARDS.yml](development/UX-EVIDENCE-REFERENCE-CARDS.yml) | Normalized source cards and automation candidates. |
| [UX-EVIDENCE-CLAIM-MAP.md](development/UX-EVIDENCE-CLAIM-MAP.md) | Claim classes and proxy limits. |
| [UX-PLAYWRIGHT-VALIDATOR-SPEC.md](development/UX-PLAYWRIGHT-VALIDATOR-SPEC.md) | Future validator/tester contract and evidence output model. |
| [UX-PLAYWRIGHT-FIXTURE-PLAN.md](development/UX-PLAYWRIGHT-FIXTURE-PLAN.md) | Known-good, known-bad, domain, and false-positive fixture plan. |
| [WORK-PACK.md](development/WORK-PACK.md) | Development route from seed package to fixture-calibrated validator. |

## Ownership Model

| Capability | Owner |
| --- | --- |
| Source claim normalization | UX Evidence Validator |
| Browser execution mechanics | Experiment Harness and future Playwright implementation |
| Bounded implementation tasks | Task Session |
| Fixture calibration | UX Evidence Validator plus Experiment Harness |
| Promotion readiness | Sigil Development |
| External source freshness | Future research refresh task-session |

## Promotion Boundary

Promotion requires:

- fixture corpus implemented,
- known-good and known-bad fixture runs,
- Playwright evidence written to the declared output root,
- hard gates catching deterministic failures,
- soft flags remaining explainable and source-card-linked,
- at least one false-positive trap proving density and salience checks do not block expert tools by default,
- Sigil Development review of experiment reports and observability signals.

Until then, this sigil remains a seed in development.

````

## Canonical SKILL Snapshot

Canonical source: https://github.com/cyberAlchemyAI/arcanum/blob/main/arcana/ux-evidence-validator/SKILL.md

````markdown
---
name: ux-evidence-validator
description: "Use when: translating UX research, accessibility standards, market practice, and Playwright browser evidence into validator-safe checks, fixture plans, or evidence reports for finished frontend interfaces."
argument-hint: "<target-url-or-artifact> [--mode research|spec|fixture-plan|calibrate|validate-interface|report] [--scenario <path>] [--output <path>]"
tier: arcana
domain: frontend-ux-evidence
version: 0.1.0-seed
origin: created from the UX Playwright evidence research task-session on 2026-06-01
allowed-tools: Read, Write, Glob, Grep, Bash, Task
---

# Sigil: UX Evidence Validator

<objective>
Turn UX evidence into a layered, Playwright-ready validation contract that proves browser-observed frontend behavior while preserving cognitive, perception, market, and subjective claims as calibrated flags or human-review residues.
</objective>

<logic-type>
Arcana: evidence-governed frontend validation and promotion boundary management.
</logic-type>

<status>
Seed. The research artifacts and validator contract exist, but executable Playwright harness code and calibrated fixture evidence are not yet implemented.
</status>

<modes>
| Mode | Use When | Output |
| --- | --- | --- |
| `research` | Source references or UX claims need normalization before validator design. | Evidence cards and claim map. |
| `spec` | A project needs a Playwright evidence contract before implementation. | Validator spec and scenario shape. |
| `fixture-plan` | The validator needs known-good, known-bad, and false-positive fixtures. | Fixture corpus plan. |
| `calibrate` | Fixture pages and harness exist and need rule calibration. | Calibration report and threshold recommendations. |
| `validate-interface` | A runnable frontend should be tested once the harness exists. | Evidence report under `output/playwright/ux-validator/<run-id>/`. |
| `report` | Existing evidence should be summarized for review or promotion. | Findings summary and residue ledger. |
</modes>

<applicability>
Use this sigil when:

- a finished frontend needs browser evidence rather than prose-only review,
- UX references need to become validator-safe claims,
- accessibility, cognitive science, perception research, market heuristics, and Playwright evidence must be kept in separate authority lanes,
- hard gates need fixture calibration before promotion,
- screenshot review and human-study residues must be explicit,
- a future implementation should produce screenshots, traces, ARIA snapshots, accessibility output, DOM measurements, findings JSON, and a residue ledger.
</applicability>

<non-applicability>
Do not use this sigil when:

- the user only wants a quick subjective design critique,
- no frontend route, HTML artifact, screenshot, or scenario exists to inspect,
- the task is pure WCAG auditing with no UX evidence synthesis,
- a human usability study is required but browser evidence is irrelevant,
- the request would collapse subjective quality into a deterministic score.
</non-applicability>

<inputs>
Expected inputs, if available:

- target URL, local route, HTML artifact, or interface screenshot set,
- scenario file or user-task description,
- viewport and browser matrix,
- product domain tags such as dashboard, ecommerce, authoring, service, marketing, game, or data tool,
- source-card set or research artifact path,
- fixture corpus path when calibrating,
- desired output root, defaulting to `output/playwright/ux-validator/<run-id>/`.
</inputs>

<process>
1. Resolve mode. If no mode is provided, infer the smallest mode that fits the request and state the inference.
2. Identify the evidence boundary: source-backed standards, browser-observable behavior, proxy claims, domain heuristics, and subjective/human-study claims.
3. Load or create evidence cards before creating rule candidates.
4. Map claims into `hard_gate`, `soft_flag`, `screenshot_review`, `human_study`, or `not_automatable`.
5. Refuse to promote cognitive, neuroscience, or market claims directly into hard gates without a conservative UI proxy and fixture evidence.
6. For `spec`, produce or update the L0-L6 validator contract and scenario shape.
7. For `fixture-plan`, define known-good, known-bad, domain, and false-positive fixtures before implementation.
8. For `calibrate`, run the harness against fixtures, compare expected vs observed findings, and tune thresholds only with source-card evidence.
9. For `validate-interface`, drive Playwright with user-facing locators where possible and collect the required evidence outputs.
10. For `report`, summarize findings with source cards, evidence paths, proxy limits, status, and residue.
11. Preserve residues for subjective workload, comprehension, trust, confidence, delight, and real-user task success.
12. Return the output contract and the next lifecycle step.
</process>

<evidence-output-contract>
Browser evidence runs should write under:

```text
output/playwright/ux-validator/<run-id>/
```

Required outputs:

- `run-metadata.json`,
- `summary.md`,
- `findings.json`,
- `console-network.json`,
- `accessibility/*.json`,
- `aria/*.yml`,
- `screenshots/*.png`,
- `measurements/*.json`,
- `traces/*.zip` when interaction evidence is required,
- `residue-ledger.yml`.
</evidence-output-contract>

<quality-bar>
A successful run must:

- keep deterministic browser failures separate from UX risk proxies,
- cite source cards for every non-trivial UX claim,
- name what Playwright observed and what it cannot prove,
- use hard gates only for deterministic or standards-backed failures,
- require fixture calibration before promoting reusable hard gates,
- capture screenshots, traces, accessibility output, ARIA snapshots, DOM measurements, console/network summaries, and residues when running browser validation,
- keep domain-specific market rules behind explicit domain tags,
- report human-study claims instead of pretending automation can measure them,
- preserve development status when fixture or implementation evidence is missing.
</quality-bar>

<anti-patterns>
Avoid:

- producing a single universal UX score,
- claiming automated accessibility scans prove complete accessibility,
- converting neuroscience or cognitive science references into deterministic browser truth,
- treating market heuristics as universal rules outside their domain,
- blocking dense expert interfaces without false-positive calibration,
- accepting screenshot diffs without stable fonts, data, motion, and viewport controls,
- treating a good spec as implementation or promotion evidence.
</anti-patterns>

<observability>
For meaningful executions, record:

- mode,
- target URL or artifact type,
- scenario count,
- generated output count,
- validator layer coverage L0-L6,
- hard gate count,
- soft flag count,
- screenshot review count,
- human-study residue count,
- source-card coverage,
- fixture calibration status,
- quality bar status,
- anti-pattern hits,
- reflection trigger recommendation.
</observability>

<promotion-gate>
Promotion requires:

- implemented fixture corpus,
- at least one known-good fixture,
- accessibility, keyboard, layout, interaction, cognitive-risk, domain, and false-positive fixtures,
- Playwright evidence reports for fixture runs,
- hard gates catching expected deterministic failures,
- L4/L5 claims remaining explainable and non-blocking unless independently justified,
- Experiment Harness report,
- Sigil Development review.
</promotion-gate>

<output-contract>
Return:

```markdown
## UX Evidence Validator Result

- Status: pass | flag | block | seed-only
- Mode: research | spec | fixture-plan | calibrate | validate-interface | report
- Target: <url, artifact, scenario, or research path>
- Evidence cards: <path or status>
- Claim classes: <hard gates, soft flags, screenshot review, human study, not automatable>
- Browser evidence: <output root or not run>
- Fixture calibration: pass | flag | block | not run
- Findings: <summary or path>
- Residue: <human-review or user-study claims>
- Validation: <checks performed>
- Next lifecycle step: <step>
```
</output-contract>

````
