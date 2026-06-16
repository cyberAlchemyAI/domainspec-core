# Implementation Layering - Triton Top2 Paper Package

## Objective

Build a MARS-governed paper package from the completed Triton Top2 research
tower without weakening evidence traceability or overclaiming.

## L0 - Evidence Inventory

Question: do we know exactly which files evidence the work?

Outputs:

- `EVIDENCE-MANIFEST.md`
- `REFERENCE-LEDGER.md`
- initial source classes and claim guard table

Promotion evidence:

- every major technical claim has at least one source artifact;
- every benchmark number links to raw artifact;
- every validation claim links to task-session evidence.

## L1 - Paper Contract

Question: can the paper be reviewed before prose exists?

Outputs:

- `PAPER-SPEC.md`
- `PAPER-STORIES.md`
- `PAPER-TEST-SPEC.md`
- `PAPER-REVIEW.md`

Promotion evidence:

- every intended paper section has inputs and blockers;
- paper test obligations exist for all claims;
- unsupported claims are explicit non-claims.

## L2 - Paper Draft And Data Appendix

Question: can the evidence be synthesized into a readable document?

Precondition:

- Lean formal-boundary lane has produced `formal/FORMAL-VALIDATION-REPORT.md`
  or has been explicitly deferred with a reason.

Outputs:

- `paper.md`
- `DATA-APPENDIX.md`
- optional `appendices/` and `figures/`

Promotion evidence:

- all paper tables trace back to source artifacts;
- paper narrative cites the evidence manifest;
- limitations match final technical reports.

## L3 - Review And Presentation Package

Question: is the document safe to present?

Outputs:

- updated `PAPER-REVIEW.md`
- `PRESENTATION-PACKAGE.md`
- final readiness marker

Promotion evidence:

- paper test spec passes or explicitly flags residuals;
- private/public boundary review passes;
- no unsupported novelty or performance claims remain.

## Deferrals

- PDF/LaTeX conversion is deferred until Markdown paper review passes.
- External submission formatting is deferred until target venue/audience is
  chosen.
- Additional benchmark scaling is deferred unless the paper review decides the
  current smoke benchmark is insufficient for presentation.
- Full real-analysis softmax derivative proof is deferred unless the first Lean
  finite-sum algebra slice is stable.
