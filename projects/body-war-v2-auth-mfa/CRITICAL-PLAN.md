# Critical pilot integrity plan

Owner-directed construction candidate; authority effect none.

## Product construction

Frontier: shared compiler, live mutation proofs, 33 finite EVF witnesses and local
ORODI rehearsal pass. Critical security/persistence requirements now have eleven exact case bindings.

1. Author critical requirement/case bindings in Alch and derive their TDE keys.
2. Generate bounded JSON request validation from declared request contracts.
3. Make OAuth consumption atomic; serialize evidence attachment/disposition per
   track and commit evidence/state together; enforce duplicate identity in PostgreSQL.
4. Exercise runner isolation, permission/CSRF/OAuth negatives, duplicate races,
   transaction rollback, consent revocation and persisted state after reconnect.
5. Retain per-key integration evidence separately from EVF and formal discharge;
   run the full current pilot campaign and verify source/artifact integrity.

D65: existing definitions -> candidate contracts -> shared compiler and explicit IO
adapters -> exact test candidate -> current evidence -> review. No ontology runtime
selectors, promotion, release or production deployment are dependencies.

## Operational support

Local developer owns disposable Docker/Postgres and browser prerequisites, already
available. Migration validation uses synthetic databases only; duplicates in an
existing database must fail uniqueness migration, never be silently deleted.
Application and operations owners retain production environment, secrets, live
provider and independent production ORODI qualification as deferred residue.
These do not block local construction and are not granted by local tests.

## Implemented candidate

Three generated request contracts precede writes. Atomic OAuth consumption,
transactional evidence/state updates, shared track locks and a duplicate identity
index are implemented. Six security cases and five PostgreSQL integrity cases bind
to eleven authored requirements. Current integrated results and counts are owned
by evidence/validation.json and evidence/obligation-coverage.json.

The remaining local work is broader domain-rule and nested-response semantics.
Operational qualification requires an exact target environment, owner and service
requirements. General formal discharge remains separate from these witnesses.

## Open Questions

Which production environment and retention/service-level requirements should a
later qualification campaign bind? See README.md#open-questions.
