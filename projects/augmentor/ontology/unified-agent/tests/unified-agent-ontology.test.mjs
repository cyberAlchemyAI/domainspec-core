import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  validatePackage,
  validateRelationBoundary
} from "../scripts/validate.mjs";

const ROOT = path.resolve(fileURLToPath(new URL("../", import.meta.url)));

const readJson = async (relativePath) => JSON.parse(await readFile(path.join(ROOT, relativePath), "utf8"));

test("source-bound unified-agent package validates", async () => {
  const receipt = await validatePackage();
  assert.equal(receipt.status, "pass", receipt.violations.join("\n"));
  assert.deepEqual(receipt.counts, {
    sources: 25,
    nodes: 22,
    relations: 28,
    views: 5,
    residue: 7
  });
});

test("all five interpretive views are populated", async () => {
  const profile = await readJson("profile.json");
  assert.deepEqual(
    profile.views.map((view) => view.view_role).sort(),
    ["bridge", "evidence", "meaning", "system", "system"]
  );
  for (const descriptor of profile.views) {
    const view = await readJson(descriptor.path);
    assert.ok(view.node_refs.length >= 7, `${descriptor.id} should contain a useful node slice`);
    assert.ok(view.relation_refs.length >= 5, `${descriptor.id} should contain bridge relations`);
    assert.ok(view.sequences.length >= 1, `${descriptor.id} should contain a readable sequence`);
    assert.ok(view.forbidden_authority_moves.length >= 4);
  }
});

test("valid boundary fixture names the non-collapse invariants", async () => {
  const fixture = await readJson("fixtures/valid-boundaries.json");
  assert.equal(fixture.expected, "pass");
  for (const required of [
    "ConversationThread != Run",
    "IntentRouteRequest != ReasoningRequest",
    "RouteCatalogProjection != DisposableSemanticIndex",
    "ResolverInvocation != Run",
    "RouteDisposition != RouteDecision",
    "RouteDisposition != JudgmentReceipt",
    "RouteDisposition != ApprovalRecord",
    "RouteDisposition != Dispatch",
    "StrategyProposal != ApprovalRecord",
    "LifecycleJoin != ResultConsumption",
    "ResultConsumption != MemoryIntakeRequest",
    "DisposableSemanticIndex != SourceRecord",
    "OntologyCandidate != AuthorityDecision",
    "JudgmentReceipt != ApprovalRecord"
  ]) {
    assert.ok(fixture.claims.includes(required), `missing ${required}`);
  }
});

test("authority-effect fixture fails closed", async () => {
  const fixture = await readJson("fixtures/invalid-authority-effect.json");
  const errors = validateRelationBoundary(fixture.relation);
  assert.equal(fixture.expected, "fail");
  assert.match(errors.join("\n"), /authority_effect none/);
});

test("value-constraining cycle fixture fails closed", async () => {
  const fixture = await readJson("fixtures/invalid-value-cycle.json");
  const errors = validateRelationBoundary(fixture.relation);
  assert.equal(fixture.expected, "fail");
  assert.match(errors.join("\n"), /value-constraining cycle-permitted/);
});

test("profile blocks authority and product projection outputs", async () => {
  const profile = await readJson("profile.json");
  assert.equal(profile.status, "candidate-local");
  assert.equal(profile.authority_effect, "none");
  assert.equal(profile.release_admission, "not-granted");
  for (const output of [
    "authority-decision",
    "promotion-verdict",
    "canonical-write",
    "resonantos-projection",
    "release-admission"
  ]) {
    assert.ok(profile.blocked_outputs.includes(output), `missing blocked output ${output}`);
  }
});
