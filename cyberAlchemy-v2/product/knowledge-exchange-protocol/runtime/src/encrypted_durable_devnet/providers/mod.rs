//! Infrastructure providers selected by construction binding 004.
//!
//! Providers realize accepted ports but do not own protocol meaning. The
//! cryptographic profile remains test-only until independent security review.

pub mod rustcrypto;
pub mod sqlx_storage;
