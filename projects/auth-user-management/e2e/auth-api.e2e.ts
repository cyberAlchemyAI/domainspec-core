import assert from "node:assert/strict";
import {
  authAccessControlSchema,
  authenticateRequestUseCase,
  authorizeRequestUseCase,
  createDrizzleAuthRepositories,
  createHmacTokenCodec,
  createMemoryAuthRepositories,
  createPbkdf2PasswordService,
  fixedClock,
  getPermissionCatalogUseCase,
  introspectTokenUseCase,
  issueAccessTokenUseCase,
  loginUseCase,
  logoutUseCase,
  seedSystemBootstrap,
  type AuthEvent,
  type IdGenerator,
} from "../src/index.js";
import {
  assertAuthError,
  assertNoSecretLeak,
  E2eScenarioRunner,
  redactSecrets,
} from "./assertions.js";
import {
  closeE2eSqlClient,
  createAuthDatabase,
  createE2eSqlClient,
  defaultE2eDatabaseUrl,
  type E2eSqlClient,
  resetAuthSchema,
} from "./postgres-schema.js";

const BASE_TIME = new Date("2026-06-21T12:00:00.000Z");
const DATABASE_URL = defaultE2eDatabaseUrl();
const TOKEN_SECRET =
  process.env.AUTH_E2E_TOKEN_SECRET ?? "auth-e2e-token-secret";
const SECRET_VALUES = [
  DATABASE_URL,
  "auth_e2e_password",
  TOKEN_SECRET,
  "admin-secret",
  "new-admin-secret",
  "runner-secret",
];

const AUTH_CONFIG = {
  sessionTtlMs: 60 * 60 * 1000,
  defaultTokenTtlSeconds: 300,
  minTokenTtlSeconds: 60,
  maxTokenTtlSeconds: 900,
};

async function main(): Promise<void> {
  const runner = new E2eScenarioRunner();
  const sql = createE2eSqlClient(DATABASE_URL);
  const db = createAuthDatabase(sql);

  try {
    await runner.scenario("bootstrap and catalog", async () => {
      await resetAuthSchema(sql);
      const repos = createDrizzleAuthRepositories(db);
      const passwordService = createE2ePasswordService();
      const consoleCalls = await captureConsoleLog(async () => {
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
                permissions: [
                  "auth-access-control.admin.*",
                  "auth-access-control.self.read",
                ],
              },
              {
                roleKey: "manager",
                displayName: "Manager",
                permissions: ["auth-access-control.admin.*"],
              },
              {
                roleKey: "billing",
                displayName: "Billing",
                permissions: ["billing.invoice.read"],
              },
            ],
          },
        );

        assert.deepEqual(result, {
          adminIdentifier: "admin",
          adminCreated: true,
          credentialRefreshed: false,
          passwordGenerated: false,
          grantsUpserted: 4,
        });

        const credential =
          await repos.principalRepo.findCredentialByIdentifier("admin");
        assert.ok(credential);
        assert.equal(credential.credentialHash.startsWith("pbkdf2:"), true);
        assert.equal(credential.credentialHash.includes("admin-secret"), false);
        assert.equal(
          await passwordService.verify("admin-secret", credential.credentialHash),
          true,
        );

        await seedSystemBootstrap(
          {
            principalRepo: repos.principalRepo,
            grantRepo: repos.grantRepo,
            passwordService,
          },
          {
            adminPassword: "new-admin-secret",
            roleDefinitions: [
              {
                roleKey: "admin",
                displayName: "Admin",
                permissions: [
                  "auth-access-control.admin.*",
                  "auth-access-control.self.read",
                ],
              },
              {
                roleKey: "manager",
                displayName: "Manager",
                permissions: ["auth-access-control.admin.*"],
              },
              {
                roleKey: "billing",
                displayName: "Billing",
                permissions: ["billing.invoice.read"],
              },
            ],
          },
        );

        assert.equal(await countRows(sql, "auth_permission_grants"), 4);
        const refreshed =
          await repos.principalRepo.findCredentialByIdentifier("admin");
        assert.ok(refreshed);
        assert.equal(
          await passwordService.verify(
            "new-admin-secret",
            refreshed.credentialHash,
          ),
          true,
        );

        const catalog = await getPermissionCatalogUseCase(repos.grantRepo)({
          namespace: "auth-access-control",
        });
        assert.deepEqual(
          catalog.permissions.map((permission) => permission.key).sort(),
          [
            "auth-access-control.admin.*",
            "auth-access-control.self.read",
          ],
        );
      });

      assertNoSecretLeak(consoleCalls, ["admin-secret", "new-admin-secret"]);
    });

    await runner.scenario("login success and token issuance", async () => {
      await resetAuthSchema(sql);
      const repos = createDrizzleAuthRepositories(db);
      const passwordService = createE2ePasswordService();
      const tokenCodec = createHmacTokenCodec(TOKEN_SECRET);
      const events: AuthEvent[] = [];
      const principalId = uuid(1);
      const sessionId = uuid(2);
      const tokenId = uuid(3);
      const secondTokenId = uuid(4);

      await repos.principalRepo.create({
        id: principalId,
        identifier: "runner@example.com",
        subjectType: "user",
        roleKeys: ["admin"],
        directPermissions: [
          "auth-access-control.self.read",
          "auth-access-control.self.read",
        ],
        credentialHash: await passwordService.hash("runner-secret"),
      });
      await repos.grantRepo.upsertGrant({
        granteeType: "role",
        granteeKey: "admin",
        permissionKey: "auth-access-control.admin.*",
        effect: "ALLOW",
      });

      const login = loginUseCase({
        ...repos,
        tokenCodec,
        passwordService,
        clock: fixedClock(BASE_TIME),
        idGenerator: sequenceIds([sessionId, tokenId]),
        config: AUTH_CONFIG,
        onEvent: (event) => {
          events.push(event);
        },
      });

      const result = await login({
        identifier: "runner@example.com",
        secret: "runner-secret",
        context: { ipReputation: "TRUSTED", hasUserAgent: true },
      });

      assert.equal(result.principalId, principalId);
      assert.equal(result.sessionId, sessionId);
      assert.equal(result.tokenId, tokenId);
      assert.deepEqual(result.permissions.sort(), [
        "auth-access-control.admin.*",
        "auth-access-control.self.read",
      ]);
      assert.deepEqual(
        events.map((event) => event.type),
        ["TokenIssued", "LoginSucceeded"],
      );
      assert.equal((await repos.sessionRepo.findById(sessionId))?.status, "ACTIVE");
      assert.deepEqual(
        (await repos.tokenRepo.findByTokenId(tokenId))?.scope.sort(),
        [
          "auth-access-control.admin.*",
          "auth-access-control.self.read",
        ],
      );

      const issueToken = issueAccessTokenUseCase({
        sessionRepo: repos.sessionRepo,
        tokenRepo: repos.tokenRepo,
        tokenCodec,
        clock: fixedClock(BASE_TIME),
        idGenerator: sequenceIds([secondTokenId]),
        config: AUTH_CONFIG,
      });
      const secondToken = await issueToken({
        sessionId,
        ttlSeconds: 120,
      });
      assert.equal(secondToken.tokenId, secondTokenId);
      assert.ok(await repos.tokenRepo.findByTokenId(secondTokenId));

      await assertAuthError("FORBIDDEN", () =>
        issueToken({ sessionId, ttlSeconds: 59 }),
      );
      await assertAuthError("FORBIDDEN", () =>
        issueToken({ sessionId, ttlSeconds: 901 }),
      );
      await assertAuthError("AUTH_REQUIRED", () =>
        issueToken({ sessionId: uuid(99), ttlSeconds: 120 }),
      );
      await repos.sessionRepo.updateStatus(sessionId, "TERMINATED");
      await assertAuthError("AUTH_REQUIRED", () =>
        issueToken({ sessionId, ttlSeconds: 120 }),
      );
    });

    await runner.scenario("login denial and risk policy", async () => {
      await resetAuthSchema(sql);
      const repos = createDrizzleAuthRepositories(db);
      const passwordService = createE2ePasswordService();
      const tokenCodec = createHmacTokenCodec(TOKEN_SECRET);

      await repos.principalRepo.create({
        id: uuid(10),
        identifier: "active@example.com",
        subjectType: "user",
        roleKeys: [],
        directPermissions: [],
        credentialHash: await passwordService.hash("runner-secret"),
      });
      await repos.principalRepo.create({
        id: uuid(11),
        identifier: "disabled@example.com",
        subjectType: "user",
        roleKeys: [],
        directPermissions: [],
        credentialHash: await passwordService.hash("runner-secret"),
      });
      await sql`
        update auth_principals
        set status = 'DISABLED'
        where identifier = 'disabled@example.com'
      `;

      const login = loginUseCase({
        ...repos,
        tokenCodec,
        passwordService,
        clock: fixedClock(BASE_TIME),
        idGenerator: sequenceIds([uuid(12), uuid(13)]),
        config: AUTH_CONFIG,
      });

      await assertAuthError("INVALID_CREDENTIALS", () =>
        login({ identifier: "", secret: "" }),
      );
      await assertAuthError("PRINCIPAL_DISABLED", () =>
        login({ identifier: "missing@example.com", secret: "runner-secret" }),
      );
      await assertAuthError("PRINCIPAL_DISABLED", () =>
        login({ identifier: "disabled@example.com", secret: "runner-secret" }),
      );
      await assertAuthError("INVALID_CREDENTIALS", () =>
        login({ identifier: "active@example.com", secret: "wrong" }),
      );
      await assertAuthError("FORBIDDEN", () =>
        login({
          identifier: "active@example.com",
          secret: "runner-secret",
          context: { ipReputation: "BLOCKED", hasUserAgent: true },
        }),
      );
      await assertAuthError("FORBIDDEN", () =>
        login({
          identifier: "active@example.com",
          secret: "runner-secret",
          context: { ipReputation: "TRUSTED", hasUserAgent: false },
        }),
      );
      await assertAuthError("FORBIDDEN", () =>
        login({
          identifier: "active@example.com",
          secret: "runner-secret",
          context: {
            ipReputation: "TRUSTED",
            failedAttemptsLast15m: 5,
            hasUserAgent: true,
          },
        }),
      );
    });

    await runner.scenario("authentication", async () => {
      await resetAuthSchema(sql);
      const repos = createDrizzleAuthRepositories(db);
      const passwordService = createE2ePasswordService();
      const tokenCodec = createHmacTokenCodec(TOKEN_SECRET);
      const principalId = uuid(20);

      await repos.principalRepo.create({
        id: principalId,
        identifier: "authn@example.com",
        subjectType: "user",
        roleKeys: [],
        directPermissions: ["auth-access-control.self.read"],
        credentialHash: await passwordService.hash("runner-secret"),
      });

      const firstLogin = await loginUseCase({
        ...repos,
        tokenCodec,
        passwordService,
        clock: fixedClock(BASE_TIME),
        idGenerator: sequenceIds([uuid(21), uuid(22)]),
        config: AUTH_CONFIG,
      })({
        identifier: "authn@example.com",
        secret: "runner-secret",
        context: { ipReputation: "TRUSTED", hasUserAgent: true },
      });

      const authenticate = authenticateRequestUseCase({
        sessionRepo: repos.sessionRepo,
        tokenRepo: repos.tokenRepo,
        tokenCodec,
        clock: fixedClock(BASE_TIME),
      });

      const authContext = await authenticate({
        authorizationHeader: `Bearer ${firstLogin.accessToken}`,
      });
      assert.equal(authContext.authContext.principalId, principalId);
      assert.equal(authContext.authContext.sessionId, firstLogin.sessionId);
      assert.equal(authContext.authContext.tokenId, firstLogin.tokenId);
      assert.deepEqual(authContext.authContext.permissions, [
        "auth-access-control.self.read",
      ]);

      await assertAuthError("AUTH_REQUIRED", () =>
        authenticate({ authorizationHeader: undefined }),
      );
      await assertAuthError("AUTH_REQUIRED", () =>
        authenticate({ authorizationHeader: "Basic abc" }),
      );
      await assertAuthError("INVALID_TOKEN", () =>
        authenticate({ authorizationHeader: "Bearer not-a-token" }),
      );

      const expired = await tokenCodec.sign(
        { sid: firstLogin.sessionId, jti: uuid(23) },
        {
          issuedAt: new Date(BASE_TIME.getTime() - 120_000),
          expiresInSeconds: 1,
        },
      );
      await assertAuthError("TOKEN_EXPIRED", () =>
        authenticate({ authorizationHeader: `Bearer ${expired}` }),
      );

      const unknown = await tokenCodec.sign(
        { sid: firstLogin.sessionId, jti: uuid(24) },
        { issuedAt: BASE_TIME, expiresInSeconds: 300 },
      );
      await assertAuthError("INVALID_TOKEN", () =>
        authenticate({ authorizationHeader: `Bearer ${unknown}` }),
      );

      await repos.tokenRepo.revoke(
        firstLogin.tokenId,
        BASE_TIME,
        "LOGOUT_TARGETED",
      );
      await assertAuthError("TOKEN_REVOKED", () =>
        authenticate({ authorizationHeader: `Bearer ${firstLogin.accessToken}` }),
      );

      const terminatedLogin = await loginUseCase({
        ...repos,
        tokenCodec,
        passwordService,
        clock: fixedClock(BASE_TIME),
        idGenerator: sequenceIds([uuid(25), uuid(26)]),
        config: AUTH_CONFIG,
      })({
        identifier: "authn@example.com",
        secret: "runner-secret",
        context: { ipReputation: "TRUSTED", hasUserAgent: true },
      });
      await repos.sessionRepo.updateStatus(
        terminatedLogin.sessionId,
        "TERMINATED",
      );
      await assertAuthError("AUTH_REQUIRED", () =>
        authenticate({
          authorizationHeader: `Bearer ${terminatedLogin.accessToken}`,
        }),
      );

      const expiredSessionLogin = await loginUseCase({
        ...repos,
        tokenCodec,
        passwordService,
        clock: fixedClock(BASE_TIME),
        idGenerator: sequenceIds([uuid(27), uuid(28)]),
        config: AUTH_CONFIG,
      })({
        identifier: "authn@example.com",
        secret: "runner-secret",
        context: { ipReputation: "TRUSTED", hasUserAgent: true },
      });
      await sql`
        update auth_sessions
        set expires_at = ${new Date(BASE_TIME.getTime() - 1000).toISOString()}
        where id = ${expiredSessionLogin.sessionId}
      `;
      await assertAuthError("AUTH_REQUIRED", () =>
        authenticate({
          authorizationHeader: `Bearer ${expiredSessionLogin.accessToken}`,
        }),
      );
    });

    await runner.scenario("authorization", async () => {
      await resetAuthSchema(sql);
      const repos = createDrizzleAuthRepositories(db);
      const principalId = uuid(30);
      const events: AuthEvent[] = [];
      const authorize = authorizeRequestUseCase({
        grantRepo: repos.grantRepo,
        clock: fixedClock(BASE_TIME),
        onEvent: (event) => {
          events.push(event);
        },
      });

      assert.equal(
        (
          await authorize({
            authContext: authContextFor(principalId, [
              "auth-access-control.self.read",
            ]),
            requiredPermission: "auth-access-control.self.read",
          })
        ).allowed,
        true,
      );
      assert.equal(
        (
          await authorize({
            authContext: authContextFor(principalId, [
              "auth-access-control.admin.*",
            ]),
            requiredPermission: "auth-access-control.admin.delete",
          })
        ).allowed,
        true,
      );

      await repos.grantRepo.upsertGrant({
        granteeType: "principal",
        granteeKey: principalId,
        permissionKey: "auth-access-control.admin.delete",
        effect: "DENY",
      });
      await assertAuthError("FORBIDDEN", () =>
        authorize({
          authContext: authContextFor(principalId, [
            "auth-access-control.admin.*",
          ]),
          requiredPermission: "auth-access-control.admin.delete",
        }),
      );
      assert.equal(events.at(-1)?.type, "AccessDenied");
      await assertAuthError("FORBIDDEN", () =>
        authorize({
          authContext: authContextFor(principalId, [
            "auth-access-control.admin.*",
          ]),
          requiredPermission: "bad-key",
        }),
      );
    });

    await runner.scenario("logout and revocation", async () => {
      await resetAuthSchema(sql);
      const repos = createDrizzleAuthRepositories(db);
      const passwordService = createE2ePasswordService();
      const tokenCodec = createHmacTokenCodec(TOKEN_SECRET);
      const events: AuthEvent[] = [];
      const principalId = uuid(40);

      await repos.principalRepo.create({
        id: principalId,
        identifier: "logout@example.com",
        subjectType: "user",
        roleKeys: [],
        directPermissions: ["auth-access-control.self.read"],
        credentialHash: await passwordService.hash("runner-secret"),
      });

      const login = (sessionId: string, tokenId: string) =>
        loginUseCase({
          ...repos,
          tokenCodec,
          passwordService,
          clock: fixedClock(BASE_TIME),
          idGenerator: sequenceIds([sessionId, tokenId]),
          config: AUTH_CONFIG,
        })({
          identifier: "logout@example.com",
          secret: "runner-secret",
          context: { ipReputation: "TRUSTED", hasUserAgent: true },
        });

      const targeted = await login(uuid(41), uuid(42));
      const logout = logoutUseCase({
        sessionRepo: repos.sessionRepo,
        tokenRepo: repos.tokenRepo,
        clock: fixedClock(BASE_TIME),
        config: AUTH_CONFIG,
        onEvent: (event) => {
          events.push(event);
        },
      });
      const targetedResult = await logout({
        sessionId: targeted.sessionId,
        callerId: principalId,
        callerPermissions: [],
        tokenId: targeted.tokenId,
      });
      assert.deepEqual(targetedResult.revokedTokenIds, [targeted.tokenId]);
      assert.equal(
        (await repos.tokenRepo.findByTokenId(targeted.tokenId))?.revokedAt?.toISOString(),
        BASE_TIME.toISOString(),
      );
      assert.equal(
        (await repos.sessionRepo.findById(targeted.sessionId))?.status,
        "TERMINATED",
      );

      const adminLogoutTarget = await login(uuid(43), uuid(44));
      const adminResult = await logout({
        sessionId: adminLogoutTarget.sessionId,
        callerId: uuid(400),
        callerPermissions: ["auth-access-control.admin.*"],
        tokenId: adminLogoutTarget.tokenId,
      });
      assert.deepEqual(adminResult.revokedTokenIds, [adminLogoutTarget.tokenId]);

      const forbiddenTarget = await login(uuid(45), uuid(46));
      await assertAuthError("FORBIDDEN", () =>
        logout({
          sessionId: forbiddenTarget.sessionId,
          callerId: uuid(401),
          callerPermissions: [],
          tokenId: forbiddenTarget.tokenId,
        }),
      );

      const allTokensTarget = await login(uuid(47), uuid(48));
      const second = await issueAccessTokenUseCase({
        sessionRepo: repos.sessionRepo,
        tokenRepo: repos.tokenRepo,
        tokenCodec,
        clock: fixedClock(BASE_TIME),
        idGenerator: sequenceIds([uuid(49)]),
        config: AUTH_CONFIG,
      })({
        sessionId: allTokensTarget.sessionId,
        ttlSeconds: 120,
      });
      const allResult = await logout({
        sessionId: allTokensTarget.sessionId,
        callerId: principalId,
        callerPermissions: [],
        revokeAllSessionTokens: true,
      });
      assert.deepEqual(allResult.revokedTokenIds.sort(), [
        allTokensTarget.tokenId,
        second.tokenId,
      ]);

      await assertAuthError("AUTH_REQUIRED", () =>
        logout({
          sessionId: uuid(404),
          callerId: principalId,
          callerPermissions: [],
        }),
      );
      await repos.sessionRepo.updateStatus(
        forbiddenTarget.sessionId,
        "TERMINATED",
      );
      await assertAuthError("AUTH_REQUIRED", () =>
        logout({
          sessionId: forbiddenTarget.sessionId,
          callerId: principalId,
          callerPermissions: ["auth-access-control.admin.*"],
        }),
      );
      const expiredTarget = await login(uuid(50), uuid(51));
      await repos.sessionRepo.updateStatus(expiredTarget.sessionId, "EXPIRED");
      await assertAuthError("AUTH_REQUIRED", () =>
        logout({
          sessionId: expiredTarget.sessionId,
          callerId: principalId,
          callerPermissions: [],
        }),
      );
      assert.ok(events.some((event) => event.type === "TokenRevoked"));
      assert.ok(events.some((event) => event.type === "LogoutCompleted"));
    });

    await runner.scenario("token introspection", async () => {
      await resetAuthSchema(sql);
      const repos = createDrizzleAuthRepositories(db);
      const passwordService = createE2ePasswordService();
      const tokenCodec = createHmacTokenCodec(TOKEN_SECRET);
      const principalId = uuid(60);

      await repos.principalRepo.create({
        id: principalId,
        identifier: "introspect@example.com",
        subjectType: "user",
        roleKeys: [],
        directPermissions: ["auth-access-control.self.read"],
        credentialHash: await passwordService.hash("runner-secret"),
      });

      const login = (sessionId: string, tokenId: string) =>
        loginUseCase({
          ...repos,
          tokenCodec,
          passwordService,
          clock: fixedClock(BASE_TIME),
          idGenerator: sequenceIds([sessionId, tokenId]),
          config: AUTH_CONFIG,
        })({
          identifier: "introspect@example.com",
          secret: "runner-secret",
          context: { ipReputation: "TRUSTED", hasUserAgent: true },
        });

      const active = await login(uuid(61), uuid(62));
      const introspect = introspectTokenUseCase({
        sessionRepo: repos.sessionRepo,
        tokenRepo: repos.tokenRepo,
        tokenCodec,
        clock: fixedClock(BASE_TIME),
      });

      assert.deepEqual(await introspect({ token: active.accessToken }), {
        active: true,
        principalId,
        exp: Math.floor((BASE_TIME.getTime() + 300_000) / 1000),
        iat: Math.floor(BASE_TIME.getTime() / 1000),
        scopes: ["auth-access-control.self.read"],
      });
      assert.equal(
        "scopes" in
          (await introspect({
            token: active.accessToken,
            includeScopes: false,
          })),
        false,
      );
      assert.equal(
        (await introspect({ token: "not-a-token" })).inactiveReason,
        "NOT_FOUND",
      );
      const unknown = await tokenCodec.sign(
        { sid: active.sessionId, jti: uuid(63) },
        { issuedAt: BASE_TIME, expiresInSeconds: 300 },
      );
      assert.equal(
        (await introspect({ token: unknown })).inactiveReason,
        "NOT_FOUND",
      );

      await repos.tokenRepo.revoke(active.tokenId, BASE_TIME, "LOGOUT_TARGETED");
      assert.equal(
        (await introspect({ token: active.accessToken })).inactiveReason,
        "TOKEN_REVOKED",
      );

      const expiredSessionId = uuid(64);
      const expiredTokenId = uuid(65);
      await repos.sessionRepo.create({
        id: expiredSessionId,
        principalId,
        status: "ACTIVE",
        effectivePermissions: [],
        createdAt: new Date(BASE_TIME.getTime() - 120_000),
        expiresAt: new Date(BASE_TIME.getTime() + 60_000),
      });
      await repos.tokenRepo.create({
        tokenId: expiredTokenId,
        sessionId: expiredSessionId,
        issuedAt: new Date(BASE_TIME.getTime() - 120_000),
        expiresAt: new Date(BASE_TIME.getTime() - 60_000),
        revokedAt: null,
        scope: [],
      });
      const expiredToken = await tokenCodec.sign(
        { sid: expiredSessionId, jti: expiredTokenId },
        {
          issuedAt: new Date(BASE_TIME.getTime() - 120_000),
          expiresInSeconds: 60,
        },
      );
      assert.equal(
        (await introspect({ token: expiredToken })).inactiveReason,
        "TOKEN_EXPIRED",
      );

      const terminated = await login(uuid(66), uuid(67));
      await repos.sessionRepo.updateStatus(terminated.sessionId, "TERMINATED");
      assert.equal(
        (await introspect({ token: terminated.accessToken })).inactiveReason,
        "SESSION_TERMINATED",
      );

      const expiredSession = await login(uuid(68), uuid(69));
      await repos.sessionRepo.updateStatus(expiredSession.sessionId, "EXPIRED");
      assert.equal(
        (await introspect({ token: expiredSession.accessToken })).inactiveReason,
        "SESSION_EXPIRED",
      );
    });

    await runner.scenario("public export smoke", async () => {
      assert.equal(typeof createMemoryAuthRepositories, "function");
      assert.equal(typeof createDrizzleAuthRepositories, "function");
      assert.equal(typeof authAccessControlSchema.authPrincipals, "object");
      assert.equal(typeof loginUseCase, "function");
      assert.equal(typeof authenticateRequestUseCase, "function");
      assert.equal(typeof authorizeRequestUseCase, "function");
      assert.equal(typeof logoutUseCase, "function");
      assert.equal(typeof introspectTokenUseCase, "function");
      assert.equal(typeof seedSystemBootstrap, "function");
    });

    console.log(runner.summary());
  } finally {
    await closeE2eSqlClient(sql);
  }
}

void main().catch((error: unknown) => {
  console.error(redactSecrets(formatError(error), SECRET_VALUES));
  process.exitCode = 1;
});

function createE2ePasswordService() {
  return createPbkdf2PasswordService({ iterations: 10_000 });
}

function sequenceIds(ids: string[]): IdGenerator {
  let index = 0;
  return {
    id() {
      const id = ids[index];
      index += 1;
      assert.ok(id, "No id left in sequence");
      return id;
    },
  };
}

function authContextFor(principalId: string, permissions: string[]) {
  return {
    principalId,
    sessionId: uuid(700),
    tokenId: uuid(701),
    permissions,
    issuedAt: BASE_TIME,
    expiresAt: new Date(BASE_TIME.getTime() + 300_000),
  };
}

function uuid(value: number): string {
  return `00000000-0000-4000-8000-${String(value).padStart(12, "0")}`;
}

async function captureConsoleLog(
  task: () => Promise<void>,
): Promise<unknown[]> {
  const originalLog = console.log;
  const calls: unknown[] = [];
  console.log = (...args: unknown[]) => {
    calls.push(args);
  };

  try {
    await task();
  } finally {
    console.log = originalLog;
  }

  return calls;
}

async function countRows(
  sql: E2eSqlClient,
  tableName: string,
): Promise<number> {
  const rows = await sql.unsafe(`select count(*)::int as count from ${tableName}`);
  const first = rows[0] as { count: number } | undefined;
  assert.ok(first, `No count returned for ${tableName}`);
  return Number(first.count);
}

function formatError(error: unknown): string {
  if (error instanceof Error) {
    return error.stack ?? error.message;
  }
  return String(error);
}
