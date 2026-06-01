# Arm C — Highest-rated frontier LLM, rudimentary prompting (industry reference)

## Purpose

Industry-baseline reference. Tests what someone using ChatGPT / Claude / Gemini / etc. with a basic "write me a grant for X" prompt would produce — the realistic counterfactual for an applicant who chooses NOT to use a structured grant-writing system at all.

## System configuration

- **No Tilth pipeline.** Direct API call to the highest-rated frontier LLM at the time of each scenario execution (selected via a defensible benchmark — Chatbot Arena ELO + LMSYS leaderboard + recent task-specific evals, pinned at scenario-execution timestamp).
- **Rudimentary prompting only.** Single-turn or two-turn prompt with the scenario opportunity + a brief applicant description. No multi-section orchestration, no Logician gates, no Judge review pass, no Red Team adversarial review, no card-driven anything.
- Frontier-LLM identity + version + prompt text recorded in `pipeline/cards/eval/results/<scenario_slug>/arm_c/system_card.yaml` for reproducibility.

## Execution recipe

For each test scenario at `pipeline/cards/eval/scenarios/<slug>.yaml`:

1. Select the highest-rated frontier LLM per the pre-registered selection rubric (Chatbot Arena ELO at scenario-execution timestamp; tie-broken by recency of model release).
2. Construct the rudimentary prompt:
   ```
   Write a grant application for the following opportunity:
   <funder name + funder URL + opportunity description>

   The applicant is:
   <fictional applicant brief description from scenario>

   Produce a complete grant application.
   ```
3. Submit prompt, capture full response. No iteration, no follow-up turns, no editing pass.
4. Save artifact at `pipeline/cards/eval/results/<scenario_slug>/arm_c/`.
5. Strip applicant identity + system identity from draft before reviewer distribution (blinding).

## Why this arm matters

Without Arm C, a finding that "Arm B > Arm A" only tells us cards help vs. card-less Tilth. The funder + reviewer panel + skeptical operator all want to know: is Tilth + cards better than the realistic alternative someone might use instead? Arm C provides that comparison.

## What gets measured

Same rubric as Arms A + B. Per-dimension scores + rank-order preference + likelihood-of-funding judgment. The three-way comparison gives the full picture.

## Selection-rubric pre-registration

The "highest-rated frontier LLM" selection rubric is pre-registered before scenario execution to prevent post-hoc model-shopping. Selection criteria: (a) public benchmark leaderboard position, (b) availability via public API at scenario-execution time, (c) no Tilth-team affiliation or insider tuning. Pre-registration document at `pipeline/cards/eval/reviewer_panel/preregistration_arm_c_selection.md` (lands when study funding lands).
