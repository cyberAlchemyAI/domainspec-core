# Decision Record — DomainSpec → Arcanum Capability Build

Scope: select + sequence **milestone 1** of the capability build/lift into public arcanum.
Source of decisions: operator, in-session via `decision-gate`, 2026-06-14.
Related artifacts: [domainspec-wedge-inventory.md](domainspec-wedge-inventory.md), [domainspec-wedge-inventory.dispatch.json](domainspec-wedge-inventory.dispatch.json).
Standing prior decision (Q1): domainspec stays private; only the free wedge is exported to public arcanum.

---

## B1 — Milestone-1 scope
**Decision: Keystone + full spec pipeline.**

Options considered:
- Keystone only (spec-write + taxonomy lift) — smallest, foundational.
- Keystone + 2 ⭐ quick wins (interrogation modes, dispatch-spec anti-bias) — balanced.
- **Keystone + full spec pipeline — SELECTED.**

**M1 build set:**
1. **spec-write (keystone)** — DomainSpec SPEC + aspect-doc template *replaces* Module Formulae as invoke's `define` baseline (full replacement, per recorded decision) + discovery-existence soft gate.
2. **Wedge lift (keystone)** — taxonomy / relationships / definitions vocabulary (DS-D1/D2 wedge subset) into `arcanum/definitions/`.
3. **test-derivation engine** — built fresh in arcanum (see B3).
4. **doc→metrics derivation O1–O16** — new arcanum sigil (runtime stays private).
5. **sync-registry** — improve `definitions-governance` (concept-graph-edge + meta-type aggregation).
6. **sync-user-stories** — new sigil (slice taxonomy + concept-coverage matrix).
7. **code-tag traceability toolchain** — new (deterministic audit; decouple default paths).
8. **audit-alignment** — new sigil (compliant/partial/missing/extra fidelity audit).

Rationale: the keystone unblocks the rest, and the full pipeline lands the complete spec→test→observability→audit wedge in one milestone. Operator accepted the higher effort/risk (esp. the engine).

Downstream impact: large M1; multiple new public sigils + an invoke contract change. Requires the plan stage to sequence and the sanitization gate before any public push.

## B2 — Public branding
**Decision: "DomainSpec" is the public wedge brand inside arcanum.**

Options considered:
- **Yes — DomainSpec is the public wedge brand — SELECTED.**
- No — neutral arcanum-native naming, keep DomainSpec private.

Rationale: open-core — give away the wedge under its name (DomainSpec), sell the trust under another (CyberAlchemy, private). Names carry over on lift; no renaming work. CyberAlchemy + governance engine + attestation remain the private moat brand.

Downstream impact: public arcanum artifacts (template, spec pipeline, sigils) carry the DomainSpec name. Reversible but costly later (public brand). Forecloses the neutral-naming path.

## B3 — Test-engine approach
**Decision: Build fresh in arcanum, using the DS skeleton as a design reference.**

Options considered:
- Port skeleton + finish in arcanum — most code reuse.
- Specify-only for M1, build in M2 — de-risk.
- **Build fresh from design as reference — SELECTED.**

Rationale: cleanest open/private boundary and provenance — no DS code crosses into public arcanum; the skeleton (`keys/roundtrip/emit/ir` + the `derive→obligation_key→roundtrip` architecture) serves as the design spec. Operator accepted the higher effort vs porting.

Downstream impact: arcanum gets a from-scratch deterministic compiler; the DS skeleton stays private as reference. Removes the code-provenance/license entanglement flagged earlier. Highest build effort of the three.

---

## Remaining blockers (must close at the plan stage, before the relevant M1 item mutates public arcanum)
- **defs-split + canonical-home** — blocks M1 item #2 (definitions lift): split the normative `DEFINITIONS.md` at the wedge/moat seam and pick ONE public canonical home (recommend DS-D1/D2 canonical, prose as example layer). Do not lift the proposed ~38-edge extension.
- **Sanitization / moat-leak audit** — constraint on every public push: strip DS-private paths, agent ids, `ZefraHub`, Portuguese confidence terms; decouple hardcoded CI validator names; whole-diff `g05` check that no moat content leaks.

## Deferred to M2+ (recorded, not in M1)
- ⭐ interrogation modes, ⭐ dispatch-spec anti-bias check (zero-dependency, low-risk — candidates to parallelize early despite deferral)
- workflow-reflect thresholds, context-builder scoring, orchestrate planner-gate, implementation-layering drift-audit, observed-invocation-loop session epilogue
- ontology-view, brownfield-translation, delegation-adapter (free-standing new sigils)
- The remaining open seams from the inventory not touched by M1 (seam-3 Lean, seam-4 host trees, seam-5 constitution lift, vault parity)

## Assumptions / constraints
- All authoring lands in public `arcanum` under submodule-first discipline (commit+push in arcanum before bumping the parent gitlink; `make bump-check`).
- Owner lifecycle: `invoke plan` → `sigil-development` / `spellcraft` for the new sigils; invoke contract edit for the template swap. This decision-gate selects scope only; it does not author.

---

# Keystone Lift Decisions (decision-gate, 2026-06-14)

Scope: the keystone definitions lift (M1 item #2) — resolve `defs-split` + `canonical-home` before `invoke plan`.

## C1 — Canonical form
**Decision: Formal DS-D1/DS-D2 canonical; TAXONOMY.md/RELATIONSHIPS.md prose recomposed as the example/explanatory layer pointing at the IDs.**
- Options: formal canonical + prose example (SELECTED) · prose canonical + IDs as index · new merged doc.
- Rationale: one machine-checkable source of truth, drift-detectable; Part C recommendation; avoids a third source.
- Downstream: `arcanum/definitions/DEFINITIONS.md` = canonical DS-D1 (25 types) / DS-D2 (29 edges); prose files link to IDs.

## C2 — Canonical home + reference direction
**Decision: Public arcanum is canonical for the wedge subset; private domainspec keeps only the moat cluster and references arcanum for wedge terms.**
- Options: arcanum canonical + DS references (SELECTED) · DS canonical + arcanum mirrors a synced copy.
- Wedge subset (canonical → arcanum): DS-D1, DS-D2, DS-D3, DS-D7, DS-D8, DS-D10, DS-P1..3.
- Moat cluster (canonical → private DS): DS-C3, DS-D9, DS-COR-1, DS-F1, DS-F5, DS-F6, DS-M13.
- Rationale: open-core traceability (public can see the real source); no duplication / no third source.
- Downstream / accepted cost: private domainspec now **depends on the arcanum submodule** for its wedge vocabulary; DS DEFINITIONS.md replaces the wedge defs with references to arcanum.
- Do-not-lift reaffirmed: the proposed ~38-edge / 7-category extension (DS-D2 marks it proposed-not-adopted).

## C3 — Ambiguous DS-D4/D5/D6 placement (DEFERRED)
- DS-D4 (derivation), DS-D5 (dual-track layers), DS-D6 (L7 orchestration contract) — agent A flagged D6 trends governance.
- **Default applied (conservative, moat-protection bias):** hold D4/D5/D6 PRIVATE until `definitions-governance` execution confirms each is decoupled from the CyberAlchemy governance chain. Do not publish by default.
- Resolve during the keystone work-pack execution, not a planning blocker.
