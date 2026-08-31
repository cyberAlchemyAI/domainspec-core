import assert from "node:assert/strict"
import { createServer } from "node:http"
import test from "node:test"
import {
  authComponents,
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
    const principalId = String(nested(profileJson, ["profile", "principal_id"]))
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
    const activityList = activitiesJson.activities as Array<Record<string, unknown>>
    assert.ok(activityList.length > 0)
    const firstActivityId = String(activityList[0]?.id)

    const suggestedTracks = await fetch(`${baseUrl}/api/suggested-tracks`, {
      headers: { cookie: cookieHeader },
    })
    assert.equal(suggestedTracks.status, 200)
    const suggestedTracksJson = await suggestedTracks.json() as Record<string, unknown>
    const seededTracks = suggestedTracksJson.suggested_tracks as Array<Record<string, unknown>>
    assert.ok(seededTracks.some((track) => track.slug === "volta-do-taquaral"))
    assert.equal(seededTracks[0]?.status, "needs_evidence")

    const suggestedTrackCsrfRejected = await fetch(`${baseUrl}/api/suggested-tracks`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: cookieHeader,
        origin: ALLOWED_ORIGIN,
      },
      body: JSON.stringify({ name: "Lago extra", place_label: "Taquaral", city: "Campinas" }),
    })
    assert.equal(suggestedTrackCsrfRejected.status, 403)

    const createdSuggestedTrack = await fetch(`${baseUrl}/api/suggested-tracks`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: cookieHeader,
        origin: ALLOWED_ORIGIN,
        "x-csrf-token": csrfToken,
      },
      body: JSON.stringify({
        name: "Lago extra",
        place_label: "Parque Portugal",
        city: "Campinas",
        distance_hint_meters: 3200,
        public_note: "Precisa de evidencia antes de qualquer geometria.",
      }),
    })
    assert.equal(createdSuggestedTrack.status, 201)
    const createdSuggestedTrackJson = await createdSuggestedTrack.json() as Record<string, unknown>
    const createdSuggestedTrackId = String(nested(createdSuggestedTrackJson, ["suggested_track", "id"]))
    assert.equal(nested(createdSuggestedTrackJson, ["suggested_track", "status"]), "needs_evidence")
    assert.equal(nested(createdSuggestedTrackJson, ["suggested_track", "authority", "route_geometry"]), "not_claimed")

    const missingConsent = await fetch(`${baseUrl}/api/suggested-tracks/${createdSuggestedTrackId}/evidence-candidates`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: cookieHeader,
        origin: ALLOWED_ORIGIN,
        "x-csrf-token": csrfToken,
      },
      body: JSON.stringify({ activity_id: firstActivityId }),
    })
    assert.equal(missingConsent.status, 400)
    assert.equal(nested(await missingConsent.json() as Record<string, unknown>, ["error"]), "consent_required")

    const evidenceCandidate = await fetch(`${baseUrl}/api/suggested-tracks/${createdSuggestedTrackId}/evidence-candidates`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: cookieHeader,
        origin: ALLOWED_ORIGIN,
        "x-csrf-token": csrfToken,
      },
      body: JSON.stringify({
        activity_id: firstActivityId,
        consent_acknowledged: true,
        consent_text: "Store only the redacted activity summary.",
      }),
    })
    assert.equal(evidenceCandidate.status, 201)
    const evidenceCandidateJson = await evidenceCandidate.json() as Record<string, unknown>
    assert.equal(JSON.stringify(evidenceCandidateJson).includes("access_token"), false)
    assert.equal(JSON.stringify(evidenceCandidateJson).includes("refresh_token"), false)
    assert.equal(nested(evidenceCandidateJson, ["suggested_track", "status"]), "evidence_submitted")
    assert.equal(nested(evidenceCandidateJson, ["suggested_track", "authority", "route_geometry"]), "not_claimed")
    assert.equal(nested(evidenceCandidateJson, ["evidence_candidate", "authority", "scoring"]), "not_claimed")
    assert.equal(nested(evidenceCandidateJson, ["evidence_candidate", "provider_activity_id"]), firstActivityId)
    assert.equal(nested(evidenceCandidateJson, ["evidence_candidate", "redacted_summary", "id"]), firstActivityId)

    const { bodyWarRepo, strava } = authComponents()
    assert.equal(
      (await bodyWarRepo.listActivityEvidenceCandidates(createdSuggestedTrackId, principalId)).length,
      1,
    )
    const originalListActivitySummaries = strava.listActivitySummaries
    let replayActivityLookups = 0
    strava.listActivitySummaries = async (replayPrincipalId, page, perPage) => {
      replayActivityLookups += 1
      return originalListActivitySummaries(replayPrincipalId, page, perPage)
    }
    const replay = await (async () => {
      try {
        return await fetch(`${baseUrl}/api/suggested-tracks/${createdSuggestedTrackId}/evidence-candidates`, {
          method: "POST",
          headers: {
            "content-type": "application/json",
            cookie: cookieHeader,
            origin: ALLOWED_ORIGIN,
            "x-csrf-token": csrfToken,
          },
          body: JSON.stringify({
            activity_id: firstActivityId,
            consent_acknowledged: true,
            consent_text: "Store only the redacted activity summary.",
          }),
        })
      } finally {
        strava.listActivitySummaries = originalListActivitySummaries
      }
    })()
    assert.equal(replay.status, 409)
    assert.deepEqual(await replay.json(), {
      error: "evidence_candidate_replay",
      message: "This activity already has evidence for this suggested track",
    })
    assert.equal(replayActivityLookups, 0)
    assert.equal(
      (await bodyWarRepo.listActivityEvidenceCandidates(createdSuggestedTrackId, principalId)).length,
      1,
    )

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
