import assert from "node:assert/strict";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { loadProjectNode } from "../../src/input/project-model.ts";
import { renderTypedRustOperation } from "../../src/typed-operation/rust.ts";
import type { TypedOperationClosureV1 } from "../../src/typed-operation/closure.ts";

const testDir = path.dirname(fileURLToPath(import.meta.url));
const authOperationSource = path.resolve(testDir, "../../../../../auth-foundation/implementation/operation-source");

function authClosure(): TypedOperationClosureV1 {
  return loadProjectNode(authOperationSource, "auth-exact-permission:authorize").typed_closure!;
}

function mutableClosure(): any {
  return structuredClone(authClosure());
}

function guardContract(closure: any): any {
  return closure.nodes.find((node: any) => node.selector === closure.operation.guard).typed_contract;
}

function findExpression(expression: any, op: string): any | null {
  if (expression.op === op) return expression;
  if (expression.op === "all" || expression.op === "any") {
    for (const term of expression.terms) {
      const found = findExpression(term, op);
      if (found !== null) return found;
    }
  } else if (expression.op === "not") return findExpression(expression.term, op);
  else if (expression.op === "exactly_one" || expression.op === "unique" || expression.op === "exists") return findExpression(expression.where, op);
  return null;
}

test("typed Rust guard lowering is deterministic, scoped, borrow-aware, and explicit about realized Rules", () => {
  const closure = authClosure();
  const first = renderTypedRustOperation(closure);
  const second = renderTypedRustOperation(closure);
  assert.equal(first, second);
  assert.match(first, /let __domainspec_rule_000 =/);
  assert.match(first, /__domainspec_rule_000 && \{/);
  assert.match(first, /\.filter\(\|session\| \{/);
  assert.match(first, /\.any\(\|role\| \{/);
  assert.match(first, /\.collect::<Vec<_>>\(\)\s+\.into_iter\(\)\s+\.collect::<BTreeSet<_>>\(\)/);
  assert.equal((first.match(/\.clone\(\)/g) ?? []).length, 1);
  assert.equal(first.includes(".to_owned()"), false);
  assert.equal(first.includes("DOMAINSPEC_RULE_BINDINGS"), false);
  assert.match(first, /pub const DOMAINSPEC_RULE_SELECTORS/);
  assert.match(first, /pub const DOMAINSPEC_RULE_IMPLEMENTATION_BINDINGS/);
  assert.match(first, /\("AF-RULE-ALLOW-IFF", "auth-exact-permission:allow-iff", "allow_iff"\)/);
  assert.equal(closure.rules.length, 8);
  assert.equal((first.match(/pub fn (?:allow_iff|authorization_admissible|complete_active_roles|default_deny|exact_active_role_grant|session_current|trusted_scope|unique_resolved_session)\(/g) ?? []).length, 8);
});

test("list projection remains a list until an authored to_set conversion", () => {
  const closure = mutableClosure();
  const completeRoles = closure.nodes.find((node: any) => node.selector === "auth-exact-permission:complete-active-roles").typed_contract;
  const setEquality = findExpression(completeRoles.expression, "set_equal");
  assert.equal(setEquality.right.op, "to_set");
  setEquality.right = setEquality.right.value;
  assert.throws(() => renderTypedRustOperation(closure), /set_equal operands are type-incompatible/);
});

test("all and any lower later terms behind their short-circuit operator", () => {
  const closure = mutableClosure();
  guardContract(closure).expression = {
    op: "any",
    terms: [
      { op: "eq", left: { op: "literal", type: "Bool", value: true }, right: { op: "literal", type: "Bool", value: true } },
      { op: "eq", left: { op: "literal", type: "Bool", value: false }, right: { op: "literal", type: "Bool", value: true } },
    ],
  };
  const rendered = renderTypedRustOperation(closure);
  assert.match(rendered, /let __domainspec_rule_001 = __domainspec_rule_000 \|\| \{/);
});

test("Rule references require exact named and typed arguments", () => {
  const missing = mutableClosure();
  const missingRef = findExpression(guardContract(missing).expression, "rule_ref");
  missingRef.arguments = [];
  assert.throws(() => renderTypedRustOperation(missing), /arguments do not exactly bind target parameters/);

  const wrongType = mutableClosure();
  const wrongTypeRef = findExpression(guardContract(wrongType).expression, "rule_ref");
  wrongTypeRef.arguments[0].value = { op: "literal", type: "Bool", value: true };
  assert.throws(() => renderTypedRustOperation(wrongType), /argument is type-incompatible/);
});

test("Rust lowering fails closed on normalized type-name collisions", () => {
  const closure = mutableClosure();
  const permission = closure.nodes.find((node: any) => node.selector === "auth-exact-permission:permission");
  closure.nodes.splice(closure.nodes.length - 1, 0, { ...structuredClone(permission), selector: "other-feature:permission" });
  assert.throws(() => renderTypedRustOperation(closure), /Rust type values collide after Rust identifier normalization/);
});

test("Rust literals use Rust escapes and reject unpaired UTF-16 surrogates", () => {
  const closure = mutableClosure();
  guardContract(closure).expression = {
    op: "eq",
    left: { op: "path", root: "context", properties: ["AUTH-EVALUATION-CONTEXT#request", "AUTH-AUTHORIZATION-REQUEST#scope_evidence_ref"] },
    right: { op: "literal", type: "String", value: "line\n\u0001\"\\é" },
  };
  assert.match(renderTypedRustOperation(closure), /line\\n\\u\{1\}\\\"\\\\é/);
  guardContract(closure).expression.right.value = "\ud800";
  assert.throws(() => renderTypedRustOperation(closure), /unpaired surrogate/);
});
