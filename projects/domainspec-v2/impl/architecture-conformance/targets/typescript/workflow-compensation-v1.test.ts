import { describe, expect, it, vi } from "vitest";

import {
  executeWorkflowCompensation,
  planWorkflowCompensation,
  WorkflowCompensationError,
} from "./workflow-compensation-v1.js";

const mappings = Object.freeze([
  Object.freeze({ stepId: "reserve", operationId: "release-reservation", dependsOn: Object.freeze([]) }),
  Object.freeze({ stepId: "charge", operationId: "refund-payment", dependsOn: Object.freeze([]) }),
  Object.freeze({ stepId: "persist", operationId: "restore-settlement", dependsOn: Object.freeze([]) }),
]);

describe("Workflow compensation v1", () => {
  it("plans forward-recovery Operations in reverse completed-step order by default", () => {
    const intent = planWorkflowCompensation({
      workflowExecutionId: "settlement-run-1",
      failedStepId: "publish",
      completedStepIds: ["reserve", "charge", "persist"],
      mappings,
    });

    expect(intent.state).toBe("requested");
    expect(intent.plan.map(({ operationId }) => operationId)).toEqual([
      "restore-settlement",
      "refund-payment",
      "release-reservation",
    ]);
    expect(intent.plan[0]?.idempotencyKey).toBe("settlement-run-1:persist:restore-settlement");
  });

  it("honors explicit dependencies and uses reverse completion only as the tie-breaker", () => {
    const intent = planWorkflowCompensation({
      workflowExecutionId: "settlement-run-2",
      failedStepId: "publish",
      completedStepIds: ["reserve", "charge", "persist"],
      mappings: [
        mappings[0]!,
        mappings[1]!,
        Object.freeze({ ...mappings[2]!, dependsOn: Object.freeze(["release-reservation"]) }),
      ],
    });

    expect(intent.plan.map(({ operationId }) => operationId)).toEqual([
      "refund-payment",
      "release-reservation",
      "restore-settlement",
    ]);
  });

  it("preflights every binding, executes exact Operations, and exposes state transitions", async () => {
    const intent = planWorkflowCompensation({
      workflowExecutionId: "settlement-run-3",
      failedStepId: "publish",
      completedStepIds: ["reserve", "charge"],
      mappings,
    });
    const calls: string[] = [];
    const outcome = await executeWorkflowCompensation(intent, intent.plan.map(({ operationId }) => Object.freeze({
      operationId,
      failureContinuation: "escalate" as const,
      execute: async (idempotencyKey: string) => {
        calls.push(`${operationId}:${idempotencyKey}`);
        return Object.freeze({ ok: true as const });
      },
    })));

    expect(outcome.state).toBe("completed");
    expect(outcome.executedOperationIds).toEqual(["refund-payment", "release-reservation"]);
    expect(calls).toHaveLength(2);
    expect(outcome.events.map(({ type }) => type)).toEqual([
      "CompensationRequested",
      "CompensationStarted",
      "CompensationCompleted",
      "CompensationStarted",
      "CompensationCompleted",
    ]);
  });

  it("does not mutate before missing bindings are rejected", async () => {
    const intent = planWorkflowCompensation({
      workflowExecutionId: "settlement-run-4",
      failedStepId: "publish",
      completedStepIds: ["reserve", "charge"],
      mappings,
    });
    const execute = vi.fn(async () => Object.freeze({ ok: true as const }));

    await expect(executeWorkflowCompensation(intent, [{
      operationId: "refund-payment",
      failureContinuation: "retry",
      execute,
    }])).rejects.toMatchObject<Partial<WorkflowCompensationError>>({ code: "COMPENSATION_BINDING_MISSING" });
    expect(execute).not.toHaveBeenCalled();
  });

  it("stops at the first failed Operation and preserves its continuation", async () => {
    const intent = planWorkflowCompensation({
      workflowExecutionId: "settlement-run-5",
      failedStepId: "publish",
      completedStepIds: ["reserve", "charge"],
      mappings,
    });
    const outcome = await executeWorkflowCompensation(intent, [
      {
        operationId: "refund-payment",
        failureContinuation: "escalate",
        execute: async () => Object.freeze({ ok: false as const, reason: "gateway-unavailable" }),
      },
      {
        operationId: "release-reservation",
        failureContinuation: "retry",
        execute: vi.fn(async () => Object.freeze({ ok: true as const })),
      },
    ]);

    expect(outcome).toMatchObject({
      state: "failed",
      executedOperationIds: [],
      failedOperationId: "refund-payment",
      failureContinuation: "escalate",
    });
  });

  it("rejects cyclic dependency graphs", () => {
    expect(() => planWorkflowCompensation({
      workflowExecutionId: "settlement-run-6",
      failedStepId: "publish",
      completedStepIds: ["reserve", "charge"],
      mappings: [
        Object.freeze({ stepId: "reserve", operationId: "release-reservation", dependsOn: Object.freeze(["refund-payment"]) }),
        Object.freeze({ stepId: "charge", operationId: "refund-payment", dependsOn: Object.freeze(["release-reservation"]) }),
      ],
    })).toThrowError(expect.objectContaining({ code: "COMPENSATION_DEPENDENCY_CYCLE" }));
  });
});
