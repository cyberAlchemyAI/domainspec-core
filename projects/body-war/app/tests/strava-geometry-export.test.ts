import assert from "node:assert/strict"
import { mkdtemp, readFile, rm, stat, writeFile } from "node:fs/promises"
import { tmpdir } from "node:os"
import { join } from "node:path"
import test from "node:test"
import {
  exportStravaGeometry,
  GeometryExportError,
} from "../src/geometry/export-strava-geometry.js"

const NOW = new Date("2026-08-13T12:00:00.000Z")

test("geometry exporter refreshes credentials and writes sanitized GeoJSON", async () => {
  await withTempDirectory(async (directory) => {
    const tokensPath = join(directory, "strava-tokens.json")
    const outputPath = join(directory, "geometry", "activities.geojson")
    const reportPath = join(directory, "geometry", "export-report.json")
    await writeJson(tokensPath, tokenStore({ expiresAt: 0 }), 0o644)

    const calls: string[] = []
    const fetchImpl = (async (input: string | URL | Request, init?: RequestInit) => {
      const url = String(input)
      calls.push(url)
      if (url === "https://www.strava.com/oauth/token") {
        assert.equal(init?.method, "POST")
        assert.match(String(init?.body), /grant_type=refresh_token/)
        return jsonResponse({
          access_token: "rotated-access-test",
          refresh_token: "rotated-refresh-test",
          expires_at: Math.floor(NOW.getTime() / 1000) + 21_600,
        })
      }
      if (url.includes("/athlete/activities")) {
        return jsonResponse([
          { id: 101, name: "Private activity name", sport_type: "Run", distance: 1000 },
          { id: 202, name: "Indoor activity", sport_type: "Workout", distance: 500 },
        ])
      }
      if (url.includes("/activities/101/streams")) {
        assert.equal(new Headers(init?.headers).get("authorization"), "Bearer rotated-access-test")
        return jsonResponse({
          latlng: {
            data: [[-22.9, -47.0], [-22.901, -47.001]],
            resolution: "high",
          },
          distance: { data: [0, 100] },
          time: { data: [0, 60] },
        })
      }
      if (url.includes("/activities/202/streams")) {
        return jsonResponse({
          distance: { data: [0, 50] },
          time: { data: [0, 30] },
        })
      }
      throw new Error(`Unexpected test URL: ${url}`)
    }) as typeof fetch

    const result = await exportStravaGeometry({
      tokensPath,
      outputPath,
      reportPath,
      clientId: "client-id-test",
      clientSecret: "client-secret-test",
      now: NOW,
      fetchImpl,
    })

    assert.deepEqual(
      {
        discovered: result.discovered,
        requested: result.requested,
        exported: result.exported,
        failed: result.failed,
        tokenRefreshed: result.tokenRefreshed,
      },
      { discovered: 2, requested: 2, exported: 1, failed: 1, tokenRefreshed: true },
    )
    assert.equal(calls.length, 4)

    const tokens = JSON.parse(await readFile(tokensPath, "utf8")) as {
      athletes: Record<string, { access_token: string; refresh_token: string }>
    }
    assert.equal(tokens.athletes.owner?.access_token, "rotated-access-test")
    assert.equal(tokens.athletes.owner?.refresh_token, "rotated-refresh-test")

    const geoJsonText = await readFile(outputPath, "utf8")
    const geoJson = JSON.parse(geoJsonText) as {
      features: Array<{
        id: string
        properties: Record<string, unknown>
        geometry: { coordinates: Array<[number, number]> }
      }>
    }
    assert.equal(geoJson.features.length, 1)
    assert.deepEqual(geoJson.features[0]?.geometry.coordinates[0], [-47, -22.9])
    assert.equal(geoJson.features[0]?.properties.authority, "exploratory_evidence")
    assert.equal(geoJson.features[0]?.properties.point_count, 2)
    assert.match(String(geoJson.features[0]?.properties.source_activity_ref), /^[a-f0-9]{24}$/)

    for (const forbidden of [
      "Private activity name",
      "expired-access-test",
      "refresh-before-test",
      "rotated-access-test",
      "rotated-refresh-test",
      "client-secret-test",
      "provider_activity_id",
    ]) {
      assert.equal(geoJsonText.includes(forbidden), false)
    }

    const report = JSON.parse(await readFile(reportPath, "utf8")) as {
      outcomes: Array<{ status: string; reason?: string }>
    }
    assert.deepEqual(report.outcomes.map((outcome) => outcome.status), ["exported", "failed"])
    assert.equal(report.outcomes[1]?.reason, "missing_latlng_stream")
    assert.equal(await fileMode(tokensPath), 0o600)
    assert.equal(await fileMode(outputPath), 0o600)
    assert.equal(await fileMode(reportPath), 0o600)
  })
})

test("submitted source fails before network access when IDs are fixtures", async () => {
  await withTempDirectory(async (directory) => {
    const submissionsPath = join(directory, "track-submissions.json")
    await writeJson(submissionsPath, {
      submissions: [{ activity_id: "activity-demo", track_id: "track-1" }],
    })
    let fetchCalled = false
    const fetchImpl = (async () => {
      fetchCalled = true
      throw new Error("network must not be called")
    }) as typeof fetch

    await assert.rejects(
      exportStravaGeometry({
        source: "submitted",
        submissionsPath,
        tokensPath: join(directory, "missing-tokens.json"),
        outputPath: join(directory, "activities.geojson"),
        reportPath: join(directory, "report.json"),
        clientId: "client-id-test",
        clientSecret: "client-secret-test",
        fetchImpl,
      }),
      (error: unknown) => error instanceof GeometryExportError &&
        error.code === "no_usable_provider_activity_ids",
    )
    assert.equal(fetchCalled, false)
  })
})

test("misaligned streams are reported without truncating evidence", async () => {
  await withTempDirectory(async (directory) => {
    const tokensPath = join(directory, "strava-tokens.json")
    const outputPath = join(directory, "activities.geojson")
    const reportPath = join(directory, "report.json")
    await writeJson(tokensPath, tokenStore({
      expiresAt: Math.floor(NOW.getTime() / 1000) + 7200,
    }))
    const fetchImpl = (async () => jsonResponse({
      latlng: { data: [[-22.9, -47.0], [-22.901, -47.001]] },
      distance: { data: [0] },
      time: { data: [0, 60] },
    })) as typeof fetch

    const result = await exportStravaGeometry({
      tokensPath,
      outputPath,
      reportPath,
      clientId: "client-id-test",
      clientSecret: "client-secret-test",
      activityIds: ["303"],
      now: NOW,
      fetchImpl,
    })

    assert.equal(result.exported, 0)
    assert.equal(result.failed, 1)
    const geoJson = JSON.parse(await readFile(outputPath, "utf8")) as { features: unknown[] }
    assert.deepEqual(geoJson.features, [])
    const report = JSON.parse(await readFile(reportPath, "utf8")) as {
      outcomes: Array<{ reason?: string }>
    }
    assert.equal(report.outcomes[0]?.reason, "unaligned_streams")
  })
})

test("empty activity discovery names the missing private-activity scope", async () => {
  await withTempDirectory(async (directory) => {
    const tokensPath = join(directory, "strava-tokens.json")
    await writeJson(tokensPath, tokenStore({
      expiresAt: Math.floor(NOW.getTime() / 1000) + 7200,
    }))
    const fetchImpl = (async () => jsonResponse([])) as typeof fetch

    await assert.rejects(
      exportStravaGeometry({
        tokensPath,
        outputPath: join(directory, "activities.geojson"),
        reportPath: join(directory, "report.json"),
        clientId: "client-id-test",
        clientSecret: "client-secret-test",
        now: NOW,
        fetchImpl,
      }),
      (error: unknown) => error instanceof GeometryExportError &&
        error.code === "no_activities_accessible_with_scope",
    )
  })
})

function tokenStore(input: { expiresAt: number }): Record<string, unknown> {
  return {
    athletes: {
      owner: {
        access_token: "expired-access-test",
        refresh_token: "refresh-before-test",
        expires_at: input.expiresAt,
        updated_at: 0,
        scope: "activity:read read",
        athlete: { id: 999 },
      },
    },
  }
}

function jsonResponse(value: unknown, status = 200): Response {
  return new Response(JSON.stringify(value), {
    status,
    headers: { "content-type": "application/json" },
  })
}

async function writeJson(path: string, value: unknown, mode?: number): Promise<void> {
  await writeFile(path, `${JSON.stringify(value, null, 2)}\n`, mode === undefined ? {} : { mode })
}

async function fileMode(path: string): Promise<number> {
  return (await stat(path)).mode & 0o777
}

async function withTempDirectory<T>(fn: (directory: string) => Promise<T>): Promise<T> {
  const directory = await mkdtemp(join(tmpdir(), "body-war-geometry-"))
  try {
    return await fn(directory)
  } finally {
    await rm(directory, { recursive: true, force: true })
  }
}
