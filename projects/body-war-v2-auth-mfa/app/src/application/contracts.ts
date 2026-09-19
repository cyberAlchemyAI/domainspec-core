// Generated from checked application ontology.
export type StravaProvider = "strava";
export type ProviderStatus = "linked" | "disconnected";
export type SuggestedTrackStatus = "needs_evidence" | "evidence_submitted" | "operator_review" | "source_backed" | "retired";
export type NoClaim = "not_claimed";
export type ActivityEvidenceCandidateStatus = "submitted" | "operator_review" | "accepted" | "rejected";
export type EmptyRequest = {

};
export type OpaqueResponse = {
  value?: unknown | undefined;
};
export type ProfileResponse = {
  profile: PublicRunnerProfile;
};
export type StatusResponse = {
  configured: boolean;
  authenticated: boolean;
  connected: boolean;
  athlete: PublicAthlete | null;
  redirect_uri: string;
  scope: string;
  identity_mode?: string | undefined;
  login_uri?: string | undefined;
  session_state?: string | undefined;
  security_available?: boolean | undefined;
};
export type RunnerProfile = {
  principalId: string;
  displayName: string;
  privacyStatus: string;
  createdAt: string;
  updatedAt: string;
};
export type ProviderAccount = {
  id: string;
  provider: StravaProvider;
  principalId: string;
  providerUserId: string;
  displayName: string | null;
  scope: (string)[];
  status: ProviderStatus;
  linkedAt: string;
  updatedAt: string;
  metadata: Record<string, unknown>;
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
export type OAuthCallbackRequest = {
  code?: string | undefined;
  state?: string | undefined;
  error?: string | undefined;
};
export type LogoutResponse = {
  ok: boolean;
};
export type PublicAthlete = {
  id: (string | number);
  firstname?: string | null | undefined;
  lastname?: string | null | undefined;
  profile?: string | null | undefined;
  strava_profile_url: string | null;
  scope: (string)[];
  provider: StravaProvider;
  status: ProviderStatus;
};
export type PublicSession = {
  expires_at: string;
};
export type PublicConnection = {
  connected: boolean;
  account: PublicAthlete | null;
  profile_url: string | null;
};
export type ProfilePrivacy = {
  provider_tokens: string;
  activity_import: string;
  csrf: string;
};
export type ProfileValidation = {
  taquaral_activity: string;
  route_geometry: string;
  scoring: string;
};
export type PublicRunnerProfile = {
  principal_id: string;
  display_name: string;
  principal_status: string;
  session: PublicSession;
  strava: PublicConnection;
  privacy: ProfilePrivacy;
  validation: ProfileValidation;
};
export type ProviderLinkResponse = {
  url: string;
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
export type ActivityPageRequest = {
  page?: string | undefined;
  per_page?: string | undefined;
};
export type ActivitiesResponse = {
  activities: (ActivitySummary)[];
  receipt: ActivityImportReceipt;
};
export type RedactionReceipt = {
  provider_tokens: string;
  raw_private_payload: string;
  maps: string;
  notes: string;
};
export type ImportConsentReceipt = {
  friend_fixture: string;
};
export type ActivityImportReceipt = {
  source: StravaProvider;
  principal_id: string;
  imported_at: string;
  summary_count: number;
  redaction: RedactionReceipt;
  consent: ImportConsentReceipt;
  authority: EvidenceAuthority;
};
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
export type CreateTrackRequest = {
  name: string;
  place_label: string;
  city: string;
  distance_hint_meters?: number | null | undefined;
  public_note?: string | undefined;
};
export type TrackKeyRequest = {
  idOrSlug: string;
};
export type TrackListResponse = {
  suggested_tracks: (PublicTrack)[];
};
export type TrackResponse = {
  suggested_track: PublicTrack;
  my_evidence_candidates?: (PublicEvidence)[] | undefined;
  evidence_summary?: EvidenceSummary | undefined;
};
export type PublicTrackAuthority = {
  route_geometry: string;
  scoring: NoClaim;
  pilot_ready: NoClaim;
};
export type PublicTrack = {
  id: string;
  slug: string;
  name: string;
  place_label: string;
  city: string;
  country: string;
  distance_hint_meters: number | null;
  status: SuggestedTrackStatus;
  geometry_authority: string;
  suggested_by: string;
  public_note: string;
  created_at: string;
  updated_at: string;
  authority: PublicTrackAuthority;
};
export type ActivityEvidenceCandidate = {
  id: string;
  suggestedTrackId: string;
  principalId: string;
  provider: StravaProvider;
  providerActivityId: string;
  redactedSummary: Record<string, unknown>;
  consentText: string;
  consentedAt: string;
  status: ActivityEvidenceCandidateStatus;
  createdAt: string;
  updatedAt: string;
};
export type AttachEvidenceRequest = {
  activity_id: string;
  consent_acknowledged?: boolean | undefined;
  consent_text?: string | undefined;
};
export type EvidenceResponse = {
  evidence_candidate: PublicEvidence;
  suggested_track?: PublicTrack | undefined;
};
export type EvidenceAuthority = {
  activity_summary: string;
  route_geometry: NoClaim;
  scoring: NoClaim;
};
export type PublicEvidence = {
  id: string;
  suggested_track_id: string;
  provider: StravaProvider;
  provider_activity_id: string;
  redacted_summary: ActivitySummary;
  consented_at: string;
  status: ActivityEvidenceCandidateStatus;
  created_at: string;
  updated_at: string;
  authority: EvidenceAuthority;
};
export type EvidenceSummaryAuthority = {
  activity_summary: string;
  route_geometry: NoClaim;
  scoring: NoClaim;
  pilot_ready: NoClaim;
};
export type EvidenceSummary = {
  candidate_count: number;
  redaction: RedactionReceipt;
  authority: EvidenceSummaryAuthority;
};
export type WithdrawEvidenceResponse = {
  withdrawn: boolean;
};
