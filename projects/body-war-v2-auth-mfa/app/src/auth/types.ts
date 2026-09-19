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

import type { ProviderAccount, RunnerProfile, OAuthState, ProviderTokenRecord, ActivitySummary, SuggestedTrackStatus, ActivityEvidenceCandidateStatus, SuggestedTrack, ActivityEvidenceCandidate } from "../application/contracts.js";
export type { ProviderAccount, RunnerProfile, OAuthState, ProviderTokenRecord, ActivitySummary, SuggestedTrackStatus, ActivityEvidenceCandidateStatus, SuggestedTrack, ActivityEvidenceCandidate } from "../application/contracts.js";

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
