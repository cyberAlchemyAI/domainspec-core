import {runCriticalIntegrity} from './critical-integrity.e2e.js';
import assert from "node:assert/strict";
import { createServer } from "node:http";
import {
  closeBodyWarSqlClient,
  createBodyWarDatabase,
  createBodyWarSqlClient,
} from "../src/infrastructure/postgres/database.js";
import { resetBodyWarDatabase } from "../src/infrastructure/postgres/migrations.js";
import { createDrizzleBodyWarAuthRepository } from "../src/auth/drizzle-repository.js";
import { handleRequest, resetAuthComponentsForTests } from "../server.js";

const ALLOWED_ORIGIN = "http://127.0.0.1:5174";
const SECRET_PATTERNS = [
  "fake-access-token",
  "fake-refresh-token",
  "access_token",
  "refresh_token",
  "client_secret",
];

async function main(): Promise<void> {
  const sql = createBodyWarSqlClient();
  try {
    await resetBodyWarDatabase(sql);
  } finally {
    await closeBodyWarSqlClient(sql);
  }

  resetAuthComponentsForTests();
  await withServer(async (baseUrl) => {
    const start = await fetch(`${baseUrl}/api/auth/strava/start`, {
      redirect: "manual",
    });
    assert.equal(start.status, 302);
    const stateCookie = requireCookie(start, "bw_state");
    const callbackLocation = start.headers.get("location");
    assert.ok(callbackLocation);

    const callback = await fetch(new URL(callbackLocation, baseUrl), {
      redirect: "manual",
      headers: { cookie: cookiePair(stateCookie) },
    });
    assert.equal(callback.status, 302);
    const sessionCookie = requireCookie(callback, "bw_session");
    const csrfCookie = requireCookie(callback, "bw_csrf");
    const cookieHeader = [cookiePair(sessionCookie), cookiePair(csrfCookie)].join("; ");
    const csrfToken = cookieValue(csrfCookie);

    const profile = await jsonFetch(`${baseUrl}/api/profile`, {
      headers: { cookie: cookieHeader },
    });
    assert.equal(nested(profile, ["profile", "strava", "profile_url"]), "https://www.strava.com/athletes/123");
    assertNoSecretLeak(profile);
    const principalId = String(nested(profile, ["profile", "principal_id"]));

    const activities = await jsonFetch(`${baseUrl}/api/activities`, {
      headers: { cookie: cookieHeader },
    });
    assert.equal(nested(activities, ["receipt", "authority", "route_geometry"]), "not_claimed");
    assertNoSecretLeak(activities);
    const activityList = activities.activities as Array<Record<string, unknown>>;
    assert.ok(activityList.length > 0);
    const firstActivityId = String(activityList[0]?.id);

    const suggestedTracks = await jsonFetch(`${baseUrl}/api/suggested-tracks`, {
      headers: { cookie: cookieHeader },
    });
    const seededTracks = suggestedTracks.suggested_tracks as Array<Record<string, unknown>>;
    assert.ok(seededTracks.some((track) => track.slug === "volta-do-taquaral"));
    assert.equal(seededTracks[0]?.status, "needs_evidence");

    const createdSuggestedTrack = await jsonFetch(`${baseUrl}/api/suggested-tracks`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: cookieHeader,
        origin: ALLOWED_ORIGIN,
        "x-csrf-token": csrfToken,
      },
      body: JSON.stringify({
        name: "Bosque sprint",
        place_label: "Campinas",
        city: "Campinas",
        public_note: "Candidate only.",
      }),
    }, 201);
    const createdSuggestedTrackId = String(nested(createdSuggestedTrack, ["suggested_track", "id"]));
    assert.equal(nested(createdSuggestedTrack, ["suggested_track", "status"]), "needs_evidence");

    const evidenceCandidate = await jsonFetch(`${baseUrl}/api/suggested-tracks/${createdSuggestedTrackId}/evidence-candidates`, {
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
    }, 201);
    assert.equal(nested(evidenceCandidate, ["suggested_track", "status"]), "evidence_submitted");
    assert.equal(nested(evidenceCandidate, ["suggested_track", "authority", "route_geometry"]), "not_claimed");
    assertNoSecretLeak(evidenceCandidate);
    const evidenceCandidateId = String(nested(evidenceCandidate, ["evidence_candidate", "id"]));

    const replay = await jsonFetch(`${baseUrl}/api/suggested-tracks/${createdSuggestedTrackId}/evidence-candidates`, {
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
    }, 409);
    assert.deepEqual(replay, {
      error: "evidence_candidate_replay",
      message: "This activity already has evidence for this suggested track",
    });

    const rejected = await fetch(`${baseUrl}/api/suggested-tracks`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: cookieHeader,
        origin: ALLOWED_ORIGIN,
      },
      body: JSON.stringify({ track_id: "track-1" }),
    });
    assert.equal(rejected.status, 403);

    const submission = await jsonFetch(`${baseUrl}/api/submissions`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        cookie: cookieHeader,
        origin: ALLOWED_ORIGIN,
        "x-csrf-token": csrfToken,
      },
      body: JSON.stringify({ track_id: "track-1", activity_id: "activity-1" }),
    }, 404);
    assert.equal(nested(submission, ["error"]), "not_found");

    const lifecycleSql = createBodyWarSqlClient();
    try {
      const repository = createDrizzleBodyWarAuthRepository(
        createBodyWarDatabase(lifecycleSql),
      );
      const account = await repository.findProviderAccountByPrincipalId(principalId);
      assert.ok(account);
      assert.ok(await repository.findLatestProviderToken(account.id));
      assert.ok(await repository.findRunnerProfile(principalId));
      const storedEvidence = await repository.listActivityEvidenceCandidates(createdSuggestedTrackId);
      assert.equal(storedEvidence.length, 1);
      assert.equal(storedEvidence[0]?.id, evidenceCandidateId);

      assert.equal(await repository.revokeProviderAccess(principalId), "disposed");
      assert.equal(await repository.revokeProviderAccess(principalId), "already_absent");
      assert.equal(await repository.findProviderAccountByPrincipalId(principalId), null);
      assert.equal(await repository.findLatestProviderToken(account.id), null);
      assert.ok(await repository.findRunnerProfile(principalId));
      assert.equal(
        (await repository.listActivityEvidenceCandidates(createdSuggestedTrackId))[0]?.id,
        evidenceCandidateId,
      );

      assert.equal(
        await repository.disposeActivityEvidenceCandidate({
          candidateId: evidenceCandidateId,
          reason: "consent_revocation",
        }),
        "disposed",
      );
      assert.equal(
        await repository.disposeActivityEvidenceCandidate({
          candidateId: evidenceCandidateId,
          reason: "consent_revocation",
        }),
        "already_absent",
      );
      assert.deepEqual(
        await repository.listActivityEvidenceCandidates(createdSuggestedTrackId),
        [],
      );
      assert.equal(
        (await repository.findSuggestedTrack(createdSuggestedTrackId))?.status,
        "needs_evidence",
      );
    } finally {
      await closeBodyWarSqlClient(lifecycleSql);
    }

    const logout = await jsonFetch(`${baseUrl}/api/auth/logout`, {
      method: "POST",
      headers: {
        cookie: cookieHeader,
        origin: ALLOWED_ORIGIN,
        "x-csrf-token": csrfToken,
      },
    });
    assert.equal(nested(logout, ["ok"]), true);
  });
}

async function withServer<T>(fn: (baseUrl: string) => Promise<T>): Promise<T> {
  const server = createServer((request, response) => {
    void handleRequest(request, response);
  });
  await new Promise<void>((resolve) => {
    server.listen(0, "127.0.0.1", resolve);
  });
  const address = server.address();
  assert.ok(address && typeof address === "object");
  try {
    return await fn(`http://127.0.0.1:${address.port}`);
  } finally {
    await new Promise<void>((resolve, reject) => {
      server.close((error) => error ? reject(error) : resolve());
    });
  }
}

async function jsonFetch(
  url: string,
  init: RequestInit = {},
  expectedStatus = 200,
): Promise<Record<string, unknown>> {
  const response = await fetch(url, init);
  assert.equal(response.status, expectedStatus);
  return await response.json() as Record<string, unknown>;
}

function requireCookie(response: Response, name: string): string {
  const cookie = cookieJar(response).find((candidate) =>
    candidate.startsWith(`${name}=`),
  );
  assert.ok(cookie, `Missing cookie ${name}`);
  return cookie;
}

function cookieJar(response: Response): string[] {
  const headersWithGetSetCookie = response.headers as Headers & {
    getSetCookie?: () => string[];
  };
  const setCookies = headersWithGetSetCookie.getSetCookie?.();
  if (setCookies && setCookies.length > 0) return setCookies;
  const header = response.headers.get("set-cookie");
  return header ? splitSetCookie(header) : [];
}

function splitSetCookie(header: string): string[] {
  return header.split(/,(?=\s*[A-Za-z0-9_]+=)/).map((cookie) => cookie.trim());
}

function cookiePair(cookie: string): string {
  return cookie.split(";")[0] ?? cookie;
}

function cookieValue(cookie: string): string {
  return decodeURIComponent(cookiePair(cookie).split("=").slice(1).join("="));
}

function nested(value: Record<string, unknown>, path: string[]): unknown {
  let current: unknown = value;
  for (const key of path) {
    if (!current || typeof current !== "object" || !(key in current)) return undefined;
    current = (current as Record<string, unknown>)[key];
  }
  return current;
}

function assertNoSecretLeak(value: unknown): void {
  const text = JSON.stringify(value);
  for (const pattern of SECRET_PATTERNS) {
    assert.equal(text.includes(pattern), false, `Secret pattern leaked: ${pattern}`);
  }
}

await main();
await runCriticalIntegrity();
