---
tags: [domainspec-v2, review, red-team, fidelity-review, admissibility-rule, edge-meta-type, relationships-yml, subagents-dispatch, anti-bias-check, claim-le-proof]
node_type: audit
is_session: true
layer: architecture
nature: technical, reference
status: active
created: 2026-07-07
timestamp: 2026-07-07T00:25:00-03:00
expires: 2026-09-05
conversation_id: 2026-07-07-dsv2-discovery-repo-fidelity-review
decisions_made: false
contradictions_found: true
specs_updated: [projects/domainspec-v2/discovery/review-2026-07-06/findings.md, telemetry/agents/subagents-dispatch.yaml]
promoted_candidates: []
expected_importance: 6
importance_rationale: "Surfaced 3 MAJOR fidelity defects that gate whether the upstream discovery doc can be trusted as the base for the future view triad; a verified review over an existing artifact, not a new mechanism."
---

# Repo-fidelity review of the domainspec-v2 discovery

## Summary

This session ran an adversarial red-team review of the domainspec-v2 discovery doc (authored the prior session) against a question the user sharpened twice: not completeness for hypothetical downstream views, but whether the doc is faithful to the rest of the repo. Routing went through `domainspec-subagents-strategy` to the `review` type skill, and the dispatch sheet evolved across two user corrections — dropping a "missing for downstream views" angle, then adding a fifth attacker for concept-omission after the user flagged that the edge/meta-type admissibility rule was absent. The check-tension anti-bias gate ran three times (once per sheet revision), PASS/PASS each; the final attacker group was five agents on the attack-vector axis (mechanics/correctness, abuse/gaming, reference/consistency, fidelity/governance, coverage/omission). The dispatch — 9 agents across 4 groups — ran attackers → robot-talks → synthesizer → two verifiers (zig-zag) → coverage auditor, and was registered and closed `resolved` in the telemetry ledger with findings banked. The two verifiers genuinely disagreed on scope (source-fidelity salvaged findings; overreach dropped most as §1-scoped-out), and I adjudicated with an explicit rule: an omission survives only if the omitted concept governs a plane the doc actively engages. The verdict was FIX — 3 MAJOR + 4 MINOR survived, 3 dropped, and no CRITICAL, because the admissibility non-collapse *math* is legitimately scoped out by §1 while only the rule *naming* is owed. The three MAJORs are: the admissibility rule is never named though the doc works the edge plane (plus a D16 modality error in step-3), the "11 UI types prose only / no registry row" clause is literally false against the active `relationships.yml`, and §6 omits the single open architectural decision `DEC-DSV2-LANE-ZA` while §4 conflates the two lanes. Every numeric, mechanical, and cited-governance claim was confirmed accurate, so the fidelity gap is concentrated in omitted authority naming and one over-strong body clause, not in miscounts. Three severity/scope calls were explicitly deferred to the owner rather than auto-resolved, and nothing in the discovery itself was edited — applying the fixes remains the next act.

## Contradictions

- questions `projects/domainspec-v2/discovery/domainspec-v2-discovery.md` — the edge/meta-type admissibility rule (`DEC-DSV2-EDGE-ADMISSIBILITY`, DS-D8/DS-D2) is worked but never named, and step-3's "checked against the legal signatures" contradicts D16 (a forbidden edge is unconstructible, not flagged). MAJOR, survived.
- questions `projects/domainspec-v2/discovery/domainspec-v2-discovery.md` against `projects/domainspec-v2/definitions/relationships/relationships.yml` — the "11 UI types exist as prose only / no registry row" clause is false; the UI types are registered as active typed edge endpoints. MAJOR, survived.
- questions `projects/domainspec-v2/discovery/domainspec-v2-discovery.md` §6/§4 — omits the single open architectural decision `DEC-DSV2-LANE-ZA` while §4 conflates the fuse (Lane Z) and generate (Lane A) lanes into one settled-looking loop. MAJOR, survived.
- validates `projects/domainspec-v2/discovery/domainspec-v2-discovery.md` — all numeric/mechanical counts (14 backend meta-types, 31 signatures, 7 EdgeTypes, RANGE→4/COUNT_CAP→2) and cited governance (triad, promotion gates, νF honesty, Saturn non-collapse) confirmed accurate.

## Open questions

- Should the adjudication rule that broke the verifier deadlock — "a doc's omission of X is a defect only if X governs a plane the doc actively engages; otherwise it is a respected scope boundary" — be lifted into the `review` skill as a standing scope heuristic, or does it stay a per-dispatch call? Untested beyond this one dispatch.

## Next steps

- Resolve the three deferred owner calls (#2 UI clause MAJOR-vs-MINOR; #3 whether the §4 "hypothesis under test" hedge makes the lane-conflation a mere rider; #1 that only the admissibility rule *naming*, not the D18/D20-D25 math, is owed), then apply the 3 MAJOR + 4 MINOR change-requests in `projects/domainspec-v2/discovery/review-2026-07-06/findings.md` to the discovery.
- Reconcile the standing close-session skill/repo mismatch (`.claude/skills/close-session` targets a non-existent `docs/vault/`; the umbrella uses `sessions/`) — carried unfixed from 2026-07-03-2010, 2026-07-03-2014, and 2026-07-06-2104.

## Recommendation

- The keystone is applying the three surviving MAJORs, starting with the admissibility-rule edge — the user's own flag. It is licensed by that finding surviving above as a MAJOR `questions` edge while every numeric and cited-governance claim `validates` as accurate — so the fix is a targeted naming addition, not a rewrite — and by the review closing `resolved`. The three deferred calls should not block starting: each only shapes a fix — which clause's severity, how much of the rule to name — not whether to fix.

## Files touched

- projects/domainspec-v2/discovery/review-2026-07-06/findings.md
- telemetry/agents/subagents-dispatch.yaml
