export type AuthTelemetry = {
  record?(event: string, attributes?: Record<string, string | number>): void;
};

export const noopAuthTelemetry: AuthTelemetry = {
  record: () => undefined,
};
