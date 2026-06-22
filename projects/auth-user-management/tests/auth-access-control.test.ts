import assert from "node:assert/strict";
import test from "node:test";
import {
  authPrincipals,
  createDrizzlePrincipalRepository,
  createHmacTokenCodec,
  createMemoryAuthRepositories,
  createPlainTextPasswordServiceForTests,
  createTrustedSessionUseCase,
  fixedClock,
  isTerminalSessionState,
  isTerminalTokenState,
  loginUseCase,
  authenticateRequestUseCase,
  authorizeRequestUseCase,
  logoutUseCase,
  introspectTokenUseCase,
  getPermissionCatalogUseCase,
  seedSystemBootstrap,
  transitionSession,
  transitionToken,
  validatePermissionKey,
  validateTokenExpiry,
  AuthValidationError,
  type AuthDrizzleDatabase,
  type AuthEvent,
  type IdGenerator,
} from "../src/index.js";

const BASE_TIME = new Date("2026-06-21T12:00:00.000Z");

test("login creates active session, resolves effective permissions, and authenticates bearer token", async () => {
  const idGenerator = sequenceIds([
    "session-1",
    "token-1",
  ]);
  const repos = createMemoryAuthRepositories({
    principals: [
      {
        id: "principal-1",
        identifier: "admin@example.com",
        subjectType: "user",
        status: "ACTIVE",
        roleKeys: ["admin"],
        directPermissions: ["auth-access-control.self.read"],
        credentialHash: "plain:correct-password",
      },
    ],
    grants: [
      {
        grantId: "grant-1",
        granteeType: "role",
        granteeKey: "admin",
        permissionKey: "auth-access-control.admin.*",
        effect: "ALLOW",
        createdAt: BASE_TIME,
      },
    ],
  });
  const events: AuthEvent[] = [];
  const tokenCodec = createHmacTokenCodec("test-secret");

  const result = await loginUseCase({
    ...repos,
    tokenCodec,
    passwordService: createPlainTextPasswordServiceForTests(),
    clock: fixedClock(BASE_TIME),
    idGenerator,
    onEvent: (event) => {
      events.push(event);
    },
  })({
    identifier: "admin@example.com",
    secret: "correct-password",
    context: { ipReputation: "TRUSTED", hasUserAgent: true },
  });

  assert.equal(result.sessionId, "session-1");
  assert.equal(result.tokenId, "token-1");
  assert.deepEqual(result.permissions.sort(), [
    "auth-access-control.admin.*",
    "auth-access-control.self.read",
  ]);
  assert.equal(result.expiresAt.toISOString(), "2026-06-21T13:00:00.000Z");
  assert.deepEqual(
    events.map((event) => event.type),
    ["TokenIssued", "LoginSucceeded"],
  );

  const authenticated = await authenticateRequestUseCase({
    sessionRepo: repos.sessionRepo,
    tokenRepo: repos.tokenRepo,
    tokenCodec,
    clock: fixedClock(BASE_TIME),
  })({ authorizationHeader: `Bearer ${result.accessToken}` });

  assert.equal(authenticated.authContext.principalId, "principal-1");
  assert.equal(authenticated.authContext.sessionId, "session-1");
  assert.equal(authenticated.authContext.tokenId, "token-1");
});

test("trusted session creates package session after external identity proof", async () => {
  const idGenerator = sequenceIds(["trusted-session-1", "trusted-token-1"]);
  const repos = createMemoryAuthRepositories({
    principals: [
      {
        id: "principal-trusted",
        identifier: "strava:123",
        subjectType: "user",
        status: "ACTIVE",
        roleKeys: ["runner"],
        directPermissions: ["body-war.profile.read"],
        credentialHash: "external:identity-proof",
      },
    ],
    grants: [
      {
        grantId: "grant-runner",
        granteeType: "role",
        granteeKey: "runner",
        permissionKey: "body-war.activity.read",
        effect: "ALLOW",
        createdAt: BASE_TIME,
      },
    ],
  });
  const tokenCodec = createHmacTokenCodec("test-secret");
  const events: AuthEvent[] = [];
  const telemetry: Array<{
    name: string;
    fields: Record<string, string | number> | undefined;
  }> = [];

  const result = await createTrustedSessionUseCase({
    ...repos,
    tokenCodec,
    clock: fixedClock(BASE_TIME),
    idGenerator,
    config: {
      sessionTtlMs: 3_600_000,
      defaultTokenTtlSeconds: 600,
      minTokenTtlSeconds: 60,
      maxTokenTtlSeconds: 900,
    },
    telemetry: {
      record(name, fields) {
        telemetry.push({ name, fields });
      },
    },
    onEvent: (event) => {
      events.push(event);
    },
  })({
    principalId: "principal-trusted",
    ttlSeconds: 120,
    metadata: { provider: "strava" },
  });

  assert.equal(result.sessionId, "trusted-session-1");
  assert.equal(result.tokenId, "trusted-token-1");
  assert.equal(result.principalId, "principal-trusted");
  assert.deepEqual(result.permissions.sort(), [
    "body-war.activity.read",
    "body-war.profile.read",
  ]);
  assert.equal((await repos.sessionRepo.findById(result.sessionId))?.status, "ACTIVE");
  assert.deepEqual(
    (await repos.tokenRepo.findByTokenId(result.tokenId))?.scope.sort(),
    ["body-war.activity.read", "body-war.profile.read"],
  );
  assert.deepEqual(events.map((event) => event.type), ["TokenIssued"]);
  assert.equal(telemetry.at(-1)?.name, "auth.trusted_session.completed");

  const authenticated = await authenticateRequestUseCase({
    sessionRepo: repos.sessionRepo,
    tokenRepo: repos.tokenRepo,
    tokenCodec,
    clock: fixedClock(BASE_TIME),
  })({ authorizationHeader: `Bearer ${result.accessToken}` });

  assert.equal(authenticated.authContext.principalId, "principal-trusted");
  assert.equal(authenticated.authContext.sessionId, "trusted-session-1");
});

test("trusted session rejects missing, disabled, and invalid ttl principals", async () => {
  const repos = createMemoryAuthRepositories({
    principals: [
      {
        id: "disabled-trusted",
        identifier: "strava:disabled",
        subjectType: "user",
        status: "DISABLED",
        roleKeys: [],
        directPermissions: [],
        credentialHash: "external:identity-proof",
      },
    ],
  });
  const trustedSession = createTrustedSessionUseCase({
    ...repos,
    tokenCodec: createHmacTokenCodec("test-secret"),
    clock: fixedClock(BASE_TIME),
    idGenerator: sequenceIds(["trusted-session-1", "trusted-token-1"]),
    config: {
      defaultTokenTtlSeconds: 300,
      minTokenTtlSeconds: 60,
      maxTokenTtlSeconds: 900,
    },
  });

  await assert.rejects(
    () => trustedSession({ principalId: "" }),
    matchesAuthError("AUTH_REQUIRED"),
  );
  await assert.rejects(
    () => trustedSession({ principalId: "missing" }),
    matchesAuthError("PRINCIPAL_DISABLED"),
  );
  await assert.rejects(
    () => trustedSession({ principalId: "disabled-trusted" }),
    matchesAuthError("PRINCIPAL_DISABLED"),
  );
  await assert.rejects(
    () => trustedSession({ principalId: "disabled-trusted", ttlSeconds: 10 }),
    matchesAuthError("PRINCIPAL_DISABLED"),
  );
});

test("login rejects missing credentials, disabled principals, invalid credentials, and risky contexts", async () => {
  const repos = createMemoryAuthRepositories({
    principals: [
      {
        id: "disabled-principal",
        identifier: "disabled@example.com",
        subjectType: "user",
        status: "DISABLED",
        roleKeys: [],
        directPermissions: [],
        credentialHash: "plain:secret",
      },
      {
        id: "active-principal",
        identifier: "active@example.com",
        subjectType: "user",
        status: "ACTIVE",
        roleKeys: [],
        directPermissions: [],
        credentialHash: "plain:secret",
      },
    ],
  });
  const login = loginUseCase({
    ...repos,
    tokenCodec: createHmacTokenCodec("test-secret"),
    passwordService: createPlainTextPasswordServiceForTests(),
    clock: fixedClock(BASE_TIME),
    idGenerator: sequenceIds(["session-1", "token-1"]),
  });

  await assert.rejects(
    () => login({ identifier: "", secret: "" }),
    matchesAuthError("INVALID_CREDENTIALS"),
  );
  await assert.rejects(
    () => login({ identifier: "disabled@example.com", secret: "secret" }),
    matchesAuthError("PRINCIPAL_DISABLED"),
  );
  await assert.rejects(
    () => login({ identifier: "active@example.com", secret: "wrong" }),
    matchesAuthError("INVALID_CREDENTIALS"),
  );
  await assert.rejects(
    () =>
      login({
        identifier: "active@example.com",
        secret: "secret",
        context: { ipReputation: "BLOCKED" },
      }),
    matchesAuthError("FORBIDDEN"),
  );
});

test("authenticate rejects missing, expired, revoked, unknown, and inactive-session tokens", async () => {
  const tokenCodec = createHmacTokenCodec("test-secret");
  const repos = createMemoryAuthRepositories({
    sessions: [
      {
        id: "session-1",
        principalId: "principal-1",
        status: "ACTIVE",
        effectivePermissions: [],
        createdAt: BASE_TIME,
        expiresAt: new Date(BASE_TIME.getTime() + 60_000),
      },
      {
        id: "session-terminated",
        principalId: "principal-1",
        status: "TERMINATED",
        effectivePermissions: [],
        createdAt: BASE_TIME,
        expiresAt: new Date(BASE_TIME.getTime() + 60_000),
      },
    ],
    tokens: [
      {
        tokenId: "revoked-token",
        sessionId: "session-1",
        issuedAt: BASE_TIME,
        expiresAt: new Date(BASE_TIME.getTime() + 60_000),
        revokedAt: BASE_TIME,
        scope: [],
      },
      {
        tokenId: "terminated-token",
        sessionId: "session-terminated",
        issuedAt: BASE_TIME,
        expiresAt: new Date(BASE_TIME.getTime() + 60_000),
        revokedAt: null,
        scope: [],
      },
    ],
  });
  const authenticate = authenticateRequestUseCase({
    sessionRepo: repos.sessionRepo,
    tokenRepo: repos.tokenRepo,
    tokenCodec,
    clock: fixedClock(BASE_TIME),
  });

  await assert.rejects(
    () => authenticate({ authorizationHeader: undefined }),
    matchesAuthError("AUTH_REQUIRED"),
  );

  const expired = await tokenCodec.sign(
    { sid: "session-1", jti: "expired-token" },
    { issuedAt: new Date(BASE_TIME.getTime() - 120_000), expiresInSeconds: 1 },
  );
  await assert.rejects(
    () => authenticate({ authorizationHeader: `Bearer ${expired}` }),
    matchesAuthError("TOKEN_EXPIRED"),
  );

  const unknown = await tokenCodec.sign(
    { sid: "session-1", jti: "unknown-token" },
    { issuedAt: BASE_TIME, expiresInSeconds: 60 },
  );
  await assert.rejects(
    () => authenticate({ authorizationHeader: `Bearer ${unknown}` }),
    matchesAuthError("INVALID_TOKEN"),
  );

  const revoked = await tokenCodec.sign(
    { sid: "session-1", jti: "revoked-token" },
    { issuedAt: BASE_TIME, expiresInSeconds: 60 },
  );
  await assert.rejects(
    () => authenticate({ authorizationHeader: `Bearer ${revoked}` }),
    matchesAuthError("TOKEN_REVOKED"),
  );

  const terminated = await tokenCodec.sign(
    { sid: "session-terminated", jti: "terminated-token" },
    { issuedAt: BASE_TIME, expiresInSeconds: 60 },
  );
  await assert.rejects(
    () => authenticate({ authorizationHeader: `Bearer ${terminated}` }),
    matchesAuthError("AUTH_REQUIRED"),
  );
});

test("authorization applies deny override and emits access denied events", async () => {
  const repos = createMemoryAuthRepositories({
    grants: [
      {
        grantId: "deny-1",
        granteeType: "principal",
        granteeKey: "principal-1",
        permissionKey: "auth-access-control.admin.delete",
        effect: "DENY",
        createdAt: BASE_TIME,
      },
    ],
  });
  const events: AuthEvent[] = [];
  const authorize = authorizeRequestUseCase({
    grantRepo: repos.grantRepo,
    clock: fixedClock(BASE_TIME),
    onEvent: (event) => {
      events.push(event);
    },
  });

  await assert.rejects(
    () =>
      authorize({
        authContext: {
          principalId: "principal-1",
          sessionId: "session-1",
          tokenId: "token-1",
          permissions: ["auth-access-control.admin.*"],
          issuedAt: BASE_TIME,
          expiresAt: new Date(BASE_TIME.getTime() + 60_000),
        },
        requiredPermission: "auth-access-control.admin.delete",
      }),
    matchesAuthError("FORBIDDEN"),
  );

  assert.equal(events[0]?.type, "AccessDenied");
  await assert.rejects(
    () =>
      authorize({
        authContext: {
          principalId: "principal-1",
          sessionId: "session-1",
          tokenId: "token-1",
          permissions: ["auth-access-control.admin.*"],
          issuedAt: BASE_TIME,
          expiresAt: new Date(BASE_TIME.getTime() + 60_000),
        },
        requiredPermission: "bad-key",
      }),
    matchesAuthError("FORBIDDEN"),
  );
});

test("logout revokes token evidence and terminates sessions", async () => {
  const repos = createMemoryAuthRepositories({
    sessions: [
      {
        id: "session-1",
        principalId: "principal-1",
        status: "ACTIVE",
        effectivePermissions: [],
        createdAt: BASE_TIME,
        expiresAt: new Date(BASE_TIME.getTime() + 60_000),
      },
    ],
    tokens: [
      {
        tokenId: "token-1",
        sessionId: "session-1",
        issuedAt: BASE_TIME,
        expiresAt: new Date(BASE_TIME.getTime() + 60_000),
        revokedAt: null,
        scope: [],
      },
    ],
  });

  const result = await logoutUseCase({
    sessionRepo: repos.sessionRepo,
    tokenRepo: repos.tokenRepo,
    clock: fixedClock(BASE_TIME),
  })({
    sessionId: "session-1",
    callerId: "principal-1",
    callerPermissions: [],
    tokenId: "token-1",
  });

  assert.deepEqual(result.revokedTokenIds, ["token-1"]);
  assert.equal((await repos.sessionRepo.findById("session-1"))?.status, "TERMINATED");
  assert.equal((await repos.tokenRepo.findByTokenId("token-1"))?.revokedAt?.toISOString(), BASE_TIME.toISOString());
});

test("token introspection reports active tokens and inactive reason precedence", async () => {
  const tokenCodec = createHmacTokenCodec("test-secret");
  const activeToken = await tokenCodec.sign(
    { sid: "session-1", jti: "token-1" },
    { issuedAt: BASE_TIME, expiresInSeconds: 60 },
  );
  const revokedToken = await tokenCodec.sign(
    { sid: "session-1", jti: "token-revoked" },
    { issuedAt: BASE_TIME, expiresInSeconds: 60 },
  );
  const repos = createMemoryAuthRepositories({
    sessions: [
      {
        id: "session-1",
        principalId: "principal-1",
        status: "ACTIVE",
        effectivePermissions: [],
        createdAt: BASE_TIME,
        expiresAt: new Date(BASE_TIME.getTime() + 60_000),
      },
    ],
    tokens: [
      {
        tokenId: "token-1",
        sessionId: "session-1",
        issuedAt: BASE_TIME,
        expiresAt: new Date(BASE_TIME.getTime() + 60_000),
        revokedAt: null,
        scope: ["auth-access-control.self.read"],
      },
      {
        tokenId: "token-revoked",
        sessionId: "session-1",
        issuedAt: BASE_TIME,
        expiresAt: new Date(BASE_TIME.getTime() - 1_000),
        revokedAt: BASE_TIME,
        scope: [],
      },
    ],
  });
  const introspect = introspectTokenUseCase({
    sessionRepo: repos.sessionRepo,
    tokenRepo: repos.tokenRepo,
    tokenCodec,
    clock: fixedClock(BASE_TIME),
  });

  assert.deepEqual(await introspect({ token: activeToken }), {
    active: true,
    principalId: "principal-1",
    exp: Math.floor((BASE_TIME.getTime() + 60_000) / 1000),
    iat: Math.floor(BASE_TIME.getTime() / 1000),
    scopes: ["auth-access-control.self.read"],
  });

  assert.equal(
    (await introspect({ token: revokedToken })).inactiveReason,
    "TOKEN_REVOKED",
  );
  assert.equal(
    (await introspect({ token: "not-a-token" })).inactiveReason,
    "NOT_FOUND",
  );
});

test("permission catalog deduplicates grants and supports namespace filtering", async () => {
  const repos = createMemoryAuthRepositories({
    grants: [
      grant("g1", "role", "admin", "auth-access-control.admin.*"),
      grant("g2", "role", "manager", "auth-access-control.admin.*"),
      grant("g3", "role", "admin", "billing.invoice.read"),
    ],
  });

  const result = await getPermissionCatalogUseCase(repos.grantRepo)({
    namespace: "auth-access-control",
  });

  assert.deepEqual(result.permissions, [
    {
      key: "auth-access-control.admin.*",
      description: "",
      status: "active",
    },
  ]);
});

test("lifecycle and validation helpers preserve copied domain behavior", () => {
  assert.equal(transitionSession("[new]", "LoginSucceeded"), "ACTIVE");
  assert.equal(transitionSession("ACTIVE", "LogoutCompleted"), "TERMINATED");
  assert.equal(isTerminalSessionState("EXPIRED"), true);
  assert.equal(transitionToken("[new]", "TokenIssued"), "ACTIVE");
  assert.equal(transitionToken("ACTIVE", "TokenRevoked"), "REVOKED");
  assert.equal(isTerminalTokenState("REVOKED"), true);
  assert.doesNotThrow(() =>
    validatePermissionKey("auth-access-control.admin.read"),
  );
  assert.throws(
    () => validatePermissionKey("not-canonical"),
    matchesAuthError("FORBIDDEN"),
  );
  assert.throws(
    () => validateTokenExpiry(BASE_TIME, BASE_TIME),
    matchesAuthError("INVALID_TOKEN"),
  );
});

test("bootstrap creates admin, syncs consumer-provided grants, and does not log plaintext", async () => {
  const repos = createMemoryAuthRepositories();
  const passwordService = createPlainTextPasswordServiceForTests();
  const logCalls: unknown[] = [];
  const originalLog = console.log;
  console.log = (...args: unknown[]) => {
    logCalls.push(args);
  };

  try {
    const result = await seedSystemBootstrap(
      {
        principalRepo: repos.principalRepo,
        grantRepo: repos.grantRepo,
        passwordService,
      },
      {
        adminPassword: "admin-secret",
        roleDefinitions: [
          {
            roleKey: "admin",
            displayName: "Admin",
            permissions: ["auth-access-control.admin.*"],
          },
        ],
      },
    );

    assert.deepEqual(result, {
      adminIdentifier: "admin",
      adminCreated: true,
      credentialRefreshed: false,
      passwordGenerated: false,
      grantsUpserted: 1,
    });
    assert.equal(logCalls.length, 0);
    assert.equal(
      (await repos.grantRepo.findAll()).at(0)?.permissionKey,
      "auth-access-control.admin.*",
    );
  } finally {
    console.log = originalLog;
  }
});

test("Drizzle repository maps auth principal rows and accepts injected database", async () => {
  const operations: Array<{ kind: string; table: unknown; value: unknown }> = [];
  const fakeDb: AuthDrizzleDatabase = {
    insert(table: unknown) {
      return {
        values(value: Record<string, unknown>) {
          operations.push({ kind: "insert", table, value });
          return {
            async returning() {
              return [
                {
                  id: "principal-db",
                  subjectType: value.subjectType,
                  status: value.status,
                  roleKeys: value.roleKeys,
                  directPermissions: value.directPermissions,
                  credentialHash: value.credentialHash,
                },
              ];
            },
          };
        },
      };
    },
    select() {
      throw new Error("not needed");
    },
    update() {
      throw new Error("not needed");
    },
  };

  const repo = createDrizzlePrincipalRepository(fakeDb);
  const principal = await repo.create({
    identifier: "admin@example.com",
    subjectType: "user",
    roleKeys: ["admin"],
    directPermissions: ["auth-access-control.self.read"],
    credentialHash: "hash",
  });

  assert.equal(principal.id, "principal-db");
  assert.equal(operations[0]?.table, authPrincipals);
  assert.deepEqual((operations[0]?.value as Record<string, unknown>).roleKeys, [
    "admin",
  ]);
});

function sequenceIds(ids: string[]): IdGenerator {
  let index = 0;
  return {
    id() {
      const id = ids[index];
      index += 1;
      if (!id) {
        throw new Error("No id left in sequence");
      }
      return id;
    },
  };
}

function matchesAuthError(code: string) {
  return (error: unknown): boolean =>
    error instanceof AuthValidationError && error.code === code;
}

function grant(
  grantId: string,
  granteeType: "role" | "principal",
  granteeKey: string,
  permissionKey: string,
) {
  return {
    grantId,
    granteeType,
    granteeKey,
    permissionKey,
    effect: "ALLOW" as const,
    createdAt: BASE_TIME,
  };
}
