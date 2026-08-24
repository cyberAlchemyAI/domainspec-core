import assert from "node:assert/strict"
import { mkdtemp, readFile, rm, stat, writeFile } from "node:fs/promises"
import { request as httpRequest } from "node:http"
import { createServer } from "node:net"
import { tmpdir } from "node:os"
import { join } from "node:path"
import test from "node:test"
import {
  buildStravaAuthorizationUrl,
  exchangeAndPersistAuthorization,
  startStravaReconnect,
  StravaReconnectError,
  validateLoopbackRedirectUri,
  validatePublicRedirectUri,
} from "../src/geometry/reconnect-strava.js"

const REDIRECT_URI = "http://127.0.0.1:5174/api/auth/strava/callback"

test("private reconnect URL makes broader scope and forced consent explicit", () => {
  const result = buildStravaAuthorizationUrl({
    clientId: "client-id-test",
    redirectUri: REDIRECT_URI,
    includePrivate: true,
    state: "state-test",
  })
  const url = new URL(result.url)
  assert.equal(result.requestedScope, "read,activity:read_all")
  assert.equal(url.searchParams.get("scope"), "read,activity:read_all")
  assert.equal(url.searchParams.get("approval_prompt"), "force")
  assert.equal(url.searchParams.get("state"), "state-test")
  assert.equal(url.searchParams.get("redirect_uri"), REDIRECT_URI)
})

test("reconnect refuses a non-loopback callback", () => {
  for (const [value, code] of [
    ["https://example.com/callback", "non_loopback_redirect_uri"],
    ["http://localhost:5174/api/auth/strava/callback", "non_loopback_redirect_uri"],
    ["http://127.0.0.1/api/auth/strava/callback", "invalid_redirect_port"],
    ["http://127.0.0.1:5174/other", "invalid_redirect_path"],
    ["http://127.0.0.1:5174/api/auth/strava/callback?x=1", "invalid_redirect_components"],
  ] as const) {
    assert.throws(
      () => validateLoopbackRedirectUri(value),
      (error: unknown) => error instanceof StravaReconnectError && error.code === code,
    )
  }
})

test("public callback requires standard HTTPS and the exact callback path", () => {
  const callback = "https://random-example.trycloudflare.com/api/auth/strava/callback"
  assert.equal(validatePublicRedirectUri(callback).toString(), callback)
  for (const [value, code] of [
    ["http://random-example.trycloudflare.com/api/auth/strava/callback", "invalid_public_redirect_uri"],
    ["https://127.0.0.1/api/auth/strava/callback", "invalid_public_redirect_host"],
    ["https://random-example.trycloudflare.com:8443/api/auth/strava/callback", "invalid_public_redirect_uri"],
    ["https://random-example.trycloudflare.com/other", "invalid_redirect_path"],
  ] as const) {
    assert.throws(
      () => validatePublicRedirectUri(value),
      (error: unknown) => error instanceof StravaReconnectError && error.code === code,
    )
  }

  const authorization = buildStravaAuthorizationUrl({
    clientId: "client-id-test",
    redirectUri: callback,
    includePrivate: true,
    state: "state-test",
  })
  assert.equal(new URL(authorization.url).searchParams.get("redirect_uri"), callback)
})

test("authorization exchange atomically replaces same-athlete token", async () => {
  await withTempDirectory(async (directory) => {
    const tokensPath = join(directory, "strava-tokens.json")
    await writeJson(tokensPath, {
      athletes: {
        "999": {
          athlete: { id: 999 },
          scope: "read activity:read",
          access_token: "old-access-test",
          refresh_token: "old-refresh-test",
          expires_at: 0,
          updated_at: 0,
        },
      },
    }, 0o644)
    const fetchImpl = (async (_input: string | URL | Request, init?: RequestInit) => {
      assert.equal(init?.method, "POST")
      assert.match(String(init?.body), /grant_type=authorization_code/)
      assert.match(String(init?.body), /redirect_uri=http%3A%2F%2F127.0.0.1%3A5174/)
      return jsonResponse({
        access_token: "new-access-test",
        refresh_token: "new-refresh-test",
        expires_at: 1_800_000_000,
        token_type: "Bearer",
        scope: "read activity:read_all",
        athlete: { id: 999, firstname: "Private name" },
      })
    }) as typeof fetch

    const result = await exchangeAndPersistAuthorization({
      code: "authorization-code-test",
      clientId: "client-id-test",
      clientSecret: "client-secret-test",
      redirectUri: REDIRECT_URI,
      requestedScope: "read,activity:read_all",
      tokensPath,
      fetchImpl,
      now: new Date("2026-08-13T12:00:00.000Z"),
    })

    assert.equal(result.acceptedScope, "read activity:read_all")
    const store = JSON.parse(await readFile(tokensPath, "utf8")) as {
      athletes: Record<string, { access_token: string; refresh_token: string; scope: string }>
    }
    assert.deepEqual(Object.keys(store.athletes), ["999"])
    assert.equal(store.athletes["999"]?.access_token, "new-access-test")
    assert.equal(store.athletes["999"]?.refresh_token, "new-refresh-test")
    assert.equal(store.athletes["999"]?.scope, "read activity:read_all")
    assert.equal((await stat(tokensPath)).mode & 0o777, 0o600)
  })
})

test("different athlete or denied private scope leaves token store unchanged", async () => {
  await withTempDirectory(async (directory) => {
    for (const scenario of ["different-athlete", "missing-scope"] as const) {
      const tokensPath = join(directory, `${scenario}.json`)
      const originalStore = {
        athletes: {
          "999": {
            athlete: { id: 999 },
            scope: "read activity:read",
            access_token: "old-access-test",
            refresh_token: "old-refresh-test",
            expires_at: 0,
            updated_at: 0,
          },
        },
      }
      await writeJson(tokensPath, originalStore)
      const fetchImpl = (async () => jsonResponse({
        access_token: "new-access-test",
        refresh_token: "new-refresh-test",
        expires_at: 1_800_000_000,
        token_type: "Bearer",
        scope: scenario === "missing-scope" ? "read activity:read" : "read activity:read_all",
        athlete: { id: scenario === "different-athlete" ? 123 : 999 },
      })) as typeof fetch

      await assert.rejects(
        exchangeAndPersistAuthorization({
          code: "authorization-code-test",
          clientId: "client-id-test",
          clientSecret: "client-secret-test",
          redirectUri: REDIRECT_URI,
          requestedScope: "read,activity:read_all",
          tokensPath,
          fetchImpl,
        }),
        (error: unknown) => error instanceof StravaReconnectError &&
          error.code === (scenario === "different-athlete"
            ? "athlete_mismatch"
            : "required_scope_not_granted"),
      )
      assert.deepEqual(JSON.parse(await readFile(tokensPath, "utf8")), originalStore)
    }
  })
})

test("explicit partner authorization appends a new athlete without changing the first", async () => {
  await withTempDirectory(async (directory) => {
    const tokensPath = join(directory, "strava-tokens.json")
    const originalAthlete = {
      athlete: { id: 999 },
      scope: "read activity:read",
      access_token: "old-access-test",
      refresh_token: "old-refresh-test",
      expires_at: 0,
      updated_at: 0,
    }
    await writeJson(tokensPath, { athletes: { "999": originalAthlete } }, 0o644)
    const fetchImpl = (async () => jsonResponse({
      access_token: "partner-access-test",
      refresh_token: "partner-refresh-test",
      expires_at: 1_800_000_000,
      token_type: "Bearer",
      scope: "read activity:read_all",
      athlete: { id: 123, firstname: "Private partner name" },
    })) as typeof fetch

    await exchangeAndPersistAuthorization({
      code: "partner-authorization-code-test",
      clientId: "client-id-test",
      clientSecret: "client-secret-test",
      redirectUri: REDIRECT_URI,
      requestedScope: "read,activity:read_all",
      tokensPath,
      addAthlete: true,
      fetchImpl,
      now: new Date("2026-08-13T12:00:00.000Z"),
    })

    const store = JSON.parse(await readFile(tokensPath, "utf8")) as {
      athletes: Record<string, {
        access_token: string
        refresh_token: string
        scope: string
      }>
    }
    assert.deepEqual(Object.keys(store.athletes).sort(), ["123", "999"])
    assert.deepEqual(store.athletes["999"], originalAthlete)
    assert.equal(store.athletes["123"]?.access_token, "partner-access-test")
    assert.equal(store.athletes["123"]?.scope, "read activity:read_all")
    assert.equal((await stat(tokensPath)).mode & 0o777, 0o600)
  })
})

test("add-athlete mode refuses to replace an already stored athlete", async () => {
  await withTempDirectory(async (directory) => {
    const tokensPath = join(directory, "strava-tokens.json")
    const originalStore = {
      athletes: {
        "999": {
          athlete: { id: 999 },
          scope: "read activity:read",
          access_token: "old-access-test",
          refresh_token: "old-refresh-test",
          expires_at: 0,
          updated_at: 0,
        },
      },
    }
    await writeJson(tokensPath, originalStore)
    const fetchImpl = (async () => jsonResponse({
      access_token: "replacement-access-test",
      refresh_token: "replacement-refresh-test",
      expires_at: 1_800_000_000,
      token_type: "Bearer",
      scope: "read activity:read_all",
      athlete: { id: 999 },
    })) as typeof fetch

    await assert.rejects(
      exchangeAndPersistAuthorization({
        code: "authorization-code-test",
        clientId: "client-id-test",
        clientSecret: "client-secret-test",
        redirectUri: REDIRECT_URI,
        requestedScope: "read,activity:read_all",
        tokensPath,
        addAthlete: true,
        fetchImpl,
      }),
      (error: unknown) => error instanceof StravaReconnectError &&
        error.code === "athlete_already_present",
    )
    assert.deepEqual(JSON.parse(await readFile(tokensPath, "utf8")), originalStore)
  })
})

test("selected athlete reconnect updates only that athlete in a multi-athlete store", async () => {
  await withTempDirectory(async (directory) => {
    const tokensPath = join(directory, "strava-tokens.json")
    const firstAthlete = {
      athlete: { id: 999 },
      scope: "read activity:read",
      access_token: "first-access-test",
      refresh_token: "first-refresh-test",
      expires_at: 0,
      updated_at: 0,
    }
    const secondAthlete = {
      athlete: { id: 123 },
      scope: "read activity:read",
      access_token: "second-old-access-test",
      refresh_token: "second-old-refresh-test",
      expires_at: 0,
      updated_at: 0,
    }
    await writeJson(tokensPath, { athletes: { "999": firstAthlete, "123": secondAthlete } })
    const fetchImpl = (async () => jsonResponse({
      access_token: "second-new-access-test",
      refresh_token: "second-new-refresh-test",
      expires_at: 1_800_000_000,
      token_type: "Bearer",
      scope: "read activity:read_all",
      athlete: { id: 123 },
    })) as typeof fetch

    await exchangeAndPersistAuthorization({
      code: "authorization-code-test",
      clientId: "client-id-test",
      clientSecret: "client-secret-test",
      redirectUri: REDIRECT_URI,
      requestedScope: "read,activity:read_all",
      tokensPath,
      athleteKey: "123",
      fetchImpl,
      now: new Date("2026-08-13T12:00:00.000Z"),
    })

    const store = JSON.parse(await readFile(tokensPath, "utf8")) as {
      athletes: Record<string, { access_token: string }>
    }
    assert.deepEqual(store.athletes["999"], firstAthlete)
    assert.equal(store.athletes["123"]?.access_token, "second-new-access-test")
  })
})

test("multi-athlete reconnect without a selector fails before token exchange", async () => {
  await withTempDirectory(async (directory) => {
    const tokensPath = join(directory, "strava-tokens.json")
    const originalStore = {
      athletes: {
        "999": { athlete: { id: 999 } },
        "123": { athlete: { id: 123 } },
      },
    }
    await writeJson(tokensPath, originalStore)
    let exchanges = 0
    const fetchImpl = (async () => {
      exchanges += 1
      return jsonResponse({})
    }) as typeof fetch

    await assert.rejects(
      exchangeAndPersistAuthorization({
        code: "authorization-code-test",
        clientId: "client-id-test",
        clientSecret: "client-secret-test",
        redirectUri: REDIRECT_URI,
        requestedScope: "read,activity:read_all",
        tokensPath,
        fetchImpl,
      }),
      (error: unknown) => error instanceof StravaReconnectError &&
        error.code === "ambiguous_token_store",
    )
    assert.equal(exchanges, 0)
    assert.deepEqual(JSON.parse(await readFile(tokensPath, "utf8")), originalStore)
  })
})

test("tunneled callback validates public Host and preserves single-use state", async () => {
  await withTempDirectory(async (directory) => {
    const tokensPath = join(directory, "strava-tokens.json")
    await writeJson(tokensPath, {
      athletes: {
        "999": {
          athlete: { id: 999 },
          scope: "read activity:read",
          access_token: "old-access-test",
          refresh_token: "old-refresh-test",
          expires_at: 0,
          updated_at: 0,
        },
      },
    })
    const port = await availablePort()
    let exchanges = 0
    const fetchImpl = (async () => {
      exchanges += 1
      return jsonResponse({
        access_token: "new-access-test",
        refresh_token: "new-refresh-test",
        expires_at: 1_800_000_000,
        token_type: "Bearer",
        scope: "read activity:read_all",
        athlete: { id: 999 },
      })
    }) as typeof fetch
    const redirectUri = `http://127.0.0.1:${port}/api/auth/strava/callback`
    const publicRedirectUri = "https://random-example.trycloudflare.com/api/auth/strava/callback"
    const session = await startStravaReconnect({
      clientId: "client-id-test",
      clientSecret: "client-secret-test",
      redirectUri,
      publicRedirectUri,
      tokensPath,
      includePrivate: true,
      state: "expected-state-test",
      timeoutMs: 5000,
      fetchImpl,
      now: new Date("2026-08-13T12:00:00.000Z"),
    })
    try {
      assert.equal(
        new URL(session.authorizationUrl).searchParams.get("redirect_uri"),
        publicRedirectUri,
      )
      const wrongHost = await localCallback(
        `${redirectUri}?state=expected-state-test&code=bad-code`,
        `127.0.0.1:${port}`,
      )
      assert.equal(wrongHost.status, 404)
      const invalid = await localCallback(
        `${redirectUri}?state=expected-state-test&state=duplicate&code=bad-code`,
        "random-example.trycloudflare.com",
      )
      assert.equal(invalid.status, 400)
      assert.equal(exchanges, 0)

      const valid = await localCallback(
        `${redirectUri}?state=expected-state-test&code=valid-code-test`,
        "random-example.trycloudflare.com",
      )
      assert.equal(valid.status, 200)
      assert.equal(valid.headers["cache-control"], "no-store")
      await session.completion
      assert.equal(exchanges, 1)
    } finally {
      await session.close()
    }
  })
})

function jsonResponse(value: unknown, status = 200): Response {
  return new Response(JSON.stringify(value), {
    status,
    headers: { "content-type": "application/json" },
  })
}

async function localCallback(
  url: string,
  host: string,
): Promise<{ status: number; headers: Record<string, string | string[] | undefined> }> {
  return await new Promise((resolve, reject) => {
    const target = new URL(url)
    const request = httpRequest({
      hostname: target.hostname,
      port: target.port,
      path: `${target.pathname}${target.search}`,
      method: "GET",
      headers: { host },
    }, (response) => {
      response.resume()
      response.once("end", () => resolve({
        status: response.statusCode ?? 0,
        headers: response.headers,
      }))
    })
    request.once("error", reject)
    request.end()
  })
}

async function writeJson(path: string, value: unknown, mode?: number): Promise<void> {
  await writeFile(path, `${JSON.stringify(value, null, 2)}\n`, mode === undefined ? {} : { mode })
}

async function withTempDirectory<T>(fn: (directory: string) => Promise<T>): Promise<T> {
  const directory = await mkdtemp(join(tmpdir(), "body-war-reconnect-"))
  try {
    return await fn(directory)
  } finally {
    await rm(directory, { recursive: true, force: true })
  }
}

async function availablePort(): Promise<number> {
  const server = createServer()
  await new Promise<void>((resolve, reject) => {
    server.once("error", reject)
    server.listen(0, "127.0.0.1", resolve)
  })
  const address = server.address()
  assert.ok(address && typeof address === "object")
  await new Promise<void>((resolve, reject) => {
    server.close((error) => error ? reject(error) : resolve())
  })
  return address.port
}
