import assert from "node:assert/strict";
import test from "node:test";
import { createMemoryBodyWarAuthRepository } from "../src/auth/memory-repository.js";
import {
  fetchStravaActivitySummaries,
  fetchStravaActivitySummaryById,
} from "../src/auth/strava-activity-provider.js";
import {
  createStravaOAuthAdapter,
  protectSecret,
  unprotectSecret,
} from "../src/auth/strava-oauth.js";

const NOW = new Date("2026-08-26T12:00:00.000Z");
const PRINCIPAL_ID = "00000000-0000-4000-8000-000000000002";
const TOKEN_SECRET = "synthetic-token-protection-secret";
const ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities";
const TOKEN_URL = "https://www.strava.com/oauth/token";
const SUMMARY_KEYS = [
  "average_speed",
  "distance",
  "id",
  "moving_time",
  "name",
  "sport_type",
  "start_date",
  "type",
];

test("provider rejects pagination windows outside pages 1..10 and 1..100 records before fetch", async () => {
  for (const [pages, perPage, startPage] of [
    [0, 10, 1],
    [11, 10, 1],
    [1.5, 10, 1],
    [1, 0, 1],
    [1, 101, 1],
    [1, 10.5, 1],
    [1, 10, 0],
    [1, 10, 11],
    [1, 10, 1.5],
    [2, 10, 10],
  ] as const) {
    let fetchCalled = false;
    const result = await fetchStravaActivitySummaries({
      accessToken: "synthetic-access",
      pages,
      perPage,
      startPage,
      fetchImpl: (async () => {
        fetchCalled = true;
        throw new Error("fetch must not be called for invalid bounds");
      }) as typeof fetch,
    });
    assert.equal(result.ok, false);
    if (!result.ok) assert.equal(result.error.code, "strava_provider_bounds_invalid");
    assert.equal(fetchCalled, false);
  }
});

test("provider can fetch one exact bounded start page", async () => {
  const calls: string[] = [];
  const result = await fetchStravaActivitySummaries({
    accessToken: "synthetic-access",
    pages: 1,
    perPage: 25,
    startPage: 4,
    fetchImpl: (async (input: string | URL | Request) => {
      const url = new URL(String(input));
      assert.equal(url.origin + url.pathname, ACTIVITIES_URL);
      assert.equal(url.searchParams.get("page"), "4");
      assert.equal(url.searchParams.get("per_page"), "25");
      calls.push(url.toString());
      return jsonResponse([providerActivity(99, "Run")]);
    }) as typeof fetch,
  });

  assert.equal(result.ok, true);
  if (result.ok) assert.deepEqual(result.value.map((summary) => summary.id), ["99"]);
  assert.equal(calls.length, 1);
});

test("provider paginates to a short page, filters run types, and projects only the allowlist", async () => {
  const calls: string[] = [];
  const fetchImpl = (async (input: string | URL | Request, init?: RequestInit) => {
    const url = new URL(String(input));
    assert.equal(url.origin + url.pathname, ACTIVITIES_URL);
    assert.equal(url.searchParams.get("per_page"), "3");
    assert.equal(new Headers(init?.headers).get("authorization"), "Bearer synthetic-access");
    calls.push(url.toString());
    const page = url.searchParams.get("page");
    if (page === "1") {
      return jsonResponse([
        providerActivity(101, "Run", {
          access_token: "forbidden-access-value",
          refresh_token: "forbidden-refresh-value",
          athlete: { id: 9 },
          map: { summary_polyline: "forbidden-polyline-value" },
          start_latlng: [-22.9, -47],
          notes: "forbidden-note-value",
          raw_payload: { private: true },
          secrets: ["forbidden-secret-value"],
        }),
        providerActivity(102, "Ride"),
        providerActivity(103, "TrailRun"),
      ]);
    }
    if (page === "2") {
      return jsonResponse([providerActivity(104, "VirtualRun")]);
    }
    throw new Error(`Unexpected test URL: ${url}`);
  }) as typeof fetch;

  const result = await fetchStravaActivitySummaries({
    accessToken: "synthetic-access",
    pages: 10,
    perPage: 3,
    fetchImpl,
  });

  assert.equal(result.ok, true);
  if (!result.ok) return;
  assert.deepEqual(result.value.map((summary) => summary.id), ["101", "103", "104"]);
  assert.equal(calls.length, 2);
  for (const summary of result.value) {
    assert.deepEqual(Object.keys(summary).sort(), SUMMARY_KEYS);
  }
  const output = JSON.stringify(result.value);
  for (const forbidden of [
    "forbidden-access-value",
    "forbidden-refresh-value",
    "forbidden-polyline-value",
    "forbidden-note-value",
    "forbidden-secret-value",
    "raw_payload",
    "athlete",
    "start_latlng",
    "coordinates",
  ]) {
    assert.equal(output.includes(forbidden), false, `Provider field leaked: ${forbidden}`);
  }
});

test("provider returns an empty success when no activities are eligible", async () => {
  const result = await fetchStravaActivitySummaries({
    accessToken: "synthetic-access",
    pages: 10,
    perPage: 100,
    fetchImpl: (async (input: string | URL | Request) => {
      const url = new URL(String(input));
      if (url.origin + url.pathname !== ACTIVITIES_URL) {
        throw new Error(`Unexpected test URL: ${url}`);
      }
      return jsonResponse([providerActivity(201, "Ride")]);
    }) as typeof fetch,
  });
  assert.deepEqual(result, { ok: true, value: [] });
});

test("provider maps credential, rate-limit, malformed, network, and 5xx failures safely", async (t) => {
  for (const [status, code] of [
    [401, "strava_credentials_revoked"],
    [403, "strava_credentials_revoked"],
    [429, "strava_rate_limited"],
    [500, "strava_provider_failed"],
  ] as const) {
    await t.test(String(status), async () => {
      const result = await fetchStravaActivitySummaries({
        accessToken: "synthetic-access",
        pages: 1,
        perPage: 10,
        fetchImpl: (async (input: string | URL | Request) => {
          assert.equal(new URL(String(input)).origin + new URL(String(input)).pathname, ACTIVITIES_URL);
          return jsonResponse({ provider_detail: "must-not-surface" }, status);
        }) as typeof fetch,
      });
      assert.equal(result.ok, false);
      if (!result.ok) {
        assert.equal(result.error.code, code);
        assert.equal(JSON.stringify(result.error).includes("must-not-surface"), false);
      }
    });
  }

  for (const [name, fetchImpl] of [
    ["malformed", async (input: string | URL | Request) => {
      assertActivityUrl(input);
      return jsonResponse({ not: "an array" });
    }],
    ["network", async (input: string | URL | Request) => {
      assertActivityUrl(input);
      throw new Error("synthetic private transport detail");
    }],
  ] as const) {
    await t.test(name, async () => {
      const result = await fetchStravaActivitySummaries({
        accessToken: "synthetic-access",
        pages: 1,
        perPage: 10,
        fetchImpl: fetchImpl as typeof fetch,
      });
      assert.equal(result.ok, false);
      if (!result.ok) {
        assert.equal(result.error.code, "strava_provider_failed");
        assert.equal(JSON.stringify(result.error).includes("private transport detail"), false);
      }
    });
  }
});

test("unexpired latest stored token is decrypted and used without refresh", async () => {
  const repository = createMemoryBodyWarAuthRepository();
  const account = await linkAccount(repository, ["read", "activity:read"]);
  const stored = await repository.storeProviderToken({
    accountId: account.id,
    accessTokenCiphertext: protectSecret("synthetic-current-access", TOKEN_SECRET),
    refreshTokenCiphertext: protectSecret("synthetic-current-refresh", TOKEN_SECRET),
    expiresAt: new Date(NOW.getTime() + 60_000).toISOString(),
  });
  const calls: string[] = [];
  const adapter = createAdapter(repository, async (input, init) => {
    const url = new URL(String(input));
    calls.push(url.origin + url.pathname);
    if (url.origin + url.pathname !== ACTIVITIES_URL) {
      throw new Error(`Unexpected test URL: ${url}`);
    }
    assert.equal(new Headers(init?.headers).get("authorization"), "Bearer synthetic-current-access");
    return jsonResponse([providerActivity(301, "Run")]);
  });

  const result = await adapter.listProviderActivitySummaries(PRINCIPAL_ID, "1", "100");
  assert.equal(result.ok, true);
  assert.deepEqual(calls, [ACTIVITIES_URL]);
  assert.equal((await repository.findLatestProviderToken(account.id))?.id, stored.id);
});

test("normal adapter routing keeps fake mode local and real mode on one exact provider page", async (t) => {
  await t.test("fake mode remains repository-backed and never fetches", async () => {
    const repository = createMemoryBodyWarAuthRepository();
    await linkAccount(repository, ["read", "activity:read"]);
    let fetchCalled = false;
    const adapter = createAdapter(repository, async () => {
      fetchCalled = true;
      throw new Error("fetch must not be called in fake mode");
    }, { fakeGateway: true });

    const result = await adapter.listActivitySummaries(PRINCIPAL_ID, "3", "20");
    assert.equal(result.ok, true);
    if (result.ok) assert.ok(result.value.length > 0);
    assert.equal(fetchCalled, false);
  });

  await t.test("real mode fetches exactly public page N", async () => {
    const repository = createMemoryBodyWarAuthRepository();
    const account = await linkAccount(repository, ["read", "activity:read"]);
    await repository.storeProviderToken({
      accountId: account.id,
      accessTokenCiphertext: protectSecret("synthetic-current-access", TOKEN_SECRET),
      refreshTokenCiphertext: protectSecret("synthetic-current-refresh", TOKEN_SECRET),
      expiresAt: new Date(NOW.getTime() + 60_000).toISOString(),
    });
    let calls = 0;
    const adapter = createAdapter(repository, async (input) => {
      const url = new URL(String(input));
      calls += 1;
      assert.equal(url.origin + url.pathname, ACTIVITIES_URL);
      assert.equal(url.searchParams.get("page"), "4");
      assert.equal(url.searchParams.get("per_page"), "25");
      return jsonResponse([providerActivity(401, "Run")]);
    });

    const result = await adapter.listActivitySummaries(PRINCIPAL_ID, "4", "25");
    assert.equal(result.ok, true);
    if (result.ok) assert.deepEqual(result.value.map((summary) => summary.id), ["401"]);
    assert.equal(calls, 1);
  });

  await t.test("invalid normal bounds fail before repository or provider access", async () => {
    let fetchCalled = false;
    const adapter = createAdapter(createMemoryBodyWarAuthRepository(), async () => {
      fetchCalled = true;
      throw new Error("fetch must not be called for invalid bounds");
    });

    const result = await adapter.listActivitySummaries(PRINCIPAL_ID, "0", "20");
    assert.equal(result.ok, false);
    if (!result.ok) assert.equal(result.error.code, "strava_provider_bounds_invalid");
    assert.equal(fetchCalled, false);
  });
});

test("expired latest token refreshes once, persists the rotated pair, then fetches", async () => {
  const repository = createMemoryBodyWarAuthRepository();
  const account = await linkAccount(repository, ["read", "activity:read"]);
  const expired = await repository.storeProviderToken({
    accountId: account.id,
    accessTokenCiphertext: protectSecret("synthetic-expired-access", TOKEN_SECRET),
    refreshTokenCiphertext: protectSecret("synthetic-refresh-before", TOKEN_SECRET),
    expiresAt: NOW.toISOString(),
  });
  const calls: string[] = [];
  const adapter = createAdapter(repository, async (input, init) => {
    const url = new URL(String(input));
    calls.push(url.origin + url.pathname);
    if (url.origin + url.pathname === TOKEN_URL) {
      assert.equal(init?.method, "POST");
      const body = new URLSearchParams(String(init?.body));
      assert.equal(body.get("grant_type"), "refresh_token");
      assert.equal(body.get("refresh_token"), "synthetic-refresh-before");
      return jsonResponse({
        access_token: "synthetic-rotated-access",
        refresh_token: "synthetic-rotated-refresh",
        expires_at: Math.floor(NOW.getTime() / 1000) + 3600,
      });
    }
    if (url.origin + url.pathname === ACTIVITIES_URL) {
      assert.equal(new Headers(init?.headers).get("authorization"), "Bearer synthetic-rotated-access");
      return jsonResponse([providerActivity(302, "Run")]);
    }
    throw new Error(`Unexpected test URL: ${url}`);
  });

  const result = await adapter.listProviderActivitySummaries(PRINCIPAL_ID, "1", "100");
  assert.equal(result.ok, true);
  assert.deepEqual(calls, [TOKEN_URL, ACTIVITIES_URL]);
  const latest = await repository.findLatestProviderToken(account.id);
  assert.ok(latest);
  assert.notEqual(latest.id, expired.id);
  assert.equal(unprotectSecret(latest.accessTokenCiphertext, TOKEN_SECRET), "synthetic-rotated-access");
  assert.equal(unprotectSecret(latest.refreshTokenCiphertext, TOKEN_SECRET), "synthetic-rotated-refresh");
});

test("adapter rejects missing account, scope, token, and unreadable ciphertext without fetch", async (t) => {
  await t.test("missing account", async () => {
    await expectPreFetchError(
      createMemoryBodyWarAuthRepository(),
      "strava_not_connected",
    );
  });

  await t.test("missing scope", async () => {
    const repository = createMemoryBodyWarAuthRepository();
    await linkAccount(repository, ["read"]);
    await expectPreFetchError(repository, "strava_scope_denied");
  });

  await t.test("missing token", async () => {
    const repository = createMemoryBodyWarAuthRepository();
    await linkAccount(repository, ["read", "activity:read"]);
    await expectPreFetchError(repository, "strava_token_missing");
  });

  await t.test("unreadable ciphertext", async () => {
    const repository = createMemoryBodyWarAuthRepository();
    const account = await linkAccount(repository, ["read", "activity:read"]);
    await repository.storeProviderToken({
      accountId: account.id,
      accessTokenCiphertext: "not-valid-ciphertext",
      refreshTokenCiphertext: "also-not-valid-ciphertext",
      expiresAt: new Date(NOW.getTime() + 60_000).toISOString(),
    });
    await expectPreFetchError(repository, "strava_token_unreadable");
  });
});

test("a rejected refresh maps safely and prevents activity retrieval", async () => {
  const repository = createMemoryBodyWarAuthRepository();
  const account = await linkAccount(repository, ["read", "activity:read"]);
  await repository.storeProviderToken({
    accountId: account.id,
    accessTokenCiphertext: protectSecret("synthetic-expired-access", TOKEN_SECRET),
    refreshTokenCiphertext: protectSecret("synthetic-rejected-refresh", TOKEN_SECRET),
    expiresAt: NOW.toISOString(),
  });
  let calls = 0;
  const adapter = createAdapter(repository, async (input) => {
    const url = new URL(String(input));
    calls += 1;
    if (url.origin + url.pathname !== TOKEN_URL) {
      throw new Error(`Unexpected test URL: ${url}`);
    }
    return jsonResponse({ error: "synthetic private rejection" }, 400);
  });

  const result = await adapter.listProviderActivitySummaries(PRINCIPAL_ID, "1", "100");
  assert.equal(result.ok, false);
  if (!result.ok) {
    assert.equal(result.error.code, "strava_credentials_revoked");
    assert.equal(JSON.stringify(result.error).includes("private rejection"), false);
  }
  assert.equal(calls, 1);
});

function createAdapter(
  repository: ReturnType<typeof createMemoryBodyWarAuthRepository>,
  fetchImpl: (
    input: string | URL | Request,
    init?: RequestInit,
  ) => Promise<Response>,
  options: { fakeGateway?: boolean } = {},
) {
  return createStravaOAuthAdapter({
    authRepos: {} as never,
    bodyWarRepo: repository,
    config: {
      clientId: "synthetic-client-id",
      clientSecret: "synthetic-client-secret",
      redirectUri: "http://127.0.0.1:5174/api/auth/strava/callback",
      publicBaseUrl: "http://127.0.0.1:5174",
      fakeGateway: options.fakeGateway ?? false,
      tokenProtectionSecret: TOKEN_SECRET,
    },
    fetchImpl: fetchImpl as typeof fetch,
    now: () => new Date(NOW),
  });
}

async function linkAccount(
  repository: ReturnType<typeof createMemoryBodyWarAuthRepository>,
  scope: string[],
) {
  return repository.upsertProviderAccount({
    provider: "strava",
    principalId: PRINCIPAL_ID,
    providerUserId: "synthetic-athlete",
    displayName: "Synthetic Runner",
    scope,
    status: "linked",
    metadata: {},
  });
}

async function expectPreFetchError(
  repository: ReturnType<typeof createMemoryBodyWarAuthRepository>,
  code: string,
): Promise<void> {
  let fetchCalled = false;
  const adapter = createAdapter(repository, async () => {
    fetchCalled = true;
    throw new Error("fetch must not be called");
  });
  const result = await adapter.listProviderActivitySummaries(PRINCIPAL_ID, "1", "100");
  assert.equal(result.ok, false);
  if (!result.ok) assert.equal(result.error.code, code);
  assert.equal(fetchCalled, false);
}

function providerActivity(
  id: number,
  sportType: string,
  extras: Record<string, unknown> = {},
): Record<string, unknown> {
  return {
    id,
    name: `Synthetic activity ${id}`,
    sport_type: sportType,
    type: sportType,
    distance: 5000,
    moving_time: 1500,
    average_speed: 3.33,
    start_date: "2026-08-25T12:00:00.000Z",
    ...extras,
  };
}

function jsonResponse(value: unknown, status = 200): Response {
  return new Response(JSON.stringify(value), {
    status,
    headers: { "content-type": "application/json" },
  });
}

function assertActivityUrl(input: string | URL | Request): void {
  const url = new URL(String(input));
  if (url.origin + url.pathname !== ACTIVITIES_URL) {
    throw new Error(`Unexpected test URL: ${url}`);
  }
}


test("historical detail verifies exact identity and projects only approved summary fields", async () => {
  const result = await fetchStravaActivitySummaryById({activityId:"987654321", athleteId:"123", accessToken:"synthetic-access", fetchImpl:async (url, init) => {
    assert.equal(String(url), "https://www.strava.com/api/v3/activities/987654321?include_all_efforts=false");
    assert.equal(new Headers(init?.headers).get("authorization"), "Bearer synthetic-access");
    assert.equal(init?.redirect, "error"); assert.ok(init?.signal instanceof AbortSignal);
    return jsonResponse(providerActivity(987654321,"Run",{athlete:{id:123},start_date:"2015-01-01T00:00:00Z",map:{polyline:"PRIVATE"},description:"PRIVATE"}));
  }});
  assert.equal(result.ok,true); if(result.ok){assert.deepEqual(Object.keys(result.value).sort(), SUMMARY_KEYS); assert.equal(result.value.start_date,"2015-01-01T00:00:00Z");}
});

test("historical detail rejects mismatched, missing and imprecise identities", async () => {
  for(const extra of [{id:1},{athlete:{id:456}},{athlete:null},{id:9007199254740992},{athlete:{id:9007199254740992}},{sport_type:"Ride",type:"Ride"}]) {
    const result=await fetchStravaActivitySummaryById({activityId:"987654321",athleteId:"123",accessToken:"secret",fetchImpl:async()=>jsonResponse(providerActivity(987654321,"Run",{athlete:{id:123},...extra}))});
    assert.equal(result.ok,false); if(!result.ok)assert.equal(result.error.code,"invalid_activity");
  }
  for(const activityId of ["../1","0","01","9223372036854775808","1?token=secret"]) {
    let calls=0;const result=await fetchStravaActivitySummaryById({activityId,athleteId:"123",accessToken:"secret",fetchImpl:async()=>{calls++;throw Error("unexpected");}});
    assert.equal(result.ok,false);assert.equal(calls,0);
  }
});

test("historical detail sanitizes provider errors and bounds response bytes", async () => {
  for(const [status,code] of [[404,"invalid_activity"],[403,"strava_scope_denied"],[401,"strava_credentials_revoked"],[429,"strava_rate_limited"],[500,"strava_provider_failed"]] as const){
    const result=await fetchStravaActivitySummaryById({activityId:"1",athleteId:"123",accessToken:"secret",fetchImpl:async()=>jsonResponse({private:"PRIVATE"},status)});
    assert.equal(result.ok,false);if(!result.ok)assert.equal(result.error.code,code);assert.ok(!JSON.stringify(result).includes("PRIVATE"));
  }
  for(const response of [()=>new Response("bad PRIVATE json"),()=>jsonResponse(providerActivity(1,"Run",{athlete:{id:123},distance:-1})),()=>new Response("x".repeat(1048577)),()=>{throw Error("PRIVATE network failure");}]){
    const result=await fetchStravaActivitySummaryById({activityId:"1",athleteId:"123",accessToken:"secret",fetchImpl:async()=>response()});
    assert.equal(result.ok,false);if(!result.ok)assert.equal(result.error.code,"strava_provider_failed");assert.ok(!JSON.stringify(result).includes("PRIVATE"));
  }
});

test("historical adapter refreshes encrypted tokens before exact detail lookup", async () => {
  const repository=createMemoryBodyWarAuthRepository();
  const account=await repository.upsertProviderAccount({provider:"strava",principalId:PRINCIPAL_ID,providerUserId:"123",displayName:"Runner",scope:["activity:read"],status:"linked",metadata:{}});
  await repository.storeProviderToken({accountId:account.id,accessTokenCiphertext:protectSecret("expired",TOKEN_SECRET),refreshTokenCiphertext:protectSecret("refresh",TOKEN_SECRET),expiresAt:NOW.toISOString()});
  const calls:string[]=[];
  const adapter=createAdapter(repository,async(url,init)=>{calls.push(String(url));if(String(url)===TOKEN_URL)return jsonResponse({access_token:"rotated",refresh_token:"rotated-refresh",expires_at:Math.floor(NOW.getTime()/1000)+3600});assert.equal(new Headers(init?.headers).get("authorization"),"Bearer rotated");return jsonResponse(providerActivity(1,"Run",{athlete:{id:123}}));});
  assert.equal((await adapter.getActivitySummary(PRINCIPAL_ID,"1")).ok,true);assert.equal(calls.length,2);assert.equal(calls[0],TOKEN_URL);
  const stored=await repository.findLatestProviderToken(account.id);assert.ok(stored);assert.notEqual(stored.accessTokenCiphertext,"rotated");assert.equal(unprotectSecret(stored.accessTokenCiphertext,TOKEN_SECRET),"rotated");
});
