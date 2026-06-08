# Stage 7 — Interrogation (refine-design-review)

**Verdict: flag → repair.** LANE-B-DESIGN.md meets all done-criteria (layer mapping, 5 bridges with
verdict/MVP/gap/owner, build order, free-vs-build honesty). Flags:

- F1: ensure NET-NEW vs EXTEND is unmistakable so the offer isn't over-scoped as "all reuse" or
  under-scoped as "all build". → repair (the Headline + the free-vs-build summary state 3 EXTEND / 2 NET-NEW).
- F2: build order must mark what is descope-able to pilot-1. → repair (Bridge 1 marked advisory in pilot-1).

bridge-verdict-decidable gate: pass — every bridge has a decidable verdict + MVP + cited path or
net-new reason. Owner-boundary preserved (read-only; building is a separate route). No promotion.
