# Final approval

- Dispatch: `2026-07-31-dual-residue-experiment-feasibility-review`
- Run: `run-20260731-dual-residue-feasibility-02`
- Auditor: Brandenburg, Martin (`/root/dr_auditor`)
- Action: `spawn-0007`
- Execution: `pass`
- Decision: `ACCEPT`
- May close: yes

## Accepted checks

- All three attacker lanes preserve distinct initial and reconciled positions.
- One bounded verifier/synthesizer zig-zag resolved the definitional objections;
  both verification receipts passed.
- Exactly five KEEP and five CRITICAL FIX dispositions remain with live evidence,
  severity, rationale, and repair.
- Comparator, `grad_indep`, DPO, D-weight, aggregate-evaluation, fail-open reporter,
  denominator, corpus, freeze, and premise-bridge evidence was spot-checked.
- The reporter counterexample is supported by `scripts/report.py:81-108`: point
  estimates can emit `VALIDATED` while paired samples and p-values are absent.
- Change requests are dependency ordered, and no refuted finding survives.
- `NOT-YET-FEASIBLE` is separate from the bounded architectural FIT assessment.
- Inventory remains non-authoritative and promotion ceilings remain candidate-local.
- The target stayed clean on `main` at
  `a07d8bcf10f6292d708e063b2ea992ee744cf807`.

## Residual blocked coverage

Pytest, smoke execution, dependency-backed mechanics, model execution, and training
remain unrun because the ML dependencies are absent and installation, downloads, and
training were forbidden. These gaps prevent empirical and runtime-readiness claims;
they do not invalidate the read-only review.

## Approved conclusion

The repository is architecturally fit as a bounded candidate evidence harness, but
the current experiment is `NOT-YET-FEASIBLE`: claim identity, treatments, corpus
custody, and statistical adjudication do not yet conform to one frozen contract. A
repaired frozen run could establish only a pinned local treatment-effect result,
subject to separate canonical-owner acceptance.
