//! Deterministic protocol-state kernel for the first encrypted co-ownership proof.
//!
//! This crate deliberately performs no cryptography, storage, Solana calls, payment,
//! publication, or deployment. Ciphertexts, keys, signatures, and challenges enter as
//! opaque commitments. A caller-owned `AuthorizationVerifier` must verify signatures.

use std::collections::{BTreeMap, BTreeSet};

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
pub struct Digest32([u8; 32]);

impl Digest32 {
    pub fn try_new(bytes: [u8; 32]) -> Result<Self, ProtocolError> {
        if bytes == [0; 32] {
            Err(ProtocolError::ZeroDigest)
        } else {
            Ok(Self(bytes))
        }
    }

    pub fn as_bytes(&self) -> &[u8; 32] {
        &self.0
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct EncryptionKeyBinding {
    pub fingerprint: Digest32,
    pub version: u64,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct KnowledgeIdentity {
    pub identity_id: Digest32,
    pub authorization_key_fingerprint: Digest32,
    pub encryption_key: EncryptionKeyBinding,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ArtifactVersion {
    pub artifact_id: Digest32,
    pub version_id: Digest32,
    pub plaintext_commitment: Digest32,
    pub policy_id: Digest32,
    pub originator_id: Digest32,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum AuthorityRule {
    OriginatorOnly,
    AnyCurrentCoowner,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct PropagationPolicy {
    pub policy_id: Digest32,
    pub originator_id: Digest32,
    pub grant_authority: AuthorityRule,
    pub reissue_authority: AuthorityRule,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct RecipientKeyEnvelope {
    pub envelope_digest: Digest32,
    pub artifact_version_id: Digest32,
    pub encryption_epoch: u64,
    pub recipient_id: Digest32,
    pub recipient_key_fingerprint: Digest32,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct DecryptionAcknowledgement {
    pub command_digest: Digest32,
    pub artifact_version_id: Digest32,
    pub encryption_epoch: u64,
    pub recipient_id: Digest32,
    pub envelope_digest: Digest32,
    pub challenge_digest: Digest32,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct CoownershipGrant {
    pub command_digest: Digest32,
    pub artifact_version_id: Digest32,
    pub policy_id: Digest32,
    pub grantor_id: Digest32,
    pub recipient_id: Digest32,
    pub recipient_key_fingerprint: Digest32,
    pub envelope_digest: Digest32,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ReissueReason {
    Lost,
    Compromised,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct KeyReissueRequest {
    pub command_digest: Digest32,
    pub artifact_version_id: Digest32,
    pub recipient_id: Digest32,
    pub previous_key_fingerprint: Digest32,
    pub replacement_key_fingerprint: Digest32,
    pub reason: ReissueReason,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct ReissueAuthorization {
    pub artifact_version_id: Digest32,
    pub recipient_id: Digest32,
    pub previous_key_fingerprint: Digest32,
    pub replacement_key_fingerprint: Digest32,
    pub encryption_epoch: u64,
    pub owner_count: usize,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct EpochRotation {
    pub command_digest: Digest32,
    pub artifact_version_id: Digest32,
    pub actor_id: Digest32,
    pub prior_epoch: u64,
    pub successor_epoch: u64,
    pub ciphertext_digest: Digest32,
    pub external_location_digest: Digest32,
    pub envelopes: Vec<RecipientKeyEnvelope>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AuthorizationProof {
    pub signer_id: Digest32,
    pub command_digest: Digest32,
    pub signature: Vec<u8>,
}

pub trait AuthorizationVerifier {
    fn verify(&self, proof: &AuthorizationProof) -> bool;
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct EncryptedCoownershipState {
    artifact: ArtifactVersion,
    owners: BTreeSet<Digest32>,
    encryption_epoch: u64,
    ciphertext_digest: Digest32,
    external_location_digest: Digest32,
    envelopes: BTreeMap<Digest32, RecipientKeyEnvelope>,
    acknowledgements: BTreeMap<Digest32, DecryptionAcknowledgement>,
}

impl EncryptedCoownershipState {
    pub fn new(
        artifact: ArtifactVersion,
        policy: &PropagationPolicy,
        originator: &KnowledgeIdentity,
        encryption_epoch: u64,
        ciphertext_digest: Digest32,
        external_location_digest: Digest32,
        originator_envelope: RecipientKeyEnvelope,
    ) -> Result<Self, ProtocolError> {
        if encryption_epoch == 0 {
            return Err(ProtocolError::InvalidEpoch);
        }
        validate_policy(&artifact, policy)?;
        if originator.identity_id != artifact.originator_id {
            return Err(ProtocolError::IdentityMismatch);
        }
        validate_envelope(
            &originator_envelope,
            artifact.version_id,
            encryption_epoch,
            originator.identity_id,
            originator.encryption_key.fingerprint,
        )?;
        let owners = BTreeSet::from([originator.identity_id]);
        let envelopes = BTreeMap::from([(originator.identity_id, originator_envelope)]);
        Ok(Self {
            artifact,
            owners,
            encryption_epoch,
            ciphertext_digest,
            external_location_digest,
            envelopes,
            acknowledgements: BTreeMap::new(),
        })
    }

    pub fn artifact(&self) -> &ArtifactVersion {
        &self.artifact
    }

    pub fn owners(&self) -> &BTreeSet<Digest32> {
        &self.owners
    }

    pub fn encryption_epoch(&self) -> u64 {
        self.encryption_epoch
    }

    pub fn ciphertext_digest(&self) -> Digest32 {
        self.ciphertext_digest
    }

    pub fn external_location_digest(&self) -> Digest32 {
        self.external_location_digest
    }

    pub fn envelope_for(&self, recipient: Digest32) -> Option<&RecipientKeyEnvelope> {
        self.envelopes.get(&recipient)
    }

    pub fn acknowledgement_for(&self, recipient: Digest32) -> Option<&DecryptionAcknowledgement> {
        self.acknowledgements.get(&recipient)
    }

    pub fn grant_coownership(
        &self,
        policy: &PropagationPolicy,
        recipient: &KnowledgeIdentity,
        grant: &CoownershipGrant,
        envelope: RecipientKeyEnvelope,
        proof: &AuthorizationProof,
        verifier: &impl AuthorizationVerifier,
    ) -> Result<Self, ProtocolError> {
        validate_policy(&self.artifact, policy)?;
        if grant.artifact_version_id != self.artifact.version_id {
            return Err(ProtocolError::ArtifactVersionMismatch);
        }
        if grant.policy_id != policy.policy_id {
            return Err(ProtocolError::PolicyMismatch);
        }
        if !self.owners.contains(&grant.grantor_id) {
            return Err(ProtocolError::GrantorNotOwner);
        }
        if !authorized(
            policy.grant_authority,
            policy.originator_id,
            grant.grantor_id,
        ) {
            return Err(ProtocolError::GrantorNotAuthorized);
        }
        if recipient.identity_id != grant.recipient_id {
            return Err(ProtocolError::IdentityMismatch);
        }
        if self.owners.contains(&grant.recipient_id) {
            return Err(ProtocolError::RecipientAlreadyOwner);
        }
        if recipient.encryption_key.fingerprint != grant.recipient_key_fingerprint {
            return Err(ProtocolError::RecipientKeyMismatch);
        }
        if envelope.envelope_digest != grant.envelope_digest {
            return Err(ProtocolError::EnvelopeMismatch);
        }
        validate_envelope(
            &envelope,
            self.artifact.version_id,
            self.encryption_epoch,
            grant.recipient_id,
            grant.recipient_key_fingerprint,
        )?;
        require_authorization(proof, grant.grantor_id, grant.command_digest, verifier)?;

        let prior_owners = self.owners.clone();
        let mut successor = self.clone();
        successor.owners.insert(grant.recipient_id);
        successor.envelopes.insert(grant.recipient_id, envelope);
        if !prior_owners.is_subset(&successor.owners)
            || !successor.owners.contains(&self.artifact.originator_id)
        {
            return Err(ProtocolError::ExistingOwnerRemoved);
        }
        Ok(successor)
    }

    pub fn acknowledge_decryption(
        &self,
        acknowledgement: DecryptionAcknowledgement,
        proof: &AuthorizationProof,
        verifier: &impl AuthorizationVerifier,
    ) -> Result<Self, ProtocolError> {
        if acknowledgement.artifact_version_id != self.artifact.version_id {
            return Err(ProtocolError::ArtifactVersionMismatch);
        }
        if acknowledgement.encryption_epoch != self.encryption_epoch {
            return Err(ProtocolError::EnvelopeEpochMismatch);
        }
        if !self.owners.contains(&acknowledgement.recipient_id) {
            return Err(ProtocolError::RecipientNotOwner);
        }
        let envelope = self
            .envelopes
            .get(&acknowledgement.recipient_id)
            .ok_or(ProtocolError::EnvelopeMissing)?;
        if envelope.envelope_digest != acknowledgement.envelope_digest {
            return Err(ProtocolError::EnvelopeMismatch);
        }
        if self
            .acknowledgements
            .contains_key(&acknowledgement.recipient_id)
        {
            return Err(ProtocolError::AcknowledgementAlreadyRecorded);
        }
        require_authorization(
            proof,
            acknowledgement.recipient_id,
            acknowledgement.command_digest,
            verifier,
        )?;
        let mut successor = self.clone();
        successor
            .acknowledgements
            .insert(acknowledgement.recipient_id, acknowledgement);
        Ok(successor)
    }

    pub fn authorize_key_reissue(
        &self,
        recipient: &KnowledgeIdentity,
        request: &KeyReissueRequest,
        proof: &AuthorizationProof,
        verifier: &impl AuthorizationVerifier,
    ) -> Result<ReissueAuthorization, ProtocolError> {
        if request.artifact_version_id != self.artifact.version_id {
            return Err(ProtocolError::ArtifactVersionMismatch);
        }
        if request.recipient_id != recipient.identity_id {
            return Err(ProtocolError::IdentityMismatch);
        }
        if !self.owners.contains(&request.recipient_id) {
            return Err(ProtocolError::RecipientNotOwner);
        }
        if recipient.encryption_key.fingerprint != request.previous_key_fingerprint {
            return Err(ProtocolError::ReissueKeyMismatch);
        }
        if request.previous_key_fingerprint == request.replacement_key_fingerprint {
            return Err(ProtocolError::ReplacementKeyUnchanged);
        }
        require_authorization(
            proof,
            request.recipient_id,
            request.command_digest,
            verifier,
        )?;
        if request.reason == ReissueReason::Compromised {
            return Err(ProtocolError::RequiresNewEncryptionEpoch);
        }
        Ok(ReissueAuthorization {
            artifact_version_id: self.artifact.version_id,
            recipient_id: request.recipient_id,
            previous_key_fingerprint: request.previous_key_fingerprint,
            replacement_key_fingerprint: request.replacement_key_fingerprint,
            encryption_epoch: self.encryption_epoch,
            owner_count: self.owners.len(),
        })
    }

    pub fn rotate_compromised_epoch(
        &self,
        policy: &PropagationPolicy,
        identities: &BTreeMap<Digest32, KnowledgeIdentity>,
        rotation: &EpochRotation,
        proof: &AuthorizationProof,
        verifier: &impl AuthorizationVerifier,
    ) -> Result<Self, ProtocolError> {
        validate_policy(&self.artifact, policy)?;
        if rotation.artifact_version_id != self.artifact.version_id {
            return Err(ProtocolError::ArtifactVersionMismatch);
        }
        if !self.owners.contains(&rotation.actor_id) {
            return Err(ProtocolError::GrantorNotOwner);
        }
        if !authorized(
            policy.reissue_authority,
            policy.originator_id,
            rotation.actor_id,
        ) {
            return Err(ProtocolError::GrantorNotAuthorized);
        }
        if rotation.prior_epoch != self.encryption_epoch
            || rotation.successor_epoch != self.encryption_epoch + 1
        {
            return Err(ProtocolError::EpochMustAdvance);
        }
        require_authorization(proof, rotation.actor_id, rotation.command_digest, verifier)?;

        let mut successor_envelopes = BTreeMap::new();
        for envelope in &rotation.envelopes {
            if successor_envelopes.contains_key(&envelope.recipient_id) {
                return Err(ProtocolError::DuplicateEnvelopeRecipient);
            }
            let identity = identities
                .get(&envelope.recipient_id)
                .ok_or(ProtocolError::IdentityMissing)?;
            validate_envelope(
                envelope,
                self.artifact.version_id,
                rotation.successor_epoch,
                identity.identity_id,
                identity.encryption_key.fingerprint,
            )?;
            successor_envelopes.insert(envelope.recipient_id, *envelope);
        }
        let covered: BTreeSet<_> = successor_envelopes.keys().copied().collect();
        if covered != self.owners {
            return Err(ProtocolError::IncompleteOwnerEnvelopeCoverage);
        }

        let mut successor = self.clone();
        successor.encryption_epoch = rotation.successor_epoch;
        successor.ciphertext_digest = rotation.ciphertext_digest;
        successor.external_location_digest = rotation.external_location_digest;
        successor.envelopes = successor_envelopes;
        successor.acknowledgements.clear();
        Ok(successor)
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ProtocolError {
    ZeroDigest,
    InvalidEpoch,
    ArtifactVersionMismatch,
    PolicyMismatch,
    IdentityMismatch,
    AuthorizationFailed,
    CommandDigestMismatch,
    GrantorNotOwner,
    GrantorNotAuthorized,
    RecipientAlreadyOwner,
    RecipientKeyMismatch,
    ExistingOwnerRemoved,
    EnvelopeMissing,
    EnvelopeMismatch,
    EnvelopeEpochMismatch,
    RecipientNotOwner,
    AcknowledgementAlreadyRecorded,
    ReissueKeyMismatch,
    ReplacementKeyUnchanged,
    RequiresNewEncryptionEpoch,
    EpochMustAdvance,
    DuplicateEnvelopeRecipient,
    IdentityMissing,
    IncompleteOwnerEnvelopeCoverage,
}

fn validate_policy(
    artifact: &ArtifactVersion,
    policy: &PropagationPolicy,
) -> Result<(), ProtocolError> {
    if artifact.policy_id != policy.policy_id {
        return Err(ProtocolError::PolicyMismatch);
    }
    if artifact.originator_id != policy.originator_id {
        return Err(ProtocolError::IdentityMismatch);
    }
    Ok(())
}

fn validate_envelope(
    envelope: &RecipientKeyEnvelope,
    artifact_version_id: Digest32,
    encryption_epoch: u64,
    recipient_id: Digest32,
    recipient_key_fingerprint: Digest32,
) -> Result<(), ProtocolError> {
    if envelope.artifact_version_id != artifact_version_id {
        return Err(ProtocolError::ArtifactVersionMismatch);
    }
    if envelope.encryption_epoch != encryption_epoch || encryption_epoch == 0 {
        return Err(ProtocolError::EnvelopeEpochMismatch);
    }
    if envelope.recipient_id != recipient_id {
        return Err(ProtocolError::IdentityMismatch);
    }
    if envelope.recipient_key_fingerprint != recipient_key_fingerprint {
        return Err(ProtocolError::RecipientKeyMismatch);
    }
    Ok(())
}

fn authorized(rule: AuthorityRule, originator: Digest32, actor: Digest32) -> bool {
    match rule {
        AuthorityRule::OriginatorOnly => actor == originator,
        AuthorityRule::AnyCurrentCoowner => true,
    }
}

fn require_authorization(
    proof: &AuthorizationProof,
    expected_signer: Digest32,
    expected_command: Digest32,
    verifier: &impl AuthorizationVerifier,
) -> Result<(), ProtocolError> {
    if proof.signer_id != expected_signer {
        return Err(ProtocolError::AuthorizationFailed);
    }
    if proof.command_digest != expected_command {
        return Err(ProtocolError::CommandDigestMismatch);
    }
    if !verifier.verify(proof) {
        return Err(ProtocolError::AuthorizationFailed);
    }
    Ok(())
}
