## s8 Toy Game — outcome

Artifact written: `/home/vrondelli/projects/domainspec-core/implementation/domainspec/docs/features/ui-prototyping-studio/development/refinement-runs/20260615T205403Z-mutation-execution-mechanics/stages/08-toy-game.md`

### Worked example (controlled, cooperative proposer)
- Input: card with `<button data-od-id="cta.primary">` at 32px; one MutationTask (odId `cta.primary`, intent "increase tap target", acceptanceText "button >= 44x44px", changeType `change`).
- Ran two cooperative sub-variants through V6→V1→V2/V4→V3→V7→V9→V9b→V5→V8:
  - **C1-A** (change lands on the anchored element, inline `style`): all required validators PASS → ADMIT, DiffSummaryHonest computed, two-gate hash-bound accept records exactly the staged hash. Mechanism is clean.
  - **C1-B** (change lands in `<style>` — the *idiomatic* CSS way to satisfy the sizing task): **V2 FAILS** (`TARGET_UNCHANGED`) because the button's od-id subtree is byte-identical. The model **false-rejects a legitimate, intent-realizing candidate**.

### Adversarial case (proposer also edits out of scope)
- **C2-A** (out-of-scope edit on an *anchored* element `card.hint`): V3 correctly REJECTS (`OUT_OF_SCOPE_CHANGE`). Fence works for anchored elements.
- **C2-B** (out-of-scope edit on *un-anchored* markup — rewrites `<h2>` title and a `<style>` rule): traced V3 exactly as specified (ChangedSet = symmetric set-diff of `odIndex`). The un-anchored changes are **not in odIndex at all**, so `ChangedSet = {cta.primary}`, `ChangedSet \ (TaskScope ∪ S) = ∅` → **V3 PASSES → ADMIT**. The adversarial title/style rewrite becomes head and is **hidden from the human diff gate** (fragments are odIndex-derived too).

### Failures interpreted
- **TG-1 / s7-B1 (BLOCK):** V3 fence is odIndex-bounded, not document-bounded; admits un-anchored out-of-scope change. C's auditability/odid advantage over B is false as written.
- **TG-2 / s7-B2 (FLAG):** acceptanceText is never machine-checked — a 33px and a 48px button get the identical ADMIT verdict against "button >= 44x44px". Admit ≠ acceptance met.
- **TG-3 (new, sharpens B1):** same odIndex-only assumption *false-rejects* the idiomatic CSS-driven realization (C1-B). The model is simultaneously too loose (adversarial un-anchored) and too strict (legitimate un-anchored CSS).
- **TG-4 / s7-B3 (NOTE):** V9 PASS is unfalsifiable — no default `B`/`S`/`k`/`c`.

### Repairs applied to the model
- **R1** — s6 validator-model V3 rewritten: change-detection is now a **whole-tree canonical diff** with od-id attribution + a `⊥` unattributed bucket; any change not dominated by a TaskScope od-id (all un-anchored markup) = REJECT.
- **R2 (caveat)** — s6 validator-model V2 marked **unsound for CSS-driven change**; R2-a vs R2-b decision deferred to the RESIDUE-B spike.
- **R3** — s6 design §8 budget gains the **intent-fidelity gap** (admit ≠ acceptanceText met; quantitative acceptance judged only by human eye).
- s6 design §3.2/D5 coverage note coupling fragments to R1; §5 V3 row updated to whole-tree; RESIDUE-B expanded to cover whole-tree fence + R2 decision + B/S/k/c calibration.
- Out-of-scope repairs (artifact port s7-A1, RevisionApplied lifecycle s7-C1, removeRevision/rollback s7-C2, accept-time staleness s7-C3, ProposeInput serialization s7-F1, RESIDUE-G, V8 capability-denial s7-A2) left to s7's required-before-plan list; not exercised by the toy game.

### Verdict
FLAG — plannable after R1 lands as code and R2 is decided by the spike, consistent with s7's required-before-plan list, now backed by a reproducible falsifying input.