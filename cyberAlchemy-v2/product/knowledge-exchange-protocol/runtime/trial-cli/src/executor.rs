use std::{
    collections::{BTreeMap, BTreeSet},
    env, fs,
    fs::{File, OpenOptions},
    io::Write,
    path::{Path, PathBuf},
    thread,
    time::Duration,
};

use borsh::BorshDeserialize;
use cyberalchemy_kep_adapters::{
    production_profile, PostgresThreeLayerStorage, ProductionCryptography, Sha256Identity,
};
use cyberalchemy_kep_solana_program::{
    key_envelope_binding, ArtifactState, ProtocolInstruction, ReissueRequest, ARTIFACT_SEED,
    REISSUE_SEED, REPLAY_SEED,
};
use cyberalchemy_knowledge_exchange_protocol::{
    encrypted_durable_devnet::{
        cryptography::{ByteIdentityProvider, CryptographyError, CryptographyPort, KeyCustodyPort},
        durable_storage::{persist_and_verify_material, retrieve_verified},
        model::{
            CryptographicContext, OpaqueRecipientEnvelope, PreparedMaterial, RecipientBinding,
            SecretHandle, StorageLayer, StorageReadiness,
        },
    },
    Digest32,
};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use solana_client::{rpc_client::RpcClient, rpc_config::RpcSendTransactionConfig};
use solana_commitment_config::CommitmentConfig;
use solana_keypair::{read_keypair_file, Keypair};
use solana_loader_v3_interface::{
    get_program_data_address, instruction as loader_instruction, state::UpgradeableLoaderState,
};
use solana_sdk::{
    instruction::{AccountMeta, Instruction},
    pubkey::Pubkey,
    signature::Signer,
    transaction::Transaction,
};
use solana_sdk_ids::system_program;
use zeroize::Zeroizing;

use crate::{hex_lower, DevnetEnvelope, TrialGateError};

const DEPLOY_CHUNK_SIZE: usize = 768;
const SOLANA_PACKET_DATA_SIZE: u64 = 1_232;

#[derive(Debug, Serialize)]
pub(crate) struct TrialEvidence {
    schema_version: &'static str,
    result: &'static str,
    cluster: &'static str,
    genesis_hash: String,
    program_id: String,
    sbf_sha256: String,
    funding: FundingEvidence,
    deployment: DeploymentEvidence,
    storage: StorageEvidence,
    cases: Vec<CaseEvidence>,
    observations: Vec<ObservationEvidence>,
    finalized_grant_revision: u64,
    finalized_reissue_revision: u64,
    recipient_decryption: &'static str,
    replacement_recipient_decryption: &'static str,
    protocol_transaction_fee_lamports: u64,
    deployment_transaction_fee_lamports: u64,
    payer_balance_delta_lamports: u64,
    retained_program_rent_lamports: u64,
    storage_cost_observation: &'static str,
    knowledge_consideration_lamports: u64,
    protocol_signed_submissions: u16,
    authority_effect: &'static str,
    observed_external_effect: &'static str,
    authorization_attestation: &'static str,
    claim_ceiling: &'static str,
}

#[derive(Debug, Serialize)]
struct StorageEvidence {
    provider: &'static str,
    encrypted_object_count: u16,
    every_object_ready_in_three_layers: bool,
    locator_commitment_sha256: String,
}

#[derive(Debug, Serialize)]
struct FundingEvidence {
    mode: &'static str,
    observed_balance_lamports: u64,
    minimum_balance_lamports: u64,
    maximum_balance_lamports: u64,
    result: &'static str,
}

#[derive(Debug, Serialize)]
struct DeploymentEvidence {
    signed_submissions: u16,
    transactions: Vec<CaseEvidence>,
    programdata_address: String,
    program_rent_lamports: u64,
    programdata_rent_lamports: u64,
    remote_sbf_sha256: String,
    upgrade_authority: String,
}

#[derive(Debug, Serialize)]
struct CaseEvidence {
    case_id: String,
    expected: &'static str,
    observed: &'static str,
    signature: String,
    slot: Option<u64>,
    fee_lamports: u64,
    error_digest: Option<String>,
}

#[derive(Debug, Serialize)]
struct ObservationEvidence {
    case_id: &'static str,
    expected: &'static str,
    observed: &'static str,
    input_sha256: String,
    output_sha256: String,
}

struct DeploymentResult {
    cases: Vec<CaseEvidence>,
    programdata_address: Pubkey,
    program_rent_lamports: u64,
    programdata_rent_lamports: u64,
    remote_sbf_sha256: String,
    upgrade_authority: Pubkey,
}

struct FileCustody {
    paths: BTreeMap<SecretHandle, String>,
}

struct AttemptJournal {
    file: std::sync::Mutex<File>,
}

#[derive(Serialize)]
struct AttemptRecord<'a> {
    schema_version: &'static str,
    effect_id: &'a str,
    stage: &'a str,
    signature: Option<&'a str>,
    detail_sha256: Option<String>,
    failure_stage: Option<&'a str>,
    failure_class: Option<&'a str>,
}

#[derive(Clone, Debug, Eq, PartialEq, Serialize)]
struct SanitizedRpcFailure {
    stage: &'static str,
    class: &'static str,
    detail_sha256: String,
}

impl SanitizedRpcFailure {
    fn from_error(stage: &'static str, error: &impl std::fmt::Display) -> Self {
        let detail = error.to_string();
        let lower = detail.to_ascii_lowercase();
        let class = if lower.contains("429")
            || lower.contains("too many requests")
            || lower.contains("rate limit")
        {
            "rate-limited-rejection"
        } else if lower.contains("timeout")
            || lower.contains("timed out")
            || lower.contains("connection")
        {
            "transport-ambiguous"
        } else if lower.contains("rpc response") || lower.contains("rpc error") {
            "rpc-rejection"
        } else {
            "unclassified-rpc-or-transport"
        };
        Self {
            stage,
            class,
            detail_sha256: hex_lower(&Sha256::digest(detail.as_bytes())),
        }
    }

    fn into_gate_error(self) -> TrialGateError {
        TrialGateError::SolanaRpc {
            stage: self.stage,
            class: self.class,
            detail_sha256: self.detail_sha256,
        }
    }
}

impl AttemptJournal {
    fn create(path: &str) -> Result<Self, TrialGateError> {
        let file = OpenOptions::new()
            .create_new(true)
            .append(true)
            .open(path)
            .map_err(|error| {
                if error.kind() == std::io::ErrorKind::AlreadyExists {
                    TrialGateError::ReconciliationRequired
                } else {
                    TrialGateError::EvidenceWrite
                }
            })?;
        Ok(Self {
            file: std::sync::Mutex::new(file),
        })
    }

    fn open_existing(path: &str) -> Result<Self, TrialGateError> {
        let file = OpenOptions::new()
            .append(true)
            .open(path)
            .map_err(|_| TrialGateError::ReconciliationRequired)?;
        Ok(Self {
            file: std::sync::Mutex::new(file),
        })
    }

    fn record(
        &self,
        effect_id: &str,
        stage: &str,
        signature: Option<&str>,
        detail: Option<&[u8]>,
    ) -> Result<(), TrialGateError> {
        let record = AttemptRecord {
            schema_version: "cav2-kep-attempt-journal/v2",
            effect_id,
            stage,
            signature,
            detail_sha256: detail.map(|value| hex_lower(&Sha256::digest(value))),
            failure_stage: None,
            failure_class: None,
        };
        let mut raw = serde_json::to_vec(&record).map_err(|_| TrialGateError::EvidenceWrite)?;
        raw.push(b'\n');
        let mut file = self
            .file
            .lock()
            .map_err(|_| TrialGateError::EvidenceWrite)?;
        file.write_all(&raw)
            .and_then(|()| file.sync_all())
            .map_err(|_| TrialGateError::EvidenceWrite)
    }

    fn record_rpc_failure(
        &self,
        effect_id: &str,
        stage: &str,
        signature: Option<&str>,
        failure: &SanitizedRpcFailure,
    ) -> Result<(), TrialGateError> {
        let record = AttemptRecord {
            schema_version: "cav2-kep-attempt-journal/v2",
            effect_id,
            stage,
            signature,
            detail_sha256: Some(failure.detail_sha256.clone()),
            failure_stage: Some(failure.stage),
            failure_class: Some(failure.class),
        };
        let mut raw = serde_json::to_vec(&record).map_err(|_| TrialGateError::EvidenceWrite)?;
        raw.push(b'\n');
        let mut file = self
            .file
            .lock()
            .map_err(|_| TrialGateError::EvidenceWrite)?;
        file.write_all(&raw)
            .and_then(|()| file.sync_all())
            .map_err(|_| TrialGateError::EvidenceWrite)
    }
}

#[derive(Debug, Serialize)]
pub(crate) struct ReconciliationReceipt {
    schema_version: &'static str,
    result: &'static str,
    signatures_checked: usize,
    finalized_successes: usize,
    finalized_failures: usize,
    still_pending: usize,
    unsigned_ambiguous_effects: usize,
    proven_pre_effect_stops: usize,
    payer_balance_lamports: u64,
    resubmissions: u8,
    authority_effect: &'static str,
    local_effect: &'static str,
    observed_external_effect: &'static str,
    authorization_attestation: &'static str,
}

#[derive(Debug, Deserialize)]
struct ObservedAttemptRecord {
    stage: String,
    signature: Option<String>,
    #[serde(default)]
    failure_stage: Option<String>,
    #[serde(default)]
    failure_class: Option<String>,
}

#[derive(Debug, Default, Eq, PartialEq)]
struct JournalAnalysis {
    signatures: BTreeSet<String>,
    unsigned_ambiguous_effects: usize,
    proven_pre_effect_stops: usize,
}

fn analyze_attempt_journal(raw: &str) -> Result<JournalAnalysis, TrialGateError> {
    let mut analysis = JournalAnalysis::default();
    for line in raw.lines().filter(|line| !line.trim().is_empty()) {
        let record: ObservedAttemptRecord =
            serde_json::from_str(line).map_err(|_| TrialGateError::ReconciliationRequired)?;
        if let Some(signature) = record.signature {
            analysis.signatures.insert(signature);
            continue;
        }

        match (
            record.failure_stage.as_deref(),
            record.failure_class.as_deref(),
        ) {
            (
                Some("execution-genesis-hash" | "execution-prefunded-balance"),
                Some("rate-limited-rejection" | "rpc-rejection"),
            ) => analysis.proven_pre_effect_stops += 1,
            (Some(_), Some("transport-ambiguous" | "unclassified-rpc-or-transport")) => {
                analysis.unsigned_ambiguous_effects += 1;
            }
            (Some(_), Some(_)) | (Some(_), None) | (None, Some(_)) => {
                analysis.unsigned_ambiguous_effects += 1;
            }
            (None, None)
                if matches!(
                    record.stage.as_str(),
                    "genesis-hash-mismatch-proven-pre-effect"
                        | "prefunded-balance-insufficient"
                        | "prefunded-balance-above-authorized-maximum"
                ) =>
            {
                analysis.proven_pre_effect_stops += 1;
            }
            (None, None) => {}
        }
    }
    Ok(analysis)
}

fn reconciliation_result(
    signatures_checked: usize,
    still_pending: usize,
    unsigned_ambiguous_effects: usize,
    proven_pre_effect_stops: usize,
) -> &'static str {
    if still_pending > 0 || unsigned_ambiguous_effects > 0 {
        "PENDING"
    } else if signatures_checked > 0 {
        "RECONCILED"
    } else if proven_pre_effect_stops > 0 {
        "PROVEN_PRE_EFFECT_STOP"
    } else {
        "PENDING"
    }
}

fn validate_prefunded_balance(
    observed_lamports: u64,
    minimum_lamports: u64,
    maximum_lamports: u64,
) -> Result<(), TrialGateError> {
    if observed_lamports < minimum_lamports || observed_lamports > maximum_lamports {
        Err(TrialGateError::FundingPrerequisite {
            observed_lamports,
            minimum_lamports,
            maximum_lamports,
        })
    } else {
        Ok(())
    }
}

pub(crate) fn reconcile(
    envelope: &DevnetEnvelope,
) -> Result<ReconciliationReceipt, TrialGateError> {
    let repository = trusted_repository_root()?;
    let journal_path = Path::new(&envelope.external_inputs.attempt_journal_path)
        .canonicalize()
        .map_err(|_| TrialGateError::ReconciliationRequired)?;
    if journal_path.starts_with(repository) {
        return Err(TrialGateError::RepositoryBoundary);
    }
    let raw =
        fs::read_to_string(&journal_path).map_err(|_| TrialGateError::ReconciliationRequired)?;
    let analysis = analyze_attempt_journal(&raw)?;
    let signatures = analysis.signatures;
    let unsigned_ambiguous_effects = analysis.unsigned_ambiguous_effects;
    let proven_pre_effect_stops = analysis.proven_pre_effect_stops;
    let rpc =
        RpcClient::new_with_commitment(envelope.rpc_url.clone(), CommitmentConfig::finalized());
    let genesis = rpc.get_genesis_hash().map_err(|error| {
        SanitizedRpcFailure::from_error("reconcile-genesis-hash", &error).into_gate_error()
    })?;
    if genesis.to_string() != envelope.expected_genesis_hash {
        return Err(TrialGateError::Solana);
    }
    let journal = AttemptJournal::open_existing(
        journal_path
            .to_str()
            .ok_or(TrialGateError::ReconciliationRequired)?,
    )?;
    let payer = keypair(&envelope.external_inputs.payer_keypair_path)?;
    let payer_balance_lamports = rpc.get_balance(&payer.pubkey()).map_err(|error| {
        SanitizedRpcFailure::from_error("reconcile-payer-balance", &error).into_gate_error()
    })?;
    let mut successes = 0;
    let mut failures = 0;
    let mut pending = 0;
    for encoded in &signatures {
        let signature = encoded
            .parse()
            .map_err(|_| TrialGateError::ReconciliationRequired)?;
        match rpc
            .get_signature_status_with_commitment_and_history(
                &signature,
                CommitmentConfig::finalized(),
                true,
            )
            .map_err(|error| {
                SanitizedRpcFailure::from_error("reconcile-signature-status", &error)
                    .into_gate_error()
            })? {
            Some(Ok(())) => {
                successes += 1;
                journal.record(
                    "reconciliation",
                    "reconciled-finalized-success",
                    Some(encoded),
                    None,
                )?;
            }
            Some(Err(error)) => {
                failures += 1;
                journal.record(
                    "reconciliation",
                    "reconciled-finalized-failure",
                    Some(encoded),
                    Some(error.to_string().as_bytes()),
                )?;
            }
            None => {
                pending += 1;
                journal.record(
                    "reconciliation",
                    "reconciled-still-pending",
                    Some(encoded),
                    None,
                )?;
            }
        }
    }
    Ok(ReconciliationReceipt {
        schema_version: "cav2-kep-devnet-reconciliation/v2",
        result: reconciliation_result(
            signatures.len(),
            pending,
            unsigned_ambiguous_effects,
            proven_pre_effect_stops,
        ),
        signatures_checked: signatures.len(),
        finalized_successes: successes,
        finalized_failures: failures,
        still_pending: pending,
        unsigned_ambiguous_effects,
        proven_pre_effect_stops,
        payer_balance_lamports,
        resubmissions: 0,
        authority_effect: "none",
        local_effect: "appended-reconciliation-observations-to-external-journal",
        observed_external_effect: "read-finalized-solana-signature-statuses-no-resubmission",
        authorization_attestation: "external-not-attested-by-runner",
    })
}

impl KeyCustodyPort for FileCustody {
    fn with_secret<R>(
        &self,
        handle: &SecretHandle,
        operation: impl FnOnce(&[u8]) -> Result<R, CryptographyError>,
    ) -> Result<R, CryptographyError> {
        let path = self
            .paths
            .get(handle)
            .ok_or(CryptographyError::SecretHandleMismatch)?;
        let secret =
            Zeroizing::new(fs::read(path).map_err(|_| CryptographyError::CustodyUnavailable)?);
        if secret.len() != 32 {
            return Err(CryptographyError::InvalidMaterial);
        }
        operation(&secret)
    }
}

struct SubmissionBudget {
    used: u16,
    limit: u16,
}

struct PreparedTrial {
    cryptography: ProductionCryptography<FileCustody>,
    material: PreparedMaterial,
    originator_binding: RecipientBinding,
    recipient_binding: RecipientBinding,
    replacement_binding: RecipientBinding,
    replacement_envelope: OpaqueRecipientEnvelope,
    plaintext: Zeroizing<Vec<u8>>,
}

impl SubmissionBudget {
    fn consume(&mut self) -> Result<(), TrialGateError> {
        if self.used >= self.limit {
            Err(TrialGateError::ProtocolBudget)
        } else {
            self.used += 1;
            Ok(())
        }
    }
}

fn digest(label: &[u8]) -> Digest32 {
    let bytes: [u8; 32] = Sha256::digest(label).into();
    Digest32::try_new(bytes).expect("SHA-256 cannot be the zero digest")
}

fn commitment(label: &[u8]) -> [u8; 32] {
    Sha256::digest(label).into()
}

fn raw32(path: &str) -> Result<[u8; 32], TrialGateError> {
    fs::read(path)
        .map_err(|_| TrialGateError::ExternalMaterial)?
        .try_into()
        .map_err(|_| TrialGateError::ExternalMaterial)
}

fn keypair(path: &str) -> Result<Keypair, TrialGateError> {
    read_keypair_file(path).map_err(|_| TrialGateError::ExternalMaterial)
}

fn ensure_external_paths(envelope: &DevnetEnvelope) -> Result<(), TrialGateError> {
    let repository = trusted_repository_root()?;
    let inputs = &envelope.external_inputs;
    let existing = [
        &envelope.sbf_path,
        &inputs.payer_keypair_path,
        &inputs.originator_keypair_path,
        &inputs.recipient_keypair_path,
        &inputs.outsider_keypair_path,
        &inputs.program_keypair_path,
        &inputs.buffer_keypair_path,
        &inputs.upgrade_authority_keypair_path,
        &inputs.plaintext_fixture_path,
        &inputs.originator_hpke_public_path,
        &inputs.originator_hpke_private_path,
        &inputs.recipient_hpke_public_path,
        &inputs.recipient_hpke_private_path,
        &inputs.replacement_hpke_public_path,
        &inputs.replacement_hpke_private_path,
    ];
    let mut distinct_paths = BTreeSet::new();
    for selected in existing {
        let path = Path::new(selected)
            .canonicalize()
            .map_err(|_| TrialGateError::ExternalMaterial)?;
        if path.starts_with(&repository) || !distinct_paths.insert(path) {
            return Err(TrialGateError::RepositoryBoundary);
        }
    }
    if Path::new(&inputs.evidence_output_path).exists() {
        return Err(TrialGateError::EvidenceWrite);
    }
    if Path::new(&inputs.evidence_output_path) == Path::new(&inputs.attempt_journal_path) {
        return Err(TrialGateError::RepositoryBoundary);
    }
    for output in [&inputs.evidence_output_path, &inputs.attempt_journal_path] {
        let output_parent = Path::new(output)
            .parent()
            .ok_or(TrialGateError::RepositoryBoundary)?
            .canonicalize()
            .map_err(|_| TrialGateError::RepositoryBoundary)?;
        if output_parent.starts_with(&repository) {
            return Err(TrialGateError::RepositoryBoundary);
        }
    }
    Ok(())
}

fn trusted_repository_root() -> Result<PathBuf, TrialGateError> {
    let manifest_dir = Path::new(env!("CARGO_MANIFEST_DIR"))
        .canonicalize()
        .map_err(|_| TrialGateError::RepositoryBoundary)?;
    let repository = manifest_dir
        .ancestors()
        .nth(5)
        .ok_or(TrialGateError::RepositoryBoundary)?
        .to_path_buf();
    if repository
        .join("cyberAlchemy-v2/product/knowledge-exchange-protocol/runtime/trial-cli")
        .canonicalize()
        .map_err(|_| TrialGateError::RepositoryBoundary)?
        != manifest_dir
    {
        return Err(TrialGateError::RepositoryBoundary);
    }
    Ok(repository)
}

fn prepare_material(envelope: &DevnetEnvelope) -> Result<PreparedTrial, TrialGateError> {
    let inputs = &envelope.external_inputs;
    let plaintext = Zeroizing::new(
        fs::read(&inputs.plaintext_fixture_path).map_err(|_| TrialGateError::ExternalMaterial)?,
    );
    if plaintext.is_empty() {
        return Err(TrialGateError::ExternalMaterial);
    }
    let a_public = raw32(&inputs.originator_hpke_public_path)?;
    let b_public = raw32(&inputs.recipient_hpke_public_path)?;
    let b2_public = raw32(&inputs.replacement_hpke_public_path)?;
    if a_public == b_public || a_public == b2_public || b_public == b2_public {
        return Err(TrialGateError::ExternalMaterial);
    }
    let a_handle = SecretHandle("originator-hpke-v1".to_owned());
    let b_handle = SecretHandle("recipient-hpke-v1".to_owned());
    let b2_handle = SecretHandle("recipient-hpke-v2".to_owned());
    let custody = FileCustody {
        paths: BTreeMap::from([
            (
                a_handle.clone(),
                inputs.originator_hpke_private_path.clone(),
            ),
            (b_handle.clone(), inputs.recipient_hpke_private_path.clone()),
            (
                b2_handle.clone(),
                inputs.replacement_hpke_private_path.clone(),
            ),
        ]),
    };
    let cryptography = ProductionCryptography::new(custody);
    let a = RecipientBinding {
        recipient_id: digest(b"CA2-DEVNET-A"),
        key_binding_id: digest(&a_public),
        key_binding_version: 1,
        key_fingerprint: digest(&[b"fingerprint-a".as_slice(), &a_public].concat()),
    };
    let b = RecipientBinding {
        recipient_id: digest(b"CA2-DEVNET-B"),
        key_binding_id: digest(&b_public),
        key_binding_version: 1,
        key_fingerprint: digest(&[b"fingerprint-b".as_slice(), &b_public].concat()),
    };
    let b2 = RecipientBinding {
        recipient_id: b.recipient_id,
        key_binding_id: digest(&b2_public),
        key_binding_version: 2,
        key_fingerprint: digest(&[b"fingerprint-b2".as_slice(), &b2_public].concat()),
    };
    cryptography
        .keys()
        .register(a.key_binding_id, a_public, a_handle);
    cryptography
        .keys()
        .register(b.key_binding_id, b_public, b_handle);
    cryptography
        .keys()
        .register(b2.key_binding_id, b2_public, b2_handle);
    let identity = Sha256Identity;
    let mut opaque_artifact_id = [0_u8; 32];
    getrandom::fill(&mut opaque_artifact_id).map_err(|_| TrialGateError::Cryptography)?;
    let context = CryptographicContext {
        artifact_version_id: Digest32::try_new(opaque_artifact_id)
            .map_err(|_| TrialGateError::Cryptography)?,
        policy_id: digest(b"CA2-KEP-NO-PRICE-POLICY-v1"),
        encryption_epoch: 1,
        plaintext_commitment: identity.digest(&plaintext),
    };
    let profile = production_profile(digest(b"CA2-KEP-PRODUCTION-CRYPTO-v1"));
    let material = cryptography
        .prepare(
            &profile,
            &context,
            &plaintext,
            &[a.clone(), b.clone()],
            &identity,
        )
        .map_err(|_| TrialGateError::Cryptography)?;
    for recipient in [&a, &b] {
        let opened = cryptography
            .open(&profile, &context, &material, recipient, &identity)
            .map_err(|_| TrialGateError::Cryptography)?;
        if opened != plaintext.as_slice() {
            return Err(TrialGateError::Cryptography);
        }
    }
    let replacement_envelope = cryptography
        .rewrap_for_reissue(&material, &a, &b2, b2_public, &identity)
        .map_err(|_| TrialGateError::Cryptography)?;
    let mut replacement_material = material.clone();
    replacement_material
        .envelopes
        .retain(|item| item.recipient.recipient_id != b.recipient_id);
    replacement_material
        .envelopes
        .push(replacement_envelope.clone());
    let replacement_opened = cryptography
        .open(&profile, &context, &replacement_material, &b2, &identity)
        .map_err(|_| TrialGateError::Cryptography)?;
    if replacement_opened != plaintext.as_slice() {
        return Err(TrialGateError::Cryptography);
    }
    Ok(PreparedTrial {
        cryptography,
        material,
        originator_binding: a,
        recipient_binding: b,
        replacement_binding: b2,
        replacement_envelope,
        plaintext,
    })
}

async fn persist(
    storage: &mut PostgresThreeLayerStorage,
    bytes: &[u8],
) -> Result<StorageReadiness, TrialGateError> {
    let (readiness, _) = persist_and_verify_material(storage, &Sha256Identity, 1, bytes)
        .await
        .map_err(|_| TrialGateError::Storage)?;
    if !readiness.is_ready() {
        return Err(TrialGateError::Storage);
    }
    Ok(readiness)
}

fn locator_commitment(readiness: &[StorageReadiness]) -> [u8; 32] {
    let mut hasher = Sha256::new();
    hasher.update(b"CA2-KEP-LOCATOR-COMMITMENT-v1");
    for object in readiness {
        for layer in cyberalchemy_knowledge_exchange_protocol::encrypted_durable_devnet::model::StorageLayer::REQUIRED {
            let locator = object.locator(layer).expect("ready storage has every locator");
            hasher.update([layer as u8]);
            hasher.update(locator.token.as_bytes());
        }
    }
    hasher.finalize().into()
}

fn protocol_instruction(
    program_id: Pubkey,
    data: ProtocolInstruction,
    accounts: Vec<AccountMeta>,
) -> Result<Instruction, TrialGateError> {
    Ok(Instruction {
        program_id,
        accounts,
        data: borsh::to_vec(&data).map_err(|_| TrialGateError::Solana)?,
    })
}

fn signed_transaction(
    rpc: &RpcClient,
    instruction: Instruction,
    payer: &Keypair,
    additional_signers: &[&Keypair],
) -> Result<Transaction, TrialGateError> {
    signed_instructions(rpc, &[instruction], payer, additional_signers)
}

fn signed_instructions(
    rpc: &RpcClient,
    instructions: &[Instruction],
    payer: &Keypair,
    additional_signers: &[&Keypair],
) -> Result<Transaction, TrialGateError> {
    let blockhash = rpc
        .get_latest_blockhash()
        .map_err(|_| TrialGateError::Solana)?;
    let mut signers: Vec<&dyn Signer> = vec![payer];
    signers.extend(additional_signers.iter().map(|item| *item as &dyn Signer));
    let transaction = Transaction::new_signed_with_payer(
        instructions,
        Some(&payer.pubkey()),
        &signers,
        blockhash,
    );
    if bincode::serialized_size(&transaction).map_err(|_| TrialGateError::Solana)?
        > SOLANA_PACKET_DATA_SIZE
    {
        return Err(TrialGateError::DeploymentBudgetImpossible);
    }
    Ok(transaction)
}

fn submit_success(
    rpc: &RpcClient,
    journal: &AttemptJournal,
    budget: &mut SubmissionBudget,
    case_id: &str,
    transaction: Transaction,
) -> Result<CaseEvidence, TrialGateError> {
    budget.consume()?;
    let local_signature = transaction.signatures[0].to_string();
    journal.record(
        case_id,
        "signed-before-submit",
        Some(&local_signature),
        None,
    )?;
    let fee = rpc
        .get_fee_for_message(&transaction.message)
        .map_err(|_| TrialGateError::Solana)?;
    let signature = match rpc.send_transaction_with_config(
        &transaction,
        RpcSendTransactionConfig {
            preflight_commitment: Some(CommitmentConfig::processed().commitment),
            max_retries: Some(0),
            ..RpcSendTransactionConfig::default()
        },
    ) {
        Ok(signature) => signature,
        Err(error) => {
            journal.record(
                case_id,
                "ambiguous-send-error",
                Some(&local_signature),
                Some(error.to_string().as_bytes()),
            )?;
            return Err(TrialGateError::Solana);
        }
    };
    journal.record(case_id, "submitted", Some(&signature.to_string()), None)?;
    let outcome = match wait_for_finalized(rpc, &signature) {
        Ok(outcome) => outcome,
        Err(error) => {
            journal.record(
                case_id,
                "ambiguous-finality-timeout-or-query-error",
                Some(&signature.to_string()),
                None,
            )?;
            return Err(error);
        }
    };
    if outcome.is_err() {
        journal.record(
            case_id,
            "finalized-failure",
            Some(&signature.to_string()),
            outcome.err().as_deref().map(str::as_bytes),
        )?;
        return Err(TrialGateError::Solana);
    }
    journal.record(
        case_id,
        "finalized-success",
        Some(&signature.to_string()),
        None,
    )?;
    let statuses = rpc
        .get_signature_statuses_with_history(&[signature])
        .map_err(|_| TrialGateError::Solana)?;
    let slot = statuses
        .value
        .first()
        .and_then(|item| item.as_ref().map(|value| value.slot))
        .ok_or(TrialGateError::Solana)?;
    Ok(CaseEvidence {
        case_id: case_id.to_owned(),
        expected: "success-finalized",
        observed: "success-finalized",
        signature: signature.to_string(),
        slot: Some(slot),
        fee_lamports: fee,
        error_digest: None,
    })
}

fn submit_rejection(
    rpc: &RpcClient,
    journal: &AttemptJournal,
    budget: &mut SubmissionBudget,
    case_id: &str,
    transaction: Transaction,
) -> Result<CaseEvidence, TrialGateError> {
    budget.consume()?;
    let local_signature = transaction.signatures[0].to_string();
    journal.record(
        case_id,
        "signed-before-submit",
        Some(&local_signature),
        None,
    )?;
    let fee = rpc.get_fee_for_message(&transaction.message).unwrap_or(0);
    let signature = match rpc.send_transaction_with_config(
        &transaction,
        RpcSendTransactionConfig {
            skip_preflight: true,
            max_retries: Some(0),
            ..RpcSendTransactionConfig::default()
        },
    ) {
        Ok(signature) => signature,
        Err(error) => {
            journal.record(
                case_id,
                "ambiguous-send-error",
                Some(&local_signature),
                Some(error.to_string().as_bytes()),
            )?;
            return Err(TrialGateError::Solana);
        }
    };
    journal.record(case_id, "submitted", Some(&signature.to_string()), None)?;
    let outcome = match wait_for_finalized(rpc, &signature) {
        Ok(outcome) => outcome,
        Err(error) => {
            journal.record(
                case_id,
                "ambiguous-finality-timeout-or-query-error",
                Some(&signature.to_string()),
                None,
            )?;
            return Err(error);
        }
    };
    let error = outcome
        .err()
        .ok_or(TrialGateError::NegativeCaseUnexpectedlySucceeded)?;
    journal.record(
        case_id,
        "finalized-expected-failure",
        Some(&signature.to_string()),
        Some(error.as_bytes()),
    )?;
    let statuses = rpc
        .get_signature_statuses_with_history(&[signature])
        .map_err(|_| TrialGateError::Solana)?;
    let slot = statuses
        .value
        .first()
        .and_then(|item| item.as_ref().map(|value| value.slot))
        .ok_or(TrialGateError::Solana)?;
    Ok(CaseEvidence {
        case_id: case_id.to_owned(),
        expected: "rejected-finalized-no-state-change",
        observed: "rejected-finalized-no-state-change",
        signature: signature.to_string(),
        slot: Some(slot),
        fee_lamports: fee,
        error_digest: Some(hex_lower(&Sha256::digest(error.as_bytes()))),
    })
}

fn wait_for_finalized(
    rpc: &RpcClient,
    signature: &solana_sdk::signature::Signature,
) -> Result<Result<(), String>, TrialGateError> {
    for _ in 0..240 {
        let status = rpc
            .get_signature_status_with_commitment_and_history(
                signature,
                CommitmentConfig::finalized(),
                true,
            )
            .map_err(|_| TrialGateError::Solana)?;
        if let Some(outcome) = status {
            return Ok(outcome.map_err(|error| error.to_string()));
        }
        thread::sleep(Duration::from_millis(500));
    }
    Err(TrialGateError::Solana)
}

fn finalized_artifact(
    rpc: &RpcClient,
    program_id: Pubkey,
    artifact: Pubkey,
) -> Result<ArtifactState, TrialGateError> {
    let account = rpc
        .get_account_with_commitment(&artifact, CommitmentConfig::finalized())
        .map_err(|_| TrialGateError::Solana)?
        .value
        .ok_or(TrialGateError::Solana)?;
    if account.owner != program_id {
        return Err(TrialGateError::Solana);
    }
    ArtifactState::try_from_slice(&account.data).map_err(|_| TrialGateError::Solana)
}

#[allow(deprecated)]
fn deploy(
    rpc: &RpcClient,
    journal: &AttemptJournal,
    envelope: &DevnetEnvelope,
    payer: &Keypair,
    program: &Keypair,
    buffer: &Keypair,
    upgrade_authority: &Keypair,
) -> Result<DeploymentResult, TrialGateError> {
    let sbf = fs::read(&envelope.sbf_path).map_err(|_| TrialGateError::SbfIdentity)?;
    if rpc.get_account(&program.pubkey()).is_ok() || rpc.get_account(&buffer.pubkey()).is_ok() {
        return Err(TrialGateError::Solana);
    }
    let mut budget = SubmissionBudget {
        used: 0,
        limit: envelope.max_deployment_signed_transactions,
    };
    let mut cases = Vec::new();
    let buffer_rent = rpc
        .get_minimum_balance_for_rent_exemption(UpgradeableLoaderState::size_of_buffer(sbf.len()))
        .map_err(|_| TrialGateError::Solana)?;
    let create = loader_instruction::create_buffer(
        &payer.pubkey(),
        &buffer.pubkey(),
        &upgrade_authority.pubkey(),
        buffer_rent,
        sbf.len(),
    )
    .map_err(|_| TrialGateError::Solana)?;
    cases.push(submit_success(
        rpc,
        journal,
        &mut budget,
        "deployment-buffer-create",
        signed_instructions(rpc, &create, payer, &[buffer])?,
    )?);
    for (index, chunk) in sbf.chunks(DEPLOY_CHUNK_SIZE).enumerate() {
        let write = loader_instruction::write(
            &buffer.pubkey(),
            &upgrade_authority.pubkey(),
            u32::try_from(index * DEPLOY_CHUNK_SIZE)
                .map_err(|_| TrialGateError::DeploymentBudgetImpossible)?,
            chunk.to_vec(),
        );
        cases.push(submit_success(
            rpc,
            journal,
            &mut budget,
            &format!("deployment-write-{index:03}"),
            signed_transaction(rpc, write, payer, &[upgrade_authority])?,
        )?);
    }
    let program_rent = rpc
        .get_minimum_balance_for_rent_exemption(UpgradeableLoaderState::size_of_program())
        .map_err(|_| TrialGateError::Solana)?;
    let finalize = loader_instruction::deploy_with_max_program_len(
        &payer.pubkey(),
        &program.pubkey(),
        &buffer.pubkey(),
        &upgrade_authority.pubkey(),
        program_rent,
        sbf.len(),
    )
    .map_err(|_| TrialGateError::Solana)?;
    cases.push(submit_success(
        rpc,
        journal,
        &mut budget,
        "deployment-finalize",
        signed_instructions(rpc, &finalize, payer, &[program, upgrade_authority])?,
    )?);
    if budget.used > envelope.max_deployment_signed_transactions {
        return Err(TrialGateError::DeploymentBudgetImpossible);
    }
    let program_account = rpc
        .get_account_with_commitment(&program.pubkey(), CommitmentConfig::finalized())
        .map_err(|_| TrialGateError::Solana)?
        .value
        .ok_or(TrialGateError::Solana)?;
    if !program_account.executable
        || program_account.owner != solana_sdk_ids::bpf_loader_upgradeable::id()
    {
        return Err(TrialGateError::Solana);
    }
    let program_state: UpgradeableLoaderState =
        bincode::deserialize(&program_account.data).map_err(|_| TrialGateError::Solana)?;
    let programdata_address = get_program_data_address(&program.pubkey());
    if program_state
        != (UpgradeableLoaderState::Program {
            programdata_address,
        })
    {
        return Err(TrialGateError::Solana);
    }
    let programdata = rpc
        .get_account_with_commitment(&programdata_address, CommitmentConfig::finalized())
        .map_err(|_| TrialGateError::Solana)?
        .value
        .ok_or(TrialGateError::Solana)?;
    if programdata.owner != solana_sdk_ids::bpf_loader_upgradeable::id() {
        return Err(TrialGateError::Solana);
    }
    let metadata_size = UpgradeableLoaderState::size_of_programdata_metadata();
    let metadata: UpgradeableLoaderState = bincode::deserialize(
        programdata
            .data
            .get(..metadata_size)
            .ok_or(TrialGateError::Solana)?,
    )
    .map_err(|_| TrialGateError::Solana)?;
    match metadata {
        UpgradeableLoaderState::ProgramData {
            upgrade_authority_address: Some(authority),
            ..
        } if authority == upgrade_authority.pubkey() => {}
        _ => return Err(TrialGateError::Solana),
    }
    let remote_bytes = programdata
        .data
        .get(metadata_size..)
        .ok_or(TrialGateError::Solana)?;
    if remote_bytes != sbf {
        return Err(TrialGateError::Solana);
    }
    Ok(DeploymentResult {
        cases,
        programdata_address,
        program_rent_lamports: program_account.lamports,
        programdata_rent_lamports: programdata.lamports,
        remote_sbf_sha256: hex_lower(&Sha256::digest(remote_bytes)),
        upgrade_authority: upgrade_authority.pubkey(),
    })
}

pub(crate) async fn execute(envelope: &DevnetEnvelope) -> Result<TrialEvidence, TrialGateError> {
    ensure_external_paths(envelope)?;
    let journal = AttemptJournal::create(&envelope.external_inputs.attempt_journal_path)?;
    journal.record("trial", "operator-invoked-execution-start", None, None)?;
    let database_url = env::var("KEP_POSTGRES_TRIAL_URL").map_err(|_| TrialGateError::Storage)?;
    let parsed_database_url =
        url::Url::parse(&database_url).map_err(|_| TrialGateError::Storage)?;
    if !matches!(parsed_database_url.scheme(), "postgres" | "postgresql")
        || !matches!(
            parsed_database_url.host_str(),
            Some("127.0.0.1" | "localhost" | "::1")
        )
    {
        return Err(TrialGateError::Storage);
    }

    let inputs = &envelope.external_inputs;
    let payer = keypair(&inputs.payer_keypair_path)?;
    let originator = keypair(&inputs.originator_keypair_path)?;
    let recipient = keypair(&inputs.recipient_keypair_path)?;
    let outsider = keypair(&inputs.outsider_keypair_path)?;
    let program = keypair(&inputs.program_keypair_path)?;
    let buffer = keypair(&inputs.buffer_keypair_path)?;
    let upgrade_authority = keypair(&inputs.upgrade_authority_keypair_path)?;
    let wallet_keys = [
        payer.pubkey(),
        originator.pubkey(),
        recipient.pubkey(),
        outsider.pubkey(),
        program.pubkey(),
        buffer.pubkey(),
        upgrade_authority.pubkey(),
    ];
    if wallet_keys.iter().collect::<BTreeSet<_>>().len() != wallet_keys.len() {
        return Err(TrialGateError::ExternalMaterial);
    }
    let rpc =
        RpcClient::new_with_commitment(envelope.rpc_url.clone(), CommitmentConfig::finalized());
    let genesis = match rpc.get_genesis_hash() {
        Ok(genesis) => genesis,
        Err(error) => {
            let failure = SanitizedRpcFailure::from_error("execution-genesis-hash", &error);
            journal.record_rpc_failure(
                "devnet-cluster",
                "genesis-hash-query-failed",
                None,
                &failure,
            )?;
            return Err(failure.into_gate_error());
        }
    };
    if genesis.to_string() != envelope.expected_genesis_hash {
        journal.record(
            "devnet-cluster",
            "genesis-hash-mismatch-proven-pre-effect",
            None,
            None,
        )?;
        return Err(TrialGateError::Solana);
    }
    let prefunded_balance = match rpc.get_balance(&payer.pubkey()) {
        Ok(balance) => balance,
        Err(error) => {
            let failure = SanitizedRpcFailure::from_error("execution-prefunded-balance", &error);
            journal.record_rpc_failure(
                "devnet-funding",
                "prefunded-balance-query-failed",
                None,
                &failure,
            )?;
            return Err(failure.into_gate_error());
        }
    };
    if let Err(error) = validate_prefunded_balance(
        prefunded_balance,
        envelope.minimum_prefunded_lamports,
        envelope.maximum_prefunded_lamports,
    ) {
        let stage = if prefunded_balance < envelope.minimum_prefunded_lamports {
            "prefunded-balance-insufficient"
        } else {
            "prefunded-balance-above-authorized-maximum"
        };
        journal.record("devnet-funding", stage, None, None)?;
        return Err(error);
    }
    journal.record("devnet-funding", "prefunded-balance-verified", None, None)?;
    let funding = FundingEvidence {
        mode: "prefunded-only",
        observed_balance_lamports: prefunded_balance,
        minimum_balance_lamports: envelope.minimum_prefunded_lamports,
        maximum_balance_lamports: envelope.maximum_prefunded_lamports,
        result: "prefunded-balance-verified",
    };

    let PreparedTrial {
        cryptography,
        material,
        originator_binding: a_binding,
        recipient_binding: b_binding,
        replacement_binding: b2_binding,
        replacement_envelope,
        plaintext,
    } = prepare_material(envelope)?;
    let identity = Sha256Identity;
    let profile = production_profile(material.profile_id);
    let mut storage = PostgresThreeLayerStorage::connect(&database_url, 4)
        .await
        .map_err(|_| TrialGateError::Storage)?;
    let a_envelope = material
        .envelopes
        .iter()
        .find(|item| item.recipient == a_binding)
        .ok_or(TrialGateError::Cryptography)?;
    let b_envelope = material
        .envelopes
        .iter()
        .find(|item| item.recipient == b_binding)
        .ok_or(TrialGateError::Cryptography)?;
    journal.record(
        "storage-initial-material",
        "write-before-effect",
        None,
        None,
    )?;
    let ciphertext_readiness = persist(&mut storage, &material.ciphertext).await?;
    let a_readiness = persist(&mut storage, &a_envelope.envelope_bytes).await?;
    let b_readiness = persist(&mut storage, &b_envelope.envelope_bytes).await?;
    let mut readiness = vec![
        ciphertext_readiness.clone(),
        a_readiness.clone(),
        b_readiness.clone(),
    ];
    let durable_locator_commitment = locator_commitment(&readiness);
    journal.record(
        "storage-initial-material",
        "three-layer-verified",
        None,
        Some(&durable_locator_commitment),
    )?;

    let funded_balance = prefunded_balance;
    let deployment = deploy(
        &rpc,
        &journal,
        envelope,
        &payer,
        &program,
        &buffer,
        &upgrade_authority,
    )?;

    let program_id = program.pubkey();
    let artifact_id = *material.context.artifact_version_id.as_bytes();
    let (artifact, _) = Pubkey::find_program_address(&[ARTIFACT_SEED, &artifact_id], &program_id);
    let mut budget = SubmissionBudget {
        used: 0,
        limit: envelope.max_protocol_signed_transactions,
    };
    let mut cases = Vec::new();
    let op_init = commitment(b"initialize-v1");
    let (init_replay, _) =
        Pubkey::find_program_address(&[REPLAY_SEED, &artifact_id, &op_init], &program_id);
    let init = protocol_instruction(
        program_id,
        ProtocolInstruction::InitializeArtifact {
            artifact_id,
            policy_commitment: *material.context.policy_id.as_bytes(),
            epoch: material.context.encryption_epoch,
            ciphertext_commitment: *material.ciphertext_identity.digest.as_bytes(),
            originator_envelope_commitment: *a_envelope.envelope_identity.digest.as_bytes(),
            locator_commitment: durable_locator_commitment,
            operation_id: op_init,
        },
        vec![
            AccountMeta::new(payer.pubkey(), true),
            AccountMeta::new_readonly(originator.pubkey(), true),
            AccountMeta::new(artifact, false),
            AccountMeta::new(init_replay, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
    )?;
    cases.push(submit_success(
        &rpc,
        &journal,
        &mut budget,
        "initialize-positive",
        signed_transaction(&rpc, init, &payer, &[&originator])?,
    )?);
    let initialized_state = finalized_artifact(&rpc, program_id, artifact)?;
    if initialized_state.originator != originator.pubkey()
        || initialized_state.has_recipient
        || initialized_state.revision != 0
    {
        return Err(TrialGateError::Solana);
    }

    let op_wrong = commitment(b"grant-wrong-signer-v1");
    let (wrong_replay, _) =
        Pubkey::find_program_address(&[REPLAY_SEED, &artifact_id, &op_wrong], &program_id);
    let grant_wrong = protocol_instruction(
        program_id,
        ProtocolInstruction::GrantCoownership {
            recipient: recipient.pubkey(),
            recipient_key_commitment: *b_binding.key_binding_id.as_bytes(),
            recipient_envelope_commitment: *b_envelope.envelope_identity.digest.as_bytes(),
            expected_revision: 0,
            operation_id: op_wrong,
        },
        vec![
            AccountMeta::new(payer.pubkey(), true),
            AccountMeta::new_readonly(outsider.pubkey(), true),
            AccountMeta::new(artifact, false),
            AccountMeta::new(wrong_replay, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
    )?;
    cases.push(submit_rejection(
        &rpc,
        &journal,
        &mut budget,
        "grant-wrong-signer",
        signed_transaction(&rpc, grant_wrong, &payer, &[&outsider])?,
    )?);
    if finalized_artifact(&rpc, program_id, artifact)? != initialized_state {
        return Err(TrialGateError::Solana);
    }

    let op_stale = commitment(b"grant-stale-v1");
    let (stale_replay, _) =
        Pubkey::find_program_address(&[REPLAY_SEED, &artifact_id, &op_stale], &program_id);
    let grant_stale = protocol_instruction(
        program_id,
        ProtocolInstruction::GrantCoownership {
            recipient: recipient.pubkey(),
            recipient_key_commitment: *b_binding.key_binding_id.as_bytes(),
            recipient_envelope_commitment: *b_envelope.envelope_identity.digest.as_bytes(),
            expected_revision: 9,
            operation_id: op_stale,
        },
        vec![
            AccountMeta::new(payer.pubkey(), true),
            AccountMeta::new_readonly(originator.pubkey(), true),
            AccountMeta::new(artifact, false),
            AccountMeta::new(stale_replay, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
    )?;
    cases.push(submit_rejection(
        &rpc,
        &journal,
        &mut budget,
        "grant-stale-revision",
        signed_transaction(&rpc, grant_stale, &payer, &[&originator])?,
    )?);
    if finalized_artifact(&rpc, program_id, artifact)? != initialized_state {
        return Err(TrialGateError::Solana);
    }

    let op_grant = commitment(b"grant-positive-v1");
    let (grant_replay, _) =
        Pubkey::find_program_address(&[REPLAY_SEED, &artifact_id, &op_grant], &program_id);
    let grant = protocol_instruction(
        program_id,
        ProtocolInstruction::GrantCoownership {
            recipient: recipient.pubkey(),
            recipient_key_commitment: *b_binding.key_binding_id.as_bytes(),
            recipient_envelope_commitment: *b_envelope.envelope_identity.digest.as_bytes(),
            expected_revision: 0,
            operation_id: op_grant,
        },
        vec![
            AccountMeta::new(payer.pubkey(), true),
            AccountMeta::new_readonly(originator.pubkey(), true),
            AccountMeta::new(artifact, false),
            AccountMeta::new(grant_replay, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
    )?;
    cases.push(submit_success(
        &rpc,
        &journal,
        &mut budget,
        "grant-positive",
        signed_transaction(&rpc, grant, &payer, &[&originator])?,
    )?);
    let grant_state = finalized_artifact(&rpc, program_id, artifact)?;
    if grant_state.originator != originator.pubkey()
        || grant_state.recipient != recipient.pubkey()
        || !grant_state.has_recipient
        || grant_state.revision != 1
        || grant_state.recipient_key_commitment != *b_binding.key_binding_id.as_bytes()
        || grant_state.recipient_key_envelope_binding
            != key_envelope_binding(
                b_binding.key_binding_id.as_bytes(),
                b_envelope.envelope_identity.digest.as_bytes(),
            )
    {
        return Err(TrialGateError::Solana);
    }
    drop(storage);
    let mut storage = PostgresThreeLayerStorage::connect(&database_url, 4)
        .await
        .map_err(|_| TrialGateError::Storage)?;
    let retrieved_ciphertext = retrieve_verified(
        &storage,
        &identity,
        1,
        ciphertext_readiness
            .locator(StorageLayer::Operational)
            .ok_or(TrialGateError::Storage)?,
        &material.ciphertext_identity,
    )
    .await
    .map_err(|_| TrialGateError::Storage)?;
    let retrieved_a_envelope = retrieve_verified(
        &storage,
        &identity,
        1,
        a_readiness
            .locator(StorageLayer::Operational)
            .ok_or(TrialGateError::Storage)?,
        &a_envelope.envelope_identity,
    )
    .await
    .map_err(|_| TrialGateError::Storage)?;
    let retrieved_b_envelope = retrieve_verified(
        &storage,
        &identity,
        1,
        b_readiness
            .locator(StorageLayer::Operational)
            .ok_or(TrialGateError::Storage)?,
        &b_envelope.envelope_identity,
    )
    .await
    .map_err(|_| TrialGateError::Storage)?;
    let mut retrieved_material = material.clone();
    retrieved_material.ciphertext = retrieved_ciphertext;
    for envelope in &mut retrieved_material.envelopes {
        if envelope.recipient == a_binding {
            envelope.envelope_bytes = retrieved_a_envelope.clone();
        } else if envelope.recipient == b_binding {
            envelope.envelope_bytes = retrieved_b_envelope.clone();
        }
    }
    let opened = cryptography
        .open(
            &profile,
            &retrieved_material.context,
            &retrieved_material,
            &b_binding,
            &identity,
        )
        .map_err(|_| TrialGateError::Cryptography)?;
    if opened != plaintext.as_slice() {
        return Err(TrialGateError::Cryptography);
    }

    journal.record(
        "storage-replacement-envelope",
        "write-before-effect",
        None,
        None,
    )?;
    let replacement_readiness = persist(&mut storage, &replacement_envelope.envelope_bytes).await?;
    readiness.push(replacement_readiness.clone());
    journal.record(
        "storage-replacement-envelope",
        "three-layer-verified",
        None,
        Some(replacement_envelope.envelope_identity.digest.as_bytes()),
    )?;
    let op_request_bad = commitment(b"request-outsider-v1");
    let (request, _) = Pubkey::find_program_address(
        &[
            REISSUE_SEED,
            &artifact_id,
            recipient.pubkey().as_ref(),
            &1_u64.to_le_bytes(),
        ],
        &program_id,
    );
    let (request_bad_replay, _) =
        Pubkey::find_program_address(&[REPLAY_SEED, &artifact_id, &op_request_bad], &program_id);
    let request_bad = protocol_instruction(
        program_id,
        ProtocolInstruction::RequestReissue {
            replacement_key_commitment: *b2_binding.key_binding_id.as_bytes(),
            expected_revision: 1,
            operation_id: op_request_bad,
        },
        vec![
            AccountMeta::new(payer.pubkey(), true),
            AccountMeta::new_readonly(outsider.pubkey(), true),
            AccountMeta::new(artifact, false),
            AccountMeta::new(request, false),
            AccountMeta::new(request_bad_replay, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
    )?;
    cases.push(submit_rejection(
        &rpc,
        &journal,
        &mut budget,
        "reissue-request-outsider",
        signed_transaction(&rpc, request_bad, &payer, &[&outsider])?,
    )?);
    if finalized_artifact(&rpc, program_id, artifact)? != grant_state {
        return Err(TrialGateError::Solana);
    }

    let op_request = commitment(b"request-positive-v1");
    let (request_replay, _) =
        Pubkey::find_program_address(&[REPLAY_SEED, &artifact_id, &op_request], &program_id);
    let request_positive = protocol_instruction(
        program_id,
        ProtocolInstruction::RequestReissue {
            replacement_key_commitment: *b2_binding.key_binding_id.as_bytes(),
            expected_revision: 1,
            operation_id: op_request,
        },
        vec![
            AccountMeta::new(payer.pubkey(), true),
            AccountMeta::new_readonly(recipient.pubkey(), true),
            AccountMeta::new(artifact, false),
            AccountMeta::new(request, false),
            AccountMeta::new(request_replay, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
    )?;
    cases.push(submit_success(
        &rpc,
        &journal,
        &mut budget,
        "reissue-request-positive",
        signed_transaction(&rpc, request_positive.clone(), &payer, &[&recipient])?,
    )?);
    if finalized_artifact(&rpc, program_id, artifact)? != grant_state {
        return Err(TrialGateError::Solana);
    }
    cases.push(submit_rejection(
        &rpc,
        &journal,
        &mut budget,
        "reissue-request-replay",
        signed_transaction(&rpc, request_positive, &payer, &[&recipient])?,
    )?);
    if finalized_artifact(&rpc, program_id, artifact)? != grant_state {
        return Err(TrialGateError::Solana);
    }

    let op_self = commitment(b"fulfill-self-v1");
    let (self_replay, _) =
        Pubkey::find_program_address(&[REPLAY_SEED, &artifact_id, &op_self], &program_id);
    let fulfill_self = protocol_instruction(
        program_id,
        ProtocolInstruction::FulfillReissue {
            replacement_envelope_commitment: *replacement_envelope
                .envelope_identity
                .digest
                .as_bytes(),
            expected_revision: 1,
            operation_id: op_self,
        },
        vec![
            AccountMeta::new(payer.pubkey(), true),
            AccountMeta::new_readonly(recipient.pubkey(), true),
            AccountMeta::new(artifact, false),
            AccountMeta::new(request, false),
            AccountMeta::new(self_replay, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
    )?;
    cases.push(submit_rejection(
        &rpc,
        &journal,
        &mut budget,
        "reissue-self-fulfillment",
        signed_transaction(&rpc, fulfill_self, &payer, &[&recipient])?,
    )?);
    if finalized_artifact(&rpc, program_id, artifact)? != grant_state {
        return Err(TrialGateError::Solana);
    }

    let op_fulfill = commitment(b"fulfill-positive-v1");
    let (fulfill_replay, _) =
        Pubkey::find_program_address(&[REPLAY_SEED, &artifact_id, &op_fulfill], &program_id);
    let fulfill = protocol_instruction(
        program_id,
        ProtocolInstruction::FulfillReissue {
            replacement_envelope_commitment: *replacement_envelope
                .envelope_identity
                .digest
                .as_bytes(),
            expected_revision: 1,
            operation_id: op_fulfill,
        },
        vec![
            AccountMeta::new(payer.pubkey(), true),
            AccountMeta::new_readonly(originator.pubkey(), true),
            AccountMeta::new(artifact, false),
            AccountMeta::new(request, false),
            AccountMeta::new(fulfill_replay, false),
            AccountMeta::new_readonly(system_program::id(), false),
        ],
    )?;
    cases.push(submit_success(
        &rpc,
        &journal,
        &mut budget,
        "reissue-fulfill-positive",
        signed_transaction(&rpc, fulfill, &payer, &[&originator])?,
    )?);
    let reissue_state = finalized_artifact(&rpc, program_id, artifact)?;
    let mut expected_reissue_state = grant_state.clone();
    expected_reissue_state.recipient_key_commitment = *b2_binding.key_binding_id.as_bytes();
    expected_reissue_state.recipient_envelope_commitment =
        *replacement_envelope.envelope_identity.digest.as_bytes();
    expected_reissue_state.recipient_key_envelope_binding = key_envelope_binding(
        b2_binding.key_binding_id.as_bytes(),
        replacement_envelope.envelope_identity.digest.as_bytes(),
    );
    expected_reissue_state.revision = 2;
    if reissue_state != expected_reissue_state {
        return Err(TrialGateError::Solana);
    }
    let request_account = rpc
        .get_account_with_commitment(&request, CommitmentConfig::finalized())
        .map_err(|_| TrialGateError::Solana)?
        .value
        .ok_or(TrialGateError::Solana)?;
    let request_state = ReissueRequest::try_from_slice(&request_account.data)
        .map_err(|_| TrialGateError::Solana)?;
    if !request_state.fulfilled {
        return Err(TrialGateError::Solana);
    }
    drop(storage);
    let storage = PostgresThreeLayerStorage::connect(&database_url, 4)
        .await
        .map_err(|_| TrialGateError::Storage)?;
    let retrieved_ciphertext = retrieve_verified(
        &storage,
        &identity,
        1,
        ciphertext_readiness
            .locator(StorageLayer::Operational)
            .ok_or(TrialGateError::Storage)?,
        &material.ciphertext_identity,
    )
    .await
    .map_err(|_| TrialGateError::Storage)?;
    let retrieved_replacement = retrieve_verified(
        &storage,
        &identity,
        1,
        replacement_readiness
            .locator(StorageLayer::Operational)
            .ok_or(TrialGateError::Storage)?,
        &replacement_envelope.envelope_identity,
    )
    .await
    .map_err(|_| TrialGateError::Storage)?;
    let mut replacement_material = material.clone();
    replacement_material.ciphertext = retrieved_ciphertext;
    replacement_material
        .envelopes
        .retain(|item| item.recipient.recipient_id != b_binding.recipient_id);
    let mut retrieved_replacement_envelope = replacement_envelope;
    retrieved_replacement_envelope.envelope_bytes = retrieved_replacement;
    replacement_material
        .envelopes
        .push(retrieved_replacement_envelope);
    let replacement_opened = cryptography
        .open(
            &profile,
            &replacement_material.context,
            &replacement_material,
            &b2_binding,
            &identity,
        )
        .map_err(|_| TrialGateError::Cryptography)?;
    if replacement_opened != plaintext.as_slice() {
        return Err(TrialGateError::Cryptography);
    }
    let ending_balance = rpc
        .get_balance(&payer.pubkey())
        .map_err(|_| TrialGateError::Solana)?;
    let fee_total = cases.iter().map(|item| item.fee_lamports).sum();
    let deployment_fee_total = deployment.cases.iter().map(|item| item.fee_lamports).sum();
    let final_locator_commitment = locator_commitment(&readiness);
    let grant_state_bytes = borsh::to_vec(&grant_state).map_err(|_| TrialGateError::Solana)?;
    let reissue_state_bytes = borsh::to_vec(&reissue_state).map_err(|_| TrialGateError::Solana)?;
    let observations = vec![
        ObservationEvidence {
            case_id: "storage-three-layer-ready",
            expected: "four encrypted objects ready in all three layers",
            observed: "verified-after-two-provider-restarts",
            input_sha256: hex_lower(material.ciphertext_identity.digest.as_bytes()),
            output_sha256: hex_lower(&final_locator_commitment),
        },
        ObservationEvidence {
            case_id: "grant-finalized-fetch",
            expected: "A preserved and B added at finalized revision one",
            observed: "finalized-state-exact",
            input_sha256: hex_lower(&Sha256::digest(initialized_state.artifact_id)),
            output_sha256: hex_lower(&Sha256::digest(&grant_state_bytes)),
        },
        ObservationEvidence {
            case_id: "recipient-decryption",
            expected: "B opens restart-retrieved ciphertext and envelope",
            observed: "exact-fixture-match",
            input_sha256: hex_lower(material.ciphertext_identity.digest.as_bytes()),
            output_sha256: hex_lower(material.context.plaintext_commitment.as_bytes()),
        },
        ObservationEvidence {
            case_id: "reissue-state-isolation",
            expected: "only B key-envelope binding and permitted revision/request state change",
            observed: "exact-structural-equality-except-permitted-fields",
            input_sha256: hex_lower(&Sha256::digest(&grant_state_bytes)),
            output_sha256: hex_lower(&Sha256::digest(&reissue_state_bytes)),
        },
        ObservationEvidence {
            case_id: "replacement-recipient-decryption",
            expected: "B2 opens restart-retrieved ciphertext and replacement envelope",
            observed: "exact-fixture-match",
            input_sha256: hex_lower(
                replacement_material
                    .envelopes
                    .last()
                    .ok_or(TrialGateError::Cryptography)?
                    .envelope_identity
                    .digest
                    .as_bytes(),
            ),
            output_sha256: hex_lower(material.context.plaintext_commitment.as_bytes()),
        },
        ObservationEvidence {
            case_id: "cost-observation",
            expected: "infrastructure costs recorded separately from zero consideration",
            observed: "fees-rent-and-local-storage-class-separated",
            input_sha256: hex_lower(&Sha256::digest(
                [
                    fee_total,
                    deployment_fee_total,
                    funded_balance,
                    ending_balance,
                ]
                .into_iter()
                .flat_map(u64::to_be_bytes)
                .collect::<Vec<_>>(),
            )),
            output_sha256: hex_lower(&Sha256::digest(0_u64.to_be_bytes())),
        },
    ];
    let observed_case_ids: BTreeSet<&str> = cases
        .iter()
        .map(|item| item.case_id.as_str())
        .chain(observations.iter().map(|item| item.case_id))
        .collect();
    let required_case_ids: BTreeSet<&str> = envelope
        .enumerated_case_ids
        .iter()
        .map(String::as_str)
        .collect();
    if observed_case_ids != required_case_ids {
        return Err(TrialGateError::ExternalMaterial);
    }
    journal.record("trial", "complete-before-evidence-write", None, None)?;
    Ok(TrialEvidence {
        schema_version: "cav2-kep-devnet-trial-evidence/v1-candidate",
        result: "PASS_BOUNDED_DEVNET",
        cluster: "solana-devnet",
        genesis_hash: genesis.to_string(),
        program_id: program_id.to_string(),
        sbf_sha256: envelope.sbf_sha256.clone(),
        funding,
        deployment: DeploymentEvidence {
            signed_submissions: u16::try_from(deployment.cases.len())
                .map_err(|_| TrialGateError::DeploymentBudgetImpossible)?,
            transactions: deployment.cases,
            programdata_address: deployment.programdata_address.to_string(),
            program_rent_lamports: deployment.program_rent_lamports,
            programdata_rent_lamports: deployment.programdata_rent_lamports,
            remote_sbf_sha256: deployment.remote_sbf_sha256,
            upgrade_authority: deployment.upgrade_authority.to_string(),
        },
        storage: StorageEvidence {
            provider: "postgresql-v1",
            encrypted_object_count: readiness.len() as u16,
            every_object_ready_in_three_layers: readiness.iter().all(StorageReadiness::is_ready),
            locator_commitment_sha256: hex::encode(final_locator_commitment),
        },
        cases,
        observations,
        finalized_grant_revision: grant_state.revision,
        finalized_reissue_revision: reissue_state.revision,
        recipient_decryption: "exact-fixture-match",
        replacement_recipient_decryption: "exact-fixture-match",
        protocol_transaction_fee_lamports: fee_total,
        deployment_transaction_fee_lamports: deployment_fee_total,
        payer_balance_delta_lamports: funded_balance.saturating_sub(ending_balance),
        retained_program_rent_lamports: deployment
            .program_rent_lamports
            .saturating_add(deployment.programdata_rent_lamports),
        storage_cost_observation: "local-postgresql-no-billed-knowledge-consideration",
        knowledge_consideration_lamports: 0,
        protocol_signed_submissions: budget.used,
        authority_effect: "none",
        observed_external_effect: "bounded-public-devnet-effects-executed",
        authorization_attestation: "external-not-attested-by-runner",
        claim_ceiling: "Exact operator-invoked public Devnet v1 trial executed after an external authorization decision that the runner does not authenticate or attest; no Mainnet, production security, availability, publication, or release claim.",
    })
}

pub(crate) fn write_evidence(
    envelope: &DevnetEnvelope,
    evidence: &TrialEvidence,
) -> Result<(), TrialGateError> {
    let raw = serde_json::to_vec_pretty(evidence).map_err(|_| TrialGateError::EvidenceWrite)?;
    let inputs = &envelope.external_inputs;
    let plaintext = Zeroizing::new(
        fs::read(&inputs.plaintext_fixture_path).map_err(|_| TrialGateError::ExternalMaterial)?,
    );
    let private_paths = [
        &inputs.originator_hpke_private_path,
        &inputs.recipient_hpke_private_path,
        &inputs.replacement_hpke_private_path,
        &inputs.payer_keypair_path,
        &inputs.originator_keypair_path,
        &inputs.recipient_keypair_path,
        &inputs.outsider_keypair_path,
        &inputs.program_keypair_path,
        &inputs.buffer_keypair_path,
        &inputs.upgrade_authority_keypair_path,
    ];
    if !plaintext.is_empty()
        && raw
            .windows(plaintext.len())
            .any(|window| window == plaintext.as_slice())
    {
        return Err(TrialGateError::EvidenceLeak);
    }
    for path in private_paths {
        let secret = Zeroizing::new(fs::read(path).map_err(|_| TrialGateError::ExternalMaterial)?);
        if !secret.is_empty()
            && raw
                .windows(secret.len())
                .any(|window| window == secret.as_slice())
        {
            return Err(TrialGateError::EvidenceLeak);
        }
    }
    fs::write(&inputs.evidence_output_path, [raw, b"\n".to_vec()].concat())
        .map_err(|_| TrialGateError::EvidenceWrite)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sanitized_rpc_failure_classifies_rate_limit_without_retaining_raw_detail() {
        let raw = "HTTP status 429 Too Many Requests: secret-provider-message";
        let failure = SanitizedRpcFailure::from_error("funding", &raw);
        assert_eq!("funding", failure.stage);
        assert_eq!("rate-limited-rejection", failure.class);
        assert_eq!(64, failure.detail_sha256.len());
        assert!(!failure.detail_sha256.contains("secret-provider-message"));
    }

    #[test]
    fn sanitized_rpc_failure_distinguishes_transport_ambiguity() {
        let failure =
            SanitizedRpcFailure::from_error("balance", &"connection timed out before response");
        assert_eq!("transport-ambiguous", failure.class);
    }

    #[test]
    fn actual_transport_ambiguity_record_remains_pending() {
        let raw = r#"{"stage":"prefunded-balance-query-failed","signature":null,"failure_stage":"execution-prefunded-balance","failure_class":"transport-ambiguous"}"#;
        let analysis = analyze_attempt_journal(raw).expect("journal parses");
        assert_eq!(0, analysis.signatures.len());
        assert_eq!(1, analysis.unsigned_ambiguous_effects);
        assert_eq!(0, analysis.proven_pre_effect_stops);
        assert_eq!(
            "PENDING",
            reconciliation_result(
                analysis.signatures.len(),
                0,
                analysis.unsigned_ambiguous_effects,
                analysis.proven_pre_effect_stops,
            )
        );
    }

    #[test]
    fn unclassified_unsigned_failure_remains_pending() {
        let raw = r#"{"stage":"genesis-hash-query-failed","signature":null,"failure_stage":"execution-genesis-hash","failure_class":"unclassified-rpc-or-transport"}"#;
        let analysis = analyze_attempt_journal(raw).expect("journal parses");
        assert_eq!(1, analysis.unsigned_ambiguous_effects);
        assert_eq!(
            "PENDING",
            reconciliation_result(0, 0, analysis.unsigned_ambiguous_effects, 0)
        );
    }

    #[test]
    fn known_genesis_rejection_is_a_proven_pre_effect_stop() {
        let raw = r#"{"stage":"genesis-hash-query-failed","signature":null,"failure_stage":"execution-genesis-hash","failure_class":"rpc-rejection"}"#;
        let analysis = analyze_attempt_journal(raw).expect("journal parses");
        assert_eq!(0, analysis.unsigned_ambiguous_effects);
        assert_eq!(1, analysis.proven_pre_effect_stops);
        assert_eq!(
            "PROVEN_PRE_EFFECT_STOP",
            reconciliation_result(0, 0, 0, analysis.proven_pre_effect_stops)
        );
    }

    #[test]
    fn known_balance_bound_rejection_is_a_proven_pre_effect_stop() {
        let raw = r#"{"stage":"prefunded-balance-insufficient","signature":null,"failure_stage":null,"failure_class":null}"#;
        let analysis = analyze_attempt_journal(raw).expect("journal parses");
        assert_eq!(1, analysis.proven_pre_effect_stops);
        assert_eq!(
            "PROVEN_PRE_EFFECT_STOP",
            reconciliation_result(0, 0, 0, analysis.proven_pre_effect_stops)
        );
    }

    #[test]
    fn zero_signatures_without_terminal_evidence_remains_pending() {
        let raw = r#"{"stage":"operator-invoked-execution-start","signature":null,"failure_stage":null,"failure_class":null}"#;
        let analysis = analyze_attempt_journal(raw).expect("journal parses");
        assert_eq!(JournalAnalysis::default(), analysis);
        assert_eq!("PENDING", reconciliation_result(0, 0, 0, 0));
    }

    #[test]
    fn signed_attempt_requires_a_final_status_before_reconciliation() {
        let raw = r#"{"stage":"signed-before-submit","signature":"1111111111111111111111111111111111111111111111111111111111111111","failure_stage":null,"failure_class":null}"#;
        let analysis = analyze_attempt_journal(raw).expect("journal parses");
        assert_eq!(1, analysis.signatures.len());
        assert_eq!(
            "PENDING",
            reconciliation_result(analysis.signatures.len(), 1, 0, 0)
        );
        assert_eq!(
            "RECONCILED",
            reconciliation_result(analysis.signatures.len(), 0, 0, 0)
        );
    }

    #[test]
    fn prefunded_balance_must_be_inside_both_bounds() {
        assert!(validate_prefunded_balance(2_000_000_000, 2_000_000_000, 10_000_000_000).is_ok());
        assert!(matches!(
            validate_prefunded_balance(0, 2_000_000_000, 10_000_000_000),
            Err(TrialGateError::FundingPrerequisite { .. })
        ));
        assert!(matches!(
            validate_prefunded_balance(10_000_000_001, 2_000_000_000, 10_000_000_000),
            Err(TrialGateError::FundingPrerequisite { .. })
        ));
    }
}
