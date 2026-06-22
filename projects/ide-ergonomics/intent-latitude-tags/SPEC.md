# SPEC (draft) — Intent-Latitude Tags + Validator Contract

Status: Lane-Z draft artifact (research-only, not canonical; promotion-gated)
Date: 2026-06-18
Owner: DomainSpec v2
Builds on: [FINDINGS.md](FINDINGS.md) · [SEED.md](SEED.md)

This is the **grounded form** (candidate B). The whole design rests on one rule
from the FINDINGS: **a tag's meaning is fixed by the validator contract, not by the
model reading the word inside the bracket.** Every section below is written so the
tag would still mean what it means even if the model ignored the bracket entirely —
because a post-hoc check enforces it. Where that is not achievable (`[goal]`,
`[constraint]`), the spec says so plainly rather than pretending.

---

## 1. The vocabulary (small and closed)

Exactly three tags. The set is closed on purpose: a closed vocabulary is what lets
a validator have a fixed contract per tag. Adding a tag requires adding a check
class in §4.

| tag | latitude | one-line meaning | grounding strength |
| --- | --- | --- | --- |
| `[literal]…[/literal]` | **zero** | reproduce / preserve this span **exactly** | **strong** — mechanically checkable |
| `[goal]…[/goal]` | **high** | this is the outcome to achieve; wording and method are free | **weak** — rubric/judge |
| `[constraint]…[/constraint]` | **bounded** | a line that must not be crossed; paraphrase is fine, violation is not | **medium** — predicate or judge |

Latitude is the axis that does **not** already exist in content-type tag systems
(`<instruction>` / `<context>` mark *what kind of content*; these mark *how much
freedom the model has over the span*). That orthogonality is the non-tautology
claim from FINDINGS.

Default (untagged span): latitude is **unspecified** — the model uses its own
judgment, exactly as today. Tags are opt-in markers on the spans that matter.

## 2. Syntax

```
[literal]<span>[/literal]
[goal]<span>[/goal]
[constraint]<span>[/constraint]
```

- Paired open/close, like XML. Reusing a bracketed form is deliberate (FINDINGS:
  the bracket's *delimiter* value is real; its *semantic* value comes from §4).
- Tags may not overlap; they may nest **only** `[literal]` inside `[goal]` /
  `[constraint]` (an exact string required inside a free-latitude outcome). Any
  other nesting is a parse error (§4.0).
- A tag id may be attached for traceability: `[literal id="disclaimer-1"]…`.
  Ids are how the validator report points back at the offending span.
- The author writes tags; the **model never emits them** in its output. Output is
  ordinary text — the tags live only in the prompt/spec.

### Worked example (one DomainSpec span)

```
Rewrite the landing page copy.

[goal]The page should feel welcoming to a first-time visitor.[/goal]

[constraint]Do not invent product features that aren't in the feature list.[/constraint]

The footer must read, verbatim:
[literal id="legal"]© 2026 Acme Inc. All rights reserved. Not legal advice.[/literal]
```

What each tag buys over a prose header — **only** because of §4, not the words:
- `[literal id="legal"]` → the validator *extracts that exact string and diff-checks
  it appears unchanged in the output*. A prose "keep this verbatim" header has no
  such check; the model may paraphrase and nothing catches it.
- `[goal]` → the validator *excludes* this span from verbatim/contains checks and
  *routes it to a goal check* (§4.2). It tells the rest of the pipeline "this is a
  success criterion, not a string to reproduce."
- `[constraint]` → registered as a guard the output is checked **against** (§4.3).

## 3. Semantics (author-facing contract)

- `[literal]` — "If one character of this span is altered, paraphrased, summarised,
  or dropped, the result is **wrong**." Use for: legal text, names, ids, quoted
  strings, API signatures, exact values.
- `[goal]` — "This is **where we are going**. Any output that achieves it is
  acceptable; the wording here is a description of done, not text to keep." Use for:
  outcomes, target states, acceptance intent. (This is the inline form of the
  [target-state](../../domainspec-v2/research/target-state/SEED.md) tower's artifact.)
- `[constraint]` — "A **boundary**. The output may say it any way, or not mention it
  at all, but must not violate it." Use for: prohibitions, invariants, scope fences.

## 4. Validator contract (the grounding — this is the load-bearing part)

The validator runs **after** the model produces output `O`, against the set of
tagged spans `T` parsed from the prompt `P`. It returns
`{verdict: PASS | FAIL, findings: [...]}`. The model honoring the tag is **not
assumed**; the check is what enforces the latitude.

### 4.0 Parse

```
parse(P) -> spans: [{tag, id?, text, start, end}]
```
Reject (author-time error, before the model runs) on: unbalanced tags, illegal
overlap, illegal nesting (§2), unknown tag name. Closed vocabulary makes this a
total function.

### 4.1 `[literal]` check — STRONG (mechanical)

```
for each literal span L:
    if normalize(L.text) is NOT a contiguous substring of normalize(O):
        FAIL { tag: literal, id: L.id, expected: L.text, reason: "verbatim span absent or altered" }
```
- `normalize` = a declared, fixed transform (e.g. collapse internal whitespace,
  NFC unicode) — declared once so "verbatim" is unambiguous.
- This check needs **no model**. It is the proof that the grounded form is not
  tautological: the tag changes what the *system* does (a diff-check exists),
  independent of how the model read the bracket.
- On FAIL the pipeline either **rejects + regenerates** (with the failing span
  re-emphasised) or **surfaces to the author** — caller's choice, recorded in the
  run config.

### 4.2 `[goal]` check — WEAK (rubric, honestly labelled)

```
for each goal span G:
    exclude G.text from all verbatim/contains checks   # mechanical, reliable part
    register G.text as an acceptance rubric
    satisfied = goal_oracle(O, G.text)                 # see grounding ladder below
    if satisfied is FALSE: FAIL { tag: goal, id: G.id, reason: "<oracle rationale>" }
    if satisfied is UNKNOWN: FLAG (not FAIL)
```
**Grounding ladder for `goal_oracle`, strongest first — use the strongest available:**
1. **Mechanical oracle** if the goal is expressible as one (a test, a regex, a
   numeric threshold, a schema). Preferred whenever possible.
2. **LLM-judge** with `G.text` as the rubric, run as a *separate* call from the
   generator. This is drift-prone (FINDINGS: judges format-sensitive) → it returns
   `FLAG`, not `FAIL`, unless the judge is itself validated on a fixture set.
3. **None** → the goal is recorded as **unenforced**; the run report must say so.
   Silent "PASS" for an unchecked goal is forbidden (claim ≤ proof).

The reliable, non-tautological part of `[goal]` is item-0: **exclusion** — the
verbatim machinery will not wrongly flag a free-latitude span. That alone is a real
behavior a prose header lacks. The satisfaction check degrades honestly.

### 4.3 `[constraint]` check — MEDIUM

```
for each constraint span C:
    if C carries a machine predicate (C.predicate):
        if predicate(O) is FALSE: FAIL { tag: constraint, id: C.id }
    else:
        violated = constraint_judge(O, C.text)   # separate call
        if violated is TRUE:    FAIL
        if violated is UNKNOWN: FLAG
```
Same ladder as `[goal]`: a declared predicate is strong; a judge is `FLAG`-grade
until fixture-validated.

### 4.4 Aggregate

```
verdict = FAIL if any finding is FAIL else PASS
report  = { per-span: [{tag, id, check-class, strength, result, rationale}],
            unenforced: [ids with no oracle] }
```
The report **must** list `unenforced` spans. The tower's honesty rule: a span the
validator could not actually check is reported as *unenforced*, never as *passed*.

## 5. What this spec deliberately does NOT claim

- It does **not** claim the model interprets `[literal]`/`[goal]` correctly because
  the words are suggestive. The FINDINGS kill that (the naive form). All force is in
  §4.
- It does **not** claim `[goal]`/`[constraint]` enforcement is reliable. Those
  degrade to judges and are `FLAG`-grade until validated on fixtures — the central
  open question (SEED residue).
- It does **not** introduce `[literal]` for *instructions* (only for *content*),
  because "did the model follow this instruction exactly" is not mechanically
  checkable. Lane Z must decide whether that scope is too narrow.

## 6. Minimal proof obligation before any promotion

1. Implement §4.0 parse + §4.1 `[literal]` check (no model needed). Show on a
   fixture set that a paraphrased verbatim span is caught (TRUE positive) and an
   intact one passes (TRUE negative). **This alone refutes the tautology charge** —
   a behavior no prose header has.
2. For `[goal]`: show item-0 exclusion measurably reduces false verbatim-flags vs
   an untagged baseline.
3. Only then design the judge-validation for `[goal]`/`[constraint]`.

Until (1)–(2) pass, this remains a Lane-Z draft, not a promotion candidate.

## 7. Lane A debt (do not skip)

This spec is the Lane-Z build. The tower still owes a Lane-A alternative to the
*same* problem (unsignalled latitude) — strongest candidates from SEED: a
**clarification loop** (ask before acting on ambiguous latitude) and **preference
uncertainty** (Russell). The synthesis must say why grounded tags beat, or lose to,
asking — before anything here is proposed for promotion.
