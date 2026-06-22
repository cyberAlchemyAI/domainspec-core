import type {
  ActivitySummary,
  OAuthState,
  ProviderAccount,
  ProviderTokenRecord,
  RunnerProfile,
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

export type BodyWarAuthRepository = {
  createOAuthState(state: OAuthState): Promise<OAuthState>;
  consumeOAuthState(state: string, now: Date): Promise<OAuthState | null>;
  upsertProviderAccount(input: UpsertProviderAccountInput): Promise<ProviderAccount>;
  findProviderAccountByPrincipalId(principalId: string): Promise<ProviderAccount | null>;
  storeProviderToken(input: StoreProviderTokenInput): Promise<ProviderTokenRecord>;
  upsertRunnerProfile(input: UpsertRunnerProfileInput): Promise<RunnerProfile>;
  findRunnerProfile(principalId: string): Promise<RunnerProfile | null>;
  listActivitySummaries(principalId: string): Promise<ActivitySummary[]>;
};
