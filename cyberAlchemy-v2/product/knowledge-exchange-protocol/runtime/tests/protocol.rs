use std::collections::BTreeMap;

use cyberalchemy_knowledge_exchange_protocol::{
    ArtifactVersion, AuthorityRule, AuthorizationProof, AuthorizationVerifier, CoownershipGrant,
    DecryptionAcknowledgement, Digest32, EncryptedCoownershipState, EncryptionKeyBinding,
    EpochRotation, KeyReissueRequest, KnowledgeIdentity, PropagationPolicy, ProtocolError,
    RecipientKeyEnvelope, ReissueReason,
};

struct TestVerifier;

impl AuthorizationVerifier for TestVerifier {
    fn verify(&self, proof: &AuthorizationProof) -> bool {
        proof.signature == b"verified"
    }
}

fn d(byte: u8) -> Digest32 {
    Digest32::try_new([byte; 32]).unwrap()
}

fn identity(id: u8, auth: u8, encryption: u8, version: u64) -> KnowledgeIdentity {
    KnowledgeIdentity {
        identity_id: d(id),
        authorization_key_fingerprint: d(auth),
        encryption_key: EncryptionKeyBinding {
            fingerprint: d(encryption),
            version,
        },
    }
}

fn envelope(recipient: &KnowledgeIdentity, epoch: u64, digest: u8) -> RecipientKeyEnvelope {
    RecipientKeyEnvelope {
        envelope_digest: d(digest),
        artifact_version_id: d(11),
        encryption_epoch: epoch,
        recipient_id: recipient.identity_id,
        recipient_key_fingerprint: recipient.encryption_key.fingerprint,
    }
}

fn proof(signer: Digest32, command: u8) -> AuthorizationProof {
    AuthorizationProof {
        signer_id: signer,
        command_digest: d(command),
        signature: b"verified".to_vec(),
    }
}

fn fixture() -> (
    EncryptedCoownershipState,
    PropagationPolicy,
    KnowledgeIdentity,
    KnowledgeIdentity,
) {
    let a = identity(1, 2, 3, 1);
    let b = identity(4, 5, 6, 1);
    let artifact = ArtifactVersion {
        artifact_id: d(10),
        version_id: d(11),
        plaintext_commitment: d(12),
        policy_id: d(13),
        originator_id: a.identity_id,
    };
    let policy = PropagationPolicy {
        policy_id: d(13),
        originator_id: a.identity_id,
        grant_authority: AuthorityRule::AnyCurrentCoowner,
        reissue_authority: AuthorityRule::AnyCurrentCoowner,
    };
    let state =
        EncryptedCoownershipState::new(artifact, &policy, &a, 1, d(14), d(15), envelope(&a, 1, 16))
            .unwrap();
    (state, policy, a, b)
}

fn grant_b(
    state: &EncryptedCoownershipState,
    policy: &PropagationPolicy,
    a: &KnowledgeIdentity,
    b: &KnowledgeIdentity,
) -> Result<EncryptedCoownershipState, ProtocolError> {
    let grant = CoownershipGrant {
        command_digest: d(20),
        artifact_version_id: d(11),
        policy_id: d(13),
        grantor_id: a.identity_id,
        recipient_id: b.identity_id,
        recipient_key_fingerprint: b.encryption_key.fingerprint,
        envelope_digest: d(21),
    };
    state.grant_coownership(
        policy,
        b,
        &grant,
        envelope(b, 1, 21),
        &proof(a.identity_id, 20),
        &TestVerifier,
    )
}

#[test]
fn grant_expands_owner_set_without_removing_originator() {
    let (state, policy, a, b) = fixture();
    let successor = grant_b(&state, &policy, &a, &b).unwrap();
    assert_eq!(1, state.owners().len());
    assert_eq!(2, successor.owners().len());
    assert!(successor.owners().contains(&a.identity_id));
    assert!(successor.owners().contains(&b.identity_id));
}

#[test]
fn rejected_authorization_leaves_prior_state_unchanged() {
    let (state, policy, a, b) = fixture();
    let grant = CoownershipGrant {
        command_digest: d(20),
        artifact_version_id: d(11),
        policy_id: d(13),
        grantor_id: a.identity_id,
        recipient_id: b.identity_id,
        recipient_key_fingerprint: b.encryption_key.fingerprint,
        envelope_digest: d(21),
    };
    let bad_proof = AuthorizationProof {
        signer_id: a.identity_id,
        command_digest: d(20),
        signature: b"forged".to_vec(),
    };
    assert_eq!(
        Err(ProtocolError::AuthorizationFailed),
        state.grant_coownership(
            &policy,
            &b,
            &grant,
            envelope(&b, 1, 21),
            &bad_proof,
            &TestVerifier,
        )
    );
    assert_eq!(1, state.owners().len());
}

#[test]
fn wrong_recipient_key_or_epoch_is_rejected() {
    let (state, policy, a, b) = fixture();
    let grant = CoownershipGrant {
        command_digest: d(20),
        artifact_version_id: d(11),
        policy_id: d(13),
        grantor_id: a.identity_id,
        recipient_id: b.identity_id,
        recipient_key_fingerprint: d(99),
        envelope_digest: d(21),
    };
    assert_eq!(
        Err(ProtocolError::RecipientKeyMismatch),
        state.grant_coownership(
            &policy,
            &b,
            &grant,
            envelope(&b, 2, 21),
            &proof(a.identity_id, 20),
            &TestVerifier,
        )
    );
}

#[test]
fn recipient_acknowledgement_is_bound_to_current_envelope() {
    let (state, policy, a, b) = fixture();
    let state = grant_b(&state, &policy, &a, &b).unwrap();
    let acknowledgement = DecryptionAcknowledgement {
        command_digest: d(30),
        artifact_version_id: d(11),
        encryption_epoch: 1,
        recipient_id: b.identity_id,
        envelope_digest: d(21),
        challenge_digest: d(31),
    };
    let successor = state
        .acknowledge_decryption(acknowledgement, &proof(b.identity_id, 30), &TestVerifier)
        .unwrap();
    assert_eq!(
        Some(&acknowledgement),
        successor.acknowledgement_for(b.identity_id)
    );
}

#[test]
fn acknowledgement_by_non_owner_is_rejected() {
    let (state, _, _, b) = fixture();
    let acknowledgement = DecryptionAcknowledgement {
        command_digest: d(30),
        artifact_version_id: d(11),
        encryption_epoch: 1,
        recipient_id: b.identity_id,
        envelope_digest: d(21),
        challenge_digest: d(31),
    };
    assert_eq!(
        Err(ProtocolError::RecipientNotOwner),
        state.acknowledge_decryption(acknowledgement, &proof(b.identity_id, 30), &TestVerifier,)
    );
}

#[test]
fn lost_key_reissue_preserves_owner_count_and_epoch() {
    let (state, policy, a, b) = fixture();
    let state = grant_b(&state, &policy, &a, &b).unwrap();
    let request = KeyReissueRequest {
        command_digest: d(40),
        artifact_version_id: d(11),
        recipient_id: b.identity_id,
        previous_key_fingerprint: b.encryption_key.fingerprint,
        replacement_key_fingerprint: d(41),
        reason: ReissueReason::Lost,
    };
    let authorization = state
        .authorize_key_reissue(&b, &request, &proof(b.identity_id, 40), &TestVerifier)
        .unwrap();
    assert_eq!(2, authorization.owner_count);
    assert_eq!(1, authorization.encryption_epoch);
    assert_eq!(2, state.owners().len());
}

#[test]
fn compromised_key_requires_new_epoch() {
    let (state, policy, a, b) = fixture();
    let state = grant_b(&state, &policy, &a, &b).unwrap();
    let request = KeyReissueRequest {
        command_digest: d(40),
        artifact_version_id: d(11),
        recipient_id: b.identity_id,
        previous_key_fingerprint: b.encryption_key.fingerprint,
        replacement_key_fingerprint: d(41),
        reason: ReissueReason::Compromised,
    };
    assert_eq!(
        Err(ProtocolError::RequiresNewEncryptionEpoch),
        state.authorize_key_reissue(&b, &request, &proof(b.identity_id, 40), &TestVerifier,)
    );
}

#[test]
fn compromised_epoch_rotation_requires_every_owner_envelope() {
    let (state, policy, a, b) = fixture();
    let state = grant_b(&state, &policy, &a, &b).unwrap();
    let identities = BTreeMap::from([(a.identity_id, a), (b.identity_id, b)]);
    let incomplete = EpochRotation {
        command_digest: d(50),
        artifact_version_id: d(11),
        actor_id: a.identity_id,
        prior_epoch: 1,
        successor_epoch: 2,
        ciphertext_digest: d(51),
        external_location_digest: d(52),
        envelopes: vec![envelope(&a, 2, 53)],
    };
    assert_eq!(
        Err(ProtocolError::IncompleteOwnerEnvelopeCoverage),
        state.rotate_compromised_epoch(
            &policy,
            &identities,
            &incomplete,
            &proof(a.identity_id, 50),
            &TestVerifier,
        )
    );
}

#[test]
fn compromised_epoch_rotation_preserves_owners_and_replaces_ciphertext() {
    let (state, policy, a, b) = fixture();
    let state = grant_b(&state, &policy, &a, &b).unwrap();
    let identities = BTreeMap::from([(a.identity_id, a), (b.identity_id, b)]);
    let rotation = EpochRotation {
        command_digest: d(50),
        artifact_version_id: d(11),
        actor_id: a.identity_id,
        prior_epoch: 1,
        successor_epoch: 2,
        ciphertext_digest: d(51),
        external_location_digest: d(52),
        envelopes: vec![envelope(&a, 2, 53), envelope(&b, 2, 54)],
    };
    let successor = state
        .rotate_compromised_epoch(
            &policy,
            &identities,
            &rotation,
            &proof(a.identity_id, 50),
            &TestVerifier,
        )
        .unwrap();
    assert_eq!(state.owners(), successor.owners());
    assert_eq!(2, successor.encryption_epoch());
    assert_eq!(d(51), successor.ciphertext_digest());
    assert_eq!(d(52), successor.external_location_digest());
}

#[test]
fn repeated_grant_is_rejected() {
    let (state, policy, a, b) = fixture();
    let state = grant_b(&state, &policy, &a, &b).unwrap();
    assert_eq!(
        Err(ProtocolError::RecipientAlreadyOwner),
        grant_b(&state, &policy, &a, &b)
    );
}

#[test]
fn originator_only_policy_rejects_downstream_grant() {
    let (state, mut policy, a, b) = fixture();
    policy.grant_authority = AuthorityRule::OriginatorOnly;
    let state = grant_b(&state, &policy, &a, &b).unwrap();
    let c = identity(60, 61, 62, 1);
    let grant = CoownershipGrant {
        command_digest: d(63),
        artifact_version_id: d(11),
        policy_id: d(13),
        grantor_id: b.identity_id,
        recipient_id: c.identity_id,
        recipient_key_fingerprint: c.encryption_key.fingerprint,
        envelope_digest: d(64),
    };
    assert_eq!(
        Err(ProtocolError::GrantorNotAuthorized),
        state.grant_coownership(
            &policy,
            &c,
            &grant,
            envelope(&c, 1, 64),
            &proof(b.identity_id, 63),
            &TestVerifier,
        )
    );
}
