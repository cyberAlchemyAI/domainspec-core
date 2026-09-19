-- A runner has at most one Strava account; athlete ownership cannot be transferred by upsert.
CREATE UNIQUE INDEX IF NOT EXISTS body_war_provider_principal_unique ON body_war_provider_accounts (principal_id, provider);
