---
id: cycle-close-research-returns
project: ui-prototyping-studio
title: "Research returns — cycle-close (what to ship for human testing)"
dispatch_id: 2026-06-17-ups-cycle-close-research
node_type: research-returns
updatedAt: 2026-06-17
---

# Research returns (verbatim-condensed) — 3 explorers, 2 rounds (robot-talks)

## Goldratt — MINIMAL-PATH
R1: committed/staged HTML are real .html files on disk; a human can open variants/candidates in a browser today → preview NOT on the minimal path. Only real blocker: README run instructions are FALSE + print the .html path. Flagged own seam: raw .html may not render faithfully if CSS-dependent.
R2 (collapse): VERIFIED — file-artifact-content-store writes HTML verbatim (no bundling/path-rewrite); fixtures are self-contained single-file (inline `<style>`, zero `<link>`/external src) → open-the-file IS faithful FOR THE FIXTURE CORPUS, but the store is content-agnostic so arbitrary CSS-dependent HTML re-promotes preview. SPLIT the claim: open-the-file = "see a variant" (visibility floor, holds) but NOT the gated saw-the-diff (needs render-in-loop). CONCEDED: preview is P0-for-ergonomics (the project's first principle); his minimal path does NOT survive without Grove's run-seam (no root package.json/lock → `pnpm install` fails today; backend has its own package.json). Final P0 split: integrity-floor path (run-seam + true README + print path + reset + protocol) vs ergonomics path (rendered diff at the gate = P0).

## Alexander — ERGONOMICS-CREDIBILITY
R1: a CLI/JSON-in-JSON-out test cannot credibly evaluate the FIRST PRINCIPLE; it re-runs the cold-start failure. Necessary: render a variant, the RENDERED diff, preview --annotate, plain-language onboarding.
R2 (collapse): CONCEDED "render a variant" → nice-to-have (open-the-file gives the retina; contingent on CSS-self-faithful HTML). HELD: the RENDERED DIFF is the irreducible render — a textual diff makes "saw-the-diff" a modality-lie (human signs on a hash, not a visible change). HELD: click-to-annotate genuinely unbuilt (open-the-file gives no hands; naive users can't hand-author selectors). Agreed ordering: Grove (run-seam+protocol) → integrity floor (true README) → his set INSIDE the protocol. Core claim held: CLI-only witnesses the integrity floor, not "a human can drive the gates."

## Grove — DELIVERY-OPS
R1: undeliverable + unsafe today — no root workspace, false README, no run seam, no reset ritual, no tester-facing F2 disclosure, no test protocol; everything uncommitted.
R2 (collapse): WITHDREW "undeliverable" → "unsafe + non-repeatable until P0" (the loop runs today via CLI). Split ergonomics: GOVERNANCE (testable NOW agent-mediated, + protocol + F2 disclosure + reset) vs VISUAL (needs preview = Deliverable 2). NEW load-bearing point: you CANNOT deliver to humans from an uncommitted tree — ONE handoff commit is necessary (freezes README/run-seam + reset script + protocol + F2 disclosure); "reset" has no referent without a committed baseline. Surface the commit-policy (DEC-EXT-COMMIT-POLICY-020) tension to the human gate.

## Convergence (all three, post-confrontation)
- Shared #1 blocker: the FALSE README + missing run-seam (Goldratt + Grove name it identically).
- Two honest deliverables: D1 governance/integrity test (cheap, now) ; D2 visual-ergonomics test (preview + rendered diff, next).
- The mutation core / register / two-gate / honest-diff DATA / SKILL / harness are already-deployed.
- preview = NOT on the integrity path, but P0 for the FIRST-PRINCIPLE (visual) claim → it's "build-needed for D2", not "not-needed".
- One handoff commit is a delivery precondition (policy decision for the human).
