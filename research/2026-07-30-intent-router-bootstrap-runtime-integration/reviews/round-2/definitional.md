# Definitional and Authority Review — Round 2

status: `GO`

All prior definitional blockers are repaired:

- Support evidence, disposition integrity digest/current wire
  `receipt_digest`, reasoning/lifecycle receipts, and authority evidence are
  separately defined. None upgrades authority by existence.
- Extraction candidate, canonical source acceptance, generated-package
  promotion, published release, and consumer installation have separate
  owners, gates, artifacts, and witnesses; deployment and production are
  separately bounded.
- Human choice, Dispatch binding, authorization, execution attempt, observed
  effect, and required receipt are explicitly non-substitutable and
  independently fail closed.
- Future acceptance cases cover candidate without confirmation, confirmed
  binding, mismatch, authorization denial, failed attempt, and effect without
  receipt.

No new public/private, routing/reasoning, or lifecycle authority collapse was
detected.
