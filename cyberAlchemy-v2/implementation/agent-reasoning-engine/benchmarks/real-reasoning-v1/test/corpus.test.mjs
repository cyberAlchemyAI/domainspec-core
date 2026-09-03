import assert from "node:assert/strict";
import test from "node:test";
import {loadBenchmark, validateMultiTurnCorpus} from "../src/corpus.mjs";
import {packageRoot} from "../src/common.mjs";

test("loads the versioned benchmark corpus", () => {
  const benchmark = loadBenchmark(packageRoot);
  assert.deepEqual(Object.fromEntries(Object.entries(benchmark.corpora).map(([key, rows]) => [key, rows.length])), {routing: 20, context: 10, lifecycle: 5, failure: 6, live: 6, live_multiturn: 4});
  assert.equal(benchmark.corpora.live_multiturn.every((scenario) => scenario.turns.length === 3), true);
});

test("rejects malformed or duplicate multi-turn contracts", () => {
  assert.throws(() => validateMultiTurnCorpus([{scenario_id: "bad", conversation_kind: "define", turns: [{turn_id: "same", request: "one", objective_kind: "define", required_terms: [], prohibited_patterns: [], required_context_item_ids: []}, {turn_id: "same", request: "two", objective_kind: "define", required_terms: [], prohibited_patterns: [], required_context_item_ids: []}]}]), /invalid turn/);
});
