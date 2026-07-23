---
tags: [inventory, arcanum-runtime, observability, validation-harness, public-private-boundary, capability, synthesis, audit]
node_type: findings
is_session: false
layer: workflow
nature: reference
status: verified
created: 2026-07-22
sources: [arcanum/spells/sigil-maintenance-loop/README.md, arcanum/spells/sigil-maintenance-loop/development/VALIDATION.md, arcanum/registry/SPELLS.md, implementation/domainspec/internal_tools/subagents-dispatch-hooks/skills/domainspec-subagents-strategy/SKILL.md, .arcanum/observability/reflections/20260722T060751Z-domainspec-subagents-strategy-reflection.md]
---

# Sigil Maintenance Loop Inventory-First Hardening

- ID: `sigil-maintenance-loop-inventory-first-hardening`
- Type: synthesis
- Status: verified
- Confidence: high

## Validation Finding

The public `sigil-maintenance-loop` already existed in Arcanum, was registered,
and had generated runtime mirrors. It was not missing, so creating another spell
would have duplicated authority. The live artifact was an under-specified
scaffold against the current Spellcraft contract: it lacked optional sigils,
prerequisites, shared state, named handoffs, local customization, and an
experiment harness. This evidence does not establish how the original scaffold
was authored.

## Inventory-First Maintenance Contract

The hardened canonical spell now requires `inventory` in `lookup` mode as its
first phase. Every maintenance invocation:

1. derives lookup terms from the target sigil, current correction or observer
   signal, and affected contract area;
2. reads `index.json` first when present;
3. returns a named `inventory-lookup-packet` with matches, exclusions, source
   references, and gaps;
4. performs this read-only lookup without a separate permission prompt; and
5. never expands the automatic phase into Inventory installation or mutation.

Missing Inventory, a missing machine index, and no match remain explicit residue.
Inventory evidence is a non-authority input to reflection and cannot approve a
sigil mutation.

## Strategy Consumer Repair

The private `domainspec-subagents-strategy` owner previously sequenced
`workflow-reflect` and `sigil-development` directly. Its maintenance hook now
invokes canonical `sigil-maintenance-loop`, passes the correction envelope and
lookup terms, and preserves explicit approval before mutation. Its separate
Inventory Hook still records durable dispatch results; it is not conflated with
the maintenance preflight lookup.

## Inventory Exploration Evidence

The repository Inventory `index.json` parsed successfully and was searched
before source expansion. It contained no direct prior entry for
`sigil-maintenance-loop` or the strategy maintenance integration, so the lookup
returned a real no-match gap rather than an invented precedent.

## Validation

- Spellcraft contract completeness: pass.
- Required and optional sigil resolution: pass.
- File-backed runtime boundary scenarios: pass, 6/6.
- Native Spellcraft example bodies: pass, 4/4.
- Experiment profile and regimes: pass.
- Timestamped final harness report: pass.
- Codex and Claude generated mirror body parity: pass.
- Markdown links and diff checks: pass.
- Public/private boundary scan: pass.
- Signal Observer recorded the manual correction once; Workflow Reflect wrote a
  one-signal manual-trigger report recommending the targeted update.

## Dispatch Boundary

Principle-1 dispatch triggers were not met. The work ran inline with one
read-only observer helper, which the strategy classifies as a helper rather than
a dispatch. No check-tension gate, confirmation sheet, registration row, or
close row was created.

## Residue

- The generic experiment output checker extracts XML-style Quality Bar and
  Anti-Pattern sections only from `SKILL.md`; this README-based spell therefore
  reports aggregate `QUALITY_BAR_STATUS=not_checked`. Spellcraft review and the
  scenario runner provide the validation evidence instead.
- Publication remains separate: no commit or push was requested or performed.

## Next Action

Use `sigil-maintenance-loop` for future strategy corrections; it will explore
Inventory automatically before reflection. If these changes are published,
commit and push the public Arcanum submodule first, then update the private
parent pointer under normal submodule discipline.

Inventory remains a non-authority read model. This entry records a validated
maintenance result; it does not promote Inventory evidence or approve future
sigil mutations.
