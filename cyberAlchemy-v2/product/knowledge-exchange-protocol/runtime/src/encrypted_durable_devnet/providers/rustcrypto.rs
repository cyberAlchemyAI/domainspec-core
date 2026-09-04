use std::collections::{BTreeMap, BTreeSet};

use chacha20poly1305::{
    XChaCha20Poly1305, XNonce,
    aead::{Aead, KeyInit, Payload},
};
use hpke::{
    Deserializable, Kem as KemTrait, OpModeR, OpModeS, Serializable,
    aead::ChaCha20Poly1305 as HpkeChaCha20Poly1305,
    kdf::HkdfSha256,
    kem::X25519HkdfSha256,
};
use sha2::{Digest, Sha256};
use zeroize::Zeroizing;

use crate::Digest32;

use super::super::{
    cryptography::{ByteIdentityProvider, CryptographyError, CryptographyPort},
    model::{
        CryptographicContext, CryptographicProfile, OpaqueRecipientEnvelope, PreparedMaterial,
        RecipientBinding,
    },
};

type Kem = X25519HkdfSha256;
type HpkeAead = HpkeChaCha20Poly1305;
type HpkeKdf = HkdfSha256;

pub const CONTENT_SUITE: &str = "XChaCha20-Poly1305-IETF";
pub const ENVELOPE_SUITE: &str = "RFC9180-BASE-X25519-HKDF-SHA256-CHACHA20POLY1305";
pub const SERIALIZATION_PROFILE: &str = "CBOR-RFC8949-CORE-DETERMINISTIC";

const CONTENT_DOMAIN: &[u8] = b"KEP:CONTENT:v1\0";
const ENVELOPE_DOMAIN: &[u8] = b"KEP:HPKE-ENVELOPE:v1\0";
const CIPHERTEXT_VERSION: u8 = 1;
const ENVELOPE_VERSION: u8 = 1;
const CONTENT_KEY_BYTES: usize = 32;
const CONTENT_NONCE_BYTES: usize = 24;

#[derive(Clone, Copy, Debug, Default)]
pub struct Sha256Identity;

impl ByteIdentityProvider for Sha256Identity {
    fn digest(&self, bytes: &[u8]) -> Digest32 {
        let mut digest: [u8; 32] = Sha256::digest(bytes).into();
        if digest == [0; 32] {
            digest = Sha256::digest([b"KEP:NONZERO-SHA256:v1\0".as_slice(), bytes].concat()).into();
        }
        Digest32::try_new(digest).expect("domain-separated SHA-256 digest must be non-zero")
    }
}

#[derive(Clone, Debug)]
struct RecipientKeyMaterial {
    public_key: Vec<u8>,
    private_key: Zeroizing<Vec<u8>>,
}

/// Recipient HPKE keys are process-local and are never serialized by this
/// provider. Tests use ephemeral instances; Devnet key custody remains a
/// separately authorized boundary.
#[derive(Clone, Debug, Default)]
pub struct RustCryptoProvider {
    recipient_keys: BTreeMap<Digest32, RecipientKeyMaterial>,
}

impl RustCryptoProvider {
    pub fn generate_recipient_binding(
        &mut self,
        recipient_id: Digest32,
        key_binding_id: Digest32,
        key_binding_version: u64,
    ) -> Result<RecipientBinding, CryptographyError> {
        if key_binding_version == 0 || self.recipient_keys.contains_key(&key_binding_id) {
            return Err(CryptographyError::InvalidMaterial);
        }
        let (private_key, public_key) = Kem::gen_keypair();
        let public_key = public_key.to_bytes().as_slice().to_vec();
        let private_key = Zeroizing::new(private_key.to_bytes().as_slice().to_vec());
        let key_fingerprint = Sha256Identity.digest(&public_key);
        self.recipient_keys.insert(
            key_binding_id,
            RecipientKeyMaterial {
                public_key,
                private_key,
            },
        );
        Ok(RecipientBinding {
            recipient_id,
            key_binding_id,
            key_binding_version,
            key_fingerprint,
        })
    }

    pub fn public_key_bytes(&self, key_binding_id: Digest32) -> Option<&[u8]> {
        self.recipient_keys
            .get(&key_binding_id)
            .map(|material| material.public_key.as_slice())
    }

    fn validate_profile(profile: &CryptographicProfile) -> Result<(), CryptographyError> {
        if profile.content_suite == CONTENT_SUITE
            && profile.envelope_suite == ENVELOPE_SUITE
            && profile.serialization == SERIALIZATION_PROFILE
        {
            Ok(())
        } else {
            Err(CryptographyError::UnsupportedProfile)
        }
    }

    fn content_aad(profile: &CryptographicProfile, context: &CryptographicContext) -> Vec<u8> {
        let mut aad = CONTENT_DOMAIN.to_vec();
        aad.extend(profile.profile_id.as_bytes());
        aad.extend(context.artifact_version_id.as_bytes());
        aad.extend(context.encryption_epoch.to_be_bytes());
        aad.extend(context.plaintext_commitment.as_bytes());
        aad.extend(context.policy_id.as_bytes());
        aad
    }

    fn envelope_info(
        profile: &CryptographicProfile,
        context: &CryptographicContext,
        recipient: &RecipientBinding,
    ) -> Vec<u8> {
        let mut info = ENVELOPE_DOMAIN.to_vec();
        info.extend(profile.profile_id.as_bytes());
        info.extend(context.artifact_version_id.as_bytes());
        info.extend(context.encryption_epoch.to_be_bytes());
        info.extend(recipient.recipient_id.as_bytes());
        info.extend(recipient.key_binding_id.as_bytes());
        info
    }

    fn envelope_aad(
        material_identity: &super::super::model::QualifiedByteIdentity,
        content_nonce: &[u8],
        context: &CryptographicContext,
        recipient: &RecipientBinding,
    ) -> Vec<u8> {
        let mut aad = Vec::new();
        aad.extend(material_identity.schema_version.to_be_bytes());
        aad.extend(material_identity.digest.as_bytes());
        aad.extend(material_identity.length.to_be_bytes());
        aad.extend(content_nonce);
        aad.extend(context.policy_id.as_bytes());
        aad.extend(recipient.key_binding_version.to_be_bytes());
        aad
    }

    fn seal_content_key(
        &self,
        profile: &CryptographicProfile,
        context: &CryptographicContext,
        recipient: &RecipientBinding,
        ciphertext_identity: &super::super::model::QualifiedByteIdentity,
        nonce: &[u8],
        content_key: &[u8],
    ) -> Result<Vec<u8>, CryptographyError> {
        let key_material = self
            .recipient_keys
            .get(&recipient.key_binding_id)
            .ok_or(CryptographyError::RecipientMismatch)?;
        if Sha256Identity.digest(&key_material.public_key) != recipient.key_fingerprint {
            return Err(CryptographyError::RecipientMismatch);
        }
        let public_key = <Kem as KemTrait>::PublicKey::from_bytes(&key_material.public_key)
            .map_err(|_| CryptographyError::InvalidMaterial)?;
        let info = Self::envelope_info(profile, context, recipient);
        let aad = Self::envelope_aad(ciphertext_identity, nonce, context, recipient);
        let (encapped_key, mut sender) =
            hpke::setup_sender::<HpkeAead, HpkeKdf, Kem>(&OpModeS::Base, &public_key, &info)
                .map_err(|_| CryptographyError::InvalidMaterial)?;
        let sealed_key = sender
            .seal(content_key, &aad)
            .map_err(|_| CryptographyError::AuthenticationFailed)?;
        let encapped_key = encapped_key.to_bytes();
        let encapped_len: u16 = encapped_key
            .len()
            .try_into()
            .map_err(|_| CryptographyError::InvalidMaterial)?;
        let sealed_len: u16 = sealed_key
            .len()
            .try_into()
            .map_err(|_| CryptographyError::InvalidMaterial)?;
        let mut envelope = Vec::with_capacity(5 + encapped_key.len() + sealed_key.len());
        envelope.push(ENVELOPE_VERSION);
        envelope.extend(encapped_len.to_be_bytes());
        envelope.extend(sealed_len.to_be_bytes());
        envelope.extend(encapped_key.as_slice());
        envelope.extend(sealed_key);
        Ok(envelope)
    }

    fn open_content_key(
        &self,
        profile: &CryptographicProfile,
        context: &CryptographicContext,
        material: &PreparedMaterial,
        envelope: &OpaqueRecipientEnvelope,
        nonce: &[u8],
    ) -> Result<Zeroizing<Vec<u8>>, CryptographyError> {
        let bytes = &envelope.envelope_bytes;
        if bytes.len() < 5 || bytes[0] != ENVELOPE_VERSION {
            return Err(CryptographyError::InvalidMaterial);
        }
        let encapped_len = u16::from_be_bytes([bytes[1], bytes[2]]) as usize;
        let sealed_len = u16::from_be_bytes([bytes[3], bytes[4]]) as usize;
        if bytes.len() != 5 + encapped_len + sealed_len {
            return Err(CryptographyError::InvalidMaterial);
        }
        let encapped_key = <Kem as KemTrait>::EncappedKey::from_bytes(&bytes[5..5 + encapped_len])
            .map_err(|_| CryptographyError::InvalidMaterial)?;
        let key_material = self
            .recipient_keys
            .get(&envelope.recipient.key_binding_id)
            .ok_or(CryptographyError::RecipientMismatch)?;
        if Sha256Identity.digest(&key_material.public_key) != envelope.recipient.key_fingerprint {
            return Err(CryptographyError::RecipientMismatch);
        }
        let private_key = <Kem as KemTrait>::PrivateKey::from_bytes(&key_material.private_key)
            .map_err(|_| CryptographyError::InvalidMaterial)?;
        let info = Self::envelope_info(profile, context, &envelope.recipient);
        let aad = Self::envelope_aad(
            &material.ciphertext_identity,
            nonce,
            context,
            &envelope.recipient,
        );
        let mut receiver = hpke::setup_receiver::<HpkeAead, HpkeKdf, Kem>(
            &OpModeR::Base,
            &private_key,
            &encapped_key,
            &info,
        )
        .map_err(|_| CryptographyError::AuthenticationFailed)?;
        let content_key = receiver
            .open(&bytes[5 + encapped_len..], &aad)
            .map_err(|_| CryptographyError::AuthenticationFailed)?;
        if content_key.len() != CONTENT_KEY_BYTES {
            return Err(CryptographyError::InvalidMaterial);
        }
        Ok(Zeroizing::new(content_key))
    }
}

impl CryptographyPort for RustCryptoProvider {
    fn prepare(
        &self,
        profile: &CryptographicProfile,
        context: &CryptographicContext,
        plaintext: &[u8],
        recipients: &[RecipientBinding],
        identity: &dyn ByteIdentityProvider,
    ) -> Result<PreparedMaterial, CryptographyError> {
        Self::validate_profile(profile)?;
        if context.encryption_epoch == 0 || identity.digest(plaintext) != context.plaintext_commitment {
            return Err(CryptographyError::ContextMismatch);
        }
        if recipients.is_empty() {
            return Err(CryptographyError::RecipientMismatch);
        }
        let mut recipient_ids = BTreeSet::new();
        let mut key_bindings = BTreeSet::new();
        if recipients.iter().any(|recipient| {
            recipient.key_binding_version == 0
                || !recipient_ids.insert(recipient.recipient_id)
                || !key_bindings.insert(recipient.key_binding_id)
        }) {
            return Err(CryptographyError::RecipientMismatch);
        }

        let mut content_key = Zeroizing::new([0_u8; CONTENT_KEY_BYTES]);
        let mut nonce_bytes = [0_u8; CONTENT_NONCE_BYTES];
        getrandom::fill(content_key.as_mut()).map_err(|_| CryptographyError::InvalidMaterial)?;
        getrandom::fill(&mut nonce_bytes).map_err(|_| CryptographyError::InvalidMaterial)?;
        let cipher = XChaCha20Poly1305::new_from_slice(content_key.as_ref())
            .map_err(|_| CryptographyError::InvalidMaterial)?;
        let nonce = XNonce::try_from(nonce_bytes.as_slice())
            .map_err(|_| CryptographyError::InvalidMaterial)?;
        let encrypted = cipher
            .encrypt(
                &nonce,
                Payload {
                    msg: plaintext,
                    aad: &Self::content_aad(profile, context),
                },
            )
            .map_err(|_| CryptographyError::AuthenticationFailed)?;
        let mut ciphertext = Vec::with_capacity(1 + CONTENT_NONCE_BYTES + encrypted.len());
        ciphertext.push(CIPHERTEXT_VERSION);
        ciphertext.extend(nonce_bytes);
        ciphertext.extend(encrypted);
        let ciphertext_identity = identity.identify(1, &ciphertext);

        let mut envelopes = Vec::with_capacity(recipients.len());
        for recipient in recipients {
            let envelope_bytes = self.seal_content_key(
                profile,
                context,
                recipient,
                &ciphertext_identity,
                &nonce_bytes,
                content_key.as_ref(),
            )?;
            envelopes.push(OpaqueRecipientEnvelope {
                recipient: recipient.clone(),
                envelope_identity: identity.identify(1, &envelope_bytes),
                envelope_bytes,
            });
        }
        Ok(PreparedMaterial {
            context: context.clone(),
            profile_id: profile.profile_id,
            ciphertext,
            ciphertext_identity,
            envelopes,
        })
    }

    fn open(
        &self,
        profile: &CryptographicProfile,
        context: &CryptographicContext,
        material: &PreparedMaterial,
        recipient: &RecipientBinding,
        identity: &dyn ByteIdentityProvider,
    ) -> Result<Vec<u8>, CryptographyError> {
        Self::validate_profile(profile)?;
        if &material.context != context || material.profile_id != profile.profile_id {
            return Err(CryptographyError::ContextMismatch);
        }
        if !material
            .ciphertext_identity
            .matches(identity.digest(&material.ciphertext), &material.ciphertext)
            || material.ciphertext.len() < 1 + CONTENT_NONCE_BYTES + 16
            || material.ciphertext[0] != CIPHERTEXT_VERSION
        {
            return Err(CryptographyError::AuthenticationFailed);
        }
        let envelope = material
            .envelopes
            .iter()
            .find(|candidate| &candidate.recipient == recipient)
            .ok_or(CryptographyError::RecipientMismatch)?;
        if !envelope
            .envelope_identity
            .matches(identity.digest(&envelope.envelope_bytes), &envelope.envelope_bytes)
        {
            return Err(CryptographyError::AuthenticationFailed);
        }
        let nonce_bytes = &material.ciphertext[1..1 + CONTENT_NONCE_BYTES];
        let content_key = self.open_content_key(profile, context, material, envelope, nonce_bytes)?;
        let cipher = XChaCha20Poly1305::new_from_slice(content_key.as_ref())
            .map_err(|_| CryptographyError::InvalidMaterial)?;
        let nonce = XNonce::try_from(nonce_bytes).map_err(|_| CryptographyError::InvalidMaterial)?;
        let plaintext = cipher
            .decrypt(
                &nonce,
                Payload {
                    msg: &material.ciphertext[1 + CONTENT_NONCE_BYTES..],
                    aad: &Self::content_aad(profile, context),
                },
            )
            .map_err(|_| CryptographyError::AuthenticationFailed)?;
        if identity.digest(&plaintext) != context.plaintext_commitment {
            return Err(CryptographyError::AuthenticationFailed);
        }
        Ok(plaintext)
    }
}
