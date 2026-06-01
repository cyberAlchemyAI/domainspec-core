---
scope: pipeline-wide reference template
purpose: eliminate repeated framework boilerplate in component analyses
created: 2026-04-19
---

# Component Analysis Template

Reference template for all Thesis Team audits, component analyses, and seat-binding reviews. Authors and reviewers reference this file instead of restating the shared framework in every analysis. Only write what is **unique/delta** for the component under review.

## How to Use

1. At the top of any new component analysis, write: `Framework: per pipeline/templates/component_analysis_template.md`
2. State ONLY the component-specific content — bindings, findings, scores, fixes.
3. Do NOT restate the Five Laws, Four Autonomy Rules, failure modes taxonomy, dev-vs-prod distinctions, or standard interface patterns. They live here once.

---

## §1 — Five Operating Laws (binding reference)

All component analyses evaluate against these. Canonical source: `/SOUL.md`.

| Law | Short Name | What Reviewers Check |
|-----|-----------|---------------------|
| L1 | RFA Is Truth | Claims trace to RFA or PROJECT_CONTEXT. No secondhand sources. |
| L2 | No Boundary Drift | Component stays inside RFA-defined scope. No silent expansion. |
| L3 | Org Isolation | One PROJECT_CONTEXT per session. No cross-org data flow. |
| L4 | Apolitical Language + Admin-Risk | Funder dialect code-switching correct. Flagged terms surfaced, never silently rewritten. |
| L5 | Applicant Brings Substance | No fabricated credentials, data, or partnerships. |

---

## §2 — Four Autonomy Rules (binding reference)

Canonical source: `/SOUL.md`.

| Rule | Short Name | What Reviewers Check |
|------|-----------|---------------------|
| R1 | Save State Always | Component saves state on both success and failure. |
| R2 | Test Your Own Work | `validate()` step exists. Self-test before marking complete. |
| R3 | Be Explicit | Input path, output path, scope, done-definition all specified. |
| R4 | Clean Output | No markdown fences in structured data. No LLM self-commentary. Format validated. |

---

## §3 — Standard Failure Modes

Every component analysis should check for these common failure patterns. Only document findings — don't restate the list.

- **Stale state**: component reads cached/old data without freshness check
- **Silent fallback**: degradation happens without WARN emission
- **Missing validation gate**: no PRE or POST Logician gate where one is architecturally required
- **Cross-family violation**: reviewer and author share model family (L-003)
- **Content dump in prompt**: file contents pasted instead of referenced by path (L-002)
- **Aspiration-as-enforcement**: design names a mechanism as load-bearing that doesn't exist on-disk (L-006)
- **Unbounded retry**: revision loop without counter or operator escalation (L-005)
- **Scope leak**: data crosses org boundary, or v0.2+ feature leaks into v0.1

---

## §4 — Standard Hardenings Checklist

Reviewers verify these are present or explicitly scoped out with rationale:

- [ ] Cedar gate bound for security-relevant boundaries
- [ ] Logician PRE-gate for precondition enforcement
- [ ] Logician POST-gate for output validation
- [ ] Fallback cascade defined (retry count → cache → degraded-mode + WARN)
- [ ] Error path bound (not just happy path)
- [ ] State persistence on failure (Rule 1)
- [ ] Self-validation step (Rule 2)
- [ ] Admin-risk term scanning integration (if component produces text)

---

## §5 — Dev vs. Prod Hardware Context

Do not restate in every analysis. Reference this section.

| Tier | Hardware | RAM | Constraint |
|------|----------|-----|------------|
| Dev | M1 Mac Mini | 8 GB | v0.1 must run here. 20% safety margin (A7). |
| Baseline | Mac Studio 128 GB | 128 GB | Production floor. 10% safety margin. |
| Pro | NVIDIA DGX Spark / Mac Studio 128 GB | 128+ GB | Primary production. 5% safety margin. |

If v0.1 runs on Dev, it flies on Baseline/Pro. Component analyses only need to flag Dev-tier constraints when they are binding.

---

## §6 — Standard Interface Pattern

Components in the Tilth pipeline follow this interface contract. Only document deviations.

- **Input**: file path(s) + scope definition + done-definition (Rule 3)
- **Output**: file path(s) + format specification (Rule 4)
- **Validation**: self-test before completion (Rule 2)
- **State**: saved on success AND failure (Rule 1)
- **Dependencies**: declared explicitly, not discovered at runtime
- **Cedar gates**: declared for any security-relevant boundary
- **Logician gates**: PRE (preconditions) and POST (output validation) declared

---

## §7 — Audit Cycle (L-005)

All analyses follow the two-audit cycle per L-005:

1. **Audit #1 — Scoping pass.** Surface all legitimate findings broadly.
2. **Fix round.** Apply repairs into v2.
3. **Audit #2 — Verification pass.** Did v2 repairs land? Any regressions?
4. **PASS**: Editor READY + Judge >= 85 + Red Team READY (or residuals self-downgrade) → LOCK.
5. **DISAGREEMENT**: code/blueprint → operator + Opus synthesis. Grant writing → comments-in-draft.

---

## §8 — Component Analysis Output Format

When writing a new component analysis, use this structure. Each section is component-specific content only.

```
# [Component Name] — [Analysis Type] (e.g., "Scout Bindings — Thesis Team Audit")

Framework: per pipeline/templates/component_analysis_template.md

## Component Identity
- Seat/role:
- Scope:
- Architecture section reference:
- Blueprint section reference:

## Law Bindings (delta only)
[Which laws are load-bearing for THIS component and how they bind specifically.
Skip laws that bind in the standard way with no component-specific nuance.]

## Rule Bindings (delta only)
[Same — only component-specific applications of the four rules.]

## Interfaces
[Input/output paths, formats, dependencies — only what's unique to this component.]

## Findings
[The actual audit content — convergent findings, divergent findings, severity.]

## Fixes Required
[Table: #, Change, Source, Severity]

## Verdict
[Score, lock/no-lock, conditions.]
```

---

## Cross-References

- Five Laws + Four Rules canonical: `/SOUL.md`
- Locked architecture: `pipeline/architecture/v0.1/tilth_architecture_locked.md`
- Lessons (mandatory pre-checks): `/lessons.md`
- Audit cycle discipline: L-005 in `/lessons.md`
- Enforcement-layer existence audit: L-006 in `/lessons.md`
- Session orientation: `pipeline/SESSION_BOOTSTRAP.md`
