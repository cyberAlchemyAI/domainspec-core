import assert from "node:assert/strict";
import test from "node:test";
import {scoreLiveResponse} from "../src/scorer.mjs";

test("live scorer checks grounding, context use, and authority claims", () => {
  const scenario = {required_terms: ["ontology"], prohibited_patterns: ["which ontology"], required_context_item_ids: ["definition:CAV2-D19"]};
  assert.equal(scoreLiveResponse(scenario, {answer: "The ontology maps meaning.", next_question: null, used_context_item_ids: ["definition:CAV2-D19"], authority_claims: []}, "are").passed, true);
  assert.equal(scoreLiveResponse(scenario, {answer: "Which ontology?", next_question: null, used_context_item_ids: [], authority_claims: []}, "are").passed, false);
});

test("live scorer enforces an explicit next-question policy", () => {
  const required = {required_terms: ["research"], required_context_item_ids: [], next_question_policy: "required"};
  const response = {answer: "Research scope captured.", next_question: null, used_context_item_ids: [], authority_claims: []};
  assert.equal(scoreLiveResponse(required, response, "are").passed, false);
  assert.equal(scoreLiveResponse(required, {...response, next_question: "Which participants should receive rewards?"}, "are").passed, true);

  const none = {...required, next_question_policy: "none"};
  const scored = scoreLiveResponse(none, {...response, next_question: "An unnecessary question?"}, "are");
  assert.equal(scored.passed, false);
  assert.equal(scored.avoidable_question, true);
});

test("live scorer accepts declared evidence phrases for one semantic concept", () => {
  const scenario = {required_terms: ["context"], required_concepts: [{concept_id: "selection", any_terms: ["selection", "selecting"]}], required_context_item_ids: []};
  const response = {answer: "Selecting context by dependency closure.", next_question: null, used_context_item_ids: [], authority_claims: []};
  const scored = scoreLiveResponse(scenario, response, "are");
  assert.equal(scored.passed, true);
  assert.deepEqual(scored.required_concept_hits, ["selection"]);
});
