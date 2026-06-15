# Deep-Spec Dispatch — UI Prototyping Studio

**Dispatch ID:** `ui-prototyping-studio-deep-spec-001`
**Status:** validated `pass` (`scripts/validate-dispatch.py`)
**Goal:** take the `ui-prototyping-studio` spec from *architecture-strong / evidence-sparse* to **one-shot implementation readiness**, with **human–agent ergonomics as the first principle**.

This is a *route artifact*, not an execution log. It tells `refine` (the orchestrator) how to chain capabilities, where the dialectic converges, what evidence each lane must return, and which gates protect the spec from being silently mutated.

## Why this route exists

A discovery pass found the spec is **governance-clear but execution-light**: fitness scoring (O-004), exploit-conformance metric, identity/DNA rejection lifecycle, accessibility interaction detail, and error/recovery flows are all underspecified, and there is **no user-validated UX evidence**. This route is built to attack exactly those gaps.

## The shape

```
                          s0  context-builder  (evidence baseline + ergonomics charter)
                                     │ frame.evidence-baseline
                                     ▼
                          s1  deep-research (FAN-OUT, parallel)
                              ├─ token-researcher → resonant-os-design-tokens philosophy
                              └─ web-tool-researcher → prototyping / token / UX tooling
                                     │ handle.token-philosophy
            ┌────────────────────────┴────────────────────────┐
   LANE A (antithesis)                                 LANE B (thesis)
   s2  refine · challenger        ──handle.antithesis──▶  s3  refine · defender
   novel + better implementations    (zig-zag critique)    defend + deepen current design
   in domainspec UI types                                  (D-001..D-009)
            └────────────────────────┬────────────────────────┘
                                     ▼  zig-zag dialectic
                          s4  refine · synthesis  → SYNTHESIZED-DEEP-DESIGN.md (frame.deep-design)
                                     │
        ┌───────────────┬───────────┴───────────┬────────────────────┐
        ▼               ▼                        ▼                    ▼
   s5 residuality   s6 ux-evidence          s7 playwright        s8 naive-user
   stressors /      validator-safe checks   PLANNED test suite   cold-start walkthrough
   invalidations    + fixture plan          (no execution)       (context-isolated agent)
        └───────────────┴───────────┬───────────┴────────────────────┘
                                     ▼
                          s9  refine · synthesis
                              → DEEP-SPEC-PROPOSAL.md + ONE-SHOT-IMPLEMENTATION-PLAN.md
                                     │ handoff.implementation-readiness
                                     ▼
                          s10 implementation-readiness → decision + next-route menu
```

## The two lanes (zig-zag dialectic)

- **Lane A — challenger / antithesis (`s2`, `refine`):** generates novel and better implementation directions and alternative paths, expressed in **domainspec UI types**, informed by the resonant-os-design-tokens research and a web-tooling survey. Ranks directions by **ergonomics gain vs cost** (pareto).
- **Lane B — defender / thesis (`s3`, `refine`):** restates and defends the load-bearing decisions `D-001..D-009`, names which Lane A proposals it can absorb vs must reject, and defends manual governance **as a feature, not friction**.
- **`s4` synthesis:** the zig-zag resolves — every contested point becomes a *decision*, a *logged residue*, or a *deferred option*. No endless alternation (stop conditions enforce this).

## The ergonomics-evidence floor

- **`s5` residuality-spec** — stresses the deepened design for invalidations; every significant stressor maps to a residue or an open question; attractors reported as clusters.
- **`s6` ux-evidence-validator** — translates ergonomics / WCAG 2.2 / design-system practice into **validator-safe checks** + a **fixture plan**; hard gates only for deterministic or standards-backed failures, everything else classified as soft-flag / screenshot-review / human-study.
- **`s7` Playwright (planned mode)** — designs the *whole* UI test suite without running it; each scenario names locator strategy, expected evidence (screenshot/trace/axe/measurement), and the failure interpretation.
- **`s8` naive-user agent** — a **context-isolated** agent that receives *only task goals and the rendered surface*, never the internal docs or rationale, so its friction is genuine. Boundary `b-naive-isolation` enforces this (`on_violation: block`).

## Gates (what protects the spec)

| Gate | Kind | Protects |
|------|------|----------|
| `g0-charter` | human_approval | ergonomics charter + role split approved before lanes run |
| `g1-research-boundary` | policy | web/github research stays labelled `external_context` |
| `g2-convergence` | quality | dialectic converges or logs residue with an owner |
| `g3-residuality` | validation | every stressor → residue or open question |
| `g4-ux-evidence` | validation | UX claims classified; hard gates only when deterministic |
| `g5-test-plan` | validation | Playwright plan is planned-only, with evidence + failure interpretation |
| `g6-naive-isolation` | policy | naive-user agent never saw internal rationale |
| `g7-promotion-guardrail` | promotion_guardrail | **no** SPEC/domain/glossary/inventory promotion; outputs are proposals |
| `g8-final-approval` | human_approval | proposal + plan approved before any spec mutation |

The promotion guardrail deliberately mirrors the studio's own ethos: **nothing becomes durable without explicit human approval.**

## Artifacts the run will produce

`CONTEXT-PACK.md` · `RESEARCH-EVIDENCE-CARDS.md` · `LANE-A-NOVEL-DESIGN.md` · `LANE-B-DEFENSE.md` · `SYNTHESIZED-DEEP-DESIGN.md` · `RESIDUALITY-STRESSORS.md` · `UX-EVIDENCE-REPORT.md` · `UX-FIXTURE-PLAN.md` · `PLAYWRIGHT-TEST-PLAN.md` · `COLD-START-USABILITY-FINDINGS.md` · `DEEP-SPEC-PROPOSAL.md` · `ONE-SHOT-IMPLEMENTATION-PLAN.md`

## Validate

```bash
python3 .claude/skills/dispatch-spec/scripts/validate-dispatch.py \
  projects/ui-prototyping-studio/development/deep-spec-dispatch/DEEP-SPEC-DISPATCH.json
# → VALIDATION=pass
```

## Subagent strategy

`status: required` · `parallelism: mixed` · `join_policy: parent_synthesis` · `authorization: approved` (operator approved in-session). 9 role-bound agents; the naive-user agent is context-isolated by contract.
