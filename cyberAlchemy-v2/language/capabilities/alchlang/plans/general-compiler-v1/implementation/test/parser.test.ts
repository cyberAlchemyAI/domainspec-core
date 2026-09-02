import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { CompilationRejected, compileCarrier, parseDomainSource, parsePredicate } from "../src/index.js";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const examplePath = path.join(root, "examples/customer-approval.md");
const outboxExamplePath = path.join(root, "examples/outbox-operation.md");

test("textual Markdown parses and compiles into all generated artifacts", () => {
  const parsed = parseDomainSource(readFileSync(examplePath, "utf8"));
  const result = compileCarrier(parsed.carrier);
  assert.equal(parsed.source_kind, "markdown-alchlang");
  assert.equal(result.plan.model.domain_id, "customer-approval");
  assert.equal(result.plan.model.actions[0].id, "ReleaseCredit");
  assert.deepEqual(Object.keys(result.files).sort(), ["domain.events.ts", "domain.graph.json", "domain.machine.ts", "domain.schema.ts", "domain.test-obligations.json", "domain.tools.ts", "domain.types.ts", "traceability.json", "unsupported-residue.json"]);
});

test("predicate parser translates explicit textual comparisons", () => {
  const expression = parsePredicate("riskScore <= 472 and status == approved", new Map([["riskScore", "integer"], ["status", "string"]]));
  assert.deepEqual(expression, { operator: "and", operands: [
    { operator: "lte", operands: [{ node: "fact_ref", ref: "riskScore" }, { node: "literal", value_type: "integer", value: 472 }] },
    { operator: "eq", operands: [{ node: "fact_ref", ref: "status" }, { node: "literal", value_type: "string", value: "approved" }] }
  ] });
});

test("text source never defaults owner or domain", () => {
  assert.throws(() => parseDomainSource("entity Customer\n\nstate:\n  pending -> approved\n\nrule:\n  A customer with riskScore <= 472 is considered high-risk."), (error: unknown) => error instanceof CompilationRejected && error.issues.some((issue) => issue.code === "MISSING_OWNER") && error.issues.some((issue) => issue.code === "TEXT_REQUIRED"));
});

test("effect and performs syntax is explicit in the carrier", () => {
  const parsed = parseDomainSource(readFileSync(outboxExamplePath, "utf8"));
  const carrier = parsed.carrier as any;
  assert.deepEqual(carrier.effects[0], {
    effect_id: "PersistOrderWithOutbox",
    pattern_ref: "transactional-outbox",
    integration_binding_ref: "sqlite-transactional-outbox",
    write_refs: ["OrderOperation", "OutboxMessage"],
    event_refs: ["outbox-message-recorded"],
    guarantee: "atomic-state-and-outbox",
    failure_continuation: "rollback",
    authority_boundary_ref: "order-transaction-authority"
  });
  assert.deepEqual(carrier.actions[0].performs, [{ effect_ref: "PersistOrderWithOutbox", integration_binding_ref: "sqlite-transactional-outbox" }]);
});
