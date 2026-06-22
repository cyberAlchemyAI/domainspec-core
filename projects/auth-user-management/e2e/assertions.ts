import assert from "node:assert/strict";
import { AuthValidationError } from "../src/index.js";

export class E2eScenarioRunner {
  private readonly passed: string[] = [];

  async scenario(
    name: string,
    task: () => Promise<void> | void,
  ): Promise<void> {
    try {
      await task();
      this.passed.push(name);
    } catch (error) {
      throw new Error(`Scenario failed: ${name}\n${formatUnknownError(error)}`);
    }
  }

  summary(): string {
    return `auth-user-management E2E passed ${this.passed.length} scenarios`;
  }
}

export async function assertAuthError(
  code: string,
  task: () => Promise<unknown>,
): Promise<void> {
  try {
    await task();
  } catch (error) {
    assert.ok(
      error instanceof AuthValidationError,
      `Expected AuthValidationError ${code}, received ${formatUnknownError(error)}`,
    );
    assert.equal(error.code, code);
    return;
  }

  assert.fail(`Expected AuthValidationError ${code}`);
}

export function assertNoSecretLeak(values: unknown[], secrets: string[]): void {
  const serialized = values
    .map((value) => {
      if (Array.isArray(value)) {
        return value.map(String).join(" ");
      }
      return String(value);
    })
    .join("\n");

  for (const secret of secrets) {
    if (secret.length > 0) {
      assert.equal(
        serialized.includes(secret),
        false,
        "Unexpected secret in console output",
      );
    }
  }
}

export function redactSecrets(value: string, secrets: string[]): string {
  let redacted = value;
  for (const secret of secrets) {
    if (secret.length > 0) {
      redacted = redacted.split(secret).join("<redacted>");
    }
  }
  return redacted.replace(
    /postgres:\/\/([^:]+):([^@]+)@/g,
    "postgres://$1:<redacted>@",
  );
}

function formatUnknownError(error: unknown): string {
  if (error instanceof Error) {
    return error.stack ?? error.message;
  }
  return String(error);
}
