---
tags: [definitions, cyberalchemy-v2, canonical-artifact, axiom, invariant, premise, durability, canonical-kinds, enforcement]
node_type: conceptual
is_session: true
layer: ontology
nature: explanatory, technical
status: active
created: 2026-07-08
timestamp: 2026-07-08T15:20:22-03:00
expires: 2026-09-06
conversation_id: 2026-07-08-cav2-axiom-invariant-premise
decisions_made: true
contradictions_found: true
specs_updated: [cyberAlchemy-v2/authority/definitions/DEFINITIONS.md, cyberAlchemy-v2/authority/definitions/DEFINITIONS-INDEX.md, cyberAlchemy-v2/authority/definitions/DEFINITION-SCHEMAS.md, cyberAlchemy-v2/authority/definitions/DEFINITION-DRIFT-AUDIT.md, cyberAlchemy-v2/ontology/CANONICAL-KINDS.md]
promoted_candidates: []
expected_importance: 8
importance_rationale: "Promoted five canonical CAV2 definitions (D51–D55) that fix the artifact-typing and foundational-vocabulary layer of the authority spine — the axiom/invariant/constitution/premise ladder — grounded in and tested against two real axiom corpora."
---

# CAV2 canonical artifact + the axiom / invariant / premise ladder

## Summary

This session began as a definitions-governance check — does cyberAlchemy-v2 define "canonical artifact"? (it did not) — and grew into a full build of the artifact-typing and foundational-vocabulary layer of the CAV2 authority spine. Through discussion it established that a *canonical artifact* is typed-and-process-born and **decoupled from authority**, promoting `CAV2-D51` (canonical artifact) and `CAV2-D52` (artifact durability: `ephemeral | perennial`, carrying a contradiction-tolerance coupling), plus a candidate Tier-1 `CANONICAL-KINDS.md` registry that rolls fine kinds up to the `CAV2-D49` authority kinds. It then worked out the ladder **axiom → invariant → constitution → validator**, using the **subject-test** (world vs system) as the discriminator, and stress-tested it against two real corpora: ZefraHub and maestro-trama axioms. The evidence showed many "axioms" there are actually **invariants** (must-hold, prescriptive), the maestro creative axioms are genuine **descriptive** world-truths, and hedged entries (`AX-SYS-3` "hypothesis", `AX-ONT-7` "conjecture", `veracidade: low`) are really **premises**. On that basis it promoted `CAV2-D53` (axiom = foundational world-truth held true, with fan-out), `CAV2-D54` (invariant = system must-hold, the generic parent of D16/D29/D38/D49), and `CAV2-D55` (premise = a `veracidade`-low/`convicção`-high bet, evidence-gated to become an axiom). Once D53 established that an axiom is *not* a definition, it corrected the now-stale `CANONICAL-KINDS` axiom row (rollup marked `unresolved`/`deferred` pending AUTHORITY-MODEL OQ-2). A parallel thread audited how a constitution is actually enforced: the model exists (constitution-governance's validation-mode taxonomy — `deterministic`/`review`/`hybrid`/`none-yet` — and context-injection is explicitly *not* enforcement), but CAV2 is **review-first today**, with one form-only advisory validator and no act-time/agent gate wired. All promotions were synced across the index, the schema registry (`CAV2-D51-SCHEMA`), and recorded in the drift audit, including the "canonical artifact" prose-divergence flag and the not-reversed `ledger` hold. Nothing was committed.

## Contradictions

- validates `cyberAlchemy-v2/authority/definitions/reviews/constitution-invariant-axiom-role-review.md` — its provisional invariant/axiom/constitution role split was promoted (and sharpened with the subject-test + corpus evidence) into `CAV2-D53`/`D54`.
- questions `cyberAlchemy-v2/development/reviews/2026-06-21-authority-elevation-protocol-review/attacks.md` — its prose uses "canonical artifact" in the *authoritative-version* sense, opposite to the promoted `CAV2-D51` decoupled-from-authority sense; recorded in the drift audit, historical prose left unrewritten (ephemeral artifact).

## Next steps

- Route AUTHORITY-MODEL **OQ-2** (should `invariant`/`axiom` be first-class authority kinds?) through `decision-gate`; then set the `CANONICAL-KINDS.md` `axiom` row rollup accordingly (currently `unresolved`/`deferred`).
- Enforcement fork — pick one: (a) promote the constitution-governance `<validation-model>` into a CAV2-local canonical definition/constitution, or (b) execute the frozen Tier-1 task-session — port `arcanum/tools/validate-artifact-constitution.sh` to cav2 roots + wire a `PostToolUse` hook — for CAV2's first *blocking* gate.
- Decide `premise` vs `hypothesis` (`PR-OQ-1`): one term with `hypothesis` as alias, or two.
- Commit this session's changes (submodule-first if `cyberAlchemy-v2` is a submodule); nothing was committed.

## Recommendation

The keystone is the **enforcement gate** — the validator/agent-runtime rung is the only rung of `axiom → invariant → constitution → validator` that is *defined but unbuilt*. Licensing fact: this session's enforcement audit found CAV2 is review-first with a single form-only advisory validator and no act-time gate, so the five definitions just promoted cannot yet be mechanically honored by the agents that write the code. Recommend the next session take the frozen **Tier-1 build** (port the validator + wire the hook) — the cheap, unblocking move — before the heavier typed-relations/registry work; that this is the single highest-leverage next step is a hunch informed by the audit, not a landed test.

## Files touched

- cyberAlchemy-v2/authority/definitions/DEFINITIONS.md
- cyberAlchemy-v2/authority/definitions/DEFINITIONS-INDEX.md
- cyberAlchemy-v2/authority/definitions/DEFINITION-SCHEMAS.md
- cyberAlchemy-v2/authority/definitions/DEFINITION-DRIFT-AUDIT.md
- cyberAlchemy-v2/ontology/CANONICAL-KINDS.md
