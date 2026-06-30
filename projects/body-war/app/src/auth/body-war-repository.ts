import type {
  ActivitySummary,
  ActivityEvidenceCandidate,
  OAuthState,
  ProviderAccount,
  ProviderTokenRecord,
  RunnerProfile,
  SuggestedTrack,
} from "./types.js";

export type UpsertProviderAccountInput = {
  provider: "strava";
  principalId: string;
  providerUserId: string;
  displayName: string | null;
  scope: string[];
  status: "linked" | "disconnected";
  metadata: Record<string, unknown>;
};

export type UpsertRunnerProfileInput = {
  principalId: string;
  displayName: string;
  privacyStatus?: string | undefined;
};

export type StoreProviderTokenInput = {
  accountId: string;
  accessTokenCiphertext: string;
  refreshTokenCiphertext: string;
  expiresAt: string;
};

export type CreateSuggestedTrackInput = {
  principalId: string;
  name: string;
  placeLabel: string;
  city: string;
  country?: string | undefined;
  distanceHintMeters?: number | null | undefined;
  publicNote?: string | undefined;
};

export type AddActivityEvidenceCandidateInput = {
  suggestedTrackId: string;
  principalId: string;
  providerActivityId: string;
  redactedSummary: Record<string, unknown>;
  consentText: string;
  consentedAt: string;
};

export type BodyWarAuthRepository = {
  createOAuthState(state: OAuthState): Promise<OAuthState>;
  consumeOAuthState(state: string, now: Date): Promise<OAuthState | null>;
  upsertProviderAccount(input: UpsertProviderAccountInput): Promise<ProviderAccount>;
  findProviderAccountByPrincipalId(principalId: string): Promise<ProviderAccount | null>;
  storeProviderToken(input: StoreProviderTokenInput): Promise<ProviderTokenRecord>;
  upsertRunnerProfile(input: UpsertRunnerProfileInput): Promise<RunnerProfile>;
  findRunnerProfile(principalId: string): Promise<RunnerProfile | null>;
  listActivitySummaries(principalId: string): Promise<ActivitySummary[]>;
  ensureDefaultSuggestedTracks(): Promise<SuggestedTrack[]>;
  listSuggestedTracks(): Promise<SuggestedTrack[]>;
  findSuggestedTrack(idOrSlug: string): Promise<SuggestedTrack | null>;
  createSuggestedTrack(input: CreateSuggestedTrackInput): Promise<SuggestedTrack>;
  addActivityEvidenceCandidate(input: AddActivityEvidenceCandidateInput): Promise<ActivityEvidenceCandidate>;
  listActivityEvidenceCandidates(
    suggestedTrackId: string,
    principalId?: string | undefined,
  ): Promise<ActivityEvidenceCandidate[]>;
};

export const DEFAULT_SUGGESTED_TRACK = {
  slug: "volta-do-taquaral",
  name: "Volta do Taquaral",
  placeLabel: "Parque Portugal / Lagoa do Taquaral",
  city: "Campinas",
  country: "BR",
  distanceHintMeters: 6400,
  publicNote: "Sugestao inicial para reunir evidencias antes de qualquer geometria source-backed.",
} as const;

export function suggestedTrackSlug(value: string): string {
  const normalized = value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
  return normalized || "suggested-track";
}
