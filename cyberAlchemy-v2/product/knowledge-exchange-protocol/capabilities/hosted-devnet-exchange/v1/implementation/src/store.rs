use base64::{engine::general_purpose::STANDARD, Engine};
use sha2::{Digest, Sha256};
use sqlx::{postgres::PgPoolOptions, PgPool, Row};

use crate::model::{ClientErrorEventRequest, Database};

#[derive(Clone)]
pub enum Persistence {
    Memory,
    Postgres(PgPool),
}

impl Persistence {
    pub async fn postgres(database_url: &str) -> Result<Self, String> {
        let pool = PgPoolOptions::new()
            .max_connections(8)
            .connect(database_url)
            .await
            .map_err(|error| format!("PostgreSQL connection failed: {error}"))?;
        for migration in [
            include_str!("../migrations/001_hosted_exchange.sql"),
            include_str!("../migrations/002_error_intelligence.sql"),
        ] {
            for statement in migration.split("-- statement") {
                let statement = statement.trim();
                if !statement.is_empty() {
                    sqlx::query(statement)
                        .execute(&pool)
                        .await
                        .map_err(|error| format!("PostgreSQL migration failed: {error}"))?;
                }
            }
        }
        Ok(Self::Postgres(pool))
    }

    pub async fn load(&self) -> Result<Database, String> {
        match self {
            Self::Memory => Ok(Database::default()),
            Self::Postgres(pool) => {
                let row = sqlx::query(
                    "SELECT state_json FROM kep_hosted.application_state WHERE state_id = 1",
                )
                .fetch_optional(pool)
                .await
                .map_err(|error| format!("PostgreSQL state load failed: {error}"))?;
                match row {
                    Some(row) => serde_json::from_value(row.get("state_json"))
                        .map_err(|error| format!("PostgreSQL state JSON is invalid: {error}")),
                    None => Ok(Database::default()),
                }
            }
        }
    }

    pub async fn save(
        &self,
        state: &Database,
        event_type: &str,
        entity_id: &str,
    ) -> Result<(), String> {
        match self {
            Self::Memory => Ok(()),
            Self::Postgres(pool) => {
                let state_json = serde_json::to_value(state)
                    .map_err(|error| format!("state serialization failed: {error}"))?;
                let event_json = serde_json::json!({
                    "event_type": event_type,
                    "entity_id": entity_id,
                    "state_sha256": hex::encode(Sha256::digest(serde_json::to_vec(&state_json).unwrap_or_default()))
                });
                let mut transaction = pool
                    .begin()
                    .await
                    .map_err(|error| format!("PostgreSQL transaction failed: {error}"))?;
                let previous: Vec<u8> = sqlx::query("SELECT event_digest FROM kep_hosted.event_journal ORDER BY event_id DESC LIMIT 1 FOR UPDATE")
                    .fetch_optional(&mut *transaction)
                    .await
                    .map_err(|error| format!("journal lock failed: {error}"))?
                    .map(|row| row.get("event_digest"))
                    .unwrap_or_else(|| vec![0_u8; 32]);
                let mut hasher = Sha256::new();
                hasher.update(b"CA2-KEP-HOSTED-EVENT-v1");
                hasher.update(&previous);
                hasher.update(event_json.to_string().as_bytes());
                let event_digest: [u8; 32] = hasher.finalize().into();
                sqlx::query("INSERT INTO kep_hosted.application_state (state_id, state_json, revision) VALUES (1, $1, 1) ON CONFLICT (state_id) DO UPDATE SET state_json = EXCLUDED.state_json, revision = kep_hosted.application_state.revision + 1, updated_at = clock_timestamp()")
                    .bind(&state_json)
                    .execute(&mut *transaction)
                    .await
                    .map_err(|error| format!("state persistence failed: {error}"))?;
                sqlx::query("INSERT INTO kep_hosted.event_journal (event_type, entity_id, event_json, previous_event_digest, event_digest) VALUES ($1, $2, $3, $4, $5)")
                    .bind(event_type)
                    .bind(entity_id)
                    .bind(event_json)
                    .bind(previous)
                    .bind(event_digest.as_slice())
                    .execute(&mut *transaction)
                    .await
                    .map_err(|error| format!("journal append failed: {error}"))?;
                for artifact in state.artifacts.values() {
                    let ciphertext = STANDARD
                        .decode(&artifact.ciphertext_base64)
                        .map_err(|_| "persisted ciphertext is not base64".to_string())?;
                    let digest = hex::decode(&artifact.ciphertext_sha256)
                        .map_err(|_| "persisted ciphertext digest is not hex".to_string())?;
                    sqlx::query("INSERT INTO kep_hosted.encrypted_archive (object_digest, encrypted_bytes) VALUES ($1, $2) ON CONFLICT (object_digest) DO NOTHING")
                        .bind(digest)
                        .bind(ciphertext)
                        .execute(&mut *transaction)
                        .await
                        .map_err(|error| format!("encrypted archive insert failed: {error}"))?;
                }
                transaction
                    .commit()
                    .await
                    .map_err(|error| format!("PostgreSQL commit failed: {error}"))
            }
        }
    }

    pub async fn record_client_error(&self, event: &ClientErrorEventRequest) -> Result<(), String> {
        match self {
            Self::Memory => Ok(()),
            Self::Postgres(pool) => {
                let diagnostic_digest = hex::decode(&event.diagnostic_digest)
                    .map_err(|_| "client error diagnostic digest is not hex".to_string())?;
                let canonical = serde_json::json!({
                    "attempt_id": event.attempt_id,
                    "operation_kind": event.operation_kind,
                    "stage": event.stage,
                    "error_code": event.error_code,
                    "effect_status": event.effect_status,
                    "network": event.network,
                    "safe_message": event.safe_message,
                    "diagnostic_digest": event.diagnostic_digest,
                    "rpc_request_id": event.rpc_request_id,
                    "transaction_signature": event.transaction_signature,
                    "reporter": event.reporter,
                    "registry_version": event.registry_version,
                    "source_layer": event.source_layer,
                    "retry_disposition": event.retry_disposition,
                    "http_status": event.http_status,
                    "rpc_code": event.rpc_code,
                    "transaction_error": event.transaction_error,
                    "instruction_index": event.instruction_index,
                    "instruction_error": event.instruction_error,
                    "program_id": event.program_id,
                    "custom_program_code": event.custom_program_code,
                    "correlation_id": event.correlation_id,
                });
                let mut hasher = Sha256::new();
                hasher.update(b"CA2-KEP-HOSTED-CLIENT-ERROR-v1");
                hasher.update(canonical.to_string().as_bytes());
                let event_digest: [u8; 32] = hasher.finalize().into();
                sqlx::query("INSERT INTO kep_hosted.client_error_journal (attempt_id, operation_kind, stage, error_code, effect_status, network, safe_message, diagnostic_digest, rpc_request_id, transaction_signature, event_digest, reporter, registry_version, source_layer, retry_disposition, http_status, rpc_code, transaction_error, instruction_index, instruction_error, program_id, custom_program_code, correlation_id) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23) ON CONFLICT (attempt_id) DO NOTHING")
                    .bind(&event.attempt_id)
                    .bind(&event.operation_kind)
                    .bind(&event.stage)
                    .bind(&event.error_code)
                    .bind(&event.effect_status)
                    .bind(&event.network)
                    .bind(&event.safe_message)
                    .bind(diagnostic_digest)
                    .bind(&event.rpc_request_id)
                    .bind(&event.transaction_signature)
                    .bind(event_digest.as_slice())
                    .bind(&event.reporter)
                    .bind(&event.registry_version)
                    .bind(&event.source_layer)
                    .bind(&event.retry_disposition)
                    .bind(event.http_status.map(i32::from))
                    .bind(event.rpc_code)
                    .bind(&event.transaction_error)
                    .bind(event.instruction_index.map(i32::from))
                    .bind(&event.instruction_error)
                    .bind(&event.program_id)
                    .bind(event.custom_program_code.map(i64::from))
                    .bind(&event.correlation_id)
                    .execute(pool)
                    .await
                    .map_err(|error| format!("client error journal append failed: {error}"))?;
                Ok(())
            }
        }
    }
}
