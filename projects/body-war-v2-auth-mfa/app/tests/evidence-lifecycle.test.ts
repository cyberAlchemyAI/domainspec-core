import assert from "node:assert/strict";
import test from "node:test";
import { createMemoryBodyWarAuthRepository } from "../src/auth/memory-repository.js";

const PRINCIPAL_ID = "00000000-0000-4000-8000-000000000001";
const CONSENTED_AT = "2026-08-26T12:00:00.000Z";

test("exact evidence disposition is idempotent and resets only its affected track", async () => {
  const repository = createMemoryBodyWarAuthRepository();
  const firstTrack = await repository.createSuggestedTrack({
    principalId: PRINCIPAL_ID,
    name: "First synthetic track",
    placeLabel: "Synthetic place A",
    city: "Campinas",
  });
  const secondTrack = await repository.createSuggestedTrack({
    principalId: PRINCIPAL_ID,
    name: "Second synthetic track",
    placeLabel: "Synthetic place B",
    city: "Campinas",
  });
  const firstCandidate = await addCandidate(repository, firstTrack.id, "activity-a");
  const lastFirstTrackCandidate = await addCandidate(
    repository,
    firstTrack.id,
    "activity-b",
  );
  await addCandidate(repository, secondTrack.id, "activity-c");

  assert.equal(await repository.disposeActivityEvidenceCandidate({candidateId:firstCandidate.id,principalId:"another-runner",reason:"consent_revocation"}),"already_absent");
  assert.equal((await repository.listActivityEvidenceCandidates(firstTrack.id)).length,2);
  assert.equal(
    await repository.disposeActivityEvidenceCandidate({
      candidateId: firstCandidate.id,
      reason: "deletion",
    }),
    "disposed",
  );
  assert.equal((await repository.findSuggestedTrack(firstTrack.id))?.status, "evidence_submitted");
  assert.equal((await repository.listActivityEvidenceCandidates(firstTrack.id)).length, 1);

  assert.equal(
    await repository.disposeActivityEvidenceCandidate({
      candidateId: firstCandidate.id,
      reason: "deletion",
    }),
    "already_absent",
  );
  assert.equal(
    await repository.disposeActivityEvidenceCandidate({
      candidateId: lastFirstTrackCandidate.id,
      reason: "consent_revocation",
    }),
    "disposed",
  );

  assert.equal((await repository.findSuggestedTrack(firstTrack.id))?.status, "needs_evidence");
  assert.equal((await repository.findSuggestedTrack(secondTrack.id))?.status, "evidence_submitted");
  assert.equal((await repository.listActivityEvidenceCandidates(secondTrack.id)).length, 1);
});

test("provider revocation removes tokens while preserving profile and evidence", async () => {
  const repository = createMemoryBodyWarAuthRepository();
  const account = await repository.upsertProviderAccount({
    provider: "strava",
    principalId: PRINCIPAL_ID,
    providerUserId: "synthetic-athlete",
    displayName: "Synthetic Runner",
    scope: ["read", "activity:read"],
    status: "linked",
    metadata: {},
  });
  await repository.upsertRunnerProfile({
    principalId: PRINCIPAL_ID,
    displayName: "Synthetic Runner",
  });
  await repository.storeProviderToken({
    accountId: account.id,
    accessTokenCiphertext: "ciphertext-a",
    refreshTokenCiphertext: "ciphertext-b",
    expiresAt: "2026-08-26T13:00:00.000Z",
  });
  const latest = await repository.storeProviderToken({
    accountId: account.id,
    accessTokenCiphertext: "ciphertext-c",
    refreshTokenCiphertext: "ciphertext-d",
    expiresAt: "2026-08-26T14:00:00.000Z",
  });
  const track = await repository.createSuggestedTrack({
    principalId: PRINCIPAL_ID,
    name: "Synthetic retained evidence track",
    placeLabel: "Synthetic place",
    city: "Campinas",
  });
  const evidence = await addCandidate(repository, track.id, "activity-retained");

  assert.equal((await repository.findLatestProviderToken(account.id))?.id, latest.id);
  assert.equal(await repository.revokeProviderAccess(PRINCIPAL_ID), "disposed");
  assert.equal(await repository.findProviderAccountByPrincipalId(PRINCIPAL_ID), null);
  assert.equal(await repository.findLatestProviderToken(account.id), null);
  assert.equal((await repository.findRunnerProfile(PRINCIPAL_ID))?.displayName, "Synthetic Runner");
  assert.equal(
    (await repository.listActivityEvidenceCandidates(track.id))[0]?.id,
    evidence.id,
  );
  assert.equal(await repository.revokeProviderAccess(PRINCIPAL_ID), "already_absent");
});

async function addCandidate(
  repository: ReturnType<typeof createMemoryBodyWarAuthRepository>,
  suggestedTrackId: string,
  providerActivityId: string,
) {
  return repository.addActivityEvidenceCandidate({
    suggestedTrackId,
    principalId: PRINCIPAL_ID,
    providerActivityId,
    redactedSummary: {
      id: providerActivityId,
      name: "Synthetic Run",
      sport_type: "Run",
      type: "Run",
      distance: 5000,
      moving_time: 1500,
      average_speed: 3.33,
      start_date: CONSENTED_AT,
    },
    consentText: "Store only the synthetic redacted summary.",
    consentedAt: CONSENTED_AT,
  });
}
