import assert from "node:assert/strict"
import { createServer } from "node:http"
import test from "node:test"
import {
  handleRequest,
  publicActivityImportReceipt,
  publicRunnerProfile,
  resetAuthComponentsForTests,
  stravaProfileUrl,
} from "../server.js"

const BASE_TIME = new Date("2026-06-21T12:00:00.000Z")
const ALLOWED_ORIGIN = "http://127.0.0.1:5174"

test("Body War local fake-Strava auth flow creates safe profile and cookies", async () => {
  resetAuthComponentsForTests()
  await withServer(async (baseUrl) => {
    const start = await fetch(`${baseUrl}/api/auth/strava/start`, {
      redirect: "manual",
    })
    assert.equal(start.status, 302)
    const stateCookie = cookieJar(start).find((cookie) => cookie.startsWith("bw_state="))
    assert.ok(stateCookie)
    const callbackLocation = start.headers.get("location")
    assert.ok(callbackLocation)

    const callback = await fetch(new URL(callbackLocation, baseUrl), {
      redirect: "manual",
      headers: { cookie: cookiePair(stateCookie) },
    })
    assert.equal(callback.status, 302)
    const callbackCookies = cookieJar(callback)
    const sessionCookie = callbackCookies.find((cookie) => cookie.startsWith("bw_session="))
    const csrfCookie = callbackCookies.find((cookie) => cookie.startsWith("bw_csrf="))
    assert.ok(sessionCookie)
    assert.ok(csrfCookie)
    const cookieHeader = [cookiePair(sessionCookie), cookiePair(csrfCookie)].join("; ")
    const csrfToken = cookieValue(csrfCookie)

    const profile = await fetch(`${baseUrl}/api/profile`, {
      headers: { cookie: cookieHeader },
    })
    assert.equal(profile.status, 200)
    const profileJson = await profile.json() as Record<string, unknown>
    assert.equal(JSON.stringify(profileJson).includes("fake-access-token"), false)
    assert.equal(JSON.stringify(profileJson).includes("fake-refresh-token"), false)
    assert.equal(
      nested(profileJson, ["profile", "strava", "profile_url"]),
      "https://www.strava.com/athletes/123",
    )

    const status = await fetch(`${baseUrl}/api/status`, {
      headers: { cookie: cookieHeader },
    })
    assert.equal(status.status, 200)
    assert.equal(nested(await status.json() as Record<string, unknown>, ["connected"]), true)

    const activities = await fetch(`${baseUrl}/api/activities`, {
      headers: { cookie: cookieHeader },
    })
    assert.equal(activities.status, 200)
    const activitiesJson = await activities.json() as Record<string, unknown>
    assert.equal(JSON.stringify(activitiesJson).includes("access_token"), false)
    assert.equal(nested(activitiesJson, ["receipt", "authority", "route_geometry"]), "not_claimed")

    const csrfRejected = await fetch(`${baseUrl}/api/submissions`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: cookieHeader,
        origin: ALLOWED_ORIGIN,
      },
      body: JSON.stringify({ track_id: "track-1" }),
    })
    assert.equal(csrfRejected.status, 403)
    assert.equal(nested(await csrfRejected.json() as Record<string, unknown>, ["error"]), "csrf_required")

    const originRejected = await fetch(`${baseUrl}/api/submissions`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: cookieHeader,
        origin: "https://example.invalid",
        "x-csrf-token": csrfToken,
      },
      body: JSON.stringify({ track_id: "track-1" }),
    })
    assert.equal(originRejected.status, 403)
    assert.equal(nested(await originRejected.json() as Record<string, unknown>, ["error"]), "origin_not_allowed")

    const submission = await fetch(`${baseUrl}/api/submissions`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: cookieHeader,
        origin: ALLOWED_ORIGIN,
        "x-csrf-token": csrfToken,
      },
      body: JSON.stringify({
        track_id: "track-1",
        activity_id: "activity-1",
        activity_name: "Redacted Run",
      }),
    })
    assert.equal(submission.status, 201)

    const logout = await fetch(`${baseUrl}/api/auth/logout`, {
      method: "POST",
      headers: {
        cookie: cookieHeader,
        origin: ALLOWED_ORIGIN,
        "x-csrf-token": csrfToken,
      },
    })
    assert.equal(logout.status, 200)
    assert.equal(nested(await logout.json() as Record<string, unknown>, ["ok"]), true)
  })
})

test("Body War public runner profile exposes Strava link without provider tokens", () => {
  assert.equal(stravaProfileUrl("123"), "https://www.strava.com/athletes/123")
  assert.equal(stravaProfileUrl("not-an-athlete-id"), null)

  const profile = publicRunnerProfile({
    auth: {
      principalId: "strava:123",
      sessionId: "session-1",
      permissions: ["body-war.activity.read"],
      tokenId: "token-1",
      issuedAt: BASE_TIME,
      expiresAt: new Date(BASE_TIME.getTime() + 60_000),
    },
    profile: {
      principalId: "strava:123",
      displayName: "Ada Runner",
      privacyStatus: "private",
      createdAt: BASE_TIME.toISOString(),
      updatedAt: BASE_TIME.toISOString(),
    },
    account: {
      id: "account-1",
      provider: "strava",
      principalId: "strava:123",
      providerUserId: "123",
      displayName: "Ada Runner",
      scope: ["read", "activity:read"],
      status: "linked",
      linkedAt: BASE_TIME.toISOString(),
      updatedAt: BASE_TIME.toISOString(),
      metadata: {
        athlete: {
          id: 123,
          firstname: "Ada",
          lastname: "Runner",
          access_token: "must-not-leak",
        },
      },
    },
  })

  assert.equal(
    profile.strava && typeof profile.strava === "object" && "profile_url" in profile.strava
      ? profile.strava.profile_url
      : null,
    "https://www.strava.com/athletes/123",
  )
  assert.equal(JSON.stringify(profile).includes("must-not-leak"), false)
})

test("Body War activity import receipt keeps route authority deferred", () => {
  const receipt = publicActivityImportReceipt({
    principalId: "strava:123",
    summaryCount: 2,
    importedAt: BASE_TIME.toISOString(),
  })

  assert.equal(receipt.summary_count, 2)
  assert.deepEqual(receipt.authority, {
    activity_summary: "imported",
    route_geometry: "not_claimed",
    scoring: "not_claimed",
  })
  assert.equal(JSON.stringify(receipt).includes("access_token"), false)
  assert.equal(JSON.stringify(receipt).includes("refresh_token"), false)
})

async function withServer<T>(fn: (baseUrl: string) => Promise<T>): Promise<T> {
  const server = createServer((request, response) => {
    void handleRequest(request, response)
  })
  await new Promise<void>((resolve) => {
    server.listen(0, "127.0.0.1", resolve)
  })
  const address = server.address()
  assert.ok(address && typeof address === "object")
  try {
    return await fn(`http://127.0.0.1:${address.port}`)
  } finally {
    await new Promise<void>((resolve, reject) => {
      server.close((error) => error ? reject(error) : resolve())
    })
  }
}

function cookieJar(response: Response): string[] {
  const headersWithGetSetCookie = response.headers as Headers & {
    getSetCookie?: () => string[]
  }
  const setCookies = headersWithGetSetCookie.getSetCookie?.()
  if (setCookies && setCookies.length > 0) return setCookies
  const header = response.headers.get("set-cookie")
  return header ? splitSetCookie(header) : []
}

function splitSetCookie(header: string): string[] {
  return header.split(/,(?=\\s*[A-Za-z0-9_]+=)/).map((cookie) => cookie.trim())
}

function cookiePair(cookie: string): string {
  return cookie.split(";")[0] ?? cookie
}

function cookieValue(cookie: string): string {
  return decodeURIComponent(cookiePair(cookie).split("=").slice(1).join("="))
}

function nested(value: Record<string, unknown>, path: string[]): unknown {
  let current: unknown = value
  for (const key of path) {
    if (!current || typeof current !== "object" || !(key in current)) return undefined
    current = (current as Record<string, unknown>)[key]
  }
  return current
}
