import { randomUUID } from "node:crypto";
import type {
  AddActivityEvidenceCandidateInput,
  BodyWarAuthRepository,
  CreateSuggestedTrackInput,
  DisposeActivityEvidenceCandidateInput,
  StoreProviderTokenInput,
  UpsertProviderAccountInput,
  UpsertRunnerProfileInput,
} from "./body-war-repository.js";
import {
  DEFAULT_SUGGESTED_TRACK as DEFAULT_TRACK,
  suggestedTrackSlug,
} from "./body-war-repository.js";
import type {
  ActivitySummary,
  ActivityEvidenceCandidate,
  OAuthState,
  ProviderAccount,
  ProviderTokenRecord,
  RunnerProfile,
  SuggestedTrack,
} from "./types.js";

export function createMemoryBodyWarAuthRepository(): BodyWarAuthRepository {
  const states = new Map<string, OAuthState>();
  const accounts = new Map<string, ProviderAccount>();
  const accountIdsByPrincipal = new Map<string, string>();
  const profiles = new Map<string, RunnerProfile>();
  const tokens = new Map<string, ProviderTokenRecord>();
  const suggestedTracks = new Map<string, SuggestedTrack>();
  const evidenceCandidates = new Map<string, ActivityEvidenceCandidate>();

  const ensureDefaultSuggestedTracks = async (): Promise<SuggestedTrack[]> => {
    const existing = [...suggestedTracks.values()].find((track) =>
      track.slug === DEFAULT_TRACK.slug,
    );
    const now = new Date().toISOString();
    const seeded: SuggestedTrack = {
      id: existing?.id ?? randomUUID(),
      slug: DEFAULT_TRACK.slug,
      name: DEFAULT_TRACK.name,
      placeLabel: DEFAULT_TRACK.placeLabel,
      city: DEFAULT_TRACK.city,
      country: DEFAULT_TRACK.country,
      distanceHintMeters: DEFAULT_TRACK.distanceHintMeters,
      status: existing?.status ?? "needs_evidence",
      geometryAuthority: existing?.geometryAuthority ?? "needs_evidence",
      suggestedByPrincipalId: existing?.suggestedByPrincipalId ?? null,
      publicNote: DEFAULT_TRACK.publicNote,
      createdAt: existing?.createdAt ?? now,
      updatedAt: now,
    };
    suggestedTracks.set(seeded.id, seeded);
    return [cloneSuggestedTrack(seeded)];
  };

  return {
    async createOAuthState(state) {
      const cloned = cloneState(state);
      states.set(cloned.state, cloned);
      return cloneState(cloned);
    },

    async consumeOAuthState(state, now) {
      const found = states.get(state);
      if (!found || found.consumedAt || now >= new Date(found.expiresAt)) {
        return null;
      }
      const consumed = { ...found, consumedAt: now.toISOString() };
      states.set(state, consumed);
      return cloneState(consumed);
    },

    async upsertProviderAccount(input) {
      const key = `${input.provider}:${input.providerUserId}`;
      const existing = accounts.get(key);
      const now = new Date().toISOString();
      const account: ProviderAccount = {
        id: existing?.id ?? randomUUID(),
        provider: input.provider,
        principalId: input.principalId,
        providerUserId: input.providerUserId,
        displayName: input.displayName,
        scope: [...input.scope],
        status: input.status,
        metadata: { ...input.metadata },
        linkedAt: existing?.linkedAt ?? now,
        updatedAt: now,
      };
      accounts.set(key, account);
      accountIdsByPrincipal.set(input.principalId, key);
      return cloneAccount(account);
    },

    async findProviderAccountByPrincipalId(principalId) {
      const key = accountIdsByPrincipal.get(principalId);
      const account = key ? accounts.get(key) : undefined;
      return account?.status === "linked" ? cloneAccount(account) : null;
    },

    async storeProviderToken(input: StoreProviderTokenInput) {
      const now = new Date().toISOString();
      const record: ProviderTokenRecord = {
        id: randomUUID(),
        accountId: input.accountId,
        accessTokenCiphertext: input.accessTokenCiphertext,
        refreshTokenCiphertext: input.refreshTokenCiphertext,
        expiresAt: input.expiresAt,
        createdAt: now,
        updatedAt: now,
      };
      tokens.set(record.id, record);
      return { ...record };
    },

    async findLatestProviderToken(accountId) {
      const record = [...tokens.values()]
        .filter((candidate) => candidate.accountId === accountId)
        .sort((a, b) => a.createdAt.localeCompare(b.createdAt))
        .at(-1);
      return record ? { ...record } : null;
    },

    async revokeProviderAccess(principalId) {
      const key = accountIdsByPrincipal.get(principalId);
      if (!key) return "already_absent";
      const account = accounts.get(key);
      if (!account) return "already_absent";

      let removedToken = false;
      for (const [tokenId, token] of tokens.entries()) {
        if (token.accountId === account.id) {
          tokens.delete(tokenId);
          removedToken = true;
        }
      }

      if (account.status === "disconnected") {
        return removedToken ? "disposed" : "already_absent";
      }

      accounts.set(key, {
        ...account,
        status: "disconnected",
        updatedAt: new Date().toISOString(),
      });
      return "disposed";
    },

    async upsertRunnerProfile(input: UpsertRunnerProfileInput) {
      const existing = profiles.get(input.principalId);
      const now = new Date().toISOString();
      const profile: RunnerProfile = {
        principalId: input.principalId,
        displayName: input.displayName,
        privacyStatus: input.privacyStatus ?? existing?.privacyStatus ?? "private",
        createdAt: existing?.createdAt ?? now,
        updatedAt: now,
      };
      profiles.set(input.principalId, profile);
      return { ...profile };
    },

    async findRunnerProfile(principalId) {
      const profile = profiles.get(principalId);
      return profile ? { ...profile } : null;
    },

    async listActivitySummaries(principalId) {
      return [
        {
          id: `fake-activity-${principalId.slice(0, 8)}`,
          name: "Redacted Strava activity summary",
          sport_type: "Run",
          type: "Run",
          distance: 5000,
          moving_time: 1500,
          average_speed: 3.33,
          start_date: "2026-06-21T12:00:00.000Z",
        },
      ];
    },

    async ensureDefaultSuggestedTracks() {
      return ensureDefaultSuggestedTracks();
    },

    async listSuggestedTracks() {
      await ensureDefaultSuggestedTracks();
      return [...suggestedTracks.values()]
        .sort(compareSuggestedTracks)
        .map(cloneSuggestedTrack);
    },

    async findSuggestedTrack(idOrSlug) {
      await ensureDefaultSuggestedTracks();
      const found = [...suggestedTracks.values()].find((track) =>
        track.id === idOrSlug || track.slug === idOrSlug,
      );
      return found ? cloneSuggestedTrack(found) : null;
    },

    async createSuggestedTrack(input: CreateSuggestedTrackInput) {
      const now = new Date().toISOString();
      const baseSlug = suggestedTrackSlug(input.name);
      const slug = uniqueSuggestedTrackSlug(baseSlug, suggestedTracks);
      const track: SuggestedTrack = {
        id: randomUUID(),
        slug,
        name: input.name,
        placeLabel: input.placeLabel,
        city: input.city,
        country: input.country ?? "BR",
        distanceHintMeters: input.distanceHintMeters ?? null,
        status: "needs_evidence",
        geometryAuthority: "needs_evidence",
        suggestedByPrincipalId: input.principalId,
        publicNote: input.publicNote ?? "",
        createdAt: now,
        updatedAt: now,
      };
      suggestedTracks.set(track.id, track);
      return cloneSuggestedTrack(track);
    },

    async addActivityEvidenceCandidate(input: AddActivityEvidenceCandidateInput) {
      const now = new Date().toISOString();
      const candidate: ActivityEvidenceCandidate = {
        id: randomUUID(),
        suggestedTrackId: input.suggestedTrackId,
        principalId: input.principalId,
        provider: "strava",
        providerActivityId: input.providerActivityId,
        redactedSummary: { ...input.redactedSummary },
        consentText: input.consentText,
        consentedAt: input.consentedAt,
        status: "submitted",
        createdAt: now,
        updatedAt: now,
      };
      evidenceCandidates.set(candidate.id, candidate);

      const track = suggestedTracks.get(input.suggestedTrackId);
      if (track && track.status === "needs_evidence") {
        suggestedTracks.set(track.id, {
          ...track,
          status: "evidence_submitted",
          updatedAt: now,
        });
      }

      return cloneActivityEvidenceCandidate(candidate);
    },

    async listActivityEvidenceCandidates(suggestedTrackId, principalId) {
      return [...evidenceCandidates.values()]
        .filter((candidate) =>
          candidate.suggestedTrackId === suggestedTrackId &&
          (!principalId || candidate.principalId === principalId),
        )
        .sort((a, b) => b.createdAt.localeCompare(a.createdAt))
        .map(cloneActivityEvidenceCandidate);
    },

    async disposeActivityEvidenceCandidate(
      input: DisposeActivityEvidenceCandidateInput,
    ) {
      const candidate = evidenceCandidates.get(input.candidateId);
      if (!candidate) return "already_absent";

      evidenceCandidates.delete(input.candidateId);
      const hasRemainingEvidence = [...evidenceCandidates.values()].some(
        (other) => other.suggestedTrackId === candidate.suggestedTrackId,
      );
      if (!hasRemainingEvidence) {
        const track = suggestedTracks.get(candidate.suggestedTrackId);
        if (track) {
          suggestedTracks.set(track.id, {
            ...track,
            status: "needs_evidence",
            updatedAt: new Date().toISOString(),
          });
        }
      }
      return "disposed";
    },
  };
}

function cloneState(state: OAuthState): OAuthState {
  return { ...state };
}

function cloneAccount(account: ProviderAccount): ProviderAccount {
  return {
    ...account,
    scope: [...account.scope],
    metadata: { ...account.metadata },
  };
}

function cloneSuggestedTrack(track: SuggestedTrack): SuggestedTrack {
  return { ...track };
}

function cloneActivityEvidenceCandidate(
  candidate: ActivityEvidenceCandidate,
): ActivityEvidenceCandidate {
  return {
    ...candidate,
    redactedSummary: { ...candidate.redactedSummary },
  };
}

function uniqueSuggestedTrackSlug(
  baseSlug: string,
  tracks: Map<string, SuggestedTrack>,
): string {
  const used = new Set([...tracks.values()].map((track) => track.slug));
  let slug = baseSlug;
  let suffix = 2;
  while (used.has(slug)) {
    slug = `${baseSlug}-${suffix}`;
    suffix += 1;
  }
  return slug;
}

function compareSuggestedTracks(a: SuggestedTrack, b: SuggestedTrack): number {
  if (a.slug === DEFAULT_TRACK.slug) return -1;
  if (b.slug === DEFAULT_TRACK.slug) return 1;
  return b.createdAt.localeCompare(a.createdAt);
}
