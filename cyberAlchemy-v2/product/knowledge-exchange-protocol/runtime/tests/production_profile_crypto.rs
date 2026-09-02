use cyberalchemy_knowledge_exchange_protocol::{
    Digest32,
    encrypted_durable_devnet::{
        cryptography::{ByteIdentityProvider, CryptographyError, CryptographyPort},
        model::{CryptographicContext, CryptographicProfile, RecipientBinding},
        providers::rustcrypto::{
            CONTENT_SUITE, ENVELOPE_SUITE, RustCryptoProvider, SERIALIZATION_PROFILE,
            Sha256Identity,
        },
    },
};

fn d(byte: u8) -> Digest32 {
    Digest32::try_new([byte; 32]).unwrap()
}

fn fixture() -> (
    Sha256Identity,
    RustCryptoProvider,
    CryptographicProfile,
    CryptographicContext,
    Vec<RecipientBinding>,
) {
    let identity = Sha256Identity;
    let plaintext = b"governed ontology definition bytes";
    let profile = CryptographicProfile {
        profile_id: d(1),
        content_suite: CONTENT_SUITE.to_owned(),
        envelope_suite: ENVELOPE_SUITE.to_owned(),
        serialization: SERIALIZATION_PROFILE.to_owned(),
    };
    let context = CryptographicContext {
        artifact_version_id: d(2),
        policy_id: d(3),
        encryption_epoch: 1,
        plaintext_commitment: identity.digest(plaintext),
    };
    let mut provider = RustCryptoProvider::default();
    let first = provider.generate_recipient_binding(d(4), d(5), 1).unwrap();
    let second = provider.generate_recipient_binding(d(6), d(7), 1).unwrap();
    (identity, provider, profile, context, vec![first, second])
}

#[test]
fn sha256_known_answer_is_exact() {
    let digest = Sha256Identity.digest(b"abc");
    assert_eq!(
        &[
            0xba, 0x78, 0x16, 0xbf, 0x8f, 0x01, 0xcf, 0xea, 0x41, 0x41, 0x40, 0xde, 0x5d,
            0xae, 0x22, 0x23, 0xb0, 0x03, 0x61, 0xa3, 0x96, 0x17, 0x7a, 0x9c, 0xb4, 0x10,
            0xff, 0x61, 0xf2, 0x00, 0x15, 0xad,
        ],
        digest.as_bytes()
    );
}

#[test]
fn each_bound_recipient_opens_the_same_authenticated_plaintext() {
    let (identity, provider, profile, context, recipients) = fixture();
    let plaintext = b"governed ontology definition bytes";
    let material = provider
        .prepare(&profile, &context, plaintext, &recipients, &identity)
        .unwrap();
    assert_eq!(2, material.envelopes.len());
    assert_ne!(material.ciphertext, plaintext);
    for recipient in &recipients {
        assert_eq!(
            plaintext,
            provider
                .open(&profile, &context, &material, recipient, &identity)
                .unwrap()
                .as_slice()
        );
    }
}

#[test]
fn os_randomness_produces_distinct_ciphertexts_and_envelopes() {
    let (identity, provider, profile, context, recipients) = fixture();
    let plaintext = b"governed ontology definition bytes";
    let first = provider
        .prepare(&profile, &context, plaintext, &recipients, &identity)
        .unwrap();
    let second = provider
        .prepare(&profile, &context, plaintext, &recipients, &identity)
        .unwrap();
    assert_ne!(first.ciphertext, second.ciphertext);
    assert_ne!(
        first.envelopes[0].envelope_bytes,
        second.envelopes[0].envelope_bytes
    );
}

#[test]
fn ciphertext_envelope_and_context_tampering_fail_closed() {
    let (identity, provider, profile, context, recipients) = fixture();
    let plaintext = b"governed ontology definition bytes";
    let material = provider
        .prepare(&profile, &context, plaintext, &recipients, &identity)
        .unwrap();

    let mut ciphertext_tamper = material.clone();
    *ciphertext_tamper.ciphertext.last_mut().unwrap() ^= 1;
    assert_eq!(
        Err(CryptographyError::AuthenticationFailed),
        provider.open(
            &profile,
            &context,
            &ciphertext_tamper,
            &recipients[0],
            &identity
        )
    );

    let mut envelope_tamper = material.clone();
    *envelope_tamper.envelopes[0]
        .envelope_bytes
        .last_mut()
        .unwrap() ^= 1;
    assert_eq!(
        Err(CryptographyError::AuthenticationFailed),
        provider.open(
            &profile,
            &context,
            &envelope_tamper,
            &recipients[0],
            &identity
        )
    );

    let mut wrong_context = context.clone();
    wrong_context.policy_id = d(90);
    assert_eq!(
        Err(CryptographyError::ContextMismatch),
        provider.open(
            &profile,
            &wrong_context,
            &material,
            &recipients[0],
            &identity
        )
    );
}

#[test]
fn unsupported_profile_duplicate_recipient_and_unknown_key_are_rejected() {
    let (identity, provider, profile, context, recipients) = fixture();
    let plaintext = b"governed ontology definition bytes";
    let mut wrong_profile = profile.clone();
    wrong_profile.content_suite = "not-selected".to_owned();
    assert_eq!(
        Err(CryptographyError::UnsupportedProfile),
        provider.prepare(
            &wrong_profile,
            &context,
            plaintext,
            &recipients,
            &identity
        )
    );
    assert_eq!(
        Err(CryptographyError::RecipientMismatch),
        provider.prepare(
            &profile,
            &context,
            plaintext,
            &[recipients[0].clone(), recipients[0].clone()],
            &identity
        )
    );
    let unknown = RecipientBinding {
        recipient_id: d(91),
        key_binding_id: d(92),
        key_binding_version: 1,
        key_fingerprint: d(93),
    };
    assert_eq!(
        Err(CryptographyError::RecipientMismatch),
        provider.prepare(&profile, &context, plaintext, &[unknown], &identity)
    );
}
