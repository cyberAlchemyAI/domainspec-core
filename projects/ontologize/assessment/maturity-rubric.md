# Four-Autonomy Maturity Rubric (0–3 per rule)

> **Status: candidate.** Scoring rubric used by Section D of [`assessment-template.md`](assessment-template.md).
> Method assertions tagged **[SB]** / **[H]**. — *candidate-only.*

## What this scores

Each of the **canonical Four Autonomy Rules** is scored **0–3** based on the client's *observed* agent
practice (what they actually do, not what they intend). Total range **0–12**, descriptive only — there
is no pass/fail threshold; the total is one input to lane selection (Section E). [SB scorability per
[WORK-PACK.md](../WORK-PACK.md) T1 acceptance]

**Source of the Four Autonomy Rules:** defined verbatim in `projects/goldenquill/SOUL.md:40-50`
("The Four Autonomy Rules (Organism Pattern)") — named canonical there and by
`projects/goldenquill/AGENTS.md:16` — and recorded source-backed in [DEFINITIONS.md](../DEFINITIONS.md):56.
[SB]

## Scoring scale (applies to every rule)

| Level | Meaning |
| --- | --- |
| **0 — Absent / greenfield** | The discipline does not exist. (A client running no agents scores 0 across all four rules — the agent layer is greenfield [SB [PLAN.md](../PLAN.md):33].) |
| **1 — Ad-hoc** | Happens sometimes, by individual habit, not by design; inconsistent; not relied on. |
| **2 — Consistent but informal** | Done routinely and deliberately, but enforced by convention/people, not by deterministic code; gaps under load. |
| **3 — Deterministic / enforced** | Built into the system as a non-bypassable gate; fail-closed; reproducible regardless of operator. |

> **Scoring discipline [H]:** score the **observed** behavior. "They plan to" or "they could" = the
> lower level. Cite the evidence in Section D. The 0/1/2/3 boundary is the same shape as GoldenQuill's
> own ladder from convention to deterministic Logician gates [SB the rules are enforced as PRE/POST
> gates in `projects/goldenquill/logician/`].

## Per-rule level descriptors

### R1 — Save State Always
*Canonical: "Every operation saves state on both success and failure. An agent that only saves wins has
amnesia about its losses." [SB SOUL.md:44]*

| Score | Descriptor |
| --- | --- |
| 0 | No agents, or agents keep no state; a crash loses everything. |
| 1 | State saved on success only / occasionally; failures leave no trace. |
| 2 | State saved on success and failure by convention; checkpointing exists but is manual or skippable. |
| 3 | Every operation checkpoints on success **and** failure through an enforced write path; interrupted runs are recoverable. |

### R2 — Test Your Own Work (the magic step)
*Canonical: "Before marking any task complete, validate." The single `if validate()` that turns a tool
into an autonomous agent. [SB SOUL.md:46]*

| Score | Descriptor |
| --- | --- |
| 0 | No self-validation; output is assumed correct or checked only by a human downstream. |
| 1 | Some agents spot-check sometimes; no standard validation step. |
| 2 | Agents validate before completion as a routine practice, but checks are informal / not enforced. |
| 3 | A deterministic validation gate runs before any task is marked complete; failing validation blocks completion (fail-closed). |

### R3 — Be Explicit
*Canonical: "Every task between agents includes input file path, output file path, exact scope, done
definition." No "score the draft" — the actual paths and thresholds. [SB SOUL.md:48]*

| Score | Descriptor |
| --- | --- |
| 0 | Tasks passed as vague natural-language asks; no defined inputs/outputs/scope. |
| 1 | Some tasks specify paths/scope; inconsistent and often implicit. |
| 2 | Tasks routinely carry input, output, scope, and done-definition by convention. |
| 3 | Task contracts (input path, output path, scope, done-definition) are structurally required; an under-specified task cannot run. |

### R4 — Clean Output
*Canonical: "Strip markdown fences from structured data. Strip conversational fluff. Validate format.
Never pass raw LLM output to the next seat." [SB SOUL.md:50]*

| Score | Descriptor |
| --- | --- |
| 0 | Raw model output is passed downstream unmodified. |
| 1 | Output is cleaned manually/occasionally when someone notices a problem. |
| 2 | Output cleaning + format validation is routine practice but not enforced. |
| 3 | Output is deterministically stripped and format-validated before handoff; malformed output is rejected, never forwarded. |

## Recording the score

Enter the per-rule score and the **observed evidence** in Section D of the template. Example shape:

```text
R1 Save State Always       : 1  — "Cron jobs log success to a file; failures are silent (observed in ops review)."
R2 Test Your Own Work      : 0  — "No validation step; humans catch errors after the fact."
R3 Be Explicit             : 2  — "Runbook specifies inputs/outputs per job; followed by convention."
R4 Clean Output            : 1  — "One script strips JSON fences; most outputs passed raw."
Maturity total             : 4 / 12   (low → pulls toward Lane A / hybrid, agent layer largely greenfield)
```
