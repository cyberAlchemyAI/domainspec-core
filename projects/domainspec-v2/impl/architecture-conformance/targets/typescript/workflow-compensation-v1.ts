export const COMPENSATION_STATES = Object.freeze([
  "not-required",
  "requested",
  "running",
  "completed",
  "failed",
] as const);

export type CompensationState = (typeof COMPENSATION_STATES)[number];
export type CompensationFailureContinuation = "retry" | "escalate" | "terminal-failure";

export type CompensationMapping = Readonly<{
  stepId: string;
  operationId: string | null;
  dependsOn: readonly string[];
}>;

export type CompensationPlanEntry = Readonly<{
  stepId: string;
  operationId: string;
  dependsOn: readonly string[];
  idempotencyKey: string;
}>;

export type CompensationEvent = Readonly<{
  type:
    | "CompensationNotRequired"
    | "CompensationRequested"
    | "CompensationStarted"
    | "CompensationCompleted"
    | "CompensationFailed";
  workflowExecutionId: string;
  failedStepId: string;
  operationId: string | null;
  idempotencyKey: string | null;
  reason: string | null;
}>;

export type CompensationIntent = Readonly<{
  schemaVersion: "domainspec.workflow-compensation-intent/v1";
  workflowExecutionId: string;
  failedStepId: string;
  state: "not-required" | "requested";
  plan: readonly CompensationPlanEntry[];
  events: readonly CompensationEvent[];
}>;

export type CompensationOperationBinding = Readonly<{
  operationId: string;
  failureContinuation: CompensationFailureContinuation;
  execute: (idempotencyKey: string) => Promise<Readonly<{ ok: true }> | Readonly<{ ok: false; reason: string }>>;
}>;

export type CompensationExecutionOutcome = Readonly<{
  schemaVersion: "domainspec.workflow-compensation-outcome/v1";
  state: "not-required" | "completed" | "failed";
  executedOperationIds: readonly string[];
  failedOperationId: string | null;
  failureContinuation: CompensationFailureContinuation | null;
  events: readonly CompensationEvent[];
}>;

export class WorkflowCompensationError extends Error {
  constructor(readonly code: string, message: string) {
    super(message);
    this.name = "WorkflowCompensationError";
  }
}

function reject(code: string, message: string): never {
  throw new WorkflowCompensationError(code, message);
}

function requireIdentity(value: string, label: string): void {
  if (!/^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/.test(value)) {
    reject("COMPENSATION_IDENTITY_INVALID", `${label}:${value}`);
  }
}

function event(
  type: CompensationEvent["type"],
  workflowExecutionId: string,
  failedStepId: string,
  operationId: string | null,
  idempotencyKey: string | null,
  reason: string | null = null,
): CompensationEvent {
  return Object.freeze({ type, workflowExecutionId, failedStepId, operationId, idempotencyKey, reason });
}

export function planWorkflowCompensation(input: Readonly<{
  workflowExecutionId: string;
  failedStepId: string;
  completedStepIds: readonly string[];
  mappings: readonly CompensationMapping[];
}>): CompensationIntent {
  requireIdentity(input.workflowExecutionId, "workflowExecutionId");
  requireIdentity(input.failedStepId, "failedStepId");
  if (new Set(input.completedStepIds).size !== input.completedStepIds.length) {
    reject("COMPENSATION_COMPLETED_STEP_DUPLICATE", "completed step IDs must be unique");
  }

  const mappings = new Map<string, CompensationMapping>();
  for (const mapping of input.mappings) {
    requireIdentity(mapping.stepId, "mapping.stepId");
    if (mappings.has(mapping.stepId)) reject("COMPENSATION_MAPPING_DUPLICATE", mapping.stepId);
    if (mapping.operationId !== null) requireIdentity(mapping.operationId, "mapping.operationId");
    if (new Set(mapping.dependsOn).size !== mapping.dependsOn.length) {
      reject("COMPENSATION_DEPENDENCY_DUPLICATE", mapping.stepId);
    }
    for (const dependency of mapping.dependsOn) requireIdentity(dependency, "mapping.dependsOn");
    mappings.set(mapping.stepId, mapping);
  }

  const selected = [...input.completedStepIds].reverse().flatMap((stepId) => {
    requireIdentity(stepId, "completedStepId");
    const mapping = mappings.get(stepId);
    if (!mapping || mapping.operationId === null) return [];
    return [{ stepId, operationId: mapping.operationId, dependsOn: Object.freeze([...mapping.dependsOn]) }];
  });
  const operationIds = selected.map(({ operationId }) => operationId);
  if (new Set(operationIds).size !== operationIds.length) {
    reject("COMPENSATION_OPERATION_DUPLICATE", "one compensation Operation may occur only once in a plan");
  }

  if (selected.length === 0) {
    return Object.freeze({
      schemaVersion: "domainspec.workflow-compensation-intent/v1",
      workflowExecutionId: input.workflowExecutionId,
      failedStepId: input.failedStepId,
      state: "not-required",
      plan: Object.freeze([]),
      events: Object.freeze([event("CompensationNotRequired", input.workflowExecutionId, input.failedStepId, null, null)]),
    });
  }

  const selectedIds = new Set(operationIds);
  for (const item of selected) {
    for (const dependency of item.dependsOn) {
      if (dependency === item.operationId || !selectedIds.has(dependency)) {
        reject("COMPENSATION_DEPENDENCY_INVALID", `${item.operationId}:depends-on:${dependency}`);
      }
    }
  }

  const ordered: typeof selected = [];
  const pending = [...selected];
  const emitted = new Set<string>();
  while (pending.length > 0) {
    const index = pending.findIndex((item) => item.dependsOn.every((dependency) => emitted.has(dependency)));
    if (index < 0) reject("COMPENSATION_DEPENDENCY_CYCLE", "compensation dependency graph is cyclic");
    const [next] = pending.splice(index, 1);
    if (!next) reject("COMPENSATION_PLAN_INTERNAL", "missing selected compensation");
    ordered.push(next);
    emitted.add(next.operationId);
  }

  const plan = Object.freeze(ordered.map((item) => Object.freeze({
    ...item,
    idempotencyKey: `${input.workflowExecutionId}:${item.stepId}:${item.operationId}`,
  })));
  return Object.freeze({
    schemaVersion: "domainspec.workflow-compensation-intent/v1",
    workflowExecutionId: input.workflowExecutionId,
    failedStepId: input.failedStepId,
    state: "requested",
    plan,
    events: Object.freeze([event("CompensationRequested", input.workflowExecutionId, input.failedStepId, null, null)]),
  });
}

export async function executeWorkflowCompensation(
  intent: CompensationIntent,
  bindings: readonly CompensationOperationBinding[],
): Promise<CompensationExecutionOutcome> {
  if (intent.state === "not-required") {
    return Object.freeze({
      schemaVersion: "domainspec.workflow-compensation-outcome/v1",
      state: "not-required",
      executedOperationIds: Object.freeze([]),
      failedOperationId: null,
      failureContinuation: null,
      events: intent.events,
    });
  }

  const registry = new Map<string, CompensationOperationBinding>();
  for (const binding of bindings) {
    requireIdentity(binding.operationId, "binding.operationId");
    if (registry.has(binding.operationId)) reject("COMPENSATION_BINDING_DUPLICATE", binding.operationId);
    registry.set(binding.operationId, binding);
  }
  for (const item of intent.plan) {
    if (!registry.has(item.operationId)) {
      reject("COMPENSATION_BINDING_MISSING", item.operationId);
    }
  }

  const executed: string[] = [];
  const events: CompensationEvent[] = [...intent.events];
  for (const item of intent.plan) {
    const binding = registry.get(item.operationId);
    if (!binding) reject("COMPENSATION_BINDING_MISSING", item.operationId);
    events.push(event("CompensationStarted", intent.workflowExecutionId, intent.failedStepId, item.operationId, item.idempotencyKey));
    let outcome: Awaited<ReturnType<CompensationOperationBinding["execute"]>>;
    try {
      outcome = await binding.execute(item.idempotencyKey);
    } catch (error) {
      outcome = Object.freeze({ ok: false, reason: error instanceof Error ? error.message : "compensation-operation-threw" });
    }
    if (!outcome.ok) {
      events.push(event("CompensationFailed", intent.workflowExecutionId, intent.failedStepId, item.operationId, item.idempotencyKey, outcome.reason));
      return Object.freeze({
        schemaVersion: "domainspec.workflow-compensation-outcome/v1",
        state: "failed",
        executedOperationIds: Object.freeze([...executed]),
        failedOperationId: item.operationId,
        failureContinuation: binding.failureContinuation,
        events: Object.freeze(events),
      });
    }
    executed.push(item.operationId);
    events.push(event("CompensationCompleted", intent.workflowExecutionId, intent.failedStepId, item.operationId, item.idempotencyKey));
  }

  return Object.freeze({
    schemaVersion: "domainspec.workflow-compensation-outcome/v1",
    state: "completed",
    executedOperationIds: Object.freeze(executed),
    failedOperationId: null,
    failureContinuation: null,
    events: Object.freeze(events),
  });
}
