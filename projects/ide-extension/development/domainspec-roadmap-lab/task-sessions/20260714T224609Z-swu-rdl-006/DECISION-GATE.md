# Decision Gate: SWU-RDL-006 Dirty IDE Route Ownership

## Target Scope

`SWU-RDL-006` focused Roadmap Lab IDE route and Canvas witness.

## Result

BLOCK.

## Blocker Question

How should Roadmap Lab proceed when its required IDE route/kernel files are
already dirty with substantial Craft Frontier and Operations v1 work?

## Options

### 1. Finish or isolate the current IDE Operations/Craft work first

- Benefit: keeps SWU-RDL-006 strict, avoids corrupting unrelated dirty hunks,
  preserves the Roadmap Lab architecture requirement to reuse the real Canvas
  kernel.
- Cost/risk: Roadmap Lab pauses here until that IDE surface is committed,
  shelved, or explicitly separated.
- When to choose: when the current dirty IDE work has its own owner or is
  intended to land.
- Downstream impact: rerun SWU-RDL-006 on a stable baseline; validation remains
  focused and credible.

### 2. Explicitly authorize composing SWU-RDL-006 into the dirty IDE files now

- Benefit: fastest path to keep moving in one worktree.
- Cost/risk: higher merge and regression risk; Roadmap Lab changes would be
  interleaved with Operations v1/Craft Frontier hunks and require broader IDE
  regression evidence.
- When to choose: only if the same owner accepts the current dirty work and wants
  Roadmap Lab integrated into it immediately.
- Downstream impact: SWU-RDL-006 context must expand to include Operations v1,
  Craft Frontier UI, package scripts, and their tests.

### 3. Create a separate minimal Roadmap Lab wrapper route without touching the dirty Canvas page

- Benefit: avoids most dirty hunks.
- Cost/risk: likely violates the architecture by duplicating or bypassing the
  accepted Canvas kernel; may produce a false witness that does not prove the
  real parent route/event path.
- When to choose: only if owners revise the architecture and accept a temporary
  non-canonical demo.
- Downstream impact: requires design/work-pack amendment before mutation.

## Recommendation

Choose option 1. It is the stricter route without unnecessary hardening: stop
before touching shared IDE runtime files, finish or isolate the existing
Operations/Craft changes, then resume SWU-RDL-006 against a coherent baseline.

## Remaining Blockers

1. Human/owner decision on the dirty IDE worktree path.
2. If option 2 is chosen, expanded context and validation scope are required
   before mutation.
3. If option 3 is chosen, Roadmap Lab architecture and work-pack must be amended
   before mutation.
