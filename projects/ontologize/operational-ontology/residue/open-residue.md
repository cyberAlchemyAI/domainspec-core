# Open residue — operational-ontology research

Step `validate-and-record-residue`. Carried forward after execution 2026-06-12. Each has a next
object + owner. None of these is promoted.

| id | residue | owner | next route |
| -- | ------- | ----- | ---------- |
| R1 | Operational branch is a **candidate extension**; not accepted as a branch. | ontology-harness | branch-acceptance review |
| R2 | Apex slots (`operational_constitution` L6, `operational_axiom` L7) are declared but **empty**. First operational axiom/constitution candidates not yet drafted. | Constitution Governance | PromotionRecord route |
| R3 | **Circular-governance risk**: `artifact-constitution` discipline already scopes `disciplines/**`. An operational constitution governing disciplines must not take a governed discipline as sole authority source. | Constitution Governance | constitution design w/ circular-authority check |
| R-T1 | Flat signals ledger lacks outcome fields; richest data in `envelopes/`. Derivation tooling must read envelopes. | inventory / observability | envelope-aware derivation |
| R-T2 | Telemetry concentrated in `arcanum/.arcanum/`; domainspec-core root + project roots sparse — branch may under-sample project-level operation. | observability-setup | broaden per-project observability |
| R-G1 | No telemetry stream emits **"discipline hardened"** or **"lesson promoted"** mutations. New instrumentation needed before those mutation types are real. | signal-observer | add envelope fields |
| R-S1 | Schema/Artifact Constitution docs not read for mirror-side evidence (how constitutions cite disciplines). | discipline-authority | read constitutions |
| R-N1 | B1 label ("business" vs "meaning") still open upstream (R12); does not affect B-op schema but touches shared vocabulary. | ontology-vault | upstream decision-gate |

## Verdict recorded

H0 refuted as stated; reframed and accepted: the operational branch's highest category is an
operational constitution + axiom set; `DISCIPLINES.md` is its disciplined source/feed layer.
See [decisions/disciplines-as-axiom.md](../decisions/disciplines-as-axiom.md).
