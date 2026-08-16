#!/usr/bin/env node

const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");

const [sheetArg, routeArg] = process.argv.slice(2);
if (!sheetArg || !routeArg) {
  process.stderr.write(
    "usage: validate-selector-bindings.cjs <dispatch-sheet.json> <DISPATCH-ROUTE.json>\n",
  );
  process.exit(2);
}

const root = process.cwd();
const sheetPath = path.relative(root, path.resolve(root, sheetArg)).replaceAll(path.sep, "/");
const routePath = path.relative(root, path.resolve(root, routeArg)).replaceAll(path.sep, "/");
const sheetBytes = fs.readFileSync(path.resolve(root, sheetArg));
const routeBytes = fs.readFileSync(path.resolve(root, routeArg));
const sheet = JSON.parse(sheetBytes);
const route = JSON.parse(routeBytes);
const sheetSha256 = crypto.createHash("sha256").update(sheetBytes).digest("hex");
const routeSha256 = crypto.createHash("sha256").update(routeBytes).digest("hex");

const expectedByRole = new Map([
  ["baseline-extractor", "baseline_extractor-agent-0"],
  ["candidate-m", "candidate_writers-agent-0"],
  ["candidate-e", "candidate_writers-agent-1"],
  ["candidate-q", "candidate_writers-agent-2"],
  ["audition-synthesizer", "audition_synthesizer-agent-0"],
  ["semantic-reviewer", "audition_reviewers-agent-0"],
  ["beginner-flow-reviewer", "audition_reviewers-agent-1"],
  ["findings-writer", "findings_writer-agent-0"],
  ["audition-auditor", "audition_auditor-agent-0"],
]);

const errors = [];
const rows = new Map();
for (const group of sheet.groups ?? []) {
  (group.agents ?? []).forEach((agent, index) => {
    rows.set(`${group.group_id}-agent-${index}`, { group, agent, index });
  });
}

if (!sheet.context?.includes("model value host-default is a declarative sentinel")) {
  errors.push("sheet context does not declare host-default model inheritance");
}
if (!sheet.context?.includes("token_budget value is an advisory output-length self-limit")) {
  errors.push("sheet context does not declare advisory token budgets");
}

const roles = route.subagent_strategy?.roles ?? [];
const seen = new Set();
const bindings = [];
for (const role of roles) {
  const expectedSelector = expectedByRole.get(role.role_id);
  if (!expectedSelector) {
    errors.push(`unexpected route role ${role.role_id}`);
    continue;
  }

  const expectedTarget = `${sheetPath}#${expectedSelector}`;
  if (role.capability_target !== expectedTarget) {
    errors.push(`${role.role_id} target mismatch: expected ${expectedTarget}`);
  }
  if (role.capability_ref !== "whisper") {
    errors.push(`${role.role_id} capability_ref is not whisper`);
  }
  if (!(role.input_refs ?? []).includes(sheetPath)) {
    errors.push(`${role.role_id} does not include the exact sheet as an input_ref`);
  }
  if (seen.has(expectedSelector)) {
    errors.push(`duplicate selector ${expectedSelector}`);
  }
  seen.add(expectedSelector);

  const selected = rows.get(expectedSelector);
  if (!selected) {
    errors.push(`${role.role_id} selector does not resolve: ${expectedSelector}`);
    continue;
  }
  const { group, agent, index } = selected;
  if (agent.model !== "host-default") {
    errors.push(`${expectedSelector} model must be host-default`);
  }
  if (!Number.isInteger(agent.token_budget) || agent.token_budget <= 0) {
    errors.push(`${expectedSelector} token_budget must be a positive advisory target`);
  }
  if (!agent.agent_name || !agent.initial_prompt) {
    errors.push(`${expectedSelector} is missing identity or initial_prompt`);
  }
  if ((group.agents?.length ?? 0) >= 2 && !agent.angle) {
    errors.push(`${expectedSelector} is missing its tension angle`);
  }

  bindings.push({
    role_id: role.role_id,
    selector: expectedSelector,
    group_id: group.group_id,
    agent_index: index,
    agent_name: agent.agent_name,
    model_policy: agent.model,
    advisory_token_budget: agent.token_budget,
    angle_bound: agent.angle !== undefined,
    initial_prompt_bound: true,
  });
}

for (const roleId of expectedByRole.keys()) {
  if (!roles.some((role) => role.role_id === roleId)) {
    errors.push(`missing route role ${roleId}`);
  }
}
for (const selector of rows.keys()) {
  if (!seen.has(selector)) {
    errors.push(`sheet row has no route selector: ${selector}`);
  }
}

const routeDigestBinding = `${sheetPath} at SHA-256 ${sheetSha256}.`;
if (!(route.subagent_strategy?.context ?? []).some((value) => value.includes(routeDigestBinding))) {
  errors.push("route context does not bind the exact current sheet digest");
}

const result = {
  schema: "domainspec.audition-selector-binding-validation.v1",
  status: errors.length === 0 ? "pass" : "block",
  sheet_path: sheetPath,
  sheet_sha256: sheetSha256,
  route_path: routePath,
  route_sha256: routeSha256,
  expected_binding_count: expectedByRole.size,
  resolved_binding_count: bindings.length,
  model_policy: "inherited-host-default",
  token_budget_policy: "advisory-output-length-self-limit-not-host-enforced",
  bindings,
  errors,
};

process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
process.exit(errors.length === 0 ? 0 : 2);
