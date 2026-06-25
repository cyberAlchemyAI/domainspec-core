# Authority-Triage — Validation Experiment

Sigil: `authority-triage` (candidate) · Profile: sigil-development
Status: **first corpus run — PASS** · Created: 2026-06-24

## Purpose

Validate that `authority-triage` correctly classifies arbitrary candidates into
`already-authority` / `build-from-owned` / `not-authority` / `new-authority` /
`blocked-default-deny`, sweeps for an owner before any net-new verdict, and routes
to the narrowest owner. The **Claude Code memory** is the natural first corpus: a
real, mixed bag of captured candidates.

## Corpus — the 7 Claude Code memory notes

| # | Candidate (memory note) | Expected verdict | Expected route |
| --- | --- | --- | --- |
| 1 | `precedent-sweep / build-from-owned` | build-from-owned | constitution-governance (consolidate, deriving from CAV2-D48) |
| 2 | `ergonomics-first-principle` | build-from-owned | VALUE doc (≈ `CAV2-CAND-HMI-001`; owner: keep as proposition) |
| 3 | `cav2-condense-knowledge-is-purpose` | build-from-owned | VALUE doc (overlaps `CAV2-D2/D18/D19/distill`) |
| 4 | `saturn-domainspec-public` | new-authority | decision-gate + boundaries (public/private Decision) |
| 5 | `engine-algorithm-proprietary` | new-authority | decision-gate + boundaries (IP/moat Decision) |
| 6 | `explanation-style-plain-concrete` | not-authority | stays memory (personal interaction preference) |
| 7 | `pdfkit-themed-builder` | not-authority | stays memory (tooling reminder) |

## Run results (the sigil's process applied)

| # | Precedent sweep | Verdict | Route | Match? |
| --- | --- | --- | --- | --- |
| 1 | OWNER FOUND — `CAV2-D48` + research precedent gate | build-from-owned | constitution-governance (consolidation) | ✅ |
| 2 | OWNER FOUND — `CAV2-CAND-HMI-001` | build-from-owned | VALUE doc | ✅ |
| 3 | OWNER FOUND — `CAV2-D2/D18/D19` | build-from-owned | VALUE doc | ✅ |
| 4 | clean (no owner) → needs-authority YES → Decision kind (enumerated) | new-authority | decision-gate + boundaries | ✅ |
| 5 | clean (no owner) → needs-authority YES → Decision kind (enumerated) | new-authority | decision-gate + boundaries | ✅ |
| 6 | n/a → needs-authority NO (governs no future work) | not-authority | stays memory | ✅ |
| 7 | n/a → needs-authority NO | not-authority | stays memory | ✅ |

**Score: 7/7.** The two `new-authority` cases (#4, #5) were then actually promoted
to governed decision records + `boundaries.md` entries — a downstream check that the
routing produces real governed artifacts. The three `build-from-owned` shadows
(#1–#3) were correctly **not** promoted (no duplication of owned authority). No
`blocked-default-deny` case appeared (all kinds enumerated).

## Quality-bar checks

- ✅ precedent sweep ran BEFORE any verdict (build-from-owned first);
- ✅ `not-authority` distinguished from authority candidates (no over-promotion);
- ✅ each kind cited an Authority-Kinds row / owner;
- ✅ routed to exactly one narrowest owner; wrote nothing into an authority surface itself;
- ✅ preferred consolidation over net-new for the diffuse build-from-owned rule.

## Gaps / not-yet-covered (promotion-readiness)

- Only **one corpus** (the memory batch). A fuller harness needs **low/medium/complex
  synthetic cases**, including a clean **`blocked-default-deny`** case (an
  unenumerated authority kind) and an **axiom-candidate** case.
- No deterministic check — classification is review-mode (acceptable for a candidate).

## Verdict + recommendation

**VALIDATION: PASS on the memory corpus** (7/7, plus a real downstream promotion).
**Promotion-readiness: NOT YET** — add the two synthetic corpora (esp. the
default-deny case), then promote to `arcanum/arcana/authority-triage/`. ⚠️ Promotion
to `arcanum/` is a **public submodule** write needing a boundary scrub + submodule
commit — the operator's call, not auto.
