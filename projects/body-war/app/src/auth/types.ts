import type { AuthContext } from "@domainspec/auth-user-management";

export type JsonRecord = Record<string, unknown>;

export type CookieMap = Record<string, string | undefined>;

export type AppError = {
  code: string;
  status: number;
  message: string;
  details?: JsonRecord | undefined;
};

export type AppResult<T> =
  | { ok: true; value: T }
  | { ok: false; error: AppError };

export type ProviderAccount = {
  id: string;
  provider: "strava";
  principalId: string;
  providerUserId: string;
  displayName: string | null;
  scope: string[];
  status: "linked" | "disconnected";
  linkedAt: string;
  updatedAt: string;
  metadata: JsonRecord;
};

export type RunnerProfile = {
  principalId: string;
  displayName: string;
  privacyStatus: string;
  createdAt: string;
  updatedAt: string;
};

export type OAuthState = {
  state: string;
  nonce: string;
  redirectTarget: string;
  createdAt: string;
  expiresAt: string;
  consumedAt: string | null;
};

export type ProviderTokenRecord = {
  id: string;
  accountId: string;
  accessTokenCiphertext: string;
  refreshTokenCiphertext: string;
  expiresAt: string;
  createdAt: string;
  updatedAt: string;
};

export type ActivitySummary = {
  id: string;
  name: string;
  sport_type?: string | undefined;
  type?: string | undefined;
  distance: number;
  moving_time: number;
  average_speed: number;
  start_date: string;
};

export type SuggestedTrackStatus =
  | "needs_evidence"
  | "evidence_submitted"
  | "operator_review"
  | "source_backed"
  | "retired";

export type ActivityEvidenceCandidateStatus =
  | "submitted"
  | "operator_review"
  | "accepted"
  | "rejected";

export type SuggestedTrack = {
  id: string;
  slug: string;
  name: string;
  placeLabel: string;
  city: string;
  country: string;
  distanceHintMeters: number | null;
  status: SuggestedTrackStatus;
  geometryAuthority: string;
  suggestedByPrincipalId: string | null;
  publicNote: string;
  createdAt: string;
  updatedAt: string;
};

export type ActivityEvidenceCandidate = {
  id: string;
  suggestedTrackId: string;
  principalId: string;
  provider: "strava";
  providerActivityId: string;
  redactedSummary: JsonRecord;
  consentText: string;
  consentedAt: string;
  status: ActivityEvidenceCandidateStatus;
  createdAt: string;
  updatedAt: string;
};

export type AuthenticatedRequest = {
  auth: AuthContext;
  csrfToken?: string | undefined;
};

export function appError(
  code: string,
  status: number,
  message: string,
  details?: JsonRecord,
): AppError {
  return { code, status, message, details };
}
