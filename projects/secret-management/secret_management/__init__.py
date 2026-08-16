"""Opaque references plus candidate-local bounded secret consumption."""

from .execution import (
    SECRET_EXECUTION_PROFILE,
    SECRET_EXECUTION_RECEIPT_SCHEMA_ID,
    SECRET_EXECUTION_SCHEMA_VERSION,
    SECRET_EXECUTION_STATUS,
    ExecutionGrant,
    SecretExecutionError,
    SecretResolver,
    consume_secret,
)
from .secret_contract import (
    REDACTED_SECRET_REF_SCHEMA_ID,
    REDACTION_PROFILE,
    REFERENCE_STATUS,
    SECRET_REF_SCHEMA_ID,
    SecretContractError,
    SecretRef,
    project_secret_ref,
    redacted_secret_ref_envelope,
)

__all__ = [
    "REDACTED_SECRET_REF_SCHEMA_ID",
    "REDACTION_PROFILE",
    "REFERENCE_STATUS",
    "SECRET_EXECUTION_PROFILE",
    "SECRET_EXECUTION_RECEIPT_SCHEMA_ID",
    "SECRET_EXECUTION_SCHEMA_VERSION",
    "SECRET_EXECUTION_STATUS",
    "SECRET_REF_SCHEMA_ID",
    "ExecutionGrant",
    "SecretContractError",
    "SecretExecutionError",
    "SecretRef",
    "SecretResolver",
    "consume_secret",
    "project_secret_ref",
    "redacted_secret_ref_envelope",
]
