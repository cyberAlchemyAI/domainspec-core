---
tags: [inventory, strategy-result, dispatch, subagents, research, v2-repo, domainspec, operational-evidence, claim-le-proof, non-collapse]
node_type: synthesis
is_session: false
layer: strategy
nature: synthesis
status: flag
created: 2026-07-15
dispatch_id: 2026-07-15-fpr01-04-cost-estimate
dispatch_type: research
working_folder: projects/domainspec-v2/research/2026-07-15-fpr01-04-cost-estimate/
sources: [projects/domainspec-v2/research/2026-07-15-fpr01-04-cost-estimate/research.md, projects/domainspec-v2/research/2026-07-15-fpr01-04-cost-estimate/findings.md, telemetry/agents/subagents-dispatch.yaml, projects/domainspec-v2/development/first-production-release/ROADMAP.md]
---

# DomainSpec v2 FPR-01 Through FPR-04 Cost Estimate Strategy Result

This is a non-authority Inventory read model of the resolved research dispatch
`2026-07-15-fpr01-04-cost-estimate`. It makes the accepted estimate searchable
without turning modeled effort into measured duration, converting candidate
work into FPR authority, selecting an implementation posture, closing an FPR
gate, or approving a budget baseline.

## P1 Trigger Decision

Dispatch was required by all four P1 triggers. The question required synthesis
across the live FPR task graph, completed Task Session receipts, validation and
compute burden, owner latency, learning-map implementation, and candidate
rebind risk. Separate explorers were also required to protect the parent
context, isolate bottom-up, empirical, and adversarial estimates, and permit
independent challenge of arithmetic and definitions.

## Lanes And Subagents

- Abramsky produced the bottom-up FPR and learning-map work breakdown, unit
  definitions, validation census, and route arithmetic.
- Kahneman calibrated the forecast against available Task Session evidence and
  identified the limits of the sparse reference class.
- Baez modeled serial owner latency, rework, expiry, and candidate-to-authority
  migration tails.
- Noether synthesized the three estimates without collapsing their units.
- Russell ran the non-vacuity and arithmetic gate and returned a conditional
  pass after corrections.
- Turing wrote the durable findings artifact.
- Brandenburg independently audited the findings, requested one bounded
  repair, and returned `ACCEPT` after the repair.
- Popper's planned definitional-soundness review did not launch because the
  runtime thread ceiling had been reached. That gate is `NOT REVIEWED`, not a
  pass.

The executed research role count was seven: three explorers, one synthesizer,
one skeptic, one writer, and one auditor. The pre-dispatch double-PASS tension
check was infrastructure and is not counted as a research role.

## Dependency Flow And Gate State

The intended route was
`explorers -> synthesizer <-> reviewers -> writer -> auditor`. One bounded
synthesis/review loop ran. Russell's conditional result reached the writer;
Popper's missing result remained explicit residue. The auditor then returned
`REVISE` once for a calendar arithmetic error, sunk-work boundary, and route
verdict matrix. The corrected findings passed the final audit.

- P1 gate: dispatch required.
- Check-tension: two independent gate agents returned `PASS` on the revised
  dispatch sheet.
- Human gate: explicitly confirmed before registration.
- Ledger: one dispatch row and one close row were appended through the
  deterministic register-dispatch appender.
- Closeout: `exit_reason: resolved`; `loops_used: 1`; final approver
  Brandenburg returned `ACCEPT`.
- Review completeness: partial because the definitional-soundness reviewer did
  not run.

## Accepted Cost Model

The remaining path contains 13 receipt-serial SWUs. The completed
`SWU-FPR01-001` census is sunk and excluded from every band.

| Scope | Modeled engineering PD low / base / high | Modeled owner-review hours low / base / high |
|---|---:|---:|
| FPR-01 | 4.5 / 8 / 14 | 8 / 20 / 38 |
| FPR-02 | 5.5 / 10 / 18 | 4 / 8 / 16 |
| FPR-03 | 7 / 13 / 24 | 8 / 16 / 30 |
| FPR-04 | 9.5 / 17 / 30 | 4 / 8 / 16 |
| Total | **26.5 / 48 / 86** | **24 / 52 / 100** |

The separate modeled calendar envelope is **10-16 / 20-32 / 41-68 weeks**.
It includes serial authority waits and is not derived from person-days.

## Non-Collapsed Planning Views

The accepted findings preserve six different planning views:

1. engineering person-days for focused implementation resource;
2. narrowly defined owner-review hours;
3. Task Session equivalents for receipt and rework pressure;
4. E3 aggregate accountable-owner, implementer, reviewer, and verifier hours;
5. elapsed calendar time including waits; and
6. automated CPU-hours.

They overlap or answer different questions and must not be summed or converted
without a separately selected cost/capacity model. The 43 unique negative
controls imply at least 53 negative executions because the 10 FPR-02 controls
run twice. The roughly 70 total acceptance executions remain an approximate,
unverified bridge. FPR-01 through FPR-04 compute is assumption-only at 1-4
accepted CPU-hours and 8-30 iterative CPU-hours.

## Route Comparison

| Route | Modeled engineering PD low / base / high | Modeled owner-review hours low / base / high | Posture |
|---|---:|---:|---|
| Assurance-first plus learning map | 46 / 84 / 150 | 36 / 76 / 148 | Provisional |
| Candidate-first plus later rebind | 50 / 94 / 174 | 40 / 84 / 164 | Provisional |
| Candidate-first incremental tax | +4 / +10 / +24 | +4 / +8 / +16 | Modeled rebind risk |

Candidate-first is not the cheaper route. It can shorten time to interactive
evidence only when a genuinely separate engineering lane exists, and it closes
no FPR gate. Russell conditionally passed the finite arithmetic witness for
both routes. Popper did not review their definitional soundness. Both verdicts
therefore remain `PROVISIONAL`, not approved budget baselines.

## Validation And Claim Boundary

- Three explorer returns are preserved verbatim in `research.md`.
- `findings.md` contains exactly one reciprocal connection and one final Open
  Questions section.
- The corrected high-tail serial calendar is 41-68 weeks; the original 45-68
  explorer value remains only in the immutable verbatim transcript.
- The completed census exclusion, route verdict matrix, partial reviewer
  disclosure, and provisional posture are explicit.
- Markdown structure, trailing whitespace, and `git diff --check` passed.
- The final auditor returned `ACCEPT` after one bounded revision.

Acceptance applies to the bounded research artifact. It does not establish a
budget, SLA, release date, route decision, engineering allocation, owner
commitment, or production readiness claim.

## Workflow Residue

The runtime thread ceiling prevented Popper from launching. Idle pre-dispatch
gate threads were later reused for writer and auditor roles; those gate roles
remained outside the research role count. The final writer and auditor work was
separate, and the missing definitional gate was disclosed rather than inferred.

This leaves one blocker only for promoting the forecast into an approved
budget baseline: rerun an independent definitional-soundness review over the
unit separations and route language. It does not invalidate use of the current
bands as explicitly provisional planning evidence.

## Next Human Action

Use the assurance-first base case of 84 engineering PD, 76 owner-review hours,
and a separate 20-32 week calendar envelope only as the current provisional
planning case. Before making it a budget baseline or external commitment,
rerun Popper's definitional-soundness review. As each remaining SWU closes,
record focused engineering time, narrow owner-review time, owner wait, retries,
execution count, and CPU separately, then recalibrate after FPR-01.

The candidate-first posture remains a later project decision. This dispatch
does not resolve `D-IOLM-POSTURE` or authorize the learning-map implementation
to substitute candidate graph output for DomainSpec FPR authority.

## Connections

- derives-from -> `projects/domainspec-v2/research/2026-07-15-fpr01-04-cost-estimate/research.md`
- summarizes -> `projects/domainspec-v2/research/2026-07-15-fpr01-04-cost-estimate/findings.md`
- evidenced-by -> `telemetry/agents/subagents-dispatch.yaml`
