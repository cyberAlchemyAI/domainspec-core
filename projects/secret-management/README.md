# Secret Management

Candidate-local L0 and L1A contracts for opaque secret references, redacted
evidence, and one fake-only bounded consumption transaction. L0 validates
high-entropy reference identifiers, derives a stable digest identity, discards
the raw identifier and purpose, and emits only redacted metadata in a
self-digesting envelope.

L1A accepts an already-issued structural `ExecutionGrant` bound to one reference,
consumer, request, and strict expiry. After every binding is validated, it permits
one call through a provider-neutral resolver boundary and one trusted callback
over an internal lease. The lease owns a mutable copy, rejects replay and callback
return values, and clears its buffer on callback success or failure. The included
resolver implementation remains test-owned and in-memory.

This prototype does not issue or authenticate grants, store real secrets, manage
credentials, integrate SOPS, read files or environment variables, run subprocesses,
use a CLI, contact a provider or network, or integrate voice generation. Its
evidence is limited to single-process, single-threaded CPython 3.12 candidate
behavior. It is not a credential store, deployment, or production security
boundary; a trusted callback can still copy material.

Run the bounded tests from the repository root with CPython 3.12:

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3.12 -m unittest discover \
  -s projects/secret-management/tests -p 'test_*.py' -v
```
