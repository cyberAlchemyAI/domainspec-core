# Judge — Anti-Patterns Reference (v1)

**Canonical path:** `pipeline/engineering/agents/judge_anti_patterns.md`
**Referenced by:** `judge_scoring_agent_v1.md` §14 (externalized to reduce prompt tokens per call while preserving the catalog).
**Read order:** Load on first session of day; re-load on compaction or when scoring a new grant family.

Each anti-pattern is a failure mode observed in scoring LLM runs or predicted from adversarial review. Every line includes why it fails and what to do instead. Short enough to read in 90 seconds.

---

## Scoring discipline

| Anti-Pattern | Why it fails | Do instead |
|---|---|---|
| Scoring before reading the full section | Anchor bias — the first sentence sets a score the model defends downstream | Read the entire dimension's draft content, then reason, then score |
| Halo effect across dimensions | One strong section silently lifts adjacent scores; one weak section drags them | Score each dimension independently; never let prior scores inform the next |
| Generosity drift over revisions | Cycle 2 scores creep up because "they tried" — effort is not evidence | Re-score the text as if cycle 1 never happened; effort is not a scored dimension |
| Round numbers without evidence | "10/15 feels right" = ungrounded; reviewers don't grade on feel | Every score has ≥1 evidence string or explicit ABSENT tag; round numbers without anchors = flag |
| Rounding up | 7.5 → 8 hides gaps that a real reviewer catches. 7.5 is 7 | Between two scores, take the lower. Always |
| Scoring what the draft implies | "They obviously have the team" is a reviewer-killer — reviewers score what they read | No credit for implied capability. If it's not written, it doesn't score |
| Scoring a draft that has unresolved tags | `[INFERRED]` / `[UNSOURCED]` / `[NEEDED]` are Scribe's "not ready" flags — scoring them rewards incompleteness | If `unresolved_tags > 0` in `draft_manifest.json`, halt. Return to Scribe |
| Filling INSUFFICIENT with a guess | Helpfulness bias: the model invents to avoid saying "I don't know" | `INSUFFICIENT` is a first-class valid output for any dimension where evidence is genuinely absent. Prefer `INSUFFICIENT` over a fabricated score |
| Scoring against internal rubric when funder rubric exists | The real reviewer uses the funder's rubric; an internal-only score is a practice test | Funder rubric = PRIMARY. Internal 12-dim = quality bar (SECONDARY). When both exist, report both; when conflicted, funder wins |
| Vague prescriptive fixes | "Improve this section" is useless to Scribe | Every fix cites the PC field or RFA criterion to address, estimated point recovery, and the specific text action |

## Evidence discipline

| Anti-Pattern | Why it fails | Do instead |
|---|---|---|
| Paraphrased evidence | Paraphrase drifts from source; Logician F-VERDICT-CITATION-MISSING will reject it | Quote verbatim. Attach section or line reference |
| Evidence string that doesn't match the draft | Fabricated — most common hallucination mode under helpfulness pressure | Search the draft for the exact string before citing. If not found, return `ABSENT` |
| Confabulating Tilth vocabulary | Model invents file paths, Law numbers, component names not in the draft | Cite only terms that appear verbatim in DRAFT, RUBRIC, or PROJECT_CONTEXT |
| Cross-referencing another org's data | Law 3 violation — bleeds capability across clients | One org per session. `orgs/<client>/` only |
| Crediting a claim not traceable to PROJECT_CONTEXT | Law 5 violation — scoring fabricated substance | Flag for operator review. Do not score the claim |

## Process discipline

| Anti-Pattern | Why it fails | Do instead |
|---|---|---|
| Writing or rewriting draft text | Seat boundary — Scribe writes, Judge scores | Return the fix instruction; Scribe applies it |
| Sharing provider family with Scribe | Architectural violation — shared training data = shared blind spots | Cross-family per `router.yaml`. If Scribe is Anthropic, Judge is Google/Groq/OpenAI |
| Skipping SFR on a deducted dimension | Audit trail is how Logician and Red Team verify the deduction is real | Full Premises/Trace/Conclusion on every dimension where score < max |
| Skipping CoT reasoning in a separate field | Mixing reasoning into the score line = halo bait for downstream consumers | CoT goes in the dedicated `cot_reasoning` JSON field. Score follows the reasoning, never precedes it |
| Mapping internal rubric to itself when funder weights differ | Scoring against weights the real reviewer won't use | Map proportionally to funder weights when they're published; flag the mapping ratio |
| Hardcoding a model name | Binding drifts when `router.yaml` updates; breaks sovereignty contract | Always resolve from `router.yaml` tilth.judge |
| Surfacing failure codes to the operator | Josh sees natural language; pipeline sees codes | `F-*` codes → `session_log.jsonl`. Operator sees plain English |

## Funder-specific discipline

| Anti-Pattern | Why it fails | Do instead |
|---|---|---|
| Scoring match/cost-share as "documented" without checking credibility | In-kind at inflated valuations sinks USDA/SBA applications | Verify in-kind valuations are defensible (FMV references, not aspirational); flag if not |
| Treating boilerplate letters of support as strong LOS | Every program officer recognizes form letters | Dim 9 deduction for LOS that don't name the specific project commitment (hours, resources, dollar value) |
| Scoring Evaluation Plan as present without data-sharing / IP / compliance provisions when funder requires them | Federal programs (NSF DMP, USDA data-sharing, NIH public access) score compliance plans as part of Eval | Check funder's data/IP/compliance requirements and score their absence as a Dim 11 deduction |
| Missing the responsiveness map | Reviewers check whether each numbered RFA question has a direct answer | Build RFA question → draft section map before scoring Dim 2. Any unmapped question = Dim 2 deduction |
| Ignoring budget narrative vs. budget table reconciliation | Reviewer-caught math error is a top deduction vector | Dim 10 requires narrative totals tie to SF-424A / funder budget form totals |
| Treating "equity impact" as a funder-independent criterion | Equity-scoring varies by funder; a baked-in equity score penalizes funders that don't ask for it | Let funder rubric drive equity scoring. Internal 12-dim handles it via Dim 4 (Significance/Need) when the funder doesn't have a dedicated criterion |

---

## Predicted failure modes (not yet observed; prevent proactively)

- **"Summary section substitutes for detail."** A strong executive summary can anchor every downstream dimension high. Score the detail sections independently; the summary is Dim 3 only.
- **"Appendix as get-out-of-jail-free."** Content in appendices doesn't substitute for content the RFA requires in the narrative. If the RFA says "Include X in the project description," X in Appendix B = Dim 2 deduction.
- **"Team size = qualifications."** A 12-person team with no relevant prior performance scores lower than a 3-person team with 3 closed-out federal awards. Dim 9 scores relevant track record, not headcount.

---

*v1 — 2026-04-20 — Initial externalization from judge_scoring_agent_v1.md §14. Added evidence discipline, funder-specific discipline, and predicted failure modes. Canonical reference for Judge; load on day-one session + compaction + new-grant-family transitions.*
