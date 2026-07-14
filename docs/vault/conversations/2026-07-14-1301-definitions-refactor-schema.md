---
tags: [definitions-governance, cyberalchemy-v2, authority, schema, refactor]
node_type: discovery
is_session: true
layer: ontology
nature: [explanatory, technical]
status: active
created: 2026-07-14
timestamp: 2026-07-14T13:01:04-03:00
expires: 2026-09-12
conversation_id: 2026-07-14-definitions-refactor-schema
decisions_made: true
contradictions_found: true
specs_updated: [cyberAlchemy-v2/authority/definitions/definitions-refactor/DEFINITIONS-VICTOR.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "Turns the definitions refactor from a broad cleanup into a stricter proposal discipline: only repo-grounded, internally coherent terms survive, while schema is reintroduced from active CAV2-D56 with explicit unresolved enforcement questions."
---

# Definitions refactor criteria and Schema D56 correction

## Summary

The session set out to refactor the CyberAlchemy v2 definitions surface because the existing definitions material was judged over-formalized, inconsistent, and not useful enough for the repo. The owner set the operating criterion for the refactor: keep definitions only when they are internally consistent, complete enough to guide use, not formalized beyond what the repository can actually sustain, and anchored to things that already exist rather than to invented models. A subagent review strategy was discussed, including reviewer passes, robot-talks, and zig-zag review, but the practical focus stayed on `definitions-refactor/DEFINITIONS-VICTOR.md`. Several authority-field definitions in D34 were challenged; owner, scope, surface, and challenge_route were removed or treated as not ready because they were poorly defined. Open Questions were added as a discipline across definitions so each term records what still needs improvement either in the definition itself or in application and enforcement. The owner clarified that a formal Authority definition should not be expanded until its fields are grounded in existing artifacts and practices. Schema was reintroduced as `CAV2-D56` because it already exists in DomainSpec meta-types, edge signatures, dispatch and ledger records, frontmatter, and validator-facing schema practice. An incorrect generic schema definition was corrected: the proposal now imports the active D56 content using `schema S = (K, C, R, N)` while avoiding dependency on rejected public schema wording. The result is a refactor proposal file, not canonical promotion, with explicit open questions about schema enforcement, conformance, level, and actual consumers.

## Contradictions

- questions cyberAlchemy-v2/authority/definitions/DEFINITIONS.md - active `CAV2-D56` provides the imported schema formalism, but the refactor still questions whether all actual repository schemas instantiate `K`, `C`, `R`, and `N`, and whether "conformance by inspection alone" holds for documentary, review-enforced, or cross-file schemas.
- questions cyberAlchemy-v2/authority/definitions/definitions-refactor/DEFINITIONS-VICTOR.md - the Authority field set was partially drafted without enough grounded definitions for owner, scope, surface, and challenge_route; those terms were removed or left unasserted rather than promoted as usable vocabulary.

## Open questions

- What minimum evidence is required before a field inside Authority counts as a real definition rather than a placeholder?
- How formal should a definition be when the purpose is to create rules for existing repository practice rather than impose a new model?
- Which schema consumers should be sampled first to test whether the active D56 structure is too strong, too weak, or correctly scoped?

## Next steps

- Validate `CAV2-D56` against representative schema consumers: DomainSpec meta-types, edge signatures, dispatch records, ledger records, frontmatter, and validator inputs.
- Rebuild the Authority definition only after each proposed field has repo evidence, boundary conditions, and a clear enforcement or application route.
- Continue the definitions refactor by separating active imports, owner-gated candidates, and deferred terms without silently reusing rejected public wording.

## Recommendation

Attack the Authority field evidence before polishing prose. License: this session already showed that a plausible-looking field list collapses when owner, scope, surface, and challenge_route are asked to justify themselves against actual repo use; that failure is the useful signal, not a formatting defect.

## Files touched

- cyberAlchemy-v2/authority/definitions/definitions-refactor/DEFINITIONS-VICTOR.md
